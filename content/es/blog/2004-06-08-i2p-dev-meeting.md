---
title: "Reunión de desarrolladores de I2P - 8 de junio de 2004"
date: 2004-06-08
author: "duck"
description: "Acta de la reunión de desarrollo de I2P del 08 de junio de 2004."
categories: ["meeting"]
---

## Resumen rápido

<p class="attendees-inline"><strong>Presentes:</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## Registro de la reunión

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; hora de la reunión 21:02:33 &lt;duck&gt; el informe está en http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; pero cometí un error en la numeración 21:02:45 &lt;duck&gt; así que se saltará el primer punto 5 21:02:53 &lt;hypercubus&gt; ¡bien! 21:03:03  * duck pone un poco de hielo en su cerveza 21:03:14  * mihi renombraría el primer #5 a #4 ;) 21:03:27 &lt;hypercubus&gt; nah, mejor tengamos dos puntos 4 la próxima semana ;-) 21:03:37  * duck renombra 'hypercubus' a 'mihi' 21:03:48 &lt;hypercubus&gt; ¡bien! 21:03:49 &lt;duck&gt; ok 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; ¿hay un Nightblade en el canal? 21:04:39 &lt;duck&gt; (inactivo     : 0 días 0 horas 0 mins 58 segs) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck recupera el micrófono 21:06:15 &lt;duck&gt; Nightblade escribió una biblioteca SAM para C / C++ 21:06:23 &lt;duck&gt; me compila... pero eso es todo lo que puedo decir :) 21:06:37 &lt;mihi&gt; ¿no hay casos de prueba? ;) 21:07:06 &lt;duck&gt; si hay algún usuario de rFfreebsd, Nightblade podría estar interesado en ustedes 21:07:08 &lt;ugha_node&gt; Las llamadas a strstr en el código realmente me molestaron. ;) 21:07:27 &lt;ugha_node&gt; duck: ¿Qué es un rFfreebsd? 21:07:42 &lt;duck&gt; así es como escribí freebsd 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; Qué lástima que -F no funcione con rm. 21:08:30 &lt;duck&gt; ugha_node: tiene licencia bsd; así que arréglalo 21:08:41 &lt;fvw&gt; me suena sensato :). Por desgracia desinstalé mi última máquina freebsd hace un tiempo. Yo                  tengo cuentas en máquinas de otras personas, y estoy dispuesto a ejecutar casos de prueba. 21:08:43 &lt;ugha_node&gt; duck: Puede que lo haga. :) 21:08:50 &lt;duck&gt; (malditos hippies de BSD) 21:09:09 &lt;duck&gt; oh, agradable y breve, frank 21:09:17 &lt;duck&gt; ¿Más comentarios sobre libsam? 21:09:49 &lt;duck&gt; fvw: Supongo que Nightblade se pondrá en contacto contigo si lo necesita 21:09:50  * fvw refunfuña por el comportamiento perfectamente sensato de unix al matar su cliente de irc. 21:10:02 &lt;duck&gt; pero dado que su correo tenía una semana, puede que ya haya encontrado algo 21:10:17 &lt;mihi&gt; fvw: ? 21:10:24 &lt;fvw&gt; sí, si alguien quería aceptar mi ofrecimiento, como que me lo perdí. Siéntanse                  libres de enviar un correo o algo así. 21:10:42  * duck salta al #2 21:10:46 &lt;hypercubus&gt; ehm, ¿a dónde? ;-) 21:10:54 &lt;duck&gt; 2) navegar i2p y la web normal con un solo navegador 21:10:57 &lt;fvw&gt; instalación reciente, todavía no le he dicho a mi zsh que no haga hup a cosas en segundo plano.                  &lt;/offtopic&gt;

21:11:09 &lt;fvw&gt; hypercubus: Estoy en la lista pública de correo de usuarios, creo. fvw.i2p@var.cx
21:12:11 &lt;duck&gt; hubo algunas cosas sobre añadir todos los TLD a la lista de exclusiones del proxy de tu navegador
21:12:23 &lt;fvw&gt; ¿eso requiere discusión? Creo que ya se trató bastante en la                  lista de correo.
21:12:24 &lt;duck&gt; Creo que es un hack sucio
21:12:36 &lt;fvw&gt; sí, eso se mencionó. Bienvenido de nuevo.
21:12:47 &lt;duck&gt; fvw: No leí el hilo :)
21:13:12 &lt;duck&gt; ok, si no quieres discutirlo, pasa al #3
21:13:19 &lt;duck&gt; * 3) canal de chat
21:13:23 &lt;hypercubus&gt; El script de cervantes funciona perfectamente en Konqueror 3.2.2, Firefox 0.8 y                         Opera 7.51, todos para Gentoo con KDE 3.2.2
21:13:39  * mihi coloca una bandera en el #4
21:13:55 &lt;duck&gt; #i2p-chat es un canal alternativo aquí para chat fuera de tema y soporte ligero
21:14:08 &lt;duck&gt; No sé quién lo registró
21:14:12 &lt;hypercubus&gt; yo lo hice
21:14:17 &lt;duck&gt; así que mejor ten cuidado :)
21:14:22 &lt;fvw&gt; ehm, no hay #4, solo dos #5 :)
21:14:33 &lt;hypercubus&gt; con suerte me acordaré de la contraseña cuando la necesite ;-)
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Canal: #i2p-chat
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Contacto: hypercubus &lt;&lt;ONLINE&gt;&gt;

21:14:33 &lt;mihi&gt; [22:27] -ChanServ-    Alternativo: cervantes &lt;&lt;ONLINE&gt;&gt; 21:14:37 &lt;mihi&gt; [22:27] -ChanServ-   Registrado: hace 4 días (0h 2m 41s) 21:15:12 &lt;hypercubus&gt; le di poderes de op a algunas personas de confianza para cuando no esté y haya problemas 21:15:24 &lt;duck&gt; suena bien 21:15:39 &lt;duck&gt; puede que sea un poco excesivo 21:15:51 &lt;hypercubus&gt; nunca se sabe en IRC ;-) 21:15:55 &lt;duck&gt; pero después de que protogirl entró aquí pensé que sería bueno limpiar este canal 21:16:03 &lt;hypercubus&gt; je 21:16:27 &lt;hypercubus&gt; de todos modos lo necesitaremos seguro en algún momento en los próximos meses 21:16:34 &lt;duck&gt; jups 21:16:48 &lt;duck&gt; y entonces la gente de freenode nos expulsará  21:16:55 &lt;hypercubus&gt; ;-) 21:17:13 &lt;duck&gt; no les gusta nada que no esté escrito en su kampf 21:17:16 &lt;duck&gt; ejem 21:17:44  * duck pasa a $nextitem y dispara el breakpoint de mihi 21:17:47 &lt;hypercubus&gt; pensé que vincular el canal nuevo con soporte lo legitimaría para freenode 21:18:47 &lt;duck&gt; hypercubus: podrías sorprenderte 21:19:04 &lt;hypercubus&gt; *tos* admito que no leí todas las políticas... 21:19:24 &lt;duck&gt; es ruleta rusa 21:19:39 &lt;hypercubus&gt; hmm, no pensé que fuera tan grave 21:19:52  * duck está siendo negativo 21:19:54 &lt;hypercubus&gt; bueno, veré qué podemos hacer 21:20:09 &lt;fvw&gt; perdón, se me debe haber pasado algo. ¿Por qué freenode nos expulsaría? 21:20:21  * duck mira el contador de timeout del breakpoint de mihi 21:20:32 &lt;duck&gt; fvw: se centran en canales de desarrollo 21:20:35 &lt;mihi&gt; ? 21:20:53 &lt;mihi&gt; duck: el breakpoint se activa con /^4).*/ 21:21:01 &lt;duck&gt; mihi: pero no hay #4 21:21:06 &lt;fvw&gt; ¿y? i2p es tan alpha que ahora mismo incluso el soporte es desarrollo. 21:21:11 &lt;fvw&gt; (y no, no puedes citarme en eso) 21:21:36 &lt;duck&gt; fvw: puede que no estés familiarizado con los tipos de discusión que sí ocurrieron en IIP 21:21:38 &lt;hypercubus&gt; sí, pero tenemos *2* canales para ello 21:21:45 &lt;duck&gt; y que probablemente ocurrirán en los canales #i2p 21:22:04 &lt;duck&gt; Estoy bastante seguro de que a freenode no le gusta. 21:22:10 &lt;Nightblade&gt; ahora estoy aquí 21:22:49 &lt;hypercubus&gt; les donaremos una máquina de margaritas o algo así 21:22:49 &lt;mihi&gt; duck: ¿a qué te refieres? ¿a los floods? ¿o a #cl? ¿o qué? 21:23:08 &lt;fvw&gt; ¿discusiones en IIP o discusiones en #iip? Nunca he visto nada aparte de desarrollo y soporte en #iip. Y las discusiones en IIP se moverían a I2P, no a #i2p@freenode. 21:23:09 &lt;duck&gt; todo tipo de charla políticamente incorrecta 21:23:36 &lt;fvw&gt; ¿hay máquinas de margaritas? Oh, yo quiero. 21:23:54 &lt;duck&gt; en fin 21:24:38 &lt;hypercubus&gt; ¿revisamos el 2)? 21:24:58 &lt;duck&gt; hypercubus: ¿qué tienes que añadir sobre el proxy del navegador? 21:25:18 &lt;hypercubus&gt; ups, el número 1... ya que nightblade acaba de honrarnos con su presencia ;-) 21:25:33 &lt;duck&gt; Nightblade: nos tomamos la libertad de 'discutir' libsam 21:25:42 &lt;Nightblade&gt; Ok, diré unas líneas 21:25:48 &lt;hypercubus&gt; pero sí, tenía algo que no se mencionó en la lista sobre lo del navegador también, ahora que lo pienso 21:25:56 &lt;duck&gt; Nightblade: fvw nos dijo que podría ayudar con algunas pruebas en FreeBSD 21:26:20 &lt;fvw&gt; Ya no tengo una máquina FreeBSD, pero tengo cuentas en máquinas FreeBSD; denme casos de prueba y con gusto los ejecuto. 21:27:02 &lt;Nightblade&gt; He empezado a trabajar en un dht en C++, que usa Libsam (C).  Por ahora no he avanzado especialmente aunque he estado trabajando mucho en ello.  ahora mismo los nodos en el dht pueden "pingearse" entre sí a través de un mensaje de datos sam 21:27:09 &lt;Nightblade&gt; en el proceso encontré un par de bugs menores en libsam 21:27:18 &lt;Nightblade&gt; de la cual publicaré una nueva versión en algún momento 21:27:51 &lt;ugha_node&gt; Nightblade: ¿Podrías eliminar esas llamadas a 'strstr' de libsam? :) 21:27:52 &lt;Nightblade&gt; el caso de prueba es: intenta compilarlo y repórtame los errores 21:28:01 &lt;Nightblade&gt; ¿qué tiene de malo strstr 21:28:21 &lt;ugha_node&gt; No está pensado para usarse en lugar de strcmp. 21:28:38 &lt;Nightblade&gt; ah sí, también voy a portar libsam a Windows, pero eso no será en un futuro cercano 21:29:07 &lt;Nightblade&gt; ¿hay algo mal con la forma en que lo estoy usando, aparte de la estética? 21:29:15 &lt;Nightblade&gt; puedes enviarme cambios o decirme qué preferirías hacer 21:29:19 &lt;Nightblade&gt; simplemente me pareció la forma más fácil 21:29:21 &lt;ugha_node&gt; Nightblade: no noté nada. 21:29:32 &lt;fvw&gt; strcmp es más eficiente que strstr, por supuesto. 21:29:36 &lt;ugha_node&gt; Pero solo le eché un vistazo por encima. 21:30:20 &lt;ugha_node&gt; fvw: A veces puedes explotar cosas que usan strstr en lugar de strcmp, pero no es el caso. 21:31:22 &lt;Nightblade&gt; sí, ahora veo algunos lugares donde puedo cambiarlo 21:31:28 &lt;fvw&gt; eso también, pero supongo que lo habrías notado. Bueno, de hecho, tendrías que usar strncmp para prevenir esos exploits. Pero eso es aparte. 21:31:31 &lt;Nightblade&gt; no recuerdo por qué lo hice así 21:31:57 &lt;ugha_node&gt; fvw: de acuerdo. 21:32:27 &lt;Nightblade&gt; oh, ahora recuerdo por qué 21:32:40 &lt;Nightblade&gt; es una forma perezosa de no tener que calcular la longitud para strncmp 21:32:49 &lt;duck&gt; je 21:32:52 &lt;ugha_node&gt; Nightblade: Jeje. 21:33:01 &lt;fvw&gt; usa min(strlen(foo), sizeof(*foo)) 21:33:04 &lt;hypercubus&gt; ¿damos comienzo a los azotes? 21:33:15 &lt;fvw&gt; ¿Pensé que el sexo oral venía primero? *se agacha* 21:33:32 &lt;fvw&gt; bien, siguiente punto, creo. ¿Hypercube tenía un comentario sobre el proxy? 21:33:38 &lt;hypercubus&gt; je 21:33:54 &lt;duck&gt; ¡que venga! 21:34:03 &lt;Nightblade&gt; haré los cambios para la próxima versión - al menos cambiaré algunos 21:34:25 &lt;hypercubus&gt; ok, bueno, esto se discutió brevemente en el canal hace unas semanas, pero creo que merece retomarse 21:34:48 &lt;deer&gt; * Sugadude se ofrece voluntario para realizar el sexo oral. 21:34:59 &lt;hypercubus&gt; en lugar de añadir TLD a la lista de bloqueo de tu navegador, o usar el script del proxy, hay una tercera vía 21:35:29 &lt;hypercubus&gt; que no debería tener las mismas desventajas que los otros dos enfoques en cuanto al anonimato 21:36:17 &lt;fvw&gt; ¿que te contaré por el baratísimo precio de $29.99? ¡Suelta ya! 21:36:27 &lt;hypercubus&gt; y sería hacer que el eeproxy reescriba las páginas HTML entrantes para incrustar la página en un frameset...  21:36:58 &lt;hypercubus&gt; el marco principal contendría el contenido HTTP solicitado, el otro marco serviría como barra de control 21:37:13 &lt;hypercubus&gt; y te permitiría activar/desactivar el proxy a voluntad 21:37:40 &lt;hypercubus&gt; y también te avisaría, quizá mediante bordes de colores o algún otro tipo de alerta, de que estás navegando de forma no anónima 21:37:54 &lt;fvw&gt; ¿cómo vas a evitar que un sitio i2p (con javascript etc) desactive el anonimato? 21:37:59  * duck intenta aplicar tolerancia de nivel-de-habilidad de jrandom 21:37:59 &lt;hypercubus&gt; o que un enlace en una página de eepsite lleve a la RealWeb(tm) 21:38:04 &lt;duck&gt; ¡genial! ¡hazlo! 21:38:16 &lt;fvw&gt; aún tendrás que hacer algo tipo fproxy, o crear algo no controlado por el navegador para el cambio. 21:38:29 &lt;ugha_node&gt; fvw: correcto. 21:39:10 &lt;hypercubus&gt; por eso vuelvo a soltar esto aquí; quizá alguien tenga ideas sobre cómo asegurar esto 21:39:31 &lt;hypercubus&gt; pero en mi opinión esto será algo que la mayoría de los usuarios finales de i2p necesitarán mucho 21:39:33 &lt;hypercubus&gt; *usuarios 21:40:04 &lt;hypercubus&gt; porque los enfoques de TLD/script de proxy/navegador dedicado son demasiado pedirle al usuario general de la red 21:40:29 &lt;fvw&gt; A la larga, creo que un equivalente de fproxy es la mejor idea. Pero eso definitivamente no es una prioridad en mi humilde opinión, y en realidad no creo que navegar sitios vaya a ser la killer app de i2p. 21:40:42 &lt;Sonium&gt; ¿Qué es el netDb, de todos modos? 21:40:59 &lt;duck&gt; Sonium: base de datos de routers conocidos 21:41:10 &lt;hypercubus&gt; fproxy es demasiado engorroso para la mayoría de los usuarios 21:41:32 &lt;Sonium&gt; ¿una base de datos así no compromete el anonimato? 21:41:39 &lt;hypercubus&gt; en mi opinión es parte de la razón por la que freenet nunca prendió en la comunidad no desarrolladora 21:41:41 &lt;fvw&gt; hypercube: no necesariamente. La autoconfiguración de proxy ("pac") puede hacerlo tan simple como rellenar un único valor en la configuración de tu navegador. Creo que no deberíamos subestimar el hecho de que, en el futuro previsible, todos los usuarios de i2p serán al menos ligeramente avispados en lo informático. (toda la evidencia en freenet-support no obstante) 21:42:00 &lt;ugha_node&gt; Sonium: No, los 'malos' podrían recopilar esa información manualmente de todos modos. 21:42:21 &lt;Sonium&gt; pero si NetDb está caído i2p está caído, ¿no? 21:42:29 &lt;fvw&gt; hypercubus: No realmente, creo que el hecho de que no haya funcionado en absoluto desde principios de la 0.5 tiene más culpa de eso. &lt;/offtopic time="once again"&gt;

21:42:44 &lt;fvw&gt; Sonium: puedes tener más de un netdb (cualquiera puede ejecutar uno)
21:42:58 &lt;hypercubus&gt; ya tenemos pac, y aunque funciona de forma espectacular desde el punto de                         vista técnico, en la práctica no va a proteger el anonimato                         del avg. jog
21:43:03 &lt;hypercubus&gt; *avg. joe
21:43:22 &lt;ugha_node&gt; fvw: Err.. Cada router tiene su propio netDb.
21:43:42 &lt;duck&gt; ok. Estoy a punto de desmayarme. asegúrense de *baff* cerrar la reunión cuando                   terminen
21:43:52 &lt;ugha_node&gt; I2P ya no tiene dependencias centrales.
21:44:07 &lt;hypercubus&gt; ok, bueno, solo quería dejar esta idea formalmente en los registros ;-)
21:44:30 &lt;fvw&gt; ugha_node: ok, entonces un netdb publicado. En realidad no ejecuto un nodo (todavía), no                  estoy del todo al día con la terminología.
21:44:34 &lt;ugha_node&gt; Hmm. ¿No quería mihi decir algo?
21:45:05  * fvw le da a duck chocolate con sabor a café para mantenerlo despierto y en marcha un poco            más.
21:45:07 &lt;mihi&gt; no :)
21:45:21 &lt;mihi&gt; ¿duck es un dispositivo de red? ;)
21:45:25 &lt;ugha_node&gt; mihi: Por cierto, ¿vas a tomar la recompensa por aumentar el tamaño de ventana?
21:45:28  * fvw le da a duck chocolate con sabor a alcohol para apagarlo indefinidamente.
21:45:30 &lt;hypercubus&gt; en sueco
21:45:52 &lt;mihi&gt; ugha_node: ¿qué recompensa?
21:46:00 &lt;hypercubus&gt; bien, entonces pasamos al 5), ¿rant-a-rama? ;-)
21:46:13 &lt;ugha_node&gt; mihi: http://www.i2p.net/node/view/224
21:46:27  * duck come un poco del chocolate de fvw
21:47:16 &lt;mihi&gt; ugha_node: definitivamente no; lo siento
21:47:36 &lt;ugha_node&gt; mihi: Uh, ok. :(
21:48:33  * mihi intentó hacer un hack del "viejo" API de streaming hace algún tiempo, pero ese estaba demasiado            lleno de bugs...
21:48:53 &lt;mihi&gt; pero en mi humilde opinión sería más fácil arreglar ese en lugar de arreglar el mío...
21:49:21 &lt;ugha_node&gt; Je.
21:49:42 &lt;hypercubus&gt; tan modesto
21:49:46 &lt;mihi&gt; ya que ya tiene algo de soporte (roto) de "reordering" (reordenamiento)
21:50:49 &lt;Sonium&gt; ¿hay alguna forma de preguntarle a deer cuántas personas hay en el canal i2p-#i2p?
21:51:01 &lt;duck&gt; no
21:51:08 &lt;hypercubus&gt; nop, pero puedo agregar eso a bogobot
21:51:08 &lt;Sonium&gt; :/
21:51:11 &lt;Nightblade&gt; !list
21:51:13 &lt;deer&gt; &lt;duck&gt; 10 personas
21:51:13 &lt;hypercubus&gt; después de que termine el instalador ;-)
21:51:24 &lt;Sonium&gt; !list
21:51:32 &lt;Sonium&gt; o_O
21:51:35 &lt;mihi&gt; Sonium ;)
21:51:38 &lt;ugha_node&gt; ¡Este no es un canal fserv!
21:51:39 &lt;Sonium&gt; ¡era una trampa!
21:51:40 &lt;ugha_node&gt; :)
21:51:41 &lt;hypercubus&gt; debería ser !who
21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown
21:51:48 &lt;cervantes&gt; ups, me perdí la reunión
21:51:57 &lt;ugha_node&gt; !list
21:52:01 &lt;Nightblade&gt; !who
21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom
21:52:17 &lt;mihi&gt; !who !has !the !list ?
21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands
21:52:33 &lt;Nightblade&gt; !ban fvw!*@*
21:52:42 &lt;mihi&gt; !ban *!*@*
21:52:50 &lt;hypercubus&gt; presiento que va a caer el mazo
21:52:51 &lt;duck&gt; suena como un buen momento para cerrarlo
21:52:55 &lt;Sonium&gt; por cierto, también deberías implementar un comando !8 como tiene chanserv
21:52:59 &lt;fvw&gt; bien, ahora que eso está resuelto, vamos a cer.. sí. eso.
21:53:00  * hypercubus es psíquico
21:53:05 &lt;duck&gt; *BAFF*
21:53:11 &lt;Nightblade&gt; !baff
21:53:12 &lt;hypercubus&gt; mi pelo, mi pelo
21:53:24  * fvw señala a hypercube y se ríe. ¡Tu pelo! ¡Tu pelo! </div>
