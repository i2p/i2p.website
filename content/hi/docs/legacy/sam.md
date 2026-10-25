---
title: "SAM V1 विनिर्देश"
description: "लेगेसी सिंपल एनॉनिमस मैसेजिंग प्रोटोकॉल संस्करण 1 (अप्रचलित)"
slug: "sam"
aliases:
  - "/hi/docs/api/sam"
  - "/hi/docs/api/sam/"
  - "/hi/sam"
  - "/hi/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## चेतावनी - पुराना - असमर्थित - [SAMv3](/docs/api/samv3) का उपयोग करें

नीचे I2P के साथ इंटरैक्ट करने के लिए एक सरल client protocol का version 1 निर्दिष्ट है। नए विकल्प: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob)।

## SAMv1 API के लिए भाषा लाइब्रेरी

- C
- C#
- Perl
- Python

लाइब्रेरीज़ I2P स्रोत रिपॉज़िटरी में हैं।

### I2P 0.9.14 परिवर्तन

रिपोर्ट किया गया version "1.0" ही रहता है।

- DEST GENERATE अब SIGNATURE_TYPE parameter का समर्थन करता है।
- HELLO VERSION में MIN parameter अब वैकल्पिक है।
- HELLO VERSION में MIN और MAX parameters अब single-digit versions जैसे "3" का समर्थन करते हैं।

## संस्करण 1 प्रोटोकॉल

क्लाइंट एप्लिकेशन SAM bridge से बात करता है, जो सभी I2P कार्यक्षमताओं को संभालता है (virtual streams के लिए streaming lib का उपयोग करके, या async messages के लिए सीधे I2CP का उपयोग करके)।

सभी client\<--\>SAM bridge संचार एक single TCP socket पर अनएन्क्रिप्टेड और अप्रमाणित होता है। SAM bridge तक पहुंच को firewalls या अन्य साधनों के माध्यम से सुरक्षित किया जाना चाहिए (संभवतः bridge में ACLs हो सकते हैं कि वह किन IPs से connections स्वीकार करता है)।

ये सभी SAM संदेश एक ही लाइन पर सादे ASCII में भेजे जाते हैं, जो newline character (\\n) से समाप्त होते हैं। नीचे दिखाया गया formatting केवल पठनीयता के लिए है, और जबकि प्रत्येक संदेश में पहले दो शब्दों का अपना विशिष्ट क्रम होना चाहिए, key=value pairs का क्रम बदला जा सकता है (जैसे "ONE TWO A=B C=D" या "ONE TWO C=D A=B" दोनों पूर्णतः वैध निर्माण हैं)। इसके अतिरिक्त, प्रोटोकॉल case-sensitive है।

SAM संदेश UTF-8 में व्याख्या किए जाते हैं। Key=value जोड़े एक single space से अलग होने चाहिए। Values को double quotes में enclosed किया जा सकता है यदि उनमें spaces हैं, जैसे key="long value text"। कोई escaping mechanism नहीं है।

संचार तीन अलग रूप ले सकता है:

- [Virtual streams](/docs/api/streaming)
- [Repliable datagrams](/docs/specs/datagrams#repliable) (FROM फील्ड के साथ संदेश)
- [Anonymous datagrams](/docs/specs/datagrams#raw) (कच्चे गुमनाम संदेश)

## SAM कनेक्शन हैंडशेक

SAM संचार तब तक नहीं हो सकता जब तक कि client और bridge किसी protocol version पर सहमत नहीं हो जाते, जो client द्वारा HELLO भेजने और bridge द्वारा HELLO REPLY भेजने से होता है:

```
HELLO VERSION MIN=$min MAX=$max
```
और

```
HELLO REPLY RESULT=$result VERSION=1.0
```
I2P 0.9.14 के अनुसार, MIN पैरामीटर वैकल्पिक है। MAX पैरामीटर प्रदान किया जाना चाहिए और version 1 का उपयोग करने के लिए "1" से अधिक या बराबर और "2" से कम होना चाहिए।

RESULT मान निम्नलिखित में से कोई एक हो सकता है:

- `OK`
- `NOVERSION`

## SAM सेशन

एक SAM सेशन तब बनाया जाता है जब एक क्लाइंट SAM bridge के लिए एक सॉकेट खोलता है, हैंडशेक संचालित करता है, और SESSION CREATE संदेश भेजता है, और सेशन तब समाप्त हो जाता है जब सॉकेट डिस्कनेक्ट हो जाता है।

प्रत्येक I2P Destination एक समय में केवल एक SAM session के लिए उपयोग किया जा सकता है, और केवल उन रूपों में से एक का उपयोग कर सकता है (अन्य रूपों के माध्यम से प्राप्त संदेश छोड़ दिए जाते हैं)।

bridge को client द्वारा भेजा गया SESSION CREATE message निम्नलिखित है:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION निर्दिष्ट करता है कि संदेश/स्ट्रीम भेजने और प्राप्त करने के लिए कौन सा destination उपयोग किया जाना चाहिए। यदि कोई $name दिया गया है, तो SAM bridge अपने स्थानीय storage (sam.keys फ़ाइल) में संबंधित destination (और निजी key) की खोज करता है। यदि उस नाम से मेल खाने वाला कोई संबंध मौजूद नहीं है, तो यह एक नया बनाता है। यदि destination को TRANSIENT के रूप में निर्दिष्ट किया गया है, तो यह हमेशा एक नया बनाता है।

ध्यान दें कि DESTINATION एक पहचानकर्ता है, *Base 64 encoded डेटा नहीं*। Destination को निर्दिष्ट करने के लिए, आपको [SAM V3](/docs/api/samv3) का उपयोग करना होगा।

DIRECTION केवल STREAM सेशन के लिए निर्दिष्ट किया जा सकता है, जो bridge को निर्देश देता है कि client या तो streams बना रहा होगा या प्राप्त कर रहा होगा, या दोनों। यदि यह निर्दिष्ट नहीं है, तो BOTH मान लिया जाएगा। DIRECTION=RECEIVE होने पर outbound stream बनाने का प्रयास त्रुटि का कारण बनना चाहिए, और DIRECTION=CREATE होने पर incoming streams को नजरअंदाज कर दिया जाएगा।

दिए गए अतिरिक्त विकल्पों को I2P session कॉन्फ़िगरेशन में फीड किया जाना चाहिए यदि वे SAM bridge द्वारा व्याख्यायित नहीं हैं (जैसे "tunnels.depthInbound=0")। इन विकल्पों का विवरण नीचे दिया गया है।

SAM bridge स्वयं पहले से ही कॉन्फ़िगर होना चाहिए कि उसे I2P के माध्यम से किस router के साथ संचार करना चाहिए (हालांकि यदि आवश्यक हो तो override प्रदान करने का एक तरीका हो सकता है, जैसे i2cp.tcp.host=localhost और i2cp.tcp.port=7654)।

session create message प्राप्त करने के बाद, SAM bridge एक session status message के साथ उत्तर देगा, जैसा कि निम्नलिखित है:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
RESULT का मान निम्नलिखित में से एक हो सकता है:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

यदि यह ठीक नहीं है, तो MESSAGE में मानव-पठनीय जानकारी होनी चाहिए कि session क्यों नहीं बनाया जा सका।

ध्यान दें कि यदि $name नहीं मिलता है और इसके बजाय एक transient destination बनाया जाता है तो कोई चेतावनी नहीं दी जाती है। ध्यान दें कि वास्तविक transient base 64 destination reply में output नहीं होता है; यह SESSION CREATE में दिया गया $name या TRANSIENT होता है। यदि आपको इन सुविधाओं की आवश्यकता है, तो आपको [SAM V3](/docs/api/samv3) का उपयोग करना होगा।

## SAM वर्चुअल स्ट्रीम

Virtual streams की विश्वसनीय और क्रमबद्ध डिलीवरी की गारंटी है, जैसे ही उपलब्ध हो failure और success की सूचना के साथ।

STYLE=STREAM के साथ session स्थापित करने के बाद, client और SAM bridge दोनों streams को प्रबंधित करने के लिए विभिन्न messages को असिंक्रोनस रूप से आगे-पीछे भेज सकते हैं, जैसा कि नीचे सूचीबद्ध है:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
यह स्थानीय destination से निर्दिष्ट peer तक एक नया virtual connection स्थापित करता है, इसे session-scoped unique ID के साथ चिह्नित करता है। unique ID एक ASCII base 10 integer है जो 1 से (2^31-1) तक होता है।

$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

SAM bridge को इसके जवाब में एक stream status message भेजना चाहिए:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT का मान निम्नलिखित में से एक हो सकता है:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

यदि RESULT OK है, तो निर्दिष्ट destination उपलब्ध है और उसने कनेक्शन को अधिकृत किया है; यदि कनेक्शन संभव नहीं था (timeout, आदि), तो RESULT में उपयुक्त error value होगी (एक वैकल्पिक human-readable MESSAGE के साथ)।

प्राप्त करने वाले छोर पर, SAM bridge केवल client को निम्नलिखित रूप में सूचित करता है:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
यह client को बताता है कि दिया गया destination उनके साथ एक virtual connection बनाया है। निम्नलिखित data stream को दिए गए unique ID के साथ चिह्नित किया जाएगा, जो कि -1 से -(2^31-1) तक का एक ASCII base 10 integer है।

$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) है।

जब client virtual connection पर data भेजना चाहता है, तो वे इसे निम्न प्रकार से करते हैं:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
यह निर्दिष्ट डेटा को उस buffer में जोड़ता है जो virtual connection के माध्यम से peer को भेजा जा रहा है। send size $numBytes बताता है कि newline के बाद कितने 8bit bytes शामिल हैं, जो 1 से 32768 (32KB) तक हो सकते हैं।

SAM bridge तब संदेश को यथासंभव तेज़ी से और कुशलता से वितरित करने का सर्वोत्तम प्रयास करेगा, संभवतः कई SEND संदेशों को एक साथ buffer करके। यदि डेटा वितरित करने में कोई त्रुटि होती है, या यदि दूरस्थ पक्ष कनेक्शन बंद कर देता है, तो SAM bridge क्लाइंट को बताएगा:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT मान निम्नलिखित में से कोई एक हो सकता है:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

यदि कनेक्शन को दूसरे peer द्वारा सही तरीके से बंद कर दिया गया है, तो $result को OK पर सेट किया जाता है। यदि $result OK नहीं है, तो MESSAGE एक वर्णनात्मक संदेश प्रदान कर सकता है, जैसे "peer unreachable", आदि। जब भी कोई client कनेक्शन बंद करना चाहता है, तो वे SAM bridge को close message भेजते हैं:

```
STREAM CLOSE
       ID=$id
```
bridge तब उसकी आवश्यक सफाई करता है और उस ID को छोड़ देता है - इस पर कोई और संदेश भेजा या प्राप्त नहीं किया जा सकता।

संचार के दूसरी तरफ के लिए, जब भी peer ने कुछ डेटा भेजा हो और वह client के लिए उपलब्ध हो, तो SAM bridge तुरंत इसे पहुंचा देगा:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
सभी streams स्वतः ही बंद हो जाते हैं जब SAM bridge और client के बीच का connection टूट जाता है।

## SAM Repliable Datagrams

जबकि I2P में स्वाभाविक रूप से FROM address नहीं होता है, उपयोग में आसानी के लिए एक अतिरिक्त परत repliable datagrams के रूप में प्रदान की गई है - यह 31744 bytes तक के अव्यवस्थित और अविश्वसनीय संदेश हैं जिनमें FROM address शामिल होता है (header material के लिए 1KB तक छोड़कर)। यह FROM address SAM द्वारा आंतरिक रूप से प्रमाणीकृत किया जाता है (स्रोत को सत्यापित करने के लिए destination की signing key का उपयोग करते हुए) और इसमें replay prevention शामिल है।

न्यूनतम आकार 1 है। सर्वोत्तम डिलीवरी विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है।

STYLE=DATAGRAM के साथ SAM session स्थापित करने के बाद, client SAM bridge को भेज सकता है:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
जब एक datagram आता है, तो bridge इसे client को इसके माध्यम से पहुंचाता है:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

SAM bridge कभी भी client को authentication headers या अन्य fields को expose नहीं करता, केवल वह data जो sender ने प्रदान किया था। यह तब तक जारी रहता है जब तक session बंद नहीं हो जाता (client द्वारा connection drop करने से)।

## SAM Anonymous Datagrams

I2P की bandwidth का अधिकतम उपयोग करते हुए, SAM clients को anonymous datagrams भेजने और प्राप्त करने की अनुमति देता है, authentication और reply की जानकारी client पर ही छोड़ते हुए। ये datagrams अविश्वसनीय और अव्यवस्थित होते हैं, और 32768 bytes तक हो सकते हैं।

न्यूनतम आकार 1 है। सर्वोत्तम वितरण विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है।

STYLE=RAW के साथ SAM session स्थापित करने के बाद, client SAM bridge को भेज सकता है:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

जब एक कच्चा datagram आता है, तो bridge इसे client को इसके माध्यम से भेजता है:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM उपयोगिता कार्यक्षमता

निम्नलिखित संदेश का उपयोग client द्वारा SAM bridge से name resolution के लिए query करने के लिए किया जा सकता है:

```
NAMING LOOKUP
       NAME=$name
```
जिसका उत्तर दिया जाता है

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
RESULT मान निम्नलिखित में से कोई एक हो सकता है:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

यदि NAME=ME है, तो उत्तर में वर्तमान सेशन द्वारा उपयोग किया गया destination शामिल होगा (यह उपयोगी है यदि आप एक TRANSIENT का उपयोग कर रहे हैं)। यदि $result OK नहीं है, तो MESSAGE एक वर्णनात्मक संदेश दे सकता है, जैसे "bad format", आदि।

$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

निम्नलिखित संदेश का उपयोग करके पब्लिक और प्राइवेट base64 keys उत्पन्न की जा सकती हैं:

```
DEST GENERATE
```
जिसका उत्तर दिया जाता है

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
I2P 0.9.14 से, एक वैकल्पिक पैरामीटर SIGNATURE_TYPE समर्थित है। SIGNATURE_TYPE मान कोई भी नाम (जैसे ECDSA_SHA256_P256, केस इनसेंसिटिव) या नंबर (जैसे 1) हो सकता है जो [Key Certificates](/docs/specs/common-structures#type_Certificate) द्वारा समर्थित है। डिफ़ॉल्ट DSA_SHA1 है।

$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

$privkey, [Destination](/docs/specs/common-structures#type_Destination) के बाद [Private Key](/docs/specs/common-structures#type_PrivateKey) और फिर [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) के संयोजन का base 64 है, जो signature type के आधार पर 884 या अधिक base 64 characters (binary में 663 या अधिक bytes) होता है।

## RESULT मान

ये वे मान हैं जो RESULT फील्ड द्वारा ले जाए जा सकते हैं, उनके अर्थ के साथ:

| Value | Meaning |
|-------|---------|
| `OK` | ऑपरेशन सफलतापूर्वक पूरा हुआ |
| `CANT_REACH_PEER` | peer मौजूद है, लेकिन पहुंचा नहीं जा सकता |
| `DUPLICATED_DEST` | निर्दिष्ट Destination पहले से उपयोग में है |
| `I2P_ERROR` | एक सामान्य I2P त्रुटि (जैसे I2CP डिस्कनेक्शन, आदि) |
| `INVALID_KEY` | निर्दिष्ट key वैध नहीं है (गलत प्रारूप, आदि) |
| `KEY_NOT_FOUND` | नामकरण प्रणाली दिए गए नाम को हल नहीं कर सकती |
| `PEER_NOT_FOUND` | peer नेटवर्क पर नहीं मिल सकता |
| `TIMEOUT` | किसी घटना की प्रतीक्षा में समय समाप्त (जैसे peer का उत्तर) |
## Tunnel, I2CP, और Streaming विकल्प

ये विकल्प SAM SESSION CREATE लाइन के अंत में name=value जोड़ों के रूप में पास किए जा सकते हैं।

सभी sessions में [I2CP options जैसे tunnel lengths](/docs/protocol/i2cp#options) शामिल हो सकते हैं। STREAM sessions में [Streaming lib options](/docs/api/streaming#options) शामिल हो सकते हैं। option names और defaults के लिए उन references को देखें।

## Base 64 नोट्स

Base 64 encoding में I2P मानक Base 64 वर्णमाला "A-Z, a-z, 0-9, -, ~" का उपयोग करना चाहिए।

## क्लाइंट लाइब्रेरी कार्यान्वयन

C, C++, C#, Perl, और Python के लिए client libraries उपलब्ध हैं। ये I2P Source Package में apps/sam/ directory में स्थित हैं।

## डिफ़ॉल्ट SAM सेटअप

डिफ़ॉल्ट SAM पोर्ट 7656 है। SAM I2P Router में डिफ़ॉल्ट रूप से सक्षम नहीं है; इसे मैन्युअल रूप से शुरू करना होगा, या router console में configure clients पेज पर या clients.config फ़ाइल में स्वचालित रूप से शुरू होने के लिए कॉन्फ़िगर करना होगा।
