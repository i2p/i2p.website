---
title: "Notas de estado de I2P del 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Actualización semanal sobre el regreso del desarrollador tras un viaje, el progreso del transporte SSU, la finalización de la recompensa por pruebas unitarias y la interrupción del servicio"
categories: ["status"]
---

Hola a todos, es hora de retomar nuestras notas semanales de estado

* Index

1) Estado del Des[arrollador] 2) Estado del Des[arrollo] 3) Recompensa por pruebas unitarias 4) Interrupción del servicio 5) ???

* 1) Dev[eloper] status

Después de 4 ciudades en 4 países, por fin me estoy asentando y volviendo a avanzar con el código. La semana pasada terminé de reunir las últimas piezas para un portátil, ya no ando de sofá en sofá y, aunque no tengo acceso a internet en casa, hay muchos cibercafés por aquí, así que el acceso es fiable (solo que poco frecuente y caro).

Ese último punto significa que no estaré pasando tanto tiempo en irc como antes, al menos hasta el otoño (tengo un subarriendo hasta agosto o así y estaré buscando un sitio donde pueda tener acceso a Internet 24/7). Eso no significa, sin embargo, que vaya a hacer menos - simplemente estaré trabajando en gran medida en mi propia red de pruebas, sacando compilaciones para pruebas en la red en producción (y, eh, ah sí, lanzamientos). Sí significa, eso sí, que quizá queramos trasladar algunas discusiones que antes se daban de forma libre en #i2p a la lista [1] y/o al foro [2] (aunque sigo leyendo el historial de #i2p). Aún no he encontrado un lugar razonable al que pueda ir para nuestras reuniones de desarrollo, así que no asistiré esta semana, pero quizá para la próxima semana ya haya encontrado uno.

En fin, basta de hablar de mí.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Mientras me he estado mudando, he estado trabajando en dos frentes principales: la documentación y el transporte SSU (esta última solo desde que conseguí el portátil). La documentación aún está en progreso, con un gran y algo intimidante documento de visión general, así como una serie de documentos de implementación más pequeños (que cubren cosas como la estructura del código fuente, la interacción entre componentes, etc.).

El progreso de SSU va bien - los nuevos campos de bits de ACK están en su lugar, la comunicación está gestionando la pérdida (simulada) de forma eficaz, las tasas son apropiadas para las distintas condiciones y he solucionado algunos de los errores más feos con los que me había encontrado anteriormente. Sigo probando estos cambios y, cuando sea apropiado, planificaremos una serie de pruebas en la red en producción para las que necesitaremos algunos voluntarios que nos ayuden. Más noticias al respecto cuando estén disponibles.

* 3) Unit test bounty

¡Me complace anunciar que Comwiz se ha presentado con una serie de parches para reclamar la primera fase de la recompensa por pruebas unitarias [3]! Todavía estamos trabajando en algunos detalles menores de los parches, pero ya he recibido las actualizaciones y generado los informes de junit y clover según sea necesario. Espero que en breve tengamos los parches en CVS, momento en el que publicaremos la documentación de pruebas de Comwiz.

Como clover es un producto comercial (gratuito para desarrolladores [4] de software de código abierto (OSS)), solo quienes hayan instalado clover y recibido su licencia de clover podrán generar los informes de clover. En cualquier caso, publicaremos periódicamente en la web los informes de clover, para que quienes no tengan clover instalado aún puedan ver lo bien que está funcionando nuestra suite de pruebas.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Como muchos habrán notado, (al menos) uno de los outproxies (proxies de salida) está fuera de línea (squid.i2p), al igual que www.i2p, dev.i2p, cvs.i2p y mi blog. No son eventos inconexos - la máquina que los aloja está averiada.

=jr
