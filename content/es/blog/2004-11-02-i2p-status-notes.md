---
title: "Notas de estado de I2P del 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Actualización semanal del estado de I2P que cubre el estado de la red, optimizaciones de memoria del núcleo, correcciones de seguridad en el enrutamiento de tunnel (túnel de I2P), progreso de la biblioteca de streaming y desarrollos en correo/BitTorrent"
categories: ["status"]
---

¡Hola a todos, es hora de la actualización semanal!

## Índice:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Estado de la red

Más o menos como antes - un número estable de pares, eepsites(sitios I2P) bastante accesibles, y IRC durante horas seguidas. Puedes echar un vistazo a la accesibilidad de varios eepsites(sitios I2P) a través de varias páginas:
- `http://gott.i2p/sites.html`
- `http://www.baffled.i2p/links.html`
- `http://thetower.i2p/pings.txt`

## 2) Actualizaciones del núcleo

Para quienes frecuentan el canal (o leen los registros de CVS), han visto mucha actividad, aunque ha pasado un tiempo desde la última versión. Se puede encontrar en línea una lista completa de cambios desde la versión 0.4.1.3, pero hay dos modificaciones importantes, una buena y una mala:

La buena noticia es que hemos reducido drásticamente el memory churn (alta rotación de asignación y liberación de memoria) provocado por toda clase de creación absurda de objetos temporales. Por fin me harté de ver cómo el GC (recolector de basura) se volvía loco mientras depuraba la nueva biblioteca de streaming, así que, tras unos días de perfilado, ajustes y optimización, las partes más feas han quedado saneadas.

La mala es una corrección de error relacionada con la forma en que se manejan algunos mensajes enrutados por tunnel - hubo algunas situaciones en las que se enviaba un mensaje directamente al router de destino en lugar de ser enrutado por tunnel antes de la entrega, lo que podría ser explotado por un adversario que pueda programar un poco. Ahora, en caso de duda, enrutamos por tunnel correctamente.

Eso puede sonar bien, pero la parte 'mala' es que significa que habrá algo más de latencia debido a los saltos adicionales, aunque estos son saltos que de todos modos era necesario utilizar.

También hay otras actividades de depuración en curso en el núcleo, así que aún no ha habido un lanzamiento oficial - CVS HEAD está en 0.4.1.3-8. En los próximos días probablemente tengamos una versión 0.4.1.4, solo para dejar todo eso resuelto. No incluirá la nueva biblioteca de streaming, por supuesto.

## 3) Biblioteca de streaming

Hablando de la streaming lib (biblioteca de streaming), hemos avanzado mucho en este frente, y la comparación en paralelo entre las bibliotecas antigua y nueva se ve bien. Sin embargo, aún queda trabajo por hacer y, como dije la última vez, no vamos a precipitar su salida. Eso sí significa que la hoja de ruta se ha retrasado, probablemente en el rango de 2-3 semanas. Más detalles cuando estén disponibles.

## 4) progreso de mail.i2p

¡Muchas novedades esta semana: proxies de entrada y de salida funcionando! Consulta www.postman.i2p para más información.

## 5) Progreso de BT

Últimamente ha habido mucha actividad en torno a portar un cliente de BitTorrent, así como a actualizar algunos ajustes del tracker. Quizá podamos obtener algunas novedades de las personas involucradas durante la reunión.

## 6) ???

Eso es todo por mi parte. Perdón por el retraso, se me olvidó todo ese rollo del cambio de hora. En fin, nos vemos en un rato.

=jr
