"""Valida o pipeline de sprites sem assets reais, no fluxo atual:
strips transparentes + sprites.json (fronteiras exatas) -> slice_by_bounds +
escala por núcleo. Também testa o fallback chroma_slice e o fallback procedural."""
import json
import os
import sys
import tempfile

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402
from kungfolk import sprites  # noqa: E402
from kungfolk.characters import SACI  # noqa: E402
from kungfolk.engine import Fighter  # noqa: E402

GAP = 20


def make_strip(path, n=6, cell=120, h=220):
    """Strip TRANSPARENTE com n bonecos espaçados; devolve as fronteiras [x,w]."""
    w = n * cell + (n + 1) * GAP
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    bounds = []
    for i in range(n):
        x = GAP + i * (cell + GAP)
        cx = x + cell // 2
        bh = 150 + (i % 3) * 18
        pygame.draw.ellipse(surf, (60, 40, 30, 255), (cx - 28, h - 16 - bh, 56, bh))
        pygame.draw.circle(surf, (172, 52, 40, 255), (cx, h - 16 - bh), 24)
        bounds.append([x, cell])
    pygame.image.save(surf, path)
    return bounds


def main():
    pygame.init()
    pygame.display.set_mode((4, 4))
    tmp = tempfile.mkdtemp()
    saci_dir = os.path.join(tmp, 'saci')
    os.makedirs(saci_dir)
    b_idle = make_strip(os.path.join(saci_dir, 'idle.png'), n=6)
    make_strip(os.path.join(saci_dir, 'walk.png'), n=8)   # sem bounds -> chroma_slice
    # só idle tem fronteiras gravadas; walk cai no fallback chroma_slice
    json.dump({'idle': b_idle}, open(os.path.join(saci_dir, 'sprites.json'), 'w'))

    sprites.ASSET_ROOT = tmp
    ss = sprites.SpriteSet(saci_dir)
    assert ss.has('idle') and len(ss.anims['idle']) == 6, 'idle: %s' % (
        len(ss.anims.get('idle', [])))
    assert ss.has('walk') and len(ss.anims['walk']) == 8, 'walk: %s' % (
        len(ss.anims.get('walk', [])))
    # escala por núcleo: a MEDIANA dos frames de idle ~ CORE_BODY
    cores = sorted(sprites._core_height(f) for f in ss.anims['idle'])
    core = cores[len(cores) // 2]
    assert abs(core - sprites.CORE_BODY) <= 6, 'núcleo idle fora do alvo: %d' % core
    print('slice_by_bounds + chroma_slice OK | idle=6 walk=8 núcleo=%d' % core)

    SACI.sprites = ss
    f = Fighter(SACI, 480, 1, None)
    canvas = pygame.Surface((960, 540))
    for _ in range(20):
        f.anim += 1
        assert sprites.render(canvas, f) is None
    print('render via sprite OK (estado %s)' % sprites.resolve(f)[0])

    SACI.sprites = None
    sprites.render(canvas, f)
    print('fallback procedural OK')
    pygame.quit()
    print('PIPELINE DE SPRITES OK')


if __name__ == '__main__':
    main()
