---
title: "Agrupar Múltiples Dientes de Datos en Ajo"
number: "115"
author: "original"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Necesita-Investigación"
thread: "http://zzz.i2p/topics/1797"
---

## Visión General

Esta propuesta trata sobre enviar múltiples Dientes de Ajo de Datos dentro de un Mensaje de Ajo de extremo a extremo, en lugar de solo uno.


## Motivación

No está claro.


## Cambios Requeridos

Los cambios serían en OCMOSJ y clases auxiliares relacionadas, y en ClientMessagePool. Como no hay cola ahora, sería necesaria una nueva cola y algo de retraso. Cualquier agrupamiento tendría que respetar un tamaño máximo de ajo para minimizar pérdidas. ¿Quizás 3KB? Se querría instrumentar cosas primero para medir con qué frecuencia se utilizaría esto.


## Reflexiones

No está claro si esto tendrá algún efecto útil, ya que la transmisión ya hace agrupaciones y selecciona el MTU óptimo. La agrupación aumentaría el tamaño del mensaje y la probabilidad de pérdida exponencial.

La excepción es el contenido no comprimido, comprimido en el nivel de I2CP. Pero el tráfico HTTP ya está comprimido en un nivel superior, y los datos de Bittorrent suelen ser incomprensibles. ¿Qué deja esto? I2pd actualmente no hace la compresión x-i2p-gzip, por lo que podría ayudar mucho más allí. Pero el objetivo declarado de no quedarse sin etiquetas es mejor arreglado con una implementación adecuada de ventanas en su biblioteca de transmisión.


## Compatibilidad

Esto es compatible hacia atrás, ya que el receptor de ajo ya procesará todos los dientes que reciba.
