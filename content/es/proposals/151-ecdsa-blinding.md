---
title: "Desviación de claves ECDSA"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivación

A algunas personas no les gusta EdDSA o RedDSA. Deberíamos ofrecer algunas alternativas y permitirles desviar firmas ECDSA.

## Descripción general

Esta propuesta describe el desvío de claves para tipos de firma ECDSA 1, 2, 3.

## Propuesta

Funciona de la misma manera que RedDSA, pero todo está en Big Endian.
Solo se permiten los mismos tipos de firma, por ejemplo, 1->1, 2->2, 3->3.

### Definiciones

B
    Punto base de la curva

L
   Orden del grupo de la curva elíptica. Propiedad de la curva.

DERIVE_PUBLIC(a)
    Convierte una clave privada a pública, multiplicando B sobre una curva elíptica

alpha
    Un número aleatorio de 32 bytes conocido por aquellos que conocen el destino.

GENERATE_ALPHA(destination, date, secret)
    Genera alpha para la fecha actual, para quienes conocen el destino y el secreto.

a
    La clave privada de firma de 32 bytes no desviada usada para firmar el destino

A
    La clave pública de firma de 32 bytes no desviada en el destino,
    = DERIVE_PUBLIC(a), como en la curva correspondiente

a'
    La clave privada de firma desviada de 32 bytes usada para firmar el conjunto de arrendamiento cifrado
    Esta es una clave privada ECDSA válida.

A'
    La clave pública de firma ECDSA desviada de 32 bytes en el Destino,
    puede generarse con DERIVE_PUBLIC(a'), o desde A y alpha.
    Esta es una clave pública ECDSA válida en la curva

H(p, d)
    Función hash SHA-256 que toma una cadena de personalización p y datos d, y
    produce una salida de longitud de 32 bytes.

    Use SHA-256 de la siguiente manera::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Una función criptográfica de derivación de claves que toma algún material de clave de entrada ikm (que
    debe tener buena entropía pero no se requiere que sea una cadena aleatoria uniforme), una sal
    de longitud de 32 bytes, y un valor 'info' específico de contexto, y produce una salida
    de n bytes adecuada para usar como material de clave.

    Use HKDF como se especifica en [RFC-5869](https://tools.ietf.org/html/rfc5869), usando la función hash HMAC SHA-256
    como se especifica en [RFC-2104](https://tools.ietf.org/html/rfc2104). Esto significa que SALT_LEN es de 32 bytes máx.

### Cálculos de desviación

Un nuevo secreto alpha y claves desviadas deben generarse cada día (UTC).
El secreto alpha y las claves desviadas se calculan de la siguiente manera.

GENERATE_ALPHA(destination, date, secret), para todas las partes:

```text
// GENERATE_ALPHA(destination, date, secret)

  // El secreto es opcional, de lo contrario longitud cero
  A = la clave pública de firma del destino
  stA = tipo de firma de A, 2 bytes big endian (0x0001, 0x0002 o 0x0003)
  stA' = tipo de firma de la clave pública desviada A', 2 bytes big endian, siempre el mismo que stA
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD de la fecha actual UTC
  secret = cadena codificada en UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // tratar seed como un valor big-endian de 64 bytes
  alpha = seed mod L
```

BLIND_PRIVKEY(), para el propietario que publica el conjunto de arrendamiento:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = la clave privada de firma del destino
  // Adición usando aritmética escalar
  clave privada de firma desviada = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  clave pública de firma desviada = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), para los clientes que recuperan el conjunto de arrendamiento:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = la clave pública de firma del destino
  // Adición usando elementos de grupo (puntos en la curva)
  clave pública desviada = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Ambos métodos de calcular A' producen el mismo resultado, como se requiere.

## Dirección b33

La clave pública de ECDSA es un par (X,Y), así que para P256, por ejemplo, son 64 bytes, en lugar de 32 como para RedDSA.
La dirección b33 será más larga, o la clave pública puede almacenarse en formato comprimido como en las billeteras de bitcoin.

## Referencias

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
