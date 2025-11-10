---
title: "Notas de estado de I2P del 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren el estado de la red, el progreso de la versión 0.5, el estado de la versión 0.6, azneti2p, el port para FreeBSD y hosts.txt como Red de Confianza"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) Estado de la red 2) progreso 0.5 3) estado 0.6 4) azneti2p 5) fbsd 6) hosts.txt como WoT (red de confianza) 7) ???

* 1) Net status

En general, la red se está comportando bien, aunque tuvimos algunos problemas con uno de los servidores IRC fuera de línea y con mi outproxy (proxy de salida) fallando. Sin embargo, el otro servidor IRC estaba (y aún está) disponible (aunque por el momento no tiene CTCP deshabilitado - véase [1]), así que pudimos saciar nuestra necesidad de IRC :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Hay progreso, ¡siempre hacia adelante! Vale, supongo que debería entrar en un poco más de detalle que eso. Por fin tengo implementada y probada la nueva criptografía de enrutamiento del tunnel (¡bien!), pero durante algunas discusiones encontramos un lugar donde podría haber un nivel de fuga de anonimato, así que se está revisando (el primer salto habría sabido que era el primer salto, lo cual es Malo. pero realmente muy fácil de arreglar). De todos modos, espero tener la documentación y el código sobre eso actualizados y publicados pronto, y la documentación sobre el resto de la operación/agrupación/etc del tunnel 0.5 publicada más tarde. Más noticias cuando haya más noticias.

* 3) 0.6 status

(¡¿qué!?)

Mule ha empezado a investigar el transporte UDP, y hemos estado consultando a zab para aprovechar su experiencia con el código UDP de LimeWire. Todo es muy prometedor, pero queda mucho trabajo por hacer (y aún faltan varios meses en la hoja de ruta [2]).  ¿Tienes alguna idea o sugerencia?  ¡Participa y ayuda a orientarlo hacia lo que hay que hacer!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Casi me caigo de la silla cuando me llegó la info, pero parece que los de Azureus han escrito un plugin para I2P que permite tanto el uso anónimo de trackers como la comunicación de datos anónima. También funcionan varios torrents dentro de un único I2P destination (destino de I2P), y usa directamente el I2PSocket, lo que permite una integración estrecha con la biblioteca de streaming. El plugin azneti2p aún está en una fase temprana con esta versión 0.1, y hay muchas optimizaciones y mejoras de facilidad de uso en camino, pero si te apetece ensuciarte las manos, pásate por i2p-bt en las redes IRC de I2P y súmate a la diversión :)

Para los de espíritu aventurero, obtén la última versión de azureus [3], consulta su guía de I2P [4] y consigue el plugin [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck ha estado adoptando medidas heroicas para mantener la compatibilidad con i2p-bt, y hay actividad de hacking frenética en #i2p-bt mientras escribo esto, así que estén atentos a una nueva versión de i2p-bt muy pronto.

* 5) fbsd

Gracias al trabajo de lioux, ahora hay una entrada en los ports de FreeBSD para i2p [6]. Aunque realmente no buscamos tener muchas instalaciones específicas de distribuciones disponibles, él promete mantenerla actualizada cuando le demos suficiente aviso previo de un nuevo lanzamiento. Esto debería ser útil para la gente de fbsd-current - ¡gracias, lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Ahora que la versión 0.4.2.6 ha incluido el addressbook (libreta de direcciones) de Ragnarok, el proceso de mantener tu hosts.txt actualizado con nuevas entradas está en tus manos.  No solo eso, sino que puedes considerar las suscripciones del addressbook como una web de confianza rudimentaria: importas nuevas entradas desde un sitio en el que confías para que te presente nuevos destinos (cuyos valores predeterminados son dev.i2p y duck.i2p).

Con esta capacidad llega toda una nueva dimensión: la posibilidad de que las personas elijan a qué sitios, en esencia, enlazar en su hosts.txt y a cuáles no. Si bien hay espacio para el libre para todos público que se ha dado en el pasado, ahora que el sistema de nombres no solo es teoría sino que, en la práctica, está completamente distribuido, la gente tendrá que definir sus propias políticas sobre la publicación de los destinos de otras personas.

La parte importante entre bastidores aquí es que esto es una oportunidad de aprendizaje para la comunidad de I2P. Antes, tanto gott como yo intentábamos ayudar a impulsar el problema del sistema de nombres publicando el sitio de gott como jrandom.i2p (él pidió ese sitio primero - yo no, y no tengo ningún control en absoluto sobre el contenido de esa URL). Ahora podemos comenzar a explorar cómo vamos a tratar con sitios que no están listados en http://dev.i2p.net/i2p/hosts.txt o en forum.i2p. No estar publicado en esos lugares no impide de ninguna manera que un sitio funcione: tu hosts.txt es simplemente tu libreta de direcciones local.

En fin, basta de divagar, solo quería poner a la gente al tanto para que todos podamos ver qué hay que hacer.

* 7) ???

¡Vaya, eso es un montón de cosas! Semana ocupada, y no preveo que las cosas se calmen pronto. Así que pásate por la reunión en unos minutos y podemos hablar de ello.

=jr
