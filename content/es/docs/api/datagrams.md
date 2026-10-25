---
title: "Datagramas"
description: "Formatos de mensajes autenticados, contestables y sin procesar por encima de I2CP"
slug: "datagrams"
aliases:
  - "/es/datagrams"
  - "/es/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Descripción General de Datagramas {#overview}

Los datagramas se construyen sobre la base [I2CP](/docs/specs/i2cp) para proporcionar mensajes autenticados y con capacidad de respuesta en un formato estándar. Esto permite que las aplicaciones lean de manera confiable la dirección "de origen" de un datagrama y sepan que la dirección realmente envió el mensaje. Esto es necesario para algunas aplicaciones ya que el mensaje base de I2P es completamente crudo - no tiene dirección "de origen" (a diferencia de los paquetes IP). Además, el mensaje y el remitente son autenticados mediante la firma de la carga útil.

Los datagramas, al igual que [los paquetes de la biblioteca de streaming](/docs/api/streaming), son una construcción a nivel de aplicación. Estos protocolos son independientes de los [transportes](/docs/overview/transport) de bajo nivel; los protocolos son convertidos a mensajes I2NP por el router, y cualquiera de los protocolos puede ser transportado por cualquiera de los transportes.

## Guía de Aplicaciones {#application}

Las aplicaciones escritas en Java pueden usar la API de datagramas, mientras que las aplicaciones en otros lenguajes pueden usar el soporte de datagramas de [SAM](/docs/api/samv3). También hay soporte limitado en i2ptunnel en el [proxy SOCKS](/docs/api/socks), los tipos de túnel 'streamr', y las clases udpTunnel.

### Longitud del Datagrama {#length}

El diseñador de la aplicación debe considerar cuidadosamente el equilibrio entre datagramas con respuesta vs. sin respuesta. Además, el tamaño del datagrama afectará la confiabilidad, debido a la fragmentación del tunnel en mensajes de tunnel de 1KB. Cuantos más fragmentos de mensaje haya, más probable será que uno de ellos sea descartado por un salto intermedio. No se recomiendan mensajes de más de unos pocos KB. Por encima de aproximadamente 10 KB, la probabilidad de entrega disminuye drásticamente.

[Ver la página de Especificación de Datagramas.](/docs/specs/datagrams)

También ten en cuenta que las diversas sobrecargas agregadas por las capas inferiores, en particular los garlic messages, representan una gran carga para los mensajes intermitentes como los utilizados por una aplicación Kademlia-over-UDP. Las implementaciones están actualmente ajustadas para tráfico frecuente utilizando la biblioteca de streaming.

### Número de protocolo y puertos I2CP {#protocol}

El número de protocolo I2CP estándar para datagramas firmados (con respuesta posible) es PROTO_DATAGRAM (17). Las aplicaciones pueden o no elegir establecer el protocolo en el encabezado I2CP. El valor predeterminado depende de la implementación. Debe establecerse para demultiplexar el tráfico de datagramas y streaming recibido en el mismo Destination.

Como los datagramas no están orientados a conexión, la aplicación puede requerir números de puerto para correlacionar datagramas con peers particulares o sesiones de comunicación, como es tradicional con UDP sobre IP. Las aplicaciones pueden agregar puertos 'from' y 'to' al encabezado I2CP (gzip) como se describe en la [página I2CP](/docs/specs/i2cp#format).

No hay ningún método dentro de la API de datagram para especificar si es no-respondible (raw) o respondible. La aplicación debe estar diseñada para esperar el tipo apropiado. El número de protocolo I2CP o puerto debe ser usado por la aplicación para indicar el tipo de datagram. Los números de protocolo I2CP PROTO_DATAGRAM (firmado, también conocido como Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, y PROTO_DATAGRAM3 están definidos en la API I2PSession para este propósito. Un patrón de diseño común en aplicaciones de datagram cliente/servidor es usar datagramas firmados para una solicitud que incluye un nonce, y usar un datagrama raw para la respuesta, devolviendo el nonce de la solicitud.

**Valores por defecto:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Integridad de Datos {#integrity}

La integridad de los datos está garantizada por la suma de verificación gzip CRC-32 implementada en [la capa I2CP](/docs/specs/i2cp#format). Los datagramas autenticados (Datagram1 y Datagram2) también aseguran la integridad. No hay campo de suma de verificación en el protocolo de datagramas.

### Encapsulación de Paquetes {#encapsulation}

Cada datagrama se envía a través de I2P como un único mensaje (o como un clove individual en un [Garlic Message](/docs/overview/garlic-routing)). La encapsulación de mensajes se implementa en las capas subyacentes de [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np) y [tunnel message](/docs/specs/tunnel-message). No hay un mecanismo delimitador de paquetes ni un campo de longitud en el protocolo de datagramas.

## Especificación {#spec}

[Ver la página de Especificación de Datagramas.](/docs/specs/datagrams)
