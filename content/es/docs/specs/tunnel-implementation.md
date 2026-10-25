---
title: "Implementación de Tunnel"
description: "Especificación de la operación, construcción y procesamiento de mensajes de túneles I2P"
slug: "tunnel-implementation"
aliases:
  - "/es/docs/specs/implementation"
  - "/es/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Esta página documenta la implementación actual de tunnel.

## Resumen de Tunnels {#tunnel.overview}

Dentro de I2P, los mensajes se transmiten en una dirección a través de un túnel virtual de pares, utilizando cualquier medio disponible para pasar el mensaje al siguiente salto. Los mensajes llegan al *gateway* del túnel, se agrupan y/o fragmentan en mensajes de túnel de tamaño fijo, y se reenvían al siguiente salto en el túnel, que procesa y verifica la validez del mensaje y lo envía al siguiente salto, y así sucesivamente, hasta que alcanza el endpoint del túnel. Ese *endpoint* toma los mensajes agrupados por el gateway y los reenvía según las instrucciones - ya sea a otro router, a otro túnel en otro router, o localmente.

Todos los tunnels funcionan de la misma manera, pero pueden segmentarse en dos grupos diferentes: tunnels de entrada y tunnels de salida. Los tunnels de entrada tienen un gateway no confiable que pasa mensajes hacia abajo hacia el creador del tunnel, que sirve como el endpoint del tunnel. Para los tunnels de salida, el creador del tunnel sirve como el gateway, pasando mensajes hacia el endpoint remoto.

El creador del tunnel selecciona exactamente qué peers participarán en el tunnel, y proporciona a cada uno los datos de configuración necesarios. Pueden tener cualquier número de saltos. La intención es hacer difícil tanto para los participantes como para terceros determinar la longitud de un tunnel, o incluso para participantes que colaboren determinar si forman parte del mismo tunnel (salvo en la situación donde peers que colaboran estén uno al lado del otro en el tunnel).

En la práctica, se utiliza una serie de grupos de tunnels para diferentes propósitos: cada destino de cliente local tiene su propio conjunto de tunnels de entrada y tunnels de salida, configurados para satisfacer sus necesidades de anonimato y rendimiento. Además, el router en sí mantiene una serie de grupos para participar en la base de datos de red y para gestionar los tunnels.

I2P es una red inherentemente de conmutación de paquetes, incluso con estos tunnels, lo que le permite aprovechar múltiples tunnels ejecutándose en paralelo, aumentando la resistencia y equilibrando la carga. Fuera de la capa central de I2P, hay una biblioteca de streaming de extremo a extremo opcional disponible para aplicaciones cliente, que expone operaciones similares a TCP, incluyendo reordenamiento de mensajes, retransmisión, control de congestión, etc.

Una descripción general de la terminología de tunnel de I2P está [en la página de descripción general de tunnels](/docs/overview/tunnel-routing).

## Operación de Tunnel (Procesamiento de Mensajes) {#tunnel.operation}

### Resumen

Después de que se construye un tunnel, los [mensajes I2NP](/docs/specs/i2np) son procesados y pasados a través de él. La operación del tunnel tiene cuatro procesos distintos, realizados por varios peers en el tunnel.

1. Primero, el gateway del tunnel acumula un número
   de mensajes I2NP y los preprocesa en mensajes de tunnel para
   su entrega.
2. A continuación, ese gateway cifra esos datos preprocesados, luego
   los reenvía al primer salto.
3. Ese par, y los subsecuentes
   participantes del tunnel, desenvuelven una capa del cifrado, verificando que no sea
   un duplicado, luego lo reenvían al siguiente par.
4. Finalmente, los mensajes del tunnel llegan al punto final donde los mensajes I2NP
   originalmente agrupados por el gateway son reensamblados y reenviados según
   se solicitó.

Los participantes intermedios del tunnel no saben si están en un tunnel de entrada o de salida; siempre "cifran" para el siguiente salto. Por lo tanto, aprovechamos el cifrado AES simétrico para "descifrar" en la puerta de enlace del tunnel de salida, de modo que el texto plano se revele en el punto final de salida.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Procesamiento de Gateway {#tunnel.gateway}

#### Preprocesamiento de Mensajes {#tunnel.preprocessing}

La función de un tunnel gateway es fragmentar y empaquetar [mensajes I2NP](/docs/specs/i2np) en [mensajes de tunnel](/docs/specs/tunnel-message) de tamaño fijo y cifrar los mensajes de tunnel. Los mensajes de tunnel contienen lo siguiente:

- Un Tunnel ID de 4 bytes
- Un IV (vector de inicialización) de 16 bytes
- Un checksum
- Relleno, si es necesario
- Uno o más pares { instrucción de entrega, fragmento de mensaje I2NP }

Los IDs de tunnel son números de 4 bytes utilizados en cada salto - los participantes saben qué ID de tunnel deben escuchar para recibir mensajes y qué ID de tunnel deben usar para reenviarlos al siguiente salto, y cada salto elige el ID de tunnel en el que recibe mensajes. Los tunnels en sí mismos tienen una duración corta (10 minutos). Incluso si tunnels posteriores se construyen usando la misma secuencia de peers, el ID de tunnel de cada salto cambiará.

Para prevenir que los adversarios marquen los mensajes a lo largo de la ruta ajustando el tamaño del mensaje, todos los mensajes de tunnel tienen un tamaño fijo de 1024 bytes. Para acomodar mensajes I2NP más grandes así como para soportar los más pequeños de manera más eficiente, el gateway divide los mensajes I2NP más grandes en fragmentos contenidos dentro de cada mensaje de tunnel. El endpoint intentará reconstruir el mensaje I2NP a partir de los fragmentos durante un período corto de tiempo, pero los descartará según sea necesario.

Los detalles están en la [especificación de mensajes de tunnel](/docs/specs/tunnel-message).

### Cifrado de Gateway

Después del preprocesamiento de los mensajes en una carga útil con relleno, el gateway construye un valor IV aleatorio de 16 bytes, lo cifra iterativamente junto con el mensaje del tunnel según sea necesario, y reenvía la tupla {tunnelID, IV, mensaje del tunnel cifrado} al siguiente salto.

Cómo se realiza el cifrado en el gateway depende de si el tunnel es de entrada o de salida. Para tunnels de entrada, simplemente seleccionan un IV aleatorio, lo postprocesan y actualizan para generar el IV para el gateway y usan ese IV junto con su propia clave de capa para cifrar los datos preprocesados. Para tunnels de salida deben descifrar iterativamente el IV (sin cifrar) y los datos preprocesados con el IV y las claves de capa para todos los saltos en el tunnel. El resultado del cifrado del tunnel de salida es que cuando cada peer lo cifra, el punto final recuperará los datos preprocesados iniciales.

### Procesamiento de Participantes {#tunnel.participant}

Cuando un peer recibe un mensaje de tunnel, verifica que el mensaje provino del mismo salto anterior que antes (inicializado cuando el primer mensaje pasa por el tunnel). Si el peer anterior es un router diferente, o si el mensaje ya ha sido visto, el mensaje se descarta. El participante entonces cifra el IV recibido con AES256/ECB usando su clave IV para determinar el IV actual, usa ese IV con la clave de capa del participante para cifrar los datos, cifra el IV actual con AES256/ECB usando su clave IV nuevamente, luego reenvía la tupla {nextTunnelId, nextIV, encryptedData} al siguiente salto. Este doble cifrado del IV (tanto antes como después del uso) ayuda a abordar una cierta clase de ataques de confirmación.

La detección de mensajes duplicados se maneja mediante un filtro Bloom decadente en los IVs de los mensajes. Cada router mantiene un único filtro Bloom para contener el XOR del IV y el primer bloque del mensaje recibido para todos los tunnels en los que está participando, modificado para eliminar las entradas vistas después de 10-20 minutos (cuando los tunnels habrán expirado). El tamaño del filtro Bloom y los parámetros utilizados son suficientes para saturar completamente la conexión de red del router con una probabilidad insignificante de falsos positivos. El valor único alimentado al filtro Bloom es el XOR del IV y el primer bloque para prevenir que pares coludidos no secuenciales en el tunnel etiqueten un mensaje reenviándolo con el IV y el primer bloque intercambiados.

### Procesamiento de Extremos {#tunnel.endpoint}

Después de recibir y validar un mensaje de tunnel en el último salto del tunnel, la forma en que el endpoint recupera los datos codificados por el gateway depende de si el tunnel es un tunnel entrante o saliente. Para tunnels salientes, el endpoint cifra el mensaje con su clave de capa como cualquier otro participante, exponiendo los datos preprocesados. Para tunnels entrantes, el endpoint también es el creador del tunnel, por lo que simplemente puede descifrar iterativamente el IV y el mensaje, usando las claves de capa e IV de cada paso en orden inverso.

En este punto, el extremo del túnel tiene los datos preprocesados enviados por la puerta de enlace, que luego puede analizar para extraer los mensajes I2NP incluidos y reenviarlos según se solicite en sus instrucciones de entrega.

## Construcción de Túneles {#tunnel.building}

Al construir un tunnel, el creador debe enviar una solicitud con los datos de configuración necesarios a cada uno de los saltos y esperar a que todos estén de acuerdo antes de habilitar el tunnel. Las solicitudes están cifradas para que solo los peers que necesiten conocer una pieza de información (como la capa del tunnel o la clave IV) tengan esos datos. Además, solo el creador del tunnel tendrá acceso a la respuesta del peer. Hay tres dimensiones importantes a tener en cuenta al crear los tunnels: qué peers se utilizan (y dónde), cómo se envían las solicitudes (y se reciben las respuestas), y cómo se mantienen.

### Selección de Peers {#tunnel.peerselection}

Además de los dos tipos de túneles - de entrada y de salida - hay dos estilos de selección de pares utilizados para diferentes túneles - exploratorio y cliente. Los túneles exploratorios se utilizan tanto para el mantenimiento de la base de datos de red como para el mantenimiento de túneles, mientras que los túneles cliente se utilizan para mensajes de cliente de extremo a extremo.

#### Selección de Peers para Tunnels Exploratorios {#tunnel.selection.exploratory}

Los túneles exploratorios se construyen a partir de una selección aleatoria de peers de un subconjunto de la red. El subconjunto particular varía según el router local y sus necesidades de enrutamiento de túneles. En general, los túneles exploratorios se construyen a partir de peers seleccionados aleatoriamente que están en la categoría de perfil "no fallando pero activo" del peer. El propósito secundario de los túneles, más allá del mero enrutamiento de túneles, es encontrar peers de alta capacidad subutilizados para que puedan ser promovidos para su uso en túneles de cliente.

La selección de peers exploratorios se discute más a fondo en la [página de Perfilado y Selección de Peers](/docs/overview/peer-selection).

#### Selección de Peers para Túneles de Cliente {#tunnel.selection.client}

Los túneles de cliente se construyen con un conjunto de requisitos más estrictos: el router local seleccionará peers de su categoría de perfil "rápido y de alta capacidad" para que el rendimiento y la confiabilidad satisfagan las necesidades de la aplicación cliente. Sin embargo, hay varios detalles importantes más allá de esa selección básica que deben respetarse, dependiendo de las necesidades de anonimato del cliente.

La selección de peers del cliente se discute más en detalle en la [página de Perfilado y Selección de Peers](/docs/overview/peer-selection).

#### Ordenamiento de Peers dentro de los Tunnels {#ordering}

Los peers están ordenados dentro de los tunnels para lidiar con el [ataque de predecesor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([actualización de 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

Para frustrar el ataque de predecesor, la selección de tunnel mantiene a los pares seleccionados en un orden estricto - si A, B y C están en un tunnel para un pool de tunnel particular, el salto después de A es siempre B, y el salto después de B es siempre C.

El ordenamiento se implementa generando una clave aleatoria de 32 bytes para cada pool de túneles al inicio. Los peers no deberían poder adivinar el ordenamiento, o un atacante podría crear dos hashes de router muy separados para maximizar la probabilidad de estar en ambos extremos de un túnel. Los peers se ordenan por distancia XOR del Hash SHA256 de (el hash del peer concatenado con la clave aleatoria) desde la clave aleatoria:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Debido a que cada pool de túneles utiliza una clave aleatoria diferente, el ordenamiento es consistente dentro de un solo pool pero no entre diferentes pools. Se generan nuevas claves en cada reinicio del router.

### Entrega de Solicitudes {#tunnel.request}

Un tunnel de múltiples saltos se construye usando un solo mensaje de construcción que se descifra y reenvía repetidamente. En la terminología de [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf), esto es construcción de tunnel telescópica "no interactiva".

Este método de preparación, entrega y respuesta de solicitudes de tunnel está [diseñado](/docs/specs/tunnel-creation) para reducir el número de predecesores expuestos, disminuir el número de mensajes transmitidos, verificar la conectividad adecuada y evitar el ataque de conteo de mensajes de la creación telescópica tradicional de tunnels. (Este método, que envía mensajes para extender un tunnel a través de la parte ya establecida del tunnel, se denomina construcción telescópica "interactiva" de tunnels en el documento "Hashing it out".)

Los detalles de los mensajes de solicitud y respuesta de tunnel, y su cifrado, [se especifican aquí](/docs/specs/tunnel-creation).

Los peers pueden rechazar las solicitudes de creación de túneles por diversas razones, aunque se conoce una serie de cuatro rechazos de gravedad creciente: rechazo probabilístico (debido a que el router se acerca a su capacidad, o en respuesta a una avalancha de solicitudes), sobrecarga transitoria, sobrecarga de ancho de banda y falla crítica. Cuando se reciben, estos cuatro son interpretados por el creador del túnel para ayudar a ajustar su perfil del router en cuestión.

Para más información sobre el perfilado de peers, consulta la [página de Perfilado y Selección de Peers](/docs/overview/peer-selection).

### Grupos de Túneles {#tunnel.pooling}

Para permitir una operación eficiente, el router mantiene una serie de pools de túneles, cada uno gestionando un grupo de túneles utilizados para un propósito específico con su propia configuración. Cuando se necesita un túnel para ese propósito, el router selecciona uno del pool apropiado al azar. En general, hay dos pools de túneles exploratorios - uno entrante y uno saliente - cada uno usando la configuración predeterminada del router. Además, hay un par de pools para cada destino local - un pool de túneles entrantes y uno saliente. Esos pools utilizan la configuración especificada cuando el destino local se conecta al router a través de [I2CP](/docs/specs/i2cp), o los valores predeterminados del router si no se especifica.

Cada pool tiene dentro de su configuración algunos ajustes clave, que definen cuántos tunnels mantener activos, cuántos tunnels de respaldo mantener en caso de fallo, qué tan largos deberían ser los tunnels, si esas longitudes deberían ser aleatorizadas, así como cualquier otra configuración permitida al configurar tunnels individuales. Las opciones de configuración se especifican en la [página I2CP](/docs/specs/i2cp).

### Longitudes de Tunnel y Valores Predeterminados {#length}

[En la página de resumen de túneles](/docs/overview/tunnel-routing#length).

### Estrategia de Construcción Anticipada y Prioridad {#strategy}

La construcción de tunnels es costosa, y los tunnels expiran un tiempo fijo después de ser construidos. Sin embargo, cuando un pool se queda sin tunnels, el Destination queda esencialmente muerto. Además, la tasa de éxito de construcción de tunnels puede variar enormemente tanto con las condiciones locales como globales de la red. Por lo tanto, es importante mantener una estrategia de construcción anticipatoria y adaptativa para asegurar que los nuevos tunnels se construyan exitosamente antes de que se necesiten, sin construir un exceso de tunnels, construirlos demasiado pronto, o consumir demasiada CPU o ancho de banda creando y enviando los mensajes de construcción cifrados.

Para cada tupla {exploratorio/cliente, entrada/salida, longitud, varianza de longitud} el router mantiene estadísticas sobre el tiempo requerido para una construcción exitosa de tunnel. Usando estas estadísticas, calcula cuánto tiempo antes de la expiración de un tunnel debe comenzar a intentar construir un reemplazo. A medida que se acerca el tiempo de expiración sin un reemplazo exitoso, inicia múltiples intentos de construcción en paralelo, y luego incrementará el número de intentos paralelos si es necesario.

Para limitar el ancho de banda y el uso de CPU, el router también limita el número máximo de intentos de construcción pendientes en todos los pools. Las construcciones críticas (aquellas para tunnels exploratorios y para pools que se han quedado sin tunnels) tienen prioridad.

## Limitación de Mensajes en Tunnel {#tunnel.throttling}

Aunque los tunnels dentro de I2P se parecen a una red de conmutación de circuitos, todo dentro de I2P está estrictamente basado en mensajes - los tunnels son simplemente trucos contables para ayudar a organizar la entrega de mensajes. No se hacen suposiciones con respecto a la confiabilidad u orden de los mensajes, y las retransmisiones se dejan a niveles superiores (por ejemplo, la biblioteca de streaming de la capa cliente de I2P). Esto permite a I2P aprovechar las técnicas de limitación disponibles tanto para redes de conmutación de paquetes como de conmutación de circuitos. Por ejemplo, cada router puede mantener un registro del promedio móvil de cuántos datos está usando cada tunnel, combinar eso con todos los promedios utilizados por otros tunnels en los que el router está participando, y ser capaz de aceptar o rechazar solicitudes adicionales de participación en tunnels basándose en su capacidad y utilización. Por otro lado, cada router puede simplemente descartar mensajes que están más allá de su capacidad, aprovechando la investigación utilizada en el Internet normal.

En la implementación actual, los routers implementan una estrategia de descarte temprano aleatorio ponderado (WRED). Para todos los routers participantes (participante interno, gateway de entrada y endpoint de salida), el router comenzará a descartar aleatoriamente una porción de mensajes cuando se aproximen a los límites de ancho de banda. A medida que el tráfico se acerca o excede los límites, se descartan más mensajes. Para un participante interno, todos los mensajes son fragmentados y rellenados y por lo tanto tienen el mismo tamaño. En el gateway de entrada y endpoint de salida, sin embargo, la decisión de descarte se toma sobre el mensaje completo (coalescido), y se tiene en cuenta el tamaño del mensaje. Los mensajes más grandes tienen más probabilidades de ser descartados. Además, es más probable que los mensajes sean descartados en el endpoint de salida que en el gateway de entrada, ya que esos mensajes no están tan "avanzados" en su trayecto y por lo tanto el costo de red de descartar esos mensajes es menor.

## Trabajo Futuro {#future}

### Mezcla/Agrupación {#tunnel.mixing}

¿Qué estrategias podrían utilizarse en el gateway y en cada salto para retrasar, reordenar, reroutar o rellenar mensajes? ¿En qué medida debería hacerse esto automáticamente, cuánto debería configurarse como una configuración por tunnel o por salto, y cómo debería el creador del tunnel (y a su vez, el usuario) controlar esta operación? Todo esto queda como desconocido, para ser resuelto en una versión futura distante.

### Relleno

Las estrategias de relleno se pueden usar en varios niveles, abordando la exposición de información del tamaño de mensaje a diferentes adversarios. El tamaño fijo actual del mensaje de tunnel es de 1024 bytes. Sin embargo, dentro de esto, los mensajes fragmentados en sí mismos no son rellenados por el tunnel en absoluto, aunque para mensajes extremo a extremo, pueden ser rellenados como parte del envoltorio garlic.

### WRED

Las estrategias WRED tienen un impacto significativo en el rendimiento de extremo a extremo y en la prevención del colapso por congestión de red. La estrategia WRED actual debe ser cuidadosamente evaluada y mejorada.
