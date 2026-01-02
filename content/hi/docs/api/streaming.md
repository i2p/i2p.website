---
title: "स्ट्रीमिंग प्रोटोकॉल"
description: "अधिकांश I2P अनुप्रयोगों द्वारा उपयोग किया जाने वाला TCP-जैसा ट्रांसपोर्ट"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

**I2P Streaming Library** I2P की message layer पर विश्वसनीय, क्रमबद्ध, प्रमाणित परिवहन प्रदान करती है, जो **IP पर TCP** के समान है। यह [I2CP protocol](/docs/specs/i2cp/) के ऊपर स्थित है और लगभग सभी इंटरैक्टिव I2P अनुप्रयोगों द्वारा उपयोग की जाती है, जिनमें HTTP proxies, IRC, BitTorrent और email शामिल हैं।

### मुख्य विशेषताएं

- **SYN**, **ACK**, और **FIN** flags का उपयोग करके एक-चरणीय कनेक्शन सेटअप जो राउंड-ट्रिप्स को कम करने के लिए पेलोड डेटा के साथ बंडल किया जा सकता है।
- **Sliding-window congestion control**, slow start और congestion avoidance के साथ जो I2P के उच्च-विलंबता वातावरण के लिए अनुकूलित है।
- पैकेट संपीड़न (डिफ़ॉल्ट 4KB संपीड़ित सेगमेंट) जो पुनः संचरण लागत और विखंडन विलंबता को संतुलित करता है।
- I2P destinations के बीच पूर्णतः **प्रमाणित, एन्क्रिप्टेड**, और **विश्वसनीय** चैनल एब्सट्रैक्शन।

यह डिज़ाइन छोटे HTTP अनुरोधों और प्रतिक्रियाओं को एकल राउंड-ट्रिप में पूर्ण होने में सक्षम बनाता है। एक SYN पैकेट अनुरोध पेलोड ले जा सकता है, जबकि प्रतिक्रियाकर्ता का SYN/ACK/FIN पूर्ण प्रतिक्रिया बॉडी शामिल कर सकता है।

---

## API मूल बातें

Java स्ट्रीमिंग API मानक Java सॉकेट प्रोग्रामिंग को दर्शाता है:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` I2CP के माध्यम से एक router सत्र को negotiate करता है या पुनः उपयोग करता है।
- यदि कोई key प्रदान नहीं की गई है, तो एक नया destination स्वचालित रूप से उत्पन्न हो जाता है।
- डेवलपर्स `options` map के माध्यम से I2CP विकल्प (जैसे कि tunnel लंबाई, एन्क्रिप्शन प्रकार, या कनेक्शन सेटिंग्स) पास कर सकते हैं।
- `I2PSocket` और `I2PServerSocket` मानक Java `Socket` इंटरफेस को प्रतिबिंबित करते हैं, जिससे माइग्रेशन सरल हो जाता है।

पूर्ण Javadocs I2P router console से या [यहाँ](/docs/specs/streaming/) उपलब्ध हैं।

---

## कॉन्फ़िगरेशन और ट्यूनिंग

सॉकेट मैनेजर बनाते समय आप कॉन्फ़िगरेशन प्रॉपर्टीज़ को इस तरह पास कर सकते हैं:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### मुख्य विकल्प

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### कार्यभार के अनुसार व्यवहार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
संस्करण 0.9.4 के बाद से नई सुविधाओं में reject log suppression, DSA सूची समर्थन (0.9.21), और अनिवार्य प्रोटोकॉल प्रवर्तन (0.9.36) शामिल हैं। 2.10.0 के बाद से routers में transport layer पर post-quantum hybrid encryption (ML-KEM + X25519) शामिल है।

---

## प्रोटोकॉल विवरण

प्रत्येक stream को एक **Stream ID** द्वारा पहचाना जाता है। Packets TCP के समान control flags ले जाते हैं: `SYNCHRONIZE`, `ACK`, `FIN`, और `RESET`। Packets में एक साथ data और control flags दोनों हो सकते हैं, जो अल्पकालिक connections के लिए दक्षता में सुधार करता है।

### कनेक्शन जीवनचक्र

1. **SYN भेजा गया** — प्रारंभकर्ता वैकल्पिक डेटा शामिल करता है।
2. **SYN/ACK प्रतिक्रिया** — उत्तरदाता वैकल्पिक डेटा शामिल करता है।
3. **ACK अंतिमीकरण** — विश्वसनीयता और सत्र स्थिति स्थापित करता है।
4. **FIN/RESET** — व्यवस्थित बंद करने या अचानक समाप्ति के लिए उपयोग किया जाता है।

### विखंडन और पुनर्व्यवस्था

क्योंकि I2P tunnel विलंबता और संदेश पुनर्क्रम का परिचय देते हैं, लाइब्रेरी अज्ञात या जल्दी आने वाली streams से पैकेट को बफर करती है। बफर किए गए संदेशों को तब तक संग्रहीत किया जाता है जब तक समन्वयन पूर्ण नहीं हो जाता, जिससे पूर्ण, क्रम में डिलीवरी सुनिश्चित होती है।

### प्रोटोकॉल प्रवर्तन

विकल्प `i2p.streaming.enforceProtocol=true` (0.9.36 से डिफ़ॉल्ट) यह सुनिश्चित करता है कि कनेक्शन सही I2CP प्रोटोकॉल नंबर का उपयोग करें, जिससे एक destination को साझा करने वाले कई subsystems के बीच संघर्ष को रोका जा सके।

---

## इंटरऑपरेबिलिटी और सर्वोत्तम प्रथाएं

स्ट्रीमिंग प्रोटोकॉल **Datagram API** के साथ सह-अस्तित्व में है, जो डेवलपर्स को कनेक्शन-उन्मुख और कनेक्शन-रहित ट्रांसपोर्ट के बीच चयन करने का विकल्प देता है।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### साझा क्लाइंट

एप्लिकेशन **shared clients** के रूप में चलकर मौजूदा tunnels का पुनः उपयोग कर सकते हैं, जिससे कई सेवाएं एक ही destination को साझा कर सकती हैं। हालांकि यह overhead को कम करता है, यह cross-service correlation जोखिम को बढ़ाता है—सावधानी से उपयोग करें।

### भीड़ नियंत्रण

- स्ट्रीमिंग लेयर RTT-आधारित फीडबैक के माध्यम से नेटवर्क लेटेंसी और थ्रूपुट को लगातार अनुकूलित करती है।
- जब routers योगदान देने वाले पीयर होते हैं (participating tunnels सक्षम) तो एप्लिकेशन सर्वोत्तम प्रदर्शन करते हैं।
- TCP-जैसे कंजेशन कंट्रोल मैकेनिज्म धीमे पीयर्स को ओवरलोड होने से रोकते हैं और tunnels में बैंडविड्थ उपयोग को संतुलित करने में मदद करते हैं।

### विलंबता संबंधी विचार

चूंकि I2P कई सौ मिलीसेकंड की बेस लेटेंसी जोड़ता है, एप्लिकेशन को राउंड-ट्रिप्स को कम करना चाहिए। जहां संभव हो कनेक्शन सेटअप के साथ डेटा बंडल करें (जैसे, SYN में HTTP अनुरोध)। कई छोटे क्रमिक आदान-प्रदान पर निर्भर डिज़ाइन से बचें।

---

## परीक्षण और संगतता

- पूर्ण संगतता सुनिश्चित करने के लिए हमेशा **Java I2P** और **i2pd** दोनों के विरुद्ध परीक्षण करें।
- यद्यपि प्रोटोकॉल मानकीकृत है, कार्यान्वयन में मामूली अंतर हो सकते हैं।
- पुराने routers को सहजता से संभालें—कई peers अभी भी 2.0 से पूर्व के संस्करण चलाते हैं।
- RTT और retransmission मेट्रिक्स पढ़ने के लिए `I2PSocket.getOptions()` और `getSession()` का उपयोग करके कनेक्शन आँकड़ों की निगरानी करें।

प्रदर्शन tunnel कॉन्फ़िगरेशन पर बहुत अधिक निर्भर करता है:   - **छोटी tunnels (1–2 hops)** → कम latency, कम anonymity।   - **लंबी tunnels (3+ hops)** → अधिक anonymity, बढ़ी हुई RTT।

---

## मुख्य सुधार (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## सारांश

**I2P Streaming Library** I2P के भीतर सभी विश्वसनीय संचार की रीढ़ है। यह क्रम में, प्रमाणित, एन्क्रिप्टेड संदेश वितरण सुनिश्चित करती है और अनाम वातावरण में TCP के लिए लगभग प्रत्यक्ष प्रतिस्थापन प्रदान करती है।

इष्टतम प्रदर्शन प्राप्त करने के लिए: - SYN+payload bundling के साथ round-trips को न्यूनतम करें।   - अपने workload के लिए window और timeout parameters को tune करें।   - latency-sensitive applications के लिए छोटे tunnels को प्राथमिकता दें।   - peers को overload होने से बचाने के लिए congestion-friendly designs का उपयोग करें।
