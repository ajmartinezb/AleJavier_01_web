# Pauta del libro de Física PAES

El libro de Física sigue **la misma pauta que el de Biología** (`biologia/pauta.md`): un archivo por
sección, redacción propia, fuentes registradas, recuadros `nota`/`tip`/`ejemplo`, figuras propias,
evaluación formativa en HTML, `preguntas.json` con 3 ítems por título y validación con `--revisar`.
Aquí solo se anotan las diferencias.

## Rutas y comandos

- Capítulos en `fisica/capitulos/capNN-slug/`. El HTML publicado (`fisica/sitio/`) no se edita a mano:
  ```bash
  python herramientas/construir.py fisica            # generar
  python herramientas/construir.py fisica --revisar  # generar y revisar las preguntas IA
  ```
- `fisica/temario.md` es el temario DEMRE 2027 de Física con el control de cobertura y
  `fisica/progreso.md` el estado de cada capítulo. Ambos se actualizan al cerrar la sesión.

## Particularidades de Física

1. **Magnitudes con unidades del SI** y notación científica con `×10<sup>n</sup>`. Se escriben
   con espacio entre número y unidad (`340 m/s`, `2,5 Hz`) y coma decimal.
2. **Fórmulas** en texto con `<sub>`/`<sup>` y símbolos griegos (λ, Δ, θ). Toda fórmula se
   presenta con el significado y la unidad de cada símbolo.
3. **Cada sección con cálculos** lleva al menos un ejemplo resuelto dentro de la teoría, con
   el procedimiento completo (datos → fórmula → reemplazo → resultado con unidad).
4. **Gráficos**: la PAES usa mucho gráficos (posición–tiempo, perfil de una onda, espectros).
   Se dibujan como SVG propios, con ejes rotulados y unidades.
5. **Distractores de cálculo**: en los ítems numéricos, los distractores salen de errores
   reales (invertir la fórmula, confundir período con frecuencia, olvidar convertir unidades).
6. **Temario 2027**: el área Ondas se centra en las **ondas electromagnéticas**. Lo que se
   explica con ondas mecánicas (cuerdas, resortes, agua, sonido) se usa como modelo para
   entender las electromagnéticas y se dice explícitamente.
