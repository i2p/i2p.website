---
title: "Modelo de Amenazas de I2P"
description: "Análisis de ataques considerados en el diseño de I2P y las mitigaciones implementadas"
slug: "threat-model"
aliases:
  - "/es/how_threatmodel"
  - "/es/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## ¿Qué Queremos Decir con "Anónimo"?

Tu nivel de anonimato se puede describir como "qué tan difícil es para alguien descubrir información que no quieres que sepan" — quién eres, dónde te encuentras, con quién te comunicas, o incluso cuándo te comunicas. El anonimato "perfecto" no es un concepto útil aquí — el software no te hará indistinguible de las personas que no usan computadoras o que no están en Internet. En su lugar, estamos trabajando para proporcionar suficiente anonimato para satisfacer las necesidades reales de quienquiera que podamos — desde aquellos que simplemente navegan por sitios web, hasta aquellos que intercambian datos, hasta aquellos que temen ser descubiertos por organizaciones o estados poderosos.

La pregunta de si I2P proporciona suficiente anonimato para tus necesidades particulares es difícil de responder, pero esta página esperamos que te ayude a responder esa pregunta explorando cómo opera I2P bajo varios ataques para que puedas decidir si satisface tus necesidades.

Damos la bienvenida a más investigación y análisis sobre la resistencia de I2P a las amenazas descritas a continuación. Se necesita más revisión de la literatura existente (gran parte de ella enfocada en Tor) y trabajo original centrado en I2P.

---

## Resumen de Topología de Red

I2P se basa en las ideas de muchos [otros](/docs/overview/comparison/) sistemas, pero se deben tener en cuenta algunos puntos clave al revisar literatura relacionada:

- **I2P es una mixnet de ruta libre gratuita** — el creador del mensaje define explícitamente la ruta por la que se enviarán los mensajes (el tunnel de salida), y el destinatario del mensaje define explícitamente la ruta por la que se recibirán los mensajes (el tunnel de entrada).
- **I2P no tiene puntos de entrada y salida oficiales** — todos los pares participan completamente en la mezcla, y no hay proxies de entrada o salida a nivel de red (sin embargo, a nivel de aplicación, existen algunos proxies).
- **I2P está completamente distribuido** — no hay controles centrales ni autoridades. Se podrían modificar algunos routers para operar cascadas de mezcla (construyendo tunnels y distribuyendo las claves necesarias para controlar el reenvío en el punto final del tunnel) o perfiles basados en directorios y selección, todo sin romper la compatibilidad con el resto de la red, pero hacerlo por supuesto no es necesario (e incluso puede perjudicar el anonimato).

Hemos documentado planes para implementar retrasos no triviales y estrategias de procesamiento por lotes cuya existencia solo es conocida por el hop particular o gateway del tunnel que recibe el mensaje, permitiendo que una mixnet de latencia mayormente baja proporcione tráfico de cobertura para comunicación de mayor latencia (por ejemplo, correo electrónico). Sin embargo, somos conscientes de que se requieren retrasos significativos para proporcionar protección significativa, y que la implementación de tales retrasos será un desafío importante. No está claro en este momento si realmente implementaremos estas características de retraso.

En teoría, los routers a lo largo de la ruta del mensaje pueden inyectar un número arbitrario de saltos antes de reenviar el mensaje al siguiente par, aunque la implementación actual no lo hace.

---

## El Modelo de Amenazas

El diseño de I2P comenzó en 2003, poco después del advenimiento de [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/), y [Tor](https://www.torproject.org/). Nuestro diseño se beneficia sustancialmente de la investigación publicada en esa época. I2P utiliza varias técnicas de onion routing, por lo que continuamos beneficiándonos del significativo interés académico en Tor.

Tomando de los ataques y análisis presentados en la [literatura de anonimato](http://freehaven.net/anonbib/topic.html) (principalmente [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)), lo siguiente describe brevemente una amplia variedad de ataques así como muchas de las defensas de I2P. Actualizamos esta lista para incluir nuevos ataques a medida que son identificados.

Se incluyen algunos ataques que pueden ser únicos de I2P. No tenemos buenas respuestas para todos estos ataques, sin embargo continuamos investigando y mejorando nuestras defensas.

Además, muchos de estos ataques son significativamente más fáciles de lo que deberían ser, debido al tamaño modesto de la red actual. Aunque somos conscientes de algunas limitaciones que necesitan ser abordadas, I2P está diseñado para soportar cientos de miles, o millones, de participantes. A medida que continuemos difundiendo la palabra y haciendo crecer la red, estos ataques se volverán mucho más difíciles.

Las páginas de [comparaciones de red](/docs/overview/comparison/) y [terminología "garlic"](/docs/overview/garlic-routing/) también pueden ser útiles para revisar.

### Ataques de Fuerza Bruta

Un ataque de fuerza bruta puede ser llevado a cabo por un adversario pasivo o activo global, observando todos los mensajes que pasan entre todos los nodos e intentando correlacionar qué mensaje sigue qué ruta. Montar este ataque contra I2P debería ser no trivial, ya que todos los peers en la red están enviando mensajes frecuentemente (tanto mensajes de extremo a extremo como mensajes de mantenimiento de red), además un mensaje de extremo a extremo cambia de tamaño y datos a lo largo de su ruta. Adicionalmente, el adversario externo no tiene acceso a los mensajes tampoco, ya que la comunicación entre routers está tanto cifrada como transmitida en streaming (haciendo que dos mensajes de 1024 bytes sean indistinguibles de un mensaje de 2048 bytes).

Sin embargo, un atacante poderoso puede usar fuerza bruta para detectar tendencias — si pueden enviar 5GB a un destino I2P y monitorear la conexión de red de todos, pueden eliminar a todos los peers que no recibieron 5GB de datos. Existen técnicas para derrotar este ataque, pero pueden ser prohibitivamente costosas (ver: las imitaciones de [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html) o tráfico de velocidad constante). La mayoría de los usuarios no se preocupan por este ataque, ya que el costo de ejecutarlo es extremo (y a menudo requiere actividad ilegal). Sin embargo, el ataque sigue siendo posible, por ejemplo por un observador en un ISP grande o un punto de intercambio de Internet. Aquellos que quieran defenderse contra él querrán tomar las contramedidas apropiadas, como establecer límites bajos de ancho de banda, y usar leasesets no publicados o cifrados para los sitios I2P. Otras contramedidas, como retrasos no triviales y rutas restringidas, no están implementadas actualmente.

Como defensa parcial contra un solo router o grupo de routers que intenten enrutar todo el tráfico de la red, los routers contienen límites sobre cuántos túneles pueden ser enrutados a través de un solo peer. A medida que la red crece, estos límites están sujetos a ajustes adicionales. Otros mecanismos para la calificación, selección y evasión de peers se discuten en la página de selección de peers.

### Ataques de Temporización

Los mensajes de I2P son unidireccionales y no implican necesariamente que se enviará una respuesta. Sin embargo, las aplicaciones sobre I2P muy probablemente tendrán patrones reconocibles dentro de la frecuencia de sus mensajes — por ejemplo, una solicitud HTTP será un mensaje pequeño con una gran secuencia de mensajes de respuesta que contengan la respuesta HTTP. Usando estos datos así como una vista amplia de la topología de red, un atacante podría ser capaz de descalificar algunos enlaces por ser demasiado lentos para haber pasado el mensaje.

Este tipo de ataque es poderoso, pero su aplicabilidad a I2P no es obvia, ya que la variación en los retrasos de mensajes debido a colas, procesamiento de mensajes y limitación de velocidad a menudo igualarán o superarán el tiempo de pasar un mensaje a lo largo de un solo enlace — incluso cuando el atacante sabe que se enviará una respuesta tan pronto como se reciba el mensaje. Sin embargo, hay algunos escenarios que expondrán respuestas bastante automáticas — la biblioteca de streaming lo hace (con el SYN+ACK) al igual que el modo de mensaje de entrega garantizada (con el DataMessage+DeliveryStatusMessage).

Sin limpieza de protocolos o mayor latencia, los adversarios activos globales pueden obtener información sustancial. Por tanto, las personas preocupadas por estos ataques podrían aumentar la latencia (usando retrasos no triviales o estrategias de agrupación), incluir limpieza de protocolos, u otras técnicas avanzadas de enrutamiento de túneles, pero estas no están implementadas en I2P.

Referencias: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Ataques de Intersección

Los ataques de intersección contra sistemas de baja latencia son extremadamente poderosos: hacer contacto periódico con el objetivo y llevar registro de qué pares están en la red. Con el tiempo, a medida que ocurre la rotación de nodos, el atacante obtendrá información significativa sobre el objetivo simplemente intersectando los conjuntos de pares que están en línea cuando un mensaje pasa exitosamente. El costo de este ataque es significativo a medida que la red crece, pero puede ser factible en algunos escenarios.

En resumen, si un atacante está en ambos extremos de tu tunnel al mismo tiempo, puede tener éxito. I2P no tiene una defensa completa contra esto para comunicación de baja latencia. Esta es una debilidad inherente del enrutamiento cebolla de baja latencia. Tor proporciona una [advertencia similar](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting).

Defensas parciales implementadas en I2P:

- [Ordenamiento estricto](/docs/specs/tunnel-implementation/#ordering) de peers
- Perfilado y selección de peers de un grupo pequeño que cambia lentamente
- Límites en el número de tunnels enrutados a través de un solo peer
- Prevención de que peers del mismo rango IP /16 sean miembros de un solo tunnel
- Para sitios I2P u otros servicios alojados, admitimos alojamiento simultáneo en múltiples routers, o multihoming

Incluso en conjunto, estas defensas no son una solución completa. Además, hemos tomado algunas decisiones de diseño que pueden aumentar significativamente nuestra vulnerabilidad:

- No utilizamos "nodos guardianes" de ancho de banda bajo
- Utilizamos grupos de tunnels compuestos por varios tunnels, y el tráfico puede cambiar de tunnel a tunnel.
- Los tunnels no son duraderos; se construyen nuevos tunnels cada 10 minutos.
- Las longitudes de tunnel son configurables. Aunque se recomiendan tunnels de 3 saltos para protección completa, varias aplicaciones y servicios utilizan tunnels de 2 saltos por defecto.

En el futuro, podría ser posible para peers que puedan permitirse retrasos significativos (según estrategias de retrasos no triviales y agrupamiento por lotes). Además, esto solo es relevante para destinos que otras personas conocen — un grupo privado cuyo destino solo es conocido por peers de confianza no tiene que preocuparse, ya que un adversario no puede hacer "ping" a ellos para montar el ataque.

Referencia: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Ataques de Denegación de Servicio

Hay toda una serie de ataques de denegación de servicio disponibles contra I2P, cada uno con diferentes costos y consecuencias:

**Ataque de usuario codicioso:** Esto es simplemente gente tratando de consumir significativamente más recursos de los que están dispuestos a contribuir. La defensa contra esto es:

- Establecer valores predeterminados para que la mayoría de usuarios proporcionen recursos a la red. En I2P, los usuarios enrutan tráfico por defecto. En marcado contraste con [otras redes](/docs/overview/comparison/), más del 95% de los usuarios de I2P retransmiten tráfico para otros.
- Proporcionar opciones de configuración fáciles para que los usuarios puedan aumentar su contribución (porcentaje de compartición) a la red. Mostrar métricas fáciles de entender como "ratio de compartición" para que los usuarios puedan ver lo que están contribuyendo.
- Mantener una comunidad sólida con blogs, foros, IRC y otros medios de comunicación.

**Ataque de inanición:** Un usuario hostil puede intentar dañar la red creando un número significativo de peers en la red que no están identificados como estando bajo el control de la misma entidad (como con Sybil). Estos nodos entonces deciden no proporcionar ningún recurso a la red, causando que los peers existentes busquen a través de una base de datos de red más grande o soliciten más túneles de los que deberían ser necesarios. Alternativamente, los nodos pueden proporcionar servicio intermitente eliminando periódicamente tráfico seleccionado, o rechazando conexiones a ciertos peers. Este comportamiento puede ser indistinguible del de un nodo con mucha carga o que está fallando. I2P aborda estos problemas manteniendo perfiles de los peers, intentando identificar aquellos con bajo rendimiento y simplemente ignorándolos, o usándolos raramente. Hemos mejorado significativamente la capacidad de reconocer y evitar peers problemáticos; sin embargo, aún se requieren esfuerzos significativos en esta área.

**Ataque de inundación:** Un usuario hostil puede intentar inundar la red, un peer, un destino o un tunnel. La inundación de red y peer es posible, e I2P no hace nada para prevenir la inundación estándar de la capa IP. La inundación de un destino con mensajes enviando una gran cantidad a las diversas puertas de entrada de tunnel entrantes del objetivo es posible, pero el destino lo sabrá tanto por el contenido del mensaje como porque las pruebas del tunnel fallarán. Lo mismo ocurre para inundar solo un tunnel. I2P no tiene defensas para un ataque de inundación de red. Para un ataque de inundación de destino y tunnel, el objetivo identifica cuáles tunnels no responden y construye otros nuevos. También se podría escribir código nuevo para agregar aún más tunnels si el cliente desea manejar la carga mayor. Si, por otro lado, la carga es más de lo que el cliente puede manejar, pueden instruir a los tunnels para que regulen el número de mensajes o bytes que deben transmitir (una vez que se implemente la operación avanzada de tunnel).

**Ataque de carga de CPU:** Actualmente existen algunos métodos para que las personas soliciten remotamente que un peer realice alguna operación criptográficamente costosa, y un atacante hostil podría usar estos para inundar ese peer con un gran número de ellas en un intento de sobrecargar la CPU. Tanto el uso de buenas prácticas de ingeniería como el requerir potencialmente certificados no triviales (por ejemplo, HashCash) adjuntos a estas solicitudes costosas deberían mitigar el problema, aunque puede haber espacio para que un atacante explote varios errores en la implementación.

**Ataque DOS de floodfill:** Un usuario hostil puede intentar dañar la red convirtiéndose en un router floodfill. Las defensas actuales contra routers floodfill poco confiables, intermitentes o maliciosos son deficientes. Un router floodfill puede proporcionar respuestas incorrectas o ninguna respuesta a las consultas, y también puede interferir con la comunicación entre floodfill. Se han implementado algunas defensas y perfiles de pares, sin embargo queda mucho por hacer. Para más información consulte la [página de base de datos de red](/docs/specs/common-structures/).

### Ataques de Etiquetado

Los ataques de etiquetado — modificar un mensaje para que pueda ser identificado posteriormente a lo largo de la ruta — son por sí mismos imposibles en I2P, ya que los mensajes que pasan por los tunnels están firmados. Sin embargo, si un atacante es el gateway del tunnel de entrada así como un participante más adelante en ese tunnel, con colusión pueden identificar el hecho de que están en el mismo tunnel (y antes de agregar identificadores únicos de salto y otras actualizaciones, los pares que coluden dentro del mismo tunnel pueden reconocer ese hecho sin ningún esfuerzo). Un atacante en un tunnel de salida y cualquier parte de un tunnel de entrada no pueden coludir, ya que el cifrado del tunnel rellena y modifica los datos por separado para los tunnels de entrada y salida. Los atacantes externos no pueden hacer nada, ya que los enlaces están cifrados y los mensajes firmados.

### Ataques de Particionamiento

Los ataques de partición — encontrar formas de segregar (técnica o analíticamente) los peers en una red — son importantes de tener en cuenta cuando se trata con un adversario poderoso, ya que el tamaño de la red juega un papel clave en determinar tu anonimato. La partición técnica mediante el corte de enlaces entre peers para crear redes fragmentadas es abordada por la base de datos de red integrada de I2P, que mantiene estadísticas sobre varios peers para permitir que cualquier conexión existente a otras secciones fragmentadas sea explotada para sanar la red. Sin embargo, si el atacante desconecta todos los enlaces a peers no controlados, esencialmente aislando el objetivo, ninguna cantidad de sanación de la base de datos de red lo solucionará. En ese punto, lo único que el router puede esperar hacer es notar que un número significativo de peers previamente confiables se han vuelto no disponibles y alertar al cliente que está temporalmente desconectado (este código de detección no está implementado en este momento).

Particionar la red analíticamente buscando diferencias en cómo se comportan los routers y destinos y agrupándolos en consecuencia es también un ataque muy poderoso. Por ejemplo, un atacante que [recolecte](#harvesting-attacks) la base de datos de la red sabrá cuándo un destino particular tiene 5 túneles entrantes en su LeaseSet mientras otros tienen solo 2 o 3, permitiendo al adversario potencialmente particionar clientes por el número de túneles seleccionados. Otra partición es posible cuando se trata de retrasos no triviales y estrategias de agrupamiento, ya que las puertas de enlace de túnel y los saltos particulares con retrasos distintos de cero probablemente se destaquen. Sin embargo, estos datos solo están expuestos a esos saltos específicos, por lo que para particionar efectivamente en ese aspecto, el atacante necesitaría controlar una porción significativa de la red (y aún así eso sería solo una partición probabilística, ya que no sabrían qué otros túneles o mensajes tienen esos retrasos).

También se discute en la [página de base de datos de red](/docs/specs/common-structures/) (ataque de arranque inicial).

### Ataques de Predecesor

El ataque predecessor consiste en recopilar estadísticas de forma pasiva en un intento de ver qué peers están 'cerca' del destino participando en sus tunnels y llevando un registro del salto anterior o siguiente (para tunnels de salida o entrada, respectivamente). Con el tiempo, utilizando una muestra perfectamente aleatoria de peers y un ordenamiento aleatorio, un atacante podría ver qué peer aparece como 'más cercano' estadísticamente más que el resto, y ese peer sería a su vez donde se encuentra ubicado el objetivo.

I2P evita esto de cuatro maneras: primero, los peers seleccionados para participar en tunnels no se muestrean aleatoriamente a través de la red — se derivan del algoritmo de selección de peers que los divide en niveles. Segundo, con [ordenamiento estricto](/docs/specs/tunnel-implementation/#ordering) de peers en un tunnel, el hecho de que un peer aparezca con más frecuencia no significa que sea la fuente. Tercero, con longitud de tunnel permutada (no habilitada por defecto) incluso los tunnels de 0 saltos pueden proporcionar negación plausible ya que la variación ocasional del gateway se verá como tunnels normales. Cuarto, con rutas restringidas (no implementadas), solo el peer con una conexión restringida al objetivo contactará alguna vez al objetivo, mientras que los atacantes simplemente se encontrarán con ese gateway.

El método actual de construcción de tunnel fue específicamente diseñado para combatir el ataque predecesor. Consulta también [el ataque de intersección](#intersection-attacks).

Referencias: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), que es una actualización del [artículo de ataque predecesor de 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf).

### Ataques de Recolección

"Harvesting" significa compilar una lista de usuarios que ejecutan I2P. Puede utilizarse para ataques legales y para ayudar a otros ataques simplemente ejecutando un peer, viendo a quién se conecta, y recopilando cualquier referencia a otros peers que pueda encontrar.

I2P en sí mismo no está diseñado con defensas efectivas contra este ataque, ya que existe la base de datos de red distribuida que contiene precisamente esta información. Los siguientes factores hacen que el ataque sea algo más difícil en la práctica:

- El crecimiento de la red hará más difícil obtener una proporción determinada de la red
- Los routers floodfill implementan límites de consultas como protección contra DOS
- El "modo oculto", que impide que un router publique su información en la netDb, (pero también le impide retransmitir datos) no se usa ampliamente ahora pero podría serlo.

En implementaciones futuras, las rutas restringidas básicas e integrales reducirían el poder de este ataque, ya que los peers "ocultos" no publican sus direcciones de contacto en la base de datos de red — solo los túneles a través de los cuales se puede llegar a ellos (así como sus claves públicas, etc).

En el futuro, los routers podrían usar GeoIP para identificar si se encuentran en un país particular donde la identificación como un nodo I2P sería riesgosa. En ese caso, el router podría habilitar automáticamente el modo oculto, o implementar otros métodos de enrutamiento restringidos.

### Identificación Mediante Análisis de Tráfico

Al inspeccionar el tráfico que entra y sale de un router, un ISP malicioso o un firewall a nivel estatal podría identificar que una computadora está ejecutando I2P. Como se discutió [arriba](#harvesting-attacks), I2P no está específicamente diseñado para ocultar que una computadora está ejecutando I2P. Sin embargo, varias decisiones de diseño tomadas en el diseño de la capa de transporte y los protocolos hacen que sea algo difícil identificar el tráfico I2P:

- Selección aleatoria de puertos
- Cifrado punto a punto de todo el tráfico
- Intercambio de claves DH sin bytes de protocolo u otros campos constantes sin cifrar
- Uso simultáneo de transportes TCP y UDP. UDP puede ser mucho más difícil de rastrear para algunos equipos de Inspección Profunda de Paquetes (DPI).

En el futuro cercano, planeamos abordar directamente los problemas de análisis de tráfico mediante una mayor ofuscación de los protocolos de transporte de I2P, posiblemente incluyendo:

- Relleno en la capa de transporte a longitudes aleatorias, especialmente durante el handshake de conexión
- Estudio de las firmas de distribución de tamaño de paquetes, y relleno adicional según sea necesario
- Desarrollo de métodos de transporte adicionales que imiten SSL u otros protocolos comunes
- Revisión de las estrategias de relleno en capas superiores para ver cómo afectan los tamaños de paquete en la capa de transporte
- Revisión de métodos implementados por varios firewalls a nivel estatal para bloquear Tor
- Trabajar directamente con expertos en DPI y ofuscación

Referencia: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Ataques Sybil

Sybil describe una categoría de ataques donde el adversario crea números arbitrariamente grandes de nodos que colaboran entre sí y usa el aumento en números para ayudar a montar otros ataques. Por ejemplo, si un atacante está en una red donde los pares se seleccionan aleatoriamente y quiere una probabilidad del 80% de ser uno de esos pares, simplemente crea cinco veces el número de nodos que hay en la red y lanza los dados. Cuando la identidad es gratuita, Sybil puede ser una técnica muy potente para un adversario poderoso. La técnica principal para abordar esto es simplemente hacer que la identidad sea 'no gratuita' — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (entre otros) usa el hecho de que las direcciones IP son limitadas, mientras que IIP usó [HashCash](http://www.hashcash.org/) para 'cobrar' por crear una nueva identidad. Actualmente no hemos implementado ninguna técnica particular para abordar Sybil, pero sí incluimos certificados de marcador de posición en las estructuras de datos del router y del destino que pueden contener un certificado HashCash de valor apropiado cuando sea necesario (o algún otro certificado que pruebe escasez).

Requerir certificados HashCash en varios lugares tiene dos problemas principales:

- Mantener la compatibilidad hacia atrás
- El problema clásico de HashCash — seleccionar valores de HashCash que sean pruebas de trabajo significativas en máquinas de gama alta, mientras siguen siendo factibles en máquinas de gama baja como dispositivos móviles.

Varias limitaciones en el número de routers en un rango de IP determinado restringen la vulnerabilidad a atacantes que no tienen la capacidad de colocar máquinas en varios bloques de IP. Sin embargo, esta no es una defensa significativa contra un adversario poderoso.

Consulta la [página de base de datos de red](/docs/specs/common-structures/) para más discusión sobre Sybil.

### Ataques de Agotamiento de Compañeros

(Referencia: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Sección 5.2)

Al negarse a aceptar o reenviar solicitudes de construcción de tunnel, excepto hacia un par coludido, un router podría asegurar que un tunnel se forme completamente de su conjunto de routers coludidos. Las posibilidades de éxito se incrementan si hay un gran número de routers coludidos, es decir, un [ataque Sybil](#sybil-attacks). Esto se mitiga en cierta medida por nuestros métodos de perfilado de pares utilizados para monitorear el rendimiento de los pares. Sin embargo, este es un ataque poderoso cuando el número de routers se acerca a *f* = 0.2, o 20% de nodos maliciosos, como se especifica en el documento. Los routers maliciosos también podrían mantener conexiones al router objetivo y proporcionar excelente ancho de banda de reenvío para el tráfico sobre esas conexiones, en un intento de manipular los perfiles gestionados por el objetivo y parecer atractivos. Puede ser necesaria investigación adicional y defensas.

### Ataques Criptográficos

Utilizamos criptografía fuerte con claves largas, y asumimos la seguridad de las primitivas criptográficas estándar de la industria utilizadas en I2P. Las características de seguridad incluyen la detección inmediata de mensajes alterados a lo largo de la ruta, la imposibilidad de descifrar mensajes que no estén dirigidos a ti, y defensa contra ataques de intermediario (man-in-the-middle). Los tamaños de clave elegidos en 2003 fueron bastante conservadores en su momento, y siguen siendo más largos que los utilizados en [otras redes de anonimato](https://torproject.org/). No creemos que las longitudes actuales de las claves sean nuestra mayor debilidad, especialmente para adversarios tradicionales que no sean de nivel estatal; los errores y el pequeño tamaño de la red son mucho más preocupantes. Por supuesto, todos los algoritmos criptográficos eventualmente se vuelven obsoletos debido a la llegada de procesadores más rápidos, la investigación criptográfica y los avances en métodos como las tablas arcoíris, clusters de hardware de videojuegos, etc. Desafortunadamente, I2P no fue diseñado con mecanismos sencillos para alargar las claves o cambiar los valores de secreto compartido mientras se mantiene la compatibilidad hacia atrás.

La actualización de las diversas estructuras de datos y protocolos para soportar claves más largas tendrá que abordarse eventualmente, y esto será una empresa importante, tal como lo será para [otros](https://torproject.org/). Con suerte, a través de una planificación cuidadosa, podemos minimizar la disrupción e implementar mecanismos para facilitar las transiciones futuras.

En el futuro, varios protocolos I2P y estructuras de datos soportarán el relleno seguro de mensajes a tamaños arbitrarios, por lo que los mensajes podrían hacerse de tamaño constante o los garlic messages podrían modificarse aleatoriamente para que algunos cloves parezcan contener más subcloves de los que realmente contienen. Sin embargo, en este momento, los mensajes garlic, tunnel y de extremo a extremo incluyen relleno aleatorio simple.

### Ataques de Anonimato contra Floodfill

Además de los ataques DOS contra floodfill descritos [arriba](#denial-of-service-attacks), los routers floodfill están en una posición única para aprender sobre los participantes de la red, debido a su papel en la netDb y la alta frecuencia de comunicación con esos participantes. Esto se mitiga en parte porque los routers floodfill solo gestionan una porción del keyspace total, y el keyspace rota diariamente, como se explica en la [página de base de datos de red](/docs/specs/common-structures/). Los mecanismos específicos por los cuales los routers se comunican con floodfills han sido cuidadosamente diseñados. Sin embargo, estas amenazas deberían estudiarse más a fondo. Las amenazas potenciales específicas y las defensas correspondientes son un tema para investigación futura.

### Otros Ataques a la Base de Datos de Red

Un usuario hostil puede intentar dañar la red creando uno o más routers floodfill y diseñándolos para ofrecer respuestas incorrectas, lentas o nulas. Varios escenarios se discuten en la [página de base de datos de red](/docs/specs/common-structures/).

### Ataques a Recursos Centrales

Hay algunos recursos centralizados o limitados (algunos dentro de I2P, otros no) que podrían ser atacados o utilizados como vector para ataques. La ausencia de jrandom a partir de noviembre de 2007, seguida por la pérdida del servicio de hosting i2p.net en enero de 2008, resaltó numerosos recursos centralizados en el desarrollo y operación de la red I2P, la mayoría de los cuales ahora están distribuidos. Los ataques contra recursos accesibles externamente afectan principalmente la capacidad de los nuevos usuarios para encontrarnos, no el funcionamiento de la red en sí.

- El sitio web está replicado y utiliza DNS round-robin para acceso público externo.
- Los routers ahora admiten [múltiples ubicaciones externas de reseed](/docs/overview/faq/#reseed), sin embargo pueden necesitarse más hosts de reseed, y el manejo de hosts de reseed no confiables o maliciosos puede necesitar mejoras.
- Los routers ahora admiten múltiples ubicaciones de archivos de actualización. Un host de actualización malicioso podría proporcionar un archivo enorme; es necesario limitar el tamaño.
- Los routers ahora admiten múltiples firmantes de actualización confiables por defecto.
- Los routers ahora manejan mejor múltiples peers floodfill no confiables. Los floodfills maliciosos necesitan más estudio.
- El código ahora se almacena en un sistema de control de código fuente distribuido.
- Los routers dependen de un solo host de noticias, pero hay una URL de respaldo codificada que apunta a un host diferente. Un host de noticias malicioso podría proporcionar un archivo enorme; es necesario limitar el tamaño.
- Los [servicios del sistema de nombres](/docs/overview/naming/), incluyendo proveedores de suscripción de libreta de direcciones, servicios add-host y servicios de salto, podrían ser maliciosos. Se implementaron protecciones sustanciales para suscripciones en la versión 0.6.1.31, con mejoras adicionales en versiones posteriores. Sin embargo, todos los servicios de nombres requieren cierta medida de confianza; consulta [la página de nombres](/docs/overview/naming/) para más detalles.
- Seguimos dependiendo del servicio DNS para i2p2.de; perder esto causaría una interrupción sustancial en nuestra capacidad de atraer nuevos usuarios, y reduciría la red (a corto y mediano plazo), tal como lo hizo la pérdida de i2p.net.

### Ataques de Desarrollo

Estos ataques no van dirigidos directamente contra la red, sino que van tras su equipo de desarrollo, ya sea introduciendo obstáculos legales a cualquiera que contribuya al desarrollo del software, o utilizando cualquier medio disponible para conseguir que los desarrolladores subviertan el software. Las medidas técnicas tradicionales no pueden derrotar estos ataques, y si alguien amenazara la vida o el sustento de un desarrollador (o incluso simplemente emitiera una orden judicial junto con una orden de silencio, bajo amenaza de prisión), tendríamos un gran problema.

Sin embargo, dos técnicas ayudan a defenderse contra estos ataques:

- Todos los componentes de la red deben ser de código abierto para permitir la inspección, verificación, modificación y mejora. Si un desarrollador se ve comprometido, una vez que se note, la comunidad debería exigir explicaciones y dejar de aceptar el trabajo de ese desarrollador. Todos los checkins a nuestro sistema de control de código fuente distribuido están firmados criptográficamente, y los empaquetadores de versiones utilizan un sistema de lista de confianza para restringir las modificaciones a aquellas previamente aprobadas.
- Desarrollo a través de la propia red, permitiendo que los desarrolladores permanezcan anónimos pero aún así aseguren el proceso de desarrollo. Todo el desarrollo de I2P puede ocurrir a través de I2P — utilizando un sistema de control de código fuente distribuido, chat IRC, servidores web públicos, foros de discusión (forum.i2p), y los sitios de distribución de software, todos disponibles dentro de I2P.

También mantenemos relaciones con varias organizaciones que ofrecen asesoría legal, en caso de que sea necesaria alguna defensa.

### Ataques de Implementación (Errores)

Por más que tratemos, la mayoría de aplicaciones no triviales incluyen errores en el diseño o implementación, e I2P no es una excepción. Puede haber errores que podrían ser explotados para atacar el anonimato o la seguridad de la comunicación que se ejecuta sobre I2P de maneras inesperadas. Para ayudar a resistir ataques contra el diseño o los protocolos en uso, publicamos todos los diseños y documentación y solicitamos revisión y críticas con la esperanza de que muchos ojos mejoren el sistema. No creemos en la seguridad por oscuridad.

Además, el código está siendo tratado de la misma manera, con poca aversión a retrabajar o descartar algo que no esté cumpliendo con las necesidades del sistema de software (incluyendo la facilidad de modificación). La documentación para el diseño e implementación de la red y los componentes de software son una parte esencial de la seguridad, ya que sin ella es poco probable que los desarrolladores estén dispuestos a dedicar el tiempo para aprender lo suficiente el software como para identificar deficiencias y errores.

Es probable que nuestro software contenga, en particular, errores relacionados con denegación de servicio a través de errores de memoria insuficiente (OOMs), problemas de cross-site-scripting (XSS) en la consola del router, y otras vulnerabilidades a entradas no estándar a través de los diversos protocolos.

I2P sigue siendo una red pequeña con una comunidad de desarrollo reducida y casi ningún interés por parte de grupos académicos o de investigación. Por lo tanto, carecemos del análisis que [otras redes de anonimato](https://torproject.org/) pueden haber recibido. Continuamos reclutando personas para que [se involucren](/get-involved/) y ayuden.

---

## Otras Defensas

### Listas de bloqueo

En cierta medida, I2P podría mejorarse para evitar pares que operen en direcciones IP incluidas en una lista de bloqueo. Varias listas de bloqueo están comúnmente disponibles en formatos estándar, enumerando organizaciones anti-P2P, potenciales adversarios a nivel estatal, y otros.

En la medida en que los peers activos aparezcan realmente en la lista de bloqueo actual, el bloqueo por solo un subconjunto de peers tendería a segmentar la red, exacerbar los problemas de alcanzabilidad y disminuir la confiabilidad general. Por lo tanto, querríamos acordar una lista de bloqueo particular y habilitarla por defecto.

Las listas de bloqueo son solo una parte (quizás una pequeña parte) de un conjunto de defensas contra la malicia. En gran medida, el sistema de perfiles hace un buen trabajo midiendo el comportamiento del router para que no necesitemos confiar en nada en netDb. Sin embargo, se puede hacer más. Para cada una de las áreas en la lista anterior, hay mejoras que podemos hacer en la detección de comportamiento malicioso.

Si una lista de bloqueo está alojada en una ubicación central con actualizaciones automáticas, la red es vulnerable a un [ataque de recurso central](#central-resource-attacks). La suscripción automática a una lista le da al proveedor de la lista el poder de cerrar completamente la red I2P.

Actualmente, se distribuye una lista de bloqueo predeterminada con nuestro software, que incluye únicamente las IPs de fuentes de ataques DOS previos. No existe un mecanismo de actualización automática. En caso de que un rango de IP particular implemente ataques serios contra la red I2P, tendríamos que pedir a las personas que actualicen su lista de bloqueo manualmente a través de mecanismos externos como foros, blogs, etc.
