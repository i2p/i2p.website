---
title: "डेबियन और उबंटू पर I2P इंस्टॉल करना"
aliases:
  - "/hi/debian"
  - "/hi/debian/"
description: "डेबियन, उबंटू, और उनके डेरिवेटिव्स पर आधिकारिक रिपॉजिटरीज का उपयोग करके I2P इंस्टॉल करने की संपूर्ण गाइड"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P प्रोजेक्ट Debian, Ubuntu, और उनके व्युत्पन्न वितरणों के लिए आधिकारिक पैकेज बनाए रखता है। यह गाइड हमारे आधिकारिक रिपॉजिटरी का उपयोग करके I2P इंस्टॉल करने के लिए व्यापक निर्देश प्रदान करती है।

मुझे खेद है, लेकिन आपने अनुवाद के लिए कोई पाठ प्रदान नहीं किया है। कृपया "---" के बाद अनुवाद के लिए अंग्रेजी पाठ प्रदान करें।

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
IMPORTANT: केवल अनुवाद प्रदान करें। प्रश्न न पूछें, स्पष्टीकरण प्रदान न करें, या कोई टिप्पणी न जोड़ें। भले ही पाठ केवल एक शीर्षक हो या अधूरा लगे, इसे जैसा है वैसा ही अनुवाद करें।

## Debian Installation

Debian और इसके downstream distributions (LMDE, Kali Linux, ParrotOS, Knoppix, आदि) को `deb.i2p.net` पर आधिकारिक I2P Debian repository का उपयोग करना चाहिए।

1. [I2P Router Console](http://127.0.0.1:7657/) खोलें
2. [Network Configuration page](http://127.0.0.1:7657/confignet) पर जाएं
3. सूचीबद्ध पोर्ट नंबरों को नोट करें (आमतौर पर 9000-31000 के बीच यादृच्छिक पोर्ट)
4. अपने router/firewall में इन UDP और TCP पोर्ट्स को forward करें

**`deb.i2p2.de` और `deb.i2p2.no` पर हमारे पुराने repositories का जीवनकाल समाप्त हो चुका है।** यदि आप इन legacy repositories का उपयोग कर रहे हैं, तो कृपया `deb.i2p.net` पर नए repository में माइग्रेट करने के लिए नीचे दिए गए निर्देशों का पालन करें।

नीचे दिए गए सभी चरणों के लिए root एक्सेस की आवश्यकता है। या तो `su` के साथ root उपयोगकर्ता पर स्विच करें, या प्रत्येक कमांड के साथ `sudo` उपसर्ग (prefix) लगाएं।

## Post-Installation Configuration

**चरण 1: आवश्यक पैकेज इंस्टॉल करें**

1. [Configuration page](http://127.0.0.1:7657/config.jsp) पर जाएं
2. bandwidth settings अनुभाग खोजें
3. डिफ़ॉल्ट सेटिंग्स 96 KB/s download / 40 KB/s upload हैं
4. यदि आपके पास तेज़ इंटरनेट है तो इन्हें बढ़ाएं (उदाहरण के लिए, सामान्य ब्रॉडबैंड कनेक्शन के लिए 250 KB/s down / 100 KB/s up)

सुनिश्चित करें कि आपके पास आवश्यक टूल इंस्टॉल हैं:

## Debian इंस्टॉलेशन

ये पैकेज सुरक्षित HTTPS रिपॉजिटरी एक्सेस, डिस्ट्रिब्यूशन डिटेक्शन और फ़ाइल डाउनलोड को सक्षम करते हैं।

### Important Notice

**चरण 2: I2P रिपॉजिटरी जोड़ें**

आपके द्वारा उपयोग किया जाने वाला command आपके Debian संस्करण पर निर्भर करता है। सबसे पहले, यह निर्धारित करें कि आप कौन सा संस्करण चला रहे हैं:

इसे [Debian release information](https://wiki.debian.org/LTS/) के साथ cross-reference करें ताकि आपके distribution codename (जैसे, Bookworm, Bullseye, Buster) की पहचान की जा सके।

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
**डेबियन बुल्सआई (11) या नए संस्करण के लिए:**

**Debian व्युत्पन्न (LMDE, Kali, ParrotOS, इत्यादि) के लिए Bullseye-समतुल्य या नए संस्करण पर:**

**Debian Buster (10) या पुराने संस्करणों के लिए:**

```bash
sudo apt-get update
```
**Buster-समकक्ष या पुराने पर Debian व्युत्पन्न के लिए:**

**चरण 3: रिपॉजिटरी साइनिंग की डाउनलोड करें**

**चरण 4: कुंजी फिंगरप्रिंट सत्यापित करें**

```bash
sudo apt-get install i2p
```
कुंजी पर भरोसा करने से पहले, सत्यापित करें कि इसका फिंगरप्रिंट आधिकारिक I2P साइनिंग कुंजी से मेल खाता है:

### Prerequisites

**सत्यापित करें कि आउटपुट में यह फ़िंगरप्रिंट दिखाई दे रहा है:**

⚠️ **यदि फ़िंगरप्रिंट मेल नहीं खाता है तो आगे न बढ़ें।** यह एक समझौता किए गए डाउनलोड का संकेत हो सकता है।

**चरण 5: रिपॉजिटरी की इंस्टॉल करें**

सत्यापित keyring को सिस्टम keyrings डायरेक्टरी में कॉपी करें:

**केवल Debian Buster या पुराने संस्करणों के लिए**, आपको एक symlink भी बनाना होगा:

**चरण 6: पैकेज सूचियों को अपडेट करें**

अपने सिस्टम के पैकेज डेटाबेस को I2P रिपॉजिटरी को शामिल करने के लिए रिफ्रेश करें:

**चरण 7: I2P इंस्टॉल करें**

I2P router और keyring package दोनों को इंस्टॉल करें (जो सुनिश्चित करता है कि आपको भविष्य में key updates प्राप्त हों):

```
ppa:i2p-maintainers/i2p
```
बढ़िया! I2P अब इंस्टॉल हो गया है। [Post-Installation Configuration](#post-installation-configuration) सेक्शन पर जारी रखें।

---

मुझे खेद है, लेकिन आपने अनुवाद करने के लिए कोई पाठ प्रदान नहीं किया है। केवल "---" (विभाजक रेखाएं) हैं। कृपया अनुवाद करने के लिए वास्तविक अंग्रेजी पाठ प्रदान करें।

I2P इंस्टॉल करने के बाद, आपको router शुरू करना होगा और कुछ प्रारंभिक कॉन्फ़िगरेशन करना होगा।

I2P पैकेज I2P राउटर चलाने के तीन तरीके प्रदान करते हैं:

जरूरत पड़ने पर `i2prouter` स्क्रिप्ट का उपयोग करके I2P को मैन्युअली शुरू करें:

**महत्वपूर्ण**: `sudo` का उपयोग **न करें** या इसे root के रूप में न चलाएं! I2P को आपके सामान्य उपयोगकर्ता के रूप में चलना चाहिए।

I2P को रोकने के लिए:

यदि आप एक non-x86 सिस्टम पर हैं या Java Service Wrapper आपके प्लेटफ़ॉर्म पर काम नहीं करता है, तो उपयोग करें:

## Next Steps

फिर से, `sudo` का उपयोग **न** करें या root के रूप में न चलाएं।

### विधि 1: कमांड लाइन इंस्टॉलेशन (अनुशंसित)

सर्वोत्तम अनुभव के लिए, I2P को अपने सिस्टम के बूट होने पर स्वचालित रूप से शुरू होने के लिए कॉन्फ़िगर करें, लॉगिन से पहले भी:

### विधि 2: Software Center GUI का उपयोग करना

यह एक कॉन्फ़िगरेशन डायलॉग खोलता है। I2P को सिस्टम सर्विस के रूप में सक्षम करने के लिए "Yes" चुनें।

### Initial Router Configuration

**यह अनुशंसित विधि है** क्योंकि: - I2P बूट पर स्वचालित रूप से शुरू होता है - आपका router बेहतर नेटवर्क एकीकरण बनाए रखता है - आप नेटवर्क स्थिरता में योगदान करते हैं - I2P तुरंत उपलब्ध होता है जब आपको इसकी आवश्यकता हो

पहली बार I2P शुरू करने के बाद, नेटवर्क में एकीकृत होने में कई मिनट लगेंगे। इस बीच, इन आवश्यक सेटिंग्स को कॉन्फ़िगर करें:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
इष्टतम प्रदर्शन और नेटवर्क भागीदारी के लिए, अपने NAT/firewall के माध्यम से I2P ports को forward करें:

यदि आपको port forwarding में सहायता की आवश्यकता है, तो [portforward.com](https://portforward.com) राउटर-विशिष्ट गाइड प्रदान करता है।

डिफ़ॉल्ट बैंडविड्थ सेटिंग्स रूढ़िवादी हैं। अपने इंटरनेट कनेक्शन के आधार पर उन्हें समायोजित करें:

```bash
cat /etc/debian_version
```
**नोट**: अधिक लिमिट सेट करने से नेटवर्क को मदद मिलती है और आपकी अपनी परफॉर्मेंस में सुधार होता है।

I2P साइट्स (eepsites) और सेवाओं तक पहुँचने के लिए, अपने ब्राउज़र को I2P के HTTP proxy का उपयोग करने के लिए कॉन्फ़िगर करें:

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Firefox, Chrome और अन्य ब्राउज़रों के लिए विस्तृत सेटअप निर्देशों के लिए हमारी [Browser Configuration Guide](/docs/guides/browser-config) देखें।

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
मुझे खेद है, लेकिन आपने अनुवाद के लिए कोई पाठ प्रदान नहीं किया है। कृपया "---" चिह्नों के बाद अंग्रेजी पाठ शामिल करें ताकि मैं इसे हिंदी में अनुवाद कर सकूं।

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
यदि इंस्टॉलेशन के दौरान आपको GPG key की त्रुटियां मिलती हैं:

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
यदि I2P अपडेट प्राप्त नहीं कर रहा है:

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
यदि आप पुराने `deb.i2p2.de` या `deb.i2p2.no` repositories का उपयोग कर रहे हैं:

अब जब I2P इंस्टॉल और चालू है:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
अदृश्य इंटरनेट में आपका स्वागत है!

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **अगर फिंगरप्रिंट मेल नहीं खाता है तो आगे न बढ़ें।** इसका अर्थ हो सकता है कि डाउनलोड संक्रमित है।

**चरण 5: रिपॉजिटरी कुंजी स्थापित करें**

सत्यापित कुंजी-वलय को सिस्टम कुंजी-वलय निर्देशिका में कॉपी करें:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**केवल डेबियन बस्टर या उससे पुराने संस्करण के लिए**, आपको एक सिमलिंक बनाने की भी आवश्यकता है:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**चरण 6: पैकेज सूचियों को अद्यतन करें**

I2P रिपॉजिटरी शामिल करने के लिए अपने सिस्टम के पैकेज डेटाबेस को ताज़ा करें:

```bash
sudo apt-get update
```
**चरण 7: आई2पी स्थापित करें**

I2P राउटर और कीरिंग पैकेज दोनों को स्थापित करें (जो भविष्य में कुंजी अद्यतन प्राप्त करना सुनिश्चित करता है):

```bash
sudo apt-get install i2p i2p-keyring
```
बहुत बढ़िया! I2P अब स्थापित हो गया है। [स्थापना के बाद का विन्यास](#post-installation-configuration) अनुभाग पर जारी रखें।

मुझे खेद है, लेकिन आपने अनुवाद के लिए कोई पाठ प्रदान नहीं किया है। कृपया "---" के बाद अनुवाद के लिए अंग्रेजी पाठ प्रदान करें।

## स्थापना के बाद कॉन्फ़िगरेशन

I2P स्थापित करने के बाद, आपको राउटर शुरू करना होगा और कुछ प्रारंभिक विन्यास करना होगा।

### महत्वपूर्ण सूचना

I2P पैकेज I2P राउटर चलाने के तीन तरीके प्रदान करते हैं:

#### Option 1: On-Demand (Basic)

आवश्यकता होने पर `i2prouter` स्क्रिप्ट का उपयोग करके मैन्युअल रूप से I2P शुरू करें:

```bash
i2prouter start
```
**महत्वपूर्ण**: `sudo` का उपयोग न करें या इसे रूट के रूप में न चलाएं! I2P को आपके सामान्य उपयोगकर्ता के रूप में चलाना चाहिए।

I2P को रोकने के लिए:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

यदि आप एक गैर-x86 सिस्टम पर हैं या जावा सर्विस रैपर आपके प्लेटफॉर्म पर काम नहीं करता है, तो इसका उपयोग करें:

```bash
i2prouter-nowrapper
```
फिर से, `sudo` का उपयोग न करें या रूट के रूप में चलाएं।

#### Option 3: System Service (Recommended)

सर्वोत्तम अनुभव के लिए, अपने सिस्टम के बूट होने पर, लॉगिन से पहले भी, I2P को स्वचालित रूप से शुरू करने के लिए कॉन्फ़िगर करें:

```bash
sudo dpkg-reconfigure i2p
```
यह एक विन्यास संवाद खोलता है। I2P को एक सिस्टम सेवा के रूप में सक्षम करने के लिए "हां" का चयन करें।

**यह अनुशंसित विधि है** क्योंकि: - बूट होते समय I2P स्वचालित रूप से शुरू हो जाता है - आपका राउटर बेहतर नेटवर्क एकीकरण बनाए रखता है - आप नेटवर्क स्थिरता में योगदान देते हैं - I2P तुरंत उपलब्ध होता है जब भी आपको इसकी आवश्यकता होती है

### पूर्वापेक्षाएँ

I2P को पहली बार शुरू करने के बाद, नेटवर्क में एकीकृत होने में कई मिनट लगेंगे। इस बीच, इन आवश्यक सेटिंग्स को कॉन्फ़िगर करें:

#### 1. Configure NAT/Firewall

अनुकूल प्रदर्शन और नेटवर्क भागीदारी के लिए, अपने NAT/फ़ायरवॉल के माध्यम से I2P पोर्ट्स को अग्रेषित करें:

- सुनिश्चित करें कि आप I2P को root के रूप में नहीं चला रहे हैं: `ps aux | grep i2p`
- लॉग्स जाँचें: `tail -f ~/.i2p/wrapper.log`
- सत्यापित करें कि Java इंस्टॉल है: `java -version`

यदि आपको पोर्ट फॉरवर्डिंग में सहायता की आवश्यकता है, तो [portforward.com](https://portforward.com) राउटर-विशिष्ट गाइड प्रदान करता है।

#### 2. Adjust Bandwidth Settings

डिफ़ॉल्ट बैंडविड्थ सेटिंग्स सावधानी भरी होती हैं। अपने इंटरनेट कनेक्शन के आधार पर उन्हें समायोजित करें:

1. कुंजी फ़िंगरप्रिंट को पुनः डाउनलोड और सत्यापित करें (ऊपर चरण 3-4)
2. सुनिश्चित करें कि keyring फ़ाइल में सही अनुमतियाँ हैं: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

**नोट**: उच्च सीमाएँ निर्धारित करने से नेटवर्क को सहायता मिलती है और आपके स्वयं के प्रदर्शन में सुधार होता है।

#### 3. Configure Your Browser

I2P साइटों (ईपीसाइट्स) और सेवाओं तक पहुंचने के लिए, अपने ब्राउज़र को I2P के HTTP प्रॉक्सी का उपयोग करने के लिए कॉन्फ़िगर करें:

फ़ायरफ़ॉक्स, क्रोम और अन्य ब्राउज़रों के लिए विस्तृत सेटअप निर्देशों के लिए हमारे [ब्राउज़र कॉन्फ़िगरेशन गाइड](/docs/guides/browser-config) देखें।

मुझे खेद है, लेकिन आपने अनुवाद के लिए कोई पाठ प्रदान नहीं किया है। कृपया "---" के बाद अनुवाद के लिए अंग्रेजी पाठ प्रदान करें।

## समस्या निवारण

### स्थापना चरण

1. रिपॉजिटरी कॉन्फ़िगर होने की पुष्टि करें: `cat /etc/apt/sources.list.d/i2p.list`
2. पैकेज लिस्ट अपडेट करें: `sudo apt-get update`
3. I2P अपडेट्स की जांच करें: `sudo apt-get upgrade`

### Migrating from old repositories

यदि स्थापना के दौरान आपको GPG कुंजी त्रुटियाँ प्राप्त होती हैं:

1. पुराने रिपॉजिटरी को हटाएं: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. ऊपर दिए गए [Debian Installation](#debian-installation) चरणों का पालन करें
3. अपडेट करें: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

### अपडेट काम नहीं कर रहे हैं

यदि I2P अपडेट प्राप्त नहीं कर रहा है:

- I2P साइटों तक पहुँचने के लिए [अपने ब्राउज़र को कॉन्फ़िगर करें](/docs/guides/browser-config)
- अपने router की निगरानी के लिए [I2P router console](http://127.0.0.1:7657/) देखें
- जानें कि आप कौन से [I2P applications](/docs/applications/) उपयोग कर सकते हैं
- नेटवर्क को समझने के लिए [I2P कैसे काम करता है](/docs/overview/tech-intro) के बारे में पढ़ें

### पुराने रिपॉजिटरी से माइग्रेट करना

यदि आप पुराने `deb.i2p2.de` या `deb.i2p2.no` रिपॉजिटरी का उपयोग कर रहे हैं:

1. पुरानी रिपॉजिटरी हटाएं: `sudo rm /etc/apt/sources.list.d/i2p.list`  
2. ऊपर दिए गए [डेबियन स्थापना](#debian-installation) चरणों का पालन करें  
3. अद्यतन करें: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

मुझे खेद है, लेकिन आपने अनुवाद के लिए कोई पाठ प्रदान नहीं किया है। कृपया "---" के बाद अनुवाद के लिए अंग्रेजी पाठ प्रदान करें।

## अगले कदम

अब जब I2P स्थापित है और चल रहा है:

- I2P साइट्स तक पहुँचने के लिए अपने ब्राउज़र को [कॉन्फ़िगर करें](/docs/guides/browser-config)
- अपने राउटर की निगरानी करने के लिए [I2P राउटर कंसोल](http://127.0.0.1:7657/) का पता करें
- [I2P एप्लिकेशन्स](/docs/applications/) के बारे में जानें जिनका आप उपयोग कर सकते हैं
- नेटवर्क को समझने के लिए जानें कि [I2P कैसे काम करता है](/docs/overview/tech-intro)

अदृश्य इंटरनेट में आपका स्वागत है!
