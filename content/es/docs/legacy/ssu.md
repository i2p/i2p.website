---
title: "SSU (heredado)"
description: "Transporte UDP seguro semiconfiable original"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Obsoleto:** SSU fue reemplazado por SSU2. Se eliminó el soporte en i2pd 2.44.0 (API 0.9.56, nov 2022) y en Java I2P 2.4.0 (API 0.9.61, dic 2023).

SSU ofrecía una entrega parcialmente fiable basada en UDP, con control de congestión, travesía de NAT y soporte para introducer (nodo introductor). Complementaba a NTCP al gestionar routers detrás de NAT/cortafuegos y al coordinar el descubrimiento de IP.

## Elementos de la dirección

- `transport`: `SSU`
- `caps`: indicadores de capacidad (`B`, `C`, `4`, `6`, etc.)
- `host` / `port`: escucha IPv4 o IPv6 (opcional cuando el router está detrás de un cortafuegos)
- `key`: clave de introducción en Base64
- `mtu`: Opcional; predeterminado 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: entradas de introducer (introductor) cuando el router está detrás de un cortafuegos

## Características

- Atravesamiento de NAT cooperativo mediante introducers (nodos presentadores)
- Detección de IP local mediante pruebas entre pares y la inspección de paquetes entrantes
- Estado del cortafuegos retransmitido automáticamente a otros transportes y a la consola del router
- Entrega semiconfiable: los mensajes se retransmiten hasta un límite y luego se descartan
- Control de congestión con aumento aditivo/disminución multiplicativa y campos de bits de ACK de fragmentos

SSU también se encargaba de tareas de metadatos, como balizas de temporización y negociación de MTU. Toda la funcionalidad ahora la proporciona (con criptografía moderna) [SSU2](/docs/specs/ssu2/).
