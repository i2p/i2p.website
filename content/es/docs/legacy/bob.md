---
title: "BOB – Puente Abierto Básico"
description: "API obsoleta para la gestión de destinos (obsoleta)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Advertencia:** BOB (Basic Open Bridge, una API heredada de I2P) solo admite el tipo de firma DSA-SHA1 heredado. Java I2P dejó de incluir BOB en **1.7.0 (2022-02)**; solo está presente en instalaciones que se iniciaron con 1.6.1 o anterior y en algunas compilaciones de i2pd. Las nuevas aplicaciones **deben** usar [SAM v3](/docs/api/samv3/).

## Vinculaciones de lenguajes

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Notas del protocolo

- `KEYS` denota un destino en base64 (claves públicas + privadas).  
- `KEY` es una clave pública en base64.  
- Las respuestas `ERROR` tienen la forma `ERROR <description>\n`.  
- `OK` indica la finalización del comando; los datos opcionales siguen en la misma línea.  
- Las líneas `DATA` transmiten salida adicional antes de un `OK` final.

El comando `help` es la única excepción: puede no devolver nada para indicar “no existe tal comando”.

## Banner de conexión

BOB utiliza líneas ASCII terminadas con salto de línea (LF o CRLF). Al conectarse, emite:

```
BOB <version>
OK
```
Versión actual: `00.00.10`. Las compilaciones anteriores usaban dígitos hexadecimales en mayúsculas y una numeración no estándar.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## Comandos principales

> Para ver los detalles completos de los comandos, conéctese con `telnet localhost 2827` y ejecute `help`.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## Resumen de obsolescencia

- BOB no tiene soporte para tipos de firma modernos, LeaseSets cifrados ni características de transporte.
- La API está congelada; no se añadirán nuevos comandos.
- Las aplicaciones que aún dependen de BOB deberían migrar a SAM v3 lo antes posible.
