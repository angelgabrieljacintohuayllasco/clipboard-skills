---
name: quality-gate
description: Use before calling any work done, delivering to a client, merging, or deploying — "¿está listo?", "revisa la calidad", "ya terminaste?", "verify this", "run the checks", "is this production ready". Runs the project's measurable gate (format, lint, types, tests, coverage on new code, mutation, complexity, module size, duplication, dependency cycles, vulnerabilities, secrets), reports real numbers vs thresholds, and BLOCKS delivery when something fails. Nunca declara "listo" sin salida de comandos reales. NO define los umbrales (constitution) ni arregla bugs (fixer).
---

# Quality-Gate — "listo" es un código de salida, no una sensación

## Overview

El momento más peligroso de una sesión con IA es cuando dice "listo, ya funciona". Esta skill convierte esa frase en algo verificable: **un comando corre, produce números, y esos números se comparan contra la constitución del proyecto.**

Si la salida no está pegada en el reporte, no se corrió. Decir "los tests pasan" sin mostrar la salida es la mentira más común del desarrollo asistido por IA — y casi siempre es involuntaria: el modelo infiere el resultado en lugar de observarlo.

## Cuándo usar

- Antes de decir "terminado" o entregar a alguien.
- Antes de merge, tag, release o deploy.
- Al recibir código de otro agente o de otra sesión.
- Periódicamente en un proyecto vivo (el trinquete se verifica, no se supone).

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| No existen umbrales todavía | `constitution` |
| No hay tests que correr | `test-strategy` |
| El gate falla y hay que arreglarlo | `fixer` (bug) / `refactor` (estructura) |
| Deuda acumulada demasiado grande para un gate | `tech-debt` |

## Regla de hierro: sin salida pegada, no pasó

```
CADA AFIRMACION DE CALIDAD VIENE CON: COMANDO EJECUTADO + SALIDA REAL + NUMERO vs UMBRAL.
```

Prohibido: "todo verde", "los tests pasan", "no hay errores de tipos", "cobertura ~80%", si no se ejecutó en esta sesión y no se está mostrando la evidencia. Si un comando no existe o no se puede ejecutar, se reporta como **NO VERIFICADO**, no como aprobado.

## Proceso

### 1. Localiza el gate

Busca en este orden: `docs/project/constitution.md` → `AGENTS.md` → scripts del manifiesto (`package.json`, `Makefile`, `justfile`, `pyproject.toml`) → configuración de CI. Si no hay gate: **no continúes verificando a ciegas**; ejecuta `constitution` primero y dilo.

### 2. Ejecuta, en orden barato → caro

| Orden | Capa | Por qué antes |
|---|---|---|
| 1 | Formato + lint + tipos | Segundos. Atrapa la mitad de los errores triviales. |
| 2 | Tests unitarios + cobertura de código nuevo | Minutos. El corazón del gate. |
| 3 | Complejidad, tamaño, parámetros, duplicación | Rápido. Es lo que evita el monolito dentro de 6 meses. |
| 4 | Ciclos de dependencias + dependencias sin usar | Rápido. Estructura sana = cambios baratos. |
| 5 | Auditoría de vulnerabilidades + escaneo de secretos | Rápido. Nunca opcional. |
| 6 | E2E de caminos críticos | Lento. Solo los flujos del spec. |
| 7 | Mutación (núcleo o archivos cambiados) | Muy lento. Incremental aquí, completo de noche. |

Ejecuta **todo** aunque algo falle temprano. Un reporte con un solo fallo obliga a repetir el ciclo entero; uno con la lista completa se arregla de una pasada.

### 3. Compara contra umbrales y decide

| Resultado | Acción |
|---|---|
| Todo dentro de umbral | **PASA** — se puede entregar/desplegar |
| Falla algo de la capa 1-5 | **BLOQUEA** — no se entrega. Reportar y arreglar. |
| Cobertura o mutación baja respecto a la medición anterior | **BLOQUEA** (trinquete roto) |
| Herramienta ausente | **NO VERIFICADO** — decirlo explícitamente, nunca contarlo como verde |
| Falla un E2E crítico | **BLOQUEA**, sin importar lo demás |

### 4. Revisión humana de capa 2

Si el diff toca zonas sensibles declaradas en la constitución (auth, dinero, datos personales, migraciones, criptografía, envíos masivos), el gate verde **no alcanza**: marca el diff como pendiente de lectura humana y di exactamente qué archivos y por qué. Las métricas no detectan un `if (user.role)` invertido ni un endpoint sin verificación de propiedad.

### 5. Reporte

```
GATE: <PASA | BLOQUEA> — <proyecto> @ <commit/rama>

| Chequeo        | Comando                  | Resultado | Umbral | Estado |
|----------------|--------------------------|-----------|--------|--------|
| Tipos          | tsc --noEmit             | 0 errores | 0      | OK     |
| Tests          | vitest run               | 84/84     | todos  | OK     |
| Cobertura nueva| vitest --coverage        | 71%       | ≥80%   | FALLA  |
| Complejidad    | eslint                   | máx 14    | ≤10    | FALLA  |
| Secretos       | gitleaks detect          | 0         | 0      | OK     |
| Mutación       | —                        | —         | ≥60%   | NO VERIFICADO |

BLOQUEA por: cobertura de código nuevo, complejidad en src/orders/calc.ts:88
Revisión humana pendiente: src/auth/session.ts (zona sensible)
Siguiente paso: tests para calc.ts + extraer la rama de descuentos.
```

## Trampas del propio gate

| Trampa | Cómo se ve | Qué hacer |
|---|---|---|
| Tests que no afirman nada | Cobertura alta, mutación baja | Subir mutación en el núcleo; borrar tests sin aserciones |
| Cobertura global en vez de código nuevo | 78% estable eternamente | Medir sobre el diff (clean as you code) |
| Tests que se saltan solos | `skip`, `only`, `xit` olvidados | Fallar el gate si existen marcas de salto sin ticket |
| Mocks de todo | Verde en CI, roto en producción | Al menos un test de integración real por camino crítico |
| Umbral bajado para pasar | Commit que toca el config del gate | Cambiar un umbral requiere entrada en el historial de la constitución |
| Gate lento que nadie corre | "lo corro después" | Partir: rápido en pre-push, completo en CI, mutación nocturna |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Funciona, lo probé a mano" | Probaste una vez, un camino, hoy. El gate prueba todos los caminos cada vez, para siempre. |
| "Los tests fallan pero es del entorno" | Entonces el gate está roto y esa es la falla número uno a arreglar. Un gate en el que no se confía no sirve para nada. |
| "Es poquito código, no hace falta" | El tamaño del diff no predice el tamaño del incidente. |
| "El cliente tiene prisa" | Entregar roto cuesta más tiempo del que ahorra saltarse el gate. Si de verdad hay que entregar con fallas, se entrega **declarando cuáles**. |
| "Subo cobertura escribiendo tests triviales" | Sube el número, no la seguridad. La mutación lo delata en la siguiente corrida. |
| "El lint me molesta, lo desactivo" | Desactivar la regla no elimina el problema: lo esconde y lo hace crecer. |

## Formato de salida

Tabla de chequeos (comando, resultado real, umbral, estado), veredicto **PASA/BLOQUEA**, lista de fallas con archivo:línea, chequeos NO VERIFICADOS, diffs pendientes de revisión humana, y el siguiente paso concreto.
