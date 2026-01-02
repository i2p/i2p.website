---
title: "SAM v3"
description: "गैर-Java I2P अनुप्रयोगों के लिए स्थिर ब्रिज प्रोटोकॉल"
slug: "samv3"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SAM v3 ("Simple Anonymous Messaging") वर्तमान **स्थिर, router agnostic API** है जो बाहरी अनुप्रयोगों को I2P नेटवर्क के साथ संचार करने की अनुमति देता है बिना router को स्वयं एम्बेड किए। यह **streams**, **datagrams**, और **raw messages** तक एकीकृत पहुंच प्रदान करता है, और गैर-Java सॉफ़्टवेयर के लिए प्रामाणिक ब्रिज परत बना रहता है।

## 1. अवलोकन और उद्देश्य

SAM v3 डेवलपर्स को किसी भी भाषा में I2P aware सॉफ़्टवेयर बनाने में सक्षम बनाता है, एक हल्के TCP/UDP प्रोटोकॉल का उपयोग करके। यह router की आंतरिक कार्यप्रणाली को सरल बनाता है, TCP (7656) और UDP (7655) पर न्यूनतम कमांड प्रदान करता है। **Java I2P** और **i2pd** दोनों SAM v3 विनिर्देश के उपसमुच्चय को लागू करते हैं, हालांकि i2pd में 2025 तक अभी भी अधिकांश 3.2 और 3.3 एक्सटेंशन की कमी है।

## 2. संस्करण इतिहास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.7.3 (May 2009)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Streams + Datagrams; binary destinations; `SESSION CREATE STYLE=` parameter.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.1</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.14 (Jul 2014)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature type negotiation via `SIGNATURE_TYPE`; improved `DEST GENERATE`.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.24 (Jan 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per session encryption + tunnel options; `STREAM CONNECT ID` support.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.3</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.25 (Mar 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY / SUBSESSION architecture; multiplexing; improved datagrams.</td></tr>
  </tbody>
</table>
### नामकरण नोट

- **Java I2P** `PRIMARY/SUBSESSION` का उपयोग करता है।
- **i2pd** और **I2P+** backward compatibility के लिए legacy `MASTER/SUBSESSION` terminology का उपयोग जारी रखते हैं।

## 3. मुख्य कार्यप्रवाह

### संस्करण बातचीत

```
HELLO VERSION MIN=3.1 MAX=3.3
HELLO REPLY RESULT=OK VERSION=3.3
```
### गंतव्य निर्माण

```
DEST GENERATE SIGNATURE_TYPE=7
```
- `SIGNATURE_TYPE=7` → **Ed25519 (EdDSA SHA512)**। I2P 0.9.15 के बाद से दृढ़ता से अनुशंसित।

### सत्र निर्माण

```
SESSION CREATE STYLE=STREAM DESTINATION=NAME     OPTION=i2cp.leaseSetEncType=4,0     OPTION=inbound.quantity=3     OPTION=outbound.quantity=3
```
- `i2cp.leaseSetEncType=4,0` → `4` X25519 (ECIES X25519 AEAD Ratchet) है और `0` संगतता के लिए ElGamal फ़ॉलबैक है।
- स्थिरता के लिए स्पष्ट tunnel मात्राएँ: Java I2P डिफ़ॉल्ट **2**, i2pd डिफ़ॉल्ट **5**।

### प्रोटोकॉल संचालन

```
STREAM CONNECT ID=1 DESTINATION=b32address.i2p
STREAM SEND ID=1 SIZE=128
STREAM CLOSE ID=1
```
मुख्य संदेश प्रकारों में शामिल हैं: `STREAM CONNECT`, `STREAM ACCEPT`, `STREAM FORWARD`, `DATAGRAM SEND`, `RAW SEND`, `NAMING LOOKUP`, `DEST LOOKUP`, `PING`, `QUIT`।

### सुचारु शटडाउन

```
QUIT
```
## 4. कार्यान्वयन अंतर (Java I2P बनाम i2pd)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Java I2P 2.10.0</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">i2pd 2.58.0 (Sept&nbsp;2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SAM enabled by default</td><td style="border:1px solid var(--color-border); padding:0.5rem;">❌ Requires manual enable in router console</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✅ Enabled via `enabled=true` in `i2pd.conf`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default ports</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP 7656 / UDP 7655</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Same</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">AUTH / USER / PASSWORD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PING / PONG keepalive</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">QUIT / STOP / EXIT commands</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">FROM_PORT / TO_PORT / PROTOCOL</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY/SUBSESSION support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 0.9.47)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Absent</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SESSION ADD / REMOVE</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 2.9.0)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSL/TLS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ None</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default tunnel quantities</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=5</td></tr>
  </tbody>
</table>
**सिफारिश:** क्रॉस router संगतता सुनिश्चित करने के लिए हमेशा tunnel की संख्या स्पष्ट रूप से निर्दिष्ट करें।

## 5. समर्थित लाइब्रेरीज़ (2025 स्नैपशॉट)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maintenance Status (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">libsam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Maintained by I2P Project (eyedeekay)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">i2psam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal updates since 2019</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/sam3">sam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active; migrated from `eyedeekay/sam3`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/onramp">onramp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actively maintained (2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2plib">i2plib</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Modern async replacement for `i2p.socket`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">i2p.socket</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Abandoned (last release 2017)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://i2pgit.org/robin/Py2p">Py2p</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unverified/inactive</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">i2p-rs</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental; unstable API</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">@diva.exchange/i2p-sam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">TypeScript / JS</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Most actively maintained (2024–2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/I2PSharp">I2PSharp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Functional; light maintenance</td></tr>
  </tbody>
</table>
## 6. आगामी और नई सुविधाएँ (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NAMING LOOKUP `OPTIONS=true`</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 formats</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ (Java only)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid crypto (ML KEM)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java 17+ runtime requirement</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Planned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.11.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P over Tor blocking</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Improved floodfill selection</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0+</td></tr>
  </tbody>
</table>
## 7. सुरक्षा और कॉन्फ़िगरेशन नोट्स

- SAM को केवल `127.0.0.1` पर bind करें।
- स्थायी सेवाओं के लिए, स्थिर keys के साथ **PRIMARY** sessions का उपयोग करें।
- सुविधा समर्थन की जाँच के लिए `HELLO VERSION` का उपयोग करें।
- router की सक्रियता सत्यापित करने के लिए `PING` या `NAMING LOOKUP` का उपयोग करें।
- अप्रमाणित रिमोट SAM कनेक्शन से बचें (i2pd में TLS नहीं है)।

## 8. संदर्भ और विनिर्देश

- [SAM v3 विशिष्टता](/docs/api/samv3/)
- [SAM v2 (लिगेसी)](/docs/legacy/samv2/)
- [स्ट्रीमिंग विशिष्टता](/docs/specs/streaming/)
- [डेटाग्राम](/docs/api/datagrams/)
- [दस्तावेज़ीकरण हब](/docs/)
- [i2pd दस्तावेज़ीकरण](https://i2pd.website/docs)

## 9. सारांश

SAM v3 सभी गैर-Java I2P अनुप्रयोगों के लिए **अनुशंसित ब्रिज प्रोटोकॉल** बना हुआ है। यह स्थिरता, क्रॉस लैंग्वेज बाइंडिंग्स, और router प्रकारों में सुसंगत प्रदर्शन प्रदान करता है।

SAM के साथ विकास करते समय: - **Ed25519** signatures और **X25519** encryption का उपयोग करें। - `HELLO VERSION` के माध्यम से सुविधा समर्थन को गतिशील रूप से सत्यापित करें। - संगतता के लिए डिज़ाइन करें, विशेष रूप से जब Java I2P और i2pd routers दोनों का समर्थन कर रहे हों।
