---
title: "Coincidir OBEPs con IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Resumen

Esta propuesta añade una opción I2CP para túneles de salida que hace que los túneles se seleccionen o construyan cuando se envía un mensaje de manera que el OBEP coincida con uno de los IBGWs del LeaseSet para el Destination objetivo.


## Motivación

La mayoría de los routers I2P emplean una forma de eliminación de paquetes para la gestión de la congestión. La implementación de referencia utiliza una estrategia WRED que toma en cuenta tanto el tamaño del mensaje como la distancia de viaje (véase [documentación de tunnel throttling](/docs/specs/implementation/#tunnelthrottling)). Debido a esta estrategia, la principal fuente de pérdida de paquetes es el OBEP.


## Diseño

Al enviar un mensaje, el remitente selecciona o construye un túnel con un OBEP que sea el mismo router que uno de los IBGWs del destinatario. Al hacerlo, el mensaje saldrá directamente de un túnel y entrará en el otro, sin necesidad de ser enviado a través del cable entre ellos.


## Implicaciones de seguridad

Este modo efectivamente significaría que el destinatario está seleccionando el OBEP del remitente. Para mantener la privacidad actual, este modo haría que los túneles de salida se construyan un salto más largo que lo especificado por la opción outbound.length de I2CP (con el salto final posiblemente estando fuera del nivel rápido del remitente).


## Especificación

Se añade una nueva opción I2CP a la [especificación I2CP](/docs/specs/i2cp/):

    outbound.matchEndWithTarget
        Booleano

        Valor por defecto: específico del caso

        Si es verdadero, el router seleccionará túneles de salida para mensajes enviados durante
        esta sesión de manera que el OBEP del túnel sea uno de los IBGWs para el
        Destination objetivo. Si no existe tal túnel, el router construirá uno.


## Compatibilidad

La compatibilidad con versiones anteriores está asegurada, ya que los routers siempre pueden enviar mensajes a sí mismos.


## Implementación

### Java I2P

La construcción de túneles y el envío de mensajes son actualmente subsistemas separados:

- BuildExecutor solo conoce las opciones outbound.* del grupo de túneles de salida,
  y no tiene visibilidad sobre su uso.

- OutboundClientMessageOneShotJob solo puede seleccionar un túnel del grupo existente;
  si entra un mensaje de cliente y no hay túneles de salida, el router descarta el mensaje.

Implementar esta propuesta requeriría diseñar una forma para que estos dos subsistemas interactúen.

### i2pd

Se ha completado una implementación de prueba.


## Rendimiento

Esta propuesta tiene varios efectos sobre la latencia, RTT y pérdida de paquetes:

- Es probable que en la mayoría de los casos, este modo requiera construir un nuevo túnel
  en el primer mensaje en lugar de usar un túnel existente, añadiendo latencia.

- Para túneles estándar, el OBEP puede necesitar encontrar y conectarse al IBGW,
  añadiendo latencia que incrementa el primer RTT (ya que esto ocurre después de que se haya enviado el primer paquete). Usando este modo, el OBEP necesitaría encontrar y conectarse al IBGW durante la construcción del túnel, añadiendo la misma latencia pero reduciendo el primer RTT (ya que esto ocurre antes de que se haya enviado el primer paquete).

- El tamaño actualmente estándar VariableTunnelBuild es de 2641 bytes. Por lo tanto, se espera que este modo resulte en una menor pérdida de paquetes para tamaños de mensaje promedio mayores que este.

Se necesita más investigación para investigar estos efectos, con el fin de decidir qué túneles estándar se beneficiarían de tener este modo habilitado por defecto.
