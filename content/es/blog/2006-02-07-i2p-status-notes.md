---
title: "Notas de estado de I2P para 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Progreso en las pruebas de la red PRE, optimización de exponente corto para el cifrado ElGamal, y I2Phex 0.1.1.37 con soporte para gwebcache"
categories: ["status"]
---

Hola a todos, otra vez es martes

* Index

1) Estado de la red 2) _PRE progreso de la red 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

No ha habido cambios sustanciales en la red en producción en la última semana, así que el estado de la red en producción no ha cambiado mucho.  Por otro lado...

* 2) _PRE net progress

La semana pasada empecé a hacer commits de código incompatible con versiones anteriores para la versión 0.6.1.10 en una rama separada en CVS (i2p_0_6_1_10_PRE), y un grupo de voluntarios ha ayudado a probarlo. Esta nueva red _PRE no puede comunicarse con la red en producción y no ofrece anonimato significativo (ya que hay menos de 10 pares). Con los registros de pen register (metadatos de conexiones) de esos routers, se han localizado y corregido algunos errores importantes tanto en el código nuevo como en el antiguo, aunque las pruebas y las mejoras continúan.

Un aspecto del nuevo esquema criptográfico de creación de tunnel es que el creador debe realizar por adelantado el cifrado asimétrico costoso para cada salto, mientras que la creación de tunnel anterior hacía el cifrado solo si el salto previo aceptaba participar en el tunnel. Este cifrado podría tardar 400-1000ms o más, dependiendo tanto del rendimiento de la CPU local como de la longitud del tunnel (realiza un cifrado ElGamal completo por cada salto). Una optimización que se utiliza actualmente en la _PRE net es el uso de un exponente corto [1] - en lugar de usar una 'x' de 2048 bits como clave de ElGamal, usamos una 'x' de 228 bits, que es la longitud sugerida para igualar el trabajo del problema del logaritmo discreto. Esto ha reducido el tiempo de cifrado por salto en un orden de magnitud, aunque no afecta el tiempo de descifrado.

Hay muchos puntos de vista contradictorios sobre el uso de exponentes cortos y, en general, no es seguro, pero por lo que he podido averiguar, dado que usamos un primo seguro fijo (grupo Oakley 14 [2]), el orden de q debería estar bien. Si alguien tiene más ideas en esta línea, sin embargo, me encantaría saber más.

La gran alternativa es pasar a cifrado de 1024 bits (en el que podríamos entonces usar, quizá, un exponente corto de 160 bits).  Esto podría ser apropiado en cualquier caso, y si las cosas resultan demasiado problemáticas con el cifrado de 2048 bits en la red _PRE, podríamos dar el salto dentro de la red _PRE. De lo contrario, podríamos esperar hasta la versión 0.6.1.10, cuando haya un despliegue más amplio del nuevo cifrado para ver si es necesario. Se proporcionará mucha más información si parece probable realizar tal cambio.

[1] "Sobre el acuerdo de claves de Diffie-Hellman con exponentes cortos" -     van Oorschot, Weiner en EuroCrypt 96.  espejado en     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

En cualquier caso, muchos avances en la _PRE net, con la mayor parte de la comunicación al respecto teniendo lugar dentro del canal #i2p_pre en irc2p.

* 3) I2Phex 0.1.1.37

Complication ha fusionado y parcheado el código más reciente de I2Phex para admitir gwebcaches, compatible con el port pycache de Rawn. Esto significa que los usuarios pueden descargar I2Phex, instalarlo, pulsar "Connect to the network", y, tras un minuto o dos, I2Phex obtendrá algunas referencias a pares de I2Phex existentes y se unirá a la red. ¡No más líos con gestionar manualmente archivos i2phex.hosts, ni compartir claves manualmente (w00t)! Hay dos gwebcaches por defecto, pero se pueden cambiar o añadir una tercera modificando las propiedades i2pGWebCache0, i2pGWebCache1 o i2pGWebCache2 en i2phex.cfg.

¡Buen trabajo, Complication y Rawn!

* 4) ???

Eso es todo por el momento, lo cual también es bueno, porque ya voy tarde a la reunión :)  Nos vemos en #i2p en breve

=jr
