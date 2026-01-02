---
title: "I2P पर IRC"
description: "I2P IRC नेटवर्क, क्लाइंट, टनल, और सर्वर सेटअप के लिए संपूर्ण गाइड (2025 में अपडेट किया गया)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

**मुख्य बिंदु**

- I2P अपनी टनलों के माध्यम से IRC ट्रैफ़िक के लिए **end-to-end encryption** प्रदान करता है। IRC क्लाइंट में **SSL/TLS को निष्क्रिय करें** जब तक कि आप clearnet पर outproxy नहीं कर रहे हों।
- पूर्व-कॉन्फ़िगर किया गया **Irc2P** क्लाइंट tunnel डिफ़ॉल्ट रूप से **127.0.0.1:6668** पर सुनता है। अपने IRC क्लाइंट को उस एड्रेस और पोर्ट से कनेक्ट करें।
- "router‑provided TLS" शब्द का उपयोग न करें। "I2P's native encryption" या "end‑to‑end encryption" का उपयोग करें।

## त्वरित प्रारंभ (Java I2P)

1. **Hidden Services Manager** को `http://127.0.0.1:7657/i2ptunnel/` पर खोलें और सुनिश्चित करें कि **Irc2P** tunnel **चल रहा है**।
2. अपने IRC क्लाइंट में, **server** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **off** सेट करें।
3. कनेक्ट करें और `#i2p`, `#i2p-dev`, `#i2p-help` जैसे चैनल्स में शामिल हों।

**i2pd** उपयोगकर्ताओं (C++ राउटर) के लिए, `tunnels.conf` में एक क्लाइंट tunnel बनाएं (नीचे दिए गए उदाहरण देखें)।

## नेटवर्क और सर्वर

### IRC2P (main community network)

- Federated सर्वर: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`।
- **Irc2P** tunnel `127.0.0.1:6668` पर इनमें से किसी एक से स्वचालित रूप से कनेक्ट होता है।
- सामान्य चैनल: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`।

### Ilita network

- सर्वर: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`।
- प्राथमिक भाषाएं: रूसी और अंग्रेज़ी। कुछ होस्ट्स पर वेब फ्रंट-एंड उपलब्ध हैं।

## Client setup

### Recommended, actively maintained

- **WeeChat (टर्मिनल)** — मजबूत SOCKS समर्थन; स्क्रिप्ट करना आसान।
- **Pidgin (डेस्कटॉप)** — अभी भी रखरखाव में; Windows/Linux के लिए अच्छी तरह से काम करता है।
- **Thunderbird Chat (डेस्कटॉप)** — ESR 128+ में समर्थित।
- **The Lounge (सेल्फ-होस्टेड वेब)** — आधुनिक वेब क्लाइंट।

### IRC2P (मुख्य समुदाय नेटवर्क)

- **LimeChat** (मुफ्त, ओपन सोर्स)।
- **Textual** (App Store पर सशुल्क; बिल्ड करने के लिए सोर्स उपलब्ध)।

### Ilita नेटवर्क

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- प्रोटोकॉल: **IRC**
- सर्वर: **127.0.0.1**
- पोर्ट: **6668**
- एन्क्रिप्शन: **off**
- यूज़रनेम/निक: कोई भी

#### Thunderbird Chat

- खाता प्रकार: **IRC**
- सर्वर: **127.0.0.1**
- पोर्ट: **6668**
- SSL/TLS: **बंद**
- वैकल्पिक: कनेक्ट होने पर चैनल्स में स्वतः शामिल हों

#### Dispatch (SAM v3)

`config.toml` डिफ़ॉल्ट उदाहरण:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Irc2P क्लाइंट टनल: **127.0.0.1:6668** → अपस्ट्रीम सर्वर **port 6667** पर।
- Hidden Services Manager: `http://127.0.0.1:7657/i2ptunnel/`।

### अनुशंसित, सक्रिय रूप से रखरखाव किया गया

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Ilita के लिए अलग tunnel (उदाहरण):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### macOS विकल्प

- **SAM सक्षम करें** Java I2P में (डिफ़ॉल्ट रूप से बंद) `/configclients` या `clients.config` पर।
- डिफ़ॉल्ट: **127.0.0.1:7656/TCP** और **127.0.0.1:7655/UDP**।
- अनुशंसित क्रिप्टो: `SIGNATURE_TYPE=7` (Ed25519) और `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 with ElGamal fallback) या केवल `4` आधुनिक-मात्र के लिए।

### उदाहरण विन्यास

- Java I2P डिफ़ॉल्ट: **2 inbound / 2 outbound**।
- i2pd डिफ़ॉल्ट: **5 inbound / 5 outbound**।
- IRC के लिए: **2–3 प्रत्येक** पर्याप्त है; routers में सुसंगत व्यवहार के लिए स्पष्ट रूप से सेट करें।

## क्लाइंट सेटअप

- **आंतरिक I2P IRC कनेक्शन के लिए SSL/TLS सक्षम न करें**। I2P पहले से ही end‑to‑end एन्क्रिप्शन प्रदान करता है। अतिरिक्त TLS ओवरहेड जोड़ता है बिना गुमनामी लाभ के।
- स्थिर पहचान के लिए **persistent keys** का उपयोग करें; परीक्षण के अलावा हर रीस्टार्ट पर keys को पुनः उत्पन्न करने से बचें।
- यदि कई ऐप्स IRC का उपयोग करते हैं, तो क्रॉस-सर्विस सहसंबंध को कम करने के लिए **अलग tunnels** (गैर-साझा) को प्राथमिकता दें।
- यदि आपको रिमोट कंट्रोल (SAM/I2CP) की अनुमति देनी आवश्यक है, तो localhost पर bind करें और SSH tunnels या प्रमाणित reverse proxies के साथ एक्सेस को सुरक्षित करें।

## Alternative connection method: SOCKS5

कुछ क्लाइंट I2P के SOCKS5 proxy के माध्यम से कनेक्ट हो सकते हैं: **127.0.0.1:4447**। सर्वोत्तम परिणामों के लिए, 6668 पर एक समर्पित IRC क्लाइंट tunnel को प्राथमिकता दें; SOCKS एप्लिकेशन‑लेयर आइडेंटिफायर्स को sanitize नहीं कर सकता और यदि क्लाइंट anonymity के लिए डिज़ाइन नहीं किया गया है तो जानकारी लीक हो सकती है।

## Troubleshooting

- **कनेक्ट नहीं हो पा रहा** — सुनिश्चित करें कि Irc2P tunnel चल रहा है और router पूरी तरह से bootstrapped है।
- **Resolve/join पर रुक जाता है** — दोबारा जांचें कि SSL **disabled** है और client **127.0.0.1:6668** की ओर point कर रहा है।
- **High latency** — I2P डिज़ाइन से ही higher-latency है। Tunnel quantities को मध्यम (2–3) रखें और rapid reconnect loops से बचें।
- **SAM apps का उपयोग करते समय** — पुष्टि करें कि SAM enabled है (Java) या firewalled नहीं है (i2pd)। Long‑lived sessions की सिफारिश की जाती है।

## Appendix: Ports and naming

- सामान्य IRC टनल पोर्ट: **6668** (Irc2P डिफ़ॉल्ट), **6667** और **6669** वैकल्पिक के रूप में।
- `.b32.i2p` होस्टनेम: 52-अक्षर का मानक रूप; LS2/उन्नत सर्टिफिकेट के लिए विस्तारित 56+ अक्षर के रूप मौजूद हैं। `.i2p` होस्टनेम का उपयोग करें जब तक कि आपको स्पष्ट रूप से b32 एड्रेस की आवश्यकता न हो।
