---
title: "NTCP (TCP basado en NIO)"
description: "Transporte TCP heredado basado en Java NIO para I2P, reemplazado por NTCP2"
slug: "ntcp"
aliases:
  - "/es/docs/transport/ntcp"
  - "/es/docs/transport/ntcp/"
  - "/es/docs/ntcp"
  - "/es/docs/ntcp/"
  - "/es/ntcp"
  - "/es/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

OBSOLETO, YA NO ES COMPATIBLE. Deshabilitado por defecto desde 0.9.40 2019-05. Soporte eliminado desde 0.9.50 2021-05. Reemplazado por [NTCP2](/docs/specs/ntcp2). NTCP es un transporte basado en Java NIO introducido en la versión 0.6.1.22 de I2P. Java NIO (nuevo I/O) no sufre los problemas de 1 hilo por conexión del antiguo transporte TCP. NTCP-over-IPv6 es compatible desde la versión 0.9.8.

Por defecto, NTCP utiliza la IP/Puerto detectada automáticamente por SSU. Cuando se habilita en config.jsp, SSU notificará/reiniciará NTCP cuando cambie la dirección externa o cuando cambie el estado del firewall. Ahora puedes habilitar TCP entrante sin una IP estática o servicio dyndns.

El código NTCP dentro de I2P es relativamente ligero (1/4 del tamaño del código SSU) porque utiliza el transporte TCP de Java subyacente para la entrega confiable.

## Especificación de Dirección del Router {#ra}

Las siguientes propiedades se almacenan en la base de datos de red.

- **Nombre del transporte:** NTCP
- **host:** IP (IPv4 o IPv6).
  Se permite dirección IPv6 acortada (con "::").
  Anteriormente se permitían nombres de host, pero están obsoletos desde la versión 0.9.32. Ver propuesta 141.
- **port:** 1024 - 65535

## Especificación del Protocolo NTCP

### Formato de Mensaje Estándar

Después del establecimiento, el transporte NTCP envía mensajes I2NP individuales, con una suma de verificación simple. El mensaje no cifrado se codifica de la siguiente manera:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Los datos se cifran entonces con AES/256/CBC. La clave de sesión para el cifrado se negocia durante el establecimiento (usando Diffie-Hellman de 2048 bits). El establecimiento entre dos routers se implementa en la clase EstablishState y se detalla a continuación. El IV para el cifrado AES/256/CBC son los últimos 16 bytes del mensaje cifrado anterior.

Se requieren de 0 a 15 bytes de relleno para que la longitud total del mensaje (incluyendo los seis bytes de tamaño y suma de verificación) sea un múltiplo de 16. El tamaño máximo del mensaje es actualmente de 16 KB. Por lo tanto, el tamaño máximo de datos es actualmente de 16 KB - 6, o 16378 bytes. El tamaño mínimo de datos es 1.

### Formato del Mensaje de Sincronización de Tiempo

Un caso especial es un mensaje de metadatos donde el sizeof(data) es 0. En ese caso, el mensaje no cifrado se codifica como:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Longitud total: 16 bytes. El mensaje de sincronización de tiempo se envía aproximadamente cada 15 minutos. El mensaje se cifra de la misma manera que los mensajes estándar.

### Sumas de verificación

Los mensajes estándar y de sincronización de tiempo utilizan la suma de verificación Adler-32 tal como se define en la [Especificación ZLIB](http://tools.ietf.org/html/rfc1950).

### Tiempo de espera de inactividad

El tiempo de espera de inactividad y el cierre de conexión queda a discreción de cada endpoint y puede variar. La implementación actual reduce el tiempo de espera cuando el número de conexiones se acerca al máximo configurado, y aumenta el tiempo de espera cuando el número de conexiones es bajo. El tiempo de espera mínimo recomendado es de dos minutos o más, y el tiempo de espera máximo recomendado es de diez minutos o más.

### Intercambio de RouterInfo

Después del establecimiento, y cada 30-60 minutos a partir de entonces, los dos routers generalmente deberían intercambiar RouterInfos usando un DatabaseStoreMessage. Sin embargo, Alice debería verificar si el primer mensaje en cola es un DatabaseStoreMessage para no enviar un mensaje duplicado; esto suele ocurrir cuando se conecta a un router floodfill.

### Secuencia de Establecimiento

En el estado de establecimiento, hay una secuencia de mensajes de 4 fases para intercambiar claves DH y firmas. En los primeros dos mensajes hay un intercambio Diffie Hellman de 2048 bits. Luego, se intercambian firmas de los datos críticos para confirmar la conexión.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### Intercambio de Claves DH {#DH}

El intercambio de claves DH inicial de 2048 bits utiliza el mismo primo compartido (p) y generador (g) que se usa para el [cifrado ElGamal](/docs/specs/cryptography#elgamal) de I2P.

El intercambio de claves DH consiste en una serie de pasos, mostrados a continuación. La correspondencia entre estos pasos y los mensajes enviados entre routers I2P, está marcada en negrita.

1. Alice genera un entero secreto x. Luego calcula `X = g^x mod p`.
2. Alice envía X a Bob **(Mensaje 1)**.
3. Bob genera un entero secreto y. Luego calcula `Y = g^y mod p`.
4. Bob envía Y a Alice. **(Mensaje 2)**
5. Alice ahora puede calcular `sessionKey = Y^x mod p`.
6. Bob ahora puede calcular `sessionKey = X^y mod p`.
7. Tanto Alice como Bob ahora tienen una clave compartida `sessionKey = g^(x*y) mod p`.

La sessionKey se utiliza entonces para intercambiar identidades en **Mensaje 3** y **Mensaje 4**. La longitud del exponente (x e y) para el intercambio DH está documentada en la [página de criptografía](/docs/specs/cryptography#exponent).

#### Detalles de la Clave de Sesión

La clave de sesión de 32 bytes se crea de la siguiente manera:

1. Tomar la clave DH intercambiada, representada como un array de bytes BigInteger de longitud mínima positiva (complemento a dos big-endian)
2. Si el bit más significativo es 1 (es decir, array[0] & 0x80 != 0), anteponer un byte 0x00, como en la representación BigInteger.toByteArray() de Java
3. Si ese array de bytes es mayor o igual a 32 bytes, usar los primeros 32 bytes (más significativos)
4. Si ese array de bytes es menor a 32 bytes, agregar bytes 0x00 para extender a 32 bytes. *(extremadamente improbable)*

#### Mensaje 1 (Solicitud de Sesión)

Esta es la solicitud DH. Alice ya tiene la [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) de Bob, la dirección IP y el puerto, tal como se contiene en su [Router Info](/docs/specs/common-structures#struct_RouterInfo), que fue publicada en la [network database](/docs/overview/network-database). Alice envía a Bob:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Contenidos:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Notas:**

- Bob verifica HXxorHI usando su propio hash de router. Si no se verifica, Alice ha contactado al router incorrecto, y Bob cierra la conexión.

#### Mensaje 2 (Sesión Creada)

Esta es la respuesta DH. Bob le envía a Alice:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Contenidos sin cifrar:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Contenidos Cifrados:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Notas:**

- Alice puede descartar la conexión si la desviación del reloj con Bob es demasiado alta según se calcula usando tsB.

#### Mensaje 3 (Confirmación de Sesión A)

Esto contiene la identidad del router de Alice, y una firma de los datos críticos. Alice envía a Bob:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Contenidos sin cifrar:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Contenidos Cifrados:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Notas:**

- Bob verifica la firma, y en caso de fallo, abandona la conexión.
- Bob puede abandonar la conexión si la desviación del reloj con Alice es demasiado alta según se calcula usando tsA.
- Alice usará los últimos 16 bytes del contenido cifrado de este mensaje como el IV para el siguiente mensaje.
- Hasta la versión 0.9.15, la router identity siempre era de 387 bytes, la firma siempre era una firma DSA de 40 bytes, y el padding siempre era de 15 bytes. A partir de la versión 0.9.16, la router identity puede ser más larga de 387 bytes, y el tipo y longitud de la firma están implícitos por el tipo de la [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) en la [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) de Alice. El padding es el necesario para un múltiplo de 16 bytes para todo el contenido sin cifrar.
- La longitud total del mensaje no puede determinarse sin descifrarlo parcialmente para leer la Router Identity. Como la longitud mínima de la Router Identity es 387 bytes, y la longitud mínima de Signature es 40 (para DSA), el tamaño total mínimo del mensaje es 2 + 387 + 4 + (longitud de la firma) + (padding a 16 bytes), o 2 + 387 + 4 + 40 + 15 = 448 para DSA. El receptor podría leer esa cantidad mínima antes del descifrado para determinar la longitud real de la Router Identity. Para Certificates pequeños en la Router Identity, eso probablemente será todo el mensaje, y no habrá más bytes en el mensaje que requieran una operación de descifrado adicional.

#### Mensaje 4 (Confirmación de Sesión B)

Esta es una firma de los datos críticos. Bob le envía a Alice:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Contenidos sin cifrar:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Contenidos Encriptados:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Notas:**

- Alice verifica la firma, y en caso de fallo, desconecta la conexión.
- Bob utilizará los últimos 16 bytes del contenido cifrado de este mensaje como el IV para el siguiente mensaje.
- Hasta la versión 0.9.15, la firma siempre era una firma DSA de 40 bytes y el relleno siempre era de 8 bytes. A partir de la versión 0.9.16, el tipo y longitud de la firma están implícitos en el tipo de la [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) en la [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) de Bob. El relleno es el necesario para completar un múltiplo de 16 bytes para todo el contenido sin cifrar.

#### Después del Establecimiento

Se establece la conexión y pueden intercambiarse mensajes estándar o de sincronización de tiempo. Todos los mensajes posteriores están cifrados con AES usando la clave de sesión DH negociada. Alice utilizará los últimos 16 bytes del contenido cifrado del mensaje #3 como el siguiente IV. Bob utilizará los últimos 16 bytes del contenido cifrado del mensaje #4 como el siguiente IV.

### Mensaje de Verificación de Conexión

Alternativamente, cuando Bob recibe una conexión, podría ser una conexión de verificación (quizás iniciada por Bob pidiendo a alguien que verifique su listener). Check Connection no se usa actualmente. Sin embargo, para el registro, las conexiones de verificación se formatean de la siguiente manera. Una conexión de información de verificación recibirá 256 bytes que contienen:

- 32 bytes de datos no interpretados e ignorados
- 1 byte de tamaño
- esa cantidad de bytes que conforman la dirección IP del router local (tal como es alcanzado por el lado remoto)
- 2 bytes del número de puerto en el que se alcanzó el router local
- 4 bytes del tiempo de red i2p según lo conoce el lado remoto (segundos desde la época)
- datos de relleno no interpretados, hasta el byte 223
- xor del hash de identidad del router local y el SHA256 de los bytes 32 hasta los bytes 223

La verificación de conexión está completamente deshabilitada a partir de la versión 0.9.12.

## Discusión

Ahora en la [Página de Discusión NTCP](/docs/discussions/ntcp).

## Trabajo Futuro {#future}

- El tamaño máximo del mensaje debería incrementarse a aproximadamente 32 KB.

- Un conjunto de tamaños de paquete fijos puede ser apropiado para ocultar aún más la
  fragmentación de datos a adversarios externos, pero el relleno de tunnel, garlic y 
  extremo a extremo debería ser suficiente para la mayoría de necesidades hasta entonces.
  Sin embargo, actualmente no existe provisión para relleno más allá del siguiente límite de 16 bytes,
  para crear un número limitado de tamaños de mensaje.

- La utilización de memoria (incluyendo la del kernel) para NTCP debería compararse con la de SSU.

- ¿Pueden los mensajes de establecimiento ser rellenados aleatoriamente de alguna manera, para frustrar la identificación del tráfico I2P basada en los tamaños iniciales de paquetes?
