---
title: "Notas de estado de I2P del 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que abarcan los avances del cifrado de tunnel 0.5, un nuevo servidor NNTP y propuestas técnicas"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) estado 0.5 2) nntp 3) propuestas técnicas 4) ???

* 1) 0.5 status

Ha habido muchos avances en lo referente a la 0.5, con una gran tanda de commits ayer. La mayor parte del router ahora usa el nuevo cifrado de tunnel y la agrupación de tunnel [1], y ha estado funcionando bien en la red de pruebas. Todavía quedan por integrar algunas piezas clave, y el código obviamente no es retrocompatible, pero espero que podamos hacer un despliegue a mayor escala en algún momento de la próxima semana.

Como se mencionó antes, la versión inicial 0.5 proporcionará la base sobre la cual puedan operar distintas estrategias de selección/ordenación de pares de tunnel.  Comenzaremos con un conjunto básico de parámetros configurables para los conjuntos de tipo exploratorio y de cliente, pero es probable que versiones posteriores incluyan otras opciones para distintos perfiles de usuario.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Como se menciona en el sitio de LazyGuy [2] y en mi blog [3], tenemos un nuevo servidor NNTP en funcionamiento en la red, accesible en nntp.fr.i2p. Mientras LazyGuy ha puesto en marcha algunos scripts de suck [4] para leer unas cuantas listas de gmane, el contenido es, en buena medida, de, para y por usuarios de I2P. jdot, LazyGuy y yo investigamos qué lectores de noticias podían usarse de forma segura, y parece que hay soluciones bastante sencillas. Consulta mi blog para obtener instrucciones sobre cómo ejecutar slrn [5] para realizar lectura y publicación anónimas de noticias.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion y otros han publicado una serie de RFC para diversas cuestiones técnicas en el wiki de ugha [6] con el fin de ayudar a desarrollar en detalle algunos de los problemas más complejos a nivel de cliente y de aplicación. Por favor, utilicen ese espacio como el lugar para discutir cuestiones de nomenclatura, actualizaciones de SAM, ideas sobre swarming (descarga en enjambre), y similares: cuando publiquen allí, todos podremos colaborar en nuestro propio lugar para obtener un mejor resultado.

[6] http://ugha.i2p/I2pRfc

* 4) ???

Eso es todo lo que tengo por ahora (menos mal, porque la reunión empieza en breve). Como siempre, publica tus ideas cuando y donde quieras :)

=jr
