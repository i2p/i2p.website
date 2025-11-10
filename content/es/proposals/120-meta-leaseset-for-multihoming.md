---
title: "Meta-LeaseSet para Multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Rechazado"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Resumen

Esta propuesta trata sobre implementar un soporte adecuado para multihoming en I2P que pueda escalar hasta sitios grandes.


## Motivación

El multihoming es un truco y presumiblemente no funcionará para, por ejemplo, facebook.i2p a gran escala. Supongamos que tuviéramos 100 multihogares cada uno con 16 túneles, serían 1600 publicaciones de LS cada 10 minutos, o casi 3 por segundo. Los floodfills se verían abrumados y los mecanismos de control se activarían. Y eso es antes de siquiera mencionar el tráfico de búsqueda.

Necesitamos algún tipo de meta-LS, donde el LS liste los 100 hashes de LS reales. Esto tendría una duración larga, mucho más que 10 minutos. Así es una búsqueda en dos etapas para el LS, pero la primera etapa podría ser almacenada en caché por horas.


## Especificación

El meta-LeaseSet tendría el siguiente formato::

  - Destinación
  - Marca de tiempo de publicación
  - Expiración
  - Banderas
  - Propiedades
  - Número de entradas
  - Número de revocaciones

  - Entradas. Cada entrada contiene:
    - Hash
    - Banderas
    - Expiración
    - Costo (prioridad)
    - Propiedades

  - Revocaciones. Cada revocación contiene:
    - Hash
    - Banderas
    - Expiración

  - Firma

Las banderas y propiedades se incluyen para máxima flexibilidad.


## Comentarios

Esto podría luego generalizarse para ser una búsqueda de servicio de cualquier tipo. El identificador del servicio es un hash SHA256.

Para una escalabilidad aún más masiva, podríamos tener múltiples niveles, es decir, un meta-LS podría apuntar a otros meta-LS.
