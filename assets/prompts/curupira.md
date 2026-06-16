# Prompts — Curupira (Nano Banana Pro)

Mesmo fluxo que funcionou no Saci:
1. Gere o **model sheet (PROMPT 0)** primeiro, escolha o melhor, salve em
   `assets/sprites/curupira/_model_sheet.png` (referência, o `_` faz o jogo
   ignorar).
2. Gere a **FOLHA A** (9 animações) e a **FOLHA B** (6 animações), **anexando o
   model sheet como referência** em cada geração. Salve em
   `assets/sprites/curupira/_sheet_raw.png` e `_sheet2_raw.png`.
3. Me mande — eu importo (cuido do mapeamento dos nomes).

## Regras de cada folha
- Fundo **magenta/roxo uniforme**, sem cenário, sem bordas.
- Personagem **virado para a direita** (o motor espelha sozinho).
- **Pés na linha de base** em cada linha; figura inteira dentro da célula;
  espaço de fundo claro entre as figuras.
- Cada linha com um **rótulo branco à esquerda** exatamente como indicado.

## BLOCO DE ESTILO (cole em tudo)
> 1930s rubber hose cartoon, Cuphead game art style, hand-drawn cel animation,
> thick slightly-uneven black ink outlines, flat colors, no gradients, no
> shading, muted vintage palette, clean silhouette

## FICHA DO CURUPIRA (cole em tudo)
> Curupira from Brazilian folklore: a fierce little forest-guardian imp, coppery
> red-brown skin, a wild blazing mane of orange-and-yellow FLAMES for hair, big
> pointed ears, a jagged grin of sharp saw-like teeth, a short skirt of green
> leaves, white four-finger rubber-hose cartoon gloves, big oval eyes with black
> pie-cut pupils (white wedge notch), a wild mischievous scowl. His SIGNATURE
> TRAIT: BOTH FEET ARE TURNED BACKWARDS — heels point forward, toes point
> backward (draw this clearly in every frame).

---

## PROMPT 0 — Model sheet (gerar primeiro; 4:3 ou 1:1)

```
Character model sheet, 1930s rubber hose cartoon, Cuphead game art style,
thick slightly-uneven black ink outlines, flat colors, no gradients, no
shading, muted vintage palette. Character: Curupira from Brazilian folklore —
a fierce little forest-guardian imp, coppery red-brown skin, a wild blazing
mane of orange-and-yellow FLAMES for hair, big pointed ears, a jagged grin of
sharp saw-like teeth, a short skirt of green leaves, white four-finger
rubber-hose gloves, big oval eyes with black pie-cut pupils. SIGNATURE TRAIT:
both feet are turned BACKWARDS — heels forward, toes pointing back.
Sheet layout: the same character drawn 4 times in a row on a flat solid magenta
background (#FF00FF): front view, 3/4 view facing right, side view facing right
(clearly showing the backward feet), back view. Same height, feet aligned on
one baseline. Below: 3 small head studies (fierce grin with saw teeth, angry
roaring, dizzy with X eyes and the mane reduced to embers). No text, no labels,
no watermarks, no scenery.
```

---

## FOLHA A — 9 animações de combate (gerar de uma vez, anexando o model sheet)

```
A single 2D fighting-game sprite sheet on a flat solid magenta background
(#FF00FF), no scenery, no borders. 1930s rubber hose cartoon, Cuphead game art
style, thick black ink outlines, flat colors. Use the attached reference
(Curupira) EXACTLY in every frame — same design, colors, the flaming mane, the
saw teeth and the BACKWARD FEET. Lay out NINE animation rows, each a horizontal
strip of equal cells, with a small white text label at the far left of each
row. All characters face right, feet on the row baseline, fully inside each
cell. Rows, top to bottom:

Row 1 — "IDLE (6)": breathing idle loop, fists up in a relaxed guard, the mane
flickering, backward feet planted, subtle up-and-down bounce.

Row 2 — "WALK (6)": a stomping walk cycle on his backward feet (heels leading),
mane trailing behind, a little dust puff on each step.

Row 3 — "JUMP (3)": jump. Frame 1 rising, body and mane stretched up. Frame 2
apex, knees tucked. Frame 3 falling, arms up, mane streaming.

Row 4 — "CROUCH (2)": crouching low on bent legs, guard up, mane drooping over
the brow. Frame 2 a tiny idle wobble.

Row 5 — "PUNCH (5)": a hard knuckle bonk. Frame 1 guard. Frame 2 anticipation,
fist pulled far back, gritted saw teeth. Frame 3 SMEAR FRAME, the arm a
stretched motion-blur fan. Frame 4 full extension, glove huge, leaning in.
Frame 5 recovering to guard.

Row 6 — "CROUCH PUNCH (4)": low jab while crouching. Frame 1 crouched guard.
Frame 2 fist back. Frame 3 low straight punch near the ground with smear lines.
Frame 4 back to crouched guard.

Row 7 — "KICK (6)": a backward mule-kick using his reversed feet — he tips
forward and lashes the leg out behind/forward. Frame 1 stance. Frame 2 winding,
leg coiled. Frame 3 SMEAR FRAME, the kicking leg a wide motion arc. Frame 4 leg
fully extended, big backward foot huge. Frame 5 retracting. Frame 6 landing,
dust puff.

Row 8 — "AIR KICK (4)": a flying kick in mid-air (floating mid-cell). Frame 1
airborne, leg coiled. Frame 2 thrusting out with smear. Frame 3 full extension,
body stretched diagonally, mane trailing. Frame 4 holding the pose.

Row 9 — "SPECIAL P (5)": BRASA DA JUBA — he rips a ball of fire from his blazing
mane and hurls it forward. Frame 1 winding up, hand grabbing the mane, sparks.
Frame 2 a glowing ember forming in his gloved hand. Frame 3 throwing it forward,
body leaning in. Frame 4 the fireball leaving his hand, follow-through pose.
Frame 5 recovering, mane settling.
```

---

## FOLHA B — 6 animações restantes (gerar de uma vez, anexando o model sheet)

```
A single 2D fighting-game sprite sheet on a flat solid magenta background
(#FF00FF), no scenery, no borders. 1930s rubber hose cartoon, Cuphead game art
style, thick black ink outlines, flat colors. Use the attached reference
(Curupira) EXACTLY in every frame — flaming mane, saw teeth, backward feet. Lay
out SIX animation rows, each a horizontal strip of equal cells, small white
text label at the far left. All face right, feet on the baseline, fully inside
each cell. Rows, top to bottom:

Row 1 — "SPECIAL K (5)": TRUPIDA — a charging headbutt lunge, the flaming mane
leading like a comet. Frame 1 crouching to charge, sparks. Frame 2 launching
forward low, mane streaming back. Frame 3 full charge, head down, mane a blazing
trail, big smear. Frame 4 impact pose, mane flaring on contact. Frame 5
skidding to a stop, recovering.

Row 2 — "HITSTUN (3)": getting hit from the right. Frame 1 head snapped back,
mouth open, mane scattering sparks. Frame 2 body bent backwards, arms flailing,
little stars. Frame 3 stumbling, regaining balance.

Row 3 — "BLOCK (2)": blocking, arms crossed in front of the face, gloves
forward like a shield, body braced, mane pressed down, one eye peeking. Frame 2
identical with a small impact shake.

Row 4 — "KNOCKDOWN (5)": knocked down and getting up. Frame 1 launched backwards
in mid-air, limbs flailing, mane streaming. Frame 2 hitting the ground on his
back, dust clouds. Frame 3 flat on the ground, dizzy, stars circling, mane
flickering low. Frame 4 pushing himself up with the gloves. Frame 5 back on his
backward feet, mane reigniting, shaking it off.

Row 5 — "KO (2)": knocked out, lying flat on his back, X eyes, tongue out, the
mane reduced to a few sad smoking embers. Frame 2 identical but the chest rises
(breathing) and an ember drifts up.

Row 6 — "WIN (5)": victory dance — a fierce triumphant stomp, the mane flaring
huge and bright, arms raised, jagged grin, sparks flying. Frames: stomp down,
arms up roaring, mane at its biggest, a little hop, big final pose.
```

---

## Contagens (para conferência)
idle 6 · walk 6 · jump 3 · crouch 2 · punch 5 · crouch_punch 4 · kick 6 ·
air_kick 4 · special_p 5 · special_k 5 · hitstun 3 · block 2 · knockdown 5 ·
ko 2 · win 5

## Como entra no jogo
Salve as folhas em `assets/sprites/curupira/` (`_sheet_raw.png` = Folha A,
`_sheet2_raw.png` = Folha B) e me avise. Eu rodo o importador apontando os nomes
certos; ele gera os 15 PNGs e o Curupira fica 100% desenhado, igual ao Saci.
