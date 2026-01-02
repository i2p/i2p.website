---
title: "अपने एप्लिकेशन में I2P एम्बेड करना"
description: "अपने ऐप के साथ I2P router को जिम्मेदारी से बंडल करने के लिए अपडेट की गई व्यावहारिक मार्गदर्शिका"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

अपने एप्लिकेशन के साथ I2P को बंडल करना उपयोगकर्ताओं को जोड़ने का एक शक्तिशाली तरीका है—लेकिन केवल तभी जब router को जिम्मेदारी से कॉन्फ़िगर किया गया हो।

## 1. Router टीमों के साथ समन्वय करें

- बंडलिंग से पहले **Java I2P** और **i2pd** के मेंटेनर्स से संपर्क करें। वे आपके डिफ़ॉल्ट्स की समीक्षा कर सकते हैं और संगतता संबंधी चिंताओं को उजागर कर सकते हैं।
- अपने स्टैक के अनुसार router implementation चुनें:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **अन्य भाषाएं** → एक router बंडल करें और [SAM v3](/docs/api/samv3/) या [I2CP](/docs/specs/i2cp/) का उपयोग करके इंटीग्रेट करें
- router बाइनरीज़ और डिपेंडेंसीज़ (Java runtime, ICU, आदि) के लिए पुनर्वितरण शर्तों की पुष्टि करें।

## 2. अनुशंसित कॉन्फ़िगरेशन डिफ़ॉल्ट

"आप जितना उपभोग करते हैं उससे अधिक योगदान करें" का लक्ष्य रखें। आधुनिक डिफ़ॉल्ट सेटिंग्स नेटवर्क के स्वास्थ्य और स्थिरता को प्राथमिकता देती हैं।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### भाग लेने वाली Tunnels आवश्यक बनी रहती हैं

भाग लेने वाली tunnels को **बंद न करें**।

1. जो राउटर रिले नहीं करते वे स्वयं खराब प्रदर्शन करते हैं।
2. नेटवर्क स्वैच्छिक क्षमता साझाकरण पर निर्भर करता है।
3. कवर ट्रैफिक (रिले किया गया ट्रैफिक) गुमनामी में सुधार करता है।

**आधिकारिक न्यूनतम:** - साझा बैंडविड्थ: ≥ 12 KB/s   - Floodfill स्वतः ऑप्ट-इन: ≥ 128 KB/s   - अनुशंसित: 2 inbound / 2 outbound tunnels (Java I2P डिफ़ॉल्ट)

## 3. स्थिरता और रीसीडिंग

स्थायी स्टेट डायरेक्टरियाँ (`netDb/`, प्रोफाइल, सर्टिफिकेट्स) को रन्स के बीच संरक्षित रखा जाना चाहिए।

persistence के बिना, आपके उपयोगकर्ता हर स्टार्टअप पर reseed ट्रिगर करेंगे—जिससे प्रदर्शन खराब होगा और reseed सर्वर पर लोड बढ़ेगा।

यदि persistence (स्थायी भंडारण) संभव नहीं है (उदाहरण के लिए, containers या अस्थायी इंस्टॉल):

1. इंस्टॉलर में **1,000–2,000 router infos** बंडल करें।
2. सार्वजनिक सर्वरों पर भार कम करने के लिए एक या अधिक कस्टम reseed सर्वर संचालित करें।

कॉन्फ़िगरेशन वेरिएबल: - बेस डायरेक्टरी: `i2p.dir.base` - कॉन्फ़िग डायरेक्टरी: `i2p.dir.config` - reseeding के लिए `certificates/` शामिल करें।

## 4. सुरक्षा और एक्सपोज़र

- Router console (`127.0.0.1:7657`) को केवल स्थानीय रखें।
- UI को बाहरी रूप से उजागर करते समय HTTPS का उपयोग करें।
- जब तक आवश्यक न हो, बाहरी SAM/I2CP को अक्षम करें।
- शामिल plugins की समीक्षा करें—केवल वही भेजें जो आपका ऐप समर्थन करता है।
- रिमोट console एक्सेस के लिए हमेशा प्रमाणीकरण शामिल करें।

**2.5.0 के बाद से शामिल की गई सुरक्षा सुविधाएं:** - एप्लिकेशन के बीच NetDB अलगाव (2.4.0+)   - DoS शमन और Tor ब्लॉकलिस्ट (2.5.1)   - NTCP2 प्रोबिंग प्रतिरोध (2.9.0)   - Floodfill router चयन में सुधार (2.6.0+)

## 5. समर्थित APIs (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
सभी आधिकारिक दस्तावेज़ `/docs/api/` के अंतर्गत स्थित हैं — पुराना `/spec/samv3/` पथ मौजूद **नहीं** है।

## 6. नेटवर्किंग और पोर्ट्स

विशिष्ट डिफ़ॉल्ट पोर्ट: - 4444 – HTTP प्रॉक्सी   - 4445 – HTTPS प्रॉक्सी   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router Console   - 7658 – लोकल I2P साइट   - 6668 – IRC प्रॉक्सी   - 9000–31000 – रैंडम router पोर्ट (UDP/TCP इनबाउंड)

राउटर पहली बार चलने पर एक यादृच्छिक इनबाउंड पोर्ट चुनते हैं। फ़ॉरवर्डिंग प्रदर्शन में सुधार करती है, लेकिन UPnP इसे स्वचालित रूप से संभाल सकता है।

## 7. आधुनिक परिवर्तन (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. उपयोगकर्ता अनुभव और परीक्षण

- I2P क्या करता है और बैंडविड्थ क्यों साझा की जाती है, यह संप्रेषित करें।
- router डायग्नोस्टिक्स प्रदान करें (बैंडविड्थ, tunnels, reseed स्थिति)।
- Windows, macOS, और Linux पर बंडल्स का परीक्षण करें (कम-RAM शामिल)।
- **Java I2P** और **i2pd** peers दोनों के साथ इंटरऑप की पुष्टि करें।
- नेटवर्क ड्रॉप्स और ungraceful exits से रिकवरी का परीक्षण करें।

## 9. समुदाय संसाधन

- फोरम: [i2pforum.net](https://i2pforum.net) या I2P के अंदर `http://i2pforum.i2p`।
- कोड: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p)।
- IRC (Irc2P नेटवर्क): `#i2p-dev`, `#i2pd`।
  - `#i2papps` अप्रमाणित; हो सकता है कि मौजूद न हो।
  - स्पष्ट करें कि कौन सा नेटवर्क (Irc2P बनाम ilita.i2p) आपके चैनल को होस्ट करता है।

जिम्मेदारी से एम्बेड करने का मतलब है उपयोगकर्ता अनुभव, प्रदर्शन और नेटवर्क योगदान के बीच संतुलन बनाना। इन डिफॉल्ट्स का उपयोग करें, router रखरखावकर्ताओं के साथ समन्वय बनाए रखें, और रिलीज़ से पहले वास्तविक-विश्व लोड के तहत परीक्षण करें।
