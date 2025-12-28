---
title: "Routers ECIES"
number: "156"
author: "zzz, original"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## Nota
Despliegue de red y pruebas en progreso.
Sujeto a revisión.
Estado:

- Routers ECIES implementados desde la versión 0.9.48, ver [Common](/docs/specs/common-structures/).
- Creación de túneles implementada desde la versión 0.9.48, ver [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- Mensajes cifrados a routers ECIES implementados desde la versión 0.9.49, ver [ECIES-ROUTERS](/docs/specs/ecies-routers/).
- Nuevos mensajes de construcción de túneles implementados desde la versión 0.9.51.


## Visión general


### Resumen

Las Identidades de Router actualmente contienen una clave de cifrado ElGamal.
Esto ha sido el estándar desde los inicios de I2P.
ElGamal es lento y debe ser reemplazado en todos los lugares donde se utilice.

Las propuestas para LS2 [Prop123](/proposals/123-new-netdb-entries/) y ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/)
(ahora especificadas en [ECIES](/docs/specs/ecies/)) definieron el reemplazo de ElGamal por ECIES
para Destinos.

Esta propuesta define el reemplazo de ElGamal por ECIES-X25519 para routers.
Esta propuesta proporciona una visión general de los cambios requeridos.
La mayoría de los detalles están en otras propuestas y especificaciones.
Vea la sección de referencia para enlaces.


### Objetivos

Vea [Prop152](/proposals/152-ecies-tunnels/) para objetivos adicionales.

- Reemplazar ElGamal con ECIES-X25519 en Identidades de Router
- Reutilizar primitivas criptográficas existentes
- Mejorar la seguridad de los mensajes de construcción de túneles donde sea posible manteniendo la compatibilidad
- Soportar túneles con pares mixtos ElGamal/ECIES
- Maximizar la compatibilidad con la red actual
- No requerir una actualización "día de la bandera" para toda la red
- Despliegue gradual para minimizar riesgos
- Nuevo mensaje de construcción de túnel más pequeño


### Objetivos no buscados

Vea [Prop152](/proposals/152-ecies-tunnels/) para objetivos adicionales no buscados.

- No se requiere routers de doble clave
- Cambios en la capa de cifrado, para eso vea [Prop153](/proposals/153-chacha20-layer-encryption/)


## Diseño


### Ubicación de la Clave y Tipo de Criptografía

Para Destinos, la clave está en el leaseset, no en el Destino, y
admitimos múltiples tipos de cifrado en el mismo leaseset.

Nada de eso es necesario para routers. La clave de cifrado del router
está en su Identidad de Router. Vea la especificación de estructuras comunes [Common](/docs/specs/common-structures/).

Para routers, reemplazaremos la clave ElGamal de 256 bytes en la Identidad del Router
con una clave X25519 de 32 bytes y 224 bytes de relleno.
Esto se indicará por el tipo de criptografía en el certificado de clave.
El tipo de criptografía (igual que se usa en LS2) es 4.
Esto indica una clave pública X25519 de 32 bytes en formato little-endian.
Esta es la construcción estándar como se define en la especificación de estructuras comunes [Common](/docs/specs/common-structures/).

Esto es idéntico al método propuesto para ECIES-P256
para tipos de criptografía 1-3 en la propuesta 145 [Prop145](/proposals/145-ecies/).
Si bien esta propuesta nunca fue adoptada, los desarrolladores de la implementación en Java se prepararon para
tipos de criptografía en certificados de clave de Identidad del Router al añadir comprobaciones en varios
lugares en la base de código. La mayor parte de este trabajo se realizó a mediados de 2019.


### Mensaje de Construcción de Túnel

Se requieren varios cambios a la especificación de creación de túneles [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies)
para usar ECIES en lugar de ElGamal.
Además, realizaremos mejoras en los mensajes de construcción de túneles
para aumentar la seguridad.

En la fase 1, cambiaremos el formato y el cifrado del
Registro de Solicitud de Construcción y el Registro de Respuesta de Construcción para saltos ECIES.
Estos cambios serán compatibles con routers ElGamal existentes.
Estos cambios están definidos en la propuesta 152 [Prop152](/proposals/152-ecies-tunnels/).

En la fase 2, agregaremos una nueva versión del
Mensaje de Solicitud de Construcción, Mensaje de Respuesta de Construcción,
Registro de Solicitud de Construcción y Registro de Respuesta de Construcción.
El tamaño será reducido para eficiencia.
Estos cambios deben ser compatibles por todos los saltos en un túnel, y todos los saltos deben ser ECIES.
Estos cambios están definidos en la propuesta 157 [Prop157](/proposals/157-new-tbm/).


### Cifrado de extremo a extremo

#### Historia

En el diseño original de Java I2P, había un único Gestor de Clave de Sesión ElGamal (SKM)
compartido por el router y todos sus Destinos locales.
Como un SKM compartido podría filtrar información y permitir correlación por atacantes,
el diseño fue cambiado para soportar SKMs ElGamal separados para el router y cada Destino.
El diseño ElGamal soportaba solo remitentes anónimos;
el remitente enviaba solo claves efímeras, no una clave estática.
El mensaje no estaba vinculado a la identidad del remitente.

Luego, diseñamos el ECIES Ratchet SKM en
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/), ahora especificado en [ECIES](/docs/specs/ecies/).
Este diseño fue especificado utilizando el patrón "IK" de Noise, que incluía la clave estática del remitente en el primer mensaje. Este protocolo se utiliza para Destinos ECIES (tipo 4).
El patrón IK no permite remitentes anónimos.

Por lo tanto, incluimos en la propuesta una forma de enviar también mensajes anónimos
a un Ratchet SKM, usando una clave estática llena de ceros. Esto simulaba un patrón "N" de Noise,
pero de manera compatible, por lo que un ECIES SKM podría recibir tanto mensajes anónimos como no anónimos.
La intención era usar clave cero para routers ECIES.


#### Casos de Uso y Modelos de Amenaza

El caso de uso y modelo de amenaza para mensajes enviados a routers es muy diferente del
de mensajes de extremo a extremo entre Destinos.


Caso de uso y modelo de amenaza del Destino:

- No anónimo de/después de destinos (remitente incluye clave estática)
- Soporte eficiente de tráfico sostenido entre destinos (handshake completo, streaming y etiquetas)
- Siempre enviado a través de túneles de salida y entrada
- Ocultar todas las características identificativas del OBEP y IBGW, requiriendo codificación Elligator2 de claves efímeras.
- Ambos participantes deben usar el mismo tipo de cifrado


Caso de uso y modelo de amenaza del Router:

- Mensajes anónimos de routers o destinos (remitente no incluye clave estática)
- Solo para Búsquedas y Almacenes de Base de Datos encriptados, generalmente a floodfills
- Mensajes ocasionales
- No se deben correlacionar múltiples mensajes
- Siempre enviado a través de túneles de salida directamente a un router. No se utilizan túneles de entrada
- OBEP sabe que está reenviando el mensaje a un router y conoce su tipo de cifrado
- Los dos participantes pueden tener diferentes tipos de cifrado
- Respuestas de Búsqueda de Base de Datos son mensajes de una sola vez utilizando la clave de respuesta y la etiqueta en el mensaje de Búsqueda de Base de Datos
- Confirmaciones de Almacén de Base de Datos son mensajes de una sola vez utilizando un mensaje de Estado de Entrega empaquetado


Metas no buscadas del caso de uso del Router:

- No hay necesidad de mensajes no anónimos
- No hay necesidad de enviar mensajes a través de túneles exploratorios de entrada (un router no publica leasesets exploratorios)
- No hay necesidad de tráfico sostenido de mensajes utilizando etiquetas
- No hay necesidad de ejecutar Gestores de Clave de Sesión "doble clave" como se describe en [ECIES](/docs/specs/ecies/) para Destinos. Los routers solo tienen una clave pública.


#### Conclusiones del Diseño

El SKM del Router ECIES no necesita un Ratchet SKM completo como se especifica en [ECIES](/docs/specs/ecies/) para Destinos.
No hay requisito para mensajes no anónimos utilizando el patrón IK.
El modelo de amenaza no requiere claves efímeras codificadas con Elligator2.

Por lo tanto, el SKM del router usará el patrón "N" de Noise, mismo que se especifica
en [Prop152](/proposals/152-ecies-tunnels/) para la construcción de túneles.
Utilizará el mismo formato de payload que se especifica en [ECIES](/docs/specs/ecies/) para Destinos.
El modo de clave estática cero (sin vinculación o sesión) de IK especificado en [ECIES](/docs/specs/ecies/) no será utilizado.

Las respuestas a las búsquedas se encriptarán con una etiqueta de rachet si se solicita en la búsqueda.
Esto se documenta en [Prop154](/proposals/154-ecies-lookups/), ahora especificado en [I2NP](/docs/specs/i2np/).

El diseño permite que el router tenga un solo Gestor de Clave de Sesión ECIES.
No hay necesidad de ejecutar Gestores de Clave de Sesión "doble clave" como
se describe en [ECIES](/docs/specs/ecies/) para Destinos.
Los routers solo tienen una clave pública.

Un router ECIES no tiene una clave estática ElGamal.
El router aún necesita una implementación de ElGamal para construir túneles
a través de routers ElGamal y enviar mensajes cifrados a routers ElGamal.

Un router ECIES PUEDE requerir un Gestor de Clave de Sesión ElGamal parcial para
recibir mensajes etiquetados por ElGamal recibidos como respuestas a búsquedas NetDB
de routers floodfill anteriores a 0.9.46, ya que esos routers no
tienen una implementación de respuestas etiquetadas por ECIES como se especifica en [Prop152](/proposals/152-ecies-tunnels/).
Si no, un router ECIES puede no solicitar una respuesta cifrada de un
router floodfill anterior a 0.9.46.

Esto es opcional. La decisión puede variar en varias implementaciones de I2P
y puede depender de la cantidad de la red que se ha actualizado a
0.9.46 o superior.
En esta fecha, aproximadamente el 85% de la red está en 0.9.46 o superior.


## Especificación

X25519: Ver [ECIES](/docs/specs/ecies/).

Identidad del Router y Certificado de Clave: Ver [Common](/docs/specs/common-structures/).

Construcción de Túneles: Ver [Prop152](/proposals/152-ecies-tunnels/).

Nuevo Mensaje de Construcción de Túneles: Ver [Prop157](/proposals/157-new-tbm/).


### Encriptación de Solicitud

La encriptación de la solicitud es la misma que se especifica en [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) y [Prop152](/proposals/152-ecies-tunnels/),
usando el patrón "N" de Noise.

Las respuestas a búsquedas se cifrarán con una etiqueta de rachet si se solicita en la búsqueda.
Los mensajes de solicitud de Búsqueda de Base de Datos contienen la clave de respuesta de 32 bytes y la etiqueta de respuesta de 8 bytes
como se especifica en [I2NP](/docs/specs/i2np/) y [Prop154](/proposals/154-ecies-lookups/). La clave y la etiqueta se utilizan para encriptar la respuesta.

No se crean conjuntos de etiquetas.
El esquema de clave estática cero especificado en
ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) y [ECIES](/docs/specs/ecies/) no será utilizado.
Las claves efímeras no serán codificadas con Elligator2.

Generalmente, estos serán mensajes de Nueva Sesión y se enviarán con una clave estática cero
(sin vinculación ni sesión), ya que el remitente del mensaje es anónimo.


#### KDF para ck y h Iniciales

Esto es estándar [NOISE](https://noiseprotocol.org/noise.html) para el patrón "N" con un nombre de protocolo estándar.
Esto es lo mismo que se especifica en [Tunnel-Creation-ECIES] y [Prop152](/proposals/152-ecies-tunnels/) para mensajes de construcción de túneles.


  ```text

Este es el patrón de mensaje "e":

  // Definir protocol_name.
  Establecer protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, codificado en US-ASCII, sin terminación NULL).

  // Definir Hash h = 32 bytes
  // Rellenar a 32 bytes. NO lo hashear, porque no supera los 32 bytes.
  h = protocol_name || 0

  Definir ck = clave de encadenamiento de 32 bytes. Copiar los datos de h a ck.
  Establecer chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // hasta aquí, puede ser precalculado por todos los routers.


  ```


#### KDF para Mensaje

Los creadores de mensajes generan un par de claves X25519 efímeras para cada mensaje.
Las claves efímeras deben ser únicas por mensaje.
Esto es lo mismo que se especifica en [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) y [Prop152](/proposals/152-ecies-tunnels/) para mensajes de construcción de túneles.


  ```dataspec


// Par de claves estáticas X25519 del router de destino (hesk, hepk) de la Identidad del Router
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || abajo significa añadir
  h = SHA256(h || hepk);

  // hasta aquí, puede ser precalculado por cada router
  // para todos los mensajes entrantes

  // El emisor genera un par de claves efímeras X25519
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  Fin del patrón de mensaje "e".

  Este es el patrón de mensaje "es":

  // Noise es
  // El emisor realiza un DH X25519 con la clave pública estática del receptor.
  // El router de destino
  // extrae la clave efímera del emisor que precede al registro encriptado.
  claveCompartida = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[cadenaClave, k] = MixKey(claveCompartida)
  // Parámetros de ChaChaPoly para cifrar/descifrar
  datosClave = HKDF(cadenaClave, claveCompartida, "", 64)
  // La clave de la cadena no se usa
  //cadenaClave = datosClave[0:31]

  // Parámetros de AEAD
  k = datosClave[32:63]
  n = 0
  textoPlano = registro de solicitud de construcción de 464 bytes
  ad = h
  cifrado = ENCRYPTAR(k, n, textoPlano, ad)

  Fin del patrón de mensaje "es".

  // MixHash(ciphertext) no es requerido
  //h = SHA256(h || ciphertext)


  ```


#### Payload

El payload es el mismo formato de bloque definido en [ECIES](/docs/specs/ecies/) y [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Todos los mensajes deben contener un bloque de DateTime para la prevención de repeticiones.


### Cifrado de Respuesta

Las respuestas a mensajes de Búsqueda de Base de Datos son mensajes de Almacén de Base de Datos o de Respuesta de Búsqueda de Base de Datos.
Se cifran como mensajes de Sesión Existente con
la clave de respuesta de 32 bytes y la etiqueta de respuesta de 8 bytes
como se especifica en [I2NP](/docs/specs/i2np/) y [Prop154](/proposals/154-ecies-lookups/).


No hay respuestas explícitas a mensajes de Almacén de Base de Datos. El remitente puede integrar su
propia respuesta como un Mensaje Garlic para sí mismo, conteniendo un mensaje de Estado de Entrega.


## Justificación

Este diseño maximiza la reutilización de primitivas criptográficas, protocolos y códigos existentes.

Este diseño minimiza el riesgo.


## Notas de Implementación

Los routers más antiguos no verifican el tipo de cifrado del router y enviarán registros de construcción o mensajes netdb cifrados con ElGamal.
Algunos routers recientes tienen errores y enviarán varios tipos de registros de construcción malformados.
Algunos routers recientes pueden enviar mensajes netdb no anónimos (ratchet completo).
Los implementadores deben detectar y rechazar estos registros y mensajes
lo antes posible, para reducir el uso de CPU.


## Problemas

La propuesta 145 [Prop145](/proposals/145-ecies/) puede o no ser reescrita para ser mayormente compatible con
la Propuesta 152 [Prop152](/proposals/152-ecies-tunnels/).


## Migración

La implementación, prueba y despliegue tomará varias versiones
y aproximadamente un año. Las fases son las siguientes. La asignación de
cada fase a una versión en particular está por confirmar y depende de
la velocidad de desarrollo.

Los detalles de la implementación y migración pueden variar para
cada implementación de I2P.


### Conexiones Básicas Punto a Punto

Los routers ECIES pueden conectarse y recibir conexiones de routers ElGamal.
Esto debería ser posible ahora, ya que varias comprobaciones fueron añadidas al código base de Java
a mediados de 2019 como reacción a la propuesta 145 [Prop145](/proposals/145-ecies/) sin terminar.
Asegúrese de que no haya nada en las bases de código
que impida conexiones punto a punto a routers no ElGamal.

Comprobaciones de corrección de código:

- Asegúrese de que los routers ElGamal no solicitan respuestas cifradas con AEAD a mensajes DatabaseLookup
  (cuando la respuesta regresa a través de un túnel exploratorio al router)
- Asegúrese de que los routers ECIES no solicitan respuestas cifradas con AES a mensajes DatabaseLookup
  (cuando la respuesta regresa a través de un túnel exploratorio al router)

Hasta las fases posteriores, cuando las especificaciones e implementaciones estén completas:

- Asegúrese de que no se intenten construir túneles por routers ElGamal a través de routers ECIES.
- Asegúrese de que no se envíen mensajes cifrados con ElGamal por routers ElGamal a routers floodfill ECIES.
  (Lookups de Base de Datos y Almacenamientos de Base de Datos)
- Asegúrese de que no se envíen mensajes cifrados con ECIES por routers ECIES a routers floodfill ElGamal.
  (Lookups de Base de Datos y Almacenamientos de Base de Datos)
- Asegúrese de que los routers ECIES no se conviertan automáticamente en floodfill.

No se deberían requerir cambios.
Versión objetivo, si se requieren cambios: 0.9.48


### Compatibilidad de NetDB

Asegúrese de que las infos de router ECIES se puedan almacenar y recuperar de routers floodfill ElGamal.
Esto debería ser posible ahora, ya que varias comprobaciones fueron añadidas al código base de Java
a mediados de 2019 como reacción a la propuesta 145 [Prop145] sin terminar.
Asegúrese de que no haya nada en las bases de código
que impida el almacenamiento de RouterInfos no ElGamal en la base de datos de red.

No deberían requerirse cambios.
Versión objetivo, si se requieren cambios: 0.9.48


### Construcción de Túneles

Implementar la construcción de túneles como se define en la propuesta 152 [Prop152](/proposals/152-ecies-tunnels/).
Iniciar teniendo un router ECIES construyendo túneles con todos los saltos ElGamal;
usar su propio registro de solicitud de construcción para un túnel de entrada para probar y depurar.

Luego pruebe y soporte routers ECIES construyendo túneles con una mezcla de
saltos ElGamal y ECIES.

Luego habilite la construcción de túneles a través de routers ECIES.
No debería ser necesario un chequeo de versión mínima a menos que se hagan cambios incompatibles
a la propuesta 152 después de una versión.

Versión objetivo: 0.9.48, finales de 2020


### Mensajes Ratchet a routers floodfill ECIES

Implementar y probar la recepción de mensajes ECIES (con clave estática cero) por routers floodfill ECIES,
como se define en la propuesta 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/).
Implementar y probar la recepción de respuestas AEAD a mensajes DatabaseLookup por routers ECIES.

Habilitar el auto-floodfill por routers ECIES.
Luego habilitar el envío de mensajes ECIES a routers ECIES.
No debería ser necesario un chequeo de versión mínima a menos que se hagan cambios incompatibles
a la propuesta 152 después de una versión.

Versión objetivo: 0.9.49, principios de 2021.
Los routers ECIES pueden convertirse automáticamente en floodfill.


### Rekeying y Nuevas Instalaciones

Nuevas instalaciones por defecto usarán ECIES a partir de la versión 0.9.49.

Reclutar gradualmente todos los routers para minimizar el riesgo y la interrupción de la red.
Use el código existente que hizo el rekeying para la migración de tipo de firma hace años.
Este código da a cada router una pequeña posibilidad al azar de rekeying en cada reinicio.
Después de varios reinicios, un router probablemente habrá reclaveado a ECIES.

El criterio para iniciar el reclaveo es que una porción suficiente de la red,
quizás el 50%, pueda construir túneles a través de routers ECIES (0.9.48 o superior).

Antes de hacer un reclaveo agresivo de toda la red, la gran mayoría
(tal vez 90% o más) debe poder construir túneles a través de routers ECIES (0.9.48 o superior)
Y enviar mensajes a floodfills ECIES (0.9.49 o superior).
Este objetivo probablemente se alcanzará para la versión 0.9.52.

El reclaveo tomará varias versiones.

Versión objetivo:
0.9.49 para nuevos routers por defecto a ECIES;
0.9.49 para comenzar lentamente el reclaveo;
0.9.50 - 0.9.52 para aumentar repetidamente la tasa de reclaveo;
finales de 2021 para que la mayoría de la red esté reclaveada.


### Nuevo Mensaje de Construcción de Túnel (Fase 2)

Implementar y probar el nuevo Mensaje de Construcción de Túneles como se define en la propuesta 157 [Prop157](/proposals/157-new-tbm/).
Desplegar el soporte en la versión 0.9.51.
Hacer pruebas adicionales, luego habilitar en la versión 0.9.52.

Las pruebas serán difíciles.
Antes de que esto pueda ser ampliamente probado, un buen subconjunto de la red debe soportarlo.
Antes de que sea ampliamente útil, la mayoría de la red debe soportarlo.
Si se requieren cambios de especificación o implementación después de las pruebas,
eso retrasaría el despliegue para una versión adicional.

Versión objetivo: 0.9.52, finales de 2021.


### Rekeying Completo

En este punto, los routers más antiguos que alguna versión TBD
no podrán construir túneles a través de la mayoría de los pares.

Versión objetivo: 0.9.53, principios de 2022.


