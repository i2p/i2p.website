---
title: "LeaseSet Encriptado"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Rechazado"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Vista general

Esta propuesta trata sobre el rediseño del mecanismo para encriptar LeaseSets.


## Motivación

El LS encriptado actual es horrendo e inseguro. Puedo decirlo, lo diseñé e
implementé.

Razones:

- Encriptado con AES CBC
- Una sola clave AES para todos
- Las expiraciones de arrendamiento siguen expuestas
- La clave pública de encriptación sigue expuesta


## Diseño

### Objetivos

- Hacer que todo sea opaco
- Claves para cada destinatario


### Estrategia

Hacerlo como lo hace GPG/OpenPGP. Encriptar asimétricamente una clave simétrica para cada
destinatario. Los datos se deseencriptan con esa clave asimétrica. Ver por ejemplo [RFC-4880-S5.1]_
SI podemos encontrar un algoritmo que sea pequeño y rápido.

El truco es encontrar una encriptación asimétrica que sea pequeña y rápida. ElGamal con 514
bytes es un poco doloroso aquí. Podemos hacerlo mejor.

Ver por ejemplo http://security.stackexchange.com/questions/824...

Esto funciona para números pequeños de destinatarios (o en realidad, claves; aún puedes
distribuir claves a varias personas si lo deseas).


## Especificación

- Destino
- Marca de tiempo publicada
- Expiración
- Banderas
- Longitud de los datos
- Datos encriptados
- Firma

Los datos encriptados podrían estar precedidos por algún especificador de tipo de encriptación, o no.


## Referencias

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
