---
title: "I2PControl JSON-RPC"
description: "I2PControl webapp के माध्यम से रिमोट router प्रबंधन API"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# I2PControl API दस्तावेज़

-------------चेक ऐड स्टफ--------------

I2PControl एक **JSON-RPC 2.0** API है जो I2P router के साथ बंडल आती है (संस्करण 0.9.39 से)। यह structured JSON अनुरोधों के माध्यम से router की प्रमाणित निगरानी और नियंत्रण सक्षम करता है।

> **डिफ़ॉल्ट पासवर्ड:** `itoopie` — यह फैक्ट्री डिफ़ॉल्ट है और सुरक्षा के लिए इसे **तुरंत बदला जाना चाहिए**।

## 1. अवलोकन और पहुँच

| लागूकरण             | डिफ़ॉल्ट एंडपॉइंट                 | प्रोटोकॉल | डिफ़ॉल्ट रूप से सक्षम                             | टिप्पणियाँ                  |
|----------------------------|----------------------------------|----------|------------------------------------------------|------------------------|
| जावा I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP     | ❌ वेबएप्स के माध्यम से सक्षम करना होगा (राउटर कंसोल) | पैकेजबद्ध वेबएप्प         |
| i2pd (C++ लागूकरण)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ डिफ़ॉल्ट रूप से सक्षम                           | पुराने प्लगइन व्यवहार |
---

Java I2P के मामले में, आपको **Router Console → WebApps → I2PControl** में जाना होगा और इसे सक्षम करना होगा (स्वचालित रूप से शुरू होने के लिए सेट करें)। एक बार सक्रिय होने पर, सभी methods के लिए आवश्यक है कि आप पहले authenticate करें और session token प्राप्त करें।

## 2. JSON-RPC प्रारूप

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
सभी अनुरोध JSON-RPC 2.0 संरचना का पालन करते हैं:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
एक सफल प्रतिक्रिया में `result` फील्ड शामिल होता है; असफलता पर, एक `error` ऑब्जेक्ट वापस किया जाता है:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
या

## 3. प्रमाणीकरण प्रवाह

### अनुरोध (प्रमाणीकरण)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### सफल प्रतिक्रिया

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| फ़ील्ड      | दिशा      | प्रकार   | विवरण                                                    |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | अनुरोध   | long   | ग्राहक द्वारा अनुरोधित I2PControl API संस्करण। `1` का उपयोग करें। |
| `Password` | अनुरोध   | String | I2PControl के साथ प्रमाणीकरण के लिए उपयोग किया गया पासवर्ड।           |
| `API`      | प्रतिक्रिया  | long   | सर्वर द्वारा लागू प्राथमिक API संस्करण।           |
| `Token`    | प्रतिक्रिया  | String | बाद के अनुरोधों के लिए उपयोग किया जाने वाला प्रमाणीकरण टोकन।       |
---

आपको उस `Token` को सभी बाद के requests में `params` में शामिल करना होगा।

## 4. विधियां और एंडपॉइंट्स

### 4.1 RouterInfo

---

router के बारे में मुख्य टेलीमेट्री जानकारी प्राप्त करता है।

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**अनुरोध उदाहरण**

#### स्टेटस कोड Enum (`i2p.router.net.status`)

| कुंजी                                    | प्रकार   | विवरण                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | स्ट्रिंग | मुक्त-प्रारूप, अनुवादित राउटर स्थिति जिसे प्रदर्शित करने के लिए बनाया गया है।             |
| `i2p.router.uptime`                    | लंबा   | मिलीसेकंड में राउटर का अपटाइम। पुराने i2pd संस्करण स्ट्रिंग लौटा सकते हैं। |
| `i2p.router.version`                   | स्ट्रिंग | पूर्ण राउटर संस्करण।                                                    |
| `i2p.router.net.status`                | लंबा   | नेटवर्क स्थिति कोड; नीचे दी गई तालिका देखें।                               |
| `i2p.router.net.bw.inbound.1s`         | डबल | बाइट प्रति सेकंड में वर्तमान आगमन बैंडविड्थ।                          |
| `i2p.router.net.bw.inbound.15s`        | डबल | 15-सेकंड की औसत आगमन बैंडविड्थ, बाइट प्रति सेकंड में।                |
| `i2p.router.net.bw.outbound.1s`        | डबल | बाइट प्रति सेकंड में वर्तमान निर्गमन बैंडविड्थ।                         |
| `i2p.router.net.bw.outbound.15s`       | डबल | 15-सेकंड की औसत निर्गमन बैंडविड्थ, बाइट प्रति सेकंड में।               |
| `i2p.router.net.tunnels.participating` | लंबा   | टनलों की संख्या जिसमें यह राउटर भाग ले रहा है।                |
#### स्थिति कोड एन्यूम (`i2p.router.net.status`)

| कोड | अर्थ                                              |
|------|----------------------------------------------------|
| 0    | ठीक है                                             |
| 1    | परीक्षण किया जा रहा है                             |
| 2    | फायरवॉल के पीछे                                     |
| 3    | छिपा हुआ                                           |
| 4    | चेतावनी: फायरवॉल और तेज़                             |
| 5    | चेतावनी: फायरवॉल और फ्लडफिल                         |
| 6    | चेतावनी: आउटबाउंड TCP के साथ फायरवॉल             |
| 7    | चेतावनी: UDP अक्षम के साथ फायरवॉल                |
| 8    | I2CP त्रुटि                                        |
| 9    | घड़ी का अंतर (क्लॉक स्क्यू)                         |
| 10   | निजी TCP पते में त्रुटि                            |
| 11   | सममित NAT में त्रुटि                               |
| 12   | UDP पोर्ट उपयोग में है                              |
| 13   | कोई सक्रिय पीयर नहीं: कनेक्शन और फायरवॉल जांचें    |
| 14   | UDP अक्षम और TCP अनसेट है                          |
#### नेटडीबी और पीयर फ़ील्ड्स

| कुंजी                                  | प्रकार    | विवरण                                        |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | ज्ञात समकक्षों की संख्या, स्थानीय राउटर को छोड़कर। |
| `i2p.router.netdb.activepeers`       | long    | सक्रिय समकक्षों की संख्या।                            |
| `i2p.router.netdb.fastpeers`         | long    | तेज़ के रूप में वर्गीकृत समकक्षों की संख्या।                |
| `i2p.router.netdb.highcapacitypeers` | long    | उच्च क्षमता वाले के रूप में वर्गीकृत समकक्षों की संख्या।       |
| `i2p.router.netdb.isreseeding`       | boolean | क्या एक पुन:बीजन प्रगति पर है।                   |
**Response Fields (result)** आधिकारिक दस्तावेजों (GetI2P) के अनुसार: - `i2p.router.status` (String) — एक human-readable स्थिति - `i2p.router.uptime` (long) — milliseconds (या पुराने i2pd के लिए string) :contentReference[oaicite:0]{index=0} - `i2p.router.version` (String) — version string :contentReference[oaicite:1]{index=1} - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — B/s में inbound bandwidth :contentReference[oaicite:2]{index=2} - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — B/s में outbound bandwidth :contentReference[oaicite:3]{index=3} - `i2p.router.net.status` (long) — numeric स्थिति कोड (नीचे enum देखें) :contentReference[oaicite:4]{index=4} - `i2p.router.net.tunnels.participating` (long) — भाग लेने वाली tunnels की संख्या :contentReference[oaicite:5]{index=5} - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — netDb peer stats :contentReference[oaicite:6]{index=6} - `i2p.router.netdb.isreseeding` (boolean) — क्या reseed सक्रिय है :contentReference[oaicite:7]{index=7} - `i2p.router.netdb.knownpeers` (long) — कुल ज्ञात peers :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| पैरामीटर | प्रकार | विवरण |
|-----------|--------|------------------------------|
| `Stat`    | स्ट्रिंग | राउटर RateStat का नाम। |
| `Period`  | लंबी | मिलिसेकंड में दर अवधि। |
दिए गए समय अवधि के दौरान दर मेट्रिक्स (जैसे बैंडविड्थ, tunnel सफलता) प्राप्त करने के लिए उपयोग किया जाता है।

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**अनुरोध उदाहरण**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**नमूना प्रतिक्रिया**

### 4.3 RouterManager

---

| पैरामीटर            | परिणाम            | विवरण                                                           |
|--------------------|-------------------|-----------------------------------------------------------------------|
| `Restart`          | null              | तुरंत राउटर पुनःप्रारंभ करना शुरू करता है।                                |
| `RestartGraceful`  | null              | भाग लेने वाले टनल समाप्त होने के बाद पुनःप्रारंभ करता है।                          |
| `Shutdown`         | null              | तुरंत राउटर बंद करना शुरू करता है।                               |
| `ShutdownGraceful` | null              | भाग लेने वाले टनल समाप्त होने के बाद बंद करता है।                        |
| `Reseed`           | null              | एक राउटर रीसीड शुरू करता है।                                               |
| `FindUpdates`      | boolean या String | अवरुद्ध करने वाला। हस्ताक्षरित राउटर अपडेट के लिए खोज करता है।                        |
| `Update`           | String            | अवरुद्ध करने वाला। हस्ताक्षरित राउटर अपडेट शुरू करता है और अंतिम स्थिति लौटाता है। |
प्रशासनिक कार्य करें।

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**अनुमतित पैरामीटर / मेथड्स**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**अनुरोध उदाहरण**

### 4.4 NetworkSetting

**सफल प्रतिक्रिया**

---

| कुंजी                             | स्वीकृत मान                                      | विवरण                                                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | स्ट्रिंग, 1–65535                                     | NTCP पोर्ट; परिवर्तन के लिए पुनःप्रारंभ की आवश्यकता होती है।                        |
| `i2p.router.net.ntcp.hostname`  | स्ट्रिंग                                              | NTCP होस्टनाम; परिवर्तन के लिए पुनःप्रारंभ की आवश्यकता होती है।                    |
| `i2p.router.net.ntcp.autoip`    | `always`, `true`, या `false`                        | NTCP स्वचालित पता चयन।                            |
| `i2p.router.net.ssu.port`       | स्ट्रिंग, 1–65535                                     | SSU पोर्ट; परिवर्तन के लिए पुनःप्रारंभ की आवश्यकता होती है।                         |
| `i2p.router.net.ssu.hostname`   | स्ट्रिंग                                              | SSU बाह्य होस्टनाम; परिवर्तन के लिए पुनःप्रारंभ की आवश्यकता होती है।            |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu`, या `local,upnp,ssu` | SSU पता-खोज स्रोत।                               |
| `i2p.router.net.ssu.detectedip` | null                                                | केवल पढ़ने योग्य पता जो SSU द्वारा पता लगाया गया हो।                              |
| `i2p.router.net.upnp`           | स्ट्रिंग                                              | UPnP सेटिंग।                                                |
| `i2p.router.net.bw.share`       | स्ट्रिंग, 0–100                                       | भाग लेने वाली टनल के लिए उपलब्ध बैंडविड्थ का प्रतिशत। |
| `i2p.router.net.bw.in`          | गैर-ऋणात्मक पूर्णांक स्ट्रिंग                         | आगमन बैंडविड्थ सीमा KiB/s में।                            |
| `i2p.router.net.bw.out`         | गैर-ऋणात्मक पूर्णांक स्ट्रिंग                         | निर्गत बैंडविड्थ सीमा KiB/s में।                           |
| `i2p.router.net.laptopmode`     | स्ट्रिंग                                              | लैपटॉप मोड सेटिंग।                                         |
नेटवर्क कॉन्फ़िगरेशन पैरामीटर प्राप्त करें या सेट करें (ports, upnp, bandwidth share, आदि)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**अनुरोध उदाहरण (वर्तमान मान प्राप्त करें)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**नमूना प्रतिक्रिया**

> नोट: 2.41 से पहले के i2pd versions स्ट्रिंग्स के बजाय numeric types वापस कर सकते हैं — clients को दोनों को handle करना चाहिए। :contentReference[oaicite:11]{index=11}

### 4.5 उन्नत सेटिंग्स

---

| पैरामीटर | प्रकार               | विवरण                                                                |
|----------|---------------------|----------------------------------------------------------------------|
| `get`    | स्ट्रिंग             | `get` परिणाम ऑब्जेक्ट के अंदर एक सेटिंग लौटाता है।                     |
| `getAll` | n/a                 | `getAll` के अंदर पूर्ण विन्यास मैप लौटाता है।                          |
| `set`    | मैप<स्ट्रिंग, स्ट्रिंग> | अन्य कुंजियों को हटाए बिना आपूर्ति की गई सेटिंग्स को अद्यतन करता है।       |
| `setAll` | मैप<स्ट्रिंग, स्ट्रिंग> | **विनाशकारी:** सभी सेटिंग्स को प्रतिस्थापित करता है और आपूर्ति नहीं की गई कुंजियों को हटा देता है। |
आंतरिक router पैरामीटर्स को संशोधित करने की अनुमति देता है।

**अनुरोध उदाहरण**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**प्रतिक्रिया उदाहरण**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### मानक JSON-RPC2 त्रुटि कोड

---

| पैरामीटर | प्रकार | विवरण |
|-----------|--------|-----------------------------|
| `Echo` | स्ट्रिंग | मान जो `Result` के रूप में लौटाया गया है। |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### I2PControl विशिष्ट त्रुटि कोड

I2PControl को स्वयं प्रबंधित करता है। वर्तमान जावा हैंडलर पासवर्ड परिवर्तन का समर्थन करता है।

| पैरामीटर              | प्रकार   | विवरण                                                                 |
|-----------------------|--------|------------------------------------------------------------------------|
| `i2pcontrol.password` | स्ट्रिंग | एक नया I2PControl पासवर्ड सेट करता है और मौजूदा प्रमाणीकरण टोकन निरस्त करता है। |
परिणाम में `SettingsSaved` शामिल है। यदि पासवर्ड बदल दिया गया था, तो परिणाम में `"i2pcontrol.password": null` भी शामिल होता है। लेगेसी स्टैंडअलोन प्लगइन से listen-address और listen-port सेटिंग्स वर्तमान जावा हैंडलर में सक्रिय नहीं हैं।

> **डिफ़ॉल्ट पासवर्ड:** `itoopie` — यह फैक्ट्री डिफ़ॉल्ट है और सुरक्षा के लिए इसे **तुरंत बदला जाना चाहिए**।

## 5. त्रुटि कोड

### मानक JSON-RPC2 त्रुटि कोड

| कोड   | अर्थ               |
|--------|--------------------|
| -32700 | JSON पार्स त्रुटि  |
| -32600 | अमान्य अनुरोध       |
| -32601 | विधि नहीं मिली     |
| -32602 | अमान्य पैरामीटर    |
| -32603 | आंतरिक त्रुटि      |
### I2PControl विशिष्ट त्रुटि कोड

| कोड   | अर्थ                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | अमान्य पासवर्ड प्रदान किया गया                                                               |
| -32002 | कोई प्रमाणीकरण टोकन प्रस्तुत नहीं किया गया                                                        |
| -32003 | प्रमाणीकरण टोकन मौजूद नहीं है                                                       |
| -32004 | प्रदान किया गया प्रमाणीकरण टोकन समाप्त हो गया था और इसे हटा दिया जाएगा                        |
| -32005 | उपयोग किए गए I2PControl API का संस्करण निर्दिष्ट नहीं था, लेकिन निर्दिष्ट करना आवश्यक है |
| -32006 | निर्दिष्ट I2PControl API संस्करण I2PControl द्वारा समर्थित नहीं है               |
> **डिफ़ॉल्ट पासवर्ड:** `itoopie` — यह फैक्ट्री डिफ़ॉल्ट है और सुरक्षा के लिए इसे **तुरंत बदला जाना चाहिए**।

## 6. उपयोग और सर्वोत्तम प्रथाएं

- हमेशा `Token` parameter शामिल करें (प्रमाणीकरण के अलावा)।
- पहले उपयोग पर डिफ़ॉल्ट password (`itoopie`) बदलें।
- Java I2P के लिए, WebApps के माध्यम से I2PControl webapp सक्षम होना सुनिश्चित करें।
- थोड़ी भिन्नता के लिए तैयार रहें: कुछ fields I2P version के आधार पर numbers या strings हो सकते हैं।
- display-friendly output के लिए लंबे status strings को wrap करें।

> **डिफ़ॉल्ट पासवर्ड:** `itoopie` — यह फैक्ट्री डिफ़ॉल्ट है और सुरक्षा के लिए इसे **तुरंत बदला जाना चाहिए**।
