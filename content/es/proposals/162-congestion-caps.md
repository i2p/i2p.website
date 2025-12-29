---
title: "Límites de Congestión"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Abierto"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Resumen

Añadir indicadores de congestión a la Información del Router (RI) publicada.


## Motivación

Los "límites" de ancho de banda (capacidades) indican límites de ancho de banda compartido y alcanzabilidad, pero no el estado de congestión.
Un indicador de congestión ayudará a los routers a evitar intentar construir a través de un router congestionado,
lo que contribuye a más congestión y reduce el éxito en la construcción de túneles.


## Diseño

Definir nuevas capacidades para indicar varios niveles de congestión o problemas de capacidad.
Estos estarán en las capacidades de nivel superior del RI, no en las capacidades de dirección.


### Definición de Congestión

En general, congestión significa que es poco probable que el par
reciba y acepte una solicitud de construcción de túnel.
Cómo definir o clasificar los niveles de congestión es específico de la implementación.

Las implementaciones pueden considerar uno o más de los siguientes:

- En o cerca de los límites de ancho de banda
- En o cerca del máximo de túneles participantes
- En o cerca del máximo de conexiones en uno o más transportes
- Superado el umbral para la profundidad de cola, latencia o uso de CPU; desbordamiento de cola interna
- Capacidades de CPU y memoria de la plataforma / OS base
- Congestión de red percibida
- Estado de red, como cortafuegos, NAT simétrico, oculto o con proxy
- Configurado para no aceptar túneles

El estado de congestión debe basarse en un promedio de condiciones
durante varios minutos, no en una medición instantánea.


## Especificación

Actualizar [NETDB](/docs/overview/network-database/) como sigue:


```text
D: Congestión media, o un router de bajo rendimiento (por ejemplo Android, Raspberry Pi)
     Otros routers deben degradar o limitar la aparente capacidad de túnel de este router en el perfil.

  E: Alta congestión, este router está cerca o en algún límite,
     y está rechazando o dejando caer la mayoría de las solicitudes de túnel.
     Si este RI fue publicado en los últimos 15 minutos, otros routers
     deben degradar o limitar severamente la capacidad de este router.
     Si este RI es más antiguo que 15 minutos, tratar como 'D'.

  G: Este router está rechazando temporal o permanentemente todos los túneles.
     No intentar construir un túnel a través de este router,
     hasta que se reciba un nuevo RI sin la 'G'.
```

Para consistencia, las implementaciones deben añadir cualquier capacidad de congestión
al final (después de R o U).


## Análisis de Seguridad

No se puede confiar en ninguna información de pares publicada.
Las capacidades, como cualquier otra cosa en la Información del Router, pueden ser falseadas.
Nunca usamos nada en la Información del Router para aumentar la capacidad percibida de un router.

Publicar indicadores de congestión, diciendo a los pares que eviten este router, es inherentemente
mucho más seguro que los indicadores permisivos o de capacidad que solicitan más túneles.

Los indicadores actuales de capacidad de ancho de banda (L-P, X) solo se confían para evitar
routers de muy bajo ancho de banda. La capacidad "U" (inaccesible) tiene un efecto similar.

Cualquier indicador de congestión publicado debería tener el mismo efecto que
rechazar o dejar caer una solicitud de construcción de túnel, con propiedades de seguridad similares.


## Notas

Los pares no deben evitar completamente los routers 'D', solo degradarlos.

Se debe tener cuidado de no evitar completamente los routers 'E',
para que cuando toda la red esté congestionada y publique 'E',
no se rompa completamente.

Los routers pueden usar diferentes estrategias para qué tipos de túneles construir a través de routers 'D' y 'E',
por ejemplo, exploratorio frente a cliente, o túneles de alta frente a baja capacidad de cliente.

Los routers probablemente no deberían publicar una capacidad de congestión al inicio o apagado por defecto,
incluso si su estado de red es desconocido, para prevenir la detección de reinicio por pares.


## Compatibilidad

Sin problemas, todas las implementaciones ignoran capacidades desconocidas.


## Migración

Las implementaciones pueden añadir soporte en cualquier momento, no se necesita coordinación.

Plan preliminar:
Publicar capacidades en 0.9.58 (abril 2023);
actuar sobre capacidades publicadas en 0.9.59 (julio 2023).


## Referencias

* [NETDB](/docs/overview/network-database/)
