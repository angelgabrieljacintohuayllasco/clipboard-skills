---
name: env-doctor
description: "Project won't start, build or install for environmental reasons: runtime versions, deps, env vars, ports, DB connection. \"no arranca\", \"no compila\", \"works on my machine\", fails only in CI."
---

# Env-Doctor — por qué no arranca

## Overview

Un proyecto que no arranca suele tener **más de una causa**, y la primera que encuentras casi nunca es la única. Por eso este diagnóstico recorre todas las capas antes de concluir: parar en el primer hallazgo genera el ciclo "arregla uno, aparece otro" que consume tardes enteras.

## Cuándo usar

- Clon nuevo que no levanta; build que falla; "en mi máquina sí funciona".
- Después de actualizar dependencias, cambiar de máquina o de sistema operativo.
- Falla solo en CI o solo en el servidor.
- Un servicio dependiente (base de datos, caché, cola) no responde.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Arranca pero se comporta mal | `fixer` |
| Falla al publicar en producción | `deploy` |
| Nadie sabe si está corriendo | `observability` |

## Regla de hierro: diagnosticar todas las capas antes de tocar nada

```
NO MODIFIQUES EL ENTORNO HASTA TERMINAR EL DIAGNOSTICO COMPLETO. RECOLECTA TODOS LOS PROBLEMAS, LUEGO PROPON LOS ARREGLOS EN ORDEN.
```

Y nunca imprimas valores de secretos: reporta "definido / sin definir", jamás el contenido.

## Orden de diagnóstico

1. **Versión del runtime.** Lee la versión requerida del manifiesto del proyecto (campo de motores, requisitos de versión, archivos de versión de herramientas) y compárala con la instalada. Las diferencias de versión mayor explican la mayoría de los fallos misteriosos.
2. **Dependencias instaladas.** ¿Existe la carpeta de dependencias? ¿El archivo de bloqueo coincide con lo instalado? ¿Hay conflictos o paquetes faltantes? ¿El entorno virtual está activo? Instalación desde cero limpia si hay dudas (y verificar que el archivo de bloqueo está en el repo).
3. **Variables de entorno.** Busca en el código todas las lecturas de variables y compáralas con el archivo de ejemplo y con lo que hay definido. Lista las referenciadas y no definidas, con el archivo:línea donde se usan.
4. **Puertos.** Localiza los puertos configurados y verifica si están ocupados por otro proceso. Un servidor zombi de una sesión anterior es una causa clásica.
5. **Servicios externos.** Base de datos, caché, cola, APIs: ¿el host responde? ¿el puerto está abierto? ¿las credenciales son de este entorno? Probar la conectividad sin exponer credenciales.
6. **Archivos de configuración.** ¿Existen y son válidos? Configuración, certificados, archivos de datos. Validar el formato, no solo la existencia.
7. **Sistema y herramientas.** Permisos, rutas con espacios o caracteres no latinos, herramientas de compilación nativas ausentes, límites de longitud de ruta, diferencias de mayúsculas entre sistemas de archivos, finales de línea.
8. **Diferencias con el entorno que sí funciona.** Si funciona en otra máquina o en CI: comparar versiones, variables y sistema operativo. La diferencia está ahí, no en el código.

## Salida

Una línea por capa (`ok` o `problema → arreglo`), y al final la lista priorizada, lo más bloqueante primero:

```
FALLA  Runtime: instalado 18, el proyecto requiere >=20 (manifiesto)
       → instalar la versión 20 con el gestor de versiones del proyecto
FALLA  Variable DATABASE_URL sin definir (usada en src/db.ts:12)
       → copiar el archivo de ejemplo a .env y completarla
OK     Puerto 3000 libre
OK     Dependencias sincronizadas con el archivo de bloqueo
AVISO  El archivo de ejemplo tiene 3 variables que el código ya no usa
```

## Reglas

- Diagnostica todas las capas antes de concluir: los fallos de arranque suelen tener varias causas.
- Nunca imprimas valores secretos: solo "definido / sin definir".
- Da el comando exacto para el sistema operativo detectado.
- No modifiques el entorno sin permiso: primero diagnóstico, luego oferta de arreglo.
- Si el problema era de entorno y no del código, **deja constancia**: agrega al `AGENTS.md` o al `gotchas.md` la versión requerida, la variable faltante o la dependencia del sistema. Un diagnóstico que no se documenta se repite con la próxima persona.
- Si el proyecto no tiene archivo de ejemplo de variables ni instrucciones de arranque, ese es un hallazgo en sí mismo: proponer crearlos.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Borro las dependencias y reinstalo, seguro se arregla" | A veces funciona y nunca sabes por qué, así que vuelve a pasar. Diagnostica primero. |
| "Actualizo todo a la última versión" | Cambias un problema conocido por varios desconocidos. Ajusta a la versión que el proyecto declara. |
| "En mi máquina funciona" | Es el dato más valioso del diagnóstico: compara las dos máquinas y la diferencia es la causa. |
| "Instalo la dependencia que falta y listo" | Si falta, el manifiesto o el archivo de bloqueo están mal. Arregla la causa, no el síntoma local. |
