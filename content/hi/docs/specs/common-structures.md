---
title: "सामान्य संरचनाएँ"
description: "विभिन्न I2P विनिर्देशों में प्रयुक्त साझा डेटा प्रकार और सीरियलाइज़ेशन प्रारूप"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

यह दस्तावेज़ सभी I2P प्रोटोकॉल में प्रयुक्त मूलभूत डेटा संरचनाएँ निर्दिष्ट करता है, जिनमें [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) आदि शामिल हैं। ये सामान्य संरचनाएँ विभिन्न I2P कार्यान्वयनों और प्रोटोकॉल परतों के बीच अंतरसंचालनीयता सुनिश्चित करती हैं।

### 0.9.58 के बाद के प्रमुख बदलाव

- Router Identities के लिए ElGamal और DSA-SHA1 अप्रचलित (X25519 + EdDSA का उपयोग करें)
- पोस्ट-क्वांटम ML-KEM समर्थन बीटा परीक्षण में (2.10.0 से opt-in (स्वैच्छिक सक्रियण))
- Service record विकल्पों का मानकीकरण किया गया ([Proposal 167](/proposals/167-service-records/), 0.9.66 में लागू)
- संपीड़नयोग्य पैडिंग विनिर्देशों को अंतिम रूप दिया गया ([Proposal 161](/hi/proposals/161-ri-dest-padding/), 0.9.57 में लागू)

---

## सामान्य प्रकार विनिर्देश

### पूर्णांक

**विवरण:** नेटवर्क बाइट क्रम (big-endian) में एक अऋणात्मक पूर्णांक को निरूपित करता है।

**सामग्री:** 1 से 8 बाइट्स, जो एक unsigned integer (बिना चिन्ह वाला पूर्णांक) का प्रतिनिधित्व करते हैं।

**उपयोग:** I2P प्रोटोकॉलों में सर्वत्र फील्ड की लंबाइयाँ, गिनतियाँ, प्रकार पहचानकर्ता, और संख्यात्मक मान।

---

### दिनांक

**विवरण:** Unix epoch (1 जनवरी 1970 00:00:00 GMT) से बीते मिलीसेकंड का प्रतिनिधित्व करने वाला टाइमस्टैम्प।

**सामग्री:** 8-बाइट पूर्णांक (unsigned long, बिना चिह्न वाला long प्रकार का पूर्णांक)

**विशेष मान:** - `0` = अपरिभाषित या null (रिक्त) तिथि - अधिकतम मान: `0xFFFFFFFFFFFFFFFF` (वर्ष 584,942,417,355)

**कार्यान्वयन संबंधी टिप्पणियाँ:** - हमेशा UTC/GMT समय क्षेत्र - मिलीसेकंड-स्तरीय परिशुद्धता आवश्यक - लीज़ की समाप्ति, RouterInfo प्रकाशन, और टाइमस्टैम्प सत्यापन के लिए उपयोग किया जाता है

---

### अक्षर शृंखला

**विवरण:** लंबाई प्रीफिक्स के साथ UTF-8 एन्कोडेड स्ट्रिंग.

**प्रारूप:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**सीमाएँ:** - अधिकतम लंबाई: 255 बाइट्स (अक्षर नहीं - बहु-बाइट UTF-8 अनुक्रम कई बाइट्स के रूप में गिने जाते हैं) - लंबाई शून्य हो सकती है (खाली स्ट्रिंग) - Null terminator शामिल नहीं है - स्ट्रिंग null-terminated नहीं है

**महत्वपूर्ण:** UTF-8 अनुक्रम प्रत्येक वर्ण के लिए कई बाइट का उपयोग कर सकते हैं। 100 वर्णों वाली string (टेक्स्ट डेटा का अनुक्रम) यदि मल्टी-बाइट वर्णों का उपयोग करती है, तो 255-बाइट सीमा से अधिक हो सकती है।

---

## क्रिप्टोग्राफिक कुंजी संरचनाएँ

### सार्वजनिक कुंजी

**विवरण:** असममित एन्क्रिप्शन के लिए सार्वजनिक कुंजी। कुंजी का प्रकार और लंबाई संदर्भ-निर्भर होते हैं या उन्हें Key Certificate (कुंजी प्रमाणपत्र) में निर्दिष्ट किया जाता है।

**डिफ़ॉल्ट प्रकार:** ElGamal (0.9.58 से Router पहचानों के लिए अप्रचलित)

**समर्थित प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**कार्यान्वयन आवश्यकताएँ:**

1. **X25519 (Type 4) - वर्तमान मानक:**
   - ECIES-X25519-AEAD-Ratchet एन्क्रिप्शन के लिए उपयोग होता है
   - 0.9.48 से Router Identities (राउटर पहचानें) के लिए अनिवार्य
   - लिटिल-एंडियन एन्कोडिंग (अन्य प्रकारों के विपरीत)
   - देखें [ECIES](/docs/specs/ecies/) और [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - लेगेसी:**
   - संस्करण 0.9.58 से Router पहचान के लिए अप्रचलित
   - Destinations (I2P में गंतव्य पहचान) के लिए अभी भी मान्य (यह फ़ील्ड 0.6/2005 से अप्रयुक्त)
   - [ElGamal विनिर्देशन](/docs/specs/cryptography/) में परिभाषित स्थिर अभाज्य संख्याओं का उपयोग करता है
   - पिछड़ी संगतता (backward compatibility) के लिए समर्थन बनाए रखा गया है

3. **MLKEM (क्वांटम-पश्चात) - बीटा:**
   - हाइब्रिड दृष्टिकोण ML-KEM को X25519 के साथ संयोजित करता है
   - 2.10.0 में डिफ़ॉल्ट रूप से सक्षम नहीं है
   - Hidden Service Manager (छिपी सेवा प्रबंधक) के माध्यम से मैनुअल सक्रियण आवश्यक है
   - देखें [ECIES-HYBRID](/docs/specs/ecies/#hybrid) और [Proposal 169](/proposals/169-pq-crypto/)
   - टाइप कोड और विनिर्देश परिवर्तन के अधीन हैं

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### निजी कुंजी

**विवरण:** असममित डिक्रिप्शन (asymmetric decryption) के लिए निजी कुंजी, जो PublicKey प्रकारों के अनुरूप है।

**भंडारण:** प्रकार और लंबाई संदर्भ से अनुमानित, या डेटा संरचनाओं/कुंजी फ़ाइलों में अलग से संग्रहीत।

**समर्थित प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**सुरक्षा नोट्स:** - निजी कुंजियाँ क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक संख्या जेनरेटर का उपयोग करके अवश्य उत्पन्न की जानी चाहिए - X25519 निजी कुंजियाँ RFC 7748 में परिभाषित scalar clamping (स्केलर क्लैम्पिंग: निजी-कुंजी स्केलर के कुछ बिटों को मास्क/निश्चित करके सुरक्षित सीमा में बाँधने की प्रक्रिया) का उपयोग करती हैं - जब कुंजी-सामग्री की आवश्यकता न रहे, तो उसे मेमोरी से सुरक्षित रूप से अवश्य मिटा दिया जाना चाहिए

**JavaDoc (Java का डॉक्यूमेंटेशन उपकरण):** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### सेशन कुंजी

**Description:** I2P के tunnel और garlic encryption में AES-256 एन्क्रिप्शन और डिक्रिप्शन के लिए सममित कुंजी।

**सामग्री:** 32 बाइट (256 बिट)

**उपयोग:** - tunnel लेयर एन्क्रिप्शन (AES-256/CBC with IV) - garlic संदेश एन्क्रिप्शन (I2P की 'garlic encryption' तकनीक, जिसमें समूहित संदेशों का एन्क्रिप्शन होता है) - एंड-टू-एंड सेशन एन्क्रिप्शन

**जनरेशन:** क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक संख्या जनरेटर का उपयोग करना अनिवार्य है।

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**विवरण:** हस्ताक्षर सत्यापन के लिए सार्वजनिक कुंजी। प्रकार और लंबाई Key Certificate of Destination में निर्दिष्ट होती है या संदर्भ से अनुमानित की जाती है।

**डिफ़ॉल्ट प्रकार:** DSA_SHA1 (0.9.58 से अप्रचलित)

**समर्थित प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**कार्यान्वयन आवश्यकताएँ:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - वर्तमान मानक:**
   - 2015 के उत्तरार्ध से सभी नए Router Identities और Destinations के लिए डिफ़ॉल्ट
   - SHA-512 हैशिंग के साथ Ed25519 कर्व का उपयोग करता है
   - 32-बाइट सार्वजनिक कुंजियाँ, 64-बाइट हस्ताक्षर
   - Little-endian (सबसे कम महत्वपूर्ण बाइट पहले) एन्कोडिंग (अधिकांश अन्य प्रकारों के विपरीत)
   - उच्च प्रदर्शन और सुरक्षा

2. **RedDSA_SHA512_Ed25519 (Type 11) - विशेषीकृत:**
   - केवल एन्क्रिप्टेड leasesets और blinding (छिपाकर गणना) के लिए ही उपयोग होता है
   - Router पहचानें या मानक Destinations के लिए कभी उपयोग नहीं होता
   - EdDSA से प्रमुख अंतर:
     - निजी कुंजियाँ modular reduction (मॉड्यूलो-आधारित घटाव) के जरिए; clamping (बिट सीमाबद्ध करना) नहीं
     - हस्ताक्षरों में 80 बाइट्स का यादृच्छिक डेटा शामिल होता है
     - निजी कुंजियों के हैश की बजाय सार्वजनिक कुंजियों का सीधे उपयोग करता है
   - देखें [Red25519 specification](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - लेगेसी:**
   - 0.9.58 से Router पहचानों के लिए अप्रचलित
   - नई Destinations (गंतव्य) के लिए हतोत्साहित
   - 1024-बिट DSA, SHA-1 के साथ (ज्ञात कमजोरियाँ)
   - केवल संगतता के लिए समर्थन बनाए रखा गया है

4. **बहु-घटक कुंजियाँ:**
   - जब यह दो घटकों से मिलकर बना हो (उदा., ECDSA (एलिप्टिक कर्व डिजिटल सिग्नेचर एल्गोरिदम) के बिंदु X,Y)
   - प्रत्येक घटक को प्रारंभिक शून्यों के साथ लंबाई/2 तक पैड किया जाता है
   - उदाहरण: 64-बाइट ECDSA कुंजी = 32-बाइट X + 32-बाइट Y

**जावाडॉक:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**विवरण:** हस्ताक्षर बनाने के लिए निजी कुंजी, जो SigningPublicKey प्रकारों के अनुरूप है।

**स्टोरेज:** निर्माण के समय प्रकार और लंबाई निर्दिष्ट की जाती है।

**समर्थित प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**सुरक्षा आवश्यकताएँ:** - क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक स्रोत का उपयोग करके उत्पन्न करें - उचित अभिगम नियंत्रणों के साथ सुरक्षित रखें - कार्य पूर्ण होने पर मेमोरी से सुरक्षित रूप से मिटाएँ - EdDSA (एक क्रिप्टोग्राफ़िक डिजिटल हस्ताक्षर एल्गोरिद्म) के लिए: 32-बाइट सीड को SHA-512 (क्रिप्टोग्राफ़िक हैश फ़ंक्शन) से हैश किया जाता है, पहले 32 बाइट्स से स्केलर बनता है (क्लैम्प्ड) - RedDSA (EdDSA का एक प्रकार) के लिए: कुंजी-निर्माण भिन्न है (क्लैम्पिंग की बजाय मॉड्यूलर रिडक्शन)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### हस्ताक्षर

**विवरण:** डेटा पर क्रिप्टोग्राफिक हस्ताक्षर, जो SigningPrivateKey प्रकार के अनुरूप हस्ताक्षर एल्गोरिदम का उपयोग करके उत्पन्न किया गया है।

**प्रकार और लंबाई:** हस्ताक्षर के लिए उपयोग किए गए कुंजी प्रकार से निर्धारित।

**समर्थित प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**प्रारूप नोट्स:** - बहु-घटक हस्ताक्षर (उदा., ECDSA R,S मान) को प्रति तत्व लंबाई/2 तक अग्रणी शून्यों से पैड किया जाता है - EdDSA और RedDSA little-endian encoding (कम-महत्वपूर्ण-बाइट पहले क्रम) का उपयोग करते हैं - अन्य सभी प्रकार big-endian encoding (अधिक-महत्वपूर्ण-बाइट पहले क्रम) का उपयोग करते हैं

**सत्यापन:** - संबंधित SigningPublicKey (हस्ताक्षर सार्वजनिक कुंजी) का उपयोग करें - कुंजी प्रकार के लिए हस्ताक्षर एल्गोरिथ्म के विनिर्देशों का पालन करें - जाँचें कि हस्ताक्षर की लंबाई कुंजी प्रकार के लिए अपेक्षित लंबाई से मेल खाती है

**जावाडॉक:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### हैश

**विवरण:** डेटा का SHA-256 हैश, I2P भर में अखंडता सत्यापन और पहचान के लिए उपयोग किया जाता है।

**सामग्री:** 32 बाइट (256 बिट)

**उपयोग:** - Router पहचान हैश (नेटवर्क डेटाबेस कुंजियाँ) - Destination (गंतव्य) हैश (नेटवर्क डेटाबेस कुंजियाँ) - Leases (लीज़) में Tunnel गेटवे की पहचान - डेटा अखंडता सत्यापन - Tunnel ID का निर्माण

**एल्गोरिथ्म:** SHA-256 जैसा कि FIPS 180-4 में परिभाषित है

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### सत्र टैग

**विवरण:** सत्र की पहचान और टैग-आधारित एन्क्रिप्शन के लिए उपयोग की जाने वाली यादृच्छिक संख्या।

**महत्वपूर्ण:** Session Tag (सेशन टैग—अस्थायी पहचान टैग) का आकार एन्क्रिप्शन प्रकार के अनुसार बदलता है: - **ElGamal/AES+SessionTag:** 32 बाइट (पुराना) - **ECIES-X25519:** 8 बाइट (वर्तमान मानक)

**वर्तमान मानक (ECIES - एलिप्टिक कर्व इंटीग्रेटेड एन्क्रिप्शन स्कीम):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
विस्तृत विनिर्देशों के लिए [ECIES](/docs/specs/ecies/) और [ECIES-ROUTERS](/docs/specs/ecies/#routers) देखें।

**लेगेसी (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**उत्पादन:** cryptographically secure random number generator (कूटलेखी रूप से सुरक्षित यादृच्छिक संख्या जनक) का उपयोग अनिवार्य है।

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**विवरण:** tunnel में router की स्थिति का एक अद्वितीय पहचानकर्ता। tunnel में प्रत्येक हॉप का अपना अलग TunnelId (टनल में हॉप की पहचान/ID) होता है।

**प्रारूप:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**उपयोग:** - प्रत्येक router पर आने/जाने वाली tunnel कनेक्शनों की पहचान करता है - tunnel श्रृंखला के प्रत्येक हॉप पर अलग TunnelId - गेटवे tunnel की पहचान करने के लिए Lease संरचनाओं में उपयोग किया जाता है

**विशेष मान:** - `0` = विशेष प्रोटोकॉल उपयोगों के लिए आरक्षित (सामान्य संचालन में बचें) - TunnelIds प्रत्येक router के लिए केवल स्थानीय रूप से अर्थपूर्ण होते हैं

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## प्रमाणपत्र विनिर्देश

### प्रमाणपत्र

**विवरण:** पूरे I2P में प्रयुक्त रसीदें, proof-of-work (कार्य का प्रमाण—गणनात्मक प्रयास-आधारित सत्यापन), या क्रिप्टोग्राफिक मेटाडेटा के लिए कंटेनर।

**प्रारूप:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**कुल आकार:** 3 बाइट न्यूनतम (NULL प्रमाणपत्र), अधिकतम 65538 बाइट

### प्रमाणपत्र के प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### कुंजी प्रमाणपत्र (प्रकार 5)

**परिचय:** संस्करण 0.9.12 (दिसंबर 2013)

**उद्देश्य:** गैर-डिफ़ॉल्ट कुंजी प्रकार निर्दिष्ट करता है और मानक 384-बाइट KeysAndCert संरचना से परे अतिरिक्त कुंजी डेटा संग्रहीत करता है।

**पेलोड संरचना:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**महत्वपूर्ण कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **कुंजी प्रकार का क्रम:**
   - **चेतावनी:** हस्ताक्षर कुंजी प्रकार, क्रिप्टो कुंजी प्रकार से पहले आता है
   - यह सहज-बोध के विपरीत है, लेकिन संगतता बनाए रखने के लिए ऐसा रखा गया है
   - क्रम: SPKtype, CPKtype (CPKtype, SPKtype नहीं)

2. **KeysAndCert (Keys और Certificate की संरचना) में कुंजी डेटा का विन्यास:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **अतिरिक्त कुंजी डेटा की गणना:**
   - If Crypto Key > 256 बाइट्स: Excess = (Crypto Length - 256)
   - If Signing Key > 128 बाइट्स: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**उदाहरण (ElGamal क्रिप्टो कुंजी):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Router पहचान आवश्यकताएँ:** - NULL certificate (रिक्त प्रमाणपत्र) का उपयोग संस्करण 0.9.15 तक किया गया - गैर-डिफ़ॉल्ट कुंजी प्रकारों के लिए 0.9.16 से Key Certificate (कुंजी प्रमाणपत्र) आवश्यक - X25519 encryption keys (एन्क्रिप्शन कुंजियाँ) 0.9.48 से समर्थित

**गंतव्य आवश्यकताएँ:** - NULL certificate (रिक्त प्रमाणपत्र) या Key Certificate (कुंजी प्रमाणपत्र) (आवश्यकतानुसार) - 0.9.12 से गैर-डिफ़ॉल्ट हस्ताक्षर कुंजी प्रकारों के लिए Key Certificate आवश्यक है - क्रिप्टो सार्वजनिक कुंजी फ़ील्ड 0.6 (2005) से उपयोग में नहीं है, लेकिन फिर भी मौजूद होना आवश्यक है

**महत्वपूर्ण चेतावनियाँ:**

1. **NULL बनाम KEY Certificate:**
   - types (0,0) वाला KEY certificate (KEY प्रमाणपत्र), जो ElGamal+DSA_SHA1 (क्रिप्टोग्राफ़िक कुंजी/हस्ताक्षर एल्गोरिद्म संयोजन) निर्दिष्ट करता है, अनुमत है, लेकिन अनुशंसित नहीं है
   - ElGamal+DSA_SHA1 के लिए हमेशा NULL certificate (NULL प्रमाणपत्र) का उपयोग करें (canonical representation—कैनोनिकल/मानक रूप)
   - (0,0) वाला KEY certificate 4 बाइट लंबा होता है और संगतता संबंधी समस्याएँ पैदा कर सकता है
   - कुछ कार्यान्वयन संभवतः (0,0) KEY certificates को सही ढंग से संभाल नहीं पाएँगे

2. **अतिरिक्त डेटा सत्यापन:**
   - कार्यान्वयन को यह सत्यापित करना अनिवार्य है कि प्रमाणपत्र की लंबाई कुंजी प्रकारों के लिए अपेक्षित लंबाई से मेल खाती हो
   - ऐसे प्रमाणपत्रों को अस्वीकार करें जिनमें अतिरिक्त डेटा हो जो कुंजी प्रकारों से मेल नहीं खाता
   - वैध प्रमाणपत्र संरचना के बाद आने वाले किसी भी अनुगामी कचरा डेटा को प्रतिबंधित करें

**JavaDoc:** [प्रमाणपत्र](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### मैपिंग

**विवरण:** कॉन्फ़िगरेशन और मेटाडेटा के लिए प्रयुक्त कुंजी-मूल्य गुणों का संग्रह।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**आकार सीमाएँ:** - कुंजी लंबाई: 0-255 बाइट्स (+ 1 लंबाई बाइट) - मान लंबाई: 0-255 बाइट्स (+ 1 लंबाई बाइट) - कुल मैपिंग आकार: 0-65535 बाइट्स (+ 2 आकार फ़ील्ड बाइट्स) - अधिकतम संरचना आकार: 65537 बाइट्स

**महत्वपूर्ण छँटाई संबंधी आवश्यकता:**

जब मैपिंग्स **हस्ताक्षरित संरचनाओं** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig) में दिखाई देती हैं, तो हस्ताक्षर की अपरिवर्तनीयता सुनिश्चित करने के लिए प्रविष्टियाँ कुंजी के अनुसार अनिवार्य रूप से क्रमबद्ध होनी चाहिए:

1. **सॉर्ट विधि:** यूनिकोड कोड पॉइंट मानों का उपयोग करके शब्दकोशीय क्रम (Java String.compareTo() के समकक्ष)
2. **केस सेंसिटिविटी:** कुंजियाँ और मान सामान्यतः केस-सेंसिटिव होते हैं (एप्लिकेशन पर निर्भर)
3. **डुप्लिकेट कुंजियाँ:** हस्ताक्षरित संरचनाओं में अनुमत नहीं (इससे हस्ताक्षर सत्यापन विफल होगा)
4. **वर्ण एन्कोडिंग:** UTF-8 बाइट-स्तरीय तुलना

**छँटाई क्यों महत्वपूर्ण है:** - हस्ताक्षर बाइट प्रतिनिधित्व पर गणना किए जाते हैं - अलग-अलग कुंजी क्रम अलग-अलग हस्ताक्षर उत्पन्न करते हैं - अहस्ताक्षरित मैपिंग्स में छँटाई की आवश्यकता नहीं होती लेकिन वही परंपरा का पालन करना चाहिए

**कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **एन्कोडिंग में अतिरिक्तता:**
   - `=` और `;` दोनों विभाजक तथा स्ट्रिंग-लंबाई बाइट्स मौजूद हैं
   - यह अकार्यक्षम है, पर संगतता के लिए बनाए रखा गया है
   - लंबाई बाइट्स को प्रामाणिक माना जाता है; विभाजक आवश्यक तो हैं, पर अतिरिक्त हैं

2. **अक्षर समर्थन:**
   - दस्तावेज़ के बावजूद, स्ट्रिंग्स के भीतर `=` और `;` वास्तव में समर्थित हैं (लंबाई बाइट्स इसे संभालती हैं)
   - UTF-8 एन्कोडिंग पूर्ण यूनिकोड का समर्थन करती है
   - **चेतावनी:** I2CP UTF-8 का उपयोग करता है, लेकिन I2NP ऐतिहासिक रूप से UTF-8 को सही ढंग से संभाल नहीं पाता था
   - अधिकतम अनुकूलता के लिए, संभव हो तो I2NP मैपिंग के लिए ASCII का उपयोग करें

3. **विशेष संदर्भ:**
   - **RouterInfo/RouterAddress:** अनिवार्य रूप से क्रमबद्ध हों, डुप्लिकेट न हों
   - **I2CP SessionConfig:** अनिवार्य रूप से क्रमबद्ध हों, डुप्लिकेट न हों  
   - **एप्लिकेशन मैपिंग्स:** क्रमबद्ध करना अनुशंसित है, पर हमेशा आवश्यक नहीं

**उदाहरण (RouterInfo विकल्प):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**जावाडॉक:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## सामान्य संरचना विनिर्देश

### कुंजियाँ और प्रमाणपत्र

**विवरण:** एन्क्रिप्शन कुंजी, साइनिंग कुंजी, और प्रमाणपत्र को जोड़ने वाली मूलभूत संरचना। RouterIdentity (Router की पहचान) और Destination (गंतव्य) दोनों के रूप में उपयोग किया जाता है।

**संरचना:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**कुंजी संरेखण:** - **क्रिप्टोग्राफ़िक सार्वजनिक कुंजी:** आरंभ पर संरेखित (बाइट 0) - **पैडिंग:** बीच में (यदि आवश्यक हो) - **हस्ताक्षर सार्वजनिक कुंजी:** अंत पर संरेखित (बाइट 256 से बाइट 383) - **प्रमाणपत्र:** बाइट 384 से शुरू होता है

**आकार की गणना:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### पैडिंग जनरेशन दिशानिर्देश ([प्रस्ताव 161](/hi/proposals/161-ri-dest-padding/))

**कार्यान्वयन संस्करण:** 0.9.57 (जनवरी 2023, रिलीज़ 2.1.0)

**पृष्ठभूमि:** - गैर-ElGamal+DSA कुंजियों के लिए, 384-बाइट की स्थिर संरचना में पैडिंग मौजूद है - Destinations (I2P में गंतव्य) के लिए, 256-बाइट का पब्लिक की फ़ील्ड संस्करण 0.6 (2005) से अप्रयुक्त है - पैडिंग इस तरह उत्पन्न की जानी चाहिए कि वह सुरक्षित रहते हुए संपीड़नीय भी हो

**आवश्यकताएँ:**

1. **न्यूनतम यादृच्छिक डेटा:**
   - कम से कम 32 बाइट क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक डेटा का उपयोग करें
   - यह सुरक्षा के लिए पर्याप्त एंट्रॉपी प्रदान करता है

2. **संपीड़न रणनीति:**
   - पूरे padding/public key फ़ील्ड में वही 32 बाइट्स दोहराएँ
   - I2NP Database Store, Streaming SYN, SSU2 handshake जैसी प्रोटोकॉल्स संपीड़न का उपयोग करती हैं
   - सुरक्षा से समझौता किए बिना उल्लेखनीय बैंडविड्थ बचत होती है

3. **उदाहरण:**

**Router की पहचान (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**गंतव्य (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **यह क्यों काम करता है:**
   - पूर्ण संरचना का SHA-256 हैश अब भी सारी एंट्रॉपी (यादृच्छिकता) शामिल करता है
   - नेटवर्क डेटाबेस DHT (वितरित हैश तालिका) का वितरण केवल हैश पर निर्भर करता है
   - साइनिंग कुंजी (32 बाइट EdDSA/X25519) 256 बिट एंट्रॉपी प्रदान करती है
   - अतिरिक्त 32 बाइट के दोहराए गए यादृच्छिक डेटा = कुल 512 बिट एंट्रॉपी
   - क्रिप्टोग्राफ़िक मज़बूती के लिए पर्याप्त से अधिक

5. **कार्यान्वयन नोट्स:**
   - अनिवार्य है कि पूरी 387+ बाइट संरचना को संग्रहीत किया जाए और प्रेषित किया जाए
   - पूर्ण असंपीड़ित संरचना पर SHA-256 हैश की गणना की जाती है
   - संपीड़न प्रोटोकॉल स्तर पर लागू किया जाता है (I2NP, Streaming, SSU2)
   - 0.6 (2005) से सभी संस्करणों के साथ पिछड़ा-संगत

**JavaDoc (Java दस्तावेज़ीकरण):** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (router की पहचान)

**विवरण:** I2P नेटवर्क में किसी router की अद्वितीय पहचान करता है। इसकी संरचना KeysAndCert (कुंजियों और प्रमाणपत्र की एकीकृत संरचना) के समान है।

**प्रारूप:** ऊपर दिए गए KeysAndCert संरचना को देखें

**वर्तमान आवश्यकताएँ (0.9.58 तक):**

1. **अनिवार्य कुंजी प्रकार:**
   - **एन्क्रिप्शन:** X25519 (प्रकार 4, 32 बाइट)
   - **हस्ताक्षर:** EdDSA_SHA512_Ed25519 (प्रकार 7, 32 बाइट)
   - **प्रमाणपत्र:** कुंजी प्रमाणपत्र (प्रकार 5)

2. **अप्रचलित कुंजी प्रकार:**
   - ElGamal (प्रकार 0) 0.9.58 से Router Identities (पहचानें) के लिए अप्रचलित है
   - DSA_SHA1 (प्रकार 0) 0.9.58 से Router Identities के लिए अप्रचलित है
   - इनका नए routers के लिए उपयोग नहीं किया जाना चाहिए

3. **सामान्य आकार:**
   - X25519 + EdDSA कुंजी प्रमाणपत्र के साथ = 391 बाइट्स
   - 32 बाइट्स X25519 सार्वजनिक कुंजी
   - 320 बाइट्स पैडिंग ([Proposal 161](/hi/proposals/161-ri-dest-padding/) के अनुसार संपीडनीय)
   - 32 बाइट्स EdDSA सार्वजनिक कुंजी
   - 7 बाइट्स प्रमाणपत्र (3-बाइट हेडर + 4-बाइट कुंजी प्रकार)

**ऐतिहासिक विकास:** - 0.9.16-पूर्व: हमेशा NULL प्रमाणपत्र (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Key Certificate (कुंजी प्रमाणपत्र) समर्थन जोड़ा गया - 0.9.48+: X25519 एन्क्रिप्शन कुंजियों का समर्थन जोड़ा गया - 0.9.58+: ElGamal और DSA_SHA1 अप्रचलित कर दिए गए

**नेटवर्क डेटाबेस कुंजी:** - RouterInfo (राउटर की जानकारी) की कुंजी पूर्ण RouterIdentity (राउटर की पहचान) के SHA-256 हैश पर आधारित है - हैश 391+ बाइट की संपूर्ण संरचना (padding (पैडिंग) सहित) पर गणना किया जाता है

**यह भी देखें:** - पैडिंग उत्पन्न करने के दिशानिर्देश ([प्रस्ताव 161](/hi/proposals/161-ri-dest-padding/)) - ऊपर दिया गया कुंजी प्रमाणपत्र विनिर्देश

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### गंतव्य

**विवरण:** सुरक्षित संदेश प्रेषण हेतु Endpoint (एंडपॉइंट, अर्थात संचार का अंतिम बिंदु) पहचानकर्ता। संरचनात्मक रूप से KeysAndCert के समान, लेकिन उपयोग के अर्थगत पहलू भिन्न हैं।

**प्रारूप:** ऊपर दी गई KeysAndCert संरचना देखें

**RouterIdentity से महत्वपूर्ण अंतर:** - **पब्लिक की फ़ील्ड उपयोग में नहीं है और इसमें यादृच्छिक डेटा हो सकता है** - यह फ़ील्ड संस्करण 0.6 (2005) से उपयोग में नहीं है - मूल रूप से पुराने I2CP-to-I2CP एन्क्रिप्शन के लिए था (निष्क्रिय) - वर्तमान में केवल अप्रचलित LeaseSet एन्क्रिप्शन के लिए IV (Initialization Vector—प्रारंभिक वेक्टर) के रूप में उपयोग होता है

**वर्तमान अनुशंसाएँ:**

1. **हस्ताक्षर कुंजी:**
   - **अनुशंसित:** EdDSA_SHA512_Ed25519 (प्रकार 7, 32 बाइट)
   - विकल्प: ECDSA प्रकार (Elliptic Curve Digital Signature Algorithm - दीर्घवृत्त वक्र डिजिटल हस्ताक्षर एल्गोरिथम) पुराने संस्करणों के साथ संगतता हेतु
   - इससे बचें: DSA_SHA1 (अप्रचलित, अनुशंसित नहीं)

2. **एन्क्रिप्शन कुंजी:**
   - यह फ़ील्ड प्रयुक्त नहीं है, पर उपस्थित होना अनिवार्य है
   - **अनुशंसित:** [Proposal 161](/hi/proposals/161-ri-dest-padding/) के अनुसार यादृच्छिक डेटा से भरें (संपीड़नीय)
   - आकार: हमेशा 256 बाइट्स (ElGamal (एक सार्वजनिक-कुंजी एन्क्रिप्शन योजना) स्लॉट, भले ही ElGamal के लिए उपयोग नहीं होता)

3. **प्रमाणपत्र:**
   - ElGamal + DSA_SHA1 के लिए NULL प्रमाणपत्र (केवल लेगेसी के लिए)
   - अन्य सभी हस्ताक्षर कुंजी प्रकारों के लिए कुंजी प्रमाणपत्र

**सामान्य आधुनिक गंतव्य:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**वास्तविक एन्क्रिप्शन कुंजी:** - Destination (I2P गंतव्य पता) के लिए एन्क्रिप्शन कुंजी **LeaseSet** में होती है, Destination में नहीं - LeaseSet वर्तमान एन्क्रिप्शन सार्वजनिक कुंजी(यों) को रखता है - एन्क्रिप्शन कुंजी के प्रबंधन के लिए LeaseSet2 विनिर्देश देखें

**नेटवर्क डेटाबेस कुंजी:** - LeaseSet की कुंजी पूर्ण Destination (I2P में गंतव्य पहचान) के SHA-256 हैश पर आधारित होती है - हैश पूर्ण 387+ बाइट संरचना पर गणना किया जाता है

**JavaDoc:** [Destination (गंतव्य)](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## नेटवर्क डेटाबेस संरचनाएँ

### Lease (लीज़—I2P में एक प्रविष्टि जो inbound tunnel के अंत-बिंदु और समाप्ति को बताती है)

**विवरण:** किसी विशिष्ट tunnel को किसी Destination (I2P में गंतव्य पहचान) के लिए संदेश प्राप्त करने की अनुमति देता है। मूल LeaseSet प्रारूप (type 1) का हिस्सा है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**कुल आकार:** 44 बाइट्स

**उपयोग:** - केवल मूल LeaseSet में उपयोग किया जाता है (प्रकार 1, अप्रचलित) - LeaseSet2 और बाद के रूपांतरों के लिए, इसके बजाय Lease2 का उपयोग करें

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (प्रकार 1)

**विवरण:** मूल LeaseSet प्रारूप. किसी Destination (गंतव्य) के लिए अधिकृत tunnels और कुंजियाँ शामिल करता है. नेटवर्क डेटाबेस में संग्रहीत. **स्थिति: अप्रचलित** (इसके बजाय LeaseSet2 का उपयोग करें).

**संरचना:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**डेटाबेस संग्रहण:** - **डेटाबेस प्रकार:** 1 - **कुंजी:** Destination (गंतव्य) का SHA-256 हैश - **मान:** पूर्ण LeaseSet संरचना

**महत्वपूर्ण नोट्स:**

1. **Destination (गंतव्य) सार्वजनिक कुंजी अप्रयुक्त:**
   - Destination में एन्क्रिप्शन सार्वजनिक कुंजी फ़ील्ड अप्रयुक्त है
   - LeaseSet में एन्क्रिप्शन कुंजी ही वास्तविक एन्क्रिप्शन कुंजी है

2. **अस्थायी कुंजियाँ:**
   - `encryption_key` अस्थायी है (router के प्रारंभ पर पुनः उत्पन्न होता है)
   - `signing_key` अस्थायी है (router के प्रारंभ पर पुनः उत्पन्न होता है)
   - रीस्टार्ट के बाद कोई भी कुंजी स्थायी नहीं रहती

3. **निरस्तीकरण (कार्यान्वित नहीं किया गया):**
   - `signing_key` का उद्देश्य LeaseSet के निरस्तीकरण के लिए था
   - निरस्तीकरण तंत्र कभी कार्यान्वित नहीं किया गया
   - शून्य-लीज़ LeaseSet निरस्तीकरण के लिए अभिप्रेत था, लेकिन अप्रयुक्त है

4. **वर्ज़निंग/टाइमस्टैम्प:**
   - LeaseSet में `published` टाइमस्टैम्प फ़ील्ड स्पष्ट रूप से मौजूद नहीं है
   - वर्ज़न सभी लीज़ (lease—टनेल तक पहुँच का अस्थायी रिकॉर्ड) में सबसे पहले होने वाली समाप्ति तिथि होता है
   - स्वीकार किए जाने के लिए नए LeaseSet में लीज़ की समाप्ति तिथि और भी पहले की होनी चाहिए

5. **लीज़ समाप्ति का प्रकाशन:**
   - Pre-0.9.7: सभी लीज़ एक ही समाप्ति समय (सबसे प्रारंभिक) के साथ प्रकाशित की जाती थीं
   - 0.9.7+: प्रत्येक लीज़ की वास्तविक, व्यक्तिगत समाप्ति समय प्रकाशित होते हैं
   - यह कार्यान्वयन का विवरण है, विशिष्टता का हिस्सा नहीं है

6. **शून्य Lease (लीज़):**
   - LeaseSet में शून्य Lease तकनीकी रूप से अनुमत है
   - निरसन के लिए अभिप्रेत (लागू नहीं किया गया)
   - व्यवहार में अप्रयुक्त
   - LeaseSet2 रूपांतरों को कम-से-कम एक Lease की आवश्यकता होती है

**अप्रचलन:** LeaseSet प्रकार 1 अप्रचलित है। नए कार्यान्वयनों को **LeaseSet2 (प्रकार 3)** का उपयोग करना चाहिए, जो प्रदान करता है: - प्रकाशित टाइमस्टैम्प फ़ील्ड (बेहतर संस्करण निर्धारण) - कई एन्क्रिप्शन कुंजियों का समर्थन - ऑफ़लाइन हस्ताक्षर क्षमता - 4-byte लीज़ समाप्ति (8-byte की तुलना में) - अधिक लचीले विकल्प

**जावाडॉक:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet (I2P में गंतव्य तक पहुँच हेतु प्रकाशित रिकॉर्ड) के प्रकार

### Lease2 (I2P में Lease का नया संस्करण)

**विवरण:** 4-बाइट समाप्ति के साथ उन्नत लीज़ फ़ॉर्मेट। LeaseSet2 (प्रकार 3) और MetaLeaseSet (प्रकार 7) में प्रयुक्त।

**परिचय:** संस्करण 0.9.38 (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**कुल आकार:** 40 बाइट्स (मूल Lease (I2P में LeaseSet की एक प्रविष्टि) की तुलना में 4 बाइट्स छोटा)

**मूल Lease (I2P में इनबाउंड टनल की प्रविष्टि और उसकी समाप्ति समय का रिकॉर्ड) से तुलना:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**जावाडॉक:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### ऑफ़लाइन हस्ताक्षर

**Description:** पूर्व-हस्ताक्षरित अस्थायी कुंजियों के लिए वैकल्पिक संरचना, जो LeaseSet के प्रकाशन की अनुमति देती है, Destination (I2P में गंतव्य पहचान) की निजी हस्ताक्षर कुंजी तक ऑनलाइन पहुँच के बिना।

**परिचय:** संस्करण 0.9.38 (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**उद्देश्य:** - ऑफ़लाइन LeaseSet निर्माण को सक्षम बनाता है - Destination (I2P में पहचान/पता) की मास्टर कुंजी को ऑनलाइन उजागर होने से सुरक्षित रखता है - अस्थायी कुंजी को ऑफ़लाइन हस्ताक्षर के बिना नया LeaseSet प्रकाशित करके निरस्त किया जा सकता है

**उपयोग परिदृश्य:**

1. **उच्च-सुरक्षा गंतव्य:**
   - मास्टर हस्ताक्षर कुंजी ऑफ़लाइन संग्रहीत (HSM, कोल्ड स्टोरेज)
   - अस्थायी कुंजियाँ सीमित समय अवधियों के लिए ऑफ़लाइन उत्पन्न की जाती हैं
   - समझौता हुई अस्थायी कुंजी मास्टर कुंजी को उजागर नहीं करती

2. **एन्क्रिप्टेड LeaseSet प्रकाशन:**
   - EncryptedLeaseSet में ऑफ़लाइन हस्ताक्षर शामिल हो सकता है
   - ब्लाइंडेड सार्वजनिक कुंजी + ऑफ़लाइन हस्ताक्षर अतिरिक्त सुरक्षा प्रदान करते हैं

**सुरक्षा संबंधी विचार:**

1. **समाप्ति प्रबंधन:**
   - उचित समाप्ति अवधि निर्धारित करें (दिनों से सप्ताह तक, वर्षों नहीं)
   - समाप्ति से पहले नई अस्थायी कुंजियाँ उत्पन्न करें
   - कम समाप्ति अवधि = बेहतर सुरक्षा, अधिक रखरखाव

2. **कुंजी निर्माण:**
   - सुरक्षित परिवेश में ऑफ़लाइन अस्थायी कुंजियाँ उत्पन्न करें
   - ऑफ़लाइन मास्टर कुंजी से हस्ताक्षर करें
   - केवल हस्ताक्षरित अस्थायी कुंजी + हस्ताक्षर को ऑनलाइन router पर स्थानांतरित करें

3. **रद्दीकरण:**
   - अप्रत्यक्ष रूप से रद्द करने के लिए ऑफ़लाइन हस्ताक्षर के बिना नया LeaseSet प्रकाशित करें
   - या अलग transient key (अस्थायी कुंजी) के साथ नया LeaseSet प्रकाशित करें

**हस्ताक्षर सत्यापन:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**कार्यान्वयन संबंधी नोट्स:** - कुल आकार sigtype (हस्ताक्षर प्रकार) और Destination (I2P गंतव्य/पहचान) की साइनिंग कुंजी के प्रकार पर निर्भर करता है - न्यूनतम आकार: 4 + 2 + 32 (EdDSA कुंजी) + 64 (EdDSA हस्ताक्षर) = 102 बाइट्स - अधिकतम व्यावहारिक आकार: ~600 बाइट्स (RSA-4096 अस्थायी कुंजी + RSA-4096 हस्ताक्षर)

**के साथ संगत:** - LeaseSet2 (प्रकार 3) - EncryptedLeaseSet (प्रकार 5) - MetaLeaseSet (प्रकार 7)

**यह भी देखें:** [प्रस्ताव 123](/proposals/123-new-netdb-entries/) ऑफ़लाइन हस्ताक्षर प्रोटोकॉल के विस्तृत विवरण के लिए।

---

### LeaseSet2Header (LeaseSet2 का हेडर; I2P में किसी डेस्टिनेशन तक रूटिंग/पहुँच से संबंधित मेटाडेटा का भाग)

**विवरण:** LeaseSet2 (प्रकार 3) और MetaLeaseSet (प्रकार 7) के लिए साझा हेडर संरचना।

**परिचय:** संस्करण 0.9.38 (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**न्यूनतम कुल आकार:** 395 बाइट्स (ऑफ़लाइन हस्ताक्षर के बिना)

**फ्लैग परिभाषाएँ (बिट क्रम: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**फ्लैग विवरण:**

**बिट 0 - ऑफ़लाइन कुंजियाँ:** - `0`: कोई ऑफ़लाइन हस्ताक्षर नहीं, LeaseSet हस्ताक्षर को सत्यापित करने के लिए Destination (गंतव्य पहचान) की साइनिंग कुंजी का उपयोग करें - `1`: OfflineSignature संरचना फ्लैग्स फ़ील्ड के बाद आती है

**बिट 1 - अप्रकाशित:** - `0`: मानक प्रकाशित LeaseSet, जिसे floodfills तक प्रसारित किया जाना चाहिए - `1`: अप्रकाशित LeaseSet (केवल क्लाइंट-साइड)   - इसे प्रसारित, प्रकाशित, या क्वेरी के जवाब में भेजा नहीं जाना चाहिए   - यदि अवधि समाप्त हो जाए, तो प्रतिस्थापन के लिए netdb से क्वेरी न करें (जब तक बिट 2 भी सेट न हो)   - स्थानीय tunnels या परीक्षण के लिए उपयोग किया जाता है

**बिट 2 - ब्लाइंडेड (0.9.42 से):** - `0`: मानक LeaseSet - `1`: यह अनएन्क्रिप्टेड LeaseSet प्रकाशित होने पर ब्लाइंड किया जाएगा और एन्क्रिप्ट किया जाएगा   - प्रकाशित संस्करण EncryptedLeaseSet (type 5) होगा   - यदि समाप्त हो गया हो, तो प्रतिस्थापन के लिए netdb में **ब्लाइंडेड लोकेशन** को क्वेरी करें   - बिट 1 को भी 1 पर सेट करना आवश्यक है (अप्रकाशित + ब्लाइंडेड)   - एन्क्रिप्टेड हिडन सर्विसेज के लिए उपयोग किया जाता है

**समाप्ति सीमाएँ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**प्रकाशित टाइमस्टैम्प की आवश्यकताएँ:**

LeaseSet (प्रकार 1) में `published` फ़ील्ड नहीं था, इसलिए संस्करण निर्धारण के लिए सबसे शुरुआती लीज़-समाप्ति की खोज करनी पड़ती थी। LeaseSet2 1-सेकंड के रिज़ॉल्यूशन वाला स्पष्ट `published` टाइमस्टैम्प (समय-मुहर) जोड़ता है।

**महत्वपूर्ण कार्यान्वयन नोट:** - Routers को प्रति Destination (I2P गंतव्य पहचानकर्ता) प्रति सेकंड एक बार से भी **काफी धीमी** दर पर LeaseSet प्रकाशन को दर-सीमित करना अनिवार्य है - यदि उससे तेज़ प्रकाशित कर रहे हों, तो सुनिश्चित करें कि हर नए LeaseSet का `published` समय कम-से-कम 1 सेकंड बाद हो - यदि `published` समय वर्तमान संस्करण से नया नहीं है, तो Floodfills LeaseSet को अस्वीकार कर देंगे - सुझाया गया न्यूनतम अंतराल: प्रकाशनों के बीच 10-60 सेकंड

**गणना के उदाहरण:**

**LeaseSet2 (अधिकतम 11 मिनट):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (अधिकतम 18.2 घंटे):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**संस्करण प्रबंधन:** - यदि `published` टाइमस्टैम्प बड़ा हो तो LeaseSet को "नया" माना जाता है - Floodfills केवल सबसे नए संस्करण को संग्रहीत करते हैं और प्रसारित करते हैं - सावधानी रखें जब सबसे पुराना Lease (LeaseSet के भीतर की एक प्रविष्टि) पिछले LeaseSet के सबसे पुराने Lease से मेल खाता हो

---

### LeaseSet2 (प्रकार 3)

**विवरण:** कई एन्क्रिप्शन कुंजियों, ऑफ़लाइन हस्ताक्षरों और सेवा रिकॉर्ड्स के साथ आधुनिक LeaseSet प्रारूप। I2P की छिपी सेवाओं के लिए वर्तमान मानक।

**परिचय:** संस्करण 0.9.38 (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**संरचना:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**डेटाबेस भंडारण:** - **डेटाबेस प्रकार:** 3 - **कुंजी:** Destination (I2P में पते/पहचान की इकाई) का SHA-256 हैश - **मान:** पूर्ण LeaseSet2 संरचना

**हस्ताक्षर गणना:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### एन्क्रिप्शन कुंजी प्राथमिकता क्रम

**प्रकाशित (सर्वर) LeaseSet के लिए:** - कुंजियाँ सर्वर की प्राथमिकता के क्रम में सूचीबद्ध हैं (सबसे अधिक प्राथमिकता पहले) - एकाधिक प्रकारों का समर्थन करने वाले क्लाइंट्स को सर्वर की प्राथमिकता का सम्मान करना चाहिए - सूची में से पहले समर्थित प्रकार का चयन करें - आम तौर पर, उच्च नंबर वाले (नवीन) कुंजी प्रकार अधिक सुरक्षित/कुशल होते हैं - अनुशंसित क्रम: कुंजियों को टाइप कोड के उल्टे क्रम में सूचीबद्ध करें (नवीनतम पहले)

**उदाहरण सर्वर वरीयता:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**अप्रकाशित (क्लाइंट) LeaseSet के लिए:** - कुंजी क्रम व्यावहारिक रूप से मायने नहीं रखता (क्लाइंट की ओर कनेक्शन का प्रयास शायद ही कभी किया जाता है) - संगति के लिए उसी परंपरा का पालन करें

**क्लाइंट कुंजी चयन:** - सर्वर की वरीयता का सम्मान करें (पहला समर्थित प्रकार चुनें) - या कार्यान्वयन-परिभाषित वरीयता का उपयोग करें - या दोनों क्षमताओं के आधार पर संयुक्त वरीयता निर्धारित करें

### विकल्प मैपिंग

**आवश्यकताएँ:** - विकल्पों को कुंजी के आधार पर (lexicographic, UTF-8 byte order) अनिवार्य रूप से क्रमबद्ध किया जाना चाहिए - क्रमबद्धता से हस्ताक्षर की अपरिवर्तनशीलता सुनिश्चित होती है - डुप्लिकेट कुंजियाँ अनुमत नहीं हैं

**मानक प्रारूप ([प्रस्ताव 167](/proposals/167-service-records/)):**

API 0.9.66 (जून 2025, रिलीज़ 2.9.0) से, सेवा रिकॉर्ड विकल्प एक मानकीकृत प्रारूप का पालन करते हैं। पूर्ण विनिर्देश के लिए [प्रस्ताव 167](/proposals/167-service-records/) देखें।

**सेवा रिकॉर्ड विकल्प प्रारूप:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**उदाहरण सेवा रिकॉर्ड्स:**

**1. स्व-संदर्भित SMTP सर्वर:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. एकल बाहरी SMTP सर्वर:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. एकाधिक SMTP सर्वर (लोड बैलेंसिंग):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. ऐप विकल्पों के साथ HTTP सेवा:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**TTL (टाइम-टू-लाइव) सिफारिशें:** - न्यूनतम: 86400 सेकंड (1 दिन) - लंबी TTL netdb क्वेरी लोड को कम करती है - क्वेरी में कमी और सेवा अपडेट के प्रसार के बीच संतुलन - स्थिर सेवाओं के लिए: 604800 (7 दिन) या उससे अधिक

**कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **एन्क्रिप्शन कुंजियाँ (संस्करण 0.9.44 तक):**
   - ElGamal (प्रकार 0, 256 बाइट): लेगेसी संगतता
   - X25519 (प्रकार 4, 32 बाइट): वर्तमान मानक
   - MLKEM वेरिएंट: Post-quantum (क्वांटम-उपरांत; बीटा, अभी अंतिम रूप नहीं दिया गया)

2. **कुंजी लंबाई सत्यापन:**
   - Floodfills और क्लाइंट्स को अज्ञात कुंजी प्रकारों को पार्स करने में अनिवार्य रूप से सक्षम होना चाहिए
   - अज्ञात कुंजियों को छोड़ने के लिए keylen फ़ील्ड का उपयोग करें
   - यदि कुंजी प्रकार अज्ञात हो, तो पार्सिंग विफल न करें

3. **प्रकाशित टाइमस्टैम्प:**
   - रेट-लिमिटिंग के बारे में LeaseSet2Header नोट्स देखें
   - प्रकाशनों के बीच न्यूनतम 1-सेकंड का अंतराल
   - अनुशंसित: प्रकाशनों के बीच 10-60 सेकंड का अंतराल

4. **एन्क्रिप्शन प्रकार माइग्रेशन:**
   - एकाधिक कुंजियाँ क्रमिक माइग्रेशन का समर्थन करती हैं
   - संक्रमण अवधि के दौरान पुरानी और नई दोनों कुंजियों को सूचीबद्ध करें
   - पर्याप्त क्लाइंट उन्नयन अवधि के बाद पुरानी कुंजी हटा दें

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (मेटालीज़)

**विवरण:** MetaLeaseSet के लिए Lease संरचना, जो tunnels की बजाय अन्य LeaseSets को संदर्भित कर सकती है। लोड बैलेंसिंग और अतिरिक्तता के लिए उपयोग किया जाता है।

**परिचय:** संस्करण 0.9.38, 0.9.40 के लिए निर्धारित कार्यान्वयन (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**कुल आकार:** 40 बाइट्स

**प्रविष्टि प्रकार (फ्लैग्स के बिट 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**उपयोग परिदृश्य:**

1. **लोड बैलेंसिंग:**
   - कई MetaLease प्रविष्टियों वाला MetaLeaseSet
   - प्रत्येक प्रविष्टि अलग-अलग LeaseSet2 की ओर संकेत करती है
   - क्लाइंट लागत फ़ील्ड के आधार पर चयन करते हैं

2. **अतिरिक्तता:**
   - बैकअप LeaseSets की ओर इंगित करने वाली कई प्रविष्टियाँ
   - यदि प्राथमिक LeaseSet उपलब्ध न हो तो वैकल्पिक उपाय

3. **सेवा स्थानांतरण:**
   - MetaLeaseSet नए LeaseSet की ओर संकेत करता है
   - Destinations (I2P के गंतव्य) के बीच सुगम संक्रमण की अनुमति देता है

**कॉस्ट फ़ील्ड का उपयोग:** - कम कॉस्ट = अधिक प्राथमिकता - कॉस्ट 0 = सर्वोच्च प्राथमिकता - कॉस्ट 255 = न्यूनतम प्राथमिकता - क्लाइंट्स को कम कॉस्ट वाली प्रविष्टियों को प्राथमिकता देनी चाहिए (SHOULD) - समान कॉस्ट वाली प्रविष्टियों का लोड-बैलेंस यादृच्छिक रूप से किया जा सकता है

**Lease2 के साथ तुलना:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**जावाडॉक:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (प्रकार 7)

**विवरण:** MetaLease प्रविष्टियाँ रखने वाला LeaseSet का प्रकार, जो अन्य LeaseSets के लिए अप्रत्यक्ष संदर्भ प्रदान करता है। load balancing (ट्रैफ़िक का संतुलित वितरण), redundancy (विश्वसनीयता हेतु अतिरिक्त व्यवस्था), और service migration (सेवा को दूसरे स्थान/इंस्टेंस पर स्थानांतरित करना) के लिए उपयोग किया जाता है।

**परिचय:** 0.9.38 में परिभाषित, 0.9.40 में कार्यरत होने के लिए निर्धारित (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**स्थिति:** विनिर्देश पूर्ण है। उत्पादन परिनियोजन की स्थिति को वर्तमान I2P रिलीज़ के साथ सत्यापित किया जाना चाहिए।

**संरचना:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**डेटाबेस भंडारण:** - **डेटाबेस प्रकार:** 7 - **कुंजी:** Destination (I2P में गंतव्य पहचानकर्ता) का SHA-256 हैश - **मान:** पूर्ण MetaLeaseSet संरचना

**हस्ताक्षर की गणना:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**उपयोग परिदृश्य:**

**1. लोड बैलेंसिंग:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Failover (विफलता की स्थिति में स्वचालित रूप से बैकअप सिस्टम पर स्विच):**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. सेवा स्थानांतरण:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. बहु-स्तरीय आर्किटेक्चर:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**रद्दीकरण सूची:**

निरसन सूची MetaLeaseSet को पहले से प्रकाशित LeaseSets को स्पष्ट रूप से निरस्त करने की अनुमति देती है:

- **उद्देश्य:** विशिष्ट Destinations (I2P में गंतव्य/पता) को अब वैध नहीं के रूप में चिह्नित करना
- **सामग्री:** निरस्त Destination संरचनाओं के SHA-256 hashes
- **उपयोग:** क्लाइंट्स को उन LeaseSets का उपयोग बिल्कुल नहीं करना चाहिए जिनका Destination hash निरस्तीकरण सूची में आता है
- **प्रचलित मान:** अधिकांश परिनियोजनों में खाली (numr=0)

**रद्दीकरण का उदाहरण:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**समाप्ति प्रबंधन:**

MetaLeaseSet (I2P में LeaseSet का मेटा-रूप) अधिकतम expires=65535 सेकंड (~18.2 घंटे) के साथ LeaseSet2Header (LeaseSet v2 का हेडर) का उपयोग करता है:

- LeaseSet2 (अधिकतम ~11 मिनट) की तुलना में काफी लंबा
- तुलनात्मक रूप से स्थिर अप्रत्यक्षता के लिए उपयुक्त
- संदर्भित LeaseSets की समाप्ति अवधि छोटी हो सकती है
- क्लाइंट्स को MetaLeaseSet तथा संदर्भित LeaseSets दोनों की समाप्ति की जाँच करनी चाहिए

**विकल्प मैपिंग:**

- LeaseSet2 विकल्पों जैसा ही प्रारूप उपयोग करें
- सेवा रिकॉर्ड ([Proposal 167](/proposals/167-service-records/)) शामिल कर सकते हैं
- कुंजी के अनुसार क्रमबद्ध होना अनिवार्य है
- सेवा रिकॉर्ड आमतौर पर अंतिम सेवा का वर्णन करते हैं, न कि अप्रत्यक्षता संरचना का

**क्लाइंट कार्यान्वयन नोट्स:**

1. **रिज़ॉल्यूशन प्रक्रिया:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **कैशिंग:**
   - MetaLeaseSet (ऐसी संरचना जो कई LeaseSets का संदर्भ देती है) और संदर्भित LeaseSets दोनों को कैश करें
   - दोनों स्तरों की समाप्ति की जाँच करें
   - अद्यतन MetaLeaseSet प्रकाशन के लिए निगरानी करें

3. **फेलओवर:**
   - यदि पसंदीदा एंट्री विफल हो, तो अगली सबसे कम लागत वाली को आज़माएँ
   - असफल एंट्रियों को अस्थायी रूप से अनुपलब्ध के रूप में चिह्नित करने पर विचार करें
   - पुनर्प्राप्ति के लिए समय-समय पर फिर से जाँचें

**कार्यान्वयन स्थिति:**


**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (प्रकार 5)

**विवरण:** बेहतर गोपनीयता के लिए एन्क्रिप्टेड और ब्लाइंडेड LeaseSet। केवल ब्लाइंडेड सार्वजनिक कुंजी और मेटाडेटा दिखाई देते हैं; वास्तविक leases (I2P में टनल एक्सेस रिकॉर्ड) और एन्क्रिप्शन कुंजियाँ एन्क्रिप्ट की गई होती हैं।

**परिचय:** 0.9.38 में परिभाषित, 0.9.39 में कार्यरत (देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/))

**संरचना:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**डेटाबेस स्टोरेज:** - **डेटाबेस प्रकार:** 5 - **कुंजी:** **blinded Destination (I2P गंतव्य/पहचान)** का SHA-256 हैश (मूल Destination नहीं) - **मान:** पूर्ण EncryptedLeaseSet (एन्क्रिप्टेड leaseSet) संरचना

**LeaseSet2 की तुलना में महत्वपूर्ण अंतर:**

1. **LeaseSet2Header संरचना का उपयोग नहीं करता** (फ़ील्ड मिलते-जुलते हैं, लेकिन लेआउट अलग है)
2. **पूर्ण Destination (I2P गंतव्य पहचान) के बजाय ब्लाइंडेड सार्वजनिक कुंजी**
3. **सादा-पाठ लीज़ और कुंजियों के बजाय एन्क्रिप्टेड पेलोड**
4. **डेटाबेस कुंजी ब्लाइंडेड Destination का हैश है, मूल Destination नहीं**

**हस्ताक्षर की गणना:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**हस्ताक्षर प्रकार की आवश्यकता:**

**RedDSA_SHA512_Ed25519 (type 11) का उपयोग अनिवार्य है:** - 32-बाइट blinded सार्वजनिक कुंजियाँ - 64-बाइट हस्ताक्षर - blinding (हस्ताक्षर करते समय संदेश को हस्ताक्षरकर्ता से छुपाने की तकनीक) सुरक्षा गुणों के लिए आवश्यक - देखें [Red25519 विशिष्टता](//docs/specs/red25519-signature-scheme/

**EdDSA से प्रमुख अंतर:** - निजी कुंजियाँ modular reduction (मॉड्यूलो में घटाव; clamping नहीं) द्वारा - हस्ताक्षरों में 80 बाइट यादृच्छिक डेटा शामिल होता है - सार्वजनिक कुंजियों का सीधे उपयोग करता है (हैश नहीं) - सुरक्षित blinding ऑपरेशन सक्षम करता है (ब्लाइंडिंग: हस्ताक्षर करने से पहले संदेश/कुंजी को यादृच्छिकता से छुपाने की प्रक्रिया)

**Blinding (क्रिप्टोग्राफ़िक छिपाव) और कूटलेखन:**

विस्तृत जानकारी के लिए [EncryptedLeaseSet विनिर्देशन](/docs/specs/encryptedleaseset/) देखें:

**1. Key Blinding (कुंजी को ब्लाइंड/छिपाने की तकनीक):**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. डेटाबेस स्थान:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. एन्क्रिप्शन परतें (तीन-स्तरीय):**

**लेयर 1 - ऑथेंटिकेशन लेयर (क्लाइंट एक्सेस):** - एन्क्रिप्शन: ChaCha20 स्ट्रीम साइफर - की डेरिवेशन: HKDF, प्रत्येक क्लाइंट के लिए अलग सीक्रेट्स के साथ - प्रमाणित क्लाइंट बाहरी लेयर को डिक्रिप्ट कर सकते हैं

**परत 2 - एन्क्रिप्शन परत:** - एन्क्रिप्शन: ChaCha20 - कुंजी: क्लाइंट और सर्वर के बीच DH (Diffie-Hellman कुंजी-विनिमय) से व्युत्पन्न - इसमें वास्तविक LeaseSet2 या MetaLeaseSet शामिल है

**परत 3 - आंतरिक LeaseSet:** - पूर्ण LeaseSet2 या MetaLeaseSet - सभी tunnels, एन्क्रिप्शन कुंजियाँ, विकल्प शामिल - केवल सफल डिक्रिप्शन के बाद सुलभ

**एन्क्रिप्शन कुंजी व्युत्पत्ति:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**खोज प्रक्रिया:**

**अधिकृत क्लाइंट्स के लिए:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**अनधिकृत क्लाइंट्स के लिए:** - डिक्रिप्ट नहीं कर सकते, भले ही उन्हें EncryptedLeaseSet (एन्क्रिप्टेड leaseSet) मिल जाए - ब्लाइंडेड संस्करण से मूल Destination (I2P का गंतव्य पता) निर्धारित नहीं कर सकते - विभिन्न blinding periods (ब्लाइंडिंग अवधि; दैनिक रोटेशन) के बीच EncryptedLeaseSets को आपस में लिंक नहीं कर सकते

**समाप्ति समय:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**प्रकाशित टाइमस्टैम्प:**

LeaseSet2Header (I2P में LeaseSet v2 का हेडर) के समान आवश्यकताएँ: - प्रकाशनों के बीच समय में कम-से-कम 1 सेकंड की वृद्धि होनी चाहिए - यदि वर्तमान संस्करण से नया नहीं है तो Floodfills (I2P के netDb के विशेष नोड जो डेटा संग्रहित/वितरित करते हैं) अस्वीकार कर देंगे - अनुशंसित: प्रकाशनों के बीच 10-60 सेकंड

**एन्क्रिप्टेड LeaseSets (I2P में leaseSet: सेवा तक पहुँच के लिए उपयोग होने वाले इनबाउंड tunnel विवरणों का सेट) के साथ ऑफ़लाइन हस्ताक्षर:**

ऑफ़लाइन हस्ताक्षरों का उपयोग करते समय विशेष ध्यान देने योग्य बातें: - Blinded public key (ब्लाइंडेड सार्वजनिक कुंजी) प्रतिदिन बदलती है - ऑफ़लाइन हस्ताक्षर को नई blinded key के साथ प्रतिदिन पुनः उत्पन्न करना होगा - या अंदरूनी LeaseSet पर ऑफ़लाइन हस्ताक्षर का उपयोग करें, बाहरी EncryptedLeaseSet पर नहीं - नोट्स के लिए [Proposal 123](/proposals/123-new-netdb-entries/) देखें

**कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **क्लाइंट प्राधिकरण:**
   - कई क्लाइंट को अलग-अलग कुंजियों के साथ अधिकृत किया जा सकता है
   - प्रत्येक अधिकृत क्लाइंट के पास अद्वितीय डिक्रिप्शन प्रमाण-पत्र होते हैं
   - प्राधिकरण कुंजियाँ बदलकर क्लाइंट का प्राधिकरण रद्द करें

2. **दैनिक कुंजी रोटेशन:**
   - Blinded keys (ब्लाइंडेड कीज़—गोपनीयता हेतु छिपाई गई कुंजियाँ) UTC मध्यरात्रि पर बदलती हैं
   - क्लाइंट को प्रतिदिन blinded Destination (I2P में Destination—गंतव्य पहचान—का ब्लाइंडेड रूप) की पुनर्गणना करनी होती है
   - पुराने EncryptedLeaseSets रोटेशन के बाद खोज योग्य नहीं हो जाते

3. **गोपनीयता गुणधर्म:**
   - Floodfills मूल Destination (I2P का गंतव्य-पहचान ऑब्जेक्ट) का पता नहीं लगा सकते
   - अनधिकृत क्लाइंट सेवा तक पहुँच नहीं कर सकते
   - अलग-अलग blinding (पहचान छिपाने की तकनीक) अवधियों को आपस में जोड़ा नहीं जा सकता
   - समाप्ति समय से आगे कोई स्पष्ट-पाठ मेटाडेटा नहीं होता

4. **प्रदर्शन:**
   - क्लाइंट को दैनिक blinding (ब्लाइंडिंग) गणना करना आवश्यक है
   - त्रि-स्तरीय एन्क्रिप्शन गणनात्मक ओवरहेड बढ़ाता है
   - डिक्रिप्टेड आंतरिक LeaseSet को कैश करने पर विचार करें

**सुरक्षा संबंधी विचार:**

1. **प्राधिकरण कुंजी प्रबंधन:**
   - क्लाइंट प्राधिकरण प्रमाण-पत्रों को सुरक्षित रूप से वितरित करें
   - सूक्ष्म-स्तरीय रद्दीकरण के लिए प्रति क्लाइंट अद्वितीय प्रमाण-पत्रों का उपयोग करें
   - प्राधिकरण कुंजियों को नियमित अंतराल पर बदलें

2. **घड़ी समकालन:**
   - दैनिक blinding (गोपनीयता हेतु क्रिप्टोग्राफ़िक तकनीक) समकालित UTC तिथियों पर निर्भर करती है
   - घड़ी के समय में अंतर लुकअप विफलताओं का कारण बन सकता है
   - सहनशीलता के लिए पिछले/अगले दिन की blinding का समर्थन करने पर विचार करें

3. **मेटाडेटा का रिसाव:**
   - Published और expires फ़ील्ड स्पष्ट-पाठ में होते हैं
   - पैटर्न विश्लेषण सेवा की विशेषताओं का खुलासा कर सकता है
   - यदि चिंता हो तो प्रकाशन अंतराल को यादृच्छिक बनाएं

**JavaDoc प्रलेखन:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router संरचनाएँ

### RouterAddress (I2P router का transport पता, जिस पर अन्य routers उससे कनेक्ट होते हैं)

**विवरण:** एक विशिष्ट ट्रांसपोर्ट प्रोटोकॉल के माध्यम से किसी router के लिए कनेक्शन संबंधी जानकारी को परिभाषित करता है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**गंभीर - समाप्ति फ़ील्ड:**

⚠️ **समाप्ति फ़ील्ड को अनिवार्य रूप से सभी शून्य (8 शून्य बाइट्स) पर सेट किया जाना चाहिए।**

- **कारण:** रिलीज़ 0.9.3 से, गैर-शून्य Expiration (समाप्ति) के कारण हस्ताक्षर सत्यापन विफल हो जाता है
- **इतिहास:** Expiration मूल रूप से उपयोग में नहीं था, हमेशा null रहता था
- **वर्तमान स्थिति:** फ़ील्ड को 0.9.12 से फिर से पहचाना गया है, लेकिन नेटवर्क अपग्रेड का इंतज़ार करना होगा
- **कार्यान्वयन:** हमेशा 0x0000000000000000 पर सेट करें

किसी भी गैर-शून्य समाप्ति समय से RouterInfo के हस्ताक्षर का सत्यापन विफल हो जाएगा।

### परिवहन प्रोटोकॉल

**वर्तमान प्रोटोकॉल (2.10.0 तक):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**ट्रांसपोर्ट शैली मान:** - `"SSU2"`: वर्तमान UDP-आधारित ट्रांसपोर्ट - `"NTCP2"`: वर्तमान TCP-आधारित ट्रांसपोर्ट - `"NTCP"`: पुराना, हटाया गया (उपयोग न करें) - `"SSU"`: पुराना, हटाया गया (उपयोग न करें)

### सामान्य विकल्प

आमतौर पर सभी transports (ट्रांसपोर्ट प्रोटोकॉल) में निम्नलिखित शामिल होते हैं:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### SSU2-विशिष्ट विकल्प

पूर्ण विवरण के लिए [SSU2 विनिर्देश](/docs/specs/ssu2/) देखें।

**आवश्यक विकल्प:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**वैकल्पिक विकल्प:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**उदाहरण SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### NTCP2-विशिष्ट विकल्प

पूर्ण विवरण के लिए [NTCP2 विनिर्देश](/docs/specs/ntcp2/) देखें।

**आवश्यक विकल्प:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**वैकल्पिक विकल्प (0.9.50 से):**

```
"caps" = Capability string
```
**उदाहरण NTCP2 RouterAddress (router का पता):**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### कार्यान्वयन संबंधी टिप्पणियाँ

1. **लागत मान:**
   - UDP (SSU2) दक्षता के कारण आम तौर पर कम लागत (5-6)
   - TCP (NTCP2) ओवरहेड के कारण आम तौर पर अधिक लागत (10-11)
   - कम लागत = वरीय ट्रांसपोर्ट

2. **कई पते:**
   - Routers कई RouterAddress प्रविष्टियाँ प्रकाशित कर सकते हैं
   - विभिन्न transports (परिवहन प्रोटोकॉल) (SSU2 और NTCP2)
   - विभिन्न IP संस्करण (IPv4 और IPv6)
   - क्लाइंट लागत और क्षमताओं के आधार पर चयन करते हैं

3. **Hostname बनाम IP:**
   - प्रदर्शन के लिए IP पते को प्राथमिकता दें
   - होस्टनेम समर्थित हैं, लेकिन DNS लुकअप का अतिरिक्त ओवरहेड जोड़ते हैं
   - प्रकाशित RouterInfos के लिए IP का उपयोग करने पर विचार करें

4. **Base64 एन्कोडिंग:**
   - सभी कुंजियाँ और बाइनरी डेटा Base64 में एन्कोड किए गए हैं
   - मानक Base64 (RFC 4648)
   - padding (अतिरिक्त भराव) नहीं, और कोई गैर-मानक अक्षर नहीं

**JavaDoc (जावा दस्तावेज़ीकरण):** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**विवरण:** नेटवर्क डेटाबेस में संग्रहीत, किसी router के बारे में प्रकाशित संपूर्ण जानकारी। इसमें पहचान, पते और क्षमताएँ शामिल होती हैं।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**डेटाबेस स्टोरेज:** - **डेटाबेस प्रकार:** 0 - **कुंजी:** RouterIdentity (राउटर पहचान) का SHA-256 हैश - **मान:** पूर्ण RouterInfo (राउटर जानकारी) संरचना

**प्रकाशित टाइमस्टैम्प:** - 8-बाइट दिनांक (epoch से मिलीसेकंड) - RouterInfo वर्ज़निंग के लिए उपयोग होता है - Routers समय-समय पर नया RouterInfo प्रकाशित करते हैं - Floodfills प्रकाशित टाइमस्टैम्प के आधार पर नवीनतम संस्करण बनाए रखते हैं

**पता क्रमबद्धता:** - **ऐतिहासिक:** बहुत पुराने routers में उनके डेटा के SHA-256 के अनुसार पते क्रमबद्ध होना आवश्यक था - **वर्तमान:** क्रमबद्धता आवश्यक नहीं है, अनुकूलता के लिए इसे लागू करना सार्थक नहीं है - पते किसी भी क्रम में हो सकते हैं

**पीयर आकार फ़ील्ड (ऐतिहासिक):** - आधुनिक I2P में **हमेशा 0** - प्रतिबंधित मार्गों के लिए अभिप्रेत था (लागू नहीं किया गया) - लागू किया जाता, तो उसके बाद उतने Router Hashes आते - कुछ पुराने कार्यान्वयनों में क्रमबद्ध पीयर सूची की आवश्यकता हो सकती थी

**विकल्प मैपिंग:**

विकल्पों को कुंजी के अनुसार अनिवार्य रूप से क्रमबद्ध होना चाहिए। मानक विकल्पों में शामिल हैं:

**क्षमता विकल्प:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**नेटवर्क विकल्प:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**सांख्यिकीय विकल्प:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
मानक विकल्पों की पूरी सूची के लिए [Network Database RouterInfo दस्तावेज़](/docs/specs/common-structures/#routerInfo) देखें।

**हस्ताक्षर की गणना:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**सामान्य आधुनिक RouterInfo (Router की जानकारी):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **एकाधिक पते:**
   - Routers आमतौर पर 1-4 पते प्रकाशित करते हैं
   - IPv4 और IPv6 रूपांतर
   - SSU2 और/या NTCP2 ट्रांसपोर्ट
   - प्रत्येक पता स्वतंत्र होता है

2. **संस्करण-प्रबंधन:**
   - नवीनतर RouterInfo में `published` टाइमस्टैम्प अधिक हाल का होता है
   - Routers लगभग हर ~2 घंटे में या जब पते बदलते हैं, पुनर्प्रकाशित करते हैं
   - Floodfills केवल नवीनतम संस्करण को संग्रहीत करते हैं और उसी को प्रसारित करते हैं

3. **सत्यापन:**
   - RouterInfo (राउटर की जानकारी रिकॉर्ड) को स्वीकार करने से पहले हस्ताक्षर सत्यापित करें
   - प्रत्येक RouterAddress (राउटर पता) में समाप्ति फ़ील्ड सभी शून्य है, यह जाँचें
   - सत्यापित करें कि विकल्प मैपिंग कुंजी के अनुसार क्रमबद्ध है
   - जाँचें कि प्रमाणपत्र और कुंजी प्रकार ज्ञात/समर्थित हैं

4. **नेटवर्क डेटाबेस:**
   - Floodfills (विशेष routers जो नेटवर्क डेटाबेस प्रविष्टियों का संग्रह/वितरण करते हैं) Hash(RouterIdentity) द्वारा अनुक्रमित RouterInfo संग्रहीत करते हैं
   - अंतिम प्रकाशन के बाद ~2 दिनों तक संग्रहीत रहता है
   - Routers अन्य routers को खोजने के लिए floodfills से क्वेरी करते हैं

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## कार्यान्वयन संबंधी टिप्पणियाँ

### बाइट क्रम (Endianness—मेमोरी में बाइट्स की व्यवस्था)

**डिफ़ॉल्ट: Big-Endian (नेटवर्क बाइट ऑर्डर)**

अधिकांश I2P संरचनाएँ big-endian (जहाँ सबसे महत्वपूर्ण बाइट पहले आती है) बाइट क्रम का उपयोग करती हैं: - सभी पूर्णांक प्रकार (1-8 बाइट्स) - दिनांक टाइमस्टैम्प - TunnelId - स्ट्रिंग लंबाई प्रीफ़िक्स - प्रमाणपत्र प्रकार और लंबाइयाँ - कुंजी प्रकार कोड - मैपिंग आकार फ़ील्ड्स

**अपवाद: Little-Endian (कम-महत्त्व वाला बाइट पहले वाला बाइट क्रम)**

निम्नलिखित कुंजी प्रकार **little-endian** (कम-महत्त्वपूर्ण-बाइट-प्रथम क्रम) एन्कोडिंग का उपयोग करते हैं:
- **X25519** एन्क्रिप्शन कुंजियाँ (प्रकार 4)
- **EdDSA_SHA512_Ed25519** हस्ताक्षर कुंजियाँ (प्रकार 7)
- **EdDSA_SHA512_Ed25519ph** हस्ताक्षर कुंजियाँ (प्रकार 8)
- **RedDSA_SHA512_Ed25519** हस्ताक्षर कुंजियाँ (प्रकार 11)

**कार्यान्वयन:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### संरचना का संस्करण निर्धारण

**कभी भी स्थिर आकार मानकर न चलें:**

कई संरचनाओं की लंबाई परिवर्तनीय होती है: - RouterIdentity (राउटर की पहचान): 387+ बाइट्स (हमेशा 387 नहीं) - Destination (गंतव्य): 387+ बाइट्स (हमेशा 387 नहीं) - LeaseSet2 (LeaseSet का दूसरा संस्करण): लंबाई में काफी भिन्नता होती है - Certificate (प्रमाणपत्र): 3+ बाइट्स

**हमेशा आकार फ़ील्ड पढ़ें:** - प्रमाणपत्र की लंबाई बाइट्स 1-2 पर - शुरुआत में मैपिंग का आकार - KeysAndCert का मान हमेशा 384 + 3 + certificate_length के रूप में गणना करें

**अतिरिक्त डेटा की जाँच करें:** - मान्य संरचनाओं के बाद आने वाले अनावश्यक डेटा को रोकें - सत्यापित करें कि प्रमाणपत्रों की लंबाई कुंजी प्रकारों से मेल खाती है - स्थिर आकार के प्रकारों के लिए अपेक्षित सटीक लंबाइयों को अनिवार्य करें

### वर्तमान अनुशंसाएँ (अक्टूबर 2025)

**नई Router पहचानों के लिए:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/hi/proposals/161-ri-dest-padding/)
```
**नए गंतव्यों के लिए:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/hi/proposals/161-ri-dest-padding/)
```
**नए LeaseSets के लिए:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**एन्क्रिप्टेड सेवाओं के लिए:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### अप्रचलित विशेषताएँ - उपयोग न करें

**अप्रचलित एन्क्रिप्शन:** - ElGamal (प्रकार 0) Router पहचानों के लिए (0.9.58 में अप्रचलित) - ElGamal/AES+SessionTag एन्क्रिप्शन (ECIES-X25519 का उपयोग करें)

**अप्रचलित साइनिंग:** - DSA_SHA1 (प्रकार 0) Router पहचानें के लिए (0.9.58 से अप्रचलित) - ECDSA वैरिएंट (प्रकार 1-3) नए कार्यान्वयनों के लिए - RSA वैरिएंट (प्रकार 4-6) SU3 फ़ाइलों को छोड़कर

**अप्रचलित नेटवर्क फ़ॉर्मेट:** - LeaseSet प्रकार 1 (LeaseSet2 का उपयोग करें) - Lease (I2P रिकॉर्ड, 44 बाइट्स, Lease2 का उपयोग करें) - मूल Lease की समाप्ति का फ़ॉर्मेट

**अप्रचलित ट्रांसपोर्ट्स:** - NTCP (0.9.50 में हटाया गया) - SSU (2.4.0 में हटाया गया)

**अप्रचलित प्रमाणपत्र:** - HASHCASH (प्रकार 1) - HIDDEN (प्रकार 2) - SIGNED (प्रकार 3) - MULTIPLE (прकार 4)

### सुरक्षा संबंधी विचार

**कुंजी निर्माण:** - हमेशा क्रिप्टोग्राफ़िक रूप से सुरक्षित यादृच्छिक संख्या जनरेटर का उपयोग करें - विभिन्न संदर्भों में कुंजियों का पुन: उपयोग कभी न करें - उपयुक्त अभिगम नियंत्रणों के साथ निजी कुंजियों की सुरक्षा करें - समाप्त होने पर मेमोरी से कुंजी सामग्री को सुरक्षित रूप से मिटा दें

**हस्ताक्षर सत्यापन:** - डेटा पर भरोसा करने से पहले हमेशा हस्ताक्षरों को सत्यापित करें - जांचें कि हस्ताक्षर की लंबाई कुंजी प्रकार से मेल खाती है - सुनिश्चित करें कि हस्ताक्षरित डेटा में अपेक्षित फ़ील्ड शामिल हैं - क्रमबद्ध mappings (मैपिंग्स) के लिए, हस्ताक्षर करने/सत्यापित करने से पहले छँटाई क्रम सत्यापित करें

**टाइमस्टैम्प सत्यापन:** - यह जाँचें कि प्रकाशित समय उचित हैं (बहुत दूर भविष्य में नहीं) - यह सत्यापित करें कि लीज़ की समाप्ति तिथियाँ अभी समाप्त नहीं हुई हैं - घड़ी के विचलन की सहिष्णुता पर विचार करें (±30 सेकंड सामान्य)

**नेटवर्क डेटाबेस:** - संग्रहित करने से पहले सभी संरचनाओं को सत्यापित करें - DoS रोकने के लिए आकार सीमाएँ लागू करें - क्वेरियों और प्रकाशनों पर दर-सीमा लागू करें - सत्यापित करें कि डेटाबेस कुंजियाँ संरचना हैश से मेल खाती हैं

### संगतता नोट्स

**पिछली संगतता:** - पुराने routers के लिए ElGamal और DSA_SHA1 अब भी समर्थित हैं - अप्रचलित कुंजी प्रकार कार्यशील तो हैं, लेकिन अनुशंसित नहीं हैं - कंप्रेस करने योग्य पैडिंग ([प्रस्ताव 161](/hi/proposals/161-ri-dest-padding/)) 0.6 तक पिछली संगतता रखती है

**Forward Compatibility (भविष्य संस्करणों के साथ संगतता):** - अज्ञात कुंजी प्रकारों को लंबाई फ़ील्ड्स का उपयोग करके पार्स किया जा सकता है - अज्ञात प्रमाणपत्र प्रकारों को लंबाई का उपयोग करके छोड़ा जा सकता है - अज्ञात हस्ताक्षर प्रकारों को सुगमता से संभाला जाना चाहिए - कार्यान्वयन को अज्ञात वैकल्पिक विशेषताओं पर विफल नहीं होना चाहिए

**माइग्रेशन रणनीतियाँ:** - संक्रमण के दौरान पुराने और नए दोनों कुंजी प्रकारों का समर्थन - LeaseSet2 कई एन्क्रिप्शन कुंजियों की सूची दे सकता है - ऑफ़लाइन हस्ताक्षर सुरक्षित कुंजी रोटेशन सक्षम करते हैं - MetaLeaseSet (पारदर्शी सेवा माइग्रेशन के लिए संरचना) सेवा माइग्रेशन को पारदर्शी बनाता है

### परीक्षण और सत्यापन

**संरचना सत्यापन:** - सत्यापित करें कि सभी लंबाई फ़ील्ड अपेक्षित सीमाओं के भीतर हैं - जाँचें कि चर-लंबाई वाली संरचनाएँ सही ढंग से पार्स होती हैं - सुनिश्चित करें कि हस्ताक्षरों का सत्यापन सफल है - न्यूनतम और अधिकतम आकार वाली संरचनाओं दोनों के साथ परीक्षण करें

**सीमांत मामले:** - शून्य-लंबाई स्ट्रिंग्स - खाली मैपिंग्स - lease (I2P में रूटिंग रिकॉर्ड) की न्यूनतम और अधिकतम संख्या - शून्य-लंबाई पेलोड वाला प्रमाणपत्र - बहुत बड़ी संरचनाएँ (अधिकतम आकार के निकट)

**अंतरसंचालनीयता:** - आधिकारिक Java I2P कार्यान्वयन के विरुद्ध परीक्षण करें - i2pd के साथ अनुकूलता की जाँच करें - विभिन्न नेटवर्क डेटाबेस सामग्री के साथ परीक्षण करें - ज्ञात-सही परीक्षण वेक्टरों के साथ सत्यापन करें

---

## संदर्भ

### विनिर्देश

- [I2NP प्रोटोकॉल](/docs/specs/i2np/)
- [I2CP प्रोटोकॉल](/docs/specs/i2cp/)
- [SSU2 ट्रांसपोर्ट](/docs/specs/ssu2/)
- [NTCP2 ट्रांसपोर्ट](/docs/specs/ntcp2/)
- [Tunnel प्रोटोकॉल](/docs/specs/implementation/)
- [डेटाग्राम प्रोटोकॉल](/docs/api/datagrams/)

### कूटलेखन

- [क्रिप्टोग्राफ़ी का अवलोकन](/docs/specs/cryptography/)
- [ElGamal/AES एन्क्रिप्शन](/docs/legacy/elgamal-aes/)
- [ECIES-X25519 एन्क्रिप्शन (ECIES: एलिप्टिक कर्व एकीकृत एन्क्रिप्शन स्कीम)](/docs/specs/ecies/)
- [Routers के लिए ECIES](/docs/specs/ecies/#routers)
- [ECIES हाइब्रिड (पोस्ट-क्वांटम)](/docs/specs/ecies/#hybrid)
- [Red25519 हस्ताक्षर](/docs/specs/red25519-signature-scheme/)
- [एन्क्रिप्टेड LeaseSet](/docs/specs/encryptedleaseset/)

### प्रस्ताव

- [प्रस्ताव 123: netDB में नई प्रविष्टियाँ](/proposals/123-new-netdb-entries/)
- [प्रस्ताव 134: GOST हस्ताक्षर प्रकार](/proposals/134-gost/)
- [प्रस्ताव 136: प्रायोगिक हस्ताक्षर प्रकार](/proposals/136-experimental-sigtypes/)
- [प्रस्ताव 145: ECIES-P256](/proposals/145-ecies/)
- [प्रस्ताव 156: ECIES Routers](/proposals/156-ecies-routers/)
- [प्रस्ताव 161: Padding (पैडिंग/भराई) निर्माण](/hi/proposals/161-ri-dest-padding/)
- [प्रस्ताव 167: सेवा रिकॉर्ड](/proposals/167-service-records/)
- [प्रस्ताव 169: पोस्ट-क्वांटम क्रिप्टोग्राफी](/proposals/169-pq-crypto/)
- [सभी प्रस्तावों की सूची](/proposals/)

### नेटवर्क डेटाबेस

- [नेटवर्क डेटाबेस का अवलोकन](/docs/specs/common-structures/)
- [RouterInfo मानक विकल्प](/docs/specs/common-structures/#routerInfo)

### JavaDoc API संदर्भ

- [कोर डेटा पैकेज](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### बाहरी मानक

- **RFC 7748 (X25519):** सुरक्षा के लिए एलिप्टिक कर्व्स
- **RFC 7539 (ChaCha20):** IETF प्रोटोकॉल्स के लिए ChaCha20 और Poly1305
- **RFC 4648 (Base64):** Base16, Base32, और Base64 डेटा एन्कोडिंग्स
- **FIPS 180-4 (SHA-256):** सुरक्षित हैश मानक
- **FIPS 204 (ML-DSA):** Module-Lattice-Based Digital Signature Standard (मॉड्यूल-लैटिस-आधारित डिजिटल हस्ताक्षर मानक)
- [IANA सेवा रजिस्ट्री](http://www.dns-sd.org/ServiceTypes.html)

### सामुदायिक संसाधन

- [I2P वेबसाइट](/)
- [I2P फ़ोरम](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P GitHub मिरर](https://github.com/i2p/i2p.i2p)
- [तकनीकी प्रलेखन सूचकांक](/docs/)

### रिलीज़ जानकारी

- [I2P 2.10.0 रिलीज़](/hi/blog/2025/09/08/i2p-2.10.0-release/)
- [रिलीज़ इतिहास](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [चेंजलॉग](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## परिशिष्ट: त्वरित संदर्भ तालिकाएँ

### कुंजी प्रकार त्वरित संदर्भ

**वर्तमान मानक (सभी नए कार्यान्वयनों के लिए अनुशंसित):** - **एन्क्रिप्शन:** X25519 (प्रकार 4, 32 बाइट, लिटिल-एंडियन) - **हस्ताक्षर:** EdDSA_SHA512_Ed25519 (प्रकार 7, 32 बाइट, लिटिल-एंडियन)

**लेगेसी (समर्थित लेकिन अप्रचलित):** - **एन्क्रिप्शन:** ElGamal (type 0, 256 बाइट्स, big-endian (सबसे महत्त्वपूर्ण बाइट पहले वाला क्रम)) - **साइनिंग:** DSA_SHA1 (type 0, 20-बाइट निजी / 128-बाइट सार्वजनिक, big-endian)

**विशेषीकृत:** - **हस्ताक्षर (एन्क्रिप्टेड LeaseSet):** RedDSA_SHA512_Ed25519 (प्रकार 11, 32 बाइट, little-endian (कम-महत्वपूर्ण बाइट पहले))

**पोस्ट-क्वांटम (बीटा, अंतिम रूप नहीं दिया गया):** - **हाइब्रिड एन्क्रिप्शन:** MLKEM_X25519 वेरिएंट्स (प्रकार 5-7) - **शुद्ध PQ (पोस्ट-क्वांटम) एन्क्रिप्शन:** MLKEM वेरिएंट्स (अभी प्रकार कोड आवंटित नहीं किए गए हैं)

### संरचना आकार त्वरित संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### डेटाबेस प्रकार त्वरित संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### ट्रांसपोर्ट प्रोटोकॉल त्वरित संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### संस्करण माइलस्टोन त्वरित संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/hi/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
