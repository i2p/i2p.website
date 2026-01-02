---
title: "प्लगइन पैकेज प्रारूप"
description: "I2P प्लगइन्स के लिए .xpi2p / .su3 पैकेजिंग नियम"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## अवलोकन

I2P प्लगइन्स हस्ताक्षरित आर्काइव होते हैं जो router की कार्यक्षमता का विस्तार करते हैं। ये `.xpi2p` या `.su3` फ़ाइलों के रूप में उपलब्ध होते हैं, `~/.i2p/plugins/<name>/` (या Windows पर `%APPDIR%\I2P\plugins\<name>\`) में इंस्टॉल होते हैं, और sandboxing (पृथक नियंत्रित परिवेश) के बिना पूर्ण router अनुमतियों के साथ चलते हैं।

### समर्थित प्लगइन प्रकार

- कंसोल वेबऐप्स
- नए eepsites जिनमें cgi-bin, वेबऐप्स हों
- कंसोल थीम्स
- कंसोल अनुवाद
- Java प्रोग्राम (इन-प्रोसेस या अलग JVM)
- शेल स्क्रिप्ट्स और नेटिव बाइनरीज़

### सुरक्षा मॉडल

**गंभीर:** प्लगइन्स उसी JVM (Java Virtual Machine, जावा वर्चुअल मशीन) में I2P router के समान अनुमतियों के साथ चलते हैं। उन्हें बिना किसी प्रतिबंध के इन तक पहुँच होती है:
- फ़ाइल सिस्टम (पढ़ना और लिखना)
- Router APIs और आंतरिक स्थिति
- नेटवर्क कनेक्शन्स
- बाहरी प्रोग्राम का निष्पादन

प्लगइन्स को पूर्णतः विश्वसनीय कोड के रूप में मानना चाहिए। उपयोगकर्ताओं को स्थापना से पहले प्लगइन के स्रोतों और डिजिटल हस्ताक्षरों का सत्यापन करना अनिवार्य है।

---

## फ़ाइल प्रारूप

### SU3 प्रारूप (प्रबल रूप से अनुशंसित)

**स्थिति:** सक्रिय, I2P 0.9.15 (सितंबर 2014) से पसंदीदा प्रारूप

`.su3` फ़ॉर्मेट निम्न प्रदान करता है: - **RSA-4096 हस्ताक्षर कुंजियाँ** (xpi2p में DSA-1024 की तुलना में) - हस्ताक्षर फ़ाइल हेडर में संग्रहीत होता है - मैजिक नंबर: `I2Psu3` - बेहतर भविष्य-संगतता

**संरचना:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### XPI2P प्रारूप (पुराना, अप्रचलित)

**स्थिति:** बैकवर्ड संगतता के लिए समर्थित, नए प्लगइन्स के लिए अनुशंसित नहीं

`.xpi2p` फ़ॉर्मैट पुराने क्रिप्टोग्राफिक हस्ताक्षरों का उपयोग करता है: - **DSA-1024 हस्ताक्षर** (NIST-800-57 के अनुसार अप्रचलित) - ZIP के आरंभ में 40-बाइट DSA हस्ताक्षर जोड़ा जाता है - plugin.config में `key` फ़ील्ड आवश्यक है

**संरचना:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**माइग्रेशन मार्ग:** xpi2p से su3 में स्थानांतरण करते समय, संक्रमण के दौरान `updateURL` और `updateURL.su3` दोनों प्रदान करें। आधुनिक routers (0.9.15+) स्वतः SU3 को प्राथमिकता देते हैं।

---

## आर्काइव लेआउट और plugin.config

### आवश्यक फ़ाइलें

**plugin.config** - कुंजी-मूल्य युग्मों वाली मानक I2P कॉन्फ़िगरेशन फ़ाइल

### आवश्यक गुणधर्म

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**संस्करण फ़ॉर्मैट के उदाहरण:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

वैध विभाजक: `.` (डॉट), `-` (डैश), `_` (अंडरस्कोर)

### वैकल्पिक मेटाडेटा गुण

#### जानकारी प्रदर्शित करें

- `date` - जारी करने की तिथि (Java long टाइमस्टैम्प)
- `author` - डेवलपर का नाम (`user@mail.i2p` अनुशंसित)
- `description` - अंग्रेज़ी विवरण
- `description_xx` - स्थानीयकृत विवरण (xx = भाषा कोड)
- `websiteURL` - प्लगइन मुखपृष्ठ (`http://foo.i2p/`)
- `license` - लाइसेंस पहचानकर्ता (उदा., "Apache-2.0", "GPL-3.0")

#### कॉन्फ़िगरेशन अद्यतन

- `updateURL` - XPI2P अपडेट स्थान (पुराना)
- `updateURL.su3` - SU3 अपडेट स्थान (अधिमान्य)
- `min-i2p-version` - आवश्यक न्यूनतम I2P संस्करण
- `max-i2p-version` - अधिकतम संगत I2P संस्करण
- `min-java-version` - न्यूनतम Java संस्करण (उदा., `1.7`, `17`)
- `min-jetty-version` - न्यूनतम Jetty संस्करण (Jetty 6+ के लिए `6` उपयोग करें)
- `max-jetty-version` - अधिकतम Jetty संस्करण (Jetty 5 के लिए `5.99999` उपयोग करें)

#### स्थापना संबंधी व्यवहार

- `dont-start-at-install` - डिफ़ॉल्ट `false`. यदि `true` है, तो मैन्युअल रूप से शुरू करना आवश्यक है
- `router-restart-required` - डिफ़ॉल्ट `false`. उपयोगकर्ता को सूचित करता है कि अपडेट के बाद रीस्टार्ट आवश्यक है
- `update-only` - डिफ़ॉल्ट `false`. यदि प्लगइन पहले से इंस्टॉल नहीं है तो विफल होता है
- `install-only` - डिफ़ॉल्ट `false`. यदि प्लगइन पहले से मौजूद है तो विफल होता है
- `min-installed-version` - अपडेट के लिए आवश्यक न्यूनतम संस्करण
- `max-installed-version` - अपडेट किए जा सकने वाला अधिकतम संस्करण
- `disableStop` - डिफ़ॉल्ट `false`. यदि `true` है, तो Stop बटन छुपाता है

#### कंसोल एकीकरण

- `consoleLinkName` - कंसोल सारांश पट्टी के लिंक के लिए पाठ
- `consoleLinkName_xx` - स्थानीयकृत लिंक पाठ (xx = भाषा कोड)
- `consoleLinkURL` - लिंक का गंतव्य (उदा., `/appname/index.jsp`)
- `consoleLinkTooltip` - होवर टेक्स्ट (0.7.12-6 से समर्थित)
- `consoleLinkTooltip_xx` - स्थानीयकृत टूलटिप
- `console-icon` - 32x32 आइकन का पथ (0.9.20 से समर्थित)
- `icon-code` - वेब संसाधन रहित प्लगइन्स के लिए Base64-एन्कोडेड 32x32 PNG (0.9.25 से)

#### प्लैटफ़ॉर्म आवश्यकताएँ (केवल दिखाने हेतु)

- `required-platform-OS` - ऑपरेटिंग सिस्टम की आवश्यकता (लागू नहीं किया जाता)
- `other-requirements` - अतिरिक्त आवश्यकताएँ (उदा., "Python 3.8+")

#### निर्भरता प्रबंधन (अभी कार्यान्वित नहीं)

- `depends` - अल्पविराम से अलग की गई प्लगइन निर्भरताएँ
- `depends-version` - निर्भरताओं के लिए संस्करण आवश्यकताएँ
- `langs` - भाषा पैक की सामग्री
- `type` - प्लगइन का प्रकार (app/theme/locale/webapp)

### अपडेट URL में वेरिएबल प्रतिस्थापन

**फ़ीचर स्थिति:** I2P 1.7.0 (0.9.53) से उपलब्ध

दोनों `updateURL` और `updateURL.su3` प्लेटफ़ॉर्म-विशिष्ट वेरिएबल्स का समर्थन करते हैं:

**वेरिएबल्स:** - `$OS` - ऑपरेटिंग सिस्टम: `windows`, `linux`, `mac` - `$ARCH` - आर्किटेक्चर: `386`, `amd64`, `arm64`

**उदाहरण:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Windows AMD64 पर परिणाम:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
यह प्लेटफ़ॉर्म-विशिष्ट बिल्ड्स के लिए एक ही plugin.config फ़ाइल का उपयोग सक्षम करता है।

---

## निर्देशिका संरचना

### मानक लेआउट

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### निर्देशिकाओं के उद्देश्य

**console/locale/** - I2P के आधारभूत अनुवादों के लिए संसाधन बंडल वाली JAR फ़ाइलें - प्लगइन-विशिष्ट अनुवाद `console/webapps/*.war` या `lib/*.jar` में होने चाहिए

**console/themes/** - प्रत्येक उपनिर्देशिका में एक पूर्ण कंसोल थीम होती है - थीम खोज पथ में स्वतः जोड़ा जाता है

**console/webapps/** - कंसोल एकीकरण के लिए `.war` फ़ाइलें - यदि `webapps.config` में अक्षम न किया गया हो तो स्वतः प्रारंभ हो जाती हैं - WAR का नाम प्लगइन के नाम से मेल खाना आवश्यक नहीं है

**eepsite/** - अपनी स्वयं की Jetty इंस्टेंस सहित संपूर्ण eepsite - `jetty.xml` कॉन्फ़िगरेशन में variable substitution (चर प्रतिस्थापन) आवश्यक है - zzzot और pebble प्लगइन के उदाहरण देखें

**lib/** - प्लगइन JAR लाइब्रेरीज़ - classpath में `clients.config` या `webapps.config` के माध्यम से निर्दिष्ट करें

---

## वेबऐप कॉन्फ़िगरेशन

### webapps.config का प्रारूप

मानक I2P कॉन्फ़िगरेशन फ़ाइल जो वेबऐप के व्यवहार को नियंत्रित करती है।

**सिंटैक्स:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**महत्वपूर्ण नोट्स:** - router 0.7.12-9 से पहले, अनुकूलता के लिए `plugin.warname.startOnLoad` का उपयोग करें - API 0.9.53 से पहले, classpath (जावा में क्लास-लोडिंग का पथ) केवल तब काम करता था जब warname, प्लगइन नाम से मेल खाता था - 0.9.53+ से, classpath किसी भी webapp (वेब अनुप्रयोग) नाम के लिए काम करता है

### वेब ऐप के लिए सर्वोत्तम प्रथाएँ

1. **ServletContextListener का कार्यान्वयन**
   - क्लीनअप के लिए `javax.servlet.ServletContextListener` को implement करें
   - या servlet में `destroy()` को override करें
   - अपडेट के दौरान और router रुकने पर सही तरीके से बंद होना सुनिश्चित करता है

2. **लाइब्रेरी प्रबंधन**
   - साझा JARs को `lib/` में रखें, WAR (Web Application Archive—वेब ऐप्लिकेशन आर्काइव) के अंदर नहीं
   - `webapps.config` classpath (क्लासपाथ) के माध्यम से संदर्भ दें
   - अलग से इंस्टॉल/अपडेट प्लगइन्स की सुविधा देता है

3. **परस्पर-विरोधी लाइब्रेरीज़ से बचें**
   - Jetty, Tomcat, या servlet JARs (Java Archive फ़ाइलें) को कभी बंडल न करें
   - मानक I2P स्थापना से JARs को कभी बंडल न करें
   - मानक लाइब्रेरीज़ के लिए classpath (क्लास-लोडिंग पथ) सेक्शन की जाँच करें

4. **संकलन आवश्यकताएँ**
   - `.java` या `.jsp` स्रोत फ़ाइलें शामिल न करें
   - स्टार्टअप विलंब से बचने के लिए सभी JSPs को पूर्व-संकलित करें
   - Java/JSP कम्पाइलर की उपलब्धता मानकर न चलें

5. **Servlet API अनुकूलता**
   - I2P Servlet 3.0 का समर्थन करता है (0.9.30 से)
   - **एनोटेशन स्कैनिंग समर्थित नहीं है** (@WebContent)
   - पारंपरिक `web.xml` deployment descriptor (परिनियोजन विवरणक) प्रदान करना आवश्यक है

6. **Jetty संस्करण**
   - वर्तमान: Jetty 9 (I2P 0.9.30+)
   - एब्स्ट्रैक्शन (अमूर्तता) के लिए `net.i2p.jetty.JettyStart` का उपयोग करें
   - Jetty API में बदलावों से सुरक्षा करता है

---

## क्लाइंट कॉन्फ़िगरेशन

### clients.config प्रारूप

प्लगइन द्वारा आरंभ किए गए क्लाइंट (सेवाएँ) को परिभाषित करता है।

**मूलभूत क्लाइंट:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Stop/Uninstall के साथ क्लाइंट:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### प्रॉपर्टी संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### चर प्रतिस्थापन

निम्नलिखित चर `args`, `stopargs`, `uninstallargs`, और `classpath` में प्रतिस्थापित किए जाते हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### प्रबंधित बनाम अप्रबंधित क्लाइंट्स

**प्रबंधित क्लाइंट्स (अनुशंसित, 0.9.4 से):** - ClientAppManager द्वारा इंस्टैंशिएट किया जाता है - रेफरेंस और स्टेट ट्रैकिंग बनाए रखता है - लाइफसाइकल प्रबंधन अधिक सरल - बेहतर मेमोरी प्रबंधन

**अप्रबंधित क्लाइंट्स:** - router द्वारा शुरू किए जाते हैं, स्थिति का ट्रैक नहीं रखा जाता - कई प्रारंभ/रोक कॉल्स को सुचारू रूप से संभालना चाहिए - समन्वय के लिए स्थैतिक स्थिति या PID फ़ाइलें (प्रक्रिया आईडी फ़ाइलें) उपयोग करें - router के शटडाउन पर कॉल किया जाता है (संस्करण 0.7.12-3 से)

### ShellService (0.9.53 / 1.7.0 से)

बाहरी प्रोग्राम चलाने के लिए स्वचालित state (स्थिति) ट्रैकिंग के साथ एक सामान्यीकृत समाधान।

**विशेषताएँ:** - प्रक्रिया के जीवनचक्र को संभालता है - ClientAppManager के साथ संचार करता है - स्वचालित PID प्रबंधन - क्रॉस-प्लेटफ़ॉर्म समर्थन

**उपयोग:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
प्लेटफ़ॉर्म-विशिष्ट स्क्रिप्ट्स के लिए:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**वैकल्पिक (लेगेसी):** OS प्रकार की जाँच करने वाला Java रैपर लिखें, उपयुक्त `.bat` या `.sh` फ़ाइल के साथ `ShellCommand` को कॉल करें।

---

## स्थापना प्रक्रिया

### उपयोगकर्ता स्थापना प्रक्रिया

1. उपयोगकर्ता Router Console Plugin Configuration Page (`/configplugins`) पर प्लगइन URL पेस्ट करता है
2. Router प्लगइन फ़ाइल डाउनलोड करता है
3. हस्ताक्षर सत्यापन (यदि कुंजी अज्ञात हो और strict mode (कड़ा मोड) सक्षम हो, तो विफल)
4. ZIP अखंडता जाँच
5. `plugin.config` को निकालना और पार्स करना
6. संस्करण संगतता सत्यापन (`min-i2p-version`, `min-java-version`, आदि)
7. webapp (वेब अनुप्रयोग) नाम टकराव का पता लगाना
8. अपडेट होने पर मौजूदा प्लगइन को रोकना
9. डायरेक्टरी सत्यापन (यह `plugins/` के अधीन होना चाहिए)
10. सभी फ़ाइलें प्लगइन डायरेक्टरी में निकालना
11. `plugins.config` को अद्यतन करना
12. प्लगइन प्रारंभ करना (जब तक `dont-start-at-install=true` न हो)

### सुरक्षा और विश्वास

**कुंजी प्रबंधन:** - नए हस्ताक्षरकर्ताओं के लिए First-key-seen trust model (पहली बार देखी गई कुंजी पर आधारित भरोसे का मॉडल) - केवल jrandom और zzz कुंजियाँ पूर्व-पैकेज्ड हैं - 0.9.14.1 से, अज्ञात कुंजियाँ डिफ़ॉल्ट रूप से अस्वीकार की जाती हैं - Advanced property (उन्नत सेटिंग) विकास के लिए ओवरराइड कर सकती है

**स्थापना प्रतिबंध:** - आर्काइव्स को केवल प्लगइन निर्देशिका में ही अनपैक होना चाहिए - इंस्टॉलर `plugins/` के बाहर के पथों को अस्वीकार करता है - स्थापना के बाद प्लगइन्स अन्य स्थानों पर फ़ाइलों तक पहुँच सकते हैं - कोई sandboxing (सीमित, नियंत्रित वातावरण में चलाना) या विशेषाधिकार पृथक्करण नहीं

---

## अद्यतन तंत्र

### अपडेट जांच प्रक्रिया

1. Router plugin.config से `updateURL.su3` (प्राथमिक) या `updateURL` पढ़ता है
2. बाइट्स 41-56 प्राप्त करने के लिए HTTP HEAD या आंशिक GET अनुरोध
3. रिमोट फ़ाइल से संस्करण स्ट्रिंग निकालें
4. VersionComparator का उपयोग करके इंस्टॉल किए गए संस्करण से तुलना करें
5. यदि नया हो, तो उपयोगकर्ता को प्रॉम्प्ट करें या ऑटो-डाउनलोड करें (सेटिंग्स के आधार पर)
6. प्लगइन बंद करें
7. अपडेट इंस्टॉल करें
8. प्लगइन शुरू करें (जब तक उपयोगकर्ता की प्राथमिकता बदली न हो)

### संस्करणों की तुलना

संस्करणों को डॉट/डैश/अंडरस्कोर से अलग घटकों के रूप में पार्स किया जाता है: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**अधिकतम लंबाई:** 16 बाइट (SUD/SU3 हेडर से मेल खाना चाहिए)

### अपडेट करने की सर्वोत्तम प्रथाएँ

1. रिलीज़ के लिए हमेशा संस्करण बढ़ाएँ
2. पिछले संस्करण से अपडेट पथ का परीक्षण करें
3. बड़े बदलावों के लिए `router-restart-required` पर विचार करें
4. माइग्रेशन (स्थानांतरण) के दौरान `updateURL` और `updateURL.su3` दोनों प्रदान करें
5. परीक्षण के लिए बिल्ड नंबर प्रत्यय का उपयोग करें (`1.2.3-456`)

---

## Classpath (क्लास फ़ाइलों के खोज-पथ) और मानक लाइब्रेरियाँ

### Classpath (Java में कक्षाओं और संसाधनों का खोज-पथ) में हमेशा उपलब्ध

`$I2P/lib` की निम्नलिखित JAR फ़ाइलें I2P 0.9.30+ के लिए हमेशा classpath (क्लासपाथ) में होती हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### विशेष टिप्पणियाँ

**commons-logging.jar:** - 0.9.30 से खाली - 0.9.30 से पहले: Apache Tomcat JULI - 0.9.24 से पहले: Commons Logging + JULI - 0.9 से पहले: केवल Commons Logging

**jasper-compiler.jar:** - Jetty 6 (0.9) से खाली

**systray4j.jar:** - 0.9.26 में हटाया गया

### Classpath में नहीं है (निर्दिष्ट करना आवश्यक है)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### क्लासपाथ विनिर्देश

**clients.config में:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**webapps.config में:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**महत्वपूर्ण:** संस्करण 0.7.13-3 से, classpaths (क्लास खोज पथ) थ्रेड-विशिष्ट हैं, JVM-व्यापी नहीं। प्रत्येक क्लाइंट के लिए पूर्ण classpath निर्दिष्ट करें।

---

## जावा संस्करण आवश्यकताएँ

### वर्तमान आवश्यकताएँ (अक्टूबर 2025)

**I2P 2.10.0 और उससे पहले:** - न्यूनतम: Java 7 (0.9.24 से आवश्यक, जनवरी 2016) - अनुशंसित: Java 8 या उससे अधिक

**I2P 2.11.0 और उसके बाद (आगामी):** - **न्यूनतम: Java 17+** (2.9.0 रिलीज़ नोट्स में घोषित) - दो रिलीज़ पहले चेतावनी दी गई (2.9.0 → 2.10.0 → 2.11.0)

### प्लगइन अनुकूलता रणनीति

**अधिकतम संगतता के लिए (I2P 2.10.x तक):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Java 8+ विशेषताओं के लिए:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Java 11+ विशेषताओं के लिए:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**2.11.0+ के लिए तैयारी:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### संकलन के लिए सर्वोत्तम प्रथाएँ

**नए JDK का उपयोग करते हुए पुराने टार्गेट के लिए कम्पाइल करते समय:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
यह उन APIs के उपयोग को रोकता है जो लक्षित Java संस्करण में उपलब्ध नहीं हैं।

---

## Pack200 संपीड़न - अप्रचलित

### महत्वपूर्ण अद्यतन: Pack200 (Java का JAR पैकिंग/संपीड़न प्रारूप) का उपयोग न करें

**स्थिति:** अप्रचलित और हटा दिया गया

मूल विनिर्देश ने 60-65% आकार में कमी के लिए Pack200 compression (Pack200 संपीड़न फ़ॉर्मेट) की दृढ़ता से अनुशंसा की थी। **यह अब मान्य नहीं है।**

**समयरेखा:** - **JEP 336:** Pack200 को Java 11 में deprecated (अप्रचलित) घोषित किया गया (सितंबर 2018) - **JEP 367:** Pack200 को Java 14 में हटा दिया गया (मार्च 2020)

**आधिकारिक I2P अपडेट्स स्पेसिफिकेशन में कहा गया है:** > "zip में मौजूद Jar और war फ़ाइलें अब pack200 से संपीड़ित नहीं की जातीं, जैसा कि ऊपर 'su2' फ़ाइलों के लिए प्रलेखित है, क्योंकि हाल के Java रनटाइम्स अब इसका समर्थन नहीं करते।"

**क्या करें:**

1. **बिल्ड प्रक्रियाओं से pack200 को तुरंत हटाएँ**
2. **मानक ZIP संपीड़न का उपयोग करें**
3. **विकल्पों पर विचार करें:**
   - कोड को छोटा करने के लिए ProGuard/R8
   - नेटिव बाइनरी के लिए UPX
   - यदि कस्टम अनपैकर उपलब्ध कराया जाए तो आधुनिक संपीड़न एल्गोरिदम (zstd, brotli)

**मौजूदा प्लगइन्स के लिए:** - पुराने routers (0.7.11-5 से लेकर Java 10 तक) अभी भी pack200 अनपैक कर सकते हैं - नए routers (Java 11+) pack200 को अनपैक नहीं कर सकते - pack200 compression के बिना प्लगइन्स को पुनः जारी करें

---

## हस्ताक्षर कुंजियाँ और सुरक्षा

### कुंजी निर्माण (SU3 फॉर्मेट)

i2p.scripts रिपॉजिटरी से `makeplugin.sh` स्क्रिप्ट का उपयोग करें:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**मुख्य विवरण:** - एल्गोरिदम: RSA_SHA512_4096 - प्रारूप: X.509 प्रमाणपत्र - संग्रहण: Java keystore प्रारूप

### प्लगइन्स पर हस्ताक्षर

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### कुंजी प्रबंधन की सर्वोत्तम प्रथाएँ

1. **एक बार उत्पन्न करें, सदा सुरक्षित रखें**
   - Routers भिन्न कुंजियों के साथ डुप्लिकेट कुंजी-नामों को अस्वीकार करते हैं
   - Routers भिन्न कुंजी-नामों के साथ डुप्लिकेट कुंजियों को अस्वीकार करते हैं
   - कुंजी/नाम मेल न खाने पर अपडेट अस्वीकार किए जाते हैं

2. **सुरक्षित संग्रहण**
   - keystore (कुंजी-संग्रह) का सुरक्षित बैकअप लें
   - मजबूत पासफ़्रेज़ का उपयोग करें
   - कभी भी version control में commit न करें

3. **कुंजी रोटेशन**
   - वर्तमान आर्किटेक्चर में समर्थित नहीं
   - दीर्घकालिक कुंजी उपयोग की योजना बनाएँ
   - टीम विकास के लिए multi-signature (बहु-हस्ताक्षर) योजनाओं पर विचार करें

### विरासत DSA हस्ताक्षर (XPI2P)

**स्थिति:** कार्यक्षम लेकिन अप्रचलित

xpi2p फ़ॉर्मेट द्वारा उपयोग किए गए DSA-1024 हस्ताक्षर: - 40-बाइट हस्ताक्षर - 172 base64 वर्णों वाली सार्वजनिक कुंजी - NIST-800-57 न्यूनतम (L=2048, N=224) की अनुशंसा करता है - I2P इससे कमजोर (L=1024, N=160) का उपयोग करता है

**अनुशंसा:** इसके बजाय SU3 (साइन किया हुआ पैकेज फ़ॉर्मेट) को RSA-4096 (4096-बिट RSA) के साथ उपयोग करें।

---

## प्लगइन विकास दिशानिर्देश

### आवश्यक सर्वोत्तम प्रथाएँ

1. **दस्तावेज़ीकरण**
   - स्थापना निर्देशों के साथ स्पष्ट README प्रदान करें
   - कॉन्फ़िगरेशन विकल्पों और डिफ़ॉल्ट मानों का दस्तावेज़ीकरण करें
   - प्रत्येक रिलीज़ के साथ changelog (परिवर्तन लॉग) शामिल करें
   - आवश्यक I2P/Java संस्करण निर्दिष्ट करें

2. **आकार अनुकूलन**
   - सिर्फ़ आवश्यक फ़ाइलें शामिल करें
   - router JARs को कभी बंडल न करें
   - इंस्टॉल बनाम अपडेट पैकेज अलग रखें (लाइब्रेरियाँ lib/ में)
   - ~~Pack200 compression (Java का Pack200 संपीड़न फ़ॉर्मैट) का उपयोग करें~~ **अप्रचलित - मानक ZIP का उपयोग करें**

3. **कॉन्फ़िगरेशन**
   - रनटाइम के दौरान `plugin.config` को कभी संशोधित न करें
   - रनटाइम सेटिंग्स के लिए अलग कॉन्फ़िगरेशन फ़ाइल का उपयोग करें
   - आवश्यक router सेटिंग्स का प्रलेखन करें (SAM पोर्ट्स, tunnels, आदि)
   - उपयोगकर्ता की मौजूदा कॉन्फ़िगरेशन का सम्मान करें

4. **संसाधनों का उपयोग**
   - डिफ़ॉल्ट बैंडविड्थ की आक्रामक खपत से बचें
   - CPU उपयोग की उचित सीमाएँ लागू करें
   - शटडाउन के समय संसाधनों को मुक्त करें
   - जहाँ उपयुक्त हो, daemon threads (बैकग्राउंड थ्रेड, जो प्रक्रिया के बंद होते ही स्वतः समाप्त हो जाते हैं) का उपयोग करें

5. **परीक्षण**
   - सभी प्लेटफ़ॉर्म्स पर इंस्टॉल/अपग्रेड/अनइंस्टॉल का परीक्षण करें
   - पिछले संस्करण से अपडेट्स का परीक्षण करें
   - अपडेट्स के दौरान वेबऐप का रुकना/पुनरारंभ सत्यापित करें
   - न्यूनतम समर्थित I2P संस्करण के साथ परीक्षण करें

6. **फ़ाइल सिस्टम**
   - कभी भी `$I2P` में न लिखें (यह केवल-पढ़ने योग्य हो सकता है)
   - रनटाइम डेटा `$PLUGIN` या `$CONFIG` में लिखें
   - डायरेक्टरी खोज के लिए `I2PAppContext` का उपयोग करें
   - `$CWD` के स्थान के बारे में कोई अनुमान न लगाएँ

7. **संगतता**
   - मानक I2P क्लासों को डुप्लिकेट न करें
   - आवश्यक होने पर क्लासों का विस्तार करें, प्रतिस्थापित न करें
   - plugin.config में `min-i2p-version`, `min-jetty-version` जाँचें
   - यदि आप उनका समर्थन करते हैं, तो पुराने I2P संस्करणों के साथ परीक्षण करें

8. **शटडाउन हैंडलिंग**
   - clients.config में उचित `stopargs` लागू करें
   - शटडाउन हुक्स पंजीकृत करें: `I2PAppContext.addShutdownTask()`
   - कई start/stop कॉलों को सुगमता से संभालें
   - सभी थ्रेड्स को daemon mode (बैकग्राउंड मोड; ऐसे थ्रेड जो JVM को बंद होने से नहीं रोकते) में सेट करें

9. **सुरक्षा**
   - सभी बाहरी इनपुट का सत्यापन करें
   - `System.exit()` को कभी कॉल न करें
   - उपयोगकर्ता की गोपनीयता का सम्मान करें
   - सुरक्षित कोडिंग प्रथाओं का पालन करें

10. **लाइसेंसिंग**
    - प्लगइन लाइसेंस को स्पष्ट रूप से निर्दिष्ट करें
    - बंडल की गई लाइब्रेरियों के लाइसेंस का सम्मान करें
    - आवश्यक श्रेय शामिल करें
    - आवश्यक होने पर स्रोत कोड तक पहुँच उपलब्ध कराएँ

### उन्नत विचारणाएँ

**समय-क्षेत्र प्रबंधन:** - Router JVM का समय-क्षेत्र UTC पर सेट करता है - उपयोगकर्ता का वास्तविक समय-क्षेत्र: `I2PAppContext` प्रॉपर्टी `i2p.systemTimeZone`

**निर्देशिका खोज:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**संस्करण क्रमांकन:** - semantic versioning (अर्थ-आधारित संस्करण निर्धारण) का उपयोग करें (major.minor.patch) - परीक्षण के लिए build number जोड़ें (1.2.3-456) - अपडेट्स के लिए monotonic (केवल बढ़ती/गैर-घटती) वृद्धि सुनिश्चित करें

**Router क्लास एक्सेस:** 
- सामान्यतः `router.jar` पर निर्भरता से बचें
- इसके बजाय `i2p.jar` में मौजूद public APIs का उपयोग करें
- भविष्य में I2P संभवतः router क्लास एक्सेस को सीमित कर सकता है

**JVM क्रैश रोकथाम (ऐतिहासिक):** - 0.7.13-3 में ठीक किया गया - class loaders (क्लास लोडर्स) का सही उपयोग करें - चल रहे प्लगइन में JARs (JAR फ़ाइलें) को अपडेट करने से बचें - आवश्यकता होने पर restart-on-update (अपडेट पर पुनरारंभ) के लिए डिज़ाइन करें

---

## Eepsite प्लगइन्स

### अवलोकन

प्लगइन्स अपने Jetty (Java वेब सर्वर) और I2PTunnel इंस्टेंस के साथ पूर्ण eepsites प्रदान कर सकते हैं।

### वास्तुकला

**इनका प्रयास न करें:** - मौजूदा eepsite में स्थापित करना - router के डिफ़ॉल्ट eepsite के साथ मर्ज करना - केवल एक eepsite उपलब्ध मान लेना

**इसके बजाय:** - नया I2PTunnel इंस्टेंस प्रारंभ करें (CLI (कमांड-लाइन इंटरफेस) के माध्यम से) - नया Jetty इंस्टेंस प्रारंभ करें - `clients.config` में दोनों को कॉन्फ़िगर करें

### उदाहरण संरचना

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### jetty.xml में वेरिएबल प्रतिस्थापन

पथों के लिए `$PLUGIN` चर का उपयोग करें:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router प्लगइन के प्रारंभ के दौरान प्रतिस्थापन करता है.

### उदाहरण

संदर्भ कार्यान्वयन: - **zzzot प्लगइन** - टॉरेंट ट्रैकर - **pebble प्लगइन** - ब्लॉग प्लेटफ़ॉर्म

दोनों zzz के प्लगइन पृष्ठ (I2P-internal) पर उपलब्ध हैं।

---

## कंसोल एकीकरण

### सारांश पट्टी के लिंक

router कंसोल सारांश पट्टी में क्लिक करने योग्य लिंक जोड़ें:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
स्थानीयकृत संस्करण:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### कंसोल आइकन

**इमेज फ़ाइल (0.9.20 से):**

```properties
console-icon=/myicon.png
```
यदि निर्दिष्ट किया गया हो तो `consoleLinkURL` के सापेक्ष पथ (0.9.53 से), अन्यथा वेबऐप नाम के सापेक्ष।

**एम्बेडेड आइकन (0.9.25 से):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
इससे जनरेट करें:

```bash
base64 -w 0 icon-32x32.png
```
या Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
आवश्यकताएँ:
- 32x32 पिक्सेल
- PNG प्रारूप
- Base64 एन्कोडेड (कोई लाइन ब्रेक नहीं)

---

## अंतर्राष्ट्रीयकरण

### अनुवाद पैकेज

**I2P बेस अनुवादों के लिए:** - JAR फ़ाइलें `console/locale/` में रखें - मौजूदा I2P एप्स के लिए resource bundles (संसाधन बंडल) शामिल हों - नामकरण: `messages_xx.properties` (xx = भाषा कोड)

**प्लगइन-विशिष्ट अनुवादों के लिए:** - `console/webapps/*.war` में शामिल करें - या `lib/*.jar` में शामिल करें - मानक Java ResourceBundle पद्धति का उपयोग करें

### plugin.config में स्थानीयकृत स्ट्रिंग्स

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
समर्थित फ़ील्ड: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### कंसोल थीम अनुवाद

`console/themes/` में मौजूद थीमें स्वतः थीम खोज पथ में जोड़ दी जाती हैं.

---

## प्लेटफ़ॉर्म-विशिष्ट प्लगइन्स

### पृथक पैकेज दृष्टिकोण

प्रत्येक प्लेटफ़ॉर्म के लिए अलग-अलग प्लगइन नाम उपयोग करें:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### चर प्रतिस्थापन दृष्टिकोण

प्लेटफ़ॉर्म वेरिएबल्स के साथ एक plugin.config:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
clients.config में:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### रनटाइम पर OS की पहचान

शर्त-आधारित निष्पादन के लिए Java का दृष्टिकोण:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## समस्या निवारण

### सामान्य समस्याएँ

**प्लगइन शुरू नहीं हो रहा:** 1. I2P संस्करण संगतता जाँचें (`min-i2p-version`) 2. Java संस्करण सत्यापित करें (`min-java-version`) 3. त्रुटियों के लिए router लॉग जाँचें 4. classpath (Java का क्लास-पाथ) में सभी आवश्यक JAR फ़ाइलें मौजूद हैं, यह सत्यापित करें

**वेबऐप सुलभ नहीं:** 1. पुष्टि करें कि `webapps.config` इसे निष्क्रिय नहीं कर रहा है 2. Jetty संस्करण संगतता (`min-jetty-version`) जांचें 3. सुनिश्चित करें कि `web.xml` मौजूद है (annotation scanning (एनोटेशन स्कैनिंग) समर्थित नहीं है) 4. परस्पर-विरोधी वेबऐप नामों की जांच करें

**अपडेट विफल:** 1. सत्यापित करें कि संस्करण स्ट्रिंग बढ़ाई गई है 2. जाँचें कि हस्ताक्षर हस्ताक्षर कुंजी से मेल खाता है 3. सुनिश्चित करें कि प्लगइन नाम स्थापित संस्करण से मेल खाता है 4. `update-only`/`install-only` सेटिंग्स की समीक्षा करें

**बाहरी प्रोग्राम बंद नहीं हो रहा है:** 1. स्वचालित जीवनचक्र के लिए ShellService का उपयोग करें 2. उचित `stopargs` प्रबंधन लागू करें 3. PID फ़ाइल की सफाई की जाँच करें 4. प्रक्रिया के समाप्त होने की पुष्टि करें

### डिबग लॉगिंग

router में डिबग लॉगिंग सक्षम करें:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
लॉग्स जांचें:

```
~/.i2p/logs/log-router-0.txt
```
---

## संदर्भ जानकारी

### आधिकारिक विनिर्देश

- [प्लगइन विनिर्देश](/docs/specs/plugin/)
- [विन्यास प्रारूप](/docs/specs/configuration/)
- [अद्यतन विनिर्देश](/docs/specs/updates/)
- [क्रिप्टोग्राफी](/docs/specs/cryptography/)

### I2P संस्करण इतिहास

**वर्तमान रिलीज़:** - **I2P 2.10.0** (8 सितंबर 2025)

**0.9.53 के बाद के प्रमुख रिलीज़:** - 2.10.0 (सितंबर 2025) - Java 17+ की घोषणा - 2.9.0 (जून 2025) - Java 17+ चेतावनी - 2.8.0 (अक्टूबर 2024) - पोस्ट-क्वांटम क्रिप्टोग्राफी परीक्षण - 2.6.0 (मई 2024) - I2P-over-Tor ब्लॉकिंग - 2.4.0 (दिसंबर 2023) - NetDB सुरक्षा सुधार - 2.2.0 (मार्च 2023) - भीड़ नियंत्रण - 2.1.0 (जनवरी 2023) - नेटवर्क सुधार - 2.0.0 (नवंबर 2022) - SSU2 ट्रांसपोर्ट प्रोटोकॉल - 1.7.0/0.9.53 (फरवरी 2022) - ShellService, वेरिएबल प्रतिस्थापन - 0.9.15 (सितंबर 2014) - SU3 फ़ॉर्मेट पेश किया गया

**संस्करण क्रमांकन:** - 0.9.x श्रृंखला: संस्करण 0.9.53 तक - 2.x श्रृंखला: 2.0.0 से शुरू (SSU2 परिचय)

### डेवलपर संसाधन

**स्रोत कोड:** - मुख्य रिपॉजिटरी: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub मिरर: https://github.com/i2p/i2p.i2p

**प्लगइन उदाहरण:** - zzzot (BitTorrent ट्रैकर) - pebble (ब्लॉग प्लेटफ़ॉर्म) - i2p-bote (सर्वर-रहित ईमेल) - orchid (Tor क्लाइंट) - seedless (पीयर एक्सचेंज)

**बिल्ड टूल्स:** - makeplugin.sh - कुंजी निर्माण और डिजिटल हस्ताक्षर - i2p.scripts रिपॉज़िटरी में उपलब्ध - su3 निर्माण और सत्यापन को स्वचालित करता है

### सामुदायिक सहायता

**फोरम:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (I2P-आंतरिक)

**IRC/चैट:** - OFTC पर #i2p-dev - I2P नेटवर्क के भीतर IRC

---

## परिशिष्ट A: पूर्ण plugin.config उदाहरण

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## परिशिष्ट B: clients.config का पूर्ण उदाहरण

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## परिशिष्ट C: पूर्ण webapps.config उदाहरण

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## परिशिष्ट D: माइग्रेशन जाँच-सूची (0.9.53 से 2.10.0)

### आवश्यक परिवर्तन

- [ ] **बिल्ड प्रक्रिया से Pack200 (Java JAR संपीड़न प्रारूप) को हटाएँ**
  - Ant/Maven/Gradle स्क्रिप्ट्स से pack200 कार्य हटाएँ
  - pack200 के बिना मौजूदा प्लगइन्स को पुनः जारी करें

- [ ] **Java संस्करण आवश्यकताओं की समीक्षा करें**
  - नई सुविधाओं के लिए Java 11+ आवश्यक करने पर विचार करें
  - I2P 2.11.0 में Java 17+ की आवश्यकता की योजना बनाएं
  - plugin.config में `min-java-version` को अपडेट करें

- [ ] **दस्तावेज़ीकरण अपडेट करें**
  - Pack200 संदर्भ हटाएँ
  - Java संस्करण आवश्यकताओं को अपडेट करें
  - I2P संस्करण संदर्भ अपडेट करें (0.9.x → 2.x)

### अनुशंसित परिवर्तन

- [ ] **क्रिप्टोग्राफ़िक हस्ताक्षरों को सुदृढ़ करें**
  - यदि अभी तक नहीं किया गया है, तो XPI2P से SU3 पर माइग्रेट करें
  - नए प्लगइनों के लिए RSA-4096 कुंजियों का उपयोग करें

- [ ] **नई सुविधाओं का लाभ उठाएँ (यदि 0.9.53+ का उपयोग कर रहे हैं)**
  - प्लेटफ़ॉर्म-विशिष्ट अपडेट के लिए `$OS` / `$ARCH` वेरिएबल्स का उपयोग करें
  - बाहरी प्रोग्रामों के लिए ShellService (शेल सेवा) का उपयोग करें
  - बेहतर वेबऐप क्लासपाथ का उपयोग करें (किसी भी WAR नाम के साथ काम करता है)

- [ ] **संगतता परीक्षण**
  - I2P 2.10.0 पर परीक्षण करें
  - Java 8, 11, 17 के साथ सत्यापित करें
  - Windows, Linux, macOS पर जाँच करें

### वैकल्पिक संवर्द्धन

- [ ] उचित ServletContextListener (एप्लिकेशन जीवनचक्र श्रोता) लागू करें
- [ ] स्थानीयकृत विवरण जोड़ें
- [ ] कंसोल आइकन प्रदान करें
- [ ] शटडाउन हैंडलिंग में सुधार करें
- [ ] व्यापक लॉगिंग जोड़ें
- [ ] स्वचालित परीक्षण लिखें
