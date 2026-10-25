---
title: "Blockfile and Hosts Database Specification"
description: "Specification of the I2P blockfile file format and the tables in the hostsdb.blockfile used by the Blockfile Naming Service"
slug: "blockfile"
aliases:
  - "/en/blockfile"
  - "/en/blockfile/"
category: "Formats"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Overview

This document specifies the I2P blockfile file format and the tables in
the hostsdb.blockfile used by the Blockfile Naming Service [NAMING](/docs/overview/naming/).

The blockfile provides fast Destination lookup in a compact format.
While the blockfile page overhead is substantial, the destinations are
stored in binary rather than in Base 64 as in the hosts.txt format. In
addition, the blockfile provides the capability of arbitrary metadata
storage (such as added date, source, and comments) for each entry. The
metadata may be used in the future to provide advanced addressbook
features. The blockfile storage requirement is a modest increase over
the hosts.txt format, and the blockfile provides approximately 10x
reduction in lookup times.

A blockfile is simply on-disk storage of multiple sorted maps (key-value
pairs), implemented as skiplists. The blockfile format is adopted from
the Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html). First we will define the file
format, then the use of that format by the BlockfileNamingService.

## Blockfile Format

The original blockfile spec was modified to add magic numbers to each
page. The file is structured in 1024-byte pages. Pages are numbered
starting from 1. The "superblock" is always at page 1, i.e. starting
at byte 0 in the file. The metaindex skiplist is always at page 2, i.e.
starting at byte 1024 in the file.

All 2-byte integer values are unsigned. All 4-byte integer values (page
numbers) are signed and negative values are illegal. All integer values
are stored in network byte order (big endian).

The database is designed to be opened and accessed by a single thread.
The BlockfileNamingService provides synchronization.

### Superblock format

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

### Skip list block page format

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

### Skip level block page format

All levels have a span. Not all spans have levels.

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

### Skip span block page format

Key/value structures are sorted by key within each span and across all spans.
Key/value structures are sorted by key within each span.
Spans other than the first span may not be empty.

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

### Span Continuation block page format

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

### Key/value structure format

Key and value lengths must not be split across pages, i.e. all 4 bytes must be on the same page.
If there is not enough room the last 1-3 bytes of a page are unused and the
lengths will be at offset 8 in the continuation page. Key and value data
may be split across pages. Max key and value lengths are 65535 bytes.

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

### Free list block page format

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

### Free page block format

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

The metaindex (located at page 2) is a mapping of US-ASCII strings to
4-byte integers. The key is the name of the skiplist and the value is
the page index of the skiplist.


## Blockfile Naming Service Tables

The tables created and used by the BlockfileNamingService are as
follows. The maximum number of entries per span is 16.

### Properties Skiplist

`%%__INFO__%%` is the main database skiplist with String/Properties key/value
entries containing only one entry:

**info** - a Properties (UTF-8 String/String Map), serialized as a [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Java long time (ms)
- **upgraded** - Java long time (ms) (as of database version 2)
- **lists** - Comma-separated list of host databases, to be searched in-order for lookups. Almost always "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - The version of each database in lists, for example: listversion_hosts.txt=4. Used to identify partial or aborted upgrade of individual lists. (as of database version 4)


### Reverse Lookup Skiplist

`%%__REVERSE__%%` is the reverse lookup skiplist with Integer/Properties
key/value entries (as of database version 2):

- The skiplist keys are 4-byte Integers, the first 4 bytes of the hash of the [Destination](/docs/specs/common-structures/#struct-destination).
- The skiplist values are each a Properties (a UTF-8 String/String Map) serialized as a [Mapping](/docs/specs/common-structures/#type-mapping)
  - There may be multiple entries in the properties, each one is a reverse mapping, as there may be more than one hostname for a given destination, or there could be collisions with the same first 4 bytes of the hash.
  - Each property key is a hostname.
  - Each property value is the empty string.

### hosts.txt, userhosts.txt, and privatehosts.txt Skiplists

For each host database, there is a skiplist containing the hosts for
that database. Note that the version 4 format supports multiple
Destinations per hostname. This format was introduced in I2P release
0.9.26. Version 3 databases are automatically migrated to version 4.

The keys/values in these skiplists are as follows:

**key** - a UTF-8 String (the hostname)

**value** -
- Database version 4: A DestEntry, which is a one-byte number of Properties/Destination pairs to follow. That number of pairs of: A Properties (a UTF-8 String/String Map) serialized as a [Mapping](/docs/specs/common-structures/#type-mapping) followed by a binary [Destination](/docs/specs/common-structures/#struct-destination) (serialized as usual).
- Database version 3: a DestEntry, which is a Properties (a UTF-8 String/String Map) serialized as a [Mapping](/docs/specs/common-structures/#type-mapping) followed by a binary [Destination](/docs/specs/common-structures/#struct-destination) (serialized as usual).

The DestEntry Properties typically contains:

- **"a"** - The time added (Java long time in ms)
- **"m"** - The time last modified (Java long time in ms)
- **"notes"** - User-supplied comments
- **"s"** - The original source of the entry (typically a file name or subscription URL)
- **"v"** - If the signature of the entry was verified, "true" or "false"

Hostname keys are stored in lower-case and always end in ".i2p".


## References

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
