---
title: "Notas de estado de I2P del 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Actualización semanal sobre la estabilidad de 0.6.1.4, la hoja de ruta de optimización del rendimiento, el lanzamiento de I2Phex 0.1.1.35, el desarrollo del cliente BT (BitTorrent) I2P-Rufus, los avances de I2PSnarkGUI y los rediseños de la interfaz de usuario de Syndie"
categories: ["status"]
---

Hola a todos, otra vez martes

* Index

1) Estado de la red / hoja de ruta a corto plazo 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

La 0.6.1.4 sigue pareciendo bastante sólida, aunque desde entonces ha habido algunas correcciones de errores en CVS. También he añadido algunas optimizaciones para SSU para transferir datos de manera más eficiente, lo que espero que tenga un impacto perceptible en la red una vez que se despliegue ampliamente. Sin embargo, por el momento estoy posponiendo la 0.6.1.5, ya que hay algunas otras cosas que quiero incluir en la próxima versión. El plan actual es publicarla este fin de semana, así que estén atentos a las últimas novedades.

La versión 0.6.2 incluirá muchas mejoras importantes para enfrentarse a adversarios aún más potentes, pero hay algo que no afectará: el rendimiento. Si bien el anonimato es sin duda la razón de ser de I2P, si el rendimiento y la latencia son deficientes, no tendremos usuarios. Por ello, mi plan es llevar el rendimiento al nivel que debe tener antes de pasar a implementar las estrategias de ordenación de pares de la 0.6.2 y las nuevas técnicas de creación de tunnel.

* 2) I2Phex

También ha habido mucha actividad últimamente en el frente de I2Phex, con una nueva versión 0.1.1.35 [1]. También ha habido más cambios en CVS (¡gracias, Legion!), así que no me sorprendería ver una 0.1.1.36 más adelante esta semana.

También ha habido buenos avances en el ámbito de gwebcache (ver http://awup.i2p/), aunque, que yo sepa, nadie ha empezado a trabajar en modificar I2Phex para usar un gwebcache compatible con I2P (¿te interesa? ¡avísame!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Se rumorea que defnax y Rawn han estado haciendo algunas modificaciones en el cliente Rufus BT, integrando algo de código relacionado con I2P de I2P-BT. No conozco el estado actual de la adaptación, pero parece que tendrá algunas funciones interesantes. Seguro que sabremos más cuando haya más que contar.

* 4) I2PSnarkGUI

Otro rumor que circula es que Markus ha estado haciendo algo de hacking en una nueva GUI en C#... las capturas de pantalla en PlanetPeer se ven bastante bien [2]. Todavía hay planes para una interfaz web independiente de la plataforma, pero esto se ve bastante bien. Estoy seguro de que sabremos más de Markus a medida que la GUI progrese.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

También ha habido algo de debate en torno a los rediseños de la interfaz de usuario (UI) de Syndie [3], y espero que veamos algunos avances en ese frente en breve. dust también está trabajando intensamente en Sucker, añadiendo mejor soporte para incorporar más canales RSS/Atom en Syndie, así como algunas mejoras al propio SML.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Muchísimas cosas en marcha, como siempre. Pásate por #i2p en unos minutos para nuestra reunión semanal de desarrollo.

=jr
