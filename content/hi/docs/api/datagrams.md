---
title: "डेटाग्राम"
description: "I2CP के ऊपर प्रमाणित, उत्तर देने योग्य, और कच्चे संदेश प्रारूप"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## सारांश

Datagrams, [I2CP](/docs/specs/i2cp/) के ऊपर और streaming library के समानांतर संदेश-उन्मुख संचार प्रदान करते हैं। ये connection-oriented streams की आवश्यकता के बिना **repliable**, **authenticated**, या **raw** पैकेट सक्षम करते हैं। Routers, datagrams को I2NP messages और tunnel messages में समाहित करते हैं, चाहे NTCP2 या SSU2 ट्रैफ़िक को वहन करे।

मुख्य उद्देश्य एप्लिकेशनों (जैसे trackers, DNS resolvers, या गेम) को स्व-निहित पैकेट भेजने की अनुमति देना है जो अपने प्रेषक की पहचान करते हैं।

> **2025 में नया:** I2P Project ने **Datagram2 (protocol 19)** और **Datagram3 (protocol 20)** को स्वीकृत किया, जो एक दशक में पहली बार replay protection और कम-ओवरहेड repliable messaging जोड़ता है।

---

## 1. प्रोटोकॉल स्थिरांक

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
प्रोटोकॉल 19 और 20 को **प्रस्ताव 163 (अप्रैल 2025)** में औपचारिक रूप दिया गया था। ये पश्च संगतता (backward compatibility) के लिए Datagram1 / RAW के साथ सह-अस्तित्व में हैं।

---

## 2. डेटाग्राम प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### विशिष्ट डिज़ाइन पैटर्न

- **Request → Response:** एक signed Datagram2 (request + nonce) भेजें, एक raw या Datagram3 reply (echo nonce) प्राप्त करें।
- **High-frequency/low-overhead:** Datagram3 या RAW को प्राथमिकता दें।
- **Authenticated control messages:** Datagram2।
- **Legacy compatibility:** Datagram1 अभी भी पूरी तरह से supported है।

---

## 3. Datagram2 और Datagram3 विवरण (2025)

### Datagram2 (प्रोटोकॉल 19)

Datagram1 के लिए उन्नत प्रतिस्थापन। विशेषताएं: - **रीप्ले रोकथाम:** 4-बाइट एंटी-रीप्ले टोकन। - **ऑफ़लाइन हस्ताक्षर समर्थन:** ऑफ़लाइन-हस्ताक्षरित Destinations द्वारा उपयोग सक्षम करता है। - **विस्तारित हस्ताक्षर कवरेज:** destination hash, flags, options, offline sig block, payload शामिल हैं। - **पोस्ट-क्वांटम तैयार:** भविष्य के ML-KEM हाइब्रिड के साथ संगत। - **ओवरहेड:** ≈ 457 बाइट्स (X25519 keys)।

### Datagram3 (प्रोटोकॉल 20)

कच्चे और हस्ताक्षरित प्रकारों के बीच अंतर को पाटता है। विशेषताएं: - **बिना हस्ताक्षर के उत्तर योग्य:** प्रेषक के 32-बाइट हैश + 2-बाइट फ्लैग्स शामिल हैं। - **न्यूनतम ओवरहेड:** ≈ 34 बाइट्स। - **कोई रीप्ले सुरक्षा नहीं** — एप्लिकेशन को लागू करना होगा।

दोनों protocols API 0.9.66 की सुविधाएं हैं और Java router में Release 2.9.0 से लागू हैं; अभी तक कोई i2pd या Go implementations नहीं हैं (अक्टूबर 2025)।

---

## 4. आकार और विखंडन सीमाएं

- **Tunnel संदेश का आकार:** 1 028 बाइट्स (4 B Tunnel ID + 16 B IV + 1 008 B payload)।
- **प्रारंभिक खंड:** 956 B (सामान्य TUNNEL डिलीवरी)।
- **अनुवर्ती खंड:** 996 B।
- **अधिकतम खंड:** 63–64।
- **व्यावहारिक सीमा:** ≈ 62 708 B (~61 KB)।
- **अनुशंसित सीमा:** विश्वसनीय डिलीवरी के लिए ≤ 10 KB (इससे अधिक होने पर ड्रॉप्स तेजी से बढ़ते हैं)।

**ओवरहेड सारांश:** - Datagram1 ≈ 427 B (न्यूनतम)।   - Datagram2 ≈ 457 B।   - Datagram3 ≈ 34 B।   - अतिरिक्त परतें (I2CP gzip header, I2NP, Garlic, Tunnel): + ~5.5 KB सबसे खराब स्थिति में।

---

## 5. I2CP / I2NP एकीकरण

संदेश पथ: 1. एप्लिकेशन डेटाग्राम बनाता है (I2P API या SAM के माध्यम से)।   2. I2CP gzip हेडर (`0x1F 0x8B 0x08`, RFC 1952) और CRC-32 checksum के साथ लपेटता है।   3. प्रोटोकॉल + पोर्ट नंबर gzip हेडर फ़ील्ड में संग्रहीत किए जाते हैं।   4. Router इसे I2NP संदेश के रूप में समाहित करता है → Garlic clove → 1 KB tunnel fragments।   5. Fragments outbound से होते हुए → नेटवर्क → inbound tunnel से गुजरते हैं।   6. पुनः जोड़ा गया डेटाग्राम प्रोटोकॉल नंबर के आधार पर एप्लिकेशन हैंडलर को वितरित किया जाता है।

**अखंडता:** CRC-32 (I2CP से) + वैकल्पिक क्रिप्टोग्राफिक हस्ताक्षर (Datagram1/2)। डेटाग्राम के भीतर कोई अलग चेकसम फ़ील्ड नहीं है।

---

## 6. प्रोग्रामिंग इंटरफेस

### Java API

पैकेज `net.i2p.client.datagram` में शामिल हैं: - `I2PDatagramMaker` – हस्ताक्षरित datagrams बनाता है।   - `I2PDatagramDissector` – सत्यापित करता है और प्रेषक की जानकारी निकालता है।   - `I2PInvalidDatagramException` – सत्यापन विफल होने पर फेंका जाता है।

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) एक Destination साझा करने वाले ऐप्स के लिए प्रोटोकॉल और पोर्ट मल्टीप्लेक्सिंग का प्रबंधन करता है।

**Javadoc पहुंच:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (केवल I2P नेटवर्क) - [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (clearnet मिरर) - [Official Javadocs](http://docs.i2p-projekt.de/javadoc/) (आधिकारिक दस्तावेज़)

### SAM v3 समर्थन

- SAM 3.2 (2016): PORT और PROTOCOL पैरामीटर जोड़े गए।
- SAM 3.3 (2016): PRIMARY/subsession मॉडल पेश किया गया; एक Destination पर streams + datagrams की अनुमति देता है।
- Datagram2 / 3 session styles के लिए समर्थन spec 2025 में जोड़ा गया (कार्यान्वयन लंबित)।
- आधिकारिक विनिर्देश: [SAM v3 Specification](/docs/api/samv3/)

### i2ptunnel मॉड्यूल

- **udpTunnel:** I2P UDP ऐप्स के लिए पूरी तरह कार्यात्मक आधार (`net.i2p.i2ptunnel.udpTunnel`)।
- **streamr:** A/V स्ट्रीमिंग के लिए परिचालनात्मक (`net.i2p.i2ptunnel.streamr`)।
- **SOCKS UDP:** 2.10.0 तक **कार्यात्मक नहीं** (केवल UDP स्टब)।

> सामान्य-उद्देश्य UDP के लिए, Datagram API या udpTunnel का सीधे उपयोग करें—SOCKS UDP पर निर्भर न रहें।

---

## 7. पारिस्थितिकी तंत्र और भाषा समर्थन (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P इस समय एकमात्र router है जो पूर्ण SAM 3.3 subsessions और Datagram2 API का समर्थन करता है।

---

## 8. उदाहरण उपयोग – UDP Tracker (I2PSnark 2.10.0)

Datagram2/3 का पहला वास्तविक अनुप्रयोग:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
पैटर्न सुरक्षा और प्रदर्शन को संतुलित करने के लिए प्रमाणित और हल्के डेटाग्राम के मिश्रित उपयोग को प्रदर्शित करता है।

---

## 9. सुरक्षा और सर्वोत्तम प्रथाएं

- प्रमाणित आदान-प्रदान के लिए या जब replay attacks महत्वपूर्ण हों तो Datagram2 का उपयोग करें।
- मध्यम विश्वास के साथ तेज़ उत्तर देने योग्य प्रतिक्रियाओं के लिए Datagram3 को प्राथमिकता दें।
- सार्वजनिक प्रसारण या गुमनाम डेटा के लिए RAW का उपयोग करें।
- विश्वसनीय वितरण के लिए payloads को ≤ 10 KB रखें।
- ध्यान रखें कि SOCKS UDP अभी भी कार्यरत नहीं है।
- प्राप्ति पर हमेशा gzip CRC और digital signatures को सत्यापित करें।

---

## 10. तकनीकी विनिर्देश

यह खंड निम्न-स्तरीय डेटाग्राम प्रारूपों, एनकैप्सुलेशन, और प्रोटोकॉल विवरणों को कवर करता है।

### 10.1 प्रोटोकॉल पहचान

Datagram प्रारूपों में एक सामान्य हैडर **नहीं** होता है। Router केवल payload बाइट्स से प्रकार का अनुमान नहीं लगा सकते।

जब कई डेटाग्राम प्रकारों को मिलाते हैं—या जब स्ट्रीमिंग के साथ डेटाग्राम को संयोजित करते हैं—तो स्पष्ट रूप से सेट करें: - **प्रोटोकॉल नंबर** (I2CP या SAM के माध्यम से) - वैकल्पिक रूप से **पोर्ट नंबर**, यदि आपका एप्लिकेशन सेवाओं को मल्टीप्लेक्स करता है

प्रोटोकॉल को अनसेट (`0` या `PROTO_ANY`) छोड़ना अनुचित है और इससे रूटिंग या डिलीवरी त्रुटियां हो सकती हैं।

### 10.2 रॉ डेटाग्राम

नॉन-रिप्लायएबल डेटाग्राम में कोई प्रेषक या प्रमाणीकरण डेटा नहीं होता है। ये अपारदर्शी पेलोड हैं, जो उच्च-स्तरीय डेटाग्राम API के बाहर संभाले जाते हैं लेकिन SAM और I2PTunnel के माध्यम से समर्थित हैं।

**प्रोटोकॉल:** `18` (`PROTO_DATAGRAM_RAW`)

**प्रारूप:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
पेलोड की लंबाई ट्रांसपोर्ट सीमाओं द्वारा सीमित है (≈32 KB व्यावहारिक अधिकतम, अक्सर इससे बहुत कम)।

### 10.3 डेटाग्राम1 (उत्तर देने योग्य डेटाग्राम)

प्रेषक का **Destination** और प्रमाणीकरण तथा उत्तर पते के लिए एक **Signature** एम्बेड करता है।

**प्रोटोकॉल:** `17` (`PROTO_DATAGRAM`)

**ओवरहेड:** ≥427 बाइट्स **पेलोड:** लगभग ~31.5 KB तक (ट्रांसपोर्ट द्वारा सीमित)

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: एक Destination (387+ बाइट्स)
- `signature`: key type से मेल खाने वाला एक Signature
  - DSA_SHA1 के लिए: payload के SHA-256 hash का Signature
  - अन्य key types के लिए: payload पर सीधे Signature

**नोट्स:** - गैर-DSA प्रकारों के लिए हस्ताक्षर I2P 0.9.14 में मानकीकृत किए गए थे। - LS2 (Proposal 123) ऑफ़लाइन हस्ताक्षर वर्तमान में Datagram1 में समर्थित नहीं हैं।

### 10.4 Datagram2 प्रारूप

एक बेहतर repliable datagram जो **replay resistance** (पुनः प्रयोग प्रतिरोध) जोड़ता है जैसा कि [Proposal 163](/proposals/163-datagram2/) में परिभाषित है।

**प्रोटोकॉल:** `19` (`PROTO_DATAGRAM2`)

कार्यान्वयन जारी है। अनुप्रयोगों में अतिरेक (redundancy) के लिए nonce या timestamp जांच शामिल होनी चाहिए।

### 10.5 Datagram3 प्रारूप

**उत्तर देने योग्य लेकिन असत्यापित** डेटाग्राम प्रदान करता है। एम्बेडेड गंतव्य और हस्ताक्षर के बजाय router द्वारा रखरखाव किए गए सत्र प्रमाणीकरण पर निर्भर करता है।

**प्रोटोकॉल:** `20` (`PROTO_DATAGRAM3`) **स्थिति:** 0.9.66 से विकास के अधीन

उपयोगी जब: - Destinations बड़े हों (जैसे, post-quantum keys) - Authentication किसी अन्य layer पर होता हो - Bandwidth efficiency महत्वपूर्ण हो

### 10.6 डेटा अखंडता

डेटाग्राम की अखंडता I2CP परत में **gzip CRC-32 checksum** द्वारा सुरक्षित की जाती है। डेटाग्राम पेलोड प्रारूप के भीतर कोई स्पष्ट checksum फ़ील्ड मौजूद नहीं है।

### 10.7 पैकेट एनकैप्सुलेशन

प्रत्येक डेटाग्राम को एकल I2NP संदेश के रूप में या **Garlic Message** में एक व्यक्तिगत clove के रूप में एन्कैप्सुलेट किया जाता है। I2CP, I2NP, और tunnel परतें लंबाई और फ्रेमिंग को संभालती हैं — datagram प्रोटोकॉल में कोई आंतरिक सीमांकक या लंबाई फ़ील्ड नहीं है।

### 10.8 पोस्ट-क्वांटम (PQ) विचार

यदि **Proposal 169** (ML-DSA signatures) लागू किया जाता है, तो signature और destination के आकार नाटकीय रूप से बढ़ जाएंगे — ~455 bytes से **≥3739 bytes** तक। यह परिवर्तन datagram overhead को काफी बढ़ा देगा और प्रभावी payload क्षमता को कम कर देगा।

**Datagram3**, जो सत्र-स्तरीय प्रमाणीकरण (एम्बेडेड हस्ताक्षरों पर नहीं) पर निर्भर करता है, संभवतः पोस्ट-क्वांटम I2P वातावरण में पसंदीदा डिज़ाइन बन जाएगा।

---

## 11. संदर्भ

- [Proposal 163 – Datagram2 और Datagram3](/proposals/163-datagram2/)
- [Proposal 160 – UDP Tracker Integration](/proposals/160-udp-trackers/)
- [Proposal 144 – Streaming MTU Calculations](/proposals/144-ecies-x25519-aead-ratchet/)
- [Proposal 169 – Post-Quantum Signatures](/proposals/169-pq-crypto/)
- [I2CP Specification](/docs/specs/i2cp/)
- [I2NP Specification](/docs/specs/i2np/)
- [Tunnel Message Specification](/docs/specs/implementation/)
- [SAM v3 Specification](/docs/api/samv3/)
- [i2ptunnel Documentation](/docs/api/i2ptunnel/)

## 12. परिवर्तन लॉग मुख्य बिंदु (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. सारांश

डेटाग्राम सबसिस्टम अब चार प्रोटोकॉल वेरिएंट का समर्थन करता है जो पूर्ण-प्रमाणित से लेकर हल्के कच्चे ट्रांसमिशन तक का स्पेक्ट्रम प्रदान करते हैं। डेवलपर्स को सुरक्षा-संवेदनशील उपयोग के मामलों के लिए **Datagram2** और कुशल उत्तर योग्य ट्रैफ़िक के लिए **Datagram3** की ओर स्थानांतरित होना चाहिए। सभी पुराने प्रकार दीर्घकालिक इंटरऑपरेबिलिटी सुनिश्चित करने के लिए संगत बने रहते हैं।
