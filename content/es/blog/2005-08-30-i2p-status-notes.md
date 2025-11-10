---
title: "Notas de estado de I2P del 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Actualización semanal que cubre el estado de la red en 0.6.0.3 con problemas de NAT, el despliegue de floodfill netDb y el progreso de la internacionalización de Syndie"
categories: ["status"]
---

Hola a todos, ya llegó otra vez ese momento de la semana

* Index

1) Estado de la red 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

Con la 0.6.0.3 disponible desde hace una semana, los informes son bastante buenos, aunque el registro y la visualización han sido bastante confusos para algunos. Hasta hace unos minutos, I2P informa de que un número considerable de personas han configurado incorrectamente sus NAT o cortafuegos: de 241 pares, 41 han visto que el estado cambie a ERR-Reject, mientras que 200 han estado directamente OK (cuando pueden obtener un estado explícito). Esto no es bueno, pero ha ayudado a precisar un poco más lo que hay que hacer.

Desde el lanzamiento, ha habido algunas correcciones de errores para condiciones de error de larga data, llevando el HEAD actual de CVS a 0.6.0.3-4, que probablemente se publicará como 0.6.0.4 más adelante esta semana.

* 2) floodfill netDb

Como se comentó [1] en mi blog [2], estamos probando una nueva netDb retrocompatible que abordará tanto la situación de rutas restringidas que estamos viendo (20% de los routers) como simplificará un poco las cosas. La floodfill netDb se despliega como parte de 0.6.0.3-4 sin ninguna configuración adicional, y básicamente funciona consultando primero dentro de la floodfill db antes de recurrir a la kademlia db existente. Si algunas personas quieren ayudar a probarla, actualicen a 0.6.0.3-4 y pruébenla.

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

El desarrollo de Syndie está avanzando bastante bien, con la sindicación remota completa en funcionamiento y optimizada para las necesidades de I2P (minimizando el número de solicitudes HTTP, y en su lugar agrupando los resultados y las subidas en peticiones HTTP POST multiparte). La nueva sindicación remota significa que puedes ejecutar tu propia instancia local de Syndie, leer y publicar sin conexión, y luego, más adelante, sincronizar tu Syndie con el de otra persona - descargando cualquier entrada nueva y subiendo las entradas creadas localmente (ya sea en lote, por blog o por entrada).

Uno de los sitios públicos de Syndie es syndiemedia.i2p (también accesible en la web en http://syndiemedia.i2p.net/), cuyos archivos públicos están disponibles en http://syndiemedia.i2p/archive/archive.txt (apunta tu nodo de Syndie a esa dirección para sincronizarlo). La 'página principal' en ese syndiemedia se ha filtrado para incluir solo mi blog, de forma predeterminada, pero aún puedes acceder a los demás blogs mediante el menú desplegable y ajustar tu configuración predeterminada en consecuencia. (con el tiempo, el valor predeterminado de syndiemedia.i2p cambiará a un conjunto de publicaciones y blogs introductorios, ofreciendo un buen punto de entrada a syndie).

Un esfuerzo que aún está en marcha es la internacionalización de la base de código de Syndie. He modificado mi copia local para que funcione correctamente con cualquier contenido (cualquier conjunto de caracteres / configuración regional / etc) en cualquier máquina (con conjuntos de caracteres / configuración regional / etc potencialmente diferentes), sirviendo los datos de forma limpia para que el navegador del usuario pueda interpretarlos correctamente. Sin embargo, me he topado con problemas con un componente de Jetty que Syndie utiliza, ya que su clase para manejar solicitudes multiparte internacionalizadas no tiene en cuenta el conjunto de caracteres. Aún ;)

De todos modos, eso significa que, una vez que la parte de internacionalización esté resuelta, el contenido y los blogs podrán renderizarse y editarse en todos los idiomas (pero no traducirse, claro, todavía). Hasta entonces, sin embargo, el contenido creado podría estropearse una vez que la internacionalización esté terminada (ya que hay cadenas UTF-8 dentro de las áreas de contenido firmado). Pero aun así, siéntanse libres de experimentar, y espero tener todo terminado esta noche o mañana en algún momento.

Además, algunas ideas que aún están en el horizonte para SML [3] incluyen una etiqueta [torrent attachment="1"]my file[/torrent] que ofrecería una forma de un solo clic para permitir que la gente lance el torrent adjunto en su cliente BT favorito (susibt, i2p-bt, azneti2p, o incluso un cliente BT no-I2P). ¿Hay demanda de otros tipos de hooks (ganchos) (p. ej., una etiqueta [ed2k]) o la gente tiene ideas totalmente diferentes y descabelladas para distribuir contenido en Syndie?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

¡En fin, hay muchísimas cosas en marcha, así que pásate por la reunión en 10 minutos en irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p o en freenode.net!

=jr
