---
title: "Perfilado y Selección de Peers"
description: "Cómo los routers I2P crean perfiles y seleccionan pares para construir túneles"
slug: "peer-selection"
aliases:
  - "/es/how_peerselection"
  - "/es/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Nota

Esta página describe la implementación Java de I2P para el perfilado y selección de pares tal como era en 2010. Aunque sigue siendo en gran medida precisa, algunos detalles pueden ya no ser correctos. Continuamos evolucionando las estrategias de prohibición, bloqueo y selección para abordar amenazas, ataques y condiciones de red más recientes. La red actual tiene múltiples implementaciones de router con diversas versiones. Otras implementaciones de I2P pueden tener estrategias de perfilado y selección completamente diferentes, o pueden no usar perfilado en absoluto.

## Visión general {#overview}

### Perfilado de Pares {#profiling}

**Peer profiling** es el proceso de recopilar datos basados en el rendimiento **observado** de otros routers o pares, y clasificar esos pares en grupos. El profiling **no** utiliza ningún dato de rendimiento declarado publicado por el propio par en la [base de datos de red](/docs/overview/network-database).

Los perfiles se utilizan para dos propósitos:

1. Seleccionar peers para retransmitir nuestro tráfico, lo cual se discute a continuación
2. Elegir peers del conjunto de routers floodfill para usar en el almacenamiento y consultas de la base de datos de red,
   lo cual se discute en la página de [base de datos de red](/docs/overview/network-database)

### Selección de Pares {#selection}

**La selección de peers** es el proceso de elegir qué routers de la red queremos que retransmitan nuestros mensajes (qué peers les pediremos que se unan a nuestros tunnels). Para lograr esto, llevamos un registro del rendimiento de cada peer (el "perfil" del peer) y usamos esos datos para estimar qué tan rápidos son, con qué frecuencia podrán aceptar nuestras solicitudes, y si parecen estar sobrecargados o de otra manera incapaces de realizar de manera confiable lo que acuerdan hacer.

A diferencia de otras redes anónimas, en I2P, el ancho de banda declarado no es confiable y se usa **únicamente** para evitar aquellos peers que anuncian un ancho de banda muy bajo e insuficiente para enrutar túneles. Toda selección de peers se realiza a través de perfilado. Esto previene ataques simples basados en peers que declaran alto ancho de banda para capturar grandes cantidades de túneles. También hace más difíciles los [ataques de temporización](/docs/overview/threat-model#timing).

La selección de pares se realiza con bastante frecuencia, ya que un router puede mantener un gran número de tunnels de cliente y exploratorios, y la vida útil de un tunnel es de solo 10 minutos.

### Información Adicional {#further-info}

Para más información consulta el artículo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) presentado en [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1). Consulta [más abajo](#notes) las notas sobre cambios menores desde que se publicó el artículo.

## Perfiles {#profiles}

Cada peer tiene un conjunto de puntos de datos recopilados sobre ellos, incluyendo estadísticas sobre cuánto tiempo tardan en responder a una consulta de la base de datos de red, con qué frecuencia fallan sus tunnels, y cuántos peers nuevos son capaces de presentarnos, así como puntos de datos simples como cuándo los escuchamos por última vez o cuándo ocurrió el último error de comunicación.

Los perfiles son bastante pequeños, unos pocos KB. Para controlar el uso de memoria, el tiempo de expiración del perfil se reduce a medida que aumenta el número de perfiles. Los perfiles se mantienen en memoria hasta el apagado del router, momento en que se escriben al disco. Al iniciar, los perfiles se leen para que el router no necesite reinicializar todos los perfiles, permitiendo así que un router se reintegre rápidamente a la red después del arranque.

## Resúmenes de Peers {#summaries}

Aunque los perfiles en sí mismos pueden considerarse un resumen del rendimiento de un peer, para permitir una selección efectiva de peers dividimos cada resumen en cuatro valores simples, que representan la velocidad del peer, su capacidad, qué tan bien integrado está en la red, y si está fallando.

### Velocidad {#speed}

El cálculo de velocidad simplemente revisa el perfil y estima cuántos datos podemos enviar o recibir en un solo tunnel a través del par en un minuto. Para esta estimación solo observa el rendimiento del minuto anterior.

### Capacidad {#capacity}

El cálculo de capacidad simplemente revisa el perfil y estima cuántos tunnels el peer estaría dispuesto a participar durante un período de tiempo determinado. Para esta estimación examina cuántas solicitudes de construcción de tunnel el peer ha aceptado, rechazado y descartado, y cuántos de los tunnels acordados fallaron posteriormente. Aunque el cálculo está ponderado por tiempo para que la actividad reciente cuente más que la actividad posterior, pueden incluirse estadísticas de hasta 48 horas de antigüedad.

Reconocer y evitar peers no confiables e inalcanzables es de importancia crítica. Desafortunadamente, como la construcción y prueba de túneles requiere la participación de varios peers, es difícil identificar positivamente la causa de una solicitud de construcción descartada o un fallo de prueba. El router asigna una probabilidad de fallo a cada uno de los peers, y usa esa probabilidad en el cálculo de capacidad. Los descartes y fallos de prueba tienen un peso mucho mayor que los rechazos.

## Organización de Peers {#organization}

Como se mencionó anteriormente, analizamos a fondo el perfil de cada peer para obtener algunos cálculos clave, y basándonos en estos, organizamos cada peer en tres grupos: rápido, alta capacidad y estándar.

Los agrupamientos no son mutuamente excluyentes, ni tampoco están desvinculados:

- Un peer se considera de "alta capacidad" si su cálculo de capacidad cumple o
  supera la mediana de todos los peers.
- Un peer se considera "rápido" si ya es de "alta capacidad" y su
  cálculo de velocidad cumple o supera la mediana de todos los peers.
- Un peer se considera "estándar" si no es de "alta capacidad"

### Límites del Tamaño de Grupo {#group-limits}

El tamaño de los grupos puede estar limitado.

- El grupo rápido está limitado a 30 peers.
  Si hubiera más, solo aquellos con la calificación de velocidad más alta se colocan en el grupo.
- El grupo de alta capacidad está limitado a 75 peers (incluyendo el grupo rápido).
  Si hubiera más, solo aquellos con la calificación de capacidad más alta se colocan en el grupo.
- El grupo estándar no tiene un límite fijo, pero es algo menor que el número de RouterInfos
  almacenados en la base de datos de red local.
  En un router activo en la red actual, puede haber alrededor de 1000 RouterInfos y 500 perfiles de peer
  (incluyendo aquellos en los grupos rápido y de alta capacidad).

## Recálculo y Estabilidad {#recalculation}

Los resúmenes se recalculan y los peers se reorganizan en grupos cada 45 segundos.

Los grupos tienden a ser bastante estables, es decir, no hay mucha "rotación" en las clasificaciones en cada recálculo. Los peers en los grupos de alta velocidad y alta capacidad reciben más túneles construidos a través de ellos, lo que aumenta sus puntuaciones de velocidad y capacidad, lo que refuerza su presencia en el grupo.

## Selección de Peers {#peer-selection}

El router selecciona peers de los grupos anteriores para construir tunnels a través de ellos.

### Selección de Pares para Túneles de Cliente {#client-tunnels}

Los túneles de cliente se utilizan para el tráfico de aplicaciones, como para proxies HTTP y servidores web.

Para reducir la susceptibilidad a [algunos ataques](http://blog.torproject.org/blog/one-cell-enough) y aumentar el rendimiento, los peers para construir tunnels de cliente se eligen aleatoriamente del grupo más pequeño, que es el grupo "rápido". No hay sesgo hacia seleccionar peers que fueron previamente participantes en un tunnel para el mismo cliente.

### Selección de Peers para Tunnels Exploratorios {#exploratory-tunnels}

Los túneles exploratorios se utilizan para propósitos administrativos del router, como el tráfico de la base de datos de red y las pruebas de túneles de cliente. Los túneles exploratorios también se usan para contactar routers previamente no conectados, razón por la cual se les llama "exploratorios". Estos túneles suelen ser de bajo ancho de banda.

Los peers para construir tunnels exploratorios generalmente se eligen aleatoriamente del grupo estándar. Si la tasa de éxito de estos intentos de construcción es baja comparada con la tasa de éxito de construcción de tunnels de cliente, el router seleccionará un promedio ponderado de peers aleatoriamente del grupo de alta capacidad en su lugar. Esto ayuda a mantener una tasa de éxito de construcción satisfactoria incluso cuando el rendimiento de la red es deficiente. No hay sesgo hacia la selección de peers que fueron previamente participantes en un tunnel exploratorio.

Como el grupo estándar incluye un subconjunto muy grande de todos los peers que conoce el router, los túneles exploratorios se construyen esencialmente a través de una selección aleatoria de todos los peers, hasta que la tasa de éxito de construcción se vuelve demasiado baja.

### Restricciones {#restrictions}

Para prevenir algunos ataques simples, y por rendimiento, existen las siguientes restricciones:

- Dos peers del mismo espacio IP /16 no pueden estar en el mismo túnel.
- Un peer puede participar en un máximo del 33% de todos los túneles creados por el router.
- Los peers con ancho de banda extremadamente bajo no se utilizan.
- Los peers para los cuales falló un intento de conexión reciente no se utilizan.

### Ordenación de Pares en Tunnels {#ordering}

Los peers están ordenados dentro de los tunnels para lidiar con el [ataque de predecesor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([actualización 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)). Más información está en la [página de tunnels](/docs/specs/tunnel-implementation#ordering).

## Trabajo Futuro {#future}

- Continuar analizando y ajustando los cálculos de velocidad y capacidad según sea necesario
- Implementar una estrategia de expulsión más agresiva si es necesario para controlar el uso de memoria a medida que la red crece
- Evaluar los límites de tamaño de grupo
- Usar datos GeoIP para incluir o excluir ciertos peers, si está configurado

## Notas {#notes}

Para aquellos que lean el artículo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), por favor tengan en cuenta los siguientes cambios menores en I2P desde la publicación del artículo:

- El cálculo de Integración aún no se utiliza
- En el documento, los "grupos" se llaman "niveles"
- El nivel "Failing" ya no se utiliza
- El nivel "Not Failing" ahora se llama "Standard"

## Referencias {#references}

- [Perfilado y Selección de Pares en la Red Anónima I2P](/pdf/I2P-PET-CON-2009.1.pdf)
- [Una Celda es Suficiente](http://blog.torproject.org/blog/one-cell-enough)
- [Guardias de Entrada de Tor](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Artículo de Murdoch 2007](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Optimización para Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Ataques de Enrutamiento de Pocos Recursos Contra Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
