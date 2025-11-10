---
title: "Notas de estado de I2P del 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Actualización semanal de estado que cubre la versión 0.3.2.3, cambios de capacidad, actualizaciones del sitio web y consideraciones de seguridad"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, y la hoja de ruta**

Después del lanzamiento de la 0.3.2.3 la semana pasada, han hecho un gran trabajo al actualizarse: ahora solo nos quedan dos rezagados (uno en 0.3.2.2 y otro muy atrás en 0.3.1.4 :). En los últimos días la red ha sido más fiable de lo habitual: la gente permanece en irc.duck.i2p durante horas seguidas, las descargas de archivos de mayor tamaño desde eepsites(I2P Sites) se están completando correctamente y la accesibilidad general de eepsite(I2P Site) es bastante buena. Dado que va bien y quiero mantenerlos alerta, decidí cambiar algunos conceptos fundamentales y los tendremos desplegados en una versión 0.3.3 en uno o dos días.

Como algunas personas han comentado sobre nuestro cronograma, preguntándose si vamos a cumplir las fechas que habíamos publicado, decidí que probablemente debía actualizar el sitio web para reflejar la hoja de ruta que tengo en mi PalmPilot, así que lo hice [1]. Las fechas se han retrasado y algunos elementos se han reordenado, pero el plan sigue siendo el mismo que se discutió el mes pasado [2].

0.4 cumplirá con los cuatro criterios de lanzamiento mencionados (funcional, seguro, anónimo y escalable), aunque antes de 0.4.2 pocas personas detrás de NAT y cortafuegos podrán participar, y antes de 0.4.3 habrá un límite superior efectivo al tamaño de la red debido a la sobrecarga de mantener un gran número de conexiones TCP con otros routers.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Durante la última semana, más o menos, la gente en #i2p me ha oído de vez en cuando despotricar sobre cómo nuestras clasificaciones de fiabilidad son completamente arbitrarias (y los problemas que eso ha causado en las últimas versiones). Así que nos hemos deshecho por completo del concepto de fiabilidad, sustituyéndolo por una medición de capacidad: "¿cuánto puede hacer un par por nosotros?" Esto ha tenido efectos en cadena en todo el código de selección y perfilado de pares (y obviamente en la consola del router), pero, más allá de eso, no se cambió gran cosa.

Se puede ver más información sobre este cambio en la página revisada de selección de pares [3], y cuando se lance 0.3.3, podrán ver el impacto de primera mano (he estado experimentando con ello durante los últimos días, ajustando algunos parámetros, etc.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) actualizaciones del sitio web**

Durante la última semana, hemos avanzado mucho en el rediseño del sitio web [4] - simplificando la navegación, limpiando algunas páginas clave, importando contenido antiguo y redactando algunas entradas nuevas [5]. Estamos casi listos para poner el sitio en producción, pero aún quedan algunas cosas por hacer.

Hoy más temprano, duck revisó el sitio e hizo un inventario de las páginas que nos faltan, y después de las actualizaciones de esta tarde, hay algunos asuntos pendientes que espero que podamos abordar o conseguir voluntarios que se encarguen de ellos:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Más allá de eso, creo que el sitio está bastante cerca de estar listo para pasar a producción. ¿Alguien tiene sugerencias o inquietudes en ese sentido?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) ataques y defensas**

Connelly ha estado ideando algunos enfoques nuevos para intentar abrir brechas en la seguridad y el anonimato de la red, y al hacerlo ha dado con algunas formas en que podemos mejorar las cosas. Aunque algunos aspectos de las técnicas que describió no se ajustan del todo a I2P, ¿quizá ustedes puedan ver maneras de ampliarlas para atacar la red aún más? Vamos, inténtenlo :)

**5) ???**

Eso es más o menos todo lo que puedo recordar antes de la reunión de esta noche - por favor, no duden en plantear cualquier otra cosa que se me haya pasado por alto. En fin, nos vemos en #i2p en unos minutos.

=jr
