---
title: "Notas de estado de I2P para 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Actualización tardía que abarca el estado del lanzamiento 0.6, el sistema PeerTest, las introducciones de SSU, correcciones en la interfaz web de I2PTunnel y mnet sobre I2P"
categories: ["status"]
---

Hola a todos, notas con retraso hoy,

* Index:

1) estado de la versión 0.6 2) PeerTest 3) introducciones de SSU 4) interfaz web de I2PTunnel 5) mnet sobre i2p 6) ???

* 1) 0.6 status

Como habrán visto, lanzamos la versión 0.6 hace unos días y, en general, las cosas han ido bastante bien. Algunas de las mejoras en el transporte desde la 0.5.* han puesto de manifiesto problemas con la implementación de netDb, pero ya hay correcciones para gran parte de ello en fase de pruebas ahora (como la compilación 0.6-1) y se desplegarán como 0.6.0.1 en breve. También nos hemos encontrado con algunos problemas con distintas configuraciones de NAT y de cortafuegos, así como problemas de MTU con algunos usuarios - problemas que no estaban presentes en la red de pruebas más pequeña debido a que había menos probadores. Se han añadido soluciones alternativas para los casos más problemáticos, pero contamos con una solución a largo plazo que llegará pronto - peer tests (pruebas entre pares).

* 2) PeerTest

Con la 0.6.1, vamos a implementar un nuevo sistema para probar y configurar de forma colaborativa las direcciones IP públicas y los puertos. Está integrado en el protocolo SSU principal y será compatible con versiones anteriores. Básicamente, lo que hace es permitir que Alice le pregunte a Bob cuál es su dirección IP pública y su número de puerto y, a su vez, que Bob le pida a Charlie que confirme que su configuración es correcta o que averigüe cuál es la limitación que impide el correcto funcionamiento. La técnica no es nada nueva en la red, pero sí es una incorporación nueva a la base de código de I2P y debería eliminar la mayoría de los errores de configuración más comunes.

* 3) SSU introductions

Como se describe en la especificación del protocolo SSU, habrá funcionalidad para permitir que las personas detrás de cortafuegos y NAT participen plenamente en la red, incluso si de otro modo no pudieran recibir mensajes UDP no solicitados. No funcionará en todas las situaciones posibles, pero cubrirá la mayoría. Hay similitudes entre los mensajes descritos en la especificación de SSU y los mensajes necesarios para el PeerTest, así que quizá, cuando se actualice la especificación con esos mensajes, podamos acoplar las introducciones a los mensajes de PeerTest. En cualquier caso, desplegaremos estas introducciones en la 0.6.2, y eso también será compatible con versiones anteriores.

* 4) I2PTunnel web interface

Algunas personas han notado y han presentado informes sobre diversas anomalías en la interfaz web de I2PTunnel, y smeghead ha comenzado a preparar las correcciones necesarias; ¿podría explicar esas actualizaciones con más detalle, así como proporcionar una fecha estimada para ellas?

* 5) mnet over i2p

Aunque no he estado en el canal cuando se estaban llevando a cabo las discusiones, por lo que he leído en los logs parece que icepick ha estado haciendo algo de hacking para conseguir que mnet funcione sobre i2p - permitiendo que el almacén de datos distribuido de mnet ofrezca publicación de contenido resiliente con operación anónima. No sé demasiado sobre el progreso en este frente, pero parece que icepick está avanzando bien integrándose con I2P a través de SAM y twisted, ¿quizá icepick pueda contarnos más?

* 6) ???

Ok, hay muchas más cosas en marcha de las que he mencionado arriba, pero ya voy con retraso, así que supongo que debería dejar de escribir y enviar este mensaje. Podré conectarme un rato esta noche, así que si alguien está por ahí podríamos tener una reunión sobre las 9:30 p. m. o así (cuando leas esto ;) en #i2p en los servidores IRC habituales {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

¡Gracias por su paciencia y su ayuda para seguir avanzando!

=jr
