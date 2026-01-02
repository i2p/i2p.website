---
title: "v3dgsend"
description: "Utilidad CLI para enviar datagramas I2P mediante SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Estado: Esta es una referencia concisa para la utilidad `v3dgsend`. Complementa la documentación de la [API de Datagramas](/docs/api/datagrams/) y [SAM v3](/docs/api/samv3/).

## Resumen general

`v3dgsend` es una herramienta de línea de comandos para enviar datagramas I2P utilizando la interfaz SAMv3. Es útil para probar la entrega de datagramas, prototipar servicios y verificar el comportamiento de extremo a extremo sin escribir un cliente completo.

Los usos típicos incluyen:

- Prueba de humo de accesibilidad de datagramas a un Destino
- Validación de configuración de firewall y libreta de direcciones
- Experimentación con datagramas sin procesar vs. firmados (respondibles)

## Uso

La invocación básica varía según la plataforma y el paquete. Las opciones comunes incluyen:

- Destination: Destination en base64 o nombre `.i2p`
- Protocol: raw (PROTOCOL 18) o signed (PROTOCOL 17)
- Payload: cadena en línea o archivo de entrada

Consulte el empaquetado de su distribución o la salida de `--help` para conocer las banderas exactas.

## Ver también

- [API de Datagramas](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Biblioteca de Streaming](/docs/api/streaming/) (alternativa a los datagramas)
