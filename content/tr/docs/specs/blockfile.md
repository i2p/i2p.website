---
title: "Blockfile ve Hosts Veritabanı Spesifikasyonu"
description: "Blockfile Naming Service tarafından kullanılan I2P blockfile dosya biçimi ve hostsdb.blockfile içindeki tabloların belirtimi"
slug: "blockfile"
aliases:
  - "/tr/blockfile"
  - "/tr/blockfile/"
category: "Formatlar"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## Genel Bakış

Bu belge, I2P blockfile dosya biçimini ve Blockfile Naming Service [NAMING](/docs/overview/naming/) tarafından kullanılan hostsdb.blockfile içindeki tabloları belirtir.

Blockfile, kompakt bir formatta hızlı Destination araması sağlar. Blockfile sayfa ek yükü önemli olsa da, destination'lar hosts.txt formatındaki gibi Base 64 yerine binary olarak saklanır. Ayrıca, blockfile her giriş için keyfi metadata depolama yeteneği (ekleme tarihi, kaynak ve yorumlar gibi) sağlar. Metadata gelecekte gelişmiş adres defteri özelliklerini sağlamak için kullanılabilir. Blockfile depolama gereksinimi hosts.txt formatına göre mütevazı bir artıştır ve blockfile arama sürelerinde yaklaşık 10 kat azalma sağlar.

Bir blockfile, basitçe birden fazla sıralanmış haritanın (anahtar-değer çiftleri) disk üzerinde depolanması olup, skiplist'ler olarak uygulanır. Blockfile formatı Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html) formatından benimsenmiştir. Önce dosya formatını tanımlayacağız, ardından bu formatın BlockfileNamingService tarafından kullanımını açıklayacağız.

## Blockfile Formatı

Orijinal blockfile özelliği her sayfaya sihirli numaralar eklemek için değiştirildi. Dosya 1024 baytlık sayfalar halinde yapılandırılmıştır. Sayfalar 1'den başlayarak numaralandırılır. "Superblock" her zaman sayfa 1'dedir, yani dosyada 0 baytından başlar. Metaindex skiplist her zaman sayfa 2'dedir, yani dosyada 1024 baytından başlar.

Tüm 2-byte tamsayı değerleri işaretsizdir. Tüm 4-byte tamsayı değerleri (sayfa numaraları) işaretlidir ve negatif değerler geçersizdir. Tüm tamsayı değerleri ağ byte sırasında (big endian) saklanır.

Veritabanı tek bir thread tarafından açılıp erişilecek şekilde tasarlanmıştır. BlockfileNamingService senkronizasyonu sağlar.

### Superblock formatı

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
### Skip list blok sayfa formatı

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
### Atlama seviyesi blok sayfa formatı

Tüm seviyelerin bir aralığı vardır. Tüm aralıkların seviyesi yoktur.

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
### Span blok sayfa formatını atla

Anahtar/değer yapıları her span içinde ve tüm span'lar boyunca anahtara göre sıralanır. Anahtar/değer yapıları her span içinde anahtara göre sıralanır. İlk span dışındaki span'lar boş olamaz.

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
### Span Continuation blok sayfa formatı

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
### Anahtar/değer yapısı formatı

Anahtar ve değer uzunlukları sayfalar arasında bölünmemelidir, yani tüm 4 bayt aynı sayfada olmalıdır. Yeterli yer yoksa, bir sayfanın son 1-3 baytı kullanılmaz ve uzunluklar devam sayfasında offset 8'de yer alır. Anahtar ve değer verileri sayfalar arasında bölünebilir. Maksimum anahtar ve değer uzunlukları 65535 bayttır.

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
### Serbest liste blok sayfa formatı

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
### Serbest sayfa blok formatı

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
Metaindex (sayfa 2'de bulunur), US-ASCII dizelerini 4-byte tam sayılarla eşleştiren bir haritadır. Anahtar, skiplist'in adıdır ve değer, skiplist'in sayfa dizinidir.

## Blockfile İsimlendirme Servisi Tabloları

BlockfileNamingService tarafından oluşturulan ve kullanılan tablolar aşağıdaki gibidir. Span başına maksimum giriş sayısı 16'dır.

### Özellikler Atlama Listesi

`%%__INFO__%%`, yalnızca bir girdi içeren String/Properties anahtar/değer girişleri ile ana veritabanı skiplist'idir:

**info** - bir Properties (UTF-8 String/String Map), [Mapping](/docs/specs/common-structures/#type-mapping) olarak serileştirilmiş:

- **version** - "4"
- **created** - Java long time (ms)
- **upgraded** - Java long time (ms) (veritabanı sürüm 2 itibariyle)
- **lists** - Aramalar için sırayla aranacak host veritabanlarının virgülle ayrılmış listesi. Neredeyse her zaman "privatehosts.txt,userhosts.txt,hosts.txt".
- **listversion_*** - lists içindeki her veritabanının sürümü, örneğin: listversion_hosts.txt=4. Bireysel listelerin kısmi veya yarıda kalan yükseltmelerini tanımlamak için kullanılır. (veritabanı sürüm 4 itibariyle)

### Ters Arama Skiplist

`%%__REVERSE__%%`, Integer/Properties anahtar/değer girişleri içeren ters arama skiplist'idir (veritabanı sürüm 2 itibariyle):

- Skiplist anahtarları 4-byte Integer'lardır, [Destination](/docs/specs/common-structures/#struct-destination) hash'inin ilk 4 byte'ıdır.
- Skiplist değerleri, her biri bir [Mapping](/docs/specs/common-structures/#type-mapping) olarak serileştirilen Properties'tir (bir UTF-8 String/String Map)
  - Properties'te birden fazla giriş olabilir, her biri ters eşleme olduğundan, belirli bir destination için birden fazla hostname olabilir veya hash'in aynı ilk 4 byte'ı ile çakışmalar olabilir.
  - Her property anahtarı bir hostname'dir.
  - Her property değeri boş string'dir.

### hosts.txt, userhosts.txt ve privatehosts.txt Atlama Listeleri

Her host veritabanı için, o veritabanındaki hostları içeren bir skiplist bulunur. Sürüm 4 formatının hostname başına birden fazla Destination'ı desteklediğini unutmayın. Bu format I2P sürümü 0.9.26'da tanıtıldı. Sürüm 3 veritabanları otomatik olarak sürüm 4'e geçirilir.

Bu skiplists'lerdeki anahtar/değer çiftleri şu şekildedir:

**key** - bir UTF-8 String (hostname)

**değer** - - Veritabanı sürüm 4: Bir DestEntry, takip edecek Properties/Destination çiftlerinin sayısını belirten tek baytlık bir sayıdır. O sayı kadar çift: Bir Properties (UTF-8 String/String Map) [Mapping](/docs/specs/common-structures/#type-mapping) olarak serileştirilmiş ve ardından ikili [Destination](/docs/specs/common-structures/#struct-destination) (her zamanki gibi serileştirilmiş). - Veritabanı sürüm 3: bir DestEntry, [Mapping](/docs/specs/common-structures/#type-mapping) olarak serileştirilmiş Properties (UTF-8 String/String Map) ve ardından ikili [Destination](/docs/specs/common-structures/#struct-destination) (her zamanki gibi serileştirilmiş).

DestEntry Properties genellikle şunları içerir:

- **"a"** - Eklenme zamanı (Java long time ms cinsinden)
- **"m"** - Son değiştirilme zamanı (Java long time ms cinsinden)
- **"notes"** - Kullanıcı tarafından sağlanan yorumlar
- **"s"** - Girişin orijinal kaynağı (genellikle dosya adı veya abonelik URL'si)
- **"v"** - Girişin imzası doğrulandıysa, "true" veya "false"

Hostname anahtarları küçük harflerle saklanır ve her zaman ".i2p" ile biter.

## Referanslar

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [ADLANDIRMA](/docs/overview/naming/)
