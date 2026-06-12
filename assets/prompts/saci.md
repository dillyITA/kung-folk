# Prompts — Saci-Pererê (Nano Banana Pro)

## Como usar

1. Gere o **PROMPT 0 (model sheet)** primeiro. Gere 3–4 vezes, escolha a melhor.
   Essa imagem é a "bíblia" do personagem.
2. Em TODA geração seguinte, **anexe o model sheet como imagem de referência**
   e cole o prompt da animação (cada um já inclui o bloco de estilo).
3. Gere 2–3 candidatos por animação e escolha o mais consistente.
4. Salve como `assets/sprites/saci/<nome>.png` (idle.png, walk.png...).
   O fundo magenta e o espaçamento irregular eu resolvo no pipeline (chroma-key
   + fatiador automático).

**Aspect ratio por nº de frames:** 2–3 frames → 16:9 · 4–6 frames → 21:9
(ou o mais largo disponível) · 8+ frames → divida em duas gerações de 4–5
frames usando o mesmo prompt (parte 1 / parte 2).

---

## BLOCO DE ESTILO (já embutido em todos os prompts)

> 1930s rubber hose cartoon, Cuphead game art style, hand-drawn cel animation,
> thick slightly-uneven black ink outlines, flat colors, no gradients, no
> shading, muted vintage palette, clean silhouette

## FICHA DO PERSONAGEM (idem)

> Saci-Pererê from Brazilian folklore: small mischievous one-legged boy, dark
> brown skin, round cartoon belly, bare chest, red shorts with a small gold
> patch, floppy red stocking cap with a gold pom-pom on the drooping tip,
> smoking a small brown corncob pipe, white four-finger rubber-hose cartoon
> gloves, ONE single centered leg ending in one big bare cartoon foot, big
> oval eyes with black pie-cut pupils (white wedge notch), cheeky grin

---

## PROMPT 0 — Model sheet (gerar primeiro, 4:3 ou 1:1)

```
Character model sheet, 1930s rubber hose cartoon, Cuphead game art style,
hand-drawn cel animation, thick slightly-uneven black ink outlines, flat
colors, no gradients, no shading, muted vintage palette, clean silhouette.
Character: Saci-Pererê from Brazilian folklore: small mischievous one-legged
boy, dark brown skin, round cartoon belly, bare chest, red shorts with a small
gold patch, floppy red stocking cap with a gold pom-pom on the drooping tip,
smoking a small brown corncob pipe, white four-finger rubber-hose cartoon
gloves, ONE single centered leg ending in one big bare cartoon foot, big oval
eyes with black pie-cut pupils (white wedge notch), cheeky grin.
Sheet layout: the same character drawn 4 times in a row on a flat solid
magenta background (#FF00FF): front view, 3/4 view facing right, side view
facing right, back view. Same height, feet aligned on one baseline.
Below the row: 3 small head studies (grinning, angry with gritted teeth,
dizzy with X eyes). No text, no labels, no watermarks, no background scenery.
```

---

## ANIMAÇÕES
*(em todos: anexar o model sheet como referência)*

### idle.png — 6 frames, loop

```
Sprite sheet for a 2D fighting game, exactly 6 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê,
one-legged boy with red cap, red shorts, pipe, white gloves) EXACTLY — same
design, colors and proportions in every frame.
Animation: IDLE breathing loop, full body, facing right, standing balanced on
his single leg, fists up in a relaxed boxing guard. Frame by frame: subtle
bounce up and down, chest inflating and deflating, the cap tip swaying, a
small puff of pipe smoke appearing on frames 4-6. Feet on the same baseline
in all frames, character fully inside each cell.
```

### walk.png — 6 frames, loop

```
Sprite sheet for a 2D fighting game, exactly 6 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: HOP cycle (he has one leg, so he hops to move), full body, facing
right. Frame 1: crouched anticipation, knee bent, body squashed. Frame 2:
pushing off, body stretching up. Frame 3: airborne, cap and shorts trailing
up, leg tucked. Frame 4: apex, relaxed. Frame 5: landing, body squashing,
dust puff under the foot. Frame 6: recovering to standing. Strong squash and
stretch, baseline consistent.
```

### jump.png — 3 frames

```
Sprite sheet for a 2D fighting game, exactly 3 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: JUMP, full body, facing right. Frame 1: rising fast, body and cap
stretched vertically, leg extended down. Frame 2: apex, body neutral, leg
tucked under him, arms slightly open. Frame 3: falling, arms up, cap floating
above the head, foot reaching for the ground.
```

### crouch.png — 2 frames

```
Sprite sheet for a 2D fighting game, exactly 2 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: CROUCH, full body, facing right, ducking low on his bent single
leg, body compressed and squashed, guard up protecting the face, cap drooping
over the forehead. Frame 1 and frame 2 nearly identical with a tiny idle
wobble difference.
```

### punch.png — 5 frames

```
Sprite sheet for a 2D fighting game, exactly 5 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: STRAIGHT PUNCH with the white-gloved fist, full body, facing right.
Frame 1: guard stance. Frame 2: anticipation, fist pulled far back, body
twisted back, angry gritted teeth. Frame 3: SMEAR FRAME, the punching arm
drawn as a stretched motion-blur fan of multiple arm shapes. Frame 4: full
extension, arm very long (rubber hose stretch), glove huge, body leaning in.
Frame 5: recovering back to guard.
```

### crouch_punch.png — 4 frames

```
Sprite sheet for a 2D fighting game, exactly 4 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: LOW JAB while crouching on his bent single leg, full body, facing
right. Frame 1: crouched guard. Frame 2: fist pulled back. Frame 3: low
straight punch fully extended near the ground, smear lines behind the arm.
Frame 4: recovering to crouched guard.
```

### kick.png — 6 frames

```
Sprite sheet for a 2D fighting game, exactly 6 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: SPINNING ONE-LEG KICK — he briefly floats on a tiny dust whirlwind
while his single leg whips forward, full body, facing right. Frame 1: stance.
Frame 2: leaning back, leg coiled, small dust swirl forming under him.
Frame 3: SMEAR FRAME, the kicking leg drawn as a wide motion arc fan.
Frame 4: leg fully extended forward, big bare foot huge, toes spread.
Frame 5: leg retracting. Frame 6: landing back on the foot, dust puff.
```

### air_kick.png — 4 frames

```
Sprite sheet for a 2D fighting game, exactly 4 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: FLYING KICK in mid-air, full body, facing right, no ground contact
(draw him floating mid-cell). Frame 1: airborne, leg coiled. Frame 2: leg
thrusting forward-down with smear lines. Frame 3: full extension, foot first,
body stretched diagonally, cap trailing behind. Frame 4: holding the pose,
slight wobble.
```

### special_p.png — Redemoinho, 5 frames (parte 1 de 1)

```
Sprite sheet for a 2D fighting game, exactly 5 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: WHIRLWIND SPELL, full body, facing right. Frame 1: winding up,
both gloved arms spinning in circles, speed lines around the hands. Frame 2:
arms a blurred circular smear, a small cream-and-sepia tornado forming in
front of him with leaves. Frame 3: hurling the tornado forward, body leaning
in, arms thrown forward. Frame 4: the tornado detached, flying right, he
holds the follow-through pose. Frame 5: recovering to stance, dust settling.
```

### special_k.png — Sumiço (teleporte), 5 frames

```
Sprite sheet for a 2D fighting game, exactly 5 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: VANISHING INTO A WHIRLWIND, full body, facing right. Frame 1:
crossing arms, mischievous grin, cap tip rising. Frame 2: body twisting like
a corkscrew, shapes stretching into a spiral. Frame 3: fully transformed into
a small cream-and-sepia tornado with his red cap spinning on top. Frame 4:
the tornado shrinking, leaves flying. Frame 5: only a puff of smoke and the
cap falling — he is gone.
```

### hitstun.png — 3 frames

```
Sprite sheet for a 2D fighting game, exactly 3 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: GETTING HIT, full body, facing right (the blow comes from the
right). Frame 1: head snapped back, mouth open in a big O, eyes wide, cap
flying up off the head. Frame 2: body bent backwards like a banana, arms
flailing, tiny stars around the head. Frame 3: stumbling, regaining balance,
grabbing the cap back.
```

### block.png — 2 frames

```
Sprite sheet for a 2D fighting game, exactly 2 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: BLOCKING, full body, facing right, arms crossed in front of the
face, gloves forward like a shield, body braced and compressed, one eye
peeking between the gloves, cap pressed down. Frame 2 identical with a small
impact shake.
```

### knockdown.png — 5 frames

```
Sprite sheet for a 2D fighting game, exactly 5 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: KNOCKED DOWN AND GETTING UP, full body, facing right. Frame 1:
launched backwards in mid-air, limbs flailing, cap detached. Frame 2: hitting
the ground on his back, dust clouds, foot up. Frame 3: flat on the ground,
dizzy, little stars circling. Frame 4: pushing himself up with the gloves,
grabbing the cap. Frame 5: back on his single leg, shaking it off.
```

### ko.png — 2 frames, loop

```
Sprite sheet for a 2D fighting game, exactly 2 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: KNOCKED OUT, lying flat on his back on the ground, X eyes, tongue
out, cap fallen beside the head, pipe still puffing a sad little smoke ring.
Frame 2 identical but the belly rises (breathing) and the smoke ring drifts.
```

### win.png — 5 frames, loop

```
Sprite sheet for a 2D fighting game, exactly 5 frames in ONE horizontal row,
evenly spaced equal cells, flat solid magenta background (#FF00FF), no text,
no borders. 1930s rubber hose cartoon, Cuphead game art style, thick black
ink outlines, flat colors. Use the attached character reference (Saci-Pererê)
EXACTLY in every frame.
Animation: VICTORY DANCE, full body, facing the viewer slightly. He hops
joyfully on his single leg, sweeps the red cap off his head with one gloved
hand and waves it in the air, huge grin, pipe smoke making a heart shape.
Frames: hop up with cap raised, apex waving cap, landing squash, hop again,
big final pose with cap high and chest out.
```
