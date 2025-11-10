---
title: "Notas de estado de I2P del 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Breve actualización semanal sobre la estabilidad de la red 0.5.0.7, el progreso del transporte UDP SSU con soporte para múltiples redes y la financiación de la recompensa por pruebas unitarias"
categories: ["status"]
---

Hola a todos, hoy solo unas breves notas semanales de estado

* Index

1) Estado de la red 2) Estado de SSU 3) Recompensa por prueba unitaria 4) ???

* 1) Net status

La mayoría de las personas han actualizado a la versión 0.5.0.7 de la semana pasada con bastante rapidez (¡gracias!) y el resultado general parece positivo. La red parece bastante fiable y la limitación de velocidad previa de tunnel (túneles) se ha resuelto. Sin embargo, algunos usuarios siguen informando de problemas intermitentes y los estamos investigando.

* 2) SSU status

La mayor parte de mi tiempo la dedico al código UDP de la versión 0.6, y no, no está listo para su lanzamiento, y sí, hay progreso ;) Ahora mismo puede manejar múltiples redes, manteniendo algunos pares en UDP y otros en TCP con un rendimiento bastante razonable. La parte difícil es abordar todos los casos de congestión/contención, ya que la red en funcionamiento estará bajo carga constante, pero ha habido muchos avances en ese aspecto en el último día o así. Más noticias cuando haya más noticias.

* 3) Unit test bounty

Como duck mencionó en la lista [1], zab ha aportado fondos iniciales a una recompensa para ayudar a I2P con una serie de actualizaciones de pruebas - algunos fondos para cualquiera que pueda completar las tareas enumeradas en la página de la recompensa [2]. Hemos recibido algunas donaciones adicionales para esa recompensa [3] - actualmente asciende a $1000USD. Si bien las recompensas ciertamente no ofrecen "remuneración de mercado", son un pequeño incentivo para los desarrolladores que quieren ayudar.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Ok, llego tarde a la reunión otra vez... Probablemente debería firmar esto y enviarlo, ¿eh? Pásate por la reunión y también podemos hablar de otros temas.

=jr
