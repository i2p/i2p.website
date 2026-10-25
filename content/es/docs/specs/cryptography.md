---
title: "Especificación de Criptografía de Bajo Nivel"
description: "Detalles de bajo nivel de los algoritmos criptográficos utilizados en I2P"
slug: "cryptography"
aliases:
  - "/es/how_cryptography"
  - "/es/how_cryptography/"
category: "Diseño"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Descripción general

> **Nota:** Este documento está mayormente obsoleto. Consulta los siguientes documentos para las especificaciones actuales: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Esta página especifica los detalles de bajo nivel de la criptografía en I2P.

Hay varios algoritmos criptográficos en uso dentro de I2P. En el diseño original de I2P, solo había uno de cada tipo: un algoritmo simétrico, un algoritmo asimétrico, un algoritmo de firma y un algoritmo de hash. No había provisión para agregar más algoritmos o migrar a otros con mayor seguridad.

En años recientes hemos añadido un marco de trabajo para soportar múltiples primitivas y combinaciones de manera compatible con versiones anteriores. Se definen numerosos algoritmos de firma, con longitudes variables de clave y firma, mediante "tipos de firma". Los esquemas de cifrado extremo a extremo, que utilizan una combinación de cifrado asimétrico y simétrico, y con longitudes variables de clave, se definen mediante "tipos de cifrado".

Varios protocolos y estructuras de datos en I2P incluyen campos para especificar el tipo de firma y/o el tipo de cifrado. Estos campos, junto con las definiciones de tipos, definen las longitudes de clave y firma y las primitivas criptográficas necesarias para utilizarlas. Las definiciones de los tipos de firma y cifrado están en la [especificación de Estructuras Comunes](/docs/specs/common-structures).

Los protocolos I2P originales NTCP, SSU y ElGamal/AES+SessionTags utilizan una combinación de cifrado asimétrico ElGamal y cifrado simétrico AES. Los protocolos más nuevos NTCP2 y ECIES-X25519-AEAD-Ratchet utilizan una combinación de intercambio de claves X25519 y cifrado simétrico ChaCha20/Poly1305.

- ECIES-X25519-AEAD-Ratchet ha reemplazado a ElGamal/AES+SessionTags.
- NTCP2 ha reemplazado a NTCP.
- SSU2 ha reemplazado a SSU.
- La creación de túneles X25519 ha reemplazado a la creación de túneles ElGamal.

## Cifrado Asimétrico

El algoritmo de cifrado asimétrico original en I2P es ElGamal. El algoritmo más nuevo, usado en varios lugares, es el intercambio de claves DH ECIES X25519.

Estamos en el proceso de migrar todo el uso de ElGamal a X25519.

NTCP (con ElGamal) fue migrado a NTCP2 (con X25519). ElGamal/AES+SessionTag está siendo migrado a ECIES-X25519-AEAD-Ratchet.

### X25519

Para los detalles del uso de X25519, consulte [NTCP2](/docs/specs/ntcp2) y [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal se utiliza en varios lugares en I2P:

- Para cifrar mensajes TunnelBuild de router a router
- Para cifrado extremo a extremo (destino a destino) como parte de ElGamal/AES+SessionTag usando la clave de cifrado en el LeaseSet
- Para cifrado de algunos almacenamientos y consultas de netDb enviados a routers floodfill como parte de ElGamal/AES+SessionTag (destino a router o router a router).

Utilizamos números primos comunes para el cifrado y descifrado ElGamal de 2048, según lo establecido por IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). Actualmente solo usamos ElGamal para cifrar el IV y la clave de sesión en un único bloque, seguido por la carga útil cifrada con AES usando esa clave e IV.

El ElGamal sin cifrar contiene:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
El H(data) es el SHA256 de los datos que están cifrados en el bloque ElGamal, y está precedido por un byte aleatorio distinto de cero. Este byte es realmente aleatorio a partir de la versión 0.9.28; antes de eso siempre era 0xFF. Posiblemente podría usarse para banderas en el futuro. Los datos cifrados en el bloque pueden tener hasta 222 bytes de longitud. Como los datos cifrados pueden contener un número considerable de ceros si el texto claro es menor a 222 bytes, se recomienda que las capas superiores rellenen el texto claro a 222 bytes con datos aleatorios. Longitud total: típicamente 255 bytes.

El ElGamal encriptado contiene:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Cada parte cifrada se antepone con ceros hasta alcanzar un tamaño de exactamente 257 bytes. Longitud total: 514 bytes. En uso típico, las capas superiores rellenan los datos de texto claro a 222 bytes, resultando en un bloque sin cifrar de 255 bytes. Esto se codifica como dos partes cifradas de 256 bytes, y hay un solo byte de relleno de ceros antes de cada parte en esta capa.

Consulta el código ElGamal [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

El primo compartido es el primo Oakley para claves de 2048 bits [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
o como un valor hexadecimal:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Usando 2 como generador.

#### Exponente Corto {#exponent}

Aunque el tamaño estándar del exponente es de 2048 bits (256 bytes) y el PrivateKey de I2P es de 256 bytes completos, en algunos casos utilizamos el tamaño de exponente corto de 226 bits (28.25 bytes). Esto debería ser seguro para usar con los números primos Oakley [vanOorschot1996] [BENCHMARKS].

Además, [Koshiba2004] aparentemente respalda esto, según este hilo de sci.crypt [SCI.CRYPT]. El resto de la PrivateKey se rellena con ceros.

Antes de la versión 0.9.8, todos los routers usaban el exponente corto. A partir de la versión 0.9.8, los routers x86 de 64 bits usan un exponente completo de 2048 bits. Todos los routers ahora usan el exponente completo excepto un pequeño número de routers en hardware muy lento, que continúan usando el exponente corto debido a preocupaciones sobre la carga del procesador. La transición a un exponente más largo para estas plataformas es un tema para estudio futuro.

#### Obsolescencia

Se debe estudiar la vulnerabilidad de la red a un ataque ElGamal y el impacto de la transición a una longitud de bits mayor. Puede ser bastante difícil hacer cualquier cambio compatible con versiones anteriores.

## Cifrado Simétrico

El algoritmo de cifrado simétrico original en I2P es AES. El algoritmo más reciente, utilizado en varios lugares, es Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Estamos en proceso de migrar todo el uso de AES a ChaCha20/Poly1305.

NTCP (con AES) fue migrado a NTCP2 (con ChaCha20/Poly1305). ElGamal/AES+SessionTag está siendo migrado a ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

Para los detalles del uso de ChaCha20/Poly1305 consulta [NTCP2](/docs/specs/ntcp2) y [ECIES](/docs/specs/ecies).

### AES

AES se utiliza para cifrado simétrico, en varios casos:

- Para el cifrado de transporte SSU (ver sección "Transportes") después del intercambio de claves DH
- Para cifrado extremo a extremo (destino a destino) como parte de ElGamal/AES+SessionTag
- Para el cifrado de algunos almacenamientos y consultas de netDb enviados a routers floodfill como parte de ElGamal/AES+SessionTag (destino a router o router a router).
- Para el cifrado de mensajes de prueba de tunnel periódicos enviados desde el router hacia sí mismo, a través de sus propios tunnels.

Utilizamos AES con claves de 256 bits y bloques de 128 bits en modo CBC. El relleno utilizado está especificado en IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, sección 8.1 (para tipo de bloque 02)). En este caso, el relleno consiste en octetos generados pseudoaleatoriamente para coincidir con bloques de 16 bytes. Específicamente, consulte el código CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) y la implementación Cryptix AES [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), así como el relleno, encontrado en la función ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Obsolescencia

Se debe estudiar la vulnerabilidad de la red a un ataque AES y el impacto de la transición a una longitud de bits mayor. Puede ser muy difícil hacer que cualquier cambio sea compatible hacia atrás.

## Firmas {#sig}

Se definen numerosos algoritmos de firma, con longitudes de clave y firma variables, según los tipos de firma. Es relativamente fácil agregar más tipos de firma.

EdDSA-SHA512-Ed25519 es el algoritmo de firma predeterminado actual. DSA, que era el algoritmo original antes de que añadiéramos soporte para tipos de firma, aún está en uso en la red.

### DSA

Las firmas se generan y verifican con [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) de 1024 bits (L=1024, N=160), tal como se implementa en [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). Se eligió DSA porque es mucho más rápido para firmas que ElGamal.

#### SEMILLA

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Contador

```
33
```
#### Primo DSA (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### Cociente DSA (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### Generador DSA (g)

1024 bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
La SigningPublicKey es de 1024 bits. La SigningPrivateKey es de 160 bits.

#### Obsolescencia

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) recomienda un mínimo de (L=2048, N=224) para uso posterior a 2010. Esto puede mitigarse en cierta medida mediante el "período criptográfico", o tiempo de vida de una clave determinada.

El número primo fue elegido en 2003, y la persona que eligió el número (TheCrypto) ya no es desarrollador de I2P actualmente. Por tanto, no sabemos si el primo elegido es un 'primo fuerte'. Si se elige un primo más grande para propósitos futuros, este debería ser un primo fuerte, y documentaremos el proceso de construcción.

## Nuevos Algoritmos de Firma

A partir del lanzamiento 0.9.12, el router admite algoritmos de firma adicionales que son más seguros que DSA de 1024 bits. El primer uso fue para Destinations; el soporte para Router Identities se agregó en el lanzamiento 0.9.16. Los Destinations existentes no se pueden migrar de firmas antiguas a nuevas; sin embargo, existe soporte para un solo tunnel con múltiples Destinations, y esto proporciona una forma de cambiar a tipos de firma más nuevos. El tipo de firma está codificado en el Destination y Router Identity, de modo que se pueden agregar nuevos algoritmos de firma o curvas en cualquier momento.

Los tipos de firma soportados actualmente son los siguientes:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (no ampliamente utilizado)
- ECDSA-SHA512-P521 (no ampliamente utilizado)
- EdDSA-SHA512-Ed25519 (predeterminado desde la versión 0.9.15)
- RedDSA-SHA512-Ed25519 (desde la versión 0.9.39)

Los tipos de firma adicionales se utilizan únicamente en la capa de aplicación, principalmente para firmar y verificar archivos su3. Estos tipos de firma son los siguientes:

- RSA-SHA256-2048 (no ampliamente usado)
- RSA-SHA384-3072 (no ampliamente usado)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (a partir de la versión 0.9.25; no ampliamente usado)

### ECDSA

ECDSA utiliza las curvas estándar NIST y los hashes SHA-2 estándar.

Migramos los nuevos destinos a ECDSA-SHA256-P256 en el marco temporal de las versiones 0.9.16 - 0.9.19. El uso para Router Identities está soportado desde la versión 0.9.16 y la migración de routers existentes ocurrió en 2015.

### RSA

RSA estándar PKCS#1 v1.5 (RFC 2313) con el exponente público F4 = 65537.

RSA ahora se utiliza para firmar todo el contenido confiable fuera de banda, incluyendo actualizaciones de router, reseeding, plugins y noticias. Las firmas están incrustadas en el formato "su3" [UPDATES]. Se recomiendan y utilizan claves de 4096 bits por todos los firmantes conocidos. RSA no se utiliza, ni está planeado para uso, en ningún Destination en la red o Router Identities.

### EdDSA 25519

EdDSA estándar usando curva 25519 y hashes SHA-2 estándar de 512 bits.

Soportado desde la versión 0.9.15.

Los destinos e identidades del router se migraron a finales de 2015.

### RedDSA 25519

EdDSA estándar usando curva 25519 y hashes SHA-2 estándar de 512 bits, pero con claves privadas diferentes y modificaciones menores en la firma. Para leasesets cifrados. Consulta [EncryptedLeaseSet](/docs/specs/encryptedleaseset) y [Red25519](/docs/specs/red25519) para más detalles.

Compatible desde la versión 0.9.39.

## Hashes

Los hashes se utilizan en algoritmos de firma y como claves en la DHT de la red.

Los algoritmos de firma más antiguos usan SHA1 y SHA256. Los algoritmos de firma más nuevos usan SHA512. El DHT usa SHA256.

### SHA256

Los hashes DHT dentro de I2P son SHA256 estándar.

#### Obsolescencia

Se debe estudiar la vulnerabilidad de la red a un ataque SHA-256 y el impacto de la transición a un hash más largo. Puede ser bastante difícil hacer que cualquier cambio sea compatible con versiones anteriores.

## Transportes

En la capa de protocolo más baja, la comunicación punto a punto entre routers está protegida por la seguridad de la capa de transporte.

Las conexiones NTCP2 utilizan X25519 Diffie-Hellman y cifrado autenticado ChaCha20/Poly1305.

Los transportes SSU y el obsoleto NTCP utilizan un intercambio de claves Diffie-Hellman de 256 bytes (2048 bits) usando el mismo primo compartido y generador especificado anteriormente para ElGamal, seguido de cifrado simétrico AES como se describe anteriormente.

Está planeado migrar SSU a SSU2 (con X25519 y ChaCha20/Poly1305).

Todos los transportes proporcionan secreto perfecto hacia adelante [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) en los enlaces de transporte.

### Conexiones NTCP2 {#tcp}

Las conexiones NTCP2 utilizan X25519 Diffie-Hellman y cifrado autenticado ChaCha20/Poly1305, y el marco de protocolo Noise [Noise](https://noiseprotocol.org/noise.html).

Consulta la especificación NTCP2 [NTCP2](/docs/specs/ntcp2) para detalles y referencias.

### Conexiones UDP {#udp}

SSU (el transporte UDP) cifra cada paquete con AES256/CBC con tanto un IV explícito como MAC (HMAC-MD5-128) después de acordar una clave de sesión efímera a través de un intercambio Diffie-Hellman de 2048 bits, autenticación station-to-station con la clave DSA del otro router, además cada mensaje de red tiene su propio hash para verificación de integridad local.

Consulta la especificación SSU para más detalles.

ADVERTENCIA - El HMAC-MD5-128 de I2P usado en SSU aparentemente no es estándar. Al parecer, una versión temprana de SSU usaba HMAC-SHA256, y luego se cambió a MD5-128 por razones de rendimiento, pero se dejó intacto el tamaño del búfer de 32 bytes. Consulta HMACGenerator.java y las notas de estado del 2005-07-05 para más detalles.

### Conexiones NTCP

NTCP ya no se utiliza, fue reemplazado por NTCP2.

Las conexiones NTCP se negociaron con una implementación Diffie-Hellman de 2048, utilizando la identidad del router para proceder con un acuerdo estación a estación, seguido de algunos campos específicos del protocolo cifrados, con todos los datos posteriores cifrados con AES (como se mencionó anteriormente). La razón principal para realizar la negociación DH en lugar de usar ElGamalAES+SessionTag es que proporciona 'secreto perfecto hacia adelante' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy), mientras que ElGamalAES+SessionTag no lo hace.

## Referencias

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Benchmarks de Crypto++, originalmente en http://www.eskimo.com/~weidai/benchmarks.html (ahora caído), rescatado de http://www.archive.org/, con fecha del 23 de abril de 2008.
- [Common](/docs/specs/common-structures) - Especificación de Estructuras Comunes
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
