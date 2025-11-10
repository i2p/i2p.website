---
title: "Notas de estado de I2P del 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Actualización semanal del estado de I2P que abarca el rendimiento de la versión 0.3.4.1, el equilibrio de carga del outproxy (proxy de salida) y las actualizaciones de la documentación"
categories: ["status"]
---

¡Hola a todos, hora de la actualización semanal!

## Índice:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 estado

Bueno, lanzamos la versión 0.3.4.1 el otro día y ha estado funcionando bastante bien. Los tiempos de conexión en irc se han mantenido de forma consistente durante varias horas, y las tasas de transferencia también van bastante bien (obtuve 25KBps de un eepsite(sitio de I2P) el otro día usando 3 flujos paralelos).

Una característica muy interesante añadida en la versión 0.3.4.1 (que olvidé incluir en el anuncio de la versión) fue el parche de mule que permite al eepproxy distribuir en modo round-robin las solicitudes no I2P a través de una serie de outproxies (proxies de salida). El valor predeterminado sigue siendo usar únicamente el outproxy squid.i2p, pero si vas a tu router.config y cambias la línea clientApp para que tenga:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
enrutará aleatoriamente cada solicitud HTTP a través de uno de los dos outproxies (proxies de salida) listados (squid.i2p y www1.squid.i2p). Con eso, si hay algunas personas más operando outproxies, ustedes no dependerán tanto de squid.i2p. Por supuesto, todos han oído mis preocupaciones respecto a los outproxies, pero contar con esta capacidad le da a la gente más opciones.

Hemos estado viendo algo de inestabilidad en las últimas horas, pero con la ayuda de duck y cervantes he identificado dos errores graves y estoy probando correcciones ahora mismo. Las correcciones son significativas, así que espero tener disponible la 0.3.4.2 en uno o dos días, después de verificar los resultados.

## 2) Documentación actualizada

Hemos estado descuidando un poco mantener la documentación del sitio actualizada y, aunque aún hay algunos huecos importantes (p. ej., la documentación de netDb e i2ptunnel), recientemente hemos actualizado algunas (las comparativas de redes y la sección de Preguntas frecuentes (FAQ)). A medida que nos acercamos a las versiones 0.4 y 1.0, agradecería que la gente pudiera revisar el sitio y ver qué se puede mejorar.

Cabe destacar un Salón de la Fama actualizado - por fin lo hemos puesto al día para reflejar las generosas donaciones que han hecho ustedes (¡gracias!). A medida que avancemos, utilizaremos estos recursos para compensar a los programadores y otros colaboradores, así como para cubrir los costos en que incurramos (p. ej., proveedores de alojamiento, etc).

## 3) progreso de la 0.4

Al revisar las notas de la semana pasada, todavía nos quedan algunas cosas pendientes para la 0.4, pero las simulaciones han ido bastante bien y se han encontrado la mayoría de los problemas de kaffe. Lo que sería estupendo, sin embargo, es que la gente pudiera poner a prueba a fondo distintos aspectos del router o de las aplicaciones cliente e informar de cualquier error que encuentren.

## 4) ???

Eso es todo lo que tengo para comentar por el momento: agradezco el tiempo que están dedicando para ayudarnos a avanzar, y creo que estamos progresando mucho. Por supuesto, si alguien tiene algo más de lo que quiera hablar, pásense por la reunión en #i2p a... eh... ahora :)

=jr
