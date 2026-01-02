---
title: "प्रबंधित क्लाइंट्स (Managed Clients)"
description: "राउटर-प्रबंधित एप्लिकेशन ClientAppManager और पोर्ट मैपर के साथ कैसे एकीकृत होते हैं"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. अवलोकन

[`clients.config`](/docs/specs/configuration/#clients-config) में एंट्रीज़ राउटर को बताती हैं कि स्टार्टअप पर कौन से एप्लिकेशन लॉन्च करने हैं। प्रत्येक एंट्री **managed** क्लाइंट (अधिमानित) या **unmanaged** क्लाइंट के रूप में चल सकती है। Managed क्लाइंट `ClientAppManager` के साथ सहयोग करते हैं, जो:

- एप्लिकेशन को इंस्टैंशिएट करता है और राउटर कंसोल के लिए लाइफसाइकल स्टेट को ट्रैक करता है
- उपयोगकर्ता को स्टार्ट/स्टॉप नियंत्रण प्रदान करता है और राउटर एग्जिट पर क्लीन शटडाउन लागू करता है
- एक हल्का **क्लाइंट रजिस्ट्री** और **पोर्ट मैपर** होस्ट करता है ताकि एप्लिकेशन एक-दूसरे की सेवाओं को खोज सकें

Unmanaged clients बस एक `main()` method को invoke करते हैं; इनका उपयोग केवल legacy code के लिए करें जिसे modernize नहीं किया जा सकता।

## 2. एक Managed Client को लागू करना

प्रबंधित clients को या तो `net.i2p.app.ClientApp` (user-facing apps के लिए) या `net.i2p.router.app.RouterApp` (router extensions के लिए) implement करना होगा। नीचे दिए गए constructors में से एक प्रदान करें ताकि manager context और configuration arguments supply कर सके:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
`args` array में `clients.config` या `clients.config.d/` में व्यक्तिगत फ़ाइलों में configured किए गए values होते हैं। default lifecycle wiring को inherit करने के लिए जब भी संभव हो `ClientApp` / `RouterApp` helper classes को extend करें।

### 2.1 Lifecycle Methods

प्रबंधित क्लाइंट्स से अपेक्षा की जाती है कि वे निम्नलिखित को लागू करें:

- `startup()` - प्रारंभिकरण करें और तुरंत वापस लौटें। INITIALIZED स्थिति से संक्रमण के लिए कम से कम एक बार `manager.notify()` को कॉल करना आवश्यक है।
- `shutdown(String[] args)` - संसाधनों को मुक्त करें और बैकग्राउंड थ्रेड्स को बंद करें। स्थिति को STOPPING या STOPPED में बदलने के लिए कम से कम एक बार `manager.notify()` को कॉल करना आवश्यक है।
- `getState()` - कंसोल को सूचित करें कि ऐप चल रहा है, शुरू हो रहा है, बंद हो रहा है, या विफल हो गया है

जब उपयोगकर्ता कंसोल के साथ इंटरैक्ट करते हैं तो manager इन methods को कॉल करता है।

### 2.2 Advantages

- राउटर कंसोल में सटीक स्थिति रिपोर्टिंग
- थ्रेड्स या स्टैटिक संदर्भों को लीक किए बिना साफ पुनरारंभ
- एप्लिकेशन बंद होने के बाद कम मेमोरी फुटप्रिंट
- इंजेक्ट किए गए कॉन्टेक्स्ट के माध्यम से केंद्रीकृत लॉगिंग और त्रुटि रिपोर्टिंग

## 3. Unmanaged Clients (Fallback Mode)

यदि कॉन्फ़िगर की गई class एक managed interface को implement नहीं करती है, तो router इसे `main(String[] args)` को invoke करके launch करता है और परिणामी process को track नहीं कर सकता। console सीमित जानकारी दिखाता है और shutdown hooks शायद run न हों। इस mode को उन scripts या one-off utilities के लिए आरक्षित रखें जो managed APIs को adopt नहीं कर सकतीं।

## 4. Client Registry

प्रबंधित और अप्रबंधित clients स्वयं को manager के साथ register कर सकते हैं ताकि अन्य components नाम से reference प्राप्त कर सकें:

```java
manager.register(this);
```
रजिस्ट्रेशन क्लाइंट के `getName()` रिटर्न वैल्यू को रजिस्ट्री की के रूप में उपयोग करता है। ज्ञात रजिस्ट्रेशन में `console`, `i2ptunnel`, `Jetty`, `outproxy`, और `update` शामिल हैं। फीचर्स को समन्वित करने के लिए `ClientAppManager.getRegisteredApp(String name)` के साथ एक क्लाइंट को पुनः प्राप्त करें (उदाहरण के लिए, console द्वारा Jetty से स्टेटस विवरण के लिए क्वेरी करना)।

ध्यान दें कि client registry और port mapper अलग-अलग सिस्टम हैं। client registry नाम लुकअप द्वारा इंटर-एप्लिकेशन संचार को सक्षम बनाता है, जबकि port mapper सेवा खोज के लिए सेवा नामों को host:port संयोजनों से मैप करता है।

## 3. अप्रबंधित क्लाइंट्स (Fallback मोड)

पोर्ट मैपर आंतरिक TCP सेवाओं के लिए एक सरल डायरेक्टरी प्रदान करता है। लूपबैक पोर्ट्स को रजिस्टर करें ताकि सहयोगी हार्डकोडेड एड्रेस से बच सकें:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
या स्पष्ट host विनिर्देश के साथ:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
`PortMapper.getPort(String name)` का उपयोग करके सेवाओं को खोजें (यदि नहीं मिला तो -1 रिटर्न करता है) या `getPort(String name, int defaultPort)` (यदि नहीं मिला तो डिफ़ॉल्ट रिटर्न करता है)। `isRegistered(String name)` के साथ रजिस्ट्रेशन स्टेटस चेक करें और `getActualHost(String name)` के साथ रजिस्टर्ड होस्ट को रिट्रीव करें।

`net.i2p.util.PortMapper` से सामान्य पोर्ट मैपर सेवा स्थिरांक:

- `SVC_CONSOLE` - Router console (डिफ़ॉल्ट पोर्ट 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (डिफ़ॉल्ट पोर्ट 4444)
- `SVC_HTTPS_PROXY` - HTTPS proxy (डिफ़ॉल्ट पोर्ट 4445)
- `SVC_I2PTUNNEL` - I2PTunnel मैनेजर
- `SVC_SAM` - SAM bridge (डिफ़ॉल्ट पोर्ट 7656)
- `SVC_SAM_SSL` - SAM bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB bridge (डिफ़ॉल्ट पोर्ट 2827)
- `SVC_EEPSITE` - मानक eepsite (डिफ़ॉल्ट पोर्ट 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tunnel (डिफ़ॉल्ट पोर्ट 6668)
- `SVC_SUSIDNS` - SusiDNS

नोट: `httpclient`, `httpsclient`, और `httpbidirclient` i2ptunnel tunnel प्रकार हैं (`tunnel.N.type` configuration में उपयोग किए जाते हैं), port mapper service constants नहीं।

## 4. क्लाइंट रजिस्ट्री

### 2.1 लाइफसाइकिल मेथड्स

संस्करण 0.9.42 से, router `clients.config.d/` डायरेक्टरी के भीतर अलग-अलग फ़ाइलों में कॉन्फ़िगरेशन को विभाजित करने का समर्थन करता है। प्रत्येक फ़ाइल में एकल client के लिए properties होती हैं जिनमें सभी properties `clientApp.0.` के साथ prefixed होती हैं:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
यह नई स्थापनाओं और प्लगइन्स के लिए अनुशंसित दृष्टिकोण है।

### 2.2 फायदे

पिछड़े संगतता के लिए, पारंपरिक प्रारूप क्रमिक संख्यांकन का उपयोग करता है:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**आवश्यक:** - `main` - ClientApp या RouterApp को implement करने वाला पूर्ण class नाम, या static `main(String[] args)` युक्त

**वैकल्पिक:** - `name` - router console के लिए प्रदर्शन नाम (class name को डिफ़ॉल्ट मानता है) - `args` - स्पेस या टैब से अलग किए गए तर्क (quoted strings का समर्थन करता है) - `delay` - शुरू होने से पहले सेकंड (डिफ़ॉल्ट 120) - `onBoot` - यदि true है तो `delay=0` को बाध्य करता है - `startOnLoad` - client को सक्षम/अक्षम करता है (डिफ़ॉल्ट true)

**प्लगइन-विशिष्ट:** - `stopargs` - शटडाउन के दौरान पास किए गए आर्गुमेंट्स - `uninstallargs` - प्लगइन अनइंस्टॉल के दौरान पास किए गए आर्गुमेंट्स - `classpath` - कॉमा से अलग किए गए अतिरिक्त classpath एंट्रीज़

**प्लगइन्स के लिए वेरिएबल प्रतिस्थापन:** - `$I2P` - I2P बेस डायरेक्टरी - `$CONFIG` - यूज़र कॉन्फ़िगरेशन डायरेक्टरी (उदाहरण के लिए, ~/.i2p) - `$PLUGIN` - प्लगइन डायरेक्टरी - `$OS` - ऑपरेटिंग सिस्टम का नाम - `$ARCH` - आर्किटेक्चर का नाम

## 5. पोर्ट मैपर

- प्रबंधित क्लाइंट को प्राथमिकता दें; केवल तभी अप्रबंधित का उपयोग करें जब बिल्कुल आवश्यक हो।
- initialization और shutdown को हल्का रखें ताकि console संचालन responsive बना रहे।
- वर्णनात्मक registry और port नामों का उपयोग करें ताकि diagnostic टूल (और अंतिम उपयोगकर्ता) समझ सकें कि सेवा क्या करती है।
- static singletons से बचें - संसाधनों को साझा करने के लिए injected context और manager पर निर्भर रहें।
- सटीक console स्थिति बनाए रखने के लिए सभी state transitions पर `manager.notify()` को कॉल करें।
- यदि आपको अलग JVM में चलाना आवश्यक हो, तो दस्तावेज़ीकरण करें कि logs और diagnostics को main console में कैसे प्रदर्शित किया जाता है।
- बाहरी प्रोग्राम के लिए, प्रबंधित क्लाइंट लाभ प्राप्त करने के लिए ShellService (संस्करण 1.7.0 में जोड़ा गया) का उपयोग करने पर विचार करें।

## 6. कॉन्फ़िगरेशन फॉर्मेट

प्रबंधित क्लाइंट्स को **संस्करण 0.9.4** (17 दिसंबर, 2012) में पेश किया गया था और **संस्करण 2.10.0** (9 सितंबर, 2025) तक अनुशंसित आर्किटेक्चर बने हुए हैं। मुख्य APIs इस अवधि में शून्य ब्रेकिंग परिवर्तनों के साथ स्थिर रहे हैं:

- कंस्ट्रक्टर सिग्नेचर अपरिवर्तित
- लाइफसाइकल मेथड (startup, shutdown, getState) अपरिवर्तित
- ClientAppManager पंजीकरण मेथड अपरिवर्तित
- PortMapper पंजीकरण और लुकअप मेथड अपरिवर्तित

उल्लेखनीय सुधार: - **0.9.42 (2019)** - व्यक्तिगत कॉन्फ़िगरेशन फ़ाइलों के लिए clients.config.d/ डायरेक्टरी संरचना - **1.7.0 (2021)** - बाहरी प्रोग्राम स्थिति ट्रैकिंग के लिए ShellService जोड़ा गया - **2.10.0 (2025)** - वर्तमान रिलीज़ जिसमें कोई managed client API परिवर्तन नहीं

अगले प्रमुख रिलीज़ के लिए न्यूनतम Java 17+ की आवश्यकता होगी (infrastructure requirement, API परिवर्तन नहीं)।

## References

- [clients.config विनिर्देश](/docs/specs/configuration/#clients-config)
- [कॉन्फ़िगरेशन फ़ाइल विनिर्देश](/docs/specs/configuration/)
- [I2P तकनीकी दस्तावेज़ सूची](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp interface](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp interface](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [वैकल्पिक Javadoc (स्थिर)](https://docs.i2p-projekt.de/javadoc/)
- [वैकल्पिक Javadoc (clearnet मिरर)](https://eyedeekay.github.io/javadoc-i2p/)

> **नोट:** I2P नेटवर्क http://idk.i2p/javadoc-i2p/ पर व्यापक प्रलेखन होस्ट करता है जिसके लिए I2P router की आवश्यकता होती है। clearnet एक्सेस के लिए, ऊपर दिए गए GitHub Pages mirror का उपयोग करें।
