---
title: "Notas de estado de I2P del 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Actualización semanal del estado de I2P que abarca la versión 0.4.1.1, el análisis de estadísticas de red, los planes para la biblioteca de streaming en 0.4.2 y el eepserver incluido"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

## Índice:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 estado

Tras un lanzamiento 0.4.1 bastante accidentado (y la posterior actualización rápida 0.4.1.1), la red parece haber vuelto a la normalidad - unos cincuenta y tantos pares activos en este momento, y tanto irc como eepsites(Sitios I2P) son accesibles. La mayor parte de los problemas se debió a pruebas insuficientes del nuevo transporte fuera de condiciones de laboratorio (p. ej., sockets que se rompían en momentos extraños, retrasos excesivos, etc.). La próxima vez que necesitemos hacer cambios en esa capa, nos aseguraremos de probarlo más ampliamente antes del lanzamiento.

## 2) Imágenes bonitas

Durante los últimos días ha habido un gran número de actualizaciones en CVS, y una de las novedades añadidas fue un nuevo componente de registro de estadísticas, que nos permite extraer simplemente los datos estadísticos en bruto a medida que se generan, en lugar de lidiar con los promedios burdos recopilados en /stats.jsp. Con ello, he estado monitorizando algunas estadísticas clave en unos cuantos routers, y nos estamos acercando a localizar los problemas de estabilidad restantes. Las estadísticas en bruto son bastante voluminosas (una ejecución de 20 horas en la máquina de duck generó casi 60MB de datos), pero para eso tenemos gráficos bonitos - `http://dev.i2p.net/~jrandom/stats/`

El eje Y en la mayoría de esos gráficos está en milisegundos, mientras que el eje X está en segundos. Hay algunas cosas interesantes que señalar. Primero, client.sendAckTime.png es una aproximación bastante buena de una única latencia de ida y vuelta, ya que el mensaje de acuse (ack) se envía junto con la carga útil y luego regresa por la ruta completa del tunnel (túnel) - por lo tanto, la gran mayoría de los casi 33,000 mensajes enviados con éxito tuvo un tiempo de ida y vuelta inferior a 10 segundos. Si luego revisamos client.sendsPerFailure.png junto con client.sendAttemptAverage.png, vemos que los 563 envíos fallidos agotaron casi todos el número máximo de reintentos que permitimos (5 con un tiempo de espera suave de 10s por intento y 60s de tiempo de espera estricto), mientras que la mayoría de los otros intentos tuvo éxito en el primer o segundo intento.

Otra imagen interesante es client.timeout.png, que siembra muchas dudas sobre una hipótesis que tenía - que los fallos en el envío de mensajes estaban correlacionados con algún tipo de congestión local. Los datos representados en la gráfica muestran que el uso de ancho de banda entrante varió ampliamente cuando se produjeron fallos, no hubo picos consistentes en el tiempo de procesamiento del envío local y, aparentemente, no hubo ningún patrón en absoluto con la latencia de la prueba de tunnel.

Los archivos dbResponseTime.png y dbResponseTime2.png son similares a client.sendAckTime.png, excepto que corresponden a mensajes de netDb en lugar de mensajes de cliente de extremo a extremo.

El transport.sendMessageFailedLifetime.png muestra cuánto tiempo mantenemos un mensaje localmente antes de marcarlo como fallido por alguna razón (por ejemplo, porque se alcanza su expiración o el par al que va dirigido es inaccesible). Algunos fallos son inevitables, pero esta imagen muestra un número significativo que falla justo después del tiempo de espera local de envío (10s). Hay algunas cosas que podemos hacer para abordar esto: - primero, podemos hacer que la shitlist (lista negra) sea más adaptativa- aumentando exponencialmente el período durante el cual un par está en la shitlist, en lugar de un valor fijo de 4 minutos para cada uno. (esto ya se ha confirmado en CVS) - segundo, podemos marcar preventivamente como fallidos los mensajes cuando parezca que de todos modos fallarían. Para lograrlo, cada conexión lleva un seguimiento de su tasa de envío y, cada vez que se agrega un nuevo mensaje a su cola, si el número de bytes ya encolados dividido por la tasa de envío excede el tiempo restante hasta la expiración, marcar el mensaje como fallido de inmediato. También podríamos usar esta métrica al determinar si aceptar más solicitudes de tunnel a través de un par.

De todos modos, pasemos a la siguiente imagen bonita - transport.sendProcessingTime.png. En esta se ve que esta máquina en particular rara vez es responsable de mucha latencia - típicamente 10-100ms, aunque algunos picos llegan a 1s o más.

Cada punto representado en tunnel.participatingMessagesProcessed.png indica cuántos mensajes se transmitieron a través de un tunnel en el que participó ese router. Al combinar esto con el tamaño promedio de los mensajes, obtenemos una carga de red estimada que el par asume para otras personas.

La última imagen es tunnel.testSuccessTime.png, que muestra cuánto tarda un mensaje en salir por un tunnel y regresar a casa a través de otro tunnel entrante, dándonos una estimación de qué tan buenos son nuestros tunnels.

De acuerdo, ya hay suficientes imágenes bonitas por ahora. Puedes generar los datos tú mismo con cualquier versión posterior a 0.4.1.1-6 estableciendo la propiedad de configuración del router (enrutador) "stat.logFilters" en una lista separada por comas de nombres de estadísticas (obtén los nombres de la página /stats.jsp). Eso se vuelca en stats.log, que puedes procesar con

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
que lo divide en archivos separados para cada estadística, adecuados para cargarlos en tu herramienta favorita (p. ej., gnuplot).

## 3) 0.4.1.2 y 0.4.2

Ha habido muchas actualizaciones desde la versión 0.4.1.1 (consulte el historial para ver la lista completa), pero aún no hay correcciones críticas. Las incluiremos en la próxima versión de parche 0.4.1.2 más adelante esta semana, después de abordar algunos errores pendientes relacionados con la autodetección de IP.

La siguiente tarea importante en ese momento será alcanzar la 0.4.2, que actualmente está prevista como una gran renovación del procesamiento de tunnels. Va a ser mucho trabajo, revisar el cifrado y el procesamiento de mensajes, así como la agrupación de tunnels, pero es bastante crítico, ya que un atacante podría llevar a cabo con bastante facilidad algunos ataques estadísticos contra los tunnels ahora mismo (p. ej., ataque del predecesor con ordenación aleatoria de tunnels o recolección de netDb).

dm planteó, sin embargo, la cuestión de si tendría sentido abordar primero la biblioteca de streaming (actualmente prevista para la versión 0.4.3). El beneficio de eso sería que la red sería a la vez más fiable y tendría mejor rendimiento (throughput), lo que animaría a otros desarrolladores a ponerse a trabajar en aplicaciones cliente. Una vez eso esté implementado, podría volver a la renovación del tunnel y abordar los problemas de seguridad (no visibles para el usuario).

Técnicamente, las dos tareas planificadas para 0.4.2 y 0.4.3 son ortogonales, y de todos modos se van a hacer ambas, así que no parece haber mucha desventaja en intercambiarlas. Me inclino a estar de acuerdo con dm y, a menos que alguien pueda aportar algunas razones para mantener 0.4.2 como la actualización de tunnel y 0.4.3 como la biblioteca de streaming, las intercambiaremos.

## 4) eepserver incluido

Como se mencionó en las notas de la versión 0.4.1, hemos incluido el software y la configuración necesarios para ejecutar un eepsite(sitio I2P) listo para usar - simplemente puedes colocar un archivo en el directorio ./eepsite/docroot/ y compartir el destino de I2P que se encuentra en la consola del router.

Unas cuantas personas me llamaron la atención por mi entusiasmo con los archivos .war; sin embargo, la mayoría de las aplicaciones, por desgracia, requieren un poco más de trabajo que simplemente colocar un archivo en el directorio ./eepsite/webapps/. He preparado un breve tutorial sobre cómo ejecutar el motor de blogs blojsom, y puedes ver cómo se ve eso en el sitio de detonate.

## 5) ???

Eso es todo lo que tengo por ahora; pásate por la reunión dentro de 90 minutos si quieres hablar del tema.

=jr
