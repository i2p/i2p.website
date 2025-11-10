---
title: "Notas de estado de I2P del 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Actualización semanal del estado de I2P que aborda la degradación del rendimiento de la red, la planificación del lanzamiento de la versión 0.3.5, las necesidades de documentación y el progreso de Stasher DHT (tabla hash distribuida)"
categories: ["status"]
---

Bueno, chicos y chicas, ¡otra vez es martes!

## Índice:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Bueno, como ya se habrán dado cuenta, aunque el número de usuarios en la red se ha mantenido bastante estable, el rendimiento se ha degradado significativamente en los últimos días. La causa ha sido una serie de errores en el código de selección de pares y de entrega de mensajes, expuestos cuando hubo un ataque de denegación de servicio (DoS) menor la semana pasada. El resultado ha sido que, básicamente, los tunnels de todos han estado fallando de forma constante, lo que tiene un cierto efecto de bola de nieve. Así que no, no eres solo tú - la red ha estado horrenda para el resto de nosotros también ;)

Pero la buena noticia es que solucionamos los problemas bastante rápido, y han estado en CVS desde la semana pasada, pero la red seguirá funcionando mal para los usuarios hasta que salga la próxima versión. Dicho esto...

## 2) 0.3.5 y 0.4

Aunque la próxima versión incluirá todas las novedades que tenemos previstas para la 0.4 (nuevo instalador, nuevo estándar de interfaz web, nueva interfaz i2ptunnel, bandeja del sistema y servicio de Windows, mejoras en subprocesos, correcciones de errores, etc), la manera en que la última versión se degradó con el tiempo fue reveladora. Quiero que avancemos más lentamente con estas versiones, dándoles tiempo para desplegarse más ampliamente y para que los problemas se manifiesten. Aunque el simulador puede explorar lo básico, no tiene manera de simular los problemas naturales de la red que vemos en la red real (al menos, todavía no).

Por lo tanto, la próxima versión será la 0.3.5 - con suerte, el último lanzamiento 0.3.*, aunque quizá no, si surgen otros problemas. Al mirar atrás a cómo se comportó la red cuando estuve desconectado en junio, las cosas empezaron a degradarse tras unas dos semanas. En consecuencia, mi idea es posponer pasar al nivel de lanzamiento 0.4 hasta que podamos mantener un alto grado de fiabilidad durante al menos dos semanas. Eso no significa que no vayamos a trabajar mientras tanto, por supuesto.

De todos modos, como mencioné la semana pasada, hypercubus está trabajando sin descanso en el nuevo sistema de instalación, lidiando con que yo esté cambiando cosas y exigiendo soporte para sistemas estrafalarios. Deberíamos dejarlo todo ultimado en los próximos días para sacar una versión 0.3.5 en los próximos días.

## 3) documentación

Una de las cosas importantes que tenemos que hacer durante esa "ventana de pruebas" de dos semanas antes de 0.4 es documentar como locos. Lo que me pregunto es qué cosas consideran que le faltan a nuestra documentación - ¿qué preguntas tienen que necesitemos responder? Aunque me gustaría decir "ok, ahora, vayan y escriban esos documentos", soy realista, así que lo único que pido es que identifiquen de qué tratarían esos documentos.

Por ejemplo, uno de los documentos en los que estoy trabajando ahora es una revisión del modelo de amenazas, que ahora describiría como una serie de casos de uso que explican cómo I2P puede satisfacer las necesidades de distintas personas, incluyendo la funcionalidad, los atacantes que preocupan a esa persona y cómo se defiende.

Si consideras que tu pregunta no requiere un documento completo para abordarla, simplemente formúlala como una pregunta y podemos añadirla a las Preguntas frecuentes (FAQ).

## 4) actualización de stasher

Aum estuvo en el canal más temprano hoy con una actualización (mientras yo lo acribillaba a preguntas):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Así que, como puedes ver, muchísimos avances. Aunque las claves se validen por encima de la capa DHT, eso es buenísimo (en mi humilde opinión). ¡Vamos, aum!

## 5) ???

Ok, eso es todo lo que tengo que decir (lo cual es bueno, ya que la reunión empieza en unos momentos)... ¡Pásate y di lo que quieras!

=jr
