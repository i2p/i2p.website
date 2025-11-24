---
title: "Multihoming Invisible"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Open"
thread: "http://zzz.i2p/topics/2335"
---

## Visión general

Esta propuesta describe un diseño para un protocolo que permite que un cliente de I2P, servicio o proceso equilibrador externo gestione múltiples enrutadores que albergan de manera transparente un único [Destino](http://localhost:63465/en/docs/specs/common-structures/#destination).

La propuesta actualmente no especifica una implementación concreta. Podría implementarse como una extensión de [I2CP](/en/docs/specs/i2cp/), o como un nuevo protocolo.

## Motivación

El multihoming es cuando se utilizan múltiples enrutadores para alojar el mismo Destino. La forma actual de realizar multihoming con I2P es ejecutar el mismo Destino en cada enrutador de manera independiente; el enrutador que es utilizado por los clientes en cualquier momento es el último que publica un [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset).

Esto es un truco y probablemente no funcionará para grandes sitios web a gran escala. Supongamos que tuviéramos 100 enrutadores de multihoming cada uno con 16 túneles. Serían 1600 publicaciones de LeaseSet cada 10 minutos, o casi 3 por segundo. Los floodfills se verían abrumados y entrarían en acción los mecanismos de limitación. Y eso antes de mencionar siquiera el tráfico de búsqueda.

[Proposal 123](/en/proposals/123-new-netdb-entries/) resuelve este problema con un meta-LeaseSet, que enumera los 100 hashes de LeaseSet reales. Una búsqueda se convierte en un proceso de dos etapas: primero buscando el meta-LeaseSet, y luego uno de los LeaseSets nombrados. Esta es una buena solución para el problema de tráfico de búsqueda, pero por sí sola crea una fuga de privacidad significativa: Es posible determinar qué enrutadores de multihoming están en línea mediante la monitorización del meta-LeaseSet publicado, ya que cada LeaseSet real corresponde a un único enrutador.

Necesitamos una manera para que un cliente o servicio de I2P distribuya un único Destino a través de múltiples enrutadores, de una forma que sea indistinguible de usar un único enrutador (desde la perspectiva del propio LeaseSet).

## Diseño

### Definiciones

    Usuario
        La persona u organización que quiere hacer multihoming de sus Destinos. Aquí
        se considera un solo Destino sin pérdida de generalidad (WLOG).

    Cliente
        La aplicación o servicio que se ejecuta detrás del Destino. Puede ser una
        aplicación del lado del cliente, del lado del servidor, o peer-to-peer; nos
        referimos a ella como un cliente en el sentido de que se conecta a los
        enrutadores de I2P.

        El cliente consta de tres partes, que pueden estar todas en el mismo
        proceso o pueden estar distribuidas en procesos o máquinas (en una
        configuración multi-cliente):

        Balanceador
            La parte del cliente que gestiona la selección de pares y la
            construcción de túneles. Hay un solo balanceador en cualquier momento,
            y se comunica con todos los enrutadores de I2P. Puede haber balanceadores
            de respaldo.

        Frontend
            La parte del cliente que puede operar en paralelo. Cada frontend se
            comunica con un solo enrutador de I2P.

        Backend
            La parte del cliente que se comparte entre todos los frontends. No
            tiene comunicación directa con ningún enrutador de I2P.

    Enrutador
        Un enrutador de I2P ejecutado por el usuario que se encuentra en el límite
        entre la red I2P y la red del usuario (similar a un dispositivo de borde en redes
        corporativas). Construye túneles bajo el comando de un balanceador, y enruta
        paquetes para un cliente o frontend.

### Visión general de alto nivel

Imagine la siguiente configuración deseada:

- Una aplicación cliente con un Destino.
- Cuatro enrutadores, cada uno gestionando tres túneles entrantes.
- Los doce túneles deben publicarse en un único LeaseSet.

Cliente único

```
                -{ [Túnel 1]===\
                 |-{ [Túnel 2]====[Enrutador 1]-----
                 |-{ [Túnel 3]===/               \
                 |                                 \
                 |-{ [Túnel 4]===\                 \
  [Destino]      |-{ [Túnel 5]====[Enrutador 2]-----  \
    \            |-{ [Túnel 6]===/               \   \
     [LeaseSet]--|                               [Cliente]
                 |-{ [Túnel 7]===\               /   /
                 |-{ [Túnel 8]====[Enrutador 3]-----  /
                 |-{ [Túnel 9]===/                 /
                 |                                 /
                 |-{ [Túnel 10]==\               /
                 |-{ [Túnel 11]===[Enrutador 4]-----
                  -{ [Túnel 12]==/

Multi-cliente

```
                -{ [Túnel 1]===\
                 |-{ [Túnel 2]====[Enrutador 1]---------[Frontend 1]
                 |-{ [Túnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Túnel 4]===\            \                    \
  [Destino]      |-{ [Túnel 5]====[Enrutador 2]---\-----[Frontend 2]   \
    \            |-{ [Túnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balanceador]         [Backend]
                 |-{ [Túnel 7]===\          /   /                /   /
                 |-{ [Túnel 8]====[Enrutador 3]---/-----[Frontend 3]   /
                 |-{ [Túnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Túnel 10]==\          /                    /
                 |-{ [Túnel 11]===[Enrutador 4]---------[Frontend 4]
                  -{ [Túnel 12]==/

### Proceso general del cliente
- Cargar o generar un Destino.

- Abrir una sesión con cada enrutador, vinculada al Destino.

- Periódicamente (aproximadamente cada diez minutos, pero más o menos según la
  vitalidad del túnel):

  - Obtener el nivel rápido de cada enrutador.

  - Utilizar el superconjunto de pares para construir túneles hacia/desde cada
    enrutador.

    - Por defecto, los túneles hacia/desde un enrutador en particular utilizarán
      pares del nivel rápido de ese enrutador, pero esto no está impuesto por el
      protocolo.

  - Recopilar el conjunto de túneles entrantes activos de todos los enrutadores
    activos, y crear un LeaseSet.

  - Publicar el LeaseSet a través de uno o más de los enrutadores.

### Diferencias con I2CP
Para crear y gestionar esta configuración, el cliente necesita la siguiente
nueva funcionalidad más allá de lo que actualmente proporciona [I2CP](/en/docs/specs/i2cp/):

- Decirle a un enrutador que construya túneles, sin crear un LeaseSet para
  ellos.
- Obtener una lista de los túneles actuales en el pool entrante.

Además, la siguiente funcionalidad permitiría una flexibilidad significativa en
cómo el cliente gestiona sus túneles:

- Obtener el contenido del nivel rápido de un enrutador.
- Decirle a un enrutador que construya un túnel entrante o saliente utilizando
  una lista dada de pares.

### Esquema del protocolo

```
         Cliente                           Enrutador

                    --------------------->  Crear Sesión
   Estado de Sesión  <---------------------
                    --------------------->  Obtener Nivel Rápido
        Lista de Pares  <---------------------
                    --------------------->  Crear Túnel
    Estado de Túnel  <---------------------
                    --------------------->  Obtener Pool de Túneles
      Lista de Túneles  <---------------------
                    --------------------->  Publicar LeaseSet
                    --------------------->  Enviar Paquete
      Estado de Envío  <---------------------
  Paquete Recibido  <---------------------

### Mensajes
    Crear Sesión
        Crear una sesión para el Destino dado.

    Estado de Sesión
        Confirmación de que la sesión ha sido configurada, y el cliente ahora
        puede comenzar a construir túneles.

    Obtener Nivel Rápido
        Solicitar una lista de los pares que el enrutador actualmente consideraría
        para construir túneles.

    Lista de Pares
        Una lista de pares conocidos por el enrutador.

    Crear Túnel
        Solicitar que el enrutador construya un nuevo túnel a través de los pares
        especificados.

    Estado de Túnel
        El resultado de una construcción de túnel particular, una vez que está
        disponible.

    Obtener Pool de Túneles
        Solicitar una lista de los túneles actuales en el pool entrante o saliente
        para el Destino.

    Lista de Túneles
        Una lista de túneles para el pool solicitado.

    Publicar LeaseSet
        Solicitar que el enrutador publique el LeaseSet proporcionado a través de
        uno de los túneles salientes para el Destino. No se necesita un estado de
        respuesta; el enrutador debe continuar intentándolo hasta que se satisfaga
        que el LeaseSet ha sido publicado.

    Enviar Paquete
        Un paquete saliente del cliente. Opcionalmente especifica un túnel saliente
        a través del cual el paquete debe (¿debería?) enviarse.

    Estado de Envío
        Informa al cliente del éxito o fracaso del envío de un paquete.

    Paquete Recibido
        Un paquete entrante para el cliente. Opcionalmente especifica el túnel
        entrante a través del cual se recibió el paquete(?)

## Implicaciones de seguridad

Desde la perspectiva de los enrutadores, este diseño es funcionalmente equivalente
al statu quo. El enrutador todavía construye todos los túneles, mantiene sus propios
perfiles de pares y ejecuta la separación entre las operaciones del enrutador y del
cliente. En la configuración predeterminada es completamente idéntica, porque los
túneles para ese enrutador se construyen desde su propio nivel rápido.

Desde la perspectiva del netDB, un único LeaseSet creado a través de este protocolo es
idéntico al statu quo, porque aprovecha la funcionalidad preexistente. Sin embargo, para
LeaseSets más grandes que se acerquen a 16 Arrendamientos, puede ser posible que un
observador determine que el LeaseSet es multihomed:

- El tamaño máximo actual del nivel rápido es de 75 pares. La Puerta de Enlace Entrante
  (IBGW, el nodo publicado en un Lease) se selecciona de una fracción del nivel
  (particionado aleatoriamente por conjunto de túneles por hash, no por número):

      1 salto
          Todo el nivel rápido

      2 saltos
          La mitad del nivel rápido
          (el predeterminado hasta mediados de 2014)

      3+ saltos
          Un cuarto del nivel rápido
          (3 siendo el predeterminado actual)

  Eso significa que, en promedio, los IBGWs serán de un conjunto de 20-30 pares.

- En una configuración de un solo domicilio, un LeaseSet completo de 16 túneles
  tendría 16 IBGWs seleccionados aleatoriamente de un conjunto de hasta (digamos)
  20 pares.

- En una configuración de 4 enrutadores multihomed utilizando la configuración
  predeterminada, un LeaseSet completo de 16 túneles tendría 16 IBGWs seleccionados
  aleatoriamente de un conjunto de como máximo 80 pares, aunque es probable que
  haya una fracción de pares comunes entre los enrutadores.

Por lo tanto, con la configuración predeterminada, puede ser posible a través del
análisis estadístico determinar que un LeaseSet está siendo generado por este
protocolo. También podría ser posible averiguar cuántos enrutadores hay, aunque el
efecto de la rotación sobre los niveles rápidos reduciría la efectividad de este
análisis.

Dado que el cliente tiene control total sobre qué pares selecciona, esta fuga de
información podría reducirse o eliminarse seleccionando los IBGWs de un conjunto
reducido de pares.

## Compatibilidad

Este diseño es completamente compatible con versiones anteriores de la red, porque
no hay cambios en el formato del [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset). Todos los enrutadores necesitarían ser
conscientes del nuevo protocolo, pero esto no es una preocupación ya que todos serían
controlados por la misma entidad.

## Notas de rendimiento y escalabilidad

El límite superior de 16 [Arrendamiento](http://localhost:63465/en/docs/specs/common-structures/#lease) por LeaseSet no se ve alterado por esta
propuesta. Para los Destinos que requieran más túneles que esto, existen dos
posibles modificaciones de red:

- Aumentar el límite superior en el tamaño de LeaseSets. Esto sería lo más simple
  de implementar (aunque todavía requeriría un soporte de red generalizado antes de
  que pudiera ser ampliamente utilizado), pero podría resultar en búsquedas más
  lentas debido al mayor tamaño de los paquetes. El tamaño máximo factible de un
  LeaseSet está definido por la MTU de los transportes subyacentes, y es por lo
  tanto alrededor de 16kB.

- Implementar [Proposal 123](/en/proposals/123-new-netdb-entries/) para LeaseSets escalonados. En combinación con esta
  propuesta, los Destinos para los sub-LeaseSets podrían distribuirse a través de
  múltiples enrutadores, actuando efectivamente como múltiples direcciones IP para
  un servicio en la red pública.

## Agradecimientos

Gracias a psi por la discusión que llevó a esta propuesta.
