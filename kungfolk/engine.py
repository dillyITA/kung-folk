"""Núcleo de luta: estados, física, ataques, projéteis e leitura de comandos."""
from collections import deque
from dataclasses import dataclass
import pygame
from . import config as C

# Estados do lutador
IDLE, WALK, JUMP, CROUCH = 'idle', 'walk', 'jump', 'crouch'
ATTACK, SPECIAL = 'attack', 'special'
HITSTUN, BLOCKSTUN, KNOCKDOWN = 'hitstun', 'blockstun', 'knockdown'
KO, WIN = 'ko', 'win'


@dataclass
class Attack:
    name: str
    startup: int
    active: int
    recovery: int
    damage: int
    hitstun: int = 14
    blockstun: int = 9
    push: float = 5.0
    hitbox: tuple = (30, 78, 56, 34)   # (dx frente, altura do centro, w, h)
    knockdown: bool = False
    lunge: float = 0.0
    chip: int = 0
    projectile: dict = None
    teleport: bool = False
    aerial: bool = False
    anim: str = 'punch'                # tag usada pelo desenho procedural


@dataclass
class InputFrame:
    dir_x: int = 0
    jump: bool = False
    crouch: bool = False
    punch: bool = False
    kick: bool = False
    special_p: bool = False
    special_k: bool = False


class Projectile:
    """Projétil de especial (redemoinho, bola de fogo...)."""

    def __init__(self, owner, kind, x, y, vx, damage, knockdown=False, chip=2):
        self.owner, self.kind = owner, kind
        self.x, self.y, self.vx = x, y, vx
        self.damage, self.knockdown, self.chip = damage, knockdown, chip
        self.age = 0
        self.alive = True

    def rect(self):
        r = pygame.Rect(0, 0, 52, 56)
        r.center = (int(self.x), int(self.y))
        return r

    def update(self):
        self.x += self.vx
        self.age += 1
        if self.x < -60 or self.x > C.WIDTH + 60:
            self.alive = False


class HumanController:
    """Lê teclado e detecta o comando de especial (↓ ↘ → + botão)."""

    def __init__(self, keymap):
        self.km = keymap
        self.hist = deque([5] * 22, maxlen=22)  # notação numpad relativa ao facing

    def sample(self, f, pressed, keys):
        km = self.km
        dx = (1 if keys[km['right']] else 0) - (1 if keys[km['left']] else 0)
        down = bool(keys[km['down']])
        fx = dx * f.facing  # frente = positivo
        if down:
            rel = 3 if fx > 0 else (1 if fx < 0 else 2)
        else:
            rel = 6 if fx > 0 else (4 if fx < 0 else 5)
        self.hist.append(rel)

        inp = InputFrame(dir_x=dx, jump=km['up'] in pressed, crouch=down)
        if km['punch'] in pressed:
            if self._qcf():
                inp.special_p = True
            else:
                inp.punch = True
        if km['kick'] in pressed:
            if self._qcf():
                inp.special_k = True
            else:
                inp.kick = True
        return inp

    def _qcf(self):
        """Quarto de círculo pra frente: um ↓ seguido de → (ou ↘) recente."""
        h = list(self.hist)
        saw_fwd_at = None
        for i in range(len(h) - 1, -1, -1):
            back = len(h) - 1 - i
            if saw_fwd_at is None:
                if h[i] in (6, 3):
                    saw_fwd_at = back
                elif back > 4:
                    return False
            else:
                if h[i] in (2, 1):
                    return True
                if back > 17:
                    return False
        return False


class Fighter:
    """Um lutador: máquina de estados + física + frame data."""

    def __init__(self, char, x, facing, controller):
        self.char = char
        self.x, self.y = float(x), float(C.FLOOR_Y)
        self.vx, self.vy = 0.0, 0.0
        self.facing = facing
        self.hp = char.hp
        self.state = IDLE
        self.frame = 0          # frames no estado atual
        self.anim = 0           # contador global de animação
        self.walk_phase = 0.0   # distância acumulada — sincroniza o ciclo de andar
        self.attack = None
        self.hit_done = False
        self.stun = 0
        self.down_until = 9999
        self.invuln = 0
        self.crouching = False
        self.hold_x = 0
        self.squash = 0          # frames de "amassada" ao aterrissar
        self.ctrl = controller
        self.opponent = None
        self.pending_projectile = None
        # flags de FX consumidas pela cena
        self.jumped = False
        self.landed = False
        self.teleported = False

    # ---------- consultas ----------
    def on_floor(self):
        return self.y >= C.FLOOR_Y - 0.5

    def set_state(self, s):
        if s != self.state:
            self.state = s
            self.frame = 0

    def busy(self):
        return self.state in (ATTACK, SPECIAL, HITSTUN, BLOCKSTUN, KNOCKDOWN, KO, WIN)

    def invulnerable(self):
        return self.invuln > 0 or self.state in (KNOCKDOWN, KO)

    def is_blocking(self):
        return (self.on_floor()
                and self.state in (IDLE, WALK, CROUCH, BLOCKSTUN)
                and self.hold_x == -self.facing)

    def hurtbox(self):
        if self.state in (KNOCKDOWN, KO):
            r = pygame.Rect(0, 0, 90, 36)
            r.center = (int(self.x), int(self.y - 18))
        elif not self.on_floor():
            r = pygame.Rect(0, 0, 50, 100)
            r.center = (int(self.x), int(self.y - 80))
        elif self.crouching or self.state == CROUCH:
            r = pygame.Rect(0, 0, 56, 92)
            r.center = (int(self.x), int(self.y - 46))
        else:
            r = pygame.Rect(0, 0, 52, 144)
            r.center = (int(self.x), int(self.y - 72))
        return r

    def body_rect(self):
        r = pygame.Rect(0, 0, 44, 120)
        r.center = (int(self.x), int(self.y - 60))
        return r

    def in_active(self):
        a = self.attack
        return a and a.startup <= self.frame < a.startup + a.active

    def attack_rect(self):
        # hitbox derivada da arte (ponta do golpe) quando há sprites; senão, a
        # estática do frame data (boneco procedural).
        ss = getattr(self.char, 'sprites', None)
        if ss is not None:
            r = ss.strike_rect(self)
            if r is not None:
                return r
        a = self.attack
        r = pygame.Rect(0, 0, a.hitbox[2], a.hitbox[3])
        r.center = (int(self.x + self.facing * a.hitbox[0]), int(self.y - a.hitbox[1]))
        return r

    # ---------- ações ----------
    def start_attack(self, a, st=ATTACK):
        self.attack = a
        self.hit_done = False
        if not a.aerial:
            self.vx = 0
        self.set_state(st)

    def take_hit(self, a, blocked, dir_):
        """dir_: sentido do empurrão (pra longe do atacante)."""
        if blocked:
            self.hp = max(0, self.hp - a.chip)
            self.stun = a.blockstun
            self.set_state(BLOCKSTUN)
            self.vx = dir_ * a.push * 0.9
        else:
            self.hp = max(0, self.hp - a.damage)
            if a.knockdown or not self.on_floor():
                self.set_state(KNOCKDOWN)
                self.vy = -7.5
                self.vx = dir_ * 4.0
                self.down_until = 9999
            else:
                self.stun = a.hitstun
                self.set_state(HITSTUN)
                self.vx = dir_ * a.push

    # ---------- atualização ----------
    def update(self, inp):
        self.anim += 1
        self.frame += 1
        self.walk_phase += abs(self.vx)
        self.hold_x = inp.dir_x
        if self.invuln > 0:
            self.invuln -= 1
        if self.squash > 0:
            self.squash -= 1
        st = self.state

        if st in (HITSTUN, BLOCKSTUN):
            self.vx *= 0.86
            if self.frame >= self.stun:
                self.set_state(IDLE)
        elif st == KNOCKDOWN:
            if self.on_floor() and self.vy >= 0:
                self.vx *= 0.8
                if self.frame >= self.down_until:
                    self.set_state(IDLE)
                    self.invuln = 28
            # rede de segurança: levanta à força após um teto de tempo, mesmo
            # que down_until nunca tenha sido fixado (evita ficar caído pra
            # sempre num caminho raro).
            if self.state == KNOCKDOWN and self.frame >= 160:
                self.y = C.FLOOR_Y
                self.vy = 0
                self.set_state(IDLE)
                self.invuln = 28
        elif st in (KO, WIN):
            self.vx *= 0.8
        elif st in (ATTACK, SPECIAL):
            a = self.attack
            if a.lunge and self.frame < a.startup + a.active:
                self.vx = a.lunge * self.facing
            elif not a.aerial:
                self.vx = 0
            if self.frame == a.startup:
                if a.projectile:
                    self.pending_projectile = a
                if a.teleport and self.opponent is not None:
                    side = 1 if self.x < self.opponent.x else -1
                    self.x = self.opponent.x + side * 80
                    self.invuln = 12
                    self.teleported = True
            if self.frame >= a.startup + a.active + a.recovery:
                self.attack = None
                self.set_state(IDLE if self.on_floor() else JUMP)
        else:
            if self.on_floor():
                self.crouching = inp.crouch
                mv = self.char.moves
                if inp.special_p and 'special_p' in mv:
                    self.start_attack(mv['special_p'], SPECIAL)
                elif inp.special_k and 'special_k' in mv:
                    self.start_attack(mv['special_k'], SPECIAL)
                elif inp.punch:
                    self.start_attack(mv['crouch_punch'] if self.crouching else mv['punch'])
                elif inp.kick and not self.crouching:
                    self.start_attack(mv['kick'])
                elif inp.jump and not self.crouching:
                    self.vy = self.char.jump
                    self.vx = inp.dir_x * self.char.speed
                    self.set_state(JUMP)
                    self.jumped = True
                elif self.crouching:
                    self.vx = 0
                    self.set_state(CROUCH)
                else:
                    self.vx = inp.dir_x * self.char.speed
                    self.set_state(WALK if inp.dir_x else IDLE)
            else:
                if (inp.punch or inp.kick) and not self.attack:
                    self.start_attack(self.char.moves['air_kick'])

        # física
        self.x += self.vx
        if not self.on_floor() or self.vy < 0:
            self.vy += C.GRAVITY
            self.y += self.vy
            if self.y >= C.FLOOR_Y:
                self.y = C.FLOOR_Y
                self.vy = 0
                self.landed = True
                self.squash = 7
                if self.state == JUMP:
                    self.set_state(IDLE)
                elif self.state == ATTACK and self.attack and self.attack.aerial:
                    self.attack = None
                    self.set_state(IDLE)
                elif self.state == KNOCKDOWN:
                    self.down_until = self.frame + 42
                    self.vx *= 0.4
        self.x = max(C.STAGE_MARGIN, min(C.WIDTH - C.STAGE_MARGIN, self.x))
