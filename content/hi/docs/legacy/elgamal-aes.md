---
title: "ElGamal/AES + SessionTag (सेशन टैग) एन्क्रिप्शन"
description: "ElGamal, AES, SHA-256, और one-time session tags (एक-बार उपयोग वाले सेशन टैग) को संयोजित करने वाला लेगेसी एंड-टू-एंड एन्क्रिप्शन"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **स्थिति:** यह दस्तावेज़ लेगेसी ElGamal/AES+SessionTag एन्क्रिप्शन प्रोटोकॉल का वर्णन करता है। यह केवल पिछड़ी संगतता के लिए समर्थित है, क्योंकि आधुनिक I2P संस्करण (2.10.0+) [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) (एक आधुनिक एन्क्रिप्शन स्कीम) का उपयोग करते हैं। ElGamal प्रोटोकॉल अप्रचलित है और केवल ऐतिहासिक तथा अंतरसंचालनीयता उद्देश्यों के लिए बनाए रखा गया है।

## अवलोकन

ElGamal/AES+SessionTag ने garlic संदेशों (I2P में कई संदेशों को एक साथ पैक किए गए संदेश) के लिए I2P का मूल end-to-end एन्क्रिप्शन तंत्र प्रदान किया। यह निम्न का संयोजन था:

- **ElGamal (2048-बिट)** — कुंजी आदान-प्रदान के लिए
- **AES-256/CBC** — पेलोड एन्क्रिप्शन के लिए
- **SHA-256** — हैशिंग और IV व्युत्पत्ति के लिए
- **Session Tags (32 बाइट्स) (सत्र टैग)** — एक-बार उपयोग वाले संदेश पहचानकर्ताओं के लिए

इस प्रोटोकॉल ने routers और गंतव्यों को स्थायी कनेक्शनों को बनाए बिना सुरक्षित रूप से संचार करने की अनुमति दी। प्रत्येक सत्र में असममित ElGamal एक्सचेंज के माध्यम से एक सममित AES कुंजी स्थापित की जाती थी, जिसके बाद उस सत्र का संदर्भ देने वाले हल्के "tagged" संदेश होते थे।

## प्रोटोकॉल का संचालन

### सत्र स्थापना (नया सत्र)

एक नया सत्र ऐसे संदेश के साथ शुरू हुआ, जिसमें दो अनुभाग थे:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
ElGamal ब्लॉक के अंदर का स्पष्ट-पाठ निम्न से मिलकर बना था:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### मौजूदा सत्र संदेश

एक बार सत्र स्थापित हो जाने पर, प्रेषक कैश किए गए सत्र टैग का उपयोग करके **existing-session** (मौजूदा सत्र) संदेश भेज सकता था:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Routers प्रेषित टैग्स को लगभग **15 मिनट** तक कैश करते थे, जिसके बाद जो टैग्स उपयोग में नहीं आए थे वे समाप्त हो जाते थे। प्रत्येक टैग ठीक **एक संदेश** के लिए मान्य था, ताकि correlation attacks (सहसंबंध हमले) को रोका जा सके।

### AES-एन्क्रिप्टेड ब्लॉक प्रारूप

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Routers, या तो Pre-IV (नए सत्रों के लिए) या सत्र टैग (मौजूदा सत्रों के लिए) से व्युत्पन्न सत्र कुंजी और IV (Initialization Vector, आरंभीकरण वेक्टर) का उपयोग करके डिक्रिप्ट करते हैं। डिक्रिप्शन के बाद, वे plaintext payload (सादा-पाठ पेलोड) के SHA-256 हैश की पुनर्गणना करके अखंडता सत्यापित करते हैं।

## Session Tag (सेशन टैग) प्रबंधन

- टैग **एकतरफ़ा** होते हैं: Alice → Bob के टैग Bob → Alice के लिए पुनः उपयोग नहीं किए जा सकते।
- टैग लगभग **15 मिनट** बाद समाप्त हो जाते हैं।
- Routers प्रति-गंतव्य session key managers (सत्र कुंजी प्रबंधक) बनाए रखते हैं ताकि टैग, कुंजियों, और समाप्ति समय को ट्रैक किया जा सके।
- एप्लिकेशन [I2CP options](/docs/specs/i2cp/) के माध्यम से टैग के व्यवहार को नियंत्रित कर सकते हैं:
  - **`i2cp.tagThreshold`** — पुनःपूर्ति से पहले कैश किए गए टैगों की न्यूनतम सीमा
  - **`i2cp.tagCount`** — प्रति संदेश नए टैगों की संख्या

इस तंत्र ने गणनात्मक रूप से महंगे ElGamal हैंडशेक्स को न्यूनतम किया, जबकि संदेशों के बीच unlinkability (आपस में लिंक न कर पाने की क्षमता) को बनाए रखा।

## विन्यास और दक्षता

Session tags (सेशन टैग्स) को I2P के उच्च विलंबता, गैर-क्रमबद्ध ट्रांसपोर्ट में दक्षता बढ़ाने के लिए पेश किया गया था। एक सामान्य विन्यास **प्रति संदेश 40 टैग** प्रदान करता था, जिससे लगभग 1.2 KB का ओवरहेड जुड़ जाता था। एप्लिकेशन अपेक्षित ट्रैफिक के आधार पर डिलीवरी व्यवहार समायोजित कर सकते थे:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
Routers समय-समय पर समाप्त हो चुके टैगों को हटाते हैं और अप्रयुक्त सत्र स्थिति को छांटते हैं, ताकि मेमोरी उपयोग कम हो और tag-flooding (टैगों की बाढ़) हमलों का शमन हो।

## सीमाएँ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
इन कमियों ने सीधे [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) प्रोटोकॉल के डिज़ाइन के लिए प्रेरणा दी, जो perfect forward secrecy (पूर्ण अग्र-गोपनीयता), authenticated encryption (प्रमाणित एन्क्रिप्शन), और कुशल key exchange (कुंजी विनिमय) प्रदान करता है।

## अप्रचलन और स्थानांतरण की स्थिति

- **प्रस्तुत किया गया:** I2P के शुरुआती रिलीज़ (pre-0.6)
- **अप्रचलित:** ECIES-X25519 (एलिप्टिक-कर्व आधारित कुंजी-अदला-बदली और एन्क्रिप्शन योजना) के परिचय के साथ (0.9.46 → 0.9.48)
- **हटा दिया गया:** 2.4.0 से डिफ़ॉल्ट नहीं रहा (दिसंबर 2023)
- **समर्थित:** केवल पुराने संस्करणों के साथ संगतता मात्र

आधुनिक routers और गंतव्य अब **क्रिप्टो प्रकार 4 (ECIES-X25519)** की घोषणा करते हैं **प्रकार 0 (ElGamal/AES)** के बजाय। पुराना प्रोटोकॉल पुराने पीयर्स के साथ interoperability (अंतःपरिचालन) के लिए अब भी मान्य है, लेकिन नए परिनियोजनों में इसका उपयोग नहीं किया जाना चाहिए।

## ऐतिहासिक संदर्भ

ElGamal/AES+SessionTag I2P की शुरुआती कूटलेखी संरचना के लिए आधारभूत था। इसके संकर डिज़ाइन ने एक-बार-उपयोग सेशन टैग और एक-दिशात्मक सेशन जैसे नवाचार पेश किए, जिन्होंने आगामी प्रोटोकॉलों के विकास को दिशा दी। इनमें से कई विचार आधुनिक रचनाओं में विकसित हुए, जैसे deterministic ratchets (नियतात्मक रैचेट: कुंजी-उन्नयन तंत्र) और संकर पोस्ट-क्वांटम कुंजी विनिमय।
