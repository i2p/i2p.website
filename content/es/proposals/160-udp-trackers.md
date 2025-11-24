---
title: "Rastreadores UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Closed"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Estado

Aprobado en revisión el 2025-06-24.
Especificación está en [UDP specification](/en/docs/spec/udp-bittorrent-announces/).
Implementado en zzzot 0.20.0-beta2.
Implementado en i2psnark a partir de API 0.9.67.
Revisar documentación de otras implementaciones para ver su estado.


## Resumen

Esta propuesta es para la implementación de rastreadores UDP en I2P.


### Historia de Cambios

Una propuesta preliminar para rastreadores UDP en I2P se publicó en nuestra página de especificaciones de bittorrent [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
en mayo de 2014; esto fue antes de nuestro proceso formal de propuestas, y nunca se implementó.
Esta propuesta se creó a principios de 2022 y simplifica la versión de 2014.

Como esta propuesta depende de datagramas replicables, se puso en espera una vez que
comenzamos a trabajar en la propuesta Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) a principios de 2023.
Esa propuesta fue aprobada en abril de 2025.

La versión de 2023 de esta propuesta especificaba dos modos, "compatibilidad" y "rápido".
Un análisis más detallado reveló que el modo rápido sería inseguro y también
ineficiente para clientes con un gran número de torrents.
Además, BiglyBT indicó una preferencia por el modo de compatibilidad.
Este modo será más fácil de implementar para cualquier rastreador o cliente que soporte
el estándar [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Aunque el modo de compatibilidad es más complejo de implementar desde cero
tamaño del cliente, tenemos código preliminar para ello iniciado en 2023.

Por lo tanto, la versión actual aquí es aún más simple para eliminar el modo rápido,
y eliminar el término "compatibilidad". La versión actual cambia al
nuevo formato Datagram2, y añade referencias al protocolo de extensión de anuncio UDP
[BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Además, se añade un campo de duración de ID de conexión a la respuesta de conexión,
para extender las eficiencias de este protocolo.


## Motivación

A medida que la base de usuarios en general y el número de usuarios de bittorrent específicamente continúa creciendo,
necesitamos hacer que rastreadores y anuncios sean más eficientes para que los rastreadores no se saturen.

Bittorrent propuso rastreadores UDP en BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) en 2008, y la gran mayoría
de los rastreadores en clearnet son ahora solo UDP.

Es difícil calcular el ahorro de ancho de banda de los datagramas frente al protocolo de transmisión.
Una solicitud replicable es de aproximadamente el mismo tamaño que un SYN de transmisión, pero la carga útil
es aproximadamente 500 bytes más pequeña porque el GET HTTP tiene una cadena de parámetros
de URL enorme de 600 bytes.
La respuesta en bruto es mucho menor que un SYN ACK de transmisión, lo que proporciona una reducción significativa
para el tráfico saliente de un rastreador.

Además, deberían haber reducciones específicas de implementación en la memoria,
ya que los datagramas requieren mucho menos estado en memoria que una conexión de transmisión.

El cifrado post-cuántico y las firmas como se prevé en [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/) aumentarán sustancialmente
la sobrecarga de estructuras cifradas y firmadas, incluyendo destinos,
leasesets, SYN de transmisión y SYN ACK. Es importante minimizar esta
sobrecarga donde sea posible antes de que la criptografía PQ sea adoptada en I2P.


## Diseño

Esta propuesta utiliza datagramas replicables2, datagramas replicables3, y datagramas en bruto,
como se define en [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/).
Datagrama2 y Datagrama3 son nuevas variantes de datagramas replicables,
definidas en la Propuesta 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagram2 añade resistencia al repetido y soporte de firma offline.
Datagram3 es más pequeño que el antiguo formato de datagrama, pero sin autenticación.


### BEP 15

Para referencia, el flujo de mensajes definido en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) es como sigue:

```
Cliente                        Rastreador
    Solicitud de conexión ------------->
      <-------------- Respuesta de conexión
    Solicitud de anuncio ------------->
      <-------------- Respuesta de anuncio
    Solicitud de anuncio ------------->
      <-------------- Respuesta de anuncio
```

La fase de conexión es necesaria para prevenir suplantación de dirección IP.
El rastreador devuelve un ID de conexión que el cliente utiliza en anuncios subsecuentes.
Este ID de conexión expira por defecto en un minuto en el cliente, y en dos minutos en el rastreador.

I2P utilizará el mismo flujo de mensajes que BEP 15,
para facilitar la adopción en bases de código de clientes existentes compatibles con UDP:
para eficiencia, y por razones de seguridad discutidas a continuación:

```
Cliente                        Rastreador
    Solicitud de conexión ------------->       (Datagrama replicable2)
      <-------------- Respuesta de conexión   (En bruto)
    Solicitud de anuncio ------------->       (Datagrama replicable3)
      <-------------- Respuesta de anuncio    (En bruto)
    Solicitud de anuncio ------------->       (Datagrama replicable3)
      <-------------- Respuesta de anuncio    (En bruto)
             ...
```

Esto potencialmente proporciona un gran ahorro de ancho de banda sobre
anuncios de transmisión (TCP).
Mientras que el Datagram2 es de aproximadamente el mismo tamaño que un SYN de transmisión,
la respuesta en bruto es mucho menor que el SYN ACK de transmisión.
Las solicitudes subsecuentes utilizan Datagram3, y las respuestas subsecuentes son en bruto.

Las solicitudes de anuncio son Datagram3 para que el rastreador no necesite
mantener una gran tabla de mapeo de IDs de conexión al destino o hash del anuncio.
En su lugar, el rastreador puede generar IDs de conexión criptográficamente
a partir del hash del remitente, la marca de tiempo actual (basada en algún intervalo),
y un valor secreto.
Cuando se recibe una solicitud de anuncio, el rastreador valida la
ID de conexión, y luego utiliza el
hash del remitente de Datagram3 como el objetivo de envío.


### Soporte de Rastreador/Cliente

Para una aplicación integrada (enrutador y cliente en un mismo proceso, por ejemplo i2psnark, y el plugin ZzzOT Java),
o para una aplicación basada en I2CP (por ejemplo BiglyBT),
debería ser fácil implementar y enrutar el tráfico de transmisión y de datagramas por separado.
Se espera que ZzzOT e i2psnark sean el primer rastreador y cliente en implementar esta propuesta.

Los rastreadores y clientes no integrados se discuten a continuación.


Rastreadores
``````````

Hay cuatro implementaciones de rastreadores I2P conocidas:

- zzzot, un plugin de enrutador Java integrado, ejecutándose en opentracker.dg2.i2p y varios otros
- tracker2.postman.i2p, ejecutándose presumiblemente detrás de un enrutador Java y túnel de servidor HTTP
- El antiguo C opentracker, portado por zzz, con soporte UDP comentado
- El nuevo C opentracker, portado por r4sas, ejecutándose en opentracker.r4sas.i2p y posiblemente otros,
  ejecutándose presumiblemente detrás de un enrutador i2pd y túnel de servidor HTTP

Para una aplicación de rastreador externa que actualmente utiliza un túnel de servidor HTTP para recibir
solicitudes de anuncio, la implementación podría ser bastante difícil.
Podría desarrollarse un túnel especializado para traducir datagramas a solicitudes/respuestas HTTP locales.
O, podría diseñarse un túnel especializado que maneje tanto solicitudes HTTP como datagramas
que reenviaría los datagramas al proceso externo.
Estas decisiones de diseño dependerán en gran medida de las implementaciones específicas de enrutador y rastreador,
y están fuera del alcance de esta propuesta.


Clientes
```````
Los clientes de torrent basados en SAM externos como qbittorrent y otros clientes basados en libtorrent
requerirían SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/) que no es soportado por i2pd.
Esto también es necesario para el soporte DHT, y es lo suficientemente complejo como para que no se haya implementado
ninguna implementación de cliente SAM de esta propuesta hasta el momento.


### Vida Útil de la Conexión

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que el ID de conexión expira en un minuto en el cliente, y en dos minutos en el rastreador.
No es configurable.
Eso limita las posibles ganancias de eficiencia, a menos que
los clientes agrupen anuncios para hacer todos ellos dentro de una ventana de un minuto.
Actualmente, i2psnark no agrupa anuncios; los distribuye, para evitar rachas de tráfico.
Se informa que los usuarios avanzados están ejecutando miles de torrents a la vez,
y enviar una ráfaga de tantos anuncios en un minuto no es realista.

Aquí, proponemos extender la respuesta de conexión para añadir un campo opcional de duración de conexión.
El valor predeterminado, si no está presente, es de un minuto. De lo contrario, la duración especificada
en segundos, será utilizada por el cliente, y el rastreador mantendrá el
ID de conexión durante un minuto más.


### Compatibilidad con BEP 15

Este diseño mantiene la compatibilidad con [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tanto como sea posible
para limitar los cambios requeridos en clientes y rastreadores existentes.

El único cambio requerido es el formato de información del par en la respuesta de anuncio.
La adición del campo de duración en la respuesta de conexión no es obligatoria
pero es muy recomendable para la eficiencia, como se explicó anteriormente.


### Análisis de Seguridad

Un objetivo importante de un protocolo de anuncio UDP es prevenir la suplantación de direcciones.
El cliente debe realmente existir y tener un leaseset real.
Debe tener túneles de entrada para recibir la Respuesta de Conexión.
Estos túneles podrían ser de cero hop y construidos instantáneamente, pero eso
expondría al creador.
Este protocolo logra ese objetivo.


### Problemas

- Esta propuesta no soporta destinos cegados,
  pero puede ser extendida para hacerlo. Véase abajo.


## Especificación

### Protocolos y Puertos

Datagrama replicable2 utiliza el protocolo I2CP 19;
Datagrama replicable3 utiliza el protocolo I2CP 20;
datagramas en bruto utilizan el protocolo I2CP 18.
Las solicitudes pueden ser Datagram2 o Datagram3. Las respuestas son siempre en bruto.
El formato de datagrama replicable anterior ("Datagrama1") utilizando el protocolo I2CP 17
NO debe usarse para solicitudes o respuestas; deben descartarse si se reciben
en los puertos de solicitud/respuesta. Note que el protocolo de Datagram1 17
se sigue utilizando para el protocolo DHT.

Las solicitudes utilizan el "to port" I2CP de la URL de anuncio; véase más abajo.
El "from port" de la solicitud es elegido por el cliente, pero debería ser no cero,
y un puerto diferente de los utilizados por DHT, para que las respuestas
puedan ser clasificadas fácilmente.
Los rastreadores deberían rechazar solicitudes recibidas en el puerto incorrecto.

Las respuestas utilizan el "to port" de I2CP de la solicitud.
El "from port" de la solicitud es el "to port" de la solicitud.


### URL de Anuncio

El formato de URL de anuncio no está especificado en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html),
pero como en clearnet, las URLs de anuncio UDP son del form "udp://host:port/path".
La ruta es ignorada y puede estar vacía, pero típicamente es "/announce" en clearnet.
La parte :port siempre debería estar presente, sin embargo,
si se omite la parte ":port", usar un puerto I2CP predeterminado de 6969,
ya que es el puerto común en clearnet.
También pueden haber parámetros CGI &a=b&c=d añadidos,
esos pueden ser procesados y proporcionados en la solicitud de anuncio, ver [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Si no hay parámetros o rutas, también se puede omitir la barra final,
como se implica en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).


### Formatos de Datagramas

Todos los valores se envían en orden de byte de red (big endian).
No espere que los paquetes tengan exactamente un cierto tamaño.
Las futuras extensiones podrían aumentar el tamaño de los paquetes.


Solicitud de Conexión
```````````````````

Cliente a rastreador.
16 bytes. Debe ser un Datagram2 replicable. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.


```
Offset  Size            Nombre            Valor
  0       64-bit integer  protocol_id     0x41727101980 // constante mágica
  8       32-bit integer  acción          0 // conectar
  12      32-bit integer  transaction_id
```



Respuesta de Conexión
````````````````

Rastreador al cliente.
16 o 18 bytes. Debe ser en bruto. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se señala a continuación.


```
Offset  Size            Nombre            Valor
  0       32-bit integer  acción          0 // conectar
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  duración        opcional  // Cambio de BEP 15
```

La respuesta DEBE ser enviada al "to port" de I2CP que se recibió como el "from port" de la solicitud.

El campo de duración es opcional e indica la duración del ID de conexión del cliente en segundos.
El valor predeterminado es 60, y el mínimo si está especificado es 60.
El máximo es 65535 o alrededor de 18 horas.
El rastreador debería mantener el ID de conexión durante 60 segundos más que la duración del cliente.


Solicitud de Anuncio
````````````````

Cliente a rastreador.
98 bytes como mínimo. Debe ser un Datagram3 replicable. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se señala a continuación.

El ID de conexión es como se recibe en la respuesta de conexión.



```
Offset  Size            Nombre            Valor
  0       64-bit integer  connection_id
  8       32-bit integer  acción          1     // anunciar
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  descargado
  64      64-bit integer  restante
  72      64-bit integer  cargado
  80      32-bit integer  evento           0     // 0: ninguno; 1: completado; 2: comenzado; 3: detenido
  84      32-bit integer  dirección IP      0     // por defecto
  88      32-bit integer  clave
  92      32-bit integer  num_want        -1    // por defecto
  96      16-bit integer  puerto
  98      varía           opciones     opcional  // Según lo especificado en BEP 41
```

Cambios de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- clave es ignorada
- puerto probablemente es ignorado
- La sección de opciones, si está presente, es como se define en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La respuesta DEBE ser enviada al "to port" de I2CP que se recibió como el "from port" de la solicitud.
No utilice el puerto de la solicitud de anuncio.


Respuesta de Anuncio
````````````````

Rastreador al cliente.
20 bytes como mínimo. Debe ser en bruto. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepto como se señala a continuación.



```
Offset  Size            Nombre            Valor
  0           32-bit integer  acción          1 // anunciar
  4           32-bit integer  transaction_id
  8           32-bit integer  intervalo
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    hashes binarios     // Cambio de BEP 15
  ...                                             // Cambio de BEP 15
```

Cambios de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- En lugar de IPv4+puerto de 6 bytes o IPv6+puerto de 18 bytes, devolvemos
  un múltiplo de respuestas "compactas" de 32 bytes con los hashes binarios SHA-256 de los pares.
  Como con las respuestas compactas TCP, no incluimos un puerto.

La respuesta DEBE ser enviada al "to port" de I2CP que se recibió como el "from port" de la solicitud.
No utilice el puerto de la solicitud de anuncio.

Los datagramas de I2P tienen un tamaño máximo muy grande de alrededor de 64 KB;
sin embargo, para una entrega confiable, se deben evitar datagramas de más de 4 KB.
Para la eficiencia de ancho de banda, los rastreadores deberían probablemente limitar los pares máximos
a alrededor de 50, lo que corresponde a alrededor de un paquete de 1600 bytes antes de la sobrecarga
en varias capas, y debería estar dentro de un límite de carga útil de mensaje de dos túneles
después de la fragmentación.

Como en BEP 15, no hay una cuenta incluida del número de direcciones de pares
(IP/puerto para BEP 15, hashes aquí) para seguir.
Aunque no está contemplado en BEP 15, un marcador de fin de pares
de todos ceros podría definirse para indicar que la información de pares está completa
y algunos datos de extensión siguen.

Para que la extensión sea posible en el futuro, los clientes deberían ignorar
un hash de 32 bytes con todos ceros, y cualquier dato que lo siga.
Los rastreadores deberían rechazar anuncios de un hash de todos ceros,
aunque ese hash ya está prohibido por los enrutadores Java.


Scrape
``````

La solicitud/respuesta de Scrape de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) no es requerida por esta propuesta,
pero puede ser implementada si se desea, no se requieren cambios.
El cliente debe adquirir un ID de conexión primero.
La solicitud de Scrape es siempre un Datagram3 replicable.
La respuesta de Scrape es siempre en bruto.


Respuesta de Error
````````````````

Rastreador al cliente.
8 bytes como mínimo (si el mensaje está vacío).
Debe ser en bruto. Igual que en [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sin cambios.

```

Offset  Size            Nombre            Valor
  0       32-bit integer  acción          3 // error
  4       32-bit integer  transaction_id
  8       string          mensaje

```



## Extensiones

No se incluyen bits de extensión o un campo de versión.
Los clientes y rastreadores no deberían asumir que los paquetes tienen un cierto tamaño.
De esta manera, se pueden añadir campos adicionales sin romper la compatibilidad.
El formato de extensiones definido en [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) se recomienda si es necesario.

La respuesta de conexión se modifica para añadir un campo de duración de ID de conexión opcional.

Si se requiere soporte para destinos cegados, podemos ya sea añadir la
dirección de 35 bytes cegada al final de la solicitud de anuncio,
o solicitar hashes cegados en las respuestas,
utilizando el formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parámetros TBD).
El conjunto de direcciones de pares de 35 bytes cegadas podría añadirse al final de la respuesta de anuncio,
tras un hash de 32 bytes de todos ceros.


## Directrices de implementación

Vea la sección de diseño arriba para una discusión de los desafíos para
clientes y rastreadores no integrados, no-I2CP.


### Clientes

Para un determinado nombre de host del rastreador, un cliente debería preferir URLs UDP sobre HTTP,
y no debería anunciarse a ambos.

Clientes con soporte existente de BEP 15 deberían requerir sólo pequeñas modificaciones.

Si un cliente soporta DHT u otros protocolos de datagrama, probablemente debería
seleccionar un puerto diferente como el "from port" de la solicitud para que las respuestas
regresen a ese puerto y no se mezclen con mensajes DHT.
El cliente sólo recibe datagramas en bruto como respuestas.
Los rastreadores nunca enviarán un datagrama replicable2 al cliente.

Clientes con una lista predeterminada de opentrackers deberían actualizar la lista para
añadir URLs UDP una vez que los opentrackers conocidos soporto de UDP.

Los clientes pueden o no implementar retransmisión de solicitudes.
Las retransmisiones, si se implementan, deberían usar un tiempo de espera inicial
de al menos 15 segundos, y duplicar el tiempo de espera para cada retransmisión
(retiro exponencial).

Los clientes deben retirarse después de recibir una respuesta de error.


### Rastreadores

Los rastreadores con soporte existente de BEP 15 deberían requerir solo pequeñas modificaciones.
Esta propuesta difiere de la propuesta de 2014, en que el rastreador
debe soportar la recepción de datagrama replicable2 y datagrama3 en el mismo puerto.

Para minimizar los requerimientos de recursos del rastreador,
este protocolo está diseñado para eliminar cualquier requisito de que el rastreador
almacene mapeos de hashes de clientes a IDs de conexión para su validación posterior.
Esto es posible porque el paquete de solicitud de anuncio es un paquete replicable
Datagrama3, por lo que contiene el hash del remitente.

Una implementación recomendada es:

- Definir la época actual como el tiempo actual con una resolución de la duración de la conexión,
  ``época = ahora / duración``.
- Definir una función de hash criptográfica ``H(secreto, clientehash, época)`` que genere
  un output de 8 bytes.
- Generar el constante aleatoria secreta utilizada para todas las conexiones.
- Para respuestas de conexión, generar ``connection_id = H(secreto, clientehash, época)``
- Para solicitudes de anuncio, validar el ID de conexión recibido en la época actual verificando
  ``connection_id == H(secreto, clientehash, época) || connection_id == H(secreto, clientehash, época - 1)``


## Migración

Los clientes existentes no soportan URLs de anuncio UDP y las ignoran.

Los rastreadores existentes no soportan la recepción de datagramas replicables o en bruto, serán descartados.

Esta propuesta es completamente opcional. Ni clientes ni rastreadores están requeridos para implementarla en ningún momento.


## Despliegue

Se espera que las primeras implementaciones sean en ZzzOT e i2psnark.
Serán utilizados para pruebas y verificación de esta propuesta.

Otras implementaciones seguirán como se desee después de que las pruebas y la verificación estén completas.


