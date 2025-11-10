---
title: "Notas de estado de I2P para 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Actualización semanal del estado de I2P que cubre la implementación de un nuevo protocolo de transporte, la autodetección de IP y el progreso de la versión 0.4.1"
categories: ["status"]
---

Hola a todos, es hora de la actualización semanal

## Índice:

1. New transport
2. 0.4.1 status
3. ???

## 1) Nuevo transporte

La versión 0.4.1 ha tardado más de lo esperado, pero el nuevo protocolo de transporte y su implementación ya están disponibles con todo lo planificado - detección de IP, establecimiento de conexiones de bajo costo y una interfaz más sencilla para ayudar a depurar cuando las conexiones fallan. Esto se logra desechando por completo el antiguo protocolo de transporte e implementando uno nuevo, aunque seguimos teniendo los mismos términos de moda (2048bit DH + STS, AES256/CBC/PKCS#5). Si desea revisar el protocolo, está en la documentación. La nueva implementación también es mucho más limpia, ya que la versión anterior no era más que un conjunto de actualizaciones acumuladas durante el último año.

De todos modos, hay algunas cosas en el nuevo código de detección de IP que vale la pena mencionar. Lo más importante es que es completamente opcional: si especificas una dirección IP en la página de configuración (o en el propio router.config), siempre usará esa dirección, pase lo que pase. Sin embargo, si lo dejas en blanco, tu router permitirá que el primer par con el que contacte le diga cuál es su dirección IP, y entonces empezará a escuchar en ella (tras añadirla a su propio RouterInfo y colocarla en la base de datos de la red). Bueno, eso no es del todo cierto - si no has establecido explícitamente una dirección IP, confiará en cualquiera para que le diga a qué dirección IP se le puede alcanzar siempre que el par no tenga conexiones. Así que, si tu conexión a Internet se reinicia, quizá dándote una nueva dirección DHCP, tu router confiará en el primer par al que pueda contactar.

Sí, esto significa que ya no necesitas dyndns. Por supuesto, puedes seguir usándolo si lo deseas, pero no es necesario.

Sin embargo, esto no cubre todo lo que necesitas: si tienes NAT o un cortafuegos, conocer tu dirección IP externa es solo la mitad del trabajo; aún necesitas abrir el puerto entrante. Pero es un comienzo.

(como nota al margen, para las personas que operan sus propias redes privadas de I2P o simuladores, hay un nuevo par de opciones que deben configurarse i2np.tcp.allowLocal y i2np.tcp.tagFile)

## 2) estado de 0.4.1

Más allá de los elementos de la hoja de ruta para la 0.4.1, quiero incluir algunas cosas más: tanto correcciones de errores como actualizaciones del monitoreo de la red. En este momento estoy investigando algunos problemas de actividad excesiva de asignación y liberación de memoria, y quiero explorar algunas hipótesis sobre los problemas ocasionales de fiabilidad en la red, pero estaremos listos para publicar la versión pronto, quizá el jueves. Lamentablemente no será retrocompatible, así que el proceso será un poco accidentado, pero con el nuevo proceso de actualización y una implementación del transporte más tolerante, no debería ser tan malo como las anteriores actualizaciones no retrocompatibles.

## 3) ???

Sí, hemos tenido actualizaciones breves las últimas dos semanas, pero eso se debe a que estamos en las trincheras, concentrados en la implementación, en lugar de en varios diseños de más alto nivel. Podría hablarles de los datos de perfilado, o de la caché de etiquetas de conexión de 10.000 para el nuevo transporte, pero eso no es tan interesante. Sin embargo, quizá tengan algunas cosas adicionales que discutir, así que pásense por la reunión de esta noche y suéltenlo todo.

=jr
