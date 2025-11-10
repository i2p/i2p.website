---
title: "Notas de estado de I2P del 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Actualización semanal que cubre las mejoras de la versión 0.6.0.3, el estado de la red Irc2P, el frontend web susibt para i2p-bt y la publicación segura con Syndie"
categories: ["status"]
---

Hola a todos, ya es hora de las notas de estado semanales otra vez

* Index

1) estado de 0.6.0.3 2) estado de IRC 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Como se mencionó el otro día [1], tenemos una nueva versión 0.6.0.3 disponible, lista para su disfrute. Es una gran mejora respecto a la versión 0.6.0.2 (no es raro obtener varios días sin desconexión en irc - yo he tenido tiempos de actividad de 5 días, interrumpidos por una actualización), pero hay algunas cosas que vale la pena señalar. Aun así, no siempre es así - las personas con conexiones de red lentas se encuentran con problemas, pero es un avance.

Ha surgido una pregunta (muy) común sobre el código de prueba de pares-"¿Por qué dice Status: Unknown?" Unknown (Desconocido) está *perfectamente bien* - NO es indicativo de un problema. Además, si ves que a veces alterna entre "OK" y "ERR-Reject", eso NO significa que esté bien: si alguna vez ves ERR-Reject, eso significa que es muy probable que tengas un problema de NAT o de firewall. Sé que es confuso, y más adelante habrá una versión con una visualización del estado más clara (y resolución automática, cuando sea posible), pero por ahora, no te sorprendas si te ignoro cuando digas "omg está roto!!!11 el estado es Unknown!" ;)

(La causa del exceso de valores de estado Unknown es que estamos ignorando las pruebas entre pares en las que "Charlie" [2] es alguien con quien ya tenemos una sesión SSU, ya que eso implica que podría atravesar nuestro NAT incluso si nuestro NAT está roto)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Como se mencionó arriba, los operadores de Irc2P han hecho un gran trabajo con su red, ya que la latencia ha bajado muchísimo y la fiabilidad ha subido muchísimo - no he visto un netsplit (separación de red en IRC) en días. También hay un nuevo servidor IRC allí, con lo cual tenemos 3 - irc.postman.i2p, irc.arcturus.i2p y irc.freshcoffee.i2p. ¿Quizás alguien del equipo de Irc2P pueda darnos una actualización sobre su progreso durante la reunión?

* 3) susibt

susi23 (conocida por susimail) ha vuelto con un par de herramientas relacionadas con bt (BitTorrent) - susibt [3] y un nuevo tracker bot (bot del rastreador) [4]. susibt es una aplicación web (trivialmente desplegable en tu instancia de jetty de i2p) para gestionar el funcionamiento de i2p-bt. Como dice su sitio:

SusiBT es una interfaz web para i2p-bt. Se integra en su router i2p y permite cargas y descargas automáticas, reanudar tras reiniciar y algunas funciones de gestión como la carga y descarga de archivos. Las versiones posteriores de la aplicación admitirán la creación y carga automáticas de archivos torrent.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

¿Puedo oír un "w00t"?

* 4) Syndie

Como se mencionó en la lista y en el canal, tenemos una nueva aplicación cliente para publicación en blogs segura y autenticada / distribución de contenido. Con Syndie, la pregunta de "¿tu eepsite(sitio I2P) está en línea?" desaparece, ya que puedes leer el contenido incluso cuando el sitio está caído, pero Syndie evita todos los problemas feos inherentes a las redes de distribución de contenidos al centrarse en el frontend (capa de presentación). De todos modos, sigue muy en desarrollo, pero si la gente quiere entrar y probarlo, hay un nodo público de Syndie en http://syndiemedia.i2p/ (también accesible en la web en http://66.111.51.110:8000/). No dudes en entrar y crear un blog, o, si te sientes aventurero, ¡publica algunos comentarios/sugerencias/preocupaciones! Por supuesto, se aceptan parches, pero también sugerencias de funcionalidades, así que dale con todo.

* 5) ???

Decir que hay mucho en marcha es quedarse un poco corto... además de lo anterior, estoy trabajando en algunas mejoras del control de congestión de SSU (-1 ya está en cvs), nuestro limitador de ancho de banda y la netDb (por la ocasional inaccesibilidad de sitios), además de depurar el problema de CPU reportado en el foro. Estoy seguro de que otros también están trabajando en cosas interesantes que contar, así que, con suerte, se pasarán por la reunión de esta noche para explayarse :)

¡En fin, nos vemos esta noche a las 20:00 GMT en #i2p en los servidores de siempre!

=jr
