---
title: "Anuncios de BitTorrent por UDP"
description: "Especificación del protocolo para las solicitudes announce (solicitud de anuncio del rastreador) de rastreadores de BitTorrent basados en UDP en I2P"
slug: "udp-bittorrent-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

Esta especificación documenta el protocolo para los anuncios de BitTorrent por UDP en I2P. Para la especificación general de BitTorrent en I2P, consulta la [documentación de BitTorrent sobre I2P](/docs/applications/bittorrent/). Para conocer los antecedentes e información adicional sobre el desarrollo de esta especificación, consulta la [Propuesta 160](/proposals/160-udp-trackers/).

Este protocolo fue aprobado formalmente el 24 de junio de 2025 e implementado en la versión 2.10.0 de I2P (API 0.9.67), publicada el 8 de septiembre de 2025. La compatibilidad con UDP tracker (servidor de seguimiento) está actualmente operativa en la red I2P, con múltiples trackers de producción y compatibilidad total del cliente i2psnark.

## Diseño

Esta especificación utiliza datagram2 y datagram3 con posibilidad de respuesta (repliable), así como datagramas en bruto, tal como se definen en la [Especificación de Datagramas de I2P](/docs/api/datagrams/). Datagram2 y Datagram3 son variantes de los datagramas con posibilidad de respuesta (repliable), definidos en la [Propuesta 163](/proposals/163-datagram2/). Datagram2 añade resistencia a ataques de repetición (replay) y compatibilidad con firmas fuera de línea. Datagram3 es más pequeño que el formato antiguo de datagrama, pero carece de autenticación.

### BEP 15 (Propuesta de mejora de BitTorrent)

Como referencia, el flujo de mensajes definido en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) es el siguiente:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
La fase de conexión es necesaria para evitar la suplantación de direcciones IP. El rastreador devuelve un ID de conexión que el cliente utiliza en anuncios posteriores. Este ID de conexión caduca de forma predeterminada en un minuto en el cliente y en dos minutos en el rastreador.

I2P utiliza el mismo flujo de mensajes que BEP 15, para facilitar la adopción en bases de código de cliente compatibles con UDP, para mayor eficiencia y por razones de seguridad que se detallan a continuación:

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
Esto potencialmente proporciona un gran ahorro de ancho de banda frente a los anuncios por streaming (TCP). Si bien el Datagram2 (tipo de datagrama) tiene aproximadamente el mismo tamaño que un SYN de streaming, la respuesta sin formato es mucho más pequeña que el SYN ACK de streaming. Las solicitudes posteriores usan Datagram3 (tipo de datagrama), y las respuestas posteriores son sin formato.

Las solicitudes de anuncio son Datagram3 (formato de datagrama de I2P versión 3) para que el rastreador no tenga que mantener una gran tabla de correspondencias de ID de conexión con destino de anuncio o hash. En su lugar, el rastreador puede generar los ID de conexión criptográficamente a partir del hash del remitente, la marca de tiempo actual (basada en algún intervalo) y un valor secreto. Cuando se recibe una solicitud de anuncio, el rastreador valida el ID de conexión y luego usa el hash del remitente de Datagram3 como destino de envío.

### Duración de la conexión

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que el ID de conexión caduca en un minuto en el cliente y en dos minutos en el tracker (rastreador). No es configurable. Eso limita las posibles ganancias de eficiencia, a menos que los clientes agrupen las solicitudes announce (peticiones del cliente al tracker) para hacerlas todas dentro de una ventana de un minuto. i2psnark no agrupa actualmente las solicitudes announce; las distribuye para evitar ráfagas de tráfico. Se informa que los usuarios avanzados ejecutan miles de torrents a la vez, y concentrar tantas solicitudes announce en un minuto no es realista.

Aquí proponemos extender la respuesta de conexión para añadir un campo opcional de tiempo de vida de la conexión. El valor predeterminado, si no está presente, es de un minuto. De lo contrario, el cliente usará el tiempo de vida especificado en segundos, y el rastreador mantendrá el ID de conexión durante un minuto más.

### Compatibilidad con BEP 15 (Propuesta de Mejora de BitTorrent 15)

Este diseño mantiene la compatibilidad con [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) en la medida de lo posible para limitar los cambios necesarios en los clientes y rastreadores existentes.

El único cambio obligatorio es el formato de la información de pares en la respuesta de anuncio. La incorporación del campo lifetime (vida útil) en la respuesta de conexión no es obligatoria, pero se recomienda encarecidamente para mayor eficiencia, como se explicó arriba.

### Análisis de seguridad

Un objetivo importante de un protocolo de anuncio por UDP es impedir la suplantación de direcciones. El cliente debe existir realmente y adjuntar un leaseSet real. Debe tener tunnels de entrada para recibir la Connect Response (respuesta de conexión). Estos tunnels podrían ser de cero saltos y construirse al instante, pero eso expondría al creador. Este protocolo cumple ese objetivo.

### Problemas

Este protocolo no admite blinded destinations (destinos ocultados), pero puede ampliarse para hacerlo. Véase más abajo.

## Especificación

### Protocolos y puertos

Datagram2 repliable (admite respuesta) utiliza el protocolo I2CP 19; Datagram3 repliable utiliza el protocolo I2CP 20; los datagramas sin formato utilizan el protocolo I2CP 18. Las solicitudes pueden ser Datagram2 o Datagram3. Las respuestas siempre son sin formato. El formato de datagrama repliable ("Datagram1") más antiguo que utiliza el protocolo I2CP 17 NO debe usarse para solicitudes ni respuestas; deben descartarse si se reciben en los puertos de solicitud/respuesta. Tenga en cuenta que el protocolo 17 de Datagram1 sigue utilizándose para el protocolo DHT.

Las solicitudes usan el "to port" (puerto de destino) de I2CP indicado en la URL de anuncio; véase más abajo. El "from port" (puerto de origen) de la solicitud lo elige el cliente, pero debe ser distinto de cero y no debe coincidir con los puertos usados por DHT, para que las respuestas puedan clasificarse fácilmente. Los rastreadores deberían rechazar las solicitudes recibidas en el puerto incorrecto.

Las respuestas usan el "to port" de I2CP (puerto de destino) de la solicitud. El "from port" (puerto de origen) de la respuesta es el "to port" de la solicitud.

### URL de anuncio

El formato de la URL de announce no está especificado en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), pero, como en clearnet (internet abierta), las URLs de announce por UDP tienen la forma "udp://host:port/path". La ruta se ignora y puede estar vacía, pero normalmente es "/announce" en clearnet. La parte :port debe estar siempre presente; sin embargo, si se omite la parte ":port", use un puerto I2CP predeterminado de 6969, ya que ese es el puerto común en clearnet. También pueden añadirse parámetros CGI &a=b&c=d; estos pueden procesarse y proporcionarse en la solicitud de announce, vea [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Si no hay parámetros ni ruta, la / final también puede omitirse, como se infiere de [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Formatos de datagramas

Todos los valores se envían en orden de bytes de red (big endian, más significativo primero). No espere que los paquetes tengan exactamente un tamaño determinado. Las extensiones futuras podrían aumentar el tamaño de los paquetes.

#### Solicitud de conexión

Cliente al tracker. 16 bytes. Debe ser un Datagram2 (formato de datagrama de segunda generación de I2P) al que se pueda responder. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Respuesta de conexión

Del rastreador al cliente. 16 o 18 bytes. Debe ser sin procesar. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se indica a continuación.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
La respuesta DEBE enviarse al "to port" de I2CP que se recibió como el "from port" de la solicitud.

El campo lifetime es opcional e indica, en segundos, la vida útil del connection_id para el cliente. El valor predeterminado es 60, y el mínimo, si se especifica, es 60. El máximo es 65535, o aproximadamente 18 horas. El rastreador debería mantener el connection_id durante 60 segundos más que la vida útil indicada por el cliente.

#### Solicitud de anuncio

Del cliente al rastreador. 98 bytes como mínimo. Debe ser un Datagram3 (tipo de datagrama de I2P v3) que admita respuesta. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) salvo lo indicado a continuación.

El connection_id es el recibido en la respuesta de conexión.

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
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Cambios con respecto a [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- la clave se ignora
- la dirección IP no se utiliza
- el puerto probablemente se ignore, pero debe ser el mismo que el puerto de origen de I2CP
- La sección de opciones, si está presente, es la definida en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La respuesta DEBE enviarse al "to port" de I2CP que se recibió como el "from port" de la solicitud. No uses el puerto de la solicitud de anuncio.

#### Respuesta de anuncio

Del tracker al cliente. 20 bytes como mínimo. Debe ser en bruto. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) salvo lo indicado a continuación.

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
Cambios con respecto a [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- En lugar de IPv4+puerto de 6 bytes o IPv6+puerto de 18 bytes, devolvemos un número múltiplo de "respuestas compactas" de 32 bytes con los hashes binarios SHA-256 de los pares. Como con las respuestas compactas TCP, no incluimos un puerto.

La respuesta DEBE enviarse al "to port" de I2CP que se recibió como el "from port" de la solicitud. No utilice el puerto de la solicitud de anuncio.

Los datagramas de I2P tienen un tamaño máximo muy grande de aproximadamente 64 KB; sin embargo, para una entrega fiable, deberían evitarse los datagramas mayores de 4 KB. Por eficiencia en el uso del ancho de banda, los rastreadores probablemente deberían limitar el número máximo de pares a aproximadamente 50, lo que corresponde a un paquete de aproximadamente 1600 bytes sin contar la sobrecarga de las distintas capas, y debería quedar dentro del límite de carga útil de dos mensajes de tunnel tras la fragmentación.

Como en BEP 15, no se incluye un contador del número de direcciones de pares (IP/puerto en BEP 15, hashes aquí) que siguen. Aunque no se contempla en BEP 15, podría definirse un marcador de fin de pares de todos ceros para indicar que la información de pares está completa y que a continuación siguen algunos datos de extensión.

Para que dicha extensión sea posible en el futuro, los clientes deberían ignorar un hash de 32 bytes compuesto íntegramente por ceros, y cualquier dato que lo siga. Los rastreadores deberían rechazar anuncios provenientes de un hash compuesto íntegramente por ceros, aunque ese hash ya está prohibido por los routers Java.

#### Scrape (extracción automatizada de datos)

La solicitud/respuesta de scrape (consulta de estadísticas del tracker) de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) no es obligatoria según esta especificación, pero puede implementarse si se desea, sin requerir cambios. El cliente debe obtener primero un ID de conexión. La solicitud de scrape es siempre repliable (se puede responder directamente) Datagram3. La respuesta de scrape es siempre raw (no repliable).

#### Respuesta de error

Del tracker al cliente. 8 bytes como mínimo (si el mensaje está vacío). Debe ser en bruto. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Extensiones

No se incluyen bits de extensión ni un campo de versión. Los clientes y los rastreadores no deben suponer que los paquetes tienen un tamaño determinado. De este modo, se pueden añadir campos adicionales sin romper la compatibilidad. Se recomienda el formato de extensiones definido en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) si se requiere.

La respuesta de conexión se modifica para añadir una vida útil opcional del ID de conexión.

Si se requiere compatibilidad con destinos cegados, podemos o bien añadir la dirección cegada de 35 bytes al final de la solicitud announce, o solicitar hashes cegados en las respuestas, usando el formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parámetros por definir). El conjunto de direcciones de pares de 35 bytes cegadas podría añadirse al final de la respuesta announce, después de un hash de 32 bytes de todos ceros.

## Directrices de implementación

Consulte la sección de diseño anterior para un análisis de los desafíos de los clientes y los trackers no integrados y que no usan I2CP.

### Clientes

Para un nombre de host de tracker dado, un cliente debería preferir URLs UDP en lugar de URLs HTTP y no debería anunciarse a ambos.

Los clientes que ya cuenten con soporte para BEP 15 solo deberían requerir pequeñas modificaciones.

Si un cliente admite DHT (tabla hash distribuida) u otros protocolos de datagramas, probablemente debería seleccionar un puerto diferente como el "from port" de la solicitud para que las respuestas lleguen a ese puerto y no se mezclen con los mensajes de DHT. El cliente solo recibe datagramas en bruto como respuestas. Los trackers nunca enviarán un repliable datagram2 al cliente.

Los clientes con una lista predeterminada de opentrackers (rastreador abierto de BitTorrent) deben actualizarla para añadir URLs UDP una vez que se confirme que los opentrackers conocidos admiten UDP.

Es posible que los clientes implementen o no la retransmisión de solicitudes. Las retransmisiones, si se implementan, deberían usar un tiempo de espera inicial de al menos 15 segundos y duplicar el tiempo de espera en cada retransmisión (backoff exponencial).

Los clientes deben esperar antes de volver a intentarlo después de recibir una respuesta de error.

### Rastreadores

Los trackers con compatibilidad existente con BEP 15 deberían requerir solo pequeñas modificaciones. Esta especificación difiere de la propuesta de 2014 en que el tracker debe admitir la recepción de datagram2 (formato de datagrama v2) y datagram3 (formato de datagrama v3) con posibilidad de respuesta en el mismo puerto.

Para minimizar los requisitos de recursos del tracker, este protocolo está diseñado para eliminar cualquier requisito de que el tracker almacene mapeos de hashes de los clientes a ID de conexión para su validación posterior. Esto es posible porque el paquete de solicitud announce (anuncio) es un paquete Datagram3 al que se puede responder, por lo que contiene el hash del remitente.

Una implementación recomendada es:

- Defina la época actual como el tiempo actual con una resolución igual a la duración de la conexión, `epoch = now / lifetime`.
- Defina una función hash criptográfica `H(secret, clienthash, epoch)` que genere una salida de 8 bytes.
- Genere el secreto constante aleatorio utilizado para todas las conexiones.
- Para las respuestas de conexión, genere `connection_id = H(secret, clienthash, epoch)`
- Para las solicitudes de anuncio, valide el ID de conexión recibido en la época actual verificando `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Estado del despliegue

Este protocolo fue aprobado el 24 de junio de 2025 y está plenamente operativo en la red I2P desde septiembre de 2025.

### Implementaciones actuales

**i2psnark**: El soporte completo para rastreadores UDP se incluye en la versión 2.10.0 de I2P (API 0.9.67), publicada el 8 de septiembre de 2025. Todas las instalaciones de I2P a partir de esta versión incluyen de forma predeterminada la compatibilidad con rastreadores UDP.

**zzzot tracker**: La versión 0.20.0-beta2 y posteriores admiten anuncios por UDP. A fecha de octubre de 2025, los siguientes trackers (servidores de seguimiento) de producción están operativos: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Notas de compatibilidad de clientes

**Limitaciones de SAM v3.3**: Los clientes externos de BitTorrent que usan SAM (Mensajería Anónima Simple) requieren soporte de SAM v3.3 para Datagram2/3. Esto está disponible en Java I2P pero actualmente no está soportado por i2pd (la implementación de I2P en C++), lo que podría limitar la adopción en clientes basados en libtorrent como qBittorrent.

**Clientes I2CP**: Los clientes que utilizan I2CP directamente (como BiglyBT) pueden implementar soporte para rastreadores UDP sin las limitaciones de SAM.

## Referencias

- **[BEP15]**: [Protocolo de tracker UDP de BitTorrent](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Extensiones del protocolo de tracker UDP](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Especificación de datagramas de I2P](/docs/api/datagrams/)
- **[Prop160]**: [Propuesta de trackers UDP](/proposals/160-udp-trackers/)
- **[Prop163]**: [Propuesta de Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent sobre I2P](/docs/applications/bittorrent/)
