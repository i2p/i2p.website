---
title: "I2P क्लाइंट प्रोटोकॉल (I2CP)"
description: "एप्लिकेशन I2P router के साथ सेशन्स, tunnels, और LeaseSets का नेगोशिएशन कैसे करते हैं।"
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

I2CP I2P router और किसी भी क्लाइंट प्रक्रिया के बीच निम्न-स्तरीय नियंत्रण प्रोटोकॉल है। यह जिम्मेदारियों का सख्त पृथक्करण परिभाषित करता है:

- **Router**: रूटिंग, क्रिप्टोग्राफी, tunnels के जीवनचक्र, और नेटवर्क डेटाबेस संचालन का प्रबंधन करता है
- **क्लाइंट**: अनामिकता गुणों का चयन करता है, tunnels को कॉन्फ़िगर करता है, और संदेश भेजता/प्राप्त करता है

संपूर्ण संचार एकल TCP socket (नेटवर्क कनेक्शन का एंडपॉइंट) के माध्यम से होता है (वैकल्पिक रूप से TLS-wrapped (TLS द्वारा संरक्षित)), जो असमकालिक, full-duplex (दो-तरफ़ा समानांतर संचार) संचालन को सक्षम बनाता है।

**प्रोटोकॉल संस्करण**: I2CP प्रारंभिक कनेक्शन स्थापना के दौरान भेजे जाने वाले प्रोटोकॉल संस्करण बाइट `0x2A` (दशमलव में 42) का उपयोग करता है। यह संस्करण बाइट प्रोटोकॉल की शुरुआत से स्थिर बना हुआ है।

**वर्तमान स्थिति**: यह विनिर्देशन router संस्करण 0.9.67 (API संस्करण 0.9.67) के लिए सटीक है, जो 2025-09 में जारी हुआ।

## कार्यान्वयन संदर्भ

### जावा कार्यान्वयन

संदर्भ कार्यान्वयन Java I2P में है:
- क्लाइंट SDK: `i2p.jar` पैकेज
- router कार्यान्वयन: `router.jar` पैकेज
- [Javadocs](http://docs.i2p-projekt.de/javadoc/)

जब क्लाइंट और router एक ही JVM में चलते हैं, तो I2CP संदेशों को serialization (डेटा को बाइट अनुक्रम में बदलना) के बिना Java ऑब्जेक्ट्स के रूप में पास किया जाता है। बाहरी क्लाइंट TCP पर serialized प्रोटोकॉल का उपयोग करते हैं।

### C++ कार्यान्वयन

i2pd (C++ I2P router) क्लाइंट कनेक्शनों के लिए I2CP को बाहरी रूप से भी इम्प्लीमेंट करता है।

### गैर‑Java क्लाइंट्स

एक पूर्ण I2CP क्लाइंट लाइब्रेरी के **कोई ज्ञात गैर-जावा कार्यान्वयन** नहीं हैं। गैर-जावा अनुप्रयोगों को इसके बजाय उच्च-स्तरीय प्रोटोकॉल का उपयोग करना चाहिए:

- **SAM (Simple Anonymous Messaging) v3**: सॉकेट-आधारित इंटरफेस, कई भाषाओं में उपलब्ध लाइब्रेरीज़ के साथ
- **BOB (Basic Open Bridge)**: SAM का सरल विकल्प

ये उच्च-स्तरीय प्रोटोकॉल I2CP की जटिलता को आंतरिक रूप से संभालते हैं और साथ ही स्ट्रीमिंग लाइब्रेरी (TCP जैसी कनेक्शनों के लिए) और डेटाग्राम लाइब्रेरी (UDP जैसी कनेक्शनों के लिए) भी प्रदान करते हैं।

## कनेक्शन स्थापना

### 1. TCP कनेक्शन

router के I2CP पोर्ट से कनेक्ट करें: - डिफ़ॉल्ट: `127.0.0.1:7654` - router सेटिंग्स के माध्यम से कॉन्फ़िगर किया जा सकता है - वैकल्पिक TLS wrapper (रैपर) (दूरस्थ कनेक्शनों के लिए दृढ़तापूर्वक अनुशंसित)

### 2. प्रोटोकॉल हैंडशेक

**चरण 1**: प्रोटोकॉल संस्करण बाइट `0x2A` भेजें

**चरण 2**: घड़ी समकालन

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
router अपना वर्तमान समय-चिह्न और I2CP API संस्करण स्ट्रिंग लौटाता है (0.8.7 से)।

**चरण 3**: प्रमाणीकरण (यदि सक्षम हो)

0.9.11 से, प्रमाणीकरण को GetDateMessage (तारीख प्राप्त करने वाला संदेश) में ऐसी Mapping (मैपिंग) के माध्यम से शामिल किया जा सकता है, जिसमें निम्नलिखित हों: - `i2cp.username` - `i2cp.password`

संस्करण 0.9.16 से, जब प्रमाणीकरण सक्षम होता है, तो अन्य कोई संदेश भेजे जाने से पहले प्रमाणीकरण को GetDateMessage के माध्यम से **अवश्य** पूरा किया जाना है।

**चरण 4**: सत्र निर्माण

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**चरण 5**: Tunnel तैयार होने का संकेत

```
Router → Client: RequestVariableLeaseSetMessage
```
यह संदेश संकेत देता है कि inbound tunnels बन चुके हैं। router इसे तब तक नहीं भेजेगा जब तक कम से कम एक inbound और एक outbound tunnel मौजूद न हों।

**चरण 6**: LeaseSet का प्रकाशन

```
Client → Router: CreateLeaseSet2Message
```
इस चरण में, सत्र संदेश भेजने और प्राप्त करने के लिए पूर्ण रूप से क्रियाशील है।

## संदेश प्रवाह पैटर्न

### प्रेषित संदेश (क्लाइंट दूरस्थ गंतव्य को भेजता है)

**i2cp.messageReliability=none के साथ**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**i2cp.messageReliability=BestEffort के साथ**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### आने वाला संदेश (Router क्लाइंट तक पहुँचाता है)

**i2cp.fastReceive=true होने पर** (0.9.4 से डिफ़ॉल्ट):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**i2cp.fastReceive=false के साथ** (अप्रचलित):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
आधुनिक क्लाइंट्स को हमेशा fast receive mode (तेज़ प्राप्ति मोड) का उपयोग करना चाहिए।

## सामान्य डेटा संरचनाएँ

### I2CP संदेश शीर्षलेख

सभी I2CP संदेश इस सामान्य हेडर का उपयोग करते हैं:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **बॉडी लंबाई**: 4-बाइट पूर्णांक, केवल संदेश बॉडी की लंबाई (हेडर को छोड़कर)
- **प्रकार**: 1-बाइट पूर्णांक, संदेश प्रकार पहचानकर्ता
- **संदेश बॉडी**: 0+ बाइट्स, प्रारूप संदेश प्रकार के अनुसार बदलता है

**संदेश आकार की सीमा**: अधिकतम लगभग 64 KB.

### सेशन आईडी

2-बाइट का पूर्णांक, जो router पर किसी सत्र की अद्वितीय पहचान करता है।

**विशेष मान**: `0xFFFF` "कोई सत्र नहीं" का संकेत करता है (स्थापित सत्र के बिना hostname लुकअप्स के लिए उपयोग किया जाता है)।

### संदेश आईडी

किसी सत्र के भीतर किसी संदेश की अद्वितीय पहचान के लिए router द्वारा उत्पन्न 4-बाइट पूर्णांक।

**महत्वपूर्ण**: संदेश आईडी वैश्विक रूप से अद्वितीय **नहीं** हैं; वे केवल एक सत्र के भीतर अद्वितीय हैं। वे क्लाइंट द्वारा उत्पन्न nonce (एक बार प्रयुक्त यादृच्छिक संख्या) से भी भिन्न हैं।

### पेलोड प्रारूप

संदेश पेलोड मानक 10-बाइट gzip हेडर के साथ gzip से संपीड़ित होते हैं: - शुरुआत होती है: `0x1F 0x8B 0x08` (RFC 1952) - 0.7.1 से: gzip हेडर के अप्रयुक्त हिस्सों में प्रोटोकॉल, from-port, और to-port की जानकारी शामिल होती है - यह एक ही गंतव्य पर स्ट्रीमिंग और डेटाग्राम को सक्षम करता है

**संपीड़न नियंत्रण**: संपीड़न को अक्षम करने के लिए `i2cp.gzip=false` सेट करें (gzip effort (प्रयास) को 0 पर सेट करता है)। gzip हेडर अभी भी शामिल रहता है, लेकिन संपीड़न ओवरहेड न्यूनतम रहता है।

### SessionConfig संरचना

क्लाइंट सत्र के लिए विन्यास परिभाषित करता है:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**महत्वपूर्ण आवश्यकताएँ**: 1. **मैपिंग को कुंजी के आधार पर क्रमबद्ध होना चाहिए** हस्ताक्षर सत्यापन के लिए 2. **निर्माण तिथि** router के वर्तमान समय से ±30 सेकंड के भीतर होनी चाहिए 3. **हस्ताक्षर** Destination (I2P में गंतव्य पहचान/एंडपॉइंट) के SigningPrivateKey (हस्ताक्षर करने वाली निजी कुंजी) द्वारा बनाया जाता है

**ऑफ़लाइन हस्ताक्षर** (संस्करण 0.9.38 के अनुसार):

यदि आप ऑफ़लाइन साइनिंग का उपयोग कर रहे हैं, तो मैपिंग में शामिल होना चाहिए: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

फिर हस्ताक्षर अस्थायी SigningPrivateKey द्वारा उत्पन्न किया जाता है.

## मुख्य कॉन्फ़िगरेशन विकल्प

### Tunnel विन्यास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**टिप्पणियाँ**: - `quantity` के लिए मान > 6 को 0.9.0+ चलाने वाले पीयर्स की आवश्यकता होती है और यह संसाधन उपयोग को उल्लेखनीय रूप से बढ़ा देता है - उच्च-उपलब्धता सेवाओं के लिए `backupQuantity` को 1-2 पर सेट करें - Zero-hop tunnels (शून्य-हॉप tunnels) में विलंबता कम करने के लिए गुमनामी का त्याग किया जाता है, लेकिन ये परीक्षण के लिए उपयोगी हैं

### संदेश प्रबंधन

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**संदेश विश्वसनीयता**: - `None`: router से कोई स्वीकृति नहीं (0.8.1 से स्ट्रीमिंग लाइब्रेरी का डिफ़ॉल्ट) - `BestEffort`: router स्वीकृति + सफलता/विफलता सूचनाएँ भेजता है - `Guaranteed`: लागू नहीं (वर्तमान में BestEffort की तरह व्यवहार करता है)

**प्रति-संदेश ओवरराइड** (0.9.14 से): - `messageReliability=none` वाले सत्र में, शून्य से भिन्न nonce (एक-बार-प्रयोग होने वाली अद्वितीय संख्या) सेट करने पर उस विशिष्ट संदेश के लिए डिलीवरी सूचना का अनुरोध होता है - `BestEffort` सत्र में nonce=0 सेट करने से उस संदेश के लिए सूचनाएँ निष्क्रिय हो जाती हैं

### LeaseSet विन्यास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### लेगेसी ElGamal/AES सेशन टैग्स

ये विकल्प केवल पुराने ElGamal एन्क्रिप्शन के लिए प्रासंगिक हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**नोट**: ECIES-X25519 क्लाइंट एक अलग ratchet mechanism (क्रमिक कुंजी-परिवर्तन तंत्र) का उपयोग करते हैं और इन विकल्पों को नज़रअंदाज़ करते हैं।

## एन्क्रिप्शन के प्रकार

I2CP `i2cp.leaseSetEncType` विकल्प के माध्यम से कई एंड-टू-एंड एन्क्रिप्शन पद्धतियों का समर्थन करता है। आधुनिक और पुराने समकक्षों दोनों का समर्थन करने के लिए कई प्रकार (कॉमा से अलग करके) निर्दिष्ट किए जा सकते हैं।

### समर्थित एन्क्रिप्शन प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**अनुशंसित विन्यास**:

```
i2cp.leaseSetEncType=4,0
```
यह X25519 (वांछित; एक आधुनिक elliptic-curve key agreement एल्गोरिद्म) को अनुकूलता के लिए ElGamal (एक सार्वजनिक-कुंजी क्रिप्टोसिस्टम) फॉलबैक के साथ प्रदान करता है।

### एन्क्रिप्शन प्रकार के विवरण

**प्रकार 0 - ElGamal/AES+SessionTags**: - 2048-बिट ElGamal सार्वजनिक कुंजियाँ (256 बाइट) - AES-256 सममित एन्क्रिप्शन - 32-बाइट session tags (अस्थायी सत्र-टोकन) बैचों में भेजे जाते हैं - उच्च CPU, बैंडविड्थ और मेमोरी ओवरहेड - पूरे नेटवर्क में चरणबद्ध रूप से हटाया जा रहा है

**प्रकार 4 - ECIES-X25519-AEAD-Ratchet**: - X25519 कुंजी विनिमय (32-बाइट कुंजियाँ) - ChaCha20/Poly1305 AEAD (Authenticated Encryption with Associated Data, संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) - Signal-style double ratchet (डबल रैचेट, Signal जैसा कुंजी-अपडेट तंत्र) - 8-बाइट सेशन टैग (ElGamal के लिए 32-बाइट के मुकाबले) - टैग synchronized PRNG (pseudorandom number generator, छद्म-यादृच्छिक संख्या जनक) के माध्यम से उत्पन्न किए जाते हैं (पहले से नहीं भेजे जाते) - ~92% ओवरहेड में कमी (ElGamal की तुलना में) - आधुनिक I2P के लिए मानक (अधिकांश routers इसका उपयोग करते हैं)

**प्रकार 5-6 - पोस्ट-क्वांटम हाइब्रिड**: - X25519 को ML-KEM (कुंजी एन्कैप्सुलेशन तंत्र) (NIST FIPS 203) के साथ संयोजित करता है - क्वांटम-प्रतिरोधी सुरक्षा प्रदान करता है - संतुलित सुरक्षा/प्रदर्शन के लिए ML-KEM-768 - अधिकतम सुरक्षा के लिए ML-KEM-1024 - PQ (पोस्ट-क्वांटम) कुंजी सामग्री के कारण संदेश आकार बड़े होते हैं - नेटवर्क समर्थन का परिनियोजन अभी भी जारी है

### स्थानांतरण रणनीति

I2P नेटवर्क सक्रिय रूप से ElGamal (प्रकार 0) से X25519 (प्रकार 4) में माइग्रेट हो रहा है: - NTCP → NTCP2 (पूर्ण) - SSU → SSU2 (पूर्ण) - ElGamal tunnels → X25519 tunnels (पूर्ण) - ElGamal end-to-end (छोर-से-छोर) → ECIES-X25519 (अधिकांशतः पूर्ण)

## LeaseSet2 और उन्नत विशेषताएँ

### LeaseSet2 विकल्प (0.9.38 से)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Blinded Addresses (क्रिप्टोग्राफिक ब्लाइंडिंग के जरिए छुपाए गए पते)

संस्करण 0.9.39 से, गंतव्य "blinded" पते (b33 format) का उपयोग कर सकते हैं जो समय-समय पर बदलते हैं: - पासवर्ड सुरक्षा के लिए `i2cp.leaseSetSecret` आवश्यक है - प्रति-क्लाइंट वैकल्पिक प्रमाणीकरण - विवरण के लिए प्रस्ताव 123 और 149 देखें

### सेवा रिकॉर्ड (0.9.66 से)

LeaseSet2 सेवा रिकॉर्ड विकल्पों का समर्थन करता है (प्रस्ताव 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
प्रारूप DNS SRV रिकॉर्ड शैली का अनुसरण करता है, लेकिन I2P के लिए अनुकूलित है।

## एकाधिक सत्र (0.9.21 से)

एकल I2CP कनेक्शन कई सत्रों को बनाए रख सकता है:

**प्राथमिक सत्र**: किसी कनेक्शन पर बनाया गया पहला सत्र **उप-सत्र**: वे अतिरिक्त सत्र जो प्राथमिक सत्र के tunnel पूल को साझा करते हैं

### उपसत्र की विशेषताएँ

1. **साझा Tunnels**: प्राथमिक वाले ही इनबाउंड/आउटबाउंड tunnel pools का उपयोग करें
2. **साझा एन्क्रिप्शन कुंजियाँ**: एकसमान LeaseSet एन्क्रिप्शन कुंजियों का उपयोग करना अनिवार्य है
3. **भिन्न हस्ताक्षर कुंजियाँ**: अलग-अलग Destination (गंतव्य) हस्ताक्षर कुंजियों का उपयोग करना अनिवार्य है
4. **गुमनामी की कोई गारंटी नहीं**: प्राथमिक सत्र से स्पष्ट रूप से जुड़ा हुआ (उसी router, वही tunnels)

### Subsession (उप-सत्र) उपयोग-प्रकरण

विभिन्न हस्ताक्षर प्रकारों का उपयोग करने वाले गंतव्यों के साथ संचार सक्षम करें: - प्राथमिक: EdDSA हस्ताक्षर (आधुनिक) - उप-सत्र: DSA हस्ताक्षर (पुराने संस्करणों के साथ अनुकूलता)

### Subsession (उप-सत्र) का जीवनचक्र

**निर्माण**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**समापन**: - उप-सत्र को समाप्त करना: प्राथमिक सत्र अक्षुण्ण रहता है - प्राथमिक सत्र को समाप्त करना: सभी उप-सत्रों को समाप्त कर देता है और कनेक्शन बंद करता है - DisconnectMessage (डिस्कनेक्ट संदेश): सभी सत्रों को समाप्त कर देता है

### सत्र ID प्रबंधन

अधिकांश I2CP संदेशों में एक Session ID फ़ील्ड शामिल होती है. अपवाद: - DestLookup / DestReply (अप्रचलित, HostLookup / HostReply का उपयोग करें) - GetBandwidthLimits / BandwidthLimits (प्रतिक्रिया सत्र-विशिष्ट नहीं है)

**महत्वपूर्ण**: क्लाइंट्स को एक साथ कई CreateSession संदेश लंबित नहीं रखने चाहिए, क्योंकि प्रतिक्रियाओं को अनुरोधों से निश्चित रूप से संबद्ध नहीं किया जा सकता।

## संदेश कैटलॉग

### संदेश प्रकारों का सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**कुंजी**: C = क्लाइंट, R = Router

### मुख्य संदेश के विवरण

#### CreateSessionMessage (प्रकार 1)

**उद्देश्य**: एक नया I2CP सत्र प्रारंभ करें

**सामग्री**: SessionConfig (सत्र विन्यास) संरचना

**प्रतिक्रिया**: SessionStatusMessage (status=Created या Invalid)

**आवश्यकताएँ**: - SessionConfig में दिनांक router समय से ±30 सेकंड के भीतर होना चाहिए - हस्ताक्षर सत्यापन के लिए मैपिंग को कुंजी के आधार पर क्रमबद्ध होना चाहिए - Destination (गंतव्य) के पास पहले से कोई सक्रिय सत्र नहीं होना चाहिए

#### RequestVariableLeaseSetMessage (प्रकार 37)

**उद्देश्य**: Router inbound tunnels के लिए क्लाइंट से प्राधिकरण का अनुरोध करता है

**सामग्री**: - सत्र आईडी - Lease (लीज़) की संख्या - Lease संरचनाओं की array (प्रत्येक का अपना अलग समाप्ति समय)

**प्रतिक्रिया**: CreateLeaseSet2Message

**महत्त्व**: यह संकेत दर्शाता है कि सत्र कार्यरत है। router इसे केवल तब भेजता है जब: 1. कम-से-कम एक इनबाउंड tunnel निर्मित हो 2. कम-से-कम एक आउटबाउंड tunnel निर्मित हो

**समय-सीमा अनुशंसा**: यदि सत्र बनाए जाने के 5+ मिनट के भीतर यह संदेश प्राप्त नहीं होता है, तो क्लाइंट्स को सत्र को समाप्त कर देना चाहिए।

#### CreateLeaseSet2Message (प्रकार 41)

**उद्देश्य**: क्लाइंट LeaseSet को नेटवर्क डेटाबेस में प्रकाशित करता है

**सामग्री**: - सत्र ID - LeaseSet प्रकार बाइट (1, 3, 5, या 7) - LeaseSet या LeaseSet2 या EncryptedLeaseSet या MetaLeaseSet - निजी कुंजियों की संख्या - निजी कुंजी सूची (LeaseSet में प्रत्येक सार्वजनिक कुंजी के लिए एक, उसी क्रम में)

**निजी कुंजियाँ**: आने वाले garlic संदेश (I2P का बंडल संदेश) को डिक्रिप्ट करने के लिए आवश्यक। प्रारूप:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**नोट**: अप्रचलित CreateLeaseSetMessage (type 4) को प्रतिस्थापित करता है, जो निम्नलिखित को संभाल नहीं सकता: - LeaseSet2 वैरिएंट - गैर-ElGamal एन्क्रिप्शन - एकाधिक एन्क्रिप्शन प्रकार - एन्क्रिप्टेड LeaseSets - ऑफ़लाइन साइनिंग कुंजियाँ

#### SendMessageExpiresMessage (प्रकार 36)

**उद्देश्य**: समाप्ति समय और उन्नत विकल्पों सहित गंतव्य पर संदेश भेजें

**सामग्री**: - सत्र ID - गंतव्य - पेलोड (gzipped) - नॉन्स (4 बाइट) - फ्लैग्स (2 बाइट) - नीचे देखें - समाप्ति तिथि (6 बाइट, 8 से ट्रंकेट किया गया)

**फ़्लैग्स फ़ील्ड** (2 बाइट, बिट क्रम 15...0):

**बिट्स 15-11**: अप्रयुक्त, 0 होना अनिवार्य है

**Bits 10-9**: संदेश की विश्वसनीयता ओवरराइड (अप्रयुक्त, इसके बजाय nonce (एक-बार उपयोग की जाने वाली अद्वितीय संख्या) का उपयोग करें)

**बिट 8**: LeaseSet को बंडल न करें - 0: Router LeaseSet को garlic में बंडल कर सकता है - 1: LeaseSet को बंडल न करें

**बिट 7-4**: टैग की निम्न सीमा (केवल ElGamal पर लागू, ECIES में अनदेखा)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**बिट्स 3-0**: आवश्यकता होने पर भेजे जाने वाले टैग (केवल ElGamal के लिए, ECIES में अनदेखा किया जाता है)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (संदेश स्थिति संदेश) (प्रकार 22)

**उद्देश्य**: संदेश की डिलीवरी स्थिति के बारे में क्लाइंट को सूचित करना

**सामग्री**: - सेशन ID - मैसेज ID (router द्वारा जनित) - स्टेटस कोड (1 बाइट) - आकार (4 बाइट, सिर्फ status=0 के लिए प्रासंगिक) - नॉन्स (4 बाइट, क्लाइंट के SendMessage nonce से मेल खाता है)

**स्थिति कोड** (प्रेषित संदेश):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**सफलता कोड**: 1, 2, 4, 6 **विफलता कोड**: अन्य सभी

**स्टेटस कोड 0** (अप्रचलित): उपलब्ध संदेश (आने वाला, तेज़ प्राप्ति निष्क्रिय)

#### HostLookupMessage (प्रकार 38)

**उद्देश्य**: होस्टनेम या हैश द्वारा डेस्टिनेशन लुकअप (DestLookup का स्थान लेता है)

**सामग्री**: - सत्र ID (या सत्र न होने पर 0xFFFF) - अनुरोध ID (4 बाइट) - मिलीसेकंड में टाइमआउट (4 बाइट, अनुशंसित न्यूनतम: 10000) - अनुरोध प्रकार (1 बाइट) - लुकअप कुंजी (Hash, hostname String, या Destination)

**अनुरोध प्रकार**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
प्रकार 2-4 उपलब्ध होने पर LeaseSet विकल्प (प्रस्ताव 167) लौटाते हैं।

**प्रतिक्रिया**: HostReplyMessage

#### HostReplyMessage (प्रकार 39)

**उद्देश्य**: HostLookupMessage (होस्ट लुकअप संदेश) के प्रति प्रतिक्रिया

**सामग्री**: - सत्र ID - अनुरोध ID - परिणाम कोड (1 बाइट) - Destination (I2P पता/पहचान) (सफल होने पर मौजूद, कभी-कभी कुछ विशिष्ट विफलताओं में भी) - मैपिंग (केवल लुकअप प्रकार 2-4 के लिए, खाली हो सकता है)

**परिणाम कोड**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (प्रकार 42)

**उद्देश्य**: router को blinded destination (गोपनीयता हेतु छिपाई गई गंतव्य पहचान) के प्रमाणीकरण आवश्यकताओं के बारे में सूचित करना (since 0.9.43)

**सामग्री**: - सेशन ID - फ्लैग्स (1 बाइट) - एंडपॉइंट प्रकार (1 बाइट): 0=Hash, 1=hostname, 2=Destination, 3=SigType+Key - ब्लाइंडेड हस्ताक्षर प्रकार (2 बाइट) - समाप्ति (4 बाइट, एपोक से सेकंड) - एंडपॉइंट डेटा (प्रकार के अनुसार बदलता है) - प्राइवेट कुंजी (32 बाइट, केवल यदि फ्लैग बिट 0 सेट हो) - लुकअप पासवर्ड (String, केवल यदि फ्लैग बिट 4 सेट हो)

**फ्लैग्स** (बिट क्रम 76543210):

- **बिट 0**: 0=सभी, 1=प्रति-क्लाइंट
- **बिट्स 3-1**: प्रमाणीकरण योजना (यदि बिट 0=1): 000=DH (Diffie-Hellman), 001=PSK (Pre-Shared Key)
- **बिट 4**: 1=सीक्रेट आवश्यक
- **बिट्स 7-5**: अप्रयुक्त, 0 पर सेट करें

**कोई प्रतिक्रिया नहीं**: Router चुपचाप संसाधित करता है

**उपयोग मामला**: blinded destination (b33 address) पर भेजने से पहले, क्लाइंट को निम्न में से एक करना होगा: 1. HostLookup के माध्यम से b33 का लुकअप करें, या 2. BlindingInfo message भेजें

यदि गंतव्य को प्रमाणीकरण की आवश्यकता है, तो BlindingInfo अनिवार्य है.

#### ReconfigureSessionMessage (प्रकार 2)

**उद्देश्य**: निर्माण के बाद सत्र विन्यास को अद्यतन करना

**सामग्री**: - सेशन आईडी - SessionConfig (सेशन कॉन्फ़िगरेशन) (केवल बदले गए विकल्प आवश्यक)

**प्रतिक्रिया**: SessionStatusMessage (सेशन स्थिति संदेश) (status=Updated या Invalid)

**नोट्स**: - Router नई कॉन्फ़िगरेशन को मौजूदा कॉन्फ़िगरेशन के साथ मर्ज करता है - Tunnel विकल्प (`inbound.*`, `outbound.*`) हमेशा लागू किए जाते हैं - सत्र निर्माण के बाद कुछ विकल्प अपरिवर्तनीय हो सकते हैं - दिनांक router समय से ±30 सेकंड के भीतर होना चाहिए - मैपिंग को कुंजी के अनुसार क्रमबद्ध होना चाहिए

#### DestroySessionMessage (सत्र समाप्ति संदेश) (प्रकार 3)

**उद्देश्य**: सत्र समाप्त करना

**सामग्री**: सत्र आईडी

**अपेक्षित प्रतिक्रिया**: SessionStatusMessage (status=Destroyed)

**वास्तविक व्यवहार** (Java I2P 0.9.66 तक): - Router कभी SessionStatus(Destroyed) नहीं भेजता - यदि कोई सत्र शेष नहीं है: DisconnectMessage भेजता है - यदि subsessions (उप-सत्र) शेष हैं: कोई उत्तर नहीं

**महत्वपूर्ण**: Java I2P का व्यवहार विनिर्देश से भिन्न है। व्यक्तिगत उपसत्रों को समाप्त करते समय कार्यान्वयनों को सावधानी बरतनी चाहिए।

#### DisconnectMessage (प्रकार 30)

**उद्देश्य**: यह सूचित करना कि कनेक्शन जल्द ही समाप्त होने वाला है

**सामग्री**: कारण स्ट्रिंग

**प्रभाव**: कनेक्शन पर मौजूद सभी सत्र नष्ट कर दिए जाते हैं, सॉकेट बंद हो जाता है

**कार्यान्वयन**: मुख्य रूप से Java I2P में router → क्लाइंट

## प्रोटोकॉल संस्करण इतिहास

### संस्करण पहचान

I2CP प्रोटोकॉल का संस्करण Get/SetDate संदेशों में आदान-प्रदान किया जाता है (0.8.7 से)। पुराने routers के लिए संस्करण संबंधी जानकारी उपलब्ध नहीं है।

**संस्करण स्ट्रिंग**: "core" API के संस्करण को दर्शाता है, यह जरूरी नहीं कि router संस्करण हो।

### विशेषताओं की समयरेखा

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## सुरक्षा संबंधी विचार

### प्रमाणीकरण

**डिफ़ॉल्ट**: कोई प्रमाणीकरण आवश्यक नहीं **वैकल्पिक**: उपयोगकर्ता नाम/पासवर्ड प्रमाणीकरण (0.9.11 से) **अनिवार्य**: सक्रिय होने पर, अन्य संदेशों से पहले प्रमाणीकरण पूरा होना आवश्यक है (0.9.16 से)

**दूरस्थ कनेक्शन**: प्रमाण-पत्रों और निजी कुंजियों की सुरक्षा के लिए हमेशा TLS (ट्रांसपोर्ट लेयर सिक्योरिटी) (`i2cp.SSL=true`) का उपयोग करें।

### घड़ी का विचलन

SessionConfig Date (सेशन कॉन्फ़िगरेशन की तिथि) router समय से ±30 सेकंड के भीतर होनी चाहिए, अन्यथा सेशन अस्वीकार कर दिया जाएगा. समय समकालित करने के लिए Get/SetDate का उपयोग करें.

### निजी कुंजी का प्रबंधन

CreateLeaseSet2Message में आने वाले संदेशों को डिक्रिप्ट करने के लिए निजी कुंजियाँ होती हैं। इन कुंजियों के लिए यह आवश्यक है: - सुरक्षित रूप से प्रेषित की जाएँ (दूरस्थ कनेक्शनों के लिए TLS) - router द्वारा सुरक्षित रूप से संग्रहीत की जाएँ - समझौता होने पर बदली जाएँ

### संदेश की समाप्ति

स्पष्ट समाप्ति समय निर्धारित करने के लिए हमेशा SendMessageExpires (SendMessage नहीं) का उपयोग करें। यह: - संदेशों को अनिश्चितकाल तक कतार में पड़े रहने से रोकता है - संसाधन खपत को कम करता है - विश्वसनीयता में सुधार करता है

### सत्र टैग प्रबंधन

**ElGamal** (अप्रचलित): - टैगों को बैचों में भेजे जाने चाहिए - खोए हुए टैग डिक्रिप्शन विफलताओं का कारण बनते हैं - उच्च मेमोरी ओवरहेड (अतिरिक्त मेमोरी-खर्च)

**ECIES-X25519** (वर्तमान): - समकालिक PRNG (छद्म-यादृच्छिक संख्या जनक) के माध्यम से उत्पन्न टैग - पूर्व-प्रेषण की आवश्यकता नहीं - संदेश हानि के प्रति सहनशील - काफी कम ओवरहेड

## सर्वोत्तम प्रथाएँ

### क्लाइंट डेवलपर्स के लिए

1. **फास्ट रिसीव मोड का उपयोग करें**: हमेशा `i2cp.fastReceive=true` सेट करें (या डिफ़ॉल्ट पर भरोसा करें)

2. **ECIES-X25519 (एलिप्टिक-curve आधारित एन्क्रिप्शन स्कीम) को प्राथमिकता दें**: सर्वोत्तम प्रदर्शन और संगतता के लिए `i2cp.leaseSetEncType=4,0` कॉन्फ़िगर करें

3. **स्पष्ट समाप्ति समय निर्धारित करें**: SendMessageExpires का उपयोग करें, SendMessage नहीं

4. **Subsessions (उप-सेशन) को सावधानीपूर्वक संभालें**: ध्यान रखें कि subsessions destinations (गंतव्य) के बीच कोई अनामिकता प्रदान नहीं करते

5. **सत्र निर्माण टाइमआउट**: यदि 5 मिनट के भीतर RequestVariableLeaseSet (एक विशिष्ट संदेश/ऑब्जेक्ट का नाम) प्राप्त न हो, तो सत्र समाप्त करें

6. **कॉन्फ़िगरेशन मैपिंग को क्रमबद्ध करें**: SessionConfig पर हस्ताक्षर करने से पहले हमेशा मैपिंग कुंजियों को क्रमबद्ध करें

7. **उचित Tunnel संख्या का उपयोग करें**: आवश्यक न होने पर `quantity` > 6 सेट न करें

8. **नॉन-जावा के लिए SAM/BOB पर विचार करें**: I2CP को सीधे लागू करने के बजाय SAM लागू करें

### Router डेवलपर्स के लिए

1. **तिथियों का सत्यापन**: SessionConfig की तिथियों पर ±30 सेकंड की समय-विंडो लागू करें

2. **संदेश का आकार सीमित करें**: ~64 KB का अधिकतम संदेश आकार लागू करें

3. **एकाधिक सत्रों का समर्थन**: 0.9.21 विनिर्देश के अनुसार subsession (उप-सत्र) समर्थन लागू करें

4. **RequestVariableLeaseSet (I2NP संदेश) तुरंत भेजें**: केवल तब जब दोनों इनबाउंड और आउटबाउंड tunnels बन चुके हों

5. **Deprecated (अप्रचलित) संदेशों को संभालें**: स्वीकार करें, लेकिन ReceiveMessageBegin/End के उपयोग को हतोत्साहित करें

6. **ECIES-X25519 (X25519-आधारित Elliptic Curve Integrated Encryption Scheme, आधुनिक सार्वजनिक-कुंजी एन्क्रिप्शन)**: नई तैनातियों के लिए टाइप 4 एन्क्रिप्शन को प्राथमिकता दें

## डीबगिंग और समस्या निवारण

### सामान्य समस्याएँ

**सत्र अस्वीकृत (अमान्य)**: - क्लॉक स्क्यू (±30 सेकंड के भीतर होना चाहिए) की जाँच करें - सत्यापित करें कि Mapping कुंजी के अनुसार क्रमबद्ध है - सुनिश्चित करें कि Destination पहले से उपयोग में न हो

**RequestVariableLeaseSet नहीं**: - Router संभवतः tunnels बना रहा है (अधिकतम 5 मिनट तक प्रतीक्षा करें) - नेटवर्क कनेक्टिविटी समस्याओं की जाँच करें - सुनिश्चित करें कि पर्याप्त पीयर कनेक्शन हैं

**संदेश वितरण विफलताएँ**: - विफलता के विशिष्ट कारण के लिए MessageStatus कोड जांचें - सत्यापित करें कि दूरस्थ LeaseSet प्रकाशित और वर्तमान है - सुनिश्चित करें कि एन्क्रिप्शन प्रकार संगत हों

**उपसत्र से संबंधित समस्याएँ**: - सत्यापित करें कि प्राथमिक सत्र पहले बनाया गया है - पुष्टि करें कि एन्क्रिप्शन कुंजियाँ समान हैं - जाँचें कि हस्ताक्षर कुंजियाँ भिन्न हैं

### निदान संदेश

**GetBandwidthLimits**: router की क्षमता की जानकारी प्राप्त करें **HostLookup**: नाम समाधान और LeaseSet (I2P में किसी गंतव्य के tunnels की लीज़ प्रविष्टियों का सेट) उपलब्धता का परीक्षण करें **MessageStatus**: संदेश वितरण को एंड-टू-एंड ट्रैक करें

## संबंधित विनिर्देश

- **सामान्य संरचनाएँ**: /docs/specs/common-structures/
- **I2NP (नेटवर्क प्रोटोकॉल)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Tunnel निर्माण**: /docs/specs/implementation/
- **स्ट्रीमिंग लाइब्रेरी**: /docs/specs/streaming/
- **डेटाग्राम लाइब्रेरी**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## संदर्भित प्रस्ताव

- [प्रस्ताव 123](/proposals/123-new-netdb-entries/): एन्क्रिप्टेड LeaseSets और प्रमाणीकरण
- [प्रस्ताव 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [प्रस्ताव 149](/proposals/149-b32-encrypted-ls2/): ब्लाइंडेड पता प्रारूप (b33)
- [प्रस्ताव 152](/proposals/152-ecies-tunnels/): X25519 tunnel निर्माण
- [प्रस्ताव 154](/proposals/154-ecies-lookups/): ECIES डेस्टिनेशनों से डेटाबेस लुकअप्स
- [प्रस्ताव 156](/proposals/156-ecies-routers/): Router का ECIES-X25519 की ओर माइग्रेशन
- [प्रस्ताव 161](/hi/proposals/161-ri-dest-padding/): डेस्टिनेशन पैडिंग संपीड़न
- [प्रस्ताव 167](/proposals/167-service-records/): LeaseSet सर्विस रिकॉर्ड्स
- [प्रस्ताव 169](/proposals/169-pq-crypto/): पोस्ट-क्वांटम हाइब्रिड क्रिप्टोग्राफी (ML-KEM)

## Javadoc संदर्भ

- [I2CP पैकेज](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [क्लाइंट API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## अप्रचलन सारांश

### अप्रचलित संदेश (उपयोग न करें)

- **CreateLeaseSetMessage** (प्रकार 4): CreateLeaseSet2Message का उपयोग करें
- **RequestLeaseSetMessage** (प्रकार 21): RequestVariableLeaseSetMessage का उपयोग करें
- **ReceiveMessageBeginMessage** (प्रकार 6): तेज़ प्राप्ति मोड का उपयोग करें
- **ReceiveMessageEndMessage** (प्रकार 7): तेज़ प्राप्ति मोड का उपयोग करें
- **DestLookupMessage** (प्रकार 34): HostLookupMessage का उपयोग करें
- **DestReplyMessage** (प्रकार 35): HostReplyMessage का उपयोग करें
- **ReportAbuseMessage** (प्रकार 29): कभी कार्यान्वित नहीं किया गया

### अप्रचलित विकल्प

- ElGamal एन्क्रिप्शन (प्रकार 0): ECIES-X25519 (प्रकार 4) पर स्थानांतरित करें
- DSA हस्ताक्षर: EdDSA या ECDSA पर स्थानांतरित करें
- `i2cp.fastReceive=false`: हमेशा तेज़ रिसीव मोड का उपयोग करें
