"""Efeitos: fontes, partículas cartoon, filtro de filme vintage e sons sintetizados."""
import math
import random
import pygame
from . import config as C

_fonts = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont(
            'georgia,palatino,timesnewroman,serif', size, bold=bold)
    return _fonts[key]


def text(surf, s, size, pos, color=C.INK, center=True, shadow=None, bold=True):
    f = font(size, bold)
    img = f.render(s, True, color)
    r = img.get_rect(center=pos) if center else img.get_rect(topleft=pos)
    if shadow:
        surf.blit(f.render(s, True, shadow), r.move(3, 3))
    surf.blit(img, r)
    return r


def make_shadow():
    s = pygame.Surface((90, 22), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (30, 22, 16, 70), s.get_rect())
    return s


def star_points(cx, cy, r_out, r_in, n=4, rot=0.0):
    pts = []
    for i in range(n * 2):
        ang = rot + math.pi * i / n
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    return pts


class Particles:
    """Partículas cartoon: faíscas-estrela, poeira, fumaça e brasas."""

    def __init__(self):
        self.items = []

    def _add(self, kind, x, y, vx, vy, life, size):
        self.items.append(dict(kind=kind, x=x, y=y, vx=vx, vy=vy,
                               life=life, age=0, size=size,
                               rot=random.uniform(0, math.pi)))

    def spark(self, x, y, n=9):
        for _ in range(n):
            a = random.uniform(0, math.tau)
            sp = random.uniform(2, 7)
            self._add('star', x, y, math.cos(a) * sp, math.sin(a) * sp - 2,
                      random.randint(10, 20), random.uniform(5, 11))

    def block(self, x, y):
        for _ in range(5):
            a = random.uniform(-2.4, -0.7)
            self._add('dust', x, y, math.cos(a) * 3, math.sin(a) * 3,
                      random.randint(8, 14), random.uniform(3, 6))

    def dust(self, x, y, n=6):
        for _ in range(n):
            self._add('dust', x + random.uniform(-14, 14), y,
                      random.uniform(-1.6, 1.6), random.uniform(-2.2, -0.4),
                      random.randint(12, 22), random.uniform(4, 9))

    def poof(self, x, y, n=12):
        for _ in range(n):
            a = random.uniform(0, math.tau)
            sp = random.uniform(1, 4)
            self._add('smoke', x + random.uniform(-10, 10), y - random.uniform(0, 90),
                      math.cos(a) * sp, math.sin(a) * sp - 1,
                      random.randint(14, 26), random.uniform(6, 13))

    def flame(self, x, y, n=8):
        for _ in range(n):
            self._add('flame', x, y + random.uniform(-16, 16),
                      random.uniform(-2, 2), random.uniform(-2.5, -0.5),
                      random.randint(10, 18), random.uniform(5, 10))

    def update(self):
        for p in self.items:
            p['age'] += 1
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.12 if p['kind'] == 'star' else -0.02
            p['rot'] += 0.25
        self.items = [p for p in self.items if p['age'] < p['life']]

    def draw(self, surf):
        for p in self.items:
            k = 1 - p['age'] / p['life']
            s = max(1.5, p['size'] * k)
            x, y = int(p['x']), int(p['y'])
            if p['kind'] == 'star':
                pts = star_points(x, y, s * 1.6, s * 0.55, 4, p['rot'])
                pygame.draw.polygon(surf, C.INK, [(px + 1, py + 1) for px, py in pts])
                pygame.draw.polygon(surf, C.WHITE_W, pts)
            elif p['kind'] == 'dust':
                pygame.draw.circle(surf, C.SEPIA, (x, y), int(s))
            elif p['kind'] == 'smoke':
                pygame.draw.circle(surf, C.SMOKE, (x, y), int(s))
                pygame.draw.circle(surf, C.INK, (x, y), int(s), 1)
            else:  # flame
                pygame.draw.circle(surf, C.FIRE_1, (x, y), int(s))
                pygame.draw.circle(surf, C.FIRE_2, (x, y), max(1, int(s * 0.55)))


class Vintage:
    """Pós-processamento: vinheta, grão de filme, tom sépia, flicker e arranhões."""

    def __init__(self):
        self.t = 0
        self.vignette = self._build_vignette()
        self.grain = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        self.tint = pygame.Surface((C.WIDTH, C.HEIGHT))
        self.tint.fill((250, 240, 220))
        self.flick = pygame.Surface((C.WIDTH, C.HEIGHT))
        self.flick.fill((255, 250, 235))
        self.scratch_x = None
        self.scratch_t = 0

    def _build_vignette(self):
        v = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        n = 70
        for j in range(n):
            d = j * 2
            alpha = int(((n - j) / n) ** 2 * 110)
            pygame.draw.rect(v, (24, 14, 10, alpha),
                             pygame.Rect(d, d, C.WIDTH - 2 * d, C.HEIGHT - 2 * d), 2)
        return v

    def apply(self, surf):
        self.t += 1
        if self.t % 3 == 0:
            self.grain.fill((0, 0, 0, 0))
            for _ in range(150):
                x = random.randrange(C.WIDTH)
                y = random.randrange(C.HEIGHT)
                col = random.choice(((30, 22, 16), (240, 230, 200)))
                self.grain.fill((col[0], col[1], col[2], random.randint(8, 26)),
                                (x, y, 2, 2))
        surf.blit(self.tint, (0, 0), special_flags=pygame.BLEND_MULT)
        surf.blit(self.grain, (0, 0))
        surf.blit(self.vignette, (0, 0))
        self.flick.set_alpha(random.randint(0, 7))
        surf.blit(self.flick, (0, 0))
        if self.scratch_t <= 0 and random.random() < 0.007:
            self.scratch_x = random.randrange(60, C.WIDTH - 60)
            self.scratch_t = random.randint(3, 7)
        if self.scratch_t > 0:
            self.scratch_t -= 1
            pygame.draw.line(surf, (70, 58, 46), (self.scratch_x, 0),
                             (self.scratch_x + random.randint(-2, 2), C.HEIGHT), 1)


class SoundBank:
    """SFX retrô sintetizados com numpy; silencioso se numpy/áudio faltarem."""

    def __init__(self):
        self.ok = False
        self.snd = {}
        try:
            import numpy as np
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 2, 256)
            self._build(np)
            self.ok = True
        except Exception:
            pass

    def _mk(self, np, dur, f0, f1=None, vol=0.5, decay=9.0, noise=0.0, square=0.5):
        sr = 22050
        n = int(sr * dur)
        t = np.arange(n) / sr
        fr = np.linspace(f0, f1 if f1 is not None else f0, n)
        phase = np.cumsum(2 * np.pi * fr / sr)
        w = np.sin(phase) * (1 - square) + np.sign(np.sin(phase)) * square
        if noise:
            w = w * (1 - noise) + np.random.uniform(-1, 1, n) * noise
        w = w * np.exp(-decay * t) * vol
        d = (w * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(np.column_stack([d, d])))

    def _build(self, np):
        self.snd = dict(
            hit=self._mk(np, 0.13, 150, 55, vol=0.55, decay=22, noise=0.5),
            block=self._mk(np, 0.07, 460, 380, vol=0.35, decay=30, square=0.8),
            whoosh=self._mk(np, 0.11, 900, 300, vol=0.16, decay=16, noise=0.95),
            special=self._mk(np, 0.22, 200, 540, vol=0.4, decay=9, square=0.6),
            ko=self._mk(np, 0.75, 170, 48, vol=0.6, decay=3.5, noise=0.15),
            blip=self._mk(np, 0.07, 520, vol=0.3, decay=20, square=0.7),
            start=self._mk(np, 0.28, 330, 660, vol=0.4, decay=6, square=0.5),
        )

    def play(self, name):
        if self.ok and name in self.snd:
            try:
                self.snd[name].play()
            except Exception:
                pass
