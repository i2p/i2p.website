---
title: "Notas de estado de I2P del 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Actualización semanal del estado de I2P que cubre la recuperación de la red, el progreso de las pruebas de la biblioteca de streaming, los planes para el próximo lanzamiento de la versión 0.4.2 y mejoras en la libreta de direcciones"
categories: ["status"]
---

Hola a todos, es hora de una actualización de estado

## Índice:


1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Estado de la red

Después de la racha de 2-3 días de la semana pasada en que las cosas estaban bastante congestionadas, la red ha vuelto a la normalidad (probablemente porque dejamos de hacer pruebas de estrés al puerto de BitTorrent ;). Desde entonces, la red ha sido bastante fiable: de hecho tenemos algunos routers que han estado en funcionamiento durante 30-40+ días, pero las conexiones de IRC todavía han tenido sus baches ocasionales. Por otro lado...

## 2) Biblioteca de streaming

Durante la última semana aproximadamente, hemos estado haciendo muchas más pruebas en vivo de la streaming lib (biblioteca de streaming) en la red y las cosas se han visto bastante bien. Duck configuró un tunnel con ella que la gente podía usar para acceder a su servidor IRC, y a lo largo de unos pocos días solo tuve dos desconexiones innecesarias (lo que nos ayudó a localizar algunos errores). También hemos tenido una instancia de i2ptunnel apuntando a un outproxy squid (proxy de salida) que la gente ha estado probando, y tanto el rendimiento, la latencia como la fiabilidad han mejorado mucho en comparación con la lib antigua, que probamos en paralelo.

En general, la biblioteca de streaming parece estar en un estado lo suficientemente bueno para una primera versión. Quedan algunas cosas todavía sin completar, pero es una mejora significativa sobre la biblioteca anterior, y tenemos que darte una razón para actualizar más adelante, ¿no? ;)

De hecho, solo para tentarte (o quizá inspirarte a que propongas algunas soluciones), las principales cosas que veo que se avecinan para el streaming lib (biblioteca de streaming) son: - algunos algoritmos para compartir información de congestión y de RTT (tiempo de ida y vuelta) entre flujos (¿por destino objetivo? ¿por destino de origen? ¿para todos los destinos locales?) - optimizaciones adicionales para flujos interactivos (en la implementación actual la mayor parte del enfoque está en flujos de gran volumen) - un uso más explícito de las funcionalidades del nuevo streaming lib en I2PTunnel, reduciendo la sobrecarga por tunnel. - limitación de ancho de banda a nivel de cliente (en una u otra dirección de un flujo, o en ambas, o posiblemente compartida entre múltiples flujos). Esto se sumaría a la limitación global de ancho de banda del router, por supuesto. - varios controles para que los destinos regulen cuántos flujos aceptan o crean (tenemos algo de código básico, pero en gran medida deshabilitado) - listas de control de acceso (permitiendo únicamente flujos hacia o desde ciertos otros destinos conocidos) - controles web y monitoreo del estado de los distintos flujos, así como la capacidad de cerrarlos explícitamente o limitarlos

Seguro que a ustedes se les ocurren otras cosas también, pero eso es solo una lista breve de cosas que me encantaría ver en la biblioteca de streaming, aunque no voy a retrasar la versión 0.4.2 por ello. Si alguien está interesado en alguna de ellas, por favor, avísenme.

## 3) 0.4.2

Entonces, si la biblioteca de streaming está en buena forma, ¿cuándo vamos a tener el lanzamiento? El plan actual es lanzarlo para finales de la semana, quizá incluso mañana mismo. Hay algunas otras cosas en marcha que quiero resolver primero y, por supuesto, hay que probarlas, bla, bla, bla.

El gran cambio en la versión 0.4.2 será, por supuesto, la nueva biblioteca de streaming. Desde la perspectiva de la API, es idéntica a la biblioteca anterior - I2PTunnel y los streams (flujos de datos) de SAM la usan automáticamente, pero a nivel de paquetes, *no* es retrocompatible. Esto nos deja con un dilema interesante - no hay nada dentro de I2P que nos obligue a convertir la 0.4.2 en una actualización obligatoria, sin embargo, las personas que no actualicen no podrán usar I2PTunnel - sin eepsites(I2P Sites), sin IRC, sin outproxy, sin correo electrónico. No quiero alejar a nuestros usuarios veteranos obligándolos a actualizar, pero tampoco quiero alienarlos haciendo que todo lo útil deje de funcionar ;)

Estoy abierto a que me convenzan en cualquier sentido - sería bastante fácil cambiar una sola línea de código para que la versión 0.4.2 no se comunique con las versiones anteriores, o podríamos dejarlo así y que la gente actualice cuando vaya al sitio web o al foro a quejarse de que todo está roto. ¿Qué opinan?

## 4) AddressBook.py 0.3.1

Ragnarok ha publicado una nueva versión de parche para su aplicación de libreta de direcciones - consulta `http://ragnarok.i2p/` para más información (¿o quizá pueda ponernos al día en la reunión?)

## 5) ???

Sé que hay mucha más actividad en marcha - con el puerto de BitTorrent, susimail, el nuevo servicio de hosting de slacker, entre otras cosas. ¿Alguien tiene algo más que tratar? Si es así, pasen por la reunión en ~30m en #i2p en los servidores de IRC habituales!

=jr
