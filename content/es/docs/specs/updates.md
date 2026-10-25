---
title: "Especificación de Actualización de Software"
description: "Especificación para el mecanismo de actualización de software I2P, formato de archivo SU3 y fuente de noticias"
slug: "updates"
aliases:
  - "/es/updates"
  - "/es/updates/"
category: "Diseño"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Descripción general

I2P utiliza un sistema simple, pero seguro, para la actualización automática de software. La consola del router extrae periódicamente un archivo de noticias desde una URL de I2P configurable. Hay una URL de respaldo codificada que apunta al sitio web del proyecto, en caso de que el host de noticias predeterminado del proyecto falle.

El contenido del archivo de noticias se muestra en la página de inicio de la consola del router. Además, el archivo de noticias contiene el número de versión más reciente del software. Si la versión es superior al número de versión del router, mostrará una indicación al usuario de que hay una actualización disponible.

El router puede opcionalmente descargar, o descargar e instalar, la nueva versión si está configurado para hacerlo.

## Especificación de Archivo de Noticias Antiguas

Este formato fue reemplazado por el formato de noticias su3 a partir de la versión 0.9.17.

El archivo news.xml puede contener los siguientes elementos:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Los parámetros en la entrada i2p.release son los siguientes. Todas las claves no distinguen entre mayúsculas y minúsculas. Todos los valores deben estar encerrados entre comillas dobles.

**date** : La fecha de lanzamiento de la versión del router. No se usa. Formato no especificado.

**minJavaVersion** : La versión mínima de Java requerida para ejecutar la versión actual. A partir de la versión 0.9.9.

**minVersion** : La versión mínima del router requerida para actualizar a la versión actual. Si un router es más antiguo que esta, el usuario debe (¿manualmente?) actualizar primero a una versión intermedia. A partir del lanzamiento 0.9.9.

**su3Clearnet** : Una o más URLs HTTP donde el archivo de actualización .su3 puede encontrarse en la clearnet (no-I2P). Las URLs múltiples deben estar separadas por un espacio o coma. A partir de la versión 0.9.9.

**su3SSL** : Una o más URLs HTTPS donde el archivo de actualización .su3 puede encontrarse en la clearnet (no-I2P). Múltiples URLs deben estar separadas por un espacio o coma. A partir de la versión 0.9.9.

**sudTorrent** : El enlace magnet para el torrent .sud (no-pack200) de la actualización. A partir de la versión 0.9.4.

**su2Torrent** : El enlace magnet para el torrent .su2 (pack200) de la actualización. Desde la versión 0.9.4.

**su3Torrent** : El enlace magnet para el torrent .su3 (nuevo formato) de la actualización. A partir de la versión 0.9.9.

**version** : Requerido. La última versión actual del router disponible.

Los elementos pueden incluirse dentro de comentarios XML para evitar la interpretación por parte de los navegadores. El elemento i2p.release y la versión son obligatorios. Todos los demás son opcionales. NOTA: Debido a limitaciones del analizador, un elemento completo debe estar en una sola línea.

## Especificación de Archivo de Actualización

A partir de la versión 0.9.9, el archivo de actualización firmado, llamado i2pupdate.su3, utilizará el formato de archivo "su3" especificado a continuación. Los firmantes de versiones aprobados utilizarán claves RSA de 4096 bits. Los certificados de clave pública X.509 para estos firmantes se distribuyen en los paquetes de instalación del router. Las actualizaciones pueden contener certificados para nuevos firmantes aprobados, y/o contener una lista de certificados a eliminar para revocación.

## Especificación de Archivo de Actualización Antigua

Este formato está obsoleto desde la versión 0.9.9.

El archivo de actualización firmado, tradicionalmente llamado i2pupdate.sud, es simplemente un archivo zip con un encabezado de 56 bytes antepuesto. El encabezado contiene:

- Una [Signature](/docs/specs/common-structures#signature) DSA de 40 bytes
- Una versión I2P de 16 bytes en UTF-8, rellenada con ceros finales si es necesario

La firma cubre únicamente el archivo zip - no la versión antepuesta. La firma debe coincidir con una de las DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) configuradas en el router, que tiene una lista codificada por defecto de las claves de los administradores de lanzamiento actuales del proyecto.

Para propósitos de comparación de versiones, los campos de versión contienen [0-9]*, los separadores de campo son '-', '_', y '.', y todos los demás caracteres son ignorados.

A partir de la versión 0.8.8, la versión también debe especificarse como un comentario del archivo zip en UTF-8, sin los ceros finales. El router que se actualiza verifica que la versión en el encabezado (no cubierta por la firma) coincida con la versión en el comentario del archivo zip, que sí está cubierta por la firma. Esto previene la falsificación del número de versión en el encabezado.

## Descarga e Instalación

El router primero descarga el encabezado del archivo de actualización desde una de una lista configurable de URLs de I2P, usando el cliente HTTP incorporado y proxy, y verifica que la versión sea más reciente. Esto previene el problema de hosts de actualización que no tienen el archivo más reciente. El router luego descarga el archivo de actualización completo. El router verifica que la versión del archivo de actualización sea más reciente antes de la instalación. También, por supuesto, verifica la firma, y verifica que el comentario del archivo zip coincida con la versión del encabezado, como se explicó anteriormente.

El archivo zip se extrae y se copia como "i2pupdate.zip" en el directorio de configuración de I2P (~/.i2p en Linux).

A partir de la versión 0.7.12, el router soporta descompresión Pack200. Los archivos dentro del archivo zip con sufijo .jar.pack o .war.pack son descomprimidos de forma transparente a un archivo .jar o .war. Los archivos de actualización que contienen archivos .pack tradicionalmente se nombran con el sufijo '.su2'. Pack200 reduce el tamaño de los archivos de actualización en aproximadamente 60%.

A partir de la versión 0.8.7, el router eliminará los archivos libjbigi.so y libjcpuid.so si el archivo zip contiene un archivo lib/jbigi.jar, de modo que los nuevos archivos se extraerán de jbigi.jar.

A partir de la versión 0.8.12, si el archivo zip contiene un archivo deletelist.txt, el router eliminará los archivos listados ahí. El formato es:

- Un nombre de archivo por línea
- Todos los nombres de archivo son relativos al directorio de instalación; no se permiten nombres de archivo absolutos, ni archivos que comiencen con ".."
- Los comentarios comienzan con '#'

El router luego eliminará el archivo deletelist.txt.

## Especificación de Archivo SU3

Esta especificación se utiliza para actualizaciones del router desde la versión 0.9.9, datos de reseed desde la versión 0.9.14, plugins desde la versión 0.9.15, y el archivo de noticias desde la versión 0.9.17.

### Problemas con el formato anterior .sud/.su2

- Sin número mágico o flags
- No hay forma de especificar compresión, pack200 o no, o algoritmo de firma
- La versión no está cubierta por la firma, por lo que se hace cumplir requiriendo que esté en el comentario del archivo zip (para archivos de router) o en el archivo plugin.config (para plugins)
- Firmante no especificado, por lo que el verificador debe probar todas las claves conocidas
- El formato de firma-antes-de-datos requiere dos pasadas para generar el archivo

### Objetivos

- Corregir los problemas anteriores
- Migrar a un algoritmo de firma más seguro
- Mantener la información de versión en el mismo formato y desplazamiento para compatibilidad con verificadores de versión existentes
- Verificación de firma y extracción de archivos en una sola pasada

### Especificación

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Todos los campos no utilizados deben establecerse en 0 para compatibilidad con versiones futuras.

### Detalles de la Firma

La firma cubre toda la cabecera comenzando en el byte 0, hasta el final del contenido. Utilizamos firmas en bruto. Toma el hash de los datos (usando el tipo de hash implícito en el tipo de firma en los bytes 8-9) y pásalo a una función de firma o verificación "en bruto" (por ejemplo, "NONEwithRSA" en Java).

Aunque la verificación de firma y la extracción de contenido pueden implementarse en una sola pasada, una implementación debe leer y almacenar en buffer los primeros 10 bytes para determinar el tipo de hash antes de comenzar a verificar.

Las longitudes de las firmas para los varios tipos de firma se indican en la especificación de [Signature](/docs/specs/common-structures#signature). Rellena la firma con ceros iniciales si es necesario. Consulta la [página de detalles de criptografía](/docs/specs/cryptography#sig) para los parámetros de los varios tipos de firma.

### Notas

El tipo de contenido especifica el dominio de confianza. Para cada tipo de contenido, los clientes mantienen un conjunto de certificados de clave pública X.509 para las partes de confianza autorizadas a firmar ese contenido. Solo pueden utilizarse certificados para el tipo de contenido especificado. El certificado se busca por el ID del firmante. Los clientes deben verificar que el tipo de contenido sea el esperado para la aplicación.

Todos los valores están en orden de bytes de red (big endian).

Para una implementación en Python de firmas RSA sin formato compatible con Java "NONEwithRSA", consulta [este artículo de Stack Overflow](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## Especificación del Archivo de Actualización SU3 del Router

### Detalles de SU3

- Tipo de Contenido SU3: 1 (ACTUALIZACIÓN DE ROUTER)
- Tipo de Archivo SU3: 0 (ZIP)
- Versión SU3: La versión del router

Los archivos jar y war en el zip ya no se comprimen con pack200 como se documenta arriba para los archivos "su2", porque los runtimes de Java recientes ya no lo soportan.

### Notas

- Para las versiones de lanzamiento, la versión SU3 es la versión "base" del router, por ejemplo "0.9.20".
- Para las compilaciones de desarrollo, que están soportadas desde la versión 0.9.20, la versión SU3 es la versión "completa" del router, por ejemplo "0.9.20-5" o "0.9.20-5-rc". Ver RouterVersion.java en el [código fuente de I2P](https://github.com/i2p/i2p.i2p).

## Especificación de Archivo de Reseed SU3

A partir de la versión 0.9.14, los datos de reseed se entregan en un formato de archivo "su3".

### Objetivos

- Archivos firmados con firmas fuertes y certificados confiables para prevenir ataques de intermediario que podrían iniciar a las víctimas en una red separada y no confiable.
- Usar el formato de archivo su3 ya utilizado para actualizaciones y plugins
- Un solo archivo comprimido para acelerar el reseeding, que era lento al obtener 200 archivos

### Especificación

1. El archivo debe llamarse "i2pseeds.su3". A partir de la versión 0.9.42, el solicitante debe agregar una cadena de consulta "?netid=2" a la URL de la solicitud, asumiendo el ID de red actual de 2. Esto puede usarse para prevenir conexiones entre redes. Las redes de prueba deben establecer un ID de red diferente. Ver la propuesta 147 para más detalles.
2. El archivo debe estar en el mismo directorio que los router infos en el servidor web.
3. Un router primero intentará obtener (URL índice)/i2pseeds.su3; si eso falla, obtendrá la URL índice y luego obtendrá los archivos individuales de router info encontrados en los enlaces.

### Detalles de SU3

- Tipo de Contenido SU3: 3 (RESEED)
- Tipo de Archivo SU3: 0 (ZIP)
- Versión SU3: Segundos desde la época, en ASCII (date +%s). NO se reinicia en 2038 o 2106.
- Los archivos de información del router en el archivo zip deben estar en el "nivel superior". No hay directorios en el archivo zip.
- Los archivos de información del router deben nombrarse "routerInfo-(hash del router en base 64 de 44 caracteres).dat", como en el mecanismo de reseed anterior. Se debe usar el alfabeto base 64 de I2P.

### Notas

- Advertencia: Se sabe que varios reseeds no responden a través de IPv6. Se recomienda forzar o preferir IPv4.
- Advertencia: Algunos reseeds usan certificados CA autofirmados. Las implementaciones deben importar y confiar en estas CAs al hacer reseed, u omitir los reseeds autofirmados de la lista de reseed.
- Las claves de firmante de reseed se distribuyen a las implementaciones como certificados X.509 autofirmados con claves RSA-4096 (tipo de firma 6). Las implementaciones deberían hacer cumplir las fechas válidas en los certificados.

## Especificación de Archivo de Plugin SU3

A partir de la versión 0.9.15, los plugins pueden empaquetarse en formato de archivo "su3".

### Detalles de SU3

- Tipo de Contenido SU3: 2 (PLUGIN)
- Tipo de Archivo SU3: 0 (ZIP) - Consulta la [especificación de plugin](/docs/specs/plugin) para más detalles.
- Versión SU3: La versión del plugin, debe coincidir con la del plugin.config.

Los archivos jar y war en el zip no deben comprimirse con pack200 como se documenta arriba para los archivos "su2", ya que las versiones recientes de Java runtime ya no lo soportan.

## Especificación de Archivo de Noticias SU3

A partir de la versión 0.9.17, las noticias se entregan en formato de archivo "su3".

### Objetivos

- Noticias firmadas con firmas fuertes y certificados confiables
- Usar formato de archivo su3 ya utilizado para actualizaciones, reseeding y plugins
- Formato XML estándar para usar con analizadores estándar
- Formato Atom estándar para usar con lectores y generadores de feeds estándar
- Sanitización y verificación de HTML antes de mostrar en la consola
- Adecuado para implementación fácil en Android y otras plataformas sin consola HTML

### Detalles de SU3

- Tipo de Contenido SU3: 4 (NEWS)
- Tipo de Archivo SU3: 1 (XML) o 3 (XML.GZ)
- Versión SU3: Segundos desde la época, en ASCII (date +%s). NO se reinicia en 2038 o 2106.
- Formato de Archivo: XML o XML comprimido con gzip, que contiene un Feed XML [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom). El conjunto de caracteres debe ser UTF-8.

### Detalles del Feed Atom

Se utilizan los siguientes elementos `<feed>`:

**`<entry>`** : Un elemento de noticias. Ver más abajo.

**`<i2p:release>`** : Metadatos de actualización de I2P. Ver más abajo.

**`<i2p:revocations>`** : Revocaciones de certificados. Ver más abajo.

**`<i2p:blocklist>`** : Datos de lista de bloqueo. Ver abajo.

**`<updated>`** : Requerido. Marca de tiempo para el feed (conforme a la sección 3.3 de [RFC 4287](https://tools.ietf.org/html/rfc4287) y [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Detalles de la entrada Atom

Cada `<entry>` de Atom en el feed de noticias puede ser analizada y mostrada en la consola del router. Se utilizan los siguientes elementos:

**`<author>`** : Opcional. Contiene `<name>` - El nombre del autor de la entrada.

**`<content>`** : Requerido. Contenido, debe ser type="xhtml". El XHTML será sanitizado con una lista blanca de elementos permitidos y una lista negra de atributos no permitidos. Los clientes pueden ignorar un elemento, o la entrada que lo contiene, o todo el feed cuando se encuentre un elemento que no esté en la lista blanca.

**`<link>`** : Opcional. Enlace para más información.

**`<summary>`** : Opcional. Resumen breve, adecuado para un tooltip.

**`<title>`** : Requerido. Título de la entrada de noticias.

**`<updated>`** : Requerido. Marca de tiempo para esta entrada (conforme a la sección 3.3 de [RFC 4287](https://tools.ietf.org/html/rfc4287) y [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Detalles del Atom i2p:release

Debe haber al menos una entidad `<i2p:release>` en el feed. Cada una contiene los siguientes atributos y entidades:

**date (atributo)** : Requerido. Marca de tiempo para esta entrada (conforme a [RFC 4287](https://tools.ietf.org/html/rfc4287) sección 3.3 y [RFC 3339](https://tools.ietf.org/html/rfc3339)). La fecha también puede estar en formato truncado yyyy-mm-dd (sin la 'T'); este es el formato "full-date" en RFC 3339. En este formato se asume que la hora es 00:00:00 UTC para cualquier procesamiento.

**minJavaVersion (atributo)** : Si está presente, la versión mínima de Java requerida para ejecutar la versión actual.

**minVersion (atributo)** : Si está presente, la versión mínima del router requerida para actualizar a la versión actual. Si un router es más antiguo que esta, el usuario debe actualizar (¿manualmente?) a una versión intermedia primero.

**`<i2p:version>`** : Requerido. La última versión actual del router disponible.

**`<i2p:update>`** : Un archivo de actualización (uno o más). Debe contener al menos un hijo.   - type (atributo): "sud", "su2", o "su3". Debe ser único en todos los elementos `<i2p:update>`.   - `<i2p:clearnet>`: Enlaces de descarga directa fuera de la red (cero o más). href (atributo): Un enlace http clearnet estándar.   - `<i2p:clearnetssl>`: Enlaces de descarga directa fuera de la red (cero o más). href (atributo): Un enlace https clearnet estándar.   - `<i2p:torrent>`: Enlace magnet dentro de la red. href (atributo): Un enlace magnet.   - `<i2p:url>`: Enlaces de descarga directa dentro de la red (cero o más). href (atributo): Un enlace http .i2p dentro de la red.

### Detalles de Atom i2p:revocations

Esta entidad es opcional y hay como máximo una entidad `<i2p:revocations>` en el feed. Esta característica es compatible a partir de la versión 0.9.26.

La entidad `<i2p:revocations>` contiene una o más entidades `<i2p:crl>`. La entidad `<i2p:crl>` contiene los siguientes atributos:

**updated (atributo)** : Requerido. Marca de tiempo para esta entrada (conforme a [RFC 4287](https://tools.ietf.org/html/rfc4287) sección 3.3 y [RFC 3339](https://tools.ietf.org/html/rfc3339)). La fecha también puede estar en formato truncado yyyy-mm-dd (sin la 'T'); este es el formato "full-date" en RFC 3339. En este formato se asume que la hora es 00:00:00 UTC para cualquier procesamiento.

**id (atributo)** : Requerido. Un id único para el creador de esta CRL.

**(contenido de entidad)** : Requerido. Una Lista de Revocación de Certificados (CRL) estándar codificada en base 64 con saltos de línea, comenzando con la línea '-----BEGIN X509 CRL-----' y terminando con la línea '-----END X509 CRL-----'. Consulte [RFC 5280](https://tools.ietf.org/html/rfc5280) para más información sobre CRLs.

### Detalles de la lista de bloqueo i2p de Atom

Esta entidad es opcional y hay como máximo una entidad `<i2p:blocklist>` en el feed. Esta funcionalidad está programada para implementarse en la versión 0.9.28.

La entidad `<i2p:blocklist>` contiene una o más entidades `<i2p:block>` o `<i2p:unblock>`, una entidad "updated", y los atributos "signer" y "sig":

**signer (atributo)** : Requerido. Un id único (UTF-8) para la clave pública utilizada para firmar esta lista de bloqueo.

**sig (atributo)** : Requerido. Una firma en el formato code:b64sig, donde code es el número de tipo de firma ASCII, y b64sig es la firma codificada en base 64 (alfabeto I2P). Ver abajo para la especificación de los datos que deben ser firmados.

**`<updated>`** : Requerido. Marca de tiempo para la lista de bloqueo (conforme a la [RFC 4287](https://tools.ietf.org/html/rfc4287) sección 3.3 y [RFC 3339](https://tools.ietf.org/html/rfc3339)). La fecha también puede estar en formato truncado yyyy-mm-dd (sin la 'T'); este es el formato "full-date" en RFC 3339. En este formato se asume que la hora es 00:00:00 UTC para cualquier procesamiento.

**`<i2p:block>`** : Opcional, se permiten múltiples entidades. Una sola entrada, ya sea una dirección IPv4 o IPv6 literal, o un hash de router de 44 caracteres en base 64 (alfabeto I2P). Las direcciones IPv6 pueden estar en formato abreviado (conteniendo "::"). El soporte para entradas con máscara de red, por ejemplo x.y.0.0/16, es opcional. El soporte para nombres de host es opcional.

**`<i2p:unblock>`** : Opcional, se permiten múltiples entidades. Mismo formato que `<i2p:block>`.

**Especificación de firma:** Para generar los datos que se van a firmar o verificar, concatena los siguientes datos en codificación ASCII: La cadena actualizada seguida de una nueva línea (ASCII 0x0a), luego cada entrada de bloque en el orden recibido con una nueva línea después de cada una, luego cada entrada de desbloqueo en el orden recibido con una nueva línea después de cada una.

## Especificación de Archivo de Lista de Bloqueo

Por determinar, no implementado, ver propuesta 130. Las actualizaciones de la lista de bloqueo se entregan en el archivo de noticias, ver arriba.

## Trabajo Futuro

- El mecanismo de actualización del router es parte de la consola web del router. Actualmente no existe ninguna disposición para actualizaciones de un router integrado que carezca de la consola del router.

## Referencias

- **[CRYPTO-SIG]** [Criptografía - Firmas](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [Código Fuente de I2P](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Especificación de Plugin](/docs/specs/plugin)
- **[Python]** [Firmas RSA Raw en Python](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Fecha y Hora](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Formato de Sindicación Atom](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Listas de Revocación de Certificados](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Tipo de Firma](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [Tipo SigningPublicKey](/docs/specs/common-structures#signingpublickey)
