---
title: "Trackers UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Cerrado"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Estado

Aprobado en revisión 2025-06-24. La especificación está en [especificación UDP](/docs/specs/udp-bittorrent-announces/). Implementado en zzzot 0.20.0-beta2. Implementado en i2psnark a partir de la API 0.9.67. Consulte la documentación de otras implementaciones para conocer el estado.

## Descripción general

Esta propuesta es para la implementación de rastreadores UDP en I2P.

### Change History

Una propuesta preliminar para trackers UDP en I2P fue publicada en nuestra [página de especificaciones de bittorrent](/docs/applications/bittorrent/) en mayo de 2014; esto precedió nuestro proceso formal de propuestas y nunca fue implementada. Esta propuesta fue creada a principios de 2022 y simplifica la versión de 2014.

Como esta propuesta depende de datagramas que pueden ser respondidos, se puso en espera una vez que comenzamos a trabajar en la [propuesta Datagram2](/proposals/163-datagram2/) a principios de 2023. Esa propuesta fue aprobada en abril de 2025.

La versión 2023 de esta propuesta especificó dos modos, "compatibilidad" y "rápido". Un análisis posterior reveló que el modo rápido sería inseguro, y también sería ineficiente para clientes con un gran número de torrents. Además, BiglyBT indicó una preferencia por el modo de compatibilidad. Este modo será más fácil de implementar para cualquier tracker o cliente que soporte el estándar [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Aunque el modo de compatibilidad es más complejo de implementar desde cero en el lado del cliente, sí tenemos código preliminar para ello iniciado en 2023.

Por lo tanto, la versión actual aquí está más simplificada para eliminar el modo rápido, y eliminar el término "compatibilidad". La versión actual cambia al nuevo formato Datagram2, y añade referencias al protocolo de extensión de anuncio UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Además, se agrega un campo de duración del ID de conexión a la respuesta de conexión, para extender las mejoras de eficiencia de este protocolo.

## Motivation

A medida que la base de usuarios en general y el número de usuarios de bittorrent específicamente continúa creciendo, necesitamos hacer que los trackers y los anuncios sean más eficientes para que los trackers no se vean abrumados.

Bittorrent propuso trackers UDP en BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) en 2008, y la gran mayoría de trackers en clearnet ahora son solo UDP.

Es difícil calcular el ahorro de ancho de banda de los datagramas frente al protocolo de streaming. Una solicitud que puede ser respondida tiene aproximadamente el mismo tamaño que un SYN de streaming, pero la carga útil es aproximadamente 500 bytes menor porque el HTTP GET tiene una cadena de parámetros de URL enorme de 600 bytes. La respuesta en bruto es mucho más pequeña que un SYN ACK de streaming, proporcionando una reducción significativa para el tráfico saliente de un tracker.

Además, debería haber reducciones de memoria específicas de la implementación, ya que los datagramas requieren mucho menos estado en memoria que una conexión de streaming.

El cifrado y las firmas Post-Quantum como se prevé en [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) aumentarán sustancialmente la sobrecarga de las estructuras cifradas y firmadas, incluyendo destinos, leaseSets, streaming SYN y SYN ACK. Es importante minimizar esta sobrecarga donde sea posible antes de que el cifrado PQ sea adoptado en I2P.

## Motivación

Esta propuesta utiliza repliable datagram2, repliable datagram3, y raw datagrams, como se define en [/docs/api/datagrams/](/docs/api/datagrams/). Datagram2 y Datagram3 son nuevas variantes de repliable datagrams, definidas en la Propuesta 163 [/proposals/163-datagram2/](/proposals/163-datagram2/). Datagram2 añade resistencia a la reproducción y soporte para firmas sin conexión. Datagram3 es más pequeño que el formato de datagrama anterior, pero sin autenticación.

### BEP 15

Para referencia, el flujo de mensajes definido en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) es el siguiente:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
La fase de conexión es necesaria para prevenir la suplantación de direcciones IP. El tracker devuelve un ID de conexión que el cliente utiliza en anuncios posteriores. Este ID de conexión expira por defecto en un minuto en el cliente, y en dos minutos en el tracker.

I2P utilizará el mismo flujo de mensajes que BEP 15, para facilitar la adopción en bases de código de clientes existentes con capacidad UDP: por eficiencia, y por las razones de seguridad discutidas a continuación:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
Esto potencialmente proporciona un gran ahorro de ancho de banda sobre los anuncios de streaming (TCP). Mientras que el Datagram2 tiene aproximadamente el mismo tamaño que un SYN de streaming, la respuesta raw es mucho más pequeña que el SYN ACK de streaming. Las solicitudes posteriores usan Datagram3, y las respuestas posteriores son raw.

Las solicitudes de anuncio son Datagram3 para que el tracker no necesite mantener una gran tabla de mapeo de IDs de conexión a destino de anuncio o hash. En su lugar, el tracker puede generar IDs de conexión criptográficamente a partir del hash del remitente, la marca de tiempo actual (basada en algún intervalo), y un valor secreto. Cuando se recibe una solicitud de anuncio, el tracker valida el ID de conexión, y luego usa el hash del remitente Datagram3 como el objetivo de envío.

### Historial de Cambios

Para una aplicación integrada (router y cliente en un proceso, por ejemplo i2psnark, y el plugin Java ZzzOT), o para una aplicación basada en I2CP (por ejemplo BiglyBT), debería ser sencillo implementar y enrutar el tráfico de streaming y datagramas por separado. Se espera que ZzzOT e i2psnark sean el primer tracker y cliente en implementar esta propuesta.

Los trackers y clientes no integrados se discuten a continuación.

#### Trackers

Existen cuatro implementaciones conocidas de rastreadores I2P:

- zzzot, un plugin integrado para router Java, ejecutándose en opentracker.dg2.i2p y varios otros
- tracker2.postman.i2p, ejecutándose presumiblemente detrás de un router Java y túnel HTTP Server
- El antiguo opentracker en C, portado por zzz, con soporte UDP comentado
- El nuevo opentracker en C, portado por r4sas, ejecutándose en opentracker.r4sas.i2p y posiblemente otros,
  ejecutándose presumiblemente detrás de un router i2pd y túnel HTTP Server

Para una aplicación de tracker externo que actualmente usa un túnel de servidor HTTP para recibir solicitudes de anuncio, la implementación podría ser bastante difícil. Se podría desarrollar un túnel especializado para traducir datagramas a solicitudes/respuestas HTTP locales. O se podría diseñar un túnel especializado que maneje tanto solicitudes HTTP como datagramas y que reenvíe los datagramas al proceso externo. Estas decisiones de diseño dependerán en gran medida de las implementaciones específicas del router y tracker, y están fuera del alcance de esta propuesta.

#### Clients

Los clientes de torrent externos basados en SAM como qbittorrent y otros clientes basados en libtorrent requerirían [SAM v3.3](/docs/api/samv3/) que no es compatible con i2pd. Esto también es requerido para soporte DHT, y es lo suficientemente complejo que ningún cliente de torrent SAM conocido lo ha implementado. No se esperan implementaciones basadas en SAM de esta propuesta pronto.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que el ID de conexión expira en un minuto en el cliente, y en dos minutos en el tracker. No es configurable. Eso limita las posibles mejoras de eficiencia, a menos que los clientes agrupen los anuncios para hacerlos todos dentro de una ventana de un minuto. i2psnark actualmente no agrupa los anuncios; los distribuye en el tiempo, para evitar ráfagas de tráfico. Se reporta que los usuarios avanzados ejecutan miles de torrents a la vez, y enviar tantos anuncios en ráfagas en un minuto no es realista.

Aquí, proponemos extender la respuesta de conexión para añadir un campo opcional de tiempo de vida de la conexión. El valor predeterminado, si no está presente, es un minuto. De lo contrario, el tiempo de vida especificado en segundos será usado por el cliente, y el tracker mantendrá el ID de conexión por un minuto adicional.

### Compatibility with BEP 15

Este diseño mantiene compatibilidad con [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tanto como sea posible para limitar los cambios requeridos en clientes y trackers existentes.

El único cambio requerido es el formato de la información del peer en la respuesta de announce. La adición del campo lifetime en la respuesta de connect no es requerida pero es altamente recomendada por eficiencia, como se explica arriba.

### BEP 15

Un objetivo importante de un protocolo de anuncio UDP es prevenir la suplantación de direcciones. El cliente debe existir realmente y agrupar un leaseset real. Debe tener túneles de entrada para recibir la Respuesta de Conexión. Estos túneles podrían ser de cero saltos y construirse instantáneamente, pero eso expondría al creador. Este protocolo logra ese objetivo.

### Soporte de Tracker/Cliente

- Esta propuesta no soporta destinos ciegos,
  pero puede ser extendida para hacerlo. Ver más abajo.

## Diseño

### Protocols and Ports

Repliable Datagram2 utiliza el protocolo I2CP 19; repliable Datagram3 utiliza el protocolo I2CP 20; los datagramas raw utilizan el protocolo I2CP 18. Las solicitudes pueden ser Datagram2 o Datagram3. Las respuestas son siempre raw. El formato de datagrama repliable más antiguo ("Datagram1") que utiliza el protocolo I2CP 17 NO debe ser utilizado para solicitudes o respuestas; estos deben descartarse si se reciben en los puertos de solicitud/respuesta. Nótese que el protocolo Datagram1 17 aún se utiliza para el protocolo DHT.

Las peticiones utilizan el "puerto de destino" I2CP de la URL de anuncio; ver más abajo. El "puerto de origen" de la petición es elegido por el cliente, pero debe ser distinto de cero y un puerto diferente de los utilizados por DHT, para que las respuestas puedan clasificarse fácilmente. Los trackers deben rechazar las peticiones recibidas en el puerto incorrecto.

Las respuestas utilizan el "puerto de destino" I2CP de la solicitud. El "puerto de origen" de la solicitud es el "puerto de destino" de la solicitud.

### Announce URL

El formato de URL de announce no está especificado en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), pero como en clearnet, las URLs de announce UDP tienen la forma "udp://host:port/path". La ruta se ignora y puede estar vacía, pero típicamente es "/announce" en clearnet. La parte :port siempre debe estar presente, sin embargo, si se omite la parte ":port", usar un puerto I2CP por defecto de 6969, ya que ese es el puerto común en clearnet. También puede haber parámetros cgi &a=b&c=d añadidos, estos pueden ser procesados y proporcionados en la solicitud de announce, ver [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Si no hay parámetros o ruta, la / final también puede omitirse, como se implica en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Duración de la Conexión

Todos los valores se envían en orden de bytes de red (big endian). No esperes que los paquetes sean exactamente de un tamaño determinado. Las extensiones futuras podrían aumentar el tamaño de los paquetes.

#### Connect Request

Cliente al tracker. 16 bytes. Debe ser un Datagram2 con respuesta posible. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker a cliente. 16 o 18 bytes. Debe ser raw. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se indica a continuación.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
La respuesta DEBE ser enviada al "puerto de destino" I2CP que fue recibido como el "puerto de origen" de la solicitud.

El campo lifetime es opcional e indica el tiempo de vida del connection_id del cliente en segundos. El valor predeterminado es 60, y el mínimo si se especifica es 60. El máximo es 65535 o aproximadamente 18 horas. El tracker debe mantener el connection_id durante 60 segundos más que el tiempo de vida del cliente.

#### Announce Request

Cliente a tracker. 98 bytes mínimo. Debe ser un Datagram3 que permita respuesta. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se indica a continuación.

El connection_id es como se recibió en la respuesta de conexión.

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Cambios respecto a [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key se ignora
- port probablemente se ignora
- La sección de opciones, si está presente, se define como en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La respuesta DEBE ser enviada al "puerto destino" I2CP que fue recibido como "puerto origen" de la solicitud. No uses el puerto de la solicitud de anuncio.

#### Announce Response

Del tracker al cliente. 20 bytes mínimo. Debe ser sin formato. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se indica a continuación.

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
Cambios de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- En lugar de 6 bytes IPv4+puerto o 18 bytes IPv6+puerto, devolvemos
  un múltiple de "respuestas compactas" de 32 bytes con los hashes SHA-256 binarios de peers.
  Al igual que con las respuestas compactas TCP, no incluimos un puerto.

La respuesta DEBE ser enviada al "puerto de destino" I2CP que fue recibido como el "puerto de origen" de la solicitud. No uses el puerto de la solicitud de anuncio.

Los datagramas I2P tienen un tamaño máximo muy grande de aproximadamente 64 KB; sin embargo, para una entrega confiable, se deben evitar los datagramas mayores a 4 KB. Por eficiencia de ancho de banda, los trackers probablemente deberían limitar el máximo de peers a aproximadamente 50, lo que corresponde a un paquete de aproximadamente 1600 bytes antes de la sobrecarga en varias capas, y debería estar dentro del límite de carga útil de dos mensajes de túnel después de la fragmentación.

Como en BEP 15, no se incluye un recuento del número de direcciones de peers (IP/puerto para BEP 15, hashes aquí) que seguirán. Aunque no se contempla en BEP 15, se podría definir un marcador de fin de peers con todos ceros para indicar que la información de peer está completa y que sigue algún dato de extensión.

Para que la extensión sea posible en el futuro, los clientes deben ignorar un hash de 32 bytes de todos ceros, y cualquier dato que le siga. Los trackers deben rechazar anuncios de un hash de todos ceros, aunque ese hash ya está prohibido por los routers de Java.

#### Scrape

La solicitud/respuesta scrape de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) no es requerida por esta propuesta, pero puede implementarse si se desea, no se requieren cambios. El cliente debe adquirir primero un ID de conexión. La solicitud scrape es siempre un Datagram3 con respuesta. La respuesta scrape es siempre raw.

#### Trackers

Del tracker al cliente. 8 bytes mínimo (si el mensaje está vacío). Debe ser raw. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Los bits de extensión o un campo de versión no están incluidos. Los clientes y trackers no deben asumir que los paquetes sean de un tamaño determinado. De esta manera, se pueden agregar campos adicionales sin romper la compatibilidad. Se recomienda el formato de extensiones definido en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) si es necesario.

La respuesta de conexión se modifica para agregar un tiempo de vida opcional del ID de conexión.

Si se requiere soporte para destinos cegados, podemos agregar la dirección cegada de 35 bytes al final de la solicitud de anuncio, o solicitar hashes cegados en las respuestas, usando el formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parámetros por determinar). El conjunto de direcciones de peers cegadas de 35 bytes podría agregarse al final de la respuesta de anuncio, después de un hash de 32 bytes con todos ceros.

## Implementation guidelines

Consulta la sección de diseño anterior para una discusión de los desafíos para clientes y trackers no integrados y que no utilizan I2CP.

### Compatibilidad con BEP 15

Para un nombre de host de tracker dado, un cliente debería preferir UDP sobre URLs HTTP, y no debería anunciarse a ambos.

Los clientes con soporte BEP 15 existente deberían requerir solo modificaciones menores.

Si un cliente soporta DHT u otros protocolos de datagramas, probablemente debería seleccionar un puerto diferente como el "puerto de origen" de la solicitud para que las respuestas regresen a ese puerto y no se mezclen con los mensajes DHT. El cliente solo recibe datagramas sin formato como respuestas. Los trackers nunca enviarán un datagram2 con capacidad de respuesta al cliente.

Los clientes con una lista predeterminada de opentrackers deben actualizar la lista para agregar URLs UDP después de que se confirme que los opentrackers conocidos soportan UDP.

Los clientes pueden o no implementar la retransmisión de solicitudes. Las retransmisiones, si se implementan, deben usar un tiempo de espera inicial de al menos 15 segundos, y duplicar el tiempo de espera para cada retransmisión (backoff exponencial).

Los clientes deben retroceder después de recibir una respuesta de error.

### Análisis de Seguridad

Los trackers con soporte BEP 15 existente deberían requerir solo pequeñas modificaciones. Esta propuesta difiere de la propuesta de 2014, en que el tracker debe soportar la recepción de datagram2 y datagram3 con respuesta en el mismo puerto.

Para minimizar los requisitos de recursos del tracker, este protocolo está diseñado para eliminar cualquier requisito de que el tracker almacene mapeos de hashes de cliente a IDs de conexión para validación posterior. Esto es posible porque el paquete de solicitud de anuncio es un paquete Datagram3 que puede ser respondido, por lo que contiene el hash del remitente.

Una implementación recomendada es:

- Define la época actual como el tiempo actual con una resolución del tiempo de vida de la conexión,
  ``epoch = now / lifetime``.
- Define una función hash criptográfica ``H(secret, clienthash, epoch)`` que genera
  una salida de 8 bytes.
- Genera la constante aleatoria secreta utilizada para todas las conexiones.
- Para respuestas de conexión, genera ``connection_id = H(secret,  clienthash, epoch)``
- Para solicitudes de anuncio, valida el ID de conexión recibido en la época actual verificando
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Los clientes existentes no admiten las URL de anuncio UDP y las ignoran.

Los trackers existentes no admiten la recepción de datagramas respondibles o sin procesar, estos serán descartados.

Esta propuesta es completamente opcional. Ni los clientes ni los trackers están obligados a implementarla en ningún momento.

## Rollout

Las primeras implementaciones se esperan en ZzzOT e i2psnark. Se utilizarán para pruebas y verificación de esta propuesta.

Otras implementaciones seguirán según se desee después de que las pruebas y verificación estén completas.
