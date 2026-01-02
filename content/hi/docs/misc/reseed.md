---
title: "Reseed (I2P नेटवर्क से पहली बार जुड़ने हेतु शुरुआती डेटा डाउनलोड प्रक्रिया) होस्ट"
description: "reseed services (प्रारंभिक साथियों की सूची प्रदान करने वाली सेवाएँ) और alternate bootstrap methods (नेटवर्क से पहली बार जुड़ने के वैकल्पिक तरीके) का संचालन"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Reseed होस्ट्स के बारे में

नए routers को I2P नेटवर्क से जुड़ने के लिए कुछ पीयर्स की आवश्यकता होती है। Reseed hosts (reseed: प्रारंभिक पीयर्स का सेट प्राप्त करने की प्रक्रिया) एन्क्रिप्टेड HTTPS डाउनलोड्स के माध्यम से वह प्रारंभिक bootstrap सेट (आरंभिक सेटअप हेतु डेटा) उपलब्ध कराते हैं। प्रत्येक reseed bundle host द्वारा साइन किया जाता है, जिससे अप्रमाणित पक्षों द्वारा छेड़छाड़ रोकी जाती है। स्थापित routers समय-समय पर, यदि उनका पीयर सेट पुराना हो जाए, तो reseed कर सकते हैं।

### नेटवर्क बूटस्ट्रैप प्रक्रिया

जब कोई I2P router पहली बार शुरू होता है या लंबे समय तक ऑफ़लाइन रहा होता है, तो नेटवर्क से जुड़ने के लिए उसे RouterInfo डेटा की आवश्यकता होती है। क्योंकि router के पास कोई मौजूदा पीयर्स नहीं होते, वह यह जानकारी I2P नेटवर्क के भीतर से प्राप्त नहीं कर सकता। reseed तंत्र (प्रारंभिक बूटस्ट्रैप प्रक्रिया) विश्वसनीय बाहरी HTTPS सर्वरों से RouterInfo फ़ाइलें प्रदान करके इस बूटस्ट्रैप समस्या का समाधान करता है।

reseed प्रक्रिया (नए router को नेटवर्क से जोड़ने हेतु शुरुआती डेटा प्राप्त करने की प्रक्रिया) एकल क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित बंडल में 75-100 RouterInfo फ़ाइलें प्रदान करती है। यह सुनिश्चित करता है कि नए router मैन-इन-द-मिडल हमलों के प्रति उजागर हुए बिना शीघ्रता से कनेक्शन स्थापित कर सकें, जो उन्हें अविश्वसनीय, पृथक नेटवर्क विभाजनों में अलग-थलग कर सकते हैं।

### वर्तमान नेटवर्क स्थिति

अक्टूबर 2025 तक, I2P नेटवर्क router संस्करण 2.10.0 (API संस्करण 0.9.67) पर संचालित हो रहा है। संस्करण 0.9.14 में पेश किया गया reseed प्रोटोकॉल (नए router को नेटवर्क की प्रारंभिक जानकारी उपलब्ध कराने की प्रक्रिया) अपनी मुख्य कार्यक्षमता में स्थिर है और अपरिवर्तित बना हुआ है। उपलब्धता और सेंसरशिप-प्रतिरोध सुनिश्चित करने के लिए नेटवर्क विश्वभर में वितरित कई स्वतंत्र reseed सर्वर बनाए रखता है।

सेवा [checki2p](https://checki2p.com/reseed) हर 4 घंटे पर सभी I2P reseed (बूटस्ट्रैप डेटा वितरण) सर्वरों की निगरानी करती है, और reseed अवसंरचना के लिए रीयल-टाइम स्थिति जाँच और उपलब्धता मेट्रिक्स प्रदान करती है।

## SU3 फ़ाइल प्रारूप विनिर्देश

SU3 फ़ाइल फ़ॉर्मेट I2P के reseed (नेटवर्क के प्रारंभिक netDb डेटा और संपर्क प्राप्त करने की प्रक्रिया) प्रोटोकॉल का आधार है, जो क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित सामग्री का वितरण प्रदान करता है। इस फ़ॉर्मेट को समझना reseed सर्वर और क्लाइंट्स के कार्यान्वयन के लिए आवश्यक है।

### फ़ाइल संरचना

SU3 प्रारूप तीन मुख्य घटकों से बना होता है: हेडर (40+ बाइट्स), सामग्री (परिवर्तनीय लंबाई), और हस्ताक्षर (जिसकी लंबाई हेडर में निर्दिष्ट होती है)।

#### हेडर प्रारूप (बाइट्स 0-39 न्यूनतम)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Reseed (I2P नेटवर्क की प्रारंभिक बूटस्ट्रैप/सीडिंग प्रक्रिया)-विशिष्ट SU3 (हस्ताक्षरित अपडेट/रीसीड फ़ाइल फ़ॉर्मेट) पैरामीटर

रीसीड बंडलों के लिए, SU3 फ़ाइल में निम्नलिखित विशेषताएँ होनी चाहिए:

- **फ़ाइल नाम**: ठीक-ठीक `i2pseeds.su3` होना चाहिए
- **सामग्री प्रकार** (बाइट 27): 0x03 (RESEED)
- **फ़ाइल प्रकार** (बाइट 25): 0x00 (ZIP)
- **हस्ताक्षर प्रकार** (बाइट 8-9): 0x0006 (RSA-4096-SHA512)
- **संस्करण स्ट्रिंग**: ASCII में Unix timestamp (epoch (एपोक) के बाद से सेकंड, date +%s फ़ॉर्मेट)
- **हस्ताक्षरकर्ता ID**: X.509 प्रमाणपत्र के CN से मेल खाता ईमेल-शैली का पहचानकर्ता

#### नेटवर्क ID क्वेरी पैरामीटर

संस्करण 0.9.42 से, routers reseed अनुरोधों (प्रारंभिक नेटवर्क बूटस्ट्रैप हेतु) में `?netid=2` जोड़ते हैं। यह विभिन्न नेटवर्कों के बीच कनेक्शनों को रोकता है, क्योंकि टेस्ट नेटवर्क अलग-अलग नेटवर्क ID का उपयोग करते हैं। वर्तमान I2P प्रोडक्शन नेटवर्क नेटवर्क ID 2 का उपयोग करता है।

उदाहरण अनुरोध: `https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP सामग्री संरचना

सामग्री अनुभाग (हेडर के बाद, सिग्नेचर से पहले) में निम्नलिखित आवश्यकताओं वाला एक मानक ZIP आर्काइव समाहित होता है:

- **संपीड़न**: मानक ZIP संपीड़न (DEFLATE)
- **फ़ाइल संख्या**: आम तौर पर 75-100 RouterInfo फ़ाइलें (I2P router की जानकारी वाली फ़ाइलें)
- **डायरेक्टरी संरचना**: सभी फ़ाइलें शीर्ष स्तर पर ही होनी चाहिए (कोई उप-डायरेक्टरी नहीं)
- **फ़ाइल नामकरण**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64 वर्णमाला**: I2P की परिवर्तित Base64 वर्णमाला का उपयोग अनिवार्य है

I2P Base64 वर्णमाला, फ़ाइल सिस्टम और URL संगतता सुनिश्चित करने के लिए `+` और `/` की जगह `-` और `~` का उपयोग करती है, इसलिए यह मानक Base64 से भिन्न है।

### क्रिप्टोग्राफिक हस्ताक्षर

हस्ताक्षर बाइट 0 से लेकर सामग्री अनुभाग के अंत तक पूरी फ़ाइल को कवर करता है। स्वयं हस्ताक्षर सामग्री के बाद जोड़ा जाता है।

#### हस्ताक्षर एल्गोरिदम (RSA-4096-SHA512)

1. बाइट 0 से सामग्री के अंत तक का SHA-512 हैश निकालें
2. "raw" RSA का उपयोग करके हैश पर डिजिटल हस्ताक्षर करें (Java की शब्दावली में NONEwithRSA)
3. 512 बाइट तक पहुँचाने के लिए, आवश्यकता होने पर डिजिटल हस्ताक्षर को शुरुआत में शून्य जोड़कर पैड करें
4. 512-बाइट का डिजिटल हस्ताक्षर फ़ाइल के अंत में जोड़ें

#### हस्ताक्षर सत्यापन प्रक्रिया

क्लाइंटों को निम्नलिखित करना आवश्यक है:

1. हस्ताक्षर के प्रकार और लंबाई निर्धारित करने के लिए बाइट्स 0-11 पढ़ें
2. सामग्री की सीमाएँ पता लगाने के लिए पूरा हेडर पढ़ें
3. SHA-512 हैश की गणना करते हुए सामग्री को स्ट्रीम करें
4. फ़ाइल के अंत से डिजिटल हस्ताक्षर निकालें
5. हस्ताक्षरकर्ता की RSA-4096 सार्वजनिक कुंजी का उपयोग करके डिजिटल हस्ताक्षर सत्यापित करें
6. यदि डिजिटल हस्ताक्षर का सत्यापन विफल हो, तो फ़ाइल को अस्वीकार करें

### प्रमाणपत्र विश्वास मॉडल

Reseed साइनर कुंजियाँ RSA-4096 कुंजियों के साथ स्वहस्ताक्षरित X.509 प्रमाणपत्रों के रूप में वितरित की जाती हैं। ये प्रमाणपत्र I2P router पैकेजों में `certificates/reseed/` निर्देशिका में शामिल होते हैं।

प्रमाणपत्र प्रारूप: - **कुंजी प्रकार**: RSA-4096 - **हस्ताक्षर**: स्व-हस्ताक्षरित - **Subject CN (सामान्य नाम)**: SU3 हेडर में Signer ID से मेल खाना चाहिए - **वैधता तिथियाँ**: क्लाइंट्स को प्रमाणपत्र की वैधता अवधि का अनुपालन सुनिश्चित करना चाहिए

## Reseed Host चलाना (I2P नेटवर्क में आरंभिक नेटवर्क डेटा प्रदान करने वाला सर्वर)

reseed सेवा (नए routers को प्रारंभिक नेटवर्क समकक्ष उपलब्ध कराने वाली सेवा) का संचालन सुरक्षा, विश्वसनीयता, और नेटवर्क विविधता संबंधी आवश्यकताओं पर सावधानीपूर्वक ध्यान देने की मांग करता है। अधिक स्वतंत्र reseed होस्ट प्रतिरोधक क्षमता बढ़ाते हैं और आक्रमणकारियों या सेंसरों के लिए नए routers के जुड़ने को अवरुद्ध करना अधिक कठिन बना देते हैं।

### तकनीकी आवश्यकताएँ

#### सर्वर विनिर्देश

- **ऑपरेटिंग सिस्टम**: Unix/Linux (Ubuntu, Debian, FreeBSD परीक्षित और अनुशंसित)
- **कनेक्टिविटी**: स्थिर IPv4 पता आवश्यक, IPv6 अनुशंसित लेकिन वैकल्पिक
- **CPU**: न्यूनतम 2 कोर
- **RAM**: न्यूनतम 2 GB
- **बैंडविड्थ**: प्रति माह लगभग 15 GB
- **अपटाइम**: 24/7 संचालन आवश्यक
- **I2P Router**: अच्छी तरह से एकीकृत I2P router, जो लगातार चलता रहे

#### सॉफ़्टवेयर आवश्यकताएँ

- **Java**: JDK 8 या उससे नया (I2P 2.11.0 से Java 17+ आवश्यक होगा)
- **वेब सर्वर**: nginx या Apache, reverse proxy समर्थन के साथ (X-Forwarded-For हेडर की सीमाओं के कारण Lighttpd अब समर्थित नहीं है)
- **TLS/SSL**: मान्य TLS प्रमाणपत्र (Let's Encrypt, स्व-हस्ताक्षरित, या व्यावसायिक CA)
- **DDoS सुरक्षा**: fail2ban या समकक्ष (अनिवार्य, वैकल्पिक नहीं)
- **Reseed टूल्स**: https://i2pgit.org/idk/reseed-tools से आधिकारिक reseed-tools

### सुरक्षा आवश्यकताएँ

#### HTTPS/TLS कॉन्फ़िगरेशन

- **प्रोटोकॉल**: केवल HTTPS, HTTP पर कोई फॉलबैक नहीं
- **TLS संस्करण**: न्यूनतम TLS 1.2
- **साइफ़र सूट**: Java 8+ के साथ संगत मज़बूत सिफरों का समर्थन होना चाहिए
- **प्रमाणपत्र CN/SAN (कॉमन नेम/सब्जेक्ट अल्टरनेटिव नेम)**: सर्व किए जा रहे URL के होस्टनेम से मेल खाना चाहिए
- **प्रमाणपत्र प्रकार**: यदि डेव टीम को सूचित किया गया हो तो स्व-हस्ताक्षरित हो सकता है, या मान्यता प्राप्त CA द्वारा जारी

#### प्रमाणपत्र प्रबंधन

SU3 हस्ताक्षर प्रमाणपत्र और TLS प्रमाणपत्र अलग उद्देश्यों की पूर्ति करते हैं:

- **TLS प्रमाणपत्र** (`certificates/ssl/`): HTTPS ट्रांसपोर्ट को सुरक्षित करता है
- **SU3 (I2P में हस्ताक्षरित अपडेट/रीसीड फाइल का फॉर्मेट) हस्ताक्षर प्रमाणपत्र** (`certificates/reseed/`): रीसीड बंडलों पर हस्ताक्षर करता है

router पैकेजों में शामिल करने के लिए दोनों प्रमाणपत्रों को reseed (प्रारंभिक नोड-सूची उपलब्ध कराने की प्रक्रिया) समन्वयक (zzz@mail.i2p) को प्रदान किया जाना चाहिए।

#### DDoS और स्क्रैपिंग सुरक्षा

Reseed servers (रीसीड सर्वर—नेटवर्क में नए नोड्स को प्रारंभिक पीयर और नेटवर्क जानकारी प्रदान करने वाले सर्वर) को समय-समय पर त्रुटिपूर्ण कार्यान्वयनों, बॉटनेट्स, और नेटवर्क डेटाबेस को स्क्रैप करने का प्रयास करने वाले दुर्भावनापूर्ण तत्वों से हमलों का सामना करना पड़ता है। सुरक्षा उपायों में शामिल हैं:

- **fail2ban**: rate limiting (दर-सीमांकन) और हमले के शमन के लिए आवश्यक
- **Bundle Diversity** (बंडल विविधता): विभिन्न अनुरोधकर्ताओं को अलग-अलग RouterInfo सेट प्रदान करें
- **Bundle Consistency** (बंडल स्थिरता): उसी IP से दोहराए गए अनुरोधों के लिए, कॉन्फ़िगर योग्य समय-विंडो के भीतर वही बंडल प्रदान करें
- **IP लॉगिंग प्रतिबंध**: लॉग या IP पतों को सार्वजनिक न करें (गोपनीयता नीति की आवश्यकता)

### कार्यान्वयन विधियाँ

#### विधि 1: आधिकारिक reseed-tools (अनुशंसित)

I2P परियोजना द्वारा देखरेख किया जाने वाला प्रामाणिक कार्यान्वयन। रेपोजिटरी: https://i2pgit.org/idk/reseed-tools

**स्थापना**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
पहली बार चलाने पर, टूल उत्पन्न करेगा: - `your-email@mail.i2p.crt` (SU3 साइनिंग प्रमाणपत्र) - `your-email@mail.i2p.pem` (SU3 साइनिंग निजी कुंजी) - `your-email@mail.i2p.crl` (प्रमाणपत्र रद्दीकरण सूची) - TLS प्रमाणपत्र और कुंजी फ़ाइलیں

**विशेषताएँ**: - स्वचालित SU3 bundle (I2P अपडेट पैकेज फ़ॉर्मैट) जनरेशन (350 विविधताएँ, प्रत्येक में 77 RouterInfos (I2P router की जानकारी रिकॉर्ड)) - बिल्ट-इन HTTPS सर्वर - cron के माध्यम से हर 9 घंटे में कैश का पुनर्निर्माण - X-Forwarded-For हेडर के लिए `--trustProxy` फ्लैग के साथ समर्थन - reverse proxy कॉन्फ़िगरेशन के साथ संगत

**प्रोडक्शन परिनियोजन**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### विधि 2: Python कार्यान्वयन (pyseeder)

PurpleI2P परियोजना द्वारा वैकल्पिक कार्यान्वयन: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### विधि 3: Docker परिनियोजन

कंटेनरीकृत परिवेशों के लिए, कई Docker के लिए तैयार कार्यान्वयन उपलब्ध हैं:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Tor onion service (Tor नेटवर्क पर छिपी सेवा) और IPFS (विकेन्द्रीकृत फाइल सिस्टम) का समर्थन जोड़ता है

### रिवर्स प्रॉक्सी विन्यास

#### nginx कॉन्फ़िगरेशन

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Apache कॉन्फ़िगरेशन

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### पंजीकरण और समन्वय

अपने reseed server (I2P में नए इंस्टॉलेशन को प्रारंभिक netDb डेटा देने वाला सर्वर) को आधिकारिक I2P पैकेज में शामिल करने के लिए:

1. सेटअप और परीक्षण पूरा करें
2. दोनों प्रमाणपत्र (SU3 signing और TLS) reseed coordinator (रीसीड समन्वयक) को भेजें
3. संपर्क: zzz@mail.i2p या zzz@i2pmail.org
4. अन्य ऑपरेटरों के साथ समन्वय के लिए IRC2P पर #i2p-dev से जुड़ें

### संचालन संबंधी सर्वोत्तम प्रथाएँ

#### निगरानी और लॉगिंग

- आँकड़ों के लिए Apache/nginx के combined log format (संयुक्त लॉग फ़ॉर्मेट) को सक्षम करें
- log rotation (लॉग फ़ाइलों का रोलओवर) लागू करें (लॉग तेज़ी से बढ़ते हैं)
- बंडल निर्माण की सफलता और पुनर्निर्माण समय की निगरानी करें
- बैंडविड्थ उपयोग और अनुरोध पैटर्न को ट्रैक करें
- IP पते या विस्तृत प्रवेश लॉग कभी सार्वजनिक न करें

#### रखरखाव समय-сारणी

- **हर 9 घंटे**: SU3 bundle cache (SU3 बंडल कैश) को पुनर्निर्मित करें (cron के माध्यम से स्वचालित)
- **साप्ताहिक**: हमलों के पैटर्न के लिए लॉग की समीक्षा करें
- **मासिक**: I2P router और reseed-tools (reseed उपकरण) को अपडेट करें
- **आवश्यकतानुसार**: TLS प्रमाणपत्र नवीनीकृत करें (Let's Encrypt के साथ स्वचालित करें)

#### पोर्ट चयन

- डिफ़ॉल्ट: 8443 (अनुशंसित)
- वैकल्पिक: 1024-49151 के बीच कोई भी पोर्ट
- पोर्ट 443: root विशेषाधिकार या पोर्ट फ़ॉरवर्डिंग की आवश्यकता होती है (iptables redirect अनुशंसित)

पोर्ट फ़ॉरवर्डिंग का उदाहरण:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## वैकल्पिक Reseed (I2P नेटवर्क से आरंभिक router जानकारी प्राप्त करने की प्रक्रिया) विधियाँ

अन्य bootstrap (प्रारंभिक सेटअप) विकल्प प्रतिबंधात्मक नेटवर्कों के पीछे मौजूद उपयोगकर्ताओं की मदद करते हैं:

### फ़ाइल-आधारित reseed (प्रारंभिक netDb डेटा आयात)

संस्करण 0.9.16 में पेश किया गया, फाइल-आधारित reseeding (नेटवर्क से प्रारंभिक peers/जानकारी प्राप्त करने की प्रक्रिया) उपयोगकर्ताओं को RouterInfo (router की जानकारी वाला रिकॉर्ड) बंडलों को मैन्युअल रूप से लोड करने की अनुमति देता है। यह विधि विशेष रूप से उन उपयोगकर्ताओं के लिए उपयोगी है जो सेंसरशिप वाले क्षेत्रों में हैं, जहाँ HTTPS reseed servers अवरुद्ध होते हैं।

**प्रक्रिया**: 1. एक विश्वसनीय संपर्क अपने router का उपयोग करके एक SU3 बंडल तैयार करता है 2. बंडल को ईमेल, USB ड्राइव, या किसी अन्य out-of-band channel (मुख्य चैनल से अलग संचार माध्यम) के माध्यम से स्थानांतरित किया जाता है 3. उपयोगकर्ता `i2pseeds.su3` को I2P कॉन्फ़िगरेशन डायरेक्टरी में रखता है 4. रीस्टार्ट पर Router स्वचालित रूप से बंडल का पता लगाता है और उसे प्रोसेस करता है

**प्रलेखन**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**उपयोग के मामले**: - reseed servers (I2P में प्रारंभिक बूटस्ट्रैप/पीयर-खोज सर्वर) को ब्लॉक करने वाले राष्ट्रीय फायरवॉल के पीछे के उपयोगकर्ता - manual bootstrap की आवश्यकता वाले पृथक नेटवर्क - परीक्षण और विकास पर्यावरण

### Cloudflare द्वारा प्रॉक्सी किया गया रीसीडिंग (I2P नेटवर्क में प्रारंभिक जुड़ने की प्रक्रिया)

Cloudflare के CDN के माध्यम से reseed (नेटवर्क में प्रारम्भिक नोड-सूची प्राप्त करने की प्रक्रिया) ट्रैफ़िक को रूट करना उच्च सेंसरशिप वाले क्षेत्रों में संचालकों के लिए कई लाभ प्रदान करता है।

**लाभ**: - क्लाइंट्स से मूल सर्वर का IP पता छिपा रहता है - Cloudflare के बुनियादी ढांचे के माध्यम से DDoS सुरक्षा - edge caching (नेटवर्क के किनारे पर कैशिंग) के माध्यम से भौगोलिक लोड वितरण - वैश्विक क्लाइंट्स के लिए बेहतर प्रदर्शन

**कार्यान्वयन आवश्यकताएँ**: - `--trustProxy` फ्लैग reseed-tools में सक्रिय - DNS रिकॉर्ड के लिए Cloudflare प्रॉक्सी सक्रिय - X-Forwarded-For हेडर का उचित प्रबंधन

**महत्वपूर्ण विचारणीय बातें**: - Cloudflare पोर्ट प्रतिबंध लागू होते हैं (समर्थित पोर्ट का ही उपयोग करना होगा) - समान-क्लाइंट बंडल में संगति बनाए रखने के लिए X-Forwarded-For का समर्थन आवश्यक है - SSL/TLS विन्यास Cloudflare द्वारा प्रबंधित किया जाता है

**प्रलेखन**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### सेंसरशिप-प्रतिरोधी रणनीतियाँ

Nguyen Phong Hoang (USENIX FOCI 2019) के शोध में सेंसरशुदा नेटवर्क के लिए अतिरिक्त bootstrap methods (नेटवर्क तक प्रारंभिक पहुँच स्थापित करने की विधियाँ) की पहचान की गई है:

#### क्लाउड स्टोरेज सेवा प्रदाता

- **Box, Dropbox, Google Drive, OneDrive**: सार्वजनिक लिंक पर SU3 फ़ाइलें (I2P पैकेज फ़ाइलें) होस्ट करें
- **फ़ायदा**: वैध सेवाओं को बाधित किए बिना इन्हें ब्लॉक करना कठिन है
- **सीमा**: उपयोगकर्ताओं को URL मैन्युअल रूप से वितरित करने की आवश्यकता होती है

#### IPFS (एक विकेन्द्रीकृत पीयर-टू-पीयर फ़ाइल प्रणाली) वितरण

- InterPlanetary File System (IPFS, विकेन्द्रीकृत कंटेंट-ऐड्रेस्ड स्टोरेज नेटवर्क) पर रीसीड बंडल्स होस्ट करें
- कंटेंट-ऐड्रेस्ड स्टोरेज छेड़छाड़ को रोकता है
- टेकडाउन प्रयासों के प्रति प्रतिरोधी

#### Tor की ओनियन सेवाएँ

- Reseed सर्वर (I2P में प्रारंभिक नेटवर्क डेटा उपलब्ध कराने वाले) .onion पतों के माध्यम से सुलभ
- IP-आधारित ब्लॉकिंग के प्रति प्रतिरोधी
- उपयोगकर्ता के सिस्टम पर Tor क्लाइंट आवश्यक है

**शोध प्रलेखन**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### ज्ञात I2P ब्लॉकिंग वाले देश

2025 तक, निम्नलिखित देशों द्वारा I2P reseed servers (I2P नेटवर्क से प्रारंभिक रूप से जुड़ने के लिए आवश्यक डेटा प्रदान करने वाले सर्वर) को अवरुद्ध किए जाने की पुष्टि हुई है:
- चीन
- ईरान
- ओमान
- कतर
- कुवैत

इन क्षेत्रों के उपयोगकर्ताओं को वैकल्पिक bootstrap methods (नेटवर्क से प्रारंभिक कनेक्शन स्थापित करने की विधियाँ) या सेंसरशिप-प्रतिरोधी reseeding रणनीतियाँ (reseeding: netDb के लिए प्रारंभिक नोड/डेटा प्राप्त करने की रणनीतियाँ) का उपयोग करना चाहिए।

## कार्यान्वयनकर्ताओं के लिए प्रोटोकॉल विवरण

### Reseed (I2P नेटवर्क बूटस्ट्रैप) अनुरोध विनिर्देश

#### क्लाइंट का व्यवहार

1. **सर्वर चयन**: Router एक हार्डकोडेड reseed (प्रारंभिक नेटवर्क डेटा) URLs की सूची बनाए रखता है
2. **यादृच्छिक चयन**: क्लाइंट उपलब्ध सूची से सर्वर को यादृच्छिक रूप से चुनता है
3. **अनुरोध प्रारूप**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: सामान्य ब्राउज़रों की नकल करनी चाहिए (उदा., "Wget/1.11.4")
5. **पुनः प्रयास लॉजिक**: यदि SU3 अनुरोध विफल हो, तो इंडेक्स पेज पार्सिंग पर वापस जाएँ
6. **प्रमाणपत्र सत्यापन**: TLS प्रमाणपत्र को सिस्टम ट्रस्ट स्टोर के साथ सत्यापित करें
7. **SU3 हस्ताक्षर सत्यापन**: हस्ताक्षर को ज्ञात reseed प्रमाणपत्रों के साथ सत्यापित करें

#### सर्वर का व्यवहार

1. **बंडल चयन**: netDb से RouterInfos (router की जानकारी रिकॉर्ड) का छद्म-यादृच्छिक उपसमुच्चय चुनें
2. **क्लाइंट ट्रैकिंग**: स्रोत IP द्वारा अनुरोधों की पहचान करें (X-Forwarded-For को ध्यान में रखते हुए)
3. **बंडल स्थिरता**: समय-खिड़की के भीतर दोहराए गए अनुरोधों को वही बंडल लौटाएँ (आमतौर पर 8–12 घंटे)
4. **बंडल विविधता**: नेटवर्क विविधता के लिए अलग-अलग क्लाइंट्स को अलग-अलग बंडल लौटाएँ
5. **Content-Type**: `application/octet-stream` या `application/x-i2p-reseed`

### RouterInfo फ़ाइल प्रारूप

reseed bundle (प्रारंभिक बीज पैकेज) में प्रत्येक `.dat` फ़ाइल में एक RouterInfo संरचना (router सूचना की संरचना) होती है:

**फ़ाइल नामकरण**: `routerInfo-{base64-hash}.dat` - हैश 44 वर्णों का होता है और I2P base64 वर्णमाला का उपयोग करता है - उदाहरण: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**फ़ाइल सामग्री**: - RouterIdentity (router हैश, एन्क्रिप्शन कुंजी, हस्ताक्षर कुंजी) - प्रकाशन समय-चिह्न - Router पते (IP, पोर्ट, ट्रांसपोर्ट प्रकार) - Router क्षमताएँ और विकल्प - उपर्युक्त सभी डेटा को कवर करने वाला हस्ताक्षर

### नेटवर्क विविधता आवश्यकताएँ

नेटवर्क के केंद्रीकरण को रोकने और Sybil attack (कई नकली पहचानें बनाकर किया जाने वाला हमला) का पता लगाने को सक्षम करने के लिए:

- **पूर्ण NetDb डंप नहीं**: किसी एकल क्लाइंट को सभी RouterInfos कभी न प्रदान करें
- **यादृच्छिक सैंपलिंग**: हर बंडल में उपलब्ध पीयर्स का अलग-अलग उपसमुच्चय होता है
- **न्यूनतम बंडल आकार**: 75 RouterInfos (राउटर जानकारी रिकॉर्ड) (मूल 50 से बढ़ाया गया)
- **अधिकतम बंडल आकार**: 100 RouterInfos
- **नवीनता**: RouterInfos हाल के होने चाहिए (उत्पन्न होने के 24 घंटों के भीतर)

### IPv6 संबंधी विचार

**वर्तमान स्थिति** (2025): - कई reseed सर्वर (आरंभिक पीयर सूची प्रदान करने वाले) IPv6 पर अनुत्तरदायी हैं - क्लाइंट्स को विश्वसनीयता के लिए IPv4 को प्राथमिकता देनी चाहिए या उसे अनिवार्य करना चाहिए - नए परिनियोजन के लिए IPv6 समर्थन की सिफारिश की जाती है, पर यह अत्यावश्यक नहीं है

**कार्यान्वयन टिप्पणी**: dual-stack servers (ऐसे सर्वर जो IPv4 और IPv6 दोनों का समर्थन करते हैं) को कॉन्फ़िगर करते समय, यह सुनिश्चित करें कि IPv4 और IPv6 दोनों के लिसन पते सही ढंग से कार्य कर रहे हों, या यदि IPv6 का उचित रूप से समर्थन नहीं किया जा सकता, तो उसे निष्क्रिय कर दें।

## सुरक्षा संबंधी विचार

### धमकी मॉडल

reseed protocol (I2P नेटवर्क में netDb के लिए प्रारंभिक डेटा प्राप्त करने की प्रक्रिया) निम्न से बचाव करता है:

1. **मैन-इन-द-मिडल हमले**: RSA-4096 हस्ताक्षर बंडल से छेड़छाड़ को रोकते हैं
2. **नेटवर्क विभाजन**: कई स्वतंत्र रीसीड सर्वर एकल नियंत्रण बिंदु बनने से रोकते हैं
3. **सिबिल हमले**: बंडल की विविधता हमलावर की उपयोगकर्ताओं को अलग-थलग करने की क्षमता को सीमित करती है
4. **सेंसरशिप**: कई सर्वर और वैकल्पिक विधियाँ अतिरिक्तता प्रदान करते हैं

reseed प्रोटोकॉल निम्न के विरुद्ध सुरक्षा प्रदान नहीं करता:

1. **समझौता किए गए reseed servers (I2P नेटवर्क में प्रारम्भिक peers की सूची देने वाले सर्वर)**: यदि हमलावर reseed प्रमाणपत्र की निजी कुंजियों पर नियंत्रण कर ले
2. **पूर्ण नेटवर्क ब्लॉकिंग**: यदि किसी क्षेत्र में सभी reseed विधियाँ ब्लॉक कर दी जाएँ
3. **दीर्घकालिक निगरानी**: Reseed अनुरोध I2P में शामिल होने का प्रयास करने वाले IP पते का खुलासा करते हैं

### प्रमाणपत्र प्रबंधन

**निजी कुंजी सुरक्षा**: - प्रयोग में न होने पर SU3 signing keys (SU3 फ़ाइलों को प्रमाणित करने वाली हस्ताक्षर कुंजियाँ) को ऑफ़लाइन रखें - कुंजी एन्क्रिप्शन के लिए मज़बूत पासवर्ड का उपयोग करें - कुंजियों और प्रमाणपत्रों के सुरक्षित बैकअप बनाए रखें - उच्च-मूल्य परिनियोजन के लिए hardware security modules (HSMs) (हार्डवेयर सुरक्षा मॉड्यूल—विशेषीकृत क्रिप्टोग्राफ़िक डिवाइस) पर विचार करें

**प्रमाणपत्र निरस्तीकरण**: - प्रमाणपत्र निरस्तीकरण सूचियाँ (CRLs) समाचार फ़ीड के माध्यम से वितरित की जाती हैं - समझौता-ग्रस्त प्रमाणपत्रों को समन्वयक द्वारा निरस्त किया जा सकता है - Routers सॉफ़्टवेयर अपडेट के साथ CRLs को स्वतः अद्यतन करते हैं

### हमले का शमन

**DDoS (वितरित सेवा अभाव) सुरक्षा**: - अत्यधिक अनुरोधों के लिए fail2ban नियम - वेब सर्वर स्तर पर दर-सीमा निर्धारण - प्रति IP पता कनेक्शन सीमाएँ - एक अतिरिक्त परत के लिए Cloudflare या इसी प्रकार का CDN (सामग्री वितरण नेटवर्क)

**स्क्रैपिंग की रोकथाम**: - अनुरोध करने वाले प्रत्येक IP के लिए अलग-अलग बंडल - प्रति IP समय-आधारित बंडल कैशिंग - ऐसे लॉगिंग पैटर्न जो स्क्रैपिंग प्रयासों का संकेत देते हैं - पहचाने गए हमलों पर अन्य ऑपरेटरों के साथ समन्वय

## परीक्षण और मान्यकरण

### अपने Reseed Server का परीक्षण

#### विधि 1: Router की नई स्थापना

1. एक साफ सिस्टम पर I2P इंस्टॉल करें
2. कॉन्फ़िगरेशन में अपना reseed URL (I2P में प्रारंभिक peers/नोड्स से जुड़ने हेतु बूटस्ट्रैप URL) जोड़ें
3. अन्य reseed URLs हटाएँ या अक्षम करें
4. router शुरू करें और सफल reseed के लिए लॉग्स की निगरानी करें
5. 5-10 मिनट के भीतर नेटवर्क से कनेक्शन सत्यापित करें

अपेक्षित लॉग आउटपुट:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### विधि 2: हस्तचालित SU3 सत्यापन

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### विधि 3: checki2p निगरानी

https://checki2p.com/reseed पर उपलब्ध सेवा सभी पंजीकृत I2P reseed (I2P में प्रारंभिक बूटस्ट्रैप प्रक्रिया) सर्वरों पर हर 4 घंटे में स्वचालित जाँच करती है। यह प्रदान करती है:

- उपलब्धता निगरानी
- प्रतिक्रिया समय मेट्रिक्स
- TLS (ट्रांसपोर्ट लेयर सिक्योरिटी) प्रमाणपत्र सत्यापन
- SU3 (I2P का पैकेज फ़ॉर्मेट) हस्ताक्षर सत्यापन
- ऐतिहासिक अपटाइम डेटा

जैसे ही आपका reseed (बूटस्ट्रैप सर्वर) I2P प्रोजेक्ट के साथ पंजीकृत हो जाता है, वह 24 घंटे के भीतर checki2p पर स्वतः दिखाई देने लगेगा।

### सामान्य समस्याओं का निवारण

**समस्या**: "हस्ताक्षर कुंजी पढ़ने में असमर्थ" पहली बार चलाने पर - **समाधान**: यह अपेक्षित है। नई कुंजियाँ उत्पन्न करने के लिए 'y' दर्ज करें।

**समस्या**: router हस्ताक्षर सत्यापित करने में विफल - **कारण**: प्रमाणपत्र router के trust store (विश्वसनीय प्रमाणपत्र संग्रह) में नहीं है - **समाधान**: प्रमाणपत्र को `~/.i2p/certificates/reseed/` निर्देशिका में रखें

**समस्या**: विभिन्न क्लाइंट्स को एक ही बंडल भेजा जा रहा है - **कारण**: X-Forwarded-For हेडर सही तरीके से फ़ॉरवर्ड नहीं हो रहा है - **समाधान**: `--trustProxy` सक्षम करें और रिवर्स प्रॉक्सी हेडर कॉन्फ़िगर करें

**समस्या**: "Connection refused" त्रुटियाँ - **कारण**: इंटरनेट से पोर्ट सुलभ नहीं - **समाधान**: फ़ायरवॉल नियम जाँचें, पोर्ट फ़ॉरवर्डिंग सत्यापित करें

**समस्या**: बंडल पुनर्निर्माण के दौरान उच्च CPU उपयोग - **कारण**: 350+ SU3 (I2P का साइन किया हुआ अपडेट फ़ाइल फ़ॉर्मेट) विविधताएँ उत्पन्न करते समय यह सामान्य व्यवहार है - **समाधान**: पर्याप्त CPU संसाधन सुनिश्चित करें, पुनर्निर्माण की आवृत्ति कम करने पर विचार करें

## संदर्भ जानकारी

### आधिकारिक दस्तावेज़ीकरण

- **Reseed (I2P नेटवर्क में प्रारंभिक peers उपलब्ध कराने की प्रक्रिया) योगदानकर्ताओं के लिए मार्गदर्शिका**: /guides/creating-and-running-an-i2p-reseed-server/
- **Reseed नीति आवश्यकताएँ**: /guides/reseed-policy/
- **SU3 विनिर्देश**: /docs/specs/updates/
- **Reseed टूल्स रिपॉज़िटरी**: https://i2pgit.org/idk/reseed-tools
- **Reseed टूल्स दस्तावेज़ीकरण**: https://eyedeekay.github.io/reseed-tools/

### वैकल्पिक कार्यान्वयन

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder (रीसीड सर्वर)**: https://github.com/torbjo/i2p-reseeder

### सामुदायिक संसाधन

- **I2P फ़ोरम**: https://i2pforum.net/
- **Gitea रिपॉजिटरी**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev (IRC2P पर)
- **स्थिति निगरानी**: https://checki2p.com/reseed

### संस्करण इतिहास

- **0.9.14** (2014): SU3 रीसीड फ़ॉर्मैट पेश किया गया
- **0.9.16** (2014): फ़ाइल-आधारित रीसीडिंग जोड़ी गई
- **0.9.42** (2019): Network ID क्वेरी पैरामीटर की आवश्यकता
- **2.0.0** (2022): SSU2 ट्रांसपोर्ट प्रोटोकॉल पेश किया गया
- **2.4.0** (2024): NetDB का आइसोलेशन और सुरक्षा में सुधार
- **2.6.0** (2024): I2P-over-Tor कनेक्शनों को ब्लॉक कर दिए गए
- **2.10.0** (2025): वर्तमान स्थिर रिलीज़ (सितंबर 2025 तक)

### हस्ताक्षर प्रकार संदर्भ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**रीसीड मानक**: Type 6 (RSA-SHA512-4096) रीसीड बंडलों के लिए आवश्यक है।

## आभार

नेटवर्क को सुलभ और लचीला बनाए रखने के लिए प्रत्येक reseed operator (जो नए router को नेटवर्क से जुड़ने हेतु प्रारंभिक जानकारी/सीड्स प्रदान करता है) को धन्यवाद। निम्नलिखित योगदानकर्ताओं और परियोजनाओं को विशेष सम्मान:

- **zzz**: लंबे समय से I2P डेवलपर और reseed (I2P नेटवर्क के प्रारम्भिक bootstrap की प्रक्रिया) समन्वयक
- **idk**: reseed-tools के वर्तमान मेंटेनर और रिलीज़ प्रबंधक
- **Nguyen Phong Hoang**: सेंसरशिप-प्रतिरोधी reseeding रणनीतियों पर शोध
- **PurpleI2P Team**: वैकल्पिक I2P कार्यान्वयन और उपकरण
- **checki2p**: reseed अवसंरचना के लिए स्वचालित निगरानी सेवा

I2P नेटवर्क की विकेन्द्रीकृत reseed (नेटवर्क से पहली बार जुड़ते समय आवश्यक प्रारम्भिक पीअर्स/नोड्स की सूची उपलब्ध कराने की प्रक्रिया) अवसंरचना दुनिया भर के दर्जनों संचालकों के सामूहिक प्रयास का प्रतिनिधित्व करती है, जो यह सुनिश्चित करती है कि स्थानीय सेंसरशिप या तकनीकी बाधाओं के बावजूद नए उपयोगकर्ता हमेशा नेटवर्क से जुड़ने का रास्ता खोज सकें।
