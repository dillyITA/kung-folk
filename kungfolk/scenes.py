"""Cenas do jogo: título, modo, seleção de personagem, luta e resultado."""
import math
import random
import pygame
from . import config as C
from . import fx
from .engine import (Fighter, HumanController, Projectile, InputFrame,
                     IDLE, WALK, CROUCH, ATTACK, SPECIAL, KO, WIN, KNOCKDOWN)
from .characters import CHARACTERS, draw_projectile
from .stage import ForestStage
from .ai import CPUController
from . import sprites

K = pygame.K_RETURN


def draw_preview(surf, fighter):
    """Desenha um lutador 'vivo' fora da luta (título/seleção/resultado)."""
    fighter.anim += 1
    sprites.render(surf, fighter)


# ---------------------------------------------------------------- título
class TitleScene:
    def __init__(self, game):
        self.g = game
        self.t = 0
        from .characters import SACI, CURUPIRA
        self.pv1 = Fighter(SACI, 190, 1, None)
        self.pv2 = Fighter(CURUPIRA, 770, -1, None)
        self.stage = ForestStage()

    def update(self, pressed, keys):
        self.t += 1
        if K in pressed:
            self.g.sounds.play('start')
            self.g.switch(ModeScene(self.g, self.stage))
        if pygame.K_ESCAPE in pressed:
            self.g.running = False

    def draw(self, surf):
        self.stage.draw(surf, self.t)
        veil = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        veil.fill((235, 222, 191, 90))
        surf.blit(veil, (0, 0))
        wob = math.sin(self.t * 0.05) * 4
        fx.text(surf, 'KUNG-FOLK', 92, (C.WIDTH // 2, 150 + wob),
                C.DARKRED, shadow=C.INK)
        fx.text(surf, '~ um jogo de luta do folclore brasileiro ~', 24,
                (C.WIDTH // 2, 218), C.INK)
        draw_preview(surf, self.pv1)
        draw_preview(surf, self.pv2)
        if (self.t // 30) % 2 == 0:
            fx.text(surf, 'PRESSIONE ENTER', 30, (C.WIDTH // 2, 330), C.INK)
        fx.text(surf, 'protótipo — fatia vertical', 16, (C.WIDTH // 2, C.HEIGHT - 22),
                C.SEPIA)


# ---------------------------------------------------------------- modo
class ModeScene:
    OPTIONS = ('1 JOGADOR  —  contra a máquina',
               '2 JOGADORES  —  no mesmo teclado')

    def __init__(self, game, stage=None):
        self.g = game
        self.t = 0
        self.sel = 0
        self.stage = stage or ForestStage()

    def update(self, pressed, keys):
        self.t += 1
        if pygame.K_ESCAPE in pressed:
            self.g.switch(TitleScene(self.g))
            return
        for k in (pygame.K_w, pygame.K_UP):
            if k in pressed:
                self.sel = (self.sel - 1) % 2
                self.g.sounds.play('blip')
        for k in (pygame.K_s, pygame.K_DOWN):
            if k in pressed:
                self.sel = (self.sel + 1) % 2
                self.g.sounds.play('blip')
        if K in pressed:
            self.g.sounds.play('start')
            self.g.switch(SelectScene(self.g, 'cpu' if self.sel == 0 else '2p'))

    def draw(self, surf):
        self.stage.draw(surf, self.t)
        veil = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        veil.fill((235, 222, 191, 120))
        surf.blit(veil, (0, 0))
        fx.text(surf, 'ESCOLHA O MODO', 48, (C.WIDTH // 2, 130), C.DARKRED,
                shadow=C.INK)
        for i, opt in enumerate(self.OPTIONS):
            y = 250 + i * 70
            col = C.DARKRED if i == self.sel else C.INK
            if i == self.sel:
                pygame.draw.rect(surf, C.CREAM, (150, y - 28, 660, 56))
                pygame.draw.rect(surf, C.INK, (150, y - 28, 660, 56), 3)
                arrow = 160 + math.sin(self.t * 0.15) * 5
                fx.text(surf, '>', 30, (arrow + 14, y), C.DARKRED)
            fx.text(surf, opt, 26, (C.WIDTH // 2, y), col)
        fx.text(surf, 'W/S ou setas para mover · ENTER confirma · ESC volta', 17,
                (C.WIDTH // 2, C.HEIGHT - 30), C.INK)


# ---------------------------------------------------------------- seleção
class SelectScene:
    def __init__(self, game, mode):
        self.g = game
        self.mode = mode
        self.t = 0
        self.sel = [0, 1]
        self.locked = [False, False]
        self.stage = ForestStage()
        self.previews = [Fighter(ch, 0, 1, None) for ch in CHARACTERS]
        self.start_delay = 0

    def update(self, pressed, keys):
        self.t += 1
        if pygame.K_ESCAPE in pressed:
            self.g.switch(ModeScene(self.g))
            return
        # P1
        if not self.locked[0]:
            if C.P1_KEYS['left'] in pressed or C.P1_KEYS['right'] in pressed:
                self.sel[0] = (self.sel[0] + 1) % len(CHARACTERS)
                self.g.sounds.play('blip')
            if C.P1_KEYS['punch'] in pressed or K in pressed:
                self.locked[0] = True
                self.g.sounds.play('start')
                if self.mode == 'cpu':
                    self.sel[1] = (self.sel[0] + 1) % len(CHARACTERS)
                    self.locked[1] = True
        # P2
        if self.mode == '2p' and not self.locked[1]:
            if C.P2_KEYS['left'] in pressed or C.P2_KEYS['right'] in pressed:
                self.sel[1] = (self.sel[1] + 1) % len(CHARACTERS)
                self.g.sounds.play('blip')
            if C.P2_KEYS['punch'] in pressed:
                self.locked[1] = True
                self.g.sounds.play('start')
        if all(self.locked):
            self.start_delay += 1
            if self.start_delay > 45:
                c1, c2 = CHARACTERS[self.sel[0]], CHARACTERS[self.sel[1]]
                ctrl1 = HumanController(C.P1_KEYS)
                if self.mode == 'cpu':
                    ctrl2 = CPUController(level=0.55)
                    names = ('P1', 'CPU')
                else:
                    ctrl2 = HumanController(C.P2_KEYS)
                    names = ('P1', 'P2')
                self.g.switch(FightScene(self.g, c1, c2, ctrl1, ctrl2, names))

    def draw(self, surf):
        self.stage.draw(surf, self.t)
        veil = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        veil.fill((235, 222, 191, 120))
        surf.blit(veil, (0, 0))
        fx.text(surf, 'ESCOLHA SEU LUTADOR', 44, (C.WIDTH // 2, 70), C.DARKRED,
                shadow=C.INK)
        panel_w, panel_h = 330, 330
        for i, ch in enumerate(CHARACTERS):
            px = 130 + i * (panel_w + 70)
            rect = pygame.Rect(px, 120, panel_w, panel_h)
            pygame.draw.rect(surf, C.CREAM, rect)
            pygame.draw.rect(surf, C.INK, rect, 4)
            # busto desenhado (idle), os dois se encarando
            sprites.draw_bust(surf, ch, rect.centerx, rect.y + 110,
                              max_h=196, facing=1 if i == 0 else -1)
            fx.text(surf, ch.name, 28, (rect.centerx, rect.y + 230), C.INK)
            fx.text(surf, ch.title, 17, (rect.centerx, rect.y + 262), C.SEPIA)
            # cursores
            picks = []
            if self.sel[0] == i:
                picks.append(('P1', C.RED, self.locked[0]))
            if (self.mode == '2p' or self.locked[1]) and self.sel[1] == i:
                picks.append(('P2' if self.mode == '2p' else 'CPU', C.GOLD,
                              self.locked[1]))
            for j, (tag, col, lk) in enumerate(picks):
                off = 6 + j * 8
                pygame.draw.rect(surf, col, rect.inflate(off * 2, off * 2), 4)
                fx.text(surf, tag + (' OK' if lk else ''), 20,
                        (rect.centerx - 80 + j * 160, rect.bottom + 24), col)
            # lutador animado de corpo inteiro, nas laterais
            pv = self.previews[i]
            pv.x = 62 if i == 0 else C.WIDTH - 62
            pv.y = C.HEIGHT - 20
            pv.facing = 1 if i == 0 else -1
            draw_preview(surf, pv)
        fx.text(surf, 'P1: A/D + F  ·  P2: SETAS + K  ·  ESC volta', 17,
                (C.WIDTH // 2, C.HEIGHT - 16), C.INK)


# ---------------------------------------------------------------- luta
class FightScene:
    def __init__(self, game, c1, c2, ctrl1, ctrl2, names=('P1', 'P2')):
        self.g = game
        self.c1, self.c2 = c1, c2
        self.ctrl1, self.ctrl2 = ctrl1, ctrl2
        self.names = names
        self.stage = ForestStage()
        self.particles = fx.Particles()
        self.canvas = pygame.Surface((C.WIDTH, C.HEIGHT))
        self.shadow_img = fx.make_shadow()
        self.wins = [0, 0]
        self.round_no = 1
        self.t = 0
        self.paused = False
        self.message = ''
        self.callout = None  # (texto, x, y, frames)
        self.reset_round()

    # ---------- estrutura de round ----------
    def reset_round(self):
        self.p1 = Fighter(self.c1, 290, 1, self.ctrl1)
        self.p2 = Fighter(self.c2, 670, -1, self.ctrl2)
        self.p1.opponent = self.p2
        self.p2.opponent = self.p1
        self.projectiles = []
        self.timer = C.ROUND_TIME * 60
        self.phase = 'intro'
        self.ptimer = 0
        self.hitstop = 0
        self.shake = 0.0
        self.message = ''
        self.callout = None

    def fighters(self):
        return (self.p1, self.p2)

    # ---------- atualização ----------
    def update(self, pressed, keys):
        self.t += 1
        if pygame.K_ESCAPE in pressed:
            self.paused = not self.paused
            self.g.sounds.play('blip')
        if self.paused:
            if pygame.K_q in pressed:
                self.g.switch(TitleScene(self.g))
            if K in pressed:
                self.paused = False
            return
        self.particles.update()
        if self.shake > 0:
            self.shake *= 0.82
        if self.phase == 'intro':
            self.ptimer += 1
            for f in self.fighters():
                f.update(InputFrame())
            if self.ptimer == 70:
                self.g.sounds.play('start')
            if self.ptimer >= 110:
                self.phase = 'play'
            return
        if self.phase == 'ko':
            self.ptimer += 1
            if self.ptimer < 40 and self.t % 2 == 0:
                pass  # câmera lenta no K.O.
            else:
                for f in self.fighters():
                    f.update(InputFrame())
                self._update_projectiles(resolve=False)
            if self.ptimer >= 130:
                self._next_round()
            return
        # ---- fase de jogo ----
        self._update_facing()
        inps = [f.ctrl.sample(f, pressed, keys) for f in self.fighters()]
        if self.hitstop > 0:
            self.hitstop -= 1
        else:
            for f, inp in zip(self.fighters(), inps):
                f.update(inp)
            self._consume_fx_flags()
            self._spawn_projectiles()
            self._push_apart()
            self._update_projectiles(resolve=True)
            self._resolve_strikes()
        self.timer -= 1
        self._check_round_end()

    def _update_facing(self):
        for f in self.fighters():
            if f.on_floor() and f.state in (IDLE, WALK, CROUCH):
                f.facing = 1 if f.opponent.x > f.x else -1

    def _consume_fx_flags(self):
        for f in self.fighters():
            if f.jumped or f.landed:
                self.particles.dust(f.x, C.FLOOR_Y + 6)
                f.jumped = f.landed = False
            if f.teleported:
                self.particles.poof(f.x, f.y)
                self.g.sounds.play('special')
                f.teleported = False
            if f.state in (ATTACK, SPECIAL) and f.frame == 1:
                self.g.sounds.play('whoosh')
                if f.state == SPECIAL:
                    self.callout = (f.attack.name, f.x, f.y - 175, 50)
                    self.g.sounds.play('special')

    def _spawn_projectiles(self):
        for f in self.fighters():
            if f.pending_projectile is None:
                continue
            a = f.pending_projectile
            f.pending_projectile = None
            if any(pr.owner is f for pr in self.projectiles):
                continue  # um projétil por lutador, regra clássica
            pj = a.projectile
            self.projectiles.append(Projectile(
                f, pj['kind'], f.x + f.facing * 52, f.y - pj.get('h', 64),
                pj['speed'] * f.facing, pj['damage'],
                pj.get('knockdown', False), pj.get('chip', 2)))

    def _push_apart(self):
        a, b = self.p1, self.p2
        if a.state in (KNOCKDOWN, KO) or b.state in (KNOCKDOWN, KO):
            return
        r1, r2 = a.body_rect(), b.body_rect()
        if r1.colliderect(r2):
            overlap = min(r1.right, r2.right) - max(r1.left, r2.left)
            s = overlap / 2 + 0.5
            left, right = (a, b) if a.x <= b.x else (b, a)
            left.x = max(C.STAGE_MARGIN, left.x - s)
            right.x = min(C.WIDTH - C.STAGE_MARGIN, right.x + s)

    def _update_projectiles(self, resolve):
        for pr in self.projectiles:
            pr.update()
            if not (resolve and pr.alive):
                continue
            d = self.p2 if pr.owner is self.p1 else self.p1
            if pr.rect().colliderect(d.hurtbox()) and not d.invulnerable():
                from .engine import Attack
                fake = Attack(pr.kind, 0, 0, 0, pr.damage, push=6.0,
                              knockdown=pr.knockdown, chip=pr.chip)
                self._land_hit(fake, pr.owner, d, (pr.x, pr.y))
                pr.alive = False
        self.projectiles = [p for p in self.projectiles if p.alive]

    def _resolve_strikes(self):
        for atk in self.fighters():
            d = atk.opponent
            a = atk.attack
            if (a is None or not atk.in_active() or atk.hit_done
                    or a.projectile is not None or a.teleport):
                continue
            hb = atk.attack_rect()
            if hb.colliderect(d.hurtbox()) and not d.invulnerable():
                atk.hit_done = True
                pt = hb.clip(d.hurtbox()).center
                self._land_hit(a, atk, d, pt)

    def _land_hit(self, a, attacker, d, pt):
        blocked = d.is_blocking()
        dir_ = 1 if d.x >= attacker.x else -1
        d.take_hit(a, blocked, dir_)
        if blocked:
            self.hitstop = 4
            self.shake = 3
            self.particles.block(pt[0], pt[1])
            self.g.sounds.play('block')
        else:
            self.hitstop = 8
            self.shake = 7
            self.particles.spark(pt[0], pt[1])
            self.g.sounds.play('hit')

    def _check_round_end(self):
        if self.phase != 'play':
            return
        dead = [f for f in self.fighters() if f.hp <= 0]
        if dead:
            for f in dead:
                f.set_state(KO)
                f.vy = -8
                f.vx = -f.facing * 4.5
            alive = [f for f in self.fighters() if f.hp > 0]
            for f in alive:
                f.set_state(WIN)
            self.round_winner = alive[0] if len(alive) == 1 else None
            self.message = 'K.O.!'
            self.phase = 'ko'
            self.ptimer = 0
            self.g.sounds.play('ko')
        elif self.timer <= 0:
            if self.p1.hp > self.p2.hp:
                self.round_winner = self.p1
            elif self.p2.hp > self.p1.hp:
                self.round_winner = self.p2
            else:
                self.round_winner = None
            if self.round_winner:
                self.round_winner.set_state(WIN)
            self.message = 'TEMPO!'
            self.phase = 'ko'
            self.ptimer = 0
            self.g.sounds.play('ko')

    def _next_round(self):
        w = self.round_winner
        if w is self.p1:
            self.wins[0] += 1
        elif w is self.p2:
            self.wins[1] += 1
        if max(self.wins) >= C.WINS_TO_TAKE:
            i = 0 if self.wins[0] > self.wins[1] else 1
            char = (self.c1, self.c2)[i]
            self.g.switch(ResultScene(self.g, char, self.names[i]))
            return
        self.round_no += 1
        self.reset_round()

    # ---------- desenho ----------
    def draw(self, surf):
        cv = self.canvas
        cv.fill(C.PAPER)
        self.stage.draw(cv, self.t)
        # sombras
        for f in self.fighters():
            h = C.FLOOR_Y - f.y
            w = max(36, 86 - h * 0.25)
            img = pygame.transform.smoothscale(self.shadow_img, (int(w), 18))
            cv.blit(img, (int(f.x - w / 2), C.FLOOR_Y + 2))
        # projéteis e lutadores (atacante por cima)
        order = sorted(self.fighters(),
                       key=lambda f: 1 if f.state in (ATTACK, SPECIAL) else 0)
        for f in order:
            sprites.render(cv, f)
        for pr in self.projectiles:
            draw_projectile(cv, pr)
        self.particles.draw(cv)
        self._draw_hud(cv)
        self._draw_messages(cv)
        # tremor de tela
        ox = random.uniform(-self.shake, self.shake)
        oy = random.uniform(-self.shake, self.shake) * 0.6
        surf.fill(C.INK)
        surf.blit(cv, (int(ox), int(oy)))
        if self.paused:
            veil = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
            veil.fill((41, 31, 27, 150))
            surf.blit(veil, (0, 0))
            fx.text(surf, 'PAUSA', 56, (C.WIDTH // 2, 220), C.CREAM)
            fx.text(surf, 'ENTER continua  ·  Q sai pro menu', 24,
                    (C.WIDTH // 2, 290), C.CREAM)

    def _draw_hud(self, surf):
        bw, bh, y = 360, 26, 30
        specs = ((40, self.p1, self.c1, self.names[0], 0, False),
                 (C.WIDTH - 40 - bw, self.p2, self.c2, self.names[1], 1, True))
        for x, f, ch, tag, wi, flip in specs:
            # placa creme atrás de nome + estrelas (legível sobre a copa escura)
            plate = pygame.Rect(x - 4, y + bh + 2, bw + 8, 28)
            pygame.draw.rect(surf, C.CREAM, plate)
            pygame.draw.rect(surf, C.INK, plate, 3)
            pygame.draw.rect(surf, C.INK, (x - 4, y - 4, bw + 8, bh + 8))
            pygame.draw.rect(surf, C.CREAM, (x, y, bw, bh))
            ratio = max(0.0, f.hp / ch.hp)
            fw = int(bw * ratio)
            if fw > 0:
                fill_x = x + (bw - fw) if flip else x
                pygame.draw.rect(surf, C.RED, (fill_x, y, fw, bh))
                pygame.draw.rect(surf, C.GOLD, (fill_x, y + 3, fw, 4))
            name_x = (x + 6) if not flip else (x + bw - 6)
            label = '%s — %s' % (ch.name, tag)
            img = fx.font(18).render(label, True, C.INK)
            r = img.get_rect()
            r.topleft = (name_x, y + bh + 7)
            if flip:
                r.topright = (name_x, y + bh + 7)
            surf.blit(img, r)
            # estrelas de round
            for s in range(C.WINS_TO_TAKE):
                sx = (x + bw - 50 + s * 26) if not flip else (x + 50 - s * 26)
                col = C.GOLD if s < self.wins[wi] else C.SEPIA
                pts = fx.star_points(sx, y + bh + 16, 9, 4, 5, -math.pi / 2)
                pygame.draw.polygon(surf, col, [(int(a), int(b)) for a, b in pts])
                pygame.draw.polygon(surf, C.INK,
                                    [(int(a), int(b)) for a, b in pts], 2)
        # relógio
        secs = max(0, self.timer // 60)
        pygame.draw.circle(surf, C.INK, (C.WIDTH // 2, y + 22), 34)
        pygame.draw.circle(surf, C.CREAM, (C.WIDTH // 2, y + 22), 29)
        fx.text(surf, str(secs), 30, (C.WIDTH // 2, y + 22), C.INK)
        fx.text(surf, 'ROUND %d' % self.round_no, 15, (C.WIDTH // 2, y + 64), C.INK)

    def _draw_messages(self, surf):
        cx, cy = C.WIDTH // 2, 250
        wob = 1 + 0.08 * math.sin(self.t * 0.25)
        if self.phase == 'intro':
            if self.ptimer < 70:
                fx.text(surf, 'ROUND %d' % self.round_no, int(72 * wob), (cx, cy),
                        C.DARKRED, shadow=C.INK)
            else:
                fx.text(surf, 'LUTEM!', int(84 * wob), (cx, cy), C.RED, shadow=C.INK)
            if self.round_no == 1:
                plate = pygame.Rect(0, 0, 620, 52)
                plate.center = (cx, C.HEIGHT - 32)
                pygame.draw.rect(surf, C.CREAM, plate)
                pygame.draw.rect(surf, C.INK, plate, 3)
                fx.text(surf, 'P1: WASD + F soco / G chute   ·   P2: setas + K / L', 17,
                        (cx, C.HEIGHT - 42), C.INK)
                fx.text(surf, 'ESPECIAL:  baixo, baixo-frente, frente + golpe', 17,
                        (cx, C.HEIGHT - 22), C.DARKRED)
        elif self.phase == 'ko' and self.message:
            fx.text(surf, self.message, int(96 * wob), (cx, cy), C.DARKRED,
                    shadow=C.INK)
            if self.ptimer > 60 and self.round_winner is not None:
                who = self.names[0] if self.round_winner is self.p1 else self.names[1]
                fx.text(surf, '%s vence o round!' % who, 30, (cx, cy + 70), C.INK)
        if self.callout:
            txt, x, y, fr = self.callout
            fx.text(surf, txt, 24, (int(x), int(y - (50 - fr) * 0.6)), C.DARKRED,
                    shadow=C.CREAM)
            fr -= 1
            self.callout = (txt, x, y, fr) if fr > 0 else None


# ---------------------------------------------------------------- resultado
class ResultScene:
    def __init__(self, game, char, tag):
        self.g = game
        self.char = char
        self.tag = tag
        self.t = 0
        self.stage = ForestStage()
        self.pv = Fighter(char, C.WIDTH // 2, 1, None)
        self.pv.set_state(WIN)
        self.particles = fx.Particles()

    def update(self, pressed, keys):
        self.t += 1
        if self.t % 14 == 0:
            self.particles.spark(random.randint(140, C.WIDTH - 140),
                                 random.randint(90, 260), 5)
        self.particles.update()
        if K in pressed or pygame.K_ESCAPE in pressed:
            self.g.sounds.play('start')
            self.g.switch(TitleScene(self.g))

    def draw(self, surf):
        self.stage.draw(surf, self.t)
        veil = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        veil.fill((235, 222, 191, 110))
        surf.blit(veil, (0, 0))
        wob = 1 + 0.06 * math.sin(self.t * 0.2)
        fx.text(surf, 'VITÓRIA!', int(76 * wob), (C.WIDTH // 2, 120), C.DARKRED,
                shadow=C.INK)
        fx.text(surf, '%s  (%s)' % (self.char.name, self.tag), 34,
                (C.WIDTH // 2, 195), C.INK)
        fx.text(surf, self.char.title, 20, (C.WIDTH // 2, 232), C.SEPIA)
        draw_preview(surf, self.pv)
        self.particles.draw(surf)
        if (self.t // 30) % 2 == 0:
            fx.text(surf, 'ENTER volta ao título', 22, (C.WIDTH // 2, C.HEIGHT - 40),
                    C.INK)
