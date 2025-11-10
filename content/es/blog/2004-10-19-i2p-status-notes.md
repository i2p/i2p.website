---
title: "I2P Status Notes for 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Actualización semanal del estado de I2P que cubre la versión 0.4.1.3, mejoras en el rendimiento de tunnel, progreso de la biblioteca de streaming y el motor de búsqueda de files.i2p"
categories: ["status"]
---

Hola a todos, es martes de nuevo

## Índice

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

La versión 0.4.1.3 salió hace uno o dos días y parece que la mayoría se ha actualizado (¡gracias!). La red está funcionando bastante bien, pero todavía no hay un aumento revolucionario en la fiabilidad. Sin embargo, los errores del watchdog de la 0.4.1.2 han desaparecido (o al menos nadie los ha mencionado). Mi objetivo es que esta versión 0.4.1.3 sea el último parche antes de la 0.4.2, aunque, por supuesto, si surge algo importante que haya que corregir, publicaremos otro.

## 2) Tiempo de prueba del Tunnel, y tiempo de procesamiento del envío

Los cambios más significativos en la versión 0.4.1.3 fueron en las pruebas de tunnel - en lugar de tener un período de prueba fijo (¡30 segundos!), ahora tenemos tiempos de espera mucho más agresivos derivados del rendimiento medido. Esto es bueno, ya que ahora marcamos los tunnels como fallidos cuando son demasiado lentos para hacer algo útil. Sin embargo, esto es malo, ya que a veces los tunnels se congestionan temporalmente, y si los probamos durante ese período, marcamos como fallido un tunnel que de otro modo funcionaría.

Un gráfico reciente que muestra cuánto tarda una prueba de tunnel en un router:

Esos son generalmente tiempos de prueba de tunnel aceptables - pasan a través de 4 pares remotos (con tunnels de 2 saltos), lo que sitúa a la mayoría en ~1-200ms por salto. Sin embargo, eso no siempre es así, como se puede ver - a veces tarda del orden de segundos por salto.

Aquí es donde entra el siguiente gráfico - el tiempo de cola desde que un router en particular quiso enviar un mensaje hasta que ese mensaje fue emitido a través de un socket:

Aproximadamente el 95% está por debajo de 50 ms, pero los picos son letales.

Necesitamos eliminar esos picos, además de sortear situaciones con un mayor número de pares que fallan. Tal como está ahora, cuando 'aprendemos' que un par está fallando en nuestros tunnels, en realidad no estamos aprendiendo nada específico de su router: esos picos pueden hacer que incluso los pares de alta capacidad parezcan lentos si coincidimos con uno de esos picos.

## 3) Biblioteca de Streaming

La segunda parte de sortear los tunnels fallidos se logrará en parte gracias a la biblioteca de streaming, proporcionándonos una comunicación de streaming de extremo a extremo mucho más robusta. Esta discusión no es nada nueva - la biblioteca hará todas esas funciones avanzadas de las que hemos estado hablando desde hace tiempo (y, por supuesto, también tendrá su cuota de errores). Ha habido mucho progreso en este frente, y la implementación probablemente esté al 60%.

Más noticias cuando haya más noticias.

## 4) files.i2p

Ok, hemos tenido muchas nuevas eepsites(I2P Sites) últimamente, lo cual es genial. Solo quiero señalar esta en particular porque tiene una función bastante útil para el resto de nosotros. Si no has visitado files.i2p, básicamente es un motor de búsqueda similar a Google, con un caché de los sitios que rastrea (así puedes tanto buscar como navegar cuando el eepsite(I2P Site) está fuera de línea). Muy bueno.

## 5) ???

Las notas de estado de esta semana son bastante breves, pero hay muchas cosas en marcha - - simplemente no tengo tiempo para escribir más antes de la reunión. Así que pásate por #i2p en unos minutos y podemos hablar de cualquier cosa que tontamente haya pasado por alto.

=jr
