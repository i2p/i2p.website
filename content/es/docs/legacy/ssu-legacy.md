---
title: "Transporte SSU (Obsoleto)"
description: "Transporte UDP original utilizado antes de SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Obsoleto:** SSU (Secure Semi-Reliable UDP) ha sido reemplazado por [SSU2](/docs/specs/ssu2/). Java I2P eliminó SSU en la versión 2.4.0 (API 0.9.61) y i2pd lo eliminó en la 2.44.0 (API 0.9.56). Este documento se conserva únicamente como referencia histórica.

## Aspectos destacados

- Transporte UDP que proporciona entrega punto a punto cifrada y autenticada de mensajes de I2NP.
- Se basaba en un intercambio Diffie–Hellman de 2048 bits (el mismo número primo que ElGamal).
- Cada datagrama llevaba un HMAC‑MD5 de 16 bytes (variante truncada no estándar) + un IV de 16 bytes, seguido de una carga útil cifrada con AES‑256‑CBC.
- La prevención de repeticiones y el estado de la sesión se controlaban dentro de la carga útil cifrada.

## Encabezado del mensaje

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Cálculo de MAC utilizado: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` con una clave de MAC de 32 bytes. La longitud de la carga útil, un entero de 16 bits en big-endian, se incluía dentro del cálculo del MAC. La versión del protocolo por defecto era `0`; netId por defecto era `2` (red principal).

## Claves de sesión y MAC

Derivado del secreto compartido de DH:

1. Convierta el valor compartido en una matriz de bytes big-endian (orden de bytes de mayor peso primero) (anteponga `0x00` si el bit más significativo está en 1).
2. Clave de sesión: los primeros 32 bytes (rellene con ceros si es más corta).
3. Clave MAC: bytes 33–64; si no hay suficientes, recurra al hash SHA-256 del valor compartido.

## Estado

Los Routers ya no anuncian direcciones SSU. Los clientes deberían migrar a los transportes SSU2 o NTCP2. Se pueden encontrar implementaciones históricas en versiones anteriores:

- Código fuente de Java anterior a la versión 2.4.0 en `router/transport/udp`
- Código fuente de i2pd (implementación de I2P en C++) anterior a la versión 2.44.0

Para el comportamiento actual del transporte UDP, consulte la [especificación de SSU2](/docs/specs/ssu2/).
