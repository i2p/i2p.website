---
title: "Blockfile- und Hosts-Datenbank-Spezifikation"
description: "Spezifikation des I2P-Blockfile-Dateiformats und der Tabellen in der hostsdb.blockfile, die vom Blockfile Naming Service verwendet werden"
slug: "blockfile"
aliases:
  - "/de/blockfile"
  - "/de/blockfile/"
category: "Formate"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Überblick

Dieses Dokument spezifiziert das I2P blockfile Dateiformat und die Tabellen in der hostsdb.blockfile, die vom Blockfile Naming Service [NAMING](/docs/overview/naming/) verwendet werden.

Die Blockdatei bietet eine schnelle Destination-Suche in einem kompakten Format. Obwohl der Overhead der Blockdatei-Seiten erheblich ist, werden die Destinations in binärer Form gespeichert und nicht in Base 64 wie im hosts.txt-Format. Zusätzlich bietet die Blockdatei die Möglichkeit, beliebige Metadaten (wie Hinzufügungsdatum, Quelle und Kommentare) für jeden Eintrag zu speichern. Die Metadaten können in Zukunft verwendet werden, um erweiterte Adressbuch-Funktionen bereitzustellen. Der Speicherbedarf der Blockdatei ist nur geringfügig höher als beim hosts.txt-Format, und die Blockdatei bietet etwa eine 10-fache Reduzierung der Suchzeiten.

Eine Blockfile ist einfach eine festplattenbasierte Speicherung mehrerer sortierter Maps (Schlüssel-Wert-Paare), implementiert als Skiplists. Das Blockfile-Format wurde von der Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html) übernommen. Zuerst werden wir das Dateiformat definieren, dann die Verwendung dieses Formats durch den BlockfileNamingService.

## Blockfile-Format

Die ursprüngliche Blockfile-Spezifikation wurde modifiziert, um jeder Seite magische Zahlen hinzuzufügen. Die Datei ist in 1024-Byte-Seiten strukturiert. Die Seiten werden beginnend mit 1 nummeriert. Der "Superblock" befindet sich immer auf Seite 1, d.h. beginnend bei Byte 0 in der Datei. Die Metaindex-Skiplist befindet sich immer auf Seite 2, d.h. beginnend bei Byte 1024 in der Datei.

Alle 2-Byte-Ganzzahlenwerte sind vorzeichenlos. Alle 4-Byte-Ganzzahlenwerte (Seitennummern) sind vorzeichenbehaftet und negative Werte sind unzulässig. Alle Ganzzahlenwerte werden in Netzwerk-Byte-Reihenfolge (Big Endian) gespeichert.

Die Datenbank ist so konzipiert, dass sie von einem einzigen Thread geöffnet und darauf zugegriffen werden kann. Der BlockfileNamingService stellt die Synchronisation bereit.

### Superblock-Format

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
### Skip-Liste Block-Seitenformat

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
### Skip-Level-Block-Seitenformat

Alle Ebenen haben eine Spanne. Nicht alle Spannen haben Ebenen.

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
### Span-Block-Seitenformat überspringen

Schlüssel/Wert-Strukturen sind nach Schlüssel innerhalb jedes Bereichs und über alle Bereiche hinweg sortiert. Schlüssel/Wert-Strukturen sind nach Schlüssel innerhalb jedes Bereichs sortiert. Bereiche außer dem ersten Bereich dürfen nicht leer sein.

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
### Span Continuation Block-Seitenformat

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
### Schlüssel/Wert-Strukturformat

Schlüssel- und Wertlängen dürfen nicht über Seiten aufgeteilt werden, d.h. alle 4 Bytes müssen sich auf derselben Seite befinden. Wenn nicht genügend Platz vorhanden ist, bleiben die letzten 1-3 Bytes einer Seite ungenutzt und die Längen befinden sich bei Offset 8 auf der Fortsetzungsseite. Schlüssel- und Wertdaten können über Seiten aufgeteilt werden. Die maximalen Schlüssel- und Wertlängen betragen 65535 Bytes.

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
### Format der freien Liste Blockseite

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
### Format für freie Seitenblöcke

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
Der Metaindex (befindet sich auf Seite 2) ist eine Zuordnung von US-ASCII-Zeichenketten zu 4-Byte-Ganzzahlen. Der Schlüssel ist der Name der Skiplist und der Wert ist der Seitenindex der Skiplist.

## Blockfile Naming Service Tabellen

Die vom BlockfileNamingService erstellten und verwendeten Tabellen sind wie folgt. Die maximale Anzahl der Einträge pro Span beträgt 16.

### Properties Skiplist

`%%__INFO__%%` ist die Haupt-Datenbank-Skiplist mit String/Properties-Schlüssel/Wert-Einträgen, die nur einen Eintrag enthält:

**info** - ein Properties (UTF-8 String/String Map), serialisiert als ein [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Java long time (ms)
- **upgraded** - Java long time (ms) (ab Datenbankversion 2)
- **lists** - Komma-getrennte Liste von Host-Datenbanken, die in der angegebenen Reihenfolge für Lookups durchsucht werden. Fast immer "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - Die Version jeder Datenbank in lists, zum Beispiel: listversion_hosts.txt=4. Wird verwendet, um teilweise oder abgebrochene Upgrades einzelner Listen zu identifizieren. (ab Datenbankversion 4)

### Reverse Lookup Skiplist

`%%__REVERSE__%%` ist die Reverse-Lookup-Skiplist mit Integer/Properties-Schlüssel/Wert-Einträgen (ab Datenbankversion 2):

- Die skiplist-Schlüssel sind 4-Byte-Integer, die ersten 4 Bytes des Hashes der [Destination](/docs/specs/common-structures/#struct-destination).
- Die skiplist-Werte sind jeweils eine Properties (eine UTF-8 String/String Map), serialisiert als [Mapping](/docs/specs/common-structures/#type-mapping)
  - Es kann mehrere Einträge in den Properties geben, jeder ist ein umgekehrtes Mapping, da es mehr als einen Hostnamen für eine gegebene Destination geben kann, oder es könnte Kollisionen mit denselben ersten 4 Bytes des Hashes geben.
  - Jeder Property-Schlüssel ist ein Hostname.
  - Jeder Property-Wert ist der leere String.

### hosts.txt, userhosts.txt und privatehosts.txt Sperrlisten

Für jede Host-Datenbank gibt es eine Skiplist, die die Hosts für diese Datenbank enthält. Beachten Sie, dass das Version-4-Format mehrere Destinations pro Hostname unterstützt. Dieses Format wurde in I2P-Version 0.9.26 eingeführt. Version-3-Datenbanken werden automatisch zu Version 4 migriert.

Die Schlüssel/Werte in diesen Skiplisten sind wie folgt:

**key** - ein UTF-8 String (der Hostname)

**value** - - Datenbankversion 4: Ein DestEntry, welcher eine Ein-Byte-Zahl von Properties/Destination-Paaren ist, die folgen. Diese Anzahl von Paaren aus: Properties (eine UTF-8 String/String Map) serialisiert als [Mapping](/docs/specs/common-structures/#type-mapping), gefolgt von einer binären [Destination](/docs/specs/common-structures/#struct-destination) (wie üblich serialisiert). - Datenbankversion 3: ein DestEntry, welcher Properties (eine UTF-8 String/String Map) serialisiert als [Mapping](/docs/specs/common-structures/#type-mapping) ist, gefolgt von einer binären [Destination](/docs/specs/common-structures/#struct-destination) (wie üblich serialisiert).

Die DestEntry-Eigenschaften enthalten normalerweise:

- **"a"** - Die Zeit der Hinzufügung (Java long Zeit in ms)
- **"m"** - Die Zeit der letzten Änderung (Java long Zeit in ms)
- **"notes"** - Benutzerdefinierte Kommentare
- **"s"** - Die ursprüngliche Quelle des Eintrags (normalerweise ein Dateiname oder eine Abonnement-URL)
- **"v"** - Ob die Signatur des Eintrags verifiziert wurde, "true" oder "false"

Hostname-Schlüssel werden in Kleinbuchstaben gespeichert und enden immer mit ".i2p".

## Referenzen

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
