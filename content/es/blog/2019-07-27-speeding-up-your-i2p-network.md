---
title: "Aumentar la velocidad de su red I2P"
date: 2019-07-27
author: "mhatta"
description: "Acelerar tu red I2P"
categories: ["tutorial"]
---

*Esta entrada está adaptada directamente a partir de material creado originalmente para el de mhatta* [blog de Medium](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Él merece el crédito por la publicación original. Se ha actualizado en ciertos lugares donde* *se refiere a versiones antiguas de I2P como si fueran actuales y ha sido objeto de una ligera* *edición. -idk*

Justo después de iniciarse, I2P suele percibirse como algo lento. Es cierto, y todos sabemos por qué: por su propia naturaleza, [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) (enrutamiento garlic) añade sobrecarga a la experiencia familiar de usar Internet para que puedas tener privacidad, pero esto significa que, para muchos o la mayoría de los servicios de I2P, tus datos tendrán que pasar por 12 saltos de forma predeterminada.

![Análisis de herramientas para el anonimato en línea](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Además, a diferencia de Tor, I2P se diseñó principalmente como una red cerrada. Puedes acceder fácilmente a [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) u otros recursos dentro de I2P, pero no está pensado para acceder a sitios web de [clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking)) (Internet abierta) a través de I2P. Existen algunos "outproxies" (proxies de salida) de I2P similares a los nodos de salida de [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)) para acceder a la clearnet, pero la mayoría son muy lentos de usar, ya que ir a la clearnet es efectivamente *otro* salto en una conexión que ya tiene 6 saltos de entrada y seis de salida.

Hasta hace unas pocas versiones, este problema era incluso más difícil de abordar porque muchos usuarios del router de I2P tenían dificultades para configurar los parámetros de ancho de banda de sus routers. Si todos los que pueden se toman el tiempo para ajustar correctamente sus parámetros de ancho de banda, mejorarán no solo tu conexión, sino también la red de I2P en su conjunto.

## Ajuste de los límites de ancho de banda

Como I2P es una red peer-to-peer, tienes que compartir parte de tu ancho de banda de red con otros pares. Puedes elegir cuánto en "Configuración de ancho de banda de I2P" (botón "Configurar ancho de banda" en la sección "Aplicaciones y Configuración" de la I2P Router Console, o http://localhost:7657/config).

![Configuración de ancho de banda de I2P](https://geti2p.net/images/blog/bandwidthmenu.png)

Si ve un límite de ancho de banda compartido de 48 KBps, que es muy bajo, es posible que no haya ajustado su ancho de banda compartido respecto al valor predeterminado. Como señaló el autor original del material en el que se basa esta entrada del blog, I2P tiene un límite predeterminado de ancho de banda compartido que es muy bajo hasta que el usuario lo ajusta para evitar causar problemas con la conexión del usuario.

Sin embargo, dado que muchos usuarios quizá no sepan exactamente qué ajustes de ancho de banda deben modificar, la [versión 0.9.38 de I2P](https://geti2p.net/en/download) introdujo un Asistente de nueva instalación. Incluye una Prueba de ancho de banda, que detecta automáticamente (gracias al [NDT](https://www.measurementlab.net/tests/ndt/) de M-Lab) y ajusta en consecuencia la configuración de ancho de banda de I2P.

Si desea volver a ejecutar el asistente, por ejemplo tras un cambio en su proveedor de servicios o porque instaló I2P antes de la versión 0.9.38, puede volver a iniciarlo desde el enlace 'Setup' en la página 'Help & FAQ', o simplemente acceder al asistente directamente en http://localhost:7657/welcome

![¿Puedes encontrar "Setup"?](https://geti2p.net/images/blog/sidemenu.png)

Usar el Asistente es sencillo, simplemente sigue haciendo clic en "Next". A veces los servidores de medición seleccionados por M-Lab están caídos y la prueba falla. En ese caso, haz clic en "Previous" (no uses el botón "back" de tu navegador web), y luego vuelve a intentarlo.

![Resultados de la prueba de ancho de banda](https://geti2p.net/images/blog/bwresults.png)

## Ejecución continua de I2P

Incluso después de ajustar el ancho de banda, tu conexión podría seguir siendo lenta. Como dije, I2P es una red P2P. Tomará algo de tiempo para que tu I2P router sea descubierto por otros pares y se integre en la red de I2P. Si tu router no permanece encendido el tiempo suficiente para integrarse bien, o si lo apagas de forma abrupta con demasiada frecuencia, la red seguirá siendo bastante lenta. Por otro lado, cuanto más tiempo mantengas tu I2P router en ejecución de manera continua, más rápida y estable será tu conexión, y más de tu ancho de banda se utilizará en la red.

Sin embargo, muchas personas quizá no puedan mantener su I2P router en funcionamiento. En tal caso, aún puede ejecutar el I2P router en un servidor remoto, como un VPS, y luego usar el reenvío de puertos mediante SSH.
