---
title: "Protocolo de la Granja de Ajo"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Abierto"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Visión General

Esta es la especificación del protocolo de la Granja de Ajo,
basado en JRaft, su código "exts" para la implementación sobre TCP,
y su aplicación de ejemplo "dmprinter" [JRAFT](https://github.com/datatechnology/jraft).
JRaft es una implementación del protocolo Raft [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

No pudimos encontrar ninguna implementación con un protocolo documentado de cableado.
Sin embargo, la implementación de JRaft es lo suficientemente simple como para que pudiéramos
inspeccionar el código y luego documentar su protocolo.
Esta propuesta es el resultado de ese esfuerzo.

Este será el backend para la coordinación de routers que publican
entradas en un Meta LeaseSet. Consulte la propuesta 123.


## Objetivos

- Tamaño de código pequeño
- Basado en una implementación existente
- Sin objetos serializados de Java ni ninguna característica o codificación específica de Java
- Cualquier inicio es fuera del alcance. Se supone que al menos otro servidor está codificado de forma estática o configurado fuera de la banda de este protocolo.
- Soporte tanto para casos de uso fuera de banda como en-I2P.


## Diseño

El protocolo Raft no es un protocolo concreto; define solo una máquina de estados.
Por lo tanto, documentamos el protocolo concreto de JRaft y basamos nuestro protocolo en él.
No hay cambios en el protocolo JRaft, aparte de la adición de
un apretón de manos de autenticación.

Raft elige un Líder cuyo trabajo es publicar un registro.
El registro contiene datos de configuración de Raft y datos de aplicación.
Los datos de la aplicación contienen el estado de cada Router del Servidor y el Destino
para el clúster Meta LS2.
Los servidores utilizan un algoritmo común para determinar el editor y el contenido
del Meta LS2.
El editor del Meta LS2 NO es necesariamente el Líder de Raft.


## Especificación

El protocolo de conexión es sobre sockets SSL o sockets I2P no SSL.
Los sockets I2P se proxifican a través del Proxy HTTP.
No hay soporte para sockets no SSL de clearnet.

### Apretón de manos y autenticación

No definido por JRaft.

Objetivos:

- Método de autenticación de usuario/contraseña
- Identificador de versión
- Identificador de clúster
- Extensible
- Facilidad de proxificación cuando se utiliza para sockets I2P
- No exponer innecesariamente el servidor como un servidor de la Granja de Ajo
- Protocolo simple para que no se requiera una implementación completa de servidor web
- Compatible con estándares comunes, para que las implementaciones puedan utilizar
  bibliotecas estándar si se desea

Usaremos un apretón de manos similar al websocket [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) y
autenticación HTTP Digest [RFC-2617](https://tools.ietf.org/html/rfc2617).
La autenticación básica RFC 2617 NO está soportada.
Al proxificar a través del proxy HTTP, comunicar con
el proxy según lo especificado en [RFC-2616](https://tools.ietf.org/html/rfc2616).

#### Credenciales

Si los nombres de usuario y contraseñas son por clúster, o
por servidor, es dependiente de la implementación.


#### Solicitud HTTP 1

El originador enviará lo siguiente.

Todas las líneas se terminan con CRLF como requiere HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(puerto)
  Cache-Control: no-cache
  Connection: close
  (cualquier otro encabezado es ignorado)
  (línea en blanco)

  CLUSTER es el nombre del clúster (por defecto "farm")
  VERSION es la versión de la Granja de Ajo (actualmente "1")
```


#### Respuesta HTTP 1

Si la ruta no es correcta, el destinatario enviará una respuesta estándar "HTTP/1.1 404 Not Found",
como en [RFC-2616](https://tools.ietf.org/html/rfc2616).

Si la ruta es correcta, el destinatario enviará una respuesta estándar "HTTP/1.1 401 Unauthorized",
incluyendo el encabezado de autenticación WWW-Authenticate HTTP digest,
como en [RFC-2617](https://tools.ietf.org/html/rfc2617).

Ambas partes cerrarán entonces el socket.


#### Solicitud HTTP 2

El originador enviará lo siguiente,
como en [RFC-2617](https://tools.ietf.org/html/rfc2617) y [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Todas las líneas se terminan con CRLF como requiere HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(puerto)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (encabezados Sec-Websocket-* si son proxificados)
  Authorization: (encabezado de autorización HTTP digest como en RFC 2617)
  (cualquier otro encabezado es ignorado)
  (línea en blanco)

  CLUSTER es el nombre del clúster (por defecto "farm")
  VERSION es la versión de la Granja de Ajo (actualmente "1")
```


#### Respuesta HTTP 2

Si la autenticación no es correcta, el destinatario enviará otra respuesta estándar "HTTP/1.1 401 Unauthorized",
como en [RFC-2617](https://tools.ietf.org/html/rfc2617).

Si la autenticación es correcta, el destinatario enviará la siguiente respuesta,
como en [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Todas las líneas se terminan con CRLF como requiere HTTP.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (encabezados Sec-Websocket-*)
  (cualquier otro encabezado es ignorado)
  (línea en blanco)
```

Después de que esto es recibido, el socket permanece abierto.
El protocolo Raft definido a continuación comienza, en el mismo socket.


#### Caching

Las credenciales se deben almacenar en caché durante al menos una hora, de modo que
las conexiones subsecuentes puedan saltar directamente a
"Solicitud HTTP 2" arriba.


### Tipos de Mensajes

Hay dos tipos de mensajes, solicitudes y respuestas.
Las solicitudes pueden contener Entradas de Registro, y son de tamaño variable;
las respuestas no contienen Entradas de Registro y tienen un tamaño fijo.

Los tipos de mensajes 1-4 son los mensajes RPC estándar definidos por Raft.
Este es el protocolo central de Raft.

Los tipos de mensajes 5-15 son los mensajes RPC extendidos definidos por
JRaft, para soportar clientes, cambios dinámicos de servidor y
sincronización eficiente de registros.

Los tipos de mensajes 16-17 son los mensajes RPC de Compactación de Registro definidos
en la sección 7 de Raft.


| Mensaje | Número | Enviado Por | Enviado A | Notas |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | Candidato | Seguidor | RPC estándar de Raft; no debe contener entradas de registro |
| RequestVoteResponse | 2 | Seguidor | Candidato | RPC estándar de Raft |
| AppendEntriesRequest | 3 | Líder | Seguidor | RPC estándar de Raft |
| AppendEntriesResponse | 4 | Seguidor | Líder / Cliente | RPC estándar de Raft |
| ClientRequest | 5 | Cliente | Líder / Seguidor | La respuesta es AppendEntriesResponse; debe contener solo entradas de registro de Aplicación |
| AddServerRequest | 6 | Cliente | Líder | Debe contener una única entrada de registro ClusterServer solamente |
| AddServerResponse | 7 | Líder | Cliente | El líder también enviará un JoinClusterRequest |
| RemoveServerRequest | 8 | Seguidor | Líder | Debe contener una única entrada de registro ClusterServer solamente |
| RemoveServerResponse | 9 | Líder | Seguidor | |
| SyncLogRequest | 10 | Líder | Seguidor | Debe contener una única entrada de registro LogPack solamente |
| SyncLogResponse | 11 | Seguidor | Líder | |
| JoinClusterRequest | 12 | Líder | Nuevo Servidor | Invitación a unirse; debe contener una única entrada de registro de Configuración solamente |
| JoinClusterResponse | 13 | Nuevo Servidor | Líder | |
| LeaveClusterRequest | 14 | Líder | Seguidor | Comando para salir |
| LeaveClusterResponse | 15 | Seguidor | Líder | |
| InstallSnapshotRequest | 16 | Líder | Seguidor | Sección 7 de Raft; Debe contener una única entrada de registro SnapshotSyncRequest solamente |
| InstallSnapshotResponse | 17 | Seguidor | Líder | Sección 7 de Raft |


### Establecimiento

Después del apretón de manos HTTP, la secuencia de establecimiento es la siguiente:

```text
Nuevo Servidor Alice              Seguidor Aleatorio Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Si Bob dice que es el líder, continuar como abajo.
  De lo contrario, Alice debe desconectarse de Bob y conectarse al líder.


  Nuevo Servidor Alice              Líder Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       O InstallSnapshotRequest
  SyncLogResponse  ------->
  O InstallSnapshotResponse
```

Secuencia de Desconexión:

```text
Seguidor Alice              Líder Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Secuencia de Elección:

```text
Candidato Alice               Seguidor Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  si Alice gana la elección:

  Líder Alice                Seguidor Bob

  AppendEntriesRequest   ------->
  (latido)
          <---------   AppendEntriesResponse
```


### Definiciones

- Origen: Identifica al originador del mensaje
- Destino: Identifica al receptor del mensaje
- Términos: Ver Raft. Inicializado en 0, aumenta monotonamente
- Índices: Ver Raft. Inicializado en 0, aumenta monotonamente


### Solicitudes

Las solicitudes contienen un encabezado y cero o más entradas de registro.
Las solicitudes contienen un encabezado de tamaño fijo y Entradas de Registro opcionales de tamaño variable.


#### Encabezado de Solicitud

El encabezado de la solicitud es de 45 bytes, como sigue.
Todos los valores son big-endian sin signo.

```dataspec
Tipo de Mensaje:      1 byte
  Origen:            ID, entero de 4 bytes
  Destino:           ID, entero de 4 bytes
  Término:              Término actual (ver notas), entero de 8 bytes
  Último Término de Registro:     entero de 8 bytes
  Último Índice de Registro:    entero de 8 bytes
  Índice de Confirmación:      entero de 8 bytes
  Tamaño de entradas de registro:  Tamaño total en bytes, entero de 4 bytes
  Entradas de registro:       ver abajo, longitud total como especificada
```


#### Notas

En el RequestVoteRequest, Término es el término del candidato.
De lo contrario, es el término actual del líder.

En el AppendEntriesRequest, cuando el tamaño de las entradas de registro es cero,
este mensaje es un mensaje de latido (mantenimiento de conexión).


#### Entradas de Registro

El registro contiene cero o más entradas de registro.
Cada entrada de registro es como sigue.
Todos los valores son big-endian sin signo.

```dataspec
Término:           entero de 8 bytes
  Tipo de Valor:     1 byte
  Tamaño de entrada:     En bytes, entero de 4 bytes
  Entrada:          longitud como especificada
```


#### Contenidos del Registro

Todos los valores son big-endian sin signo.

| Tipo de Valor de Registro | Número |
| :--- | :--- |
| Aplicación | 1 |
| Configuración | 2 |
| Servidor de Clúster | 3 |
| Paquete de Registro | 4 |
| Solicitud de Sincronización de Instantánea | 5 |


#### Aplicación

Los contenidos de la aplicación están codificados en UTF-8 [JSON](https://www.json.org/).
Consulte la sección de Capa de Aplicación a continuación.


#### Configuración

Esto se utiliza para que el líder serialice una nueva configuración de clúster y la replique a sus pares.
Contiene cero o más configuraciones de Servidor de Clúster.


```dataspec
Índice de Registro:  entero de 8 bytes
  Último Índice de Registro:  entero de 8 bytes
  Datos de Servidor de Clúster para cada servidor:
    ID:                entero de 4 bytes
    Tamaño de los datos del punto final: En bytes, entero de 4 bytes
    Datos del punto final:     cadena ASCII de la forma "tcp://localhost:9001", longitud como especificada
```


#### Servidor de Clúster

La información de configuración para un servidor en un clúster.
Esto se incluye solo en un mensaje AddServerRequest o RemoveServerRequest.

Cuando se usa en un Mensaje AddServerRequest:

```dataspec
ID:                entero de 4 bytes
  Tamaño de los datos del punto final: En bytes, entero de 4 bytes
  Datos del punto final:     cadena ASCII de la forma "tcp://localhost:9001", longitud como especificada
```


Cuando se usa en un Mensaje RemoveServerRequest:

```dataspec
ID:                entero de 4 bytes
```


#### Paquete de Registro

Esto se incluye solo en un mensaje SyncLogRequest.

Lo siguiente se comprime (gzip) antes de la transmisión:

```dataspec
Tamaño de los datos del índice: En bytes, entero de 4 bytes
  Tamaño de los datos del registro:   En bytes, entero de 4 bytes
  Datos del índice:     8 bytes para cada índice, longitud como especificada
  Datos del registro:       longitud como especificada
```


#### Solicitud de Sincronización de Instantánea

Esto se incluye solo en un mensaje InstallSnapshotRequest.

```dataspec
Último Índice de Registro:  entero de 8 bytes
  Último Término de Registro:   entero de 8 bytes
  Tamaño de los datos de Configuración: En bytes, entero de 4 bytes
  Datos de Configuración:     longitud como especificada
  Desplazamiento:          El desplazamiento de los datos en la base de datos, en bytes, entero de 8 bytes
  Tamaño de los datos:        En bytes, entero de 4 bytes
  Datos:            longitud como especificada
  Terminado:         1 si está terminado, 0 si no está terminado (1 byte)
```


### Respuestas

Todas las respuestas son de 26 bytes, como se indica a continuación.
Todos los valores son big-endian sin signo.

```dataspec
Tipo de Mensaje:   1 byte
  Origen:         ID, entero de 4 bytes
  Destino:    Usualmente la ID de destino real (ver notas), entero de 4 bytes
  Término:           Término actual, entero de 8 bytes
  Siguiente Índice:     Inicializado en último índice de registro del líder + 1, entero de 8 bytes
  Aceptado:    1 si aceptado, 0 si no aceptado (ver notas), 1 byte
```


#### Notas

La ID de Destino es generalmente el destino real para este mensaje.
Sin embargo, para AppendEntriesResponse, AddServerResponse y RemoveServerResponse,
es la ID del líder actual.

En el RequestVoteResponse, Aceptado es 1 para un voto para el candidato (solicitante),
y 0 para no voto.


## Capa de Aplicación

Cada Servidor publica periódicamente datos de Aplicación al registro en un ClientRequest.
Los datos de la aplicación contienen el estado de cada Router del Servidor y el Destino
para el clúster Meta LS2.
Los servidores utilizan un algoritmo común para determinar el editor y el contenido
del Meta LS2.
El servidor con el mejor estado reciente en el registro es el editor del Meta LS2.
El editor del Meta LS2 NO es necesariamente el Líder de Raft.


### Contenidos de Datos de Aplicación

Los contenidos de la aplicación están codificados en UTF-8 [JSON](https://www.json.org/),
para simplicidad y extensibilidad.
La especificación completa está TDB.
El objetivo es proporcionar suficientes datos para escribir un algoritmo para determinar el "mejor"
router para publicar el Meta LS2, y para que el editor tenga suficiente información
para ponderar los Destinos en el Meta LS2.
Los datos contendrán estadísticas de los routers y de los Destinos.

Los datos pueden contener opcionalmente datos de detección remota sobre la salud de los
otros servidores, y la capacidad para obtener el Meta LS.
Estos datos no serían soportados en el primer lanzamiento.

Los datos pueden contener opcionalmente información de configuración publicada
por un cliente administrador.
Estos datos no serían soportados en el primer lanzamiento.

Si "nombre: valor" está listado, eso especifica la clave y valor del mapa JSON.
De lo contrario, la especificación está TDB.


Datos del clúster (nivel superior):

- cluster: Nombre del clúster
- date: Fecha de estos datos (long, ms desde la época)
- id: ID de Raft (entero)

Datos de configuración (config):

- Cualquier parámetro de configuración

Estado de publicación del MetaLS (meta):

- destination: el destino del metaLS, base64
- lastPublishedLS: si está presente, codificación base64 de los últimos metales publicados
- lastPublishedTime: en ms, o 0 si nunca
- publishConfig: Estado de configuración del publicador apagado/encendido/auto
- publishing: estado de publicador de metales booleano true/false

Datos del Router (router):

- lastPublishedRI: si está presente, codificación base64 del último informe de router publicado
- uptime: Tiempo de actividad en ms
- Retardo de trabajo
- Túneles de exploración
- Túneles de participación
- Ancho de banda configurado
- Ancho de banda actual

Destinos (destinos):
Lista

Datos del Destino:

- destination: el destino, base64
- uptime: Tiempo de actividad en ms
- Túneles configurados
- Túneles actuales
- Ancho de banda configurado
- Ancho de banda actual
- Conexiones configuradas
- Conexiones actuales
- Datos de lista negra

Datos de detección remota del router:

- Última versión de RI vista
- Tiempo de obtención de LS
- Datos de prueba de conexión
- Datos de perfil de los floodfills más cercanos
  para los períodos de tiempo ayer, hoy y mañana

Datos de detección remota del destino:

- Última versión de LS vista
- Tiempo de obtención de LS
- Datos de prueba de conexión
- Datos de perfil de los floodfills más cercanos
  para los períodos de tiempo ayer, hoy y mañana

Datos de detección del Meta LS:

- Última versión vista
- Tiempo de obtención
- Datos de perfil de los floodfills más cercanos
  para los períodos de tiempo ayer, hoy y mañana


## Interfaz de Administración

TDB, posiblemente una propuesta separada.
No requerida para el primer lanzamiento.

Requisitos de una interfaz de administración:

- Soporte para múltiples destinos maestras, es decir, múltiples clústeres virtuales (granjas)
- Proporcionar visión comprensiva del estado compartido del clúster - todas las estadísticas publicadas por los miembros, quién es el líder actual, etc.
- Capacidad para forzar la remoción de un participante o líder del clúster
- Capacidad para forzar la publicación del metaLS (si el nodo actual es el editor)
- Capacidad para excluir hashes del metaLS (si el nodo actual es el editor)
- Funcionalidad de importación/exportación de configuración para implementaciones en masa


## Interfaz del Router

TDB, posiblemente una propuesta separada.
i2pcontrol no es requerido para el primer lanzamiento y los cambios detallados se incluirán en una propuesta separada.

Requisitos para la API de la Granja de Ajo al router (Java en-JVM o i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // probablemente no en el MVP
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // o MetaLeaseSet firmado? ¿Quién firma?
- stopPublishingMetaLS(Hash masterHash)
- autenticación TDB?


## Justificación

Atomix es demasiado grande y no permitirá personalizaciones para que podamos enrutar
el protocolo sobre I2P. Además, su formato de cableado no está documentado y depende
de la serialización en Java.


## Notas


## Problemas

- No hay manera para que un cliente se entere y se conecte a un líder desconocido.
  Sería un cambio menor para que un Seguidor envíe la Configuración como una Entrada de Registro en la AppendEntriesResponse.


## Migración

No hay problemas de compatibilidad hacia atrás.


## Referencias

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
