---
title: "सॉफ़्टवेयर अपडेट विनिर्देश"
description: "I2P सॉफ्टवेयर अपडेट तंत्र, SU3 फ़ाइल प्रारूप, और समाचार फीड के लिए विनिर्देश"
slug: "updates"
aliases:
  - "/hi/updates"
  - "/hi/updates/"
category: "डिज़ाइन"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## अवलोकन

I2P स्वचालित सॉफ़्टवेयर अपडेट के लिए एक सरल, लेकिन सुरक्षित, सिस्टम का उपयोग करता है। router console समय-समय पर एक कॉन्फ़िगर करने योग्य I2P URL से एक न्यूज़ फ़ाइल खींचता है। डिफ़ॉल्ट प्रोजेक्ट न्यूज़ होस्ट के बंद होने की स्थिति में, प्रोजेक्ट वेबसाइट की ओर इशारा करने वाला एक हार्डकोडेड बैकअप URL है।

न्यूज़ फ़ाइल की सामग्री router console के होम पेज पर प्रदर्शित की जाती है। इसके अतिरिक्त, न्यूज़ फ़ाइल में सॉफ़्टवेयर का सबसे नवीनतम संस्करण नंबर होता है। यदि यह संस्करण router के संस्करण नंबर से अधिक है, तो यह उपयोगकर्ता को यह संकेत दिखाएगा कि एक अपडेट उपलब्ध है।

यदि router ऐसा करने के लिए कॉन्फ़िगर किया गया है तो वह वैकल्पिक रूप से नया version डाउनलोड कर सकता है, या डाउनलोड करके इंस्टॉल कर सकता है।

## पुरानी समाचार फ़ाइल विशिष्टता

यह प्रारूप रिलीज़ 0.9.17 के अनुसार su3 news प्रारूप द्वारा बदल दिया गया है।

news.xml फ़ाइल में निम्नलिखित तत्व हो सकते हैं:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
i2p.release एंट्री में पैरामीटर निम्नलिखित हैं। सभी keys केस-असंवेदनशील हैं। सभी values को डबल कोट्स में संलग्न होना चाहिए।

**date** : router संस्करण की रिलीज़ दिनांक। अप्रयुक्त। प्रारूप निर्दिष्ट नहीं।

**minJavaVersion** : वर्तमान संस्करण को चलाने के लिए आवश्यक Java का न्यूनतम संस्करण। रिलीज 0.9.9 के अनुसार।

**minVersion** : वर्तमान संस्करण में अपडेट करने के लिए आवश्यक router का न्यूनतम संस्करण। यदि कोई router इससे पुराना है, तो उपयोगकर्ता को पहले किसी मध्यवर्ती संस्करण में (मैन्युअल रूप से?) अपडेट करना होगा। रिलीज़ 0.9.9 के अनुसार।

**su3Clearnet** : एक या अधिक HTTP URLs जहाँ .su3 अपडेट फाइल clearnet (गैर-I2P) पर मिल सकती है। कई URLs को स्पेस या कॉमा से अलग किया जाना चाहिए। रिलीज 0.9.9 के अनुसार।

**su3SSL** : एक या अधिक HTTPS URLs जहाँ .su3 update file clearnet (non-I2P) पर मिल सकती है। कई URLs को स्पेस या कॉमा से अलग किया जाना चाहिए। रिलीज़ 0.9.9 के अनुसार।

**sudTorrent** : अपडेट के .sud (non-pack200) torrent के लिए magnet link। रिलीज़ 0.9.4 के अनुसार।

**su2Torrent** : अपडेट के .su2 (pack200) torrent के लिए magnet link। रिलीज़ 0.9.4 से।

**su3Torrent** : अपडेट के .su3 (नया प्रारूप) torrent के लिए magnet link। रिलीज़ 0.9.9 के अनुसार।

**version** : आवश्यक। उपलब्ध नवीनतम वर्तमान router संस्करण।

ब्राउज़र द्वारा व्याख्या को रोकने के लिए elements को XML comments के अंदर शामिल किया जा सकता है। i2p.release element और version आवश्यक हैं। अन्य सभी वैकल्पिक हैं। नोट: parser की सीमाओं के कारण पूरे element को एक ही लाइन पर होना चाहिए।

## अपडेट फ़ाइल विनिर्देश

रिलीज़ 0.9.9 के बाद से, हस्ताक्षरित अपडेट फ़ाइल, जिसका नाम i2pupdate.su3 है, नीचे निर्दिष्ट "su3" फ़ाइल फॉर्मेट का उपयोग करेगी। स्वीकृत रिलीज़ हस्ताक्षरकर्ता 4096-bit RSA keys का उपयोग करेंगे। इन हस्ताक्षरकर्ताओं के लिए X.509 पब्लिक key सर्टिफिकेट router इंस्टॉलेशन पैकेज में वितरित किए जाते हैं। अपडेट में नए, स्वीकृत हस्ताक्षरकर्ताओं के लिए सर्टिफिकेट हो सकते हैं, और/या निरसन के लिए हटाए जाने वाले सर्टिफिकेट की सूची हो सकती है।

## पुराना अपडेट फ़ाइल विनिर्देश

यह प्रारूप रिलीज़ 0.9.9 के बाद से अप्रचलित है।

हस्ताक्षरित अपडेट फ़ाइल, पारंपरिक रूप से i2pupdate.sud नाम से जानी जाती है, यह केवल एक zip फ़ाइल है जिसमें 56 बाइट का header पहले से जोड़ा गया है। header में निम्नलिखित होता है:

- एक 40-byte DSA [Signature](/docs/specs/common-structures#signature)
- UTF-8 में एक 16-byte I2P version, आवश्यकता के अनुसार trailing zeroes के साथ padded

हस्ताक्षर केवल zip archive को कवर करता है - prepended version को नहीं। हस्ताक्षर router में कॉन्फ़िगर किए गए DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) में से किसी एक से मेल खाना चाहिए, जिसमें वर्तमान प्रोजेक्ट release managers की keys की एक hardcoded default list होती है।

संस्करण तुलना के उद्देश्यों के लिए, संस्करण फ़ील्ड में [0-9]* होते हैं, फ़ील्ड विभाजक '-', '_', और '.' हैं, और अन्य सभी वर्णों को नज़रअंदाज़ किया जाता है।

संस्करण 0.8.8 के अनुसार, संस्करण को UTF-8 में zip file comment के रूप में भी निर्दिष्ट करना होगा, बिना trailing zeroes के। अपडेट करने वाला router यह सत्यापित करता है कि header में संस्करण (जो signature द्वारा कवर नहीं है) zip file comment में संस्करण से मेल खाता है, जो signature द्वारा कवर है। यह header में संस्करण संख्या की spoofing को रोकता है।

## डाउनलोड और इंस्टॉलेशन

router पहले एक कॉन्फ़िगर योग्य I2P URLs की सूची में से किसी एक से अपडेट फ़ाइल का header डाउनलोड करता है, built-in HTTP client और proxy का उपयोग करके, और जांचता है कि version नया है। यह उन अपडेट hosts की समस्या को रोकता है जिनके पास नवीनतम फ़ाइल नहीं है। router फिर पूरी अपडेट फ़ाइल डाउनलोड करता है। router इंस्टॉलेशन से पहले यह सत्यापित करता है कि अपडेट फ़ाइल का version नया है। यह निश्चित रूप से signature को भी सत्यापित करता है, और यह सत्यापित करता है कि zip फ़ाइल comment header version से मेल खाता है, जैसा कि ऊपर बताया गया है।

zip फ़ाइल को extract किया जाता है और I2P configuration directory (~/.i2p on Linux) में "i2pupdate.zip" के रूप में copy किया जाता है।

रिलीज़ 0.7.12 से, router Pack200 डीकंप्रेशन को सपोर्ट करता है। zip archive के अंदर .jar.pack या .war.pack suffix वाली फाइलें transparently .jar या .war फाइल में decompress हो जाती हैं। .pack फाइलों वाली अपडेट फाइलों को पारंपरिक रूप से '.su2' suffix के साथ नाम दिया जाता है। Pack200 अपडेट फाइलों को लगभग 60% तक छोटा कर देता है।

रिलीज़ 0.8.7 के अनुसार, router libjbigi.so और libjcpuid.so फाइलों को डिलीट कर देगा यदि zip archive में lib/jbigi.jar फाइल मौजूद है, ताकि नई फाइलें jbigi.jar से extract हो सकें।

रिलीज़ 0.8.12 के अनुसार, यदि zip archive में deletelist.txt फ़ाइल है, तो router उसमें सूचीबद्ध फ़ाइलों को डिलीट कर देगा। फॉर्मेट है:

- प्रति लाइन एक फ़ाइल नाम
- सभी फ़ाइल नाम installation directory के सापेक्ष हैं; कोई absolute फ़ाइल नाम की अनुमति नहीं है, ".." से शुरू होने वाली कोई फ़ाइलें नहीं
- टिप्पणियां '#' से शुरू होती हैं

router तब deletelist.txt फ़ाइल को हटा देगा।

## SU3 फ़ाइल विनिर्देश

यह स्पेसिफिकेशन रिलीज़ 0.9.9 से router अपडेट के लिए, रिलीज़ 0.9.14 से reseed डेटा के लिए, रिलीज़ 0.9.15 से plugins के लिए, और रिलीज़ 0.9.17 से न्यूज़ फ़ाइल के लिए उपयोग किया जाता है।

### पिछले .sud/.su2 प्रारूप के साथ समस्याएं

- कोई magic number या flags नहीं
- compression, pack200 या नहीं, या signing algo निर्दिष्ट करने का कोई तरीका नहीं
- Version signature द्वारा कवर नहीं किया गया है, इसलिए इसे zip file comment में (router files के लिए) या plugin.config file में (plugins के लिए) होना आवश्यक है
- Signer निर्दिष्ट नहीं है इसलिए verifier को सभी ज्ञात keys को try करना होगा
- Signature-before-data format के लिए file generate करने के लिए दो passes की आवश्यकता होती है

### लक्ष्य

- उपरोक्त समस्याओं को ठीक करें
- अधिक सुरक्षित signature algorithm में माइग्रेट करें
- मौजूदा version checkers के साथ संगतता के लिए version info को समान format और offset में रखें
- One-pass signature verification और file extraction

### विनिर्देश

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
भविष्य के संस्करणों के साथ संगतता के लिए सभी अप्रयुक्त फ़ील्ड को 0 पर सेट किया जाना चाहिए।

### हस्ताक्षर विवरण

हस्ताक्षर बाइट 0 से शुरू होने वाले पूरे हेडर को कवर करता है, कंटेंट के अंत तक। हम raw signatures का उपयोग करते हैं। डेटा का हैश लें (बाइट्स 8-9 पर signature type द्वारा निहित hash type का उपयोग करके) और उसे "raw" sign या verify function में पास करें (जैसे Java में "NONEwithRSA")।

जबकि signature verification और content extraction को एक ही pass में implement किया जा सकता है, एक implementation को verify करना शुरू करने से पहले hash type निर्धारित करने के लिए पहले 10 bytes को read और buffer करना चाहिए।

विभिन्न signature प्रकारों के लिए signature की लंबाई [Signature](/docs/specs/common-structures#signature) specification में दी गई है। यदि आवश्यक हो तो signature को leading zeros के साथ pad करें। विभिन्न signature प्रकारों के parameters के लिए [cryptography details page](/docs/specs/cryptography#sig) देखें।

### नोट्स

कंटेंट टाइप ट्रस्ट डोमेन (विश्वास क्षेत्र) को निर्दिष्ट करता है। प्रत्येक कंटेंट टाइप के लिए, क्लाइंट्स उन पार्टियों के लिए X.509 पब्लिक की सर्टिफिकेट्स का एक सेट बनाए रखते हैं जिन पर उस कंटेंट पर हस्ताक्षर करने के लिए भरोसा किया जाता है। केवल निर्दिष्ट कंटेंट टाइप के लिए सर्टिफिकेट्स का उपयोग किया जा सकता है। सर्टिफिकेट को हस्ताक्षरकर्ता की ID द्वारा खोजा जाता है। क्लाइंट्स को यह सत्यापित करना होगा कि कंटेंट टाइप वह है जो एप्लिकेशन के लिए अपेक्षित है।

सभी मान नेटवर्क बाइट ऑर्डर (big endian) में हैं।

Java "NONEwithRSA" के साथ संगत Raw RSA signatures के python implementation के लिए, [इस Stack Overflow लेख](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530) को देखें।

## SU3 Router Update File Specification

### SU3 विवरण

- SU3 Content Type: 1 (ROUTER UPDATE)
- SU3 File Type: 0 (ZIP)
- SU3 Version: router संस्करण

zip में jar और war फाइलें अब pack200 के साथ संपीड़ित नहीं हैं जैसा कि ऊपर "su2" फाइलों के लिए दस्तावेजीकरण किया गया है, क्योंकि हाल के Java runtimes अब इसका समर्थन नहीं करते हैं।

### नोट्स

- रिलीज़ के लिए, SU3 संस्करण "बेस" router संस्करण है, जैसे "0.9.20"।
- डेवलपमेंट बिल्ड के लिए, जो रिलीज़ 0.9.20 से समर्थित हैं, SU3 संस्करण "पूर्ण" router संस्करण है, जैसे "0.9.20-5" या "0.9.20-5-rc"। [I2P source](https://github.com/i2p/i2p.i2p) में RouterVersion.java देखें।

## SU3 Reseed File विनिर्देश

0.9.14 के अनुसार, reseed डेटा "su3" फ़ाइल प्रारूप में वितरित किया जाता है।

### लक्ष्य

- मजबूत हस्ताक्षर और विश्वसनीय प्रमाणपत्रों के साथ हस्ताक्षरित फाइलें जो man-in-the-middle हमलों को रोकने के लिए जो पीड़ितों को एक अलग, अविश्वसनीय नेटवर्क में boot कर सकते हैं।
- su3 फाइल प्रारूप का उपयोग करें जो पहले से ही अपडेट और plugins के लिए उपयोग किया जाता है
- reseeding को तेज़ करने के लिए एक संपीड़ित फाइल, क्योंकि 200 फाइलें fetch करना धीमा था

### विनिर्देश

1. फ़ाइल का नाम "i2pseeds.su3" होना चाहिए। 0.9.42 के अनुसार, अनुरोधकर्ता को request URL में query string "?netid=2" जोड़नी चाहिए, मौजूदा network ID 2 को मानते हुए। इसका उपयोग cross-network connections को रोकने के लिए किया जा सकता है। Test networks में एक अलग network ID सेट करना चाहिए। विवरण के लिए proposal 147 देखें।
2. फ़ाइल web server पर router infos के समान directory में होनी चाहिए।
3. एक router पहले (index URL)/i2pseeds.su3 fetch करने की कोशिश करेगा; यदि वह असफल हो जाता है तो यह index URL को fetch करेगा और फिर links में मिली व्यक्तिगत router info files को fetch करेगा।

### SU3 विवरण

- SU3 Content Type: 3 (RESEED)
- SU3 File Type: 0 (ZIP)
- SU3 Version: युग के बाद से सेकंड, ASCII में (date +%s)। 2038 या 2106 में रोल ओवर नहीं होता।
- zip फाइल में router info फाइलें "शीर्ष स्तर" पर होनी चाहिए। zip फाइल में कोई डायरेक्टरी नहीं हैं।
- Router info फाइलों का नाम "routerInfo-(44 character base 64 router hash).dat" होना चाहिए, जैसा कि पुराने reseed तंत्र में था। I2P base 64 वर्णमाला का उपयोग किया जाना चाहिए।

### नोट्स

- चेतावनी: कई reseed IPv6 के माध्यम से अनुत्तरदायी होने के लिए जाने जाते हैं। IPv4 को बाध्यकारी या प्राथमिकता देने की सिफारिश की जाती है।
- चेतावनी: कुछ reseed स्व-हस्ताक्षरित CA प्रमाणपत्र का उपयोग करते हैं। Implementation को reseed करते समय या तो इन CA को import करना और उन पर भरोसा करना चाहिए, या reseed सूची से स्व-हस्ताक्षरित reseed को हटा देना चाहिए।
- Reseed signer keys को RSA-4096 keys (signature type 6) के साथ स्व-हस्ताक्षरित X.509 प्रमाणपत्र के रूप में implementation में वितरित किया जाता है। Implementation को प्रमाणपत्रों में वैध तारीखों को लागू करना चाहिए।

## SU3 प्लगइन फ़ाइल विशिष्टता

0.9.15 के बाद से, plugins को "su3" फ़ाइल फॉर्मेट में पैकेज किया जा सकता है।

### SU3 विवरण

- SU3 Content Type: 2 (PLUGIN)
- SU3 File Type: 0 (ZIP) - विवरण के लिए [plugin specification](/docs/specs/plugin) देखें।
- SU3 Version: plugin संस्करण, जो plugin.config में दिए गए से मेल खाना चाहिए।

Zip में jar और war फाइलों को pack200 के साथ compress नहीं किया जाना चाहिए जैसा कि ऊपर "su2" फाइलों के लिए documented है, क्योंकि recent Java runtimes अब इसे support नहीं करते हैं।

## SU3 News File विनिर्देश

0.9.17 से, समाचार "su3" फ़ाइल प्रारूप में वितरित किया जाता है।

### लक्ष्य

- मजबूत signatures और विश्वसनीय certificates के साथ signed news
- अपडेट, reseeding, और plugins के लिए पहले से उपयोग में आने वाले su3 file format का उपयोग
- standard parsers के साथ उपयोग के लिए मानक XML format
- standard feed readers और generators के साथ उपयोग के लिए मानक Atom format
- console पर प्रदर्शित करने से पहले HTML की sanitization और verification
- Android और HTML console के बिना अन्य platforms पर आसान implementation के लिए उपयुक्त

### SU3 विवरण

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) या 3 (XML.GZ)
- SU3 Version: युग से सेकंड, ASCII में (date +%s)। 2038 या 2106 में रोल ओवर नहीं होता।
- File Format: XML या gzipped XML, जिसमें [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed होता है। Charset UTF-8 होना चाहिए।

### Atom Feed विवरण

निम्नलिखित `<feed>` elements का उपयोग किया जाता है:

**`<entry>`** : एक समाचार आइटम। नीचे देखें।

**`<i2p:release>`** : I2P अपडेट मेटाडेटा। नीचे देखें।

**`<i2p:revocations>`** : प्रमाणपत्र निरस्तीकरण। नीचे देखें।

**`<i2p:blocklist>`** : ब्लॉकलिस्ट डेटा। नीचे देखें।

**`<updated>`** : आवश्यक। फ़ीड के लिए टाइमस्टैम्प ([RFC 4287](https://tools.ietf.org/html/rfc4287) धारा 3.3 और [RFC 3339](https://tools.ietf.org/html/rfc3339) के अनुसार)।

### Atom एंट्री विवरण

समाचार फ़ीड में प्रत्येक Atom `<entry>` को router console में पार्स और प्रदर्शित किया जा सकता है। निम्नलिखित तत्वों का उपयोग किया जाता है:

**`<author>`** : वैकल्पिक। इसमें `<name>` होता है - प्रविष्टि लेखक का नाम।

**`<content>`** : आवश्यक। Content, type="xhtml" होना चाहिए। XHTML को अनुमतित elements की whitelist और अनुमतित नहीं attributes की blacklist के साथ sanitize किया जाएगा। Clients किसी element को, या enclosing entry को, या पूरे feed को ignore कर सकते हैं जब कोई non-whitelisted element मिले।

**`<link>`** : वैकल्पिक। अधिक जानकारी के लिए लिंक।

**`<summary>`** : वैकल्पिक। छोटा सारांश, टूलटिप के लिए उपयुक्त।

**`<title>`** : आवश्यक। समाचार प्रविष्टि का शीर्षक।

**`<updated>`** : आवश्यक। इस प्रविष्टि के लिए टाइमस्टैम्प ([RFC 4287](https://tools.ietf.org/html/rfc4287) धारा 3.3 और [RFC 3339](https://tools.ietf.org/html/rfc3339) के अनुरूप)।

### Atom i2p:release विवरण

फीड में कम से कम एक `<i2p:release>` entity होनी चाहिए। प्रत्येक में निम्नलिखित attributes और entities होती हैं:

**date (attribute)** : आवश्यक। इस प्रविष्टि के लिए टाइमस्टैम्प ([RFC 4287](https://tools.ietf.org/html/rfc4287) खंड 3.3 और [RFC 3339](https://tools.ietf.org/html/rfc3339) के अनुरूप)। तारीख yyyy-mm-dd के संक्षिप्त प्रारूप में भी हो सकती है ('T' के बिना); यह RFC 3339 में "full-date" प्रारूप है। इस प्रारूप में किसी भी प्रसंस्करण के लिए समय को 00:00:00 UTC माना जाता है।

**minJavaVersion (attribute)** : यदि मौजूद है, तो वर्तमान संस्करण चलाने के लिए आवश्यक Java का न्यूनतम संस्करण।

**minVersion (attribute)** : यदि उपस्थित है, तो वर्तमान संस्करण में अपडेट करने के लिए आवश्यक router का न्यूनतम संस्करण। यदि कोई router इससे पुराना है, तो उपयोगकर्ता को पहले किसी मध्यवर्ती संस्करण में अपडेट करना होगा (मैन्युअल रूप से?)।

**`<i2p:version>`** : आवश्यक। उपलब्ध नवीनतम वर्तमान router संस्करण।

**`<i2p:update>`** : एक अपडेट फ़ाइल (एक या अधिक)। इसमें कम से कम एक child होना चाहिए।   - type (attribute): "sud", "su2", या "su3"। सभी `<i2p:update>` elements में अद्वितीय होना चाहिए।   - `<i2p:clearnet>`: नेटवर्क के बाहर प्रत्यक्ष डाउनलोड लिंक (शून्य या अधिक)। href (attribute): एक मानक clearnet http लिंक।   - `<i2p:clearnetssl>`: नेटवर्क के बाहर प्रत्यक्ष डाउनलोड लिंक (शून्य या अधिक)। href (attribute): एक मानक clearnet https लिंक।   - `<i2p:torrent>`: नेटवर्क के भीतर magnet लिंक। href (attribute): एक magnet लिंक।   - `<i2p:url>`: नेटवर्क के भीतर प्रत्यक्ष डाउनलोड लिंक (शून्य या अधिक)। href (attribute): एक नेटवर्क के भीतर http .i2p लिंक।

### Atom i2p:revocations विवरण

यह entity वैकल्पिक है और feed में अधिकतम एक `<i2p:revocations>` entity होती है। यह सुविधा release 0.9.26 से समर्थित है।

`<i2p:revocations>` entity में एक या अधिक `<i2p:crl>` entities होती हैं। `<i2p:crl>` entity में निम्नलिखित attributes होते हैं:

**updated (attribute)** : आवश्यक। इस entry के लिए timestamp ([RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 और [RFC 3339](https://tools.ietf.org/html/rfc3339) के अनुसार)। दिनांक truncated format yyyy-mm-dd में भी हो सकता है ('T' के बिना); यह RFC 3339 में "full-date" format है। इस format में किसी भी processing के लिए समय को 00:00:00 UTC माना जाता है।

**id (attribute)** : आवश्यक। इस CRL के निर्माता के लिए एक अद्वितीय id।

**(entity content)** : आवश्यक। एक मानक base 64 encoded Certificate Revocation List (CRL) newlines के साथ, जो '-----BEGIN X509 CRL-----' लाइन से शुरू होकर '-----END X509 CRL-----' लाइन पर समाप्त होती है। CRLs के बारे में अधिक जानकारी के लिए [RFC 5280](https://tools.ietf.org/html/rfc5280) देखें।

### Atom i2p:blocklist विवरण

यह entity वैकल्पिक है और feed में अधिकतम एक `<i2p:blocklist>` entity होती है। इस feature को release 0.9.28 में implement करने की योजना है।

`<i2p:blocklist>` entity में एक या अधिक `<i2p:block>` या `<i2p:unblock>` entities, एक "updated" entity, और "signer" तथा "sig" attributes होते हैं:

**signer (attribute)** : आवश्यक। इस blocklist पर हस्ताक्षर करने के लिए उपयोग की जाने वाली public key के लिए एक अद्वितीय id (UTF-8)।

**sig (attribute)** : आवश्यक। format code:b64sig में एक signature, जहाँ code ASCII signature type number है, और b64sig base 64 encoded signature है (I2P alphabet)। sign किए जाने वाले data की specification के लिए नीचे देखें।

**`<updated>`** : आवश्यक। blocklist के लिए timestamp ([RFC 4287](https://tools.ietf.org/html/rfc4287) section 3.3 और [RFC 3339](https://tools.ietf.org/html/rfc3339) के अनुरूप)। दिनांक छोटे प्रारूप yyyy-mm-dd में भी हो सकता है ('T' के बिना); यह RFC 3339 में "full-date" प्रारूप है। इस प्रारूप में किसी भी प्रसंस्करण के लिए समय 00:00:00 UTC माना जाता है।

**`<i2p:block>`** : वैकल्पिक, कई entities की अनुमति है। एक single entry, या तो literal IPv4 या IPv6 address, या 44-character base 64 router hash (I2P alphabet)। IPv6 addresses संक्षिप्त प्रारूप में हो सकते हैं (जिनमें "::" होता है)। netmask के साथ entries के लिए समर्थन, जैसे x.y.0.0/16, वैकल्पिक है। host names के लिए समर्थन वैकल्पिक है।

**`<i2p:unblock>`** : वैकल्पिक, कई entities की अनुमति है। `<i2p:block>` के समान format।

**हस्ताक्षर विनिर्देश:** हस्ताक्षरित या सत्यापित किए जाने वाले डेटा को उत्पन्न करने के लिए, निम्नलिखित डेटा को ASCII एन्कोडिंग में जोड़ें: अपडेट किया गया स्ट्रिंग जिसके बाद एक newline (ASCII 0x0a) हो, फिर प्रत्येक block entry को प्राप्त क्रम में प्रत्येक के बाद एक newline के साथ, फिर प्रत्येक unblock entry को प्राप्त क्रम में प्रत्येक के बाद एक newline के साथ।

## ब्लॉकलिस्ट फ़ाइल विनिर्देश

TBD, अनिम्प्लिमेंटेड, प्रस्ताव 130 देखें। ब्लॉकलिस्ट अपडेट news फ़ाइल में वितरित किए जाते हैं, ऊपर देखें।

## भविष्य का कार्य

- Router अपडेट तंत्र वेब router console का हिस्सा है। वर्तमान में router console की कमी वाले embedded router के अपडेट के लिए कोई प्रावधान नहीं है।

## संदर्भ

- **[CRYPTO-SIG]** [Cryptography - Signatures](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P Source Code](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Plugin Specification](/docs/specs/plugin)
- **[Python]** [Python RSA Raw Signatures](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - दिनांक और समय](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom Syndication Format](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Certificate Revocation Lists](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Signature Type](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [SigningPublicKey Type](/docs/specs/common-structures#signingpublickey)
