---
name: ai-security
description: Usar cuando se construye o revisa algo que usa IA/LLM o un agente — chatbots, agentes con herramientas, RAG, automatizaciones con IA, features que meten input no confiable en un prompt, o cuando se instala/usa código generado por IA. También "es seguro mi agente/bot de IA", "revisa la seguridad de la IA", "parámetros de seguridad para agentes". Aplica los riesgos específicos de IA (OWASP LLM Top 10 2025 + OWASP Agentic Top 10) con controles concretos: mínimo privilegio y acotado de herramientas, defensa de prompt injection, niveles de aprobación humana por riesgo, manejo de secretos, sandbox, y anti-slopsquatting en dependencias. NO reemplaza a `app-security` (seguridad general de la app) — es su complemento para la parte de IA/agentes.
---

# AI-security — seguridad de sistemas con IA y de código generado por IA

## Overview

La seguridad clásica (`app-security`) no cubre lo que rompe en un sistema con IA: el modelo mezcla instrucciones y datos en el mismo canal, un agente con herramientas puede hacer daño real, y el código que genera trae riesgos nuevos (paquetes alucinados). Esta skill añade la capa específica de IA sobre la baseline normal.

Marco de referencia: **OWASP Top 10 for LLM Applications 2025** y **OWASP Top 10 for Agentic Applications** (Black Hat EU 2025), más el AI Agent Security Cheat Sheet de OWASP y la investigación de slopsquatting (Cloud Security Alliance, 2026).

Regla mental: *no se puede evitar perfectamente que un prompt sea inyectado; se diseña para que, si lo es, el daño sea mínimo.* La defensa es **limitar el radio de daño**, no confiar en detectar cada ataque.

## Los riesgos que sí o sí se revisan

**OWASP LLM Top 10 2025 (los de mayor incidencia):**
1. **Prompt Injection (#1)** — instrucciones y datos van por el mismo canal; un input puede hacerse pasar por instrucción. Todo lo que llega de fuera (mensajes, documentos recuperados, respuestas de API, correos, páginas) es **no confiable**.
2. **Excessive Agency** — tres causas: demasiada **funcionalidad** (herramientas más allá de la tarea), demasiados **permisos** (más privilegio del necesario), demasiada **autonomía** (acciones de alto impacto sin humano).
3. **Insecure Output Handling** — usar la salida del modelo sin validar (ejecutarla, meterla en SQL/HTML/shell).
4. **Sensitive Information Disclosure** — el modelo filtra secretos o datos personales que tenía en contexto.
5. **Supply chain** — incluye paquetes alucinados (ver slopsquatting abajo).

**OWASP Agentic Top 10 (si hay agente con herramientas/memoria):** goal hijacking, tool misuse, **memory/context poisoning** (datos envenenados que quedan en la memoria del agente y sesgan decisiones futuras).

## Controles concretos (parámetros)

### 1. Mínimo privilegio + acotar herramientas
- Dar al agente **solo** las herramientas que la tarea necesita, con el **menor permiso** posible.
- Separar razonamiento de ejecución: nada de shell abierto, credenciales cloud crudas o `kubectl` sin restringir; en su lugar, un set corto de operaciones acotadas.
- Acotar rutas y comandos: `allowed_paths`, `allowed_commands` (allowlist, nunca `*`), `blocked_patterns: *.env, *.key, *secret*`.

### 2. Defensa de prompt injection
- Tratar **todo input externo como no confiable**; delimitarlo con fronteras claras entre instrucciones y datos.
- Para contenido no confiable pesado, una llamada LLM aparte que lo **valide/resuma** antes de meterlo al contexto principal.
- No dar por buena la salida del modelo: **validar antes de ejecutar/mostrar** (schema/allowlist de herramientas).

### 3. Aprobación humana por nivel de riesgo (HITL)
Clasificar cada acción y fijar el umbral de auto-aprobación:
| Nivel | Ejemplos | Regla |
|---|---|---|
| LOW | leer | auto |
| MEDIUM | escribir, llamar API | auto o log |
| HIGH | financiero, borrado | **aprobación humana** |
| CRITICAL | irreversible, cambio de privilegios, envío masivo | **aprobación + step-up auth** |
Aprobar los **parámetros exactos**, no solo el nombre de la herramienta.

### 4. Secretos y datos
- Nunca poner claves/tokens/passwords en el prompt ni en el código; usar variables de entorno / gestor de secretos.
- Redactar secretos en logs (`password`, `api_key`, `token`, `secret`). Clasificar datos antes de meterlos al contexto.
- Fugas: vigilar salidas grandes hacia webhooks o patrones de exfiltración.

### 5. Sandbox y límites de recurso
- Ejecutar código del agente en sandbox aislado, sin red y con privilegios mínimos por defecto.
- Topes: llamadas por minuto, coste por sesión (evita "denial-of-wallet"), profundidad de recursión, largo de cadena de herramientas, reintentos.

### 6. Anti-slopsquatting (dependencias que propone la IA)
Los modelos alucinan nombres de paquetes inexistentes (**~5% comercial, ~20% open source**, CSA 2026) y hay atacantes que los registran (caso `react-code shift`: 237 repos). Los agentes eliminan el checkpoint humano que antes atrapaba esto.
- **Verificar que cada paquete nuevo exista de verdad** y sea el nombre correcto (registro oficial), antes de instalar.
- **Lockfile + pinning por hash**; prohibido instalar sin allowlist o revisión humana.
- Enforce en CI/CD.

### 7. Auditoría y detección de anomalías
- Loggear toda llamada a herramienta (parámetros, tiempo, estado) con traza inmutable.
- Umbrales de alarma: llamadas/min excesivas, fallos repetidos, intentos de inyección, coste por sesión sobre el tope.

## Proceso

1. Identificar la superficie de IA: ¿hay LLM? ¿agente con herramientas? ¿memoria? ¿entra input externo al prompt? ¿se instala código/paquetes que propuso IA?
2. Correr primero la baseline normal (`app-security` por tipo de app).
3. Aplicar los controles 1-7 según lo que aplique.
4. Para diffs de código agéntico, cruzar con `diff-review` (sección de código IA).
5. Reportar por riesgo: qué está cubierto, qué falta, y el control concreto que cierra cada hueco.

## Anti-patrones prohibidos

- Confiar en "detectar" prompt injection en vez de limitar el daño.
- Dar al agente todas las herramientas/permisos "por comodidad".
- Ejecutar la salida del modelo sin validar.
- Acciones de alto impacto sin aprobación humana.
- Instalar un paquete que propuso la IA sin verificar que exista.
- Secretos en el prompt o en logs.
- Tratar el contenido recuperado (RAG, web, correo) como confiable.

## Relación

- `app-security` — baseline general por tipo de app (esta es la capa IA encima).
- `constitution` / `quality-gate` — umbrales y gate (incluyen existencia de paquetes + lockfile).
- `diff-review` — lectura humana de diffs de código agéntico.
- `agentic-coding` — cómo trabaja el agente; esta skill es su lado de seguridad.
