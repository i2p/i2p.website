---
title: "Blockfile विनिर्देश"
description: "होस्टनेम समाधान के लिए I2P द्वारा प्रयुक्त ऑन-डिस्क blockfile (ब्लॉक-आधारित फ़ाइल) स्टोरेज फ़ॉर्मेट"
slug: "blockfile"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## अवलोकन

यह दस्तावेज़ **I2P blockfile file format** (ब्लॉक-आधारित फ़ाइल फ़ॉर्मेट) और **Blockfile Naming Service** द्वारा उपयोग किए जाने वाले `hostsdb.blockfile` में मौजूद तालिकाओं को निर्दिष्ट करता है।   पृष्ठभूमि के लिए, देखें [I2P नामकरण और पता पुस्तिका](/docs/overview/naming)।

blockfile (I2P में एक फ़ाइल फ़ॉर्मेट) संक्षिप्त बाइनरी प्रारूप में **तेज़ डेस्टिनेशन लुकअप्स** संभव बनाता है।   पुराने `hosts.txt` सिस्टम की तुलना में:

- गंतव्य बाइनरी में संग्रहीत होते हैं, Base64 में नहीं।  
- मनमाना मेटाडेटा (जैसे, जोड़े जाने की तिथि, स्रोत, टिप्पणियाँ) संलग्न किया जा सकता है।  
- लुकअप का समय लगभग **10× तेज़** होता है।  
- डिस्क उपयोग में मामूली वृद्धि होती है।

एक blockfile डिस्क-आधारित क्रमबद्ध मैप्स (कुंजी-मूल्य युग्म) का संग्रह है, जिसे **skiplists** (स्किपलिस्ट, परतदार क्रमित-सूची-आधारित डेटा-स्ट्रक्चर) के रूप में कार्यान्वित किया गया है। यह [Metanotion Blockfile Database](http://www.metanotion.net/software/sandbox/block.html) से व्युत्पन्न है। यह विनिर्देश पहले फ़ाइल संरचना को परिभाषित करता है, फिर बताता है कि `BlockfileNamingService` द्वारा इसका उपयोग कैसे किया जाता है।

> Blockfile Naming Service (नाम सेवा) ने **I2P 0.8.8** में पुराने `hosts.txt` कार्यान्वयन को प्रतिस्थापित किया।   > आरंभ होने पर, यह `privatehosts.txt`, `userhosts.txt`, और `hosts.txt` से प्रविष्टियाँ आयात करता है

---

## ब्लॉकफ़ाइल प्रारूप

यह प्रारूप **1024-बाइट पेजों** से बना है, अखंडता सुनिश्चित करने के लिए प्रत्येक के प्रारंभ में एक **magic number** (पहचान हेतु विशिष्ट मान) होता है।   पेजों की क्रम संख्या 1 से शुरू होती है:

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
सभी पूर्णांक **नेटवर्क बाइट क्रम (big-endian)** का उपयोग करते हैं।   2-बाइट मान unsigned (बिना चिह्न) होते हैं; 4-बाइट मान (पृष्ठ संख्याएँ) signed (चिह्नित) होते हैं और धनात्मक होने चाहिए।

> **Threading (थ्रेड प्रबंधन):** डेटाबेस को **एकल-थ्रेड अभिगम** के लिए डिज़ाइन किया गया है; `BlockfileNamingService` समकालिकरण प्रदान करता है।

---

### सुपरब्लॉक प्रारूप

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

### Skip List (स्किप लिस्ट) ब्लॉक पृष्ठ प्रारूप

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

### स्किप लेवल ब्लॉक पेज फ़ॉर्मेट

हर स्तर में एक स्पैन होता है, लेकिन सभी स्पैन में स्तर नहीं होते।

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

### स्किप स्पैन ब्लॉक पृष्ठ प्रारूप

Key/value युग्म सभी स्पैनों में key के अनुसार क्रमबद्ध किए जाते हैं। पहले के अलावा अन्य स्पैन खाली नहीं होने चाहिए।

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

### Span Continuation Block (स्पैन कंटिन्यूएशन ब्लॉक) का पृष्ठ प्रारूप

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

### कुंजी/मान संरचना प्रारूप

कुंजी और मान के **लंबाई फ़ील्ड पृष्ठों में नहीं फैल सकते** (सभी 4 बाइट एक ही पृष्ठ में फिट होने चाहिए)।   यदि पर्याप्त स्थान शेष नहीं है, तो अधिकतम 3 बाइट तक पैड करें और अगले पृष्ठ के ऑफ़सेट 8 से जारी रखें।

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

### मुक्त सूची ब्लॉक पृष्ठ प्रारूप

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

### खाली पृष्ठ ब्लॉक प्रारूप

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

### मेटा अनुक्रमणिका

पृष्ठ 2 पर स्थित।   **US-ASCII strings (US-ASCII अक्षर-शृंखलाएँ)** → **4-बाइट पूर्णांक** को मैप करता है।   कुंजी skiplist (स्किपलिस्ट) का नाम है; मान पृष्ठ सूचकांक है।

---

## ब्लॉकफ़ाइल नामकरण सेवा की तालिकाएँ

सेवा कई skiplists (skip list नामक डेटा संरचना) परिभाषित करती है। प्रत्येक स्पैन अधिकतम 16 प्रविष्टियों का समर्थन करता है।

---

### प्रॉपर्टीज़ Skiplist (परतों वाली सूची डेटा संरचना)

`%%__INFO__%%` में एक प्रविष्टि शामिल है:

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
सामान्य फ़ील्ड्स:

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

### रिवर्स लुकअप Skiplist (बहु-स्तरीय लिंक्ड-लिस्ट आधारित तेज़ खोज डेटा संरचना)

`%%__REVERSE__%%` में **Integer → Properties** प्रविष्टियाँ होती हैं (DB v2 से)।

- **कुंजी:** Destination (I2P में गंतव्य पहचान) के SHA-256 हैश के पहले 4 बाइट्स।  
- **मान:** Properties ऑब्जेक्ट (सीरियलाइज़्ड मैपिंग)।  
- कई प्रविष्टियाँ टकरावों और मल्टी-होस्टनेम Destinations को संभालती हैं।  
- प्रत्येक प्रॉपर्टी कुंजी = होस्टनेम; मान = खाली स्ट्रिंग.

---

### होस्ट डेटाबेस Skiplists (तेज़ खोज हेतु बहु-स्तरीय लिंक्ड-लिस्ट डेटा संरचना)

`hosts.txt`, `userhosts.txt`, और `privatehosts.txt` में से प्रत्येक होस्टनेम्स → डेस्टिनेशन्स (I2P पते) की मैपिंग करता है।

संस्करण 4 प्रति होस्टनेम एक से अधिक Destinations (I2P में गंतव्य/पहचान) का समर्थन करता है (जिसकी शुरुआत **I2P 0.9.26** में हुई थी)।   संस्करण 3 के डेटाबेस स्वतः माइग्रेट हो जाते हैं।

#### कुंजी

UTF-8 स्ट्रिंग (होस्टनेम, छोटे अक्षरों में, `.i2p` पर समाप्त)

#### मान

- **संस्करण 4:**  
  - 1 बाइट में गुण/गंतव्य युग्मों की संख्या  
  - प्रत्येक युग्म के लिए: गुण → गंतव्य (बाइनरी)
- **संस्करण 3:**  
  - गुण → गंतव्य (बाइनरी)

#### DestEntry गुण

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

## कार्यान्वयन संबंधी टिप्पणियाँ

`BlockfileNamingService` Java क्लास इस विनिर्देश को कार्यान्वित करती है।

- router संदर्भ के बाहर, डेटाबेस **केवल-पढ़ने** मोड में खुलता है जब तक `i2p.naming.blockfile.writeInAppContext=true` न हो।  
- मल्टी‑इंस्टेंस या मल्टी‑JVM (Java Virtual Machine—जावा वर्चुअल मशीन) एक्सेस के लिए अभिप्रेत नहीं है।  
- तीन प्राथमिक मैप (`privatehosts`, `userhosts`, `hosts`) और तेज़ लुकअप के लिए एक रिवर्स मैप बनाए रखता है।

---

## संदर्भ

- [I2P नामकरण और पता पुस्तिका दस्तावेज़](/docs/overview/naming/)  
- [सामान्य संरचनाओं का विनिर्देश](/docs/specs/common-structures/)  
- [Metanotion ब्लॉकफ़ाइल डेटाबेस](http://www.metanotion.net/software/sandbox/block.html)  
- [BlockfileNamingService JavaDoc](https://geti2p.net/javadoc/i2p/naming/BlockfileNamingService.html)
