---
name: constitution
description: "Set a project's non-negotiable rules and measurable quality thresholds (coverage, complexity, size, security). \"define las reglas del proyecto\", new repo without definition of done."
---

# Constitution — las restricciones que reemplazan a leer cada línea

## Overview

La práctica que hoy sostiene el desarrollo asistido por IA a escala: **el humano deja de auditar línea por línea y pasa a fijar restricciones extremas y medir**. Robert C. Martin lo resumió así — no revisa el código que escriben sus agentes; mide cobertura de pruebas, estructura de dependencias, complejidad ciclomática, tamaño de módulos y mutación, e infiere la calidad de esas métricas.

La contraparte (Grady Booch) también es cierta: las métricas no ven una vulnerabilidad lógica ni un permiso mal puesto. Por eso esta skill define **dos capas**: lo que la máquina verifica siempre, y la lista corta de diffs donde un humano sigue siendo obligatorio.

Una constitución es un archivo. Si no es un archivo que se puede ejecutar y verificar, es una charla.

## Cuándo usar

- Repo nuevo: antes de la primera línea de producción.
- Repo existente sin definición medible de "listo".
- Cambia el perfil de riesgo (el prototipo ahora tiene usuarios reales, entra dinero, entran datos personales).
- Un gate se volvió ruido y hay que recalibrar umbrales (con evidencia, no por fastidio).

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Correr las métricas y decidir si pasa | `quality-gate` |
| Decidir qué probar y cómo | `test-strategy` |
| Cómo se escribe el código (nombres, funciones, smells) | `code-standard` |
| Elegir stack o estructura de módulos | `architecture` |

## Regla de hierro: umbral sin comando es decoración

```
CADA LIMITE DE LA CONSTITUCION VIVE JUNTO AL COMANDO EXACTO QUE LO VERIFICA Y AL VALOR MEDIDO HOY.
```

"Mantener baja la complejidad" no es una restricción. `npx eslint . --rule 'complexity: [error, 10]'` sí lo es. Si no existe herramienta para medir algo en este stack, o se instala, o el límite se baja a una convención de `code-standard` y se declara como no verificable automáticamente.

## Perfiles y umbrales por defecto

Elige perfil (lo acuerda `intake`) y ajusta con motivo escrito. Los valores vienen de defaults de industria: Sonar way (cobertura 80% en código nuevo, duplicación ≤3%, complejidad cognitiva ≤15 por función), McCabe/NIST (complejidad ciclomática ≤10 por función, hasta 15 con justificación escrita), y práctica de mutación (75-85% es sólido; 100% es humo por mutantes equivalentes).

| Restricción | P1 Prototipo | P2 Estándar | P3 Crítico |
|---|---|---|---|
| Cobertura de líneas **en código nuevo** | — | ≥ 80% | ≥ 90% en núcleo de dominio |
| Puntaje de mutación (núcleo) | — | ≥ 60% | ≥ 80% |
| Complejidad ciclomática por función | ≤ 15 | ≤ 10 | ≤ 10 (sin excepciones) |
| Complejidad cognitiva por función | ≤ 25 | ≤ 15 | ≤ 15 |
| Longitud de función | ≤ 80 LOC | ≤ 50 LOC | ≤ 40 LOC |
| Tamaño de archivo/módulo | ≤ 600 LOC | ≤ 400 LOC | ≤ 300 LOC |
| Parámetros por función | ≤ 5 | ≤ 4 | ≤ 3 |
| Anidamiento | ≤ 4 | ≤ 3 | ≤ 3 |
| Duplicación | — | ≤ 3% | ≤ 3% |
| Ciclos de dependencias | evitar | **0** | **0** |
| Dependencias nuevas | libre | justificadas + auditadas | justificadas + auditadas + fijadas por versión |
| Paquetes: existencia + integridad | — | lockfile presente | lockfile + hash pinning; existencia verificada (anti-slopsquatting) |
| Secretos en el repo | 0 | 0 | 0 + escaneo en CI |
| Vulnerabilidades altas/críticas conocidas | declaradas | 0 | 0 + SBOM |
| Errores de tipado / lint | — | 0 | 0 |
| E2E de caminos críticos | — | 3-5 flujos | todos los flujos de dinero/datos |
| Revisión humana del diff | no | en zonas sensibles | obligatoria en todo el dominio |
| Rollback | no aplica | documentado | **ensayado** |

**Regla del trinquete (ratchet):** los umbrales nunca bajan. Si hoy la cobertura real es 34%, el gate se fija en 34% y solo sube. El código nuevo cumple el objetivo completo desde el día uno (clean as you code); el legado se paga con `tech-debt`, no se amnistía.

## Las dos capas

**Capa 1 — máquina (siempre, sin excepción):** formato, lint, tipos, tests, cobertura de código nuevo, mutación del núcleo, complejidad, tamaño, duplicación, ciclos de dependencias, auditoría de dependencias, **verificación de existencia de cada paquete nuevo (anti-slopsquatting) + lockfile íntegro con versiones fijadas**, escaneo de secretos, build reproducible.

> **Slopsquatting** (CSA 2026): los modelos alucinan nombres de paquetes inexistentes (~5% comercial, ~20% open source) y hay atacantes que registran esos nombres. Todo paquete que proponga un agente se **verifica que exista y sea el correcto** antes de instalarlo; nunca instalar sin allowlist o revisión. Para apps agénticas/con IA, añadir a la constitución los límites de **agencia** (OWASP LLM 2025 "Excessive Agency"): mínimo de herramientas, mínimo de permisos, y aprobación humana para acciones de alto impacto. Ver la skill `ai-security`.

**Capa 2 — humano obligatorio (aunque la capa 1 esté verde):** un diff que toque cualquiera de esto se lee línea por línea, y lo lee alguien que no lo escribió:

- Autenticación, autorización, sesiones, permisos y reglas multi-tenant.
- Dinero: cobros, precios, saldos, descuentos, reembolsos.
- Datos personales, borrado, retención, exportación.
- Migraciones destructivas e irreversibles.
- Criptografía, secretos, tokens, webhooks entrantes.
- Cualquier cosa que envíe mensajes o correos a terceros a escala.

El resto del código lo verifica la capa 1. Ese es el trato: **el humano gana tiempo donde la máquina alcanza y lo gasta donde la máquina es ciega.**

## Estructura del archivo

`docs/project/constitution.md` (plantilla completa en `templates/constitution.md`):

```markdown
# Constitución — <proyecto>
version: 1 · perfil: P2 · actualizado: YYYY-MM-DD

## Principios (máximo 7, cada uno verificable u observable)
1. El código nuevo entra verde o no entra.
2. Todo criterio de aceptación tiene una prueba automática.
3. Ninguna función supera los límites de la tabla.
4. Dependencia nueva = decisión justificada, no reflejo.
5. Nada de secretos en el repo, nunca.
...

## Límites verificables
| Métrica | Límite | Comando | Valor hoy |
|---|---|---|---|
| Cobertura código nuevo | ≥80% | `npm run test:cov` | 0% |
| Complejidad | ≤10 | `npx eslint . --max-warnings 0` | ok |
...

## Comando único del gate
`npm run gate`  → corre todo lo anterior y falla con código ≠ 0

## Revisión humana obligatoria
<rutas/módulos sensibles de ESTE proyecto>

## Excepciones vigentes
| Regla | Dónde | Motivo | Vence |
|---|---|---|---|
```

Toda excepción lleva **fecha de vencimiento**. Sin fecha, no es excepción: es una regla que se abandonó.

## Cómo instalar los gates (día 1, no al final)

1. Un solo comando de entrada: `npm run gate` / `make gate` / `just gate`. Quien pide el proyecto tiene que poder verificarlo sin saber el stack.
2. Ese comando encadena: formato → lint → tipos → tests + cobertura → complejidad/tamaño → duplicación → ciclos de dependencias → auditoría de deps → escaneo de secretos.
3. Mismo comando en CI, en el hook de pre-push y en el cierre de cada tarea. Un gate que solo vive en CI se descubre tarde; uno que solo vive local no protege la rama.
4. Mutación: pesada. Corre sobre archivos cambiados en el gate normal y completa de noche o semanal.
5. Escribe en `AGENTS.md` de la raíz: cómo construir, cómo probar, cómo correr el gate, y el enlace a la constitución. Es lo primero que lee cualquier agente y cualquier persona nueva.

Herramientas por ecosistema (elegir las que existan; no inventar):

| Ecosistema | Lint/complejidad | Tests + cobertura | Mutación | Dependencias | Secretos |
|---|---|---|---|---|---|
| JS/TS | eslint (`complexity`, `max-lines`, `max-params`), tsc | vitest/jest `--coverage` | Stryker | `npm audit`, madge (ciclos), knip | gitleaks |
| Python | ruff, radon/xenon, mypy | pytest + coverage.py | mutmut/cosmic-ray | pip-audit, import-linter | gitleaks |
| PHP | phpstan, phpcs | phpunit + coverage | infection | composer audit | gitleaks |
| Rust | clippy | cargo test + tarpaulin | cargo-mutants | cargo audit/deny | gitleaks |
| Go | golangci-lint, gocyclo | go test -cover | go-mutesting | govulncheck | gitleaks |
| Java/Kotlin | detekt/checkstyle | JUnit + JaCoCo | PIT | OWASP dep-check | gitleaks |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Los umbrales frenan la velocidad" | Frenan la velocidad de meter deuda. Sin gate, la IA genera más código del que nadie puede revisar, y lo que no se revisa se paga en producción. |
| "100% de cobertura o nada" | La cobertura mide líneas ejecutadas, no aserciones útiles. Por eso existe el puntaje de mutación. 80% con mutación decente vale más que 100% con tests que no afirman nada. |
| "Este proyecto es especial, los límites no aplican" | Entonces escribe la excepción con módulo, motivo y fecha de vencimiento. Excepción escrita: legítima. Excepción hablada: deuda. |
| "Lo mido al final" | Al final el costo de cumplir es el de reescribir. Los gates son baratos solo si existen desde el primer commit. |
| "Las métricas están verdes, entonces el código está bien" | Verde significa que no se detectó lo detectable. Por eso existe la capa 2 (revisión humana en zonas sensibles). |
| "Es un proyecto personal, sin gates" | Perfil P1: build + lint + un smoke test. Son 10 minutos y evitan que el prototipo llegue a producción sin que nadie lo decida. |

## Formato de salida

- `docs/project/constitution.md` escrito o actualizado (versión + fecha).
- Tabla de límites con **comando** y **valor medido hoy** (no estimado: medido).
- Comando único del gate creado y ejecutado una vez, con su salida real.
- Lista de rutas con revisión humana obligatoria.
- Excepciones vigentes con fecha de vencimiento.
- `AGENTS.md` actualizado.
