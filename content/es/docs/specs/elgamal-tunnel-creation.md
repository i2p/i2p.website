---
title: "Especificación de Creación de Tunnel (ElGamal)"
description: "Especificación de construcción de túneles basada en ElGamal heredada, reemplazada por X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/es/tunnel-alt-creation"
  - "/es/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Descripción general {#tunnelcreate-overview}

NOTA: OBSOLETO - Esta es la especificación de construcción de túnel ElGamal. Consulta la [especificación de construcción de túnel X25519](/docs/specs/tunnel-creation-ecies) para el método actual.

Este documento especifica los detalles de los mensajes de construcción de tunnel cifrados utilizados para crear tunnels usando un método de "telescopado no interactivo". Consulte el documento de construcción de tunnel [TUNNEL-IMPL](/docs/specs/tunnel-implementation) para obtener una descripción general del proceso, incluyendo los métodos de selección y ordenamiento de pares.

La creación del tunnel se logra mediante un solo mensaje que se transmite a lo largo de la ruta de peers en el tunnel, se reescribe en el lugar y se transmite de vuelta al creador del tunnel. Este único mensaje de tunnel está compuesto por un número variable de registros (hasta 8) - uno para cada peer potencial en el tunnel. Los registros individuales están cifrados asimétricamente (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) para ser leídos solo por un peer específico a lo largo de la ruta, mientras que una capa adicional de cifrado simétrico (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) se añade en cada salto para exponer el registro cifrado asimétricamente solo en el momento apropiado.

### Número de Registros {#number}

No todos los registros deben contener datos válidos. El mensaje de construcción para un túnel de 3 saltos, por ejemplo, puede contener más registros para ocultar la longitud real del túnel a los participantes. Hay dos tipos de mensajes de construcción. El Tunnel Build Message original ([TBM](/docs/specs/i2np#msg-tunnelbuild)) contiene 8 registros, lo cual es más que suficiente para cualquier longitud práctica de túnel. El Variable Tunnel Build Message más reciente ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) contiene de 1 a 8 registros. El originador puede equilibrar el tamaño del mensaje con la cantidad deseada de ofuscación de la longitud del túnel.

En la red actual, la mayoría de los tunnels tienen 2 o 3 saltos de longitud. La implementación actual utiliza un VTBM de 5 registros para construir tunnels de 4 saltos o menos, y el TBM de 8 registros para tunnels más largos. El VTBM de 5 registros (que, cuando se fragmenta, cabe en tres mensajes de tunnel de 1KB) reduce el tráfico de red y aumenta la tasa de éxito de construcción, porque es menos probable que se pierdan los mensajes más pequeños.

El mensaje de respuesta debe ser del mismo tipo y longitud que el mensaje de construcción.

### Especificación de Registro de Solicitud {#tunnelcreate-requestrecord}

También especificado en la Especificación I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Texto plano del registro, visible solo para el hop consultado:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Los campos de ID del siguiente túnel y hash de identidad del siguiente router se utilizan para especificar el siguiente salto en el tunnel, aunque para un extremo de tunnel de salida, especifican dónde debe enviarse el mensaje de respuesta de creación de tunnel reescrito. Además, el ID del siguiente mensaje especifica el ID de mensaje que el mensaje (o respuesta) debe usar.

La clave de la capa del tunnel, la clave IV del tunnel, la clave de respuesta y el IV de respuesta son cada uno valores aleatorios de 32 bytes generados por el creador, para uso únicamente en este registro de solicitud de construcción.

El campo flags contiene lo siguiente:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
El bit 7 indica que el salto será un gateway de entrada (IBGW). El bit 6 indica que el salto será un endpoint de salida (OBEP). Si ningún bit está establecido, el salto será un participante intermedio. Ambos no pueden estar establecidos al mismo tiempo.

#### Creación de Registro de Solicitud

Cada salto obtiene un Tunnel ID aleatorio, distinto de cero. Se completan los Tunnel IDs del salto actual y del siguiente. Cada registro obtiene una clave IV de tunnel aleatoria, IV de respuesta, clave de capa y clave de respuesta.

#### Cifrado de Registros de Solicitud {#encryption}

Ese registro de texto claro está cifrado con ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) usando la clave pública de cifrado del salto y formateado en un registro de 528 bytes:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
En el registro cifrado de 512 bytes, los datos ElGamal contienen los bytes 1-256 y 258-513 del bloque cifrado ElGamal de 514 bytes [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Los dos bytes de relleno del bloque (los bytes cero en las ubicaciones 0 y 257) se eliminan.

Dado que el texto en claro utiliza el campo completo, no hay necesidad de relleno adicional más allá de `SHA256(cleartext) + cleartext`.

Cada registro de 528 bytes se cifra entonces de forma iterativa (usando descifrado AES, con la clave de respuesta y el IV de respuesta para cada salto) de manera que la identidad del router solo estará en texto claro para el salto en cuestión.

### Procesamiento de Saltos y Encriptación {#tunnelcreate-hopprocessing}

Cuando un salto recibe un TunnelBuildMessage, busca entre los registros contenidos en él uno que comience con su propio hash de identidad (recortado a 16 bytes). Luego descifra el bloque ElGamal de ese registro y recupera el texto claro protegido. En ese punto, se aseguran de que la solicitud de tunnel no sea un duplicado alimentando la clave de respuesta AES-256 en un filtro Bloom. Los duplicados o solicitudes inválidas se descartan. Los registros que no estén marcados con la hora actual, o la hora anterior si es poco después del comienzo de la hora, deben descartarse. Por ejemplo, toma la hora en la marca de tiempo, conviértela a tiempo completo, entonces si está más de 65 minutos atrasada o 5 minutos adelantada respecto al tiempo actual, es inválida. El filtro Bloom debe tener una duración de al menos una hora (más unos pocos minutos, para permitir el desfase del reloj), de modo que los registros duplicados en la hora actual que no sean rechazados al verificar la marca de tiempo de hora en el registro, serán rechazados por el filtro.

Después de decidir si aceptarán participar en el tunnel o no, reemplazan el registro que contenía la solicitud con un bloque de respuesta cifrado. Todos los demás registros se cifran con AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) usando la clave de respuesta y el IV incluidos. Cada uno se cifra por separado con AES/CBC usando la misma clave de respuesta y IV de respuesta. El modo CBC no se continúa (encadena) a través de los registros.

Cada salto conoce solo su propia respuesta. Si está de acuerdo, mantendrá el tunnel hasta su expiración, incluso si no será utilizado, ya que no puede saber si todos los demás saltos estuvieron de acuerdo.

#### Especificación del Registro de Respuesta {#tunnelcreate-replyrecord}

Después de que el hop actual lee su registro, lo reemplaza con un registro de respuesta indicando si acepta o no participar en el tunnel, y si no lo hace, clasifica su razón de rechazo. Esto es simplemente un valor de 1 byte, donde 0x0 significa que acepta participar en el tunnel, y valores más altos significan niveles más altos de rechazo.

Se definen los siguientes códigos de rechazo:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Para ocultar otras causas, como el apagado del router, de los pares, la implementación actual usa TUNNEL_REJECT_BANDWIDTH para casi todos los rechazos.

La respuesta se cifra con la clave de sesión AES que se le entregó en el bloque cifrado, rellenada con 495 bytes de datos aleatorios para alcanzar el tamaño completo del registro. El relleno se coloca antes del byte de estado:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Esto también se describe en la especificación I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### Preparación del Mensaje de Construcción de Tunnel {#tunnelcreate-requestpreparation}

Al construir un nuevo Tunnel Build Message, todos los Build Request Records deben construirse primero y cifrarse asimétricamente usando ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Cada registro se descifra entonces de forma preventiva con las claves de respuesta e IVs de los saltos anteriores en la ruta, usando AES [CRYPTO-AES](/docs/specs/cryptography#AES). Ese descifrado debe ejecutarse en orden inverso para que los datos cifrados asimétricamente aparezcan en texto claro en el salto correcto después de que su predecesor los cifre.

Los registros excedentes que no se necesitan para solicitudes individuales simplemente se rellenan con datos aleatorios por parte del creador.

### Entrega de Mensaje de Construcción de Tunnel {#tunnelcreate-requestdelivery}

Para tunnels salientes, la entrega se realiza directamente desde el creador del tunnel hasta el primer salto, empaquetando el TunnelBuildMessage como si el creador fuera simplemente otro salto en el tunnel. Para tunnels entrantes, la entrega se realiza a través de un tunnel saliente existente. El tunnel saliente generalmente proviene del mismo pool que el nuevo tunnel que se está construyendo. Si no hay un tunnel saliente disponible en ese pool, se utiliza un tunnel exploratorio saliente. Al inicio, cuando aún no existe un tunnel exploratorio saliente, se utiliza un tunnel saliente falso de 0 saltos.

### Manejo de Endpoint de Mensaje de Construcción de Tunnel {#tunnelcreate-endpointhandling}

Para la creación de un túnel de salida, cuando la solicitud llega a un endpoint de salida (según se determina por la bandera 'permitir mensajes a cualquiera'), el salto se procesa como de costumbre, encriptando una respuesta en lugar del registro y encriptando todos los otros registros, pero como no hay un 'siguiente salto' al cual reenviar el TunnelBuildMessage, en su lugar coloca los registros de respuesta encriptados en un TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) o VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (el tipo de mensaje y el número de registros debe coincidir con el de la solicitud) y lo entrega al túnel de respuesta especificado dentro del registro de solicitud. Ese túnel de respuesta reenvía el Tunnel Build Reply Message de vuelta al creador del túnel, igual que para cualquier otro mensaje [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). El creador del túnel luego lo procesa, como se describe a continuación.

El tunnel de respuesta fue seleccionado por el creador de la siguiente manera: Generalmente es un tunnel de entrada del mismo grupo que el nuevo tunnel de salida que se está construyendo. Si no hay ningún tunnel de entrada disponible en ese grupo, se utiliza un tunnel exploratorio de entrada. Al inicio, cuando aún no existe ningún tunnel exploratorio de entrada, se utiliza un tunnel de entrada falso de 0 saltos.

Para la creación de un tunnel de entrada, cuando la solicitud llega al punto final de entrada (también conocido como el creador del tunnel), no hay necesidad de generar un mensaje explícito de respuesta de construcción de tunnel, y el router procesa cada una de las respuestas, como se indica a continuación.

### Procesamiento de Mensajes de Respuesta de Construcción de Tunnel {#tunnelcreate-replyprocessing}

Para procesar los registros de respuesta, el creador simplemente tiene que descifrar AES cada registro individualmente, usando la clave de respuesta y el IV de cada salto en el tunnel después del par (en orden inverso). Esto entonces expone la respuesta especificando si están de acuerdo en participar en el tunnel o por qué se niegan. Si todos están de acuerdo, el tunnel se considera creado y puede ser usado inmediatamente, pero si alguien se niega, el tunnel se descarta.

Los acuerdos y rechazos se registran en el perfil de cada peer [PEER-SELECTION](/docs/overview/peer-selection), para ser utilizados en futuras evaluaciones de la capacidad de túnel del peer.

## Historia y Notas {#tunnelcreate-notes}

Esta estrategia surgió durante una discusión en la lista de correo de I2P entre Michael Rogers, Matthew Toseland (toad), y jrandom sobre el ataque de predecesor. Ver [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Fue introducida en la versión 0.6.1.10 el 16-02-2006, que fue la última vez que se realizó un cambio no compatible con versiones anteriores en I2P.

Notas:

- Este diseño no previene que dos peers hostiles dentro de un tunnel etiqueten uno o más registros de solicitud o respuesta para detectar que están dentro del mismo tunnel, pero hacer esto puede ser detectado por el creador del tunnel al leer la respuesta, causando que el tunnel sea marcado como inválido.

- Este diseño no incluye una prueba de trabajo en la sección cifrada asimétricamente, aunque el hash de identidad de 16 bytes podría reducirse a la mitad con la última parte reemplazada por una función hashcash de hasta 2^64 de costo.

- Este diseño por sí solo no previene que dos peers hostiles dentro de un tunnel utilicen información de temporización para determinar si están en el mismo tunnel. El uso de entrega de solicitudes por lotes y sincronizada podría ayudar (agrupando solicitudes y enviándolas en el minuto sincronizado con ntp). Sin embargo, hacer esto permite que los peers 'etiqueten' las solicitudes retrasándolas y detectando el retraso más tarde en el tunnel, aunque tal vez descartar solicitudes que no se entreguen en una pequeña ventana funcionaría (aunque hacer eso requeriría un alto grado de sincronización de reloj). Alternativamente, ¿quizás los saltos individuales podrían inyectar un retraso aleatorio antes de reenviar la solicitud?

- ¿Hay algún método no fatal para etiquetar la solicitud?

- La marca de tiempo con una resolución de una hora se usa para la prevención de repetición. Esta restricción no se aplicó hasta la versión 0.9.16.

## Trabajo Futuro {#future}

- En la implementación actual, el originador deja un registro vacío
  para sí mismo. Por lo tanto, un mensaje de n registros solo puede construir un tunnel de n-1 saltos.
  Esto parece ser necesario para los tunnels de entrada (donde el penúltimo salto
  puede ver el prefijo hash para el siguiente salto), pero no para los tunnels de salida.
  Esto debe investigarse y verificarse. Si es posible usar el
  registro restante sin comprometer el anonimato, deberíamos hacerlo.

- Análisis adicional de posibles ataques de etiquetado y temporización descritos en las notas anteriores.

- Usar solo VTBM; no seleccionar peers antiguos que no lo soporten.

- El Build Request Record no especifica un tiempo de vida o expiración del tunnel;
  cada salto expira el tunnel después de 10 minutos, que es una constante
  codificada de toda la red. Podríamos usar un bit en el campo de bandera y tomar 4 (o 8)
  bytes del relleno para especificar un tiempo de vida o expiración. El solicitante
  solo especificaría esta opción si todos los participantes la soportaran.

## Referencias {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
