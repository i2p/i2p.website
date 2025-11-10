---
title: "Notas de estado de I2P del 2006-04-18"
date: 2006-04-18
author: "jr"
description: "0.6.1.16 mejoras de la red, análisis del colapso por congestión durante la creación de tunnel, y actualizaciones sobre el desarrollo de Feedspace"
categories: ["status"]
---

Hola a todos, vuelve a ser martes para nuestras notas de estado semanales

* Index

1) Estado de la red y 0.6.1.16 2) Creación de tunnel y congestión 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Con el 70% de la red actualizado a 0.6.1.16, parece que estamos observando una mejora respecto a las versiones anteriores y, con los problemas que se corrigieron en esa versión ya superados, tenemos una visión más clara de nuestro próximo cuello de botella.  Para quienes aún no estén en 0.6.1.16, por favor actualicen lo antes posible, ya que las versiones anteriores rechazarán arbitrariamente las solicitudes de creación de tunnels (incluso si el router tiene recursos suficientes para participar en más tunnels).

* 2) Tunnel creation and congestion

En este momento, parece que estamos experimentando lo que probablemente se describa mejor como colapso por congestión - las solicitudes de creación de tunnel están siendo rechazadas porque los routers tienen poco ancho de banda, así que se envían más solicitudes de creación de tunnel con la esperanza de encontrar otros routers con recursos disponibles, solo para aumentar el ancho de banda utilizado. Este problema existe desde que cambiamos al nuevo cifrado de creación de tunnel en 0.6.1.10 y puede vincularse en gran medida al hecho de que no recibimos retroalimentación por salto de aceptación/rechazo hasta que (o más exactamente, *a menos que*) la solicitud y la respuesta hayan recorrido la longitud de dos tunnels. Si cualquiera de esos pares no retransmite el mensaje, no sabemos qué par falló, qué pares aceptaron y qué pares lo rechazaron explícitamente.

Ya limitamos el número de solicitudes concurrentes de creación de tunnel en curso (y las pruebas muestran que aumentar el tiempo de espera no ayuda), por lo que la solución tradicional de Nagle no es suficiente.  Estoy probando ahora algunos ajustes a nuestro código de procesamiento de solicitudes para reducir la frecuencia de descartes silenciosos de solicitudes (en contraposición a rechazos explícitos), y a nuestro código de generación de solicitudes para reducir la concurrencia bajo carga.  También estoy probando otras mejoras que están logrando tasas de éxito sustancialmente mayores en la construcción de tunnel, aunque esas aún no están listas para un uso seguro.

Hay luz al final del tunnel, y agradezco su paciencia al seguir con nosotros a medida que avanzamos. Espero que tengamos otro lanzamiento más adelante esta semana para publicar algunas de las mejoras, tras lo cual reevaluaremos el estado de la red para ver si se ha abordado el colapso por congestión.

* 3) Feedspace

Frosk ha estado trabajando arduamente en Feedspace y ha actualizado algunas páginas en el sitio de Trac, incluyendo un nuevo documento de descripción general, un conjunto de tareas pendientes, algunos detalles de la base de datos y más.  Pásate por http://feedspace.i2p/ para ponerte al día con los cambios más recientes, y quizá bombardear a Frosk con preguntas en cuanto te sea posible :)

* 4) ???

Eso es todo lo que estoy listo para discutir por ahora, pero por favor pásate por #i2p para nuestra reunión más tarde esta noche (8pm UTC) y así charlamos un poco más!

=jr
