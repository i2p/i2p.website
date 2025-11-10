---
title: "Notas de estado de I2P para el 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Actualización semanal que cubre los planes de despliegue del transporte SSU, la finalización de la recompensa por pruebas unitarias y consideraciones sobre licencias, y el estado de Kaffe Java"
categories: ["status"]
---

Hola a todos, otra vez toca la actualización semanal

* Index

1) Estado de SSU 2) Estado de las pruebas unitarias 3) Estado de Kaffe 4) ???

* 1) SSU status

Ha habido algo más de progreso en el transporte SSU, y mi idea actual es que, tras algunas pruebas adicionales en la red real, podremos desplegarlo como la 0.6 sin mucha demora. La primera versión de SSU no incluirá soporte para quienes no puedan abrir un puerto en su cortafuegos o configurar su NAT, pero eso se implementará en la 0.6.1. Una vez que la 0.6.1 haya salido, esté probada y funcionando de maravilla (aka 0.6.1.42), pasaremos a la 1.0.

Mi inclinación personal es eliminar por completo el transporte TCP a medida que se despliega el transporte SSU, para que las personas no tengan que tener ambos habilitados (reenviando tanto puertos TCP como UDP) y para que los desarrolladores no tengan que mantener código que no es necesario. ¿Alguien tiene alguna opinión firme al respecto?

* 2) Unit test status

Como se mencionó la semana pasada, Comwiz se ha presentado para reclamar la primera fase de la recompensa por pruebas unitarias (¡hurra por Comwiz!  gracias a duck y zab por financiar también la recompensa). El código se ha confirmado en CVS y, según tu configuración local, quizá puedas generar los informes de junit y clover entrando en el directorio i2p/core/java y ejecutando "ant test junit.report" (espera alrededor de una hora...) y ver i2p/reports/core/html/junit/index.html. Por otro lado, puedes ejecutar "ant useclover test junit.report clover.report" y ver i2p/reports/core/html/clover/index.html.

La desventaja de ambos conjuntos de pruebas tiene que ver con ese concepto tan absurdo que la clase dirigente llama "ley de derechos de autor". Clover es un producto comercial, aunque la gente de cenqua permite su uso gratuito por parte de desarrolladores de código abierto (y amablemente han accedido a concedernos una licencia). Para generar los informes de clover, necesitas tener clover instalado localmente - yo tengo clover.jar en ~/.ant/lib/, junto a mi archivo de licencia. La mayoría de la gente no necesitará clover, y como publicaremos los informes en la web, no hay pérdida de funcionalidad por no instalarlo.

Por otro lado, nos vemos afectados por la otra cara de la ley de derechos de autor cuando tomamos en consideración el propio framework de pruebas unitarias: junit se publica bajo la IBM Common Public License 1.0 que, según la FSF [1], no es compatible con la GPL. Ahora bien, si bien no tenemos ningún código GPL (al menos no en el núcleo ni en el router), al volver a nuestra política de licencias [2], nuestro objetivo, en los pormenores de cómo otorgamos licencias, es permitir que la mayor cantidad posible de personas use lo que se está creando, ya que el anonimato se fortalece con la compañía.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Dado que algunas personas inexplicablemente publican software bajo la GPL, tiene sentido que nos esforcemos por permitirles usar I2P sin restricciones. Como mínimo, eso significa que no podemos permitir que la funcionalidad real que exponemos dependa del código bajo la CPL (p. ej., junit.framework.*). Me gustaría extender eso para incluir también las pruebas unitarias, pero junit parece ser la lingua franca de los frameworks de pruebas (y no creo que sería ni remotamente sensato decir "oye, ¡construyamos nuestro propio framework de pruebas unitarias de dominio público!", dados nuestros recursos).

Dado todo eso, esto es lo que estoy pensando. Incluiremos junit.jar en CVS y lo usaremos cuando los usuarios ejecuten las pruebas unitarias, pero las propias pruebas unitarias no se integrarán en i2p.jar ni en router.jar, y no se distribuirán en las versiones. Podríamos poner a disposición un conjunto adicional de archivos JAR (i2p-test.jar y router-test.jar), si fuera necesario, pero no serían utilizables por aplicaciones con licencia GPL (ya que dependen de junit).

=jr
