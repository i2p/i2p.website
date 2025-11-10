---
title: "Notas de estado de I2P del 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Actualización semanal sobre el éxito del lanzamiento 0.6.0.5, el rendimiento de floodfill netDb, los avances de Syndie con RSS y pet names (nombres personalizados), y la nueva aplicación susidns de gestión de la libreta de direcciones"
categories: ["status"]
---

Hola a todos,

* Index

1) Estado de la red 2) Estado de Syndie 3) susidns 4) ???

* 1) Net status

Como muchos han visto, la versión 0.6.0.5 se publicó la semana pasada tras una breve revisión 0.6.0.4, y, hasta ahora, la fiabilidad ha mejorado considerablemente y la red ha crecido más que nunca. Aún hay margen de mejora, pero parece que el nuevo netDb está funcionando según lo diseñado. Incluso hemos puesto a prueba el mecanismo de respaldo - cuando los pares floodfill no son accesibles, los routers recurren al netDb de Kademlia, y el otro día, cuando se produjo ese escenario, la fiabilidad de irc y de eepsite(Sitio I2P) no disminuyó de forma sustancial.

Recibí una pregunta sobre cómo funciona el nuevo netDb y he publicado la respuesta [1] en mi blog [2]. Como siempre, si alguien tiene preguntas sobre ese tipo de cosas, no duden en hacérmelas llegar, ya sea en la lista o fuera de ella, en el foro, o incluso en tu blog ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Como pueden ver en syndiemedia.i2p (y http://syndiemedia.i2p.net/), ha habido mucho progreso últimamente, incluyendo RSS, pet names (nombres personalizados), controles administrativos y los inicios de un uso razonable de css. También se han implementado la mayoría de las sugerencias de Isamoor, así como las de Adam, así que, si alguien tiene algo en mente que le gustaría ver ahí, ¡envíenme un mensaje!

Syndie está ya bastante cerca de la beta, momento en el cual se distribuirá como una de las aplicaciones predeterminadas de I2P, así como empaquetada de forma independiente, por lo que cualquier ayuda sería muy apreciada. Con las últimas incorporaciones de hoy (en cvs), personalizar la apariencia (skinning) de Syndie también es muy sencillo: basta con crear un nuevo archivo syndie_standard.css en tu directorio i2p/docs/, y los estilos especificados sustituirán los estilos predeterminados de Syndie. Más información al respecto se puede encontrar en mi blog [2].

* 3) susidns

Susi ha creado rápidamente otra aplicación web para nosotros: susidns [3]. Esto sirve como una interfaz sencilla para gestionar la aplicación addressbook (libreta de direcciones) - sus entradas, suscripciones, etc. Tiene muy buen aspecto, así que esperamos poder incluirla pronto como una de las aplicaciones predeterminadas, pero por ahora, es muy sencillo obtenerla desde su eepsite(I2P Site), guardarla en tu directorio webapps, reiniciar tu router, y listo.

[3] http://susi.i2p/?page_id=13

* 4) ???

Si bien sin duda nos hemos estado enfocando en el lado de las aplicaciones cliente (y seguiremos haciéndolo), aún dedico gran parte de mi tiempo al funcionamiento central de la red, y hay cosas interesantes en camino - cruce de cortafuegos y NAT mediante introductions (introducciones), autoconfiguración de SSU mejorada, ordenación y selección avanzada de pares, e incluso algo de manejo sencillo de rutas restringidas. En cuanto al sitio web, HalfEmpty ha realizado algunas mejoras en nuestras hojas de estilo (¡bien!).

En fin, hay mucho en marcha, pero eso es todo lo que tengo tiempo de mencionar por ahora; pásate por la reunión a las 8 p. m. UTC y saluda :)

=jr
