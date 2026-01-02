---
title: "Tunnels unidireccionales"
description: "Resumen histórico del diseño de tunnel unidireccional de I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Aviso histórico:** Esta página conserva la discusión heredada “Unidirectional Tunnels” como referencia. Consulte la [documentación de implementación de tunnel](/docs/specs/implementation/) vigente para el comportamiento actual.

## Descripción general

I2P construye **tunnels unidireccionales**: un tunnel transporta el tráfico saliente y un tunnel separado transporta las respuestas entrantes. Esta estructura se remonta a los diseños de red más tempranos y sigue siendo un diferenciador clave frente a los sistemas de circuitos bidireccionales como Tor. Para la terminología y los detalles de implementación, consulta la [descripción general de tunnel](/docs/overview/tunnel-routing/) y la [especificación de tunnel](/docs/specs/implementation/).

## Revisión

- Los tunnel unidireccionales mantienen separado el tráfico de petición y de respuesta, de modo que cualquier grupo individual de pares confabulados observa solo la mitad de un trayecto de ida y vuelta.
- Los ataques de temporización deben cruzarse con dos conjuntos de tunnel (saliente y entrante) en lugar de analizar un único circuito, aumentando la dificultad de la correlación.
- Los conjuntos independientes, entrante y saliente, permiten a los routers ajustar la latencia, la capacidad y las características de gestión de fallos por dirección.
- Entre los inconvenientes se incluyen una mayor complejidad en la gestión de pares y la necesidad de mantener múltiples conjuntos de tunnel para una prestación de servicio fiable.

## Anonimato

El artículo de Hermann y Grothoff, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), analiza ataques de predecesor contra tunnels unidireccionales, sugiriendo que adversarios determinados pueden, con el tiempo, confirmar pares de larga duración. Los comentarios de la comunidad señalan que el estudio se basa en supuestos específicos sobre la paciencia del adversario y sus facultades legales, y no compara el enfoque con ataques de temporización que afectan a diseños bidireccionales. La investigación continua y la experiencia práctica siguen reforzando los tunnels unidireccionales como una elección deliberada de anonimato, más que como un descuido.
