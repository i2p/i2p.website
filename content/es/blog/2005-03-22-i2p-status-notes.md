---
title: "Notas de estado de I2P del 2005-03-22"
date: 2005-03-22
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que cubren el lanzamiento 0.5.0.3, la implementación del procesamiento por lotes de mensajes de tunnel y herramientas de actualización automática"
categories: ["status"]
---

Hola a todos, una breve actualización de estado

* Index

1) 0.5.0.3 2) procesamiento por lotes 3) actualización 4) ???

* 0.5.0.3

La nueva versión ya está disponible y la mayoría de ustedes han actualizado bastante rápido - ¡gracias!  Hubo varias correcciones de errores para distintos problemas, pero nada revolucionario - lo más importante fue dejar fuera de la red a los usuarios de 0.5 y 0.5.0.1. He estado siguiendo el comportamiento de la red desde entonces, analizando lo que está ocurriendo, y aunque ha habido cierta mejora, todavía hay algunas cosas que hay que resolver.

Habrá una nueva versión en uno o dos días con una corrección para una incidencia que nadie ha encontrado todavía, pero que rompe el nuevo código de procesamiento por lotes. También habrá algunas herramientas para automatizar el proceso de actualización según las preferencias del usuario, además de otros detalles menores.

* batching

Como mencioné en mi blog, hay margen para reducir drásticamente el ancho de banda y la cantidad de mensajes requeridos en la red realizando una agrupación muy simple en lotes de mensajes de tunnel - en lugar de colocar cada mensaje I2NP, sin importar su tamaño, en un mensaje de tunnel propio, añadiendo un breve retraso podemos agrupar hasta 15 o más dentro de un único mensaje de tunnel. Las mayores ganancias se verán en servicios que usan mensajes pequeños (como IRC), mientras que las transferencias de archivos grandes no se verán afectadas tanto. El código para realizar la agrupación en lotes se ha implementado y probado, pero desafortunadamente hay un error en la red en producción que haría que todos, excepto el primer mensaje I2NP dentro de un mensaje de tunnel, se perdieran. Por eso vamos a hacer una versión intermedia con esa corrección incluida, seguida de la versión con la agrupación en lotes aproximadamente una semana después.

* updating

En esta versión interina, vamos a incluir parte del código de la tan comentada 'actualización automática'. Contamos con las herramientas para comprobar periódicamente si hay anuncios de actualización auténticos, descargar la actualización ya sea de forma anónima o no, y luego o bien instalarla o simplemente mostrar un aviso en la consola del router indicándote que está lista y esperando a ser instalada. La propia actualización usará ahora el nuevo formato de actualización firmada de smeghead, que es esencialmente la actualización junto con una firma DSA. Las claves usadas para verificar esa firma vendrán incluidas con I2P y también serán configurables en la consola del router.

El comportamiento predeterminado será simplemente comprobar periódicamente si hay anuncios de actualización, pero no actuar sobre ellos: solo mostrar en la consola del router una función de “Actualizar ahora” con un solo clic. Habrá muchos otros escenarios para distintas necesidades de los usuarios, pero esperamos que todos queden cubiertos mediante una nueva página de configuración.

* ???

Me siento un poco indispuesto, así que lo anterior no entra realmente en todos los detalles de lo que pasa. Pásate por la reunión y rellena los huecos :)

Ah, como comentario aparte, también estaré publicando una nueva clave PGP para mi uso en uno o dos días (ya que esta vence en breve...), así que estén atentos.

=jr
