---
title: "पता पुस्तिका सब्स्क्रिप्शन फ़ीड कमांड"
description: "hostname धारकों से entry अपडेट प्रसारित करने के लिए name servers को सक्षम बनाने हेतु commands के साथ address subscription feed को विस्तारित करने का विनिर्देश।"
slug: "subscription"
aliases:
  - "/hi/docs/specs/subscription-spec"
  - "/hi/docs/specs/subscription-spec/"
category: "प्रारूप"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## अवलोकन

यह विनिर्देश address subscription feed को commands के साथ विस्तारित करता है, ताकि name servers को hostname holders से entry updates को broadcast करने में सक्षम बनाया जा सके। 0.9.26 में implemented किया गया, मूल रूप से proposal 112 में प्रस्तावित।

## प्रेरणा

पहले, hosts.txt subscription servers केवल hosts.txt फॉर्मेट में डेटा भेजते थे, जो इस प्रकार है:

```
example.i2p=b64destination
```
इसमें कई समस्याएं हैं:

- Hostname धारक अपने hostnames के साथ जुड़े Destination को अपडेट नहीं कर सकते (जैसे कि signing key को एक मजबूत प्रकार में अपग्रेड करने के लिए)।
- Hostname धारक अपने hostnames को मनमाने तरीके से छोड़ नहीं सकते; उन्हें संबंधित Destination private keys सीधे नए धारक को देनी होंगी।
- यह प्रमाणित करने का कोई तरीका नहीं है कि एक subdomain संबंधित base hostname द्वारा नियंत्रित है; यह वर्तमान में केवल कुछ name servers द्वारा व्यक्तिगत रूप से लागू किया जाता है।

## डिज़ाइन

यह विनिर्देश hosts.txt प्रारूप में कई command lines जोड़ता है। इन commands के साथ, name servers अपनी सेवाओं का विस्तार करके कई अतिरिक्त सुविधाएं प्रदान कर सकते हैं। इस विनिर्देश को लागू करने वाले clients नियमित subscription प्रक्रिया के माध्यम से इन सुविधाओं को सुन सकेंगे।

सभी command lines को संबंधित Destination द्वारा signed होना चाहिए। इससे यह सुनिश्चित होता है कि परिवर्तन केवल hostname धारक के अनुरोध पर ही किए जाएं।

## सुरक्षा निहितार्थ

यह विनिर्देश गुमनामी को प्रभावित नहीं करता है।

Destination key का नियंत्रण खोने से जुड़े जोखिम में वृद्धि होती है, क्योंकि कोई भी व्यक्ति जो इसे प्राप्त कर लेता है वह इन commands का उपयोग करके किसी भी संबंधित hostname में परिवर्तन कर सकता है। लेकिन यह वर्तमान स्थिति से अधिक समस्याजनक नहीं है, जहां कोई व्यक्ति जो Destination प्राप्त कर लेता है वह hostname का impersonate कर सकता है और (आंशिक रूप से) इसके traffic को अपने नियंत्रण में ले सकता है। बढ़े हुए जोखिम को hostname धारकों को यह क्षमता देकर संतुलित किया जाता है कि वे hostname से जुड़े Destination को बदल सकें, यदि उन्हें लगता है कि Destination से छेड़छाड़ हुई है; वर्तमान system के साथ यह असंभव है।

## विनिर्देश

### नई लाइन प्रकार

दो नए प्रकार की लाइनें हैं:

1. Add और Change commands:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. कमांड हटाएं:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### क्रमबद्धता

एक feed जरूरी नहीं कि क्रम में या पूर्ण हो। उदाहरण के लिए, एक change command किसी add command से पहले की लाइन में हो सकती है, या add command के बिना भी हो सकती है।

Keys किसी भी क्रम में हो सकती हैं। डुप्लिकेट keys की अनुमति नहीं है। सभी keys और values case-sensitive हैं।

### सामान्य कुंजियाँ

सभी commands में आवश्यक:

**sig** : B64 signature, गंतव्य से signing key का उपयोग करके

दूसरे hostname और/या destination के संदर्भ:

**oldname** : एक दूसरा hostname (नया या बदला हुआ)

**olddest** : एक दूसरा b64 destination (नया या परिवर्तित)

**oldsig** : एक दूसरा b64 signature, olddest से signing key का उपयोग करते हुए

अन्य सामान्य keys:

**action** : एक कमांड

**name** : होस्टनेम, केवल तभी मौजूद होता है जब इससे पहले `example.i2p=b64dest` न हो

**dest** : b64 destination, केवल तभी मौजूद होता है जब इसके पहले `example.i2p=b64dest` न हो

**date** : epoch से सेकंड में

**expires** : epoch के बाद से सेकंड में

### कमांड्स

"Add" कमांड को छोड़कर सभी कमांड में `action=command` key/value होना आवश्यक है।

पुराने clients के साथ compatibility के लिए, अधिकांश commands से पहले `example.i2p=b64dest` लगाया जाता है, जैसा कि नीचे बताया गया है। परिवर्तनों के लिए, ये हमेशा नए values होते हैं। कोई भी पुराने values key/value section में शामिल किए जाते हैं।

सूचीबद्ध keys आवश्यक हैं। सभी commands में यहाँ परिभाषित न की गई अतिरिक्त key/value items हो सकती हैं।

#### Hostname जोड़ें

**example.i2p=b64dest द्वारा पूर्ववर्ती** : हाँ, यह नया host name और destination है।

**action** : शामिल नहीं है, यह निहित है।

**sig** : हस्ताक्षर

उदाहरण:

```
example.i2p=b64dest#!sig=b64sig
```
#### होस्टनाम बदलें

**example.i2p=b64dest द्वारा पूर्व में** : हाँ, यह नया होस्ट नाम और पुराना destination है।

**action** : changename

**oldname** : पुराना होस्टनेम, जिसे बदला जाना है

**sig** : हस्ताक्षर

उदाहरण:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### गंतव्य बदलें

**example.i2p=b64dest द्वारा पूर्ववर्ती** : हाँ, यह पुराना host name और नया destination है।

**action** : changedest

**olddest** : पुराना dest, जिसे बदला जाना है

**oldsig** : olddest का उपयोग करके हस्ताक्षर

**sig** : हस्ताक्षर

उदाहरण:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### होस्टनेम उपनाम जोड़ें

**example.i2p=b64dest द्वारा पूर्व में** : हाँ, यह नया (alias) होस्ट नाम और पुराना destination है।

**action** : addname

**oldname** : पुराना hostname

**sig** : हस्ताक्षर

उदाहरण:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### गंतव्य उपनाम जोड़ें

(क्रिप्टो अपग्रेड के लिए उपयोग किया जाता है)

**example.i2p=b64dest से पूर्व** : हाँ, यह पुराना host name और नया (वैकल्पिक) destination है।

**action** : adddest

**olddest** : पुराना dest

**oldsig** : olddest का उपयोग करके signature

**sig** : dest का उपयोग करते हुए हस्ताक्षर

उदाहरण:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### सबडोमेन जोड़ें

**subdomain.example.i2p=b64dest द्वारा पूर्ववर्ती** : हाँ, यह नया host subdomain नाम और destination है।

**action** : addsubdomain

**oldname** : उच्च-स्तरीय hostname (example.i2p)

**olddest** : उच्च-स्तरीय गंतव्य (जैसे example.i2p)

**oldsig** : olddest का उपयोग करके signature

**sig** : dest का उपयोग करके हस्ताक्षर

उदाहरण:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### मेटाडेटा अपडेट करें

**example.i2p=b64dest द्वारा पूर्ववर्ती** : हाँ, यह पुराना host name और destination है।

**action** : update

**sig** : हस्ताक्षर

(यहाँ कोई भी अपडेटेड keys जोड़ें)

उदाहरण:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### होस्टनेम हटाएं

**example.i2p=b64dest द्वारा पूर्व निर्धारित** : नहीं, ये विकल्पों में निर्दिष्ट हैं

**action** : remove

**name** : होस्टनेम

**dest** : गंतव्य

**sig** : हस्ताक्षर

उदाहरण:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### इस गंतव्य के साथ सभी को हटाएं

**example.i2p=b64dest द्वारा पूर्व निर्धारित** : नहीं, ये विकल्पों में निर्दिष्ट हैं

**action** : removeall

**name** : पुराना hostname, केवल सलाहकारी

**dest** : पुराना dest, इस dest वाले सभी को हटा दिया जाता है

**sig** : हस्ताक्षर

उदाहरण:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### हस्ताक्षर

सभी commands में एक signature key/value `sig=b64signature` होना चाहिए जहां signature अन्य data के लिए है, destination signing key का उपयोग करके।

पुराने और नए destination वाले commands के लिए, `oldsig=b64signature` भी होना चाहिए, और oldname, olddest, या दोनों में से कोई एक।

Add या Change command में, सत्यापन के लिए public key उस Destination में होती है जिसे जोड़ा या बदला जाना है।

कुछ add या edit commands में, एक अतिरिक्त destination का संदर्भ हो सकता है, उदाहरण के लिए जब कोई alias जोड़ते हैं, या कोई destination या host name बदलते हैं। उस स्थिति में, एक दूसरा signature शामिल होना चाहिए और दोनों को verified होना चाहिए। दूसरा signature "inner" signature है और इसे पहले signed और verified किया जाता है ("outer" signature को छोड़कर)। client को परिवर्तनों को verify और accept करने के लिए कोई भी अतिरिक्त कार्रवाई करनी चाहिए।

oldsig हमेशा "आंतरिक" signature होता है। 'oldsig' या 'sig' keys की उपस्थिति के बिना sign और verify करें। sig हमेशा "बाहरी" signature होता है। 'oldsig' key की उपस्थिति के साथ लेकिन 'sig' key के बिना sign और verify करें।

#### हस्ताक्षरों के लिए इनपुट

हस्ताक्षर बनाने या सत्यापित करने के लिए बाइट स्ट्रीम उत्पन्न करने हेतु, निम्नलिखित तरीके से serialize करें:

- "sig" key को हटाएं
- यदि oldsig के साथ verify कर रहे हैं, तो "oldsig" key को भी हटाएं
- केवल Add या Change commands के लिए, `example.i2p=b64dest` output करें
- यदि कोई keys शेष रह जाती हैं, तो `#!` output करें
- Options को UTF-8 key के अनुसार sort करें, duplicate keys पर fail करें
- प्रत्येक key/value के लिए, `key=value` output करें, उसके बाद (यदि यह अंतिम key/value नहीं है तो) एक `#`

नोट्स:

- नई लाइन आउटपुट न करें
- आउटपुट एन्कोडिंग UTF-8 है
- सभी destination और signature एन्कोडिंग I2P alphabet का उपयोग करते हुए Base 64 में है
- Keys और values case-sensitive हैं
- Host names छोटे अक्षरों में होने चाहिए

## संगतता

hosts.txt प्रारूप में सभी नई लाइनें अग्रणी टिप्पणी वर्णों का उपयोग करके लागू की गई हैं, इसलिए सभी पुराने I2P संस्करण नए कमांड को टिप्पणियों के रूप में व्याख्या करेंगे।

जब I2P router नई specification में अपडेट होते हैं, तो वे पुराने comments की पुनर्व्याख्या नहीं करेंगे, लेकिन अपने subscription feeds के बाद के fetches में नए commands को सुनना शुरू कर देंगे। इसलिए name servers के लिए यह महत्वपूर्ण है कि वे command entries को किसी तरीके से बनाए रखें, या etag support को सक्षम करें ताकि router सभी पुराने commands को fetch कर सकें।
