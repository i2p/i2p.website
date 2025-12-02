---
title: "एड्रेसबुक सब्सक्रिप्शन फीड कमांड्स"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "बंद"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
toc: true
---

## नोट

नेटवर्क deployment पूर्ण हो गया। आधिकारिक specification के लिए [SPEC](/docs/specs/subscription/) देखें।

## अवलोकन

यह प्रस्ताव address subscription feed को commands के साथ विस्तारित करने के बारे में है, ताकि name servers को hostname holders से entry updates broadcast करने में सक्षम बनाया जा सके। 0.9.26 में implemented किया गया।

## प्रेरणा

अभी के लिए, hosts.txt subscription servers केवल hosts.txt format में data भेजते हैं, जो निम्नलिखित है:

  ```text
  example.i2p=b64destination
  ```
इसके साथ कई समस्याएं हैं:

- Hostname धारक अपने hostnames के साथ जुड़े Destination को अपडेट नहीं कर सकते
  (उदाहरण के लिए signing key को अधिक मजबूत प्रकार में upgrade करने के लिए)।
- Hostname धारक अपने hostnames को मनमाने तरीके से छोड़ नहीं सकते; उन्हें संबंधित 
  Destination private keys को सीधे नए धारक को देना होगा।
- इस बात को प्रमाणित करने का कोई तरीका नहीं है कि subdomain संबंधित base hostname 
  द्वारा नियंत्रित है; वर्तमान में इसे केवल कुछ name servers द्वारा व्यक्तिगत रूप से 
  लागू किया जाता है।

## डिज़ाइन

यह प्रस्ताव hosts.txt format में कई command lines जोड़ता है। इन commands के साथ, name servers अपनी सेवाओं को विस्तृत करके कई अतिरिक्त features प्रदान कर सकते हैं। इस प्रस्ताव को implement करने वाले clients नियमित subscription प्रक्रिया के माध्यम से इन features को सुन सकेंगे।

सभी command lines को संबंधित Destination द्वारा हस्ताक्षरित होना चाहिए। यह सुनिश्चित करता है कि परिवर्तन केवल hostname धारक के अनुरोध पर ही किए जाएं।

## सुरक्षा निहितार्थ

इस प्रस्ताव का anonymity पर कोई प्रभाव नहीं है।

Destination key का नियंत्रण खोने से जुड़े जोखिम में वृद्धि होती है, क्योंकि कोई व्यक्ति जो इसे प्राप्त कर लेता है वह इन commands का उपयोग करके किसी भी संबंधित hostnames में परिवर्तन कर सकता है। लेकिन यह मौजूदा स्थिति से अधिक समस्या नहीं है, जहां कोई व्यक्ति जो Destination प्राप्त कर लेता है वह hostname का रूप धारण कर सकता है और (आंशिक रूप से) इसके traffic को अपने नियंत्रण में ले सकता है। बढ़े हुए जोखिम को hostname holders को यह क्षमता देकर संतुलित किया गया है कि वे hostname से जुड़े Destination को बदल सकें, यदि उन्हें लगता है कि Destination समझौता हो गया है; यह वर्तमान system के साथ असंभव है।

## विशिष्टता

### New line types

यह प्रस्ताव दो नए प्रकार की लाइनें जोड़ता है:

1. Add और Change कमांड्स:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```
2. कमांड हटाएं:

     ```text
     #!key1=val1#key2=val2 ...
     ```
#### Ordering

एक feed जरूरी नहीं कि क्रम में हो या पूरी हो। उदाहरण के लिए, एक change command किसी add command से पहले की लाइन पर हो सकती है, या add command के बिना हो सकती है।

Keys किसी भी क्रम में हो सकती हैं। Duplicate keys की अनुमति नहीं है। सभी keys और values case-sensitive हैं।

### Common keys

सभी commands में आवश्यक:

sig
  B64 signature, signing key का उपयोग करके destination से

दूसरे hostname और/या destination के संदर्भ:

oldname
  एक दूसरा hostname (नया या बदला हुआ)
olddest
  एक दूसरा b64 destination (नया या बदला हुआ)
oldsig
  एक दूसरा b64 signature, nolddest से signing key का उपयोग करके

अन्य सामान्य keys:

action
  एक command
name
  होस्टनेम, केवल तभी उपस्थित होता है जब example.i2p=b64dest से पहले न हो
dest
  b64 destination, केवल तभी उपस्थित होता है जब example.i2p=b64dest से पहले न हो
date
  epoch से सेकंड में
expires
  epoch से सेकंड में

### Commands

"Add" command को छोड़कर सभी commands में "action=command" key/value होना आवश्यक है।

पुराने clients के साथ compatibility के लिए, अधिकतर commands के पहले example.i2p=b64dest आता है, जैसा कि नीचे बताया गया है। बदलाव के लिए, ये हमेशा नए values होते हैं। कोई भी पुराने values key/value section में शामिल किए जाते हैं।

सूचीबद्ध keys आवश्यक हैं। सभी commands में अतिरिक्त key/value items हो सकते हैं जो यहाँ परिभाषित नहीं हैं।

#### Add hostname
Preceded by example.i2p=b64dest
  हाँ, यह नया host name और destination है।
action
  शामिल नहीं है, यह निहित है।
sig
  signature

उदाहरण:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```
#### Change hostname
example.i2p=b64dest से पूर्व
  हाँ, यह नया host name और पुराना destination है।
action
  changename
oldname
  पुराना hostname, जिसे बदला जाना है
sig
  signature

उदाहरण:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```
#### Change destination
इससे पहले example.i2p=b64dest
  हाँ, यह पुराना host name और नया destination है।
action
  changedest
olddest
  पुराना dest, जिसे बदला जाना है
oldsig
  olddest का उपयोग करके signature
sig
  signature

उदाहरण:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```
#### Add hostname alias
इससे पहले example.i2p=b64dest
  हाँ, यह नया (उपनाम) host नाम और पुराना destination है।
action
  addname
oldname
  पुराना hostname
sig
  signature

उदाहरण:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```
#### Add destination alias
(crypto upgrade के लिए उपयोग किया जाता है)

example.i2p=b64dest से पहले
  हाँ, यह पुराना host name और नया (वैकल्पिक) destination है।
action
  adddest
olddest
  पुराना dest
oldsig
  olddest का उपयोग करते हुए signature
sig
  dest का उपयोग करते हुए signature

उदाहरण:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```
#### Add subdomain
Preceded by subdomain.example.i2p=b64dest
  हाँ, यह नया host subdomain नाम और destination है।
action
  addsubdomain
oldname
  उच्च-स्तरीय hostname (example.i2p)
olddest
  उच्च-स्तरीय destination (example.i2p के लिए)
oldsig
  olddest का उपयोग करके signature
sig
  dest का उपयोग करके signature

उदाहरण:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```
#### क्रमांकन
example.i2p=b64dest से पूर्व
  हाँ, यह पुराना host name और destination है।
action
  update
sig
  signature

(यहाँ कोई भी अपडेटेड keys जोड़ें)

उदाहरण:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```
#### Remove hostname
example.i2p=b64dest से पहले
  नहीं, ये options action में निर्दिष्ट हैं
action
  remove
name
  hostname
dest
  destination
sig
  signature

उदाहरण:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```
#### Remove all with this destination
example.i2p=b64dest से पहले
  नहीं, ये options action में निर्दिष्ट हैं
action
  removeall
name
  पुराना hostname, केवल सलाहकारी
dest
  पुराना dest, इस dest वाले सभी हटा दिए जाते हैं
sig
  signature

उदाहरण:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```
### Signatures

सभी commands में एक signature key/value "sig=b64signature" होना चाहिए जहाँ signature अन्य data के लिए है, destination signing key का उपयोग करके।

पुराने और नए destination वाले commands के लिए, oldsig=b64signature भी होना चाहिए, और या तो oldname, olddest, या दोनों होना चाहिए।

Add या Change command में, verification के लिए public key उस Destination में होती है जिसे add या change किया जाना है।

कुछ add या edit commands में, एक अतिरिक्त destination का संदर्भ हो सकता है, उदाहरण के लिए जब एक alias जोड़ते समय, या किसी destination या host name को बदलते समय। उस स्थिति में, एक दूसरा signature शामिल होना चाहिए और दोनों को verify किया जाना चाहिए। दूसरा signature "inner" signature है और इसे पहले signed और verified किया जाता है ("outer" signature को छोड़कर)। client को changes को verify और accept करने के लिए आवश्यक कोई भी अतिरिक्त कार्रवाई करनी चाहिए।

oldsig हमेशा "inner" signature होता है। 'oldsig' या 'sig' keys के बिना sign और verify करें। sig हमेशा "outer" signature होता है। 'oldsig' key के साथ sign और verify करें लेकिन 'sig' key के बिना।

#### होस्टनाम जोड़ें

signature बनाने या verify करने के लिए byte stream generate करने हेतु, निम्नलिखित रूप में serialize करें:

- "sig" की को हटाएं
- यदि oldsig के साथ सत्यापित कर रहे हैं, तो "oldsig" की को भी हटाएं
- केवल Add या Change commands के लिए,
  example.i2p=b64dest आउटपुट करें
- यदि कोई keys शेष रहती हैं, तो "#!" आउटपुट करें
- UTF-8 key के अनुसार options को सॉर्ट करें, duplicate keys होने पर fail करें
- प्रत्येक key/value के लिए, key=value आउटपुट करें, उसके बाद (यदि अंतिम key/value नहीं है)
  एक '#'

नोट्स

- एक newline आउटपुट न करें
- आउटपुट एन्कोडिंग UTF-8 है
- सभी destination और signature एन्कोडिंग I2P alphabet का उपयोग करके Base 64 में है
- Keys और values case-sensitive हैं
- Host names lower-case में होना चाहिए

## Compatibility

hosts.txt फॉर्मेट में सभी नई लाइनें leading comment characters का उपयोग करके implemented की गई हैं, इसलिए I2P के सभी पुराने versions नए commands को comments के रूप में interpret करेंगे।

जब I2P router नई specification पर update होते हैं, तो वे पुराने comments की फिर से व्याख्या नहीं करेंगे, लेकिन अपनी subscription feeds के बाद के fetches में नए commands को सुनना शुरू कर देंगे। इसलिए name servers के लिए यह महत्वपूर्ण है कि वे command entries को किसी तरीके से persist करें, या etag support को enable करें ताकि router सभी पिछले commands को fetch कर सकें।

## References

* [SPEC](/docs/specs/subscription/)
