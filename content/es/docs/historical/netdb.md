---
title: "Discusión sobre la base de datos de la red"
description: "Notas históricas sobre floodfill, experimentos con Kademlia (algoritmo DHT) y ajustes futuros para la netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Nota:** Esta discusión archivada describe enfoques históricos de la base de datos de la red (netDb). Consulta la [documentación principal de netDb](/docs/specs/common-structures/) para conocer el comportamiento actual y la orientación.

## Historia

La netDb de I2P se distribuye mediante un algoritmo floodfill simple. Las primeras versiones también mantenían una implementación de Kademlia DHT como respaldo, pero demostró ser poco fiable y fue deshabilitada por completo en la versión 0.6.1.20. El diseño floodfill reenvía una entrada publicada a un router participante, espera la confirmación y vuelve a intentarlo con otros pares floodfill si es necesario. Los pares floodfill difunden stores (mensajes de almacenamiento) desde routers no floodfill a todos los demás participantes floodfill.

A finales de 2009, las consultas de Kademlia se reintrodujeron parcialmente para reducir la carga de almacenamiento en los routers floodfill individuales.

### Introducción a Floodfill

Floodfill apareció por primera vez en la versión 0.6.0.4, mientras que Kademlia (protocolo DHT) siguió disponible como respaldo. En ese momento, la gran pérdida de paquetes y las rutas restringidas dificultaban obtener acuses de recibo de los cuatro pares más cercanos, lo que a menudo requería decenas de intentos de almacenamiento redundantes. Pasar a un subconjunto floodfill de routers accesibles desde el exterior proporcionó una solución pragmática a corto plazo.

### Repensar Kademlia (protocolo de tabla hash distribuida)

Entre las alternativas consideradas se encontraban:

- Ejecutando la netDb como una Kademlia DHT (tabla hash distribuida Kademlia) limitada a routers alcanzables que opten por participar
- Manteniendo el modelo floodfill pero limitando la participación a routers capaces y verificando la distribución con comprobaciones aleatorias

El enfoque floodfill se impuso porque era más fácil de implementar y la netDb solo contiene metadatos, no cargas útiles de usuario. La mayoría de los destinos nunca publican un LeaseSet porque el remitente suele empaquetar su LeaseSet en garlic messages (mensajes "garlic" que encapsulan varios mensajes).

## Estado actual (perspectiva histórica)

Los algoritmos de netDb (base de datos de la red) están optimizados para las necesidades de la red y, históricamente, han gestionado cómodamente unos cientos de routers. Las estimaciones iniciales sugerían que 3–5 routers floodfill (nodos especializados que almacenan y distribuyen datos en la netDb) podrían soportar aproximadamente 10.000 nodos.

### Cálculos actualizados (marzo de 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Donde:

- `N`: routers en la red
- `L`: Número promedio de destinos de cliente por router (más uno por el `RouterInfo`)
- `F`: Porcentaje de fallos de tunnel
- `R`: Período de reconstrucción del tunnel como fracción de la vida útil del tunnel
- `S`: Tamaño promedio de una entrada de netDb
- `T`: Vida útil del tunnel

Usando valores de 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) da como resultado:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### ¿Volverá Kademlia?

Los desarrolladores debatieron reintroducir Kademlia (algoritmo de tabla hash distribuida, DHT) hacia principios de 2007. El consenso fue que la capacidad de floodfill podía ampliarse de forma incremental según fuera necesario, mientras que Kademlia añadía una complejidad y unos requisitos de recursos significativos para el conjunto base de routers. El mecanismo de respaldo permanece inactivo a menos que la capacidad de floodfill resulte insuficiente.

### Planificación de capacidad de Floodfill (routers especiales que almacenan y propagan la netDb)

La admisión automática de routers de clase de ancho de banda `O` en floodfill, aunque tentadora, arriesga escenarios de denegación de servicio si nodos hostiles optan por participar. Un análisis histórico indicó que limitar el conjunto de floodfill (por ejemplo, 3–5 pares gestionando ~10K routers) era más seguro. Se han utilizado operadores de confianza o heurísticas automáticas para mantener un conjunto de floodfill adecuado pero controlado.

## Tareas pendientes de Floodfill (router especial de I2P que almacena y distribuye la netDb) (Histórico)

> Esta sección se conserva para la posteridad. La página principal de netDb realiza el seguimiento de la hoja de ruta actual y de las consideraciones de diseño.

Incidentes operativos, como un período el 13 de marzo de 2008 con solo un floodfill router disponible, motivaron varias mejoras introducidas en las versiones 0.6.1.33 hasta la 0.7.x, entre ellas:

- Aleatorización de la selección de floodfill para las búsquedas y preferencia por pares con buena respuesta
- Visualización de métricas adicionales de floodfill en la página "Profiles" de la consola del router
- Reducciones progresivas en el tamaño de las entradas de netDb para reducir el uso de ancho de banda de floodfill
- Activación automática para un subconjunto de routers de clase `O` basada en el rendimiento recopilado a través de datos de perfil
- Mejoras en las listas de bloqueo, la selección de pares floodfill y las heurísticas de exploración

Las ideas restantes del período incluían:

- Usar estadísticas de `dbHistory` para evaluar y seleccionar mejor a pares floodfill
- Mejorar el comportamiento de reintento para evitar contactar repetidamente a pares que fallan
- Aprovechar las métricas de latencia y las puntuaciones de integración en la selección
- Detectar y reaccionar más rápidamente ante routers floodfill que fallan
- Seguir reduciendo las demandas de recursos en nodos de alto ancho de banda y floodfill

Incluso a la fecha de estas notas, la red se consideraba resiliente, con infraestructura establecida para responder rápidamente a floodfills hostiles o a ataques de denegación de servicio dirigidos contra floodfills.

## Notas adicionales

- La consola del router lleva tiempo exponiendo datos de perfil mejorados para ayudar a analizar la fiabilidad de floodfill.
- Aunque los comentarios históricos especulaban sobre Kademlia u otros esquemas DHT (tabla hash distribuida) alternativos, floodfill ha seguido siendo el algoritmo principal para las redes de producción.
- La investigación orientada al futuro se centró en que la admisión a floodfill fuera adaptativa y en limitar las oportunidades de abuso.
