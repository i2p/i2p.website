---
title: "Vencimiento del Presentador"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Descripción

Esta propuesta trata sobre mejorar la tasa de éxito para las presentaciones.


## Motivación

Los presentadores expiran después de un cierto tiempo, pero esa información no se publica en el
RouterInfo. Los routers actualmente deben usar heurísticas para estimar cuándo un
presentador ya no es válido.


## Diseño

En una RouterAddress SSU que contiene presentadores, el publicador puede incluir opcionalmente
tiempos de expiración para cada presentador.


## Especificación

```
iexp{X}={nnnnnnnnnn}

X :: El número del presentador (0-2)

nnnnnnnnnn :: El tiempo en segundos (no ms) desde la época.
```

### Notas
* Cada expiración debe ser mayor que la fecha de publicación del RouterInfo,
  y menos de 6 horas después de la fecha de publicación del RouterInfo.

* Los routers publicadores y presentadores deben intentar mantener al presentador válido
  hasta la expiración, sin embargo, no hay forma de garantizar esto.

* Los routers no deben usar un presentador publicado después de su expiración.

* Las expiraciones de los presentadores están en el mapeo de RouterAddress.
  No son el campo de expiración de 8 bytes (actualmente no utilizado) en el RouterAddress.

**Ejemplo:** `iexp0=1486309470`


## Migración

No hay problemas. La implementación es opcional.
La compatibilidad con versiones anteriores está asegurada, ya que los routers antiguos ignorarán parámetros desconocidos.
