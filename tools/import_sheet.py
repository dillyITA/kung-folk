"""Converte uma FOLHA rotulada (várias linhas, rótulos de texto à esquerda,
fundo magenta) em strips por animação que o pipeline de runtime consome.

  .venv/bin/python tools/import_sheet.py assets/sprites/saci/_sheet_raw.png saci

Detecta as linhas pelas âncoras dos rótulos (margem esquerda), descarta o texto
por altura, fatia cada linha em figuras e RECONCILIA com a contagem conhecida
(funde figuras partidas / divide as que se encostam). Salva
assets/sprites/<dir>/<animacao>.png como strip transparente.

Layout padrão (ordem das linhas + nº de frames) — sobrescreva com um arquivo
<dir>/layout.txt (uma linha "nome contagem" por linha) se a folha for outra."""
import os
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import numpy as np                       # noqa: E402
import pygame                            # noqa: E402
from kungfolk import sprites as S        # noqa: E402

DEFAULT_LAYOUT = [
    ('idle', 6), ('walk', 6), ('jump', 3), ('crouch', 2), ('punch', 5),
    ('crouch_punch', 4), ('kick', 6), ('air_kick', 4), ('special_p', 5),
    ('special_k', 5), ('hitstun', 3), ('block', 2), ('knockdown', 5),
    ('ko', 2), ('win', 5),
]
LABEL_MARGIN = 180   # x: figuras começam depois disso; rótulos ficam antes
GAP_PAD = 22         # padding magenta entre frames no strip de saída


def col_runs(col, gap_min, min_w):
    raw, j, n = [], 0, len(col)
    while j < n:
        if col[j]:
            k = j
            while k < n and col[k]:
                k += 1
            raw.append([j, k])
            j = k
        else:
            j += 1
    merged = []
    for r in raw:
        if merged and r[0] - merged[-1][1] < gap_min:
            merged[-1][1] = r[1]
        else:
            merged.append(r[:])
    return [r for r in merged if r[1] - r[0] >= min_w]


def reconcile(runs, count):
    """Ajusta a lista de runs para exatamente `count` figuras."""
    runs = [list(r) for r in runs]
    while len(runs) > count:                       # funde o menor vão
        i = min(range(len(runs) - 1), key=lambda i: runs[i + 1][0] - runs[i][1])
        runs[i][1] = runs[i + 1][1]
        del runs[i + 1]
    while len(runs) < count and runs:              # divide o mais largo
        i = max(range(len(runs)), key=lambda i: runs[i][1] - runs[i][0])
        x0, x1 = runs[i]
        mid = (x0 + x1) // 2
        runs[i] = [x0, mid]
        runs.insert(i + 1, [mid, x1])
    return runs


def load_layout(out_dir):
    p = os.path.join(out_dir, 'layout.txt')
    if not os.path.exists(p):
        return DEFAULT_LAYOUT
    out = []
    with open(p) as fh:
        for line in fh:
            line = line.split('#')[0].split()
            if len(line) == 2:
                out.append((line[0], int(line[1])))
    return out or DEFAULT_LAYOUT


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sheet_path, char_dir = sys.argv[1], sys.argv[2]
    out_dir = os.path.join(S.ASSET_ROOT, char_dir)
    os.makedirs(out_dir, exist_ok=True)
    layout = load_layout(out_dir)

    pygame.init()
    pygame.display.set_mode((4, 4))
    img = pygame.image.load(sheet_path).convert_alpha()
    w, h = img.get_size()
    rgb = pygame.surfarray.array3d(img).astype(np.int16)
    bg = S.dominant_bg(rgb)
    alpha = S.alpha_from_bg(rgb, bg)
    fg = alpha > 40
    fg[:6, :] = fg[-6:, :] = False
    fg[:, :6] = fg[:, -6:] = False
    print('fundo detectado (RGB):', bg.tolist())

    # âncoras de linha = clusters de rótulo na margem esquerda
    strip = fg[8:LABEL_MARGIN, :]
    ys = np.where(strip.sum(axis=0) > 1)[0]
    labels, s, p = [], None, None
    for y in ys:
        if s is None:
            s = p = y
        elif y - p > 60:
            labels.append((s + p) // 2)
            s = y
        p = y
    if s is not None:
        labels.append((s + p) // 2)
    print('linhas detectadas:', len(labels))

    made, bounds = [], {}
    for i, center in enumerate(labels):
        if i >= len(layout):
            print('  (linha %d sem nome no layout — ignorada)' % i)
            continue
        name, count = layout[i]
        a = max(0, center - 46) if i > 0 else 0
        b = (labels[i + 1] - 46) if i + 1 < len(labels) else h
        band = fg[:, a:b].copy()
        rowh = b - a
        # APAGA O RÓTULO: texto fica numa faixa fina em torno do y do rótulo,
        # da esquerda até o 1º vão grande (as figuras começam depois). Funciona
        # com o rótulo acima das figuras (folha 1) ou ao lado delas (folha 2).
        sy0, sy1 = max(0, center - 40 - a), min(rowh, center + 40 - a)
        sx = np.where(band[:, sy0:sy1].any(axis=1))[0]
        if len(sx):
            lr, prev = sx[-1] + 1, sx[0]
            for x in sx[1:]:
                if x - prev - 1 >= 32:
                    lr = prev + 1
                    break
                prev = x
            band[:lr, sy0:sy1] = False
        # FIGURA: coluna com conteúdo na metade de baixo da linha.
        lower = int(rowh * 0.42)
        fig_col = band[:, lower:].any(axis=1)
        runs = col_runs(fig_col, gap_min=max(8, w // 110), min_w=max(20, w // 90))
        runs = reconcile(runs, count)
        frames = [_crop(img, alpha, r[0], r[1], a, b) for r in runs]
        frames = [f for f in frames if f is not None]
        bounds[name] = _save_strip(frames, os.path.join(out_dir, name + '.png'))
        made.append('%s(%d)' % (name, len(frames)))
        print('  %-13s -> %d frames' % (name, len(frames)))

    # grava as fronteiras exatas dos frames (merge com o que já existir, pois
    # cada folha cobre só parte das animações do personagem)
    import json
    jp = os.path.join(out_dir, 'sprites.json')
    meta = {}
    if os.path.exists(jp):
        with open(jp) as fh:
            meta = json.load(fh)
    meta.update(bounds)
    with open(jp, 'w') as fh:
        json.dump(meta, fh, indent=0)

    print('\nstrips salvos em %s:\n  %s' % (out_dir, '  '.join(made)))
    pygame.quit()


def _vruns(mask):
    out, j, n = [], 0, len(mask)
    while j < n:
        if mask[j]:
            k = j
            while k < n and mask[k]:
                k += 1
            out.append((j, k))
            j = k
        else:
            j += 1
    return out


def _crop(img, alpha, x0, x1, ay, by):
    """Recorta a figura no run (x0..x1), pegando o maior bloco vertical de
    conteúdo (descarta texto de rótulo que sobre por cima da figura)."""
    a = alpha[x0:x1, ay:by]
    fgm = a > 40
    vr = _vruns(fgm.any(axis=0))
    if not vr:
        return None
    y0, y1 = max(vr, key=lambda r: r[1] - r[0])     # bloco mais alto = figura
    xs = np.where(fgm[:, y0:y1].any(axis=1))[0]
    if not len(xs):
        return None
    fx0, fx1 = int(xs[0]), int(xs[-1]) + 1
    sub = img.subsurface(pygame.Rect(x0 + fx0, ay + y0, fx1 - fx0, y1 - y0)).copy()
    pa = pygame.surfarray.pixels_alpha(sub)
    pa[:] = a[fx0:fx1, y0:y1]
    del pa
    return sub


def _save_strip(frames, path):
    """Empacota os frames num strip transparente, alinhados pela base.
    Devolve [[x, largura], ...] de cada frame (fronteiras exatas p/ o runtime)."""
    if not frames:
        return []
    fw = [f.get_width() for f in frames]
    fh = [f.get_height() for f in frames]
    total_w = sum(fw) + GAP_PAD * (len(frames) + 1)
    total_h = max(fh) + GAP_PAD * 2
    strip = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
    x = GAP_PAD
    base = total_h - GAP_PAD
    bounds = []
    for f in frames:
        strip.blit(f, (x, base - f.get_height()))
        bounds.append([x, f.get_width()])
        x += f.get_width() + GAP_PAD
    pygame.image.save(strip, path)
    return bounds


if __name__ == '__main__':
    main()
