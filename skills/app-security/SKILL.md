---
name: app-security
description: "Harden an app handling users, money, personal data, uploads, tokens or secrets. \"es seguro?\", \"revisa la seguridad\", \"me hackearon\", \"expuse una clave\", before shipping. OWASP Top 10 baseline."
---

# App-Security — el baseline defensivo de lo que construyes

## Overview

Casi todos los incidentes de aplicaciones no vienen de un ataque sofisticado: vienen de un control de acceso mal hecho, una configuración por defecto, una dependencia sin auditar o una clave en el repositorio. El listado de referencia de la industria (OWASP Top 10:2025) pone en el primer lugar el **control de acceso roto**, segundo la **configuración insegura** y tercero las **fallas de cadena de suministro**.

La regla que ahorra el 90% del trabajo: **nada que venga del cliente decide permisos, precios ni identidad.**

## Cuándo usar

- Diseñar autenticación, roles, sesiones, multi-inquilino.
- Subidas de archivos, webhooks entrantes, integraciones con terceros.
- Antes de exponer algo a internet o a usuarios reales.
- Después de un incidente o de exponer una credencial.
- Revisión periódica de dependencias y configuración.

## Cuándo NO usar

| Situación | Ruta |
|---|---|
| Pruebas ofensivas autorizadas, CTF, análisis de binarios | herramientas/skills de pentest, no esta |
| Bug funcional sin componente de seguridad | `fixer` |
| Revisión de un diff concreto | `diff-review` (trae el guion corto de seguridad) |

## Regla de hierro: el servidor no confía en nadie

```
TODA ENTRADA SE VALIDA DEL LADO QUE NO CONTROLA EL USUARIO. TODA AUTORIZACION SE VERIFICA POR RECURSO, NO POR PANTALLA.
```

Esconder un botón no es autorización. Validar en el navegador no es validar. Un identificador en la URL es una entrada del usuario, no una prueba de propiedad.

## Baseline por capas

### 1. Identidad y acceso (la categoría #1)
- Verificar **propiedad del recurso** en cada operación: "¿este usuario puede tocar ESTE registro?", no solo "¿está logueado?".
- Denegar por defecto; permitir explícito. Los roles se evalúan en el servidor, en un solo lugar.
- Multi-inquilino: el identificador de inquilino sale de la sesión, **jamás** del cuerpo o de la URL.
- Sesiones: expiración, invalidación al cambiar contraseña, cookies `HttpOnly` + `Secure` + `SameSite`.
- Contraseñas: algoritmo lento y actual (argon2/bcrypt/scrypt), nunca hash propio. Límite de intentos y retardo progresivo.
- Segundo factor en cuentas administrativas. Recuperación de cuenta: el camino favorito para entrar; tratarlo con el mismo rigor que el login.

### 2. Secretos
- Nunca en el repo, ni en el historial, ni en el bundle del cliente, ni en logs, ni en capturas.
- Variables de entorno o gestor de secretos; `.env.example` con claves vacías.
- Escaneo de secretos en el gate y en el historial.
- **Credencial expuesta = rotarla inmediatamente**, antes de limpiar el historial. Borrar el archivo no revoca nada: ya se copió.
- Una credencial por entorno y por servicio, con el permiso mínimo.

### 3. Entrada y salida
- Validar con esquema en el borde: tipo, rango, longitud, formato. Rechazar lo desconocido.
- Consultas parametrizadas siempre; nada de concatenar SQL. Nada de comandos del sistema con entrada de usuario; si es inevitable, lista blanca estricta.
- Salida escapada según el destino (HTML, atributos, SQL, shell, plantillas de mensajes).
- Subidas: validar tipo real (no la extensión), límite de tamaño, renombrar, guardar fuera de la raíz web, servir con `Content-Type` fijo y sin ejecución.
- Peticiones salientes construidas con datos del usuario: lista blanca de destinos (evitar que tu servidor sea usado para alcanzar la red interna).

### 4. Configuración
- Depuración apagada en producción; errores genéricos al usuario y detalle solo en el log.
- CORS con origen explícito, no comodín. Cabeceras de seguridad y política de contenido.
- Puertos y paneles de administración cerrados a internet; base de datos nunca expuesta.
- Permisos mínimos en la nube; buckets privados por defecto.
- Entornos separados: producción no comparte credenciales con desarrollo, ni datos reales sin anonimizar.

### 5. Dependencias (cadena de suministro)
- Auditoría en cada gate; versiones fijadas; lockfile commiteado.
- Instalar solo lo necesario; revisar qué arrastra y quién la mantiene.
- Actualizaciones de seguridad con cadencia, no cuando explota.
- Scripts de instalación de paquetes: sospechosos por defecto en entornos automatizados.

### 6. Datos
- Cifrado en tránsito siempre; en reposo para lo sensible.
- Guardar lo mínimo. El dato que no existe no se filtra.
- Datos personales: propósito declarado, plazo de retención, borrado y exportación posibles.
- Respaldos cifrados, **restauración probada** (respaldo no verificado = sin respaldo).
- Nunca datos reales en entornos de prueba.

### 7. Registro y detección
- Registrar: inicios de sesión y fallos, cambios de permisos, operaciones sobre dinero, borrados, accesos administrativos.
- Nunca registrar: contraseñas, tokens, números completos de tarjeta, documentos de identidad.
- Alertar sobre picos de error, fallos de autenticación y uso anómalo.

## Ajustes por tipo de aplicación

| Tipo | Lo que se rompe primero |
|---|---|
| **Web** | Control de acceso por vista en vez de por recurso; XSS por render sin escapar; CSRF en formularios; claves de API en el bundle del navegador |
| **API** | Endpoints sin verificación de propiedad; sin límite de uso; enumeración de identificadores; versiones viejas abiertas |
| **Bot de mensajería** | Webhook sin verificar firma; comandos administrativos sin lista blanca; inyección de prompt desde mensajes de usuario; credenciales de sesión del canal en texto plano |
| **Automatización** | Credenciales en el script; ejecución con permisos de más; datos descargados y olvidados en disco |
| **Escritorio** | Contenido remoto con acceso a APIs nativas; puente entre interfaz y sistema demasiado ancho; actualizaciones sin firmar |
| **Móvil** | Secretos dentro del APK (es lectura pública); tráfico sin validar certificado; datos sensibles en almacenamiento no cifrado; permisos excesivos |

## Si ya pasó algo (orden, no pánico)

1. Contener: rotar credenciales, revocar sesiones, cerrar el acceso.
2. Preservar evidencia (logs, copias) antes de limpiar.
3. Determinar alcance: qué datos, cuántos usuarios, desde cuándo.
4. Arreglar la causa raíz, no el síntoma.
5. Avisar a quien corresponde según la ley y el contrato.
6. Registrar en `bugs.md` con causa raíz y prevención.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Es un proyecto chico, nadie lo va a atacar" | Los escaneos son automáticos e indiscriminados. No te eligen: te encuentran. |
| "La clave está en el frontend pero ofuscada" | Todo lo que llega al navegador o al APK es público. Ofuscar no es proteger. |
| "Ya validé en el cliente" | El cliente lo controla el usuario. La validación del servidor es la única que cuenta. |
| "Lo aseguramos antes de salir a producción" | Retrofit de seguridad = rediseño. El control de acceso se diseña con el modelo de datos. |
| "Uso HTTPS, estoy seguro" | HTTPS protege el tránsito. No arregla permisos, inyección ni configuración. |
| "Nadie conoce esa URL" | Seguridad por oscuridad: dura hasta el primer escaneo o el primer referer filtrado. |

## Formato de salida

- Hallazgos por categoría con severidad, escenario de explotación concreto y corrección.
- Qué se verificó automáticamente (auditoría de dependencias, escaneo de secretos, cabeceras) con su salida real.
- Lo que requiere decisión del dueño del producto (retención de datos, segundo factor, permisos).
- Acciones inmediatas si hay algo expuesto, en orden.
