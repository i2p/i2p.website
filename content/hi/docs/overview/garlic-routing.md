---
title: "गार्लिक रूटिंग (Garlic Routing)"
description: "I2P में garlic routing शब्दावली, आर्किटेक्चर, और आधुनिक कार्यान्वयन को समझना"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. अवलोकन

**Garlic routing** I2P की मुख्य नवाचारों में से एक है, जो स्तरित एन्क्रिप्शन, संदेश बंडलिंग और एकदिशात्मक tunnels को संयोजित करती है। हालांकि अवधारणात्मक रूप से **onion routing** के समान, यह मॉडल को विस्तारित करती है और एकल लिफाफे ("garlic") में कई एन्क्रिप्टेड संदेशों ("cloves") को बंडल करती है, जिससे दक्षता और गुमनामी में सुधार होता है।

*garlic routing* शब्द को [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) द्वारा [Roger Dingledine's Free Haven Master's Thesis](https://www.freehaven.net/papers.html) (जून 2000, §8.1.1) में गढ़ा गया था। I2P डेवलपर्स ने 2000 के दशक की शुरुआत में इस शब्द को अपनाया ताकि इसके बंडलिंग संवर्द्धन और एकदिशात्मक परिवहन मॉडल को दर्शाया जा सके, जो इसे Tor के circuit‑switched डिज़ाइन से अलग करता है।

> **सारांश:** Garlic routing = स्तरित एन्क्रिप्शन + संदेश बंडलिंग + एकदिशीय tunnels के माध्यम से गुमनाम वितरण।

---

## 2. "Garlic" शब्दावली

ऐतिहासिक रूप से, I2P के भीतर *garlic* शब्द का उपयोग तीन अलग-अलग संदर्भों में किया गया है:

1. **स्तरित एन्क्रिप्शन** – tunnel-स्तरीय onion-शैली सुरक्षा  
2. **एकाधिक संदेशों को बंडल करना** – एक "garlic message" के अंदर कई "cloves"  
3. **End-to-end एन्क्रिप्शन** – पूर्व में *ElGamal/AES+SessionTags*, अब *ECIES‑X25519‑AEAD‑Ratchet*

जबकि आर्किटेक्चर बरकरार है, एन्क्रिप्शन योजना को पूरी तरह से आधुनिक बनाया गया है।

---

## 3. स्तरित एन्क्रिप्शन

Garlic routing अपने मूलभूत सिद्धांत को onion routing के साथ साझा करता है: प्रत्येक router केवल एन्क्रिप्शन की एक परत को डिक्रिप्ट करता है, केवल अगले hop को जानता है और पूर्ण पथ को नहीं।

हालांकि, I2P **unidirectional tunnels** (एकदिशीय सुरंगों) को लागू करता है, bidirectional circuits नहीं:

- **Outbound tunnel**: निर्माता से संदेश भेजता है  
- **Inbound tunnel**: निर्माता को वापस संदेश लाता है

एक पूर्ण राउंड ट्रिप (Alice ↔ Bob) चार tunnels का उपयोग करती है: Alice की outbound → Bob की inbound, फिर Bob की outbound → Alice की inbound। यह डिज़ाइन द्विदिशात्मक सर्किट की तुलना में **सहसंबंध डेटा एक्सपोज़र को आधा कर देता है**।

टनल कार्यान्वयन विवरण के लिए, [Tunnel Specification](/docs/specs/implementation) और [Tunnel Creation (ECIES)](/docs/specs/implementation) स्पेसिफिकेशन देखें।

---

## 4. एकाधिक संदेशों को बंडल करना ("Cloves")

Freedman की मूल garlic routing ने एक संदेश के भीतर कई एन्क्रिप्टेड "bulbs" को बंडल करने की कल्पना की थी। I2P इसे **garlic message** के अंदर **cloves** के रूप में लागू करता है — प्रत्येक clove के पास अपने स्वयं के एन्क्रिप्टेड डिलीवरी निर्देश और लक्ष्य (router, destination, या tunnel) होते हैं।

Garlic bundling I2P को निम्नलिखित करने की अनुमति देता है:

- डेटा संदेशों के साथ पावतियों और मेटाडेटा को संयोजित करें
- दिखाई देने वाले ट्रैफ़िक पैटर्न को कम करें
- अतिरिक्त कनेक्शन के बिना जटिल संदेश संरचनाओं का समर्थन करें

![Garlic Message Cloves](/images/garliccloves.png)   *चित्र 1: एक Garlic Message जिसमें कई cloves हैं, प्रत्येक के अपने delivery instructions के साथ।*

विशिष्ट लौंग में शामिल हैं:

1. **डिलीवरी स्टेटस मैसेज** — डिलीवरी की सफलता या विफलता की पुष्टि करने वाली acknowledgments।  
   इन्हें गोपनीयता बनाए रखने के लिए अपनी garlic परत में लपेटा जाता है।
2. **डेटाबेस स्टोर मैसेज** — स्वचालित रूप से बंडल किए गए LeaseSets ताकि peers बिना netDb को फिर से क्वेरी किए जवाब दे सकें।

लौंग को बंडल किया जाता है जब:

- एक नया LeaseSet प्रकाशित किया जाना चाहिए
- नए session tags वितरित किए जाते हैं
- हाल ही में कोई बंडल नहीं हुआ है (~1 मिनट डिफ़ॉल्ट रूप से)

Garlic messages एक ही पैकेट में कई एन्क्रिप्टेड घटकों की कुशल एंड-टू-एंड डिलीवरी प्राप्त करते हैं।

---

## 5. एन्क्रिप्शन का विकास

### 5.1 Historical Context

प्रारंभिक दस्तावेज़ीकरण (≤ v0.9.12) में *ElGamal/AES+SessionTags* एन्क्रिप्शन का वर्णन किया गया था:   - **ElGamal 2048‑bit** ने AES session keys को लपेटा   - **AES‑256/CBC** पेलोड एन्क्रिप्शन के लिए   - 32‑बाइट session tags प्रति संदेश एक बार उपयोग किए गए

वह क्रिप्टोसिस्टम **पुराना हो चुका है**।

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

2019 और 2023 के बीच, I2P पूरी तरह से ECIES‑X25519‑AEAD‑Ratchet में स्थानांतरित हो गया। आधुनिक स्टैक निम्नलिखित घटकों को मानकीकृत करता है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
ECIES माइग्रेशन के लाभ:

- **Forward secrecy** प्रति-संदेश ratcheting keys के माध्यम से  
- ElGamal की तुलना में **कम payload size**  
- क्रिप्टोएनालिटिक प्रगति के खिलाफ **लचीलापन**  
- भविष्य के post-quantum hybrids के साथ **संगतता** (Proposal 169 देखें)

अतिरिक्त विवरण: [ECIES विशिष्टता](/docs/specs/ecies) और [EncryptedLeaseSet विशिष्टता](/docs/specs/encryptedleaseset) देखें।

---

## 6. LeaseSets and Garlic Bundling

Garlic envelopes में अक्सर गंतव्य की पहुँच को प्रकाशित या अपडेट करने के लिए LeaseSets शामिल होते हैं।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
सभी LeaseSets विशेष routers द्वारा बनाए रखे गए *floodfill DHT* के माध्यम से वितरित किए जाते हैं। प्रकाशनों को सत्यापित, टाइमस्टैम्प और दर-सीमित किया जाता है ताकि मेटाडेटा सहसंबंध को कम किया जा सके।

विवरण के लिए [Network Database दस्तावेज़](/docs/specs/common-structures) देखें।

---

## 7. Modern “Garlic” Applications within I2P

I2P प्रोटोकॉल स्टैक में garlic-based एन्क्रिप्शन और मैसेज बंडलिंग का उपयोग किया जाता है:

1. **Tunnel निर्माण और उपयोग** — प्रत्येक hop के लिए स्तरित एन्क्रिप्शन  
2. **End-to-end संदेश वितरण** — cloned-acknowledgment और LeaseSet cloves के साथ बंडल किए गए garlic messages  
3. **Network Database प्रकाशन** — गोपनीयता के लिए garlic envelopes में लिपटे LeaseSets  
4. **SSU2 और NTCP2 transports** — Noise फ्रेमवर्क और X25519/ChaCha20 primitives का उपयोग करके underlay एन्क्रिप्शन

Garlic routing इस प्रकार एक *एन्क्रिप्शन लेयरिंग की विधि* और एक *नेटवर्क मैसेजिंग मॉडल* दोनों है।

---

## 6. LeaseSets और Garlic Bundling

I2P का दस्तावेज़ीकरण केंद्र [यहाँ उपलब्ध है](/docs/), जिसे निरंतर बनाए रखा जाता है। प्रासंगिक सक्रिय विनिर्देशों में शामिल हैं:

- [ECIES Specification](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel Creation (ECIES)](/docs/specs/implementation) — आधुनिक tunnel निर्माण प्रोटोकॉल
- [I2NP Specification](/docs/specs/i2np) — I2NP संदेश प्रारूप
- [SSU2 Specification](/docs/specs/ssu2) — SSU2 UDP परिवहन
- [Common Structures](/docs/specs/common-structures) — netDb और floodfill व्यवहार

शैक्षणिक सत्यापन: Hoang et al. (IMC 2018, USENIX FOCI 2019) और Muntaka et al. (2025) I2P की डिज़ाइन की संरचनात्मक स्थिरता और परिचालन लचीलापन की पुष्टि करते हैं।

---

## 7. I2P के भीतर आधुनिक "Garlic" अनुप्रयोग

चल रहे प्रस्ताव:

- **प्रस्ताव 169:** हाइब्रिड पोस्ट-क्वांटम (ML-KEM 512/768/1024 + X25519)  
- **प्रस्ताव 168:** Transport बैंडविड्थ अनुकूलन  
- **डेटाग्राम और स्ट्रीमिंग अपडेट:** उन्नत कंजेशन प्रबंधन

भविष्य के अनुकूलन में अतिरिक्त संदेश विलंब रणनीतियाँ या garlic-message स्तर पर बहु-tunnel अतिरेक शामिल हो सकते हैं, जो Freedman द्वारा मूल रूप से वर्णित अप्रयुक्त डिलीवरी विकल्पों पर आधारित होंगे।

---

## 8. वर्तमान दस्तावेज़ीकरण और संदर्भ

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
