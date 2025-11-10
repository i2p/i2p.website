---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Descripción general

Esta propuesta añade un nuevo tipo de firma utilizando BLAKE2b-512 con
cadenas de personalización y sales, para reemplazar SHA-512.
Esto eliminará tres clases de posibles ataques.

## Motivación

Durante las discusiones y diseño de NTCP2 (propuesta 111) y LS2 (propuesta 123),
consideramos brevemente varios ataques que eran posibles, y cómo
prevenirlos. Tres de estos ataques son Ataques de Extensión de Longitud,
Ataques de Protocolo Cruzado, e Identificación de Mensajes Duplicados.

Tanto para NTCP2 como para LS2, decidimos que
estos ataques no eran directamente relevantes para las propuestas en cuestión,
y cualquier solución entraba en conflicto con el objetivo de minimizar las nuevas primitivas.
Además, determinamos que la velocidad de las funciones hash en estos protocolos
no era un factor importante en nuestras decisiones.
Por lo tanto, en su mayoría deferimos la solución a una propuesta separada.
Aunque añadimos algunas características de personalización a la especificación LS2,
no requerimos ninguna nueva función hash.

Muchos proyectos, como ZCash [ZCASH]_, están utilizando funciones hash y
algoritmos de firma basados en algoritmos más nuevos que no son vulnerables a
los siguientes ataques.

### Ataques de Extensión de Longitud

SHA-256 y SHA-512 son vulnerables a Ataques de Extensión de Longitud (LEA) [LEA]_.
Este es el caso cuando se firma los datos reales, no el hash de los datos.
En la mayoría de los protocolos de I2P (streaming, datagramas, netdb y otros), los datos reales son firmados. Una excepción son los archivos SU3, donde se firma el hash.
La otra excepción son los datagramas firmados para DSA (tipo de firma 0) solamente,
donde se firma el hash.
Para otros tipos de firma de datagramas firmados, se firma los datos.

### Ataques de Protocolo Cruzado

Los datos firmados en protocolos I2P pueden ser vulnerables a
Ataques de Protocolo Cruzado (CPA) debido a la falta de separación de dominio.
Esto permite a un atacante usar datos recibidos en un contexto
(como un datagrama firmado) y presentarlos como datos firmados válidos
en otro contexto (como transmisión o base de datos de red).
Aunque es poco probable que los datos firmados de un contexto sean analizados
como datos válidos en otro contexto, es difícil o imposible
analizar todas las situaciones para saber con certeza.
Además, en algún contexto, puede ser posible que un atacante
induzca a una víctima a firmar datos especialmente preparados que podrían ser datos válidos
en otro contexto.
Nuevamente, es difícil o imposible analizar todas las situaciones para saber con certeza.

### Identificación de Mensajes Duplicados

Los protocolos I2P pueden ser vulnerables a la Identificación de Mensajes Duplicados (DMI).
Esto puede permitir a un atacante identificar que dos mensajes firmados tienen el mismo
contenido, incluso si estos mensajes y sus firmas están cifrados.
Aunque es poco probable debido a los métodos de cifrado utilizados en I2P,
es difícil o imposible analizar todas las situaciones para saber con certeza.
Al usar una función hash que proporcione un método para agregar una sal aleatoria,
todas las firmas serán diferentes incluso al firmar los mismos datos.
Aunque Red25519 como se define en la propuesta 123 añade una sal aleatoria a la función hash,
esto no resuelve el problema para conjuntos de arrendamientos no cifrados.

### Velocidad

Aunque no es un motivo principal para esta propuesta,
SHA-512 es relativamente lento, y hay funciones hash más rápidas disponibles.

## Objetivos

- Prevenir los ataques mencionados
- Minimizar el uso de nuevas primitivas criptográficas
- Usar primitivas criptográficas probadas y estándar
- Usar curvas estándar
- Usar primitivas más rápidas si están disponibles

## Diseño

Modificar el tipo de firma existente RedDSA_SHA512_Ed25519 para usar BLAKE2b-512
en lugar de SHA-512. Añadir cadenas de personalización únicas para cada caso de uso.
El nuevo tipo de firma puede ser utilizado tanto para conjuntos de arrendamientos sin cegado como con cegado.

## Justificación

- BLAKE2b no es vulnerable a LEA [BLAKE2]_.
- BLAKE2b proporciona un método estándar para agregar cadenas de personalización para separación de dominios
- BLAKE2b proporciona un método estándar para agregar una sal aleatoria para prevenir DMI.
- BLAKE2b es más rápido que SHA-256 y SHA-512 (y MD5) en hardware moderno,
  según [BLAKE2]_.
- Ed25519 sigue siendo nuestro tipo de firma más rápido, mucho más rápido que ECDSA, al menos en Java.
- Ed25519 [ED25519-REFS]_ requiere una función hash criptográfica de 512 bits.
  No especifica SHA-512. BLAKE2b es igualmente adecuada para la función hash.
- BLAKE2b está ampliamente disponible en bibliotecas para muchos lenguajes de programación, como Noise.

## Especificación

Usar BLAKE2b-512 sin clave como en [BLAKE2]_ con sal y personalización.
Todos los usos de firmas BLAKE2b usarán una cadena de personalización de 16 caracteres.

Cuando se use en la firma RedDSA_BLAKE2b_Ed25519,
se permite una sal aleatoria, sin embargo, no es necesaria, ya que el algoritmo de firma
agrega 80 bytes de datos aleatorios (ver propuesta 123).
Si se desea, al realizar el hash de los datos para calcular r,
establecer una nueva sal aleatoria BLAKE2b de 16 bytes para cada firma.
Al calcular S, restablecer la sal al valor predeterminado de todo ceros.

Cuando se use en la verificación RedDSA_BLAKE2b_Ed25519,
no use una sal aleatoria, use el valor predeterminado de todo ceros.

Las características de sal y personalización no están especificadas en [RFC-7693]_;
use esas características como se especifica en [BLAKE2]_.

### Tipo de Firma

Para RedDSA_BLAKE2b_Ed25519, reemplazar la función hash SHA-512
en RedDSA_SHA512_Ed25519 (tipo de firma 11, como se define en la propuesta 123)
con BLAKE2b-512. No hay otros cambios.

No necesitamos un reemplazo para
EdDSA_SHA512_Ed25519ph (tipo de firma 8) para archivos su3,
porque la versión pre-lleva de EdDSA no es vulnerable a LEA.
EdDSA_SHA512_Ed25519 (tipo de firma 7) no es compatible con archivos su3.

=======================  ===========  ======  =====
        Tipo             Código de Tipo  Desde   Uso
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Para Identidades de Router, Destinos y conjuntos de arrendamientos cifrados solamente; nunca usado para Identidades de Router
=======================  ===========  ======  =====

### Longitudes Comunes de Datos de Estructura

Lo siguiente se aplica al nuevo tipo de firma.

==================================  =============
            Tipo de Datos              Longitud    
==================================  =============
Hash                                     64      
Clave Privada                            32      
Clave Pública                            32      
Firma                                    64      
==================================  =============

### Personalizaciones

Para proporcionar separación de dominio para los diversos usos de las firmas,
usaremos la característica de personalización de BLAKE2b.

Todos los usos de las firmas BLAKE2b usarán una cadena de personalización de 16 caracteres.
Cualquier nuevo uso debe ser agregado a la tabla aquí, con una personalización única.

Los usos del apretón de manos NTCP 1 y SSU a continuación son para los datos firmados definidos en el
apretón de manos en sí.
Los RouterInfos firmados en Mensajes DatabaseStore usarán la personalización de Entrada NetDb,
como si fueran almacenados en la NetDB.

==================================  ==========================
         Uso                        Personalización de 16 Bytes
==================================  ==========================
I2CP SessionConfig                  "I2CP_SessionConf"
Entradas NetDB (RI, LS, LS2)         "network_database"
Apretón de manos NTCP 1                    "NTCP_1_handshake"
Datagramas Firmados                    "sign_datagramI2P"
Transmisión                           "streaming_i2psig"
Apretón de manos SSU                       "SSUHandshakeSign"
Archivos SU3                         n/a, no soportado
Pruebas unitarias                      "test1234test5678"
==================================  ==========================

## Notas

## Problemas

- Alternativa 1: Propuesta 146;
  Proporciona resistencia a LEA
- Alternativa 2: Ed25519ctx en RFC 8032;
  Proporciona resistencia a LEA y personalización.
  Estandarizado, pero ¿alguien lo usa?
  Ver [RFC-8032]_ y [ED25519CTX]_.
- ¿Es el hash "con clave" útil para nosotros?

## Migración

Lo mismo que con el despliegue de tipos de firma anteriores.

Planeamos cambiar los routers nuevos del tipo 7 al tipo 12 como predeterminado.
Planeamos eventualmente migrar routers existentes del tipo 7 al tipo 12,
usando el proceso de "reclaveo" utilizado después de que el tipo 7 fue introducido.
Planeamos cambiar los destinos nuevos del tipo 7 al tipo 12 como predeterminado.
Planeamos cambiar los destinos cifrados nuevos del tipo 11 al tipo 13 como predeterminado.

Apoyaremos el cegamiento desde los tipos 7, 11, y 12 al tipo 12.
No apoyaremos el cegamiento del tipo 12 al tipo 11.

Los routers nuevos podrían empezar a usar el nuevo tipo de firma por defecto después de unos meses.
Los destinos nuevos podrían empezar a usar el nuevo tipo de firma por defecto después de quizás un año.

Para la versión mínima del router 0.9.TBD, los routers deben asegurar:

- No almacenar (o propagar) un RI o LS con el nuevo tipo de firma a routers con menos de la versión 0.9.TBD.
- Al verificar un almacenamiento netdb, no buscar un RI o LS con el nuevo tipo de firma de routers con menos de la versión 0.9.TBD.
- Routers con un nuevo tipo de firma en su RI no pueden conectarse a routers con menos de la versión 0.9.TBD,
  ya sea con NTCP, NTCP2, o SSU.
- Las conexiones de transmisión y los datagramas firmados no funcionarán a routers con menos de la versión 0.9.TBD,
  pero no hay forma de saberlo, por lo que el nuevo tipo de firma no debe usarse por defecto durante un período
  de meses o años después de que 0.9.TBD sea lanzado.

## Referencias

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "Firmas de alta velocidad y alta seguridad" por Daniel
    J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, y
    Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://en.wikipedia.org/wiki/Length_extension_attack

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
