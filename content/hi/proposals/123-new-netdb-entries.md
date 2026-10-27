---
title: "नए netDB एंट्रीज़"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "खुला"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## स्थिति

इस प्रस्ताव के कुछ भाग पूर्ण हैं और 0.9.38 और 0.9.39 में लागू किए गए हैं।   सामान्य संरचनाएँ, I2CP, I2NP, और अन्य विनिर्देश अब उन परिवर्तनों को दर्शाने के लिए अद्यतन किए गए हैं जो अब समर्थित हैं।

पूर्ण हुए भाग अभी भी छोटे संशोधनों के अधीन हैं।   इस प्रस्ताव के अन्य भाग अभी विकासाधीन हैं   और बड़े पैमाने पर संशोधन के अधीन हैं।

सेवा लुकअप (प्रकार 9 और 11) कम प्राथमिकता वाले हैं और   अनिर्धारित हैं, और एक अलग प्रस्ताव में अलग किए जा सकते हैं।

## अवलोकन

यह निम्नलिखित 4 प्रस्तावों का एक अद्यतन और समूहीकरण है:

- 110 LS2  
- 120 मैसिव मल्टीहोमिंग के लिए मेटा LS2  
- 121 एन्क्रिप्टेड LS2  
- 122 अनॉथेंटिकेटेड सर्विस लुकअप (एनीकास्टिंग)

ये प्रस्ताव अधिकांशतः स्वतंत्र हैं, लेकिन स्वास्थ्य के लिए हम कई में एक   सामान्य प्रारूप परिभाषित और उपयोग करते हैं।

निम्नलिखित प्रस्ताव थोड़े संबंधित हैं:

- 140 इनविजिबल मल्टीहोमिंग (इस प्रस्ताव के साथ असंगत)  
- 142 न्यू क्रिप्टो टेम्पलेट (नए सममित क्रिप्टो के लिए)  
- 144 ECIES-X25519-AEAD-Ratchet  
- 145 ECIES-P256  
- 146 Red25519  
- 148 EdDSA-BLAKE2b-Ed25519  
- 149 B32 for Encrypted LS2  
- 150 Garlic Farm Protocol  
- 151 ECDSA Blinding

## प्रस्ताव

यह प्रस्ताव 5 नए DatabaseEntry प्रकारों और उन्हें नेटवर्क डेटाबेस में   संग्रहीत करने और उन्हें पुनः प्राप्त करने की प्रक्रिया को परिभाषित करता है,   साथ ही उन पर हस्ताक्षर करने और उन हस्ताक्षरों को सत्यापित करने की विधि को भी।

### लक्ष्य

- पिछड़ा संगत  
- पुराने शैली के मल्टीहोमिंग के साथ LS2 का उपयोग  
- समर्थन के लिए कोई नया क्रिप्टो या प्राथमिक आवश्यक नहीं  
- क्रिप्टो और हस्ताक्षर के अलगाव को बनाए रखें; सभी वर्तमान और भावी संस्करणों का समर्थन करें  
- वैकल्पिक ऑफ़लाइन हस्ताक्षर कुंजियों को सक्षम करें  
- फिंगरप्रिंटिंग को कम करने के लिए टाइमस्टैम्प की सटीकता कम करें  
- गंतव्यों के लिए नया क्रिप्टो सक्षम करें  
- मैसिव मल्टीहोमिंग सक्षम करें  
- मौजूदा एन्क्रिप्टेड LS के कई मुद्दों को ठीक करें  
- फ्लडफिल्स द्वारा दृश्यता को कम करने के लिए वैकल्पिक ब्लाइंडिंग  
- एन्क्रिप्टेड एकल-कुंजी और कई रद्द करने योग्य कुंजियों दोनों का समर्थन करता है  
- आउटप्रॉक्सी, एप्लिकेशन DHT बूटस्ट्रैप, और अन्य उपयोगों के लिए आसान लुकअप के लिए सेवा लुकअप  
- 32-बाइट बाइनरी गंतव्य हैश पर निर्भर कुछ भी न तोड़ें, उदाहरण के लिए बिटटॉरेंट  
- लीज़सेट्स में लचीलापन जोड़ें गुणों के माध्यम से, जैसे कि हमारे पास राउटरइन्फो में है।  
- प्रकाशित टाइमस्टैम्प और चर समाप्ति को हेडर में डालें, ताकि यह तब भी काम करे जब सामग्री एन्क्रिप्टेड हो (सबसे पुराने लीज़ से टाइमस्टैम्प प्राप्त न करें)  
- सभी नए प्रकार मौजूदा लीज़सेट्स के समान DHT स्थान और स्थानों में रहते हैं, ताकि उपयोगकर्ता पुराने LS से LS2 में माइग्रेट कर सकें, या LS2, मेटा और एन्क्रिप्टेड के बीच बदल सकें, बिना गंतव्य या हैश को बदले।  
- मौजूदा गंतव्य को ऑफ़लाइन कुंजियों का उपयोग करने के लिए परिवर्तित किया जा सकता है, या ऑनलाइन कुंजियों पर वापस, बिना गंतव्य या हैश को बदले।

### गैर-लक्ष्य / क्षेत्र से बाहर

- नया DHT रोटेशन एल्गोरिदम या साझा यादृच्छिक उत्पादन  
- नया एन्क्रिप्शन प्रकार और उस नए प्रकार का उपयोग करने के लिए एंड-टू-एंड एन्क्रिप्शन योजना एक अलग प्रस्ताव में होगी। यहां कोई नया क्रिप्टो निर्दिष्ट या चर्चा नहीं किया गया है।  
- RIs या टनल निर्माण के लिए नया एन्क्रिप्शन। यह एक अलग प्रस्ताव में होगा।  
- I2NP DLM / DSM / DSRM संदेशों के एन्क्रिप्शन, संचरण और प्राप्ति के तरीके। नहीं बदल रहा है।  
- मेटा को वास्तव में कैसे उत्पन्न करें और समर्थन करें, जिसमें बैकएंड इंटर-राउटर संचार, प्रबंधन, विफलता के बाद पुनर्स्थापना, और समन्वय शामिल है। समर्थन I2CP, या i2pcontrol, या एक नए प्रोटोकॉल में जोड़ा जा सकता है। यह मानकीकृत हो सकता है या नहीं।  
- लंबे समय तक चलने वाले टनल को वास्तव में कैसे लागू और प्रबंधित करें, या मौजूदा टनल को रद्द करें। यह अत्यंत कठिन है, और बिना इसके, आपके पास एक उचित ग्रेसफुल शटडाउन नहीं हो सकता।  
- धमकी मॉडल में परिवर्तन  
- ऑफ़लाइन भंडारण प्रारूप, या डेटा को संग्रहीत/पुनः प्राप्त/साझा करने के तरीके।  
- कार्यान्वयन विवरण यहां चर्चा नहीं किए गए हैं और प्रत्येक परियोजना के लिए छोड़ दिए गए हैं।

### औचित्य

LS2 में एन्क्रिप्शन प्रकार बदलने और भविष्य के प्रोटोकॉल परिवर्तनों के लिए फ़ील्ड जोड़ता है।

एन्क्रिप्टेड LS2 मौजूदा एन्क्रिप्टेड LS के कई सुरक्षा मुद्दों को ठीक करता है लीज़ के पूरे सेट के असममित एन्क्रिप्शन का उपयोग करके।

मेटा LS2 लचीला, कुशल, प्रभावी और बड़े पैमाने पर मल्टीहोमिंग प्रदान करता है।

सेवा रिकॉर्ड और सेवा सूची नामकरण लुकअप और DHT बूटस्ट्रैपिंग जैसी एनीकास्ट सेवाएं प्रदान करते हैं।

### नेटडीबी डेटा प्रकार

प्रकार संख्याओं का उपयोग I2NP डेटाबेस लुकअप/स्टोर संदेशों में किया जाता है।

एंड-टू-एंड कॉलम इंगित करता है कि क्या प्रश्नोत्तरी/प्रतिक्रियाएं एक गंतव्य को एक गर्लिक संदेश में भेजी जाती हैं।

मौजूदा प्रकार:

| नेटडीबी डेटा | लुकअप प्रकार | स्टोर प्रकार |
|------------|-------------|------------|
| कोई भी        | 0           | कोई भी        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| अन्वेषणात्मक| 3           | DSRM       |
नए प्रकार:

| नेटडीबी डेटा     | लुकअप प्रकार | स्टोर प्रकार | मानक LS2 हेडर? | एंड-टू-एंड भेजा गया? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | हाँ              | हाँ              |
| एन्क्रिप्टेड LS2  | 1           | 5          | नहीं               | नहीं               |
| मेटा LS2       | 1           | 7          | हाँ              | नहीं               |
| सेवा रिकॉर्ड | n/a         | 9          | हाँ              | नहीं               |
| सेवा सूची   | 4           | 11         | नहीं               | नहीं               |
### टिप्पणियाँ

- लुकअप प्रकार वर्तमान में डेटाबेस लुकअप संदेश में बिट्स 3-2 में हैं। कोई भी अतिरिक्त प्रकार बिट 4 के उपयोग की आवश्यकता होगी।

- पुराने राउटर द्वारा डेटाबेस स्टोर संदेश प्रकार फ़ील्ड में ऊपरी बिट्स को अनदेखा किया जाता है, इसलिए सभी स्टोर प्रकार विषम हैं। हम इसे एक संपीड़ित RI के रूप में नहीं, बल्कि एक LS के रूप में विफल होना पसंद करेंगे।

- क्या प्रकार हस्ताक्षर द्वारा कवर किए गए डेटा में स्पष्ट या अंतर्निहित या न कुछ होना चाहिए?

### लुकअप/स्टोर प्रक्रिया

प्रकार 3, 5, और 7 को एक मानक लीज़सेट लुकअप (प्रकार 1) के जवाब में लौटाया जा सकता है।   प्रकार 9 को कभी भी लुकअप के जवाब में नहीं लौटाया जाता है।   प्रकार 11 को एक नए सेवा लुकअप प्रकार (प्रकार 11) के जवाब में लौटाया जाता है।

केवल प्रकार 3 को क्लाइंट-टू-क्लाइंट गर्लिक संदेश में भेजा जा सकता है।

### प्रारूप

प्रकार 3, 7, और 9 सभी एक सामान्य प्रारूप का उपयोग करते हैं::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
मानक LS2 हेडर

प्रकार-विशिष्ट भाग

### गोपनीयता/सुरक्षा विचार

मानक LS2 हस्ताक्षर:

## मानक LS2 हेडर

प्रकार 5 (एन्क्रिप्टेड) में एक गंतव्य के साथ शुरू नहीं होता है और एक अलग प्रारूप है। नीचे देखें।

### प्रारूप

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### औचित्य

  - नीचे परिभाषित के रूप में

  - नीचे प्रत्येक भाग में परिभाषित के रूप में

  - लंबाई हस्ताक्षर प्रकार द्वारा निहित है जो हस्ताक्षर कुंजी का है

- अप्रकाशित/प्रकाशित: एंड-टू-एंड डेटाबेस स्टोर भेजते समय उपयोग के लिए,
  भेजने वाला राउटर इंगित करना चाह सकता है कि इस लीज़सेट को दूसरों को नहीं भेजा जाना चाहिए। हम वर्तमान में इस स्थिति को बनाए रखने के लिए ह्यूरिस्टिक्स का उपयोग करते हैं।

### मुद्दे

- प्रकाशित: लीज़सेट के 'संस्करण' को निर्धारित करने के लिए आवश्यक जटिल तर्क को बदलता है। वर्तमान में, संस्करण अंतिम-समाप्ति लीज़ की समाप्ति है, और एक प्रकाशन राउटर को कम से कम 1ms तक बढ़ाना होगा जब एक लीज़सेट प्रकाशित करते हैं जो केवल एक पुरानी लीज़ को हटाता है।

- समाप्ति: नेटडीबी प्रविष्टि के लिए एक समाप्ति की अनुमति देता है जो इसकी अंतिम-समाप्ति लीज़सेट से पहले हो। LS2 के लिए उपयोगी नहीं हो सकता है, जहां लीज़सेट को 11 मिनट की अधिकतम समाप्ति के साथ रहने की उम्मीद है, लेकिन अन्य नए प्रकारों के लिए, यह आवश्यक है (नीचे मेटा LS और सेवा रिकॉर्ड देखें)।

- ऑफ़लाइन कुंजियां वैकल्पिक हैं, प्रारंभिक/आवश्यक कार्यान्वयन जटिलता को कम करने के लिए।

### टिप्पणियाँ

- टाइमस्टैम्प सटीकता को और अधिक कम किया जा सकता है (10 मिनट?) लेकिन संस्करण संख्या जोड़नी होगी। यह मल्टीहोमिंग को तोड़ सकता है, जब तक कि हमारे पास क्रम संरक्षित एन्क्रिप्शन नहीं है? शायद बिना टाइमस्टैम्प के नहीं किया जा सकता।

- वैकल्पिक: 3 बाइट टाइमस्टैम्प (एपॉक / 10 मिनट), 1-बाइट संस्करण, 2-बाइट समाप्ति

- क्या प्रकार डेटा / हस्ताक्षर में स्पष्ट या अंतर्निहित है? हस्ताक्षर के लिए "डोमेन" स्थिरांक?

## नए DatabaseEntry प्रकार

### लीज़सेट 2

प्रकार 11 (सेवा सूची) कई सेवा रिकॉर्ड का एक समूह है और एक अलग प्रारूप है। नीचे देखें।

- राउटर को एक सेकंड से अधिक बार एक LS प्रकाशित नहीं करना चाहिए। यदि वे करते हैं, तो उन्हें पिछले प्रकाशित LS पर 1 अधिक कृत्रिम रूप से प्रकाशित टाइमस्टैम्प बढ़ाना चाहिए।

TBD

    Standard LS flag (1)
प्रकार 3, 7, और 9 मानक LS2 हेडर का उपयोग करते हैं, नीचे निर्दिष्ट:

    Standard LS2 type (3)
मौजूदा लीज़सेट से परिवर्तन:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
लुकअप के साथ

    10 minutes, as in a regular LS.
स्टोर के साथ

    Destination

### प्रारूप

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### औचित्य

- राउटर कार्यान्वयन अस्थायी कुंजियों और हस्ताक्षर को कैश कर सकते हैं ताकि हर बार सत्यापन से बचा जा सके। विशेष रूप से, फ्लडफिल्स, और लंबे समय तक चलने वाले कनेक्शन के दोनों छोर पर राउटर, इससे लाभान्वित हो सकते हैं।

- ऑफ़लाइन कुंजियां और हस्ताक्षर केवल लंबे समय तक चलने वाले गंतव्यों के लिए उपयुक्त हैं, यानी सर्वर, क्लाइंट नहीं।

### चर्चा

पर संग्रहीत करें

सामान्य समाप्ति

द्वारा प्रकाशित

- प्रकाशित टाइमस्टैम्प, समाप्ति टाइमस्टैम्प, झंडे, और गुण जोड़ें
- एन्क्रिप्शन प्रकार जोड़ें
- रद्दीकरण कुंजी हटाएं

यह प्रस्ताव अंत-से-अंत एन्क्रिप्शन कुंजी के लिए लीज़सेट में सार्वजनिक कुंजी का उपयोग जारी रखता है, और गंतव्य में सार्वजनिक कुंजी फ़ील्ड को अब की तरह अनुपयोग में छोड़ देता है। एन्क्रिप्शन प्रकार गंतव्य कुंजी प्रमाणपत्र में निर्दिष्ट नहीं है, यह 0 रहेगा।

- गुण: भविष्य के विस्तार और लचीलापन। शेष डेटा के पार्स करने के लिए आवश्यक होने की स्थिति में पहले रखा गया।

### नए एन्क्रिप्शन मुद्दे

एक अस्वीकृत वैकल्पिक विकल्प गंतव्य कुंजी प्रमाणपत्र में एन्क्रिप्शन प्रकार निर्दिष्ट करना है, गंतव्य में सार्वजनिक कुंजी का उपयोग करना, और लीज़सेट में सार्वजनिक कुंजी का उपयोग नहीं करना। हम ऐसा करने की योजना नहीं बना रहे हैं।

- एक नए एन्क्रिप्शन प्रकार में संक्रमण को आसान बनाने के लिए एकाधिक एन्क्रिप्शन प्रकार/सार्वजनिक कुंजी जोड़े हैं। इसे करने का दूसरा तरीका है कई लीज़सेट प्रकाशित करना, संभवतः समान टनल का उपयोग करके, जैसा कि हम अब DSA और EdDSA गंतव्यों के लिए करते हैं। टनल पर आने वाले एन्क्रिप्शन प्रकार की पहचान मौजूदा सत्र टैग तंत्र के साथ की जा सकती है, और/या प्रत्येक कुंजी का प्रयास डिक्रिप्शन करके। आने वाले संदेशों की लंबाई भी एक संकेत दे सकती है।

- वास्तविक सार्वजनिक कुंजी का स्थान नहीं बदलता है।
- गंतव्य को बदले बिना एन्क्रिप्शन प्रकार, या सार्वजनिक कुंजी, बदल सकता है।
- अनुपयोग में रद्दीकरण फ़ील्ड को हटा देता है
- इस प्रस्ताव में अन्य DatabaseEntry प्रकारों के साथ मूल संगतता
- एकाधिक एन्क्रिप्शन प्रकारों की अनुमति देता है

- राउटरइन्फो से भिन्न लीज़सेट में सार्वजनिक कुंजी और एन्क्रिप्शन प्रकार का स्थान
- लीज़सेट में अनुपयोग में सार्वजनिक कुंजी बनाए रखता है
- नेटवर्क भर में कार्यान्वयन की आवश्यकता है; वैकल्पिक रूप से, प्रायोगिक एन्क्रिप्शन प्रकारों का उपयोग किया जा सकता है, यदि फ्लडफिल्स द्वारा अनुमति दी गई हो (लेकिन प्रायोगिक हस्ताक्षर प्रकारों के समर्थन के बारे में संबंधित प्रस्ताव 136 और 137 देखें)। वैकल्पिक प्रस्ताव प्रायोगिक एन्क्रिप्शन प्रकारों के लिए लागू करने और परीक्षण करने के लिए आसान हो सकता है।

### टिप्पणियाँ

- एन्क्रिप्शन प्रकार संयोजन का प्रतिनिधित्व करता है  
  वक्र, कुंजी लंबाई, और एंड-टू-एंड योजना,  
  KDF और MAC सहित, यदि कोई है।

- हमने एक कुंजी लंबाई फ़ील्ड शामिल किया है, ताकि LS2  
  अज्ञात एन्क्रिप्शन प्रकारों के लिए भी फ्लडफिल द्वारा पार्स करने योग्य और सत्यापित करने योग्य हो।

- प्रस्तावित किया जाने वाला पहला नया एन्क्रिप्शन प्रकार  
  शायद ECIES/X25519 होगा। यह कैसे उपयोग किया जाता है एंड-टू-एंड  
  (या तो ElGamal/AES+SessionTag का थोड़ा संशोधित संस्करण  
  या कुछ पूरी तरह से नया, उदाहरण के लिए, ChaCha/Poly) एक या अधिक अलग प्रस्तावों में निर्दिष्ट किया जाएगा।  
  ECIES प्रस्ताव 144 और 145 भी देखें।

### एन्क्रिप्टेड LS2

LS2 के लाभ:

- लीज़ में 8-बाइट समाप्ति 4 बाइट में बदल गई है।

LS2 के नुकसान:

इनमें से कुछ इस प्रस्ताव के लिए बाहर के क्षेत्र में हैं,   लेकिन अभी के लिए यहां नोट्स डाल रहे हैं क्योंकि हमारे पास   अभी तक एक अलग एन्क्रिप्शन प्रस्ताव नहीं है।   ECIES प्रस्ताव 144 और 145 भी देखें।

- यदि हम कभी रद्दीकरण लागू करते हैं, तो हम शून्य समाप्ति फ़ील्ड के साथ कर सकते हैं, या शून्य लीज़, या दोनों। एक अलग रद्दीकरण कुंजी की कोई आवश्यकता नहीं है।

लक्ष्य:

    Standard LS flag (1)
एन्क्रिप्टेड LS2 को कभी भी एंड-टू-एंड गर्लिक संदेश में नहीं भेजा जाता है। ऊपर की तरह मानक LS2 का उपयोग करें।

    Encrypted LS2 type (5)
मौजूदा एन्क्रिप्टेड लीज़सेट से परिवर्तन:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
लुकअप के साथ

    10 minutes, as in a regular LS, or hours, as in a meta LS.
स्टोर के साथ

    Destination


### परिभाषाएँ

पर संग्रहीत करें

सामान्य समाप्ति

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

द्वारा प्रकाशित

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

हम एन्क्रिप्टेड LS2 के लिए उपयोग किए जाने वाले क्रिप्टोग्राफिक बिल्डिंग ब्लॉक्स के अनुरूप निम्नलिखित फ़ंक्शन परिभाषित करते हैं:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### प्रारूप

SIG

- एन्क्रिप्शन कुंजियां सर्वर पसंद के क्रम में हैं, सबसे पसंदीदा पहले। डिफ़ॉल्ट क्लाइंट व्यवहार पहली कुंजी का चयन करना है जिसके समर्थित एन्क्रिप्शन प्रकार हैं। क्लाइंट एन्क्रिप्शन समर्थन, सापेक्ष प्रदर्शन, और अन्य कारकों के आधार पर अन्य चयन एल्गोरिदम का उपयोग कर सकते हैं।

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

ऊपर निर्दिष्ट मानक LS2 हेडर का उपयोग नहीं करता है।

#### लेयर 0 (बाहरी)

प्रकार

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

ब्लाइंडेड पब्लिक की सिग प्रकार

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

ब्लाइंडेड पब्लिक की

    Length as implied by sig type

प्रकाशित टाइमस्टैम्प

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

समाप्ति

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

फ़्लैग

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

अस्थायी कुंजी डेटा

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

हस्ताक्षर

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (मध्य)

फ़्लैग

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH क्लाइंट प्रमाणीकरण डेटा

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

PSK क्लाइंट प्रमाणीकरण डेटा

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### लेयर 2 (आंतरिक)

प्रकार

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

डेटा

    LeaseSet2 data for the given type.

    Includes the header and signature.


### ब्लाइंडिंग कुंजी व्युत्पत्ति

हम key blinding के लिए निम्नलिखित scheme का उपयोग करते हैं, जो Ed25519 और [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) पर आधारित है। Re25519 signatures Ed25519 curve पर हैं और hash के लिए SHA-512 का उपयोग करते हैं।

हम [Tor's rend-spec-v3.txt परिशिष्ट A.2](https://spec.torproject.org/rend-spec-v3) का उपयोग नहीं करते, जिसके डिज़ाइन लक्ष्य समान हैं, क्योंकि इसकी blinded public keys prime-order subgroup से बाहर हो सकती हैं, जिनके सुरक्षा निहितार्थ अज्ञात हैं।

#### लक्ष्य

- ब्लाइंडिंग जोड़ें
- एकाधिक हस्ताक्षर प्रकारों की अनुमति दें
- कोई नया क्रिप्टो प्राथमिक आवश्यक नहीं
- वैकल्पिक रूप से प्रत्येक प्राप्तकर्ता के लिए एन्क्रिप्ट करें, रद्द करने योग्य
- केवल मानक LS2 और मेटा LS2 के एन्क्रिप्शन का समर्थन करें

#### सुरक्षा

एक blinding scheme की सुरक्षा के लिए आवश्यक है कि alpha का वितरण unblinded private keys के समान हो। हालाँकि, जब हम एक Ed25519 private key (sig type 7) को Red25519 private key (sig type 11) में blind करते हैं, तो वितरण भिन्न होता है। [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) की आवश्यकताओं को पूरा करने के लिए, unblinded keys के लिए भी Red25519 (sig type 11) का उपयोग किया जाना चाहिए, ताकि "एक re-randomized public key और उस key के अंतर्गत signature(s) का संयोजन उस key को उजागर न करे जिससे इसे re-randomized किया गया था।" हम मौजूदा destinations के लिए type 7 की अनुमति देते हैं, लेकिन उन नए destinations के लिए type 11 की सिफारिश करते हैं जिन्हें encrypt किया जाएगा।

#### परिभाषाएँ

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

अल्फा

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

एक

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

एक

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### ब्लाइंडिंग गणनाएँ

प्रत्येक दिन (UTC) एक नया secret alpha और blinded keys उत्पन्न किए जाने चाहिए। secret alpha और blinded keys की गणना निम्नानुसार की जाती है।

GENERATE_ALPHA(destination, date, secret), सभी पक्षों के लिए:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY(), leaseset प्रकाशित करने वाले स्वामी के लिए:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY(), leaseset प्राप्त करने वाले क्लाइंट्स के लिए:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
A' की गणना करने की दोनों विधियाँ अपेक्षा के अनुसार समान परिणाम देती हैं।

#### हस्ताक्षर करना

unblinded leaseset को unblinded Ed25519 या Red25519 signing private key से साइन किया जाता है और सामान्य रूप से unblinded Ed25519 या Red25519 signing public key (sig प्रकार 7 या 11) से सत्यापित किया जाता है।

यदि signing public key offline है, तो unblinded leaseset को unblinded transient Ed25519 या Red25519 signing private key से signed किया जाता है और सामान्य रूप से unblinded Ed25519 या Red25519 transient signing public key (sig types 7 या 11) से verified किया जाता है। encrypted leasesets के लिए offline keys पर अतिरिक्त notes के लिए नीचे देखें।

encrypted leaseset को sign करने के लिए हम Red25519 का उपयोग करते हैं, जो blinded keys के साथ sign और verify करने के लिए [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) पर आधारित है। Red25519 signatures Ed25519 curve पर आधारित हैं, जिनमें hash के लिए SHA-512 का उपयोग होता है।

Red25519 मानक Ed25519 के समान है, सिवाय उसके जो नीचे निर्दिष्ट है।

#### Sign/Verify गणनाएँ

encrypted leaseset के बाहरी भाग में Red25519 keys और signatures का उपयोग होता है।

Red25519, Ed25519 के लगभग समान है। दो अंतर हैं:

Red25519 private keys random numbers से generate की जाती हैं और फिर उन्हें mod L से reduce करना आवश्यक होता है, जहाँ L ऊपर परिभाषित है। Ed25519 private keys random numbers से generate की जाती हैं और फिर bytes 0 और 31 पर bitwise masking का उपयोग करके "clamped" की जाती हैं। Red25519 के लिए ऐसा नहीं किया जाता है। ऊपर परिभाषित GENERATE_ALPHA() और BLIND_PRIVKEY() functions mod L का उपयोग करके उचित Red25519 private keys generate करते हैं।

Red25519 में, हस्ताक्षर के लिए r की गणना अतिरिक्त यादृच्छिक डेटा का उपयोग करती है, और निजी कुंजी के हैश के बजाय सार्वजनिक कुंजी मान का उपयोग करती है। यादृच्छिक डेटा के कारण, प्रत्येक Red25519 हस्ताक्षर अलग होता है, भले ही समान कुंजी से समान डेटा पर हस्ताक्षर किया जाए।

हस्ताक्षर:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
सत्यापन:

```text
// same as in Ed25519
```
### एन्क्रिप्शन और प्रोसेसिंग

#### subcredentials की व्युत्पत्ति

Blinding process के भाग के रूप में, हमें यह सुनिश्चित करने की आवश्यकता है कि एक encrypted LS2 को केवल वही व्यक्ति डिक्रिप्ट कर सके जिसके पास संबंधित Destination की signing public key हो। पूरे Destination की आवश्यकता नहीं होती है। इसे प्राप्त करने के लिए, हम signing public key से एक credential derive करते हैं:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
personalization string सुनिश्चित करती है कि credential का किसी भी ऐसे hash से टकराव न हो जो DHT lookup key के रूप में उपयोग होता है, जैसे साधारण Destination hash।

किसी दिए गए blinded key के लिए, हम तब एक subcredential प्राप्त कर सकते हैं:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
subcredential को नीचे दी गई key derivation प्रक्रियाओं में शामिल किया गया है, जो उन keys को Destination की signing public key के ज्ञान से जोड़ता है।

#### लेयर 1 एन्क्रिप्शन

सबसे पहले, key derivation प्रक्रिया के लिए input तैयार किया जाता है:

```text
outerInput = subcredential || publishedTimestamp
```
इसके बाद, एक यादृच्छिक salt उत्पन्न किया जाता है:

```text
outerSalt = CSRNG(32)
```
इसके बाद layer 1 को encrypt करने के लिए उपयोग की जाने वाली key derive की जाती है:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
अंत में, लेयर 1 प्लेनटेक्स्ट को एन्क्रिप्ट और सीरियलाइज़ किया जाता है:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### लेयर 1 डिक्रिप्शन

salt को layer 1 ciphertext से parse किया जाता है:

```text
outerSalt = outerCiphertext[0:31]
```
इसके बाद layer 1 को encrypt करने के लिए उपयोग की जाने वाली key derive की जाती है:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
अंत में, layer 1 ciphertext को decrypt किया जाता है:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### लेयर 2 एन्क्रिप्शन

जब client authorization सक्षम होता है, तो ``authCookie`` की गणना नीचे वर्णित अनुसार की जाती है। जब client authorization अक्षम होता है, तो ``authCookie`` शून्य-लंबाई वाला byte array होता है।

एन्क्रिप्शन लेयर 1 के समान ढंग से आगे बढ़ता है:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### लेयर 2 डिक्रिप्शन

जब client authorization सक्षम होता है, तो ``authCookie`` की गणना नीचे वर्णित अनुसार की जाती है। जब client authorization अक्षम होता है, तो ``authCookie`` शून्य-लंबाई वाला byte array होता है।

डिक्रिप्शन लेयर 1 के समान ढंग से आगे बढ़ता है:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### प्रति-client प्राधिकरण

जब किसी Destination के लिए client authorization सक्षम की जाती है, तो server उन clients की सूची बनाए रखता है जिन्हें वह encrypted LS2 data को decrypt करने के लिए authorize कर रहा है। प्रति-client संग्रहीत data authorization mechanism पर निर्भर करता है, और इसमें किसी प्रकार की key material शामिल होती है जिसे प्रत्येक client generate करके secure out-of-band mechanism से server को भेजता है।

प्रति-क्लाइंट प्राधिकरण को लागू करने के लिए दो विकल्प हैं:

#### DH क्लाइंट प्राधिकरण

प्रत्येक client एक DH keypair ``[csk_i, cpk_i]`` उत्पन्न करता है, और public key ``cpk_i`` server को भेजता है।

सर्वर प्रोसेसिंग ^^^^^^^^^^^^^^^^^ सर्वर एक नया ``authCookie`` और एक ephemeral DH keypair जनरेट करता है:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
फिर प्रत्येक अधिकृत client के लिए, server ``authCookie`` को उसकी public key से encrypt करता है:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
सर्वर प्रत्येक ``[clientID_i, clientCookie_i]`` tuple को एन्क्रिप्टेड LS2 की layer 1 में रखता है, साथ ही ``epk`` भी।

क्लाइंट प्रोसेसिंग ^^^^^^^^^^^^^^^^^ क्लाइंट अपनी निजी कुंजी का उपयोग करके अपने अपेक्षित client identifier ``clientID_i``, encryption key ``clientKey_i``, और encryption IV ``clientIV_i`` को derive करता है:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
फिर क्लाइंट layer 1 authorization data में ऐसी प्रविष्टि खोजता है जिसमें ``clientID_i`` शामिल है। यदि कोई मेल खाती प्रविष्टि मौजूद है, तो क्लाइंट उसे डिक्रिप्ट करके ``authCookie`` प्राप्त करता है:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### प्री-शेयर्ड की क्लाइंट प्राधिकरण

प्रत्येक क्लाइंट एक गुप्त 32-बाइट कुंजी ``psk_i`` उत्पन्न करता है और उसे सर्वर को भेजता है। वैकल्पिक रूप से, सर्वर गुप्त कुंजी उत्पन्न कर सकता है और उसे एक या अधिक क्लाइंट्स को भेज सकता है।

सर्वर प्रोसेसिंग
^^^^^^^^^^^^^^^^^
सर्वर एक नया ``authCookie`` और salt जनरेट करता है:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
फिर प्रत्येक अधिकृत क्लाइंट के लिए, सर्वर ``authCookie`` को उसकी प्री-शेयर्ड कुंजी से एन्क्रिप्ट करता है:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
सर्वर प्रत्येक ``[clientID_i, clientCookie_i]`` tuple को ``authSalt`` के साथ encrypted LS2 की layer 1 में रखता है।

क्लाइंट प्रोसेसिंग
^^^^^^^^^^^^^^^^^
क्लाइंट अपनी pre-shared key का उपयोग करके अपना अपेक्षित client identifier ``clientID_i``, encryption key ``clientKey_i``, और encryption IV ``clientIV_i`` व्युत्पन्न करता है:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
फिर क्लाइंट layer 1 authorization data में ऐसी प्रविष्टि खोजता है जिसमें ``clientID_i`` शामिल है। यदि कोई मेल खाती प्रविष्टि मौजूद है, तो क्लाइंट उसे डिक्रिप्ट करके ``authCookie`` प्राप्त करता है:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### सुरक्षा संबंधी विचार

ऊपर दिए गए दोनों client authorization तंत्र client membership के लिए गोपनीयता प्रदान करते हैं। कोई entity जो केवल Destination जानता है, किसी भी समय देख सकता है कि कितने clients subscribed हैं, लेकिन यह track नहीं कर सकता कि कौन से clients जोड़े जा रहे हैं या revoke किए जा रहे हैं।

सर्वरों को हर बार encrypted LS2 जनरेट करते समय क्लाइंट्स के क्रम को randomize करना चाहिए, ताकि क्लाइंट्स सूची में अपनी स्थिति जान न सकें और यह अनुमान न लगा सकें कि अन्य क्लाइंट्स कब जोड़े या revoked किए गए हैं।

एक सर्वर प्राधिकरण डेटा की सूची में यादृच्छिक प्रविष्टियाँ सम्मिलित करके सदस्यता लिए गए क्लाइंटों की संख्या छिपाना चुन सकता है।

DH client authorization के लाभ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- सुरक्षा के लिए पूरी चीज को एन्क्रिप्ट करें
- केवल AES के साथ नहीं, सुरक्षित रूप से एन्क्रिप्ट करें
- प्रत्येक प्राप्तकर्ता के लिए एन्क्रिप्ट करें

DH client authorization की कमियाँ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- N clients के लिए server side पर N + 1 DH operations आवश्यक हैं।
- Client side पर एक DH operation आवश्यक है।
- Client को secret key generate करनी होती है।

PSK क्लाइंट प्राधिकरण के लाभ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- इसमें किसी DH ऑपरेशन की आवश्यकता नहीं होती।
- सर्वर को secret key जनरेट करने की अनुमति देता है।
- यदि चाहें तो सर्वर को एक ही key को कई clients के साथ साझा करने की अनुमति देता है।

PSK क्लाइंट प्राधिकरण की कमियाँ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- योजना की सुरक्षा client key material के out-of-band आदान-प्रदान पर गंभीर रूप से निर्भर है। कोई विरोधी जो किसी विशेष client के लिए इस आदान-प्रदान को intercept करता है, उस client के लिए अधिकृत किसी भी subsequent encrypted LS2 को decrypt कर सकता है, तथा यह भी निर्धारित कर सकता है कि client की access कब revoked होती है।

### Base 32 पतों के साथ एन्क्रिप्टेड LS

प्रस्ताव 149 देखें।

BitTorrent के लिए एन्क्रिप्टेड LS2 का उपयोग नहीं किया जा सकता, क्योंकि compact announce replies 32 बाइट के होते हैं। इन 32 बाइट में केवल hash होता है। leaseset के एन्क्रिप्टेड होने या signature types के संकेत के लिए कोई स्थान नहीं है।

### ऑफ़लाइन कुंजियों के साथ एन्क्रिप्टेड LS

offline keys वाले एन्क्रिप्टेड leaseSets के लिए, blinded private keys भी offline जनरेट किए जाने चाहिए, प्रत्येक दिन के लिए एक।

चूँकि वैकल्पिक offline signature block एन्क्रिप्टेड leaseset के cleartext भाग में होता है, floodfills को scrape करने वाला कोई भी व्यक्ति इसका उपयोग कई दिनों तक leaseset को track करने के लिए कर सकता है (परंतु उसे decrypt नहीं कर सकता)। इसे रोकने के लिए, keys के owner को प्रत्येक दिन के लिए नई transient keys भी generate करनी चाहिए। transient और blinded keys दोनों को पहले से generate किया जा सकता है और batch में router को दिया जा सकता है।

इस प्रस्ताव में कई transient और blinded keys को पैकेज करने तथा उन्हें client या router को उपलब्ध कराने के लिए कोई file format परिभाषित नहीं किया गया है। इस प्रस्ताव में offline keys के साथ encrypted leasesets के समर्थन के लिए कोई I2CP protocol enhancement परिभाषित नहीं किया गया है।

### टिप्पणियाँ

- एन्क्रिप्टेड leasesets का उपयोग करने वाली सेवा एन्क्रिप्टेड संस्करण floodfills को
  प्रकाशित करेगी। हालाँकि, दक्षता के लिए, प्रमाणीकृत होने के बाद (उदाहरण के लिए,
  whitelist के माध्यम से) यह क्लाइंट्स को wrapped garlic message में अनएन्क्रिप्टेड
  leasesets भेजेगी।

- Floodfills दुरुपयोग रोकने के लिए अधिकतम आकार को उचित मान तक सीमित कर सकते हैं।

- डिक्रिप्शन के बाद, कई जाँचें की जानी चाहिए, जिनमें यह भी शामिल है कि आंतरिक timestamp और expiration शीर्ष स्तर पर मौजूद वाले से मेल खाते हों।

- ChaCha20 को AES के बजाय चुना गया। यदि AES हार्डवेयर समर्थन उपलब्ध हो तो गतियाँ समान हैं, लेकिन जब AES हार्डवेयर समर्थन उपलब्ध न हो, जैसे कि निचले स्तर के ARM डिवाइसों पर, तो ChaCha20 2.5-3 गुना तेज़ है।

- हमें गति की इतनी परवाह नहीं है कि keyed BLAKE2b का उपयोग करें। इसका आउटपुट आकार इतना बड़ा है कि हमारी आवश्यकता के सबसे बड़े n को समाहित कर सके (या हम प्रत्येक वांछित key के लिए counter argument के साथ इसे एक बार कॉल कर सकते हैं)। BLAKE2b, SHA-256 से बहुत तेज़ है, और keyed-BLAKE2b hash function calls की कुल संख्या कम कर देगा। हालाँकि, proposal 148 देखें, जहाँ अन्य कारणों से BLAKE2b पर स्विच करने का प्रस्ताव है। [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html) देखें।

### Meta LS2

यह multihoming को प्रतिस्थापित करने के लिए उपयोग किया जाता है। किसी भी leaseset की तरह, यह निर्माता द्वारा हस्ताक्षरित होता है। यह destination hashes की एक प्रमाणित सूची है।

Meta LS2 एक tree structure का शीर्ष है, और संभवतः उसके intermediate nodes में भी है। इसमें कई entries होती हैं, जिनमें से प्रत्येक massive multihoming के समर्थन के लिए एक LS, LS2, या किसी अन्य Meta LS2 की ओर इंगित करती है। एक Meta LS2 में LS, LS2, और Meta LS2 entries का मिश्रण हो सकता है। tree के leaves सदैव एक LS या LS2 होते हैं। tree एक DAG है; loops निषिद्ध हैं; lookup करने वाले clients को loops का पता लगाना और उनका अनुसरण करने से मना करना चाहिए।

एक Meta LS2 का expiration एक standard LS या LS2 की तुलना में बहुत अधिक लंबा हो सकता है। top level का expiration publication date के कई घंटे बाद तक हो सकता है। अधिकतम expiration time को floodfills और clients द्वारा लागू किया जाएगा, और यह TBD है।

Meta LS2 का उपयोग-मामला massive multihoming है, लेकिन router restart के समय routers का leasesets से correlation के लिए अभी LS या LS2 के साथ जो सुरक्षा उपलब्ध है, उससे अधिक सुरक्षा प्रदान नहीं करता। यह "facebook" उपयोग-मामले के बराबर है, जिसे शायद correlation protection की आवश्यकता नहीं है। इस उपयोग-मामले को शायद offline keys की आवश्यकता है, जो tree के प्रत्येक node पर standard header में प्रदान की जाती हैं।

leaf routers, intermediate और master Meta LS signers के बीच समन्वय के लिए back-end protocol यहाँ निर्दिष्ट नहीं है। आवश्यकताएँ अत्यंत सरल हैं - बस यह सत्यापित करना कि peer up है, और हर कुछ घंटों में एक नया LS प्रकाशित करना। एकमात्र जटिलता विफलता पर top-level या intermediate-level Meta LSes के लिए नए publishers चुनने में है।

मिक्स-एंड-मैच leasesets, जहाँ कई routers के leases को मिलाकर, हस्ताक्षरित करके एक ही leaseset में प्रकाशित किया जाता है, का वर्णन proposal 140, "invisible multihoming" में किया गया है। यह proposal जिस रूप में लिखा गया है, अव्यवहार्य है, क्योंकि streaming connections किसी एक router के प्रति "sticky" नहीं रहेंगे, देखें http://zzz.i2p/topics/2335 .

invisible multihoming के लिए back-end protocol, और router तथा client internals के साथ interaction काफी जटिल होगा।

top-level Meta LS के लिए floodfill पर अत्यधिक भार से बचने हेतु, expiration कम से कम कई घंटे होनी चाहिए। Clients को top-level Meta LS को cache करना चाहिए, और यदि वह unexpired हो तो restarts के दौरान उसे persist करना चाहिए।

हमें क्लाइंट्स के लिए ट्री को ट्रैवर्स करने हेतु कुछ एल्गोरिदम परिभाषित करना होगा, जिसमें fallback भी शामिल हों, ताकि उपयोग फैला रहे। hash दूरी, लागत और randomness का कोई फंक्शन। यदि किसी नोड के पास LS या LS2 और Meta LS दोनों हों, तो हमें जानना होगा कि उन leaseSets का उपयोग कब करने की अनुमति है, और ट्री को कब ट्रैवर्स करते रहना है।

TBD

    Standard LS flag (1)
प्रकार 3, 7, और 9 मानक LS2 हेडर का उपयोग करते हैं, नीचे निर्दिष्ट:

    Meta LS2 type (7)
मौजूदा लीज़सेट से परिवर्तन:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
लुकअप के साथ

    Hours. Max 18.2 hours (65535 seconds)
स्टोर के साथ

    "master" Destination or coordinator, or intermediate coordinators

### प्रारूप

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
फ़्लैग्स और प्रॉपर्टीज़: भविष्य में उपयोग के लिए

### टिप्पणियाँ

- इसका उपयोग करने वाली एक वितरित सेवा के पास सेवा destination की private key वाले एक या अधिक "masters" होंगे। वे (out of band) सक्रिय destinations की वर्तमान सूची निर्धारित करेंगे और Meta LS2 प्रकाशित करेंगे। redundancy के लिए, कई masters Meta LS2 को multihome (अर्थात् एक साथ प्रकाशित) कर सकते हैं।

- एक वितरित सेवा एकल destination से शुरू हो सकती है या पुरानी शैली की multihoming का उपयोग कर सकती है, फिर Meta LS2 में संक्रमण कर सकती है। एक मानक LS lookup LS, LS2 या Meta LS2 में से कोई एक लौटा सकता है।

- जब कोई सेवा Meta LS2 का उपयोग करती है, तो उसके पास कोई tunnels (leases) नहीं होते हैं।

### सेवा रिकॉर्ड

यह एक व्यक्तिगत रिकॉर्ड है जो बताता है कि एक destination किसी सेवा में भाग ले रहा है। इसे participant से floodfill को भेजा जाता है। इसे floodfill द्वारा कभी अलग से नहीं भेजा जाता, बल्कि केवल Service List के भाग के रूप में भेजा जाता है। Service Record का उपयोग किसी सेवा में भागीदारी रद्द करने के लिए भी किया जाता है, जिसमें expiration को शून्य पर सेट किया जाता है।

यह कोई LS2 नहीं है, लेकिन यह मानक LS2 हेडर और सिग्नेचर फ़ॉर्मेट का उपयोग करता है।

TBD

    n/a, see Service List
प्रकार 3, 7, और 9 मानक LS2 हेडर का उपयोग करते हैं, नीचे निर्दिष्ट:

    Service Record type (9)
मौजूदा लीज़सेट से परिवर्तन:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
लुकअप के साथ

    Hours. Max 18.2 hours (65535 seconds)
स्टोर के साथ

    Destination

### प्रारूप

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### टिप्पणियाँ

- यदि expires पूरी तरह शून्य है, तो floodfill को record रद्द कर देना चाहिए और उसे अब service list में शामिल नहीं करना चाहिए।

- स्टोरेज: floodfill इन रिकॉर्ड्स के स्टोरेज को सख्ती से throttle कर सकता है और प्रति hash संग्रहीत रिकॉर्ड्स की संख्या तथा उनकी expiration को सीमित कर सकता है। hashes की whitelist भी उपयोग की जा सकती है।

- उसी hash पर कोई भी अन्य netdb प्रकार की प्राथमिकता होती है, इसलिए एक service record कभी भी किसी LS/RI को overwrite नहीं कर सकता, परंतु एक LS/RI उस hash पर सभी service records को overwrite करेगा।

### सेवा सूची

यह LS2 जैसा बिल्कुल नहीं है और एक अलग प्रारूप का उपयोग करता है।

सेवा सूची floodfill द्वारा बनाई और हस्ताक्षरित की जाती है। यह unauthenticated है क्योंकि कोई भी floodfill को एक Service Record प्रकाशित करके किसी सेवा में शामिल हो सकता है।

एक Service List में Short Service Records होते हैं, पूर्ण Service Records नहीं। इनमें signatures होते हैं, लेकिन केवल hashes होते हैं, पूर्ण destinations नहीं; इसलिए पूर्ण destination के बिना इन्हें सत्यापित नहीं किया जा सकता।

सेवा सूचियों की सुरक्षा (यदि कोई हो) और वांछनीयता TBD है। Floodfills प्रकाशन और lookups को सेवाओं की whitelist तक सीमित कर सकते हैं, लेकिन वह whitelist implementation या operator preference के आधार पर भिन्न हो सकती है। implementations के बीच एक सामान्य, base whitelist पर सहमति प्राप्त करना संभव नहीं हो सकता।

यदि ऊपर दिए गए सर्विस रिकॉर्ड में सर्विस नेम शामिल है, तो फ्लडफिल ऑपरेटर्स आपत्ति उठा सकते हैं; यदि केवल हैश शामिल है, तो कोई सत्यापन नहीं होता है, और एक सर्विस रिकॉर्ड किसी भी अन्य netdb type से पहले फ्लडफिल में दर्ज हो सकता है।

TBD

    Service List lookup type (11)
प्रकार 3, 7, और 9 मानक LS2 हेडर का उपयोग करते हैं, नीचे निर्दिष्ट:

    Service List type (11)
मौजूदा लीज़सेट से परिवर्तन:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
लुकअप के साथ

    Hours, not specified in the list itself, up to local policy
स्टोर के साथ

    Nobody, never sent to floodfill, never flooded.

### प्रारूप

ऊपर निर्दिष्ट मानक LS2 हेडर का उपयोग नहीं करता है।

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Service List के हस्ताक्षर सत्यापित करने के लिए:

- सेवा नाम का hash आगे जोड़ें
- निर्माता का hash हटाएँ
- संशोधित सामग्री का हस्ताक्षर जाँचें

प्रत्येक Short Service Record के हस्ताक्षर सत्यापित करने के लिए:

- destination fetch करें
- (published timestamp + expires + flags + port + service name का Hash) के signature की जाँच करें

प्रत्येक Revocation Record के हस्ताक्षर को सत्यापित करने के लिए:

- destination fetch करें
- (published timestamp + 4 zero bytes + flags + port + service name का Hash) के signature की जाँच करें

### टिप्पणियाँ

- हम अज्ञात signature प्रकारों का समर्थन कर सकें, इसलिए sig type के बजाय signature length का उपयोग करते हैं।

- सेवा सूची की कोई समाप्ति नहीं होती; प्राप्तकर्ता नीति या व्यक्तिगत रिकॉर्ड की समाप्ति के आधार पर स्वयं निर्णय ले सकते हैं।

- Service Lists को flood नहीं किया जाता, केवल अलग-अलग Service Records को किया जाता है। प्रत्येक
  floodfill एक Service List बनाता है, उस पर हस्ताक्षर करता है और उसे cache करता है। floodfill
  cache समय तथा service और revocation records की अधिकतम संख्या के लिए अपनी नीति का उपयोग करता है।

## Common Structures Spec में आवश्यक परिवर्तन

### कुंजी प्रमाणपत्र

यह प्रस्ताव के दायरे से बाहर है। इसे ECIES प्रस्ताव 144 और 145 में जोड़ें।

### नई इंटरमीडिएट संरचनाएँ

Lease2, MetaLease, LeaseSet2Header, और OfflineSignature के लिए नई संरचनाएं जोड़ें। रिलीज़ 0.9.38 से प्रभावी।

### नए NetDB प्रकार

प्रत्येक नए leaseset प्रकार के लिए संरचनाएँ जोड़ें, जो ऊपर से सम्मिलित हैं। LeaseSet2, EncryptedLeaseSet और MetaLeaseSet के लिए, रिलीज़ 0.9.38 से प्रभावी। Service Record और Service List के लिए, प्रारंभिक और अनिर्धारित।

### नया हस्ताक्षर प्रकार

RedDSA_SHA512_Ed25519 Type 11 जोड़ें। public key 32 bytes है; private key 32 bytes है; hash 64 bytes है; signature 64 bytes है।

## एन्क्रिप्शन स्पेक में आवश्यक परिवर्तन

यह इस प्रस्ताव के दायरे से बाहर है। प्रस्ताव 144 और 145 देखें।

## I2NP में आवश्यक परिवर्तन

नोट जोड़ें: LS2 को केवल न्यूनतम संस्करण वाले floodfills पर ही प्रकाशित किया जा सकता है।

### डेटाबेस लुकअप संदेश

सेवा सूची lookup प्रकार जोड़ें।

### परिवर्तन

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### डेटाबेस स्टोर संदेश

सभी नए store types जोड़ें।

### परिवर्तन

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP में आवश्यक परिवर्तन

### I2CP Options

router-पक्ष में व्याख्यायित नए विकल्प, SessionConfig Mapping में भेजे जाते हैं:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
client-side पर interpret किए जाने वाले नए विकल्प:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### सत्र कॉन्फ़िगरेशन

ध्यान दें कि ऑफ़लाइन हस्ताक्षरों के लिए, विकल्प i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, और i2cp.leaseSetOfflineSignature आवश्यक हैं, और हस्ताक्षर transient signing private key द्वारा किया जाता है।

### LeaseSet अनुरोध संदेश

Router से client तक। कोई बदलाव नहीं। Leases 8-byte timestamps के साथ भेजे जाते हैं, भले ही लौटाया गया leaseset 4-byte timestamps वाला LS2 हो। ध्यान दें कि प्रतिक्रिया Create Leaseset या Create Leaseset2 Message हो सकती है।

### वेरिएबल Leaseset संदेश का अनुरोध

Router से client तक। कोई बदलाव नहीं। Leases 8-byte timestamps के साथ भेजे जाते हैं, भले ही लौटाया गया leaseset 4-byte timestamps वाला LS2 हो। ध्यान दें कि प्रतिक्रिया Create Leaseset या Create Leaseset2 Message हो सकती है।

### Leaseset2 Message बनाएँ

क्लाइंट से router तक। नया संदेश, जिसका उपयोग Create Leaseset Message के स्थान पर किया जाए।

### औचित्य

- router को store type parse करने के लिए, type message में होना चाहिए, जब तक कि इसे session config में पहले से router को पास न किया गया हो। सामान्य parsing code के लिए, इसे message में ही रखना आसान होता है।

- router को private key का type और length जानने के लिए,
  यह lease set के बाद होना चाहिए, जब तक कि parser session config में type पहले से न जानता हो।
  सामान्य parsing code के लिए, इसे message से ही जानना आसान होता है।

- पहले revocation के लिए परिभाषित और अप्रयुक्त signing private key LS2 में मौजूद नहीं है।

### संदेश प्रकार

Create Leaseset2 Message के लिए message type 41 है।

### प्रारूप

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### टिप्पणियाँ

- न्यूनतम router संस्करण 0.9.39 है।
- message type 40 वाला प्रारंभिक संस्करण 0.9.38 में था, लेकिन format बदल दिया गया था।
  Type 40 छोड़ दिया गया है और असमर्थित है।

### मुद्दे

- encrypted और meta LS के समर्थन के लिए अधिक बदलाव आवश्यक हैं।

### ब्लाइंडिंग जानकारी संदेश

Client से router तक। नया संदेश।

### औचित्य

- router को यह जानना होता है कि कोई destination blinded है या नहीं।
  यदि वह blinded है और secret या per-client authentication का उपयोग करता है,
  तो उसके पास वह जानकारी भी होनी चाहिए।

- नए फॉर्मेट के b32 address ("b33") का Host Lookup router को बताता है कि address blinded है, लेकिन Host Lookup message में secret या private key को router तक पास करने के लिए कोई mechanism नहीं है। हालाँकि हम Host Lookup message को वह जानकारी जोड़ने के लिए extend कर सकते हैं, नया message define करना अधिक साफ़ है।

- हमें client के लिए router को बताने का एक प्रोग्रामेटिक तरीका चाहिए।
  अन्यथा, उपयोगकर्ता को प्रत्येक destination को मैन्युअली कॉन्फ़िगर करना होगा।

### उपयोग

किसी blinded destination को संदेश भेजने से पहले, client को या तो Host Lookup संदेश में "b33" को lookup करना होगा, या Blinding Info संदेश भेजना होगा। यदि blinded destination किसी secret या per-client authentication की आवश्यकता रखता है, तो client को Blinding Info संदेश भेजना होगा।

router इस संदेश का उत्तर नहीं भेजता है।

### संदेश प्रकार

Blinding Info Message के लिए message type 42 है।

### प्रारूप

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### टिप्पणियाँ

- न्यूनतम router संस्करण 0.9.43 है

### मुद्दे

### होस्ट उत्तर संदेश (enc)

"b33" hostnames की lookups को support करने और यदि router के पास आवश्यक जानकारी नहीं है तो संकेत लौटाने के लिए, हम Host Reply Message के लिए अतिरिक्त result codes परिभाषित करते हैं, इस प्रकार:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
मान 1-255 पहले से ही त्रुटियों के रूप में परिभाषित हैं, इसलिए backwards compatibility से जुड़ी कोई समस्या नहीं है।

### Meta Redirect संदेश

router से client तक। नया संदेश।

### औचित्य

क्लाइंट को यह पहले से ज्ञात नहीं होता है कि दिया गया Hash Meta LS में resolve होगा।

यदि किसी Destination के लिए leaseset lookup का परिणाम Meta LS के रूप में मिलता है, तो router recursive resolution करेगा। datagrams के मामले में client side को इसकी जानकारी की आवश्यकता नहीं होती; हालाँकि, streaming में, जहाँ protocol SYN ACK में destination की जाँच करता है, वहाँ यह जानना आवश्यक है कि "वास्तविक" destination क्या है। इसलिए, हमें एक नए message की आवश्यकता है।

### उपयोग

router उस वास्तविक destination के लिए कैश बनाए रखता है जो किसी meta LS से उपयोग किया जाता है। जब client किसी ऐसे destination को संदेश भेजता है जो meta LS पर resolve होता है, तो router पिछली बार उपयोग किए गए वास्तविक destination के लिए कैश जाँचता है। यदि कैश खाली है, तो router meta LS से एक destination चुनता है और leaseset lookup करता है। यदि leaseset lookup सफल होता है, तो router उस destination को कैश में जोड़ता है और client को एक Meta Redirect Message भेजता है। यह केवल एक बार किया जाता है, जब तक कि destination समाप्त न हो जाए और उसे बदलना आवश्यक न हो। यदि आवश्यक हो तो client को भी जानकारी कैश करनी चाहिए। Meta Redirect Message प्रत्येक SendMessage के उत्तर में नहीं भेजा जाता है।

router यह संदेश केवल उन clients को भेजता है जिनका संस्करण 0.9.47 या उससे उच्चतर है।

क्लाइंट इस संदेश का उत्तर नहीं भेजता है।

### संदेश प्रकार

Meta Redirect Message के लिए संदेश प्रकार 43 है।

### प्रारूप

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Meta के समर्थन के लिए परिवर्तन

Meta को कैसे उत्पन्न और समर्थित किया जाए, जिसमें routerों के बीच संचार और समन्वय शामिल है, यह इस प्रस्ताव के दायरे से बाहर है। संबंधित प्रस्ताव 150 देखें।

### Offline Keys के समर्थन के लिए परिवर्तन

Offline signatures को streaming या repliable datagrams में सत्यापित नहीं किया जा सकता। नीचे दिए गए अनुभाग देखें।

## निजी कुंजी फ़ाइल में परिवर्तन आवश्यक

private key फ़ाइल (eepPriv.dat) का फ़ॉर्मेट हमारे विनिर्देशों का आधिकारिक हिस्सा नहीं है, लेकिन यह [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) में प्रलेखित है और अन्य कार्यान्वयन इसका समर्थन करते हैं। इससे private keys को अलग-अलग कार्यान्वयनों में ले जाना संभव होता है।

transient public key और offline signing जानकारी को संग्रहीत करने के लिए परिवर्तन आवश्यक हैं।

### परिवर्तन

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### निजी कुंजी फ़ाइल के लिए CLI परिवर्तन आवश्यक

निम्नलिखित विकल्पों के लिए समर्थन जोड़ें:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## स्ट्रीमिंग में आवश्यक परिवर्तन

ऑफ़लाइन हस्ताक्षर वर्तमान में स्ट्रीमिंग में सत्यापित नहीं किए जा सकते। नीचे दिया गया परिवर्तन विकल्पों में offline signing ब्लॉक जोड़ता है। इससे यह जानकारी I2CP के माध्यम से प्राप्त करने की आवश्यकता नहीं रहती।

### परिवर्तन

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### टिप्पणियाँ

- वैकल्पिक तरीका यह है कि केवल एक फ़्लैग जोड़ा जाए और I2CP के माध्यम से transient public key प्राप्त की जाए
  (ऊपर दिए गए Host Lookup / Host Reply Message अनुभाग देखें)

## Repliable Datagram में आवश्यक परिवर्तन

repliable datagram प्रसंस्करण में ऑफ़लाइन हस्ताक्षर सत्यापित नहीं किए जा सकते। एक flag की आवश्यकता है जो संकेत दे कि ऑफ़लाइन हस्ताक्षरित है, लेकिन flag रखने के लिए कोई स्थान नहीं है। इसके लिए पूरी तरह नया protocol number और format आवश्यक होगा।

### परिवर्तन

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### टिप्पणियाँ

- विकल्प यह है कि केवल एक flag जोड़ा जाए, और I2CP के माध्यम से transient public key प्राप्त की जाए
  (ऊपर दिए गए Host Lookup / Host Reply Message अनुभाग देखें)
- अब जब हमारे पास flag bytes हैं, तो क्या कोई अन्य विकल्प हैं जिन्हें हमें जोड़ना चाहिए?

## SAM V3 में आवश्यक परिवर्तन

SAM को DESTINATION base 64 में ऑफ़लाइन हस्ताक्षरों का समर्थन करने के लिए उन्नत किया जाना आवश्यक है।

### परिवर्तन

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
ध्यान दें कि ऑफ़लाइन हस्ताक्षर केवल STREAM और RAW के लिए समर्थित हैं, DATAGRAM के लिए नहीं (जब तक हम एक नया DATAGRAM प्रोटोकॉल परिभाषित नहीं करते)।

ध्यान दें कि SESSION STATUS सभी शून्यों वाली एक Signing Private Key और ठीक वैसा ही Offline Signature डेटा लौटाएगा जैसा SESSION CREATE में दिया गया था।

ध्यान दें कि DEST GENERATE और SESSION CREATE DESTINATION=TRANSIENT का उपयोग एक offline signed destination बनाने के लिए नहीं किया जा सकता है।

### मुद्दे

संस्करण को 3.4 तक बढ़ाएँ, या इसे 3.1/3.2/3.3 पर ही रहने दें ताकि इसे 3.2/3.3 की सभी चीज़ों की आवश्यकता के बिना जोड़ा जा सके?

अन्य परिवर्तन TBD। ऊपर I2CP Host Reply Message अनुभाग देखें।

## BOB में आवश्यक परिवर्तन

offline signatures और/या Meta LS का समर्थन करने के लिए BOB को उन्नत करना होगा। यह कम प्राथमिकता है और संभवतः कभी निर्दिष्ट या कार्यान्वित नहीं किया जाएगा। SAM V3 पसंदीदा इंटरफ़ेस है।

## प्रकाशन, माइग्रेशन, संगतता

encrypted LS2 को छोड़कर, LS2 को LS1 के समान DHT location पर publish किया जाता है। LS1 और LS2 दोनों को publish करने का कोई तरीका नहीं है, जब तक LS2 किसी भिन्न location पर न हो।

एन्क्रिप्टेड LS2 को blinded key type और key data के hash पर प्रकाशित किया जाता है। फिर इस hash का उपयोग दैनिक "routing key" उत्पन्न करने के लिए किया जाता है, जैसा कि LS1 में होता है।

LS2 का उपयोग केवल तब किया जाएगा जब नई सुविधाओं की आवश्यकता हो (नया crypto, encrypted LS, meta, आदि)। LS2 को केवल निर्दिष्ट संस्करण या उससे उच्चतर वाले floodfills पर ही प्रकाशित किया जा सकता है।

LS2 प्रकाशित करने वाले सर्वर जानते होंगे कि कनेक्ट होने वाले सभी क्लाइंट LS2 का समर्थन करते हैं। वे garlic में LS2 भेज सकते हैं।

क्लाइंट्स LS2 को garlics में केवल तब भेजेंगे जब नई crypto का उपयोग कर रहे हों। Shared clients अनिश्चितकाल तक LS1 का उपयोग करेंगे? TODO: ऐसे shared clients कैसे बनाए जाएँ जो पुरानी और नई दोनों crypto का समर्थन करें?

## रोलआउट

0.9.38 में मानक LS2 के लिए floodfill समर्थन शामिल है, जिसमें ऑफ़लाइन कुंजियाँ भी शामिल हैं।

0.9.39 में LS2 और Encrypted LS2 के लिए I2CP समर्थन, sig type 11 से signing/verification, Encrypted LS2 के लिए floodfill समर्थन (sig types 7 और 11, offline keys के बिना), और LS2 को encrypting/decrypting (per-client authorization के बिना) शामिल है।

0.9.40 में पर-क्लाइंट प्राधिकरण के साथ LS2 को एन्क्रिप्ट/डिक्रिप्ट करने की क्षमता, Meta LS2 के लिए floodfill और I2CP समर्थन, ऑफलाइन कुंजियों के साथ एन्क्रिप्टेड LS2 के समर्थन और एन्क्रिप्टेड LS2 के लिए b32 समर्थन शामिल होने की योजना है।

## आभार

एन्क्रिप्टेड LS2 डिज़ाइन पर [Tor के v3 hidden service descriptors](https://spec.torproject.org/rend-spec-v3) का गहरा प्रभाव है, जिनके डिज़ाइन लक्ष्य समान थे।

## संदर्भ

* ["उच्च-गति उच्च-सुरक्षा हस्ताक्षर" द्वारा Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, और Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
