---
title: "Notas de estado de I2P del 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Notas semanales del estado del desarrollo de I2P que incluyen actualizaciones de la versión 0.4.2.6, avances de tunnel en la versión 0.5 con filtros de Bloom, i2p-bt 0.1.6 y Fortuna PRNG (generador de números pseudoaleatorios)."
categories: ["status"]
---

Hola a todos, nuevamente es hora de una actualización

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

No lo parece, pero ha pasado más de un mes desde que salió la versión 0.4.2.6 y las cosas siguen en bastante buen estado.  Ha habido una serie de actualizaciones bastante útiles [1] desde entonces, pero nada realmente bloqueante que obligue a sacar una nueva versión.  Sin embargo, en el último día o dos hemos recibido correcciones de errores muy buenas (¡gracias anon y Sugadude!), y si no estuviéramos a punto de la versión 0.5, probablemente la empaquetaría y la publicaría.  La actualización de anon corrige un caso límite en la biblioteca de streaming que ha estado provocando muchas de las expiraciones de tiempo de espera vistas en BT y otras transferencias grandes, así que, si te sientes aventurero, hazte con CVS HEAD y pruébala.  O espera a la próxima versión, por supuesto.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Mucho, muchísimo progreso en el frente de la 0.5 (como cualquiera en la lista i2p-cvs [2] puede atestiguar). Todas las actualizaciones de tunnel y varios ajustes de rendimiento se han probado, y aunque no incluye mucho en cuanto a los diversos [3] algoritmos de orden impuesto, sí cubre lo básico. También hemos integrado un conjunto de filtros de Bloom (con licencia BSD) [4] de XLattice [5], lo que nos permite detectar ataques de repetición sin requerir ningún uso de memoria por mensaje y con una sobrecarga de casi 0 ms. Para acomodar nuestras necesidades, los filtros se han ampliado de manera trivial para que decaigan, de modo que, después de que un tunnel expire, el filtro ya no tenga los IVs (vectores de inicialización) que vimos en ese tunnel.

Aunque estoy intentando incluir todo lo que pueda en la versión 0.5, también me doy cuenta de que debemos esperar lo inesperado - es decir, que la mejor manera de mejorarlo es ponerlo en tus manos y aprender de cómo funciona (y cómo no funciona) para ti.  Para ayudar con esto, como he mencionado antes, vamos a lanzar una versión 0.5 (esperemos que la próxima semana), rompiendo la retrocompatibilidad, y luego trabajaremos en mejorarla a partir de ahí, lanzando una versión 0.5.1 cuando esté lista.

Al revisar la hoja de ruta [6], lo único que se pospone para la 0.5.1 es el ordenamiento estricto. También habrá mejoras en la limitación de tasa y el balanceo de carga con el tiempo, estoy seguro, pero espero que estemos ajustando eso prácticamente para siempre. Sin embargo, se han debatido otras cosas que esperaba incluir en la 0.5, como la herramienta de descarga y el código de actualización con un clic, pero parece que esas también se aplazarán.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck ha parcheado una nueva versión de i2p-bt (¡bien!), disponible en los lugares habituales, así que consigue la tuya mientras está caliente [7]. Entre esta actualización y el parche de anon para la biblioteca de streaming, prácticamente saturé mi enlace de subida mientras sembraba algunos archivos, así que pruébalo.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Como se mencionó en la reunión de la semana pasada, smeghead ha estado trabajando sin parar en un montón de actualizaciones distintas últimamente y, mientras lucha por hacer que I2P funcione con gcj, han surgido unos problemas realmente horribles con el PRNG (generador de números pseudoaleatorios) en algunas JVM, lo que prácticamente nos obliga a disponer de un PRNG en el que podamos confiar. Tras recibir respuesta del equipo de GNU-Crypto, aunque su implementación de Fortuna aún no se ha desplegado realmente, parece ser la que mejor encaja con nuestras necesidades. Puede que consigamos incluirla en la versión 0.5, pero lo más probable es que se aplace a la 0.5.1, ya que querremos ajustarla para que pueda proporcionarnos la cantidad necesaria de datos aleatorios.

* 5) ???

Muchas cosas están pasando, y últimamente también ha habido un repunte de actividad en el foro [8], así que seguro que se me han pasado algunas cosas. En cualquier caso, pásate por la reunión en unos minutos y di lo que tengas en mente (o simplemente lee sin participar y suelta algún comentario mordaz al azar)

=jr [8] http://forum.i2p.net/
