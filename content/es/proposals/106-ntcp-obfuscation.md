---
title: "Ofuscación de NTCP"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Rechazado"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Resumen

Esta propuesta trata sobre la renovación del transporte NTCP para mejorar su resistencia a la identificación automatizada.

## Motivación

Los datos de NTCP están encriptados después del primer mensaje (y el primer mensaje parece ser datos aleatorios), lo que evita la identificación del protocolo a través del "análisis de carga útil". Aún es vulnerable a la identificación del protocolo mediante "análisis de flujo". Esto es porque los primeros 4 mensajes (es decir, el apretón de manos) tienen una longitud fija (288, 304, 448 y 48 bytes).

Al agregar cantidades aleatorias de datos aleatorios a cada uno de los mensajes, podemos hacerlo mucho más difícil.

## Modificaciones a NTCP

Esto es bastante complejo pero previene cualquier detección por equipos DPI.

Los siguientes datos se agregarán al final del mensaje de 288 bytes 1:

- Un bloque cifrado ElGamal de 514 bytes
- Relleno aleatorio

El bloque ElG está cifrado con la clave pública de Bob. Cuando se descifra a 222 bytes, contiene:
- 214 bytes de relleno aleatorio
- 4 bytes 0 reservados
- 2 bytes de longitud de relleno a seguir
- 2 bytes de versión del protocolo y banderas

En los mensajes 2-4, los últimos dos bytes del relleno ahora indicarán la longitud de más relleno a seguir.

Tenga en cuenta que el bloque ElG no tiene secreto hacia adelante perfecto, pero no hay nada interesante allí.

¿Podríamos modificar nuestra biblioteca ElG para que cifre tamaños de datos más pequeños si pensamos que 514 bytes es demasiado? ¿Es el cifrado ElG para cada configuración de NTCP demasiado?

El soporte para esto se anunciaría en el netdb RouterAddress con la opción "version=2". Si solo se reciben 288 bytes en el Mensaje 1, se asume que Alice es la versión 1 y no se envía relleno en los mensajes siguientes. Tenga en cuenta que la comunicación podría bloquearse si un MITM fragmentara el IP a 288 bytes (muy poco probable según Brandon).
