"""Constantes globais: tela, física, paleta vintage e controles."""
import pygame

WIDTH, HEIGHT = 960, 540
FPS = 60
FLOOR_Y = 468
GRAVITY = 0.62
STAGE_MARGIN = 48
ROUND_TIME = 99          # segundos por round
WINS_TO_TAKE = 2         # melhor de 3

# ---- Paleta vintage (cartoon anos 1930) ----
PAPER     = (235, 222, 191)
CREAM     = (244, 233, 205)
INK       = (41, 31, 27)
SEPIA     = (196, 168, 124)
RED       = (172, 52, 40)
DARKRED   = (122, 36, 30)
GOLD      = (208, 158, 64)
GREEN_D   = (74, 84, 50)
GREEN_M   = (104, 116, 66)
GREEN_L   = (148, 148, 100)
BROWN     = (96, 64, 40)
SKIN_SACI = (88, 56, 38)
SKIN_CURU = (172, 98, 52)
FIRE_1    = (224, 138, 44)
FIRE_2    = (238, 186, 84)
SMOKE     = (210, 200, 178)
WHITE_W   = (246, 240, 220)

# ---- Controles ----
P1_KEYS = dict(left=pygame.K_a, right=pygame.K_d, up=pygame.K_w, down=pygame.K_s,
               punch=pygame.K_f, kick=pygame.K_g)
P2_KEYS = dict(left=pygame.K_LEFT, right=pygame.K_RIGHT, up=pygame.K_UP, down=pygame.K_DOWN,
               punch=pygame.K_k, kick=pygame.K_l)
