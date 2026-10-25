---
title: "Especificación de Plugin"
description: "Reglas de empaquetado .xpi2p / .su3 para plugins de I2P"
slug: "plugin"
aliases:
  - "/es/plugin_spec"
  - "/es/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Resumen

Este documento especifica un formato de archivo .xpi2p (como el .xpi de Firefox), pero con un archivo de descripción plugin.config simple en lugar de un archivo XML install.rdf. Este formato de archivo se utiliza tanto para las instalaciones iniciales de plugins como para las actualizaciones de plugins.

Además, este documento proporciona una breve descripción general de cómo el router instala plugins, y políticas y pautas para desarrolladores de plugins.

El formato básico de archivo .xpi2p es el mismo que un archivo i2pupdate.sud (el formato usado para las actualizaciones del router), pero el instalador permitirá al usuario instalar el complemento incluso si aún no conoce la clave del firmante.

A partir de la versión 0.9.15, se admite el formato de archivo SU3 y es el preferido. Este formato permite claves de firma más seguras.

> **Nota:** Ya no recomendamos distribuir plugins en el formato xpi2p. Usa el formato su3.

La estructura de directorios estándar permitirá a los usuarios instalar los siguientes tipos de complementos:

- Aplicaciones web de consola
- Nuevo eepsite con cgi-bin, aplicaciones web
- Temas de consola
- Traducciones de consola
- Programas Java
- Programas Java en una JVM separada
- Cualquier script de shell o programa

Un plugin instala todos sus archivos en `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` en Windows). El instalador evitará la instalación en cualquier otro lugar, aunque el plugin puede acceder a bibliotecas en otros sitios cuando esté ejecutándose.

Esto debe verse únicamente como una forma de facilitar la instalación, desinstalación y actualización, y de reducir los conflictos básicos entre plugins.

Sin embargo, esencialmente no hay un modelo de seguridad una vez que el plugin está ejecutándose. El plugin se ejecuta en la misma JVM y con los mismos permisos que el router, y tiene acceso completo al sistema de archivos, al router, a la ejecución de programas externos, etc.

## Detalles

foo.xpi2p es un archivo de actualización firmada (sud) que contiene lo siguiente:

Encabezado .sud estándar antepuesto al archivo zip, que contiene lo siguiente:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Archivo Zip que contiene lo siguiente:

### archivo plugin.config

Este archivo es obligatorio. Es un archivo de configuración estándar de I2P que contiene las siguientes propiedades:

#### Propiedades Requeridas

Las siguientes cuatro son propiedades requeridas. Las primeras tres deben ser idénticas a las del plugin instalado para un plugin de actualización.

-   **name** - Se instalará en este nombre de directorio. Para plugins nativos, es posible que desees nombres separados en diferentes paquetes - foo-windows y foo-linux, por ejemplo.
-   **key** - Clave pública DSA como 172 caracteres B64 terminando en '='. Omite para formato SU3.
-   **signer** - se recomienda tunombre@mail.i2p
-   **version** - Debe estar en un formato que VersionComparator pueda analizar, ej. 1.2.3-4. 16 bytes máximo (debe coincidir con la versión sud). Los separadores de números válidos son '.', '-', y '_'. Esto debe ser mayor que el del plugin instalado para un plugin de actualización.

#### Propiedades de Visualización

Los valores de las siguientes propiedades se muestran en /configplugins en la consola del router si están presentes:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` recomendado
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - El verificador de actualizaciones revisará los bytes 41-56 en esta URL para determinar si hay una versión más nueva disponible. A partir de la versión 1.7.0 (0.9.53), es posible usar las variables `$OS` y `$ARCH` en la URL. No recomendado. No usar a menos que hayas distribuido previamente plugins en formato xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - La ubicación del archivo de actualización en formato su3, desde la versión 0.9.15. A partir de la versión 1.7.0 (0.9.53), es posible usar las variables `$OS` y `$ARCH` en la URL.
-   **description** - en inglés
-   **description_xx** - para el idioma xx
-   **license** - La licencia del plugin
-   **disableStop=true** - Por defecto false. Si es true, no se mostrará el botón de detener. Usar esto si no hay webapps ni clientes con stopargs.

#### Propiedades de los Enlaces de la Barra de Resumen de la Consola

Las siguientes propiedades se utilizan para agregar un enlace en la barra de resumen de la consola:

-   **consoleLinkName** - será añadido a la barra de resumen
-   **consoleLinkName_xx** - para el idioma xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - soportado desde 0.7.12-6
-   **consoleLinkTooltip_xx** - idioma xx desde 0.7.12-6

#### Propiedades del Icono de Consola

Las siguientes propiedades opcionales pueden usarse para añadir un icono personalizado en la consola:

-   **console-icon** - compatible desde 0.9.20. Solo para webapps. Una ruta a una imagen de 32x32, ej. /icon.png. Desde 1.7.0 (API 0.9.53), si se especifica consoleLinkURL, la ruta es relativa a esa URL. De lo contrario es relativa al nombre de la webapp. Se aplica a todas las webapps en el plugin.
-   **icon-code** - compatible desde 0.9.25. Proporciona un icono de consola para plugins sin recursos web. Una cadena B64 producida llamando `net.i2p.data.Base64 encode FILE` en un archivo de imagen png de 32x32.

#### Propiedades del Instalador

Las siguientes propiedades son utilizadas por el instalador de plugins:

-   **type** - app/theme/locale/webapp/... (sin implementar, probablemente no necesario)
-   **min-i2p-version** - La versión mínima de I2P que requiere este plugin
-   **max-i2p-version** - La versión máxima de I2P en la que funcionará este plugin
-   **min-java-version** - La versión mínima de Java que requiere este plugin
-   **min-jetty-version** - soportado desde 0.8.13, usar 6 para webapps de Jetty 6
-   **max-jetty-version** - soportado desde 0.8.13, usar 5.99999 para webapps de Jetty 5
-   **required-platform-OS** - sin implementar - quizás solo se mostrará, no se verificará
-   **other-requirements** - sin implementar, ej. python x.y - no verificado por el instalador, solo se muestra al usuario
-   **dont-start-at-install=true** - Por defecto falso. No iniciará el plugin cuando se instale o actualice.
-   **router-restart-required=true** - Por defecto falso. Esto no reinicia el router o el plugin en una actualización, solo informa al usuario que se requiere un reinicio.
-   **update-only=true** - Por defecto falso. Si es verdadero, fallará si no existe una instalación.
-   **install-only=true** - Por defecto falso. Si es verdadero, fallará si existe una instalación.
-   **min-installed-version** - para actualizar, si existe una instalación
-   **max-installed-version** - para actualizar, si existe una instalación
-   **depends=plugin1,plugin2,plugin3** - sin implementar
-   **depends-version=0.3.4,,5.6.7** - sin implementar

#### Propiedades de Traducción

-   **langs=xx,yy,Klingon,...** - (no implementado) (yy es la bandera del país)

### Directorios y Archivos de la Aplicación

Cada uno de los siguientes directorios o archivos es opcional, pero algo debe estar ahí o no hará nada:

**console/**

-   **locale/** - Solo jars que contengan nuevos paquetes de recursos (traducciones) para aplicaciones en la instalación base de I2P. Los paquetes para este plugin deben ir dentro de console/webapp/foo.war o lib/foo.jar
-   **themes/** - Nuevos temas para la consola del router. Coloca cada tema en un subdirectorio.
-   **webapps/** - (Ver notas importantes a continuación sobre webapps) .wars - Estos se ejecutarán en el momento de la instalación a menos que se desactiven en webapps.config. El nombre del war no tiene que ser el mismo que el nombre del plugin. No dupliques nombres de war en la instalación base de I2P.
-   **webapps.config** - Mismo formato que el webapps.config del router. También se usa para especificar jars adicionales en $PLUGIN/lib/ o $I2P/lib para el classpath de la webapp, con `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Nota:** Antes de la versión 1.7.0 (API 0.9.53), la línea classpath solo se cargaba si el warname era el mismo que el nombre del plugin. A partir de la API 0.9.53, la configuración classpath funcionará para cualquier warname.

> **Nota:** Antes de la versión 0.7.12-9 del router, el router buscaba `plugin.warname.startOnLoad` en lugar de `webapps.warname.startOnLoad`. Para compatibilidad con versiones más antiguas del router, un plugin que desee desactivar un war debería incluir ambas líneas.

**eepsite/**

(Ver notas importantes a continuación sobre eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - El instalador tendrá que hacer sustitución de variables aquí para establecer la ruta. La ubicación y el nombre de este archivo realmente no importa, siempre que esté configurado en clients.config - puede ser más conveniente estar un nivel arriba desde aquí.

**lib/**

Coloca cualquier archivo jar aquí, y especifícalos en una línea de classpath en console/webapps.config y/o clients.config

### archivo clients.config

Este archivo es opcional y especifica los clientes que se ejecutarán cuando se inicie un plugin. Utiliza el mismo formato que el archivo clients.config del router. Consulta la especificación del archivo de configuración clients.config para obtener más información sobre el formato y detalles importantes sobre cómo se inician y detienen los clientes.

-   **clientApp.0.stopargs=foo bar stop baz** - Si está presente, la clase será llamada con estos argumentos para detener el cliente. Todas las tareas de detención se llaman sin demora. Nota: El router no puede determinar si tus clientes no administrados están ejecutándose o no.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Si está presente, la clase será llamada con estos argumentos justo antes de eliminar $PLUGIN. Todas las tareas de desinstalación se llaman sin demora.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - El ejecutor de plugins realizará sustitución de variables en las líneas args y stopargs como sigue:
    -   `$I2P` - directorio de instalación base de I2P
    -   `$CONFIG` - directorio de configuración de I2P (típicamente ~/.i2p)
    -   `$PLUGIN` - directorio de instalación de este plugin (típicamente ~/.i2p/plugins/appname)
    -   `$OS` - el sistema operativo host en la forma `windows`, `linux`, `mac`
    -   `$ARCH` - la arquitectura host en la forma `386`, `amd64`, `arm64`

(Ver notas importantes a continuación sobre la ejecución de scripts de shell o programas externos)

## Tareas del Instalador de Plugins

Esto enumera lo que sucede cuando I2P instala un plugin.

1.  Se descarga el archivo .xpi2p.
2.  Se verifica la firma .sud contra las claves almacenadas. A partir de la versión 0.9.14.1, si no hay una clave que coincida, la instalación falla, a menos que se configure una propiedad avanzada del router para permitir todas las claves.
3.  Verificar la integridad del archivo zip.
4.  Extraer el archivo plugin.config.
5.  Verificar la versión de I2P, para asegurar que el plugin funcionará.
6.  Verificar que las webapps no dupliquen las aplicaciones $I2P existentes.
7.  Detener el plugin existente (si está presente).
8.  Verificar que el directorio de instalación no exista aún si update=false, o preguntar para sobrescribir.
9.  Verificar que el directorio de instalación sí exista si update=true, o preguntar para crear.
10. Descomprimir el plugin en appDir/plugins/name/
11. Añadir el plugin a plugins.config

## Tareas Iniciales de Plugin

Esto enumera lo que sucede cuando se inician los plugins. Primero, se verifica plugins.config para ver qué plugins necesitan ser iniciados. Para cada plugin:

1.  Verificar clients.config, y cargar e iniciar cada elemento (agregar los jars configurados al classpath).
2.  Verificar console/webapp y console/webapp.config. Cargar e iniciar los elementos requeridos (agregar los jars configurados al classpath).
3.  Agregar console/locale/foo.jar al classpath de traducciones si está presente.
4.  Agregar console/theme a la ruta de búsqueda de temas si está presente.
5.  Agregar el enlace de la barra de resumen.

## Notas de la Aplicación Web de Consola

Las webapps de consola con tareas en segundo plano deben implementar un ServletContextListener (ver seedless o i2pbote como ejemplos), o sobrescribir destroy() en el servlet, para que puedan ser detenidas. A partir de la versión 0.7.12-3 del router, las webapps de consola siempre serán detenidas antes de ser reiniciadas, por lo que no necesitas preocuparte por múltiples instancias, siempre que hagas esto. También a partir de la versión 0.7.12-3 del router, las webapps de consola serán detenidas al apagar el router.

No incluyas los archivos jar de bibliotecas en la webapp; ponlos en lib/ y coloca un classpath en webapps.config. Entonces puedes crear plugins separados de instalación y actualización, donde el plugin de actualización no contenga los archivos jar de bibliotecas.

Nunca incluyas Jetty, Tomcat o archivos jar de servlet en tu plugin, ya que pueden entrar en conflicto con la versión de la instalación I2P. Ten cuidado de no incluir ninguna biblioteca que pueda generar conflictos.

No incluyas archivos .java o .jsp; de lo contrario, Jetty los recompilará durante la instalación, lo que aumentará el tiempo de inicio. Aunque la mayoría de las instalaciones de I2P tendrán un compilador de Java y JSP funcional en el classpath, esto no está garantizado y puede no funcionar en todos los casos.

Por ahora, una webapp que necesite agregar archivos de classpath en $PLUGIN debe tener el mismo nombre que el plugin. Por ejemplo, una webapp en el plugin foo debe llamarse foo.war.

Aunque I2P ha soportado Servlet 3.0 desde la versión 0.9.30 de I2P, NO soporta el escaneo de anotaciones para @WebContent (sin archivo web.xml). Se requerirían varios jars de tiempo de ejecución adicionales, y no los proporcionamos en una instalación estándar. Contacta a los desarrolladores de I2P si necesitas soporte para @WebContent.

## Notas sobre Eepsite

No está claro cómo hacer que un plugin se instale en un eepsite existente. El router no tiene conexión con el eepsite, y puede o no estar ejecutándose, y puede haber más de uno. Es mejor iniciar tu propia instancia de Jetty e instancia de I2PTunnel, para un eepsite completamente nuevo.

Puede instanciar un nuevo I2PTunnel (algo parecido a lo que hace el CLI de i2ptunnel), pero por supuesto no aparecerá en la interfaz gráfica de i2ptunnel, esa es una instancia diferente. Pero eso está bien. Entonces puedes iniciar y detener i2ptunnel y jetty juntos.

Por lo tanto, no cuentes con que el router fusione automáticamente esto con algún eepsite existente. Probablemente no sucederá. Inicia un nuevo I2PTunnel y Jetty desde clients.config. Los mejores ejemplos de esto son los plugins zzzot y pebble.

¿Cómo conseguir la sustitución de rutas en jetty.xml? Ver los plugins zzzot y pebble como ejemplos.

## Notas de Inicio/Parada del Cliente

A partir de la versión 0.9.4, el router soporta clientes de plugin "gestionados". Los clientes de plugin gestionados son instanciados e iniciados por el `ClientAppManager`. El ClientAppManager mantiene una referencia al cliente y recibe actualizaciones sobre el estado del cliente. Se prefieren los clientes de plugin gestionados, ya que es mucho más fácil implementar el seguimiento de estado y arrancar y detener un cliente. También es mucho más fácil evitar referencias estáticas en el código del cliente que podrían llevar a un uso excesivo de memoria después de que se detenga un cliente. Consulta la especificación del archivo de configuración clients.config para más información sobre cómo escribir un cliente gestionado.

Para clientes de plugin "no administrados", el router no tiene forma de monitorear el estado de los clientes iniciados a través de clients.config. El autor del plugin debe manejar múltiples llamadas de inicio o parada de manera elegante, si es posible, manteniendo una tabla de estado estático, o usando archivos PID, etc. Evite el registro de logs o excepciones en múltiples inicios o paradas. Esto también aplica para una llamada de parada sin un inicio previo. A partir de la versión 0.7.12-3 del router, los plugins se detendrán al apagar el router, lo que significa que todos los clientes con stopargs en clients.config serán llamados, hayan sido iniciados previamente o no.

## Notas sobre Scripts de Shell y Programas Externos

Para ejecutar scripts de shell u otros programas externos, escribe una pequeña clase Java que verifique el tipo de sistema operativo, luego ejecute ShellCommand en el archivo .bat o .sh que proporciones. Se añadió una solución generalizada para esto en I2P 1.7.0/0.9.53, el "ShellService" que realiza seguimiento de estado para un solo comando y se comunica con el ClientAppManager.

Los programas externos no se detendrán cuando el router se detenga, y una segunda copia se iniciará cuando el router arranque. Esto generalmente puede mitigarse usando un ShellService para realizar el seguimiento de estado. Si eso no es adecuado para tu caso de uso, podrías escribir una clase wrapper o script de shell que haga el almacenamiento usual del PID en un archivo PID, y verificarlo al iniciar.

## Otras Pautas para Plugins

-   Consulta la rama monotone de i2p.scripts o cualquiera de los plugins de ejemplo en la página de zzz para obtener el script de shell makeplugin.sh. Esto automatiza la mayoría de las tareas para la generación de claves, creación de archivos su3 del plugin y verificación. Deberías incorporar este script en tu proceso de construcción del plugin.
-   Se recomienda encarecidamente Pack200 para jars y wars en plugins, generalmente reduce los plugins en un 60-65%. Consulta cualquiera de los plugins de ejemplo en la página de zzz para ver un ejemplo. El desempaquetado Pack200 es compatible con routers 0.7.11-5 o superior, que son esencialmente todos los routers que soportan plugins.
-   Los plugins no deben intentar escribir en ningún lugar de $I2P ya que puede ser de solo lectura, y de todos modos no es una buena política.
-   Los plugins pueden escribir en $CONFIG pero se recomienda mantener archivos solo en $PLUGIN. Todos los archivos en $PLUGIN serán eliminados al desinstalar.
-   $CWD puede estar en cualquier lugar; no asumas que está en un lugar particular, no intentes leer o escribir archivos relativos a $CWD. Para un ShellService, siempre es lo mismo que $PLUGIN.
-   Los programas Java deben averiguar dónde están con los getters de directorio en I2PAppContext.
-   El directorio del plugin es `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, o coloca un argumento $PLUGIN en la línea args en clients.config.
-   Todos los archivos de configuración deben estar en UTF-8.
-   Para ejecutar en una JVM separada, usa ShellCommand con `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Como alternativa a stopargs en clients.config, un cliente Java puede registrar un hook de cierre con `I2PAppContext.addShutdownTask()`. Pero esto no cerraría un plugin al actualizar, por lo que se recomienda stopargs. Además, establece todos los hilos creados en modo daemon.
-   No incluyas clases que dupliquen las de la instalación estándar. Extiende las clases si es necesario.
-   Ten cuidado con las diferentes definiciones de classpath en wrapper.config entre instalaciones antiguas y nuevas.
-   Los clientes rechazarán claves duplicadas con diferentes nombres de clave, y nombres de clave duplicados con diferentes claves, y diferentes claves o nombres de clave en paquetes de actualización. Protege tus claves. Solo las generes una vez.
-   No modifiques el archivo plugin.config en tiempo de ejecución ya que será sobrescrito en la actualización. Usa un archivo de configuración diferente en el directorio para almacenar la configuración en tiempo de ejecución.
-   En general, los plugins no deberían requerir acceso a $I2P/lib/router.jar. No accedas a clases del router, a menos que estés haciendo algo especial.
-   Como cada versión debe ser mayor que la anterior, podrías mejorar tu script de construcción para agregar un número de construcción al final de la versión.
-   Los plugins nunca deben llamar a `System.exit()`.
-   Por favor respeta las licencias cumpliendo los requisitos de licencia para cualquier software que incluyas.
-   El router establece la zona horaria de la JVM en UTC. Si un plugin necesita conocer la zona horaria real del usuario, está almacenada por el router en la propiedad I2PAppContext `i2p.systemTimeZone`.

## Classpaths

Los siguientes archivos jar en $I2P/lib se pueden asumir que están en el classpath estándar para todas las instalaciones de I2P, sin importar qué tan antigua o nueva sea la instalación original.

Todas las APIs públicas recientes en los jars de i2p tienen el número de versión desde-lanzamiento especificado en los Javadocs. Si tu plugin requiere ciertas características que solo están disponibles en versiones recientes, asegúrate de establecer las propiedades min-i2p-version, min-jetty-version, o ambas, en el archivo plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Los siguientes jars en $I2P/lib se puede asumir que están presentes en todas las instalaciones de I2P, sin importar qué tan antigua o nueva sea la instalación original, pero no necesariamente están en el classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Cualquier cosa no listada arriba puede no estar presente en el classpath de todos, incluso si la tienes en el classpath en TU versión de i2p. Si necesitas algún jar no listado arriba, añade $I2P/lib/foo.jar al classpath especificado en clients.config o webapps.config en tu plugin.

Anteriormente, una entrada de classpath especificada en clients.config se agregaba al classpath para toda la JVM. Sin embargo, a partir de la versión 0.7.13-3, esto se corrigió usando cargadores de clases, y ahora, como se pretendía originalmente, el classpath especificado en clients.config es solo para el hilo particular. Por lo tanto, especifique el classpath completo requerido para cada cliente.

## Notas sobre la Versión de Java

I2P ha requerido Java 7 desde la versión 0.9.24 (enero de 2016). I2P ha requerido Java 6 desde la versión 0.9.12 (abril de 2014). Cualquier usuario de I2P en la última versión debería estar ejecutando una JVM 1.7 (7.0).

Si tu plugin **no requiere 1.7**:

-   Asegúrese de que todos los archivos java y jsp estén compilados con source="1.6" target="1.6".
-   Asegúrese de que todos los jars de bibliotecas incluidos también sean para 1.6 o inferior.

Si tu plugin **requiere 1.7**:

-   Ten en cuenta que en tu página de descarga.
-   Añade min-java-version=1.7 a tu plugin.config

En cualquier caso, **debes** establecer un bootclasspath al compilar con Java 8 para prevenir fallos en tiempo de ejecución.

## La JVM Se Bloquea Al Actualizar

Nota: todo esto debería estar solucionado ahora.

La JVM tiene tendencia a bloquearse al actualizar archivos jar en un plugin si ese plugin estuvo ejecutándose desde que se inició I2P (incluso si el plugin fue detenido posteriormente). Esto puede haber sido solucionado con la implementación del cargador de clases en la versión 0.7.13-3, pero puede que no.

Lo más seguro es diseñar tu plugin con el jar dentro del war (para una aplicación web), o requerir un reinicio después de la actualización, o no actualizar los jars en tu plugin.

Debido a la forma en que funcionan los class loaders dentro de una webapp, _puede_ ser seguro tener jars externos si especificas el classpath en webapps.config. Se requieren más pruebas para verificar esto. No especifiques el classpath con un cliente 'falso' en clients.config si solo se necesita para una webapp - usa webapps.config en su lugar.

Lo menos seguro, y aparentemente la fuente de la mayoría de fallos, son los clientes con jars de plugins especificados en el classpath en clients.config.

Nada de esto debería ser un problema en la instalación inicial - nunca deberías tener que requerir un reinicio para una instalación inicial de un plugin.

## Referencias

-   [Especificación del Archivo de Configuración](/docs/specs/configuration)
-   [Criptografía DSA](/docs/specs/cryptography#DSA)
-   [Especificación de Actualizaciones](/docs/specs/updates)
