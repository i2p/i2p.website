---
title: "Denominación y Libreta de Direcciones"
description: "Cómo I2P mapea nombres de host legibles por humanos a destinos"
slug: "naming"
aliases:
  - "/es/docs/specs/naming"
  - "/es/docs/specs/naming/"
  - "/es/docs/naming"
  - "/es/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Descripción general

I2P incluye una biblioteca de nombres genérica y una implementación base diseñada para funcionar con un mapeo local de nombres a destinos, así como una aplicación complementaria llamada [libreta de direcciones](#address-book). I2P también soporta [nombres de host Base32](#base32-names) similares a las direcciones .onion de Tor.

El libro de direcciones es un sistema de nomenclatura legible por humanos, seguro, distribuido y basado en una red de confianza, que sacrifica únicamente la exigencia de que todos los nombres legibles por humanos sean globalmente únicos al exigir solo unicidad local. Mientras que todos los mensajes en I2P están criptográficamente dirigidos por su destino, diferentes personas pueden tener entradas en el libro de direcciones local para "Alice" que se refieren a diferentes destinos. Las personas aún pueden descubrir nuevos nombres importando libros de direcciones publicados de pares especificados en su red de confianza, agregando las entradas proporcionadas a través de un tercero, o (si algunas personas organizan una serie de libros de direcciones publicados usando un sistema de registro de primero en llegar, primero en ser servido) las personas pueden elegir tratar estos libros de direcciones como servidores de nombres, emulando el DNS tradicional.

NOTA: Para conocer el razonamiento detrás del sistema de nomenclatura de I2P, argumentos comunes en contra y posibles alternativas, consulta la página de [discusión sobre nomenclatura](/docs/legacy/naming/).

---

## Componentes del Sistema de Nombres

No hay una autoridad de nomenclatura central en I2P. Todos los nombres de host son locales.

El sistema de nomenclatura es bastante simple y la mayor parte está implementado en aplicaciones externas al router, pero incluidas con la distribución de I2P. Los componentes son:

1. El [servicio de nombres](#naming-services) local que realiza búsquedas y también maneja [nombres de host Base32](#base32-names).
2. El [proxy HTTP](#http-proxy) que solicita búsquedas al router y dirige al usuario a servicios de salto remotos para ayudar con búsquedas fallidas.
3. Los [formularios host-add](#host-add-services) HTTP que permiten a los usuarios agregar hosts a su hosts.txt local.
4. Los [servicios de salto](#jump-services) HTTP que proporcionan sus propias búsquedas y redirección.
5. La aplicación [libreta de direcciones](#address-book) que fusiona listas de hosts externos, obtenidas vía HTTP, con la lista local.
6. La aplicación [SusiDNS](#susidns) que es una interfaz web simple para la configuración de la libreta de direcciones y visualización de las listas de hosts locales.

---

## Servicios de Nombres

Todos los destinos en I2P son claves de 516 bytes (o más largas). (Para ser más precisos, es una clave pública de 256 bytes más una clave de firma de 128 bytes más un certificado de 3 o más bytes, que en representación Base64 son 516 o más bytes. Ahora se utilizan [Certificados](/docs/legacy/naming/#certificates) no nulos para indicación del tipo de firma. Por lo tanto, los certificados en destinos generados recientemente son de más de 3 bytes.

Si una aplicación (i2ptunnel o el proxy HTTP) desea acceder a un destino por nombre, el router realiza una búsqueda local muy simple para resolver ese nombre.

### Servicio de Nomenclatura Hosts.txt

El Servicio de Nombres hosts.txt realiza una búsqueda lineal simple a través de archivos de texto. Este servicio de nombres fue el predeterminado hasta la versión 0.8.8 cuando fue reemplazado por el Servicio de Nombres Blockfile. El formato hosts.txt se había vuelto demasiado lento después de que el archivo creciera a miles de entradas.

Realiza una búsqueda lineal a través de tres archivos locales, en orden, para buscar nombres de host y convertirlos a una clave de destino de 516 bytes. Cada archivo está en un [formato de archivo de configuración](/docs/specs/configuration/) simple, con hostname=base64, uno por línea. Los archivos son:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Servicio de Nombres Blockfile

El Servicio de Nombres Blockfile almacena múltiples "libretas de direcciones" en un único archivo de base de datos llamado hostsdb.blockfile. Este Servicio de Nombres es el predeterminado desde la versión 0.8.8.

Un blockfile es simplemente almacenamiento en disco de múltiples mapas ordenados (pares clave-valor), implementado como skiplists. El formato blockfile está especificado en la [página Blockfile](/docs/specs/blockfile/). Proporciona búsqueda rápida de Destination en un formato compacto. Aunque la sobrecarga del blockfile es sustancial, los destinations se almacenan en binario en lugar de en Base 64 como en el formato hosts.txt. Además, el blockfile proporciona la capacidad de almacenamiento de metadatos arbitrarios (como fecha de adición, fuente y comentarios) para cada entrada para implementar características avanzadas de libreta de direcciones. El requisito de almacenamiento del blockfile es un aumento modesto sobre el formato hosts.txt, y el blockfile proporciona aproximadamente una reducción de 10x en los tiempos de búsqueda.

Al crearse, el servicio de nombres importa entradas de los tres archivos utilizados por el Servicio de Nombres hosts.txt. El blockfile imita la implementación anterior manteniendo tres mapas que se buscan en orden, llamados privatehosts.txt, userhosts.txt y hosts.txt. También mantiene un mapa de búsqueda inversa para implementar búsquedas inversas rápidas.

### Otras Facilidades del Servicio de Nombres

La búsqueda no distingue entre mayúsculas y minúsculas. Se utiliza la primera coincidencia y no se detectan conflictos. No hay aplicación de reglas de nomenclatura en las búsquedas. Las búsquedas se almacenan en caché durante unos minutos. La resolución Base 32 se [describe a continuación](#base32-names). Para una descripción completa de la API del Servicio de Nombres, consulte los [Javadocs del Servicio de Nombres](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). Esta API se amplió significativamente en la versión 0.8.7 para proporcionar adiciones y eliminaciones, almacenamiento de propiedades arbitrarias con el nombre del host y otras características.

### Servicios de Nombres Alternativos y Experimentales

El servicio de nombres se especifica con la propiedad de configuración `i2p.naming.impl=class`. Son posibles otras implementaciones. Por ejemplo, existe una funcionalidad experimental para búsquedas en tiempo real (como DNS) a través de la red dentro del router. Para más información consulta las [alternativas en la página de discusión](/docs/legacy/naming/#alternatives).

El proxy HTTP realiza una búsqueda a través del router para todos los nombres de host que terminan en '.i2p'. De lo contrario, reenvía la solicitud a un outproxy HTTP configurado. Por lo tanto, en la práctica, todos los nombres de host HTTP (Sitio I2P) deben terminar en el pseudo-Dominio de Nivel Superior '.i2p'.

Si el router no logra resolver el nombre de host, el proxy HTTP devuelve una página de error al usuario con enlaces a varios servicios de "salto". Ver más abajo para detalles.

---

## Dominio .i2p.alt

Previamente [solicitamos reservar el TLD .i2p](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) siguiendo los procedimientos especificados en [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). Sin embargo, esta solicitud y todas las demás fueron rechazadas, y RFC 6761 fue declarado un "error".

Después de muchos años de trabajo del equipo de GNUnet y otros, el dominio .alt fue reservado como un TLD de uso especial en [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) a finales de 2023. Aunque no hay registradores oficiales sancionados por IANA, hemos registrado el dominio .i2p.alt con el principal registrador no oficial [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). Esto no impide que otros usen el dominio, pero debería ayudar a desalentarlo.

Un beneficio del dominio .alt es que, en teoría, los resolutores DNS no reenviarán las solicitudes .alt una vez que se actualicen para cumplir con RFC 9476, y eso evitará las filtraciones de DNS. Para compatibilidad con los nombres de host .i2p.alt, el software y servicios de I2P deben actualizarse para manejar estos nombres de host eliminando el TLD .alt. Estas actualizaciones están programadas para la primera mitad de 2024.

En este momento, no hay planes para hacer que .i2p.alt sea la forma preferida para mostrar e intercambiar nombres de host de I2P. Este es un tema para futuras investigaciones y discusiones.

---

## Libreta de Direcciones

### Suscripciones Entrantes y Fusión

La aplicación de libreta de direcciones recupera periódicamente los archivos hosts.txt de otros usuarios y los fusiona con el hosts.txt local, después de varias verificaciones. Los conflictos de nombres se resuelven por orden de llegada.

Suscribirse al archivo hosts.txt de otro usuario implica otorgarle cierta cantidad de confianza. No quieres que, por ejemplo, 'secuestren' un nuevo sitio ingresando rápidamente su propia clave para un sitio nuevo antes de pasarte la nueva entrada host/clave.

Por esta razón, la única suscripción configurada por defecto es `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, que contiene una copia del hosts.txt incluido en la versión de I2P. Los usuarios deben configurar suscripciones adicionales en su aplicación local de libreta de direcciones (a través de subscriptions.txt o [SusiDNS](#susidns)).

Algunos otros enlaces de suscripción a libretas de direcciones públicas:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Los operadores de estos servicios pueden tener varias políticas para listar hosts. La presencia en esta lista no implica respaldo.

### Reglas de Nomenclatura

Aunque esperamos que no haya limitaciones técnicas dentro de I2P para los nombres de host, la libreta de direcciones impone varias restricciones en los nombres de host importados desde suscripciones. Esto lo hace por cordura tipográfica básica y compatibilidad con navegadores, y por seguridad. Las reglas son esencialmente las mismas que las del RFC2396 Sección 3.2.2. Cualquier nombre de host que viole estas reglas podría no propagarse a otros routers.

Reglas de Nomenclatura:

- Los nombres se convierten a minúsculas al importar.
- Se verifica que los nombres no entren en conflicto con nombres existentes en userhosts.txt y hosts.txt (pero no privatehosts.txt) después de la conversión a minúsculas.
- Deben contener solo [a-z] [0-9] '.' y '-' después de la conversión a minúsculas.
- No deben comenzar con '.' o '-'.
- Deben terminar con '.i2p'.
- Máximo 67 caracteres, incluyendo el '.i2p'.
- No deben contener '..'.
- No deben contener '.-' o '-.' (desde la versión 0.6.1.33).
- No deben contener '--' excepto en 'xn--' para IDN.
- Los hostnames Base32 (*.b32.i2p) están reservados para uso base 32 y por tanto no se permite importarlos.
- Ciertos hostnames reservados para uso del proyecto no están permitidos (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, y otros)
- Se desaconsejan los hostnames que comienzan con 'www.' y son rechazados por algunos servicios de registro. Algunas implementaciones de addressbook eliminan automáticamente los prefijos 'www.' de las búsquedas. Por tanto, registrar 'www.example.i2p' es innecesario, y registrar un destino diferente para 'www.example.i2p' y 'example.i2p' hará que 'www.example.i2p' sea inalcanzable para algunos usuarios.
- Se verifica la validez base64 de las claves.
- Se verifica que las claves no entren en conflicto con claves existentes en hosts.txt (pero no privatehosts.txt).
- Longitud mínima de clave 516 bytes.
- Longitud máxima de clave 616 bytes (para dar cuenta de certificados de hasta 100 bytes).

Cualquier nombre recibido a través de suscripción que pase todas las verificaciones se añade mediante el servicio de nombres local.

Tenga en cuenta que los símbolos '.' en un nombre de host no tienen significado alguno, y no denotan ninguna jerarquía real de nomenclatura o confianza. Si el nombre 'host.i2p' ya existe, no hay nada que impida que cualquiera agregue un nombre 'a.host.i2p' a su hosts.txt, y este nombre puede ser importado por el address book de otros. Los métodos para denegar subdominios a no 'propietarios' de dominio (¿certificados?), y la deseabilidad y viabilidad de estos métodos, son temas para discusión futura.

Los Nombres de Dominio Internacionalizados (IDN) también funcionan en i2p (usando la forma punycode 'xn--'). Para ver los nombres de dominio IDN .i2p renderizados correctamente en la barra de direcciones de Firefox, añade 'network.IDN.whitelist.i2p (boolean) = true' en about:config.

Como la aplicación de libreta de direcciones no utiliza privatehosts.txt en absoluto, en la práctica este archivo es el único lugar donde es apropiado colocar alias privados o "nombres de mascota" para sitios que ya están en hosts.txt.

### Formato Avanzado de Feed de Suscripción

A partir de la versión 0.9.26, los sitios de suscripción y clientes pueden soportar un protocolo avanzado de feeds hosts.txt que incluye metadatos incluyendo firmas. Este formato es compatible con versiones anteriores del formato estándar hosts.txt hostname=base64destination. Consulta [la especificación](/docs/specs/subscription/) para más detalles.

### Suscripciones Salientes

Address Book publicará el archivo hosts.txt fusionado en una ubicación (tradicionalmente hosts.txt en el directorio principal del sitio I2P local) para que otros puedan acceder a él para sus suscripciones. Este paso es opcional y está deshabilitado por defecto.

### Problemas de Hospedaje y Transporte HTTP

La aplicación de libreta de direcciones, junto con eepget, guarda la información de Etag y/o Last-Modified devuelta por el servidor web de la suscripción. Esto reduce considerablemente el ancho de banda requerido, ya que el servidor web devolverá un '304 Not Modified' en la siguiente descarga si no ha cambiado nada.

Sin embargo, todo el archivo hosts.txt se descarga si ha cambiado. Consulte la discusión sobre este tema más abajo.

Se recomienda encarecidamente que los hosts que sirven un archivo hosts.txt estático o una aplicación CGI equivalente entreguen un encabezado Content-Length, y un encabezado Etag o Last-Modified. También asegúrese de que el servidor entregue un '304 Not Modified' cuando sea apropiado. Esto reducirá drásticamente el ancho de banda de la red y reducirá las posibilidades de corrupción.

---

## Servicios de Agregar Host

Un servicio de adición de hosts es una aplicación CGI simple que toma un nombre de host y una clave Base64 como parámetros y los añade a su archivo hosts.txt local. Si otros routers se suscriben a ese hosts.txt, el nuevo nombre de host/clave se propagará a través de la red.

Se recomienda que los servicios de adición de hosts impongan, como mínimo, las restricciones impuestas por la aplicación de libreta de direcciones listada arriba. Los servicios de adición de hosts pueden imponer restricciones adicionales en nombres de host y claves, por ejemplo:

- Un límite en el número de 'subdominios'.
- Autorización para 'subdominios' a través de varios métodos.
- Hashcash o certificados firmados.
- Revisión editorial de nombres de host y/o contenido.
- Categorización de hosts por contenido.
- Reserva o rechazo de ciertos nombres de host.
- Restricciones en el número de nombres registrados en un período de tiempo determinado.
- Retrasos entre el registro y la publicación.
- Requisito de que el host esté activo para verificación.
- Expiración y/o revocación.
- Rechazo de suplantación IDN.

---

## Servicios de Salto

Un servicio de salto es una aplicación CGI simple que toma un nombre de host como parámetro y devuelve una redirección 301 a la URL apropiada con una cadena `?i2paddresshelper=key` anexada. El proxy HTTP interpretará la cadena anexada y usará esa clave como el destino real. Además, el proxy almacenará en caché esa clave para que el ayudante de direcciones no sea necesario hasta el reinicio.

Ten en cuenta que, al igual que con las suscripciones, usar un servicio de salto implica cierta cantidad de confianza, ya que un servicio de salto podría redirigir maliciosamente a un usuario a un destino incorrecto.

Para proporcionar el mejor servicio, un servicio de salto debería estar suscrito a varios proveedores de hosts.txt para que su lista local de hosts esté actualizada.

---

## SusiDNS

SusiDNS es simplemente una interfaz web frontend para configurar suscripciones de libreta de direcciones y acceder a los cuatro archivos de libreta de direcciones. Todo el trabajo real lo realiza la aplicación 'address book'.

Actualmente, hay poco cumplimiento de las reglas de nomenclatura del libro de direcciones dentro de SusiDNS, por lo que un usuario puede introducir nombres de host localmente que serían rechazados por las reglas de suscripción del libro de direcciones.

---

## Nombres Base32

I2P soporta nombres de host Base32 similares a las direcciones .onion de Tor. Las direcciones Base32 son mucho más cortas y fáciles de manejar que los Destinations Base64 completos de 516 caracteres o los addresshelpers. Ejemplo: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

En Tor, la dirección tiene 16 caracteres (80 bits), o la mitad del hash SHA-1. I2P utiliza 52 caracteres (256 bits) para representar el hash SHA-256 completo. La forma es {52 chars}.b32.i2p. Tor tiene una [propuesta](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) para convertir a un formato idéntico de {52 chars}.onion para sus servicios ocultos. Base32 está implementado en el servicio de nombres, que consulta al router sobre I2CP para buscar el leaseSet y obtener el Destination completo. Las búsquedas Base32 solo serán exitosas cuando el Destination esté activo y publicando un leaseSet. Debido a que la resolución puede requerir una búsqueda en la base de datos de red, puede tomar significativamente más tiempo que una búsqueda en la libreta de direcciones local.

Las direcciones Base32 pueden usarse en la mayoría de lugares donde se utilizan nombres de host o destinos completos, sin embargo hay algunas excepciones donde pueden fallar si el nombre no se resuelve inmediatamente. I2PTunnel fallará, por ejemplo, si el nombre no se resuelve a un destino.

---

## Nombres Base32 Extendidos

Los nombres base 32 extendidos fueron introducidos en la versión 0.9.40 para soportar leasesets cifrados. Las direcciones para leasesets cifrados se identifican por 56 o más caracteres codificados, sin incluir el ".b32.i2p" (35 o más bytes decodificados), comparado con 52 caracteres (32 bytes) para las direcciones base 32 tradicionales. Ver propuestas 123 y 149 para información adicional.

Las direcciones Base 32 estándar ("b32") contienen el hash del destino. Esto no funcionará para ls2 cifrado (propuesta 123).

No puedes usar una dirección base 32 tradicional para un LS2 cifrado (propuesta 123), ya que solo contiene el hash del destino. No proporciona la clave pública no ciega. Los clientes deben conocer la clave pública del destino, el tipo de firma, el tipo de firma ciega, y una clave secreta o privada opcional para obtener y descifrar el leaseset. Por lo tanto, una dirección base 32 sola es insuficiente. El cliente necesita ya sea el destino completo (que contiene la clave pública), o la clave pública por sí misma. Si el cliente tiene el destino completo en una libreta de direcciones, y la libreta de direcciones soporta búsqueda inversa por hash, entonces la clave pública puede ser recuperada.

Por lo tanto, necesitamos un nuevo formato que ponga la clave pública en lugar del hash en una dirección base32. Este formato también debe contener el tipo de firma de la clave pública y el tipo de firma del esquema de ocultación.

Esta sección documenta un nuevo formato b32 para estas direcciones. Aunque nos hemos referido a este nuevo formato durante las discusiones como una dirección "b33", el nuevo formato real conserva el sufijo habitual ".b32.i2p".

### Creación y codificación

Construye un nombre de host de {56+ caracteres}.b32.i2p (35+ caracteres en binario) de la siguiente manera. Primero, construye los datos binarios que se van a codificar en base 32:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Post-procesamiento y suma de verificación:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Cualquier bit no utilizado al final del b32 debe ser 0. No hay bits no utilizados para una dirección estándar de 56 caracteres (35 bytes).

### Decodificación y Verificación

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits de Clave Secreta y Privada

Los bits de clave secreta y privada se utilizan para indicar a los clientes, proxies u otro código del lado del cliente que se requerirá la clave secreta y/o privada para descifrar el leaseset. Las implementaciones particulares pueden solicitar al usuario que proporcione los datos requeridos, o rechazar los intentos de conexión si faltan los datos requeridos.

### Notas

- El XOR de los primeros 3 bytes con el hash proporciona una capacidad de suma de verificación limitada, y asegura que todos los caracteres base32 al principio estén aleatorizados. Solo unas pocas combinaciones de flag y sigtype son válidas, por lo que cualquier error tipográfico probablemente creará una combinación inválida y será rechazada.
- En el caso habitual (sigtypes de 1 byte, sin secreto, sin autenticación por cliente), el hostname será {56 chars}.b32.i2p, decodificando a 35 bytes, igual que Tor.
- La suma de verificación de 2 bytes de Tor tiene una tasa de falsos negativos de 1/64K. Con 3 bytes, menos algunos bytes ignorados, la nuestra se acerca a 1 en un millón, ya que la mayoría de las combinaciones flag/sigtype son inválidas.
- Adler-32 es una mala elección para entradas pequeñas, y para detectar cambios pequeños. Usamos CRC-32 en su lugar. CRC-32 es rápido y está ampliamente disponible.
- Aunque está fuera del alcance de esta especificación, los routers y/o clientes deben recordar y cachear (probablemente de forma persistente) el mapeo de clave pública a destination, y viceversa.
- Distinguir los sabores antiguos de los nuevos por longitud. Las direcciones b32 antiguas son siempre {52 chars}.b32.i2p. Las nuevas son {56+ chars}.b32.i2p
- El hilo de discusión de Tor [está aquí](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- No esperes que los sigtypes de 2 bytes sucedan nunca, solo llegamos a 13. No hay necesidad de implementar ahora.
- El nuevo formato puede usarse en enlaces jump (y ser servido por servidores jump) si se desea, igual que b32.
- Cualquier secreto, clave privada, o clave pública de más de 32 bytes excedería la longitud máxima de etiqueta DNS de 63 caracteres. Probablemente a los navegadores no les importa.
- Sin problemas de compatibilidad hacia atrás. Las direcciones b32 más largas fallarán al convertirse a hashes de 32 bytes en software antiguo.
