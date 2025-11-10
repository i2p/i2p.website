---
title: "Notas de estado de I2P del 2006-05-09"
date: 2006-05-09
author: "jr"
description: "Versión 0.6.1.18 con mejoras en la estabilidad de la red, nuevo servidor de desarrollo 'baz' y desafíos de compatibilidad de GCJ en Windows"
categories: ["status"]
---

Hola a todos, ya es martes otra vez

* Index

1) Estado de la red y 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Después de otra semana de pruebas y ajustes, lanzamos una nueva versión a primera hora de la tarde que debería colocarnos en un entorno más estable desde el cual realizar mejoras. Probablemente no veamos mucho efecto hasta que se despliegue ampliamente, así que quizá tengamos que esperar unos días para ver cómo evoluciona, pero las mediciones, por supuesto, continuarán.

Uno de los aspectos de las compilaciones y versiones más recientes que zzz mencionó el otro día fue que aumentar el número de backup tunnels ahora puede tener un impacto considerable cuando se hace al tiempo que se reduce el número de tunnels paralelos. No creamos nuevos leases (autorizaciones temporales de entrada) hasta que tenemos un número suficiente de tunnels activos, de modo que los backup tunnels pueden desplegarse rápidamente en caso de fallo de un tunnel activo, reduciendo la frecuencia con la que un cliente se queda sin un lease activo. Aun así, esto es solo un ajuste a un síntoma, y la última versión debería ayudar a abordar la causa raíz.

* 2) baz

"baz", la nueva máquina que bar donó por fin ha llegado, un portátil amd64 Turion (con winxp en el disco de arranque y unos cuantos otros sistemas operativos en preparación mediante unidades externas). También he estado trabajando con él estos últimos días, intentando probar algunas ideas de despliegue en él. Sin embargo, un problema con el que me estoy encontrando es hacer que gcj funcione en Windows. Más concretamente, un gcj con un gnu/classpath moderno. Los comentarios que circulan son bastante negativos: se puede compilar de forma nativa en mingw o compilarse de forma cruzada desde Linux, pero tiene problemas como provocar un fallo de segmentación cada vez que una excepción cruza un límite de dll. Así que, por ejemplo, si java.io.File (ubicado en libgcj.dll) lanza una excepción, si esta es capturada por algo en net.i2p.* (ubicado en libi2p.dll o i2p.exe), *puf*, adiós a la aplicación.

Sí, la cosa no pinta muy bien. Al equipo de gcj le interesaría mucho si alguien pudiera sumarse y ayudar con el desarrollo en win32, pero no parece que haya soporte viable inminente. Así que parece que tendremos que planear seguir usando una JVM de Sun en Windows, mientras damos soporte a gcj/kaffe/sun/ibm/etc en *nix. Supongo que eso no es tan malo, ya que son los usuarios de *nix quienes tienen problemas para empaquetar y distribuir JVMs.

* 3) ???

Ok, ya voy tarde para la reunión, así que debería terminar esto y cambiar a la ventana de irc, supongo... nos vemos en un rato ;)

=jr
