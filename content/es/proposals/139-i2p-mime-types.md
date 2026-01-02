---
title: "Tipos MIME I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Abierto"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Descripción general

Definir tipos MIME para formatos de archivos comunes de I2P.
Incluir las definiciones en paquetes Debian.
Proveer un manejador para el tipo .su3, y posiblemente otros.


## Motivación

Para facilitar la resiembra y la instalación de plugins cuando se descargan con un navegador,
necesitamos un tipo MIME y un manejador para archivos .su3.

Ya que nos encontramos en ello, tras aprender a escribir el archivo de definición MIME,
siguiendo el estándar de freedesktop.org, podemos añadir definiciones para otros tipos
de archivos comunes de I2P.
Aunque son menos útiles para archivos que usualmente no se descargan, como la
base de datos del bloque del libro de direcciones (hostsdb.blockfile), estas definiciones
permitirán que los archivos sean mejor identificados e iconificados al usar un visor
de directorios gráfico como "nautilus" en Ubuntu.

Al estandarizar los tipos MIME, cada implementación de router puede escribir manejadores
según sea apropiado, y el archivo de definición MIME puede ser compartido por todas las implementaciones.


## Diseño

Escribir un archivo fuente XML siguiendo el estándar freedesktop.org e incluirlo
en los paquetes Debian. El archivo es "debian/(package).sharedmimeinfo".

Todos los tipos MIME de I2P comenzarán con "application/x-i2p-", excepto para el jrobin rrd.

Los manejadores para estos tipos MIME son específicos de la aplicación y no serán
especificados aquí.

También incluiremos las definiciones con Jetty, y las incluiremos con el
software de resiembra o las instrucciones.


## Especificación

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(genérico)	application/x-i2p-su3

.su3	(actualización de router)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(resiembra)	application/x-i2p-su3-reseed

.su3	(noticias)		application/x-i2p-su3-news

.su3	(lista de bloqueos)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Notas

No todos los formatos de archivo listados arriba son usados por implementaciones de routers no Java;
algunos pueden ni siquiera estar bien especificados. Sin embargo, documentarlos aquí
puede permitir una consistencia entre implementaciones en el futuro.

Algunas extensiones de archivo como ".config", ".dat" y ".info" pueden coincidir con otros
tipos MIME. Estos pueden ser desambiguados con datos adicionales como
el nombre completo del archivo, un patrón de nombre de archivo, o números mágicos.
Ver el borrador del archivo i2p.sharedmimeinfo en el hilo zzz.i2p para ejemplos.

Los importantes son los tipos .su3, y esos tipos tienen tanto
una extensión única como definiciones de números mágicos robustas.


## Migración

No aplicable.
