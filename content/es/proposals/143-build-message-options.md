---
title: "Opciones del Mensaje de Construcción de Túnel"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Rechazado"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Nota
Esta propuesta no fue implementada como se especificó,
sin embargo, los mensajes de construcción largos y cortos de ECIES (propuestas 152 y 157)
fueron diseñados con campos de opciones extensibles.
Véase la [especificación de Tunnel Creation ECIES](/docs/specs/implementation/#tunnel-creation-ecies) para la especificación oficial.


## Resumen

Añadir un mecanismo flexible y extensible para opciones en los Registros de Construcción de Túnel I2NP
que están contenidos en los mensajes de Construcción de Túnel y Respuesta de Construcción de Túnel.


## Motivación

Existen algunas propuestas tentativas y no documentadas que están próximas a establecer opciones o configuraciones en el Mensaje de Construcción de Túnel,
para que el creador del túnel pueda pasar algunos parámetros a cada salto del túnel.

Hay 29 bytes libres en el TBM. Queremos mantener la flexibilidad para futuras mejoras, pero también usar el espacio sabiamente.
Usar la construcción 'mapping' consumiría al menos 6 bytes por opción ("1a=1b;").
Definir más campos de opción de manera rígida podría causar problemas más adelante.

Este documento propone un nuevo esquema de mapeo de opciones, flexible.


## Diseño

Necesitamos una representación de opción que sea compacta y al mismo tiempo flexible, para que podamos ajustar múltiples
opciones, de longitud variable, en 29 bytes.
Estas opciones aún no están definidas, y no es necesario que lo estén en este momento.
No uses la estructura "mapping" (que codifica un objeto de propiedades Java), es demasiado derrochadora.
Usa un número para indicar cada opción y longitud, resultando en una codificación compacta pero flexible.
Las opciones deben registrarse por número en nuestras especificaciones, pero también reservaremos un rango para opciones experimentales.


## Especificación

Preliminar - se describen varias alternativas a continuación.

Esto estaría presente solo si el bit 5 en las banderas (byte 184) está configurado en 1.

Cada opción es un número de opción de dos bytes y longitud, seguido de los bytes de valor de opción de longitud.

Las opciones comienzan en el byte 193 y continúan a través del último byte 221 como máximo.

Número de opción/longitud:

Dos bytes. Bits 15-4 son el número de opción de 12 bits, 1 - 4095.
Bits 3-0 son el número de bytes de valor de la opción a seguir, 0 - 15.
Una opción booleana podría tener cero bytes de valor.
Mantendremos un registro de números de opción en nuestras especificaciones, y también definiremos un rango para opciones experimentales.

El valor de la opción es de 0 a 15 bytes, para ser interpretado por quien necesite esa opción. Los números de opción desconocidos deben ser ignorados.

Las opciones concluyen con un número de opción/longitud de 0/0, es decir, dos bytes 0.
El resto de los 29 bytes, si los hay, debe llenarse con relleno aleatorio, como es habitual.

Esta codificación nos da espacio para 14 opciones de 0 bytes, o 9 opciones de 1 byte, o 7 opciones de 2 bytes.
Una alternativa sería usar solo un byte para el número de opción/longitud,
quizás con 5 bits para el número de opción (máximo 32) y 3 bits para la longitud (máximo 7).
Esto aumentaría la capacidad a 28 opciones de 0 bytes, 14 opciones de 1 byte, o 9 opciones de dos bytes.
También podríamos hacerlo variable, donde un número de opción de 5 bits de 31 significa leer 8 bits más para el número de opción.

Si el salto del túnel necesita devolver opciones al creador, podemos usar el mismo formato en el mensaje de respuesta de construcción de túnel,
prefijado por algún número mágico de varios bytes (ya que no tenemos un byte de bandera definido para indicar que las opciones están presentes).
Hay 495 bytes libres en el TBRM.


## Notas

Estos cambios son para los Registros de Construcción de Túnel, y por lo tanto pueden usarse en todas las variantes de Mensajes de Construcción -
Solicitud de Construcción de Túnel, Solicitud de Construcción de Túnel Variable, Respuesta de Construcción de Túnel, y Respuesta de Construcción de Túnel Variable.


## Migración

El espacio no utilizado en los Registros de Construcción de Túnel se llena con datos aleatorios y actualmente se ignora.
El espacio puede convertirse para contener opciones sin problemas de migración.
En el mensaje de construcción, la presencia de opciones se indica en el byte de banderas.
En el mensaje de respuesta de construcción, la presencia de opciones se indica mediante un número mágico de varios bytes.
