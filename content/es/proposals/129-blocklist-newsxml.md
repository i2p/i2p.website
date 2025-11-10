---
title: "Lista de bloqueos en el feed de noticias"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Descripción general

Esta propuesta es para distribuir actualizaciones de la lista de bloqueos en el archivo de noticias,
que se distribuye en formato su3 firmado.
Implementado en 0.9.28.

## Motivación

Sin esto, la lista de bloqueos solo se actualiza en la versión.
Utiliza la suscripción de noticias existente.
Este formato podría ser utilizado en varias implementaciones de router, pero sólo el router Java
utiliza la suscripción de noticias actualmente.

## Diseño

Agregar una nueva sección al archivo news.xml.
Permitir el bloqueo por dirección IP o hash del router.
La sección tendrá su propio sello de tiempo.
Permitir el desbloqueo de entradas previamente bloqueadas.

Incluir una firma de la sección, que será especificada.
La firma cubrirá el sello de tiempo.
La firma debe verificarse al importar.
El firmante será especificado y puede ser diferente del firmante su3.
Los routers pueden usar una lista de confianza diferente para la lista de bloqueos.

## Especificación

Ahora en la página de especificación de actualización del router.

Las entradas son ya sea una dirección literal IPv4 o IPv6, 
o un hash de router codificado en base64 de 44 caracteres.
Las direcciones IPv6 pueden estar en formato abreviado (contienen "::").
El soporte para bloqueo con una máscara de red, por ejemplo, x.y.0.0/16, es opcional.
El soporte para nombres de host es opcional.

## Migración

Los routers que no soporten esto ignorarán la nueva sección XML.

## Ver también

Propuesta 130
