---
title: "Reunión de desarrollo de I2P, 19 de agosto de 2003"
date: 2003-08-19
author: "jrand0m"
description: "54ª reunión de desarrolladores de I2P sobre actualizaciones del SDK, revisión de I2NP, avances en criptografía y estado del desarrollo"
categories: ["meeting"]
---

<h2 id="quick-recap">Resumen rápido</h2>

<p class="attendees-inline"><strong>Presentes:</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Registro de la reunión</h2>

<div class="irc-log"> --- Registro abierto Tue Aug 19 16:56:12 2003 17:00 -!- logger [logger@anon.iip] se ha unido a #iip-dev 17:00 -!- Tema de #iip-dev: Reuniones semanales de desarrollo de IIP y otras 	 conversaciones entre desarrolladores se realizan aquí. 17:00 [Usuarios #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: #iip-dev: Total de 15 nicks [0 ops, 0 halfops, 0 voices, 15 normales] 17:00 -!- Irssi: La unión a #iip-dev se sincronizó en 7 s 17:00 < hezekiah> ¡Muy bien! :) 17:00 < hezekiah> Ambos loggers están en su lugar. :) 17:01 < thecrypto> ¡yah! 17:03 < hezekiah> Hmmm ... 17:03 < hezekiah> Se suponía que esta reunión empezaba hace 3 minutos. 17:03 < hezekiah> Me pregunto qué pasa. 17:04 < thecrypto> bueno, quién está inactivo 17:04 < hezekiah> jrand0m ni siquiera está en línea. 17:04 < hezekiah> nop ha estado inactivo 15 minutos. 17:05 < nop> hola 17:05 < nop> perdón 17:05 < nop> Estoy súper ocupado en el trabajo 17:05 < mihi> [22:36] * jrand0m se va a cenar pero volveré dentro de 	 media hora para la reunión 17:05 -!- jrand0m [~jrandom@anon.iip] se ha unido a #iip-dev 17:05 < hezekiah> Hola, jrand0m. 17:05 < nop> hola 17:05 < nop> ok, aquí está la cosa 17:05 < nop> No puedo ser visto en IIP en el trabajo ahora mismo 17:05 < nop> así que me pondré al día con ustedes más tarde 17:05 < nop> me llamaron la atención por eso ayer 17:05 < nop> así que 17:05 < hezekiah> Adiós, nop. 17:05 < thecrypto> bye 17:06 < nop> Me quedaré en el canal 17:06 < nop> solo que no será obvio :) 17:06 < hezekiah> ¿jrand0m? Como tú eres quien más habla estos días, ¿hay 	 algo que quieras en la agenda para esta reunión? 17:07 < jrand0m> de vuelta 17:08 < jrand0m> ok, la pasta al pesto estaba buena. 17:08 < jrand0m> déjame sacar las cosas tipo agenda 17:09 -!- Lookaround [~chatzilla@anon.iip] se ha unido a #iip-dev 17:09 < jrand0m> x.1) modificaciones al i2cp SDK x.2) revisión de i2np x.3) transporte HTTP con polling x.4) estado de desarrollo x.5) por hacer x.6) plan para las próximas dos semanas 17:09 < jrand0m> (pon la x en el número de la agenda donde encaje) 17:10 < thecrypto> tú eres la agencda 17:10 < hezekiah> jrand0m: no tengo nada que decir, y nop puede 17:10 < hezekiah> no puede hablar. 17:10 < jrand0m> lol 17:10 < hezekiah> Lo más probable es que UserX no añada nada (normalmente 	 no lo hace), así que por mí es todo tuyo. :0 17:10 < hezekiah> :) 17:10 < jrand0m> 'k.  ¿estamos registrando? 17:10 < jrand0m> je 17:10 < hezekiah> Estoy registrando todo. 17:10 < jrand0m> genial.  ok.  0.1) bienvenidos. 17:10 < jrand0m> hola. 17:11 < jrand0m> 0.2) lista de correo 17:11 < jrand0m> la lista está caída por el momento, vuelve lo antes posible.  lo sabrán cuando esté :) 17:11 < jrand0m> mientras tanto, wiki o usa iip para conversar. 17:11 < jrand0m> 1.1) modificaciones al i2cp SDK 17:12 < jrand0m> El SDK se ha actualizado con algunas correcciones de errores, además se han introducido algunas cosas nuevas en la 	 especificación. 17:12 < jrand0m> Ayer publiqué en la lista con la información. 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> ¿alguna pregunta sobre lo que publiqué, 	 o ideas sobre un plan para implementar los cambios?  (¿u otras alternativas que 	 no haya considerado?) 17:13 < hezekiah> He estado corriendo como pollo sin cabeza 	 preparándome para la universidad. 17:13 < jrand0m> vale, entendido. 17:13 < hezekiah> Le eché un vistazo superficial a lo que escribiste, pero aún no he 	 mirado los cambios a la especificación. 17:13 < jrand0m> apenas nos queda más de tu tiempo, ¿no...? 17:13 < hezekiah> No hasta que llegue a la universidad. 17:14 < hezekiah> Una vez que llegue, probablemente no se sepa de mí durante al 	 menos una semana mientras me adapto. 17:14 < jrand0m> y una vez que llegues tendrás mucho que acomodarte 	 (si mal no recuerdo de cuando fui a la escuela ;) 17:14 < jrand0m> je, eso. 17:14 < hezekiah> Para entonces, debería ser un poco más eficiente y tener 	 más tiempo para poder programar. 17:14 < jrand0m> genial 17:14 < thecrypto> yo solo estoy haciendo criptografía, así que las estructuras de datos son mi real 	 preocupación; una vez que tenga el modo CTS listo, probablemente me ponga a trabajar en eso 17:14 < hezekiah> En fin, esa es mi suposición. 17:14 < jrand0m> genial, thecrypto 17:15 < jrand0m> ok, lo bueno es que el SDK funciona perfectamente (con 	 los bugs que encontró mihi corregidos [¡yay mihi!]) sin la actualización a la especificación. 17:15 -!- arsenic [~none@anon.iip] se ha unido a #iip-dev 17:16 < jrand0m> ok, pasemos a 1.2) revisión de i2np 17:16 < jrand0m> ¿alguien leyó el documento? 17:16 < jrand0m> ;) 17:16 < hezekiah> Yo no, todavía. 17:16 < hezekiah> Como dije, ahora mismo soy un pollo sin cabeza. 17:17 < hezekiah> Por cierto, jrand0m, parece que te gusta enviar PDFs. 17:17 < jrand0m> ¿todos pueden leer OpenOffice .swx? 17:17 < hezekiah> Yo sí. 17:17 < jrand0m> [si es así, enviaré swx] 17:17 -!- abesimpson [~k@anon.iip] se ha unido a #iip-dev 17:17 < thecrypto> yo puedo 17:17 < hezekiah> No puedo buscar texto en un PDF con KGhostView. 17:17 < hezekiah> Así que eso duele de verdad. 17:17 < jrand0m> eso apesta, hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] se ha unido a #iip-dev 17:17 < hezekiah> La versión para Linux de Adobe Acrobat tampoco es muy amigable. 17:18 < jrand0m> ok, será formato OpenOffice en lugar de PDF. 17:18 < hezekiah> Genial. 17:18 < jrand0m> eh, ok.  i2np tiene algunos cambios menores en la estructura 	 LeaseSet (reflejando el cambio de i2cp publicado antes), pero por lo demás, 	 está en gran medida listo. 17:19 < hezekiah> jrand0m: ¿Todos estos documentos están en el CVS de cathedral? 17:19 < nop> oh 17:19 < nop> ¿puedo intervenir? 17:19 < hezekiah> es decir, copias de los archivos PDF que has estado enviando a la 	 lista, etc. 17:19 < hezekiah> nop: Adelante. 17:19 < nop> esto está fuera de tema pero es importante 17:19 -!- ChZEROHag [hag@anon.iip] se ha unido a #iip-dev 17:19 < nop> IIP-dev y el correo están un poco raros ahora mismo 17:19 < hezekiah> Me di cuenta. 17:19 < nop> así que tengan paciencia con nosotros por un rato 17:20 < nop> estamos tratando de ponerlo en marcha 17:20 < nop> pero tiene SpamAssassin integrado 17:20 < nop> lo cual son buenas noticias 17:20 < nop> :) 17:20 < nop> y muchas otras funciones 17:20 < jrand0m> ¿alguna estimación, nop, para la lista? 17:20  * ChZEROHag asoma la nariz 17:20 < jrand0m> (sé que estás ocupado, no es fastidio, solo preguntaba) 17:20 < nop> con suerte para mañana 17:20 < jrand0m> genial 17:20 < nop> el administrador de correo está trabajando en ello 17:21  * hezekiah observa que a jrand0m le gusta _mucho_ la lista iip-dev. ;-) 17:21 < nop> jaja 17:21 < hezekiah> ¡Vamos delta407! 17:21 < nop> en fin 17:21 < jrand0m> lo mejor es documentar las decisiones públicamente, hezekiah ;) 17:21 < nop> volvamos a nuestra reunión habitual 17:21 < jrand0m> je 17:21 -!- nop ahora se llama nop_afk 17:21 < hezekiah> jrand0m: ¿Entonces dónde estábamos? 17:21 < jrand0m> ok, a tu pregunta, hezekiah> algunos sí, pero los últimos 	 no.  Cambiaré a ponerlos en formato OpenOffice. 17:21 < jrand0m> en lugar de los PDFs 17:22 < hezekiah> OK. 17:22 < hezekiah> Sería realmente genial si todos los documentos estuvieran en CVS. 17:22 < jrand0m> definitivamente, y lo estarán 17:22 < hezekiah> Así puedo simplemente actualizar y sé que tengo la última edición. 17:22 < jrand0m> (hay tres borradores que no lo están por ahora) 17:22 < hezekiah> (Por cierto, un poco fuera de tema, ¿pero ya está 	 activo el acceso anónimo a cathedral?) 17:23 < jrand0m> todavía no. 17:23 < jrand0m> ok, para el viernes, espero tener otro borrador de I2NP en 	 forma completa [o sea, no más ... en las secciones de explicación de 	 Kademlia y detalles de implementación de ejemplo] 17:24 < jrand0m> no hay cambios significativos.  solo más contenido 	 para aclarar cosas. 17:24 < hezekiah> Genial. 17:24 < hezekiah> ¿Habrá disposición en bytes de las estructuras de datos disponible en él? 17:24 < jrand0m> 1.3) especificación de I2P Polling HTTP Transport. 17:24 < jrand0m> no, los diseños en bytes van en la especificación de estructuras 	 de datos, que debería convertirse al formato estándar en lugar de html 17:25 < jrand0m> (aunque I2NP ya tiene todos los diseños en bytes necesarios) 17:25 < jrand0m> ((si lo lees *ejem* ;) 17:25 < hezekiah> Bien. 17:25 < hezekiah> lol 17:25 < hezekiah> Perdón por eso. 17:25 < hezekiah> Como dije, he estado muy ocupado. 17:25 < jrand0m> je, no te preocupes, pronto te vas a la universidad, se 	 supone que deberías estar de fiesta :) 17:25 < hezekiah> ¿De fiesta? 17:25 < jrand0m> ok, 1.3) especificación de I2NP Polling HTTP Transport 17:25 < hezekiah> Hmmm ... supongo que solo soy raro. 17:25 < jrand0m> je 17:26 < jrand0m> ok, intenté enviar esto antes, pero haré commit 	 en breve.  es un protocolo de transporte rápido y sucio que encaja con I2NP 	 para permitir que los routers envíen datos de un lado a otro sin conexiones 	 directas (p. ej., firewalls, proxies, etc.) 17:27 < jrand0m> Estoy *esperando* que alguien pueda ver cómo funciona esto y construir 	 transportes similares (p. ej., TCP bidireccional, UDP, HTTP directo, etc.) 17:27 -!- mihi [none@anon.iip] ha salido [Tiempo de espera de ping agotado] 17:27 < hezekiah> Hmmm, bueno yo no 17:27 < jrand0m> antes de sacar I2NP a revisión, necesitamos incluir 	 transportes de ejemplo para que la gente pueda ver el panorama completo 17:27 < hezekiah> no creo que _yo_ vaya a construir ningún transporte pronto. ;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] se ha unido a #iip-dev 17:27 < hezekiah> TCP está funcionando para Java y Python. 17:27 < hezekiah> (Al menos de cliente a router.) 17:27 < jrand0m> no te preocupes, solo lo dejo como una tarea por hacer para la gente 	 que quiera contribuir 17:28 < hezekiah> Correcto. 17:28 < jrand0m> cierto, cliente-router tiene requisitos diferentes que 	 router-router. 17:28 < jrand0m> ok, de todos modos, 1.4) estado de desarrollo 17:28 < jrand0m> ¿cómo vamos con CBC, thecrypto? 17:28 < thecrypto> Se ha hecho commit de CBC 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS está casi listo 17:28 < hezekiah> thecrypto: ¿Qué es CTS? 17:29 < thecrypto> solo tengo que averiguar cómo implementarlo bien 17:29 < jrand0m> CTS siendo CipherText Stealing (robo de texto cifrado) :) 17:29 < hezekiah> ¡Ah! 17:29 < thecrypto> CipherText Stealing (robo de texto cifrado) 17:29 -!- WinBear [WinBear@anon.iip] ha salido [EOF del cliente] 17:29 < jrand0m> ¿tomaste la referencia de nop sobre eso? 17:29 < hezekiah> OK. Estamos usando CBC con CTS en lugar de padding. 17:29 < hezekiah> Hmm. 17:29 < thecrypto> básicamente, hace que el mensaje tenga exactamente la longitud adecuada 17:29 < jrand0m> ¿eso es viable para el lado de Python, hezekiah? 17:29 < hezekiah> Puede que necesite darle un buen repaso a la librería de criptografía 	 de Python que estoy usando para hacer que use CTS correctamente. 17:30 < hezekiah> Siempre he preferido CTS sobre el padding, pero no sé 	 qué hace PyCrypt. 17:30 < jrand0m> ¿Qué puede hacer Python de fábrica para permitir la recuperación 	 exacta del tamaño del mensaje? 17:30 < thecrypto> todo lo que necesitas hacer es cambiar cómo procesas los 	 dos últimos bloques 17:30 < hezekiah> Tengo la sensación de que esa librería va a tener que 	 reescribirse bastante. 17:30 < hezekiah> jrand0m: Lo de CBC en Python es transparente. Simplemente 	 envías el búfer a la función encrypt del objeto AES. 17:31 < hezekiah> Devuelve texto cifrado.

17:31 < hezekiah> Fin de la historia.
17:31 < jrand0m> ¿Hace D(E(data,key),key) == data, byte por byte, exactamente del mismo tamaño?
17:31 < hezekiah> Así que si tiene la idea loca de usar padding (relleno) en lugar de CTS, entonces quizá tenga que meterme en sus entrañas y arreglarlo.
17:31 < jrand0m> (¿independientemente del tamaño de entrada?)
17:31 -!- mihi [~none@anon.iip] se ha unido a #iip-dev
17:31 < hezekiah> jrand0m: Sí. Debería.
17:31 < jrand0m> hezekiah> si pudieras revisar exactamente qué algoritmo usa para hacer el padding (relleno), sería genial
17:32 < hezekiah> De acuerdo.
17:32  * jrand0m está reticente a exigir un mod a una librería cripto de Python si la librería ya usa un mecanismo estándar y útil
17:32 < hezekiah> De una u otra forma, CBC con CTS suena bien.
17:32 < hezekiah> jrand0m: Esta librería cripto de Python apesta.
17:32 < jrand0m> je, 'k
17:33 < thecrypto> solo tengo que calcular cómo manipular los dos bloques
17:33 < hezekiah> jrand0m: Habrá que reescribir ElGamal por completo en C solo para que sea lo bastante rápido para usarlo.
17:33 < jrand0m> hezekiah> ¿cuál es el benchmark para ElGamal en Python de 256 bytes? solo se hace una vez por comunicación dest-dest...
17:34 < jrand0m> (si lo sabes de memoria, claro)
17:34 < hezekiah> Tendría que probarlo.
17:34 < hezekiah> El cifrado es solo un segundo o dos, creo
17:34 < jrand0m> < 5 seg, < 2 seg, > 10 seg, > 30 seg?
17:34 < thecrypto> probablemente haré algo de trabajo con eso
17:34 < hezekiah> El descifrado podría estar en algún lugar entre 5 o 10 segundos.
17:34 < jrand0m> genial.
17:35 < jrand0m> hezekiah> ¿has hablado con jeremiah o tienes alguna noticia sobre el estado del API de cliente de Python?
17:35 < hezekiah> thecrypto: Todo lo que deberías necesitar es escribir un módulo en C que funcione con Python.
17:35 < hezekiah> No tengo idea de en qué ha estado.
17:35 < hezekiah> No he hablado con él desde que regresé.
17:35 < jrand0m> 'k
17:35 < jrand0m> ¿algún otro comentario sobre el estado del desarrollo?
17:36 < hezekiah> Eh, no mucho de mi parte.
17:36 < hezekiah> Ya he explicado cómo ando de tiempo libre.
17:36 < jrand0m> vale. entendido
17:36 < hezekiah> Mis únicos planes son levantar el API en C y poner el router de Python de nuevo conforme a la especificación.
17:37 < jrand0m> 'k
17:37 < hezekiah> ¡Oh por Dios!
17:37 < jrand0m> 1.4) por hacer
17:37 < jrand0m> ¿sí señor?
17:37 < hezekiah> ¡La librería cripto de Python no implementa CTS ni padding!
17:37 < hezekiah> Tendré que hacerlo manualmente.
17:37 < jrand0m> ¿hmm? ¿requiere que los datos sean múltiplos de 16 bytes?
17:37 < hezekiah> Sí.
17:38 < jrand0m> je
17:38 < jrand0m> en fin.
17:38 < hezekiah> Actualmente el router de Python usa padding.
17:38 < jrand0m> ok. aquí hay algunos pendientes que hay que sacar.
17:38 < hezekiah> Ahora lo recuerdo.
17:38 < hezekiah> Bueno, de
17:38 < hezekiah> seamos francos sobre una cosa.
17:38 < hezekiah> El router de Python nunca estuvo realmente pensado para ser usado.
17:39 < hezekiah> Su objetivo principal es que yo me familiarice mucho con la especificación y además logra otra cosa:
17:39 < hezekiah> Obliga al router de Java a cumplir _exactamente_ con la especificación.
17:39 < jrand0m> ambas metas muy importantes.
17:39 < hezekiah> A veces el router de Java no cumple del todo, y entonces el router de Python pega el grito en el cielo.
17:39 < hezekiah> Así que realmente no necesita ser rápido ni estable.
17:39 < jrand0m> además no estoy seguro de que nunca vaya a usarse en el SDK
17:39 < jrand0m> exacto. exactamente.
17:39 < jrand0m> sin embargo, el API de cliente de Python es otra cosa
17:39 < hezekiah> En cambio, el API de cliente de Python sí necesita ser decente.
17:40 < jrand0m> exacto.
17:40 < hezekiah> Pero ese es el problema de jeremiah. :)
17:40 < hezekiah> Se lo he dejado a él.
17:40 < jrand0m> los routers locales del SDK son solo para uso de desarrollo de clientes
17:40 < jrand0m> lol
17:40 < jrand0m> ok, como decía... ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - necesitamos a alguien que empiece a trabajar en una página web pequeña para I2P que se use para publicar las diversas especificaciones relacionadas con I2P para revisión por pares.
17:41 < jrand0m> Me gustaría que esto estuviera listo antes del 1/9.
17:41 < hezekiah> OK. Declaro desde ya que no quieren que lo haga yo.
17:41 < hezekiah> No soy buen diseñador de páginas web. :)
17:41 < jrand0m> ni yo, si alguien aquí ha visto mi flog ;)
17:41 < jrand0m> ¿cohesion?  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> Pobre cohesion, siempre atrapado con el trabajo sucio. :-)
17:42  * cohesion lee el historial
17:42 < hezekiah> ;)
17:42 < jrand0m> je
17:42 < cohesion> jrand0m: lo haré
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> envíame las especificaciones
17:42 < jrand0m> 'k, gracias.
17:42 < jrand0m> las especificaciones aún no están todas listas.
17:43 < jrand0m> pero el contenido que tendrá que estar ahí es:
17:43 < cohesion> bueno, lo que tienes y lo que te gustaría publicar
17:43 < jrand0m> -especificación de I2CP, especificación de I2NP, especificación de transporte HTTP por sondeo, especificación de transporte TCP, análisis de seguridad, análisis de rendimiento, especificación de estructuras de datos, y un readme/intro
17:44 < jrand0m> (esos 7 documentos estarán en formato pdf y/o texto)
17:44 < cohesion> k
17:44 < jrand0m> salvo el readme/intro
17:45 < jrand0m> Espero que todos esos documentos estén listos para la próxima semana (8/26). ¿Eso te dará tiempo suficiente para armar una página pequeña para un lanzamiento el 1/9?
17:46 < jrand0m> ok. otra cosa que tendrá que venir en camino es un simulador de red de I2P.
17:46 < jrand0m> ¿tenemos a alguien buscando un proyecto de CS (Ciencias de la Computación)?  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m: sí, eso es factible
17:47 < hezekiah> Yo no, por unos cuantos años. ;-)
17:47 < jrand0m> genial cohesion
17:47 < thecrypto> no por un año
17:47  * cohesion vuelve al trabajo
17:47 < jrand0m> gracias cohesion
17:48 < jrand0m> ok, 1.6) próximas dos semanas. en mi plato está subir estas especificaciones, docs y análisis. Publicaré &amp; haré commit tan pronto como pueda.
17:48 < jrand0m> POR FAVOR LEAN LAS ESPECIFICACIONES Y COMENTEN
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m: De acuerdo. En cuanto tenga tiempo, empezaré a leer. :)
17:48 < jrand0m> Preferiría que la gente publique comentarios en la lista, pero si quieren ser anónimos, envíenme comentarios en privado y publicaré respuestas en la lista de forma anónima.
17:49 < hezekiah> (¿Cuál crees que es el ETA para que los archivos de OpenOffice de la documentación estén en CVS?)
17:49 < jrand0m> Puedo hacer commit de las últimas revs dentro de 10 minutos de que termine esta reunión.
17:49 < hezekiah> Genial. :)
17:50 < jrand0m> ok, eso es todo para 1.*.
17:50 < jrand0m> 2.x) ¿comentarios/preguntas/preocupaciones/quejas?
17:50 < jrand0m> ¿cómo va el mod del SDK, mihi?
17:51 < jrand0m> ¿o alguien más?  :)
17:51 < hezekiah> jrand0m: ¿Qué es ese mod del SDK del que hablas?
17:52 < jrand0m> hezekiah> dos correcciones de bugs al SDK, hice commit (&amp; publiqué) el otro día
17:52 < hezekiah> Ah
17:52 < hezekiah> Qué bien.
17:52 < jrand0m> (rotar los IDs de mensaje, sincronizar escrituras)
17:52 < hezekiah> ¿Solo del lado Java, o también del lado Python?
17:52 < jrand0m> yo no hablo Python.
17:53 < hezekiah> lol
17:53 < jrand0m> no estoy seguro de si los bugs existen allí. ¿rotas los IDs de mensaje cada 255 mensajes y sincronizas tus escrituras?
17:54 < hezekiah> Creo que el router de Python hace ambas cosas
17:54 < jrand0m> genial.
17:54 < jrand0m> te avisaremos si no lo hace ;)
17:54 < hezekiah> ¿Qué quieres decir exactamente con «sincronizar tus escrituras»?
17:55 < jrand0m> o sea, asegurarte de que no se escriban múltiples mensajes a un cliente al mismo tiempo si hay múltiples clientes tratando de enviarle mensajes al mismo tiempo.
17:55 < hezekiah> Todos los datos enviados sobre la conexión TCP se envían en el orden en que se originaron.
17:56 < hezekiah> Así que no tendrás 1/2 del mensaje A y luego 1/3 del mensaje B.
17:56 < jrand0m> 'k
17:56 < hezekiah> Recibirás el mensaje A y luego el mensaje B.
17:56 < hezekiah> OK ... si nadie más va a hablar, sugiero que levantemos la reunión.
17:56 < mihi> mi simple TCP/IP sobre I2P parece funcionar...
17:56 < jrand0m> ¡niiiiice!!
17:56  * mihi estaba ausente un poco, perdón
17:57 < hezekiah> ¿Alguien más tiene algo que decir?
17:57 < jrand0m> mihi> ¿así que podremos ejecutar pserver sobre eso?
17:57 < mihi> mientras no intentes crear muchas conexiones a la vez.
17:57 < mihi> jrand0m: supongo que sí: pude llegar a google a través de eso
17:57 < jrand0m> niiiice
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> entonces tienes un outproxy y un inproxy?
17:58 < mihi> exacto.
17:58 < jrand0m> genial
17:58 < mihi> el destino necesita claves, el origen las genera bajo demanda
17:58  * hezekiah le entrega a jrand0m el *baf*er. Rompe la cosa cuando termines, tío.
17:58 < jrand0m> bien. con suerte el servicio de nombres de co podría ayudar con eso cuando esté listo.
17:59 < jrand0m> ok, genial. mihi, avísame a mí o a cualquier otro si hay algo en lo que podamos ayudar :)
17:59 < mihi> arreglen esa cosa de los 128 msgids o construyan un soporte GARANTIZADO mejor
17:59  * jrand0m *baf*ea a nop_afk en la cabeza por tener un trabajo de verdad
18:00 < mihi> jrand0m: el abuso del baf cuesta 20 yodels
18:00 < jrand0m> lol
18:00 < jrand0m> ¿mejor soporte garantizado?
18:00 < jrand0m> (o sea, mejor rendimiento que el descrito? lo arreglaremos en la impl)
18:00 < mihi> ¿probaste mi caso de prueba con start_thread=end_thread=300?
18:01 < mihi> genera muchos mensajes en una dirección, y eso hace que se consuman todos los msgids...
18:01 < jrand0m> hmm, no, no había visto ese mensaje
18:01 < hezekiah> jrand0m: ¿Sería razonable hacer el msgid de 2 bytes?
18:01  * jrand0m probó el 200 / 201, pero eso está arreglado con el último
18:01 -!- cohesion [cohesion@anon.iip] ha salido [se va a la reunión del lug]
18:01 < mihi> ¿cuál último?
18:01 < hezekiah> Entonces tendrían 65535 msgids (si no cuentas el msgid 0)
18:01 < hezekiah> .
18:02 < jrand0m> IDs de mensaje de 2 bytes no harían daño. Estoy cómodo con ese cambio.
18:02 < jrand0m> mihi> el que te envié por correo
18:02 < mihi> si tienes uno más nuevo que el que me enviaste, envíalo (o dame acceso a cvs)
18:03 < mihi> hmm, ese me falla con 200/201 (así como con 300)
18:03 < jrand0m> hmm. Haré más pruebas y depuración y te enviaré por correo lo que obtenga.
18:03 < mihi> gracias.
18:04 < jrand0m> ok.
18:04  * jrand0m declara la reunión
18:04 < jrand0m> *baf*'ed
18:04  * hezekiah cuelga el *baf*er reverentemente en su estante especial.
18:05  * hezekiah luego gira, sale por la puerta y la azota detrás de él. El baffer se cae del estante.
18:05 < hezekiah> ;-) --- Registro cerrado Tue Aug 19 18:05:36 2003 </div>
