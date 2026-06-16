"""Cenário: clareira na mata, estilo cartoon vintage de ALTO CONTRASTE —
troncos e copa escuros e opacos com contorno de tinta, pra ler bem na tela
(a versão aquarela pálida anterior sumia contra a vinheta)."""
import math
import random
import pygame
from . import config as C

# paleta dedicada do cenário (mais saturada/escura que a base)
SKY_TOP = (228, 206, 158)
SKY_BOT = (198, 170, 120)
HILL_FAR = (150, 152, 104)
HILL_NEAR = (118, 130, 78)
MATA = (66, 80, 44)          # massa de mata atrás dos troncos
TRUNK = (104, 70, 42)
TRUNK_SH = (78, 50, 30)      # lado sombreado do tronco
CANOPY = (58, 74, 42)
CANOPY_HI = (84, 100, 58)
GROUND = (92, 108, 60)
GROUND_DK = (70, 84, 46)
GRASS = (132, 142, 88)
BEAM = (250, 240, 200)


class ForestStage:
    name = 'CLAREIRA DA MATA'

    def __init__(self, seed=7):
        self.rng = random.Random(seed)
        self.base = self._build()
        self.motes = [(self.rng.uniform(0, C.WIDTH), self.rng.uniform(80, 420),
                       self.rng.uniform(0.2, 0.7), self.rng.uniform(0, 6.3))
                      for _ in range(12)]

    def _ink_poly(self, s, pts, color, w=3):
        pts = [(int(x), int(y)) for x, y in pts]
        pygame.draw.polygon(s, color, pts)
        pygame.draw.polygon(s, C.INK, pts, w)

    def _ink_circle(self, s, c, r, color, w=3):
        pygame.draw.circle(s, color, (int(c[0]), int(c[1])), int(r))
        pygame.draw.circle(s, C.INK, (int(c[0]), int(c[1])), int(r), w)

    def _build(self):
        rng = self.rng
        s = pygame.Surface((C.WIDTH, C.HEIGHT))
        # céu em degradê quente
        for y in range(C.HEIGHT):
            k = y / C.HEIGHT
            col = tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * k) for i in range(3))
            pygame.draw.line(s, col, (0, y), (C.WIDTH, y))
        # sol pálido
        self._ink_circle(s, (190, 120), 52, (236, 214, 158), 0)
        # morros distantes (opacos, contorno suave)
        for cx, cy, rx, ry, col in ((150, 500, 360, 150, HILL_FAR),
                                    (560, 520, 440, 180, HILL_NEAR),
                                    (900, 500, 340, 150, HILL_FAR)):
            r = pygame.Rect(cx - rx, cy - ry, rx * 2, ry * 2)
            pygame.draw.ellipse(s, col, r)
        # massa escura de mata na faixa dos troncos
        pygame.draw.rect(s, MATA, (0, 70, C.WIDTH, C.FLOOR_Y - 70 + 8))
        # feixes de luz (camada translúcida)
        beams = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        for lx in (330, 660):
            pygame.draw.polygon(beams, (BEAM[0], BEAM[1], BEAM[2], 46),
                                [(lx - 30, 70), (lx + 34, 70),
                                 (lx + 130, C.FLOOR_Y), (lx + 26, C.FLOOR_Y)])
        s.blit(beams, (0, 0))
        # troncos escuros e opacos, com contorno de tinta
        for i in range(5):
            x = 110 + i * 200 + rng.randint(-30, 30)
            w = rng.randint(40, 58)
            sway = rng.randint(-14, 16)
            self._ink_poly(s, [(x - w // 2, C.FLOOR_Y + 8), (x + w // 2, C.FLOOR_Y + 8),
                               (x + w // 3 + sway, 96), (x - w // 3 + sway, 84)], TRUNK)
            # lado sombreado
            pygame.draw.polygon(s, TRUNK_SH,
                                [(x + w // 6, C.FLOOR_Y + 8), (x + w // 2, C.FLOOR_Y + 8),
                                 (x + w // 3 + sway, 96), (x + sway, 90)])
            # cascas
            for _ in range(3):
                yy = rng.randint(160, 420)
                pygame.draw.arc(s, C.INK, pygame.Rect(x - w // 2, yy, w, 22), 3.4, 6.0, 2)
        # copa densa no topo: festão de círculos escuros com contorno
        for x in range(-30, C.WIDTH + 60, 84):
            r = 66 + rng.randint(-10, 12)
            self._ink_circle(s, (x, 26), r, CANOPY)
            self._ink_circle(s, (x + 30, 20), int(r * 0.6), CANOPY_HI, 0)
        # arbustos na base dos troncos
        for x in range(-10, C.WIDTH + 40, 130):
            r = 34 + rng.randint(-6, 12)
            self._ink_circle(s, (x + rng.randint(-12, 12), C.FLOOR_Y + 6), r, HILL_NEAR)
        # chão
        pygame.draw.rect(s, GROUND, (0, C.FLOOR_Y + 8, C.WIDTH, C.HEIGHT))
        pygame.draw.rect(s, GROUND_DK, (0, C.HEIGHT - 60, C.WIDTH, 60))
        pygame.draw.line(s, C.INK, (0, C.FLOOR_Y + 8), (C.WIDTH, C.FLOOR_Y + 8), 4)
        for _ in range(48):
            x = rng.randint(0, C.WIDTH)
            y = rng.randint(C.FLOOR_Y + 16, C.HEIGHT - 8)
            for d in (-5, 0, 5):
                pygame.draw.line(s, GRASS, (x, y), (x + d, y - rng.randint(8, 16)), 2)
        return s

    def draw(self, surf, t):
        surf.blit(self.base, (0, 0))
        # cipós balançando
        for i, x0 in enumerate((250, 700)):
            sway = math.sin(t * 0.02 + i * 2.4) * 16
            pts = [(x0 + sway * (y / 180.0) ** 2, 60 + y) for y in range(0, 181, 30)]
            pygame.draw.lines(surf, CANOPY, False,
                              [(int(a), int(b)) for a, b in pts], 6)
            end = pts[-1]
            self._ink_circle(surf, (end[0], end[1] + 8), 11, CANOPY_HI)
        # vagalumes / poeira dourada
        for (x, y, sp, ph) in self.motes:
            mx = (x + t * sp) % (C.WIDTH + 40) - 20
            my = y + math.sin(t * 0.03 + ph) * 14
            pygame.draw.circle(surf, C.GOLD, (int(mx), int(my)), 2)
