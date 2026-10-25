---
title: "La Base de Datos de Red"
description: "Entendiendo la base de datos de red distribuida (netDb) de I2P - una DHT especializada para información de contacto de routers y búsquedas de destinos"
slug: "network-database"
aliases:
  - "/es/how_networkdatabase"
  - "/es/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Resumen

La netDb de I2P es una base de datos distribuida especializada que contiene solo dos tipos de datos: información de contacto del router (**RouterInfos**) e información de contacto del destino (**LeaseSets**). Cada pieza de datos está firmada por la parte apropiada y verificada por cualquiera que la use o almacene. Además, los datos contienen información de vitalidad, lo que permite descartar entradas irrelevantes, reemplazar entradas más antiguas con otras más nuevas y protección contra ciertas clases de ataques.

La netDb se distribuye con una técnica simple llamada "floodfill", donde un subconjunto de todos los routers, llamados "floodfill routers", mantiene la base de datos distribuida.

---

## RouterInfo

Cuando un router I2P quiere contactar con otro router, necesita conocer algunas piezas clave de datos - todas las cuales son empaquetadas y firmadas por el router en una estructura llamada "RouterInfo", que se distribuye con el SHA256 de la identidad del router como clave. La estructura en sí contiene:

- La identidad del router (una clave de cifrado, una clave de firma y un certificado)
- Las direcciones de contacto en las que se puede alcanzar
- Cuándo fue publicado esto
- Un conjunto de opciones de texto arbitrarias
- La firma de lo anterior, generada por la clave de firma de la identidad

### Opciones Esperadas

Las siguientes opciones de texto, aunque no son estrictamente obligatorias, se espera que estén presentes:

- **caps** (Flags de capacidades - usado para indicar participación floodfill, ancho de banda aproximado, y alcanzabilidad percibida)
  - **D**: Congestión media (desde la versión 0.9.58)
  - **E**: Congestión alta (desde la versión 0.9.58)
  - **f**: Floodfill
  - **G**: Rechazando todos los túneles (desde la versión 0.9.58)
  - **H**: Oculto
  - **K**: Menos de 12 KBps de ancho de banda compartido
  - **L**: 12 - 48 KBps de ancho de banda compartido (por defecto)
  - **M**: 48 - 64 KBps de ancho de banda compartido
  - **N**: 64 - 128 KBps de ancho de banda compartido
  - **O**: 128 - 256 KBps de ancho de banda compartido
  - **P**: 256 - 2000 KBps de ancho de banda compartido (desde la versión 0.9.20, ver nota abajo)
  - **R**: Alcanzable
  - **U**: No alcanzable
  - **X**: Más de 2000 KBps de ancho de banda compartido (desde la versión 0.9.20, ver nota abajo)

"Ancho de banda compartido" == (porcentaje compartido %) * min(ancho de banda entrada, ancho de banda salida)

Para compatibilidad con routers más antiguos, un router puede publicar múltiples letras de ancho de banda, por ejemplo "PO".

Nota: el límite entre las clases de ancho de banda P y X puede ser 2000 o 2048 KBps, a elección del implementador.

- **netId** = 2 (Compatibilidad básica de red - Un router se negará a comunicarse con un peer que tenga un netId diferente)
- **router.version** (Usado para determinar compatibilidad con características y mensajes más nuevos)

Notas sobre las capacidades R/U: Un router normalmente debería publicar la capacidad R o U, a menos que el estado de accesibilidad sea actualmente desconocido. R significa que el router es directamente accesible (no se requieren introducers, no está detrás de firewall) en al menos una dirección de transporte. U significa que el router NO es directamente accesible en NINGUNA dirección de transporte.

Opciones obsoletas: - ~~coreVersion~~ (Nunca se utilizó, eliminado en la versión 0.9.24) - ~~stat_uptime~~ = 90m (No se utiliza desde la versión 0.7.9, eliminado en la versión 0.9.24)

Estos valores son utilizados por otros routers para decisiones básicas. ¿Deberíamos conectarnos a este router? ¿Deberíamos intentar enrutar un tunnel a través de este router? La bandera de capacidad de ancho de banda, en particular, se utiliza únicamente para determinar si el router cumple con un umbral mínimo para enrutar tunnels. Por encima del umbral mínimo, el ancho de banda anunciado no se usa ni se confía en ninguna parte del router, excepto para mostrar en la interfaz de usuario y para depuración y análisis de red.

Números de NetID válidos:

| Uso | Número NetID |
|-------|--------------|
| Reservado | 0 |
| Reservado | 1 |
| Red Actual (predeterminada) | 2 |
| Redes Futuras Reservadas | 3 - 15 |
| Bifurcaciones y Redes de Prueba | 16 - 254 |
| Reservado | 255 |
### Opciones Adicionales

Las opciones de texto adicionales incluyen un pequeño número de estadísticas sobre la salud del router, las cuales son agregadas por sitios como [stats.i2p](http://stats.i2p/) para análisis de rendimiento de red y depuración. Estas estadísticas fueron elegidas para proporcionar datos cruciales para los desarrolladores, como las tasas de éxito de construcción de tunnel, mientras se equilibra la necesidad de dichos datos con los efectos secundarios que podrían resultar de revelar esta información. Las estadísticas actuales se limitan a:

- Tasas de éxito, rechazo y tiempo de espera de construcción de túneles exploratorios
- Promedio de 1 hora del número de túneles participantes

Estas son opcionales, pero si se incluyen, ayudan al análisis del rendimiento de toda la red. A partir de la API 0.9.58, estas estadísticas se simplifican y estandarizan, de la siguiente manera:

- Las claves de opción son stat_(nombre_estadística).(período_estadística)
- Los valores de opción están separados por ';'
- Las estadísticas para conteos de eventos o porcentajes normalizados utilizan el 4º valor; los primeros tres valores no se usan pero deben estar presentes
- Las estadísticas para valores promedio utilizan el 1º valor, y no se requiere separador ';'
- Para una ponderación equitativa de todos los routers en el análisis de estadísticas, y para anonimato adicional, los routers deben incluir estas estadísticas solo después de un tiempo de actividad de una hora o más, y solo una vez cada 16 veces que se publique el RI.

Ejemplo:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Los routers floodfill pueden publicar datos adicionales sobre el número de entradas en su base de datos de red. Estos son opcionales, pero si se incluyen, ayudan al análisis del rendimiento de toda la red.

Las siguientes dos opciones deben ser incluidas por los routers floodfill en cada RI publicado:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Ejemplo:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Los datos publicados se pueden ver en la interfaz de usuario del router, pero no son utilizados ni confiables para ningún otro router.

### Opciones de Familia

A partir de la versión 0.9.24, los routers pueden declarar que forman parte de una "familia", operada por la misma entidad. Múltiples routers de la misma familia no se utilizarán en un único tunnel.

Las opciones de familia son:

- **family** (El nombre de la familia)
- **family.key** El código de tipo de firma de la [Clave Pública de Firma](/docs/specs/common-structures/#type_SigningPublicKey) de la familia (en dígitos ASCII) concatenado con ':' concatenado con la Clave Pública de Firma en base 64
- **family.sig** La firma de ((nombre de familia en UTF-8) concatenado con (hash del router de 32 bytes)) en base 64

### Expiración de RouterInfo

Los RouterInfos no tienen un tiempo de expiración establecido. Cada router es libre de mantener su propia política local para equilibrar la frecuencia de las búsquedas de RouterInfo con el uso de memoria o disco. En la implementación actual, existen las siguientes políticas generales:

- No hay expiración durante la primera hora de funcionamiento, ya que los datos almacenados de forma persistente pueden estar desactualizados.
- No hay expiración si hay 25 o menos RouterInfos.
- A medida que crece el número de RouterInfos locales, el tiempo de expiración se reduce, en un intento de mantener un número razonable de RouterInfos. El tiempo de expiración con menos de 120 routers es de 72 horas, mientras que el tiempo de expiración con 300 routers es de alrededor de 30 horas.
- Los RouterInfos que contienen introducers [SSU](/docs/legacy/ssu/) expiran en aproximadamente una hora, ya que la lista de introducers expira en aproximadamente ese tiempo.
- Los floodfills usan un tiempo de expiración corto (1 hora) para todos los RouterInfos locales, ya que los RouterInfos válidos serán republicados frecuentemente en ellos.

### Almacenamiento Persistente de RouterInfo

Los RouterInfos se escriben periódicamente al disco para que estén disponibles después de un reinicio.

Puede ser deseable almacenar persistentemente Meta LeaseSets con expiraciones largas. Esto depende de la implementación.

### Véase También

- [Especificación de RouterInfo](/docs/specs/common-structures/#struct_RouterInfo)
- [Javadoc de RouterInfo](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

La segunda pieza de datos distribuida en el netDb es un "LeaseSet" - que documenta un grupo de **puntos de entrada de túnel (leases)** para un destino de cliente particular. Cada uno de estos leases especifica la siguiente información:

- El router de puerta de enlace del tunnel (especificando su identidad)
- El ID del tunnel en ese router para enviar mensajes (un número de 4 bytes)
- Cuándo expirará ese tunnel.

El leaseSet en sí se almacena en la netDb bajo la clave derivada del SHA256 del destino. Una excepción son los Encrypted LeaseSets (LS2), a partir de la versión 0.9.38. Se utiliza el SHA256 del byte de tipo (3) seguido de la clave pública ciega para la clave DHT, y luego se rota como es habitual. Ver la sección Métrica de Proximidad Kademlia a continuación.

Además de estos leases, el LeaseSet incluye:

- El destino en sí mismo (una clave de cifrado, una clave de firma y un certificado)
- Clave pública de cifrado adicional: utilizada para el cifrado extremo a extremo de mensajes garlic
- Clave pública de firma adicional: destinada para la revocación de leaseSet, pero actualmente no se utiliza.
- Firma de todos los datos del leaseSet, para asegurar que el destino publicó el leaseSet.

- [Especificación de Lease](/docs/specs/common-structures/#struct_Lease)
- [Especificación de LeaseSet](/docs/specs/common-structures/#struct_LeaseSet)
- [Javadoc de Lease](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [Javadoc de LeaseSet](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

A partir de la versión 0.9.38, se definen tres nuevos tipos de LeaseSets: LeaseSet2, MetaLeaseSet y EncryptedLeaseSet. Ver más abajo.

### LeaseSets No Publicados

Un LeaseSet para un destino usado solo para conexiones salientes está *no publicado*. Nunca se envía para publicación a un router floodfill. Los tunnels de "Cliente", como aquellos para navegación web y clientes IRC, están no publicados. Los servidores aún podrán enviar mensajes de vuelta a esos destinos no publicados, debido a los [mensajes de almacenamiento I2NP](#leaseset-storage-to-peers).

### LeaseSets Revocados

Un LeaseSet puede ser *revocado* publicando un nuevo LeaseSet con cero leases. Las revocaciones deben estar firmadas por la clave de firma adicional en el LeaseSet. Las revocaciones no están completamente implementadas, y no está claro si tienen algún uso práctico. Este es el único uso planificado para esa clave de firma, por lo que actualmente no se utiliza.

### LeaseSet2 (LS2)

A partir de la versión 0.9.38, los floodfills soportan una nueva estructura LeaseSet2. Esta estructura es muy similar a la antigua estructura LeaseSet, y sirve para el mismo propósito. La nueva estructura proporciona la flexibilidad requerida para soportar nuevos tipos de cifrado, múltiples tipos de cifrado, opciones, claves de firma offline, y otras características. Consulta la propuesta 123 para más detalles.

### Meta LeaseSet (LS2)

A partir de la versión 0.9.38, los floodfills soportan una nueva estructura Meta LeaseSet. Esta estructura proporciona una estructura tipo árbol en la DHT, para referenciar otros LeaseSets. Usando Meta LeaseSets, un sitio puede implementar servicios grandes multihomed, donde varios Destinations diferentes se utilizan para proporcionar un servicio común. Las entradas en un Meta LeaseSet son Destinations u otros Meta LeaseSets, y pueden tener expiraciones largas, hasta 18.2 horas. Usando esta facilidad, debería ser posible ejecutar cientos o miles de Destinations alojando un servicio común. Ver la propuesta 123 para más detalles.

### LeaseSets Cifrados (LS1)

Esta sección describe el método antiguo e inseguro de cifrar LeaseSets usando una clave simétrica fija. Consulta más abajo la versión LS2 de LeaseSets cifrados.

En un LeaseSet *cifrado*, todos los Leases están cifrados con una clave separada. Los leases solo pueden ser decodificados, y por tanto el destino solo puede ser contactado, por aquellos que tengan la clave. No hay ninguna bandera u otra indicación directa de que el LeaseSet esté cifrado. Los LeaseSets cifrados no se usan ampliamente, y es un tema para trabajo futuro investigar si la interfaz de usuario y la implementación de los LeaseSets cifrados podría mejorarse.

### LeaseSets Cifrados (LS2)

A partir de la versión 0.9.38, los floodfills soportan una nueva estructura EncryptedLeaseSet. El Destination está oculto, y solo una clave pública ciega y una expiración son visibles para el floodfill. Solo aquellos que tienen el Destination completo pueden descifrar la estructura. La estructura se almacena en una ubicación DHT basada en el hash de la clave pública ciega, no en el hash del Destination. Ver la propuesta 123 para más detalles.

### Expiración de LeaseSet

Para LeaseSets regulares, la expiración es el momento de la expiración más tardía de sus leases. Para las nuevas estructuras de datos LeaseSet2, la expiración se especifica en el encabezado. Para LeaseSet2, la expiración debe coincidir con la expiración más tardía de sus leases. Para EncryptedLeaseSet y MetaLeaseSet, la expiración puede variar, y se puede aplicar una expiración máxima, por determinar.

### Almacenamiento Persistente de LeaseSet

No se requiere almacenamiento persistente de datos de LeaseSet, ya que expiran muy rápidamente. Sin embargo, puede ser recomendable el almacenamiento persistente de datos de EncryptedLeaseSet y MetaLeaseSet con expiraciones largas.

### Selección de Clave de Cifrado (LS2)

LeaseSet2 puede contener múltiples claves de cifrado. Las claves están ordenadas por preferencia del servidor, siendo la más preferida la primera. El comportamiento predeterminado del cliente es seleccionar la primera clave con un tipo de cifrado soportado. Los clientes pueden usar otros algoritmos de selección basados en el soporte de cifrado, rendimiento relativo y otros factores.

---

## Arranque inicial

El netDb está descentralizado, sin embargo necesitas al menos una referencia a un peer para que el proceso de integración te conecte. Esto se logra mediante "reseeding" de tu router con el RouterInfo de un peer activo - específicamente, recuperando su archivo `routerInfo-$hash.dat` y almacenándolo en tu directorio `netDb/`. Cualquiera puede proporcionarte esos archivos - incluso puedes proporcionárselos a otros exponiendo tu propio directorio netDb. Para simplificar el proceso, voluntarios publican sus directorios netDb (o un subconjunto) en la red regular (no-i2p), y las URLs de estos directorios están codificadas en I2P. Cuando el router se inicia por primera vez, automáticamente descarga de una de estas URLs, seleccionada al azar.

---

## Floodfill

La netDb floodfill es un mecanismo de almacenamiento distribuido simple. El algoritmo de almacenamiento es sencillo: enviar los datos al peer más cercano que se haya anunciado como un router floodfill. Cuando el peer en la netDb floodfill recibe un almacenamiento netDb de un peer que no está en la netDb floodfill, lo envía a un subconjunto de los peers de la netDb floodfill. Los peers seleccionados son los más cercanos (según la [métrica XOR](#kademlia-closeness-metric)) a una clave específica.

Determinar quién forma parte del floodfill netDb es trivial - está expuesto en la routerInfo publicada de cada router como una capacidad.

Los floodfills no tienen una autoridad central y no forman un "consenso" - solo implementan una superposición DHT simple.

### Participación Voluntaria en Router Floodfill

A diferencia de Tor, donde los servidores de directorio están codificados de forma fija y son confiables, y operados por entidades conocidas, los miembros del conjunto de peers floodfill de I2P no necesitan ser confiables y cambian con el tiempo.

Para aumentar la confiabilidad del netDb y minimizar el impacto del tráfico netDb en un router, floodfill se habilita automáticamente solo en routers que están configurados con límites de ancho de banda altos. Los routers con límites de ancho de banda altos (que deben configurarse manualmente, ya que el valor predeterminado es mucho menor) se presume que están en conexiones de menor latencia y es más probable que estén disponibles 24/7. El ancho de banda mínimo compartido actual para un router floodfill es de 128 KBytes/seg.

Además, un router debe pasar varias pruebas adicionales de estado (tiempo de cola de mensajes salientes, retraso de trabajos, etc.) antes de que la operación floodfill se habilite automáticamente.

Con las reglas actuales para la inclusión automática, aproximadamente el 6% de los routers en la red son routers floodfill.

Mientras que algunos peers están configurados manualmente para ser floodfill, otros son simplemente routers de alto ancho de banda que se ofrecen automáticamente como voluntarios cuando el número de peers floodfill cae por debajo de un umbral. Esto previene cualquier daño a largo plazo en la red por perder la mayoría o todos los floodfills debido a un ataque. A su vez, estos peers dejarán de ser floodfill cuando haya demasiados floodfills activos.

### Roles del Router Floodfill

Los únicos servicios adicionales de un router floodfill, además de los de los routers no-floodfill, son aceptar almacenamientos en la netDb y responder a consultas de la netDb. Dado que generalmente tienen un ancho de banda alto, es más probable que participen en un gran número de tunnels (es decir, actúen como "relé" para otros), pero esto no está directamente relacionado con sus servicios de base de datos distribuida.

---

## Métrica de Cercanía Kademlia

La netDb utiliza una métrica XOR simple estilo Kademlia para determinar la proximidad. Para crear una clave Kademlia, se calcula el hash SHA256 de la RouterIdentity o Destination. Una excepción son los Encrypted LeaseSets (LS2), a partir de la versión 0.9.38. El SHA256 del byte de tipo (3) seguido de la clave pública ciega se utiliza para la clave DHT, y luego se rota como de costumbre.

Se realiza una modificación a este algoritmo para aumentar los costos de [ataques Sybil](#sybil-attack-partial-keyspace). En lugar del hash SHA256 de la clave que se busca o almacena, el hash SHA256 se toma de la clave de búsqueda binaria de 32 bytes concatenada con la fecha UTC representada como una cadena ASCII de 8 bytes yyyyMMdd, es decir, SHA256(key + yyyyMMdd). Esto se llama la "routing key", y cambia todos los días a medianoche UTC. Solo la clave de búsqueda se modifica de esta manera, no los hashes de los router floodfill. La transformación diaria del DHT a veces se llama "rotación del keyspace", aunque no es estrictamente una rotación.

Las claves de enrutamiento nunca se envían por la red en ningún mensaje I2NP, solo se utilizan localmente para determinar la distancia.

---

## Segmentación de la Base de Datos de Red - Sub-Bases de Datos

Tradicionalmente, las DHT estilo Kademlia no se preocupan por preservar la no vinculabilidad de la información almacenada en cualquier nodo particular de la DHT. Por ejemplo, una pieza de información puede ser almacenada en un nodo de la DHT, y luego solicitada de vuelta desde ese nodo incondicionalmente. Dentro de I2P y usando la netDb, este no es el caso, la información almacenada en la DHT solo puede ser compartida bajo ciertas circunstancias conocidas donde es "seguro" hacerlo. Esto es para prevenir una clase de ataques donde un actor malicioso puede tratar de asociar un client tunnel con un router enviando un almacenamiento a un client tunnel, y luego solicitándolo de vuelta directamente desde el "Host" sospechoso del client tunnel.

### Estructura de Segmentación

Los routers I2P pueden implementar defensas efectivas contra esta clase de ataque siempre que se cumplan algunas condiciones. Una implementación de base de datos de red debería poder realizar un seguimiento de si una entrada de base de datos fue recibida a través de un tunnel de cliente o directamente. Si fue recibida a través de un tunnel de cliente, entonces también debería realizar un seguimiento de a través de qué tunnel de cliente fue recibida, utilizando el destino local del cliente. Si la entrada fue recibida a través de múltiples tunnels de cliente, entonces la netDb debería realizar un seguimiento de todos los destinos donde se observó la entrada. También debería realizar un seguimiento de si una entrada fue recibida como respuesta a una consulta, o como un almacenamiento.

En las implementaciones tanto de Java como de C++, esto se logra utilizando primero una sola netDb "Principal" para búsquedas directas y operaciones floodfill. Esta netDb principal existe en el contexto del router. Luego, cada cliente recibe su propia versión de la netDb, que se utiliza para capturar entradas de base de datos enviadas a los túneles del cliente y responder a búsquedas enviadas por los túneles del cliente. Llamamos a estas "Bases de Datos de Red del Cliente" o "Sub-Bases de Datos" y existen en el contexto del cliente. La netDb operada por el cliente existe solo durante la vida útil del cliente y contiene únicamente entradas que se comunican con los túneles del cliente. Esto hace imposible que las entradas enviadas por los túneles del cliente se superpongan con las entradas enviadas directamente al router.

Además, cada netDb necesita ser capaz de recordar si una entrada de base de datos fue recibida porque fue enviada a uno de nuestros destinos, o porque fue solicitada por nosotros como parte de una búsqueda. Si una entrada de base de datos fue recibida como un almacenamiento, es decir, algún otro router nos la envió, entonces una netDb debería responder a las solicitudes de la entrada cuando otro router busque la clave. Sin embargo, si fue recibida como una respuesta a una consulta, entonces la netDb solo debería responder a una consulta por la entrada si la entrada ya había sido almacenada en el mismo destino. Un cliente nunca debería responder consultas con una entrada de la netDb principal, solo de su propia base de datos de red del cliente.

Estas estrategias deben tomarse y usarse de forma combinada para que ambas se apliquen. En combinación, "segmentan" la netDb y la protegen contra ataques.

---

## Mecánicas de Almacenamiento, Verificación y Búsqueda

### Almacenamiento de RouterInfo a Peers

Los [I2NP](/docs/specs/i2np/) DatabaseStoreMessages que contienen el RouterInfo local se intercambian con pares como parte de la inicialización de una conexión de transporte [NTCP](/docs/specs/ntcp2/) o [SSU](/docs/specs/ssu2/).

### Almacenamiento de LeaseSet a Pares

Los [I2NP](/docs/specs/i2np/) DatabaseStoreMessages que contienen el leaseSet local se intercambian periódicamente con peers empaquetándolos en un mensaje garlic junto con el tráfico normal del Destination relacionado. Esto permite que una respuesta inicial, y respuestas posteriores, se envíen a un lease apropiado, sin requerir ninguna búsqueda de leaseSet, o requerir que los Destinations que se comunican hayan publicado leaseSets en absoluto.

### Selección de Floodfill

El DatabaseStoreMessage debe enviarse al floodfill que esté más cerca de la clave de enrutamiento actual para el RouterInfo o LeaseSet que se está almacenando. Actualmente, el floodfill más cercano se encuentra mediante una búsqueda en la base de datos local. Incluso si ese floodfill no es realmente el más cercano, lo inundará "más cerca" enviándolo a múltiples otros floodfills. Esto proporciona un alto grado de tolerancia a fallos.

En Kademlia tradicional, un peer haría una búsqueda "find-closest" antes de insertar un elemento en la DHT al objetivo más cercano. Como la operación de verificación tenderá a descubrir floodfills más cercanos si están presentes, un router mejorará rápidamente su conocimiento del "vecindario" de la DHT para el RouterInfo y LeaseSets que publica regularmente. Aunque I2NP no define un mensaje "find-closest", si se vuelve necesario, un router puede simplemente hacer una búsqueda iterativa para una clave con el bit menos significativo invertido (es decir, key ^ 0x01) hasta que no se reciban peers más cercanos en los DatabaseSearchReplyMessages. Esto asegura que se encontrará el peer verdaderamente más cercano incluso si un peer más distante tenía el elemento netDb.

### Almacenamiento de RouterInfo en Floodfills

Un router publica su propia RouterInfo conectándose directamente a un router floodfill y enviándole un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage con un Reply Token diferente de cero. El mensaje no está cifrado con garlic encryption de extremo a extremo, ya que esta es una conexión directa, por lo que no hay routers intermedios (y no hay necesidad de ocultar estos datos de todos modos). El router floodfill responde con un [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, con el Message ID establecido al valor del Reply Token.

En algunas circunstancias, un router también puede enviar el RouterInfo DatabaseStoreMessage a través de un tunnel exploratorio; por ejemplo, debido a límites de conexión, incompatibilidad de conexión, o el deseo de ocultar la IP real del floodfill. El floodfill puede no aceptar tal almacenamiento en momentos de sobrecarga o basándose en otros criterios; si declarar explícitamente ilegal el almacenamiento no directo de un RouterInfo es un tema para estudio posterior.

### Almacenamiento de LeaseSet en Floodfills

El almacenamiento de LeaseSets es mucho más sensible que el de RouterInfos, ya que un router debe asegurarse de que el LeaseSet no pueda asociarse con el router.

Un router publica un LeaseSet local enviando un DatabaseStoreMessage de [I2NP](/docs/specs/i2np/) con un Reply Token distinto de cero a través de un túnel cliente saliente para ese Destination. El mensaje está cifrado end-to-end con garlic encryption usando el Session Key Manager del Destination, para ocultar el mensaje del endpoint saliente del túnel. El router floodfill responde con un DeliveryStatusMessage de [I2NP](/docs/specs/i2np/), con el Message ID establecido al valor del Reply Token. Este mensaje se envía de vuelta a uno de los túneles entrantes del cliente.

### Inundación

Como cualquier router, un floodfill utiliza varios criterios para validar el LeaseSet o RouterInfo antes de almacenarlo localmente. Estos criterios pueden ser adaptativos y depender de las condiciones actuales, incluyendo la carga actual, el tamaño de la netDb y otros factores. Toda validación debe realizarse antes del flooding.

Después de que un router floodfill recibe un DatabaseStoreMessage que contiene un RouterInfo o LeaseSet válido que es más reciente que el previamente almacenado en su NetDb local, lo "inunda". Para inundar una entrada de NetDb, busca varios (actualmente 3) routers floodfill más cercanos a la clave de enrutamiento de la entrada NetDb. (La clave de enrutamiento es el hash SHA256 del RouterIdentity o Destination con la fecha (yyyyMMdd) agregada.) Al inundar a aquellos más cercanos a la clave, no más cercanos a sí mismo, el floodfill asegura que el almacenamiento llegue al lugar correcto, incluso si el router que almacena no tenía buen conocimiento del "vecindario" DHT para la clave de enrutamiento.

El floodfill entonces se conecta directamente a cada uno de esos pares y les envía un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage con un Reply Token de cero. El mensaje no está cifrado con garlic encryption de extremo a extremo, ya que esta es una conexión directa, por lo que no hay routers intermedios (y no hay necesidad de ocultar estos datos de todos modos). Los otros routers no responden ni re-inundan, ya que el Reply Token es cero.

Los floodfills no deben hacer flood a través de túneles; el DatabaseStoreMessage debe enviarse a través de una conexión directa.

Los floodfills nunca deben propagar un LeaseSet expirado o un RouterInfo publicado hace más de una hora.

### Búsqueda de RouterInfo y LeaseSet

El [I2NP](/docs/specs/i2np/) DatabaseLookupMessage se utiliza para solicitar una entrada de netDb de un router floodfill. Las consultas se envían a través de uno de los tunnels exploratorios de salida del router. Las respuestas se especifican para regresar a través de uno de los tunnels exploratorios de entrada del router.

Las búsquedas generalmente se envían a los dos routers floodfill "buenos" (la conexión no falla) más cercanos a la clave solicitada, en paralelo.

Si la clave se encuentra localmente por el router floodfill, responde con un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Si la clave no se encuentra localmente por el router floodfill, responde con un [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage que contiene una lista de otros routers floodfill cercanos a la clave.

Las búsquedas de leaseSet están cifradas end-to-end con garlic encryption desde la versión 0.9.5. Las búsquedas de RouterInfo no están cifradas y por lo tanto son vulnerables al espionaje por parte del punto final saliente (OBEP) del túnel cliente. Esto se debe al costo del cifrado ElGamal. El cifrado de búsquedas de RouterInfo puede habilitarse en una versión futura.

A partir de la versión 0.9.7, las respuestas a una búsqueda de LeaseSet (un DatabaseStoreMessage o un DatabaseSearchReplyMessage) serán cifradas incluyendo la clave de sesión y la etiqueta en la búsqueda. Esto oculta la respuesta del gateway entrante (IBGW) del tunnel de respuesta. Las respuestas a búsquedas de RouterInfo serán cifradas si habilitamos el cifrado de búsqueda.

(Referencia: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Secciones 2.2-2.3 para los términos en cursiva que aparecen a continuación)

Debido al tamaño relativamente pequeño de la red y la redundancia de inundación, las búsquedas suelen ser O(1) en lugar de O(log n). Es muy probable que un router conozca un router floodfill lo suficientemente cercano a la clave para obtener la respuesta en el primer intento. En versiones anteriores a la 0.8.9, los routers usaban una redundancia de búsqueda de dos (es decir, se realizaban dos búsquedas en paralelo a diferentes pares), y no se implementó ni el enrutamiento *recursivo* ni *iterativo* para las búsquedas. Las consultas se enviaban a través de *múltiples rutas simultáneamente* para *reducir la posibilidad de fallo en la consulta*.

A partir de la versión 0.8.9, se implementan *búsquedas iterativas* sin redundancia de búsqueda. Esta es una búsqueda más eficiente y confiable que funcionará mucho mejor cuando no se conocen todos los peers floodfill, y elimina una limitación seria para el crecimiento de la red. A medida que la red crece y cada router conoce solo un pequeño subconjunto de los peers floodfill, las búsquedas se convertirán en O(log n). Incluso si el peer no devuelve referencias más cercanas a la clave, la búsqueda continúa con el peer más cercano siguiente, para mayor robustez, y para prevenir que un floodfill malicioso cree un agujero negro en una parte del espacio de claves. Las búsquedas continúan hasta que se alcance un tiempo de espera total de búsqueda, o se consulte el número máximo de peers.

Los *IDs de nodo* son *verificables* ya que usamos el hash del router directamente tanto como el ID del nodo como la clave de Kademlia. Las respuestas incorrectas que no están más cerca de la clave de búsqueda generalmente se ignoran. Dado el tamaño actual de la red, un router tiene *conocimiento detallado del vecindario del espacio de IDs de destino*.

### Verificación de Almacenamiento de RouterInfo

Nota: La verificación de RouterInfo está deshabilitada desde la versión 0.9.7.1 para prevenir el ataque descrito en el documento [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf). No está claro si la verificación puede rediseñarse para realizarse de forma segura.

Para verificar que un almacenamiento fue exitoso, un router simplemente espera unos 10 segundos, luego envía una consulta a otro floodfill router cercano a la clave (pero no al que se envió el almacenamiento). Las consultas se envían a través de uno de los túneles exploratorios salientes del router. Las consultas están cifradas de extremo a extremo con garlic encryption para prevenir el espionaje por parte del punto final saliente (OBEP).

### Verificación de Almacenamiento de LeaseSet

Para verificar que un almacenamiento fue exitoso, un router simplemente espera aproximadamente 10 segundos, luego envía una consulta a otro router floodfill cercano a la clave (pero no al que se envió el almacenamiento). Las consultas se envían a través de uno de los túneles cliente salientes para el destino del LeaseSet que se está verificando. Para prevenir el espionaje por parte del OBEP del túnel saliente, las consultas están cifradas end-to-end con garlic encryption. Se especifica que las respuestas regresen a través de uno de los túneles entrantes del cliente.

A partir del lanzamiento 0.9.7, las respuestas para búsquedas tanto de RouterInfo como de LeaseSet (un DatabaseStoreMessage o un DatabaseSearchReplyMessage) serán cifradas, para ocultar la respuesta del gateway de entrada (IBGW) del túnel de respuesta.

### Exploración

*Exploration* es una forma especial de búsqueda en netdb, donde un router intenta conocer nuevos routers. Lo hace enviando a un router floodfill un [I2NP](/docs/specs/i2np/) DatabaseLookup Message, buscando una clave aleatoria. Como esta búsqueda fallará, el floodfill normalmente respondería con un [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage que contiene hashes de routers floodfill cercanos a la clave. Esto no sería útil, ya que el router solicitante probablemente ya conoce esos floodfills, y sería poco práctico agregar todos los routers floodfill al campo "no incluir" del DatabaseLookup Message. Para una consulta de exploración, el router solicitante establece una bandera especial en el DatabaseLookup Message. El floodfill entonces responderá únicamente con routers no-floodfill cercanos a la clave solicitada.

### Notas sobre las Respuestas de Búsqueda

La respuesta a una solicitud de búsqueda es ya sea un Mensaje de Almacén de Base de Datos (en caso de éxito) o un Mensaje de Respuesta de Búsqueda de Base de Datos (en caso de fallo). El DSRM contiene un campo de hash del router 'from' para indicar la fuente de la respuesta; el DSM no lo tiene. El campo 'from' del DSRM no está autenticado y puede ser falsificado o inválido. No hay otras etiquetas de respuesta. Por lo tanto, al hacer múltiples solicitudes en paralelo, es difícil monitorear el rendimiento de los diversos routers floodfill.

---

## MultiHoming

Los destinos pueden estar alojados en múltiples routers simultáneamente, utilizando las mismas claves privadas y públicas (tradicionalmente almacenadas en archivos eepPriv.dat). Como ambas instancias publicarán periódicamente sus leaseSets firmados a los peers floodfill, el leaseSet publicado más recientemente será devuelto a un peer que solicite una búsqueda en la base de datos. Como los leaseSets tienen (como máximo) una vida útil de 10 minutos, si una instancia particular se cae, la interrupción será de 10 minutos como máximo, y generalmente mucho menos que eso. La función de multihoming ha sido verificada y está en uso por varios servicios en la red.

A partir de la versión 0.9.38, los floodfills soportan una nueva estructura Meta LeaseSet. Esta estructura proporciona una estructura tipo árbol en el DHT, para hacer referencia a otros LeaseSets. Usando Meta LeaseSets, un sitio puede implementar servicios grandes multihomed, donde varios Destinations diferentes se utilizan para proporcionar un servicio común. Las entradas en un Meta LeaseSet son Destinations u otros Meta LeaseSets, y pueden tener expiraciones largas, hasta 18.2 horas. Usando esta facilidad, debería ser posible ejecutar cientos o miles de Destinations hospedando un servicio común. Ver propuesta 123 para detalles.

---

## Análisis de Amenazas

También se discute en [la página del modelo de amenazas](/docs/overview/threat-model/#floodfill).

Un usuario hostil puede intentar dañar la red creando uno o más routers floodfill y configurándolos para ofrecer respuestas malas, lentas o ninguna respuesta. Algunos escenarios se discuten a continuación.

### Mitigación General a Través del Crecimiento

Actualmente hay alrededor de 1700 floodfill routers en la red. La mayoría de los siguientes ataques se volverán más difíciles, o tendrán menos impacto, a medida que el tamaño de la red y el número de floodfill routers aumenten.

### Mitigación General a Través de Redundancia

Mediante flooding, todas las entradas de netdb se almacenan en los 3 routers floodfill más cercanos a la clave.

### Falsificaciones

Todas las entradas de netDb están firmadas por sus creadores, por lo que ningún router puede falsificar un RouterInfo o LeaseSet.

### Lento o sin respuesta

Cada router mantiene un conjunto ampliado de estadísticas en el [perfil de pares](/docs/overview/peer-selection/) para cada router floodfill, cubriendo varias métricas de calidad para ese par. El conjunto incluye:

- Tiempo de respuesta promedio
- Porcentaje de consultas respondidas con los datos solicitados
- Porcentaje de almacenamientos que fueron verificados exitosamente
- Último almacenamiento exitoso
- Última búsqueda exitosa
- Última respuesta

Cada vez que un router necesita determinar qué floodfill router está más cerca de una clave, utiliza estas métricas para determinar qué floodfill routers son "buenos". Los métodos y umbrales utilizados para determinar la "bondad" son relativamente nuevos y están sujetos a análisis y mejoras adicionales. Aunque un router completamente no responsivo será identificado y evitado rápidamente, los routers que solo son maliciosos a veces pueden ser mucho más difíciles de manejar.

### Ataque Sybil (Espacio de Claves Completo)

Un atacante puede montar un [ataque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) creando un gran número de routers floodfill distribuidos por todo el espacio de claves.

(En un ejemplo relacionado, un investigador creó recientemente un [gran número de relays de Tor](http://blog.torproject.org/blog/june-2010-progress-report).) Si tiene éxito, esto podría ser un ataque DOS efectivo contra toda la red.

Si los floodfills no se están comportando lo suficientemente mal como para ser marcados como "malos" usando las métricas de perfil de pares descritas anteriormente, este es un escenario difícil de manejar. La respuesta de Tor puede ser mucho más ágil en el caso de los relays, ya que los relays sospechosos pueden ser eliminados manualmente del consenso. A continuación se listan algunas posibles respuestas para la red I2P, sin embargo ninguna de ellas es completamente satisfactoria:

- Compilar una lista de hashes de router o IPs maliciosos, y anunciar la lista a través de varios medios (noticias de consola, sitio web, foro, etc.); los usuarios tendrían que descargar manualmente la lista y agregarla a su "lista negra" local.
- Pedirle a todos en la red que habiliten floodfill manualmente (combatir Sybil con más Sybil)
- Lanzar una nueva versión de software que incluya la lista "maliciosa" hardcodeada
- Lanzar una nueva versión de software que mejore las métricas y umbrales del perfil de pares, en un intento de identificar automáticamente los pares "maliciosos".
- Agregar software que descalifique floodfills si demasiados de ellos están en un solo bloque de IP
- Implementar una lista negra automática basada en suscripción controlada por un individuo o grupo único. Esto esencialmente implementaría una porción del modelo de "consenso" de Tor. Desafortunadamente también le daría a un individuo o grupo único el poder de bloquear la participación de cualquier router o IP particular en la red, o incluso de cerrar completamente o destruir toda la red.

Este ataque se vuelve más difícil a medida que el tamaño de la red crece.

### Ataque Sybil (Espacio de Claves Parcial)

Un atacante puede montar un [ataque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) creando un pequeño número (8-15) de routers floodfill agrupados de cerca en el espacio de claves, y distribuir ampliamente los RouterInfos de estos routers. Entonces, todas las búsquedas y almacenamientos para una clave en ese espacio de claves serían dirigidos a uno de los routers del atacante. Si tiene éxito, esto podría ser un ataque DOS efectivo contra un sitio I2P en particular, por ejemplo.

Como el espacio de claves está indexado por el hash criptográfico (SHA256) de la clave, un atacante debe usar un método de fuerza bruta para generar repetidamente hashes de router hasta que tenga suficientes que estén lo suficientemente cerca de la clave. La cantidad de poder computacional requerido para esto, que depende del tamaño de la red, es desconocida.

Como defensa parcial contra este ataque, el algoritmo utilizado para determinar la "cercanía" de Kademlia varía con el tiempo. En lugar de usar el Hash de la clave (es decir, H(k)) para determinar la cercanía, utilizamos el Hash de la clave concatenada con la cadena de fecha actual, es decir, H(k + YYYYMMDD). Una función llamada "generador de clave de enrutamiento" hace esto, que transforma la clave original en una "clave de enrutamiento". En otras palabras, todo el espacio de claves de netdb "rota" cada día a medianoche UTC. Cualquier ataque de espacio de claves parcial tendría que regenerarse cada día, ya que después de la rotación, los routers atacantes ya no estarían cerca de la clave objetivo, ni entre sí.

Este ataque se vuelve más difícil a medida que crece el tamaño de la red. Sin embargo, investigaciones recientes demuestran que la rotación del espacio de claves no es particularmente efectiva. Un atacante puede precalcular numerosos hashes de router con anticipación, y solo unos pocos routers son suficientes para "eclipsar" una porción del espacio de claves dentro de media hora después de la rotación.

Una consecuencia de la rotación diaria del espacio de claves es que la base de datos de red distribuida puede volverse poco confiable durante unos minutos después de la rotación -- las búsquedas fallarán porque el router más "cercano" nuevo aún no ha recibido un almacenamiento. La magnitud del problema y los métodos para mitigarlo (por ejemplo, "transferencias" de netDb a medianoche) son un tema para estudio posterior.

### Ataques de Bootstrap

Un atacante podría intentar arrancar nuevos routers en una red aislada o controlada en su mayoría tomando control de un sitio web de reseed, o engañando a los desarrolladores para que agreguen su sitio web de reseed a la lista codificada en el router.

Varias defensas son posibles, y la mayoría de estas están planeadas:

- No permitir la degradación de HTTPS a HTTP para el reseeding. Un atacante MITM podría simplemente bloquear HTTPS y luego responder al HTTP.
- Incluir datos de reseed en el instalador

Defensas que están implementadas:

- Cambiar la tarea de reseed para obtener un subconjunto de RouterInfos de varios sitios de reseed en lugar de usar solo un sitio único
- Crear un servicio de monitoreo de reseed fuera de la red que sondee periódicamente los sitios web de reseed y verifique que los datos no estén obsoletos o sean inconsistentes con otras vistas de la red
- A partir de la versión 0.9.14, los datos de reseed se empaquetan en un archivo zip firmado y la firma se verifica cuando se descarga. Consulte [la especificación su3](/docs/specs/updates/#su3) para más detalles.

### Captura de Consultas

Ver también [lookup](#routerinfo-and-leaseset-lookup) (Referencia: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Secciones 2.2-2.3 para los términos en cursiva que aparecen a continuación)

Similar a un ataque de bootstrap, un atacante que use un router floodfill podría intentar "dirigir" a los peers hacia un subconjunto de routers controlados por él devolviendo sus referencias.

Es poco probable que esto funcione a través de la exploración, porque la exploración es una tarea de baja frecuencia. Los routers adquieren la mayoría de sus referencias de pares a través de la actividad normal de construcción de tunnels. Los resultados de exploración generalmente se limitan a unos pocos hashes de router, y cada consulta de exploración se dirige a un router floodfill aleatorio.

A partir de la versión 0.8.9, se implementan *búsquedas iterativas*. Para las referencias de router floodfill devueltas en una respuesta DatabaseSearchReplyMessage de [I2NP](/docs/specs/i2np/) a una búsqueda, estas referencias se siguen si están más cerca (o son las siguientes más cercanas) de la clave de búsqueda. El router solicitante no confía en que las referencias estén más cerca de la clave (es decir, son *verificablemente correctas*). La búsqueda tampoco se detiene cuando no se encuentra una clave más cercana, sino que continúa consultando el siguiente nodo más cercano, hasta que se alcance el tiempo límite o el número máximo de consultas. Esto previene que un floodfill malicioso cree un agujero negro en una parte del espacio de claves. Además, la rotación diaria del espacio de claves requiere que un atacante regenere una información de router dentro de la región del espacio de claves deseada. Este diseño asegura que el ataque de captura de consultas descrito en [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) sea mucho más difícil.

### Selección de Relay Basada en DHT

(Referencia: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sección 3)

Esto no tiene mucho que ver con floodfill, pero consulta la [página de selección de pares](/docs/overview/peer-selection/) para una discusión sobre las vulnerabilidades de la selección de pares para túneles.

### Filtraciones de Información

(Referencia: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Sección 3)

Este documento aborda las debilidades en las búsquedas DHT de "Finger Table" utilizadas por Torsk y NISAN. A primera vista, estas no parecen aplicarse a I2P. Primero, el uso de DHT por parte de Torsk y NISAN es significativamente diferente al de I2P. Segundo, las búsquedas de la base de datos de red de I2P solo están vagamente correlacionadas con los procesos de [selección de peers](/docs/overview/peer-selection/) y [construcción de tunnels](/docs/overview/tunnel-routing/); solo se utilizan peers previamente conocidos para los tunnels. Además, la selección de peers no está relacionada con ninguna noción de cercanía de clave DHT.

Algo de esto puede ser realmente más interesante cuando la red I2P se vuelva mucho más grande. En este momento, cada router conoce una gran proporción de la red, por lo que buscar un Router Info particular en la base de datos de red no es una indicación fuerte de una intención futura de usar ese router en un tunnel. Tal vez cuando la red sea 100 veces más grande, la búsqueda pueda ser más correlativa. Por supuesto, una red más grande hace que un ataque Sybil sea mucho más difícil.

Sin embargo, el problema general de la filtración de información de DHT en I2P necesita mayor investigación. Los routers floodfill están en posición de observar consultas y recopilar información. Ciertamente, a un nivel de *f* = 0.2 (20% de nodos maliciosos, como se especifica en el documento) esperamos que muchas de las amenazas Sybil que describimos ([aquí](/docs/overview/threat-model/#sybil), [aquí](#sybil-attack-full-keyspace) y [aquí](#sybil-attack-partial-keyspace)) se vuelvan problemáticas por varias razones.

---

## Historia

[Movido a la página de discusión de netdb](/docs/legacy/netdb/).

---

## Trabajo Futuro

Cifrado extremo a extremo de consultas y respuestas adicionales del netDb.

Mejores métodos para rastrear las respuestas de búsqueda.
