---
title: "Encriptación de Capa de Túnel ChaCha"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Abierto"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Resumen

Esta propuesta se basa en y requiere los cambios de la propuesta 152: Túneles ECIES.

Solo los túneles construidos a través de saltos que soporten el formato BuildRequestRecord para túneles ECIES-X25519
pueden implementar esta especificación.

Esta especificación requiere el formato de Opciones de Construcción de Túnel para indicar
el tipo de encriptación de capa de túnel, y la transmisión de claves AEAD de capa.

### Objetivos

Los objetivos de esta propuesta son:

- Reemplazar AES256/ECB+CBC con ChaCha20 para el IV y encriptación de capa de túnel establecidos
- Usar ChaCha20-Poly1305 para protección AEAD entre saltos
- Ser indetectable de la encriptación de capa de túnel existente por no participantes del túnel
- No hacer cambios a la longitud total del mensaje del túnel

### Procesamiento de Mensajes de Túnel Establecido

Esta sección describe cambios en:

- Preprocesamiento + encriptación de Entrada y Salida del Gateway
- Encriptación de Participante + postprocesamiento
- Encriptación de Punto Final de Entrada y Salida + postprocesamiento

Para una descripción general del procesamiento actual de mensajes de túnel, consulte la especificación [Tunnel Implementation](/docs/specs/implementation/).

Solo se discuten cambios para enrutadores que soporten la encriptación de capa ChaCha20.

No se consideran cambios para túneles mixtos con encriptación de capa AES, hasta que se pueda idear un protocolo seguro
para convertir un IV AES de 128 bits en un nonce ChaCha20 de 64 bits. Los filtros de Bloom garantizan la unicidad
para el IV completo, pero la primera mitad de IVs únicos podría ser idéntica.

Esto significa que la encriptación de capa debe ser uniforme para todos los saltos en el túnel, y debe establecerse utilizando
opciones de construcción de túnel durante el proceso de creación del túnel.

Todos los gateways y participantes del túnel necesitarán mantener un filtro de Bloom para validar los dos nonces independientes.

El ``nonceKey`` mencionado en toda esta propuesta reemplaza al ``IVKey`` utilizado en la encriptación de capa AES.
Se genera utilizando el mismo KDF de la propuesta 152.

### Encriptación AEAD de Mensajes de Salto a Salto

Será necesario generar un ``AEADKey`` adicional único para cada par de saltos consecutivos.
Esta clave será utilizada por los saltos consecutivos para encriptar y desencriptar mediante ChaCha20-Poly1305
el mensaje interno del túnel encriptado con ChaCha20.

Los mensajes del túnel deberán reducir la longitud del marco interno encriptado en 16 bytes para
acomodar el MAC de Poly1305.

AEAD no puede ser utilizado directamente en los mensajes, ya que se necesita desencriptación iterativa por los túneles salientes.
La desencriptación iterativa solo se puede lograr, de la manera en que se utiliza ahora, usando ChaCha20 sin AEAD.

```text
+----+----+----+----+----+----+----+----+
  |    ID del Túnel      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | tunnelNonce cont. |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  |  obfsNonce cont.  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Datos Encriptados           +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  ID del Túnel :: `TunnelId`
         4 bytes
         el ID del siguiente salto

  tunnelNonce ::
         8 bytes
         el nonce de capa del túnel

  obfsNonce ::
         8 bytes
         el nonce de encriptación de capa del túnel

  Datos Encriptados ::
         992 bytes
         el mensaje del túnel encriptado

  Poly1305 MAC ::
         16 bytes

  tamaño total: 1028 Bytes
```

Los saltos internos (con saltos precedentes y siguientes), tendrán dos ``AEADKeys``, uno para desencriptar
la capa AEAD del salto anterior, y encriptar la capa AEAD al salto siguiente.

Todos los participantes internos del salto tendrán así 64 bytes adicionales de material de clave incluidos en sus BuildRequestRecords.

El Punto Final de Salida y el Gateway de Entra solamente requerirán 32 bytes adicionales de datos de clave,
ya que no encriptan mensajes de capa de túnel entre sí.

El Gateway de Salida genera su clave ``outAEAD``, que es la misma que la clave ``inAEAD`` del primer
salto saliente.

El Punto Final de Entrada genera su clave ``inAEAD``, que es la misma que la clave ``outAEAD`` del último
salto entrante.

Los saltos internos recibirán una ``inAEADKey`` y una ``outAEADKey`` que se usarán para desencriptar
mensajes entrantes y encriptar mensajes salientes, respectivamente.

Como ejemplo, en un túnel con saltos internos OBGW, A, B, OBEP:

- La ``inAEADKey`` de A es la misma que la ``outAEADKey`` de OBGW
- La ``inAEADKey`` de B es la misma que la ``outAEADKey`` de A
- La ``outAEADKey`` de B es la misma que la ``inAEADKey`` de OBEP

Las claves son únicas para los pares de saltos, por lo que la ``inAEADKey`` de OBEP será diferente a la ``inAEADKey`` de A,
la ``outAEADKey`` de A diferente a la ``outAEADKey`` de B, etc.

### Procesamiento de Mensajes del Creador del Túnel y del Gateway

Los gateways fragmentarán y agruparán mensajes de la misma manera, reservando espacio después del marco de instrucciones-fragmento para el MAC de Poly1305.

Los mensajes internos de I2NP que contengan marcos AEAD (incluyendo el MAC) pueden dividirse en fragmentos,
pero cualquier fragmento perdido resultará en una desencriptación AEAD fallida (fallo en la verificación del MAC) en el
punto final.

### Preprocesamiento y Encriptación del Gateway

Cuando los túneles soporten encriptación de capa ChaCha20, los gateways generarán dos nonces de 64 bits por conjunto de mensajes.

Túneles de entrada:

- Encriptar el IV y el(los) mensaje(s) del túnel usando ChaCha20
- Usar ``tunnelNonce`` y ``obfsNonce`` de 8 bytes dado el tiempo de vida de los túneles
- Usar ``obfsNonce`` de 8 bytes para la encriptación del ``tunnelNonce``
- Destruir el túnel antes de 2^(64 - 1) - 1 conjuntos de mensajes: 2^63 - 1 = 9,223,372,036,854,775,807

  - Límite de nonce para evitar colisión de los nonces de 64 bits
  - Límite de nonce casi imposible de alcanzar, dado que esto sería más de ~15,372,286,728,091,294 msgs/segundo para túneles de 10 minutos

- Ajustar el filtro de Bloom basado en un número razonable de elementos esperados (¿128 msgs/seg, 1024 msgs/seg? TBD)

El Gateway de Entrada del túnel (IBGW), procesa los mensajes recibidos de la Salida del Endpoint de otro túnel (OBEP).

En este punto, la capa de mensaje más externa está encriptada usando encriptación de transporte punto a punto.
Las cabeceras de los mensajes I2NP son visibles, en la capa de túnel, para el OBEP y el IBGW.
Los mensajes internos de I2NP están envueltos en dientes de Ajo, encriptados usando encriptación de sesión de extremo a extremo.

El IBGW preprocesa los mensajes en los mensajes de túnel con el formato apropiado, y los encripta de la siguiente manera:

```text

// IBGW genera nonces aleatorios, asegurando que no haya colisión en su filtro de Bloom para cada nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW "encripta" ChaCha20 cada uno de los mensajes de túnel preprocesados con su tunnelNonce y layerKey
  encMsg = ChaCha20(msg = mensaje de túnel, nonce = tunnelNonce, key = layerKey)

  // Encriptar ChaCha20-Poly1305 cada marco de datos encriptados del mensaje con el tunnelNonce y outAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

El formato del mensaje de túnel cambiará ligeramente, usando dos nonces de 8 bytes en lugar de un IV de 16 bytes.
El ``obfsNonce`` utilizado para encriptar el nonce se adjunta al ``tunnelNonce`` de 8 bytes,
y es encriptado por cada salto usando el ``tunnelNonce`` encriptado y el ``nonceKey`` del salto.

Después de que el conjunto de mensajes haya sido pre-eminentemente desencriptado para cada salto, el Gateway
ChaCha20-Poly1305 AEAD encripta la parte de texto cifrado de cada mensaje de túnel usando
el ``tunnelNonce`` y su ``outAEADKey``.

Túneles de salida:

- Desencriptar mensajes de túnel de manera iterativa
- Encriptar ChaCha20-Poly1305 marcos de mensajes de túnel desencriptados preeminentemente
- Usar las mismas reglas para nonces de capa que los Túneles de Entrada
- Generar nonces aleatorios una vez por conjunto de mensajes de túnel enviados

```text


// Para cada conjunto de mensajes, generar nonces únicos y aleatorios
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Para cada salto, encriptar ChaCha20 el tunnelNonce anterior con la clave IV del salto actual
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = clave del nonce del salto)

  // Para cada salto, desencriptar ChaCha20 el mensaje del túnel con el tunnelNonce y layerKey del salto actual
  decMsg = ChaCha20(msg = mensaje del túnel, nonce = tunnelNonce, key = layerKey del salto)

  // Para cada salto, desencriptar ChaCha20 la obfsNonce con el tunnelNonce encriptado del salto actual y nonceKey
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey del salto)

  // Después del procesamiento del salto, encriptar ChaCha20-Poly1305 cada marco de datos desencriptados del mensaje del túnel con el tunnelNonce encriptado del primer salto y inAEADKey
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = tunnelNonce encriptado del primer salto, key = inAEADKey del primer salto / outAEADKey del Gateway)
```

### Procesamiento de Participantes

Los participantes rastrearán mensajes vistos de la misma manera, usando filtros de Bloom decadentes.

Los nonces de túnel deberán ser encriptados una vez por salto, para prevenir ataques de confirmación
por saltos colusorios no consecutivos.

Los saltos encriptarán el nonce recibido para prevenir ataques de confirmación entre saltos anteriores y posteriores,
es decir, saltos colusorios no consecutivos siendo capaces de decir que pertenecen al mismo túnel.

Para validar el ``tunnelNonce`` y ``obfsNonce`` recibidos, los participantes revisan cada nonce individualmente
contra su filtro de Bloom para duplicados.

Después de la validación, el participante:

- Desencripta ChaCha20-Poly1305 el texto cifrado AEAD de cada mensaje del túnel con el ``tunnelNonce`` recibido y su ``inAEADKey``
- Encripta ChaCha20 el ``tunnelNonce`` con su ``nonceKey`` y ``obfsNonce`` recibido
- Encripta ChaCha20 cada marco de datos cifrados del mensaje de túnel con el ``tunnelNonce`` encriptado y su ``layerKey``
- Encripta ChaCha20-Poly1305 cada marco de datos cifrados del mensaje de túnel con el ``tunnelNonce`` encriptado y su ``outAEADKey``
- Encripta ChaCha20 el ``obfsNonce`` con su ``nonceKey`` y ``tunnelNonce`` encriptado
- Envía el tupla {``nextTunnelId``, encriptado (``tunnelNonce`` || ``obfsNonce``), texto cifrado AEAD || MAC} al siguiente salto.

```text

// Para verificación, los saltos del túnel deben comprobar la unicidad de cada nonce recibido en el filtro de Bloom 
  // Después de la verificación, desenvuelva el/los marco(s) AEAD desencriptando ChaCha20-Poly1305 cada marco encriptado del mensaje del túnel 
  // con el tunnelNonce recibido y inAEADKey 
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = encMsg recibido \|\| MAC, nonce = tunnelNonce recibido, key = inAEADKey)

  // Encripta ChaCha20 el tunnelNonce con el obfsNonce y la nonceKey del salto
  tunnelNonce = ChaCha20(msg = tunnelNonce recibido, nonce = obfsNonce recibido, key = nonceKey)

  // Encripta ChaCha20 cada marco de datos cifrados del mensaje del túnel con el tunnelNonce encriptado y la layerKey del salto
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Para la protección AEAD, también encripta ChaCha20-Poly1305 cada marco de datos cifrados de los mensajes
  // con el tunnelNonce encriptado y el outAEADKey del salto
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // Encripta ChaCha20 el obfsNonce recibido con el tunnelNonce encriptado y la nonceKey del salto
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Procesamiento de Punto Final de Entrada

Para túneles ChaCha20, se usará el siguiente esquema para desencriptar cada mensaje del túnel:

- Validar el ``tunnelNonce`` y ``obfsNonce`` recibidos de manera independiente contra su filtro de Bloom
- Desencriptar ChaCha20-Poly1305 el marco de datos cifrados usando el ``tunnelNonce`` recibido y ``inAEADKey``
- Desencriptar ChaCha20 el marco de datos cifrados usando el ``tunnelNonce`` recibido y la ``layerKey`` del salto
- Desencriptar ChaCha20 el ``obfsNonce`` usando el ``nonceKey`` del salto y el ``tunnelNonce`` recibido para obtener el ``obfsNonce`` previo
- Desencriptar ChaCha20 el ``tunnelNonce`` recibido usando el ``nonceKey`` del salto y el ``obfsNonce`` desencriptado para obtener el ``tunnelNonce`` previo
- Desencriptar ChaCha20 los datos encriptados usando el ``tunnelNonce`` desencriptado y la ``layerKey`` del salto previo
- Repetir los pasos para la desencriptación de nonce y capa para cada salto en el túnel, de regreso al IBGW
- La desencriptación del marco AEAD solo se necesita en la primera ronda

```text

// Para la primera ronda, desencripta ChaCha20-Poly1305 cada dato cifrado del mensaje + MAC 
  // usando el tunnelNonce recibido y inAEADKey 
  msg = encTunMsg \|\| MAC
  tunnelNonce = tunnelNonce recibido
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Repetir para cada salto en el túnel de regreso al IBGW 
  // Para cada ronda, desencripta ChaCha20 cada capa de encriptación de cada mensaje cifrado del marco de datos 
  // Reemplaza el tunnelNonce recibido con el tunnelNonce desencriptado de la ronda previa para cada salto 
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Análisis de Seguridad para la Encriptación de Capa de Túnel ChaCha20+ChaCha20-Poly1305

Cambiar de AES256/ECB+AES256/CBC a ChaCha20+ChaCha20-Poly1305 tiene varias ventajas, y nuevas consideraciones de seguridad.

Las principales consideraciones de seguridad a tener en cuenta, son que los nonces ChaCha20 y ChaCha20-Poly1305 deben ser únicos por mensaje,
durante la vida de la clave que se utiliza.

No usar nonces únicos con la misma clave en diferentes mensajes rompe ChaCha20 y ChaCha20-Poly1305.

Usar un ``obfsNonce`` adjunto permite al IBEP desencriptar el ``tunnelNonce`` para la encriptación de capa de cada salto,
recuperando el nonce previo.

El ``obfsNonce`` junto al ``tunnelNonce`` no revela ninguna información nueva a los saltos del túnel,
ya que el ``obfsNonce`` está encriptado usando el ``tunnelNonce`` encriptado. Esto también permite al IBEP recuperar
el ``obfsNonce`` previo de manera similar a la recuperación del ``tunnelNonce``.

La mayor ventaja de seguridad es que no hay ataques de confirmación u oráculo contra ChaCha20,
y usar ChaCha20-Poly1305 entre saltos agrega protección AEAD contra la manipulación de texto cifrado por
atacantes MitM fuera de banda.

Existen ataques prácticos de oráculo contra AES256/ECB + AES256/CBC, cuando se reutiliza la clave (como en la encriptación de capa de túnel).

Los ataques de oráculo contra AES256/ECB no funcionarán, debido a la doble encriptación utilizada, y la encriptación es sobre un
bloque único (el IV del túnel).

Los ataques de oráculo de relleno contra AES256/CBC no funcionarán, porque no se usa relleno. Si la longitud del mensaje del túnel cambiara alguna vez a longitudes no mod-16, AES256/CBC aún no sería vulnerable debido a que los IVs duplicados son rechazados.

Ambos ataques también se bloquean al no permitir múltiples llamadas de oráculo utilizando el mismo IV, ya que los IVs duplicados son rechazados.

## Referencias

* [Tunnel-Implementation](/docs/specs/implementation/)
