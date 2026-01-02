---
title: "Notas de estado de I2P del 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Análisis del rendimiento de la red, investigación de cuellos de botella de la CPU, planificación del lanzamiento de Syndie 1.0 y evaluación del control de versiones distribuido"
categories: ["status"]
---

Hola a todos, unas notas de estado con retraso esta semana

* Index

1) Estado de la red 2) Estado de desarrollo del Router 3) Justificación de Syndie (continuación) 4) Estado de desarrollo de Syndie 5) Control de versiones distribuido 6) ???

* 1) Net status

Las últimas una o dos semanas han sido bastante estables en irc y otros servicios, aunque dev.i2p/squid.i2p/www.i2p/cvs.i2p tuvieron algunos contratiempos (debido a problemas temporales relacionados con el sistema operativo). Todo parece estar en un estado estable por el momento.

* 2) Router dev status

La otra cara de la discusión sobre Syndie es "entonces, ¿qué significa eso para el router?", y, para responder a eso, permíteme explicar un poco en qué punto se encuentra ahora mismo el desarrollo del router.

En general, lo que impide que el router alcance la versión 1.0 es, en mi opinión, su rendimiento, no sus propiedades de anonimato. Sin duda, hay cuestiones de anonimato que mejorar, pero aunque obtenemos un rendimiento bastante bueno para una red anónima, nuestro rendimiento no es suficiente para un uso más amplio. Además, las mejoras en el anonimato de la red no mejorarán su rendimiento (en la mayoría de los casos que se me ocurren, las mejoras de anonimato reducen el throughput (caudal de datos) y aumentan la latencia). Necesitamos resolver primero los problemas de rendimiento, porque si el rendimiento es insuficiente, todo el sistema es insuficiente, sin importar qué tan sólidas sean sus técnicas de anonimato.

Entonces, ¿qué está frenando nuestro rendimiento? Por extraño que parezca, parece ser nuestro uso de CPU. Antes de explicar exactamente por qué, primero un poco más de contexto.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Por lo tanto, necesitamos niveles de routers: algunos accesibles globalmente con altos límites de ancho de banda (tier A), y otros no (tier B). Esto ya se ha implementado en la práctica mediante la información de capacidad en la netDb y, desde hace uno o dos días, la proporción de tier B respecto a tier A ha sido de alrededor de 3 a 1 (93 routers con cap L, M, N u O, y 278 con cap K).

Ahora, básicamente hay dos recursos escasos que gestionar en el nivel A - ancho de banda y CPU. El ancho de banda puede gestionarse por los medios habituales (distribuir la carga entre un conjunto amplio, hacer que algunos pares gestionen cantidades enormes [p. ej., los que tienen T3s], y rechazar o limitar tunnels y conexiones individuales).

Gestionar el uso de CPU es más difícil. El principal cuello de botella de CPU observado en routers de nivel A es el descifrado de las solicitudes de construcción de tunnel. Los routers grandes pueden quedar (y quedan) completamente consumidos por esta actividad; por ejemplo, el tiempo de descifrado de tunnel con promedio histórico en uno de mis routers es de 225ms, y la frecuencia *promedio* histórica de descifrado de solicitudes de tunnel es de 254 eventos cada 60 segundos, o 4.2 por segundo. Basta con multiplicar esos dos valores y se ve que el 95% de la CPU se consume solo en el descifrado de solicitudes de tunnel (y eso sin tener en cuenta los picos en el recuento de eventos). Ese router de alguna manera aún logra participar en 4-6000 tunnels a la vez, aceptando aproximadamente el 80% de las solicitudes descifradas.

Por desgracia, debido a que la CPU de ese router está tan sobrecargada, tiene que descartar una cantidad significativa de solicitudes para construir tunnels antes de que siquiera puedan ser descifradas (de lo contrario, las solicitudes permanecerían en la cola tanto tiempo que, incluso si fueran aceptadas, el solicitante original las habría considerado perdidas o demasiado cargadas como para hacer nada de todos modos). En ese sentido, la tasa de aceptación del 80% del router se ve mucho peor: a lo largo de su vida útil, descifró alrededor de 250 mil solicitudes (lo que significa que se aceptaron alrededor de 200 mil), pero tuvo que descartar alrededor de 430 mil solicitudes en la cola de descifrado debido a la sobrecarga de la CPU (convirtiendo esa tasa de aceptación del 80% en 30%).

Las soluciones parecen ir en la dirección de reducir el costo de CPU relevante del descifrado de solicitudes de tunnel. Si reducimos el tiempo de CPU en un orden de magnitud, eso aumentaría sustancialmente la capacidad del router de nivel A, reduciendo así los rechazos (tanto explícitos como implícitos, debido a solicitudes descartadas). Eso, a su vez, aumentaría la tasa de éxito de construcción de tunnel, reduciendo así la frecuencia de vencimientos de lease (concesión temporal), lo que a su vez reduciría la carga de ancho de banda en la red debido a la reconstrucción de tunnel.

Un método para lograr esto sería cambiar las solicitudes de construcción de tunnel de usar Elgamal de 2048 bits a, digamos, 1024 o 768 bits. El problema, sin embargo, es que si rompes el cifrado de un mensaje de solicitud de construcción de tunnel, conoces la ruta completa del tunnel. Incluso si optáramos por esta vía, ¿cuánto nos aportaría? Una mejora de un orden de magnitud en el tiempo de descifrado podría quedar anulada por un aumento de un orden de magnitud en la proporción de nivel B a nivel A (también conocido como el problema de los freeriders), y entonces nos quedaríamos atascados, ya que no hay forma de que podamos pasar a Elgamal de 512 o 256 bits (y mirarnos al espejo ;)

Una alternativa sería usar un cifrado más débil, pero eliminar la protección contra los ataques de conteo de paquetes que añadimos con el nuevo proceso de construcción de tunnel. Eso nos permitiría usar claves negociadas completamente efímeras en un tunnel telescópico similar a Tor (aunque, de nuevo, expondría al creador del tunnel a ataques pasivos triviales de conteo de paquetes que identifican un servicio).

Otra idea es publicar y utilizar información de carga aún más explícita en el netDb, permitiendo que los clientes detecten con mayor precisión situaciones como la anterior, en las que un router de alto ancho de banda descarta el 60% de sus mensajes de solicitud de tunnel sin siquiera mirarlos. Hay algunos experimentos que vale la pena realizar por esta vía, y pueden hacerse con retrocompatibilidad total, así que deberíamos verlos pronto.

Así que ese es el cuello de botella en el router/red tal como lo veo hoy. Se agradecerán mucho todas las sugerencias sobre cómo podemos abordarlo.

* 3) Syndie rationale continued

Hay una publicación detallada en el foro sobre Syndie y cómo encaja con todo - consúltalo en <http://forum.i2p.net/viewtopic.php?t=1910>

Además, solo me gustaría destacar dos fragmentos de la documentación de Syndie en la que se está trabajando. Primero, de irc (y de la FAQ que aún no está publicada):

<bar> una pregunta que me he estado planteando es: ¿quién más adelante va a tener        el valor suficiente para alojar servidores/archivos de producción de Syndie?  <bar> ¿no van a ser tan fáciles de rastrear como los eepsites(I2P Sites)        lo son hoy?  <jrandom> los archivos públicos de Syndie no tienen la capacidad de        *leer* el contenido publicado en los foros, a menos que los foros publiquen        las claves para hacerlo  <jrandom> y consulta el segundo párrafo de usecases.html  <jrandom> por supuesto, quienes alojan archivos que reciban órdenes legales        de retirar un foro probablemente lo harán  <jrandom> (pero entonces la gente puede mudarse a otro        archivo, sin interrumpir el funcionamiento del foro)  <void> sí, deberías mencionar el hecho de que la migración a un        medio diferente va a ser transparente  <bar> si mi archivo cierra, puedo subir todo mi foro a uno        nuevo, ¿verdad?  <jrandom> exacto, bar  <void> pueden usar dos métodos al mismo tiempo mientras migran  <void> y cualquiera puede sincronizar los medios  <jrandom> correcto, void

La sección relevante de (aún no publicado) Syndie usecases.html es:


Aunque muchos grupos distintos suelen querer organizar debates en un foro en línea, la naturaleza centralizada de los foros tradicionales (sitios web, BBS, etc.) puede ser un problema. Por ejemplo, el sitio que aloja el foro puede ser dejado fuera de línea mediante ataques de denegación de servicio o por acción administrativa. Además, un único servidor ofrece un punto sencillo para monitorizar la actividad del grupo, de modo que, incluso si un foro es seudónimo, esos seudónimos pueden vincularse a la IP que publicó o leyó mensajes individuales.

Además, los foros no solo están descentralizados, sino que también están organizados de manera ad hoc y, aun así, son totalmente compatibles con otras técnicas de organización. Esto significa que un grupo pequeño de personas puede gestionar su foro usando una técnica (distribuir los mensajes pegándolos en un sitio wiki), y otro puede gestionar su foro usando otra técnica (publicar sus mensajes en una tabla hash distribuida como OpenDHT), y si una persona conoce ambas técnicas, puede sincronizar ambos foros entre sí. Esto permite que quienes solo conocían el sitio wiki hablen con quienes solo conocían el servicio OpenDHT sin saber nada los unos de los otros. Yendo más allá, Syndie permite que células individuales controlen su propia exposición mientras se comunican a través de toda la organización.

* 4) Syndie dev status

Ha habido muchos avances en Syndie últimamente, con 7 versiones alfa distribuidas a la gente en el canal de irc. La mayoría de los problemas importantes en la interfaz programable se han abordado, y espero que podamos publicar la versión 1.0 de Syndie más adelante este mes.

¿Acabo de decir "1.0"? ¡Claro que sí! Si bien Syndie 1.0 será una aplicación basada en texto, y ni siquiera alcanzará la usabilidad de otras aplicaciones de texto comparables (como mutt o tin), proporcionará toda la gama de funcionalidades, permitirá estrategias de sindicación basadas en HTTP y en archivos y, con suerte, demostrará a los posibles desarrolladores las capacidades de Syndie.

Por ahora, estoy planificando tentativamente un lanzamiento de Syndie 1.1 (permitiendo que la gente organice mejor sus archivos y hábitos de lectura) y quizá una versión 1.2 para integrar algo de funcionalidad de búsqueda (tanto búsquedas simples como quizá búsquedas de texto completo de lucene). Syndie 2.0 probablemente será la primera versión con interfaz gráfica de usuario (GUI), y el complemento para el navegador llegará con la 3.0. El soporte para archivos adicionales y redes de distribución de mensajes llegará cuando se implementen, por supuesto (freenet, mixminion/mixmaster/smtp, opendht, gnutella, etc).

Me doy cuenta, no obstante, de que Syndie 1.0 no será el gran revulsivo que algunos quieren, ya que las aplicaciones basadas en texto son realmente para los geeks, pero me gustaría intentar romper con el hábito de ver "1.0" como una versión final y, en su lugar, considerarla un comienzo.

* 5) Distributed version control

Hasta ahora, he estado trasteando con subversion como el vcs (sistema de control de versiones) para Syndie, aunque en realidad solo domino CVS y clearcase. Esto se debe a que estoy sin conexión la mayor parte del tiempo y, incluso cuando estoy en línea, la conexión por marcación (dialup) es lenta, así que las funciones locales de diff/revert/etc de subversion me han sido bastante útiles. Sin embargo, ayer void me sugirió que exploráramos en su lugar uno de los sistemas distribuidos.

Les eché un vistazo hace unos años al evaluar sistemas de control de versiones para I2P, pero los descarté porque no necesitaba su funcionalidad sin conexión (entonces tenía buen acceso a Internet), así que no valía la pena aprenderlos. Ya no es así, así que ahora los estoy considerando un poco más.

- From what I can see, darcs, monotone, and codeville are the top

candidatos, y el VCS (sistema de control de versiones) basado en parches de darcs parece particularmente atractivo. Por ejemplo, puedo hacer todo mi trabajo localmente y simplemente subir con scp los diffs comprimidos con gzip y cifrados con gpg a un directorio de Apache en dev.i2p.net, y la gente puede contribuir sus propios cambios publicando sus diffs comprimidos con gzip y cifrados con gpg en ubicaciones de su elección. Cuando llegue el momento de etiquetar una versión, haría un darcs diff que especifica el conjunto de parches incluidos en la versión y subiría ese diff en .gz/.gpg como los demás (además de publicar los archivos tar.bz2, .exe y .zip reales, por supuesto ;)

Y, como detalle especialmente interesante, estos archivos diff comprimidos con gzip o cifrados con gpg pueden publicarse como adjuntos en mensajes de Syndie, permitiendo que Syndie se autoaloje.

¿Alguien tiene experiencia con estos cacharros? ¿Algún consejo?

* 6) ???

Solo 24 pantallas de texto esta vez (incluida la publicación del foro) ;) Lamentablemente no pude asistir a la reunión, pero, como siempre, me encantaría saber de ustedes si tienen ideas o sugerencias - simplemente publiquen en la lista, en el foro o pásense por IRC.

=jr
