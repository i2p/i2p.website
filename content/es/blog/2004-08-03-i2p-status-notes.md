---
title: "Notas de estado de I2P del 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Actualización semanal del estado de I2P sobre el rendimiento de la versión 0.3.4, el desarrollo de una nueva consola web y diversos proyectos de aplicaciones"
categories: ["status"]
---

hola a todos, vamos a quitarnos de encima esta actualización de estado

## Índice:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) estado de 0.3.4

Con el lanzamiento 0.3.4 de la semana pasada, la nueva red está funcionando bastante bien - las conexiones irc duran varias horas seguidas y el acceso a eepsite(sitio de I2P) parece ser bastante fiable. El rendimiento sigue siendo en general bajo, aunque ha mejorado ligeramente (antes obtenía de forma constante 4-5KBps, ahora obtengo de forma constante 5-8KBps). oOo ha publicado un par de scripts que resumen la actividad de irc, incluyendo el tiempo de ida y vuelta de los mensajes y la duración de la conexión (basados en el bogobot de hypercubus, que fue recientemente incorporado a CVS)

## 2) En preparación para 0.3.4.1

Como todos los que están en 0.3.4 han notado, fui *cough* un poco verboso en mi registro, lo cual ya se ha corregido en cvs. Además, tras desarrollar algunas herramientas para estresar la ministreaming lib, he añadido un 'choke' (limitador) para que no consuma cantidades enormes de memoria (bloqueará cuando se intente añadir más de 128KB de datos al búfer de un flujo, de modo que, al enviar un archivo grande, tu router no cargue ese archivo completo en memoria). Creo que esto ayudará con los problemas de OutOfMemory que la gente ha estado viendo, pero voy a añadir algo de código adicional de monitorización / depuración para verificarlo.

## 3) Nueva consola web / controlador de I2PTunnel

Además de las modificaciones anteriores para la 0.3.4.1, tenemos lista la primera versión preliminar de la nueva consola del router para algunas pruebas. Por varias razones, aún no la vamos a incluir como parte de la instalación predeterminada, así que habrá instrucciones sobre cómo ponerla en marcha cuando salga la revisión 0.3.4.1 en unos días. Como habéis visto, soy realmente horrible con el diseño web y, como muchos de vosotros habéis estado diciendo, debería dejar de perder el tiempo con la capa de la aplicación y hacer que el núcleo y el router queden sólidos como una roca. Así que, aunque la nueva consola tiene gran parte de la funcionalidad que queremos (configurar el router por completo a través de unas páginas web sencillas, ofrecer un resumen rápido y legible del estado de salud del router, y poner a disposición la capacidad de crear / editar / detener / iniciar distintas instancias de I2PTunnel), de verdad necesito ayuda de gente que sea buena con la parte web.

Las tecnologías usadas en la nueva consola web son JSP estándar, CSS y JavaBeans simples que consultan el router / I2PTunnels para obtener datos y procesan solicitudes. Todo está empaquetado en un par de archivos .war y se despliega en un servidor web Jetty integrado (que debe iniciarse a través de las líneas clientApp.* del router). Los JSPs y JavaBeans principales de la consola del router son técnicamente bastante sólidos, aunque los nuevos JSPs y JavaBeans que desarrollé para gestionar instancias de I2PTunnel son algo chapuceros.

## 4) Cosas de la 0.4

Más allá de la nueva interfaz web, la versión 0.4 incluirá el nuevo instalador de hypercubus, que aún no hemos integrado del todo. También necesitamos realizar algunas simulaciones a gran escala (especialmente la gestión de aplicaciones asimétricas como IRC y outproxies (proxies de salida)). Además, hay algunas actualizaciones que necesito sacar adelante en kaffe/classpath para que podamos poner en marcha la nueva infraestructura web en JVM de código abierto. También tengo que preparar algunos documentos más (uno sobre escalabilidad y otro analizando la seguridad/anonimato en algunos escenarios comunes). Asimismo, queremos que todas las mejoras que propongas se integren en la nueva consola web.

Ah, y corrige cualquier error que ayudes a encontrar :)

## 5) Otras actividades de desarrollo

Si bien se ha avanzado mucho en el sistema base de I2P, eso es solo la mitad de la historia - muchos de ustedes están haciendo un gran trabajo en aplicaciones y bibliotecas para hacer que I2P sea útil. He visto algunas preguntas en el historial del chat sobre quién está trabajando en qué, así que, para ayudar a difundir esa información, aquí está todo lo que sé al respecto (si estás trabajando en algo que no aparece y quieres compartirlo, si estoy equivocado, o si quieres comentar tus avances, ¡por favor, coméntalo!).

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Eso es todo lo que se me ocurre por ahora - pásate por la reunión más tarde esta noche para charlar de cosas. Como siempre, a las 21:00 GMT en #i2p en los servidores de siempre.

=jr
