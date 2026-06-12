"""CPU: oponente controlado por máquina, com nível de dificuldade 0..1."""
import random
from .engine import InputFrame


class CPUController:
    def __init__(self, level=0.55, seed=None):
        self.rng = random.Random(seed)
        self.level = level
        self.timer = 0
        self.mode = 'wait'

    def sample(self, f, pressed, keys):
        inp = InputFrame()
        opp = f.opponent
        if opp is None:
            return inp
        dist = abs(opp.x - f.x)
        fwd = 1 if opp.x > f.x else -1
        r = self.rng.random

        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.rng.randint(int(26 - self.level * 14), 38)
            if dist > 280:
                if r() < 0.20 + 0.35 * self.level:
                    self.mode = 'special_p'
                else:
                    self.mode = self.rng.choice(
                        ['approach', 'approach', 'approach', 'jumpin'])
            elif dist > 130:
                self.mode = self.rng.choice(
                    ['approach', 'approach', 'jumpin', 'special_k', 'wait'])
            else:
                self.mode = self.rng.choice(
                    ['poke', 'poke', 'kick', 'crouch_poke', 'retreat', 'jumpback'])

        m = self.mode
        if m == 'approach':
            inp.dir_x = fwd
        elif m == 'retreat':
            inp.dir_x = -fwd
        elif m == 'jumpin':
            inp.dir_x = fwd
            if f.on_floor() and not f.busy():
                inp.jump = True
            self.mode = 'air_attack'
        elif m == 'jumpback':
            inp.dir_x = -fwd
            if f.on_floor() and not f.busy():
                inp.jump = True
            self.mode = 'wait'
        elif m == 'air_attack':
            inp.dir_x = fwd
            if not f.on_floor() and dist < 120 and r() < 0.35:
                inp.kick = True
                self.mode = 'wait'
        elif m == 'poke':
            if dist < 115:
                inp.punch = r() < 0.18 + 0.2 * self.level
            else:
                inp.dir_x = fwd
        elif m == 'crouch_poke':
            inp.crouch = True
            if dist < 110:
                inp.punch = r() < 0.15 + 0.2 * self.level
        elif m == 'kick':
            if dist < 135:
                inp.kick = r() < 0.15 + 0.18 * self.level
            else:
                inp.dir_x = fwd
        elif m == 'special_p':
            if f.on_floor() and not f.busy():
                inp.special_p = True
            self.mode = 'wait'
        elif m == 'special_k':
            if f.on_floor() and not f.busy() and r() < 0.6:
                inp.special_k = True
            else:
                inp.dir_x = fwd
            self.mode = 'wait'

        # bloqueio reativo: segura pra trás quando o oponente ataca de perto
        if (opp.attack is not None and opp.state in ('attack', 'special')
                and dist < 170 and r() < self.level * 0.5):
            inp.dir_x = -fwd
            inp.punch = inp.kick = inp.jump = False
        return inp
