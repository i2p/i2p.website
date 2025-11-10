---
title: "Notas de estado de I2P del 2006-03-21"
date: 2006-03-21
author: "jr"
description: "Integración de JRobin para estadísticas de red, bots de IRC biff y toopie, y anuncio de una nueva clave GPG"
categories: ["status"]
---

Hola a todos, ya es martes otra vez

* Index

1) Estado de la red 2) jrobin 3) biff y toopie 4) nueva clave 5) ???

* 1) Net status

La semana pasada ha sido bastante estable, sin ninguna nueva versión todavía.  He estado trabajando intensamente en la limitación de tunnel y en la operación de bajo ancho de banda, pero para ayudar con esas pruebas he integrado JRobin con la consola web y nuestro sistema de gestión de estadísticas.

* 2) JRobin

JRobin [1] es un port en Java puro de RRDtool [2], que nos permite generar gráficos bonitos como los que zzz ha estado produciendo con muy poca sobrecarga de memoria. Lo hemos configurado para funcionar íntegramente en memoria, de modo que no hay contención de bloqueos de archivos, y el tiempo para actualizar la base de datos es imperceptible. Hay un montón de cosas interesantes que JRobin puede hacer y que no estamos aprovechando, pero la próxima versión incluirá la funcionalidad básica, además de un medio para exportar los datos en un formato que RRDtool pueda entender.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman ha estado trabajando arduamente en algunos bots útiles, y me complace informar que el entrañable biff ha vuelto [3], avisándote cada vez que tienes correo (anónimo) mientras estás en irc2p. Además, postman ha creado un bot completamente nuevo para nosotros - toopie - para servir como bot de información para I2P/irc2p. Todavía estamos alimentando a toopie con preguntas frecuentes (FAQs), pero en breve entrará en los canales habituales. ¡Gracias, postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Para quienes estén prestando atención, se habrán dado cuenta de que mi clave GPG expira en unos días.  Mi nueva clave @ http://dev.i2p.net/~jrandom tiene la huella digital 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 y el ID de la clave 33DC8D49.  Esta publicación está firmada con mi clave antigua, pero mis publicaciones (y lanzamientos) posteriores durante el próximo año estarán firmadas con la nueva clave.

* 5) ???

Eso es todo por el momento - ¡pásate por #i2p en unos minutos para nuestra reunión semanal y saludar!

=jr
