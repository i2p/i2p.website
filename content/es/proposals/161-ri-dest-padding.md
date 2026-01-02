---
title: "RI y Padding de Destino"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Open"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Estado

Implementado en 0.9.57.
Dejamos esta propuesta abierta para que podamos mejorar y discutir las ideas en la sección de "Planificación Futura".


## Visión general


### Resumen

La clave pública ElGamal en los Destinos no ha sido utilizada desde el lanzamiento 0.6 (2005).
Si bien nuestras especificaciones dicen que no se utiliza, NO dicen que las implementaciones puedan evitar
generar un par de claves ElGamal y simplemente llenar el campo con datos aleatorios.

Proponemos cambiar las especificaciones para decir que
el campo es ignorado y que las implementaciones PUEDEN llenar el campo con datos aleatorios.
Este cambio es compatible hacia atrás. No se conoce ninguna implementación que valide
la clave pública ElGamal.

Además, esta propuesta ofrece orientación a los implementadores sobre cómo generar los
datos aleatorios para el padding de Destino Y de Identidad de Router para que sean comprimibles mientras
siguen siendo seguros, y sin que las representaciones en Base 64 parezcan estar corruptas o inseguras.
Esto proporciona la mayoría de los beneficios de eliminar los campos de padding sin ningún
cambio disruptivo en el protocolo.
Destinos comprimibles reducen el tamaño de SYN de streaming y de datagramas replicables;
Identidades de Router comprimibles reducen los Mensajes de Almacenamiento en Base de Datos, mensajes SSU2 de Sesión Confirmada,
y archivos de reseed su3.

Finalmente, la propuesta discute posibilidades para nuevos formatos de Destino e Identidad de Router
que eliminarían el padding por completo. También hay una breve discusión sobre criptografía post-cuántica
y cómo eso puede afectar la planificación futura.


### Objetivos

- Eliminar el requerimiento de generar un par de claves ElGamal para Destinos
- Recomendar mejores prácticas para que los Destinos y las Identidades de Router sean altamente comprimibles,
  pero que no muestren patrones obvios en las representaciones en Base 64.
- Fomentar la adopción de las mejores prácticas por todas las implementaciones para que
  los campos no sean distinguibles
- Reducir el tamaño del SYN de streaming
- Reducir el tamaño de los datagramas replicables
- Reducir el tamaño del bloque RI de SSU2
- Reducir el tamaño de la Sesión Confirmada de SSU2 y la frecuencia de fragmentación
- Reducir el tamaño del Mensaje de Almacenamiento en Base de Datos (con RI)
- Reducir el tamaño del archivo de reseed
- Mantener la compatibilidad en todos los protocolos y APIs
- Actualizar las especificaciones
- Discutir alternativas para nuevos formatos de Destino e Identidad de Router

Al eliminar el requerimiento de generar claves ElGamal, las implementaciones pueden
ser capaces de eliminar completamente el código ElGamal, sujeto a consideraciones de compatibilidad hacia atrás
en otros protocolos.


## Diseño

Hablando estrictamente, la clave pública de firma de 32 bytes sola (en ambos Destinos e Identidades de Router)
y la clave pública de cifrado de 32 bytes (solo en Identidades de Router) es un número aleatorio
que proporciona toda la entropía necesaria para los hashes SHA-256 de estas estructuras
para ser criptográficamente fuertes y distribuidos al azar en la base de datos DHT de la red.

Sin embargo, por precaución, recomendamos un mínimo de 32 bytes de datos aleatorios
para ser usados en el campo de clave pública ElG y en el padding. Además, si los campos fueran todos ceros,
los destinos en Base 64 contendrían largas secuencias de caracteres AAAA, lo que podría causar alarma
o confusión a los usuarios.

Para el tipo de firma Ed25519 y el tipo de cifrado X25519:
Los Destinos contendrán 11 copias (352 bytes) de los datos aleatorios.
Las Identidades de Router contendrán 10 copias (320 bytes) de los datos aleatorios.


### Ahorros Estimados

Los Destinos están incluidos en cada SYN de streaming
y datagramas replicables.
Los Infos de Router (que contienen las Identidades de Router) están incluidos en los Mensajes de Almacenamiento en Base de Datos
y en los mensajes de Sesión Confirmada en NTCP2 y SSU2.

NTCP2 no comprime el Info de Router.
Los RI en los Mensajes de Almacenamiento en Base de Datos y mensajes de Sesión Confirmada de SSU2 son comprimidos con gzip.
Los Infos de Router son comprimidos en archivos de reseed SU3.

Los Destinos en Mensajes de Almacenamiento en Base de Datos no son comprimidos.
Los mensajes SYN de streaming son comprimidos con gzip en la capa I2CP.

Para el tipo de firma Ed25519 y el tipo de cifrado X25519,
ahorros estimados:

| Tipo de Datos | Tamaño Total | Claves y Cert | Padding sin Comprimir | Padding Comprimido | Tamaño | Ahorros |
|---------------|--------------|---------------|-----------------------|--------------------|--------|---------|
| Destino | 391 | 39 | 352 | 32 | 71 | 320 bytes (82%) |
| Identidad de Router | 391 | 71 | 320 | 32 | 103 | 288 bytes (74%) |
| Info de Router | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 bytes (29%) |

Notas: Se asume que el certificado de 7 bytes no es comprimible, sobrecarga de gzip adicional nula.
Ninguna es cierta, pero los efectos serán pequeños.
Ignora otras partes comprimibles del Info de Router.


## Especificación

Los cambios propuestos en nuestras especificaciones actuales se documentan a continuación.


### Estructuras Comunes
Cambiar la especificación de estructuras comunes
para especificar que el campo de clave pública de Destino de 256 bytes se ignora y puede
contener datos aleatorios.

Agregar una sección a la especificación de estructuras comunes
recomendando la mejor práctica para el campo de clave pública de Destino y los
campos de padding en el Destino y la Identidad de Router, de la siguiente manera:

Generar 32 bytes de datos aleatorios utilizando un generador de números pseudoaleatorios criptográficamente seguro (PRNG)
y repetir esos 32 bytes según sea necesario para llenar el campo de clave pública (para Destinos)
y el campo de padding (para Destinos e Identidades de Router).

### Archivo de Clave Privada
El formato del archivo de clave privada (eepPriv.dat) no es una parte oficial de nuestras especificaciones
pero está documentado en los [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)
y otras implementaciones lo soportan.
Esto permite la portabilidad de claves privadas a diferentes implementaciones.
Agregar una nota a ese javadoc que la clave pública de cifrado puede ser padding aleatorio
y la clave privada de cifrado puede ser todo ceros o datos aleatorios.

### SAM
Nota en la especificación SAM que la clave privada de cifrado no se usa y puede ser ignorada.
Cualquier dato aleatorio puede ser devuelto por el cliente.
El Puente SAM puede enviar datos aleatorios en la creación (con DEST GENERATE o SESSION CREATE DESTINATION=TRANSIENT)
en lugar de todos ceros, para que la representación en Base 64 no tenga una cadena de caracteres AAAA
y parezca rota.


### I2CP
No se requieren cambios en I2CP. La clave privada para la clave pública de cifrado en el Destino
no se envía al router.


## Planificación Futura


### Cambios en el Protocolo

A un costo de cambios en el protocolo y una falta de compatibilidad hacia atrás, podríamos
cambiar nuestros protocolos y especificaciones para eliminar el campo de padding en
el Destino, Identidad de Router, o ambos.

Esta propuesta tiene cierta similitud con el formato de leaseset cifrado "b33",
que contiene solo una clave y un campo de tipo.

Para mantener alguna compatibilidad, ciertas capas de protocolo podrían "expandir" el campo de padding
con todos ceros para presentar a otras capas de protocolo.

Para los Destinos, también podríamos eliminar el campo de tipo de cifrado en el certificado de clave,
con un ahorro de dos bytes.
Alternativamente, los Destinos podrían obtener un nuevo tipo de cifrado en el certificado de clave,
indicando una clave pública cero (y padding).

Si la conversión de compatibilidad entre formatos antiguos y nuevos no se incluye en alguna capa de protocolo,
las siguientes especificaciones, APIs, protocolos y aplicaciones se verían afectadas:

- Especificación de estructuras comunes
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Reseeding
- Archivo de Clave Privada
- API central y de router de Java
- API i2pd
- Bibliotecas SAM de terceros
- Herramientas empaquetadas y de terceros
- Varios plugins de Java
- Interfaces de usuario
- Aplicaciones P2P como MuWire, bitcoin, monero
- hosts.txt, libreta de direcciones y suscripciones

Si la conversión se especifica en alguna capa, la lista se reduciría.

Los costos y beneficios de estos cambios no están claros.

Propuestas específicas TBD:


### Claves PQ

Las claves públicas de cifrado Post-Cuanticas (PQ), para cualquier algoritmo anticipado,
son más grandes de 256 bytes. Esto eliminaría cualquier padding y cualquier ahorro de los cambios propuestos
arriba, para Identidades de Router.

En un enfoque "híbrido" PQ, como lo que está haciendo SSL, las claves PQ serían solo efímeras,
y no aparecerían en la Identidad de Router.

Las claves de firma PQ no son viables,
y las Destinos no contienen claves públicas de cifrado.
Las claves estáticas para ratchet están en el Lease Set, no en el Destino.
de modo que podemos eliminar Destinos de la discusión siguiente.

Entonces PQ solo afecta los Infos de Router, y solo para claves estáticas PQ (no efímeras), no para híbrido PQ.
Esto sería para un nuevo tipo de cifrado y afectaría NTCP2, SSU2 y
mensajes de Búsqueda en Base de Datos cifrados y sus respuestas.
El marco de tiempo estimado para el diseño, desarrollo y despliegue de eso sería ????????
Pero sería después de híbrido o ratchet ????????????

Para más discusión ver [this topic](http://zzz.i2p/topics/3294).


## Problemas

Puede ser deseable volver a teclear la red a un ritmo lento, para proporcionar cobertura para nuevos routers.
"Volver a teclear" podría significar simplemente cambiar el padding, sin realmente cambiar las claves.

No es posible volver a teclear los Destinos existentes.

¿Deberían Identidades de Router con padding en el campo de clave pública ser identificadas con un tipo de cifrado diferente en el certificado de clave? Esto causaría problemas de compatibilidad.


## Migración

No hay problemas de compatibilidad hacia atrás para reemplazar la clave ElGamal con padding.

Volver a teclear, si se implementa, sería similar a lo realizado
en tres transiciones anteriores de identidad de router:
De firmas DSA-SHA1 a ECDSA, luego a
firmas EdDSA, luego a cifrado X25519.

Sujeto a problemas de compatibilidad hacia atrás, y después de deshabilitar SSU,
las implementaciones pueden eliminar completamente el código ElGamal.
Aproximadamente el 14% de los routers en la red son del tipo de cifrado ElGamal, incluidos muchos floodfills.

Se encuentra un borrador de solicitud de fusión para Java I2P en [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
