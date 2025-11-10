---
title: "Notas de estado de I2P del 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Actualización semanal del estado de I2P que aborda los problemas de rendimiento de la versión 0.3.3 y las próximas optimizaciones"
categories: ["status"]
---

Hola a todos, es hora de la sesión semanal de desahogo

## Índice:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Publicamos la versión 0.3.3 el viernes pasado y, tras uno o dos días de bastante inestabilidad, parece ir bien. No tan bien como la 0.3.2.3, pero por lo general he podido quedarme en irc.duck.i2p en sesiones de 2-7h. Sin embargo, como he visto a mucha gente con problemas, puse en marcha el logger (registro) y monitoricé en detalle qué estaba pasando. La respuesta corta es que simplemente estábamos usando más ancho de banda del necesario, lo que provocaba congestión y fallos de tunnel (debido a que los mensajes de prueba agotaban el tiempo de espera, etc).

He pasado los últimos días de vuelta en el simulador, ejecutando una serie de heartbeats (mensajes de latido) a través de una red para ver qué podemos mejorar, y tenemos toda una serie de actualizaciones en camino basadas en eso:

### netDb update to operate more efficiently

Los mensajes de consulta de netDb existentes son de hasta 10+KB, y aunque las respuestas exitosas son frecuentes, las respuestas fallidas podrían ser de hasta 30+KB (ya que ambas contenían estructuras RouterInfo completas). El nuevo netDb reemplaza esas estructuras RouterInfo completas con el hash del router - convirtiendo mensajes de 10KB y 30KB en mensajes de ~100 bytes.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Estas estructuras eran un vestigio de una idea antigua, pero no aportan ningún valor al anonimato ni a la seguridad del sistema. Al eliminarlas en favor de un conjunto más sencillo de puntos de datos de respuesta, reducimos drásticamente el tamaño de los mensajes de gestión de tunnel y reducimos a la mitad el tiempo de garlic encryption.

### Actualización de netDb para operar de manera más eficiente

El código era un poco 'verboso' durante la creación del tunnel, así que se han omitido los mensajes innecesarios.

### eliminar el SourceRouteBlock y el SourceRouteReplyMessage

Parte del código criptográfico para el garlic routing (enrutamiento garlic) utilizaba relleno fijo basado en algunas técnicas de garlic routing que no estamos utilizando (cuando lo escribí en septiembre y octubre pensé que íbamos a implementar garlic routing multisalto en lugar de tunnels).

También estoy trabajando para ver si puedo lograr la actualización integral del enrutamiento de tunnel para añadir los ID de tunnel por salto.

Como se puede ver en la hoja de ruta, esto abarca gran parte de la versión 0.4.1, pero dado que el cambio en netDb supuso perder compatibilidad con versiones anteriores, bien podríamos aprovechar para realizar de una vez una serie de cambios incompatibles con versiones anteriores.

Sigo ejecutando pruebas en el simulador y tengo que ver si puedo terminar lo del ID de tunnel por salto, pero espero sacar una nueva versión de parche en uno o dos días. No será retrocompatible, así que será una actualización accidentada, pero debería valer la pena.

## 2) NativeBigInteger

Iakin ha estado realizando algunas actualizaciones al código de NativeBigInteger para el equipo de Freenet, optimizando algunas cosas que no usamos, pero también armando código de detección de CPU que podemos usar para seleccionar automáticamente la biblioteca nativa adecuada. Eso significa que podremos distribuir jbigi como una única biblioteca en la instalación predeterminada y elegirá la correcta sin tener que pedirle nada al usuario. También aceptó liberar sus modificaciones y el nuevo código de detección de CPU para que podamos incorporarlo a nuestro código fuente (¡bien por Iakin!). No estoy seguro de cuándo se desplegará, pero avisaré cuando así sea, ya que quienes ya tengan bibliotecas de jbigi probablemente necesiten una nueva.

## 3) ???

Bueno, la última semana hemos estado metidos de lleno en el código, así que no hay demasiadas novedades. ¿Alguien tiene algo más que tratar? Si es así, pásense por la reunión de esta noche, a las 21:00 GMT en #i2p.

=jr
