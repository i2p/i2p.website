---
title: "Implementación antigua de tunnel (heredada)"
description: "Descripción archivada del diseño de tunnel usado antes de I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Estado de legado:** Este contenido se conserva únicamente como referencia histórica. Documenta el sistema de tunnel que se distribuía antes de I2P&nbsp;0.6.1.10 y no debe usarse para el desarrollo moderno. Consulte la [implementación actual](/docs/specs/implementation/) para obtener orientación de producción.

El subsistema de tunnel original también usaba tunnels unidireccionales, pero difería en el formato de los mensajes, la detección de duplicados y la estrategia de construcción. Muchas secciones a continuación replican la estructura del documento obsoleto para facilitar la comparación.

## 1. Descripción general del Tunnel

- Los Tunnels se construían como secuencias ordenadas de pares seleccionados por el creador.
- Las longitudes de los Tunnels variaban de 0–7 saltos, con varios ajustes para relleno, limitación y generación de chaff (tráfico señuelo).
- Los Tunnels de entrada entregaban mensajes desde una puerta de enlace no confiable al creador (punto final); los Tunnels de salida enviaban los datos alejándolos del creador.
- La vida útil de los Tunnels era de 10 minutos, tras lo cual se construían nuevos Tunnels (a menudo usando los mismos pares pero con diferentes ID de Tunnel).

## 2. Funcionamiento en el diseño heredado

### 2.1 Preprocesamiento de mensajes

Las puertas de enlace acumularon ≤32&nbsp;KB de carga útil de I2NP, seleccionaron el relleno y produjeron una carga útil que contenía:

- Un campo de longitud de relleno de dos bytes y esa misma cantidad de bytes aleatorios
- Una secuencia de pares `{instructions, I2NP message}` que describen los destinos de entrega, la fragmentación y los retrasos opcionales
- Mensajes I2NP completos rellenados hasta un múltiplo de 16 bytes

Las instrucciones de entrega empaquetaban la información de enrutamiento en campos de bits (tipo de entrega, indicadores de retraso, indicadores de fragmentación y extensiones opcionales). Los mensajes fragmentados llevaban un ID de mensaje de 4 bytes más un indicador de índice/último fragmento.

### 2.2 Cifrado en la puerta de enlace

El diseño heredado fijaba la longitud del tunnel en ocho saltos para la fase de cifrado. Las puertas de enlace aplicaban capas de AES-256/CBC junto con bloques de suma de verificación, de modo que cada salto pudiera verificar la integridad sin reducir la carga útil. La propia suma de verificación era un bloque derivado de SHA-256 incrustado dentro del mensaje.

### 2.3 Comportamiento de los participantes

Los participantes seguían los identificadores de tunnel entrantes, verificaban la integridad de forma temprana y descartaban duplicados antes de reenviar. Como los bloques de relleno y verificación estaban integrados, el tamaño del mensaje se mantenía constante independientemente del número de saltos.

### 2.4 Procesamiento del extremo

Los extremos descifraron los bloques en capas secuencialmente, validaron las sumas de verificación y volvieron a dividir la carga útil en las instrucciones codificadas más los mensajes I2NP para su posterior entrega.

## 3. Construcción de Tunnel (Proceso obsoleto)

1. **Selección de pares:** Los pares se eligieron a partir de perfiles mantenidos localmente (exploratorio vs. cliente). El documento original ya destacaba la mitigación del [ataque de predecesor](https://en.wikipedia.org/wiki/Predecessor_attack) reutilizando listas ordenadas de pares por cada grupo de tunnel.
2. **Entrega de solicitudes:** Los mensajes de construcción se reenviaban salto a salto con secciones cifradas para cada par. Se debatieron ideas alternativas, como la extensión telescópica, el reencaminamiento a mitad del trayecto o eliminar bloques de suma de comprobación, como experimentos, pero nunca se adoptaron.
3. **Agrupación:** Cada destino local mantenía grupos de entrada y de salida por separado. Los ajustes incluían la cantidad deseada, tunnels de respaldo, variación de longitud, limitación y políticas de relleno.

## 4. Conceptos de limitación y mezcla

El documento antiguo propuso varias estrategias que influyeron en las versiones posteriores:

- Descarte aleatorio temprano ponderado (WRED) para el control de congestión
- Limitadores por tunnel basados en promedios móviles del uso reciente
- Controles opcionales de chaff (relleno de tráfico) y batching (agrupación por lotes) (no totalmente implementados)

## 5. Alternativas archivadas

Secciones del documento original exploraron ideas que nunca se implementaron:

- Eliminar bloques de suma de verificación para reducir el procesamiento por salto
- Aplicar telescoping (construcción escalonada) a tunnels a mitad del trayecto para cambiar la composición de pares
- Cambiar a tunnels bidireccionales (finalmente rechazado)
- Usar hashes más cortos o diferentes esquemas de relleno

Estas ideas siguen siendo un valioso contexto histórico, pero no reflejan la base de código moderna.

## Referencias

- Archivo original de documentos heredados (pre-0.6.1.10)
- [Descripción general de Tunnel](/docs/overview/tunnel-routing/) para la terminología actual
- [Perfilado y selección de pares](/docs/overview/tunnel-routing#peer-selection/) para heurísticas modernas
