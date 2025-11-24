```markdown
---
title: "Nuevas entradas netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Abierta"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Estado

Partes de esta propuesta están completas e implementadas en 0.9.38 y 0.9.39. 
Las Estructuras Comunes, I2CP, I2NP y otras especificaciones ahora están actualizadas 
para reflejar los cambios que están soportados actualmente.

Las partes completadas aún están sujetas a revisiones menores. 
Otras partes de esta propuesta están aún en desarrollo y sujetas a revisiones sustanciales.

El Búsqueda de Servicios (tipos 9 y 11) son de baja prioridad y no están programados, 
y podrían ser divididos en una propuesta separada.


## Visión general

Esta es una actualización y agregación de las siguientes 4 propuestas:

- 110 LS2
- 120 Meta LS2 para multihoming masivo
- 121 LS2 Encriptado
- 122 Búsqueda de servicio no autenticada (anycasting)

Estas propuestas son mayormente independientes, pero por racionalidad definimos 
y usamos un formato común para varias de ellas.

Las siguientes propuestas están algo relacionadas:

- 140 Multihoming Invisible (incompatible con esta propuesta)
- 142 Nuevo Plantilla Criptográfica (para nueva criptografía simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 para LS2 Encriptado
- 150 Protocolo de Granja de Ajo
- 151 ECDSA Cegamiento


## Propuesta

Esta propuesta define 5 nuevos tipos de DatabaseEntry y el proceso 
para almacenarlos y recuperarlos de la base de datos de la red, 
así como el método para firmarlos y verificar esas firmas.

### Metas

- Compatibilidad con versiones anteriores
- LS2 Utilizable con multihoming de estilo antiguo
- No se requieren nuevas criptografías o primitivos para soporte
- Mantener desacoplamiento de criptografía y la firma; 
  soportar todas las versiones actuales y futuras
- Habilitar claves de firma fuera de línea opcionales
- Reducir la precisión de las marcas de tiempo para reducir el fingerprinting
- Habilitar nueva criptografía para destinos
- Habilitar multihoming masivo
- Corregir múltiples problemas con LS encriptado existente
- Cegamiento opcional para reducir visibilidad por floodfills
- El cifrado soporta claves revocables tanto de una sola clave 
  como de clave múltiple
- Búsqueda de servicios para facilitar la búsqueda de outproxies, 
  bootstrap de DHT de aplicaciones y otros usos
- No romper nada que dependa de hashes de destino binarios de 32 bytes, 
  por ejemplo, bittorrent
- Agregar flexibilidad a leasesets mediante propiedades, como tenemos en routerinfos.
- Poner marca de tiempo publicarda y expiración variable en el encabezado, 
  por lo que funciona incluso si los contenidos están encriptados 
  (no derivar marca de tiempo del arrendamiento más temprano)
- Todos los nuevos tipos viven en el mismo espacio DHT y ubicaciones pares 
  como leasesets existentes, para que los usuarios puedan migrar del viejo LS a LS2, 
  o cambiar entre LS2, Meta y Encriptado, sin cambiar el Destino o hash.
- Un Destino existente puede ser convertido para usar claves fuera de línea, 
  o volver a claves en línea, sin cambiar el Destino o hash.


### No metas / Fuera de alcance

- Nuevo algoritmo de rotación DHT o generación aleatoria compartida
- El tipo específico de nuevo cifrado y el esquema de cifrado de extremo a extremo 
  para usar ese nuevo tipo estaría en una propuesta separada. 
  No se especifica ni discute ningún nuevo cifrado aquí.
- Nuevo cifrado para RIs o construcción de túneles. 
  Eso estaría en una propuesta separada.
- Métodos de cifrado, transmisión y recepción de mensajes I2NP DLM / DSM / DSRM. 
  No cambiar.
- Cómo generar y soportar Meta, incluida la comunicación entre routers de respaldo, 
  gestión, recuperación y coordinación. 
  El soporte puede añadirse a I2CP, o i2pcontrol, o un nuevo protocolo. 
  Esto puede o no estar estandarizado.
- Cómo implementar y gestionar túneles de expiración más larga, 
  o cancelar túneles existentes. 
  Es extremadamente difícil y, sin él, no se puede tener 
  un apagado razonable y controlado.
- Cambios en el modelo de amenazas
- Formato de almacenamiento fuera de línea, o métodos para almacenar/recuperar/compartir los datos.
- Los detalles de implementación no se discuten aquí y se dejan a cada proyecto.



### Justificación

LS2 agrega campos para cambiar el tipo de cifrado 
y para futuros cambios en el protocolo.

LS2 Encriptado corrige varios problemas de seguridad 
con el actual LS encriptado utilizando cifrado asimétrico 
del conjunto completo de arrendamientos.

Meta LS2 proporciona multihoming flexible, eficiente, efectivo y a gran escala.

Registro de servicio y Lista de servicios proporcionan servicios anycast 
como búsqueda de nombres y bootstrap DHT.


### Tipos de Datos NetDB

Los números de tipo se usan en los Mensajes de Búsqueda/Almacenamiento de Base de Datos I2NP.

La columna de extremo a extremo se refiere a si las consultas/respuestas 
se envían a un Destino en un Mensaje de Ajo.


Tipos existentes:

            Datos NetDB               Tipo Búsqueda   Tipo Almacen   
cualquiera                                0            cualquiera     
LS                                        1             1      
RI                                        2             0      
exploratorio                              3            DSRM    

Nuevos tipos:

            Datos NetDB               Tipo Búsqueda   Tipo Almacenamiento   ¿Encabezado LS2 Estándar?   ¿Enviado de extremo a extremo?
LS2                                       1             3             sí                 sí
LS2 Encriptado                            1             5             no                  no
Meta LS2                                  1             7             sí                 no
Registro de Servicio                      n/a           9             sí                 no
Lista de Servicios                        4            11             no                 no



Notas
`````
- Los tipos de búsqueda son actualmente bits 3-2 en el Mensaje de Búsqueda de Base de Datos. 
  Cualquier tipo adicional requeriría el uso del bit 4.

- Todos los tipos de almacenamiento son impares ya que los bits superiores en el campo 
  de tipo de Mensaje de Almacenamiento de Base de Datos son ignorados por routers antiguos.
  Preferiríamos que el análisis fallara como un LS en lugar de como un RI comprimido.

- ¿El tipo debe ser explícito o implícito o ninguno de los dos en los datos cubiertos 
  por la firma?



### Proceso de Búsqueda/Almacenamiento

Los tipos 3, 5 y 7 pueden ser devueltos en respuesta a una búsqueda estándar de leaseset 
(tipo 1). 
El tipo 9 nunca se devuelve en respuesta a una búsqueda. 
El tipo 11 se devuelve en respuesta a un nuevo tipo de búsqueda de servicio (tipo 11).

Solo el tipo 3 puede ser enviado en un mensaje de ajo de cliente a cliente.



### Formato

Los tipos 3, 7 y 9 tienen un formato común::

  Encabezado LS2 Estándar
  - como se define a continuación

  Parte Específica del Tipo
  - como se define a continuación en cada parte

  Firma LS2 Estándar:
  - Longitud según lo implicado por el tipo de firma de clave de firma

El tipo 5 (Encriptado) no comienza con un Destino y tiene un formato diferente. 
Ver abajo.

El tipo 11 (Lista de Servicios) es una agregación de varios Registros de Servicios y tiene un 
formato diferente. Ver abajo.


### Consideraciones de Privacidad/Seguridad

PENDIENTE



## Encabezado LS2 Estándar

Los tipos 3, 7 y 9 usan el encabezado LS2 estándar, especificado a continuación:


### Formato
::

  Encabezado LS2 Estándar:
  - Tipo (1 byte)
    No está realmente en el encabezado, pero forma parte de los datos cubiertos por la firma.
    Se toma del campo en el Mensaje de Almacenamiento de Base de Datos.
  - Destino (387+ bytes)
  - Marca de tiempo publicada (4 bytes, big endian, segundos desde la época, se reinicia en 2106)
  - Expira (2 bytes, big endian) (desplazamiento desde la marca de tiempo publicada en segundos, 
    máx 18.2 horas)
  - Banderas (2 bytes)
    Orden de bits: 15 14 ... 3 2 1 0
    Bit 0: Si es 0, sin claves fuera de línea; si es 1, claves fuera de línea
    Bit 1: Si es 0, un leaseset estándar publicado.
           Si es 1, un leaseset no publicado. No debe ser inundado, publicado, 
           o enviado en respuesta a una consulta. Si este leaseset expira, 
           no consultar la netdb para uno nuevo, a menos que se configure el bit 2.
    Bit 2: Si es 0, un leaseset estándar publicado.
           Si es 1, este leaseset no encriptado será cegado y encriptado al ser publicado.
           Si este leaseset expira, consulta la ubicación cegada en la netdb para uno nuevo.
           Si este bit se establece en 1, establece el bit 1 en 1 también.
           Desde la versión 0.9.42.
    Bits 3-15: establecer en 0 para compatibilidad con usos futuros
  - Si la bandera indica claves fuera de línea, la sección de firma fuera de línea:
    Marca de tiempo Expira (4 bytes, big endian, segundos desde la época, se reinicia en 2106)
    Tipo de firma transitoria (2 bytes, big endian)
    Clave pública de firma transitoria (longitud como se implica por el tipo de firma)
    Firma de la marca de tiempo de expiración, tipo de firma transitoria y clave pública,
    por la clave pública de destino,
    longitud como se implica por el tipo de firma de la clave pública de destino.
    Esta sección puede, y debe, generarse fuera de línea.


Justificación
`````````````

- No publicado/publicado: Para el uso al enviar un almacén de base de datos de extremo a extremo,
  el router emisor puede desear indicar que este leaseset no debería enviarse a otros. 
  Actualmente usamos heurísticas para mantener este estado.

- Publicado: Reemplaza la lógica compleja requerida para determinar la 'versión' del
  leaseset. Actualmente, la versión es la expiración del último arrendamiento que expira, 
  y un router de publicación debe incrementar esa expiración al menos en 1ms cuando
  publica un leaseset que solo elimina un arrendamiento anterior.

- Expira: Permite la expiración de una entrada en la netdb más temprana que la de
  su último arrendamiento que expira. Puede que no sea útil para LS2, 
  donde se espera que leasesets queden con una expiración máxima de 11 minutos, pero
  para otros tipos nuevos, es necesario (ver Meta LS y Registro de Servicio a continuación).

- Claves fuera de línea son opcionales, para reducir la complejidad de implementación 
  inicial/requerida.


### Problemas

- Podría reducir aún más la precisión de la marca de tiempo (¿10 minutos?) 
  pero tendríamos que añadir número de versión. 
  Esto podría romper el multihoming, a menos que tengamos cifrado preservador de orden.
  Probablemente no se pueda hacer sin marcas de tiempo.

- Alternativa: marca de tiempo de 3 bytes (época / 10 minutos), número de versión de 1 byte, 
  expiración de 2 bytes

- ¿El tipo es explícito o implícito en datos / firma? ¿Constantes de "dominio" para la firma?


Notas
`````

- Los routers no deben publicar un LS más de una vez por segundo.
  Si lo hacen, deben incrementar artificialmente la marca de tiempo publicada en 1
  sobre el LS publicado previamente.

- Las implementaciones de routers podrían almacenar en caché las claves transitorias 
  y la firma para evitar la verificación cada vez. En particular, floodfills y routers en ambos extremos 
  de conexiones de larga duración podrían beneficiarse de esto.

- Las claves y firmas offline solo son apropiadas para destinos de larga duración,
  es decir, servidores, no clientes.



## Nuevos tipos de DatabaseEntry


### LeaseSet 2

Cambios del LeaseSet existente:

- Añadir marca de tiempo publicada, marca de tiempo de expiración, banderas y propiedades
- Añadir tipo de cifrado
- Eliminar clave de revocación

Búsqueda con
    Bandera de LS estándar (1)
Almacenar con
    Tipo de LS2 estándar (3)
Almacenar en
    Hash del destino
    Este hash luego se usa para generar la "clave de ruteo" diaria, como en LS1
Expiración típica
    10 minutos, como en un LS regular.
Publicado por
    Destino

Formato
``````
::

  Encabezado LS2 Estándar como se especifica arriba

  Parte Específica del Tipo LS2 Estándar
  - Propiedades (Mapeado como especificado en la especificación de estructuras comunes, 2 bytes cero si no hay ninguna)
  - Número de secciones de claves a seguir (1 byte, máximo TBD)
  - Secciones de claves:
    - Tipo de cifrado (2 bytes, big endian)
    - Longitud de clave de cifrado (2 bytes, big endian)
      Esto es explícito, por lo que los floodfills pueden analizar LS2 con tipos de cifrado desconocidos.
    - Clave de cifrado (número de bytes especificado)
  - Número de lease2 (1 byte)
  - Lease2s (40 bytes cada uno)
    Estas son arrendamientos, pero con una expiración de 4 bytes en lugar de 8 bytes,
    segundos desde la época (se reinicia en 2106)

  Firma LS2 Estándar:
  - Firma
    Si la bandera indica claves fuera de línea, esto es firmado por la clave pública transitoria,
    de lo contrario, por la clave pública de destino.
    Longitud como se implica por el tipo de firma de clave de firma.
    La firma es de todo lo anterior.




Justificación
`````````````

- Propiedades: Expansión y flexibilidad futuras.
  Colocadas primero por si es necesario para el análisis de los datos restantes.

- Múltiples pares tipo de cifrado/claves públicas son
  para facilitar la transición a nuevos tipos de cifrado. La otra forma de hacerlo
  es publicar múltiples leasesets, posiblemente usando los mismos túneles,
  como lo hacemos ahora para destinos DSA y EdDSA.
  La identificación del tipo de cifrado entrante en un túnel
  puede hacerse con el mecanismo de etiqueta de sesión existente,
  y/o con intentos de descifrado utilizando cada clave. Las longitudes de los mensajes entrantes
  también pueden proporcionar una pista.

Discusión
``````````

Esta propuesta continúa usando la clave pública en el leaseset para la
clave de cifrado de extremo a extremo, y deja el campo de clave pública en 
el Destino sin usar, como está ahora. El tipo de cifrado no está especificado
en el certificado de clave de Destino, permanecerá en 0.

Una alternativa rechazada es especificar el tipo de cifrado en el certificado de clave de Destino,
usar la clave pública en el Destino, y no usar la clave pública
en el leaseset. No planeamos hacer esto.

Beneficios de LS2:

- La ubicación de la clave pública real no cambia.
- El tipo de cifrado, o la clave pública, puede cambiar sin cambiar el Destino.
- Elimina el campo de revocación no utilizado
- Compatibilidad básica con otros tipos de DatabaseEntry en esta propuesta
- Permitir múltiples tipos de cifrado

Desventajas de LS2:

- La ubicación de la clave pública y el tipo de cifrado difiere de RouterInfo
- Mantiene la clave pública no utilizada en el leaseset
- Requiere implementación en toda la red; en la alternativa, pueden
  usarse tipos de cifrado experimentales, si son permitidos por floodfills
  (pero ver propuestas relacionadas 136 y 137 sobre soporte para tipos de firma experimentales).
  La propuesta alternativa podría ser más fácil de implementar y probar para tipos
  de cifrado experimentales.


Nuevos problemas de cifrado
```````````````````````````
Algunas de estas cuestiones están fuera de alcance para esta propuesta,
pero colocando notas aquí por ahora ya que no tenemos
una propuesta separada de cifrado todavía.
Ver también las propuestas de ECIES 144 y 145.

- El tipo de cifrado representa la combinación
  de curva, longitud de clave, y esquema de extremo a extremo,
  incluyendo KDF y MAC, si hay.

- Hemos incluido un campo de longitud de clave, para que el LS2 sea
  analizable y verificable por el floodfill incluso para tipos de cifrado desconocidos.

- El primer tipo de cifrado nuevo que se propondrá probablemente será ECIES/X25519. 
  Cómo se usa de extremo a extremo (ya sea una versión ligeramente modificada de ElGamal/AES+Etiqueta de Sesión
  o algo completamente nuevo, p.ej. ChaCha/Poly) se especificará
  en una o varias propuestas separadas.
  Ver también las propuestas de ECIES 144 y 145.


Notas
`````
- Expiración de 8 bytes en arrendamientos cambiada a 4 bytes.

- Si alguna vez implementamos la revocación, podemos hacerlo con un campo de expiración en cero,
  o cero arrendamientos, o ambos. No hay necesidad de una clave de revocación separada.

- Las claves de cifrado están en orden de preferencia del servidor, de mayor preferencia primero. 
  El comportamiento por defecto del cliente es seleccionar la primera clave con 
  un tipo de cifrado compatible. Los clientes pueden utilizar otros algoritmos de selección 
  basados en el soporte de cifrado, rendimiento relativo y otros factores.


### LS2 Encriptado

Metas:

- Añadir cegamiento
- Permitir múltiples tipos de firma
- No requerir nuevos primitivos de cifrado
- Opcionalmente cifrar a cada destinatario, revocable
- Apoyar la encriptación de LS2 Estándar y Meta LS2 solo

LS2 Encriptado nunca se envía en un mensaje de ajo de extremo a extremo.
Utiliza el LS2 estándar arriba.


Cambios del LeaseSet encriptado existente:

- Encriptar todo para seguridad
- Encriptar de manera segura, no solo con AES.
- Encriptar a cada destinatario

Búsqueda con
    Bandera de LS estándar (1)
Almacenar con
    Tipo de LS2 Encriptado (5)
Almacenar en
    Hash de tipo de firma cegada y clave pública cegada
    Dos byte tipo de firma (big endian, por ej. 0x000b) || clave pública cegada
    Este hash luego se usa para generar la "clave de ruteo" diaria, como en LS1
Expiración típica
    10 minutos, como en un LS regular, u horas, como en un meta LS.
Publicado por
    Destino


Definiciones
`````````````
Definimos las siguientes funciones correspondientes a los bloques de construcción criptográficos 
utilizados para LS2 encriptados:

CSRNG(n)
    Salida de n bytes de un generador de números aleatorios criptográficamente seguros.

    Además del requisito de que CSRNG sea criptográficamente seguro (y, por lo tanto,
    adecuado para generar material clave), DEBE ser seguro 
    para que alguna salida de n bytes se utilice como material clave cuando las secuencias de bytes 
    inmediatamente precedentes y siguientes a ella sean expuestas en la red 
    (tales como en una sal, o padding encriptado). Las implementaciones que 
    dependen de una fuente potencialmente poco fiable deberían aplanar
    cualquier salida que deba exponerse en la red [PRNG-REFS]_.

H(p, d)
    Función hash SHA-256 que toma una cadena de personalización p y datos d, y
    produce una salida de longitud de 32 bytes.

    Utilizar SHA-256 como sigue::

        H(p, d) := SHA-256(p || d)

STREAM
    El cifrador de flujo ChaCha20 como se especifica en [RFC-7539-S2.4]_, con el contador inicial
    establecido en 1. S_KEY_LEN = 32 y S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Cifra el texto sin formato usando la clave k, y el nonce iv que DEBE ser único para 
        la clave k. Devuelve un texto cifrado que tiene el mismo tamaño que el texto sin formato.

        Todo el texto cifrado debe ser indistinguible de aleatorio si la clave es privada.

    DECRYPT(k, iv, ciphertext)
        Descifra el texto cifrado usando la clave k, y el nonce iv. Devuelve el texto sin formato.


SIG
    El esquema de firmas RedDSA (correspondiente a SigType 11) con cegamiento de clave.
    Tiene las siguientes funciones:

    DERIVE_PUBLIC(privkey)
        Devuelve la clave pública correspondiente a la clave privada dada.

    SIGN(privkey, m)
        Devuelve una firma por la clave privada privkey sobre el mensaje dado m.

    VERIFY(pubkey, m, sig)
        Verifica la firma sig contra la clave pública pubkey y el mensaje m. Devuelve
        verdadero si la firma es válida, falso de otro modo.

    También debe soportar las siguientes operaciones de cegamiento de clave:

    GENERATE_ALPHA(data, secret)
        Genera alpha para aquellos que conocen los datos y un secreto opcional.
        El resultado debe estar distribuido según las claves privadas.

    BLIND_PRIVKEY(privkey, alpha)
        Ciega una clave privada, usando un secreto alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Ciega una clave pública, usando un secreto alpha.
        Para un par de claves dado (privkey, pubkey) debe cumplirse el siguiente relación::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH
    Sistema de acuerdo de claves públicas X25519. Claves privadas de 32 bytes, claves públicas de 32
    bytes, produce salidas de 32 bytes. Tiene las siguientes
    funciones:

    GENERATE_PRIVATE()
        Genera una nueva clave privada.

    DERIVE_PUBLIC(privkey)
        Devuelve la clave pública correspondiente a la clave privada dada.

    DH(privkey, pubkey)
        Genera un secreto compartido a partir de las claves privadas y públicas dadas.

HKDF(salt, ikm, info, n)
    Una función de derivación de clave criptográfica que toma algún material de entrada ikm (que
    debería tener buena entropía pero no requiere ser una cadena aleatoria)
    uniforme), una sal de longitud 32 bytes, y un valor de 'info' específico del 
    contexto, y produce una salida de n bytes adecuada para usarse como material clave.

    Utilizar HKDF como se especifica en [RFC-5869]_, utilizando la función hash HMAC 
    SHA-256 como se especifica en [RFC-2104]_. Esto significa que SALT_LEN es 32 bytes máx.


Formato
``````
El formato de LS2 encriptado consiste en tres capas anidadas:

- Una capa exterior que contiene la información en texto plano necesaria 
  para almacenamiento y recuperación.
- Una capa intermedia que maneja la autenticación de cliente.
- Una capa interior que contiene los datos reales de LS2.

El formato general se ve como::

    Datos de la Capa 0 + Enc(datos de la capa 1 + Enc(datos de la capa 2)) + Firma

Tenga en cuenta que LS2 encriptado está cegado. El Destino no está en el encabezado.
La ubicación de almacenamiento DHT es SHA-256(tipo de sig || clave pública cegada), y se rota diariamente.

NO utilice el encabezado LS2 estándar especificado arriba.

#### Capa 0 (exterior)
Tipo
    1 byte

    No está realmente en el encabezado, sino parte de los datos cubiertos por la firma.
    Se toma del campo en el Mensaje de Almacenamiento de Base de Datos.

Tipo de Sig de Clave Pública Cegada
    2 bytes, big endian
    Esto siempre será tipo 11, identificando una clave cegada Red25519.

Clave Pública Cegada
    Longitud como se implica por el tipo de sig

Marca de tiempo publicada
    4 bytes, big endian

    Segundos desde la época, se reinicia en 2106

Expira
    2 bytes, big endian

    Desplazamiento desde la marca de tiempo publicada en segundos, máx 18.2 horas

Banderas
    2 bytes

    Orden de bits: 15 14 ... 3 2 1 0

    Bit 0: Si es 0, sin claves fuera de línea; si es 1, claves fuera de línea

    Otros bits: Establecidos en 0 para compatibilidad con usos futuros

Datos de clave transitoria
    Presentes si la bandera indica claves fuera de línea

    Marca de tiempo expiran
        4 bytes, big endian

        Segundos desde la época, se reinicia en 2106

    Tipo de firma transitoria
        2 bytes, big endian

    Clave pública de firma transitoria
        Longitud como se implica por el tipo de firma

    Firma
        Longitud como se implica por el tipo de clave pública cegada

        Sobre marca de tiempo expiran, tipo firma transitoria, y clave pública.

        Verificado con la clave pública cegada.

lenOuterCiphertext
    2 bytes, big endian

outerCiphertext
    lenOuterCiphertext bytes

    Datos de capa 1 encriptados. Ver más abajo para derivación de clave y algoritmos de cifrado.

Firma
    Longitud como se implica por el tipo de sig de la clave de firma usada

    La firma es de todo lo anterior.

    Si la bandera indica claves fuera de línea, la firma se verifica con la llave pública transitoria. 
    De lo contrario, la firma se verifica con la clave pública cegada.


#### Capa 1 (intermedio)
Banderas
    1 byte
    
    Orden de bits: 76543210

    Bit 0: 0 para todos, 1 para cliente por cliente, sección de autenticación a seguir

    Bits 3-1: Esquema de autenticación, solo si bit 0 está establecido en 1 para cliente por cliente, 
              de lo contrario 000
              000: autenticación de clientes DH (o sin autenticación cliente por cliente)
              001: autenticación de clientes PSK

    Bits 7-4: Sin usar, establecer en 0 para compatibilidad futura

Datos de autenticación de clientes DH
    Presentes si el bit de bandera 0 está establecido en 1 y los bits de bandera 3-1 están establecidos en 000.

    clavePublicaEfimera
        32 bytes

    clientes
        2 bytes, big endian

        Número de entradas de autorización de cliente a seguir, 40 bytes cada una

    clienteAuth
        Datos de autorización para un solo cliente.
        Ver más abajo para el algoritmo de autorización por cliente.

        clienteID_i
            8 bytes

        clienteCookie_i
            32 bytes

Datos de autenticación de clientes PSK
    Presentes si el bit de bandera 0 está establecido en 1 y los bits de bandera 3-1 están establecidos en 001.

    authSalt
        32 bytes

    clientes
        2 bytes, big endian

        Número de entradas de autorización de cliente a seguir, 40 bytes cada una

    clienteAuth
        Datos de autorización para un solo cliente.
        Ver más abajo para el algoritmo de autorización por cliente.

        clienteID_i
            8 bytes

        clienteCookie_i
            32 bytes


innerCiphertext
    Longitud implícita por lenOuterCiphertext (cualquier dato que quede)

    Datos de la capa 2 encriptados. Ver más abajo para derivación de clave y algoritmos de cifrado.


#### Capa 2 (interna)
Tipo
    1 byte

    Ya sea 3 (LS2) o 7 (Meta LS2)

Datos
    Datos de LeaseSet2 para el dado tipo.

    Incluye el encabezado y la firma.


Derivación de Clave de Cegamiento
`````````````````````````````````

Utilizamos el siguiente esquema de cegamiento de claves,
basado en Ed25519 y ZCash RedDSA [ZCASH]_.
Las firmas Red25519 se realizan sobre la curva Ed25519, usando SHA-512 para el hash.

No usamos el anexo A.2 [TOR-REND-SPEC-V3]_ de rend-spec-v3.txt de Tor,
que tiene metas de diseño similares, porque sus claves públicas cegadas 
pueden estar fuera del subgrupo de orden principal, con implicaciones de seguridad desconocidas.


#### Metas

- Clave pública de firma en destino sin cegar debe ser
  Ed25519 (tipo de sig 7) o Red25519 (tipo de sig 11);
  no se admiten otros tipos de sig
- Si la clave pública de firma está fuera de línea, la clave pública de firma transitoria también debe estar en Ed25519
- El cegamiento es computacionalmente simple
- Utilizar primitivos criptográficos existentes
- Las claves públicas cegadas no pueden ser desenmascaradas
- Las claves públicas cegadas deben estar en la curva Ed25519 y subgrupo de orden principal
- Se debe conocer la clave pública de firma del destino
  (el destino completo no es requerido) para derivar la clave pública cegada
- Proporcionar opcionalmente un secreto adicional requerido para derivar la clave pública cegada


#### Seguridad

La seguridad de un esquema de cegamiento requiere que la
distribución de alpha es la misma que las claves privadas sin cegar.
Sin embargo, cuando cegamos una clave privada Ed25519 (sig type 7)
a una clave privada Red25519 (sig type 11), la distribución es diferente.
Para cumplir con los requisitos de la sección 4.1.6.1 [ZCASH]_,
Red25519 (sig type 11) debería usarse también para las claves no cegadas,
para que "la combinación de una clave pública re-aleatorizada y firma(s)
bajo esa clave no revelan la clave de la que fue re-aleatorizada."
Permitimos el tipo 7 para destinos existentes, pero recomendamos
el tipo 11 para nuevos destinos que serán encriptados.



#### Definiciones

B
    El punto base Ed25519 (generador) 2^255 - 19 como en [ED25519-REFS]_

L
    El orden Ed25519 2^252 + 27742317777372353535851937790883648493
    como en [ED25519-REFS]_

DERIVE_PUBLIC(a)
    Convertir una clave privada en pública, como en Ed25519 (multiplicar por G)

alpha
    Un número aleatorio de 32 bytes conocido por aquellos que conocen el destino.

GENERATE_ALPHA(destination, date, secret)
    Generar alpha para la fecha actual, para aquellos que conocen el destino y el secreto.
    El resultado debe estar distribuido como claves privadas Ed25519.

a
    La clave privada de firma de 32 bytes no cegada EdDSA o RedDSA utilizada 
    para firmar el destino

A
    La clave pública de firma de 32 bytes no cegada EdDSA o RedDSA en el destino,
    = DERIVE_PUBLIC(a), como en Ed25519

a'
    La clave privada de firma de 32 bytes cegada EdDSA utilizada para firmar el 
    leaseset encriptado
    Esta es una clave privada válida EdDSA.

A'
    La clave pública de firma de 32 bytes cegada EdDSA en el Destino,
    puede ser generada con DERIVE_PUBLIC(a'), o desde A y alpha.
    Esta es una clave pública válida EdDSA, en la curva y en el subgrupo de orden principal.

LEOS2IP(x)
    Invierte el orden de los bytes de entrada a little-endian

H*(x)
    32 bytes = (LEOS2IP(SHA512(x))) mod B, igual que en Ed25519 hash-and-reduce


#### Cálculos de Cegamiento

Una nueva alfa secreta y claves cegadas deben ser generadas 
cada día (UTC).
El secreto alfa y las claves cegadas se calculan como sigue.

GENERATE_ALPHA(destination, date, secret), para todas las partes:

  ```text
// GENERATE_ALPHA(destination, date, secret)

  // El secreto es opcional, de lo contrario de longitud cero
  A = clave pública de firma del destino
  stA = tipo de firma de A, 2 bytes big endian (0x0007 o 0x000b)
  stA' = tipo de firma de clave pública cegada A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD de la fecha actual UTC
  secret = cadena codificada UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // trata la seed como un valor little-endian de 64 bytes
  alpha = seed mod L
```

BLIND_PRIVKEY(), para el propietario que publica el leaseset:

  ```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // Si para una clave privada Ed25519 (tipo 7)
  seed = clave privada de firma del destino
  a = mitad izquierda de SHA512(seed) y recortada como de costumbre para Ed25519
  // en caso contrario, para una clave privada Red25519 (tipo 11)
  a = clave privada de firma del destino
  // Adición utilizando aritmética escalar
  clave privada de firma cegada = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  clave pública de firma cegada = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), para los clientes que recuperan el leaseset:

  ```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = clave pública de firma del destino
  // Adición utilizando elementos del grupo (puntos en la curva)
  clave pública cegada = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Ambos métodos de calcular A' producen el mismo resultado, como se requiere.



#### Firma

El leaseset no cegado es firmado por la clave privada de firma Ed25519 o Red25519 sin cegar
y verificado con la clave pública de firma Ed25519 o Red25519 no cegada (tipos de sig 7 o 11) como de costumbre.

Si la clave pública de firma está fuera de línea,
el leaseset no cegado es firmado por la clave privada de firma transitoria Ed25519 o Red25519 no cegada
y verificado con la clave pública de firma transitoria Ed25519 o Red25519 no cegada (tipos de sig 7 o 11) como de costumbre.
Véase abajo para notas adicionales sobre claves fuera de línea para leasesets encriptados.

Para la firma del leaseset encriptado, utilizamos Red25519, basado en RedDSA [ZCASH]_
para firmar y verificar con claves cegadas.
Las firmas Red25519 se realizan sobre la curva Ed25519, usando SHA-512 para el hash.

Red25519 es idéntico a Ed25519 estándar salvo por lo especificado a continuación.


#### Cálculos de Firma/Verificación

La parte exterior del leaseset encriptado utiliza claves y firmas Red25519.

Red25519 es casi idéntico a Ed25519. Hay dos diferencias:

Las claves privadas Red25519 se generan a partir de números aleatorios y luego deben ser reducidas modulo L, donde L está definido arriba.
Las claves privadas Ed25519 se generan a partir de números aleatorios y luego se "recortan" usando
enmascaramiento bit a los bytes 0 y 31. Esto no se hace para Red25519.
Las funciones GENERATE_ALPHA() y BLIND_PRIVKEY() definidas arriba generan
claves privadas Red25519 correctas utilizando mod L.

En Red25519, el cálculo de r para firmar utiliza datos aleatorios adicionales, 
y usa el valor de la clave pública en lugar del hash de la clave privada.
Debido a los datos aleatorios, cada firma Red25519 es diferente, incluso
al firmar los mismos datos con la misma clave.

Firmando:

  ```text
T = 80 bytes aleatorios
  r = H*(T || clave pública || mensaje)
  // el resto es igual que en Ed25519
```

Verificación:

  ```text
// igual que en Ed25519
```



Cifrado y procesamiento
```````````````````````
#### Derivación de subcredenciales
Como parte del proceso de cegamiento, necesitamos asegurar que un LS2 encriptado solo
puede ser descifrado por alguien que conozca la clave pública de firma correspondiente 
del Destino.
El destino completo no es requerido.
Para lograr esto, derivamos una credencial de la clave pública de firma:

  ```text
A = clave pública de firma del destino
  stA = tipo de firma de A, 2 bytes big endian (0x0007 o 0x000b)
  stA' = tipo de firma de A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```

La cadena de personalización asegura que la credencial no colisione con ningún hash 
usado como clave de búsqueda DHT, como el hash de Destino simple.

Para una clave cegada dada, entonces podemos derivar una subcredencial:

  ```text
subcredential = H("subcredential", credential || clavePublicaCegada)
```

La subcredencial se incluye en los procesos de derivación de clave a continuación, lo que une esas
claves al conocimiento de la clave pública de firma del Destino.

#### Cifrado de la Capa 1
Primero, se prepara la entrada al proceso de derivación de clave:

  ```text
outerInput = subcredential || marcaDeTiempoPublicada
```

Luego, se genera una sal aleatoria:

  ```text
outerSalt = CSRNG(32)
```

Luego, se deriva la clave utilizada para cifrar la capa 1:

  ```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Finalmente, se encripta y se serialize el texto plano de la capa 1:

  ```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

#### Descifrado de la Capa 1
La sal se analiza del texto cifrado de la capa 1:

  ```text
outerSalt = outerCiphertext[0:31]
```

Luego, se deriva la clave usada para cifrar la capa 1:

  ```text
outerInput = subcredential || marcaDeTiempoPublicada
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Finalmente, se descifra el texto cifrado de la capa 1:

  ```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

#### Cifrado de la Capa 2
Cuando la autorización de cliente está habilitada, ``authCookie`` se calcula como se describe a continuación.
Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el arreglo de bytes de longitud cero.

El cifrado procede de forma similar a la capa 1:

  ```text
innerInput = authCookie || subcredential || marcaDeTiempoPublicada
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

#### Descifrado de la Capa 2
Cuando la autorización de cliente está habilitada, ``authCookie`` se calcula como se describe a continuación.
Cuando la autorización de cliente está deshabilitada, ``authCookie`` es el arreglo de bytes de longitud cero.

El descifrado procede de forma similar a la capa 1:

  ```text
innerInput = authCookie || subcredential || marcaDeTiempoPublicada
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```


Autorización por cliente
``````````````````````
Cuando la autorización de cliente está habilitada para un Destino, el servidor mantiene una lista de
clientes que están autorizando para descifrar los datos del LS2 encriptado. Los datos almacenados por cliente
depende del mecanismo de autorización, e incluye alguna forma de material clave que cada
cliente genera y envía al servidor a través de un mecanismo seguro out-of-band.

Existen dos alternativas para implementar la autorización por cliente:

#### Autorización de cliente DH
Cada cliente genera un par de claves DH ``[csk_i, cpk_i]``, y envía la clave pública ``cpk_i``
al servidor.

Procesamiento del servidor
^^^^^^^^^^^^^^^^^
El servidor genera un nuevo ``authCookie`` y un par de claves DH efímero:

  ```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```

Luego, para cada cliente autorizado, el servidor encripta ``authCookie`` a su clave pública:

  ```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || marcaDeTiempoPublicada
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

El servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` en la capa 1 del
LS2 encriptado, junto con ``epk``.

Procesamiento del cliente
^^^^^^^^^^^^^^^^^
El cliente utiliza su clave privada para derivar su identificador de cliente esperado ``clientID_i``,
clave de cifrado ``clientKey_i``, y IV de cifrado ``clientIV_i``:

  ```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || marcaDeTiempoPublicada
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Luego el cliente busca en los datos de autorización de la capa 1 una entrada que contenga
``clientID_i``. Si existe una entrada coincidente, el cliente la descifra para obtener
``authCookie``:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Autorización de cliente con clave precompartida
Cada cliente genera una clave secreta de 32 bytes ``psk_i``, y la envía al servidor.
Alternativamente, el servidor puede generar la clave secreta, y enviarla a uno o más clientes.


Procesamiento del servidor
^^^^^^^^^^^^^^^^^
El servidor genera un nuevo ``authCookie`` y una sal:

  ```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```

Luego, para cada cliente autorizado, el servidor encripta ``authCookie`` a su clave precompartida:

  ```text
authInput = psk_i || subcredential || marcaDeTiempoPublicada
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

El servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` en la capa 1 del
LS2 encriptado, junto con ``authSalt``.

Procesamiento del cliente
^^^^^^^^^^^^^^^^^
El cliente usa su clave precompartida para derivar su identificador de cliente esperado ``clientID_i``,
clave de cifrado ``clientKey_i``, y IV de cifrado ``clientIV_i``:

  ```text
authInput = psk_i || subcredential || marcaDeTiempoPublicada
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Luego el cliente busca en los datos de autorización de la capa 1 una entrada que contenga
``clientID_i``. Si existe una entrada coincidente, el cliente la descifra para obtener
``authCookie``:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Consideraciones de seguridad
Ambos mecanismos de autorización de cliente anteriores proporcionan privacidad para la membresía de cliente.
Una entidad que solo conoce el Destino puede ver cuántos clientes están suscritos en cualquier
momento, pero no puede rastrear qué clientes están siendo añadidos o revocados.

Los servidores DEBERÍAN aleatorizar el orden de los clientes cada vez que generan un LS2 encriptado, para
evitar que los clientes aprendan su posición en la lista e infieran cuándo otros clientes han
sido añadidos o revocados.

Un servidor PUEDE elegir ocultar el número de clientes que están suscritos insertando entradas
aleatorias en la lista de datos de autorización.

Ventajas de la autorización de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- La seguridad del esquema no depende solamente del intercambio fuera de banda de material clave de cliente.
  La clave privada del cliente nunca necesita salir de su dispositivo, y por lo tanto un
  adversario que pueda interceptar el intercambio fuera de banda, pero no pueda romper el algoritmo DH,
  no puede descifrar el LS2 encriptado, o determinar cuánto tiempo el cliente tiene acceso.

Desventajas de la autorización de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Requiere N + 1 operaciones DH en el lado del servidor para N clientes.
- Requiere una operación DH en el lado del cliente.
- Requiere que el cliente genere la clave secreta.

Ventajas de la autorización de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- No requiere operaciones DH.
- Permite al servidor generar la clave secreta.
- Permite al servidor compartir la misma clave con varios clientes, si
  así se desea.

Desventajas de la autorización de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- La seguridad del esquema es críticamente dependiente del intercambio fuera de banda de
  material clave de cliente. Un adversario que intercepte el intercambio
  para un cliente particular puede descifrar cualquier LS2 encriptado
  posterior para el cual ese cliente está autorizado, así como determinar
  cuando se revoca el acceso del cliente.


LS encriptado con Direcciones Base 32
`````````````````````````````````````

Ver propuesta 149.

No se puede usar un LS2 encriptado para bittorrent, debido a respuestas compactas de anuncio
que son de 32 bytes. Los 32 bytes contienen solo el hash. No hay espacio para una
indicación de que el leaseset está encriptado, o los tipos de firma.



LS encriptado con Claves Offline
``````````````````````````````
Para leasesets encriptados con claves offline, las claves privadas cegadas deben también generarse fuera de línea,
una por cada día.

Como el bloque de firma offline opcional está en la parte en claro del leaseset encriptado,
cualquiera raspando los floodfills podría usar esto para rastrear el leaseset (pero no descifrarlo)
durante varios días.
Para prevenir esto, el propietario de las claves debe generar nuevas claves transitorias
para cada día también.
Tanto las claves transitorias como las cegadas pueden generarse con antelación, y proporcionarse al router
en un lote.

No hay un formato de archivo definido en esta propuesta para empacar múltiples claves transitorias y
cegadas y proporcionarlas al cliente o router.
No hay un protocolo de I2CP definido en esta propuesta para soportar
leasesets encriptados con claves offline.



Notas
`````

- Un servicio usando leasesets encriptados publicaría la versión encriptada a los
  floodfills. Sin embargo, para eficiencia, enviaría leasesets no encriptados a
  los clientes en el mensaje de ajo encapsulado, una vez autenticados (vía whitelist, por ejemplo).

- Los floodfills pueden limitar el tamaño máximo a un valor razonable para evitar abusos.

- Después de descifrar, se deben realizar varias verificaciones, incluyendo que
  la marca de tiempo y expiración interna coincidan con las del nivel superior.

- ChaCha20 se seleccionó sobre AES. Mientras que las velocidades son similares si el
  soporte de hardware AES está disponible, ChaCha20 es 2.5-3x más rápida cuando
  el soporte de hardware AES no está disponible, como en dispositivos ARM de gama baja.

- No nos importa lo suficiente la velocidad para usar BLAKE2b con clave. Tiene un tamaño 
  de salida lo suficientemente grande para acomodar el n más grande que requerimos 
  (o podemos llamarlo una vez por llave deseada con un argumento contador). 
  BLAKE2b es mucho más rápido que SHA-256, y BLAKE2b con clave reduciría 
  el número total de llamadas a la función hash. 
  Sin embargo, ver propuesta 148, donde se propone que pasemos a BLAKE2b por otras razones.
  [UNSCIENTIFIC-KDF-SPEEDS]_


### Meta LS2

Esto se usa para reemplazar el multihoming. Como cualquier leaseset, esto está firmado por el
creador. Esta es una lista autenticada de hashes de destino.

El Meta LS2 es el nivel superior de, y posiblemente nodos intermedios de,
una estructura de árbol.
Contiene una serie de entradas, cada una apuntando a un LS, LS2, o otro Meta LS2
para soportar multihoming masivo.
Un Meta LS2 puede contener una mezcla de entradas LS, LS2 y Meta LS2.
Las hojas del árbol siempre son un LS o LS2.
El árbol es un DAG; los bucles están prohibidos; los clientes que buscan deben detectar y
negarse a seguir bucles.

Un Meta LS2 puede tener una expiración mucho más larga que un LS o LS2 estándar.
El nivel superior puede tener una expiración varias horas después de la fecha de publicación.
El tiempo máximo de expiración será impuesto por floodfills y clientes, y está TBD.

El caso de uso para Meta LS2 es el multihoming masivo, pero sin más
protección para la correlación de routers a leasesets (en el momento del reinicio del router) de la que
se proporciona ahora con LS o LS2.
Esto es equivalente al caso de uso de "facebook", que probablemente no necesita
protección de correlación. Este caso de uso probablemente necesita claves offline,
que se proporcionan en el encabezado estándar en cada nodo del árbol.

El protocolo de backend para la coordinación entre los routers de hoja, nodos intermedios y maestros firmantes de Meta LS
no se especifica aquí. Los requisitos son extremadamente simples: solo verificar que el par está activo,
y publicar un nuevo LS cada pocas horas. La única complejidad es para seleccionar nuevos
publicadores para los Meta LS de nivel superior o intermedio en caso de fallo.

Leasesets combinados donde los arrendamientos de varios routers se combinan, firman y publican
en un único leaseset están documentados en la propuesta 140, "multihoming invisible".
Esta propuesta es inviable tal como está escrita, porque las conexiones de streaming no serían
"adhesivas" a un único router, ver http://zzz.i2p/topics/2335 .

El protocolo de backend, y la interacción con los internos del router y cliente, sería
bastante compleja para multihoming invisible.

Para evitar sobrecargar el floodfill para el Meta LS de nivel superior, la expiración debería
ser de varias horas al menos. Los clientes deben almacenar en caché el Meta LS de nivel superior, y
perpetuarlo a través de reinicios si no ha expirado.

Necesitamos definir algún algoritmo para los clientes para recorrer el árbol, incluidos los fallbacks,
para que el uso esté disperso. Alguna función de distancia hash, costo y aleatoriedad.
Si un nodo tiene tanto LS o LS2 como Meta LS, necesitamos saber cuándo está permitido
usar esos leasesets, y cuándo seguir recorriendo el árbol.




Búsqueda con
    Bandera de LS estándar (1)
Almacenar con
    Tipo de Meta LS2 (7)
Almacenar en
    Hash del destino
    Este hash luego se usa para generar la "clave de ruteo" diaria, como en LS1
Expiración típica
    Horas. Máx 18.2 horas (65535 segundos)
Publicado por
    Destino "maestro" o coordinador, o coordinadores intermedios

Formato
``````
::

  Encabezado LS2 Estándar como se especifica arriba

  Parte Específica del Tipo de Meta LS2
  - Propiedades (Mapeado como especificado en la especificación de estructuras comunes, 2 bytes cero si no hay ninguna)
  - Número de entradas (1 byte) Máximo TBD
  - Entradas. Cada entrada contiene: (40 bytes)
    - Hash (32 bytes)
    - Banderas (2 bytes)
      TBD. Establecer todos en cero para compatibilidad con usos futuros.
    - Tipo (1 byte) El tipo de LS al que está haciendo referencia;
      1 para LS, 3 para LS2, 5 para encriptado, 7 para meta, 0 para desconocido.
    - Costo (prioridad) (1 byte)
    - Expira (4 bytes) (4 bytes, big endian, segundos desde la época, se reinicia en 2106)
  - Número de revocaciones (1 byte) Máximo TBD
  - Revocaciones: Cada revocación contiene: (32 bytes)
    - Hash (32 bytes)

  Firma LS2 Estándar:
  - Firma (40+ bytes)
    La firma es de todo lo anterior.

Banderas y propiedades: para uso futuro


Notas
`````
- Un servicio distribuido que utilice esto tendría uno o más "maestros" con el
  clave privada del destino del servicio. Determinarían (fuera de banda) la
  lista actual de destinos activos y publicarían el Meta LS2. Para
  redundancia, múltiples maestros podrían multihome (es decir, publicar simultáneamente) el
  Meta LS2.

- Un servicio distribuido podría comenzar con un único destino o usar multihoming de estilo antiguo,
  y luego hacer la transición a un Meta LS2. Una búsqueda de LS estándar podría devolver
  cualquiera de un LS, LS2, o Meta LS2.

- Cuando un servicio usa un Meta LS2, no tiene túneles (arrendamientos).


### Registro de Servicio

Este es un registro individual que dice que un destino está participando en un
servicio. Se envía del participante al floodfill. Nunca se envía
individualmente por un floodfill, sino solo como parte de una Lista de Servicios. El Registro
de Servicio también se usa para revocar la participación en un servicio, estableciendo la
expiración en cero.

Este no es un LS2 pero usa el formato de encabezado y firma LS2 estándar.

Búsqueda con
    n/a, ver Lista de Servicios
Almacenar con
    Tipo de Registro de Servicio (9)
Almacenar en
    Hash del nombre del servicio
    Este hash luego se usa para generar la "clave de ruteo" diaria, como en LS1
Expiración típica
    Horas. Máx 18.2 horas (65535 segundos)
Publicado por
    Destino

Formato
``````
::

  Encabezado LS2 Estándar como se especifica arriba

  Parte Específica del Tipo de Registro de Servicio
  - Puerto (2 bytes, big endian) (0 si no especificado)
  - Hash del nombre del servicio (32 bytes)

  Firma LS2 Estándar:
  - Firma (40+ bytes)
    La firma es de todo lo anterior.


Notas
`````
- Si expira está en ceros, el floodfill debería revocar el registro y ya no
  incluirlo en la lista de servicios.

- Almacenamiento: El floodfill puede limitar estrictamente el almacenamiento de estos registros y
  limitar el número de registros almacenados por hash y su expiración. Una lista blanca
  de hashes también puede ser usada.

- Cualquier otro tipo de netdb en el mismo hash tiene prioridad, por lo que un registro de servicio nunca
  puede sobrescribir un LS/RI, pero un LS/RI sobrescribirá todos los registros de servicio en ese hash.



### Lista de Servicios

Esto no es nada como un LS2 y utiliza un formato diferente.

La lista de servicio es creada y firmada por el floodfill. No está autenticada
en el sentido de que cualquiera puede unirse a un servicio publicando un Registro de Servicio a
un floodfill.

Una Lista de Servicios contiene Registros de Servicios Cortos, no Registros de Servicios completos. Estos
contienen firmas pero solo hashes, no destinos completos, por lo que no pueden
ser verificados sin el destino completo.

La seguridad, si la hay, y la deseabilidad de listas de servicios están TBD.
Los floodfills podrían limitar la publicación, y las búsquedas, a una lista blanca de servicios,
pero esa lista blanca puede variar según la implementación, o según la preferencia del operador.
Podría no ser posible alcanzar un consenso sobre una lista blanca común base
entre implementaciones.

Si el nombre del servicio se incluye en el registro de servicio arriba,
entonces los operadores de floodfill podrían objetar; si solo se incluye el hash,
no hay verificación, y un registro de servicio podría "entrar" antes de
cualquier otro tipo de netdb y ser almacenado en floodfill.

Búsqueda con
    Tipo de búsqueda de Lista de Servicios (11)
Almacenar con
    Tipo de Lista de Servicios (11)
Almacenar en
    Hash del nombre del servicio
    Este hash luego se usa para generar la "clave de ruteo" diaria, como en LS1
Expiración típica
    Horas, no especificada en la lista misma, hasta la política local
Publicado por
    Nadie, nunca enviado a floodfill, nunca inundado.

Formato
``````
NO utiliza el encabezado LS2 estándar especificado arriba.

::

  - Tipo (1 byte)
    No está realmente en el encabezado, sino parte de los datos cubiertos por la firma.
    Se toma del campo en el Mensaje de Almacenamiento de Base de Datos.
  - Hash del nombre del servicio (implícito, en el mensaje de Almacenamiento de Base de Datos)
  - Hash del Creador (floodfill) (32 bytes)
  - Marca de tiempo publicada (8 bytes, big endian)

  - Número de Registros de Servicios Cortos (1 byte)
  - Lista de Registros de Servicios Cortos:
    Cada Registro de Servicios Cortos contiene (90+ bytes)
    - Hash Dest (32 bytes)
    - Marca de tiempo publicada (8 bytes, big endian)
    - Expira (4 bytes, big endian) (desplazamiento desde publicación en ms)
    - Banderas (2 bytes)
    - Puerto (2 bytes, big endian)
    - Longitud de firma (2 bytes, big endian)
    - Firma del dest (40+ bytes)

  - Número de Registros de Revocación (1 byte)
  - Lista de Registros de Revocación:
    Cada Registro de Revocación contiene (86+ bytes)
    - Hash Dest (32 bytes)
    - Marca de tiempo publicada (8 bytes, big endian)
    - Banderas (2 bytes)
    - Puerto (2 bytes, big endian)
    - Longitud de firma (2 bytes, big endian)
    - Firma del dest (40+ bytes)

  - Firma del floodfill (40+ bytes)
    La firma es de todo lo anterior.

Para verificar la firma de la Lista de Servicios:

- anteponer el hash del nombre del servicio
- quitar el hash del creador
- Comprobar la firma de los contenidos modificados

Para verificar la firma de cada Registro de Servicios Cortos:

- Obtener destino
- Comprobar la firma de (marca de tiempo publicada + expira + banderas + puerto + Hash del
  nombre del servicio)

Para verificar la firma de cada Registro de Revocación:

- Obtener destino
- Comprobar la firma de (marca de tiempo publicada + 4 bytes ceros + banderas + puerto + Hash
  del nombre del servicio)

Notas
`````
- Usamos longitud de firma en lugar de tipo de sig para que podamos soportar tipos de firma desconocidos.

- No hay expiración de una lista de servicios, los destinatarios pueden tomar su propia
  decisión basada en la política o la expiración de los registros individuales.

- Las Listas de Servicios no se inundan, solo los Registros de Servicios individuales sí. 
  Cada floodfill crea, firma y almacena en caché una Lista de Servicios. 
  El floodfill usa su propia política para el tiempo de almacenamiento en caché y el
  número máximo de registros de servicio y revocación.


## Cambios Requeridos en Especificaciones de Estructuras Comunes


### Certificados de Clave

Fuera de alcance para esta propuesta.
Añadir a las propuestas ECIES 144 y 145.


### Nuevas Estructuras Intermedias

Añadir nuevas estructuras para Lease2, MetaLease, LeaseSet2Header, 
y OfflineSignature.
Efectivo a partir de la versión 0.9.38.


### Nuevos Tipos de NetDB

Añadir estructuras para cada nuevo tipo de leaseset, incorporado desde arriba.
Para LeaseSet2, EncryptedLeaseSet, y MetaLeaseSet,
efectivo a partir de la versión 0.9.38.
Para Registro de Servicio y Lista de Servicios,
preliminar y no programado.


### Nuevo Tipo de Firma

Añadir RedDSA_SHA512_Ed25519 Tipo 11.
La clave pública es de 32 bytes; la clave privada es de 32 bytes; el hash es de 64 bytes; la firma es de 64 bytes.



## Cambios Requeridos en Especificaciones de Cifrado

Fuera de alcance para esta propuesta.
Ver propuestas 144 y 145.



## Cambios Requeridos en I2NP

Añadir nota: LS2 solo puede ser publicado a floodfills con una versión mínima.


### Mensaje de Búsqueda de Base de Datos

Añadir el tipo de búsqueda de lista de servicios.

Cambios
```````
::

  Byte de banderas: campo de tipo de búsqueda, actualmente
  bits 3-2, se expande a bits 4-2.
  Tipo de búsqueda 0x04 se define como la búsqueda de lista de servicios.

  Añadir nota: La búsqueda de lista de servicios sólo puede enviarse a floodfills con una versión mínima.
  La versión mínima es 0.9.38.


### Mensaje de Almacenamiento de Base de Datos

Añadir todos los nuevos tipos de almacenamiento.

Cambios
```````
::

  Byte de tipo: Campo de tipo, actualmente bit 0, se expande a bits 3-0.
  Tipo 3 se define como un almacenamiento LS2.
  Tipo 5 se define como un almacenamiento LS2 encriptado.
  Tipo 7 se define como un almacenamiento Meta LS2.
  Tipo 9 se define como un almacenamiento de registro de servicio.

  Tipo 11 se define como un almacenamiento de lista de servicios.
  Otros tipos están indefinidos e inválidos.

  Añadir nota: Todos los nuevos tipos solo pueden publicarse a floodfills con una versión mínima.
  La versión mínima es 0.9.38.




## Cambios Requeridos en I2CP


### Opciones I2CP

Nuevas opciones interpretadas lado del router, enviadas en mapeo SessionConfig:

::

  i2cp.leaseSetType=nnn       El tipo de leaseset a ser enviado en el Mensaje de Crear Leaseset
                              El valor es el mismo que el tipo de almacenamiento netdb en
                              la tabla anterior.
                              Interpretado lado del cliente, pero también pasado al router en el
                              SessionConfig, para declarar la intención y verificar el soporte.

  i2cp.leaseSetEncType=nnn[,nnn]  Los tipos de cifrado a ser usados.
                                  Interpretado lado del cliente, pero también pasado al router en
                                  el SessionConfig, para declarar la intención y verificar el soporte.
                                  Ver propuestas 144 y 145.

  i2cp.leaseSetOfflineExpiration=nnn  La expiración de la firma offline, ASCII,
                                      segundos desde la época.

  i2cp.leaseSetTransientPublicKey=[type:]b64  El base 64 de la clave privada transitoria,
                                              prefijado por un número de tipo de firma opcional
                                              o nombre, predeterminado DSA_SHA1.
                                              Longitud como inferido por el tipo de firma

  i2cp.leaseSetOfflineSignature=b64   El base 64 de la firma offline.
                                      Longitud como inferido por el tipo de clave pública
                                      de destino

  i2cp.leaseSetSecret=b64     El base 64 de un secreto usado para cegar la
                              dirección del leaseset, predeterminado ""

  i2cp.leaseSetAuthType=nnn   El tipo de autenticación para LS2 encriptado.
                              0 para sin autenticación cliente por cliente (el defecto)
                              1 para autenticación cliente por cliente DH
                              2 para autenticación cliente por cliente PSK

  i2cp.leaseSetPrivKey=b64    Una clave privada de base 64 para ser usada por el router para
                              descifrar el LS2 encriptado,
                              solo si la autenticación cliente por cliente está habilitada


Nuevas opciones interpretadas lado del cliente:

::

  i2cp.leaseSetType=nnn     El tipo de leaseset a ser enviado en el Mensaje de Crear Leaseset
                            El valor es el mismo que el tipo de almacenamiento netdb en
                            la tabla anterior.
                            Interpretado lado del cliente, pero también pasado al router en el
                            SessionConfig, para declarar la intención y verificar el soporte.

  i2cp.leaseSetEncType=nnn[,nnn]  Los tipos de cifrado a ser usados.
                                  Interpretado lado del cliente, pero también pasado al router en
                                  el SessionConfig, para declarar la intención y verificar el soporte.
                                  Ver propuestas 144 y 145.

  i2cp.leaseSetSecret=b64     El base 64 de un secreto usado para cegar la
                              dirección del leaseset, predeterminado ""

  i2cp.leaseSetAuthType=nnn       El tipo de autenticación para LS2 encriptado.
                                  0 para sin autenticación cliente por cliente (el defecto)
                                  1 para autenticación cliente por cliente DH
                                  2 para autenticación cliente por cliente PSK

  i2cp.leaseSetBlindedType=nnn   El tipo de firma de la clave cegada para LS2 encriptado.
                                 El predeterminado depende del tipo de sig del destino.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   El base 64 del nombre del cliente (ignorado, solo uso UI),
                                                 seguido por ':', seguido por el base 64 de la clave pública
                                                 para usar para autenticación cliente por cliente DH. nnn empieza con 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   El base 64 del nombre del cliente (ignorado, solo uso UI),
                                                   seguido por ':', seguido por el base 64 de la clave privada
                                                   para usar para autenticación cliente por cliente PSK. nnn empieza con 0

### Configuración de Sesión

Tenga en cuenta que para las firmas offline, las opciones
i2cp.leaseSetOfflineExpiration,
i2cp.leaseSetTransientPublicKey, y
i2cp.leaseSetOfflineSignature son necesarias,
y la firma es por la clave de firma transitoria privada.



### Mensaje de Solicitud de Leaseset

Router a cliente.
Sin cambios.
Los arrendamientos se envían con marcas de tiempo de 8 bytes, incluso si el
leaseset devuelto será un LS2 con marcas de tiempo de 4 bytes.
Tenga en cuenta que la respuesta puede ser un Mensaje de Crear Leaseset o Mensaje de Crear Leaseset2.



### Mensaje de Solicitud de Leaseset Variable

Router a cliente.
Sin cambios.
Los arrendamientos se envían con marcas de tiempo de 8 bytes, incluso si el
leaseset devuelto será un LS2 con marcas de tiempo de 4 bytes.
Tenga en cuenta que la respuesta puede ser un Mensaje de Crear Leaseset o Mensaje de Crear Leaseset2.



### Mensaje de Creación de
