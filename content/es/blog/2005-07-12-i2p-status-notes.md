---
title: "Notas de estado de I2P del 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Actualización semanal sobre el restablecimiento del servicio, el progreso de las pruebas de SSU y el análisis de la capa criptográfica de I2CP para una posible simplificación"
categories: ["status"]
---

Hola a todos, ya llegó otra vez esa hora de la semana

* Index

1) squid/www/cvs/dev.i2p restaurado 2) pruebas de SSU 3) criptografía de I2CP 4) ???

* 1) squid/www/cvs/dev.i2p restored

Después de romperme la cabeza con varios servidores en colocation, algunos de los servicios antiguos se han restablecido - squid.i2p (uno de los dos outproxies predeterminados), www.i2p (un enlace seguro a www.i2p.net), dev.i2p (un enlace seguro a dev.i2p.net, donde se encuentran los archivos de las listas de correo, cvsweb y las semillas predeterminadas de netDb), y cvs.i2p (un enlace seguro a nuestro servidor CVS - cvs.i2p.net:2401). Mi blog sigue desaparecido, pero su contenido se perdió de todos modos, así que habrá que empezar de cero tarde o temprano. Ahora que estos servicios vuelven a estar en línea de forma fiable, es hora de pasar a la...

* 2) SSU testing

Como se menciona en ese pequeño recuadro amarillo en la consola del router de cada uno, hemos iniciado la siguiente ronda de pruebas en la red real para SSU. Las pruebas no son para todo el mundo, pero si eres aventurero y te sientes cómodo realizando algo de configuración manual, consulta los detalles indicados en tu consola del router (http://localhost:7657/index.jsp). Puede que haya varias rondas de pruebas, pero no preveo cambios importantes en SSU antes de la versión 0.6 (0.6.1 añadirá compatibilidad para quienes no puedan configurar el reenvío de puertos o, de otro modo, no puedan recibir conexiones UDP entrantes).

* 3) I2CP crypto

Al trabajar de nuevo en la nueva documentación introductoria, tengo cierta dificultad para justificar la capa adicional de cifrado realizada dentro del I2CP SDK. La intención original de la capa criptográfica de I2CP era proporcionar una protección básica de extremo a extremo de los mensajes transmitidos, así como permitir que los clientes I2CP (es decir, I2PTunnel, the SAM bridge, I2Phex, azneti2p, etc) se comuniquen a través de routers no confiables. Sin embargo, a medida que avanzó la implementación, la protección de extremo a extremo de la capa I2CP se ha vuelto redundante, ya que todos los mensajes del cliente están cifrados de extremo a extremo por el router dentro de mensajes garlic, incluyendo el leaseSet del remitente y, a veces, un mensaje de estado de entrega. Esta capa garlic ya proporciona cifrado de extremo a extremo desde el router del remitente hasta el router del receptor - la única diferencia es que no protege contra que ese router en sí sea hostil.

Sin embargo, considerando los casos de uso previsibles, no logro encontrar un escenario válido en el que no se confiara en el router local. Como mínimo, el cifrado de I2CP solo oculta el contenido del mensaje transmitido desde el router - el router todavía necesita saber a qué destino debe enviarse. Si es necesario, podemos añadir un listener I2CP SSH/SSL para permitir que el cliente I2CP y el router funcionen en máquinas separadas, o quienes necesiten tales escenarios pueden usar herramientas de tunnelling existentes.

Solo para reiterar las capas de cifrado que se usan ahora mismo, tenemos:  * La capa ElGamal/AES+SessionTag de extremo a extremo de I2CP, que cifra desde    el destino del remitente hasta el destino del destinatario.  * La capa de garlic encryption (cifrado 'garlic') de extremo a extremo del router    (ElGamal/AES+SessionTag), que cifra desde el router del remitente hasta    el router del destinatario.  * La capa de cifrado del tunnel para los tunnels entrantes y salientes    en los saltos a lo largo de cada uno (pero no entre el punto final del    saliente y la puerta de enlace del entrante).  * La capa de cifrado de transporte entre cada router.

Quiero ser bastante prudente a la hora de eliminar una de esas capas, pero no quiero malgastar nuestros recursos haciendo trabajo innecesario. Lo que propongo es eliminar esa primera capa de cifrado de I2CP (pero, por supuesto, manteniendo la autenticación utilizada durante el establecimiento de la sesión de I2CP, la autorización de leaseSet y la autenticación del remitente). ¿Alguien puede dar una razón por la que deberíamos mantenerla?

* 4) ???

Eso es todo por el momento, pero como siempre hay mucho en marcha. Seguimos sin reunión esta semana, pero si alguien tiene algo que plantear, por favor no dude en publicarlo en la lista o en el foro. Además, aunque leo el historial en #i2p, las preguntas o inquietudes generales deberían enviarse a la lista para que más personas puedan participar en la discusión.

=jr
