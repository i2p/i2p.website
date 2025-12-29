---
title: "Tunnel संचालन मार्गदर्शिका"
description: "I2P tunnels के निर्माण, तथा उनके माध्यम से ट्रैफ़िक के एन्क्रिप्शन और परिवहन के लिए एक एकीकृत विनिर्देश।"
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **दायरा:** यह मार्गदर्शिका tunnel कार्यान्वयन, संदेश प्रारूप, और दोनों tunnel निर्माण विनिर्देशों (ECIES (एन्क्रिप्शन योजना) और पुरानी ElGamal) को एकीकृत करती है। मौजूदा डीप लिंक ऊपर दिए गए उपनामों के माध्यम से काम करते रहेंगे।

## Tunnel मॉडल {#tunnel-model}

I2P पेलोड्स को *एकदिशीय tunnels* के माध्यम से अग्रेषित करता है: ऐसे router के क्रमबद्ध समूह जो ट्रैफिक को एक ही दिशा में ले जाते हैं। दो गंतव्यों के बीच एक पूर्ण राउंड-ट्रिप के लिए चार tunnels आवश्यक होते हैं (दो आउटबाउंड, दो इनबाउंड)।

शब्दावली के लिए [Tunnel अवलोकन](/docs/overview/tunnel-routing/) से शुरू करें, फिर संचालन संबंधी विवरण के लिए इस मार्गदर्शिका का उपयोग करें।

### संदेश जीवनचक्र {#message-lifecycle}

1. tunnel **गेटवे** एक या अधिक I2NP संदेशों को समूहित करता है, उन्हें खंडित करता है, और वितरण निर्देश लिखता है।
2. गेटवे पेलोड को निश्चित आकार (1024&nbsp;B) के tunnel संदेश में संकुलित करता है, आवश्यकता होने पर पैडिंग जोड़ता है।
3. प्रत्येक **प्रतिभागी** पिछले हॉप का सत्यापन करता है, अपना एन्क्रिप्शन लेयर लागू करता है, और {nextTunnelId, nextIV, encryptedPayload} को अगले हॉप को अग्रेषित करता है।
4. tunnel **एंडपॉइंट** अंतिम लेयर हटाता है, वितरण निर्देशों को प्रक्रिया करता है, खंडों को पुनः संयोजित करता है, और पुनर्निर्मित I2NP संदेशों को प्रेषित करता है।

डुप्लिकेट पहचान IV (Initialization Vector, आरंभन सदिश) और पहले कूट-खंड के XOR (exclusive OR) के आधार पर कुंजीकृत एक क्षयशील Bloom filter (प्रायिक सदस्यता फिल्टर) का उपयोग करती है, ताकि IV की अदला-बदली पर आधारित टैगिंग हमलों को रोका जा सके।

### भूमिकाएँ एक नज़र में {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### एन्क्रिप्शन कार्यप्रवाह {#encryption-workflow}

- **इनबाउंड tunnels:** गेटवे अपनी लेयर कुंजी से एक बार एन्क्रिप्ट करता है; डाउनस्ट्रीम प्रतिभागी एन्क्रिप्ट करते रहते हैं जब तक कि निर्माता अंतिम पेलोड को डिक्रिप्ट नहीं कर देता।
- **आउटबाउंड tunnels:** गेटवे प्रत्येक hop (मध्यवर्ती नोड) के एन्क्रिप्शन का इनवर्स पहले से लागू कर देता है, ताकि प्रत्येक प्रतिभागी एन्क्रिप्ट करे। जब एंडपॉइंट एन्क्रिप्ट करता है, तो गेटवे का मूल प्लेनटेक्स्ट प्रकट हो जाता है।

दोनों दिशाएँ `{tunnelId, IV, encryptedPayload}` को next hop (नेटवर्क में अगला नोड) तक अग्रेषित करती हैं।

---

## Tunnel संदेश प्रारूप {#tunnel-message-format}

Tunnel गेटवे I2NP संदेशों को निश्चित आकार के लिफ़ाफ़ों में खंडित करते हैं ताकि पेलोड की लंबाई छिपाई जा सके और प्रति-हॉप प्रसंस्करण सरल बनाया जा सके।

### एन्क्रिप्टेड लेआउट {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – अगले हॉप के लिए 32-बिट पहचानकर्ता (शून्य से भिन्न, प्रत्येक बिल्ड चक्र में बदलता है).
- **IV** – प्रत्येक संदेश के लिए चुना गया 16-बाइट AES IV.
- **Encrypted payload** – AES-256-CBC ciphertext (कूटपाठ) के 1008 बाइट्स.

कुल आकार: 1028 बाइट्स.

### डिक्रिप्टेड लेआउट {#decrypted-layout}

जब कोई हॉप अपनी एन्क्रिप्शन परत हटा देता है:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **चेकसम** डिक्रिप्ट किए गए ब्लॉक को सत्यापित करता है।
- **पैडिंग** यादृच्छिक गैर-शून्य बाइट्स होती हैं, जो एक शून्य बाइट पर समाप्त होती हैं।
- **डिलीवरी निर्देश** एंडपॉइंट को बताते हैं कि प्रत्येक फ्रैगमेंट को कैसे संभालना है (स्थानीय रूप से डिलीवर करना, किसी अन्य tunnel को अग्रेषित करना, आदि)।
- **फ्रैगमेंट** अंतर्निहित I2NP संदेश वहन करते हैं; एंडपॉइंट उन्हें उच्चतर परतों को भेजने से पहले पुनः संयोजित करता है।

### प्रसंस्करण चरण {#processing-steps}

1. गेटवे I2NP संदेशों को खंडित कर कतार में डालते हैं, और पुनर्संयोजन के लिए आंशिक खंडों को थोड़े समय तक सुरक्षित रखते हैं।
2. गेटवे उपयुक्त लेयर कुंजियों से पेलोड को एन्क्रिप्ट करता है और tunnel ID तथा IV (Initialization Vector - आरंभिक वैक्टर) सेट करता है।
3. प्रत्येक प्रतिभागी IV (AES-256/ECB) और फिर पेलोड (AES-256/CBC) को एन्क्रिप्ट करता है, उसके बाद IV को पुनः एन्क्रिप्ट करके संदेश अग्रेषित करता है।
4. एंडपॉइंट उल्टे क्रम में डिक्रिप्ट करता है, चेकसम सत्यापित करता है, डिलिवरी निर्देशों को निष्पादित करता है, और खंडों का पुनर्संयोजन करता है।

---

## Tunnel निर्माण (ECIES-X25519) {#tunnel-creation-ecies}

आधुनिक routers ECIES-X25519 कुंजियों के साथ tunnels बनाते हैं, जिससे बिल्ड संदेश छोटे हो जाते हैं और forward secrecy (लंबी-अवधि कुंजी लीक होने पर भी पुराने संदेश सुरक्षित रहना) सक्षम होती है।

- **Build message:** एक एकल `TunnelBuild` (या `VariableTunnelBuild`) I2NP संदेश 1–8 एन्क्रिप्टेड बिल्ड रिकॉर्ड वहन करता है, प्रत्येक हॉप पर एक।
- **Layer keys:** निर्माता प्रति-हॉप लेयर, IV (Initialization Vector—प्रारंभिक वेक्टर), और उत्तर कुंजियाँ HKDF (HMAC-based Key Derivation Function—HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन) के माध्यम से, हॉप की स्थिर X25519 (Curve25519 आधारित Diffie–Hellman) पहचान और निर्माता की अल्पकालिक कुंजी का उपयोग करके व्युत्पन्न करते हैं।
- **Processing:** प्रत्येक हॉप अपना रिकॉर्ड डिक्रिप्ट करता है, रिक्वेस्ट फ्लैग्स को मान्य करता है, रिप्लाई ब्लॉक (सफलता या विस्तृत विफलता कोड) लिखता है, शेष रिकॉर्ड्स को पुनः एन्क्रिप्ट करता है, और संदेश को अग्रेषित करता है।
- **Replies:** निर्माता को garlic encryption से लिपटा हुआ रिप्लाई संदेश प्राप्त होता है। असफल के रूप में चिह्नित रिकॉर्ड में एक गंभीरता कोड शामिल होता है ताकि router पीयर की प्रोफाइलिंग कर सके।
- **Compatibility:** routers अभी भी पिछड़ी संगतता के लिए legacy ElGamal (पारंपरिक सार्वजनिक-कुंजी एन्क्रिप्शन योजना) बिल्ड्स स्वीकार कर सकते हैं, लेकिन नई tunnels डिफ़ॉल्ट रूप से ECIES (Elliptic Curve Integrated Encryption Scheme—एलिप्टिक कर्व आधारित एकीकृत एन्क्रिप्शन योजना) का उपयोग करती हैं।

> फ़ील्ड-दर-फ़ील्ड स्थिरांकों और कुंजी-व्युत्पत्ति टिप्पणियों के लिए, ECIES (Elliptic Curve Integrated Encryption Scheme—दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) प्रस्ताव इतिहास और router स्रोत देखें; यह गाइड परिचालन प्रवाह को कवर करता है।

---

## पुराने Tunnel का निर्माण (ElGamal-2048) {#tunnel-creation-elgamal}

मूल tunnel निर्माण प्रारूप में ElGamal सार्वजनिक कुंजियों का उपयोग किया जाता था। आधुनिक routers पिछली संगतता के लिए सीमित समर्थन बनाए रखते हैं।

> **स्थिति:** अप्रचलित। इसे ऐतिहासिक संदर्भ के लिए और उन सभी के लिए, जो legacy-compatible tooling (पुराने संस्करणों के साथ संगत टूलिंग) का रखरखाव कर रहे हैं, यहाँ रखा गया है।

- **Non-interactive telescoping:** (बिना अंतःक्रिया वाला क्रमिक-विस्तार) एक ही build संदेश पूरे पथ से होकर गुजरता है। प्रत्येक हॉप अपने 528-बाइट रिकॉर्ड को डिक्रिप्ट करता है, संदेश को अद्यतन करता है, और उसे आगे अग्रेषित करता है।
- **परिवर्ती लंबाई:** Variable Tunnel Build Message (VTBM, चर लंबाई वाला Tunnel निर्माण संदेश) ने 1–8 रिकॉर्ड की अनुमति दी। पहले वाला स्थिर संदेश हमेशा आठ रिकॉर्ड शामिल करता था ताकि tunnel की लंबाई छिपी रहे।
- **अनुरोध रिकॉर्ड विन्यास:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **फ्लैग्स:** बिट 7 एक इनबाउंड गेटवे (IBGW) को दर्शाता है; बिट 6 एक आउटबाउंड एंडपॉइंट (OBEP) को चिह्नित करता है। ये परस्पर अनन्य होते हैं.
- **एन्क्रिप्शन:** प्रत्येक रिकॉर्ड को hop (रिले चरण) की सार्वजनिक कुंजी का उपयोग करते हुए ElGamal-2048 से एन्क्रिप्ट किया जाता है। सममित AES-256-CBC लेयरिंग यह सुनिश्चित करती है कि केवल इच्छित hop ही अपना रिकॉर्ड पढ़ सके.
- **मुख्य तथ्य:** tunnel IDs गैर-शून्य 32-बिट मान होते हैं; निर्माता वास्तविक tunnel की लंबाई छिपाने के लिए डमी रिकॉर्ड सम्मिलित कर सकते हैं; विश्वसनीयता असफल बिल्ड्स को पुनः प्रयास करने पर निर्भर करती है.

---

## Tunnel पूल और जीवनचक्र {#tunnel-pools}

Routers अन्वेषण ट्रैफ़िक के लिए और प्रत्येक I2CP सत्र के लिए स्वतंत्र इनबाउंड और आउटबाउंड tunnel पूल बनाए रखते हैं।

- **Peer selection:** अन्वेषणात्मक tunnels विविधता बढ़ाने के लिए “active, not failing” पीयर बकेट से चुनती हैं; क्लाइंट tunnels तेज, उच्च-क्षमता वाले पीयर्स को प्राथमिकता देती हैं।
- **Deterministic ordering:** पीयर्स को `SHA256(peerHash || poolKey)` और पूल की यादृच्छिक कुंजी के बीच XOR दूरी के आधार पर क्रमबद्ध किया जाता है। रीस्टार्ट पर कुंजी रोटेट होती है, जिससे एक रन के भीतर स्थिरता मिलती है, जबकि रनों के पार predecessor attacks (पूर्ववर्ती हमले) को कठिन बनाती है।
- **Lifecycle:** routers `{mode, direction, length, variance}` ट्यूपल प्रति ऐतिहासिक बिल्ड समय को ट्रैक करते हैं। tunnels की अवधि समाप्ति के पास पहुँचने पर, प्रतिस्थापन जल्दी शुरू हो जाते हैं; विफलताएँ होने पर router समानांतर बिल्ड्स बढ़ाता है, और लंबित प्रयासों पर सीमा लगाता है।
- **Configuration knobs:** सक्रिय/बैकअप tunnels की संख्या, हॉप लंबाई और वैरिएंस, ज़ीरो-हॉप अनुमतियाँ, और बिल्ड दर सीमाएँ — ये सभी प्रति पूल ट्यून किए जा सकते हैं।

---

## भीड़भाड़ और विश्वसनीयता {#congestion}

यद्यपि tunnels सर्किट जैसे लगते हैं, routers उन्हें संदेश कतारों की तरह मानते हैं। विलंबता को सीमित रखने के लिए Weighted Random Early Discard (WRED) (भार-आधारित यादृच्छिक प्रारंभिक त्याग नीति) का उपयोग किया जाता है:

- जैसे-जैसे उपयोग कॉन्फ़िगर की गई सीमाओं के करीब आता है, ड्रॉप होने की संभावना बढ़ती है।
- प्रतिभागी निश्चित आकार के फ्रैगमेंट को आधार मानते हैं; गेटवे/एंडपॉइंट्स संयुक्त फ्रैगमेंट आकार के आधार पर ड्रॉप करते हैं, सबसे पहले बड़े पेलोड को दंडित करते हुए।
- आउटबाउंड एंडपॉइंट्स अन्य भूमिकाओं से पहले ड्रॉप करते हैं ताकि नेटवर्क संसाधनों का न्यूनतम अपव्यय हो।

गारंटीकृत वितरण को [स्ट्रीमिंग लाइब्रेरी](/docs/specs/streaming/) जैसी उच्चतर परतों पर छोड़ दिया जाता है। जिन अनुप्रयोगों को विश्वसनीयता चाहिए, उन्हें पुनःप्रेषण और स्वीकृतियों को स्वयं संभालना होगा।

---

## अधिक पठन {#further-reading}

- [पीयर चयन](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel का अवलोकन](/docs/overview/tunnel-routing/)
- [पुराना Tunnel कार्यान्वयन](/docs/legacy/old-implementation/)
