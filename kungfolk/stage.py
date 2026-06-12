"""Cenário: clareira na mata em 'aquarela' — manchas translúcidas sobrepostas,
sem contorno de tinta (só os personagens têm tinta, como no Cuphead)."""
import math
import random
import pygame
from . import config as C


class ForestStage:
    name = 'CLAREIRA DA MATA'

    def __init__(self, seed=7):
        self.rng = random.Random(seed)
        self.base = self._build()
        self.motes = [(self.rng.uniform(0, C.WIDTH), self.rng.uniform(80, 420),
                       self.rng.uniform(0.2, 0.7), self.rng.uniform(0, 6.3))
                      for _ in range(12)]

    def _smudge(self, layer, cx, cy, rx, ry, color, alpha=30, n=5):
        """Mancha aquarela: elipses translúcidas levemente deslocadas."""
        rng = self.rng
        for _ in range(n):
            w = int(rx * 2 * rng.uniform(0.78, 1.15))
            h = int(ry * 2 * rng.uniform(0.78, 1.15))
            r = pygame.Rect(0, 0, max(4, w), max(4, h))
            r.center = (int(cx + rng.uniform(-rx, rx) * 0.14),
                        int(cy + rng.uniform(-ry, ry) * 0.14))
            pygame.draw.ellipse(layer, (color[0], color[1], color[2], alpha), r)

    def _build(self):
        rng = self.rng
        s = pygame.Surface((C.WIDTH, C.HEIGHT))
        # céu: lavagem em degradê creme → pêssego
        for y in range(C.HEIGHT):
            k = y / C.HEIGHT
            col = (int(242 - 30 * k), int(232 - 44 * k), int(206 - 58 * k))
            pygame.draw.line(s, col, (0, y), (C.WIDTH, y))
        wash = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        # sol aguado
        self._smudge(wash, 195, 125, 95, 92, (238, 212, 152), 22, 4)
        self._smudge(wash, 195, 125, 56, 54, (248, 230, 170), 36, 3)
        # morros distantes (verde acinzentado, perspectiva atmosférica)
        for cx, cy, rx, ry in ((150, 505, 360, 150), (540, 515, 430, 175),
                               (880, 505, 340, 145)):
            self._smudge(wash, cx, cy, rx, ry, (164, 168, 122), 34, 6)
        # massas de mata atrás dos troncos
        for cx in range(-40, C.WIDTH + 80, 140):
            self._smudge(wash, cx, C.FLOOR_Y - 16 + rng.randint(-12, 12),
                         120, 80 + rng.randint(0, 30), (110, 122, 76), 42, 6)
        # troncos suaves, pintados (sem contorno)
        trunks = []
        for i in range(6):
            x = 60 + i * 172 + rng.randint(-26, 26)
            w = rng.randint(26, 42)
            sway = rng.randint(-16, 18)
            trunks.append((x, w, sway))
            pts = [(x - w // 2, C.FLOOR_Y + 8), (x + w // 2, C.FLOOR_Y + 8),
                   (x + w // 3 + sway, 64), (x - w // 3 + sway, 56)]
            pygame.draw.polygon(wash, (108, 80, 54, 170), pts)
            pygame.draw.polygon(wash, (84, 62, 44, 90),
                                [(p[0] + w // 4, p[1]) for p in pts])
        # tufos de folhagem agarrados aos troncos (na altura da copa)
        for x, w, sway in trunks:
            for side in (-1, 1):
                bx = x + sway // 2 + side * (w // 2 + rng.randint(10, 34))
                by = rng.randint(70, 150)
                self._smudge(wash, bx, by, 52, 30, (96, 110, 66), 44, 4)
                self._smudge(wash, bx + side * 14, by + 16, 34, 20,
                             (118, 130, 78), 34, 3)
        # copa no topo: faixa densa de folhagem
        for x in range(-30, C.WIDTH + 60, 70):
            self._smudge(wash, x, 8 + rng.randint(-8, 8), 92, 66, (78, 92, 52), 54, 6)
            self._smudge(wash, x + 30, 46, 60, 40, (100, 114, 66), 40, 4)
        # feixes de luz descendo
        for lx in (330, 620):
            beam = [(lx - 26, 0), (lx + 30, 0), (lx + 120, C.FLOOR_Y),
                    (lx + 30, C.FLOOR_Y)]
            pygame.draw.polygon(wash, (250, 238, 190, 22), beam)
        s.blit(wash, (0, 0))
        # chão pintado
        pygame.draw.rect(s, (99, 107, 64), (0, C.FLOOR_Y + 8, C.WIDTH, C.HEIGHT))
        gw = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        for _ in range(26):
            gx = rng.randint(0, C.WIDTH)
            gy = rng.randint(C.FLOOR_Y + 12, C.HEIGHT)
            col = rng.choice(((70, 78, 48), (126, 132, 84), (88, 96, 58)))
            self._smudge(gw, gx, gy, rng.randint(30, 90), rng.randint(6, 14),
                         col, 30, 3)
        s.blit(gw, (0, 0))
        # linha do chão suave (referência de palco)
        pygame.draw.line(s, (62, 68, 42), (0, C.FLOOR_Y + 8), (C.WIDTH, C.FLOOR_Y + 8), 3)
        # tufos de capim soltos
        for _ in range(40):
            x = rng.randint(0, C.WIDTH)
            y = rng.randint(C.FLOOR_Y + 16, C.HEIGHT - 6)
            for d in (-4, 0, 4):
                pygame.draw.line(s, (130, 136, 88), (x, y),
                                 (x + d, y - rng.randint(6, 13)), 2)
        return s

    def draw(self, surf, t):
        surf.blit(self.base, (0, 0))
        # cipós balançando (pintados, sem tinta)
        for i, x0 in enumerate((250, 700)):
            sway = math.sin(t * 0.02 + i * 2.4) * 16
            pts = [(x0 + sway * (y / 180.0) ** 2, 70 + y) for y in range(0, 181, 30)]
            pygame.draw.lines(surf, (78, 90, 54), False,
                              [(int(a), int(b)) for a, b in pts], 6)
            end = pts[-1]
            pygame.draw.circle(surf, (104, 118, 68), (int(end[0]), int(end[1]) + 8), 10)
        # vagalumes / poeira dourada
        for i, (x, y, sp, ph) in enumerate(self.motes):
            mx = (x + t * sp) % (C.WIDTH + 40) - 20
            my = y + math.sin(t * 0.03 + ph) * 14
            pygame.draw.circle(surf, C.GOLD, (int(mx), int(my)), 2)
