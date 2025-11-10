---
title: "Notas de estado de I2P del 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren el progreso del enrutamiento de tunnel 0.5, la adaptación de SAM a .NET, la compilación con GCJ y las discusiones sobre el transporte UDP"
categories: ["status"]
---

Hola a todos, breve informe de estado semanal

* Index

1) estado de 0.5 2) sam.net 3) progreso de gcj 4) udp 5) ???

* 1) 0.5 status

Durante la última semana ha habido mucho progreso en torno a la 0.5. Los problemas de los que hablábamos antes se han resuelto, lo que simplifica drásticamente la criptografía y elimina el problema de bucles de tunnel. La nueva técnica [1] se ha implementado y las pruebas unitarias ya están en su lugar. A continuación, voy a ensamblar más código para integrar esos tunnels en el router principal y luego construir la infraestructura de gestión de tunnel y de pools (agrupaciones). Una vez que eso esté listo, lo pasaremos por el simulador y, finalmente, a una red paralela para someterlo a pruebas intensivas antes de darle los últimos retoques y llamarlo 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead ha preparado un nuevo port del protocolo SAM a .net - c#, mono/gnu.NET compatible (¡bien por smeghead!). Esto está en cvs bajo i2p/apps/sam/csharp/ con nant y otras herramientas auxiliares - ahora todos ustedes, desarrolladores de .net, pueden empezar a hackear con i2p :)

* 3) gcj progress

smeghead definitivamente está en racha - según el último recuento, con algunas modificaciones el router compila con la última compilación de gcj [2] (w00t!).  Aún no funciona, pero las modificaciones para sortear la confusión de gcj con algunos constructos de clases internas son sin duda un avance.    ¿Quizá smeghead pueda darnos una actualización?

[2] http://gcc.gnu.org/java/

* 4) udp

No hay mucho que decir aquí, aunque Nightblade sí planteó un conjunto interesante de inquietudes [3] en el foro, preguntando por qué estamos optando por UDP. Si tienes inquietudes similares u otras sugerencias sobre cómo podemos abordar los problemas que señalé en mi respuesta, ¡por favor, participa!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Sí, vale, vuelvo a llegar tarde con las notas, descuéntame del sueldo ;)  De todos modos, hay mucho en marcha, así que pásate por el canal para la reunión, revisa los logs publicados después, o publica en la lista si tienes algo que decir.  Ah, por cierto, he cedido y he abierto un blog dentro de i2p [4].

=jr [4] http://jrandom.dev.i2p/ (clave en http://dev.i2p.net/i2p/hosts.txt)
