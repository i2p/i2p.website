---
title: "परिवहन परत"
description: "I2P की परिवहन परत को समझना - routers के बीच बिंदु-से-बिंदु संचार के तरीके, NTCP2 और SSU2 सहित"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. अवलोकन

I2P में **ट्रांसपोर्ट** routers के बीच प्रत्यक्ष, बिंदु-से-बिंदु संचार की एक विधि है। ये तंत्र router प्रमाणीकरण का सत्यापन करते हुए गोपनीयता और अखंडता सुनिश्चित करते हैं।

प्रत्येक ट्रांसपोर्ट ऐसे कनेक्शन प्रतिमानों का उपयोग करके संचालित होता है, जिनमें प्रमाणीकरण, प्रवाह नियंत्रण, पुष्टिकरण, और पुनःप्रेषण क्षमताएँ शामिल होती हैं।

---

## 2. वर्तमान ट्रांसपोर्ट्स

I2P वर्तमान में दो प्रमुख transports (परिवहन प्रोटोकॉल) का समर्थन करता है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 लेगेसी ट्रांसपोर्ट (अप्रचलित)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. ट्रांसपोर्ट सेवाएँ

परिवहन उप-प्रणाली निम्नलिखित सेवाएँ प्रदान करती है:

### 3.1 संदेश वितरण

- विश्वसनीय [I2NP](/docs/specs/i2np/) संदेश वितरण (ट्रांसपोर्ट्स I2NP मैसेजिंग को विशेष रूप से संभालते हैं)
- क्रमानुसार वितरण सार्वभौमिक रूप से **सुनिश्चित नहीं** है
- प्राथमिकता-आधारित संदेश कतारबद्धता

### 3.2 कनेक्शन प्रबंधन

- कनेक्शन की स्थापना और समापन
- थ्रेशहोल्ड प्रवर्तन के साथ कनेक्शन सीमा प्रबंधन
- प्रति-पीयर स्थिति ट्रैकिंग
- स्वचालित और मैनुअल पीयर बैन सूची का प्रवर्तन

### 3.3 नेटवर्क कॉन्फ़िगरेशन

- प्रति ट्रांसपोर्ट कई router पते (v0.9.8 से IPv4 और IPv6 का समर्थन)
- UPnP फ़ायरवॉल पोर्ट खोलना
- NAT/फ़ायरवॉल traversal (मार्ग-पारगमन) समर्थन
- कई तरीकों के माध्यम से स्थानीय IP का पता लगाना

### 3.4 सुरक्षा

- बिंदु-से-बिंदु आदान-प्रदान के लिए एन्क्रिप्शन
- स्थानीय नियमों के अनुसार IP पता सत्यापन
- घड़ी सहमति निर्धारण (NTP बैकअप)

### 3.5 बैंडविड्थ प्रबंधन

- इनबाउंड और आउटबाउंड बैंडविड्थ सीमाएँ
- आउटगोइंग संदेशों के लिए इष्टतम ट्रांसपोर्ट चयन

---

## 4. ट्रांसपोर्ट पते

उपप्रणाली router संपर्क बिंदुओं की सूची बनाए रखती है:

- ट्रांसपोर्ट विधि (NTCP2, SSU2)
- IP पता
- पोर्ट नंबर
- वैकल्पिक पैरामीटर

प्रति ट्रांसपोर्ट विधि कई पते संभव हैं।

### 4.1 सामान्य पता विन्यास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. ट्रांसपोर्ट चयन

सिस्टम [I2NP संदेश](/docs/specs/i2np/) के लिए transports (परिवहन प्रोटोकॉल) का चयन उच्च-स्तरीय प्रोटोकॉलों से स्वतंत्र रूप से करता है। चयन एक **बोली प्रणाली** का उपयोग करता है, जहाँ प्रत्येक transport बोलियाँ प्रस्तुत करता है, और सबसे कम मूल्य वाली बोली जीतती है।

### 5.1 बोली निर्धारण के कारक

- ट्रांसपोर्ट वरीयता सेटिंग्स
- मौजूदा पीयर कनेक्शन
- वर्तमान बनाम सीमा कनेक्शन संख्या
- हालिया कनेक्शन प्रयास इतिहास
- संदेश आकार प्रतिबंध
- पीयर RouterInfo (राउटर की जानकारी) की ट्रांसपोर्ट क्षमताएँ
- कनेक्शन की प्रत्यक्षता (प्रत्यक्ष बनाम introducer (परिचयक) पर निर्भर)
- पीयर द्वारा घोषित ट्रांसपोर्ट वरीयताएँ

आम तौर पर, दो routers एक साथ एकल ट्रांसपोर्ट कनेक्शन बनाए रखते हैं, हालाँकि एक साथ बहु-ट्रांसपोर्ट कनेक्शन भी संभव हैं।

---

## 6. NTCP2

**NTCP2** (New Transport Protocol 2) I2P के लिए आधुनिक TCP-आधारित ट्रांसपोर्ट है, जिसे संस्करण 0.9.36 में पेश किया गया था।

### 6.1 मुख्य विशेषताएँ

- **Noise Protocol Framework** (क्रिप्टोग्राफ़िक हैंडशेक फ्रेमवर्क) (Noise_XK pattern) पर आधारित
- कुंजी विनिमय के लिए **X25519** (एलिप्टिक-कर्व एल्गोरिद्म) का उपयोग करता है
- प्रमाणित कूटलेखन के लिए **ChaCha20/Poly1305** (AEAD योजना) का उपयोग करता है
- हैशिंग के लिए **BLAKE2s** (हैश फ़ंक्शन) का उपयोग करता है
- DPI (Deep Packet Inspection, गहरी पैकेट जाँच) का प्रतिरोध करने के लिए प्रोटोकॉल obfuscation (अस्पष्टकरण)
- ट्रैफ़िक विश्लेषण प्रतिरोध के लिए वैकल्पिक padding (भरण)

### 6.2 कनेक्शन स्थापना

1. **सत्र अनुरोध** (Alice → Bob): अस्थायी X25519 कुंजी + एन्क्रिप्टेड पेलोड
2. **सत्र बनाया गया** (Bob → Alice): अस्थायी कुंजी + एन्क्रिप्टेड पुष्टिकरण
3. **सत्र की पुष्टि** (Alice → Bob): RouterInfo (router की जानकारी) के साथ अंतिम हैंडशेक

इसके बाद का सारा डेटा हैंडशेक से व्युत्पन्न सेशन कुंजियों से एन्क्रिप्ट किया जाता है।

पूर्ण विवरण के लिए [NTCP2 विनिर्देश](/docs/specs/ntcp2/) देखें।

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) I2P के लिए आधुनिक UDP-आधारित ट्रांसपोर्ट है, जिसका परिचय संस्करण 0.9.56 में कराया गया था।

### 7.1 मुख्य विशेषताएँ

- **Noise Protocol Framework** (Noise_XK pattern) पर आधारित
- कुंजी विनिमय के लिए **X25519** का उपयोग करता है
- प्रमाणित एन्क्रिप्शन के लिए **ChaCha20/Poly1305** का उपयोग करता है
- selective acknowledgments (चयनात्मक स्वीकृतियाँ) के साथ आंशिक रूप से विश्वसनीय वितरण
- hole punching और relay/introduction के माध्यम से NAT traversal (NAT पारगमन)
- कनेक्शन माइग्रेशन का समर्थन
- Path MTU discovery (पथ MTU खोज)

### 7.2 SSU (पुराना) पर लाभ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
विस्तृत जानकारी के लिए [SSU2 Specification](/docs/specs/ssu2/) देखें।

---

## 8. NAT Traversal (NAT के पीछे स्थित डिवाइस/सेवा तक पहुँचने की तकनीक)

दोनों ट्रांसपोर्ट्स NAT traversal (NAT के पार संचार स्थापित करने की तकनीक) का समर्थन करते हैं, ताकि फायरवॉल के पीछे मौजूद routers नेटवर्क में भाग ले सकें।

### 8.1 SSU2 परिचय

जब कोई router सीधे इनबाउंड कनेक्शनों को प्राप्त नहीं कर सकता:

1. Router अपने RouterInfo में **introducer** (संपर्क-मध्यस्थ) पते प्रकाशित करता है
2. कनेक्ट होने वाला पीयर introducer को एक परिचय अनुरोध भेजता है
3. Introducer फ़ायरवॉल के पीछे वाले router को कनेक्शन जानकारी अग्रेषित करता है
4. फ़ायरवॉल के पीछे वाला router आउटबाउंड कनेक्शन आरंभ करता है (hole punch — NAT के जरिए रास्ता बनाना)
5. प्रत्यक्ष संचार स्थापित हो जाता है

### 8.2 NTCP2 और फ़ायरवॉल

NTCP2 को इनबाउंड TCP कनेक्टिविटी की आवश्यकता होती है। NAT (नेटवर्क एड्रेस ट्रांसलेशन) के पीछे के router यह कर सकते हैं:

- पोर्ट्स को स्वचालित रूप से खोलने के लिए UPnP का उपयोग करें
- पोर्ट फ़ॉरवर्डिंग को मैन्युअल रूप से कॉन्फ़िगर करें
- आने वाले कनेक्शनों के लिए SSU2 पर निर्भर करें, जबकि जाने वाले कनेक्शनों के लिए NTCP2 का उपयोग करें

---

## 9. प्रोटोकॉल अस्पष्टिकरण

दोनों आधुनिक ट्रांसपोर्ट्स में obfuscation (ट्रैफ़िक को पहचानना कठिन बनाने की तकनीक) विशेषताएँ शामिल हैं:

- **यादृच्छिक पैडिंग** हैंडशेक संदेशों में
- **एन्क्रिप्टेड हेडर** जो प्रोटोकॉल सिग्नेचर उजागर नहीं करते
- **परिवर्तनीय-लंबाई संदेश** ट्रैफ़िक विश्लेषण का प्रतिरोध करने के लिए
- **कोई स्थिर पैटर्न नहीं** कनेक्शन स्थापना में

> **नोट**: Transport-layer obfuscation (परिवहन-स्तर पर अस्पष्टता) I2P के tunnel आर्किटेक्चर द्वारा प्रदान की गई गुमनामी का पूरक है, लेकिन उसका प्रतिस्थापन नहीं है।

---

## 10. भविष्य का विकास

योजनाबद्ध अनुसंधान और सुधारों में शामिल हैं:

- **Pluggable transports** (प्लग-इन आधारित ट्रांसपोर्ट तकनीक) – Tor-संगत ट्रैफिक-छलावरण प्लगइन्स
- **QUIC-based transport** – QUIC प्रोटोकॉल के लाभों की जांच
- **Connection limit optimization** – इष्टतम पीयर कनेक्शन सीमाओं पर शोध
- **Enhanced padding strategies** – ट्रैफिक विश्लेषण के प्रति प्रतिरोध में सुधार

---

## 11. संदर्भ

- [NTCP2 विनिर्देश](/docs/specs/ntcp2/) – Noise-आधारित TCP परिवहन
- [SSU2 विनिर्देश](/docs/specs/ssu2/) – सुरक्षित अर्ध-विश्वसनीय UDP 2
- [I2NP विनिर्देश](/docs/specs/i2np/) – I2P नेटवर्क प्रोटोकॉल संदेश
- [सामान्य संरचनाएँ](/docs/specs/common-structures/) – RouterInfo और पते की संरचनाएँ
- [ऐतिहासिक NTCP चर्चा](/docs/ntcp/) – लेगेसी परिवहन के विकास का इतिहास
- [लेगेसी SSU प्रलेखन](/docs/legacy/ssu/) – मूल SSU विनिर्देश (अप्रचलित)
