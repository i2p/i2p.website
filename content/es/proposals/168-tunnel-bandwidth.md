---
title: "Parámetros de Ancho de Banda de Túnel"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Cerrado"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## NOTA

Esta propuesta fue aprobada y ahora está en la
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) desde la API 0.9.65.
Todavía no hay implementaciones conocidas; las fechas de implementación / versiones de la API están por determinar.


## Visión General

A medida que hemos aumentado el rendimiento de la red en los últimos años
con nuevos protocolos, tipos de encriptación y mejoras en el control de congestión,
las aplicaciones más rápidas como la transmisión de video se están volviendo posibles.
Estas aplicaciones requieren un alto ancho de banda en cada salto en sus túneles cliente.

Sin embargo, los routers participantes no tienen ninguna información sobre cuánto
ancho de banda utilizará un túnel cuando reciben un mensaje de construcción de túnel.
Solo pueden aceptar o rechazar un túnel en función del ancho de banda total actual
utilizado por todos los túneles participantes y el límite total de ancho de banda para túneles participantes.

Los routers solicitantes tampoco tienen ninguna información sobre cuánto ancho de banda
está disponible en cada salto.

Además, actualmente los routers no tienen forma de limitar el tráfico entrante en un túnel.
Esto sería muy útil durante momentos de sobrecarga o DDoS de un servicio.

Esta propuesta aborda estos problemas añadiendo parámetros de ancho de banda
a los mensajes de solicitud y respuesta de construcción de túnel.


## Diseño

Añadir parámetros de ancho de banda a los registros en mensajes de construcción de túnel ECIES (ver [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies))
en el campo de mapeo de opciones de construcción de túnel. Utilizar nombres de parámetros cortos ya que el espacio disponible
para el campo de opciones es limitado.
Los mensajes de construcción de túnel son de tamaño fijo por lo que esto no aumenta el
tamaño de los mensajes.


## Especificación

Actualizar la [especificación de mensajes de construcción de túnel ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
como sigue:

Para ambos registros de construcción ECIES largos y cortos:

### Opciones de Solicitud de Construcción

Las siguientes tres opciones pueden establecerse en el campo de mapeo de opciones de construcción de túnel del registro:
Un router solicitante puede incluir cualquiera, todas, o ninguna.

- m := ancho de banda mínimo requerido para este túnel (entero positivo en KBps como cadena)
- r := ancho de banda solicitado para este túnel (entero positivo en KBps como cadena)
- l := límite de ancho de banda para este túnel; solo enviado a IBGW (entero positivo en KBps como cadena)

Restricción: m <= r <= l

El router participante debería rechazar el túnel si se especifica "m" y no puede
proveer al menos esa cantidad de ancho de banda.

Las opciones de solicitud se envían a cada participante en el registro de solicitud de construcción cifrado correspondiente,
y no son visibles para otros participantes.


### Opción de Respuesta de Construcción

La siguiente opción puede establecerse en el campo de mapeo de opciones de respuesta de construcción del registro,
cuando la respuesta es ACEPTADA:

- b := ancho de banda disponible para este túnel (entero positivo en KBps como cadena)

El router participante debería incluir esto si se especificó "m" o "r"
en la solicitud de construcción. El valor debería ser al menos el del valor "m" si está especificado,
pero puede ser menor o mayor que el valor "r" si está especificado.

El router participante debería intentar reservar y proporcionar al menos esta
cantidad de ancho de banda para el túnel, sin embargo esto no está garantizado.
Los routers no pueden predecir condiciones 10 minutos en el futuro, y
el tráfico participante tiene menor prioridad que el propio tráfico de un router y sus túneles.

Los routers también pueden sobre-allocar el ancho de banda disponible si es necesario, y esto es
probablemente deseable, ya que otros saltos en el túnel podrían rechazarlo.

Por estas razones, la respuesta del router participante debería tratarse
como un compromiso de mejor esfuerzo, pero no como una garantía.

Las opciones de respuesta se envían al router solicitante en el registro de respuesta de construcción cifrado correspondiente,
y no son visibles para otros participantes.


## Notas de Implementación

Los parámetros de ancho de banda se ven en los routers participantes en la capa del túnel,
es decir, el número de mensajes de túnel de tamaño fijo de 1 KB por segundo.
El overhead de transporte (NTCP2 o SSU2) no está incluido.

Este ancho de banda puede ser mucho más o menos que el ancho de banda visto en el cliente.
Los mensajes de túnel contienen un overhead sustancial, incluyendo overhead de capas superiores
incluyendo ráfaga y streaming. Los mensajes pequeños intermitentes como las confirmaciones de streaming
se expandirán a 1 KB cada uno.
Sin embargo, la compresión gzip en la capa I2CP puede reducir sustancialmente el ancho de banda.

La implementación más simple en el router solicitante es utilizar
los anchos de banda promedio, mínimo, y/o máximo de los túneles actuales en el grupo
para calcular los valores a poner en la solicitud.
Algoritmos más complejos son posibles y quedan a discreción del implementador.

No hay opciones I2CP o SAM actuales definidas para que el cliente le diga al
router qué ancho de banda se requiere, y no se proponen nuevas opciones aquí.
Las opciones pueden definirse en una fecha posterior si es necesario.

Las implementaciones pueden usar el ancho de banda disponible u otros datos, algoritmos, política local,
o configuración local para calcular el valor de ancho de banda devuelto en la
respuesta de construcción. No está especificado por esta propuesta.

Esta propuesta requiere que las puertas de enlace entrantes implementen la limitación por túnel
si se solicita mediante la opción "l".
No requiere que otros saltos participantes implementen limitación por túnel o global
de ningún tipo, ni especifica un algoritmo o implementación en particular, si alguna.

Esta propuesta tampoco requiere que los routers clientes limiten el tráfico
al valor "b" devuelto por el salto participante, y dependiendo de la aplicación,
eso puede no ser posible, particularmente para los túneles entrantes.

Esta propuesta solo afecta a los túneles creados por el originador. No hay
método definido para solicitar o asignar ancho de banda para túneles "del otro extremo" creados
por el propietario del otro extremo de una conexión de extremo a extremo.


## Análisis de Seguridad

El fingerprinting o correlación del cliente puede ser posible en función de las solicitudes.
El router cliente (originador) puede desear aleatorizar los valores "m" y "r" en lugar de enviar
el mismo valor a cada salto; o enviar un conjunto limitado de valores que representen "cubetas" de ancho de banda,
o alguna combinación de ambos.

DDoS por sobre-asignación: Aunque puede ser posible realizar un DDoS a un router ahora al construir y
usar un gran número de túneles a través de él, esta propuesta posiblemente lo hace mucho más fácil,
simplemente solicitando uno o más túneles con solicitudes de ancho de banda grandes.

Las implementaciones pueden y deben usar una o más de las siguientes estrategias
para mitigar este riesgo:

- Sobre-asignación del ancho de banda disponible
- Limitar la asignación por túnel a algún porcentaje del ancho de banda disponible
- Limitar la tasa de aumento en el ancho de banda asignado
- Limitar la tasa de aumento en el ancho de banda usado
- Limitar el ancho de banda asignado para un túnel si no se usa al inicio de la vida útil del túnel (úsalo o piérdelo)
- Seguimiento del ancho de banda promedio por túnel
- Seguimiento del ancho de banda solicitado vs. el ancho de banda real usado por túnel


## Compatibilidad

No hay problemas. Todas las implementaciones conocidas actualmente ignoran el campo de mapeo en los mensajes de construcción,
y omiten correctamente un campo de opciones no vacío.


## Migración

Las implementaciones pueden añadir soporte en cualquier momento, no se necesita coordinación.

Como actualmente no hay una versión de la API definida donde se requiera el soporte para esta propuesta,
los routers deben verificar una respuesta "b" para confirmar el soporte.


