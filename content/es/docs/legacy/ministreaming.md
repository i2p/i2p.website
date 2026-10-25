---
title: "Biblioteca Ministreaming"
description: "Notas históricas sobre la primera capa de transporte tipo TCP de I2P"
slug: "ministreaming"
aliases:
  - "/es/ministreaming"
  - "/es/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Nota

La librería ministreaming ha sido mejorada y extendida por la [librería streaming](/docs/api/streaming) "completa". Ministreaming está deprecado y es incompatible con las aplicaciones actuales. La siguiente documentación es antigua. También ten en cuenta que streaming extiende ministreaming en el mismo paquete Java (net.i2p.client.streaming), por lo que la documentación actual de la API contiene ambos. Las clases y métodos obsoletos de ministreaming están claramente marcados como deprecados en los Javadocs.

## Biblioteca Ministreaming

La biblioteca ministreaming es una capa sobre el núcleo [I2CP](/docs/protocol/i2cp) que permite flujos confiables, ordenados y autenticados de mensajes para operar a través de una capa de mensajes no confiable, desordenada y no autenticada. Al igual que la relación entre TCP e IP, esta funcionalidad de streaming tiene toda una serie de compromisos y optimizaciones disponibles, pero en lugar de integrar esa funcionalidad en el código base de I2P, se ha separado en su propia biblioteca tanto para mantener las complejidades similares a TCP separadas como para permitir implementaciones alternativas optimizadas.

La biblioteca ministreaming fue escrita by mihi como parte de su aplicación [I2PTunnel](/docs/api/i2ptunnel) y luego fue separada y liberada bajo la licencia BSD. Se llama biblioteca de "mini"streaming porque hace algunas simplificaciones en la implementación, mientras que una biblioteca de streaming más robusta podría estar más optimizada para operar sobre I2P. Los dos problemas principales con la biblioteca ministreaming son su uso del protocolo tradicional de establecimiento de dos fases TCP y el tamaño de ventana fijo actual de 1. El problema de establecimiento es menor para streams de larga duración, pero para los cortos, como solicitudes HTTP rápidas, el impacto puede ser significativo. En cuanto al tamaño de ventana, la biblioteca ministreaming no mantiene ningún ID u ordenamiento dentro de los mensajes enviados (ni incluye ningún ACK o SACK a nivel de aplicación), por lo que debe esperar en promedio el doble del tiempo que toma enviar un mensaje antes de enviar otro.

Incluso con esos problemas, la biblioteca ministreaming funciona bastante bien en muchas situaciones, y su API es tanto bastante simple como capaz de mantenerse sin cambios a medida que se introducen diferentes implementaciones de streaming. La biblioteca se despliega en su propio ministreaming.jar. Los desarrolladores en Java que deseen usarla pueden acceder a la API directamente, mientras que los desarrolladores en otros lenguajes pueden usarla a través del soporte de streaming de [SAM](/docs/api/samv3).
