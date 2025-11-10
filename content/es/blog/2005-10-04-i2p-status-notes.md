---
title: "Notas de estado de I2P del 2005-10-04"
date: 2005-10-04
author: "jr"
description: "Actualización semanal que cubre el éxito del lanzamiento 0.6.1.1 con 3-400 pares, los esfuerzos de reconciliación del fork de i2phex y los avances en la automatización de Syndie con pet names (nombres asignados por el usuario) y pulls programados (extracciones)"
categories: ["status"]
---

Hola a todos, es hora de nuestras notas semanales de estado (inserte vítores aquí)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

Como se anunció en los lugares habituales, la 0.6.1.1 salió el otro día y, hasta ahora, los informes han sido positivos. La red ha crecido hasta situarse de forma estable en 300–400 pares conocidos, y el rendimiento ha sido bastante bueno, aunque el uso de CPU ha aumentado un poco. Esto probablemente se deba a errores de larga data que permiten incorrectamente que se acepten direcciones IP inválidas, lo que a su vez provoca una rotación más alta de lo necesario. Ha habido correcciones para esto y otras cosas en las compilaciones de CVS desde la 0.6.1.1, así que probablemente tengamos una 0.6.1.2 más adelante esta semana.

* 2) i2phex

Aunque algunos quizá hayan notado la discusión en varios foros sobre i2phex y la bifurcación de legion, ha habido comunicación adicional entre legion y yo, y estamos trabajando para volver a fusionar ambos. Habrá más información al respecto cuando esté disponible.

Además, redzara está trabajando intensamente en fusionar i2phex con la versión actual de phex, y striker ha aportado algunas mejoras adicionales, así que hay novedades interesantes en camino.

* 3) syndie

Ragnarok ha estado trabajando intensamente en syndie en los últimos días, integrando la base de datos de pet names (nombres de confianza) de syndie con la del router, así como automatizando la sindicación con extracciones programadas desde repositorios remotos seleccionados. La parte de automatización ya está terminada y, aunque queda algo de trabajo de interfaz de usuario (UI), ¡está en bastante buen estado!

* 4) ???

También están pasando muchas otras cosas estos días, incluyendo trabajo en la nueva documentación de introducción técnica, la migración de IRC y la renovación del sitio web. Si alguien tiene algo que le gustaría comentar, pásense por la reunión en unos minutos y saluden.

=jr
