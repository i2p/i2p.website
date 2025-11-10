---
title: "Notas de estado de I2P del 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren los errores de la 0.5.0.1 y la próxima 0.5.0.2, actualizaciones de la hoja de ruta, el editor de la libreta de direcciones y actualizaciones de i2p-bt"
categories: ["status"]
---

Hola a todos, es hora de nuestra actualización de estado

* Index

1) 0.5.0.1 2) hoja de ruta 3) editor y configuración de la libreta de direcciones 4) i2p-bt 5) ???

* 1) 0.5.0.1

Como se comentó la semana pasada, pocas horas después de la reunión publicamos una nueva versión 0.5.0.1 que corrige los errores de la 0.5 que habían provocado el enorme número de tunnels que se estaban creando (entre otras cosas). En general, esta revisión ha mejorado las cosas, pero con pruebas más amplias nos hemos topado con algunos errores adicionales que han estado afectando a algunas personas. En particular, la revisión 0.5.0.1 puede devorar muchísima CPU si tienes una máquina lenta o si los tunnels de tu router fallan en masa, y algunos servidores I2PTunnel de larga duración pueden devorar RAM hasta provocar un OOM (se queda sin memoria). También hay un error de larga data en la biblioteca de streaming, por el que podemos no llegar a establecer una conexión si se producen exactamente los fallos adecuados.

La mayoría de estos (entre otros) se han corregido en cvs, pero algunos siguen pendientes.  Una vez que estén todos corregidos, lo empaquetaremos y lo lanzaremos como la versión 0.5.0.2.  No estoy del todo seguro de cuándo será; con suerte, esta semana, pero ya veremos.

* 2) roadmap

Después de los lanzamientos mayores, la hoja de ruta [1] parece que se... ajusta.  La versión 0.5 no fue diferente.  Esa página refleja lo que considero razonable y apropiado para el camino a seguir, pero, por supuesto, si más personas se suman a ayudar con las tareas, sin duda puede ajustarse.  Notarás la pausa significativa entre la 0.6 y la 0.6.1 y, si bien esto sí refleja mucho trabajo, también refleja el hecho de que me voy a mudar (es esa época del año otra vez).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate ha comenzado a trabajar en una interfaz web para gestionar las entradas del libro de direcciones (hosts.txt), y parece bastante prometedora. ¿Quizá podamos recibir una actualización de detonate durante la reunión?

Además, smeghead ha estado trabajando en una interfaz web para administrar la configuración de la libreta de direcciones (subscriptions.txt, config.txt).  ¿Quizás podamos obtener una actualización de smeghead durante la reunión?

* 4) i2p-bt

Ha habido algunos avances en el frente de i2p-bt, con una nueva versión 0.1.8 que aborda los problemas de compatibilidad de azneti2p, como se discutió en la reunión de la semana pasada. ¿Quizás podamos obtener una actualización de duck o smeghead durante la reunión?

Legion también ha creado un fork (bifurcación) de i2p-bt rev, ha incorporado algo de otro código, ha parcheado algunas cosas y tiene un binario para Windows disponible en su eepsite(sitio de I2P).  El anuncio [2] parece sugerir que el código fuente podría ponerse a disposición, aunque no está publicado en el eepsite(sitio de I2P) por el momento.  Los desarrolladores de I2P no han auditado (ni siquiera visto) el código de ese cliente, así que quienes necesiten anonimato quizá quieran obtener y revisar primero una copia del código.

[2] http://forum.i2p.net/viewtopic.php?t=382

También hay trabajo en una versión 2 del cliente de BitTorrent de Legion, aunque no sé en qué estado se encuentra.  ¿Quizá podamos obtener una actualización de Legion durante la reunión?

* 5) ???

Eso es prácticamente todo lo que tengo que decir por ahora; hay muchísimas cosas en marcha. ¿Alguien más está trabajando en algo sobre lo que quizá podamos obtener una actualización durante la reunión?

=jr
