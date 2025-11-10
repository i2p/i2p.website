---
title: "Notas de estado de I2P del 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Actualización breve sobre el estado de PeerTest, la transición de la red Irc2P, el progreso de la GUI (interfaz gráfica) de Feedspace y el cambio de la hora de la reunión a las 8 p. m. GMT"
categories: ["status"]
---

Hola a todos, hoy unas notas breves.

* Index:

1) Estado de PeerTest 2) Irc2P 3) Feedspace 4) meta 5) ???

* 1) PeerTest status

Como se mencionó antes, la próxima versión 0.6.1 incluirá una serie de pruebas para configurar con más cuidado el router y para verificar la alcanzabilidad (o señalar qué debe hacerse), y aunque ya hemos tenido algo de código en CVS desde hace dos compilaciones, aún quedan algunos retoques antes de que funcione con la fluidez necesaria. En este momento, estoy haciendo algunas ligeras modificaciones al flujo de pruebas documentado [1], añadiendo un paquete adicional para verificar la alcanzabilidad de Charlie y retrasando la respuesta de Bob a Alice hasta que Charlie haya respondido. Esto debería reducir la cantidad de valores de estado "ERR-Reject" innecesarios que la gente ve, ya que Bob no responderá a Alice hasta que cuente con un Charlie disponible para las pruebas (y cuando Bob no responde, Alice ve "Unknown" como estado).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

En fin, sí, eso es todo: debería salir la 0.6.0.2-3 mañana, y se publicará como versión cuando esté completamente probada.

* 2) Irc2P

Como se mencionó en el foro [2], los usuarios de I2P que usan IRC necesitan actualizar su configuración para cambiarse a la nueva red de IRC. Duck se desconectará temporalmente para [redacted], y en lugar de confiar en que el servidor no tenga ningún problema durante ese tiempo, postman y smeghead han tomado la iniciativa y han creado una nueva red de IRC para su uso. Postman también ha replicado el tracker de duck y el sitio i2p-bt en [3], y creo que vi algo en la nueva red de IRC sobre susi poniendo en marcha una nueva instancia de IdleRPG (consulta la lista de canales para más información).

¡Mi agradecimiento para los responsables de la antigua red i2pirc (duck, baffled, el equipo de metropipe, postman) y para los responsables de la nueva red irc2p (postman, arcturus)! ¡Los servicios y contenidos interesantes hacen que I2P valga la pena, y depende de ustedes crearlos!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Hablando de eso, el otro día estaba leyendo el blog de frosk y parece que hay más avances en Feedspace, en particular en una interfaz gráfica de usuario (GUI) muy agradable. Sé que puede que aún no esté lista para probarla, pero estoy seguro de que frosk nos enviará algo de código cuando llegue el momento. Por cierto, también he oído un rumor sobre otra herramienta de blogs basada en la web, orientada al anonimato, que está en camino y podrá integrarse con Feedspace cuando esté lista, pero, de nuevo, estoy seguro de que oiremos más información al respecto cuando esté lista.

* 4) meta

Como el maldito avaro que soy, me gustaría adelantar un poco las reuniones - en lugar de las 21:00 GMT, probemos a las 20:00 GMT. ¿Por qué? Porque se ajusta mejor a mi horario ;) (los cibercafés más cercanos no permanecen abiertos hasta muy tarde).

* 5) ???

Eso es todo por el momento - Voy a intentar estar cerca de un cibercafé para la reunión de esta noche, así que no duden en pasarse por #i2p a las *8*P GMT en los servidores irc /new/ {irc.postman.i2p, irc.arcturus.i2p}. Puede que tengamos un bot changate conectado a irc.freenode.net - ¿alguien quiere ejecutar uno?

chao, =jr
