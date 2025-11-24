---
title: "Mejoras en el Transporte IPv6"
number: "158"
author: "zzz, orignal"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Closed"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
---

## Nota
Implementación y prueba de la red en curso.
Sujeto a revisiones menores.


## Resumen

Esta propuesta es para implementar mejoras en los transportes SSU y NTCP2 para IPv6.


## Motivación

A medida que IPv6 crece en todo el mundo y los entornos solo IPv6 (especialmente en móviles) se vuelven más comunes, necesitamos mejorar nuestro soporte para IPv6 y eliminar las suposiciones de que todos los routers son compatibles con IPv4.



### Verificación de Conectividad

Al seleccionar pares para túneles, o al seleccionar rutas OBEP/IBGW para dirigir mensajes,
ayuda calcular si el router A puede conectarse al router B.
En general, esto significa determinar si A tiene capacidad de salida para un tipo de transporte y dirección (IPv4/v6) que coincide con una de las direcciones de entrada anunciadas de B.

Sin embargo, en muchos casos no sabemos las capacidades de A y tenemos que hacer suposiciones.
Si A está oculto o detrás de un cortafuegos, las direcciones no se publican, y no tenemos conocimiento directo, por lo que asumimos que es compatible con IPv4, y no con IPv6.
La solución es añadir dos nuevas "capacidades" o capacidades a la Información del Router para indicar la capacidad de salida para IPv4 e IPv6.


### Presentadores IPv6

Nuestras especificaciones [SSU](/en/docs/transport/ssu/) y [SSU-SPEC](/en/docs/spec/ssu/) contienen errores e inconsistencias sobre si los presentadores IPv6 son compatibles para presentaciones IPv4.
En cualquier caso, esto nunca se ha implementado ni en Java I2P ni en i2pd.
Esto necesita ser corregido.


### Presentaciones IPv6

Nuestras especificaciones [SSU](/en/docs/transport/ssu/) y [SSU-SPEC](/en/docs/spec/ssu/) dejan claro que
las presentaciones IPv6 no son compatibles.
Esto fue bajo la suposición de que IPv6 nunca está tras un cortafuegos.
Esto claramente no es cierto, y necesitamos mejorar el soporte para routers IPv6 tras un cortafuegos.


### Diagramas de Introducción

Leyenda: ----- es IPv4, ====== es IPv6

Actualmente solo IPv4:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


Introducción IPv4, presentador IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

Introducción IPv6, presentador IPv6


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

Introducción IPv6, presentador IPv4

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Diseño

Hay tres cambios que se implementarán.

- Añadir capacidades "4" y "6" a las capacidades de Dirección del Router para indicar soporte de salida IPv4 e IPv6
- Añadir soporte para presentaciones IPv4 a través de presentadores IPv6
- Añadir soporte para presentaciones IPv6 a través de presentadores IPv4 e IPv6



## Especificación

### Cap 4/6

Esto se implementó originalmente sin una propuesta formal, pero es necesario para presentaciones IPv6, así que lo incluimos aquí.
Ver también [CAPS](http://zzz.i2p/topics/3050).


Se definen dos nuevas capacidades "4" y "6".
Estas nuevas capacidades se añadirán a la propiedad "caps" en la Dirección del Router, no en las caps info del Router.
Actualmente no tenemos una propiedad "caps" definida para NTCP2.
Una dirección SSU con presentadores es, por definición, IPv4 en este momento. No soportamos presentación IPv6 en absoluto.
Sin embargo, esta propuesta es compatible con presentaciones IPv6. Ver abajo.

Además, un router puede soportar conectividad a través de una red superpuesta como I2P sobre Yggdrasil, pero no desea publicar una dirección, o esa dirección no tiene un formato estándar IPv4 o IPv6.
Este nuevo sistema de capacidades debería ser lo suficientemente flexible como para soportar también estas redes.

Definimos los siguientes cambios:

NTCP2: Agregar propiedad "caps"

SSU: Agregar soporte para una Dirección de Router sin un host o presentadores, para indicar soporte de salida
para IPv4, IPv6, o ambos.

Ambos transportes: Definir los siguientes valores de caps:

- "4": Soporte para IPv4
- "6": Soporte para IPv6

Se pueden soportar múltiples valores en una sola dirección. Ver abajo.
Al menos una de estas caps es obligatoria si no se incluye un valor de "host" en la Dirección del Router.
A lo sumo una de estas caps es opcional si se incluye un valor de "host" en la Dirección del Router.
Caps de transporte adicionales pueden ser definidos en el futuro para indicar soporte para redes superpuestas u otra conectividad.


#### Casos de uso y ejemplos

SSU:

SSU con host: 4/6 opcional, nunca más de uno.
Ejemplo: SSU caps="4" host="1.2.3.4" key=... port="1234"

SSU solo de salida para uno, el otro se publica: Solo caps, 4/6.
Ejemplo: SSU caps="6"

SSU con presentadores: nunca se combinan. Se requiere 4 o 6.
Ejemplo: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

SSU oculto: Solo caps, 4, 6, o 46. Se permite múltiple.
No es necesario tener dos direcciones, una con 4 y otra con 6.
Ejemplo: SSU caps="46"

NTCP2:

NTCP2 con host: 4/6 opcional, nunca más de uno.
Ejemplo: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

NTCP2 solo de salida para uno, el otro se publica: Caps, s, solo v, 4/6/y, se permite múltiple.
Ejemplo: NTCP2 caps="6" i=... s=... v="2"

NTCP2 oculto: Caps, s, solo v 4/6, se permite múltiple No es necesario tener dos direcciones, una con 4 y otra con 6.
Ejemplo: NTCP2 caps="46" i=... s=... v="2"



### Presentadores IPv6 para IPv4

Se requieren los siguientes cambios para corregir errores e inconsistencias en las especificaciones.
También hemos descrito esto como "parte 1" de la propuesta.

#### Cambios en la Especificación

[SSU](/en/docs/transport/ssu/) dice actualmente (notas IPv6):

IPv6 es soportado desde la versión 0.9.8. Las direcciones de retransmisión publicadas pueden ser IPv4 o IPv6, y la comunicación Alice-Bob puede ser a través de IPv4 o IPv6.

Añadir lo siguiente:

Aunque la especificación se cambió a partir de la versión 0.9.8, la comunicación Alice-Bob vía IPv6 no fue realmente soportada hasta la versión 0.9.50.
Las versiones anteriores de los routers Java publicaban erróneamente la capacidad 'C' para direcciones IPv6,
aunque en realidad no actuaban como un presentador vía IPv6.
Por lo tanto, los routers solo deberían confiar en la capacidad 'C' en una dirección IPv6 si la versión del router es 0.9.50 o superior.



[SSU-SPEC](/en/docs/spec/ssu/) dice actualmente (Solicitud de retransmisión):

La dirección IP solo se incluye si es diferente de la dirección y puerto de origen del paquete.
En la implementación actual, la longitud de IP es siempre 0 y el puerto es siempre 0,
y el receptor debe usar la dirección y puerto de origen del paquete.
Este mensaje puede enviarse a través de IPv4 o IPv6. Si es IPv6, Alice debe incluir su dirección IPv4 y puerto.

Añadir lo siguiente:

La IP y el puerto deben incluirse para introducir una dirección IPv4 al enviar este mensaje sobre IPv6.
Esto es soportado desde la versión 0.9.50.



### Presentaciones IPv6

Los tres mensajes de retransmisión de SSU (RelayRequest, RelayResponse, y RelayIntro) contienen campos de longitud de IP para indicar la longitud de la dirección IP (Alice, Bob, o Charlie) que seguirá.

Por lo tanto, no se requiere ningún cambio en el formato de los mensajes.
Solo cambios textuales en las especificaciones, indicando que se permiten direcciones IP de 16 bytes.

Los siguientes cambios son necesarios para las especificaciones.
También hemos descrito esto como "parte 2" de la propuesta.


#### Cambios en la Especificación

[SSU](/en/docs/transport/ssu/) dice actualmente (notas IPv6):

La comunicación Bob-Charlie y Alice-Charlie es solo a través de IPv4.

[SSU-SPEC](/en/docs/spec/ssu/) dice actualmente (Solicitud de retransmisión):

No hay planes para implementar retransmisión para IPv6.

Cambiar para decir:

La retransmisión para IPv6 es soportada desde la versión 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) dice actualmente (Respuesta de retransmisión):

La dirección IP de Charlie debe ser IPv4, ya que esa es la dirección a la que Alice enviará la Solicitud de Sesión después del Hole Punch. No hay planes para implementar retransmisión para IPv6.

Cambiar para decir:

La dirección IP de Charlie puede ser IPv4 o, desde la versión 0.9.xx, IPv6.
Esa es la dirección a la que Alice enviará la Solicitud de Sesión después del Hole Punch.
La retransmisión para IPv6 es soportada desde la versión 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) dice actualmente (Introducción de retransmisión):

La dirección IP de Alice siempre es de 4 bytes en la implementación actual, porque Alice está tratando de conectarse a Charlie vía IPv4.
Este mensaje debe enviarse a través de una conexión IPv4 establecida,
ya que esa es la única forma en que Bob conoce la dirección IPv4 de Charlie para volver a Alice en la Respuesta de Retransmisión.

Cambiar para decir:

Para IPv4, la dirección IP de Alice es siempre de 4 bytes, porque Alice está tratando de conectarse a Charlie vía IPv4.
Desde la versión 0.9.xx, IPv6 es soportado, y la dirección IP de Alice puede ser de 16 bytes.

Para IPv4, este mensaje debe enviarse a través de una conexión IPv4 establecida,
ya que esa es la única forma en que Bob conoce la dirección IPv4 de Charlie para volver a Alice en la Respuesta de Retransmisión.
Desde la versión 0.9.xx, IPv6 es soportado, y este mensaje puede enviarse a través de una conexión IPv6 establecida.

También añadir:

Desde la versión 0.9.xx, cualquier dirección SSU publicada con presentadores debe contener "4" o "6" en la opción "caps".


## Migración

Todos los routers antiguos deben ignorar la propiedad caps en NTCP2 y los caracteres de capacidad desconocidos en la propiedad caps de SSU.

Cualquier dirección SSU con presentadores que no contenga una cap "4" o "6" se asume que es para introducción IPv4.
