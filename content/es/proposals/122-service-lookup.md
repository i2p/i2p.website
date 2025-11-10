---
title: "Búsqueda de Servicios"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Rechazado"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Visión General

Esta es la propuesta "todo vale en la netdb" completa y bombástica. También conocida como anycast. Este sería el 4to subtipo propuesto de LS2.

## Motivación

Supongamos que quisieras anunciar tu destino como un outproxy, o un nodo GNS, o una puerta de enlace Tor, o un DHT de Bittorrent o imule o i2phex o un Seedless bootstrap, etc. Podrías almacenar esta información en el netDB en lugar de usar una capa de arranque o información separada.

No hay nadie a cargo, así que, a diferencia del multihoming masivo, no puedes tener una lista autoritativa firmada. Así que simplemente publicarías tu registro en un floodfill. El floodfill los agregaría y los enviaría como respuesta a las consultas.

## Ejemplo

Supongamos que tu servicio era "GNS". Enviarías un almacenamiento de base de datos al floodfill:

- Hash de "GNS"
- destino
- marca de tiempo de publicación
- expiración (0 por revocación)
- puerto
- firma

Cuando alguien hiciera una búsqueda, obtendría una lista de esos registros:

- Hash de "GNS"
- Hash del Floodfill
- Marca de tiempo
- número de registros
- Lista de registros
- firma del floodfill

Las expiraciones serían relativamente largas, por lo menos horas.

## Implicaciones de seguridad

El inconveniente es que esto podría convertirse en el DHT de Bittorrent o peor. Como mínimo, los floodfills tendrían que limitar severamente la tasa y capacidad de los almacenes y consultas. Podríamos poner en una lista blanca nombres de servicios aprobados para límites superiores. También podríamos prohibir los servicios no incluidos en la lista blanca por completo.

Por supuesto, incluso el netDB de hoy está abierto al abuso. Puedes almacenar datos arbitrarios en el netDB, siempre y cuando parezca un RI o LS y la firma sea verificada. Pero esto lo haría mucho más fácil.
