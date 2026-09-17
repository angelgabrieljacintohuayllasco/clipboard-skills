---
name: refactor
description: Use when code works but needs restructuring without changing behaviour — monolithic files (1500+ LOC), duplicated logic, tangled state, "cada cambio rompe otra cosa", "me da miedo tocarlo", extracting modules, splitting a god file, cleaning architecture, preparing ground before a big feature. Behaviour is frozen: same inputs, same outputs, same side effects. NO usar con un bug activo (fixer), sin red de pruebas (test-strategy primero) ni cuando la base no se puede salvar (rebuild).
---

# Refactor — reestructurar sin cambiar comportamiento

## Overview

Reestructura código que FUNCIONA. El comportamiento observable queda congelado: mismas entradas → mismas salidas → mismos efectos. Si el comportamiento cambia, no es refactor: es un bug nuevo introducido por ti, y encima difícil de detectar porque nadie lo estaba buscando.

## Cuándo usar

- Monolito que hay que partir en módulos.
- Lógica duplicada, funciones enormes, estado global enredado.
- "Funciona pero me da miedo tocarlo" / "cada fix rompe otra cosa".
- Preparar el terreno ANTES de una funcionalidad grande.
- Pagar deuda priorizada por `tech-debt`.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Hay un bug activo | `fixer` primero. Nunca mezclar fix con refactor |
| No hay forma de verificar el comportamiento actual | `test-strategy` (caracterización) antes |
| El comportamiento actual también está mal | Eso es rediseño: acuérdalo explícitamente con quien decide |
| La base no se puede salvar | `rebuild`, tras `triage` |
| Estética sin dolor real | No hacer nada. YAGNI también aplica al orden |

## Regla de hierro: red de seguridad ANTES de mover código

```
SIN PRUEBAS DE CARACTERIZACION NO HAY REFACTOR.
```

1. Identifica los comportamientos críticos de lo que vas a mover. Fuentes: criterios de aceptación del spec, `bugs.md` (cada bug arreglado es un caso de regresión real), la tabla "qué no tocar" de `state.md`.
2. Si hay tests: córrelos y guarda el resultado como línea base. Si fallan hoy, ese es el primer problema.
3. Si no hay: escribe pruebas que capturen lo que el sistema **hace hoy** (aunque sea feo — documentan lo que ES, no lo que debería ser).
4. Ten siempre a mano una verificación mínima rápida: compilación, chequeo de sintaxis, validación de configuración, arranque del proyecto.

## Proceso: pasos chicos, verificados

1. **Mapa de dependencias implícitas** antes de extraer. El fallo número uno al sacar código de un monolito es que la función dependía en silencio de variables compartidas, closures o estado global: nada "se ve mal" y aun así rompe. Antes de mover algo, lista cada identificador libre que usa y decide qué recibe por parámetro y qué tomaba del entorno.
2. **Un movimiento por paso**: extraer UNA función o módulo → verificar → confirmar el cambio. Nada de reorganizaciones masivas de carpetas.
3. **Estrangulamiento, no trasplante**: el módulo nuevo convive con el viejo; el viejo lo llama; se migran las llamadas de a una. El monolito muere por partes, no de un golpe.
4. **Respeta las zonas rojas**: si las notas marcan bloques intocables (candados, expresiones de clasificación, controles anti-duplicado), se mueven íntegros o no se mueven. Cada uno existe por un bug real que alguien pagó.
5. **Sin cambios de comportamiento colados**: ni "de paso lo mejoro", ni renombrar campos que otros consumen, ni cambiar mensajes que alguien parsea.
6. **Stop-loss**: si la verificación falla y no la restauras en un paso, vuelve atrás y replanifica. No acumules pasos rotos "que después arreglo".

## Qué mejora un refactor (y qué se mide)

| Antes | Después | Métrica que lo demuestra |
|---|---|---|
| Archivo de 2.000 líneas | 5 módulos con responsabilidad clara | Tamaño máximo de archivo |
| Función de 300 líneas | Funciones con nombre por paso | Longitud y complejidad máximas |
| Lógica repetida en 4 lugares | Una implementación | Porcentaje de duplicación |
| Todo importa todo | Dependencias en una dirección | Ciclos = 0 |
| No se puede probar sin levantar el sistema | Dominio puro testeable | Tiempo del conjunto de pruebas |

Si el refactor no mueve ninguna métrica, probablemente fue mover muebles.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es puro mover código, no necesita pruebas" | Mover código ES el momento exacto donde se pierden dependencias implícitas. |
| "Aprovecho y arreglo este bug que vi" | Anótalo y repórtalo; no lo toques en este cambio. Fix y refactor mezclados = nadie sabe qué rompió qué. |
| "Aprovecho y mejoro este comportamiento" | Cambiar comportamiento es decisión de quien manda, no tuya, y encima invalida tu red de pruebas. |
| "Refactor total de una vez queda más limpio" | Sin verificación intermedia, el monolito te gana. Siempre. |
| "Lo hago yo de memoria, conozco este código" | Tu memoria no incluye los tres lugares que leen esa variable global. |

## Formato de salida

Por cada paso: qué se movió, verificación ejecutada y su resultado. Al final: estructura resultante, métricas antes/después, deuda restante (qué quedó sin migrar y por qué), salida del gate completo y actualización de las notas del proyecto si cambió la arquitectura.
