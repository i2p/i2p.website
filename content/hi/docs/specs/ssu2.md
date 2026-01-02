---
title: "SSU2 विनिर्देश"
description: "सुरक्षित अर्ध-विश्वसनीय UDP ट्रांसपोर्ट प्रोटोकॉल संस्करण 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. अवलोकन

SSU2 एक UDP-आधारित ट्रांसपोर्ट-लेयर प्रोटोकॉल है, जिसका उपयोग I2P में सुरक्षित, अर्ध-विश्वसनीय router से router के बीच संचार के लिए किया जाता है। यह सामान्य-उद्देश्य ट्रांसपोर्ट नहीं है, बल्कि **I2NP संदेश विनिमय** के लिए विशेषीकृत है।

### मुख्य क्षमताएँ

- Noise XK pattern (Noise प्रोटोकॉल का XK पैटर्न) के माध्यम से प्रमाणित कुंजी विनिमय
- DPI (डीप पैकेट इंस्पेक्शन) प्रतिरोध के लिए एन्क्रिप्टेड हेडर
- रिले और hole-punching (NAT के पीछे साथियों के बीच सीधे कनेक्शन स्थापित करने की तकनीक) का उपयोग करके NAT (नेटवर्क एड्रेस ट्रांसलेशन) ट्रैवर्सल
- कनेक्शन माइग्रेशन और पते का सत्यापन
- वैकल्पिक पथ सत्यापन
- Forward secrecy (अग्र-गोपनीयता) और replay protection (रीप्ले हमलों से सुरक्षा)

### लेगेसी (पुरानी प्रणालियाँ) और संगतता

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2 Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU1 Removed</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.61</td></tr>
  </tbody>
</table>
SSU1 अब पूरे सार्वजनिक I2P नेटवर्क में उपयोग में नहीं है।

---

## 2. क्रिप्टोग्राफी

SSU2 I2P-विशिष्ट एक्सटेंशनों के साथ **Noise_XK_25519_ChaChaPoly_SHA256** का उपयोग करता है।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie-Hellman</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (RFC 7748)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32-byte keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Cipher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (RFC 7539)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD encryption</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Used for key derivation and message integrity</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KDF</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HKDF-SHA256 (RFC 5869)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">For session and header keys</td></tr>
  </tbody>
</table>
`mixHash()` के माध्यम से हेडर और पेलोड को क्रिप्टोग्राफिक रूप से बाँधा जाता है.   कार्यान्वयन दक्षता के लिए, सभी क्रिप्टोग्राफिक प्रिमिटिव्स (मूलभूत क्रिप्टो घटक) NTCP2 और ECIES के साथ साझा किए जाते हैं.

---

## 3. संदेश का अवलोकन

### 3.1 UDP डेटाग्राम नियम

- प्रत्येक UDP डेटाग्राम में **ठीक एक SSU2 संदेश** होता है.  
- Session Confirmed (सेशन पुष्टिकृत) संदेश कई डेटाग्रामों में खंडित किए जा सकते हैं.

**न्यूनतम आकार:** 40 बाइट्स   **अधिकतम आकार:** 1472 बाइट्स (IPv4) / 1452 बाइट्स (IPv6)

### 3.2 संदेश प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Header</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake initiation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Created</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake response</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Confirmed</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Final handshake, may be fragmented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted I2NP message blocks</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT reachability testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token or rejection notice</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Request for validation token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal signaling</td></tr>
  </tbody>
</table>
---

## 4. सत्र स्थापना

### 4.1 मानक प्रवाह (वैध टोकन)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.2 टोकन प्राप्ति

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.3 अमान्य टोकन

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```
---

## 5. हेडर संरचनाएँ

### 5.1 लंबा हेडर (32 बाइट्स)

सत्र स्थापना से पहले उपयोग किया जाता है (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random unique ID</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random (ignored during handshake)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Always 2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NetID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2 = main I2P network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved (0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Source Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random ID distinct from destination</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token for address validation</td></tr>
  </tbody>
</table>
### 5.2 संक्षिप्त हेडर (16 बाइट्स)

स्थापित सत्रों के दौरान उपयोग किया जाता है (SessionConfirmed, Data).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Stable throughout session</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Incrementing per message</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type (2 or 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ACK/fragment flags</td></tr>
  </tbody>
</table>
---

## 6. कूटलेखन

### 6.1 AEAD (संबद्ध डेटा के साथ प्रमाणित एन्क्रिप्शन)

सभी पेलोड **ChaCha20/Poly1305 AEAD** (संबद्ध डेटा सहित प्रमाणीकरणयुक्त एन्क्रिप्शन) से एन्क्रिप्ट किए जाते हैं:

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```
- Nonce (एक बार प्रयुक्त मान): 12 बाइट्स (4 शून्य + 8 काउंटर)
- टैग: 16 बाइट्स
- संबद्ध डेटा: अखंडता बाइंडिंग के लिए हेडर शामिल करता है

### 6.2 हेडर सुरक्षा

हेडर सत्र हेडर कुंजियों से व्युत्पन्न ChaCha20 keystream (स्ट्रीम सिफर से उत्पन्न कुंजी-धारा) का उपयोग करके मास्क किए जाते हैं। यह सुनिश्चित करता है कि सभी Connection IDs (कनेक्शन पहचानकर्ता) और पैकेट फ़ील्ड यादृच्छिक प्रतीत हों, जिससे DPI (Deep Packet Inspection) के प्रति प्रतिरोधकता मिलती है।

### 6.3 कुंजी व्युत्पत्ति

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Phase</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Initial</td><td style="border:1px solid var(--color-border); padding:0.6rem;">introKey + salt</td><td style="border:1px solid var(--color-border); padding:0.6rem;">handshake header key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake</td><td style="border:1px solid var(--color-border); padding:0.6rem;">DH(X25519)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey + AEAD key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Data phase</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">TX/RX keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Key rotation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">oldKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">newKey</td></tr>
  </tbody>
</table>
---

## 7. सुरक्षा और Replay (दोहराए गए हमले) की रोकथाम

- टोकन प्रति‑IP जारी किए जाते हैं, जो ~60 सेकंड में समाप्त हो जाते हैं.  
- रीप्ले को प्रति‑सत्र Bloom filters (प्रायिकता-आधारित सदस्यता जाँच संरचना) के माध्यम से रोका जाता है.  
- डुप्लिकेट अल्पकालिक कुंजियाँ अस्वीकृत कर दी जाती हैं.  
- हेडर और पेलोड क्रिप्टोग्राफ़िक रूप से परस्पर जुड़े होते हैं.

Routers को AEAD (Authenticated Encryption with Associated Data; संबद्ध डेटा सहित प्रमाणीकृत एन्क्रिप्शन) प्रमाणीकरण में विफल, या अमान्य संस्करण या NetID वाले किसी भी पैकेट को त्याग देना चाहिए।

---

## 8. पैकेट क्रमांकन और सत्र का जीवनकाल

प्रत्येक दिशा अपना स्वयं का 32-बिट काउंटर बनाए रखती है।   - 0 से शुरू होता है, प्रत्येक पैकेट पर बढ़ता है।   - रैप नहीं होना चाहिए; 2³² तक पहुँचने से पहले session rekey (सेशन की बदलना) करें या सत्र समाप्त करें।

कनेक्शन IDs पूरे सत्र के दौरान अपरिवर्तित रहती हैं, माइग्रेशन के दौरान भी।

---

## 9. डेटा चरण

- प्रकार = 6 (डेटा)
- संक्षिप्त हेडर (16 बाइट्स)
- पेलोड में एक या अधिक एन्क्रिप्टेड ब्लॉक होते हैं:
  - ACK/NACK सूचियाँ
  - I2NP संदेश खंड
  - पैडिंग (0–31 बाइट्स यादृच्छिक)
  - समापन ब्लॉक (वैकल्पिक)

चयनात्मक पुनः-प्रेषण (selective retransmission) और क्रम-बाह्य डिलीवरी (out-of-order delivery) समर्थित हैं। विश्वसनीयता “अर्ध-विश्वसनीय” (semi-reliable) बनी रहती है — पुनःप्रयास सीमाएँ पार होने के बाद गुम पैकेटों को चुपचाप त्याग दिया जा सकता है।

---

## 10. रिले और NAT पारगमन

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Determines inbound reachability</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Issues new token or rejection</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Requests new address token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Coordinates NAT hole punching</td></tr>
  </tbody>
</table>
रिले routers इन नियंत्रण संदेशों का उपयोग करके प्रतिबंधात्मक NATs के पीछे स्थित पीयर्स की सहायता करते हैं।

---

## 11. सत्र समाप्ति

किसी भी peer (सहकर्मी नोड) एक Data message (डेटा संदेश) के भीतर **Termination block** (समापन ब्लॉक) का उपयोग करके सत्र को बंद कर सकता है। प्राप्त होते ही संसाधनों को तुरंत मुक्त कर देना चाहिए। स्वीकृति के बाद दोहराए गए समापन पैकेटों को नज़रअंदाज़ किया जा सकता है।

---

## 12. कार्यान्वयन दिशानिर्देश

Routers **MUST**: - version = 2 और NetID = 2 को सत्यापित करें.   - 40 बाइट से छोटे पैकेट या अमान्य AEAD को ड्रॉप करें.   - 120s replay cache (रीप्ले कैश) लागू करें.   - पुन: उपयोग किए गए टोकन या ephemeral keys (क्षणिक कुंजियाँ) को अस्वीकार करें.

Routers **SHOULD**: - 0–31 बाइट की पैडिंग को यादृच्छिक करें.   - अनुकूली पुनर्प्रेषण का उपयोग करें (RFC 6298).   - स्थानांतरण से पहले प्रति-पीयर पथ सत्यापन लागू करें.

---

## 13. सुरक्षा सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Achieved By</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Forward secrecy</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 ephemeral keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Replay protection</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tokens + Bloom filter</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated encryption</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KCI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Noise XK pattern</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">DPI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted headers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Relay + Hole Punch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Migration</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Static connection IDs</td></tr>
  </tbody>
</table>
---

## 14. संदर्भ

- [प्रस्ताव 159 – SSU2](/proposals/159-ssu2/)
- [Noise प्रोटोकॉल फ्रेमवर्क](https://noiseprotocol.org/noise.html)
- [RFC 9000 – QUIC ट्रांसपोर्ट](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9001 – QUIC TLS](https://datatracker.ietf.org/doc/html/rfc9001)
- [RFC 7539 – ChaCha20/Poly1305 AEAD (प्रमाणीकृत एन्क्रिप्शन के साथ संबद्ध डेटा)](https://datatracker.ietf.org/doc/html/rfc7539)
- [RFC 7748 – X25519 ECDH](https://datatracker.ietf.org/doc/html/rfc7748)
- [RFC 5869 – HKDF-SHA256](https://datatracker.ietf.org/doc/html/rfc5869)
