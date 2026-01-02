---
title: "Búsquedas en la Base de Datos desde Destinos ECIES"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Closed"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Nota
ECIES a ElG está implementado en 0.9.46 y la fase de propuesta está cerrada.
Véase [I2NP](/docs/specs/i2np/) para la especificación oficial.
Esta propuesta aún puede ser referenciada para información de fondo.
ECIES a ECIES con claves incluidas está implementado a partir de 0.9.48.
La sección ECIES-a-ECIES (claves derivadas) puede ser reabierta o incorporada
en una propuesta futura.


## Visión general

### Definiciones

- AEAD: ChaCha20/Poly1305
- DLM: Mensaje de Búsqueda en la Base de Datos I2NP
- DSM: Mensaje de Almacenamiento en la Base de Datos I2NP
- DSRM: Respuesta de Búsqueda en la Base de Datos I2NP
- ECIES: ECIES-X25519-AEAD-Ratchet (propuesta 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): Como se define en [ECIES](/docs/specs/ecies/)
- LS: Leaseset
- lookup: DLM I2NP
- reply: DSM o DSRM I2NP


### Resumen

Al enviar un DLM para un LS a un floodfill, el DLM generalmente especifica
que la respuesta sea etiquetada, cifrada con AES, y enviada por un túnel al destino.
El soporte para respuestas cifradas con AES se añadió en la 0.9.7.

Las respuestas cifradas con AES fueron especificadas en la 0.9.7 para minimizar la gran sobrecarga criptográfica de ElG y porque reutilizaba la función de etiquetas/AES en ElGamal/AES+SessionTags.
Sin embargo, las respuestas AES pueden ser alteradas en el IBEP ya que no tienen autenticación, y las respuestas no son secreto hacia adelante.

Con destinos [ECIES](/docs/specs/ecies/), la intención de la propuesta 144 es que
los destinos ya no soporten etiquetas de 32 bytes y descifrado AES.
Los detalles no se incluyeron intencionalmente en esa propuesta.

Esta propuesta documenta una nueva opción en el DLM para solicitar respuestas cifradas con ECIES.


### Objetivos

- Nuevas banderas para DLM cuando se solicita una respuesta cifrada a través de un túnel a un destino ECIES.
- Para la respuesta, agregar secreto hacia adelante y autenticación del remitente resistente a la
  suplantación por compromiso de clave del solicitante (destino) (KCI).
- Mantener el anonimato del solicitante
- Minimizar la sobrecarga criptográfica

### No Objetivos

- No cambiar las propiedades de cifrado o seguridad de la búsqueda (DLM).
  La búsqueda tiene secreto hacia adelante sólo para compromiso de clave del solicitante.
  El cifrado es para la clave estática del floodfill.
- No hay problemas de secreto hacia adelante o autenticación del remitente resistentes a la
  suplantación por compromiso de clave del respondedor (floodfill) (KCI).
  El floodfill es una base de datos pública y responderá a búsquedas
  de cualquiera.
- No diseñar enrutadores ECIES en esta propuesta.
  Dónde va la clave pública X25519 de un enrutador está por definirse.


## Alternativas

En ausencia de una forma definida de cifrar respuestas a destinos ECIES, hay varias alternativas:

1) No solicitar respuestas cifradas. Las respuestas estarán sin cifrar.
Java I2P utiliza actualmente este enfoque.

2) Agregar soporte para etiquetas de 32 bytes y respuestas cifradas con AES a destinos solo ECIES,
y solicitar respuestas cifradas con AES como de costumbre. i2pd utiliza actualmente este enfoque.

3) Solicitar respuestas cifradas con AES como de costumbre, pero redirigirlas a través de
túneles exploratorios al enrutador.
Java I2P utiliza actualmente este enfoque en algunos casos.

4) Para destinos duales ElG y ECIES,
solicitar respuestas cifradas con AES como de costumbre. Java I2P utiliza actualmente este enfoque.
i2pd aún no ha implementado destinos de criptografía dual.


## Diseño

- El nuevo formato DLM añadirá un bit al campo de banderas para especificar respuestas cifradas con ECIES.
  Las respuestas cifradas con ECIES utilizarán el formato de mensaje de Sesión Existente [ECIES](/docs/specs/ecies/),
  con una etiqueta antepuesta y un payload y MAC ChaCha/Poly.

- Definir dos variantes. Una para enrutadores ElG, donde una operación DH no es posible,
  y una para futuros enrutadores ECIES, donde una operación DH es posible y puede proporcionar
  seguridad adicional. Para estudios futuros.

DH no es posible para respuestas de enrutadores ElG porque no publican
una clave pública X25519.


## Especificación

En la especificación DLM (DatabaseLookup) de [I2NP](/docs/specs/i2np/), realizar los siguientes cambios.


Agregar el bit de bandera 4 "ECIESFlag" para las nuevas opciones de cifrado.

```text
flags ::
       bit 4: ECIESFlag
               antes de la versión 0.9.46 ignorado
               a partir de la versión 0.9.46:
               0  => enviar respuesta sin cifrar o con ElGamal
               1  => enviar respuesta cifrada con ChaCha/Poly utilizando la clave incluida
                     (si la etiqueta está incluida depende del bit 1)
```

El bit de bandera 4 se utiliza en combinación con el bit 1 para determinar el modo de cifrado de la respuesta.
El bit de bandera 4 solo debe configurarse al enviar a enrutadores con versión 0.9.46 o superior.

En la tabla a continuación,
"DH n/a" significa que la respuesta no está cifrada.
"DH no" significa que las claves de respuesta están incluidas en la solicitud.
"DH yes" significa que las claves de respuesta se derivan de la operación DH.


| Flag bits 4,1 | Desde Dest | A Enrutador | Respuesta | DH? | notas |
|---------------|------------|-------------|-----------|-----|-------|
| 0 0            | Cualquiera | Cualquiera  | sin cifrar| n/a | actual |
| 0 1            | ElG        | ElG         | AES       | no  | actual |
| 0 1            | ECIES      | ElG         | AES       | no  | solución i2pd |
| 1 0            | ECIES      | ElG         | AEAD      | no  | esta propuesta |
| 1 0            | ECIES      | ECIES       | AEAD      | no  | 0.9.49 |
| 1 1            | ECIES      | ECIES       | AEAD      | sí  | futuro |


### ElG a ElG

_destino ElG_ envía una búsqueda a un _enrutador ElG_.

Cambios menores en la especificación para verificar el nuevo bit 4.
Sin cambios en el formato binario existente.


Generación de clave del solicitante (aclaración):

```text
reply_key :: CSRNG(32) 32 bytes de datos aleatorios
  reply_tags :: Cada uno es CSRNG(32) 32 bytes de datos aleatorios
```

Formato del mensaje (agregar verificación para ECIESFlag):

```text
reply_key ::
       `SessionKey` de 32 bytes, big-endian
       solo incluido si encryptionFlag == 1 Y ECIESFlag == 0, solo a partir de la versión 0.9.7

  tags ::
       `Integer` de 1 byte
       rango válido: 1-32 (normalmente 1)
       el número de etiquetas de respuesta que siguen
       solo incluido si encryptionFlag == 1 Y ECIESFlag == 0, solo a partir de la versión 0.9.7

  reply_tags ::
       una o más `SessionTag`s de 32 bytes (normalmente una)
       solo incluido si encryptionFlag == 1 Y ECIESFlag == 0, solo a partir de la versión 0.9.7
```


### ECIES a ElG

_destino ECIES_ envía una búsqueda a un _enrutador ElG_.
Soportado a partir de la 0.9.46.

Los campos reply_key y reply_tags están redefinidos para una respuesta cifrada con ECIES.

Generación de clave del solicitante:

```text
reply_key :: CSRNG(32) 32 bytes de datos aleatorios
  reply_tags :: Cada uno es CSRNG(8) 8 bytes de datos aleatorios
```

Formato del mensaje:
Redefinir los campos reply_key y reply_tags de la siguiente manera:

```text
reply_key ::
       `SessionKey` ECIES de 32 bytes, big-endian
       solo incluido si encryptionFlag == 0 Y ECIESFlag == 1, solo a partir de la versión 0.9.46

  tags ::
       `Integer` de 1 byte
       valor requerido: 1
       el número de etiquetas de respuesta que siguen
       solo incluida si encryptionFlag == 0 Y ECIESFlag == 1, solo a partir de la versión 0.9.46

  reply_tags ::
       un `SessionTag` ECIES de 8 bytes
       solo incluida si encryptionFlag == 0 Y ECIESFlag == 1, solo a partir de la versión 0.9.46
```


La respuesta es un mensaje de Sesión Existente ECIES, como se define en [ECIES](/docs/specs/ecies/).

```text
tag :: etiqueta de respuesta de 8 bytes

  k :: clave de sesión de 32 bytes
     La reply_key.

  n :: 0

  ad :: La etiqueta de respuesta de 8 bytes

  payload :: Datos en texto claro, el DSM o DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### ECIES a ECIES (0.9.49)

_destino ECIES_ o _enrutador_ envía una búsqueda a un _enrutador ECIES_, con claves de respuesta incluidas.
Soportado a partir de la 0.9.49.

Los enrutadores ECIES se introdujeron en la 0.9.48, véase [Prop156](/proposals/156-ecies-routers/).
A partir de la 0.9.49, los destinos y enrutadores ECIES pueden utilizar el mismo formato que en
la sección "ECIES a ElG" arriba, con claves de respuesta incluidas en la solicitud.
La búsqueda utilizará el "formato de una sola vez" en [ECIES](/docs/specs/ecies/)
ya que el solicitante es anónimo.

Para un nuevo método con claves derivadas, véase la siguiente sección.


### ECIES a ECIES (futuro)

_destino ECIES_ o _enrutador_ envía una búsqueda a un _enrutador ECIES_, y las claves de respuesta se derivan de la DH.
No está completamente definido o soportado, su implementación está por definirse.

La búsqueda utilizará el "formato de una sola vez" en [ECIES](/docs/specs/ecies/)
ya que el solicitante es anónimo.

Redefinir el campo reply_key de la siguiente manera. No hay etiquetas asociadas.
Las etiquetas serán generadas en el KDF a continuación.

Esta sección está incompleta y requiere más estudio.


```text
reply_key ::
       `PublicKey` X25519 efímero de 32 bytes del solicitante, little-endian
       solo incluido si encryptionFlag == 1 Y ECIESFlag == 1, solo a partir de la versión 0.9.TBD
```

La respuesta es un mensaje de Sesión Existente ECIES, como se define en [ECIES](/docs/specs/ecies/).
Ver [ECIES](/docs/specs/ecies/) para todas las definiciones.


```text
// Claves efímeras X25519 de Alice
  // aesk = clave privada efímera de Alice
  aesk = GENERATE_PRIVATE()
  // aepk = clave pública efímera de Alice
  aepk = DERIVE_PUBLIC(aesk)
  // Claves estáticas X25519 de Bob
  // bsk = clave privada estática de Bob
  bsk = GENERATE_PRIVATE()
  // bpk = clave pública estática de Bob
  // bpk es parte de RouterIdentity o se publica en RouterInfo (por definir)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey de ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chainKey de la Sección de Payload
  2) k de la Nueva Sesión KDF o split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Salida 1: no utilizada
  unused = keydata[0:31]
  // Salida 2: La chain key para inicializar el nuevo
  // ratchet de etiqueta de sesión y clave simétrica
  // para transmisiones de Alice a Bob
  ck = keydata[32:63]

  // claves de cadena de etiqueta de sesión y clave simétrica
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: etiqueta de 8 bytes como se genera de RATCHET_TAG() en [ECIES](/docs/specs/ecies/)

  k :: clave de 32 bytes como se genera de RATCHET_KEY() en [ECIES](/docs/specs/ecies/)

  n :: El índice de la etiqueta. Normalmente 0.

  ad :: La etiqueta de 8 bytes

  payload :: Datos en texto claro, el DSM o DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```


### Formato de respuesta

Este es el mensaje de sesión existente,
igual que en [ECIES](/docs/specs/ecies/), copiado abajo como referencia.

```text
+----+----+----+----+----+----+----+----+
  |       Etiqueta de Sesión               |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sección de Payload         +
  |       Datos cifrados con ChaCha20     |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Código de autenticación de mensaje Poly1305 |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Etiqueta de Sesión :: 8 bytes, texto claro

  Datos cifrados de Sección de Payload :: datos restantes menos 16 bytes

  MAC :: Código de autenticación de mensaje Poly1305, 16 bytes
```


## Justificación

Los parámetros de cifrado de la respuesta en la búsqueda, introducidos por primera vez en la 0.9.7, 
son algo de una violación de capas. Se hace de esta manera por eficiencia.
Pero también porque la búsqueda es anónima.

Podríamos hacer que el formato de búsqueda sea genérico, como con un campo de tipo de cifrado,
pero probablemente eso sea más problemático de lo que vale.

La propuesta anterior es la más sencilla y minimiza el cambio al formato de búsqueda.


## Notas

Las búsquedas y almacenes de base de datos en enrutadores ElG deben estar cifrados con ElGamal/AESSessionTag
como de costumbre.


## Issues

Se requiere un análisis adicional sobre la seguridad de las dos opciones de respuesta ECIES.


## Migración

No hay problemas de compatibilidad retroactiva. Los enrutadores que publiciten una router.version de 0.9.46 o superior
en su RouterInfo deben soportar esta función.
Los enrutadores no deben enviar un DatabaseLookup con las nuevas banderas a enrutadores con una versión inferior a 0.9.46.
Si un mensaje de búsqueda en la base de datos con el bit 4 configurado y el bit 1 sin configurar se envía por error a
un enrutador sin soporte, probablemente ignora la clave y etiqueta suministradas, y
envía la respuesta sin cifrar.
