# psico-renew

Una skill de bienestar para Claude Code y Claude. Cuando estás estresado, frustrado con un bug o hablándote mal, te ayuda a:

1. **Calmar el cuerpo** con una respiración o un anclaje de 30–60 segundos si el malestar está alto.
2. **Renovar el pensamiento** con 2–3 preguntas respaldadas por la psicología (terapia cognitivo-conductual, ACT, autocompasión). Las busca en internet en fuentes clínicas confiables (NHS, APA, universidades, centros clínicos) y te dice de dónde salen.
3. **Volver al mundo real** con un mini-descanso: levantarte del escritorio, dejar la pantalla y la IA, y hablar con una persona de verdad.

Está pensada para ser **breve a propósito**: dos respuestas y a otra cosa. No busca que hables más con una IA, sino menos.

> **Importante:** psico-renew no es terapia ni sustituye a un profesional de la salud mental. Si estás en crisis o piensas en hacerte daño, contacta ya una línea de ayuda: **024** en España, **800 911 2000** en México, **\*4141** en Chile, **135** o **(011) 5275-1135** en Argentina, **988** en EE. UU., o busca la de tu país en [findahelpline.com](https://findahelpline.com). Ante peligro inmediato, llama al número de emergencias local.

## Instalación

### Claude Code, como plugin (recomendado)

```
/plugin marketplace add approvedworkman/psico-renew
/plugin install psico-renew@psico-renew
```

### Claude Code, copiando la skill

```bash
git clone https://github.com/approvedworkman/psico-renew.git
cp -r psico-renew/skills/psico-renew ~/.claude/skills/
```

Así queda disponible en todos tus proyectos. Para un solo proyecto, cópiala en `.claude/skills/` dentro de ese proyecto.

### Claude.ai o la app de Claude

Comprime la carpeta `skills/psico-renew` en un `.zip` (sin la carpeta `evals/`) y súbela en la sección de Skills de la configuración. Para que pueda buscar fuentes, activa la búsqueda web.

## Uso

Se activa sola cuando cuentas que estás estresado, abrumado, con síndrome del impostor o diciéndote cosas como "soy un inútil". También puedes pedirla directamente:

- `psico-renew: no paro de pensar que voy a arruinar la demo de mañana`
- `necesito calmarme, llevo 8 horas con este bug`
- `dame un mini-descanso, trabajo desde casa`

Si lo detecta en medio de otra tarea (por ejemplo, mientras arregla tu código), solo te ofrece la pausa en una línea y sigue con lo que estabas haciendo.

### Mini-descansos desde la terminal

El catálogo de descansos también se puede usar sin Claude:

```bash
python3 skills/psico-renew/scripts/mini_descanso.py --contexto remoto --minutos 5
python3 skills/psico-renew/scripts/mini_descanso.py --tipo social -n 3
```

Opciones: `--contexto oficina|remoto|cualquiera`, `--minutos N`, `--tipo social|movimiento|sentidos|cualquiera`, `-n N`, `--excluir id1,id2`, `--json`. Los descansos sociales tienen el doble de probabilidad de salir.

## Estructura

```
.claude-plugin/          Manifiestos del plugin y del marketplace
skills/psico-renew/
├── SKILL.md             Instrucciones de la skill
├── references/
│   ├── crisis.md        Protocolo de crisis y líneas de ayuda verificadas
│   ├── fuentes-confiables.md  Qué fuentes usar, cuáles evitar, consultas de ejemplo
│   └── banco-preguntas.md     Preguntas de respaldo con su fuente, por si no hay búsqueda web
├── assets/mini_descansos.json Catálogo de mini-descansos
├── scripts/mini_descanso.py   Sorteo de mini-descansos (solo biblioteca estándar)
└── evals/               Casos de prueba (formato de `claude plugin eval`)
```

## Pruebas

Los casos de `skills/psico-renew/evals/` comparan la skill contra Claude sin ella: preguntas con fuente, mini-descanso en remoto, protocolo de crisis y oferta discreta en medio de una tarea de código. Con Claude Code 2.1.269 o posterior:

```bash
cd skills/psico-renew
claude plugin eval . --allow-tools Write,Edit,Bash,WebSearch,WebFetch --scaffold
```

Son ejecuciones reales del modelo y consumen uso.

## Por qué así

- Las preguntas salen de técnicas con evidencia (TCC, ACT, autocompasión) y se citan para que puedas confiar en ellas y profundizar.
- Los micro-descansos de 10 minutos o menos aumentan la energía y reducen la fatiga ([Albulescu et al., 2022, *PLOS ONE*](https://doi.org/10.1371/journal.pone.0272460)).
- La conexión social es uno de los factores de bienestar más sólidos que se conocen, así que dos de cada tres descansos implican hablar con alguien.
