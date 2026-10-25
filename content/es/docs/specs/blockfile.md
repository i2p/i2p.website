---
title: "Especificación de Archivo de Bloqueo y Base de Datos de Hosts"
description: "Especificación del formato de archivo blockfile de I2P y las tablas en hostsdb.blockfile utilizadas por el Servicio de Nombres Blockfile"
slug: "blockfile"
aliases:
  - "/es/blockfile"
  - "/es/blockfile/"
category: "Formatos"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Resumen

Este documento especifica el formato de archivo blockfile de I2P y las tablas en el hostsdb.blockfile utilizado por el Servicio de Nomenclatura Blockfile [NAMING](/docs/overview/naming/).

El blockfile proporciona una búsqueda rápida de Destination en un formato compacto. Aunque la sobrecarga de páginas del blockfile es sustancial, los destinations se almacenan en binario en lugar de en Base 64 como en el formato hosts.txt. Además, el blockfile proporciona la capacidad de almacenamiento arbitrario de metadatos (como fecha de adición, fuente y comentarios) para cada entrada. Los metadatos pueden utilizarse en el futuro para proporcionar características avanzadas de la libreta de direcciones. El requerimiento de almacenamiento del blockfile es un incremento modesto sobre el formato hosts.txt, y el blockfile proporciona aproximadamente una reducción de 10x en los tiempos de búsqueda.

Un blockfile es simplemente almacenamiento en disco de múltiples mapas ordenados (pares clave-valor), implementados como skiplists. El formato blockfile está adoptado de la Base de Datos Blockfile de Metanotion [METANOTION](http://www.metanotion.net/software/sandbox/block.html). Primero definiremos el formato de archivo, luego el uso de ese formato por el BlockfileNamingService.

## Formato de Archivo de Bloques

La especificación original del blockfile fue modificada para agregar números mágicos a cada página. El archivo está estructurado en páginas de 1024 bytes. Las páginas están numeradas comenzando desde 1. El "superbloque" siempre está en la página 1, es decir, comenzando en el byte 0 del archivo. La skiplist del metaíndice siempre está en la página 2, es decir, comenzando en el byte 1024 del archivo.

Todos los valores enteros de 2 bytes son sin signo. Todos los valores enteros de 4 bytes (números de página) son con signo y los valores negativos son ilegales. Todos los valores enteros se almacenan en orden de bytes de red (big endian).

La base de datos está diseñada para ser abierta y accedida por un solo hilo. El BlockfileNamingService proporciona sincronización.

### Formato de superbloque

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x3141de493250 ("1A" 0xde "I2P")</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Major version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x02</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">File length</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x01 = yes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max number of key/value pairs per span (16 for hostsdb). Used for new skip lists.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Page size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Prior to 1.2, 1024 is assumed.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Formato de página de bloque de lista de saltos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x536b69704c697374 "SkipList"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of keys - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Spans</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of spans - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Levels</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Total number of levels - may only be valid at startup</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">As of version 1.2. Max number of key/value pairs per span. Prior to that, specified for all skiplists in the superblock. Used for new spans in this skip list.</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Formato de página de bloque de nivel de salto

Todos los niveles tienen un span. No todos los spans tienen niveles.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x42534c6576656c73 "BSLevels"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">'current height' entries, 4 bytes each, lowest first</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">remaining</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Omitir formato de página de bloque span

Las estructuras clave/valor se ordenan por clave dentro de cada span y a través de todos los spans. Las estructuras clave/valor se ordenan por clave dentro de cada span. Los spans distintos al primer span no pueden estar vacíos.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x5370616e "Span"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16 for hostsdb</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Current number of keys</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Formato de página de bloque de continuación de span

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x434f4e54 "CONT"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key/value structures</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
### Formato de estructura clave/valor

Las longitudes de clave y valor no deben dividirse entre páginas, es decir, los 4 bytes deben estar en la misma página. Si no hay suficiente espacio, los últimos 1-3 bytes de una página quedan sin usar y las longitudes estarán en el desplazamiento 8 en la página de continuación. Los datos de clave y valor pueden dividirse entre páginas. Las longitudes máximas de clave y valor son 65535 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">value length in bytes</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-</td><td style="border:1px solid var(--color-border); padding:0.6rem;">key data</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;"></td><td style="border:1px solid var(--color-border); padding:0.6rem;">value data</td></tr>
</tbody>
</table>
### Formato de página de bloque de lista libre

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x2366724c69737423 "#frList#"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block</td><td style="border:1px solid var(--color-border); padding:0.6rem;">or 0 if none</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">in this block (0 - 252)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Free pages</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes each, only the first (valid number) are valid</td></tr>
</tbody>
</table>
### Formato de bloque de página libre

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0x7e2146524545217e "~!FREE!~"</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td><td style="border:1px solid var(--color-border); padding:0.6rem;">unused</td><td style="border:1px solid var(--color-border); padding:0.6rem;"></td></tr>
</tbody>
</table>
El metaíndice (ubicado en la página 2) es una asignación de cadenas US-ASCII a enteros de 4 bytes. La clave es el nombre de la skiplist y el valor es el índice de página de la skiplist.

## Tablas del Servicio de Nombres Blockfile

Las tablas creadas y utilizadas por el BlockfileNamingService son las siguientes. El número máximo de entradas por span es 16.

### Lista de Salto de Propiedades

`%%__INFO__%%` es la skiplist principal de la base de datos con entradas clave/valor String/Properties que contiene solo una entrada:

**info** - un Properties (Mapa de Cadena/Cadena UTF-8), serializado como un [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Tiempo largo de Java (ms)
- **upgraded** - Tiempo largo de Java (ms) (a partir de la versión 2 de la base de datos)
- **lists** - Lista separada por comas de bases de datos de hosts, que se buscarán en orden para las consultas. Casi siempre "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - La versión de cada base de datos en las listas, por ejemplo: listversion_hosts.txt=4. Se usa para identificar actualizaciones parciales o interrumpidas de listas individuales. (a partir de la versión 4 de la base de datos)

### Lista de Salto de Búsqueda Inversa

`%%__REVERSE__%%` es la skiplist de búsqueda inversa con entradas clave/valor Integer/Properties (a partir de la versión 2 de la base de datos):

- Las claves de la skiplist son enteros de 4 bytes, los primeros 4 bytes del hash del [Destination](/docs/specs/common-structures/#struct-destination).
- Los valores de la skiplist son cada uno una Properties (un Mapa String/String UTF-8) serializado como un [Mapping](/docs/specs/common-structures/#type-mapping)
  - Puede haber múltiples entradas en las propiedades, cada una es un mapeo inverso, ya que puede haber más de un nombre de host para un destino dado, o podría haber colisiones con los mismos primeros 4 bytes del hash.
  - Cada clave de propiedad es un nombre de host.
  - Cada valor de propiedad es la cadena vacía.

### Listas de exclusión de hosts.txt, userhosts.txt y privatehosts.txt

Para cada base de datos de hosts, hay una skiplist que contiene los hosts para esa base de datos. Tenga en cuenta que el formato versión 4 admite múltiples Destinations por nombre de host. Este formato se introdujo en la versión 0.9.26 de I2P. Las bases de datos versión 3 se migran automáticamente a la versión 4.

Las claves/valores en estas skiplists son las siguientes:

**key** - una cadena UTF-8 (el nombre del host)

**value** - - Versión 4 de base de datos: Una DestEntry, que es un número de un byte de pares Properties/Destination a seguir. Ese número de pares de: Un Properties (un Mapa UTF-8 String/String) serializado como un [Mapping](/docs/specs/common-structures/#type-mapping) seguido por un [Destination](/docs/specs/common-structures/#struct-destination) binario (serializado como de costumbre). - Versión 3 de base de datos: una DestEntry, que es un Properties (un Mapa UTF-8 String/String) serializado como un [Mapping](/docs/specs/common-structures/#type-mapping) seguido por un [Destination](/docs/specs/common-structures/#struct-destination) binario (serializado como de costumbre).

Las propiedades DestEntry típicamente contienen:

- **"a"** - El tiempo agregado (tiempo largo de Java en ms)
- **"m"** - El tiempo de la última modificación (tiempo largo de Java en ms)
- **"notes"** - Comentarios proporcionados por el usuario
- **"s"** - La fuente original de la entrada (típicamente un nombre de archivo o URL de suscripción)
- **"v"** - Si la firma de la entrada fue verificada, "true" o "false"

Las claves de nombre de host se almacenan en minúsculas y siempre terminan en ".i2p".

## Referencias

- [Destino](/docs/specs/common-structures/#struct-destination)
- [Mapeo](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NOMENCLATURA](/docs/overview/naming/)
