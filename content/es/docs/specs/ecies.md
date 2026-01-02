---
title: "Especificación de cifrado ECIES-X25519-AEAD-Ratchet (mecanismo de trinquete criptográfico)"
description: "Esquema de cifrado integrado de curva elíptica para I2P (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Descripción general

### Propósito

ECIES-X25519-AEAD-Ratchet es el protocolo moderno de cifrado de extremo a extremo de I2P, que reemplaza el sistema heredado ElGamal/AES+SessionTags. Proporciona secreto perfecto hacia adelante, cifrado autenticado y mejoras significativas en rendimiento y seguridad.

### Mejoras principales con respecto a ElGamal/AES+SessionTags

- **Claves más pequeñas**: Claves de 32 bytes frente a claves públicas ElGamal de 256 bytes (reducción del 87,5 %)
- **Secreto hacia adelante**: Logrado mediante DH ratcheting (mecanismo de avance escalonado) (no disponible en el protocolo heredado)
- **Criptografía moderna**: X25519 DH, ChaCha20-Poly1305 AEAD (cifrado autenticado con datos asociados), SHA-256
- **Cifrado autenticado**: Autenticación integrada mediante construcción AEAD
- **Protocolo bidireccional**: Sesiones de entrada/salida emparejadas frente al protocolo heredado unidireccional
- **Etiquetas eficientes**: Etiquetas de sesión de 8 bytes frente a etiquetas de 32 bytes (reducción del 75 %)
- **Ofuscación del tráfico**: La codificación Elligator2 (técnica de ofuscación de curvas elípticas) hace que los intercambios iniciales sean indistinguibles de datos aleatorios

### Estado de despliegue

- **Lanzamiento inicial**: Versión 0.9.46 (25 de mayo de 2020)
- **Despliegue de la red**: Completo desde 2020
- **Estado actual**: Maduro, ampliamente desplegado (más de 5 años en producción)
- **Compatibilidad del router**: Se requiere la versión 0.9.46 o superior
- **Requisitos de Floodfill**: Adopción cercana al 100% para consultas cifradas

### Estado de la implementación

**Completamente implementado:** - mensajes New Session (NS) con vinculación - mensajes New Session Reply (NSR) - mensajes Existing Session (ES) - mecanismo de ratchet DH (mecanismo de avance escalonado) - ratchets de etiquetas de sesión y de claves simétricas - bloques DateTime, NextKey, ACK, ACK Request, Garlic Clove y Padding

**No implementado (a partir de la versión 0.9.50):** - bloque MessageNumbers (tipo 6) - bloque de opciones (tipo 5) - bloque de terminación (tipo 4) - respuestas automáticas a nivel de protocolo - modo de clave estática cero - sesiones multicast

**Nota**: El estado de implementación para las versiones desde la 1.5.0 hasta la 2.10.0 (2021-2025) requiere verificación, ya que es posible que se hayan añadido nuevas características.

---

## Fundamentos del protocolo

### Marco del protocolo Noise

ECIES-X25519-AEAD-Ratchet se basa en el [Noise Protocol Framework](https://noiseprotocol.org/) (marco del protocolo Noise) (Revisión 34, 2018-07-11), específicamente en el patrón de negociación **IK** (Interactivo, clave estática remota conocida) con extensiones específicas de I2P.

### Identificador del protocolo Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Componentes del identificador:** - `Noise` - Marco base - `IK` - Patrón de saludo interactivo con clave estática remota conocida - `elg2` - Codificación Elligator2 para claves efímeras (extensión de I2P) - `+hs2` - MixHash invocado antes del segundo mensaje para mezclar la etiqueta (extensión de I2P) - `25519` - Función Diffie-Hellman X25519 - `ChaChaPoly` - Cifrado AEAD ChaCha20-Poly1305 - `SHA256` - Función hash SHA-256

### Patrón de negociación de Noise

**Notación del patrón IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Significados de los tokens:** - `e` - Transmisión de clave efímera - `s` - Transmisión de clave estática - `es` - DH entre la clave efímera de Alice y la clave estática de Bob - `ss` - DH entre la clave estática de Alice y la clave estática de Bob - `ee` - DH entre la clave efímera de Alice y la clave efímera de Bob - `se` - DH entre la clave estática de Bob y la clave efímera de Alice

### Propiedades de seguridad de Noise

Usando la terminología de Noise, el patrón IK proporciona:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Niveles de autenticación:** - **Nivel 1**: La carga útil está autenticada como perteneciente al propietario de la clave estática del remitente, pero es vulnerable a Key Compromise Impersonation (suplantación por compromiso de clave, KCI) - **Nivel 2**: Resistente a ataques KCI después de NSR

**Niveles de confidencialidad:** - **Nivel 2**: Secreto hacia adelante si la clave estática del remitente se ve comprometida posteriormente - **Nivel 4**: Secreto hacia adelante si la clave efímera del remitente se ve comprometida posteriormente - **Nivel 5**: Secreto hacia adelante completo después de que ambas claves efímeras se eliminen

### Diferencias entre IK y XK

El patrón IK difiere del patrón XK utilizado en NTCP2 y SSU2:

1. **Cuatro operaciones DH**: IK usa 4 operaciones DH (es, ss, ee, se) frente a 3 para XK
2. **Autenticación inmediata**: Alice queda autenticada en el primer mensaje (Nivel de Autenticación 1)
3. **Secreto hacia adelante más rápido**: Se logra secreto hacia adelante completo (Nivel 5) después del segundo mensaje (1-RTT, una ida y vuelta)
4. **Compensación**: La carga útil del primer mensaje no tiene secreto hacia adelante (frente a XK, donde todas las cargas útiles tienen secreto hacia adelante)

**Resumen**: IK permite la entrega en 1-RTT de la respuesta de Bob con pleno secreto perfecto hacia adelante, a costa de que la solicitud inicial no tenga secreto perfecto hacia adelante.

### Conceptos del Signal Double Ratchet (algoritmo de doble trinquete)

ECIES incorpora conceptos del [Signal Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/) (algoritmo de doble trinquete de Signal):

- **DH Ratchet** (mecanismo de avance criptográfico): Proporciona secreto hacia adelante al intercambiar periódicamente nuevas claves DH
- **Symmetric Key Ratchet**: Deriva nuevas claves de sesión para cada mensaje
- **Session Tag Ratchet**: Genera etiquetas de sesión de un solo uso de forma determinista

**Diferencias clave con Signal:** - **Ratcheting menos frecuente** (mecanismo de actualización progresiva de claves): I2P solo hace ratcheting cuando es necesario (cerca del agotamiento de etiquetas o por política) - **Etiquetas de sesión en lugar de cifrado de encabezados**: Usa etiquetas deterministas en lugar de encabezados cifrados - **ACKs explícitos**: Usa bloques de ACK en banda en lugar de depender únicamente del tráfico de retorno - **Ratchets de etiquetas y de claves separados**: Más eficiente para el receptor (puede posponer el cálculo de la clave)

### Extensiones de I2P para Noise (marco de protocolos criptográficos)

1. **Codificación Elligator2** (técnica para hacer que las claves en curvas elípticas parezcan aleatorias): Claves efímeras codificadas para ser indistinguibles de lo aleatorio
2. **Etiqueta antepuesta a NSR**: Etiqueta de sesión agregada antes del mensaje NSR para permitir la correlación
3. **Formato de carga útil definido**: Estructura de carga útil basada en bloques para todos los tipos de mensajes
4. **Encapsulación I2NP**: Todos los mensajes envueltos en cabeceras I2NP Garlic Message
5. **Fase de datos separada**: Los mensajes de transporte (ES) difieren de la fase de datos estándar de Noise (marco de protocolos criptográficos)

---

## Primitivas criptográficas

### X25519 Diffie-Hellman

**Especificación**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Propiedades principales:** - **Tamaño de la clave privada**: 32 bytes - **Tamaño de la clave pública**: 32 bytes - **Tamaño del secreto compartido**: 32 bytes - **Orden de bytes**: Little-endian (menos significativo primero) - **Curva**: Curve25519

**Operaciones:**

### X25519 GENERATE_PRIVATE()

Genera una clave privada aleatoria de 32 bytes:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Deriva la clave pública correspondiente:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Devuelve una clave pública de 32 bytes en formato little-endian (byte menos significativo primero).

### X25519 DH(privkey, pubkey)

Realiza el acuerdo de claves Diffie-Hellman:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Devuelve un secreto compartido de 32 bytes.

**Nota de seguridad**: Los implementadores deben validar que el secreto compartido no consista únicamente en ceros (clave débil). Rechace y aborte el handshake (negociación) si esto ocurre.

### ChaCha20-Poly1305 AEAD (cifrado autenticado con datos asociados)

**Especificación**: [RFC 7539](https://tools.ietf.org/html/rfc7539) sección 2.8

**Parámetros:** - **Tamaño de clave**: 32 bytes (256 bits) - **Tamaño de nonce (número usado una vez)**: 12 bytes (96 bits) - **Tamaño de MAC**: 16 bytes (128 bits) - **Tamaño de bloque**: 64 bytes (interno)

**Formato del nonce (número aleatorio de un solo uso):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**Construcción de AEAD:**

AEAD (cifrado autenticado con datos asociados) combina el cifrado en flujo ChaCha20 con el MAC Poly1305:

1. Generar el flujo de claves de ChaCha20 a partir de la clave y el nonce (número único de uso único)
2. Cifrar el texto plano mediante XOR con el flujo de claves
3. Calcular el MAC Poly1305 sobre (datos asociados || texto cifrado)
4. Adjuntar el MAC de 16 bytes al texto cifrado

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Cifra el texto plano con autenticación:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Propiedades:** - El texto cifrado tiene la misma longitud que el texto en claro (cifrado de flujo) - La salida es plaintext_length + 16 bytes (incluye el MAC) - Toda la salida es indistinguible de datos aleatorios si la clave es secreta - El MAC autentica tanto los datos asociados como el texto cifrado

### ChaCha20-Poly1305 DESCIFRAR(k, n, ciphertext, ad)

Descifra y verifica la autenticación:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Requisitos críticos de seguridad:** - Los nonces (valores únicos de un solo uso) DEBEN ser únicos para cada mensaje con la misma clave - Los nonces NO DEBEN reutilizarse (fallo catastrófico si se reutilizan) - La verificación del MAC DEBE usar comparación en tiempo constante para evitar ataques de temporización - Una verificación de MAC fallida DEBE resultar en el rechazo completo del mensaje (sin descifrado parcial)

### Función hash SHA-256

**Especificación**: NIST FIPS 180-4

**Propiedades:** - **Tamaño de salida**: 32 bytes (256 bits) - **Tamaño de bloque**: 64 bytes (512 bits) - **Nivel de seguridad**: 128 bits (resistencia a colisiones)

**Operaciones:**

### SHA-256 H(p, d)

Hash SHA-256 con cadena de personalización:

```
H(p, d) := SHA256(p || d)
```
Donde `||` denota concatenación, `p` es la cadena de personalización, `d` son los datos.

### SHA-256 MixHash(d) (función de mezcla de hash)

Actualiza el hash incremental con nuevos datos:

```
h = SHA256(h || d)
```
Se utiliza durante todo el handshake de Noise para mantener el hash de la transcripción.

### Derivación de claves con HKDF

**Especificación**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Descripción**: Función de derivación de claves basada en HMAC usando SHA-256

**Parámetros:** - **Función hash**: HMAC-SHA256 - **Longitud de la sal**: Hasta 32 bytes (tamaño de salida de SHA-256) - **Longitud de salida**: Variable (hasta 255 * 32 bytes)

**Función HKDF:**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Patrones de uso comunes:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**Cadenas de información utilizadas en ECIES:** - `"KDFDHRatchetStep"` - derivación de la clave del ratchet DH (mecanismo de avance criptográfico) - `"TagAndKeyGenKeys"` - inicializar las claves de etiquetas y de la cadena de claves - `"STInitialization"` - inicialización del ratchet de etiqueta de sesión - `"SessionTagKeyGen"` - generación de etiquetas de sesión - `"SymmetricRatchet"` - generación de claves simétricas - `"XDHRatchetTagSet"` - clave del conjunto de etiquetas del ratchet DH - `"SessionReplyTags"` - generación del conjunto de etiquetas NSR - `"AttachPayloadKDF"` - derivación de la clave de la carga útil NSR

### Codificación Elligator2 (método criptográfico para representar claves públicas como datos indistinguibles de datos aleatorios)

**Propósito**: Codificar claves públicas X25519 de modo que sean indistinguibles de cadenas aleatorias uniformes de 32 bytes.

**Especificación**: [Artículo sobre Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Problema**: Las claves públicas X25519 estándar tienen una estructura reconocible. Un observador puede identificar los mensajes de handshake (negociación) detectando estas claves, incluso si el contenido está cifrado.

**Solución**: Elligator2 proporciona una aplicación biyectiva entre ~50% de las claves públicas X25519 válidas y cadenas de 254 bits de aspecto aleatorio.

**Generación de claves con Elligator2:**

### Elligator2 GENERATE_PRIVATE_ELG2()

Genera una clave privada que se corresponde con una clave pública codificable mediante Elligator2 (técnica que permite codificar claves públicas de forma indistinguible de datos aleatorios):

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Importante**: Aproximadamente el 50% de las claves privadas generadas aleatoriamente producirán claves públicas no codificables. Deben descartarse y debe intentarse la regeneración.

**Optimización del rendimiento**: Genera claves por adelantado en un hilo en segundo plano para mantener una reserva de pares de claves adecuados, evitando demoras durante el handshake (negociación inicial).

### Elligator2 ENCODE_ELG2(pubkey)

Codifica una clave pública en 32 bytes con apariencia aleatoria:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Detalles de codificación:** - Elligator2 (técnica de mapeo criptográfico) produce 254 bits (no los 256 completos) - Los 2 bits más significativos del byte 31 son relleno aleatorio - El resultado se distribuye uniformemente en todo el espacio de 32 bytes - Codifica con éxito aproximadamente el 50% de las claves públicas X25519 válidas

### Elligator2 DECODE_ELG2(encodedKey)

Se decodifica de vuelta a la clave pública original:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Propiedades de seguridad:** - Las claves codificadas son indistinguibles computacionalmente de bytes aleatorios - Ninguna prueba estadística puede detectar de forma fiable claves codificadas con Elligator2 - La decodificación es determinista (la misma clave codificada siempre produce la misma clave pública) - La codificación es biyectiva para el ~50% de las claves del subconjunto codificable

**Notas de implementación:** - Almacenar las claves codificadas en la fase de generación para evitar volver a codificarlas durante la negociación inicial - Las claves no aptas de la generación con Elligator2 (mapeo criptográfico para ofuscar claves) pueden usarse para NTCP2 (que no requiere Elligator2) - La generación de claves en segundo plano es esencial para el rendimiento - El tiempo medio de generación se duplica debido a una tasa de rechazo del 50%

---

## Formatos de mensajes

### Descripción general

ECIES define tres tipos de mensaje:

1. **New Session (NS)** (nueva sesión): Mensaje de negociación inicial de Alice a Bob
2. **New Session Reply (NSR)** (respuesta a nueva sesión): Respuesta de negociación de Bob a Alice
3. **Existing Session (ES)** (sesión existente): Todos los mensajes posteriores en ambas direcciones

Todos los mensajes están encapsulados en el formato I2NP Garlic Message con capas adicionales de cifrado.

### Contenedor de mensajes Garlic de I2NP

Todos los mensajes ECIES se encapsulan en encabezados estándar de I2NP Garlic Message (mensaje Garlic):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Campos:** - `type`: 0x26 (Garlic Message) - `msg_id`: ID de mensaje I2NP de 4 bytes - `expiration`: marca de tiempo Unix de 8 bytes (milisegundos) - `size`: tamaño de la carga útil de 2 bytes - `chks`: suma de verificación de 1 byte - `length`: longitud de los datos cifrados de 4 bytes - `encrypted data`: carga útil cifrada con ECIES

**Propósito**: Proporciona identificación y enrutamiento de mensajes en la capa I2NP. El campo `length` permite a los receptores conocer el tamaño total de la carga útil cifrada.

### Mensaje de Nueva Sesión (NS)

El mensaje de nueva sesión inicia una nueva sesión desde Alice hacia Bob. Se presenta en tres variantes:

1. **Con vinculación** (1b): Incluye la clave estática de Alice para comunicación bidireccional
2. **Sin vinculación** (1c): Omite la clave estática para comunicación unidireccional
3. **De un solo uso** (1d): Modo de un solo mensaje sin establecimiento de sesión

### Mensaje NS con vinculación (Tipo 1b)

**Caso de uso**: Transmisión en continuo, datagramas a los que se puede responder, cualquier protocolo que requiera respuestas

**Longitud total**: 96 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalles del campo:**

**Clave pública efímera** (32 bytes, sin cifrar): - Clave pública X25519 de un solo uso de Alice - Codificada con Elligator2 (indistinguible de datos aleatorios) - Se genera nueva para cada mensaje NS (nunca se reutiliza) - Formato little-endian

**Sección de clave estática** (32 bytes cifrados, 48 bytes con MAC): - Contiene la clave pública estática X25519 de Alice (32 bytes) - Cifrado con ChaCha20 - Autenticado con MAC Poly1305 (16 bytes) - Usado por Bob para vincular la sesión al destino de Alice

**Payload Section** (cifrado de longitud variable, +16 bytes de MAC): - Contiene garlic cloves (subbloques de garlic encryption; "dientes de ajo" en la terminología de I2P) y otros bloques - Debe incluir el bloque DateTime como primer bloque - Suele incluir bloques Garlic Clove con datos de la aplicación - Puede incluir el bloque NextKey para ratchet inmediato (mecanismo de avance criptográfico) - Cifrado con ChaCha20 - Autenticado con MAC Poly1305 (16 bytes)

**Propiedades de seguridad:** - La clave efímera proporciona el componente de secreto perfecto hacia adelante - La clave estática autentica a Alice (vinculándola al destino) - Ambas secciones tienen MAC independientes para separación de dominios - El handshake completo realiza 2 operaciones DH (es, ss)

### NS Message (mensaje NS) sin vinculación (Tipo 1c)

**Caso de uso**: Datagramas sin procesar en los que no se espera ni se desea respuesta

**Longitud total**: 96 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Diferencia clave**: La Flags Section (sección de banderas) contiene 32 bytes de ceros en lugar de una clave estática.

**Detección**: Bob determina el tipo de mensaje descifrando la sección de 32 bytes y verificando si todos los bytes son cero: - Todos en cero → sesión no vinculada (tipo 1c) - Algún byte distinto de cero → sesión vinculada con clave estática (tipo 1b)

**Propiedades:** - No tener una clave estática significa que no hay vinculación con el destino de Alice - Bob no puede enviar respuestas (no se conoce el destino) - Realiza solo 1 operación DH (Diffie-Hellman) (es) - Sigue el patrón "N" de Noise en lugar de "IK" - Más eficiente cuando nunca se necesitan respuestas

**Sección de indicadores** (reservada para uso futuro): Actualmente, todo son ceros. Podría utilizarse para la negociación de características en versiones futuras.

### NS Mensaje de un solo uso (Tipo 1d)

**Caso de uso**: Mensaje anónimo único, sin sesión ni respuesta esperada

**Longitud total**: 96 + payload_length bytes

**Formato**: Idéntico a NS sin vinculación (tipo 1c)

**Distinción**:  - Tipo 1c puede enviar múltiples mensajes en la misma sesión (los mensajes ES siguen) - Tipo 1d envía exactamente un mensaje sin establecimiento de sesión - En la práctica, las implementaciones pueden tratar ambos de forma idéntica inicialmente

**Propiedades:** - Anonimato máximo (sin clave estática, sin sesión) - Ninguna de las partes conserva estado de sesión - Sigue el patrón "N" de Noise (marco de protocolos criptográficos) - Una única operación DH (es)

### Mensaje de respuesta de nueva sesión (NSR)

Bob envía uno o más mensajes NSR en respuesta al mensaje NS de Alice. NSR completa el handshake Noise IK y establece una sesión bidireccional.

**Longitud total**: 72 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalles del campo:**

**Etiqueta de sesión** (8 bytes, en claro): - Generada a partir del conjunto de etiquetas de NSR (véanse las secciones de KDF) - Correlaciona esta respuesta con el mensaje NS de Alice - Permite a Alice identificar a qué NS responde este NSR - Uso único (nunca se reutiliza)

**Clave pública efímera** (32 bytes, en claro): - La clave pública X25519 de un solo uso de Bob - Codificada con Elligator2 - Generada de nuevo para cada mensaje NSR - Debe ser diferente para cada NSR enviado

**MAC de la sección de clave** (16 bytes): - Autentica datos vacíos (ZEROLEN) - Parte del protocolo Noise IK (se pattern; patrón estático-efímero) - Utiliza el hash de la transcripción como datos asociados - Crítico para vincular NSR a NS

**Sección de carga útil** (longitud variable): - Contiene garlic cloves (submensajes en el esquema garlic encryption) y bloques - Suele incluir respuestas de la capa de aplicación - Puede estar vacía (NSR solo con ACK) - Tamaño máximo: 65519 bytes (65535 - MAC de 16 bytes)

**Múltiples mensajes NSR:**

Bob puede enviar varios mensajes NSR en respuesta a un NS: - Cada NSR tiene una clave efímera única - Cada NSR tiene una etiqueta de sesión única - Alice usa el primer NSR recibido para completar el intercambio inicial - Los otros NSR son redundancia (en caso de pérdida de paquetes)

**Temporización crítica:** - Alice debe recibir un NSR antes de enviar mensajes ES - Bob debe recibir un mensaje ES antes de enviar mensajes ES - NSR establece claves de sesión bidireccionales mediante la operación split()

**Propiedades de seguridad:** - Completa el apretón de manos Noise IK - Realiza 2 operaciones DH adicionales (ee, se) - Total de 4 operaciones DH entre NS+NSR - Logra autenticación mutua (Nivel 2) - Proporciona secreto hacia adelante débil (Nivel 4) para la carga útil de NSR

### Mensaje de Sesión Existente (ES)

Todos los mensajes posteriores a la negociación NS/NSR usan el formato Existing Session (formato de sesión existente). Los mensajes ES se utilizan de forma bidireccional tanto por Alice como por Bob.

**Longitud total**: 8 + payload_length + 16 bytes (mínimo 24 bytes)

**Formato**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalles del campo:**

**Etiqueta de sesión** (8 bytes, en claro): - Generada a partir del conjunto de etiquetas de salida actual - Identifica la sesión y el número de mensaje - El receptor busca la etiqueta para encontrar la clave de sesión y el nonce (número único de uso) - Uso único (cada etiqueta se usa exactamente una vez) - Formato: primeros 8 bytes de la salida de HKDF

**Sección de carga útil** (longitud variable): - Contiene garlic cloves (unidades individuales de Garlic Encryption) y bloques - Sin bloques obligatorios (puede estar vacía) - Bloques comunes: Garlic Clove, NextKey, ACK, ACK Request, Padding - Tamaño máximo: 65519 bytes (65535 - MAC de 16 bytes)

**MAC** (16 bytes): - Etiqueta de autenticación Poly1305 - Se calcula sobre toda la carga útil - Datos asociados: la etiqueta de sesión de 8 bytes - Debe verificarse correctamente o el mensaje será rechazado

**Proceso de búsqueda de etiquetas:**

1. El receptor extrae una etiqueta de 8 bytes
2. Busca la etiqueta en todos los conjuntos de etiquetas entrantes actuales
3. Recupera la clave de sesión asociada y el número de mensaje N
4. Construye el nonce (número único de uso): `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Descifra la carga útil usando AEAD con la etiqueta como datos asociados
6. Elimina la etiqueta del conjunto de etiquetas (de un solo uso)
7. Procesa los bloques descifrados

**Etiqueta de sesión no encontrada:**

Si la etiqueta no se encuentra en ningún conjunto de etiquetas: - Puede ser un mensaje NS (tipo de mensaje de I2P) → intentar el descifrado NS - Puede ser un mensaje NSR (tipo de mensaje de I2P) → intentar el descifrado NSR - Puede ser un ES (esquema ElGamal+SessionTags en I2P) fuera de orden → esperar brevemente la actualización del conjunto de etiquetas - Puede ser un ataque de repetición → rechazar - Puede tratarse de datos corruptos → rechazar

**Carga útil vacía:**

Los mensajes ES pueden tener cargas útiles vacías (0 bytes): - Sirven como un ACK (acuse de recibo) explícito cuando se recibió una solicitud de ACK - Proporcionan una respuesta a nivel de protocolo sin datos de aplicación - Aún consumen una etiqueta de sesión - Son útiles cuando la capa superior no tiene datos inmediatos para enviar

**Propiedades de seguridad:** - Secreto perfecto hacia adelante completo (Nivel 5) después de recibir NSR - Cifrado autenticado mediante AEAD (cifrado autenticado con datos asociados) - La etiqueta actúa como datos asociados adicionales - Máximo de 65535 mensajes por tagset (conjunto de etiquetas) antes de que sea necesario un ratchet (mecanismo de derivación incremental de claves)

---

## Funciones de derivación de claves

Esta sección documenta todas las operaciones KDF (función de derivación de claves) utilizadas en ECIES, mostrando las derivaciones criptográficas completas.

### Notación y constantes

**Constantes:** - `ZEROLEN` - Matriz de bytes de longitud cero (cadena vacía) - `||` - Operador de concatenación

**Variables:** - `h` - Hash acumulado de la transcripción (32 bytes) - `chainKey` - Clave de encadenamiento para HKDF (32 bytes) - `k` - Clave de cifrado simétrico (32 bytes) - `n` - Nonce / número de mensaje

**Claves:** - `ask` / `apk` - clave privada/pública estática de Alice - `aesk` / `aepk` - clave privada/pública efímera de Alice - `bsk` / `bpk` - clave privada/pública estática de Bob - `besk` / `bepk` - clave privada/pública efímera de Bob

### Funciones de derivación de claves para mensajes NS

### KDF 1: Clave de cadena inicial

Se realiza una vez durante la inicialización del protocolo (puede precalcularse):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Resultado:** - `chainKey` = clave de encadenamiento inicial para todas las KDF posteriores (funciones de derivación de claves) - `h` = hash inicial de la transcripción

### KDF 2 (función de derivación de claves): Mezcla de clave estática de Bob

Bob realiza esto una vez (puede precalcularse para todas las sesiones entrantes):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Generación de clave efímera de Alice

Alice genera claves nuevas para cada NS message (mensaje NS):

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: Sección de clave estática de NS (es DH)

Deriva claves para cifrar la clave estática de Alice:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: Sección de carga útil de NS (ss DH, solo vinculada)

Para sesiones vinculadas, realiza un segundo DH (intercambio de claves Diffie-Hellman) para cifrar la carga útil:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Notas importantes:**

1. **Bound (vinculado) vs Unbound (no vinculado)**: 
   - Bound realiza 2 operaciones DH (Diffie–Hellman) (es + ss)
   - Unbound realiza 1 operación DH (solo es)
   - Unbound incrementa el nonce (número usado una vez) en lugar de derivar una clave nueva

2. **Seguridad frente a la reutilización de claves**:
   - Nonces (valor único de un solo uso) diferentes (0 vs 1) evitan la reutilización de clave/nonce
   - Datos asociados diferentes (h es diferente) proporcionan separación de dominios

3. **Transcripción del hash**:
   - `h` ahora contiene: protocol_name, prólogo vacío, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Esta transcripción vincula todas las partes del mensaje NS entre sí

### NSR Reply Tagset KDF (función de derivación de claves del conjunto de etiquetas de respuesta de NSR)

Bob genera etiquetas para los mensajes NSR:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### Funciones de derivación de claves del mensaje NSR

### KDF 6: Generación de claves efímeras de NSR

Bob genera una clave efímera nueva para cada NSR (solicitud de sesión de Noise):

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: Sección de claves de NSR (ee (efímero-efímero) y se (estático-efímero) DH)

Deriva claves para la sección de claves de NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Crítico**: Esto completa el handshake Noise IK (intercambio inicial del protocolo Noise IK). `chainKey` ahora contiene contribuciones de las 4 operaciones DH (es, ss, ee, se).

### KDF 8: Sección de carga útil de NSR

Deriva claves para el cifrado de la carga útil de NSR:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Notas importantes:**

1. **Operación de división**: 
   - Crea claves independientes para cada dirección
   - Evita la reutilización de claves entre Alice→Bob y Bob→Alice

2. **Vinculación de la carga útil NSR**:
   - Usa `h` como datos asociados para vincular la carga útil al handshake (proceso de establecimiento de conexión)
   - Una KDF (función de derivación de claves) independiente ("AttachPayloadKDF") proporciona separación de dominios

3. **Preparación para ES**:
   - Después de NSR, ambas partes pueden enviar mensajes ES
   - Alice debe recibir NSR antes de enviar ES
   - Bob debe recibir ES antes de enviar ES

### KDFs de mensajes de ES

Los mensajes ES usan claves de sesión generadas previamente a partir de los tagsets (conjuntos de etiquetas):

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Proceso del receptor:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### Función DH_INITIALIZE

Crea un tagset (conjunto de etiquetas) para un único sentido:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Contextos de uso:**

1. **Conjunto de etiquetas NSR**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **Conjuntos de etiquetas ES**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Conjuntos de etiquetas con ratchet (mecanismo criptográfico de avance)**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Mecanismos de trinquete

ECIES (esquema de cifrado integrado sobre curvas elípticas) utiliza tres mecanismos de ratchet (mecanismo de avance criptográfico) sincronizados para proporcionar secreto hacia adelante y una gestión eficiente de sesiones.

### Descripción general de Ratchet (mecanismo de trinquete)

**Tres tipos de Ratchet (mecanismo de avance escalonado):**

1. **DH Ratchet** (mecanismo de avance criptográfico): Realiza intercambios de claves Diffie-Hellman para generar nuevas claves raíz
2. **Session Tag Ratchet**: Deriva etiquetas de sesión de un solo uso de forma determinista
3. **Symmetric Key Ratchet**: Deriva claves de sesión para el cifrado de mensajes

**Relación:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Propiedades clave:**

- **Remitente**: Genera etiquetas y claves bajo demanda (no se necesita almacenamiento)
- **Receptor**: Pre-genera etiquetas para una ventana de anticipación (se requiere almacenamiento)
- **Sincronización**: El índice de la etiqueta determina el índice de la clave (N_tag = N_key)
- **Secreto hacia adelante**: Logrado mediante un DH ratchet (mecanismo de avance Diffie–Hellman) periódico
- **Eficiencia**: El receptor puede aplazar el cálculo de la clave hasta que se reciba la etiqueta

### DH Ratchet (mecanismo de avance de claves Diffie-Hellman)

El DH ratchet (mecanismo de avance de Diffie-Hellman) proporciona secreto hacia adelante al intercambiar periódicamente nuevas claves efímeras.

### Frecuencia del DH Ratchet (mecanismo de trinquete Diffie‑Hellman)

**Condiciones requeridas del Ratchet (mecanismo de avance criptográfico):** - Conjunto de etiquetas próximo al agotamiento (la etiqueta 65535 es el máximo) - Políticas específicas de la implementación:   - Umbral de cantidad de mensajes (p. ej., cada 4096 mensajes)   - Umbral de tiempo (p. ej., cada 10 minutos)   - Umbral de volumen de datos (p. ej., cada 100 MB)

**Primer Ratchet recomendado** (mecanismo de avance criptográfico): Alrededor del número de etiqueta 4096 para evitar alcanzar el límite

**Valores máximos:** - **ID máximo del conjunto de etiquetas**: 65535 - **ID máximo de clave**: 32767 - **Máximo de mensajes por conjunto de etiquetas**: 65535 - **Máximo teórico de datos por sesión**: ~6.9 TB (64K conjuntos de etiquetas × 64K mensajes × 1730 bytes promedio)

### Identificadores de etiquetas y de claves del DH Ratchet (mecanismo de avance Diffie-Hellman)

**Conjunto de etiquetas inicial** (tras el handshake): - ID del conjunto de etiquetas: 0 - Aún no se han enviado bloques NextKey (siguiente clave) - No se han asignado IDs de clave

**Después del primer Ratchet (mecanismo de trinquete criptográfico)**: - ID del conjunto de etiquetas: 1 = (1 + ID de clave de Alice + ID de clave de Bob) = (1 + 0 + 0) - Alice envía NextKey con ID de clave 0 - Bob responde con NextKey con ID de clave 0

**Conjuntos de etiquetas posteriores**: - ID del conjunto de etiquetas = 1 + ID de la clave del emisor + ID de la clave del receptor - Ejemplo: Conjunto de etiquetas 5 = (1 + sender_key_2 + receiver_key_2)

**Tabla de progresión del conjunto de etiquetas:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Nueva clave generada en este ratchet (mecanismo de actualización de claves criptográficas)

**Reglas del ID de clave:** - Los ID son secuenciales a partir de 0 - Los ID se incrementan solo cuando se genera una nueva clave - El ID de clave máximo es 32767 (15 bits) - Después del ID de clave 32767, se requiere una nueva sesión

### Flujo de mensajes de DH Ratchet (mecanismo de avance criptográfico Diffie-Hellman)

**Roles:** - **Remitente de etiquetas**: Posee el conjunto de etiquetas de salida, envía mensajes - **Receptor de etiquetas**: Posee el conjunto de etiquetas de entrada, recibe mensajes

**Patrón:** El emisor de etiquetas inicia el ratchet (mecanismo de avance criptográfico) cuando el conjunto de etiquetas está a punto de agotarse.

**Diagrama de flujo de mensajes:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Patrones de Ratchet (mecanismo de trinquete):**

**Creación de Tag Sets (conjuntos de etiquetas) de número par** (2, 4, 6, ...): 1. El emisor genera una nueva clave 2. El emisor envía un NextKey block (bloque NextKey) con la nueva clave 3. El receptor envía un NextKey block con el ID de la clave antigua (ACK, acuse de recibo) 4. Ambos realizan DH (Diffie-Hellman) con (nueva clave del emisor × clave antigua del receptor)

**Creación de conjuntos de etiquetas con numeración impar** (3, 5, 7, ...): 1. El remitente solicita la clave inversa (envía NextKey (siguiente clave) con el indicador de solicitud) 2. El receptor genera una nueva clave 3. El receptor envía un bloque NextKey con la nueva clave 4. Ambos realizan Diffie-Hellman (DH) con (clave antigua del remitente × clave nueva del receptor)

### Formato del bloque NextKey (siguiente clave)

Consulte la sección Formato de la carga útil para obtener la especificación detallada del bloque NextKey (siguiente clave).

**Elementos clave:** - **Byte de indicadores**:   - Bit 0: Clave presente (1) o solo ID (0)   - Bit 1: Clave inversa (1) o clave directa (0)   - Bit 2: Solicitar clave inversa (1) o sin solicitud (0) - **ID de clave**: 2 bytes, big-endian (0-32767) - **Clave pública**: 32 bytes X25519 (si el bit 0 = 1)

**Ejemplos de bloques NextKey (siguiente clave):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### KDF (función de derivación de claves) del DH Ratchet (mecanismo de trinquete)

Cuando se intercambian nuevas claves:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Temporización crítica:**

**Remitente de etiquetas:** - Crea un nuevo conjunto de etiquetas salientes de inmediato - Comienza a usar las nuevas etiquetas de inmediato - Elimina el conjunto de etiquetas salientes antiguo

**Receptor de etiquetas:** - Crea un nuevo conjunto de etiquetas entrantes - Conserva el conjunto de etiquetas entrantes anterior durante el período de gracia (3 minutos) - Acepta etiquetas de ambos conjuntos, el antiguo y el nuevo, durante el período de gracia - Elimina el conjunto de etiquetas entrantes anterior tras el período de gracia

### Gestión del estado de DH Ratchet (mecanismo de avance de Diffie-Hellman)

**Estado del remitente:** - Conjunto de etiquetas salientes actual - ID del conjunto de etiquetas e IDs de claves - Siguiente clave raíz (para el próximo ratchet (mecanismo de avance criptográfico)) - Número de mensajes en el conjunto de etiquetas actual

**Estado del receptor:** - Conjunto(s) actual(es) de etiquetas entrantes (puede haber 2 durante el período de gracia) - Números de mensajes anteriores (PN) para la detección de huecos - Ventana de anticipación de etiquetas pre-generadas - Siguiente clave raíz (para el siguiente ratchet, mecanismo de avance criptográfico)

**Reglas de transición de estado:**

1. **Antes del primer Ratchet (mecanismo de avance criptográfico)**:
   - Usando el conjunto de etiquetas 0 (de NSR)
   - No hay identificadores de clave asignados

2. **Iniciando Ratchet (mecanismo de avance criptográfico)**:
   - Generar nueva clave (si en esta ronda le toca generar al remitente)
   - Enviar el bloque NextKey en el mensaje ES
   - Esperar la respuesta de NextKey antes de crear un nuevo conjunto de etiquetas de salida

3. **Recepción de una solicitud de Ratchet (mecanismo de avance criptográfico)**:
   - Generar una nueva clave (si el receptor está generando en esta ronda)
   - Realizar DH (Diffie-Hellman) con la clave recibida
   - Crear un nuevo conjunto de etiquetas de entrada
   - Enviar NextKey reply (respuesta NextKey)
   - Conservar el conjunto de etiquetas de entrada anterior durante un período de gracia

4. **Completar Ratchet (mecanismo de actualización de claves)**:
   - Recibir la respuesta NextKey
   - Realizar DH
   - Crear un nuevo conjunto de etiquetas de salida
   - Comenzar a usar las nuevas etiquetas

### Ratchet de etiquetas de sesión (mecanismo de avance criptográfico)

El session tag ratchet (mecanismo de avance criptográfico para etiquetas de sesión) genera session tags de 8 bytes de un solo uso de forma determinista.

### Propósito del Session Tag Ratchet (mecanismo de avance criptográfico para etiquetas de sesión)

- Sustituye la transmisión explícita de etiquetas (ElGamal enviaba etiquetas de 32 bytes)
- Permite al receptor pre-generar etiquetas para una ventana de anticipación
- El emisor las genera bajo demanda (no requiere almacenamiento)
- Se sincroniza con el ratchet (mecanismo de avance) de clave simétrica mediante un índice

### Fórmula del ratchet (mecanismo de avance tipo trinquete) de etiquetas de sesión

**Inicialización:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Generación de etiqueta (para la etiqueta N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Secuencia completa:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Implementación del emisor de Session Tag Ratchet (mecanismo de avance criptográfico de etiquetas de sesión)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Proceso del emisor:** 1. Llamar a `get_next_tag()` para cada mensaje 2. Usar la etiqueta devuelta en el mensaje ES 3. Almacenar el índice N para un posible seguimiento de ACK (confirmación de recepción) 4. No es necesario almacenar la etiqueta (se genera bajo demanda)

### Implementación del receptor de Session Tag Ratchet

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Proceso del receptor:** 1. Pre-generar etiquetas para la ventana de anticipación (p. ej., 32 etiquetas) 2. Almacenar las etiquetas en una tabla hash o diccionario 3. Cuando llegue el mensaje, consultar la etiqueta para obtener el índice N 4. Eliminar la etiqueta del almacenamiento (uso único) 5. Ampliar la ventana si el recuento de etiquetas cae por debajo del umbral

### Estrategia de anticipación de etiquetas de sesión

**Propósito**: Equilibrar el uso de memoria frente al manejo de mensajes fuera de orden

**Tamaños de anticipación recomendados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Anticipación adaptativa:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Recortar por detrás:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Cálculo de memoria:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Manejo de etiquetas de sesión fuera de orden

**Escenario**: Los mensajes llegan fuera de orden

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Comportamiento del receptor:**

1. Recibir tag_5:
   - Buscar: encontrado en el índice 5
   - Procesar mensaje
   - Eliminar tag_5
   - Máximo recibido: 5

2. Se recibe tag_7 (fuera de orden):
   - Búsqueda: encontrado en el índice 7
   - Procesar el mensaje
   - Eliminar tag_7
   - Máximo recibido: 7
   - Nota: tag_6 sigue en almacenamiento (aún no se ha recibido)

3. Recibir tag_6 (retrasado):
   - Buscar: encontrado en el índice 6
   - Procesar mensaje
   - Eliminar tag_6
   - Máximo recibido: 7 (sin cambios)

4. Recibir tag_8:
   - Buscar: encontrado en el índice 8
   - Procesar mensaje
   - Eliminar tag_8
   - Máximo recibido: 8

**Mantenimiento de la ventana:** - Llevar un registro del índice más alto recibido - Mantener una lista de índices faltantes (gaps, huecos) - Ampliar la ventana en función del índice más alto - Opcional: Expirar los huecos antiguos tras un tiempo de espera

### Ratchet de clave simétrica (mecanismo de rotación progresiva de claves simétricas)

El symmetric key ratchet (mecanismo de avance de clave simétrica) genera claves de cifrado de 32 bytes sincronizadas con etiquetas de sesión.

### Propósito del Symmetric Key Ratchet (mecanismo de avance de clave simétrica)

- Proporciona una clave de cifrado única para cada mensaje
- Sincronizado con session tag ratchet (mecanismo de avance de etiquetas de sesión) (mismo índice)
- El emisor puede generarla bajo demanda
- El receptor puede aplazar la generación hasta que se reciba la etiqueta

### Fórmula del Symmetric Key Ratchet (mecanismo de trinquete de clave simétrica)

**Inicialización:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Generación de la clave (para la clave N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Secuencia completa:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Implementación del emisor de Symmetric Key Ratchet (trinquete de clave simétrica)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Proceso del emisor:** 1. Obtener la siguiente etiqueta y su índice N 2. Generar la clave para el índice N 3. Usar la clave para cifrar el mensaje 4. No se requiere almacenamiento de claves

### Implementación del receptor del Symmetric Key Ratchet (mecanismo de avance de clave simétrica)

**Estrategia 1: Generación diferida (Recomendado)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Proceso de generación diferida:** 1. Recibir ES message (mensaje ES) con etiqueta 2. Consultar la etiqueta para obtener el índice N 3. Generar las claves de 0 a N (si aún no se han generado) 4. Usar la clave N para descifrar el mensaje 5. La clave de cadena ahora se encuentra en el índice N

**Ventajas:** - Uso mínimo de memoria - Claves generadas solo cuando se necesitan - Implementación simple

**Desventajas:** - Debe generar todas las claves de 0 a N la primera vez que se use - No puede procesar mensajes fuera de orden sin almacenamiento en caché

**Estrategia 2: Pregeneración con ventana de etiquetas (Alternativa)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Proceso de pre-generación:** 1. Pre-generar claves que coincidan con la ventana de etiquetas (p. ej., 32 claves) 2. Almacenar las claves indexadas por número de mensaje 3. Cuando se reciba la etiqueta, buscar la clave correspondiente 4. Ampliar la ventana a medida que se utilicen las etiquetas

**Ventajas:** - Maneja mensajes fuera de orden de forma natural - Recuperación rápida de claves (sin demora de generación)

**Desventajas:** - Mayor uso de memoria (32 bytes por clave frente a 8 bytes por etiqueta) - Es necesario mantener las claves sincronizadas con las etiquetas

**Comparación de memoria:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Sincronización del Ratchet (mecanismo de avance criptográfico) simétrico con etiquetas de sesión

**Requisito crítico**: El índice de etiqueta de sesión DEBE ser igual al índice de clave simétrica

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Modos de fallo:**

Si falla la sincronización: - Clave incorrecta utilizada para el descifrado - La verificación de MAC falla - Mensaje rechazado

**Prevención:** - Usa siempre el mismo índice para la etiqueta y la clave - Nunca omitas índices en ninguno de los ratchets (mecanismo de actualización criptográfica) - Gestiona con cuidado los mensajes fuera de orden

### Construcción del nonce del trinquete simétrico

El Nonce (número aleatorio de un solo uso) se deriva del número de mensaje:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Ejemplos:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Propiedades importantes:** - Los Nonces (valores únicos usados una vez) son únicos para cada mensaje en un conjunto de etiquetas - Los Nonces nunca se repiten (las etiquetas de un solo uso lo garantizan) - El contador de 8 bytes permite 2^64 mensajes (solo usamos 2^16) - El formato del Nonce coincide con la construcción basada en contador de la RFC 7539

---

## Gestión de sesiones

### Contexto de sesión

Todas las sesiones entrantes y salientes deben pertenecer a un contexto específico:

1. **Contexto del router**: Sesiones para el propio router
2. **Contexto de destino**: Sesiones para un destino local específico (aplicación cliente)

**Regla crítica**: Las sesiones NO DEBEN compartirse entre contextos para evitar ataques de correlación.

**Implementación:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Implementación de I2P en Java:**

En Java I2P, la clase `SessionKeyManager` (gestor de claves de sesión) proporciona esta funcionalidad: - Un `SessionKeyManager` por router - Un `SessionKeyManager` por destino local - Gestión separada de las sesiones ECIES y ElGamal dentro de cada contexto

### Vinculación de sesión

**Vinculación** asocia una sesión con un destino remoto específico.

### Sesiones vinculadas

**Características:** - Incluir la clave estática del remitente en el mensaje NS - El destinatario puede identificar el destino del remitente - Permite comunicación bidireccional - Una sola sesión saliente por destino - Puede tener varias sesiones entrantes (durante transiciones)

**Casos de uso:** - Conexiones de streaming (similar a TCP) - Datagramas con posibilidad de respuesta - Cualquier protocolo que requiera solicitud/respuesta

**Proceso de vinculación:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Beneficios:** 1. **Ephemeral-Ephemeral DH** (Diffie-Hellman efímero-efímero): La respuesta usa ee DH (secreto perfecto hacia adelante) 2. **Continuidad de sesión**: Ratchets (mecanismos de avance criptográfico) mantienen la vinculación con el mismo destino 3. **Seguridad**: Evita el secuestro de sesión (autenticado por clave estática) 4. **Eficiencia**: Una sola sesión por destino (sin duplicación)

### Sesiones no vinculadas

**Características:** - No hay clave estática en el mensaje NS (la sección de indicadores está compuesta únicamente por ceros) - El destinatario no puede identificar al remitente - Comunicación unidireccional únicamente - Se permiten múltiples sesiones hacia el mismo destino

**Casos de uso:** - Datagramas sin formato (enviar y olvidar) - Publicación anónima - Mensajería estilo broadcast (difusión a todos los destinatarios)

**Propiedades:** - Más anónimo (sin identificación del remitente) - Más eficiente (1 DH (Diffie-Hellman) vs 2 DH en el handshake) - No es posible responder (el destinatario no sabe dónde responder) - Sin session ratcheting (uso único o limitado)

### Emparejamiento de sesiones

**Emparejamiento** conecta una sesión entrante con una sesión saliente para comunicación bidireccional.

### Creación de sesiones emparejadas

**Perspectiva de Alice (iniciadora):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Perspectiva de Bob (receptor):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Beneficios del emparejamiento de sesiones

1. **ACKs en banda**: Se pueden confirmar mensajes sin un clove separado (clove: submensaje encapsulado)
2. **Ratcheting eficiente (mecanismo criptográfico de avance "ratchet")**: Ambas direcciones avanzan el ratchet conjuntamente
3. **Control de flujo**: Se puede implementar contrapresión a través de sesiones emparejadas
4. **Consistencia del estado**: Más fácil mantener el estado sincronizado

### Reglas de emparejamiento de sesiones

- La sesión saliente puede estar no emparejada (NS no vinculado)
- La sesión entrante para un NS vinculado debería estar emparejada
- El emparejamiento ocurre al crear la sesión, no después
- Las sesiones emparejadas tienen la misma vinculación de destino
- Los ratchets (mecanismos de avance criptográfico) ocurren de forma independiente pero están coordinados

### Ciclo de vida de la sesión

### Ciclo de vida de la sesión: fase de creación

**Creación de sesión saliente (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Creación de sesión entrante (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Ciclo de vida de la sesión: Fase activa

**Transiciones de estado:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Mantenimiento activo de la sesión:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Ciclo de vida de la sesión: fase de expiración

**Valores de tiempo de espera de la sesión:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Lógica de expiración:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Regla crítica**: Las sesiones salientes DEBEN expirar antes que las sesiones entrantes para evitar la desincronización.

**Terminación ordenada:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Múltiples mensajes NS

**Escenario**: El mensaje NS de Alice se pierde o se pierde la respuesta NSR.

**Comportamiento de Alice:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Propiedades importantes:**

1. **Claves efímeras únicas**: Cada NS usa una clave efímera diferente
2. **Negociaciones independientes**: Cada NS crea un estado de negociación por separado
3. **Correlación de NSR**: La etiqueta NSR identifica a qué NS responde
4. **Limpieza de estado**: Los estados de NS no utilizados se descartan tras una NSR satisfactoria

**Prevención de ataques:**

Para evitar el agotamiento de recursos:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Múltiples mensajes NSR

**Escenario**: Bob envía múltiples NSRs (p. ej., datos de respuesta divididos en varios mensajes).

**Comportamiento de Bob:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Comportamiento de Alice:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Limpieza de Bob:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Propiedades importantes:**

1. **Se permiten múltiples NSRs (solicitudes de sesión Noise)**: Bob puede enviar múltiples NSRs por cada NS (sesión Noise)
2. **Claves efímeras diferentes**: Cada NSR debe usar una clave efímera única
3. **Mismo conjunto de etiquetas de NSR**: Todas las NSRs para una NS usan el mismo conjunto de etiquetas
4. **Gana el primer ES (patrón Ephemeral-Static de Noise)**: El primer ES de Alice determina cuál NSR tuvo éxito
5. **Limpieza después del ES**: Bob descarta los estados no utilizados tras recibir el ES

### Máquina de estados de la sesión

**Diagrama de estados completo:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Descripciones de estado:**

- **NEW**: Sesión saliente creada, aún no se ha enviado ningún NS
- **PENDING_REPLY**: NS enviado, esperando NSR
- **AWAITING_ES**: NSR enviado, esperando el primer ES de Alice
- **ESTABLISHED**: Negociación completada, puede enviar/recibir ES
- **ACTIVE**: Intercambiando mensajes ES activamente
- **RATCHETING**: DH ratchet (mecanismo de avance criptográfico de Diffie-Hellman) en progreso (subconjunto de ACTIVE)
- **EXPIRED**: Sesión caducada por tiempo de espera, pendiente de eliminación
- **TERMINATED**: Sesión terminada explícitamente

---

## Formato de carga útil

La sección de carga útil de todos los mensajes ECIES (esquema de cifrado integrado con curvas elípticas) (NS, NSR, ES) utiliza un formato basado en bloques similar a NTCP2.

### Estructura de bloques

**Formato general:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 1 byte - Número de tipo de bloque
- `size`: 2 bytes - Tamaño del campo de datos en big-endian (0-65516)
- `data`: Longitud variable - Datos específicos del bloque

**Restricciones:**

- Tamaño máximo de la trama ChaChaPoly: 65535 bytes
- MAC Poly1305: 16 bytes
- Tamaño máximo total de bloques: 65519 bytes (65535 - 16)
- Tamaño máximo de un bloque: 65519 bytes (incluye encabezado de 3 bytes)
- Tamaño máximo de datos de un bloque: 65516 bytes

### Tipos de bloques

**Tipos de bloques definidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Manejo de bloques desconocidos:**

Las implementaciones DEBEN ignorar los bloques con números de tipo desconocido y tratarlos como relleno. Esto garantiza la compatibilidad con futuras versiones.

### Reglas de ordenamiento de bloques

### Orden de mensajes NS

**Obligatorio:** - El bloque DateTime DEBE ser el primero

**Permitidos:** - Garlic Clove (submensaje "clove" de I2P) (tipo 11) - Opciones (tipo 5) - si está implementado - Relleno (tipo 254)

**Prohibido:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Ejemplo de carga útil NS válida:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Orden de mensajes de NSR

**Obligatorio:** - Ninguno (la carga útil puede estar vacía)

**Permitidos:** - Garlic Clove (submensaje de garlic encryption) (tipo 11) - Opciones (tipo 5) - si está implementado - Relleno (tipo 254)

**Prohibido:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Ejemplo de carga útil NSR válida:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
o

```
(empty - ACK only)
```
### Orden de mensajes de ES

**Obligatorio:** - Ninguno (la carga útil puede estar vacía)

**Permitidos (en cualquier orden):** - Garlic Clove (tipo 11) - NextKey (tipo 7) - ACK (tipo 8) - ACK Request (tipo 9) - Termination (tipo 4) - si se implementa - MessageNumbers (tipo 6) - si se implementa - Options (tipo 5) - si se implementa - Padding (tipo 254)

**Reglas especiales:** - Termination DEBE ser el último bloque (excepto Padding) - Padding DEBE ser el último bloque - Se permiten múltiples Garlic Cloves (submensajes dentro de un mensaje de garlic encryption) - Se permiten hasta 2 bloques NextKey (directo e inverso) - NO se permiten múltiples bloques de Padding

**Ejemplos de cargas útiles ES válidas:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### Bloque DateTime (Tipo 0)

**Propósito**: Marca de tiempo para la prevención de ataques de repetición y la validación del desfase del reloj

**Tamaño**: 7 bytes (cabecera de 3 bytes + datos de 4 bytes)

**Formato:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 0
- `size`: 4 (big-endian, orden de bytes más significativo primero)
- `timestamp`: 4 bytes - marca de tiempo Unix en segundos (sin signo, big-endian)

**Formato de marca de tiempo:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Reglas de validación:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Prevención de ataques de repetición:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Notas de implementación:**

1. **Mensajes NS**: DateTime DEBE ser el primer bloque
2. **Mensajes NSR/ES**: DateTime normalmente no se incluye
3. **Ventana de repetición**: 5 minutos es el mínimo recomendado
4. **Filtro de Bloom**: Recomendado para una detección eficiente de repeticiones
5. **Desfase del reloj**: Permitir 5 minutos hacia el pasado, 2 minutos hacia el futuro

### Bloque Garlic Clove (sub-bloque en garlic encryption) (Tipo 11)

**Propósito**: Encapsula mensajes I2NP para su entrega

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 11
- `size`: Tamaño total de clove (submensaje dentro de un garlic message) (variable)
- `Delivery Instructions`: Como se especifica en la especificación de I2NP
- `type`: Tipo de mensaje I2NP (1 byte)
- `Message_ID`: ID de mensaje I2NP (4 bytes)
- `Expiration`: Marca de tiempo Unix en segundos (4 bytes)
- `I2NP Message body`: Datos de mensaje de longitud variable

**Formatos de instrucciones de entrega:**

**Entrega local** (1 byte):

```
+----+
|0x00|
+----+
```
**Entrega al destino** (33 bytes):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Entrega al router** (33 bytes):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Entrega vía Tunnel** (37 bytes):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Encabezado de mensaje de I2NP** (9 bytes en total):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: Tipo de mensaje I2NP (Database Store, Database Lookup, Data, etc.)
- `msg_id`: identificador de mensaje de 4 bytes
- `expiration`: marca de tiempo Unix de 4 bytes (segundos)

**Diferencias importantes con respecto al formato Clove (submensaje en I2P) de ElGamal:**

1. **Sin certificado**: Se omite el campo de certificado (no se utiliza en ElGamal)
2. **Sin Clove ID**: Se omite el Clove ID (siempre era 0)
3. **Sin expiración de Clove**: En su lugar, se utiliza la expiración del mensaje I2NP
4. **Encabezado compacto**: Encabezado I2NP de 9 bytes frente al formato ElGamal más grande
5. **Cada Clove (submensaje dentro de garlic encryption) es un bloque separado**: No hay estructura CloveSet

**Múltiples Cloves (submensajes dentro de un mensaje garlic):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Tipos comunes de mensajes I2NP en Cloves (submensajes dentro de garlic encryption):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Procesamiento de Clove (diente de ajo):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### Bloque NextKey (Tipo 7)

**Propósito**: intercambio de claves mediante DH ratchet (mecanismo de avance de Diffie-Hellman)

**Formato (Clave presente - 38 bytes):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Formato (solo ID de clave - 6 bytes):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 7
- `size`: 3 (solo ID) o 35 (con clave)
- `flag`: 1 byte - Bits de bandera
- `key ID`: 2 bytes - Identificador de clave Big-endian (byte más significativo primero) (0-32767)
- `Public Key`: 32 bytes - Clave pública X25519 (little-endian; byte menos significativo primero), si el bit 0 de la bandera = 1

**Bits de bandera:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Ejemplos de banderas:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Reglas del identificador de clave:**

- Los ID son secuenciales: 0, 1, 2, ..., 32767
- El ID solo se incrementa cuando se genera una nueva clave
- Se usa el mismo ID para varios mensajes hasta el próximo ratchet (mecanismo de trinquete)
- El ID máximo es 32767 (después hay que iniciar una sesión nueva)

**Ejemplos de uso:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Lógica de procesamiento:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Múltiples NextKey Blocks (bloques NextKey):**

Un único mensaje ES puede contener hasta 2 bloques NextKey cuando ambas direcciones están realizando ratcheting (avance de claves tipo “ratchet”) simultáneamente:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### Bloque ACK (Tipo 8)

**Propósito**: Confirmar la recepción de mensajes en banda

**Formato (ACK único - 7 bytes):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Formato (Múltiples ACKs):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 8
- `size`: 4 * número de ACKs (confirmaciones) (mínimo 4)
- Para cada ACK:
  - `tagsetid`: 2 bytes - ID del conjunto de etiquetas en Big-endian (0-65535)
  - `N`: 2 bytes - número de mensaje en Big-endian (0-65535)

**Determinación del ID del conjunto de etiquetas:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Ejemplo de ACK único:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Ejemplo de múltiples ACK (confirmaciones):**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Procesamiento:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Cuándo enviar acuses de recibo:**

1. **ACK Request explícita**: Responda siempre al bloque ACK Request (ACK: acuse de recibo)
2. **Entrega de LeaseSet**: Cuando el remitente incluye el LeaseSet en el mensaje
3. **Establecimiento de sesión**: Puede enviar un ACK a NS/NSR (aunque el protocolo prefiere un ACK implícito vía ES)
4. **Confirmación de ratchet (mecanismo de avance criptográfico)**: Puede enviar ACK al recibir NextKey
5. **Capa de aplicación**: Según lo requiera el protocolo de capa superior (p. ej., Streaming)

**Temporización de ACK:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### Bloque de solicitud de ACK (Tipo 9)

**Propósito**: Solicitar acuse de recibo en banda del mensaje actual

**Formato:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Campos:**

- `blk`: 9
- `size`: 1
- `flg`: 1 byte - Indicadores (todos los bits actualmente sin uso, establecidos en 0)

**Uso:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Respuesta del receptor:**

Cuando se recibe ACK Request (petición de acuse de recibo):

1. **Con Immediate Data (datos inmediatos)**: Incluir el bloque ACK en la respuesta inmediata
2. **Sin Immediate Data**: Iniciar un temporizador (p. ej., 100 ms) y enviar un ES vacío con ACK si el temporizador expira
3. **Tag Set ID (ID del conjunto de etiquetas)**: Usar el ID de tagset entrante actual
4. **Número de mensaje**: Usar el número de mensaje asociado con la session tag (etiqueta de sesión) recibida

**Procesamiento:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Cuándo usar ACK Request (solicitud de acuse de recibo):**

1. **Mensajes críticos**: Mensajes que requieren acuse de recibo
2. **Entrega de LeaseSet**: Al incluir un LeaseSet
3. **Session Ratchet** (mecanismo de avance de claves de sesión): Después de enviar el NextKey block (bloque para la siguiente clave)
4. **Fin de la transmisión**: Cuando el emisor no tiene más datos que enviar pero quiere confirmación

**Cuándo NO usarlo:**

1. **Protocolo de streaming**: La capa de streaming gestiona los ACKs (confirmaciones de recepción)
2. **Mensajes de alta frecuencia**: Evite la solicitud de ACK en cada mensaje (sobrecarga)
3. **Datagramas no importantes**: Los datagramas sin formato por lo general no necesitan ACKs

### Bloque de Terminación (Tipo 4)

**Estado**: SIN IMPLEMENTAR

**Propósito**: Finalizar la sesión de forma ordenada

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 4
- `size`: 1 o más bytes
- `rsn`: 1 byte - Código de motivo
- `addl data`: Datos adicionales opcionales (el formato depende del motivo)

**Códigos de motivo:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Uso (cuando se implemente):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Reglas:**

- DEBE ser el último bloque excepto Padding (relleno)
- Padding DEBE seguir a Termination (terminación) si está presente
- No permitido en mensajes NS o NSR
- Solo permitido en mensajes ES

### Bloque de opciones (Tipo 5)

**Estado**: SIN IMPLEMENTAR

**Propósito**: Negociar parámetros de sesión

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 5
- `size`: 21 bytes o más
- `ver`: 1 byte - Versión del protocolo (debe ser 0)
- `flg`: 1 byte - Indicadores (todos los bits actualmente sin usar)
- `STL`: 1 byte - Longitud de la etiqueta de sesión (debe ser 8)
- `STimeout`: 2 bytes - Tiempo de espera de inactividad de la sesión en segundos (big-endian)
- `SOTW`: 2 bytes - Ventana de etiquetas salientes del remitente (big-endian)
- `RITW`: 2 bytes - Ventana de etiquetas entrantes del receptor (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: 1 byte cada uno - Parámetros de relleno (punto fijo 4.4)
- `tdmy`: 2 bytes - Tráfico de relleno máximo que está dispuesto a enviar (bytes/s, big-endian)
- `rdmy`: 2 bytes - Tráfico de relleno solicitado (bytes/s, big-endian)
- `tdelay`: 2 bytes - Retraso intra-mensaje máximo que está dispuesto a insertar (ms, big-endian)
- `rdelay`: 2 bytes - Retraso intra-mensaje solicitado (ms, big-endian)
- `more_options`: Variable - Extensiones futuras

**Parámetros de relleno (formato de punto fijo 4.4):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Negociación de la ventana de etiquetas:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Valores predeterminados (cuando no se negocian opciones):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### Bloque MessageNumbers (Tipo 6)

**Estado**: NO IMPLEMENTADO

**Propósito**: Indicar el último mensaje enviado en el conjunto de etiquetas anterior (permite la detección de huecos)

**Formato:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Campos:**

- `blk`: 6
- `size`: 2
- `PN`: 2 bytes - Número del último mensaje del conjunto de etiquetas anterior (big-endian (orden de bytes de mayor a menor significancia), 0-65535)

**Definición de PN (Número anterior):**

PN es el índice de la última etiqueta enviada en el conjunto de etiquetas anterior.

**Uso (cuando esté implementado):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Beneficios para el receptor:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Reglas:**

- NO DEBE enviarse en el conjunto de etiquetas 0 (no hay conjunto de etiquetas previo)
- Solo se envía en mensajes ES
- Solo se envía en el/los primer(os) mensaje(s) de un nuevo conjunto de etiquetas
- El valor PN es desde la perspectiva del remitente (última etiqueta que envió el remitente)

**Relación con Signal:**

En Signal Double Ratchet (protocolo de doble trinquete de Signal), PN está en la cabecera del mensaje. En ECIES, está en la carga útil cifrada y es opcional.

### Bloque de relleno (Tipo 254)

**Propósito**: Resistencia al análisis de tráfico y ofuscación del tamaño de los mensajes

**Formato:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 254
- `size`: 0-65516 bytes (big-endian, más significativo primero)
- `padding`: Datos aleatorios o ceros

**Reglas:**

- DEBE ser el último bloque del mensaje
- NO se permiten múltiples bloques de relleno
- Puede tener longitud cero (solo encabezado de 3 bytes)
- Los datos de relleno pueden ser ceros o bytes aleatorios

**Relleno predeterminado:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Estrategias de resistencia al análisis de tráfico:**

**Estrategia 1: Tamaño aleatorio (predeterminado)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estrategia 2: Redondear a un múltiplo**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estrategia 3: Tamaños de mensajes fijos**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estrategia 4: Relleno negociado (Options block)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Mensajes solo de relleno:**

Los mensajes pueden consistir completamente en relleno (sin datos de la aplicación):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Notas de implementación:**

1. **Relleno de ceros**: Aceptable (será cifrado por ChaCha20)
2. **Relleno aleatorio**: No aporta seguridad adicional tras el cifrado, pero consume más entropía
3. **Rendimiento**: La generación de relleno aleatorio puede ser costosa; considere usar ceros
4. **Memoria**: Los bloques de relleno grandes consumen ancho de banda; tenga cuidado con el tamaño máximo

---

## Guía de implementación

### Requisitos previos

**Bibliotecas criptográficas:**

- **X25519** (intercambio de claves de curva elíptica): libsodium, NaCl o Bouncy Castle
- **ChaCha20-Poly1305** (algoritmo AEAD: cifrado ChaCha20 con autenticación Poly1305): libsodium, OpenSSL 1.1.0+ o Bouncy Castle
- **SHA-256** (función hash criptográfica de 256 bits): OpenSSL, Bouncy Castle o soporte integrado en el lenguaje
- **Elligator2** (técnica de ofuscación de puntos en curvas elípticas): Soporte limitado en bibliotecas; puede requerir una implementación personalizada

**Implementación de Elligator2 (método de mapeo uniforme a curvas elípticas para ofuscación):**

Elligator2 (técnica criptográfica para ocultar claves públicas) no está ampliamente implementado. Opciones:

1. **OBFS4**: El pluggable transport (mecanismo de transporte modular) obfs4 de Tor incluye una implementación de Elligator2
2. **Implementación personalizada**: Basada en [Elligator2 paper](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: Implementación de referencia en GitHub

**Nota sobre Java I2P:** Java I2P usa la biblioteca net.i2p.crypto.eddsa con extensiones personalizadas de Elligator2 (técnica criptográfica para camuflar claves públicas).

### Orden recomendado de implementación

**Fase 1: Criptografía fundamental** 1. Generación e intercambio de claves DH X25519 2. Cifrado/descifrado con AEAD ChaCha20-Poly1305 3. Cálculo de hash SHA-256 y MixHash 4. Derivación de claves mediante HKDF 5. Codificación/decodificación Elligator2 (se pueden usar vectores de prueba inicialmente)

**Fase 2: Formatos de mensajes** 1. mensaje NS (no vinculado) - formato más simple 2. mensaje NS (vinculado) - añade clave estática 3. mensaje NSR 4. mensaje ES 5. Análisis y generación de bloques

**Fase 3: Gestión de sesión** 1. Creación y almacenamiento de sesión 2. Gestión del conjunto de etiquetas (emisor y receptor) 3. Ratchet (mecanismo de avance) de etiquetas de sesión 4. Ratchet de clave simétrica 5. Búsqueda de etiquetas y gestión de la ventana

**Fase 4: DH Ratcheting (avance de claves con Diffie-Hellman)** 1. Gestión del bloque NextKey 2. Función de derivación de claves (KDF) de DH ratchet 3. Creación del conjunto de etiquetas después del ratchet 4. Gestión de múltiples conjuntos de etiquetas

**Fase 5: Lógica del protocolo** 1. Máquina de estados NS/NSR/ES 2. Prevención de ataques de repetición (DateTime, filtro de Bloom) 3. Lógica de retransmisión (múltiples NS/NSR) 4. Gestión de ACK (acuse de recibo)

**Fase 6: Integración** 1. Procesamiento de I2NP Garlic Clove (unidad individual dentro de un mensaje de garlic encryption) 2. Agrupación de LeaseSet 3. Integración del protocolo de streaming 4. Integración del protocolo de datagramas

### Implementación del emisor

**Ciclo de vida de la sesión saliente:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Implementación del receptor

**Ciclo de vida de la sesión entrante:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Clasificación de mensajes

**Distinción de tipos de mensajes:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Mejores prácticas de gestión de sesiones

**Almacenamiento de sesión:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Gestión de memoria:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Estrategias de prueba

**Pruebas unitarias:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Pruebas de integración:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Vectores de prueba:**

Implementar vectores de prueba de la especificación:

1. **Noise IK Handshake**: Use vectores de prueba estándar de Noise
2. **HKDF**: Use vectores de prueba del RFC 5869
3. **ChaCha20-Poly1305**: Use vectores de prueba del RFC 7539
4. **Elligator2**: Use vectores de prueba del artículo de Elligator2 o de OBFS4

**Pruebas de interoperabilidad:**

1. **Java I2P**: Probar frente a la implementación de referencia de Java I2P
2. **i2pd**: Probar frente a la implementación de i2pd en C++
3. **Capturas de paquetes**: Usar el disector de Wireshark (si está disponible) para verificar los formatos de mensajes
4. **Entre implementaciones**: Crear un banco de pruebas que pueda enviar/recibir entre implementaciones

### Consideraciones de rendimiento

**Generación de claves:**

La generación de claves mediante Elligator2 (técnica criptográfica) es costosa (tasa de rechazo del 50%):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Búsqueda de etiquetas:**

Utiliza tablas hash para la búsqueda de etiquetas en O(1):

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Optimización de memoria:**

Diferir la generación de claves simétricas:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Procesamiento por lotes:**

Procesar múltiples mensajes por lotes:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Consideraciones de seguridad

### Modelo de amenazas

**Capacidades del adversario:**

1. **Observador pasivo**: Puede observar todo el tráfico de la red
2. **Atacante activo**: Puede inyectar, modificar, descartar y repetir mensajes
3. **Nodo comprometido**: Puede comprometer un router o un destino
4. **Análisis de tráfico**: Puede realizar análisis estadístico de los patrones de tráfico

**Objetivos de seguridad:**

1. **Confidencialidad**: Contenido del mensaje oculto para el observador
2. **Autenticación**: Identidad del remitente verificada (para sesiones vinculadas)
3. **Secreto perfecto hacia adelante**: Los mensajes pasados permanecen secretos incluso si se comprometen las claves
4. **Prevención de repetición**: No se pueden repetir mensajes antiguos
5. **Ofuscación del tráfico**: Los handshakes son indistinguibles de datos aleatorios

### Supuestos criptográficos

**Suposiciones de dificultad:**

1. **X25519 CDH**: El problema de Diffie-Hellman computacional es difícil en Curve25519
2. **ChaCha20 PRF**: ChaCha20 es una función pseudoaleatoria
3. **Poly1305 MAC**: Poly1305 es inforjable bajo ataque de mensaje elegido
4. **SHA-256 CR**: SHA-256 es resistente a colisiones
5. **HKDF Security**: HKDF extrae y expande claves distribuidas uniformemente

**Niveles de seguridad:**

- **X25519**: seguridad de ~128 bits (orden de la curva 2^252)
- **ChaCha20**: claves de 256 bits, seguridad de 256 bits
- **Poly1305**: seguridad de 128 bits (probabilidad de colisión)
- **SHA-256**: resistencia a colisiones de 128 bits, resistencia a preimagen de 256 bits

### Gestión de claves

**Generación de claves:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Almacenamiento de claves:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Rotación de claves:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Mitigaciones de ataques

### Mitigaciones contra ataques de repetición

**Validación de fecha y hora:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Filtro de Bloom para mensajes NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Uso único de Session Tag (etiquetas de sesión):**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Mitigaciones contra la suplantación por compromiso de clave (KCI)

**Problema**: La autenticación de los mensajes NS es vulnerable a KCI (suplantación por compromiso de clave) (Nivel de autenticación 1)

**Mitigación**:

1. Realiza la transición a NSR (Nivel 2 de autenticación) lo antes posible
2. No confíes en la carga útil de NS para operaciones críticas de seguridad
3. Espera la confirmación de NSR antes de realizar acciones irreversibles

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Medidas de mitigación contra la denegación de servicio

**Protección contra inundaciones de NS:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Límites de almacenamiento de etiquetas:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Gestión adaptativa de recursos:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Resistencia al análisis de tráfico

**Codificación Elligator2:**

Garantiza que los mensajes de negociación (handshake) sean indistinguibles de datos aleatorios:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Estrategias de relleno:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Ataques de temporización:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Escollos de implementación

**Errores comunes:**

1. **Reutilización de nonce** (número usado una vez): NUNCA reutilices pares (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# CORRECTO: Nonce (número único de uso) diferente para cada mensaje    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# MAL: Reutilizar una clave efímera    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # MAL

# CORRECTO: Clave nueva para cada mensaje    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# MAL: Generador de números aleatorios no criptográfico    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # INSEGURO

# BUENO: generador de números aleatorios criptográficamente seguro    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# MAL: Comparación con salida temprana    if computed_mac == received_mac:  # Fuga de temporización

       pass
   
# CORRECTO: Comparación en tiempo constante    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# MAL: Descifrar antes de verificar    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # DEMASIADO TARDE    if not mac_ok:

       return error
   
# CORRECTO: AEAD (cifrado autenticado con datos asociados) verifica antes de descifrar    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# MAL: Eliminación simple    del private_key  # Sigue en memoria

# CORRECTO: Sobrescribir antes de eliminar    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Casos de prueba críticos para la seguridad

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Solo ECIES (esquema integrado de cifrado en curvas elípticas) (recomendado para nuevos despliegues)

i2cp.leaseSetEncType=4

# Doble clave (ECIES + ElGamal por compatibilidad)

i2cp.leaseSetEncType=4,0

# Solo ElGamal (heredado, no recomendado)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# LS2 estándar (el más común)

i2cp.leaseSetType=3

# LS2 cifrado (destinos cegados)

i2cp.leaseSetType=5

# Meta LS2 (múltiples destinos)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Clave estática para ECIES (esquema de cifrado integrado de curva elíptica) (opcional, se genera automáticamente si no se especifica)

# Clave pública X25519 de 32 bytes, codificada en base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Tipo de firma (para LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES de router a router (Esquema de Cifrado Integrado de Curva Elíptica)

i2p.router.useECIES=true

```

**Build Properties:**

```java
// Para clientes I2CP (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[límites]

# Límite de memoria para sesiones ECIES (esquema de cifrado integrado de curva elíptica)

ecies.memory = 128M

[ecies]

# Habilitar ECIES (esquema de cifrado integrado de curva elíptica)

enabled = true

# Solo ECIES (esquema de cifrado integrado basado en curvas elípticas) o de doble clave

compatibility = true  # true = doble clave, false = solo ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Solo ECIES (Esquema Integrado de Cifrado de Curva Elíptica)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# Añadir ECIES manteniendo ElGamal

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Comprobar tipos de conexión

i2prouter.exe status

# o

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# Eliminar ElGamal

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# Reiniciar el router I2P o la aplicación

systemctl restart i2p

# o

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Volver a usar únicamente ElGamal si hay problemas

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Máximo de sesiones entrantes

i2p.router.maxInboundSessions=1000

# Número máximo de sesiones salientes

i2p.router.maxOutboundSessions=1000

# Tiempo de espera de la sesión (segundos)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Límite de almacenamiento de etiquetas (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Ventana de anticipación

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Mensajes antes del ratchet (mecanismo de avance criptográfico)

i2p.ecies.ratchetThreshold=4096

# Tiempo antes del ratchet (mecanismo de avance criptográfico) (segundos)

i2p.ecies.ratchetTimeout=600  # 10 minutos

```

### Monitoring and Debugging

**Logging:**

```properties
# Habilitar el registro de depuración de ECIES (esquema integrado de cifrado basado en curvas elípticas)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Ejemplos

print("NS (vinculado, carga útil de 1KB):", calculate_ns_size(1024, bound=True), "bytes")

# Salida: 1120 bytes

print("NSR (carga útil de 1KB):", calculate_nsr_size(1024), "bytes")

# Salida: 1096 bytes

print("ES (carga útil de 1KB):", calculate_es_size(1024), "bytes")

# Salida: 1048 bytes

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---