---
name: ui-bug
description: Use when a frontend problem is visual or interactive — broken layout, overlapping or invisible elements, wrong colors, z-index, responsive/mobile issues, buttons that do nothing, modals that won't open, scroll or focus bugs, "se ve mal", "no se ve", "el botón no hace nada", CSS roto, in React/Vue/Svelte, WordPress/CMS, Tauri/Electron or plain HTML. Diagnose by looking at the real DOM, computed styles and console — never by reading source alone. NO para lógica de negocio sin síntoma visual (fixer).
---

# UI-Bug — se diagnostica mirando, no leyendo

## Overview

Un bug de interfaz se diagnostica **mirando la pantalla real**. El DOM renderizado, los estilos computados y la consola dicen la verdad; el código fuente solo dice la intención. Entre ambos hay una cascada de CSS, un runtime, una caché y a veces un plugin ajeno.

## Cuándo usar

- Maquetación rota, elementos encimados o desaparecidos, responsive mal, estilos que no aplican.
- Interacción muerta: clic que no dispara, modal que no abre, scroll trabado, foco perdido.
- Diferencia entre lo que el código "debería" renderizar y lo que se ve.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Lógica de negocio equivocada sin síntoma visual | `fixer` |
| No hay bug: se quiere mejorar el diseño | `web-app` (checklist de entrega) |
| La página ni carga (500, build roto) | `fixer` / `env-doctor` |
| Va lento pero se ve bien | `performance` |

## Regla de hierro: reproducir en pantalla ANTES de editar

```
SI NO LO VISTE FALLAR EN PANTALLA, NO LO ARREGLES TODAVIA.
```

| Objetivo | Cómo mirar |
|---|---|
| Web local o en línea | Navegador automatizable: captura, árbol de accesibilidad, consola, red, estilos computados |
| Sitio con CMS en producción | Mismo navegador contra el sitio real; revisar consola y red, y con la caché purgada |
| Aplicación de escritorio | Captura de la ventana real de la aplicación |
| Estados hover/foco/arrastre | Provocar el estado y capturar; no deducirlo del CSS |
| Móvil | Emular el ancho **y** recargar (muchas condiciones se evalúan al cargar); si el reporte vino de un teléfono, reproducir ese ancho |

## Proceso

1. **Reproducir** en el mismo viewport y dispositivo del reporte. Captura del estado roto = evidencia base.
2. **Inspeccionar lo real**:
   - Consola: un error de JavaScript anterior mata toda la interactividad posterior sin dejar rastro visual.
   - DOM: ¿el elemento existe? ¿está donde crees?
   - Estilos computados: ¿quién gana la cascada y por qué?
   - Red: ¿cargó el CSS, la fuente, la imagen? ¿404 silencioso?
3. **Clasificar la causa**:
   - (a) CSS/cascada/especificidad
   - (b) apilamiento: `z-index`, contexto de apilamiento, `overflow`
   - (c) maquetación: flex/grid/tamaños/desbordes
   - (d) estado JS: evento no ligado, condición de render, error previo
   - (e) recurso que no cargó
   - (f) caché, plugin o tema de terceros que pisa estilos
4. **Fix mínimo en el código fuente** — nunca "arreglar" con JavaScript inyectado en el navegador; eso solo sirve para diagnosticar.
5. **Verificar**: captura después, en el viewport del reporte **y** en al menos uno más. Ejecutar la interacción real (clic, envío, apertura), no suponerla.
6. **No romper lo de al lado**: revisar una pantalla vecina que use el mismo componente o estilo.

## Trampas frecuentes

| Síntoma | Causa típica no obvia |
|---|---|
| "El botón no hace nada" | Error JS anterior rompió el script; o hay un overlay invisible encima (`pointer-events`, apilamiento) |
| El estilo no aplica | Especificidad u orden de carga; en CMS, caché o el tema pisando con `!important` |
| Bien en escritorio, roto en móvil | Desborde horizontal por un ancho fijo; condición de medios que nunca coincide |
| Elemento desaparecido | Está en el DOM: `overflow: hidden` del padre, altura 0, o detrás de otro |
| Funciona en desarrollo, roto en producción | Recurso 404 por ruta relativa, CSS eliminado por el build, caché del CDN |
| Modal detrás del contenido | Un ancestro con `transform`/`filter` creó un contexto de apilamiento nuevo |
| El foco se pierde o el teclado no llega | Elemento no enfocable usado como botón (`div` con clic) |

## Accesibilidad: el bug que nadie reporta

Mientras estás dentro, verifica lo barato: ¿se puede usar con Tab y Enter? ¿el foco se ve? ¿los controles son elementos reales (`button`, `a`) y no `div` con manejadores? Un control inaccesible no aparece en el reporte del cliente, pero excluye usuarios de verdad.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Por el código, seguro es X" | El código dice la intención. La cascada, el runtime y la caché deciden otra cosa. Mira primero. |
| "Agrego `!important` y listo" | Parche que pudre la cascada para todos los que vengan. Encuentra quién gana y por qué. |
| "Se ve bien en mi viewport" | El reporte vino de otro. Reproduce el suyo. |
| "Lo arreglo con un `setTimeout`" | Esconde una condición de carrera que volverá en un dispositivo más lento. |
| "Es solo CSS, no necesita verificación" | El CSS es global por naturaleza: lo que arreglas aquí rompe allá. Revisa una pantalla vecina. |

## Formato de salida

Captura antes/después, causa raíz clasificada (a-f), archivo:línea del fix, viewports verificados, interacción real ejecutada, y nota en `gotchas.md` si la causa fue una trampa del entorno (caché, tema, plugin).
