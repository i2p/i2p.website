---
title: "SAM v1"
description: "Protocolo de mensajería anónima simple heredado (en desuso)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsoleto:** SAM v1 se mantiene únicamente como referencia histórica. Las aplicaciones nuevas deberían usar [SAM v3](/docs/api/samv3/) o [BOB](/docs/legacy/bob/). El puente original solo admite destinos DSA-SHA1 y un conjunto limitado de opciones.

## Bibliotecas

El árbol del código fuente de I2P en Java aún incluye enlaces heredados para C, C#, Perl y Python. Ya no se mantienen y se distribuyen principalmente para compatibilidad con versiones archivadas.

## Negociación de versiones

Los clientes se conectan a través de TCP (por defecto `127.0.0.1:7656`) y intercambian:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
A partir de Java I2P 0.9.14, el parámetro `MIN` es opcional y tanto `MIN` como `MAX` aceptan formas de un solo dígito (`"3"` etc.) para puentes actualizados.

## Creación de sesión

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` carga o crea una entrada en `sam.keys`; `TRANSIENT` siempre crea un destino temporal.
- `STYLE` selecciona flujos virtuales (similar a TCP), datagramas firmados o datagramas en bruto.
- `DIRECTION` se aplica solo a sesiones de flujo; de forma predeterminada es `BOTH`.
- Los pares clave/valor adicionales se pasan como opciones de I2CP (por ejemplo, `tunnels.quantityInbound=3`).

El puente responde con:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Los errores devuelven `DUPLICATED_DEST`, `I2P_ERROR` o `INVALID_KEY`, además de un mensaje opcional.

## Formatos de mensajes

Los mensajes SAM son ASCII de una sola línea con pares clave/valor delimitados por espacios. Las claves están en UTF‑8; los valores pueden ir entre comillas si contienen espacios. No se define ningún mecanismo de escape.

Tipos de comunicación:

- **Flujos** – encaminados a través de la biblioteca de streaming de I2P
- **Datagramas con posibilidad de respuesta** – cargas útiles firmadas (Datagram1)
- **Datagramas sin formato** – cargas útiles sin firma (Datagram RAW)

## Opciones añadidas en 0.9.14

- `DEST GENERATE` acepta `SIGNATURE_TYPE=...` (permitiendo Ed25519 (algoritmo de firma digital), etc.)
- `HELLO VERSION` trata `MIN` como opcional y acepta cadenas de versión de un solo dígito

## Cuándo usar SAM v1

Solo para la interoperabilidad con software heredado que no puede actualizarse. Para todo desarrollo nuevo, utilice:

- [SAM v3](/docs/api/samv3/) para acceso completo a flujos/datagramas
- [BOB](/docs/legacy/bob/) para la gestión de destinos (sigue siendo limitado, pero admite funciones más modernas)

## Referencias

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Especificación de datagramas](/docs/api/datagrams/)
- [Protocolo de streaming](/docs/specs/streaming/)

SAM v1 sentó las bases para el desarrollo de aplicaciones agnósticas del router, pero el ecosistema ha evolucionado. Considere este documento como una ayuda de compatibilidad más que como un punto de partida.
