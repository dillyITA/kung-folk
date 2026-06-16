"""Valida o pipeline de sprites sem precisar de assets reais:
gera uma tira magenta sintética, confere que o chroma-key + fatiamento
acham o nº certo de frames, e que o fallback procedural continua de pé."""
import os
import sys
import tempfile

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402
from kungfolk import sprites  # noqa: E402
from kungfolk.characters import SACI  # noqa: E402
from kungfolk.engine import Fighter, IDLE  # noqa: E402

MAGENTA = (199, 44, 224)   # roxo-magenta, como o do model sheet gerado


def make_strip(path, n=6, cell=180, h=220):
    """Desenha n bonecos distintos sobre fundo magenta, espaçados."""
    gap = 36
    w = n * cell + (n + 1) * gap
    surf = pygame.Surface((w, h))
    surf.fill(MAGENTA)
    for i in range(n):
        cx = gap + i * (cell + gap) + cell // 2
        # "corpo": altura varia por frame, pés alinhados na base
        bh = 150 + (i % 3) * 20
        pygame.draw.ellipse(surf, (60, 40, 30),
                            (cx - 30, h - 20 - bh, 60, bh))
        pygame.draw.circle(surf, (172, 52, 40), (cx, h - 20 - bh), 26)  # "gorro"
    # uma sujeirinha solta (deve ser descartada por min_w)
    pygame.draw.circle(surf, (255, 240, 200), (gap // 2, 12), 2)
    pygame.image.save(surf, path)


def main():
    pygame.init()
    pygame.display.set_mode((4, 4))   # surfarray/convert precisam de display

    tmp = tempfile.mkdtemp()
    saci_dir = os.path.join(tmp, 'saci')
    os.makedirs(saci_dir)
    make_strip(os.path.join(saci_dir, 'idle.png'), n=6)
    make_strip(os.path.join(saci_dir, 'walk.png'), n=8)

    # aponta o ASSET_ROOT do pipeline para a pasta temporária
    sprites.ASSET_ROOT = tmp

    ss = sprites.SpriteSet(saci_dir)
    assert ss.has('idle'), 'idle não carregou'
    assert len(ss.anims['idle']) == 6, 'idle: esperava 6 frames, veio %d' % len(ss.anims['idle'])
    assert len(ss.anims['walk']) == 8, 'walk: esperava 8 frames, veio %d' % len(ss.anims['walk'])
    # escala: idle deve ficar na altura alvo
    th = max(f.get_height() for f in ss.anims['idle'])
    assert abs(th - sprites.TARGET_H) <= 2, 'escala fora do alvo: %d' % th
    print('fatiamento OK: idle=6, walk=8, altura=%d' % th)

    # draw() escolhe frame e desenha sem erro
    SACI.sprites = ss
    f = Fighter(SACI, 480, 1, None)
    canvas = pygame.Surface((960, 540))
    for _ in range(20):
        f.anim += 1
        assert sprites.render(canvas, f) is None
    # frame de idle deve estar entre 0 e n-1
    name, mode = sprites.resolve(f)
    assert name == 'idle' and mode == 'loop'
    print('render via sprite OK (estado %s)' % name)

    # fallback: personagem sem sprites volta ao procedural sem quebrar
    SACI.sprites = None
    sprites.render(canvas, f)
    print('fallback procedural OK')

    pygame.quit()
    print('PIPELINE DE SPRITES OK')


if __name__ == '__main__':
    main()
