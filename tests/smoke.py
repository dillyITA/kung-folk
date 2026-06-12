"""Teste de fumaça: roda CPU vs CPU sem janela e confere que nada explode."""
import os
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402
from kungfolk.game import Game  # noqa: E402
from kungfolk.scenes import FightScene, ResultScene  # noqa: E402
from kungfolk.characters import SACI, CURUPIRA  # noqa: E402
from kungfolk.ai import CPUController  # noqa: E402


def main():
    g = Game()
    g.switch(FightScene(g, SACI, CURUPIRA,
                        CPUController(level=0.7, seed=1),
                        CPUController(level=0.7, seed=2),
                        names=('CPU 1', 'CPU 2')))
    total_hits = 0
    last_hp = (SACI.hp, CURUPIRA.hp)
    for i in range(3600):  # ~60s de jogo
        g.step([])
        sc = g.scene
        if isinstance(sc, FightScene):
            hp = (sc.p1.hp, sc.p2.hp)
            if hp != last_hp:
                total_hits += 1
                last_hp = hp
    sc = g.scene
    print('cena final:', type(sc).__name__)
    if isinstance(sc, FightScene):
        print('hp: %s x %s | rounds: %s | round %d | fase %s'
              % (sc.p1.hp, sc.p2.hp, sc.wins, sc.round_no, sc.phase))
    assert total_hits > 0, 'nenhum golpe conectou em 60s — IA ou hitboxes quebradas'
    print('golpes registrados:', total_hits)
    print('OK — 3600 frames sem erro')
    pygame.quit()


if __name__ == '__main__':
    main()
