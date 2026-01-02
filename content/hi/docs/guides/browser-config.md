---
title: "वेब ब्राउज़र कॉन्फ़िगरेशन"
description: "लोकप्रिय ब्राउज़रों को डेस्कटॉप और Android पर I2P के HTTP/HTTPS प्रॉक्सी का उपयोग करने के लिए कॉन्फ़िगर करें"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: दस्तावेज़
---

यह गाइड दर्शाती है कि सामान्य ब्राउज़रों को I2P के built‑in HTTP proxy के माध्यम से ट्रैफ़िक भेजने के लिए कैसे कॉन्फ़िगर करें। इसमें Safari, Firefox, और Chrome/Chromium ब्राउज़रों के लिए विस्तृत चरण-दर-चरण निर्देश शामिल हैं।

**महत्वपूर्ण नोट्स**:

- I2P का डिफ़ॉल्ट HTTP प्रॉक्सी `127.0.0.1:4444` पर सुनता है।
- I2P, I2P नेटवर्क के अंदर ट्रैफ़िक की सुरक्षा करता है (.i2p साइट्स)।
- अपने ब्राउज़र को कॉन्फ़िगर करने से पहले सुनिश्चित करें कि आपका I2P router चल रहा है।

## Safari (macOS)

Safari macOS पर सिस्टम-वाइड प्रॉक्सी सेटिंग्स का उपयोग करता है।

### Step 1: Open Network Settings

1. **Safari** खोलें और **Safari → Settings** (या **Preferences**) पर जाएं
2. **Advanced** टैब पर क्लिक करें
3. **Proxies** सेक्शन में, **Change Settings...** पर क्लिक करें

यह आपके Mac की System Network Settings को खोलेगा।

![Safari Advanced Settings](/images/guides/browser-config/accessi2p_1.png)

### चरण 1: नेटवर्क सेटिंग्स खोलें

1. नेटवर्क सेटिंग्स में, **Web Proxy (HTTP)** के लिए चेकबॉक्स पर टिक करें
2. निम्नलिखित दर्ज करें:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. अपनी सेटिंग्स सहेजने के लिए **OK** पर क्लिक करें

![Safari Proxy Configuration](/images/guides/browser-config/accessi2p_2.png)

अब आप Safari में `.i2p` साइट्स ब्राउज़ कर सकते हैं!

**नोट**: ये प्रॉक्सी सेटिंग्स उन सभी एप्लिकेशन को प्रभावित करेंगी जो macOS सिस्टम प्रॉक्सी का उपयोग करते हैं। यदि आप I2P ब्राउज़िंग को अलग रखना चाहते हैं तो एक अलग यूज़र अकाउंट बनाने या केवल I2P के लिए एक अलग ब्राउज़र का उपयोग करने पर विचार करें।

## Firefox (Desktop)

Firefox के पास सिस्टम से स्वतंत्र अपनी स्वयं की प्रॉक्सी सेटिंग्स हैं, जो इसे समर्पित I2P ब्राउज़िंग के लिए आदर्श बनाती हैं।

### चरण 2: HTTP प्रॉक्सी कॉन्फ़िगर करें

1. ऊपरी दाएं कोने में **मेनू बटन** (☰) पर क्लिक करें
2. **Settings** चुनें

![Firefox Settings](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. सेटिंग्स सर्च बॉक्स में, **"proxy"** टाइप करें
2. **Network Settings** तक स्क्रॉल करें
3. **Settings...** बटन पर क्लिक करें

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### चरण 1: सेटिंग्स खोलें

1. **Manual proxy configuration** चुनें
2. निम्नलिखित दर्ज करें:
   - **HTTP Proxy**: `127.0.0.1` **Port**: `4444`
3. **SOCKS Host** को खाली छोड़ें (जब तक कि आपको विशेष रूप से SOCKS proxy की आवश्यकता न हो)
4. **Proxy DNS when using SOCKS** को केवल तभी चेक करें जब SOCKS proxy का उपयोग कर रहे हों
5. सहेजने के लिए **OK** पर क्लिक करें

![Firefox Manual Proxy Configuration](/images/guides/browser-config/accessi2p_5.png)

आप अब Firefox में `.i2p` साइटें ब्राउज़ कर सकते हैं!

**सुझाव**: I2P ब्राउज़िंग के लिए समर्पित एक अलग Firefox प्रोफ़ाइल बनाने पर विचार करें। इससे आपकी I2P ब्राउज़िंग नियमित ब्राउज़िंग से अलग रहती है। प्रोफ़ाइल बनाने के लिए, Firefox एड्रेस बार में `about:profiles` टाइप करें।

## Chrome / Chromium (Desktop)

Chrome और Chromium-आधारित ब्राउज़र (Brave, Edge, आदि) आमतौर पर Windows और macOS पर सिस्टम प्रॉक्सी सेटिंग्स का उपयोग करते हैं। यह गाइड Windows कॉन्फ़िगरेशन दिखाता है।

### चरण 2: प्रॉक्सी सेटिंग्स खोजें

1. ऊपर दाईं ओर **तीन बिंदु मेनू** (⋮) पर क्लिक करें
2. **Settings** चुनें

![Chrome Settings](/images/guides/browser-config/accessi2p_6.png)

### चरण 3: मैन्युअल प्रॉक्सी कॉन्फ़िगर करें

1. Settings सर्च बॉक्स में, **"proxy"** टाइप करें
2. **Open your computer's proxy settings** पर क्लिक करें

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

यह Windows Network & Internet सेटिंग्स को खोलेगा।

1. **Manual proxy setup** तक स्क्रॉल करें
2. **Set up** पर क्लिक करें

![Windows Proxy Setup](/images/guides/browser-config/accessi2p_8.png)

### चरण 1: Chrome सेटिंग्स खोलें

1. **Use a proxy server** को **On** पर टॉगल करें
2. निम्नलिखित दर्ज करें:
   - **Proxy IP address**: `127.0.0.1`
   - **Port**: `4444`
3. वैकल्पिक रूप से, **"Don't use the proxy server for addresses beginning with"** में अपवाद जोड़ें (जैसे, `localhost;127.*`)
4. **Save** पर क्लिक करें

![Chrome Proxy Configuration](/images/guides/browser-config/accessi2p_9.png)

अब आप Chrome में `.i2p` साइटों को ब्राउज़ कर सकते हैं!

**नोट**: ये सेटिंग्स Windows पर सभी Chromium-आधारित ब्राउज़रों और कुछ अन्य एप्लिकेशनों को प्रभावित करती हैं। इससे बचने के लिए, एक समर्पित I2P प्रोफ़ाइल के साथ Firefox का उपयोग करने पर विचार करें।

### चरण 2: प्रॉक्सी सेटिंग्स खोलें

Linux पर, आप सिस्टम सेटिंग्स बदलने से बचने के लिए proxy flags के साथ Chrome/Chromium को launch कर सकते हैं:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
या एक डेस्कटॉप लॉन्चर स्क्रिप्ट बनाएं:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
`--user-data-dir` फ्लैग I2P ब्राउज़िंग के लिए एक अलग Chrome प्रोफाइल बनाता है।

## Firefox (डेस्कटॉप)

आधुनिक "Fenix" Firefox बिल्ड डिफ़ॉल्ट रूप से about:config और एक्सटेंशन को सीमित करते हैं। IceRaven एक Firefox फोर्क है जो एक्सटेंशन के एक चयनित सेट को सक्षम करता है, जिससे प्रॉक्सी सेटअप सरल हो जाता है।

एक्सटेंशन-आधारित कॉन्फ़िगरेशन (IceRaven):

1) यदि आप पहले से IceRaven का उपयोग करते हैं, तो पहले ब्राउज़िंग इतिहास साफ़ करने पर विचार करें (Menu → History → Delete History)। 2) Menu → Add‑Ons → Add‑Ons Manager खोलें। 3) "I2P Proxy for Android and Other Systems" एक्सटेंशन इंस्टॉल करें। 4) ब्राउज़र अब I2P के माध्यम से proxy करेगा।

यह एक्सटेंशन pre-Fenix Firefox-आधारित ब्राउज़रों पर भी काम करता है यदि [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/) से इंस्टॉल किया जाए।

Firefox Nightly में व्यापक एक्सटेंशन समर्थन सक्षम करने के लिए एक अलग प्रक्रिया की आवश्यकता होती है [जो Mozilla द्वारा दस्तावेजीकृत है](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/)।

## Internet Explorer / Windows System Proxy

Windows पर, सिस्टम प्रॉक्सी डायलॉग IE पर लागू होता है और Chromium‑आधारित ब्राउज़र द्वारा उपयोग किया जा सकता है जब वे सिस्टम सेटिंग्स को इनहेरिट करते हैं।

1) "Network and Internet Settings" → "Proxy" खोलें। 2) "Use a proxy server for your LAN" सक्षम करें। 3) HTTP के लिए address `127.0.0.1`, port `4444` सेट करें। 4) वैकल्पिक रूप से "Bypass proxy server for local addresses" चेक करें।
