---
title: "I2PTunnel"
description: "I2P पर इंटरफेस करने और सेवाएं प्रदान करने के लिए उपकरण"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

I2PTunnel एक मुख्य I2P घटक है जो I2P नेटवर्क पर इंटरफेसिंग और सेवाएं प्रदान करने के लिए है। यह tunnel abstraction के माध्यम से TCP-आधारित और मीडिया स्ट्रीमिंग अनुप्रयोगों को गुमनाम रूप से संचालित करने में सक्षम बनाता है। एक tunnel का गंतव्य [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), या एक पूर्ण destination key द्वारा परिभाषित किया जा सकता है।

प्रत्येक स्थापित tunnel स्थानीय रूप से सुनता है (जैसे, `localhost:port`) और आंतरिक रूप से I2P destinations से जुड़ता है। एक सेवा होस्ट करने के लिए, वांछित IP और port की ओर इंगित करने वाला एक tunnel बनाएं। एक संबंधित I2P destination key उत्पन्न की जाती है, जो सेवा को I2P network के भीतर विश्व स्तर पर पहुंच योग्य बनाती है। I2PTunnel वेब इंटरफ़ेस [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/) पर उपलब्ध है।

---

## डिफ़ॉल्ट सेवाएं

### सर्वर tunnel

- **I2P Webserver** – I2P पर आसान होस्टिंग के लिए [localhost:7658](http://localhost:7658) पर एक Jetty webserver के लिए tunnel।  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### क्लाइंट टनल

- **I2P HTTP Proxy** – `localhost:4444` – I2P और outproxies के माध्यम से इंटरनेट ब्राउज़ करने के लिए उपयोग किया जाता है।
- **I2P HTTPS Proxy** – `localhost:4445` – HTTP proxy का सुरक्षित संस्करण।
- **Irc2P** – `localhost:6668` – डिफ़ॉल्ट अनाम IRC नेटवर्क tunnel।
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – रिपॉज़िटरी SSH एक्सेस के लिए क्लाइंट tunnel।
- **Postman SMTP** – `localhost:7659` – आउटगोइंग मेल के लिए क्लाइंट tunnel।
- **Postman POP3** – `localhost:7660` – इनकमिंग मेल के लिए क्लाइंट tunnel।

> नोट: केवल I2P Webserver एक डिफ़ॉल्ट **server tunnel** है; अन्य सभी client tunnels हैं जो बाहरी I2P सेवाओं से कनेक्ट होते हैं।

---

## कॉन्फ़िगरेशन

I2PTunnel कॉन्फ़िगरेशन विनिर्देश [/spec/configuration](/docs/specs/configuration/) पर प्रलेखित है।

---

## क्लाइंट मोड

### मानक

एक स्थानीय TCP पोर्ट खोलता है जो I2P destination पर किसी सेवा से कनेक्ट होता है। redundancy के लिए अल्पविराम से अलग किए गए एकाधिक destination entries का समर्थन करता है।

### HTTP

HTTP/HTTPS अनुरोधों के लिए एक प्रॉक्सी tunnel। स्थानीय और दूरस्थ outproxies, हेडर स्ट्रिपिंग, कैशिंग, प्रमाणीकरण, और पारदर्शी संपीड़न का समर्थन करता है।

**गोपनीयता सुरक्षा:**   - headers को हटाता है: `Accept-*`, `Referer`, `Via`, `From`   - host headers को Base32 destinations के साथ प्रतिस्थापित करता है   - RFC-अनुरूप hop-by-hop stripping को लागू करता है   - पारदर्शी decompression के लिए समर्थन जोड़ता है   - आंतरिक error pages और स्थानीयकृत responses प्रदान करता है

**कम्प्रेशन व्यवहार:**   - अनुरोध कस्टम हेडर `X-Accept-Encoding: x-i2p-gzip` का उपयोग कर सकते हैं   - `Content-Encoding: x-i2p-gzip` वाली प्रतिक्रियाएं स्वचालित रूप से डीकम्प्रेस की जाती हैं   - दक्षता के लिए MIME प्रकार और प्रतिक्रिया लंबाई के आधार पर कम्प्रेशन का मूल्यांकन किया जाता है

**स्थायित्व (2.5.0 के बाद से नया):**   HTTP Keepalive और persistent connections अब Hidden Services Manager के माध्यम से I2P-होस्टेड सेवाओं के लिए समर्थित हैं। यह विलंबता और कनेक्शन ओवरहेड को कम करता है लेकिन अभी तक सभी hops में पूर्ण RFC 2616-अनुरूप persistent sockets को सक्षम नहीं करता है।

**पाइपलाइनिंग:** असमर्थित और अनावश्यक बनी हुई है; आधुनिक ब्राउज़रों ने इसे पदावनत कर दिया है।

**User-Agent व्यवहार:**   - **Outproxy:** वर्तमान Firefox ESR User-Agent का उपयोग करता है।   - **Internal:** गुमनामी स्थिरता के लिए `MYOB/6.66 (AN/ON)`।

### IRC क्लाइंट

I2P-आधारित IRC सर्वरों से कनेक्ट करता है। गोपनीयता के लिए पहचानकर्ताओं को फ़िल्टर करते हुए कमांड के सुरक्षित सबसेट की अनुमति देता है।

### SOCKS 4/4a/5

TCP कनेक्शन के लिए SOCKS proxy क्षमता प्रदान करता है। UDP अभी तक Java I2P में लागू नहीं किया गया है (केवल i2pd में उपलब्ध है)।

### CONNECT

SSL/TLS कनेक्शनों के लिए HTTP `CONNECT` टनलिंग को लागू करता है।

### Streamr

TCP-आधारित encapsulation के माध्यम से UDP-शैली स्ट्रीमिंग सक्षम करता है। संबंधित Streamr सर्वर tunnel के साथ जोड़े जाने पर मीडिया स्ट्रीमिंग का समर्थन करता है।

![I2PTunnel Streamr आरेख](/images/I2PTunnel-streamr.png)

---

## सर्वर मोड

### मानक सर्वर

एक TCP गंतव्य बनाता है जो स्थानीय IP:port से मैप होता है।

### HTTP सर्वर

एक destination बनाता है जो स्थानीय वेब सर्वर के साथ इंटरफेस करता है। कम्प्रेशन (`x-i2p-gzip`), हेडर स्ट्रिपिंग, और DDoS सुरक्षा का समर्थन करता है। अब **persistent connection support** (v2.5.0+) और **thread pooling optimization** (v2.7.0–2.9.0) से लाभान्वित होता है।

### HTTP द्विदिशात्मक

**पदावनत** – अभी भी कार्यात्मक है लेकिन हतोत्साहित। बिना outproxying के HTTP सर्वर और क्लाइंट दोनों के रूप में कार्य करता है। मुख्य रूप से डायग्नोस्टिक loopback परीक्षणों के लिए उपयोग किया जाता है।

### IRC सर्वर

IRC सेवाओं के लिए एक फ़िल्टर किया गया destination बनाता है, जो client destination keys को hostnames के रूप में पास करता है।

### Streamr सर्वर

I2P के माध्यम से UDP-शैली के डेटा स्ट्रीम को संभालने के लिए Streamr client tunnel के साथ युग्मित।

---

## नई सुविधाएँ (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## सुरक्षा सुविधाएँ

- गुमनामी के लिए **Header stripping** (Accept, Referer, From, Via)
- in/outproxy के आधार पर **User-Agent randomization**
- **POST rate limiting** और **Slowloris protection**
- streaming subsystems में **Connection throttling**
- tunnel layer पर **Network congestion handling**
- क्रॉस-एप्लिकेशन लीक को रोकने वाला **NetDB isolation**

---

## तकनीकी विवरण

- डिफ़ॉल्ट destination key का आकार: 516 बाइट्स (विस्तारित LS2 प्रमाणपत्रों के लिए अधिक हो सकता है)  
- Base32 पते: `{52–56+ chars}.b32.i2p`  
- Server tunnels Java I2P और i2pd दोनों के साथ संगत रहते हैं  
- पदावनत सुविधा: केवल `httpbidirserver`; 0.9.59 के बाद से कोई हटाव नहीं  
- सभी प्लेटफ़ॉर्म के लिए सही डिफ़ॉल्ट पोर्ट और document roots की पुष्टि की गई

---

## सारांश

I2PTunnel, I2P के साथ एप्लिकेशन एकीकरण की रीढ़ बना हुआ है। 0.9.59 और 2.10.0 के बीच, इसमें स्थायी कनेक्शन समर्थन, post-quantum encryption, और थ्रेडिंग में बड़े सुधार जोड़े गए। अधिकांश कॉन्फ़िगरेशन संगत रहते हैं, लेकिन डेवलपर्स को अपने सेटअप की जांच करनी चाहिए ताकि यह सुनिश्चित हो सके कि वे आधुनिक ट्रांसपोर्ट और सुरक्षा डिफ़ॉल्ट के अनुरूप हैं।
