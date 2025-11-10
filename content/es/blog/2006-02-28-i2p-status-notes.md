---
title: "Notas de estado de I2P del 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Mejoras de red con 0.6.1.12, hoja de ruta hacia 0.6.2 con nuevas estrategias de selección de pares y oportunidades para miniproyectos"
categories: ["status"]
---

Hola a todos, es hora de nuestro desahogo de los martes otra vez

* Index

1) Estado de la red y 0.6.1.12 2) Camino hacia 0.6.2 3) Miniproyectos 4) ???

* 1) Net status and 0.6.1.12

La semana pasada trajo mejoras sustanciales en la red, primero con el despliegue generalizado de la 0.6.1.11 el martes pasado, seguido por la versión 0.6.1.12 de este lunes (que hasta ahora se ha distribuido al 70% de la red - ¡gracias!). En general, las cosas han mejorado mucho con respecto tanto a la 0.6.1.10 como a versiones anteriores: las tasas de éxito en la construcción de tunnels son un orden de magnitud superiores sin ninguno de esos tunnels de respaldo, la latencia ha bajado, el uso de CPU ha bajado y el rendimiento ha subido. Además, con TCP completamente deshabilitado, la tasa de retransmisión de paquetes se mantiene bajo control.

* 2) Road to 0.6.2

Todavía queda por mejorar el código de selección de pares, ya que seguimos viendo tasas de rechazo de tunnels de cliente del 10-20%, y los tunnels de alto rendimiento (10+KBps) no son tan comunes como deberían. Por otro lado, ahora que la carga de CPU ha bajado tanto, puedo ejecutar un router adicional en dev.i2p.net sin causar problemas a mi router principal (que sirve squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p y otros, moviendo 2-300+KBps).

Además, estoy probando algunas mejoras para personas en redes muy congestionadas (¿cómo?, ¿es que hay gente que no?). Parece haber algunos avances en ese frente, pero harán falta más pruebas.  Esto debería, espero, ayudar a las 4 o 5 personas en irc2p que parecen tener problemas para mantener conexiones estables (y, por supuesto, también a quienes sufren en silencio los mismos síntomas).

Una vez que eso funcione bien, todavía nos queda trabajo por hacer antes de poder llamarlo 0.6.2 - necesitamos las nuevas estrategias de ordenación de pares, además de estas estrategias mejoradas de selección de pares.  Como base, me gustaría tener tres estrategias nuevas - = ordenación estricta (limitando el predecesor y el sucesor de cada par,   con una rotación MTBF) = extremos fijos (usando un par fijo como puerta de enlace de entrada y   punto final de salida) = vecino limitado (usando un conjunto limitado de pares como el primer   salto remoto)

Hay otras estrategias interesantes por abordar, pero esas tres son las más relevantes.  Una vez que estén implementadas, estaremos funcionalmente completos para 0.6.2.  Estimación aproximada para marzo/abril.

* 3) Miniprojects

Hay más cosas útiles por hacer de las que puedo contar, pero solo quiero llamar su atención sobre una entrada en mi blog que describe cinco pequeños proyectos que un programador podría armar rápidamente sin invertir demasiado tiempo [1]. Si alguien está interesado en ponerse con alguno de ellos, estoy seguro de que asignaríamos algunos recursos [2] del fondo general a modo de agradecimiento, aunque me doy cuenta de que la mayoría de ustedes lo hace por el hack y no por el dinero ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

De todos modos, ese es un rápido resumen de lo que está pasando, hasta donde sé. Felicidades también a cervantes por el usuario número 500 del foro, por cierto :) Como siempre, pásate por #i2p para la reunión en unos minutos.

=jr
