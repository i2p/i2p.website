---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## Motivación

ECIES-P256 es mucho más rápido que ElGamal. Ya existen algunos eepsites i2pd con tipo de criptografía ECIES-P256 y Java debería poder comunicarse con ellos y viceversa. i2pd lo ha soportado desde la versión 2.16.0 (0.9.32 Java).

## Visión General

Esta propuesta introduce el nuevo tipo de criptografía ECIES-P256 que puede aparecer en la parte del certificado de identidad, o como un tipo de clave de encriptación separado en LeaseSet2. Puede usarse en RouterInfo, LeaseSet1 y LeaseSet2.

### Ubicaciones de Claves ElGamal

Como revisión,
las claves públicas ElGamal de 256 bytes pueden encontrarse en las siguientes estructuras de datos.
Consulte la especificación de estructuras comunes.

- En una Identidad de Router
  Esta es la clave de encriptación del router.

- En un Destino
  La clave pública del destino se utilizó para la antigua encriptación i2cp-to-i2cp
  que fue desactivada en la versión 0.6, actualmente no se usa salvo para
  el IV para encriptación de LeaseSet, que está en desuso.
  En su lugar, se utiliza la clave pública en el LeaseSet.

- En un LeaseSet
  Esta es la clave de encriptación del destino.

En el punto 3 arriba, la clave pública ECIES todavía ocupa 256 bytes, aunque la longitud real de la clave es de 64 bytes.
El resto debe completarse con relleno aleatorio.

- En un LS2
  Esta es la clave de encriptación del destino. El tamaño de la clave es 64 bytes.


### EncTypes en Certificados de Clave

ECIES-P256 usa el tipo de encriptación 1.
Los tipos de encriptación 2 y 3 deben reservarse para ECIES-P284 y ECIES-P521


### Usos de Criptografía Asimétrica

Esta propuesta describe el reemplazo de ElGamal para:

1) Mensajes de Construcción de Túnel (la clave está en RouterIdentity). El bloque de ElGamal es de 512 bytes
  
2) ElGamal+AES/SessionTag de Cliente a Cliente (la clave está en LeaseSet, la clave del Destino no se utiliza). El bloque de ElGamal es de 514 bytes

3) Encriptación de router a router de netdb y otros mensajes I2NP. El bloque de ElGamal es de 514 bytes


### Objetivos

- Compatible hacia atrás
- Sin cambios en la estructura de datos existente
- Mucho más eficiente en CPU que ElGamal

### No Objetivos

- RouterInfo y LeaseSet1 no pueden publicar ElGamal y ECIES-P256 juntos

### Justificación

El motor ElGamal/AES+SessionTag siempre se bloquea debido a la falta de etiquetas, lo que produce una degradación dramática del rendimiento en las comunicaciones de I2P. La construcción del túnel es la operación más pesada porque el originador debe ejecutar la encriptación ElGamal 3 veces por cada solicitud de construcción de túnel.


## Primitivas Criptográficas requeridas

1) Generación de claves de curva EC P256 y DH

2) AES-CBC-256

3) SHA256


## Propuesta Detallada

Un destino con ECIES-P256 se publica a sí mismo con el tipo de criptografía 1 en el certificado. Los primeros 64 bytes de los 256 en la identidad deben interpretarse como la clave pública ECIES y el resto debe ser ignorado. La clave de encriptación separada de LeaseSet se basa en el tipo de clave de la identidad.

### Bloque ECIES para ElGamal/AES+SessionTags
El bloque ECIES reemplaza el bloque ElGamal para ElGamal/AES+SessionTags. La longitud es de 514 bytes.
Consiste en dos partes de 257 bytes cada una. 
La primera parte comienza con cero y luego la clave pública temporal P256 de 64 bytes, el resto de 192 bytes es relleno aleatorio.
La segunda parte comienza con cero y luego 256 bytes cifrados con AES-CBC-256 con el mismo contenido que en ElGamal.

### Bloque ECIES para el registro de construcción de túnel
El registro de construcción de túnel es el mismo, pero sin ceros al inicio en los bloques.
Un túnel puede ser a través de cualquier combinación de tipos de criptografía de routers y se hace por registro.
El originador del túnel cifra los registros dependiendo del tipo de criptografía publicado por el participante del túnel, el participante del túnel descifra en base a su tipo de criptografía.

### Clave AES-CBC-256
Este es el cálculo de claves compartidas ECDH donde el KDF es SHA256 sobre la coordenada x.
Supongamos que Alice es la cifradora y Bob es el descifrador.
Asumamos que k es la clave privada temporal P256 elegida aleatoriamente por Alice y P es la clave pública de Bob.
S es el secreto compartido S(Sx, Sy)
Alice calcula S "acordando" k con P, por ejemplo, S = k*P.

Supongamos que K es la clave pública temporal de Alice y p es la clave privada de Bob.
Bob toma K del primer bloque del mensaje recibido y calcula S = p*K

La clave de encriptación AES es SHA256(Sx) e iv es Sy.
