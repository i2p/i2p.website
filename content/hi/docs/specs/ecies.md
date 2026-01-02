---
title: "ECIES-X25519-AEAD-Ratchet (क्रमिक कुंजी-परिवर्तन तंत्र) एन्क्रिप्शन विनिर्देश"
description: "I2P के लिए एलिप्टिक कर्व इंटीग्रेटेड एन्क्रिप्शन स्कीम (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## अवलोकन

### उद्देश्य

ECIES-X25519-AEAD-Ratchet I2P का आधुनिक एंड-टू-एंड एन्क्रिप्शन प्रोटोकॉल है, जो पुराने ElGamal/AES+SessionTags सिस्टम की जगह लेता है। यह forward secrecy (कुंजियाँ बाद में लीक होने पर भी पूर्व संदेश गोपनीय रहते हैं), प्रमाणीकृत एन्क्रिप्शन, और प्रदर्शन व सुरक्षा में उल्लेखनीय सुधार प्रदान करता है।

### ElGamal/AES+SessionTags की तुलना में मुख्य सुधार

- **छोटी कुंजियाँ**: 32-बाइट कुंजियाँ बनाम 256-बाइट ElGamal पब्लिक कुंजियाँ (87.5% कमी)
- **Forward Secrecy (आगे की गोपनीयता)**: DH ratcheting (क्रमिक कुंजी नवीनीकरण) के माध्यम से हासिल (पुराने प्रोटोकॉल में उपलब्ध नहीं)
- **आधुनिक क्रिप्टोग्राफ़ी**: X25519 DH, ChaCha20-Poly1305 AEAD (Associated Data सहित प्रमाणित एन्क्रिप्शन), SHA-256
- **प्रमाणित एन्क्रिप्शन**: AEAD संरचना के माध्यम से अंतर्निर्मित प्रमाणीकरण
- **Bidirectional Protocol (द्विदिश प्रोटोकॉल)**: युग्मित inbound/outbound सेशन बनाम एकदिश पुराना प्रोटोकॉल
- **कुशल टैग**: 8-बाइट सेशन टैग बनाम 32-बाइट टैग (75% कमी)
- **Traffic Obfuscation (ट्रैफ़िक अस्पष्टता)**: Elligator2 encoding से हैंडशेक्स रैंडम से अप्रभेद्य हो जाते हैं

### परिनियोजन स्थिति

- **प्रारंभिक रिलीज़**: संस्करण 0.9.46 (May 25, 2020)
- **नेटवर्क परिनियोजन**: 2020 तक पूर्ण
- **वर्तमान स्थिति**: परिपक्व, व्यापक रूप से परिनियोजित (प्रोडक्शन में 5+ वर्ष)
- **Router समर्थन**: संस्करण 0.9.46 या उच्चतर आवश्यक
- **Floodfill आवश्यकताएँ**: एन्क्रिप्टेड लुकअप्स हेतु लगभग 100% अपनाने की आवश्यकता

### कार्यान्वयन स्थिति

**पूर्णतः कार्यान्वित:** - New Session (NS) संदेश बाइंडिंग सहित - New Session Reply (NSR) संदेश - Existing Session (ES) संदेश - DH ratchet मेकैनिज़्म (Diffie–Hellman आधारित कुंजी-रोटेशन तंत्र) - सेशन टैग और सिमेट्रिक की रैचेट्स - DateTime, NextKey, ACK, ACK Request, Garlic Clove (I2P 'garlic' संदेश का उप-घटक), और Padding ब्लॉक्स

**लागू नहीं (संस्करण 0.9.50 तक):** - MessageNumbers ब्लॉक (type 6) - Options ब्लॉक (type 5) - Termination ब्लॉक (type 4) - प्रोटोकॉल-स्तरीय स्वचालित प्रतिक्रियाएँ - शून्य स्थिर कुंजी मोड - मल्टीकास्ट सत्र

**नोट**: संस्करण 1.5.0 से 2.10.0 तक (2021–2025) के लिए कार्यान्वयन स्थिति का सत्यापन आवश्यक है, क्योंकि कुछ सुविधाएँ जोड़ी गई हो सकती हैं।

---

## प्रोटोकॉल की बुनियाद

### Noise Protocol Framework (क्रिप्टोग्राफी में हैंडशेक और कुंजी-सहमति प्रोटोकॉल डिज़ाइन करने का एक ढांचा)

ECIES-X25519-AEAD-Ratchet [Noise Protocol Framework](https://noiseprotocol.org/) (Revision 34, 2018-07-11) पर आधारित है, विशेष रूप से **IK** (परस्परक्रियात्मक, ज्ञात दूरस्थ स्थिर कुंजी) हैंडशेक पैटर्न पर, और इसमें I2P-विशिष्ट विस्तार शामिल हैं।

### Noise Protocol पहचानकर्ता (Noise Protocol: एक क्रिप्टोग्राफ़िक हैंडशेक ढांचा)

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**पहचानकर्ता घटक:** - `Noise` - आधारभूत फ्रेमवर्क - `IK` - ज्ञात दूरस्थ स्थिर कुंजी के साथ इंटरैक्टिव हैंडशेक पैटर्न - `elg2` - अस्थायी कुंजियों के लिए Elligator2 एन्कोडिंग (I2P विस्तार) - `+hs2` - दूसरे संदेश से पहले टैग को मिलाने के लिए MixHash कॉल किया जाता है (I2P विस्तार) - `25519` - X25519 Diffie-Hellman फ़ंक्शन - `ChaChaPoly` - ChaCha20-Poly1305 AEAD साइफ़र (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) - `SHA256` - SHA-256 हैश फ़ंक्शन

### Noise (क्रिप्टोग्राफ़िक प्रोटोकॉल फ्रेमवर्क) हैंडशेक पैटर्न

**IK पैटर्न संकेतन:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**टोकन के अर्थ:** - `e` - अस्थायी कुंजी प्रेषण - `s` - स्थिर कुंजी प्रेषण - `es` - Alice की अस्थायी कुंजी और Bob की स्थिर कुंजी के बीच DH (Diffie-Hellman कुंजी विनिमय) - `ss` - Alice की स्थिर कुंजी और Bob की स्थिर कुंजी के बीच DH - `ee` - Alice की अस्थायी कुंजी और Bob की अस्थायी कुंजी के बीच DH - `se` - Bob की स्थिर कुंजी और Alice की अस्थायी कुंजी के बीच DH

### Noise सुरक्षा गुणधर्म

Noise की शब्दावली में, IK पैटर्न प्रदान करता है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**प्रमाणीकरण स्तर:** - **स्तर 1**: पेलोड का प्रमाणीकरण इस रूप में होता है कि वह प्रेषक की स्थिर कुंजी के स्वामी का है, लेकिन Key Compromise Impersonation (KCI, कुंजी समझौता प्रतिरूपण) के प्रति संवेदनशील - **स्तर 2**: NSR के बाद KCI हमलों के प्रति प्रतिरोधी

**गोपनीयता स्तर:** - **स्तर 2**: यदि प्रेषक की स्थिर कुंजी बाद में समझौता हो जाती है, तो Forward secrecy (आगे की गोपनीयता) - **स्तर 4**: यदि प्रेषक की अस्थायी कुंजी बाद में समझौता हो जाती है, तो Forward secrecy - **स्तर 5**: दोनों अस्थायी कुंजियों के हटाए जाने के बाद पूर्ण Forward secrecy

### IK और XK के बीच अंतर

IK पैटर्न, NTCP2 और SSU2 में प्रयुक्त XK पैटर्न से भिन्न है:

1. **चार DH ऑपरेशन्स**: IK 4 DH ऑपरेशन्स (es, ss, ee, se) का उपयोग करता है, जबकि XK में 3 होते हैं
2. **तुरंत प्रमाणीकरण**: पहले संदेश में Alice का प्रमाणीकरण हो जाता है (प्रमाणीकरण स्तर 1)
3. **तेज़ Forward Secrecy (forward secrecy: भविष्य में कुंजियाँ लीक होने पर भी पुराने संदेश सुरक्षित रहते हैं)**: दूसरे संदेश (1-RTT) के बाद पूर्ण forward secrecy (स्तर 5) प्राप्त हो जाती है
4. **ट्रेड-ऑफ**: पहले संदेश का पेलोड forward-secret नहीं है (जबकि XK में सभी पेलोड forward-secret होते हैं)

**सारांश**: IK (एक हैंडशेक पैटर्न) Bob की प्रतिक्रिया की 1-RTT (एक राउंड-ट्रिप में) डिलीवरी को पूर्ण forward secrecy (आगे की गोपनीयता) के साथ सक्षम करता है, जिसकी कीमत यह है कि प्रारंभिक अनुरोध में forward secrecy नहीं होती।

### Signal Double Ratchet (डबल रैचेट एल्गोरिद्म) की अवधारणाएँ

ECIES (Elliptic Curve Integrated Encryption Scheme — दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) [Signal डबल रैचेट एल्गोरिथ्म](https://signal.org/docs/specifications/doubleratchet/) से अवधारणाएँ सम्मिलित करता है:

- **DH Ratchet**: (Diffie-Hellman आधारित रैचेट तंत्र) नियमित अंतराल पर नई DH कुंजियों का आदान-प्रदान करके forward secrecy (आगत गोपनीयता) प्रदान करता है
- **Symmetric Key Ratchet**: (सममित-कुंजी रैचेट तंत्र) प्रत्येक संदेश के लिए नई सेशन कुंजियाँ व्युत्पन्न करता है
- **Session Tag Ratchet**: (सेशन टैग रैचेट तंत्र) नियतात्मक रूप से एक-बार-उपयोग वाले सेशन टैग उत्पन्न करता है

**Signal से मुख्य अंतर:** - **कम बार होने वाला Ratcheting** (कुंजी-अद्यतन शृंखला प्रक्रिया): I2P केवल आवश्यकता पड़ने पर ही ratchet करता है (टैग लगभग समाप्त होने पर या नीति के अनुसार) - **Header Encryption के बजाय Session Tags** (सत्र टैग): एन्क्रिप्टेड हेडर के बजाय नियतात्मक टैग का प्रयोग करता है - **Explicit ACKs** (स्वीकृतियाँ): केवल रिवर्स ट्रैफिक पर निर्भर रहने के बजाय इन-बैंड ACK ब्लॉक्स का उपयोग करता है - **अलग Tag और Key Ratchets**: रिसीवर के लिए अधिक कुशल (कुंजी गणना को टाल सकता है)

### Noise (क्रिप्टोग्राफिक प्रोटोकॉल फ्रेमवर्क) के लिए I2P विस्तारों

1. **Elligator2 Encoding**: क्षणिक कुंजियाँ इस प्रकार एन्कोड की जाती हैं कि वे यादृच्छिक से अप्रभेद्य हों
2. **NSR से पहले टैग जोड़ा गया**: सहसंबंध के लिए NSR संदेश से पहले सेशन टैग जोड़ा गया
3. **परिभाषित पेलोड फ़ॉर्मेट**: सभी संदेश प्रकारों के लिए ब्लॉक-आधारित पेलोड संरचना
4. **I2NP एन्कैप्सुलेशन**: सभी संदेश I2NP Garlic Message हेडर में लपेटे जाते हैं
5. **अलग डेटा चरण**: ट्रांसपोर्ट संदेश (ES) मानक Noise (क्रिप्टोग्राफ़िक हैंडशेक प्रोटोकॉल) डेटा चरण से अलग हो जाते हैं

---

## क्रिप्टोग्राफी के मूल घटक

### X25519 डिफ़ी-हेलमैन

**विनिर्देश**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**मुख्य विशेषताएँ:** - **निजी कुंजी का आकार**: 32 बाइट - **सार्वजनिक कुंजी का आकार**: 32 बाइट - **साझा रहस्य का आकार**: 32 बाइट - **Endianness** (बाइट क्रम): Little-endian (निम्नतम बाइट पहले) - **वक्र**: Curve25519

**संचालन:**

### X25519 GENERATE_PRIVATE()

एक यादृच्छिक 32-बाइट निजी कुंजी उत्पन्न करता है:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

संबंधित सार्वजनिक कुंजी व्युत्पन्न करता है:

```
pubkey = curve25519_scalarmult_base(privkey)
```
32-बाइट little-endian (जहाँ सबसे कम महत्वपूर्ण बाइट पहले होती है) सार्वजनिक कुंजी वापस करता है।

### X25519 DH(privkey, pubkey)

Diffie-Hellman key agreement (कुंजी-सहमति प्रोटोकॉल) निष्पादित करता है:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
32-बाइट का साझा रहस्य लौटाता है।

**सुरक्षा नोट**: कार्यान्वयनकर्ताओं को यह सत्यापित करना अनिवार्य है कि shared secret (साझा गोपनीय मान) सभी शून्य न हो (कमज़ोर कुंजी)। ऐसा होने पर अस्वीकार करें और हैंडशेक (प्रारंभिक आदान-प्रदान) रद्द कर दें।

### ChaCha20-Poly1305 AEAD (संबद्ध डेटा के साथ प्रमाणित एन्क्रिप्शन)

**विनिर्देश**: [RFC 7539](https://tools.ietf.org/html/rfc7539) अनुभाग 2.8

**पैरामीटर्स:** - **कुंजी आकार**: 32 बाइट (256 बिट) - **नॉन्स आकार**: 12 बाइट (96 बिट) - **MAC आकार**: 16 बाइट (128 बिट) - **ब्लॉक आकार**: 64 बाइट (आंतरिक)

**Nonce (एक बार प्रयुक्त मान) का प्रारूप:**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**AEAD (Authenticated Encryption with Associated Data; प्रमाणित एन्क्रिप्शन विद संबद्ध डेटा) संरचना:**

AEAD (Authenticated Encryption with Associated Data, संबद्ध डेटा सहित प्रमाणीकृत एन्क्रिप्शन) ChaCha20 stream cipher को Poly1305 MAC के साथ संयोजित करता है:

1. कुंजी और nonce (एक-बार प्रयुक्त संख्या) से ChaCha20 keystream (कुंजी-धारा) उत्पन्न करें
2. plaintext (साधारण पाठ) को keystream के साथ XOR (एक्सक्लूसिव-OR) द्वारा एन्क्रिप्ट करें
3. (associated data (संलग्न डेटा) || ciphertext (कूटपाठ)) पर Poly1305 MAC (संदेश प्रमाणीकरण कोड) की गणना करें
4. ciphertext के अंत में 16-बाइट MAC जोड़ें

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

प्रामाणीकरण के साथ सादा पाठ को एन्क्रिप्ट करता है:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**गुण:** - Ciphertext (एन्क्रिप्ट किया गया पाठ) की लंबाई plaintext (मूल पाठ) जितनी ही होती है (stream cipher (बाइट/बिट धारा पर काम करने वाला सिफर)) - आउटपुट plaintext_length + 16 bytes होता है (इसमें MAC (संदेश प्रमाणीकरण कोड) शामिल है) - यदि key (कुंजी) गोपनीय है तो पूरा आउटपुट यादृच्छिक से अभेद्य होता है - MAC associated data (सहबद्ध डेटा) और ciphertext दोनों को प्रमाणित करता है

### ChaCha20-Poly1305 DECRYPT(k, n, ciphertext, ad)

डिक्रिप्ट करता है और प्रमाणीकरण सत्यापित करता है:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**महत्वपूर्ण सुरक्षा आवश्यकताएँ:** - Nonces (एक-बार-उपयोग संख्या) प्रत्येक संदेश के लिए उसी कुंजी के साथ अनिवार्य रूप से अद्वितीय हों - Nonces का पुन: उपयोग कदापि नहीं किया जाना चाहिए (पुन: उपयोग करने पर विनाशकारी विफलता) - MAC (संदेश प्रमाणीकरण कोड) सत्यापन में टाइमिंग हमलों को रोकने के लिए constant-time (स्थिर-समय) तुलना का उपयोग करना अनिवार्य है - असफल MAC सत्यापन का परिणाम संदेश के पूर्ण अस्वीकार में होना अनिवार्य है (कोई आंशिक डिक्रिप्शन नहीं)

### SHA-256 हैश फ़ंक्शन

**विनिर्देशन**: NIST FIPS 180-4

**विशेषताएँ:** - **आउटपुट आकार**: 32 बाइट (256 बिट) - **ब्लॉक आकार**: 64 बाइट (512 बिट) - **सुरक्षा स्तर**: 128 बिट (टकराव-प्रतिरोध)

**संचालन:**

### SHA-256 H(p, d)

personalization string (व्यक्तिकरण स्ट्रिंग) के साथ SHA-256 हैश:

```
H(p, d) := SHA256(p || d)
```
जहाँ `||` संयोजन को दर्शाता है, `p` personalization string (व्यक्तिकरण स्ट्रिंग) है, और `d` डेटा है।

### SHA-256 MixHash(d)

नए डेटा के साथ चल रहे हैश को अद्यतन करता है:

```
h = SHA256(h || d)
```
ट्रांसक्रिप्ट हैश बनाए रखने के लिए पूरे Noise हैंडशेक के दौरान उपयोग किया जाता है।

### HKDF कुंजी व्युत्पत्ति

**विनिर्देश**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**विवरण**: SHA-256 का उपयोग करने वाला HMAC (हैश-आधारित संदेश प्रमाणीकरण कोड)-आधारित कुंजी व्युत्पत्ति फ़ंक्शन

**पैरामीटर्स:** - **हैश फ़ंक्शन**: HMAC-SHA256 (HMAC-आधारित संदेश प्रमाणीकरण कोड, जो SHA-256 हैश का उपयोग करता है) - **सॉल्ट लंबाई**: अधिकतम 32 बाइट (SHA-256 (256-बिट का सुरक्षित हैश एल्गोरिद्म) आउटपुट आकार) - **आउटपुट लंबाई**: परिवर्तनीय (अधिकतम 255 * 32 बाइट)

**HKDF (HMAC-आधारित कुंजी व्युत्पन्न फ़ंक्शन):**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**सामान्य उपयोग के पैटर्न:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**ECIES में प्रयुक्त इन्फो स्ट्रिंग्स:** - `"KDFDHRatchetStep"` - DH रैचेट (क्रमिक कुंजी अद्यतन तंत्र) कुंजी व्युत्पत्ति - `"TagAndKeyGenKeys"` - टैग और कुंजी-श्रृंखला कुंजियों का आरंभिककरण - `"STInitialization"` - सेशन टैग रैचेट आरंभिककरण - `"SessionTagKeyGen"` - सेशन टैग उत्पादन - `"SymmetricRatchet"` - सममित कुंजी उत्पादन - `"XDHRatchetTagSet"` - DH रैचेट टैगसेट (टैग का समूह) कुंजी - `"SessionReplyTags"` - NSR टैगसेट उत्पादन - `"AttachPayloadKDF"` - NSR पेलोड कुंजी व्युत्पत्ति

### Elligator2 एन्कोडिंग

**उद्देश्य**: X25519 पब्लिक कीज़ को इस तरह एन्कोड करना कि वे समान-वितरित यादृच्छिक 32-बाइट स्ट्रिंग्स से अप्रभेद्य हों।

**विनिर्देश**: [Elligator2 शोधपत्र](https://elligator.cr.yp.to/elligator-20130828.pdf)

**समस्या**: मानक X25519 (एक ECDH एलिप्टिक-कर्व योजना) सार्वजनिक कुंजियों की संरचना पहचानने योग्य होती है। कोई पर्यवेक्षक इन कुंजियों का पता लगाकर handshake संदेशों की पहचान कर सकता है, भले ही सामग्री एन्क्रिप्टेड हो।

**समाधान**: Elligator2 ~50% मान्य X25519 सार्वजनिक कुंजियों और यादृच्छिक दिखने वाली 254-बिट स्ट्रिंगों के बीच bijective mapping (एक-एक तथा सर्व-व्यापी प्रतिचित्रण) प्रदान करता है।

**Elligator2 (एक क्रिप्टोग्राफ़िक मैपिंग तकनीक) के साथ कुंजी जनन:**

### Elligator2 GENERATE_PRIVATE_ELG2()

ऐसी निजी कुंजी उत्पन्न करता है जो Elligator2 (एक क्रिप्टोग्राफ़िक मैपिंग तकनीक) से एन्कोड होने योग्य सार्वजनिक कुंजी पर मैप होती है:

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**महत्वपूर्ण**: यादृच्छिक रूप से उत्पन्न निजी कुंजियों में से लगभग 50% ऐसी सार्वजनिक कुंजियाँ उत्पन्न करेंगी जिन्हें एन्कोड नहीं किया जा सकता। इन्हें त्याग देना चाहिए और पुनः उत्पन्न करने का प्रयास करना चाहिए।

**प्रदर्शन अनुकूलन**: हैंडशेक के दौरान विलंब से बचने के लिए उपयुक्त कुंजी-युग्मों का एक पूल बनाए रखने हेतु पृष्ठभूमि थ्रेड में कुंजियाँ पहले से उत्पन्न करें।

### Elligator2 ENCODE_ELG2(pubkey)

एक सार्वजनिक कुंजी को 32 यादृच्छिक जैसी दिखने वाली बाइट्स में एन्कोड करता है:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**एन्कोडिंग विवरण:** - Elligator2 254 बिट उत्पन्न करता है (पूर्ण 256 नहीं) - बाइट 31 के शीर्ष 2 बिट रैंडम पैडिंग होते हैं - परिणाम 32-बाइट स्पेस में समान रूप से वितरित होता है - मान्य X25519 सार्वजनिक कुंजियों में से लगभग 50% को सफलतापूर्वक एन्कोड करता है

### Elligator2 (एक क्रिप्टोग्राफिक मैपिंग तकनीक) DECODE_ELG2(encodedKey)

डिकोड करने पर मूल सार्वजनिक कुंजी प्राप्त होती है:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**सुरक्षा गुणधर्म:** - एन्कोडेड कुंजियाँ परिकलनिक रूप से यादृच्छिक बाइट्स से अप्रभेद्य होती हैं - कोई भी सांख्यिकीय परीक्षण Elligator2-एन्कोडेड कुंजियों का विश्वसनीय रूप से पता नहीं लगा सकता - डिकोडिंग नियतात्मक होती है (एक ही एन्कोडेड कुंजी हमेशा वही सार्वजनिक कुंजी उत्पन्न करती है) - एन्कोडिंग एन्कोड करने योग्य उपसमुच्चय में आने वाली ~50% कुंजियों के लिए bijective (एक-एक तथा सर्व-समापी) होती है

**कार्यान्वयन नोट्स:** - हैंडशेक के दौरान पुनः-एन्कोडिंग से बचने के लिए सृजन चरण में एन्कोडेड कुंजियाँ संग्रहीत करें - Elligator2 (एक क्रिप्टोग्राफ़िक मैपिंग तकनीक) जनरेशन से प्राप्त अनुपयुक्त कुंजियाँ NTCP2 के लिए उपयोग की जा सकती हैं (जिसमें Elligator2 की आवश्यकता नहीं होती) - प्रदर्शन के लिए पृष्ठभूमि में कुंजी सृजन आवश्यक है - 50% अस्वीकृति दर के कारण औसत सृजन समय दोगुना हो जाता है

---

## संदेश प्रारूप

### अवलोकन

ECIES (Elliptic Curve Integrated Encryption Scheme - दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) तीन संदेश प्रकार परिभाषित करता है:

1. **नया सत्र (NS)**: Alice द्वारा Bob को भेजा गया प्रारंभिक हैंडशेक संदेश
2. **नया सत्र प्रत्युत्तर (NSR)**: Bob द्वारा Alice को भेजा गया हैंडशेक प्रत्युत्तर
3. **मौजूदा सत्र (ES)**: आगे के सभी संदेश, दोनों दिशाओं में

सभी संदेश I2NP Garlic Message फ़ॉर्मैट में एनकैप्सुलेट किए जाते हैं, और उन पर अतिरिक्त एन्क्रिप्शन परतें लागू की जाती हैं।

### I2NP Garlic Message कंटेनर

सभी ECIES (Elliptic Curve Integrated Encryption Scheme—अण्डवक्र समेकित एन्क्रिप्शन योजना) संदेश मानक I2NP Garlic Message हेडर में लिपटे होते हैं:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**फ़ील्ड्स:** - `type`: 0x26 (Garlic Message) - `msg_id`: 4-बाइट I2NP संदेश ID - `expiration`: 8-बाइट Unix टाइमस्टैम्प (मिलीसेकंड) - `size`: 2-बाइट पेलोड का आकार - `chks`: 1-बाइट चेकसम - `length`: 4-बाइट एन्क्रिप्टेड डेटा की लंबाई - `encrypted data`: ECIES-एन्क्रिप्टेड पेलोड

**उद्देश्य**: I2NP-स्तर पर संदेश पहचान और रूटिंग प्रदान करता है। `length` फ़ील्ड प्राप्तकर्ताओं को कुल एन्क्रिप्टेड पेलोड का आकार जानने की अनुमति देती है।

### नया सत्र (NS) संदेश

New Session संदेश Alice से Bob तक एक नया सेशन आरंभ करता है। यह तीन प्रकारों में आता है:

1. **Binding सहित** (1b): द्विदिश संचार के लिए Alice की स्थिर कुंजी शामिल करता है (Binding: पहचान/कुंजी को बाँधकर प्रमाणित संबंध)
2. **Binding रहित** (1c): एक-दिशा संचार के लिए स्थिर कुंजी को छोड़ देता है
3. **एक-बार** (1d): सत्र स्थापना के बिना एकल-संदेश मोड

### Binding (बाइंडिंग) सहित NS संदेश (प्रकार 1b)

**उपयोग मामला**: स्ट्रीमिंग, उत्तर-योग्य डेटाग्राम, उत्तर की आवश्यकता वाले किसी भी प्रोटोकॉल

**कुल लंबाई**: 96 + payload_length बाइट्स

**प्रारूप**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड विवरण:**

**क्षणिक सार्वजनिक कुंजी** (32 बाइट, स्पष्ट-पाठ): - ऐलिस की एक-बार उपयोग वाली X25519 सार्वजनिक कुंजी - Elligator2 के साथ एन्कोड की गई (यादृच्छिक से अप्रभेद्य) - प्रत्येक NS message (NS संदेश) के लिए नई उत्पन्न की जाती है (कभी पुनः उपयोग नहीं होती) - लिटिल-एंडियन प्रारूप

**स्थैतिक कुंजी अनुभाग** (32 बाइट एन्क्रिप्टेड, 48 बाइट MAC (Message Authentication Code—संदेश प्रमाणीकरण कोड) के साथ): - Alice की X25519 (एलिप्टिक-कर्व कुंजी-अदला-बदली एल्गोरिथ्म) स्थैतिक सार्वजनिक कुंजी (32 बाइट) शामिल है - ChaCha20 (स्ट्रीम साइफर) से एन्क्रिप्टेड - Poly1305 MAC (16 बाइट) से प्रमाणीकृत - Bob द्वारा सत्र को Alice के destination से बाँधने के लिए प्रयुक्त

**पेलोड अनुभाग** (परिवर्ती लंबाई में एन्क्रिप्टेड, +16 बाइट MAC): - इसमें garlic cloves (garlic संदेश के उप-संदेश) और अन्य ब्लॉक शामिल होते हैं - पहले ब्लॉक के रूप में DateTime ब्लॉक शामिल होना चाहिए - सामान्यतः एप्लिकेशन डेटा वाले Garlic Clove blocks शामिल होते हैं - तुरंत ratchet (कुंजी-परिवर्तन तंत्र) के लिए NextKey ब्लॉक शामिल हो सकता है - ChaCha20 से एन्क्रिप्टेड - Poly1305 MAC (16 बाइट) से प्रमाणीकरण

**सुरक्षा गुणधर्म:** - अस्थायी कुंजी forward secrecy (आगे की गोपनीयता) घटक प्रदान करती है - स्थिर कुंजी Alice का प्रमाणीकरण करती है (गंतव्य से बाइंडिंग) - डोमेन पृथक्करण के लिए दोनों हिस्सों में अलग-अलग MACs (Message Authentication Codes) हैं - संपूर्ण हैंडशेक 2 DH ऑपरेशन (es, ss) करता है

### बाइंडिंग के बिना NS संदेश (प्रकार 1c)

**उपयोग मामला**: Raw datagrams (कनेक्शन-रहित पैकेट-आधारित संदेश) जहाँ किसी उत्तर की न अपेक्षा होती है और न इच्छा

**कुल लंबाई**: 96 + payload_length बाइट्स

**प्रारूप**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**मुख्य अंतर**: Flags Section (फ़्लैग्स अनुभाग) में स्थिर कुंजी की जगह शून्य के 32 बाइट्स होते हैं।

**Detection**: Bob 32-बाइट सेक्शन को डिक्रिप्ट करके और यह जांचकर कि सभी बाइट शून्य हैं, संदेश का प्रकार निर्धारित करता है: - सभी शून्य → Unbound session (बाइंड न किया हुआ सत्र) (प्रकार 1c) - गैर-शून्य → Bound session with static key (स्थिर कुंजी वाला बाउंड सत्र) (प्रकार 1b)

**गुण:** - static key (स्थिर कुंजी) न होने का मतलब Alice के गंतव्य से कोई बाइंडिंग नहीं होती - Bob उत्तर नहीं भेज सकता (कोई गंतव्य ज्ञात नहीं) - केवल 1 DH (Diffie-Hellman) ऑपरेशन (es) करता है - Noise "N" pattern (Noise प्रोटोकॉल का "N" पैटर्न) का अनुसरण करता है, "IK" के बजाय - जब उत्तर की कभी आवश्यकता नहीं होती, तब अधिक कुशल

**फ्लैग्स अनुभाग** (भविष्य में उपयोग के लिए सुरक्षित): वर्तमान में सभी मान शून्य हैं। भविष्य के संस्करणों में feature negotiation (फ़ीचर पर सहमति स्थापित करने की प्रक्रिया) के लिए उपयोग किया जा सकता है।

### NS एक-बार का संदेश (प्रकार 1d)

**उपयोग परिदृश्य**: बिना सत्र के और बिना उत्तर की अपेक्षा के एकल गुमनाम संदेश

**कुल लंबाई**: 96 + payload_length बाइट्स

**प्रारूप**: बाइंडिंग के बिना NS के समान (type 1c)

**अंतर**:  - Type 1c उसी सत्र में कई संदेश भेज सकता है (आगे ES संदेश आते हैं) - Type 1d सत्र स्थापना के बिना ठीक एक संदेश भेजता है - व्यवहार में, कार्यान्वयन प्रारम्भ में इन्हें समान रूप से मान सकते हैं

**विशेषताएँ:** - अधिकतम गुमनामी (कोई स्थिर कुंजी नहीं, कोई सत्र नहीं) - किसी भी पक्ष द्वारा सत्र स्थिति संग्रहीत नहीं की जाती - Noise "N" पैटर्न का अनुसरण करता है - एकल DH (Diffie-Hellman) ऑपरेशन (es)

### नया सेशन उत्तर (NSR) संदेश

Bob, Alice के NS संदेश के जवाब में, एक या अधिक NSR संदेश भेजता है। NSR, Noise IK handshake (प्रारंभिक सुरक्षित हैंडशेक) को पूर्ण करता है और द्विदिश सत्र स्थापित करता है।

**कुल लंबाई**: 72 + payload_length बाइट्स

**प्रारूप**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड विवरण:**

**सेशन टैग** (8 बाइट, सादा पाठ): - NSR tagset (टैगों का समूह) से उत्पन्न (KDF (Key Derivation Function, कुंजी व्युत्पन्न फलन) अनुभाग देखें) - इस उत्तर को Alice के NS संदेश से संबद्ध करता है - Alice को यह पहचानने देता है कि यह NSR किस NS का उत्तर है - एक-बार उपयोग (कभी पुन: उपयोग नहीं किया जाता)

**अस्थायी सार्वजनिक कुंजी** (32 बाइट्स, सादा-पाठ): - बॉब की एक-बार-प्रयोग वाली X25519 (कुंजी-विनिमय वक्र) सार्वजनिक कुंजी - Elligator2 (एन्कोडिंग योजना) से एन्कोड की गई - प्रत्येक NSR संदेश (एक विशेष संदेश प्रकार) के लिए नई उत्पन्न की जाती है - भेजे गए प्रत्येक NSR के लिए अलग होना आवश्यक है

**Key Section MAC** (16 बाइट्स): - खाली डेटा (ZEROLEN) को प्रमाणित करता है - Noise IK प्रोटोकॉल (se pattern) का हिस्सा - हैश प्रतिलेख को संबद्ध डेटा के रूप में उपयोग करता है - NSR को NS से बाँधने के लिए अत्यंत महत्वपूर्ण

**पेलोड सेक्शन** (परिवर्तनीय लंबाई): - इसमें garlic cloves (गार्लिक संदेश के उपघटक) और ब्लॉक्स शामिल होते हैं - आम तौर पर एप्लिकेशन-लेयर के प्रत्युत्तर शामिल होते हैं - खाली हो सकता है (ACK-only NSR) - अधिकतम आकार: 65519 bytes (65535 - 16 byte MAC)

**कई NSR संदेश:**

Bob एक NS के प्रत्युत्तर में अनेक NSR संदेश भेज सकता है:
- प्रत्येक NSR के पास एक अद्वितीय अस्थायी कुंजी होती है
- प्रत्येक NSR में एक अद्वितीय session tag (सत्र टैग) होता है
- Alice पहले प्राप्त NSR का उपयोग हैंडशेक पूरा करने के लिए करती है
- अन्य NSR रिडंडेंसी हैं (पैकेट लॉस की स्थिति में)

**महत्वपूर्ण समय-क्रम:** - Alice को ES संदेश भेजने से पहले एक NSR (एक संदेश प्रकार) प्राप्त करना चाहिए - Bob को ES संदेश भेजने से पहले एक ES संदेश प्राप्त करना चाहिए - NSR split() ऑपरेशन के माध्यम से द्विदिश सत्र कुंजियाँ स्थापित करता है

**सुरक्षा गुणधर्म:** - Noise IK handshake (Noise प्रोटोकॉल का IK हैंडशेक पैटर्न) पूरा करता है - 2 अतिरिक्त DH operations (Diffie-Hellman कुंजी-विनिमय क्रियाएँ) (ee, se) निष्पादित करता है - NS+NSR मिलाकर कुल 4 DH operations - द्विपक्षीय प्रमाणीकरण (स्तर 2) प्राप्त करता है - NSR पेलोड के लिए कमजोर फ़ॉरवर्ड सीक्रेसी (स्तर 4) प्रदान करता है

### विद्यमान सत्र (ES) संदेश

NS/NSR हैंडशेक के बाद सभी संदेश Existing Session (मौजूदा सत्र) प्रारूप का उपयोग करते हैं। ES संदेशों का उपयोग Alice और Bob दोनों द्वारा द्विदिश रूप से किया जाता है।

**कुल लंबाई**: 8 + payload_length + 16 बाइट (न्यूनतम 24 बाइट)

**प्रारूप**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड विवरण:**

**Session Tag** (8 बाइट, स्पष्ट-पाठ): - वर्तमान निर्गामी tagset से उत्पन्न - सत्र और संदेश संख्या की पहचान करता है - प्राप्तकर्ता टैग के आधार पर सत्र कुंजी और nonce (एक बार प्रयुक्त होने वाला यादृच्छिक मान) प्राप्त करता है - एक-बार उपयोग (प्रत्येक टैग का ठीक एक बार ही प्रयोग होता है) - प्रारूप: HKDF (HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन) आउटपुट के पहले 8 बाइट

**पेलोड अनुभाग** (परिवर्तनीय लंबाई): - इसमें garlic cloves (I2P में 'garlic encryption' के अंदर उप-संदेश इकाइयाँ) और ब्लॉक होते हैं - कोई अनिवार्य ब्लॉक नहीं (खाली हो सकता है) - सामान्य ब्लॉक: Garlic Clove, NextKey, ACK, ACK Request, Padding - अधिकतम आकार: 65519 bytes (65535 - 16 byte MAC)

**MAC** (16 बाइट्स): - Poly1305 प्रमाणीकरण टैग - पूरे पेलोड पर गणना की जाती है - संबद्ध डेटा: 8-बाइट का सेशन टैग - सही ढंग से सत्यापित होना आवश्यक है, अन्यथा संदेश अस्वीकार कर दिया जाता है

**टैग लुकअप प्रक्रिया:**

1. रिसीवर 8-बाइट टैग निकालता है
2. सभी वर्तमान आगत टैगसेट्स में टैग ढूँढता है
3. संबद्ध सेशन कुंजी और संदेश संख्या N प्राप्त करता है
4. नॉन्स (एक-बार प्रयुक्त मान) बनाता है: `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. AEAD (Authenticated Encryption with Associated Data - संबद्ध डेटा सहित प्रमाणीकरणयुक्त एन्क्रिप्शन) का उपयोग करते हुए, टैग को संबद्ध डेटा के रूप में लेकर पेलोड को डिक्रिप्ट करता है
6. टैगसेट से टैग हटाता है (एक-बार उपयोग)
7. डिक्रिप्ट किए गए ब्लॉक्स का प्रसंस्करण करता है

**Session Tag (सत्र टैग) नहीं मिला:**

यदि tag किसी भी tagset में नहीं मिलता है: - संभवतः NS संदेश → NS डिक्रिप्शन का प्रयास करें - संभवतः NSR संदेश → NSR डिक्रिप्शन का प्रयास करें - संभवतः out-of-order ES → tagset अपडेट के लिए थोड़ी देर प्रतीक्षा करें - संभवतः रीप्ले हमला → अस्वीकार करें - संभवतः दूषित डेटा → अस्वीकार करें

**रिक्त पेलोड:**

ES messages (एक विशेष प्रकार के संदेश) में खाली पेलोड (0 बाइट) हो सकते हैं: - जब ACK अनुरोध प्राप्त हो, तो यह स्पष्ट ACK के रूप में कार्य करता है - एप्लिकेशन डेटा के बिना प्रोटोकॉल-स्तर की प्रतिक्रिया प्रदान करता है - फिर भी एक session tag (सत्र टैग) का उपभोग करता है - जब उच्चतर लेयर के पास भेजने के लिए तत्काल डेटा न हो, तब उपयोगी

**सुरक्षा विशेषताएँ:** - NSR प्राप्त होने के बाद पूर्ण फॉरवर्ड सीक्रेसी (लेवल 5) - AEAD (एसोसिएटेड डेटा के साथ प्रमाणीकृत एन्क्रिप्शन) के माध्यम से प्रमाणीकृत एन्क्रिप्शन - टैग अतिरिक्त एसोसिएटेड डेटा के रूप में कार्य करता है - ratchet (क्रमिक कुंजी-अपडेट तंत्र) आवश्यक होने से पहले प्रति tagset अधिकतम 65535 संदेश

---

## कुंजी व्युत्पत्ति फलन

यह अनुभाग ECIES (दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) में प्रयुक्त सभी KDF (कुंजी-व्युत्पत्ति फ़ंक्शन) क्रियाओं का प्रलेखन करता है, तथा पूर्ण क्रिप्टोग्राफ़िक व्युत्पत्तियाँ प्रदर्शित करता है।

### प्रतीक-विधान और स्थिरांक

**स्थिरांक:** - `ZEROLEN` - शून्य-लंबाई बाइट ऐरे (रिक्त स्ट्रिंग) - `||` - संयोजन ऑपरेटर

**वेरिएबल्स:** - `h` - रनिंग हैश ट्रांस्क्रिप्ट (32 बाइट्स) - `chainKey` - HKDF के लिए चेनिंग की (32 बाइट्स) - `k` - सममित सिफर कुंजी (32 बाइट्स) - `n` - Nonce (एक-बार प्रयुक्त यादृच्छिक संख्या) / संदेश संख्या

**कुंजियाँ:** - `ask` / `apk` - Alice की स्थिर निजी/सार्वजनिक कुंजी - `aesk` / `aepk` - Alice की अस्थायी निजी/सार्वजनिक कुंजी - `bsk` / `bpk` - Bob की स्थिर निजी/सार्वजनिक कुंजी - `besk` / `bepk` - Bob की अस्थायी निजी/सार्वजनिक कुंजी

### NS संदेश के लिए कुंजी व्युत्पत्ति फलन

### KDF 1: प्रारंभिक श्रृंखला कुंजी

प्रोटोकॉल प्रारंभ पर केवल एक बार किया जाता है (पूर्व-गणना की जा सकती है):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**परिणाम:** - `chainKey` = सभी आगामी KDFs (कुंजी व्युत्पत्ति फलन) के लिए प्रारंभिक चेनिंग कुंजी - `h` = प्रारंभिक ट्रांस्क्रिप्ट हैश

### KDF 2 (कुंजी व्युत्पन्न फ़ंक्शन): Bob की स्थिर कुंजी का मिश्रण

Bob यह कार्य एक बार करता है (इसे सभी इनबाउंड सत्रों के लिए पहले से गणना किया जा सकता है):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: ऐलिस की अस्थायी कुंजी उत्पत्ति

Alice प्रत्येक NS संदेश के लिए नई कुंजियाँ उत्पन्न करती है:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF (कुंजी व्युत्पत्ति फ़ंक्शन) 4: NS स्थिर कुंजी अनुभाग (es DH)

एलिस की स्थिर कुंजी को एन्क्रिप्ट करने के लिए कुंजियाँ व्युत्पन्न करता है:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF (कुंजी व्युत्पत्ति फ़ंक्शन) 5: NS पेलोड अनुभाग (ss DH (स्टैटिक-स्टैटिक डिफी-हेलमैन), केवल बाइंड)

बाउंड सत्रों के लिए, पेलोड एन्क्रिप्शन हेतु दूसरा DH (Diffie-Hellman कुंजी विनिमय) करें:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**महत्वपूर्ण टिप्पणियाँ:**

1. **Bound बनाम Unbound**: 
   - Bound 2 DH (Diffie-Hellman कुंजी-विनिमय) ऑपरेशन करता है (es + ss)
   - Unbound 1 DH ऑपरेशन करता है (केवल es)
   - Unbound नई key (कुंजी) व्युत्पन्न करने के बजाय nonce (एक बार उपयोग होने वाला मान) को बढ़ाता है

2. **कुंजी पुन:उपयोग सुरक्षा**:
   - भिन्न nonce (एक-बार उपयोग होने वाली संख्या) मान (0 बनाम 1) कुंजी/nonce के पुन:उपयोग को रोकते हैं
   - भिन्न संबद्ध डेटा (h अलग है) डोमेन पृथक्करण प्रदान करता है

3. **हैश ट्रांसक्रिप्ट**:
   - `h` में अब शामिल हैं: protocol_name, empty prologue, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - यह ट्रांसक्रिप्ट NS संदेश के सभी भागों को एक साथ बाँधता है

### NSR उत्तर टैगसेट कुंजी व्युत्पन्न फ़ंक्शन

Bob NSR संदेशों (NSR नामक संदेश प्रकार) के लिए टैग उत्पन्न करता है:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### NSR संदेश कुंजी व्युत्पत्ति फ़ंक्शन

### KDF 6: NSR अस्थायी कुंजी सृजन

Bob प्रत्येक NSR के लिए एक नई ephemeral key (क्षणिक कुंजी) उत्पन्न करता है:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: NSR कुंजी अनुभाग (ee और se DH (Diffie-Hellman कुंजी-विनिमय))

NSR key section (NSR का कुंजी अनुभाग) के लिए कुंजियाँ व्युत्पन्न करता है:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**महत्वपूर्ण**: यह Noise IK handshake (Noise प्रोटोकॉल का IK हैंडशेक) को पूरा करता है। `chainKey` में अब सभी 4 DH ऑपरेशन्स (es, ss, ee, se) का योगदान शामिल है।

### KDF 8: NSR पेलोड अनुभाग

NSR पेलोड एन्क्रिप्शन हेतु कुंजियाँ व्युत्पन्न करता है:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**महत्वपूर्ण टिप्पणियाँ:**

1. **विभाजन ऑपरेशन**:
   - प्रत्येक दिशा के लिए स्वतंत्र कुंजियाँ बनाता है
   - Alice→Bob और Bob→Alice के बीच कुंजियों के पुन: उपयोग को रोकता है

2. **NSR पेलोड बाइंडिंग**:
   - हैंडशेक से पेलोड को बांधने के लिए `h` को associated data (संबद्ध डेटा) के रूप में उपयोग करता है
   - अलग KDF ("AttachPayloadKDF") domain separation (डोमेन पृथक्करण) प्रदान करता है

3. **ES तत्परता**:
   - NSR के बाद, दोनों पक्ष ES संदेश भेज सकते हैं
   - Alice को ES भेजने से पहले NSR प्राप्त करना होगा
   - Bob को ES भेजने से पहले ES प्राप्त करना होगा

### ES संदेश KDFs (Key Derivation Functions, कुंजी व्युत्पत्ति फ़ंक्शन)

ES संदेश टैगसेट्स से पूर्व-उत्पन्न सत्र कुंजियों का उपयोग करते हैं:

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**प्राप्तकर्ता प्रक्रिया:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### DH_INITIALIZE फ़ंक्शन

एक दिशा के लिए एक tagset (टैग्स का समूह) बनाता है:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**उपयोग संदर्भ:**

1. **NSR Tagset (NSR टैगसेट)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets (ES टैगसेट्स)**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted Tagsets (रैचेटेड टैगसेट्स)**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## रैचेट (क्रिप्टोग्राफ़िक कुंजी अद्यतन तंत्र) यंत्रणाएँ

ECIES (Elliptic Curve Integrated Encryption Scheme—एलिप्टिक कर्व आधारित एकीकृत एन्क्रिप्शन योजना) forward secrecy और कुशल सत्र प्रबंधन प्रदान करने के लिए तीन समकालिक ratchet तंत्रों का उपयोग करता है।

### Ratchet (क्रिप्टोग्राफी में क्रमिक कुंजी-अद्यतन तंत्र) का अवलोकन

**तीन Ratchet (कुंजी-अग्रसारण तंत्र) प्रकार:**

1. **DH Ratchet** (क्रमिक कुंजी-अपडेट तंत्र): नई रूट कुंजियाँ उत्पन्न करने के लिए Diffie-Hellman कुंजी विनिमय करता है
2. **Session Tag Ratchet** (Session tags: अस्थायी, एक-बार-उपयोग पहचान टैग): नियतात्मक रूप से एक-बार-उपयोग session tags व्युत्पन्न करता है
3. **Symmetric Key Ratchet**: संदेश एन्क्रिप्शन के लिए सत्र कुंजियाँ व्युत्पन्न करता है

**संबंध:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**मुख्य गुणधर्म:**

- **प्रेषक**: आवश्यकतानुसार टैग और कुंजियाँ बनाता है (संग्रहण की आवश्यकता नहीं)
- **ग्राही**: look-ahead window (अग्र-दृष्टि विंडो) के लिए टैग पहले से बनाता है (संग्रहण आवश्यक)
- **समकालिकता**: टैग सूचकांक कुंजी सूचकांक निर्धारित करता है (N_tag = N_key)
- **फॉरवर्ड सीक्रेसी**: आवधिक DH ratchet (Diffie-Hellman आधारित रैचेट तंत्र) के माध्यम से प्राप्त
- **दक्षता**: ग्राही टैग प्राप्त होने तक कुंजी गणना स्थगित कर सकता है

### DH Ratchet (डिफी-हेल्मन रैचेट, संदेश-दर-संदेश कुंजी बदलने वाला तंत्र)

DH ratchet (Diffie-Hellman आधारित क्रमिक कुंजी-अपडेट तंत्र) समय-समय पर नई अल्पकालिक कुंजियों का आदान-प्रदान करके फॉरवर्ड सीक्रेसी प्रदान करता है।

### DH Ratchet (Diffie-Hellman आधारित क्रमिक कुंजी-अद्यतन तंत्र) की आवृत्ति

**आवश्यक Ratchet (क्रमिक कुंजी-अपडेट तंत्र) शर्तें:** - टैग सेट समाप्ति के करीब (टैग 65535 अधिकतम है) - कार्यान्वयन-विशिष्ट नीतियाँ:   - संदेशों की संख्या की सीमा (उदा., हर 4096 संदेशों पर)   - समय सीमा (उदा., हर 10 मिनट में)   - डेटा मात्रा सीमा (उदा., हर 100 MB पर)

**अनुशंसित पहला Ratchet (क्रिप्टोग्राफ़िक रैचेट तंत्र)**: सीमा तक पहुँचने से बचने के लिए टैग नंबर 4096 के आसपास

**अधिकतम मान:** - **अधिकतम tag set (टैग का समूह) ID**: 65535 - **अधिकतम कुंजी ID**: 32767 - **प्रति tag set अधिकतम संदेश**: 65535 - **प्रति सत्र सैद्धांतिक अधिकतम डेटा**: ~6.9 TB (64K tag sets × 64K messages × 1730 बाइट औसत)

### DH Ratchet (Diffie-Hellman आधारित कुंजी-घुमाव तंत्र) के टैग और कुंजी पहचानकर्ता

**प्रारंभिक टैग सेट** (हैंडशेक के बाद): - टैग सेट ID: 0 - अभी तक कोई NextKey (अगली कुंजी) ब्लॉक नहीं भेजे गए हैं - कोई कुंजी ID आवंटित नहीं की गई है

**पहले Ratchet (क्रमिक-अपडेट एन्क्रिप्शन तंत्र) के बाद**: - टैग सेट आईडी: 1 = (1 + एलिस की कुंजी आईडी + बॉब की कुंजी आईडी) = (1 + 0 + 0) - एलिस कुंजी आईडी 0 के साथ NextKey भेजती है - बॉब कुंजी आईडी 0 के साथ NextKey भेजकर उत्तर देता है

**परवर्ती टैग सेट**: - टैग सेट ID = 1 + प्रेषक की कुंजी ID + प्राप्तकर्ता की कुंजी ID - उदाहरण: टैग सेट 5 = (1 + sender_key_2 + receiver_key_2)

**टैग सेट प्रगति तालिका:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = इस ratchet (क्रमिक कुंजी-अग्रसारण तंत्र) में नई कुंजी उत्पन्न की गई

**Key ID नियम:** - ID 0 से शुरू होकर क्रमिक होते हैं - ID में वृद्धि केवल तब होती है जब नई कुंजी उत्पन्न की जाती है - अधिकतम कुंजी ID 32767 (15 बिट) है - कुंजी ID 32767 के बाद नया सत्र आवश्यक है

### DH Ratchet (डिफी-हेलमैन रैचेट) संदेश प्रवाह

**भूमिकाएँ:** - **टैग प्रेषक**: आउटबाउंड टैग सेट का स्वामी होता है, संदेश भेजता है - **टैग प्राप्तकर्ता**: इनबाउंड टैग सेट का स्वामी होता है, संदेश प्राप्त करता है

**पैटर्न:** टैग प्रेषक ratchet (क्रिप्टोग्राफ़िक आगे-खिसकने वाली कुंजी-अद्यतन प्रक्रिया) तब आरंभ करता है जब टैग सेट लगभग समाप्त हो जाता है।

**संदेश प्रवाह आरेख:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**रैचेट पैटर्न:**

**सम-संख्या वाले टैग सेट बनाना** (2, 4, 6, ...): 1. प्रेषक नई कुंजी उत्पन्न करता है 2. प्रेषक नई कुंजी के साथ NextKey ब्लॉक भेजता है 3. प्राप्तकर्ता पुरानी कुंजी ID के साथ NextKey ब्लॉक भेजता है (ACK) 4. दोनों (नई प्रेषक कुंजी × पुरानी प्राप्तकर्ता कुंजी) के साथ DH (Diffie-Hellman कुंजी-विनिमय) करते हैं

**विषम-संख्या वाले Tag Sets (टैग सेट) का निर्माण** (3, 5, 7, ...): 1. प्रेषक रिवर्स कुंजी का अनुरोध करता है (अनुरोध फ़्लैग के साथ NextKey भेजता है) 2. प्राप्तकर्ता नई कुंजी उत्पन्न करता है 3. प्राप्तकर्ता नई कुंजी के साथ NextKey ब्लॉक भेजता है 4. दोनों (प्रेषक की पुरानी कुंजी × प्राप्तकर्ता की नई कुंजी) के साथ DH (Diffie-Hellman कुंजी-विनिमय) करते हैं

### NextKey ब्लॉक प्रारूप

विस्तृत NextKey ब्लॉक विनिर्देश के लिए Payload Format अनुभाग देखें।

**मुख्य तत्व:** - **फ्लैग्स बाइट**:   - बिट 0: कुंजी मौजूद (1) या केवल ID (0)   - बिट 1: रिवर्स कुंजी (1) या फॉरवर्ड कुंजी (0)   - बिट 2: रिवर्स कुंजी का अनुरोध (1) या कोई अनुरोध नहीं (0) - **कुंजी ID**: 2 बाइट, big-endian (सबसे-महत्त्वपूर्ण-बाइट-प्रथम क्रम) (0-32767) - **सार्वजनिक कुंजी**: 32 बाइट X25519 (यदि बिट 0 = 1)

**NextKey Blocks (NextKey ब्लॉक्स) के उदाहरण:**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### DH Ratchet KDF (DH रैचेट आधारित कुंजी व्युत्पन्न फ़ंक्शन)

जब नई कुंजियों का आदान-प्रदान होता है:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**महत्त्वपूर्ण समय-निर्धारण:**

**टैग प्रेषक:** - तुरंत नया आउटबाउंड टैग सेट बनाता है - तुरंत नए टैग का उपयोग शुरू करता है - पुराना आउटबाउंड टैग सेट हटाता है

**टैग रिसीवर:** - नया इनबाउंड टैग सेट बनाता है - grace period (अनुग्रह अवधि) (3 मिनट) के लिए पुराने इनबाउंड टैग सेट को बनाए रखता है - grace period के दौरान पुराने और नए दोनों टैग सेट से टैग स्वीकार करता है - grace period के बाद पुराने इनबाउंड टैग सेट को हटा देता है

### DH Ratchet (Diffie-Hellman आधारित रैचेट) की स्थिति का प्रबंधन

**प्रेषक की स्थिति:** - वर्तमान आउटबाउंड टैग सेट - टैग सेट ID और कुंजी IDs - अगली रूट कुंजी (अगले ratchet (क्रमिक कुंजी-परिवर्तन प्रक्रिया) के लिए) - वर्तमान टैग सेट में संदेशों की संख्या

**प्राप्तकर्ता स्थिति:** - वर्तमान इनबाउंड टैग सेट (अनुग्रह अवधि के दौरान 2 हो सकते हैं) - पिछले संदेशों की संख्याएँ (PN) अंतर का पता लगाने के लिए - पहले से जनित टैगों की लुक-अहेड विंडो - अगली रूट कुंजी (अगले ratchet (क्रमिक कुंजी-परिवर्तन तंत्र) के लिए)

**स्टेट ट्रांज़िशन नियम:**

1. **प्रथम रैचेट से पहले**:
   - टैग सेट 0 (NSR से) का उपयोग
   - कोई कुंजी ID आवंटित नहीं किए गए हैं

2. **Ratchet (क्रमिक कुंजी-परिवर्तन तंत्र) आरंभ करना**:
   - नई कुंजी उत्पन्न करें (यदि इस दौर में प्रेषक उत्पन्न कर रहा हो)
   - ES message में NextKey block भेजें
   - नई outbound tag set (प्रेषित दिशा में उपयोग होने वाला टैग-समूह) बनाने से पहले NextKey reply की प्रतीक्षा करें

3. **Ratchet Request (क्रमिक कुंजी-परिवर्तन अनुरोध) प्राप्त करना**:
   - नई कुंजी उत्पन्न करें (यदि इस राउंड में रिसीवर उत्पन्न कर रहा है)
   - प्राप्त कुंजी के साथ DH (Diffie-Hellman कुंजी आदान-प्रदान) करें
   - नया inbound tag set (आने वाले संदेशों के लिए टैग समूह) बनाएँ
   - NextKey (अगली-कुंजी) उत्तर भेजें
   - अनुग्रह अवधि के लिए पुराना inbound tag set बनाए रखें

4. **Ratchet (क्रिप्टोग्राफ़िक रैचेट) का समापन**:
   - NextKey उत्तर प्राप्त करें
   - डिफ़ी-हेलमैन (DH) करें
   - नया आउटबाउंड टैग सेट बनाएं
   - नए टैग का उपयोग शुरू करें

### सेशन टैग रैचेट

session tag ratchet (session tags उत्पन्न करने वाला तंत्र) नियतात्मक रूप से एक-बार-उपयोग वाले 8-बाइट session tags उत्पन्न करता है।

### Session Tag Ratchet (एक प्रगतिशील कुंजी-अद्यतन तंत्र) का उद्देश्य

- स्पष्ट टैग प्रेषण को प्रतिस्थापित करता है (ElGamal 32-बाइट टैग भेजता था)
- प्राप्तकर्ता को look-ahead window (आगे की झलक के लिए विंडो) हेतु टैग पहले से उत्पन्न करने में सक्षम बनाता है
- प्रेषक मांग पर उत्पन्न करता है (भंडारण की आवश्यकता नहीं)
- सूचकांक के माध्यम से symmetric key ratchet (सममित कुंजी के क्रमिक-अपडेट तंत्र) के साथ समकालित होता है

### Session Tag Ratchet (क्रमिक अद्यतन तंत्र) सूत्र

**आरंभीकरण:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**टैग जनरेशन (टैग N के लिए):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**पूर्ण अनुक्रम:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Session Tag Ratchet (क्रमिक कुंजी-अद्यतन तंत्र) प्रेषक का कार्यान्वयन

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**प्रेषक प्रक्रिया:** 1. प्रत्येक संदेश के लिए `get_next_tag()` कॉल करें 2. ES संदेश में लौटा हुआ टैग का उपयोग करें 3. संभावित ACK (पुष्टिकरण) ट्रैकिंग के लिए इंडेक्स N सहेजें 4. टैग को संग्रहीत करने की आवश्यकता नहीं (आवश्यकतानुसार उत्पन्न किया जाता है)

### Session Tag Ratchet (सेशन टैग के लिए कुंजी आगे बढ़ाने वाला तंत्र) रिसीवर कार्यान्वयन

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**रिसीवर प्रक्रिया:** 1. लुक-अहेड विंडो के लिए पहले से टैग जनरेट करें (उदा., 32 टैग) 2. टैग को हैश टेबल या डिक्शनरी में संग्रहीत करें 3. जब संदेश आए, तो टैग ढूंढकर इंडेक्स N प्राप्त करें 4. स्टोरेज से टैग हटाएँ (एक बार उपयोग) 5. यदि टैग की संख्या सीमा से नीचे गिर जाए, तो विंडो का विस्तार करें

### Session Tag (सेशन टैग) लुक-अहेड रणनीति

**उद्देश्य**: मेमोरी उपयोग और out-of-order message handling (संदेशों को आगमन-क्रम से हटकर संसाधित करना) के बीच संतुलन

**अनुशंसित Look-Ahead (पूर्व-दृष्टि) आकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**अनुकूली लुक-अहेड:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**पीछे से ट्रिम:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**मेमोरी गणना:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### सेशन टैग की आउट-ऑफ-ऑर्डर (क्रम से बाहर) हैंडलिंग

**परिदृश्य**: संदेश क्रम से बाहर पहुँचते हैं

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**प्राप्तकर्ता का व्यवहार:**

1. tag_5 प्राप्त करें:
   - खोजें: इंडेक्स 5 पर मिला
   - संदेश संसाधित करें
   - tag_5 हटाएँ
   - अधिकतम प्राप्त: 5

2. tag_7 प्राप्त करें (क्रम से बाहर):
   - खोजें: index 7 पर मिला
   - संदेश संसाधित करें
   - tag_7 हटाएँ
   - उच्चतम प्राप्त: 7
   - नोट: tag_6 अभी भी भंडारण में है (अभी तक प्राप्त नहीं हुआ)

3. tag_6 प्राप्त करें (विलंबित):
   - खोजें: सूचकांक 6 पर मिला
   - संदेश संसाधित करें
   - tag_6 हटाएँ
   - अब तक प्राप्त उच्चतम: 7 (अपरिवर्तित)

4. tag_8 प्राप्त करें:
   - खोजें: इंडेक्स 8 पर मिला
   - संदेश संसाधित करें
   - tag_8 हटाएँ
   - सर्वाधिक प्राप्त: 8

**विंडो रखरखाव:** - उच्चतम प्राप्त इंडेक्स का ट्रैक रखें - लापता इंडेक्स (अंतराल) की सूची बनाए रखें - उच्चतम इंडेक्स के आधार पर विंडो का विस्तार करें - वैकल्पिक: टाइमआउट के बाद पुराने अंतरालों को समाप्त करें

### सममित कुंजी रैचेट

symmetric key ratchet (कुंजियों को क्रमिक रूप से अद्यतन करने की प्रक्रिया) 32-byte की एन्क्रिप्शन कुंजियाँ उत्पन्न करती है, जो session tags के साथ समकालित होती हैं।

### Symmetric Key Ratchet (क्रमिक कुंजी-परिवर्तन तंत्र) का उद्देश्य

- प्रत्येक संदेश के लिए एक विशिष्ट एन्क्रिप्शन कुंजी प्रदान करता है
- Session tag ratchet (कुंजी-क्रम आगे बढ़ाने का तंत्र) के साथ समकालित (वही सूचकांक)
- प्रेषक आवश्यकतानुसार उत्पन्न कर सकता है
- प्राप्तकर्ता टैग प्राप्त होने तक उत्पन्न करना स्थगित कर सकता है

### सममित कुंजी Ratchet (क्रमिक कुंजी-अद्यतन तंत्र) का सूत्र

**आरंभिकरण:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**कुंजी निर्माण (कुंजी N के लिए):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**पूर्ण अनुक्रम:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### सममित कुंजी रैचेट प्रेषक कार्यान्वयन

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**प्रेषक प्रक्रिया:** 1. अगला टैग और उसका सूचकांक N प्राप्त करें 2. सूचकांक N के लिए कुंजी उत्पन्न करें 3. संदेश को एन्क्रिप्ट करने के लिए कुंजी का उपयोग करें 4. कुंजी भंडारण की आवश्यकता नहीं

### सममित कुंजी Ratchet (क्रमिक कुंजी-परिवर्तन तंत्र) प्राप्तकर्ता का कार्यान्वयन

**रणनीति 1: Deferred Generation (स्थगित सृजन) (अनुशंसित)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**विलंबित जनरेशन प्रक्रिया:** 1. टैग के साथ ES संदेश प्राप्त करें 2. सूचकांक N प्राप्त करने के लिए टैग का लुकअप करें 3. कुंजियाँ 0 से N तक उत्पन्न करें (यदि पहले से उत्पन्न न हों) 4. संदेश को डिक्रिप्ट करने के लिए कुंजी N का उपयोग करें 5. अब श्रृंखला कुंजी सूचकांक N पर स्थित है

**लाभ:** - मेमोरी का न्यूनतम उपयोग - कुंजियाँ केवल आवश्यकता होने पर ही बनाई जाती हैं - सरल कार्यान्वयन

**कमियाँ:** - पहली बार उपयोग पर 0 से N तक सभी कुंजियाँ उत्पन्न करनी होंगी - कैशिंग के बिना क्रम से बाहर (out-of-order) संदेशों को संभाल नहीं सकता

**रणनीति 2: टैग विंडो के साथ पूर्व-सृजन (वैकल्पिक)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**पूर्व-सृजन प्रक्रिया:** 1. टैग विंडो से मेल खाने वाली कुंजियाँ पहले से उत्पन्न करें (उदा., 32 कुंजियाँ) 2. संदेश संख्या के आधार पर इंडेक्स की गई कुंजियाँ संग्रहीत करें 3. जब टैग प्राप्त हो, तो संबंधित कुंजी ढूँढें 4. टैग उपयोग होने पर विंडो का विस्तार करें

**फायदे:** - क्रम से बाहर आने वाले संदेशों को स्वाभाविक रूप से संभालता है - तेज़ कुंजी प्राप्ति (सृजन में कोई देरी नहीं)

**कमियां:** - अधिक मेमोरी उपयोग (प्रति कुंजी 32 बाइट्स बनाम प्रति टैग 8 बाइट्स) - कुंजियों को टैगों के साथ समकालित रखना आवश्यक है

**मेमोरी तुलना:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Session Tags (सत्र टैग्स) के साथ सममित रैचेट का समकालन

**महत्वपूर्ण आवश्यकता**: सेशन टैग का इंडेक्स सममित कुंजी के इंडेक्स के बराबर होना अनिवार्य है

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**विफलता के प्रकार:**

यदि समकालन टूट जाए: - decryption (डिक्रिप्शन) के लिए गलत कुंजी का उपयोग - MAC verification (मैसेज ऑथेंटिकेशन कोड सत्यापन) विफल - संदेश अस्वीकार कर दिया गया

**निवारण:** - टैग और कुंजी के लिए हमेशा एक ही सूचकांक का उपयोग करें - किसी भी ratchet (क्रमिक-परिवर्तन तंत्र) में सूचकांकों को कभी न छोड़ें - क्रम से बाहर आए संदेशों को सावधानीपूर्वक संभालें

### सममित Ratchet (कुंजी-अद्यतन तंत्र) Nonce (एक बार प्रयुक्त होने वाला यादृच्छिक मान) निर्माण

Nonce (cryptography में एक बार उपयोग होने वाली संख्या) संदेश संख्या से व्युत्पन्न किया जाता है:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**उदाहरण:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**महत्वपूर्ण गुण:** - Nonce (एकबारगी प्रयुक्त मान) किसी tagset (टैग का समूह) में प्रत्येक संदेश के लिए अद्वितीय होते हैं - Nonce कभी दोहराए नहीं जाते (एक-बार-उपयोग टैग यह सुनिश्चित करते हैं) - 8-बाइट काउंटर 2^64 संदेशों की अनुमति देता है (हम केवल 2^16 का उपयोग करते हैं) - Nonce का फ़ॉर्मेट RFC 7539 की काउंटर-आधारित संरचना से मेल खाता है

---

## सत्र प्रबंधन

### सत्र संदर्भ

सभी इनबाउंड और आउटबाउंड सत्र किसी विशिष्ट संदर्भ से संबंधित होने चाहिए:

1. **Router Context**: router के स्वयं उपयोग के लिए सत्र
2. **Destination Context**: किसी विशिष्ट स्थानीय Destination (क्लाइंट एप्लिकेशन) के लिए सत्र

**महत्वपूर्ण नियम**: कोरिलेशन हमलों को रोकने के लिए संदर्भों के बीच सेशनों को कभी भी साझा नहीं किया जाना चाहिए।

**कार्यान्वयन:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Java I2P कार्यान्वयन:**

Java I2P में, `SessionKeyManager` क्लास यह कार्यक्षमता प्रदान करता है: - प्रति router एक `SessionKeyManager` - प्रत्येक स्थानीय destination (गंतव्य) के लिए एक `SessionKeyManager` - प्रत्येक संदर्भ के भीतर ECIES और ElGamal सत्रों का अलग-अलग प्रबंधन

### सेशन बाइंडिंग

**Binding (बाइंडिंग)** किसी सत्र को किसी विशिष्ट दूरस्थ गंतव्य से संबद्ध करती है।

### बंधित सत्र

**विशेषताएँ:** - NS संदेश में प्रेषक की स्थिर कुंजी शामिल होती है - प्राप्तकर्ता प्रेषक के गंतव्य की पहचान कर सकता है - द्विदिश संचार सक्षम करता है - प्रति गंतव्य एकल आउटबाउंड सत्र - एकाधिक इनबाउंड सत्र हो सकते हैं (संक्रमण के दौरान)

**उपयोग के मामले:** - स्ट्रीमिंग कनेक्शन (TCP जैसा) - उत्तर-सक्षम डेटाग्राम - कोई भी प्रोटोकॉल जिसे अनुरोध/प्रतिक्रिया की आवश्यकता हो

**बाइंडिंग प्रक्रिया:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**लाभ:** 1. **Ephemeral-Ephemeral DH** (अस्थायी-कुंजियों वाला Diffie-Hellman): उत्तर ee DH का उपयोग करता है (पूर्ण फॉरवर्ड सीक्रेसी) 2. **सत्र निरंतरता**: Ratchets (कुंजी-अग्रसरण तंत्र) उसी गंतव्य से जुड़ाव बनाए रखते हैं 3. **सुरक्षा**: सत्र हाइजैकिंग को रोकता है (स्थिर कुंजी द्वारा प्रमाणित) 4. **दक्षता**: प्रति गंतव्य एक ही सत्र (डुप्लीकेशन नहीं)

### Unbound सत्र

**विशेषताएँ:** - NS message में कोई स्थिर कुंजी नहीं (flags अनुभाग में सभी शून्य) - प्राप्तकर्ता प्रेषक की पहचान नहीं कर सकता - केवल एक-तरफ़ा संचार - एक ही गंतव्य के लिए एकाधिक सत्रों की अनुमति है

**उपयोग के मामले:** - रॉ डेटाग्राम (भेजें और भूल जाएँ) - अनाम प्रकाशन - प्रसारण-शैली संदेश भेजना

**विशेषताएँ:** - अधिक गुमनाम (प्रेषक की पहचान नहीं होती) - अधिक दक्ष (हैंडशेक में 1 DH (Diffie-Hellman कुंजी-विनिमय) बनाम 2 DH) - उत्तर संभव नहीं (प्राप्तकर्ता को यह नहीं पता कि कहाँ उत्तर देना है) - session ratcheting नहीं (क्रमिक कुंजी-परिवर्तन तंत्र; एक बार या सीमित उपयोग)

### सत्र युग्मन

**पेयरिंग** द्विदिश संचार के लिए एक इनबाउंड सत्र को एक आउटबाउंड सत्र से जोड़ती है।

### युग्मित सत्र बनाना

**एलिस का दृष्टिकोण (प्रारंभकर्ता):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bob का दृष्टिकोण (responder, उत्तरदाता):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Session Pairing (सत्र पेयरिंग) के लाभ

1. **इन-बैंड ACKs**: अलग clove (garlic संदेश का उप-भाग) के बिना संदेशों की पुष्टि की जा सकती है
2. **Efficient Ratcheting (कुंजी-अपडेट तंत्र)**: दोनों दिशाओं का रैचेट एक-साथ आगे बढ़ता है
3. **फ़्लो कंट्रोल**: युग्मित सत्रों के पार back-pressure (उल्टा-दबाव आधारित नियंत्रण) लागू किया जा सकता है
4. **स्टेट कंसिस्टेंसी**: समकालित अवस्था बनाए रखना आसान होता है

### सत्र युग्मन के नियम

- आउटबाउंड सत्र अयुग्मित हो सकता है (अबंधित NS)
- बंधित NS के लिए इनबाउंड सत्र युग्मित होना चाहिए
- युग्मन सत्र निर्माण के समय होता है, बाद में नहीं
- युग्मित सत्रों में समान गंतव्य बाइंडिंग होती है
- Ratchets (कुंजी-रोलओवर तंत्र) स्वतंत्र रूप से होते हैं, लेकिन समन्वित रहते हैं

### सत्र जीवनचक्र

### सत्र जीवनचक्र: निर्माण चरण

**निर्गामी सत्र निर्माण (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**इनबाउंड सत्र निर्माण (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### सत्र जीवनचक्र: सक्रिय चरण

**स्थिति संक्रमण:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**सक्रिय सत्र रखरखाव:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### सत्र जीवनचक्र: समाप्ति चरण

**सत्र समय-सीमा मान:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**अवधि-समाप्ति तर्क:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**महत्वपूर्ण नियम**: समकालिकता भंग से बचाने के लिए आउटबाउंड सत्र इनबाउंड सत्रों से पहले अवश्य समाप्त होने चाहिए।

**सुचारू समापन:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### कई NS संदेश

**परिदृश्य**: ऐलिस का NS संदेश (एक संदेश प्रकार) खो जाता है या NSR उत्तर (एक संदेश प्रकार) खो जाता है।

**ऐलिस का व्यवहार:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**महत्वपूर्ण गुण:**

1. **अद्वितीय अस्थायी कुंजियाँ**: प्रत्येक NS एक भिन्न अस्थायी कुंजी का उपयोग करता है
2. **स्वतंत्र हैंडशेक्स**: प्रत्येक NS अलग हैंडशेक स्टेट बनाता है
3. **NSR सहसंबंध**: NSR टैग यह पहचानता है कि वह किस NS को उत्तर देता है
4. **स्टेट क्लीनअप**: अप्रयुक्त NS स्टेट्स सफल NSR के बाद हटा दिए जाते हैं

**हमलों की रोकथाम:**

संसाधन समाप्ति को रोकने के लिए:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### कई NSR संदेश

**परिदृश्य**: बॉब कई NSR भेजता है (उदाहरण के लिए, उत्तर डेटा कई संदेशों में विभाजित)।

**Bob का व्यवहार:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**एलिस का व्यवहार:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bob की सफाई:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**महत्वपूर्ण गुणधर्म:**

1. **एकाधिक NSR अनुमत हैं**: बॉब प्रति NS कई NSR भेज सकता है
2. **अलग-अलग अस्थायी कुंजियाँ (ephemeral keys)**: प्रत्येक NSR को एक अद्वितीय अस्थायी कुंजी का उपयोग करना चाहिए
3. **एक ही NSR tagset**: एक NS के लिए सभी NSR एक ही tagset (टैगों का समूह) का उपयोग करते हैं
4. **पहला ES प्रभावी होता है**: ऐलिस का पहला ES तय करता है कि कौन-सा NSR सफल हुआ
5. **ES के बाद साफ-सफाई**: ES प्राप्त होने के बाद बॉब अनुपयोगी स्टेट्स (स्थिति जानकारी) त्याग देता है

### सत्र स्टेट मशीन

**पूर्ण अवस्था आरेख:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**स्थिति विवरण:**

- **NEW**: आउटबाउंड सत्र बनाया गया, अभी तक कोई NS नहीं भेजा गया
- **PENDING_REPLY**: NS भेजा, NSR की प्रतीक्षा
- **AWAITING_ES**: NSR भेजा, Alice से पहले ES की प्रतीक्षा
- **ESTABLISHED**: हैंडशेक पूर्ण, ES भेजना/प्राप्त करना संभव है
- **ACTIVE**: ES संदेशों का सक्रिय रूप से आदान-प्रदान हो रहा है
- **RATCHETING**: DH ratchet (Diffie-Hellman आधारित क्रमिक कुंजी-परिवर्तन प्रक्रिया) जारी है (ACTIVE का उपसमुच्चय)
- **EXPIRED**: सत्र का समय समाप्त, हटाए जाने की प्रतीक्षा में
- **TERMINATED**: सत्र को स्पष्ट रूप से समाप्त किया गया

---

## पेलोड प्रारूप

सभी ECIES (Elliptic Curve Integrated Encryption Scheme, दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) संदेशों (NS, NSR, ES) का पेलोड अनुभाग NTCP2 के समान ब्लॉक-आधारित प्रारूप का उपयोग करता है.

### ब्लॉक संरचना

**सामान्य प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 1 बाइट - ब्लॉक प्रकार संख्या
- `size`: 2 बाइट - Big-endian (बाइट क्रम जिसमें सबसे महत्वपूर्ण बाइट पहले आती है) डेटा फ़ील्ड का आकार (0-65516)
- `data`: परिवर्तनीय लंबाई - ब्लॉक-विशिष्ट डेटा

**सीमाएँ:**

- अधिकतम ChaChaPoly (एन्क्रिप्शन स्कीम) फ्रेम: 65535 बाइट्स
- Poly1305 MAC (संदेश प्रमाणीकरण कोड): 16 बाइट्स
- अधिकतम कुल ब्लॉक: 65519 बाइट्स (65535 - 16)
- अधिकतम एकल ब्लॉक: 65519 बाइट्स (3-बाइट हेडर सहित)
- अधिकतम एकल ब्लॉक डेटा: 65516 बाइट्स

### ब्लॉक प्रकार

**परिभाषित ब्लॉक प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**अज्ञात ब्लॉक हैंडलिंग:**

कार्यान्वयन के लिए अज्ञात प्रकार संख्या वाले ब्लॉकों को अनदेखा करना और उन्हें padding (भराव) के रूप में मानना अनिवार्य है। यह आगे की संगतता सुनिश्चित करता है।

### ब्लॉक क्रम निर्धारण नियम

### NS संदेश क्रम

**आवश्यक:** - DateTime block (दिनांक-समय ब्लॉक) सबसे पहले होना अनिवार्य है

**अनुमेय:** - Garlic Clove (garlic encryption में संदेश का उप-घटक) (type 11) - विकल्प (type 5) - यदि कार्यान्वित हो - पैडिंग (type 254)

**निषिद्ध:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**वैध NS पेलोड का उदाहरण:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### NSR संदेशों का क्रम

**आवश्यक:** - कोई नहीं (पेलोड खाली हो सकता है)

**अनुमत:** - Garlic Clove (Garlic संदेश का उप-खंड) (प्रकार 11) - विकल्प (प्रकार 5) - यदि कार्यान्वित किया गया हो - पैडिंग (प्रकार 254)

**निषिद्ध:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**वैध NSR पेलोड का उदाहरण:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
या

```
(empty - ACK only)
```
### ES संदेशों का क्रम

**आवश्यक:** - कोई नहीं (payload (डेटा सामग्री) खाली हो सकता है)

**अनुमत (किसी भी क्रम में):** - Garlic Clove (garlic संदेश का 'clove' घटक) (प्रकार 11) - NextKey (प्रकार 7) - ACK (प्रकार 8) - ACK Request (प्रकार 9) - Termination (प्रकार 4) - यदि कार्यान्वित हो - MessageNumbers (प्रकार 6) - यदि कार्यान्वित हो - Options (प्रकार 5) - यदि कार्यान्वित हो - Padding (प्रकार 254)

**विशेष नियम:** - Termination (समाप्ति) का ब्लॉक अंतिम ब्लॉक होना ही चाहिए (Padding (भराई) को छोड़कर) - Padding का ब्लॉक अंतिम ब्लॉक होना ही चाहिए - एक से अधिक Garlic Cloves (garlic संदेश के उप-घटक) अनुमत हैं - अधिकतम 2 NextKey (अगली कुंजी) ब्लॉक अनुमत हैं (फ़ॉरवर्ड और रिवर्स) - एक से अधिक Padding ब्लॉक अनुमत नहीं हैं

**वैध ES पेलोड के उदाहरण:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### DateTime ब्लॉक (प्रकार 0)

**उद्देश्य**: replay (दोहराए गए हमले) की रोकथाम और clock skew (घड़ियों के समय में अंतर) के सत्यापन के लिए टाइमस्टैम्प

**आकार**: 7 बाइट (3 बाइट हेडर + 4 बाइट डेटा)

**प्रारूप:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 0
- `size`: 4 (big-endian - सबसे महत्वपूर्ण बाइट पहले)
- `timestamp`: 4 बाइट - सेकंड में Unix टाइमस्टैम्प (unsigned - बिना साइन, big-endian)

**टाइमस्टैम्प प्रारूप:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**मान्यकरण नियम:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**रीप्ले रोकथाम:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**कार्यान्वयन संबंधी नोट्स:**

1. **NS संदेश**: DateTime (तिथि-समय) अनिवार्य रूप से पहला ब्लॉक होना चाहिए
2. **NSR/ES संदेश**: DateTime आम तौर पर शामिल नहीं होता
3. **रीप्ले विंडो**: 5 मिनट न्यूनतम अनुशंसित है
4. **ब्लूम फ़िल्टर**: कुशल रीप्ले पहचान के लिए अनुशंसित
5. **क्लॉक स्क्यू**: 5 मिनट पीछे, 2 मिनट आगे तक अनुमति दें

### Garlic Clove Block (I2P में garlic encryption के भीतर का 'clove' ब्लॉक) (प्रकार 11)

**उद्देश्य**: प्रेषण के लिए I2NP संदेशों को एनकैप्सुलेट करता है

**स्वरूप:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 11
- `size`: clove (garlic संदेश की इकाई) का कुल आकार (परिवर्तनीय)
- `Delivery Instructions`: जैसा कि I2NP विशिष्टता में निर्दिष्ट है
- `type`: I2NP संदेश प्रकार (1 बाइट)
- `Message_ID`: I2NP संदेश ID (4 बाइट)
- `Expiration`: सेकंड में Unix टाइमस्टैम्प (4 बाइट)
- `I2NP Message body`: परिवर्तनीय लंबाई वाला संदेश डेटा

**डिलीवरी निर्देश प्रारूप:**

**स्थानीय वितरण** (1 बाइट):

```
+----+
|0x00|
+----+
```
**डेस्टिनेशन डिलीवरी** (33 बाइट्स):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router डिलीवरी** (33 बाइट्स):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel डिलीवरी** (37 बाइट्स):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**I2NP संदेश हेडर** (कुल 9 बाइट):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: I2NP (I2P का नेटवर्क प्रोटोकॉल) संदेश प्रकार (Database Store, Database Lookup, Data, आदि)
- `msg_id`: 4-बाइट संदेश पहचानकर्ता
- `expiration`: 4-बाइट Unix टाइमस्टैम्प (सेकंड)

**ElGamal Clove Format से महत्वपूर्ण अंतर:**

1. **कोई प्रमाणपत्र नहीं**: प्रमाणपत्र फ़ील्ड छोड़ा गया (ElGamal में अप्रयुक्त)
2. **कोई Clove ID नहीं**: Clove ID (garlic encryption में प्रयुक्त उप-संदेश की पहचान) छोड़ा गया (हमेशा 0 होता था)
3. **कोई Clove Expiration नहीं**: इसके बजाय I2NP संदेश की समाप्ति का उपयोग करता है
4. **संक्षिप्त हेडर**: 9-बाइट I2NP हेडर बनाम बड़ा ElGamal फ़ॉर्मैट
5. **हर Clove एक अलग ब्लॉक है**: कोई CloveSet (Clove का समूह) संरचना नहीं

**एकाधिक Cloves (कलियाँ):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Cloves (garlic संदेश के घटक) में आम I2NP संदेश प्रकार:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Clove (garlic संदेश का उपघटक) का प्रसंस्करण:**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### NextKey Block (अगली कुंजी ब्लॉक) (प्रकार 7)

**उद्देश्य**: DH ratchet (क्रमिक कुंजी अद्यतन तंत्र) कुंजी आदान-प्रदान

**प्रारूप (कुंजी मौजूद - 38 बाइट):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**प्रारूप (केवल कुंजी आईडी - 6 बाइट्स):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 7
- `size`: 3 (केवल ID) या 35 (कुंजी सहित)
- `flag`: 1 बाइट - फ़्लैग बिट्स
- `key ID`: 2 बाइट्स - Big-endian (उच्चतम-क्रम बाइट पहले) कुंजी पहचानकर्ता (0-32767)
- `Public Key`: 32 बाइट्स - X25519 सार्वजनिक कुंजी (little-endian; निम्नतम-क्रम बाइट पहले), यदि फ़्लैग बिट 0 = 1

**फ्लैग बिट्स:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**फ़्लैग उदाहरण:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**कुंजी ID के नियम:**

- ID क्रमिक होते हैं: 0, 1, 2, ..., 32767
- ID केवल तभी बढ़ता है जब नई कुंजी उत्पन्न की जाती है
- अगले ratchet (कुंजी आगे बढ़ाने की प्रक्रिया) तक कई संदेशों के लिए वही ID उपयोग की जाती है
- अधिकतम ID 32767 है (इसके बाद नया सत्र शुरू करना आवश्यक है)

**उपयोग के उदाहरण:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**प्रसंस्करण तर्क:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**एकाधिक NextKey Blocks (अगली कुंजी के ब्लॉक्स):**

जब दोनों दिशाओं में ratcheting (कुंजी-परिवर्तन प्रक्रिया) एक साथ हो रही हो, तब एक ही ES (एक संदेश प्रकार) संदेश में अधिकतम 2 NextKey blocks (अगली कुंजी वाले ब्लॉक) हो सकते हैं:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### ACK ब्लॉक (प्रकार 8)

**उद्देश्य**: प्राप्त संदेशों की पुष्टि in-band (उसी चैनल में) करना

**प्रारूप (एकल ACK - 7 बाइट्स):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**प्रारूप (कई ACKs (पुष्टिकरण)):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 8
- `size`: 4 * ACKs (स्वीकृतियाँ) की संख्या (न्यूनतम 4)
- प्रत्येक ACK के लिए:
  - `tagsetid`: 2 बाइट - Big-endian (बिग-एंडियन बाइट क्रम) टैग सेट ID (0-65535)
  - `N`: 2 बाइट - Big-endian संदेश संख्या (0-65535)

**टैग सेट ID का निर्धारण:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**एकल ACK (स्वीकृति संकेत) उदाहरण:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**कई ACKs का उदाहरण:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**प्रसंस्करण:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**ACKs (स्वीकृति संकेत) कब भेजें:**

1. **स्पष्ट ACK अनुरोध**: ACK (पुष्टि) अनुरोध ब्लॉक का हमेशा उत्तर दें
2. **LeaseSet वितरण**: जब प्रेषक संदेश में LeaseSet शामिल करे
3. **सत्र स्थापना**: NS/NSR का ACK कर सकता है (हालाँकि प्रोटोकॉल ES के माध्यम से निहित ACK को प्राथमिकता देता है)
4. **Ratchet (क्रिप्टोग्राफिक रैचेट तंत्र) पुष्टि**: NextKey (अगली कुंजी) की प्राप्ति का ACK कर सकता है
5. **एप्लिकेशन लेयर**: जैसा उच्च-स्तरीय प्रोटोकॉल द्वारा आवश्यक हो (उदा., Streaming)

**ACK (पुष्टिकरण) टाइमिंग:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### ACK अनुरोध ब्लॉक (प्रकार 9)

**उद्देश्य**: वर्तमान संदेश के लिए in-band (उसी संचार चैनल में) प्राप्ति-पुष्टिकरण का अनुरोध

**प्रारूप:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 9
- `size`: 1
- `flg`: 1 बाइट - Flags (संकेतक) (सभी बिट्स वर्तमान में अप्रयुक्त हैं, 0 पर सेट)

**उपयोग:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**प्राप्तकर्ता की प्रतिक्रिया:**

जब ACK Request (स्वीकृति अनुरोध) प्राप्त होता है:

1. **तुरंत डेटा के साथ**: तुरंत प्रतिक्रिया में ACK (पुष्टिकरण) ब्लॉक शामिल करें
2. **तुरंत डेटा के बिना**: टाइमर शुरू करें (उदा., 100ms) और यदि टाइमर समाप्त हो जाए तो ACK के साथ खाली ES भेजें
3. **टैग सेट ID**: वर्तमान इनबाउंड टैग सेट ID का उपयोग करें
4. **संदेश संख्या**: प्राप्त सत्र टैग से संबद्ध संदेश संख्या का उपयोग करें

**प्रसंस्करण:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**ACK Request (पुष्टिकरण अनुरोध) का उपयोग कब करें:**

1. **महत्वपूर्ण संदेश**: जिनकी पुष्टि अनिवार्य है
2. **LeaseSet प्रेषण**: जब एक LeaseSet को बंडल किया जा रहा हो
3. **Session Ratchet (सत्र रैचेट—कुंजी-क्रम अद्यतन तंत्र)**: NextKey block भेजने के बाद (अगली कुंजी वाला ब्लॉक)
4. **प्रेषण समाप्ति**: जब प्रेषक के पास भेजने के लिए और डेटा न हो, पर पुष्टि चाहिए

**कब उपयोग नहीं करना चाहिए:**

1. **Streaming Protocol (स्ट्रीमिंग प्रोटोकॉल)**: स्ट्रीमिंग लेयर ACKs (प्राप्ति-पुष्टि संदेश) को संभालती है
2. **उच्च-आवृत्ति संदेश**: हर संदेश पर ACK Request (प्राप्ति-पुष्टि का अनुरोध) से बचें (overhead)
3. **गैर-महत्वपूर्ण Datagrams (स्वतंत्र पैकेट)**: आमतौर पर कच्चे datagrams को ACKs की आवश्यकता नहीं होती

### समापन ब्लॉक (प्रकार 4)

**स्थिति**: लागू नहीं किया गया

**उद्देश्य**: सेशन को सुगमतापूर्वक समाप्त करना

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 4
- `size`: 1 या अधिक बाइट्स
- `rsn`: 1 बाइट - कारण कोड
- `addl data`: वैकल्पिक अतिरिक्त डेटा (प्रारूप कारण पर निर्भर करता है)

**कारण कोड:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**उपयोग (जब कार्यान्वित किया जाएगा):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**नियम:**

- Padding (डेटा भराई) को छोड़कर यह अवश्य अंतिम ब्लॉक होना चाहिए
- यदि Termination (समापन) मौजूद हो, तो Padding अवश्य उसके बाद आना चाहिए
- NS या NSR संदेशों में अनुमति नहीं है
- केवल ES संदेशों में अनुमति है

### विकल्प ब्लॉक (प्रकार 5)

**स्थिति**: लागू नहीं किया गया

**उद्देश्य**: सत्र पैरामीटर पर सहमति बनाना

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 5
- `size`: 21 या अधिक बाइट
- `ver`: 1 बाइट - प्रोटोकॉल संस्करण (0 होना चाहिए)
- `flg`: 1 बाइट - फ्लैग्स (सभी बिट्स वर्तमान में अनुपयोगी)
- `STL`: 1 बाइट - सेशन टैग लंबाई (8 होना चाहिए)
- `STimeout`: 2 बाइट - सेशन आइडल टाइमआउट सेकंड में (बिग-एंडियन)
- `SOTW`: 2 बाइट - प्रेषक आउटबाउंड टैग विंडो (बिग-एंडियन)
- `RITW`: 2 बाइट - रिसीवर इनबाउंड टैग विंडो (बिग-एंडियन)
- `tmin`, `tmax`, `rmin`, `rmax`: प्रत्येक 1 बाइट - पैडिंग पैरामीटर (4.4 फिक्स्ड-पॉइंट)
- `tdmy`: 2 बाइट - भेजने के लिए तैयार अधिकतम डमी ट्रैफिक (बाइट/सेकंड, बिग-एंडियन)
- `rdmy`: 2 बाइट - अनुरोधित डमी ट्रैफिक (बाइट/सेकंड, बिग-एंडियन)
- `tdelay`: 2 बाइट - सम्मिलित करने के लिए तैयार अधिकतम इंट्रा-मैसेज देरी (msec, बिग-एंडियन)
- `rdelay`: 2 बाइट - अनुरोधित इंट्रा-मैसेज देरी (msec, बिग-एंडियन)
- `more_options`: परिवर्तनीय - भविष्य के एक्सटेंशन

**पैडिंग पैरामीटर (4.4 स्थिर-बिंदु):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**टैग विंडो नेगोशिएशन:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**डिफ़ॉल्ट मान (जब विकल्पों का नेगोशिएशन नहीं हुआ हो):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### MessageNumbers ब्लॉक (प्रकार 6)

**स्थिति**: लागू नहीं किया गया

**उद्देश्य**: पिछले टैग सेट में भेजे गए अंतिम संदेश को इंगित करना (अंतर का पता लगाने में सक्षम बनाता है)

**प्रारूप:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 6
- `size`: 2
- `PN`: 2 बाइट - पिछले टैग सेट का अंतिम संदेश क्रमांक (big-endian (बाइट क्रम जिसमें सबसे महत्वपूर्ण बाइट पहले आती है), 0-65535)

**PN (Previous Number) की परिभाषा:**

PN पिछले टैग सेट में भेजे गए अंतिम टैग का सूचकांक है।

**उपयोग (कार्यान्वित होने पर):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**प्राप्तकर्ता के लाभ:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**नियम:**

- tag set (टैग का समूह) 0 में कदापि नहीं भेजा जाना चाहिए (कोई पूर्व tag set नहीं)
- केवल ES messages (ES प्रकार के संदेश) में भेजा जाता है
- नए tag set के प्रथम संदेश(संदेशों) में ही भेजा जाता है
- PN value (PN मान) प्रेषक के दृष्टिकोण से होती है (आखिरी टैग जो प्रेषक ने भेजा)

**Signal से संबंध:**

Signal Double Ratchet (Signal प्रोटोकॉल का डबल रैचेट एल्गोरिद्म) में, PN संदेश हेडर में होता है। ECIES (एलिप्टिक कर्व-आधारित समेकित एन्क्रिप्शन स्कीम) में, यह एन्क्रिप्टेड पेलोड में होता है और वैकल्पिक है।

### पैडिंग ब्लॉक (टाइप 254)

**उद्देश्य**: ट्रैफिक विश्लेषण के प्रति प्रतिरोध और संदेश आकार का छुपाव

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**फ़ील्ड्स:**

- `blk`: 254
- `size`: 0-65516 बाइट्स (big-endian, सबसे महत्त्वपूर्ण बाइट पहले)
- `padding`: यादृच्छिक या शून्य डेटा

**नियम:**

- यह संदेश में अंतिम ब्लॉक होना चाहिए
- एक से अधिक Padding (भराई) ब्लॉक की अनुमति नहीं है
- शून्य लंबाई हो सकती है (केवल 3-बाइट हेडर)
- Padding डेटा शून्य या यादृच्छिक बाइट्स हो सकता है

**डिफ़ॉल्ट पैडिंग:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**ट्रैफ़िक विश्लेषण प्रतिरोध रणनीतियाँ:**

**रणनीति 1: यादृच्छिक आकार (डिफ़ॉल्ट)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**रणनीति 2: गुणज तक राउंड करें**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**रणनीति 3: स्थिर संदेश आकार**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**रणनीति 4: समझौता-आधारित पैडिंग (विकल्प ब्लॉक)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**सिर्फ Padding (भराव) वाले संदेश:**

संदेश पूरी तरह पैडिंग से बने हो सकते हैं (कोई एप्लिकेशन डेटा नहीं):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**कार्यान्वयन संबंधी टिप्पणियाँ:**

1. **सभी-शून्य पैडिंग**: स्वीकार्य (ChaCha20 द्वारा एन्क्रिप्ट किया जाएगा)
2. **यादृच्छिक पैडिंग**: एन्क्रिप्शन के बाद कोई अतिरिक्त सुरक्षा प्रदान नहीं करती, लेकिन अधिक एंट्रॉपी (यादृच्छिकता का परिमाण) का उपयोग करती है
3. **प्रदर्शन**: यादृच्छिक पैडिंग उत्पन्न करना संसाधन-गहन हो सकता है; शून्य का उपयोग करने पर विचार करें
4. **मेमोरी**: बड़े पैडिंग ब्लॉक बैंडविड्थ की खपत करते हैं; अधिकतम आकार पर सावधानी बरतें

---

## कार्यान्वयन मार्गदर्शिका

### पूर्वापेक्षाएँ

**क्रिप्टोग्राफिक लाइब्रेरीज़:**

- **X25519**: libsodium, NaCl, या Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+, या Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle, या भाषा का अंतर्निर्मित समर्थन
- **Elligator2**: सीमित लाइब्रेरी समर्थन; कस्टम कार्यान्वयन की आवश्यकता हो सकती है

**Elligator2 का कार्यान्वयन:**

Elligator2 (एक क्रिप्टोग्राफ़िक तकनीक) का व्यापक रूप से लागू नहीं किया गया है। विकल्प:

1. **OBFS4**: Tor के obfs4 pluggable transport (सेंसरशिप-परिहार के लिए मॉड्यूलर परिवहन तंत्र) में Elligator2 का कार्यान्वयन शामिल है
2. **कस्टम कार्यान्वयन**: [Elligator2 शोध-पत्र](https://elligator.cr.yp.to/elligator-20130828.pdf) पर आधारित
3. **kleshni/Elligator**: GitHub पर संदर्भ कार्यान्वयन

**Java I2P नोट:** Java I2P net.i2p.crypto.eddsa लाइब्रेरी का उपयोग करता है, जिसमें कस्टम Elligator2 (एक क्रिप्टोग्राफिक मैपिंग तकनीक) जोड़ शामिल हैं।

### अनुशंसित कार्यान्वयन क्रम

**चरण 1: कोर क्रिप्टोग्राफ़ी** 1. X25519 DH (Diffie‑Hellman — डिफ़ी‑हेलमैन) कुंजी उत्पन्न करना और विनिमय 2. ChaCha20‑Poly1305 AEAD (Authenticated Encryption with Associated Data — संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) एन्क्रिप्शन/डीक्रिप्शन 3. SHA‑256 हैशिंग और MixHash (हैश मिश्रण प्रक्रिया) 4. HKDF (HMAC‑based Key Derivation Function — HMAC‑आधारित कुंजी व्युत्पत्ति फ़ंक्शन) कुंजी व्युत्पत्ति 5. Elligator2 एन्कोडिंग/डीकोडिंग (प्रारम्भ में टेस्ट वेक्टर का उपयोग किया जा सकता है)

**चरण 2: संदेश प्रारूप** 1. NS संदेश (unbound) - सबसे सरल प्रारूप 2. NS संदेश (bound) - स्थिर कुंजी जोड़ता है 3. NSR संदेश 4. ES संदेश 5. ब्लॉक पार्सिंग और उत्पादन

**चरण 3: सत्र प्रबंधन** 1. सत्र निर्माण और भंडारण 2. टैग सेट प्रबंधन (प्रेषक और प्राप्तकर्ता) 3. सत्र टैग ratchet (क्रमिक कुंजी-अद्यतन तंत्र) 4. सममित कुंजी ratchet 5. टैग लुकअप और विंडो प्रबंधन

**चरण 4: DH Ratcheting (Diffie-Hellman आधारित रैचेटिंग तकनीक)** 1. NextKey block का प्रसंस्करण 2. DH ratchet KDF (Key Derivation Function, कुंजी व्युत्पन्न फ़ंक्शन) 3. रैचेट के बाद Tag set (टैगों का समूह) का निर्माण 4. एकाधिक Tag set का प्रबंधन

**चरण 5: प्रोटोकॉल लॉजिक** 1. NS/NSR/ES स्टेट मशीन 2. रीप्ले रोकथाम (DateTime, Bloom filter) 3. पुनः-प्रेषण लॉजिक (एकाधिक NS/NSR) 4. ACK प्रबंधन

**चरण 6: एकीकरण** 1. I2NP Garlic Clove (Garlic संदेश की उप-इकाई) प्रसंस्करण 2. LeaseSet समूहीकरण 3. स्ट्रीमिंग प्रोटोकॉल एकीकरण 4. डेटाग्राम प्रोटोकॉल एकीकरण

### प्रेषक कार्यान्वयन

**आउटबाउंड सत्र जीवनचक्र:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### रिसीवर का कार्यान्वयन

**आगत सत्र जीवनचक्र:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### संदेश वर्गीकरण

**संदेश प्रकारों का भेद:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### सत्र प्रबंधन की सर्वोत्तम प्रथाएँ

**सत्र संग्रहण:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**मेमोरी प्रबंधन:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### परीक्षण रणनीतियाँ

**इकाई परीक्षण:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**एकीकरण परीक्षण:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**परीक्षण वेक्टर:**

विनिर्देश के अनुसार परीक्षण वेक्टर कार्यान्वित करें:

1. **Noise IK Handshake**: Noise के मानक परीक्षण वेक्टरों का उपयोग करें
2. **HKDF**: RFC 5869 के परीक्षण वेक्टरों का उपयोग करें
3. **ChaCha20-Poly1305**: RFC 7539 के परीक्षण वेक्टरों का उपयोग करें
4. **Elligator2**: Elligator2 शोध-पत्र या OBFS4 से परीक्षण वेक्टरों का उपयोग करें

**अंतरसंचालनीयता परीक्षण:**

1. **Java I2P**: Java I2P संदर्भ कार्यान्वयन के विरुद्ध परीक्षण करें
2. **i2pd**: C++ i2pd कार्यान्वयन के विरुद्ध परीक्षण करें
3. **पैकेट कैप्चर**: संदेश प्रारूपों को सत्यापित करने के लिए Wireshark dissector (पैकेट विश्लेषक मॉड्यूल, यदि उपलब्ध हो) का उपयोग करें
4. **अंतर-कार्यान्वयन**: ऐसा टेस्ट हार्नेस बनाएँ जो कार्यान्वयनों के बीच भेज/प्राप्त कर सके

### प्रदर्शन संबंधी विचार

**कुंजी निर्माण:**

Elligator2 (एक क्रिप्टोग्राफिक मैपिंग तकनीक) के लिए कुंजी उत्पन्न करना गणनात्मक रूप से महंगा है (50% अस्वीकृति दर):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**टैग लुकअप:**

O(1) टैग खोज के लिए हैश तालिकाएँ उपयोग करें:

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**मेमोरी अनुकूलन:**

सममित कुंजी उत्पन्न करने को स्थगित करें:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**बैच प्रसंस्करण:**

कई संदेशों को बैच में संसाधित करें:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## सुरक्षा संबंधी विचार

### धमकी मॉडल

**विरोधी की क्षमताएँ:**

1. **निष्क्रिय निरीक्षक**: समस्त नेटवर्क ट्रैफ़िक की निगरानी कर सकता है
2. **सक्रिय हमलावर**: संदेशों को इंजेक्ट, संशोधित, ड्रॉप, और रिप्ले (दोहराकर भेजना) कर सकता है
3. **समझौता-ग्रस्त नोड**: किसी router या गंतव्य को समझौता-ग्रस्त बना सकता है
4. **ट्रैफ़िक विश्लेषण**: ट्रैफ़िक पैटर्न का सांख्यिकीय विश्लेषण कर सकता है

**सुरक्षा लक्ष्य:**

1. **गोपनीयता**: संदेश की सामग्री पर्यवेक्षक से छिपी रहती है
2. **प्रमाणीकरण**: प्रेषक की पहचान सत्यापित (बाउंड सत्रों के लिए)
3. **Forward Secrecy** (आगे की गोपनीयता): कुंजियों से समझौता हो जाने पर भी पुराने संदेश गोपनीय बने रहते हैं
4. **रीप्ले-रोकथाम**: पुराने संदेशों का रीप्ले संभव नहीं
5. **ट्रैफ़िक अस्पष्टकरण**: हैंडशेक यादृच्छिक डेटा से अप्रभेद्य

### क्रिप्टोग्राफिक धारणाएँ

**कठिनता मान्यताएँ:**

1. **X25519 CDH**: Curve25519 पर Computational Diffie-Hellman समस्या कठिन है
2. **ChaCha20 PRF**: ChaCha20 एक छद्म-यादृच्छिक फ़ंक्शन (pseudorandom function) है
3. **Poly1305 MAC**: Poly1305 चुने हुए संदेश आक्रमण (chosen message attack) के तहत जालसाजी-प्रतिरोधी है
4. **SHA-256 CR**: SHA-256 टकराव-प्रतिरोधी है
5. **HKDF Security**: HKDF समान रूप से वितरित कुंजियों को निकालता और विस्तारित करता है

**सुरक्षा स्तर:**

- **X25519**: ~128-बिट सुरक्षा (वक्र का क्रम 2^252)
- **ChaCha20**: 256-बिट कुंजियाँ, 256-बिट सुरक्षा
- **Poly1305**: 128-बिट सुरक्षा (टकराव की संभावना)
- **SHA-256**: 128-बिट टकराव-प्रतिरोध, 256-बिट पूर्व-छवि प्रतिरोध

### कुंजी प्रबंधन

**कुंजी निर्माण:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**कुंजी भंडारण:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**कुंजी परिवर्तन:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### हमलों के शमन उपाय

### रीप्ले हमले के शमन उपाय

**DateTime वैधता जांच:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**NS संदेशों के लिए Bloom Filter (प्रायिकता-आधारित फ़िल्टर):**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Session Tag (सत्र टैग) का एक-बार उपयोग:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Key Compromise Impersonation (KCI) (कुंजी-समझौते के कारण प्रतिरूपण) शमन उपाय

**समस्या**: NS संदेश प्रमाणीकरण KCI (कुंजी से समझौता होने पर प्रतिरूपण) के प्रति असुरक्षित है (प्रमाणीकरण स्तर 1)

**शमन**:

1. यथाशीघ्र NSR (प्रमाणीकरण स्तर 2) में संक्रमण करें
2. सुरक्षा-आवश्यक कार्यों के लिए NS payload (NS संदेश का डेटा भाग) पर भरोसा न करें
3. अपरिवर्तनीय कार्रवाइयाँ करने से पहले NSR की पुष्टि की प्रतीक्षा करें

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Denial-of-Service (सेवा-अस्वीकरण) के शमन उपाय

**NS फ्लड सुरक्षा:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**टैग संग्रहण सीमाएँ:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**अनुकूली संसाधन प्रबंधन:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### ट्रैफ़िक विश्लेषण प्रतिरोध

**Elligator2 एन्कोडिंग:**

हैंडशेक संदेशों को यादृच्छिक डेटा से अप्रभेद्य बनाता है:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**पैडिंग रणनीतियाँ:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**टाइमिंग हमले:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### कार्यान्वयन में सामान्य गलतियाँ

**सामान्य गलतियाँ:**

1. **Nonce का पुन: उपयोग**: (key, nonce) युग्मों का कभी भी पुन: उपयोग न करें
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# सही: हर संदेश के लिए अलग nonce (एक बार प्रयुक्त यादृच्छिक मान)    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# गलत: अस्थायी कुंजी का पुन: उपयोग    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # गलत

# अच्छा: प्रत्येक संदेश के लिए नई कुंजी    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# खराब: गैर-क्रिप्टोग्राफ़िक RNG (यादृच्छिक संख्या जनक)    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # असुरक्षित

# अच्छा: क्रिप्टोग्राफ़िक रूप से सुरक्षित RNG (रैंडम नंबर जनरेटर)    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# खराब: शीघ्र-निकास तुलना    if computed_mac == received_mac:  # टाइमिंग लीक

       pass
   
# सही: स्थिर-समय तुलना    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# खराब: सत्यापन से पहले डिक्रिप्ट करना    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # बहुत देर हो चुकी    if not mac_ok:

       return error
   
# सही: AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) डिक्रिप्ट करने से पहले सत्यापन करता है    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# गलत: सरल हटाना    del private_key  # अब भी मेमोरी में

# उचित: हटाने से पहले ओवरराइट करें    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# सुरक्षा-महत्त्वपूर्ण परीक्षण मामले

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# केवल ECIES (अण्डाकार वक्र एकीकृत एन्क्रिप्शन योजना) (नए परिनियोजन के लिए अनुशंसित)

i2cp.leaseSetEncType=4

# द्वि-कुंजी (संगतता के लिए ECIES + ElGamal)

i2cp.leaseSetEncType=4,0

# केवल ElGamal (पुराना, अनुशंसित नहीं)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# मानक LS2 (सबसे सामान्य)

i2cp.leaseSetType=3

# कूटबद्ध LS2 (blinded destinations, अर्थात पहचान-अस्पष्ट किए गए destinations)

i2cp.leaseSetType=5

# Meta LS2 (कई गंतव्य)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# ECIES (Elliptic Curve Integrated Encryption Scheme, दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना) के लिए स्थिर कुंजी (वैकल्पिक, यदि निर्दिष्ट न हो तो स्वतः उत्पन्न हो जाती है)

# 32-बाइट की X25519 सार्वजनिक कुंजी, Base64-कूटबद्ध

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# LeaseSet के लिए हस्ताक्षर प्रकार

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# Router-से-router ECIES (दीर्घवृत्तीय वक्र एकीकृत एन्क्रिप्शन योजना)

i2p.router.useECIES=true

```

**Build Properties:**

```java
// I2CP क्लाइंट्स (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[सीमाएँ]

# ECIES (एलिप्टिक कर्व इंटीग्रेटेड एन्क्रिप्शन स्कीम) सत्रों की मेमोरी सीमा

ecies.memory = 128M

[ecies (एलिप्टिक कर्व एकीकृत एन्क्रिप्शन योजना)]

# ECIES (एलिप्टिक कर्व इंटीग्रेटेड एन्क्रिप्शन स्कीम) सक्षम करें

enabled = true

# केवल ECIES (Elliptic Curve Integrated Encryption Scheme) या द्वि-कुंजी

compatibility = true  # true = द्वि-कुंजी, false = केवल ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# केवल ECIES (दीर्घवृत्तीय वक्र समेकित एन्क्रिप्शन योजना)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# ElGamal (एक सार्वजनिक‑कुंजी कूटलेखन योजना) को बनाए रखते हुए ECIES (Elliptic Curve Integrated Encryption Scheme — दीर्घवृत्तीय वक्र समेकित कूटलेखन योजना) जोड़ें

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# कनेक्शन प्रकार जाँचें

i2prouter.exe status

# या

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# ElGamal (पब्लिक-की क्रिप्टोसिस्टम) को हटाएँ

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# I2P router या एप्लिकेशन को पुनः प्रारंभ करें

systemctl restart i2p

# या

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# यदि समस्याएँ हों तो केवल ElGamal (एक सार्वजनिक‑कुंजी क्रिप्टोसिस्टम) पर लौटें

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# इनबाउंड सत्रों की अधिकतम संख्या

i2p.router.maxInboundSessions=1000

# आउटबाउंड सत्रों की अधिकतम संख्या

i2p.router.maxOutboundSessions=1000

# सत्र समय-सीमा (सेकंड)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# टैग भंडारण सीमा (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Look-ahead window (आगे देखने की विंडो)

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# ratchet (क्रिप्टोग्राफ़िक कुंजी-अद्यतन तंत्र) से पहले के संदेश

i2p.ecies.ratchetThreshold=4096

# ratchet (कुंजी अद्यतन तंत्र) से पहले का समय (सेकंड)

i2p.ecies.ratchetTimeout=600  # 10 मिनट

```

### Monitoring and Debugging

**Logging:**

```properties
# ECIES (इलिप्टिक कर्व इंटीग्रेटेड एन्क्रिप्शन स्कीम) डीबग लॉगिंग सक्षम करें

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# उदाहरण

print("NS (बंधित, 1KB पेलोड):", calculate_ns_size(1024, bound=True), "बाइट्स")

# आउटपुट: 1120 बाइट्स

print("NSR (1KB पेलोड):", calculate_nsr_size(1024), "बाइट्स")

# आउटपुट: 1096 बाइट्स

print("ES (1KB पेलोड):", calculate_es_size(1024), "बाइट्स")

# आउटपुट: 1048 बाइट्स

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---