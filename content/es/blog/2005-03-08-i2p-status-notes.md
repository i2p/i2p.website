---
title: "Notas de estado de I2P del 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Notas semanales del estado del desarrollo de I2P que cubren las mejoras de la versión 0.5.0.2, el enfoque en la fiabilidad de la red y las actualizaciones de los servicios de correo y BitTorrent"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

* Index

1) 0.5.0.2 2) actualizaciones de mail.i2p 3) actualizaciones de i2p-bt 4) ???

* 1) 0.5.0.2

El otro día lanzamos la versión 0.5.0.2 y una buena parte de la red se ha actualizado (¡hurra!). Están llegando informes de que los peores problemas de la 0.5.0.1 han sido eliminados y, en general, todo parece funcionar bien. Aún hay algunos problemas de fiabilidad, aunque la streaming lib (biblioteca de streaming) los ha estado manejando (las conexiones de IRC que duran 12-24+ horas parecen ser la norma). He estado intentando localizar algunos de los problemas que quedan, pero sería realmente, realmente bueno que todos se actualizaran lo antes posible.

De cara al futuro, la fiabilidad es lo primero. Solo cuando una abrumadora mayoría de los mensajes que deberían tener éxito efectivamente lo tengan se trabajará en mejorar el rendimiento. Más allá del preprocesador por lotes de tunnel, otra dimensión que podríamos explorar es incorporar más datos de latencia en los perfiles. Actualmente solo usamos mensajes de prueba y de gestión de tunnel para determinar la clasificación de "speed" de cada par, pero probablemente deberíamos capturar cualquier RTT (tiempo de ida y vuelta) medible en otras acciones, como netDb e incluso mensajes de cliente de extremo a extremo. Por otro lado, habrá que ponderarlos en consecuencia, ya que en un mensaje de extremo a extremo no podemos separar las cuatro porciones del RTT medible (nuestra salida, su entrada, su salida, nuestra entrada). Quizá podamos hacer algún truco de garlic para empaquetar un mensaje dirigido a uno de nuestros tunnels entrantes junto con algunos mensajes salientes, excluyendo los tunnels del otro lado del bucle de medición.

* 2) mail.i2p updates

De acuerdo, no sé qué actualizaciones nos tiene preparadas postman, pero habrá una actualización durante la reunión. ¡Consulta los registros para averiguarlo!

* 3) i2p-bt update

No sé qué actualizaciones tienen duck y compañía para nosotros, pero he oído algunos rumores de avances en el canal. Quizá podamos sacarle una actualización.

* 4) ???

Hay muchísimo en marcha, pero si hay algo en particular que quieran plantear y debatir, pásense por la reunión en unos minutos. Ah, y solo como recordatorio, si aún no han actualizado, háganlo lo antes posible (actualizar es ridículamente sencillo - descargar un archivo, hacer clic en un botón)

=jr
