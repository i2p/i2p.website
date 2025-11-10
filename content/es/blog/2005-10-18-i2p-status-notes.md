---
title: "Notas de estado de I2P del 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Actualización semanal que cubre el éxito del lanzamiento 0.6.1.3, la discusión de colaboración con Freenet, el análisis de ataques de bootstrap contra tunnel, los avances sobre el error de subida de I2Phex y la recompensa por NAT simétrico."
categories: ["status"]
---

Hola a todos, es martes otra vez

* Index

1) 0.6.1.3
2) Freenet, I2P y redes oscuras (¡vaya!)
3) Ataques de arranque de Tunnel
4) I2Phex
5) Syndie/Sucker
6) ??? [recompensa de 500+ por NAT simétrico]

* 1) 0.6.1.3

El viernes pasado publicamos una nueva versión 0.6.1.3, y con el 70% de la red actualizado, los informes han sido muy positivos. Las nuevas mejoras de SSU parecen haber reducido las retransmisiones innecesarias, permitiendo un rendimiento más eficiente a velocidades más altas, y hasta donde sé no ha habido problemas importantes con el proxy de IRC ni con las mejoras de Syndie.

Cabe destacar que Eol ha ofrecido una recompensa en rentacoder[1] por soporte de NAT simétrico, ¡así que ojalá logremos avances en ese frente!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Por fin hemos cerrado ese hilo de más de 100 mensajes con una visión más clara de las dos redes, dónde encajan y qué margen tenemos para seguir colaborando. No voy a entrar aquí en qué topologías o modelos de amenaza les resultan más adecuados, pero puedes profundizar en las listas si quieres saber más. En cuanto a la colaboración, le envié a toad algo de código de ejemplo para reutilizar nuestro transporte SSU, lo cual puede ser útil para la gente de Freenet a corto plazo, y más adelante quizá trabajemos juntos para ofrecer premix routing (enrutamiento de premezcla) a los usuarios de Freenet en entornos donde I2P sea viable. A medida que Freenet avance, quizá podamos hacer que Freenet funcione también sobre I2P como una aplicación cliente, permitiendo la distribución automática de contenido entre los usuarios que lo ejecuten (p. ej., haciendo circular archivos y publicaciones de Syndie), pero primero veremos cómo funcionan los sistemas previstos de Freenet para carga y distribución de contenido.

* 3) Tunnel bootstrap attacks

Michael Rogers se puso en contacto en relación con algunos ataques nuevos e interesantes contra la creación de tunnels en I2P [2][3][4]. El ataque principal (llevar a cabo con éxito un ataque de predecesor durante todo el bootstrap process (proceso de arranque)) es interesante, pero no realmente práctico - la probabilidad de éxito es (c/n)^t, con c atacantes, n pares en la red y t tunnels construidos por el objetivo (a lo largo de su vida útil) - menor que la probabilidad de que un adversario se apodere de todos los h saltos en un tunnel (P(success) = (c/n)^h) después de que el router haya construido h tunnels.

Michael ha publicado otro ataque en la lista que estamos analizando en este momento, así que podrás seguirlo allí también.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker está logrando más avances con el error de subida, y los informes indican que ya lo tiene localizado. Con suerte, entrará en CVS esta noche, y poco después se publicará como 0.1.1.33. Estén atentos al foro [5] para más información.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Corre el rumor de que redzara también está avanzando bastante bien para volver a fusionarse con la rama principal de Phex, así que, con suerte, con la ayuda de Gregor, pondremos todo al día pronto.

* 5) Syndie/Sucker

dust ha estado trabajando intensamente con Sucker también, con código que incorpora más datos RSS/Atom en Syndie. Quizás podamos lograr que Sucker y la CLI de publicación se integren aún más en Syndie, quizá incluso con una interfaz web para programar importaciones de diferentes fuentes RSS/Atom en varios blogs. Ya veremos...

* 6) ???

Hay mucho más sucediendo además de lo anterior, pero ese es, a grandes rasgos, lo principal de lo que estoy al tanto. Si alguien tiene preguntas/inquietudes, o quiere plantear otras cosas, acérquense a la reunión esta noche a las 8PM UTC en #i2p!

=jr
