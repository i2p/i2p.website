---
title: "I2P Status Notes for 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Actualización de Año Nuevo que abarca la estabilidad de la versión 0.6.1.8, los resultados de las pruebas de carga y el perfilado de pares para optimizar el rendimiento, y una revisión integral de 2005 con un adelanto de la hoja de ruta de 2006"
categories: ["status"]
---

¡Hola a todos, feliz año nuevo! Retomemos nuestras notas semanales de estado tras una semana sin ellas -

* Index

1) Estado de la red y 0.6.1.8 2) Resultados de pruebas de carga y perfilado de pares 3) Revisión de 2005 / avance de 2006 / ???

* 1) Net status and 0.6.1.8

La otra semana lanzamos la 0.6.1.8 y los informes de campo indican que las modificaciones de zzz han ayudado bastante, y las cosas parecen bastante estables en la red, incluso con el tráfico de red sustancialmente incrementado últimamente (la media parece haberse duplicado en el último mes, según stats.i2p). I2PSnark también parece estar funcionando bastante bien - aunque nos hemos topado con algunos contratiempos, hemos rastreado y corregido la mayoría en compilaciones posteriores. No ha habido muchos comentarios respecto a la nueva interfaz de blog de Syndie, pero sí ha habido un ligero aumento en el tráfico de Syndie (en parte debido al descubrimiento por parte de protocol del importador rss/atom de dust :)

* 2) Load testing results and peer profiling

Durante las últimas semanas, he estado tratando de acotar nuestro cuello de botella de rendimiento. Los distintos componentes de software son capaces de enviar datos a tasas mucho más altas de las que solemos ver para la comunicación de extremo a extremo sobre I2P, así que he estado midiendo su rendimiento en la red en vivo con código personalizado para someterlos a pruebas de estrés. El primer conjunto de pruebas, construyendo tunnels de entrada de un salto a través de todos los routers de la red y transmitiendo datos por ese tunnel lo antes posible, arrojó resultados bastante prometedores, con routers manejando tasas que estaban en el orden de lo que cabría esperar de sus capacidades (p. ej., la mayoría solo manejando un promedio histórico de 4-16KBps, pero otros alcanzando 20-120KBps a través de un solo tunnel). Esta prueba fue una buena base de referencia para seguir explorando y demostró que el propio procesamiento del tunnel es capaz de mover mucho más de lo que solemos ver.

Los intentos de replicar esos resultados a través de tunnels activos no fueron tan exitosos. O, quizá se podría decir que fueron más exitosos, ya que mostraron un rendimiento similar al que vemos actualmente, lo que significaba que íbamos por buen camino. Volviendo a los resultados de la prueba de 1 salto, modifiqué el código para seleccionar pares que identifiqué manualmente como rápidos y volví a ejecutar las pruebas de carga a través de tunnels activos con esta selección de pares "tramposa", y, si bien no alcanzó la marca de 120KBps, sí mostró una mejora razonable.

Desafortunadamente, pedir a las personas que seleccionen manualmente a sus pares tiene serios problemas tanto para el anonimato como, bueno, para la facilidad de uso, pero con los datos de las pruebas de carga en la mano, parece haber una solución. Durante los últimos días he estado probando un método nuevo para perfilar a los pares por su velocidad: esencialmente monitorizar su caudal máximo sostenido, en lugar de su latencia reciente. Las implementaciones simplistas han sido bastante exitosas y, si bien no ha elegido exactamente a los pares que yo habría escogido manualmente, ha hecho un trabajo bastante bueno. Aun así, quedan algunos detalles por resolver, como asegurarnos de poder promover los tunnels exploratorios al nivel rápido, pero actualmente estoy probando algunos experimentos en ese frente.

En general, creo que nos estamos acercando al final de esta etapa de mejora del caudal (throughput), ya que estamos presionando contra el cuello de botella más pequeño y ampliándolo. Estoy seguro de que pronto nos toparemos con el siguiente, y esto definitivamente no nos va a dar velocidades normales de Internet, pero debería ayudar.

* 3) 2005 review / 2006 preview / ???

Decir que 2005 abrió mucho camino es quedarse corto - hemos mejorado I2P de numerosas maneras en las 25 versiones del año pasado, multiplicamos por cinco el tamaño de la red, desplegamos varias nuevas aplicaciones cliente (Syndie, I2Phex, I2PSnark, I2PRufus), migramos a la nueva red IRC irc2p de postman y cervantes, y vimos florecer algunos eepsites(I2P Sites) útiles (como stats.i2p de zzz, orion.i2p de orion, y los servicios de proxy y monitoreo de tino, por mencionar solo algunos). La comunidad también ha madurado un poco más, en gran medida gracias a los esfuerzos de soporte de Complication y otros en el foro y en los canales, y la calidad y la diversidad de los informes de errores de todos los sectores han mejorado sustancialmente. El apoyo financiero continuo de quienes están dentro de la comunidad ha sido impresionante, y si bien aún no está al nivel necesario para un desarrollo completamente sostenible, sí contamos con un colchón que puede mantenerme alimentado durante el invierno.

A todos los que han participado durante este último año, ya sea técnica, social o económicamente, ¡gracias por su ayuda!

2006 va a ser un gran año para nosotros, con la 0.6.2 llegando este invierno, con el lanzamiento 1.0 previsto para algún momento de la primavera o el verano, y la 2.0 en otoño, si no antes. Este es el año en el que veremos de qué somos capaces, y el trabajo en la capa de aplicación será aún más crítico que antes. Así que si tienes algunas ideas, ahora es el momento de ponerse manos a la obra :)

De todos modos, nuestra reunión semanal de estado comienza en unos minutos, así que si hay algo que quieras discutir más a fondo, pásate por #i2p en los lugares habituales [1] y ¡saluda!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
