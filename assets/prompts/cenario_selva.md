# Prompts — Cenário: A SELVA (Nano Banana Pro)

Duas camadas, como você pediu:

1. **FUNDO (estático)** — a vista profunda da mata, desenhada atrás de tudo. Não
   se mexe. Imagem **opaca**, tela cheia.
2. **FRENTE (animada)** — a folhagem perto dos lutadores (folhas grandes nos
   cantos de baixo, cipós pendurados no topo), que **balança** de leve. Imagem
   **transparente** (fundo magenta), por cima da cena, **emoldurando sem cobrir**
   a área central onde os lutadores se movem.

Quando estiverem prontas, me mande — eu escrevo o loader (carrega o fundo, anima
a frente com balanço/parallax) e alinho com o chão do jogo.

## Restrições técnicas (importantes pro encaixe)
- **Proporção 16:9** (ex.: 1536×864). É o formato da tela (960×540).
- **Linha do chão a ~87% da altura** (de cima pra baixo) — é onde os lutadores
  pisam. Mantenha o solo/clareira nessa faixa nas duas camadas.
- **Contraste forte e cores ricas** (a versão pálida sumia contra a vinheta).
  Paleta vintage quente, mas saturada — não lavada.
- **FRENTE**: fundo **magenta uniforme (#FF00FF)** onde for transparente. O
  **MEIO/centro tem que ficar vazio (só magenta)** — folhagem só nos cantos de
  baixo, nas laterais e pendurada do topo, pra não tampar a luta.

## BLOCO DE ESTILO (cole nos dois)
> 1930s rubber hose cartoon, Cuphead game background art, hand-painted cel look,
> bold black ink outlines on the nearer shapes, flat colors with simple cel
> shading, muted-but-saturated vintage palette, warm filtered light, clean
> readable shapes, no text, no characters, no watermark.

---

## CAMADA 1 — FUNDO ESTÁTICO (opaco, tela cheia)

```
A 16:9 hand-painted background plate for a 2D fighting game, 1930s rubber hose
cartoon / Cuphead background style, flat colors with simple cel shading, muted
but saturated vintage palette, bold ink outlines on nearer shapes. Subject: a
deep Brazilian rainforest (Mata Atlântica) clearing seen straight-on, with clear
depth in layers:
- TOP: a dense dark-green canopy with a gap letting warm golden light pour down
  in soft god-rays.
- FAR: misty pale-green distant trees and hills, atmospheric perspective (lighter
  and bluer the farther away).
- MID: tall thick tree trunks and big tropical leaves (monstera, banana fronds),
  hanging lianas, layered greens from olive to deep forest green.
- A flat mossy CLEARING FLOOR running across the image at about 87% of the
  height from the top, where fighters will stand — keep this ground band clear
  and unobstructed.
Warm sepia-tinged 1930s film mood, rich contrast, fireflies/golden dust motes in
the air. No characters, no text, no UI, no border. Fill the whole frame edge to
edge (opaque, no transparency).
```

---

## CAMADA 2 — FRENTE ANIMADA (transparente, emoldura sem cobrir)

```
A 16:9 foreground overlay layer for a 2D fighting game, on a FLAT SOLID MAGENTA
background (#FF00FF) that fills the entire CENTER of the image (the middle must
stay empty magenta so it never covers the fighters). 1930s rubber hose cartoon /
Cuphead style, bold black ink outlines, flat colors with simple cel shading,
saturated jungle greens, warm vintage palette. Paint near-foreground jungle
foliage ONLY around the edges, framing the scene:
- BOTTOM-LEFT and BOTTOM-RIGHT corners: big lush ferns, broad tropical leaves
  (monstera/banana) and tall grasses rising from the bottom edge, slightly
  out-of-focus near plants, darker and richer than the background.
- TOP edge: a few hanging lianas/vines with leaves and little hanging flowers,
  dangling down from the top into the upper corners.
- Optionally a couple of big leaf silhouettes poking in from the far left/right
  sides.
Everything reads as the closest layer (boldest outlines, deepest saturation).
Leave the whole central area and the lower-middle (where characters fight and
stand) as pure empty magenta. No characters, no text, no border.
```

---

## Opcional — MEIO (parallax suave, se quiser mais profundidade)
Uma 3ª camada transparente (magenta) com troncos/folhagem de profundidade
intermediária, que se move **menos** que a frente. Mesmo bloco de estilo; peça
"midground jungle trunks and foliage band across the middle, on magenta, leaving
the ground clear". Dá pra adicionar depois sem refazer as outras.

## Como entra no jogo
Salve em `assets/sprites/stages/selva/`:
- `fundo.png` (Camada 1, opaca)
- `frente.png` (Camada 2, magenta/transparente)
- `meio.png` (opcional)

Me avise. Eu carrego o fundo estático atrás dos lutadores e animo a frente com um
balanço senoidal suave (e leve parallax), alinhando a linha do chão com o
`FLOOR_Y` do jogo. A vinheta + grão de filme continuam por cima, dando o
acabamento vintage.
