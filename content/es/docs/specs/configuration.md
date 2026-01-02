---
title: "Configuración del Router"
description: "Opciones y formatos de configuración para I2P routers y clientes"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Descripción general

Este documento proporciona una especificación técnica exhaustiva de los archivos de configuración de I2P utilizados por el router y diversas aplicaciones. Cubre las especificaciones del formato de archivo, las definiciones de propiedades y los detalles de implementación verificados frente al código fuente de I2P y la documentación oficial.

### Alcance

- Archivos y formatos de configuración del router
- Configuraciones de aplicaciones cliente
- Configuraciones de tunnel de I2PTunnel
- Especificaciones del formato de archivo e implementación
- Características específicas de la versión y elementos en desuso

### Notas de implementación

Los archivos de configuración se leen y se escriben utilizando los métodos `DataHelper.loadProps()` y `storeProps()` en la biblioteca central de I2P. El formato del archivo difiere significativamente del formato serializado utilizado en los protocolos de I2P (véase [Especificación de estructuras comunes - asignación de tipos](/docs/specs/common-structures/#type-mapping)).

---

## Formato general del archivo de configuración

Los archivos de configuración de I2P siguen un formato de propiedades de Java modificado, con excepciones y restricciones específicas.

### Especificación de formato

Basado en [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) con las siguientes diferencias fundamentales:

#### Codificación

- **DEBE** utilizar la codificación UTF-8 (NO ISO-8859-1 como en las Properties estándar de Java)
- Implementación: Usa las utilidades `DataHelper.getUTF8()` para todas las operaciones de archivo

#### Secuencias de escape

- **NO** se reconocen secuencias de escape (incluida la barra invertida `\`)
- La continuación de línea **NO** es compatible
- Los caracteres de barra invertida se tratan como literales

#### Caracteres de comentario

- `#` inicia un comentario en cualquier posición de una línea
- `;` inicia un comentario **solo** cuando está en la columna 1
- `!` NO inicia un comentario (difiere de Java Properties)

#### Separadores de clave-valor

- `=` es el **ÚNICO** separador válido de clave-valor
- `:` **NO** se reconoce como separador
- El espacio en blanco **NO** se reconoce como separador

#### Manejo de espacios en blanco

- Los espacios en blanco al principio y al final **NO** se eliminan de las claves
- Los espacios en blanco al principio y al final **SÍ** se eliminan de los valores

#### Procesamiento de líneas

- Las líneas sin `=` se ignoran (se tratan como comentarios o líneas en blanco)
- Los valores vacíos (`key=`) se admiten a partir de la versión 0.9.10
- Las claves con valores vacíos se almacenan y se recuperan normalmente

#### Restricciones de caracteres

**Las claves NO pueden contener**: - `#` (signo de almohadilla/numeral) - `=` (signo igual) - `\n` (carácter de nueva línea) - No pueden comenzar con `;` (punto y coma)

**Los valores NO pueden contener**: - `#` (símbolo hash/almohadilla) - `\n` (carácter de nueva línea) - No pueden empezar ni terminar con `\r` (retorno de carro) - No pueden empezar ni terminar con espacios en blanco (se recortan automáticamente)

### Ordenación de archivos

Los archivos de configuración no tienen por qué estar ordenados por clave. Sin embargo, la mayoría de las aplicaciones de I2P ordenan las claves alfabéticamente al escribir archivos de configuración para facilitar: - Edición manual - Operaciones de diff (comparación de cambios) del control de versiones - Legibilidad humana

### Detalles de implementación

#### Lectura de archivos de configuración

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Comportamiento**: - Lee archivos codificados en UTF-8 - Aplica todas las reglas de formato descritas anteriormente - Valida las restricciones de caracteres - Devuelve un objeto Properties vacío si el archivo no existe - Lanza `IOException` por errores de lectura

#### Escritura de archivos de configuración

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Comportamiento**: - Escribe archivos codificados en UTF-8 - Ordena las claves alfabéticamente (a menos que se use OrderedProperties) - Establece los permisos de archivo al modo 600 (solo lectura/escritura del usuario) a partir de la versión 0.8.1 - Lanza `IllegalArgumentException` por caracteres no válidos en claves o valores - Lanza `IOException` por errores de escritura

#### Validación de formato

La implementación realiza una validación estricta: - Se verifican las claves y los valores para detectar caracteres prohibidos - Las entradas inválidas provocan excepciones durante las operaciones de escritura - La lectura ignora silenciosamente las líneas con formato incorrecto (líneas sin `=`)

### Ejemplos de formato

#### Archivo de configuración válido

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Ejemplos de configuraciones no válidas

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Biblioteca central y configuración del router

### Configuración de clientes (clients.config)

**Ubicación**: `$I2P_CONFIG_DIR/clients.config` (heredado) o `$I2P_CONFIG_DIR/clients.config.d/` (moderno)   **Interfaz de configuración**: consola del router en `/configclients`   **Cambio de formato**: Versión 0.9.42 (agosto de 2019)

#### Estructura de directorios (versión 0.9.42+)

A partir de la versión 0.9.42, el archivo clients.config predeterminado se divide automáticamente en archivos de configuración individuales:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Comportamiento de migración**: - En la primera ejecución tras actualizar a 0.9.42+, el archivo monolítico se divide automáticamente - Las propiedades en los archivos divididos llevan el prefijo `clientApp.0.` - Se sigue admitiendo el formato heredado para compatibilidad retroactiva - El formato dividido habilita el empaquetado modular y la gestión de complementos

#### Formato de propiedades

Las líneas tienen la forma `clientApp.x.prop=val`, donde `x` es el número de la aplicación.

**Requisitos de numeración de la aplicación**: - DEBE comenzar con 0 - DEBE ser consecutiva (sin saltos) - El orden determina la secuencia de inicio

#### Propiedades obligatorias

##### principal

- **Tipo**: String (nombre de clase completamente calificado)
- **Obligatorio**: Sí
- **Descripción**: El constructor o el método `main()` de esta clase se invocará según el tipo de cliente (gestionado vs. no gestionado)
- **Ejemplo**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Propiedades opcionales

##### nombre

- **Tipo**: Cadena
- **Obligatorio**: No
- **Descripción**: Nombre mostrado en la consola del router
- **Ejemplo**: `clientApp.0.name=Router Console`

##### argumentos

- **Tipo**: Cadena (separada por espacios o tabulaciones)
- **Obligatorio**: No
- **Descripción**: Argumentos pasados al constructor de la clase principal o al método main()
- **Entrecomillado**: Los argumentos que contengan espacios o tabulaciones pueden entrecomillarse con `'` o `"`
- **Ejemplo**: `clientApp.0.args=-d $CONFIG/eepsite`

##### retraso

- **Tipo**: Entero (segundos)
- **Requerido**: No
- **Predeterminado**: 120
- **Descripción**: Segundos a esperar antes de iniciar el cliente
- **Sobrescritura**: Sobrescrito por `onBoot=true` (establece el retardo en 0)
- **Valores especiales**:
  - `< 0`: Esperar a que el router alcance el estado RUNNING y luego iniciar inmediatamente en un hilo nuevo
  - `= 0`: Ejecutar inmediatamente en el mismo hilo (las excepciones se propagan a la consola)
  - `> 0`: Iniciar tras el retardo en un hilo nuevo (las excepciones se registran, no se propagan)

##### onBoot

- **Tipo**: Booleano
- **Obligatorio**: No
- **Predeterminado**: false
- **Descripción**: Fuerza un retraso de 0 y anula la configuración explícita de retraso
- **Caso de uso**: Iniciar servicios críticos de inmediato al arranque del router

##### startOnLoad

- **Tipo**: Boolean
- **Obligatorio**: No
- **Predeterminado**: true
- **Descripción**: Indica si se debe iniciar el cliente
- **Caso de uso**: Deshabilitar clientes sin eliminar la configuración

#### Propiedades específicas del complemento

Estas propiedades solo las usan los complementos (no los clientes principales):

##### stopargs

- **Tipo**: Cadena (separada por espacios o tabulaciones)
- **Descripción**: Argumentos proporcionados para detener el cliente
- **Sustitución de variables**: Sí (ver más abajo)

##### uninstallargs

- **Tipo**: Cadena (separada por espacios o tabulaciones)
- **Descripción**: Argumentos utilizados para desinstalar el cliente
- **Sustitución de variables**: Sí (ver abajo)

##### ruta de clases

- **Tipo**: Cadena (rutas separadas por comas)
- **Descripción**: Elementos adicionales del classpath para el cliente
- **Sustitución de variables**: Sí (ver más abajo)

#### Sustitución de variables (solo complementos)

Las siguientes variables se sustituyen en `args`, `stopargs`, `uninstallargs` y `classpath` para los plugins:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Nota**: La sustitución de variables se realiza solo para los plugins, no para los clientes del núcleo.

#### Tipos de cliente

##### Clientes administrados

- El constructor se invoca con los parámetros `RouterContext` y `ClientAppManager`
- El cliente debe implementar la interfaz `ClientApp`
- Ciclo de vida controlado por el router
- Puede iniciarse, detenerse y reiniciarse dinámicamente

##### Clientes no gestionados

- Se invoca el método `main(String[] args)`
- Se ejecuta en un hilo separado
- Ciclo de vida no gestionado por el router
- Tipo de cliente heredado

#### Configuración de ejemplo

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Configuración del registro (logger.config)

**Ubicación**: `$I2P_CONFIG_DIR/logger.config`   **Interfaz de configuración**: consola del router en `/configlogging`

#### Referencia de propiedades

##### Configuración del búfer de la consola

###### logger.consoleBufferSize

- **Tipo**: Entero
- **Predeterminado**: 20
- **Descripción**: Cantidad máxima de mensajes de registro para almacenar en búfer en la consola
- **Rango**: 1-1000 recomendado

##### Formato de fecha y hora

###### logger.dateFormat

- **Tipo**: String (patrón de SimpleDateFormat)
- **Predeterminado**: Según la configuración regional del sistema
- **Ejemplo**: `HH:mm:ss.SSS`
- **Documentación**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Niveles de registro

###### logger.defaultLevel

- **Tipo**: Enumeración
- **Predeterminado**: ERROR
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descripción**: Nivel de registro predeterminado para todas las clases

###### logger.minimumOnScreenLevel

- **Tipo**: Enumeración
- **Predeterminado**: CRIT
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descripción**: Nivel mínimo para los mensajes mostrados en pantalla

###### logger.record.{class}

- **Tipo**: Enumeración
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descripción**: Anulación del nivel de registro por clase
- **Ejemplo**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Opciones de visualización

###### logger.displayOnScreen

- **Tipo**: Booleano
- **Predeterminado**: true
- **Descripción**: Si se deben mostrar los mensajes de registro en la salida de consola

###### logger.dropDuplicates

- **Tipo**: Booleano
- **Predeterminado**: true
- **Descripción**: Descartar mensajes de registro duplicados consecutivos

###### logger.dropOnOverflow

- **Tipo**: Booleano
- **Predeterminado**: false
- **Descripción**: Descartar mensajes cuando el búfer esté lleno (en lugar de bloquear)

##### Comportamiento de vaciado

###### logger.flushInterval

- **Tipo**: Entero (segundos)
- **Predeterminado**: 29
- **Desde**: Versión 0.9.18
- **Descripción**: Con qué frecuencia volcar el búfer de registro al disco

##### Configuración del formato

###### logger.format

- **Tipo**: Cadena (secuencia de caracteres)
- **Descripción**: Plantilla de formato de mensaje de registro
- **Caracteres de formato**:
  - `d` = fecha/hora
  - `c` = nombre de la clase
  - `t` = nombre del hilo
  - `p` = prioridad (nivel de registro)
  - `m` = mensaje
- **Ejemplo**: `dctpm` produce `[marca de tiempo] [clase] [hilo] [nivel] mensaje`

##### Compresión (Versión 0.9.56+)

###### logger.gzip

- **Tipo**: Booleano
- **Predeterminado**: false
- **Desde**: Versión 0.9.56
- **Descripción**: Habilitar la compresión gzip para los archivos de registro rotados

###### logger.minGzipSize

- **Tipo**: Entero (bytes)
- **Valor predeterminado**: 65536
- **Desde**: Versión 0.9.56
- **Descripción**: Tamaño mínimo de archivo para activar la compresión (64 KB por defecto)

##### Gestión de archivos

###### logger.logBufferSize

- **Tipo**: Entero (bytes)
- **Predeterminado**: 1024
- **Descripción**: Número máximo de mensajes en el búfer antes de vaciarlo

###### logger.logFileName

- **Tipo**: Cadena (ruta de archivo)
- **Predeterminado**: `logs/log-@.txt`
- **Descripción**: Patrón de nomenclatura del archivo de registro (`@` se reemplaza con el número de rotación)

###### logger.logFilenameOverride

- **Tipo**: Cadena (ruta de archivo)
- **Descripción**: Anulación del nombre del archivo de registro (desactiva el patrón de rotación)

###### logger.logFileSize

- **Tipo**: Cadena (tamaño con unidad)
- **Predeterminado**: 10M
- **Unidades**: K (kilobytes), M (megabytes), G (gigabytes)
- **Ejemplo**: `50M`, `1G`

###### logger.logRotationLimit

- **Tipo**: Entero
- **Predeterminado**: 2
- **Descripción**: Número de archivo de rotación más alto (desde log-0.txt hasta log-N.txt)

#### Ejemplo de configuración

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Configuración de complementos

#### Configuración individual del plugin (plugins/*/plugin.config)

**Ubicación**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Formato**: Formato estándar de los archivos de configuración de I2P   **Documentación**: [Especificación del plugin](/docs/specs/plugin/)

##### Propiedades obligatorias

###### nombre

- **Tipo**: Cadena
- **Obligatorio**: Sí
- **Descripción**: Nombre visible del plugin
- **Ejemplo**: `name=I2P Plugin Example`

###### clave

- **Tipo**: Cadena (clave pública)
- **Obligatorio**: Sí (omitir para plugins firmados con SU3)
- **Descripción**: Clave pública de firma del plugin para verificación
- **Formato**: Clave de firma codificada en Base64

###### firmante

- **Tipo**: Cadena
- **Requerido**: Sí
- **Descripción**: Identidad del firmante del plugin
- **Ejemplo**: `signer=user@example.i2p`

###### versión

- **Tipo**: Cadena (formato VersionComparator, comparador de versiones)
- **Obligatorio**: Sí
- **Descripción**: Versión del complemento para la comprobación de actualizaciones
- **Formato**: versionado semántico o formato comparable personalizado
- **Ejemplo**: `version=1.2.3`

##### Propiedades de pantalla

###### fecha

- **Tipo**: Long (Unix timestamp (marca de tiempo de Unix) en milisegundos)
- **Descripción**: Fecha de lanzamiento del plugin

###### autor

- **Tipo**: Cadena
- **Descripción**: Nombre del autor del complemento

###### websiteURL

- **Tipo**: Cadena (URL)
- **Descripción**: URL del sitio web del complemento

###### updateURL

- **Tipo**: Cadena (URL)
- **Descripción**: URL de verificación de actualizaciones del complemento

###### updateURL.su3

- **Tipo**: Cadena (URL)
- **Desde**: Versión 0.9.15
- **Descripción**: URL de actualización en formato SU3 (preferida)

###### descripción

- **Tipo**: Cadena
- **Descripción**: Descripción del complemento en inglés

###### description_{language}

- **Tipo**: Cadena
- **Descripción**: Descripción localizada del complemento
- **Ejemplo**: `description_de=Deutsche Beschreibung`

###### licencia

- **Tipo**: Cadena
- **Descripción**: Identificador de la licencia del complemento
- **Ejemplo**: `license=Apache 2.0`

##### Propiedades de instalación

###### no-iniciar-durante-la-instalación

- **Tipo**: Booleano
- **Predeterminado**: false
- **Descripción**: Impide el inicio automático después de la instalación

###### Se requiere reiniciar el router

- **Tipo**: Booleano
- **Predeterminado**: false
- **Descripción**: Requiere reiniciar el router después de la instalación

###### solo instalación

- **Tipo**: Boolean
- **Predeterminado**: false
- **Descripción**: Instalar solo una vez (sin actualizaciones)

###### solo actualización

- **Tipo**: Booleano
- **Predeterminado**: false
- **Descripción**: Actualizar solo la instalación existente (sin instalación nueva)

##### Ejemplo de configuración del complemento

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Configuración global de plugins (plugins.config)

**Ubicación**: `$I2P_CONFIG_DIR/plugins.config`   **Propósito**: Habilitar/deshabilitar complementos instalados a nivel global

##### Formato de propiedad

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Nombre del plugin según plugin.config
- `startOnLoad`: Indica si se debe iniciar el plugin al iniciar el router

##### Ejemplo

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Configuración de aplicaciones web (webapps.config)

**Ubicación**: `$I2P_CONFIG_DIR/webapps.config`   **Propósito**: Habilitar/deshabilitar y configurar aplicaciones web

#### Formato de la propiedad

##### webapps.{name}.startOnLoad

- **Tipo**: Booleano
- **Descripción**: Si iniciar la aplicación web al iniciar el router
- **Formato**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Tipo**: Cadena (rutas separadas por espacios o comas)
- **Descripción**: Elementos adicionales del classpath (ruta de clases de Java) para la aplicación web
- **Formato**: `webapps.{name}.classpath=[paths]`

#### Sustitución de variables

Las rutas permiten las siguientes sustituciones de variables:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Resolución del Classpath (ruta de clases)

- **Aplicaciones web del núcleo**: Rutas relativas a `$I2P/lib`
- **Aplicaciones web de complementos**: Rutas relativas a `$CONFIG/plugins/{appname}/lib`

#### Ejemplo de configuración

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Configuración del Router (router.config)

**Ubicación**: `$I2P_CONFIG_DIR/router.config`   **Interfaz de configuración**: Consola del router en `/configadvanced`   **Propósito**: Ajustes principales del router y parámetros de red

#### Categorías de configuración

##### Configuración de red

Configuración de ancho de banda:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Configuración del transporte:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Comportamiento del Router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Configuración de la consola

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Configuración de la hora

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Nota**: La configuración del router es extensa. Consulta la consola del router en `/configadvanced` para la referencia completa de propiedades.

---

## Archivos de configuración de aplicaciones

### Configuración de la libreta de direcciones (addressbook/config.txt)

**Ubicación**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Aplicación**: SusiDNS   **Propósito**: Resolución de nombres de host y gestión de la libreta de direcciones

#### Ubicaciones de archivos

##### router_addressbook

- **Predeterminado**: `../hosts.txt`
- **Descripción**: Libreta de direcciones principal (nombres de host a nivel del sistema)
- **Formato**: Formato estándar del archivo hosts

##### privatehosts.txt

- **Ubicación**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Descripción**: Asignaciones de nombres de host privados
- **Prioridad**: Máxima (anula todas las demás fuentes)

##### userhosts.txt

- **Ubicación**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Descripción**: Asignaciones de nombres de host añadidas por el usuario
- **Gestión**: A través de la interfaz de SusiDNS

##### hosts.txt

- **Ubicación**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Descripción**: Libreta de direcciones pública descargada
- **Fuente**: Fuentes de suscripción

#### Servicio de nombres

##### BlockfileNamingService (Predeterminado desde 0.8.8)

Formato de almacenamiento: - **Archivo**: `hostsdb.blockfile` - **Ubicación**: `$I2P_CONFIG_DIR/addressbook/` - **Rendimiento**: ~10x consultas más rápidas que hosts.txt - **Formato**: Formato de base de datos binario

Servicio de nombres heredado: - **Formato**: Texto plano hosts.txt - **Estado**: Obsoleto pero aún se admite - **Caso de uso**: Edición manual, control de versiones

#### Reglas de nombres de host

Los nombres de host de I2P deben cumplir con:

1. **Requisito de TLD (dominio de nivel superior)**: Debe terminar con `.i2p`
2. **Longitud máxima**: 67 caracteres en total
3. **Conjunto de caracteres**: `[a-z]`, `[0-9]`, `.` (punto), `-` (guion)
4. **Mayúsculas/minúsculas**: Solo minúsculas
5. **Restricciones de inicio**: No puede comenzar con `.` o `-`
6. **Patrones prohibidos**: No puede contener `..`, `.-` o `-.` (desde 0.6.1.33)
7. **Reservado**: Nombres de host Base32 `*.b32.i2p` (52 caracteres de base32.b32.i2p)

##### Ejemplos válidos

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Ejemplos no válidos

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Gestión de suscripciones

##### subscriptions.txt

- **Ubicación**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Formato**: Una URL por línea
- **Predeterminado**: `http://i2p-projekt.i2p/hosts.txt`

##### Formato de la fuente de suscripción (Desde 0.9.26)

Formato de canal avanzado con metadatos:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Propiedades de los metadatos: - `added`: Fecha en que se agregó el nombre de host (formato YYYYMMDD) - `src`: Identificador de origen - `sig`: Firma opcional

**Compatibilidad con versiones anteriores**: El formato simple hostname=destination sigue siendo admitido.

#### Ejemplo de configuración

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Configuración de I2PSnark (i2psnark.config.d/i2psnark.config)

**Ubicación**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Aplicación**: I2PSnark cliente BitTorrent   **Interfaz de configuración**: Interfaz web en http://127.0.0.1:7657/i2psnark

#### Estructura de directorios

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Configuración principal (i2psnark.config)

Configuración predeterminada mínima:

```properties
i2psnark.dir=i2psnark
```
Propiedades adicionales gestionadas a través de la interfaz web:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Configuración individual de torrent

**Ubicación**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Formato**: Configuración por torrent   **Gestión**: Automática (mediante la GUI web)

Las propiedades incluyen: - Configuración de subida/descarga específica del torrent - Prioridades de archivos - Información del rastreador - Límites de pares

**Nota**: La configuración de torrents se gestiona principalmente a través de la interfaz web. No se recomienda la edición manual.

#### Organización de datos de torrents

El almacenamiento de datos está separado de la configuración:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Configuración de I2PTunnel (i2ptunnel.config)

**Ubicación**: `$I2P_CONFIG_DIR/i2ptunnel.config` (legado) o `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (moderno)   **Interfaz de configuración**: Consola del Router en `/i2ptunnel`   **Cambio de formato**: Versión 0.9.42 (agosto de 2019)

#### Estructura de directorios (Versión 0.9.42+)

A partir de la versión 0.9.42, el archivo i2ptunnel.config se divide automáticamente:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Diferencia crítica de formato**: - **Formato monolítico**: Propiedades con el prefijo `tunnel.N.` - **Formato dividido**: Propiedades **SIN** prefijo (p. ej., `description=`, no `tunnel.0.description=`)

#### Comportamiento de migración

En la primera ejecución después de actualizar a la 0.9.42: 1. Se lee el i2ptunnel.config existente 2. Se crean configuraciones de tunnel individuales en i2ptunnel.config.d/ 3. Se eliminan los prefijos de las propiedades en los archivos divididos 4. Se realiza una copia de seguridad del archivo original 5. El formato heredado sigue siendo compatible para mantener la compatibilidad con versiones anteriores

#### Secciones de configuración

La configuración de I2PTunnel está documentada en detalle en la sección [Referencia de configuración de I2PTunnel](#i2ptunnel-configuration-reference) a continuación. Las descripciones de las propiedades son aplicables tanto al formato monolítico (`tunnel.N.property`) como al dividido (`property`).

---

## Referencia de configuración de I2PTunnel

Esta sección proporciona una referencia técnica completa de todas las propiedades de configuración de I2PTunnel. Las propiedades se muestran en formato dividido (sin el prefijo `tunnel.N.`). Para el formato monolítico, antepón a todas las propiedades el prefijo `tunnel.N.`, donde N es el número de tunnel.

**Importante**: Las propiedades descritas como `tunnel.N.option.i2cp.*` están implementadas en I2PTunnel y **NO** son compatibles a través de otras interfaces como el protocolo I2CP o SAM API.

### Propiedades básicas

#### tunnel.N.description (descripción)

- **Tipo**: Cadena
- **Contexto**: Todos los tunnels
- **Descripción**: Descripción del tunnel legible por humanos para mostrar en la interfaz de usuario
- **Ejemplo**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (nombre)

- **Tipo**: Cadena
- **Contexto**: Todos los tunnels
- **Obligatorio**: Sí
- **Descripción**: Identificador único de tunnel y nombre para mostrar
- **Ejemplo**: `name=I2P HTTP Proxy`

#### tunnel.N.type (type)

- **Tipo**: Enumeración
- **Contexto**: Todos los tunnels
- **Requerido**: Sí
- **Valores**:
  - `client` - Tunnel de cliente genérico
  - `httpclient` - Cliente de proxy HTTP
  - `ircclient` - Tunnel de cliente IRC
  - `socksirctunnel` - Proxy SOCKS para IRC
  - `sockstunnel` - Proxy SOCKS (versión 4, 4a, 5)
  - `connectclient` - Cliente de proxy CONNECT
  - `streamrclient` - Cliente de Streamr
  - `server` - Tunnel de servidor genérico
  - `httpserver` - Tunnel de servidor HTTP
  - `ircserver` - Tunnel de servidor IRC
  - `httpbidirserver` - Servidor HTTP bidireccional
  - `streamrserver` - Servidor de Streamr

#### tunnel.N.interface (interfaz)

- **Tipo**: Cadena (dirección IP o nombre de host)
- **Contexto**: Solo tunnels de cliente
- **Predeterminado**: 127.0.0.1
- **Descripción**: Interfaz local a la que vincular para conexiones entrantes
- **Nota de seguridad**: Vincular a 0.0.0.0 permite conexiones remotas
- **Ejemplo**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Tipo**: Entero
- **Contexto**: Solo para tunnels de cliente
- **Rango**: 1-65535
- **Descripción**: Puerto local en el que escuchar para conexiones de cliente
- **Ejemplo**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Tipo**: Cadena (dirección IP o nombre de host)
- **Contexto**: Solo Server tunnels (túneles de servidor)
- **Descripción**: Servidor local al que reenviar las conexiones
- **Ejemplo**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Tipo**: Entero
- **Contexto**: Solo para tunnels de servidor
- **Rango**: 1-65535
- **Descripción**: Puerto en targetHost al que conectarse
- **Ejemplo**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Tipo**: Cadena (destinos separados por comas o espacios)
- **Contexto**: Solo para tunnels de cliente
- **Formato**: `destination[:port][,destination[:port]]`
- **Descripción**: Destino(s) de I2P a los que conectarse
- **Ejemplos**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Tipo**: Cadena (dirección IP o nombre de host)
- **Predeterminado**: 127.0.0.1
- **Descripción**: Dirección de la interfaz I2CP del router I2P
- **Nota**: Se ignora cuando se ejecuta en el contexto del router
- **Ejemplo**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Tipo**: Entero
- **Predeterminado**: 7654
- **Rango**: 1-65535
- **Descripción**: Puerto I2CP del router I2P
- **Nota**: Se ignora cuando se ejecuta en contexto de router
- **Ejemplo**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Tipo**: Booleano
- **Valor predeterminado**: true
- **Descripción**: Indica si iniciar el tunnel cuando se carga I2PTunnel
- **Ejemplo**: `startOnLoad=true`

### Configuración del proxy

#### tunnel.N.proxyList (proxyList)

- **Tipo**: Cadena (nombres de host separados por comas o espacios)
- **Contexto**: Solo proxies HTTP y SOCKS
- **Descripción**: Lista de hosts de outproxy
- **Ejemplo**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Configuración del servidor

#### tunnel.N.privKeyFile (privKeyFile)

- **Tipo**: Cadena (ruta de archivo)
- **Contexto**: Servidores y tunnels de cliente persistentes
- **Descripción**: Archivo que contiene claves privadas de destino persistentes
- **Ruta**: Absoluta o relativa al directorio de configuración de I2P
- **Ejemplo**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Tipo**: Cadena (nombre de host)
- **Contexto**: Solo servidores HTTP
- **Predeterminado**: Nombre de host Base32 del destino
- **Descripción**: Valor del encabezado Host enviado al servidor local
- **Ejemplo**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Tipo**: Cadena (nombre de host)
- **Contexto**: Solo para servidores HTTP
- **Descripción**: Anulación del host virtual para un puerto de entrada específico
- **Caso de uso**: Alojar varios sitios en diferentes puertos
- **Ejemplo**: `spoofedHost.8080=site1.example.i2p`

### Opciones específicas del cliente

#### tunnel.N.sharedClient (sharedClient)

- **Tipo**: Booleano
- **Contexto**: Solo tunnels de cliente
- **Predeterminado**: false
- **Descripción**: Si varios clientes pueden compartir este tunnel
- **Ejemplo**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Tipo**: Booleano
- **Contexto**: Solo para Client tunnels
- **Predeterminado**: false
- **Descripción**: Almacenar y reutilizar las claves de destino entre reinicios
- **Conflicto**: Mutuamente excluyente con `i2cp.newDestOnResume=true`
- **Ejemplo**: `option.persistentClientKey=true`

### Opciones de I2CP (protocolo de cliente de I2P) (Implementación en I2PTunnel (herramienta de tunnel de I2P))

**Importante**: Estas propiedades llevan el prefijo `option.i2cp.` pero están implementadas en I2PTunnel, no en la capa del protocolo I2CP. No están disponibles a través de I2CP ni de las APIs de SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Tipo**: Booleano
- **Contexto**: Solo para tunnels de cliente
- **Predeterminado**: false
- **Descripción**: Retrasar la creación del tunnel hasta la primera conexión
- **Caso de uso**: Ahorrar recursos para tunnels que se usan rara vez
- **Ejemplo**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Tipo**: Booleano
- **Contexto**: Solo para tunnels de cliente
- **Predeterminado**: false
- **Requiere**: `i2cp.closeOnIdle=true`
- **Conflicto**: Mutuamente excluyente con `persistentClientKey=true`
- **Descripción**: Crear un nuevo destino tras el tiempo de espera por inactividad
- **Ejemplo**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Tipo**: Cadena (clave codificada en base64)
- **Contexto**: Solo tunnels de servidor
- **Descripción**: Clave de cifrado privada persistente de leaseset
- **Caso de uso**: Mantener un leaseset cifrado coherente entre reinicios
- **Ejemplo**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Tipo**: Cadena (sigtype:base64)
- **Contexto**: Solo para tunnels de servidor
- **Formato**: `sigtype:base64key`
- **Descripción**: Clave privada persistente para firmar el leaseSet (conjunto de arrendamientos)
- **Ejemplo**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Opciones específicas del servidor

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Tipo**: Booleano
- **Contexto**: Solo tunnels de servidor
- **Predeterminado**: false
- **Descripción**: Usar una IP local única por cada destino I2P remoto
- **Caso de uso**: Rastrear direcciones IP de clientes en los registros del servidor
- **Nota de seguridad**: Puede reducir el anonimato
- **Ejemplo**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Tipo**: Cadena (hostname:port)
- **Contexto**: Solo para tunnels de servidor
- **Descripción**: Sobrescribe targetHost/targetPort para el puerto entrante NNNN
- **Caso de uso**: Enrutamiento basado en puertos a diferentes servicios locales
- **Ejemplo**: `option.targetForPort.8080=localhost:8080`

### Configuración del grupo de subprocesos

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Tipo**: Booleano
- **Contexto**: Solo para tunnels de servidor
- **Predeterminado**: true
- **Descripción**: Usar un grupo de subprocesos para la gestión de conexiones
- **Nota**: Siempre false para servidores estándar (se ignora)
- **Ejemplo**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Tipo**: Entero
- **Contexto**: Solo para tunnels de servidor
- **Predeterminado**: 65
- **Descripción**: Tamaño máximo del grupo de subprocesos
- **Nota**: Se ignora para servidores estándar
- **Ejemplo**: `option.i2ptunnel.blockingHandlerCount=100`

### Opciones del cliente HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Tipo**: Booleano
- **Contexto**: solo clientes HTTP
- **Predeterminado**: false
- **Descripción**: Permitir conexiones SSL a direcciones .i2p
- **Ejemplo**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Tipo**: Booleano
- **Contexto**: solo clientes HTTP
- **Predeterminado**: false
- **Descripción**: Desactivar enlaces de address helper (asistente de direcciones) en las respuestas del proxy
- **Ejemplo**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Tipo**: Cadena (URLs separadas por comas o espacios)
- **Contexto**: Solo para clientes HTTP
- **Descripción**: URLs de servidores Jump (servidores de salto) para la resolución de nombres de host
- **Ejemplo**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Tipo**: Booleano
- **Contexto**: Solo clientes HTTP
- **Predeterminado**: false
- **Descripción**: Reenviar encabezados Accept-* (excepto Accept y Accept-Encoding)
- **Ejemplo**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Tipo**: Booleano
- **Contexto**: Solo clientes HTTP
- **Predeterminado**: false
- **Descripción**: Pasar encabezados Referer (cabecera HTTP de referencia) a través del proxy
- **Nota de privacidad**: Puede filtrar información
- **Ejemplo**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Tipo**: Booleano
- **Contexto**: Solo para clientes HTTP
- **Predeterminado**: false
- **Descripción**: Reenviar encabezados User-Agent a través del proxy
- **Nota de privacidad**: Puede filtrar información del navegador
- **Ejemplo**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Tipo**: Booleano
- **Contexto**: Solo para clientes HTTP
- **Predeterminado**: false
- **Descripción**: Pasar encabezados Via a través del proxy
- **Ejemplo**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Tipo**: Cadena (destinos separados por comas o espacios)
- **Contexto**: Solo clientes HTTP
- **Descripción**: Outproxies (proxies de salida) SSL dentro de la red para HTTPS
- **Ejemplo**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Tipo**: Booleano
- **Contexto**: Solo clientes HTTP
- **Valor predeterminado**: true
- **Descripción**: Usar complementos locales de outproxy (proxy de salida) registrados
- **Ejemplo**: `option.i2ptunnel.useLocalOutproxy=true`

### Autenticación del cliente HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Tipo**: Enum
- **Contexto**: solo clientes HTTP
- **Predeterminado**: false
- **Valores**: `true`, `false`, `basic`, `digest`
- **Descripción**: Requiere autenticación local para el acceso al proxy
- **Nota**: `true` es equivalente a `basic`
- **Ejemplo**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Tipo**: Cadena (hexadecimal en minúsculas de 32 caracteres)
- **Contexto**: solo clientes HTTP
- **Requiere**: `proxyAuth=basic` o `proxyAuth=digest`
- **Descripción**: Hash MD5 de la contraseña del usuario USER
- **En desuso**: Utilice SHA-256 en su lugar (0.9.56+)
- **Ejemplo**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Tipo**: Cadena (hexadecimal en minúsculas de 64 caracteres)
- **Contexto**: Solo clientes HTTP
- **Requiere**: `proxyAuth=digest`
- **Desde**: Versión 0.9.56
- **Estándar**: RFC 7616
- **Descripción**: Hash SHA-256 de la contraseña para el usuario USER
- **Ejemplo**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Autenticación del proxy de salida

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Tipo**: Booleano
- **Contexto**: Solo clientes HTTP
- **Predeterminado**: false
- **Descripción**: Enviar autenticación al outproxy (proxy de salida hacia Internet)
- **Ejemplo**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Tipo**: Cadena
- **Contexto**: Solo clientes HTTP
- **Requiere**: `outproxyAuth=true`
- **Descripción**: Nombre de usuario para la autenticación del proxy de salida
- **Ejemplo**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Tipo**: Cadena
- **Contexto**: Solo clientes HTTP
- **Requiere**: `outproxyAuth=true`
- **Descripción**: Contraseña para la autenticación de outproxy (proxy de salida)
- **Seguridad**: Almacenada en texto plano
- **Ejemplo**: `option.outproxyPassword=secret`

### Opciones del cliente SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Tipo**: Cadena (destinos separados por comas o espacios)
- **Contexto**: Solo para clientes SOCKS
- **Descripción**: Proxies de salida dentro de la red para puertos no especificados
- **Ejemplo**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Tipo**: Cadena (destinos separados por comas o espacios)
- **Contexto**: Solo clientes SOCKS
- **Descripción**: Proxies de salida dentro de la red específicamente para el puerto NNNN
- **Ejemplo**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Tipo**: Enumeración
- **Contexto**: Solo para clientes SOCKS
- **Predeterminado**: socks
- **Desde**: Versión 0.9.57
- **Valores**: `socks`, `connect` (HTTPS)
- **Descripción**: Tipo de outproxy (proxy de salida) configurado
- **Ejemplo**: `option.outproxyType=connect`

### Opciones del servidor HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Tipo**: Entero
- **Contexto**: Solo para servidores HTTP
- **Predeterminado**: 0 (sin límite)
- **Descripción**: Máximo de solicitudes POST desde un destino por cada postCheckTime
- **Ejemplo**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Tipo**: Entero
- **Contexto**: solo servidores HTTP
- **Predeterminado**: 0 (ilimitado)
- **Descripción**: Máximo de solicitudes POST desde todos los destinos por postCheckTime
- **Ejemplo**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Tipo**: Entero (segundos)
- **Contexto**: Solo servidores HTTP
- **Predeterminado**: 300
- **Descripción**: Ventana de tiempo para comprobar los límites de POST
- **Ejemplo**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Tipo**: Entero (segundos)
- **Contexto**: Solo servidores HTTP
- **Valor predeterminado**: 1800
- **Descripción**: Duración del bloqueo tras superar maxPosts para un único destino
- **Ejemplo**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Tipo**: Entero (segundos)
- **Contexto**: Solo servidores HTTP
- **Predeterminado**: 600
- **Descripción**: Duración del bloqueo tras superar maxTotalPosts
- **Ejemplo**: `option.postTotalBanTime=1200`

### Opciones de seguridad del servidor HTTP

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Tipo**: Booleano
- **Contexto**: Solo servidores HTTP
- **Predeterminado**: false
- **Descripción**: Rechaza conexiones aparentemente a través de un inproxy (puerta de entrada desde Internet a I2P)
- **Ejemplo**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Tipo**: Booleano
- **Contexto**: solo para servidores HTTP
- **Valor predeterminado**: false
- **Desde**: Versión 0.9.25
- **Descripción**: Rechaza las conexiones con el encabezado Referer
- **Ejemplo**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Tipo**: booleano
- **Contexto**: solo para servidores HTTP
- **Predeterminado**: false
- **Desde**: Versión 0.9.25
- **Requiere**: propiedad `userAgentRejectList`
- **Descripción**: Rechaza las conexiones cuyo User-Agent coincida
- **Ejemplo**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Tipo**: Cadena (cadenas de coincidencia separadas por comas)
- **Contexto**: Solo para servidores HTTP
- **Desde**: Versión 0.9.25
- **Mayúsculas/minúsculas**: Coincidencia sensible a mayúsculas y minúsculas
- **Especial**: "none" (desde 0.9.33) coincide con un User-Agent vacío
- **Descripción**: Lista de patrones de User-Agent a rechazar
- **Ejemplo**: `option.userAgentRejectList=Mozilla,Opera,none`

### Opciones del servidor IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Tipo**: Cadena (patrón de nombre de host)
- **Contexto**: Solo para servidores IRC
- **Predeterminado**: `%f.b32.i2p`
- **Marcadores**:
  - `%f` = Hash de destino base32 completo
  - `%c` = Hash de destino cloaked (enmascarado) (ver cloakKey)
- **Descripción**: Formato del nombre de host enviado al servidor IRC
- **Ejemplo**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Tipo**: Cadena (frase de contraseña)
- **Contexto**: Solo servidores IRC
- **Predeterminado**: Aleatorio por sesión
- **Restricciones**: Sin comillas ni espacios
- **Descripción**: Frase de contraseña para la ocultación consistente del nombre de host
- **Caso de uso**: Seguimiento persistente del usuario a través de reinicios/servidores
- **Ejemplo**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Tipo**: Enum (enumeración)
- **Contexto**: Solo para servidores IRC
- **Predeterminado**: user
- **Valores**: `user`, `webirc`
- **Descripción**: Método de autenticación para el servidor IRC
- **Ejemplo**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Tipo**: Cadena (contraseña)
- **Contexto**: solo para servidores IRC
- **Requiere**: `method=webirc`
- **Restricciones**: sin comillas ni espacios
- **Descripción**: Contraseña para la autenticación del protocolo WEBIRC
- **Ejemplo**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Tipo**: Cadena (dirección IP)
- **Contexto**: Solo para servidores IRC
- **Requiere**: `method=webirc`
- **Descripción**: Dirección IP suplantada para el protocolo WEBIRC
- **Ejemplo**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Configuración de SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Tipo**: Booleano
- **Predeterminado**: false
- **Contexto**: Todos los tunnels
- **Comportamiento**:
  - **Servidores**: Usar SSL para conexiones al servidor local
  - **Clientes**: Requerir SSL de los clientes locales
- **Ejemplo**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Tipo**: Cadena (ruta de archivo)
- **Contexto**: Solo tunnels de cliente
- **Predeterminado**: `i2ptunnel-(random).ks`
- **Ruta**: Relativa a `$(I2P_CONFIG_DIR)/keystore/` si no es absoluta
- **Generado automáticamente**: Se crea si no existe
- **Descripción**: Archivo de almacén de claves (keystore) que contiene la clave privada SSL
- **Ejemplo**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Tipo**: Cadena (contraseña)
- **Contexto**: Solo para tunnels de cliente
- **Predeterminado**: changeit
- **Generada automáticamente**: Contraseña aleatoria si se crea un nuevo almacén de claves
- **Descripción**: Contraseña del almacén de claves SSL
- **Ejemplo**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Tipo**: Cadena (alias)
- **Contexto**: Solo para tunnels de cliente
- **Generado automáticamente**: Se crea si se genera una clave nueva
- **Descripción**: Alias para la clave privada en el almacén de claves
- **Ejemplo**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Tipo**: Cadena (contraseña)
- **Contexto**: Solo tunnels de cliente
- **Generado automáticamente**: Contraseña aleatoria si se crea una clave nueva
- **Descripción**: Contraseña de la clave privada en el almacén de claves
- **Ejemplo**: `option.keyPassword=keypass123`

### Opciones genéricas de I2CP y de Streaming (transmisión de datos)

Todas las propiedades `tunnel.N.option.*` (no documentadas específicamente arriba) se pasan a través de la interfaz I2CP y la biblioteca de streaming, con el prefijo `tunnel.N.option.` eliminado.

**Importante**: Estas son independientes de las opciones específicas de I2PTunnel. Consulte: - [Especificación de I2CP](/docs/specs/i2cp/) - [Especificación de la biblioteca de Streaming](/docs/specs/streaming/)

Ejemplos de opciones de streaming:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Ejemplo completo de Tunnel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Historial de versiones y cronología de características

### Versión 0.9.10 (2013)

**Característica**: Compatibilidad con valores vacíos en archivos de configuración - Las claves con valores vacíos (`key=`) ahora se admiten - Antes se ignoraban o provocaban errores de análisis

### Versión 0.9.18 (2015)

**Característica**: Configuración del intervalo de vaciado del búfer del registro - Propiedad: `logger.flushInterval` (valor predeterminado: 29 segundos) - Reduce la E/S de disco manteniendo una latencia de registro aceptable

### Versión 0.9.23 (noviembre de 2015)

**Cambio importante**: Requisito mínimo: Java 7 - Finalizó el soporte para Java 6 - Necesario para seguir recibiendo actualizaciones de seguridad

### Versión 0.9.25 (2015)

**Características**: Opciones de seguridad del servidor HTTP - `tunnel.N.option.rejectReferer` - Rechazar conexiones que incluyan la cabecera Referer - `tunnel.N.option.rejectUserAgents` - Rechazar cabeceras User-Agent específicas - `tunnel.N.option.userAgentRejectList` - Patrones de User-Agent a rechazar - **Caso de uso**: Mitigar rastreadores y clientes no deseados

### Versión 0.9.33 (enero de 2018)

**Característica**: Filtrado de User-Agent mejorado - el valor de cadena "none" en `userAgentRejectList` coincide con un User-Agent vacío - Correcciones de errores adicionales para i2psnark, i2ptunnel, streaming, SusiMail

### Versión 0.9.41 (2019)

**Obsolescencia**: BOB Protocol (protocolo BOB de I2P) eliminado de Android - los usuarios de Android deben migrar a SAM (protocolo SAM de I2P) o I2CP

### Versión 0.9.42 (agosto de 2019)

**Cambio importante**: Separación de archivos de configuración - `clients.config` dividido en una estructura de directorios `clients.config.d/` - `i2ptunnel.config` dividido en una estructura de directorios `i2ptunnel.config.d/` - Migración automática en la primera ejecución tras la actualización - Permite el empaquetado modular y la gestión de plugins - El formato monolítico heredado sigue siendo compatible

**Funciones adicionales**: - Mejoras de rendimiento de SSU - Prevención de cruce entre redes (Propuesta 147) - Compatibilidad inicial con tipos de cifrado

### Versión 0.9.56 (2021)

**Características**: Mejoras de seguridad y de registro - `logger.gzip` - Compresión Gzip para archivos de registro rotados (predeterminado: false) - `logger.minGzipSize` - Tamaño mínimo para la compresión (predeterminado: 65536 bytes) - `tunnel.N.option.proxy.auth.USER.sha256` - Autenticación digest SHA-256 (RFC 7616) - **Seguridad**: SHA-256 reemplaza a MD5 para la autenticación digest

### Versión 0.9.57 (enero de 2023)

**Función**: Configuración del tipo de outproxy (proxy de salida) SOCKS - `tunnel.N.option.outproxyType` - Selecciona el tipo de outproxy (socks|connect) - Predeterminado: socks - Compatibilidad con HTTPS CONNECT para outproxies HTTPS

### Versión 2.6.0 (julio de 2024)

**Cambio incompatible**: I2P-over-Tor bloqueado - Ahora se rechazan las conexiones desde direcciones IP de nodos de salida de Tor - **Motivo**: Degrada el rendimiento de I2P, desperdicia recursos de los nodos de salida de Tor - **Impacto**: Se bloqueará a los usuarios que accedan a I2P a través de nodos de salida de Tor - Los relés que no son de salida y los clientes de Tor no se ven afectados

### Versión 2.10.0 (septiembre de 2025 - actualidad)

**Características principales**: - **Criptografía poscuántica** disponible (activación opcional mediante Hidden Service Manager) - **Compatibilidad con tracker UDP** para I2PSnark para reducir la carga del tracker - **Mejoras de estabilidad del Modo Oculto** para reducir el agotamiento de RouterInfo - Mejoras de red para routers congestionados - Atravesamiento UPnP/NAT mejorado - Mejoras en NetDB con eliminación agresiva de leaseset - Reducciones de observabilidad para eventos del router

**Configuración**: No se han añadido nuevas propiedades de configuración

**Próximo cambio crítico**: La próxima versión (probablemente 2.11.0 o 3.0.0) requerirá Java 17 o posterior

---

## Funciones en desuso y cambios incompatibles

### Obsolescencias críticas

#### Acceso a I2P sobre Tor (Versión 2.6.0+)

- **Estado**: BLOQUEADO desde julio de 2024
- **Impacto**: Se rechazan las conexiones procedentes de direcciones IP de nodos de salida de Tor
- **Motivo**: Degrada el rendimiento de la red I2P sin aportar beneficios de anonimato
- **Afecta**: Solo a los nodos de salida de Tor, no a los relés ni a los clientes normales de Tor
- **Alternativa**: Use I2P o Tor por separado, no combinados

#### Autenticación por resumen MD5

- **Estado**: Obsoleto (usar SHA-256)
- **Propiedad**: `tunnel.N.option.proxy.auth.USER.md5`
- **Motivo**: MD5 roto criptográficamente
- **Reemplazo**: `tunnel.N.option.proxy.auth.USER.sha256` (desde 0.9.56)
- **Cronología**: MD5 aún es compatible, pero se desaconseja

### Cambios en la arquitectura de configuración

#### Archivos de configuración monolíticos (Versión 0.9.42+)

- **Afectados**: `clients.config`, `i2ptunnel.config`
- **Estado**: Obsoleto en favor de una estructura de directorios separada
- **Migración**: Automática en la primera ejecución tras la actualización a la 0.9.42
- **Compatibilidad**: El formato heredado sigue funcionando (retrocompatible)
- **Recomendación**: Usa el formato dividido para nuevas configuraciones

### Requisitos de la versión de Java

#### Compatibilidad con Java 6

- **Finalizado**: Versión 0.9.23 (noviembre de 2015)
- **Mínimo**: Se requiere Java 7 desde la versión 0.9.23

#### Requisito de Java 17 (Próximamente)

- **Estado**: CAMBIO CRÍTICO INMINENTE
- **Objetivo**: Próximo lanzamiento mayor después de 2.10.0 (probablemente 2.11.0 o 3.0.0)
- **Mínimo actual**: Java 8
- **Acción requerida**: Prepararse para la migración a Java 17
- **Cronograma**: Se anunciará junto con las notas de la versión

### Características eliminadas

#### Protocolo BOB (Basic Open Bridge, puente abierto básico) (Android)

- **Eliminado**: Versión 0.9.41
- **Plataforma**: Solo Android
- **Alternativa**: protocolos SAM (interfaz para aplicaciones de I2P) o I2CP (protocolo de control para comunicarse con el router)
- **Escritorio**: BOB (puente básico para aplicaciones externas a I2P) sigue disponible en plataformas de escritorio

### Migraciones recomendadas

1. **Autenticación**: Migrar de autenticación digest (por resumen) con MD5 a digest con SHA-256
2. **Formato de configuración**: Migrar a una estructura de directorios dividida para clientes y tunnels
3. **Entorno de ejecución de Java**: Planificar la actualización a Java 17 antes de la próxima versión principal
4. **Integración con Tor**: No enrutar I2P a través de nodos de salida de Tor

---

## Referencias

### Documentación oficial

- [Especificación de configuración de I2P](/docs/specs/configuration/) - Especificación oficial del formato de archivo de configuración
- [Especificación de plugin de I2P](/docs/specs/plugin/) - Configuración y empaquetado de plugins
- [Estructuras comunes de I2P - Asignación de tipos](/docs/specs/common-structures/#type-mapping) - Formato de serialización de datos del protocolo
- [Formato de propiedades de Java](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Especificación del formato base

### Código fuente

- [Repositorio del Router Java de I2P](https://github.com/i2p/i2p.i2p) - Espejo en GitHub
- [Gitea de los desarrolladores de I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - Repositorio oficial del código fuente de I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Implementación de E/S de archivos de configuración

### Recursos de la comunidad

- [I2P Forum](https://i2pforum.net/) - Debates y soporte comunitarios activos
- [I2P Website](/) - Sitio web oficial del proyecto

### Documentación de la API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - Documentación de la API para métodos de archivos de configuración

### Estado de la especificación

- **Última actualización de la especificación**: enero de 2023 (Versión 0.9.57)
- **Versión actual de I2P**: 2.10.0 (septiembre de 2025)
- **Precisión técnica**: la especificación se mantiene precisa hasta la 2.10.0 (sin cambios que rompan la compatibilidad)
- **Mantenimiento**: documento vivo, se actualiza cuando se modifica el formato de configuración
