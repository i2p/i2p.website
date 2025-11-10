---
title: "Notas de estado de I2P del 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Actualización semanal sobre las correcciones de netDb en la 0.5.0.6, los avances en el transporte UDP de SSU, los resultados del perfilado bayesiano de pares y el desarrollo de Q"
categories: ["status"]
---

Hola a todos, toca actualización otra vez

* Index

1) Estado de la red 2) Estado de SSU 3) Perfilado bayesiano de pares 4) Estado de Q 5) ???

* 1) Net status

La versión 0.5.0.6 de la semana pasada parece haber solucionado los problemas de netDb que estábamos viendo (¡bien!). Los sitios y servicios son mucho más fiables que en la 0.5.0.5, aunque ha habido algunos informes de problemas en los que un sitio o servicio se vuelve inaccesible después de unos días de tiempo de actividad.

* 2) SSU status

Ha habido muchos avances en el código UDP 0.6, con el primer lote de commits ya realizados en CVS. Aún no es algo que realmente puedas usar, pero los fundamentos están establecidos. La negociación de sesión funciona bien y la entrega de mensajes semiconfiable se comporta como se espera. Aun así, todavía queda mucho trabajo por hacer: hay que escribir casos de prueba y depurar situaciones atípicas, pero es un avance.

Si todo va bien, podríamos tener algunas pruebas alfa la próxima semana, solo para personas que puedan configurar explícitamente sus cortafuegos/NAT. Me gustaría dejar afinado el funcionamiento general primero antes de añadir el relay handler (manejador de relay), ajustar la netDb para una caducidad de routerInfo más rápida y seleccionar relays para publicar. También voy a aprovechar esta oportunidad para realizar toda una batería de pruebas, ya que se están abordando varios factores críticos de encolado.

* 3) Bayesian peer profiling

bla ha estado trabajando intensamente en algunas revisiones sobre cómo decidimos a través de qué pares enrutar mediante tunnel, y aunque bla no pudo asistir a la reunión, hay algunos datos interesantes que informar:

<+bla> He realizado mediciones directas de velocidad de nodos: he perfilado unos 150 nodos usando OB tunnels de longitud 0, IB tunnels de longitud 1, batching-interval = 0ms
<+bla> Además, acabo de hacer una estimación de velocidad _muy_ básica y _preliminar_ usando clasificación bayesiana ingenua
<+bla> Esto último se hizo usando las longitudes por defecto de los expl. tunnels (tunnels exploratorios)
<+bla> La intersección entre el conjunto de nodos sobre los que tengo "ground truth" (valores de referencia), y el conjunto de nodos de las mediciones actuales, es de 117 nodos
<+bla> Los resultados no son _tan_ malos, pero tampoco demasiado impresionantes
<+bla> Ver http://theland.i2p/estspeed.png
<+bla> La separación básica entre muy lentos y rápidos está más o menos bien, pero la separación de grano fino entre los pares más rápidos podría ser mucho mejor
<+jrandom2p> hmm, ¿cómo se calcularon los valores reales? ¿es el RTT (tiempo de ida y vuelta) completo o es RTT/longitud?
<+bla> Usando los expl. tunnels normales, es casi imposible evitar los retardos por agrupación.
<+bla> Los valores reales son los de ground-truth: aquellos obtenidos usando OB=0 e IB=1
<+bla> (y variance=0, y sin retardo por agrupación)
<+jrandom2p> aun así, desde aquí los resultados se ven bastante buenos
<+bla> Los tiempos estimados son los obtenidos usando inferencia bayesiana a partir de expl. tunnels _reales_ de longitud 2 +/- 1
<+bla> Esto se obtuvo a partir de 3000 RTTs, registrados durante un período de unas 3 horas (eso es mucho)
<+bla> Esto asume (por el momento) que la velocidad de los pares es estática. Aún tengo que implementar la ponderación
<+jrandom2p> suena increíble. buen trabajo, bla
<+jrandom2p> hmm, entonces la estimación debería ser igual a 1/4 de la real
<+bla> jrandom: No: Todos los RTT medidos (usando los expl. tunnels normales) se corrigen por el número de saltos en el recorrido de ida y vuelta
<+jrandom2p> ah, ok
<+bla> Solo después de eso se entrena el clasificador bayesiano
<+bla> Por ahora, agrupo los tiempos medidos por salto en 10 clases: 50, 100, ..., 450 ms, y una clase adicional >500 ms
<+bla> Por ejemplo, los retrasos pequeños por salto podrían ponderarse con un factor mayor, al igual que los fallos completos (>60000 ms).
<+bla> Aunque... el 65% de los tiempos estimados caen dentro de 0.5 desviaciones estándar del tiempo real del nodo
<+bla> Sin embargo, esto hay que rehacerlo, ya que la desviación estándar está muy influida por los fallos >60000 ms

Tras debatirlo más a fondo, bla presentó una comparación frente a la calculadora de velocidad existente, publicada @ http://theland.i2p/oldspeed.png Los espejos de esos PNG están disponibles en http://dev.i2p.net/~jrandom/estspeed.png y http://dev.i2p.net/~jrandom/oldspeed.png

(para la terminología, IB=saltos de tunnel entrantes, OB=saltos de tunnel salientes, y, tras algunas aclaraciones, las mediciones de "ground truth" (mediciones de referencia) se obtuvieron con 1 salto de salida y 0 saltos de entrada, no al revés)

* 4) Q status

Aum también ha avanzado mucho en Q; recientemente ha estado trabajando en una interfaz de cliente web. La próxima compilación de Q no será compatible con versiones anteriores, ya que incluye una gran cantidad de nuevas funciones, pero estoy seguro de que sabremos más de Aum cuando haya más información que compartir :)

* 5) ???

Eso es todo por el momento (tengo que terminar esto antes de la hora de la reunión). Ah, por cierto, parece que me mudaré antes de lo previsto, así que quizá algunas de las fechas en la hoja de ruta se muevan mientras estoy en tránsito hacia donde acabe. De todos modos, pásate por el canal en unos minutos para bombardearnos con ideas nuevas.

=jr
