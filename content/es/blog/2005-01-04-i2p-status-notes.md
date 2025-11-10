---
title: "Notas de estado de I2P del 2005-01-04"
date: 2005-01-04
author: "jr"
description: "Primeras notas de estado semanales de 2005 que cubren el crecimiento de la red hasta 160 routers, las características de la versión 0.4.2.6 y el desarrollo de la versión 0.5"
categories: ["status"]
---

Hola a todos, es hora de nuestras primeras notas de estado semanales de 2005

* Index

1) Estado de la red 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Durante la última semana, las cosas han estado bastante interesantes en la red: en Nochevieja, se publicaron comentarios en un sitio web popular hablando sobre i2p-bt y hemos tenido un pequeño aumento de nuevos usuarios. En este momento hay entre 120-150 routers en la red, aunque llegó a un máximo de 160 hace unos días. Aun así, la red aguantó bien, con pares de alta capacidad absorbiendo la carga adicional sin mucha interrupción para otros pares. Algunos usuarios que ejecutan sin límites de ancho de banda en enlaces realmente rápidos han reportado un caudal de 2-300KBps, mientras que aquellos con menos capacidad usan las habituales tasas bajas de 1-5KBps.

Creo recordar que Connelly mencionó que estaba viendo más de 300 routers diferentes a lo largo de unos días después de Año Nuevo, así que ha habido una rotación significativa. Por otro lado, ahora tenemos de forma estable entre 120 y 150 usuarios en línea, a diferencia de los 80-90 anteriores, lo cual es un aumento razonable. Aun así, *no* queremos que crezca demasiado todavía, ya que hay problemas de implementación conocidos que aún deben abordarse. En concreto, hasta la versión 0.6 [1], querremos mantenernos por debajo de 2-300 pares para mantener el número de hilos en un nivel razonable. Sin embargo, si alguien quiere ayudar a implementar el transporte UDP, podremos lograrlo mucho más rápido.

En la última semana, he estado observando las estadísticas que publican los trackers de i2p-bt y se han transferido gigas de archivos grandes, con algunos informes de 80-120KBps. IRC ha tenido más altibajos de lo habitual desde que se publicaron esos comentarios en ese sitio web, pero siguen pasando horas entre una desconexión y otra. (por lo que puedo ver, el router en el que está irc.duck.i2p ha estado funcionando bastante cerca de su límite de ancho de banda, lo cual explicaría las cosas)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Se han realizado algunas correcciones y se han añadido nuevas funciones a CVS desde la versión 0.4.2.5 que queremos desplegar pronto, incluyendo correcciones de fiabilidad para la biblioteca de streaming, una mayor resiliencia ante cambios de dirección IP y la inclusión de la implementación de la libreta de direcciones de ragnarok.

Si no has oído hablar del addressbook (libreta de direcciones) o no lo has usado, la versión corta es que actualizará mágicamente tu archivo hosts.txt al obtener periódicamente e integrar los cambios de algunas ubicaciones alojadas de forma anónima (siendo las predeterminadas http://dev.i2p/i2p/hosts.txt y http://duck.i2p/hosts.txt). No necesitarás cambiar ningún archivo, modificar ninguna configuración ni ejecutar aplicaciones adicionales - se implementará dentro del I2P router como un archivo .war estándar.

Por supuesto, si *de verdad* desea meterse de lleno con la libreta de direcciones (addressbook), es más que bienvenido - consulte el sitio de Ragnarok [2] para los detalles. Las personas que ya tengan la libreta de direcciones implementada en su router tendrán que hacer algunos ajustes durante la actualización a la 0.4.2.6, pero funcionará con todos sus parámetros de configuración anteriores.

[2] http://ragnarok.i2p/

* 3) 0.5

¡Números, números, números! Bueno, como he dicho antes, la versión 0.5 renovará cómo funciona el tunnel routing (enrutamiento de túneles), y se está avanzando en ese frente. En los últimos días he estado implementando el nuevo código de cifrado (y pruebas unitarias), y cuando estén funcionando publicaré un documento que describa mis ideas actuales sobre cómo, qué y por qué operará el nuevo tunnel routing. Estoy implementando ahora el cifrado para esto, en lugar de más tarde, para que la gente pueda revisar lo que significa en un sentido concreto, así como detectar áreas problemáticas y sugerir mejoras. Espero tener el código funcionando para finales de la semana, así que quizá haya más documentos publicados este fin de semana. Aunque no prometo nada.

* 4) jabber @ chat.i2p

jdot ha puesto en marcha un nuevo servidor Jabber, y parece funcionar bastante bien tanto para conversaciones uno a uno como para chat de grupo. Consulta la información en el foro [3]. El canal de discusión de desarrollo de i2p seguirá siendo el irc #i2p, pero siempre es bueno tener alternativas.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

Ok, eso es prácticamente todo lo que tengo que mencionar por ahora - estoy seguro de que hay mucho más en marcha que otros querrán comentar, así que pásate por la reunión en 15m en el lugar de siempre [4] y cuéntanos qué hay!

=jr
