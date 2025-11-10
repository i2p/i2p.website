---
title: "Notas de estado de I2P del 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Actualización del estado de la red, nuevo proceso de construcción de tunnel para 0.6.2 y mejoras de fiabilidad"
categories: ["status"]
---

Hola a todos, el martes no deja de volver...

* Index

1) Estado de la red 2) Nuevo proceso de compilación 3) ???

* 1) Net status

La última semana no ha traído muchos cambios a la red, con la mayoría de los usuarios (77%) actualizados a la última versión. Aun así, hay algunos cambios importantes en camino, relacionados con el nuevo proceso de construcción de tunnel, y estos cambios causarán algunos contratiempos para quienes ayudan a probar las compilaciones no publicadas. En general, sin embargo, quienes usan las versiones deberían seguir teniendo un nivel de servicio bastante fiable.

* 2) New build process

Como parte de la renovación de los tunnel para la 0.6.2, estamos cambiando el procedimiento utilizado dentro del router para adaptarnos mejor a las condiciones cambiantes y gestionar la carga de forma más limpia. Esto es un paso previo a integrar las nuevas estrategias de selección de pares y la nueva criptografía de creación de tunnel, y es totalmente retrocompatible. Sin embargo, por el camino estamos saneando algunas de las peculiaridades del proceso de construcción de tunnel y, aunque algunas de esas peculiaridades han ayudado a disimular ciertos problemas de fiabilidad, puede que hayan supuesto un compromiso menos que óptimo entre anonimato y fiabilidad. En concreto, se recurría a tunnels de 1 salto de respaldo ante fallos catastróficos; el nuevo proceso preferirá, en cambio, la inaccesibilidad en lugar de utilizar tunnels de respaldo, lo que significa que la gente verá más problemas de fiabilidad. Al menos, serán visibles hasta que se aborde la causa del problema de fiabilidad de los tunnel.

En cualquier caso, por el momento el proceso de compilación no proporciona un nivel de fiabilidad aceptable, pero en cuanto lo haga lo publicaremos para todos ustedes en una versión.

* 3) ???

Sé que algunos otros están trabajando en diferentes actividades relacionadas, pero dejaré que sean ellos quienes nos den las novedades cuando lo consideren apropiado. En cualquier caso, nos vemos en la reunión en unos minutos.

=jr
