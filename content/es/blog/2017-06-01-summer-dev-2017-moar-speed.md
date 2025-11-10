---
title: "I2P Summer Dev 2017: ¡AÚN MÁS velocidad!"
date: 2017-06-01
author: "str4d"
description: "El Summer Dev de este año se centrará en la recopilación de métricas y en mejoras de rendimiento para la red."
categories: ["summer-dev"]
---

¡Ha llegado esa época del año otra vez! Estamos iniciando nuestro programa de desarrollo de verano, en el que nos centramos en un aspecto concreto de I2P para hacerlo avanzar. Durante los próximos tres meses, animaremos tanto a nuevos colaboradores como a los miembros actuales de la comunidad a elegir una tarea y disfrutarla.

El año pasado nos centramos en ayudar a usuarios y desarrolladores a aprovechar I2P, mejorando las herramientas de API y dedicando más atención a las aplicaciones que se ejecutan sobre I2P. Este año, queremos mejorar la experiencia de usuario trabajando en un aspecto que afecta a todos: el rendimiento.

Aunque a las redes de enrutamiento de cebolla a menudo se las denomina redes de "baja latencia", existe una sobrecarga significativa creada al enrutar el tráfico a través de equipos adicionales. El diseño de tunnel unidireccional de I2P implica que, de forma predeterminada, un recorrido de ida y vuelta entre dos Destinos ¡involucrará a doce participantes! Mejorar el rendimiento de estos participantes ayudará tanto a reducir la latencia de las conexiones de extremo a extremo como a aumentar la calidad de los tunnels en toda la red.

## ¡MÁS velocidad!

Nuestro programa de desarrollo de este año tendrá cuatro componentes:

### Measure

¡No podemos saber si mejoramos el rendimiento sin una línea base! Crearemos un sistema de métricas para recopilar datos de uso y de rendimiento acerca de I2P de forma que preserve la privacidad, y también adaptaremos diversas herramientas de evaluación de rendimiento para ejecutarse sobre I2P (p. ej., iperf3).

### Medición

Hay mucho margen para mejorar el rendimiento de nuestro código existente, para, por ejemplo, reducir la sobrecarga de participar en tunnels. Estudiaremos posibles mejoras en las primitivas criptográficas, los transportes de red (tanto a nivel de enlace como de extremo a extremo), el perfilado de pares y la selección de rutas de tunnel.

### Optimizar

Tenemos varias propuestas abiertas para mejorar la escalabilidad de la red I2P (p. ej., Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Trabajaremos en estas propuestas y comenzaremos a implementar las propuestas finalizadas en los distintos routers de la red.

### Avanzar

I2P es una red conmutada por paquetes, como Internet, sobre la que se ejecuta. Esto nos brinda una gran flexibilidad en cómo enrutamos los paquetes, tanto para el rendimiento como para la privacidad. ¡La mayor parte de esta flexibilidad permanece inexplorada! Queremos fomentar la investigación sobre cómo diversas técnicas de clearnet (internet abierta) para mejorar el ancho de banda pueden aplicarse a I2P, y cómo podrían afectar la privacidad de los participantes de la red.

## Take part in Summer Dev!

Tenemos muchas más ideas sobre cosas que nos gustaría lograr en estas áreas. Si te interesa trabajar en software de privacidad y anonimato, diseñar protocolos (criptográficos o de otro tipo) o investigar ideas futuras, ¡ven a charlar con nosotros en IRC o Twitter! Siempre nos complace dar la bienvenida a los recién llegados a nuestra comunidad. ¡También enviaremos pegatinas de I2P a todas las nuevas personas colaboradoras que participen!

Iremos publicando aquí a medida que avancemos, pero también puedes seguir nuestro progreso y compartir tus propias ideas y trabajo con el hashtag #I2PSummer en Twitter. ¡Que empiece el verano!
