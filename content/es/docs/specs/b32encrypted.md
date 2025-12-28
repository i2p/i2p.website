---
title: "B32 para Leasesets cifrados"
description: "Formato de dirección en Base 32 para LS2 leasesets cifrados"
slug: "b32encrypted"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implementado"
---

## Descripción general

Las direcciones Base 32 ("b32") contienen el hash del destino. Esto no funcionará para LS2 cifrado (propuesta 123).

No podemos usar una dirección base 32 tradicional para un LS2 cifrado (propuesta 123), ya que solo contiene el hash del destino. No proporciona la clave pública no cegada. Los clientes deben conocer la clave pública del destino, el tipo de firma, el tipo de firma cegada y un secreto opcional o una clave privada para obtener y descifrar el leaseSet. Por lo tanto, una dirección base 32 por sí sola es insuficiente. El cliente necesita o bien el destino completo (que contiene la clave pública), o bien la clave pública por sí sola. Si el cliente tiene el destino completo en una libreta de direcciones, y la libreta de direcciones admite búsquedas inversas por hash, entonces se puede recuperar la clave pública.

Este formato coloca la clave pública en lugar del hash en una dirección base32. Este formato también debe contener el tipo de firma de la clave pública y el tipo de firma del esquema de cegado.

Este documento especifica un formato b32 para estas direcciones. Aunque durante las discusiones nos hemos referido a este nuevo formato como una dirección "b33", el formato nuevo real conserva el sufijo habitual ".b32.i2p".

## Estado de implementación

La propuesta 123 (Nuevas entradas de netDB) alcanzó su implementación completa en la versión 0.9.43 (octubre de 2019). El conjunto de funcionalidades de LS2 (tipo de leaseSet 2 cifrado) se ha mantenido estable hasta la versión 2.10.0 (septiembre de 2025), sin cambios que rompan la compatibilidad en el formato de direccionamiento ni en las especificaciones criptográficas.

Hitos clave de implementación: - 0.9.38: Compatibilidad con Floodfill para LS2 estándar con claves fuera de línea - 0.9.39: Tipo de firma RedDSA 11 y cifrado/descifrado básico - 0.9.40: Compatibilidad completa con direcciones B32 (Propuesta 149) - 0.9.41: Autenticación por cliente basada en X25519 - 0.9.42: Todas las funciones de blinding (cegado criptográfico) operativas - 0.9.43: Implementación completa declarada (octubre de 2019)

## Diseño

- El nuevo formato contiene la clave pública no cegada, el tipo de firma no cegada y el tipo de firma cegada.
- Opcionalmente indica los requisitos de secreto y/o de clave privada para enlaces privados.
- Utiliza el sufijo ".b32.i2p" existente, pero con una longitud mayor.
- Incluye una suma de verificación para la detección de errores.
- Las direcciones para leasesets cifrados se identifican por 56 o más caracteres codificados (35 o más bytes decodificados), en comparación con 52 caracteres (32 bytes) para las direcciones tradicionales en base 32.

## Especificación

### Creación y codificación

Construye un nombre de host de {56+ caracteres}.b32.i2p (35+ caracteres en binario) de la siguiente manera:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Posprocesamiento y suma de verificación:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Cualquier bit sin usar al final del b32 debe ser 0. No hay bits sin usar en una dirección estándar de 56 caracteres (35 bytes).

### Decodificación y verificación

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits de claves secretas y privadas

Los bits de clave secreta y de clave privada se utilizan para indicar a los clientes, proxies u otro código del lado del cliente que se requerirá la clave secreta y/o la clave privada para descifrar el leaseset. Implementaciones concretas pueden solicitar al usuario que proporcione los datos necesarios, o rechazar los intentos de conexión si faltan dichos datos.

Estos bits sirven únicamente como indicadores. La clave secreta o privada nunca debe incluirse en la propia dirección B32, ya que eso comprometería la seguridad.

## Detalles criptográficos

### Esquema de cegado

El esquema de cegado utiliza RedDSA, basado en Ed25519 y en el diseño de ZCash, generando firmas Red25519 sobre la curva Ed25519 usando SHA-512. Este enfoque garantiza que las claves públicas cegadas permanezcan en el subgrupo de orden primo, evitando las preocupaciones de seguridad presentes en algunos diseños alternativos.

Las claves cegadas se rotan diariamente en función de la fecha UTC utilizando la fórmula:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
La ubicación de almacenamiento de la DHT (tabla hash distribuida) se calcula como:

```
SHA256(type_byte || blinded_public_key)
```
### Cifrado

El leaseset cifrado utiliza la cifra de flujo ChaCha20 para el cifrado, elegida por su rendimiento superior en dispositivos que carecen de aceleración por hardware de AES. La especificación emplea HKDF (función de derivación de claves basada en HMAC) para la derivación de claves y X25519 (intercambio de claves de curva elíptica) para operaciones de Diffie-Hellman.

Los leasesets cifrados tienen una estructura de tres capas: - Capa externa: metadatos en claro - Capa intermedia: autenticación del cliente (métodos DH o PSK) - Capa interna: datos LS2 propiamente dichos con información de lease

### Métodos de autenticación

La autenticación por cliente admite dos métodos:

**Autenticación DH**: Utiliza el acuerdo de claves X25519. Cada cliente autorizado proporciona su clave pública al servidor, y el servidor cifra la capa intermedia utilizando un secreto compartido derivado de ECDH.

**Autenticación PSK**: Utiliza claves precompartidas directamente para el cifrado.

El bit de bandera 2 en la dirección B32 indica si se requiere autenticación por cliente.

## Caché

Si bien está fuera del alcance de esta especificación, routers y clientes deben recordar y almacenar en caché (se recomienda que sea persistente) la asignación de la clave pública al destino, y viceversa.

El servicio de nombres basado en blockfile, sistema de libreta de direcciones predeterminado de I2P desde la versión 0.9.8, mantiene múltiples libretas de direcciones con un mapa dedicado de búsqueda inversa que proporciona búsquedas rápidas por hash. Esta funcionalidad es fundamental para la resolución de leaseSet (conjunto de arrendamientos de túnel) cifrados cuando inicialmente solo se conoce un hash.

## Tipos de firma

A partir de la versión 2.10.0 de I2P, se definen los tipos de firma del 0 al 11. La codificación de un solo byte sigue siendo el estándar, con codificación de dos bytes disponible pero no utilizada en la práctica.

**Tipos de uso común:** - Tipo 0 (DSA_SHA1): Obsoleto para routers, compatible con destinos - Tipo 7 (EdDSA_SHA512_Ed25519): Estándar actual para identidades de router y destinos - Tipo 11 (RedDSA_SHA512_Ed25519): Exclusivamente para LS2 leasesets cifrados con soporte de cegado

**Nota importante**: Solo Ed25519 (tipo 7) y Red25519 (tipo 11) admiten el cegado necesario para leaseSets cifrados. No se pueden usar otros tipos de firma con esta función.

Los tipos 9-10 (algoritmos GOST) siguen reservados pero sin implementar. Los tipos 4-6 y 8 están marcados como "solo fuera de línea" para claves de firma fuera de línea.

## Notas

- Distinguir las variantes antiguas de las nuevas por la longitud. Las direcciones b32 antiguas son siempre {52 chars}.b32.i2p. Las nuevas son {56+ chars}.b32.i2p
- La codificación base32 sigue la RFC 4648, con decodificación insensible a mayúsculas/minúsculas y se prefiere la salida en minúsculas
- Las direcciones pueden superar los 200 caracteres al utilizar tipos de firma con claves públicas más grandes (p. ej., ECDSA P521 con claves de 132 bytes)
- El nuevo formato puede utilizarse en jump links (enlaces de salto) (y ser servido por jump servers (servidores de salto)) si se desea, igual que el b32 estándar
- Las claves cegadas rotan a diario según la fecha UTC para mejorar la privacidad
- Este formato se desvía del enfoque del apéndice A.2 del archivo rend-spec-v3.txt de Tor, que tiene posibles implicaciones de seguridad con claves públicas cegadas fuera de la curva

## Compatibilidad de versiones

Esta especificación es válida para I2P desde la versión 0.9.47 (agosto de 2020) hasta la versión 2.10.0 (septiembre de 2025). Durante este período no se han producido cambios incompatibles en el B32 addressing format (formato de direccionamiento B32), en la encrypted LS2 structure (estructura LS2 cifrada) ni en las implementaciones criptográficas. Todas las direcciones creadas con 0.9.47 siguen siendo totalmente compatibles con las versiones actuales.

## Referencias

**CRC-32** - [CRC-32 (Wikipedia)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Suma de verificación del Protocolo de Control de Transmisión en Flujo](https://tools.ietf.org/html/rfc3309)

**Especificaciones de I2P** - [Especificación de LeaseSet cifrado](/docs/specs/encryptedleaseset/) - [Propuesta 123: Nuevas entradas de netDB](/proposals/123-new-netdb-entries/) - [Propuesta 149: B32 (dirección base32) para LS2 cifrado (versión 2 de LeaseSet)](/proposals/149-b32-encrypted-ls2/) - [Especificación de estructuras comunes](/docs/specs/common-structures/) - [Nombres y libreta de direcciones](/docs/overview/naming/)

**Comparación con Tor** - [Hilo de discusión de Tor (contexto de diseño)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Recursos adicionales** - [Proyecto I2P](/) - [Foro de I2P](https://i2pforum.net) - [Documentación de la API de Java](http://docs.i2p-projekt.de/javadoc/)
