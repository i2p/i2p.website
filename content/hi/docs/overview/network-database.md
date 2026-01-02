---
title: "नेटवर्क डेटाबेस"
description: "I2P के वितरित नेटवर्क डेटाबेस (netDb) को समझना - router संपर्क जानकारी और गंतव्य खोज के लिए एक विशेषीकृत वितरित हैश तालिका (DHT)"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. सारांश

**netDb** एक विशेषीकृत वितरित डेटाबेस है, जिसमें केवल दो प्रकार के डेटा होते हैं:
- **RouterInfos** – router संपर्क जानकारी
- **LeaseSets** – गंतव्य संपर्क जानकारी

सारा डेटा क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित और सत्यापन योग्य है। प्रत्येक प्रविष्टि में liveliness information (सक्रियता/उपलब्धता संबंधी जानकारी) शामिल होती है, जो अप्रचलित प्रविष्टियों को हटाने और पुरानी प्रविष्टियों को बदलने में सहायक होती है, और कुछ श्रेणियों के हमलों के विरुद्ध सुरक्षा प्रदान करती है।

वितरण में **floodfill** तंत्र का उपयोग किया जाता है, जहाँ routers का एक उपसमूह वितरित डेटाबेस को बनाए रखता है।

---

## 2. RouterInfo (router की जानकारी)

जब routers को अन्य routers से संपर्क करना होता है, तो वे **RouterInfo** (router से संबंधित जानकारी) बंडलों का आदान-प्रदान करते हैं, जिनमें शामिल हैं:

- **Router की पहचान** – एन्क्रिप्शन कुंजी, साइनिंग कुंजी, प्रमाणपत्र
- **संपर्क पते** – router तक कैसे पहुँचा जाए
- **प्रकाशन समय-चिह्न** – यह जानकारी कब प्रकाशित की गई थी
- **मनमाने पाठ विकल्प** – क्षमता फ्लैग्स (संकेत-चिह्न) और सेटिंग्स
- **क्रिप्टोग्राफिक हस्ताक्षर** – प्रामाणिकता सिद्ध करता है

### 2.1 क्षमता फ्लैग्स

Routers अपनी RouterInfo में अक्षरीय कोडों के जरिए अपनी क्षमताएँ घोषित करते हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 बैंडविड्थ श्रेणियाँ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 नेटवर्क आईडी मान

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 RouterInfo (I2P router की जानकारी) आँकड़े

Routers नेटवर्क विश्लेषण के लिए वैकल्पिक स्वास्थ्य आँकड़े प्रकाशित करते हैं: - Exploratory tunnel (अन्वेषणात्मक tunnel) निर्माण सफलता/अस्वीकृति/समय-सीमा समाप्ति दरें - 1-घंटे का औसत भाग लेने वाले tunnel की संख्या

आँकड़े `stat_(statname).(statperiod)` प्रारूप का पालन करते हैं, जिसमें मान सेमीकोलन से अलग किए गए होते हैं।

**उदाहरण आँकड़े:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers भी प्रकाशित कर सकते हैं: `netdb.knownLeaseSets` और `netdb.knownRouters`

### 2.5 Family (परिवार) विकल्प

रिलीज़ 0.9.24 से, routers अपनी परिवार सदस्यता (एक ही ऑपरेटर) घोषित कर सकते हैं:

- **family**: परिवार का नाम
- **family.key**: हस्ताक्षर प्रकार कोड, base64-एन्कोडेड हस्ताक्षर हेतु सार्वजनिक कुंजी के साथ संयोजित
- **family.sig**: परिवार के नाम और 32-बाइट router हैश का हस्ताक्षर

एक ही tunnel में, एक ही family के एक से अधिक routers इस्तेमाल नहीं किए जाएंगे।

### 2.6 RouterInfo की समाप्ति

- अपटाइम के पहले घंटे के दौरान कोई समाप्ति नहीं
- संग्रहीत RouterInfos की संख्या 25 या कम होने पर कोई समाप्ति नहीं
- स्थानीय गणना बढ़ने पर समाप्ति अवधि घटती है (<120 routers पर 72 घंटे; 300 routers पर ~30 घंटे)
- SSU introducers (परिचायक नोड) ~1 घंटे में समाप्त हो जाते हैं
- Floodfills सभी स्थानीय RouterInfos के लिए 1 घंटे की समाप्ति का उपयोग करते हैं

---

## 3. LeaseSet

**LeaseSets** विशिष्ट गंतव्यों के लिए tunnel प्रवेश बिंदुओं का दस्तावेज़ित करते हैं, और निम्नलिखित निर्दिष्ट करते हैं:

- **Tunnel गेटवे router की पहचान**
- **4-बाइट tunnel ID**
- **Tunnel समाप्ति समय**

LeaseSets में शामिल हैं: - **Destination** – एन्क्रिप्शन कुंजी, साइनिंग कुंजी, प्रमाणपत्र - **अतिरिक्त एन्क्रिप्शन सार्वजनिक कुंजी** – एंड-टू-एंड garlic encryption के लिए - **अतिरिक्त साइनिंग सार्वजनिक कुंजी** – निरस्तीकरण के लिए (वर्तमान में अप्रयुक्त) - **क्रिप्टोग्राफिक हस्ताक्षर**

### 3.1 LeaseSet के प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 LeaseSet समाप्ति

सामान्य LeaseSets अपनी सबसे अंतिम लीज़ की समाप्ति पर समाप्त हो जाते हैं। LeaseSet2 की समाप्ति शीर्षलेख में निर्दिष्ट होती है। EncryptedLeaseSet और MetaLeaseSet की समाप्ति भिन्न हो सकती है, और उन पर संभावित अधिकतम सीमा लागू की जा सकती है।

---

## 4. बूटस्ट्रैपिंग

विकेंद्रीकृत netDb के साथ एकीकृत होने के लिए कम से कम एक पीयर संदर्भ आवश्यक होता है। **Reseeding** (नेटवर्क के लिए प्रारंभिक RouterInfo प्राप्त करने की प्रक्रिया) स्वयंसेवकों की netDb डायरेक्टरीज़ से RouterInfo फाइलें (`routerInfo-$hash.dat`) प्राप्त करता है। पहले स्टार्टअप पर यह स्वतः ही यादृच्छिक रूप से चुने गए हार्डकोड किए गए URLs से उन्हें प्राप्त करता है।

---

## 5. Floodfill तंत्र (I2P में netDb के वितरित सूचीकरण और वितरण की व्यवस्था)

floodfill netDb सरल वितरित भंडारण का उपयोग करता है: डेटा को सबसे निकट floodfill पीयर को भेजता है। जब गैर‑floodfill पीयर स्टोर संदेश भेजते हैं, तो floodfill उन्हें विशिष्ट कुंजी के सबसे निकट स्थित floodfill पीयर के एक उपसमुच्चय को अग्रेषित करते हैं।

Floodfill भागीदारी RouterInfo में एक क्षमता फ़्लैग (`f`) के रूप में दर्शाई जाती है।

### 5.1 Floodfill Opt-In आवश्यकताएँ

Tor के हार्डकोड किए गए विश्वसनीय डायरेक्टरी सर्वरों के विपरीत, I2P का floodfill समूह **अविश्वसनीय** है और समय के साथ बदलता रहता है।

Floodfill स्वतः केवल उन उच्च बैंडविड्थ वाले routers पर सक्षम होता है जो इन आवश्यकताओं को पूरा करते हैं: - न्यूनतम 128 KBytes/sec साझा बैंडविड्थ (मैन्युअल रूप से कॉन्फ़िगर की गई) - अतिरिक्त स्वास्थ्य परीक्षण पास करने चाहिए (outbound message queue time, job lag)

वर्तमान स्वचालित opt-in (सहमति देकर शामिल होना) के परिणामस्वरूप लगभग **6% नेटवर्क floodfill भागीदारी** होती है।

मैन्युअल रूप से कॉन्फ़िगर किए गए floodfills, स्वचालित स्वयंसेवकों के साथ मौजूद रहते हैं। जब floodfill की संख्या सीमा से नीचे गिरती है, तो उच्च-बैंडविड्थ routers स्वचालित रूप से स्वयंसेवा के लिए आगे आते हैं। जब बहुत अधिक floodfills मौजूद होते हैं, तो वे स्वयं un-floodfill हो जाते हैं (यानी floodfill मोड से बाहर हो जाते हैं)।

### 5.2 Floodfill भूमिकाएँ

netDb स्टोर्स स्वीकार करने और क्वेरियों का जवाब देने के अलावा, floodfills मानक router कार्य करते हैं। उनकी अधिक बैंडविड्थ आमतौर पर अधिक tunnel भागीदारी का मतलब होती है, लेकिन इसका डेटाबेस सेवाओं से सीधा संबंध नहीं है।

---

## 6. Kademlia (वितरित हैश तालिका प्रोटोकॉल) निकटता मेट्रिक

netDb XOR-आधारित **Kademlia-शैली** (Kademlia: एक वितरित हैश-टेबल एल्गोरिथ्म) दूरी मापन का उपयोग करता है। RouterIdentity या Destination का SHA256 हैश Kademlia कुंजी बनाता है (LS2 Encrypted LeaseSets को छोड़कर, जो type byte 3 तथा blinded public key (ब्लाइंडेड सार्वजनिक कुंजी) के SHA256 का उपयोग करते हैं)।

### 6.1 कुंजी-स्थान रोटेशन

Sybil attack (सिबिल हमला) की लागत बढ़ाने के लिए, `SHA256(key)` का उपयोग करने के बजाय, सिस्टम उपयोग करता है:

```
SHA256(key + yyyyMMdd)
```
जहाँ तिथि 8-बाइट ASCII UTC तिथि होती है। यह **routing key** (रूटिंग कुंजी) बनाता है, जो प्रतिदिन UTC मध्यरात्रि पर बदलती है—इसे **keyspace rotation** (कीस्पेस रोटेशन, यानी कुंजी-स्थान का दैनिक परिवर्तन) कहा जाता है।

रूटिंग कुंजियाँ कभी भी I2NP संदेशों में प्रेषित नहीं की जातीं; उनका उपयोग केवल स्थानीय दूरी निर्धारण के लिए किया जाता है।

---

## 7. नेटवर्क डेटाबेस (netDb) विभाजन

परंपरागत Kademlia DHTs संग्रहीत जानकारी की unlinkability (जोड़े न जा सकने की क्षमता) को बरकरार नहीं रखते। I2P **विभाजन** लागू करके उन हमलों को रोकता है जो client tunnels को routers से संबद्ध करते हैं।

### 7.1 विभाजन रणनीति

Routers ट्रैक करते हैं: - क्या प्रविष्टियाँ client tunnels के माध्यम से पहुँचीं या सीधे - यदि tunnel के माध्यम से, तो कौन-सा client tunnel/destination (गंतव्य) - एकाधिक tunnel आगमन ट्रैक किए जाते हैं - संग्रहण बनाम लुकअप प्रतिक्रियाओं में अंतर किया जाता है

Java और C++ दोनों कार्यान्वयन निम्न का उपयोग करते हैं: - एक **"Main" netDb** जो router संदर्भ में प्रत्यक्ष lookups/floodfill operations के लिए होता है - **"Client Network Databases"** या **"Sub-Databases"** client संदर्भों में, जहाँ client tunnels को भेजी गई प्रविष्टियाँ कैप्चर की जाती हैं

क्लाइंट netDbs केवल क्लाइंट के जीवनकाल तक ही अस्तित्व में रहते हैं और इनमें केवल क्लाइंट tunnel प्रविष्टियाँ होती हैं। क्लाइंट tunnels की प्रविष्टियाँ प्रत्यक्ष आगमन के साथ ओवरलैप नहीं कर सकतीं।

प्रत्येक netDb यह ट्रैक करता है कि प्रविष्टियाँ 'stores' के रूप में आई हैं (लुकअप अनुरोधों का उत्तर देने के लिए) या 'lookup replies' के रूप में (केवल तभी उत्तर देती हैं जब पहले से उसी डेस्टिनेशन (गंतव्य पता) पर संग्रहीत हों)। क्लाइंट कभी भी Main netDb प्रविष्टियों का उपयोग करके क्वेरियों का उत्तर नहीं देते; वे केवल क्लाइंट नेटवर्क डेटाबेस प्रविष्टियों से उत्तर देते हैं।

संयुक्त रणनीतियाँ क्लाइंट-router संबद्धता हमलों के विरुद्ध netDb को **विभाजित** करती हैं।

---

## 8. भंडारण, सत्यापन, और खोज

### 8.1 पीयर्स को RouterInfo का भंडारण

I2NP `DatabaseStoreMessage` जो NTCP या SSU ट्रांसपोर्ट कनेक्शन आरंभीकरण के दौरान स्थानीय RouterInfo के आदान-प्रदान को शामिल करता है।

### 8.2 पीयर्स पर LeaseSet भंडारण

I2NP `DatabaseStoreMessage`, जिसमें स्थानीय LeaseSet शामिल होता है, को समय-समय पर Destination (I2P में endpoint/पता) ट्रैफ़िक के साथ बंडल किए गए, garlic encryption से एन्क्रिप्ट किए गए संदेशों के जरिए अदला-बदली किया जाता है, जिससे LeaseSet लुकअप के बिना प्रतिक्रियाएँ संभव हो जाती हैं।

### 8.3 Floodfill चयन

`DatabaseStoreMessage` वर्तमान रूटिंग कुंजी के सबसे नज़दीकी floodfill को भेजा जाता है। सबसे नज़दीकी floodfill स्थानीय डेटाबेस खोज के जरिए पाया जाता है। भले ही वह वास्तव में सबसे नज़दीकी न हो, फ्लडिंग (एक साथ कई नोड्स को प्रसारण करने की प्रक्रिया) कई floodfills को भेजकर इसे "और नज़दीक" तक फैला देती है।

पारंपरिक Kademlia (एक वितरित हैश तालिका प्रोटोकॉल) सम्मिलन से पहले "find-closest" खोज (यानी "सबसे निकट" खोज) का उपयोग करती है। हालाँकि I2NP में ऐसे संदेश नहीं होते, routers वास्तविक निकटतम समकक्ष की खोज सुनिश्चित करने के लिए सबसे कम महत्वपूर्ण बिट को उलटकर (`key ^ 0x01`) आवर्ती खोज कर सकते हैं।

### 8.4 Floodfills पर RouterInfo (राउटर जानकारी) का भंडारण

routers एक floodfill से सीधे कनेक्ट करके RouterInfo प्रकाशित करते हैं, और शून्य से भिन्न Reply Token के साथ I2NP `DatabaseStoreMessage` भेजते हैं. संदेश end-to-end garlic encryption से एन्क्रिप्टेड नहीं होता (सीधा कनेक्शन, कोई मध्यस्थ नहीं). floodfill `DeliveryStatusMessage` के साथ उत्तर देता है, जहाँ Reply Token को Message ID के रूप में उपयोग किया जाता है.

Routers exploratory tunnel (कनेक्शन सीमाएँ, असंगतता, IP छुपाना) के माध्यम से भी RouterInfo (राउटर के बारे में वर्णन-सूचना) भेज सकते हैं। Floodfills अधिभार के दौरान ऐसे संग्रह अनुरोधों को अस्वीकार कर सकते हैं।

### 8.5 LeaseSet का Floodfills में संग्रहण

LeaseSet (I2P में किसी गंतव्य की कनेक्टिविटी जानकारी) का भंडारण, RouterInfo (router के बारे में जानकारी) की तुलना में अधिक संवेदनशील है। Routers को अपने साथ LeaseSet की संबद्धता को रोकना चाहिए।

Routers आउटबाउंड क्लाइंट tunnel के माध्यम से गैर-शून्य Reply Token के साथ `DatabaseStoreMessage` भेज कर LeaseSet प्रकाशित करते हैं। संदेश Destination (I2P में गंतव्य पहचान) के Session Key Manager का उपयोग कर end-to-end garlic encryption से सुरक्षित है, जिससे tunnel के आउटबाउंड endpoint से यह छिपा रहता है। Floodfill `DeliveryStatusMessage` के साथ उत्तर देता है, जो इनबाउंड tunnel के माध्यम से लौटाया जाता है।

### 8.6 Flooding (नेटवर्क में संदेश/डेटा को सभी नोड्स/पीयर्स तक व्यापक रूप से प्रसारित करने की विधि) प्रक्रिया

Floodfills स्थानीय रूप से संग्रहीत करने से पहले RouterInfo/LeaseSet का सत्यापन करते हैं; इसके लिए वे लोड, netdb के आकार, और अन्य कारकों पर निर्भर अनुकूली मानदंड अपनाते हैं।

मान्य नया डेटा प्राप्त करने के बाद, floodfills इसे "flood" करते हैं, routing key (रूटिंग कुंजी) के 3 सबसे नज़दीकी floodfill routers को ढूँढकर। प्रत्यक्ष कनेक्शन I2NP `DatabaseStoreMessage` शून्य Reply Token (जवाबी टोकन) के साथ भेजते हैं। अन्य routers न तो जवाब देते हैं और न ही दोबारा "flood" करते हैं।

**महत्वपूर्ण प्रतिबंध:** - Floodfills को tunnels के माध्यम से प्रसारित नहीं करना चाहिए; केवल प्रत्यक्ष कनेक्शन - Floodfills कभी भी अवधि-समाप्त LeaseSet या एक घंटे से अधिक पहले प्रकाशित RouterInfo को प्रसारित नहीं करते

### 8.7 RouterInfo और LeaseSet लुकअप

I2NP `DatabaseLookupMessage` floodfill routers से netdb प्रविष्टियाँ अनुरोध करता है। लुकअप्स आउटबाउंड अन्वेषणात्मक tunnel के माध्यम से भेजे जाते हैं; उत्तर वापसी के लिए किस इनबाउंड अन्वेषणात्मक tunnel का उपयोग करना है, यह निर्दिष्ट करते हैं।

लुकअप अनुरोध सामान्यतः अनुरोधित कुंजी के सबसे निकट वाले दो "good" floodfill routers को समानांतर रूप से भेजे जाते हैं।

- **स्थानीय मिलान**: I2NP `DatabaseStoreMessage` प्रतिक्रिया प्राप्त करता है
- **कोई स्थानीय मिलान नहीं**: कुंजी के निकट अन्य floodfill router संदर्भों के साथ I2NP `DatabaseSearchReplyMessage` प्राप्त करता है

LeaseSet लुकअप end-to-end garlic encryption का उपयोग करते हैं (0.9.5 से)। ElGamal की लागत के कारण RouterInfo (router की जानकारी) लुकअप एन्क्रिप्ट नहीं होते, जिससे वे आउटबाउंड एंडपॉइंट पर निगरानी के प्रति असुरक्षित हो जाते हैं।

संस्करण 0.9.7 से, लुकअप उत्तरों में सेशन कुंजी और टैग शामिल होते हैं, जिससे उत्तर इनबाउंड गेटवे से छिपे रहते हैं।

### 8.8 इटरेटिव लुकअप्स

0.8.9 से पहले: recursive (रिकर्सिव) या iterative (इटरेटिव) रूटिंग के बिना दो समानांतर रिडंडेंट लुकअप।

संस्करण 0.8.9 से: **Iterative lookups** (क्रमिक लुकअप प्रक्रिया) बिना अतिरिक्तता के लागू—अधिक कुशल, विश्वसनीय, और अपूर्ण floodfill ज्ञान के लिए उपयुक्त। जैसे-जैसे नेटवर्क बढ़ते हैं और routers कम floodfills जानते हैं, lookups O(log n) जटिलता के निकट पहुँचते हैं।

इटरेटिव लुकअप निकटतर पीयर संदर्भ न होने पर भी जारी रहते हैं, जिससे दुर्भावनापूर्ण black-holing (जानबूझकर ट्रैफ़िक को निगल कर रोक देना) रोकी जाती है। वर्तमान अधिकतम क्वेरी संख्या और टाइमआउट लागू हैं।

### 8.9 सत्यापन

**RouterInfo सत्यापन**: 0.9.7.1 से निष्क्रिय किया गया ताकि "Practical Attacks Against the I2P Network" शोधपत्र में वर्णित हमलों को रोका जा सके।

**LeaseSet सत्यापन**: Routers ~10 सेकंड प्रतीक्षा करते हैं, फिर outbound client tunnel के माध्यम से किसी अलग floodfill से लुकअप करते हैं। एंड-टू-एंड garlic encryption इसे outbound endpoint से छुपाती है। प्रत्युत्तर inbound tunnels के माध्यम से वापस आते हैं।

संस्करण 0.9.7 से, उत्तर इस प्रकार एन्क्रिप्ट किए जाते हैं कि सेशन कुंजी/टैग इनबाउंड गेटवे से छिपे रहें।

### 8.10 अन्वेषण

**अन्वेषण** में नए routers के बारे में जानने के लिए यादृच्छिक कुंजियों के साथ netdb लुकअप शामिल होता है। Floodfills `DatabaseSearchReplyMessage` के साथ उत्तर देते हैं, जिसमें अनुरोधित कुंजी के निकट non-floodfill router हैश शामिल होते हैं। अन्वेषण क्वेरियाँ `DatabaseLookupMessage` में एक विशेष फ़्लैग सेट करती हैं।

---

## 9. MultiHoming (एकाधिक नेटवर्क कनेक्शनों के जरिए एक ही सिस्टम/सेवा को जोड़ने की व्यवस्था)

समान निजी/सार्वजनिक कुंजियों (परंपरागत `eepPriv.dat`) का उपयोग करने वाले Destinations (I2P पते/पहचान) एक साथ कई routers पर होस्ट कर सकते हैं। प्रत्येक इंस्टेंस समय-समय पर हस्ताक्षरित LeaseSets प्रकाशित करता है; सबसे हाल में प्रकाशित LeaseSet ही लुकअप अनुरोधकर्ताओं को वापस मिलता है। जब LeaseSet की अधिकतम आयु 10 मिनट होती है, तो आउटेज अधिकतम लगभग 10 मिनट तक ही रहते हैं।

संस्करण 0.9.38 से, **Meta LeaseSets** अलग-अलग Destinations (I2P गंतव्य/पता) का उपयोग कर सामान्य सेवाएँ प्रदान करने वाली बड़ी multihomed (कई नेटवर्क इंटरफ़ेस/कनेक्शनों वाली) सेवाओं का समर्थन करती हैं। Meta LeaseSet प्रविष्टियाँ Destinations या अन्य Meta LeaseSets होती हैं, जिनका समाप्ति समय अधिकतम 18.2 घंटे तक होता है, जिससे सामान्य सेवाएँ होस्ट करने वाले सैकड़ों/हज़ारों Destinations सक्षम होते हैं।

---

## 10. खतरा विश्लेषण

वर्तमान में लगभग 1700 floodfill routers (विशेष routers जो netDb में डेटा वितरित और संग्रहित करते हैं) कार्यरत हैं। नेटवर्क का विस्तार अधिकांश हमलों को अधिक कठिन या कम प्रभावशाली बना देता है।

### 10.1 सामान्य शमन उपाय

- **वृद्धि**: अधिक floodfills हमलों को कठिन या कम असरदार बना देते हैं
- **अतिरिक्तता**: सभी netdb प्रविष्टियाँ फ्लडिंग के माध्यम से कुंजी के सबसे निकट 3 floodfill routers पर संग्रहीत की जाती हैं
- **हस्ताक्षर**: सभी प्रविष्टियाँ निर्माता द्वारा हस्ताक्षरित होती हैं; जालसाज़ी असंभव है

### 10.2 धीमे या अनुत्तरदायी Routers

Routers floodfills के लिए विस्तारित पीयर प्रोफ़ाइल आँकड़े बनाए रखते हैं: - औसत प्रतिक्रिया समय - क्वेरी उत्तर प्रतिशत - स्टोर सत्यापन सफलता प्रतिशत - अंतिम सफल स्टोर - अंतिम सफल लुकअप - अंतिम प्रतिक्रिया

सबसे निकटतम floodfill के चयन हेतु "goodness" (उपयुक्तता सूचक) निर्धारित करते समय routers इन मापदंडों का उपयोग करते हैं। जो routers बिल्कुल भी प्रतिक्रिया नहीं देते, उन्हें शीघ्र पहचाना और टाला जाता है; आंशिक रूप से दुर्भावनापूर्ण routers अधिक चुनौती पेश करते हैं।

### 10.3 Sybil हमला (पूर्ण Keyspace (कुंजी-स्थान))

हमलावर एक प्रभावी DoS हमले के तौर पर पूरे keyspace (कुंजी-परास) में बिखरे हुए अनेक floodfill routers बना सकते हैं।

यदि "bad" के रूप में नामित करने लायक पर्याप्त गलत व्यवहार नहीं है, तो संभावित प्रतिक्रियाएँ शामिल हैं: - कंसोल समाचार, वेबसाइट, फ़ोरम के माध्यम से घोषित खराब router हैश/IP सूचियों का संकलन - नेटवर्क-व्यापी floodfill सक्रियकरण ("अधिक Sybil के साथ Sybil से लड़ना") - हार्डकोडेड "bad" सूचियों वाले नए सॉफ़्टवेयर संस्करण - स्वचालित पहचान के लिए बेहतर पीयर प्रोफ़ाइल मीट्रिक्स और सीमांत मान - एक ही IP ब्लॉक में अनेक floodfills को अयोग्य ठहराने वाला IP ब्लॉक योग्यता निर्धारण - स्वचालित सदस्यता-आधारित ब्लैकलिस्ट (Tor consensus के समान)

बड़े नेटवर्क इसे और कठिन बना देते हैं।

### 10.4 सिबिल आक्रमण (आंशिक Keyspace (कुंजी-क्षेत्र))

हमलावर 8–15 floodfill routers बना सकते हैं, जिन्हें keyspace (कुंजी स्थान) में आपस में बहुत पास-पास क्लस्टर किया गया हो। उस keyspace के लिए सभी lookups/stores हमलावर के routers की ओर निर्देशित हो जाते हैं, जिससे विशिष्ट I2P साइटों पर DOS (सेवा-वंचन हमला) संभव हो जाता है।

चूंकि keyspace क्रिप्टोग्राफ़िक SHA256 हैश का अनुक्रमण करता है, हमलावरों को पर्याप्त निकटता वाले routers उत्पन्न करने के लिए brute-force (संपूर्ण-परीक्षण) की आवश्यकता होती है।

**रक्षा**: Kademlia निकटता एल्गोरिद्म समय के साथ `SHA256(key + YYYYMMDD)` का उपयोग करके बदलता रहता है, जो हर दिन UTC मध्यरात्रि पर बदल जाता है. यह **keyspace rotation** (कुंजी-स्थान का परिवर्तन) हमले के दैनिक पुनर्जनन को बाध्य करता है.

> **Note**: हालिया शोध से पता चलता है कि keyspace (कुंजी स्थान) रोटेशन विशेष रूप से प्रभावी नहीं है—हमलावर router हैशों की पूर्व-गणना कर सकते हैं, और रोटेशन के बाद आधे घंटे के भीतर keyspace के कुछ हिस्सों को अलग-थलग करने के लिए केवल कुछ routers की आवश्यकता होती है।

दैनिक रोटेशन का परिणाम: रोटेशन के बाद कुछ मिनटों तक वितरित netdb अविश्वसनीय हो जाती है—नए सबसे निकट router को stores (store संदेश) प्राप्त होने से पहले lookups (खोज अनुरोध) विफल हो जाते हैं।

### 10.5 बूटस्ट्रैप हमले

हमलावर reseed websites (I2P में नेटवर्क से पहली बार जुड़ने के लिए आवश्यक seed जानकारी देने वाली वेबसाइटें) पर कब्जा कर सकते हैं या डेवलपरों को धोखा देकर दुर्भावनापूर्ण reseed websites जोड़वा सकते हैं, जिससे नए routers अलग-थलग/बहुसंख्यक-नियंत्रित नेटवर्कों में बूट हो जाएँ।

**लागू किए गए बचाव उपाय:** - एकल साइट के बजाय कई reseed (नेटवर्क में शामिल होने के लिए शुरुआती सीड/बूटस्ट्रैप सेवा) साइटों से RouterInfo (router की जानकारी का रिकॉर्ड) के उपसमुच्चय प्राप्त करना - नेटवर्क के बाहर reseed मॉनिटरिंग, जो साइटों को नियमित रूप से पोल करती है - संस्करण 0.9.14 से, reseed डेटा बंडल हस्ताक्षरित zip फ़ाइलों के रूप में होते हैं, जिनके लिए डाउनलोड किए गए हस्ताक्षर का सत्यापन किया जाता है (देखें [su3 विनिर्देश](/docs/specs/updates))

### 10.6 क्वेरी कैप्चर

Floodfill routers लौटाए गए संदर्भों के माध्यम से समकक्षों को हमलावर-नियंत्रित routers की ओर "मार्गित" कर सकते हैं।

कम आवृत्ति के कारण अन्वेषण के जरिए होने की संभावना कम है; routers मुख्यतः सामान्य tunnel निर्माण के माध्यम से पीयर संदर्भ प्राप्त करते हैं।

संस्करण 0.8.9 से, पुनरावृत्त खोजें लागू की गई हैं। `DatabaseSearchReplyMessage` के floodfill रेफ़रेंस, यदि वे खोज कुंजी के अधिक निकट हों, तो उनका अनुसरण किया जाता है। अनुरोध करने वाले routers रेफ़रेंस की निकटता पर भरोसा नहीं करते। अधिक निकट कुंजियाँ न होने पर भी, टाइमआउट/अधिकतम क्वेरी तक खोज जारी रहती है, जिससे दुर्भावनापूर्ण black-holing (अनुरोधों को जानबूझकर गायब करना) को रोका जाता है।

### 10.7 सूचना का रिसाव

I2P में DHT (वितरित हैश तालिका) की सूचना-लीक पर और जांच की आवश्यकता है। Floodfill routers क्वेरियों का अवलोकन करके जानकारी एकत्र करते हैं। जब दुर्भावनापूर्ण नोड्स 20% तक हों, तो पहले वर्णित Sybil (बहु-पहचान) खतरे कई कारणों से समस्याग्रस्त हो जाते हैं।

---

## 11. भविष्य का कार्य

- अतिरिक्त netDb लुकअप और प्रतिक्रियाओं के लिए एंड-टू-एंड एन्क्रिप्शन
- बेहतर लुकअप प्रतिक्रिया ट्रैकिंग विधियाँ
- keyspace rotation (कुंजी-स्थान घुमाव) से जुड़ी विश्वसनीयता संबंधी समस्याओं के लिए शमन विधियाँ

---

## 12. संदर्भ

- [सामान्य संरचनाओं का विनिर्देश](/docs/specs/common-structures/) – RouterInfo और LeaseSet संरचनाएँ
- [I2NP विनिर्देश](/docs/specs/i2np/) – डेटाबेस संदेश प्रकार
- [प्रस्ताव 123: नई netDb प्रविष्टियाँ](/proposals/123-new-netdb-entries) – LeaseSet2 विनिर्देश
- [ऐतिहासिक netDb चर्चा](/docs/netdb/) – विकास इतिहास और संग्रहीत चर्चाएँ
