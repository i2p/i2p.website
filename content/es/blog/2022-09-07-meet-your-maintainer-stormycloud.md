---
title: "Conoce a tu mantenedor: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Una entrevista con los mantenedores del Outproxy (proxy de salida) de StormyCloud"
categories: ["general"]
API_Translate: verdadero
---

## Una conversación con StormyCloud Inc.

Con la versión más reciente de [I2P Java](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release), el outproxy (proxy de salida) existente, false.i2p, fue reemplazado por el nuevo outproxy StormyCloud para las nuevas instalaciones de I2P. Para las personas que estén actualizando su router, el cambio al servicio Stormycloud puede hacerse rápidamente.

En el Administrador de Servicios Ocultos, cambia tanto Outproxies como SSL Outproxies a exit.stormycloud.i2p y haz clic en el botón Guardar en la parte inferior de la página.

## ¿Quién es StormyCloud Inc.?

**Misión de StormyCloud Inc.**

Defender el acceso a Internet como un derecho humano universal. Al hacerlo, el grupo protege la privacidad electrónica de los usuarios y fortalece la comunidad fomentando el acceso sin restricciones a la información y, de ese modo, el libre intercambio de ideas a través de las fronteras. Esto es esencial porque Internet es la herramienta más poderosa disponible para marcar una diferencia positiva en el mundo.

**Declaración de la visión**

Convertirse en pionero en ofrecer Internet libre y abierto a todas las personas del universo, porque el acceso a Internet es un derecho humano básico ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Me reuní con Dustin para saludar y hablar más sobre la privacidad, la necesidad de servicios como StormyCloud y qué atrajo a la empresa a I2P.

**¿Qué inspiró la creación de StormyCloud?**

A finales de 2021, estaba en el subreddit /r/tor. Había una persona que había respondido en un hilo sobre cómo usar Tor y que contaba que dependía de Tor para mantenerse en contacto con su familia. Su familia vivía en Estados Unidos, pero en ese momento esa persona residía en un país donde el acceso a Internet estaba muy restringido. Tenía que extremar las precauciones sobre con quién se comunicaba y qué decía. Por estas razones, dependía de Tor. Pensé en cómo puedo comunicarme con la gente sin miedo ni restricciones y en que debería ser igual para todos.

El objetivo de StormyCloud es ayudar al mayor número de personas posible a hacerlo.

**¿Cuáles han sido algunos de los desafíos de poner en marcha StormyCloud?**

El costo — es escandalosamente caro. Optamos por utilizar un centro de datos, ya que la escala de lo que estamos haciendo no es algo que pueda hacerse en una red doméstica. Hay gastos de equipamiento y costos de alojamiento recurrentes.

Con respecto a la creación de la organización sin fines de lucro, seguimos los pasos de Emerald Onion y utilizamos algunos de sus documentos y lecciones aprendidas. La comunidad de Tor cuenta con muchos recursos disponibles que son de gran ayuda.

**¿Cómo ha sido la respuesta a sus servicios?**

En julio atendimos 1.500 millones de solicitudes DNS en todos nuestros servicios. La gente valora que no se realizan registros. Los datos sencillamente no existen, y eso le gusta a la gente.

**¿Qué es un outproxy?**

Un outproxy (proxy de salida) es similar a los nodos de salida de Tor, permite que el tráfico de clearnet (tráfico normal de internet) se retransmita a través de la red I2P. En otras palabras, permite que los usuarios de I2P accedan a internet con la seguridad de la red I2P.

**¿Qué tiene de especial el Outproxy (proxy de salida) de I2P de StormyCloud?**

Para empezar, somos multi-homed (con múltiples servidores), es decir, contamos con varios servidores que atienden tráfico de outproxy (proxy de salida). Esto garantiza que el servicio siempre esté disponible para la comunidad. Todos los registros en nuestros servidores se eliminan cada 15 minutos. Esto garantiza que ni las fuerzas del orden ni nosotros tengamos acceso a ningún dato. Admitimos visitar enlaces onion de Tor a través del outproxy, y nuestro outproxy es bastante rápido.

**¿Cómo define la privacidad? ¿Cuáles son algunos de los problemas que observa con la extralimitación y el tratamiento de datos?**

La privacidad es la libertad frente al acceso no autorizado. La transparencia es importante, como el consentimiento expreso (opt-in) — un ejemplo de ello son los requisitos del RGPD.

Hay grandes empresas que acaparan datos que se utilizan para [acceso a datos de ubicación sin orden judicial](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). Hay un exceso de intromisión de las empresas tecnológicas en lo que la gente considera que es, y debería ser, privado, como fotos o mensajes.

Es importante seguir realizando esfuerzos de divulgación sobre cómo mantener seguras las comunicaciones y qué herramientas o aplicaciones pueden ayudar a una persona a hacerlo. También es importante la manera en que interactuamos con toda la información disponible. Debemos confiar, pero verificar.

**¿Cómo encaja I2P en la declaración de misión y visión de StormyCloud?**

I2P es un proyecto de código abierto, y lo que ofrece está alineado con la misión de StormyCloud Inc. I2P proporciona una capa de privacidad y protección para el tráfico y la comunicación, y el proyecto cree que todas las personas tienen derecho a la privacidad.

Nos enteramos de I2P a principios de 2022 al hablar con personas de la comunidad de Tor, y nos gustó lo que estaba haciendo el proyecto. Parecía similar a Tor.

Durante nuestra introducción a I2P y sus capacidades, vimos la necesidad de un outproxy (proxy de salida) fiable. Recibimos un gran apoyo de miembros de la comunidad de I2P para crear y empezar a ofrecer el servicio de outproxy.

**Conclusión**

La necesidad de conciencia sobre la vigilancia de lo que debería ser privado en nuestras vidas en línea es constante. La recopilación de cualquier dato debe realizarse con consentimiento, y la privacidad debería ser implícita.

Cuando no podemos confiar en que nuestro tráfico o nuestras comunicaciones no vayan a ser observados sin nuestro consentimiento, afortunadamente tenemos acceso a redes que, por diseño, anonimizarán el tráfico y ocultarán nuestras ubicaciones.

Gracias a StormyCloud y a todas las personas que proporcionan outproxies (proxies de salida) o nodos para Tor e I2P, para que la gente pueda acceder a Internet de forma más segura cuando lo necesite. Espero que más personas integren las capacidades de estas redes complementarias para crear un ecosistema de privacidad más robusto para todos.

Obtén más información sobre los servicios de StormyCloud Inc. en [https://stormycloud.org/](https://stormycloud.org/) y apoya su trabajo realizando una donación en [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
