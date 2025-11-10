---
title: "Notas de estado de I2P del 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Actualización semanal del estado de I2P que abarca la estabilidad de la red, el desarrollo de la biblioteca de streaming, los avances en mail.i2p y los avances en BitTorrent"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

## Índice

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Estado de la red

No quiero tentar a la suerte, pero durante la última semana la red ha estado prácticamente como antes - bastante estable para irc, con los eepsites(I2P Sites) cargando de forma fiable, aunque los archivos grandes todavía suelen requerir reanudar la descarga. Básicamente, nada nuevo que informar, más allá del hecho de que no hay nada nuevo que informar.

Oh, una cosa que encontramos fue que aunque Jetty admite la reanudación de HTTP, solo lo hace para HTTP 1.1. Eso está bien para la mayoría de los navegadores y herramientas de descarga, *excepto* wget: wget envía la solicitud de reanudación como HTTP 1.0. Así que, para descargar archivos grandes, usa curl u otra herramienta con capacidad de reanudación HTTP 1.1 (¡gracias a duck y ardvark por investigar y encontrar una solución!).

## 2) Streaming lib (biblioteca de streaming)

Dado que la red ha estado bastante estable, he dedicado casi todo mi tiempo a trabajar en la nueva biblioteca de streaming. Aunque aún no está terminada, ha habido mucho progreso - los escenarios básicos funcionan bien, las ventanas deslizantes están funcionando bien para el self-clocking (autorregulación del ritmo), y la nueva biblioteca funciona como un reemplazo directo de la anterior, desde la perspectiva del cliente (aunque las dos bibliotecas de streaming no pueden comunicarse entre sí).

En los últimos días he estado trabajando en algunos escenarios más interesantes. El más importante es la red con alta latencia, que simulamos inyectando retrasos en los mensajes recibidos, ya sea un retraso aleatorio simple de 0-30s o un retraso escalonado (el 80% del tiempo hay una latencia de 0-10s, 10% @ 10-20s de latencia, 5% @ 20-30s, 3% @ 30-40s, 4% @ 40-50s). Otra prueba importante ha sido el descarte aleatorio de mensajes - esto no debería ser común en I2P, pero deberíamos ser capaces de manejarlo.

El rendimiento general ha sido bastante bueno, pero todavía queda mucho trabajo por hacer antes de poder desplegar esto en la red en producción. Esta actualización será 'peligrosa' en el sentido de que es tremendamente poderosa - si se hace terriblemente mal, podemos provocarnos un DDoS en un abrir y cerrar de ojos, pero si se hace bien, bueno, baste decir que hay mucho potencial (prometer menos y cumplir más).

Así que, dicho esto, y como la red está bastante en 'estado estable', no tengo prisa por lanzar algo que no esté suficientemente probado. Más novedades cuando haya más novedades.

## 3) progreso de mail.i2p

postman y su equipo han estado trabajando duro para el correo electrónico en i2p (véase www.postman.i2p), y hay novedades interesantes en camino - ¿quizás postman tenga alguna actualización para nosotros?

Como comentario aparte, entiendo y me identifico con las solicitudes de una interfaz de correo web, pero postman está desbordado trabajando en cosas interesantes en el back-end del sistema de correo. Sin embargo, una alternativa es instalar una interfaz de correo web *localmente* en tu propio servidor web - existen soluciones de webmail basadas en JSP/servlet. Eso te permitiría ejecutar tu propia interfaz de correo web local en, por ejemplo, `http://localhost:7657/mail/`

Sé que hay algunos scripts de código abierto por ahí para acceder a cuentas POP3, lo cual nos deja a mitad de camino - ¿quizá alguien podría buscar alguno que admita POP3 y SMTP autenticado? ¡Vamos, sabes que quieres!

## 4) ???

Ok, eso es todo lo que tengo que decir por ahora - pásate por la reunión en unos minutos y dinos qué está pasando.

=jr
