---
title: "Notas de estado de I2P del 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Actualización semanal del estado de I2P que incluye el lanzamiento de la versión 0.4.1.2, experimentos de limitación dinámica, desarrollo de la biblioteca de streaming para 0.4.2 y discusiones por correo electrónico"
categories: ["status"]
---

Hola a todos, es hora de nuestra actualización semanal

## Índice:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

La nueva versión 0.4.1.2 salió hace unos días y las cosas han ido más o menos como se esperaba; sin embargo, ha habido algunos contratiempos con el nuevo componente watchdog (supervisor), lo que hace que mate su router cuando las cosas están Mal en lugar de reiniciarlo. Como mencioné hoy más temprano, estoy buscando personas que usen la nueva herramienta de registro de estadísticas para enviarme algunos datos, así que agradecería mucho su ayuda.

## 2) 0.4.1.3

Habrá otra versión antes de que salga la 0.4.2, ya que quiero que la red sea lo más sólida posible antes de seguir adelante. En este momento estoy experimentando con una limitación dinámica de la participación en los tunnel: indicando a los routers que rechacen solicitudes de forma probabilística si están saturados o si sus tunnel son más lentos de lo habitual. Estas probabilidades y umbrales se calculan dinámicamente a partir de las estadísticas que se están recopilando: si tu tiempo de prueba de tunnel de 10 minutos es mayor que tu tiempo de prueba de tunnel de 60 minutos, acepta la solicitud de tunnel con una probabilidad de 60minRate/10minRate (y si tu número actual de tunnel es mayor que tu número promedio de tunnel a 60 minutos, acéptala con p=60mRate/curTunnels).

Otro posible mecanismo de limitación es suavizar el ancho de banda en esa línea - rechazando tunnels de forma probabilística cuando nuestro uso de ancho de banda se dispara. En cualquier caso, el propósito de todo esto es ayudar a distribuir el uso de la red y equilibrar los tunnels entre más personas. El principal problema que hemos tenido con el balanceo de carga ha sido un *exceso* abrumador de capacidad y, por ello, ninguno de nuestros "maldita sea, vamos lentos, rechacemos" disparadores se ha activado. Estos nuevos mecanismos probabilísticos deberían, con suerte, mantener bajo control los cambios rápidos.

No tengo ningún plan específico para cuándo saldrá la versión 0.4.1.3 - quizá el fin de semana. Los datos que la gente envíe (de más arriba) deberían ayudar a determinar si esto valdrá la pena, o si hay otras vías que valgan más la pena.

## 3) 0.4.2

Como discutimos en la reunión de la semana pasada, hemos cambiado el orden de las versiones 0.4.2 y 0.4.3 - la 0.4.2 será la nueva biblioteca de streaming, y la 0.4.3 será la actualización de tunnel.

He estado volviendo a revisar la bibliografía sobre la funcionalidad de transmisión en flujo de TCP y hay algunos temas interesantes que son motivo de preocupación para I2P. En concreto, nuestro alto tiempo de ida y vuelta nos inclina hacia algo como XCP, y probablemente deberíamos ser bastante agresivos con diversas formas de explicit congestion notification (notificación explícita de congestión), aunque no podemos aprovechar algo como la opción de marca de tiempo, ya que nuestros relojes pueden estar desincronizados hasta un minuto.

Además, querremos asegurarnos de que podamos optimizar la streaming lib (biblioteca de streaming) para gestionar conexiones de corta duración (para lo cual el TCP estándar es bastante malo) - por ejemplo, quiero poder enviar solicitudes HTTP GET pequeñas (<32KB) y respuestas pequeñas (<32KB) en literalmente tres mensajes:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
De todos modos, aún no se ha escrito mucho código para esto; la parte del protocolo parece bastante similar a TCP y los paquetes se asemejan a una combinación de la propuesta de human y la propuesta anterior. Si alguien tiene sugerencias o ideas, o quiere ayudar con la implementación, por favor póngase en contacto.

## 4) discusión por correo electrónico

Ha habido algunas discusiones interesantes sobre el correo electrónico dentro de (y fuera de) I2P - postman ha publicado un conjunto de ideas en línea y está buscando sugerencias. También ha habido discusiones relacionadas en #mail.i2p. ¿Quizá podamos lograr que postman nos dé una actualización?

## 5) ???

Eso es todo por el momento. Pásate por la reunión en unos minutos y trae tus comentarios :)

=jr
