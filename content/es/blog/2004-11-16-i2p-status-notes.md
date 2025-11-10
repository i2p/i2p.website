---
title: "Notas de estado de I2P para 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Actualización semanal del estado de I2P que abarca problemas de congestión de la red, avances en la biblioteca de streaming, progreso de BitTorrent y planes de próximas versiones"
categories: ["status"]
---

Hola a todos, es martes de nuevo

## Índice

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Congestión

Lo sé, estoy rompiendo la costumbre de llamar al punto 1 "Net status", pero esta semana "congestión" parece apropiada. La red en sí ha estado funcionando bastante bien, pero a medida que aumentaba el uso de bittorrent, las cosas empezaron a saturarse cada vez más, lo que desembocó prácticamente en un colapso por congestión.

Esto era de esperar, y solo refuerza nuestro plan - publicar la nueva biblioteca de streaming y renovar nuestra gestión de tunnels, de modo que tengamos datos suficientes sobre los pares para usar cuando fallen nuestros pares rápidos. Hubo otros factores en juego en los recientes problemas de la red, pero la mayor parte se puede atribuir al aumento de la congestión y a los consiguientes fallos de tunnels (lo que a su vez provocó toda clase de selección de pares descontrolada).

## 2) Transmisión

Ha habido mucho progreso con la streaming lib (biblioteca de transmisión), y he configurado un proxy Squid conectado a ella a través de la red en producción que he estado usando con frecuencia para mi navegación web normal. Con la ayuda de mule, también hemos estado sometiendo los streams (flujos) a bastante presión canalizando frost y FUQID a través de la red (¡Dios mío, nunca me di cuenta de lo agresivo que era frost antes de hacer esto!). De esta manera se han identificado algunos errores significativos de larga data, y se han añadido algunos ajustes para ayudar a controlar cantidades masivas de conexiones.

Los flujos de gran volumen también están funcionando muy bien, con tanto arranque lento como evitación de congestión, y las conexiones rápidas de envío/respuesta (al estilo HTTP get+response) están haciendo exactamente lo que deben.

Espero que reclutemos a algunos voluntarios para intentar desplegarlo más ampliamente durante los próximos días y que, con suerte, podamos llegar pronto a la versión 0.4.2. No quiero decir que vaya a ser tan bueno que te lave los platos, y estoy seguro de que se colarán algunos errores, pero parece prometedor.

## 3) BT

Salvo los problemas recientes de la red, el i2p-bt port (adaptación) ha estado avanzando a pasos agigantados. Sé que algunas personas han descargado más de 1 GB de datos a través de él, y el rendimiento ha sido el esperado (debido a la vieja biblioteca de streaming, ~4KBps por par en el enjambre). Intento seguir el trabajo que se está discutiendo en el canal #i2p-bt; ¿quizá duck podría darnos un resumen en la reunión?

## 4) ???

Eso es todo por mi parte por ahora. Nos vemos en la reunión en unos minutos.

=jr
