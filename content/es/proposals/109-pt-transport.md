---
title: "PT Transporte"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Abierto"
thread: "http://zzz.i2p/topics/1551"
---

## Resumen

Esta propuesta es para crear un transporte de I2P que se conecte a otros routers
a través de Transportes Enchufables.


## Motivación

Los Transportes Enchufables (PTs) fueron desarrollados por Tor como una forma de añadir transportes de ofuscación a los puentes de Tor de manera modular.

I2P ya tiene un sistema de transporte modular que disminuye la barrera para añadir
transportes alternativos. Añadir soporte para PTs proporcionaría a I2P una manera fácil de experimentar con protocolos alternativos, y prepararse para resistir bloqueos.


## Diseño

Existen algunas capas potenciales de implementación:

1. Un PT genérico que implementa SOCKS y ExtORPort y configura y bifurca los
   procesos de entrada y salida, y se registra con el sistema de comunicación. Esta capa no sabe
   nada sobre NTCP, y puede o no utilizar NTCP. Bueno para pruebas.

2. Basándose en 1), un PT NTCP genérico que se basa en el código de NTCP y canaliza
   NTCP a 1).

3. Basándose en 2), un PT NTCP-xxxx específico configurado para ejecutar un proceso externo dado de entrada
   y salida.
