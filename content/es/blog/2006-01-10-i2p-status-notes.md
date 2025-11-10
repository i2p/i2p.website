---
title: "Notas de estado de I2P para 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Actualización semanal que cubre algoritmos de perfilado de rendimiento, mejoras en la vista del blog de Syndie, avances en las conexiones HTTP persistentes y el desarrollo de la gwebcache de I2Phex"
categories: ["status"]
---

Hola a todos, parece que ya es martes otra vez

* Index

1) Estado de la red 2) Perfilado de rendimiento 3) Blogs de Syndie 4) Conexiones HTTP persistentes 5) I2Phex gwebcache 6) ???

* 1) Net status

La última semana ha habido muchas correcciones de errores y mejoras en CVS, con la compilación actual en 0.6.1.8-11. La red ha estado razonablemente estable, aunque algunos cortes en distintos proveedores de servicios de I2P provocaron algún que otro contratiempo. Por fin nos deshicimos de la rotación innecesariamente alta de identidades de router en CVS, y hay una nueva corrección de errores en el núcleo que zzz propuso ayer y que parece bastante prometedora, pero tendremos que esperar y ver cómo afecta. Otras dos cosas importantes de la última semana han sido el nuevo perfilado de velocidad basado en el throughput (rendimiento), y trabajo importante en la vista de blog de Syndie. En cuanto a cuándo veremos la 0.6.1.9, debería salir a finales de esta semana, a más tardar el fin de semana. Estén atentos en los lugares de siempre.

* 2) Throughput profiling

Hemos probado algunos algoritmos nuevos de perfilado de pares para supervisar el throughput (rendimiento), pero durante la última semana aproximadamente parece que nos hemos quedado con uno que resulta bastante bueno. En esencia, supervisa el throughput confirmado de tunnels individuales en periodos de 1 minuto, ajustando en consecuencia las estimaciones de throughput para los pares. No intenta calcular una tasa promedio para un par, ya que hacerlo es muy complicado debido a que los tunnels incluyen múltiples pares, así como a que las mediciones de throughput confirmado a menudo requieren múltiples tunnels. En su lugar, calcula una tasa pico promedio - específicamente, mide las tres tasas más altas a las que los tunnels de ese par pudieron transferir y promedia esas.

La esencia es que estas tasas, al medirse durante un minuto completo, representan velocidades sostenidas que el par es capaz de mantener, y dado que cada par es al menos tan rápido como la tasa medida de extremo a extremo, es seguro marcar a cada uno como tan rápido. Habíamos probado otra variante de esto - medir el rendimiento total de un par a través de tunnels en distintos periodos, y eso ofrecía información aún más clara sobre la tasa máxima, pero sesgaba fuertemente en contra de los pares que aún no estaban marcados como "fast", ya que los "fast" se usan con mucha más frecuencia (client tunnels solo usan pares fast). El resultado de esa medición de rendimiento total fue que recopiló datos excelentes para aquellos que estaban suficientemente exigidos, pero solo los pares fast estaban suficientemente exigidos y hubo poca exploración efectiva.

Sin embargo, el uso de intervalos de 1 minuto y del rendimiento de un tunnel individual parece arrojar valores más razonables. Veremos este algoritmo desplegado en la próxima versión.

* 3) Syndie blogs

Basado en algunos comentarios, se han realizado más mejoras en la vista de blog de Syndie, lo que le da un estilo claramente diferente de la vista con hilos similar a los grupos de noticias/foros. Además, ahora cuenta con una capacidad completamente nueva para definir información general del blog a través de la arquitectura existente de Syndie. Como ejemplo, consulta la entrada predeterminada del blog "acerca de Syndie":  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Esto apenas roza el inicio de lo que podemos hacer. La próxima versión te permitirá definir el logotipo de tu propio blog, tus propios enlaces (a blogs, entradas, archivos adjuntos y URLs externas arbitrarias), y con suerte aún más personalización. Una de esas personalizaciones son los iconos por etiqueta - me gustaría incluir un conjunto de iconos predeterminados para usar con etiquetas estándar, pero la gente podrá definir iconos para sus propias etiquetas para usarlos dentro de su blog, e incluso sobrescribir los iconos predeterminados para las etiquetas estándar (de nuevo, solo cuando la gente esté viendo su blog, por supuesto). Quizá incluso alguna configuración de estilo para mostrar las entradas con distintas etiquetas de forma diferente (por supuesto, solo se permitirían personalizaciones de estilo muy específicas - nada de exploits arbitrarios de CSS con Syndie, muchas gracias :)

Aún hay mucho más que me gustaría hacer con la vista del blog que no estará en la próxima versión, pero debería ser un buen empujón para que la gente empiece a explorar algunas de sus funcionalidades, lo cual, con suerte, les permitirá mostrarme lo que *ustedes* necesitan, en lugar de lo que yo creo que quieren. Puede que sea buen programador, pero soy pésimo adivino.

* 4) HTTP persistent connections

zzz es un maniático, te lo digo. Ha habido avances en una función solicitada desde hace mucho: compatibilidad con conexiones HTTP persistentes, que te permiten enviar múltiples solicitudes HTTP sobre un solo flujo, recibiendo múltiples respuestas a cambio. Creo que alguien pidió esto por primera vez hace unos dos años, y podría ayudar bastante con algunos tipos de eepsite(sitio de I2P) o con un uso intensivo de outproxies (proxies de salida). Sé que el trabajo aún no está terminado, pero va avanzando. Esperemos que zzz pueda darnos una actualización del estado durante la reunión.

* 5) I2Phex gwebcache

He oído informes de avances para restaurar el soporte de gwebcache en I2Phex, pero no sé en qué estado se encuentra ahora mismo. Quizás Complication pueda actualizarnos al respecto esta noche?

* 6) ???

Hay mucho en marcha, como pueden ver, pero si hay otras cosas que les gustaría plantear y discutir, pásense por la reunión en unos minutos y peguen un grito. Por cierto, un sitio interesante que he estado siguiendo últimamente es http://freedomarchive.i2p/ (para los perezosos que no tienen I2P instalado, pueden usar el inproxy de Tino (puerta de enlace de entrada) a través de http://freedomarchive.i2p.tin0.de/). En cualquier caso, nos vemos en unos minutos.

=jr
