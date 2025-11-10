---
title: "Notas de estado de I2P del 2005-04-19"
date: 2005-04-19
author: "jr"
description: "Actualización semanal que cubre las próximas correcciones de la versión 0.5.0.7, el avance del transporte UDP de SSU, los cambios en la hoja de ruta que trasladan la versión 0.6 a junio y el desarrollo de Q"
categories: ["status"]
---

Hola a todos, ya llegó ese momento de la semana otra vez,

* Index

1) Estado de la red 2) Estado de SSU 3) Actualización de la hoja de ruta 4) Estado de Q 5) ???

* 1) Net status

Durante las casi dos semanas desde que salió 0.5.0.6, las cosas han sido mayormente positivas, aunque los proveedores de servicios (eepsites(I2P Sites), ircd, etc.) se han estado encontrando con algunos errores últimamente. Si bien los clientes funcionan bien, con el tiempo un servidor puede encontrarse en una situación en la que el fallo de tunnels puede activar un código de throttling (limitación) excesivo, impidiendo la reconstrucción y publicación adecuadas del leaseSet.

Ha habido algunas correcciones en CVS, entre otras cosas, y espero que tengamos publicada una nueva versión 0.5.0.7 en uno o dos días.

* 2) SSU status

Para quienes no siguen mi blog (oh, tan emocionante), ha habido muchos avances con el transporte UDP, y ahora mismo es bastante seguro decir que el transporte UDP no será nuestro cuello de botella de rendimiento :) Mientras depuraba ese código, aproveché para revisar también la gestión de colas en niveles superiores, identificando puntos donde podemos eliminar estrangulamientos innecesarios. Como dije la semana pasada, todavía queda mucho por hacer. Habrá más información disponible cuando haya más información disponible.

* 3) Roadmap update

Ya es abril, así que la hoja de ruta [1] se ha actualizado en consecuencia - descartando la 0.5.1 y moviendo algunas fechas. El gran cambio ahí es pasar la 0.6 de abril a junio, aunque en realidad no es un cambio tan grande como parece. Como mencioné la semana pasada, mi propio calendario ha cambiado un poco, y en lugar de mudarme a $somewhere en junio, me mudaré a $somewhere en mayo. Aunque podríamos tener lo necesario para la 0.6 listo este mes, de ninguna manera voy a lanzar una actualización mayor como esa y luego desaparecer durante un mes, ya que la realidad del software es que habrá errores que no se detecten en las pruebas.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum ha estado trabajando a toda máquina en Q, añadiendo más novedades para nosotros, con las últimas capturas de pantalla publicadas en su sitio [2]. También ha hecho commit del código en CVS (¡genial!), así que esperamos poder comenzar las pruebas alfa pronto. Estoy seguro de que oiremos más de aum con detalles sobre cómo ayudar, o puedes explorar el contenido en CVS en i2p/apps/q/

[2] http://aum.i2p/q/

* 5) ???

También han estado ocurriendo muchas más cosas, con debates animados en la lista de correo, el foro y irc. No voy a intentar resumirlos aquí, ya que faltan solo unos minutos para la reunión, ¡pero pásate si hay algo que no se haya tratado y que quieras plantear!

=jr
