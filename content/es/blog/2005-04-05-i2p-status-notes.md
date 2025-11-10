---
title: "Notas de estado de I2P para 2005-04-05"
date: 2005-04-05
author: "jr"
description: "Actualización semanal sobre los problemas del lanzamiento 0.5.0.5, la investigación sobre el perfilado bayesiano de pares y el progreso de la aplicación Q"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) 0.5.0.5 2) Perfilado bayesiano de pares 3) Q 4) ???

* 1) 0.5.0.5

El lanzamiento 0.5.0.5 de la semana pasada ha tenido sus altibajos - el cambio principal para abordar algunos ataques en la netDb parece funcionar como se esperaba, pero ha dejado al descubierto algunos errores largamente pasados por alto en el funcionamiento de la netDb. Esto ha provocado problemas de fiabilidad considerables, especialmente para eepsites (sitios de I2P). No obstante, los errores se han identificado y solucionado en CVS, y esas correcciones, junto con algunas otras, se publicarán como la versión 0.5.0.6 en el transcurso del próximo día.

* 2) Bayesian peer profiling

bla ha estado investigando cómo mejorar nuestro perfilado de pares aprovechando un filtrado bayesiano simple a partir de las estadísticas recopiladas [1]. Parece bastante prometedor, aunque no estoy seguro de en qué punto está en este momento - ¿quizá podamos obtener una actualización de bla durante la reunión?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

Se está avanzando mucho con la aplicación Q de aum, tanto en la funcionalidad central como con algunas personas que están creando diversos frontends xmlrpc. Se rumorea que podríamos ver otra versión de Q este fin de semana, con un montón de novedades descritas en http://aum.i2p/q/

* 4) ???

Ok, sí, notas de estado muy breves, ya que confundí las zonas horarias *otra vez* (de hecho, también confundí los días; pensé que era lunes hasta hace unas horas). De todos modos, hay un montón de cosas en marcha que no se mencionan arriba, así que pásate por la reunión y a ver qué hay!

=jr
