---
title: "Soporte de Floodfill para Tipos de Firma Experimentales"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Resumen

Para tipos de firma en el rango experimental (65280-65534),
los floodfills deberían aceptar almacenes netdb sin verificar la firma.

Esto apoyará la prueba de nuevos tipos de firma.


## Motivación

La propuesta GOST 134 ha revelado dos problemas con el rango experimental de tipos de firma previamente no utilizado.

Primero, dado que los tipos de firma en el rango experimental no pueden ser reservados, pueden ser usados para
múltiples tipos de firma a la vez.

Segundo, a menos que una información del router o un conjunto de arrendamiento con un tipo de firma experimental pueda ser almacenado en un floodfill,
el nuevo tipo de firma es difícil de probar completamente o usar de forma experimental.


## Diseño

Los floodfills deberían aceptar, y difundir, los almacenes LS con tipos de firma en el rango experimental,
sin verificar la firma. El soporte para almacenes RI está por determinar, y puede tener más implicaciones de seguridad.


## Especificación


Para tipos de firma en el rango experimental, un floodfill debe aceptar y difundir almacenes netdb
sin verificar la firma.

Para prevenir la suplantación de routers y destinos no experimentales, un floodfill
nunca debería aceptar un almacén de un tipo de firma experimental que tenga una colisión
de hash con una entrada netdb existente de un tipo de firma diferente.
Esto previene el secuestro de una entrada netdb previa.

Además, un floodfill debería sobrescribir una entrada netdb experimental
con un almacén de un tipo de firma no experimental que tenga una colisión de hash,
para prevenir el secuestro de un hash previamente ausente.

Los floodfills deberían asumir que la longitud de la clave pública de firma es 128, o derivarla de
la longitud del certificado de clave, si es más larga. Algunas implementaciones pueden
no soportar longitudes más largas a menos que el tipo de firma esté reservado de manera informal.


## Migración

Una vez que esta función sea soportada, en una versión conocida del router,
las entradas netdb de tipo de firma experimental pueden ser almacenadas en floodfills de esa versión o superior.

Si algunas implementaciones de router no soportan esta función, el almacén netdb
fallará, pero eso es lo mismo que ahora.


## Problemas

Puede haber implicaciones de seguridad adicionales, para ser investigadas (ver propuesta 137)

Algunas implementaciones pueden no soportar longitudes de clave mayores a 128,
como se describió anteriormente. Además, puede ser necesario imponer un máximo de 128
(en otras palabras, no hay datos de clave excesivos en el certificado de clave),
para reducir la capacidad de los atacantes de generar colisiones de hash.

Se necesitarán abordar problemas similares con tipos de cifrado no cero,
que aún no han sido propuestos formalmente.


## Notas

Los almacenes NetDB de tipos de firma desconocidos que no están en el rango experimental continuarán
siendo rechazados por los floodfills, ya que la firma no puede ser verificada.


