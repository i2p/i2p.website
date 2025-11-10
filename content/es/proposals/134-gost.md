---
title: "Tipo de Firma GOST"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Abierto"
thread: "http://zzz.i2p/topics/2239"
---

## Visión General

La firma de curva elíptica GOST R 34.10 es utilizada por oficiales y empresas en Rusia. 
Su soporte podría simplificar la integración de aplicaciones existentes (usualmente basadas en CryptoPro).
La función hash es GOST R 34.11 de 32 o 64 bytes.
Básicamente funciona de la misma manera que EcDSA, el tamaño de la firma y de la clave pública es de 64 o 128 bytes.

## Motivación

La criptografía de curvas elípticas nunca ha sido completamente confiable y genera mucha especulación sobre posibles puertas traseras.
Por lo tanto, no existe un tipo de firma definitivo que sea confiable para todos.
Agregar un tipo de firma más le dará a la gente más opciones sobre lo que confían más.

## Diseño

GOST R 34.10 utiliza una curva elíptica estándar con sus propios conjuntos de parámetros.
Se puede reutilizar la matemática de los grupos existentes.
Sin embargo, el proceso de firma y verificación es diferente y debe implementarse.
Vea RFC: https://www.rfc-editor.org/rfc/rfc7091.txt
Se supone que GOST R 34.10 funciona junto con el hash GOST R 34.11.
Usaremos GOST R 34.10-2012 (también conocido como steebog) de 256 o 512 bits.
Vea RFC: https://tools.ietf.org/html/rfc6986

GOST R 34.10 no especifica parámetros; sin embargo, existen algunos buenos conjuntos de parámetros que utilizan todos.
GOST R 34.10-2012 con claves públicas de 64 bytes hereda los conjuntos de parámetros de CryptoPro de GOST R 34.10-2001.
Vea RFC: https://tools.ietf.org/html/rfc4357

Sin embargo, los conjuntos de parámetros más nuevos para claves de 128 bytes son creados por el comité técnico especial tc26 (tc26.ru).
Vea RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

La implementación basada en OpenSSL en i2pd muestra que es más rápida que P256 y más lenta que 25519.

## Especificación

Solo se soportan GOST R 34.10-2012 y GOST R 34.11-2012.
Dos nuevos tipos de firma:
9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A representa el tipo de clave pública y firma de 64 bytes, tamaño de hash de 32 bytes y conjunto de parámetros CryptoProA (también conocido como CryptoProXchA)
10 - GOSTR3410_GOSTR3411_512_TC26_A representa el tipo de clave pública y firma de 128 bytes, tamaño de hash de 64 bytes y conjunto de parámetros A de TC26.

## Migración

Se supone que estos tipos de firma se usarán solo como tipos de firma opcionales.
No se requiere migración. i2pd ya lo soporta.
