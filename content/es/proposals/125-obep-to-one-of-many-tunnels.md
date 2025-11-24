---
title: "Entrega OBEP a Túneles 1-de-N o N-de-N"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
---

## Resumen

Esta propuesta cubre dos mejoras para mejorar el rendimiento de la red:

- Delegar la selección de IBGW al OBEP proporcionándole una lista de alternativas en lugar de una sola opción.

- Habilitar el enrutamiento de paquetes multicast en el OBEP.


## Motivación

En el caso de conexión directa, la idea es reducir la congestión de la conexión, dando al OBEP flexibilidad en cómo se conecta a los IBGWs. La capacidad de especificar múltiples túneles también nos permite implementar multicast en el OBEP (entregando el mensaje a todos los túneles especificados).

Una alternativa a la parte de delegación de esta propuesta sería enviar a través de un hash [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset), similar a la capacidad existente de especificar un hash [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification) de destino. Esto resultaría en un mensaje más pequeño y un LeaseSet potencialmente más nuevo. Sin embargo:

1. Forzaría al OBEP a realizar una búsqueda.

2. El LeaseSet puede no estar publicado en un floodfill, por lo que la búsqueda fallaría.

3. El LeaseSet puede estar encriptado, por lo que el OBEP no podría obtener los arrendamientos.

4. Especificar un LeaseSet revela al OBEP el [Destination](/en/docs/specs/common-structures/#destination) del mensaje, lo cual de otro modo solo podrían descubrir rastreando todos los LeaseSets en la red y buscando una coincidencia de Lease.


## Diseño

El originador (OBGW) colocaría algunos (¿todos?) de los [Leases](http://localhost:63465/en/docs/specs/common-structures/#lease) de destino en las instrucciones de entrega [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) en lugar de elegir solo uno.

El OBEP seleccionaría uno de esos para entregar. El OBEP seleccionaría, si estuviera disponible, uno al que ya esté conectado o del que ya tenga conocimiento. Esto haría que la ruta OBEP-IBGW fuera más rápida y confiable, y reduciría las conexiones generales de la red.

Tenemos un tipo de entrega no utilizado (0x03) y dos bits restantes (0 y 1) en las banderas para [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions), que podemos aprovechar para implementar estas características.


## Implicaciones de Seguridad

Esta propuesta no cambia la cantidad de información filtrada sobre el Destino objetivo del OBGW o su vista del NetDB:

- Un adversario que controle el OBEP y esté rastreando LeaseSets desde el NetDB ya puede determinar si se está enviando un mensaje a un Destino particular, buscando el par [TunnelId](http://localhost:63465/en/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification). En el peor de los casos, la presencia de múltiples Leases en el TMDI podría hacer que sea más rápido encontrar una coincidencia en la base de datos del adversario.

- Un adversario que opere un Destino malicioso ya puede obtener información sobre la vista del NetDB de una víctima conectada, publicando LeaseSets conteniendo diferentes túneles de entrada a diferentes floodfills, y observando a través de qué túneles se conecta el OBGW. Desde su punto de vista, el OBEP seleccionando qué túnel usar es funcionalmente idéntico a que el OBGW haga la selección.

La bandera de multicast filtra el hecho de que el OBGW está realizando multicast a los OBEPs. Esto crea una compensación entre rendimiento y privacidad que debe considerarse al implementar protocolos de nivel superior. Siendo una bandera opcional, los usuarios pueden tomar la decisión apropiada para su aplicación. Puede haber beneficios si este fuera el comportamiento predeterminado para aplicaciones compatibles, sin embargo, ya que el uso generalizado por una variedad de aplicaciones reduciría la filtración de información sobre qué aplicación particular proviene un mensaje.


## Especificación

Las Instrucciones de Entrega del Primer Fragmento [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) se modificarían de la siguiente manera:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bits 6-5: delivery type
                 0x03 = TUNNELS
       bit 0: multicast? Si es 0, entregar a uno de los túneles
                        Si es 1, entregar a todos los túneles
                        Establecer a 0 para compatibilidad con usos futuros si
                        el tipo de entrega no es TUNNELS

Count ::
       1 byte
       Opcional, presente si el tipo de entrega es TUNNELS
       2-255 - Número de pares id/hash para seguir

Tunnel ID :: `TunnelId`
To Hash ::
       36 bytes cada uno
       Opcional, presente si el tipo de entrega es TUNNELS
       pares id/hash

Longitud total: La longitud típica es:
       75 bytes para entrega TUNNELS con count 2 (mensaje de túnel no fragmentado);
       79 bytes para entrega TUNNELS con count 2 (primer fragmento)

Resto de las instrucciones de entrega sin cambios
```


## Compatibilidad

Los únicos pares que necesitan entender la nueva especificación son los OBGWs y los OBEPs. Por lo tanto, podemos hacer este cambio compatible con la red existente haciendo que su uso sea condicional en la versión I2P objetivo [VERSIONS](/en/docs/specs/i2np/#protocol-versions):

* Los OBGWs deben seleccionar OBEPs compatibles al construir túneles de salida, basados en la versión I2P anunciada en su [RouterInfo](http://localhost:63465/en/docs/specs/common-structures/#routerinfo).

* Los pares que anuncian la versión objetivo deben soportar el análisis de las nuevas banderas y no deben rechazar las instrucciones como inválidas.

