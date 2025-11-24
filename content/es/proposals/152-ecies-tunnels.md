---
title: "Túneles ECIES"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Nota
Despliegue y pruebas de red en progreso.
Sujeto a revisiones menores.
Ver [SPEC](/en/docs/spec/) para la especificación oficial.


## Resumen

Este documento propone cambios en la encriptación de mensajes de construcción de túneles
usando primitivas criptográficas introducidas por [ECIES-X25519](/en/docs/spec/ecies/).
Es una parte de la propuesta global 
[Prop156](/en/proposals/156-ecies-routers/) para convertir routers de claves ElGamal a ECIES-X25519.

Con el fin de facilitar la transición de la red de ElGamal + AES256 a ECIES + ChaCha20,
son necesarios túneles con routers mixtos ElGamal y ECIES.
Se proporcionan especificaciones para el manejo de saltos mixtos en túneles.
No se realizarán cambios en el formato, procesamiento o encriptación de los saltos ElGamal.

Los creadores de túneles ElGamal deberán crear pares de claves efímeras X25519 por salto,
y seguir esta especificación para crear túneles que contengan saltos ECIES.

Esta propuesta especifica los cambios necesarios para la Construcción de Túneles con ECIES-X25519.
Para una visión general de todos los cambios requeridos para los routers ECIES, ver la propuesta 156 [Prop156](/en/proposals/156-ecies-routers/).

Esta propuesta mantiene el mismo tamaño para los registros de construcción de túneles,
como se requiere para la compatibilidad. Los registros de construcción y mensajes más pequeños se
implementarán más tarde - ver [Prop157](/en/proposals/157-new-tbm/).


### Primitivas Criptográficas

No se introducen nuevas primitivas criptográficas. Las primitivas requeridas para implementar esta propuesta son:

- AES-256-CBC como en [Cryptography](/en/docs/spec/cryptography/)
- Funciones STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) y DECRYPT(k, n, ciphertext, ad) - como en [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) y [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funciones DH X25519 - como en [NTCP2](/en/docs/spec/ntcp2/) y [ECIES-X25519](/en/docs/spec/ecies/)
- HKDF(salt, ikm, info, n) - como en [NTCP2](/en/docs/spec/ntcp2/) y [ECIES-X25519](/en/docs/spec/ecies/)

Otras funciones de Noise definidas en otros lugares:

- MixHash(d) - como en [NTCP2](/en/docs/spec/ntcp2/) y [ECIES-X25519](/en/docs/spec/ecies/)
- MixKey(d) - como en [NTCP2](/en/docs/spec/ntcp2/) y [ECIES-X25519](/en/docs/spec/ecies/)


### Objetivos

- Aumentar la velocidad de las operaciones criptográficas
- Reemplazar ElGamal + AES256/CBC con primitivas ECIES para BuildRequestRecords y BuildReplyRecords.
- No cambiar el tamaño de los BuildRequestRecords y BuildReplyRecords encriptados (528 bytes) por compatibilidad
- No nuevos mensajes I2NP
- Mantener el tamaño de los registros de construcción encriptados para compatibilidad
- Añadir secreto hacia adelante para los Mensajes de Construcción de Túneles.
- Añadir encriptación autenticada
- Detectar la reordenación de saltos en los BuildRequestRecords
- Aumentar la resolución de la marca de tiempo para que el tamaño del filtro de Bloom pueda reducirse
- Añadir campo para la expiración del túnel para que puedan ser posibles duraciones de túnel variables (sólo en túneles totalmente ECIES)
- Añadir campo de opciones extensibles para funciones futuras
- Reutilizar primitivas criptográficas existentes
- Mejorar la seguridad del mensaje de construcción del túnel donde sea posible, manteniendo la compatibilidad
- Soportar túneles con pares ElGamal/ECIES mixtos
- Mejorar las defensas contra ataques de "etiquetado" en los mensajes de construcción
- Los saltos no necesitan conocer el tipo de encriptación del siguiente salto antes de procesar el mensaje de construcción,
  ya que pueden no tener el RI del siguiente salto en ese momento
- Maximizar la compatibilidad con la red actual
- No cambiar la encriptación de petición/respuesta AES de construcción de túnel para routers ElGamal
- No cambiar la encriptación "en capa" AES de túneles, para eso ver [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Continuar soportando tanto TBM/TBRM de 8 registros como VTBM/VTBRM de tamaño variable
- No requerir una actualización de "día de bandera" para toda la red


### No Objetivos

- Rediseño completo de los mensajes de construcción de túneles que requiera un "día de bandera".
- Reducir el tamaño de los mensajes de construcción de túneles (requiere todos los saltos ECIES y una nueva propuesta)
- Uso de opciones de construcción de túneles como se define en [Prop143](/en/proposals/143-build-message-options/), sólo requerido para mensajes pequeños
- Túneles bidireccionales - para eso ver [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Mensajes de construcción de túneles más pequeños - para eso ver [Prop157](/en/proposals/157-new-tbm/)


## Modelo de Amenazas

### Objetivos de Diseño

- Ningún salto es capaz de determinar el originador del túnel.

- Los saltos intermedios no deben poder determinar la dirección del túnel
  o su posición en el túnel.

- Ningún salto puede leer ningún contenido de otras peticiones o registros de respuesta, excepto
  para el hash del router truncado y clave efímera para el siguiente salto

- Ningún miembro del túnel de respuesta para la construcción saliente puede leer ningún registro de respuesta.

- Ningún miembro del túnel saliente para la construcción entrante puede leer ningún registro de petición,
  excepto que OBEP puede ver el hash del router truncado y clave efímera para IBGW




### Ataques de Etiquetado

Un objetivo principal del diseño de construcción de túneles es hacer más difícil
para los routers coludidos X e Y saber si están en un túnel único.
Si el router X está en el salto m y el router Y está en el salto m+1, obviamente lo sabrán.
Pero si el router X está en el salto m y el router Y está en el salto m+n para n>1, esto debería ser mucho más difícil.

Los ataques de etiquetado son aquellos en los que el router del medio del salto X altera el mensaje de construcción de túnel de tal manera que
el router Y puede detectar la alteración cuando el mensaje de construcción llega allí.
El objetivo es que cualquier mensaje alterado sea descartado por un router entre X e Y antes de que llegue al router Y.
Para modificaciones que no sean descartadas antes del router Y, el creador del túnel debería detectar la corrupción en la respuesta
y descartar el túnel.

Posibles ataques:

- Alterar un registro de construcción
- Reemplazar un registro de construcción
- Añadir o eliminar un registro de construcción
- Reordenar los registros de construcción




TODO: ¿El diseño actual previene todos estos ataques?






## Diseño

### Marco del Protocolo Noise

Esta propuesta proporciona los requisitos basados en el Marco del Protocolo Noise
[NOISE](https://noiseprotocol.org/noise.html) (Revisión 34, 2018-07-11).
En la jerga de Noise, Alice es la iniciadora, y Bob es el respondedor.

Esta propuesta se basa en el protocolo Noise Noise_N_25519_ChaChaPoly_SHA256.
Este protocolo Noise utiliza las siguientes primitivas:

- Patrón de Análisis Unidireccional: N
  Alice no transmite su clave estática a Bob (N)

- Función DH: X25519
  X25519 DH con una longitud de clave de 32 bytes como se especifica en [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Función de Cifrado: ChaChaPoly
  AEAD_CHACHA20_POLY1305 como se especifica en [RFC-7539](https://tools.ietf.org/html/rfc7539) sección 2.8.
  12 byte nonce, con los primeros 4 bytes establecidos en cero.
  Idéntico al mencionado en [NTCP2](/en/docs/spec/ntcp2/).

- Función de Hash: SHA256
  Hash estándar de 32 bytes, ya utilizado extensamente en I2P.


Adiciones al Marco
````````````````````````````

Ninguna.


### Patrones de Análisis

Los análisis utilizan patrones de análisis [Noise](https://noiseprotocol.org/noise.html).

La siguiente correspondencia de letras se utiliza:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje

La solicitud de construcción es idéntica al patrón Noise N.
Esto es también idéntico a la primera (Solicitud de Sesión) mensaje en el patrón XK utilizado en [NTCP2](/en/docs/spec/ntcp2/).


  ```dataspec

<- s
  ...
  e es p ->





  ```


### Encriptación de Solicitud

Los registros de solicitud de construcción son creados por el creador del túnel y encriptados asimétricamente al salto individual.
Esta encriptación asimétrica de registros de solicitud es actualmente ElGamal como se define en [Cryptography](/en/docs/spec/cryptography/)
y contiene un checksum SHA-256. Este diseño no es secreto hacia adelante.

El nuevo diseño utilizará el patrón unidireccional Noise "N" con ECIES-X25519 DH efímero-estático, con un HKDF, y
ChaCha20/Poly1305 AEAD para secreto hacia adelante, integridad y autenticación.
Alice es la solicitante de construcción de túnel. Cada salto en el túnel es un Bob.


(Propiedades de Seguridad de la Carga Útil)

  ```text

N:                      Autenticación   Confidencialidad
    -> e, es                  0                2

    Autenticación: Ninguna (0).
    Esta carga útil puede haber sido enviada por cualquier parte, incluyendo un atacante activo.

    Confidencialidad: 2.
    Encriptado para un destinatario conocido, secreto hacia adelante sólo para el compromiso del remitente,
    vulnerable a repeticiones. Esta carga útil está encriptada basada únicamente en DHs
    involucrando el par de claves estáticas del destinatario. Si la clave privada estática del destinatario es comprometida,
    incluso en una fecha posterior, esta carga útil puede ser desencriptada. Este mensaje
    también puede ser repetido, ya que no hay contribución efímera del destinatario.

    "e": Alice genera un nuevo par de claves efímeras y las almacena en la variable e,
         escribe la clave pública efímera como texto claro en el búfer de mensajes,
         y hashea la clave pública junto con el viejo h para
         derivar un nuevo h.

    "es": Se realiza un DH entre la clave efímera de Alice y el par de claves estáticas de
          Bob. El resultado es hasheado junto con el viejo ck para
          derivar un nuevo ck y k, y n se establece en cero.





  ```



### Encriptación de Respuesta

Los registros de respuesta de construcción son creados por el creador de los saltos y encriptados simétricamente al creador.
Esta encriptación simétrica de registros de respuesta es actualmente AES con un checksum SHA-256 añadido.
y contiene un checksum SHA-256. Este diseño no es secreto hacia adelante.

El nuevo diseño utilizará ChaCha20/Poly1305 AEAD para integridad y autenticación.


### Justificación

La clave pública efímera en la solicitud no necesita ser ofuscada con AES
o Elligator2. El salto anterior es el único que puede verla, y ese salto
sabe que el siguiente salto es ECIES.

Los registros de respuesta no necesitan encriptación asimétrica completa con otro DH.



## Especificación



### Registros de Solicitud de Construcción

Los BuildRequestRecords encriptados son de 528 bytes para ambos ElGamal y ECIES, por compatibilidad.


Registro de Solicitud Desencriptado (ElGamal)
```````````````````````````````````````````````

Para referencia, esta es la actual especificación del registro de BuildRequestRecord de túnel para routers ElGamal, tomada de [I2NP](/en/docs/spec/i2np/).
Los datos desencriptados se anteponen con un byte distinto de cero y el hash SHA-256 de los datos antes de la encriptación,
como se define en [Cryptography](/en/docs/spec/cryptography/).

Todos los campos son en big-endian.

Tamaño desencriptado: 222 bytes

  ```dataspec


bytes     0-3: ID de túnel para recibir mensajes, no cero
  bytes    4-35: hash de identidad local del router
  bytes   36-39: siguiente ID de túnel, no cero
  bytes   40-71: hash de identidad del siguiente router
  bytes  72-103: clave de capa de túnel AES-256
  bytes 104-135: clave IV de túnel AES-256
  bytes 136-167: clave de respuesta AES-256
  bytes 168-183: IV de respuesta AES-256
  byte      184: banderas
  bytes 185-188: hora de solicitud (en horas desde la época, redondeado hacia abajo)
  bytes 189-192: siguiente ID de mensaje
  bytes 193-221: relleno aleatorio / no interpretado




  ```


Registro de Solicitud Encriptado (ElGamal)
`````````````````````````````````````````

Para referencia, esta es la actual especificación del registro de BuildRequestRecord de túnel para routers ElGamal, tomada de [I2NP](/en/docs/spec/i2np/).

Tamaño encriptado: 528 bytes

  ```dataspec


bytes    0-15: hash de identidad truncado del salto
  bytes  16-528: ElGamal BuildRequestRecord encriptado




  ```




Registro de Solicitud Desencriptado (ECIES)
```````````````````````````````````````````

Esta es la especificación propuesta del registro de BuildRequestRecord de túnel para routers ECIES-X25519.
Resumen de cambios:

- Eliminar hash de router de 32 bytes no utilizado
- Cambiar hora de solicitud de horas a minutos
- Añadir campo de expiración para futuros tiempos de túnel variables
- Añadir más espacio para banderas
- Añadir Mapeo para opciones adicionales de construcción
- Las claves AES-256 de respuesta e IV no se utilizan para el propio registro de respuesta del salto
- El registro desencriptado es más largo debido a que hay una menor sobrecarga de encriptación


El registro de solicitud no contiene ninguna clave de respuesta ChaCha.
Esas claves se derivan de un KDF. Ver abajo.

Todos los campos son en big-endian.

Tamaño desencriptado: 464 bytes

  ```dataspec


bytes     0-3: ID de túnel para recibir mensajes, no cero
  bytes     4-7: siguiente ID de túnel, no cero
  bytes    8-39: hash de identidad del siguiente router
  bytes   40-71: clave de capa de túnel AES-256
  bytes  72-103: clave IV de túnel AES-256
  bytes 104-135: clave de respuesta AES-256
  bytes 136-151: IV de respuesta AES-256
  byte      152: banderas
  bytes 153-155: más banderas, no usadas, establecer en 0 por compatibilidad
  bytes 156-159: hora de solicitud (en minutos desde la época, redondeada hacia abajo)
  bytes 160-163: expiración de solicitud (en segundos desde la creación)
  bytes 164-167: siguiente ID de mensaje
  bytes   168-x: opciones de construcción de túnel (Mapeo)
  bytes     x-x: otros datos como se indica por las banderas o opciones
  bytes   x-463: relleno aleatorio




  ```

El campo de banderas es el mismo que se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/) y contiene lo siguiente::

 Orden de bits: 76543210 (bit 7 es MSB)
 bit 7: si está establecido, permite mensajes de cualquiera
 bit 6: si está establecido, permite mensajes a cualquiera, y envía la respuesta al
        salto siguiente especificado en un Mensaje de Respuesta de Construcción de Túnel
 bits 5-0: No definido, se debe establecer en 0 por compatibilidad con futuras opciones

El bit 7 indica que el salto será una puerta de enlace de entrada (IBGW).  El bit 6
indica que el salto será un punto final de salida (OBEP).  Si ninguno de los bits está
establecido, el salto será un participante intermedio.  Ambos no pueden ser establecidos al mismo tiempo.

La expiración de la solicitud es para una futura duración variable de túnel.
Por ahora, el único valor soportado es 600 (10 minutos).

Las opciones de construcción del túnel es una estructura de Mapeo como se define en [Common](/en/docs/spec/common-structures/).
Esto es para uso futuro. Actualmente no se definen opciones.
Si la estructura de Mapeo está vacía, es de dos bytes 0x00 0x00.
El tamaño máximo del Mapeo (incluyendo el campo de longitud) es 296 bytes,
y el valor máximo del campo de longitud del Mapeo es 294.



Registro de Solicitud Encriptado (ECIES)
```````````````````````````````````````

Todos los campos son en big-endian excepto por la clave pública efímera que es little-endian.

Tamaño encriptado: 528 bytes

  ```dataspec


bytes    0-15: hash de identidad truncado del salto
  bytes   16-47: clave pública X25519 efímera del remitente
  bytes  48-511: BuildRequestRecord ChaCha20 encriptado
  bytes 512-527: MAC Poly1305




  ```



### Registros de Respuesta de Construcción

Los BuildReplyRecords encriptados son de 528 bytes para ambos ElGamal y ECIES, por compatibilidad.


Registro de Respuesta Desencriptado (ElGamal)
`````````````````````````````````````````````
Las respuestas ElGamal son encriptadas con AES.

Todos los campos son en big-endian.

Tamaño desencriptado: 528 bytes

  ```dataspec


bytes   0-31: Hash SHA-256 de los bytes 32-527
  bytes 32-526: datos aleatorios
  byte     527: respuesta

  longitud total: 528




  ```


Registro de Respuesta Desencriptado (ECIES)
`````````````````````````````````````````````
Esta es la especificación propuesta del registro de BuildReplyRecord de túnel para routers ECIES-X25519.
Resumen de cambios:

- Añadir Mapeo para opciones de respuesta de construcción
- El registro desencriptado es más largo debido a que hay una menor sobrecarga de encriptación

Las respuestas ECIES son encriptadas con ChaCha20/Poly1305.

Todos los campos son en big-endian.

Tamaño desencriptado: 512 bytes

  ```dataspec


bytes    0-x: Opciones de Respuesta de Construcción de Túnel (Mapeo)
  bytes    x-x: otros datos como se indica por las opciones
  bytes  x-510: Relleno aleatorio
  byte     511: Byte de Respuesta




  ```

Las opciones de respuesta de construcción del túnel es una estructura de Mapeo como se define en [Common](/en/docs/spec/common-structures/).
Esto es para uso futuro. Actualmente no se definen opciones.
Si la estructura de Mapeo está vacía, es de dos bytes 0x00 0x00.
El tamaño máximo del Mapeo (incluyendo el campo de longitud) es 511 bytes,
y el valor máximo del campo de longitud del Mapeo es 509.

El byte de respuesta es uno de los siguientes valores
como se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/) para evitar la diferenciación:

- 0x00 (aceptar)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Registro de Respuesta Encriptado (ECIES)
`````````````````````````````````````````

Tamaño encriptado: 528 bytes

  ```dataspec


bytes   0-511: BuildReplyRecord ChaCha20 encriptado
  bytes 512-527: MAC Poly1305




  ```

Después de la transición completa a registros ECIES, las reglas de relleno son las mismas que para los registros de solicitud.


### Encriptación Simétrica de Registros

Se permiten túneles mixtos, y son necesarios, para la transición de ElGamal a ECIES.
Durante el período de transición, habrá un número creciente de routers con claves bajo ECIES.

El preprocesamiento de criptografía simétrica funcionará de la misma manera:

- "encriptación":

  - el cifrador se ejecuta en modo de desencriptación
  - los registros de solicitud se desencriptan preventivamente en el preprocesamiento (ocultando los registros de solicitud encriptados)

- "desencriptación":

  - el cifrador se ejecuta en modo de encriptación
  - los registros de solicitud se encriptan (revelando el siguiente registro de solicitud de texto claro) por los saltos participantes

- ChaCha20 no tiene "modos", por lo que simplemente se ejecuta tres veces:

  - una vez en el preprocesamiento
  - una vez por el salto
  - una vez en el procesamiento final de respuesta

Cuando se utilizan túneles mixtos, los creadores de túneles deberán basar la encriptación simétrica
de BuildRequestRecord en el tipo de encriptación del salto actual y anterior.

Cada salto utilizará su propio tipo de encriptación para encriptar BuildReplyRecords y los otros
registros en el VariableTunnelBuildMessage (VTBM).

En la ruta de respuesta, el punto final (emisor) necesitará deshacer la [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), utilizando la clave de respuesta de cada salto.

Como ejemplo aclarativo, veamos un túnel saliente con ECIES rodeado de ElGamal:

- Emisor (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Todos los BuildRequestRecords están en su estado encriptado (usando ElGamal o ECIES).

El cifrador AES256/CBC, cuando se usa, todavía se usa para cada registro, sin encadenamiento a través de múltiples registros.

Del mismo modo, ChaCha20 se utilizará para encriptar cada registro, no se reproduce a través del VTBM completo.

Los registros de solicitud son preprocesados por el Emisor (OBGW):

- El registro de H3 es "encriptado" usando:

  - la clave de respuesta de H2 (ChaCha20)
  - la clave de respuesta de H1 (AES256/CBC)

- El registro de H2 es "encriptado" usando:

  - la clave de respuesta de H1 (AES256/CBC)

- El registro de H1 sale sin encriptación simétrica

Solo H2 verifica la bandera de encriptación de respuesta, y ve que está seguido por AES256/CBC.

Después de ser procesados por cada salto, los registros están en un estado "desencriptado":

- El registro de H3 es "desencriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)

- El registro de H2 es "desencriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)
  - la clave de respuesta de H2 (ChaCha20-Poly1305)

- El registro de H1 es "desencriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)
  - la clave de respuesta de H2 (ChaCha20)
  - la clave de respuesta de H1 (AES256/CBC)

El creador del túnel, también conocido como Punto Final de Entrada (IBEP), postprocesa la respuesta:

- El registro de H3 es "encriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)

- El registro de H2 es "encriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)
  - la clave de respuesta de H2 (ChaCha20-Poly1305)

- El registro de H1 es "encriptado" usando:

  - la clave de respuesta de H3 (AES256/CBC)
  - la clave de respuesta de H2 (ChaCha20)
  - la clave de respuesta de H1 (AES256/CBC)


### Claves de Registro de Solicitud (ECIES)

Estas claves se incluyen explícitamente en los BuildRequestRecords de ElGamal.
Para los BuildRequestRecords de ECIES, las claves de túnel y las claves de respuesta AES están incluidas,
pero las claves de respuesta ChaCha se derivan del intercambio DH.
Ver [Prop156](/en/proposals/156-ecies-routers/) para detalles de las claves estáticas ECIES del router.

A continuación se describe cómo derivar las claves que antes se transmitían en los registros de solicitud.


KDF para ck y h Inicial
````````````````````````

Esto es estándar [NOISE](https://noiseprotocol.org/noise.html) para el patrón "N" con un nombre de protocolo estándar.

  ```text

Este es el patrón de mensaje "e":

  // Definir protocol_name.
  Establecer protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, codificado en US-ASCII, sin terminación NULL).

  // Definir Hash h = 32 bytes
  // Rellenar hasta 32 bytes. NO lo hashees, porque no es más de 32 bytes.
  h = protocol_name || 0

  Definir ck = cadena de claves de 32 bytes. Copiar los datos de h a ck.
  Establecer chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // hasta aquí, todo puede ser precalculado por todos los routers.




  ```


KDF para Registro de Solicitud
````````````````````````````````

Los creadores de túnel ElGamal generan un par de claves efímeras X25519 para cada
salto ECIES en el túnel, y utilizan el esquema anterior para encriptar sus BuildRequestRecord.
Los creadores de túnel ElGamal usarán el esquema anterior para encriptar a saltos ElGamal.

Los creadores de túneles ECIES necesitarán encriptar a cada clave pública de salto ElGamal usando el
esquema definido en [Tunnel-Creation](/en/docs/spec/tunnel-creation/). Los creadores de túneles ECIES utilizarán el esquema anterior para encriptar
a saltos ECIES.

Esto significa que los saltos de túnel sólo verán registros encriptados con su mismo tipo de encriptación.

Para los creadores de túneles ElGamal y ECIES, deberán generar pares de claves efímeras X25519 únicas
por salto para encriptar a los saltos ECIES.

**IMPORTANTE**:
Las claves efímeras deben ser únicas por salto ECIES, y por registro de construcción.
No usar claves únicas abre una vector de ataque para que los saltos coludidos confirmen que están en el mismo túnel.


  ```dataspec


// Cada par de claves estáticas X25519 del salto (hesk, hepk) de la Identidad del Router
  hesk = GENERAR_PRIVADA()
  hepk = DERIVAR_PÚBLICA(hesk)

  // MixHash(hepk)
  // || abajo significa añadir
  h = SHA256(h || hepk);

  // hasta aquí, todo puede ser precalculado por cada router
  // para todas las solicitudes de construcción entrantes

  // El remitente genera un par de claves efímeras X25519 por salto ECIES en el VTBM (sesk, sepk)
  sesk = GENERAR_PRIVADA()
  sepk = DERIVAR_PÚBLICA(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Fin del patrón de mensaje "e".

  Este es el patrón de mensaje "es":

  // Noise es
  // El remitente realiza un DH X25519 con la clave pública estática del salto.
  // Cada Salto, encuentra el registro con su hash de identidad truncado,
  // y extrae la clave efímera del remitente que precede al registro encriptado.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // parámetros ChaChaPoly para encriptar/desencriptar
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Guardar para KDF de Registro de Respuesta
  cadenaClave = keydata[0:31]

  // parámetros AEAD
  k = keydata[32:63]
  n = 0
  texto = 464 bytes de registro de solicitud de construcción
  ad = h
  textoCifrado = ENCRYPT(k, n, texto, ad)

  Fin del patrón de mensaje "es".

  // MixHash(textoCifrado)
  // Guardar para KDF de Registro de Respuesta
  h = SHA256(h || textoCifrado)





  ```

``replyKey``, ``layerKey`` y ``layerIV`` aún deben incluirse dentro de los registros ElGamal,
y pueden generarse aleatoriamente.


### Encriptación de Registro de Solicitud (ElGamal)

Como se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
No hay cambios en la encriptación para saltos ElGamal.




### Encriptación de Registro de Respuesta (ECIES)

El registro de respuesta es encriptado con ChaCha20/Poly1305.

  ```dataspec


// parámetros AEAD
  k = cadenaClave de la solicitud de construcción
  n = 0
  texto = 512 bytes de registro de respuesta de construcción
  ad = h de la solicitud de construcción

  textoCifrado = ENCRYPT(k, n, texto, ad)




  ```



### Encriptación de Registro de Respuesta (ElGamal)

Como se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/).
No hay cambios en la encriptación para saltos ElGamal.



### Análisis de Seguridad

ElGamal no proporciona secreto hacia adelante para Mensajes de Construcción de Túneles.

AES256/CBC se encuentra en una posición ligeramente mejor, siendo vulnerable solo a un debilitamiento teórico de un
ataque `biclique` de texto claro conocido.

El único ataque práctico conocido contra AES256/CBC es un ataque oracle de relleno, cuando el IV es conocido por el atacante.

Un atacante necesitaría romper la encriptación ElGamal del siguiente salto para obtener la información de clave AES256/CBC (clave de respuesta e IV).

ElGamal es significativamente más intensivo en CPU que ECIES, lo que lleva a un posible agotamiento de recursos.

ECIES, utilizado con nuevas claves efímeras por-BuildRequestRecord o VariableTunnelBuildMessage, proporciona secreto hacia adelante.

ChaCha20Poly1305 proporciona encriptación AEAD, permitiendo al destinatario verificar la integridad del mensaje antes de intentar desencriptarlo.


## Justificación

Este diseño maximiza la reutilización de primitivas criptográficas, protocolos y código existentes.
Este diseño minimiza el riesgo.




## Notas de Implementación

* Los routers más antiguos no verifican el tipo de encriptación del salto y enviarán registros encriptados con ElGamal.
  Algunos routers recientes tienen fallas y enviarán varios tipos de registros malformados.
  Los implementadores deberían detectar y rechazar estos registros antes de la operación DH
  si es posible, para reducir el uso de la CPU.


## Problemas



## Migración

Ver [Prop156](/en/proposals/156-ecies-routers/).



