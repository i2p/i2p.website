---
title: "Comandos de Suscripción a Feeds de Libreta de Direcciones"
description: "Especificación para extender la fuente de suscripción de direcciones con comandos que permitan a los servidores de nombres difundir actualizaciones de entradas desde los poseedores de nombres de host."
slug: "subscription"
aliases:
  - "/es/docs/specs/subscription-spec"
  - "/es/docs/specs/subscription-spec/"
category: "Formatos"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Resumen

Esta especificación extiende el feed de suscripción de direcciones con comandos, para permitir que los servidores de nombres transmitan actualizaciones de entradas de los propietarios de nombres de host. Implementado en la versión 0.9.26, propuesto originalmente en la propuesta 112.

## Motivación

Anteriormente, los servidores de suscripción hosts.txt simplemente enviaban datos en formato hosts.txt, que es el siguiente:

```
example.i2p=b64destination
```
Hay varios problemas con esto:

- Los poseedores de nombres de host no pueden actualizar el Destination asociado con sus nombres de host (para, por ejemplo, actualizar la clave de firma a un tipo más fuerte).
- Los poseedores de nombres de host no pueden renunciar a sus nombres de host de forma arbitraria; deben entregar las claves privadas del Destination correspondiente directamente al nuevo poseedor.
- No hay forma de autenticar que un subdominio esté controlado por el nombre de host base correspondiente; esto actualmente solo se aplica individualmente por algunos servidores de nombres.

## Diseño

Esta especificación añade una serie de líneas de comandos al formato hosts.txt. Con estos comandos, los servidores de nombres pueden extender sus servicios para proporcionar una serie de características adicionales. Los clientes que implementen esta especificación podrán escuchar estas características a través del proceso de suscripción regular.

Todas las líneas de comando deben estar firmadas por el Destination correspondiente. Esto garantiza que los cambios solo se realicen a petición del titular del nombre de host.

## Implicaciones de Seguridad

Esta especificación no afecta el anonimato.

Existe un aumento en el riesgo asociado con perder el control de una clave de Destination, ya que alguien que la obtenga puede usar estos comandos para realizar cambios en cualquier nombre de host asociado. Pero esto no representa un problema mayor que el estado actual, donde alguien que obtiene un Destination puede suplantar un nombre de host y (parcialmente) tomar control de su tráfico. El riesgo aumentado también se equilibra al dar a los propietarios de nombres de host la capacidad de cambiar el Destination asociado con un nombre de host, en caso de que crean que el Destination ha sido comprometido; esto es imposible con el sistema actual.

## Especificación

### Nuevos Tipos de Línea

Hay dos nuevos tipos de líneas:

1. Comandos Add y Change:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Comandos para eliminar:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Ordenación

Un feed no es necesariamente secuencial o completo. Por ejemplo, un comando de cambio puede estar en una línea antes que un comando de agregar, o sin un comando de agregar.

Las claves pueden estar en cualquier orden. No se permiten claves duplicadas. Todas las claves y valores distinguen entre mayúsculas y minúsculas.

### Claves Comunes

Requerido en todos los comandos:

**sig** : Firma B64, usando la clave de firma del destino

Referencias a un segundo nombre de host y/o destino:

**oldname** : Un segundo nombre de host (nuevo o modificado)

**olddest** : Un segundo destino b64 (nuevo o modificado)

**oldsig** : Una segunda firma b64, usando la clave de firma de olddest

Otras claves comunes:

**action** : Un comando

**name** : El nombre del host, solo presente si no está precedido por `example.i2p=b64dest`

**dest** : El destino en b64, solo presente si no está precedido por `example.i2p=b64dest`

**date** : En segundos desde epoch

**expires** : En segundos desde epoch

### Comandos

Todos los comandos excepto el comando "Add" deben contener una clave/valor `action=command`.

Para compatibilidad con clientes más antiguos, la mayoría de comandos van precedidos por `example.i2p=b64dest`, como se indica a continuación. Para cambios, estos son siempre los valores nuevos. Cualquier valor antiguo se incluye en la sección clave/valor.

Las claves listadas son obligatorias. Todos los comandos pueden contener elementos clave/valor adicionales no definidos aquí.

#### Agregar Nombre de Host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host y destino.

**action** : NO se incluye, está implícito.

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!sig=b64sig
```
#### Cambiar Nombre de Host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host y el destino anterior.

**action** : changename

**oldname** : el nombre de host antiguo, a ser reemplazado

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Cambiar Destino

**Precedido por example.i2p=b64dest** : SÍ, este es el nombre de host antiguo y el nuevo destino.

**action** : changedest

**olddest** : el destino antiguo, a ser reemplazado

**oldsig** : firma usando olddest

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Agregar Alias de Nombre de Host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host (alias) y el destino anterior.

**action** : addname

**oldname** : el nombre de host anterior

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Agregar Alias de Destino

(Usado para actualización criptográfica)

**Precedido por example.i2p=b64dest** : SÍ, este es el nombre de host antiguo y el destino nuevo (alternativo).

**action** : adddest

**olddest** : el destino antiguo

**oldsig** : firma usando olddest

**sig** : firma usando dest

Ejemplo:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Agregar Subdominio

**Precedido por subdomain.example.i2p=b64dest** : SÍ, este es el nuevo nombre de subdominio de host y destino.

**action** : addsubdomain

**oldname** : el nombre de host de nivel superior (example.i2p)

**olddest** : el destino de nivel superior (por ejemplo.i2p)

**oldsig** : firma usando olddest

**sig** : firma usando dest

Ejemplo:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Actualizar Metadatos

**Precedido por example.i2p=b64dest** : SÍ, este es el nombre de host y destino anterior.

**action** : update

**sig** : firma

(agregar cualquier clave actualizada aquí)

Ejemplo:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Eliminar Nombre de Host

**Precedido por example.i2p=b64dest** : NO, estos se especifican en las opciones

**action** : remove

**name** : el nombre del host

**dest** : el destino

**sig** : firma

Ejemplo:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Eliminar Todo con Este Destino

**Precedido por example.i2p=b64dest** : NO, estos se especifican en las opciones

**action** : removeall

**name** : el antiguo hostname, solo informativo

**dest** : el dest antiguo, todos los que tienen este dest son eliminados

**sig** : firma

Ejemplo:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Firmas

Todos los comandos deben contener una clave/valor de firma `sig=b64signature` donde la firma es para los otros datos, usando la clave de firma del destino.

Para comandos que incluyan un destino antiguo y nuevo, también debe haber un `oldsig=b64signature`, y ya sea oldname, olddest, o ambos.

En un comando Add o Change, la clave pública para verificación está en el Destination que se va a añadir o cambiar.

En algunos comandos de agregar o editar, puede haber un destino adicional referenciado, por ejemplo al agregar un alias, o cambiar un destino o nombre de host. En ese caso, debe incluirse una segunda firma y ambas deben ser verificadas. La segunda firma es la firma "interna" y se firma y verifica primero (excluyendo la firma "externa"). El cliente debe tomar cualquier acción adicional necesaria para verificar y aceptar los cambios.

oldsig es siempre la firma "interna". Firmar y verificar sin las claves 'oldsig' o 'sig' presentes. sig es siempre la firma "externa". Firmar y verificar con la clave 'oldsig' presente pero sin la clave 'sig'.

#### Entrada para Firmas

Para generar un flujo de bytes para crear o verificar la firma, serializar de la siguiente manera:

- Eliminar la clave "sig"
- Si se verifica con oldsig, también eliminar la clave "oldsig"
- Solo para comandos Add o Change, generar `example.i2p=b64dest`
- Si quedan claves, generar `#!`
- Ordenar las opciones por clave UTF-8, fallar si hay claves duplicadas
- Para cada clave/valor, generar `key=value`, seguido por (si no es la última clave/valor) un `#`

Notas:

- No generar una nueva línea
- La codificación de salida es UTF-8
- Toda la codificación de destino y firma está en Base 64 usando el alfabeto I2P
- Las claves y valores distinguen entre mayúsculas y minúsculas
- Los nombres de host deben estar en minúsculas

## Compatibilidad

Todas las nuevas líneas en el formato hosts.txt se implementan usando caracteres de comentario al inicio, por lo que todas las versiones anteriores de I2P interpretarán los nuevos comandos como comentarios.

Cuando los routers I2P se actualicen a la nueva especificación, no reinterpretarán comentarios antiguos, pero comenzarán a escuchar nuevos comandos en búsquedas posteriores de sus feeds de suscripción. Por lo tanto, es importante que los servidores de nombres persistan las entradas de comandos de alguna manera, o habiliten el soporte de etag para que los routers puedan obtener todos los comandos pasados.
