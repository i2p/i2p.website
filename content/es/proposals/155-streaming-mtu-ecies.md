---
title: "MTU de Transmisión para Destinos ECIES"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Nota
Despliegue y prueba de red en progreso.
Sujeto a revisiones menores.


## Visión General


### Resumen

ECIES reduce el sobrecargo del mensaje de sesión existente (ES) en unos 90 bytes.
Por lo tanto, podemos aumentar el MTU en unos 90 bytes para las conexiones ECIES.
Ver the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Sin aumentar el MTU, en muchos casos los ahorros de sobrecarga no son realmente "ahorros",
ya que los mensajes se rellenarán para usar de todos modos dos mensajes de túnel completos.

Esta propuesta no requiere ningún cambio en las especificaciones.
Se publica como una propuesta únicamente para facilitar la discusión y el consenso
del valor recomendado y de los detalles de implementación.


### Objetivos

- Aumentar el MTU negociado
- Maximizar el uso de mensajes de túnel de 1 KB
- No cambiar el protocolo de transmisión


## Diseño

Usar la opción existente MAX_PACKET_SIZE_INCLUDED y la negociación del MTU.
La transmisión continúa utilizando el mínimo del MTU enviado y recibido.
El valor por defecto sigue siendo 1730 para todas las conexiones, sin importar qué claves se usen.

Se alienta a las implementaciones a incluir la opción MAX_PACKET_SIZE_INCLUDED en todos los paquetes SYN, en ambas direcciones,
aunque esto no es un requisito.

Si un destino es únicamente ECIES, usar el valor más alto (ya sea como Alice o Bob).
Si un destino tiene clave dual, el comportamiento puede variar:

Si el cliente de clave dual está fuera del router (en una aplicación externa),
puede no "saber" la clave que se está usando en el otro extremo, y Alice puede solicitar
un valor más alto en el SYN, mientras el máximo de datos en el SYN sigue siendo 1730.

Si el cliente de clave dual está dentro del router, la información de qué clave
se está usando puede ser o no conocida por el cliente.
Es posible que el conjunto de arrendamiento aún no se haya obtenido, o que las interfaces de la API interna
no hagan fácilmente esa información disponible para el cliente.
Si la información está disponible, Alice puede usar el valor más alto;
de lo contrario, Alice debe usar el valor estándar de 1730 hasta que se negocie.

Un cliente de clave dual como Bob puede enviar el valor más alto en respuesta,
incluso si no se recibió ningún valor o un valor de 1730 de parte de Alice;
sin embargo, no hay ninguna disposición para negociar hacia arriba en la transmisión,
por lo que el MTU debe permanecer en 1730.


Como se señala en the [Streaming API documentation](/docs/api/streaming/),
los datos en los paquetes SYN enviados de Alice a Bob pueden exceder el MTU de Bob.
Esto es una debilidad en el protocolo de transmisión.
Por lo tanto, los clientes de clave dual deben limitar los datos en los paquetes SYN enviados
a 1730 bytes, mientras envían una opción de MTU más alta.
Una vez que se recibe el MTU más alto de Bob, Alice puede aumentar la carga útil máxima
real enviada.


### Análisis

Como se describe en the [ECIES specification](/docs/specs/ecies/#overhead), la sobrecarga de ElGamal para los mensajes de sesión existentes es
de 151 bytes, y la sobrecarga de Ratchet es de 69 bytes.
Por lo tanto, podemos aumentar el MTU para las conexiones ratchet en (151 - 69) = 82 bytes,
de 1730 a 1812.


## Especificación

Agregar los siguientes cambios y aclaraciones a la sección de Selección y Negociación de MTU de the [Streaming API documentation](/docs/api/streaming/).
No hay cambios en the [Streaming specification](/docs/specs/streaming/).


El valor por defecto de la opción i2p.streaming.maxMessageSize sigue siendo 1730 para todas las conexiones, sin importar qué claves se usen.
Los clientes deben usar el mínimo del MTU enviado y recibido, como de costumbre.

Hay cuatro constantes y variables MTU relacionadas:

- DEFAULT_MTU: 1730, sin cambios, para todas las conexiones
- i2cp.streaming.maxMessageSize: por defecto 1730 o 1812, puede ser cambiado por configuración
- ALICE_SYN_MAX_DATA: Los datos máximos que Alice puede incluir en un paquete SYN
- negotiated_mtu: El mínimo del MTU de Alice y Bob, a ser usado como el tamaño máximo de datos
  en el SYN ACK de Bob a Alice, y en todos los paquetes subsecuentes enviados en ambas direcciones


Hay cinco casos a considerar:


### 1) Alice solo ElGamal
Sin cambios, 1730 MTU en todos los paquetes.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize por defecto: 1730
- Alice puede enviar MAX_PACKET_SIZE_INCLUDED en SYN, no requerido a menos que != 1730


### 2) Alice solo ECIES
1812 MTU en todos los paquetes.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize por defecto: 1812
- Alice debe enviar MAX_PACKET_SIZE_INCLUDED en SYN


### 3) Alice Clave Dual y sabe que Bob es ElGamal
1730 MTU en todos los paquetes.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize por defecto: 1812
- Alice puede enviar MAX_PACKET_SIZE_INCLUDED en SYN, no requerido a menos que != 1730


### 4) Alice Clave Dual y sabe que Bob es ECIES
1812 MTU en todos los paquetes.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize por defecto: 1812
- Alice debe enviar MAX_PACKET_SIZE_INCLUDED en SYN


### 5) Alice Clave Dual y clave de Bob desconocida
Enviar 1812 como MAX_PACKET_SIZE_INCLUDED en paquete SYN pero limitar los datos del paquete SYN a 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize por defecto: 1812
- Alice debe enviar MAX_PACKET_SIZE_INCLUDED en SYN


### Para todos los casos

Alice y Bob calculan
negotiated_mtu, el mínimo del MTU de Alice y Bob, a ser usado como el tamaño máximo de datos
en el SYN ACK de Bob a Alice, y en todos los paquetes subsecuentes enviados en ambas direcciones.


## Justificación

Ver the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) para por qué el valor actual es 1730.
Ver the [ECIES specification](/docs/specs/ecies/#overhead) para por qué la sobrecarga de ECIES es 82 bytes menos que ElGamal.


## Notas de Implementación

Si la transmisión está creando mensajes de tamaño óptimo, es muy importante que
la capa ECIES-Ratchet no se rellene más allá de ese tamaño.

El tamaño óptimo del mensaje Garlic para caber en dos mensajes de túnel,
incluyendo la cabecera de 16 bytes del Mensaje Garlic I2NP, 4 bytes de Longitud del Mensaje Garlic,
8 bytes de etiqueta ES, y 16 bytes MAC, es 1956 bytes.

Un algoritmo de relleno recomendado en ECIES es el siguiente:

- Si la longitud total del Mensaje Garlic es de 1954-1956 bytes,
  no agregar un bloque de relleno (no hay espacio)
- Si la longitud total del Mensaje Garlic es de 1938-1953 bytes,
  agregar un bloque de relleno para alcanzar exactamente 1956 bytes.
- De lo contrario, rellenar como de costumbre, por ejemplo con una cantidad aleatoria de 0-15 bytes.

Estrategias similares podrían ser utilizadas en el tamaño óptimo de un solo mensaje de túnel (964)
y tamaño de tres mensajes de túnel (2952), aunque estos tamaños deberían ser raros en la práctica.


## Problemas

El valor 1812 es preliminar. Por confirmar y posiblemente ajustar.


## Migración

Sin problemas de compatibilidad hacia atrás.
Esta es una opción existente y la negociación del MTU ya es parte de la especificación.

Los destinos ECIES más antiguos soportarán 1730.
Cualquier cliente que reciba un valor más alto responderá con 1730, y el extremo contrario
negociará a la baja, como de costumbre.


