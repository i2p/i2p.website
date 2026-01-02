---
title: "SOCKS प्रॉक्सी"
description: "I2P के SOCKS tunnel का सुरक्षित उपयोग (2.10.0 के लिए अद्यतन)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **सावधानी:** SOCKS tunnel एप्लिकेशन payloads को बिना sanitize किए forward करता है। कई protocols IPs, hostnames, या अन्य identifiers leak करते हैं। केवल उस software के साथ SOCKS का उपयोग करें जिसे आपने anonymity के लिए audit किया है।

---

## 1. अवलोकन

I2P **SOCKS 4, 4a, और 5** proxy समर्थन प्रदान करता है outbound connections के लिए एक **I2PTunnel client** के माध्यम से। यह मानक applications को I2P destinations तक पहुंचने में सक्षम बनाता है लेकिन **clearnet तक पहुंच नहीं** सकता। कोई **SOCKS outproxy नहीं** है, और सभी traffic I2P network के भीतर ही रहता है।

### कार्यान्वयन सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**समर्थित पता प्रकार:** - `.i2p` होस्टनाम (addressbook प्रविष्टियाँ) - Base32 हैश (`.b32.i2p`) - Base64 या clearnet समर्थन नहीं

---

## 2. सुरक्षा जोखिम और सीमाएं

### एप्लिकेशन-लेयर लीकेज

SOCKS एप्लिकेशन लेयर के नीचे काम करता है और प्रोटोकॉल को सैनिटाइज नहीं कर सकता। कई क्लाइंट (जैसे, ब्राउज़र, IRC, ईमेल) में मेटाडेटा शामिल होता है जो आपका IP एड्रेस, होस्टनेम, या सिस्टम विवरण प्रकट कर देता है।

सामान्य लीक में शामिल हैं: - मेल हेडर या IRC CTCP प्रतिक्रियाओं में IP   - प्रोटोकॉल पेलोड में वास्तविक नाम/उपयोगकर्ता नाम   - OS फिंगरप्रिंट वाले User-agent स्ट्रिंग   - बाहरी DNS क्वेरी   - WebRTC और ब्राउज़र टेलीमेट्री

**I2P इन लीक को रोक नहीं सकता**—ये tunnel परत के ऊपर होते हैं। केवल गुमनामी के लिए डिज़ाइन किए गए **ऑडिटेड क्लाइंट** के लिए ही SOCKS का उपयोग करें।

### साझा टनल पहचान

यदि कई एप्लिकेशन एक SOCKS tunnel साझा करते हैं, तो वे समान I2P destination identity साझा करते हैं। यह विभिन्न सेवाओं में correlation या fingerprinting को सक्षम बनाता है।

**समाधान:** प्रत्येक एप्लिकेशन के लिए **non-shared tunnels** का उपयोग करें और रीस्टार्ट के दौरान सुसंगत क्रिप्टोग्राफिक पहचान बनाए रखने के लिए **persistent keys** को सक्षम करें।

### UDP मोड स्टब्ड आउट

SOCKS5 में UDP समर्थन लागू नहीं किया गया है। प्रोटोकॉल UDP क्षमता का विज्ञापन करता है, लेकिन कॉल्स को नजरअंदाज कर दिया जाता है। केवल TCP क्लाइंट्स का उपयोग करें।

### डिज़ाइन के अनुसार कोई Outproxy नहीं

Tor के विपरीत, I2P SOCKS-आधारित clearnet outproxies प्रदान **नहीं** करता है। बाहरी IP तक पहुँचने का प्रयास विफल हो जाएगा या पहचान उजागर कर देगा। यदि outproxying आवश्यक है तो HTTP या HTTPS proxies का उपयोग करें।

---

## 3. ऐतिहासिक संदर्भ

डेवलपर्स ने लंबे समय से गुमनाम उपयोग के लिए SOCKS को हतोत्साहित किया है। आंतरिक डेवलपर चर्चाओं और 2004 की [Meeting 81](/hi/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) और [Meeting 82](/hi/blog/2004/03/23/i2p-dev-meeting-march-23-2004/) से:

> "मनमाना ट्रैफ़िक को फ़ॉरवर्ड करना असुरक्षित है, और गुमनामी सॉफ़्टवेयर के डेवलपर्स के रूप में हमारे लिए यह आवश्यक है कि हम अपने अंतिम उपयोगकर्ताओं की सुरक्षा को अपने दिमाग में सर्वोपरि रखें।"

SOCKS समर्थन संगतता के लिए शामिल किया गया था लेकिन उत्पादन वातावरण के लिए अनुशंसित नहीं है। लगभग हर इंटरनेट एप्लिकेशन संवेदनशील मेटाडेटा लीक करता है जो गुमनाम रूटिंग के लिए उपयुक्त नहीं है।

---

## 4. कॉन्फ़िगरेशन

### Java I2P

1. [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel) खोलें  
2. **"SOCKS 4/4a/5"** प्रकार की एक नई क्लाइंट tunnel बनाएं  
3. विकल्पों को कॉन्फ़िगर करें:  
   - लोकल पोर्ट (कोई भी उपलब्ध)  
   - शेयर्ड क्लाइंट: प्रत्येक ऐप के लिए अलग पहचान हेतु *अक्षम* करें  
   - पर्सिस्टेंट की: की सहसंबंध को कम करने के लिए *सक्षम* करें  
4. tunnel शुरू करें

### i2pd

i2pd में SOCKS5 समर्थन डिफ़ॉल्ट रूप से `127.0.0.1:4447` पर सक्षम होता है। `i2pd.conf` में `[SOCKSProxy]` के अंतर्गत कॉन्फ़िगरेशन आपको पोर्ट, होस्ट और tunnel पैरामीटर समायोजित करने की अनुमति देता है।

---

## 5. विकास समयरेखा

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
SOCKS मॉड्यूल में 2013 के बाद से कोई बड़े प्रोटोकॉल अपडेट नहीं हुए हैं, लेकिन इसके आसपास के tunnel stack में प्रदर्शन और क्रिप्टोग्राफिक सुधार हुए हैं।

---

## 6. अनुशंसित विकल्प

किसी भी **production**, **public-facing**, या **security-critical** एप्लिकेशन के लिए, SOCKS के बजाय आधिकारिक I2P APIs में से किसी एक का उपयोग करें:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
ये APIs उचित गंतव्य अलगाव, क्रिप्टोग्राफिक पहचान नियंत्रण, और बेहतर routing प्रदर्शन प्रदान करते हैं।

---

## 7. OnionCat / GarliCat

OnionCat अपने GarliCat मोड (`fd60:db4d:ddb5::/48` IPv6 रेंज) के माध्यम से I2P का समर्थन करता है। अभी भी कार्यात्मक है लेकिन 2019 के बाद से सीमित विकास के साथ।

**उपयोग संबंधी सावधानियां:** - SusiDNS में मैन्युअल `.oc.b32.i2p` कॉन्फ़िगरेशन की आवश्यकता होती है   - स्थिर IPv6 असाइनमेंट की आवश्यकता होती है   - I2P प्रोजेक्ट द्वारा आधिकारिक रूप से समर्थित नहीं

केवल उन्नत VPN-over-I2P सेटअप के लिए अनुशंसित।

---

## 8. सर्वोत्तम प्रथाएं

यदि आपको SOCKS का उपयोग करना ही है: 1. प्रत्येक एप्लिकेशन के लिए अलग tunnels बनाएं।   2. shared client mode को अक्षम करें।   3. persistent keys को सक्षम करें।   4. SOCKS5 DNS resolution को बाध्य करें।   5. लीक के लिए प्रोटोकॉल व्यवहार की जांच करें।   6. clearnet कनेक्शन से बचें।   7. लीक के लिए नेटवर्क ट्रैफ़िक की निगरानी करें।

---

## 9. तकनीकी सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. निष्कर्ष

I2P में SOCKS proxy मौजूदा TCP applications के साथ बुनियादी संगतता प्रदान करता है लेकिन यह **मजबूत गुमनामी की गारंटी के लिए डिज़ाइन नहीं किया गया है**। इसका उपयोग केवल नियंत्रित, ऑडिट किए गए परीक्षण वातावरण के लिए किया जाना चाहिए।

> गंभीर तैनाती के लिए, **SAM v3** या **Streaming API** में माइग्रेट करें। ये API एप्लिकेशन पहचान को अलग करते हैं, आधुनिक क्रिप्टोग्राफी का उपयोग करते हैं, और निरंतर विकास प्राप्त करते हैं।

---

### अतिरिक्त संसाधन

- [आधिकारिक SOCKS दस्तावेज़](/docs/api/socks/)  
- [SAM v3 विनिर्देश](/docs/api/samv3/)  
- [Streaming Library दस्तावेज़](/docs/specs/streaming/)  
- [I2PTunnel संदर्भ](/docs/specs/implementation/)  
- [I2P डेवलपर दस्तावेज़](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [समुदाय मंच](https://i2pforum.net)
