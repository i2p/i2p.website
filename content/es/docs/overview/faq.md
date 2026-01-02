---
title: "Preguntas Frecuentes"
description: "Preguntas frecuentes completas sobre I2P: ayuda del router, configuración, reseeds, privacidad/seguridad, rendimiento y solución de problemas"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Ayuda del Router I2P

### ¿En qué sistemas funcionará I2P? {#systems}

I2P está escrito en el lenguaje de programación Java. Ha sido probado en Windows, Linux, FreeBSD y OSX. También está disponible una versión para Android.

En términos de uso de memoria, I2P está configurado para utilizar 128 MB de RAM por defecto. Esto es suficiente para navegación y uso de IRC. Sin embargo, otras actividades pueden requerir una mayor asignación de memoria. Por ejemplo, si se desea ejecutar un router de alto ancho de banda, participar en torrents de I2P o servir hidden services de alto tráfico, se requiere una mayor cantidad de memoria.

En términos de uso de CPU, I2P ha sido probado para funcionar en sistemas modestos como la gama de computadoras de placa única Raspberry Pi. Como I2P hace un uso intensivo de técnicas criptográficas, una CPU más potente estará mejor preparada para manejar la carga de trabajo generada por I2P, así como las tareas relacionadas con el resto del sistema (es decir, sistema operativo, interfaz gráfica, otros procesos, por ejemplo, navegación web).

Se recomienda usar Sun/Oracle Java u OpenJDK.

### ¿Es necesario instalar Java para usar I2P? {#java}

Sí, se requiere Java para usar I2P Core. Incluimos Java dentro de nuestros instaladores fáciles para Windows, Mac OSX y Linux. Si estás ejecutando la aplicación I2P para Android, también necesitarás un entorno de ejecución de Java como Dalvik o ART instalado en la mayoría de los casos.

### ¿Qué es un "I2P Site" y cómo configuro mi navegador para poder usarlos? {#I2P-Site}

Un Sitio I2P es un sitio web normal excepto que está alojado dentro de I2P. Los sitios I2P tienen direcciones que parecen direcciones normales de internet, terminando en ".i2p" de una manera legible para humanos y no criptográfica, para el beneficio de las personas. En realidad, conectarse a un Sitio I2P requiere criptografía, lo que significa que las direcciones de Sitios I2P también son los largos Destinations "Base64" y las direcciones "B32" más cortas. Es posible que necesites realizar configuración adicional para navegar correctamente. Navegar Sitios I2P requerirá activar el Proxy HTTP en tu instalación de I2P y luego configurar tu navegador para usarlo. Para más información, consulta la sección "Navegadores" a continuación o la Guía de "Configuración del Navegador".

### ¿Qué significan los números Activos x/y en la consola del router? {#active}

En la página de Peers en tu consola del router, puedes ver dos números - Activos x/y. El primer número es la cantidad de peers a los que has enviado o de los que has recibido un mensaje en los últimos minutos. El segundo número es la cantidad de peers vistos recientemente, este siempre será mayor o igual que el primer número.

### Mi router tiene muy pocos pares activos, ¿está bien esto? {#peers}

Sí, esto puede ser normal, especialmente cuando el router acaba de iniciarse. Los routers nuevos necesitarán tiempo para arrancar y conectarse al resto de la red. Para ayudar a mejorar la integración en la red, el tiempo de actividad y el rendimiento, revisa estas configuraciones:

- **Compartir ancho de banda** - Si un router está configurado para compartir ancho de banda, enrutará más tráfico para otros routers, lo que ayuda a integrarlo con el resto de la red, así como a mejorar el rendimiento de la conexión local. Esto puede configurarse en la página [http://localhost:7657/config](http://localhost:7657/config).
- **Interfaz de red** - Asegúrate de que no haya una interfaz especificada en la página [http://localhost:7657/confignet](http://localhost:7657/confignet). Esto puede reducir el rendimiento a menos que tu computadora tenga múltiples interfaces con varias direcciones IP externas.
- **Protocolo I2NP** - Asegúrate de que el router esté configurado para esperar conexiones en un protocolo válido para el sistema operativo del host y configuraciones de red vacías (Avanzado). No ingreses una dirección IP en el campo 'Nombre de host' en la página de configuración de red. El protocolo I2NP que selecciones aquí solo se utilizará si aún no tienes una dirección accesible. La mayoría de las conexiones inalámbricas 4G y 5G de Verizon en Estados Unidos, por ejemplo, bloquean UDP y no se puede acceder a través de él. Otros usarían UDP de manera forzada incluso si está disponible para ellos. Elige una configuración razonable de los protocolos I2NP listados.

### Me opongo a ciertos tipos de contenido. ¿Cómo evito distribuirlos, almacenarlos o acceder a ellos? {#badcontent}

No hay ninguno de estos materiales instalado por defecto. Sin embargo, dado que I2P es una red peer-to-peer (entre pares), es posible que encuentres contenido prohibido por accidente. Aquí hay un resumen de cómo I2P te protege de estar involucrado innecesariamente en violaciones de tus creencias.

- **Distribución** - El tráfico es interno a la red I2P, no eres un [nodo de salida](#exit) (referido como outproxy en nuestra documentación).
- **Almacenamiento** - La red I2P no realiza almacenamiento distribuido de contenido, esto debe ser instalado y configurado específicamente por el usuario (con Tahoe-LAFS, por ejemplo). Esa es una característica de una red anónima diferente, [Freenet](http://freenetproject.org/). Al ejecutar un router I2P, no estás almacenando contenido para nadie.
- **Acceso** - Tu router no solicitará ningún contenido sin tu instrucción específica para hacerlo.

### ¿Es posible bloquear I2P? {#blocking}

Sí, la forma más fácil y común es bloqueando los servidores bootstrap o "Reseed". Bloquear completamente todo el tráfico ofuscado también funcionaría (aunque esto rompería muchas, muchas otras cosas que no son I2P y la mayoría no está dispuesta a llegar tan lejos). En el caso del bloqueo de reseed, hay un paquete de reseed en Github, bloquearlo también bloqueará Github. Puedes realizar reseed a través de un proxy (se pueden encontrar muchos en Internet si no quieres usar Tor) o compartir paquetes de reseed de forma amigo-a-amigo sin conexión.

### En `wrapper.log` veo un error que indica "`Protocol family unavailable`" al cargar la Consola del Router {#protocolfamily}

A menudo este error ocurrirá con cualquier software Java habilitado para red en algunos sistemas que están configurados para usar IPv6 por defecto. Hay algunas formas de resolver esto:

- En sistemas basados en Linux, puedes ejecutar `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Busca las siguientes líneas en `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Si las líneas están presentes, descoméntalas eliminando los "#". Si las líneas no están presentes, añádelas sin los "#".

Otra opción sería eliminar el `::1` de `~/.i2p/clients.config`

**ADVERTENCIA**: Para que cualquier cambio en `wrapper.config` tenga efecto, debe detener completamente el router y el wrapper. ¡Hacer clic en *Reiniciar* en la consola del router NO volverá a leer este archivo! Debe hacer clic en *Apagar*, esperar 11 minutos y luego iniciar I2P.

### ¿La mayoría de los sitios I2P dentro de I2P están caídos? {#down}

Si consideras cada sitio I2P que se ha creado alguna vez, sí, la mayoría están caídos. Las personas y los sitios I2P vienen y van. Una buena manera de comenzar en I2P es revisar una lista de sitios I2P que están actualmente activos. [identiguy.i2p](http://identiguy.i2p) rastrea los sitios I2P activos.

### ¿Por qué I2P está escuchando en el puerto 32000? {#port32000}

El wrapper de servicio Java Tanuki que utilizamos abre este puerto — vinculado a localhost — para comunicarse con el software que se ejecuta dentro de la JVM. Cuando se inicia la JVM, se le proporciona una clave para que pueda conectarse al wrapper. Después de que la JVM establece su conexión con el wrapper, el wrapper rechaza cualquier conexión adicional.

Puede encontrar más información en la [documentación del wrapper](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### ¿Cómo configuro mi navegador? {#browserproxy}

La configuración del proxy para diferentes navegadores está en una página separada con capturas de pantalla. Son posibles configuraciones más avanzadas con herramientas externas, como el complemento de navegador FoxyProxy o el servidor proxy Privoxy, pero podrían introducir fugas en tu configuración.

### ¿Cómo me conecto a IRC dentro de I2P? {#irc}

Se crea un túnel al servidor IRC principal dentro de I2P, Irc2P, cuando se instala I2P (consulta la [página de configuración de I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)), y se inicia automáticamente cuando arranca el router I2P. Para conectarte a él, indica a tu cliente IRC que se conecte a `localhost 6668`. Los usuarios de clientes tipo HexChat pueden crear una nueva red con el servidor `localhost/6668` (recuerda marcar "Bypass proxy server" si tienes un servidor proxy configurado). Los usuarios de Weechat pueden usar el siguiente comando para añadir una nueva red:

```
/server add irc2p localhost/6668
```
### ¿Cómo configuro mi propio sitio I2P? {#myI2P-Site}

El método más fácil es hacer clic en el enlace [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) en la consola del router y crear un nuevo 'Server Tunnel' (túnel de servidor). Puedes servir contenido dinámico configurando el destino del tunnel hacia el puerto de un servidor web existente, como Tomcat o Jetty. También puedes servir contenido estático. Para esto, configura el destino del tunnel a: `0.0.0.0 port 7659` y coloca el contenido en el directorio `~/.i2p/eepsite/docroot/`. (En sistemas que no son Linux, esto puede estar en una ubicación diferente. Verifica la consola del router.) El software 'eepsite' viene como parte del paquete de instalación de I2P y está configurado para iniciarse automáticamente cuando I2P se inicia. El sitio predeterminado que esto crea se puede acceder en http://127.0.0.1:7658. Sin embargo, tu 'eepsite' también es accesible para otros a través de tu archivo de claves del eepsite, ubicado en: `~/.i2p/eepsite/i2p/eepsite.keys`. Para obtener más información, lee el archivo readme en: `~/.i2p/eepsite/README.txt`.

### ¿Si alojo un sitio web en I2P en casa, que contenga solo HTML y CSS, es peligroso? {#hosting}

Depende de tu adversario y tu modelo de amenaza. Si solo te preocupan las violaciones de "privacidad" corporativas, delincuentes comunes y la censura, entonces no es realmente peligroso. Las fuerzas del orden probablemente te encontrarán de todos modos si realmente lo desean. Solo alojar cuando tienes un navegador de usuario doméstico normal (de internet) en ejecución hará realmente difícil saber quién está alojando esa parte. Por favor considera el alojamiento de tu sitio I2P igual que alojar cualquier otro servicio - es tan peligroso - o seguro - como tú mismo lo configures y gestiones.

Nota: Ya existe una forma de separar el alojamiento de un servicio i2p (destination) del router i2p. Si [entiendes cómo](/docs/overview/tech-intro#i2pservices) funciona, entonces puedes simplemente configurar una máquina separada como servidor para el sitio web (o servicio) que será públicamente accesible y reenviar eso al servidor web a través de un túnel SSH [muy] seguro o usar un sistema de archivos compartido y seguro.

### ¿Cómo encuentra I2P los sitios web ".i2p"? {#addresses}

La aplicación de Libreta de Direcciones de I2P asigna nombres legibles por humanos a destinos a largo plazo, asociados con servicios, lo que la hace más parecida a un archivo hosts o a una lista de contactos que a una base de datos de red o a un servicio DNS. También es local-first (prioriza lo local): no existe un espacio de nombres global reconocido, tú decides a qué se asigna cualquier dominio .i2p dado al final. El punto intermedio es algo llamado "Jump Service" (servicio de salto) que proporciona un nombre legible por humanos al redirigirte a una página donde se te preguntará "¿Le das permiso al router de I2P para llamar a $SITE_CRYPTO_KEY con el nombre $SITE_NAME.i2p?" o algo por el estilo. Una vez que está en tu libreta de direcciones, puedes generar tus propias URL de salto para ayudar a compartir el sitio con otros.

### ¿Cómo agrego direcciones a la Libreta de Direcciones? {#addressbook}

No puedes agregar una dirección sin conocer al menos el base32 o base64 del sitio que deseas visitar. El "hostname" que es legible para humanos es solo un alias para la dirección criptográfica, que corresponde al base32 o base64. Sin la dirección criptográfica, no hay forma de acceder a un sitio I2P, esto es por diseño. Distribuir la dirección a personas que aún no la conocen es generalmente responsabilidad del proveedor del servicio Jump. Visitar un sitio I2P que es desconocido activará el uso de un servicio Jump. stats.i2p es el servicio Jump más confiable.

Si estás alojando un sitio a través de i2ptunnel, entonces aún no tendrá un registro con un servicio de salto. Para darle una URL localmente, visita la página de configuración y haz clic en el botón que dice "Add to Local Address Book." Luego ve a http://127.0.0.1:7657/dns para buscar la URL del asistente de direcciones y compartirla.

### ¿Qué puertos usa I2P? {#ports}

Los puertos que utiliza I2P se pueden dividir en 2 secciones:

1. Puertos de cara a Internet, que se utilizan para la comunicación con otros routers I2P
2. Puertos locales, para conexiones locales

Estos se describen en detalle a continuación.

#### 1. Puertos expuestos a Internet

Nota: Desde la versión 0.7.8, las nuevas instalaciones no utilizan el puerto 8887; se selecciona un puerto aleatorio entre 9000 y 31000 cuando el programa se ejecuta por primera vez. El puerto seleccionado se muestra en la [página de configuración](http://127.0.0.1:7657/confignet) del router.

**SALIENTE**

- UDP desde el puerto aleatorio listado en la [página de configuración](http://127.0.0.1:7657/confignet) hacia puertos UDP remotos arbitrarios, permitiendo respuestas
- TCP desde puertos altos aleatorios hacia puertos TCP remotos arbitrarios
- UDP saliente en el puerto 123, permitiendo respuestas. Esto es necesario para la sincronización de tiempo interna de I2P (vía SNTP - consultando un host SNTP aleatorio en pool.ntp.org u otro servidor que especifiques)

**ENTRANTE**

- (Opcional, recomendado) UDP al puerto indicado en la [página de configuración](http://127.0.0.1:7657/confignet) desde ubicaciones arbitrarias
- (Opcional, recomendado) TCP al puerto indicado en la [página de configuración](http://127.0.0.1:7657/confignet) desde ubicaciones arbitrarias
- El TCP entrante se puede deshabilitar en la [página de configuración](http://127.0.0.1:7657/confignet)

#### 2. Puertos I2P locales

Los puertos I2P locales escuchan solo conexiones locales de forma predeterminada, excepto donde se indique:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### Me faltan muchos hosts en mi libreta de direcciones. ¿Cuáles son algunos buenos enlaces de suscripción? {#subscriptions}

La libreta de direcciones se encuentra en [http://localhost:7657/dns](http://localhost:7657/dns) donde se puede encontrar más información.

**¿Cuáles son algunos buenos enlaces de suscripción a la libreta de direcciones?**

Puedes intentar lo siguiente:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### ¿Cómo puedo acceder a la consola web desde mis otras máquinas o protegerla con contraseña? {#remote_webconsole}

Por motivos de seguridad, la consola de administración del router por defecto solo escucha conexiones en la interfaz local.

Existen dos métodos para acceder a la consola de forma remota:

1. Túnel SSH
2. Configurar tu consola para que esté disponible en una dirección IP pública con un nombre de usuario y contraseña

Estos se detallan a continuación:

**Método 1: Túnel SSH**

Si estás ejecutando un sistema operativo tipo Unix, este es el método más fácil para acceder remotamente a tu consola I2P. (Nota: El software de servidor SSH está disponible para sistemas que ejecutan Windows, por ejemplo [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Una vez que hayas configurado el acceso SSH a tu sistema, se pasa la bandera '-L' a SSH con los argumentos apropiados - por ejemplo:

```
ssh -L 7657:localhost:7657 (System_IP)
```
donde '(System_IP)' se reemplaza con la dirección IP de tu sistema. Este comando reenvía el puerto 7657 (el número antes de los dos puntos) al puerto 7657 del sistema remoto (especificado por la cadena 'localhost' entre los primeros y segundos dos puntos) (el número después de los segundos dos puntos). Tu consola I2P remota estará ahora disponible en tu sistema local como 'http://localhost:7657' y estará disponible mientras tu sesión SSH esté activa.

Si deseas iniciar una sesión SSH sin iniciar un shell en el sistema remoto, puedes agregar la opción '-N':

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Método 2: Configurar tu consola para que esté disponible en una dirección IP pública con un nombre de usuario y contraseña**

1. Abre `~/.i2p/clients.config` y reemplaza:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   con:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   donde reemplazas (System_IP) con la dirección IP pública de tu sistema

2. Ve a [http://localhost:7657/configui](http://localhost:7657/configui) y añade un nombre de usuario y contraseña para la consola si lo deseas - Se recomienda encarecidamente añadir un nombre de usuario y contraseña para proteger tu consola I2P de manipulaciones, lo que podría llevar a la des-anonimización.

3. Ve a [http://localhost:7657/index](http://localhost:7657/index) y pulsa "Graceful restart", que reinicia la JVM y recarga las aplicaciones cliente

Una vez que se inicie, ahora deberías poder acceder a tu consola de forma remota. Carga la consola del router en `http://(IP_del_Sistema):7657` y se te solicitará el nombre de usuario y la contraseña que especificaste en el paso 2 anterior si tu navegador admite la ventana emergente de autenticación.

NOTA: Puedes especificar 0.0.0.0 en la configuración anterior. Esto especifica una interfaz, no una red o máscara de red. 0.0.0.0 significa "enlazar a todas las interfaces", por lo que puede ser accesible en 127.0.0.1:7657 así como en cualquier IP de LAN/WAN. Ten cuidado al usar esta opción ya que la consola estará disponible en TODAS las direcciones configuradas en tu sistema.

### ¿Cómo puedo usar aplicaciones desde mis otras máquinas? {#remote_i2cp}

Por favor, consulta la respuesta anterior para obtener instrucciones sobre cómo usar el reenvío de puertos SSH, y también consulta esta página en tu consola: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### ¿Es posible usar I2P como proxy SOCKS? {#socks}

El proxy SOCKS ha sido funcional desde la versión 0.7.1. Se admiten SOCKS 4/4a/5. I2P no tiene un outproxy SOCKS, por lo que está limitado solo para uso dentro de I2P.

Muchas aplicaciones filtran información sensible que podría identificarte en Internet y este es un riesgo del que debes ser consciente al usar el proxy SOCKS de I2P. I2P solo filtra los datos de conexión, pero si el programa que pretendes ejecutar envía esta información como contenido, I2P no tiene forma de proteger tu anonimato. Por ejemplo, algunas aplicaciones de correo enviarán la dirección IP de la máquina en la que se están ejecutando a un servidor de correo. Recomendamos herramientas o aplicaciones específicas de I2P (como [I2PSnark](http://localhost:7657/i2psnark/) para torrents), o aplicaciones que se sabe que son seguras de usar con I2P que incluyen complementos populares encontrados en [Firefox](https://www.mozilla.org/).

### ¿Cómo accedo a IRC, BitTorrent u otros servicios en Internet normal? {#proxy_other}

Existen servicios llamados Outproxies que hacen de puente entre I2P e Internet, similar a los Tor Exit Nodes. La funcionalidad de outproxy predeterminada para HTTP y HTTPS es proporcionada por `exit.stormycloud.i2p` y está gestionada por StormyCloud Inc. Se configura en el HTTP Proxy. Además, para ayudar a proteger el anonimato, I2P no permite realizar conexiones anónimas a Internet regular de forma predeterminada. Consulte la página [Socks Outproxy](/docs/api/socks#outproxy) para más información.

---

## Reseeds

### Mi router ha estado activo durante varios minutos y tiene cero o muy pocas conexiones {#reseed}

Primero revisa la página [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) en la Consola del Router – tu base de datos de red. Si no ves ningún router listado desde dentro de I2P pero la consola indica que deberías estar detrás de un firewall, entonces probablemente no puedes conectarte a los servidores de reseed. Si ves otros routers de I2P listados, entonces intenta reducir el número de conexiones máximas en [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) quizás tu router no puede manejar muchas conexiones.

### ¿Cómo hago un reseed manualmente? {#manual_reseed}

En circunstancias normales, I2P te conectará a la red automáticamente usando nuestros enlaces de arranque. Si una interrupción de internet hace que falle el arranque desde los servidores reseed, una forma fácil de arrancar es usando el navegador Tor (Por defecto abre localhost), que funciona muy bien con [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). También es posible hacer reseed de un router I2P manualmente.

Al usar el navegador Tor para resembrar puedes seleccionar múltiples URLs a la vez y continuar. Aunque el valor predeterminado que es 2 (de las múltiples urls) también funcionará, pero será lento.

---

## Privacidad-Seguridad

### ¿Es mi router un "nodo de salida" (outproxy) hacia Internet normal? No quiero que lo sea. {#exit}

No, tu router participa en el transporte de tráfico cifrado de extremo a extremo a través de la red i2p hacia un punto final de tunnel aleatorio, normalmente no un outproxy, pero no se pasa tráfico entre tu router e Internet sobre la capa de transporte. Como usuario final, no deberías ejecutar un outproxy si no tienes experiencia en administración de sistemas y redes.

### ¿Es fácil detectar el uso de I2P analizando el tráfico de red? {#detection}

El tráfico de I2P generalmente parece tráfico UDP, y no mucho más – y hacer que parezca no mucho más es un objetivo. También soporta TCP. Con algo de esfuerzo, el análisis pasivo de tráfico puede ser capaz de clasificar el tráfico como "I2P", pero esperamos que el desarrollo continuo de ofuscación de tráfico reduzca esto aún más. Incluso una capa de ofuscación de protocolo bastante simple como obfs4 evitará que los censores bloqueen I2P (es un objetivo que I2P implementa).

### ¿Es seguro usar I2P? {#safe}

Depende de tu modelo de amenaza personal. Para la mayoría de las personas, I2P es mucho más seguro que no usar ninguna protección. Algunas otras redes (como Tor, mixminion/mixmaster), probablemente son más seguras contra ciertos adversarios. Por ejemplo, el tráfico de I2P no utiliza TLS/SSL, por lo que no tiene los problemas del "eslabón más débil" que tiene Tor. I2P fue utilizado por muchas personas en Siria durante la "Primavera Árabe", y recientemente el proyecto ha experimentado un mayor crecimiento en instalaciones lingüísticas más pequeñas de I2P en Oriente Próximo y Medio. Lo más importante a tener en cuenta aquí es que I2P es una tecnología y necesitas una guía/tutorial para mejorar tu privacidad/anonimato en Internet. También verifica tu navegador o importa el motor de búsqueda de huellas digitales para bloquear ataques de fingerprinting con un conjunto de datos muy grande (es decir: colas largas típicas / estructura de datos diversa muy precisa) sobre muchas características del entorno y no uses VPN para reducir todos los riesgos que provienen de sí misma, como el comportamiento de la caché TLS propia y la construcción técnica del negocio del proveedor que puede ser hackeado más fácilmente que un sistema de escritorio propio. Tal vez usar un navegador Tor aislado (Tor Browser) con sus excelentes protecciones anti-fingerprint y una protección general de tiempo de ejecución tipo appguard que solo permita las comunicaciones del sistema necesarias, y un último uso de máquina virtual con scripts de desactivación anti-espía y live-cd para eliminar cualquier "riesgo casi permanente posible" y reducir todos los riesgos mediante una probabilidad decreciente, sean una buena opción en redes públicas y modelos de riesgo individuales elevados, y podría ser lo mejor que puedes hacer con este objetivo para el uso de i2p.

### Veo direcciones IP de todos los demás nodos I2P en la consola del router. ¿Significa eso que mi dirección IP es visible para otros? {#netdb_ip}

Sí, para otros nodos I2P que conocen tu router. Utilizamos esto para conectarnos con el resto de la red I2P. Las direcciones están físicamente ubicadas en objetos "routerInfos (clave,valor)", ya sea obtenidos remotamente o recibidos de pares. Los "routerInfos" contienen cierta información (algunas opcionales añadidas de forma oportunista), "publicada por el par", sobre el router mismo para el arranque inicial. No hay datos en este objeto sobre clientes. Mirando más de cerca bajo el capó te dirá que todos son contabilizados con el tipo más reciente de creación de identificadores llamado "SHA-256 Hashes (bajo=hash positivo(-clave), alto=hash negativo(+clave))". La red I2P tiene su propia base de datos de routerInfos creados durante la carga e indexación, pero esto depende profundamente de la realización de las tablas clave/valor y la topología de la red y el estado de carga / estado de ancho de banda y las probabilidades de enrutamiento para almacenamientos en componentes de base de datos.

### ¿Es seguro usar un outproxy? {#proxy_safe}

Depende de cuál sea tu definición de "seguro". Los outproxies son excelentes cuando funcionan, pero desafortunadamente son operados voluntariamente por personas que pueden perder el interés o no tener los recursos para mantenerlos 24/7 – ten en cuenta que puedes experimentar períodos de tiempo durante los cuales los servicios no están disponibles, están interrumpidos o no son confiables, y no estamos asociados con este servicio ni tenemos influencia sobre él.

Los outproxys en sí mismos pueden ver tu tráfico entrar y salir, con la excepción de los datos HTTPS/SSL cifrados de extremo a extremo, tal como tu ISP puede ver tu tráfico entrar y salir de tu computadora. Si te sientes cómodo con tu ISP, no sería peor con el outproxy.

### ¿Qué hay sobre los ataques de "Desanonimización"? {#deanon}

Para una explicación muy detallada, lee más en nuestros artículos sobre [Modelo de Amenazas](/docs/overview/threat-model). En general, la des-anonimización no es trivial, pero es posible si no eres lo suficientemente cauteloso.

---

## Acceso a Internet/Rendimiento

### No puedo acceder a sitios de Internet regulares a través de I2P. {#outproxy}

El proxy hacia sitios de Internet (eepsites que salen a Internet) se proporciona como un servicio a los usuarios de I2P por proveedores sin bloqueo. Este servicio no es el enfoque principal del desarrollo de I2P, y se proporciona de forma voluntaria. Los eepsites que están alojados en I2P siempre deberían funcionar sin un outproxy (proxy de salida). Los outproxies son una conveniencia pero por diseño no son perfectos ni una parte importante del proyecto. Tenga en cuenta que es posible que no puedan proporcionar el servicio de alta calidad que otros servicios de I2P pueden ofrecer.

### No puedo acceder a sitios https:// o ftp:// a través de I2P. {#https}

El proxy HTTP predeterminado solo admite salida HTTP y HTTPS.

### ¿Por qué mi router está usando demasiada CPU? {#cpu}

Primero, asegúrate de tener la última versión de cada componente relacionado con I2P: las versiones antiguas tenían secciones de código que consumían CPU innecesariamente. También existe un [registro de rendimiento](/docs/overview/performance) que documenta algunas de las mejoras en el rendimiento de I2P a lo largo del tiempo.

### ¿Mis pares activos / pares conocidos / túneles participantes / conexiones / ancho de banda varían drásticamente con el tiempo! ¿Hay algo mal? {#vary}

La estabilidad general de la red I2P es un área de investigación continua. Una cantidad particular de esa investigación se centra en cómo pequeños cambios en la configuración modifican el comportamiento del router. Como I2P es una red peer-to-peer (entre pares), las acciones de otros peers influirán en el rendimiento de tu router.

### ¿Qué hace que las descargas, torrents, navegación web y todo lo demás sea más lento en I2P en comparación con la internet regular? {#slow}

I2P tiene diferentes protecciones que añaden enrutamiento adicional y capas extra de cifrado. También rebota el tráfico a través de otros peers (Tunnels) que tienen su propia velocidad y calidad, algunos son lentos, otros rápidos. Esto suma mucha sobrecarga y tráfico a diferentes ritmos en diferentes direcciones. Por diseño, todas estas cosas lo harán más lento en comparación con una conexión directa en internet, pero mucho más anónimo y aún lo suficientemente rápido para la mayoría de las cosas.

A continuación se presenta un ejemplo con una explicación para ayudar a proporcionar contexto sobre las consideraciones de latencia y ancho de banda al usar I2P.

Considere el diagrama a continuación. Representa una conexión entre un cliente que realiza una solicitud a través de I2P, un servidor que recibe la solicitud a través de I2P y luego responde también a través de I2P. El circuito por el cual viaja la solicitud también se muestra.

Según el diagrama, considere que las cajas etiquetadas como 'P', 'Q' y 'R' representan un túnel de salida (outbound tunnel) para 'A' y que las cajas etiquetadas como 'X', 'Y' y 'Z' representan un túnel de salida para 'B'. De manera similar, las cajas etiquetadas como 'X', 'Y' y 'Z' representan un túnel de entrada (inbound tunnel) para 'B' mientras que las cajas etiquetadas como 'P_1', 'Q_1' y 'R_1' representan un túnel de entrada para 'A'. Las flechas entre las cajas muestran la dirección del tráfico. El texto arriba y abajo de las flechas detalla algunos ejemplos de ancho de banda entre un par de saltos, así como ejemplos de latencias.

Cuando tanto el cliente como el servidor están utilizando túneles de 3 saltos en todo momento, un total de 12 routers I2P adicionales participan en la retransmisión del tráfico. 6 pares retransmiten el tráfico desde el cliente al servidor, el cual se divide en un túnel de salida de 3 saltos desde 'A' ('P', 'Q', 'R') y un túnel de entrada de 3 saltos hacia 'B' ('X', 'Y', 'Z'). De manera similar, 6 pares retransmiten el tráfico desde el servidor de vuelta al cliente.

Primero, podemos considerar la latencia - el tiempo que tarda una solicitud de un cliente en atravesar la red I2P, llegar al servidor y volver al cliente. Sumando todas las latencias vemos que:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
El tiempo total de ida y vuelta en nuestro ejemplo suma 740 ms, ciertamente mucho mayor que lo que normalmente se vería al navegar sitios web de Internet regulares.

En segundo lugar, podemos considerar el ancho de banda disponible. Esto se determina a través del enlace más lento entre saltos desde el cliente y el servidor, así como cuando el tráfico está siendo transmitido por el servidor al cliente. Para el tráfico que va del cliente al servidor, vemos que el ancho de banda disponible en nuestro ejemplo entre los saltos 'R' y 'X', así como entre los saltos 'X' e 'Y' es de 32 KB/s. A pesar de un ancho de banda disponible mayor entre los otros saltos, estos saltos actuarán como un cuello de botella y limitarán el ancho de banda máximo disponible para el tráfico de 'A' a 'B' a 32 KB/s. De manera similar, rastreando la ruta del servidor al cliente se muestra que hay un ancho de banda máximo de 64 KB/s - entre los saltos 'Z_1' y 'Y_1', 'Y_1' y 'X_1' y 'Q_1' y 'P_1'.

Recomendamos aumentar tus límites de ancho de banda. Esto ayuda a la red al incrementar la cantidad de ancho de banda disponible, lo cual mejorará tu experiencia con I2P. La configuración de ancho de banda se encuentra en la página [http://localhost:7657/config](http://localhost:7657/config). Ten en cuenta los límites de tu conexión a internet determinados por tu proveedor de servicios de internet (ISP) y ajusta tu configuración en consecuencia.

También recomendamos configurar una cantidad suficiente de ancho de banda compartido: esto permite que los túneles participantes se enruten a través de tu router I2P. Permitir tráfico participante mantiene tu router bien integrado en la red y mejora tus velocidades de transferencia.

I2P es un trabajo en progreso. Se están implementando muchas mejoras y correcciones, y, en términos generales, ejecutar la versión más reciente ayudará a tu rendimiento. Si no lo has hecho, instala la versión más reciente.

### Creo que encontré un error, ¿dónde puedo reportarlo? {#bug}

Puedes reportar cualquier error o problema que encuentres en nuestro rastreador de errores, que está disponible tanto en internet no privado como en I2P. Tenemos un foro de discusión, también disponible en I2P e internet no privado. También puedes unirte a nuestro canal de IRC: ya sea a través de nuestra red IRC, IRC2P, o en Freenode.

- **Nuestro rastreador de errores:**
  - Internet no privada: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - En I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Nuestros foros:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Pegar registros:** Puede pegar cualquier registro de interés en un servicio de pegado como los servicios de internet no privada listados en la [Wiki de PrivateBin](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), o un servicio de pegado de I2P como esta [instancia de PrivateBin](http://paste.crypthost.i2p) o este [servicio de pegado sin Javascript](http://pasta-nojs.i2p) y hacer seguimiento en IRC en #i2p
- **IRC:** Únase a #i2p-dev Para discutir con los desarrolladores en IRC

Por favor incluye información relevante de la página de registros del router que está disponible en: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Solicitamos que compartas todo el texto bajo la sección 'I2P Version and Running Environment' así como cualquier error o advertencia que se muestre en los diversos registros mostrados en la página.

---

### ¡Tengo una pregunta! {#question}

¡Genial! Encuéntranos en IRC:

- en `irc.freenode.net` canal `#i2p`
- en `IRC2P` canal `#i2p`

o publica en [el foro](http://i2pforum.i2p/) y lo publicaremos aquí (con la respuesta, esperamos).
