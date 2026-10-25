---
title: "Protocolos de Criptografía Post-Cuántica"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Abrir"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Estado

| Protocolo / Característica | Estado |
|--------------------|--------|
| Ratchet | Completo en Java I2P e i2pd |
| NTCP2 | Beta Q1 2026 |
| SSU2 | Implementación comenzando pronto, Beta Q2/Q3 2026 |
| MLDSA SigTypes | Baja prioridad, probablemente 2027+ |
## Descripción general

Si bien la investigación y la competencia por criptografía poscuántica (PQ) adecuada han avanzado durante una década, las opciones no se han aclarado hasta hace poco.

Comenzamos a analizar las implicaciones de la criptografía post-cuántica en 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Los estándares TLS incorporaron soporte para cifrado híbrido en los últimos dos años y ahora se utiliza en una parte significativa del tráfico cifrado en internet gracias al soporte en Chrome y Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST ha finalizado y publicado recientemente los algoritmos recomendados para la criptografía post-cuántica [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Varias bibliotecas criptográficas comunes ya admiten los estándares NIST o lanzarán soporte en un futuro próximo.

Tanto [Cloudflare](https://blog.cloudflare.com/pq-2024/) como [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recomiendan que la migración comience de inmediato. Véase también el FAQ de la NSA sobre criptografía post-cuántica de 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P debería ser un referente en seguridad y criptografía. Este es el momento de implementar los algoritmos recomendados. Utilizando nuestro flexible sistema de tipos criptográficos y de firma, añadiremos tipos para criptografía híbrida, así como para firmas post-cuánticas e híbridas.

## Objetivos

- Seleccionar algoritmos resistentes a computación cuántica (PQ)
- Añadir algoritmos PQ puros e híbridos a los protocolos I2P donde corresponda
- Definir múltiples variantes
- Seleccionar las mejores variantes tras implementación, pruebas, análisis e investigación
- Añadir soporte de forma incremental y con compatibilidad hacia atrás

## No Objetivos

- No cambiar los protocolos de cifrado unidireccionales (Noise N)
- No alejarse de SHA256, no está amenazado a corto plazo por la computación cuántica (PQ)
- No seleccionar las variantes preferidas definitivas en este momento

## Modelo de Amenazas

- Routers en el OBEP o IBGW, posiblemente en colusión,
  almacenando mensajes garlic para descifrado posterior (confidencialidad directa)
- Observadores de red
  almacenando mensajes de transporte para descifrado posterior (confidencialidad directa)
- Participantes de la red falsificando firmas para RI, LS, streaming, datagramas
  u otras estructuras

## Protocolos afectados

Modificaremos los siguientes protocolos, aproximadamente en orden de desarrollo. El despliegue general probablemente se llevará a cabo desde finales de 2025 hasta mediados de 2027. Consulte la sección de Prioridades y Despliegue a continuación para más detalles.

| Protocolo / Característica | Estado |
|--------------------|--------|
| Hybrid MLKEM Ratchet y LS | Aprobado 2025-06; beta 2025-08; lanzamiento 2025-11 |
| Hybrid MLKEM NTCP2 | Probado en red en vivo, Aprobado 2026-02; objetivo beta 2026-05; objetivo lanzamiento 2026-08 |
| Hybrid MLKEM SSU2 | Aprobado 2026-02; objetivo beta 2026-08; objetivo lanzamiento 2026-11 |
| MLDSA SigTypes 12-14 | La propuesta es estable pero puede no finalizarse hasta 2027 |
| MLDSA Dests | Probado en red en vivo, requiere actualización de red para soporte floodfill |
| Hybrid SigTypes 15-17 | Preliminar |
| Hybrid Dests | |
## Diseño

Admitiremos los estándares NIST FIPS 203 y 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), que están basados en, pero NO son compatibles con, CRYSTALS-Kyber y CRYSTALS-Dilithium (versiones 3.1, 3 y anteriores).

### Intercambio de claves

Admitiremos el intercambio de claves híbrido en los siguientes protocolos:

| Proto   | Noise Type | ¿Solo PQ? | ¿Híbrido? |
|---------|------------|-----------|-----------|
| NTCP2   | XK         | no        | sí        |
| SSU2    | XK         | no        | sí        |
| Ratchet | IK         | no        | sí        |
| TBM     | N          | no        | no        |
| NetDB   | N          | no        | no        |
PQ KEM proporciona únicamente claves efímeras y no admite directamente handshakes de clave estática como Noise XK e IK.

Noise N no utiliza un intercambio de claves bidireccional, por lo que no es adecuado para cifrado híbrido.

Por lo tanto, solo admitiremos cifrado híbrido para NTCP2, SSU2 y Ratchet. Definiremos las tres variantes de ML-KEM tal como se especifica en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para un total de 3 nuevos tipos de cifrado. Los tipos híbridos solo se definirán en combinación con X25519.

Los nuevos tipos de cifrado son:

| Tipo | Código |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
La sobrecarga será considerable. Los tamaños típicos de los mensajes 1 y 2 (para XK e IK) son actualmente de alrededor de 100 bytes (antes de cualquier carga útil adicional). Esto aumentará entre 8x y 15x dependiendo del algoritmo.

### Firmas

Admitiremos firmas PQ e híbridas en las siguientes estructuras:

Por lo tanto, admitiremos tanto firmas exclusivamente PQ como firmas híbridas. Definiremos las tres variantes de ML-DSA tal como se especifica en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), tres variantes híbridas con Ed25519 y tres variantes exclusivamente PQ con prehash únicamente para archivos SU3, lo que da un total de 9 nuevos tipos de firma. Los tipos híbridos solo se definirán en combinación con Ed25519. Utilizaremos el ML-DSA estándar, NO las variantes de pre-hash (HashML-DSA), excepto para los archivos SU3.

| Tipo | ¿Admite solo PQ? | ¿Admite híbrido? |
|------|------------------|-----------------|
| RouterInfo | sí | sí |
| LeaseSet | sí | sí |
| Streaming SYN/SYNACK/Close | sí | sí |
| Datagrams respondibles | sí | sí |
| Datagram2 (prop. 163) | sí | sí |
| Mensaje I2CP de creación de sesión | sí | sí |
| Archivos SU3 | sí | sí |
| Certificados X.509 | sí | sí |
| Almacenes de claves Java | sí | sí |
Utilizaremos la variante de firma "con cobertura" (hedged) o aleatorizada, no la variante "determinista", tal como se define en la sección 3.4 de [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Esto garantiza que cada firma sea diferente, incluso cuando se aplica sobre los mismos datos, y proporciona protección adicional contra ataques de canal lateral. Consulte la sección de notas de implementación a continuación para obtener detalles adicionales sobre las decisiones algorítmicas, incluyendo la codificación y el contexto.

Los nuevos tipos de firma son:

Los certificados X.509 y otras codificaciones DER utilizarán las estructuras compuestas y OIDs definidos en el [borrador de IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Tipo | Código |
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
La sobrecarga será considerable. Los tamaños típicos de identidad de destino y router con Ed25519 son de 391 bytes. Estos aumentarán entre 3,5x y 6,8x según el algoritmo. Las firmas Ed25519 son de 64 bytes. Estas aumentarán entre 38x y 76x según el algoritmo. Los RouterInfo firmados típicos, LeaseSet, datagramas con respuesta y mensajes de streaming firmados son aproximadamente 1 KB. Estos aumentarán entre 3x y 8x según el algoritmo.

Dado que los nuevos tipos de destino e identidad de router no contendrán relleno, no serán compresibles. Los tamaños de los destinos e identidades de router que se comprimen con gzip en tránsito aumentarán entre 12x y 38x dependiendo del algoritmo.

Para los Destinations (destinos), los nuevos tipos de firma son compatibles con todos los tipos de cifrado en el leaseSet. Establezca el tipo de cifrado en el certificado de clave en NONE (255).

### Combinaciones Legales

Para RouterIdentities, el tipo de cifrado ElGamal está obsoleto. Los nuevos tipos de firma son compatibles únicamente con el cifrado X25519 (tipo 4). Los nuevos tipos de cifrado se indicarán en las RouterAddresses. El tipo de cifrado en el certificado de clave continuará siendo el tipo 4.

Los vectores de prueba para SHA3-256, SHAKE128 y SHAKE256 están disponibles en [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Nueva Criptografía Requerida

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anteriormente CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Utilizado únicamente para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 y SHAKE256 (extensiones XOF de SHA3-128 y SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Ten en cuenta que la biblioteca Java bouncycastle admite todo lo anterior. La compatibilidad con la biblioteca C++ está disponible en OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

No admitiremos [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), ya que es mucho más lento y pesado que ML-DSA. No admitiremos el próximo FIPS 206 (Falcon), puesto que aún no ha sido estandarizado. No admitiremos NTRU ni otros candidatos de criptografía post-cuántica que no hayan sido estandarizados por el NIST.

### Alternativas

Existe una [investigación](https://eprint.iacr.org/2020/379.pdf) sobre la adaptación de Wireguard (IK) para criptografía puramente PQ (post-cuántica), aunque dicho trabajo presenta varias cuestiones abiertas sin resolver. Posteriormente, este enfoque fue implementado como Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) para PQ Wireguard.

### Rosenpass

Rosenpass utiliza un handshake similar a Noise KK con claves estáticas preshared Classic McEliece 460896 (500 KB cada una) y claves efímeras Kyber-512 (esencialmente MLKEM-512). Dado que los textos cifrados de Classic McEliece tienen solo 188 bytes, y las claves públicas y textos cifrados de Kyber-512 son de tamaño razonable, ambos mensajes del handshake caben en un MTU UDP estándar. La clave compartida de salida (osk) del handshake PQ KK se utiliza como clave preshared de entrada (psk) para el handshake IK estándar de Wireguard. Por lo tanto, hay dos handshakes completos en total: uno puramente PQ y otro puramente X25519.

No podemos hacer nada de esto para reemplazar nuestros handshakes XK e IK porque:

Hay mucha información valiosa en el whitepaper, y lo revisaremos en busca de ideas e inspiración. PENDIENTE.

- No podemos usar KK, Bob no tiene la clave estática de Alice
- Las claves estáticas de 500KB son demasiado grandes
- No queremos un viaje de ida y vuelta adicional

Actualice las secciones y tablas en el documento de estructuras comunes [/docs/specs/common-structures/](/docs/specs/common-structures/) de la siguiente manera:

## Especificación

### Estructuras Comunes

Los nuevos tipos de Clave Pública son:

#### Problemas

Las claves públicas híbridas son la clave X25519. Las claves públicas KEM son la clave PQ efímera enviada de Alice a Bob. La codificación y el orden de bytes se definen en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Tipo | Longitud de Clave Pública | Desde | Uso |
|------|--------------------------|-------|-----|
| MLKEM512_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM512 | 800 | 0.9.xx | Ver propuesta 169, solo para handshakes (intercambios de claves), no para Leasesets, RIs ni Destinations |
| MLKEM768 | 1184 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| NONE | 0 | 0.9.xx | Ver propuesta 169, solo para destinations con tipos de firma PQ (post-cuántica), no para RIs ni Leasesets |
Las claves MLKEM*_CT no son realmente claves públicas, son el "texto cifrado" (ciphertext) enviado de Bob a Alice en el handshake de Noise. Se enumeran aquí por completitud.

Los nuevos tipos de Clave Privada son:

#### PrivateKey

Las claves privadas híbridas son las claves X25519. Las claves privadas KEM son exclusivas para Alice. La codificación KEM y el orden de bytes se definen en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Tipo | Longitud de Clave Privada | Desde | Uso |
|------|--------------------------|-------|-----|
| MLKEM512_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM512 | 1632 | 0.9.xx | Ver propuesta 169, solo para handshakes (negociaciones de conexión), no para Leasesets, RIs ni Destinations |
| MLKEM768 | 2400 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Ver propuesta 169, solo para handshakes, no para Leasesets, RIs ni Destinations |
Los nuevos tipos de Clave Pública de Firma son:

#### SigningPublicKey

Las claves públicas de firma híbridas consisten en la clave Ed25519 seguida de la clave PQ, tal como se define en el [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Longitud (bytes) | Desde | Uso |
|------|-----------------|-------|-----|
| MLDSA44 | 1312 | 0.9.xx | Ver propuesta 169 |
| MLDSA65 | 1952 | 0.9.xx | Ver propuesta 169 |
| MLDSA87 | 2592 | 0.9.xx | Ver propuesta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Ver propuesta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Ver propuesta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Ver propuesta 169 |
| MLDSA44ph | 1344 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb |
| MLDSA65ph | 1984 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb |
| MLDSA87ph | 2624 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb |
Los nuevos tipos de Signing Private Key (clave privada de firma) son:

#### SigningPrivateKey

Las claves privadas de firma híbrida consisten en la clave Ed25519 seguida de la clave PQ (post-cuántica), tal como se define en el [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Longitud (bytes) | Desde | Uso |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | Ver propuesta 169 |
| MLDSA65 | 4032 | 0.9.xx | Ver propuesta 169 |
| MLDSA87 | 4896 | 0.9.xx | Ver propuesta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Ver propuesta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Ver propuesta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Ver propuesta 169 |
| MLDSA44ph | 2592 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
| MLDSA65ph | 4064 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
| MLDSA87ph | 4928 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
Los nuevos tipos de firma son:

Las firmas híbridas son la firma Ed25519 seguida de la firma PQ (post-cuántica), tal como se define en el [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Las firmas híbridas se verifican comprobando ambas firmas, y el proceso falla si cualquiera de ellas no es válida. La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Firma

Las firmas híbridas consisten en la firma Ed25519 seguida de la firma PQ, tal como se describe en el [borrador de IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Las firmas híbridas se verifican comprobando ambas firmas, y fallan si cualquiera de ellas no es válida. La codificación y el orden de bytes están definidos en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Longitud (bytes) | Desde | Uso |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | Ver propuesta 169 |
| MLDSA65 | 3309 | 0.9.xx | Ver propuesta 169 |
| MLDSA87 | 4627 | 0.9.xx | Ver propuesta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Ver propuesta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Ver propuesta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Ver propuesta 169 |
| MLDSA44ph | 2484 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
| MLDSA65ph | 3373 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
| MLDSA87ph | 4691 | 0.9.xx | Solo para archivos SU3, no para estructuras netdb. Ver propuesta 169 |
Los nuevos tipos de clave pública criptográfica son:

#### Certificados de clave

Las claves públicas de firma híbridas consisten en la clave Ed25519 seguida de la clave PQ, tal como se define en el [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). La codificación y el orden de bytes se definen en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Tipo | Código de Tipo | Longitud Total de Clave Pública | Desde | Uso |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Ver propuesta 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Ver propuesta 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Ver propuesta 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Ver propuesta 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Ver propuesta 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Ver propuesta 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Solo para archivos SU3 |
| MLDSA65ph | 19 | n/a | 0.9.xx | Solo para archivos SU3 |
| MLDSA87ph | 20 | n/a | 0.9.xx | Solo para archivos SU3 |
Para destinos con tipos de firma Hybrid o PQ, utilice NONE (tipo 255) para el tipo de cifrado, pero no hay clave criptográfica, y la sección principal completa de 384 bytes está destinada a la clave de firma.

| Tipo | Código de Tipo | Longitud Total de Clave Pública | Desde | Uso |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Ver propuesta 169, solo para Leasesets, no para RIs ni Destinations |
| NONE | 255 | 0 | 0.9.xx | Ver propuesta 169 |
Los tipos de claves híbridas NUNCA se incluyen en los certificados de clave; solo en los leasesets.

Sin relleno. La longitud total es 7 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud excedente de la clave.

#### Tamaños de destino

A continuación se indican las longitudes para los nuevos tipos de Destination. El tipo de cifrado para todos es NONE (tipo 255) y la longitud de la clave de cifrado se trata como 0. La sección completa de 384 bytes se utiliza para la primera parte de la clave pública de firma. NOTA: Esto es diferente a la especificación para los tipos de firma ECDSA_SHA512_P521 y RSA, donde se mantuvo la clave ElGamal de 256 bytes en el destination aunque no se utilizara.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Ejemplo de flujo de bytes de destino de 1319 bytes para MLDSA44:

Ejemplo de flujo de bytes de identidad de router de 1351 bytes para MLDSA44:

| Tipo | Código de Tipo | Longitud Total de Clave Pública | Principal | Exceso | Longitud Total de Dest |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Tamaños de RouterIdent

A continuación se indican las longitudes para los nuevos tipos de Destination. El tipo de cifrado para todos es X25519 (tipo 4). La sección completa de 352 bytes tras la clave pública X25519 se utiliza para la primera parte de la clave pública de firma. Sin relleno. La longitud total es 39 + longitud total de la clave. La longitud del certificado de clave es 4 + longitud excedente de la clave.

Los handshakes (intercambios de autenticación) utilizan patrones de handshake del [Protocolo Noise](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Tipo | Código de Tipo | Longitud Total de Clave Pública | Principal | Exceso | Longitud Total de RouterIdent |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Las siguientes modificaciones a XK e IK para la confidencialidad directa híbrida (hfs, por sus siglas en inglés) se especifican en la sección 5 de [la especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

El patrón e1 se define de la siguiente manera, tal como se especifica en la sección 4 de la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

#### KDF para split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Identificadores de Noise

El patrón ekem1 se define de la siguiente manera, según lo especificado en la sección 4 de la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Formato de nueva sesión (con vinculación)

Esta sección aplica tanto a los protocolos IK como XK.

### Patrones de Intercambio de Claves

El handshake híbrido está definido en la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). El primer mensaje, de Alice a Bob, contiene e1, la clave de encapsulación, antes del payload del mensaje. Esto se trata como una clave estática adicional; se llama a EncryptAndHash() (como Alice) o DecryptAndHash() (como Bob). Luego se procesa el payload del mensaje de la manera habitual.

Se utiliza la siguiente asignación de letras:

- e = clave efímera de un solo uso
- s = clave estática
- p = carga útil del mensaje
- e1 = clave PQ efímera de un solo uso, enviada de Alice a Bob
- ekem1 = el texto cifrado KEM, enviado de Bob a Alice

Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos utilizados según se definen en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### KDF del protocolo de enlace Noise

#### 1b) Formato de nueva sesión (con vinculación)

- ¿Deberíamos dejar de enviar datos ratchet 0-RTT (distintos del LS)?
- ¿Deberíamos cambiar el ratchet de IK a XK si no enviamos datos 0-RTT?

#### Descripción general

kem_shared_key = DECAPS(ciphertext, decap_key)

Tenga en cuenta que tanto el encap_key como el texto cifrado están encriptados dentro de bloques ChaCha/Poly en los mensajes 1 y 2 del protocolo de enlace Noise. Serán descifrados como parte del proceso de protocolo de enlace.

El segundo mensaje, de Bob a Alice, contiene ekem1, el texto cifrado, antes del payload del mensaje. Esto se trata como una clave estática adicional; se llama a EncryptAndHash() sobre él (como Bob) o DecryptAndHash() (como Alice). Luego, se calcula el kem_shared_key y se llama a MixKey(kem_shared_key). A continuación, se procesa el payload del mensaje de la manera habitual.

#### Operaciones ML-KEM definidas

Para XK: Después del patrón de mensaje 'es' y antes del payload (carga útil), añadir:

O

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Para IK: Después del patrón de mensaje 'es' y antes del patrón de mensaje 's', añadir:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Tenga en cuenta que tanto la encap_key como el ciphertext están cifrados dentro de bloques ChaCha/Poly en los mensajes 1 y 2 del handshake de Noise. Serán descifrados como parte del proceso de handshake.

La kem_shared_key se mezcla en la clave de encadenamiento mediante MixHash(). Consulte a continuación para más detalles.

#### KDF de Alice para el Mensaje 1

Para XK: Después del patrón de mensaje 'ee' y antes del payload, añadir:

O

Para IK: Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', agregar:

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
#### KDF de Bob para el Mensaje 1

Para XK: Después del patrón de mensaje 'ee' y antes del payload, añadir:

O

Para IK: Después del patrón de mensaje 'ee' y antes del patrón de mensaje 'se', agregar:

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
#### KDF de Bob para el Mensaje 2

Actualizar la especificación ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) de la siguiente manera:

O

Formato cifrado:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF de Alice para el Mensaje 2

Después del patrón de mensaje 'ee' (y antes del patrón de mensaje 'ss' para IK), añadir:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF para el Mensaje 3

sin cambios

#### KDF para split()

sin cambios

### Ratchet

Cambios: El ratchet actual tiene un payload vacío para la primera sección ChaCha, y el payload en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene el texto cifrado PQ encriptado. La segunda sección tiene un payload vacío. La tercera sección contiene el payload.

#### Encabezado largo

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Encabezado corto

Cambios: El ratchet actual contenía la clave estática en la primera sección ChaCha y el payload (carga útil) en la segunda sección. Con ML-KEM, ahora hay tres secciones. La primera sección contiene la clave pública PQ cifrada. La segunda sección contiene la clave estática. La tercera sección contiene el payload.

Formato cifrado:

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

| Tipo | Código de Tipo | Long. X | Long. Msg 1 | Long. Msg 1 Enc | Long. Msg 1 Dec | Long. clave PQ | Long. pl |
|------|----------------|---------|-------------|-----------------|-----------------|----------------|----------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Tenga en cuenta que el payload debe contener un bloque DateTime, por lo que el tamaño mínimo del payload es 7. Los tamaños mínimos del mensaje 1 pueden calcularse en consecuencia.

#### 1g) Formato de respuesta de nueva sesión

Cambios: El NTCP2 actual contiene únicamente las opciones de la sección ChaCha. Con ML-KEM, la sección ChaCha también contendrá la clave pública PQ cifrada.

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

| Tipo | Código de tipo | Longitud Y | Longitud Msg 2 | Longitud Msg 2 cifrado | Longitud Msg 2 descifrado | Longitud PQ CT | Longitud opt |
|------|----------------|------------|----------------|------------------------|---------------------------|----------------|--------------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Ten en cuenta que, aunque el mensaje 2 normalmente tendrá un payload no nulo, la especificación del ratchet [/docs/specs/ecies/](/docs/specs/ecies/) no lo requiere, por lo que el tamaño mínimo del payload es 0. Los tamaños mínimos del mensaje 2 pueden calcularse en consecuencia.

### NTCP2

Actualizar la especificación NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) de la siguiente manera:

#### Encabezado largo

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Contenido sin procesar:

Para que PQ y non-PQ NTCP2 puedan ser compatibles en la misma dirección y puerto del router, utilizamos el bit más significativo del valor X (clave pública efímera X25519) para indicar que se trata de una conexión PQ. Este bit siempre está sin activar en conexiones non-PQ.

Nota: el campo de versión en el bloque de opciones del mensaje 1 debe establecerse en 2, incluso para conexiones PQ.

Para Bob, después de la des-ofuscación AES de X, verificar X[31] & 0x80. Si el bit está establecido, limpiarlo con X[31] &= 0x7f y descifrar mediante Noise como una conexión PQ. Si el bit está limpio, descifrar mediante Noise como una conexión no PQ de la manera habitual.

Para PQ NTCP2 anunciado en una dirección de router y puerto diferente, esto no es necesario.

Para obtener información adicional, consulte la sección Direcciones publicadas a continuación.

Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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
Nota: el campo de versión en el bloque de opciones del mensaje 1 debe establecerse en 2, incluso para conexiones PQ.

Tamaños:

| Tipo | Código de Tipo | Long. X | Long. Msg 1 | Long. Enc Msg 1 | Long. Dec Msg 1 | Long. clave PQ | Long. opt |
|------|----------------|---------|-------------|-----------------|-----------------|----------------|-----------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

#### 2) SessionCreated

Cambios: el NTCP2 actual contiene solo las opciones en una única sección ChaCha. Con ML-KEM, habrá una nueva sección ChaCha antes de las opciones, que contendrá el texto cifrado PQ cifrado.

Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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

| Tipo | Código de tipo | Long. Y | Long. Msg 2 | Long. Msg 2 Enc | Long. Msg 2 Dec | Long. PQ CT | Long. opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

#### 3) SessionConfirmed

Sin cambios

#### Función de Derivación de Clave (KDF) (para la fase de datos)

Sin cambios

#### Direcciones publicadas

En todos los casos, utilice el nombre de transporte NTCP2 como de costumbre.

Utilice la misma dirección/puerto que para una conexión no PQ y sin firewall. Solo se admite una variante PQ. En la dirección del router, publique v=2 (como de costumbre) y el nuevo parámetro pq=[3|4|5] para indicar MLKEM 512/768/1024. Alice establece el MSB de la clave efímera (key[31] & 0x80) en la solicitud de sesión para indicar que se trata de una conexión híbrida. Véase arriba. Los routers más antiguos ignorarán el parámetro pq y se conectarán como no PQ de la forma habitual.

Direcciones con firewall (sin IP publicada): En la dirección del router, publicar v=2 (como de costumbre). No es necesario publicar un parámetro pq.

Alice puede conectarse a un Bob PQ utilizando la variante PQ que Bob publica, independientemente de si Alice anuncia soporte PQ en su router info, o si anuncia la misma variante.

En la especificación actual, los mensajes 1 y 2 están definidos para tener una cantidad "razonable" de relleno, con un rango recomendado de 0 a 31 bytes y sin un máximo especificado.

#### Relleno máximo

Hasta la API 0.9.68 (versión 2.11.0), Java I2P implementaba un máximo de 256 bytes de relleno para conexiones no-PQ, aunque esto no estaba documentado anteriormente. A partir de la API 0.9.69 (versión 2.12.0), Java I2P implementa el mismo relleno máximo para conexiones no-PQ que para MLKEM-512. Véase la tabla a continuación.

Utilizar el tamaño de mensaje definido como el relleno máximo, es decir, el relleno máximo duplicará el tamaño del mensaje para las conexiones PQ, de la siguiente manera:

Utilice el tamaño de mensaje definido como el padding máximo, es decir, el padding máximo duplicará el tamaño del mensaje para conexiones PQ, de la siguiente manera:

| Relleno Máximo del Mensaje | no-PQ (hasta 0.9.68) | no-PQ (desde 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

Tenga en cuenta que MLKEM-1024 NO es compatible con SSU2, ya que las claves son demasiado grandes para caber dentro de un datagrama estándar de 1500 bytes.

#### Encabezado largo

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

El encabezado largo tiene 32 bytes. Se utiliza antes de que se cree una sesión, para los mensajes Token Request, SessionRequest, SessionCreated y Retry. También se utiliza para los mensajes Peer Test y Hole Punch fuera de sesión.

#### Tamaño de nueva sesión

En los siguientes mensajes, establezca el campo ver (versión) en el encabezado largo a 3 o 4, para indicar MLKEM-512 o MLKEM-768.

En los siguientes mensajes, establece el campo ver (versión) en la cabecera larga a 2, como de costumbre, incluso si se admite MLKEM-512 o MLKEM-768. Las implementaciones también pueden establecer el valor en 3 o 4, si el otro extremo lo admite, pero no es necesario. Las implementaciones deben aceptar cualquier valor entre 2 y 4.

- (0) Solicitud de sesión
- (1) Sesión creada
- (9) Reintentar
- (10) Solicitud de token
- (11) Hole Punch

En el siguiente mensaje, establezca el campo ver (versión) en la cabecera larga a cualquier versión entre 2 y 4, porque la elección de la versión corresponde a Alice, no a Charlie. Es aceptable establecerla siempre en 2. Las implementaciones deben aceptar cualquier valor entre 2 y 4.

- (7) Prueba de par (mensajes fuera de sesión 5-7)

Tamaños, sin incluir la sobrecarga IP:

- Relay Request (Solicitud de retransmisión)
- Relay Response (Respuesta de retransmisión)
- Relay Intro (Introducción de retransmisión)
- Peer Test (Prueba de par)

Antes del cifrado de cabecera:

Antes del cifrado de cabeceras:

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

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Ofuscación

sin cambios

#### SessionRequest (Tipo 0)

Cambio de KDF para protección contra suplantación: Para abordar los problemas planteados en la Propuesta 165 [Prop165]_, pero con una solución diferente, modificamos el KDF para la solicitud de sesión (Session Request). Esto aplica únicamente a las sesiones PQ. El KDF para las sesiones no PQ permanece sin cambios.

Cambio de KDF para protección contra suplantación: Para abordar los problemas planteados en la Propuesta 165 [Prop165]_, pero con una solución diferente, modificamos la KDF para la Solicitud de Sesión. Esto solo aplica para sesiones PQ. La KDF para sesiones no PQ permanece sin cambios.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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

| Tipo | Código de tipo | Longitud X | Longitud Msg 1 | Longitud cifrada Msg 1 | Longitud descifrada Msg 1 | Longitud clave PQ | Longitud pl |
|------|----------------|------------|----------------|------------------------|---------------------------|-------------------|-------------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado grande | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 y 1338 para IPv6. Véase más abajo.

Tamaño máximo: utiliza el MTU de Bob tal como se publica en su RouterInfo, o el valor predeterminado de 1500 si no está presente en el RouterInfo. No uses MLKEM768_X25519 si el MTU publicado es demasiado bajo.

#### SessionCreated (Tipo 1)

Cambios: el SSU2 actual contiene solo la carga útil en una única sección ChaCha. Con ML-KEM, habrá una nueva sección ChaCha antes de la carga útil, que contendrá el cifrado PQ cifrado.

Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Datos sin cifrar (etiqueta de autenticación Poly1305 no mostrada):

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
Tamaños, sin incluir la sobrecarga IP:

| Tipo | Código de tipo | Long. Y | Long. Msg 2 | Long. Msg 2 cif. | Long. Msg 2 desc. | Long. CT PQ | Long. pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | demasiado grande | | | | |
Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 y 1338 para IPv6. Véase más abajo.

Firmas PQ: Los bloques Relay, los bloques Peer Test y los mensajes Peer Test contienen firmas. Desafortunadamente, las firmas PQ son más grandes que el MTU. Actualmente no existe ningún mecanismo para fragmentar bloques o mensajes Relay o Peer Test en múltiples paquetes UDP. El protocolo debe extenderse para admitir la fragmentación. Esto se realizará en una propuesta separada que está por definirse. Hasta que se complete, Relay y Peer Test no serán compatibles.

#### SessionConfirmed (Tipo 2)

sin cambios

#### KDF para la fase de datos

sin cambios

#### Relay y Prueba de Pares

Los siguientes bloques contienen campos de versión. Permanecerán en la versión 2 (por compatibilidad con un Bob no-PQ) y no cambiarán a la versión 3/4 para PQ.

- SAMv3
- Bittorrent
- Guías para desarrolladores
- Nomenclatura / libreta de direcciones / servidores de salto
- Otros documentos

En todos los casos, utilice el nombre de transporte SSU2 como de costumbre. MLKEM-1024 no es compatible.

#### Direcciones publicadas

Usar la misma dirección/puerto que la variante sin PQ y sin firewall. Se admiten una o ambas variantes PQ. En la dirección del router, publicar v=2 (como de costumbre) y el nuevo parámetro pq=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Los routers con un MTU inferior al mínimo especificado a continuación no deben publicar un parámetro "pq" que contenga "4". Publicar 4,3 para indicar preferencia por MLKEM-768, o 3,4 para indicar preferencia por MLKEM-512. La versión real queda a criterio del iniciador y la preferencia puede no ser respetada. Los routers con un MTU inferior al mínimo especificado a continuación no deben conectarse usando MLKEM768. Los routers más antiguos ignorarán el parámetro pq y se conectarán sin PQ como de costumbre.

Ten cuidado de no superar el MTU con MLKEM768. El MTU mínimo para MLKEM768_X25519 es 1318 para IPv4 y 1338 para IPv6 (asumiendo un payload mínimo de 10 bytes con un bloque DateTime y un bloque Padding o RelayTagRequest). El MTU mínimo para SSU2 en general es 1280, por lo que no todos los peers pueden usar MLKEM768. No publiques ni uses MLKEM768 si el MTU real es inferior al mínimo, ya sea localmente o según lo anunciado por el peer. Ten cuidado de no incluir un tamaño de relleno tal que el mensaje 1 o 2 supere el MTU local o remoto.

Direcciones con firewall (sin IP publicada): En la dirección del router, publicar v=2 (como de costumbre). El parámetro pq DEBE publicarse en las direcciones con firewall para admitir el relay (retransmisión).

Direcciones con firewall (sin IP publicada): En la dirección del router, publique v=2 (como de costumbre). El parámetro pq DEBE publicarse en las direcciones con firewall, para admitir relay.

En la especificación actual, los mensajes 1 y 2 están definidos para tener una cantidad "razonable" de relleno, con un rango recomendado de 0 a 31 bytes y sin un máximo especificado.

#### MTU

TODO: ¿Existe una forma más eficiente de definir la firma/verificación para evitar copiar la firma?

### Streaming

TODO

### Archivos SU3

La sección 8.1 del [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) prohíbe HashML-DSA en certificados X.509 y no asigna OIDs para HashML-DSA, debido a la complejidad de implementación y la reducción de seguridad que implica.

Para firmas exclusivamente PQ de archivos SU3, utilice los OIDs definidos en el [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) de las variantes sin pre-hash para los certificados. No definimos firmas híbridas de archivos SU3, porque podríamos tener que aplicar hash a los archivos dos veces (aunque HashML-DSA y X2559 utilizan la misma función hash SHA512). Además, concatenar dos claves y firmas en un certificado X.509 sería completamente no estándar.

Tenga en cuenta que no permitimos la firma Ed25519 de archivos SU3 y, aunque hemos definido la firma Ed25519ph, nunca hemos acordado un OID para ella ni la hemos utilizado.

Los tipos de firma normales no están permitidos para los archivos SU3; utilice las variantes ph (prehash).

El nuevo tamaño máximo de Destination será de 2599 bytes (3468 en base 64).

### Otras Especificaciones

El nuevo tamaño máximo de Destination será 2599 (3468 en base 64).

Aumento de tamaño (bytes):

- Si el mensaje 1 tiene menos de 919 bytes, corresponde al protocolo ratchet actual.
- Si el mensaje 1 tiene 919 bytes o más, probablemente sea MLKEM512_X25519.
  Intentar primero con MLKEM512_X25519 y, si falla, intentar con el protocolo ratchet actual.

## Análisis de Sobrecarga

### Intercambio de claves

Velocidad:

| Tipo | Clave pública (Msg 1) | Texto cifrado (Msg 2) |
|------|----------------------|----------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Velocidades según lo informado por [Cloudflare](https://blog.cloudflare.com/pq-2024/):

Resultados preliminares de las pruebas en Java:

| Tipo | Velocidad relativa |
|------|----------------|
| X25519 DH/keygen | línea base |
| MLKEM512 | 2.25x más rápido |
| MLKEM768 | 1.5x más rápido |
| MLKEM1024 | 1x (igual) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% más lento |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% más lento |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% más lento |
Tamaño:

| Tipo | DH/encaps relativo | DH/desencaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | línea base | línea base | línea base |
| MLKEM512 | 29x más rápido | 22x más rápido | 17x más rápido |
| MLKEM768 | 17x más rápido | 14x más rápido | 9x más rápido |
| MLKEM1024 | 12x más rápido | 10x más rápido | 6x más rápido |
### Firmas

#### Tamaños

Los tipos de firma normales no están permitidos para los archivos SU3; utiliza las variantes ph (prehash).

| Tipo | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (cada msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Velocidades

Resultados preliminares de las pruebas en Java:

| Tipo | Signo de velocidad relativa | verificar |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | referencia | referencia |
| MLDSA44 | 5x más lento | 2x más rápido |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Tamaño:

| Tipo | Signo de velocidad relativa | verificar | generación de claves |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | referencia | referencia | referencia |
| MLDSA44 | 4.6x más lento | 1.7x más rápido | 2.6x más rápido |
| MLDSA65 | 8.1x más lento | igual | 1.5x más rápido |
| MLDSA87 | 11.1x más lento | 1.5x más lento | igual |
## Análisis de seguridad

Las categorías de seguridad del NIST se resumen en la [presentación del NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf), diapositiva 10. Criterios preliminares: Nuestra categoría de seguridad NIST mínima debería ser 2 para protocolos híbridos y 3 para los exclusivamente poscuánticos (PQ-only).

| Categoría | Tan Seguro Como |
|-----------|-----------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Categorías de seguridad NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Esta propuesta define tanto tipos de firma híbrida como exclusivamente PQ (post-cuántica). El híbrido MLDSA44 es preferible al MLDSA65 exclusivamente PQ. Los tamaños de claves y firmas para MLDSA65 y MLDSA87 son probablemente demasiado grandes para nosotros, al menos en un principio.

| Algoritmo | Categoría de Seguridad |
|-----------|------------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Firmas

Categorías de seguridad NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

Si bien definiremos e implementaremos 3 tipos de cifrado y 9 tipos de firma, planeamos medir el rendimiento durante el desarrollo y analizar más a fondo los efectos del aumento en los tamaños de las estructuras. También continuaremos investigando y monitoreando los avances en otros proyectos y protocolos.

| Algoritmo | Categoría de Seguridad |
|-----------|------------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Preferencias de tipo

Tras el desarrollo y las pruebas, se establecerá un tipo preferido o predeterminado para cada caso de uso. La selección requerirá equilibrar el ancho de banda, la CPU y el nivel de seguridad estimado. No todos los tipos pueden ser adecuados o estar permitidos para todos los casos de uso.

Las preferencias preliminares son las siguientes, sujetas a cambios:

Cifrado: MLKEM768_X25519

Firmas: MLDSA44_EdDSA_SHA512_Ed25519

Las restricciones preliminares son las siguientes, sujetas a cambios:

Firmas: MLDSA87 y su variante híbrida probablemente son demasiado grandes; MLDSA65 y su variante híbrida pueden ser demasiado grandes

Las bibliotecas Bouncycastle, BoringSSL y WolfSSL ya son compatibles con MLKEM y MLDSA. El soporte de OpenSSL estará disponible en su versión 3.5 el 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Notas de implementación

### Soporte de Biblioteca

La biblioteca Noise de southernstorm.com adaptada por Java I2P contenía soporte preliminar para handshakes híbridos, pero lo eliminamos por no utilizarse; tendremos que volver a añadirlo y actualizarlo para que coincida con la [especificación Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

Utilizaremos la variante de firma "hedged" (con aleatorización) en lugar de la variante "determinista", tal como se define en la sección 3.4 de [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Esto garantiza que cada firma sea diferente, incluso cuando se aplica sobre los mismos datos, y proporciona protección adicional contra ataques de canal lateral. Si bien [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) especifica que la variante "hedged" es la predeterminada, esto puede o no ser así en las distintas bibliotecas. Los implementadores deben asegurarse de que se utilice la variante "hedged" para la firma.

### Variantes de Firma

Utilizamos el proceso de firma estándar (denominado Pure ML-DSA Signature Generation) que codifica el mensaje internamente como 0x00 || len(ctx) || ctx || message, donde ctx es un valor opcional de tamaño 0x00..0xFF. No se utiliza ningún contexto opcional. len(ctx) == 0. Este proceso está definido en [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algoritmo 2, paso 10 y Algoritmo 3, paso 5. Nótese que algunos vectores de prueba publicados pueden requerir configurar un modo en el que el mensaje no sea codificado.

El aumento de tamaño resultará en una mayor fragmentación de túneles para los almacenes en NetDB, los handshakes de streaming y otros mensajes. Verifique los cambios en rendimiento y fiabilidad.

### Confiabilidad

Encuentra y verifica cualquier código que limite el tamaño en bytes de los router infos y leasesets.

### Tamaños de Estructura

Revisar y posiblemente reducir el máximo de LS/RI almacenados en RAM o en disco, para limitar el aumento del almacenamiento. ¿Aumentar los requisitos mínimos de ancho de banda para los floodfills?

### NetDB

La clasificación/detección automática de múltiples protocolos en los mismos tunnels debería ser posible basándose en una verificación de longitud del mensaje 1 (New Session Message). Usando MLKEM512_X25519 como ejemplo, la longitud del mensaje 1 es 816 bytes mayor que la del protocolo ratchet actual, y el tamaño mínimo del mensaje 1 (con solo un payload DateTime incluido) es de 919 bytes. La mayoría de los tamaños del mensaje 1 con el ratchet actual tienen un payload inferior a 816 bytes, por lo que pueden clasificarse como ratchet no híbrido. Los mensajes de gran tamaño probablemente sean POSTs, que son poco frecuentes.

### Ratchet

#### Túneles Compartidos

Por lo tanto, la estrategia recomendada es:

Esto debería permitirnos soportar eficientemente el ratchet estándar y el ratchet híbrido en el mismo destino, tal como anteriormente soportábamos ElGamal y ratchet en el mismo destino. Por lo tanto, podemos migrar al protocolo híbrido MLKEM mucho más rápidamente que si no pudiéramos soportar protocolos duales para el mismo destino, ya que podemos añadir soporte MLKEM a los destinos existentes.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Las combinaciones compatibles requeridas son:

Las siguientes combinaciones pueden ser complejas y NO es obligatorio que sean compatibles, aunque podrían serlo dependiendo de la implementación:

- Más de un MLKEM
- ElG + uno o más MLKEM
- X25519 + uno o más MLKEM
- ElG + X25519 + uno o más MLKEM

Es posible que no intentemos admitir múltiples algoritmos MLKEM (por ejemplo, MLKEM512_X25519 y MLKEM_768_X25519) en el mismo destino. Selecciona solo uno; sin embargo, eso depende de que elijamos una variante MLKEM preferida, para que los túneles de cliente HTTP puedan usar una. Depende de la implementación.

- Selección de Hash para Noise - ¿quedarse con SHA256 o actualizar?
  SHA256 debería ser seguro durante otros 20-30 años, no está amenazado por PQ (computación cuántica post-cuántica),
  Ver [presentación del NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) y [presentación del NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Si SHA256 se rompe, tendremos problemas peores (netdb).
- NTCP2 puerto separado, dirección de router separada
- SSU2 relay / prueba de pares
- Campo de versión SSU2
- Versión de dirección de router SSU2

PODEMOS intentar soportar tres algoritmos (por ejemplo X25519, MLKEM512_X25519 y MLKEM769_X25519) en el mismo destino. La clasificación y la estrategia de reintento pueden resultar demasiado complejas. La configuración y la interfaz de usuario de configuración pueden ser demasiado complejas. Depende de la implementación.

Probablemente NO intentaremos dar soporte a ElGamal y a los algoritmos híbridos en el mismo destino. ElGamal está obsoleto, y ElGamal + híbrido sin X25519 no tiene mucho sentido. Además, tanto los mensajes de nueva sesión de ElGamal como los híbridos son de gran tamaño, por lo que las estrategias de clasificación frecuentemente tendrían que intentar ambas descifraciones, lo cual resultaría ineficiente. Depende de la implementación.

Los clientes pueden usar las mismas claves estáticas X25519 o claves diferentes para los protocolos X25519 e híbrido en los mismos tunnels, según la implementación.

La especificación ECIES permite Garlic Messages en el payload del New Session Message, lo que posibilita la entrega 0-RTT del paquete de streaming inicial, generalmente un HTTP GET, junto con el leaseSet del cliente. Sin embargo, el payload del New Session Message no tiene forward secrecy (secreto hacia adelante). Dado que esta propuesta enfatiza un forward secrecy mejorado para el ratchet, las implementaciones pueden o deberían diferir la inclusión del payload de streaming, o del mensaje de streaming completo, hasta el primer Existing Session Message. Esto tendría como costo la entrega 0-RTT. Las estrategias también pueden depender del tipo de tráfico o del tipo de tunnel, o bien de si se trata de un GET vs. POST, por ejemplo. Depende de la implementación.

#### Secreto hacia adelante

MLKEM, MLDSA, o ambos en el mismo destino, aumentarán drásticamente el tamaño del New Session Message, como se describe anteriormente. Esto puede reducir significativamente la fiabilidad de la entrega del New Session Message a través de tunnels, donde deben fragmentarse en múltiples mensajes de tunnel de 1024 bytes. El éxito de la entrega es proporcional al número exponencial de fragmentos. Las implementaciones pueden utilizar diversas estrategias para limitar el tamaño del mensaje, a expensas de la entrega 0-RTT. Dependiente de la implementación.

#### Tamaño de nueva sesión

Establecemos el bit más significativo de la clave efímera (key[31] & 0x80) en la solicitud de sesión para indicar que se trata de una conexión híbrida. Esto nos permite ejecutar tanto NTCP estándar como NTCP híbrido en el mismo puerto. Solo se admitirá una variante híbrida, que se anunciará en la dirección del router. Por ejemplo, v=2,3 o v=2,4 o v=2,5.

### NTCP2

Como Alice, para una conexión PQ, antes de la ofuscación, establece X[31] |= 0x80. Esto convierte a X en una clave pública X25519 no válida. Después de la ofuscación, AES-CBC la aleatorizará. El MSB de X será aleatorio después de la ofuscación.

#### Ofuscación

Como Bob, verificar si (X[31] & 0x80) != 0 después de la des-ofuscación. Si es así, se trata de una conexión PQ.

La versión mínima del router requerida para NTCP2-PQ está por determinar.

Los clientes pueden usar las mismas o diferentes claves estáticas X25519 para los protocolos X25519 y los híbridos en los mismos túneles, dependiendo de la implementación.

Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

### SSU2

Utilizamos el campo de versión en el encabezado largo y lo establecemos en 3 para MLKEM512 y 4 para MLKEM768. v=2,3,4 en la dirección sería suficiente.

La versión mínima del router requerida para NTCP2-PQ está por determinarse (TBD).

Nota: Los códigos de tipo son solo para uso interno. Los routers permanecerán como tipo 4, y el soporte se indicará en las direcciones del router.

## Compatibilidad del Router

### Nombres de Transporte

En todos los casos, utilice los nombres de transporte NTCP2 y SSU2 como de costumbre.

### Tipos de Enc. del Router

No recomendado. Utilice únicamente los nuevos transportes listados anteriormente que coincidan con el tipo de router. Los routers más antiguos no pueden conectarse, construir tunnels a través de, ni enviar mensajes de netDb. Requeriría varios ciclos de versiones para depurar y garantizar el soporte antes de habilitarlo por defecto. Podría extender el despliegue en un año o más en comparación con las alternativas que se describen a continuación.

#### Routers de Tipo 5/6/7

Recomendado. Dado que PQ no afecta a la clave estática X25519 ni a los protocolos de handshake N, podríamos dejar los routers como tipo 4 y simplemente anunciar nuevos transportes. Los routers más antiguos aún podrían conectarse, construir tunnels a través de ellos o enviarles mensajes netdb.

#### Routers de Tipo 4

MLKEM-768 es el recomendado para Ratchet, NTCP2 y SSU2, como el mejor equilibrio entre seguridad y longitud de clave.

#### Recomendaciones

Los routers más antiguos verifican los RIs y, por lo tanto, no pueden conectarse, construir tunnels a través de ellos ni enviarles mensajes netdb. Llevaría varios ciclos de lanzamiento depurar y garantizar el soporte antes de habilitarlo por defecto. Presentaría los mismos problemas que el despliegue de los tipos de cifrado 5/6/7; podría extender el despliegue un año o más en comparación con la alternativa de despliegue del tipo de cifrado 4 mencionada anteriormente.

### Tipos de firma del router

#### Routers de tipo 12-17

Sin alternativas.

Estas pueden estar presentes en el LS con claves X25519 de tipo 4 más antiguas. Los routers más antiguos ignorarán las claves desconocidas.

### Tipos de Cifrado LS

#### Claves LS de tipo 5-7

Los destinos pueden admitir múltiples tipos de clave, pero solo mediante intentos de descifrado del mensaje 1 con cada clave. La sobrecarga puede mitigarse manteniendo un recuento de descifrados exitosos para cada clave e intentando primero con la clave más utilizada. Java I2P utiliza esta estrategia para ElGamal+X25519 en el mismo destino.

Los routers verifican las firmas de los leaseSet y, por lo tanto, no pueden conectarse ni recibir leaseSets para destinos de tipo 12-17. Se necesitarían varios ciclos de lanzamiento para depurar y garantizar el soporte antes de habilitarlo por defecto.

### Tipos de Firma de Destino

#### Destinos de tipo 12-17

Los routers verifican las firmas de leaseSet y, por lo tanto, no pueden conectarse ni recibir leaseSets para destinos de tipo 12-17. Se necesitarían varios ciclos de lanzamiento para depurar y asegurar el soporte antes de habilitarlo por defecto.

Estas pueden estar presentes en el LS con claves X25519 de tipo 4 más antiguas. Los routers más antiguos ignorarán las claves desconocidas.

## Prioridades y Despliegue

Los datos más valiosos son el tráfico de extremo a extremo, cifrado con ratchet. Como observador externo entre saltos de tunnel, está cifrado dos veces más: con cifrado de tunnel y cifrado de transporte. Como observador externo entre el OBEP y el IBGW, está cifrado solo una vez más, con cifrado de transporte. Como participante OBEP o IBGW, ratchet es el único cifrado. Sin embargo, dado que los tunnels son unidireccionales, capturar ambos mensajes en el protocolo de enlace ratchet requeriría la colaboración de routers comprometidos, a menos que los tunnels se construyeran con el OBEP y el IBGW en el mismo router.

El modelo de amenaza PQ de romper las claves de autenticación en un período de tiempo razonable (digamos unos pocos meses) y luego suplantar la autenticación o descifrar en tiempo casi real, ¿está mucho más lejos? Y es en ese momento cuando querríamos migrar a claves estáticas PQC.

Por lo tanto, el modelo de amenaza PQ (post-cuántica) más temprano es el OBEP/IBGW almacenando tráfico para descifrado posterior. Deberíamos implementar el ratchet híbrido primero.

Ratchet es la prioridad más alta. Los transportes son los siguientes. Las firmas tienen la prioridad más baja.

El despliegue de firmas también llegará un año o más después que el despliegue del cifrado, ya que no es posible ninguna compatibilidad con versiones anteriores. Además, la adopción de MLDSA en la industria será estandarizada por el CA/Browser Forum y las Autoridades de Certificación. Las CAs necesitan primero soporte de módulo de seguridad de hardware (HSM), que actualmente no está disponible [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Esperamos que el CA/Browser Forum impulse las decisiones sobre opciones de parámetros específicos, incluyendo si se deben admitir o requerir firmas compuestas [borrador IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Deberíamos poder simplemente probar uno tras otro, como hicimos con X25519, para ser verificados.

El trabajo sobre el soporte de firmas MLDSA en I2P está suspendido hasta finales de 2027 o 2028, a la espera de que los organismos de estándares seleccionen algoritmos, posiblemente reduzcan el tamaño de las claves y/o firmas, y promuevan la adopción industrial. Véase [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) y [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Además, la adopción de MLDSA en la industria será estandarizada por el IETF, el Foro CA/Navegadores (CA/Browser Forum) y las Autoridades de Certificación. Las AC necesitan primero soporte en módulos de seguridad hardware (HSM), que actualmente no está disponible [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Esperamos que el IETF y el Foro CA/Navegadores impulsen las decisiones sobre opciones específicas de parámetros, incluyendo si apoyar o requerir firmas compuestas [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Hito | Objetivo |
|-----------|--------|
| Ratchet beta | Finales de 2025 |
| Seleccionar mejor tipo de cifrado | Principios de 2026 |
| NTCP2 beta | Principios de 2026 |
| SSU2 beta | Mediados de 2026 |
| Ratchet producción | Mediados de 2026 |
| Ratchet predeterminado | Finales de 2026 |
| Firma beta | Finales de 2026 |
| NTCP2 producción | Finales de 2026 |
| SSU2 producción | Principios de 2027 |
| Seleccionar mejor tipo de firma | Principios de 2027 |
| NTCP2 predeterminado | Principios de 2027 |
| SSU2 predeterminado | Mediados de 2027 |
| Firma producción | Mediados de 2027 |
## Migración

Deberíamos poder simplemente intentar uno y luego el otro, como hicimos con X25519, para comprobarlo.

Deberíamos poder simplemente intentar uno y luego el otro, como hicimos con X25519, para comprobarlo.

## 1b) Formato de nueva sesión (con vinculación)

SHA256 debería ser seguro durante otros 20-30 años, sin amenazas por computación cuántica (PQ), ver [presentación de NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) y [presentación de NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Si SHA256 se rompe, tendremos problemas más graves (netDb).

## Referencias

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
