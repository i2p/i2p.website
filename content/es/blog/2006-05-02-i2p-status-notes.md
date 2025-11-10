---
title: "Notas de estado de I2P del 2006-05-02"
date: 2006-05-02
author: "jr"
description: "Mejoras en la salud de la red en 0.6.1.17, progreso continuo del rediseño de Syndie y próximas optimizaciones del router"
categories: ["status"]
---

Hola a todos, vuelve a ser martes una vez más

* Index

1) Estado de la red 2) Estado de Syndie 3) ???

* 1) Net status

Tras otra semana con la 0.6.1.17, varias de las métricas principales de la salud de la red se mantienen en buen estado. Sin embargo, estamos viendo que algunos de los problemas restantes se están propagando hasta la capa de aplicación, concretamente el reciente aumento de reconexiones en los servidores de irc2p. Postman, cervantes, Complication y yo hemos estado analizando diversos aspectos del comportamiento de la red en lo que respecta al rendimiento visible para el usuario, y hemos localizado e implementado algunas mejoras (el CVS HEAD actual es 0.6.1.17-4). Aún estamos supervisando su comportamiento y experimentando con algunos retoques antes de publicarlo como 0.6.1.18, aunque probablemente falten solo unos pocos días.

* 2) Syndie status

As mentioned before, syndie is being massively revamped. When I say massively, I mean nearly completely redesigned and reimplemented ;) The framework is in place (including continual testing with gcj), and the first few pieces are coming together, but its still a while away from functional. Once its in a position where more hands can help move it forward (and, erm, *use it*), there'll be more information available, but right now the syndie revamp is basically the back burner item while working through the router improvements.

* 3) ???

Eso es básicamente todo lo que hay que informar por ahora; como siempre, si tienes algo que plantear, pásate por la reunión en unos minutos y di hola.

=jr
