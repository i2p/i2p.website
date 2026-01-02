---
title: "Multihoming Invisible"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Abrir"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Descripción general

Esta propuesta describe un diseño para un protocolo que permite a un cliente I2P, servicio o proceso balanceador externo gestionar múltiples routers que alojan de forma transparente un único [Destination](http://localhost:63465/docs/specs/common-structures/#destination).

La propuesta actualmente no especifica una implementación concreta. Podría implementarse como una extensión de [I2CP](/docs/specs/i2cp/), o como un nuevo protocolo.

## Motivación

Multihoming es donde se utilizan múltiples routers para alojar la misma Destination. La forma actual de hacer multihoming con I2P es ejecutar la misma Destination en cada router de forma independiente; el router que utilizan los clientes en cualquier momento particular es el último que publicó un LeaseSet.

Esto es un hack y presumiblemente no funcionará para sitios web grandes a escala. Digamos que tuviéramos 100 routers multihoming cada uno con 16 túneles. Eso son 1600 publicaciones de LeaseSet cada 10 minutos, o casi 3 por segundo. Los floodfills se verían abrumados y se activarían los limitadores. Y eso es antes de siquiera mencionar el tráfico de búsqueda.

La Propuesta 123 resuelve este problema con un meta-LeaseSet, que enumera los 100 hashes de LeaseSet reales. Una búsqueda se convierte en un proceso de dos etapas: primero buscar el meta-LeaseSet, y luego uno de los LeaseSets nombrados. Esta es una buena solución al problema del tráfico de búsqueda, pero por sí sola crea una filtración significativa de privacidad: Es posible determinar qué routers de multihoming están en línea monitoreando el meta-LeaseSet publicado, porque cada LeaseSet real corresponde a un solo router.

Necesitamos una forma para que un cliente o servicio I2P pueda distribuir un solo Destination a través de múltiples routers, de manera que sea indistinguible de usar un solo router (desde la perspectiva del propio LeaseSet).

## Diseño

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Imagina la siguiente configuración deseada:

- Una aplicación cliente con un Destination.
- Cuatro routers, cada uno gestionando tres túneles entrantes.
- Los doce túneles deberían publicarse en un único LeaseSet.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Definiciones

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Descripción general de alto nivel

- Cargar o generar un Destination.

- Abrir una sesión con cada router, vinculada al Destination.

- Periódicamente (aproximadamente cada diez minutos, pero más o menos según la
  vitalidad del tunnel):

- Obtener el nivel rápido de cada router.

- Utiliza el superconjunto de peers para construir túneles hacia/desde cada router.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Recopilar el conjunto de túneles de entrada activos de todos los routers activos, y crear un LeaseSet.

- Publicar el LeaseSet a través de uno o más de los routers.

### Cliente único

Para crear y administrar esta configuración, el cliente necesita la siguiente funcionalidad nueva más allá de lo que actualmente proporciona [I2CP](/docs/specs/i2cp/):

- Decirle a un router que construya túneles, sin crear un LeaseSet para ellos.
- Obtener una lista de los túneles actuales en el pool de entrada.

Además, la siguiente funcionalidad permitiría una flexibilidad significativa en cómo el cliente administra sus túneles:

- Obtener el contenido del nivel rápido de un router.
- Indicar a un router que construya un túnel de entrada o salida utilizando una lista dada de
  peers.

### Multi-cliente

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Proceso general del cliente

**Crear Sesión** - Crear una sesión para el Destination dado.

**Estado de Sesión** - Confirmación de que la sesión ha sido configurada, y el cliente ahora puede comenzar a construir túneles.

**Get Fast Tier** - Solicitar una lista de los peers que el router actualmente consideraría para construir túneles.

**Lista de Peers** - Una lista de peers conocidos por el router.

**Crear Túnel** - Solicita que el router construya un nuevo túnel a través de los peers especificados.

**Estado del Tunnel** - El resultado de una construcción particular de tunnel, una vez que está disponible.

**Obtener Pool de Túneles** - Solicitar una lista de los túneles actuales en el pool de entrada o salida para el Destination.

**Lista de Túneles** - Una lista de túneles para el pool solicitado.

**Publicar LeaseSet** - Solicitud de que el router publique el LeaseSet proporcionado a través de uno de los túneles de salida para el Destino. No se necesita estado de respuesta; el router debe continuar reintentando hasta estar satisfecho de que el LeaseSet ha sido publicado.

**Send Packet** - Un paquete saliente del cliente. Opcionalmente especifica un túnel de salida a través del cual el paquete debe (¿debería?) ser enviado.

**Send Status** - Informa al cliente del éxito o falla del envío de un paquete.

**Paquete Recibido** - Un paquete entrante para el cliente. Opcionalmente especifica el túnel de entrada a través del cual se recibió el paquete(?)

## Security implications

Desde la perspectiva de los routers, este diseño es funcionalmente equivalente al status quo. El router aún construye todos los túneles, mantiene sus propios perfiles de peers, y hace cumplir la separación entre las operaciones del router y del cliente. En la configuración por defecto es completamente idéntica, porque los túneles para ese router se construyen desde su propio nivel rápido.

Desde la perspectiva de la netDB, un solo LeaseSet creado mediante este protocolo es idéntico al status quo, porque aprovecha la funcionalidad preexistente. Sin embargo, para LeaseSets más grandes que se aproximen a 16 Leases, puede ser posible que un observador determine que el LeaseSet es multihomed:

- El tamaño máximo actual del nivel rápido es de 75 peers. El Inbound Gateway
  (IBGW, el nodo publicado en un Lease) se selecciona de una fracción del nivel
  (particionado aleatoriamente por pool de túnel mediante hash, no por recuento):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Eso significa que en promedio los IBGW serán de un conjunto de 20-30 peers.

- En una configuración single-homed, un LeaseSet completo de 16 túneles tendría 16 IBGWs seleccionados aleatoriamente de un conjunto de hasta (digamos) 20 peers.

- En una configuración multihomed de 4 routers usando la configuración predeterminada, un LeaseSet completo de 16 túneles tendría 16 IBGWs seleccionados aleatoriamente de un conjunto de como máximo 80 peers, aunque es probable que haya una fracción de peers comunes entre routers.

Por lo tanto, con la configuración predeterminada, puede ser posible a través del análisis estadístico determinar que un LeaseSet está siendo generado por este protocolo. También podría ser posible determinar cuántos routers hay, aunque el efecto de la rotación en los niveles rápidos reduciría la efectividad de este análisis.

Como el cliente tiene control total sobre qué peers selecciona, esta filtración de información podría reducirse o eliminarse seleccionando IBGWs de un conjunto reducido de peers.

## Compatibility

Este diseño es completamente compatible hacia atrás con la red, porque no hay cambios en el formato de LeaseSet. Todos los routers necesitarían estar al tanto del nuevo protocolo, pero esto no es una preocupación ya que todos estarían controlados por la misma entidad.

## Performance and scalability notes

El límite superior de 16 Leases por LeaseSet no se ve alterado por esta propuesta. Para Destinations que requieren más túneles que esto, hay dos posibles modificaciones de red:

- Incrementar el límite superior del tamaño de los LeaseSets. Esta sería la opción más simple de implementar (aunque aún requeriría soporte generalizado en la red antes de poder ser ampliamente utilizada), pero podría resultar en búsquedas más lentas debido a los tamaños de paquete más grandes. El tamaño máximo factible de LeaseSet está definido por el MTU de los transportes subyacentes, y por lo tanto es de alrededor de 16kB.

- Implementar la Propuesta 123 para LeaseSets por niveles. En combinación con esta propuesta,
  los Destinations para los sub-LeaseSets podrían distribuirse a través de múltiples
  routers, actuando efectivamente como múltiples direcciones IP para un servicio de clearnet.

## Acknowledgements

Gracias a psi por la discusión que llevó a esta propuesta.
