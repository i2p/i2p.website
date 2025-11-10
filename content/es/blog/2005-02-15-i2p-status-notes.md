---
title: "Notas de estado de I2P del 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que abarcan el crecimiento de la red hasta 211 routers, los preparativos para el lanzamiento de la versión 0.5 y i2p-bt 0.1.7"
categories: ["status"]
---

Hola, otra vez llegó ese momento de la semana,

* Index

1) Estado de la red 2) Estado de la versión 0.5 3) i2p-bt 0.1.7 4) ???

* 1) Net status

Si bien no han aparecido errores nuevos en la red, la semana pasada obtuvimos cierta exposición en un popular sitio web p2p francés, lo que ha llevado a un aumento tanto en usuarios como en la actividad de bittorrent.  En el punto más alto, alcanzamos 211 routers en la red, aunque últimamente se mantiene entre 150 y 180.  El uso de ancho de banda reportado también ha aumentado, aunque desafortunadamente la fiabilidad de irc se ha degradado, con uno de los servidores reduciendo sus límites de ancho de banda debido a la carga.  Ha habido varias mejoras en la biblioteca de streaming para ayudar con esto, pero han estado en la rama 0.5-pre, por lo que aún no están disponibles en la red en producción.

Otro problema transitorio ha sido la interrupción de uno de los outproxies HTTP (proxy de salida HTTP) (www1.squid.i2p), lo que provoca que el 50% de las solicitudes al outproxy fallen. Puedes quitar temporalmente ese outproxy abriendo la configuración de tu I2PTunnel [1], editando el eepProxy y cambiando la línea "Outproxies:" para que contenga solo "squid.i2p". Esperamos tener ese otro de nuevo en línea pronto para aumentar la redundancia.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Ha habido muchos avances esta última semana en 0.5 (apuesto a que ya estás cansado de oírlo, ¿eh?). Gracias a la ayuda de postman, cervantes, duck, spaetz y de alguien que no quiso ser nombrado, hemos estado ejecutando una red de pruebas con el nuevo código durante casi una semana y hemos resuelto una buena cantidad de errores que no había visto en mi red de pruebas local.

Desde hace aproximadamente un día, los cambios han sido menores, y no preveo que quede código sustancial por hacer antes de que salga la versión 0.5. Hay algo de limpieza adicional, documentación y ensamblaje pendientes, y no está de más dejar que la red de pruebas de la 0.5 siga funcionando por si con el tiempo se ponen de manifiesto errores adicionales.  Como esta va a ser una PUBLICACIÓN INCOMPATIBLE CON VERSIONES ANTERIORES, para que puedan planificar la actualización, fijaré como fecha límite sencilla ESTE VIERNES para la publicación de la 0.5.

Como bla mencionó en irc, los operadores de eepsite(I2P Site) pueden querer poner su sitio fuera de línea el jueves o el viernes y mantenerlo fuera de línea hasta el sábado, cuando muchos usuarios ya se habrán actualizado. Esto ayudará a reducir el efecto de un ataque de intersección (p. ej., si el 90% de la red ha migrado a 0.5 y usted aún está en 0.4, si alguien accede a su eepsite(I2P Site), sabrá que usted es parte del 10% de routers que quedan en la red).

Podría empezar a comentar lo que se ha actualizado en la versión 0.5, pero acabaría escribiendo páginas y páginas, así que quizá debería esperar y ponerlo en la documentación, que debería redactar :)

* 3) i2p-bt 0.1.7

duck ha preparado una versión de corrección de errores para la actualización 0.1.6 de la semana pasada, y se dice por ahí que está impresionante (quizá /demasiado/ potente, dado el aumento del uso de la red ;)  Más información en el foro i2p-bt [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

Muchas otras cosas están ocurriendo en las discusiones de IRC y en el foro [3], demasiado como para resumirlas brevemente. ¿Quizá las personas interesadas puedan pasarse por la reunión y darnos novedades e ideas? En fin, nos vemos en breve

=jr
