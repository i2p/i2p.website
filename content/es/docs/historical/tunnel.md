---
title: "Discusión sobre Tunnels"
description: "Exploración histórica del relleno de túneles, fragmentación y estrategias de construcción"
slug: "tunnel"
aliases:
  - "/es/docs/discussions/tunnel"
  - "/es/docs/discussions/tunnel/"
  - "/es/tunnel_discussion"
  - "/es/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Nota: Este documento contiene información antigua sobre alternativas a la implementación actual de túneles en I2P, y especulaciones sobre posibilidades futuras. Para información actual consulta [la página de túneles](/docs/specs/tunnel-implementation).

Esa página documenta la implementación actual de construcción de tunnel a partir de la versión 0.6.1.10. El método anterior de construcción de tunnel, utilizado antes de la versión 0.6.1.10, está documentado en [la página de tunnel antigua](/docs/historical/tunnel-alt).

### Alternativas de Configuración {#config}

Más allá de su longitud, puede haber parámetros configurables adicionales para cada tunnel que se pueden usar, como una limitación en la frecuencia de entrega de mensajes, cómo se debe usar el relleno, cuánto tiempo debe estar en operación un tunnel, si se deben inyectar mensajes de relleno, y qué estrategias de agrupación, si las hay, se deben emplear. Ninguna de estas está implementada actualmente.

### Alternativas de Relleno {#tunnel.padding}

Son posibles varias estrategias de relleno de túnel, cada una con sus propios méritos:

- Sin relleno
- Relleno a un tamaño aleatorio
- Relleno a un tamaño fijo
- Relleno al KB más cercano
- Relleno al tamaño exponencial más cercano (2^n bytes)

Estas estrategias de relleno se pueden utilizar en varios niveles, abordando la exposición de información del tamaño de mensajes a diferentes adversarios. Después de recopilar y revisar algunas estadísticas de la red 0.4, así como explorar las compensaciones de anonimato, estamos comenzando con un tamaño fijo de mensaje de tunnel de 1024 bytes. Sin embargo, dentro de esto, los mensajes fragmentados en sí mismos no son rellenados por el tunnel en absoluto (aunque para mensajes de extremo a extremo, pueden ser rellenados como parte del empaquetado garlic).

### Alternativas de Fragmentación {#tunnel.fragmentation}

Para evitar que los adversarios etiqueten los mensajes a lo largo de la ruta ajustando el tamaño del mensaje, todos los mensajes de tunnel tienen un tamaño fijo de 1024 bytes. Para acomodar mensajes I2NP más grandes, así como para soportar los más pequeños de manera más eficiente, el gateway divide los mensajes I2NP más grandes en fragmentos contenidos dentro de cada mensaje de tunnel. El endpoint intentará reconstruir el mensaje I2NP a partir de los fragmentos durante un breve período de tiempo, pero los descartará según sea necesario.

Los routers tienen mucha libertad en cuanto a cómo se organizan los fragmentos, ya sea que se empaqueten de manera ineficiente como unidades discretas, se agrupen por un breve período para ajustar más carga útil en los mensajes de túnel de 1024 bytes, o se rellenen oportunísticamente con otros mensajes que el gateway quería enviar.

### Más Alternativas {#tunnel.alternatives}

#### Ajustar el Procesamiento de Túnel en Curso {#tunnel.reroute}

Aunque el algoritmo simple de enrutamiento de túneles debería ser suficiente para la mayoría de casos, hay tres alternativas que se pueden explorar:

- Hacer que un peer distinto al endpoint actúe temporalmente como el punto
  de terminación para un tunnel ajustando el cifrado utilizado en el gateway para darles
  el texto plano de los mensajes I2NP preprocesados. Cada peer podría verificar si
  tenía el texto plano, procesando el mensaje al recibirlo como si lo tuviera.
- Permitir que los routers que participan en un tunnel remezclen el mensaje antes
  de reenviarlo - rebotándolo a través de uno de los tunnels salientes de ese peer,
  llevando instrucciones para la entrega al siguiente salto.
- Implementar código para que el creador del tunnel redefina el "siguiente salto" de un peer en
  el tunnel, permitiendo una redirección dinámica adicional.

#### Usar Tunnels Bidireccionales {#tunnel.bidirectional}

La estrategia actual de usar dos tunnels separados para la comunicación entrante y saliente no es la única técnica disponible, y sí tiene implicaciones de anonimato. En el lado positivo, al usar tunnels separados se reduce los datos de tráfico expuestos para análisis a los participantes en un tunnel - por ejemplo, los peers en un tunnel saliente desde un navegador web solo verían el tráfico de una solicitud HTTP GET, mientras que los peers en un tunnel entrante verían la carga útil entregada a lo largo del tunnel. Con tunnels bidireccionales, todos los participantes tendrían acceso al hecho de que, por ejemplo, se envió 1KB en una dirección, luego 100KB en la otra. En el lado negativo, usar tunnels unidireccionales significa que hay dos conjuntos de peers que necesitan ser perfilados y contabilizados, y se debe tener cuidado adicional para abordar la velocidad incrementada de los ataques de predecesor. El proceso de agrupación y construcción de tunnels descrito a continuación debería minimizar las preocupaciones del ataque de predecesor, aunque si se deseara, no sería mucho problema construir tanto los tunnels entrantes como salientes a lo largo de los mismos peers.

#### Comunicación de Canal Trasero {#tunnel.backchannel}

En este momento, los valores IV utilizados son valores aleatorios. Sin embargo, es posible que ese valor de 16 bytes se use para enviar mensajes de control desde el gateway al endpoint, o en túneles salientes, desde el gateway a cualquiera de los peers. El gateway entrante podría codificar ciertos valores en el IV una vez, que el endpoint sería capaz de recuperar (ya que sabe que el endpoint también es el creador). Para túneles salientes, el creador podría entregar ciertos valores a los participantes durante la creación del túnel (ej. "si ves 0x0 como IV, eso significa X", "0x1 significa Y", etc). Dado que el gateway en el túnel saliente también es el creador, pueden construir un IV de modo que cualquiera de los peers reciba el valor correcto. El creador del túnel podría incluso dar al gateway del túnel entrante una serie de valores IV que ese gateway podría usar para comunicarse con participantes individuales exactamente una vez (aunque esto tendría problemas con respecto a la detección de colusión).

Esta técnica podría usarse más adelante para entregar mensajes a mitad del flujo, o para permitir que el gateway de entrada le diga al endpoint que está siendo víctima de un DoS o que de otra manera está a punto de fallar. Por el momento, no hay planes para aprovechar este canal de retorno.

#### Mensajes de Tunnel de Tamaño Variable {#tunnel.variablesize}

Mientras que la capa de transporte puede tener su propio tamaño de mensaje fijo o variable, utilizando su propia fragmentación, la capa de tunnel puede usar en su lugar mensajes de tunnel de tamaño variable. La diferencia es una cuestión de modelos de amenaza: un tamaño fijo en la capa de transporte ayuda a reducir la información expuesta a adversarios externos (aunque el análisis de flujo general aún funciona), pero para adversarios internos (es decir, participantes del tunnel) el tamaño del mensaje queda expuesto. Los mensajes de tunnel de tamaño fijo ayudan a reducir la información expuesta a los participantes del tunnel, pero no ocultan la información expuesta a los puntos finales y gateways del tunnel. Los mensajes de extremo a extremo de tamaño fijo ocultan la información expuesta a todos los peers de la red.

Como siempre, es una cuestión de contra quién está tratando de proteger I2P. Los mensajes de tunnel de tamaño variable son peligrosos, ya que permiten a los participantes usar el tamaño del mensaje en sí como un canal secundario hacia otros participantes - por ejemplo, si ves un mensaje de 1337 bytes, estás en el mismo tunnel que otro par en colusión. Incluso con un conjunto fijo de tamaños permitidos (1024, 2048, 4096, etc), ese canal secundario aún existe ya que los pares podrían usar la frecuencia de cada tamaño como portador (por ejemplo, dos mensajes de 1024 bytes seguidos de un 8192). Los mensajes más pequeños sí incurren en la sobrecarga de las cabeceras (IV, tunnel ID, porción hash, etc), pero los mensajes de tamaño fijo más grandes o aumentan la latencia (debido al agrupamiento) o aumentan dramáticamente la sobrecarga (debido al relleno). La fragmentación ayuda a amortizar la sobrecarga, a costa de la pérdida potencial de mensajes debido a fragmentos perdidos.

Los ataques de temporización también son relevantes al revisar la efectividad de los mensajes de tamaño fijo, aunque requieren una vista sustancial de los patrones de actividad de la red para ser efectivos. Los retrasos artificiales excesivos en el tunnel serán detectados por el creador del tunnel, debido a las pruebas periódicas, causando que todo ese tunnel sea desechado y que los perfiles de los peers dentro de él sean ajustados.

### Construyendo Alternativas {#tunnel.building.alternatives}

Referencia: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Método Antiguo de Construcción de Tunnel {#tunnel.building.old}

El método antiguo de construcción de túneles, utilizado antes de la versión 0.6.1.10, está documentado en [la página de túneles antiguos](/docs/historical/tunnel-alt). Este era un método "todo a la vez" o "paralelo", donde los mensajes se enviaban en paralelo a cada uno de los participantes.

#### Construcción Telescópica de Una Sola Vez {#tunnel.building.oneshot}

NOTA: Este es el método actual.

Una pregunta que surgió con respecto al uso de los túneles exploratorios para enviar y recibir mensajes de creación de túneles es cómo esto impacta la vulnerabilidad del túnel a ataques de predecesor. Mientras que los extremos y gateways de esos túneles estarán distribuidos aleatoriamente a través de la red (quizás incluso incluyendo al creador del túnel en ese conjunto), otra alternativa es usar las rutas de los túneles mismos para pasar la solicitud y respuesta, como se hace en [Tor](https://www.torproject.org/). Esto, sin embargo, puede llevar a filtraciones durante la creación del túnel, permitiendo que los peers descubran cuántos saltos hay más adelante en el túnel monitoreando el tiempo o el conteo de paquetes mientras se construye el túnel.

#### Construcción Telescópica "Interactiva" {#tunnel.building.telescoping}

Construye los saltos uno a la vez con un mensaje a través de la parte existente del tunnel para cada uno. Tiene problemas importantes ya que los peers pueden contar los mensajes para determinar su ubicación en el tunnel.

#### Túneles no exploratorios para gestión {#tunnel.building.nonexploratory}

Una segunda alternativa al proceso de construcción de tunnels es proporcionar al router un conjunto adicional de pools de entrada y salida no exploratorios, utilizándolos para la solicitud y respuesta del tunnel. Asumiendo que el router tiene una vista bien integrada de la red, esto no debería ser necesario, pero si el router estuviera particionado de alguna manera, usar pools no exploratorios para la gestión de tunnels reduciría la filtración de información sobre qué peers están en la partición del router.

#### Entrega de Solicitud Exploratoria {#tunnel.building.exploratory}

Una tercera alternativa, utilizada hasta I2P 0.6.1.10, encripta con garlic encryption los mensajes individuales de solicitud de tunnel y los entrega a los saltos individualmente, transmitiéndolos a través de tunnels exploratorios con su respuesta regresando en un tunnel exploratorio separado. Esta estrategia ha sido abandonada en favor de la descrita anteriormente.

#### Más Historia y Discusión {#history}

Antes de la introducción del Mensaje de Construcción de Túnel Variable, había al menos dos problemas:

1. El tamaño de los mensajes (causado por un máximo de 8 saltos, cuando la longitud típica del tunnel es de 2 o 3 saltos...
   y la investigación actual indica que más de 3 saltos no mejora el anonimato);
2. La alta tasa de fallos de construcción, especialmente para tunnels largos (y exploratorios), ya que todos los saltos deben estar de acuerdo o el tunnel es descartado.

El VTBM ha solucionado el #1 y mejorado el #2.

Welterde ha propuesto modificaciones al método paralelo para permitir la reconfiguración. Sponge ha propuesto usar 'tokens' de algún tipo.

Cualquier estudiante de construcción de túneles debe estudiar el registro histórico que llevó al método actual, especialmente las diversas vulnerabilidades de anonimato que pueden existir en varios métodos. Los archivos de correo de octubre de 2005 son particularmente útiles. Como se indica en [la especificación de creación de túneles](/docs/specs/tunnel-creation), la estrategia actual surgió durante una discusión en la lista de correo de I2P entre Michael Rogers, Matthew Toseland (toad) y jrandom sobre el ataque predecesor.

#### Alternativas de Ordenamiento de Pares {#ordering}

También es posible un ordenamiento menos estricto, asegurando que aunque el salto después de A puede ser B, B nunca puede estar antes de A. Otras opciones de configuración incluyen la capacidad de que solo las puertas de enlace de túneles de entrada y los puntos finales de túneles de salida sean fijos, o rotados según una tasa MTBF.

## Mezcla/Agrupamiento {#tunnel.mixing}

¿Qué estrategias se deben usar en el gateway y en cada hop para retrasar, reordenar, rerutar o rellenar mensajes? ¿Hasta qué punto esto se debe hacer automáticamente, cuánto se debe configurar como una configuración por tunnel o por hop, y cómo debe controlar el creador del tunnel (y a su vez, el usuario) esta operación? Todo esto se deja como desconocido, para ser resuelto en una versión futura.
