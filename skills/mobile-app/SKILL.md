---
name: mobile-app
description: Use when building or shipping a mobile app or APK — Android/iOS, Kotlin/Swift, React Native, Flutter, Capacitor/Cordova, PWA-to-app, "hazme una app para el celular", "genera el APK", "subirla a Play Store", permissions, push notifications, offline storage, signing, store requirements and releases. Covers platform constraints, permissions, offline, release/signing and the mobile-specific gate. NO para apps de escritorio (desktop-app) ni sitios web responsivos (web-app).
---

# Mobile-App — el entorno más hostil en el que va a correr tu código

## Overview

Un teléfono es un entorno hostil: red intermitente, batería limitada, el sistema mata tu proceso cuando quiere, la pantalla es chica, los permisos los concede (o niega) el usuario, y **el paquete que publicas es leíble por cualquiera**. Además, publicar tiene reglas de terceros con fechas límite: versiones mínimas del sistema, formatos de empaquetado, declaraciones de privacidad, requisitos técnicos que cambian cada año.

Lo que en web es un ajuste rápido, aquí es una versión nueva que la gente puede no instalar nunca.

## Cuándo usar

- Construir o ampliar una aplicación móvil, nativa o híbrida.
- Generar, firmar o publicar un paquete.
- Permisos, notificaciones, almacenamiento local, trabajo sin conexión.
- Preparar una publicación en tienda o una distribución directa.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Sitio web que se ve en móvil | `web-app` |
| Aplicación de escritorio | `desktop-app` |
| API que consume la app | `api-backend` |
| Algo se ve mal en pantalla | `ui-bug` |

## Regla de hierro: el paquete es público

```
TODO LO QUE VIAJA DENTRO DEL APK/IPA ES LEIBLE: CLAVES, ENDPOINTS, LOGICA, TEXTOS. NINGUN SECRETO VIVE AHI.
```

Cualquiera puede descomprimir el paquete y leerlo. Las claves de servicios de pago, bases de datos o APIs privilegiadas viven en tu servidor; la app solo habla con tu servidor. Las validaciones de negocio que importan se hacen del lado del servidor: la app se puede modificar.

## Decisiones tempranas

| Decisión | Criterio |
|---|---|
| Nativo vs multiplataforma | ¿Usa capacidades del sistema a fondo o es principalmente pantallas y datos? ¿Quién la mantendrá? |
| Tienda vs distribución directa | La tienda impone requisitos y revisiones, pero da confianza, actualizaciones y alcance. Instalar un archivo a mano exige que el usuario baje sus defensas — mala señal para un producto público |
| Versión mínima del sistema | Cubre a tus usuarios reales, no a todos los teléfonos del mundo |
| Sin conexión | ¿Solo lectura en caché, o crear y editar y sincronizar después? Cambia toda la arquitectura |
| Notificaciones | ¿De verdad hacen falta? Traen infraestructura, permisos y fatiga del usuario |

Antes de empezar a construir, verifica los **requisitos vigentes de la tienda** (versión mínima del sistema objetivo, formato de publicación, requisitos técnicos del empaquetado, declaración de datos y privacidad) y sus fechas límite. Cambian todos los años y bloquean publicaciones sin aviso útil.

## Construcción

### Ciclo de vida y recursos
- El sistema puede suspender o matar la app en cualquier momento: guarda el estado, restaura al volver.
- Nada de trabajo pesado en el hilo principal; una interfaz que traba se siente rota.
- Cuidar batería y datos: nada de sondeos constantes, de ubicación continua sin motivo ni de descargas en red móvil sin avisar.
- Probar en gama baja, no solo en el mejor teléfono disponible.

### Red intermitente
- Asume caída en mitad de la petición: tiempos límite, reintentos con retardo creciente, mensajes claros.
- Diferencia "sin conexión" de "el servidor falló": el usuario necesita saber si esperar o reintentar.
- Cola de acciones pendientes si la app permite crear datos sin conexión, con sincronización idempotente.

### Permisos
- Pedir en el momento en que se usan, explicando para qué, no todos al abrir.
- Funcionar de forma degradada si el usuario niega; nunca bloquear la app entera.
- Pedir el mínimo: cada permiso sensible es fricción, riesgo de rechazo en tienda y desconfianza.

### Almacenamiento
- Datos sensibles en el almacén cifrado del sistema, no en preferencias planas ni en archivos sueltos.
- Base local con migraciones versionadas y probadas desde la versión publicada anterior.
- Limitar el crecimiento de cachés: llenar el teléfono es motivo de desinstalación.

### Interfaz
- Área segura, teclado que tapa campos, rotación, texto grande por accesibilidad, modo oscuro si el sistema lo pide.
- Áreas táctiles cómodas; navegación con el botón atrás coherente.
- Estados de carga/vacío/error en cada pantalla que trae datos.

## Publicación

| Paso | Detalle |
|---|---|
| Firma | Clave de firma generada, **respaldada fuera del equipo** y nunca en el repositorio. Perderla puede significar perder la app publicada |
| Versionado | Código de versión incremental + nombre visible; trazable al commit |
| Requisitos técnicos | Versión objetivo del sistema y formato de empaquetado vigentes, verificados antes de enviar |
| Privacidad | Declaración de datos recolectados coherente con lo que la app hace de verdad |
| Prueba en dispositivo real | Al menos uno físico, de gama baja |
| Publicación escalonada | Por porcentaje, mirando errores y reseñas antes de completar |
| Compatibilidad del servidor | Las versiones viejas siguen ahí: el backend no puede romperlas |
| Interruptores remotos | Apagar una funcionalidad rota sin publicar versión nueva |

## Gate específico de móvil

| Chequeo | Qué verifica |
|---|---|
| Construcción de release firmada | Compila, firma y se instala |
| Instalación limpia + actualización sobre versión anterior | Migración de datos incluida |
| Sin secretos en el paquete | Escaneo del artefacto, no solo del repo |
| Permisos declarados = permisos usados | Nada de más |
| Modo avión / red lenta | Comportamiento definido |
| Ciclo de vida | Suspender, matar y restaurar sin perder estado |
| Pruebas de interfaz de los caminos críticos | En emulador y en un dispositivo real |
| Tamaño del paquete | Con trinquete: no crece sin motivo |

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Guardo la clave de la API en la app, está compilada" | Compilado no es cifrado. Se extrae en minutos. |
| "Pido todos los permisos al inicio, es más fácil" | Aumenta rechazos de tienda y desinstalaciones, y no lo necesitas. |
| "Probé en el emulador, alcanza" | El emulador no tiene red mala, batería, ni el sistema matándote la app. |
| "Si hay un bug publico otra versión" | La revisión tarda y la gente no actualiza. Interruptores remotos y publicación escalonada. |
| "La validación la hago en la app" | La app la controla el usuario. La validación real vive en el servidor. |
| "Genero el APK y que lo instalen a mano" | Válido para pruebas internas. Para un producto público, pides al usuario que ignore las advertencias de seguridad de su teléfono. |

## Formato de salida

- Plataformas y versiones mínimas soportadas.
- Permisos solicitados y justificación de cada uno.
- Comportamiento sin conexión y estrategia de sincronización.
- Resultado del gate, incluido el escaneo de secretos sobre el paquete final.
- Estado de firma, respaldo de la clave y plan de publicación.
- Requisitos de tienda verificados con fecha de verificación.
