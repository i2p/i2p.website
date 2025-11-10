---
title: "Notas de estado de I2P del 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren el lanzamiento 0.5.0.5 con procesamiento por lotes, protocolo de transporte UDP (SSU) y el almacén distribuido Q"
categories: ["status"]
---

Hola a todos, es hora de las notas de estado semanales

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Como todos hicieron un gran trabajo al actualizar a la 0.5.0.4 tan rápido, vamos a sacar la nueva versión 0.5.0.5 después de la reunión. Como se comentó la semana pasada, el gran cambio es la inclusión del código de batching (agrupación en lotes), que agrupa varios mensajes pequeños en lugar de darles a cada uno su propio mensaje de tunnel completo de 1KB. Si bien esto por sí solo no será revolucionario, debería reducir sustancialmente la cantidad de mensajes que se envían, así como el ancho de banda utilizado, especialmente para servicios como IRC.

Habrá más información en el anuncio de la versión, pero hay otras dos cosas importantes que se presentan con la revisión 0.5.0.5. Primero, dejaremos de brindar soporte a los usuarios con versiones anteriores a la 0.5.0.4 - hay bastante más de 100 usuarios en la 0.5.0.4, y hay problemas importantes con las versiones anteriores. Segundo, hay una corrección importante de anonimato en la nueva compilación que, si bien requeriría cierto esfuerzo de desarrollo para montarse, no es inverosímil. La mayor parte del cambio afecta a cómo gestionamos la netDb (base de datos de red) - en lugar de actuar a la ligera y almacenar en caché entradas por todas partes, solo responderemos a solicitudes de netDb para elementos que nos hayan sido entregados explícitamente, independientemente de si tenemos o no los datos en cuestión.

Como siempre, hay correcciones de errores y algunas funciones nuevas, pero habrá más información en el anuncio del lanzamiento.

* 2) UDP (SSU)

Como se ha venido comentando de forma intermitente durante los últimos 6-12 meses, vamos a migrar a UDP para nuestra comunicación entre routers una vez que se publique la versión 0.6.  Para avanzar más en ese camino, tenemos un primer borrador del protocolo de transporte disponible en CVS @ http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Es un protocolo bastante simple con los objetivos descritos en el documento, y aprovecha las capacidades de I2P para autenticar y proteger los datos, además de exponer la menor información externa posible. Ni siquiera la primera parte de un handshake de conexión (negociación inicial) es identificable para alguien que no esté ejecutando I2P. El comportamiento del protocolo aún no está completamente definido en la especificación, por ejemplo cómo se disparan los temporizadores o cómo se usan los tres indicadores de estado semiconfiables distintos, pero sí cubre los aspectos básicos del cifrado, la paquetización y el NAT hole punching (perforación de NAT). Nada de esto se ha implementado aún, pero lo estará pronto, ¡así que se agradecerán mucho los comentarios!

* 3) Q

Aum ha estado trabajando sin parar en Q(uartermaster), un sistema de almacenamiento distribuido, y la primera versión de la documentación ya está disponible [1].  Una de las ideas interesantes ahí consiste en alejarse de una DHT (tabla hash distribuida) directa hacia un sistema al estilo memcached [2], en el que cada usuario realiza cualquier búsqueda por completo de forma *local*, y solicita los datos propiamente dichos al servidor de Q "directamente" (bueno, a través de I2P).  En fin, cosas interesantes; quizá, si Aum está despierto [3], podamos arrancarle una actualización.

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] ¡Malditas zonas horarias!

* 4) ???

Hay muchas más cosas en marcha, y si quedaran algo más que unos pocos minutos para la reunión, podría seguir, pero así es la vida.  Pásate por aquí

# i2p en un rato para chatear.

=jr
