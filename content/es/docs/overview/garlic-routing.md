---
title: "Garlic Routing"
description: "Entendiendo la terminología, arquitectura e implementación del garlic routing en I2P"
slug: "garlic-routing"
aliases:
  - "/es/how_garlicrouting"
  - "/es/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Enrutamiento Garlic y Terminología "Garlic"

Los términos "garlic routing" y "garlic encryption" a menudo se usan de manera bastante imprecisa cuando se refiere a la tecnología de I2P. Aquí explicamos la historia de los términos, los diversos significados y el uso de los métodos "garlic" en I2P.

"Garlic routing" fue acuñado por primera vez por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) en la [tesis de maestría](https://www.freehaven.net/papers.html) de Roger Dingledine sobre Free Haven, Sección 8.1.1 (junio de 2000), como derivado del [Onion Routing](https://www.onion-router.net/).

"Garlic" puede haber sido utilizado originalmente por los desarrolladores de I2P porque I2P implementa una forma de agrupamiento como describe Freedman, o simplemente para enfatizar las diferencias generales con Tor. El razonamiento específico puede haberse perdido en la historia. En general, cuando se hace referencia a I2P, el término "garlic" puede significar una de tres cosas:

1. Cifrado por capas
2. Agrupación de múltiples mensajes juntos
3. Cifrado ElGamal/AES

Desafortunadamente, el uso de la terminología "garlic" por parte de I2P a lo largo de los años no siempre ha sido preciso; por lo tanto, se advierte al lector cuando encuentre este término. Con suerte, la explicación a continuación aclarará las cosas.

### Cifrado por Capas

El enrutamiento cebolla es una técnica para construir rutas, o túneles, a través de una serie de pares, y luego usar ese túnel. Los mensajes son cifrados repetidamente por el originador, y luego descifrados por cada salto. Durante la fase de construcción, solo las instrucciones de enrutamiento para el siguiente salto se exponen a cada par. Durante la fase de operación, los mensajes se pasan a través del túnel, y el mensaje y sus instrucciones de enrutamiento solo se exponen al punto final del túnel.

Esto es similar a la forma en que Mixmaster (ver [comparaciones de redes](/docs/overview/comparison/)) envía mensajes - tomando un mensaje, cifrándolo con la clave pública del destinatario, tomando ese mensaje cifrado y cifrándolo (junto con las instrucciones que especifican el siguiente salto), y luego tomando ese mensaje cifrado resultante y así sucesivamente, hasta que tenga una capa de cifrado por salto a lo largo de la ruta.

En este sentido, el "garlic routing" como concepto general es idéntico al "onion routing". Tal como se implementa en I2P, por supuesto, hay varias diferencias de la implementación en Tor; ver más abajo. Aun así, hay similitudes sustanciales de tal manera que I2P se beneficia de una [gran cantidad de investigación académica sobre onion routing](https://www.onion-router.net/Publications.html), [Tor, y mixnets similares](https://freehaven.net/anonbib/topic.html).

### Agrupando Múltiples Mensajes

Michael Freedman definió el "garlic routing" como una extensión del onion routing, en la que múltiples mensajes se agrupan juntos. Llamó a cada mensaje un "bulbo". Todos los mensajes, cada uno con sus propias instrucciones de entrega, se exponen en el punto final. Esto permite el agrupamiento eficiente de un "bloque de respuesta" de onion routing con el mensaje original.

Este concepto está implementado en I2P, como se describe a continuación. Nuestro término para los "bulbos" de garlic encryption es "cloves" (dientes). Cualquier número de mensajes puede estar contenido, en lugar de solo un mensaje único. Esta es una distinción significativa del onion routing implementado en Tor. Sin embargo, es solo una de muchas diferencias arquitectónicas importantes entre I2P y Tor; quizás no sea, por sí sola, suficiente para justificar un cambio en la terminología.

Otra diferencia del método descrito por Freedman es que la ruta es unidireccional - no hay "punto de retorno" como se ve en el enrutamiento cebolla o los bloques de respuesta mixmaster, lo cual simplifica enormemente el algoritmo y permite una entrega más flexible y confiable.

### Cifrado ElGamal/AES

En algunos casos, "garlic encryption" puede simplemente significar cifrado [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) (sin múltiples capas).

---

## Métodos "Garlic" en I2P

Ahora que hemos definido varios términos relacionados con "garlic", podemos decir que I2P utiliza garlic routing, agrupamiento y cifrado en tres lugares:

1. Para construir y enrutar a través de tunnels (cifrado por capas)
2. Para determinar el éxito o fallo de la entrega de mensajes extremo a extremo (agrupación)
3. Para publicar algunas entradas de la base de datos de red (reduciendo la probabilidad de un ataque exitoso de análisis de tráfico) (ElGamal/AES)

También existen maneras significativas en las que esta técnica puede utilizarse para mejorar el rendimiento de la red, aprovechando las compensaciones entre latencia y rendimiento del transporte, y ramificando los datos a través de rutas redundantes para aumentar la confiabilidad.

### Construcción y Enrutamiento de Tunnels

En I2P, los tunnels son unidireccionales. Cada parte construye dos tunnels, uno para el tráfico de salida y otro para el tráfico de entrada. Por lo tanto, se requieren cuatro tunnels para un solo mensaje de ida y vuelta y su respuesta.

Los tunnels se construyen, y luego se utilizan, con cifrado por capas. Esto se describe en la [página de implementación de tunnel](/docs/specs/tunnel-implementation/). Utilizamos [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) para el cifrado.

Los tunnels son un mecanismo de propósito general para transportar todos los [mensajes I2NP](/docs/specs/i2np/), y los Garlic Messages no se utilizan para construir tunnels. No agrupamos múltiples mensajes I2NP en un solo Garlic Message para desempaquetarlos en el extremo del tunnel de salida; el cifrado del tunnel es suficiente.

### Agrupación de Mensajes de Extremo a Extremo

En la capa por encima de los tunnels, I2P entrega mensajes extremo a extremo entre [Destinations](/docs/specs/common-structures/). Al igual que dentro de un solo tunnel, utilizamos [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) para el cifrado. Cada mensaje de cliente entregado al router a través de la [interfaz I2CP](/docs/api/i2cp/) se convierte en un solo Garlic Clove con sus propias Instrucciones de Entrega, dentro de un Garlic Message. Las Instrucciones de Entrega pueden especificar un Destination, Router o Tunnel.

Generalmente, un Garlic Message contendrá solo un clove. Sin embargo, el router empaquetará periódicamente dos cloves adicionales en el Garlic Message:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Un Mensaje de Estado de Entrega**, con Instrucciones de Entrega especificando que debe ser enviado de vuelta al router de origen como un acuse de recibo. Esto es similar al "bloque de respuesta" o "cebolla de respuesta" descrito en las referencias. Se utiliza para determinar el éxito o fallo de la entrega de mensajes de extremo a extremo. El router de origen puede, ante la falla de recibir el Mensaje de Estado de Entrega dentro del período de tiempo esperado, modificar el enrutamiento hacia el Destination del extremo lejano, o tomar otras acciones.

2. **Un Mensaje Database Store**, que contiene un LeaseSet para el Destino de origen, con Instrucciones de Entrega especificando el router del destino final. Al incluir periódicamente un LeaseSet, el router asegura que el extremo remoto será capaz de mantener las comunicaciones. De lo contrario, el extremo remoto tendría que consultar a un router floodfill por la entrada de la base de datos de red, y todos los LeaseSets tendrían que ser publicados en la base de datos de red, como se explica en la [página de base de datos de red](/docs/specs/common-structures/).

Por defecto, los mensajes de Estado de Entrega y Almacén de Base de Datos se agrupan cuando el LeaseSet local cambia, cuando se entregan Session Tags adicionales, o si los mensajes no han sido agrupados en el minuto anterior.

Obviamente, los mensajes adicionales están actualmente agrupados para propósitos específicos, y no forman parte de un esquema de enrutamiento de propósito general.

A partir de la versión 0.9.12, el Mensaje de Estado de Entrega es envuelto en otro Mensaje Garlic por el originador para que el contenido esté cifrado y no sea visible para los routers en la ruta de retorno.

### Almacenamiento en la Base de Datos de Red Floodfill

Como se explica en la [página de base de datos de red](/docs/specs/common-structures/), los LeaseSets locales se envían a los routers floodfill en un Mensaje de Almacén de Base de Datos envuelto en un Mensaje Garlic para que no sea visible al gateway de salida del túnel.

---

## Trabajo Futuro

El mecanismo de Garlic Message es muy flexible y proporciona una estructura para implementar muchos tipos de métodos de entrega de mixnet. Junto con la opción de retraso no utilizada en las Instrucciones de Entrega del mensaje de túnel, es posible un amplio espectro de estrategias de agrupación por lotes, retraso, mezcla y enrutamiento.

En particular, existe potencial para mucha más flexibilidad en el punto final del tunnel de salida. Los mensajes podrían posiblemente ser enrutados desde allí hacia uno de varios tunnels (minimizando así las conexiones punto a punto), o multidifundidos a varios tunnels para redundancia, o streaming de audio y video.

Dichos experimentos pueden entrar en conflicto con la necesidad de garantizar la seguridad y el anonimato, como limitar ciertas rutas de enrutamiento, restringir los tipos de mensajes I2NP que pueden reenviarse a lo largo de varias rutas y hacer cumplir ciertos tiempos de caducidad de mensajes.

Como parte del cifrado ElGamal/AES, un mensaje garlic contiene una cantidad de datos de relleno especificada por el remitente, lo que permite al remitente tomar contramedidas activas contra el análisis de tráfico. Esto no se utiliza actualmente, más allá del requisito de rellenar hasta un múltiplo de 16 bytes.

Cifrado de mensajes adicionales hacia y desde los [floodfill routers](/docs/specs/common-structures/).

---

## Referencias

- El término garlic routing fue acuñado por primera vez en la [tesis de maestría](https://www.freehaven.net/papers.html) de Free Haven de Roger Dingledine (junio de 2000), ver Sección 8.1.1 escrita por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/).
- [Publicaciones de Onion Router](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Proyecto Tor](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing fue descrito por primera vez en [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) por David M. Goldschlag, Michael G. Reed, y Paul F. Syverson en 1996.
