---
title: "Notas de estado de I2P del 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Actualización semanal del estado de I2P que abarca el progreso del desarrollo, mejoras en el transporte TCP y la nueva función userhosts.txt"
categories: ["status"]
---

Hola, equipo, actualización rápida esta semana

## Índice

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Estado del desarrollo

La red ha estado bastante estable durante la última semana, así que he podido centrar mi tiempo en la versión 0.4.1 - renovando el transporte TCP y añadiendo soporte para detectar direcciones IP y eliminando esa vieja "target changed identities". Esto también debería eliminar la necesidad de entradas de dyndns.

No será la configuración ideal de cero clics para las personas que estén detrás de NATs o cortafuegos - aún tendrán que configurar el reenvío de puertos para poder recibir conexiones TCP entrantes. Sin embargo, debería ser menos propensa a errores. Estoy haciendo todo lo posible por mantener la compatibilidad con versiones anteriores, pero no prometo nada en ese aspecto. Más noticias cuando esté listo.

## 2) Nuevo userhosts.txt vs. hosts.txt

En la próxima versión tendremos el tan solicitado soporte para un par de archivos hosts.txt - uno que se sobrescribe durante las actualizaciones (o desde `http://dev.i2p.net/i2p/hosts.txt`) y otro que el usuario puede mantener localmente. En la próxima versión (o CVS HEAD) puedes editar el archivo "userhosts.txt", que se consulta antes que hosts.txt para cualquier entrada - por favor, realiza tus cambios locales allí, ya que el proceso de actualización sobrescribirá hosts.txt (pero no userhosts.txt).

## 3) ???

Como mencioné, solo unas breves notas esta semana. ¿Alguien tiene algo más que quiera plantear? Pásense por la reunión en unos minutos.

=jr
