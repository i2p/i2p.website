---
title: "Notas de estado de I2P del 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Notas semanales sobre el estado del desarrollo de I2P que abarcan el éxito del lanzamiento de la versión 0.5, la próxima corrección de errores 0.5.0.1, estrategias de ordenación de pares de tunnel y actualizaciones de azneti2p"
categories: ["status"]
---

Hola a todos, hora de la actualización semanal

* Index

1) 0.5 2) Próximos pasos 3) azneti2p 4) ???

* 1) 0.5

Como ya habrán oído, por fin lanzamos la 0.5 y, en general, ha ido bastante bien. Agradezco mucho la rapidez con la que los usuarios han actualizado: en el primer día, entre el 50% y el 75% de la red ya estaba en 0.5. Gracias a la rápida adopción, hemos podido ver más pronto el impacto de los distintos cambios y, a su vez, hemos encontrado varios errores. Si bien aún quedan algunos problemas pendientes, esta noche publicaremos una nueva versión 0.5.0.1 para abordar los más importantes.

Como beneficio colateral de los errores, ha sido interesante ver que los routers pueden manejar miles de tunnels ;)

* 2) Next steps

Después de la versión 0.5.0.1, podría haber otra compilación para experimentar con algunos cambios en la construcción de tunnel exploratorios (como usar solo uno o dos pares no fallidos, siendo el resto de alta capacidad, en lugar de que todos los pares sean no fallidos).  Después de eso, daremos el salto hacia la 0.5.1, que mejorará el rendimiento del tunnel (al agrupar varios mensajes pequeños en un único mensaje de tunnel) y permitirá al usuario tener mayor control sobre su susceptibilidad al ataque de predecesor.

Esos controles adoptarán la forma de estrategias de ordenación y selección de pares por cliente, una para la puerta de enlace de entrada y el extremo de salida, y otra para el resto del tunnel.  Esbozo preliminar actual de las estrategias que preveo:  = aleatorio (lo que tenemos ahora)  = equilibrado (intentar explícitamente reducir la frecuencia con la que usamos cada par)  = estricto (si alguna vez usamos A-->B-->C, se mantienen en ese orden
            durante tunnels posteriores [limitado en el tiempo])  = laxo (generar una clave aleatoria para el cliente, calcular el XOR
           entre esa clave y cada par, y ordenar siempre los pares
           seleccionados por la distancia a esa clave [limitado en el tiempo])  = fijo (usar siempre los mismos pares por MBTF)

En fin, ese es el plan, aunque no estoy seguro de qué estrategias se desplegarán primero. Sugerencias más que bienvenidas :)

* 3) azneti2p

La gente de azureus ha estado trabajando duro con un montón de actualizaciones, y su última snapshot b34 [1] parece incluir algunas correcciones de errores relacionadas con I2P. Aunque no he tenido tiempo de auditar el código fuente desde aquel último problema de anonimato que señalé, han corregido ese error en particular, así que, si te sientes con ganas de experimentar, hazte con su actualización y pruébala.

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Hay muchísimas cosas en marcha, y estoy seguro de que ni siquiera me he acercado a cubrirlo todo. Pásate por la reunión en unos minutos y mira qué hay.

=jr
