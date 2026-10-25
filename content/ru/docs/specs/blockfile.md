---
title: "Спецификация Blockfile и базы данных Hosts"
description: "Спецификация формата файла I2P blockfile и таблиц в hostsdb.blockfile, используемых службой именования Blockfile"
slug: "blockfile"
aliases:
  - "/ru/blockfile"
  - "/ru/blockfile/"
category: "Форматы"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Обзор

Данный документ описывает формат файлов I2P blockfile и таблицы в hostsdb.blockfile, используемые службой имен Blockfile [NAMING](/docs/overview/naming/).

Блочный файл обеспечивает быстрый поиск Destination в компактном формате. Хотя накладные расходы на страницы блочного файла существенны, destinations хранятся в бинарном формате, а не в Base 64, как в формате hosts.txt. Кроме того, блочный файл предоставляет возможность хранения произвольных метаданных (таких как дата добавления, источник и комментарии) для каждой записи. Метаданные могут использоваться в будущем для предоставления расширенных возможностей адресной книги. Требования к хранилищу блочного файла незначительно превышают формат hosts.txt, при этом блочный файл обеспечивает примерно 10-кратное сокращение времени поиска.

Blockfile — это просто дисковое хранилище нескольких отсортированных карт (пар ключ-значение), реализованное как списки с пропусками. Формат blockfile заимствован из базы данных Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html). Сначала мы определим формат файла, затем рассмотрим использование этого формата службой BlockfileNamingService.

## Формат файла блоков

Оригинальная спецификация blockfile была изменена для добавления магических чисел на каждую страницу. Файл структурирован в виде страниц размером 1024 байта. Страницы нумеруются начиная с 1. "Суперблок" всегда находится на странице 1, т.е. начиная с байта 0 в файле. Метаиндекс skiplist всегда находится на странице 2, т.е. начиная с байта 1024 в файле.

Все 2-байтовые целочисленные значения являются беззнаковыми. Все 4-байтовые целочисленные значения (номера страниц) являются знаковыми, и отрицательные значения недопустимы. Все целочисленные значения хранятся в сетевом порядке байтов (big endian).

База данных спроектирована для открытия и доступа одним потоком. BlockfileNamingService обеспечивает синхронизацию.

### Формат суперблока

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
### Формат страницы блока списка пропусков

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
### Формат страницы блока пропуска уровня

Все уровни имеют диапазон. Не все диапазоны имеют уровни.

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
### Пропустить формат страницы блока span

Структуры ключ/значение сортируются по ключу внутри каждого диапазона и во всех диапазонах. Структуры ключ/значение сортируются по ключу внутри каждого диапазона. Диапазоны, кроме первого диапазона, не могут быть пустыми.

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
### Формат страницы блока продолжения диапазона

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
### Формат структуры ключ/значение

Длины ключей и значений не должны разделяться между страницами, т.е. все 4 байта должны находиться на одной странице. Если места недостаточно, последние 1-3 байта страницы остаются неиспользованными, а длины будут располагаться со смещением 8 в продолжающей странице. Данные ключей и значений могут разделяться между страницами. Максимальные длины ключей и значений составляют 65535 байт.

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
### Формат страницы блока свободного списка

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
### Формат блока свободной страницы

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
Метаиндекс (расположенный на странице 2) представляет собой отображение строк US-ASCII на 4-байтовые целые числа. Ключ — это название skiplist, а значение — индекс страницы skiplist.

## Таблицы службы имен Blockfile

Таблицы, создаваемые и используемые BlockfileNamingService, следующие. Максимальное количество записей на промежуток составляет 16.

### Список пропуска свойств

`%%__INFO__%%` — это главный skiplist базы данных с записями ключ/значение String/Properties, содержащий только одну запись:

**info** - Properties (UTF-8 String/String Map), сериализованный как [Mapping](/docs/specs/common-structures/#type-mapping):

- **version** - "4"
- **created** - Java long время (мс)
- **upgraded** - Java long время (мс) (начиная с версии базы данных 2)
- **lists** - Список баз данных хостов, разделенный запятыми, которые должны быть просмотрены по порядку при поиске. Почти всегда "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - Версия каждой базы данных в списках, например: listversion_hosts.txt=4. Используется для определения частичного или прерванного обновления отдельных списков. (начиная с версии базы данных 4)

### Список пропусков обратного поиска

`%%__REVERSE__%%` — это skiplist обратного поиска с записями ключ/значение типа Integer/Properties (начиная с версии базы данных 2):

- Ключи skiplist являются 4-байтовыми целыми числами, первые 4 байта хэша [Destination](/docs/specs/common-structures/#struct-destination).
- Значения skiplist представляют собой Properties (карта UTF-8 строк), сериализованная как [Mapping](/docs/specs/common-structures/#type-mapping)
  - В свойствах может быть несколько записей, каждая из которых является обратным отображением, поскольку для данного destination может быть более одного имени хоста, или могут возникнуть коллизии с одинаковыми первыми 4 байтами хэша.
  - Каждый ключ свойства является именем хоста.
  - Каждое значение свойства является пустой строкой.

### Списки пропуска hosts.txt, userhosts.txt и privatehosts.txt

Для каждой базы данных хостов существует skiplist, содержащий хосты для этой базы данных. Обратите внимание, что формат версии 4 поддерживает несколько Destination для каждого имени хоста. Этот формат был введен в релизе I2P 0.9.26. Базы данных версии 3 автоматически мигрируют в версию 4.

Ключи/значения в этих списках с пропусками следующие:

**key** - строка UTF-8 (имя хоста)

**value** - - База данных версии 4: DestEntry, который представляет собой однобайтовое число пар Свойства/Назначение, которые следуют далее. Это количество пар: Свойства (UTF-8 карта Строка/Строка), сериализованные как [Mapping](/docs/specs/common-structures/#type-mapping), за которыми следует бинарное [Destination](/docs/specs/common-structures/#struct-destination) (сериализованное обычным образом). - База данных версии 3: DestEntry, который представляет собой Свойства (UTF-8 карта Строка/Строка), сериализованные как [Mapping](/docs/specs/common-structures/#type-mapping), за которыми следует бинарное [Destination](/docs/specs/common-structures/#struct-destination) (сериализованное обычным образом).

Свойства DestEntry обычно содержат:

- **"a"** - Время добавления (Java long время в мс)
- **"m"** - Время последнего изменения (Java long время в мс)
- **"notes"** - Комментарии пользователя
- **"s"** - Исходный источник записи (обычно имя файла или URL подписки)
- **"v"** - Если подпись записи была проверена, "true" или "false"

Ключи имен хостов хранятся в нижнем регистре и всегда заканчиваются на ".i2p".

## Ссылки

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
