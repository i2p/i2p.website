---
title: "Notas de estado de I2P del 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren el estado de la red, el diseño de enrutamiento de tunnel 0.5, i2pmail.v2 y la corrección de seguridad de azneti2p_0.2"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) Estado de red 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, not much to report here - things still work as they did last week, size of the net is still pretty similar, perhaps a little larger.  Some neat new sites are popping up - see the forum [1] and orion [2] for details.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Gracias a la ayuda de postman, dox, frosk y cervantes (y de todos los que trasladaron datos por sus routers mediante tunnels ;), hemos recopilado estadísticas del tamaño de los mensajes de un día completo [3]. Hay dos conjuntos de estadísticas allí - la altura y la anchura del zoom. Esto estuvo motivado por el deseo de explorar el impacto de diferentes estrategias de relleno de mensajes en la carga de la red, como se explica [4] en uno de los borradores del enrutamiento de tunnel 0.5. (ooOOoo imágenes bonitas).

Lo inquietante de lo que encontré al revisar todo eso fue que, usando unos umbrales de relleno bastante simples ajustados a mano, aplicar relleno hasta esos tamaños fijos aun así terminaría desperdiciando más del 25% del ancho de banda.  Sí, ya sé, no vamos a hacer eso. Quizá ustedes puedan dar con algo mejor analizando esos datos en bruto.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

En realidad, ese enlace [4] nos lleva al estado de los planes de la 0.5 para el enrutamiento de tunnel. Como publicó Connelly [5], últimamente ha habido mucha discusión en IRC sobre algunos de los borradores, con polecat, bla, duck, nickster, detonate y otros aportando sugerencias y haciendo preguntas incisivas (ok, y pullas ;). Tras algo más de una semana, encontramos una posible vulnerabilidad con [4] que tiene que ver con un adversario que, de algún modo, lograra hacerse con el control de la puerta de enlace del tunnel entrante y que además controlara uno de los otros pares más adelante en ese tunnel. Aunque en la mayoría de los casos esto, por sí solo, no expondría el extremo y sería difícil de lograr probabilísticamente a medida que la red crece, aun así Apesta (tm).

So in comes [6].  This gets rid of that issue, allows us to have tunnels of any length, and solves world hunger [7].  It does open another issue where an attacker could build loops in the tunnel, but based on a suggestion [8] Taral made last year regarding the session tags used on ElGamal/AES, we can minimize the damage done by using a series of synchronized pseudorandom number generators [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] ¿Adivina qué afirmación es falsa? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

No te preocupes si lo anterior te resulta confuso - estás viendo las tripas de algunos problemas de diseño bien enrevesados que se están resolviendo a la vista de todos. Si lo anterior *no* te suena confuso, ponte en contacto, porque siempre estamos buscando más cabezas para desmenuzar estos temas :)

De todos modos, como mencioné en la lista [10], lo siguiente que me gustaría es implementar la segunda estrategia [6] para resolver los detalles restantes.  El plan para 0.5 actualmente es reunir todos los cambios incompatibles con versiones anteriores - el nuevo cifrado de tunnel, etc - y publicar eso como 0.5.0, luego, a medida que eso se estabilice en la red, pasar a las otras partes de 0.5 [11], como ajustar la estrategia de pooling (agrupación) según se describe en las propuestas, y publicar eso como 0.5.1.  Espero que todavía podamos llegar a 0.5.0 para fin de mes, pero ya veremos.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

El otro día postman publicó un borrador de un plan de acción para la infraestructura de correo de próxima generación [12], y tiene una pinta realmente genial.  Por supuesto, siempre podemos imaginar aún más florituras y extras, pero su arquitectura es bastante buena en muchos aspectos.  Revisa lo que se ha documentado hasta ahora [13], y ponte en contacto con el postman con tus ideas.

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

Como publiqué en la lista [14], el plugin azneti2p original para azureus tenía un error grave de anonimato. El problema era que, en torrents mixtos donde algunos usuarios son anónimos y otros no, los usuarios anónimos contactaban a los no anónimos /directamente/ en lugar de a través de I2P. Paul Gardner y el resto de los desarrolladores de azureus respondieron con rapidez y publicaron un parche de inmediato. El problema que observé ya no está presente en azureus v. 2203-b12 + azneti2p_0.2.

Sin embargo, no hemos revisado ni auditado el código para evaluar posibles problemas de anonimato, así que "úsalo bajo tu propia responsabilidad" (por otro lado, decimos lo mismo acerca de I2P antes del lanzamiento de la versión 1.0). Si te animas, sé que los desarrolladores de Azureus agradecerían recibir más comentarios e informes de errores sobre el plugin. Por supuesto, mantendremos a la gente informada si nos enteramos de cualquier otro problema.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Hay mucho en marcha, como puedes ver. Creo que eso es todo lo que tengo que comentar, pero pásate por la reunión dentro de 40 minutos si hay algo más que te gustaría tratar (o si solo quieres desahogarte sobre lo anterior)

=jr
