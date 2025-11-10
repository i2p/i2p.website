---
title: "Mensaje de Restablecimiento para ElGamal/AES+SessionTags"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Abierto"
thread: "http://zzz.i2p/topics/2056"
---

## Visión General

Esta propuesta es para un mensaje I2NP que puede ser usado para restablecer las etiquetas de sesión entre dos destinos.

## Motivación

Imagina que un destino tiene un montón de etiquetas confirmadas con otro destino. Pero ese destino se reinició o perdió estas etiquetas de alguna otra manera. El primer destino sigue enviando mensajes con etiquetas y el segundo destino no puede descifrar. El segundo destino debería tener una forma de decirle al primer destino que restablezca (empiece desde cero) a través de un elemento de ajo adicional de la misma manera que envía el LeaseSet actualizado.

## Diseño

### Mensaje Propuesto

Este nuevo elemento debe contener el tipo de entrega "destino" con un nuevo mensaje I2NP llamado "Restablecimiento de etiquetas" y contener el hash de identificación del remitente. Debe incluir marca de tiempo y firma.

Puede ser enviado en cualquier momento si un destino no puede descifrar mensajes.

### Uso

Si reinicio mi router e intento conectar con otro destino, envío un elemento con mi nuevo LeaseSet, y enviaría un elemento adicional con este mensaje conteniendo mi dirección. Un destino remoto recibe este mensaje, elimina todas las etiquetas salientes hacia mí y comienza desde ElGamal.

Es un caso bastante común que un destino solo se comunique con un destino remoto. En caso de reinicio, debería enviar este mensaje a todos junto con el primer mensaje de streaming o datagrama.
