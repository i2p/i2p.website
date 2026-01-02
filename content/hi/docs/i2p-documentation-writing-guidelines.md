---
title: "I2P प्रलेखन लेखन दिशानिर्देश"
description: "I2P तकनीकी दस्तावेज़ीकरण में सुसंगतता, सटीकता और सुगम्यता बनाए रखें"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**उद्देश्य:** I2P तकनीकी प्रलेखन में निरंतरता, सटीकता, और सुलभता बनाए रखना

---

## मूलभूत सिद्धांत

### 1. सब कुछ सत्यापित करें

**कभी मानकर न चलें या अनुमान न लगाएँ।** सभी तकनीकी कथनों को निम्न के विरुद्ध सत्यापित किया जाना चाहिए: - वर्तमान I2P स्रोत कोड (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - आधिकारिक API दस्तावेज़ीकरण (https://i2p.github.io/i2p.i2p/  - कॉन्फ़िगरेशन विनिर्देश [/docs/specs/](/docs/) - हालिया रिलीज़ नोट्स [/releases/](/categories/release/)

**उचित सत्यापन का उदाहरण:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. संक्षिप्तता पर स्पष्टता

ऐसे डेवलपर्स के लिए लिखें जो पहली बार I2P से परिचित हो रहे हों। पूर्व-ज्ञान मानने के बजाय अवधारणाओं को पूरी तरह समझाएँ।

**उदाहरण:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. सुलभता पहले

भले ही I2P एक network overlay (मौजूदा नेटवर्क के ऊपर काम करने वाली परत) है, दस्तावेज़ीकरण clearnet (सामान्य इंटरनेट) पर डेवलपर्स के लिए सुलभ होना चाहिए। I2P-आंतरिक संसाधनों के लिए हमेशा clearnet पर सुलभ वैकल्पिक साधन प्रदान करें।

---

## तकनीकी सटीकता

### API और इंटरफ़ेस प्रलेखन

**हमेशा शामिल करें:** 1. पहली बार उल्लेख पर पूर्ण पैकेज नाम: `net.i2p.app.ClientApp` 2. रिटर्न टाइप सहित पूर्ण मेथड सिग्नेचर 3. पैरामीटर के नाम और प्रकार 4. आवश्यक बनाम वैकल्पिक पैरामीटर

**उदाहरण:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### विन्यास गुणधर्म

कॉन्फ़िगरेशन फ़ाइलों का दस्तावेज़ीकरण करते समय: 1. सटीक प्रॉपर्टी नाम दिखाएँ 2. फ़ाइल एन्कोडिंग निर्दिष्ट करें (I2P कॉन्फ़िग फ़ाइलों के लिए UTF-8) 3. पूर्ण उदाहरण प्रदान करें 4. डिफ़ॉल्ट मानों का दस्तावेज़ करें 5. वह संस्करण उल्लेख करें जब प्रॉपर्टीज़ जोड़ी/बदली गईं

**उदाहरण:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### स्थिरांक और Enumerations (एनम प्रकार)

कॉन्स्टेंट्स का दस्तावेज़ीकरण करते समय, वास्तविक कोड नामों का उपयोग करें:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### समान अवधारणाओं के बीच अंतर करें

I2P में कई परस्पर-अतिव्यापी प्रणालियाँ हैं। आप किस प्रणाली का दस्तावेज़ बना रहे हैं, इसे हमेशा स्पष्ट करें:

**उदाहरण:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## प्रलेखन URLs और संदर्भ

### URL अभिगम्यता नियम

1. **प्राथमिक संदर्भ** को clearnet (सार्वजनिक इंटरनेट) पर सुलभ URLs का उपयोग करना चाहिए
2. **I2P-आंतरिक URLs** (.i2p डोमेन्स) में पहुँच-संबंधी नोट्स शामिल होने चाहिए
3. **हमेशा विकल्प प्रदान करें** जब I2P-आंतरिक संसाधनों से लिंक करें

**I2P-आंतरिक URLs के लिए टेम्पलेट:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### अनुशंसित I2P संदर्भ URLs

**आधिकारिक विनिर्देश:** - [विन्यास](/docs/specs/configuration/) - [प्लगइन](/docs/specs/plugin/) - [दस्तावेज़ सूचकांक](/docs/)

**API प्रलेखन (सबसे नवीनतम चुनें):** - सबसे नवीनतम: https://i2p.github.io/i2p.i2p/ (API 0.9.66, I2P 2.10.0 तक) - Clearnet मिरर: https://eyedeekay.github.io/javadoc-i2p/

**स्रोत कोड:** - GitLab (आधिकारिक): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub mirror (प्रतिलिपि): https://github.com/i2p/i2p.i2p

### लिंक फ़ॉर्मेट मानक

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## संस्करण ट्रैकिंग

### दस्तावेज़ मेटाडेटा

प्रत्येक तकनीकी दस्तावेज़ में फ्रंटमैटर (दस्तावेज़ के आरंभ का मेटाडेटा खंड) में संस्करण मेटाडेटा शामिल होना चाहिए:

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**फ़ील्ड परिभाषाएँ:** - `lastUpdated`: वर्ष-माह जब दस्तावेज़ की अंतिम बार समीक्षा/अद्यतन किया गया - `accurateFor`: वह I2P संस्करण जिसके विरुद्ध इस दस्तावेज़ का सत्यापन किया गया था - `reviewStatus`: इनमें से एक: "draft", "needs-review", "verified", "outdated"

### सामग्री में संस्करण संदर्भ

संस्करणों का उल्लेख करते समय: 1. वर्तमान संस्करण के लिए **गाढ़ा** का उपयोग करें: "**संस्करण 2.10.0** (सितंबर 2025)" 2. ऐतिहासिक संदर्भों के लिए संस्करण संख्या और तारीख दोनों निर्दिष्ट करें 3. जहाँ प्रासंगिक हो, API (एप्लिकेशन प्रोग्रामिंग इंटरफ़ेस) संस्करण को I2P संस्करण से अलग उल्लेख करें

**उदाहरण:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### समय के साथ बदलावों का दस्तावेज़ीकरण

विकसित हुई विशेषताओं के लिए:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### अप्रचलन सूचनाएँ

यदि अप्रचलित विशेषताओं का प्रलेखन कर रहे हैं:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## शब्दावली मानक

### आधिकारिक I2P शब्दावली

इन सटीक शब्दों का एकसमान रूप से उपयोग करें:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### प्रबंधित क्लाइंट शब्दावली

प्रबंधित क्लाइंट्स का दस्तावेज़ीकरण करते समय:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### कॉन्फ़िगरेशन शब्दावली

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### पैकेज और क्लास के नाम

पहली बार उल्लेख करते समय हमेशा पूर्ण रूप से योग्य नामों का उपयोग करें, उसके बाद छोटे नाम:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## कोड उदाहरण और स्वरूपण

### Java कोड के उदाहरण

उचित सिंटैक्स हाइलाइटिंग और पूर्ण उदाहरणों का उपयोग करें:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**कोड उदाहरण आवश्यकताएँ:** 1. महत्वपूर्ण पंक्तियों को समझाने वाली टिप्पणियाँ शामिल करें 2. जहाँ उपयुक्त हो वहाँ त्रुटि हैंडलिंग दिखाएँ 3. यथार्थपरक चर नामों का उपयोग करें 4. I2P कोडिंग परंपराओं से मेल खाएँ (4-space इंडेंट) 5. यदि संदर्भ से स्पष्ट न हो तो imports दिखाएँ

### कॉन्फ़िगरेशन उदाहरण

पूर्ण और मान्य कॉन्फ़िगरेशन के उदाहरण दिखाएँ:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### कमांड लाइन के उदाहरण

उपयोगकर्ता कमांड के लिए `$` का उपयोग करें, root के लिए `#`:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### इनलाइन कोड

इनके लिए बैकटिक्स का उपयोग करें: - मेथड नाम: `startup()` - क्लास नाम: `ClientApp` - प्रॉपर्टी नाम: `clientApp.0.main` - फ़ाइल नाम: `clients.config` - कॉन्स्टेंट्स: `SVC_HTTP_PROXY` - पैकेज नाम: `net.i2p.app`

---

## लहजा और स्वर

### पेशेवर लेकिन सुलभ

तकनीकी पाठकों के लिए बिना उपेक्षापूर्ण लहजा अपनाए लिखें:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### कर्तृवाच्य

स्पष्टता के लिए सक्रिय वाच्य का उपयोग करें:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### निर्देशों के लिए अनिवार्यताएँ

प्रक्रियात्मक सामग्री में प्रत्यक्ष आज्ञार्थक वाक्यों का उपयोग करें:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### अनावश्यक जटिल शब्दावली से बचें

पहली बार उपयोग होने पर शब्दों की व्याख्या करें:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### विराम चिह्न दिशानिर्देश


---

## दस्तावेज़ संरचना

### मानक अनुभाग क्रम

API प्रलेखन के लिए:

1. **अवलोकन** - यह फ़ीचर क्या करता है, यह क्यों मौजूद है
2. **कार्यान्वयन** - इसे कैसे कार्यान्वित/उपयोग करें
3. **विन्यास** - इसे कैसे विन्यस्त करें
4. **API संदर्भ** - विधियों/गुणों के विस्तृत विवरण
5. **उदाहरण** - पूर्णतः कार्यशील उदाहरण
6. **श्रेष्ठ प्रथाएँ** - युक्तियाँ और अनुशंसाएँ
7. **संस्करण इतिहास** - कब प्रस्तुत किया गया, समय के साथ हुए परिवर्तन
8. **संदर्भ** - संबंधित दस्तावेज़ों के लिंक

### शीर्षक पदानुक्रम

सार्थक हेडिंग स्तरों का उपयोग करें:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### सूचना बॉक्स

विशेष सूचनाओं के लिए blockquotes (उद्धरण-ब्लॉक) का उपयोग करें:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### सूचियाँ और संगठन

**अनुक्रम-रहित सूचियाँ** गैर-अनुक्रमिक मदों के लिए:

```markdown
- First item
- Second item
- Third item
```
**क्रमांकित सूचियाँ** क्रमिक चरणों के लिए:

```markdown
1. First step
2. Second step
3. Third step
```
**परिभाषा सूचियाँ** शब्दों की व्याख्या के लिए:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## बचने योग्य सामान्य गलतियाँ

### 1. समान प्रणालियों को लेकर भ्रम

**इनमें भ्रम न करें:** - ClientAppManager रजिस्ट्री बनाम PortMapper - i2ptunnel tunnel प्रकार बनाम port mapper service constants - ClientApp बनाम RouterApp (अलग संदर्भ) - प्रबंधित बनाम अप्रबंधित क्लाइंट्स

**हमेशा यह स्पष्ट करें कि कौन-सा सिस्टम** जिसके बारे में आप चर्चा कर रहे हैं:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. पुराने संस्करण के संदर्भ

**न करें:** - पुराने संस्करणों को "current" के रूप में संदर्भित करें - अप्रचलित API दस्तावेज़ीकरण से लिंक करें - उदाहरणों में deprecated method signatures (अप्रचलित मेथड सिग्नेचर) का उपयोग करें

**करें:** - प्रकाशित करने से पहले रिलीज़ नोट्स की जांच करें - यह सुनिश्चित करें कि API दस्तावेज़ीकरण वर्तमान संस्करण से मेल खाता हो - उदाहरणों को अद्यतन करें ताकि वे वर्तमान सर्वोत्तम प्रथाओं का उपयोग करें

### 3. अप्राप्य URLs

**ऐसा न करें:** - केवल .i2p डोमेन (जिनके clearnet (खुला सार्वजनिक इंटरनेट) विकल्प न हों) से लिंक न करें - टूटी या पुरानी दस्तावेज़ीकरण URLs का उपयोग न करें - स्थानीय file:// paths से लिंक न करें

**करें:** - सभी I2P-आंतरिक लिंक के लिए clearnet (सार्वजनिक इंटरनेट) विकल्प प्रदान करें - प्रकाशन से पहले यह सत्यापित करें कि URLs सुलभ हैं - स्थायी URLs का उपयोग करें (geti2p.net, अस्थायी होस्टिंग नहीं)

### 4. अपूर्ण कोड उदाहरण

**ऐसा न करें:** - संदर्भ के बिना अंश न दिखाएँ - त्रुटि प्रबंधन न छोड़ें - अपरिभाषित वेरिएबल्स का उपयोग न करें - जहाँ स्पष्ट न हो वहाँ इम्पोर्ट स्टेटमेंट्स न छोड़ें

**करें:** - पूर्ण, संकलनीय उदाहरण दिखाएँ - आवश्यक त्रुटि प्रबंधन शामिल करें - प्रत्येक महत्वपूर्ण पंक्ति क्या करती है, समझाएँ - प्रकाशित करने से पहले उदाहरणों का परीक्षण करें

### 5. द्व्यर्थक वक्तव्य

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Markdown परंपराएँ

### फ़ाइल नामकरण

फ़ाइल नामों के लिए kebab-case (शब्दों को हाइफ़न से जोड़ने की शैली) का उपयोग करें: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### फ्रंटमैटर प्रारूप

हमेशा YAML frontmatter (YAML फ़ाइल के शीर्ष पर मेटाडेटा ब्लॉक) शामिल करें:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### लिंक स्वरूपण

**आंतरिक लिंक** (दस्तावेज़ीकरण के भीतर):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**बाहरी लिंक** (अन्य संसाधनों के लिए):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**कोड रिपॉज़िटरी लिंक**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### तालिका स्वरूपण

GitHub-flavored Markdown (GitHub शैली वाला Markdown) तालिकाओं का उपयोग करें:

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### कोड ब्लॉक भाषा टैग्स

सिंटैक्स हाइलाइटिंग के लिए हमेशा भाषा निर्दिष्ट करें:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## समीक्षा जाँच-सूची

प्रलेखन प्रकाशित करने से पहले, जाँच करें:


---

**प्रतिक्रिया:** यदि आपको इन दिशानिर्देशों में समस्याएँ मिलती हैं या आपके पास सुझाव हैं, तो कृपया उन्हें आधिकारिक I2P विकास चैनलों के माध्यम से प्रस्तुत करें।
