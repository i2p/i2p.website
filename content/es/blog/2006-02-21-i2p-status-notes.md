---
title: "Notas de estado de I2P para 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Problemas de red con la versión 0.6.1.10, versión de seguimiento rápida 0.6.1.11, y preocupaciones de seguridad en IE"
categories: ["status"]
---

Hola a todos, ya es martes otra vez

* Index

1) Estado de la red 2) ???

* 1) Net status

La red ha pasado por algunos contratiempos con la versión 0.6.1.10, debido en parte a la incompatibilidad con versiones anteriores, pero también a errores inesperados. Ni la fiabilidad ni el tiempo de actividad en 0.6.1.10 fueron suficientes, así que en los últimos 5 días ha habido una avalancha de parches, culminando en la nueva versión 0.6.1.11 - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

La mayoría de los errores encontrados en 0.6.1.10 han estado presentes desde la versión 0.6 publicada en septiembre pasado, pero no eran fácilmente evidentes mientras había transportes alternativos a los que recurrir (TCP). Mi red de pruebas local simula fallos de paquetes, pero realmente no cubría el router churn (rotación de routers) y otros fallos persistentes de la red. La _PRE red de prueba también incluía un conjunto autoseleccionado de pares bastante fiables, así que hubo situaciones importantes que no se exploraron completamente antes del lanzamiento completo. Eso es un problema, obviamente, y la próxima vez nos aseguraremos de incluir una selección más amplia de escenarios.

* 2) ???

Hay muchas cosas en marcha en este momento, pero la nueva versión 0.6.1.11 pasó al primer lugar de la cola.  La red seguirá estando un poco inestable hasta que un gran número de personas esté al día, tras lo cual el trabajo seguirá avanzando.  Vale la pena mencionar que cervantes está investigando algún tipo de exploit de dominio de seguridad relacionado con IE, y aunque no estoy seguro de que esté listo para explicar los detalles, los resultados preliminares sugieren que es viable, así que quienes se preocupan por el anonimato deberían evitar IE mientras tanto (pero eso ya lo sabían de todos modos ;).  ¿Quizá cervantes pueda darnos un resumen en la reunión?

De todos modos, eso es todo lo que tengo que comentar por ahora - pásate por la reunión en unos minutos para saludar!

=jr
