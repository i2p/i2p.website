---
title: "Lista de bloqueo en formato SU3"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Abierto"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Visión general

Esta propuesta es para distribuir actualizaciones de la lista de bloqueo en un archivo su3 separado.


## Motivación

Sin esto, la lista de bloqueo solo se actualiza en la versión de lanzamiento. Este formato podría ser utilizado en varias implementaciones de routers.


## Diseño

Definir el formato para ser encapsulado en un archivo su3. Permitir el bloqueo por IP o por hash del router. Los routers pueden suscribirse a una URL o importar un archivo obtenido por otros medios. El archivo su3 contiene una firma que debe ser verificada al importar.


## Especificación

Por añadir a la página de especificación de actualización del router.

Definir nuevo tipo de contenido LISTA_DE_BLOQUEO (5). Definir nuevo tipo de archivo TXT_GZ (4) (formato .txt.gz). Las entradas son una por línea, ya sea una dirección literal IPv4 o IPv6, o un hash de router codificado en base64 de 44 caracteres. El soporte para el bloqueo con una máscara de red, por ejemplo x.y.0.0/16, es opcional. Para desbloquear una entrada, precederla con '!'. Los comentarios comienzan con '#'.

## Migración

n/a


