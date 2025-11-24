---
title: "Mensajes de Construcción de Túneles Más Pequeños"
number: "157"
author: "zzz, original"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Closed"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
---

## Nota
Implementado desde la versión API 0.9.51.
Despliegue y prueba de red en progreso.
Sujeto a revisiones menores.
Ver [I2NP](/en/docs/spec/i2np/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) para la especificación final.



## Visión General


### Resumen

El tamaño actual de los registros de Solicitud y Respuesta de Construcción de Túneles cifrados es 528.
Para los mensajes típicos de Construcción de Túneles Variables y Respuesta de Construcción de Túneles Variables,
el tamaño total es de 2113 bytes. Este mensaje se fragmenta en tres mensajes de túnel de 1KB para el camino inverso.

Los cambios al formato de registro de 528 bytes para los enrutadores ECIES-X25519 se especifican en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).
Para una mezcla de enrutadores ElGamal y ECIES-X25519 en un túnel, el tamaño del registro debe permanecer
en 528 bytes. Sin embargo, si todos los enrutadores en un túnel son ECIES-X25519, es posible un nuevo registro de construcción más pequeño, ya que el cifrado ECIES-X25519 tiene mucho menos sobrecarga que ElGamal.

Mensajes más pequeños ahorrarían ancho de banda. Además, si los mensajes pudieran caber en un
único mensaje de túnel, el camino inverso sería tres veces más eficiente.

Esta propuesta define nuevos registros de solicitud y respuesta y nuevos mensajes de Solicitud de Construcción y Respuesta de Construcción.

El creador del túnel y todos los saltos en el túnel creado deben ser ECIES-X25519 y al menos versión 0.9.51.
Esta propuesta no será útil hasta que la mayoría de los enrutadores en la red sean ECIES-X25519.
Se espera que esto suceda para finales de 2021.


### Objetivos

Ver [Prop152](/en/proposals/152-ecies-tunnels/) y [Prop156](/en/proposals/156-ecies-routers/) para objetivos adicionales.

- Registros y mensajes más pequeños
- Mantener suficiente espacio para futuras opciones, como en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Ajustarse en un solo mensaje de túnel para el camino inverso
- Soportar solo saltos ECIES
- Mantener mejoras implementadas en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)
- Maximizar la compatibilidad con la red actual
- Ocultar mensajes de construcción entrantes del OBEP
- Ocultar mensajes de respuesta de construcción salientes del IBGW
- No requerir actualización de "día de cambios" para toda la red
- Despliegue gradual para minimizar riesgos
- Reutilizar primitivas criptográficas existentes


### No Objetivos

Ver [Prop156](/en/proposals/156-ecies-routers/) para no objetivos adicionales.

- Sin requisito para túneles mixtos ElGamal/ECIES
- Cambios en el cifrado de capa, para eso ver [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- Sin aceleraciones de operaciones criptográficas. Se asume que ChaCha20 y AES son similares,
  incluso con AESNI, al menos para los pequeños tamaños de datos en cuestión.


## Diseño


### Registros

Ver apéndice para cálculos.

Los registros de solicitud y respuesta cifrados serán de 218 bytes, comparados con 528 bytes ahora.

Los registros de solicitud en texto claro serán de 154 bytes,
comparados con 222 bytes para registros ElGamal,
y 464 bytes para registros ECIES como se define en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Los registros de respuesta en texto claro serán de 202 bytes,
comparados con 496 bytes para registros ElGamal,
y 512 bytes para registros ECIES como se define en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

El cifrado de respuesta será ChaCha20 (NO ChaCha20/Poly1305),
por lo que los registros de texto claro no necesitan ser múltiplos de 16 bytes.

Los registros de solicitud se harán más pequeños al usar HKDF para crear las
claves de capa y de respuesta, por lo que no necesitan ser incluidas explícitamente en la solicitud.


### Mensajes de Construcción de Túneles

Ambos serán "variables" con un campo de número de registros de un byte,
como con los mensajes Variables existentes.

ShortTunnelBuild: Tipo 25
````````````````````````````````

Longitud típica (con 4 registros): 873 bytes

Cuando se usa para construcciones de túneles entrantes,
se recomienda (pero no es obligatorio) que este mensaje sea cifrado con ajo por el originador,
dirigiéndose a la puerta de enlace entrante (instrucciones de entrega ROUTER),
para ocultar mensajes de construcción entrantes del OBEP.
El IBGW descifra el mensaje,
coloca la respuesta en la ranura correcta,
y envía el ShortTunnelBuildMessage al siguiente salto.

La longitud del registro se selecciona para que un STBM cifrado con ajo quepa
en un único mensaje de túnel. Vea el apéndice a continuación.

OutboundTunnelBuildReply: Tipo 26
``````````````````````````````````````

Definimos un nuevo mensaje de OutboundTunnelBuildReply.
Este se usa solo para construcciones de túneles salientes.
El propósito es ocultar mensajes de respuesta de construcción salientes del IBGW.
Debe ser cifrado con ajo por el OBEP, dirigiéndose al originador
(instrucciones de entrega TUNNEL).
El OBEP descifra el mensaje de construcción del túnel,
construye un mensaje OutboundTunnelBuildReply,
y coloca la respuesta en el campo de texto claro.
Los otros registros se colocan en las otras ranuras.
Luego cifra con ajo el mensaje al originador con las claves simétricas derivadas.

Notas
```````

Al cifrar con ajo el OTBRM y el STBM, también evitamos cualquier posible
problema de compatibilidad en el IBGW y OBEP de los túneles emparejados.


### Flujo de Mensajes


  {% highlight %}
STBM: Mensaje de construcción de túnel corto (tipo 25)
  OTBRM: Mensaje de respuesta de construcción de túnel saliente (tipo 26)

  Construcción de salida A-B-C
  Responder a través del túnel entrante existente D-E-F


                  Nuevo Túnel
           STBM      STBM      STBM
  Creador ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | Envoltura de ajo
                                            | OTBRM
                                            | (Entrega de TUNNEL)
                                            | del OBEP al
                                            | creador
                Túnel existente             /
  Creador <-------F---------E-------- D <--/
                                     IBGW



  Construcción de entrada D-E-F
  Enviado a través del túnel de salida existente A-B-C


                Túnel existente
  Creador ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | Envoltura de ajo (opcional)
                                            | STBM
                                            | (Entrega de ROUTER)
                                            | del creador
                  Nuevo Túnel                | al IBGW
            STBM      STBM      STBM        /
  Creador <------ F <------ E <------ D <--/
                                     IBGW



{% endhighlight %}



### Cifrado de Registro

Cifrado de registro de solicitud y respuesta: como se define en [Prop152](/en/proposals/152-ecies-tunnels/) y [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/).

Cifrado de registro de respuesta para otras ranuras: ChaCha20.


### Cifrado de Capa

Actualmente no hay planes para cambiar el cifrado de capa para los túneles construidos con
esta especificación; seguiría siendo AES, como se usa actualmente en todos los túneles.

Cambiar el cifrado de capa a ChaCha20 es un tema para más investigación.



### Nuevo Mensaje de Datos de Túnel

Actualmente no hay planes para cambiar el Mensaje de Datos de Túnel de 1KB usado para los túneles construidos con
esta especificación.

Puede ser útil introducir un nuevo mensaje I2NP que sea más grande o de tamaño variable, concurrente con esta propuesta,
para su uso en estos túneles.
Esto reduciría la sobrecarga para mensajes grandes.
Esto es un tema para más investigación.




## Especificación


### Registro de Solicitud Corto



Registro de Solicitud Corto Sin Cifrar
```````````````````````````````````````

Esta es la especificación propuesta del registro de solicitud de construcción de túneles para los enrutadores ECIES-X25519.
Resumen de cambios de [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Cambiar longitud sin cifrar de 464 a 154 bytes
- Cambiar longitud cifrada de 528 a 218 bytes
- Eliminar claves de capa y de respuesta e IVs, se generarán a partir de split() y un KDF


El registro de solicitud no contiene ninguna clave de respuesta ChaCha.
Esas claves son derivadas de un KDF. Ver abajo.

Todos los campos son big-endian.

Tamaño sin cifrar: 154 bytes.


  {% highlight lang='dataspec' %}

bytes     0-3: ID del túnel para recibir mensajes, no cero
  bytes     4-7: ID del siguiente túnel, no cero
  bytes    8-39: hash de identidad del siguiente enrutador
  byte       40: banderas
  bytes   41-42: más banderas, sin uso, establecer en 0 para compatibilidad
  byte       43: tipo de cifrado de capa
  bytes   44-47: hora de solicitud (en minutos desde la época, redondeado hacia abajo)
  bytes   48-51: expiración de la solicitud (en segundos desde la creación)
  bytes   52-55: siguiente ID de mensaje
  bytes    56-x: opciones de construcción de túnel (Mapping)
  bytes     x-x: otros datos según lo implicado por banderas u opciones
  bytes   x-153: relleno aleatorio (ver abajo)

{% endhighlight %}


El campo de banderas es el mismo que se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/) y contiene lo siguiente::

 Orden de bits: 76543210 (el bit 7 es el MSB)
 bit 7: si está establecido, permitir mensajes de cualquiera
 bit 6: si está establecido, permitir mensajes a cualquiera, y enviar la respuesta al
        siguiente salto especificado en un mensaje de Respuesta de Construcción de Túnel
 bits 5-0: No Definidos, deben establecerse en 0 para compatibilidad con futuras opciones

El bit 7 indica que el salto será una puerta de enlace entrante (IBGW). El bit 6
indica que el salto será un punto final saliente (OBEP). Si ninguno de los bits está
está establecido, el salto será un participante intermedio. Ambos no pueden estar establecidos a la vez.

Tipo de cifrado de capa: 0 para AES (como en los túneles actuales);
1 para futuro (¿ChaCha?)

La expiración de la solicitud es para la duración variable futura del túnel.
Por ahora, el único valor soportado es 600 (10 minutos).

La clave pública efímera del creador es una clave ECIES, big-endian.
Se usa para el KDF para las claves y IVs de capa y respuesta del IBGW.
Esto solo se incluye en el registro de texto claro en un mensaje de Construcción de Túnel Entrante.
Es necesario porque no hay DH en esta capa para el registro de construcción.

Las opciones de construcción de túnel son una estructura Mapping como se define en [Common](/en/docs/spec/common-structures/).
Esto es para uso futuro. Actualmente no se definen opciones.
Si la estructura Mapping está vacía, estos son dos bytes 0x00 0x00.
El tamaño máximo del Mapping (incluyendo el campo de longitud) es 98 bytes,
y el valor máximo del campo de longitud de Mapping es 96.



Registro de Solicitud Corto Cifrado
`````````````````````````````````````

Todos los campos son big-endian excepto la clave pública efímera que es little-endian.

Tamaño cifrado: 218 bytes


  {% highlight lang='dataspec' %}

bytes    0-15: hash truncado de identidad del salto
  bytes   16-47: Clave pública efímera X25519 del remitente
  bytes  48-201: ShortBuildRequestRecord cifrado con ChaCha20
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### Registro de Respuesta Corto


Registro de Respuesta Corto Sin Cifrar
`````````````````````````````````````
Esta es la especificación propuesta del registro de ShortBuildReply para los enrutadores ECIES-X25519.
Resumen de cambios de [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/):

- Cambiar longitud sin cifrar de 512 a 202 bytes
- Cambiar longitud cifrada de 528 a 218 bytes


Las respuestas ECIES se cifran con ChaCha20/Poly1305.

Todos los campos son big-endian.

Tamaño sin cifrar: 202 bytes.


  {% highlight lang='dataspec' %}

bytes    0-x: Opciones de Respuesta de Construcción de Túnel (Mapping)
  bytes    x-x: otros datos según lo implicado por las opciones
  bytes  x-200: Relleno aleatorio (ver abajo)
  byte     201: Byte de respuesta

{% endhighlight %}

Las opciones de respuesta de construcción de túnel son una estructura Mapping como se define en [Common](/en/docs/spec/common-structures/).
Esto es para uso futuro. Actualmente no se definen opciones.
Si la estructura Mapping está vacía, estos son dos bytes 0x00 0x00.
El tamaño máximo del Mapping (incluyendo el campo de longitud) es 201 bytes,
y el valor máximo del campo de longitud de Mapping es 199.

El byte de respuesta es uno de los siguientes valores
como se define en [Tunnel-Creation](/en/docs/spec/tunnel-creation/) para evitar la identificación:

- 0x00 (aceptar)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Registro de Respuesta Corto Cifrado
```````````````````````````````````

Tamaño cifrado: 218 bytes


  {% highlight lang='dataspec' %}

bytes   0-201: ShortBuildReplyRecord cifrado con ChaCha20
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### KDF

Ver sección KDF abajo.




### ShortTunnelBuild
I2NP Tipo 25

Este mensaje se envía a saltos intermedios, OBEP y IBEP (creador).
No puede enviarse al IBGW (usar Construcción de Túnel Entrante envuelto con ajo en su lugar).
Cuando lo recibe el OBEP, se transforma en un OutboundTunnelBuildReply,
envuelto con ajo, y se envía al originador.



  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 byte `Integer`
         Valores válidos: 1-8

  tamaño del registro: 218 bytes
  tamaño total: 1+$num*218
{% endhighlight %}

Notas
`````
* El número típico de registros es 4, para un tamaño total de 873.




### OutboundTunnelBuildReply
I2NP Tipo 26

Este mensaje solo se envía por el OBEP al IBEP (creador) a través de un túnel entrante existente.
No puede enviarse a ningún otro salto.
Siempre está cifrado con ajo.


  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         Número total de registros,
         1 byte `Integer`
         Valores válidos: 1-8

  ShortBuildReplyRecords ::
         Registros cifrados
         longitud: num * 218

  tamaño del registro cifrado: 218 bytes
  tamaño total: 1+$num*218
{% endhighlight %}

Notas
`````
* El número típico de registros es 4, para un tamaño total de 873.
* Este mensaje debe ser cifrado con ajo.



### KDF

Usamos ck del estado de Noise después del cifrado/descifrado de registros de construcción de túnel
para derivar las siguientes claves: clave de respuesta, clave de capa AES, clave de IV AES y clave/etiqueta de respuesta de ajo para OBEP.

Clave de respuesta:
A diferencia de los registros largos, no podemos usar la parte izquierda de ck para la clave de respuesta, porque no es la última y se usará después.
La clave de respuesta se usa para cifrar la respuesta de ese registro usando AEAD/ChaCha20/Poly1305 y ChaCha20 para responder a otros registros.
Ambos usan la misma clave, el nonce es la posición del registro en el mensaje comenzando desde 0.


  {% highlight lang='dataspec' %}
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  Clave de capa:
  La clave de capa siempre es AES por ahora, pero el mismo KDF puede ser usado para ChaCha20

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  Clave de IV para registros que no sean OBEP:
  ivKey = keydata[0:31]
  porque es la última

  Clave de IV para registro OBEP:
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  Clave/etiqueta de respuesta de ajo OBEP:
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

{% endhighlight %}





## Justificación

Este diseño maximiza la reutilización de primitivas criptográficas, protocolos y código existentes.

Este diseño minimiza el riesgo.

ChaCha20 es ligeramente más rápido que AES para registros pequeños, en pruebas de Java.
ChaCha20 evita un requisito para tamaños de datos múltiplos de 16.


## Notas de Implementación

- Al igual que con el mensaje de construcción de túnel variable existente,
  no se recomiendan mensajes de menos de 4 registros.
  El valor típico por defecto es 3 saltos.
  Los túneles entrantes deben construirse con un registro extra para
  que el último salto no sepa que es el último.
  Para que los saltos intermedios no sepan si un túnel es entrante o saliente,
  también deberían construirse túneles salientes con 4 registros.



## Problemas



## Migración

La implementación, pruebas, y despliegue tomará varias versiones
y aproximadamente un año. Las fases son las siguientes. La asignación de
cada fase a una versión particular se determinará y dependerá del
ritmo de desarrollo.

Los detalles de la implementación y migración pueden variar para
cada implementación de I2P.

El creador del túnel debe asegurar que todos los saltos en el túnel creado sean ECIES-X25519, Y sean al menos la versión TBD.
El creador del túnel NO tiene que ser ECIES-X25519; puede ser ElGamal.
Sin embargo, si el creador es ElGamal, revela al salto más cercano que es el creador.
Por lo tanto, en la práctica, estos túneles solo deberían ser creados por enrutadores ECIES.

No debería ser necesario que el OBEP o IBGW del túnel emparejado sea ECIES o
de ninguna versión en particular.
Los nuevos mensajes están envueltos con ajo y no son visibles en el OBEP o IBGW
del túnel emparejado.

Fase 1: Implementación, no habilitada por defecto

Fase 2 (próxima versión): Habilitar por defecto

No hay problemas de compatibilidad hacia atrás. Los nuevos mensajes solo pueden ser enviados a enrutadores que los soportan.




## Apéndice


Sin sobrecarga de ajo para STBM entrante no cifrado,
si no usamos ITBM:



  {% highlight lang='text' %}
Tamaño actual de 4 ranuras: 4 * 528 + sobrecarga = 3 mensajes de túnel

  Mensaje de construcción de 4 ranuras para ajustar en un mensaje de túnel, solo ECIES:

  1024
  - 21 encabezado de fragmento
  ----
  1003
  - 35 instrucciones de entrega no fragmentadas ROUTER
  ----
  968
  - 16 encabezado I2NP
  ----
  952
  - 1 número de ranuras
  ----
  951
  / 4 ranuras
  ----
  237 Nuevo tamaño de registro de construcción cifrado (vs. 528 ahora)
  - 16 hash truncado
  - 32 clave efímera
  - 16 MAC
  ----
  173 tamaño máximo de registro de construcción en texto claro (vs. 222 ahora)



{% endhighlight %}


Con sobrecarga de ajo para el patrón de ruido 'N' para cifrar STBM entrante,
si no usamos ITBM:


  {% highlight lang='text' %}
Tamaño actual de 4 ranuras: 4 * 528 + sobrecarga = 3 mensajes de túnel

  Mensaje de construcción de 4 ranuras cifrado con ajo para ajustar en un mensaje de túnel, solo ECIES:

  1024
  - 21 encabezado de fragmento
  ----
  1003
  - 35 instrucciones de entrega no fragmentadas ROUTER
  ----
  968
  - 16 encabezado I2NP
  -  4 longitud
  ----
  948
  - 32 bytes de clave efímera
  ----
  916
  - 7 bytes de bloque de DateTime
  ----
  909
  - 3 bytes de sobrecarga de bloque Garlic
  ----
  906
  - 9 bytes de encabezado I2NP
  ----
  897
  - 1 byte de instrucciones de entrega LOCAL de Garlic
  ----
  896
  - 16 bytes de Poly1305 MAC
  ----
  880
  - 1 número de ranuras
  ----
  879
  / 4 ranuras
  ----
  219 Nuevo tamaño de registro de construcción cifrado (vs. 528 ahora)
  - 16 hash truncado
  - 32 clave efímera
  - 16 MAC
  ----
  155 tamaño máximo de registro de construcción en texto claro (vs. 222 ahora)


{% endhighlight %}

Notas:

Tamaño actual de registro de construcción en texto claro antes de relleno no utilizado: 193

La eliminación del hash completo del enrutador y la generación HKDF de claves/IVs liberarían suficiente espacio para futuras opciones.
Si todo es HKDF, el espacio requerido en texto claro es de unos 58 bytes (sin ninguna opción).

El OTBRM envuelto con ajo será ligeramente más pequeño que el STBM envuelto con ajo,
porque las instrucciones de entrega son LOCAL no ROUTER,
no se incluye ningún bloque de DATETIME, y
usa una etiqueta de 8 bytes en lugar de la clave efímera de 32 bytes para un mensaje completo 'N'.




