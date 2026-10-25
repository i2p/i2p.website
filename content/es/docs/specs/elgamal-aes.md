---
title: "Cifrado ElGamal/AES + SessionTag"
description: "Cifrado de extremo a extremo heredado que combina ElGamal, AES, SHA-256 y etiquetas de sesión de un solo uso"
slug: "elgamal-aes"
aliases:
  - "/es/how_elgamalaes"
  - "/es/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Descripción general

ElGamal/AES+SessionTags se utiliza para el cifrado de extremo a extremo.

Como un sistema no confiable, desordenado y basado en mensajes, I2P utiliza una combinación simple de algoritmos de cifrado asimétrico y simétrico para proporcionar confidencialidad e integridad de datos a los garlic messages. En conjunto, la combinación se denomina ElGamal/AES+SessionTags, pero esa es una forma excesivamente verbosa de describir el uso de ElGamal de 2048 bits, AES256, SHA256 y nonces de 32 bytes.

La primera vez que un router quiere cifrar un mensaje garlic a otro router, cifran el material de claves para una clave de sesión AES256 con ElGamal y añaden la carga útil cifrada AES256/CBC después de ese bloque ElGamal cifrado. Además de la carga útil cifrada, la sección cifrada AES contiene la longitud de la carga útil, el hash SHA256 de la carga útil no cifrada, así como un número de "etiquetas de sesión" - nonces aleatorios de 32 bytes. La próxima vez que el remitente quiera cifrar un mensaje garlic a otro router, en lugar de cifrar con ElGamal una nueva clave de sesión, simplemente eligen una de las etiquetas de sesión previamente entregadas y cifran la carga útil con AES como antes, usando la clave de sesión utilizada con esa etiqueta de sesión, antepuesta con la etiqueta de sesión misma. Cuando un router recibe un mensaje cifrado garlic, verifican los primeros 32 bytes para ver si coincide con una etiqueta de sesión disponible - si coincide, simplemente descifran el mensaje con AES, pero si no, descifran el primer bloque con ElGamal.

Cada etiqueta de sesión puede usarse solo una vez para prevenir que adversarios internos correlacionen innecesariamente diferentes mensajes como si fueran entre los mismos routers. El remitente de un mensaje cifrado ElGamal/AES+SessionTag elige cuándo y cuántas etiquetas entregar, abasteciendo al destinatario con suficientes etiquetas para cubrir una ráfaga de mensajes. Los mensajes garlic pueden detectar la entrega exitosa de etiquetas empaquetando un pequeño mensaje adicional como un clove (un "mensaje de estado de entrega") - cuando el mensaje garlic llega al destinatario previsto y se descifra exitosamente, este pequeño mensaje de estado de entrega es uno de los cloves expuestos y tiene instrucciones para que el destinatario envíe el clove de vuelta al remitente original (a través de un tunnel de entrada, por supuesto). Cuando el remitente original recibe este mensaje de estado de entrega, sabe que las etiquetas de sesión empaquetadas en el mensaje garlic fueron entregadas exitosamente.

Las etiquetas de sesión tienen una vida útil corta, después de la cual se descartan si no se usan. Además, la cantidad almacenada para cada clave está limitada, al igual que el número de claves mismas - si llegan demasiadas, pueden descartarse mensajes nuevos o antiguos. El remitente hace seguimiento de si los mensajes que usan etiquetas de sesión están llegando, y si no hay comunicación suficiente puede descartar los que previamente se asumían como entregados correctamente, volviendo al cifrado ElGamal completo y costoso. Una sesión continuará existiendo hasta que todas sus etiquetas se agoten o expiren.

Las sesiones son unidireccionales. Las etiquetas se entregan de Alice a Bob, y Alice luego usa las etiquetas, una por una, en mensajes posteriores a Bob.

Las sesiones pueden establecerse entre Destinations, entre routers, o entre un router y un Destination. Cada router y Destination mantiene su propio Gestor de Claves de Sesión para realizar un seguimiento de las Claves de Sesión y las Etiquetas de Sesión. Los Gestores de Claves de Sesión separados evitan que los adversarios correlacionen múltiples Destinations entre sí o con un router.

## Recepción de Mensajes

Cada mensaje recibido tiene una de dos condiciones posibles:

1. Es parte de una sesión existente y contiene una Session Tag y un bloque cifrado AES
2. Es para una nueva sesión y contiene tanto bloques cifrados ElGamal como AES

Cuando un router recibe un mensaje, primero asumirá que proviene de una sesión existente e intentará buscar el Session Tag y descifrar los datos siguientes usando AES. Si eso falla, asumirá que es para una nueva sesión e intentará descifrarlo usando ElGamal.

## Especificación del Mensaje de Nueva Sesión {#new}

Un mensaje ElGamal de Nueva Sesión contiene dos partes, un bloque ElGamal cifrado y un bloque AES cifrado.

El mensaje cifrado contiene:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### Bloque ElGamal

El Bloque ElGamal cifrado siempre tiene 514 bytes de longitud.

Los datos ElGamal sin cifrar tienen una longitud de 222 bytes y contienen:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
La [Session Key](/docs/specs/common-structures#type_SessionKey) de 32 bytes es el identificador de la sesión. El Pre-IV de 32 bytes se utilizará para generar el IV para el bloque AES que sigue; el IV son los primeros 16 bytes del Hash SHA-256 del Pre-IV.

La carga útil de 222 bytes está cifrada [usando ElGamal](/docs/specs/cryptography#elgamal) y el bloque cifrado tiene 514 bytes de longitud.

### Bloque AES {#aes}

Los datos no cifrados en el bloque AES contienen lo siguiente:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Definición

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Longitud mínima: 48 bytes

Los datos son entonces [Cifrados con AES](/docs/specs/cryptography), usando la clave de sesión y el IV (calculado desde el pre-IV) de la sección ElGamal. La longitud del Bloque AES cifrado es variable pero siempre es un múltiplo de 16 bytes.

#### Notas

- La longitud máxima real de la carga útil, y la longitud máxima del bloque, es menor a 64 KB; consulta la [Descripción general de I2NP](/docs/protocol/i2np).
- New Session Key actualmente no se usa y nunca está presente.

## Especificación de Mensaje de Sesión Existente {#existing}

Los session tags entregados exitosamente se recuerdan durante un período breve (actualmente 15 minutos) hasta que se usan o se descartan. Un tag se usa empaquetándolo en un Existing Session Message que contiene solo un bloque cifrado AES, y no está precedido por un bloque ElGamal.

El mensaje de sesión existente es el siguiente:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Definición

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
El session tag también sirve como pre-IV. El IV son los primeros 16 bytes del Hash SHA-256 del sessionTag.

Para decodificar un mensaje de una sesión existente, un router busca la Session Tag para encontrar una Session Key asociada. Si se encuentra la Session Tag, el bloque AES se descifra usando la Session Key asociada. Si no se encuentra la tag, se asume que el mensaje es un [New Session Message](#new).

## Opciones de Configuración de Etiquetas de Sesión {#config}

A partir de la versión 0.9.2, el cliente puede configurar el número predeterminado de Session Tags para enviar y el umbral bajo de tags para la sesión actual. Para conexiones de streaming breves o datagramas, estas opciones pueden utilizarse para reducir significativamente el ancho de banda. Consulta la [especificación de opciones I2CP](/docs/protocol/i2cp#options) para más detalles. La configuración de sesión también puede ser anulada por mensaje individual. Consulta la [especificación I2CP Send Message Expires](/docs/specs/i2cp#msg_SendMessageExpires) para más detalles.

## Trabajo Futuro {#future}

**Nota:** ElGamal/AES+SessionTags está siendo reemplazado por ECIES-X25519-AEAD-Ratchet (Propuesta 144). Los problemas e ideas referenciados a continuación han sido incorporados en el diseño del nuevo protocolo. Los siguientes elementos no serán abordados en ElGamal/AES+SessionTags.

Hay muchas áreas posibles para ajustar los algoritmos del Gestor de Claves de Sesión; algunas pueden interactuar con el comportamiento de la biblioteca de streaming, o tener un impacto significativo en el rendimiento general.

- El número de etiquetas entregadas podría depender del tamaño del mensaje, teniendo en cuenta
  el relleno eventual a 1KB en la capa de mensaje del tunnel.

- Los clientes podrían enviar una estimación de la duración de la sesión al router, como una recomendación sobre el número de tags requeridos.

- La entrega de muy pocas etiquetas hace que el router recurra a un cifrado ElGamal costoso.

- El router puede asumir la entrega de Session Tags, o esperar confirmación antes de usarlos;
  hay compromisos para cada estrategia.

- Para mensajes muy breves, casi la totalidad de los 222 bytes de los campos pre-IV y padding en el bloque ElGamal
  podrían utilizarse para todo el mensaje, en lugar de establecer una sesión.

- Evaluar la estrategia de padding; actualmente añadimos padding hasta un mínimo de 128 bytes.
  Sería mejor agregar algunas etiquetas a los mensajes pequeños que añadir padding.

- Quizás las cosas podrían ser más eficientes si el sistema de Session Tag fuera bidireccional,
  para que las etiquetas entregadas en el camino 'directo' pudieran usarse en el camino 'inverso',
  evitando así ElGamal en la respuesta inicial.
  El router actualmente utiliza algunos trucos como este cuando envía
  mensajes de prueba de túnel a sí mismo.

- Cambio de Session Tags a
  [un PRNG sincronizado](/docs/overview/performance#future#prng).

- Varias de estas ideas pueden requerir un nuevo tipo de mensaje I2NP, o
  establecer una bandera en las
  [Instrucciones de Entrega](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  o establecer un número mágico en los primeros bytes del campo Session Key
  y aceptar un pequeño riesgo de que la Session Key aleatoria coincida con el número mágico.
