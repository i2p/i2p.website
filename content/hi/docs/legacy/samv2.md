---
title: "SAM V2 विशिष्टता"
description: "लेगेसी सिंपल एनॉनिमस मैसेजिंग प्रोटोकॉल संस्करण 2 (अप्रचलित)"
slug: "samv2"
aliases:
  - "/hi/docs/api/samv2"
  - "/hi/docs/api/samv2/"
  - "/hi/samv2"
  - "/hi/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## चेतावनी - बहिष्कृत - असमर्थित - [SAMv3](/docs/api/samv3) का उपयोग करें

नीचे I2P के साथ इंटरैक्ट करने के लिए एक सरल client protocol का version 2 निर्दिष्ट है।

SAM V2 को I2P रिलीज़ 0.6.1.31 में पेश किया गया था। SAM V1 से महत्वपूर्ण अंतर "\*\*\*" से चिह्नित हैं। विकल्प: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob)।

## संस्करण 2 में परिवर्तन

SAM V2 को I2P रिलीज 0.6.1.31 में पेश किया गया था। संस्करण 1 की तुलना में, SAM v2 एक ही I2P destination पर कई sockets को *समानांतर में* प्रबंधित करने का तरीका प्रदान करता है, यानी client को दूसरे socket पर डेटा भेजने से पहले एक socket पर डेटा सफलतापूर्वक भेजे जाने का इंतजार नहीं करना पड़ता। सभी डेटा एक ही client\<--\>SAM socket के माध्यम से ट्रांजिट होता है। कई sockets के लिए, [SAM V3](/docs/api/samv3) देखें।

### I2P 0.9.14 परिवर्तन

रिपोर्ट किया गया संस्करण "2.0" ही बना रहता है।

- DEST GENERATE अब SIGNATURE_TYPE पैरामीटर का समर्थन करता है।
- HELLO VERSION में MIN पैरामीटर अब वैकल्पिक है।
- HELLO VERSION में MIN और MAX पैरामीटर अब एकल-अंक संस्करण जैसे "3" का समर्थन करते हैं।

## संस्करण 2 प्रोटोकॉल

क्लाइंट एप्लिकेशन SAM bridge से बात करती है, जो सभी I2P कार्यक्षमता को संभालता है (virtual streams के लिए streaming lib का उपयोग करके, या async messages के लिए सीधे I2CP का उपयोग करके)।

सभी client\<--\>SAM bridge संचार एकल TCP socket पर अनएन्क्रिप्टेड और अप्रमाणित है। SAM bridge तक पहुंच को फ़ायरवॉल या अन्य माध्यमों से सुरक्षित किया जाना चाहिए (संभवतः bridge में ACL हो सकते हैं कि वह किन IP से कनेक्शन स्वीकार करता है)।

ये सभी SAM संदेश एक ही लाइन पर सादे ASCII में भेजे जाते हैं, जो newline character (\\n) से समाप्त होते हैं। नीचे दिखाया गया formatting केवल पठनीयता के लिए है, और जबकि प्रत्येक संदेश के पहले दो शब्द अपने विशिष्ट क्रम में रहने चाहिए, key=value जोड़ों का क्रम बदला जा सकता है (उदाहरण के लिए "ONE TWO A=B C=D" या "ONE TWO C=D A=B" दोनों पूर्णतः वैध निर्माण हैं)। इसके अलावा, यह protocol case-sensitive है।

SAM संदेश UTF-8 में व्याख्या किए जाते हैं। Key=value जोड़ों को एक स्थान से अलग किया जाना चाहिए। यदि values में स्थान हैं तो उन्हें double quotes में बंद किया जा सकता है, जैसे key="long value text"। कोई escaping तंत्र नहीं है।

संचार तीन अलग रूप ले सकता है:

- [Virtual streams](/docs/api/streaming)
- [Repliable datagrams](/docs/specs/datagrams#repliable) (FROM फील्ड वाले संदेश)
- [Anonymous datagrams](/docs/specs/datagrams#raw) (कच्चे गुमनाम संदेश)

## SAM Connection Handshake

SAM संचार तब तक नहीं हो सकता जब तक कि client और bridge प्रोटोकॉल संस्करण पर सहमत नहीं हो जाते, जो client द्वारा HELLO भेजने और bridge द्वारा HELLO REPLY भेजने से होता है:

```
HELLO VERSION MIN=$min MAX=$max
```
और

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
I2P 0.9.14 के अनुसार, MIN पैरामीटर वैकल्पिक है। MAX पैरामीटर अवश्य प्रदान किया जाना चाहिए और version 2 का उपयोग करने के लिए "2" से अधिक या बराबर तथा "3" से कम होना चाहिए।

RESULT मान निम्नलिखित में से कोई एक हो सकता है:

- `OK`
- `NOVERSION`

## SAM सेशन

एक SAM सेशन तब बनाया जाता है जब कोई client SAM bridge के लिए एक socket खोलता है, handshake संचालित करता है, और SESSION CREATE संदेश भेजता है, और यह सेशन तब समाप्त हो जाता है जब socket डिस्कनेक्ट हो जाता है।

प्रत्येक I2P Destination एक समय में केवल एक SAM session के लिए उपयोग किया जा सकता है, और केवल उन रूपों में से एक का उपयोग कर सकता है (अन्य रूपों के माध्यम से प्राप्त संदेश छोड़ दिए जाते हैं)।

क्लाइंट द्वारा bridge को भेजा गया SESSION CREATE संदेश निम्नलिखित है:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION निर्दिष्ट करता है कि संदेश/स्ट्रीम भेजने और प्राप्त करने के लिए कौन सा destination उपयोग करना चाहिए। यदि $name दिया गया है, तो SAM bridge अपने स्थानीय भंडारण (sam.keys फ़ाइल) में संबंधित destination (और निजी कुंजी) की खोज करता है। यदि उस नाम से मेल खाता कोई संबंध मौजूद नहीं है, तो यह एक नया बनाता है। यदि destination को TRANSIENT के रूप में निर्दिष्ट किया गया है, तो यह हमेशा एक नया बनाता है।

ध्यान दें कि DESTINATION एक पहचानकर्ता है, *Base 64 encoded डेटा नहीं*। Destination को निर्दिष्ट करने के लिए, आपको [SAM V3](/docs/api/samv3) का उपयोग करना होगा।

DIRECTION केवल STREAM sessions के लिए निर्दिष्ट किया जा सकता है, जो bridge को निर्देश देता है कि client या तो streams बना रहा होगा या प्राप्त कर रहा होगा, या दोनों। यदि यह निर्दिष्ट नहीं है, तो BOTH मान लिया जाएगा। DIRECTION=RECEIVE के दौरान एक outbound stream बनाने का प्रयास करने पर त्रुटि होनी चाहिए, और DIRECTION=CREATE के दौरान incoming streams को अनदेखा किया जाएगा।

दिए गए अतिरिक्त विकल्पों को I2P session configuration में भेजा जाना चाहिए यदि वे SAM bridge द्वारा व्याख्यायित नहीं किए जाते हैं (जैसे "tunnels.depthInbound=0")। इन विकल्पों का विवरण नीचे दिया गया है।

SAM bridge स्वयं पहले से ही इस बात के साथ कॉन्फ़िगर होना चाहिए कि उसे I2P के माध्यम से किस router के साथ संचार करना चाहिए (हालांकि यदि आवश्यक हो तो override प्रदान करने का कोई तरीका हो सकता है, जैसे i2cp.tcp.host=localhost और i2cp.tcp.port=7654)।

session create message प्राप्त करने के बाद, SAM bridge एक session status message के साथ उत्तर देगा, जो निम्नलिखित है:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
RESULT का मान निम्न में से कोई एक हो सकता है:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

यदि यह ठीक नहीं है, तो MESSAGE में मानव-पठनीय जानकारी होनी चाहिए कि session क्यों नहीं बनाया जा सका।

ध्यान दें कि यदि $name नहीं मिलता है और इसके बजाय एक अस्थायी destination बनाया जाता है तो कोई चेतावनी नहीं दी जाती है। ध्यान दें कि वास्तविक अस्थायी base 64 destination reply में output नहीं होता है; यह SESSION CREATE में दिया गया $name या TRANSIENT होता है। यदि आपको इन सुविधाओं की आवश्यकता है, तो आपको [SAM V3](/docs/api/samv3) का उपयोग करना होगा।

## SAM वर्चुअल स्ट्रीम्स

Virtual streams की गारंटी है कि वे विश्वसनीय रूप से और क्रम में भेजे जाएंगे, जैसे ही उपलब्ध हो तो असफलता और सफलता की अधिसूचना के साथ।

STYLE=STREAM के साथ सत्र स्थापित करने के बाद, क्लाइंट और SAM bridge दोनों streams के प्रबंधन के लिए विभिन्न संदेशों को असिंक्रोनस रूप से आगे-पीछे भेज सकते हैं, जैसा कि नीचे सूचीबद्ध है:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
यह स्थानीय गंतव्य से निर्दिष्ट peer के लिए एक नया virtual connection स्थापित करता है, इसे session-scoped unique ID के साथ चिह्नित करता है। unique ID एक ASCII base 10 integer है जो 1 से (2^31-1) तक होता है।

$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

SAM bridge इसका उत्तर एक stream status संदेश के साथ देता है:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT मान निम्नलिखित में से एक हो सकता है:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

यदि RESULT OK है, तो निर्दिष्ट destination उपलब्ध है और कनेक्शन को अधिकृत किया गया है; यदि कनेक्शन संभव नहीं था (timeout, आदि), तो RESULT में उपयुक्त error value होगा (एक वैकल्पिक human-readable MESSAGE के साथ)।

प्राप्त करने वाले छोर पर, SAM bridge केवल client को निम्नलिखित तरीके से सूचित करता है:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
यह client को बताता है कि दिया गया destination उनके साथ एक virtual connection बनाया है। निम्नलिखित data stream को दिए गए unique ID के साथ चिह्नित किया जाएगा, जो कि -1 से -(2^31-1) तक का ASCII base 10 integer है।

$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

जब क्लाइंट वर्चुअल कनेक्शन पर डेटा भेजना चाहता है, तो वे इसे निम्नलिखित तरीके से करते हैं:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
यह SAM bridge से कहता है कि निर्दिष्ट डेटा को उस buffer में जोड़े जो virtual connection के माध्यम से peer को भेजा जा रहा है। send size $numBytes यह बताता है कि newline के बाद कितने 8bit bytes शामिल हैं, जो 1 से 32768 (32KB) तक हो सकते हैं।

**\*\*\* SAM bridge तुरंत उत्तर देता है:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** जहाँ $bufferState हो सकता है:

- `BUFFER_FULL` - SAM का buffer में भेजने के लिए 32 या अधिक KB डेटा है, और बाद के SEND requests असफल हो जाएंगे
- `READY` - SAM का buffer भरा नहीं है, और अगला SEND request सफल होने की गारंटी है

**\*\*\*** और $result इनमें से एक है:

- `OK` - डेटा सफलतापूर्वक buffer किया गया है
- `FAILED` - buffer भरा हुआ था, कोई डेटा buffer नहीं किया गया

**\*\*\*** यदि SAM bridge ने BUFFER_FULL के साथ उत्तर दिया है, तो यह अपना buffer फिर से उपलब्ध होते ही दूसरा संदेश भेजेगा:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** जब परिणाम OK होता है, तो SAM bridge फिर संदेश को यथासंभव तेज़ी से और कुशलता से पहुंचाने का भरसक प्रयास करेगा, संभवतः कई SEND संदेशों को एक साथ buffer करके। यदि डेटा पहुंचाने में कोई त्रुटि होती है, या यदि remote side कनेक्शन बंद कर देता है, तो SAM bridge client को बताएगा:

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

यदि connection को दूसरे peer द्वारा सही तरीके से बंद कर दिया गया है, तो $result को OK पर सेट किया जाता है। यदि $result OK नहीं है, तो MESSAGE एक वर्णनात्मक संदेश दे सकता है, जैसे "peer unreachable", आदि। जब भी कोई client connection बंद करना चाहता है, वे SAM bridge को close message भेजते हैं:

```
STREAM CLOSE
       ID=$id
```
bridge तब अपने आवश्यक कार्यों की सफाई करता है और उस ID को त्याग देता है - इस पर कोई और संदेश भेजे या प्राप्त नहीं किए जा सकते।

संचार के दूसरी तरफ के लिए, जब भी peer ने कुछ डेटा भेजा हो और वह client के लिए उपलब्ध हो, SAM bridge तुरंत इसे पहुंचा देगा:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** SAM version 2.0 के साथ, हालांकि, client को पहले SAM bridge को बताना होता है कि पूरे session के लिए कितना incoming data की अनुमति है, एक message भेजकर:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** जहाँ $limit हो सकती है:

- `NONE` - SAM bridge सुनना जारी रखेगा और आने वाले data को deliver करेगा (version 1.0 के समान व्यवहार)
- एक integer (2^64 से कम) - प्राप्त bytes की संख्या जिसके बाद SAM bridge incoming stream पर सुनना बंद कर देगा। जब भी client stream से अधिक bytes स्वीकार करने के लिए तैयार हो, उसे फिर से ऐसा message भेजना होगा, अधिक $limit के साथ।

**\*\*\*** क्लाइंट को ऐसे STREAM RECEIVE संदेश तभी भेजने होंगे जब peer के साथ कनेक्शन स्थापित हो चुका हो, यानी जब क्लाइंट को SAM bridge से "STREAM CONNECTED" या "STREAM STATUS RESULT=OK" प्राप्त हो चुका हो।

SAM bridge और client के बीच connection टूटने पर सभी streams स्वचालित रूप से बंद हो जाते हैं।

## SAM Repliable Datagrams

जबकि I2P में मूल रूप से FROM address नहीं होता, उपयोग में आसानी के लिए एक अतिरिक्त परत repliable datagrams के रूप में प्रदान की जाती है - 31744 bytes तक के अव्यवस्थित और अविश्वसनीय संदेश जिनमें FROM address शामिल होता है (header सामग्री के लिए 1KB तक छोड़कर)। यह FROM address SAM द्वारा आंतरिक रूप से प्रमाणित किया जाता है (स्रोत को सत्यापित करने के लिए destination की signing key का उपयोग करके) और इसमें replay prevention शामिल है।

न्यूनतम आकार 1 है। सर्वोत्तम डिलीवरी विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है।

SAM session को STYLE=DATAGRAM के साथ स्थापित करने के बाद, client SAM bridge को भेज सकता है:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
जब एक datagram आता है, तो bridge इसे client तक पहुंचाता है:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

SAM bridge कभी भी client को authentication headers या अन्य fields को expose नहीं करता, केवल वह data जो sender ने प्रदान किया था। यह तब तक जारी रहता है जब तक session बंद नहीं हो जाता (client द्वारा connection drop करने पर)।

## SAM अनाम डेटाग्राम

I2P की bandwidth का अधिकतम उपयोग करते हुए, SAM clients को anonymous datagrams भेजने और प्राप्त करने की अनुमति देता है, authentication और reply की जानकारी client पर ही छोड़ देता है। ये datagrams अविश्वसनीय और अव्यवस्थित होते हैं, और 32768 bytes तक हो सकते हैं।

न्यूनतम आकार 1 है। सर्वोत्तम डिलीवरी विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है।

STYLE=RAW के साथ SAM सेशन स्थापित करने के बाद, क्लाइंट SAM bridge को भेज सकता है:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination, [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

जब एक raw datagram आता है, तो bridge इसे client तक पहुंचाता है के माध्यम से:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM उपयोगिता कार्यक्षमता

निम्नलिखित संदेश का उपयोग क्लाइंट द्वारा SAM bridge से नाम रिज़ॉल्यूशन के लिए क्वेरी करने के लिए किया जा सकता है:

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

यदि NAME=ME है, तो reply में current session द्वारा उपयोग किया गया destination होगा (उपयोगी है यदि आप TRANSIENT का उपयोग कर रहे हैं)। यदि $result OK नहीं है, तो MESSAGE एक वर्णनात्मक संदेश दे सकता है, जैसे "bad format", आदि।

$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) है।

निम्नलिखित संदेश का उपयोग करके पब्लिक और प्राइवेट base64 keys जेनरेट की जा सकती हैं:

```
DEST GENERATE
```
जिसका उत्तर दिया जाता है

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
I2P 0.9.14 से, एक वैकल्पिक पैरामीटर SIGNATURE_TYPE समर्थित है। SIGNATURE_TYPE मान कोई भी नाम (जैसे ECDSA_SHA256_P256, case insensitive) या संख्या (जैसे 1) हो सकता है जो [Key Certificates](/docs/specs/common-structures#type_Certificate) द्वारा समर्थित है। डिफ़ॉल्ट DSA_SHA1 है।

$destination [Destination](/docs/specs/common-structures#type_Destination) का base 64 है, जो signature type के आधार पर 516 या अधिक base 64 characters (binary में 387 या अधिक bytes) होता है।

$privkey [Destination](/docs/specs/common-structures#type_Destination) के बाद [Private Key](/docs/specs/common-structures#type_PrivateKey) के बाद [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) के संयोजन का base 64 है, जो signature type के आधार पर 884 या अधिक base 64 characters (binary में 663 या अधिक bytes) होता है।

## RESULT मान

ये वे मान हैं जो RESULT फील्ड द्वारा ले जाए जा सकते हैं, उनके अर्थ के साथ:

| Value | Meaning |
|-------|---------|
| `OK` | ऑपरेशन सफलतापूर्वक पूरा हुआ |
| `CANT_REACH_PEER` | peer मौजूद है, लेकिन पहुँचा नहीं जा सकता |
| `DUPLICATED_DEST` | निर्दिष्ट Destination पहले से उपयोग में है |
| `I2P_ERROR` | एक सामान्य I2P त्रुटि (जैसे I2CP डिस्कनेक्शन, आदि) |
| `INVALID_KEY` | निर्दिष्ट key मान्य नहीं है (गलत फॉर्मेट, आदि) |
| `KEY_NOT_FOUND` | नेमिंग सिस्टम दिए गए नाम को हल नहीं कर सकता |
| `PEER_NOT_FOUND` | peer नेटवर्क पर नहीं मिला |
| `TIMEOUT` | किसी इवेंट की प्रतीक्षा में समय सीमा समाप्त (जैसे peer का जवाब) |
## Tunnel, I2CP, और Streaming विकल्प

ये विकल्प SAM SESSION CREATE लाइन के अंत में name=value जोड़ों के रूप में पास किए जा सकते हैं।

सभी sessions में [I2CP विकल्प जैसे tunnel lengths](/docs/protocol/i2cp#options) शामिल हो सकते हैं। STREAM sessions में [Streaming lib विकल्प](/docs/api/streaming#options) शामिल हो सकते हैं। विकल्प नामों और defaults के लिए उन संदर्भों को देखें।

## Base 64 नोट्स

Base 64 encoding में I2P मानक Base 64 वर्णमाला "A-Z, a-z, 0-9, -, ~" का उपयोग करना चाहिए।

## क्लाइंट लाइब्रेरी इम्प्लीमेंटेशन

Client libraries C, C++, C#, Perl, और Python के लिए उपलब्ध हैं। ये I2P Source Package में apps/sam/ directory में हैं। कुछ पुराने हो सकते हैं और SAMv2 support के लिए अपडेट नहीं किए गए होंगे।

## डिफ़ॉल्ट SAM सेटअप

डिफ़ॉल्ट SAM पोर्ट 7656 है। SAM I2P Router में डिफ़ॉल्ट रूप से सक्षम नहीं है; इसे मैन्युअल रूप से शुरू करना होगा, या router console में configure clients पेज पर, या clients.config फाइल में स्वचालित रूप से शुरू होने के लिए कॉन्फ़िगर करना होगा।
