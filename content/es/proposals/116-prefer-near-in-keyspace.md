---
title: "Preferir Enrutadores Cercanos en el Espacio de Claves"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/1874"
---

## Descripción General

Esta es una propuesta para organizar a los pares de manera que prefieran conectarse a otros pares que estén cerca de ellos en el espacio de claves.

## Motivación

La idea es mejorar el éxito de la construcción de túneles, aumentando la probabilidad de que un enrutador ya esté conectado a otro.

## Diseño

### Cambios Requeridos

Este cambio requeriría:

1. Que cada enrutador prefiera conexiones cercanas a ellos en el espacio de claves.
2. Que cada enrutador esté al tanto de que cada enrutador prefiere conexiones cercanas a ellos en el espacio de claves.

### Ventajas para la Construcción de Túneles

Si construyes un túnel::

    A -largo-> B -corto-> C -corto-> D

(salto largo/aleatorio vs corto en el espacio de claves), puedes adivinar dónde probablemente falló la construcción del túnel e intentar con otro par en ese punto. Además, te permitiría detectar partes más densas en el espacio de claves y hacer que los enrutadores simplemente no las usen ya que podría ser alguien coludiendo.

Si construyes un túnel::

    A -largo-> B -largo-> C -corto-> D

y falla, puedes deducir que lo más probable es que haya fallado en C -> D y puedes elegir otro salto D.

También puedes construir túneles de modo que el OBEP esté más cerca del IBGW y usar esos túneles con OBEP que estén más cerca del IBGW dado en un LeaseSet.

## Implicaciones de Seguridad

Si aleatorizas la colocación de saltos cortos vs largos en el espacio de claves, un atacante probablemente no obtendrá mucha ventaja.

Sin embargo, la mayor desventaja es que podría hacer que la enumeración de usuarios sea un poco más fácil.
