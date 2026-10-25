---
title: "Proxy SOCKS"
description: "Usando el túnel SOCKS de I2P de forma segura"
slug: "socks"
aliases:
  - "/es/socks"
  - "/es/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS y Proxies SOCKS {#overview}

El proxy SOCKS funciona desde la versión 0.7.1. Se admiten SOCKS 4/4a/5. Habilita SOCKS creando un túnel cliente SOCKS en i2ptunnel. Se admiten tanto clientes compartidos como no compartidos. No hay outproxy SOCKS, por lo que tiene un uso limitado.

Como dice en las [FAQ](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
Y citando de un correo electrónico de 2005:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Esperar que simplemente podamos conectar un cliente arbitrario sobre I2P sin auditar tanto su comportamiento como los protocolos que expone en términos de seguridad y anonimato es ingenuo. Prácticamente *todas* las aplicaciones y protocolos violan el anonimato, a menos que hayan sido diseñados específicamente para ello, e incluso entonces, la mayoría de esos también lo hacen. Esa es la realidad. Los usuarios finales están mejor servidos con sistemas diseñados para el anonimato y la seguridad. Modificar sistemas existentes para que funcionen en entornos anónimos no es una hazaña menor, requiere órdenes de magnitud más trabajo que simplemente usar las APIs de I2P existentes.

El proxy SOCKS soporta nombres estándar de la libreta de direcciones, pero no destinos Base64. Los hashes Base32 deberían funcionar a partir de la versión 0.7. Solo soporta conexiones salientes, es decir, un Cliente I2PTunnel. El soporte UDP está esbozado pero aún no funciona. La selección de outproxy por número de puerto está esbozada.

## Ver También {#see-also}

- Las notas de la Reunión 81 (16 de marzo, 2004) y la Reunión 82 (23 de marzo, 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Si Logras Que Algo Funcione {#working}

Por favor háganoslo saber. Y por favor proporcionen advertencias sustanciales sobre los riesgos de los proxies SOCKS.
