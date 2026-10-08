---
title: "Enrutamiento de Tunnel"
description: "Visión general de la terminología, construcción y operación de tunnels I2P"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Descripción general

Esta página contiene una descripción general de la terminología y operación de los tunnels de I2P, con enlaces a páginas más técnicas, detalles y especificaciones.

Como se explica brevemente en la [introducción](/docs/overview/intro/), I2P construye "tunnels" virtuales - rutas temporales y unidireccionales a través de una secuencia de routers. Estos tunnels se clasifican como tunnels entrantes (donde todo lo que se les da va hacia el creador del tunnel) o tunnels salientes (donde el creador del tunnel empuja los mensajes lejos de él). Cuando Alice quiere enviar un mensaje a Bob, ella (típicamente) lo enviará a través de uno de sus tunnels salientes existentes con instrucciones para que el endpoint de ese tunnel lo reenvíe al router de enlace para uno de los tunnels entrantes actuales de Bob, que a su vez se lo pasa a Bob.

![Alice conectándose a través de su tunnel saliente a Bob vía su tunnel entrante](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Vocabulario de Tunnel

- **Tunnel gateway** - el primer router en un tunnel. Para tunnels entrantes, este es el mencionado en el LeaseSet publicado en la [base de datos de red](/docs/overview/network-database/). Para tunnels salientes, el gateway es el router de origen. (ej. tanto A como D arriba)

- **Tunnel endpoint** - el último router en un tunnel. (ej. tanto C como F arriba)

- **Participante del tunnel** - todos los routers en un tunnel excepto el gateway o endpoint (por ejemplo, tanto B como E anteriormente)

- **tunnel de n-saltos** - un tunnel con un número específico de saltos entre routers, por ejemplo:
  - **tunnel de 0-saltos** - un tunnel donde la puerta de enlace también es el punto final
  - **tunnel de 1-salto** - un tunnel donde la puerta de enlace habla directamente con el punto final
  - **tunnel de 2-(o más)-saltos** - un tunnel donde hay al menos un participante intermedio del tunnel. (el diagrama anterior incluye dos tunnels de 2-saltos - uno saliente desde Alice, uno entrante hacia Bob)

- **Tunnel ID** - Un [entero de 4 bytes](/docs/specs/common-structures/#type_TunnelId) diferente para cada salto en un tunnel, y único entre todos los tunnels en un router. Elegido aleatoriamente por el creador del tunnel.

---

## Información de Construcción de Tunnel

Los routers que desempeñan los tres roles (gateway, participant, endpoint) reciben diferentes datos en el [Mensaje de Construcción de Túnel](/docs/specs/tunnel-creation/) inicial para realizar sus tareas:

**El gateway del tunnel recibe:**

- **clave de cifrado del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar mensajes e instrucciones al siguiente salto
- **clave IV del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar doblemente el IV al siguiente salto
- **clave de respuesta** - una [clave pública AES](/docs/specs/common-structures/#type_SessionKey) para cifrar la respuesta a la solicitud de construcción del tunnel
- **IV de respuesta** - el IV para cifrar la respuesta a la solicitud de construcción del tunnel
- **ID del tunnel** - entero de 4 bytes (solo gateways de entrada)
- **siguiente salto** - qué router es el siguiente en la ruta (a menos que este sea un tunnel de 0 saltos, y el gateway también sea el endpoint)
- **ID del siguiente tunnel** - El ID del tunnel en el siguiente salto

**Todos los participantes intermedios del tunnel obtienen:**

- **clave de cifrado del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar mensajes e instrucciones al siguiente salto
- **clave IV del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar doblemente el IV al siguiente salto
- **clave de respuesta** - una [clave pública AES](/docs/specs/common-structures/#type_SessionKey) para cifrar la respuesta a la solicitud de construcción del tunnel
- **IV de respuesta** - el IV para cifrar la respuesta a la solicitud de construcción del tunnel
- **ID del tunnel** - entero de 4 bytes
- **siguiente salto** - qué router es el siguiente en la ruta
- **ID del siguiente tunnel** - El ID del tunnel en el siguiente salto

**El endpoint del tunnel obtiene:**

- **clave de cifrado del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar mensajes e instrucciones al endpoint (a sí mismo)
- **clave IV del tunnel** - una [clave privada AES](/docs/specs/common-structures/#type_SessionKey) para cifrar doblemente el IV al endpoint (a sí mismo)
- **clave de respuesta** - una [clave pública AES](/docs/specs/common-structures/#type_SessionKey) para cifrar la respuesta a la solicitud de construcción del tunnel (solo endpoints de salida)
- **IV de respuesta** - el IV para cifrar la respuesta a la solicitud de construcción del tunnel (solo endpoints de salida)
- **ID del tunnel** - entero de 4 bytes (solo endpoints de salida)
- **router de respuesta** - la puerta de entrada entrante del tunnel a través del cual enviar la respuesta (solo endpoints de salida)
- **ID del tunnel de respuesta** - El ID del tunnel del router de respuesta (solo endpoints de salida)

Los detalles están en la [especificación de creación de tunnel](/docs/specs/tunnel-creation/).

---

## Agrupación de Túneles

Varios tunnels para un propósito particular pueden agruparse en un "pool de tunnels", como se describe en la [especificación de tunnels](/docs/specs/tunnel-implementation/#tunnel.pooling). Esto proporciona redundancia y ancho de banda adicional. Los pools utilizados por el router mismo se llaman "tunnels exploratorios". Los pools utilizados por las aplicaciones se llaman "tunnels de cliente".

---

## Longitud del Tunnel

Como se mencionó anteriormente, cada cliente solicita que su router proporcione tunnels que incluyan al menos un cierto número de saltos. La decisión sobre cuántos routers tener en los tunnels de salida y entrada tiene un efecto importante en la latencia, rendimiento, confiabilidad y anonimato proporcionado por I2P: cuantos más peers tengan que atravesar los mensajes, más tiempo tarda en llegar y más probable es que uno de esos routers falle prematuramente. Cuantos menos routers haya en un tunnel, más fácil es para un adversario realizar ataques de análisis de tráfico y comprometer el anonimato de alguien. Las longitudes de tunnel son especificadas por los clientes a través de [opciones I2CP](/docs/specs/i2cp/#options). El número máximo de saltos en un tunnel es 7.

### tunnels de 0 saltos

Sin routers remotos en un túnel, el usuario tiene una negación plausible muy básica (ya que nadie sabe con certeza que el peer que les envió el mensaje no lo estaba simplemente reenviando como parte del túnel). Sin embargo, sería bastante fácil montar un ataque de análisis estadístico y notar que los mensajes dirigidos a un destino específico siempre se envían a través de un único gateway. Los análisis estadísticos contra túneles salientes de 0 saltos son más complejos, pero podrían mostrar información similar (aunque serían ligeramente más difíciles de montar).

### tunnels de 1 salto

Con solo un router remoto en un tunnel, el usuario tiene tanto negación plausible como anonimato básico, siempre que no se enfrenten a un adversario interno (como se describe en el [modelo de amenazas](/docs/overview/threat-model/)). Sin embargo, si el adversario ejecutara un número suficiente de routers de tal manera que el único router remoto en el tunnel sea a menudo uno de esos comprometidos, podrían montar el ataque de análisis estadístico de tráfico mencionado anteriormente.

### tunnels de 2 saltos

Con dos o más routers remotos en un túnel, los costos de montar el ataque de análisis de tráfico aumentan, ya que muchos routers remotos tendrían que ser comprometidos para llevarlo a cabo.

### tunnels de 3 saltos (o más)

Para reducir la susceptibilidad a [algunos ataques](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), se recomiendan 3 o más saltos para el nivel más alto de protección. [Estudios recientes](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) también concluyen que más de 3 saltos no proporciona una protección adicional.

### Longitudes predeterminadas de tunnel

El router utiliza túneles de 2 saltos por defecto para sus túneles exploratorios. Los valores predeterminados de los túneles de cliente son establecidos por la aplicación, usando [opciones I2CP](/docs/specs/i2cp/#options). La mayoría de las aplicaciones usan 2 o 3 saltos como su configuración predeterminada.

---

## Pruebas de Tunnel

Todos los tunnels son probados periódicamente por su creador enviando un DeliveryStatusMessage a través de un tunnel saliente y dirigido a otro tunnel entrante (probando ambos tunnels a la vez). Si alguno de ellos falla un número consecutivo de pruebas, se marca como no funcional. Si se usaba para el tunnel entrante de un cliente, se crea un nuevo leaseSet. Las fallas en las pruebas de tunnel también se reflejan en la [calificación de capacidad en el perfil del par](/docs/overview/peer-selection/#capacity).

---

La creación de túneles es manejada por [garlic routing](/docs/overview/garlic-routing/) un Tunnel Build Message a un router, solicitando que participe en el túnel (proporcionándole toda la información apropiada, como se mencionó anteriormente, junto con un certificado, que actualmente es un certificado 'nulo', pero admitirá hashcash u otros certificados no gratuitos cuando sea necesario). Ese router reenvía el mensaje al siguiente salto en el túnel. Los detalles están en la [especificación de creación de túneles](/docs/specs/tunnel-creation/).

## Creación de Tunnel

---

El cifrado de múltiples capas se maneja mediante [garlic encryption](/docs/overview/garlic-routing/) de mensajes de túnel. Los detalles están en la [especificación de túnel](/docs/specs/tunnel-implementation/). El IV de cada salto se cifra con una clave separada como se explica allí.

## Cifrado de Tunnel

---

---

## Trabajo Futuro

- Se podrían usar otras técnicas de prueba de tunnel, como envolver con garlic encryption una serie de pruebas en cloves, probar participantes individuales del tunnel por separado, etc.

- Cambiar a valores predeterminados de túneles exploratorios de 3 saltos.

- En una versión futura distante, pueden implementarse opciones que especifiquen la configuración de pooling, mixing y generación de chaff.

- En una versión futura distante, pueden implementarse límites en la cantidad y tamaño de mensajes permitidos durante la vida útil del tunnel (por ejemplo, no más de 300 mensajes o 1MB por minuto).

---

## Ver También

- [Especificación de tunnel](/docs/specs/tunnel-implementation/)
- [Especificación de creación de tunnel](/docs/specs/tunnel-creation/)
- [Tunnels unidireccionales](/docs/legacy/unidirectional/)
- [Especificación de mensajes de tunnel](/docs/specs/tunnel-message/)
- [Enrutamiento garlic](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [Opciones I2CP](/docs/specs/i2cp/#options)
