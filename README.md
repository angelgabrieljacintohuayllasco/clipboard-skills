# dev-skills — ingeniería de software para agentes de IA

36 skills (`SKILL.md`) que hacen que un agente de IA trabaje **como un programador profesional**, no como un generador de código que dice "listo" sin haber verificado nada. Funcionan en Claude Code y en cualquier agente compatible con el formato [Agent Skills](https://agentskills.io) (Codex, OpenCode, Cursor…).

> **EN —** 36 software-engineering skills for coding agents. Spec before code (`intake` → `constitution` → `architecture` → `feature` → `quality-gate` → `deploy`), measurable quality gates that block delivery, human review where metrics are blind, diagnosis-first repair (`triage` → `fixer` / `ui-bug` / `agent-debug` / `refactor` / `rebuild`), security baselines (OWASP Top 10:2025 + OWASP LLM/Agentic), and domain packs for web, API, bots, automation, desktop and mobile. Written in Spanish; descriptions carry English triggers so they fire in either language.

Sirve igual para un programador con veinte años de oficio y para alguien que solo sabe describir lo que quiere: el agente detecta el registro, hace las preguntas que un desarrollador le haría a su cliente, **recomienda las restricciones y métricas de calidad**, construye por rebanadas verificadas y bloquea la entrega cuando los números no dan.

## La idea

Tres prácticas que hoy sostienen el desarrollo asistido por IA:

1. **Restricciones antes que revisión.** Robert C. Martin dejó de leer el código de sus agentes: en su lugar los rodea de restricciones extremas y mide cobertura de pruebas, estructura de dependencias, complejidad ciclomática, tamaño de módulos y pruebas de mutación. De esas métricas infiere la calidad. Este pack convierte eso en un archivo por proyecto (`constitution.md`) y en un comando (`gate`) que falla con código distinto de cero.
2. **La máquina no ve todo.** La crítica de Grady Booch también es cierta: las métricas no detectan un permiso invertido ni una migración destructiva. Por eso hay una segunda capa: lista corta de zonas donde la revisión humana sigue siendo obligatoria (`diff-review`).
3. **Especificación antes que código.** El flujo que reemplazó al "vibe coding": aclarar la intención, marcar los huecos en vez de rellenarlos, planificar bajo restricciones, implementar, verificar contra la especificación (`intake` → `constitution` → `architecture` → `feature` → `quality-gate`).

Y un dato que ordena las prioridades: según el informe de DORA sobre IA, **la IA amplifica el sistema que ya tienes**. Con un pipeline débil, lo que se acelera es la deuda técnica.

## Cómo se usa

```
PEDIDO
  ├─ vago / proyecto nuevo ─────────► intake ──► constitution ──► architecture ──► feature
  ├─ funcionalidad en repo vivo ────► feature
  ├─ algo roto ─────────────────────► triage ──► fixer / ui-bug / agent-debug / refactor / rebuild
  └─ terminado ─────────────────────► quality-gate ──► deploy ──► project-memory
```

Ejemplo real de conversación con `intake` activo:

> **Usuario:** hazme un CRM de WhatsApp
> **Agente:** Siete preguntas y te propongo las reglas de calidad. (1) ¿Canal oficial con API o no oficial? — recomiendo oficial: el no oficial es gratis pero puede costarte el número. (2) ¿Cuántos mensajes al día?… (7) ¿Qué es lo peor que pasa si falla a las 3 AM?
> **Agente:** Perfil recomendado **P2**: cobertura ≥80% en código nuevo, complejidad ≤10, cero secretos en el repo, pruebas de conversación y de duplicados, gate en un comando. Sube ~20% el tiempo y baja mucho el riesgo. ¿Vamos así?

## Instalación

```bash
git clone https://github.com/angelgabrieljacintohuayllasco/dev-skills.git
cd dev-skills
./install.sh                                        # todas, a ~/.claude/skills
./install.sh ~/.claude/skills intake constitution quality-gate   # solo algunas
```

Windows: `.\install.ps1` o `.\install.ps1 -Skills intake,constitution,quality-gate`. Otro agente: pasa su directorio de skills como destino, o copia las carpetas de `skills/` a mano.

Cada carpeta es independiente: puedes llevarte solo `intake`, `constitution` y `quality-gate` y ya tienes el 80% del valor.

## Las skills

### Núcleo del proceso
| Skill | Para qué |
|---|---|
| `dev-router` | Qué skill toca y en qué orden; adapta el registro a quien pide |
| `intake` | La entrevista de descubrimiento: spec, criterios de aceptación, supuestos, perfil de rigor |
| `constitution` | Restricciones y umbrales verificables + instalación de los gates |
| `architecture` | Decisiones caras de revertir, con ADR y límites de dependencias |
| `feature` | Implementar una rebanada vertical bajo la constitución |
| `test-strategy` | Qué probar, en qué nivel, y qué NO probar |
| `quality-gate` | Correr las métricas y **bloquear** la entrega si fallan |
| `code-standard` | Cómo se escribe: nombres, funciones, KISS, YAGNI, DRY, catálogo de olores |
| `diff-review` | Revisión humana por riesgo, donde las métricas son ciegas |
| `tech-debt` | Medir la deuda, cobrar interés visible, plan de pago |
| `project-memory` | Memoria del proyecto en el repo (`AGENTS.md` + `docs/project/`) |
| `agentic-coding` | El método del agente: explorar → planear → ejecutar → verificar con evidencia → revisión adversarial en contexto fresco |

### Transversales
| Skill | Para qué |
|---|---|
| `app-security` | Baseline defensivo (OWASP Top 10:2025) por tipo de aplicación |
| `ai-security` | Lo que usa IA o agentes: OWASP LLM Top 10 + Agentic, prompt injection, agencia excesiva, slopsquatting |
| `data-layer` | Modelado, migraciones seguras, integridad, respaldos probados |
| `observability` | Que el sistema avise antes que el cliente |
| `performance` | Medir, arreglar lo que domina, volver a medir |
| `deploy` | Publicar de forma que se pueda deshacer |

### Dominios
| Skill | Para qué |
|---|---|
| `web-app` | Webs y aplicaciones web: estados, formularios, accesibilidad, responsive, SEO |
| `api-backend` | Contratos, idempotencia, reintentos, webhooks, trabajos en segundo plano |
| `bot-dev` | Bots de mensajería: canal, estado, resiliencia, escalamiento a humano |
| `automation` | Scripts, cron, scraping, ETL: idempotente, reanudable y ruidoso al fallar |
| `desktop-app` | Electron/Tauri/nativo: puente seguro, empaquetado, firma, actualización |
| `mobile-app` | Android/iOS/APK: permisos, sin conexión, firma, requisitos de tienda |

### Diagnóstico y reparación
| Skill | Para qué |
|---|---|
| `triage` | ¿Parchar, reestructurar, depurar el agente o rehacer? Solo lectura |
| `fixer` | Reproducir, causa raíz, fix quirúrgico y prueba de regresión |
| `ui-bug` | Bugs visuales e interactivos: se diagnostican mirando |
| `agent-debug` | Bots de IA que deciden mal: estado, prompt, clasificadores, herramientas, datos |
| `refactor` | Reestructurar con el comportamiento congelado |
| `rebuild` | Rehacer rescatando reglas de negocio y bugs viejos |
| `env-doctor` | Por qué no arranca: todas las capas antes de concluir |

### Apoyo
| Skill | Para qué |
|---|---|
| `consulta` | Responder y documentar sin tocar código |
| `valida-idea` | Veredicto honesto antes de construir, con criterio de muerte |
| `batch` | Un cambio repetitivo en muchos archivos, verificado |
| `readme-generator` | README real, sin comandos inventados |
| `changelog-generator` | Commits → consecuencias para quien usa |

## Perfiles de rigor

| | P1 Prototipo | P2 Estándar | P3 Crítico |
|---|---|---|---|
| Cuándo | demo, uso personal | producto con usuarios | dinero, datos personales, irreversible |
| Cobertura (código nuevo) | — | ≥80% | ≥90% núcleo |
| Mutación | — | ≥60% | ≥80% |
| Complejidad por función | ≤15 | ≤10 | ≤10 |
| Archivo | ≤600 LOC | ≤400 LOC | ≤300 LOC |
| Ciclos de dependencias | evitar | 0 | 0 |
| Revisión humana | no | zonas sensibles | todo el dominio |
| Rollback | — | documentado | ensayado |

Los umbrales salen de referencias públicas: el perfil por defecto de SonarQube (80% de cobertura en código nuevo, ≤3% duplicación, complejidad cognitiva ≤15), el límite clásico de McCabe (complejidad ciclomática ≤10) y la práctica habitual de mutación (75-85% es sólido). Se ajustan por proyecto **con motivo escrito**, y nunca bajan: trinquete.

## Convenciones de archivos

```
AGENTS.md                      # contexto operativo para agentes y personas
docs/project/spec.md           # qué se construye y criterios de aceptación
docs/project/constitution.md   # restricciones y umbrales, con su comando
docs/project/architecture.md   # mapa + decisions/ADR-000X.md
docs/project/state.md          # estado, pendientes, zonas rojas
docs/project/bugs.md           # síntoma → causa raíz → fix → prevención
docs/project/gotchas.md        # trampas no obvias
docs/project/runbook.md        # desplegar, revertir, restaurar
```

Plantillas listas en `skills/constitution/templates/`. Si usas una bóveda de notas (Obsidian u otra), `project-memory` explica cómo espejar estos archivos por proyecto sin duplicar la fuente de verdad.

## Principios que atraviesan todo el pack

- Sin salida de comando pegada, no se ejecutó. "Los tests pasan" no es evidencia.
- Todo hueco se pregunta o se declara como supuesto. Nunca se rellena en silencio.
- Toda pregunta lleva recomendación por defecto: preguntar sin recomendar es trasladar el trabajo.
- Un cambio, un propósito. No se mezcla fix con refactor con feature.
- Los umbrales solo suben.
- Lo que no se documenta se vuelve a pagar.

## Validar

```bash
python scripts/validate_skills.py
```

Comprueba frontmatter (`name`, `description`), nombre = carpeta, límites de longitud y que no haya rutas personales ni correos. Corre en CI en cada push.

## Packs hermanos

- [`agent-modes`](https://github.com/angelgabrieljacintohuayllasco/agent-modes) — modos de trabajo del agente: `extremly` (pensar al extremo), `maraton` (ejecutar sin parar con estado en disco), `investigacion` (fuentes clasificadas), `ver-video`, `mcp-master`, `obsidian-memory`.
- [`marketing-skills`](https://github.com/angelgabrieljacintohuayllasco/marketing-skills) — Meta Ads y TikTok Ads con guardarraíles de dinero.

## Licencia

MIT.

## Fuentes

- Robert C. Martin sobre no revisar el código de sus agentes y medir en su lugar — [tweet](https://x.com/unclebobmartin/status/2044114698451476492), [cobertura del debate](https://startupfortune.com/uncle-bob-martin-says-he-no-longer-reads-ai-generated-code-and-the-developer-world-is-split/)
- GitHub Spec Kit — flujo constitution → specify → clarify → plan → tasks → implement — [repo](https://github.com/github/spec-kit)
- SonarQube, perfil de calidad por defecto y métricas — [documentación](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
- Pruebas de mutación, umbrales prácticos — [guía Stryker](https://qaskills.sh/blog/mutation-testing-stryker-guide-2026)
- DORA, ROI del desarrollo asistido por IA — [informe](https://dora.dev/ai/roi/report/)
- OWASP Top 10:2025 — [listado](https://owasp.org/Top10/2025/)
- AGENTS.md como contexto de repo para agentes — [especificación](https://agentsstandard.com/)
