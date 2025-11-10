---
title: "Notas de estado de I2P del 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Desafíos de fiabilidad de la red, próxima versión 0.6.1.10 con nuevo cifrado para la creación de tunnel, y cambios incompatibles con versiones anteriores"
categories: ["status"]
---

Hola a todos, ya es martes otra vez,

* Index

1) Estado de la red 2) Estado de 0.6.1.10 3) ???

* 1) Net status

Durante la última semana, he estado probando unos cuantos ajustes diferentes para aumentar la fiabilidad de la creación de tunnels en la red en producción, pero aún no ha habido un avance decisivo. Sin embargo, ha habido algunos cambios sustanciales en CVS, pero no son lo que yo llamaría... estables. Así que, en general, recomendaría que la gente use la versión más reciente (0.6.1.9, etiquetada en CVS como i2p_0_6_1_9), o tunnels de no más de 1 salto con las últimas compilaciones. Por otro lado...

* 2) 0.6.1.10 status

En lugar de batallar indefinidamente con pequeños ajustes, he estado trabajando en mi red de pruebas local para migrar al nuevo esquema criptográfico y proceso de creación de tunnel (túnel de I2P) [1]. Esto debería reducir en gran medida la tasa de fallos en la creación de tunnel, tras lo cual podremos ajustarlo más, si es necesario.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Una consecuencia desafortunada es que la versión 0.6.1.10 no será compatible con versiones anteriores.  Hace mucho que no tenemos una versión incompatible con versiones anteriores, pero en los primeros tiempos lo hicimos varias veces, así que no debería ser un gran problema.  Básicamente, después de que funcione de maravilla en mi red de pruebas local, la desplegaremos en paralelo a unos cuantos valientes para pruebas iniciales; luego, cuando esté lista para el lanzamiento, simplemente cambiaremos las referencias de nodos semilla para que apunten a los nodos semilla de la nueva red y la publicaremos.

No tengo una fecha estimada para la versión 0.6.1.10, pero por el momento se ve bastante bien (la mayoría de las longitudes de tunnel están saliendo bien, pero hay algunas ramas que aún no he sometido a pruebas de estrés).  Más noticias cuando las haya, por supuesto.

* 3) ???

Eso es más o menos todo lo que tengo que mencionar por el momento, aunque sé que hay cosas en las que otros están hackeando y yo tengo algunos trucos bajo la manga para más adelante, pero ya sabremos más cuando sea el momento adecuado. En fin, ¡nos vemos en unos minutos!

=jr
