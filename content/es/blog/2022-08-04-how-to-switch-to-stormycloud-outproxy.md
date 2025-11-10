---
title: "Cómo cambiar al servicio de Outproxy (proxy de salida) de StormyCloud"
date: 2022-08-04
author: "idk"
description: "Cómo cambiar al servicio de Outproxy (proxy de salida) de StormyCloud"
categories: ["general"]
API_Translate: verdadero
---

## Cómo cambiar al servicio StormyCloud Outproxy

**Un nuevo Outproxy (proxy de salida) profesional**

Durante años, I2P ha contado con un único outproxy (proxy de salida) predeterminado, `false.i2p`, cuya fiabilidad se ha ido degradando. Aunque han surgido varios competidores para asumir parte de la carga, en su mayoría no pueden ofrecerse voluntariamente para atender de forma predeterminada a los clientes de toda una implementación de I2P. No obstante, StormyCloud, una organización profesional sin ánimo de lucro que opera nodos de salida de Tor, ha puesto en marcha un nuevo servicio profesional de outproxy que ha sido probado por miembros de la comunidad de I2P y que se convertirá en el nuevo outproxy predeterminado en la próxima versión.

**¿Quiénes son StormyCloud?**

En sus propias palabras, StormyCloud es:

> Misión de StormyCloud Inc: Defender el acceso a Internet como un derecho humano universal. Al hacerlo, el grupo protege la privacidad electrónica de los usuarios y construye comunidad fomentando el acceso sin restricciones a la información y, por tanto, el libre intercambio de ideas a través de las fronteras. Esto es esencial porque Internet es la herramienta más poderosa disponible para lograr un cambio positivo en el mundo.

> Hardware: Somos propietarios de todo nuestro hardware y actualmente realizamos colocation en un centro de datos Tier 4. A día de hoy contamos con un enlace ascendente (uplink) de 10GBps, con la opción de actualizar a 40GBps sin necesidad de grandes cambios. Contamos con nuestro propio ASN y espacio de direcciones IP (IPv4 e IPv6).

Para obtener más información sobre StormyCloud, visite su [sitio web](https://www.stormycloud.org/).

Or, visit them on [I2P](http://stormycloud.i2p/).

**Cambiar al Outproxy (proxy de salida) de StormyCloud en I2P**

Para cambiar al outproxy (proxy de salida) de StormyCloud *hoy mismo* puedes visitar [el Administrador de Servicios Ocultos](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0). Una vez allí, debes cambiar el valor de **Outproxies** y **SSL Outproxies** a `exit.stormycloud.i2p`. Una vez hecho esto, desplázate hasta la parte inferior de la página y haz clic en el botón "Save".

**Gracias a StormyCloud**

Queremos agradecer a StormyCloud por ofrecer voluntariamente servicios de outproxy de alta calidad a la red I2P.
