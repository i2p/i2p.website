---
title: "Notas de estado de I2P del 2006-10-10"
date: 2006-10-10
author: "jr"
description: "Lanzamiento 0.6.1.26 con comentarios positivos, Syndie 0.910a acercándose a la 1.0 y evaluación del control de versiones distribuido para Syndie"
categories: ["status"]
---

Hola a todos, breves notas de estado esta semana

* Index

1) 0.6.1.26 y estado de la red 2) Estado del desarrollo de Syndie 3) Revisión del control de versiones distribuido 4) ???

* 1) 0.6.1.26 and network status

El otro día publicamos una nueva versión 0.6.1.26, que incluye muchas mejoras de i2psnark de zzz y algunas nuevas comprobaciones de seguridad de NTP de Complication, y los informes han sido positivos. La red parece estar creciendo ligeramente sin nuevos efectos extraños, aunque algunas personas todavía tienen problemas para establecer sus tunnels (como siempre ha sido el caso).

* 2) Syndie development status

Han ido llegando cada vez más mejoras, y la versión alfa actual va por la 0.910a. La lista de funcionalidades para la 1.0 está prácticamente cumplida, así que ahora se trata en gran medida de corrección de errores y documentación. Pásate por #i2p si quieres ayudar a probar :)

Además, ha habido algunas discusiones en el canal sobre diseños de la GUI de Syndie - meerboop ha propuesto algunas ideas geniales y está trabajando en documentarlas. La GUI de Syndie es el componente principal de la versión Syndie 2.0, así que cuanto antes pongamos eso en marcha, antes podremos conquistar el mund^W^W^W^W lanzar Syndie entre las masas desprevenidas.

También hay una nueva propuesta en mi blog en Syndie sobre el seguimiento de errores y de solicitudes de nuevas funcionalidades usando el propio Syndie. Para facilitar el acceso, he publicado una exportación en texto plano de esa entrada en la web - la página 1 está en <http://dev.i2p.net/~jrandom/bugsp1.txt> y la página 2 está en <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

Una de las cosas que aún hay que resolver para Syndie es qué sistema público de control de versiones utilizar y, como se mencionó antes, es necesaria la funcionalidad distribuida y sin conexión. He estado revisando unas seis alternativas de código abierto que existen (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville), examinando a fondo su documentación, probándolas y hablando con sus desarrolladores. Por ahora, monotone y bzr parecen ser los mejores en términos de funcionalidad y seguridad (con repositorios no confiables, necesitamos criptografía fuerte para asegurarnos de que solo estamos incorporando cambios auténticos), y la estrecha integración criptográfica de monotone resulta muy atractiva. Aún estoy revisando varios cientos de páginas de documentación, pero por lo que he hablado con los desarrolladores de monotone, parecen estar haciendo todo de la manera correcta.

Por supuesto, independientemente del dvcs (sistema de control de versiones distribuido) que terminemos eligiendo, todas las versiones estarán disponibles en formato tarball simple, y se aceptarán parches para su revisión en formato diff -uw simple. Aun así, para quienes consideren involucrarse en el desarrollo, me encantaría conocer sus opiniones y preferencias.

* 4) ???

Como puedes ver, hay muchas cosas en marcha, como siempre. También ha habido más discusión en ese hilo "solve world hunger" del foro, así que consúltalo en <http://forum.i2p.net/viewtopic.php?t=1910>

Si tienes algo más que discutir, por favor pásate por #i2p para nuestra reunión de desarrollo de esta noche, o publícalo en el foro o en la lista.

=jr
