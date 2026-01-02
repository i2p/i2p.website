---
title: "B32 para LS2 Encriptado"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
toc: true
---

## Nota
Despliegue y prueba en red en progreso.
Sujeto a revisiones menores.
Ver [SPEC](/docs/specs/b32-for-encrypted-leasesets/) para la especificación oficial.


## Resumen

Las direcciones estándar en Base 32 ("b32") contienen el hash del destino.
Esto no funcionará para ls2 encriptado (propuesta 123).

No se puede usar una dirección base 32 tradicional para un LS2 encriptado (propuesta 123),
ya que solo contiene el hash del destino. No proporciona la clave pública no cegada.
Los clientes deben conocer la clave pública del destino, el tipo de firma,
el tipo de firma cegada, y una clave secreta o privada opcional
para obtener y descifrar el leaseset.
Por lo tanto, una dirección base 32 por sí sola es insuficiente.
El cliente necesita ya sea el destino completo (que contiene la clave pública),
o la clave pública por sí sola.
Si el cliente tiene el destino completo en una libreta de direcciones, y la libreta de direcciones
admite la búsqueda inversa por hash, entonces se puede recuperar la clave pública.

Por lo tanto, necesitamos un nuevo formato que coloque la clave pública en lugar del hash en
una dirección base32. Este formato también debe contener el tipo de firma de la
clave pública y el tipo de firma del esquema de cegado.

Este documento propone un nuevo formato b32 para estas direcciones.
Aunque hemos referido a este nuevo formato durante las discusiones
como una dirección "b33", el nuevo formato real conserva el sufijo habitual ".b32.i2p".

## Objetivos

- Incluir tanto los tipos de firma no cegados como los cegados para admitir futuros esquemas de cegado
- Soportar claves públicas mayores a 32 bytes
- Asegurarse de que los caracteres b32 sean todos o mayormente aleatorios, especialmente al principio
  (no queremos que todas las direcciones empiecen con los mismos caracteres)
- Analizable
- Indicar que se requiere un secreto de cegado y/o clave por cliente
- Añadir una suma de verificación para detectar errores tipográficos
- Minimizar la longitud, mantener la longitud de la etiqueta del DNS debajo de 63 caracteres para un uso normal
- Continuar usando base 32 para insensibilidad a mayúsculas y minúsculas
- Retener el sufijo habitual ".b32.i2p".

## No-Objetivos

- No soportar enlaces "privados" que incluyan secreto de cegado y/o clave por cliente;
  esto sería inseguro.


## Diseño

- El nuevo formato contendrá la clave pública no cegada, tipo de firma no cegada,
  y tipo de firma cegada.
- Contener opcionalmente un secreto y/o clave privada, solo para enlaces privados
- Usar el sufijo existente ".b32.i2p", pero con una longitud mayor.
- Añadir una suma de verificación.
- Las direcciones para leasesets encriptados se identifican por 56 o más caracteres codificados
  (35 o más bytes decodificados), en comparación con 52 caracteres (32 bytes) para direcciones base 32 tradicionales.


## Especificación

### Creación y codificación

Construir un nombre de host de {56+ caracteres}.b32.i2p (35+ caracteres en binario) de la siguiente manera:

```text
flag (1 byte)
    bit 0: 0 para tipos de firma de un byte, 1 para tipos de firma de dos bytes
    bit 1: 0 para sin secreto, 1 si se requiere secreto
    bit 2: 0 para sin autenticación por cliente,
           1 si se requiere clave privada del cliente
    bits 7-3: No utilizados, establecer en 0

  public key sigtype (1 o 2 bytes según lo indicado en las flags)
    Si 1 byte, se asume que el byte superior es cero

  blinded key sigtype (1 o 2 bytes según lo indicado en las flags)
    Si 1 byte, se asume que el byte superior es cero

  public key
    Número de bytes según lo implica el tipo de firma
```

Post-procesamiento y suma de verificación:

```text
Construir los datos binarios como arriba.
  Tratar la suma de verificación como little-endian.
  Calcular suma de verificación = CRC-32(data[3:end])
  data[0] ^= (byte) checksum
  data[1] ^= (byte) (checksum >> 8)
  data[2] ^= (byte) (checksum >> 16)

  hostname = Base32.encode(data) || ".b32.i2p"
```

Cualquier bit no utilizado al final del b32 debe ser 0.
No hay bits no utilizados para una dirección estándar de 56 caracteres (35 bytes).


### Decodificación y Verificación

```text
eliminar el ".b32.i2p" del nombre de host
  data = Base32.decode(hostname)
  Calcular suma de verificación = CRC-32(data[3:end])
  Tratar la suma de verificación como little-endian.
  flags = data[0] ^ (byte) checksum
  si tipos de firma de 1 byte:
    pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
    blinded sigtype = data[2] ^ (byte) (checksum >> 16)
  si no (tipos de firma de 2 bytes):
    pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
    blinded sigtype = data[3] || data[4]
  analizar el resto según las flags para obtener la clave pública
```


### Bits de Secreto y Clave Privada

Los bits de secreto y clave privada se utilizan para indicar a los clientes, proxies u otros
códigos del lado del cliente que se requerirá el secreto y/o clave privada para descifrar el
leaseset. Implementaciones particulares pueden pedir al usuario que proporcione los
datos requeridos, o rechazar los intentos de conexión si faltan los datos necesarios.


## Justificación

- Hacer XOR de los primeros 3 bytes con el hash proporciona una capacidad de checksum limitada,
  y asegura que todos los caracteres base32 al principio estén aleatorizados.
  Solo unas pocas combinaciones de flags y tipos de firma son válidas, por lo que cualquier error tipográfico probablemente creará una combinación inválida y será rechazado.
- En el caso habitual (tipos de firma de 1 byte, sin secreto, sin autenticación por cliente),
  el nombre de host será {56 caracteres}.b32.i2p, decodificándose a 35 bytes, igual que Tor.
- El checksum de 2 bytes de Tor tiene una tasa de falsos negativos de 1/64K. Con 3 bytes, menos algunos bytes ignorados,
  el nuestro se aproxima a 1 en un millón, ya que la mayoría de las combinaciones flag/sigtype son inválidas.
- Adler-32 es una mala elección para entradas pequeñas, y para detectar cambios pequeños.
  Usar CRC-32 en su lugar. CRC-32 es rápido y está ampliamente disponible.

## Caching

Aunque está fuera del alcance de esta propuesta, los routers y/o clientes deben recordar y almacenar en caché
(probablemente de forma persistente) el mapeo de clave pública a destino, y viceversa.


## Notas

- Distinguir sabores antiguos de nuevos por longitud. Las direcciones b32 antiguas son siempre {52 caracteres}.b32.i2p. Las nuevas son {56+ caracteres}.b32.i2p
- Hilo de discusión de Tor: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- No esperar que los tipos de firma de 2 bytes sucedan, solo estamos en 13. No hay necesidad de implementar ahora.
- El nuevo formato puede ser utilizado en enlaces de salto (y servido por servidores de salto) si se desea, al igual que b32.


## Problemas

- Cualquier secreto, clave privada o clave pública mayor de 32 bytes
  excederá la longitud máxima de la etiqueta DNS de 63 caracteres. Probablemente a los navegadores no les importe.


## Migración

No hay problemas de compatibilidad hacia atrás. Las direcciones b32 más largas fallarán al ser convertidas
a hashes de 32 bytes en software antiguo.
