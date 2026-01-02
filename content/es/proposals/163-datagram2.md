---
title: "Protocolo Datagram2"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Closed"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Status

Aprobado en revisión 2025-04-15.
Cambios incorporados en las especificaciones.
Implementado en Java I2P a partir de la API 0.9.66.
Revise la documentación de implementación para el estado.


## Resumen

Extraído de [Prop123](/proposals/123-new-netdb-entries/) como una propuesta separada.

Las firmas offline no pueden ser verificadas en el procesamiento de datagramas replicables.
Se necesita una bandera para indicar firma offline pero no hay lugar para poner una bandera.

Requerirá un número y formato de protocolo I2CP completamente nuevo,
para ser agregado a la especificación [DATAGRAMS](/docs/api/datagrams/).
Llamémoslo "Datagram2".


## Objetivos

- Añadir soporte para firmas offline
- Añadir resistencia a la repetición
- Añadir sabor sin firmas
- Añadir campos de banderas y opciones para extensibilidad


## No-Objetivos

Soporte completo end-to-end para control de congestión, etc.
Eso se construiría sobre, o como una alternativa a, Datagram2, que es un protocolo de bajo nivel.
No tendría sentido diseñar un protocolo de alto rendimiento únicamente sobre
Datagram2, debido al campo de origen y la sobrecarga de firma.
Cualquier protocolo de este tipo debería hacer un handshake inicial con Datagram2 y luego
cambiar a datagramas RAW.


## Motivación

Restos del trabajo de LS2 por lo demás completado en 2019.

Se espera que la primera aplicación en usar Datagram2 sea
los anuncios UDP de bittorrent, como implementado en i2psnark y zzzot,
ver [Prop160](/proposals/160-udp-trackers/).


## Especificación de Datagramas Replicables

Para referencia,
a continuación se presenta una revisión de la especificación para datagramas replicables,
copiada de [Datagrams](/docs/api/datagrams/).
El número de protocolo I2CP estándar para datagramas replicables es PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: un `Destination`
          longitud: 387+ bytes
          El originador y firmante del datagrama

  signature :: una `Signature`
               Tipo de firma debe coincidir con el tipo de clave pública de firma de $from
               longitud: 40+ bytes, como lo implica el tipo de Firma.
               Para el tipo de clave DSA_SHA1 por defecto:
                  La `Signature` DSA del hash SHA-256 de la carga útil.
               Para otros tipos de clave:
                  La `Signature` de la carga útil.
               La firma puede ser verificada por la clave pública de firma de $from

  payload ::  Los datos
              Longitud: 0 hasta aproximadamente 31.5 KB (ver notas)

  Longitud total: Longitud de la carga útil + 423+
```


## Diseño

- Definir nuevo protocolo 19 - Datagram replicable con opciones.
- Definir nuevo protocolo 20 - Datagram replicable sin firma.
- Añadir campo de banderas para firmas offline y expansión futura
- Mover la firma después de la carga útil para un procesamiento más fácil
- Nueva especificación de firma diferente de datagrama replicable o streaming, para que
  la verificación de la firma falle si se interpreta como datagrama replicable o streaming.
  Esto se logra moviendo la firma después de la carga útil,
  e incluyendo el hash de destino en la función de firma.
- Añadir prevención de repetición para datagramas, como se hizo en [Prop164](/proposals/164-streaming/) para streaming.
- Añadir sección para opciones arbitrarias
- Reutilizar formato de firma offline de [Common](/docs/specs/common-structures/) y [Streaming](/docs/specs/streaming/).
- La sección de firma offline debe estar antes de las secciones
  de carga útil y firma de longitud variable, ya que especifica la longitud
  de la firma.


## Especificación

### Protocolo

El nuevo número de protocolo I2CP para Datagram2 es 19.
Añádelo como PROTO_DATAGRAM2 a [I2CP](/docs/specs/i2cp/).

El nuevo número de protocolo I2CP para Datagram3 es 20.
Añádelo como PROTO_DATAGRAM2 a [I2CP](/docs/specs/i2cp/).


### Formato de Datagram2

Añadir Datagram2 a [DATAGRAMS](/docs/api/datagrams/) como sigue:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: un `Destination`
          longitud: 387+ bytes
          El originador y (a menos que esté firmado offline) firmante del datagrama

  flags :: (2 bytes)
           Orden de bits: 15 14 ... 3 2 1 0
           Bits 3-0: Versión: 0x02 (0 0 1 0)
           Bit 4: Si es 0, sin opciones; si es 1, mapeo de opciones incluido
           Bit 5: Si es 0, sin firma offline; si es 1, firmado offline
           Bits 15-6: sin usar, configurado en 0 para compatibilidad con usos futuros

  options :: (2+ bytes si están presentes)
           Si la bandera indica que hay opciones presentes, un `Mapping`
           que contiene opciones de texto arbitrarias

  offline_signature ::
               Si la bandera indica claves offline, la sección de firma offline,
               como se especifica en la Especificación de Estructuras Comunes,
               con los siguientes 4 campos. Longitud: varía según los tipos de firma online y offline,
               típicamente 102 bytes para Ed25519
               Esta sección puede, y debería, ser generada offline.

    expires :: Marca de tiempo de expiración
               (4 bytes, big endian, segundos desde la época, se reinicia en 2106)

    sigtype :: Tipo de firma transitorio (2 bytes, big endian)

    pubkey :: Clave pública de firma transitoria (longitud según lo implica el tipo de firma),
              típicamente 32 bytes para el tipo de firma Ed25519.

    offsig :: un `Signature`
              Firma de la marca de tiempo de expiración, tipo de firma transitorio,
              y clave pública, por la clave pública del destino,
              longitud: 40+ bytes, como lo implica el tipo de Firma, típicamente
              64 bytes para el tipo de firma Ed25519.

  payload ::  Los datos
              Longitud: 0 hasta aproximadamente 61 KB (ver notas)

  signature :: una `Signature`
               El tipo de firma debe coincidir con el tipo de clave pública de firma de $from
               (si no hay firma offline) o el tipo de firma transitorio
               (si está firmado offline)
               longitud: 40+ bytes, como lo implica el tipo de Firma, típicamente
               64 bytes para el tipo de firma Ed25519.
               La `Signature` de la carga útil y otros campos según se especifica a continuación.
               La firma es verificada por la clave pública de firma de $from
               (si no hay firma offline) o la clave pública transitoria
               (si está firmado offline)

```

Longitud total: mínimo 433 + longitud de la carga útil;
longitud típica para emisores X25519 y sin firmas offline:
457 + longitud de la carga útil.
Tenga en cuenta que el mensaje típicamente será comprimido con gzip en la capa I2CP,
lo que resultará en ahorros significativos si el destino from es comprimible.

Nota: El formato de firma offline es el mismo que en la especificación de Estructuras Comunes [Common](/docs/specs/common-structures/) y [Streaming](/docs/specs/streaming/).

### Firmas

La firma cubre los siguientes campos.

- Preludio: El hash de 32 bytes del destino objetivo (no incluido en el datagrama)
- flags
- options (si están presentes)
- offline_signature (si está presente)
- payload

En el datagrama replicable, para el tipo de clave DSA_SHA1, la firma era sobre el
hash SHA-256 de la carga útil, no la carga útil en sí; aquí, la firma es
siempre sobre los campos anteriores (NO el hash), independientemente del tipo de clave.


### Verificación de ToHash

Los receptores deben verificar la firma (usando su hash de destino)
y descartar el datagrama en caso de falla, para prevenir repeticiones.


### Formato de Datagram3

Añadir Datagram3 a [DATAGRAMS](/docs/api/datagrams/) como sigue:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: un `Hash`
              longitud: 32 bytes
              El originador del datagrama

  flags :: (2 bytes)
           Orden de bits: 15 14 ... 3 2 1 0
           Bits 3-0: Versión: 0x03 (0 0 1 1)
           Bit 4: Si es 0, sin opciones; si es 1, mapeo de opciones incluido
           Bits 15-5: sin usar, configurado en 0 para compatibilidad con usos futuros

  options :: (2+ bytes si están presentes)
           Si la bandera indica que hay opciones presentes, un `Mapping`
           que contiene opciones de texto arbitrarias

  payload ::  Los datos
              Longitud: 0 hasta aproximadamente 61 KB (ver notas)

```

Longitud total: mínimo 34 + longitud de la carga útil.


### SAM

Añadir STYLE=DATAGRAM2 y STYLE=DATAGRAM3 a la especificación SAMv3.
Actualizar la información sobre firmas offline.


### Sobrecarga

Este diseño añade 2 bytes de sobrecarga a los datagramas replicables para las banderas.
Esto es aceptable.


## Análisis de Seguridad

Incluir el hash de destino en la firma debería ser efectivo para prevenir ataques de repetición.

El formato de Datagram3 carece de firmas, por lo que el remitente no puede ser verificado,
y son posibles ataques de repetición. Cualquier validación requerida debe
realizarse en la capa de aplicación, o por el router en la capa de ratchet.


## Notas

- La longitud práctica está limitada por capas más bajas de protocolos - la especificación de
  mensajes del túnel [TUNMSG](/docs/specs/implementation/#notes) limita los mensajes a aproximadamente 61.2 KB y los transportes
  [TRANSPORT](/docs/overview/transport/) actualmente limitan los mensajes a aproximadamente 64 KB, por lo que la longitud de
  los datos aquí está limitada a aproximadamente 61 KB.
- Ver notas importantes sobre la fiabilidad de datagramas grandes [API](/docs/api/datagrams/). Para
  mejores resultados, limite la carga útil a aproximadamente 10 KB o menos.


## Compatibilidad

Ninguna. Las aplicaciones deben ser reescritas para enrutar mensajes de I2CP de Datagram2
basados en protocolo y/o puerto.
Los mensajes de Datagram2 que se enruten incorrectamente y se interpreten como
mensajes de datagrama replicable o streaming fallarán basados en firma, formato o ambos.


## Migración

Cada aplicación UDP debe detectar soporte y migrar por separado.
La aplicación UDP más prominente es bittorrent.

### Bittorrent

Bittorrent DHT: Necesita probablemente una bandera de extensión,
e.g. i2p_dg2, coordinar con BiglyBT

Bittorrent UDP Announces [Prop160](/proposals/160-udp-trackers/): Diseño desde el principio.
Coordinar con BiglyBT, i2psnark, zzzot

### Otros

Bote: Poco probable que migre, no mantenido activamente

Streamr: Nadie lo está usando, no se planea migración

Aplicaciones UDP SAM: Ninguna conocida


## Referencias

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/overview/transport/)
* [TUNMSG](/docs/specs/implementation/#notes)
