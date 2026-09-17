# Constitución — <PROYECTO>

```yaml
version: 1
perfil: P2            # P1 prototipo | P2 estándar | P3 crítico
actualizado: YYYY-MM-DD
gate: "npm run gate"  # comando único que verifica todo
```

## Principios (máximo 7, verificables u observables)

1. El código nuevo entra verde o no entra. El gate manda, no la opinión.
2. Todo criterio de aceptación del spec tiene al menos una prueba automática.
3. Ninguna unidad supera los límites de la tabla; si hay que superarlos, se escribe excepción con fecha.
4. Dependencia nueva = decisión justificada por escrito, no reflejo.
5. Cero secretos en el repo. Cero. Nunca.
6. Un cambio = un propósito. No se mezcla fix con refactor con feature.
7. Lo que no se puede revertir en 5 minutos no se despliega un viernes.

## Límites verificables

| Métrica | Límite | Comando | Valor hoy | Notas |
|---|---|---|---|---|
| Cobertura de líneas (código nuevo) | ≥ 80% | `npm run test:cov` | — | trinquete: nunca baja |
| Puntaje de mutación (núcleo) | ≥ 60% | `npx stryker run` | — | semanal / nocturno |
| Complejidad ciclomática por función | ≤ 10 | `npx eslint .` (regla `complexity`) | — | |
| Complejidad cognitiva por función | ≤ 15 | `npx eslint .` (sonarjs) | — | |
| Longitud de función | ≤ 50 LOC | `npx eslint .` (`max-lines-per-function`) | — | |
| Tamaño de archivo | ≤ 400 LOC | `npx eslint .` (`max-lines`) | — | |
| Parámetros | ≤ 4 | `npx eslint .` (`max-params`) | — | |
| Duplicación | ≤ 3% | `npx jscpd src` | — | |
| Ciclos de dependencias | 0 | `npx madge --circular src` | — | |
| Errores de tipos | 0 | `npx tsc --noEmit` | — | |
| Vulnerabilidades altas/críticas | 0 | `npm audit --audit-level=high` | — | |
| Secretos | 0 | `gitleaks detect` | — | |
| E2E de caminos críticos | 3-5 flujos verdes | `npm run test:e2e` | — | |

## Comando único del gate

```bash
npm run gate
```

Encadena: formato → lint → tipos → tests+cobertura → complejidad/tamaño → duplicación → ciclos → auditoría de dependencias → secretos. Falla con código de salida ≠ 0. Corre en local (pre-push) y en CI con la misma definición.

## Revisión humana obligatoria (la máquina es ciega aquí)

Todo diff que toque estas rutas lo lee una persona que no lo escribió:

- `src/auth/**` — autenticación, sesiones, permisos
- `src/billing/**` — dinero, precios, saldos
- `src/**/migrations/**` — cambios de esquema destructivos
- cualquier archivo que maneje datos personales, tokens o webhooks entrantes

## Lo que este proyecto NO hace (anti-alcance)

- ...

## Excepciones vigentes

| Regla | Dónde | Motivo | Vence |
|---|---|---|---|
| | | | |

Sin fecha de vencimiento no es excepción: es una regla abandonada.

## Historial de cambios de la constitución

| Fecha | Versión | Cambio | Motivo |
|---|---|---|---|
