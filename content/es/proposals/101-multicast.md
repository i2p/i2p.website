---
title: "Multicast"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Dead"
thread: "http://zzz.i2p/topics/172"
---

## Visión general

Idea básica: Envía una copia a través de tu túnel de salida, el punto final de salida distribuye a todas las puertas de entrada. Se excluye el cifrado de extremo a extremo.

## Diseño

- Nuevo tipo de mensaje de túnel de multidifusión (tipo de entrega = 0x03)
- Distribución de multidifusión del punto final de salida
- ¿Nuevo tipo de mensaje I2NP Multicast?
- Nuevo tipo de mensaje I2CP Multicast SendMessageMessage
- No cifrar router-router en OutNetMessageOneShotJob (¿ajo?)

Aplicación:

- ¿Proxy RTSP?

Streamr:

- ¿Ajustar MTU? ¿O simplemente hacerlo en la aplicación?
- Recepción y transmisión bajo demanda
