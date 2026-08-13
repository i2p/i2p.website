---
title: "Bittorrent sobre I2P"
description: "Especificaciones de protocolo para clientes BitTorrent y trackers en I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Hay varios clientes y trackers de BitTorrent en I2P. Como el direccionamiento de I2P utiliza un Destination en lugar de una IP y puerto, se requieren cambios menores en el software del tracker y cliente para operar en I2P. Estos cambios se especifican a continuación. Observe cuidadosamente las pautas para la compatibilidad con clientes y trackers de I2P más antiguos.

Esta página especifica los detalles del protocolo comunes a todos los clientes y trackers. Los clientes y trackers específicos pueden implementar otras características o protocolos únicos.

Damos la bienvenida a portabilizaciones adicionales de software de cliente y tracker a I2P.

---

## Orientación General para Desarrolladores

La mayoría de clientes bittorrent que no son de Java se conectarán a I2P a través de [SAMv3](/docs/api/samv3/). Las sesiones SAM (o dentro de I2P, grupos de túneles o conjuntos de túneles) están diseñadas para ser duraderas. La mayoría de clientes bittorrent solo necesitarán una sesión, creada al inicio y cerrada al salir. I2P es diferente de Tor, donde los circuitos pueden crearse y descartarse rápidamente. Piensa cuidadosamente y consulta con los desarrolladores de I2P antes de diseñar tu aplicación para usar más de una o dos sesiones simultáneas, o para crearlas y descartarlas rápidamente. Los clientes bittorrent no deben crear una sesión única para cada conexión. Diseña tu cliente para usar la misma sesión para anuncios y conexiones de cliente.

Además, asegúrese de que la configuración de su cliente (y la orientación a los usuarios sobre la configuración del router, o los valores predeterminados del router si incluye uno) resulte en que sus usuarios contribuyan con más recursos a la red de los que consumen. I2P es una red peer-to-peer, y la red no puede sobrevivir si una aplicación popular lleva la red a una congestión permanente.

No proporciones soporte para bittorrent a través de un outproxy I2P hacia la clearnet ya que probablemente será bloqueado. Consulta con los operadores de outproxy para obtener orientación.

Las implementaciones de router Java I2P e i2pd son independientes y tienen diferencias menores en comportamiento, soporte de características y configuraciones predeterminadas. Por favor, prueba tu aplicación con la versión más reciente de ambos routers.

SAM de i2pd está habilitado por defecto; SAM de Java I2P no lo está. Proporciona instrucciones a tus usuarios sobre cómo habilitar SAM en Java I2P (a través de /configclients en la consola del router), y/o proporciona un buen mensaje de error al usuario si falla la conexión inicial, por ejemplo "asegúrate de que I2P esté ejecutándose y que la interfaz SAM esté habilitada".

Los routers Java I2P e i2pd tienen valores predeterminados diferentes para las cantidades de tunnel. El valor predeterminado de Java es 2 y el valor predeterminado de i2pd es 5. Para la mayoría de casos con ancho de banda bajo a medio y recuentos de conexión bajos a medios, 3 es suficiente. Por favor especifica la cantidad de tunnel en el mensaje SESSION CREATE para obtener un rendimiento consistente con los routers Java I2P e i2pd.

I2P soporta múltiples tipos de firma y cifrado. Por compatibilidad, I2P usa por defecto tipos antiguos e ineficientes, por lo que todos los clientes deberían especificar tipos más nuevos.

Si usas SAM, el tipo de firma se especifica en los comandos DEST GENERATE y SESSION CREATE (para transitorio). Todos los clientes deben establecer SIGNATURE_TYPE=7 (Ed25519).

El tipo de cifrado se especifica en el comando SAM SESSION CREATE o en las opciones i2cp. Se permiten múltiples tipos de cifrado. Algunos trackers soportan ECIES-X25519, algunos soportan ElGamal, y algunos soportan ambos. Los clientes deberían establecer i2cp.leaseSetEncType=4,0 (para ECIES-X25519 y ElGamal) para poder conectarse a ambos.

El soporte DHT requiere SAMv3.3 PRIMARY y SUBSESSIONS para TCP y UDP sobre la misma sesión. Esto requerirá un esfuerzo de desarrollo sustancial del lado del cliente, a menos que el cliente esté escrito en Java. i2pd actualmente no soporta SAMv3.3. libtorrent actualmente no soporta SAMv3.3.

Sin soporte para DHT, es posible que desees anunciar automáticamente a una lista configurable de trackers abiertos conocidos para que los enlaces magnet funcionen. Consulta con los usuarios de I2P para obtener información sobre los trackers abiertos que están actualmente en funcionamiento y mantén tus valores predeterminados actualizados. Soportar la extensión i2p_pex también ayudará a aliviar la falta de soporte para DHT.

Para obtener más orientación para desarrolladores sobre cómo asegurar que tu aplicación use solo los recursos que necesita, consulta la [especificación SAMv3](/docs/api/samv3/) y [nuestra guía para incluir I2P con tu aplicación](/docs/applications/embedding/). Contacta a los desarrolladores de I2P o i2pd para obtener más asistencia.

---

## Anuncios

Los clientes generalmente incluyen un parámetro falso port=6881 en el anuncio, para compatibilidad con trackers más antiguos. Los trackers pueden ignorar el parámetro port, y no deberían requerirlo.

El parámetro ip es la base 64 del [Destination](/docs/specs/common-structures/#struct_Destination) del cliente, usando el alfabeto Base 64 de I2P [A-Z][a-z][0-9]-~. Los [Destinations](/docs/specs/common-structures/#struct_Destination) son de 387+ bytes, por lo que la Base 64 es de 516+ bytes. Los clientes generalmente añaden ".i2p" al Destination Base 64 para compatibilidad con trackers más antiguos. Los trackers no deberían requerir un ".i2p" añadido.

Los otros parámetros son los mismos que en bittorrent estándar.

Los destinos actuales para clientes son de 387 o más bytes (516 o más en codificación Base 64). Un máximo razonable a asumir, por ahora, es de 475 bytes. Como el tracker debe decodificar el Base64 para entregar respuestas compactas (ver abajo), el tracker probablemente debería decodificar y rechazar Base64 defectuoso cuando se anuncie.

El tipo de respuesta predeterminado es no compacto. Los clientes pueden solicitar una respuesta compacta con el parámetro compact=1. Un tracker puede, pero no está obligado a, devolver una respuesta compacta cuando se solicite. Nota: Todos los trackers populares ahora admiten respuestas compactas y al menos uno requiere compact=1 en el anuncio. Todos los clientes deberían solicitar y admitir respuestas compactas.

Se recomienda encarecidamente a los desarrolladores de nuevos clientes I2P que implementen anuncios a través de su propio tunnel en lugar del proxy cliente HTTP en el puerto 4444. Hacerlo es más eficiente y permite el cumplimiento de destino por parte del tracker (ver más abajo).

La especificación para anuncios UDP se finalizó en junio de 2025. El soporte en varios clientes I2P y trackers se implementará gradualmente más adelante en 2025. Consulta a continuación para obtener información adicional.

---

## Respuestas de Tracker No Compactas

Nota: Obsoleto. Todos los trackers populares ahora soportan respuestas compactas y al menos uno requiere compact=1 en el anuncio. Todos los clientes deberían solicitar y soportar respuestas compactas.

La respuesta no compacta es igual que en bittorrent estándar, con una "ip" I2P. Esta es una larga "cadena DNS" codificada en base64, probablemente con un sufijo ".i2p".

Los trackers generalmente incluyen una clave de puerto falsa, o usan el puerto del anuncio, para compatibilidad con clientes más antiguos. Los clientes deben ignorar el parámetro de puerto, y no deberían requerirlo.

El valor de la clave ip es el base 64 del [Destination](/docs/specs/common-structures/#struct_Destination) del cliente, como se describe arriba. Los trackers generalmente añaden ".i2p" al Destination en Base 64 si no estaba en el ip del announce, para compatibilidad con clientes más antiguos. Los clientes no deberían requerir un ".i2p" añadido en las respuestas.

Las demás claves y valores de respuesta son los mismos que en el bittorrent estándar.

---

## Respuestas de Tracker Compactas

En la respuesta compacta, el valor de la clave del diccionario "peers" es una cadena de bytes única, cuya longitud es un múltiplo de 32 bytes. Esta cadena contiene los [Hashes SHA-256 de 32 bytes](/docs/specs/common-structures/#type_Hash) concatenados de los [Destinations](/docs/specs/common-structures/#struct_Destination) binarios de los peers. Este hash debe ser calculado por el tracker, a menos que se use el enforcement de destination (ver más abajo), en cuyo caso el hash entregado en las cabeceras HTTP X-I2P-DestHash o X-I2P-DestB32 puede ser convertido a binario y almacenado. La clave peers puede estar ausente, o el valor de peers puede tener longitud cero.

Aunque el soporte para respuestas compactas es opcional tanto para clientes como para trackers, se recomienda encarecidamente ya que reduce el tamaño nominal de respuesta en más del 90%.

---

## Aplicación de Destino

Algunos, pero no todos, los clientes bittorrent de I2P anuncian a través de sus propios tunnels. Los trackers pueden optar por prevenir la suplantación requiriendo esto, y verificando el [Destination](/docs/specs/common-structures/#struct_Destination) del cliente usando cabeceras HTTP añadidas por el tunnel I2PTunnel HTTP Server. Las cabeceras son X-I2P-DestHash, X-I2P-DestB64, y X-I2P-DestB32, que son diferentes formatos para la misma información. Estas cabeceras no pueden ser suplantadas por el cliente. Un tracker que requiera destinations no necesita requerir el parámetro ip announce en absoluto.

Como varios clientes usan el proxy HTTP en lugar de su propio tunnel para anuncios, la aplicación de destinos impedirá el uso por parte de esos clientes a menos que o hasta que esos clientes se conviertan para anunciar a través de su propio tunnel.

Desafortunadamente, a medida que la red crezca, también aumentará la cantidad de malicia, por lo que esperamos que todos los trackers eventualmente apliquen restricciones de destinos. Tanto los desarrolladores de trackers como de clientes deberían anticipar esto.

---

## Anunciar Nombres de Host

Los nombres de host de URL de anuncio en archivos torrent generalmente siguen los [estándares de nomenclatura de I2P](/docs/overview/naming/). Además de los nombres de host de las libretas de direcciones y los nombres de host Base 32 ".b32.i2p", se debe soportar el Destination Base 64 completo (con o sin ".i2p" añadido). Los trackers no abiertos deben reconocer su propio nombre de host en cualquiera de estos formatos.

Para preservar el anonimato, los clientes generalmente deberían ignorar las URLs de anuncio que no sean de I2P en los archivos torrent.

---

## Conexiones de Cliente

Las conexiones cliente-a-cliente utilizan el protocolo estándar sobre TCP. No hay clientes I2P conocidos que actualmente soporten comunicación uTP.

I2P usa [Destinations](/docs/specs/common-structures/#struct_Destination) de 387+ bytes para las direcciones, como se explicó anteriormente.

Si el cliente solo tiene el hash del destino (como de una respuesta compacta o PEX), debe realizar una búsqueda codificándolo con Base 32, agregando ".b32.i2p", y consultando el Servicio de Nombres, el cual devolverá el Destination completo si está disponible.

Si el cliente tiene el Destination completo de un peer que recibió en una respuesta no compacta, debe usarlo directamente en la configuración de la conexión. No conviertas un Destination de vuelta a un hash Base 32 para la búsqueda, esto es bastante ineficiente.

---

## Prevención de Red Cruzada

Para preservar el anonimato, los clientes bittorrent de I2P generalmente no admiten anuncios o conexiones de pares que no sean de I2P. Los proxies de salida HTTP de I2P a menudo bloquean los anuncios. No se conocen proxies de salida SOCKS que admitan tráfico bittorrent.

Para prevenir el uso por parte de clientes que no sean I2P a través de un proxy HTTP entrante, los trackers de I2P a menudo bloquean accesos o anuncios que contengan una cabecera HTTP X-Forwarded-For. Los trackers deberían rechazar anuncios de red estándar con IPs IPv4 o IPv6, y no entregarlos en las respuestas.

---

## PEX

I2P PEX está basado en ut_pex. Como no parece haber una especificación formal de ut_pex disponible, puede ser necesario revisar el código fuente de libtorrent para obtener ayuda. Es un mensaje de extensión, identificado como "i2p_pex" en [el handshake de extensión](http://www.bittorrent.org/beps/bep_0010.html). Contiene un diccionario bencoded con hasta 3 claves: "added", "added.f" y "dropped". Los valores added y dropped son cada uno una cadena de un solo byte, cuya longitud es un múltiplo de 32 bytes. Estas cadenas de bytes son los hashes SHA-256 concatenados de los [Destinations](/docs/specs/common-structures/#struct_Destination) binarios de los peers. Este es el mismo formato que el valor del diccionario de peers en el formato de respuesta compacta i2p especificado anteriormente. El valor added.f, si está presente, es el mismo que en ut_pex.

---

## DHT

El soporte para DHT está incluido en el cliente i2psnark desde la versión 0.9.2. Las diferencias preliminares respecto a [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) se describen a continuación y están sujetas a cambios. Contacta con los desarrolladores de I2P si deseas desarrollar un cliente que soporte DHT.

A diferencia del DHT estándar, I2P DHT no utiliza un bit en el handshake de opciones, o el mensaje PORT. Se anuncia con un mensaje de extensión, identificado como "i2p_dht" en [el handshake de extensión](http://www.bittorrent.org/beps/bep_0010.html). Contiene un diccionario bencoded con dos claves, "port" y "rport", ambos enteros.

El puerto UDP (datagrama) listado en la información compacta del nodo se usa para recibir datagramas con respuesta posible (firmados). Esto se usa para consultas, excepto para anuncios. Llamamos a esto el "puerto de consulta". Este es el valor "port" del mensaje de extensión. Las consultas usan el número de protocolo [I2CP](/docs/specs/i2cp/) 17.

Además de ese puerto UDP, usamos un segundo puerto de datagramas igual al puerto de consulta + 1. Este se usa para recibir datagramas sin firmar (en bruto) para respuestas, errores y anuncios. Este puerto proporciona mayor eficiencia ya que las respuestas contienen tokens enviados en la consulta, y no necesitan ser firmadas. Llamamos a este el "puerto de respuesta". Este es el valor "rport" del mensaje de extensión. Debe ser 1 + el puerto de consulta. Las respuestas y anuncios usan el protocolo [I2CP](/docs/specs/i2cp/) número 18.

La información compacta de peer es de 32 bytes (Hash SHA256 de 32 bytes) en lugar de IP de 4 bytes + puerto de 2 bytes. No hay puerto de peer. En una respuesta, la clave "values" es una lista de cadenas, cada una conteniendo una sola información compacta de peer.

La información compacta del nodo es de 54 bytes (20 bytes de Node ID + 32 bytes de hash SHA256 + 2 bytes de puerto) en lugar de 20 bytes de Node ID + 4 bytes de IP + 2 bytes de puerto. En una respuesta, la clave "nodes" es una cadena de bytes única con información compacta de nodos concatenada.

Requisito de ID de nodo seguro: Para hacer más difíciles varios ataques DHT, los primeros 4 bytes del ID del Nodo deben coincidir con los primeros 4 bytes del Hash de destino, y los siguientes dos bytes del ID del Nodo deben coincidir con los siguientes dos bytes del hash de destino en OR exclusivo con el puerto.

En un archivo torrent, la clave "nodes" del diccionario de torrent sin tracker está por definir. Podría ser una lista de cadenas binarias de 32 bytes (hashes SHA256) en lugar de una lista de listas que contengan una cadena de host y un entero de puerto. Alternativas: Una sola cadena de bytes con hashes concatenados, o una lista de cadenas únicamente.

---

## Rastreadores de Datagramas (UDP)

La especificación para anuncios UDP en I2P se finalizó en 2025-06. El soporte en varios clientes I2P y trackers se implementará gradualmente durante 2025. Las diferencias con [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) están documentadas en [la especificación de anuncios UDP](/docs/specs/udp-announces/). La especificación también requiere soporte para [los nuevos formatos Datagram 2/3](/docs/specs/datagrams/).

---

## Información Adicional

Una especificación preliminar para calcular el conjunto rápido permitido se encuentra en [Propuesta 172](/proposals/172-bep6-allowed-fast)

---

## Información adicional

- Los estándares de bittorrent de I2P generalmente se discuten en [zzz.i2p](http://zzz.i2p/).
- Un gráfico de las capacidades actuales del software de tracker está [también disponible allí](http://zzz.i2p/files/trackers.html).
- Las [FAQ de bittorrent de I2P](http://forum.i2p/viewtopic.php?t=2068)
- [Discusión sobre DHT en I2P](http://zzz.i2p/topics/812)
