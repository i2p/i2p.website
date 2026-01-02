---
title: "Rendimiento"
description: "Rendimiento de la red I2P: cómo se comporta hoy, mejoras históricas e ideas para ajustes futuros"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Rendimiento de la Red I2P: Velocidad, Conexiones y Gestión de Recursos

La red I2P es completamente dinámica. Cada cliente es conocido por otros nodos y prueba localmente los nodos conocidos en cuanto a alcanzabilidad y capacidad. Solo los nodos alcanzables y capaces se guardan en una NetDB local. Durante el proceso de construcción de túneles, los mejores recursos se seleccionan de este conjunto para construir túneles. Debido a que las pruebas ocurren continuamente, el conjunto de nodos cambia. Cada nodo I2P conoce una parte diferente de la NetDB, lo que significa que cada router tiene un conjunto diferente de nodos I2P para ser utilizados en los túneles. Incluso si dos routers tienen el mismo subconjunto de nodos conocidos, las pruebas de alcanzabilidad y capacidad probablemente mostrarán resultados diferentes, ya que los otros routers podrían estar bajo carga justo cuando un router realiza las pruebas, pero estar libres cuando el segundo router las realiza.

Esto describe por qué cada nodo I2P tiene diferentes nodos para construir tunnels. Debido a que cada nodo I2P tiene una latencia y ancho de banda diferentes, los tunnels (que se construyen a través de esos nodos) tienen diferentes valores de latencia y ancho de banda. Y como cada nodo I2P tiene diferentes tunnels construidos, no hay dos nodos I2P que tengan los mismos conjuntos de tunnels.

Un servidor/cliente se conoce como un "destination" y cada destination tiene al menos un túnel de entrada y uno de salida. El valor predeterminado es 3 saltos por túnel. Esto suma 12 saltos (12 nodos I2P diferentes) para un viaje completo de ida y vuelta cliente → servidor → cliente.

Cada paquete de datos se envía a través de 6 otros nodos de I2P hasta llegar al servidor:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

y en el camino de regreso 6 nodos I2P diferentes:

servidor - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - cliente

El tráfico en la red necesita un ACK antes de enviar nuevos datos; necesita esperar hasta que un ACK regrese del servidor: enviar datos, esperar el ACK, enviar más datos, esperar el ACK. Como el RTT (Round Trip Time) se acumula de la latencia de cada nodo I2P individual y cada conexión en este viaje de ida y vuelta, usualmente toma 1–3 segundos hasta que un ACK regresa al cliente. Debido al diseño del transporte TCP e I2P, un paquete de datos tiene un tamaño limitado. Juntas, estas condiciones establecen un límite de ancho de banda máximo por tunnel de aproximadamente 20–50 kB/s. Sin embargo, si solo un salto en el tunnel tiene únicamente 5 kB/s de ancho de banda disponible, todo el tunnel queda limitado a 5 kB/s, independientemente de la latencia y otras limitaciones.

El cifrado, la latencia y cómo se construye un túnel lo hace bastante costoso en tiempo de CPU para construir un túnel. Es por esto que un destino solo tiene permitido tener un máximo de 6 túneles de entrada y 6 de salida para transportar datos. Con un máximo de 50 kB/s por túnel, un destino podría usar aproximadamente 300 kB/s de tráfico combinado (en realidad podría ser más si se usan túneles más cortos con anonimato bajo o nulo disponible). Los túneles usados se descartan cada 10 minutos y se construyen nuevos. Este cambio de túneles, y a veces clientes que se apagan o pierden su conexión a la red, a veces romperá túneles y conexiones. Un ejemplo de esto se puede ver en la Red IRC2P en pérdida de conexión (ping timeout) o al usar eepget.

Con un conjunto limitado de destinos y un conjunto limitado de túneles por destino, un nodo I2P solo utiliza un conjunto limitado de túneles a través de otros nodos I2P. Por ejemplo, si un nodo I2P es "hop1" en el pequeño ejemplo anterior, solo ve un túnel participante que se origina desde el cliente. Si sumamos toda la red I2P, solo un número bastante limitado de túneles participantes podría construirse con una cantidad limitada de ancho de banda en total. Si se distribuyen estos números limitados entre la cantidad de nodos I2P, solo hay una fracción del ancho de banda/capacidad disponible para su uso.

Para mantener el anonimato, un solo router no debería ser utilizado por toda la red para construir túneles. Si un router actúa como router de túnel para todos los nodos I2P, se convierte en un punto central de fallo muy real, así como en un punto central para recopilar IPs y datos de los clientes. Esta es la razón por la cual la red distribuye el tráfico entre nodos en el proceso de construcción de túneles.

Otra consideración para el rendimiento es la forma en que I2P maneja las redes en malla. Cada salto de conexión punto a punto utiliza una conexión TCP o UDP en los nodos I2P. Con 1000 conexiones, se observan 1000 conexiones TCP. Eso es bastante, y algunos routers domésticos y de pequeñas oficinas solo permiten un número pequeño de conexiones. I2P intenta limitar estas conexiones a menos de 1500 por tipo UDP y por tipo TCP. Esto limita también la cantidad de tráfico enrutado a través de un nodo I2P.

Si un nodo es alcanzable, tiene una configuración de ancho de banda de >128 kB/s compartido y está alcanzable 24/7, debería ser utilizado después de algún tiempo para tráfico participante. Si se cae en el ínterin, las pruebas de un nodo I2P realizadas por otros nodos les indicarán que no es alcanzable. Esto bloquea un nodo durante al menos 24 horas en otros nodos. Por lo tanto, los otros nodos que probaron ese nodo como caído no usarán ese nodo durante 24 horas para construir túneles. Es por esto que tu tráfico es menor después de un reinicio/apagado de tu router I2P durante un mínimo de 24 horas.

Además, otros nodos I2P necesitan conocer un router I2P para probarlo en cuanto a alcanzabilidad y capacidad. Este proceso puede acelerarse cuando interactúas con la red, por ejemplo, usando aplicaciones o visitando sitios I2P, lo que resultará en más construcción de túneles y, por lo tanto, más actividad y alcanzabilidad para las pruebas realizadas por los nodos en la red.

## Historial de Rendimiento (seleccionado)

A lo largo de los años, I2P ha experimentado una serie de mejoras de rendimiento notables:

### Native math

Implementado mediante enlaces JNI a la biblioteca GNU MP (GMP) para acelerar `modPow` de BigInteger, que anteriormente dominaba el tiempo de CPU. Los primeros resultados mostraron mejoras de velocidad dramáticas en criptografía de clave pública. Ver: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Anteriormente, las respuestas a menudo requerían una búsqueda en la base de datos de red del LeaseSet del remitente. Incluir el LeaseSet del remitente en el garlic inicial mejora la latencia de respuesta. Esto ahora se hace de forma selectiva (al inicio de una conexión o cuando cambia el LeaseSet) para reducir la sobrecarga.

### Matemáticas nativas

Se movieron algunos pasos de validación más temprano en el handshake de transporte para rechazar peers defectuosos antes (relojes incorrectos, NAT/firewall defectuoso, versiones incompatibles), ahorrando CPU y ancho de banda.

### Envolviendo con garlic un LeaseSet de "respuesta" (optimizado)

Utiliza pruebas de túneles según el contexto: evita probar túneles que ya se sabe que están transmitiendo datos; prioriza las pruebas cuando estén inactivos. Esto reduce la sobrecarga y acelera la detección de túneles con fallos.

### Rechazo de TCP más eficiente

Mantener las selecciones para una conexión determinada reduce la entrega fuera de orden y permite que la biblioteca de streaming aumente los tamaños de ventana, mejorando el rendimiento.

### Ajustes de prueba de túneles

GZip o similar para estructuras detalladas (por ejemplo, opciones de RouterInfo) reduce el ancho de banda cuando es apropiado.

### Selección persistente de túnel/lease

Reemplazo del protocolo simplista "ministreaming". El streaming moderno incluye ACKs selectivos y control de congestión adaptado al sustrato anónimo y orientado a mensajes de I2P. Ver: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

A continuación se presentan ideas documentadas históricamente como posibles mejoras. Muchas están obsoletas, implementadas o han sido reemplazadas por cambios arquitectónicos.

### Comprimir estructuras de datos seleccionadas

Mejorar cómo los routers eligen peers para la construcción de túneles para evitar aquellos lentos o sobrecargados, mientras se mantiene resistente a ataques Sybil por adversarios poderosos.

### Protocolo de streaming completo

Reduce la exploración innecesaria cuando el espacio de claves es estable; ajuste cuántos pares se devuelven en las búsquedas y cuántas búsquedas concurrentes se realizan.

### Session Tag tuning and improvements (legacy)

Para el esquema heredado ElGamal/AES+SessionTag, estrategias más inteligentes de expiración y reposición reducen los respaldos ElGamal y las etiquetas desperdiciadas.

### Mejor perfilado y selección de pares

Generar etiquetas desde un PRNG sincronizado inicializado durante el establecimiento de una nueva sesión, reduciendo la sobrecarga por mensaje de las etiquetas pre-entregadas.

### Ajuste de la base de datos de red

Tiempos de vida de túnel más largos combinados con recuperación pueden reducir los costos de reconstrucción; equilibrar con anonimato y confiabilidad.

### Ajustes y mejoras de Session Tag (obsoleto)

Rechazar peers inválidos más temprano y hacer las pruebas de túnel más conscientes del contexto para reducir la contención y la latencia.

### Migrar SessionTag a PRNG sincronizado (heredado)

El bundling selectivo de LeaseSet, las opciones comprimidas de RouterInfo y la adopción del protocolo de streaming completo contribuyen a un mejor rendimiento percibido.

---


Véase también:

- [Enrutamiento de Túneles](/docs/overview/tunnel-routing/)
- [Selección de Pares](/docs/overview/tunnel-routing/)
- [Transportes](/docs/overview/transport/)
- [Especificación SSU2](/docs/specs/ssu2/) y [Especificación NTCP2](/docs/specs/ntcp2/)
