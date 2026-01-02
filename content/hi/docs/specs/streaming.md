---
title: "स्ट्रीमिंग प्रोटोकॉल"
description: "अधिकांश I2P अनुप्रयोगों में प्रयुक्त विश्वसनीय, TCP जैसा ट्रांसपोर्ट"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## अवलोकन

I2P Streaming Library, I2P की अविश्वसनीय संदेश परत के ऊपर विश्वसनीय, क्रमानुसार और प्रमाणीकृत डेटा आपूर्ति प्रदान करती है — IP पर TCP के समान। यह वेब ब्राउज़िंग, IRC, ईमेल और फ़ाइल साझाकरण जैसे लगभग सभी इंटरैक्टिव I2P अनुप्रयोगों द्वारा उपयोग की जाती है।

यह I2P के उच्च-विलंबता वाले गुमनाम tunnels के पार विश्वसनीय प्रसारण, भीड़ नियंत्रण, पुनःप्रेषण, और प्रवाह नियंत्रण सुनिश्चित करता है। प्रत्येक स्ट्रीम destinations (गंतव्य) के बीच एंड-टू-एंड पूरी तरह एन्क्रिप्टेड होती है।

---

## मूलभूत डिज़ाइन सिद्धांत

स्ट्रीमिंग लाइब्रेरी एक **एक-चरणीय कनेक्शन सेटअप** लागू करती है, जिसमें SYN, ACK और FIN फ़्लैग उसी संदेश में डेटा पेलोड वहन कर सकते हैं। यह उच्च-विलंबता वाले परिवेशों में round-trips (आवागमन चक्र) को न्यूनतम करता है — एक छोटा HTTP ट्रांज़ैक्शन एक ही round-trip में पूरा हो सकता है।

भीड़ नियंत्रण और पुनर्प्रेषण TCP पर आधारित है, लेकिन I2P के परिवेश के लिए अनुकूलित किया गया है। विंडो आकार संदेश-आधारित हैं, बाइट-आधारित नहीं, और tunnel की विलंबता तथा ओवरहेड के अनुरूप ट्यून किए गए हैं। प्रोटोकॉल TCP के AIMD एल्गोरिदम (Additive Increase Multiplicative Decrease—योगात्मक वृद्धि, गुणात्मक कमी) के समान slow start (धीमी शुरुआत), congestion avoidance (भीड़ से बचाव), और exponential backoff (घातीय बैकऑफ) का समर्थन करता है।

---

## आर्किटेक्चर

स्ट्रीमिंग लाइब्रेरी एप्लिकेशनों और I2CP इंटरफ़ेस के बीच संचालित होती है।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
अधिकांश उपयोगकर्ता इसे I2PSocketManager, I2PTunnel, या SAMv3 के माध्यम से एक्सेस करते हैं। लाइब्रेरी destination (गंतव्य) प्रबंधन, tunnel का उपयोग, और पुनःप्रेषण को पारदर्शी रूप से संभालती है।

---

## पैकेट प्रारूप

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### हेडर विवरण

- **Stream IDs**: 32-बिट मान जो स्थानीय और रिमोट स्ट्रीम्स की अद्वितीय पहचान करते हैं।
- **Sequence Number**: SYN के लिए 0 से शुरू होता है, प्रत्येक संदेश के साथ बढ़ता है।
- **Ack Through**: N तक के सभी संदेशों की पुष्टि करता है, NACK सूची में मौजूद संदेशों को छोड़कर।
- **Flags**: अवस्था और व्यवहार को नियंत्रित करने वाला बिटमास्क।
- **Options**: RTT, MTU, और प्रोटोकॉल negotiation के लिए परिवर्तनशील लंबाई की सूची।

### कुंजी फ़्लैग्स

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## प्रवाह नियंत्रण और विश्वसनीयता

Streaming **संदेश-आधारित विंडोइंग** का उपयोग करता है, TCP के बाइट-आधारित तरीके के विपरीत। एक समय में प्रेषणाधीन बिना पुष्टि वाले पैकेटों की संख्या वर्तमान विंडो आकार (डिफ़ॉल्ट 128) के बराबर होती है।

### यंत्रणाएँ

- **भीड़ नियंत्रण:** Slow start (धीमी शुरुआत) और AIMD (Additive Increase/Multiplicative Decrease—योगात्मक वृद्धि/गुणात्मक कमी) आधारित बचाव।  
- **Choke/Unchoke (रोक/मुक्त):** बफ़र के भरण-स्तर के आधार पर प्रवाह-नियंत्रण संकेत।  
- **पुनर्प्रेषण:** RFC 6298 आधारित RTO (Retransmission Timeout—पुनर्प्रेषण समय-सीमा) गणना, exponential backoff (घातीय बैकऑफ़) सहित।  
- **डुप्लिकेट फ़िल्टरिंग:** संभावित रूप से क्रम-परिवर्तित संदेशों के बावजूद विश्वसनीयता सुनिश्चित करती है।

सामान्य कॉन्फ़िगरेशन मान:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## कनेक्शन स्थापना

1. **प्रारंभकर्ता** एक SYN भेजता है (वैकल्पिक रूप से पेलोड और FROM_INCLUDED के साथ)।  
2. **उत्तरदाता** SYN+ACK के साथ उत्तर देता है (पेलोड शामिल हो सकता है)।  
3. **प्रारंभकर्ता** स्थापना की पुष्टि करते हुए अंतिम ACK भेजता है।

वैकल्पिक प्रारंभिक पेलोड पूर्ण handshake (कनेक्शन स्थापित करने की प्रारंभिक प्रक्रिया) के पूरा होने से पहले डेटा संचरण की अनुमति देते हैं।

---

## कार्यान्वयन विवरण

### पुनःप्रेषण और Timeout (समय-समाप्ति)

पुनःप्रेषण एल्गोरिदम **RFC 6298** का पालन करता है।   - **प्रारंभिक RTO:** 9s   - **न्यूनतम RTO:** 100ms   - **अधिकतम RTO:** 45s   - **अल्फा:** 0.125   - **बीटा:** 0.25

### नियंत्रण ब्लॉक साझा करना

उसी पीयर के साथ हाल की कनेक्शन्स तेज़ रैंप‑अप के लिए पिछले RTT (राउंड‑ट्रिप समय) और window data (कंजेशन विंडो से संबंधित डेटा) का पुनः उपयोग करती हैं, जिससे “कोल्ड स्टार्ट” विलंबता से बचा जा सके। कंट्रोल ब्लॉक्स कुछ मिनटों के बाद समाप्त हो जाते हैं।

### MTU (अधिकतम संचरण इकाई) और खंडन

- डिफ़ॉल्ट MTU: **1730 बाइट्स** (दो I2NP संदेश फिट होते हैं)।  
- ECIES (Elliptic Curve Integrated Encryption Scheme—एलिप्टिक कर्व आधारित संयोजित एन्क्रिप्शन योजना) गंतव्य: **1812 बाइट्स** (कम ओवरहेड)।  
- न्यूनतम समर्थित MTU: 512 बाइट्स।

पेलोड का आकार 22-बाइट के न्यूनतम streaming header (डेटा स्ट्रीम का हेडर) को शामिल नहीं करता है।

---

## संस्करण इतिहास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## एप्लिकेशन-स्तरीय उपयोग

### जावा उदाहरण

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### SAMv3 और i2pd समर्थन

- **SAMv3**: गैर-Java क्लाइंट्स के लिए STREAM (स्ट्रीम) और DATAGRAM (डेटाग्राम) मोड प्रदान करता है.  
- **i2pd**: कॉन्फ़िगरेशन फ़ाइल विकल्पों के माध्यम से समान स्ट्रीमिंग पैरामीटर उपलब्ध कराता है (उदा. `i2p.streaming.maxWindowSize`, `profile`, आदि).

---

## Streaming और Datagrams के बीच चयन

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## सुरक्षा और पोस्ट‑क्वांटम भविष्य

स्ट्रीमिंग सत्र I2CP लेयर पर एंड-टू-एंड एन्क्रिप्टेड होते हैं। Post-quantum hybrid encryption (यानी ऐसा हाइब्रिड एन्क्रिप्शन जो क्वांटम-कंप्यूटिंग आधारित हमलों के विरुद्ध सुरक्षा के लिए बनाया गया है) (ML-KEM + X25519) का 2.10.0 में प्रायोगिक समर्थन है, लेकिन यह डिफ़ॉल्ट रूप से निष्क्रिय रहता है।

---

## संदर्भ

- [स्ट्रीमिंग API अवलोकन](/docs/specs/streaming/)  
- [स्ट्रीमिंग प्रोटोकॉल विनिर्देश](/docs/specs/streaming/)  
- [I2CP विनिर्देश](/docs/specs/i2cp/)  
- [प्रस्ताव 144: स्ट्रीमिंग MTU गणनाएँ](/proposals/144-ecies-x25519-aead-ratchet/)  
- [I2P 2.10.0 रिलीज़ नोट्स](/hi/blog/2025/09/08/i2p-2.10.0-release/)
