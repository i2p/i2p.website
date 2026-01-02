---
title: "Comandos de la fuente de suscripción de direcciones"
description: "Extensión para las fuentes de suscripción de direcciones que permite a los propietarios de nombres de host actualizar y gestionar sus registros"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Descripción general

Esta especificación amplía el canal de suscripción de direcciones con comandos, lo que permite que los servidores de nombres difundan actualizaciones de entradas provenientes de los titulares de nombres de host. Propuesto originalmente en [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (septiembre de 2014), implementado en la versión 0.9.26 (junio de 2016) y desplegado en toda la red con estado CERRADO.

El sistema se ha mantenido estable e inalterado desde su implementación inicial, y continúa operando de manera idéntica en I2P 2.10.0 (Router API 0.9.65, septiembre de 2025).

## Motivación

Anteriormente, los servidores de suscripción de hosts.txt enviaban datos únicamente en un formato hosts.txt simple:

```
example.i2p=b64destination
```
Este formato básico generó varios problemas:

- Los titulares del nombre de host no pueden actualizar el Destino asociado a sus nombres de host (por ejemplo, para actualizar la clave de firma a un tipo criptográfico más sólido).
- Los titulares del nombre de host no pueden ceder sus nombres de host arbitrariamente. Deben entregar directamente al nuevo titular las claves privadas del Destino correspondiente.
- No hay forma de autenticar que un subdominio esté controlado por el nombre de host base correspondiente. Actualmente, esto solo lo aplican individualmente algunos servidores de nombres.

## Diseño

Esta especificación agrega líneas de comandos al formato hosts.txt. Con estos comandos, los servidores de nombres pueden ampliar sus servicios para ofrecer funciones adicionales. Los clientes que implementen esta especificación pueden escuchar estas funciones mediante el proceso de suscripción habitual.

Todas las líneas de comandos deben estar firmadas por la Destination (identidad/dirección en I2P) correspondiente. Esto garantiza que los cambios se realicen solo a petición del titular del nombre de host.

## Implicaciones de seguridad

Esta especificación no afecta el anonimato.

Aumenta el riesgo asociado a perder el control de una clave de Destino, ya que quien la obtenga puede usar estos comandos para realizar cambios en cualquier nombre de host asociado. Sin embargo, esto no es un problema mayor que el status quo, en el que quien obtenga un Destino puede suplantar un nombre de host y (parcialmente) tomar el control de su tráfico. El aumento del riesgo se compensa al dar a los titulares de nombres de host la capacidad de cambiar el Destino asociado a un nombre de host en caso de que consideren que el Destino ha sido comprometido. Esto es imposible con el sistema actual.

## Especificación

### Nuevos tipos de línea

Hay dos nuevos tipos de líneas:

1. **Comandos Add y Change:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Eliminar comandos:**

```
#!key1=val1#key2=val2...
```
#### Ordenación

Un feed no necesariamente está en orden ni es completo. Por ejemplo, un comando change puede aparecer en una línea antes de un comando add, o sin un comando add.

Las claves pueden estar en cualquier orden. No se permiten claves duplicadas. Todas las claves y los valores distinguen entre mayúsculas y minúsculas.

### Claves comunes

**Obligatorio en todos los comandos:**

**sig** : firma en Base64, utilizando la clave de firma del destino

**Referencias a un segundo nombre de host y/o destino:**

**oldname** : Un segundo nombre de host (nuevo o cambiado)

**olddest** : Un segundo destino Base64 (nuevo o cambiado)

**oldsig** : Una segunda firma en Base64, utilizando la clave de firma de olddest

**Otras claves comunes:**

**acción** : Un comando

**name** : El nombre de host, solo presente si no está precedido por `example.i2p=b64dest`

**dest** : El destino Base64, solo presente si no está precedido por `example.i2p=b64dest`

**date** : En segundos desde la época

**expires** : En segundos desde la época Unix

### Comandos

Todos los comandos excepto el comando "Add" deben contener un par clave/valor `action=command`.

Para mantener la compatibilidad con clientes antiguos, la mayoría de los comandos van precedidos por `example.i2p=b64dest`, como se indica a continuación. En el caso de cambios, se indican siempre los valores nuevos. Cualquier valor anterior se incluye en la sección de pares clave/valor.

Las claves enumeradas son obligatorias. Todos los comandos pueden contener elementos adicionales de clave/valor no definidos aquí.

#### Añadir nombre de host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host y destino.

**acción** : NO incluido, está implícito.

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!sig=b64sig
```
#### Cambiar el nombre de host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host y el destino anterior.

**acción** : changename

**oldname** : el nombre de host antiguo, que se reemplazará

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Cambiar destino

**Precedido por example.i2p=b64dest** : SÍ, este es el antiguo nombre de host y el nuevo destino.

**acción** : changedest

**olddest** : el destino anterior, que será reemplazado

**oldsig** : firma usando olddest

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Agregar alias de nombre de host

**Precedido por example.i2p=b64dest** : SÍ, este es el nuevo nombre de host (alias) y el destino anterior.

**acción** : addname

**oldname** : el nombre de host anterior

**sig** : firma

Ejemplo:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Agregar alias de destino

(Se usa para la actualización criptográfica)

**Precedido por example.i2p=b64dest** : SÍ, este es el nombre de host anterior y el nuevo destino (alternativo).

**action** : adddest

**olddest** : el destino anterior

**oldsig** : firma usando olddest

**sig** : firma usando dest

Ejemplo:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Agregar subdominio

**Precedido por subdomain.example.i2p=b64dest** : SÍ, este es el nuevo nombre de subdominio y destino.

**action** : addsubdomain

**oldname** : el nombre de host de nivel superior (example.i2p)

**olddest** : el destino de nivel superior (por ejemplo.i2p)

**oldsig** : firma usando olddest

**sig** : firma usando dest

Ejemplo:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Actualizar metadatos

**Precedido por example.i2p=b64dest** : SÍ, este es el antiguo nombre de host y destino.

**acción** : actualización

**sig** : firma

(añade aquí cualquier clave actualizada)

Ejemplo:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Eliminar nombre de host

**Precedido por example.i2p=b64dest** : NO, se especifican en las opciones

**acción** : eliminar

**name** : el nombre de host

**dest** : el destino

**sig** : firma

Ejemplo:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Eliminar todo con este destino

**Precedido por example.i2p=b64dest** : NO, estos se especifican en las opciones

**action** : removeall

**dest** : el destino

**sig** : firma

Ejemplo:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Firmas

Todos los comandos deben estar firmados por el Destination (identificador de destino en I2P) correspondiente. Los comandos con dos Destination pueden necesitar dos firmas.

`oldsig` es siempre la firma "interna". Firme y verifique sin que estén presentes las claves `oldsig` ni `sig`. `sig` es siempre la firma "externa". Firme y verifique con la clave `oldsig` presente pero no la clave `sig`.

#### Entrada para firmas

Para generar una secuencia de bytes para crear o verificar la firma, serialice de la siguiente manera:

1. Elimina la clave `sig`
2. Si se verifica con `oldsig`, elimina también la clave `oldsig`
3. Solo para los comandos Add o Change, emite `example.i2p=b64dest`
4. Si quedan claves, emite `#!`
5. Ordena las opciones por clave UTF-8, falla si hay claves duplicadas
6. Para cada par clave/valor, emite `key=value`, seguido (si no es el último par clave/valor) de un `#`

**Notas**

- No emitas un salto de línea
- La codificación de salida es UTF-8
- Toda la codificación de destino y de firma está en Base 64 usando el alfabeto de I2P
- Las claves y los valores distinguen mayúsculas y minúsculas
- Los nombres de host deben estar en minúsculas

#### Tipos de firma actuales

A partir de la versión 2.10.0 de I2P, se admiten los siguientes tipos de firma para destinos:

- **EdDSA_SHA512_Ed25519** (Tipo 7): La más común para destinos desde la 0.9.15. Usa una clave pública de 32 bytes y una firma de 64 bytes. Este es el tipo de firma recomendado para nuevos destinos.
- **RedDSA_SHA512_Ed25519** (Tipo 13): Disponible únicamente para destinos y leasesets (conjuntos leaseSet de I2P) cifrados (desde la 0.9.39).
- Tipos heredados (DSA_SHA1, variantes de ECDSA): Siguen siendo compatibles, pero están obsoletos para nuevas identidades de router a partir de la 0.9.58.

Nota: Las opciones criptográficas poscuánticas están disponibles a partir de I2P 2.10.0, pero aún no son los tipos de firma predeterminados.

## Compatibilidad

Todas las nuevas líneas en el formato hosts.txt se implementan usando caracteres de comentario al inicio (`#!`), de modo que todas las versiones anteriores de I2P interpretarán los nuevos comandos como comentarios y los ignorarán sin problemas.

Cuando los routers de I2P se actualicen a la nueva especificación, no volverán a reinterpretar los comentarios antiguos, pero comenzarán a reconocer nuevos comandos en consultas posteriores de sus fuentes de suscripción. Por lo tanto, es importante que los servidores de nombres conserven las entradas de comandos de alguna manera, o habiliten la compatibilidad con ETag para que los routers puedan obtener todos los comandos anteriores.

## Estado de la implementación

**Despliegue inicial:** Versión 0.9.26 (7 de junio de 2016)

**Estado actual:** Estable y sin cambios hasta I2P 2.10.0 (Router API 0.9.65, septiembre de 2025)

**Estado de la propuesta:** CERRADA (desplegada con éxito en toda la red)

**Ubicación de la implementación:** `apps/addressbook/java/src/net/i2p/addressbook/` en el router Java de I2P

**Clases clave:** - `SubscriptionList.java`: Gestiona el procesamiento de suscripciones - `Subscription.java`: Gestiona fuentes de suscripción individuales - `AddressBook.java`: Funcionalidad central de la libreta de direcciones - `Daemon.java`: Servicio en segundo plano de la libreta de direcciones

**URL de suscripción predeterminada:** `http://i2p-projekt.i2p/hosts.txt`

## Detalles del transporte

Las suscripciones utilizan HTTP con soporte para GET condicional:

- **Encabezado ETag:** Admite una detección eficiente de cambios
- **Encabezado Last-Modified:** Realiza el seguimiento de los tiempos de actualización de la suscripción
- **304 Not Modified:** Los servidores deberían devolver esto cuando el contenido no ha cambiado
- **Content-Length:** Altamente recomendado para todas las respuestas

El I2P router utiliza el comportamiento estándar de un cliente HTTP con soporte de caché adecuado.

## Contexto de la versión

**Nota sobre el versionado de I2P:** Aproximadamente a partir de la versión 1.5.0 (agosto de 2021), I2P cambió del versionado 0.9.x al versionado semántico (1.x, 2.x, etc.). Sin embargo, la versión interna de la Router API sigue utilizando la numeración 0.9.x por compatibilidad retroactiva. En octubre de 2025, la versión actual es I2P 2.10.0 con la versión de la Router API 0.9.65.

Este documento de especificación se redactó originalmente para la versión 0.9.49 (febrero de 2021) y sigue siendo completamente exacto para la versión actual 0.9.65 (I2P 2.10.0), porque el sistema de fuentes de suscripción no ha tenido cambios desde su implementación original en la 0.9.26.

## Referencias

- [Propuesta 112 (Original)](/proposals/112-addressbook-subscription-feed-commands/)
- [Especificación oficial](/docs/specs/subscription/)
- [Documentación sobre nombres de I2P](/docs/overview/naming/)
- [Especificación de estructuras comunes](/docs/specs/common-structures/)
- [Repositorio del código fuente de I2P](https://github.com/i2p/i2p.i2p)
- [Repositorio Gitea de I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Desarrollos relacionados

Si bien el propio sistema de fuentes de suscripción no ha cambiado, los siguientes desarrollos relacionados en la infraestructura de nombres de I2P pueden resultar de interés:

- **Nombres Base32 extendidos** (0.9.40+): Compatibilidad con direcciones base32 de más de 56 caracteres para leaseSets cifrados. No afecta al formato del feed de suscripción.
- **Registro de TLD .i2p.alt** (RFC 9476, finales de 2023): Registro oficial en GANA de .i2p.alt como TLD alternativo. Las futuras actualizaciones del router pueden eliminar el sufijo .alt, pero no se requieren cambios en los comandos de suscripción.
- **Criptografía poscuántica** (2.10.0+): Disponible, pero no predeterminada. Se considerará en el futuro el uso de algoritmos de firma en los feeds de suscripción.
