---
title: "Túneles Bidireccionales"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Necesita-Investigación"
thread: "http://zzz.i2p/topics/2041"
---

## Descripción General

Esta propuesta trata sobre la implementación de túneles bidireccionales en I2P.

## Motivación

i2pd va a introducir túneles bidireccionales construidos a través de otros enrutadores i2pd solo por ahora. Para la red aparecerán como túneles regulares de entrada y salida.

## Diseño

### Objetivos

1. Reducir el uso de red y CPU al disminuir el número de mensajes TunnelBuild.
2. Capacidad para saber instantáneamente si un participante se ha ido.
3. Perfilado y estadísticas más precisos.
4. Usar otras darknets como pares intermedios.

### Modificaciones al Túnel

TunnelBuild
```````````
Los túneles se construyen de la misma manera que los túneles de entrada. No se requiere un mensaje de respuesta. Hay un tipo especial de participante llamado "entrada" marcado por una bandera, que sirve como IBGW y OBEP al mismo tiempo. El mensaje tiene el mismo formato que VaribaleTunnelBuild pero ClearText contiene diferentes campos::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

También contendrá un campo mencionando a qué darknet pertenece el siguiente par y alguna información adicional si no es I2P.

TunnelTermination
``````````````````
Si un par desea irse, crea mensajes TunnelTermination que cifra con la clave de capa y envía en dirección "de entrada". Si un participante recibe dicho mensaje, lo cifra con su clave de capa y lo envía al siguiente par. Una vez que un mensaje llega al propietario del túnel, comienza a descifrarlo par a par hasta que obtiene un mensaje sin cifrar. Descubre qué par se ha ido y termina el túnel.
