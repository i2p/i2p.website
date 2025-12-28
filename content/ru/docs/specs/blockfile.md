---
title: "Спецификация Blockfile (формат блочного файла)"
description: "Формат хранения на диске blockfile (блочный файл), используемый в I2P для разрешения имён хостов"
slug: "blockfile"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Обзор

Этот документ определяет **формат файла I2P blockfile** и таблицы в `hostsdb.blockfile`, используемые в **Blockfile Naming Service** (службе именования Blockfile). Для справки см. [Именование в I2P и адресная книга](/docs/overview/naming).

blockfile (файл блоков) позволяет выполнять **быстрый поиск назначений** в компактном двоичном формате.   По сравнению с устаревшей системой `hosts.txt`:

- Destinations (адреса назначения в I2P) хранятся в двоичном виде, а не в Base64.  
- Можно прикреплять произвольные метаданные (например, дату добавления, источник, комментарии).  
- Время поиска примерно **в 10× раз быстрее**.  
- Использование дискового пространства умеренно увеличивается.

Blockfile (файл блоков) — это хранящаяся на диске коллекция отсортированных отображений (пары ключ‑значение), реализованных в виде **скип-листов**. Он был создан на основе [Metanotion Blockfile Database](http://www.metanotion.net/software/sandbox/block.html). Эта спецификация сначала определяет структуру файла, затем описывает, как этот формат используется `BlockfileNamingService`.

> Blockfile Naming Service (служба имён на основе блочных файлов) заменила старую реализацию `hosts.txt` в **I2P 0.8.8**.   > При инициализации она импортирует записи из `privatehosts.txt`, `userhosts.txt` и `hosts.txt`.

---

## Формат Blockfile

Формат состоит из **1024-байтовых страниц**, каждая из которых имеет префикс в виде **магического числа** для обеспечения целостности.   Страницы нумеруются начиная с 1:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Page</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Superblock (starts at byte 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Metaindex skiplist (starts at byte 1024)</td>
    </tr>
  </tbody>
</table>
Все целые числа используют **сетевой порядок байтов (big-endian — старший байт первым)**.   2-байтовые значения беззнаковые; 4-байтовые значения (номера страниц) знаковые и должны быть положительными.

> **Потоковая модель:** База данных спроектирована для **однопоточного доступа**; `BlockfileNamingService` обеспечивает синхронизацию.

---

### Формат суперблока

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number <code>0x3141de493250</code> (<code>"1A"</code> <code>0xde</code> <code>"I2P"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major version <code>0x01</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minor version <code>0x02</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File length (in bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First free list page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-21</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mounted flag (<code>0x01</code> = yes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">22-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (max key/value pairs per span, 16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Page size (as of v1.2; 1024 before that)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Формат страницы блока Skip List (структура данных «список с пропусками»)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x536b69704c697374</code> (<code>"SkipList"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First level page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (total keys, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Spans (total spans, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24-27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Levels (total levels, valid at startup)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-29</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span size (as of v1.2; used for new spans)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">30-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Формат страницы блокировки при пропуске уровня

У каждого уровня есть диапазон, но не у каждого диапазона есть уровни.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x42534c6576656c73</code> (<code>"BSLevels"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current height</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Span page</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next level pages (<code>current height</code> × 4 bytes, lowest first)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remaining bytes unused</td>
    </tr>
  </tbody>
</table>
---

### Пропустить Span (строчный элемент) Block (блочный элемент) Формат страницы

Пары ключ/значение отсортированы по ключу по всем интервалам. Интервалы, кроме первого, не должны быть пустыми.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x5370616e</code> (<code>"Span"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">First continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Previous span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next span page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max keys (16 for hostsdb)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18-19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Size (current keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Формат страницы блока продолжения диапазона

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x434f4e54</code> (<code>"CONT"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next continuation page or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key/value structures</td>
    </tr>
  </tbody>
</table>
---

### Формат структуры ключ/значение

Для ключа и значения **поля длины не могут пересекать границы страниц** (все 4 байта должны уместиться).   Если остается недостаточно места, добавьте до 3 байт заполнения и продолжайте со смещения 8 на следующей странице.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2-3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Value length (bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4-…</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key data → Value data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&mdash;</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max length = 65535 bytes each</td>
    </tr>
  </tbody>
</table>
---

### Формат страницы блока свободного списка

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x2366724c69737423</code> (<code>"#frList#"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Next free list block or 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12-15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number of valid free pages (0 – 252)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Free page numbers (4 bytes each)</td>
    </tr>
  </tbody>
</table>
---

### Формат блока свободной страницы

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Byte</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic <code>0x7e2146524545217e</code> (<code>"~!FREE!~"</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-1023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unused</td>
    </tr>
  </tbody>
</table>
---

### Метаиндекс

Расположено на странице 2.   Отображает **строки US-ASCII** → **4-байтовые целые числа**.   Ключ — имя skiplist (список с пропусками); значение — индекс страницы.

---

## Таблицы службы имён Blockfile (формат блочного файла)

Сервис определяет несколько skiplist (структура данных «пропускающий список»).   Каждый диапазон поддерживает до 16 элементов.

---

### Свойства Skiplist (структура данных «скип-лист»)

`%%__INFO__%%` содержит одну запись:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>info</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A Properties object (UTF-8 String / String map) serialized as a Mapping</td>
    </tr>
  </tbody>
</table>
Типичные поля:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>version</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"4"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>created</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>upgraded</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java long (ms since epoch, since DB v2)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>lists</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma-separated host DBs (e.g. <code>privatehosts.txt,userhosts.txt,hosts.txt</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>listversion_*</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version of each DB (used to detect partial upgrades, since v4)</td>
    </tr>
  </tbody>
</table>
---

### Скип-лист обратного поиска

`%%__REVERSE__%%` содержит записи **Integer → Properties** (начиная с DB v2).

- **Ключ:** Первые 4 байта хэша SHA-256 от Destination (адреса назначения в I2P).  
- **Значение:** Объект Properties (сериализованный Mapping).  
- Несколько записей позволяют обрабатывать коллизии и Destinations с несколькими именами хоста.  
- Каждый ключ свойства = имя хоста; значение = пустая строка.

---

### Скип-листы базы данных хостов

Каждый из `hosts.txt`, `userhosts.txt` и `privatehosts.txt` сопоставляет имена хостов → назначения.

Версия 4 поддерживает несколько Destinations (уникальные адреса назначения) на одно имя хоста (введено в **I2P 0.9.26**).   Базы данных версии 3 мигрируются автоматически.

#### Ключ

Строка UTF-8 (имя хоста, в нижнем регистре, оканчивается на `.i2p`)

#### Значение

- **Версия 4:**  
  - 1 байт — количество пар свойство/Destination (адрес назначения)  
  - Для каждой пары: Свойства → Destination (в двоичном виде)
- **Версия 3:**  
  - Свойства → Destination (в двоичном виде)

#### Свойства DestEntry

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>a</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Time added (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>m</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Last modified (Java long ms)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>notes</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User comments</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>s</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Source (file or subscription URL)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>v</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verified (<code>true</code>/<code>false</code>)</td>
    </tr>
  </tbody>
</table>
---

## Примечания по реализации

Класс Java `BlockfileNamingService` реализует эту спецификацию.

- Вне контекста router, база данных открывается **только для чтения**, если не установлено `i2p.naming.blockfile.writeInAppContext=true`.  
- Не предназначено для доступа из нескольких экземпляров или нескольких JVM.  
- Поддерживает три основные отображения (`privatehosts`, `userhosts`, `hosts`) и обратное отображение для быстрого поиска.

---

## Ссылки

- [Документация по именованию и адресной книге I2P](/docs/overview/naming/)  
- [Спецификация общих структур](/docs/specs/common-structures/)  
- [База данных Metanotion Blockfile](http://www.metanotion.net/software/sandbox/block.html)  
- [JavaDoc для BlockfileNamingService](https://geti2p.net/javadoc/i2p/naming/BlockfileNamingService.html)
