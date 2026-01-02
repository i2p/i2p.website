---
title: "Transporte NTCP2"
description: "Transporte TCP basado en Noise (marco de protocolos criptográficos) para enlaces de router a router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Descripción general

NTCP2 reemplaza el transporte NTCP heredado por un Noise-based handshake (protocolo de establecimiento de conexión basado en Noise) que resiste el fingerprinting de tráfico, cifra los campos de longitud y admite suites de cifrado modernas. Los routers pueden ejecutar NTCP2 junto con SSU2 como los dos protocolos de transporte obligatorios en la red I2P. NTCP (versión 1) se declaró obsoleto en la 0.9.40 (mayo de 2019) y se eliminó por completo en la 0.9.50 (mayo de 2021).

## Noise Protocol Framework (marco de protocolos criptográficos Noise)

NTCP2 usa el Noise Protocol Framework (marco del protocolo Noise) [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) con extensiones específicas de I2P:

- **Patrón**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Identificador extendido**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (para la inicialización del KDF)
- **Función DH**: X25519 (RFC 7748) - claves de 32 bytes, codificación little-endian (orden de bytes con el menos significativo primero)
- **Cifrado**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - Nonce de 12 bytes: primeros 4 bytes a cero, los últimos 8 bytes son un contador (little-endian)
  - Valor máximo del nonce: 2^64 - 2 (la conexión debe finalizar antes de alcanzar 2^64 - 1)
- **Función hash**: SHA-256 (salida de 32 bytes)
- **MAC**: Poly1305 (etiqueta de autenticación de 16 bytes)

### Extensiones específicas de I2P

1. **Ofuscación con AES**: Claves efímeras cifradas con AES-256-CBC usando el hash del router de Bob y un IV publicado
2. **Relleno aleatorio**: Relleno en claro en los mensajes 1-2 (autenticado), relleno AEAD en el mensaje 3+ (cifrado)
3. **Ofuscación de longitud con SipHash-2-4**: Longitudes de trama de dos bytes combinadas mediante XOR con la salida de SipHash
4. **Estructura de trama**: Tramas con prefijo de longitud para la fase de datos (compatibilidad con streaming TCP)
5. **Cargas útiles basadas en bloques**: Formato de datos estructurado con bloques tipados

## Flujo de negociación

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Negociación de tres mensajes

1. **SessionRequest** - la clave efímera ofuscada de Alice, opciones, indicaciones para el relleno
2. **SessionCreated** - la clave efímera ofuscada de Bob, opciones cifradas, relleno
3. **SessionConfirmed** - la clave estática cifrada de Alice y RouterInfo (información del router) (dos tramas AEAD)

### Patrones de mensajes de Noise (marco de protocolos criptográficos)

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Niveles de autenticación:** - 0: Sin autenticación (cualquier parte podría haberlo enviado) - 2: Autenticación del remitente resistente a la suplantación por compromiso de clave (KCI)

**Niveles de confidencialidad:** - 1: Receptor efímero (secreto hacia adelante, sin autenticación del receptor) - 2: Receptor conocido, secreto hacia adelante solo frente al compromiso del remitente - 5: Secreto hacia adelante fuerte (efímero-efímero + efímero-estático DH)

## Especificaciones de mensajes

### Notación de claves

- `RH_A` = Hash del Router para Alice (32 bytes, SHA-256)
- `RH_B` = Hash del Router para Bob (32 bytes, SHA-256)
- `||` = Operador de concatenación
- `byte(n)` = Un solo byte con valor n
- Todos los enteros de múltiples bytes son **big-endian** (orden de bytes con el más significativo primero) a menos que se especifique lo contrario
- Las claves X25519 son **little-endian** (orden de bytes con el menos significativo primero) (32 bytes)

### Cifrado autenticado (ChaCha20-Poly1305)

**Función de cifrado:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Parámetros:** - `key`: clave de cifrado de 32 bytes del KDF (función de derivación de claves) - `nonce`: 12 bytes (4 bytes a cero + contador de 8 bytes, little-endian (orden de bytes de menor a mayor)) - `associatedData`: hash de 32 bytes en la fase de handshake (negociación inicial); de longitud cero en la fase de datos - `plaintext`: Datos a cifrar (0+ bytes)

**Salida:** - Texto cifrado: Misma longitud que el texto plano - MAC: 16 bytes (etiqueta de autenticación Poly1305)

**Gestión de Nonce (número usado una vez):** - El contador empieza en 0 para cada instancia de cifrado - Se incrementa por cada operación AEAD en esa dirección - Contadores separados para Alice→Bob y Bob→Alice en la fase de datos - Debe terminarse la conexión antes de que el contador alcance 2^64 - 1

## Mensaje 1: Solicitud de sesión

Alice inicia la conexión con Bob.

**Operaciones de Noise (marco de protocolos criptográficos)**: `e, es` (generación e intercambio de claves efímeras)

### Formato sin procesar

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Restricciones de tamaño:** - Mínimo: 80 bytes (32 AES + 48 AEAD) - Máximo: 65535 bytes en total - **Caso especial**: Máx. 287 bytes al conectarse a direcciones "NTCP" (detección de versión)

### Contenido descifrado

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloque de opciones (16 bytes, big-endian, más significativo primero)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Campos críticos:** - **ID de red** (desde 0.9.42): Rechazo rápido de conexiones entre redes - **m3p2len**: Tamaño exacto de la parte 2 del mensaje 3 (debe coincidir al enviarse)

### Función de derivación de claves (KDF-1)

**Inicializar el protocolo:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Operaciones de MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Operación MixKey (patrón es):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Notas de implementación

1. **Ofuscación AES**: Usada solo para resistencia a DPI (inspección profunda de paquetes); cualquiera con el hash del router de Bob y el IV (vector de inicialización) puede descifrar X
2. **Prevención de repetición**: Bob debe almacenar en caché los valores X (o sus equivalentes cifrados) durante al menos 2*D segundos (D = desfase máximo del reloj)
3. **Validación de marca de tiempo**: Bob debe rechazar conexiones con |tsA - current_time| > D (normalmente D = 60 segundos)
4. **Validación de curva**: Bob debe verificar que X sea un punto X25519 válido
5. **Rechazo rápido**: Bob puede comprobar X[31] & 0x80 == 0 antes del descifrado (las claves X25519 válidas tienen el MSB (bit más significativo) a 0)
6. **Gestión de errores**: Ante cualquier fallo, Bob cierra con TCP RST tras un tiempo de espera aleatorio y la lectura de un número aleatorio de bytes
7. **Almacenamiento en búfer**: Alice debe vaciar todo el mensaje (incluido el relleno) de una vez para mayor eficiencia

## Mensaje 2: SessionCreated

Bob responde a Alice.

**Operaciones de Noise**: `e, ee` (DH efímero-efímero)

### Formato en bruto

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Contenido descifrado

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloque de opciones (16 bytes, big-endian (orden de bytes con el más significativo primero))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Función de derivación de claves (KDF-2)

**Operaciones de MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**Operación MixKey (función de mezcla de clave) (patrón ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Limpieza de memoria:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Notas de implementación

1. **Encadenamiento AES**: El cifrado de Y utiliza el estado AES-CBC del mensaje 1 (no se restablece)
2. **Prevención de repetición**: Alice debe almacenar en caché los valores Y durante al menos 2*D segundos
3. **Validación de marca de tiempo**: Alice debe rechazar |tsB - current_time| > D
4. **Validación de curva**: Alice debe verificar que Y sea un punto X25519 válido
5. **Manejo de errores**: Alice cierra con TCP RST ante cualquier fallo
6. **Almacenamiento en búfer**: Bob debe enviar de una vez el mensaje completo

## Mensaje 3: SessionConfirmed (confirmación de sesión)

Alice confirma la sesión y envía RouterInfo (información del router).

**Operaciones de Noise**: `s, se` (revelación de clave estática y DH estático-efímero)

### Estructura de dos partes

El Mensaje 3 consta de **dos tramas AEAD (cifrado autenticado con datos asociados) separadas**:

1. **Parte 1**: Trama fija de 48 bytes con la clave estática cifrada de Alice
2. **Parte 2**: Trama de longitud variable con RouterInfo (estructura de información del router), opciones y relleno

### Formato en bruto

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Restricciones de tamaño:** - Parte 1: Exactamente 48 bytes (32 de texto en claro + 16 de MAC) - Parte 2: Longitud especificada en el mensaje 1 (campo m3p2len) - Máximo total: 65535 bytes (parte 1 máx. 48, por lo tanto, parte 2 máx. 65487)

### Contenido descifrado

**Parte 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Parte 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Función de derivación de claves (KDF-3)

**Parte 1 (patrón s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Parte 2 (patrón se):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Limpieza de memoria:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Notas de implementación

1. **Validación de RouterInfo (información del router)**: Bob debe verificar la firma, la marca de tiempo y la coherencia de la clave
2. **Verificación de coincidencia de claves**: Bob debe verificar que la clave estática de Alice en la parte 1 coincida con la clave en el RouterInfo
3. **Ubicación de la clave estática**: Buscar un parámetro "s" coincidente en la RouterAddress (dirección del router) de NTCP o NTCP2
4. **Orden de bloques**: RouterInfo debe ir primero, Opciones en segundo lugar (si está presente), Relleno al final (si está presente)
5. **Planificación de la longitud**: Alice debe asegurarse de que m3p2len en el mensaje 1 coincida exactamente con la longitud de la parte 2
6. **Almacenamiento en búfer**: Alice debe enviar ambas partes juntas en un único envío TCP
7. **Encadenamiento opcional**: Alice puede adjuntar inmediatamente una trama de la fase de datos para mayor eficiencia

## Fase de datos

Una vez completado el handshake (establecimiento de conexión), todos los mensajes usan tramas AEAD (cifrado autenticado con datos asociados) de longitud variable con campos de longitud ofuscados.

### Función de derivación de claves (fase de datos)

**Función Split (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Derivación de claves de SipHash:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Estructura de la trama

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Limitaciones de la trama:** - Mínimo: 18 bytes (2 longitud ofuscada + 0 texto en claro + 16 MAC) - Máximo: 65537 bytes (2 longitud ofuscada + 65535 trama) - Recomendado: Unos pocos KB por trama (minimizar la latencia del receptor)

### Ofuscación de la longitud con SipHash (función hash autenticada)

**Propósito**: Evitar que la inspección profunda de paquetes (DPI) identifique los límites de las tramas

**Algoritmo:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Decodificación:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Notas:** - Cadenas de IV separadas para cada dirección (Alice→Bob y Bob→Alice) - Si SipHash devuelve uint64, use los 2 bytes menos significativos como máscara - Convierta el uint64 al siguiente IV como bytes en formato little-endian

### Formato de bloque

Cada trama contiene cero o más bloques:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Límites de tamaño:** - Trama máxima: 65535 bytes (incluye MAC) - Espacio máximo de bloque: 65519 bytes (trama - MAC de 16 bytes) - Bloque individual máximo: 65519 bytes (cabecera de 3 bytes + 65516 de datos)

### Tipos de bloques

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Reglas de orden de bloques:** - **Mensaje 3 parte 2**: RouterInfo, Options (opcional), Padding (opcional) - NO se permiten otros tipos - **Fase de datos**: Cualquier orden excepto:   - Padding DEBE ser el último bloque si está presente   - Termination DEBE ser el último bloque (excepto Padding) si está presente - Se permiten múltiples bloques de I2NP por trama - NO se permiten múltiples bloques de Padding por trama

### Tipo de bloque 0: Fecha y hora

Sincronización temporal para la detección de desfase del reloj.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Implementación**: Redondear al segundo más cercano para evitar la acumulación de desfase del reloj.

### Tipo de bloque 1: Opciones

Parámetros de relleno y de modelado del tráfico.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Relaciones de relleno** (número de punto fijo 4.4, value/16.0): - `tmin`: Proporción mínima de relleno de transmisión (0.0 - 15.9375) - `tmax`: Proporción máxima de relleno de transmisión (0.0 - 15.9375) - `rmin`: Proporción mínima de relleno de recepción (0.0 - 15.9375) - `rmax`: Proporción máxima de relleno de recepción (0.0 - 15.9375)

**Ejemplos:** - 0x00 = 0% de relleno - 0x01 = 6,25% de relleno - 0x10 = 100% de relleno (relación 1:1) - 0x80 = 800% de relleno (relación 8:1)

**Tráfico de relleno:** - `tdmy`: Máximo dispuesto a enviar (2 bytes, promedio en bytes/seg) - `rdmy`: Solicitado para recibir (2 bytes, promedio en bytes/seg)

**Inserción de retardo:** - `tdelay`: Máximo que se está dispuesto a insertar (2 bytes, promedio en milisegundos) - `rdelay`: Retardo solicitado (2 bytes, promedio en milisegundos)

**Directrices:** - Los valores mínimos indican la resistencia deseada al análisis de tráfico - Los valores máximos indican restricciones de ancho de banda - El emisor debe respetar el máximo del receptor - El emisor puede respetar el mínimo del receptor dentro de las restricciones - No existe un mecanismo de cumplimiento; las implementaciones pueden variar

### Tipo de bloque 2: RouterInfo

Distribución de RouterInfo para poblar y difundir la netdb.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Uso:**

**En el Mensaje 3 Parte 2** (handshake): - Alice envía su RouterInfo (información del router) a Bob - El Flood bit (bit de inundación) normalmente es 0 (almacenamiento local) - RouterInfo NO está comprimido con gzip

**En la fase de datos:** - Cualquiera de las partes puede enviar su RouterInfo actualizado - Flood bit = 1: Solicitar distribución mediante floodfill (si el receptor es floodfill) - Flood bit = 0: Solo almacenamiento local en netdb

**Requisitos de validación:** 1. Verificar que el tipo de firma sea compatible 2. Verificar la firma de RouterInfo 3. Verificar que la marca de tiempo esté dentro de límites aceptables 4. Para el handshake (negociación inicial): verificar que la clave estática coincida con el parámetro "s" de la dirección NTCP2 5. Para la fase de datos: verificar que el hash del router coincida con el par de la sesión 6. Solo propagar RouterInfos con direcciones publicadas

**Notas:** - Sin mecanismo de acuse de recibo (ACK) (use I2NP DatabaseStore con token de respuesta si es necesario) - Puede contener RouterInfos de terceros (registros de identidad de routers de I2P) (uso de floodfill) - NO comprimido con gzip (a diferencia de I2NP DatabaseStore)

### Tipo de bloque 3: Mensaje I2NP

Mensaje I2NP con encabezado abreviado de 9 bytes.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Diferencias con NTCP1:** - Expiración: 4 bytes (segundos) frente a 8 bytes (milisegundos) - Longitud: Omitida (deducible a partir de la longitud del bloque) - Suma de verificación: Omitida (AEAD proporciona integridad) - Encabezado: 9 bytes frente a 16 bytes (reducción del 44%)

**Fragmentación:** - Los mensajes I2NP NO DEBEN fragmentarse entre bloques - Los mensajes I2NP NO DEBEN fragmentarse entre tramas - Se permiten múltiples bloques I2NP por trama

### Tipo de bloque 4: Terminación

Cierre explícito de la conexión con código de motivo.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Códigos de motivo:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Reglas:** - La terminación DEBE ser el último bloque que no sea de relleno en la trama - Como máximo un bloque de terminación por trama - El emisor debería cerrar la conexión después de enviar - El receptor debería cerrar la conexión después de recibir

**Manejo de errores:** - Errores de handshake (negociación inicial): Normalmente se cierra con TCP RST (sin bloque de terminación) - Errores de AEAD (cifrado autenticado con datos asociados) en la fase de datos: Tiempo de espera aleatorio + lectura aleatoria, luego enviar terminación - Consulta la sección "AEAD Error Handling" para los procedimientos de seguridad

### Tipo de bloque 254: Relleno

Relleno aleatorio para resistir el análisis de tráfico.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Reglas:** - El relleno DEBE ser el último bloque en la trama si está presente - Se permite relleno de longitud cero - Solo se permite un bloque de relleno por trama - Se permiten tramas solo de relleno - Debería cumplir con los parámetros negociados del bloque Options

**Relleno en los mensajes 1-2:** - Fuera de la trama AEAD (texto en claro) - Incluido en la cadena de hashes del siguiente mensaje (autenticado) - Se detecta manipulación cuando falla el AEAD del siguiente mensaje

**Relleno en el Mensaje 3+ y en la Fase de Datos:** - Dentro de la trama AEAD (cifrado autenticado con datos asociados; cifrada y autenticada) - Se utiliza para el conformado del tráfico y la ofuscación del tamaño

## Gestión de errores de AEAD (cifrado autenticado con datos asociados)

**Requisitos de seguridad críticos:**

### Fase de negociación (Mensajes 1-3)

**Tamaño de mensaje conocido:** - Los tamaños de los mensajes están predeterminados o se especifican de antemano - El fallo de autenticación de AEAD es inequívoco

**Respuesta de Bob al error del Mensaje 1:** 1. Establecer un tiempo de espera aleatorio (rango dependiente de la implementación, se sugiere 100-500ms) 2. Leer una cantidad aleatoria de bytes (rango dependiente de la implementación, se sugiere 1KB-64KB) 3. Cerrar la conexión con TCP RST (sin respuesta) 4. Poner en lista negra la IP de origen temporalmente 5. Registrar fallos repetidos para bloqueos a largo plazo

**Respuesta de Alice ante el fallo del Mensaje 2:** 1. Cerrar la conexión de inmediato con TCP RST (restablecimiento de TCP) 2. No responder a Bob

**Respuesta de Bob al fallo del Mensaje 3:** 1. Cerrar la conexión de inmediato con TCP RST (restablecimiento de TCP) 2. No responder a Alice

### Fase de datos

**Tamaño de mensaje ofuscado:** - El campo de longitud está ofuscado con SipHash - Una longitud no válida o un fallo de AEAD podría indicar:   - Sondeo por parte de un atacante   - Corrupción en la red   - IV de SipHash desincronizado   - Par malicioso

**Respuesta a error de AEAD (cifrado autenticado con datos asociados) o de longitud:** 1. Establecer un tiempo de espera aleatorio (se sugiere 100-500ms) 2. Leer un número aleatorio de bytes (se sugiere 1KB-64KB) 3. Enviar un bloque de terminación con código de motivo 4 (fallo de AEAD) o 9 (error de encuadre) 4. Cerrar la conexión

**Prevención del oráculo de descifrado:** - Nunca revelar el tipo de error al par antes de un tiempo de espera aleatorio - Nunca omitir la validación de longitud antes de la verificación de AEAD (cifrado autenticado con datos asociados) - Tratar una longitud no válida igual que un fallo de AEAD - Usar una ruta de gestión de errores idéntica para ambos errores

**Consideraciones de implementación:** - Algunas implementaciones pueden continuar tras errores de AEAD (cifrado autenticado con datos asociados) si son poco frecuentes - Finalizar tras errores repetidos (umbral sugerido: 3-5 errores por hora) - Equilibrio entre la recuperación ante errores y la seguridad

## RouterInfo publicado (información del router)

### Formato de la dirección del Router

El soporte para NTCP2 se anuncia a través de entradas de RouterAddress publicadas con opciones específicas.

**Estilo de transporte:** - `"NTCP2"` - NTCP2 solo en este puerto - `"NTCP"` - Tanto NTCP como NTCP2 en este puerto (detección automática)   - **Nota**: compatibilidad con NTCP (v1) eliminada en 0.9.50 (mayo de 2021)   - el estilo "NTCP" ahora está obsoleto; utiliza "NTCP2"

### Opciones obligatorias

**Todas las direcciones NTCP2 publicadas:**

1. **`host`** - Dirección IP (IPv4 o IPv6) o nombre de host
   - Formato: notación IP estándar o nombre de dominio
   - Puede omitirse en routers de solo salida o ocultos

2. **`port`** - Número de puerto TCP
   - Formato: Entero, 1-65535
   - Puede omitirse para routers solo de salida o ocultos

3. **`s`** - Clave pública estática (X25519)
   - Formato: Codificado en Base64, 44 caracteres
   - Codificación: Alfabeto Base64 de I2P
   - Origen: Clave pública X25519 de 32 bytes, little-endian (orden de bytes de menor a mayor)

4. **`i`** - Vector de inicialización para AES
   - Formato: codificado en Base64, 24 caracteres
   - Codificación: alfabeto Base64 de I2P
   - Origen: IV de 16 bytes, big-endian (byte más significativo primero)

5. **`v`** - Versión de protocolo
   - Formato: Entero o enteros separados por comas
   - Actual: `"2"`
   - Futuro: `"2,3"` (deben estar en orden numérico)

**Opciones opcionales:**

6. **`caps`** - Capacidades (desde 0.9.50)
   - Formato: Cadena de caracteres de capacidad
   - Valores:
     - `"4"` - capacidad de salida IPv4
     - `"6"` - capacidad de salida IPv6
     - `"46"` - Ambos IPv4 e IPv6 (orden recomendado)
   - No es necesario si `host` está publicado
   - Útil para routers ocultos o tras cortafuegos

7. **`cost`** - Prioridad de la dirección
   - Formato: Entero, 0-255
   - Valores más bajos = mayor prioridad
   - Sugerido: 5-10 para direcciones normales
   - Sugerido: 14 para direcciones no publicadas

### Ejemplos de entradas de RouterAddress

**Dirección IPv4 publicada:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Router oculto (solo de salida):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router de doble pila:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Reglas importantes:** - Varias direcciones NTCP2 con el **mismo puerto** DEBEN usar valores **idénticos** `s`, `i` y `v` - Puertos distintos pueden usar claves diferentes - Los routers de doble pila deberían publicar direcciones IPv4 e IPv6 separadas

### Dirección NTCP2 no publicada

**Para routers solo de salida:**

Si un router no acepta conexiones NTCP2 entrantes pero inicia conexiones salientes, DEBE igualmente publicar un RouterAddress (dirección del router) con:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Propósito:** - Permite que Bob valide la clave estática de Alice durante el handshake (negociación inicial) - Necesario para la verificación de RouterInfo en el mensaje 3, parte 2 - No se necesitan `i`, `host` ni `port` (solo saliente)

**Alternativa:** - Añade `s` y `v` a la dirección "NTCP" o SSU ya publicada

### Rotación de clave pública e IV (vector de inicialización)

**Política de seguridad crítica:**

**Reglas generales:** 1. **Nunca rotar mientras el router esté en ejecución** 2. **Almacenar de forma persistente la clave y el IV (vector de inicialización)** entre reinicios 3. **Registrar el tiempo de inactividad previo** para determinar la elegibilidad de rotación

**Tiempo mínimo de inactividad antes de la rotación:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Disparadores adicionales:** - Cambio de dirección IP local: Puede rotar independientemente del tiempo de inactividad - Router "rekey" (nuevo Router Hash): Generar nuevas claves

**Justificación:** - Evita exponer los tiempos de reinicio a través de cambios de clave - Permite que los RouterInfos en caché expiren de forma natural - Mantiene la estabilidad de la red - Reduce los intentos de conexión fallidos

**Implementación:** 1. Almacenar de forma persistente la clave, el IV y la marca de tiempo del último apagado 2. Al inicio, calcular el tiempo de inactividad = current_time - last_shutdown 3. Si el tiempo de inactividad > mínimo para el tipo de router, puede rotar 4. Si la IP cambió o hay rekeying (renovación de claves), puede rotar 5. De lo contrario, reutilizar la clave e IV anteriores

**Rotación del vector de inicialización (IV):** - Sujeta a las mismas reglas que la rotación de claves - Solo presente en direcciones publicadas (no en routers ocultos) - Se recomienda cambiar el IV cada vez que cambie la clave

## Detección de versión

**Contexto:** Cuando `transportStyle="NTCP"` (heredado), Bob admite tanto NTCP v1 como v2 en el mismo puerto y debe detectar automáticamente la versión del protocolo.

**Algoritmo de detección:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Comprobación rápida del bit más significativo (MSB):** - Antes del descifrado AES, verifique: `encrypted_X[31] & 0x80 == 0` - Las claves X25519 válidas tienen el bit más alto en 0 - Un fallo indica probablemente NTCP1 (o un ataque) - Implemente resistencia al sondeo (tiempo de espera aleatorio + lectura) en caso de fallo

**Requisitos de implementación:**

1. **Responsabilidad de Alice:**
   - Al conectarse a la dirección "NTCP", limitar el mensaje 1 a un máximo de 287 bytes
   - Almacenar en búfer y vaciar el mensaje 1 completo de una sola vez
   - Aumenta la probabilidad de entrega en un único paquete TCP

2. **Responsabilidad de Bob:**
   - Almacenar en búfer los datos recibidos antes de decidir la versión
   - Implementar una gestión adecuada de los tiempos de espera
   - Usar TCP_NODELAY para una detección rápida de la versión
   - Almacenar en búfer y vaciar el mensaje 2 completo de una sola vez una vez detectada la versión

**Consideraciones de seguridad:** - Ataques de segmentación: Bob debe ser resistente a la segmentación de TCP - Ataques de sondeo: Implementar retrasos aleatorios y lecturas de bytes ante fallos - Prevención de denegación de servicio (DoS): Limitar las conexiones pendientes simultáneas - Tiempos de espera de lectura: Tanto por lectura como totales (protección contra "slowloris")

## Directrices sobre el desfase del reloj

**Campos de marca de tiempo:** - Mensaje 1: `tsA` (marca de tiempo de Alice) - Mensaje 2: `tsB` (marca de tiempo de Bob) - Mensaje 3+: Bloques DateTime (fecha y hora) opcionales

**Desfase máximo (D):** - Típico: **±60 segundos** - Configurable según la implementación - El desfase > D generalmente es fatal

### Manejo de Bob (Mensaje 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Justificación:** Enviar el mensaje 2 incluso cuando hay desfase de reloj permite a Alice diagnosticar problemas de sincronización del reloj.

### Procesamiento de Alice (Mensaje 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Ajuste de RTT:** - Restar la mitad del RTT de la desviación calculada - Tiene en cuenta el retraso de propagación de la red - Estimación de la desviación más precisa

### Procesamiento de Bob (Mensaje 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Sincronización de tiempo

**Bloques DateTime (Fase de datos):** - Enviar periódicamente DateTime block (bloque de fecha y hora) (tipo 0) - El receptor puede usarlo para ajustar el reloj - Redondear la marca de tiempo al segundo más cercano (evitar sesgo)

**Fuentes de tiempo externas:** - NTP (Network Time Protocol) - Sincronización del reloj del sistema - Tiempo de consenso de la red de I2P

**Estrategias de ajuste del reloj:** - Si el reloj local es incorrecto: Ajusta la hora del sistema o usa un desfase - Si los relojes de los pares son sistemáticamente incorrectos: Señala el problema del par - Realiza seguimiento de las estadísticas de desfase para el monitoreo del estado de la red

## Propiedades de seguridad

### Secreto Perfecto hacia Adelante

**Logrado mediante:** - Intercambio de claves Diffie-Hellman efímero (X25519) - Tres operaciones DH: es, ee, se (Noise XK pattern, patrón Noise XK) - Las claves efímeras se destruyen tras completar el protocolo de negociación

**Progresión de confidencialidad:** - Mensaje 1: Nivel 2 (secreto perfecto hacia adelante en caso de compromiso del remitente) - Mensaje 2: Nivel 1 (destinatario efímero) - Mensaje 3+: Nivel 5 (secreto perfecto hacia adelante fuerte)

**Secreto Perfecto hacia Adelante:** - El compromiso de claves estáticas a largo plazo NO revela claves de sesión anteriores - Cada sesión usa claves efímeras únicas - Las claves privadas efímeras nunca se reutilizan - Limpieza de memoria después del acuerdo de claves

**Limitaciones:** - El Mensaje 1 es vulnerable si se compromete la clave estática de Bob (aunque se mantiene el secreto perfecto hacia adelante si Alice se ve comprometida) - Son posibles ataques de repetición para el mensaje 1 (mitigados por la marca de tiempo y la caché antirrepetición)

### Autenticación

**Autenticación mutua:** - Alice autenticada mediante clave estática en el mensaje 3 - Bob autenticado por la posesión de la clave privada estática (implícito a partir de una negociación exitosa)

**Resistencia a Key Compromise Impersonation (KCI, suplantación por compromiso de clave):** - Nivel de autenticación 2 (resistente a KCI) - Un atacante no puede hacerse pasar por Alice ni siquiera con la clave privada estática de Alice (sin la clave efímera de Alice) - Un atacante no puede hacerse pasar por Bob ni siquiera con la clave privada estática de Bob (sin la clave efímera de Bob)

**Verificación de clave estática:** - Alice sabe de antemano la clave estática de Bob (a partir de RouterInfo) - Bob verifica que la clave estática de Alice coincide con RouterInfo en el mensaje 3 - Evita ataques de intermediario

### Resistencia al análisis de tráfico

**Contramedidas de DPI (inspección profunda de paquetes):** 1. **Ofuscación con AES:** Claves efímeras cifradas, apariencia aleatoria 2. **Ofuscación de la longitud con SipHash:** Longitudes de trama no en claro 3. **Relleno aleatorio:** Tamaños de mensaje variables, sin patrones fijos 4. **Tramas cifradas:** Toda la carga útil cifrada con ChaCha20

**Prevención de ataques de repetición:** - Validación de marca de tiempo (±60 segundos) - Caché antirrepetición de claves efímeras (tiempo de vida 2*D) - Los incrementos del Nonce (número usado una vez) evitan la repetición de paquetes dentro de la sesión

**Resistencia a sondeos:** - Tiempos de espera aleatorios ante fallos de AEAD (cifrado autenticado con datos asociados) - Lecturas aleatorias de bytes antes de cerrar la conexión - Sin respuestas ante fallos de handshake (intercambio inicial) - Inclusión de direcciones IP en lista negra por fallos repetidos

**Pautas de relleno:** - Mensajes 1-2: Relleno en texto en claro (autenticado) - Mensaje 3+: Relleno cifrado dentro de tramas AEAD - Parámetros de relleno negociados (Options block, bloque de opciones) - Se permiten tramas solo de relleno

### Mitigación de denegación de servicio

**Límites de conexión:** - Máximo de conexiones activas (dependiente de la implementación) - Máximo de handshakes (negociación inicial) pendientes (p. ej., 100-1000) - Límites de conexión por IP (p. ej., 3-10 simultáneas)

**Protección de recursos:** - Operaciones DH con limitación de tasa (costosas) - Tiempos de espera de lectura por socket y totales - Protección contra "Slowloris" (ataque de conexiones lentas; límites de tiempo totales) - Inclusión de IP en lista negra por abuso

**Rechazo rápido:** - Discordancia de ID de red → cierre inmediato - Punto X25519 no válido → comprobación rápida del bit más significativo (MSB) antes del descifrado - Marca de tiempo fuera de rango → cierre sin procesamiento - Error de AEAD (cifrado autenticado con datos asociados) → sin respuesta, retraso aleatorio

**Resistencia al sondeo:** - Tiempo de espera aleatorio: 100-500ms (dependiente de la implementación) - Lectura aleatoria: 1KB-64KB (dependiente de la implementación) - Sin información de error para el atacante - Cerrar con TCP RST (sin FIN handshake)

### Seguridad criptográfica

**Algoritmos:** - **X25519**: seguridad de 128 bits, DH de curva elíptica (Curve25519) - **ChaCha20**: cifrado de flujo con clave de 256 bits - **Poly1305**: MAC con seguridad teórica de la información - **SHA-256**: resistencia a colisiones de 128 bits, resistencia a preimagen de 256 bits - **HMAC-SHA256**: PRF para la derivación de claves

**Tamaños de clave:** - Claves estáticas: 32 bytes (256 bits) - Claves efímeras: 32 bytes (256 bits) - Claves de cifrado: 32 bytes (256 bits) - MAC: 16 bytes (128 bits)

**Problemas conocidos:** - La reutilización del nonce (número usado una vez) en ChaCha20 es catastrófica (evitada mediante el incremento del contador) - X25519 tiene problemas de subgrupos pequeños (mitigado mediante la validación de la curva) - SHA-256 es teóricamente vulnerable a la extensión de longitud (no explotable en HMAC)

**No hay vulnerabilidades conocidas (a octubre de 2025):** - Noise Protocol Framework (marco de protocolos Noise) ampliamente analizado - ChaCha20-Poly1305 (cifrado autenticado) implementado en TLS 1.3 - X25519 (intercambio de claves de curva elíptica) estándar en protocolos modernos - No hay ataques prácticos contra la construcción criptográfica

## Referencias

### Especificaciones principales

- **[NTCP2 Specification](/docs/specs/ntcp2/)** - Especificación oficial de I2P
- **[Proposal 111](/proposals/111-ntcp-2/)** - Documento de diseño original con fundamentos
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Revisión 33 (2017-10-04)

### Estándares criptográficos

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Curvas elípticas para la seguridad (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 y Poly1305 para protocolos de la IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (deja obsoleto el RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: hash con clave para la autenticación de mensajes
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 para aplicaciones de funciones hash

### Especificaciones relacionadas de I2P

- **[Especificación de I2NP](/docs/specs/i2np/)** - formato de mensajes del protocolo de red de I2P
- **[Estructuras comunes](/docs/specs/common-structures/)** - formatos de RouterInfo y RouterAddress
- **[Transporte SSU](/docs/legacy/ssu/)** - transporte UDP (original, ahora SSU2)
- **[Propuesta 147](/proposals/147-transport-network-id-check/)** - verificación del ID de la red de transporte (0.9.42)

### Referencias de implementación

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Implementación de referencia (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Implementación en C++
- **[I2P Release Notes](/blog/)** - Historial de versiones y actualizaciones

### Contexto histórico

- **[Protocolo Station-To-Station (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Inspiración para Noise framework (conjunto de protocolos Noise)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (transporte conectable) (precedente de ofuscación de longitud con SipHash)

## Directrices de implementación

### Requisitos obligatorios

**Para cumplimiento:**

1. **Implementar el protocolo de enlace completo:**
   - Admitir los tres mensajes con cadenas KDF correctas (función de derivación de claves)
   - Validar todas las etiquetas AEAD (cifrado autenticado con datos asociados)
   - Verificar que los puntos X25519 sean válidos

2. **Implementar la fase de datos:**
   - Ofuscación de longitud mediante SipHash (en ambas direcciones)
   - Todos los tipos de bloque: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Gestión adecuada del nonce (valor único de un solo uso) con contadores separados

3. **Características de seguridad:**
   - Prevención de ataques de repetición (almacenar en caché claves efímeras durante 2*D)
   - Validación de marca de tiempo (±60 segundos por defecto)
   - Relleno aleatorio en los mensajes 1-2
   - Gestión de errores de AEAD (cifrado autenticado con datos asociados) con tiempos de espera aleatorios

4. **Publicación de RouterInfo (información del router):**
   - Publicar la clave estática ("s"), el IV (vector de inicialización) ("i") y la versión ("v")
   - Rotar las claves según la política
   - Admitir el campo de capacidades ("caps") para routers ocultos

5. **Compatibilidad de red:**
   - Admitir el campo de ID de red (actualmente 2 para la red principal)
   - Interoperar con las implementaciones existentes de Java e i2pd
   - Gestionar tanto IPv4 como IPv6

### Prácticas recomendadas

**Optimización del rendimiento:**

1. **Estrategia de bufferizado:**
   - Volcar mensajes completos de una vez (mensajes 1, 2, 3)
   - Usar TCP_NODELAY para mensajes de handshake (negociación inicial)
   - Almacenar en búfer múltiples bloques de datos en una sola trama
   - Limitar el tamaño de la trama a pocos KB (minimizar la latencia del receptor)

2. **Gestión de conexiones:**
   - Reutilizar conexiones cuando sea posible
   - Implementar un pool de conexiones
   - Supervisar el estado de las conexiones (bloques de DateTime)

3. **Gestión de memoria:**
   - Poner a cero los datos sensibles después de su uso (claves efímeras, resultados de DH)
   - Limitar los handshakes (intercambios de establecimiento) concurrentes (prevención de DoS)
   - Usar pools de memoria para asignaciones frecuentes

**Endurecimiento de seguridad:**

1. **Resistencia a sondeos:**
   - Tiempos de espera aleatorios: 100-500ms
   - Lecturas aleatorias de bytes: 1KB-64KB
   - Bloqueo de IP por fallos repetidos
   - Sin detalles de error para los pares

2. **Límites de recursos:**
   - Máximo de conexiones por IP: 3-10
   - Máximo de handshakes pendientes (negociaciones iniciales): 100-1000
   - Tiempos de espera de lectura: 30-60 segundos por operación
   - Tiempo de espera total de la conexión: 5 minutos para el handshake

3. **Gestión de claves:**
   - Almacenamiento persistente de la clave estática y del vector de inicialización (IV)
   - Generación aleatoria segura (generador de números aleatorios criptográfico)
   - Cumplir estrictamente las políticas de rotación
   - Nunca reutilizar claves efímeras

**Monitoreo y diagnóstico:**

1. **Métricas:**
   - Tasas de éxito/fallo del handshake (negociación inicial)
   - Tasas de errores de AEAD (cifrado autenticado con datos asociados)
   - Distribución del desfase del reloj
   - Estadísticas de la duración de la conexión

2. **Registro:**
   - Registrar fallos de handshake (negociación inicial) con códigos de motivo
   - Registrar eventos de desfase del reloj
   - Registrar direcciones IP bloqueadas
   - Nunca registrar material de claves sensible

3. **Pruebas:**
   - Pruebas unitarias para cadenas de KDF
   - Pruebas de integración con otras implementaciones
   - Fuzzing (pruebas con entradas aleatorias) para la gestión de paquetes
   - Pruebas de carga para resistencia frente a DoS

### Escollos comunes

**Errores críticos que se deben evitar:**

1. **Reutilización de nonce (número aleatorio de un solo uso):**
   - Nunca reinicies el contador de nonce a mitad de sesión
   - Usa contadores separados para cada sentido
   - Finaliza antes de alcanzar 2^64 - 1

2. **Rotación de claves:**
   - Nunca rote claves mientras el router esté en ejecución
   - Nunca reutilice claves efímeras entre sesiones
   - Cumpla las reglas de tiempo de inactividad mínimo

3. **Gestión de marcas de tiempo:**
   - Nunca aceptar marcas de tiempo expiradas
   - Ajustar siempre por RTT (tiempo de ida y vuelta) al calcular el desfase
   - Redondear las marcas de tiempo de DateTime a segundos

4. **Errores AEAD (cifrado autenticado con datos asociados):**
   - Nunca revelar el tipo de error al atacante
   - Usar siempre un tiempo de espera aleatorio antes de cerrar
   - Tratar una longitud no válida del mismo modo que un fallo de AEAD

5. **Relleno:**
   - Nunca enviar relleno fuera de los límites negociados
   - Siempre colocar el bloque de relleno al final
   - Nunca múltiples bloques de relleno por trama

6. **RouterInfo:**
   - Verificar siempre que la clave estática coincida con el RouterInfo
   - Nunca difundir RouterInfos sin direcciones publicadas
   - Validar siempre las firmas

### Metodología de pruebas

**Pruebas unitarias:**

1. **Primitivas criptográficas:**
   - Vectores de prueba para X25519, ChaCha20, Poly1305, SHA-256
   - Vectores de prueba de HMAC-SHA256
   - Vectores de prueba de SipHash-2-4

2. **Cadenas KDF:**
   - Pruebas de respuesta conocida para los tres mensajes
   - Verificar la propagación de la clave de encadenamiento
   - Probar la generación del IV de SipHash

3. **Análisis de mensajes:**
   - Decodificación de mensajes válidos
   - Rechazo de mensajes no válidos
   - Condiciones límite (vacío, tamaño máximo)

**Pruebas de integración:**

1. **Handshake (negociación inicial):**
   - Intercambio exitoso de tres mensajes
   - Rechazo por desfase de reloj
   - Detección de ataques de repetición
   - Rechazo de claves no válidas

2. **Fase de datos:**
   - Transferencia de mensajes I2NP
   - Intercambio de RouterInfo (información del router)
   - Gestión del relleno
   - Mensajes de terminación

3. **Interoperabilidad:**
   - Probar contra Java I2P
   - Probar contra i2pd
   - Probar IPv4 e IPv6
   - Probar routers publicados y ocultos

**Pruebas de seguridad:**

1. **Pruebas negativas:**
   - Etiquetas AEAD no válidas
   - Mensajes repetidos
   - Ataques por desfase de reloj
   - Tramas malformadas

2. **Pruebas de denegación de servicio (DoS):**
   - Inundación de conexiones
   - Ataques Slowloris
   - Agotamiento de CPU (DH excesivo, intercambio de claves Diffie-Hellman)
   - Agotamiento de memoria

3. **Fuzzing (pruebas aleatorias):**
   - Mensajes de negociación aleatorios
   - Tramas aleatorias de la fase de datos
   - Tipos y tamaños de bloque aleatorios
   - Valores criptográficos no válidos

### Migración desde NTCP

**Para el soporte heredado de NTCP (ahora eliminado):**

NTCP (versión 1) se eliminó en I2P 0.9.50 (mayo de 2021). Todas las implementaciones actuales deben admitir NTCP2. Notas históricas:

1. **Periodo de transición (2018-2021):**
   - 0.9.36: NTCP2 introducido (deshabilitado de forma predeterminada)
   - 0.9.37: NTCP2 habilitado de forma predeterminada
   - 0.9.40: NTCP (protocolo de transporte antiguo de I2P) declarado obsoleto
   - 0.9.50: NTCP eliminado

2. **Detección de versión:**
   - El transportStyle (estilo de transporte) "NTCP" indicaba compatibilidad con ambas versiones
   - El transportStyle "NTCP2" indicaba solo NTCP2
   - Detección automática mediante el tamaño del mensaje (287 frente a 288 bytes)

3. **Estado actual:**
   - Todos los routers deben admitir NTCP2
   - El transportStyle "NTCP" está obsoleto
   - Utilice el transportStyle "NTCP2" exclusivamente

## Apéndice A: Patrón XK de Noise

**Patrón estándar XK de Noise:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Interpretación:**

- `<-` : Mensaje del respondedor (Bob) al iniciador (Alice)
- `->` : Mensaje del iniciador (Alice) al respondedor (Bob)
- `s` : Clave estática (clave de identidad a largo plazo)
- `rs` : Clave estática remota (clave estática del par, conocida de antemano)
- `e` : Clave efímera (específica de la sesión, generada bajo demanda)
- `es` : DH efímera-estática (efímera de Alice × estática de Bob)
- `ee` : DH efímera-efímera (efímera de Alice × efímera de Bob)
- `se` : DH estática-efímera (estática de Alice × efímera de Bob)

**Secuencia de acuerdo de claves:**

1. **Pre-mensaje:** Alice conoce la clave pública estática de Bob (de RouterInfo)
2. **Mensaje 1:** Alice envía una clave efímera, realiza es DH (efímera-estática)
3. **Mensaje 2:** Bob envía una clave efímera, realiza ee DH
4. **Mensaje 3:** Alice revela la clave estática, realiza se DH

**Propiedades de seguridad:**

- Alice autenticada: Sí (por el mensaje 3)
- Bob autenticado: Sí (por poseer la clave privada estática)
- Secreto perfecto hacia adelante: Sí (claves efímeras destruidas)
- Resistencia a KCI (Key Compromise Impersonation, suplantación por compromiso de clave): Sí (nivel de autenticación 2)

## Apéndice B: Codificación Base64

**Alfabeto Base64 de I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Diferencias con el Base64 estándar:** - Caracteres 62-63: `-~` en lugar de `+/` - Relleno: Igual (`=`) u omitido según el contexto

**Uso en NTCP2:** - Clave estática ("s"): 32 bytes → 44 caracteres (sin relleno) - IV ("i"): 16 bytes → 24 caracteres (sin relleno)

**Ejemplo de codificación:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Apéndice C: Análisis de captura de paquetes

**Identificación del tráfico NTCP2:**

1. **Negociación TCP:**
   - TCP estándar: SYN, SYN-ACK, ACK
   - Puerto de destino generalmente 8887 o similar

2. **Mensaje 1 (SessionRequest - solicitud de sesión):**
   - Primeros datos de la aplicación provenientes de Alice
   - 80-65535 bytes (normalmente unos pocos cientos)
   - Parece aleatorio (clave efímera cifrada con AES)
   - 287 bytes máximo si se conecta a una dirección "NTCP"

3. **Mensaje 2 (SessionCreated, creación de sesión):**
   - Respuesta de Bob
   - 80-65535 bytes (normalmente unos pocos cientos)
   - También parece aleatorio

4. **Mensaje 3 (SessionConfirmed):**
   - De Alice
   - 48 bytes + variable (tamaño de RouterInfo (información del router) + relleno)
   - Normalmente 1-4 KB

5. **Fase de datos:**
   - Tramas de longitud variable
   - Campo de longitud ofuscado (parece aleatorio)
   - Carga útil cifrada
   - El relleno hace que el tamaño sea impredecible

**Evasión de DPI (inspección profunda de paquetes):** - Sin cabeceras en texto plano - Sin patrones fijos - Campos de longitud ofuscados - El relleno aleatorio invalida las heurísticas basadas en el tamaño

**Comparación con NTCP:** - Mensaje 1 de NTCP siempre de 288 bytes (identificable) - El tamaño del mensaje 1 de NTCP2 varía (no identificable) - NTCP tenía patrones reconocibles - NTCP2 diseñado para resistir la inspección profunda de paquetes (DPI)

## Apéndice D: Historial de versiones

**Hitos principales:**

- **0.9.36** (23 de agosto de 2018): NTCP2 introducido, deshabilitado de forma predeterminada
- **0.9.37** (4 de octubre de 2018): NTCP2 habilitado de forma predeterminada
- **0.9.40** (20 de mayo de 2019): NTCP declarado obsoleto
- **0.9.42** (27 de agosto de 2019): Se añadió el campo de ID de red (Propuesta 147)
- **0.9.50** (17 de mayo de 2021): NTCP eliminado, se añadió soporte para capacidades
- **2.10.0** (9 de septiembre de 2025): Última versión estable

**Estabilidad del protocolo:** - Sin cambios incompatibles desde la versión 0.9.50 - Mejoras continuas en la resistencia frente a sondeos - Enfoque en el rendimiento y la fiabilidad - Criptografía poscuántica en desarrollo (no habilitada de forma predeterminada)

**Estado actual del transporte:** - NTCP2: Transporte TCP obligatorio - SSU2: Transporte UDP obligatorio - NTCP (v1): Eliminado - SSU (v1): Eliminado
