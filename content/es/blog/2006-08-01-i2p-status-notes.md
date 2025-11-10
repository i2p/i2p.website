---
title: "Notas de estado de I2P del 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Rendimiento de red sólido con altas tasas de transferencia de I2PSnark, estabilidad del transporte NTCP y aclaraciones sobre la accesibilidad de eepsite"
categories: ["status"]
---

Hola a todos, es momento de unas breves notas antes de la reunión de esta noche. Me doy cuenta de que pueden tener una variedad de preguntas o asuntos que plantear, así que optaremos por un formato más fluido de lo habitual. Solo hay algunas cosas que quiero mencionar primero.

* Network status

Parece que la red va bastante bien, con enjambres de transferencias de I2PSnark bastante grandes que se completan y con tasas de transferencia bastante sustanciales alcanzadas en routers individuales - He visto 650KBytes/sec y 17,000 tunnels participantes sin sobresaltos. Los routers de gama baja también parecen estar funcionando bien, navegando eepsites(I2P Sites) e irc con tunnels de 2 saltos utilizando menos de 1KByte/sec en promedio.

No todo es color de rosa para todos, pero estamos trabajando en actualizar el comportamiento del router para permitir un rendimiento más consistente y utilizable.

* NTCP

El nuevo transporte NTCP ("nuevo" tcp) está funcionando bastante bien después de resolver los problemas iniciales. Para responder a una pregunta frecuente, a largo plazo, tanto NTCP como SSU estarán en funcionamiento - no vamos a volver a usar solo TCP.

* eepsite(I2P Site) reachability

Recuerden que las eepsites(sitios de I2P) solo son accesibles cuando la persona que las ejecuta las tiene en línea - si están caídas, no hay nada que puedan hacer para acceder a ellas ;) Lamentablemente, en los últimos días, orion.i2p no ha estado accesible, pero la red sin duda sigue funcionando - quizá pásense por inproxy.tino.i2p o eepsites(I2P Sites).i2p para sus necesidades de sondeo de la red.

De todos modos, hay muchas más cosas en marcha, pero sería un poco prematuro mencionarlas aquí. Por supuesto, si tienes alguna pregunta o inquietud, pásate por #i2p en unos minutos para nuestra *ejem* reunión semanal de desarrollo.

¡Gracias por ayudar a que avancemos! =jr
