# Prompts — Saci-Pererê: as 6 animações que faltam (Nano Banana Pro)

Gere **UMA folha** no mesmo formato da primeira (linhas rotuladas à esquerda,
fundo magenta), contendo só estas 6 animações que ficaram de fora. Depois é só
me mandar o PNG que eu importo (cuido do mapeamento dos nomes).

## Antes de gerar
- **Anexe o `_model_sheet.png`** (a referência) na geração, para manter o Saci
  idêntico.
- Fundo **magenta/roxo uniforme**, sem cenário. Sem bordas.
- Personagem **virado para a direita** (o motor espelha sozinho).
- **Pés na mesma linha de base** em cada linha; cada figura inteira dentro da
  célula; espaço de fundo claro entre as figuras.
- Cada linha com um **rótulo à esquerda** exatamente como abaixo (com o número
  de frames entre parênteses) — é por ele que o importador acha as linhas.

## BLOCO DE ESTILO (cole junto)
> 1930s rubber hose cartoon, Cuphead game art style, hand-drawn cel animation,
> thick slightly-uneven black ink outlines, flat colors, no gradients, no
> shading, muted vintage palette, clean silhouette

## FICHA (cole junto)
> Saci-Pererê: small mischievous one-legged boy, dark brown skin, round belly,
> bare chest, red shorts with a small gold patch, floppy red stocking cap with
> a gold pom-pom, smoking a corncob pipe, white four-finger rubber-hose gloves,
> ONE single centered leg ending in one big bare foot, big oval eyes with black
> pie-cut pupils, cheeky grin.

---

## PROMPT MESTRE (gera a folha inteira de uma vez)

```
A single 2D fighting-game sprite sheet on a flat solid magenta background
(#FF00FF), no scenery, no borders. 1930s rubber hose cartoon, Cuphead game art
style, thick black ink outlines, flat colors. Use the attached reference
(Saci-Pererê) EXACTLY in every frame — same design, colors and proportions.
Lay out SIX animation rows, each as one horizontal strip of equal cells, with a
small white text label at the far left of each row. All characters face right,
feet on the row baseline, fully inside each cell. The rows, top to bottom:

Row 1 — label "SPECIAL K - SUMICO (5)": he vanishes into a whirlwind. Frame 1:
crossing arms, mischievous grin. Frame 2: body twisting like a corkscrew.
Frame 3: turned into a small cream-and-sepia tornado with his red cap spinning
on top. Frame 4: tornado shrinking, leaves flying. Frame 5: only a puff of
smoke and the cap falling — he is gone.

Row 2 — label "HITSTUN (3)": getting hit from the right. Frame 1: head snapped
back, mouth open in a big O, cap flying off. Frame 2: body bent backwards like
a banana, arms flailing, little stars around the head. Frame 3: stumbling,
regaining balance.

Row 3 — label "BLOCK (2)": blocking, arms crossed in front of the face, gloves
forward like a shield, body braced, one eye peeking between the gloves. Frame 2
nearly identical with a small impact shake.

Row 4 — label "KNOCKDOWN (5)": knocked down and getting up. Frame 1: launched
backwards in mid-air, limbs flailing, cap detached. Frame 2: hitting the ground
on his back, dust clouds. Frame 3: flat on the ground, dizzy, stars circling.
Frame 4: pushing himself up with the gloves, grabbing the cap. Frame 5: back on
his single leg, shaking it off.

Row 5 — label "KO (2)": knocked out, lying flat on his back, X eyes, tongue
out, cap fallen beside the head, pipe puffing a sad little smoke ring. Frame 2
identical but the belly rises (breathing) and the smoke drifts.

Row 6 — label "WIN (5)": victory dance, hopping joyfully on his single leg,
sweeping the red cap off and waving it, huge grin, pipe smoke forming a heart.
Frames: hop up with cap raised, apex waving cap, landing squash, hop again,
big final pose with cap high.
```

---

## Se preferir gerar uma linha por vez
Use o mesmo bloco de estilo + ficha e peça "one horizontal strip of N frames on
magenta, label '<NOME> (N)' at the left", com a descrição da linha acima.
Contagens: special_k 5 · hitstun 3 · block 2 · knockdown 5 · ko 2 · win 5.

## Como entra no jogo
Me mande o PNG (salve em `assets/sprites/saci/_sheet2_raw.png`). Eu rodo o
importador apontando essas 6 linhas para os nomes certos (via `layout.txt`), ele
gera `special_k.png`, `hitstun.png`, `block.png`, `knockdown.png`, `ko.png`,
`win.png`, e o Saci fica **100% desenhado** — sem mais cair no procedural.
