---
title: "NTCP2 ट्रांसपोर्ट"
description: "router-से-router लिंक के लिए Noise (क्रिप्टोग्राफ़िक प्रोटोकॉल) आधारित TCP ट्रांसपोर्ट"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## अवलोकन

NTCP2 पुराने NTCP ट्रांसपोर्ट को एक Noise‑based handshake (कनेक्शन स्थापित करने की आरंभिक कुंजी-विनिमय प्रक्रिया) से बदलता है, जो traffic fingerprinting (ट्रैफ़िक के पैटर्न से पहचान निकालने की तकनीक) का प्रतिरोध करता है, length fields (डेटा की लंबाई बताने वाले फ़ील्ड) को एन्क्रिप्ट करता है, और आधुनिक cipher suites (एन्क्रिप्शन एल्गोरिद्म के संयोजन) का समर्थन करता है। Routers I2P नेटवर्क में दो अनिवार्य ट्रांसपोर्ट प्रोटोकॉल के रूप में NTCP2 को SSU2 के साथ चला सकते हैं। NTCP (version 1) को 0.9.40 (May 2019) में अप्रचलित घोषित किया गया और 0.9.50 (May 2021) में पूरी तरह हटा दिया गया।

## Noise Protocol Framework (क्रिप्टोग्राफिक हैंडशेक के लिए एक ढांचा)

NTCP2, I2P-विशिष्ट विस्तारों के साथ Noise Protocol Framework (क्रिप्टोग्राफ़िक प्रोटोकॉल फ़्रेमवर्क) [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) का उपयोग करता है:

- **पैटर्न**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **विस्तारित पहचानकर्ता**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (KDF (Key Derivation Function; कुंजी व्युत्पन्नीकरण फ़ंक्शन) के प्रारंभिककरण हेतु)
- **DH फ़ंक्शन (Diffie-Hellman)**: X25519 (RFC 7748) - 32-बाइट कुंजियाँ, लिटिल-एंडियन (कम-महत्वपूर्ण-बाइट पहले) एन्कोडिंग
- **साइफ़र**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12-बाइट nonce (एक बार प्रयुक्त मान): पहले 4 बाइट शून्य, आख़िरी 8 बाइट काउंटर (little-endian)
  - अधिकतम nonce मान: 2^64 - 2 (कनेक्शन को 2^64 - 1 तक पहुँचने से पहले समाप्त हो जाना चाहिए)
- **हैश फ़ंक्शन**: SHA-256 (32-बाइट आउटपुट)
- **MAC (संदेश प्रमाणीकरण कोड)**: Poly1305 (16-बाइट प्रमाणीकरण टैग)

### I2P-विशिष्ट एक्सटेंशन्स


## हैंडशेक प्रवाह

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### तीन-संदेशों वाला हैंडशेक

1. **SessionRequest** (सत्र अनुरोध संदेश) - Alice की अस्पष्टीकृत अस्थायी कुंजी, विकल्प, पैडिंग संकेत
2. **SessionCreated** (सत्र-निर्मित संदेश) - Bob की अस्पष्टीकृत अस्थायी कुंजी, कूटबद्ध विकल्प, पैडिंग
3. **SessionConfirmed** (सत्र-पुष्ट संदेश) - Alice की कूटबद्ध स्थिर कुंजी और RouterInfo (router की जानकारी) (दो AEAD फ़्रेम)

### Noise संदेश पैटर्न

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**प्रमाणीकरण स्तर:** - 0: कोई प्रमाणीकरण नहीं (कोई भी पक्ष इसे भेज सकता था) - 2: प्रेषक प्रमाणीकरण, key-compromise impersonation (कुंजी-समझौता प्रतिरूपण, KCI) के प्रति प्रतिरोधी

**गोपनीयता स्तर:** - 1: अस्थायी प्राप्तकर्ता (forward secrecy (भविष्य-गोपनीयता), प्राप्तकर्ता का प्रमाणीकरण नहीं) - 2: ज्ञात प्राप्तकर्ता, केवल प्रेषक के समझौते की स्थिति में forward secrecy - 5: मजबूत forward secrecy (ephemeral-ephemeral + ephemeral-static DH)

## संदेश विनिर्देश

### कुंजी संकेतन

- `RH_A` = ऐलिस के लिए Router हैश (32 बाइट, SHA-256)
- `RH_B` = बॉब के लिए Router हैश (32 बाइट, SHA-256)
- `||` = संयोजन ऑपरेटर
- `byte(n)` = मान n वाला एकल बाइट
- सभी बहु-बाइट पूर्णांक, जब तक अन्यथा निर्दिष्ट न हो, **big-endian** (उच्च-क्रम बाइट पहले) होते हैं
- X25519 कुंजियाँ **little-endian** (निम्न-क्रम बाइट पहले) होती हैं (32 बाइट)

### प्रमाणीकृत एन्क्रिप्शन (ChaCha20-Poly1305)

**एन्क्रिप्शन फ़ंक्शन:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**पैरामीटर्स:** - `key`: KDF (कुंजी व्युत्पन्न करने वाला फ़ंक्शन) से प्राप्त 32-बाइट साइफ़र कुंजी - `nonce`: 12 बाइट (4 शून्य बाइट + 8-बाइट काउंटर, लिटिल-एंडियन) - `associatedData`: हैंडशेक चरण में 32-बाइट हैश; डेटा चरण में शून्य-लंबाई - `plaintext`: एन्क्रिप्ट करने हेतु डेटा (0+ बाइट)

**आउटपुट:** - Ciphertext (कूट-पाठ): plaintext (स्पष्ट पाठ) जितनी ही लंबाई - MAC (Message Authentication Code, संदेश प्रमाणीकरण कोड): 16 बाइट्स (Poly1305 authentication tag, प्रमाणीकरण टैग)

**Nonce (एक-बार-प्रयोग संख्या) प्रबंधन:** - काउंटर प्रत्येक cipher instance के लिए 0 से शुरू होता है - उस दिशा में प्रत्येक AEAD (Authenticated Encryption with Associated Data) ऑपरेशन के लिए बढ़ाया जाता है - डेटा चरण में Alice→Bob और Bob→Alice के लिए अलग-अलग काउंटर - काउंटर के 2^64 - 1 तक पहुँचने से पहले कनेक्शन समाप्त करना होगा

## संदेश 1: SessionRequest (सत्र अनुरोध)

एलिस बॉब से कनेक्शन शुरू करती है।

**Noise प्रचालन (क्रिप्टोग्राफ़िक हैंडशेक प्रोटोकॉल)**: `e, es` (अस्थायी कुंजी निर्माण और आदान-प्रदान)

### रॉ फ़ॉर्मेट

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**आकार सीमाएँ:** - न्यूनतम: 80 बाइट (32 AES + 48 AEAD) - अधिकतम: कुल 65535 बाइट - **विशेष मामला**: "NTCP" पतों से जुड़ते समय अधिकतम 287 बाइट (संस्करण पहचान)

### डिक्रिप्ट की गई सामग्री

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### विकल्प ब्लॉक (16 बाइट, big-endian (सबसे महत्त्वपूर्ण बाइट पहले))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**महत्वपूर्ण फ़ील्ड:** - **Network ID** (नेटवर्क पहचानकर्ता) (since 0.9.42): क्रॉस-नेटवर्क कनेक्शनों का त्वरित अस्वीकार - **m3p2len**: संदेश 3 भाग 2 का सटीक आकार (भेजते समय मेल खाना चाहिए)

### कुंजी व्युत्पत्ति फ़ंक्शन (KDF-1)

**प्रोटोकॉल प्रारंभ करें:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**MixHash (मिक्सहैश) संचालन:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**MixKey प्रचालन (es पैटर्न):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### कार्यान्वयन संबंधी टिप्पणियाँ

1. **AES अस्पष्टिकरण**: केवल DPI (Deep Packet Inspection) प्रतिरोध के लिए प्रयुक्त; Bob के router हैश और IV के साथ कोई भी व्यक्ति X को डिक्रिप्ट कर सकता है
2. **रीप्ले रोकथाम**: Bob को कम-से-कम 2*D सेकंड तक X मानों (या उनके एन्क्रिप्टेड समकक्ष) को कैश करना चाहिए (D = घड़ी का अधिकतम विचलन)
3. **टाइमस्टैम्प सत्यापन**: Bob को उन कनेक्शनों को अस्वीकार करना चाहिए जिनमें |tsA - current_time| > D हो (आम तौर पर D = 60 सेकंड)
4. **कर्व सत्यापन**: Bob को सत्यापित करना चाहिए कि X एक वैध X25519 पॉइंट है
5. **त्वरित अस्वीकृति**: डिक्रिप्शन से पहले Bob X[31] & 0x80 == 0 की जाँच कर सकता है (वैध X25519 कुंजियों में MSB (सर्वाधिक महत्वपूर्ण बिट) क्लियर होता है)
6. **त्रुटि प्रबंधन**: किसी भी विफलता पर, Bob यादृच्छिक टाइमआउट और यादृच्छिक बाइट पढ़ने के बाद TCP RST के साथ कनेक्शन बंद करता है
7. **बफ़रिंग**: दक्षता के लिए Alice को पूरा संदेश (पैडिंग सहित) एक साथ फ्लश करना चाहिए

## संदेश 2: SessionCreated

Bob, Alice को उत्तर देता है।

**Noise ऑपरेशन्स**: `e, ee` (ephemeral-ephemeral DH — दो अस्थायी कुंजियों के बीच Diffie-Hellman)

### रॉ फ़ॉर्मेट

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### डिक्रिप्ट की गई सामग्री

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### विकल्प ब्लॉक (16 बाइट्स, big-endian (सर्वाधिक महत्त्वपूर्ण बाइट पहले))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### कुंजी व्युत्पत्ति फ़ंक्शन (KDF-2)

**MixHash ऑपरेशन्स:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey ऑपरेशन (ee pattern):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**मेमोरी साफ़-सफाई:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### कार्यान्वयन संबंधी टिप्पणियाँ

1. **AES चेनिंग**: Y एन्क्रिप्शन संदेश 1 से AES-CBC (ब्लॉक-चेनिंग मोड वाला Advanced Encryption Standard) स्टेट का उपयोग करता है (रिसेट नहीं किया जाता)
2. **रीप्ले रोकथाम**: Alice को Y मानों को कम-से-कम 2*D सेकंड तक कैश करना चाहिए
3. **टाइमस्टैम्प सत्यापन**: |tsB - current_time| > D होने पर Alice को अस्वीकार करना चाहिए
4. **कर्व सत्यापन**: Alice को सत्यापित करना चाहिए कि Y एक मान्य X25519 (एलीप्टिक-कर्व की-एक्सचेंज एल्गोरिद्म) बिंदु है
5. **त्रुटि प्रबंधन**: किसी भी विफलता पर Alice TCP RST (TCP कनेक्शन रीसेट पैकेट) भेजकर कनेक्शन बंद करती है
6. **बफ़रिंग**: Bob को पूरा संदेश एक साथ flush (आउटपुट बफ़र को तुरंत भेजना) करना चाहिए

## संदेश 3: SessionConfirmed (सत्र की पुष्टि)

Alice सत्र की पुष्टि करती है और RouterInfo भेजती है।

**Noise ऑपरेशन्स**: `s, se` (स्थिर कुंजी प्रकटीकरण और स्थिर-क्षणिक Diffie-Hellman (कुंजी विनिमय))

### द्विभागीय संरचना

संदेश 3 **दो अलग-अलग AEAD (Authenticated Encryption with Associated Data—संबद्ध डेटा के साथ प्रमाणीकृत एन्क्रिप्शन) फ्रेम** से बना है:

1. **भाग 1**: Alice की कूटबद्ध स्थिर कुंजी सहित 48-बाइट का नियत फ्रेम
2. **भाग 2**: RouterInfo, विकल्प, और पैडिंग सहित चर लंबाई वाला फ्रेम

### कच्चा प्रारूप

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**आकार प्रतिबंध:** - भाग 1: ठीक 48 बाइट्स (32 सादा पाठ + 16 MAC (Message Authentication Code—संदेश प्रमाणीकरण कोड)) - भाग 2: लंबाई संदेश 1 (m3p2len फील्ड) में निर्दिष्ट - कुल अधिकतम: 65535 बाइट्स (भाग 1 अधिकतम 48, अतः भाग 2 अधिकतम 65487)

### डिक्रिप्ट की गई सामग्री

**भाग 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**भाग 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### कुंजी व्युत्पत्ति फ़ंक्शन (KDF-3)

**भाग 1 (s पैटर्न):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**भाग 2 (se पैटर्न):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**मेमोरी क्लीनअप:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### कार्यान्वयन संबंधी टिप्पणियाँ

1. **RouterInfo सत्यापन**: Bob को हस्ताक्षर, टाइमस्टैम्प, और कुंजी की सुसंगतता सत्यापित करना चाहिए
2. **कुंजी मिलान**: Bob को सत्यापित करना चाहिए कि भाग 1 में Alice की स्थिर कुंजी RouterInfo में कुंजी से मेल खाती है
3. **स्थिर कुंजी का स्थान**: NTCP या NTCP2 के RouterAddress में मिलते-जुलते "s" पैरामीटर की तलाश करें
4. **ब्लॉक क्रम**: RouterInfo सबसे पहले होना चाहिए, Options दूसरे स्थान पर (यदि उपस्थित हो), और Padding सबसे अंतिम (यदि उपस्थित हो)
5. **लंबाई नियोजन**: Alice को सुनिश्चित करना चाहिए कि संदेश 1 में m3p2len ठीक-ठीक भाग 2 की लंबाई से मेल खाए
6. **बफरिंग**: Alice को दोनों भागों को एक ही TCP send के रूप में साथ में फ्लश करना चाहिए
7. **वैकल्पिक चेनिंग**: दक्षता के लिए Alice तुरंत data phase frame (डेटा चरण का फ्रेम) जोड़ सकती है

## डेटा चरण

हैंडशेक पूरा होने के बाद, सभी संदेश परिवर्ती-लंबाई AEAD (संबद्ध डेटा के साथ प्रमाणित एन्क्रिप्शन) फ़्रेम का उपयोग करते हैं, जिनमें लंबाई फ़ील्ड को गोपित किया गया होता है।

### कुंजी व्युत्पत्ति फ़ंक्शन (डेटा चरण)

**Split Function (Noise) (विभाजन फ़ंक्शन, Noise प्रोटोकॉल):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**SipHash कुंजी व्युत्पत्ति:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### फ्रेम संरचना

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**फ़्रेम सीमाएँ:** - न्यूनतम: 18 बाइट्स (2 obfuscated length (अस्पष्ट की गई लंबाई) + 0 साधारण-पाठ + 16 MAC (Message Authentication Code, संदेश प्रमाणीकरण कोड)) - अधिकतम: 65537 बाइट्स (2 obfuscated length + 65535 फ़्रेम) - अनुशंसित: प्रति फ़्रेम कुछ KB (प्राप्तकर्ता की विलंबता को न्यूनतम रखें)

### SipHash (एक कुंजी-आधारित तेज़ हैश फ़ंक्शन) लंबाई का अस्पष्टकरण

**उद्देश्य**: DPI (Deep Packet Inspection, गहन पैकेट निरीक्षण) द्वारा फ़्रेम सीमाओं की पहचान को रोकना

**एल्गोरिदम:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**डिकोडिंग:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**नोट्स:** - प्रत्येक दिशा के लिए अलग-अलग IV (इनिशियलाइज़ेशन वेक्टर) चेन (Alice→Bob और Bob→Alice) - यदि SipHash uint64 लौटाता है, तो मास्क के रूप में सबसे कम महत्वपूर्ण 2 बाइट्स का उपयोग करें - uint64 को little-endian बाइट्स में बदलकर अगले IV के रूप में उपयोग करें

### ब्लॉक प्रारूप

प्रत्येक फ़्रेम में शून्य या अधिक ब्लॉक होते हैं:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**आकार सीमाएँ:** - अधिकतम फ़्रेम: 65535 बाइट्स (MAC सहित) - अधिकतम ब्लॉक स्थान: 65519 बाइट्स (फ़्रेम - 16-बाइट MAC) - अधिकतम एकल ब्लॉक: 65519 बाइट्स (3-बाइट हेडर + 65516 डेटा)

### ब्लॉक प्रकार

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**ब्लॉक क्रमबद्धता के नियम:** - **संदेश 3 भाग 2**: RouterInfo, Options (वैकल्पिक), Padding (वैकल्पिक) - कोई अन्य प्रकार नहीं - **डेटा चरण**: निम्न अपवादों को छोड़कर किसी भी क्रम में:   - Padding उपस्थित होने पर अंतिम ब्लॉक होना चाहिए   - Termination उपस्थित होने पर (Padding को छोड़कर) अंतिम ब्लॉक होना चाहिए - प्रति फ्रेम एक से अधिक I2NP ब्लॉकों की अनुमति है - प्रति फ्रेम एक से अधिक Padding ब्लॉकों की अनुमति नहीं है

### ब्लॉक प्रकार 0: DateTime

घड़ी विचलन का पता लगाने के लिए समय समकालिकरण।

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**कार्यान्वयन**: clock bias (घड़ी का ऑफ़सेट) का संचय रोकने हेतु निकटतम सेकंड तक राउंड करें।

### ब्लॉक प्रकार 1: विकल्प

पैडिंग और traffic shaping (नेटवर्क ट्रैफ़िक को नियंत्रित करने की तकनीक) पैरामीटर।

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**पैडिंग अनुपात** (4.4 fixed-point float (स्थिर-बिंदु फ्लोट), value/16.0): - `tmin`: प्रेषण का न्यूनतम पैडिंग अनुपात (0.0 - 15.9375) - `tmax`: प्रेषण का अधिकतम पैडिंग अनुपात (0.0 - 15.9375) - `rmin`: प्राप्ति का न्यूनतम पैडिंग अनुपात (0.0 - 15.9375) - `rmax`: प्राप्ति का अधिकतम पैडिंग अनुपात (0.0 - 15.9375)

**उदाहरण:** - 0x00 = 0% पैडिंग - 0x01 = 6.25% पैडिंग - 0x10 = 100% पैडिंग (1:1 अनुपात) - 0x80 = 800% पैडिंग (8:1 अनुपात)

**डमी ट्रैफ़िक:** - `tdmy`: भेजने की अधिकतम स्वीकृत दर (2 बाइट्स, बाइट्स/सेकंड औसत) - `rdmy`: प्राप्त करने के लिए अनुरोधित दर (2 बाइट्स, बाइट्स/सेकंड औसत)

**विलंब सम्मिलन:** - `tdelay`: सम्मिलित करने हेतु अधिकतम स्वीकार्य (2 बाइट, मिलीसेकंड में औसत) - `rdelay`: अनुरोधित विलंब (2 बाइट, मिलीसेकंड में औसत)

**दिशानिर्देश:** - न्यूनतम मान वांछित ट्रैफ़िक विश्लेषण प्रतिरोध दर्शाते हैं - अधिकतम मान बैंडविड्थ सीमाएँ दर्शाते हैं - प्रेषक को प्राप्तकर्ता की अधिकतम सीमा का सम्मान करना चाहिए - प्रेषक, सीमाओं के भीतर, प्राप्तकर्ता की न्यूनतम सीमा का भी सम्मान कर सकता है - कोई प्रवर्तन तंत्र नहीं है; कार्यान्वयन भिन्न हो सकते हैं

### ब्लॉक प्रकार 2: RouterInfo (router की जानकारी)

netdb को भरने और फ्लडिंग के लिए RouterInfo का प्रेषण.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**उपयोग:**

**Message 3 के भाग 2 में** (हैंडशेक): - Alice अपनी RouterInfo (router की जानकारी) Bob को भेजती है - Flood bit आमतौर पर 0 (स्थानीय भंडारण) - RouterInfo gzip से संकुचित नहीं है

**डेटा चरण में:** - दोनों पक्षों में से कोई भी अपना अद्यतन RouterInfo भेज सकता है - Flood बिट = 1: floodfill वितरण का अनुरोध (यदि प्राप्तकर्ता floodfill है) - Flood बिट = 0: केवल स्थानीय netdb में भंडारण

**सत्यापन आवश्यकताएँ:** 1. सत्यापित करें कि हस्ताक्षर प्रकार समर्थित है 2. RouterInfo हस्ताक्षर सत्यापित करें 3. सत्यापित करें कि टाइमस्टैम्प स्वीकार्य सीमा के भीतर है 4. हैंडशेक के लिए: सत्यापित करें कि स्थिर कुंजी NTCP2 address के "s" पैरामीटर से मेल खाती है 5. डेटा चरण के लिए: सत्यापित करें कि router hash session peer (सत्र सहकर्मी) से मेल खाता है 6. केवल प्रकाशित पतों वाले RouterInfos को flood (प्रसारित) करें

**नोट्स:** - कोई ACK तंत्र नहीं है (आवश्यक होने पर reply token के साथ I2NP DatabaseStore का उपयोग करें) - तृतीय-पक्ष RouterInfos शामिल हो सकते हैं (floodfill का उपयोग) - gzip से संपीड़ित नहीं है (I2NP DatabaseStore के विपरीत)

### ब्लॉक प्रकार 3: I2NP संदेश

संक्षिप्त 9-बाइट हेडर वाला I2NP संदेश।

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**NTCP1 से अंतर:** - समाप्ति समय: 4 बाइट्स (सेकंड) बनाम 8 बाइट्स (मिलीसेकंड) - लंबाई: शामिल नहीं (ब्लॉक की लंबाई से निकाली जा सकती है) - चेकसम: शामिल नहीं (AEAD अखंडता प्रदान करता है) - हेडर: 9 बाइट्स बनाम 16 बाइट्स (44% कमी)

**खंडन:** - I2NP संदेशों को ब्लॉकों के पार कदापि खंडित नहीं किया जाना चाहिए - I2NP संदेशों को फ्रेमों के पार कदापि खंडित नहीं किया जाना चाहिए - प्रति फ्रेम एक से अधिक I2NP ब्लॉकों की अनुमति है

### ब्लॉक प्रकार 4: समापन

कारण कोड सहित स्पष्ट कनेक्शन बंद।

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**कारण कोड:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**नियम:** - समापन ब्लॉक फ्रेम में अंतिम non-padding ब्लॉक होना अनिवार्य है - प्रति फ्रेम अधिकतम एक समापन ब्लॉक - प्रेषक को भेजने के बाद कनेक्शन बंद कर देना चाहिए - प्राप्तकर्ता को प्राप्त करने के बाद कनेक्शन बंद कर देना चाहिए

**त्रुटि प्रबंधन:** - हैंडशेक त्रुटियाँ: आमतौर पर TCP RST (कनेक्शन रीसेट) के साथ बंद करें (कोई टर्मिनेशन ब्लॉक नहीं) - डेटा चरण AEAD (प्रमाणित एन्क्रिप्शन विद संबद्ध डेटा) त्रुटियाँ: यादृच्छिक टाइमआउट + यादृच्छिक रीड, फिर टर्मिनेशन भेजें - सुरक्षा प्रक्रियाओं के लिए "AEAD Error Handling" अनुभाग देखें

### ब्लॉक प्रकार 254: पैडिंग

ट्रैफ़िक विश्लेषण के प्रतिरोध के लिए यादृच्छिक padding (भराव डेटा)।

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**नियम:** - यदि मौजूद हो, तो पैडिंग फ़्रेम में अंतिम ब्लॉक होना अनिवार्य है - शून्य-लंबाई पैडिंग की अनुमति है - प्रति फ़्रेम केवल एक पैडिंग ब्लॉक की अनुमति है - केवल पैडिंग वाली फ़्रेमों की अनुमति है - Options block से सहमति से तय किए गए पैरामीटरों का पालन किया जाना चाहिए

**संदेश 1-2 में पैडिंग:** - AEAD (Authenticated Encryption with Associated Data — संबद्ध डेटा सहित प्रमाणीकरणयुक्त एन्क्रिप्शन) फ्रेम के बाहर (स्पष्ट-पाठ) - अगले संदेश की hash chain (हैश शृंखला) में शामिल (प्रमाणित) - छेड़छाड़ का पता तब चलता है जब अगले संदेश की AEAD विफल होती है

**Message 3+ और डेटा चरण में पैडिंग:** - AEAD फ्रेम के अंदर (एन्क्रिप्टेड और प्रमाणित) - ट्रैफ़िक शेपिंग और आकार को अस्पष्ट करने के लिए उपयोग किया जाता है

## AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) त्रुटि प्रबंधन

**अत्यावश्यक सुरक्षा आवश्यकताएँ:**

### हैंडशेक चरण (संदेश 1-3)

**ज्ञात संदेश आकार:** - संदेश का आकार पूर्वनिर्धारित होता है या पहले से निर्दिष्ट किया जाता है - AEAD (Authenticated Encryption with Associated Data, प्रमाणीकरण-सहित एन्क्रिप्शन व संबद्ध डेटा) प्रमाणीकरण विफलता असंदिग्ध होती है

**Message 1 विफलता पर Bob की प्रतिक्रिया:** 1. यादृच्छिक टाइमआउट सेट करें (सीमा कार्यान्वयन-निर्भर, सुझाव: 100-500ms) 2. बाइट्स की यादृच्छिक संख्या पढ़ें (सीमा कार्यान्वयन-निर्भर, सुझाव: 1KB-64KB) 3. TCP RST के साथ कनेक्शन बंद करें (कोई प्रतिक्रिया नहीं) 4. स्रोत IP को अस्थायी रूप से ब्लैकलिस्ट करें 5. दीर्घकालिक प्रतिबंधों के लिए बारंबार विफलताओं को ट्रैक करें

**Alice की Message 2 विफलता पर प्रतिक्रिया:** 1. TCP RST के साथ तुरंत कनेक्शन बंद करें 2. Bob को कोई प्रतिक्रिया नहीं

**Message 3 की विफलता पर Bob की प्रतिक्रिया:** 1. TCP RST (TCP में कनेक्शन रीसेट संकेत) के साथ तुरंत कनेक्शन बंद करें 2. Alice को कोई प्रतिक्रिया नहीं

### डेटा चरण

**अस्पष्टित संदेश का आकार:** - लंबाई फ़ील्ड SipHash (एक कुंजीयुक्त हैश फ़ंक्शन) द्वारा अस्पष्टित है - अमान्य लंबाई या AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) विफलता यह संकेत कर सकती है:   - हमलावर द्वारा जांच-पड़ताल   - नेटवर्क में डेटा क्षति   - असमन्वित SipHash IV (Initialization Vector—आरंभीकरण वेक्टर)   - दुर्भावनापूर्ण पीयर

**AEAD या लंबाई त्रुटि पर प्रतिक्रिया:** 1. यादृच्छिक टाइमआउट सेट करें (सुझाव 100-500ms) 2. बाइट्स की यादृच्छिक संख्या पढ़ें (सुझाव 1KB-64KB) 3. कारण कोड 4 (AEAD विफलता) या 9 (फ्रेमिंग त्रुटि) के साथ समापन ब्लॉक भेजें 4. कनेक्शन बंद करें

**Decryption Oracle (त्रुटि/टाइमिंग संकेतों के दुरुपयोग से डिक्रिप्शन-संबंधी जानकारी निकालने वाला हमला) की रोकथाम:** - यादृच्छिक टाइमआउट से पहले पीयर को कभी भी त्रुटि प्रकार प्रकट न करें - AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) जाँच से पहले लंबाई सत्यापन को कभी न छोड़ें - अमान्य लंबाई को AEAD विफलता के समान ही मानें - दोनों त्रुटियों के लिए समान त्रुटि-प्रबंधन पथ का उपयोग करें

**कार्यान्वयन संबंधी विचार:** - यदि AEAD त्रुटियाँ दुर्लभ हों, तो कुछ कार्यान्वयन जारी रह सकते हैं - बार-बार त्रुटियों के बाद समाप्त करें (सुझावित सीमा: प्रति घंटे 3-5 त्रुटियाँ) - त्रुटि पुनर्प्राप्ति और सुरक्षा के बीच संतुलन

## प्रकाशित RouterInfo (router संबंधी जानकारी)

### Router पते का प्रारूप

NTCP2 समर्थन को विशिष्ट विकल्पों के साथ प्रकाशित RouterAddress प्रविष्टियों के माध्यम से घोषित किया जाता है।

**ट्रांसपोर्ट शैली:** - `"NTCP2"` - इस पोर्ट पर केवल NTCP2 - `"NTCP"` - इस पोर्ट पर NTCP और NTCP2 दोनों (स्वतः पहचान)   - **नोट**: NTCP (v1) का समर्थन 0.9.50 (मई 2021) में हटाया गया   - "NTCP" शैली अब अप्रचलित है; "NTCP2" का उपयोग करें

### आवश्यक विकल्प

**सभी प्रकाशित NTCP2 पते:**

1. **`host`** - IP पता (IPv4 या IPv6) या होस्टनेम
   - प्रारूप: मानक IP संकेतन या डोमेन नाम
   - outbound-only (सिर्फ बाहर जाने वाले कनेक्शनों के लिए) या छिपे हुए routers के लिए इसे छोड़ा जा सकता है

2. **`port`** - TCP पोर्ट संख्या
   - प्रारूप: पूर्णांक, 1-65535
   - आउटबाउंड-ओनली या हिडन routers के लिए इसे छोड़ा जा सकता है

3. **`s`** - स्थिर सार्वजनिक कुंजी (X25519)
   - प्रारूप: Base64-एन्कोडेड, 44 अक्षर
   - एन्कोडिंग: I2P Base64 वर्णमाला
   - स्रोत: 32-बाइट X25519 सार्वजनिक कुंजी, little-endian (लिटल-एंडियन बाइट क्रम)

4. **`i`** - AES के लिए Initialization Vector (आरंभिक वेक्टर)
   - प्रारूप: Base64-एन्कोडेड, 24 वर्ण
   - एन्कोडिंग: I2P Base64 वर्णमाला
   - स्रोत: 16-बाइट IV, बिग-एंडियन

5. **`v`** - प्रोटोकॉल संस्करण
   - प्रारूप: पूर्णांक या कॉमा से अलग किए गए पूर्णांक
   - वर्तमान: `"2"`
   - भविष्य: `"2,3"` (संख्यात्मक क्रम में होना चाहिए)

**वैकल्पिक विकल्प:**

6. **`caps`** - क्षमताएँ (0.9.50 से)
   - प्रारूप: क्षमता वर्णों की स्ट्रिंग
   - मान:
     - `"4"` - IPv4 आउटबाउंड क्षमता
     - `"6"` - IPv6 आउटबाउंड क्षमता
     - `"46"` - दोनों IPv4 और IPv6 (अनुशंसित क्रम)
   - यदि `host` प्रकाशित हो तो आवश्यक नहीं
   - छिपे/फायरवॉल वाले routers के लिए उपयोगी

7. **`cost`** - पते की प्राथमिकता
   - प्रारूप: पूर्णांक (Integer), 0-255
   - कम मान = उच्च प्राथमिकता
   - अनुशंसित: सामान्य पते के लिए 5-10
   - अनुशंसित: अप्रकाशित पते के लिए 14

### उदाहरण RouterAddress प्रविष्टियाँ

**प्रकाशित IPv4 पता:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**छिपा Router (केवल आउटबाउंड):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**डुअल-स्टैक Router:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**महत्वपूर्ण नियम:** - **एक ही पोर्ट** वाले कई NTCP2 पतों के लिए **एक समान** `s`, `i`, और `v` मानों का उपयोग करना अनिवार्य है - अलग-अलग पोर्ट अलग कुंजियों का उपयोग कर सकते हैं - डुअल-स्टैक routers को अलग-अलग IPv4 और IPv6 पते प्रकाशित करने चाहिए

### अप्रकाशित NTCP2 पता

**केवल आउटबाउंड Routers के लिए:**

यदि कोई router आने वाली NTCP2 कनेक्शनों को स्वीकार नहीं करता, लेकिन आउटबाउंड कनेक्शनों को आरंभ करता है, तो उसे फिर भी निम्न के साथ एक RouterAddress प्रकाशित करना अनिवार्य है:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**उद्देश्य:** - हैंडशेक के दौरान Bob को Alice की स्थिर कुंजी सत्यापित करने की अनुमति देता है - संदेश 3 भाग 2 के RouterInfo सत्यापन के लिए आवश्यक - `i`, `host`, या `port` की आवश्यकता नहीं (केवल आउटबाउंड)

**विकल्प:** - पहले से प्रकाशित "NTCP" या SSU पते में `s` और `v` जोड़ें

### सार्वजनिक कुंजी और IV (Initialization Vector, आरंभिक वेक्टर) रोटेशन

**महत्वपूर्ण सुरक्षा नीति:**

**सामान्य नियम:** 1. **router चल रहा हो तो कभी रोटेट न करें** 2. **कुंजी और IV (Initialization Vector, आरंभीकरण वैक्टर) को स्थायी रूप से संग्रहीत करें** रीस्टार्ट्स के दौरान भी 3. **पिछले डाउनटाइम को ट्रैक करें** रोटेशन की पात्रता निर्धारित करने के लिए

**रोटेशन से पहले न्यूनतम डाउनटाइम:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**अतिरिक्त ट्रिगर्स:** - स्थानीय IP पता परिवर्तन: डाउनटाइम की परवाह किए बिना बदल सकता है - Router "rekey" (नया Router हैश): नई कुंजियाँ उत्पन्न करता है

**औचित्य:** - कुंजी परिवर्तनों के माध्यम से पुनरारंभ समय उजागर होने से रोकता है - कैश की गई RouterInfos (router सूचना रिकॉर्ड) को स्वाभाविक रूप से समाप्त होने देता है - नेटवर्क की स्थिरता बनाए रखता है - असफल कनेक्शन प्रयासों को कम करता है

**कार्यान्वयन:** 1. कुंजी, IV, और पिछले शटडाउन का टाइमस्टैम्प स्थायी रूप से संग्रहीत करें 2. स्टार्टअप पर, downtime = current_time - last_shutdown की गणना करें 3. यदि downtime > router प्रकार के लिए न्यूनतम से अधिक है, तो रोटेट किया जा सकता है 4. यदि IP बदल गया है या rekeying (कुंजी पुनर्निर्धारण) किया जा रहा है, तो रोटेट किया जा सकता है 5. अन्यथा, पिछली कुंजी और IV का पुन: उपयोग करें

**IV Rotation (IV रोटेशन):** - कुंजी रोटेशन के समान नियम लागू होते हैं - केवल प्रकाशित पतों में मौजूद (छिपे हुए routers में नहीं) - जब भी कुंजी बदले, IV बदलना अनुशंसित है

## संस्करण पहचान

**संदर्भ:** जब `transportStyle="NTCP"` (लेगेसी) हो, Bob एक ही पोर्ट पर NTCP v1 और v2 दोनों का समर्थन करता है और उसे प्रोटोकॉल संस्करण का स्वतः पता लगाना चाहिए।

**डिटेक्शन एल्गोरिदम:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**तेज़ MSB (सबसे महत्त्वपूर्ण बिट) जाँच:** - AES डिक्रिप्शन से पहले, यह जाँचें: `encrypted_X[31] & 0x80 == 0` - मान्य X25519 कुंजियों में उच्च बिट clear (शून्य) होता है - विफलता इंगित करती है कि यह संभवतः NTCP1 (या हमला) है - विफलता पर probing resistance (प्रोबिंग के प्रति प्रतिरोध) लागू करें (random timeout + read)

**कार्यान्वयन आवश्यकताएँ:**

1. **Alice की ज़िम्मेदारी:**
   - "NTCP" पते से जुड़ते समय, संदेश 1 को अधिकतम 287 बाइट्स तक सीमित करें
   - पूरे संदेश 1 को बफर करें और एक ही बार में फ्लश करें
   - एकल TCP पैकेट में डिलीवरी की संभावना बढ़ती है

2. **Bob की ज़िम्मेदारियाँ:**
   - संस्करण तय करने से पहले प्राप्त डेटा को बफर करें
   - उचित timeout (समयसीमा) हैंडलिंग लागू करें
   - तेज़ संस्करण पहचान के लिए TCP_NODELAY का उपयोग करें
   - संस्करण का पता चलने के बाद पूरे संदेश 2 को एक ही बार में बफर करें और फ्लश करें

**सुरक्षा संबंधी विचार:** - सेगमेंटेशन हमले: Bob को TCP segmentation (TCP पैकेटों का खंडन) के प्रति प्रतिरोधी होना चाहिए - प्रोबिंग हमले (जांच-परख आधारित): विफलताओं पर यादृच्छिक विलंब और बाइट-पठन लागू करें - DoS (Denial of Service, सेवा-अस्वीकरण) की रोकथाम: एक साथ लंबित कनेक्शनों की सीमा निर्धारित करें - रीड टाइमआउट्स: प्रति-रीड और कुल दोनों ("slowloris" (धीमी-कनेक्शन हमला) सुरक्षा)

## Clock Skew (सिस्टम घड़ी का अंतर) दिशानिर्देश

**टाइमस्टैम्प फ़ील्ड:** - संदेश 1: `tsA` (Alice का टाइमस्टैम्प) - संदेश 2: `tsB` (Bob का टाइमस्टैम्प) - संदेश 3+: वैकल्पिक DateTime ब्लॉक्स

**अधिकतम Skew (विचलन) (D):** - सामान्य: **±60 सेकंड** - प्रत्येक कार्यान्वयन के अनुसार विन्यास योग्य - Skew > D आमतौर पर घातक होता है

### बॉब की हैंडलिंग (संदेश 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**औचित्य:** skew (घड़ी का अंतर) होने पर भी संदेश 2 भेजना Alice को घड़ी-संबंधित समस्याओं का निदान करने में सक्षम बनाता है।

### ऐलिस की हैंडलिंग (संदेश 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**RTT (राउंड-ट्रिप टाइम) समायोजन:** - गणना किए गए skew (घड़ी का विचलन) से आधा RTT घटाएँ - नेटवर्क प्रसार विलंब को ध्यान में रखता है - skew का अधिक सटीक आकलन

### बॉब का प्रसंस्करण (संदेश 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### समय समकालिकरण

**DateTime ब्लॉक्स (डेटा चरण):** - समय-समय पर DateTime ब्लॉक भेजें (type 0) - प्राप्तकर्ता इसे घड़ी समायोजन के लिए उपयोग कर सकता है - timestamp (समय-मुद्रा) को निकटतम सेकंड तक राउंड करें (बायस से बचें)

**बाहरी समय स्रोत:** - NTP (Network Time Protocol) - सिस्टम क्लॉक समकालिकरण - I2P नेटवर्क सर्वसम्मति समय

**घड़ी समायोजन रणनीतियाँ:** - यदि स्थानीय घड़ी गलत है: सिस्टम समय समायोजित करें या ऑफ़सेट का उपयोग करें - यदि समकक्षों की घड़ियाँ लगातार गलत हैं: समकक्ष-संबंधी समस्या को चिह्नित करें - नेटवर्क स्वास्थ्य निगरानी के लिए स्क्यू (समय विचलन) आँकड़ों को ट्रैक करें

## सुरक्षा गुणधर्म

### Forward Secrecy (अग्रसक्रिय गोपनीयता)

**निम्न के माध्यम से प्राप्त:** - Ephemeral Diffie-Hellman key exchange (X25519; अस्थायी Diffie-Hellman कुंजी विनिमय) - तीन DH ऑपरेशन्स: es, ee, se (Noise XK pattern; Noise प्रोटोकॉल का XK हैंडशेक पैटर्न) - हैंडशेक पूरा होने के बाद अस्थायी कुंजियाँ नष्ट कर दी जाती हैं

**गोपनीयता का क्रम:** - संदेश 1: स्तर 2 (forward secrecy (कुंजी से समझौता हो जाने के बाद भी पुराने संदेश सुरक्षित रहने का गुण) प्रेषक के समझौते की स्थिति में) - संदेश 2: स्तर 1 (अस्थायी प्राप्तकर्ता) - संदेश 3+: स्तर 5 (मजबूत forward secrecy)

**Perfect Forward Secrecy (पूर्व सत्रों की गोपनीयता सुनिश्चित करने वाला गुण):** - दीर्घकालिक स्थिर कुंजियों का समझौता होने पर भी पिछले सत्रों की कुंजियाँ उजागर नहीं होतीं - प्रत्येक सत्र अद्वितीय अस्थायी कुंजियों का उपयोग करता है - अस्थायी निजी कुंजियों का कभी पुनः उपयोग नहीं होता - कुंजी सहमति के बाद मेमोरी की सफ़ाई

**सीमाएँ:** - संदेश 1 असुरक्षित है यदि Bob की स्थिर कुंजी से समझौता हो जाए (लेकिन Alice के समझौते के बावजूद forward secrecy (आगे की गोपनीयता) बनी रहती है) - संदेश 1 पर रीप्ले हमले संभव हैं (टाइमस्टैम्प और रीप्ले कैश से शमन किया जाता है)

### प्रमाणीकरण

**परस्पर प्रमाणीकरण:** - Alice का प्रमाणीकरण संदेश 3 में स्थायी कुंजी द्वारा - Bob का प्रमाणीकरण स्थायी निजी कुंजी के स्वामित्व से (सफल हैंडशेक से अप्रत्यक्ष रूप से)

**Key Compromise Impersonation (KCI) प्रतिरोध:** - प्रमाणीकरण स्तर 2 (KCI के प्रति प्रतिरोधी) - हमलावर Alice की static private key (स्थायी निजी कुंजी) होने पर भी Alice का प्रतिरूपण नहीं कर सकता (Alice की ephemeral key (अल्पकालिक कुंजी) के बिना) - हमलावर Bob की static private key होने पर भी Bob का प्रतिरूपण नहीं कर सकता (Bob की ephemeral key के बिना)

**स्थिर कुंजी सत्यापन:** - Alice को पहले से Bob की स्थिर कुंजी पता होती है (RouterInfo से) - Bob संदेश 3 में यह सत्यापित करता है कि Alice की स्थिर कुंजी RouterInfo से मेल खाती है - मैन-इन-द-मिडल हमलों को रोकता है

### ट्रैफ़िक विश्लेषण के प्रति प्रतिरोधक क्षमता

**DPI (Deep Packet Inspection: गहन पैकेट निरीक्षण) प्रतिरोधक उपाय:** 1. **AES Obfuscation:** अल्पकालिक कुंजियाँ एन्क्रिप्ट की जाती हैं, आउटपुट यादृच्छिक दिखाई देता है 2. **SipHash Length Obfuscation:** फ्रेम की लंबाइयाँ प्लेनटेक्स्ट में नहीं होतीं 3. **Random Padding:** संदेश आकार परिवर्तनीय, कोई स्थिर पैटर्न नहीं 4. **Encrypted Frames:** सारा पेलोड ChaCha20 से एन्क्रिप्ट किया गया है

**रीप्ले हमले की रोकथाम:** - टाइमस्टैम्प सत्यापन (±60 सेकंड) - अल्पकालिक कुंजियों का रीप्ले कैश (जीवनकाल 2*D) - Nonce (एक-बार उपयोग संख्या) में वृद्धि सत्र के भीतर पैकेट रीप्ले को रोकती है

**प्रोबिंग प्रतिरोध:** - AEAD (Authenticated Encryption with Associated Data - संबद्ध डेटा के साथ प्रमाणित एन्क्रिप्शन) विफलताओं पर यादृच्छिक टाइमआउट - कनेक्शन बंद करने से पहले यादृच्छिक बाइट पढ़ना - हैंडशेक विफलताओं पर कोई प्रतिक्रिया नहीं - बार-बार विफलताओं पर IP ब्लैकलिस्टिंग

**पैडिंग दिशानिर्देश:** - संदेश 1-2: क्लियरटेक्स्ट पैडिंग (प्रमाणित) - संदेश 3+: AEAD (प्रमाणीकरणयुक्त संबद्ध डेटा सहित एन्क्रिप्शन) फ़्रेम्स के भीतर एन्क्रिप्टेड पैडिंग - नेगोशिएट किए गए पैडिंग पैरामीटर्स (Options block) - केवल पैडिंग वाले फ़्रेम्स अनुमत हैं

### Denial of Service (सेवा-वंचन) शमन

**कनेक्शन सीमाएँ:** - अधिकतम सक्रिय कनेक्शन (क्रियान्वयन-निर्भर) - अधिकतम लंबित हैंडशेक (उदा., 100-1000) - प्रति-IP कनेक्शन सीमाएँ (उदा., 3-10 एक साथ)

**संसाधन सुरक्षा:** - DH (Diffie-Hellman) संचालन दर-सीमित (गणनात्मक रूप से महँगा) - रीड टाइमआउट प्रति-सॉकेट और कुल - "Slowloris" (धीमे कनेक्शन-आधारित हमला) से सुरक्षा (कुल समय सीमाएँ) - दुरुपयोग पर IP ब्लैकलिस्टिंग

**त्वरित अस्वीकृति:** - Network ID असंगति → तत्काल बंद - अमान्य X25519 बिंदु → डिक्रिप्शन से पहले त्वरित MSB (सबसे महत्वपूर्ण बिट) जाँच - समय-चिह्न सीमा से बाहर → किसी गणना के बिना बंद - AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) विफलता → कोई प्रतिक्रिया नहीं, यादृच्छिक विलंब

**प्रोबिंग प्रतिरोधक क्षमता:** - यादृच्छिक टाइमआउट: 100-500ms (कार्यान्वयन-निर्भर) - यादृच्छिक रीड: 1KB-64KB (कार्यान्वयन-निर्भर) - हमलावर को कोई त्रुटि जानकारी नहीं - TCP RST (तुरंत कनेक्शन रीसेट संकेत) के साथ बंद करें (कोई FIN handshake नहीं)

### क्रिप्टोग्राफिक सुरक्षा

**एल्गोरिद्म:** - **X25519**: 128-बिट सुरक्षा, दीर्घवृत्तीय वक्र DH (Curve25519) - **ChaCha20**: 256-बिट कुंजी वाला स्ट्रीम सिफर - **Poly1305**: सूचना-सैद्धांतिक रूप से सुरक्षित MAC (संदेश प्रमाणीकरण कोड) - **SHA-256**: 128-बिट टक्कर प्रतिरोध, 256-बिट पूर्व-छवि प्रतिरोध - **HMAC-SHA256**: कुंजी व्युत्पत्ति हेतु PRF (छद्म‑यादृच्छिक फलन)

**कुंजी आकार:** - स्थिर कुंजियाँ: 32 बाइट (256 बिट) - अल्पकालिक कुंजियाँ: 32 बाइट (256 बिट) - कूटलेखन कुंजियाँ: 32 बाइट (256 बिट) - MAC: 16 बाइट (128 बिट)

**ज्ञात समस्याएँ:** - ChaCha20 nonce (एक-बार-प्रयोग संख्या) का पुनः उपयोग विनाशकारी है (काउंटर बढ़ाकर रोका जाता है) - X25519 में छोटे उपसमूह से संबंधित समस्याएँ हैं (कर्व सत्यापन द्वारा कम की जाती हैं) - SHA-256 सैद्धांतिक रूप से length extension (लंबाई-विस्तार) के प्रति असुरक्षित है (HMAC में शोषण योग्य नहीं)

**कोई ज्ञात कमजोरियाँ नहीं (अक्टूबर 2025 तक):** - Noise Protocol Framework (एन्क्रिप्टेड हैंडशेक बनाने के लिए क्रिप्टोग्राफिक ढांचा) का व्यापक विश्लेषण - ChaCha20-Poly1305 (प्रमाणित एन्क्रिप्शन एल्गोरिदम) TLS 1.3 (Transport Layer Security का संस्करण 1.3) में प्रयुक्त - X25519 (कुंजी-विनिमय एलिप्टिक-कर्व एल्गोरिदम) आधुनिक प्रोटोकॉल में मानक - क्रिप्टोग्राफिक निर्माण पर कोई व्यावहारिक हमला नहीं

## संदर्भ

### मुख्य विनिर्देश

- **[NTCP2 Specification](/docs/specs/ntcp2/)** - आधिकारिक I2P विनिर्देश
- **[Proposal 111](/proposals/111-ntcp-2/)** - औचित्य सहित मूल डिज़ाइन दस्तावेज़
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - संशोधन 33 (2017-10-04)

### कूटलेखन मानक

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - सुरक्षा के लिए अण्डाकार वक्र (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - IETF प्रोटोकॉलों के लिए ChaCha20 और Poly1305
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (RFC 7539 को अप्रचलित करता है)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: संदेश प्रमाणीकरण के लिए कुंजी-आधारित हैशिंग
- **[SipHash](https://www.131002.net/siphash/)** - हैश फ़ंक्शन अनुप्रयोगों के लिए SipHash-2-4

### संबंधित I2P विनिर्देश

- **[I2NP विनिर्देश](/docs/specs/i2np/)** - I2P नेटवर्क प्रोटोकॉल संदेश प्रारूप
- **[सामान्य संरचनाएँ](/docs/specs/common-structures/)** - RouterInfo (राउटर की जानकारी), RouterAddress (राउटर का पता) के प्रारूप
- **[SSU ट्रांसपोर्ट](/docs/legacy/ssu/)** - UDP ट्रांसपोर्ट (मूल, अब SSU2)
- **[प्रस्ताव 147](/proposals/147-transport-network-id-check/)** - ट्रांसपोर्ट नेटवर्क ID जाँच (0.9.42)

### कार्यान्वयन संदर्भ

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - संदर्भ कार्यान्वयन (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++ कार्यान्वयन
- **[I2P रिलीज़ नोट्स](/blog/)** - संस्करण इतिहास और अद्यतन

### ऐतिहासिक संदर्भ

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Noise framework (क्रिप्टोग्राफ़िक हैंडशेक का ढांचा) के लिए प्रेरणा
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (अदल-बदल योग्य ट्रैफ़िक-छिपाव माध्यम) (SipHash आधारित लंबाई-छिपाव का पूर्व उदाहरण)

## कार्यान्वयन दिशानिर्देश

### अनिवार्य आवश्यकताएँ

**अनुपालन हेतु:**

1. **पूर्ण हैंडशेक लागू करें:**
   - सही KDF chains (Key Derivation Function यानी कुंजी व्युत्पत्ति फ़ंक्शन की श्रृंखलाएँ) के साथ सभी तीन संदेशों का समर्थन करें
   - सभी AEAD tags (सम्बद्ध डेटा सहित प्रमाणीकरणयुक्त एन्क्रिप्शन के टैग) को सत्यापित करें
   - सुनिश्चित करें कि X25519 points (एलिप्टिक-कर्व X25519 के बिंदु) वैध हैं

2. **डेटा चरण लागू करें:**
   - SipHash लंबाई अस्पष्टकरण (दोनों दिशाओं में)
   - सभी ब्लॉक प्रकार: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - उचित nonce (एक-बार-प्रयोग संख्या) प्रबंधन (अलग-अलग काउंटर)

3. **सुरक्षा विशेषताएँ:**
   - रीप्ले रोकथाम (अल्पकालिक कुंजियों को 2*D के लिए कैश करना)
   - टाइमस्टैम्प सत्यापन (डिफ़ॉल्ट ±60 सेकंड)
   - संदेश 1-2 में यादृच्छिक पैडिंग
   - AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) त्रुटि प्रबंधन यादृच्छिक टाइमआउट्स के साथ

4. **RouterInfo (router की सूचना) प्रकाशन:**
   - स्थिर कुंजी ("s"), IV (Initialization Vector—आरंभीकरण वेक्टर) ("i"), और संस्करण ("v") प्रकाशित करें
   - नीति के अनुसार कुंजियों का आवर्तन करें
   - छिपे हुए routers के लिए capabilities फ़ील्ड ("caps") का समर्थन करें

5. **नेटवर्क संगतता:**
   - नेटवर्क ID फ़ील्ड का समर्थन करें (वर्तमान में मुख्य नेटवर्क के लिए 2)
   - मौजूदा Java और i2pd कार्यान्वयनों के साथ परस्पर-संचालित हों
   - IPv4 और IPv6 दोनों को संभालें

### अनुशंसित प्रथाएँ

**प्रदर्शन अनुकूलन:**

1. **बफ़रिंग रणनीति:**
   - पूरे संदेशों को एक साथ फ्लश करें (संदेश 1, 2, 3)
   - हैंडशेक संदेशों के लिए TCP_NODELAY का उपयोग करें
   - कई डेटा ब्लॉकों को एकल फ्रेम में बफ़र करें
   - फ्रेम का आकार कुछ KB तक सीमित रखें (प्राप्तकर्ता लेटेंसी को न्यूनतम करें)

2. **कनेक्शन प्रबंधन:**
   - जहाँ संभव हो कनेक्शनों का पुनः उपयोग करें
   - कनेक्शन पूलिंग लागू करें
   - कनेक्शन स्वास्थ्य की निगरानी करें (DateTime blocks (तिथि-समय ब्लॉक्स))

3. **मेमोरी प्रबंधन:**
   - उपयोग के बाद संवेदनशील डेटा को शून्य करें (ephemeral keys (अस्थायी कुंजियाँ), DH results (Diffie-Hellman के परिणाम))
   - समवर्ती हैंडशेक की सीमा तय करें (DoS (Denial-of-Service/सेवा-अस्वीकरण) की रोकथाम)
   - बार-बार होने वाले आवंटन के लिए मेमोरी पूल का उपयोग करें

**सुरक्षा सुदृढ़ीकरण:**

1. **प्रोबिंग प्रतिरोध:**
   - यादृच्छिक टाइमआउट: 100-500ms
   - यादृच्छिक बाइट रीड्स: 1KB-64KB
   - बार-बार विफलताओं पर IP ब्लैकलिस्टिंग
   - पीयर्स को कोई त्रुटि विवरण नहीं

2. **संसाधन सीमाएँ:**
   - प्रति IP अधिकतम कनेक्शन: 3-10
   - अधिकतम लंबित हैंडशेक: 100-1000
   - पठन समयसीमाएँ: प्रति ऑपरेशन 30-60 सेकंड
   - कुल कनेक्शन समयसीमा: हैंडशेक के लिए 5 मिनट

3. **कुंजी प्रबंधन:**
   - स्थिर कुंजी और IV (Initialization Vector—प्रारंभन वेक्टर) का स्थायी भंडारण
   - सुरक्षित यादृच्छिक उत्पत्ति (cryptographic RNG)
   - रोटेशन नीतियों का कड़ाई से पालन करें
   - अस्थायी कुंजियों का कभी पुनः उपयोग न करें

**निगरानी और निदान:**

1. **मेट्रिक्स:**
   - हैंडशेक की सफलता/विफलता दरें
   - AEAD (प्रमाणित एन्क्रिप्शन, संबद्ध डेटा सहित) त्रुटि दरें
   - क्लॉक स्क्यू का वितरण
   - कनेक्शन अवधि के आँकड़े

2. **लॉगिंग:**
   - हैंडशेक विफलताओं को कारण कोड सहित लॉग करें
   - क्लॉक स्क्यू घटनाओं को लॉग करें
   - प्रतिबंधित IP पतों को लॉग करें
   - संवेदनशील कुंजी सामग्री को कभी भी लॉग न करें

3. **परीक्षण:**
   - KDF (कुंजी व्युत्पत्ति फ़ंक्शन) श्रृंखलाओं के लिए यूनिट परीक्षण
   - अन्य कार्यान्वयनों के साथ एकीकरण परीक्षण
   - पैकेट हैंडलिंग के लिए Fuzzing (अनियमित इनपुट परीक्षण)
   - DoS (सेवा-अस्वीकरण हमला) प्रतिरोधक क्षमता के लिए लोड परीक्षण

### आम गलतियाँ

**बचने योग्य गंभीर त्रुटियाँ:**

1. **Nonce (एक बार प्रयुक्त संख्या) का पुन:उपयोग:**
   - सत्र के दौरान nonce काउंटर को कभी रीसेट न करें
   - प्रत्येक दिशा के लिए अलग-अलग काउंटर का उपयोग करें
   - 2^64 - 1 तक पहुँचने से पहले समाप्त करें

2. **कुंजी रोटेशन:**
   - जब router चल रहा हो, तब कभी कुंजियों को रोटेट न करें
   - विभिन्न सत्रों के बीच अस्थायी (ephemeral) कुंजियों का पुन: उपयोग कभी न करें
   - न्यूनतम डाउनटाइम के नियमों का पालन करें

3. **टाइमस्टैम्प प्रबंधन:**
   - अवधि-समाप्त टाइमस्टैम्प कभी स्वीकार न करें
   - समय विचलन की गणना करते समय RTT (राउंड-ट्रिप टाइम) के अनुसार हमेशा समायोजन करें
   - DateTime टाइमस्टैम्प को सेकंड तक राउंड करें

4. **AEAD (Authenticated Encryption with Associated Data - प्रमाणित एन्क्रिप्शन विद एसोसिएटेड डेटा) त्रुटियाँ:**
   - हमलावर को कभी भी त्रुटि के प्रकार का खुलासा न करें
   - बंद करने से पहले हमेशा एक यादृच्छिक टाइमआउट का उपयोग करें
   - अमान्य लंबाई को AEAD विफलता के समान समझें

5. **पैडिंग:**
   - सहमत सीमाओं के बाहर कभी भी पैडिंग न भेजें
   - पैडिंग ब्लॉक को हमेशा सबसे अंत में रखें
   - प्रति फ़्रेम कभी भी एक से अधिक पैडिंग ब्लॉक न हों

6. **RouterInfo:**
   - हमेशा यह सत्यापित करें कि static key (स्थिर कुंजी) RouterInfo से मेल खाती है
   - प्रकाशित पतों के बिना RouterInfos को कभी भी प्रसारित न करें
   - हमेशा हस्ताक्षरों को सत्यापित करें

### परीक्षण कार्यप्रणाली

**यूनिट परीक्षण:**

1. **क्रिप्टोग्राफ़िक प्रिमिटिव्स:**
   - X25519, ChaCha20, Poly1305, SHA-256 के लिए परीक्षण वेक्टर
   - HMAC-SHA256 के परीक्षण वेक्टर
   - SipHash-2-4 के परीक्षण वेक्टर

2. **KDF चेन:**
   - तीनों संदेशों के लिए ज्ञात-उत्तर परीक्षण
   - चेनिंग कुंजी के प्रसार का सत्यापन करें
   - SipHash IV निर्माण का परीक्षण करें

3. **संदेश पार्सिंग:**
   - मान्य संदेश डिकोडिंग
   - अमान्य संदेश अस्वीकृति
   - सीमा स्थितियाँ (रिक्त, अधिकतम आकार)

**एकीकरण परीक्षण:**

1. **हैंडशेक:**
   - सफल तीन-संदेश आदान-प्रदान
   - क्लॉक-स्क्यू के आधार पर अस्वीकृति
   - रीप्ले हमले की पहचान
   - अमान्य कुंजी की अस्वीकृति

2. **डेटा चरण:**
   - I2NP संदेश स्थानांतरण
   - RouterInfo आदान-प्रदान
   - पैडिंग का प्रबंधन
   - समापन संदेश

3. **अंतरसंचालनीयता:**
   - Java I2P के साथ परीक्षण करें
   - i2pd के साथ परीक्षण करें
   - IPv4 और IPv6 का परीक्षण करें
   - प्रकाशित और छिपे हुए routers का परीक्षण करें

**सुरक्षा परीक्षण:**

1. **नकारात्मक परीक्षण:**
   - अमान्य AEAD (संबद्ध डेटा सहित प्रमाणित एन्क्रिप्शन) टैग
   - रीप्ले किए गए संदेश
   - क्लॉक स्क्यू हमले
   - गलत-संरूपित फ़्रेम

2. **DoS (सेवा-अस्वीकरण) परीक्षण:**
   - कनेक्शन फ्लडिंग
   - Slowloris हमले (धीमे-कनेक्शन आधारित)
   - CPU पर अत्यधिक भार (अत्यधिक DH (Diffie-Hellman कुंजी-विनिमय))
   - मेमोरी समाप्ति

3. **फज़िंग (Fuzzing):**
   - यादृच्छिक हैंडशेक संदेश
   - यादृच्छिक डेटा चरण फ्रेम
   - यादृच्छिक ब्लॉक प्रकार और आकार
   - अमान्य क्रिप्टोग्राफिक मान

### NTCP (ट्रांसपोर्ट प्रोटोकॉल) से माइग्रेशन

**पुराने NTCP (I2P का TCP-आधारित ट्रांसपोर्ट प्रोटोकॉल) के समर्थन हेतु (अब हटा दिया गया):**

NTCP (version 1) को I2P 0.9.50 (मई 2021) में हटा दिया गया था। सभी वर्तमान कार्यान्वयनों को NTCP2 का समर्थन करना आवश्यक है। ऐतिहासिक टिप्पणियाँ:

1. **संक्रमण अवधि (2018-2021):**
   - 0.9.36: NTCP2 पेश किया गया (डिफ़ॉल्ट रूप से निष्क्रिय)
   - 0.9.37: NTCP2 डिफ़ॉल्ट रूप से सक्षम
   - 0.9.40: NTCP अप्रचलित घोषित किया गया
   - 0.9.50: NTCP हटा दिया गया

2. **संस्करण पहचान:**
   - "NTCP" transportStyle दोनों संस्करणों का समर्थन दर्शाता था
   - "NTCP2" transportStyle केवल NTCP2 को दर्शाता था
   - संदेश आकार के माध्यम से स्वचालित पहचान (287 बनाम 288 बाइट्स)

3. **वर्तमान स्थिति:**
   - सभी routers को NTCP2 का समर्थन करना अनिवार्य है
   - "NTCP" transportStyle अब अप्रचलित है
   - केवल "NTCP2" transportStyle का उपयोग करें

## परिशिष्ट A: Noise XK Pattern (Noise प्रोटोकॉल फ़्रेमवर्क का XK हैंडशेक पैटर्न)

**मानक Noise XK पैटर्न:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**व्याख्या:**

- `<-` : उत्तरदाता (Bob) से प्रारंभकर्ता (Alice) को संदेश
- `->` : प्रारंभकर्ता (Alice) से उत्तरदाता (Bob) को संदेश
- `s` : स्थिर कुंजी (दीर्घकालिक पहचान कुंजी)
- `rs` : रिमोट स्थिर कुंजी (पीयर की स्थिर कुंजी, पहले से ज्ञात)
- `e` : अस्थायी कुंजी (सत्र-विशिष्ट, आवश्यकतानुसार उत्पन्न)
- `es` : अस्थायी-स्थिर DH (डिफी-हेल्मन कुंजी-सहमति) (Alice अस्थायी × Bob स्थिर)
- `ee` : अस्थायी-अस्थायी DH (Alice अस्थायी × Bob अस्थायी)
- `se` : स्थिर-अस्थायी DH (Alice स्थिर × Bob अस्थायी)

**कुंजी सहमति क्रम:**

1. **पूर्व-संदेश:** Alice को Bob की static public key (स्थैतिक सार्वजनिक कुंजी) ज्ञात है (RouterInfo से)
2. **संदेश 1:** Alice ephemeral key (क्षणिक कुंजी) भेजती है, es DH निष्पादित करती है
3. **संदेश 2:** Bob ephemeral key भेजता है, ee DH निष्पादित करता है
4. **संदेश 3:** Alice static key (स्थैतिक कुंजी) प्रकट करती है, se DH निष्पादित करती है

**सुरक्षा विशेषताएँ:**

- Alice प्रमाणित: हाँ (message 3 द्वारा)
- Bob प्रमाणित: हाँ (स्थिर निजी कुंजी के पास होने से)
- Forward secrecy (आगे की गोपनीयता): हाँ (क्षणिक कुंजियाँ नष्ट कर दी जाती हैं)
- KCI resistance (Known-Compromise Impersonation प्रतिरोध): हाँ (प्रमाणीकरण स्तर 2)

## परिशिष्ट बी: Base64 Encoding (बाइनरी डेटा को ASCII-पाठ में बदलने की मानक विधि)

**I2P Base64 (64-आधारित एन्कोडिंग) वर्णमाला:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Standard Base64 से अंतर:** - वर्ण 62-63: `-~` `+/` के बजाय - पैडिंग: समान (`=`) या संदर्भ के अनुसार छोड़ी जा सकती है

**NTCP2 में उपयोग:** - स्थिर कुंजी ("s"): 32 बाइट्स → 44 अक्षर (बिना पैडिंग) - IV (इनिशियलाइज़ेशन वेक्टर) ("i"): 16 बाइट्स → 24 अक्षर (बिना पैडिंग)

**एन्कोडिंग उदाहरण:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## परिशिष्ट C: पैकेट कैप्चर विश्लेषण

**NTCP2 ट्रैफ़िक की पहचान:**

1. **TCP हैंडशेक:**
   - मानक TCP SYN, SYN-ACK, ACK
   - गंतव्य पोर्ट आमतौर पर 8887 या इसी तरह

2. **संदेश 1 (SessionRequest):**
   - एलिस से पहला एप्लिकेशन डेटा
   - 80-65535 बाइट (आमतौर पर कुछ सौ)
   - यादृच्छिक प्रतीत होता है (AES से एन्क्रिप्ट की गई अस्थायी कुंजी)
   - यदि "NTCP" पते से कनेक्ट हो रहे हों तो अधिकतम 287 बाइट

3. **संदेश 2 (SessionCreated):**
   - Bob से प्रतिक्रिया
   - 80-65535 बाइट (आमतौर पर कुछ सौ)
   - यह भी यादृच्छिक प्रतीत होता है

4. **संदेश 3 (SessionConfirmed - सत्र पुष्टि):**
   - Alice से
   - 48 बाइट + परिवर्ती (RouterInfo का आकार + पैडिंग)
   - आम तौर पर 1-4 KB

5. **डेटा चरण:**
   - परिवर्ती लंबाई के फ़्रेम
   - लंबाई फ़ील्ड अस्पष्ट किया गया (यादृच्छिक प्रतीत होता है)
   - कूटबद्ध पेलोड
   - पैडिंग आकार को अप्रत्याशित बनाती है

**DPI (गहन पैकेट निरीक्षण) से बचाव:** - कोई सादा-पाठ हेडर नहीं - कोई स्थिर पैटर्न नहीं - लंबाई फ़ील्ड अस्पष्ट किए गए - रैंडम पैडिंग आकार-आधारित heuristics (अनुमान-नियम) को तोड़ती है

**NTCP से तुलना:** - NTCP संदेश 1 हमेशा 288 बाइट का होता है (पहचानने योग्य) - NTCP2 संदेश 1 का आकार बदलता रहता है (पहचानने योग्य नहीं) - NTCP में पहचानने योग्य पैटर्न थे - NTCP2 को DPI (डीप पैकेट निरीक्षण) का प्रतिरोध करने के लिए डिज़ाइन किया गया है

## परिशिष्ट D: संस्करण इतिहास

**मुख्य मील के पत्थर:**

- **0.9.36** (अगस्त 23, 2018): NTCP2 का परिचय कराया गया, डिफ़ॉल्ट रूप से निष्क्रिय
- **0.9.37** (अक्टूबर 4, 2018): NTCP2 डिफ़ॉल्ट रूप से सक्षम
- **0.9.40** (मई 20, 2019): NTCP को अप्रचलित घोषित किया गया
- **0.9.42** (अगस्त 27, 2019): Network ID फ़ील्ड जोड़ी गई (प्रस्ताव 147)
- **0.9.50** (मई 17, 2021): NTCP को हटा दिया गया, क्षमताओं के लिए समर्थन जोड़ा गया
- **2.10.0** (सितंबर 9, 2025): नवीनतम स्थिर रिलीज़

**प्रोटोकॉल स्थिरता:** - 0.9.50 से कोई पिछली संगतता तोड़ने वाले परिवर्तन नहीं - प्रोबिंग प्रतिरोध में निरंतर सुधार - प्रदर्शन और विश्वसनीयता पर ध्यान - Post-quantum cryptography (क्वांटम कंप्यूटिंग-प्रतिरोधी कूटलेखन) विकासाधीन (डिफ़ॉल्ट रूप से सक्षम नहीं)

**वर्तमान ट्रांसपोर्ट स्थिति:** - NTCP2: अनिवार्य TCP ट्रांसपोर्ट - SSU2: अनिवार्य UDP ट्रांसपोर्ट - NTCP (v1): हटाया गया - SSU (v1): हटाया गया
