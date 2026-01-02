---
title: "Router विन्यास"
description: "I2P routers और क्लाइंट्स के लिए विन्यास विकल्प और प्रारूप"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## अवलोकन

यह दस्तावेज़ router और विभिन्न अनुप्रयोगों द्वारा उपयोग की जाने वाली I2P कॉन्फ़िगरेशन फ़ाइलों का व्यापक तकनीकी विनिर्देश प्रदान करता है। इसमें फ़ाइल फ़ॉर्मेट विनिर्देश, प्रॉपर्टी परिभाषाएँ, और कार्यान्वयन विवरण शामिल हैं, जिन्हें I2P के सोर्स कोड और आधिकारिक दस्तावेज़ीकरण के साथ मिलान करके सत्यापित किया गया है।

### दायरा

- Router (राउटर) विन्यास फ़ाइलें और प्रारूप
- क्लाइंट अनुप्रयोग विन्यास
- I2PTunnel tunnel (टनल) विन्यास
- फ़ाइल प्रारूप विनिर्देश और कार्यान्वयन
- संस्करण-विशिष्ट विशेषताएँ और अप्रचलन

### कार्यान्वयन संबंधी टिप्पणियाँ

कॉन्फ़िगरेशन फ़ाइलें I2P कोर लाइब्रेरी में मौजूद `DataHelper.loadProps()` और `storeProps()` मेथड्स का उपयोग करके पढ़ी और लिखी जाती हैं। फ़ाइल फ़ॉर्मेट, I2P प्रोटोकॉल्स में उपयोग किए जाने वाले सीरियलाइज़्ड फ़ॉर्मेट से काफ़ी भिन्न है (देखें [Common Structures Specification - Type Mapping](/docs/specs/common-structures/#type-mapping)).

---

## सामान्य कॉन्फ़िगरेशन फ़ाइल प्रारूप

I2P कॉन्फ़िगरेशन फ़ाइलें विशिष्ट अपवादों और सीमाओं के साथ संशोधित Java Properties प्रारूप (Java की Properties फ़ाइलों का प्रारूप) का पालन करती हैं।

### प्रारूप विनिर्देश

[Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) पर आधारित, निम्नलिखित महत्वपूर्ण अंतर:

#### एन्कोडिंग

- **MUST** (अनिवार्य) UTF-8 एन्कोडिंग का उपयोग करें (मानक Java Properties में प्रयुक्त ISO-8859-1 नहीं)
- कार्यान्वयन: सभी फ़ाइल संचालन के लिए `DataHelper.getUTF8()` उपयोगिताओं का प्रयोग करता है

#### एस्केप सीक्वेंस

- **कोई भी** एस्केप सीक्वेंस पहचाने नहीं जाते (बैकस्लैश `\` सहित)
- लाइन कंटिन्यूएशन समर्थित **नहीं** है
- बैकस्लैश वर्णों को जस का तस माना जाता है

#### टिप्पणी चिह्न

- `#` एक पंक्ति में किसी भी स्थान पर टिप्पणी शुरू करता है
- `;` **केवल** तब टिप्पणी शुरू करता है जब वह स्तंभ 1 में हो
- `!` टिप्पणी **नहीं** शुरू करता है (Java Properties से भिन्न है)

#### कुंजी-मूल्य विभाजक

- `=` **एकमात्र** वैध कुंजी-मूल्य विभाजक है
- `:` को विभाजक के रूप में **नहीं** पहचाना जाता
- Whitespace (रिक्त स्थान) को विभाजक के रूप में **नहीं** पहचाना जाता

#### रिक्त स्थान प्रबंधन

- कुंजियों (keys) पर आरंभिक और अंतिम रिक्त स्थान **नहीं** हटाए जाते हैं
- मानों (values) पर आरंभिक और अंतिम रिक्त स्थान **हटाए जाते हैं**

#### पंक्ति प्रसंस्करण

- `=` के बिना पंक्तियाँ अनदेखी की जाती हैं (उन्हें टिप्पणियाँ या खाली पंक्तियाँ माना जाता है)
- खाली मान (`key=`) संस्करण 0.9.10 से समर्थित हैं
- खाली मान वाली कुंजियाँ सामान्य रूप से संग्रहीत और पुनर्प्राप्त की जाती हैं

#### वर्ण प्रतिबंध

**कुंजियों में ये नहीं होने चाहिए**:
- `#` (हैश/पाउंड चिह्न)
- `=` (बराबर का चिह्न)
- `\n` (न्यूलाइन वर्ण)
- `;` (सेमिकलन) से शुरू नहीं हो सकतीं

**मानों में निम्न शामिल नहीं हो सकते**:
- `#` (हैश/पाउंड चिन्ह)
- `\n` (नई पंक्ति का वर्ण)
- `\r` (कैरिज रिटर्न) से शुरू या समाप्त नहीं हो सकते
- रिक्त स्थान से शुरू या समाप्त नहीं हो सकते (आरंभ/अंत का रिक्त स्थान स्वतः हटाया जाता है)

### फ़ाइल छँटाई

कॉन्फ़िगरेशन फ़ाइलों को कुंजी के आधार पर क्रमबद्ध करना आवश्यक नहीं है। हालांकि, अधिकांश I2P एप्लिकेशन कॉन्फ़िगरेशन फ़ाइलें लिखते समय कुंजियों को वर्णानुक्रम में क्रमबद्ध करते हैं, ताकि निम्न कार्य सुगम हों: - मैनुअल संपादन - वर्ज़न कंट्रोल diff (अंतर) संचालन - मानव-पठनीयता

### कार्यान्वयन विवरण

#### कॉन्फ़िगरेशन फ़ाइलें पढ़ना

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**व्यवहार**: - UTF-8 एन्कोडेड फ़ाइलें पढ़ता है - ऊपर वर्णित सभी प्रारूप नियम लागू करता है - अक्षर प्रतिबंधों का सत्यापन करता है - यदि फ़ाइल मौजूद नहीं है तो खाली Properties ऑब्जेक्ट लौटाता है - पढ़ने में त्रुटि होने पर `IOException` फेंकता है

#### कॉन्फ़िगरेशन फ़ाइलें लिखना

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**व्यवहार**: - UTF-8 एन्कोडेड फ़ाइलें लिखता है - कुंजियों को वर्णानुक्रम में क्रमबद्ध करता है (यदि OrderedProperties का उपयोग न किया जाए) - संस्करण 0.8.1 से फ़ाइल अनुमतियों को mode 600 पर सेट करता है (केवल उपयोगकर्ता पढ़/लिख सकता है) - कुंजियों या मानों में अमान्य अक्षरों के लिए `IllegalArgumentException` फेंकता है - लेखन त्रुटियों के लिए `IOException` फेंकता है

#### प्रारूप मान्यकरण

कार्यान्वयन कठोर सत्यापन करता है: - कुंजियों और मानों में वर्जित वर्णों की जाँच की जाती है - अवैध प्रविष्टियाँ लिखने के कार्यों के दौरान अपवाद उत्पन्न करती हैं - पढ़ते समय गलत स्वरूप वाली पंक्तियाँ चुपचाप अनदेखी की जाती हैं (जिन पंक्तियों में `=` नहीं होता)

### प्रारूप के उदाहरण

#### मान्य कॉन्फ़िगरेशन फ़ाइल

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### अमान्य विन्यास उदाहरण

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## कोर लाइब्रेरी और Router कॉन्फ़िगरेशन

### क्लाइंट विन्यास (clients.config)

**स्थान**: `$I2P_CONFIG_DIR/clients.config` (पुराना) या `$I2P_CONFIG_DIR/clients.config.d/` (आधुनिक)   **विन्यास इंटरफ़ेस**: Router कंसोल `/configclients` पर   **फॉर्मेट परिवर्तन**: संस्करण 0.9.42 (अगस्त 2019)

#### डायरेक्टरी संरचना (संस्करण 0.9.42+)

रिलीज़ 0.9.42 से, डिफ़ॉल्ट clients.config फ़ाइल स्वतः अलग-अलग कॉन्फ़िगरेशन फ़ाइलों में विभाजित कर दी जाती है:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**स्थानांतरण व्यवहार**: - 0.9.42+ में अपग्रेड के बाद पहली बार चलाने पर, एकल फ़ाइल स्वतः विभाजित हो जाती है - विभाजित फ़ाइलों में प्रॉपर्टीज़ के आगे `clientApp.0.` जोड़ा जाता है - पिछली संगतता के लिए पुराना फ़ॉर्मेट अभी भी समर्थित है - विभाजित फ़ॉर्मेट मॉड्यूलर पैकेजिंग और प्लगइन प्रबंधन सक्षम करता है

#### गुणधर्म प्रारूप

पंक्तियाँ `clientApp.x.prop=val` के रूप में होती हैं, जहाँ `x` ऐप का नंबर है।

**ऐप नंबरिंग आवश्यकताएँ**: - 0 से शुरू होना अनिवार्य है - क्रमिक होना अनिवार्य है (कोई अंतराल नहीं) - क्रम स्टार्टअप अनुक्रम निर्धारित करता है

#### आवश्यक गुणधर्म

##### मुख्य

- **प्रकार**: String (पूर्ण रूप से योग्य क्लास नाम)
- **आवश्यक**: हाँ
- **वर्णन**: इस क्लास में कंस्ट्रक्टर या `main()` मेथड को क्लाइंट प्रकार (प्रबंधित बनाम अप्रबंधित) के अनुसार आह्वान किया जाएगा
- **उदाहरण**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### वैकल्पिक गुणधर्म

##### नाम

- **प्रकार**: String
- **आवश्यक**: नहीं
- **विवरण**: router console में दिखाया जाने वाला नाम
- **उदाहरण**: `clientApp.0.name=Router Console`

##### आर्गुमेंट्स

- **प्रकार**: String (स्पेस या टैब से अलग किए हुए)
- **आवश्यक**: नहीं
- **विवरण**: वे आर्ग्युमेंट्स जो main क्लास के कंस्ट्रक्टर या main() मेथड को पास किए जाते हैं
- **कोटिंग**: जिन आर्ग्युमेंट्स में स्पेस या टैब हों, उन्हें `'` या `"` से कोट किया जा सकता है
- **उदाहरण**: `clientApp.0.args=-d $CONFIG/eepsite`

##### विलंब

- **प्रकार**: पूर्णांक (सेकंड)
- **आवश्यक**: नहीं
- **डिफ़ॉल्ट**: 120
- **विवरण**: क्लायंट शुरू करने से पहले प्रतीक्षा की जाने वाली अवधि (सेकंड में)
- **अधिलेखन**: `onBoot=true` द्वारा अधिलेखित (विलंब को 0 पर सेट करता है)
- **विशेष मान**:
  - `< 0`: router के RUNNING स्थिति तक पहुँचने की प्रतीक्षा करें, फिर नए थ्रेड में तुरंत प्रारंभ करें
  - `= 0`: उसी थ्रेड में तुरंत चलाएँ (अपवाद कंसोल तक प्रसारित होते हैं)
  - `> 0`: विलंब के बाद नए थ्रेड में शुरू करें (अपवाद लॉग किए जाते हैं, प्रसारित नहीं किए जाते)

##### onBoot

- **प्रकार**: Boolean
- **आवश्यक**: नहीं
- **डिफ़ॉल्ट**: false
- **विवरण**: 0 का विलंब लागू करता है, स्पष्ट विलंब सेटिंग को ओवरराइड करता है
- **उपयोग परिदृश्य**: router बूट पर महत्वपूर्ण सेवाओं को तुरंत शुरू करें

##### startOnLoad

- **प्रकार**: Boolean (बूलियन)
- **आवश्यक**: नहीं
- **डिफ़ॉल्ट**: true
- **विवरण**: क्लाइंट को शुरू करना है या नहीं
- **उपयोग परिदृश्य**: कॉन्फ़िगरेशन हटाए बिना क्लायंट्स को निष्क्रिय करना

#### प्लगइन-विशिष्ट गुण

ये गुण केवल प्लगइन्स द्वारा उपयोग किए जाते हैं (कोर क्लाइंट्स द्वारा नहीं):

##### stopargs

- **प्रकार**: स्ट्रिंग (स्पेस या टैब से पृथक)
- **विवरण**: क्लाइंट को रोकने के लिए दिए गए आर्ग्यूमेंट्स
- **चर प्रतिस्थापन**: हाँ (नीचे देखें)

##### uninstallargs

- **प्रकार**: स्ट्रिंग (स्पेस या टैब से पृथक)
- **विवरण**: क्लाइंट को अनइंस्टॉल करने के लिए दिए गए आर्गुमेंट्स
- **वेरिएबल सब्स्टीट्यूशन**: हाँ (नीचे देखें)

##### classpath (जावा में कक्षाओं और लाइब्रेरियों को खोजने का पथ)

- **प्रकार**: String (अल्पविराम से अलग किए गए पथों)
- **विवरण**: क्लाइंट के लिए अतिरिक्त classpath तत्व
- **चर प्रतिस्थापन**: हाँ (नीचे देखें)

#### चर प्रतिस्थापन (केवल प्लगइन्स के लिए)

प्लगइन्स के लिए `args`, `stopargs`, `uninstallargs` और `classpath` में निम्नलिखित वेरिएबल्स प्रतिस्थापित किए जाते हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**नोट**: Variable substitution (चर प्रतिस्थापन) केवल प्लगइन्स के लिए किया जाता है, कोर क्लाइंट्स के लिए नहीं।

#### क्लाइंट प्रकार

##### प्रबंधित क्लाइंट्स

- कंस्ट्रक्टर को `RouterContext` और `ClientAppManager` पैरामीटर के साथ कॉल किया जाता है
- क्लाइंट को `ClientApp` इंटरफ़ेस को कार्यान्वित करना चाहिए
- जीवनचक्र router द्वारा नियंत्रित होता है
- इसे गतिशील रूप से शुरू, बंद, और पुनरारंभ किया जा सकता है

##### अप्रबंधित क्लाइंट्स

- `main(String[] args)` मेथड को कॉल किया जाता है
- अलग थ्रेड में चलता है
- जीवनचक्र का प्रबंधन router द्वारा नहीं किया जाता
- पुराना (legacy) क्लाइंट प्रकार

#### उदाहरण कॉन्फ़िगरेशन

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### लॉगर कॉन्फ़िगरेशन (logger.config)

**स्थान**: `$I2P_CONFIG_DIR/logger.config`   **कॉन्फ़िगरेशन इंटरफ़ेस**: Router console पर `/configlogging`

#### गुणों का संदर्भ

##### कंसोल बफ़र विन्यास

###### logger.consoleBufferSize

- **प्रकार**: पूर्णांक
- **डिफ़ॉल्ट**: 20
- **विवरण**: कंसोल में बफर करने के लिए लॉग संदेशों की अधिकतम संख्या
- **रेंज**: 1-1000 अनुशंसित

##### दिनांक और समय का स्वरूपण

###### logger.dateFormat

- **प्रकार**: String (SimpleDateFormat pattern — तिथि/समय प्रारूप पैटर्न)
- **डिफ़ॉल्ट**: सिस्टम लोकैल से
- **उदाहरण**: `HH:mm:ss.SSS`
- **दस्तावेज़ीकरण**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### लॉग स्तर

###### logger.defaultLevel

- **प्रकार**: Enum (एनेमरेशन प्रकार)
- **डिफ़ॉल्ट**: ERROR
- **मान**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **विवरण**: सभी क्लासों के लिए डिफ़ॉल्ट लॉगिंग स्तर

###### logger.minimumOnScreenLevel

- **प्रकार**: Enum (सीमित नामित मानों का प्रकार)
- **डिफ़ॉल्ट**: CRIT
- **मान**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **विवरण**: स्क्रीन पर दिखाए जाने वाले संदेशों के लिए न्यूनतम स्तर

###### logger.record.{class}

- **प्रकार**: Enum (एनेमरेशन प्रकार)
- **मान**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **विवरण**: प्रति-क्लास लॉगिंग स्तर ओवरराइड
- **उदाहरण**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### प्रदर्शन विकल्प

###### logger.displayOnScreen

- **प्रकार**: बूलियन
- **डिफ़ॉल्ट**: true
- **विवरण**: कंसोल आउटपुट में लॉग संदेश दिखाए जाएँ या नहीं

###### logger.dropDuplicates

- **प्रकार**: Boolean (बूलियन प्रकार; true/false)
- **डिफ़ॉल्ट**: true
- **विवरण**: लगातार आने वाले डुप्लिकेट लॉग संदेशों को छोड़ें

###### logger.dropOnOverflow

- **प्रकार**: Boolean (true/false प्रकार)
- **डिफ़ॉल्ट**: false
- **विवरण**: जब बफ़र भर जाए तो संदेश छोड़ दें (blocking (रोककर प्रतीक्षा करना) के बजाय)

##### फ्लशिंग व्यवहार

###### logger.flushInterval

- **प्रकार**: पूर्णांक (सेकंड)
- **डिफ़ॉल्ट**: 29
- **से**: संस्करण 0.9.18
- **विवरण**: लॉग बफ़र को डिस्क पर कितनी बार फ्लश करना है

##### कॉन्फ़िगरेशन प्रारूप

###### logger.format

- **प्रकार**: String (अक्षरों का क्रम)
- **विवरण**: लॉग संदेश के प्रारूप का टेम्पलेट
- **प्रारूप अक्षर**:
  - `d` = तारीख/समय
  - `c` = क्लास का नाम
  - `t` = थ्रेड का नाम
  - `p` = प्राथमिकता (लॉग स्तर)
  - `m` = संदेश
- **उदाहरण**: `dctpm` से `[टाइमस्टैम्प] [क्लास] [थ्रेड] [स्तर] संदेश` प्राप्त होता है

##### संपीड़न (संस्करण 0.9.56+)

###### logger.gzip

- **प्रकार**: Boolean (सही/गलत)
- **डिफ़ॉल्ट**: false
- **से**: संस्करण 0.9.56
- **विवरण**: रोटेट की गई लॉग फ़ाइलों के लिए gzip संपीड़न सक्षम करें

###### logger.minGzipSize

- **प्रकार**: पूर्णांक (बाइट्स)
- **डिफ़ॉल्ट**: 65536
- **से**: संस्करण 0.9.56
- **विवरण**: संपीड़न सक्रिय करने के लिए न्यूनतम फ़ाइल आकार (डिफ़ॉल्ट 64 KB)

##### फ़ाइल प्रबंधन

###### logger.logBufferSize

- **प्रकार**: पूर्णांक (बाइट्स)
- **डिफ़ॉल्ट**: 1024
- **वर्णन**: बफर को flush (बफर की सामग्री को लिख/भेज कर खाली करना) करने से पहले बफर में रखे जाने वाले संदेशों की अधिकतम संख्या

###### logger.logFileName

- **प्रकार**: String (फ़ाइल पथ)
- **डिफ़ॉल्ट**: `logs/log-@.txt`
- **विवरण**: लॉग फ़ाइल नामकरण पैटर्न (`@` को रोटेशन संख्या से बदला जाता है)

###### logger.logFilenameOverride

- **प्रकार**: String (फ़ाइल पथ)
- **विवरण**: लॉग फ़ाइल नाम के लिए ओवरराइड (रोटेशन पैटर्न को निष्क्रिय करता है)

###### logger.logFileSize

- **प्रकार**: String (इकाई सहित आकार)
- **डिफ़ॉल्ट**: 10M
- **इकाइयाँ**: K (किलोबाइट), M (मेगाबाइट), G (गीगाबाइट)
- **उदाहरण**: `50M`, `1G`

###### logger.logRotationLimit

- **Type**: पूर्णांक
- **Default**: 2
- **Description**: रोटेटेड लॉग फ़ाइल संख्या का अधिकतम मान (log-0.txt से log-N.txt तक)

#### उदाहरण विन्यास

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### प्लगइन विन्यास

#### व्यक्तिगत प्लगइन कॉन्फ़िगरेशन (plugins/*/plugin.config)

**स्थान**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **प्रारूप**: मानक I2P विन्यास फ़ाइल प्रारूप   **दस्तावेज़ीकरण**: [प्लगइन विनिर्देशन](/docs/specs/plugin/)

##### अनिवार्य गुणधर्म

###### नाम

- **प्रकार**: String
- **आवश्यक**: हाँ
- **वर्णन**: प्लगइन का प्रदर्शित नाम
- **उदाहरण**: `name=I2P Plugin Example`

###### कुंजी

- **प्रकार**: String (public key (सार्वजनिक कुंजी))
- **आवश्यक**: हाँ (SU3 हस्ताक्षरित प्लगइन्स के लिए छोड़ दें)
- **विवरण**: सत्यापन के लिए प्लगइन signing key (हस्ताक्षर कुंजी) की public key
- **प्रारूप**: Base64-encoded signing key

###### हस्ताक्षरकर्ता

- **प्रकार**: String
- **आवश्यक**: हाँ
- **विवरण**: प्लगइन साइनर की पहचान
- **उदाहरण**: `signer=user@example.i2p`

###### संस्करण

- **प्रकार**: String (VersionComparator प्रारूप)
- **आवश्यक**: हाँ
- **विवरण**: अपडेट जाँच के लिए प्लगइन संस्करण
- **प्रारूप**: Semantic versioning (अर्थ-आधारित संस्करणन) या कस्टम तुलनीय प्रारूप
- **उदाहरण**: `version=1.2.3`

##### प्रदर्शन गुण

###### तारीख

- **प्रकार**: Long (Unix टाइमस्टैम्प मिलीसेकंड में)
- **विवरण**: प्लगइन जारी करने की तिथि

###### लेखक

- **प्रकार**: String
- **विवरण**: प्लगइन लेखक का नाम

###### websiteURL

- **प्रकार**: String (URL)
- **विवरण**: प्लगइन वेबसाइट URL

###### updateURL

- **प्रकार**: String (URL)
- **विवरण**: प्लगइन के अपडेट की जांच हेतु URL

###### updateURL.su3

- **प्रकार**: स्ट्रिंग (URL)
- **से**: संस्करण 0.9.15
- **विवरण**: SU3 फ़ॉर्मेट अपडेट URL (अधिमान्य)

###### विवरण

- **प्रकार**: String (टेक्स्ट स्ट्रिंग)
- **विवरण**: अंग्रेज़ी में प्लगइन का विवरण

###### description_{language}

- **प्रकार**: स्ट्रिंग
- **विवरण**: स्थानीयकृत प्लगइन विवरण
- **उदाहरण**: `description_de=Deutsche Beschreibung`

###### लाइसेंस

- **प्रकार**: String
- **विवरण**: प्लगइन लाइसेंस पहचानकर्ता
- **उदाहरण**: `license=Apache 2.0`

##### स्थापना गुण

###### स्थापना के समय प्रारंभ न करें

- **प्रकार**: Boolean (बूलियन)
- **डिफ़ॉल्ट**: false
- **विवरण**: स्थापना के बाद स्वतः प्रारंभ को रोकें

###### router-पुनरारंभ-आवश्यक

- **प्रकार**: बूलियन
- **डिफ़ॉल्ट**: false
- **विवरण**: स्थापना के बाद router को पुनरारंभ करना आवश्यक

###### केवल-स्थापना

- **प्रकार**: Boolean
- **डिफ़ॉल्ट**: false
- **विवरण**: केवल एक बार इंस्टॉल करें (कोई अपडेट नहीं)

###### केवल अपडेट

- **प्रकार**: बूलियन
- **डिफ़ॉल्ट**: false
- **विवरण**: केवल मौजूदा स्थापना को अपडेट करें (नया इंस्टॉल नहीं)

##### उदाहरण प्लगइन कॉन्फ़िगरेशन

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### वैश्विक प्लगइन कॉन्फ़िगरेशन (plugins.config)

**स्थान**: `$I2P_CONFIG_DIR/plugins.config`   **उद्देश्य**: स्थापित प्लगइन्स को वैश्विक रूप से सक्रिय/निष्क्रिय करना

##### प्रॉपर्टी प्रारूप

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: plugin.config से प्लगइन का नाम
- `startOnLoad`: router के लॉन्च पर प्लगइन शुरू किया जाए या नहीं

##### उदाहरण

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### वेब अनुप्रयोग कॉन्फ़िगरेशन (webapps.config)

**स्थान**: `$I2P_CONFIG_DIR/webapps.config`   **उद्देश्य**: वेब अनुप्रयोगों को सक्रिय/निष्क्रिय करना और कॉन्फ़िगर करना

#### गुणधर्म प्रारूप

##### webapps.{name}.startOnLoad

- **प्रकार**: बूलियन
- **विवरण**: router लॉन्च पर वेबऐप शुरू करना है या नहीं
- **प्रारूप**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **प्रकार**: String (स्पेस या कॉमा से अलग किए गए पथ)
- **विवरण**: वेबऐप के लिए अतिरिक्त classpath तत्व
- **प्रारूप**: `webapps.{name}.classpath=[paths]`

#### चर प्रतिस्थापन

पथ निम्नलिखित चर प्रतिस्थापनों का समर्थन करते हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### क्लासपाथ निर्धारण

- **कोर वेबऐप्स**: `$I2P/lib` के सापेक्ष पथ
- **प्लगइन वेबऐप्स**: `$CONFIG/plugins/{appname}/lib` के सापेक्ष पथ

#### उदाहरण कॉन्फ़िगरेशन

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Router कॉन्फ़िगरेशन (router.config)

**स्थान**: `$I2P_CONFIG_DIR/router.config`   **कॉन्फ़िगरेशन इंटरफ़ेस**: Router कंसोल `/configadvanced` पर   **उद्देश्य**: मुख्य Router सेटिंग्स और नेटवर्क पैरामीटर

#### कॉन्फ़िगरेशन श्रेणियाँ

##### नेटवर्क कॉन्फ़िगरेशन

बैंडविड्थ सेटिंग्स:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
ट्रांसपोर्ट कॉन्फ़िगरेशन:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Router का व्यवहार

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### कंसोल विन्यास

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### समय विन्यास

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**नोट**: Router का कॉन्फ़िगरेशन काफी विस्तृत है। पूर्ण गुण संदर्भ के लिए `/configadvanced` पर router कंसोल देखें।

---

## एप्लिकेशन कॉन्फ़िगरेशन फ़ाइलें

### पता पुस्तिका विन्यास (addressbook/config.txt)

**स्थान**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **एप्लिकेशन**: SusiDNS   **उद्देश्य**: होस्टनेम रिज़ॉल्यूशन और एड्रेस बुक प्रबंधन

#### फ़ाइल स्थान

##### router_addressbook

- **डिफ़ॉल्ट**: `../hosts.txt`
- **विवरण**: मुख्य पता पुस्तिका (सिस्टम-व्यापी होस्टनेम)
- **प्रारूप**: मानक hosts फ़ाइल प्रारूप

##### privatehosts.txt

- **स्थान**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **विवरण**: निजी होस्टनेम मैपिंग्स
- **प्राथमिकता**: सर्वोच्च (अन्य सभी स्रोतों को ओवरराइड करता है)

##### userhosts.txt

- **स्थान**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **विवरण**: उपयोगकर्ता द्वारा जोड़े गए होस्टनेम मैपिंग्स
- **प्रबंधन**: SusiDNS (I2P की DNS-जैसी सेवा) इंटरफ़ेस के माध्यम से

##### hosts.txt

- **स्थान**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **विवरण**: डाउनलोड की गई सार्वजनिक पता पुस्तिका
- **स्रोत**: सदस्यता फ़ीड्स

#### नामकरण सेवा

##### BlockfileNamingService (0.8.8 से डिफ़ॉल्ट)

स्टोरेज फ़ॉर्मैट: - **फ़ाइल**: `hostsdb.blockfile` - **स्थान**: `$I2P_CONFIG_DIR/addressbook/` - **प्रदर्शन**: hosts.txt की तुलना में ~10x तेज़ लुकअप - **फ़ॉर्मैट**: बाइनरी डेटाबेस फ़ॉर्मैट

पुरानी नामकरण सेवा: - **प्रारूप**: सादा टेक्स्ट hosts.txt - **स्थिति**: अप्रचलित लेकिन अभी भी समर्थित - **उपयोग परिदृश्य**: मैनुअल संपादन, संस्करण नियंत्रण

#### होस्टनेम नियम

I2P होस्टनेम निम्न के अनुरूप होने चाहिए:

1. **TLD आवश्यकता**: अवश्य `.i2p` पर समाप्त होना चाहिए
2. **अधिकतम लंबाई**: कुल 67 अक्षर
3. **वर्ण सेट**: `[a-z]`, `[0-9]`, `.` (पूर्णविराम), `-` (हाइफ़न)
4. **केस**: केवल छोटे अक्षर
5. **प्रारंभिक प्रतिबंध**: `.` या `-` से शुरू नहीं हो सकता
6. **वर्जित पैटर्न**: `..`, `.-`, या `-.` शामिल नहीं हो सकते (संस्करण 0.6.1.33 से)
7. **आरक्षित**: Base32 होस्टनेम `*.b32.i2p` (base32.b32.i2p के 52 अक्षर)

##### वैध उदाहरण

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### अमान्य उदाहरण

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### सदस्यता प्रबंधन

##### subscriptions.txt

- **स्थान**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **प्रारूप**: प्रत्येक पंक्ति में एक URL
- **डिफ़ॉल्ट**: `http://i2p-projekt.i2p/hosts.txt`

##### सब्सक्रिप्शन फ़ीड फ़ॉर्मेट (संस्करण 0.9.26 से)

मेटाडेटा सहित उन्नत फ़ीड प्रारूप:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
मेटाडेटा गुण: - `added`: वह तिथि जब होस्टनेम जोड़ा गया था (YYYYMMDD प्रारूप) - `src`: स्रोत पहचानकर्ता - `sig`: वैकल्पिक हस्ताक्षर

**पिछड़ी संगतता**: सरल hostname=destination प्रारूप अभी भी समर्थित है।

#### उदाहरण विन्यास

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### I2PSnark कॉन्फ़िगरेशन (i2psnark.config.d/i2psnark.config)

**स्थान**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **एप्लिकेशन**: I2PSnark BitTorrent क्लाइंट   **कॉन्फ़िगरेशन इंटरफ़ेस**: http://127.0.0.1:7657/i2psnark पर वेब GUI

#### डायरेक्टरी संरचना

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### मुख्य कॉन्फ़िगरेशन (i2psnark.config)

न्यूनतम डिफ़ॉल्ट कॉन्फ़िगरेशन:

```properties
i2psnark.dir=i2psnark
```
वेब इंटरफ़ेस के माध्यम से प्रबंधित अतिरिक्त गुण:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### व्यक्तिगत टॉरेंट कॉन्फ़िगरेशन

**स्थान**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **स्वरूप**: प्रति-टोरेंट सेटिंग्स   **प्रबंधन**: स्वचालित (वेब GUI के माध्यम से)

गुणों में शामिल हैं: - टोरेंट-विशिष्ट अपलोड/डाउनलोड सेटिंग्स - फ़ाइल प्राथमिकताएँ - ट्रैकर जानकारी - पीयर सीमाएँ

**नोट**: टॉरेंट कॉन्फ़िगरेशन मुख्यतः वेब इंटरफ़ेस के माध्यम से प्रबंधित किए जाते हैं। मैन्युअल संपादन की अनुशंसा नहीं की जाती है।

#### टोरेंट डेटा का संगठन

डेटा भंडारण कॉन्फ़िगरेशन से अलग है:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### I2PTunnel कॉन्फ़िगरेशन (i2ptunnel.config)

**स्थान**: `$I2P_CONFIG_DIR/i2ptunnel.config` (पुराना) या `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (आधुनिक)   **कॉन्फ़िगरेशन इंटरफ़ेस**: Router कंसोल `/i2ptunnel` पर   **प्रारूप परिवर्तन**: संस्करण 0.9.42 (अगस्त 2019)

#### डायरेक्टरी संरचना (संस्करण 0.9.42+)

रिलीज़ 0.9.42 से, डिफ़ॉल्ट i2ptunnel.config फ़ाइल स्वतः विभाजित की जाती है:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**महत्वपूर्ण फ़ॉर्मैट भिन्नता**: - **मोनोलिथिक फ़ॉर्मैट**: प्रॉपर्टीज़ के आगे `tunnel.N.` प्रिफ़िक्स होता है - **विभाजित फ़ॉर्मैट**: प्रॉपर्टीज़ पर कोई प्रिफ़िक्स **नहीं** होता (उदा., `description=`, न कि `tunnel.0.description=`)

#### माइग्रेशन व्यवहार

0.9.42 में अपग्रेड के बाद पहली बार चलाने पर: 1. मौजूदा i2ptunnel.config फ़ाइल पढ़ी जाती है 2. अलग-अलग tunnel कॉन्फ़िग्स i2ptunnel.config.d/ में बनाई जाती हैं 3. विभाजित फ़ाइलों में गुणों से उपसर्ग हटाए जाते हैं 4. मूल फ़ाइल का बैकअप लिया जाता है 5. पिछड़ी संगतता के लिए लेगसी फ़ॉर्मैट अभी भी समर्थित है

#### कॉन्फ़िगरेशन अनुभाग

I2PTunnel कॉन्फ़िगरेशन का विस्तृत वर्णन नीचे दिए गए [I2PTunnel कॉन्फ़िगरेशन संदर्भ](#i2ptunnel-configuration-reference) अनुभाग में है। प्रॉपर्टी विवरण एकीकृत (`tunnel.N.property`) और विभाजित (`property`) दोनों प्रारूपों पर लागू होते हैं।

---

## I2PTunnel कॉन्फ़िगरेशन संदर्भ

यह अनुभाग सभी I2PTunnel कॉन्फ़िगरेशन प्रॉपर्टीज़ के लिए विस्तृत तकनीकी संदर्भ प्रदान करता है। प्रॉपर्टीज़ को विभाजित फ़ॉर्मेट में दिखाया गया है (`tunnel.N.` प्रिफ़िक्स के बिना)। एकात्मक फ़ॉर्मेट के लिए, सभी प्रॉपर्टीज़ के आगे `tunnel.N.` प्रिफ़िक्स लगाएँ, जहाँ N tunnel संख्या है।

**महत्वपूर्ण**: जिन गुणों का वर्णन `tunnel.N.option.i2cp.*` के रूप में किया गया है, वे I2PTunnel में कार्यान्वित हैं और I2CP प्रोटोकॉल या SAM API जैसे अन्य इंटरफेस के माध्यम से **नहीं** समर्थित हैं।

### मूलभूत विशेषताएँ

#### tunnel.N.description (विवरण)

- **प्रकार**: String
- **संदर्भ**: सभी tunnels
- **विवरण**: UI प्रदर्शन हेतु मानव-पठनीय tunnel विवरण
- **उदाहरण**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (नाम)

- **प्रकार**: स्ट्रिंग
- **संदर्भ**: सभी tunnels
- **आवश्यक**: हाँ
- **विवरण**: अद्वितीय tunnel पहचानकर्ता और प्रदर्शित नाम
- **उदाहरण**: `name=I2P HTTP Proxy`

#### tunnel.N.type (प्रकार)

- **प्रकार**: Enum (सूचीबद्ध प्रकार)
- **प्रसंग**: सभी tunnels
- **आवश्यक**: हाँ
- **मान**:
  - `client` - सामान्य क्लाइंट tunnel
  - `httpclient` - HTTP प्रॉक्सी क्लाइंट
  - `ircclient` - IRC क्लाइंट tunnel
  - `socksirctunnel` - SOCKS IRC प्रॉक्सी
  - `sockstunnel` - SOCKS प्रॉक्सी (संस्करण 4, 4a, 5)
  - `connectclient` - CONNECT प्रॉक्सी क्लाइंट
  - `streamrclient` - Streamr क्लाइंट
  - `server` - सामान्य सर्वर tunnel
  - `httpserver` - HTTP सर्वर tunnel
  - `ircserver` - IRC सर्वर tunnel
  - `httpbidirserver` - द्विदिश HTTP सर्वर
  - `streamrserver` - Streamr सर्वर

#### tunnel.N.interface (इंटरफ़ेस)

- **प्रकार**: स्ट्रिंग (IP address या hostname)
- **संदर्भ**: केवल क्लाइंट tunnels
- **डिफ़ॉल्ट**: 127.0.0.1
- **विवरण**: आने वाले कनेक्शनों के लिए बाइंड करने हेतु स्थानीय इंटरफेस
- **सुरक्षा नोट**: 0.0.0.0 पर बाइंड करना रिमोट कनेक्शनों की अनुमति देता है
- **उदाहरण**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **प्रकार**: पूर्णांक
- **संदर्भ**: केवल क्लाइंट tunnels
- **सीमा**: 1-65535
- **विवरण**: क्लाइंट कनेक्शनों के लिए सुनने हेतु स्थानीय पोर्ट
- **उदाहरण**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Type**: स्ट्रिंग (IP पता या होस्टनेम)
- **Context**: केवल सर्वर tunnels
- **Description**: कनेक्शनों को अग्रेषित करने के लिए स्थानीय सर्वर
- **Example**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **प्रकार**: पूर्णांक
- **संदर्भ**: केवल सर्वर tunnels
- **सीमा**: 1-65535
- **विवरण**: targetHost पर कनेक्ट करने हेतु पोर्ट
- **उदाहरण**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **प्रकार**: String (कॉमा या स्पेस से अलग किए गए गंतव्य)
- **संदर्भ**: केवल क्लाइंट tunnels (I2P में डेटा रूटिंग मार्ग)
- **प्रारूप**: `destination[:port][,destination[:port]]`
- **विवरण**: जिन I2P गंतव्य(ओं) से कनेक्ट करना है
- **उदाहरण**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **प्रकार**: स्ट्रिंग (IP पता या होस्टनेम)
- **डिफ़ॉल्ट**: 127.0.0.1
- **विवरण**: I2P router के I2CP इंटरफ़ेस का पता
- **नोट**: router संदर्भ में चलने पर इसे अनदेखा किया जाता है
- **उदाहरण**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **प्रकार**: पूर्णांक
- **डिफ़ॉल्ट**: 7654
- **सीमा**: 1-65535
- **विवरण**: I2P router का I2CP पोर्ट
- **टिप्पणी**: router संदर्भ में चलने पर इसे अनदेखा किया जाता है
- **उदाहरण**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **प्रकार**: Boolean (सच/झूठ वाला डेटा प्रकार)
- **डिफ़ॉल्ट**: true
- **विवरण**: I2PTunnel लोड होने पर tunnel शुरू किया जाए या नहीं
- **उदाहरण**: `startOnLoad=true`

### प्रॉक्सी कॉन्फ़िगरेशन

#### tunnel.N.proxyList (proxyList)

- **प्रकार**: String (कॉमा या स्पेस से अलग किए गए होस्टनेम)
- **संदर्भ**: केवल HTTP और SOCKS प्रॉक्सी
- **विवरण**: outproxy होस्टों की सूची (I2P से बाहरी इंटरनेट के लिए प्रॉक्सी)
- **उदाहरण**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### सर्वर विन्यास

#### tunnel.N.privKeyFile (privKeyFile)

- **प्रकार**: String (फ़ाइल पथ)
- **प्रसंग**: सर्वर और स्थायी क्लाइंट tunnels
- **विवरण**: फ़ाइल जिसमें स्थायी गंतव्य की निजी कुंजियाँ होती हैं
- **पथ**: पूर्ण (absolute) या I2P कॉन्फ़िग डायरेक्टरी के सापेक्ष (relative)
- **उदाहरण**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **प्रकार**: String (होस्टनेम)
- **प्रसंग**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: गंतव्य का Base32 होस्टनेम
- **विवरण**: स्थानीय सर्वर को पास किया जाने वाला Host हेडर मान
- **उदाहरण**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Type**: String (होस्टनेम)
- **Context**: केवल HTTP सर्वरों के लिए
- **Description**: विशिष्ट इनकमिंग पोर्ट के लिए वर्चुअल होस्ट ओवरराइड
- **Use Case**: अलग-अलग पोर्ट पर कई साइटें होस्ट करना
- **Example**: `spoofedHost.8080=site1.example.i2p`

### क्लाइंट-विशिष्ट विकल्प

#### tunnel.N.sharedClient (sharedClient)

- **प्रकार**: Boolean
- **संदर्भ**: केवल क्लाइंट tunnels
- **डिफ़ॉल्ट**: false
- **विवरण**: क्या कई क्लाइंट इस tunnel को साझा कर सकते हैं
- **उदाहरण**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **प्रकार**: Boolean
- **संदर्भ**: केवल client tunnels
- **डिफ़ॉल्ट**: false
- **विवरण**: पुनरारंभों के बीच destination keys (गंतव्य कुंजियाँ) को संग्रहीत करें और पुनः उपयोग करें
- **टकराव**: `i2cp.newDestOnResume=true` के साथ परस्पर बहिष्कृत
- **उदाहरण**: `option.persistentClientKey=true`

### I2CP विकल्प (I2PTunnel कार्यान्वयन)

**महत्वपूर्ण**: ये प्रॉपर्टीज़ `option.i2cp.` से शुरू होती हैं, लेकिन **I2PTunnel में लागू** हैं, I2CP प्रोटोकॉल लेयर में नहीं। ये I2CP या SAM APIs के माध्यम से उपलब्ध नहीं हैं।

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **प्रकार**: Boolean
- **संदर्भ**: केवल Client tunnels के लिए
- **डिफ़ॉल्ट**: false
- **विवरण**: पहले कनेक्शन तक tunnel निर्माण में विलंब करें
- **उपयोग मामला**: कम-उपयोग होने वाले tunnels के लिए संसाधन बचाएँ
- **उदाहरण**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **प्रकार**: Boolean (बूलियन)
- **संदर्भ**: केवल क्लाइंट tunnels
- **डिफ़ॉल्ट**: false
- **आवश्यक**: `i2cp.closeOnIdle=true`
- **संघर्ष**: `persistentClientKey=true` के साथ परस्पर अनन्य
- **विवरण**: निष्क्रियता समयसीमा के बाद नया गंतव्य बनाएँ
- **उदाहरण**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **प्रकार**: स्ट्रिंग (base64-एन्कोडेड कुंजी)
- **संदर्भ**: केवल सर्वर tunnels
- **विवरण**: स्थायी निजी leaseset (I2P में सेवा की पहुँच जानकारी का सेट) एन्क्रिप्शन कुंजी
- **उपयोग परिदृश्य**: रीस्टार्ट्स के दौरान एन्क्रिप्टेड leaseset को सुसंगत बनाए रखना
- **उदाहरण**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **प्रकार**: String (sigtype:base64)
- **प्रसंग**: केवल सर्वर tunnels
- **स्वरूप**: `sigtype:base64key`
- **विवरण**: स्थायी leaseset पर हस्ताक्षर करने की निजी कुंजी
- **उदाहरण**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### सर्वर-विशिष्ट विकल्प

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **प्रकार**: Boolean
- **संदर्भ**: केवल सर्वर tunnels
- **डिफ़ॉल्ट**: false
- **विवरण**: प्रत्येक दूरस्थ I2P destination के लिए अद्वितीय स्थानीय IP का उपयोग करें
- **उपयोग मामला**: सर्वर लॉग्स में क्लाइंट IP पतों को ट्रैक करें
- **सुरक्षा नोट**: गुमनामी कम हो सकती है
- **उदाहरण**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **प्रकार**: String (hostname:port)
- **संदर्भ**: केवल सर्वर tunnels के लिए
- **वर्णन**: आगत पोर्ट NNNN के लिए targetHost/targetPort को ओवरराइड करें
- **उपयोग मामला**: विभिन्न स्थानीय सेवाओं के लिए पोर्ट-आधारित मार्ग निर्धारण
- **उदाहरण**: `option.targetForPort.8080=localhost:8080`

### थ्रेड पूल कॉन्फ़िगरेशन

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **प्रकार**: Boolean
- **प्रसंग**: केवल सर्वर tunnels
- **डिफ़ॉल्ट**: true
- **विवरण**: कनेक्शन प्रबंधन के लिए थ्रेड पूल का उपयोग करें
- **नोट**: मानक सर्वरों के लिए हमेशा false (अनदेखा किया जाता है)
- **उदाहरण**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **प्रकार**: पूर्णांक
- **संदर्भ**: केवल सर्वर tunnels
- **डिफ़ॉल्ट**: 65
- **वर्णन**: अधिकतम थ्रेड पूल आकार
- **नोट**: मानक सर्वरों के लिए अनदेखा किया जाता है
- **उदाहरण**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP क्लाइंट विकल्प

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **डिफ़ॉल्ट**: false
- **विवरण**: .i2p पतों के लिए SSL कनेक्शनों की अनुमति दें
- **उदाहरण**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **प्रकार**: Boolean
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **डिफ़ॉल्ट**: false
- **विवरण**: प्रॉक्सी प्रतिक्रियाओं में address helper (I2P पतों को साझा कराने वाला) लिंक को अक्षम करें
- **उदाहरण**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Type**: स्ट्रिंग (कॉमा या स्पेस से अलग किए गए URLs)
- **Context**: केवल HTTP क्लाइंट्स
- **Description**: होस्टनेम रिज़ॉल्यूशन के लिए जंप सर्वर URLs
- **Example**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP क्लाइंट्स के लिए
- **डिफ़ॉल्ट**: false
- **विवरण**: Accept-* हेडर्स पास करें (Accept और Accept-Encoding को छोड़कर)
- **उदाहरण**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **प्रकार**: बूलियन
- **प्रसंग**: केवल HTTP क्लाइंट्स
- **डिफ़ॉल्ट**: false
- **विवरण**: Referer हेडर को प्रॉक्सी के माध्यम से भेजें
- **गोपनीयता नोट**: जानकारी लीक हो सकती है
- **उदाहरण**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP क्लाइंट्स के लिए
- **डिफ़ॉल्ट**: false
- **विवरण**: प्रॉक्सी के माध्यम से User-Agent (ब्राउज़र पहचान स्ट्रिंग) हेडर पास करें
- **गोपनीयता नोट**: इससे ब्राउज़र की जानकारी लीक हो सकती है
- **उदाहरण**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP क्लाइंट
- **डिफ़ॉल्ट**: false
- **विवरण**: प्रॉक्सी के माध्यम से Via headers पास करें
- **उदाहरण**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **प्रकार**: स्ट्रिंग (कॉमा या स्पेस से अलग किए गए destinations (I2P पते))
- **संदर्भ**: केवल HTTP क्लाइंट्स के लिए
- **वर्णन**: HTTPS के लिए नेटवर्क के भीतर उपलब्ध SSL outproxies (I2P से बाहरी इंटरनेट तक पहुँच देने वाले प्रॉक्सी)
- **उदाहरण**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **डिफ़ॉल्ट**: true
- **विवरण**: पंजीकृत स्थानीय outproxy प्लगइन्स का उपयोग करें
- **उदाहरण**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP क्लाइंट प्रमाणीकरण

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **प्रकार**: Enum (सूचीबद्ध प्रकार)
- **संदर्भ**: केवल HTTP क्लाइंट्स के लिए
- **डिफ़ॉल्ट**: false
- **मान**: `true`, `false`, `basic`, `digest`
- **विवरण**: प्रॉक्सी तक पहुँच के लिए स्थानीय प्रमाणीकरण आवश्यक करें
- **नोट**: `true` `basic` के समतुल्य है
- **उदाहरण**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **प्रकार**: स्ट्रिंग (32 वर्णों का लोअरकेस हेक्स)
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **आवश्यकता**: `proxyAuth=basic` या `proxyAuth=digest`
- **विवरण**: उपयोगकर्ता USER के पासवर्ड का MD5 हैश
- **अप्रचलन**: इसके बजाय SHA-256 का उपयोग करें (0.9.56+)
- **उदाहरण**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **प्रकार**: स्ट्रिंग (64-अक्षरी लोअरकेस हेक्स (हेक्साडेसिमल))
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **आवश्यक**: `proxyAuth=digest`
- **से**: संस्करण 0.9.56
- **मानक**: RFC 7616
- **विवरण**: उपयोगकर्ता USER के पासवर्ड का SHA-256 हैश
- **उदाहरण**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Outproxy (बाहरी प्रॉक्सी) प्रमाणीकरण

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **प्रकार**: Boolean
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **डिफ़ॉल्ट**: false
- **विवरण**: outproxy को प्रमाणीकरण भेजें
- **उदाहरण**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **प्रकार**: स्ट्रिंग
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **आवश्यकता**: `outproxyAuth=true`
- **विवरण**: outproxy प्रमाणीकरण (I2P नेटवर्क से सार्वजनिक इंटरनेट तक ट्रैफिक अग्रेषित करने वाला प्रॉक्सी) के लिए उपयोगकर्ता नाम
- **उदाहरण**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **प्रकार**: स्ट्रिंग
- **संदर्भ**: केवल HTTP क्लाइंट्स
- **आवश्यक**: `outproxyAuth=true`
- **विवरण**: आउटप्रॉक्सी प्रमाणीकरण के लिए पासवर्ड
- **सुरक्षा**: सादे पाठ में संग्रहीत
- **उदाहरण**: `option.outproxyPassword=secret`

### SOCKS क्लाइंट विकल्प

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Type**: स्ट्रिंग (अल्पविराम या स्पेस से विभाजित destinations अर्थात I2P गंतव्य पते)
- **Context**: केवल SOCKS क्लाइंट्स के लिए
- **Description**: नेटवर्क के भीतर outproxies (I2P नेटवर्क से इंटरनेट के लिए प्रॉक्सी सेवाएँ) अनिर्दिष्ट पोर्ट्स के लिए
- **Example**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **प्रकार**: स्ट्रिंग (अल्पविराम या स्पेस से अलग किए गए गंतव्य)
- **संदर्भ**: केवल SOCKS क्लाइंट्स के लिए
- **विवरण**: विशेष रूप से पोर्ट NNNN के लिए नेटवर्क के भीतर के outproxies (क्लियरनेट तक पहुँच के लिए निकास प्रॉक्सी)
- **उदाहरण**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **प्रकार**: Enum (सीमित मानों का प्रकार)
- **संदर्भ**: केवल SOCKS क्लाइंट्स
- **डिफ़ॉल्ट**: socks
- **से**: संस्करण 0.9.57
- **मान**: `socks`, `connect` (HTTPS)
- **विवरण**: कॉन्फ़िगर किए गए outproxy (I2P नेटवर्क से इंटरनेट हेतु बाहरी प्रॉक्सी) का प्रकार
- **उदाहरण**: `option.outproxyType=connect`

### HTTP सर्वर विकल्प

#### tunnel.N.option.maxPosts (option.maxPosts)

- **प्रकार**: पूर्णांक
- **प्रसंग**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: 0 (असीमित)
- **विवरण**: प्रति postCheckTime एक गंतव्य से POST अनुरोधों की अधिकतम संख्या
- **उदाहरण**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **प्रकार**: पूर्णांक
- **प्रसंग**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: 0 (असीमित)
- **विवरण**: प्रति postCheckTime सभी destinations से अधिकतम POST अनुरोधों की संख्या
- **उदाहरण**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **प्रकार**: पूर्णांक (सेकंड)
- **संदर्भ**: केवल HTTP सर्वर
- **डिफ़ॉल्ट**: 300
- **विवरण**: POST सीमाओं की जाँच के लिए समय-अंतराल
- **उदाहरण**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **प्रकार**: पूर्णांक (सेकंड)
- **संदर्भ**: केवल HTTP सर्वर
- **डिफ़ॉल्ट**: 1800
- **विवरण**: एकल गंतव्य के लिए, maxPosts पार होने के बाद प्रतिबंध की अवधि
- **उदाहरण**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **प्रकार**: पूर्णांक (सेकंड में)
- **संदर्भ**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: 600
- **विवरण**: maxTotalPosts पार होने के बाद प्रतिबंध की अवधि
- **उदाहरण**: `option.postTotalBanTime=1200`

### HTTP सर्वर सुरक्षा विकल्प

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: false
- **विवरण**: ऐसे कनेक्शनों को अस्वीकार करें जो संभवतः किसी inproxy (इन-प्रॉक्सी) के माध्यम से आए हों
- **उदाहरण**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP सर्वरों के लिए
- **डिफ़ॉल्ट**: false
- **से**: संस्करण 0.9.25
- **विवरण**: Referer हेडर वाले कनेक्शनों को अस्वीकार करें
- **उदाहरण**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **प्रकार**: बूलियन
- **संदर्भ**: केवल HTTP सर्वर
- **डिफ़ॉल्ट**: false
- **से**: संस्करण 0.9.25 से
- **आवश्यक**: `userAgentRejectList` प्रॉपर्टी
- **विवरण**: मेल खाते User-Agent (HTTP हेडर) वाले कनेक्शनों को अस्वीकार करता है
- **उदाहरण**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **प्रकार**: String (कॉमा से अलग किए गए मिलान स्ट्रिंग्स)
- **संदर्भ**: केवल HTTP सर्वर
- **कब से**: संस्करण 0.9.25 से
- **केस**: केस-सेंसिटिव (अक्षर-मात्रा-संवेदी) मिलान
- **विशेष**: "none" (0.9.33 से) खाली User-Agent से मेल खाता है
- **विवरण**: अस्वीकार करने के लिए User-Agent पैटर्न की सूची
- **उदाहरण**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC सर्वर विकल्प

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **प्रकार**: स्ट्रिंग (होस्टनेम पैटर्न)
- **संदर्भ**: केवल IRC सर्वर
- **डिफ़ॉल्ट**: `%f.b32.i2p`
- **टोकन**:
  - `%f` = पूर्ण base32 डेस्टिनेशन हैश
  - `%c` = क्लोक्ड डेस्टिनेशन हैश (cloakKey देखें)
- **विवरण**: IRC सर्वर को भेजा जाने वाला होस्टनेम फ़ॉर्मेट
- **उदाहरण**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **प्रकार**: String (passphrase (गुप्त वाक्यांश))
- **संदर्भ**: केवल IRC सर्वर
- **डिफ़ॉल्ट**: प्रत्येक सत्र के लिए यादृच्छिक
- **प्रतिबंध**: उद्धरण-चिन्ह या स्पेस नहीं
- **विवरण**: सुसंगत hostname cloaking (होस्टनेम छुपाना) के लिए passphrase
- **उपयोग मामला**: रीस्टार्ट या सर्वर बदलने पर भी स्थायी उपयोगकर्ता ट्रैकिंग
- **उदाहरण**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **प्रकार**: Enum (एनम)
- **संदर्भ**: केवल IRC सर्वर के लिए
- **डिफ़ॉल्ट**: user
- **मान**: `user`, `webirc`
- **विवरण**: IRC सर्वर के लिए प्रमाणीकरण विधि
- **उदाहरण**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Type**: String (टेक्स्ट मान, पासवर्ड)
- **Context**: केवल IRC सर्वरों के लिए
- **Requires**: `method=webirc`
- **Restrictions**: उद्धरण चिह्न या स्पेस नहीं
- **Description**: WEBIRC प्रोटोकॉल प्रमाणीकरण के लिए पासवर्ड
- **Example**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **प्रकार**: स्ट्रिंग (IP पता)
- **प्रसंग**: केवल IRC सर्वरों के लिए
- **आवश्यकता**: `method=webirc`
- **विवरण**: WEBIRC प्रोटोकॉल के लिए spoofed (धोखे से प्रस्तुत) IP पता
- **उदाहरण**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS विन्यास

#### tunnel.N.option.useSSL (option.useSSL)

- **Type**: Boolean (बूलियन)
- **Default**: false
- **Context**: सभी tunnels
- **Behavior**:
  - **Servers**: स्थानीय सर्वर के साथ कनेक्शनों के लिए SSL का उपयोग करें
  - **Clients**: स्थानीय क्लाइंट से SSL आवश्यक करें
- **Example**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **प्रकार**: String (फाइल पाथ)
- **संदर्भ**: केवल Client tunnels
- **डिफ़ॉल्ट**: `i2ptunnel-(random).ks`
- **पथ**: यदि पूर्ण पथ नहीं है तो `$(I2P_CONFIG_DIR)/keystore/` के सापेक्ष
- **स्वतः निर्मित**: यदि मौजूद नहीं है तो बनाया जाएगा
- **विवरण**: SSL निजी कुंजी वाली कीस्टोर फ़ाइल
- **उदाहरण**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Type**: String (पासवर्ड)
- **Context**: केवल क्लाइंट tunnels
- **Default**: changeit
- **Auto-generated**: यदि नया keystore (कुंजी-संग्रह) बनाया जाता है तो यादृच्छिक पासवर्ड
- **Description**: SSL keystore के लिए पासवर्ड
- **Example**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **प्रकार**: String (उपनाम)
- **संदर्भ**: केवल क्लाइंट tunnel
- **स्वतः-निर्मित**: नई कुंजी उत्पन्न होने पर बनाया जाता है
- **विवरण**: keystore (कीस्टोर) में प्राइवेट कुंजी का उपनाम
- **उदाहरण**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **प्रकार**: String (स्ट्रिंग) (पासवर्ड)
- **संदर्भ**: केवल Client tunnels
- **स्वतः-जनित**: यदि नई कुंजी बनाई जाए तो यादृच्छिक पासवर्ड
- **विवरण**: keystore (कुंजी-संग्रह) में private key (निजी कुंजी) के लिए पासवर्ड
- **उदाहरण**: `option.keyPassword=keypass123`

### सामान्य I2CP और स्ट्रीमिंग विकल्प

सभी `tunnel.N.option.*` प्रॉपर्टीज़ (जो ऊपर विशेष रूप से प्रलेखित नहीं हैं) को `tunnel.N.option.` प्रिफिक्स हटाकर I2CP इंटरफ़ेस और स्ट्रीमिंग लाइब्रेरी तक अग्रेषित किया जाता है।

**महत्वपूर्ण**: ये I2PTunnel-विशिष्ट विकल्पों से अलग हैं। देखें: - [I2CP विनिर्देश](/docs/specs/i2cp/) - [स्ट्रीमिंग लाइब्रेरी विनिर्देश](/docs/specs/streaming/)

स्ट्रीमिंग विकल्पों के उदाहरण:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### पूर्ण Tunnel उदाहरण

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## संस्करण इतिहास और विशेषताओं की समयरेखा

### संस्करण 0.9.10 (2013)

**Feature**: कॉन्फ़िगरेशन फ़ाइलों में खाली मान का समर्थन - खाली मान वाली कुंजियाँ (`key=`) अब समर्थित हैं - पहले इन्हें अनदेखा किया जाता था या पार्सिंग त्रुटियों का कारण बनती थीं

### संस्करण 0.9.18 (2015)

**विशेषता**: लॉगर फ्लश अंतराल कॉन्फ़िगरेशन - प्रॉपर्टी: `logger.flushInterval` (डिफ़ॉल्ट 29 सेकंड) - स्वीकार्य लॉग विलंबता बनाए रखते हुए डिस्क I/O को कम करता है

### संस्करण 0.9.23 (नवंबर 2015)

**मुख्य परिवर्तन**: Java 7 की न्यूनतम आवश्यकता - Java 6 का समर्थन समाप्त - निरंतर सुरक्षा अद्यतनों के लिए आवश्यक

### संस्करण 0.9.25 (2015)

**विशेषताएँ**: HTTP सर्वर सुरक्षा विकल्प - `tunnel.N.option.rejectReferer` - Referer हेडर वाले कनेक्शनों को अस्वीकार करें - `tunnel.N.option.rejectUserAgents` - विशिष्ट User-Agent हेडरों को अस्वीकार करें - `tunnel.N.option.userAgentRejectList` - अस्वीकार करने हेतु User-Agent पैटर्न - **उपयोग मामला**: क्रॉलर और अवांछित क्लाइंट्स को सीमित करना

### संस्करण 0.9.33 (जनवरी 2018)

**फ़ीचर**: उन्नत User-Agent फ़िल्टरिंग - `userAgentRejectList` string "none" खाली User-Agent से मेल खाता है - i2psnark, i2ptunnel, streaming, SusiMail के लिए अतिरिक्त बग फिक्स

### संस्करण 0.9.41 (2019)

**अप्रचलन**: Android से BOB Protocol (I2P का पुराना क्लाइंट प्रोटोकॉल) हटाया गया है - Android उपयोगकर्ताओं को SAM या I2CP पर स्थानांतरित होना होगा

### संस्करण 0.9.42 (अगस्त 2019)

**मुख्य परिवर्तन**: कॉन्फ़िगरेशन फ़ाइलों का विभाजन - `clients.config` को `clients.config.d/` डायरेक्टरी संरचना में विभाजित किया गया - `i2ptunnel.config` को `i2ptunnel.config.d/` डायरेक्टरी संरचना में विभाजित किया गया - अपग्रेड के बाद पहली बार चलाने पर स्वचालित migration (स्थानांतरण) - मॉड्यूलर पैकेजिंग और प्लगइन प्रबंधन सक्षम करता है - पुराना मोनोलिथिक प्रारूप अब भी समर्थित है

**अतिरिक्त सुविधाएँ**: - SSU प्रदर्शन में सुधार - क्रॉस-नेटवर्क रोकथाम (Proposal 147) - एन्क्रिप्शन प्रकारों के लिए प्रारंभिक समर्थन

### संस्करण 0.9.56 (2021)

**विशेषताएँ**: सुरक्षा और लॉगिंग में सुधार - `logger.gzip` - रोटेटेड लॉग्स के लिए Gzip संपीड़न (डिफ़ॉल्ट: false) - `logger.minGzipSize` - संपीड़न के लिए न्यूनतम आकार (डिफ़ॉल्ट: 65536 बाइट्स) - `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256 डायजेस्ट प्रमाणीकरण (RFC 7616) - **सुरक्षा**: डायजेस्ट प्रमाणीकरण के लिए MD5 की जगह SHA-256

### संस्करण 0.9.57 (जनवरी 2023)

**फ़ीचर**: SOCKS outproxy (बाहरी प्रॉक्सी) प्रकार कॉन्फ़िगरेशन - `tunnel.N.option.outproxyType` - outproxy प्रकार चुनें (socks|connect) - डिफ़ॉल्ट: socks - HTTPS outproxies के लिए HTTPS CONNECT समर्थन

### संस्करण 2.6.0 (जुलाई 2024)

**ब्रेकिंग चेंज**: I2P-over-Tor ब्लॉक किया गया - Tor एग्ज़िट नोड्स के IP पतों से आने वाले कनेक्शन अब अस्वीकार किए जाते हैं - **कारण**: I2P का प्रदर्शन घटाता है, Tor एग्ज़िट संसाधनों की बर्बादी करता है - **प्रभाव**: Tor एग्ज़िट नोड्स के माध्यम से I2P तक पहुँचने वाले उपयोगकर्ताओं को ब्लॉक किया जाएगा - गैर-एग्ज़िट रिले और Tor क्लाइंट अप्रभावित

### संस्करण 2.10.0 (सितंबर 2025 - वर्तमान)

**मुख्य विशेषताएँ**: - **Post-quantum cryptography** (क्वांटम-कंप्यूटर-रोधी कूटलेखन) उपलब्ध (Hidden Service Manager के माध्यम से opt-in) - **UDP ट्रैकर सपोर्ट** I2PSnark के लिए, ताकि ट्रैकर लोड कम हो - **Hidden Mode स्थिरता** में सुधार, ताकि RouterInfo की कमी कम हो - भीड़भाड़ वाले routers के लिए नेटवर्क सुधार - उन्नत UPnP/NAT ट्रैवर्सल - NetDB में सुधार, आक्रामक leaseset हटाने के साथ - router घटनाओं के लिए अवलोकनीयता में कमी

**कॉन्फ़िगरेशन**: कोई नई कॉन्फ़िगरेशन प्रॉपर्टीज़ नहीं जोड़ी गईं

**महत्वपूर्ण आगामी परिवर्तन**: अगला रिलीज़ (संभावित रूप से 2.11.0 या 3.0.0) के लिए Java 17 या उससे नए संस्करण की आवश्यकता होगी

---

## अप्रचलन और असंगत परिवर्तन

### गंभीर अप्रचलन

#### I2P-over-Tor पहुँच (संस्करण 2.6.0+)

- **स्थिति**: जुलाई 2024 से अवरुद्ध
- **प्रभाव**: Tor exit node (Tor नेटवर्क का एग्ज़िट नोड) के IP पतों से आने वाले कनेक्शन अस्वीकृत कर दिए जाते हैं
- **कारण**: गुमनामी के लाभ दिए बिना I2P नेटवर्क के प्रदर्शन को घटाता है
- **प्रभावित**: केवल Tor exit nodes; रिले या सामान्य Tor क्लाइंट नहीं
- **विकल्प**: I2P या Tor को अलग-अलग उपयोग करें, संयुक्त रूप से नहीं

#### MD5 डाइजेस्ट प्रमाणीकरण

- **स्थिति**: अप्रचलित (SHA-256 का उपयोग करें)
- **प्रॉपर्टी**: `tunnel.N.option.proxy.auth.USER.md5`
- **कारण**: MD5 क्रिप्टोग्राफिक रूप से असुरक्षित है
- **प्रतिस्थापन**: `tunnel.N.option.proxy.auth.USER.sha256` (संस्करण 0.9.56 से)
- **समयरेखा**: MD5 अभी भी समर्थित है, लेकिन अनुशंसित नहीं है

### कॉन्फ़िगरेशन आर्किटेक्चर में परिवर्तन

#### Monolithic (एक-खंडीय) कॉन्फ़िगरेशन फ़ाइलें (संस्करण 0.9.42+)

- **प्रभावित**: `clients.config`, `i2ptunnel.config`
- **स्थिति**: विभाजित डायरेक्टरी संरचना के पक्ष में अप्रचलित
- **स्थानांतरण**: 0.9.42 अपग्रेड के बाद पहली बार चलाने पर स्वतः
- **अनुकूलता**: पुराना प्रारूप अभी भी काम करता है (पश्च-संगत)
- **सिफारिश**: नई कॉन्फ़िगरेशन के लिए विभाजित प्रारूप का उपयोग करें

### Java संस्करण आवश्यकताएँ

#### Java 6 समर्थन

- **समाप्त**: संस्करण 0.9.23 (नवंबर 2015)
- **न्यूनतम**: संस्करण 0.9.23 से Java 7 आवश्यक है

#### Java 17 की आवश्यकता (आगामी)

- **स्थिति**: गंभीर आगामी परिवर्तन
- **लक्ष्य**: 2.10.0 के बाद अगला प्रमुख रिलीज़ (संभावित: 2.11.0 या 3.0.0)
- **वर्तमान न्यूनतम**: Java 8
- **आवश्यक कार्रवाई**: Java 17 पर माइग्रेशन के लिए तैयारी करें
- **समयरेखा**: रिलीज़ नोट्स के साथ घोषित की जाएगी

### हटाई गई विशेषताएँ

#### BOB प्रोटोकॉल (Android)

- **हटाया गया**: संस्करण 0.9.41
- **प्लेटफ़ॉर्म**: केवल Android
- **विकल्प**: SAM या I2CP प्रोटोकॉल
- **डेस्कटॉप**: डेस्कटॉप प्लेटफ़ॉर्म पर BOB अभी भी उपलब्ध है

### अनुशंसित माइग्रेशन

1. **प्रमाणीकरण**: MD5 से SHA-256 digest authentication (डाइजेस्ट प्रमाणीकरण) पर माइग्रेट करें
2. **कॉन्फ़िगरेशन फ़ॉर्मेट**: क्लाइंट्स और tunnels के लिए विभाजित डायरेक्टरी संरचना पर माइग्रेट करें
3. **Java रनटाइम**: अगली प्रमुख रिलीज़ से पहले Java 17 अपग्रेड की योजना बनाएं
4. **Tor एकीकरण**: I2P को Tor एग्जिट नोड्स के माध्यम से रूट न करें

---

## संदर्भ

### आधिकारिक प्रलेखन

- [I2P कॉन्फ़िगरेशन विनिर्देश](/docs/specs/configuration/) - आधिकारिक कॉन्फ़िगरेशन फ़ाइल फ़ॉर्मेट विनिर्देश
- [I2P प्लगइन विनिर्देश](/docs/specs/plugin/) - प्लगइन कॉन्फ़िगरेशन और पैकेजिंग
- [I2P सामान्य संरचनाएँ - टाइप मैपिंग](/docs/specs/common-structures/#type-mapping) - प्रोटोकॉल डेटा सीरियलाइज़ेशन फ़ॉर्मेट
- [Java Properties फ़ॉर्मेट](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - आधार फ़ॉर्मेट विनिर्देश

### स्रोत कोड

- [I2P Java Router रिपॉजिटरी](https://github.com/i2p/i2p.i2p) - GitHub मिरर
- [I2P Developers Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - आधिकारिक I2P स्रोत रिपॉजिटरी
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - कॉन्फ़िगरेशन फ़ाइल I/O का कार्यान्वयन

### सामुदायिक संसाधन

- [I2P Forum](https://i2pforum.net/) - सक्रिय सामुदायिक चर्चाएँ और सहायता
- [I2P Website](/) - आधिकारिक परियोजना वेबसाइट

### API दस्तावेज़ीकरण

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - कॉन्फ़िगरेशन फ़ाइल मेथड्स के लिए API प्रलेखन

### विनिर्देश स्थिति

- **अंतिम विनिर्देशन अद्यतन**: जनवरी 2023 (संस्करण 0.9.57)
- **वर्तमान I2P संस्करण**: 2.10.0 (सितंबर 2025)
- **तकनीकी सटीकता**: विनिर्देशन 2.10.0 तक सटीक बना हुआ है (कोई ब्रेकिंग परिवर्तन नहीं)
- **रखरखाव**: कॉन्फ़िगरेशन फ़ॉर्मेट में संशोधन होने पर Living document (लगातार अद्यतन होने वाला दस्तावेज़) को अद्यतन किया जाता है
