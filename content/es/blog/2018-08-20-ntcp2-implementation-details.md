---
title: "Detalles de implementación de NTCP2"
date: 2018-08-20
author: "villain"
description: "I2P's new transport protocol implementation details and technical specifications"
categories: ["development"]
---

Los protocolos de transporte de I2P se desarrollaron originalmente hace unos 15 años. En aquel entonces, el objetivo principal era ocultar los datos transferidos, no ocultar el hecho de que se estaba utilizando el propio protocolo. Nadie pensaba seriamente en protegerse contra la inspección profunda de paquetes (DPI) y la censura de protocolos. Los tiempos cambian y, aunque los protocolos de transporte originales siguen proporcionando una seguridad sólida, surgió la demanda de un nuevo protocolo de transporte. NTCP2 está diseñado para resistir las amenazas de censura actuales. Principalmente, el análisis mediante DPI de la longitud de los paquetes. Además, el nuevo protocolo utiliza los avances más modernos en criptografía. NTCP2 se basa en el [Noise Protocol Framework](https://noiseprotocol.org/noise.html), con SHA256 como función hash y x25519 como intercambio de claves Diffie-Hellman (DH) de curva elíptica.

La especificación completa del protocolo NTCP2 puede encontrarse [aquí](/docs/specs/ntcp2/).

## Nueva criptografía

NTCP2 requiere añadir los siguientes algoritmos criptográficos a una implementación de I2P:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

En comparación con nuestro protocolo original, NTCP, NTCP2 utiliza x25519 en lugar de ElGamal para la función DH, AEAD/Chaha20/Poly1305 en lugar de AES-256-CBC/Adler32, y utiliza SipHash para ofuscar la información de la longitud del paquete. La función de derivación de claves utilizada en NTCP2 es más compleja, ahora utiliza muchas llamadas a HMAC-SHA256.

*Nota de implementación de i2pd (C++): Todos los algoritmos mencionados arriba, excepto SipHash, están implementados en OpenSSL 1.1.0. SipHash se añadirá al próximo lanzamiento de OpenSSL 1.1.1. Para compatibilidad con OpenSSL 1.0.2, que se usa en la mayoría de los sistemas actuales, el desarrollador principal de i2pd [Jeff Becker](https://github.com/majestrate) ha contribuido implementaciones independientes de los algoritmos criptográficos que faltan.*

## Cambios en RouterInfo

NTCP2 requiere disponer de una tercera clave (x25519) además de las dos existentes (las claves de cifrado y de firma). Se denomina clave estática y debe añadirse a cualquiera de las direcciones de RouterInfo como un parámetro "s". Es necesaria tanto para el iniciador de NTCP2 (Alice) como para el respondedor (Bob). Si más de una dirección admite NTCP2, por ejemplo, IPv4 e IPv6, se requiere que "s" sea la misma para todas ellas. Se permite que la dirección de Alice tenga únicamente el parámetro "s" sin "host" ni "port" definidos. Además, se requiere un parámetro "v", que actualmente siempre se establece en "2".

La dirección NTCP2 puede declararse como una dirección NTCP2 separada o como una dirección NTCP de estilo antiguo con parámetros adicionales; en ese caso aceptará conexiones tanto NTCP como NTCP2. La implementación de Java de I2P usa el segundo enfoque; i2pd (implementación en C++) usa el primero.

Si un nodo acepta conexiones NTCP2, debe publicar su RouterInfo con el parámetro "i", que se utiliza como vector de inicialización (IV) para la clave pública de cifrado cuando ese nodo establece nuevas conexiones.

## Estableciendo una conexión

Para establecer una conexión, ambas partes necesitan generar pares de claves efímeras x25519. Con base en esas claves y en las claves "estáticas", derivan un conjunto de claves para la transferencia de datos. Ambas partes deben verificar que la otra parte efectivamente tenga una clave privada para esa clave estática y que esa clave estática sea la misma que en RouterInfo.

Se envían tres mensajes para establecer una conexión:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Se calcula una clave x25519 compartida, denominada «input key material», para cada mensaje; después, la clave de cifrado del mensaje se genera con una función MixKey. Se mantiene un valor ck (chaining key) mientras se intercambian mensajes. Ese valor se utiliza como entrada final al generar las claves para la transferencia de datos.

La función MixKey tiene un aspecto similar a lo siguiente en la implementación de I2P en C++:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
El mensaje **SessionRequest** se compone de una clave pública x25519 de Alice (32 bytes), un bloque de datos cifrado con AEAD/Chacha20/Poly1305 (16 bytes), un hash (16 bytes) y algunos datos aleatorios al final (relleno). La longitud del relleno se define en el bloque de datos cifrado. El bloque cifrado también contiene la longitud de la segunda parte del mensaje **SessionConfirmed**. Un bloque de datos se cifra y se firma con una clave derivada de la clave efímera de Alice y la clave estática de Bob. El valor inicial de ck para la función MixKey se establece en SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Como los 32 bytes de la clave pública x25519 pueden ser detectados por DPI, se cifran con el algoritmo AES-256-CBC usando el hash de la dirección de Bob como clave y el parámetro "i" de RouterInfo como vector de inicialización (IV).

El mensaje **SessionCreated** tiene la misma estructura que **SessionRequest**, excepto que la clave se calcula en función de las claves efímeras de ambas partes. El IV (vector de inicialización) generado después de cifrar/descifrar la clave pública del mensaje **SessionRequest** se utiliza como IV para cifrar/descifrar la clave pública efímera.

El mensaje **SessionConfirmed** tiene 2 partes: clave pública estática y el RouterInfo de Alice. La diferencia respecto de los mensajes anteriores es que la clave pública efímera se cifra con AEAD/Chaha20/Poly1305 usando la misma clave que **SessionCreated**. Esto hace que la primera parte del mensaje aumente de 32 a 48 bytes. La segunda parte también se cifra con AEAD/Chaha20/Poly1305, pero usando una nueva clave, calculada a partir de la clave efímera de Bob y la clave estática de Alice. La parte de RouterInfo también puede completarse con relleno de datos aleatorios, pero no es obligatorio, ya que RouterInfo suele tener longitud variable.

## Generación de claves de transferencia de datos

Si todas las verificaciones de hash y de claves han tenido éxito, debe estar presente un valor ck común después de la última operación MixKey en ambos lados. Este valor se utiliza para generar dos conjuntos de claves <k, sipk, sipiv>, uno para cada lado de una conexión. "k" es una clave AEAD/Chaha20/Poly1305, "sipk" es una clave SipHash, "sipiv" es un valor inicial para el IV de SipHash, que se cambia después de cada uso.

El código utilizado para generar claves se ve así en la implementación de I2P en C++:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*Nota de implementación de i2pd (C++): Los primeros 16 bytes del arreglo "sipkeys" constituyen una clave de SipHash; los últimos 8 bytes son IV (vector de inicialización). SipHash requiere dos claves de 8 bytes, pero i2pd las trata como una única clave de 16 bytes.*

## Transferencia de datos

Los datos se transfieren en tramas, cada trama tiene 3 partes:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

La longitud máxima de los datos transferidos en una trama es de 65519 bytes.

La longitud del mensaje se ofusca aplicando la función XOR con los dos primeros bytes del IV (vector de inicialización) actual de SipHash.

La parte de datos cifrada contiene bloques de datos. Cada bloque está precedido por un encabezado de 3 bytes, que define el tipo y la longitud del bloque. Generalmente se transfieren bloques de tipo I2NP, que son mensajes I2NP con un encabezado modificado. Una trama NTCP2 puede transferir varios bloques I2NP.

El otro tipo importante de bloque de datos es un bloque de datos aleatorio. Se recomienda añadir un bloque de datos aleatorio en cada trama NTCP2. Solo se puede añadir un único bloque de datos aleatorio y debe ser el último bloque.

Estos son otros bloques de datos utilizados en la implementación actual de NTCP2:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Resumen


El nuevo protocolo de transporte de I2P, NTCP2, proporciona una resistencia eficaz frente a la censura por DPI (inspección profunda de paquetes). También se traduce en una menor carga de CPU debido a la criptografía moderna y más rápida que utiliza. Facilita que I2P funcione en dispositivos de gama baja, como teléfonos inteligentes y routers domésticos. Ambas implementaciones principales de I2P tienen compatibilidad total con NTCP2 y lo ponen a disposición para su uso a partir de la versión 0.9.36 (Java) y 2.20 (i2pd, C++).
