"""Personagens: frame data dos golpes e desenho procedural estilo rubber hose
(anos 1930): membros-mangueira, luvas brancas, pés grandes, olhos pie-cut,
smear frames, squash & stretch e tremor de linha desenhada à mão."""
import math
from dataclasses import dataclass
import pygame
from . import config as C
from .engine import (Attack, IDLE, WALK, JUMP, CROUCH, ATTACK, SPECIAL,
                     HITSTUN, BLOCKSTUN, KNOCKDOWN, KO, WIN)

OUT = 3  # espessura do contorno de tinta


# ---------------- primitivas com contorno grosso ----------------
def _pt(p):
    return (int(round(p[0])), int(round(p[1])))


def _mix(c1, c2, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))


def _jit(f, idx, amp=1.4):
    """'Boiling line': tremor determinístico a ~15fps, como redesenho à mão."""
    s = (f.anim // 4) * 7.13 + idx * 12.9898
    return (math.sin(s * 3.1) * amp, math.cos(s * 2.3) * amp)


def blob(surf, c, rx, ry, color):
    r = pygame.Rect(0, 0, int(rx * 2), int(ry * 2))
    r.center = _pt(c)
    pygame.draw.ellipse(surf, C.INK, r.inflate(OUT * 2, OUT * 2))
    pygame.draw.ellipse(surf, color, r)


def poly(surf, pts, color, ink=True):
    pts = [_pt(p) for p in pts]
    pygame.draw.polygon(surf, color, pts)
    if ink:
        pygame.draw.polygon(surf, C.INK, pts, OUT)


def _bez(a, c, b, n=12):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u * u * a[0] + 2 * u * t * c[0] + t * t * b[0],
                    u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]))
    return pts


def hose(surf, a, b, sag, w, color, jitter=(0, 0)):
    """Membro-mangueira: tubo curvo de espessura constante, sem cotovelo."""
    mx = (a[0] + b[0]) / 2 + jitter[0]
    my = (a[1] + b[1]) / 2 + jitter[1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = max(1.0, math.hypot(dx, dy))
    ctrl = (mx - dy / ln * sag, my + dx / ln * sag)
    pts = _bez(a, ctrl, b)
    r = max(2, w // 2)
    for p in pts:
        pygame.draw.circle(surf, C.INK, _pt(p), r + OUT)
    for p in pts:
        pygame.draw.circle(surf, color, _pt(p), r)


def glove(surf, pos, size=11, ang=0.0):
    """Luva branca de desenho antigo: mitene redonda + três dedos."""
    parts = [(pos, size)]
    for i in (-1, 0, 1):
        a = ang + i * 0.62
        parts.append(((pos[0] + math.cos(a) * size * 0.8,
                       pos[1] + math.sin(a) * size * 0.8), size * 0.45))
    for p, r in parts:
        pygame.draw.circle(surf, C.INK, _pt(p), int(r) + OUT)
    for p, r in parts:
        pygame.draw.circle(surf, C.WHITE_W, _pt(p), int(r))


def bigfoot(surf, pos, facing, color, size=1.0, back=False):
    """Pé enorme de cartoon; back=True desenha virado pra trás (Curupira)."""
    d = -facing if back else facing
    w, h = 27 * size, 13 * size
    r = pygame.Rect(0, 0, int(w), int(h))
    r.midbottom = (int(pos[0] + d * w * 0.30), int(pos[1]) + 3)
    pygame.draw.ellipse(surf, C.INK, r.inflate(OUT * 2, OUT * 2))
    pygame.draw.ellipse(surf, color, r)
    blob(surf, (r.centerx + d * w * 0.40, r.centery + h * 0.05),
         4.5 * size, 4 * size, color)


def smear_fan(surf, pivot, tip, color, spread=0.85):
    """Leque-fantasma de movimento (smear frame) atrás de um golpe."""
    ang = math.atan2(tip[1] - pivot[1], tip[0] - pivot[0])
    ln = math.hypot(tip[0] - pivot[0], tip[1] - pivot[1])
    if ln < 8:
        return
    pts = [pivot]
    for i in range(4):
        a = ang - spread + spread * i / 3
        pts.append((pivot[0] + math.cos(a) * ln, pivot[1] + math.sin(a) * ln))
    pygame.draw.polygon(surf, color, [_pt(p) for p in pts])


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a, b, p):
    return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)


# ---------------- pose paramétrica (coords locais, +x = frente) ----------------
def pose(f):
    ph = f.anim * 0.22
    P = dict(hip=(0, 56), neck=(2, 106), head=(3, 130),
             hand_f=(28, 86), hand_b=(-18, 82),
             foot_f=(14, 4), foot_b=(-14, 4),
             lift=math.sin(f.anim * 0.09) * 2.2, brow=0)
    s = f.state

    if s == WALK:
        sw = math.sin(ph)
        P['foot_f'] = (15 + 12 * sw, 4 + max(0.0, 10 * sw))
        P['foot_b'] = (-15 - 12 * sw, 4 + max(0.0, -10 * sw))
        P['hand_f'] = (28 - 10 * sw, 86)
        P['hand_b'] = (-18 + 10 * sw, 82)
        P['lift'] = abs(math.sin(ph)) * 3.5
    elif s == CROUCH:
        P.update(hip=(0, 32), neck=(3, 66), head=(5, 88),
                 hand_f=(24, 54), hand_b=(-12, 50),
                 foot_f=(18, 3), foot_b=(-18, 3), lift=0)
    elif s == JUMP:
        P.update(hip=(0, 60), neck=(4, 108), head=(6, 132),
                 hand_f=(28, 104), hand_b=(-22, 98),
                 foot_f=(12, 32), foot_b=(-10, 24), lift=0)
    elif s in (HITSTUN, BLOCKSTUN):
        j = math.sin(f.anim * 0.9) * 3
        if f.state == BLOCKSTUN:
            P.update(neck=(-2, 102), head=(-4, 124),
                     hand_f=(20, 96), hand_b=(16, 74), brow=1)
        else:
            P.update(hip=(2, 54), neck=(-10, 102), head=(-20, 122),
                     hand_f=(-26 + j, 106), hand_b=(30 - j, 98),
                     foot_f=(22, 4), foot_b=(-8, 4), brow=2)
    elif s in (KNOCKDOWN, KO):
        if f.on_floor() and f.vy >= 0:
            P.update(hip=(-6, 16), neck=(-38, 20), head=(-56, 24),
                     hand_f=(-22, 32), hand_b=(-48, 30),
                     foot_f=(28, 8), foot_b=(36, 6), lift=0, brow=2)
        else:
            P.update(hip=(0, 64), neck=(-14, 104), head=(-28, 118),
                     hand_f=(-32, 116), hand_b=(26, 108),
                     foot_f=(26, 42), foot_b=(10, 30), lift=0, brow=2)
    elif s == WIN:
        hop = abs(math.sin(f.anim * 0.18)) * 9
        P.update(hand_f=(22, 144), hand_b=(-22, 142), lift=hop)
    elif s in (ATTACK, SPECIAL) and f.attack:
        a = f.attack
        t = f.frame
        if t < a.startup:
            p = -ease(t / max(1, a.startup)) * 0.35  # antecipação: puxa pra trás
        elif t < a.startup + a.active:
            p = 1.0
        else:
            p = 1 - ease((t - a.startup - a.active) / max(1, a.recovery))
        P['brow'] = 2
        tag = a.anim
        if tag == 'punch':
            P['hand_f'] = lerp((-8, 84), (66, 94), max(0.0, p))
            if p < 0:
                P['hand_f'] = (-8 + 18 * p, 84)
            P['hand_b'] = (-24, 80)
            P['neck'] = (2 + 8 * max(0, p), 106)
            P['head'] = (3 + 13 * max(0, p), 128)
        elif tag == 'cpunch':
            P.update(hip=(0, 32), neck=(6 * max(0, p) + 3, 66),
                     head=(10 * max(0, p) + 5, 88),
                     foot_f=(18, 3), foot_b=(-18, 3), lift=0,
                     hand_b=(-14, 48))
            P['hand_f'] = lerp((0, 42), (62, 40), max(0.0, p))
        elif tag == 'kick':
            P['foot_f'] = lerp((13, 6), (68, 60), max(0.0, p))
            P['foot_b'] = (-11, 3)
            P['hand_f'] = (32, 100)
            P['hand_b'] = (-30, 92)
            P['neck'] = (2 - 9 * max(0, p), 104)
            P['head'] = (3 - 14 * max(0, p), 126)
        elif tag == 'air':
            P.update(hip=(0, 60), neck=(6, 108), head=(9, 130),
                     hand_f=(30, 106), hand_b=(-24, 100), lift=0)
            P['foot_f'] = lerp((15, 32), (58, 24), max(0.0, p))
            P['foot_b'] = (-11, 36)
        elif tag == 'cast':
            P['hand_f'] = lerp((0, 88), (60, 92), max(0.0, p))
            P['hand_b'] = lerp((-18, 82), (54, 76), max(0.0, p))
            P['neck'] = (2 + 7 * max(0, p), 106)
            P['head'] = (3 + 10 * max(0, p), 129)
        elif tag == 'whirl_cast':
            ang = f.anim * 0.55
            P['hand_f'] = (2 + math.cos(ang) * 32, 92 + math.sin(ang) * 20)
            P['hand_b'] = (2 - math.cos(ang) * 32, 92 - math.sin(ang) * 20)
            P['lift'] = abs(math.sin(f.anim * 0.3)) * 5
        elif tag == 'lunge':
            run = math.sin(f.anim * 0.6) * 11
            P.update(hip=(4, 52), neck=(26 * max(0, p) + 2, 96),
                     head=(44 * max(0, p) + 4, 98),
                     hand_f=(-18, 68), hand_b=(-30, 58),
                     foot_f=(15 + run, 6), foot_b=(-15 - run, 6), lift=2)

    # squash & stretch
    if f.squash > 0 and f.on_floor() and s not in (KNOCKDOWN, KO):
        sq = f.squash / 7.0
        for k in ('hip', 'neck', 'head', 'hand_f', 'hand_b'):
            x, y = P[k]
            P[k] = (x * (1 + 0.10 * sq), y * (1 - 0.16 * sq))
    elif s == JUMP and f.vy < -2:
        for k in ('hip', 'neck', 'head', 'hand_f', 'hand_b'):
            x, y = P[k]
            P[k] = (x * 0.93, y * 1.07)
    return P


def world(f, P):
    def w(key):
        p = P[key]
        return (f.x + p[0] * f.facing, f.y - p[1] - P['lift'])
    return w


def _smear_now(f):
    a = f.attack
    return (a is not None and f.state in (ATTACK, SPECIAL)
            and a.anim in ('punch', 'kick', 'cpunch', 'air')
            and a.startup <= f.frame < a.startup + min(a.active, 3))


# ---------------- rosto cartoon (olhos pie-cut) ----------------
def cartoon_face(surf, f, head, fc, r=22):
    k = r / 22.0
    for ox, oy in ((10 * k, -5 * k), (-4 * k, -6 * k)):
        e = (head[0] + ox * fc, head[1] + oy)
        if f.state == KO:
            for d in ((-4, -4, 4, 4), (-4, 4, 4, -4)):
                pygame.draw.line(surf, C.INK,
                                 (e[0] + d[0] * k, e[1] + d[1] * k),
                                 (e[0] + d[2] * k, e[1] + d[3] * k), max(2, int(3 * k)))
            continue
        # olho com contorno fino (pra leitura não morrer na tinta grossa)
        er = pygame.Rect(0, 0, int(15 * k), int(19 * k))
        er.center = _pt(e)
        pygame.draw.ellipse(surf, C.WHITE_W, er)
        pygame.draw.ellipse(surf, C.INK, er, 2)
        p = (e[0] + 2.4 * k * fc, e[1] + 2.8 * k)
        pygame.draw.circle(surf, C.INK, _pt(p), int(4.6 * k))
        # recorte "pie-cut" na pupila
        notch = [(p[0], p[1]), (p[0] + 5 * k * fc, p[1] - 5 * k),
                 (p[0] + 1.4 * k * fc, p[1] - 6 * k)]
        pygame.draw.polygon(surf, C.WHITE_W, [_pt(q) for q in notch])
    # sobrancelha
    if f.state in (ATTACK, SPECIAL, HITSTUN, KNOCKDOWN):
        pygame.draw.line(surf, C.INK,
                         (head[0] - 8 * k * fc, head[1] - 14 * k),
                         (head[0] + 13 * k * fc, head[1] - 9 * k), max(3, int(4 * k)))
    # boca
    m = (head[0] + 10 * k * fc, head[1] + 9 * k)
    if f.state in (HITSTUN, KNOCKDOWN, KO):
        blob(surf, m, 4.5 * k, 5.5 * k, C.DARKRED)
    elif f.state in (ATTACK, SPECIAL):
        # dentes cerrados
        rct = pygame.Rect(0, 0, int(14 * k), int(7 * k))
        rct.center = _pt(m)
        pygame.draw.rect(surf, C.INK, rct.inflate(OUT * 2, OUT * 2))
        pygame.draw.rect(surf, C.WHITE_W, rct)
        pygame.draw.line(surf, C.INK, (rct.centerx, rct.top), (rct.centerx, rct.bottom), 1)
    else:
        pygame.draw.arc(surf, C.INK,
                        pygame.Rect(int(m[0] - 7 * k), int(m[1] - 6 * k),
                                    int(14 * k), int(11 * k)),
                        math.pi * 1.15, math.pi * 1.95, max(2, int(3 * k)))


# ---------------- SACI-PERERÊ ----------------
def _tornado(surf, x, y, t, scale=1.0):
    for i in range(6):
        yy = y - 12 - i * 18 * scale
        w = (50 - i * 6 + math.sin(t * 0.6 + i) * 7) * scale
        col = C.CREAM if i % 2 == 0 else C.SEPIA
        blob(surf, (x + math.sin(t * 0.5 + i * 1.3) * 7, yy),
             max(8, w / 2), 8.5 * scale, col)
    for k in range(3):
        a = t * 0.4 + k * 2.1
        blob(surf, (x + math.cos(a) * 36 * scale, y - 52 * scale + math.sin(a) * 32),
             4, 3, C.GREEN_M)


def draw_saci(surf, f):
    a = f.attack
    if f.state == SPECIAL and a is not None and a.teleport and f.frame >= 3:
        _tornado(surf, f.x, f.y, f.anim)
        return
    P = pose(f)
    W = world(f, P)
    hip, neck, head = W('hip'), W('neck'), W('head')
    hand_f, hand_b = W('hand_f'), W('hand_b')
    foot = W('foot_f')
    fc = f.facing
    j1, j2, j3 = _jit(f, 1), _jit(f, 2), _jit(f, 3)
    sh_b = (neck[0] - 7 * fc, neck[1] + 7)
    sh_f = (neck[0] + 7 * fc, neck[1] + 7)
    ang_b = math.atan2(hand_b[1] - sh_b[1], hand_b[0] - sh_b[0])
    ang_f = math.atan2(hand_f[1] - sh_f[1], hand_f[0] - sh_f[0])

    # braço de trás
    hose(surf, sh_b, hand_b, 10 * fc, 9, C.SKIN_SACI, j1)
    glove(surf, hand_b, 9, ang_b)
    # perna única + pezão
    if _smear_now(f) and a.anim in ('kick', 'air'):
        smear_fan(surf, hip, foot, _mix(C.SKIN_SACI, C.PAPER, 0.55))
    hose(surf, (hip[0], hip[1] - 4), foot, -9 * fc, 13, C.SKIN_SACI, j2)
    bigfoot(surf, foot, fc, C.SKIN_SACI, 1.15)
    # corpo feijão
    mid = ((hip[0] + neck[0]) / 2 + j3[0] * 0.4, (hip[1] + neck[1]) / 2 + 6)
    blob(surf, mid, 18, 22, C.SKIN_SACI)
    # shorts vermelhos com remendo
    blob(surf, (hip[0], hip[1] - 2), 17, 14, C.RED)
    pygame.draw.circle(surf, C.GOLD, _pt((hip[0] + 6 * fc, hip[1] - 2)), 4)
    pygame.draw.circle(surf, C.INK, _pt((hip[0] + 6 * fc, hip[1] - 2)), 4, 1)
    # cabeça grande
    blob(surf, (head[0] + j3[0], head[1] + j3[1]), 22, 21, C.SKIN_SACI)
    blob(surf, (head[0] - 17 * fc, head[1] + 3), 5, 6, C.SKIN_SACI)  # orelha
    cartoon_face(surf, f, (head[0] + j3[0], head[1] + j3[1]), fc)
    # gorro vermelho flopado
    sway = math.sin(f.anim * 0.12) * 6
    base_f = (head[0] + 20 * fc, head[1] - 10)
    base_b = (head[0] - 19 * fc, head[1] - 12)
    tip = (head[0] - 36 * fc, head[1] - 26 + sway)
    poly(surf, [base_f, (head[0] + 3 * fc, head[1] - 40), tip, base_b], C.RED)
    hose(surf, base_b, base_f, -3 * fc, 8, C.DARKRED)
    blob(surf, tip, 6, 6, C.GOLD)
    # cachimbo
    if f.state not in (KO, KNOCKDOWN):
        mouth = (head[0] + 16 * fc, head[1] + 10)
        tipo = (mouth[0] + 13 * fc, mouth[1] + 10)
        hose(surf, mouth, tipo, 2 * fc, 5, C.BROWN)
        blob(surf, tipo, 6, 6, C.BROWN)
        k = (f.anim % 50) / 50.0
        if k < 0.6:
            for j in range(2):
                kk = k + j * 0.18
                pygame.draw.circle(surf, C.SMOKE,
                                   _pt((tipo[0] + 4 * fc + math.sin(kk * 9) * 5,
                                        tipo[1] - 14 - kk * 34)),
                                   max(2, int(6 - kk * 6)))
    # braço da frente (por cima), com smear no soco
    if _smear_now(f) and a.anim in ('punch', 'cpunch'):
        smear_fan(surf, sh_f, hand_f, _mix(C.SKIN_SACI, C.PAPER, 0.55))
    hose(surf, sh_f, hand_f, -10 * fc, 10, C.SKIN_SACI, j1)
    glove(surf, hand_f, 10, ang_f)


def saci_portrait(surf, cx, cy, s=1.0):
    head = (cx, cy + 6 * s)
    blob(surf, head, 27 * s, 26 * s, C.SKIN_SACI)
    blob(surf, (cx - 21 * s, cy + 9 * s), 6 * s, 7 * s, C.SKIN_SACI)
    # olhos pie-cut
    for ox in (12 * s, -3 * s):
        e = (cx + ox, cy + 1 * s)
        blob(surf, e, 7.5 * s, 9 * s, C.WHITE_W)
        p = (e[0] + 2.5 * s, e[1] + 2.5 * s)
        pygame.draw.circle(surf, C.INK, _pt(p), int(5 * s))
        pygame.draw.polygon(surf, C.WHITE_W,
                            [_pt(p), _pt((p[0] + 5 * s, p[1] - 5 * s)),
                             _pt((p[0] + 1.5 * s, p[1] - 6 * s))])
    pygame.draw.arc(surf, C.INK,
                    pygame.Rect(int(cx + 4 * s), int(cy + 14 * s),
                                int(16 * s), int(12 * s)),
                    math.pi * 1.1, math.pi * 1.9, max(2, int(3 * s)))
    poly(surf, [(cx + 24 * s, cy - 10 * s), (cx + 3 * s, cy - 44 * s),
                (cx - 44 * s, cy - 28 * s), (cx - 23 * s, cy - 12 * s)], C.RED)
    blob(surf, (cx - 44 * s, cy - 28 * s), 7 * s, 7 * s, C.GOLD)
    mouth = (cx + 21 * s, cy + 20 * s)
    hose(surf, mouth, (mouth[0] + 15 * s, mouth[1] + 11 * s), 3 * s,
         max(3, int(5 * s)), C.BROWN)
    blob(surf, (mouth[0] + 17 * s, mouth[1] + 12 * s), 7 * s, 7 * s, C.BROWN)


def saci_moves():
    return {
        'punch': Attack('Cachimbada', 4, 3, 8, 6, hitstun=13, push=4.5,
                        hitbox=(30, 80, 54, 30), anim='punch'),
        'crouch_punch': Attack('Tapa Rasteiro', 4, 3, 9, 5, hitstun=12, push=4,
                               hitbox=(28, 32, 52, 26), anim='cpunch'),
        'kick': Attack('Pernada Única', 6, 4, 11, 9, hitstun=16, push=6.5,
                       hitbox=(36, 58, 62, 36), anim='kick'),
        'air_kick': Attack('Voadora do Vento', 5, 7, 8, 8, hitstun=15, push=5,
                           hitbox=(26, 60, 54, 42), aerial=True, anim='air'),
        'special_p': Attack('REDEMOINHO', 11, 2, 17, 0, anim='whirl_cast',
                            projectile=dict(kind='whirl', speed=5.5, damage=10,
                                            knockdown=True, chip=3, h=58)),
        'special_k': Attack('SUMIÇO', 8, 2, 13, 0, teleport=True, anim='whirl_cast'),
    }


# ---------------- CURUPIRA ----------------
def draw_curupira(surf, f):
    P = pose(f)
    W = world(f, P)
    hip, neck, head = W('hip'), W('neck'), W('head')
    hand_f, hand_b = W('hand_f'), W('hand_b')
    fc = f.facing
    a = f.attack
    j1, j2, j3 = _jit(f, 4), _jit(f, 5), _jit(f, 6)
    sh_b = (neck[0] - 8 * fc, neck[1] + 8)
    sh_f = (neck[0] + 8 * fc, neck[1] + 8)
    ang_b = math.atan2(hand_b[1] - sh_b[1], hand_b[0] - sh_b[0])
    ang_f = math.atan2(hand_f[1] - sh_f[1], hand_f[0] - sh_f[0])

    # braço de trás
    hose(surf, sh_b, hand_b, 11 * fc, 10, C.SKIN_CURU, j1)
    glove(surf, hand_b, 9, ang_b)
    # pernas com pés ao contrário
    for key, bd, jj in (('foot_b', 9, j2), ('foot_f', -9, j3)):
        ft = W(key)
        if key == 'foot_f' and _smear_now(f) and a.anim in ('kick', 'air'):
            smear_fan(surf, hip, ft, _mix(C.SKIN_CURU, C.PAPER, 0.55))
        hose(surf, (hip[0], hip[1] - 4), ft, bd * fc, 13, C.SKIN_CURU, jj)
        bigfoot(surf, ft, fc, C.SKIN_CURU, 1.2, back=True)
    # tanga de folhas
    for i in (-1, 0, 1):
        poly(surf, [(hip[0] + i * 10 - 6, hip[1] - 6),
                    (hip[0] + i * 10 + 6, hip[1] - 6),
                    (hip[0] + i * 10 + math.sin(f.anim * 0.2 + i) * 3, hip[1] + 12)],
             C.GREEN_D)
    # corpo feijão (túnica verde)
    mid = ((hip[0] + neck[0]) / 2 + j1[0] * 0.4, (hip[1] + neck[1]) / 2 + 6)
    blob(surf, mid, 20, 24, C.GREEN_M)
    blob(surf, (mid[0] + 2 * fc, mid[1] + 8), 14, 12, C.GREEN_L)  # barriga clara
    # cabeça grande
    hd = (head[0] + j3[0], head[1] + j3[1])
    # juba de fogo (atrás da cabeça): camada externa com tinta, interna sem
    if f.state != KO:
        n = 6
        for col, hs, ink in ((C.FIRE_1, 1.0, True), (C.FIRE_2, 0.58, False)):
            for i in range(n):
                ang = math.pi * (0.08 + 0.84 * i / (n - 1))
                bx = hd[0] - math.cos(ang) * 19 * fc
                by = hd[1] - math.sin(ang) * 17 - 4
                tall = 1.5 if i in (2, 3) else 1.0
                h = (17 + 8 * math.sin(f.anim * 0.32 + i * 1.9)) * hs * tall
                wob = math.sin(f.anim * 0.27 + i * 2.1) * 5
                tipx = bx + wob - math.cos(ang) * h * 0.7 * fc
                poly(surf, [(bx - 6, by), (bx + 6, by), (tipx, by - h)], col, ink)
    blob(surf, hd, 23, 21, C.SKIN_CURU)
    blob(surf, (hd[0] - 18 * fc, hd[1] + 3), 5.5, 7, C.SKIN_CURU)  # orelha pontuda
    cartoon_face(surf, f, hd, fc, 23)
    # braço da frente, com smear no soco
    if _smear_now(f) and a.anim in ('punch', 'cpunch'):
        smear_fan(surf, sh_f, hand_f, _mix(C.SKIN_CURU, C.PAPER, 0.55))
    hose(surf, sh_f, hand_f, -11 * fc, 11, C.SKIN_CURU, j1)
    glove(surf, hand_f, 10, ang_f)


def curupira_portrait(surf, cx, cy, s=1.0):
    head = (cx, cy + 8 * s)
    n = 6
    for col, hs, ink in ((C.FIRE_1, 1.0, True), (C.FIRE_2, 0.6, False)):
        for i in range(n):
            ang = math.pi * (0.1 + 0.8 * i / (n - 1))
            bx = cx - math.cos(ang) * 26 * s
            by = cy - math.sin(ang) * 22 * s + 4 * s
            tall = 1.5 if i in (2, 3) else 1.0
            h = (24 + (i % 2) * 8) * s * hs * tall
            poly(surf, [(bx - 8 * s, by), (bx + 8 * s, by), (bx, by - h)], col, ink)
    blob(surf, head, 28 * s, 26 * s, C.SKIN_CURU)
    for ox in (12 * s, -4 * s):
        e = (cx + ox, cy + 4 * s)
        blob(surf, e, 7.5 * s, 9 * s, C.WHITE_W)
        p = (e[0] + 2.5 * s, e[1] + 2.5 * s)
        pygame.draw.circle(surf, C.INK, _pt(p), int(5 * s))
        pygame.draw.polygon(surf, C.WHITE_W,
                            [_pt(p), _pt((p[0] + 5 * s, p[1] - 5 * s)),
                             _pt((p[0] + 1.5 * s, p[1] - 6 * s))])
    pygame.draw.line(surf, C.INK, (cx - 14 * s, cy - 6 * s), (cx + 4 * s, cy - 1 * s),
                     max(2, int(4 * s)))
    # sorriso dentuço
    rct = pygame.Rect(0, 0, int(22 * s), int(9 * s))
    rct.center = (int(cx + 6 * s), int(cy + 22 * s))
    pygame.draw.rect(surf, C.INK, rct.inflate(OUT * 2, OUT * 2))
    pygame.draw.rect(surf, C.WHITE_W, rct)
    for i in (1, 2):
        pygame.draw.line(surf, C.INK, (rct.left + i * rct.w // 3, rct.top),
                         (rct.left + i * rct.w // 3, rct.bottom), 1)


def curupira_moves():
    return {
        'punch': Attack('Cascudo', 5, 3, 9, 7, hitstun=14, push=5,
                        hitbox=(32, 82, 54, 32), anim='punch'),
        'crouch_punch': Attack('Soco de Raiz', 5, 3, 10, 6, hitstun=13, push=4.5,
                               hitbox=(30, 30, 52, 26), anim='cpunch'),
        'kick': Attack('Coice Trocado', 8, 4, 13, 11, hitstun=18, push=7.5,
                       hitbox=(38, 54, 64, 38), anim='kick'),
        'air_kick': Attack('Galho Seco', 6, 7, 9, 9, hitstun=16, push=5.5,
                           hitbox=(28, 58, 56, 44), aerial=True, anim='air'),
        'special_p': Attack('BRASA DA JUBA', 13, 2, 19, 0, anim='cast',
                            projectile=dict(kind='fire', speed=4.6, damage=11,
                                            chip=3, h=74)),
        'special_k': Attack('TRUPIDA', 10, 10, 15, 13, hitstun=20, push=8,
                            hitbox=(30, 72, 56, 62), lunge=7.5,
                            knockdown=True, chip=2, anim='lunge'),
    }


# ---------------- projéteis ----------------
def draw_projectile(surf, pr):
    t = pr.age
    if pr.kind == 'whirl':
        _tornado(surf, pr.x, pr.y + 28, t * 1.6, scale=0.62)
    else:  # bola de fogo cartoon
        d = 1 if pr.vx > 0 else -1
        flick = math.sin(t * 0.9) * 3
        # cauda de chamas
        for j, hs in enumerate((1.0, 0.7, 0.45)):
            tx = pr.x - pr.vx * (j + 1) * 2.4
            ty = pr.y + math.sin(t * 0.7 + j) * 5
            poly(surf, [(tx, ty - 8 * hs), (tx, ty + 8 * hs),
                        (tx - d * 16 * hs, ty + math.sin(t + j) * 4)],
                 C.FIRE_2, ink=(j == 0))
        blob(surf, (pr.x, pr.y), 15 + flick, 13, C.FIRE_1)
        blob(surf, (pr.x + d * 4, pr.y), 8, 7, C.FIRE_2)
        # olhinhos bravos na bola de fogo
        e = (pr.x + d * 7, pr.y - 4)
        pygame.draw.circle(surf, C.INK, _pt(e), 2)
        pygame.draw.line(surf, C.INK, (e[0] - d * 4, e[1] - 4), (e[0] + d * 2, e[1] - 2), 2)


# ---------------- definição de personagem ----------------
@dataclass
class CharacterDef:
    name: str
    title: str
    hp: int
    speed: float
    jump: float
    moves: dict
    draw: object
    portrait: object
    accent: tuple


SACI = CharacterDef('SACI-PERERÊ', 'O Travesso do Redemoinho',
                    hp=95, speed=3.4, jump=-13.2,
                    moves=saci_moves(), draw=draw_saci,
                    portrait=saci_portrait, accent=C.RED)

CURUPIRA = CharacterDef('CURUPIRA', 'O Guardião da Mata',
                        hp=110, speed=2.7, jump=-12.2,
                        moves=curupira_moves(), draw=draw_curupira,
                        portrait=curupira_portrait, accent=C.FIRE_1)

CHARACTERS = [SACI, CURUPIRA]
