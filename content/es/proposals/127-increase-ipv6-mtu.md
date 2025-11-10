---
title: "Aumentar MTU de IPv6"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Visión general

Esta propuesta es para aumentar el MTU máximo de SSU IPv6 de 1472 a 1488.
Implementado en 0.9.28.


## Motivación

El MTU de IPv4 debe ser múltiplo de 16, + 12. El MTU de IPv6 debe ser múltiplo de 16.


Cuando se añadió soporte para IPv6 por primera vez hace años, configuramos el MTU máximo de IPv6 en 1472, menos que el
MTU de IPv4 de 1484. Esto fue para mantener las cosas simples y asegurar que el MTU de IPv6 fuera menor
que el MTU existente de IPv4. Ahora que el soporte para IPv6 es estable, deberíamos poder
establecer el MTU de IPv6 más alto que el MTU de IPv4.

El MTU típico de la interfaz es 1500, por lo que razonablemente podemos aumentar el MTU de IPv6 en 16 a 1488.


## Diseño

Cambiar el máximo de 1472 a 1488.


## Especificación

En las secciones "Router Address" y "MTU" de la descripción general de SSU,
cambiar el MTU máximo de IPv6 de 1472 a 1488.


## Migración

Esperamos que los routers configuren el MTU de conexión como el mínimo del MTU local y remoto,
como de costumbre. No debería ser necesario un chequeo de versión.

Si determinamos que es necesario un chequeo de versión, estableceremos un nivel de versión mínima
de 0.9.28 para este cambio.
