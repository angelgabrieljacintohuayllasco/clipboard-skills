# AGENTS.md — <PROYECTO>

Contexto operativo para cualquier agente o persona que toque este repo. Léelo antes de escribir código.

## Qué es esto

<una frase: qué hace el sistema y para quién>

- Especificación: `docs/project/spec.md`
- Restricciones y umbrales: `docs/project/constitution.md`
- Arquitectura y decisiones: `docs/project/architecture.md`
- Estado actual y zonas rojas: `docs/project/state.md`
- Bugs resueltos (síntoma → causa raíz → fix): `docs/project/bugs.md`
- Trampas no obvias: `docs/project/gotchas.md`

## Comandos

```bash
<instalar>      # ej. npm ci
<desarrollo>    # ej. npm run dev
<tests>         # ej. npm test
<gate>          # ej. npm run gate   ← obligatorio antes de decir "listo"
<build>         # ej. npm run build
```

## Reglas de este repo

1. Nada entra sin pasar `<gate>`. Si el gate falla, el trabajo no está terminado.
2. Estilo y límites: ver la constitución. No se negocian en el chat.
3. Un cambio = un propósito (no mezclar fix + refactor + feature).
4. Secretos en `.env` (nunca commiteado). `.env.example` sí se commitea, con claves vacías.
5. Antes de tocar `<zona sensible>`, leer `docs/project/gotchas.md`.

## Zonas rojas (no tocar sin leer primero)

| Ruta | Por qué | Dónde está documentado |
|---|---|---|
| | | |

## Al terminar una sesión con avance real

Actualizar `docs/project/state.md` (y `bugs.md` / `gotchas.md` si aplica) con lo aprendido: qué se hizo, qué falta, qué no hay que volver a intentar.
