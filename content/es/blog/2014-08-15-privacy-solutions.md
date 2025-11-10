---
title: "El nacimiento de Privacy Solutions"
date: 2014-08-15
author: "Meeh"
description: "Lanzamiento de la organización"
categories: ["press"]
---

¡Hola a todos!

Hoy anunciamos el proyecto Privacy Solutions, una nueva organización que desarrolla y mantiene software de I2P. Privacy Solutions incluye varias iniciativas de desarrollo nuevas diseñadas para mejorar la privacidad, la seguridad y el anonimato de los usuarios, basadas en los protocolos y la tecnología de I2P.

Estos esfuerzos incluyen:

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

La financiación inicial de Privacy Solutions fue aportada por los partidarios de los proyectos Anoncoin y Monero. Privacy Solutions es una organización sin fines de lucro con sede en Noruega, inscrita en los registros del gobierno noruego. (Algo parecido a una 501(c)3 de EE. UU.)

Privacy Solutions planea solicitar financiación al gobierno noruego para investigación en redes, debido a BigBrother (ya explicaremos de qué se trata) y a las monedas que se prevé utilicen redes de baja latencia como capa de transporte principal. Nuestra investigación respaldará los avances en tecnología de software para el anonimato, la seguridad y la privacidad.

Primero, un poco sobre el Abscond Browser Bundle. Al principio fue un proyecto unipersonal de Meeh, pero más tarde amigos empezaron a enviar parches; ahora el proyecto intenta ofrecer el mismo acceso sencillo a I2P que tiene Tor con su Paquete del Navegador. Nuestro primer lanzamiento no está muy lejos; solo quedan algunas tareas en los scripts de gitian, incluida la configuración de la cadena de herramientas de Apple. Además, añadiremos monitorización con PROCESS_INFORMATION (una estructura de C que mantiene información vital sobre un proceso) desde la instancia de Java para comprobar el estado de I2P antes de declararlo estable. I2pd también sustituirá a la versión en Java cuando esté listo, y ya no tiene sentido distribuir un JRE dentro del paquete. Puedes leer más sobre el Abscond Browser Bundle en https://hideme.today/dev

También nos gustaría informar sobre el estado actual de i2pd. i2pd ahora admite streaming bidireccional, lo que permite utilizar no solo HTTP sino también canales de comunicación de larga duración. Se ha añadido soporte inmediato para IRC. Los usuarios de i2pd pueden usarlo del mismo modo que Java I2P para acceder a la red IRC de I2P. I2PTunnel es una de las características clave de la red I2P, que permite que aplicaciones no-I2P se comuniquen de forma transparente. Por eso es una característica vital para i2pd y uno de los hitos clave.

Por último, si estás familiarizado con I2P probablemente conozcas Bigbrother.i2p, que es un sistema de métricas que Meeh creó hace más de un año. Recientemente nos dimos cuenta de que Meeh en realidad tiene 100 GB de datos no duplicados de nodos que han estado informando desde el lanzamiento inicial. Esto también se trasladará a Privacy Solutions y se reescribirá con un backend NSPOF (sin punto único de fallo). Con esto también comenzaremos a usar Graphite (http://graphite.wikidot.com/screen-shots). Esto nos dará una excelente visión general de la red sin problemas de privacidad para nuestros usuarios finales. Los clientes filtran todos los datos excepto el país, el hash del router y la tasa de éxito en la construcción de tunnel. El nombre de este servicio es, como siempre, una pequeña broma de Meeh.

Hemos acortado un poco las noticias aquí, si te interesa más información visita https://blog.privacysolutions.no/ Aún estamos en construcción y pronto habrá más contenido!

Para más información, póngase en contacto con: press@privacysolutions.no

Saludos cordiales,

Mikal "Meeh" Villa
