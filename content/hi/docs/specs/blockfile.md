---
title: "Blockfile और Hosts Database विशिष्टता"
description: "I2P blockfile फ़ाइल फॉर्मेट और Blockfile Naming Service द्वारा उपयोग की जाने वाली hostsdb.blockfile में तालिकाओं का विनिर्देश"
slug: "blockfile"
aliases:
  - "/hi/blockfile"
  - "/hi/blockfile/"
category: "प्रारूप"
lastUpdated: "2023-11"
accurateFor: "0.9.59"
---

## अवलोकन

यह दस्तावेज़ I2P blockfile फ़ाइल प्रारूप और Blockfile Naming Service [NAMING](/docs/overview/naming/) द्वारा उपयोग की जाने वाली hostsdb.blockfile में टेबलों को निर्दिष्ट करता है।

blockfile एक कॉम्पैक्ट फॉर्मेट में तेज़ Destination lookup प्रदान करता है। जबकि blockfile page overhead काफी है, destinations को hosts.txt फॉर्मेट की तरह Base 64 में नहीं बल्कि binary में संग्रहीत किया जाता है। इसके अलावा, blockfile प्रत्येक entry के लिए मनमाना metadata storage (जैसे कि added date, source, और comments) की सुविधा प्रदान करता है। भविष्य में metadata का उपयोग उन्नत addressbook सुविधाएं प्रदान करने के लिए किया जा सकता है। blockfile storage requirement hosts.txt फॉर्मेट की तुलना में मामूली वृद्धि है, और blockfile lookup times में लगभग 10x कमी प्रदान करता है।

एक blockfile केवल कई sorted maps (key-value pairs) का on-disk storage है, जो skiplists के रूप में implemented है। blockfile format को Metanotion Blockfile Database [METANOTION](http://www.metanotion.net/software/sandbox/block.html) से अपनाया गया है। पहले हम file format को define करेंगे, फिर BlockfileNamingService द्वारा उस format के उपयोग को समझाएंगे।

## ब्लॉकफाइल प्रारूप

मूल blockfile स्पेक को प्रत्येक page में magic numbers जोड़ने के लिए संशोधित किया गया था। फ़ाइल 1024-byte pages में संरचित है। Pages की संख्या 1 से शुरू होती है। "superblock" हमेशा page 1 पर होता है, यानी फ़ाइल में byte 0 से शुरू होता है। metaindex skiplist हमेशा page 2 पर होता है, यानी फ़ाइल में byte 1024 से शुरू होता है।

सभी 2-byte integer मान unsigned हैं। सभी 4-byte integer मान (page numbers) signed हैं और negative मान अवैध हैं। सभी integer मान network byte order (big endian) में संग्रहीत किए जाते हैं।

डेटाबेस को एक सिंगल thread द्वारा खोले और एक्सेस किए जाने के लिए डिज़ाइन किया गया है। BlockfileNamingService synchronization प्रदान करती है।

### Superblock प्रारूप

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
### Skip list ब्लॉक पेज प्रारूप

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
### स्किप स्तर ब्लॉक पेज फॉर्मेट

सभी स्तरों का एक span होता है। सभी spans के स्तर नहीं होते।

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
### स्पैन ब्लॉक पेज प्रारूप छोड़ें

Key/value संरचनाएं प्रत्येक span के भीतर और सभी spans में key के आधार पर क्रमबद्ध होती हैं। Key/value संरचनाएं प्रत्येक span के भीतर key के आधार पर क्रमबद्ध होती हैं। पहले span के अलावा अन्य spans खाली नहीं हो सकते।

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
### Span Continuation block पृष्ठ प्रारूप

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
### Key/value संरचना प्रारूप

Key और value की लंबाई को pages में विभाजित नहीं किया जाना चाहिए, यानी सभी 4 bytes एक ही page पर होने चाहिए। यदि पर्याप्त स्थान नहीं है तो एक page के अंतिम 1-3 bytes अप्रयुक्त रह जाते हैं और लंबाई continuation page में offset 8 पर होगी। Key और value data को pages में विभाजित किया जा सकता है। अधिकतम key और value की लंबाई 65535 bytes है।

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
### फ्री लिस्ट ब्लॉक पेज प्रारूप

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
### फ्री पेज ब्लॉक प्रारूप

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
metaindex (page 2 पर स्थित) US-ASCII strings का 4-byte integers में mapping है। key skiplist का नाम है और value skiplist का page index है।

## ब्लॉकफाइल नेमिंग सर्विस टेबल्स

BlockfileNamingService द्वारा बनाई और उपयोग की जाने वाली तालिकाएं निम्नलिखित हैं। प्रति span में प्रविष्टियों की अधिकतम संख्या 16 है।

### Properties Skiplist

`%%__INFO__%%` मुख्य डेटाबेस skiplist है जिसमें String/Properties key/value entries हैं जिसमें केवल एक entry होती है:

**info** - एक Properties (UTF-8 String/String Map), जो एक [Mapping](/docs/specs/common-structures/#type-mapping) के रूप में serialized है:

- **version** - "4"
- **created** - Java long time (ms)
- **upgraded** - Java long time (ms) (database version 2 के रूप में)
- **lists** - होस्ट डेटाबेस की अल्पविराम-विभाजित सूची, जिसमें लुकअप के लिए क्रमानुसार खोजा जाना है। लगभग हमेशा "privatehosts.txt,userhosts.txt,hosts.txt"।
- **listversion_*** - lists में प्रत्येक डेटाबेस का संस्करण, उदाहरण के लिए: listversion_hosts.txt=4। व्यक्तिगत सूचियों के आंशिक या रद्द किए गए अपग्रेड की पहचान करने के लिए उपयोग किया जाता है। (database version 4 के रूप में)

### रिवर्स लुकअप स्किपलिस्ट

`%%__REVERSE__%%` रिवर्स लुकअप skiplist है जिसमें Integer/Properties key/value entries हैं (database version 2 के अनुसार):

- Skiplist keys 4-byte Integers हैं, [Destination](/docs/specs/common-structures/#struct-destination) के hash के पहले 4 bytes।
- Skiplist values प्रत्येक एक Properties (एक UTF-8 String/String Map) है जो [Mapping](/docs/specs/common-structures/#type-mapping) के रूप में serialized है
  - Properties में कई entries हो सकती हैं, प्रत्येक एक reverse mapping है, क्योंकि किसी दिए गए destination के लिए एक से अधिक hostname हो सकते हैं, या hash के समान पहले 4 bytes के साथ collisions हो सकते हैं।
  - प्रत्येक property key एक hostname है।
  - प्रत्येक property value empty string है।

### hosts.txt, userhosts.txt, और privatehosts.txt स्किपलिस्ट

प्रत्येक host database के लिए, उस database के hosts को शामिल करने वाली एक skiplist होती है। ध्यान दें कि version 4 format प्रति hostname कई Destinations का समर्थन करता है। यह format I2P release 0.9.26 में शुरू किया गया था। Version 3 databases स्वचालित रूप से version 4 में migrate हो जाते हैं।

इन skiplists में keys/values निम्नलिखित हैं:

**key** - एक UTF-8 स्ट्रिंग (होस्टनेम)

**value** - - Database version 4: एक DestEntry, जो एक एक-बाइट संख्या है Properties/Destination जोड़ों की जो आगे आने वाली हैं। उतनी संख्या में जोड़े: एक Properties (एक UTF-8 String/String Map) जो [Mapping](/docs/specs/common-structures/#type-mapping) के रूप में serialized है, जिसके बाद एक binary [Destination](/docs/specs/common-structures/#struct-destination) (सामान्य रूप से serialized) है। - Database version 3: एक DestEntry, जो एक Properties (एक UTF-8 String/String Map) है जो [Mapping](/docs/specs/common-structures/#type-mapping) के रूप में serialized है, जिसके बाद एक binary [Destination](/docs/specs/common-structures/#struct-destination) (सामान्य रूप से serialized) है।

DestEntry Properties में आमतौर पर शामिल होता है:

- **"a"** - जोड़ा गया समय (Java long time ms में)
- **"m"** - अंतिम बार संशोधित समय (Java long time ms में)
- **"notes"** - उपयोगकर्ता द्वारा प्रदान की गई टिप्पणियां
- **"s"** - एंट्री का मूल स्रोत (आमतौर पर एक फ़ाइल नाम या subscription URL)
- **"v"** - यदि एंट्री के signature की पुष्टि हुई है, "true" या "false"

Hostname keys को लोअर-केस में स्टोर किया जाता है और हमेशा ".i2p" से समाप्त होते हैं।

## संदर्भ

- [Destination](/docs/specs/common-structures/#struct-destination)
- [Mapping](/docs/specs/common-structures/#type-mapping)
- [METANOTION](http://www.metanotion.net/software/sandbox/block.html)
- [NAMING](/docs/overview/naming/)
