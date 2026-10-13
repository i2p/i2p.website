---
title: "सामान्य संरचनाएं विनिर्देश"
description: "सभी I2P प्रोटोकॉल में सामान्य डेटा प्रकार"
slug: "common-structures"
aliases:
  - "/docs/specs/common-structures"
  - "/docs/specs/common-structures/"
category: "डिज़ाइन"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

यह दस्तावेज़ सभी I2P प्रोटोकॉल्स में सामान्य कुछ डेटा प्रकारों का वर्णन करता है, जैसे [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/), आदि।

## सामान्य प्रकार विशिष्टीकरण

### पूर्णांक

#### विवरण

एक गैर-नकारात्मक पूर्णांक का प्रतिनिधित्व करता है।

#### सामग्री

network byte order (big endian) में 1 से 8 bytes जो एक unsigned integer को दर्शाते हैं।

### दिनांक

#### विवरण

GMT timezone में 1 जनवरी, 1970 की मध्यरात्रि से मिलीसेकंड की संख्या। यदि संख्या 0 है, तो तारीख अपरिभाषित या null है।

#### विषय-सूची

8 byte [Integer](#integer)

### स्ट्रिंग

#### विवरण

UTF-8 एन्कोडेड स्ट्रिंग को दर्शाता है।

#### विषय-सूची

1 या अधिक बाइट्स जहाँ पहला बाइट स्ट्रिंग में बाइट्स की संख्या है (वर्णों की नहीं!) और शेष 0-255 बाइट्स गैर-null समाप्त UTF-8 एन्कोडेड वर्ण सरणी हैं। लंबाई की सीमा 255 बाइट्स है (वर्णों की नहीं)। लंबाई 0 हो सकती है।

### PublicKey

#### विवरण

यह संरचना ElGamal या अन्य असममित एन्क्रिप्शन में उपयोग की जाती है, जो केवल घातांक का प्रतिनिधित्व करती है, अभाज्य संख्याओं का नहीं, जो स्थिर हैं और क्रिप्टोग्राफी विनिर्देश [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) में परिभाषित हैं। अन्य एन्क्रिप्शन योजनाओं को परिभाषित करने की प्रक्रिया चल रही है, नीचे दी गई तालिका देखें।

#### सामग्री

Key का प्रकार और लंबाई संदर्भ से समझी जाती है या Destination या RouterInfo के Key Certificate में निर्दिष्ट होती है, या [LeaseSet2](#leaseset2) या अन्य डेटा संरचना के fields में। डिफ़ॉल्ट प्रकार ElGamal है। रिलीज़ 0.9.38 के अनुसार, संदर्भ के आधार पर अन्य प्रकार भी समर्थित हो सकते हैं। जब तक अन्यथा उल्लेख न किया गया हो, Keys big-endian होती हैं।

X25519 keys का समर्थन Destinations और LeaseSet2 में रिलीज़ 0.9.44 से किया जाता है। X25519 keys का समर्थन RouterIdentities में रिलीज़ 0.9.48 से किया जाता है।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### PrivateKey

#### विवरण

यह संरचना ElGamal या अन्य asymmetric decryption में उपयोग की जाती है, जो केवल exponent को दर्शाती है, primes को नहीं जो स्थिर हैं और cryptography specification [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) में परिभाषित हैं। अन्य encryption schemes परिभाषित किए जाने की प्रक्रिया में हैं, नीचे दी गई तालिका देखें।

#### विषय-सूची

Key type और length को context से निकाला जाता है या अलग से data structure या private key file में store किया जाता है। Default type ElGamal है। Release 0.9.38 के बाद से, context के आधार पर अन्य types भी supported हो सकते हैं। Keys big-endian होती हैं जब तक अन्यथा न बताया गया हो।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### विवरण

यह संरचना सममित AES256 एन्क्रिप्शन और डिक्रिप्शन के लिए उपयोग की जाती है।

#### विषय-सूची

32 बाइट्स

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### विवरण

यह संरचना हस्ताक्षरों को सत्यापित करने के लिए उपयोग की जाती है।

#### विषय-सूची

Key type और length संदर्भ से निकाले जाते हैं या Destination के Key Certificate में निर्दिष्ट होते हैं। डिफ़ॉल्ट type DSA_SHA1 है। release 0.9.12 से, संदर्भ के आधार पर अन्य types का समर्थन हो सकता है।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### नोट्स

* जब एक key दो elements से बनी होती है (उदाहरण के लिए points X,Y), तो इसे serialize किया जाता है प्रत्येक element को length/2 तक padding करके यदि आवश्यक हो तो leading zeros के साथ।

* सभी प्रकार Big Endian हैं, EdDSA और RedDSA को छोड़कर, जो Little Endian format में संग्रहीत और प्रसारित किए जाते हैं।

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### विवरण

इस संरचना का उपयोग हस्ताक्षर बनाने के लिए किया जाता है।

#### सामग्री

Key का प्रकार और लंबाई बनाते समय निर्दिष्ट की जाती है। डिफ़ॉल्ट प्रकार DSA_SHA1 है। रिलीज़ 0.9.12 के अनुसार, संदर्भ के आधार पर अन्य प्रकार भी समर्थित हो सकते हैं।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### नोट्स

* जब एक key दो elements से मिलकर बनी होती है (उदाहरण के लिए points X,Y), तो इसे serialize किया जाता है प्रत्येक element को length/2 तक padding करके यदि आवश्यक हो तो leading zeros के साथ।

* सभी प्रकार Big Endian हैं, EdDSA और RedDSA को छोड़कर, जो Little Endian प्रारूप में संग्रहीत और प्रसारित होते हैं।

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### हस्ताक्षर

#### विवरण

यह संरचना कुछ डेटा के हस्ताक्षर को दर्शाती है।

#### सामग्री

Signature प्रकार और लंबाई का अनुमान उपयोग की गई key के प्रकार से लगाया जाता है। डिफ़ॉल्ट प्रकार DSA_SHA1 है। रिलीज़ 0.9.12 के अनुसार, संदर्भ के आधार पर अन्य प्रकार भी समर्थित हो सकते हैं।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### नोट्स

* जब एक signature दो elements से मिलकर बना होता है (उदाहरण के लिए values R,S), तो इसे serialize किया जाता है प्रत्येक element को length/2 तक padding करके leading zeros के साथ यदि आवश्यक हो।

* सभी प्रकार Big Endian हैं, EdDSA और RedDSA को छोड़कर, जो Little Endian फॉर्मेट में संग्रहीत और प्रसारित किए जाते हैं।

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### हैश

#### विवरण

किसी डेटा के SHA256 को दर्शाता है।

#### सामग्री

32 बाइट्स

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### सत्र टैग

नोट: ECIES-X25519 destinations (ratchet) और ECIES-X25519 routers के लिए Session Tags 8 bytes के होते हैं। देखें [ECIES](/docs/specs/ecies/) और [ECIES-ROUTERS](/docs/specs/ecies-routers/)।

#### विवरण

एक यादृच्छिक संख्या

#### सामग्री

32 bytes

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### विवरण

एक पहचानकर्ता को परिभाषित करता है जो tunnel में प्रत्येक router के लिए अद्वितीय है। एक Tunnel ID आमतौर पर शून्य से अधिक होता है; विशेष मामलों को छोड़कर शून्य का मान उपयोग न करें।

#### सामग्री

4 बाइट [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### प्रमाणपत्र

#### विवरण

एक certificate विभिन्न receipts या proof of works के लिए एक container है जो I2P network में उपयोग किया जाता है।

#### विषय-सूची

1 byte [Integer](#integer) जो certificate type निर्दिष्ट करता है, उसके बाद 2 byte [Integer](#integer) जो certificate payload का आकार निर्दिष्ट करता है, फिर उतने bytes।

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### नोट्स

* [Router Identities](#routeridentity) के लिए, Certificate हमेशा NULL होता है संस्करण 0.9.15 तक। 0.9.16 से, एक Key Certificate का उपयोग key types निर्दिष्ट करने के लिए किया जाता है। 0.9.48 से, X25519 encryption public key types की अनुमति है। नीचे देखें।

* [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove) के लिए, Certificate हमेशा NULL होता है, कोई अन्य वर्तमान में implemented नहीं हैं।

* [Garlic Messages](/docs/specs/i2np/#msg-garlic) के लिए, Certificate हमेशा NULL होता है, वर्तमान में कोई अन्य implement नहीं किए गए हैं।

* [Destinations](#destination) के लिए, Certificate non-NULL हो सकता है। 0.9.12 के अनुसार, एक Key Certificate का उपयोग signing public key type को निर्दिष्ट करने के लिए किया जा सकता है। नीचे देखें।

* कार्यान्वयनकर्ताओं को सावधान किया जाता है कि वे Certificates में अतिरिक्त डेटा को प्रतिबंधित करें।
  प्रत्येक certificate प्रकार के लिए उपयुक्त लंबाई को लागू किया जाना चाहिए।

#### प्रमाणपत्र प्रकार

निम्नलिखित प्रमाणपत्र प्रकार परिभाषित हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### की प्रमाणपत्र

Key certificates को release 0.9.12 में पेश किया गया था। उस release से पहले, सभी PublicKeys 256-byte ElGamal keys थीं, और सभी SigningPublicKeys 128-byte DSA-SHA1 keys थीं। एक key certificate Destination या RouterIdentity में PublicKey और SigningPublicKey के प्रकार को इंगित करने का एक तंत्र प्रदान करता है, और मानक लंबाई से अधिक किसी भी key data को package करने के लिए उपयोग होता है।

प्रमाणपत्र से पहले बिल्कुल 384 बाइट्स बनाए रखकर, और किसी भी अतिरिक्त key डेटा को प्रमाणपत्र के अंदर रखकर, हम उन सभी सॉफ्टवेयर के लिए संगतता बनाए रखते हैं जो Destinations और Router Identities को parse करते हैं।

key certificate payload में निम्नलिखित शामिल है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
चेतावनी: key type का क्रम आपकी अपेक्षा के विपरीत है; Signing Public Key Type पहले आता है।

परिभाषित Signing Public Key प्रकार हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
परिभाषित Crypto Public Key प्रकार हैं:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
जब Key Certificate मौजूद नहीं होता, तो Destination या RouterIdentity में पूर्ववर्ती 384 बाइट्स को 256-बाइट ElGamal PublicKey के बाद 128-बाइट DSA-SHA1 SigningPublicKey के रूप में परिभाषित किया जाता है। जब Key Certificate मौजूद होता है, तो पूर्ववर्ती 384 बाइट्स को निम्नलिखित के अनुसार पुनः परिभाषित किया जाता है:

* Crypto Public Key का पूरा या पहला हिस्सा

* यदि दोनों keys की कुल लंबाई 384 bytes से कम है तो Random padding

* Signing Public Key का पूर्ण या प्रथम भाग

Crypto Public Key शुरुआत में संरेखित होती है और Signing Public Key अंत में संरेखित होती है। पैडिंग (यदि कोई है) बीच में होती है। प्रमाणपत्रों में प्रारंभिक key डेटा, पैडिंग, और अतिरिक्त key डेटा भागों की लंबाई और सीमाएं स्पष्ट रूप से निर्दिष्ट नहीं हैं, बल्कि निर्दिष्ट key प्रकारों की लंबाई से प्राप्त की जाती हैं। यदि Crypto और Signing Public Keys की कुल लंबाई 384 बाइट्स से अधिक है, तो शेष भाग Key Certificate में समाहित होगा। यदि Crypto Public Key की लंबाई 256 बाइट्स नहीं है, तो दोनों keys के बीच सीमा निर्धारण की विधि इस दस्तावेज़ के भविष्य के संशोधन में निर्दिष्ट की जाएगी।

ElGamal Crypto Public Key और संकेतित Signing Public Key प्रकार का उपयोग करके उदाहरण लेआउट:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### नोट्स

* कार्यान्वयनकर्ताओं को चेतावनी दी जाती है कि वे Key Certificates में अतिरिक्त डेटा को प्रतिबंधित करें।
  प्रत्येक certificate प्रकार के लिए उपयुक्त लंबाई को लागू किया जाना चाहिए।

* प्रकार 0,0 (ElGamal,DSA_SHA1) के साथ एक KEY certificate की अनुमति है लेकिन इसे हतोत्साहित किया जाता है।
  यह अच्छी तरह से परीक्षित नहीं है और कुछ implementations में समस्याएं पैदा कर सकता है।
  (ElGamal,DSA_SHA1) Destination या RouterIdentity की canonical representation में NULL certificate का उपयोग करें, जो KEY certificate का उपयोग करने से 4 bytes छोटा होगा।

### मैपिंग

#### विवरण

key/value मैपिंग्स या गुणधर्मों का एक सेट

#### सामग्री

एक 2-बाइट साइज़ Integer जिसके बाद String=String; जोड़ों की एक श्रृंखला होती है।

चेतावनी: Mapping के अधिकांश उपयोग signed structures में होते हैं, जहाँ Mapping entries को key के आधार पर sorted होना चाहिए, ताकि signature अपरिवर्तनीय रहे। Key के आधार पर sort नहीं करने से signature failures हो सकती हैं!

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### नोट्स

* एन्कोडिंग अनुकूलित नहीं है - हमें या तो '=' और ';' वर्णों की आवश्यकता है, या
  स्ट्रिंग की लंबाई की, लेकिन दोनों की नहीं

#### विवरण

* कुछ दस्तावेज़ कहते हैं कि स्ट्रिंग में '=' या ';' शामिल नहीं हो सकते लेकिन यह एन्कोडिंग उनका समर्थन करती है

* स्ट्रिंग्स को UTF-8 के रूप में परिभाषित किया गया है लेकिन वर्तमान implementation में, I2CP UTF-8 का उपयोग करता है लेकिन I2NP नहीं करता। उदाहरण के लिए, I2NP Database Store Message में RouterInfo options mapping में UTF-8 स्ट्रिंग्स खराब हो जाएंगी।

* एन्कोडिंग डुप्लिकेट keys की अनुमति देता है, हालांकि किसी भी उपयोग में जहां mapping signed है, डुप्लिकेट्स signature failure का कारण बन सकते हैं।

* I2NP messages में शामिल mappings (जैसे कि RouterAddress या RouterInfo में) को key के अनुसार sorted होना चाहिए ताकि signature अपरिवर्तित रहे। Duplicate keys की अनुमति नहीं है।

* [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) में शामिल mappings को key के अनुसार क्रमबद्ध होना चाहिए ताकि signature अपरिवर्तनीय रहे। डुप्लिकेट keys की अनुमति नहीं है।

* Sort method Java String.compareTo() के अनुसार परिभाषित है, जो characters के Unicode value का उपयोग करती है।

* जबकि यह एप्लिकेशन पर निर्भर है, keys और values आमतौर पर case-sensitive होते हैं।

* Key और value स्ट्रिंग की लंबाई की सीमा प्रत्येक के लिए 255 bytes (characters नहीं) है, साथ में length byte भी। Length byte 0 हो सकता है।

* कुल लंबाई सीमा 65535 बाइट्स है, प्लस 2 बाइट साइज़ फील्ड, या कुल 65537।

* X25519 एन्क्रिप्शन प्रकार और Ed25519 सिग्नेचर प्रकार वाली एक Router Identity में रैंडम डेटा की 10 प्रतियां (320 बाइट्स) होंगी, जो compress होने पर लगभग 288 बाइट्स की बचत देगी।

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## सामान्य संरचना विशेषता

### KeysAndCert

#### विषय सूची

एक encryption public key, एक signing public key, और एक certificate, जो RouterIdentity या Destination के रूप में उपयोग की जाती है।

#### पैडिंग जेनरेशन दिशानिर्देश

एक [PublicKey](#publickey) के बाद एक [SigningPublicKey](#signingpublickey) और फिर एक [Certificate](#certificate)।

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### नोट्स

ये दिशानिर्देश प्रस्ताव 161 में प्रस्तावित किए गए थे और API संस्करण 0.9.57 में लागू किए गए थे। ये दिशानिर्देश 0.6 (2005) के बाद से सभी संस्करणों के साथ पिछड़े-संगत हैं। पृष्ठभूमि और अधिक जानकारी के लिए प्रस्ताव 161 देखें।

ElGamal + DSA-SHA1 के अलावा वर्तमान में उपयोग किए जाने वाले key types के किसी भी संयोजन के लिए, padding मौजूद होगी। इसके अतिरिक्त, destinations के लिए, 256-byte public key field का उपयोग version 0.6 (2005) के बाद से नहीं किया गया है।

implementers को Destination public keys, और Destination और Router Identity padding के लिए random data इस तरह generate करना चाहिए कि यह विभिन्न I2P protocols में compressible हो जबकि secure भी रहे, और Base 64 representations corrupt या insecure न दिखें। यह padding fields को हटाने के अधिकांश फायदे प्रदान करता है बिना किसी disruptive protocol changes के।

सख्ती से कहें तो, 32-बाइट signing public key अकेले (Destinations और Router Identities दोनों में) और 32-बाइट encryption public key (केवल Router Identities में) एक यादृच्छिक संख्या है जो इन संरचनाओं के SHA-256 हैश के लिए आवश्यक सभी एंट्रॉपी प्रदान करती है ताकि वे cryptographically मजबूत हों और network database DHT में यादृच्छिक रूप से वितरित हों।

हालांकि, अत्यधिक सावधानी के कारण, हम अनुशंसा करते हैं कि ElG public key field और padding में न्यूनतम 32 bytes का random data उपयोग किया जाए। इसके अतिरिक्त, यदि सभी fields शून्य होते हैं, तो Base 64 destinations में AAAA characters की लंबी श्रृंखलाएं होंगी, जो उपयोगकर्ताओं में चिंता या भ्रम का कारण बन सकती हैं।

32 बाइट्स के random डेटा को आवश्यकता के अनुसार दोहराएं ताकि पूरा KeysAndCert structure I2P प्रोटोकॉल जैसे कि I2NP Database Store Message, Streaming SYN, SSU2 handshake, और repliable Datagrams में अत्यधिक compressible हो सके।

उदाहरण:

* Ed25519 signature प्रकार वाले Destination में
  random data की 11 प्रतियाँ (352 bytes) होंगी, जो compress होने पर लगभग 320 bytes की बचत देती है।

* यह मत मानें कि ये हमेशा 387 बाइट्स होते हैं! ये 387 बाइट्स प्लस certificate length होते हैं जो बाइट्स 385-386 में निर्दिष्ट होती है, जो शून्य से अधिक हो सकती है।

कार्यान्वयन को निश्चित रूप से पूर्ण 387+ बाइट संरचना को स्टोर करना चाहिए क्योंकि संरचना का SHA-256 हैश पूरी सामग्री को कवर करता है।

#### विवरण

* रिलीज़ 0.9.12 के अनुसार, यदि certificate एक Key Certificate है, तो key fields की सीमाएं भिन्न हो सकती हैं। विवरण के लिए ऊपर Key Certificate अनुभाग देखें।

* Crypto Public Key शुरुआत में aligned है और Signing Public Key अंत में aligned है। Padding (यदि कोई है) बीच में है।

* RouterIdentity के लिए प्रमाणपत्र रिलीज़ 0.9.12 तक हमेशा NULL था।

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### विषय-सूची

किसी विशेष router को विशिष्ट रूप से पहचानने का तरीका परिभाषित करता है

#### नोट्स

KeysAndCert के समान।

padding field के लिए random data generate करने के दिशा-निर्देशों के लिए [KeysAndCert](#keysandcert) देखें।

#### विवरण

* यह मान कर न चलें कि ये हमेशा 387 bytes होते हैं! ये 387 bytes होते हैं जमा certificate की लंबाई जो bytes 385-386 में निर्दिष्ट होती है, जो शून्य से अधिक हो सकती है।

* रिलीज़ 0.9.12 के अनुसार, यदि certificate एक Key Certificate है, तो key fields की सीमाएं भिन्न हो सकती हैं। विवरण के लिए ऊपर Key Certificate section देखें।

* Crypto Public Key की शुरुआत में संरेखित है और Signing Public Key अंत में संरेखित है। padding (यदि कोई हो) बीच में है।

* key certificate और ECIES_X25519 public key के साथ RouterIdentities को release 0.9.48 से support किया जाता है।
  इससे पहले, सभी RouterIdentities ElGamal थे।

* destination की public key पुराने i2cp-to-i2cp
  encryption के लिए उपयोग की जाती थी जो version 0.6 (2005) में disable कर दी गई थी, वर्तमान में यह LeaseSet encryption के लिए IV के अलावा उपयोग नहीं होती, जो deprecated है। इसके बजाय LeaseSet में public key का उपयोग किया जाता है।

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### गंतव्य

#### सामग्री

एक Destination एक विशेष endpoint को परिभाषित करता है जहाँ messages को सुरक्षित delivery के लिए भेजा जा सकता है।

#### नोट्स

[KeysAndCert](#keysandcert) के समान, सिवाय इसके कि public key कभी उपयोग नहीं की जाती, और इसमें वैध ElGamal Public Key के बजाय random data हो सकता है।

Public key और padding fields के लिए random data generate करने के दिशा-निर्देशों के लिए [KeysAndCert](#keysandcert) देखें।

#### विवरण

* यह मत मान लीजिए कि ये हमेशा 387 bytes होते हैं! ये 387 bytes होते हैं साथ ही certificate की लंबाई जो bytes 385-386 पर निर्दिष्ट होती है, जो शून्य नहीं हो सकती।

* रिलीज़ 0.9.12 के अनुसार, यदि certificate एक Key Certificate है, तो key fields की सीमाएं अलग हो सकती हैं। विवरण के लिए ऊपर Key Certificate अनुभाग देखें।

* Crypto Public Key शुरुआत में aligned है और Signing Public Key अंत में aligned है। padding (यदि कोई है) बीच में है।

* गंतव्य की public key पुराने I2CP-to-I2CP एन्क्रिप्शन के लिए उपयोग की जाती थी जो संस्करण 0.6 में अक्षम कर दी गई थी, यह वर्तमान में अप्रयुक्त है।

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### सामग्री

पुराना। LeaseSet2 और Lease2 का उपयोग करें।

एक [Destination](#destination) को लक्षित करने वाले संदेश प्राप्त करने के लिए एक विशेष टनल के लिए प्राधिकरण निर्धारित करता है।

#### विवरण

गेटवे राउटर के [राउटर आइडेंटिटी](#routeridentity) का SHA256 [हैश](#hash), फिर [टनल आइडी](#tunnelid), और अंत में एक समाप्ति [तिथि](#date)।

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
जावाडॉक: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### विषय-सूची

पुराना। LeaseSet2 और Lease2 का उपयोग करें।

एक विशेष [Destination](#destination) के लिए वर्तमान में अधिकृत सभी [Leases](#lease) को शामिल करता है, वह [PublicKey](#publickey) जिस पर गैर्लिक संदेश एन्क्रिप्ट किए जा सकते हैं, और फिर वह [SigningPublicKey](#signingpublickey) जिसका उपयोग इस संरचना के विशेष संस्करण को रद्द करने के लिए किया जा सकता है। LeaseSet नेटवर्क डेटाबेस में संग्रहीत दो संरचनाओं में से एक है (दूसरा [RouterInfo](#routerinfo) है), और इसे उसमें शामिल [Destination](#destination) के SHA256 के तहत संग्रहीत किया जाता है।

#### नोट्स

[Destination](#destination), जिसके बाद एन्क्रिप्शन के लिए एक [PublicKey](#publickey), फिर एक [SigningPublicKey](#signingpublickey) जिसका उपयोग LeaseSet के इस संस्करण को रद्द करने के लिए किया जा सकता है, फिर एक 1 byte [Integer](#integer) जो निर्दिष्ट करता है कि set में कितने [Lease](#lease) structures हैं, जिसके बाद वास्तविक [Lease](#lease) structures हैं और अंत में [Destination](#destination) के [SigningPrivateKey](#signingprivatekey) द्वारा हस्ताक्षरित पिछले bytes का एक [Signature](#signature)।

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### विवरण

* एन्क्रिप्शन key का उपयोग end-to-end ElGamal/AES+SessionTag एन्क्रिप्शन के लिए किया जाता है
  [ELGAMAL-AES](/docs/specs/elgamal-aes/)। यह वर्तमान में हर router startup पर नई generate की जाती है, यह
  persistent नहीं है।

* signature को destination की signing public key का उपयोग करके सत्यापित किया जा सकता है।

* शून्य Leases के साथ एक LeaseSet की अनुमति है लेकिन यह अप्रयुक्त है।
  इसका उद्देश्य LeaseSet निरसन के लिए था, जो अभी तक लागू नहीं किया गया है।
  सभी LeaseSet2 variants में कम से कम एक Lease की आवश्यकता होती है।

* signing_key वर्तमान में अप्रयुक्त है। यह LeaseSet निरसन के लिए था, जो अभी तक लागू नहीं किया गया है। यह वर्तमान में हर router स्टार्टअप पर नया बनाया जाता है, यह स्थायी नहीं है। signing key type हमेशा destination के signing key type के समान होता है।

* सभी Lease की सबसे पहली समाप्ति को LeaseSet के timestamp या version के रूप में माना जाता है। Router आम तौर पर किसी LeaseSet के store को तब तक स्वीकार नहीं करते जब तक कि वह मौजूदा LeaseSet से "नया" न हो। नया LeaseSet प्रकाशित करते समय सावधानी बरतें जहाँ सबसे पुराना Lease पिछले LeaseSet के सबसे पुराने Lease के समान हो। प्रकाशन करने वाले router को आम तौर पर उस स्थिति में सबसे पुराने Lease की समाप्ति को कम से कम 1 ms बढ़ाना चाहिए।

* रिलीज़ 0.9.7 से पहले, जब originating router द्वारा भेजे गए DatabaseStore Message में शामिल किया जाता था, तो router सभी प्रकाशित leases की समाप्ति को समान मान पर सेट करता था, जो कि सबसे पहली lease का था। रिलीज़ 0.9.7 से, router प्रत्येक lease के लिए वास्तविक lease expiration प्रकाशित करता है। यह एक implementation detail है और structures specification का हिस्सा नहीं है।

* कुल आकार: 40 bytes

जावाडॉक: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### सामग्री

किसी विशेष tunnel के लिए [Destination](#destination) को लक्षित संदेशों को प्राप्त करने के लिए प्राधिकरण को परिभाषित करता है। [Lease](#lease) के समान लेकिन 4-byte end_date के साथ। [LeaseSet2](#leaseset2) द्वारा उपयोग किया जाता है। 0.9.38 से समर्थित; अधिक जानकारी के लिए proposal 123 देखें।

#### नोट्स

गेटवे राउटर के [राउटर पहचान](#routeridentity) का SHA256 [हैश](#hash), फिर [टनल आइडी](#tunnelid), और अंत में एक 4 बाइट की समाप्ति तिथि।

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### विवरण

* इस अनुभाग को ऑफलाइन उत्पन्न किया जा सकता है, और किया जाना चाहिए।

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### सामग्री

यह [LeaseSet2Header](#leaseset2header) का एक वैकल्पिक भाग है। इसका उपयोग स्ट्रीमिंग और I2CP में भी किया जाता है। संस्करण 0.9.38 से इसका समर्थन किया जा रहा है; अधिक जानकारी के लिए प्रस्ताव 123 देखें।

#### नोट्स

इसमें एक expiration, एक sigtype और transient [SigningPublicKey](#signingpublickey), और एक [Signature](#signature) होता है।

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### विवरण

* **Flags** (2 bytes):
  * Bit 0: यदि सेट है, तो offline keys मौजूद हैं (देखें [OfflineSignature](#offlinesignature))
  * Bit 1: यदि सेट है, तो यह एक unpublished leaseset है
  * Bit 2: यदि सेट है, तो यह एक blinded leaseset है
  * Bits 15-3: आरक्षित, 0 पर सेट करें

### LeaseSet2Header

#### सामग्री

यह [LeaseSet2](#leaseset2) और [MetaLeaseSet](#metaleaseset) का सामान्य भाग है। संस्करण 0.9.38 से समर्थित; अधिक जानकारी के लिए प्रस्ताव 123 देखें।

#### नोट्स

इसमें [Destination](#destination), दो timestamps, और एक वैकल्पिक [OfflineSignature](#offlinesignature) शामिल है।

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### विवरण

* कुल आकार: न्यूनतम 395 बाइट्स

* वास्तविक अधिकतम समाप्ति समय [LeaseSet2](#leaseset2) के लिए लगभग 660 (11 मिनट) और [MetaLeaseSet](#metaleaseset) के लिए 65535 (पूरे 18.2 घंटे) है।

* [LeaseSet](#leaseset) (1) में 'published' फ़ील्ड नहीं था, इसलिए versioning के लिए सबसे पुराने lease की खोज करना आवश्यक था। LeaseSet2 एक सेकंड के resolution के साथ 'published' फ़ील्ड जोड़ता है। Router को floodfill को नए leaseset भेजने की दर को प्रति सेकंड एक बार से बहुत धीमी दर पर सीमित करना चाहिए (प्रति destination)। यदि यह लागू नहीं किया गया है, तो code को यह सुनिश्चित करना चाहिए कि प्रत्येक नए leaseset का 'published' समय पिछले वाले की तुलना में कम से कम एक सेकंड बाद हो, अन्यथा floodfill नए leaseset को store या flood नहीं करेंगे।

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := वांछित सेवा का प्रतीकात्मक नाम। छोटे अक्षरों में होना चाहिए। उदाहरण: "smtp"।
  अनुमतित वर्ण [a-z0-9-] हैं और '-' से शुरू या समाप्त नहीं होना चाहिए।
  [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) या Linux /etc/services के मानक पहचानकर्ताओं का उपयोग करना चाहिए यदि वहाँ परिभाषित हैं।
- proto := वांछित सेवा का परिवहन प्रोटोकॉल। छोटे अक्षरों में होना चाहिए, या तो "tcp" या "udp"।
  "tcp" का मतलब स्ट्रीमिंग है और "udp" का मतलब उत्तर देने योग्य डेटाग्राम है।
  raw datagrams और datagram2 के लिए प्रोटोकॉल संकेतक बाद में परिभाषित किए जा सकते हैं।
  अनुमतित वर्ण [a-z0-9-] हैं और '-' से शुरू या समाप्त नहीं होना चाहिए।
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := जीवनकाल, पूर्णांक सेकंड में। धनात्मक पूर्णांक। उदाहरण: "86400"।
  न्यूनतम 86400 (एक दिन) की सिफारिश की जाती है, विवरण के लिए नीचे सिफारिशें अनुभाग देखें।
- priority := लक्ष्य होस्ट की प्राथमिकता, कम मान का मतलब अधिक प्राथमिकता है। गैर-नकारात्मक पूर्णांक। उदाहरण: "0"
  केवल तभी उपयोगी जब एक से अधिक रिकॉर्ड हों, लेकिन एक ही रिकॉर्ड होने पर भी आवश्यक।
- weight := समान प्राथमिकता वाले रिकॉर्ड के लिए सापेक्ष भार। उच्च मान का मतलब चुने जाने की अधिक संभावना है। गैर-नकारात्मक पूर्णांक। उदाहरण: "0"
  केवल तभी उपयोगी जब एक से अधिक रिकॉर्ड हों, लेकिन एक ही रिकॉर्ड होने पर भी आवश्यक।
- port := I2CP पोर्ट जिस पर सेवा मिलनी है। गैर-नकारात्मक पूर्णांक। उदाहरण: "25"
  पोर्ट 0 समर्थित है लेकिन अनुशंसित नहीं।
- target := सेवा प्रदान करने वाले गंतव्य का होस्टनाम या b32। [NAMING](/docs/overview/naming/) में दिए गए अनुसार एक मान्य होस्टनाम। छोटे अक्षरों में होना चाहिए।
  उदाहरण: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" या "example.i2p"।
  b32 की सिफारिश की जाती है जब तक कि होस्टनाम "प्रसिद्ध" न हो, यानी आधिकारिक या डिफ़ॉल्ट पता पुस्तकों में।
- appoptions := एप्लिकेशन के लिए विशिष्ट मनमाना पाठ, इसमें " " या "," नहीं होना चाहिए। एन्कोडिंग UTF-8 है।

### LeaseSet2

#### सामग्री

प्रकार 3 के I2NP डेटाबेसस्टोर संदेश में शामिल। 0.9.38 से समर्थित; अधिक जानकारी के लिए प्रस्ताव 123 देखें।

किसी विशेष [Destination](#destination) के लिए वर्तमान में अधिकृत सभी [Lease2](#lease2) को शामिल करता है, और [PublicKey](#publickey) जिसमें garlic messages को एन्क्रिप्ट किया जा सकता है। एक LeaseSet network database में संग्रहीत दो संरचनाओं में से एक है (दूसरी [RouterInfo](#routerinfo) है), और यह शामिल [Destination](#destination) के SHA256 के तहत keyed है।

#### एन्क्रिप्शन की प्राथमिकता

[LeaseSet2Header](#leaseset2header), उसके बाद विकल्प, फिर एन्क्रिप्शन के लिए एक या अधिक [PublicKey](#publickey), [Lease2](#lease2) संरचनाओं की संख्या निर्दिष्ट करने वाला [Integer](#integer), उसके बाद वास्तविक [Lease2](#lease2) संरचनाएँ, और अंत में पिछले बाइट्स का एक [Signature](#signature), जो [Destination](#destination) के [SigningPrivateKey](#signingprivatekey) या पारगमन कुंजी द्वारा हस्ताक्षरित हो।

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### विकल्प

प्रकाशित (server) leasesets के लिए, encryption keys server की प्राथमिकता के क्रम में होती हैं, सबसे पसंदीदा पहले। यदि clients एक से अधिक encryption प्रकार का समर्थन करते हैं, तो यह अनुशंसा की जाती है कि वे server की प्राथमिकता का सम्मान करें और server से जुड़ने के लिए उपयोग करने हेतु encryption method के रूप में पहले समर्थित प्रकार का चयन करें। आम तौर पर, नए (उच्च-संख्या वाले) key प्रकार अधिक सुरक्षित या कुशल होते हैं और पसंद किए जाते हैं, इसलिए keys को key प्रकार के विपरीत क्रम में सूचीबद्ध किया जाना चाहिए।

हालाँकि, क्लाइंट अपनी पसंद के आधार पर, लागूकरण-पर-निर्भर, चयन कर सकते हैं, या "संयुक्त" पसंद निर्धारित करने के लिए कुछ विधि का उपयोग कर सकते हैं। यह एक विन्यास विकल्प के रूप में, या डिबगिंग के लिए उपयोगी हो सकता है।

अप्रकाशित (क्लाइंट) leasesets में key क्रम प्रभावी रूप से कोई मायने नहीं रखता, क्योंकि आमतौर पर अप्रकाशित क्लाइंट्स से कनेक्शन का प्रयास नहीं किया जाएगा। जब तक कि यह क्रम संयुक्त प्राथमिकता निर्धारित करने के लिए उपयोग नहीं किया जाता, जैसा कि ऊपर वर्णित है।

#### नोट्स

API 0.9.66 के रूप में, सेवा रिकॉर्ड विकल्पों के लिए एक मानक प्रारूप परिभाषित किया गया है। विवरण के लिए प्रस्ताव 167 देखें। भविष्य में अलग प्रारूप का उपयोग करके सेवा रिकॉर्ड के अलावा अन्य विकल्प परिभाषित किए जा सकते हैं।

LS2 विकल्पों को key के अनुसार क्रमबद्ध होना चाहिए, ताकि signature अपरिवर्तनीय रहे।

सेवा रिकॉर्ड विकल्प निम्नानुसार परिभाषित किए गए हैं:

* गंतव्य की public key पुराने I2CP-to-I2CP एन्क्रिप्शन के लिए उपयोग की जाती थी जो संस्करण 0.6 में अक्षम कर दी गई थी, यह वर्तमान में अप्रयुक्त है।

उदाहरण:

LS2 में aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p के लिए, जो एक SMTP सर्वर की ओर इशारा करता है:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

LS2 में aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p के लिए, दो SMTP सर्वर की ओर इंगित करते हुए:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

LS2 में bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p के लिए, जो स्वयं को SMTP सर्वर के रूप में इंगित करता है:

"_smtp._tcp" "0 999999 25"

#### विवरण

* एन्क्रिप्शन keys का उपयोग end-to-end ElGamal/AES+SessionTag encryption
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (type 0) या अन्य end-to-end encryption schemes के लिए किया जाता है।
  [ECIES](/docs/specs/ecies/) और proposals 145 और 156 देखें।
  ये हर router startup पर नई बनाई जा सकती हैं
  या ये persistent हो सकती हैं।
  X25519 (type 4, [ECIES](/docs/specs/ecies/) देखें) release 0.9.44 से समर्थित है।

* signature उपरोक्त डेटा पर है, जिसके साथ DatabaseStore प्रकार (3) वाला एकल बाइट PREPENDED है।

* हस्ताक्षर को destination की signing public key का उपयोग करके सत्यापित किया जा सकता है, या transient signing public key का उपयोग करके, यदि leaseset2 header में offline signature शामिल है।

* प्रत्येक key के लिए key length प्रदान की गई है, ताकि floodfills और clients इस structure को parse कर सकें, भले ही सभी encryption types ज्ञात या समर्थित न हों।

* [LeaseSet2Header](#leaseset2header) में 'published' फील्ड पर टिप्पणी देखें

* यदि आकार एक से अधिक है, तो options mapping को key के अनुसार क्रमबद्ध होना चाहिए, ताकि signature अपरिवर्तनीय रहे।

* कुल आकार: 40 bytes

जावाडॉक: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### सामग्री

प्रारंभिक। पूरी तरह से समर्थित नहीं।

किसी विशेष tunnel के लिए प्राधिकरण को परिभाषित करता है ताकि वह [Destination](#destination) को लक्षित संदेशों को प्राप्त कर सके। [Lease2](#lease2) के समान है लेकिन tunnel id के बजाय flags और cost के साथ। [MetaLeaseSet](#metaleaseset) द्वारा उपयोग किया जाता है। प्रकार 7 के I2NP DatabaseStore संदेश में समाहित है। 0.9.38 से समर्थित; अधिक जानकारी के लिए proposal 123 देखें।

#### नोट्स

गेटवे राउटर के [RouterIdentity](#routeridentity) का SHA256 [Hash](#hash), फिर फ्लैग और लागत, और अंत में एक 4 बाइट की समाप्ति तिथि।

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### विवरण

* गंतव्य की सार्वजनिक कुंजी पुराने I2CP-to-I2CP एन्क्रिप्शन के लिए उपयोग की जाती थी जो संस्करण 0.6 में अक्षम कर दी गई थी, यह वर्तमान में अप्रयुक्त है।

जावाडॉक: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### विषय-सूची

प्रारंभिक। पूरी तरह से समर्थित नहीं।

प्रकार 7 के I2NP डेटाबेसस्टोर संदेश में शामिल। 0.9.38 से परिभाषित; अधिक जानकारी के लिए प्रस्ताव 123 देखें।

एक विशिष्ट [Destination](#destination) के लिए वर्तमान में प्राधिकृत सभी [MetaLease](#metalease) को शामिल करता है, और वह [PublicKey](#publickey) जिस पर लहसुन एन्क्रिप्शन (garlic encryption) संदेश भेजे जा सकते हैं। LeaseSet नेटवर्क डेटाबेस में संग्रहीत दो संरचनाओं में से एक है (दूसरा [RouterInfo](#routerinfo) है), और इसे शामिल [Destination](#destination) के SHA256 के अंतर्गत कुंजीबद्ध किया जाता है।

#### टिप्पणियां

[LeaseSet2Header](#leaseset2header), उसके बाद विकल्प, [Integer](#integer) जो यह निर्दिष्ट करता है कि सेट में कितनी [Lease2](#lease2) संरचनाएँ हैं, उसके बाद वास्तविक [Lease2](#lease2) संरचनाएँ और अंत में पिछले बाइट्स का एक [Signature](#signature), जो [Destination](#destination) की [SigningPrivateKey](#signingprivatekey) या पारगमन कुंजी द्वारा हस्ताक्षरित है।

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### विवरण

* हस्ताक्षर उपरोक्त डेटा पर है, जिसके आगे DatabaseStore प्रकार (7) वाला एकल बाइट जोड़ा गया है।

* हस्ताक्षर को destination की signing public key का उपयोग करके सत्यापित किया जा सकता है, या transient signing public key का उपयोग करके, यदि leaseset2 header में एक offline signature शामिल है।

* [LeaseSet2Header](#leaseset2header) में 'published' फील्ड पर नोट देखें

* गंतव्य की सार्वजनिक कुंजी का उपयोग पुराने I2CP-to-I2CP एन्क्रिप्शन के लिए किया जाता था जो संस्करण 0.6 में अक्षम कर दिया गया था, यह वर्तमान में अप्रयुक्त है।

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### विषय सूची

प्रकार 5 के I2NP डेटाबेसस्टोर संदेश में शामिल। 0.9.38 से परिभाषित; 0.9.39 से कार्यरत; अधिक जानकारी के लिए प्रस्ताव 123 देखें।

केवल ब्लाइंड कुंजी और समाप्ति स्पष्ट पाठ में दृश्यमान हैं। वास्तविक लीज सेट एन्क्रिप्टेड है।

#### नोट्स

एक दो-बाइट हस्ताक्षर प्रकार, ब्लाइंडेड [SigningPrivateKey](#signingprivatekey), प्रकाशन समय, समाप्ति और झंडियाँ। फिर, एक दो-बाइट लंबाई जिसके बाद एन्क्रिप्टेड डेटा होता है। अंत में, पिछले बाइट्स का एक [Signature](#signature), जिस पर हस्ताक्षर ब्लाइंडेड [SigningPrivateKey](#signingprivatekey) या ट्रांजिएंट कुंजी द्वारा किया गया हो।

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### विवरण

* signature ऊपर दिए गए data पर है, जिसके साथ DatabaseStore प्रकार (5) वाला एक single byte PREPENDED है।

* हस्ताक्षर को destination की signing public key का उपयोग करके सत्यापित किया जा सकता है, या transient signing public key का उपयोग करके, यदि leaseset2 header में एक offline signature शामिल है।

* Blinding और encryption को [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) में निर्दिष्ट किया गया है

* यह संरचना [LeaseSet2Header](#leaseset2header) का उपयोग नहीं करती है।

* अधिकतम वास्तविक expires time लगभग 660 (11 मिनट) है, जब तक कि यह एक encrypted [MetaLeaseSet](#metaleaseset) न हो।

* encrypted leasesets के साथ offline signatures का उपयोग करने के बारे में नोट्स के लिए प्रस्ताव 123 देखें।

* [LeaseSet2Header](#leaseset2header) में 'published' फील्ड पर नोट देखें
  (यही समस्या, भले ही हम यहाँ LeaseSet2Header फॉर्मेट का उपयोग नहीं करते)

* लागत आमतौर पर SSU के लिए 5 या 6 होती है, और NTCP के लिए 10 या 11 होती है।

* Expiration वर्तमान में अप्रयुक्त है, हमेशा null (सभी शून्य)। रिलीज़ 0.9.3 के अनुसार, expiration को शून्य माना जाता है और संग्रहीत नहीं किया जाता, इसलिए कोई भी गैर-शून्य expiration RouterInfo signature verification में विफल हो जाएगा। Expiration को लागू करना (या इन bytes के लिए कोई अन्य उपयोग) एक backwards-incompatible परिवर्तन होगा। Routers को इस field को सभी शून्य पर सेट करना चाहिए। रिलीज़ 0.9.12 के अनुसार, एक गैर-शून्य expiration field को फिर से पहचाना जाता है, हालांकि हमें इस field का उपयोग करने के लिए कई रिलीज़ों तक प्रतीक्षा करनी होगी, जब तक कि network का विशाल बहुमत इसे पहचान न ले।

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### विषय सूची

यह संरचना एक ट्रांसपोर्ट प्रोटोकॉल के माध्यम से राउटर से संपर्क करने के साधनों को परिभाषित करती है।

#### टिप्पणियां

1 बाइट [Integer](#integer), जो पते के उपयोग की सापेक्ष लागत को परिभाषित करता है, जहाँ 0 का अर्थ मुफ्त और 255 का अर्थ महंगा होता है, उसके बाद [Date](#date) आती है जिसके बाद पते का उपयोग नहीं किया जाना चाहिए, या यदि शून्य हो तो पता कभी समाप्त नहीं होता। इसके बाद परिवहन प्रोटोकॉल को परिभाषित करने वाला एक [String](#string) आता है जिसका इस राउटर पते द्वारा उपयोग किया जाता है। अंत में सभी परिवहन-विशिष्ट विकल्पों वाला एक [Mapping](#mapping) होता है जो संपर्क स्थापित करने के लिए आवश्यक होते हैं, जैसे आईपी पता, पोर्ट नंबर, ईमेल पता, यूआरएल, आदि।

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### विवरण

* निम्नलिखित विकल्प, हालांकि आवश्यक नहीं हैं, मानक हैं और अधिकांश router पतों में उपस्थित होने की अपेक्षा की जाती है: "host" (एक IPv4 या IPv6 पता या host नाम) और "port"।

* peer_size [Integer](#integer) के बाद उतनी router hashes की सूची हो सकती है।
  यह वर्तमान में अप्रयुक्त है। यह प्रतिबंधित routes के एक रूप के लिए अभिप्रेत था,
  जो अभी तक implement नहीं हुआ है।
  कुछ implementations में signature को invariant रखने के लिए सूची को sorted करना आवश्यक हो सकता है।
  इस feature को enable करने से पहले इस पर research की जानी है।

* हस्ताक्षर को router_ident की signing public key का उपयोग करके सत्यापित किया जा सकता है।

* सभी router infos में मौजूद होने वाले मानक विकल्पों के लिए network database पृष्ठ [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) देखें।

जावाडॉक: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### विषय-सूची

उस सभी डेटा को परिभाषित करता है जिसे एक router नेटवर्क के लिए प्रकाशित करना चाहता है। [RouterInfo](#routerinfo) नेटवर्क डेटाबेस में संग्रहीत दो संरचनाओं में से एक है (दूसरी [LeaseSet](#leaseset) है), और यह समाहित [RouterIdentity](#routeridentity) के SHA256 के अंतर्गत कीड किया गया है।

#### नोट्स

[RouterIdentity](#routeridentity) के बाद [Date](#date), जब प्रविष्टि प्रकाशित की गई थी

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### नोट्स

* बहुत पुराने routers के लिए addresses को उनके data के SHA256 के अनुसार क्रमबद्ध करना आवश्यक था
  ताकि signature अपरिवर्तनीय रहे।
  यह अब आवश्यक नहीं है, और backward compatibility के लिए इसे implement करना उपयुक्त नहीं है।

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* हस्ताक्षर को राउटर_आइडेंट की साइनिंग सार्वजनिक कुंजी का उपयोग करके सत्यापित किया जा सकता है।

* सभी राउटर जानकारी में मौजूद होने की उम्मीद वाले मानक विकल्पों के लिए नेटवर्क डेटाबेस पृष्ठ [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) देखें।

* बहुत पुराने राउटर्स के लिए उनके डेटा के SHA256 के अनुसार पतों को क्रमबद्ध करने की आवश्यकता थी,
  ताकि हस्ताक्षर अपरिवर्तित रहे।
  अब इसकी आवश्यकता नहीं है, और पुराने संस्करणों के साथ संगतता के लिए इसे लागू करना उचित नहीं है।

जावाडॉक: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### डिलीवरी निर्देश

टनल संदेश वितरण निर्देश [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions) में टनल संदेश विनिर्देश में परिभाषित किए गए हैं।

Garlic Message Delivery Instructions को I2NP Message Specification [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions) में परिभाषित किया गया है।

## संदर्भ

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
