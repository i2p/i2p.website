---
title: "Soporte de Floodfill para Tipos de Firma Opcionales"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Descripción General

Añadir una manera para que los floodfills anuncien soporte para tipos de firma opcionales.
Esto proporcionará una manera de soportar nuevos tipos de firma a largo plazo,
incluso si no todas las implementaciones los soportan.


## Motivación

La propuesta GOST 134 ha revelado varios problemas con el rango de tipos de firma experimentales previamente no utilizados.

Primero, dado que los tipos de firma en el rango experimental no pueden reservarse, pueden ser utilizados para
múltiples tipos de firma a la vez.

Segundo, a menos que un router info o lease set con un tipo de firma experimental pueda almacenarse en un floodfill,
el nuevo tipo de firma es difícil de probar completamente o usar de manera experimental.

Tercero, si la propuesta 136 se implementa, esto no es seguro, ya que cualquiera puede sobrescribir una entrada.

Cuarto, implementar un nuevo tipo de firma puede ser un gran esfuerzo de desarrollo.
Puede ser difícil convencer a los desarrolladores de todas las implementaciones de routers para que añadan soporte para un nuevo
tipo de firma a tiempo para cualquier lanzamiento en particular. El tiempo y las motivaciones de los desarrolladores pueden variar.

Quinto, si GOST usa un tipo de firma en el rango estándar, aún no hay manera de saber si un
floodfill particular soporta GOST.


## Diseño

Todos los floodfills deben soportar los tipos de firma DSA (0), ECDSA (1-3), y EdDSA (7).

Para cualquier otro tipo de firma en el rango estándar (no experimental), un floodfill puede
anunciar soporte en sus propiedades de router info.


## Especificación


Un router que soporta un tipo de firma opcional deberá añadir la propiedad "sigTypes"
a su router info publicado, con números de tipo de firma separados por comas.
Los tipos de firma estarán en orden numérico ascendente.
Los tipos de firma obligatorios (0-4,7) no deben incluirse.

Por ejemplo: sigTypes=9,10

Los routers que soportan tipos de firma opcionales solo deben almacenar, buscar o inundar,
a los floodfills que anuncien soporte para ese tipo de firma.


## Migración

No aplicable.
Solo los routers que soportan un tipo de firma opcional deben implementar.


## Problemas

Si no hay muchos floodfills que soporten el tipo de firma, puede ser difícil encontrarlos.

Puede que no sea necesario requerir ECDSA 384 y 521 (tipos de firma 2 y 3) para todos los floodfills.
Estos tipos no son ampliamente utilizados.

Problemas similares deberán abordarse con tipos de encriptación no cero,
lo cual aún no ha sido propuesto formalmente.


## Notas

Las tiendas de NetDB de tipos de firma desconocidos que no están en el rango experimental continuarán
siendo rechazadas por los floodfills, ya que la firma no puede verificarse.


