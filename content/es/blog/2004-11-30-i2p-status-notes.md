---
title: "Notas de estado de I2P para 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Actualización semanal del estado de I2P que abarca las versiones 0.4.2 y 0.4.2.1, avances en mail.i2p, progreso de i2p-bt y discusiones sobre la seguridad de eepsite"
categories: ["status"]
---

Hola a todos

## Índice

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 y 0.4.2.1

Desde que por fin publicamos la 0.4.2, la fiabilidad y el rendimiento de la red se dispararon durante un tiempo, hasta que nos topamos con los errores completamente nuevos que introdujimos. Las conexiones de IRC para la mayoría de la gente están durando horas seguidas, aunque para algunos que se han encontrado con parte de los problemas, ha sido un camino accidentado. No obstante, ha habido numerosas correcciones y, más tarde esta noche o a primera hora de mañana, tendremos una nueva versión 0.4.2.1 lista para descargar.

## 2) mail.i2p

Hoy más temprano, postman me hizo llegar una nota diciendo que tenía algunas cosas que quería discutir - para más información, consulta los registros de la reunión (o, si estás leyendo esto antes de la reunión, acércate).

## 3) i2p-bt

Una de las desventajas de la nueva versión es que estamos teniendo algunos problemas con el port (adaptación) i2p-bt. Algunos de los problemas se han identificado, encontrado y corregido en la biblioteca de streaming, pero se requiere más trabajo para dejarlo donde necesitamos que esté.

## 4) eepsites(Sitios I2P)

Ha habido cierta discusión a lo largo de los meses en la lista, en el canal y en el foro sobre algunos problemas con cómo funcionan los eepsites(I2P Sites) y el eepproxy - recientemente algunos han mencionado problemas con cómo y qué cabeceras se filtran, otros han señalado los peligros de los navegadores mal configurados, y también está la página de DrWoo que resume muchos de los riesgos. Un hecho particularmente digno de mención es que algunas personas están trabajando activamente en applets que secuestrarán el equipo del usuario si este no desactiva los applets. (ASÍ QUE DESACTIVA JAVA Y JAVASCRIPT EN TU NAVEGADOR)

Esto, por supuesto, nos lleva a una discusión sobre cómo podemos asegurar las cosas. He oído sugerencias de crear nuestro propio navegador o de incluir uno con ajustes seguros preconfigurados, pero seamos realistas - eso es mucho más trabajo del que cualquiera aquí está dispuesto a asumir. Sin embargo, hay tres enfoques más:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

La primera es bastante similar a lo que tenemos ahora, excepto que filtramos el contenido renderizado a través de algo como muffin o el filtro de anonimato de freenet. La desventaja aquí es que todavía expone los encabezados HTTP, así que tendríamos que anonimizar también el lado HTTP.

El segundo es muy parecido a lo que se puede ver en `http://duck.i2p/` con el CGIproxy, o, alternativamente, como se puede ver en el fproxy de Freenet. Esto también se encarga del lado HTTP.

La tercera tiene sus ventajas y desventajas - nos permite usar interfaces mucho más atractivas (ya que podemos usar con seguridad cierto JavaScript considerado seguro, etc.), pero tiene la desventaja de la incompatibilidad con versiones anteriores. ¿Quizás una combinación de esto con un filtro, permitiendo incrustar las macros en HTML filtrado?

En cualquier caso, este es un esfuerzo de desarrollo importante y aborda uno de los casos de uso más convincentes de I2P: sitios web interactivos seguros y anónimos. ¿Quizá alguien tenga otras ideas o información sobre cómo podríamos obtener lo necesario?

## 5) ???

Ok, llego tarde a la reunión, así que supongo que debería firmar esto y enviarlo, ¿eh?

=jr [a ver si consigo que gpg funcione bien...]
