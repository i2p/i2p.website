---
title: "Resumen de Transportes"
description: "Visión general de la capa de transporte de I2P para la comunicación punto a punto entre routers"
slug: "transport"
aliases:
  - "/es/transport"
  - "/es/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transportes en I2P

Un "transport" en I2P es un método para la comunicación directa punto a punto entre dos routers. Los transports deben proporcionar confidencialidad e integridad contra adversarios externos mientras autentican que el router contactado es el que debería recibir un mensaje determinado.

I2P soporta múltiples transportes simultáneamente. Actualmente hay tres transportes implementados:

1. [NTCP](/docs/legacy/ntcp/), un transporte TCP Java New I/O (NIO)
2. [SSU](/docs/legacy/ssu/), o UDP Semiseguro Semifiable
3. [NTCP2](/docs/specs/ntcp2/), una nueva versión de NTCP

Cada uno proporciona un paradigma de "conexión", con autenticación, control de flujo, confirmaciones y retransmisión.

- Entrega confiable de mensajes [I2NP](/docs/specs/i2np/). Los transportes soportan entrega de mensajes I2NP ÚNICAMENTE. No son tuberías de datos de propósito general.
- La entrega en orden de los mensajes NO está garantizada por todos los transportes.
- Mantener un conjunto de direcciones del router, una o más para cada transporte, que el router publica como su información de contacto global (el RouterInfo). Cada transporte puede conectarse usando una de estas direcciones, que pueden ser IPv4 o (a partir de la versión 0.9.8) IPv6.
- Selección del mejor transporte para cada mensaje saliente
- Encolamiento de mensajes salientes por prioridad
- Limitación de ancho de banda, tanto saliente como entrante, según la configuración del router
- Configuración y desconexión de conexiones de transporte
- Cifrado de comunicaciones punto a punto
- Mantenimiento de límites de conexión para cada transporte, implementación de varios umbrales para estos límites, y comunicación del estado del umbral al router para que pueda hacer cambios operacionales basados en el estado
- Apertura de puertos del firewall usando UPnP (Universal Plug and Play)
- Traversal cooperativo de NAT/Firewall
- Detección de IP local por varios métodos, incluyendo UPnP, inspección de conexiones entrantes, y enumeración de dispositivos de red
- Coordinación del estado del firewall e IP local, y cambios en cualquiera de los dos, entre los transportes
- Comunicación del estado del firewall e IP local, y cambios en cualquiera de los dos, al router y la interfaz de usuario
- Determinación de un reloj de consenso, que se usa para actualizar periódicamente el reloj del router, como respaldo para NTP
- Mantenimiento del estado de cada peer, incluyendo si está conectado, si estuvo conectado recientemente, y si fue alcanzable en el último intento
- Cualificación de direcciones IP válidas según un conjunto de reglas locales
- Cumplimiento de las listas automatizadas y manuales de peers prohibidos mantenidas por el router, y rechazo de conexiones salientes y entrantes a esos peers

---

El subsistema de transporte en I2P proporciona los siguientes servicios:

## Servicios de Transporte

---

- Un router no tiene direcciones publicadas, por lo que se considera "oculto" y no puede recibir conexiones entrantes
- Un router está protegido por firewall, y por lo tanto publica una dirección SSU que contiene una lista de peers cooperativos o "introducers" que ayudarán en el traversal NAT (consulta [la especificación SSU](/docs/legacy/ssu/) para más detalles)
- Un router no está protegido por firewall o sus puertos NAT están abiertos; publica tanto direcciones NTCP como SSU que contienen IP y puertos directamente accesibles.

El subsistema de transporte mantiene un conjunto de direcciones de router, cada una de las cuales enumera un método de transporte, IP y puerto. Estas direcciones constituyen los puntos de contacto anunciados y son publicadas por el router en la base de datos de red. Las direcciones también pueden contener un conjunto arbitrario de opciones adicionales.

## Direcciones de Transporte

Cada método de transporte puede publicar múltiples direcciones de router.

Los escenarios típicos son:

---

- Configuración de preferencias de transporte
- Si el transporte ya está conectado al peer
- El número de conexiones actuales comparado con varios umbrales de límite de conexión
- Si los intentos de conexión recientes al peer han fallado
- El tamaño del mensaje, ya que diferentes transportes tienen diferentes límites de tamaño
- Si el peer puede aceptar conexiones entrantes para ese transporte, según se anuncia en su RouterInfo
- Si la conexión sería indirecta (requiriendo introducers) o directa
- La preferencia de transporte del peer, según se anuncia en su RouterInfo

El sistema de transporte entrega únicamente [mensajes I2NP](/docs/specs/i2np/). El transporte seleccionado para cualquier mensaje es independiente de los protocolos y contenidos de las capas superiores (mensajes del router o del cliente, si una aplicación externa estaba usando TCP o UDP para conectarse a I2P, si la capa superior estaba usando [la biblioteca de streaming](/docs/api/streaming/) o [datagramas](/docs/api/datagrams/), etc.).

## Selección de Transporte

Para cada mensaje saliente, el sistema de transporte solicita "ofertas" de cada transporte. El transporte que oferte el valor más bajo (mejor) gana la puja y recibe el mensaje para su entrega. Un transporte puede negarse a ofertar.

Si un transporte hace una oferta, y con qué valor, depende de numerosos factores:

En general, los valores de oferta se seleccionan de modo que dos routers solo estén conectados por un único transporte en cualquier momento dado. Sin embargo, esto no es un requisito.

- Un transporte similar a TLS/SSH
- Un transporte "indirecto" para routers que no son accesibles por todos los otros routers (una forma de "rutas restringidas")
- Transportes conectables compatibles con Tor

---

Pueden desarrollarse transportes adicionales, incluyendo:

## Nuevos Transportes y Trabajo Futuro

El trabajo continúa en el ajuste de los límites de conexión predeterminados para cada transporte. I2P está diseñado como una "red de malla", donde se asume que cualquier router puede conectarse a cualquier otro router. Esta suposición puede verse quebrantada por routers que han excedido sus límites de conexión, y por routers que están detrás de firewalls de estado restrictivos (rutas restringidas).

- Un transporte similar a TLS/SSH
- Un transporte "indirecto" para routers que no son accesibles por todos los demás routers (una forma de "rutas restringidas")
- Transportes intercambiables compatibles con Tor

Los límites de conexión actuales son más altos para SSU que para NTCP, basándose en la suposición de que los requerimientos de memoria para una conexión NTCP son mayores que los de SSU. Sin embargo, como los búferes de NTCP están parcialmente en el kernel y los búferes de SSU están en el heap de Java, esa suposición es difícil de verificar.

Analiza [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) y observa cómo el relleno a nivel de capa de transporte puede mejorar las cosas.

Analice [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) y vea cómo el relleno a nivel de capa de transporte podría mejorar las cosas.
