---
title: "Verificación de ID de Red de Transporte"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Visión General

NTCP2 (propuesta 111) no rechaza conexiones de diferentes IDs de red
en la fase de Solicitud de Sesión.
La conexión debe rechazarse actualmente en la fase de Sesión Confirmada,
cuando Bob verifica el RI de Alice.

De manera similar, SSU no rechaza conexiones de diferentes IDs de red
en la fase de Solicitud de Sesión.
La conexión debe rechazarse actualmente después de la fase de Sesión Confirmada,
cuando Bob verifica el RI de Alice.

Esta propuesta cambia la fase de Solicitud de Sesión de ambos transportes para incorporar el
ID de red, de una manera compatible hacia atrás.


## Motivación

Las conexiones de la red incorrecta deberían ser rechazadas, y el
compañero debería ser puesto en lista negra, tan pronto como sea posible.


## Objetivos

- Prevenir la contaminación cruzada de redes de prueba y redes bifurcadas

- Agregar ID de red al apretón de manos de NTCP2 y SSU

- Para NTCP2,
  el receptor (conexión entrante) debería poder identificar que el ID de red es diferente,
  para poder poner en lista negra la IP del compañero.

- Para SSU,
  el receptor (conexión entrante) no puede poner en lista negra en la fase de solicitud de sesión, porque
  la IP entrante podría ser falsificada. Es suficiente cambiar la criptografía del apretón de manos.

- Prevenir resiembra desde la red incorrecta

- Debe ser compatible hacia atrás


## No-Objetivos

- NTCP 1 ya no está en uso, por lo que no se cambiará.


## Diseño

Para NTCP2,
hacer XOR con un valor solo causaría que la encriptación falle, y el
receptor no tendría suficiente información para poner en lista negra al originador,
de modo que ese enfoque no es preferido.

Para SSU,
haremos XOR con el ID de red en alguna parte de la Solicitud de Sesión.
Dado que esto debe ser compatible hacia atrás, haremos XOR con (id - 2)
por lo que será una operación nula para el valor actual del ID de red de 2.


## Especificación

### Documentación

Agrega la siguiente especificación para valores válidos de ID de red:


| Uso | Número de NetID |
|-------|--------------|
| Reservado | 0 |
| Reservado | 1 |
| Red Actual (predeterminado) | 2 |
| Redes Futuras Reservadas | 3 - 15 |
| Bifurcaciones y Redes de Prueba | 16 - 254 |
| Reservado | 255 |


La configuración de Java I2P para cambiar el predeterminado es "router.networkID=nnn".
Documenta esto mejor y anima a las bifurcaciones y redes de prueba a agregar esta configuración a su configuración.
Anima a otras implementaciones a implementar y documentar esta opción.


### NTCP2

Usa el primer byte reservado de las opciones (byte 0) en el mensaje de Solicitud de Sesión para contener el ID de red, actualmente 2.
Contiene el ID de red.
Si no es cero, el receptor deberá verificarlo contra el byte de menor peso del ID de red local.
Si no coinciden, el receptor deberá desconectar inmediatamente y poner en lista negra la IP del originador.


### SSU

Para SSU, agrega un XOR de ((netid - 2) << 8) en el cálculo HMAC-MD5.

Existente:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' significa añadir y '^' significa o exclusivo.
  payloadLength es un entero sin signo de 2 bytes
  protocolVersion es un byte 0x00
```

Nuevo:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' significa añadir, '^' significa o exclusivo, '<<' significa desplazamiento a la izquierda.
  payloadLength es un entero sin signo de dos bytes, big endian
  protocolVersion es dos bytes 0x0000, big endian
  netid es un entero sin signo de dos bytes, big endian, los valores legales son 2-254
```


### Resiembra

Agrega un parámetro ?netid=nnn a la obtención del archivo su3 de resiembra.
Actualiza el software de resiembra para verificar el netid. Si está presente y no es igual a "2",
la obtención debe ser rechazada con un código de error, quizás 403.
Agrega una opción de configuración al software de resiembra para que se pueda configurar un netid alternativo
para redes de prueba o bifurcadas.


## Notas

No podemos obligar a las redes de prueba y bifurcaciones a cambiar el ID de red.
Lo mejor que podemos hacer es documentación y comunicación.
Si descubrimos contaminación cruzada con otras redes, deberíamos intentar
contactar a los desarrolladores u operadores para explicar la importancia de cambiar el ID de red.


## Problemas


## Migración

Esto es compatible hacia atrás para el valor actual del ID de red de 2.
Si algunas personas están ejecutando redes (de prueba o de otro tipo) con un valor de ID de red diferente,
este cambio es incompatible hacia atrás.
Sin embargo, no somos conscientes de que alguien lo esté haciendo.
Si es solo una red de prueba, no es un problema, simplemente actualiza todos los enrutadores a la vez.
