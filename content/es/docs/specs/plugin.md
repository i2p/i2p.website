---
title: "Formato del paquete del complemento"
description: ".xpi2p / .su3 reglas de empaquetado para complementos de I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Descripción general

Los complementos de I2P son paquetes firmados que amplían la funcionalidad del router. Se distribuyen como archivos `.xpi2p` o `.su3`, se instalan en `~/.i2p/plugins/<name>/` (o en `%APPDIR%\I2P\plugins\<name>\` en Windows) y se ejecutan con permisos completos del router, sin sandboxing (aislamiento).

### Tipos de complementos compatibles

- Aplicaciones web de la consola
- Nuevos eepsites con cgi-bin, aplicaciones web
- Temas de la consola
- Traducciones de la consola
- Programas Java (en el mismo proceso o en una JVM separada)
- Scripts de shell y binarios nativos

### Modelo de seguridad

**CRÍTICO:** Los complementos se ejecutan en la misma JVM (Máquina Virtual de Java) con los mismos permisos que el router de I2P. Tienen acceso sin restricciones a: - Sistema de archivos (lectura y escritura) - APIs del router y su estado interno - Conexiones de red - Ejecución de programas externos

Los complementos deben tratarse como código de plena confianza. Los usuarios deben verificar las fuentes y las firmas de los complementos antes de instalarlos.

---

## Formatos de archivo

### Formato SU3 (Altamente recomendado)

**Estado:** Activo, formato preferido desde I2P 0.9.15 (septiembre de 2014)

El formato `.su3` ofrece: - **Claves de firma RSA-4096** (vs. DSA-1024 en xpi2p) - Firma almacenada en el encabezado del archivo - Número mágico: `I2Psu3` - Mejor compatibilidad futura

**Estructura:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Formato XPI2P (heredado, obsoleto)

**Estado:** Se mantiene por compatibilidad con versiones anteriores, no se recomienda para nuevos complementos

El formato `.xpi2p` utiliza firmas criptográficas antiguas: - **Firmas DSA-1024** (obsoletas según NIST-800-57) - Firma DSA de 40 bytes antepuesta al ZIP - Requiere el campo `key` en plugin.config

**Estructura:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Ruta de migración:** Al migrar de xpi2p (formato de actualización anterior) a su3 (formato de archivo de actualización firmado), proporcione tanto `updateURL` como `updateURL.su3` durante la transición. Los routers modernos (0.9.15+) priorizan automáticamente SU3.

---

## Estructura del paquete y plugin.config

### Archivos necesarios

**plugin.config** - Archivo de configuración estándar de I2P con pares clave-valor

### Propiedades obligatorias

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Ejemplos de formato de versión:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Separadores válidos: `.` (punto), `-` (guion), `_` (guion bajo)

### Propiedades opcionales de metadatos

#### Mostrar información

- `date` - Fecha de lanzamiento (timestamp long de Java)
- `author` - Nombre del desarrollador (se recomienda `user@mail.i2p`)
- `description` - Descripción en inglés
- `description_xx` - Descripción localizada (xx = código de idioma)
- `websiteURL` - Página de inicio del plugin (`http://foo.i2p/`)
- `license` - Identificador de la licencia (p. ej., "Apache-2.0", "GPL-3.0")

#### Configuración de actualizaciones

- `updateURL` - Ubicación de actualización XPI2P (heredado)
- `updateURL.su3` - Ubicación de actualización SU3 (preferida)
- `min-i2p-version` - Versión mínima de I2P requerida
- `max-i2p-version` - Versión máxima de I2P compatible
- `min-java-version` - Versión mínima de Java (p. ej., `1.7`, `17`)
- `min-jetty-version` - Versión mínima de Jetty (use `6` para Jetty 6+)
- `max-jetty-version` - Versión máxima de Jetty (use `5.99999` para Jetty 5)

#### Comportamiento de la instalación

- `dont-start-at-install` - Predeterminado `false`. Si es `true`, requiere inicio manual
- `router-restart-required` - Predeterminado `false`. Informa al usuario de que se requiere reinicio después de la actualización
- `update-only` - Predeterminado `false`. Falla si el complemento no está instalado previamente
- `install-only` - Predeterminado `false`. Falla si el complemento ya existe
- `min-installed-version` - Versión mínima requerida para la actualización
- `max-installed-version` - Versión máxima que se puede actualizar
- `disableStop` - Predeterminado `false`. Oculta el botón de detener si es `true`

#### Integración con la consola

- `consoleLinkName` - Texto para el enlace de la barra de resumen de la consola
- `consoleLinkName_xx` - Texto del enlace localizado (xx = código de idioma)
- `consoleLinkURL` - Destino del enlace (p. ej., `/appname/index.jsp`)
- `consoleLinkTooltip` - Texto emergente al pasar el cursor (compatible desde la versión 0.7.12-6)
- `consoleLinkTooltip_xx` - Texto emergente localizado
- `console-icon` - Ruta al icono de 32x32 (compatible desde la versión 0.9.20)
- `icon-code` - PNG de 32x32 codificado en Base64 para plugins sin recursos web (desde la versión 0.9.25)

#### Requisitos de plataforma (solo visualización)

- `required-platform-OS` - Requisito del sistema operativo (no impuesto)
- `other-requirements` - Requisitos adicionales (p. ej., "Python 3.8+")

#### Gestión de dependencias (sin implementar)

- `depends` - Dependencias del plugin separadas por comas
- `depends-version` - Requisitos de versión para las dependencias
- `langs` - Contenido del paquete de idiomas
- `type` - Tipo de plugin (app/theme/locale/webapp)

### Sustitución de variables en la URL de actualización

**Estado de la funcionalidad:** Disponible desde I2P 1.7.0 (0.9.53)

Tanto `updateURL` como `updateURL.su3` admiten variables específicas de la plataforma:

**Variables:** - `$OS` - Sistema operativo: `windows`, `linux`, `mac` - `$ARCH` - Arquitectura: `386`, `amd64`, `arm64`

**Ejemplo:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Resultado en Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Esto permite archivos plugin.config únicos para compilaciones específicas de la plataforma.

---

## Estructura de directorios

### Diseño estándar

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Propósitos del directorio

**console/locale/** - Archivos JAR con paquetes de recursos para traducciones básicas de I2P - Las traducciones específicas de complementos deberían estar en `console/webapps/*.war` o `lib/*.jar`

**console/themes/** - Cada subdirectorio contiene un tema de consola completo - Se añade automáticamente a la ruta de búsqueda de temas

**console/webapps/** - archivos `.war` para la integración con la consola - Se inician automáticamente a menos que estén deshabilitados en `webapps.config` - El nombre del WAR no tiene que coincidir con el nombre del complemento

**eepsite/** - eepsite completo con su propia instancia de Jetty - Requiere configuración de `jetty.xml` con sustitución de variables - Consulte los ejemplos de los plugins zzzot y pebble

**lib/** - Bibliotecas JAR de complementos - Especificar en el classpath mediante `clients.config` o `webapps.config`

---

## Configuración de la aplicación web

### Formato de webapps.config

Archivo de configuración estándar de I2P que controla el comportamiento de la aplicación web.

**Sintaxis:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Notas importantes:** - Antes del router 0.7.12-9, use `plugin.warname.startOnLoad` para compatibilidad - Antes de la API 0.9.53, classpath solo funcionaba si el warname (nombre del WAR) coincidía con el nombre del plugin - A partir de 0.9.53+, classpath funciona para cualquier nombre de aplicación web

### Buenas prácticas para aplicaciones web

1. **Implementación de ServletContextListener**
   - Implementar `javax.servlet.ServletContextListener` para tareas de limpieza
   - O sobrescribir `destroy()` en el servlet
   - Garantiza un apagado correcto durante las actualizaciones y al detener el router

2. **Gestión de librerías**
   - Coloca los JAR compartidos en `lib/`, no dentro del WAR
   - Haz referencia mediante el classpath de `webapps.config`
   - Permite instalar y actualizar complementos por separado

3. **Evitar bibliotecas en conflicto**
   - Nunca empaquetes JARs de Jetty, Tomcat ni de servlets
   - Nunca empaquetes JARs de una instalación estándar de I2P
   - Revisa la sección de classpath para las bibliotecas estándar

4. **Requisitos de compilación**
   - No incluya archivos fuente `.java` o `.jsp`
   - Precompile todas las JSP para evitar retrasos en el inicio
   - No se puede asumir la disponibilidad de un compilador de Java/JSP

5. **Compatibilidad con la API de Servlet**
   - I2P es compatible con Servlet 3.0 (desde 0.9.30)
   - **NO se admite el escaneo de anotaciones** (@WebContent)
   - Debe proporcionar el descriptor de despliegue `web.xml` tradicional

6. **Versión de Jetty (servidor web Java)**
   - Actual: Jetty 9 (I2P 0.9.30+)
   - Usa `net.i2p.jetty.JettyStart` como capa de abstracción
   - Protege contra cambios en la API de Jetty

---

## Configuración del cliente

### Formato de clients.config

Define los clientes (servicios) iniciados con el complemento.

**Cliente básico:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Cliente con Detener/Desinstalar:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Referencia de propiedades

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Sustitución de variables

Las siguientes variables se sustituyen en `args`, `stopargs`, `uninstallargs` y `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Clientes gestionados vs. no gestionados

**Clientes gestionados (Recomendado, desde 0.9.4):** - Instanciados por ClientAppManager - Mantiene el seguimiento de referencias y estado - Gestión del ciclo de vida más sencilla - Mejor gestión de memoria

**Clientes no gestionados:** - Iniciados por el router, sin seguimiento de estado - Deben manejar múltiples llamadas de inicio/detención de forma adecuada - Usar estado estático o archivos PID (identificador de proceso) para la coordinación - Invocados al apagado del router (a partir de 0.7.12-3)

### ShellService (servicio de shell; desde 0.9.53 / 1.7.0)

Solución genérica para ejecutar programas externos con seguimiento automático del estado.

**Características:** - Gestiona el ciclo de vida del proceso - Se comunica con ClientAppManager (gestor de aplicaciones cliente) - Gestión automática de PID - Compatibilidad multiplataforma

**Uso:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Para scripts específicos de la plataforma:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternativa (antigua):** Escriba un envoltorio en Java que compruebe el tipo de sistema operativo y llame a `ShellCommand` con el archivo `.bat` o `.sh` correspondiente.

---

## Proceso de instalación

### Flujo de instalación del usuario

1. El usuario pega la URL del plugin en la página de configuración de plugins de la Router Console (`/configplugins`)
2. El Router descarga el archivo del plugin
3. Verificación de firma (falla si la clave es desconocida y el modo estricto está habilitado)
4. Comprobación de integridad del ZIP
5. Extraer y analizar `plugin.config`
6. Verificación de compatibilidad de versiones (`min-i2p-version`, `min-java-version`, etc.)
7. Detección de conflictos de nombre de la aplicación web
8. Detener el plugin existente si es una actualización
9. Validación del directorio (debe estar bajo `plugins/`)
10. Extraer todos los archivos al directorio del plugin
11. Actualizar `plugins.config`
12. Iniciar el plugin (a menos que `dont-start-at-install=true`)

### Seguridad y confianza

**Gestión de claves:** - Modelo de confianza 'first-key-seen' (se confía en la primera clave que se ve) para nuevos firmantes - Solo las claves de jrandom y zzz vienen preincluidas - A partir de la 0.9.14.1, las claves desconocidas se rechazan por defecto - Una propiedad avanzada puede anularlo para desarrollo

**Restricciones de instalación:** - Los archivos comprimidos deben extraerse únicamente en el directorio del plugin - El instalador rechaza rutas fuera de `plugins/` - Los plugins pueden acceder a archivos en otras ubicaciones después de la instalación - Sin sandboxing (aislamiento en entorno controlado) ni aislamiento de privilegios

---

## Mecanismo de actualización

### Proceso de comprobación de actualizaciones

1. Router lee `updateURL.su3` (preferido) o `updateURL` desde plugin.config
2. Solicitud HTTP HEAD o GET parcial para obtener los bytes 41-56
3. Extraer la cadena de versión del archivo remoto
4. Comparar con la versión instalada usando VersionComparator
5. Si es más reciente, pedir confirmación al usuario o descargar automáticamente (según la configuración)
6. Detener el complemento
7. Instalar la actualización
8. Iniciar el complemento (a menos que la preferencia del usuario haya cambiado)

### Comparación de versiones

Versiones analizadas como componentes separados por punto/guion/guion bajo: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Longitud máxima:** 16 bytes (debe coincidir con el encabezado SUD/SU3)

### Mejores prácticas de actualización

1. Incrementa siempre el número de versión para los lanzamientos
2. Prueba la ruta de actualización desde la versión anterior
3. Considera `router-restart-required` para cambios importantes
4. Proporciona tanto `updateURL` como `updateURL.su3` durante la migración
5. Usa un sufijo de número de compilación para pruebas (`1.2.3-456`)

---

## Ruta de clases y bibliotecas estándar

### Siempre disponible en el Classpath

Los siguientes archivos JAR de `$I2P/lib` siempre están en el classpath para I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Notas especiales

**commons-logging.jar:** - Vacío desde 0.9.30 - Antes de 0.9.30: Apache Tomcat JULI - Antes de 0.9.24: Commons Logging + JULI - Antes de 0.9: solo Commons Logging

**jasper-compiler.jar:** - Vacío desde Jetty 6 (0.9)

**systray4j.jar:** - Eliminado en 0.9.26

### No está en el Classpath (ruta de clases) (Debe especificarlo)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Especificación de la ruta de clases

**En clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**En webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Importante:** A partir de la versión 0.7.13-3, los classpath son específicos por hilo, no a nivel de toda la JVM. Especifique el classpath completo para cada cliente.

---

## Requisitos de la versión de Java

### Requisitos actuales (octubre de 2025)

**I2P 2.10.0 y anteriores:** - Mínimo: Java 7 (requerido desde 0.9.24, enero de 2016) - Recomendado: Java 8 o superior

**I2P 2.11.0 y posteriores (PRÓXIMAMENTE):** - **Mínimo: Java 17+** (anunciado en las notas de la versión 2.9.0) - Aviso con dos versiones de antelación (2.9.0 → 2.10.0 → 2.11.0)

### Estrategia de compatibilidad de complementos

**Para la máxima compatibilidad (hasta I2P 2.10.x inclusive):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Para las características de Java 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Para las características de Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Preparación para 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Mejores prácticas de compilación

**Al compilar con un JDK más reciente para una versión de destino más antigua:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Esto impide utilizar APIs no disponibles en la versión de Java de destino.

---

## Compresión Pack200 - OBSOLETO

### Actualización crítica: no utilice Pack200 (formato de compresión para JAR de Java)

**Estado:** OBSOLETO Y ELIMINADO

La especificación original recomendaba encarecidamente la compresión Pack200 para una reducción del tamaño del 60-65%. **Esto ya no es válido.**

**Cronología:** - **JEP 336:** Pack200 se marcó como obsoleto en Java 11 (septiembre de 2018) - **JEP 367:** Pack200 se eliminó en Java 14 (marzo de 2020)

**La especificación oficial de actualizaciones de I2P establece:** > "Los archivos JAR y WAR en el ZIP ya no se comprimen con pack200, como se documenta arriba para los archivos 'su2', porque las versiones recientes de los entornos de ejecución de Java ya no lo admiten."

**Qué hacer:**

1. **Eliminar pack200 (formato de compresión de JAR de Java) de los procesos de compilación inmediatamente**
2. **Usar compresión ZIP estándar**
3. **Considerar alternativas:**
   - ProGuard/R8 (minificador/ofuscador) para reducción del tamaño del código
   - UPX (compresor de ejecutables) para binarios nativos
   - Algoritmos de compresión modernos (zstd, brotli) si se proporciona un desempaquetador personalizado

**Para plugins existentes:** - Los routers antiguos (0.7.11-5 hasta Java 10) aún pueden desempaquetar pack200 - Los routers nuevos (Java 11+) no pueden desempaquetar pack200 - Republicue los plugins sin compresión pack200

---

## Claves de firma y seguridad

### Generación de claves (formato SU3)

Utiliza el script `makeplugin.sh` del repositorio i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Detalles clave:** - Algoritmo: RSA_SHA512_4096 - Formato: certificado X.509 - Almacenamiento: formato de almacén de claves de Java

### Firma de plugins

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Mejores prácticas de gestión de claves

1. **Generar una vez, proteger para siempre**
   - Los Routers rechazan nombres de clave duplicados con claves diferentes
   - Los Routers rechazan claves duplicadas con nombres de clave diferentes
   - Se rechazan las actualizaciones si la clave y el nombre no coinciden

2. **Almacenamiento seguro**
   - Haz una copia de seguridad del almacén de claves (keystore) de forma segura
   - Usa una frase de contraseña segura
   - Nunca lo confirmes en el control de versiones

3. **Rotación de claves**
   - No está soportado por la arquitectura actual
   - Planificar el uso de claves a largo plazo
   - Considerar esquemas de multifirma para el desarrollo en equipo

### Firma DSA heredada (XPI2P)

**Estado:** Funcional pero obsoleto

Firmas DSA-1024 utilizadas por el formato xpi2p: - firma de 40 bytes - clave pública de 172 caracteres en base64 - NIST-800-57 recomienda (L=2048, N=224) como mínimo - I2P utiliza parámetros más débiles (L=1024, N=160)

**Recomendación:** Utiliza SU3 (formato de archivo firmado de I2P) con RSA-4096 en su lugar.

---

## Directrices para el desarrollo de plugins

### Mejores prácticas esenciales

1. **Documentación**
   - Proporcionar un README claro con instrucciones de instalación
   - Documentar las opciones de configuración y los valores predeterminados
   - Incluir un registro de cambios con cada versión
   - Especificar las versiones requeridas de I2P/Java

2. **Optimización del tamaño**
   - Incluir solo los archivos necesarios
   - Nunca empaquetar JARs del router
   - Separar paquetes de instalación y actualización (bibliotecas en lib/)
   - ~~Usar compresión Pack200~~ **OBSOLETO - Usar ZIP estándar**

3. **Configuración**
   - Nunca modifiques `plugin.config` en tiempo de ejecución
   - Usa un archivo de configuración separado para los ajustes en tiempo de ejecución
   - Documenta los ajustes necesarios del router (puertos SAM, tunnels, etc.)
   - Respeta la configuración existente del usuario

4. **Uso de recursos**
   - Evita un consumo agresivo de ancho de banda por defecto
   - Implementa límites razonables de uso de la CPU
   - Libera los recursos al finalizar
   - Usa hilos daemon (hilos en segundo plano) cuando corresponda

5. **Pruebas**
   - Probar instalación/actualización/desinstalación en todas las plataformas
   - Probar actualizaciones desde la versión anterior
   - Verificar detención/reinicio de la aplicación web durante las actualizaciones
   - Probar con la versión mínima de I2P admitida

6. **Sistema de archivos**
   - Nunca escribas en `$I2P` (puede ser de solo lectura)
   - Escribe los datos en tiempo de ejecución en `$PLUGIN` o `$CONFIG`
   - Usa `I2PAppContext` para el descubrimiento de directorios
   - No asumas la ubicación de `$CWD`

7. **Compatibilidad**
   - No dupliques las clases estándar de I2P
   - Extiende las clases si es necesario, no las reemplaces
   - Comprueba `min-i2p-version`, `min-jetty-version` en plugin.config
   - Prueba con versiones antiguas de I2P si vas a admitirlas

8. **Gestión del apagado**
   - Implementa `stopargs` adecuados en clients.config
   - Registra ganchos de apagado: `I2PAppContext.addShutdownTask()`
   - Gestiona múltiples llamadas de inicio/parada de forma adecuada
   - Configura todos los hilos en modo demonio

9. **Seguridad**
   - Validar toda entrada externa
   - Nunca llamar a `System.exit()`
   - Respetar la privacidad del usuario
   - Seguir prácticas de codificación segura

10. **Licencias**
    - Especifica claramente la licencia del plugin
    - Respeta las licencias de las bibliotecas incluidas
    - Incluye la atribución requerida
    - Proporciona acceso al código fuente si se requiere

### Consideraciones avanzadas

**Gestión de la zona horaria:** - Router establece la zona horaria de la JVM en UTC - Zona horaria real del usuario: propiedad `i2p.systemTimeZone` de `I2PAppContext`

**Descubrimiento de directorios:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Numeración de versiones:** - Usa versionado semántico (major.minor.patch) - Añade un número de compilación para pruebas (1.2.3-456) - Garantiza un incremento monótono en las actualizaciones

**Acceso a clases del router:** - En general, evite dependencias de `router.jar` - En su lugar, use las API públicas en `i2p.jar` - En el futuro, I2P podría restringir el acceso a clases del router

**Prevención de fallos de la JVM (histórico):** - Corregido en 0.7.13-3 - Utiliza correctamente los cargadores de clases - Evita actualizar archivos JAR en un plugin en ejecución - Diseña para reiniciar tras la actualización si es necesario

---

## Complementos de Eepsite

### Descripción general

Los plugins pueden proporcionar eepsites completos con sus propias instancias de Jetty e I2PTunnel.

### Arquitectura

**No intente:** - Instalar en un eepsite existente - Fusionar con el eepsite predeterminado del router - Asumir la disponibilidad de un único eepsite

**En su lugar:** - Iniciar una nueva instancia de I2PTunnel (mediante la CLI (interfaz de línea de comandos)) - Iniciar una nueva instancia de Jetty - Configurar ambos en `clients.config`

### Estructura de ejemplo

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Sustitución de variables en jetty.xml

Utiliza la variable `$PLUGIN` para las rutas:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router realiza una sustitución durante el inicio del plugin.

### Ejemplos

Implementaciones de referencia: - **zzzot plugin** - Rastreador de torrents - **pebble plugin** - Plataforma de blogs

Ambos están disponibles en la página de plugins de zzz (I2P-internal).

---

## Integración con la consola

### Enlaces de la barra de resumen

Añadir un enlace clicable a la barra de resumen de la consola del router:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Versiones localizadas:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Iconos de la consola

**Archivo de imagen (desde 0.9.20):**

```properties
console-icon=/myicon.png
```
Ruta relativa a `consoleLinkURL` si se especifica (desde 0.9.53); en caso contrario, relativa al nombre de la aplicación web.

**Icono incrustado (desde 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Generar con:

```bash
base64 -w 0 icon-32x32.png
```
O en Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Requisitos: - 32x32 píxeles - Formato PNG - Codificado en Base64 (sin saltos de línea)

---

## Internacionalización

### Paquetes de traducción

**Para las traducciones base de I2P:** - Coloque los archivos JAR en `console/locale/` - Contienen paquetes de recursos para las aplicaciones de I2P existentes - Nomenclatura: `messages_xx.properties` (xx = código de idioma)

**Para traducciones específicas de plugins:** - Incluye en `console/webapps/*.war` - O incluye en `lib/*.jar` - Usa el método estándar de Java ResourceBundle

### Cadenas localizadas en plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Campos admitidos: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Traducción del tema de la consola

Los temas en `console/themes/` se añaden automáticamente a la ruta de búsqueda de temas.

---

## Complementos específicos de la plataforma

### Enfoque de paquetes separados

Utilice distintos nombres de complementos para cada plataforma:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Enfoque de sustitución de variables

Un único plugin.config con variables de plataforma:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
En clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Detección del sistema operativo en tiempo de ejecución

Enfoque en Java para la ejecución condicional:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Solución de problemas

### Problemas comunes

**El plugin no se inicia:** 1. Compruebe la compatibilidad con la versión de I2P (`min-i2p-version`) 2. Verifique la versión de Java (`min-java-version`) 3. Revise los registros del router en busca de errores 4. Verifique que todos los archivos JAR requeridos estén en el classpath

**Aplicación web no accesible:** 1. Comprueba que `webapps.config` no la deshabilita 2. Comprueba la compatibilidad de la versión de Jetty (servidor web Java) (`min-jetty-version`) 3. Comprueba que `web.xml` esté presente (no se admite el escaneo de anotaciones) 4. Comprueba si hay nombres de aplicaciones web en conflicto

**La actualización falla:** 1. Verifica que la cadena de versión haya aumentado 2. Verifica que la firma sea válida con la clave de firma 3. Asegúrate de que el nombre del plugin coincida con la versión instalada 4. Revisa la configuración `update-only`/`install-only`

**El programa externo no se detiene:** 1. Usa ShellService (servicio de shell) para la gestión automática del ciclo de vida 2. Implementa un manejo adecuado de `stopargs` 3. Comprueba la limpieza del archivo PID 4. Verifica la terminación del proceso

### Registro de depuración

Habilitar el registro de depuración en el router:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Revisa los registros:

```
~/.i2p/logs/log-router-0.txt
```
---

## Información de referencia

### Especificaciones oficiales

- [Especificación de complementos](/docs/specs/plugin/)
- [Formato de configuración](/docs/specs/configuration/)
- [Especificación de actualización](/docs/specs/updates/)
- [Criptografía](/docs/specs/cryptography/)

### Historial de versiones de I2P

**Versión actual:** - **I2P 2.10.0** (8 de septiembre de 2025)

**Versiones principales desde 0.9.53:** - 2.10.0 (sep 2025) - anuncio sobre Java 17+ - 2.9.0 (jun 2025) - advertencia sobre Java 17+ - 2.8.0 (oct 2024) - pruebas de criptografía poscuántica - 2.6.0 (may 2024) - bloqueo de I2P-over-Tor - 2.4.0 (dic 2023) - mejoras de seguridad en NetDB - 2.2.0 (mar 2023) - control de congestión - 2.1.0 (ene 2023) - mejoras en la red - 2.0.0 (nov 2022) - protocolo de transporte SSU2 - 1.7.0/0.9.53 (feb 2022) - ShellService (servicio de shell), sustitución de variables - 0.9.15 (sep 2014) - formato SU3 introducido

**Numeración de versiones:** - Serie 0.9.x: Hasta la versión 0.9.53 - Serie 2.x: A partir de la versión 2.0.0 (introducción de SSU2)

### Recursos para desarrolladores

**Código fuente:** - Repositorio principal: https://i2pgit.org/I2P_Developers/i2p.i2p - Espejo de GitHub: https://github.com/i2p/i2p.i2p

**Ejemplos de plugins:** - zzzot (rastreador de BitTorrent) - pebble (plataforma de blogs) - i2p-bote (correo electrónico sin servidor) - orchid (cliente de Tor) - seedless (intercambio de pares)

**Herramientas de compilación:** - makeplugin.sh - Generación y firma de claves - Se encuentra en el repositorio i2p.scripts - Automatiza la creación y la verificación de su3 (archivo de actualización firmado de I2P)

### Soporte de la comunidad

**Foros:** - [Foro de I2P](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (interno de I2P)

**IRC/Chat:** - #i2p-dev en OFTC - IRC de I2P dentro de la red

---

## Apéndice A: Ejemplo completo de plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Apéndice B: Ejemplo completo de clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Apéndice C: Ejemplo completo de webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Apéndice D: Lista de verificación de migración (0.9.53 a 2.10.0)

### Cambios necesarios

- [ ] **Eliminar la compresión Pack200 del proceso de compilación**
  - Eliminar las tareas de Pack200 de los scripts de Ant/Maven/Gradle
  - Volver a publicar los complementos existentes sin Pack200

- [ ] **Revisar los requisitos de versión de Java**
  - Considerar exigir Java 11+ para nuevas funcionalidades
  - Planificar el requisito de Java 17+ para I2P 2.11.0
  - Actualizar `min-java-version` en plugin.config

- [ ] **Actualizar la documentación**
  - Eliminar las referencias a Pack200 (formato de compresión de Java)
  - Actualizar los requisitos de versión de Java
  - Actualizar las referencias de versión de I2P (0.9.x → 2.x)

### Cambios recomendados

- [ ] **Fortalecer las firmas criptográficas**
  - Migrar de XPI2P (formato de paquete de complementos de I2P) a SU3 (formato de archivo firmado para actualizaciones/paquetes de I2P) si aún no se ha hecho
  - Usar claves RSA-4096 para nuevos complementos

- [ ] **Aproveche las nuevas funciones (si usa 0.9.53+)**
  - Use las variables `$OS` / `$ARCH` para actualizaciones específicas de la plataforma
  - Use ShellService (servicio Shell) para programas externos
  - Use el classpath mejorado de la aplicación web (funciona para cualquier nombre de WAR)

- [ ] **Probar compatibilidad**
  - Probar en I2P 2.10.0
  - Verificar con Java 8, 11, 17
  - Comprobar en Windows, Linux, macOS

### Mejoras opcionales

- [ ] Implementar un ServletContextListener (escuchador del contexto del servlet) adecuado
- [ ] Añadir descripciones localizadas
- [ ] Proporcionar un icono para la consola
- [ ] Mejorar la gestión del cierre
- [ ] Añadir un registro exhaustivo
- [ ] Escribir pruebas automatizadas
