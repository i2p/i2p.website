---
title: "Notas de estado de I2P del 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que abarcan el análisis del rendimiento de la red, mejoras en el cálculo de la velocidad y el desarrollo de Feedspace"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) Estado de la red 2) Feedspace 3) ???

* 1) Net status

Durante la última semana, gran parte de mi tiempo se ha dedicado a analizar el comportamiento de la red, seguir estadísticas e intentar reproducir varios eventos en el simulador.  Aunque parte del comportamiento de red extraño puede atribuirse a las unas dos docenas de routers que aún están en versiones anteriores, el factor clave es que nuestros cálculos de velocidad no nos están dando buenos datos: no podemos identificar adecuadamente a los pares que pueden transferir datos rápidamente.  En el pasado, esto no era un gran problema, ya que había un error que nos hacía usar a los 8 pares de mayor capacidad como el grupo 'fast', en lugar de construir niveles legítimos derivados de la capacidad.  Nuestro cálculo de velocidad actual se deriva de una prueba periódica de latencia (el RTT (tiempo de ida y vuelta) de una prueba de tunnel, en particular), pero eso proporciona datos insuficientes como para tener confianza en el valor.  Lo que necesitamos es una mejor manera de recopilar más puntos de datos y, al mismo tiempo, permitir que los pares de 'alta capacidad' sean ascendidos al nivel 'fast', según sea necesario.

Para verificar que este es el problema clave al que nos enfrentamos, hice un poco de trampa y añadí funcionalidad para seleccionar manualmente qué pares deberían usarse en la selección de un determinado tunnel pool (grupo de túneles). Con esos pares elegidos explícitamente, llevo más de dos días en IRC sin desconexiones y un rendimiento bastante razonable con otro servicio que controlo. Durante los últimos dos días aproximadamente, he estado probando un nuevo calculador de velocidad usando algunas estadísticas nuevas, y aunque ha mejorado la selección, todavía tiene algunos problemas. He trabajado en algunas alternativas esta tarde, pero aún queda trabajo por hacer para probarlas en la red.

* 2) Feedspace

Frosk ha publicado otra revisión de la documentación de i2pcontent/fusenet, aunque ahora está en una nueva ubicación y con un nombre nuevo: http://feedspace.i2p/ - consulta orion [1] o mi blog [2] para la Destination (dirección/identidad en I2P).  Esto pinta realmente prometedor, tanto desde la perspectiva de "hey, funcionalidad impresionante" como de "hey, eso ayudará al anonimato de I2P".  Frosk y su equipo siguen trabajando duro, pero sin duda están buscando aportaciones (y ayuda).  ¿Quizá podamos conseguir que Frosk nos ponga al día en la reunión?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

Vale, puede que no parezca gran cosa, pero hay mucho en marcha, de verdad :) Estoy seguro de que también se me han pasado algunas cosas, así que pásate por la reunión y a ver qué se cuece.

=jr
