---
title: "Notas de estado de I2P del 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Actualización semanal que cubre el éxito del lanzamiento de la versión 0.6.1.2, un nuevo proxy I2PTunnelIRCClient para filtrar mensajes de IRC no seguros, Syndie CLI y la conversión de RSS a SML, y planes de integración de I2Phex"
categories: ["status"]
---

Hola a todos, otra vez es martes

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Esteganografía y redes oscuras (sobre: flamewar) 6) ???

* 1) 0.6.1.2

La versión 0.6.1.2 de la semana pasada ha ido bastante bien hasta ahora: el 75% de la red se ha actualizado, HTTP POST está funcionando bien y la streaming lib (biblioteca de streaming) está transmitiendo datos con una eficiencia razonable (la respuesta completa a una solicitud HTTP a menudo se recibe en un único viaje de ida y vuelta de extremo a extremo). La red también ha crecido un poco: las cifras estables parecen rondar los 400 pares, aunque se disparó un poco más hasta 6-700 con rotación (churn) durante el pico de la mención en digg/gotroot [1] el fin de semana.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (sí, un artículo muy antiguo, lo sé, pero alguien lo volvió a encontrar)

Desde que salió la 0.6.1.2, se han añadido aún más mejoras - se ha encontrado (y corregido) la causa de los recientes netsplits (divisiones de la red) de irc2p, y también se han hecho mejoras bastante importantes en la transmisión de paquetes de SSU (ahorrando más de un 5% de los paquetes). No estoy seguro de cuándo saldrá exactamente la 0.6.1.3, pero quizá más tarde esta semana. Ya veremos.

* 2) I2PTunnelIRCClient

El otro día, tras algo de debate, dust preparó rápidamente una nueva extensión para I2PTunnel - el proxy "ircclient". Funciona filtrando el contenido enviado y recibido entre el cliente y el servidor a través de I2P, eliminando mensajes de IRC inseguros y reescribiendo los que deban ajustarse. Después de algunas pruebas, está funcionando bastante bien, y dust lo ha aportado a I2PTunnel y ahora se ofrece a la gente a través de la interfaz web. Ha sido estupendo que la gente de irc2p haya parcheado sus servidores IRC para descartar mensajes inseguros, pero ahora ya no tenemos que confiar en que lo hagan: el usuario local tiene control sobre su propio filtrado.

Usarlo es bastante fácil - en lugar de crear un "Client proxy" para IRC como antes, simplemente crea un "IRC proxy". Si quieres convertir tu "Client proxy" existente en un "IRC proxy", puedes (cringe) editar el archivo i2ptunnel.config, cambiando "tunnel.1.type=client" a "tunnel.1.ircclient" (o el número que corresponda para tu proxy).

Si todo va bien, esto se convertirá en el tipo de proxy predeterminado de I2PTunnel para conexiones de IRC en la próxima versión.

¡Buen trabajo, dust, gracias!

* 3) Syndie

La función de sindicación programada de Ragnarok parece ir bien y, desde que salió la versión 0.6.1.2, han surgido dos funciones nuevas: he añadido una CLI nueva y simplificada para publicar en Syndie [2], y dust (¡bien por dust!) ha preparado algo de código para extraer contenido de un canal RSS/Atom, incorporar cualquier enclosures (adjuntos) o imágenes referenciadas en él, y convertir el contenido RSS a SML (!!!) [3][4].

Las implicaciones de ambos en conjunto deberían ser claras. Más noticias cuando haya más noticias.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (lo integraremos en CVS en breve)

* 4) I2Phex

Se dice que I2Phex está funcionando bastante bien, pero que con el tiempo aún persisten algunos problemas. Ha habido cierta discusión en el foro [5] sobre cómo proceder, y GregorK, el desarrollador principal de Phex, incluso ha intervenido para manifestar su apoyo a integrar la funcionalidad de I2Phex de nuevo en Phex (o al menos permitir que el Phex principal ofrezca una interfaz de plugin sencilla para la capa de transporte).

Esto sería realmente genial, ya que significaría mucho menos código que mantener y, además, obtendríamos el beneficio del trabajo del equipo de Phex en la mejora de la base de código. Sin embargo, para que esto funcione, necesitamos que algunos hackers den un paso al frente y se encarguen de la migración. El código de I2Phex deja bastante claro dónde sirup cambió cosas, así que no debería ser demasiado difícil, pero probablemente tampoco sea del todo trivial ;)

No tengo tiempo para ponerme con esto ahora mismo, pero pásate por el foro si quieres ayudar.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

La lista de correo [6] ha estado bastante activa últimamente con la discusión sobre esteganografía y darknets (redes oscuras). El tema se ha trasladado en gran medida a la lista técnica de Freenet [7] con el asunto "flamewar de teorías conspirativas de I2P", pero todavía continúa.

No estoy seguro de que tenga mucho que añadir que no esté ya en las propias publicaciones, pero algunas personas han mencionado que la discusión les ha ayudado a entender mejor I2P y Freenet, así que quizá valga la pena echarle un vistazo. O quizá no ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Como puedes ver, hay muchas cosas emocionantes en marcha, y estoy seguro de que se me escapa algo. ¡Pásate por #i2p en unos minutos para nuestra reunión semanal y saluda!

=jr
