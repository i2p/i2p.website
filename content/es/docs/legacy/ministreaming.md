---
title: "Ministreaming Library (biblioteca de streaming minimalista)"
description: "Notas históricas sobre la primera capa de transporte de tipo TCP de I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Obsoleto:** La biblioteca ministreaming es anterior a la [biblioteca de streaming](/docs/specs/streaming/) actual. Las aplicaciones modernas deben usar la API de streaming completa o SAM v3. La información a continuación se conserva para desarrolladores que revisan código fuente heredado distribuido en `ministreaming.jar`.

## Descripción general

Ministreaming (protocolo ligero de flujo fiable) se ejecuta sobre [I2CP](/docs/specs/i2cp/) para proporcionar entrega fiable y en orden a través de la capa de mensajes de I2P—de forma similar a TCP sobre IP. Originalmente se separó de la aplicación **I2PTunnel** en sus primeras etapas (con licencia BSD) para que los transportes alternativos pudieran evolucionar de manera independiente.

Restricciones clave de diseño:

- Establecimiento de conexión clásico en dos fases (SYN/ACK/FIN) tomado de TCP
- Tamaño de ventana fijo de **1** paquete
- Sin identificadores por paquete ni acuses de recibo selectivos

Estas decisiones mantuvieron la implementación pequeña, pero limitan el rendimiento—cada paquete suele esperar casi dos RTT (tiempo de ida y vuelta) antes de que se envíe el siguiente. Para flujos de larga duración la penalización es aceptable, pero los intercambios cortos al estilo HTTP se resienten notablemente.

## Relación con la biblioteca de streaming

La biblioteca de streaming actual continúa en el mismo paquete de Java (`net.i2p.client.streaming`). Las clases y métodos obsoletos permanecen en los Javadocs, claramente anotados para que los desarrolladores puedan identificar las APIs de la era de ministreaming. Cuando la biblioteca de streaming reemplazó a ministreaming (biblioteca de streaming anterior), añadió:

- Establecimiento de conexión más inteligente con menos viajes de ida y vuelta
- Ventanas de congestión adaptativas y lógica de retransmisión
- Mejor rendimiento en tunnels con pérdidas

## ¿Cuándo fue útil Ministreaming (minitransmisión)?

A pesar de sus límites, ministreaming (implementación mínima de streaming) proporcionó un transporte fiable en los primeros despliegues. La API era deliberadamente pequeña y preparada para el futuro, de modo que se pudieran sustituir motores de streaming alternativos sin romper la compatibilidad con los consumidores de la API. Las aplicaciones Java lo enlazaban directamente; los clientes no Java accedían a la misma funcionalidad mediante la compatibilidad de [SAM](/docs/legacy/sam/) con sesiones de streaming.

Actualmente, considere `ministreaming.jar` únicamente como una capa de compatibilidad. El nuevo desarrollo debería:

1. Utiliza la biblioteca de streaming completa (Java) o SAM v3 (estilo `STREAM`)  
2. Elimina cualquier suposición persistente de ventana fija al modernizar el código  
3. Prefiere tamaños de ventana más grandes y negociaciones de conexión optimizadas para mejorar cargas de trabajo sensibles a la latencia

## Referencia

- [Documentación de la biblioteca Streaming](/docs/specs/streaming/)
- [Javadoc de Streaming](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – incluye clases de ministreaming obsoletas
- [Especificación de SAM v3](/docs/api/samv3/) – soporte de streaming para aplicaciones no Java

Si te encuentras con código que aún depende de ministreaming (API de streaming antigua), planea portarlo a la API de streaming moderna: la red y sus herramientas esperan el comportamiento más reciente.
