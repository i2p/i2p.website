---
title: "Base de datos de red"
description: "Comprender la base de datos de red distribuida (netDb) de I2P - una DHT (tabla hash distribuida) especializada para la información de contacto de routers y las consultas de destinos"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Descripción general

La **netDb** (base de datos de red) es una base de datos distribuida especializada que contiene solo dos tipos de datos: - **RouterInfos** – información de contacto del router - **LeaseSets** – información de contacto del destino

Todos los datos están firmados criptográficamente y son verificables. Cada entrada incluye información de liveliness (estado de actividad) para descartar entradas obsoletas y reemplazar las desactualizadas, lo que protege contra ciertas clases de ataques.

La distribución utiliza un mecanismo de **floodfill**, donde un subconjunto de routers mantiene la base de datos distribuida.

---

## 2. RouterInfo (Información del router)

Cuando los routers necesitan ponerse en contacto con otros routers, intercambian paquetes de **RouterInfo** (información del router) que contienen:

- **Identidad del router** – clave de cifrado, clave de firma, certificado
- **Direcciones de contacto** – cómo alcanzar el router
- **Marca temporal de publicación** – cuándo se publicó esta información
- **Opciones de texto arbitrarias** – banderas de capacidad y configuraciones
- **Firma criptográfica** – demuestra la autenticidad

### 2.1 Indicadores de capacidad

Los routers anuncian sus capacidades mediante códigos de letras en su RouterInfo (información del router):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Clasificaciones de ancho de banda

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Valores de ID de red

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Estadísticas de RouterInfo

Los routers publican estadísticas opcionales de salud para el análisis de la red: - Tasas de éxito/rechazo/expiración por tiempo de espera en la construcción de tunnel exploratorio - Promedio de 1 hora del recuento de tunnels participantes

Las estadísticas siguen el formato `stat_(statname).(statperiod)` con valores separados por punto y coma.

**Estadísticas de ejemplo:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Los Floodfill routers también pueden publicar: `netdb.knownLeaseSets` y `netdb.knownRouters`

### 2.5 Opciones de familia

A partir de la versión 0.9.24, los routers pueden declarar pertenencia a una familia (mismo operador):

- **family**: Nombre de la familia
- **family.key**: Código de tipo de firma concatenado con la clave pública de firma codificada en base64
- **family.sig**: Firma del nombre de la familia y del hash del router de 32 bytes

Varios routers de la misma familia no se utilizarán en tunnels individuales.

### 2.6 Expiración de RouterInfo

- Sin expiración durante la primera hora de tiempo de actividad
- Sin expiración con 25 RouterInfos almacenados o menos
- La expiración se reduce a medida que crece el recuento local (72 horas con <120 routers; ~30 horas con 300 routers)
- Los introductores SSU expiran en ~1 hora
- Los Floodfills utilizan una expiración de 1 hora para todos los RouterInfos locales

---

## 3. LeaseSet (conjunto de concesiones temporales en I2P)

**LeaseSets** documentan puntos de entrada de tunnel para destinos concretos, especificando:

- **Identidad del router de entrada del tunnel**
- **ID de tunnel de 4 bytes**
- **Tiempo de expiración del tunnel**

Los LeaseSets incluyen: - **Destino** – clave de cifrado, clave de firma, certificado - **Clave pública adicional de cifrado** – para el garlic encryption de extremo a extremo - **Clave pública adicional de firma** – destinada a la revocación (actualmente sin uso) - **Firma criptográfica**

### 3.1 Variantes de LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Expiración de LeaseSet

Los LeaseSets (estructura de I2P que agrupa leases de entrada) regulares expiran en la expiración más tardía de sus leases. La expiración de LeaseSet2 se especifica en el encabezado. Las expiraciones de EncryptedLeaseSet y MetaLeaseSet pueden variar, con posible aplicación de un límite máximo.

---

## 4. Inicialización

La netDb descentralizada requiere al menos una referencia de par para integrarse. **Reseeding** (resembrado: proceso inicial para obtener pares) recupera archivos RouterInfo (`routerInfo-$hash.dat`) de los directorios netDb de los voluntarios. El primer arranque obtiene automáticamente desde URLs codificadas de forma fija seleccionadas aleatoriamente.

---

## 5. Mecanismo de Floodfill

El netDb floodfill utiliza almacenamiento distribuido simple: envía los datos al par floodfill más cercano. Cuando los pares que no son floodfill envían datos para almacenar, los floodfill los reenvían a un subconjunto de pares floodfill más cercanos a la clave específica.

La participación en Floodfill se indica como un indicador de capacidad (`f`) en RouterInfo (estructura de información del router).

### 5.1 Requisitos de adhesión voluntaria a Floodfill

A diferencia de los servidores de directorio de confianza predefinidos de Tor, el conjunto de floodfill de I2P es **no confiable** y cambia con el tiempo.

Floodfill (modo del router para almacenar y distribuir la netDb) se habilita automáticamente solo en routers de alto ancho de banda que cumplan estos requisitos: - Mínimo 128 KBytes/sec de ancho de banda compartido (configurado manualmente) - Debe superar pruebas de estado adicionales (tiempo de la cola de mensajes salientes, retraso de tareas)

La inclusión automática actual da como resultado aproximadamente **un 6% de participación de floodfill en la red** (nodos especializados que almacenan y propagan la netDb).

Los floodfill (nodos especiales que almacenan y propagan la netDb) configurados manualmente coexisten con los voluntarios automáticos. Cuando el recuento de floodfill cae por debajo del umbral, los routers de alto ancho de banda se ofrecen automáticamente como voluntarios. Cuando existen demasiados floodfill, dejan de actuar como floodfill.

### 5.2 Roles de Floodfill

Además de aceptar operaciones de almacenamiento en la netDb y responder a consultas, los floodfills realizan funciones estándar de router. Su mayor ancho de banda normalmente implica una mayor participación en tunnels, pero esto no está directamente relacionado con los servicios de base de datos.

---

## 6. Métrica de proximidad de Kademlia

netDb utiliza una métrica de distancia basada en XOR de **estilo Kademlia**. El hash SHA256 de RouterIdentity o Destination crea la clave de Kademlia (excepto para LS2 Encrypted LeaseSets, que usan SHA256 del byte de tipo 3 junto con la clave pública cegada).

### 6.1 Rotación del espacio de claves

Para aumentar los costos de un ataque Sybil, en lugar de usar `SHA256(key)`, el sistema utiliza:

```
SHA256(key + yyyyMMdd)
```
donde la fecha es una fecha UTC ASCII de 8 bytes. Esto crea la **routing key** (clave de enrutamiento), que cambia diariamente a la medianoche UTC—lo que se denomina **keyspace rotation** (rotación del espacio de claves).

Las claves de enrutamiento nunca se transmiten en mensajes I2NP; solo se utilizan para la determinación de la distancia local.

---

## 7. Segmentación de la base de datos de red

Las DHT tradicionales de Kademlia no preservan la no vinculabilidad de la información almacenada. I2P previene ataques que asocian los tunnels de cliente con routers implementando **segmentación**.

### 7.1 Estrategia de segmentación

Los Routers registran: - Si las entradas llegaron vía tunnels de cliente o directamente - Si fue vía tunnel, qué tunnel de cliente/destino - Se registran llegadas por múltiples tunnels - Se distinguen las respuestas de almacenamiento frente a las de búsqueda

Tanto las implementaciones en Java como en C++ utilizan: - Una **"Principal" netDb** para búsquedas directas/operaciones de floodfill en el contexto del router - **"Bases de datos de red de cliente"** o **"Sub-bases de datos"** en contextos de cliente, capturando entradas enviadas a tunnels de cliente

Los netDbs de cliente existen solo durante la vida útil del cliente y contienen únicamente entradas de tunnel de cliente. Las entradas provenientes de tunnels de cliente no pueden solaparse con llegadas directas.

Cada netDb registra si las entradas llegaron como stores (mensajes de almacenamiento; responden a solicitudes de búsqueda) o como respuestas de búsqueda (solo responden si previamente se almacenó en el mismo destino). Los clientes nunca responden consultas con entradas del netDb principal, solo con entradas de la base de datos de red del cliente.

Las estrategias combinadas **segmentan** la netDb (base de datos de red de I2P) contra los ataques de asociación cliente-router.

---

## 8. Almacenamiento, verificación y consulta

### 8.1 Almacenamiento de RouterInfo en pares

I2NP `DatabaseStoreMessage` que contiene el intercambio de RouterInfo (información del router) local durante la inicialización de la conexión de transporte NTCP o SSU.

### 8.2 Almacenamiento de LeaseSet en pares

Los mensajes I2NP `DatabaseStoreMessage` que contienen el LeaseSet local se intercambian periódicamente mediante mensajes cifrados con garlic encryption, empaquetados con el tráfico del Destino, lo que permite respuestas sin consultas de LeaseSet.

### 8.3 Selección de Floodfill

`DatabaseStoreMessage` envía al floodfill más cercano a la clave de enrutamiento actual. El floodfill más cercano se encuentra mediante una búsqueda en la base de datos local. Aunque no sea realmente el más cercano, la difusión por inundación lo propaga "más cerca" enviándolo a múltiples floodfills.

Kademlia tradicional utiliza una búsqueda "find-closest" (búsqueda del más cercano) antes de la inserción. Aunque I2NP carece de tales mensajes, los routers pueden realizar una búsqueda iterativa con el bit menos significativo invertido (`key ^ 0x01`) para garantizar el descubrimiento del par más cercano real.

### 8.4 Almacenamiento de RouterInfo (información del router) en los Floodfills

Los routers publican RouterInfo conectándose directamente a un floodfill, enviando un I2NP `DatabaseStoreMessage` con un token de respuesta distinto de cero. El mensaje no usa garlic encryption (técnica de cifrado 'garlic' propia de I2P) de extremo a extremo (conexión directa, sin intermediarios). El floodfill responde con `DeliveryStatusMessage` usando el token de respuesta como ID de mensaje.

Los Routers también pueden enviar RouterInfo a través de un tunnel exploratorio (límites de conexión, incompatibilidad, ocultación de IP). Los Floodfills pueden rechazar dichos almacenamientos durante una sobrecarga.

### 8.5 Almacenamiento de LeaseSet (metadatos de enrutamiento para contactar un destino en I2P) en los Floodfills (routers especiales que almacenan y difunden datos)

El almacenamiento de LeaseSet es más sensible que RouterInfo (información del router). Los routers deben impedir la asociación de un LeaseSet con ellos mismos.

Los routers publican el LeaseSet mediante un tunnel de cliente saliente, enviando un `DatabaseStoreMessage` con un token de respuesta distinto de cero. El mensaje está cifrado de extremo a extremo usando garlic encryption mediante el Administrador de claves de sesión del Destino, lo que lo oculta del extremo de salida del tunnel. El floodfill responde con un `DeliveryStatusMessage` devuelto a través del tunnel entrante.

### 8.6 Proceso de inundación

Los Floodfills validan RouterInfo (información del router)/LeaseSet antes de almacenarlos localmente utilizando criterios adaptativos que dependen de la carga, del tamaño de la netdb y de otros factores.

Después de recibir datos más nuevos válidos, los floodfills lo "inundan" buscando los 3 routers floodfill más cercanos a la clave de enrutamiento. Las conexiones directas envían I2NP `DatabaseStoreMessage` con Token de respuesta cero. Otros routers no responden ni vuelven a inundar.

**Restricciones importantes:** - Floodfills (nodos floodfill) no deben propagar a través de tunnels; solo conexiones directas - Floodfills nunca propagan un LeaseSet expirado ni un RouterInfo (información del router) publicado hace más de una hora

### 8.7 Búsqueda de RouterInfo y LeaseSet

I2NP `DatabaseLookupMessage` solicita entradas de netDb (base de datos de red) a routers floodfill (nodos que almacenan y propagan la netDb). Las consultas se envían por un tunnel exploratorio saliente; las respuestas especifican el tunnel exploratorio entrante para el retorno.

Las consultas generalmente se envían, en paralelo, a dos routers floodfill "buenos" más cercanos a la clave solicitada.

- **Coincidencia local**: recibe una respuesta I2NP de tipo `DatabaseStoreMessage`
- **Sin coincidencia local**: recibe I2NP `DatabaseSearchReplyMessage` con referencias a otros routers floodfill (routers especiales que almacenan y distribuyen la netDb) cercanas a la clave

Las búsquedas de LeaseSet usan garlic encryption de extremo a extremo (a partir de la versión 0.9.5). Las búsquedas de RouterInfo (información del router) no están cifradas debido al costo computacional de ElGamal, lo que las hace vulnerables a la inspección por parte del extremo de salida.

A partir de la 0.9.7, las respuestas de búsqueda incluyen la clave de sesión y la etiqueta, ocultando dichas respuestas a la puerta de enlace de entrada.

### 8.8 Consultas iterativas

Antes de la 0.8.9: Dos consultas redundantes en paralelo sin enrutamiento recursivo ni iterativo.

A partir de la 0.8.9: **Búsquedas iterativas** implementadas sin redundancia—más eficientes, fiables y adecuadas para un conocimiento de floodfill incompleto. A medida que las redes crecen y los routers conocen menos floodfills, las búsquedas se acercan a una complejidad O(log n).

Las búsquedas iterativas continúan incluso sin referencias a pares más cercanos, lo que evita el black-holing (absorción del tráfico sin respuesta) malicioso. Se aplican el número máximo de consultas y el tiempo de espera actuales.

### 8.9 Verificación

**Verificación de RouterInfo (información del router)**: Deshabilitada a partir de la versión 0.9.7.1 para evitar los ataques descritos en el artículo "Practical Attacks Against the I2P Network".

**Verificación de LeaseSet**: Los routers esperan ~10 segundos, luego realizan una consulta desde un floodfill diferente a través de un tunnel de cliente saliente. La garlic encryption de extremo a extremo oculta la información al extremo saliente. Las respuestas vuelven a través de tunnels entrantes.

A partir de la versión 0.9.7, las respuestas se cifran con session key/tag hiding (ocultación de clave/etiqueta de sesión) desde la puerta de enlace entrante.

### 8.10 Exploración

**Exploración** implica una búsqueda en netDb con claves aleatorias para descubrir nuevos routers. Los Floodfills responden con `DatabaseSearchReplyMessage` que contiene hashes de routers que no son floodfill cercanos a la clave solicitada. Las consultas de exploración establecen una bandera especial en `DatabaseLookupMessage`.

---

## 9. MultiHoming (conexión múltiple a redes/proveedores)

Las Destinations (destinos de I2P) que usan claves privadas/públicas idénticas (el `eepPriv.dat` tradicional) pueden alojarse en múltiples routers simultáneamente. Cada instancia publica periódicamente LeaseSets firmados; el LeaseSet publicado más reciente se devuelve a quienes realizan la consulta. Con tiempos de vida de LeaseSet de un máximo de 10 minutos, las interrupciones duran como mucho ~10 minutos.

A partir de la 0.9.38, **Meta LeaseSets** admiten servicios multihomed (con múltiples puntos de conexión) de gran escala mediante Destinations (destinos) separados que proporcionan servicios comunes. Las entradas de Meta LeaseSet son Destinations u otros Meta LeaseSets con caducidades de hasta 18,2 horas, lo que permite que cientos/miles de Destinations alojen servicios comunes.

---

## 10. Análisis de amenazas

Aproximadamente 1700 floodfill routers (routers especializados que almacenan y propagan la netDb) operan actualmente. El crecimiento de la red hace que la mayoría de los ataques sean más difíciles o de menor impacto.

### 10.1 Mitigaciones generales

- **Crecimiento**: Más floodfills hacen que los ataques sean más difíciles o menos impactantes
- **Redundancia**: Todas las entradas de netdb se almacenan en 3 routers floodfill más cercanos a la clave mediante inundación
- **Firmas**: Todas las entradas están firmadas por su creador; las falsificaciones son imposibles

### 10.2 Routers lentos o que no responden

Routers (enrutadores de I2P) mantienen estadísticas ampliadas del perfil de par para floodfills (nodos especiales que almacenan la base de datos de red de I2P):
- Tiempo de respuesta promedio
- Porcentaje de respuestas a consultas
- Porcentaje de éxito en la verificación del almacenamiento
- Último almacenamiento correcto
- Última búsqueda correcta
- Última respuesta

Los routers utilizan estas métricas al determinar la "bondad" para seleccionar el floodfill más cercano. Los routers que no responden en absoluto se identifican y se evitan rápidamente; los routers parcialmente maliciosos plantean un desafío mayor.

### 10.3 Ataque Sybil (espacio de claves completo)

Los atacantes podrían crear numerosos routers floodfill distribuidos por todo el espacio de claves como un ataque de denegación de servicio (DoS) eficaz.

Si el comportamiento indebido no es suficiente para la designación de "bad", las posibles respuestas incluyen: - Compilar listas de hash/IP de router "bad" anunciadas a través de las noticias de la consola, el sitio web y el foro - Habilitación de floodfill (nodos especiales que almacenan y distribuyen la netDb) en toda la red ("combatir a Sybil con más Sybil") - Nuevas versiones del software con listas "bad" codificadas de forma fija - Métricas y umbrales mejorados de perfiles de pares para la identificación automática - Cualificación de bloque IP que descalifique múltiples floodfills en un único bloque IP - Lista negra automática basada en suscripción (similar al consenso de Tor)

Las redes más grandes hacen que esto sea más difícil.

### 10.4 Ataque Sybil (espacio de claves parcial)

Los atacantes podrían crear entre 8 y 15 routers floodfill agrupados muy cerca en el espacio de claves. Todas las consultas/almacenamientos para ese espacio de claves se dirigen a routers del atacante, lo que permite realizar ataques de denegación de servicio (DoS) contra sitios I2P concretos.

Dado que el espacio de claves indexa hashes criptográficos SHA256, los atacantes necesitan fuerza bruta para generar routers con proximidad suficiente.

**Defensa**: El algoritmo de cercanía de Kademlia varía con el tiempo usando `SHA256(key + YYYYMMDD)`, cambiando diariamente a medianoche UTC. Esta **rotación del espacio de claves** fuerza la regeneración diaria del ataque.

> **Nota**: Investigaciones recientes indican que la rotación del espacio de claves no es particularmente efectiva—los atacantes pueden precalcular hashes de router, bastando con unos cuantos routers para eclipsar porciones del espacio de claves en media hora tras la rotación.

Consecuencia de la rotación diaria: el netdb distribuido se vuelve poco confiable durante unos minutos después de la rotación—las consultas fallan antes de que el nuevo router más cercano reciba los mensajes de almacenamiento.

### 10.5 Ataques de arranque

Los atacantes podrían tomar el control de reseed websites (sitios web de arranque/bootstrapping de I2P) o engañar a los desarrolladores para que añadan reseed websites hostiles, provocando que routers nuevos arranquen en redes aisladas/controladas por la mayoría.

**Defensas implementadas:** - Obtener subconjuntos de RouterInfo (información del router) desde múltiples sitios de reseed (proceso de incorporación inicial de pares) en lugar de un único sitio - Monitoreo de reseed fuera de la red mediante sondeos periódicos a los sitios - A partir de la 0.9.14, los paquetes de datos de reseed son archivos zip firmados con verificación de la firma descargada (ver [especificación su3](/docs/specs/updates))

### 10.6 Captura de consultas

Los Floodfill routers podrían "redirigir" a los pares hacia routers controlados por un atacante mediante referencias devueltas.

Es poco probable mediante exploración debido a su baja frecuencia; los routers obtienen referencias de pares principalmente mediante la construcción normal de tunnel.

A partir de la 0.8.9, se implementaron búsquedas iterativas. Se siguen las referencias de floodfill de `DatabaseSearchReplyMessage` si están más cerca de la clave de búsqueda. Los routers solicitantes no confían en la proximidad de las referencias. Las búsquedas continúan aunque no se encuentren claves más cercanas, hasta que se alcance el tiempo de espera o el máximo de consultas, evitando el black-holing malicioso (desvío malicioso del tráfico a un sumidero).

### 10.7 Fugas de información

La filtración de información en la DHT (tabla hash distribuida) de I2P requiere una investigación adicional. Los Floodfill routers observan las consultas y recaban información. Con un 20% de nodos maliciosos, las amenazas Sybil (ataques con identidades múltiples) descritas anteriormente se vuelven problemáticas por múltiples motivos.

---

## 11. Trabajo futuro

- Cifrado de extremo a extremo de consultas y respuestas adicionales de netDb
- Mejores métodos de seguimiento de respuestas de consultas
- Métodos de mitigación para problemas de confiabilidad en la rotación del espacio de claves

---

## 12. Referencias

- [Especificación de estructuras comunes](/docs/specs/common-structures/) – estructuras RouterInfo y LeaseSet
- [Especificación de I2NP](/docs/specs/i2np/) – tipos de mensajes de la base de datos
- [Propuesta 123: Nuevas entradas de netDb](/proposals/123-new-netdb-entries) – especificación de LeaseSet2
- [Discusión histórica de netDb](/docs/netdb/) – historial de desarrollo y debates archivados
