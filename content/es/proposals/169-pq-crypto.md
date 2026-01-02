---
title: "Protocolos Criptográficos Post-Cuánticos"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Abierto"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Resumen general

Aunque la investigación y competencia por criptografía post-cuántica (PQ) adecuada han estado en curso durante una década, las opciones no se han vuelto claras hasta hace poco.

Comenzamos a examinar las implicaciones de la criptografía PQ en 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Los estándares TLS añadieron soporte para cifrado híbrido en los últimos dos años y ahora se utiliza para una porción significativa del tráfico cifrado en internet debido al soporte en Chrome y Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST recientemente finalizó y publicó los algoritmos recomendados para la criptografía post-cuántica [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Varias bibliotecas de criptografía comunes ahora soportan los estándares de NIST o lanzarán soporte en el futuro cercano.

Tanto [Cloudflare](https://blog.cloudflare.com/pq-2024/) como [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomiendan que la migración comience inmediatamente. Ver también las preguntas frecuentes sobre PQ de la NSA de 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P debería ser un líder en seguridad y criptografía. Ahora es el momento de implementar los algoritmos recomendados. Usando nuestro sistema flexible de tipos criptográficos y tipos de firma, agregaremos tipos para criptografía híbrida, y para firmas PQ e híbridas.

## Objetivos

- Seleccionar algoritmos resistentes a PQ
- Añadir algoritmos solo PQ e híbridos a los protocolos I2P cuando sea apropiado
- Definir múltiples variantes
- Seleccionar las mejores variantes después de la implementación, pruebas, análisis e investigación
- Añadir soporte de forma incremental y con compatibilidad hacia atrás

## Objetivos Excluidos

- No cambiar los protocolos de cifrado unidireccional (Noise N)
- No alejarse de SHA256, no está amenazado a corto plazo por PQ
- No seleccionar las variantes preferidas finales en este momento

## Modelo de Amenazas

- Routers en el OBEP o IBGW, posiblemente confabulándose,
  almacenando mensajes garlic para descifrado posterior (forward secrecy)
- Observadores de red
  almacenando mensajes de transporte para descifrado posterior (forward secrecy)
- Participantes de red falsificando firmas para RI, LS, streaming, datagramas,
  u otras estructuras

## Protocolos Afectados

Modificaremos los siguientes protocolos, aproximadamente en orden de desarrollo. El despliegue general probablemente será desde finales de 2025 hasta mediados de 2027. Consulta la sección de Prioridades y Despliegue a continuación para más detalles.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Diseño

Soportaremos los estándares NIST FIPS 203 y 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que están basados en, pero NO son compatibles con, CRYSTALS-Kyber y CRYSTALS-Dilithium (versiones 3.1, 3, y anteriores).

### Key Exchange

Admitiremos el intercambio de claves híbrido en los siguientes protocolos:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM proporciona únicamente claves efímeras, y no soporta directamente handshakes de clave estática como Noise XK e IK.

Noise N no utiliza un intercambio de claves bidireccional y por lo tanto no es adecuado para el cifrado híbrido.

Por lo tanto, solo admitiremos cifrado híbrido, para NTCP2, SSU2 y Ratchet. Definiremos las tres variantes ML-KEM como en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para un total de 3 nuevos tipos de cifrado. Los tipos híbridos solo se definirán en combinación con X25519.

Los nuevos tipos de cifrado son:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
El overhead será sustancial. Los tamaños típicos de los mensajes 1 y 2 (para XK e IK) son actualmente de alrededor de 100 bytes (antes de cualquier payload adicional). Esto aumentará de 8x a 15x dependiendo del algoritmo.

### Signatures

Admitiremos firmas PQ e híbridas en las siguientes estructuras:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Por lo tanto, admitiremos tanto firmas solo PQ como híbridas. Definiremos las tres variantes ML-DSA como en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), tres variantes híbridas con Ed25519, y tres variantes solo PQ con prehash únicamente para archivos SU3, para un total de 9 nuevos tipos de firma. Los tipos híbridos solo se definirán en combinación con Ed25519. Utilizaremos el ML-DSA estándar, NO las variantes pre-hash (HashML-DSA), excepto para archivos SU3.

Utilizaremos la variante de firmado "hedged" o aleatorizada, no la variante "determinística", como se define en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sección 3.4. Esto garantiza que cada firma sea diferente, incluso cuando se aplique sobre los mismos datos, y proporciona protección adicional contra ataques de canal lateral. Consulta la sección de notas de implementación a continuación para obtener detalles adicionales sobre las opciones de algoritmo, incluyendo codificación y contexto.

Los nuevos tipos de firma son:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
Los certificados X.509 y otras codificaciones DER utilizarán las estructuras compuestas y OIDs definidos en [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

El overhead será sustancial. Los tamaños típicos de destino Ed25519 e identidad de router son de 391 bytes. Estos aumentarán de 3.5x a 6.8x dependiendo del algoritmo. Las firmas Ed25519 son de 64 bytes. Estas aumentarán de 38x a 76x dependiendo del algoritmo. Los RouterInfo firmados típicos, leaseSet, datagramas con respuesta, y mensajes de streaming firmados son de aproximadamente 1KB. Estos aumentarán de 3x a 8x dependiendo del algoritmo.

Como los nuevos tipos de identidad de destino y router no contendrán relleno, no serán comprimibles. Los tamaños de destinos e identidades de router que están comprimidos con gzip en tránsito aumentarán entre 12x - 38x dependiendo del algoritmo.

### Legal Combinations

Para Destinations, los nuevos tipos de firma son compatibles con todos los tipos de cifrado en el leaseset. Establece el tipo de cifrado en el certificado de clave a NONE (255).

Para RouterIdentities, el tipo de cifrado ElGamal está obsoleto. Los nuevos tipos de firma solo son compatibles con cifrado X25519 (tipo 4). Los nuevos tipos de cifrado se indicarán en las RouterAddresses. El tipo de cifrado en el certificado de clave continuará siendo tipo 4.

### New Crypto Required

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Usado únicamente para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 y SHAKE256 (extensiones XOF para SHA3-128 y SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Los vectores de prueba para SHA3-256, SHAKE128, y SHAKE256 están en [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Nota que la librería Java bouncycastle soporta todo lo mencionado anteriormente. El soporte en la librería C++ está en OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

No daremos soporte a [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), es mucho más lento y grande que ML-DSA. No daremos soporte al próximo FIPS206 (Falcon), aún no está estandarizado. No daremos soporte a NTRU u otros candidatos PQ que no fueron estandarizados por NIST.

### Rosenpass

Existe cierta investigación [paper](https://eprint.iacr.org/2020/379.pdf) sobre la adaptación de Wireguard (IK) para criptografía PQ pura, pero hay varias preguntas abiertas en ese documento. Posteriormente, este enfoque fue implementado como Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) para PQ Wireguard.

Rosenpass utiliza un handshake similar a Noise KK con claves estáticas Classic McEliece 460896 precompartidas (500 KB cada una) y claves efímeras Kyber-512 (esencialmente MLKEM-512). Como los textos cifrados de Classic McEliece son solo de 188 bytes, y las claves públicas y textos cifrados de Kyber-512 son razonables, ambos mensajes de handshake caben en un MTU UDP estándar. La clave compartida de salida (osk) del handshake PQ KK se utiliza como la clave precompartida de entrada (psk) para el handshake IK estándar de Wireguard. Por lo tanto, hay dos handshakes completos en total, uno PQ puro y uno X25519 puro.

No podemos hacer nada de esto para reemplazar nuestros handshakes XK e IK porque:

- No podemos hacer KK, Bob no tiene la clave estática de Alice
- Las claves estáticas de 500KB son demasiado grandes
- No queremos un viaje de ida y vuelta adicional

Hay mucha información valiosa en el documento técnico, y lo revisaremos en busca de ideas e inspiración. TODO.

## Specification

### Intercambio de Claves

Actualiza las secciones y tablas en el documento de estructuras comunes [/docs/specs/common-structures/](/docs/specs/common-structures/) de la siguiente manera:

### Firmas

Los nuevos tipos de Clave Pública son:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Las claves públicas híbridas son la clave X25519. Las claves públicas KEM son la clave PQ efímera enviada de Alice a Bob. La codificación y el orden de bytes están definidos en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Las claves MLKEM*_CT no son realmente claves públicas, son el "texto cifrado" enviado de Bob a Alice en el handshake de Noise. Se enumeran aquí para completitud.

### Combinaciones Legales

Los nuevos tipos de Private Key son:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Las claves privadas híbridas son las claves X25519. Las claves privadas KEM son solo para Alice. La codificación KEM y el orden de bytes se definen en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Nueva Criptografía Requerida

Los nuevos tipos de Signing Public Key son:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Las claves públicas de firma híbridas son la clave Ed25519 seguida de la clave PQ, como en [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). La codificación y el orden de bytes están definidos en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Alternativas

Los nuevos tipos de Signing Private Key son:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Las claves privadas de firma híbrida son la clave Ed25519 seguida de la clave PQ, como en [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Los nuevos tipos de Signature son:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Las firmas híbridas son la firma Ed25519 seguida de la firma PQ, como en [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Las firmas híbridas se verifican verificando ambas firmas, y fallan si cualquiera de las dos falla. La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Los nuevos tipos de Signing Public Key son:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Los nuevos tipos de Clave Pública Criptográfica son:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Los tipos de clave híbridos NUNCA se incluyen en certificados de clave; solo en leaseSets.

Para destinos con tipos de firma Hybrid o PQ, use NONE (tipo 255) para el tipo de cifrado, pero no hay clave criptográfica, y toda la sección principal de 384 bytes es para la clave de firma.

### Estructuras Comunes

Aquí están las longitudes para los nuevos tipos de Destination. El tipo de cifrado para todos es NONE (tipo 255) y la longitud de la clave de cifrado se trata como 0. Toda la sección de 384 bytes se utiliza para la primera parte de la clave pública de firma. NOTA: Esto es diferente de la especificación para los tipos de firma ECDSA_SHA512_P521 y RSA, donde mantuvimos la clave ElGamal de 256 bytes en el destination aunque no se usara.

Sin padding. La longitud total es 7 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud excedente de la clave.

Ejemplo de flujo de bytes de destino de 1319 bytes para MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### Clave Pública

Aquí están las longitudes para los nuevos tipos de Destination. El tipo de cifrado para todos es X25519 (tipo 4). Toda la sección de 352 bytes después de la clave pública X25519 se utiliza para la primera parte de la clave pública de firma. Sin relleno. La longitud total es 39 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud de clave excedente.

Ejemplo de flujo de bytes de identidad de router de 1351 bytes para MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

Los handshakes utilizan patrones de handshake de [Noise Protocol](https://noiseprotocol.org/noise.html).

Se utiliza la siguiente correspondencia de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje
- e1 = clave PQ efímera de un solo uso, enviada de Alice a Bob
- ekem1 = el texto cifrado KEM, enviado de Bob a Alice

Las siguientes modificaciones a XK e IK para secreto perfecto hacia adelante híbrido (hfs) están especificadas en [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 5:

```
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

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
El patrón e1 se define de la siguiente manera, como se especifica en [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 4:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
El patrón ekem1 se define de la siguiente manera, según se especifica en [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sección 4:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- ¿Deberíamos cambiar la función hash del handshake? Ver [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 no es vulnerable a PQ, pero si queremos actualizar
  nuestra función hash, ahora es el momento, mientras estamos cambiando otras cosas.
  La propuesta actual de SSH del IETF [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) es usar MLKEM768
  con SHA256, y MLKEM1024 con SHA384. Esa propuesta incluye
  una discusión de las consideraciones de seguridad.
- ¿Deberíamos dejar de enviar datos de ratchet 0-RTT (aparte del LS)?
- ¿Deberíamos cambiar ratchet de IK a XK si no enviamos datos 0-RTT?

#### Overview

Esta sección se aplica tanto a los protocolos IK como XK.

El handshake híbrido está definido en [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). El primer mensaje, de Alice a Bob, contiene e1, la clave de encapsulación, antes de la carga útil del mensaje. Esto se trata como una clave estática adicional; llama a EncryptAndHash() en ella (como Alice) o DecryptAndHash() (como Bob). Luego procesa la carga útil del mensaje como de costumbre.

El segundo mensaje, de Bob a Alice, contiene ekem1, el texto cifrado, antes de la carga útil del mensaje. Esto se trata como una clave estática adicional; llama a EncryptAndHash() en ella (como Bob) o DecryptAndHash() (como Alice). Luego, calcula la kem_shared_key y llama a MixKey(kem_shared_key). Después procesa la carga útil del mensaje como de costumbre.

#### Defined ML-KEM Operations

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados como se define en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Nota que tanto la encap_key como el ciphertext están encriptados dentro de bloques ChaCha/Poly en los mensajes 1 y 2 del handshake Noise. Serán desencriptados como parte del proceso de handshake.

El kem_shared_key se mezcla en la chaining key con MixHash(). Ver abajo para más detalles.

#### Alice KDF for Message 1

Para XK: Después del patrón de mensaje 'es' y antes de la carga útil, añadir:

O

Para IK: Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', agregar:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

Para XK: Después del patrón de mensaje 'es' y antes de la carga útil, agregar:

O

Para IK: Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', agregar:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

Para XK: Después del patrón de mensaje 'ee' y antes de la carga útil, añadir:

O

Para IK: Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', añadir:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

Después del patrón de mensaje 'ee' (y antes del patrón de mensaje 'ss' para IK), agregar:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
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

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

sin cambios

#### KDF for split()

sin cambios

### SigningPrivateKey

Actualiza la especificación ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) de la siguiente manera:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Cambios: El ratchet actual contenía la clave estática en la primera sección ChaCha, y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene la clave pública PQ cifrada. La segunda sección contiene la clave estática. La tercera sección contiene la carga útil.

Formato encriptado:

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Formato descifrado:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamaños:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Tenga en cuenta que el payload debe contener un bloque DateTime, por lo que el tamaño mínimo del payload es 7. Los tamaños mínimos del mensaje 1 pueden calcularse en consecuencia.

#### 1g) New Session Reply format

Cambios: El ratchet actual tiene una carga útil vacía para la primera sección ChaCha, y la carga útil en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene el texto cifrado PQ encriptado. La segunda sección tiene una carga útil vacía. La tercera sección contiene la carga útil.

Formato cifrado:

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Formato descifrado:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamaños:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Ten en cuenta que aunque el mensaje 2 normalmente tendrá una carga útil distinta de cero, la especificación ratchet [/docs/specs/ecies/](/docs/specs/ecies/) no lo requiere, por lo que el tamaño mínimo de carga útil es 0. Los tamaños mínimos del mensaje 2 pueden calcularse en consecuencia.

### Firma

Actualiza la especificación NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) de la siguiente manera:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Cambios: El NTCP2 actual contiene solo las opciones en la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Datos no encriptados (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamaños:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

#### 2) SessionCreated

Cambios: El NTCP2 actual contiene únicamente las opciones en la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenido sin procesar:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Datos no cifrados (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tamaños:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

#### 3) SessionConfirmed

Sin cambios

#### Key Derivation Function (KDF) (for data phase)

Sin cambios

### Certificados de Clave

Actualiza la especificación SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) de la siguiente manera:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

El encabezado largo es de 32 bytes. Se utiliza antes de que se cree una sesión, para Token Request, SessionRequest, SessionCreated, y Retry. También se utiliza para mensajes Peer Test y Hole Punch fuera de sesión.

TODO: Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768. ¿Hacemos eso solo para los tipos 0 y 1 o para los 6 tipos?

Antes del cifrado de cabecera:

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

sin cambios

#### SessionRequest (Type 0)

Cambios: El SSU2 actual contiene solo los datos del bloque en la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

Contenidos sin procesar:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos no cifrados (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
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
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Tamaños, sin incluir la sobrecarga IP:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: Aproximadamente 1316 para IPv4 y 1336 para IPv6.

#### SessionCreated (Type 1)

Cambios: El SSU2 actual contiene solo los datos del bloque en la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ encriptada.

Contenidos sin procesar:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos no encriptados (etiqueta de autenticación Poly1305 no mostrada):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tamaños, sin incluir la sobrecarga de IP:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: Aproximadamente 1316 para IPv4 y 1336 para IPv6.

#### SessionConfirmed (Type 2)

sin cambios

#### KDF for data phase

sin cambios

#### Problemas

Los bloques Relay, los bloques Peer Test y los mensajes Peer Test contienen firmas. Desafortunadamente, las firmas PQ son más grandes que el MTU. No existe actualmente un mecanismo para fragmentar bloques o mensajes Relay o Peer Test a través de múltiples paquetes UDP. El protocolo debe extenderse para soportar fragmentación. Esto se hará en una propuesta separada por determinar. Hasta que eso se complete, Relay y Peer Test no serán soportados.

#### Descripción general

Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768.

Para los mensajes 1 y 2, MLKEM768 aumentaría el tamaño de los paquetes más allá del MTU mínimo de 1280. Probablemente simplemente no se soportaría para esa conexión si el MTU fuera demasiado bajo.

Para los mensajes 1 y 2, MLKEM1024 aumentaría el tamaño de los paquetes más allá del MTU máximo de 1500. Esto requeriría fragmentar los mensajes 1 y 2, y sería una complicación importante. Probablemente no se hará.

Relay y Peer Test: Ver arriba

### Tamaños de destino

TODO: ¿Existe una forma más eficiente de definir la firma/verificación para evitar copiar la firma?

### Tamaños de RouterIdent

PENDIENTE

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) sección 8.1 prohíbe HashML-DSA en certificados X.509 y no asigna OIDs para HashML-DSA, debido a complejidades de implementación y seguridad reducida.

Para firmas únicamente PQ de archivos SU3, utilice los OID definidos en [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) de las variantes sin pre-hash para los certificados. No definimos firmas híbridas de archivos SU3, porque podríamos tener que hacer hash de los archivos dos veces (aunque HashML-DSA y X2559 usan la misma función hash SHA512). Además, concatenar dos claves y firmas en un certificado X.509 sería completamente no estándar.

Ten en cuenta que no permitimos la firma Ed25519 de archivos SU3, y aunque hemos definido la firma Ed25519ph, nunca hemos acordado un OID para ella, ni la hemos utilizado.

Los tipos de firma normales no están permitidos para archivos SU3; usa las variantes ph (prehash).

### Patrones de Handshake

El nuevo tamaño máximo de Destination será de 2599 (3468 en base 64).

Actualizar otros documentos que proporcionen orientación sobre los tamaños de Destination, incluyendo:

- SAMv3
- Bittorrent
- Directrices para desarrolladores
- Nomenclatura / libreta de direcciones / servidores de salto
- Otros documentos

## Overhead Analysis

### KDF de Handshake Noise

Aumento de tamaño (bytes):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Velocidad:

Velocidades según lo reportado por [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Resultados preliminares de pruebas en Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Tamaño:

Tamaños típicos de clave, firma, RIdent, Dest o incrementos de tamaño (Ed25519 incluido como referencia) asumiendo tipo de cifrado X25519 para RIs. Tamaño agregado para un Router Info, LeaseSet, datagramas con respuesta, y cada uno de los dos paquetes de streaming (SYN y SYN ACK) listados. Los Destinations y Leasesets actuales contienen padding repetido y son compresibles en tránsito. Los nuevos tipos no contienen padding y no serán compresibles, resultando en un incremento de tamaño mucho mayor en tránsito. Ver sección de diseño arriba.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Velocidad:

Velocidades según se reporta en [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Resultados preliminares de pruebas en Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

Las categorías de seguridad NIST se resumen en [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) diapositiva 10. Criterios preliminares: Nuestra categoría mínima de seguridad NIST debería ser 2 para protocolos híbridos y 3 para solo PQ.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Estos son todos protocolos híbridos. Probablemente sea necesario preferir MLKEM768; MLKEM512 no es lo suficientemente seguro.

Categorías de seguridad NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Esta propuesta define tanto tipos de firma híbridos como únicamente PQ. El híbrido MLDSA44 es preferible al MLDSA65 únicamente PQ. Los tamaños de claves y firmas para MLDSA65 y MLDSA87 son probablemente demasiado grandes para nosotros, al menos al principio.

Categorías de seguridad NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Aunque definiremos e implementaremos 3 tipos de criptografía y 9 tipos de firma, planeamos medir el rendimiento durante el desarrollo y analizar más a fondo los efectos del aumento en los tamaños de estructura. También continuaremos investigando y monitoreando los desarrollos en otros proyectos y protocolos.

Después de un año o más de desarrollo, intentaremos establecer un tipo preferido o predeterminado para cada caso de uso. La selección requerirá hacer compromisos entre ancho de banda, CPU y nivel de seguridad estimado. Es posible que no todos los tipos sean adecuados o estén permitidos para todos los casos de uso.

Las preferencias preliminares son las siguientes, sujetas a cambios:

Cifrado: MLKEM768_X25519

Firmas: MLDSA44_EdDSA_SHA512_Ed25519

Las restricciones preliminares son las siguientes, sujetas a cambios:

Cifrado: MLKEM1024_X25519 no permitido para SSU2

Firmas: MLDSA87 y variante híbrida probablemente demasiado grandes; MLDSA65 y variante híbrida pueden ser demasiado grandes

## Implementation Notes

### Library Support

Las librerías Bouncycastle, BoringSSL y WolfSSL ahora soportan MLKEM y MLDSA. El soporte de OpenSSL estará en su versión 3.5 el 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

La biblioteca Noise de southernstorm.com adaptada por Java I2P contenía soporte preliminar para handshakes híbridos, pero lo eliminamos por no utilizarse; tendremos que añadirlo de vuelta y actualizarlo para que coincida con [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Utilizaremos la variante de firma "hedged" o aleatorizada, no la variante "determinística", como se define en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sección 3.4. Esto garantiza que cada firma sea diferente, incluso cuando se aplique sobre los mismos datos, y proporciona protección adicional contra ataques de canal lateral. Aunque [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) especifica que la variante "hedged" es la predeterminada, esto puede ser cierto o no en diversas librerías. Los implementadores deben asegurar que la variante "hedged" se utilice para la firma.

Utilizamos el proceso de firma normal (llamado Generación de Firma ML-DSA Pura) que codifica el mensaje internamente como 0x00 || len(ctx) || ctx || message, donde ctx es algún valor opcional de tamaño 0x00..0xFF. No estamos utilizando ningún contexto opcional. len(ctx) == 0. Este proceso está definido en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algoritmo 2 paso 10 y Algoritmo 3 paso 5. Ten en cuenta que algunos vectores de prueba publicados pueden requerir configurar un modo donde el mensaje no se codifica.

### Reliability

El aumento de tamaño resultará en mucha más fragmentación de túneles para almacenamientos de NetDB, negociaciones de streaming y otros mensajes. Verifica los cambios en rendimiento y confiabilidad.

### Structure Sizes

Encuentra y verifica cualquier código que limite el tamaño en bytes de los router infos y leasesets.

### NetDB

Revisar y posiblemente reducir el máximo de LS/RI almacenados en RAM o en disco, para limitar el aumento de almacenamiento. ¿Aumentar los requisitos mínimos de ancho de banda para los floodfills?

### Ratchet

#### Operaciones ML-KEM Definidas

La auto-clasificación/detección de múltiples protocolos en los mismos tunnels debería ser posible basándose en una verificación de longitud del mensaje 1 (New Session Message). Usando MLKEM512_X25519 como ejemplo, la longitud del mensaje 1 es 816 bytes mayor que el protocolo ratchet actual, y el tamaño mínimo del mensaje 1 (con solo un payload DateTime incluido) es de 919 bytes. La mayoría de los tamaños de mensaje 1 con ratchet actual tienen un payload menor a 816 bytes, por lo que pueden clasificarse como ratchet no híbrido. Los mensajes grandes probablemente son POSTs que son raros.

Por lo tanto, la estrategia recomendada es:

- Si el mensaje 1 es menor a 919 bytes, es el protocolo ratchet actual.
- Si el mensaje 1 es mayor o igual a 919 bytes, probablemente es MLKEM512_X25519.
  Prueba MLKEM512_X25519 primero, y si falla, prueba el protocolo ratchet actual.

Esto debería permitirnos soportar eficientemente tanto el ratchet estándar como el ratchet híbrido en el mismo destino, tal como anteriormente soportamos ElGamal y ratchet en el mismo destino. Por lo tanto, podemos migrar al protocolo híbrido MLKEM mucho más rápidamente que si no pudiéramos soportar protocolos duales para el mismo destino, porque podemos añadir soporte MLKEM a destinos existentes.

Las combinaciones requeridas compatibles son:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Las siguientes combinaciones pueden ser complejas, y NO se requiere que sean compatibles, pero pueden serlo, dependiendo de la implementación:

- Más de un MLKEM
- ElG + uno o más MLKEM
- X25519 + uno o más MLKEM
- ElG + X25519 + uno o más MLKEM

Es posible que no intentemos soportar múltiples algoritmos MLKEM (por ejemplo, MLKEM512_X25519 y MLKEM_768_X25519) en el mismo destino. Elige solo uno; sin embargo, eso depende de que seleccionemos una variante MLKEM preferida, para que los túneles de cliente HTTP puedan usar una. Dependiente de la implementación.

PODEMOS intentar soportar tres algoritmos (por ejemplo X25519, MLKEM512_X25519, y MLKEM769_X25519) en el mismo destino. La clasificación y estrategia de reintentos puede ser demasiado compleja. La configuración y la interfaz de usuario de configuración pueden ser demasiado complejas. Dependiente de la implementación.

Probablemente NO intentaremos soportar algoritmos ElGamal e híbridos en el mismo destino. ElGamal es obsoleto, y ElGamal + híbrido solamente (sin X25519) no tiene mucho sentido. Además, tanto los Mensajes de Nueva Sesión ElGamal como los Híbridos son grandes, por lo que las estrategias de clasificación a menudo tendrían que probar ambos descifrados, lo cual sería ineficiente. Dependiente de la implementación.

Los clientes pueden usar las mismas claves estáticas X25519 o claves diferentes para los protocolos X25519 e híbrido en los mismos túneles, dependiendo de la implementación.

#### KDF de Alice para el Mensaje 1

La especificación ECIES permite Garlic Messages en la carga útil del New Session Message, lo que permite la entrega 0-RTT del paquete de streaming inicial, generalmente un HTTP GET, junto con el leaseSet del cliente. Sin embargo, la carga útil del New Session Message no tiene forward secrecy. Como esta propuesta enfatiza el forward secrecy mejorado para ratchet, las implementaciones pueden o deberían diferir la inclusión de la carga útil de streaming, o el mensaje de streaming completo, hasta el primer Existing Session Message. Esto sería a expensas de la entrega 0-RTT. Las estrategias también pueden depender del tipo de tráfico o tipo de túnel, o de GET vs. POST, por ejemplo. Dependiente de la implementación.

#### Bob KDF para Mensaje 1

MLKEM, MLDSA, o ambos en el mismo destino, aumentarán dramáticamente el tamaño del New Session Message, como se describió anteriormente. Esto puede disminuir significativamente la confiabilidad de la entrega del New Session Message a través de túneles, donde deben fragmentarse en múltiples mensajes de túnel de 1024 bytes. El éxito de la entrega es proporcional al número exponencial de fragmentos. Las implementaciones pueden usar varias estrategias para limitar el tamaño del mensaje, a expensas de la entrega 0-RTT. Dependiente de la implementación.

### Ratchet

Podemos establecer el MSB de la clave efímera (key[31] & 0x80) en la solicitud de sesión para indicar que esta es una conexión híbrida. Esto nos permitiría ejecutar tanto NTCP estándar como NTCP híbrido en el mismo puerto. Solo se soportaría una variante híbrida, y se anunciaría en la dirección del router. Por ejemplo, v=2,3 o v=2,4 o v=2,5.

Si no hacemos eso, necesitamos una dirección/puerto de transporte diferente, y un nuevo nombre de protocolo como "NTCP1PQ1".

Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

PENDIENTE

### SSU2

PUEDE necesitar diferentes direcciones/puertos de transporte, pero esperemos que no, tenemos un encabezado con banderas para el mensaje 1. Podríamos usar internamente el campo de versión y usar 3 para MLKEM512 y 4 para MLKEM768. Quizás solo v=2,3,4 en la dirección sería suficiente. Pero necesitamos identificadores para ambos algoritmos nuevos: ¿3a, 3b?

Verificar y confirmar que SSU2 puede manejar el RI fragmentado a través de múltiples paquetes (¿6-8?). ¿i2pd actualmente soporta solo 2 fragmentos como máximo?

Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

POR HACER

## Router Compatibility

### Transport Names

Probablemente no requeriremos nuevos nombres de transporte, si podemos ejecutar tanto el estándar como el híbrido en el mismo puerto, con banderas de versión.

Si necesitamos nuevos nombres de transporte, serían:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Nota que SSU2 no puede soportar MLKEM1024, es demasiado grande.

### Router Enc. Types

Tenemos varias alternativas a considerar:

#### Bob KDF para Mensaje 2

No recomendado. Usa únicamente los nuevos transportes listados arriba que coincidan con el tipo de router. Los routers más antiguos no pueden conectarse, construir túneles a través de, o enviar mensajes netdb hacia. Tomaría varios ciclos de lanzamiento para depurar y asegurar el soporte antes de habilitar por defecto. Podría extender el despliegue por un año o más sobre las alternativas de abajo.

#### Alice KDF para Mensaje 2

Recomendado. Como PQ no afecta la clave estática X25519 o los protocolos de handshake N, podríamos dejar los routers como tipo 4, y simplemente anunciar nuevos transportes. Los routers más antiguos aún podrían conectarse, construir tunnels a través de ellos, o enviar mensajes netDb.

#### KDF para el Mensaje 3 (solo XK)

Los routers tipo 4 podrían anunciar tanto direcciones NTCP2 como NTCP2PQ*. Estos podrían usar la misma clave estática y otros parámetros, o no. Estos probablemente necesitarán estar en puertos diferentes; sería muy difícil soportar tanto los protocolos NTCP2 como NTCP2PQ* en el mismo puerto, ya que no hay encabezado o enmarcado que permita a Bob clasificar y enmarcar el mensaje de Session Request entrante.

Puertos y direcciones separadas será difícil para Java pero sencillo para i2pd.

#### KDF para split()

Los routers Type 4 podrían anunciar tanto direcciones SSU2 como SSU2PQ*. Con flags de encabezado adicionales, Bob podría identificar el tipo de transporte entrante en el primer mensaje. Por lo tanto, podríamos soportar tanto SSU2 como SSUPQ* en el mismo puerto.

Estos podrían publicarse como direcciones separadas (como i2pd ha hecho en transiciones anteriores) o en la misma dirección con un parámetro que indique soporte PQ (como Java i2p ha hecho en transiciones anteriores).

Si están en la misma dirección, o en el mismo puerto en direcciones diferentes, estas usarían la misma clave estática y otros parámetros. Si están en direcciones diferentes con puertos diferentes, estas podrían usar la misma clave estática y otros parámetros, o no.

Puertos y direcciones separados serán difíciles para Java pero sencillos para i2pd.

#### Recommendations

PENDIENTE

### NTCP2

#### Identificadores de Noise

Los routers más antiguos verifican los RIs y por lo tanto no pueden conectarse, construir túneles a través de ellos, o enviar mensajes netDb. Tomaría varios ciclos de lanzamiento depurar y asegurar el soporte antes de habilitarlo por defecto. Serían los mismos problemas que el despliegue de enc. type 5/6/7; podría extender el despliegue por un año o más sobre la alternativa de despliegue de enc. type 4 mencionada arriba.

Sin alternativas.

### LS Enc. Types

#### 1b) Formato de nueva sesión (con vinculación)

Estos pueden estar presentes en el LS con claves X25519 tipo 4 más antiguas. Los routers más antiguos ignorarán las claves desconocidas.

Los destinos pueden soportar múltiples tipos de clave, pero solo realizando descifraciones de prueba del mensaje 1 con cada clave. La sobrecarga puede mitigarse manteniendo conteos de descifraciones exitosas para cada clave, y probando primero la clave más utilizada. Java I2P utiliza esta estrategia para ElGamal+X25519 en el mismo destino.

### Dest. Sig. Types

#### 1g) Formato de respuesta de nueva sesión

Los routers verifican las firmas de leaseSet y por lo tanto no pueden conectarse, o recibir leaseSets para destinos de tipo 12-17. Tomaría varios ciclos de lanzamiento depurar y garantizar el soporte antes de habilitar por defecto.

No hay alternativas.

## Especificación

Los datos más valiosos son el tráfico extremo a extremo, cifrado con ratchet. Como observador externo entre saltos de tunnel, está cifrado dos veces más, con cifrado de tunnel y cifrado de transporte. Como observador externo entre OBEP e IBGW, está cifrado solo una vez más, con cifrado de transporte. Como participante OBEP o IBGW, ratchet es el único cifrado. Sin embargo, como los tunnels son unidireccionales, capturar ambos mensajes en el handshake ratchet requeriría routers coludidos, a menos que los tunnels fueran construidos con el OBEP e IBGW en el mismo router.

El modelo de amenaza PQ más preocupante en este momento es almacenar tráfico hoy, para descifrarlo muchos muchos años en el futuro (secreto hacia adelante). Un enfoque híbrido protegería contra eso.

¿El modelo de amenaza PQ de romper las claves de autenticación en algún período de tiempo razonable (digamos unos pocos meses) y luego suplantar la autenticación o descifrar en tiempo casi real, está mucho más lejos? Y ahí es cuando querríamos migrar a claves estáticas PQC.

Por lo tanto, el primer modelo de amenaza PQ es OBEP/IBGW almacenando tráfico para descifrado posterior. Deberíamos implementar hybrid ratchet primero.

Ratchet tiene la prioridad más alta. Los transportes son los siguientes. Las firmas tienen la prioridad más baja.

El despliegue de firmas también será un año o más posterior al despliegue de cifrado, porque no es posible la compatibilidad hacia atrás. Además, la adopción de MLDSA en la industria será estandarizada por el CA/Browser Forum y las Autoridades de Certificación. Las CAs necesitan primero soporte de módulos de seguridad de hardware (HSM), que actualmente no está disponible [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Esperamos que el CA/Browser Forum impulse las decisiones sobre opciones específicas de parámetros, incluyendo si apoyar o requerir firmas compuestas [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Si no podemos soportar tanto los protocolos ratchet antiguos como los nuevos en los mismos túneles, la migración será mucho más difícil.

Deberíamos poder simplemente probar uno-luego-el-otro, como hicimos con X25519, para ser probado.

## Issues

- Selección de Hash Noise - ¿mantener SHA256 o actualizar?
  SHA256 debería ser bueno por otros 20-30 años, no está amenazado por PQ,
  Ver [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) y [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Si SHA256 se compromete tenemos problemas peores (netdb).
- NTCP2 puerto separado, dirección de router separada
- SSU2 relay / prueba de peer
- Campo de versión SSU2
- Versión de dirección de router SSU2
