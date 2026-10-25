---
title: "Rendimiento"
description: "Rendimiento de la red I2P: velocidad, conexiones y gestión de recursos"
slug: "performance"
aliases:
  - "/es/about/performance/future"
  - "/es/about/performance/future/"
  - "/es/about/performance/history"
  - "/es/about/performance/history/"
  - "/es/performance"
  - "/es/performance/"
  - "/es/performance-history"
  - "/es/performance-history/"
  - "/es/benchmarks"
  - "/es/benchmarks/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Rendimiento de la Red I2P: Velocidad, Conexiones y Gestión de Recursos

La red I2P es completamente dinámica. Cada cliente es conocido por otros nodos y prueba localmente los nodos conocidos para verificar su alcance y capacidad. Solo los nodos alcanzables y capaces se guardan en una NetDB local. Durante el proceso de construcción de tunnel, los mejores recursos se seleccionan de este conjunto para construir tunnels. Debido a que las pruebas ocurren continuamente, el conjunto de nodos cambia. Cada nodo I2P conoce una parte diferente de la NetDB, lo que significa que cada router tiene un conjunto diferente de nodos I2P para usar en los tunnels. Incluso si dos routers tienen el mismo subconjunto de nodos conocidos, las pruebas de alcance y capacidad probablemente mostrarán resultados diferentes, ya que los otros routers podrían estar bajo carga justo cuando un router prueba, pero estar libres cuando el segundo router prueba.

Esto describe por qué cada nodo I2P tiene diferentes nodos para construir tunnels. Debido a que cada nodo I2P tiene diferentes valores de latencia y ancho de banda, los tunnels (que se construyen a través de esos nodos) tienen diferentes valores de latencia y ancho de banda. Y debido a que cada nodo I2P tiene diferentes tunnels construidos, no hay dos nodos I2P que tengan los mismos conjuntos de tunnels.

Un servidor/cliente se conoce como un "destino" y cada destino tiene al menos un túnel de entrada y uno de salida. El valor predeterminado es 3 saltos por túnel. Esto suma un total de 12 saltos (es decir, 12 nodos I2P diferentes) para un viaje completo de ida y vuelta cliente-servidor-cliente.

Cada paquete de datos se envía a través de 6 otros nodos I2P hasta que llega al servidor:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
y en el camino de regreso 6 nodos I2P diferentes:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
El tráfico en la red necesita un ACK antes de que se envíen nuevos datos, debe esperar hasta que un ACK regrese del servidor: enviar datos, esperar el ACK, enviar más datos, esperar el ACK. Como el RTT (tiempo de ida y vuelta) se acumula por la latencia de cada nodo I2P individual y cada conexión en este viaje de ida y vuelta, usualmente toma de 1 a 3 segundos hasta que un ACK regrese al cliente. Debido al diseño de TCP y el transporte I2P, un paquete de datos tiene un tamaño limitado. Juntas, estas condiciones establecen un límite de ancho de banda máximo por tunnel de 20-50 kbyte/seg. Sin embargo, si SOLO UN salto en el tunnel tiene únicamente 5 kb/seg de ancho de banda disponible, todo el tunnel se limita a 5 kb/seg, independientemente de la latencia y otras limitaciones.

El cifrado, la latencia y cómo se construye un tunnel lo hace bastante costoso en tiempo de CPU para construir un tunnel. Por esta razón, un destino solo puede tener un máximo de 6 tunnels de ENTRADA y 6 de SALIDA para transportar datos. Con un máximo de 50 kb/seg por tunnel, un destino podría usar aproximadamente 300 kb/seg de tráfico combinado (en realidad podría ser más si se usan tunnels más cortos con poca o ninguna anonimidad disponible). Los tunnels usados se descartan cada 10 minutos y se construyen nuevos. Este cambio de tunnels, y a veces clientes que se desconectan o pierden su conexión a la red, ocasionalmente romperán tunnels y conexiones. Un ejemplo de esto se puede ver en la Red IRC2P en pérdida de conexión (tiempo de espera agotado del ping) o al usar eepget.

Con un conjunto limitado de destinos y un conjunto limitado de tunnels por destino, un nodo I2P solo utiliza un conjunto limitado de tunnels a través de otros nodos I2P. Por ejemplo, si un nodo I2P es "hop1" en el pequeño ejemplo anterior, solo vemos 1 tunnel participante que se origina desde el cliente. Si sumamos toda la red I2P, solo un número bastante limitado de tunnels participantes podría construirse con una cantidad limitada de ancho de banda en total. Si uno distribuye estos números limitados entre el número de nodos I2P, solo hay una fracción del ancho de banda/capacidad disponible para uso.

Para mantener el anonimato, un router no debería ser utilizado por toda la red para construir tunnels. Si un router actúa como tunnel router para TODOS los nodos I2P, se convierte en un punto central de falla muy real, así como en un punto central para recopilar IPs y datos de los clientes. Esta es la razón por la cual la red distribuye el tráfico entre nodos en el proceso de construcción de tunnels.

Otra consideración para el rendimiento es la forma en que I2P maneja las redes mesh. Cada salto de conexión utiliza una conexión TCP o UDP en los nodos I2P. Con 1000 conexiones, se ven 1000 conexiones TCP. Eso es bastante, y algunos routers domésticos y de oficinas pequeñas solo permiten un número pequeño de conexiones. I2P intenta limitar estas conexiones a menos de 1500 por tipo UDP y por tipo TCP. Esto también limita la cantidad de tráfico enrutado a través de un nodo I2P.

Si un nodo es accesible, tiene una configuración de ancho de banda de >128 kbyte/sec compartidos y está disponible 24/7, debería ser utilizado después de un tiempo para tráfico participante. Si se desconecta en el intermedio, las pruebas de un nodo I2P realizadas por otros nodos les indicarán que no es accesible. Esto bloquea un nodo durante al menos 24 horas en otros nodos. Así, los otros nodos que probaron ese nodo como inactivo no utilizarán ese nodo durante 24 horas para construir túneles. Esta es la razón por la cual tu tráfico es menor después de un reinicio/apagado de tu router I2P durante un mínimo de 24 horas.

Además, otros nodos I2P necesitan conocer un router I2P para probar su alcance y capacidad. Este proceso puede acelerarse cuando interactúas con la red, por ejemplo utilizando aplicaciones o visitando sitios I2P, lo que resultará en más construcción de tunnels y por lo tanto más actividad y alcance para las pruebas por parte de los nodos en la red.

---

## Mejoras de Rendimiento

Para posibles mejoras de rendimiento futuras, consulta [Mejoras de Rendimiento Futuras](/docs/overview/performance#future).

Para ver mejoras de rendimiento anteriores, consulta el [Historial de Rendimiento](/docs/overview/performance#history).
