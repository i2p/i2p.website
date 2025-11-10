---
title: "Notas de estado de I2P del 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Actualización semanal sobre el crecimiento de la red hasta 400-500 pares, la integración de Fortuna PRNG, el soporte de compilación nativa con GCJ, el cliente de torrent ligero i2psnark y el análisis del ataque de bootstrap (arranque) del tunnel"
categories: ["status"]
---

Hola a todos, más noticias desde el frente

* Index

1) Estado de la red 2) Integración de Fortuna 3) Estado de GCJ 4) i2psnark regresa 5) Más sobre bootstrapping (arranque) 6) Investigaciones sobre virus 7) ???

* 1) Net status

La última semana ha estado bastante bien en la red - las cosas parecen bastante estables, el caudal es normal, y la red sigue creciendo hasta el rango de 4-500 pares. También ha habido algunas mejoras significativas desde la versión 0.6.1.3 y, como afectan al rendimiento y la fiabilidad, espero que tengamos una versión 0.6.1.4 más adelante esta semana.

* 2) Fortuna integration

Gracias a la solución rápida de Casey Marshall [1], hemos podido integrar el generador de números pseudoaleatorios Fortuna [2] de GNU-Crypto. Esto elimina la causa de mucha frustración con la JVM de Blackdown y nos permite trabajar sin problemas con GCJ. Integrar Fortuna en I2P fue una de las principales razones por las que smeghead desarrolló "pants" (un 'portage' basado en 'ant'), así que ahora hemos tenido otro uso exitoso de pants :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Como se mencionó en la lista [3], ahora podemos ejecutar el router y la mayoría de los clientes sin problemas con GCJ [4]. La consola web en sí aún no funciona por completo, así que tienes que hacer tu propia configuración del router con router.config (aunque debería simplemente funcionar y poner en marcha tus tunnels tras un minuto aproximadamente). No estoy del todo seguro de cómo encajará GCJ en nuestros planes de lanzamiento, aunque en este momento me inclino por distribuir java puro pero dar soporte tanto a java como a versiones compiladas de forma nativa. Es un poco engorroso tener que compilar y distribuir muchas compilaciones diferentes para distintos sistemas operativos y versiones de bibliotecas, etc. ¿Alguien tiene alguna opinión firme al respecto?

Otra característica positiva del soporte de GCJ es la posibilidad de usar la biblioteca de streaming desde C/C++/Python/etc. No sé si alguien está trabajando en ese tipo de integración, pero probablemente valga la pena; así que, si te interesa trabajar en ese frente, ¡por favor avísame!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Mientras que i2p-bt fue el primer cliente de BitTorrent portado a I2P que tuvo mucho uso, eco se adelantó con su port de snark [5] hace ya bastante tiempo. Por desgracia, no se mantuvo al día ni conservó la compatibilidad con los otros clientes de BitTorrent anónimos, así que desapareció durante un tiempo. La semana pasada, sin embargo, estuve teniendo dificultades para lidiar con cuestiones de rendimiento en algún punto de la cadena i2p-bt<->sam<->streaming lib<->i2cp, así que me pasé al código original de snark de mjw e hice un port sencillo [6], reemplazando cualquier llamada a java.net.*Socket por llamadas a I2PSocket*, InetAddresses por Destinations y URLs por llamadas a EepGet. El resultado es un pequeño cliente de BitTorrent de línea de comandos (unos 60KB compilado) que ahora incluiremos en la versión de I2P.

Ragnarok ya ha empezado a hackearlo para mejorar su algoritmo de selección de bloques, y esperamos poder incorporar tanto una interfaz web como funcionalidad multitorrent antes de la versión 0.6.2. Si te interesa ayudar, ¡ponte en contacto! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

La lista de correo ha estado bastante activa últimamente, con las nuevas simulaciones y el análisis de Michael sobre la construcción del tunnel. La discusión sigue en curso, con algunas buenas ideas de Toad, Tom y polecat, así que consúltala si quieres aportar tu opinión sobre los compromisos en algunas cuestiones de diseño relacionadas con el anonimato que estaremos rediseñando para la versión 0.6.2 [7].

Para quienes buscan algo vistoso, Michael también te tiene cubierto, con una simulación de la probabilidad de que el ataque pueda identificarte - en función del porcentaje de la red que controlan [8], y en función de lo activo que esté tu tunnel [9]

(¡buen trabajo, Michael, gracias!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (siga el hilo "i2p tunnel bootstrap attack") [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Ha habido cierta discusión sobre posibles problemas de malware que se estarían distribuyendo junto con una aplicación específica con I2P habilitado, y Complication ha hecho un gran trabajo investigándolo. La información está disponible, así que puedes formarte tu propia opinión. [10]

¡Gracias, Complication, por toda tu investigación al respecto!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Muchas, muchísimas cosas pasando, como puedes ver, pero como ya llego tarde a la reunión, probablemente debería guardar esto y enviarlo, ¿eh? Nos vemos en #i2p :)

=jr
