---
title: "Notas de estado de I2P del 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Actualización semanal que cubre el éxito del lanzamiento de la versión 0.6.1.4, el análisis del ataque de bootstrap, las correcciones de seguridad de I2Phex 0.1.1.34, el desarrollo de la aplicación de voz voi2p y la integración de feeds RSS en Syndie"
categories: ["status"]
---

Hola a todos, ya llegó otra vez ese momento de la semana

* Index

1) 0.6.1.4 y estado de la red 2) boostraps (arranques iniciales), predecesores, adversarios pasivos globales y CBR 3) i2phex 0.1.1.34 4) aplicación voi2p 5) syndie y sucker 6) ???

* 1) 0.6.1.4 and net status

El lanzamiento de la versión 0.6.1.4 del sábado pasado parece haber ido bastante bien: el 75% de la red ya se ha actualizado (¡gracias!), y la mayoría del resto está en 0.6.1.3 de todos modos. Las cosas parecen estar funcionando razonablemente bien y, aunque no he recibido muchos comentarios al respecto —ni positivos ni negativos—, supongo que ustedes se quejarían a gritos si fuera malo :)

En particular, me interesaría recibir cualquier comentario de personas que utilizan conexiones por módem de acceso telefónico, ya que las pruebas que he realizado son solo una simulación básica de ese tipo de conexión.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Ha habido mucha más discusión en la lista sobre algunas ideas, con un resumen de los ataques de bootstrap (arranque) publicado en línea [1]. He avanzado en la especificación de la criptografía para la opción 3, y aunque aún no se ha publicado nada, es bastante sencillo.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Ha habido más discusiones sobre cómo mejorar la resistencia frente a adversarios poderosos mediante tunnels de tasa de bits constante (CBR), y aunque tenemos la opción de explorar esa vía, actualmente está previsto para I2P 3.0, ya que su uso adecuado requiere recursos sustanciales y probablemente tendría un impacto medible en quién estaría dispuesto a usar I2P con tal sobrecarga, así como en qué grupos podrían o no siquiera ser capaces de hacerlo.

* 3) I2Phex 0.1.1.34

El sábado pasado también publicamos una nueva versión de I2Phex [2], que corregía una fuga de descriptores de archivo que con el tiempo provocaría que I2Phex fallara (¡gracias, Complication!) y eliminaba algo de código que permitía a otras personas indicarle de forma remota a tu instancia de I2Phex que descargara determinados archivos (¡gracias, GregorK!). Se recomienda encarecidamente actualizar.

También ha habido una actualización de la versión CVS (aún no publicada) que resuelve algunos problemas de sincronización: Phex asume que algunas operaciones de red se procesan de inmediato, mientras que I2P a veces puede tardar un rato en hacer las cosas :) Esto se manifiesta en que la interfaz gráfica se queda colgada por un tiempo, las descargas o subidas se estancan, o se rechazan conexiones (y quizá de algunas otras formas). Aún no se ha probado mucho, pero probablemente se incorpore a la 0.1.1.35 esta semana. Seguro que publicarán más novedades en el foro cuando las haya.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum está trabajando sin parar en su nueva aplicación de voz (y texto) sobre I2P, y aunque aún no la he visto, suena genial. Quizá Aum pueda darnos una actualización en la reunión, o podemos simplemente esperar pacientemente la primera versión alfa :)

* 5) syndie and sucker

dust ha estado trabajando en syndie y sucker, y la última compilación de CVS de I2P ahora te permite incorporar automáticamente contenido de fuentes RSS y Atom y publicarlo en tu blog de syndie. Por el momento, tienes que añadir explícitamente lib/rome-0.7.jar y lib/jdom.jar a tu wrapper.config (wrapper.java.classpath.20 y 21), pero más adelante lo incluiremos en el paquete para que no sea necesario. Sigue siendo un trabajo en curso, y rome 0.8 (aún no lanzado) parece ofrecer cosas muy interesantes, como la posibilidad de capturar los enclosures (adjuntos) de una fuente, que luego sucker podrá importar como un adjunto a una entrada de syndie (¡aunque ahora mismo ya maneja imágenes y enlaces también!).

Como con todos los feeds RSS, parece haber algunas discrepancias en cómo se incluye el contenido, así que algunos feeds se integran más suavemente que otros. Creo que si la gente ayudara a probarlo con distintos feeds y le avisara a dust de cualquier problema con el que se rompa, eso podría ser útil. En cualquier caso, esto pinta bastante emocionante, ¡buen trabajo, dust!

* 6) ???

Eso es todo por el momento, pero si alguien tiene alguna pregunta o quiere tratar algunos temas con más detalle, acérquense a la reunión a las 8 p. m. GMT (¡recuerden el horario de verano!).

=jr
