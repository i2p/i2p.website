---
title: "Reunión de desarrolladores de I2P, 5 de agosto de 2003"
date: 2003-08-05
author: "nop"
description: "52.ª reunión de desarrolladores de I2P sobre el estado del desarrollo en Java, actualizaciones de criptografía y progreso del SDK"
categories: ["meeting"]
---

<h2 id="quick-recap">Resumen rápido</h2>

<p class="attendees-inline"><strong>Presentes:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Registro de la reunión</h2>

<div class="irc-log"> <nop>	ok, la reunión ha comenzado <nop>	¿qué hay en la agenda -->	logger (logger@anon.iip) se ha unido a #iip-dev -->	Anon02 (~anon@anon.iip) se ha unido a #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Bienvenidos a la enésima reunión de iip-dev. <hezekiah>	¿Qué hay en la agenda? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	sincronizado con un NTP estrato 2 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) se ha unido a #iip-dev <hezekiah>	Acabo de sincronizar con NIST. :) <mihi>	esta sincronización no ayuda con los retrasos de iip ;) <jrand0m>	nop: cosas que quiero ver cubiertas: estado del desarrollo en Java, estado de la criptografía en Java 	  , estado del desarrollo en Python, estado del SDK, servicio de nombres <hezekiah>	(¿Vamos a entrar al servicio de nombres _ya_?) <jrand0m>	no diseño, idiota, esa es la perorata de co.  solo habla de cosas 	  si hay cosas de las que hablar. <hezekiah>	Ah *	jrand0m guarda el LART <jrand0m>	¿algo más en la agenda? <jrand0m>	¿o nos metemos en materia? <hezekiah>	Bueno, no se me ocurre nada más que añadir. <hezekiah>	¡Ah! <hezekiah>	¡Oh! <jrand0m>	ok.  estado del desarrollo en Java: <hezekiah>	Bien. <--	mrflibble ha salido (Ping timeout) <nop>	ok <nop>	agenda <nop>	1) Bienvenida <jrand0m>	a partir de hoy, hay una API de cliente en Java con un router Java de prueba (stub) 	  que pueden comunicarse entre sí.  además, hay una aplicación llamada ATalk 	  que permite mensajería instantánea anónima + transferencia de archivos. <nop>	2) Cortes de IIP 1.1 <nop>	3) I2P <nop>	4) El final con comentarios y esas cosas *	jrand0m vuelve a la esquina <nop>	perdón 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah le da a jrand0m un gorro de burro para que lo use en 	  la esquina. ;-) <nop>	perdón por eso <nop>	no vi que habías empezado ahí <nop>	quizá debería irme a la esquina <hezekiah>	lol <jrand0m>	no hay problema.  punto 1) *	hezekiah le entrega a nop un gorro de burro también. :) <nop>	ok bienvenidos todos <nop>	bla bla <nop>	2) Cortes de IIP 1.1 -->	mrflibble (mrflibble@anon.iip) se ha unido a #iip-dev <hezekiah>	¡52ª reunión de iip-dev y toda esa buena cháchara! <nop>	el servidor recientemente tuvo algunos problemas con los sectores del disco duro y ha 	  sido reemplazado <nop>	planeo mover el condenado servidor a un entorno más estable con 	  redundancia <nop>	y posiblemente ceder el control de múltiples servidores ircd <nop>	no sé <nop>	eso es algo para discutir <--	Anon02 ha salido (EOF From client) <nop>	con suerte nuestros servidores deberían mantenerse en línea ahora que se reemplazó el disco duro <nop>	disculpen las molestias, gente <nop>	3) I2P - Jrand0m, adelante <nop>	sal de la esquina, jrand0m *	hezekiah va hacia la esquina, saca a jrand0m de su silla, lo arrastra 	  al podio, le quita su gorro de burro y le entrega el micrófono. *	nop va a esa esquina para ocupar su lugar <hezekiah>	lol! <jrand0m>	perdón, de vuelta *	nop le quita el gorro de burro a hezekiah *	nop se lo pone en la cabeza *	nop aplaude a jrand0m *	jrand0m solo mira el espectáculo <jrand0m>	er... em ok <hezekiah>	jrand0m: i2p, estado de Java, etc. ¡Habla, hombre! <jrand0m>	entonces, a partir de hoy, hay una API de cliente en Java con un router Java 	  de prueba (stub) que pueden comunicarse entre sí.  además, hay una aplicación llamada 	  ATalk que permite mensajería instantánea anónima + transferencia de archivos. <hezekiah>	¿Transferencia de archivos ya?! <jrand0m>	si sr <hezekiah>	Vaya. <hezekiah>	Estoy seguro de que voy atrasado. <jrand0m>	pero no de la manera más elegante <hezekiah>	lol <jrand0m>	toma un archivo y lo mete en un mensaje <hezekiah>	Ay. <nop>	¿cuánto tardó la transferencia local de 1.8 mb? <jrand0m>	He probado con un archivo de 4K y uno de 1.8Mb <jrand0m>	unos segundos <nop>	bien <nop>	:) <hezekiah>	¿Lo de Java ya hace cifrado real, o sigue 	  fingiendo eso? <nop>	falso <nop>	hasta yo lo sé <nop>	:) <jrand0m>	Lo calenté hablando conmigo mismo primero [p. ej., de una ventana a 	  otra, diciendo hola] así no tuvo que lidiar con la sobrecarga del primer elg <jrand0m>	correcto, en gran medida está fingido <thecrypto>	la mayor parte del cifrado es falso <thecrypto>	aunque se está trabajando en eso <hezekiah>	Por supuesto. :) <jrand0m>	definitivamente. <jrand0m>	en ese frente, ¿quieres darnos una actualización, thecrypto? <thecrypto>	bueno, por ahora terminé con ElGamal y SHA256 <thecrypto>	ahora estoy trabajando en generar primos para DSA <thecrypto>	enviaré 5 y luego podemos simplemente elegir uno <hezekiah>	nop: ¿No tenías primos en camino para usar con DSA? <thecrypto>	También tenemos algunas pruebas de rendimiento sobre ElGamal y SHA256 <thecrypto>	Y todos son rápidos <jrand0m>	últimas pruebas de rendimiento con elg: <jrand0m>	Promedio del tiempo de generación de claves: 4437	total: 443759	mín: 	  872	   máx: 21110	   Generación de claves/segundo: 0 <jrand0m>	Promedio del tiempo de cifrado    : 356	total: 35657	mín: 	  431	   máx: 611	   Bps de cifrado: 179 <jrand0m>	Promedio del tiempo de descifrado    : 983	total: 98347	mín: 	  881	   máx: 2143	   Bps de descifrado: 65

<hezekiah>	min y max: ¿son en segundos?
<jrand0m>	ten en cuenta que los Bps no son realmente útiles, ya que solo ciframos/desciframos 64 bytes
<thecrypto>	ms
<jrand0m>	no, perdón, todo eso está en milisegundos
<hezekiah>	Genial. :)
<hezekiah>	¿Y esto está hecho en java?
<thecrypto>	sí
<thecrypto>	java puro
<hezekiah>	OK. Estoy oficialmente impresionado. :)
<jrand0m>	100%.  P4 1.8
<thecrypto>	son más o menos lo mismo en mi 800 MHz
<hezekiah>	¿Cómo puedo hacer las mismas pruebas?
<jrand0m>	prueba de rendimiento de sha256:
<jrand0m>	Short Message Time Average  : 0 total: 0	min: 0	max: 	  0  Bps: NaN
<jrand0m>	Medium Message Time Average : 1 total: 130	min: 0	max: 	  10 Bps: 7876923
<jrand0m>	Long Message Time Average   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037
<thecrypto>	ejecuta el programa ElGamalBench
<hezekiah>	OK.
<hezekiah>	Voy a buscarlo.
<jrand0m>	(tamaño corto: ~10 bytes, mediano ~10KB, largo ~ 1MB)
<jrand0m>	java -cp i2p.jar ElGamalBench
<jrand0m>	(después de ejecutar "ant all")
<hezekiah>	jrand0m: Gracias. :)
<jrand0m>	sin problema
<thecrypto>	Lo de NaN significa que es tan rápido que terminamos dividiendo entre 0, es tan rápido :)
<hezekiah>	¿Cuál es la prueba de sha?
<jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) se ha unido a #iip-dev
<hezekiah>	OK.
<jrand0m>	probablemente querremos mover eso para que sean métodos main() de los motores asociados, pero están bien donde están por ahora
<hezekiah>	Veamos qué tan rápido va todo esto en un AMD K6-2 333MHz (que es un chip no muy conocido por su aritmética de enteros).
<jrand0m>	jeje
<jrand0m>	ok, así que nos quedan DSA y AES, ¿cierto?
<jrand0m>	esto está genial, thecrypto. buen trabajo.
<thecrypto>	sí
<jrand0m>	¿Puedo molestarte por un ETA (tiempo estimado) para los otros dos?  ;)
<hezekiah>	Si esto es más o menos igual de rápido en mi máquina que en la tuya, tienes que mostrarme cómo haces eso. ;-)
<thecrypto>	DSA debería estar listo casi en cuanto tenga listos los números primos
<nop>	hezekiah, ¿has probado sslcrypto para python
<thecrypto>	copiando algo de código del generador de primos y cosas así y está listo
<nop>	el que está en ese enlace
<hezekiah>	nop: sslcrypto no nos sirve.
<hezekiah>	nop: No implementa ElGamal _o_ AES _o_ sha256.
<thecrypto>	AES está casi listo salvo por algún error en algún lugar que aún estoy tratando de encontrar y destruir; en cuanto tenga eso, estará listo
<jrand0m>	thecrypto> entonces para el viernes, DSA keygen, sign, verify, y AES encrypt, decrypt para entradas de tamaño arbitrario?
<nop>	¿el del sitio de McNab no?
<thecrypto>	sí
<nop>	vaya
<thecrypto>	debería ser para el viernes
<thecrypto>	lo más probable el jueves
<jrand0m>	thecrypto> ¿eso incluye lo de UnsignedBigInteger?
<thecrypto>	no podré asistir a la reunión de la próxima semana por el campamento de verano, y volveré después de eso
<thecrypto>	jrand0m: probablemente no
<jrand0m>	ok.
<jrand0m>	así que, por el momento, la interoperabilidad entre java y python está rota.
<jrand0m>	para cripto, es decir.
---	Aviso: jeremiah está en línea (anon.iip).
-->	jeremiah (~chatzilla@anon.iip) se ha unido a #iip-dev
<jrand0m>	(o sea, para firmas, claves, cifrado y descifrado)

<nop>	hmm quizá deberíamos centrarnos más en C/C++ <thecrypto>	bueno, una vez que lo tengamos funcionando por completo podremos asegurarnos 	  de que tanto java como python puedan hablar entre sí
<jrand0m>	mientras no estés, echaré un vistazo al tema de los tipos sin signo.
<jeremiah>	¿alguien puede enviarme por email un historial? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Dame un minuto. :)
<jrand0m>	nop> ¿tenemos desarrolladores para C/C++?
<nop>	Tengo a un tipo, sí
<nop>	y sabemos que Hezekiah podría hacerlo
<jrand0m>	o quizá podamos obtener una actualización de estado del desarrollo en python de hezekiah + 	  jeremiah para ver cuándo tendremos más gente para el desarrollo en c/c++
<jrand0m>	claro, por supuesto.  pero hez+jeremiah están trabajando en python en este momento 	  (¿cierto?)
<hezekiah>	Sí.
<--	mrflibble ha salido (Tiempo de espera de ping agotado)
<hezekiah>	Estoy como dándole muchos problemas al pobre jeremiah.
<nop>	Solo decía que si python no va a tener velocidades altas
<hezekiah>	Python es principalmente para que yo entienda esta red.
<nop>	ahh
<hezekiah>	Una vez que logre que básicamente siga la especificación completa, tengo la intención 	  de pasárselo a jeremiah para que haga con ello lo que considere.
<hezekiah>	No pretende ser una implementación de la especificación de primera.
<hezekiah>	(Si quisiera eso, usaría C++.)
<jeremiah>	bueno, no hay partes realmente intensivas en procesador de la app, 	  si mal no recuerdo, aparte de la criptografía, e idealmente eso se manejaría en C de todos modos, ¿no?
<jrand0m>	claro jeremiah. todo depende de la app
-->	mrflibble (mrflibble@anon.iip) se ha unido a #iip-dev
<hezekiah>	jeremiah: En teoría.
<jrand0m>	entonces, ¿dónde estamos del lado de python?  API del cliente, router solo 	  local, etc.?
<jeremiah>	la implementación en python también nos permitirá saber qué optimizaciones 	  podríamos hacer desde el principio... me gustaría mantenerla al día o, posiblemente, 	  por delante de la implementación en C en la medida en que pueda
<hezekiah>	jrand0m: OK. Esto es lo que tengo.
<hezekiah>	En _teoría_ el router debería poder manejar todos los mensajes 	  que no son de administración de un cliente.
<hezekiah>	Sin embargo, aún no tengo cliente, así que no he podido depurarlo 	  (es decir, todavía hay bugs.)
<hezekiah>	Estoy trabajando en el cliente ahora mismo.
<jrand0m>	'k.  si puedes desactivar la verificación de firmas, deberíamos poder 	  ejecutar el cliente de java contra eso ahora
<hezekiah>	Espero tener eso hecho, salvo los mensajes de administración, en uno 	  o dos días.
<jrand0m>	podemos probar eso después de la reunión
<hezekiah>	jrand0m: OK.
<jeremiah>	he estado lidiando sobre todo con cosas del mundo real desde la última 	  reunión; puedo trabajar en la API del cliente, solo he estado intentando sincronizar mi forma de pensar 	  con la de hezekiah
<jrand0m>	genial
<hezekiah>	jeremiah: ¿Sabes qué? Espera.
<hezekiah>	jeremiah: Probablemente estoy metiendo demasiadas cosas nuevas para que tengas que 	  lidiar con ellas ahora mismo.
<jeremiah>	hezekiah: correcto, lo que iba a decir es que probablemente deberías 	  simplemente seguir adelante e implementar lo básico
<hezekiah>	jeremiah: En un rato, estará estabilizado y podrás 	  comenzar a refinarlo. (Hay muchos comentarios TODO que necesitan ayuda.)
<jeremiah>	y luego puedo ampliarlo más adelante cuando ya tenga el panorama claro
<hezekiah>	Exacto.
<hezekiah>	A ti te toca mantener todo este código. :)
<jrand0m>	genial.  entonces ETA 1-2 semanas para un router de python funcionando + API del cliente?
<hezekiah>	Me voy de vacaciones la próxima semana, así que probablemente.
<hezekiah>	¿Vamos a tener más detalles de router a router pronto?
<jrand0m>	no.
<jrand0m>	bueno, sí.
<jrand0m>	pero no.
<hezekiah>	lol
<jeremiah>	hezekiah: ¿Cuánto duran las vacaciones?
<hezekiah>	1 semana.
<jeremiah>	ok
<jrand0m>	(o sea, en cuanto salga el SDK, el 100% de mi tiempo se va a I2NP)
<hezekiah>	Espero tener escrita toda la funcionalidad no administrativa antes de 	  irme de vacaciones
<hezekiah>	.
<jrand0m>	pero luego, poco después de que vuelvas, te vas a la universidad, ¿no?
<hezekiah>	I2NP?
<hezekiah>	Correcto.
<jrand0m>	protocolo de red
<hezekiah>	Tengo como 1 semana después de las vacaciones.
<hezekiah>	Luego me voy.
<hezekiah>	Y mi tiempo libre cae en picado.
<jrand0m>	así que esa 1 semana debería ser solo de depuración
<jeremiah>	puedo trabajar en el código mientras hez no esté, de todos modos
<jrand0m>	ok
<jrand0m>	¿cómo pinta tu verano, jeremiah?
<hezekiah>	jeremiah: ¿Quizás puedas hacer que funcionen esas funciones de administración?

<thecrypto> todavía tendré un mes, después de volver de mis vacaciones, para trabajar 	  en las cosas
<jrand0m> ¿tener vida, o ser como el resto de nosotros, l00sers?  :)
<jeremiah> quizá
<hezekiah> 100sers?
<hezekiah> ¿Qué es un 100ser?
<jeremiah> me voy a la universidad el 22; fuera de eso, puedo desarrollar
<mihi> hezekiah: un perdedor
<jeremiah> y la última semana antes de irme todos mis amigos estarán fuera... así 	  que puedo entrar en modo de hiperdesarrollo
<hezekiah> mihi: ¡Ah!
<jrand0m> jeje
<hezekiah> OK. Entonces, ¿en qué íbamos de la agenda?
<hezekiah> es decir, ¿qué sigue?
<jrand0m> estado del SDK
<jrand0m> SDK == una implementación de cliente, una implementación de router solo local, una app y documentación.
<jrand0m> Me gustaría tener eso listo para el próximo martes.
<hezekiah> jeremiah: Ese backlog va en camino. Perdón que te olvidé ahí. :)
<jeremiah> gracias
<jrand0m> ok, co no está por aquí, así que lo del servicio de nombres probablemente está un poco 	  fuera de lugar
<jrand0m> podemos discutir el servicio de nombres después de que publique especificaciones o 	  cuando esté presente
<jrand0m> ok, eso es todo con lo de I2P
<jrand0m> ¿alguien más tiene cosas de I2P, o pasamos a:
<nop> 4) El final con 	  comentarios y esas cosas
<hezekiah> No se me ocurre nada.
<jrand0m> Supongo que todos han visto 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html ?
<thecrypto> no aquí
<jrand0m> (nop lo publicó aquí antes)
<hezekiah> ¿Lo del tipo al que arrestaron por enlazar a un sitio de construcción de bombas?
<jrand0m> sí
<jrand0m> la relevancia de la necesidad de poner I2P en marcha cuanto antes debería ser aparente ;)
<hezekiah> ¡OK! jeremiah, esos registros ya fueron enviados.
<jeremiah> gracias
<jrand0m> ¿alguien tiene preguntas / comentarios / ideas / frisbees, 	  o estamos teniendo una reunión cortísima de récord?
* thecrypto lanza un frisbee <-- logger ha salido (Ping timeout)
<jrand0m> caray, están muy callados hoy ;)
<mihi> pregunta:
<mihi> ¿dónde pueden conseguir los no desarrolladores tu código Java?
<jrand0m> si sr?
<thecrypto> todavía no
<mihi> 404
<jrand0m> eso estará disponible cuando estemos listos para el lanzamiento.  o sea, el 	  código fuente saldrá junto con el SDK
<jrand0m> je
<jrand0m> sí, no usamos SF
<hezekiah> nop: ¿Es posible que podamos tener cvs anónimo funcionando algún tiem?
<hezekiah> ¿tiempo?
<-- mrflibble ha salido (Ping timeout)
<nop> bueno, abriría un puerto no estándar
<jrand0m> hezekiah> tendremos eso una vez que el código tenga la licencia GPL ahí
<nop> pero estoy trabajando en viewcvs
<jrand0m> o sea, no ahora, ya que el documento de la GPL aún no se ha añadido al código
<hezekiah> jrand0m: Está en todos los directorios de código de Python y todos los 	  archivos fuente de Python especifican la licencia como GPL-2.
<jrand0m> hezekiah> ¿eso está en la cathedral?
<hezekiah> Sí.
<jrand0m> ah, de acuerdo.  i2p/core/code/python ?  ¿o un módulo diferente?
* jrand0m no lo ha visto ahí
<hezekiah> Cada directorio de código de Python tiene un archivo COPYING con la 	  GPL-2, y cada archivo fuente tiene la licencia establecida como GPL-2
<hezekiah> Es i2p/router/python y i2p/api/python
<jrand0m> 'k
<jrand0m> así que, sí, para el próximo martes tendremos el SDK + acceso público al código fuente.
<hezekiah> Genial.
<hezekiah> O como te gusta decir, wikked. ;-)
<jrand0m> je
<jrand0m> nada mas?
<hezekiah> nada mas? ¿Qué significa eso!?
<jeremiah> nada más
* jrand0m sugiere que aprendas un poco de español en la universidad
--> mrflibble (mrflibble@anon.iip) se ha unido a #iip-dev
<hezekiah> ¿Preguntas, alguien?
<hezekiah> ¡A la una!
<-- ptm (~ptm@anon.iip) ha salido de #iip-dev (ptm)
<hezekiah> ¡A las dos!
<-- mrflibble ha salido (mr. flibble dice "se acabó el juego, chicos")
<hezekiah> ¡Hablen ahora... o esperen hasta que les apetezca hablar más tarde!
<thecrypto> de acuerdo, voy a seguir optimizando ElGamal aún más, así que esperen 	  pruebas de rendimiento de ElGamal aún más rápidas en el futuro
<jrand0m> por favor, concéntrate en DSA y AES antes de afinar... por favoooooor :)
<thecrypto> lo haré
<hezekiah> La razón por la que está haciendo eso es porque estoy causándole problemas a 	  la gente otra vez. ;-)
<thecrypto> estoy generando primos de DSA
--> mrflibble (mrflibble@anon.iip) se ha unido a #iip-dev
<thecrypto> bueno, al menos haciendo el programa para generar primos de DSA ahora mismo
<hezekiah> ElGamal en Java no se lleva bien con un AMD K-6 II 333 MHz.
<hezekiah> OK.
<hezekiah> ¡Se acabó la ronda de preguntas!
<jrand0m> ok hez, terminamos.  ¿quieres hacer un powow para hacer que el cliente Java 	  y el router en Python funcionen?
<hezekiah> ¡Nos vemos la próxima semana, ciudadanos!
* hezekiah baja con fuerza el *baf*er
</div>
