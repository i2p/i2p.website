---
title: "NTCP2 कार्यान्वयन विवरण"
date: 2018-08-20
author: "villain"
description: "I2P के नए ट्रांसपोर्ट प्रोटोकॉल के कार्यान्वयन विवरण और तकनीकी विनिर्देश"
categories: ["development"]
---

I2P के ट्रांसपोर्ट प्रोटोकॉल मूल रूप से लगभग 15 साल पहले विकसित किए गए थे। उस समय, मुख्य उद्देश्य प्रेषित डेटा को छिपाना था, न कि इस तथ्य को छिपाना कि कोई स्वयं प्रोटोकॉल का उपयोग कर रहा है। किसी ने DPI (डीप पैकेट इंस्पेक्शन) और प्रोटोकॉल की सेंसरशिप के खिलाफ सुरक्षा के बारे में गंभीरता से नहीं सोचा था। समय बदलता है, और भले ही मूल ट्रांसपोर्ट प्रोटोकॉल अब भी मजबूत सुरक्षा प्रदान कर रहे हैं, एक नए ट्रांसपोर्ट प्रोटोकॉल की मांग थी। NTCP2 को वर्तमान सेंसरशिप खतरों, विशेष रूप से पैकेट की लंबाई के DPI विश्लेषण, का प्रतिरोध करने के लिए डिज़ाइन किया गया है। साथ ही, नया प्रोटोकॉल आधुनिकतम क्रिप्टोग्राफी प्रगतियों का उपयोग करता है। NTCP2 [Noise Protocol Framework](https://noiseprotocol.org/noise.html) पर आधारित है, जिसमें SHA256 को हैश फ़ंक्शन के रूप में और x25519 को एलिप्टिक कर्व Diffie-Hellman (DH) कुंजी आदान-प्रदान के लिए उपयोग किया जाता है।

NTCP2 प्रोटोकॉल का पूर्ण विनिर्देश [यहाँ](/docs/specs/ntcp2/) उपलब्ध है।

## नई क्रिप्टोग्राफी

NTCP2 requires adding the next cryptographic algorithms to an I2P implementation:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

हमारे मूल प्रोटोकॉल NTCP की तुलना में, NTCP2 DH function (डिफी-हेल्मन फ़ंक्शन) के लिए ElGamal के स्थान पर x25519 का उपयोग करता है, AES-256-CBC/Adler32 के स्थान पर AEAD/Chaha20/Poly1305 का उपयोग करता है, और पैकेट की लंबाई की जानकारी को अस्पष्ट करने के लिए SipHash का उपयोग करता है। NTCP2 में उपयोग किया गया key derivation function (कुंजी व्युत्पन्न फ़ंक्शन) अधिक जटिल है, और अब कई HMAC-SHA256 कॉल का उपयोग करता है।

*i2pd (C++) कार्यान्वयन नोट: ऊपर उल्लिखित सभी एल्गोरिदम, SipHash को छोड़कर, OpenSSL 1.1.0 में कार्यान्वित हैं। SipHash को आने वाले OpenSSL 1.1.1 रिलीज़ में जोड़ा जाएगा। अधिकांश वर्तमान प्रणालियों में प्रयुक्त OpenSSL 1.0.2 के साथ अनुकूलता के लिए, मुख्य i2pd डेवलपर [Jeff Becker](https://github.com/majestrate) ने अनुपस्थित क्रिप्टोग्राफिक एल्गोरिदम के स्वतंत्र कार्यान्वयन का योगदान दिया है।*

## RouterInfo में परिवर्तन

NTCP2 को मौजूदा दो कुंजियों (एन्क्रिप्शन और सिग्नेचर कुंजियाँ) के अतिरिक्त एक तीसरी (x25519) कुंजी की आवश्यकता होती है। इसे एक स्थिर कुंजी कहा जाता है और इसे "s" पैरामीटर के रूप में RouterInfo के किसी भी पते में जोड़ना आवश्यक है। यह NTCP2 के आरंभकर्ता (Alice) और उत्तरदाता (Bob) दोनों के लिए आवश्यक है। यदि एक से अधिक पते NTCP2 का समर्थन करते हैं, उदाहरण के लिए IPv4 और IPv6, तो उन सभी के लिए "s" समान होना आवश्यक है। Alice के पते में केवल "s" पैरामीटर होना स्वीकार्य है, बिना "host" और "port" सेट किए। इसके अलावा, "v" पैरामीटर आवश्यक है, जिसे वर्तमान में हमेशा "2" पर सेट किया जाता है।

NTCP2 address को या तो एक अलग NTCP2 address के रूप में घोषित किया जा सकता है या अतिरिक्त पैरामीटरों के साथ पुरानी शैली का NTCP address के रूप में, और उस स्थिति में यह NTCP और NTCP2 दोनों प्रकार के कनेक्शन स्वीकार करेगा। Java I2P कार्यान्वयन दूसरा तरीका अपनाता है, जबकि i2pd (C++ कार्यान्वयन) पहला तरीका अपनाता है।

यदि कोई नोड NTCP2 कनेक्शन स्वीकार करता है, तो उसे अपना RouterInfo "i" पैरामीटर के साथ प्रकाशित करना होगा, जो उस नोड द्वारा नए कनेक्शन स्थापित करने पर सार्वजनिक एन्क्रिप्शन कुंजी के लिए आरंभिक वेक्टर (IV) के रूप में उपयोग किया जाता है।

## कनेक्शन स्थापित करना

कनेक्शन स्थापित करने के लिए दोनों पक्षों को अस्थायी x25519 कुंजियों के जोड़े उत्पन्न करने की आवश्यकता होती है। उन कुंजियों और "static" कुंजियों के आधार पर वे डेटा स्थानांतरण के लिए कुंजियों का एक समूह व्युत्पन्न करते हैं। दोनों पक्षों को यह सत्यापित करना चाहिए कि दूसरे पक्ष के पास वास्तव में उस "static" कुंजी के लिए निजी कुंजी है, और वह "static" कुंजी RouterInfo में मौजूद कुंजी के समान है।

Three messages are being sent to establish a connection:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
प्रत्येक संदेश के लिए एक साझा x25519 कुंजी, जिसे «input key material» (इनपुट कुंजी सामग्री) कहा जाता है, की गणना की जाती है; इसके बाद MixKey फ़ंक्शन से संदेश एन्क्रिप्शन कुंजी उत्पन्न की जाती है। संदेशों के आदान-प्रदान के दौरान ck (चेनिंग कुंजी, chaining key) का मान संरक्षित रखा जाता है। डेटा स्थानांतरण हेतु कुंजियाँ उत्पन्न करते समय उस मान का उपयोग अंतिम इनपुट के रूप में किया जाता है।

MixKey फ़ंक्शन I2P के C++ कार्यान्वयन में कुछ इस प्रकार दिखता है:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
**SessionRequest** संदेश एक सार्वजनिक x25519 Alice कुंजी (32 बाइट्स), AEAD/Chacha20/Poly1305 से एन्क्रिप्ट किया हुआ डेटा ब्लॉक (16 बाइट्स), एक हैश (16 बाइट्स) और अंत में कुछ यादृच्छिक डेटा (padding) से बना होता है। Padding की लंबाई एन्क्रिप्ट किए गए डेटा ब्लॉक में परिभाषित होती है। एन्क्रिप्टेड ब्लॉक में **SessionConfirmed** संदेश के दूसरे भाग की लंबाई भी शामिल होती है। डेटा का ब्लॉक Alice की अल्पकालिक कुंजी और Bob की स्थिर कुंजी से व्युत्पन्न कुंजी के साथ एन्क्रिप्ट और साइन किया जाता है। MixKey फ़ंक्शन के लिए प्रारंभिक ck मान SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256) पर सेट किया गया है।

चूँकि सार्वजनिक x25519 कुंजी के 32 बाइट को DPI (डीप पैकेट निरीक्षण) द्वारा पहचाना जा सकता है, इसलिए इसे AES-256-CBC एल्गोरिदम से एन्क्रिप्ट किया जाता है, जिसमें कुंजी के रूप में बॉब के पते का हैश और इनिशियलाइज़ेशन वेक्टर (IV) के रूप में RouterInfo का "i" पैरामीटर उपयोग होता है।

**SessionCreated** संदेश की संरचना **SessionRequest** जैसी ही होती है; बस कुंजी दोनों पक्षों की अस्थायी कुंजियों के आधार पर गणना की जाती है। **SessionRequest** संदेश से सार्वजनिक कुंजी को एन्क्रिप्ट/डिक्रिप्ट करने के बाद उत्पन्न IV को अस्थायी सार्वजनिक कुंजी को एन्क्रिप्ट/डिक्रिप्ट करने के लिए IV के रूप में उपयोग किया जाता है।

**SessionConfirmed** संदेश के 2 भाग होते हैं: स्थिर सार्वजनिक कुंजी और Alice का RouterInfo. पहले के संदेशों से अंतर यह है कि क्षणिक सार्वजनिक कुंजी को AEAD/Chaha20/Poly1305 से, **SessionCreated** की उसी कुंजी का उपयोग करके, एन्क्रिप्ट किया जाता है. इससे संदेश के पहले भाग का आकार 32 से बढ़कर 48 बाइट हो जाता है. दूसरे भाग को भी AEAD/Chaha20/Poly1305 से एन्क्रिप्ट किया जाता है, लेकिन एक नई कुंजी के साथ, जो Bob की क्षणिक कुंजी और Alice की स्थिर कुंजी से गणना करके प्राप्त होती है. RouterInfo भाग में यादृच्छिक डेटा पैडिंग भी जोड़ी जा सकती है, लेकिन इसकी आवश्यकता नहीं है, क्योंकि RouterInfo प्रायः परिवर्तनीय लंबाई का होता है.

## डेटा स्थानांतरण कुंजियों का सृजन

यदि हर हैश और कुंजी सत्यापन सफल हो गए हैं, तो अंतिम MixKey ऑपरेशन के बाद दोनों पक्षों पर एक सामान्य ck मान मौजूद होना चाहिए। यह मान कनेक्शन के प्रत्येक पक्ष के लिए कुंजियों के दो सेट <k, sipk, sipiv> उत्पन्न करने में उपयोग किया जाता है। "k" एक AEAD/Chaha20/Poly1305 कुंजी है, "sipk" एक SipHash कुंजी है, "sipiv" SipHash IV के लिए प्रारंभिक मान है, जो प्रत्येक उपयोग के बाद बदल दिया जाता है।

कुंजियाँ उत्पन्न करने हेतु प्रयुक्त कोड I2P के C++ कार्यान्वयन में इस प्रकार दिखता है:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) implementation note: First 16 bytes of the "sipkeys" array are a SipHash key, the last 8 bytes are IV. SipHash requires two 8 byte keys, but i2pd handles them as a single 16 bytes key.*

## डेटा स्थानांतरण

डेटा का स्थानांतरण फ्रेमों में होता है, प्रत्येक फ्रेम के 3 भाग होते हैं:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

एक फ्रेम में स्थानांतरित किए जाने वाले डेटा की अधिकतम लंबाई 65519 बाइट्स है.

वर्तमान SipHash IV के पहले दो बाइट्स के साथ XOR फ़ंक्शन लागू करके संदेश की लंबाई को अस्पष्ट किया जाता है.

एन्क्रिप्टेड डेटा भाग में डेटा के ब्लॉक होते हैं। प्रत्येक ब्लॉक के प्रारम्भ में 3 बाइट का हेडर जोड़ा जाता है, जो ब्लॉक का प्रकार और ब्लॉक की लंबाई निर्धारित करता है। आमतौर पर, I2NP प्रकार के ब्लॉकों का स्थानांतरण किया जाता है, जो परिवर्तित हेडर वाले I2NP संदेश होते हैं। एक NTCP2 फ्रेम कई I2NP ब्लॉक स्थानांतरित कर सकता है।

दूसरा महत्वपूर्ण डेटा ब्लॉक प्रकार यादृच्छिक डेटा ब्लॉक है। हर NTCP2 फ्रेम में एक यादृच्छिक डेटा ब्लॉक जोड़ने की सिफारिश की जाती है। केवल एक यादृच्छिक डेटा ब्लॉक जोड़ा जा सकता है और वह अंतिम ब्लॉक होना चाहिए।

ये वर्तमान NTCP2 कार्यान्वयन में प्रयुक्त अन्य डेटा ब्लॉक हैं:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## सारांश

नया I2P ट्रांसपोर्ट प्रोटोकॉल NTCP2 DPI (डीप पैकेट निरीक्षण) सेंसरशिप के विरुद्ध प्रभावी प्रतिरोध प्रदान करता है। इसके द्वारा प्रयुक्त तेज़, आधुनिक क्रिप्टोग्राफी के कारण CPU पर कम भार पड़ता है। यह I2P को लो-एंड डिवाइसेज़, जैसे स्मार्टफ़ोन और घरेलू routers पर चलने की संभावना बढ़ाता है। दोनों प्रमुख I2P क्रियान्वयनों में NTCP2 का पूर्ण समर्थन है और वे NTCP2 को उपयोग के लिए संस्करण 0.9.36 (Java) तथा 2.20 (i2pd, C++) से उपलब्ध कराते हैं।
