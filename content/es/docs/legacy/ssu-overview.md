---
title: "Secure Semireliable UDP (SSU)"
description: "Transporte UDP original utilizado antes de SSU2 (obsoleto)"
slug: "ssu-overview"
aliases:
  - "/es/udp"
  - "/es/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**OBSOLETO** - SSU ha sido reemplazado por SSU2. El soporte para SSU fue eliminado de i2pd en la versión 2.44.0 (API 0.9.56) 2022-11. El soporte para SSU fue eliminado de Java I2P en la versión 2.4.0 (API 0.9.61) 2023-12.

SSU (también llamado "UDP" en gran parte de la documentación y interfaces de usuario de I2P) fue uno de los dos [transportes](/docs/transport) implementados en I2P. El otro es [NTCP2](/docs/specs/ntcp2). Se ha eliminado el soporte para [NTCP](/docs/legacy/ntcp).

SSU fue introducido en la versión 0.6 de I2P. En una instalación estándar de I2P, el router utiliza tanto NTCP como SSU para conexiones salientes. SSU-sobre-IPv6 es compatible desde la versión 0.9.8.

SSU se llama "semifiable" porque retransmitirá repetidamente los mensajes no confirmados, pero solo hasta un número máximo de veces. Después de eso, el mensaje se descarta.

## Servicios SSU

Al igual que el transporte NTCP, SSU proporciona transporte de datos confiable, encriptado, orientado a conexión y punto a punto. Exclusivo de SSU, también proporciona servicios de detección de IP y traversal de NAT, incluyendo:

- Traversal cooperativo de NAT/Firewall usando [introducers](#introduction)
- Detección de IP local mediante inspección de paquetes entrantes y [peer testing](#peerTesting)
- Comunicación del estado del firewall e IP local, y cambios de cualquiera de estos a NTCP
- Comunicación del estado del firewall e IP local, y cambios de cualquiera de estos, al router y la interfaz de usuario

## Especificación de Dirección del Router {#ra}

Las siguientes propiedades se almacenan en la base de datos de red.

- **Transport name:** SSU
- **caps:** [B,C,4,6] [Ver abajo](#capabilities).
- **host:** IP (IPv4 o IPv6).
  Se permite dirección IPv6 acortada (con "::").
  Puede estar presente o no si está detrás de firewall.
  Los nombres de host estaban permitidos anteriormente, pero están obsoletos desde la versión 0.9.32. Ver propuesta 141.
- **iexp[0-2]:** Expiración de este introducer.
  Dígitos ASCII, en segundos desde la época.
  Solo presente si está detrás de firewall y se requieren introducers.
  Opcional (incluso si otras propiedades para este introducer están presentes).
  Desde la versión 0.9.30, propuesta 133.
- **ihost[0-2]:** IP del introducer (IPv4 o IPv6).
  Los nombres de host estaban permitidos anteriormente, pero están obsoletos desde la versión 0.9.32. Ver propuesta 141.
  Se permite dirección IPv6 acortada (con "::").
  Solo presente si está detrás de firewall y se requieren introducers.
  [Ver abajo](#introduction).
- **ikey[0-2]:** Clave de introducción Base 64 del introducer. [Ver abajo](#key).
  Solo presente si está detrás de firewall y se requieren introducers.
  [Ver abajo](#introduction).
- **iport[0-2]:** Puerto del introducer 1024 - 65535.
  Solo presente si está detrás de firewall y se requieren introducers.
  [Ver abajo](#introduction).
- **itag[0-2]:** Etiqueta del introducer 1 - (2^32 - 1)
  Dígitos ASCII.
  Solo presente si está detrás de firewall y se requieren introducers.
  [Ver abajo](#introduction).
- **key:** Clave de introducción Base 64. [Ver abajo](#key).
- **mtu:** Opcional. Por defecto y máximo es 1484. Mínimo es 620.
  Debe estar presente para IPv6, donde el mínimo es 1280 y el máximo es 1488
  (el máximo era 1472 antes de la versión 0.9.28).
  El MTU de IPv6 debe ser múltiplo de 16.
  (MTU de IPv4 + 4) debe ser múltiplo de 16.
  [Ver abajo](#mtu).
- **port:** 1024 - 65535
  Puede estar presente o no si está detrás de firewall.

# Detalles del Protocolo

## Control de Congestión {#congestioncontrol}

La necesidad de SSU de solo entrega semifiable, operación amigable con TCP, y la capacidad de alto rendimiento permite una gran flexibilidad en el control de congestión. El algoritmo de control de congestión descrito a continuación está diseñado para ser tanto eficiente en ancho de banda como simple de implementar.

Los paquetes se programan según la política del router, teniendo cuidado de no exceder la capacidad de salida del router o de exceder la capacidad medida del peer remoto. La capacidad medida opera siguiendo las líneas del inicio lento y la evitación de congestión de TCP, con incrementos aditivos a la capacidad de envío y decrementos multiplicativos ante la congestión. A diferencia de TCP, los routers pueden abandonar algunos mensajes después de un período determinado o número de retransmisiones mientras continúan transmitiendo otros mensajes.

Las técnicas de detección de congestión también varían de TCP, ya que cada mensaje tiene su propio identificador único y no secuencial, y cada mensaje tiene un tamaño limitado - como máximo, 32KB. Para transmitir eficientemente esta retroalimentación al remitente, el receptor incluye periódicamente una lista de identificadores de mensajes completamente confirmados con ACK y también puede incluir campos de bits para mensajes parcialmente recibidos, donde cada bit representa la recepción de un fragmento. Si llegan fragmentos duplicados, el mensaje debe ser confirmado con ACK nuevamente, o si el mensaje aún no ha sido completamente recibido, el campo de bits debe ser retransmitido con cualquier nueva actualización.

La implementación actual no rellena los paquetes a ningún tamaño particular, sino que simplemente coloca un único fragmento de mensaje en un paquete y lo envía (con cuidado de no exceder el MTU).

### MTU {#mtu}

A partir de la versión 0.8.12 del router, se utilizan dos valores MTU para IPv4: 620 y 1484. El valor MTU se ajusta según el porcentaje de paquetes que son retransmitidos.

Para ambos valores de MTU, es deseable que (MTU % 16) == 12, de modo que la porción de carga útil después del encabezado IP/UDP de 28 bytes sea un múltiplo de 16 bytes, para propósitos de cifrado.

Para el valor pequeño de MTU, es deseable empaquetar un Variable Tunnel Build Message de 2646 bytes de manera eficiente en múltiples paquetes; con un MTU de 620 bytes, encaja perfectamente en 5 paquetes.

Basado en mediciones, 1492 se ajusta a casi todos los mensajes I2NP razonablemente pequeños (los mensajes I2NP más grandes pueden llegar a 1900 a 4500 bytes, que de todos modos no van a caber en un MTU de red en vivo).

Los valores de MTU fueron 608 y 1492 para las versiones 0.8.9 - 0.8.11. El MTU grande era 1350 antes de la versión 0.8.9.

El tamaño máximo de paquete de recepción es de 1571 bytes a partir de la versión 0.8.12. Para las versiones 0.8.9 - 0.8.11 era de 1535 bytes. Antes de la versión 0.8.9 era de 2048 bytes.

A partir de la versión 0.9.2, si la MTU de la interfaz de red de un router es menor a 1484, publicará esa información en la base de datos de red, y otros routers deberían respetarla cuando se establezca una conexión.

Para IPv6, el MTU mínimo es 1280. El encabezado IPv6 IP/UDP es de 48 bytes, por lo que usamos un MTU donde (MTU % 16 == 0), lo cual es verdadero para 1280. El MTU máximo de IPv6 es 1488. (el máximo era 1472 antes de la versión 0.9.28).

### Límites de Tamaño de Mensaje {#max}

Aunque el tamaño máximo de mensaje es nominalmente de 32KB, el límite práctico difiere. El protocolo limita el número de fragmentos a 7 bits, o 128. Sin embargo, la implementación actual limita cada mensaje a un máximo de 64 fragmentos, lo cual es suficiente para 64 * 534 = 33.3 KB cuando se usa el MTU de 608. Debido a la sobrecarga por los leaseSet agrupados y las claves de sesión, el límite práctico a nivel de aplicación es aproximadamente 6KB menor, o cerca de 26KB. Es necesario trabajo adicional para elevar el límite de transporte UDP por encima de 32KB. Para conexiones que usan el MTU más grande, son posibles mensajes más grandes.

## Tiempo de Espera de Inactividad

El tiempo de espera de inactividad y el cierre de conexión queda a discreción de cada extremo y puede variar. La implementación actual reduce el tiempo de espera cuando el número de conexiones se aproxima al máximo configurado, y aumenta el tiempo de espera cuando el número de conexiones es bajo. El tiempo de espera mínimo recomendado es de dos minutos o más, y el tiempo de espera máximo recomendado es de diez minutos o más.

## Claves {#keys}

Todo el cifrado utilizado es AES256/CBC con claves de 32 bytes e IVs de 16 bytes. Cuando Alice origina una sesión con Bob, las claves MAC y de sesión se negocian como parte del intercambio DH, y luego se utilizan para el HMAC y el cifrado, respectivamente. Durante el intercambio DH, la introKey públicamente conocible de Bob se utiliza para el MAC y el cifrado.

Tanto el mensaje inicial como la respuesta posterior utilizan la introKey del receptor (Bob) - el receptor no necesita conocer la introKey del solicitante (Alice). La clave de firma DSA utilizada por Bob debería ser conocida por Alice cuando ella lo contacta, aunque la clave DSA de Alice puede no ser conocida por Bob.

Al recibir un mensaje, el receptor verifica la dirección IP "from" y el puerto con todas las sesiones establecidas - si hay coincidencias, las claves MAC de esa sesión se prueban en el HMAC. Si ninguna de esas verifica o si no hay direcciones IP coincidentes, el receptor intenta su introKey en el MAC. Si eso no verifica, el paquete se descarta. Si sí verifica, se interpreta según el tipo de mensaje, aunque si el receptor está sobrecargado, puede descartarse de todos modos.

Si Alice y Bob tienen una sesión establecida, pero Alice pierde las claves por alguna razón y quiere contactar a Bob, puede en cualquier momento simplemente establecer una nueva sesión a través del SessionRequest y mensajes relacionados. Si Bob ha perdido la clave pero Alice no sabe eso, ella primero intentará incitarlo a responder, enviando un DataMessage con la bandera wantReply activada, y si Bob falla continuamente en responder, ella asumirá que la clave se perdió y reestablecerá una nueva.

Para el acuerdo de claves DH, se utiliza el grupo MODP de 2048 bits (#14) de [RFC3526](http://www.faqs.org/rfcs/rfc3526.html):

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Estos son los mismos p y g utilizados para el [cifrado ElGamal](/docs/specs/cryptography#elgamal) de I2P.

## Prevención de Reproducción {#replay}

La prevención de replay en la capa SSU ocurre rechazando paquetes con marcas de tiempo excesivamente antiguas o aquellos que reutilizan un IV. Para detectar IVs duplicados, se emplea una secuencia de filtros Bloom que "decaen" periódicamente para que solo se detecten los IVs agregados recientemente.

Los messageIds utilizados en DataMessages se definen en capas superiores al transporte SSU y se pasan de forma transparente. Estos IDs no siguen ningún orden particular - de hecho, es probable que sean completamente aleatorios. La capa SSU no intenta prevenir la reproducción de messageId - las capas superiores deben tener esto en cuenta.

## Direccionamiento {#addressing}

Para contactar con un peer SSU, es necesario uno de dos conjuntos de información: una dirección directa, para cuando el peer es públicamente accesible, o una dirección indirecta, para usar a un tercero que presente al peer. No hay restricción en el número de direcciones que un peer puede tener.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Cada una de las direcciones también puede exponer una serie de opciones - capacidades especiales de ese peer en particular. Para una lista de capacidades disponibles, consulta [más abajo](#capabilities).

Las direcciones, opciones y capacidades se publican en la [base de datos de red](/docs/overview/network-database).

## Establecimiento de Sesión Directa {#direct}

El establecimiento directo de sesión se utiliza cuando no se requiere una tercera parte para el atravesamiento de NAT. La secuencia de mensajes es la siguiente:

### Establecimiento de Conexión (Directa) {#establishDirect}

Alice se conecta directamente a Bob. IPv6 es compatible desde la versión 0.9.8.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Después de recibir el mensaje SessionConfirmed, Bob envía un pequeño [mensaje DeliveryStatus](/docs/specs/i2np#msg_DeliveryStatus) como confirmación. En este mensaje, el ID de mensaje de 4 bytes se establece a un número aleatorio, y el "tiempo de llegada" de 8 bytes se establece al ID actual de toda la red, que es 2 (es decir, 0x0000000000000002).

Después de que se envía el mensaje de estado, los peers usualmente intercambian [mensajes DatabaseStore](/docs/specs/i2np#msg_DatabaseStore) que contienen sus [RouterInfos](/docs/specs/common-structures#struct_RouterInfo), sin embargo, esto no es requerido.

No parece que importe el tipo del mensaje de estado o su contenido. Se agregó originalmente porque el mensaje DatabaseStore se retrasaba varios segundos; dado que el almacén ahora se envía inmediatamente, tal vez el mensaje de estado pueda eliminarse.

## Introducción {#introduction}

Las claves de introducción se entregan a través de un canal externo (la base de datos de red), donde tradicionalmente han sido idénticas al Hash del router hasta la versión 0.9.47, pero pueden ser aleatorias a partir de la versión 0.9.48. Deben usarse al establecer una clave de sesión. Para la dirección indirecta, el peer debe primero contactar al relayhost y pedirle una introducción al peer conocido en ese relayhost bajo la etiqueta dada. Si es posible, el relayhost envía un mensaje al peer direccionado diciéndole que contacte al peer solicitante, y también le da al peer solicitante la IP y puerto en el que se encuentra el peer direccionado. Además, el peer que establece la conexión debe ya conocer las claves públicas del peer al que se está conectando (pero no es necesario para ningún peer de retransmisión intermediario).

El establecimiento indirecto de sesión mediante la introducción de un tercero es necesario para un atravieso eficiente de NAT. Charlie, un router detrás de un NAT o cortafuegos que no permite paquetes UDP entrantes no solicitados, primero contacta a algunos pares, eligiendo algunos para que sirvan como introductores. Cada uno de estos pares (Bob, Bill, Betty, etc) proporciona a Charlie una etiqueta de introducción - un número aleatorio de 4 bytes - que él luego pone a disposición del público como métodos para contactarlo. Alice, un router que tiene los métodos de contacto publicados de Charlie, primero envía un paquete RelayRequest a uno o más de los introductores, pidiendo a cada uno que la presente a Charlie (ofreciendo la etiqueta de introducción para identificar a Charlie). Bob luego reenvía un paquete RelayIntro a Charlie incluyendo la IP pública y número de puerto de Alice, después envía a Alice de vuelta un paquete RelayResponse que contiene la IP pública y número de puerto de Charlie. Cuando Charlie recibe el paquete RelayIntro, envía un pequeño paquete aleatorio a la IP y puerto de Alice (abriendo un agujero en su NAT/cortafuegos), y cuando Alice recibe el paquete RelayResponse de Bob, ella inicia un nuevo establecimiento de sesión de dirección completa con la IP y puerto especificados.

### Establecimiento de Conexión (Indirecto Usando un Introductor) {#establishIndirect}

Alice primero se conecta al introducer Bob, quien retransmite la solicitud a Charlie.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Después del hole punch, la sesión se establece entre Alice y Charlie como en un establecimiento directo.

### Notas sobre IPv6

IPv6 es compatible desde la versión 0.9.8. Las direcciones de relay publicadas pueden ser IPv4 o IPv6, y la comunicación Alice-Bob puede ser a través de IPv4 o IPv6. Hasta la versión 0.9.49, la comunicación Bob-Charlie y Alice-Charlie es solo a través de IPv4. El relaying para IPv6 es compatible desde la versión 0.9.50. Consulta la especificación para más detalles.

Aunque la especificación fue cambiada a partir de la versión 0.9.8, la comunicación Alice-Bob a través de IPv6 no fue realmente compatible hasta la versión 0.9.50. Las versiones anteriores de los routers Java publicaron erróneamente la capacidad 'C' para direcciones IPv6, aunque en realidad no actuaban como introducer a través de IPv6. Por lo tanto, los routers solo deben confiar en la capacidad 'C' en una dirección IPv6 si la versión del router es 0.9.50 o superior.

## Pruebas de Peers {#peerTesting}

La automatización de las pruebas colaborativas de accesibilidad para peers está habilitada por una secuencia de mensajes PeerTest. Con su ejecución adecuada, un peer podrá determinar su propia accesibilidad y puede actualizar su comportamiento en consecuencia. El proceso de prueba es bastante simple:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Cada uno de los mensajes PeerTest lleva un nonce que identifica la serie de pruebas en sí, tal como fue inicializada por Alice. Si Alice no recibe un mensaje particular que espera, retransmitirá en consecuencia, y basándose en los datos recibidos o los mensajes faltantes, conocerá su accesibilidad. Los diversos estados finales que pueden alcanzarse son los siguientes:

- Si ella no recibe una respuesta de Bob, retransmitirá hasta un cierto número de veces, pero si nunca llega ninguna respuesta, sabrá que su firewall o NAT está de alguna manera mal configurado, rechazando todos los paquetes UDP entrantes incluso en respuesta directa a un paquete saliente. Alternativamente, Bob puede estar caído o no poder conseguir que Charlie responda.

- Si Alice no recibe un mensaje PeerTest con el
  nonce esperado de un tercero (Charlie), retransmitirá
  su solicitud inicial a Bob hasta cierto número de veces, incluso
  si ya ha recibido la respuesta de Bob. Si el primer mensaje
  de Charlie aún no llega pero el de Bob sí, ella sabe que está
  detrás de un NAT o firewall que está rechazando intentos de conexión
  no solicitados y que el reenvío de puertos no está funcionando correctamente (la
  IP y puerto que Bob proporcionó deberían estar reenviados).

- Si Alice recibe el mensaje PeerTest de Bob y ambos mensajes PeerTest de Charlie, pero los números de IP y puerto incluidos en los segundos mensajes de Bob y Charlie no coinciden, ella sabe que está detrás de un NAT simétrico, que reescribe todos sus paquetes salientes con diferentes puertos 'desde' para cada peer contactado. Necesitará reenviar explícitamente un puerto y mantener siempre ese puerto expuesto para la conectividad remota, ignorando futuros descubrimientos de puerto.

- Si Alice recibe el primer mensaje de Charlie pero no el segundo,
  retransmitirá su mensaje PeerTest a Charlie hasta un
  cierto número de veces, pero si no recibe respuesta sabe
  que Charlie está confundido o ya no está en línea.

Alice debería elegir a Bob arbitrariamente de entre los peers conocidos que parecen ser capaces de participar en pruebas de peer. Bob a su vez debería elegir a Charlie arbitrariamente de entre los peers que conoce que parecen ser capaces de participar en pruebas de peer y que están en una IP diferente tanto de Bob como de Alice. Si ocurre la primera condición de error (Alice no recibe mensajes PeerTest de Bob), Alice puede decidir designar un nuevo peer como Bob e intentar nuevamente con un nonce diferente.

La clave de introducción de Alice se incluye en todos los mensajes PeerTest para que Charlie pueda contactarla sin conocer información adicional. A partir de la versión 0.9.15, Alice debe tener una sesión establecida con Bob, para prevenir ataques de suplantación. Alice no debe tener una sesión establecida con Charlie para que la prueba de peer sea válida. Alice puede proceder a establecer una sesión con Charlie, pero no es obligatorio.

### Notas sobre IPv6

Hasta la versión 0.9.26, solo se soporta la prueba de direcciones IPv4. Solo se soporta la prueba de direcciones IPv4. Por lo tanto, toda la comunicación Alice-Bob y Alice-Charlie debe ser vía IPv4. La comunicación Bob-Charlie, sin embargo, puede ser vía IPv4 o IPv6. La dirección de Alice, cuando se especifica en el mensaje PeerTest, debe ser de 4 bytes. A partir de la versión 0.9.27, se soporta la prueba de direcciones IPv6, y la comunicación Alice-Bob y Alice-Charlie puede ser vía IPv6, si Bob y Charlie indican soporte con una capacidad 'B' en su dirección IPv6 publicada. Ver [Proposal 126](/spec/proposals/126-ipv6-peer-testing) para más detalles.

Antes de la versión 0.9.50, Alice envía la solicitud a Bob usando una sesión existente sobre el transporte (IPv4 o IPv6) que desea probar. Cuando Bob recibe una solicitud de Alice vía IPv4, Bob debe seleccionar un Charlie que anuncie una dirección IPv4. Cuando Bob recibe una solicitud de Alice vía IPv6, Bob debe seleccionar un Charlie que anuncie una dirección IPv6. La comunicación real entre Bob y Charlie puede ser vía IPv4 o IPv6 (es decir, independiente del tipo de dirección de Alice).

A partir de la versión 0.9.50, si el mensaje es sobre IPv6 para una prueba de peer IPv4, o (a partir de la versión 0.9.50) sobre IPv4 para una prueba de peer IPv6, Alice debe incluir su dirección y puerto de introducción.

Consulta la [Propuesta 158](/spec/proposals/158) para más detalles.

## Ventana de Transmisión, ACKs y Retransmisiones {#acks}

El mensaje DATA puede contener ACKs de mensajes completos y ACKs parciales de fragmentos individuales de un mensaje. Consulta la sección de mensaje de datos de [la página de especificación del protocolo](/docs/legacy/ssu) para más detalles.

Los detalles de las estrategias de ventana, ACK y retransmisión no se especifican aquí. Consulta el código Java para la implementación actual. Durante la fase de establecimiento, y para las pruebas de pares, los routers deben implementar retroceso exponencial para la retransmisión. Para una conexión establecida, los routers deben implementar una ventana de transmisión ajustable, estimación de RTT y timeout, similar a TCP o [streaming](/docs/api/streaming). Consulta el código para los parámetros iniciales, mínimos y máximos.

## Seguridad {#security}

Las direcciones de origen UDP pueden, por supuesto, ser falsificadas. Además, las IPs y puertos contenidos dentro de mensajes SSU específicos (RelayRequest, RelayResponse, RelayIntro, PeerTest) pueden no ser legítimos. También, ciertas acciones y respuestas pueden necesitar ser limitadas por tasa.

Los detalles de la validación no se especifican aquí. Los implementadores deben añadir defensas donde sea apropiado.

## Capacidades de Pares {#capabilities}

Una o más capacidades pueden publicarse en la opción "caps". Las capacidades pueden estar en cualquier orden, pero "BC46" es el orden recomendado, para mantener consistencia entre implementaciones.

**B** : Si la dirección del peer contiene la capacidad 'B', eso significa que están dispuestos y son capaces de participar en pruebas de peer como 'Bob' o 'Charlie'. Hasta la versión 0.9.26, las pruebas de peer no estaban soportadas para direcciones IPv6, y la capacidad 'B', si estaba presente para una dirección IPv6, debía ser ignorada. A partir de la versión 0.9.27, las pruebas de peer están soportadas para direcciones IPv6, y la presencia o ausencia de la capacidad 'B' en una dirección IPv6 indica soporte real (o falta de soporte).

**C** : Si la dirección del peer contiene la capacidad 'C', eso significa que están dispuestos y son capaces de servir como introducer a través de esa dirección - sirviendo como un introducer Bob para un Charlie que de otra manera sería inalcanzable. Antes de la versión 0.9.50, los routers Java publicaban incorrectamente la capacidad 'C' para direcciones IPv6, aunque los introducers IPv6 no estaban completamente implementados. Por lo tanto, los routers deberían asumir que las versiones anteriores a la 0.9.50 no pueden actuar como introducer sobre IPv6, incluso si la capacidad 'C' está anunciada.

**4** : A partir de 0.9.50, indica capacidad IPv4 saliente. Si se publica una IP en el campo host, esta capacidad no es necesaria. Si esta es una dirección con introducers para introducciones IPv4, '4' debe incluirse. Si el router está oculto, '4' y '6' pueden combinarse en una sola dirección.

**6** : A partir de la versión 0.9.50, indica capacidad IPv6 saliente. Si se publica una IP en el campo host, esta capacidad no es necesaria. Si esta es una dirección con introducers para introducciones IPv6, se debe incluir '6' (actualmente no compatible). Si el router está oculto, '4' y '6' pueden combinarse en una sola dirección.

# Trabajo Futuro {#future}

Nota: Estos problemas serán abordados en el desarrollo de SSU2.

- El análisis del rendimiento actual de SSU, incluyendo la evaluación del ajuste del tamaño de ventana y otros parámetros, y el ajuste de la implementación del protocolo para mejorar el rendimiento, es un tema para trabajo futuro.

- La implementación actual envía repetidamente confirmaciones para los mismos paquetes,
  lo cual incrementa innecesariamente la sobrecarga.

- El valor MTU pequeño predeterminado de 620 debería ser analizado y posiblemente incrementado.
  La estrategia actual de ajuste de MTU debería ser evaluada.
  ¿Encaja un paquete de biblioteca de streaming de 1730 bytes en 3 paquetes SSU pequeños? Probablemente no.

- El protocolo debería extenderse para intercambiar MTUs durante la configuración.

- El rekeying (regeneración de claves) actualmente no está implementado y nunca lo estará.

- El uso potencial de los campos 'challenge' en RelayIntro y RelayResponse,
  y el uso del campo de relleno en SessionRequest y SessionCreated, no está documentado.

- Un conjunto de tamaños de paquetes fijos puede ser apropiado para ocultar aún más la fragmentación de datos a adversarios externos, pero el relleno de tunnel, garlic y extremo a extremo debería ser suficiente para la mayoría de necesidades hasta entonces.

- Los tiempos de inicio de sesión en SessionCreated y SessionConfirmed parecen no utilizarse o no estar verificados.

# Especificación {#spec}

[Ahora en la página de especificación SSU](/docs/legacy/ssu).
