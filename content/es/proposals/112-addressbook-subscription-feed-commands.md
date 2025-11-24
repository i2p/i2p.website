---
title: "Comandos de Feed de Suscripción de Libreta de Direcciones"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Closed"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Nota
Despliegue de la red completado.
Ver [SPEC](/docs/specs/subscription/) para la especificación oficial.


## Descripción General

Esta propuesta trata sobre la extensión del feed de suscripción de direcciones con comandos, para permitir que los servidores de nombres transmitan actualizaciones de entradas de los titulares de nombres de host. Implementado en 0.9.26.


## Motivación

Actualmente, los servidores de suscripción hosts.txt solo envían datos en un formato hosts.txt, que es el siguiente:

  ```text
  example.i2p=b64destination
  ```

Hay varios problemas con esto:

- Los titulares de nombres de host no pueden actualizar el Destino asociado con sus nombres de host (para, por ejemplo, actualizar la clave de firma a un tipo más fuerte).
- Los titulares de nombres de host no pueden renunciar a sus nombres de host de manera arbitraria; deben entregar las claves privadas del Destino correspondiente directamente al nuevo titular.
- No hay forma de autenticar que un subdominio es controlado por el nombre de host base correspondiente; esto actualmente solo se aplica individualmente en algunos servidores de nombres.


## Diseño

Esta propuesta añade una serie de líneas de comando al formato hosts.txt. Con estos comandos, los servidores de nombres pueden extender sus servicios para proporcionar una serie de características adicionales. Los clientes que implementen esta propuesta podrán escuchar estas características a través del proceso de suscripción habitual.

Todas las líneas de comando deben estar firmadas por el Destino correspondiente. Esto asegura que los cambios solo se realicen a petición del titular del nombre de host.


## Implicaciones de Seguridad

Esta propuesta no tiene implicaciones sobre el anonimato.

Hay un aumento en el riesgo asociado con perder el control de una clave de Destino, ya que alguien que la obtenga puede usar estos comandos para realizar cambios en cualquier nombre de host asociado. Sin embargo, esto no es más problemático que el estado actual, donde alguien que obtenga un Destino puede hacerse pasar por un nombre de host y (parcialmente) tomar el control de su tráfico. El aumento del riesgo también se compensa al dar a los titulares de nombres de host la capacidad de cambiar el Destino asociado con un nombre de host, en el caso de que crean que el Destino ha sido comprometido; esto es imposible con el sistema actual.


## Especificación

### Nuevos tipos de líneas

Esta propuesta añade dos nuevos tipos de líneas:

1. Añadir y Cambiar comandos:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. Eliminar comandos:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### Orden
Un feed no está necesariamente en orden o completo. Por ejemplo, un comando de cambio puede estar en una línea antes de un comando de adición, o sin un comando de adición.

Las claves pueden estar en cualquier orden. No se permiten claves duplicadas. Todas las claves y valores son sensibles a mayúsculas y minúsculas.


### Claves comunes

Requerido en todos los comandos:

sig
  Firma en B64, usando la clave de firma del destino

Referencias a un segundo nombre de host y/o destino:

oldname
  Un segundo nombre de host (nuevo o cambiado)
olddest
  Un segundo destino b64 (nuevo o cambiado)
oldsig
  Una segunda firma b64, usando la clave de firma de nolddest

Otras claves comunes:

action
  Un comando
name
  El nombre de host, solo presente si no está precedido por example.i2p=b64dest
dest
  El destino b64, solo presente si no está precedido por example.i2p=b64dest
date
  En segundos desde la época
expires
  En segundos desde la época


### Comandos

Todos los comandos, excepto el comando "Añadir", deben contener una clave/valor "action=command".

Para compatibilidad con clientes más antiguos, la mayoría de los comandos están precedidos por example.i2p=b64dest, como se señala a continuación. Para cambios, estos son siempre los nuevos valores. Cualquier valor antiguo se incluye en la sección de clave/valor.

Las claves listadas son obligatorias. Todos los comandos pueden contener elementos clave/valor adicionales no definidos aquí.

#### Añadir nombre de host
Precedido por example.i2p=b64dest
  SÍ, este es el nuevo nombre de host y destino.
action
  NO incluido, es implícito.
sig
  firma

Ejemplo:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Cambiar nombre de host
Precedido por example.i2p=b64dest
  SÍ, este es el nuevo nombre de host y el destino antiguo.
action
  changename
oldname
  el nombre de host antiguo, a ser reemplazado
sig
  firma

Ejemplo:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Cambiar destino
Precedido por example.i2p=b64dest
  SÍ, este es el antiguo nombre de host y el nuevo destino.
action
  changedest
olddest
  el antiguo destino, a ser reemplazado
oldsig
  firma usando olddest
sig
  firma

Ejemplo:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Añadir alias de nombre de host
Precedido por example.i2p=b64dest
  SÍ, este es el nuevo (alias) nombre de host y el destino antiguo.
action
  addname
oldname
  el nombre de host antiguo
sig
  firma

Ejemplo:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Añadir alias de destino
(Usado para la actualización criptográfica)

Precedido por example.i2p=b64dest
  SÍ, este es el antiguo nombre de host y el nuevo destino (alternativo).
action
  adddest
olddest
  el antiguo destino
oldsig
  firma usando olddest
sig
  firma usando dest

Ejemplo:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Añadir subdominio
Precedido por subdomain.example.i2p=b64dest
  SÍ, este es el nuevo nombre de subdominio de host y destino.
action
  addsubdomain
oldname
  el nombre de host de nivel superior (example.i2p)
olddest
  el destino de nivel superior (para example.i2p)
oldsig
  firma usando olddest
sig
  firma usando dest

Ejemplo:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Actualizar metadatos
Precedido por example.i2p=b64dest
  SÍ, este es el antiguo nombre de host y destino.
action
  update
sig
  firma

(añadir cualquier clave actualizada aquí)

Ejemplo:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Eliminar nombre de host
Precedido por example.i2p=b64dest
  NO, estos se especifican en las opciones
action
  remove
name
  el nombre de host
dest
  el destino
sig
  firma

Ejemplo:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Eliminar todo con este destino
Precedido por example.i2p=b64dest
  NO, estos se especifican en las opciones
action
  removeall
name
  el antiguo nombre de host, solo a título informativo
dest
  el antiguo destino, todos con este destino son eliminados
sig
  firma

Ejemplo:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```


### Firmas

Todos los comandos deben contener una clave/valor de firma "sig=b64signature" donde se firma la otra información, usando la clave de firma del destino.

Para comandos que incluyen un destino antiguo y nuevo, también debe haber una oldsig=b64signature, y ya sea oldname, olddest, o ambos.

En un comando de Añadir o Cambiar, la clave pública para verificación está en el Destino a ser añadido o cambiado.

En algunos comandos de añadir o editar, puede haber un destino adicional referenciado, por ejemplo, al añadir un alias, o cambiar un destino o nombre de host. En ese caso, debe incluirse una segunda firma y ambas deben ser verificadas. La segunda firma es la firma "interna" y se firma y verifica primero (excluyendo la firma "externa"). El cliente debe realizar cualquier acción adicional necesaria para verificar y aceptar cambios.

oldsig es siempre la firma "interna". Se firma y verifica sin las claves 'oldsig' o 'sig' presentes. sig es siempre la firma "externa". Se firma y verifica con la clave 'oldsig' presente pero no la clave 'sig'.

#### Entrada para firmas
Para generar un flujo de bytes para crear o verificar la firma, serializar de la siguiente manera:

- Eliminar la clave "sig"
- Si se verifica con oldsig, también eliminar la clave "oldsig"
- Solo para comandos de Añadir o Cambiar,
  salida example.i2p=b64dest
- Si quedan claves, salida "#!"
- Ordenar las opciones por clave UTF-8, fallar si hay claves duplicadas
- Para cada clave/valor, salida clave=valor, seguido (si no es la última clave/valor) por un '#'

Notas

- No emitir un salto de línea
- La codificación de salida es UTF-8
- Toda la codificación de destino y firma es en Base 64 usando el alfabeto I2P
- Las claves y los valores distinguen entre mayúsculas y minúsculas
- Los nombres de host deben estar en minúsculas


## Compatibilidad

Todas las nuevas líneas en el formato hosts.txt se implementan usando caracteres de comentario al principio, por lo que todas las versiones antiguas de I2P interpretarán los nuevos comandos como comentarios.

Cuando los routers I2P se actualicen a la nueva especificación, no reinterpretarán los comentarios antiguos, pero comenzarán a escuchar nuevos comandos en recuperaciones posteriores de sus feeds de suscripción. Por lo tanto, es importante que los servidores de nombres persistan las entradas de comando de alguna manera, o habiliten el soporte etag para que los routers puedan recuperar todos los comandos anteriores.



