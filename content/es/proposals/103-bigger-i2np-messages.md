---
title: "Mensajes I2NP Más Grandes"
number: "103"
author: "zzz"
created: "2009-04-05"
lastupdated: "2009-05-27"
status: "Muerto"
thread: "http://zzz.i2p/topics/258"
---

## Visión General

Esta propuesta trata sobre aumentar el límite de tamaño en los mensajes I2NP.


## Motivación

El uso de datagramas de 12KB por parte de iMule expuso muchos problemas. El límite actual hoy
en día es más como 10KB.


## Diseño

Por hacer:

- Aumentar el límite de NTCP - ¿no es tan fácil?

- Más ajustes en la cantidad de etiquetas de sesión. ¿Podría afectar el tamaño máximo de la ventana? ¿Hay estadísticas que
  observar? ¿Hacer que el número sea variable basado en cuántos creemos que necesitan? ¿Pueden
  pedir más? ¿Pedir una cantidad?

- Investigar el aumento del tamaño máximo de SSU (¿aumentando el MTU?)

- Mucha prueba

- ¿Finalmente comprobar las mejoras del fragmentador? - ¡Necesitamos hacer pruebas de comparación
  primero!
