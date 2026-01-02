---
title: "SAM v2"
description: "Protocolo heredado de Simple Anonymous Messaging"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsoleto:** SAM v2 se entregó con I2P 0.6.1.31 y ya no se mantiene. Usa [SAM v3](/docs/api/samv3/) para nuevos desarrollos. La única mejora de v2 respecto a v1 fue la compatibilidad con varios sockets multiplexados sobre una única conexión SAM.

## Notas de la versión

- La cadena de versión reportada sigue siendo "2.0".
- Desde 0.9.14, el mensaje `HELLO VERSION` acepta valores `MIN`/`MAX` de un solo dígito y el parámetro `MIN` es opcional.
- `DEST GENERATE` admite `SIGNATURE_TYPE`, por lo que se pueden crear destinos Ed25519.

## Conceptos básicos de la sesión

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Cada destino puede tener solo una sesión SAM activa (flujos, datagramas o sin procesar).
- `STYLE` selecciona flujos virtuales, datagramas firmados o datagramas sin procesar.
- Las opciones adicionales se pasan a I2CP (por ejemplo, `tunnels.quantityInbound=3`).
- Las respuestas reflejan la v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Codificación de mensajes

ASCII orientado a líneas con pares `key=value` separados por espacios (los valores pueden ir entre comillas). Los tipos de comunicación son los mismos que en v1:

- Flujos a través de la I2P streaming library (biblioteca de transmisión de I2P)
- Datagramas con respuesta (`PROTO_DATAGRAM`)
- Datagramas sin procesar (`PROTO_DATAGRAM_RAW`)

## Cuándo usarlo

Solo para clientes heredados que no pueden migrar. SAM v3 ofrece:

- Transferencia de destino en binario (`DEST GENERATE BASE64`)
- Subsesiones y soporte para DHT (v3.3)
- Mejores informes de errores y negociación de opciones

Consulte:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [API de datagramas](/docs/api/datagrams/)
- [Protocolo de streaming](/docs/specs/streaming/)
