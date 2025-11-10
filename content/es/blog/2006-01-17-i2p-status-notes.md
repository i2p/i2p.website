---
title: "Notas de estado de I2P del 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Estado de la red con la 0.6.1.9, mejoras criptográficas en la creación de tunnel y actualizaciones de la interfaz del blog de Syndie"
categories: ["status"]
---

Hola a todos, ya es martes otra vez

* Index

1) Estado de la red y 0.6.1.9 2) Criptografía para la creación de Tunnel 3) Blogs de Syndie 4) ???

* 1) Net status and 0.6.1.9

Con la 0.6.1.9 publicada y el 70% de la red actualizado, la mayoría de las correcciones de errores incluidas parecen estar funcionando como se esperaba, y hay informes de que el nuevo perfilado de velocidad ha estado seleccionando algunos buenos pares. He oído de un caudal sostenido en pares rápidos que supera los 300KBps con un uso de CPU del 50-70%, con otros routers en el rango de 100-150KBps, disminuyendo hasta aquellos que alcanzan 1-5KBps. Sin embargo, todavía hay una rotación sustancial de identidades de router, así que parece que la corrección de errores que pensé que lo reduciría no lo ha hecho (o la rotación es legítima).

* 2) Tunnel creation crypto

En otoño, hubo mucha discusión sobre cómo construimos nuestros tunnels, junto con los compromisos entre la creación de tunnel telescópica al estilo Tor y la creación de tunnel exploratoria al estilo I2P [1]. Por el camino, ideamos una combinación [2] que elimina los problemas de la creación de tunnel telescópica al estilo Tor [3], mantiene los beneficios unidireccionales de I2P y reduce las fallas innecesarias.  Como había muchas otras cosas en marcha en ese momento, se pospuso la implementación de la nueva combinación, pero como ahora nos acercamos al lanzamiento 0.6.2, durante el cual de todos modos necesitamos renovar el código de creación de tunnel, es hora de dejar esto bien resuelto.

Esbocé un borrador de especificación para la nueva criptografía de tunnel y lo publiqué en mi blog en Syndie el otro día, y después de algunos cambios menores que surgieron al implementarla realmente, ya tenemos una especificación en CVS [4]. También hay código básico que la implementa en CVS [5], aunque aún no está integrado para la construcción real de tunnel. Si alguien está aburrido, me encantaría recibir comentarios sobre la especificación. Mientras tanto, seguiré trabajando en el nuevo código de construcción de tunnel.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html y     consulte los hilos relacionados con los ataques de bootstrap (inicialización) [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Como se mencionó anteriormente, esta nueva versión 0.6.1.9 incluye renovaciones sustanciales en la interfaz del blog de Syndie, incluyendo el nuevo estilo de cervantes y la selección de enlaces del blog y del logotipo de cada usuario (p. ej., [6]). Puedes controlar esos enlaces a la izquierda haciendo clic en el enlace "configure your blog" en tu página de perfil, lo que te llevará a http://localhost:7657/syndie/configblog.jsp. Una vez que hagas tus cambios allí, la próxima vez que subas una entrada a un archivo, esa información estará disponible para otros.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Como ya voy 20 minutos tarde a la reunión, probablemente debería ser breve.  Sé que hay algunas otras cosas en marcha, pero en lugar de sacarlas a relucir aquí, los desarrolladores que quieran hablar de ellas deberían pasarse por la reunión y plantearlas.  En fin, eso es todo por ahora, ¡nos vemos en #i2p!

=jr
