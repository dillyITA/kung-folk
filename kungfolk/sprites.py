"""Pipeline de sprites desenhados (Nano Banana etc.):

  PNG (fundo magenta)  →  chroma-key  →  fatiamento automático em frames
                       →  escala  →  player de animação por estado do lutador.

Tudo com FALLBACK: animação que não tiver PNG cai no desenho procedural,
permitindo migrar o personagem uma animação de cada vez. Os PNGs ficam em
assets/sprites/<dir>/<animacao>.png — cada um uma TIRA HORIZONTAL de frames
do personagem virado para a DIREITA (o motor espelha para a esquerda)."""
import os
import pygame
from . import config as C
from .engine import (IDLE, WALK, JUMP, CROUCH, ATTACK, SPECIAL,
                     HITSTUN, BLOCKSTUN, KNOCKDOWN, KO, WIN)

ASSET_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'sprites')

TARGET_H = 156  # altura do personagem em tela (px) — casa com o procedural

# animações reconhecidas. loop=True cicla pelo tempo no fps indicado.
ANIMS = {
    'idle':         dict(loop=True, fps=8),
    'walk':         dict(loop=True, fps=12),
    'jump':         dict(loop=False),
    'crouch':       dict(loop=True, fps=6),
    'punch':        dict(loop=False),
    'crouch_punch': dict(loop=False),
    'kick':         dict(loop=False),
    'air_kick':     dict(loop=False),
    'special_p':    dict(loop=False),
    'special_k':    dict(loop=False),
    'hitstun':      dict(loop=False),
    'block':        dict(loop=True, fps=6),
    'knockdown':    dict(loop=False),
    'ko':           dict(loop=True, fps=3),
    'win':          dict(loop=True, fps=8),
}

# tag de ataque (engine) -> animação base
_TAG2ANIM = {'punch': 'punch', 'cpunch': 'crouch_punch', 'kick': 'kick',
             'air': 'air_kick', 'cast': 'special_p'}


def _attack_anim(a):
    if a.teleport:
        return 'special_k'
    if a.anim == 'whirl_cast':       # Saci: Redemoinho (projétil)
        return 'special_p'
    if a.anim == 'lunge':            # Curupira: Trupida
        return 'special_k'
    return _TAG2ANIM.get(a.anim, 'punch')


def resolve(f):
    """(nome_da_animacao, modo_de_frame) para o estado atual do lutador."""
    s = f.state
    if s == KO:
        return 'ko', 'loop'
    if s == WIN:
        return 'win', 'loop'
    if s == KNOCKDOWN:
        return 'knockdown', 'progress'
    if s == HITSTUN:
        return 'hitstun', 'progress'
    if s == BLOCKSTUN:
        return 'block', 'loop'
    if s in (ATTACK, SPECIAL) and f.attack is not None:
        return _attack_anim(f.attack), 'attack'
    if not f.on_floor():
        return 'jump', 'jump'
    if s == CROUCH or f.crouching:
        return 'crouch', 'loop'
    if s == WALK:
        return 'walk', 'loop'
    return 'idle', 'loop'


# ---------------- chroma-key + fatiamento ----------------
def _runs(col, gap_min, min_w):
    """Segmenta um vetor booleano de colunas em corridas de conteúdo,
    fundindo lacunas menores que gap_min e descartando fragmentos < min_w."""
    raw, i, n = [], 0, len(col)
    while i < n:
        if col[i]:
            j = i
            while j < n and col[j]:
                j += 1
            raw.append([i, j])
            i = j
        else:
            i += 1
    merged = []
    for r in raw:
        if merged and r[0] - merged[-1][1] < gap_min:
            merged[-1][1] = r[1]
        else:
            merged.append(r[:])
    return [(a, b) for a, b in merged if b - a >= min_w]


def chroma_slice(path, tol=72, edge=28):
    """Carrega um PNG de fundo magenta e devolve a lista de frames recortados
    (cada um com alpha e cortado no bounding box do conteúdo)."""
    import numpy as np
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    rgb = pygame.surfarray.array3d(img).astype(np.int16)          # (w, h, 3)
    corners = np.array([rgb[0, 0], rgb[w - 1, 0], rgb[0, h - 1], rgb[w - 1, h - 1]])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))                 # (w, h)
    alpha = (np.clip((dist - tol) / edge, 0, 1) * 255).astype(np.uint8)
    fg = alpha > 40
    cols = fg.any(axis=1)
    frames = []
    for x0, x1 in _runs(cols, gap_min=max(6, w // 110), min_w=max(8, w // 90)):
        rows = fg[x0:x1].any(axis=0)
        ys = np.where(rows)[0]
        if len(ys) == 0:
            continue
        y0, y1 = int(ys[0]), int(ys[-1]) + 1
        sub = img.subsurface(pygame.Rect(x0, 0, x1 - x0, h)).copy()
        av = pygame.surfarray.pixels_alpha(sub)
        av[:] = alpha[x0:x1]
        del av
        frames.append(sub.subsurface(pygame.Rect(0, y0, x1 - x0, y1 - y0)).copy())
    return frames


class SpriteSet:
    """Conjunto de animações carregadas para um personagem."""

    def __init__(self, folder):
        self.anims = {}            # nome -> [Surface, ...] já escalados
        self.foot = {}             # nome -> [y do "chão" relativo ao frame]
        raw = {}
        for name in ANIMS:
            p = os.path.join(folder, name + '.png')
            if os.path.exists(p):
                fr = chroma_slice(p)
                if fr:
                    raw[name] = fr
        if not raw:
            return
        ref = raw.get('idle') or next(iter(raw.values()))
        ref_h = max((f.get_height() for f in ref), default=TARGET_H)
        scale = TARGET_H / ref_h if ref_h else 1.0
        for name, fr in raw.items():
            self.anims[name] = [self._scaled(f, scale) for f in fr]

    @staticmethod
    def _scaled(f, s):
        w, h = f.get_size()
        return pygame.transform.smoothscale(f, (max(1, int(w * s)), max(1, int(h * s))))

    def has(self, name):
        return name in self.anims

    def _index(self, f, name, mode):
        frames = self.anims[name]
        n = len(frames)
        if mode == 'attack' and f.attack is not None:
            a = f.attack
            total = max(1, a.startup + a.active + a.recovery)
            return min(n - 1, int(f.frame / total * n))
        if mode == 'jump':
            if f.vy < -2:
                return 0
            return min(n - 1, 1) if abs(f.vy) <= 2 else min(n - 1, 2)
        if mode == 'progress':
            return min(n - 1, int(f.frame / 30 * n))
        fps = ANIMS[name].get('fps', 8)
        return (f.anim // max(1, 60 // fps)) % n

    def draw(self, surf, f):
        name, mode = resolve(f)
        if name not in self.anims:
            return False
        img = self.anims[name][self._index(f, name, mode)]
        if f.facing < 0:
            img = pygame.transform.flip(img, True, False)
        rect = img.get_rect()
        rect.midbottom = (int(f.x), int(f.y) + 6)
        surf.blit(img, rect)
        return True


def load_all(characters):
    """Tenta carregar sprites de cada personagem; silenciosamente fica no
    procedural se não houver pasta/PNGs ou se faltar numpy."""
    for ch in characters:
        folder = os.path.join(ASSET_ROOT, getattr(ch, 'sprite_dir', '') or '')
        if not (ch.sprite_dir and os.path.isdir(folder)):
            continue
        try:
            ss = SpriteSet(folder)
        except Exception as e:                       # numpy ausente, PNG corrompido…
            print('[sprites] falha ao carregar %s: %s' % (ch.name, e))
            continue
        if ss.anims:
            ch.sprites = ss
            print('[sprites] %s: %s' % (ch.name, ', '.join(sorted(ss.anims))))


def render(surf, fighter):
    """Desenha o lutador via sprite quando disponível; senão, procedural."""
    ss = getattr(fighter.char, 'sprites', None)
    if ss is not None and ss.draw(surf, fighter):
        return
    fighter.char.draw(surf, fighter)
