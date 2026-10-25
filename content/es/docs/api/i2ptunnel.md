---
title: "I2PTunnel"
description: "Herramienta para interactuar y proporcionar servicios en I2P"
slug: "i2ptunnel"
aliases:
  - "/es/i2ptunnel"
  - "/es/i2ptunnel/"
  - "/es/i2ptunnel_migration"
  - "/es/i2ptunnel_migration/"
  - "/es/i2ptunnel_services"
  - "/es/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Descripción general {#overview}

I2PTunnel es una herramienta para interactuar con I2P y proporcionar servicios en la red. El destino de un I2PTunnel puede definirse usando un [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), o una clave de destino completa de 516 bytes. Un I2PTunnel establecido estará disponible en tu máquina cliente como localhost:puerto. Si deseas proporcionar un servicio en la red I2P, simplemente creas un I2PTunnel hacia la dirección_ip:puerto apropiada. Se generará una clave de destino correspondiente de 516 bytes para el servicio y estará disponible en toda la red I2P. Una interfaz web para la gestión de I2PTunnel está disponible en [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Servicios Predeterminados {#default-services}

### Túneles de Servidor {#default-server-tunnels}

- **I2P Webserver** - Un tunnel apuntado a un servidor web Jetty ejecutado
  en [localhost:7658](http://localhost:7658) para alojamiento conveniente y rápido en I2P.
  El directorio raíz del documento es:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, que se expande a: `C:\Users\**nombre_de_usuario**\AppData\Local\I2P\I2P Site\docroot`

### Túneles de Cliente {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - Un proxy HTTP utilizado para navegar por I2P y la internet regular de forma anónima a través de I2P. La navegación por internet a través de I2P utiliza un proxy aleatorio especificado por la opción "Outproxies:".
- **Irc2P** - *localhost:6668* - Un tunnel IRC hacia la red IRC anónima por defecto, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - Acceso SSH al repositorio Git del proyecto
- **smtp.postman.i2p** - *localhost:7659* - Un servicio SMTP proporcionado por postman en hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - El servicio POP acompañante de postman en hq.postman.i2p

## Configuración {#configuration}

[Configuración de I2PTunnel](/docs/specs/configuration)

## Modos de Cliente {#client-modes}

### Estándar {#client-modes-standard}

Abre un puerto TCP local que se conecta a un servicio (como HTTP, FTP o SMTP) en un destino dentro de I2P. El tunnel se dirige a un host aleatorio de la lista de destinos separada por comas (", ").

### HTTP {#client-mode-http}

Un túnel cliente HTTP. El túnel se conecta al destino especificado por la URL en una petición HTTP. Soporta proxy hacia internet si se proporciona un outproxy. Elimina las siguientes cabeceras de las conexiones HTTP:

- **Accept\*:** (sin incluir "Accept" y "Accept-Encoding") ya que varían considerablemente entre navegadores y pueden usarse como identificador.
- **Referer:**
- **Via:**
- **From:**

El proxy cliente HTTP proporciona una serie de servicios para proteger al usuario y brindar una mejor experiencia de usuario.

**Procesamiento de encabezados de solicitud:** - Eliminar encabezados problemáticos para la privacidad - Enrutamiento a outproxy local o remoto - Selección, almacenamiento en caché y seguimiento de disponibilidad de outproxy - Búsquedas de nombre de host a destino - Reemplazo de encabezado Host a b32 - Agregar encabezado para indicar soporte de descompresión transparente - Forzar conexión: cerrar - Soporte de proxy compatible con RFC - Procesamiento y eliminación de encabezados hop-by-hop compatibles con RFC - Autenticación opcional digest y básica de nombre de usuario/contraseña - Autenticación opcional digest y básica de nombre de usuario/contraseña para outproxy - Almacenamiento en buffer de todos los encabezados antes de pasarlos para eficiencia - Enlaces de servidor de salto - Procesamiento de respuestas de salto y formularios (ayudante de direcciones) - Procesamiento de b32 ciego y formularios de credenciales - Soporta solicitudes HTTP y HTTPS (CONNECT) estándar

**Procesamiento de encabezados de respuesta:** - Verificar si descomprimir la respuesta - Forzar conexión: cerrar - Procesamiento y eliminación de encabezados hop-by-hop conforme a RFC - Almacenamiento en búfer de todos los encabezados antes de pasarlos para mayor eficiencia

**Respuestas de error HTTP:** - Para muchos errores comunes y no tan comunes, para que el usuario sepa qué ocurrió - Más de 20 páginas de error únicas traducidas, estilizadas y formateadas para varios errores - Servidor web interno para servir formularios, CSS, imágenes y errores

#### Compresión Transparente de Respuesta {#transparent-response-compression}

La compresión de respuesta de i2ptunnel se solicita con el encabezado HTTP:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

El lado del servidor elimina este encabezado hop-by-hop antes de enviar la solicitud al servidor web. El encabezado elaborado con todos los valores q no es necesario; los servidores deberían simplemente buscar "x-i2p-gzip" en cualquier parte del encabezado.

El lado del servidor determina si comprimir la respuesta basándose en las cabeceras recibidas del servidor web, incluyendo Content-Type, Content-Length y Content-Encoding, para evaluar si la respuesta es comprimible y vale la pena el CPU adicional requerido. Si el lado del servidor comprime la respuesta, añade la siguiente cabecera HTTP:

- **Content-Encoding:** x-i2p-gzip

Si este encabezado está presente en la respuesta, el proxy cliente HTTP la descomprime de forma transparente. El lado cliente elimina este encabezado y descomprime con gunzip antes de enviar la respuesta al navegador. Ten en cuenta que aún tenemos la compresión gzip subyacente en la capa I2CP, que sigue siendo efectiva si la respuesta no está comprimida en la capa HTTP.

Este diseño y la implementación actual violan el RFC 2616 de varias maneras:

- X-Accept-Encoding no es un header estándar
- No deschunkea/chunkea por salto; pasa el chunking de extremo a extremo
- Pasa el header Transfer-Encoding de extremo a extremo
- Usa Content-Encoding, no Transfer-Encoding, para especificar la codificación por salto
- Prohíbe el gzipping x-i2p cuando Content-Encoding está configurado (pero probablemente no queremos hacer eso de todos modos)
- El lado del servidor gzipea el chunking enviado por el servidor, en lugar de hacer dechunk-gzip-rechunk y dechunk-gunzip-rechunk
- El contenido gzipeado no se chunkea después. RFC 2616 requiere que todo Transfer-Encoding que no sea "identity" esté chunkeado.
- Porque no hay chunking afuera (después) del gzip, es más difícil encontrar el final de los datos, haciendo que cualquier implementación de keepalive sea más difícil.
- RFC 2616 dice que Content-Length no debe enviarse si Transfer-Encoding está presente, pero nosotros lo hacemos. La especificación dice ignorar Content-Length si Transfer-Encoding está presente, lo cual los navegadores hacen, así que funciona para nosotros.

Los cambios para implementar una compresión hop-by-hop que cumpla con los estándares de manera compatible con versiones anteriores son un tema para estudios futuros. Cualquier cambio a dechunk-gzip-rechunk requeriría un nuevo tipo de codificación, quizás x-i2p-gzchunked. Esto sería idéntico a Transfer-Encoding: gzip, pero tendría que señalizarse de manera diferente por razones de compatibilidad. Cualquier cambio requeriría una propuesta formal.

#### Compresión Transparente de Solicitudes {#transparent-request-compression}

No soportado, aunque POST se beneficiaría. Ten en cuenta que aún tenemos la compresión gzip subyacente en la capa I2CP.

#### Persistencia {#persistence}

Los proxies cliente y servidor actualmente no admiten sockets HTTP persistentes RFC 2616 en ninguno de los tres saltos (socket del navegador, socket I2P, socket del servidor). Se inyectan encabezados Connection: close en cada salto. Se están investigando cambios para implementar la persistencia. Estos cambios deberían cumplir con los estándares y ser compatibles con versiones anteriores, y no requerirían una propuesta formal.

#### Pipelining {#pipelining}

Los proxies de cliente y servidor actualmente no admiten HTTP pipelining RFC 2616 y no hay planes para hacerlo. Los navegadores modernos no admiten pipelining a través de proxies porque la mayoría de los proxies no pueden implementarlo correctamente.

#### Compatibilidad {#compatibility}

Las implementaciones de proxy deben funcionar correctamente con otras implementaciones en el otro extremo. Los proxies de cliente deberían funcionar sin un proxy de servidor que reconozca HTTP (es decir, un tunnel estándar) en el lado del servidor. No todas las implementaciones soportan x-i2p-gzip.

#### Agente de Usuario {#user-agent}

Dependiendo de si el túnel está usando un outproxy o no, agregará el siguiente User-Agent:

- *Outproxy:* **User-Agent:** Utiliza el user agent de una versión reciente de Firefox en Windows
- *Uso interno de I2P:* **User-Agent:** MYOB/6.66 (AN/ON)

### Cliente IRC {#client-mode-irc}

Crea una conexión a un servidor IRC aleatorio especificado por la lista de destinos separados por comas (", "). Solo se permite un subconjunto de comandos IRC incluidos en la lista blanca debido a preocupaciones de anonimato.

La siguiente lista de permitidos es para comandos entrantes desde el servidor IRC hacia el cliente IRC.

**Lista de permitidos:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

También hay una lista de permitidos para comandos salientes del cliente IRC al servidor IRC. Es bastante extensa debido al número de comandos administrativos de IRC. Consulta el código fuente de IRCFilter.java para más detalles.

El filtro de salida también modifica los siguientes comandos para eliminar información identificativa: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

Permite usar el router I2P como un proxy SOCKS.

### SOCKS IRC {#client-mode-socks-irc}

Permite usar el router I2P como un proxy SOCKS con la lista blanca de comandos especificada por el modo cliente [IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Crea un túnel HTTP y utiliza el método de solicitud HTTP "CONNECT" para construir un túnel TCP que normalmente se usa para SSL y HTTPS.

### Streamr {#client-mode-streamr}

Crea un servidor UDP conectado a un túnel I2PTunnel cliente Streamr. El túnel cliente streamr se suscribirá a un túnel servidor streamr.

![Diagrama de Streamr](/images/I2PTunnel-streamr.png)

## Modos de Servidor {#server-modes}

### Estándar {#server-mode-standard}

Crea un destino hacia una ip:puerto local con un puerto TCP abierto.

### HTTP {#server-mode-http}

Crea un destino hacia un servidor HTTP local ip:puerto. Soporta gzip para solicitudes con Accept-encoding: x-i2p-gzip, responde con Content-encoding: x-i2p-gzip en tales solicitudes.

El proxy del servidor HTTP proporciona una serie de servicios para hacer que alojar un sitio web sea más fácil y seguro, y para brindar una mejor experiencia de usuario del lado del cliente.

**Procesamiento de cabeceras de solicitud:** - Validación de cabeceras - Protección contra falsificación de cabeceras - Verificaciones de tamaño de cabeceras - Rechazo opcional de inproxy y user-agent - Agregar cabeceras X-I2P para que el servidor web sepa de dónde proviene la solicitud - Reemplazo de cabecera Host para facilitar los vhosts del servidor web - Forzar connection: close - Procesamiento y eliminación de cabeceras hop-by-hop conforme a RFC - Almacenamiento en búfer de todas las cabeceras antes de pasar a través para mayor eficiencia

**Protección DDoS:** - Limitación de POST - Timeouts y protección contra slowloris - Limitación adicional ocurre en streaming para todos los tipos de tunnel

**Procesamiento de cabeceras de respuesta:** - Eliminación de algunas cabeceras problemáticas para la privacidad - Verificación del tipo MIME y otras cabeceras para determinar si comprimir la respuesta - Forzar connection: close - Procesamiento y eliminación de cabeceras hop-by-hop conforme a RFC - Almacenamiento en búfer de todas las cabeceras antes de pasarlas para mayor eficiencia

**Respuestas de error HTTP:** - Para muchos errores comunes y no tan comunes, y sobre limitación de velocidad, para que el usuario del lado cliente sepa qué ocurrió

**Compresión transparente de respuestas:** - El servidor web y/o la capa I2CP pueden comprimir, pero el servidor web a menudo no lo hace, y es más eficiente comprimir en una capa alta, incluso si I2CP también comprime. El proxy del servidor HTTP trabaja de forma cooperativa con el proxy del lado del cliente para comprimir respuestas de manera transparente.

### HTTP Bidireccional {#server-mode-http-bidir}

*Obsoleto*

Funciona tanto como un servidor HTTP I2PTunnel como un cliente HTTP I2PTunnel sin capacidades de outproxy. Una aplicación de ejemplo sería una aplicación web que realiza solicitudes tipo cliente, o pruebas de loopback de un sitio I2P como herramienta de diagnóstico.

### Servidor IRC {#server-mode-irc}

Crea un destino que filtra la secuencia de registro de un cliente y pasa la clave de destino del cliente como un nombre de host al servidor IRC.

### Streamr {#server-mode-streamr}

Se crea un cliente UDP que se conecta a un servidor multimedia. El cliente UDP se acopla con un túnel I2PTunnel servidor Streamr.
