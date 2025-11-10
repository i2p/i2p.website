---
title: "Notas de estado de I2P del 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Actualización semanal sobre el progreso del transporte SSU, la mitigación del ataque IV en tunnel y la optimización del MAC de SSU con HMAC-MD5"
categories: ["status"]
---

Hola, equipo, ha llegado ese momento de la semana,

* Index

1) Estado de desarrollo 2) Vectores de inicialización de Tunnel 3) Códigos de autenticación de mensajes de SSU 4) ???

* 1) Dev status

Otra semana, otro mensaje diciendo "Ha habido mucho progreso en el transporte SSU" ;) Mis modificaciones locales son estables y se han subido a CVS (HEAD está en 0.5.0.7-9), pero aún no hay una versión. Más noticias al respecto pronto. Los detalles sobre los cambios no relacionados con SSU están en el historial [1], aunque por ahora estoy dejando fuera de esa lista los cambios relacionados con SSU, ya que SSU aún no es utilizado por ningún usuario que no sea desarrollador (y los desarrolladores leen i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Durante los últimos días, dvorak ha estado publicando reflexiones ocasionales sobre distintas formas de atacar el cifrado del tunnel, y aunque la mayoría ya se habían abordado, pudimos idear un escenario que permitiría a los participantes etiquetar un par de mensajes para determinar que están en el mismo tunnel. La forma en que funcionaba era que el par anterior dejaba pasar un mensaje y, más tarde, tomaba el vector de inicialización (IV) y el primer bloque de datos de ese primer mensaje del tunnel y los colocaba en uno nuevo. Este nuevo, por supuesto, estaría corrupto, pero no parecería un ataque de repetición (replay), ya que los IV eran diferentes. Más adelante, el segundo par podría simplemente descartar ese mensaje para que el extremo del tunnel no pudiera detectar el ataque.

Uno de los problemas fundamentales detrás de esto es que no hay manera de verificar un mensaje de tunnel mientras avanza por el tunnel sin dar pie a toda una serie de ataques (véase una propuesta de criptografía de tunnel anterior [2] para un método que se aproxima, pero que tiene probabilidades bastante poco sólidas e impone algunos límites artificiales a los tunnels).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Sin embargo, hay una forma trivial de eludir el ataque particular descrito - simplemente tratar xor(IV, primer bloque de datos) como el identificador único que se pasa por el filtro de Bloom en lugar del IV por sí solo. De este modo, los pares intermedios verán el duplicado y lo descartarán antes de que llegue al segundo par coludido. CVS se ha actualizado para incluir esta defensa, aunque dudo muchísimo que sea una amenaza práctica dado el tamaño actual de la red, así que no la voy a publicar como una versión independiente.

Esto no afecta la viabilidad de otros ataques de temporización o de shaping (modelado de tráfico), sin embargo, es mejor mitigar los ataques fáciles de manejar en cuanto los detectamos.

* 3) SSU MACs

Como se describe en la especificación [3], el transporte SSU utiliza un MAC para cada datagrama transmitido. Esto se suma al hash de verificación enviado con cada mensaje I2NP (así como a los hashes de verificación de extremo a extremo en los mensajes de cliente). Actualmente, la especificación y el código usan un HMAC-SHA256 truncado - transmitiendo y verificando solo los primeros 16 bytes del MAC. Esto es *ejem*, un poco ineficiente, ya que el HMAC utiliza el hash SHA256 dos veces en su operación, cada vez procesando un hash de 32 bytes, y un perfilado reciente del transporte SSU sugiere que esto está cerca del camino crítico para la carga de CPU. Por ello, he estado explorando reemplazar HMAC-SHA256-128 por un HMAC-MD5(-128) simple - si bien MD5 claramente no es tan fuerte como SHA256, de todos modos estamos truncando el SHA256 al mismo tamaño que MD5, así que la cantidad de fuerza bruta requerida para una colisión es la misma (2^64 intentos). Estoy haciendo pruebas con ello en este momento y la aceleración es considerable (obteniendo más de 3x el rendimiento de HMAC en paquetes de 2KB que con SHA256), así que quizá podamos poner eso en producción en su lugar. O, si alguien puede aportar una buena razón para no hacerlo (o una alternativa mejor), es lo suficientemente sencillo cambiarlo (solo una línea de código).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

Eso es todo por el momento y, como siempre, no duden en publicar sus opiniones e inquietudes cuando quieran. CVS HEAD vuelve a ser compilable para quienes no tienen junit instalado (por el momento he extraído las pruebas de i2p.jar, pero siguen siendo ejecutables con el target test de Ant), y espero que haya más novedades sobre las pruebas de la 0.6 bastante pronto (sigo peleando con las rarezas de la colo box (servidor en colocation) por el momento - hacer telnet a mis propias interfaces falla localmente (sin ningún errno útil), funciona de forma remota, todo ello sin iptables ni otros filtros. qué alegría). Aún no tengo acceso a la red en casa, así que no estaré disponible para una reunión esta noche, pero quizá la próxima semana.

=jr
