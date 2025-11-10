---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Rechazado"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Resumen

Esta propuesta trata sobre un nuevo formato de LeaseSet con soporte para los tipos de cifrado más recientes.

## Motivación

La criptografía de extremo a extremo utilizada a través de túneles I2P tiene claves de cifrado y firma separadas. Las claves de firma están en el destino del túnel, que ya se ha ampliado con certificados de clave para soportar tipos de firma más recientes. Sin embargo, las claves de cifrado son parte del LeaseSet, que no contiene ningún certificado. Por lo tanto, es necesario implementar un nuevo formato de LeaseSet y agregar soporte para almacenarlo en el netDb.

Un aspecto positivo es que una vez que LS2 esté implementado, todos los destinos existentes podrán usar tipos de cifrado más modernos; los routers que puedan obtener y leer un LS2 tendrán garantizado el soporte para cualquier tipo de cifrado introducido junto a él.

## Especificación

El formato básico de LS2 sería así:

- dest
- marca de tiempo publicada (8 bytes)
- expira (8 bytes)
- subtipo (1 byte) (regular, cifrado, meta o servicio)
- banderas (2 bytes)

- parte específica del subtipo:
  - tipo de cifrado, clave de cifrado y arrendamientos para regular
  - blob para cifrado
  - propiedades, hashes, puertos, revocaciones, etc. para servicio

- firma
