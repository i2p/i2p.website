---
title: "Reunión de desarrolladores de I2P - 01 de junio de 2004"
date: 2004-06-01
author: "duck"
description: "Registro de la reunión de desarrollo de I2P del 01 de junio de 2004."
categories: ["meeting"]
---

## Resumen rápido

<p class="attendees-inline"><strong>Presentes:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Registro de la reunión

<div class="irc-log"> [22:59] &lt;duck&gt; mar jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; ¡Hola a todos! [23:00] &lt;mihi&gt; Hola, duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; mi propuesta: [23:00] * Masterboy se ha unido a #i2p

[23:00] <duck> 1) progreso del código
[23:00] <duck> 2) contenido destacado
[23:00] <duck> 3) estado de la red de pruebas
[23:00] <duck> 4) recompensas
[23:00] <duck> 5) ???
[23:00] <Masterboy> hola:)
[23:00] <duck> .
[23:01] <duck> como jrandom está ausente, nos tocará hacerlo nosotros mismos
[23:01] <duck> (sé que está registrando y verificando nuestra independencia)
[23:01] <Masterboy> no hay problema:P
[23:02] <duck> a menos que haya problemas con la agenda, propongo que nos ciñamos a ella
[23:02] <duck> aunque no hay mucho que pueda hacer si no lo hacen :)
[23:02] <duck> .
[23:02] <mihi> ;)
[23:02] <duck> 1) progreso del código
[23:02] <duck> no se ha enviado mucho código a cvs
[23:02] <duck> gané el trofeo esta semana: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus todavía no tiene cuenta de cvs
[23:03] <Masterboy> ¿y quién envió algo?
[23:03] <duck> ¿alguien está programando algo en secreto?
[23:03] * Nightblade se ha unido a #I2P

[23:03] <hypercubus> BrianR estaba trabajando en algunas cosas
[23:04] <hypercubus> tengo quizá un 20% del instalador 0.4 hackeado
[23:04] <duck> hypercubus: si tienes cosas entonces proporciona diffs y $dev hará commit por ti
[23:04] <duck> por supuesto se aplican los estrictos acuerdos de licencia
[23:05] <duck> hypercubus: genial, ¿algún problema / algo que valga la pena mencionar?
[23:06] <hypercubus> aún no, pero probablemente necesite un par de personas de BSD para probar los scripts de shell del preinstalador
[23:06] * duck levanta algunas piedras
[23:06] <Nightblade> ¿es solo de texto?
[23:07] <mihi> duck: ¿Cuál eres tú en duck_trophy.jpg?
[23:07] <mihi> ;)
[23:07] <Nightblade> luckypunk tiene FreeBSD, también mi ISP tiene FreeBSD pero su configuración está algo hecha un lío
[23:07] <Nightblade> me refiero a mi ISP del hosting web, no a Comcast
[23:08] <duck> mihi: el de la izquierda con gafas. wilde es el de la derecha que me entrega el trofeo
[23:08] * wilde saluda
[23:08] <hypercubus> tienes una opción... si tienes Java instalado, puedes omitir por completo el preinstalador...    si no tienes Java instalado puedes ejecutar el preinstalador binario para Linux o el binario para win32 (modo consola), o un    preinstalador genérico en script para *nix (modo consola)
[23:08] <hypercubus> el instalador principal te da la opción de usar modo consola o un modo GUI vistoso
[23:08] <Masterboy> instalaré FreeBSD pronto, así que en el futuro también le daré una oportunidad al instalador
[23:09] <hypercubus> bien, ok... no sabía si alguien más además de jrandom lo estaba usando
[23:09] <Nightblade> en FreeBSD Java se invoca como "javavm" en lugar de "java"
[23:09] <hypercubus> ¿compilado a partir del código fuente de Sun?
[23:09] <mihi> FreeBSD soporta enlaces simbólicos ;)
[23:10] <hypercubus> de todos modos, el preinstalador binario está 100% completo
[23:10] <hypercubus> se compila con gcj a binario nativo
[23:11] <hypercubus> solo te pide el directorio de instalación y te consigue un JRE
[23:11] <duck> w00t
[23:11] <Nightblade> genial
[23:11] <hypercubus> jrandom está empaquetando un JRE personalizado para i2p

[23:12] <deer> <j> .
[23:12] <Nightblade> si instalas java desde la colección de ports de freebsd usas un script envoltorio llamado    javavm
[23:12] <deer> <r> .
[23:12] <hypercubus> de todos modos este cacharro estará casi completamente automatizado
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <r> .
[23:12] <deer> <duck> r: córtalo
[23:12] <deer> <r> .
[23:12] <deer> <m> .
[23:13] <deer> <m> ups, el problema es "Nick change too fast" :(
[23:13] <duck> hypercubus: ¿tienes alguna ETA para nosotros?
[23:14] <deer> <m> ups, el problema es "Nick change too fast" :(
[23:14] <hypercubus> aún espero terminar en menos de un mes, antes de que la 0.4 esté lista para el lanzamiento
[23:14] <hypercubus> aunque por ahora estoy compilando un nuevo SO para mi sistema de desarrollo, así que pasarán un par de días    antes de que vuelva al instalador ;-)
[23:14] <hypercubus> no se preocupen
[23:15] <duck> ok. así que más noticias la próxima semana :)
[23:15] <duck> ¿algún otro trabajo de programación hecho?
[23:15] <hypercubus> con suerte... a menos que la compañía eléctrica me fastidie otra vez
[23:16] * duck se mueve a #2
[23:16] <duck> * 2) contenido destacado
[23:16] <duck> mucho audio en streaming (ogg/vorbis) hecho esta semana
[23:16] <duck> baffled está emitiendo su stream de egoplay y yo también estoy emitiendo un stream
[23:16] <Masterboy> y funciona bastante bien
[23:17] <duck> en nuestro sitio puedes obtener info sobre cómo usarlo
[23:17] <hypercubus> ¿tienes algunas estadísticas aproximadas para nosotros?
[23:17] <duck> si usas un reproductor que no esté listado allí y averiguas cómo usarlo, por favor envíamelo y lo    añadiré
[23:17] <Masterboy> duck, ¿dónde está el enlace al stream de baffled en tu sitio?
[23:17] <Masterboy> :P
[23:17] <duck> hypercubus: 4kB/s va bastante bien
[23:18] <duck> y con ogg no está taaaaan mal
[23:18] <hypercubus> ¿pero eso sigue siendo la velocidad promedio?
[23:18] <duck> mi observación es que ese es el máximo
[23:18] <duck> pero todo es ajuste de configuración
[23:19] <hypercubus> ¿alguna idea de por qué ese parece ser el máximo?
[23:19] <hypercubus> y no hablo solo de streaming aquí
[23:19] <hypercubus> sino de descargas también
[23:20] <Nightblade> ayer estaba descargando algunos archivos grandes (un par de megabytes) desde el servicio de hosting de duck y también estaba obteniendo alrededor de 4kb-5kb
[23:20] <duck> Creo que es el rtt
[23:20] <Nightblade> esas películas de Chips
[23:20] <hypercubus> 4-5 parece una mejora sobre los ~3 que he obtenido de forma consistente desde que empecé a usar i2p

[23:20] &lt;Masterboy&gt; 4-5kb no está mal..
[23:20] &lt;duck&gt; con un windowsize de 1 no consigues mucha más velocidad..
[23:20] &lt;duck&gt; recompensa por windowsize&gt;1: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: ¿quizá puedas comentar?
[23:21] &lt;hypercubus&gt; pero son 3 kbps sorprendentemente constantes
[23:21] &lt;mihi&gt; ¿sobre qué? windowsize&gt;1 con ministreaming: eres un mago si logras eso ;)
[23:21] &lt;hypercubus&gt; sin saltos en el medidor de ancho de banda... una línea bastante suave
[23:21] &lt;duck&gt; mihi: sobre por qué es tan estable a 4kb/s
[23:21] &lt;mihi&gt; ni idea. no oigo ningún sonido :(
[23:22] &lt;duck&gt; mihi: para todas las transferencias de i2ptunnel
[23:22] &lt;Masterboy&gt; mihi necesitas configurar el plugin de streaming Ogg..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; no, no hay límite dentro de i2ptunnel respecto a la velocidad. debe de estar en el router...
[23:23] &lt;duck&gt; mi razonamiento: tamaño máximo de paquete: 32kB, rtt de 5 segundos: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; suena plausible
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; otro contenido:
[23:25] * hirvox se ha unido a #i2p

[23:25] <duck> hay un nuevo eepsite de Naughtious
[23:25] <duck> anonynanny.i2p
[23:25] <duck> la clave se ha enviado a CVS y la puso en el wiki de ugha
[23:25] * mihi está escuchando "sitting in the ..." - duck++
[23:25] <Nightblade> ve si puedes abrir dos o tres streams a una velocidad de 4kb, entonces podrás saber si    está en el router o en la biblioteca de streaming
[23:26] <duck> Naughtious: ¿estás ahí? cuenta algo sobre tu plan :)
[23:26] <Masterboy> he leído que ofrece hosting
[23:26] <duck> Nightblade: probé 3 descargas paralelas desde baffled y obtuve 3-4kB cada una
[23:26] <Nightblade> ya veo
[23:27] <mihi> Nightblade: ¿cómo puedes saber eso entonces?
[23:27] * mihi le gusta escuchar en modo "stop&go" ;)
[23:27] <Nightblade> bueno, si hay algún tipo de limitación en el router que solo le permita manejar 4kb a la vez
[23:27] <Nightblade> o si es otra cosa
[23:28] <hypercubus> ¿alguien puede explicar este sitio anonynanny? no tengo un router i2p en ejecución en este momento
[23:28] <mihi> hypercubus: solo un wiki o algo así
[23:28] <duck> configuración de CMS Plone, creación de cuentas abierta
[23:28] <duck> permite subir archivos y cosas de sitios web
[23:28] <duck> a través de la interfaz web
[23:28] <Nightblade> otra cosa que hacer sería probar el rendimiento del "repliable datagram" (datagrama replicable), que por lo que sé    es lo mismo que los streams pero sin ACKs (confirmaciones)
[23:28] <duck> probablemente muy parecido a Drupal
[23:28] <hypercubus> sí, ya he ejecutado Plone antes
[23:29] <duck> Nightblade: he estado pensando en usar airhook para gestionar eso
[23:29] <duck> pero hasta ahora solo algunas ideas básicas
[23:29] <hypercubus> ¿vale cualquier cosa para el contenido del wiki, o se centra en algo en particular?
[23:29] <Nightblade> creo que airhook está bajo GPL
[23:29] <duck> el protocolo
[23:29] <duck> no el código
[23:29] <Nightblade> ah :)
[23:30] <duck> hypercubus: quiere contenido de calidad, y te deja proporcionarlo :)
[23:30] <Masterboy> sube el mejor pr0n de ti mismo que tengas hyper;P
[23:30] <duck> ok
[23:30] * Masterboy intentará hacer eso también
[23:30] <hypercubus> sí, cualquiera que tenga un wiki abierto está pidiendo contenido de calidad ;-)
[23:31] <duck> ok
[23:31] * duck pasa al #3
[23:31] <duck> * 3) estado de la red de pruebas
[23:31] <Nightblade> Airhook maneja con elegancia redes intermitentes, no confiables o con retrasos  <-- jeje no es una    descripción optimista de I2P!
[23:31] <duck> ¿cómo ha ido?
[23:32] <duck> dejemos la discusión sobre datagram sobre i2p para el final
[23:32] <tessier> me encanta ir por wikis abiertos y enlazar esto: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook es excelente
[23:32] <tessier> también lo he estado mirando para construir una red P2P.
[23:32] <Nightblade> me parece confiable (#3)
[23:32] <Nightblade> lo mejor que he visto hasta ahora
[23:33] <duck> sí
[23:33] <mihi> funciona bien, al menos para streaming de audio en stop&go
[23:33] <duck> veo tiempos de actividad bastante impresionantes en IRC
[23:33] <hypercubus> de acuerdo... estoy viendo muchos más "azules" en la consola de mi router
[23:33] <Nightblade> mihi: ¿estás escuchando techno? :)
[23:33] <duck> pero es difícil saberlo porque bogobot no parece manejar conexiones que pasan de las 00:00
[23:33] <tessier> el streaming de audio me funciona muy bien, pero cargar sitios web a menudo requiere varios intentos
[23:33] <Masterboy> tengo la opinión de que i2p funciona muy bien después de 6 horas de uso; en la 6.ª hora usé el IRC    durante 7 horas y así mi router estuvo funcionando 13 horas
[23:33] <duck> (*pista*)
[23:34] <hypercubus> duck: eh... jeje
[23:34] <hypercubus> supongo que podría arreglar eso
[23:34] <hypercubus> ¿tienes el registro configurado como diario?
[23:34] <duck> hypercubus++
[23:34] <hypercubus> la rotación de logs, digo
[23:34] <duck> oh sí
[23:34] <duck> duck--
[23:34] <hypercubus> por eso
[23:34] <Nightblade> estuve en el trabajo todo el día, encendí mi computadora, inicié i2p y estaba en el servidor IRC de duck    en solo unos minutos
[23:35] <duck> he estado viendo algunos DNFs raros
[23:35] <duck> incluso al conectarme a mis propios eepsites
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> creo que eso es lo que causa la mayoría de los problemas ahora
[23:35] <hypercubus> bogoparser solo analizará tiempos de actividad que ocurran completamente dentro de un único logfile... así que si el    logfile abarca solo 24 horas, nadie aparecerá como conectado por más de 24 horas
[23:35] <duck> Masterboy y ughabugha también lo tuvieron, creo...
[23:36] <Masterboy> sí
[23:36] <duck> (¡arréglalo y ganarás el trofeo de la próxima semana seguro!)
[23:37] <deer> <mihi> ¿bogobot está emocionado? ;)
[23:37] <Masterboy> probé mi sitio web y a veces cuando pulso refrescar toma la otra ruta? y tengo que    esperar a que cargue pero nunca espero ;P le doy de nuevo y aparece al instante
[23:37] <deer> <mihi> ups, perdón. olvidé que esto está puenteado...
[23:38] <duck> Masterboy: ¿los timeouts duran 61 segundos?
[23:39] <duck> mihi: bogobot configurado a rotaciones semanales ahora
[23:39] * mihi ha salido de IRC ("adiós, y que tengas una buena reunión")
[23:40] <Masterboy> perdón, no lo verifiqué en mi sitio web; cuando no puedo acceder al instante, simplemente pulso refrescar    y carga al instante..
[23:40] <duck> hm
[23:40] <duck> bueno, hay que arreglarlo
[23:41] <duck> .... #4
[23:41] <Masterboy> creo que la ruta no se da igual cada vez
[23:41] <duck> * 4) recompensas
[23:41] <duck> Masterboy: las conexiones locales deberían cortarse antes
[23:42] <duck> wilde tenía algunas ideas sobre recompensas... ¿estás ahí?
[23:42] <Masterboy> quizá sea un bug de selección de pares
[23:42] <wilde> no estoy seguro de que eso fuera realmente para la agenda
[23:42] <duck> oh
[23:42] <wilde> ok, pero las ideas eran algo como:
[23:42] <Masterboy> creo que cuando salgamos al público el sistema de recompensas funcionará mejor
[23:43] <Nightblade> masterboy: sí, hay dos tunnels por cada conexión, o así lo entiendo    por leer el router.config
[23:43] <wilde> podríamos usar este mes para hacer algo de pequeña publicidad de i2p y aumentar un poco el fondo de recompensas
[23:43] <Masterboy> veo que el proyecto Mute va bien: consiguieron 600$ y aún no han programado mucho ;P
[23:44] <wilde> dirigirnos a comunidades por la libertad, gente cripto, etc.
[23:44] <Nightblade> no creo que jrandom quiera publicidad
[23:44] <wilde> no atención pública de Slashdot, no
[23:44] <hypercubus> eso es lo que yo también he observado
[23:44] <Masterboy> quiero impulsarlo otra vez: cuando lo hagamos público el sistema funcionará mucho mejor ;P
[23:45] <wilde> Masterboy: las recompensas podrían acelerar el desarrollo de myi2p, por ejemplo
[23:45] <Masterboy> y como dijo jr, nada de público hasta 1.0 y solo algo de atención después de 0.4
[23:45] <Masterboy> *escribió
[23:45] <wilde> cuando tengamos como $500+ para una recompensa, la gente podría realmente sobrevivir algunas semanas
[23:46] <hypercubus> lo complicado es que, incluso si apuntamos a una comunidad de desarrolladores pequeña, como *cof* los devs de Mute, esa    gente podría difundir la noticia sobre i2p más de lo que nos gustaría
[23:46] <Nightblade> alguien podría hacer carrera arreglando bugs de i2p
[23:46] <hypercubus> y demasiado pronto
[23:46] <wilde> los enlaces a i2p ya están en muchos lugares públicos
[23:46] <Masterboy> buscas en Google y puedes encontrar i2p

[23:47] <hypercubus> lugares públicos poco visibles ;-) (vi el enlace de i2p en un freesite (sitio en Freenet)... tuve suerte de que el maldito freesite    siquiera cargara!)
[23:47] <wilde> http://en.wikipedia.org/wiki/I2p
[23:47] <Masterboy> pero estoy de acuerdo en que nada de publicidad hasta que 0.4 esté listo
[23:47] <Masterboy> ¿qué???????
[23:47] <wilde> http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] <Masterboy> protol0l hace un gran trabajo ;P
[23:48] <Masterboy> ;))))))
[23:48] <hypercubus> buen typo ;-)
[23:48] <wilde> ok, en cualquier caso, estoy de acuerdo en que deberíamos mantener I2P en privado (jr lee este registro ;)
[23:49] <Masterboy> ¿quién hizo eso?
[23:49] <Masterboy> creo que la discusión del equipo de Freenet atrajo más atención..
[23:50] <Masterboy> y que jr discutiendo con toad le da mucha información al gran público..
[23:50] <Masterboy> así que, como en el wiki de ughas, todos podemos culpar a jr por eso ;P
[23:50] <wilde> ok, en cualquier caso, veremos si podemos traer algo de $ sin atraer a /.
[23:50] <Masterboy> de acuerdo
[23:50] <hypercubus> la lista de desarrolladores de Freenet difícilmente es lo que yo llamo el "gran público" ;-)
[23:50] <wilde> .
[23:51] <hypercubus> wilde: tendrás mucho $ antes de lo que crees ;-)
[23:51] <wilde> oh vamos, hasta mi madre está suscrita a freenet-devl
[23:51] <duck> mi madre lo lee a través de gmame
[23:51] <deer> <clayboy> freenet-devl se enseña en las escuelas aquí
[23:52] <wilde> .
[23:52] <Masterboy> así que veremos más recompensas después de que 0.4 sea estable..
[23:53] <Masterboy> es decir, dentro de 2 meses ;P
[23:53] <wilde> ¿adónde se fue ese duck?
[23:53] <duck> gracias wilde  
[23:53] <hypercubus> aunque, como el único reclamante de la recompensa hasta ahora, debo decir que el dinero de la recompensa no    influyó en mi decisión de aceptar el desafío
[23:54] <wilde> jeje, lo haría si hubiera sido 100x
[23:54] <duck> eres demasiado bueno para el mundo
[23:54] <Nightblade> jaja
[23:54] * duck se mueve a #5
[23:54] <hypercubus> wilde, $100 no significan una mierda para mí ;-)
[23:54] <duck> 100 * 10 = 1000
[23:55] * duck hace pop ("5 airhook")
[23:55] <duck> tessier: ¿tienes alguna experiencia en el mundo real con eso?
[23:55] <duck> (http://www.airhook.org/)
[23:55] * Masterboy va a probar esto :P
[23:56] <duck> implementación en Java (no sé si siquiera funciona) http://cvs.ofb.net/airhook-j/
[23:56] <duck> implementación en Python (un lío, funcionó en el pasado) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck abre la válvula del despotrique
[23:58] <Nightblade> la de Java también es GPL
[23:58] <duck> llévalo a dominio público
[23:58] <hypercubus> amén
[23:58] <Nightblade> toda la documentación del protocolo tiene solo unas 3 páginas: no puede ser tan difícil
[23:59] <Masterboy> nada es difícil
[23:59] <Masterboy> solo que no es fácil
[23:59] <duck> no creo que esté completamente especificado, eso sí
[23:59] * hypercubus le quita a masterboy sus galletas de la fortuna
[23:59] <duck> podrías necesitar sumergirte en el código C para una implementación de referencia
[00:00] <Nightblade> yo lo haría, pero ahora estoy ocupado con otras cosas de i2p
[00:00] <Nightblade> (y también con mi trabajo a tiempo completo)
[00:00] <hypercubus> duck: ¿quizá una recompensa por eso?
[00:00] <Nightblade> ya la hay
[00:00] <Masterboy> ?
[00:00] <Masterboy> ahh Pseudonyms
[00:00] <duck> se podría usar a 2 niveles
[00:00] <duck> 1) como un transporte además de TCP
[00:01] <duck> 2) como un protocolo para manejar datagramas dentro de i2cp/sam
[00:01] <hypercubus> eso merece una consideración seria entonces
[00:01] <hypercubus> </obvious>

[00:02] &lt;Nightblade&gt; duck: me di cuenta de que el repliable datagram (datagrama al que se puede responder) en SAM tiene un tamaño máximo de 31kb, mientras que el    stream tiene un tamaño máximo de 32kb, lo que me hace pensar que el destino del remitente se envía con cada paquete en    modo de repliable datagram, y solo al principio en el modo de stream - [00:02] &lt;Masterboy&gt; bueno, el cvs de airhook no está muy actualizado.. [00:03] &lt;Nightblade&gt; lo que me hace pensar que sería ineficiente construir un protocolo encima de los    repliable datagrams a través de SAM [00:03] &lt;duck&gt; el tamaño de los mensajes de airhook es de 256 bytes; el de I2CP es de 32kb, así que al menos tienes que cambiar un poco [00:04] &lt;Nightblade&gt; en realidad, si quisieras hacer el protocolo en SAM podrías usar simplemente el datagrama anónimo    y hacer que el primer paquete contenga el destino del remitente.... bla bla bla - tengo muchas ideas pero no    suficiente tiempo para programarlas [00:06] &lt;duck&gt; de nuevo, tienes problemas para verificar firmas [00:06] &lt;duck&gt; así que alguien podría enviarte paquetes falsos [00:06] &lt;Masterboy&gt; tema:::: SAM [00:06] &lt;Masterboy&gt; ;P [00:07] &lt;Nightblade&gt; cierto [00:08] &lt;Nightblade&gt; pero si respondieras a ese destino y no hubiera acuse de recibo sabrías que era    un impostor [00:08] &lt;Nightblade&gt; tendría que haber un handshake (intercambio inicial) [00:08] &lt;duck&gt; pero para eso necesitarás handshakes a nivel de aplicación [00:08] &lt;Nightblade&gt; no, no realmente [00:09] &lt;Nightblade&gt; solo ponlo en una biblioteca para acceder a SAM [00:09] &lt;Nightblade&gt; esa es una mala manera de hacerlo, aunque [00:09] &lt;Nightblade&gt; hacerlo, aunque [00:09] &lt;duck&gt; también podrías usar tunnels separados [00:09] &lt;Nightblade&gt; debería estar en la biblioteca de streaming [00:11] &lt;duck&gt; sí. tiene sentido [00:12] &lt;duck&gt; ok [00:12] &lt;duck&gt; me siento con ganas de *baff* [00:13] &lt;Nightblade&gt; ja [00:13] * duck *baffs* </div>
