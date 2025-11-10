---
title: "Prueba de Pares IPv6"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Closed"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Descripción general

Esta propuesta es para implementar la Prueba de Pares SSU para IPv6.
Implementado en 0.9.27.

## Motivación

No podemos determinar y rastrear de manera confiable si nuestra dirección IPv6 está detrás de un firewall.

Cuando añadimos soporte IPv6 hace años, asumimos que IPv6 nunca tenía firewalls.

Más recientemente, en 0.9.20 (mayo de 2015), separamos el estado de alcanzabilidad v4/v6 internamente (ticket #1458).
Vea ese ticket para obtener amplia información y enlaces.

Si tienes todos los v4 y v6 detrás de un firewall, puedes simplemente forzar el firewall en la sección de configuración TCP en /confignet.

No tenemos prueba de pares para v6. Está prohibido en la especificación SSU.
Si no podemos probar regularmente la alcanzabilidad v6, no podemos transicionar sensiblemente desde/hacia el estado alcanzable v6.
Lo que nos queda es suponer que somos alcanzables si recibimos una conexión entrante,
y suponer que no lo somos si no hemos recibido una conexión entrante en un tiempo.
El problema es que una vez que declaras inalcanzable, no publicas tu IP v6,
y entonces no recibirás más (después de que el RI expire en la netdb de todos).


## Diseño

Implementar la Prueba de Pares para IPv6,
eliminando las restricciones previas de que la prueba de pares sólo estaba permitida para IPv4.
El mensaje de prueba de pares ya tiene un campo para la longitud de la IP.


## Especificación

En la sección de Capacidades de la descripción general de SSU, realiza la siguiente adición:

Hasta la versión 0.9.26, la prueba de pares no era compatible para direcciones IPv6, y
la capacidad 'B', si está presente para una dirección IPv6, debe ser ignorada.
A partir de la versión 0.9.27, la prueba de pares es compatible para direcciones IPv6, y
la presencia o ausencia de la capacidad 'B' en una dirección IPv6
indica soporte real (o falta de soporte).

En las secciones de Prueba de Pares de la descripción general de SSU y la especificación de SSU, realiza los siguientes cambios:

Notas sobre IPv6:
Hasta la versión 0.9.26, sólo se soporta la prueba de direcciones IPv4.
Por lo tanto, toda la comunicación Alice-Bob y Alice-Charlie debe ser a través de IPv4.
La comunicación Bob-Charlie, sin embargo, puede ser a través de IPv4 o IPv6.
La dirección de Alice, cuando se especifica en el mensaje PeerTest, debe tener 4 bytes.
A partir de la versión 0.9.27, se soporta la prueba de direcciones IPv6, y la comunicación Alice-Bob y Alice-Charlie puede ser a través de IPv6,
si Bob y Charlie indican soporte con una capacidad 'B' en su dirección IPv6 publicada.

Alice envía la solicitud a Bob usando una sesión existente sobre el transporte (IPv4 o IPv6) que ella desea probar.
Cuando Bob recibe una solicitud de Alice a través de IPv4, Bob debe seleccionar un Charlie que anuncie una dirección IPv4.
Cuando Bob recibe una solicitud de Alice a través de IPv6, Bob debe seleccionar un Charlie que anuncie una dirección IPv6.
La comunicación real Bob-Charlie puede ser a través de IPv4 o IPv6 (es decir, independiente del tipo de dirección de Alice).


## Migración

Los routers pueden:

1) No incrementar su versión a 0.9.27 o superior

2) Eliminar la capacidad 'B' de cualquier dirección SSU IPv6 publicada

3) Implementar la prueba de pares IPv6
