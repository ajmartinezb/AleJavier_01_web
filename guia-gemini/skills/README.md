# Skills del proyecto Libros PAES

| Skill | Para qué sirve | ¿Imprescindible? |
|---|---|---|
| `libros-paes-ciencias` | El flujo completo de un capítulo: investigar, planificar, escribir, figuras, preguntas por lotes, validar y cerrar. Trae scripts y ejemplos en `assets/` | **Sí**, es la principal |
| `paes-estudio-demre` | La metodología DEMRE para crear preguntas PAES y sus respuestas comentadas: habilidades, tipos de distractores y estructura de la respuesta | **Sí** |
| `pdf-a-html-ia-paes` | El generador del sitio (`construir.py`), los revisores de preguntas y figuras y las reglas de formato (`references/`). Es la misma carpeta `herramientas/` del proyecto | **Sí**, aunque ya viene dentro del proyecto |
| `paes-generador-preguntas` | El «operador» de preguntas por ramo y capítulo. Parte de sus rutas son de otro proyecto (los sitios Moraleja y paes-2027); aquí sirve como referencia de estilo | Opcional |
| `libreto-video-notebooklm` | Libretos para los videos resumen de NotebookLM / Gemini Notebook | Solo para los videos |

Algunas skills mencionan rutas y archivos de otros proyectos. **En este proyecto mandan** `GEMINI.md`,
las pautas de cada libro y `herramientas/references/preguntas-paes.md`.

## Cómo usarlas en Gemini

Gemini no instala skills como Claude, pero las lee igual como instrucciones:

- **Gemini CLI:** ya las encuentra en `guia-gemini/skills/`, porque `GEMINI.md` apunta a ellas. Al
  empezar una sesión, dile por ejemplo: «Lee guia-gemini/skills/libros-paes-ciencias/SKILL.md y
  guia-gemini/skills/paes-estudio-demre/SKILL.md y trabaja siguiendo ese método».
- **Gemini web (Gem):** sube los `SKILL.md` de `libros-paes-ciencias` y `paes-estudio-demre` como
  archivos de **Conocimiento** del Gem, junto con `herramientas/references/preguntas-paes.md`.

## Cómo usarlas en Claude (si vuelves)

En claude.ai: Configuración → Capacidades → Skills → subir skill. Sube un zip por skill; la carpeta
`para-claude/` del paquete ya los trae listos.
