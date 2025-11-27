---
title: "नए netDB एंट्रीज़"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "खुला"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## स्थिति

इस प्रस्ताव के कुछ हिस्से पूर्ण हैं, और 0.9.38 और 0.9.39 में लागू किए गए हैं। Common Structures, I2CP, I2NP, और अन्य विशिष्टताएं अब उन परिवर्तनों को प्रतिबिंबित करने के लिए अपडेट की गई हैं जो अब समर्थित हैं।

पूर्ण किए गए हिस्से अभी भी मामूली संशोधन के अधीन हैं। इस प्रस्ताव के अन्य हिस्से अभी भी विकास में हैं और महत्वपूर्ण संशोधन के अधीन हैं।

Service Lookup (प्रकार 9 और 11) कम-प्राथमिकता और अनिर्धारित हैं, और इन्हें एक अलग प्रस्ताव में विभाजित किया जा सकता है।

## अवलोकन

यह निम्नलिखित 4 प्रस्तावों का अपडेट और एकत्रीकरण है:

- 110 LS2
- 120 बड़े पैमाने पर multihoming के लिए Meta LS2
- 121 एन्क्रिप्टेड LS2
- 122 अप्रमाणित सेवा खोज (anycasting)

ये प्रस्ताव मुख्यतः स्वतंत्र हैं, लेकिन समझदारी के लिए हम इनमें से कई के लिए एक सामान्य प्रारूप को परिभाषित और उपयोग करते हैं।

निम्नलिखित प्रस्ताव कुछ हद तक संबंधित हैं:

- 140 Invisible Multihoming (इस प्रस्ताव के साथ असंगत)
- 142 New Crypto Template (नए symmetric crypto के लिए)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## प्रस्ताव

यह प्रस्ताव 5 नए DatabaseEntry प्रकारों को परिभाषित करता है और उन्हें network database में store करने और retrieve करने की प्रक्रिया के साथ-साथ उन्हें sign करने और उन signatures को verify करने की विधि को भी परिभाषित करता है।

### Goals

- पीछे की ओर संगत (Backwards compatible)
- LS2 पुराने स्टाइल के mulithoming के साथ उपयोगी
- समर्थन के लिए कोई नई crypto या primitives की आवश्यकता नहीं
- crypto और signing के decoupling को बनाए रखें; सभी वर्तमान और भविष्य के संस्करणों का समर्थन करें
- वैकल्पिक offline signing keys को सक्षम करें
- fingerprinting को कम करने के लिए timestamps की सटीकता कम करें
- destinations के लिए नई crypto को सक्षम करें
- बड़े पैमाने पर multihoming को सक्षम करें
- मौजूदा encrypted LS के साथ कई समस्याओं को ठीक करें
- floodfills द्वारा दृश्यता कम करने के लिए वैकल्पिक blinding
- Encrypted एकल-कुंजी और कई revocable keys दोनों का समर्थन करता है
- outproxies की आसान lookup के लिए Service lookup, application DHT bootstrap,
  और अन्य उपयोग
- 32-byte binary destination hashes पर निर्भर किसी भी चीज़ को तोड़ें नहीं, जैसे bittorrent
- leasesets में properties के माध्यम से लचीलापन जोड़ें, जैसा कि हमारे पास routerinfos में है।
- header में published timestamp और variable expiration डालें, ताकि यह तब भी काम करे
  जब contents encrypted हों (earliest lease से timestamp derive न करें)
- सभी नए प्रकार उसी DHT space और उसी स्थानों पर रहते हैं जहाँ मौजूदा leasesets हैं,
  ताकि उपयोगकर्ता पुराने LS से LS2 में migrate कर सकें,
  या LS2, Meta, और Encrypted के बीच बदलाव कर सकें,
  Destination या hash को बदले बिना।
- एक मौजूदा Destination को offline keys का उपयोग करने के लिए परिवर्तित किया जा सकता है,
  या वापस online keys पर, Destination या hash को बदले बिना।

### Non-Goals / Out-of-scope

- नया DHT rotation algorithm या shared random generation
- विशिष्ट नया encryption type और end-to-end encryption scheme
  उस नए type का उपयोग करने के लिए एक अलग proposal में होगा।
  यहाँ कोई नया crypto निर्दिष्ट या चर्चित नहीं है।
- RIs या tunnel building के लिए नया encryption।
  यह एक अलग proposal में होगा।
- I2NP DLM / DSM / DSRM messages के encryption, transmission, और reception के तरीके।
  बदला नहीं जा रहा।
- Meta generate और support कैसे करें, जिसमें backend inter-router communication, management, failover, और coordination शामिल है।
  Support को I2CP, या i2pcontrol, या एक नए protocol में जोड़ा जा सकता है।
  यह standardized हो भी सकता है और नहीं भी।
- वास्तव में longer-expiring tunnels को कैसे implement और manage करें, या मौजूदा tunnels को cancel करें।
  यह अत्यंत कठिन है, और इसके बिना, आप reasonable graceful shutdown नहीं कर सकते।
- Threat model परिवर्तन
- Offline storage format, या data को store/retrieve/share करने के तरीके।
- Implementation details यहाँ चर्चित नहीं हैं और प्रत्येक project पर छोड़े गए हैं।

### Justification

LS2 encryption प्रकार बदलने और भविष्य के protocol परिवर्तनों के लिए fields जोड़ता है।

Encrypted LS2 मौजूदा encrypted LS की कई सुरक्षा समस्याओं को ठीक करता है, leases के संपूर्ण सेट के asymmetric encryption का उपयोग करके।

Meta LS2 लचीला, कुशल, प्रभावी, और बड़े पैमाने पर multihoming प्रदान करता है।

Service Record और Service List anycast सेवाएं प्रदान करते हैं जैसे कि naming lookup और DHT bootstrapping।

### लक्ष्य

I2NP Database Lookup/Store Messages में type numbers का उपयोग किया जाता है।

end-to-end कॉलम इस बात को दर्शाता है कि क्या queries/responses को Garlic Message में किसी Destination को भेजा जाता है।

मौजूदा प्रकार:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
नए प्रकार:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### गैर-लक्ष्य / कार्यक्षेत्र से बाहर

- लुकअप प्रकार वर्तमान में Database Lookup Message में bits 3-2 हैं।
  किसी भी अतिरिक्त प्रकार के लिए bit 4 के उपयोग की आवश्यकता होगी।

- सभी store types विषम हैं क्योंकि Database Store Message type field के upper bits को पुराने routers द्वारा नजरअंदाज कर दिया जाता है।
  हम चाहते हैं कि parse compressed RI के बजाय LS के रूप में fail हो।

- क्या signature द्वारा कवर किए गए data में type explicit होना चाहिए या implicit या कोई भी नहीं?

### औचित्य

प्रकार 3, 5, और 7 एक मानक leaseset lookup (प्रकार 1) के जवाब में वापस किए जा सकते हैं। प्रकार 9 कभी भी lookup के जवाब में वापस नहीं किया जाता। प्रकार 11 एक नए service lookup प्रकार (प्रकार 11) के जवाब में वापस किया जाता है।

केवल type 3 को client-to-client Garlic message में भेजा जा सकता है।

### NetDB डेटा प्रकार

टाइप 3, 7, और 9 सभी का एक समान फॉर्मेट है::

मानक LS2 हेडर - जैसा कि नीचे परिभाषित है

टाइप-विशिष्ट भाग   - जैसा कि नीचे प्रत्येक भाग में परिभाषित किया गया है

मानक LS2 हस्ताक्षर: - signing key के sig type द्वारा निहित लंबाई के अनुसार

टाइप 5 (एन्क्रिप्टेड) Destination के साथ शुरू नहीं होता और इसका अलग फॉर्मेट होता है। नीचे देखें।

टाइप 11 (Service List) कई Service Records का एक संग्रह है और इसका एक अलग प्रारूप है। नीचे देखें।

### नोट्स

TBD

## Standard LS2 Header

टाइप 3, 7, और 9 मानक LS2 हेडर का उपयोग करते हैं, जो नीचे निर्दिष्ट है:

### लुकअप/स्टोर प्रक्रिया

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
### प्रारूप

- Unpublished/published: जब database store को end-to-end भेजते समय उपयोग के लिए,
  भेजने वाला router यह संकेत देना चाह सकता है कि इस leaseset को
  दूसरों को नहीं भेजा जाना चाहिए। हम वर्तमान में इस स्थिति को बनाए रखने के लिए heuristics का उपयोग करते हैं।

- Published: leaseset के 'version' को निर्धारित करने के लिए आवश्यक जटिल तर्क को बदल देता है। वर्तमान में, version अंतिम-समाप्त होने वाले lease की समाप्ति तिथि है, और एक publishing router को उस समाप्ति तिथि को कम से कम 1ms से बढ़ाना होगा जब वह एक leaseset प्रकाशित करता है जो केवल एक पुराने lease को हटाता है।

- Expires: एक netdb entry की expiration को उसके last-expiring leaseset से पहले होने की अनुमति देता है। LS2 के लिए उपयोगी नहीं हो सकता, जहाँ leasesets के 11-मिनट के अधिकतम expiration के साथ रहने की अपेक्षा की जाती है, लेकिन अन्य नए प्रकारों के लिए यह आवश्यक है (नीचे Meta LS और Service Record देखें)।

- ऑफलाइन keys वैकल्पिक हैं, प्रारंभिक/आवश्यक implementation की जटिलता को कम करने के लिए।

### गोपनीयता/सुरक्षा संबंधी विचारणाएं

- टाइमस्टैम्प की सटीकता को और भी कम किया जा सकता है (10 मिनट?) लेकिन version number जोड़ना होगा। यह multihoming को तोड़ सकता है, जब तक कि हमारे पास order preserving encryption न हो? शायद टाइमस्टैम्प के बिना बिल्कुल काम नहीं चल सकता।

- वैकल्पिक: 3 बाइट timestamp (epoch / 10 मिनट), 1-बाइट version, 2-बाइट expires

- क्या डेटा / signature में type explicit या implicit है? signature के लिए "Domain" constants?

### Notes

- राउटर्स को एक सेकंड में एक से अधिक बार LS प्रकाशित नहीं करना चाहिए।
  यदि वे ऐसा करते हैं, तो उन्हें पहले प्रकाशित LS की तुलना में प्रकाशित टाइमस्टैम्प को कृत्रिम रूप से 1 से बढ़ाना चाहिए।

- Router implementations transient keys और signature को cache कर सकते हैं ताकि
  हर बार verification से बचा जा सके। विशेष रूप से, floodfills, और
  long-lived connections के दोनों ends पर स्थित routers को इससे फायदा हो सकता है।

- ऑफलाइन keys और signature केवल लंबे समय तक चलने वाले destinations के लिए उपयुक्त हैं,
  यानी servers के लिए, clients के लिए नहीं।

## New DatabaseEntry types

### फॉर्मेट

मौजूदा LeaseSet से परिवर्तन:

- प्रकाशित टाइमस्टैम्प, समाप्ति टाइमस्टैम्प, फ्लैग्स, और प्रॉपर्टीज जोड़ें
- एन्क्रिप्शन प्रकार जोड़ें
- रिवोकेशन की हटाएं

के साथ खोजें

    Standard LS flag (1)
Store के साथ

    Standard LS2 type (3)
पर संग्रहीत करें

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
विशिष्ट समाप्ति

    10 minutes, as in a regular LS.
प्रकाशित करता:

    Destination

### औचित्य

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
### समस्याएं

- Properties: भविष्य के विस्तार और लचीलेपन के लिए।
  शेष डेटा के parsing के लिए आवश्यक होने की स्थिति में पहले रखा गया है।

- कई एन्क्रिप्शन प्रकार/पब्लिक की जोड़े नए एन्क्रिप्शन प्रकारों में
  संक्रमण को आसान बनाने के लिए हैं। इसे करने का दूसरा तरीका
  कई leasesets प्रकाशित करना है, संभवतः समान tunnels का उपयोग करते हुए,
  जैसा कि हम अब DSA और EdDSA destinations के लिए करते हैं।
  एक tunnel पर आने वाले एन्क्रिप्शन प्रकार की पहचान
  मौजूदा session tag तंत्र के साथ की जा सकती है,
  और/या प्रत्येक की का उपयोग करके trial decryption से। आने वाले
  संदेशों की लंबाई भी एक संकेत प्रदान कर सकती है।

### नोट्स

यह proposal leaseset में public key का उपयोग end-to-end encryption key के लिए जारी रखता है, और Destination में public key field को अप्रयुक्त छोड़ देता है, जैसा कि अभी है। Destination key certificate में encryption type निर्दिष्ट नहीं है, यह 0 ही रहेगा।

एक अस्वीकृत विकल्प यह है कि Destination key certificate में encryption type निर्दिष्ट करें, Destination में public key का उपयोग करें, और leaseset में public key का उपयोग न करें। हमारी इसे करने की कोई योजना नहीं है।

LS2 के फायदे:

- वास्तविक पब्लिक key का स्थान नहीं बदलता।
- Encryption प्रकार, या पब्लिक key, Destination को बदले बिना बदल सकती है।
- अप्रयुक्त revocation फील्ड को हटाता है
- इस proposal में अन्य DatabaseEntry प्रकारों के साथ बुनियादी संगतता
- कई encryption प्रकारों की अनुमति देता है

LS2 की कमियां:

- RouterInfo से public key और encryption type का स्थान अलग है
- leaseset में अप्रयुक्त public key को बनाए रखता है
- नेटवर्क भर में implementation की आवश्यकता है; वैकल्पिक रूप से, experimental
  encryption types का उपयोग किया जा सकता है, यदि floodfills द्वारा अनुमति दी गई हो
  (लेकिन experimental sig types के समर्थन के बारे में संबंधित proposals 136 और 137 देखें)।
  वैकल्पिक proposal को experimental encryption types के लिए implement और test करना आसान हो सकता है।

### New Encryption Issues

इसमें से कुछ इस proposal के scope से बाहर है, लेकिन अभी के लिए यहाँ notes रख रहे हैं क्योंकि हमारे पास अभी तक अलग से कोई encryption proposal नहीं है। ECIES proposals 144 और 145 भी देखें।

- एन्क्रिप्शन प्रकार curve, key length, और end-to-end scheme के संयोजन को दर्शाता है,
  जिसमें KDF और MAC भी शामिल हैं, यदि कोई हो।

- हमने एक key length फ़ील्ड शामिल किया है, ताकि LS2 को
  floodfill द्वारा अज्ञात encryption प्रकारों के लिए भी parsable और verifiable बनाया जा सके।

- पहला नया encryption type जो प्रस्तावित किया जाएगा
  शायद ECIES/X25519 होगा। यह end-to-end कैसे उपयोग किया जाएगा
  (या तो ElGamal/AES+SessionTag का थोड़ा संशोधित संस्करण
  या कुछ पूरी तरह नया, जैसे ChaCha/Poly) इसे एक या अधिक
  अलग proposals में निर्दिष्ट किया जाएगा।
  ECIES proposals 144 और 145 भी देखें।

### LeaseSet 2

- लीज़ में 8-बाइट एक्सपायरेशन को 4 बाइट्स में बदल दिया गया।

- यदि हमें कभी revocation implement करना पड़े, तो हम इसे शून्य expires field के साथ,
  या शून्य leases के साथ, या दोनों के साथ कर सकते हैं। अलग revocation key की कोई आवश्यकता नहीं।

- Encryption keys सर्वर की प्राथमिकता के क्रम में हैं, सबसे पसंदीदा पहले।
  Default client व्यवहार पहली key का चयन करना है जिसमें
  समर्थित encryption प्रकार हो। Clients अन्य चयन algorithms का उपयोग कर सकते हैं
  encryption समर्थन, सापेक्ष प्रदर्शन, और अन्य कारकों के आधार पर।

### प्रारूप

लक्ष्य:

- ब्लाइंडिंग जोड़ें
- कई sig प्रकारों की अनुमति दें
- किसी नए crypto primitives की आवश्यकता न हो
- वैकल्पिक रूप से प्रत्येक प्राप्तकर्ता के लिए एन्क्रिप्ट करें, रद्द करने योग्य
- केवल Standard LS2 और Meta LS2 के एन्क्रिप्शन का समर्थन करें

एन्क्रिप्टेड LS2 कभी भी end-to-end garlic message में नहीं भेजा जाता है। ऊपर दिए गए मानक LS2 का उपयोग करें।

मौजूदा encrypted LeaseSet से बदलाव:

- सुरक्षा के लिए पूरी चीज़ को encrypt करें
- सुरक्षित रूप से encrypt करें, केवल AES के साथ नहीं।
- प्रत्येक प्राप्तकर्ता के लिए encrypt करें

के साथ खोज

    Standard LS flag (1)
के साथ स्टोर करें

    Encrypted LS2 type (5)
पर स्टोर करें

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
सामान्य समाप्ति

    10 minutes, as in a regular LS, or hours, as in a meta LS.
द्वारा प्रकाशित

    Destination


### औचित्य

हम encrypted LS2 के लिए उपयोग किए जाने वाले cryptographic building blocks के अनुरूप निम्नलिखित functions को परिभाषित करते हैं:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### चर्चा

एन्क्रिप्टेड LS2 फॉर्मेट तीन नेस्टेड लेयर्स से मिलकर बना है:

- एक बाहरी परत जिसमें स्टोरेज और पुनर्प्राप्ति के लिए आवश्यक plaintext जानकारी होती है।
- एक मध्य परत जो क्लाइंट प्रमाणीकरण को संभालती है।
- एक आंतरिक परत जिसमें वास्तविक LS2 डेटा होता है।

समग्र प्रारूप इस प्रकार दिखता है::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

नोट करें कि encrypted LS2 blinded है। Destination header में नहीं है। DHT storage location SHA-256(sig type || blinded public key) है, और daily rotate होता है।

उपरोक्त निर्दिष्ट मानक LS2 header का उपयोग नहीं करता है।

#### Layer 0 (outer)

प्रकार

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

ब्लाइंडेड पब्लिक की सिग टाइप

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

ब्लाइंडेड पब्लिक की (Blinded Public Key)

    Length as implied by sig type

प्रकाशन टाइमस्टैम्प

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

समाप्ति

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

फ्लैग्स

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

क्षणिक कुंजी डेटा

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


#### Layer 1 (middle)

फ्लैग्स

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


#### Layer 2 (inner)

प्रकार

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

डेटा

    LeaseSet2 data for the given type.

    Includes the header and signature.


### नए एन्क्रिप्शन मुद्दे

हम key blinding के लिए निम्नलिखित scheme का उपयोग करते हैं, जो Ed25519 और [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) पर आधारित है। Re25519 signatures Ed25519 curve पर होते हैं, hash के लिए SHA-512 का उपयोग करके।

हम [Tor के rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3) का उपयोग नहीं करते हैं, जिसके समान डिज़ाइन लक्ष्य हैं, क्योंकि इसकी blinded public keys prime-order subgroup से बाहर हो सकती हैं, जिसके अज्ञात सुरक्षा निहितार्थ हैं।

#### Goals

- अनब्लाइंडेड destination में signing public key Ed25519 (sig type 7) या Red25519 (sig type 11) होनी चाहिए; 
  कोई अन्य sig types समर्थित नहीं हैं
- यदि signing public key ऑफलाइन है, तो transient signing public key भी Ed25519 होनी चाहिए
- Blinding कम्प्यूटेशनली सरल है
- मौजूदा cryptographic primitives का उपयोग करें
- Blinded public keys को unblind नहीं किया जा सकता
- Blinded public keys Ed25519 curve और prime-order subgroup पर होनी चाहिए
- Blinded public key प्राप्त करने के लिए destination की signing public key 
  (पूरा destination आवश्यक नहीं) जानना आवश्यक है
- वैकल्पिक रूप से blinded public key प्राप्त करने के लिए अतिरिक्त secret की व्यवस्था करें

#### Security

blinding scheme की सुरक्षा के लिए यह आवश्यक है कि alpha का distribution unblinded private keys के समान हो। हालांकि, जब हम Ed25519 private key (sig type 7) को Red25519 private key (sig type 11) में blind करते हैं, तो distribution अलग होता है। [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) की आवश्यकताओं को पूरा करने के लिए, Red25519 (sig type 11) का उपयोग unblinded keys के लिए भी किया जाना चाहिए, ताकि "re-randomized public key और उस key के under signature(s) का combination उस key को reveal न करे जिससे इसे re-randomize किया गया था।" हम मौजूदा destinations के लिए type 7 की अनुमति देते हैं, लेकिन नए destinations के लिए type 11 की सिफारिश करते हैं जो encrypted होंगे।

#### Definitions

ब

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

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


#### Blinding Calculations

प्रत्येक दिन (UTC) एक नया secret alpha और blinded keys जेनरेट करना होगा। secret alpha और blinded keys की गणना निम्नलिखित प्रकार से की जाती है।

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
BLIND_PUBKEY(), clients के लिए जो leaseset retrieve कर रहे हैं:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
दोनों विधियों से A' की गणना करने पर समान परिणाम प्राप्त होता है, जैसा कि आवश्यक है।

#### Signing

unblinded leaseset को unblinded Ed25519 या Red25519 signing private key द्वारा हस्ताक्षरित किया जाता है और unblinded Ed25519 या Red25519 signing public key (sig types 7 या 11) के साथ सामान्य रूप से सत्यापित किया जाता है।

यदि signing public key offline है, तो unblinded leaseset को unblinded transient Ed25519 या Red25519 signing private key द्वारा sign किया जाता है और unblinded Ed25519 या Red25519 transient signing public key (sig types 7 या 11) के साथ सामान्य रूप से verify किया जाता है। encrypted leasesets के लिए offline keys पर अतिरिक्त नोट्स के लिए नीचे देखें।

एन्क्रिप्टेड leaseset की signing के लिए, हम Red25519 का उपयोग करते हैं, जो [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) पर आधारित है और blinded keys के साथ sign और verify करने के लिए उपयोग होता है। Red25519 signatures Ed25519 curve पर होते हैं, hash के लिए SHA-512 का उपयोग करते हुए।

Red25519 मानक Ed25519 के समान है सिवाय नीचे निर्दिष्ट के अतिरिक्त।

#### Sign/Verify Calculations

एन्क्रिप्टेड leaseset का बाहरी भाग Red25519 keys और signatures का उपयोग करता है।

Red25519 Ed25519 के लगभग समान है। इसमें दो अंतर हैं:

Red25519 private keys यादृच्छिक संख्याओं से उत्पन्न की जाती हैं और फिर उन्हें mod L द्वारा कम किया जाना चाहिए, जहां L ऊपर परिभाषित है। Ed25519 private keys यादृच्छिक संख्याओं से उत्पन्न की जाती हैं और फिर bytes 0 और 31 के लिए bitwise masking का उपयोग करके "clamped" की जाती हैं। यह Red25519 के लिए नहीं किया जाता है। ऊपर परिभाषित functions GENERATE_ALPHA() और BLIND_PRIVKEY() mod L का उपयोग करके उचित Red25519 private keys उत्पन्न करते हैं।

Red25519 में, signing के लिए r की गणना अतिरिक्त random data का उपयोग करती है, और private key के hash के बजाय public key value का उपयोग करती है। Random data के कारण, प्रत्येक Red25519 signature अलग होता है, भले ही same data को same key के साथ sign किया जा रहा हो।

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
### नोट्स

#### Derivation of subcredentials

ब्लाइंडिंग प्रक्रिया के हिस्से के रूप में, हमें यह सुनिश्चित करना होगा कि एक एन्क्रिप्टेड LS2 को केवल वही व्यक्ति डिक्रिप्ट कर सकता है जो संबंधित Destination की साइनिंग public key जानता है। पूरी Destination की आवश्यकता नहीं है। इसे प्राप्त करने के लिए, हम साइनिंग public key से एक credential प्राप्त करते हैं:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
व्यक्तिगतकरण स्ट्रिंग यह सुनिश्चित करती है कि credential किसी भी hash के साथ टकराव न करे जो DHT lookup key के रूप में उपयोग किया जाता है, जैसे कि plain Destination hash।

दिए गए blinded key के लिए, हम फिर एक subcredential derive कर सकते हैं:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
subcredential को नीचे दी गई key derivation प्रक्रियाओं में शामिल किया जाता है, जो उन keys को Destination की signing public key के ज्ञान के साथ bind करता है।

#### Layer 1 encryption

सबसे पहले, key derivation प्रक्रिया के लिए input तैयार किया जाता है:

```text
outerInput = subcredential || publishedTimestamp
```
अगला, एक यादृच्छिक salt उत्पन्न किया जाता है:

```text
outerSalt = CSRNG(32)
```
तब layer 1 को encrypt करने के लिए उपयोग की जाने वाली key derive की जाती है:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
अंत में, layer 1 plaintext को encrypted और serialized किया जाता है:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

नमक (salt) को layer 1 ciphertext से parse किया जाता है:

```text
outerSalt = outerCiphertext[0:31]
```
तब layer 1 को encrypt करने के लिए उपयोग की जाने वाली key derive की जाती है:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
अंततः, layer 1 ciphertext को decrypt किया जाता है:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

जब client authorization सक्षम होता है, तो ``authCookie`` की गणना नीचे वर्णित तरीके से की जाती है। जब client authorization अक्षम होता है, तो ``authCookie`` शून्य-लंबाई का byte array होता है।

एन्क्रिप्शन layer 1 के समान तरीके से आगे बढ़ता है:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

जब client authorization सक्षम होता है, तो ``authCookie`` की गणना नीचे वर्णित तरीके से की जाती है। जब client authorization अक्षम होता है, तो ``authCookie`` शून्य-लंबाई वाला byte array होता है।

डिक्रिप्शन layer 1 के समान तरीके से आगे बढ़ता है:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### एन्क्रिप्टेड LS2

जब किसी Destination के लिए client authorization सक्षम किया जाता है, तो server उन clients की एक सूची बनाए रखता है जिन्हें वे encrypted LS2 डेटा को decrypt करने के लिए अधिकृत कर रहे हैं। प्रति-client संग्रहीत डेटा authorization mechanism पर निर्भर करता है, और इसमें किसी न किसी रूप की key material शामिल होती है जो प्रत्येक client generate करता है और एक secure out-of-band mechanism के माध्यम से server को भेजता है।

प्रति-क्लाइंट प्राधिकरण लागू करने के लिए दो विकल्प हैं:

#### DH client authorization

प्रत्येक client एक DH keypair ``[csk_i, cpk_i]`` generate करता है, और public key ``cpk_i`` को server को भेजता है।

सर्वर प्रोसेसिंग
^^^^^^^^^^^^^^^^^

सर्वर एक नया ``authCookie`` और एक ephemeral DH keypair जेनरेट करता है:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
फिर प्रत्येक अधिकृत client के लिए, server अपनी public key के लिए ``authCookie`` को encrypt करता है:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
सर्वर प्रत्येक ``[clientID_i, clientCookie_i]`` tuple को encrypted LS2 की layer 1 में ``epk`` के साथ रखता है।

क्लाइंट प्रोसेसिंग
^^^^^^^^^^^^^^^^^

क्लाइंट अपनी private key का उपयोग करके अपना अपेक्षित client identifier ``clientID_i``, encryption key ``clientKey_i``, और encryption IV ``clientIV_i`` derive करता है:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
फिर client layer 1 authorization data में एक entry की खोज करता है जिसमें ``clientID_i`` हो। यदि कोई matching entry मौजूद है, तो client उसे decrypt करता है ``authCookie`` प्राप्त करने के लिए:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

प्रत्येक client एक गुप्त 32-byte key ``psk_i`` generate करता है, और इसे server को भेजता है। वैकल्पिक रूप से, server गुप्त key generate कर सकता है, और इसे एक या अधिक clients को भेज सकता है।

सर्वर प्रोसेसिंग ^^^^^^^^^^^^^^^^^^ सर्वर एक नया ``authCookie`` और salt उत्पन्न करता है:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
फिर प्रत्येक अधिकृत client के लिए, server ``authCookie`` को अपनी pre-shared key से encrypt करता है:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
सर्वर प्रत्येक ``[clientID_i, clientCookie_i]`` tuple को encrypted LS2 की layer 1 में ``authSalt`` के साथ रखता है।

क्लाइंट प्रोसेसिंग
^^^^^^^^^^^^^^^^^

क्लाइंट अपनी pre-shared key का उपयोग करके अपना अपेक्षित client identifier ``clientID_i``, encryption key ``clientKey_i``, और encryption IV ``clientIV_i`` derive करता है:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
फिर client layer 1 authorization data में एक entry की खोज करता है जिसमें ``clientID_i`` हो। यदि कोई matching entry मौजूद है, तो client इसे decrypt करके ``authCookie`` प्राप्त करता है:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

उपरोक्त दोनों client authorization तंत्र client membership के लिए गोपनीयता प्रदान करते हैं। एक entity जो केवल Destination को जानती है, वह देख सकती है कि किसी भी समय कितने clients subscribed हैं, लेकिन यह track नहीं कर सकती कि कौन से clients को add या revoke किया जा रहा है।

सर्वर को प्रत्येक बार encrypted LS2 generate करते समय clients के क्रम को randomize करना चाहिए, ताकि clients को list में अपनी स्थिति पता न चले और वे यह अनुमान न लगा सकें कि अन्य clients को कब add या revoke किया गया है।

एक server क्लाइंट्स की संख्या को छुपाने के लिए authorization data की सूची में random entries डालकर subscribed क्लाइंट्स की संख्या को छुपाने का विकल्प चुन सकता है।

DH client authorization के फायदे ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- इस स्कीम की सुरक्षा पूरी तरह से client key material के out-of-band exchange पर निर्भर नहीं है। Client की private key को कभी भी उनके device से बाहर जाने की आवश्यकता नहीं होती, और इसलिए एक adversary जो out-of-band exchange को intercept करने में सक्षम है, लेकिन DH algorithm को तोड़ नहीं सकता, वह encrypted LS2 को decrypt नहीं कर सकता, या यह निर्धारित नहीं कर सकता कि client को कितने समय तक access दिया गया है।

DH client authorization के नुकसान
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- N clients के लिए server side पर N + 1 DH operations की आवश्यकता होती है।
- Client side पर एक DH operation की आवश्यकता होती है।
- Client को secret key generate करने की आवश्यकता होती है।

PSK क्लाइंट प्राधिकरण के फायदे
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- किसी DH ऑपरेशन की आवश्यकता नहीं होती।
- सर्वर को गुप्त कुंजी उत्पन्न करने की अनुमति देता है।
- यदि चाहें तो सर्वर को कई क्लाइंट्स के साथ एक ही कुंजी साझा करने की अनुमति देता है।

PSK client authorization के नुकसान ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- इस स्कीम की सुरक्षा मुख्य रूप से client key material के out-of-band exchange पर निर्भर करती है। यदि कोई adversary किसी विशेष client के लिए इस exchange को intercept कर लेता है, तो वे उस client के लिए authorized किसी भी subsequent encrypted LS2 को decrypt कर सकते हैं, साथ ही यह भी पता लगा सकते हैं कि client का access कब revoke किया गया है।

### परिभाषाएं

प्रस्ताव 149 देखें।

आप bittorrent के लिए encrypted LS2 का उपयोग नहीं कर सकते, क्योंकि compact announce replies 32 bytes के होते हैं। इन 32 bytes में केवल hash होता है। यहाँ इस बात का संकेत देने के लिए कोई जगह नहीं है कि leaseset encrypted है, या signature types क्या हैं।

### प्रारूप

एन्क्रिप्टेड leaseSet के लिए offline keys के साथ, blinded private keys भी offline generate करनी होंगी, प्रत्येक दिन के लिए एक।

जैसा कि वैकल्पिक ऑफलाइन signature block एन्क्रिप्टेड leaseset के cleartext भाग में है, floodfills को scrape करने वाला कोई भी व्यक्ति इसका उपयोग करके leaseset को कई दिनों तक ट्रैक कर सकता है (लेकिन इसे decrypt नहीं कर सकता)। इसे रोकने के लिए, keys के मालिक को प्रत्येक दिन के लिए नई transient keys भी generate करनी चाहिए। Transient और blinded दोनों keys को पहले से generate किया जा सकता है, और उन्हें batch में router को deliver किया जा सकता है।

इस प्रस्ताव में कई transient और blinded keys को पैकेज करने और उन्हें client या router को प्रदान करने के लिए कोई file format परिभाषित नहीं है। इस प्रस्ताव में offline keys के साथ encrypted leasesets का समर्थन करने के लिए कोई I2CP प्रोटोकॉल संवर्धन परिभाषित नहीं है।

### Notes

- एक service जो encrypted leasesets का उपयोग करती है, वह encrypted version को floodfills पर publish करेगी। हालांकि, दक्षता के लिए, यह authenticated होने के बाद (उदाहरण के लिए whitelist के माध्यम से) clients को wrapped garlic message में unencrypted leasesets भेजेगी।

- Floodfills दुरुपयोग को रोकने के लिए अधिकतम आकार को एक उचित मान तक सीमित कर सकते हैं।

- डिक्रिप्शन के बाद, कई जांच की जानी चाहिए, जिसमें यह शामिल है कि
  भीतरी timestamp और expiration टॉप लेवल पर दिए गए से मेल खाते हैं।

- ChaCha20 को AES के बजाय चुना गया था। जबकि यदि AES हार्डवेयर समर्थन उपलब्ध है तो गति समान होती है, ChaCha20 तब 2.5-3x तेज़ होता है जब AES हार्डवेयर समर्थन उपलब्ध नहीं होता, जैसे कि निम्न-स्तरीय ARM डिवाइसों पर।

- हम गति के बारे में इतनी चिंता नहीं करते कि keyed BLAKE2b का उपयोग करें। इसका output
  size काफी बड़ा है जो हमारे लिए आवश्यक सबसे बड़े n को समायोजित कर सके (या हम इसे counter argument के साथ प्रत्येक
  वांछित key के लिए एक बार call कर सकते हैं)। BLAKE2b, SHA-256 से काफी तेज़ है, और
  keyed-BLAKE2b hash function calls की कुल संख्या को कम कर देगा।
  हालांकि, proposal 148 देखें, जहाँ यह प्रस्तावित है कि हम अन्य कारणों से BLAKE2b पर switch करें।
  देखें [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html)।

### Meta LS2

यह multihoming को बदलने के लिए उपयोग किया जाता है। किसी भी leaseset की तरह, यह निर्माता द्वारा हस्ताक्षरित होता है। यह destination hashes की एक प्रमाणित सूची है।

Meta LS2 एक ट्री स्ट्रक्चर का शीर्ष, और संभावित रूप से मध्यवर्ती नोड्स है। इसमें कई entries होती हैं, जिनमें से प्रत्येक एक LS, LS2, या किसी अन्य Meta LS2 की ओर इशारा करती है ताकि बड़े पैमाने पर multihoming का समर्थन किया जा सके। एक Meta LS2 में LS, LS2, और Meta LS2 entries का मिश्रण हो सकता है। ट्री की leaves हमेशा एक LS या LS2 होती हैं। यह ट्री एक DAG है; loops प्रतिबंधित हैं; lookups करने वाले clients को loops का पता लगाना और उनका पालन करने से इनकार करना चाहिए।

एक Meta LS2 की अवधि एक मानक LS या LS2 की तुलना में बहुत अधिक हो सकती है। शीर्ष स्तर की अवधि प्रकाशन तारीख के कई घंटे बाद हो सकती है। अधिकतम अवधि समय को floodfills और clients द्वारा लागू किया जाएगा, और यह TBD है।

Meta LS2 का उपयोग मामला बड़े पैमाने पर multihoming है, लेकिन routers से leasesets के correlation के लिए (router restart के समय पर) उससे अधिक सुरक्षा नहीं है जो अभी LS या LS2 के साथ प्रदान की जाती है। यह "facebook" उपयोग मामले के बराबर है, जिसे शायद correlation protection की आवश्यकता नहीं है। इस उपयोग मामले को शायद offline keys की आवश्यकता है, जो tree के प्रत्येक node पर standard header में प्रदान की जाती हैं।

leaf routers, intermediate और master Meta LS signers के बीच समन्वय के लिए back-end protocol यहाँ निर्दिष्ट नहीं है। आवश्यकताएं अत्यंत सरल हैं - बस यह सत्यापित करना कि peer चालू है, और हर कुछ घंटों में एक नया LS प्रकाशित करना। एकमात्र जटिलता failure पर top-level या intermediate-level Meta LSes के लिए नए publishers चुनने की है।

मिक्स-और-मैच leasesets जहाँ कई routers से leases को मिलाया, साइन किया, और एक ही leaseset में प्रकाशित किया जाता है, इसे proposal 140, "invisible multihoming" में प्रलेखित किया गया है। यह proposal जैसा लिखा गया है वैसा अव्यावहारिक है, क्योंकि streaming connections एक ही router के साथ "sticky" नहीं रह पाएंगे, देखें http://zzz.i2p/topics/2335 ।

बैक-एंड प्रोटोकॉल, और router तथा client internals के साथ इंटरैक्शन, invisible multihoming के लिए काफी जटिल होगा।

टॉप-लेवल Meta LS के लिए floodfill को अधिक लोड से बचने के लिए, expiration कम से कम कई घंटे होनी चाहिए। Clients को टॉप-लेवल Meta LS को cache करना चाहिए, और यदि unexpired है तो इसे restarts में भी बनाए रखना चाहिए।

हमें clients के लिए tree को traverse करने हेतु कुछ algorithm define करना होगा, जिसमें fallbacks भी शामिल हों, ताकि usage dispersed हो सके। यह hash distance, cost, और randomness का कुछ function होगा। यदि किसी node के पास LS या LS2 और Meta LS दोनों हैं, तो हमें यह जानना होगा कि कब उन leasesets का उपयोग करना allowed है, और कब tree को traverse करना जारी रखना है।

के साथ खोजें

    Standard LS flag (1)
के साथ स्टोर करें

    Meta LS2 type (7)
पर संग्रहीत करें

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
सामान्य समाप्ति

    Hours. Max 18.2 hours (65535 seconds)
द्वारा प्रकाशित

    "master" Destination or coordinator, or intermediate coordinators

### Format

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
फ्लैग्स और properties: भविष्य के उपयोग के लिए

### ब्लाइंडिंग Key व्युत्पादन

- इस का उपयोग करने वाली एक distributed service में service destination की private key के साथ एक या अधिक "masters" होंगे। वे (out of band) सक्रिय destinations की वर्तमान सूची निर्धारित करेंगे और Meta LS2 को publish करेंगे। redundancy के लिए, कई masters Meta LS2 को multihome (यानी समवर्ती रूप से publish) कर सकते हैं।

- एक distributed service एक single destination के साथ शुरू हो सकती है या old-style multihoming का उपयोग कर सकती है, फिर Meta LS2 में transition कर सकती है। एक standard LS lookup LS, LS2, या Meta LS2 में से कोई भी एक return कर सकता है।

- जब कोई सेवा Meta LS2 का उपयोग करती है, तो इसके पास कोई tunnels (leases) नहीं होते हैं।

### Service Record

यह एक व्यक्तिगत रिकॉर्ड है जो कहता है कि एक destination किसी सेवा में भाग ले रहा है। यह प्रतिभागी से floodfill को भेजा जाता है। यह कभी भी floodfill द्वारा व्यक्तिगत रूप से नहीं भेजा जाता, बल्कि केवल Service List के हिस्से के रूप में भेजा जाता है। Service Record का उपयोग किसी सेवा में भागीदारी रद्द करने के लिए भी किया जाता है, expiration को शून्य पर सेट करके।

यह एक LS2 नहीं है लेकिन यह मानक LS2 header और signature format का उपयोग करता है।

के साथ खोजें

    n/a, see Service List
के साथ स्टोर करें

    Service Record type (9)
पर स्टोर करें

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
सामान्य समाप्ति

    Hours. Max 18.2 hours (65535 seconds)
द्वारा प्रकाशित

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- यदि expires सभी शून्य है, तो floodfill को रिकॉर्ड को revoke करना चाहिए और अब इसे service list में शामिल नहीं करना चाहिए।

- Storage: Floodfill इन रिकॉर्ड्स के storage को सख्ती से throttle कर सकता है और
  प्रति hash संग्रहीत रिकॉर्ड्स की संख्या और उनकी expiration को सीमित कर सकता है। Hashes की
  एक whitelist का भी उपयोग किया जा सकता है।

- किसी भी अन्य netdb प्रकार का समान hash पर प्राथमिकता है, इसलिए एक service record कभी भी 
  LS/RI को overwrite नहीं कर सकता, लेकिन एक LS/RI उस hash पर सभी service records को overwrite कर देगा।

### Service List

यह LS2 जैसा बिल्कुल नहीं है और एक अलग format का उपयोग करता है।

सेवा सूची floodfill द्वारा बनाई और हस्ताक्षरित की जाती है। यह अप्रमाणित है क्योंकि कोई भी व्यक्ति floodfill पर Service Record प्रकाशित करके किसी सेवा में शामिल हो सकता है।

एक Service List में Short Service Records होते हैं, पूर्ण Service Records नहीं। इनमें signatures होते हैं लेकिन केवल hashes होते हैं, पूर्ण destinations नहीं, इसलिए इन्हें पूर्ण destination के बिना verify नहीं किया जा सकता।

सुरक्षा, यदि कोई हो, और service lists की वांछनीयता TBD है। Floodfills प्रकाशन और lookups को services की एक whitelist तक सीमित कर सकते हैं, लेकिन यह whitelist implementation या operator की प्राथमिकता के आधार पर भिन्न हो सकती है। implementations में एक सामान्य, आधारभूत whitelist पर सहमति प्राप्त करना संभव नहीं हो सकता।

यदि service name को उपरोक्त service record में शामिल किया गया है, तो floodfill operators आपत्ति कर सकते हैं; यदि केवल hash शामिल है, तो कोई verification नहीं है, और एक service record किसी भी अन्य netDb प्रकार से "आगे निकल" सकता है और floodfill में store हो सकता है।

के साथ खोजें

    Service List lookup type (11)
के साथ स्टोर करें

    Service List type (11)
पर संग्रहीत करें

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
सामान्य समाप्ति

    Hours, not specified in the list itself, up to local policy
प्रकाशित करने वाला

    Nobody, never sent to floodfill, never flooded.

### Format

उपरोक्त निर्दिष्ट मानक LS2 header का उपयोग नहीं करता।

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
सेवा सूची के हस्ताक्षर को सत्यापित करने के लिए:

- सेवा नाम के hash को prepend करें
- creator के hash को हटाएं
- संशोधित contents के signature की जांच करें

प्रत्येक Short Service Record के signature को verify करने के लिए:

- गंतव्य प्राप्त करें
- हस्ताक्षर की जांच करें (प्रकाशित समयमुद्रा + समाप्ति + फ्लैग्स + पोर्ट + सेवा नाम का Hash)

प्रत्येक Revocation Record के signature को verify करने के लिए:

- गंतव्य प्राप्त करें
- हस्ताक्षर की जांच करें (प्रकाशित टाइमस्टैम्प + 4 शून्य बाइट्स + flags + port + सेवा नाम का Hash)

### Notes

- हम sig type के बजाय signature length का उपयोग करते हैं ताकि हम अज्ञात signature types को support कर सकें।

- सेवा सूची की कोई समाप्ति नहीं होती, प्राप्तकर्ता अपनी नीति या व्यक्तिगत रिकॉर्ड की समाप्ति के आधार पर अपना निर्णय ले सकते हैं।

- Service Lists flood नहीं होती हैं, केवल individual Service Records होते हैं। प्रत्येक
  floodfill एक Service List बनाता, sign करता, और cache करता है। floodfill अपनी
  स्वयं की policy का उपयोग cache time और service तथा revocation
  records की अधिकतम संख्या के लिए करता है।

## Common Structures Spec Changes Required

### एन्क्रिप्शन और प्रोसेसिंग

इस प्रस्ताव के दायरे से बाहर। ECIES प्रस्ताव 144 और 145 में जोड़ें।

### New Intermediate Structures

Lease2, MetaLease, LeaseSet2Header, और OfflineSignature के लिए नई संरचनाएं जोड़ें। रिलीज़ 0.9.38 से प्रभावी।

### New NetDB Types

ऊपर से शामिल की गई प्रत्येक नई leaseset प्रकार के लिए structures जोड़ें। LeaseSet2, EncryptedLeaseSet, और MetaLeaseSet के लिए, release 0.9.38 से प्रभावी। Service Record और Service List के लिए, प्रारंभिक और अनिर्धारित।

### New Signature Type

RedDSA_SHA512_Ed25519 Type 11 जोड़ें। Public key 32 bytes है; private key 32 bytes है; hash 64 bytes है; signature 64 bytes है।

## Encryption Spec Changes Required

इस प्रस्ताव के दायरे से बाहर। प्रस्ताव 144 और 145 देखें।

## I2NP Changes Required

नोट जोड़ें: LS2 केवल न्यूनतम संस्करण वाले floodfills पर ही प्रकाशित किया जा सकता है।

### Database Lookup Message

सेवा सूची लुकअप प्रकार जोड़ें।

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### प्रत्येक-क्लाइंट प्राधिकरण

सभी नए store types जोड़ें।

### Changes

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
## I2CP Changes Required

### I2CP Options

नए विकल्प router-side पर व्याख्या किए जाते हैं, SessionConfig Mapping में भेजे जाते हैं:

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
नए विकल्प जो client-side पर व्याख्यायित किए जाते हैं:

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
### Session Config

ध्यान दें कि offline signatures के लिए, विकल्प i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, और i2cp.leaseSetOfflineSignature आवश्यक हैं, और signature transient signing private key द्वारा किया जाता है।

### एन्क्रिप्टेड LS के साथ Base 32 पते

Router से client तक। कोई बदलाव नहीं। Leases को 8-byte timestamps के साथ भेजा जाता है, भले ही returned leaseset एक LS2 हो जिसमें 4-byte timestamps हों। ध्यान दें कि response एक Create Leaseset या Create Leaseset2 Message हो सकती है।

### ऑफलाइन Keys के साथ Encrypted LS

Router से client को। कोई बदलाव नहीं। Leases को 8-byte timestamps के साथ भेजा जाता है, भले ही returned leaseset एक LS2 हो जिसमें 4-byte timestamps हों। ध्यान दें कि response एक Create Leaseset या Create Leaseset2 Message हो सकता है।

### नोट्स

क्लाइंट से router. नया संदेश, Create Leaseset Message के स्थान पर उपयोग के लिए।

### Meta LS2

- Router के लिए store type को parse करने के लिए, type का message में होना आवश्यक है,
  जब तक कि यह session config में पहले से router को pass न किया गया हो।
  Common parsing code के लिए, इसका message में ही होना आसान है।

- राउटर को प्राइवेट key का प्रकार और लंबाई जानने के लिए,
  यह leaseSet के बाद होना चाहिए, जब तक कि parser को session config में 
  पहले से ही प्रकार पता न हो।
  सामान्य parsing code के लिए, इसे message से ही जानना आसान है।

- साइनिंग प्राइवेट key, जो पहले revocation के लिए परिभाषित थी और अप्रयुक्त थी,
  LS2 में मौजूद नहीं है।

### प्रारूप

Create Leaseset2 Message के लिए message type 41 है।

### नोट्स

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
### सेवा रिकॉर्ड

- न्यूनतम router संस्करण 0.9.39 है।
- संदेश प्रकार 40 के साथ प्रारंभिक संस्करण 0.9.38 में था लेकिन प्रारूप बदल दिया गया।
  प्रकार 40 को छोड़ दिया गया है और यह असमर्थित है।

### प्रारूप

- एन्क्रिप्टेड और meta LS को समर्थित करने के लिए और भी बदलाव की आवश्यकता है।

### नोट्स

क्लाइंट से router तक। नया संदेश।

### सेवा सूची

- राउटर को यह जानना आवश्यक है कि कोई destination blinded है या नहीं।
  यदि यह blinded है और secret या per-client authentication का उपयोग करता है,
  तो उसके पास वह जानकारी भी होनी चाहिए।

- एक नए-फॉर्मेट b32 address ("b33") की Host Lookup
  router को बताती है कि address blinded है, लेकिन Host Lookup message में
  router को secret या private key पास करने का कोई mechanism नहीं है।
  हालांकि हम उस जानकारी को जोड़ने के लिए Host Lookup message को extend कर सकते हैं,
  लेकिन एक नया message define करना अधिक स्वच्छ है।

- हमें client को router को बताने के लिए एक programmatic तरीके की आवश्यकता है।
  अन्यथा, user को प्रत्येक destination को manually configure करना होगा।

### प्रारूप

इससे पहले कि कोई client किसी blinded destination को message भेजे, उसे या तो Host Lookup message में "b33" को lookup करना होगा, या Blinding Info message भेजना होगा। यदि blinded destination को secret या per-client authentication की आवश्यकता है, तो client को Blinding Info message भेजना होगा।

राउटर इस संदेश का कोई उत्तर नहीं भेजता।

### नोट्स

Blinding Info Message के लिए message type 42 है।

### Format

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
### मुख्य प्रमाणपत्र

- न्यूनतम router संस्करण 0.9.43 है

### नई मध्यवर्ती संरचनाएं

### नए NetDB प्रकार

"b33" hostnames की lookups को support करने के लिए और यदि router के पास आवश्यक जानकारी नहीं है तो इसका संकेत return करने के लिए, हम Host Reply Message के लिए अतिरिक्त result codes को परिभाषित करते हैं, जो निम्नलिखित हैं:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
मान 1-255 पहले से ही errors के रूप में परिभाषित हैं, इसलिए कोई backwards-compatibility समस्या नहीं है।

### नया Signature Type

Router से client के लिए। नया संदेश।

### Justification

एक client को पहले से पता नहीं होता कि कोई दिया गया Hash एक Meta LS में resolve होगा।

यदि किसी Destination के लिए leaseset lookup एक Meta LS return करता है, तो router recursive resolution करेगा। Datagrams के लिए, client side को जानने की जरूरत नहीं है; हालांकि, streaming के लिए, जहाँ protocol SYN ACK में destination को check करता है, उसे पता होना चाहिए कि "real" destination क्या है। इसलिए, हमें एक नए message की आवश्यकता है।

### Usage

router एक cache बनाए रखता है वास्तविक destination के लिए जो एक meta LS से उपयोग किया जाता है। जब client एक destination को message भेजता है जो meta LS में resolve होता है, तो router cache में अंतिम बार उपयोग किए गए वास्तविक destination की जांच करता है। यदि cache खाली है, तो router meta LS से एक destination चुनता है, और leaseset को look up करता है। यदि leaseset lookup सफल है, तो router उस destination को cache में जोड़ता है, और client को एक Meta Redirect Message भेजता है। यह केवल एक बार किया जाता है, जब तक कि destination expire न हो जाए और बदलना न पड़े। Client को भी यदि आवश्यक हो तो जानकारी को cache करना चाहिए। Meta Redirect Message हर SendMessage के जवाब में नहीं भेजा जाता है।

router केवल इस संदेश को version 0.9.47 या उससे ऊपर वाले clients को भेजता है।

क्लाइंट इस संदेश का कोई उत्तर नहीं भेजता।

### डेटाबेस लुकअप संदेश

Meta Redirect Message के लिए message type 43 है।

### परिवर्तन

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
### डेटाबेस स्टोर मैसेज

मेटा को कैसे जेनरेट करना है और उसका समर्थन करना है, जिसमें inter-router communication और coordination शामिल है, यह इस प्रस्ताव के दायरे से बाहर है। संबंधित प्रस्ताव 150 देखें।

### परिवर्तन

ऑफलाइन signatures को streaming या repliable datagrams में verify नहीं किया जा सकता। नीचे दिए गए sections देखें।

## Private Key File Changes Required

निजी कुंजी फ़ाइल (eepPriv.dat) प्रारूप हमारे विनिर्देशों का एक आधिकारिक हिस्सा नहीं है लेकिन यह [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) में प्रलेखित है और अन्य implementations इसका समर्थन करते हैं। यह विभिन्न implementations में निजी कुंजियों की पोर्टेबिलिटी को सक्षम बनाता है।

अस्थायी सार्वजनिक कुंजी और ऑफ़लाइन हस्ताक्षर जानकारी को संग्रहीत करने के लिए परिवर्तन आवश्यक हैं।

### Changes

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
### I2CP विकल्प

निम्नलिखित विकल्पों के लिए समर्थन जोड़ें:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

ऑफ़लाइन signatures को वर्तमान में streaming में verify नहीं किया जा सकता। नीचे दिया गया परिवर्तन offline signing block को options में जोड़ता है। यह I2CP के माध्यम से इस जानकारी को retrieve करने से बचाता है।

### सेशन कॉन्फ़िग

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
### Request Leaseset संदेश

- वैकल्पिक तरीका केवल एक flag जोड़ना है, और transient public key को I2CP के माध्यम से retrieve करना है
  (ऊपर Host Lookup / Host Reply Message sections देखें)

## मानक LS2 हेडर

ऑफ़लाइन signatures को repliable datagram processing में verify नहीं किया जा सकता। offline signed को indicate करने के लिए एक flag की आवश्यकता है लेकिन flag रखने के लिए कोई जगह नहीं है। इसके लिए पूरी तरह से नए protocol number और format की आवश्यकता होगी।

### Request Variable Leaseset Message

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
### Leaseset2 Message बनाएं

- वैकल्पिक रूप से केवल एक फ्लैग जोड़ना है, और I2CP के माध्यम से transient public key को retrieve करना है
  (ऊपर Host Lookup / Host Reply Message sections देखें)
- क्या कोई अन्य विकल्प हैं जो हमें अब जोड़ने चाहिए जब हमारे पास flag bytes हैं?

## SAM V3 Changes Required

SAM को DESTINATION base 64 में offline signatures का समर्थन करने के लिए बेहतर बनाया जाना चाहिए।

### औचित्य

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
ध्यान दें कि offline signatures केवल STREAM और RAW के लिए समर्थित हैं, DATAGRAM के लिए नहीं (जब तक हम एक नया DATAGRAM protocol परिभाषित नहीं करते)।

ध्यान दें कि SESSION STATUS सभी शून्य की एक Signing Private Key और Offline Signature डेटा को बिल्कुल वैसे ही वापस करेगा जैसा SESSION CREATE में प्रदान किया गया था।

ध्यान दें कि DEST GENERATE और SESSION CREATE DESTINATION=TRANSIENT का उपयोग offline signed destination बनाने के लिए नहीं किया जा सकता है।

### संदेश प्रकार

वर्जन को 3.4 पर बढ़ाएं, या इसे 3.1/3.2/3.3 पर छोड़ दें ताकि इसे सभी 3.2/3.3 चीजों की आवश्यकता के बिना जोड़ा जा सके?

अन्य परिवर्तन TBD। ऊपर I2CP Host Reply Message अनुभाग देखें।

## BOB Changes Required

BOB को offline signatures और/या Meta LS का समर्थन करने के लिए बेहतर बनाना होगा। यह कम प्राथमिकता वाला है और शायद कभी निर्दिष्ट या कार्यान्वित नहीं होगा। SAM V3 पसंदीदा interface है।

## Publishing, Migration, Compatibility

LS2 (encrypted LS2 के अलावा) को LS1 के समान DHT location पर publish किया जाता है। LS1 और LS2 दोनों को publish करने का कोई तरीका नहीं है, जब तक कि LS2 किसी अलग location पर न हो।

एन्क्रिप्टेड LS2 को blinded key type और key data के hash पर प्रकाशित किया जाता है। इस hash का उपयोग फिर दैनिक "routing key" उत्पन्न करने के लिए किया जाता है, जैसे LS1 में होता है।

LS2 का उपयोग केवल तभी किया जाएगा जब नई सुविधाओं की आवश्यकता हो (नया crypto, encrypted LS, meta, आदि)। LS2 को केवल निर्दिष्ट version या उससे उच्चतर के floodfills पर प्रकाशित किया जा सकता है।

सर्वर जो LS2 प्रकाशित करते हैं वे जान जाएंगे कि कोई भी कनेक्ट करने वाले क्लाइंट LS2 को सपोर्ट करते हैं। वे garlic में LS2 भेज सकते हैं।

Clients नए crypto का उपयोग करते समय केवल garlics में LS2 भेजेंगे। Shared clients LS1 का अनिश्चित काल तक उपयोग करेंगे? TODO: एक shared clients कैसे रखें जो पुराने और नए दोनों crypto को support करे?

## Rollout

0.9.38 में standard LS2 के लिए floodfill support शामिल है, जिसमें offline keys भी हैं।

0.9.39 में LS2 और Encrypted LS2 के लिए I2CP समर्थन, sig type 11 signing/verification, Encrypted LS2 के लिए floodfill समर्थन (sig types 7 और 11, offline keys के बिना), और LS2 को encrypting/decrypting (per-client authorization के बिना) शामिल है।

0.9.40 में per-client authorization के साथ LS2 को encrypt/decrypt करने का समर्थन, Meta LS2 के लिए floodfill और I2CP समर्थन, offline keys के साथ encrypted LS2 का समर्थन, और encrypted LS2 के लिए b32 समर्थन शामिल करने की योजना है।

## नए DatabaseEntry प्रकार

एन्क्रिप्टेड LS2 डिज़ाइन [Tor के v3 hidden service descriptors](https://spec.torproject.org/rend-spec-v3) से बहुत प्रभावित है, जिसके समान डिज़ाइन लक्ष्य थे।
