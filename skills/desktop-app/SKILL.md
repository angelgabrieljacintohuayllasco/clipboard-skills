---
name: desktop-app
description: "Build or ship a desktop app: Electron, Tauri, .NET/WPF, Qt, Python GUI. \"app de escritorio\", \"programa para Windows\", installer, auto-update, signing, tray, offline. Use with ui-design."
---

# Desktop-App — el software que corre en la máquina de otro

## Overview

Una aplicación de escritorio abandona dos comodidades del mundo web: **no puedes arreglarla en caliente** (la versión mala vive en la computadora del usuario hasta que actualice) y **corre con los permisos de esa persona** sobre sus archivos y su red.

Eso cambia las prioridades: compatibilidad hacia atrás, actualización confiable, cuidado extremo con lo que ejecuta contenido remoto, y un instalador que no asuste al antivirus ni al usuario.

## Cuándo usar

- Construir o ampliar una aplicación de escritorio.
- Empaquetado, instalador, firma, auto-actualización.
- Persistencia local, trabajo sin conexión, integración con el sistema.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Se ve mal o un control no responde | `ui-bug` |
| Aplicación web | `web-app` |
| Android/iOS | `mobile-app` |
| No compila / entorno roto | `env-doctor` |

## Diseño visual

Toda pantalla nueva o rediseñada aplica `ui-design` antes de darse por terminada: tokens de tipografía, espaciado y color definidos primero, cero emojis, un solo set de iconos SVG, y verificación con capturas en los tamaños de ventana típicos. Una interfaz que funciona pero parece plantilla generada por IA no está lista.

## Regla de hierro: separar lo que dibuja de lo que tiene poder

```
LA CAPA DE INTERFAZ NUNCA TIENE ACCESO DIRECTO AL SISTEMA. TODO PASA POR UN PUENTE EXPLICITO, CHICO Y VALIDADO.
```

En marcos con motor web (Electron, Tauri y similares): aislamiento de contexto activado, integración directa con el sistema desactivada, aislamiento de procesos activo, y un puente que expone **solo** las operaciones concretas que la interfaz necesita — no un pase libre al sistema de archivos ni a ejecutar comandos. El puente valida cada argumento del lado privilegiado, porque cualquier contenido remoto o dependencia comprometida podría llamarlo.

Y nunca cargar contenido remoto arbitrario en una ventana con privilegios: un dominio de terceros dentro de tu aplicación es un intruso con tus permisos.

## Construcción

### Procesos y responsabilidades
- Un proceso coordina (ventanas, permisos, sistema); los demás dibujan.
- El trabajo pesado **nunca** en el hilo de interfaz: la aplicación que se congela se percibe como rota, aunque esté trabajando.
- Operaciones largas: progreso visible y cancelables.

### Datos locales
- Ubicación correcta por sistema operativo para configuración, datos y caché. Nunca junto al ejecutable (en muchos sistemas no hay permiso de escritura ahí).
- Base local (SQLite u otra) con migraciones versionadas: la versión nueva se instala sobre datos de la versión vieja, siempre.
- **Migración solo hacia adelante y probada**: si el usuario instala la nueva versión y luego vuelve a la anterior, sus datos no deben quedar inutilizables.
- Respaldo automático antes de migrar; el usuario debe poder exportar sus datos.
- Secretos del usuario en el almacén de credenciales del sistema, no en un archivo de texto.

### Sin conexión y sincronización
- Definir qué funciona sin red y qué no, y comunicarlo en la interfaz.
- Si hay sincronización: cola local de cambios, resolución de conflictos definida (no "el último que llega gana" por accidente) y estado visible.

### Integración con el sistema
- Atajos, bandeja, inicio automático, notificaciones: opt-in, nunca impuestos.
- Rutas con espacios y caracteres no latinos, unidades de red, permisos denegados: probar los tres.
- Múltiples instancias: decidir si se permiten; si no, activar la ventana existente.
- Cierre: guardar estado, liberar recursos, no dejar procesos huérfanos.

## Empaquetado y actualización

| Tema | Lo que se espera |
|---|---|
| Instalador | Por sistema operativo, con desinstalación limpia |
| **Firma de código** | Sin firma, el sistema y el antivirus lo bloquean o asustan al usuario. Guardar y respaldar el certificado |
| Auto-actualización | Canal seguro, verificación de firma del paquete, reversión si falla |
| Versionado | Visible en la interfaz y en los reportes de error |
| Tamaño | Un instalador enorme para una utilidad chica es una decisión, no un destino |
| Compatibilidad | El servidor (si lo hay) debe seguir atendiendo versiones viejas: la gente no actualiza |
| Interruptores remotos | Poder apagar una funcionalidad rota sin publicar una versión nueva |

Sin rollback instantáneo, la publicación escalonada es la red de seguridad: sacar la versión a una fracción de usuarios y mirar los errores antes de completar.

## Gate específico de escritorio

| Chequeo | Qué verifica |
|---|---|
| Construcción para cada sistema objetivo | Compila y empaqueta en todos los declarados |
| Instalación limpia en máquina virgen | Sin dependencias ocultas del entorno de desarrollo |
| Actualización desde la versión anterior | Con datos reales de la versión previa |
| Migración de datos + reversión | Nada queda corrupto |
| Firma verificada | El artefacto publicado está firmado |
| Pruebas de interfaz automatizadas | Caminos críticos, no solo que arranque |
| Arranque en frío | Dentro del presupuesto declarado |
| Configuración de seguridad del motor web | Aislamiento y sandbox activos, integración directa apagada |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es interno, no hace falta firmar" | El sistema del usuario no sabe que es interno. Lo bloquea igual. |
| "Habilito el acceso completo, es más simple" | Una dependencia comprometida o una página remota se convierte en ejecución en la máquina del usuario. |
| "El usuario va a actualizar" | No actualiza. Diseña asumiendo que usará la versión de hace un año. |
| "Guardo la configuración junto al .exe" | En muchas instalaciones no hay permiso de escritura ahí, y el antivirus lo mira feo. |
| "Anduvo en mi máquina de desarrollo" | Tu máquina tiene el runtime, las librerías y las rutas. La del usuario, no. Prueba en máquina limpia. |
| "El congelamiento dura solo un segundo" | Un segundo de interfaz congelada es un reporte de "se traba". Trabajo pesado fuera del hilo de interfaz. |

## Formato de salida

- Sistemas operativos soportados y versiones mínimas.
- Configuración de seguridad del puente interfaz ↔ sistema.
- Dónde viven datos, configuración y secretos.
- Resultado de: instalación limpia, actualización desde versión anterior, migración de datos.
- Estado de firma y del canal de actualización.
- Qué sigue funcionando sin conexión.
