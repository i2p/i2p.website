---
title: "Notas de estado de I2P para 2004-08-17"
date: 2004-08-17
author: "jr"
description: "Actualización semanal del estado de I2P sobre problemas de rendimiento de la red, ataques de denegación de servicio (DoS) y el desarrollo de Stasher DHT (tabla hash distribuida)"
categories: ["status"]
---

Hola a todos, es hora de la actualización

## Índice:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Estado de la red y 0.3.4.3

Aunque la red ha estado funcionando durante la última semana, por momentos hubo muchos problemas, lo que llevó a una disminución drástica de la fiabilidad. La versión 0.3.4.2 ayudó significativamente a abordar un DoS causado por cierta incompatibilidad y problemas de sincronización de tiempo —véase la gráfica de solicitudes a la base de datos de la red que muestra el DoS (picos que se salen de la gráfica), que se detuvo con la introducción de la 0.3.4.2. Lamentablemente, eso a su vez introdujo su propio conjunto de problemas, provocando que se retransmitiera un número significativo de mensajes, como puede verse en la gráfica de ancho de banda. El aumento de carga también se debió a un incremento real en la actividad de los usuarios, así que no es /tan/ descabellado ;) Aun así, fue un problema.

Durante los últimos días he sido bastante egoísta. Tenemos un montón de correcciones de errores probadas y desplegadas en algunos routers, pero aún no he publicado una versión, ya que rara vez puedo probar la interacción de las incompatibilidades en el software cuando ejecuto mis simulaciones. Así que han estado sometidos a un funcionamiento de la red terriblemente malo mientras retoco cosas para encontrar maneras de permitir que los routers rindan bien cuando muchos routers apestan. Estamos avanzando en ese frente: realizando perfilado y evitando pares que explotan la network database (la base de datos de la red), gestionando con mayor eficiencia las colas de solicitudes de la network database, e imponiendo la diversificación de tunnel.

Todavía no estamos ahí, pero soy optimista. Actualmente se están ejecutando pruebas en la red en producción y, cuando esté listo, habrá una versión 0.3.4.3 que publicará los resultados.

## 2) Stasher

Aum ha estado haciendo un trabajo impresionante en su DHT (tabla hash distribuida), y aunque por ahora tiene algunas limitaciones importantes, parece prometedor. Definitivamente aún no está listo para uso general, pero si te animas a ayudarle con las pruebas (o con código :), échale un vistazo al sitio y pon en marcha un nodo.

## 3) ???

Eso es todo por ahora. Como la reunión debería haber empezado hace un minuto, probablemente debería ir terminando. ¡Nos vemos en #i2p!

=jr
