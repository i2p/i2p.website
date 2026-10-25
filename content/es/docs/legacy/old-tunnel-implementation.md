---
title: "Implementación de Tunnel Antigua"
description: "Documentación histórica de la implementación original de tunnels de I2P anterior a 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/es/docs/historical/tunnel-alt"
  - "/es/docs/historical/tunnel-alt/"
  - "/es/tunnel"
  - "/es/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Nota: Obsoleto - ¡NO se usa! Reemplazado en 0.6.1.10 - ver [implementación actual](/docs/specs/tunnel-implementation) para la especificación activa.**

## 1) Descripción general de túneles {#tunnel.overview}

Dentro de I2P, los mensajes se pasan en una dirección a través de un túnel virtual de pares, utilizando cualquier medio disponible para pasar el mensaje al siguiente salto. Los mensajes llegan al gateway del túnel, se agrupan para la ruta, y se reenvían al siguiente salto en el túnel, que procesa y verifica la validez del mensaje y lo envía al siguiente salto, y así sucesivamente, hasta que llega al endpoint del túnel. Ese endpoint toma los mensajes agrupados por el gateway y los reenvía según las instrucciones - ya sea a otro router, a otro túnel en otro router, o localmente.

Todos los tunnels funcionan de la misma manera, pero pueden segmentarse en dos grupos diferentes: tunnels de entrada y tunnels de salida. Los tunnels de entrada tienen un gateway no confiable que pasa mensajes hacia abajo hacia el creador del tunnel, que sirve como el punto final del tunnel. Para los tunnels de salida, el creador del tunnel sirve como el gateway, pasando mensajes hacia el punto final remoto.

El creador del tunnel selecciona exactamente qué peers participarán en el tunnel, y proporciona a cada uno los datos de configuración necesarios. Pueden variar en longitud desde 0 saltos (donde el gateway es también el endpoint) hasta 7 saltos (donde hay 6 peers después del gateway y antes del endpoint). La intención es hacer difícil tanto para los participantes como para terceros determinar la longitud de un tunnel, o incluso para participantes que colaboren entre sí determinar si forman parte del mismo tunnel (salvo en la situación donde los peers que colaboran están uno al lado del otro en el tunnel). Los mensajes que han sido corrompidos también se descartan tan pronto como sea posible, reduciendo la carga de la red.

Más allá de su longitud, existen parámetros configurables adicionales para cada tunnel que se pueden usar, como una limitación en el tamaño o frecuencia de los mensajes entregados, cómo se debe usar el relleno, cuánto tiempo debe estar en operación un tunnel, si inyectar mensajes de relleno, si usar fragmentación, y qué estrategias de agrupación, si las hay, se deben emplear.

En la práctica, se utiliza una serie de pools de túneles para diferentes propósitos: cada destino de cliente local tiene su propio conjunto de túneles de entrada y túneles de salida, configurados para satisfacer sus necesidades de anonimato y rendimiento. Además, el router en sí mantiene una serie de pools para participar en la base de datos de red y para gestionar los propios túneles.

I2P es una red inherentemente de conmutación de paquetes, incluso con estos tunnels, lo que le permite aprovechar múltiples tunnels ejecutándose en paralelo, aumentando la resistencia y equilibrando la carga. Fuera de la capa central de I2P, hay una biblioteca de streaming de extremo a extremo opcional disponible para aplicaciones cliente, que expone operación similar a TCP, incluyendo reordenamiento de mensajes, retransmisión, control de congestión, etc.

## 2) Funcionamiento del tunnel {#tunnel.operation}

La operación del tunnel tiene cuatro procesos distintos, llevados a cabo por varios peers en el tunnel. Primero, el gateway del tunnel acumula una cantidad de mensajes del tunnel y los preprocesa en algo para la entrega del tunnel. A continuación, ese gateway cifra esos datos preprocesados, luego los reenvía al primer salto. Ese peer, y los participantes posteriores del tunnel, desenvuelven una capa del cifrado, verificando la integridad del mensaje, luego lo reenvían al siguiente peer. Eventualmente, el mensaje llega al endpoint donde los mensajes agrupados por el gateway se separan nuevamente y se reenvían según se solicite.

Los ID de tunnel son números de 4 bytes utilizados en cada salto - los participantes saben qué ID de tunnel deben escuchar para los mensajes y qué ID de tunnel deben usar para reenviarlos al siguiente salto. Los tunnels en sí tienen una vida corta (10 minutos en este momento), pero dependiendo del propósito del tunnel, y aunque los tunnels posteriores pueden construirse usando la misma secuencia de pares, el ID de tunnel de cada salto cambiará.

### 2.1) Preprocesamiento de mensajes {#tunnel.preprocessing}

Cuando el gateway quiere entregar datos a través del túnel, primero recopila cero o más mensajes I2NP (no más de 32KB en total), selecciona cuánto padding se utilizará, y decide cómo cada mensaje I2NP debe ser manejado por el endpoint del túnel, codificando esos datos en la carga útil cruda del túnel:

- Entero sin signo de 2 bytes que especifica el número de bytes de relleno
- esa cantidad de bytes aleatorios
- una serie de cero o más pares { instrucciones, mensaje }

Las instrucciones están codificadas de la siguiente manera:

- valor de 1 byte:
  ```
  bits 0-1: tipo de entrega
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: ¿retraso incluido?  (1 = verdadero, 0 = falso)
     bit 3: ¿fragmentado?  (1 = verdadero, 0 = falso)
     bit 4: ¿opciones extendidas?  (1 = verdadero, 0 = falso)
  bits 5-7: reservado
  ```
- si el tipo de entrega fue TUNNEL, un ID de tunnel de 4 bytes
- si el tipo de entrega fue TUNNEL o ROUTER, un hash de router de 32 bytes
- si la bandera de retraso incluido es verdadera, un valor de 1 byte:
  ```
     bit 0: tipo (0 = estricto, 1 = aleatorizado)
  bits 1-7: exponente de retraso (2^valor minutos)
  ```
- si la bandera de fragmentado es verdadera, un ID de mensaje de 4 bytes, y un valor de 1 byte:
  ```
  bits 0-6: número de fragmento
     bit 7: ¿es el último?  (1 = verdadero, 0 = falso)
  ```
- si la bandera de opciones extendidas es verdadera:
  ```
  = un tamaño de opción de 1 byte (en bytes)
  = esa cantidad de bytes
  ```
- tamaño de 2 bytes del mensaje I2NP

El mensaje I2NP se codifica en su forma estándar, y la carga útil preprocesada debe rellenarse a un múltiplo de 16 bytes.

### 2.2) Procesamiento del gateway {#tunnel.gateway}

Después del preprocesamiento de los mensajes en una carga útil con relleno, el gateway cifra la carga útil con las ocho claves, construyendo un bloque de suma de verificación para que cada peer pueda verificar la integridad de la carga útil en cualquier momento, así como un bloque de verificación de extremo a extremo para que el endpoint del túnel verifique la integridad del bloque de suma de verificación. Los detalles específicos se presentan a continuación.

El cifrado utilizado es tal que el descifrado simplemente requiere procesar los datos con AES en modo CBC, calcular el SHA256 de una porción fija específica del mensaje (bytes 16 hasta $size-144), y buscar los primeros 16 bytes de ese hash en el bloque de suma de verificación. Hay un número fijo de saltos definido (8 pares) para que podamos verificar el mensaje sin filtrar la posición en el tunnel o hacer que el mensaje "se reduzca" continuamente a medida que se quitan las capas. Para tunnels más cortos de 8 saltos, el creador del tunnel tomará el lugar de los saltos excedentes, descifrando con sus claves (para tunnels de salida, esto se hace al principio, y para tunnels de entrada, al final).

La parte difícil del cifrado es construir ese bloque de suma de verificación entrelazado, lo cual requiere esencialmente descubrir cómo se verá el hash de la carga útil en cada paso, ordenar aleatoriamente esos hashes, y luego construir una matriz de cómo se verá cada uno de esos hashes ordenados aleatoriamente en cada paso. El gateway en sí debe fingir que es uno de los peers dentro del bloque de suma de verificación para que el primer salto no pueda detectar que el salto anterior fue el gateway. Para visualizar esto un poco:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
En lo anterior, P[7] es lo mismo que los datos originales que se pasan a través del tunnel (los mensajes preprocesados), y V[7] son los primeros 16 bytes del SHA256 de eH[0-7] como se ve en peer7 después del descifrado. Para las celdas en la matriz "más arriba" que el hash, su valor se deriva cifrando la celda debajo de ella con la clave para el peer debajo de ella, usando el final de la columna a la izquierda de ella como IV. Para las celdas en la matriz "más abajo" que el hash, son iguales a la celda arriba de ellas, descifradas por la clave del peer actual, usando el final del bloque cifrado anterior en esa fila.

Con esta matriz aleatoria de bloques de suma de verificación, cada peer podrá encontrar el hash de la carga útil, o si no está allí, saber que el mensaje está corrupto. El entrelazado mediante el uso del modo CBC aumenta la dificultad para etiquetar los propios bloques de suma de verificación, pero aún es posible que ese etiquetado pase brevemente desapercibido si las columnas después de los datos etiquetados ya han sido utilizadas para verificar la carga útil en un peer. En cualquier caso, el extremo del tunnel (peer 7) sabe con certeza si alguno de los bloques de suma de verificación ha sido etiquetado, ya que eso corrompería el bloque de verificación (V[7]).

El IV[0] es un valor aleatorio de 16 bytes, e IV[i] son los primeros 16 bytes de H(D(IV[i-1], K[i-1]) xor IV_WHITENER). No usamos el mismo IV a lo largo de la ruta, ya que eso permitiría colusión trivial, y usamos el hash del valor descifrado para propagar el IV con el fin de dificultar la filtración de claves. IV_WHITENER es un valor fijo de 16 bytes.

Cuando el gateway quiere enviar el mensaje, exporta la fila correcta para el peer que es el primer salto (generalmente la fila peer1.recv) y la reenvía completamente.

### 2.3) Procesamiento del participante {#tunnel.participant}

Cuando un participante en un tunnel recibe un mensaje, descifra una capa con su clave de tunnel usando AES256 en modo CBC con los primeros 16 bytes como IV. Luego calcula el hash de lo que ve como la carga útil (bytes 16 hasta $size-144) y busca esos primeros 16 bytes de ese hash dentro del bloque de suma de verificación descifrado. Si no se encuentra coincidencia, el mensaje se descarta. De lo contrario, el IV se actualiza descifrándolo, aplicando XOR a ese valor con el IV_WHITENER, y reemplazándolo con los primeros 16 bytes de su hash. El mensaje resultante se reenvía entonces al siguiente par para su procesamiento.

Para prevenir ataques de repetición a nivel de túnel, cada participante mantiene un registro de los IVs recibidos durante la vida útil del túnel, rechazando los duplicados. El uso de memoria requerido debería ser mínimo, ya que cada túnel tiene solo una vida útil muy corta (10 minutos en este momento). Un flujo constante de 100KBps a través de un túnel con mensajes completos de 32KB daría 1875 mensajes, requiriendo menos de 30KB de memoria. Los gateways y endpoints manejan la repetición rastreando los IDs de mensaje y las expiraciones en los mensajes I2NP contenidos en el túnel.

### 2.4) Procesamiento de punto final {#tunnel.endpoint}

Cuando un mensaje llega al punto final del tunnel, lo descifra y verifica como un participante normal. Si el bloque de suma de verificación tiene una coincidencia válida, el punto final entonces calcula el hash del bloque de suma de verificación en sí mismo (como se ve después del descifrado) y lo compara con el hash de verificación descifrado (los últimos 16 bytes). Si ese hash de verificación no coincide, el punto final toma nota del intento de marcado por parte de uno de los participantes del tunnel y posiblemente descarta el mensaje.

En este punto, el extremo del tunnel tiene los datos preprocesados enviados por el gateway, los cuales puede entonces analizar para extraer los mensajes I2NP incluidos y reenviarlos según se solicite en sus instrucciones de entrega.

### 2.5) Relleno {#tunnel.padding}

Son posibles varias estrategias de relleno de túnel, cada una con sus propios méritos:

- Sin relleno
- Relleno a un tamaño aleatorio
- Relleno a un tamaño fijo
- Relleno al KB más cercano
- Relleno al tamaño exponencial más cercano (2^n bytes)

*¿Cuál usar? sin relleno es lo más eficiente, el relleno aleatorio es lo que tenemos ahora, el tamaño fijo sería un desperdicio extremo o nos obligaría a implementar fragmentación. Rellenar al tamaño exponencial más cercano (como Freenet) parece prometedor. ¿Tal vez deberíamos recopilar algunas estadísticas en la red sobre qué tamaños de mensajes hay, y luego ver qué costos y beneficios surgirían de diferentes estrategias?*

### 2.6) Fragmentación de túnel {#tunnel.fragmentation}

Para varios esquemas de relleno y mezcla, puede ser útil desde una perspectiva de anonimato fragmentar un solo mensaje I2NP en múltiples partes, cada una entregada por separado a través de diferentes mensajes de tunnel. El punto final puede o no soportar esa fragmentación (descartando o conservando fragmentos según sea necesario), y el manejo de fragmentación no se implementará inmediatamente.

### 2.7) Alternativas {#tunnel.alternatives}

#### 2.7.1) No usar un bloque de suma de verificación {#tunnel.nochecksum}

Una alternativa al proceso anterior es eliminar completamente el bloque de suma de verificación y reemplazar el hash de verificación con un hash simple de la carga útil. Esto simplificaría el procesamiento en la puerta de enlace del tunnel y ahorraría 144 bytes de ancho de banda en cada salto. Por otro lado, los atacantes dentro del tunnel podrían ajustar trivialmente el tamaño del mensaje a uno que sea fácilmente rastreable por observadores externos coludidos además de los participantes posteriores del tunnel. La corrupción también incurriría en el desperdicio de todo el ancho de banda necesario para transmitir el mensaje. Sin la validación por salto, también sería posible consumir recursos de red excesivos construyendo tunnels extremadamente largos, o construyendo bucles en el tunnel.

#### 2.7.2) Ajustar el procesamiento de tunnel a mitad de flujo {#tunnel.reroute}

Aunque el algoritmo simple de enrutamiento de túneles debería ser suficiente para la mayoría de los casos, existen tres alternativas que se pueden explorar:

- Retrasar un mensaje dentro de un tunnel en un salto arbitrario durante un período de tiempo específico o aleatorio. Esto se podría lograr reemplazando el hash en el bloque de suma de verificación con, por ejemplo, los primeros 8 bytes del hash, seguidos de algunas instrucciones de retraso. Alternativamente, las instrucciones podrían indicar al participante que interprete realmente la carga útil sin procesar tal como está, y que descarte el mensaje o continúe reenviándolo por la ruta (donde sería interpretado por el endpoint como un mensaje chaff). La última parte de esto requeriría que el gateway ajuste su algoritmo de cifrado para producir la carga útil en texto claro en un salto diferente, pero no debería ser mucho problema.

- Permitir que los routers que participan en un tunnel remezclen el mensaje antes
  de reenviarlo - rebotándolo a través de uno de los tunnels salientes propios de ese
  peer, llevando instrucciones para la entrega al siguiente salto. Esto podría usarse
  de manera controlada (con instrucciones en ruta como los retrasos mencionados arriba)
  o de forma probabilística.

- Implementar código para que el creador del tunnel redefina el "siguiente salto" de un peer en el tunnel, permitiendo mayor redirección dinámica.

#### 2.7.3) Usar túneles bidireccionales {#tunnel.bidirectional}

La estrategia actual de usar dos túneles separados para la comunicación entrante y saliente no es la única técnica disponible, y sí tiene implicaciones para el anonimato. En el lado positivo, al usar túneles separados se reduce la exposición de datos de tráfico para análisis a los participantes en un túnel - por ejemplo, los peers en un túnel saliente desde un navegador web solo verían el tráfico de una petición HTTP GET, mientras que los peers en un túnel entrante verían la carga útil entregada a lo largo del túnel. Con túneles bidireccionales, todos los participantes tendrían acceso al hecho de que, por ejemplo, se enviaron 1KB en una dirección, luego 100KB en la otra. En el lado negativo, usar túneles unidireccionales significa que hay dos conjuntos de peers que necesitan ser perfilados y contabilizados, y se debe tener cuidado adicional para abordar la velocidad incrementada de los ataques de predecesor. El proceso de agrupación y construcción de túneles descrito a continuación debería minimizar las preocupaciones del ataque de predecesor, aunque si se deseara, no sería mucho problema construir tanto los túneles entrantes como los salientes a lo largo de los mismos peers.

#### 2.7.4) Usar un tamaño de bloque más pequeño {#tunnel.smallerhashes}

En este momento, nuestro uso de AES limita nuestro tamaño de bloque a 16 bytes, lo que a su vez proporciona el tamaño mínimo para cada una de las columnas de bloque de suma de verificación. Si se usara otro algoritmo con un tamaño de bloque más pequeño, o pudiera permitir de otra manera la construcción segura del bloque de suma de verificación con porciones más pequeñas del hash, podría valer la pena explorarlo. Los 16 bytes usados ahora en cada salto deberían ser más que suficientes.

## 3) Construcción de tunnel {#tunnel.building}

Al construir un tunnel, el creador debe enviar una solicitud con los datos de configuración necesarios a cada uno de los saltos, luego esperar a que el participante potencial responda indicando si está de acuerdo o no. Estos mensajes de solicitud de tunnel y sus respuestas están envueltos con garlic encryption para que solo el router que conoce la clave pueda descifrarlos, y la ruta tomada en ambas direcciones también es enrutada por tunnel. Hay tres dimensiones importantes a tener en cuenta al producir los tunnels: qué peers se utilizan (y dónde), cómo se envían las solicitudes (y se reciben las respuestas), y cómo se mantienen.

### 3.1) Selección de peers {#tunnel.peerselection}

Más allá de los dos tipos de túneles - entrantes y salientes - hay dos estilos de selección de pares utilizados para diferentes túneles - exploratorios y de cliente. Los túneles exploratorios se utilizan tanto para el mantenimiento de la base de datos de red como para el mantenimiento de túneles, mientras que los túneles de cliente se utilizan para mensajes de cliente de extremo a extremo.

#### 3.1.1) Selección de pares para túneles exploratorios {#tunnel.selection.exploratory}

Los túneles exploratorios se construyen a partir de una selección aleatoria de pares de un subconjunto de la red. El subconjunto particular varía según el router local y sus necesidades de enrutamiento de túneles. En general, los túneles exploratorios se construyen a partir de pares seleccionados aleatoriamente que están en la categoría de perfil "no fallando pero activo" del par. El propósito secundario de los túneles, más allá del mero enrutamiento de túneles, es encontrar pares de alta capacidad subutilizados para que puedan ser promovidos para uso en túneles de cliente.

#### 3.1.2) Selección de pares para túneles de cliente {#tunnel.selection.client}

Los túneles de cliente se construyen con un conjunto más estricto de requisitos: el router local seleccionará pares de su categoría de perfil de "alta velocidad y alta capacidad" para que el rendimiento y la confiabilidad satisfagan las necesidades de la aplicación cliente. Sin embargo, hay varios detalles importantes más allá de esa selección básica que deben respetarse, dependiendo de las necesidades de anonimato del cliente.

Para algunos clientes que están preocupados por adversarios que monten un ataque de predecesor, la selección de tunnel puede mantener los peers seleccionados en un orden estricto - si A, B, y C están en un tunnel, el salto después de A es siempre B, y el salto después de B es siempre C. Un ordenamiento menos estricto también es posible, asegurando que mientras el salto después de A puede ser B, B nunca puede estar antes de A. Otras opciones de configuración incluyen la capacidad de que solo los gateways de tunnel entrantes y los endpoints de tunnel salientes sean fijos, o rotados a una tasa MTBF.

### 3.2) Entrega de solicitud {#tunnel.request}

Como se mencionó anteriormente, una vez que el creador del tunnel sabe qué peers deben formar parte del tunnel y en qué orden, el creador construye una serie de mensajes de solicitud de tunnel, cada uno conteniendo la información necesaria para ese peer. Por ejemplo, a los tunnels participantes se les proporcionará el ID de tunnel de 4 bytes en el cual deben recibir mensajes, el ID de tunnel de 4 bytes en el cual deben enviar los mensajes, el hash de 32 bytes de la identidad del siguiente salto, y la clave de capa de 32 bytes utilizada para eliminar una capa del tunnel. Por supuesto, a los endpoints de tunnel de salida no se les proporciona información del "siguiente salto" o "siguiente ID de tunnel". Sin embargo, a los gateways de tunnel de entrada se les proporcionan las 8 claves de capa en el orden en que deben ser cifradas (como se describió anteriormente). Para permitir respuestas, la solicitud contiene una etiqueta de sesión aleatoria y una clave de sesión aleatoria con la cual el peer puede cifrar con garlic encryption su decisión, así como el tunnel al cual ese garlic debe ser enviado. Además de la información anterior, se pueden incluir varias opciones específicas del cliente, como qué limitación aplicar al tunnel, qué estrategias de relleno o agrupamiento usar, etc.

Después de construir todos los mensajes de solicitud, son envueltos con garlic encryption para el router de destino y enviados a través de un túnel exploratorio. Al recibirlos, ese par determina si puede o va a participar, creando un mensaje de respuesta y tanto envolviendo con garlic encryption como enrutando por túnel la respuesta con la información suministrada. Al recibir la respuesta en el creador del túnel, el túnel se considera válido en ese salto (si es aceptado). Una vez que todos los pares han aceptado, el túnel está activo.

### 3.3) Agrupación {#tunnel.pooling}

Para permitir un funcionamiento eficiente, el router mantiene una serie de pools de túneles, cada uno gestionando un grupo de túneles utilizados para un propósito específico con su propia configuración. Cuando se necesita un túnel para ese propósito, el router selecciona uno del pool apropiado al azar. En general, hay dos pools de túneles exploratorios - uno de entrada y uno de salida - cada uno usando los valores predeterminados de exploración del router. Además, hay un par de pools para cada destino local - un túnel de entrada y uno de salida. Esos pools usan la configuración especificada cuando el destino local se conectó al router, o los valores predeterminados del router si no se especificó.

Cada pool tiene dentro de su configuración algunas opciones clave, que definen cuántos tunnels mantener activos, cuántos tunnels de respaldo mantener en caso de fallo, con qué frecuencia probar los tunnels, qué tan largos deberían ser los tunnels, si esas longitudes deberían ser aleatorias, con qué frecuencia se deberían construir tunnels de reemplazo, así como cualquiera de las otras configuraciones permitidas al configurar tunnels individuales.

### 3.4) Alternativas {#tunnel.building.alternatives}

#### 3.4.1) Construcción telescópica {#tunnel.building.telescoping}

Una pregunta que puede surgir con respecto al uso de los tunnels exploratorios para enviar y recibir mensajes de creación de tunnel es cómo esto impacta la vulnerabilidad del tunnel a ataques de predecesor. Mientras que los endpoints y gateways de esos tunnels estarán distribuidos aleatoriamente a través de la red (tal vez incluso incluyendo al creador del tunnel en ese conjunto), otra alternativa es usar las rutas del tunnel en sí mismas para pasar la solicitud y respuesta, como se hace en [TOR](https://www.torproject.org/). Esto, sin embargo, puede llevar a filtraciones durante la creación del tunnel, permitiendo que los peers descubran cuántos saltos hay más adelante en el tunnel monitoreando el tiempo o el conteo de paquetes mientras se construye el tunnel. Se podrían usar técnicas para minimizar este problema, como usar cada uno de los saltos como endpoints (según [2.7.2](#tunnel.reroute)) para un número aleatorio de mensajes antes de continuar construyendo el siguiente salto.

#### 3.4.2) Túneles no exploratorios para gestión {#tunnel.building.nonexploratory}

Una segunda alternativa al proceso de construcción de túneles es proporcionar al router un conjunto adicional de pools de entrada y salida no exploratorios, utilizándolos para la solicitud y respuesta del túnel. Asumiendo que el router tiene una vista bien integrada de la red, esto no debería ser necesario, pero si el router estuviera particionado de alguna manera, usar pools no exploratorios para la gestión de túneles reduciría la filtración de información sobre qué peers están en la partición del router.

## 4) Limitación de túneles {#tunnel.throttling}

Aunque los tunnels dentro de I2P se asemejan a una red de conmutación de circuitos, todo dentro de I2P se basa estrictamente en mensajes - los tunnels son simplemente trucos contables para ayudar a organizar la entrega de mensajes. No se hacen suposiciones respecto a la confiabilidad u ordenamiento de los mensajes, y las retransmisiones se dejan a niveles superiores (por ejemplo, la biblioteca de streaming de la capa cliente de I2P). Esto permite a I2P aprovechar las técnicas de throttling (limitación de velocidad) disponibles tanto para redes de conmutación de paquetes como de conmutación de circuitos. Por ejemplo, cada router puede llevar un registro del promedio móvil de cuántos datos está usando cada tunnel, combinarlo con todos los promedios utilizados por otros tunnels en los que el router está participando, y ser capaz de aceptar o rechazar solicitudes adicionales de participación en tunnels basándose en su capacidad y utilización. Por otro lado, cada router puede simplemente descartar mensajes que están más allá de su capacidad, aprovechando la investigación utilizada en el Internet normal.

## 5) Mezclado/agrupamiento {#tunnel.mixing}

¿Qué estrategias deberían usarse en el gateway y en cada hop para retrasar, reordenar, reredirigir o rellenar mensajes? ¿Hasta qué punto debería hacerse esto automáticamente, cuánto debería configurarse como una configuración por tunnel o por hop, y cómo debería el creador del tunnel (y a su vez, el usuario) controlar esta operación? Todo esto queda como desconocido, para ser resuelto en una futura versión.
