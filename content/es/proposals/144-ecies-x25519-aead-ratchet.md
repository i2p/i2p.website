---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Nota
Despliegue y prueba de la red en progreso.
Sujeto a revisiones menores.
Consulte [SPEC]_ para la especificación oficial.

Las siguientes características no están implementadas en la versión 0.9.46:

- MessageNumbers, Options, y bloques de Termination
- Respuestas a nivel de protocolo
- Clave estática cero
- Multicast


## Visión General

Esta es una propuesta para el primer nuevo tipo de encriptación de extremo a extremo
desde el inicio de I2P, para reemplazar ElGamal/AES+SessionTags [Elg-AES]_.

Se basa en trabajos previos como sigue:

- Especificación de estructuras comunes [Common]_
- Especificación [I2NP]_ incluyendo LS2
- ElGamal/AES+Session Tags [Elg-AES]_
- http://zzz.i2p/topics/1768 visión general de nueva criptografía asimétrica
- Visión general de criptografía de bajo nivel [CRYPTO-ELG]_
- ECIES http://zzz.i2p/topics/2418
- [NTCP2]_ [Prop111]_
- 123 Nuevas entradas de netDB
- 142 Nuevo Template de Criptografía
- Protocolo [Noise]_
- Algoritmo de double ratchet [Signal]_

El objetivo es apoyar nueva encriptación para comunicaciones de extremo a extremo, de destino a destino.

El diseño utilizará un apretón de manos y una fase de datos de Noise incorporando el double ratchet de Signal.

Todas las referencias a Signal y Noise en esta propuesta son solo para información de fondo.
No se requiere conocimiento de los protocolos Signal y Noise para entender
o implementar esta propuesta.


### Usos actuales de ElGamal

Como revisión,
las claves públicas de 256 bytes de ElGamal pueden encontrarse en las siguientes estructuras de datos.
Consulte la especificación de estructuras comunes.

- En una Identidad de Router
  Esta es la clave de encriptación del router.

- En un Destino
  La clave pública del destino se usó para la antigua encriptación i2cp-a-i2cp
  que fue deshabilitada en la versión 0.6, actualmente no se utiliza excepto para
  el IV para la encriptación de LeaseSet, que está en desuso.
  La clave pública en el LeaseSet se usa en su lugar.

- En un LeaseSet
  Esta es la clave de encriptación del destino.

- En un LS2
  Esta es la clave de encriptación del destino.



### EncTypes en Certificados de Clave

Como revisión,
añadimos soporte para tipos de encriptación cuando añadimos soporte para tipos de firma.
El campo de tipo de encriptación siempre es cero, tanto en Destinaciones como en Identidades de Router.
Si alguna vez cambiamos esto está por decidir.
Consulte la especificación de estructuras comunes [Common]_.



### Usos de Criptografía Asimétrica

Como revisión, usamos ElGamal para:

1) Mensajes de Construcción de Tunel (clave está en RouterIdentity)
   El reemplazo no está cubierto en esta propuesta.
   Consulte la propuesta 152 [Prop152]_.

2) Encriptación de router a router de netdb y otros mensajes I2NP (Clave está en RouterIdentity)
   Depende de esta propuesta.
   También requiere una propuesta para 1), o poniendo la clave en las opciones de la RI.

3) Cliente de extremo a extremo ElGamal+AES/SessionTag (clave está en LeaseSet, la clave de Destino no se usa)
   El reemplazo ESTÁ cubierto en esta propuesta.

4) DH Efímero para NTCP1 y SSU
   El reemplazo no está cubierto en esta propuesta.
   Ver propuesta 111 para NTCP2.
   No hay propuesta actual para SSU2.


### Objetivos

- Compatible con versiones anteriores
- Requiere y se basa en LS2 (propuesta 123)
- Aprovechar nueva criptografía o primitivas añadidas para NTCP2 (propuesta 111)
- No se requieren nuevos cripto o primitivas para soporte
- Mantener el desacoplamiento de criptografía y firma; apoyar todas las versiones actuales y futuras
- Habilitar nueva criptografía para destinos
- Habilitar nueva criptografía para routers, pero solo para mensajes de ajo - la construcción de túneles sería
  una propuesta separada
- No romper nada que dependa de hashes de destino binario de 32 bytes, por ejemplo, bittorrent
- Mantener la entrega de mensajes 0-RTT utilizando DH efímero-estático
- No requerir almacenamiento en búfer / colas de mensajes en esta capa de protocolo;
  continuar apoyando la entrega ilimitada de mensajes en ambas direcciones sin esperar una respuesta
- Actualizar a DH efímero-efímero después de 1 RTT
- Mantener el manejo de mensajes fuera de orden
- Mantener la seguridad de 256 bits
- Añadir secreto de reenvío
- Añadir autenticación (AEAD)
- Mucho más eficiente en CPU que ElGamal
- No depender de Java jbigi para hacer eficiente DH
- Minimizar operaciones DH
- Mucho más eficiente en ancho de banda que ElGamal (bloque ElGamal de 514 bytes)
- Soportar cripto nuevo y antiguo en el mismo túnel si se desea
- El destinatario es capaz de distinguir eficientemente entre cripto nuevo y antiguo que baja por
  el mismo túnel
- Otros no pueden distinguir entre cripto nuevo, antiguo o futuro
- Eliminar la clasificación de longitud de sesión Nuevo vs. Existente (soportar padding)
- No se requieren nuevos mensajes I2NP
- Reemplazar el checksum SHA-256 en el payload AES con AEAD
- Soportar la vinculación de sesiones de transmisión y recepción para que
  los reconocimientos puedan ocurrir dentro del protocolo, en lugar de solo fuera de banda.
  Esto también permitirá que las respuestas tengan secreto de reenvío inmediatamente.
- Habilitar la encriptación de extremo a extremo de ciertos mensajes (almacenamientos RouterInfo)
  que actualmente no hacemos debido a la sobrecarga de CPU.
- No cambiar el mensaje de ajo I2NP
  o las instrucciones de entrega de mensajes de ajo en formato.
- Eliminar campos no utilizados o redundantes en los juegos de clavo de ajo y formatos de clavo.

Eliminar varios problemas con etiquetas de sesión, incluyendo:

- Incapacidad para usar AES hasta la primera respuesta
- Falta de confiabilidad y bloqueos si se asume la entrega de etiquetas
- Ineficiente de ancho de banda, especialmente en la primera entrega
- Enorme ineficiencia de espacio para almacenar etiquetas
- Enorme sobrecarga de ancho de banda para entregar etiquetas
- Altamente complejo, difícil de implementar
- Difícil de ajustar para diversos casos de uso
  (streaming vs. datagramas, servidor vs. cliente, alto vs. bajo ancho de banda)
- Vulnerabilidades de agotamiento de memoria debido a la entrega de etiquetas


### No-Objetivos / Fuera de Alcance

- Cambios en formato LS2 (propuesta 123 está hecha)
- Nuevo algoritmo de rotación DHT o generación aleatoria compartida
- Nueva encriptación para construcción de túneles.
  Ver propuesta 152 [Prop152]_.
- Nueva encriptación para la encriptación de capa de túnel.
  Ver propuesta 153 [Prop153]_.
- Métodos de encriptación, transmisión y recepción de mensajes I2NP DLM / DSM / DSRM.
  No cambiar.
- No se apoya la comunicación LS1 a LS2 o ElGamal/AES a esta propuesta.
  Esta propuesta es un protocolo bidireccional.
  Los destinos pueden manejar la compatibilidad hacia atrás publicando dos leasesets
  usando los mismos túneles, o colocando ambos tipos de encriptación en el LS2.
- Cambios en el modelo de amenazas
- Detalles de implementación no se discuten aquí y se dejan a cada proyecto.
- (Optimista) Añadir extensiones o ganchos para soportar multidifusión



### Justificación

ElGamal/AES+SessionTag ha sido nuestro único protocolo de extremo a extremo durante unos 15 años,
esencialmente sin modificaciones al protocolo.
Ahora hay primitivas criptográficas que son más rápidas.
Necesitamos mejorar la seguridad del protocolo.
También hemos desarrollado estrategias heurísticas y soluciones para minimizar
la sobrecarga de memoria y ancho de banda del protocolo, pero esas estrategias
son frágiles, difíciles de afinar, y hacen que el protocolo sea aún más propenso
a romperse, causando que la sesión se caiga.

Durante aproximadamente el mismo tiempo, la especificación ElGamal/AES+SessionTag y la documentación relacionada
han descrito lo costoso que es en ancho de banda la entrega de etiquetas de sesión,
y han propuesto reemplazar la entrega de etiquetas de sesión con un "PRNG sincronizado".
Un PRNG sincronizado genera determinísticamente las mismas etiquetas en ambos extremos,
derivadas de una semilla común.
Un PRNG sincronizado también puede denominarse "ratchet".
Esta propuesta (finalmente) especifica ese mecanismo de ratchet, y elimina la entrega de etiquetas.

Al usar un ratchet (un PRNG sincronizado) para generar las
etiquetas de sesión, eliminamos la sobrecarga de enviar etiquetas de sesión
en el mensaje de nueva sesión y los mensajes posteriores cuando sea necesario.
Para un conjunto de etiquetas típicas de 32 etiquetas, esto es 1KB.
Esto también elimina el almacenamiento de etiquetas de sesión en el lado del envío,
reduciendo así a la mitad los requisitos de almacenamiento.

Se requiere un intercambio completo de manos en ambas direcciones, similar al patrón Noise IK, para evitar ataques de suplantación por compromiso de clave (KCI).
Ver la tabla "Propiedades de Seguridad de Payloads" de Noise en [NOISE]_.
Para más información sobre KCI, ver el documento https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf



### Modelo de Amenaza

El modelo de amenaza es algo diferente que para NTCP2 (propuesta 111).
Los nodos MitM son el OBEP y IBGW y se asume que tienen una vista completa de
la NetDB global actual o histórica, al coludir con las inundaciones.

El objetivo es evitar que estos MitMs clasifiquen el tráfico como
mensajes de nueva y existente sesión, o como nuevo cripto vs. cripto antiguo.



## Propuesta Detallada

Esta propuesta define un nuevo protocolo de extremo a extremo para reemplazar ElGamal/AES+SessionTags.
El diseño usará un apretón de manos Noise y una fase de datos incorporando el double ratchet de Signal.


### Resumen del Diseño Criptográfico

Hay cinco partes del protocolo a rediseñar:


- 1) Los nuevos y existentes formatos de contenedor de sesión
  son reemplazados por nuevos formatos.
- 2) ElGamal (claves públicas de 256 bytes, claves privadas de 128 bytes) será reemplazado
  por ECIES-X25519 (claves públicas y privadas de 32 bytes)
- 3) AES será reemplazado por
  AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abajo)
- 4) Las etiquetas de sesión serán reemplazadas por ratchets,
  que es esencialmente un PRNG criptográfico sincronizado.
- 5) El payload AES, tal como se define en la especificación ElGamal/AES+SessionTags,
  se reemplaza por un formato de bloque similar al de NTCP2.

Cada uno de los cinco cambios tiene su propia sección a continuación.


### Nuevas Primitivas Criptográficas para I2P

Las implementaciones actuales del router I2P requerirán implementaciones para
las siguientes primitivas criptográficas estándar,
que no son requeridas para los protocolos actuales de I2P:

- ECIES (pero esto es esencialmente X25519)
- Elligator2

Las implementaciones actuales del router I2P que aún no han implementado [NTCP2]_ ([Prop111]_)
también requerirán implementaciones para:

- Generación de claves X25519 y DH
- AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abajo)
- HKDF


### Tipo de Cripto

El tipo de cripto (usado en el LS2) es 4.
Esto indica una clave pública X25519 de 32 bytes en cositas, y el protocolo de extremo a extremo especificado aquí.

El tipo de cripto 0 es ElGamal.
Los tipos de cripto 1-3 están reservados para ECIES-ECDH-AES-SessionTag, ver propuesta 145 [Prop145]_.


### Marco del Protocolo Noise

Esta propuesta proporciona los requisitos basados en el Marco del Protocolo Noise
[NOISE]_ (Revisión 34, 2018-07-11).
Noise tiene propiedades similares al protocolo Station-To-Station
[STS]_, que es la base para el protocolo [SSU]_. En el idioma de Noise, Alice
es la iniciadora, y Bob es el respondedor.

Esta propuesta está basada en el protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256.
(El identificador real para la función de inicialización de clave
es "Noise_IKelg2_25519_ChaChaPoly_SHA256"
para indicar extensiones de I2P - ver la sección KDF 1 a continuación)
Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de apretón de manos interactivo: IK
  Alice transmite inmediatamente su clave estática a Bob (I)
  Alice ya conoce la clave estática de Bob (K)

- Patrón de apretón de manos unidireccional: N
  Alice no transmite su clave estática a Bob (N)

- Función DH: X25519
  DH de X25519 con una longitud de clave de 32 bytes como se especifica en [RFC-7748]_.

- Función de cifrado: ChaChaPoly
  AEAD_CHACHA20_POLY1305 como se especifica en [RFC-7539]_ sección 2.8.
  12 bytes de nonce, con los primeros 4 bytes establecidos en cero.
  Idéntico al de [NTCP2]_.

- Función de hash: SHA256
  Hash estándar de 32 bytes, ya usado extensivamente en I2P.


Adiciones al Marco
````````````````````

Esta propuesta define las siguientes mejoras a
Noise_IK_25519_ChaChaPoly_SHA256. Estas generalmente siguen las directrices en
[NOISE]_ sección 13.

1) Las claves efímeras en claro están codificadas con [Elligator2]_.

2) La respuesta se prefija con una etiqueta en claro.

3) Se define el formato de payload para los mensajes 1, 2, y la fase de datos.
   Por supuesto, esto no está definido en Noise.

Todos los mensajes incluyen un encabezado de Mensaje de Ajo [I2NP]_.
La fase de datos utiliza encriptación similar, pero no compatible, con la fase de datos de Noise.


### Patrones de Apretón de Manos

Los apretones de manos usan patrones de apretón de manos [Noise]_.

Se utiliza la siguiente correspondencia de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = payload del mensaje

Las sesiones de un solo uso y sin restricciones son similares al patrón Noise N.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es p ->

{% endhighlight %}

Las sesiones vinculadas son similares al patrón Noise IK.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

{% endhighlight %}


### Sesiones

El protocolo actual ElGamal/AES+SessionTag es unidireccional.
En esta capa, el receptor no sabe de dónde proviene un mensaje.
Las sesiones salientes y entrantes no están asociadas.
Los reconocimientos son fuera de banda usando un DeliveryStatusMessage
(envuelto en un GarlicMessage) en el clavo.

Hay una ineficiencia sustancial en un protocolo unidireccional.
Cualquier respuesta también debe usar un mensaje de 'Nueva Sesión' costoso.
Esto causa un mayor uso de ancho de banda, CPU y memoria.

También hay debilidades de seguridad en un protocolo unidireccional.
Todas las sesiones se basan en DH efímero-estático.
Sin un camino de retorno, no hay manera de que Bob "ratchet" su clave estática
a una clave efímera.
Sin saber de dónde proviene un mensaje, no hay manera de usar
la clave efímera recibida para mensajes salientes,
por lo que la respuesta inicial también usa DH efímero-estático.

Para esta propuesta, definimos dos mecanismos para crear un protocolo bidireccional: "emparejamiento" y "vinculación".
Estos mecanismos proporcionan una mayor eficiencia y seguridad.


Contexto de Sesión
```````````````````

Al igual que con ElGamal/AES+SessionTags, todas las sesiones entrantes y salientes
deben estar en un contexto dado, ya sea el contexto del router o
el contexto para un destino local particular.
En Java I2P, este contexto se llama el Session Key Manager.

Las sesiones no deben compartirse entre contextos, ya que eso permitiría
la correlación entre los diversos destinos locales,
o entre un destino local y un router.

Cuando un destino dado admite tanto ElGamal/AES+SessionTags
como esta propuesta, ambos tipos de sesiones pueden compartir un contexto.
Ver la sección 1c) a continuación.



Emparejamiento de Sesiones Entrantes y Salientes
`````````````````````````````````````````````````

Cuando se crea una sesión saliente en el origen (Alice),
se crea una nueva sesión entrante y se empareja con la sesión saliente,
a menos que no se espere respuesta (por ejemplo, datagramas en bruto).

Siempre se empareja una nueva sesión entrante con una nueva sesión saliente,
a menos que no se solicite respuesta (por ejemplo, datagramas en bruto).

Si se solicita una respuesta y se vincula a un destino remoto o router,
esa nueva sesión saliente está vinculada a ese destino o router,
y reemplaza cualquier sesión saliente anterior a ese destino o router.

El emparejamiento de sesiones entrantes y salientes proporciona un protocolo bidireccional
con la capacidad de "ratchet" las claves DH.



Vinculación de Sesiones y Destinos
`````````````````````````````````

Solo hay una sesión saliente a un destino o router dado.
Puede haber varias sesiones entrantes actuales de un destino o router dado.
Generalmente, cuando se crea una nueva sesión entrante, y se recibe tráfico
en esa sesión (que sirve como ACK), cualquier otra se marcará
para expirar relativamente rápido, en un minuto más o menos.
Se comprueba el valor anterior de mensajes enviados (PN), y si no hay
mensajes no recibidos (dentro del tamaño de la ventana) en la sesión entrante anterior,
la sesión anterior puede eliminarse inmediatamente.


Cuando se crea una sesión saliente en el originador (Alice),
está vinculada al Destino remoto (Bob),
y cualquier sesión entrante emparejada también estará vinculada al Destino remoto.
A medida que las sesiones "ratchet", continúan vinculándose al Destino remoto.

Cuando se crea una sesión entrante en el receptor (Bob),
puede estar vinculada al Destino remoto (Alice), a discreción de Alice.
Si Alice incluye información de vinculación (su clave estática) en el mensaje de Nueva Sesión,
la sesión estará vinculada a ese destino,
y se creará una sesión saliente y se vinculará al mismo Destino.
A medida que las sesiones "ratchet", continúan vinculándose al Destino remoto.


Beneficios de la Vinculación y el Emparejamiento
```````````````````````````````````````````````

Para el caso común, el uso de streaming, esperamos que Alice y Bob utilicen el protocolo de la siguiente manera:

- Alice empareja su nueva sesión saliente con una nueva sesión entrante, ambas vinculadas al destino remoto (Bob).
- Alice incluye la información de vinculación y la firma, y una solicitud de respuesta, en el
  mensaje de Nueva Sesión enviado a Bob.
- Bob empareja su nueva sesión entrante con una nueva sesión saliente, ambas vinculadas al destino remoto (Alice).
- Bob envía una respuesta (ack) a Alice en la sesión emparejada, con un cambio a una nueva clave DH.
- Alice cambia a una nueva sesión saliente con la nueva clave de Bob, emparejada con la sesión entrante existente.

Al vincular una sesión entrante a un Destino remoto, y emparejar la sesión entrante
a una sesión saliente vinculada al mismo Destino, logramos dos beneficios principales:

1) La respuesta inicial de Bob a Alice utiliza DH efímero-efímero

2) Después de que Alice recibe la respuesta de Bob y cambia, todos los mensajes subsiguientes de Alice a Bob
utilizan DH efímero-efímero.


ACK de Mensajes
``````````````

En ElGamal/AES+SessionTags, cuando se agrupa un LeaseSet como un clavo de ajo,
o se entregan etiquetas, el router de envío solicita un ACK.
Este es un clavo de ajo separado que contiene un DeliveryStatus Message.
Por seguridad adicional, el DeliveryStatus Message está envuelto en un Garlic Message.
Este mecanismo está fuera de banda desde la perspectiva del protocolo.

En el nuevo protocolo, dado que las sesiones entrantes y salientes están emparejadas,
podemos tener ACK dentro de banda. No se requiere un clavo separado.

Un ACK explícito es simplemente un mensaje de Sesión Existente sin bloque I2NP.
Sin embargo, en la mayoría de los casos, se puede evitar un ACK explícito, ya que hay tráfico inverso.
Puede ser deseable que las implementaciones esperen un poco (quizás cien ms)
antes de enviar un ACK explícito, para dar al streaming o a la capa de aplicación tiempo para responder.

Las implementaciones también necesitarán diferir el envío de cualquier ACK hasta después
de que se procese el bloque I2NP, ya que el Garlic Message puede contener un Database Store Message
con un lease set. Un lease set reciente será necesario para enrutar el ACK,
y el destino remoto (contenido en el lease set) será necesario para
verificar la clave estática de vinculación.


Tiempos de Expiración de Sesiones
`````````````````````````````````

Las sesiones salientes siempre deben expirar antes que las sesiones entrantes.
Una vez que una sesión saliente expira, y se crea una nueva, se creará una nueva sesión entrante emparejada. Si había una sesión entrante anterior,
se le permitirá expirar.


### Multicast

TBD


### Definiciones
Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados.

ZEROLEN
    matriz de bytes de longitud cero

CSRNG(n)
    salida de n bytes de un generador de números aleatorios criptográficamente seguro.

H(p, d)
    Función hash SHA-256 que toma una cadena de personalización p y datos d, y
    produce una salida de longitud 32 bytes.
    Como se define en [NOISE]_.
    || abajo significa añadir.

    Utilizar SHA-256 de la siguiente manera::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    Función hash SHA-256 que toma un hash anterior h y nuevos datos d,
    y produce una salida de longitud 32 bytes.
    || abajo significa añadir.

    Utilizar SHA-256 de la siguiente manera::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    El AEAD de ChaCha20/Poly1305 como se especifica en [RFC-7539]_.
    S_KEY_LEN = 32 y S_IV_LEN = 12.

    ENCRIPTAR(k, n, texto plano, ad)
        Encripta texto plano usando la clave del cifrado k, y un nonce n que DEBE ser único para
        la clave k.
        Los datos asociados ad son opcionales.
        Devuelve un texto cifrado que es del tamaño del texto plano + 16 bytes para el HMAC.

        Todo el texto cifrado debe ser indistinguible de aleatorio si la clave es secreta.

    DESENCRYPTAR(k, n, texto cifrado, ad)
        Desencripta el texto cifrado usando la clave del cifrado k, y un nonce n.
        Los datos asociados ad son opcionales.
        Devuelve el texto plano.

DH
    Sistema de acuerdo de clave pública X25519. Claves privadas de 32 bytes, claves públicas de 32
    bytes, produce salidas de 32 bytes. Tiene las siguientes
    funciones:

    GENERAR_PRIVADA()
        Genera una nueva clave privada.

    DERIVAR_PUBLICA(privkey)
        Devuelve la clave pública correspondiente a la clave privada dada.

    GENERAR_PRIVADA_ELG2()
        Genera una nueva clave privada que se asigna a una clave pública adecuada para codificación Elligator2.
        Tenga en cuenta que la mitad de las claves privadas generadas aleatoriamente no serán adecuadas y deben descartarse.

    CODIFICAR_ELG2(pubkey)
        Devuelve la clave pública codificada Elligator2 correspondiente a la clave pública proporcionada (mapeo inverso).
        Las claves codificadas son de pequeño fin.
        La clave codificada debe tener 256 bits indistinguibles de datos aleatorios.
        Consulte la sección Elligator2 a continuación para la especificación.

    DECODIFICAR_ELG2(pubkey)
        Devuelve la clave pública correspondiente a la clave pública codificada Elligator2 dada.
        Consulte la sección Elligator2 a continuación para la especificación.

    DH(privkey, pubkey)
        Genera un secreto compartido a partir de las claves privada y pública dadas.

HKDF(sal, ikm, info, n)
    Función de derivación de clave criptográfica que toma algún material de clave de entrada ikm (que
    debe tener buena entropía pero no se requiere que sea una cadena uniformemente aleatoria), un sal
    de longitud 32 bytes, y un valor 'info' específico del contexto, y produce una salida
    de n bytes adecuados para su uso como material de clave.

    Utilizar HKDF como se especifica en [RFC-5869]_, usando la función hash HMAC SHA-256
    como se especifica en [RFC-2104]_. Esto significa que SALT_LEN es 32 bytes máx.

MixKey(d)
    Utilizar HKDF() con una clave de cadena anterior y nuevos datos d, y
    establecer la nueva clave de cadena y k.
    Como se define en [NOISE]_.

    Utilizar HKDF de la siguiente manera::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Formato del mensaje


Revisión del Formato Actual del Mensaje
````````````````````````````````````````

El mensaje de ajo tal como se especifica en [I2NP]_ es el siguiente.
Como un objetivo de diseño es que los saltos intermedios no puedan distinguir entre cripto nuevo y antiguo,
este formato no puede cambiar, incluso si el campo de longitud es redundante.
El formato se muestra con el encabezado completo de 16 bytes, aunque el
encabezado real puede estar en un formato diferente, dependiendo del transporte utilizado.

Cuando se descifra, los datos contienen una serie de Clavos de Ajo y
datos adicionales, también conocidos como un Set de Clavos.

Consulte [I2NP]_ para obtener detalles y una especificación completa.


.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

{% endhighlight %}


Revisión del Formato de Datos Cifrados
``````````````````````````````````````

El formato actual del mensaje, usado por más de 15 años,
es ElGamal/AES+SessionTags.
En ElGamal/AES+SessionTags, hay dos formatos de mensaje:

1) Nueva sesión:
- Bloque ElGamal de 514 bytes
- Bloque AES (mínimo 128 bytes, múltiplo de 16)

2) Sesión existente:
- Etiqueta de Sesión de 32 bytes
- Bloque AES (mínimo 128 bytes, múltiplo de 16)

El relleno mínimo a 128 es como se implementó en Java I2P pero no se impone en la recepción.

Estos mensajes están encapsulados en un mensaje de ajo I2NP, que contiene
un campo de longitud, por lo que la longitud se conoce.

Tenga en cuenta que no hay relleno definido a una longitud no-módulo-16,
así que el Nuevo Sesión siempre es (mod 16 == 2),
y una Sesión Existente siempre es (mod 16 == 0).
Necesitamos arreglar esto.

El receptor primero intenta buscar los primeros 32 bytes como una Etiqueta de Sesión.
Si se encuentra, descifra el bloque AES.
Si no se encuentra, y los datos son de al menos (514+16) de longitud, intenta descifrar el bloque ElGamal,
y si tiene éxito, descifra el bloque AES.


Nuevas Etiquetas de Sesión y Comparación con Signal
```````````````````````````````````````````````````

En Signal Double Ratchet, el encabezado contiene:

- DH: Clave pública actual del ratchet
- PN: Longitud del mensaje de cadena anterior
- N: Número del mensaje

Las "cadenas de envío" de Signal son aproximadamente equivalentes a nuestros conjuntos de etiquetas.
Al usar una etiqueta de sesión, podemos eliminar la mayor parte de eso.

En Nueva Sesión, ponemos solo la clave pública en el encabezado no cifrado.

En Sesión Existente, usamos una etiqueta de sesión para el encabezado.
La etiqueta de sesión está asociada con la clave pública actual del ratchet,
y el número de mensaje.

En ambos nuevo y Sesión Existente, PN y N están en el cuerpo cifrado.

En Signal, las cosas están constantemente "ratchet". Una nueva clave pública DH requiere que el
receptor "ratchet" y envíe una nueva clave pública de regreso, lo que también sirve
como el reconocimiento de la clave pública recibida.
Eso sería demasiadas operaciones DH para nosotros.
Así que separamos el reconocimiento de la clave recibida y la transmisión de una nueva clave pública.
Cualquier mensaje que use una etiqueta de sesión generada a partir de la nueva clave pública DH constituye un ACK.
Solo transmitimos una nueva clave pública cuando deseamos volver a cifrar.

El número máximo de mensajes antes de que el DH debe "ratchet" es 65535.

Al entregar una clave de sesión, derivamos el "Conjunto de Etiquetas" de ella,
en lugar de tener que entregar etiquetas de sesión también.
Un Conjunto de Etiquetas puede ser de hasta 65536 etiquetas.
Sin embargo, los receptores deben implementar una estrategia de "mirar hacia adelante", en lugar
de generar todas las etiquetas posibles de una vez.
Solo generar a lo más N etiquetas después de la última etiqueta buena recibida.
N podría ser a lo máximo 128, pero 32 o incluso menos pueden ser una mejor elección.



### 1a) Formato de nueva sesión

Nueva Clave Pública Efímera de Sesión (32 bytes)
Datos cifrados y MAC (bytes restantes)

El mensaje de Nueva Sesión puede o no contener la clave pública estática del remitente.
Si se incluye, la sesión de retorno está vinculada a esa clave.
La clave estática debe incluirse si se esperan respuestas,
es decir, para streaming y datagramas replicables.
No debe incluirse para datagramas en bruto.

El mensaje de Nueva Sesión es similar al patrón unidireccional de Noise [NOISE]_
"N" (si no se envía la clave estática),
o al patrón de dos sentidos "IK" (si se envía la clave estática).



### 1b) Formato de nueva sesión (con vinculación)

La longitud es de 96 + longitud del payload.
Formato cifrado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nueva Clave Pública Efímera de Sesión|
  +             32 bytes                  +
  |     Codificada con Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Clave Estática                +
  |       Datos cifrados ChaCha20         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +    (MAC) para la Clave Estática       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +          Sección de Payload            +
  |       Datos cifrados ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para Sección de Payload    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Clave Pública :: 32 bytes, endianidad pequeña, Elligator2, texto claro

  Datos cifrados de Clave Estática :: 32 bytes

  Datos cifrados de la Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}


Nueva Clave Efímera de Sesión
`````````````````````````````

La clave efímera es de 32 bytes, codificada con Elligator2.
Esta clave nunca se reutiliza; se genera una nueva clave con
cada mensaje, incluidas las retransmisiones.

Clave Estática
````````````

Al descifrar, la clave estática X25519 de Alice, 32 bytes.


Payload
```````

La longitud cifrada es el resto de los datos.
La longitud descifrada es 16 menos que la longitud cifrada.
El payload debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove.
Consulte la sección de payload a continuación para el formato y requisitos adicionales.



### 1c) Formato de nueva sesión (sin vinculación)

Si no se requiere respuesta, no se envía clave estática.


La longitud es de 96 + longitud del payload.
Formato cifrado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nueva Clave Pública Efímera de Sesión|
  +             32 bytes                  +
  |     Codificada con Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Sección de Banderas         +
  |       Datos cifrados ChaCha20         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para sección anterior      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +          Sección de Payload            +
  |       Datos cifrados ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para Sección de Payload    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Clave Pública :: 32 bytes, endianidad pequeña, Elligator2, texto claro

  Datos cifrados de la Sección de Banderas :: 32 bytes

  Datos cifrados de la Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}

Nueva Clave Efímera de Sesión
`````````````````````````````

Clave efímera de Alice.
La clave efímera es de 32 bytes, codificada con Elligator2, endianidad pequeña.
Esta clave nunca se reutiliza; se genera una nueva clave con
cada mensaje, incluidas las retransmisiones.


Datos de Sección de Banderas Cifrados
````````````````````````````

La sección de Banderas no contiene nada.
Siempre son 32 bytes, porque debe tener la misma longitud
que la clave estática para mensajes de Nueva Sesión con vinculación.
Bob determina si es una clave estática o una sección de banderas
probando si los 32 bytes son todos ceros.

TODO ¿se necesitan banderas aquí?

Payload
```````

La longitud cifrada es el resto de los datos.
La longitud descifrada es 16 menos que la longitud cifrada.
El payload debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove.
Consulte la sección de payload a continuación para el formato y requisitos adicionales.




### 1d) Formato de una sola vez (sin vinculación o sesión)

Si solo se espera enviar un mensaje único,
no se requiere configuración de sesión o clave estática.


La longitud es de 96 + longitud del payload.
Formato cifrado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |     Clave Pública Efímera             |
  +             32 bytes                  +
  |     Codificada con Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Sección de Banderas         +
  |       Datos cifrados ChaCha20         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para sección anterior      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +          Sección de Payload            +
  |       Datos cifrados ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para Sección de Payload    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Clave Pública :: 32 bytes, endianidad pequeña, Elligator2, texto claro

  Datos cifrados de la Sección de Banderas :: 32 bytes

  Datos cifrados de la Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}


Nueva Clave Única de Sesión
```````````````````````````

La clave única es de 32 bytes, codificada con Elligator2, endianidad pequeña.
Esta clave nunca se reutiliza; se genera una nueva clave con
cada mensaje, incluidas las retransmisiones.


Datos de Sección de Banderas Cifrados
````````````````````````````````````````

La sección de Banderas no contiene nada.
Siempre son 32 bytes, porque debe tener la misma longitud
que la clave estática para mensajes de Nueva Sesión con vinculación.
Bob determina si es una clave estática o una sección de banderas
probando si los 32 bytes son todos ceros.

TODO ¿se necesitan banderas aquí?

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             Todos ceros               +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  ceros:: Todos ceros, 32 bytes.

{% endhighlight %}


Payload
```````

La longitud cifrada es el resto de los datos.
La longitud descifrada es 16 menos que la longitud cifrada.
El payload debe contener un bloque DateTime y generalmente contendrá uno o más bloques Garlic Clove.
Consulte la sección de payload a continuación para el formato y requisitos adicionales.



### 1f) KDFs para Mensaje de Nueva Sesión

KDF para Clave de Cadena Inicial
````````````````````````````````

Esto es estándar [NOISE]_ para IK con un nombre de protocolo modificado.
Tenga en cuenta que usamos el mismo inicializador para ambos patrones IK (sesiones vinculadas)
y para el patrón N (sesiones no vinculadas).

El nombre del protocolo se modifica por dos razones.
Primero, para indicar que las claves efímeras están codificadas con Elligator2,
y segundo, para indicar que MixHash() se llama antes del segundo mensaje
para mezclar el valor de la etiqueta.

.. raw:: html

  {% highlight lang='text' %}
Este es el patrón de mensaje "e":

  // Definir protocol_name.
  Establecer protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, codificado en US-ASCII, sin terminación NULL).

  // Definir Hash h = 32 bytes
  h = SHA256(protocol_name);

  Definir ck = cadena de clave de 32 bytes. Copiar los datos de h a ck.
  Establecer chainKey = h

  // MixHash(nul prologue)
  h = SHA256(h);

  // Hasta aquí, todo se puede pre-calcular por Alice para todas las conexiones de salida

{% endhighlight %}


KDF para Contenidos Cifrados de la Sección de Banderas/Clave Estática
```````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Este es el patrón de mensaje "e":

  // Claves estáticas X25519 de Bob
  // bpk se publica en el leaseset
  bsk = GENERAR_PRIVADA()
  bpk = DERIVAR_PUBLICA(bsk)

  // Clave pública estática de Bob
  // MixHash(bpk)
  // || abajo significa añadir
  h = SHA256(h || bpk);

  // Hasta aquí, todo se puede pre-calcular por Bob para todas las conexiones entrantes

  // Claves efímeras X25519 de Alice
  aesk = GENERAR_PRIVADA_ELG2()
  aepk = DERIVAR_PUBLICA(aesk)

  // Clave pública efímera de Alice
  // MixHash(aepk)
  // || abajo significa añadir
  h = SHA256(h || aepk);

  // h se utiliza como los datos asociados para el AEAD en el Mensaje de Nueva Sesión
  // Conservar el Hash h para el KDF de Respuesta de Nueva Sesión
  // eapk se envía en texto claro en el
  // inicio del mensaje de Nueva Sesión
  elg2_aepk = CODIFICAR_ELG2(aepk)
  // Como decodificado por Bob
  aepk = DECODIFICAR_ELG2(elg2_aepk)

  Fin del patrón de mensaje "e".

  Este es el patrón de mensaje "es":

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parámetros de ChaChaPoly para encriptar/desencriptar
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parámetros de AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  texto_cipher = ENCRYPT(k, n, sección de banderas/clave estática, ad)

  Fin del patrón de mensaje "es".

  Este es el patrón de mensaje "s":

  // MixHash(texto_cipher)
  // Guardar para el KDF de la Sección de Payload
  h = SHA256(h || texto_cipher)

  // Claves estáticas X25519 de Alice
  ask = GENERAR_PRIVADA()
  apk = DERIVAR_PUBLICA(ask)

  Fin del patrón de mensaje "s".


{% endhighlight %}



KDF para Sección de Payload (con clave estática de Alice)
```````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Este es el patrón de mensaje "ss":

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parámetros de ChaChaPoly para encriptar/desencriptar
  // chainKey de la Sección de Clave Estática
  Establecer sharedSecret = resultado de DH X25519
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parámetros de AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  texto_cipher = ENCRYPT(k, n, payload, ad)

  Fin del patrón de mensaje "ss".

  // MixHash(texto_cipher)
  // Guardar para el KDF de Respuesta de Nueva Sesión
  h = SHA256(h || texto_cipher)

{% endhighlight %}


KDF para Sección de Payload (sin clave estática de Alice)
``````````````````````````````````````````````````````````

Tenga en cuenta que este es un patrón Noise "N", pero usamos el mismo inicializador "IK"
que para sesiones vinculadas.

Los mensajes de Nueva Sesión no se pueden identificar como si contuvieran la clave estática de Alice o no
hasta que la clave estática esté descifrada e inspeccionada para determinar si contiene todos ceros.
Por lo tanto, el receptor debe utilizar la máquina de estado "IK" para todos
los mensajes de Nueva Sesión.
Si la clave estática es toda ceros, el patrón de mensaje "ss" debe omitirse.



.. raw:: html

  {% highlight lang='text' %}
chainKey = de la sección Clave/flags
  k = de la sección de clave/flags
  n = 1
  ad = h de la sección Clave/flags
  texto_cipher = ENCRYPT(k, n, payload, ad)

{% endhighlight %}



### 1g) Formato de Respuesta de Nueva Sesión

Se pueden enviar una o más Respuestas de Nueva Sesión en respuesta a un solo mensaje de Nueva Sesión.
Cada respuesta va precedida por una etiqueta, que se genera a partir de un Conjunto de Etiquetas para la sesión.

La Respuesta de Nueva Sesión está en dos partes.
La primera parte es la finalización del apretón de manos Noise IK con una etiqueta prependedada.
La longitud de la primera parte es de 56 bytes.
La segunda parte es el payload de la fase de datos.
La longitud de la segunda parte es de 16 + longitud del payload.

Longitud total es 72 + longitud del payload.
Formato cifrado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Etiqueta de Sesión 8 bytes       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Clave Pública Efímera          +
  |                                       |
  +            32 bytes                   +
  |     Codificada con Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +  (MAC) para sección de Clave (sin datos) +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +          Sección de Payload            +
  |       Datos cifrados ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +       (MAC) para Sección de Payload    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Etiqueta :: 8 bytes, texto claro

  Clave Pública :: 32 bytes, endianidad pequeña, Elligator2, texto claro

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes
         Nota: Los datos de texto plano de ChaCha20 están vacíos (ZEROLEN)

  Datos cifrados de la Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}

Etiqueta de Sesión
```````````
La etiqueta se genera en el KDF de Etiquetas de Sesión, como se inicializa
en el KDF de Inicialización de DH a continuación.
Esta correlaciona la respuesta con la sesión.
La clave de sesión de la Inicialización de DH no se utiliza.


Nueva Clave Efímera de Respuesta de Sesión
````````````````````````````````````````

La clave efímera de Bob.
La clave efímera es de 32 bytes, codificada con Elligator2, endianidad pequeña.
Esta clave nunca se reutiliza; se genera una nueva clave con
cada mensaje, incluidas las retransmisiones.


Payload
```````
La longitud cifrada es el resto de los datos.
La longitud descifrada es 16 menos que la longitud cifrada.
El payload generalmente contendrá uno o más bloques Garlic Clove.
Consulte la sección de payload a continuación para el formato y requisitos adicionales.


KDF para Conjunto de Etiquetas de Respuesta
``````````````````````````````````````

Se crean una o más etiquetas del Conjunto de Etiquetas, que se inicializa usando
el KDF a continuación, usando la clave de cadena del mensaje de Nueva Sesión.

.. raw:: html

  {% highlight lang='text' %}
// Generar conjunto de etiquetas
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

{% endhighlight %}


KDF para Contenidos Cifrados de la Sección de Clave
````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
// Claves del mensaje de Nueva Sesión
  // Claves X25519 de Alice
  // apk y aepk se envían en el mensaje de Nueva Sesión original
  // ask = Clave privada estática de Alice
  // apk = Clave pública estática de Alice
  // aesk = Clave privada efímera de Alice
  // aepk = Clave pública efímera de Alice
  // Claves estáticas X25519 de Bob
  // bsk = Clave privada estática de Bob
  // bpk = Clave pública estática de Bob

  // Generar la etiqueta
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  Este es el patrón de mensaje "e":

  // Claves efímeras de Bob
  besk = GENERAR_PRIVADA_ELG2()
  bepk = DERIVAR_PUBLICA(besk)

  // Clave pública efímera de Bob
  // MixHash(bepk)
  // || abajo significa añadir
  h = SHA256(h || bepk);

  // elg2_bepk se envía en texto claro en el
  // inicio del mensaje de Nueva Sesión
  elg2_bepk = CODIFICAR_ELG2(bepk)
  // Como decodificado por Bob
  bepk = DECODIFICAR_ELG2(elg2_bepk)

  Fin del patrón de mensaje "e".

  Este es el patrón de mensaje "ee":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parámetros de ChaChaPoly para encriptar/desencriptar
  // chainKey del mensaje de Sección de Payload de Nueva Sesión original
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Fin del patrón de mensaje "ee".

  Este es el patrón de mensaje "se":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parámetros de AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  texto_cipher = ENCRYPT(k, n, ZEROLEN, ad)

  Fin del patrón de mensaje "se".

  // MixHash(texto_cipher)
  h = SHA256(h || texto_cipher)

  chainKey se utiliza en el ratchet a continuación.

{% endhighlight %}


KDF para Contenidos Cifrados de la Sección de Payload
``````````````````````````````````````````

Esto es como el primer mensaje de Sesión Existente,
post-split, pero sin una etiqueta separada.
Además, utilizamos el hash de arriba para enlazar el
payload al mensaje NSR.


.. raw:: html

  {% highlight lang='text' %}
// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // Parámetros de AEAD para payload de Respuesta de Nueva Sesión
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  texto_cipher = ENCRYPT(k, n, payload, ad)
{% endhighlight %}


### Notas

Se pueden enviar múltiples mensajes NSR en respuesta, cada uno con claves efímeras únicas, dependiendo del tamaño de la respuesta.

Se requiere que Alice y Bob usen nuevas claves efímeras para cada mensaje NS y NSR.

Alice debe recibir uno de los mensajes NSR de Bob antes de enviar mensajes de Sesión Existente (ES),
y Bob debe recibir un mensaje ES de Alice antes de enviar mensajes ES.

El ``chainKey`` y ``k`` de la Sección de Payload del NSR de Bob se utilizan
como entradas para los Ratchets DH de ES iniciales (ambas direcciones, ver KDF de Ratchet DH).

Bob solo debe retener Sesiones Existentes para los mensajes ES recibidos de Alice.
Cualquier otra sesión entrante y saliente creada (para múltiples NSRs) debería
destruirse inmediatamente después de recibir el primer mensaje ES de Alice para una sesión dada.



### 1h) Formato de sesión existente

Etiqueta de sesión (8 bytes)
Datos cifrados y MAC (ver sección 3 a continuación)


Formato
``````
Cifrado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Etiqueta de Sesión              |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +          Sección de Payload            +
  |       Datos cifrados ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Etiqueta de Sesión :: 8 bytes, texto claro

  Datos cifrados de la Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}


Payload
```````
La longitud cifrada es el resto de los datos.
La longitud descifrada es 16 menos que la longitud cifrada.
Véase la sección de payload a continuación para el formato y los requisitos.


KDF
```

.. raw:: html

  {% highlight lang='text' %}
Ver sección AEAD a continuación.

  // Parámetros de AEAD para payload de Sesión Existente
  k = La clave de sesión de 32 bytes asociada con esta etiqueta de sesión
  n = El número del mensaje N en la cadena actual, tal como se recupera de la etiqueta de sesión asociada.
  ad = La etiqueta de sesión, 8 bytes
  texto_cipher = ENCRYPT(k, n, payload, ad)
{% endhighlight %}



### 2) ECIES-X25519


Formato: claves públicas y privadas de 32 bytes, little-endian.

Justificación: Usado en [NTCP2]_.



### 2a) Elligator2

En los apretones de manos Noise estándar, los mensajes de apretón de manos iniciales en cada dirección comienzan con
claves efímeras que se transmiten en texto claro.
Como las claves X25519 válidas son distinguidas de aleatorias, un hombre-en-el-medio puede distinguir
estos mensajes de los mensajes de Sesión Existente que comienzan con etiquetas de sesión aleatorias.
En [NTCP2]_ ([Prop111]_), usamos una función XOR de bajo coste utilizando la clave estática fuera de banda para ofuscar
la clave. Sin embargo, el modelo de amenaza aquí es diferente; no queremos permitir a cualquier MitM
usar cualquier medio para confirmar el destino del tráfico, o distinguir
los mensajes de apretón de manos iniciales de los mensajes de Sesión Existente.

Por lo tanto, se utiliza [Elligator2]_ para transformar las claves efímeras en los mensajes de Nueva Sesión y Respuesta de Nueva Sesión
para que sean indistinguibles de cadenas aleatorias uniformes.



Formato
``````

Claves públicas y privadas de 32 bytes.
Las claves codificadas son little endian.

Como se define en [Elligator2]_, las claves codificadas son indistinguibles de 254 bits aleatorios.
Requerimos 256 bits aleatorios (32 bytes). Por lo tanto, la codificación y decodificación se
definen como sigue:

Codificación:

.. raw:: html

  {% highlight lang='text' %}
Definición ENCODE_ELG2()

  // Codificar como se define en la especificación Elligator2
  encodedKey = encode(pubkey)
  // OR en 2 bits aleatorios al MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
{% endhighlight %}


Decodificación:

.. raw:: html

  {% highlight lang='text' %}
Definición DECODE_ELG2()

  // Desenmascarar 2 bits aleatorios del MSB
  encodedKey[31] &= 0x3f
  // Descodificar como se define en la especificación Elligator2
  pubkey = decode(encodedKey)
{% endhighlight %}




Justificación
`````````````

Requerido para evitar que el OBEP y el IBGW clasifiquen el tráfico.


Notas
`````

Elligator2 duplica el tiempo promedio de generación de claves, ya que la mitad de las claves
privadas resultan en claves públicas que son inadecuadas para la codificación con Elligator2.
Además, el tiempo de generación de claves no está limitado con una distribución exponencial,
ya que el generador debe seguir intentando hasta que se encuentre un par de claves adecuado.

Este costo se puede gestionar generando claves por adelantado,
en un hilo separado, para mantener un grupo de claves adecuadas.

El generador realiza la función ENCODE_ELG2() para determinar la idoneidad.
Por lo tanto, el generador debe almacenar el resultado de ENCODE_ELG2()
para que no tenga que volver a calcularse.

Además, las claves inadecuadas pueden añadirse al grupo de claves
utilizadas para [NTCP2]_, donde no se utiliza Elligator2.
Las cuestiones de seguridad de hacer esto están por determinar.




### 3) AEAD (ChaChaPoly)

AEAD usando ChaCha20 y Poly1305, igual que en [NTCP2]_.
Esto corresponde a [RFC-7539]_, que también
se usa de manera similar en TLS [RFC-7905]_.



Entradas para Sesiones de Nueva Sesión y Respuesta de Nueva Sesión
`````````````````````````````````````````````````````

Entradas para las funciones de encriptación/desencriptación
para un bloque AEAD en un mensaje de Nueva Sesión:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: clave de cifrado de 32 bytes
       Ver KDFs de Nueva Sesión y Respuesta de Nueva Sesión arriba.

  n :: Nonce basado en contador, 12 bytes.
       n = 0

  ad :: Datos asociados, 32 bytes.
        El hash SHA256 de los datos precedentes, como salida de mixHash()

  data :: Datos de texto plano, 0 o más bytes

{% endhighlight %}


Entradas para Sesiones Existentes
`````````````````````````````

Entradas para las funciones de encriptación/desencriptación
para un bloque en una Sesión Existente:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: clave de sesión de 32 bytes
       Como se busca desde la etiqueta de sesión acompañante.

  n :: Nonce basado en contador, 12 bytes.
       Comienza en 0 y se incrementa para cada mensaje al transmitir.
       Para el receptor, el valor
       tal como se mira desde la etiqueta de sesión acompañante.
       Los primeros cuatro bytes son siempre cero.
       Los últimos ocho bytes son el número del mensaje (n), codificados en pequeño fin.
       El valor máximo es 65535.
       La sesión debe "ratchet" cuando N alcance ese valor.
       Los valores más altos nunca deben usarse.

  ad :: Datos asociados
        La etiqueta de sesión

  data :: Datos de texto plano, 0 o más bytes

{% endhighlight %}


Formato Cifrado
````````````````

Salida de la función de encriptación, entrada a la función de desencriptación:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Datos cifrados ChaCha20         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje de Poly1305 |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  datos cifrados :: Del mismo tamaño que los datos de texto plano, 0 - 65519 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes

{% endhighlight %}

Notas
`````
- Dado que ChaCha20 es un cifrado de flujo, los textos planos no necesitan relleno.
  Se descartan bytes adicionales de flujo de claves.

- La clave para el cifrado (256 bits) se acuerda mediante la KDF SHA256.
  Los detalles de la KDF para cada mensaje están en secciones separadas a continuación.

- Los marcos ChaChaPoly son de tamaño conocido ya que están encapsulados en el mensaje de datos I2NP.

- Para todos los mensajes,
  el relleno está dentro del
  marco de datos autenticado.


Manejo de errores AEAD
``````````````````````

Todos los datos recibidos que no pasen la verificación AEAD deben ser descartados.
No se devuelve respuesta.


Justificación
`````````````

Usado en [NTCP2]_.



### 4) Ratchets

Todavía usamos etiquetas de sesión, como antes, pero usamos ratchets para generarlas.
Las etiquetas de sesión también tenían una opción de recompra que nunca implementamos.
Así que es como un doble ratchet pero nunca hicimos el segundo.

Aquí definimos algo similar al Double Ratchet de Signal.
Las etiquetas de sesión se generan de manera determinista e idéntica en
el lado del receptor y del remitente.

Al usar un ratchet de clave/sincronización simétrica, eliminamos el uso de memoria para almacenar etiquetas de sesión en el lado del emisor.
También eliminamos el consumo de ancho de banda al enviar conjuntos de etiquetas.
El uso del lado del receptor sigue siendo significativo, pero podemos reducirlo aún más
ya que reduciremos la etiqueta de sesión de 32 bytes a 8 bytes.

No usamos el cifrado de encabezado como se especifica (y es opcional) en Signal,
usamos etiquetas de sesión en su lugar.

Al usar un ratchet DH, logramos secreto hacia adelante, lo cual nunca se implementó
en ElGamal/AES+SessionTags.

Nota: La clave pública de sesión única de Nueva Sesión no es parte del ratchet, su única función
es cifrar la clave inicial de DH del ratchet de Alice.


Números de Mensaje
`````````````````

El Double Ratchet maneja mensajes perdidos o desordenados al incluir en el encabezado de cada mensaje
una etiqueta. El receptor busca el índice de la etiqueta, este es el número de mensaje N.
Si el mensaje contiene un bloque de Número de Mensaje con un valor PN,
el receptor puede eliminar cualquier etiqueta superior a ese valor en el conjunto de etiquetas anterior,
mientras retiene etiquetas omitidas
del conjunto de etiquetas anterior en caso de que los mensajes omitidos lleguen más tarde.


Ejemplo de Implementación
````````````````````````

Definimos las siguientes estructuras de datos y funciones para implementar estos ratchets.

TAGSET_ENTRY
    Una única entrada en un TAGSET.

    INDEX
        Un índice de entero, comenzando con 0

    SESSION_TAG
        Un identificador para salir en el alambre, 8 bytes

    SESSION_KEY
        Una clave simétrica, nunca sale en el alambre, 32 bytes

TAGSET
    Una colección de TAGSET_ENTRIES.

    CREATE(key, n)
        Generar un nuevo TAGSET usando material criptográfico inicial de 32 bytes.
        Se proporciona el identificador de sesión asociado.
        Se especifica el número inicial de etiquetas a crear; esto generalmente es 0 o 1
        para una sesión saliente.
        LAST_INDEX = -1
        Se llama a EXTEND(n).

    EXTEND(n)
        Generar n más TAGSET_ENTRIES llamando a EXTEND() n veces.

    EXTEND()
        Generar una TAGSET_ENTRY más, a menos que el número máximo de SESSION_TAGS
        ya hayan sido generadas.
        Si LAST_INDEX es mayor o igual a 65535, devolver.
        ++ LAST_INDEX
        Crear una nueva TAGSET_ENTRY con el valor LAST_INDEX y el SESSION_TAG calculado.
        Llamadas a RATCHET_TAG() y (opcionalmente) RATCHET_KEY().
        Para sesiones entrantes, el cálculo del SESSION_KEY puede
        posponerse y calcularse en GET_SESSION_KEY().
        Llamados EXPIRE()

    EXPIRE()
        Eliminar etiquetas y claves que son demasiado antiguas, o si el tamaño de TAGSET excede algún límite.

    RATCHET_TAG()
        Calcula el siguiente SESSION_TAG basado en el último SESSION_TAG.

    RATCHET_KEY()
        Calcula la siguiente SESSION_KEY basada en la última SESSION_KEY.

    SESSION
        La sesión asociada.

    CREATION_TIME
        Cuándo se creó el TAGSET.

    LAST_INDEX
        El último índice TAGSET_ENTRY generado por EXTEND().

    GET_NEXT_ENTRY()
        Usado solo para sesiones salientes.
        Se llama a EXTEND(1) si no quedan TAGSET_ENTRIES.
        Si EXTEND(1) no hizo nada, el máximo de 65535 TAGSETS ha sido usado,
        y devuelve un error.
        Devuelve la siguiente TAGSET_ENTRY no utilizada.

    GET_SESSION_KEY(sessionTag)
        Utilizado solo para sesiones entrantes.
        Devuelve la TAGSET_ENTRY que contiene sessionTag.
        Si se encuentra, se elimina la TAGSET_ENTRY.
        Si el cálculo de SESSION_KEY fue pospuesto, se calcula ahora.
        Si quedan pocas TAGSET_ENTRIES, se llama a EXTEND(n).



4a) Ratchet de DH
``````````````````

"Ratchets" pero no tan rápido como Signal lo hace.
Separamos el reconocimiento de la clave recibida de la generación de la nueva clave.
En un uso típico, Alice y Bob harán un "ratchet" (dos veces) inmediatamente en una Nueva Sesión,
pero no lo harán nuevamente.

Tenga en cuenta que un "ratchet" es para una sola dirección, y genera una cadena de mensajes/clave de sesión
para esa dirección.
Para generar claves para ambas direcciones, debe "ratchet" dos veces.

Debe realizarse un "ratchet" cada vez que se genera y envía una nueva clave.
Debe realizarse un "ratchet" cada vez que se recibe una nueva
