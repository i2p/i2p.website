---
title: "सॉफ़्टवेयर अद्यतन विनिर्देश"
description: "I2P routers के लिए सुरक्षित हस्ताक्षरित अपडेट तंत्र और फ़ीड संरचना"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

Routers I2P network के माध्यम से वितरित एक हस्ताक्षरित समाचार फ़ीड को polling (नियमित अंतराल पर पूछताछ) करके स्वतः अपडेट की जाँच करते हैं। जब कोई नया संस्करण घोषित किया जाता है, तो router क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित अपडेट आर्काइव (`.su3`) डाउनलोड करता है और उसे इंस्टॉलेशन के लिए तैयार करता है।   यह प्रणाली आधिकारिक रिलीज़ों के **प्रमाणित, छेड़छाड़-प्रतिरोधी**, और **मल्टी-चैनल** वितरण को सुनिश्चित करती है।

I2P 2.10.0 से, अपडेट प्रणाली निम्न का उपयोग करती है: - **RSA-4096 / SHA-512** हस्ताक्षर - **SU3 कंटेनर फ़ॉर्मेट** (पुराने SUD/SU2 को प्रतिस्थापित करता है) - **रेडंडेंट मिरर:** इन-नेटवर्क HTTP, क्लियरनेट HTTPS, और BitTorrent

---

## 1. समाचार फ़ीड

Routers नए संस्करणों और सुरक्षा परामर्शों का पता लगाने के लिए हर कुछ घंटों में हस्ताक्षरित Atom फ़ीड की जाँच करते हैं.   यह फ़ीड हस्ताक्षरित होती है और `.su3` फ़ाइल के रूप में वितरित की जाती है, जिसमें निम्न शामिल हो सकते हैं:

- `<i2p:version>` — नया संस्करण संख्या  
- `<i2p:minVersion>` — समर्थित न्यूनतम router संस्करण  
- `<i2p:minJavaVersion>` — आवश्यक न्यूनतम Java रनटाइम  
- `<i2p:update>` — कई डाउनलोड मिरर (I2P, HTTPS, torrent) सूचीबद्ध करता है  
- `<i2p:revocations>` — प्रमाणपत्र निरस्तीकरण डेटा  
- `<i2p:blocklist>` — समझौता किए गए समकक्षों के लिए नेटवर्क-स्तरीय ब्लॉकलिस्ट

### फ़ीड वितरण

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
router I2P फीड को प्राथमिकता देते हैं, लेकिन आवश्यकता पड़ने पर clearnet या torrent वितरण पर लौट सकते हैं।

---

## 2. फ़ाइल प्रारूप

### SU3 (वर्तमान मानक)

संस्करण 0.9.9 में पेश किए जाने पर, SU3 ने पुराने SUD और SU2 फ़ॉर्मैट्स को प्रतिस्थापित कर दिया।   प्रत्येक फ़ाइल में एक हेडर, पेलोड और ट्रेलिंग सिग्नेचर शामिल होता है।

**हेडर संरचना** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**हस्ताक्षर सत्यापन के चरण** 1. हेडर पार्स करें और हस्ताक्षर एल्गोरिथम की पहचान करें।   2. संग्रहीत हस्ताक्षरकर्ता प्रमाणपत्र का उपयोग करके हैश और हस्ताक्षर सत्यापित करें।   3. सुनिश्चित करें कि हस्ताक्षरकर्ता निरस्त नहीं है।   4. एम्बेडेड संस्करण स्ट्रिंग की तुलना पेलोड मेटाडेटा से करें।

Routers विश्वसनीय हस्ताक्षरकर्ता प्रमाणपत्रों के साथ आते हैं (वर्तमान में **zzz** और **str4d**), और किसी भी बिना हस्ताक्षरित या निरस्त स्रोतों को अस्वीकार करते हैं।

### SU2 (अप्रचलित)

- Pack200 (Java का एक संपीड़न फ़ॉर्मैट) से संपीड़ित JARs के साथ `.su2` एक्सटेंशन का उपयोग किया गया।  
- Java 14 में Pack200 (JEP 367) को अप्रचलित घोषित किए जाने के बाद इसे हटा दिया गया।  
- I2P 0.9.48+ में अक्षम; अब इसे पूरी तरह ZIP compression से प्रतिस्थापित किया गया है।

### SUD (पुराना)

- प्रारंभिक DSA-SHA1 (Digital Signature Algorithm + SHA-1 हैश) से हस्ताक्षरित ZIP फ़ॉर्मेट (pre-0.9.9).  
- signer ID या हेडर नहीं, अखंडता सीमित।  
- कमजोर क्रिप्टोग्राफी और संस्करण प्रवर्तन की कमी के कारण प्रतिस्थापित किया गया।

---

## 3. अद्यतन कार्यप्रवाह

### 3.1 हेडर सत्यापन

Routers केवल **SU3 header** प्राप्त करते हैं ताकि पूरी फ़ाइलें डाउनलोड करने से पहले संस्करण स्ट्रिंग का सत्यापन किया जा सके।   यह पुराने मिरर या पुराने संस्करणों पर बैंडविड्थ की बर्बादी को रोकता है।

### 3.2 पूर्ण डाउनलोड

हेडर का सत्यापन करने के बाद, router पूरी `.su3` फ़ाइल यहाँ से डाउनलोड करता है: - नेटवर्क के भीतर eepsite मिरर (पसंदीदा)   - HTTPS clearnet (सामान्य इंटरनेट) मिरर (फॉलबैक)   - BitTorrent (वैकल्पिक पीयर-सहायता प्राप्त वितरण)

डाउनलोड में मानक I2PTunnel HTTP क्लाइंट का उपयोग होता है, जिसमें पुनः प्रयास, समय-सीमा प्रबंधन, और mirror fallback (ज़रूरत पड़ने पर वैकल्पिक मिरर पर स्वचालित स्विच) शामिल हैं।

### 3.3 हस्ताक्षर सत्यापन

प्रत्येक डाउनलोड की गई फ़ाइल इन जाँचों से गुज़रती है: - **हस्ताक्षर जाँच:** RSA-4096/SHA512 सत्यापन   - **संस्करण मिलान:** हेडर बनाम पेलोड संस्करण जाँच   - **डाउनग्रेड रोकथाम:** सुनिश्चित करता है कि अपडेट स्थापित संस्करण से नया हो

अमान्य या मेल न खाने वाली फ़ाइलें तुरंत खारिज कर दी जाती हैं।

### 3.4 इंस्टॉलेशन स्टेजिंग

सत्यापन के बाद: 1. ZIP की सामग्री अस्थायी निर्देशिका में निकालें   2. `deletelist.txt` में सूचीबद्ध फ़ाइलें हटाएँ   3. यदि `lib/jbigi.jar` शामिल है तो नेटिव लाइब्रेरियों को प्रतिस्थापित करें   4. हस्ताक्षरकर्ता प्रमाणपत्रों को `~/.i2p/certificates/` में कॉपी करें   5. अगले पुनरारंभ पर लागू करने के लिए अपडेट को `i2pupdate.zip` में स्थानांतरित करें

अपडेट अगले स्टार्टअप पर अपने आप इंस्टॉल हो जाएगा, या जब “Install update now” को मैन्युअल रूप से ट्रिगर किया जाए।

---

## 4. फ़ाइल प्रबंधन

### deletelist.txt

नई सामग्री को अनपैक करने से पहले हटाई जाने वाली अप्रचलित फ़ाइलों की एक सादा पाठ सूची।

**नियम:** - प्रत्येक पंक्ति में एक पथ (केवल सापेक्ष पथ) - `#` से शुरू होने वाली पंक्तियाँ अनदेखी की जाएँगी - `..` और पूर्ण पथ अस्वीकृत किए जाएँगे

### नेटिव लाइब्रेरीज़

पुरानी या असंगत नेटिव बाइनरीज़ को रोकने के लिए: - यदि `lib/jbigi.jar` मौजूद है, तो पुरानी `.so` या `.dll` फ़ाइलें हटा दी जाती हैं   - सुनिश्चित करता है कि प्लेटफ़ॉर्म-विशिष्ट लाइब्रेरियाँ नए सिरे से निकाली जाती हैं

---

## 5. प्रमाणपत्र प्रबंधन

Routers अपडेट्स या समाचार फ़ीड में प्रकाशित रद्दीकरणों के माध्यम से **नए साइनर प्रमाणपत्र** प्राप्त कर सकते हैं।

- नई `.crt` फ़ाइलें प्रमाणपत्र निर्देशिका में कॉपी की जाती हैं।  
- भविष्य के सत्यापनों से पहले रद्द किए गए प्रमाणपत्र हटा दिए जाते हैं।  
- बिना किसी मैनुअल उपयोगकर्ता हस्तक्षेप की आवश्यकता के key rotation (कुंजियों को समय-समय पर बदलना) का समर्थन करता है।

सभी अपडेट ऑफलाइन **air-gapped signing systems** (इंटरनेट/नेटवर्क से पूरी तरह अलग हस्ताक्षर प्रणाली) का उपयोग करके साइन किए जाते हैं।   प्राइवेट कीज़ कभी भी बिल्ड सर्वरों पर संग्रहीत नहीं की जातीं।

---

## 6. डेवलपर दिशानिर्देश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
आगामी रिलीज़ में पोस्ट-क्वांटम हस्ताक्षर एकीकरण (देखें Proposal 169) और पुनरुत्पादन योग्य बिल্ড्स का अन्वेषण किया जाएगा।

---

## 7. सुरक्षा अवलोकन

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. संस्करणीकरण

- Router: **2.10.0 (API 0.9.67)**  
- सेमांटिक वर्शनिंग (अर्थ-आधारित संस्करण निर्धारण) `Major.Minor.Patch` के साथ।  
- न्यूनतम संस्करण प्रवर्तन असुरक्षित अपग्रेड को रोकता है।  
- समर्थित Java: **Java 8–17**। भविष्य में 2.11.0+ के लिए Java 17+ आवश्यक होगा।

---
