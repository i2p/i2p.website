---
title: "Discusión sobre NTCP"
description: "Discusión histórica sobre los protocolos de transporte NTCP vs SSU de marzo de 2007"
slug: "ntcp-discussion"
aliases:
  - "/es/docs/discussions/ntcp"
  - "/es/docs/discussions/ntcp/"
  - "/es/ntcp_discussion"
  - "/es/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Lo siguiente es una discusión sobre NTCP que tuvo lugar en marzo de 2007. No ha sido actualizada para reflejar la implementación actual. Para la especificación actual de NTCP consulta [la página de NTCP2](/docs/specs/ntcp2).

## Discusión NTCP vs. SSU, Marzo 2007 {#ntcp-ssu}

### Preguntas sobre NTCP

(adaptado de una discusión de IRC entre zzz y cervantes)

¿Por qué se prefiere NTCP sobre SSU, no tiene NTCP mayor sobrecarga y latencia? Tiene mejor confiabilidad.

¿No sufre la biblioteca de streaming sobre NTCP de los problemas clásicos de TCP-sobre-TCP? ¿Qué pasaría si tuviéramos un transporte UDP realmente simple para el tráfico originado por streaming-lib? Creo que SSU estaba destinado a ser el llamado transporte UDP realmente simple, pero resultó ser demasiado poco confiable.

### Análisis "NTCP Considerado Perjudicial" por zzz {#harmful}

Publicado en el nuevo Syndie, 2007-03-25. Esto se publicó para estimular la discusión, no te lo tomes demasiado en serio.

**Resumen:** NTCP tiene mayor latencia y sobrecarga que SSU, y es más probable que colapse cuando se usa con la biblioteca de streaming. Sin embargo, el tráfico se enruta con preferencia por NTCP sobre SSU y esto está actualmente codificado de forma fija.

#### Discusión

Actualmente tenemos dos transportes, NTCP y SSU. Tal como están implementados actualmente, NTCP tiene "ofertas" más bajas que SSU por lo que se prefiere, excepto en el caso donde existe una conexión SSU establecida pero no hay una conexión NTCP establecida para un peer.

SSU es similar a NTCP en que implementa confirmaciones de recibo, tiempos de espera y retransmisiones. Sin embargo, SSU es código de I2P con restricciones estrictas en los tiempos de espera y estadísticas disponibles sobre tiempos de ida y vuelta, retransmisiones, etc. NTCP está basado en Java NIO TCP, que es una caja negra y presumiblemente implementa estándares RFC, incluyendo tiempos de espera máximos muy largos.

La mayoría del tráfico dentro de I2P se origina en streaming-lib (HTTP, IRC, Bittorrent) que es nuestra implementación de TCP. Como el transporte de nivel inferior es generalmente NTCP debido a las ofertas más bajas, el sistema está sujeto al conocido y temido problema de TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , donde tanto las capas superiores como inferiores de TCP están realizando retransmisiones al mismo tiempo, llevando al colapso.

A diferencia del escenario de PPP sobre SSH descrito en el enlace anterior, tenemos varios saltos para la capa inferior, cada uno cubierto por un enlace NTCP. Por lo tanto, cada latencia NTCP es generalmente mucho menor que la latencia de la biblioteca de streaming de capa superior. Esto reduce las posibilidades de colapso.

Además, las probabilidades de colapso se reducen cuando el TCP de capa inferior está estrictamente limitado con timeouts bajos y un número reducido de retransmisiones en comparación con la capa superior.

La versión .28 aumentó el tiempo de espera máximo de la biblioteca de streaming de 10 seg a 45 seg, lo que mejoró mucho las cosas. El tiempo de espera máximo de SSU es de 3 seg. El tiempo de espera máximo de NTCP es presumiblemente de al menos 60 seg, que es la recomendación RFC. No hay forma de cambiar los parámetros de NTCP o monitorear el rendimiento. El colapso de la capa NTCP es [editor: texto perdido]. Quizás una herramienta externa como tcpdump podría ayudar.

Sin embargo, al ejecutar .28, el upstream reportado por i2psnark generalmente no se mantiene en un nivel alto. A menudo baja a 3-4 KBps antes de volver a subir. Esto es una señal de que aún hay colapsos.

SSU también es más eficiente. NTCP tiene mayor sobrecarga y probablemente tiempos de ida y vuelta más altos. Al usar NTCP, la proporción de (salida del tunnel) / (salida de datos de i2psnark) es de al menos 3.5 : 1. Al ejecutar un experimento donde se modificó el código para preferir SSU (la opción de configuración i2np.udp.alwaysPreferred no tiene efecto en el código actual), la proporción se redujo a aproximadamente 3 : 1, indicando mejor eficiencia.

Según informan las estadísticas de la biblioteca de streaming, las cosas mejoraron considerablemente: el tamaño de ventana de por vida aumentó de 6.3 a 7.5, el RTT disminuyó de 11.5s a 10s, y los envíos por ack bajaron de 1.11 a 1.07.

Que esto fuera tan efectivo fue sorprendente, dado que solo estábamos cambiando el transporte para el primero de los 3 a 5 hops totales que tomarían los mensajes salientes.

El efecto en las velocidades de salida de i2psnark no estaba claro debido a variaciones normales. También para el experimento, se deshabilitó el NTCP de entrada. El efecto en las velocidades de entrada en i2psnark no estaba claro.

#### Propuestas

1. **1A)** Esto es fácil -
   Deberíamos invertir las prioridades de oferta para que SSU sea preferido para todo el tráfico, si
   podemos hacer esto sin causar todo tipo de otros problemas. Esto arreglará la
   opción de configuración i2np.udp.alwaysPreferred para que funcione (ya sea como verdadero
   o falso).

2. **1B)** Alternativa a 1A), no tan fácil -
   Si podemos marcar el tráfico sin afectar negativamente nuestros objetivos de anonimato,
   deberíamos identificar el tráfico generado por streaming-lib y hacer que SSU genere una oferta baja
   para ese tráfico. Esta etiqueta tendrá que ir con el mensaje a través de cada salto
   para que los routers de reenvío también respeten la preferencia de SSU.

3. **2)** Limitar SSU aún más (reduciendo las retransmisiones máximas desde las 10 actuales) probablemente sea prudente para reducir la posibilidad de colapso.

4. **3)** Necesitamos más estudios sobre los beneficios vs. daños de un protocolo semi-confiable
   debajo de la biblioteca de streaming. ¿Son las retransmisiones sobre un solo salto beneficiosas
   y una gran ventaja o son peores que inútiles?
   Podríamos hacer un nuevo SUU (UDP no confiable seguro) pero probablemente no valga la pena. 
   Podríamos quizás agregar un tipo de mensaje sin-ack-requerido en SSU si no queremos ninguna
   retransmisión en absoluto del tráfico de streaming-lib. ¿Son deseables las
   retransmisiones estrictamente acotadas?

5. **4)** El código de envío con prioridad en .28 es solo para NTCP. Hasta ahora mis pruebas no han mostrado mucha utilidad para las prioridades SSU ya que los mensajes no se acumulan en cola el tiempo suficiente para que las prioridades sean útiles. Pero se necesitan más pruebas.

6. **5)** El nuevo timeout máximo de la librería de streaming de 45s probablemente sigue siendo demasiado bajo.
   El RFC de TCP dice 60s. Probablemente no debería ser más corto que el timeout máximo subyacente de NTCP (presumiblemente 60s).

### Respuesta de jrandom {#jrandom-response}

Publicado en nuevo Syndie, 2007-03-27

En general, estoy dispuesto a experimentar con esto, aunque recuerda por qué está NTCP en primer lugar: SSU falló en un colapso de congestión. NTCP "simplemente funciona", y aunque las tasas de retransmisión del 2-10% se pueden manejar en redes normales de un solo salto, eso nos da una tasa de retransmisión del 40% con túneles de 2 saltos. Si incluyes algunas de las tasas de retransmisión de SSU medidas que vimos antes de que se implementara NTCP (10-30+%), eso nos da una tasa de retransmisión del 83%. Quizás esas tasas fueron causadas por el bajo timeout de 10 segundos, pero aumentar tanto nos afectaría (recuerda, multiplica por 5 y tienes la mitad del recorrido).

A diferencia de TCP, no tenemos retroalimentación del tunnel para saber si el mensaje llegó - no hay confirmaciones a nivel de tunnel. Sí tenemos confirmaciones de extremo a extremo, pero solo en un pequeño número de mensajes (cada vez que distribuimos nuevas etiquetas de sesión) - de los 1,553,591 mensajes de cliente que envió mi router, solo intentamos confirmar 145,207 de ellos. Los otros pueden haber fallado silenciosamente o haber tenido éxito perfectamente.

No estoy convencido por el argumento de TCP-sobre-TCP para nosotros, especialmente dividido entre las diversas rutas por las que transferimos. Las mediciones en I2P pueden convencerme de lo contrario, por supuesto.

> *El tiempo de espera máximo de NTCP es presumiblemente de al menos 60 segundos, que es la recomendación del RFC. No hay manera de cambiar los parámetros de NTCP o monitorear el rendimiento.*

Cierto, pero las conexiones de red solo llegan a ese nivel cuando algo realmente malo está ocurriendo - el tiempo de espera de retransmisión en TCP a menudo está en el orden de decenas o cientos de milisegundos. Como señala foofighter, tienen más de 20 años de experiencia y corrección de errores en sus stacks TCP, además de una industria de miles de millones de dólares optimizando hardware y software para funcionar bien según lo que sea que hagan.

> *NTCP tiene mayor sobrecarga y probablemente mayores tiempos de ida y vuelta. cuando se usa NTCP > la proporción de (salida del tunnel) / (salida de datos de i2psnark) es de al menos 3.5 : 1. > Ejecutando un experimento donde el código fue modificado para preferir SSU (la opción de > configuración i2np.udp.alwaysPreferred no tiene efecto en el código actual), la proporción > se redujo a aproximadamente 3 : 1, indicando mejor eficiencia.*

Estos son datos muy interesantes, aunque más como una cuestión de congestión del router que de eficiencia del ancho de banda - tendrías que comparar 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct. Este punto de datos sugiere que hay algo en el router que lleva a un exceso de cola local de mensajes que ya están siendo transferidos.

> *tamaño de ventana de tiempo de vida aumentado de 6.3 a 7.5, RTT reducido de 11.5s a 10s, envíos por > ACK reducidos de 1.11 a 1.07.*

Recuerda que los envíos por ACK es solo una muestra, no un conteo completo (ya que no intentamos hacer ACK de cada envío). Tampoco es una muestra aleatoria, sino que muestrea más intensamente los períodos de inactividad o el inicio de una ráfaga de actividad - la carga sostenida no requerirá muchos ACKs.

Los tamaños de ventana en ese rango siguen siendo lamentablemente bajos para obtener el beneficio real de AIMD, y aún demasiado bajos para transmitir un solo fragmento BT de 32KB (aumentar el mínimo a 10 o 12 cubriría eso).

Aún así, la estadística wsize parece prometedora - ¿durante cuánto tiempo se mantuvo eso?

En realidad, para propósitos de prueba, es posible que quieras revisar StreamSinkClient/StreamSinkServer o incluso TestSwarm en apps/ministreaming/java/src/net/i2p/client/streaming/ - StreamSinkClient es una aplicación CLI que envía un archivo seleccionado a un destino seleccionado y StreamSinkServer crea un destino y escribe cualquier dato que se le envíe (mostrando el tamaño y tiempo de transferencia). TestSwarm combina ambos - enviando datos aleatorios masivamente a quien se conecte. Eso debería darte las herramientas para medir la capacidad de rendimiento sostenido a través de la streaming lib, en contraste con el choke/send de BT.

> *1A) Esto es fácil - > Deberíamos cambiar las prioridades de oferta para que SSU sea preferido para todo el tráfico, si > podemos hacer esto sin causar todo tipo de otros problemas. Esto arreglará la > opción de configuración i2np.udp.alwaysPreferred para que funcione (ya sea como true > o false).*

Respetar i2np.udp.alwaysPreferred es una buena idea en cualquier caso - siéntete libre de confirmar ese cambio. Sin embargo, reunamos un poco más de datos antes de cambiar las preferencias, ya que NTCP fue añadido para lidiar con un colapso de congestión creado por SSU.

> *1B) Alternativa a 1A), no tan fácil - > Si podemos marcar el tráfico sin afectar negativamente nuestros objetivos de anonimato, > deberíamos identificar el tráfico generado por streaming-lib > y hacer que SSU genere una oferta baja para ese tráfico. Esta etiqueta tendrá que ir con > el mensaje a través de cada salto > para que los routers de reenvío también respeten la preferencia SSU.*

En la práctica, existen tres tipos de tráfico: construcción/prueba de túneles, consulta/respuesta de netDb, y tráfico de la biblioteca de streaming. La red ha sido diseñada para hacer muy difícil diferenciar estos tres tipos.

> *2) Limitar SSU aún más (reduciendo las retransmisiones máximas de las actuales > 10) probablemente sea prudente para reducir la posibilidad de colapso.*

Con 10 retransmisiones, ya estamos jodidos, estoy de acuerdo. Una, tal vez dos retransmisiones es razonable, desde una capa de transporte, pero si el otro lado está demasiado congestionado para enviar ACK a tiempo (incluso con la capacidad SACK/NACK implementada), no hay mucho que podamos hacer.

En mi opinión, para abordar realmente el problema central necesitamos abordar por qué el router se congestiona tanto como para no poder hacer ACK a tiempo (lo cual, por lo que he encontrado, se debe a la contención de CPU). ¿Tal vez podemos reorganizar algunas cosas en el procesamiento del router para hacer que la transmisión de un tunnel ya existente tenga mayor prioridad de CPU que descifrar una nueva solicitud de tunnel? Aunque tenemos que tener cuidado de evitar la inanición.

> *3) Necesitamos más estudio sobre los beneficios vs. los perjuicios de un protocolo semi-confiable > debajo de la biblioteca de streaming. ¿Son las retransmisiones sobre un solo salto beneficiosas > y una gran ventaja o son peores que inútiles? > Podríamos hacer un nuevo SUU (UDP no confiable seguro) pero probablemente no vale la pena. > Podríamos quizás agregar un tipo de mensaje sin-ACK-requerido en SSU si no queremos ninguna > retransmisión en absoluto del tráfico de la biblioteca de streaming. ¿Son deseables las > retransmisiones estrictamente limitadas?*

Vale la pena investigar - ¿qué pasaría si simplemente deshabilitáramos las retransmisiones de SSU? Probablemente llevaría a tasas de reenvío mucho más altas en la biblioteca de streaming, pero tal vez no.

> *4) El código de envío por prioridad en .28 es solo para NTCP. Hasta ahora mis pruebas no han mostrado mucha utilidad para la prioridad SSU ya que los mensajes no se encolan lo suficiente como para que las prioridades sean útiles. Pero se necesitan más pruebas.*

Existe UDPTransport.PRIORITY_LIMITS y UDPTransport.PRIORITY_WEIGHT (respetado por TimedWeightedPriorityMessageQueue), pero actualmente los pesos son casi todos iguales, por lo que no hay efecto. Eso podría ajustarse, por supuesto (pero como mencionas, si no hay cola de espera, no importa).

> *5) El nuevo tiempo máximo de espera de la biblioteca de streaming de 45s probablemente sigue siendo muy bajo. El RFC de TCP dice 60s. Probablemente no debería ser más corto que el tiempo máximo de espera subyacente de NTCP (presumiblemente 60s).*

Esos 45s son el timeout máximo de retransmisión de la librería de streaming, no el timeout del stream. TCP en la práctica tiene timeouts de retransmisión órdenes de magnitud menores, aunque sí, puede llegar a 60s en enlaces que pasan por cables expuestos o transmisiones satelitales ;) Si aumentáramos el timeout de retransmisión de la librería de streaming a, por ejemplo, 75 segundos, podríamos ir por una cerveza antes de que cargue una página web (especialmente asumiendo menos de un 98% de transporte confiable). Esa es una razón por la que preferimos NTCP.

### Respuesta de zzz {#zzz-response}

Publicado en nuevo Syndie, 2007-03-31

> *Con 10 retransmisiones, ya estamos jodidos, estoy de acuerdo. Una, tal vez dos > retransmisiones es razonable, desde la capa de transporte, pero si el otro lado está > demasiado congestionado para hacer ACK a tiempo (incluso con la capacidad SACK/NACK implementada), > no hay mucho que podamos hacer.* > > *En mi opinión, para realmente abordar el problema central necesitamos abordar por qué el > router se congestiona tanto como para no hacer ACK a tiempo (lo cual, por lo que he encontrado, se debe a > la contención de CPU). ¿Tal vez podamos reorganizar algunas cosas en el procesamiento del router para > hacer que la transmisión de un tunnel ya existente tenga mayor prioridad de CPU que > descifrar una nueva solicitud de tunnel? Aunque debemos tener cuidado de evitar > la inanición.*

Una de mis principales técnicas de recopilación de estadísticas es activar net.i2p.client.streaming.ConnectionPacketHandler=DEBUG y observar los tiempos RTT y los tamaños de ventana mientras pasan. Para generalizar demasiado por un momento, es común ver 3 tipos de conexiones: RTT de ~4s, RTT de ~10s, y RTT de ~30s. El objetivo es intentar reducir las conexiones con RTT de 30s. Si la contención de CPU es la causa, entonces tal vez algo de malabarismo lo resuelva.

Reducir el máximo de retransmisiones SSU de 10 es realmente solo un intento a ciegas ya que no tenemos buenos datos sobre si estamos colapsando, teniendo problemas de TCP-sobre-TCP, o qué, así que se necesitan más datos.

> *Vale la pena investigar - ¿qué pasaría si simplemente deshabilitáramos las retransmisiones de SSU? Probablemente conduciría a tasas de reenvío mucho más altas en la biblioteca de streaming, pero tal vez no.*

Lo que no entiendo, si pudieras elaborar, son los beneficios de las retransmisiones SSU para tráfico que no es de streaming-lib. ¿Necesitamos que los mensajes de tunnel (por ejemplo) usen un transporte semi-confiable o pueden usar un transporte no confiable o algo-así-como-confiable (1 o 2 retransmisiones máximo, por ejemplo)? En otras palabras, ¿por qué semi-confiabilidad?

> *(pero como mencionas, si no hay cola, no importa).*

Implementé el envío prioritario para UDP pero se activó unas 100,000 veces menos frecuentemente que el código del lado NTCP. Tal vez eso sea una pista para investigar más o una señal - no entiendo por qué se acumularía tanto más a menudo en NTCP, pero quizás eso sea una pista sobre por qué NTCP tiene peor rendimiento.

### Pregunta respondida por jrandom {#jrandom-followup}

Publicado en el nuevo Syndie, 2007-03-31

> *tasas de retransmisión SSU medidas que vimos antes de que NTCP fuera implementado > (10-30+%)* > > ¿Puede el router medir esto por sí mismo? Si es así, ¿podría seleccionarse un transporte basado > en el rendimiento medido? (es decir, si una conexión SSU a un peer está perdiendo un > número excesivo de mensajes, preferir NTCP al enviar a ese peer)

Sí, actualmente usa esa estadística como una detección de MTU rudimentaria (si la tasa de retransmisión es alta, usa el tamaño de paquete pequeño, pero si es baja, usa el tamaño de paquete grande). Probamos algunas cosas cuando introdujimos NTCP por primera vez (y cuando nos alejamos por primera vez del transporte TCP original) que prefería SSU pero fallaba fácilmente ese transporte para un peer, causando que recurriera a NTCP. Sin embargo, ciertamente se podría hacer más en ese sentido, aunque se complica rápidamente (cómo/cuándo ajustar/restablecer las ofertas, si compartir estas preferencias entre múltiples peers o no, si compartirlo entre múltiples sesiones con el mismo peer (y por cuánto tiempo), etc.).

### Respuesta por foofighter {#foofighter}

Publicado en el nuevo Syndie, 2007-03-26

Si he entendido las cosas correctamente, la razón principal a favor de TCP (en general, tanto la variedad antigua como la nueva) era que no necesitas preocuparte por codificar una buena pila TCP. Lo cual no es imposiblemente difícil de hacer bien... solo que las pilas TCP existentes tienen una ventaja de 20 años.

Que yo sepa, no ha habido mucha teoría profunda detrás de la preferencia de TCP versus UDP, excepto las siguientes consideraciones:

- Una red solo TCP es muy dependiente de peers alcanzables (aquellos que pueden reenviar conexiones entrantes a través de su NAT)
- Aún así, incluso si los peers alcanzables son escasos, que tengan alta capacidad alivia en cierta medida los problemas de escasez topológica
- UDP permite "NAT hole punching" que permite a las personas ser "pseudo-alcanzables" (con la ayuda de introducers) que de otro modo solo podrían conectar hacia afuera
- La implementación de transporte TCP "antigua" requería muchos hilos, lo cual era un asesino del rendimiento, mientras que el transporte TCP "nuevo" funciona bien con pocos hilos
- Los routers del conjunto A fallan cuando se saturan con UDP. Los routers del conjunto B fallan cuando se saturan con TCP.
- "Se siente" (es decir, hay algunas indicaciones pero no datos científicos o estadísticas de calidad) que A está más ampliamente desplegado que B
- Algunas redes transportan datagramas UDP no-DNS con una calidad francamente pésima, mientras aún se molestan en transportar flujos TCP.

Teniendo esto en cuenta, una pequeña diversidad de transportes (tantos como sean necesarios, pero no más) parece sensata en cualquier caso. Cuál debería ser el transporte principal depende de su rendimiento. He visto cosas desagradables en mi línea cuando traté de usar su capacidad completa con UDP. Pérdidas de paquetes del orden del 35%.

Definitivamente podríamos intentar jugar con las prioridades de UDP versus TCP, pero recomendaría cautela en eso. Recomendaría que no se cambien de manera demasiado radical de una vez, o podría romper cosas.

### Respuesta de zzz (a foofighter) {#zzz-foofighter}

Publicado en nuevo Syndie, 2007-03-27

> *Por lo que sé, no ha habido mucha teoría profunda detrás de la preferencia de TCP versus UDP, excepto las siguientes consideraciones:*

Estos son todos puntos válidos. Sin embargo, estás considerando los dos protocolos de forma aislada, en lugar de pensar en qué protocolo de transporte es mejor para un protocolo de nivel superior en particular (es decir, streaming lib o no).

Lo que estoy diciendo es que tienes que tomar en consideración la biblioteca de streaming.

Así que o bien cambiar las preferencias para todos o tratar el tráfico de la biblioteca de streaming de manera diferente.

De eso es de lo que habla mi propuesta 1B) - tener una preferencia diferente para el tráfico de streaming-lib que para el tráfico que no es de streaming-lib (por ejemplo, mensajes de construcción de túneles).

> *En ese contexto, una pequeña diversidad de transportes (tantos como sean necesarios, pero no más) parece sensato en cualquier caso. Cuál debería ser el transporte principal depende de su rendimiento. He visto cosas desagradables en mi línea cuando intenté usar su capacidad completa con UDP. Pérdidas de paquetes del orden del 35%.*

De acuerdo. La nueva versión .28 puede haber mejorado las cosas para la pérdida de paquetes sobre UDP, o tal vez no.

Un punto importante: el código de transporte sí recuerda los fallos de un transporte. Así que si UDP es el transporte preferido, lo intentará primero, pero si falla para un destino particular, en el siguiente intento para ese destino probará NTCP en lugar de intentar UDP nuevamente.

> *Definitivamente podríamos intentar experimentar con las prioridades de UDP versus TCP, pero recomendaría > precaución en eso. Instaría a que no se cambien demasiado radicalmente todo de > una vez, o podría romper cosas.*

Tenemos cuatro controles de ajuste - los cuatro valores de oferta (SSU y NTCP, para ya conectados y no-ya-conectados). Podríamos hacer que SSU sea preferido sobre NTCP solo si ambos están conectados, por ejemplo, pero intentar NTCP primero si ningún transporte está conectado.

La otra forma de hacerlo gradualmente es cambiar solo el tráfico de la biblioteca de streaming (la propuesta 1B), sin embargo eso podría ser difícil y puede tener implicaciones de anonimato, no lo sé. O tal vez cambiar el tráfico solo para el primer salto de salida (es decir, no propagar la bandera al siguiente router), lo cual te da solo un beneficio parcial pero podría ser más anónimo y más fácil.

## Resultados de la Discusión {#results}

... y otros cambios relacionados en el mismo período de tiempo (2007):

- Se implementó un ajuste significativo de los parámetros de la librería de streaming,
  aumentando enormemente el rendimiento de salida, en la versión 0.6.1.28
- El envío con prioridad para NTCP se implementó en la versión 0.6.1.28
- El envío con prioridad para SSU fue implementado por zzz pero nunca se registró
- El control avanzado de ofertas de transporte
  i2np.udp.preferred se implementó en la versión 0.6.1.29.
- El pushback para NTCP se implementó en la versión 0.6.1.30, se deshabilitó en la 0.6.1.31 debido a preocupaciones de anonimato,
  y se volvió a habilitar con mejoras para abordar esas preocupaciones en la 0.6.1.32.
- Ninguna de las propuestas 1-5 de zzz ha sido implementada.
