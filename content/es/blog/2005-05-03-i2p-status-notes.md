---
title: "Notas de estado de I2P para 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Actualización semanal sobre la estabilidad de la red, el éxito de las pruebas en vivo del transporte SSU sobre UDP, los avances en el intercambio de archivos en i2phex y una próxima ausencia de 3 a 4 semanas"
categories: ["status"]
---

Hola a todos, hay muchas cosas sobre la mesa esta semana

* Index

1) Estado de la red 2) Estado de SSU 3) i2phex 4) ausente 5) ???

* 1) Net status

No hay grandes cambios en la salud general de la red: las cosas parecen bastante estables y, aunque hemos tenido algún que otro bache, los servicios parecen estar funcionando bien. Ha habido muchas actualizaciones en CVS desde la última versión, pero no correcciones de errores bloqueantes. Es posible que hagamos una versión más antes de mi mudanza, solo para distribuir más ampliamente lo último de CVS, pero aún no estoy seguro.

* 2) SSU status

¿Estás cansado de oírme decir que ha habido muchos avances en el transporte UDP? Pues, qué mala suerte: ha habido muchos avances en el transporte UDP. Durante el fin de semana dejamos las pruebas en red privada y pasamos a la red en producción, y una docena de routers aproximadamente se actualizaron y expusieron su dirección SSU, lo que permite que la mayoría de los usuarios los alcancen mediante el transporte TCP, pero que los routers con SSU habilitado se comuniquen vía UDP.

Las pruebas aún están en una etapa muy temprana, pero han ido mucho mejor de lo que esperaba. El control de congestión se comportó muy bien y tanto el rendimiento como la latencia fueron bastante adecuados - pudo identificar correctamente los límites reales de ancho de banda y compartir ese enlace de forma eficaz con flujos TCP en competencia.

Con las estadísticas recopiladas gracias a los voluntarios que prestaron su ayuda, quedó claro lo importante que es el código de acuse de recibo selectivo (SACK) para el funcionamiento correcto en redes altamente congestionadas. He pasado los últimos días implementando y probando ese código, y he actualizado la especificación de SSU [1] para incluir una nueva técnica SACK eficiente. No será retrocompatible con el código SSU anterior, por lo que las personas que han estado ayudando con las pruebas deberían desactivar el transporte SSU hasta que haya una nueva versión lista para probar (con suerte en uno o dos días).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup ha estado trabajando sin parar en un port (adaptación) de phex a i2p, y aunque queda mucho trabajo por hacer antes de que esté listo para el usuario promedio, esta noche, más temprano, pude ponerlo en marcha, navegar por los archivos compartidos de sirup, descargar algunos datos y usar su interfaz de chat *ejem* "instantánea".

Hay mucha más información disponible en el eepsite(I2P Site) de sirup [2], y la ayuda con las pruebas por parte de personas que ya están en la comunidad de i2p sería estupenda (aunque, por favor, hasta que sirup lo apruebe como una versión pública, y i2p haya llegado al menos a la 0.6, si no a la 1.0, mantengámoslo dentro de la comunidad de i2p). Creo que sirup estará presente en la reunión de esta semana, ¡así que quizá entonces podamos obtener más información!

[2] http://sirup.i2p/

* 4) awol

Hablando de estar por aquí, probablemente no estaré en la reunión de la próxima semana y estaré sin conexión durante las 3-4 semanas siguientes. Aunque eso probablemente signifique que no habrá nuevas versiones, todavía hay un montón de cosas realmente interesantes en las que la gente puede ponerse a trabajar:  = aplicaciones como feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,     el addressbook, susimail, q o algo completamente nuevo.  = el eepproxy - estaría genial incorporar filtrado, soporte para     conexiones HTTP persistentes, las ACL de 'listen on', y quizá un     backoff exponencial para tratar con timeouts de outproxy (en lugar de     plain round robin)  = el PRNG (como se discutió en la lista)  = una biblioteca de PMTU (ya sea en Java o en C con JNI)  = la recompensa por pruebas unitarias y la recompensa de GCJ  = perfilado y ajuste de memoria del router  = y mucho más.

Así que, si te sientes aburrido y quieres ayudar, pero necesitas inspiración, quizá alguna de las anteriores te anime a empezar. Probablemente pase por un cibercafé de vez en cuando, así que estaré localizable por correo electrónico, pero el tiempo de respuesta será del orden de días.

* 5) ???

De acuerdo, eso es todo lo que tengo para comentar por el momento. Para quienes quieran ayudar con las pruebas de SSU durante la próxima semana, estén atentos a la información en mi blog [3]. ¡Para el resto de ustedes, nos vemos en la reunión!

=jr [3] http://jrandom.dev.i2p/
