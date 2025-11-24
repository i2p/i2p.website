---
title: "Protocolos de Criptografía Post-Cuántica"
number: "169"
author: "zzz, original, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Abierto"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Visión general

Mientras que la investigación y la competencia para encontrar criptografía post-cuántica (PQ) adecuada han avanzado durante una década, las opciones no se han aclarado hasta hace poco.

Comenzamos a analizar las implicaciones de la criptografía PQ en 2022 [FORO]_.

Los estándares de TLS agregaron soporte para encriptación híbrida en los últimos dos años y ahora se usa para una parte significativa del tráfico cifrado en internet debido al soporte en Chrome y Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST finalizó y publicó recientemente los algoritmos recomendados para la criptografía post-cuántica [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Varias bibliotecas comunes de criptografía ahora soportan los estándares NIST o lanzarán soporte en el futuro cercano.

Tanto [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) como [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomiendan que la migración comience de inmediato. Consulte también las preguntas frecuentes de la NSA sobre PQ de 2022 [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P debería ser un líder en seguridad y criptografía. Ahora es el momento de implementar los algoritmos recomendados. Usando nuestro sistema flexible de tipos de criptografía y firmas, agregaremos tipos para criptografía híbrida y para firmas PQ e híbridas.


## Metas

- Seleccionar algoritmos resistentes a PQ
- Agregar algoritmos solo PQ e híbridos a los protocolos I2P donde sea apropiado
- Definir múltiples variantes
- Seleccionar las mejores variantes después de la implementación, pruebas, análisis e investigación
- Agregar soporte de manera incremental y con compatibilidad hacia atrás


## No metas

- No cambiar los protocolos de encriptación unidireccional (Noise N)
- No alejarse de SHA256, no amenazado a corto plazo por PQ
- No seleccionar las variantes finales preferidas en este momento


## Modelo de amenaza

- Routers en el OBEP o IBGW, posiblemente coludidos, almacenando mensajes de ajo para su posterior descifrado (secreto hacia adelante)
- Observadores de red almacenando mensajes de transporte para su posterior descifrado (secreto hacia adelante)
- Participantes de red falsificando firmas para RI, LS, streaming, datagramas, u otras estructuras


## Protocolos afectados

Modificaremos los siguientes protocolos, aproximadamente en orden de desarrollo. El despliegue general probablemente será desde finales de 2025 hasta mediados de 2027. Consulte la sección de Prioridades y Despliegue a continuación para más detalles.


| Protocolo / Función | Estado |
| ------------------- | ------ |
| Ratchet y LS híbrido MLKEM | Aproba |
| NTCP2 híbrido MLKEM | Alguno |
| SSU2 híbrido MLKEM | Alguno |
| Tipos de firmas MLDSA 12-14 | La pro |
| Destinos MLDSA | Probad |
| Tipos de firmas híbridos 15-17 | Prelim |
| Destinos híbridos |  |


## Diseño

Soportaremos los estándares NIST FIPS 203 y 204 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 
que se basan en, pero NO son compatibles con, 
CRYSTALS-Kyber y CRYSTALS-Dilithium (versiones 3.1, 3 y anteriores).

### Intercambio de claves

Soportaremos el intercambio de claves híbrido en los siguientes protocolos:

| Proto | Tipo Noise | ¿Soporta solo PQ | ¿Soporta Híbri |
| ----- | ---------- | ---------------- | -------------- |
| NTCP2 | XK | no | sí |
| SSU2 | XK | no | sí |
| Ratchet | IK | no | sí |
| TBM | N | no | no |
| NetDB | N | no | no |


KEM PQ proporciona solo claves efímeras y no soporta directamente intercambios de claves estáticas como Noise XK e IK.

Noise N no utiliza un intercambio de claves bidireccional, por lo que no es adecuado para encriptación híbrida.

Por lo tanto, solo soportaremos encriptación híbrida para NTCP2, SSU2 y Ratchet. Definiremos las tres variantes ML-KEM como en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para un total de 3 nuevos tipos de encriptación. Los tipos híbridos solo se definirán en combinación con X25519.

Los nuevos tipos de encriptación son:

| Tipo | Códi |
| ---- | ---- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


La sobrecarga será sustancial. Los tamaños típicos de mensaje 1 y 2 (para XK e IK) están actualmente alrededor de 100 bytes (antes de cualquier carga adicional). Esto aumentará de 8x a 15x dependiendo del algoritmo.

### Firmas

Soportaremos firmas PQ e híbridas en las siguientes estructuras:

| Tipo | ¿Soporta solo PQ | ¿Soporta Híbri |
| ---- | ---------------- | -------------- |
| RouterInfo | sí | sí |
| LeaseSet | sí | sí |
| Streaming SYN/SYNACK/Close | sí | sí |
| Datagramas replicables | sí | sí |
| Datagram2 (prop. 163) | sí | sí |
| Mensaje de creación de ses | n I2CP  sí | sí |
| Archivos SU3 | sí | sí |
| Certificados X.509 | sí | sí |
| Almacenes de claves Java | sí | sí |


Por lo tanto, soportaremos tanto firmas solo PQ como híbridas. Definiremos las tres variantes ML-DSA como en [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), tres variantes híbridas con Ed25519, y tres variantes solo PQ con prehash solo para archivos SU3, para un total de 9 nuevos tipos de firmas. Los tipos híbridos solo se definirán en combinación con Ed25519. Usaremos el estándar ML-DSA, NO las variantes de prehash (HashML-DSA), excepto para archivos SU3.

Usaremos la variante de firma "reforzada" o aleatorizada, no la variante "determinística", como se define en [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sección 3.4. Esto asegura que cada firma sea diferente, incluso sobre los mismos datos, y proporciona protección adicional contra ataques de canal lateral. Vea la sección de notas de implementación a continuación para detalles adicionales sobre elecciones de algoritmos, incluyendo codificación y contexto.

Los nuevos tipos de firmas son:

| Tipo | Códi |
| ---- | ---- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


Los certificados X.509 y otras codificaciones DER usarán las estructuras compuestas y OIDs definidas en [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).

La sobrecarga será sustancial. Los tamaños típicos de destino e identidad del router de Ed25519 son 391 bytes. Estos aumentarán en 3.5x a 6.8x dependiendo del algoritmo. Las firmas Ed25519 son de 64 bytes. Estas aumentarán en 38x a 76x dependiendo del algoritmo. Los mensajes RouterInfo, LeaseSet, datagramas replicables y mensajes de streaming firmados típicos son de aproximadamente 1KB. Estos aumentarán en 3x a 8x dependiendo del algoritmo.

Como los nuevos tipos de destino e identidad del router no contendrán relleno, no serán comprimibles. Los tamaños de destinos e identidades del router que son comprimidos en tránsito aumentarán en 12x - 38x dependiendo del algoritmo.

### Combinaciones Legales

Para Destinations, los nuevos tipos de firmas son compatibles con todos los tipos de encriptación en el leaseset. Establezca el tipo de encriptación en el certificado de clave en NINGUNO (255).

Para RouterIdentities, el tipo de encriptación ElGamal está en desuso. Los nuevos tipos de firmas son compatibles solo con la encriptación X25519 (tipo 4). Los nuevos tipos de encriptación se indicarán en las RouterAddresses. El tipo de encriptación en el certificado de clave seguirá siendo tipo 4.

### Nueva Criptografía Requerida

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS202]_ Usado solo para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS202]_
- SHAKE128 y SHAKE256 (extensiones XOF a SHA3-128 y SHA3-256) [FIPS202]_

Vectores de prueba para SHA3-256, SHAKE128 y SHAKE256 están en [NIST-VECTORS]_.

Tenga en cuenta que la biblioteca Java bouncycastle soporta todo lo anterior. El soporte de la biblioteca C++ está en OpenSSL 3.5 [OPENSSL]_.

### Alternativas

No soportaremos [FIPS205]_ (Sphincs+), es mucho más lento y grande que ML-DSA. No soportaremos el próximo FIPS206 (Falcon), aún no está estandarizado. No soportaremos NTRU u otros candidatos PQ que no fueron estandarizados por NIST.

Rosenpass
`````````

Hay alguna investigación [PQ-WIREGUARD]_ sobre la adaptación de Wireguard (IK) para criptografía pura PQ, pero hay varias preguntas abiertas en ese documento. Más tarde, este enfoque fue implementado como Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_ para PQ Wireguard.

Rosenpass utiliza un apretón de manos similar a Noise KK con claves estáticas de Classic McEliece 460896 preshared (500 KB cada una) y claves efímeras Kyber-512 (esencialmente MLKEM-512). Dado que los cifrados de texto de McEliece clásico son solo de 188 bytes, y las claves públicas y cifrados de texto Kyber-512 son razonables, ambos mensajes de apretón de manos caben en un MTU UDP estándar. La clave compartida de salida (osk) del apretón de manos PQ KK se usa como la clave preshared de entrada (psk) para el apretón de manos estándar de Wireguard IK. Así que hay dos apretones de manos completos en total, uno puro PQ y uno puro X25519.

No podemos hacer nada de esto para reemplazar nuestros apretones de manos XK e IK porque:

- No podemos hacer KK, Bob no tiene la clave estática de Alice.
- Claves estáticas de 500KB son demasiado grandes.
- No queremos un viaje de ida y vuelta extra.

Hay mucha información buena en el documento técnico, y lo revisaremos en busca de ideas e inspiración. TODO.

## Especificación

### Estructuras comunes

Actualice las secciones y tablas del documento de estructuras comunes [COMMON] como sigue:

Clave Pública
````````````````

Los nuevos tipos de Clave Pública son:

| Tipo | Longitud de Clave | Públic | Desde |
| ---- | ----------------- | ------ | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM512 | 800 | 0.9.xx | Ver p |
| MLKEM768 | 1184 | 0.9.xx | Ver p |
| MLKEM1024 | 1568 | 0.9.xx | Ver p |
| MLKEM512_CT | 768 | 0.9.xx | Ver p |
| MLKEM768_CT | 1088 | 0.9.xx | Ver p |
| MLKEM1024_CT | 1568 | 0.9.xx | Ver p |
| NINGUNO | 0 | .9.xx | er pr |


Las claves públicas híbridas son la clave X25519.
Las claves públicas de KEM son la clave PQ efímera enviada de Alice a Bob.
La codificación y el orden de los bytes están definidos en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Las claves MLKEM*_CT no son realmente claves públicas, son el "cifrado de texto" enviado de Bob a Alice en el apretón de manos de Noise.
Se enumeran aquí para completar.


Clave Privada
````````````````

Los nuevos tipos de Clave Privada son:

| Tipo | Longitud de Clave | rivada | esde |
| ---- | ----------------- | ------ | ---- |
| MLKEM512_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver p |
| MLKEM512 | 1632 | 0.9.xx | Ver p |
| MLKEM768 | 2400 | 0.9.xx | Ver p |
| MLKEM1024 | 3168 | 0.9.xx | Ver p |


Las claves privadas híbridas son las claves X25519.
Las claves privadas de KEM son solo para Alice.
La codificación y el orden de los bytes de KEM están definidos en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).


Clave Pública de Firma
````````````````

Los nuevos tipos de Clave Pública de Firma son:

| Tipo | Longitud (byte | Desde | Uso |
| ---- | -------------- | ----- | --- |
| MLDSA44 | 1312 | 0.9.xx | Ver p |
| MLDSA65 | 1952 | 0.9.xx | Ver p |
| MLDSA87 | 2592 | 0.9.xx | Ver p |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Ver p |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Ver p |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Ver p |
| MLDSA44ph | 1344 | 0.9.xx | Solo |
| MLDSA65ph | 1984 | 0.9.xx | Solo |
| MLDSA87ph | 2624 | 0.9.xx | Solo |


Las claves públicas de firma híbridas son la clave Ed25519 seguida de la clave PQ, según [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
La codificación y el orden de bytes están definidos en [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

Clave Privada de Firma
`````````````````

Los nuevos tipos de Clave Privada de Firma son:

| Tipo | Longitud (byte | Desde | Uso |
| ---- | -------------- | ----- | --- |
| MLDSA44 | 2560 | 0.9.xx | Ver p |
| MLDSA65 | 4032 | 0.9.xx | Ver p |
| MLDSA87 | 4896 | 0.9.xx | Ver p |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Ver p |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Ver p |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Ver p |
| MLDSA44ph | 2592 | 0.9.xx | Solo |
| MLDSA65ph | 4064 | 0.9.xx | Solo |
| MLDSA87ph | 4928 | 0.9.xx | Solo |


Las claves privadas de firma híbridas son la clave Ed25519 seguida de la clave PQ, según [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
La codificación y el orden de bytes están definidos en [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

Firma
````````

Los nuevos tipos de Firmas son:

| Tipo | Longitud (byte | Desde | Uso |
| ---- | -------------- | ----- | --- |
| MLDSA44 | 2420 | 0.9.xx | Ver p |
| MLDSA65 | 3309 | 0.9.xx | Ver p |
| MLDSA87 | 4627 | 0.9.xx | Ver p |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Ver p |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Ver p |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Ver p |
| MLDSA44ph | 2484 | 0.9.xx | Solo |
| MLDSA65ph | 3373 | 0.9.xx | Solo |
| MLDSA87ph | 4691 | 0.9.xx | Solo |


Las firmas híbridas son la firma Ed25519 seguida de la firma PQ, según [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/). Las firmas híbridas se verifican verificando ambas firmas, y fallando si cualquiera de ellas falla. La codificación y el orden de los bytes están definidos en [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).


Certificados de Claves
````````````````

Los nuevos tipos de Clave Pública de Firma son:

| Tipo | Código de T | o  Longitud Total de Cl | e Públ | a  De |
| ---- | ----------- | ----------------------- | ------ | ----- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Ver p |
| MLDSA65 | 13 | 1952 | 0.9.xx | Ver p |
| MLDSA87 | 14 | 2592 | 0.9.xx | Ver p |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Ver p |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Ver p |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Ver p |
| MLDSA44ph | 18 | n/a | 0.9.xx | Solo |
| MLDSA65ph | 19 | n/a | 0.9.xx | Solo |
| MLDSA87ph | 20 | n/a | 0.9.xx | Solo |


Los nuevos tipos de Clave Pública Cripto son:

| Tipo | Código de T | o  Longitud Total de Cl | ve Púb | ca De |
| ---- | ----------- | ----------------------- | ------ | ----- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Ver p |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Ver p |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Ver p |
| NINGUNO | 255 | 0 | 0.9.x | Ver |


Los tipos de claves híbridas NUNCA se incluyen en certificados de claves; solo en leasesets.

Para destinos con tipos de firmas Híbridos o PQ, use NONE (tipo 255) para el tipo de encriptación, pero no hay clave criptográfica, y toda la sección principal de 384 bytes es para la clave de firma.

Tamaños de Destinos
``````````````````

Aquí están las longitudes para los nuevos tipos de Destinos. El tipo de encriptación para todos es NONE (tipo 255) y la longitud de la clave de encriptación se trata como 0. Toda la sección de 384 bytes se utiliza para la primera parte de la clave pública de firma. NOTA: Esto es diferente del especificado para los tipos de firmas ECDSA_SHA512_P521 y RSA, donde mantenemos la clave de ElGamal de 256 bytes en el destino aunque no se use. Sin relleno. La longitud total es 7 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud de clave excesiva.

Ejemplo de secuencia de bytes de destino de 1319-byte para MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Tipo | Código de T | o  Longitud Total de Cl | e Públ | a  Pri | ipal |
| ---- | ----------- | ----------------------- | ------ | ------ | ---- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |


Tamaños de RouterIdent
``````````````````

Aquí están las longitudes para los nuevos tipos de Destinos. El tipo de encriptación para todos es X25519 (tipo 4). Toda la sección de 352 bytes después de la clave pública X25519 se usa para la primera parte de la clave pública de firma. Sin relleno. La longitud total es 39 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud de clave excesiva.

Ejemplo de secuencia de bytes de identidad de router de 1351-byte para MLDSA44:
enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Tipo | Código de T | o  Longitud Total de Cl | e Públ | a  Pri | ipal |
| ---- | ----------- | ----------------------- | ------ | ------ | ---- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |


### Patrones de Apretons de Manos

Los apretones de manos utilizan patrones de apretón de manos [Noise]_.

La siguiente mapeo de letras es utilizado:

- e = clave efímera de una sola vez
- s = clave estática
- p = carga del mensaje
- e1 = clave efímera PQ, enviada de Alice a Bob
- ekem1 = el cifrado de texto KEM, enviado de Bob a Alice

Las siguientes modificaciones a XK e IK para el secreto hacia adelante híbrido (hfs) se
especifican en [Noise-Hybrid]_ sección 5:

```dataspec

XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 y ekem1 son cifrados. Ver definiciones de patrón a continuación.
  NOTA: e1 y ekem1 son de diferentes tamaños (a diferencia de X25519)

```

El patrón e1 se define como sigue, según especificado en Noise-Hybrid]_ sección 4:

```dataspec

Para Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  Para Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)


```


El patrón de ekem1 se define como sigue, según especificado en Noise-Hybrid]_ sección 4:

```dataspec

Para Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  Para Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)


```

### Derivación de Claves para Apretones de Manos de Ruido

Problemas
``````

- ¿Deberíamos cambiar la función hash del apretón de manos? Verificar [Choosing-Hash]_.
  SHA256 no es vulnerable a PQ, pero si queremos actualizar
  nuestra función hash, ahora es el momento, mientras estamos cambiando otras cosas.
  La propuesta actual de SSH de IETF [SSH-HYBRID]_ es usar MLKEM768
  con SHA256 y MLKEM1024 con SHA384. Esa propuesta incluye
  una discusión de las consideraciones de seguridad.
- ¿Deberíamos dejar de enviar datos de rosetón con 0-RTT (aparte del LS)?
- ¿Deberíamos cambiar el rosetón de IK a XK si no enviamos datos de 0-RTT?


Visión general
````````

Esta sección se aplica a los protocolos IK y XK.

El apretón de manos híbrido está definido en [Noise-Hybrid]_.
El primer mensaje, de Alice a Bob, contiene e1, la clave de encapsulado, antes de la carga útil del mensaje.
Esto se trata como una clave estática adicional; llame a EncryptAndHash() en ella (como Alice)
o DecryptAndHash() (como Bob).
Luego procese la carga útil del mensaje como de costumbre.

El segundo mensaje, de Bob a Alice, contiene ekem1, el cifrado, antes de la carga útil del mensaje.
Esto se trata como una clave estática adicional; llame a EncryptAndHash() en ella (como Bob)
o DecryptAndHash() (como Alice).
Luego, calcule la kem_shared_key y llame a MixKey(kem_shared_key).
Luego procese la carga útil del mensaje como de costumbre.

### Operaciones Definidas para ML-KEM

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos usados como se define en [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()
    Alice crea las claves de encapsulación y desencapsulación.
    La clave de encapsulación se envía en el mensaje 1.
    Los tamaños de encap_key y decap_key varían según la variante de ML-KEM.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob calcula el cifrado de texto y la clave compartida,
    usando el cifrado de texto recibido en el mensaje 1.
    El cifrado de texto se envía en el mensaje 2.
    El tamaño del cifrado de texto varía según la variante de ML-KEM.
    La kem_shared_key siempre es de 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice calcula la clave compartida,
    usando el cifrado recibido en el mensaje 2.
    La kem_shared_key siempre es de 32 bytes.

Tenga en cuenta que tanto la encap_key como el ciphertext están cifrados dentro de
bloques de ChaCha/Poly en los mensajes de apretón de manos de Ruido 1 y 2.
Serán descifrados como parte del proceso de apretón de manos.

La kem_shared_key se mezcla en la clave de encadenamiento con MixHash().
Ver abajo para detalles.

Alice KDF para Mensaje 1
`````````````````````````

Para XK: Después del patrón de mensaje 'es' y antes de la carga, agregue:

O

Para IK: Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', agregue:

```text
Este es el patrón de mensaje "e1":
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // Parámetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  Fin del patrón de mensaje "e1".

  NOTA: Para la siguiente sección (carga para XK o clave estática para IK),
  los keydata y la clave de encadenamiento permanecen iguales, y n ahora es igual a 1 (en lugar de 0 para no híbrido).

```

Bob KDF para Mensaje 1
`````````````````````````

Para XK: Después del patrón de mensaje 'es' y antes de la carga, agregue:

O

Para IK: Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', agregue:

```text
Este es el patrón de mensaje "e1":

  // DecryptAndHash(encap_key_section)
  // Parámetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  Fin del patrón de mensaje "e1".

  NOTA: Para la siguiente sección (carga para XK o clave estática para IK),
  los keydata y la clave de encadenamiento permanecen iguales, y n ahora es igual a 1 (en lugar de 0 para no híbrido).

```

Bob KDF para Mensaje 2
`````````````````````````

Para XK: Después del patrón de mensaje 'ee' y antes de la carga, agregue:

O

Para IK: Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', agregue:

```text
Este es el patrón de mensaje "ekem1":

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // Parámetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Fin del patrón de mensaje "ekem1".

```

Alice KDF para Mensaje 2
`````````````````````````

Después del patrón de mensaje 'ee' (y antes del patrón de mensaje 'ss' para IK), agregue:

```text
Este es el patrón de mensaje "ekem1":

  // DecryptAndHash(kem_ciphertext_section)
  // Parámetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Fin del patrón de mensaje "ekem1".

```

KDF para Mensaje 3 (solo XK)
```````````````````````````
sin cambios

KDF para split()
```````````````
sin cambios

### Ratchet

Actualice la especificación ECIES-Ratchet [ECIES](https://geti2p.net/spec/ecies) como sigue:

Identificadores de Ruido
`````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

1b) Nuevo formato de sesión (con enlace)
```````````````````````````````````````

Cambios: El ratchet actual contenía la clave estática en la primera sección de ChaCha,
y la carga útil en la segunda sección.
Con ML-KEM, ahora hay tres secciones.
La primera sección contiene la clave pública PQ cifrada.
La segunda sección contiene la clave estática.
La tercera sección contiene la carga útil.

Formato Encriptado:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nueva Clave Pública Efímera de Sesión  |
  +             32 bytes                  +
  |     Codificada con Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Clave de Encapsulamiento ML-KEM            +
  |       Datos cifrados con ChaCha20         |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +    (MAC) para Sección de Clave de Encapsulamiento        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Clave Estática X25519           +
  |       Datos cifrados con ChaCha20          |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +    (MAC) para Sección de Clave Estática       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sección de Carga Útil            +
  |       Datos cifrados con ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +         (MAC) para Sección de Carga Útil     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

```

Formato Descifrado:

```dataspec
Parte de Carga Útil 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Clave de Encapsulamiento ML-KEM               +
  |                                       |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte de Carga Útil 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Clave Estática X25519                +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte de Carga Útil 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sección de Carga Útil            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamaños:

| Tipo | Código de | ipo | len  Msg | len  Msg 1 En | len  Msg 1 De | len  PQ ke | len  pl |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


Nota: la carga útil debe contener un bloque DateTime, por lo que el tamaño mínimo de la carga útil es 7.
Los tamaños mínimos del mensaje 1 se pueden calcular en consecuencia.

1g) Nuevo formato de Respuesta de Sesión
``````````````````````````````````````

Cambios: El ratchet actual tiene una carga útil vacía para la primera sección de ChaCha,
y la carga útil en la segunda sección.
Con ML-KEM, ahora hay tres secciones.
La primera sección contiene el cifrado PQ cifrado.
La segunda sección tiene una carga útil vacía.
La tercera sección contiene la carga útil.

Formato Encriptado:

```dataspec
+----+----+----+----+----+----+----+----+
  |       Etiqueta de Sesión   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Clave Pública Efímera           +
  |                                       |
  +            32 bytes                   +
  |     Codificada con Elligator2            |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | Cifrado de Texto ML-KEM con ChaCha20  |
  +      (ver tabla abajo para longitud)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +  (MAC) para Sección de Cifrado         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +  (MAC) para Sección de Clave (sin datos)  +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sección de Carga Útil            +
  |       Datos cifrados con ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de Autenticación de Mensaje Poly1305 |
  +         (MAC) para Sección de Carga Útil     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

```

Formato Descifrado:

```dataspec
Parte de Carga Útil 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Cifrado ML-KEM                +
  |                                       |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Parte de Carga Útil 2:

  vacía

  Parte de Carga Útil 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sección de Carga Útil            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamaños:

| Tipo | Código de | ipo | len  Msg | len  Msg 2 En | len  Msg 2 De | len  PQ CT | en   op |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


Nota: mientras que el mensaje 2 normalmente tendrá una carga útil no cero, 
la especificación de ratchet [ECIES](https://geti2p.net/spec/ecies) no lo requiere, por lo que
el tamaño mínimo de carga útil es 0.
Los tamaños mínimos del mensaje 2 se pueden calcular en consecuencia.

### NTCP2

Actualice la especificación NTCP2 [NTCP2](https://geti2p.net/spec/ntcp2) como sigue:

Identificadores de Ruido
`````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

1) Solicitud de Sesión
``````````````````

Cambios: NTCP2 actual contiene solo las opciones en la sección ChaCha.
Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +            ofuscado con RH_B           +
  |       Clave pública cifrada con AES-CBC-256         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Marco ChaChaPoly (MLKEM)            |
  +      (ver tabla abajo para longitud)     +
  |   k definido en KDF para mensaje 1      |
  +   n = 0                               +
  |   ver KDF para datos asociados         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Marco ChaChaPoly (opciones)          |
  +         32 bytes                      +
  |   k definido en KDF para mensaje 1      |
  +   n = 0                               +
  |   ver KDF para datos asociados         |
  +----+----+----+----+----+----+----+----+
  |     Padding autentificado sin cifrar         |
  ~         Padding (opcional)            ~
  |     longitud definida en bloque de opciones   |
  +----+----+----+----+----+----+----+----+

  Igual que antes, excepto que se agrega un segundo marco ChaChaPoly

```

Datos sin cifrar (etiqueta de autenticación de Poly1305 no mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Clave de Encapsulamiento ML-KEM            |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               opciones                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Padding autentificado sin cifrar         |
  +         Padding (opcional)            +
  |     longitud definida en bloque de opciones   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamaños:

| Tipo | Código de | ipo | len  Msg | len  Msg 1 En | len  Msg 1 De | len  PQ ke | len  op |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4, 
y el soporte se indicará en las direcciones del router.

2) Sesión Creada
````````````````

Cambios: NTCP2 actual contiene solo las opciones en la sección ChaCha.
Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        ofuscado con RH_B           +
  |       Clave pública cifrada con AES-CBC-256         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Marco ChaChaPoly (MLKEM)            |
  +   Datos cifrados y autentificados    +
  -      (ver tabla abajo para longitud)     -
  +   k definido en KDF para mensaje 2      +
  |   n = 0; ver KDF para datos asociados       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Marco ChaChaPoly (opciones)          |
  +   Datos cifrados y autentificados    +
  -           32 bytes                    -
  +   k definido en KDF para mensaje 2      +
  |   n = 0; ver KDF para datos asociados       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Padding autentificado sin cifrar         |
  +         Padding (opcional)            +
  |     longitud definida en bloque de opciones   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Igual que antes, excepto que se agrega un segundo marco ChaChaPoly

```

Datos descifrados (etiqueta de autenticación de Poly1305 no mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Cifrado ML-KEM            |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               opciones                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Padding autentificado sin cifrar         |
  +         Padding (opcional)            +
  |     longitud definida en bloque de opciones   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tamaños:

| Tipo | Código de | ipo | len  Msg | len  Msg 2 En | len  Msg 2 De | len  PQ CT | en   op |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4,
y el soporte se indicará en las direcciones del router.

3) Sesión Confirmada
```````````````````

sin cambios

Función de Derivación de Claves (KDF) (para fase de datos)
``````````````````````````````````````

sin cambios

### SSU2

Actualice la especificación SSU2 [SSU2](https://geti2p.net/spec/ssu2) como sigue:

Identificadores de Ruido
`````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

Cabecera Larga
`````````````

La cabecera larga es de 32 bytes. Se usa antes de que se cree una sesión, para Solicitud de Token, Solicitud de Sesión, Sesión Creada, y Reintento. También se usa para Pruebas de Par y mensajes de Perforación Fuera de Sesión.

TODO: Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768. ¿Solo hacemos eso para tipos 0 y 1 o para los 6 tipos?

Antes del cifrado de cabecera:

```dataspec

+----+----+----+----+----+----+----+----+
  |      Identificación de Conexión de Destino      |
  +----+----+----+----+----+----+----+----+
  |   Número de Paquete   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Identificación de Conexión Fuente         |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Identificación de Conexión de Destino :: 8 bytes, entero sin signo en big endian

  Número de Paquete :: 4 bytes, entero sin signo en big endian

  tipo :: El tipo de mensaje = 0, 1, 7, 9, 10, o 11

  ver :: La versión del protocolo, igual a 2
         TODO Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768.

  id :: 1 byte, la identificación de la red (actualmente 2, excepto para redes de prueba)

  flag :: 1 byte, no utilizado, configurado en 0 para compatibilidad futura

  Identificación de Conexión Fuente :: 8 bytes, entero sin signo en big endian

  Token :: 8 bytes, entero sin signo en big endian

```

Cabecera Corta
`````````````

sin cambios

Solicitud de Sesión (Tipo 0)
```````````````````````

Cambios: SSU2 actual contiene solo los datos del bloque en la sección ChaCha.
Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Bytes de Cabecera Larga 0-15, ChaCha20     |
  +  cifrados con la clave de introducción de Bob     +
  |  Ver KDF de Cifrado de Cabecera            |
  +----+----+----+----+----+----+----+----+
  |  Bytes de Cabecera Larga 16-31, ChaCha20    |
  +  cifrados con la clave de introducción de Bob n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, cifrado con ChaCha20           +
  |  cifrada con la clave de introducción de Bob n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Datos cifrados con ChaCha20 (MLKEM)     |
  +          (longitud varía)              +
  |  k definido en KDF para Solicitud de Sesión    |
  +  n = 0                                +
  |  ver KDF para datos asociados          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Datos cifrados con ChaCha20 (carga útil)     |
  +          (longitud varía)              +
  |  k definido en KDF para Solicitud de Sesión    |
  +  n = 0                                +
  |  ver KDF para datos asociados          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC de Poly1305 (16 bytes)       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Datos sin cifrar (etiqueta de autenticación de Poly1305 no mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Identificación de Conexión de Destino      |
  +----+----+----+----+----+----+----+----+
  |   Número de Paquete   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Identificación de Conexión Fuente         |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Clave de Encapsulamiento ML-KEM            |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Cuerpo de Ruido (datos del bloque)        |
  +          (longitud varía)              +
  |     ver abajo para bloques permitidos      |
  +----+----+----+----+----+----+----+----+

```

Tamaños, sin incluir la sobrecarga de IP:

| Tipo | Código de | ipo | len  Msg | len  Msg 1 En | len  Msg 1 De | len  PQ ke | len  pl |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 184 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado | rande |  |  |  |


Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4,
y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: Aproximadamente 1316 para IPv4 y 1336 para IPv6.

Sesión Creada (Tipo 1)
```````````````````````
Cambios: SSU2 actual contiene solo los datos del bloque en la sección ChaCha.
Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Bytes de Cabecera Larga 0-15, ChaCha20     |
  +  cifrados con la clave de introducción de Bob y     +
  | clave derivada, ver KDF de Cifrado de Cabecera |
  +----+----+----+----+----+----+----+----+
  |  Bytes de Cabecera Larga 16-31, ChaCha20    |
  +  cifrados con clave derivada n=0       +
  |  Ver KDF de Cifrado de Cabecera         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, cifrada con ChaCha20           +
  |       con clave derivada n=0            |
  +              (32 bytes)               +
  |       Ver KDF de Cifrado de Cabecera   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Datos ChaCha20 (MLKEM)               |
  +   Datos cifrados y autentificados    +
  |  longitud varía                        |
  +  k definido en KDF para Sesión Creada +
  |  n = 0; ver KDF para datos asociados   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Datos ChaCha20 (carga útil)            |
  +   Datos cifrados y autentificados    +
  |  longitud varía                        |
  +  k definido en KDF para Sesión Creada   +
  |  n = 0; ver KDF para datos asociados   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC de Poly1305 (16 bytes)     +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Datos descifrados (etiqueta de autenticación de Poly1305 no mostrada):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Identificación de Conexión de Destino      |
  +----+----+----+----+----+----+----+----+
  |   Número de Paquete   |tipo| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Identificación de Conexión Fuente       |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    +
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Cifrado ML-KEM            |
  +      (ver tabla abajo para longitud)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Cuerpo de Ruido (datos del bloque)        |
  +          (longitud varía)              +
  |      ver abajo para bloques permitidos      |
  +----+----+----+----+----+----+----+----+

```

Tamaños, sin incluir la sobrecarga de IP:

| Tipo | Código de | ipo | len  Msg | len  Msg 2 En | len  Msg 2 De | len  PQ CT | en   pl |
| ---- | --------- | --- | -------- | ------------- | ------------- | ---------- | ------- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado | rande |  |  |  |


Nota: Los códigos de tipo son solo para uso interno. Los routers seguirán siendo de tipo 4,
y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: Aproximadamente 1316 para IPv4 y 1336 para IPv6.

Sesión Confirmada (Tipo 2)
`````````````````````````
sin cambios

KDF para fase de datos
```````````````````````
sin cambios

Relay y Prueba de Par
```````````````````

Los bloques de Relay, los bloques de Prueba de Par, y los mensajes de Prueba de Par contienen firmas.
Desafortunadamente, las firmas PQ son más grandes que el MTU.
Actualmente no hay un mecanismo para fragmentar los bloques de Relay o los mensajes de Prueba de Par a través de paquetes UDP múltiples.
El protocolo debe extenderse para soportar la fragmentación.
Esto se hará en una propuesta separada TBD.
Hasta que eso se complete, Relay y Prueba de Par no serán soportados.

Problemas
``````

Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768.

Para los mensajes 1 y 2, MLKEM768 incrementaría los tamaños de paquete más allá del MTU mínimo de 1280.
Probablemente simplemente no lo soportaríamos para esa conexión si el MTU fuera demasiado bajo.

Para los mensajes 1 y 2, MLKEM1024 incrementaría los tamaños de paquete más allá del MTU máximo de 1500.
Esto requeriría fragmentar los mensajes 1 y 2, y sería una gran complicación.
Probablemente no lo haríamos.

Relay y Prueba de Par: Ver arriba.

### Streaming

TODO: ¿Hay una manera más eficiente de definir firma/verificación para evitar copiar la firma?

### Archivos SU3

TODO

La sección 8.1 de [MLDSA-OIDS]_ prohíbe HashML-DS
