---
title: "Actualizaciones de Transmisión"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Closed"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Descripción General

Los routers Java I2P e i2pd más antiguos que la API 0.9.58 (lanzada en marzo de 2023)
son vulnerables a un ataque de repetición de paquetes SYN en streaming.
Esto es un problema de diseño del protocolo, no un error de implementación.

Los paquetes SYN están firmados, pero la firma del paquete SYN inicial enviado de Alice a Bob
no está vinculada a la identidad de Bob, por lo que Bob puede almacenar y repetir ese paquete,
enviándolo a alguna víctima, Charlie. Charlie pensará que el paquete proviene de
Alice y le responderá a ella. En la mayoría de los casos, esto es inofensivo, pero
el paquete SYN puede contener datos iniciales (como un GET o POST) que
Charlie procesará inmediatamente.


## Diseño

La solución es que Alice incluya el hash de destino de Bob en los datos firmados del SYN.
Bob verifica en la recepción que ese hash coincida con su hash.

Cualquier posible víctima de ataque, Charlie,
verifica estos datos y rechaza el SYN si no coincide con su hash.

Al usar el campo de opción NACKs en el SYN para almacenar el hash,
el cambio es compatible hacia atrás, porque no se espera que se incluyan
NACKs en el paquete SYN y actualmente se ignoran.

Como de costumbre, todas las opciones están cubiertas por la firma, por lo que Bob no puede
reescribir el hash.

Si Alice y Charlie son API 0.9.58 o más reciente, cualquier intento de repetición por parte de Bob será rechazado.


## Especificación

Actualizar la [especificación de Streaming](/docs/specs/streaming/) para añadir la siguiente sección:

### Prevención de repetición

Para prevenir que Bob use un ataque de repetición al almacenar un paquete SYNCHRONIZE firmado válido
recibido de Alice y lo envíe más tarde a una víctima Charlie,
Alice debe incluir el hash de destino de Bob en el paquete SYNCHRONIZE de la siguiente manera:

.. raw:: html

  {% highlight lang='dataspec' %}
  Establecer el campo de cuenta NACK en 8
  Establecer el campo NACKs en el hash de destino de 32 bytes de Bob

{% endhighlight %}

Al recibir un SYNCHRONIZE, si el campo de cuenta NACK es 8,
Bob debe interpretar el campo NACKs como un hash de destino de 32 bytes,
y debe verificar que coincida con su hash de destino.
También debe verificar la firma del paquete, como de costumbre,
ya que cubre todo el paquete, incluidos los campos de cuenta de NACK y de NACKs.
Si la cuenta de NACK es 8 y el campo de NACKs no coincide,
Bob debe descartar el paquete.

Esto es necesario para las versiones 0.9.58 y superiores.
Esto es compatible hacia atrás con versiones anteriores,
porque no se esperan NACKs en un paquete SYNCHRONIZE.
Los destinos no pueden y no deben saber qué versión está ejecutando la otra parte.

No es necesario ningún cambio para el paquete SYNCHRONIZE ACK enviado de Bob a Alice;
no incluya NACKs en ese paquete.


## Análisis de Seguridad

Este problema ha estado presente en el protocolo de streaming desde que se creó en 2004.
Fue descubierto internamente por los desarrolladores de I2P.
No tenemos evidencia de que el problema haya sido explotado alguna vez.
La posibilidad real de éxito de explotación puede variar ampliamente dependiendo
del protocolo de capa de aplicación y el servicio.
Las aplicaciones peer-to-peer probablemente sean más propensas a verse afectadas
que las aplicaciones cliente/servidor.


## Compatibilidad

No hay problemas. Todas las implementaciones conocidas actualmente ignoran el campo de NACKs en el paquete SYN.
E incluso si no lo ignoraran, e intentaran interpretarlo
como NACKs para 8 mensajes diferentes, esos mensajes no estarían pendientes
durante el handshake de SYNCHRONIZE y los NACKs no tendrían sentido.


## Migración

Las implementaciones pueden añadir soporte en cualquier momento, no se necesita coordinación.
Los routers Java I2P e i2pd implementaron esto en la API 0.9.58 (lanzada en marzo de 2023).


