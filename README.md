# KUNG-FOLK

Jogo de luta 2D do **folclore brasileiro**, com estética de cartoon vintage
(anos 1930, contorno grosso, sépia, grão de filme) — inspirado em Cuphead e
Street Fighter.

> **Status: protótipo (fatia vertical)** — Saci-Pererê vs Curupira, 1 cenário,
> 1v1 contra a máquina ou 2 jogadores no mesmo teclado, especiais com comando.

## Como rodar

Requer Python 3.9+.

**macOS / Linux**
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

**Windows**
```bat
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

## Controles

| Ação        | Jogador 1 | Jogador 2 |
|-------------|-----------|-----------|
| Andar       | A / D     | ← / →     |
| Pular       | W         | ↑         |
| Agachar     | S         | ↓         |
| Soco        | F         | K         |
| Chute       | G         | L         |
| Bloquear    | segurar a direção contrária ao oponente | idem |
| Pausa       | ESC       | ESC       |

**Especiais** — quarto de círculo pra frente: **↓ ↘ → + soco/chute**

| Personagem   | ↓↘→ + Soco          | ↓↘→ + Chute              |
|--------------|----------------------|--------------------------|
| Saci-Pererê  | **Redemoinho** (projétil que derruba) | **Sumiço** (some num redemoinho e reaparece atrás do oponente) |
| Curupira     | **Brasa da Juba** (bola de fogo)      | **Trupida** (investida de cabeça que derruba) |

## Regras

- Melhor de 3 rounds, 99 segundos por round.
- Bloquear especiais causa dano de raspão (*chip damage*).
- Um projétil por lutador em tela (regra clássica).

## Estrutura

```
main.py               ponto de entrada
kungfolk/
  config.py           tela, física, paleta vintage, controles
  engine.py           lutador, estados, frame data, projéteis, comandos (QCF)
  characters.py       golpes + desenho procedural (Saci, Curupira)
  ai.py               oponente CPU com nível de dificuldade
  stage.py            cenário da clareira, desenhado em código
  fx.py               partículas, filtro de filme vintage, SFX sintetizados
  scenes.py           título, modo, seleção, luta (HUD/rounds), resultado
  game.py             loop principal
tests/smoke.py        CPU vs CPU sem janela, valida o motor
```

## Visão / roadmap

- **Elenco**: Saci-Pererê, Iara, Curupira, Boitatá, Mula-sem-cabeça, Caipora,
  Lobisomem, Corpo-seco, Boto-cor-de-rosa, Cabra-cabriola, Bicho-Papão e
  **Cuca** (vilã final).
- **Campanha**: 10 lutas em dificuldade crescente; a ordem dos oponentes
  permuta a cada tentativa — só a Cuca é fixa no fim, querendo engolir o
  espírito do Brasil numa floresta interminável.
- **Arte**: os desenhos procedurais são placeholders animados; o plano é
  trocá-los por spritesheets desenhados à mão (estilo rubber hose) sem mexer
  no motor.
- Mais cenários temáticos (rio da Iara, lamaçal do Corpo-seco, caverna da
  Cuca…), trilha sonora, golpes EX e super medidor.
