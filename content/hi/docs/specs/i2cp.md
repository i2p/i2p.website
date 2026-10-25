---
title: "I2P Client Protocol (I2CP)"
description: "एप्लिकेशन I2P router के साथ sessions, tunnels, और LeaseSets की बातचीत कैसे करती हैं।"
slug: "i2cp"
aliases:
  - "/hi/docs/api/i2cp"
  - "/hi/docs/api/i2cp/"
  - "/hi/docs/specs/i2cp-spec"
  - "/hi/docs/specs/i2cp-spec/"
category: "प्रोटोकॉल"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## अवलोकन

यह I2P Control Protocol (I2CP) का विनिर्देश है, जो clients और router के बीच निम्न-स्तरीय इंटरफेस है। Java clients I2CP client API का उपयोग करेंगे, जो इस प्रोटोकॉल को implement करता है।

I2CP को implement करने वाली client-side library का कोई ज्ञात non-Java implementation नहीं है। इसके अतिरिक्त, socket-oriented (streaming) applications को streaming protocol के implementation की आवश्यकता होगी, लेकिन इसके लिए भी कोई non-Java libraries नहीं हैं। इसलिए, non-Java clients को इसके बजाय higher-layer protocol SAM [SAMv3](/docs/api/samv3/) का उपयोग करना चाहिए, जिसके लिए कई भाषाओं में libraries उपलब्ध हैं।

यह एक निम्न-स्तरीय प्रोटोकॉल है जो Java I2P router द्वारा आंतरिक और बाहरी दोनों रूप से समर्थित है। यह प्रोटोकॉल केवल तभी serialized होता है जब client और router एक ही JVM में नहीं हों; अन्यथा, I2CP message Java objects आंतरिक JVM interface के माध्यम से पास किए जाते हैं। I2CP को C++ router i2pd द्वारा भी बाहरी रूप से समर्थित किया जाता है।

अधिक जानकारी I2CP Overview पृष्ठ [I2CP](/docs/specs/i2cp/) पर उपलब्ध है।

## सत्र

यह protocol कई "sessions" को handle करने के लिए design किया गया था, प्रत्येक session का 2-byte session ID होता है, एक single TCP connection पर, हालांकि, Multiple sessions को version 0.9.21 तक implement नहीं किया गया था। नीचे [multisession section](#multisession) देखें। Version 0.9.21 से पुराने routers के साथ single I2CP connection पर multiple sessions का उपयोग करने का प्रयास न करें।

यह भी प्रतीत होता है कि एक single client के लिए अलग connections के माध्यम से कई routers से बात करने के लिए कुछ प्रावधान हैं। यह भी untested है, और शायद उपयोगी नहीं है।

डिस्कनेक्ट के बाद session को बनाए रखने या किसी अलग I2CP connection पर इसे पुनर्प्राप्त करने का कोई तरीका नहीं है। जब socket बंद हो जाता है, तो session नष्ट हो जाता है।

## उदाहरण संदेश अनुक्रम

नोट: नीचे दिए गए उदाहरण Protocol Byte (0x2a) नहीं दिखाते हैं जो client से router को पहली बार कनेक्ट करते समय भेजा जाना चाहिए। कनेक्शन initialization के बारे में अधिक जानकारी I2CP Overview पेज [I2CP](/docs/specs/i2cp/) पर है।

### मानक सत्र स्थापना

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### बैंडविड्थ सीमा प्राप्त करें (सरल सत्र)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### डेस्टिनेशन लुकअप (सिंपल सेशन)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### आउटगोइंग संदेश

मौजूदा session, i2cp.messageReliability=none के साथ

```
  Client                                           Router

                           --------------------->  Send Message Message

```
मौजूदा session, i2cp.messageReliability=none और nonzero nonce के साथ

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
मौजूदा सत्र, i2cp.messageReliability=BestEffort के साथ

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### आने वाला संदेश

मौजूदा सेशन, i2cp.fastReceive=true के साथ (0.9.4 के बाद से)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
मौजूदा सेशन, i2cp.fastReceive=false के साथ (पुराना/अप्रचलित)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### मल्टीसेशन नोट्स {#multisession}

router संस्करण 0.9.21 से एक ही I2CP कनेक्शन पर कई sessions का समर्थन किया जाता है। सबसे पहले बनाया गया session "primary session" होता है। अतिरिक्त sessions "subsessions" होते हैं। Subsessions का उपयोग कई destinations को एक सामान्य tunnels के सेट को साझा करने के लिए किया जाता है। प्रारंभिक application के लिए primary session ECDSA signing keys का उपयोग करता है, जबकि subsession पुराने eepsites के साथ संचार के लिए DSA signing keys का उपयोग करता है।

Subsessions प्राथमिक session के समान inbound और outbound tunnel pools साझा करते हैं। Subsessions को प्राथमिक session के समान encryption keys का उपयोग करना चाहिए। यह LeaseSet encryption keys और (अप्रयुक्त) Destination encryption keys दोनों पर लागू होता है। Subsessions को destination में अलग signing keys का उपयोग करना चाहिए, इसलिए destination hash प्राथमिक session से अलग होता है। चूंकि subsessions प्राथमिक session के समान encryption keys और tunnels का उपयोग करते हैं, सभी के लिए यह स्पष्ट होता है कि Destinations एक ही router पर चल रहे हैं, इसलिए सामान्य anti-correlation anonymity गारंटी लागू नहीं होती।

Subsessions सामान्य रूप से CreateSession संदेश भेजकर और जवाब में SessionStatus संदेश प्राप्त करके बनाए जाते हैं। Subsessions को primary session बनने के बाद ही बनाया जाना चाहिए। SessionStatus प्रतिक्रिया में सफलता पर एक अनूठा Session ID होगा, जो primary session के ID से अलग होगा। जबकि CreateSession संदेश क्रम में प्रसंस्करित होने चाहिए, CreateSession संदेश को प्रतिक्रिया के साथ जोड़ने का कोई निश्चित तरीका नहीं है, इसलिए client के पास एक साथ कई CreateSession संदेश लंबित नहीं होने चाहिए। Subsession के लिए SessionConfig विकल्पों का सम्मान नहीं किया जा सकता जहाँ वे primary session से भिन्न हैं। विशेष रूप से, चूंकि subsessions primary session के समान tunnel pool का उपयोग करते हैं, tunnel विकल्पों को नजरअंदाज किया जा सकता है।

router प्रत्येक Destination के लिए client को अलग RequestVariableLeaseSet संदेश भेजेगा, और client को प्रत्येक के लिए CreateLeaseSet संदेश के साथ उत्तर देना होगा। दो Destinations के लिए leases आवश्यक रूप से समान नहीं होंगे, भले ही वे समान tunnel pool से चुने गए हों।

एक subsession को सामान्य रूप से DestroySession message के साथ नष्ट किया जा सकता है। इससे primary session नष्ट नहीं होगा या I2CP connection रुकेगा नहीं। हालांकि, primary session को नष्ट करने से सभी subsessions नष्ट हो जाएंगे और I2CP connection रुक जाएगा। एक Disconnect message सभी sessions को नष्ट कर देता है।

ध्यान दें कि अधिकांश I2CP संदेशों में Session ID होता है, लेकिन सभी में नहीं। जिनमें Session ID नहीं है, उनके लिए clients को router responses को सही तरीके से handle करने के लिए अतिरिक्त logic की आवश्यकता हो सकती है। DestLookup और DestReply में Session IDs नहीं होते हैं; इसके बजाय नए HostLookup और HostReply का उपयोग करें। GetBandwidthLimts और BandwidthLimits में session IDs नहीं होते हैं, हालांकि response session-specific नहीं है।

### संस्करण नोट्स {#notes}

client द्वारा भेजा गया प्रारंभिक protocol version byte (0x2a) में बदलाव की अपेक्षा नहीं है। release 0.8.7 से पहले, router की version जानकारी client के लिए उपलब्ध नहीं थी, जिससे नए clients का पुराने routers के साथ काम करना रुक जाता था। release 0.8.7 से, दोनों पक्षों की protocol version strings का आदान-प्रदान Get/Set Date Messages में होता है। आगे चलकर, clients इस जानकारी का उपयोग पुराने routers के साथ सही तरीके से संवाद करने के लिए कर सकते हैं। Clients और routers को ऐसे messages नहीं भेजने चाहिए जो दूसरे पक्ष द्वारा समर्थित नहीं हैं, क्योंकि वे आमतौर पर असमर्थित message प्राप्त होने पर session को disconnect कर देते हैं।

आदान-प्रदान की गई version जानकारी "core" API version या I2CP protocol version है, और यह जरूरी नहीं है कि router version हो।

I2CP protocol संस्करणों का एक बुनियादी सारांश निम्नलिखित है। विवरण के लिए, नीचे देखें।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## सामान्य संरचनाएं {#structures}

### I2CP संदेश हेडर {#struct-I2CPMessageHeader}

#### विवरण

सभी I2CP संदेशों का सामान्य हेडर, जिसमें संदेश की लंबाई और संदेश प्रकार होता है।

#### सामग्री

1.  4 byte [Integer](/docs/specs/common-structures/#integer) जो संदेश बॉडी की लंबाई निर्दिष्ट करता है
2.  1 byte [Integer](/docs/specs/common-structures/#integer) जो संदेश प्रकार निर्दिष्ट करता है।
3.  I2CP संदेश बॉडी, 0 या अधिक bytes

#### टिप्पणियां

वास्तविक संदेश लंबाई सीमा लगभग 64 KB है।

### Message ID {#struct-MessageId}

#### विवरण

किसी विशेष समय पर एक particular router पर प्रतीक्षारत संदेश की विशिष्ट पहचान करता है। यह हमेशा router द्वारा उत्पन्न किया जाता है और यह client द्वारा उत्पन्न nonce के समान नहीं है।

#### सामग्री

1.  4 बाइट [Integer](/docs/specs/common-structures/#integer)

#### नोट्स

Message IDs केवल एक session के भीतर unique होती हैं; वे globally unique नहीं होतीं।

### Payload {#struct-Payload}

#### विवरण

यह संरचना एक Destination से दूसरे Destination तक पहुंचाए जा रहे संदेश की सामग्री है।

#### विषय-सूची

1.  4 byte [Integer](/docs/specs/common-structures/#integer) लंबाई
2.  उतने bytes

#### नोट्स

पेलोड gzip प्रारूप में है जैसा कि I2CP Overview पेज [I2CP-FORMAT](/docs/specs/i2cp/#format) पर निर्दिष्ट है।

वास्तविक संदेश लंबाई सीमा लगभग 64 KB है।

### Session Config {#struct-SessionConfig}

#### विवरण

किसी विशेष client session के लिए configuration विकल्पों को परिभाषित करता है।

#### विषय सूची

1.  [Destination](/docs/specs/common-structures/#destination)
2.  विकल्पों का [Mapping](/docs/specs/common-structures/#mapping)
3.  निर्माण [Date](/docs/specs/common-structures/#date)
4.  पिछले 3 फ़ील्ड का [Signature](/docs/specs/common-structures/#signature),
    [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) द्वारा हस्ताक्षरित

#### नोट्स

- विकल्प I2CP Overview पेज पर निर्दिष्ट हैं
  [I2CP-OPTIONS](/docs/specs/i2cp/#options)।
- [Mapping](/docs/specs/common-structures/#mapping) को key के अनुसार क्रमबद्ध होना चाहिए ताकि
  router में signature सही तरीके से validate हो सके।
- creation date router द्वारा प्रोसेस किए जाने पर वर्तमान समय के +/- 30 सेकंड के भीतर होनी चाहिए,
  अन्यथा config को reject कर दिया जाएगा।

#### ऑफलाइन हस्ताक्षर

- यदि [Destination](/docs/specs/common-structures/#destination) offline signed है,
  तो [Mapping](/docs/specs/common-structures/#mapping) में तीन विकल्प होने चाहिए
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, और
  i2cp.leaseSetOfflineSignature। फिर
  [Signature](/docs/specs/common-structures/#signature) transient [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) द्वारा उत्पन्न किया जाता है और
  i2cp.leaseSetTransientPublicKey में निर्दिष्ट
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) के साथ सत्यापित किया जाता है। विवरण के लिए
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) देखें।

### Session ID {#struct-SessionId}

#### विवरण

किसी विशेष router पर एक समय बिंदु में session की विशिष्ट पहचान करता है।

#### विषय सूची

1.  2 byte [Integer](/docs/specs/common-structures/#integer)

#### नोट्स

Session ID 0xffff का उपयोग "कोई session नहीं" को दर्शाने के लिए किया जाता है, उदाहरण के लिए hostname lookups के लिए।

## संदेश

[I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html) भी देखें।

### संदेश प्रकार {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### विवरण

क्लाइंट को बताएं कि bandwidth की सीमाएं क्या हैं।

Router से Client को [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) के जवाब में भेजा गया।

#### विषय-सूची

1.  4 byte [Integer](/docs/specs/common-structures/#integer) Client inbound सीमा
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) Client outbound सीमा
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Router inbound सीमा
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Router inbound burst सीमा
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Router outbound सीमा
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Router outbound burst
    सीमा (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Router burst समय
    (seconds)
8.  नौ 4-byte [Integer](/docs/specs/common-structures/#integer) (अपरिभाषित)

#### नोट्स

क्लाइंट सीमाएं केवल सेट की गई मान हो सकती हैं, और ये वास्तविक router सीमाएं हो सकती हैं, या router सीमाओं का प्रतिशत हो सकती हैं, या विशिष्ट क्लाइंट के लिए हो सकती हैं, यह implementation पर निर्भर करता है। router सीमाओं के रूप में लेबल किए गए सभी मान 0 हो सकते हैं, यह implementation पर निर्भर करता है। रिलीज़ 0.7.2 के अनुसार।

### BlindingInfoMessage {#BlindingInfoMessage}

#### विवरण

router को सूचित करें कि एक Destination blinded है, वैकल्पिक lookup password और decryption के लिए वैकल्पिक private key के साथ। विवरण के लिए proposals 123 और 149 देखें।

router को पता होना चाहिए कि कोई destination blinded है या नहीं। यदि यह blinded है और secret या per-client authentication का उपयोग करता है, तो उसके पास वह जानकारी भी होनी चाहिए।

एक नए प्रारूप के b32 address ("b33") का Host Lookup router को बताता है कि address blinded है, लेकिन Host Lookup message में secret या private key को router तक पहुंचाने का कोई तंत्र नहीं है। जबकि हम Host Lookup message को उस जानकारी को जोड़ने के लिए विस्तृत कर सकते हैं, एक नया message परिभाषित करना अधिक स्वच्छ है।

यह संदेश client के लिए router को बताने का एक प्रोग्रामैटिक तरीका प्रदान करता है। अन्यथा, उपयोगकर्ता को प्रत्येक destination को मैन्युअल रूप से कॉन्फ़िगर करना पड़ता।

#### उपयोग

किसी client द्वारा blinded destination पर message भेजने से पहले, उसे या तो Host Lookup message में "b33" को lookup करना होगा, या Blinding Info message भेजना होगा। यदि blinded destination को secret या per-client authentication की आवश्यकता है, तो client को Blinding Info message भेजना होगा।

Router इस संदेश का कोई उत्तर नहीं भेजता। Client से Router को भेजा जाता है।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Bit order: 76543210 > - Bit 0: सभी के लिए 0, per-client के लिए 1 > - Bits 3-1: Authentication scheme, यदि bit 0 को per-client के लिए >   1 पर सेट किया गया है, अन्यथा 000 >   - 000: DH client authentication (या कोई per-client authentication नहीं) >   - 001: PSK client authentication > - Bit 4: यदि secret आवश्यक है तो 1, यदि कोई secret आवश्यक नहीं है तो 0 > - Bits 7-5: अप्रयुक्त, भविष्य की संगतता के लिए 0 पर सेट करें

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Endpoint प्रकार

> - Type 0 एक [Hash](/docs/specs/common-structures/#hash) है > - Type 1 एक hostname [String](/docs/specs/common-structures/#string) है > - Type 2 एक [Destination](/docs/specs/common-structures/#destination) है > - Type 3 एक Sig Type और >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) है

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Expiration Seconds since
    epoch
6.  Endpoint: Data as specified, one of

> - Type 0: 32 byte [Hash](/docs/specs/common-structures/#hash) > > - Type 1: host name [String](/docs/specs/common-structures/#string) > > - Type 2: binary [Destination](/docs/specs/common-structures/#destination) > >  > >  - Type 3: 2 byte [Integer](/docs/specs/common-structures/#integer) signature type, के बाद > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (लंबाई जैसा कि >       sig type द्वारा निहित है)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) डिक्रिप्शन key केवल तभी मौजूद होती है
    जब flag bit 0 को 1 पर सेट किया गया हो। एक 32-byte ECIES_X25519 private key,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Lookup Password केवल तभी मौजूद होता है जब
    flag bit 4 को 1 पर सेट किया गया हो।

#### नोट्स

- रिलीज़ 0.9.43 के अनुसार।
- Hash endpoint प्रकार संभवतः तब तक उपयोगी नहीं है जब तक कि router address book में reverse lookup करके Destination प्राप्त नहीं कर सकता।
- Hostname endpoint प्रकार संभवतः तब तक उपयोगी नहीं है जब तक कि router address book में lookup करके Destination प्राप्त नहीं कर सकता।

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

DEPRECATED। LeaseSet2, ऑफ़लाइन keys, non-ElGamal encryption प्रकार, कई encryption प्रकार, या encrypted LeaseSets के लिए उपयोग नहीं किया जा सकता। सभी routers 0.9.39 या उससे ऊपर के साथ CreateLeaseSet2Message का उपयोग करें।

#### विवरण

यह संदेश एक [RequestLeaseSetMessage](#RequestLeaseSetMessage) या [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) के जवाब में भेजा जाता है और इसमें सभी [Lease](/docs/specs/common-structures/#lease) संरचनाएं होती हैं जो I2NP Network Database में प्रकाशित की जानी चाहिए।

क्लाइंट से router को भेजा गया।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) या 20
    bytes को अनदेखा किया जाता है
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### नोट्स

SigningPrivateKey LeaseSet के भीतर से [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) से तभी मेल खाता है जब signing key का प्रकार DSA हो। यह LeaseSet revocation के लिए है, जो अभी तक लागू नहीं किया गया है और संभावना नहीं है कि कभी लागू किया जाएगा। यदि signing key का प्रकार DSA नहीं है, तो इस फ़ील्ड में 20 bytes का random data होता है। इस फ़ील्ड की लंबाई हमेशा 20 bytes होती है, यह कभी भी non-DSA signing private key की लंबाई के बराबर नहीं होती।

PrivateKey, LeaseSet के [PublicKey](/docs/specs/common-structures/#publickey) से मेल खाती है। garlic routed संदेशों को decrypt करने के लिए PrivateKey आवश्यक है।

Revocation अभी तक implement नहीं है। किसी भी client library में multiple routers से connection अभी तक implement नहीं है।

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### विवरण

यह संदेश [RequestLeaseSetMessage](#RequestLeaseSetMessage) या [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) के जवाब में भेजा जाता है और इसमें सभी [Lease](/docs/specs/common-structures/#lease) संरचनाएं होती हैं जो I2NP Network Database में प्रकाशित की जानी चाहिए।

Client से Router को भेजा गया। रिलीज 0.9.39 के बाद से। EncryptedLeaseSet के लिए प्रति-client प्रमाणीकरण 0.9.41 से समर्थित है। MetaLeaseSet अभी तक I2CP के माध्यम से समर्थित नहीं है। अधिक जानकारी के लिए प्रस्ताव 123 देखें।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  फॉलो करने के लिए lease set का एक बाइट प्रकार।

> - Type 1 एक [LeaseSet](/docs/specs/common-structures/#leaseset) है (deprecated) > - Type 3 एक [LeaseSet2](/docs/specs/common-structures/#leaseset2) है > - Type 5 एक [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) है > - Type 7 एक [MetaLeaseSet](/docs/specs/common-structures/#leaseset2) है

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) या
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) या
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) या
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  आने वाली private keys की संख्या के लिए एक byte।
5.  [PrivateKey](/docs/specs/common-structures/#privatekey) सूची। lease set में प्रत्येक public key के लिए एक, समान क्रम में। (Meta LS2 के लिए उपस्थित नहीं)

> - एन्क्रिप्शन प्रकार (2 byte [Integer](/docs/specs/common-structures/#integer)) > - एन्क्रिप्शन key की लंबाई (2 byte [Integer](/docs/specs/common-structures/#integer)) > - एन्क्रिप्शन [PrivateKey](/docs/specs/common-structures/#privatekey) (निर्दिष्ट >   bytes की संख्या)

#### नोट्स

PrivateKeys, LeaseSet के प्रत्येक [PublicKey](/docs/specs/common-structures/#publickey) से मेल खाती हैं। garlic routed संदेशों को decrypt करने के लिए PrivateKeys आवश्यक हैं।

Encrypted LeaseSets पर अधिक जानकारी के लिए प्रस्ताव 123 देखें।

MetaLeaseSet की सामग्री और प्रारूप प्रारंभिक हैं और परिवर्तन के अधीन हैं। कई router के प्रशासन के लिए कोई निर्दिष्ट प्रोटोकॉल नहीं है। अधिक जानकारी के लिए प्रस्ताव 123 देखें।

हस्ताक्षर करने वाली निजी कुंजी, जो पहले निरसन के लिए परिभाषित थी और अप्रयुक्त थी, LS2 में मौजूद नहीं है।

प्रारंभिक संस्करण message type 40 के साथ 0.9.38 में था लेकिन format बदल दिया गया था। Type 40 को छोड़ दिया गया है और यह असमर्थित है। Type 41, 0.9.39 तक वैध नहीं है।

### CreateSessionMessage {#CreateSessionMessage}

#### विवरण

यह संदेश एक client से session शुरू करने के लिए भेजा जाता है, जहाँ एक session को एकल Destination के network से connection के रूप में परिभाषित किया गया है, जिसके माध्यम से उस Destination के लिए सभी संदेश पहुंचाए जाएंगे और जिसके माध्यम से वह Destination किसी भी अन्य Destination को भेजे जाने वाले सभी संदेश भेजेगा।

Client से Router को भेजा गया। router [SessionStatusMessage](#SessionStatusMessage) के साथ जवाब देता है।

#### विषय-सूची

1.  [Session Config](#struct-sessionconfig)

#### नोट्स

- यह client द्वारा भेजा गया दूसरा message है। पहले client ने एक [GetDateMessage](#GetDateMessage) भेजा था और [SetDateMessage](#SetDateMessage) response प्राप्त किया था।
- यदि Session Config में Date router के current time से बहुत अलग है (+/- 30 seconds से अधिक), तो session को reject कर दिया जाएगा।
- यदि इस Destination के लिए router पर पहले से ही एक session मौजूद है, तो session को reject कर दिया जाएगा।
- Session Config में [Mapping](/docs/specs/common-structures/#mapping) को key के अनुसार sorted होना चाहिए ताकि router में signature सही तरीके से validate हो सके।

### DestLookupMessage {#DestLookupMessage}

#### विवरण

Client से Router को भेजा गया। Router एक [DestReplyMessage](#DestReplyMessage) के साथ जवाब देता है।

#### विषय-सूची

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### नोट्स

रिलीज़ 0.7 के अनुसार।

रिलीज 0.8.3 के अनुसार, मल्टिपल आउटस्टैंडिंग लुकअप समर्थित हैं, और लुकअप I2PSimpleSession और मानक सत्रों दोनों में समर्थित हैं।

रिलीज़ 0.9.11 के बाद से [HostLookupMessage](#HostLookupMessage) को प्राथमिकता दी जाती है।

### DestReplyMessage {#DestReplyMessage}

#### विवरण

[DestLookupMessage](#DestLookupMessage) के जवाब में Router से Client को भेजा गया।

#### विषय-सूची

1.  सफलता पर [Destination](/docs/specs/common-structures/#destination), या
    असफलता पर [Hash](/docs/specs/common-structures/#hash)

#### नोट्स

रिलीज़ 0.7 के अनुसार।

रिलीज़ 0.8.3 के अनुसार, यदि lookup असफल हो जाता है तो अनुरोधित Hash वापस किया जाता है, ताकि client के पास कई lookups outstanding हो सकें और replies को lookups के साथ correlate कर सकें। किसी Destination response को request के साथ correlate करने के लिए, Destination का Hash लें। रिलीज़ 0.8.3 से पहले, असफलता पर response खाली होता था।

### DestroySessionMessage {#DestroySessionMessage}

#### विवरण

यह संदेश एक client द्वारा session को नष्ट करने के लिए भेजा जाता है।

Client से Router को भेजा गया। Router को [SessionStatusMessage](#SessionStatusMessage) (Destroyed) के साथ जवाब देना चाहिए। हालांकि, नीचे दिए गए महत्वपूर्ण नोट्स देखें।

#### सामग्री

1.  [Session ID](#struct-sessionid)

#### नोट्स

इस बिंदु पर router को सत्र (session) से संबंधित सभी संसाधनों को मुक्त कर देना चाहिए।

API 0.9.66 के माध्यम से, Java I2P router और client libraries इस specification से काफी अलग हैं। Router कभी भी SessionStatus(Destroyed) response नहीं भेजता। यदि कोई sessions बचे नहीं हैं, तो यह एक [DisconnectMessage](#DisconnectMessage) भेजता है। यदि subsessions हैं या primary session बचा है, तो यह reply नहीं करता।

Java client library एक SessionStatus संदेश का जवाब सभी sessions को नष्ट करके और पुनः कनेक्ट करके देती है।

कई sessions के साथ एक connection पर व्यक्तिगत subsessions को नष्ट करना विभिन्न router और client implementations पर पूर्ण रूप से परीक्षित या कार्यशील नहीं हो सकता है। सावधानी बरतें।

Implementations को एक primary session के लिए destroy को सभी subsessions के लिए destroy के रूप में treat करना चाहिए, लेकिन एक single subsession के लिए destroy की अनुमति देनी चाहिए और connection को open रखना चाहिए, लेकिन Java I2P अभी ऐसा नहीं करता है। यदि Java I2P behavior को बाद की releases में बदला जाता है, तो यह यहाँ documented होगा।

### DisconnectMessage {#DisconnectMessage}

#### विवरण

दूसरी पार्टी को बताएं कि समस्याएं हैं और वर्तमान कनेक्शन नष्ट होने वाला है। यह उस कनेक्शन पर सभी सत्रों को समाप्त कर देता है। socket जल्द ही बंद हो जाएगा। या तो router से client को या client से router को भेजा जाता है।

#### सामग्री

1.  कारण [String](/docs/specs/common-structures/#string)

#### नोट्स

केवल router-to-client दिशा में लागू किया गया है, कम से कम Java I2P में।

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### विवरण

router से अनुरोध करें कि वह बताए कि उसकी वर्तमान bandwidth सीमाएं क्या हैं।

Client से Router को भेजा गया। Router [BandwidthLimitsMessage](#BandwidthLimitsMessage) के साथ जवाब देता है।

#### सामग्री

*कोई नहीं*

#### नोट्स

रिलीज़ 0.7.2 के अनुसार।

रिलीज 0.8.3 से, I2PSimpleSession और मानक सेशन दोनों में समर्थित है।

### GetDateMessage {#GetDateMessage}

#### विवरण

Client से Router को भेजा गया। router [SetDateMessage](#SetDateMessage) के साथ जवाब देता है।

#### सामग्री

1.  I2CP API Version [String](/docs/specs/common-structures/#string)
2.  Authentication [Mapping](/docs/specs/common-structures/#mapping) (वैकल्पिक, रिलीज 0.9.11 के अनुसार)

#### टिप्पणियाँ

- आमतौर पर protocol version byte भेजने के बाद client द्वारा भेजा जाने वाला पहला संदेश।
- Version string को release 0.8.7 से शामिल किया गया है। यह तभी उपयोगी है जब client और router एक ही JVM में न हों। यदि यह मौजूद नहीं है, तो client version 0.8.6 या उससे पहले का है।
- Release 0.9.11 से, authentication
  [Mapping](/docs/specs/common-structures/#mapping) शामिल की जा सकती है, जिसमें keys
  i2cp.username और i2cp.password होती हैं। Mapping को sorted होने की जरूरत नहीं क्योंकि
  यह संदेश signed नहीं है। 0.9.10 और उसके पहले तक,
  authentication को [Session Config](#struct-sessionconfig)
  Mapping में शामिल किया जाता था, और
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), या
  [DestLookupMessage](#DestLookupMessage) के लिए कोई authentication enforce नहीं की जाती थी। जब enabled हो, तो
  [GetDateMessage](#GetDateMessage) के माध्यम से authentication
  release 0.9.16 से किसी भी अन्य संदेश से पहले आवश्यक है। यह केवल router
  context के बाहर उपयोगी है। यह एक incompatible बदलाव है, लेकिन यह केवल authentication के साथ
  router context के बाहर के sessions को प्रभावित करेगा, जो दुर्लभ होना चाहिए।

### HostLookupMessage {#HostLookupMessage}

#### विवरण

Client से Router को भेजा गया। Router एक [HostReplyMessage](#HostReplyMessage) के साथ जवाब देता है।

यह [DestLookupMessage](#DestLookupMessage) को प्रतिस्थापित करता है और एक request ID, timeout, और host name lookup समर्थन जोड़ता है। चूंकि यह Hash lookups का भी समर्थन करता है, यदि router इसका समर्थन करता है तो इसका उपयोग सभी lookups के लिए किया जा सकता है। Host name lookups के लिए, router अपने context की naming service से query करेगा। यह केवल तभी उपयोगी है जब client router के context के बाहर हो। Router context के अंदर, client को स्वयं naming service से query करना चाहिए, जो बहुत अधिक कुशल है।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) request ID
3.  4 byte [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) request type
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) या host name
    [String](/docs/specs/common-structures/#string) या
    [Destination](/docs/specs/common-structures/#destination)

अनुरोध के प्रकार:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Types 2-4 अनुरोध करते हैं कि LeaseSet से options mapping को HostReply संदेश में वापस किया जाए। proposal 167 देखें।

#### नोट्स

- रिलीज़ 0.9.11 के अनुसार। पुराने routers के लिए [DestLookupMessage](#DestLookupMessage) का उपयोग करें।
- session ID और request ID को [HostReplyMessage](#HostReplyMessage) में वापस किया जाएगा। यदि कोई session नहीं है तो session ID के लिए 0xFFFF का उपयोग करें।
- Timeout Hash lookups के लिए उपयोगी है। न्यूनतम 10,000 (10 सेकंड) की सिफारिश की जाती है। भविष्य में यह remote naming service lookups के लिए भी उपयोगी हो सकता है। यह मान local host name lookups के लिए सम्मानित नहीं किया जा सकता है, जो तेज़ होना चाहिए।
- Base 32 host name lookup समर्थित है लेकिन इसे पहले Hash में बदलना बेहतर होता है।

### HostReplyMessage {#HostReplyMessage}

#### विवरण

Router से Client को [HostLookupMessage](#HostLookupMessage) के जवाब में भेजा जाता है।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) अनुरोध ID
3.  1 byte [Integer](/docs/specs/common-structures/#integer) परिणाम कोड

> - 0: सफलता > - 1: विफलता > - 2: Lookup पासवर्ड आवश्यक (0.9.43 के अनुसार) > - 3: Private key आवश्यक (0.9.43 के अनुसार) > - 4: Lookup पासवर्ड और private key आवश्यक (0.9.43 के अनुसार) > - 5: Leaseset डिक्रिप्शन विफलता (0.9.43 के अनुसार) > - 6: Leaseset lookup विफलता (0.9.66 के अनुसार) > - 7: Lookup प्रकार असमर्थित (0.9.66 के अनुसार)

4.  [Destination](/docs/specs/common-structures/#destination), केवल तभी मौजूद जब result
    code शून्य है, सिवाय lookup types 2-4 के लिए भी वापस किया जा सकता है। नीचे
    देखें।
5.  [Mapping](/docs/specs/common-structures/#mapping), केवल तभी मौजूद जब result code
    शून्य है, केवल lookup types 2-4 के लिए वापस किया जाता है। 0.9.66 के अनुसार। नीचे
    देखें।

#### लुकअप प्रकार 2-4 के लिए प्रतिक्रियाएं

प्रस्ताव 167 अतिरिक्त lookup प्रकारों को परिभाषित करता है जो leaseset से सभी विकल्प वापस करते हैं, यदि उपलब्ध हों। lookup प्रकार 2-4 के लिए, router को leaseset प्राप्त करना चाहिए, भले ही lookup key address book में हो।

यदि सफल हो, तो HostReply में leaseset से options Mapping शामिल होगी, और इसे destination के बाद आइटम 5 के रूप में शामिल करेगी। यदि Mapping में कोई options नहीं हैं, या leaseset version 1 था, तो भी इसे एक खाली Mapping के रूप में शामिल किया जाएगा (दो bytes: 0 0)। leaseset से सभी options शामिल किए जाएंगे, केवल service record options नहीं। उदाहरण के लिए, भविष्य में परिभाषित parameters के लिए options मौजूद हो सकते हैं। वापस की गई Mapping sorted हो भी सकती है और नहीं भी, यह implementation पर निर्भर है।

Leaseset lookup विफलता पर, उत्तर में एक नया error code 6 (Leaseset lookup failure) होगा और इसमें mapping शामिल नहीं होगी। जब error code 6 वापस किया जाता है, तो Destination field मौजूद हो भी सकता है और नहीं भी। यह तब मौजूद होगा जब address book में hostname lookup सफल हो गया हो, या यदि पिछली lookup सफल रही हो और परिणाम cache हो गया हो, या यदि Destination lookup message में मौजूद था (lookup type 4)।

यदि कोई lookup type समर्थित नहीं है, तो उत्तर में एक नया error code 7 (lookup type unsupported) होगा।

#### नोट्स

- रिलीज 0.9.11 के अनुसार। [HostLookupMessage](#HostLookupMessage) नोट्स देखें।
- session ID और request ID वे हैं जो [HostLookupMessage](#HostLookupMessage) से हैं।
- result code सफलता के लिए 0 है, विफलता के लिए 1-255। 1 एक सामान्य विफलता को दर्शाता है। 0.9.43 के अनुसार, अतिरिक्त विफलता कोड 2-5 को "b33" lookups के लिए विस्तारित त्रुटियों का समर्थन करने के लिए परिभाषित किया गया था। अतिरिक्त जानकारी के लिए proposals 123 और 149 देखें। 0.9.66 के अनुसार, अतिरिक्त विफलता कोड 6-7 को type 2-4 lookups के लिए विस्तारित त्रुटियों का समर्थन करने के लिए परिभाषित किया गया था। अतिरिक्त जानकारी के लिए proposal 167 देखें।

### MessagePayloadMessage {#MessagePayloadMessage}

#### विवरण

संदेश के payload को client तक पहुंचाएं।

Router से Client को भेजा गया। यदि i2cp.fastReceive=true है, जो कि default नहीं है, तो client [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) के साथ जवाब देता है।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)
3.  [Payload](#struct-payload)

#### टिप्पणियां

### MessageStatusMessage {#MessageStatusMessage}

#### विवरण

आने वाले या जाने वाले message की delivery status के बारे में client को सूचित करें। Router से Client को भेजा जाता है। यदि यह message इंगित करता है कि एक आने वाला message उपलब्ध है, तो client एक [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) के साथ जवाब देता है। एक जाने वाले message के लिए, यह एक [SendMessageMessage](#SendMessageMessage) या [SendMessageExpiresMessage](#SendMessageExpiresMessage) का response है।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) router द्वारा उत्पन्न
3.  1 byte [Integer](/docs/specs/common-structures/#integer) status
4.  4 byte [Integer](/docs/specs/common-structures/#integer) size
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce जो पहले client द्वारा उत्पन्न किया गया था

#### नोट्स

संस्करण 0.9.4 तक, ज्ञात status values हैं 0 संदेश उपलब्ध है के लिए, 1 स्वीकृत के लिए, 2 best effort सफल के लिए, 3 best effort असफल के लिए, 4 guaranteed सफल के लिए, 5 guaranteed असफल के लिए। size Integer उपलब्ध संदेश का आकार निर्दिष्ट करता है और केवल status = 0 के लिए प्रासंगिक है। यद्यपि guaranteed अभी तक कार्यान्वित नहीं है, (best effort ही एकमात्र सेवा है), वर्तमान router कार्यान्वयन guaranteed status codes का उपयोग करता है, best effort codes का नहीं।

router संस्करण 0.9.5 से, अतिरिक्त status codes परिभाषित किए गए हैं, हालांकि वे जरूरी नहीं कि implemented हों। विवरण के लिए [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) देखें। outgoing messages के लिए, codes 1, 2, 4, और 6 सफलता दर्शाते हैं; बाकी सभी विफलताएं हैं। वापस मिलने वाले failure codes अलग हो सकते हैं और implementation-specific हैं।

सभी स्थिति कोड:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
जब status = 1 (स्वीकृत), तो nonce [SendMessageMessage](#SendMessageMessage) में मौजूद nonce से मेल खाता है, और शामिल Message ID का उपयोग बाद की सफलता या विफलता की अधिसूचना के लिए किया जाएगा। अन्यथा, nonce को नजरअंदाज किया जा सकता है।

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

अप्रचलित। i2pd द्वारा समर्थित नहीं।

#### विवरण

router से अनुरोध करें कि वह एक संदेश डिलीवर करे जिसके बारे में उसे पहले सूचित किया गया था। Client से Router को भेजा जाता है। router [MessagePayloadMessage](#MessagePayloadMessage) के साथ जवाब देता है।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)

#### नोट्स

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) को [MessageStatusMessage](#MessageStatusMessage) के जवाब के रूप में भेजा जाता है जो यह बताता है कि एक नया संदेश pickup के लिए उपलब्ध है। यदि [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) में निर्दिष्ट message id अमान्य या गलत है, तो router बस कोई उत्तर नहीं दे सकता, या वह [DisconnectMessage](#DisconnectMessage) वापस भेज सकता है।

यह "fast receive" मोड में अप्रयुक्त है, जो रिलीज 0.9.4 से डिफ़ॉल्ट है।

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

अप्रचलित। i2pd द्वारा समर्थित नहीं।

#### विवरण

router को बताएं कि संदेश की डिलीवरी सफलतापूर्वक पूर्ण हो गई है और router संदेश को त्याग सकता है।

क्लाइंट से router को भेजा गया।

#### विषय सूची

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)

#### नोट्स

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage) एक [MessagePayloadMessage](#MessagePayloadMessage) के द्वारा संदेश का payload पूरी तरह से deliver होने के बाद भेजा जाता है।

यह "fast receive" मोड में अप्रयुक्त है, जो रिलीज 0.9.4 के बाद से डिफ़ॉल्ट है।

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### विवरण

Client से Router को session configuration अपडेट करने के लिए भेजा जाता है। Router [SessionStatusMessage](#SessionStatusMessage) के साथ जवाब देता है।

#### विषयसूची

1.  [Session ID](#struct-sessionid)
2.  [Session Config](#struct-sessionconfig)

#### नोट्स

- रिलीज़ 0.7.1 के अनुसार।
- यदि Session Config में Date router के वर्तमान समय से बहुत अधिक (+/- 30
  सेकंड से अधिक) अलग है, तो session को
  अस्वीकार कर दिया जाएगा।
- Session Config में [Mapping](/docs/specs/common-structures/#mapping) को
  key के अनुसार क्रमबद्ध होना चाहिए ताकि signature को
  router में सही तरीके से validate किया जा सके।
- कुछ configuration विकल्प केवल
  [CreateSessionMessage](#CreateSessionMessage) में ही सेट किए जा सकते हैं, और यहाँ के परिवर्तनों को
  router द्वारा पहचाना नहीं जाएगा। tunnel विकल्पों inbound.\*
  और outbound.\* में परिवर्तन हमेशा पहचाने जाते हैं।
- सामान्यतः, router को अपडेट की गई config को
  वर्तमान config के साथ merge करना चाहिए, इसलिए अपडेट की गई config में केवल नए या
  बदले गए विकल्पों को शामिल करना पर्याप्त है। हालांकि, merge के कारण, विकल्पों को इस तरीके से
  हटाया नहीं जा सकता; उन्हें स्पष्ट रूप से वांछित
  default value पर सेट करना होगा।

### ReportAbuseMessage {#ReportAbuseMessage}

अप्रचलित, अप्रयुक्त, असमर्थित

#### विवरण

दूसरे पक्ष (client या router) को बताएं कि वे हमले के तहत हैं, संभावित रूप से किसी विशेष MessageId के संदर्भ के साथ। यदि router हमले के तहत है, तो client दूसरे router पर माइग्रेट करने का निर्णय ले सकता है, और यदि कोई client हमले के तहत है, तो router अपने routers को फिर से बना सकता है या उन peers को banlist कर सकता है जिन्होंने इसे हमला करने वाले संदेश भेजे थे।

router से client को या client से router को भेजा जाता है।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) दुरुपयोग गंभीरता (0 न्यूनतम दुरुपयोग है, 255 अत्यधिक दुरुपयोग है)
3.  कारण [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### नोट्स

अप्रयुक्त। पूर्ण रूप से कार्यान्वित नहीं। router और client दोनों एक [ReportAbuseMessage](#ReportAbuseMessage) उत्पन्न कर सकते हैं, लेकिन प्राप्त होने पर संदेश के लिए किसी के पास हैंडलर नहीं है।

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

अप्रचलित। i2pd द्वारा समर्थित नहीं। Java I2P द्वारा clients संस्करण 0.9.7 या उच्चतर (2013-07) को नहीं भेजा जाता। RequestVariableLeaseSetMessage का उपयोग करें।

#### विवरण

अनुरोध करें कि एक client किसी विशेष inbound tunnels के सेट को शामिल करने की अधिकारिता दे। Router से Client को भेजा जाता है। client [CreateLeaseSetMessage](#CreateLeaseSetMessage) के साथ जवाब देता है।

session पर भेजे गए इन संदेशों में से पहला संदेश client को यह संकेत देता है कि tunnel बन गए हैं और traffic के लिए तैयार हैं। router को तब तक इन संदेशों में से पहला नहीं भेजना चाहिए जब तक कि कम से कम एक inbound और एक outbound tunnel नहीं बन जाते। यदि कुछ समय बाद इन संदेशों में से पहला प्राप्त नहीं होता है तो clients को timeout करके session को नष्ट कर देना चाहिए (अनुशंसित: 5 मिनट या अधिक)।

#### विषय-सूची

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) tunnel की संख्या
3.  उतने जोड़े:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  समाप्ति [Date](/docs/specs/common-structures/#date)

#### नोट्स

यह एक [LeaseSet](/docs/specs/common-structures/#leaseset) का अनुरोध करता है जिसमें सभी [Lease](/docs/specs/common-structures/#lease) entries एक ही समय पर expire होने के लिए सेट होती हैं। client versions 0.9.7 या उससे ऊपर के लिए, [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) का उपयोग किया जाता है।

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### विवरण

अनुरोध करें कि एक client विशिष्ट inbound tunnels के समूह को शामिल करने की अधिकारिता प्रदान करे।

Router से Client को भेजा गया। Client एक [CreateLeaseSetMessage](#CreateLeaseSetMessage) या [CreateLeaseSet2Message](#CreateLeaseSet2Message) के साथ जवाब देता है।

सत्र पर भेजा गया इनमें से पहला संदेश क्लाइंट को यह संकेत देता है कि tunnel बन गए हैं और ट्रैफिक के लिए तैयार हैं। router को इनमें से पहला संदेश तब तक नहीं भेजना चाहिए जब तक कम से कम एक inbound और एक outbound tunnel नहीं बन जाता। यदि कुछ समय बाद इनमें से पहला संदेश प्राप्त नहीं होता है तो क्लाइंट्स को सत्र को timeout करके नष्ट कर देना चाहिए (अनुशंसित: 5 मिनट या अधिक)।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) tunnel की संख्या
3.  उतनी [Lease](/docs/specs/common-structures/#lease) entries

#### नोट्स

यह प्रत्येक [Lease](/docs/specs/common-structures/#lease) के लिए व्यक्तिगत समाप्ति समय के साथ एक [LeaseSet](/docs/specs/common-structures/#leaseset) का अनुरोध करता है।

रिलीज़ 0.9.7 के अनुसार। उससे पहले के रिलीज़ के क्लाइंट्स के लिए, [RequestLeaseSetMessage](#RequestLeaseSetMessage) का उपयोग करें।

### SendMessageMessage {#SendMessageMessage}

#### विवरण

यह वह तरीका है जिससे एक client किसी [Destination](/docs/specs/common-structures/#destination) को message (payload) भेजता है। router एक default expiration का उपयोग करेगा।

क्लाइंट से router को भेजा गया। router एक [MessageStatusMessage](#MessageStatusMessage) के साथ जवाब देता है।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 बाइट [Integer](/docs/specs/common-structures/#integer) nonce

#### नोट्स

जैसे ही [SendMessageMessage](#SendMessageMessage) पूर्ण रूप से बरकरार पहुंचता है, router को एक [MessageStatusMessage](#MessageStatusMessage) वापस करना चाहिए जो बताए कि यह delivery के लिए स्वीकार कर लिया गया है। उस message में वही nonce होगा जो यहाँ भेजा गया था। बाद में, session configuration की delivery guarantees के आधार पर, router अतिरिक्त रूप से एक और [MessageStatusMessage](#MessageStatusMessage) भेज सकता है जो status को अपडेट करे।

रिलीज़ 0.8.1 के अनुसार, यदि i2cp.messageReliability=none है तो router कोई भी [MessageStatusMessage](#MessageStatusMessage) नहीं भेजता है।

रिलीज 0.9.4 से पहले, 0 का nonce value की अनुमति नहीं थी। रिलीज 0.9.4 के अनुसार, 0 का nonce value की अनुमति है, और यह router को बताता है कि उसे कोई भी [MessageStatusMessage](#MessageStatusMessage) नहीं भेजना चाहिए, यानी यह केवल इस संदेश के लिए i2cp.messageReliability=none की तरह काम करता है।

रिलीज़ 0.9.14 से पहले, i2cp.messageReliability=none वाले session को प्रति-message के आधार पर override नहीं किया जा सकता था। रिलीज़ 0.9.14 के अनुसार, i2cp.messageReliability=none वाले session में, client nonce को nonzero value पर सेट करके delivery success या failure के साथ [MessageStatusMessage](#MessageStatusMessage) की delivery का अनुरोध कर सकता है। Router "accepted" [MessageStatusMessage](#MessageStatusMessage) नहीं भेजेगा लेकिन बाद में client को समान nonce के साथ, और success या failure value के साथ [MessageStatusMessage](#MessageStatusMessage) भेजेगा।

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### विवरण

Client से Router को भेजा गया। [SendMessageMessage](#SendMessageMessage) के समान, सिवाय इसके कि इसमें expiration और options शामिल हैं।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 bytes के flags (options)
6.  Expiration [Date](/docs/specs/common-structures/#date) को 8 bytes से घटाकर 6
    bytes किया गया

#### नोट्स

रिलीज़ 0.7.1 तक।

"best effort" mode में, जैसे ही SendMessageExpiresMessage पूरी तरह से बरकरार पहुंचता है, router को एक MessageStatusMessage वापस करना चाहिए जो बताए कि इसे delivery के लिए स्वीकार कर लिया गया है। उस message में वही nonce होगा जो यहां भेजा गया था। बाद में, session configuration की delivery guarantees के आधार पर, router status को update करते हुए एक और MessageStatusMessage भी भेज सकता है।

रिलीज़ 0.8.1 के अनुसार, router किसी भी Message Status Message को नहीं भेजता यदि i2cp.messageReliability=none है।

रिलीज़ 0.9.4 से पहले, 0 का nonce मान अनुमतित नहीं था। रिलीज़ 0.9.4 से, 0 का nonce मान अनुमतित है, और यह router को बताता है कि उसे कोई भी Message Status Message नहीं भेजना चाहिए, यानी यह केवल इस संदेश के लिए i2cp.messageReliability=none की तरह काम करता है।

रिलीज़ 0.9.14 से पहले, i2cp.messageReliability=none के साथ एक सेशन को प्रति-मेसेज आधार पर ओवरराइड नहीं किया जा सकता था। रिलीज़ 0.9.14 से, i2cp.messageReliability=none के साथ एक सेशन में, क्लाइंट nonce को एक गैर-शून्य मान सेट करके डिलीवरी की सफलता या असफलता के साथ Message Status Message की डिलीवरी का अनुरोध कर सकता है। router "accepted" Message Status Message नहीं भेजेगा लेकिन बाद में यह क्लाइंट को समान nonce के साथ, और सफलता या असफलता मान के साथ एक Message Status Message भेजेगा।

#### फ्लैग्स फील्ड

रिलीज़ 0.8.4 के अनुसार, Date के ऊपरी दो बाइट्स को flags को शामिल करने के लिए पुनः परिभाषित किया गया है। पिछली संगतता के लिए flags का डिफ़ॉल्ट मान सभी शून्य होना चाहिए। Date वर्ष 10889 तक flags फ़ील्ड में हस्तक्षेप नहीं करेगा। flags का उपयोग एप्लिकेशन द्वारा router को संकेत प्रदान करने के लिए किया जा सकता है कि क्या LeaseSet और/या ElGamal/AES Session Tags को संदेश के साथ वितरित करना चाहिए। ये सेटिंग्स प्रोटोकॉल ओवरहेड की मात्रा और संदेश वितरण की विश्वसनीयता को महत्वपूर्ण रूप से प्रभावित करेंगी। व्यक्तिगत flag bits को रिलीज़ 0.9.2 के अनुसार निम्नलिखित रूप में परिभाषित किया गया है। परिभाषाएं परिवर्तन के अधीन हैं। flags बनाने के लिए SendMessageOptions क्लास का उपयोग करें।

बिट क्रम: 15...0

बिट्स 15-11

:   अप्रयुक्त, शून्य होना चाहिए

बिट्स 10-9

:   मैसेज विश्वसनीयता ओवरराइड (अनिम्प्लिमेंटेड, हटाया जाना है)।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
बिट 8

:   यदि 1 है, तो इस संदेश के साथ garlic में lease set को bundle न करें। यदि

    0, the router may bundle a lease set at its discretion.

बिट्स 7-4

:   निम्न टैग सीमा। यदि इससे कम टैग उपलब्ध हैं,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
बिट्स 3-0

:   यदि आवश्यक हो तो भेजे जाने वाले tags की संख्या। यह सलाहकारी है और यह नहीं

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### विवरण

क्लाइंट को उसके सेशन की स्थिति के बारे में निर्देश दें।

Router से Client को भेजा जाता है, [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), या [DestroySessionMessage](#DestroySessionMessage) के जवाब में। सभी मामलों में, [CreateSessionMessage](#CreateSessionMessage) के जवाब सहित, router को तुरंत जवाब देना चाहिए (tunnel बनने का इंतजार न करें)।

#### सामग्री

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) स्थिति

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### टिप्पणियाँ

स्टेटस मान ऊपर परिभाषित हैं। यदि स्टेटस Created है, तो Session ID वह पहचानकर्ता है जिसका उपयोग शेष सेशन के लिए किया जाना है।

### SetDateMessage {#SetDateMessage}

#### विवरण

वर्तमान दिनांक और समय। प्रारंभिक handshake के हिस्से के रूप में Router से Client को भेजा जाता है। रिलीज़ 0.9.20 के अनुसार, handshake के बाद किसी भी समय भी भेजा जा सकता है ताकि client को clock shift की सूचना दी जा सके।

#### विषय-सूची

1.  [Date](/docs/specs/common-structures/#date)
2.  I2CP API संस्करण [String](/docs/specs/common-structures/#string)

#### नोट्स

यह आमतौर पर router द्वारा भेजा गया पहला संदेश होता है। version string को release 0.8.7 के रूप में शामिल किया गया है। यह तभी उपयोगी है जब client और router एक ही JVM में नहीं हैं। यदि यह मौजूद नहीं है, तो router version 0.8.6 या उससे पुराना है।

समान JVM में clients को अतिरिक्त SetDate messages नहीं भेजे जाएंगे।

## संदर्भ

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP अवलोकन](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
