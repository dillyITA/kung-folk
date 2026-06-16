# Sprites desenhados

Coloque aqui os PNGs por personagem. O jogo usa o sprite onde existir e cai no
desenho **procedural** para o resto — dá pra migrar uma animação por vez.

```
assets/sprites/
  saci/
    idle.png      walk.png     jump.png     crouch.png
    punch.png     crouch_punch.png          kick.png     air_kick.png
    special_p.png special_k.png
    hitstun.png   block.png    knockdown.png  ko.png     win.png
  curupira/
    ...mesmos nomes...
```

(Arquivos com nomes fora dessa lista — como `_model_sheet.png` — são ignorados.)

## Regras de cada PNG

- **Uma tira horizontal**: todos os frames da animação lado a lado, virados
  para a **direita** (o motor espelha para a esquerda sozinho).
- **Fundo magenta/roxo uniforme** (o tom não precisa ser exato — o chroma-key
  amostra a cor real dos cantos). Sem cenário, sem texto, sem bordas.
- **Pés do personagem na mesma base** em todos os frames (senão ele "desliza").
- Espaço de fundo claro **entre** os frames (o fatiador separa por essas
  lacunas). Pode haver pequenos detritos (faíscas, fumaça) — fragmentos
  minúsculos são descartados.
- Frames com mesma altura de personagem; o pipeline normaliza a escala pela
  animação `idle`.

## Nomes e nº de frames sugeridos

| Arquivo | Frames | Loop |
|---|---|---|
| idle | 4–6 | sim |
| walk | 6–8 | sim |
| jump | 3 | não |
| crouch | 2 | sim |
| punch | 4–6 | não |
| crouch_punch | 4 | não |
| kick | 5–7 | não |
| air_kick | 4 | não |
| special_p / special_k | 5–10 | não |
| hitstun | 2–3 | não |
| block | 1–2 | sim |
| knockdown | 4–6 | não |
| ko | 2 | sim |
| win | 4–6 | sim |

Os prompts de geração de cada um estão em `assets/prompts/`. Se o fatiador
contar frames errado numa tira, me avise — adicionamos um `sprites.json` com a
contagem manual por animação.
