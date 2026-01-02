---
title: "पोस्ट-क्वांटम क्रिप्टो प्रोटोकॉल"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "खुला"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## अवलोकन

जबकि उपयुक्त post-quantum (PQ) cryptography के लिए अनुसंधान और प्रतिस्पर्धा एक दशक से चल रही है, विकल्प हाल तक स्पष्ट नहीं हुए थे।

हमने 2022 में PQ crypto के निहितार्थों को देखना शुरू किया [zzz.i2p](http://zzz.i2p/topics/3294)।

TLS मानकों ने पिछले दो वर्षों में hybrid encryption सपोर्ट जोड़ा है और अब यह Chrome और Firefox में सपोर्ट के कारण इंटरनेट पर एन्क्रिप्टेड ट्रैफिक के एक महत्वपूर्ण हिस्से के लिए उपयोग किया जा रहा है [Cloudflare](https://blog.cloudflare.com/pq-2024/)।

NIST ने हाल ही में post-quantum cryptography के लिए अनुशंसित algorithms को अंतिम रूप दिया और प्रकाशित किया है [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)। कई सामान्य cryptography libraries अब NIST standards का समर्थन करती हैं या निकट भविष्य में समर्थन जारी करेंगी।

दोनों [Cloudflare](https://blog.cloudflare.com/pq-2024/) और [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) की सिफारिश है कि migration तुरंत शुरू हो। 2022 NSA PQ FAQ [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF) भी देखें। I2P को सुरक्षा और cryptography में अग्रणी होना चाहिए। अब सुझाए गए algorithms को implement करने का समय है। हमारे flexible crypto type और signature type system का उपयोग करके, हम hybrid crypto के लिए और PQ तथा hybrid signatures के लिए types जोड़ेंगे।

## लक्ष्य

- PQ-प्रतिरोधी एल्गोरिदम का चयन करें
- उपयुक्त स्थानों पर I2P प्रोटोकॉल में PQ-केवल और हाइब्रिड एल्गोरिदम जोड़ें
- कई वेरिएंट परिभाषित करें
- कार्यान्वयन, परीक्षण, विश्लेषण और अनुसंधान के बाद सर्वोत्तम वेरिएंट का चयन करें
- समर्थन को क्रमिक रूप से और पिछड़ी संगतता के साथ जोड़ें

## गैर-लक्ष्य

- एक-तरफा (Noise N) एन्क्रिप्शन प्रोटोकॉल को न बदलें
- SHA256 से दूर न जाएं, PQ द्वारा निकट-अवधि में खतरा नहीं है
- इस समय अंतिम पसंदीदा वेरिएंट्स का चयन न करें

## खतरा मॉडल

- OBEP या IBGW पर routers, संभावित रूप से मिलीभगत करके,
  बाद में डिक्रिप्शन के लिए garlic messages को संग्रहीत करना (forward secrecy)
- नेटवर्क observers
  बाद में डिक्रिप्शन के लिए transport messages को संग्रहीत करना (forward secrecy)
- नेटवर्क प्रतिभागी RI, LS, streaming, datagrams,
  या अन्य संरचनाओं के लिए signatures को जाली बनाना

## प्रभावित प्रोटोकॉल

हम निम्नलिखित प्रोटोकॉल को संशोधित करेंगे, लगभग विकास के क्रम में। समग्र rollout संभवतः 2025 के अंत से 2027 के मध्य तक होगा। विवरण के लिए नीचे Priorities और Rollout सेक्शन देखें।

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## डिज़ाइन

हम NIST FIPS 203 और 204 मानकों का समर्थन करेंगे [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) जो CRYSTALS-Kyber और CRYSTALS-Dilithium (संस्करण 3.1, 3, और पुराने) पर आधारित हैं, लेकिन उनके साथ संगत नहीं हैं।

### Key Exchange

हम निम्नलिखित प्रोटोकॉल में hybrid key exchange का समर्थन करेंगे:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM केवल ephemeral keys प्रदान करता है, और static-key handshakes जैसे कि Noise XK और IK का प्रत्यक्ष समर्थन नहीं करता है।

Noise N दो-तरफा key exchange का उपयोग नहीं करता है और इसलिए यह hybrid encryption के लिए उपयुक्त नहीं है।

इसलिए हम केवल hybrid encryption का समर्थन करेंगे, NTCP2, SSU2, और Ratchet के लिए। हम तीन ML-KEM variants को [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) के अनुसार परिभाषित करेंगे, कुल 3 नए encryption types के लिए। Hybrid types केवल X25519 के साथ संयोजन में परिभाषित किए जाएंगे।

नए एन्क्रिप्शन प्रकार हैं:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
ओवरहेड काफी अधिक होगा। वर्तमान में tipical message 1 और 2 के आकार (XK और IK के लिए) लगभग 100 bytes हैं (किसी भी अतिरिक्त payload से पहले)। यह algorithm के आधार पर 8x से 15x तक बढ़ेगा।

### Signatures

हम निम्नलिखित संरचनाओं में PQ और hybrid signatures का समर्थन करेंगे:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
इसलिए हम PQ-only और hybrid signatures दोनों को support करेंगे। हम तीन ML-DSA variants को [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) के अनुसार define करेंगे, Ed25519 के साथ तीन hybrid variants, और केवल SU3 files के लिए prehash के साथ तीन PQ-only variants, कुल मिलाकर 9 नए signature types। Hybrid types केवल Ed25519 के combination में define किए जाएंगे। हम standard ML-DSA का उपयोग करेंगे, pre-hash variants (HashML-DSA) का नहीं, SU3 files को छोड़कर।

हम "hedged" या randomized signing variant का उपयोग करेंगे, "deterministic" variant का नहीं, जैसा कि [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) section 3.4 में परिभाषित है। यह सुनिश्चित करता है कि प्रत्येक signature अलग हो, भले ही वह समान data पर हो, और side-channel attacks के विरुद्ध अतिरिक्त सुरक्षा प्रदान करता है। Algorithm choices जिसमें encoding और context शामिल हैं, के बारे में अतिरिक्त विवरण के लिए नीचे implementation notes section देखें।

नई signature types हैं:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
X.509 certificates और अन्य DER encodings composite structures और OIDs का उपयोग करेंगे जो [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) में परिभाषित हैं।

ओवरहेड काफी अधिक होगा। सामान्य Ed25519 destination और router identity का आकार 391 bytes है। एल्गोरिदम के आधार पर ये 3.5x से 6.8x तक बढ़ जाएंगे। Ed25519 signatures 64 bytes के होते हैं। एल्गोरिदम के आधार पर ये 38x से 76x तक बढ़ जाएंगे। सामान्य signed RouterInfo, LeaseSet, repliable datagrams, और signed streaming messages लगभग 1KB के होते हैं। एल्गोरिदम के आधार पर ये 3x से 8x तक बढ़ जाएंगे।

चूंकि नए destination और router identity types में padding नहीं होगी, वे compress नहीं हो सकेंगे। Destinations और router identities के sizes जो in-transit में gzip होते हैं, algorithm के आधार पर 12x - 38x तक बढ़ जाएंगे।

### Legal Combinations

Destinations के लिए, नए signature types को leaseset में सभी encryption types के साथ समर्थन प्राप्त है। key certificate में encryption type को NONE (255) पर सेट करें।

RouterIdentities के लिए, ElGamal encryption type deprecated है। नए signature types केवल X25519 (type 4) encryption के साथ समर्थित हैं। नए encryption types को RouterAddresses में इंगित किया जाएगा। Key certificate में encryption type type 4 ही रहेगा।

### New Crypto Required

- ML-KEM (पूर्व में CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (पूर्व में CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (पूर्व में Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) केवल SHAKE128 के लिए उपयोग किया जाता है
- SHA3-256 (पूर्व में Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 और SHAKE256 (SHA3-128 और SHA3-256 के लिए XOF विस्तार) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128, और SHAKE256 के लिए टेस्ट वेक्टर [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) पर उपलब्ध हैं।

ध्यान दें कि Java bouncycastle library उपरोक्त सभी का समर्थन करती है। C++ library का समर्थन OpenSSL 3.5 में है [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)।

### Alternatives

हम [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+) का समर्थन नहीं करेंगे, यह ML-DSA की तुलना में बहुत धीमा और बड़ा है। हम आगामी FIPS206 (Falcon) का समर्थन नहीं करेंगे, यह अभी तक मानकीकृत नहीं है। हम NTRU या अन्य PQ उम्मीदवारों का समर्थन नहीं करेंगे जो NIST द्वारा मानकीकृत नहीं किए गए हैं।

### Rosenpass

Wireguard (IK) को pure PQ crypto के लिए adapt करने पर कुछ research [paper](https://eprint.iacr.org/2020/379.pdf) है, लेकिन उस paper में कई open questions हैं। बाद में, इस approach को PQ Wireguard के लिए Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) के रूप में implement किया गया।

Rosenpass एक Noise KK-जैसे handshake का उपयोग करता है जिसमें preshared Classic McEliece 460896 static keys (प्रत्येक 500 KB) और Kyber-512 (मूल रूप से MLKEM-512) ephemeral keys होती हैं। चूंकि Classic McEliece ciphertexts केवल 188 bytes के होते हैं, और Kyber-512 public keys और ciphertexts उचित हैं, दोनों handshake संदेश एक मानक UDP MTU में फिट हो जाते हैं। PQ KK handshake से आउटपुट shared key (osk) का उपयोग मानक Wireguard IK handshake के लिए input preshared key (psk) के रूप में किया जाता है। इसलिए कुल मिलाकर दो पूर्ण handshakes होते हैं, एक शुद्ध PQ और एक शुद्ध X25519।

हम अपने XK और IK handshakes को replace करने के लिए इनमें से कुछ भी नहीं कर सकते क्योंकि:

- हम KK नहीं कर सकते, Bob के पास Alice की static key नहीं है
- 500KB static keys बहुत बड़ी हैं
- हम एक अतिरिक्त round-trip नहीं चाहते

whitepaper में बहुत सारी अच्छी जानकारी है, और हम इसे विचारों और प्रेरणा के लिए समीक्षा करेंगे। TODO।

## Specification

### Key Exchange

निम्नलिखित के अनुसार common structures दस्तावेज़ [/docs/specs/common-structures/](/docs/specs/common-structures/) में अनुभागों और तालिकाओं को अपडेट करें:

### हस्ताक्षर

नए Public Key प्रकार हैं:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
हाइब्रिड पब्लिक keys X25519 key हैं। KEM पब्लिक keys वे ephemeral PQ key हैं जो Alice से Bob को भेजी जाती हैं। Encoding और byte order [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित हैं।

MLKEM*_CT keys वास्तव में public keys नहीं हैं, ये Noise handshake में Bob से Alice को भेजे गए "ciphertext" हैं। इन्हें यहाँ पूर्णता के लिए सूचीबद्ध किया गया है।

### वैध संयोजन

नई Private Key types हैं:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Hybrid private keys X25519 keys हैं। KEM private keys केवल Alice के लिए हैं। KEM encoding और byte order [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित हैं।

### नया Crypto आवश्यक

नए Signing Public Key प्रकार हैं:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
हाइब्रिड साइनिंग पब्लिक keys Ed25519 key के बाद PQ key होती हैं, जैसा कि [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) में है। एन्कोडिंग और बाइट ऑर्डर [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) में परिभाषित हैं।

### विकल्प

नए Signing Private Key प्रकार हैं:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
हाइब्रिड साइनिंग प्राइवेट keys Ed25519 key के बाद PQ key होती हैं, जैसा कि [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) में दिया गया है। एन्कोडिंग और byte order [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) में परिभाषित हैं।

### Rosenpass

नए Signature प्रकार हैं:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
हाइब्रिड सिग्नेचर Ed25519 सिग्नेचर के बाद PQ सिग्नेचर होते हैं, जैसा कि [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) में है। हाइब्रिड सिग्नेचर को दोनों सिग्नेचर की जांच करके वेरिफाई किया जाता है, और यदि कोई भी एक फेल हो जाता है तो यह फेल हो जाता है। एन्कोडिंग और बाइट ऑर्डर [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) में परिभाषित हैं।

### Key Certificates

नए Signing Public Key प्रकार हैं:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
नए Crypto Public Key प्रकार हैं:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
हाइब्रिड key types कभी भी key certificates में शामिल नहीं होते हैं; केवल leasesets में होते हैं।

Hybrid या PQ signature प्रकार वाले destinations के लिए, encryption प्रकार के लिए NONE (type 255) का उपयोग करें, लेकिन कोई crypto key नहीं है, और पूरा 384-byte main section signing key के लिए है।

### सामान्य संरचनाएं

यहाँ नए Destination प्रकारों के लिए लंबाइयाँ हैं। सभी के लिए Enc type NONE (type 255) है और encryption key length को 0 माना जाता है। पूरा 384-byte section signing public key के पहले भाग के लिए उपयोग किया जाता है। नोट: यह ECDSA_SHA512_P521 और RSA signature types के spec से अलग है, जहाँ हमने destination में 256-byte ElGamal key को बनाए रखा था भले ही वह अनुपयोगी था।

कोई padding नहीं। कुल लंबाई 7 + कुल key लंबाई है। Key certificate लंबाई 4 + अतिरिक्त key लंबाई है।

MLDSA44 के लिए उदाहरण 1319-byte destination byte stream:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

यहाँ नए Destination प्रकारों की लंबाई दी गई है। सभी के लिए Enc type X25519 (type 4) है। X28819 public key के बाद पूरा 352-byte सेक्शन signing public key के पहले भाग के लिए उपयोग होता है। कोई padding नहीं। कुल लंबाई 39 + total key length है। Key certificate length 4 + excess key length है।

MLDSA44 के लिए उदाहरण 1351-बाइट router identity बाइट स्ट्रीम:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

हैंडशेक [Noise Protocol](https://noiseprotocol.org/noise.html) हैंडशेक पैटर्न का उपयोग करते हैं।

निम्नलिखित अक्षर मैपिंग का उपयोग किया जाता है:

- e = एक-बार का ephemeral key
- s = static key
- p = message payload
- e1 = एक-बार का ephemeral PQ key, Alice से Bob को भेजा गया
- ekem1 = KEM ciphertext, Bob से Alice को भेजा गया

hybrid forward secrecy (hfs) के लिए XK और IK में निम्नलिखित संशोधन [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 5 में निर्दिष्ट अनुसार हैं:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 pattern निम्नलिखित रूप में परिभाषित है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) के खंड 4 में निर्दिष्ट है:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 pattern निम्नलिखित रूप में परिभाषित है, जैसा कि [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4 में निर्दिष्ट है:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- क्या हमें handshake hash function को बदलना चाहिए? देखें [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)।
  SHA256 PQ के लिए vulnerable नहीं है, लेकिन यदि हम अपने hash function को upgrade करना चाहते हैं, तो अभी समय है, जबकि हम अन्य चीजों को बदल रहे हैं।
  वर्तमान IETF SSH proposal [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) MLKEM768
  को SHA256 के साथ, और MLKEM1024 को SHA384 के साथ उपयोग करने का है। उस proposal में
  security considerations की चर्चा शामिल है।
- क्या हमें 0-RTT ratchet data भेजना बंद कर देना चाहिए (LS के अलावा)?
- यदि हम 0-RTT data नहीं भेजते हैं तो क्या हमें ratchet को IK से XK में बदल देना चाहिए?

#### Overview

यह अनुभाग IK और XK दोनों protocols पर लागू होता है।

hybrid handshake [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) में परिभाषित है। पहला संदेश, Alice से Bob को, message payload से पहले e1, encapsulation key को शामिल करता है। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() (Alice के रूप में) या DecryptAndHash() (Bob के रूप में) को call करें। फिर message payload को सामान्य रूप से process करें।

दूसरा संदेश, Bob से Alice तक, में ekem1, ciphertext शामिल है, message payload से पहले। इसे एक अतिरिक्त static key के रूप में माना जाता है; इस पर EncryptAndHash() को call करें (Bob के रूप में) या DecryptAndHash() (Alice के रूप में)। फिर, kem_shared_key की गणना करें और MixKey(kem_shared_key) को call करें। फिर message payload को सामान्य रूप से process करें।

#### Defined ML-KEM Operations

हम निम्नलिखित functions को define करते हैं जो cryptographic building blocks के अनुरूप हैं जैसा कि [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) में परिभाषित किया गया है।

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

ध्यान दें कि encap_key और ciphertext दोनों ही Noise handshake messages 1 और 2 में ChaCha/Poly blocks के अंदर encrypted हैं। ये handshake process के हिस्से के रूप में decrypt हो जाएंगे।

kem_shared_key को chaining key के साथ MixHash() का उपयोग करके मिलाया जाता है। विवरण के लिए नीचे देखें।

#### Alice KDF for Message 1

XK के लिए: 'es' message pattern के बाद और payload से पहले, जोड़ें:

या

IK के लिए: 'es' message pattern के बाद और 's' message pattern से पहले, जोड़ें:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

XK के लिए: 'es' message pattern के बाद और payload से पहले, जोड़ें:

या

IK के लिए: 'es' message pattern के बाद और 's' message pattern से पहले, जोड़ें:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

XK के लिए: 'ee' message pattern के बाद और payload से पहले, जोड़ें:

या

IK के लिए: 'ee' message pattern के बाद और 'se' message pattern से पहले, जोड़ें:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

'ee' संदेश पैटर्न के बाद (और IK के लिए 'ss' संदेश पैटर्न से पहले), जोड़ें:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

अपरिवर्तित

#### KDF for split()

अपरिवर्तित

### SigningPrivateKey

ECIES-Ratchet specification [/docs/specs/ecies/](/docs/specs/ecies/) को निम्नलिखित के अनुसार अपडेट करें:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

परिवर्तन: वर्तमान ratchet में पहले ChaCha सेक्शन में static key शामिल थी, और दूसरे सेक्शन में payload था। ML-KEM के साथ, अब तीन सेक्शन हैं। पहले सेक्शन में encrypted PQ public key है। दूसरे सेक्शन में static key है। तीसरे सेक्शन में payload है।

एन्क्रिप्टेड प्रारूप:

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
डिक्रिप्ट किया गया प्रारूप:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
आकार:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
ध्यान दें कि payload में एक DateTime block होना आवश्यक है, इसलिए न्यूनतम payload का आकार 7 है। न्यूनतम message 1 के आकार की गणना तदनुसार की जा सकती है।

#### 1g) New Session Reply format

परिवर्तन: वर्तमान ratchet में पहले ChaCha सेक्शन के लिए एक खाली payload है, और दूसरे सेक्शन में payload है। ML-KEM के साथ, अब तीन सेक्शन हैं। पहले सेक्शन में encrypted PQ ciphertext है। दूसरे सेक्शन में खाली payload है। तीसरे सेक्शन में payload है।

एन्क्रिप्टेड प्रारूप:

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
डिक्रिप्टेड प्रारूप:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
आकार:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
ध्यान दें कि जबकि message 2 में सामान्यतः एक nonzero payload होगा, ratchet specification [/docs/specs/ecies/](/docs/specs/ecies/) इसकी आवश्यकता नहीं करता, इसलिए न्यूनतम payload size 0 है। न्यूनतम message 2 sizes की तदनुसार गणना की जा सकती है।

### हस्ताक्षर

NTCP2 specification [/docs/specs/ntcp2/](/docs/specs/ntcp2/) को निम्नलिखित के अनुसार अपडेट करें:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

परिवर्तन: वर्तमान NTCP2 में केवल ChaCha अनुभाग के विकल्प शामिल हैं। ML-KEM के साथ, ChaCha अनुभाग में एन्क्रिप्टेड PQ पब्लिक की भी शामिल होगी।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
अनएन्क्रिप्टेड डेटा (Poly1305 प्रमाणीकरण टैग दिखाया नहीं गया):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
आकार:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Routers type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

#### 2) SessionCreated

परिवर्तन: वर्तमान NTCP2 में केवल ChaCha सेक्शन के विकल्प हैं। ML-KEM के साथ, ChaCha सेक्शन में एन्क्रिप्टेड PQ पब्लिक key भी होगी।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
अनएन्क्रिप्टेड डेटा (Poly1305 auth tag दिखाया नहीं गया):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
आकार:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
नोट: टाइप कोड केवल आंतरिक उपयोग के लिए हैं। Router टाइप 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

#### 3) SessionConfirmed

अपरिवर्तित

#### Key Derivation Function (KDF) (for data phase)

अपरिवर्तित

### मुख्य प्रमाणपत्र

SSU2 specification [/docs/specs/ssu2/](/docs/specs/ssu2/) को निम्नलिखित के अनुसार अपडेट करें:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

लंबा header 32 bytes का होता है। यह session बनने से पहले उपयोग किया जाता है, Token Request, SessionRequest, SessionCreated, और Retry के लिए। यह out-of-session Peer Test और Hole Punch messages के लिए भी उपयोग किया जाता है।

TODO: हम आंतरिक रूप से version field का उपयोग कर सकते हैं और MLKEM512 के लिए 3 और MLKEM768 के लिए 4 का उपयोग कर सकते हैं। क्या हम यह केवल types 0 और 1 के लिए करते हैं या सभी 6 types के लिए?

header encryption से पहले:

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

अपरिवर्तित

#### SessionRequest (Type 0)

परिवर्तन: वर्तमान SSU2 में ChaCha सेक्शन में केवल block data होता है। ML-KEM के साथ, ChaCha सेक्शन में encrypted PQ public key भी शामिल होगी।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
अनएन्क्रिप्टेड डेटा (Poly1305 authentication tag दिखाया नहीं गया):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
आकार, IP overhead शामिल नहीं:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
नोट: प्रकार कोड केवल आंतरिक उपयोग के लिए हैं। Router प्रकार 4 ही रहेंगे, और समर्थन router पतों में दर्शाया जाएगा।

MLKEM768_X25519 के लिए न्यूनतम MTU: IPv4 के लिए लगभग 1316 और IPv6 के लिए 1336।

#### SessionCreated (Type 1)

परिवर्तन: वर्तमान SSU2 में ChaCha अनुभाग में केवल ब्लॉक डेटा शामिल है। ML-KEM के साथ, ChaCha अनुभाग में एन्क्रिप्टेड PQ public key भी शामिल होगी।

कच्ची सामग्री:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
अनएन्क्रिप्टेड डेटा (Poly1305 auth tag दिखाया नहीं गया):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
आकार, IP overhead को शामिल नहीं करते हुए:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Router type 4 ही रहेंगे, और support को router addresses में दर्शाया जाएगा।

MLKEM768_X25519 के लिए न्यूनतम MTU: IPv4 के लिए लगभग 1316 और IPv6 के लिए 1336।

#### SessionConfirmed (Type 2)

अपरिवर्तित

#### KDF for data phase

अपरिवर्तित

#### समस्याएं

Relay blocks, Peer Test blocks, और Peer Test messages सभी में signatures होते हैं। दुर्भाग्य से, PQ signatures MTU से बड़े होते हैं। वर्तमान में Relay या Peer Test blocks या messages को कई UDP packets में fragment करने का कोई तंत्र नहीं है। protocol को fragmentation को support करने के लिए बढ़ाना होगा। यह एक अलग proposal TBD में किया जाएगा। जब तक यह पूरा नहीं हो जाता, Relay और Peer Test को support नहीं किया जाएगा।

#### अवलोकन

हम आंतरिक रूप से version field का उपयोग कर सकते हैं और MLKEM512 के लिए 3 तथा MLKEM768 के लिए 4 का उपयोग कर सकते हैं।

संदेश 1 और 2 के लिए, MLKEM768 पैकेट आकार को 1280 न्यूनतम MTU से अधिक बढ़ा देगा। संभावित रूप से यदि MTU बहुत कम होता तो उस कनेक्शन के लिए इसे समर्थित ही नहीं करते।

संदेश 1 और 2 के लिए, MLKEM1024 पैकेट आकार को 1500 अधिकतम MTU से बढ़ा देगा। इसके लिए संदेश 1 और 2 को विखंडित करना होगा, और यह एक बड़ी जटिलता होगी। शायद ऐसा नहीं करेंगे।

रिले और पीयर टेस्ट: ऊपर देखें

### गंतव्य आकार

TODO: क्या signature को copy करने से बचने के लिए signing/verification को define करने का कोई अधिक efficient तरीका है?

### RouterIdent आकार

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) सेक्शन 8.1 X.509 प्रमाणपत्रों में HashML-DSA को अनुमति नहीं देता है और implementation की जटिलताओं और कम सुरक्षा के कारण HashML-DSA के लिए OIDs असाइन नहीं करता है।

SU3 फ़ाइलों के PQ-only signatures के लिए, certificates के लिए non-prehash variants के [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) में परिभाषित OIDs का उपयोग करें। हम SU3 फ़ाइलों के hybrid signatures को परिभाषित नहीं करते हैं, क्योंकि हमें फ़ाइलों को दो बार hash करना पड़ सकता है (हालांकि HashML-DSA और X2559 समान hash function SHA512 का उपयोग करते हैं)। इसके अलावा, X.509 certificate में दो keys और signatures को concatenate करना पूर्णतः nonstandard होगा।

ध्यान दें कि हम SU3 फाइलों के Ed25519 signing की अनुमति नहीं देते हैं, और जबकि हमने Ed25519ph signing को परिभाषित किया है, हमने कभी भी इसके लिए OID पर सहमति नहीं बनाई है, या इसका उपयोग नहीं किया है।

SU3 फ़ाइलों के लिए सामान्य sig types की अनुमति नहीं है; ph (prehash) variants का उपयोग करें।

### Handshake Patterns

नया अधिकतम Destination साइज़ 2599 होगा (base 64 में 3468)।

Destination आकारों पर मार्गदर्शन देने वाले अन्य दस्तावेजों को अपडेट करें, जिनमें शामिल हैं:

- SAMv3
- Bittorrent
- डेवलपर दिशानिर्देश
- नामकरण / पता पुस्तिका / जंप सर्वर
- अन्य दस्तावेज़

## Overhead Analysis

### Noise Handshake KDF

आकार वृद्धि (bytes):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
गति:

[Cloudflare](https://blog.cloudflare.com/pq-2024/) द्वारा रिपोर्ट की गई गति:

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Java में प्रारंभिक परीक्षण परिणाम:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

आकार:

विशिष्ट key, sig, RIdent, Dest आकार या आकार वृद्धि (Ed25519 संदर्भ के लिए शामिल) RIs के लिए X25519 encryption प्रकार मानते हुए। Router Info, LeaseSet, repliable datagrams, और दोनों streaming (SYN और SYN ACK) packets में से प्रत्येक के लिए सूचीबद्ध अतिरिक्त आकार। वर्तमान Destinations और Leasesets में repeated padding होता है और ये in-transit संपीड़ित हो सकते हैं। नए प्रकारों में padding नहीं होता और ये संपीड़ित नहीं होंगे, जिसके परिणामस्वरूप in-transit बहुत अधिक आकार वृद्धि होगी। ऊपर design खंड देखें।

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
गति:

[Cloudflare](https://blog.cloudflare.com/pq-2024/) द्वारा रिपोर्ट की गई गति:

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Java में प्रारंभिक परीक्षण परिणाम:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

NIST सुरक्षा श्रेणियां [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) स्लाइड 10 में संक्षेप में दी गई हैं। प्रारंभिक मानदंड: hybrid protocols के लिए हमारी न्यूनतम NIST सुरक्षा श्रेणी 2 होनी चाहिए और PQ-only के लिए 3।

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

ये सभी hybrid protocols हैं। संभवतः MLKEM768 को प्राथमिकता देनी चाहिए; MLKEM512 पर्याप्त सुरक्षित नहीं है।

NIST सुरक्षा श्रेणियां [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

यह प्रस्ताव hybrid और PQ-only दोनों signature types को परिभाषित करता है। MLDSA44 hybrid, MLDSA65 PQ-only की तुलना में बेहतर है। MLDSA65 और MLDSA87 के लिए keys और sig sizes शायद हमारे लिए बहुत बड़े हैं, कम से कम शुरुआत में।

NIST सुरक्षा श्रेणियां [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

जबकि हम 3 crypto और 9 signature types को परिभाषित और कार्यान्वित करेंगे, हम विकास के दौरान प्रदर्शन को मापने की योजना बना रहे हैं, और बढ़े हुए structure sizes के प्रभावों का और विश्लेषण करेंगे। हम अन्य projects और protocols में developments पर अनुसंधान और निगरानी भी जारी रखेंगे।

एक वर्ष या अधिक के विकास के बाद हम प्रत्येक उपयोग के मामले के लिए एक पसंदीदा प्रकार या डिफ़ॉल्ट पर निर्णय लेने का प्रयास करेंगे। चयन के लिए bandwidth, CPU, और अनुमानित सुरक्षा स्तर के बीच समझौता करना आवश्यक होगा। सभी प्रकार सभी उपयोग के मामलों के लिए उपयुक्त या अनुमतित नहीं हो सकते हैं।

प्रारंभिक प्राथमिकताएं निम्नलिखित हैं, जो परिवर्तन के अधीन हैं:

एन्क्रिप्शन: MLKEM768_X25519

हस्ताक्षर: MLDSA44_EdDSA_SHA512_Ed25519

प्रारंभिक प्रतिबंध निम्नलिखित हैं, जो परिवर्तन के अधीन हैं:

एन्क्रिप्शन: MLKEM1024_X25519 SSU2 के लिए अनुमतित नहीं है

Signatures: MLDSA87 और hybrid variant संभवतः बहुत बड़े हैं; MLDSA65 और hybrid variant बहुत बड़े हो सकते हैं

## Implementation Notes

### Library Support

Bouncycastle, BoringSSL, और WolfSSL libraries अब MLKEM और MLDSA को support करती हैं। OpenSSL support उनकी 3.5 release में 8 अप्रैल, 2025 को होगी [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)।

Java I2P द्वारा अनुकूलित southernstorm.com Noise library में hybrid handshakes के लिए प्रारंभिक समर्थन था, लेकिन हमने इसे अनुपयोगी होने के कारण हटा दिया; हमें इसे वापस जोड़ना होगा और [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) के अनुसार इसे अपडेट करना होगा।

### Signing Variants

हम [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) सेक्शन 3.4 में परिभाषित "hedged" या randomized signing वेरिएंट का उपयोग करेंगे, "determinstic" वेरिएंट का नहीं। यह सुनिश्चित करता है कि प्रत्येक signature अलग हो, यहाँ तक कि समान डेटा पर भी, और side-channel attacks के विरुद्ध अतिरिक्त सुरक्षा प्रदान करता है। जबकि [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) निर्दिष्ट करता है कि "hedged" वेरिएंट डिफ़ॉल्ट है, यह विभिन्न libraries में सत्य हो भी सकता है या नहीं भी। Implementors को यह सुनिश्चित करना चाहिए कि signing के लिए "hedged" वेरिएंट का उपयोग हो।

हम सामान्य signing प्रक्रिया (जिसे Pure ML-DSA Signature Generation कहा जाता है) का उपयोग करते हैं जो message को आंतरिक रूप से 0x00 || len(ctx) || ctx || message के रूप में encode करती है, जहाँ ctx कुछ वैकल्पिक मान है जिसका आकार 0x00..0xFF है। हम किसी वैकल्पिक context का उपयोग नहीं कर रहे हैं। len(ctx) == 0। यह प्रक्रिया [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10 और Algorithm 3 step 5 में परिभाषित है। ध्यान दें कि कुछ प्रकाशित test vectors में एक ऐसा mode सेट करना आवश्यक हो सकता है जहाँ message को encode नहीं किया जाता।

### Reliability

साइज़ बढ़ने से NetDB stores, streaming handshakes, और अन्य messages के लिए बहुत अधिक tunnel fragmentation होगी। performance और reliability में बदलाव के लिए जाँच करें।

### Structure Sizes

router infos और leasesets के byte size को सीमित करने वाले किसी भी code को खोजें और जांचें।

### NetDB

RAM या disk में संग्रहीत अधिकतम LS/RI की समीक्षा करें और संभवतः कम करें, storage वृद्धि को सीमित करने के लिए। floodfills के लिए न्यूनतम bandwidth आवश्यकताओं को बढ़ाएं?

### Ratchet

#### परिभाषित ML-KEM Operations

एक ही tunnel पर कई protocols का auto-classify/detect संभव होना चाहिए message 1 (New Session Message) की length check के आधार पर। MLKEM512_X25519 को उदाहरण के रूप में उपयोग करते हुए, message 1 की length वर्तमान ratchet protocol से 816 bytes बड़ी है, और न्यूनतम message 1 size (केवल DateTime payload के साथ) 919 bytes है। वर्तमान ratchet के साथ अधिकांश message 1 sizes में 816 bytes से कम payload होता है, इसलिए उन्हें non-hybrid ratchet के रूप में classify किया जा सकता है। बड़े messages संभवतः POSTs हैं जो दुर्लभ हैं।

अतः अनुशंसित रणनीति है:

- यदि संदेश 1 919 बाइट्स से कम है, तो यह वर्तमान ratchet प्रोटोकॉल है।
- यदि संदेश 1 919 बाइट्स से अधिक या बराबर है, तो यह संभवतः MLKEM512_X25519 है।
  पहले MLKEM512_X25519 को आज़माएं, और यदि यह विफल हो जाता है, तो वर्तमान ratchet प्रोटोकॉल को आज़माएं।

यह हमें समान destination पर standard ratchet और hybrid ratchet को कुशलतापूर्वक support करने की अनुमति देगा, जैसा कि हमने पहले समान destination पर ElGamal और ratchet को support किया था। इसलिए, हम MLKEM hybrid protocol में बहुत तेज़ी से migrate कर सकते हैं, यदि हम समान destination के लिए dual-protocols को support नहीं कर सकते तो जितनी तेज़ी से कर सकते थे उससे कहीं अधिक तेज़ी से, क्योंकि हम existing destinations में MLKEM support जोड़ सकते हैं।

आवश्यक समर्थित संयोजन हैं:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

निम्नलिखित संयोजन जटिल हो सकते हैं, और इनका समर्थन किया जाना आवश्यक नहीं है, लेकिन हो सकता है, implementation-dependent:

- एक से अधिक MLKEM
- ElG + एक या अधिक MLKEM
- X25519 + एक या अधिक MLKEM
- ElG + X25519 + एक या अधिक MLKEM

हमें एक ही destination पर कई MLKEM algorithms (उदाहरण के लिए, MLKEM512_X25519 और MLKEM_768_X25519) को support करने का प्रयास नहीं करना चाहिए। केवल एक को चुनें; हालांकि, यह हमारे द्वारा एक preferred MLKEM variant का चयन करने पर निर्भर करता है, ताकि HTTP client tunnels एक का उपयोग कर सकें। Implementation-dependent।

हम एक ही destination पर तीन algorithms का समर्थन करने का प्रयास कर सकते हैं (उदाहरण के लिए X25519, MLKEM512_X25519, और MLKEM769_X25519)। classification और retry strategy बहुत जटिल हो सकती है। configuration और configuration UI बहुत जटिल हो सकता है। Implementation-dependent।

हम संभवतः एक ही destination पर ElGamal और hybrid algorithms दोनों को support करने का प्रयास नहीं करेंगे। ElGamal अप्रचलित है, और ElGamal + hybrid only (कोई X25519 नहीं) का अधिक अर्थ नहीं है। साथ ही, ElGamal और Hybrid New Session Messages दोनों बड़े होते हैं, इसलिए classification strategies को अक्सर दोनों decryptions को आजमाना पड़ेगा, जो अक्षम होगा। Implementation-dependent।

क्लाइंट्स समान टनल्स पर X25519 और hybrid protocols के लिए समान या अलग X25519 static keys का उपयोग कर सकते हैं, यह implementation-dependent होता है।

#### Message 1 के लिए Alice KDF

ECIES विशिष्टता New Session Message payload में Garlic Messages की अनुमति देती है, जो प्रारंभिक streaming packet के 0-RTT delivery की सुविधा प्रदान करती है, आमतौर पर HTTP GET, client के leaseset के साथ। हालांकि, New Session Message payload में forward secrecy नहीं होती। चूंकि यह प्रस्ताव ratchet के लिए बेहतर forward secrecy पर जोर दे रहा है, implementations को streaming payload, या पूर्ण streaming message को शामिल करने में देरी करनी चाहिए, पहले Existing Session Message तक। यह 0-RTT delivery की कीमत पर होगा। रणनीतियां traffic type या tunnel type पर भी निर्भर हो सकती हैं, या उदाहरण के लिए GET vs. POST पर। Implementation-dependent।

#### Message 1 के लिए Bob KDF

MLKEM, MLDSA, या दोनों एक ही destination पर, New Session Message के आकार को नाटकीय रूप से बढ़ा देंगे, जैसा कि ऊपर वर्णित है। यह tunnels के माध्यम से New Session Message delivery की विश्वसनीयता को महत्वपूर्ण रूप से कम कर सकता है, जहाँ उन्हें कई 1024 बाइट tunnel messages में विभाजित करना पड़ता है। Delivery की सफलता fragments की घातीय संख्या के अनुपातिक है। Implementations विभिन्न रणनीतियों का उपयोग करके message के आकार को सीमित कर सकते हैं, 0-RTT delivery की हानि के साथ। Implementation-dependent।

### Ratchet

हम session request में ephemeral key (key[31] & 0x80) का MSB set कर सकते हैं यह indicate करने के लिए कि यह एक hybrid connection है। यह हमें same port पर standard NTCP और hybrid NTCP दोनों run करने की अनुमति देगा। केवल एक hybrid variant को support किया जाएगा, और router address में advertise किया जाएगा। उदाहरण के लिए, v=2,3 या v=2,4 या v=2,5।

यदि हम ऐसा नहीं करते हैं, तो हमें अलग transport address/port की आवश्यकता होगी, और एक नया protocol name जैसे "NTCP1PQ1"।

नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Routers type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

करना है

### SSU2

MAY को अलग transport address/port की आवश्यकता हो सकती है, लेकिन उम्मीद है कि नहीं, हमारे पास message 1 के लिए flags के साथ एक header है। हम आंतरिक रूप से version field का उपयोग कर सकते हैं और MLKEM512 के लिए 3 और MLKEM768 के लिए 4 का उपयोग कर सकते हैं। शायद address में केवल v=2,3,4 पर्याप्त होगा। लेकिन हमें दोनों नए algorithms के लिए identifiers की आवश्यकता है: 3a, 3b?

जांचें और सत्यापित करें कि SSU2 कई packets में विभाजित RI को handle कर सकता है (6-8?)। i2pd वर्तमान में केवल अधिकतम 2 fragments का समर्थन करता है?

नोट: Type codes केवल आंतरिक उपयोग के लिए हैं। Routers type 4 ही रहेंगे, और समर्थन router addresses में दर्शाया जाएगा।

TODO

## Router Compatibility

### Transport Names

हमें संभवतः नए transport names की आवश्यकता नहीं होगी, यदि हम version flags के साथ same port पर standard और hybrid दोनों को चला सकते हैं।

यदि हमें नए transport names की आवश्यकता है, तो वे होंगे:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
ध्यान दें कि SSU2 MLKEM1024 को सपोर्ट नहीं कर सकता, यह बहुत बड़ा है।

### Router Enc. Types

हमारे पास विचार करने के लिए कई विकल्प हैं:

#### Bob KDF संदेश 2 के लिए

अनुशंसित नहीं। केवल उपरोक्त सूचीबद्ध नए transports का उपयोग करें जो router प्रकार से मेल खाते हैं। पुराने routers कनेक्ट नहीं कर सकते, इसके माध्यम से tunnels नहीं बना सकते, या netdb संदेश नहीं भेज सकते। डिफ़ॉल्ट रूप से सक्षम करने से पहले debug करने और समर्थन सुनिश्चित करने में कई release cycles लगेंगे। नीचे दिए गए विकल्पों की तुलना में rollout को एक साल या अधिक समय तक बढ़ा सकता है।

#### Message 2 के लिए Alice KDF

अनुशंसित। चूंकि PQ X25519 static key या N handshake protocols को प्रभावित नहीं करता है, हम routers को type 4 के रूप में छोड़ सकते हैं, और केवल नए transports का विज्ञापन कर सकते हैं। पुराने routers अभी भी connect कर सकते हैं, tunnels बना सकते हैं, या netDb messages भेज सकते हैं।

#### Message 3 के लिए KDF (केवल XK)

Type 4 routers दोनों NTCP2 और NTCP2PQ* addresses का विज्ञापन कर सकते हैं। ये समान static key और अन्य parameters का उपयोग कर सकते हैं, या नहीं भी। इन्हें संभवतः अलग-अलग ports पर होना होगा; एक ही port पर NTCP2 और NTCP2PQ* दोनों protocols को support करना बहुत कठिन होगा, क्योंकि कोई header या framing नहीं है जो Bob को आने वाले Session Request message को classify और frame करने की अनुमति दे सके।

अलग ports और addresses Java के लिए कठिन होंगे लेकिन i2pd के लिए सीधे होंगे।

#### split() के लिए KDF

Type 4 routers दोनों SSU2 और SSU2PQ* addresses का विज्ञापन कर सकते हैं। अतिरिक्त header flags के साथ, Bob पहले संदेश में आने वाले transport type की पहचान कर सकता है। इसलिए, हम एक ही port पर दोनों SSU2 और SSUPQ* का समर्थन कर सकते हैं।

ये अलग पतों के रूप में प्रकाशित किए जा सकते हैं (जैसा कि i2pd ने पिछले transitions में किया है) या उसी पते में एक parameter के साथ जो PQ support को दर्शाता है (जैसा कि Java i2p ने पिछले transitions में किया है)।

यदि समान पते में, या अलग पतों में समान port पर, तो ये समान static key और अन्य parameters का उपयोग करेंगे। यदि अलग पतों में अलग ports के साथ, तो ये समान static key और अन्य parameters का उपयोग कर सकते हैं, या नहीं भी।

अलग ports और addresses Java के लिए कठिन होंगे लेकिन i2pd के लिए सीधे होंगे।

#### Recommendations

करने के लिए

### NTCP2

#### Noise पहचानकर्ता

पुराने router RIs को verify करते हैं और इसलिए connect नहीं कर सकते, इनके through tunnel नहीं बना सकते, या इन्हें netDb messages नहीं भेज सकते। Default से enable करने से पहले debug करने और support ensure करने में कई release cycles लगेंगे। यही issues होंगे जो enc. type 5/6/7 rollout में थे; ऊपर listed type 4 enc. type rollout alternative की तुलना में rollout को एक साल या अधिक extend कर सकता है।

कोई विकल्प नहीं।

### LS Enc. Types

#### 1b) नया session format (binding के साथ)

ये पुराने type 4 X25519 keys के साथ LS में मौजूद हो सकते हैं। पुराने router अज्ञात keys को ignore कर देंगे।

Destinations कई key types का समर्थन कर सकते हैं, लेकिन केवल प्रत्येक key के साथ message 1 के trial decrypts करके। Overhead को प्रत्येक key के लिए successful decrypts की counts बनाए रखकर और सबसे अधिक उपयोग की जाने वाली key को पहले try करके कम किया जा सकता है। Java I2P समान destination पर ElGamal+X25519 के लिए इस strategy का उपयोग करता है।

### Dest. Sig. Types

#### 1g) नया Session Reply प्रारूप

Router leaseSet हस्ताक्षरों को सत्यापित करते हैं और इसलिए type 12-17 destinations के लिए कनेक्ट नहीं हो सकते या leaseSet प्राप्त नहीं कर सकते। डिफ़ॉल्ट रूप से सक्षम करने से पहले समर्थन को डिबग और सुनिश्चित करने के लिए कई release cycles लगेंगे।

कोई विकल्प नहीं।

## विनिर्देश

सबसे मूल्यवान डेटा end-to-end traffic है, जो ratchet के साथ encrypted है। tunnel hops के बीच एक external observer के रूप में, यह दो बार और encrypted है, tunnel encryption और transport encryption के साथ। OBEP और IBGW के बीच एक external observer के रूप में, यह केवल एक बार और encrypted है, transport encryption के साथ। एक OBEP या IBGW participant के रूप में, ratchet ही एकमात्र encryption है। हालांकि, चूंकि tunnels unidirectional हैं, ratchet handshake में दोनों messages को capture करने के लिए colluding routers की आवश्यकता होगी, जब तक कि tunnels को same router पर OBEP और IBGW के साथ नहीं बनाया गया हो।

फिलहाल सबसे चिंताजनक PQ threat model यह है कि आज के ट्रैफिक को स्टोर करना, और कई सालों बाद इसे decrypt करना (forward secrecy)। एक hybrid approach इससे सुरक्षा प्रदान करेगा।

PQ threat model जो authentication keys को कुछ उचित समय अवधि में (जैसे कुछ महीनों में) तोड़ने और फिर authentication का impersonation करने या लगभग real-time में decrypt करने का है, वह बहुत दूर है? और तभी हमें PQC static keys पर migrate करना होगा।

इसलिए, सबसे पहला PQ threat model OBEP/IBGW का ट्रैफिक को बाद में decryption के लिए स्टोर करना है। हमें पहले hybrid ratchet implement करना चाहिए।

Ratchet सबसे उच्च प्राथमिकता है। Transports अगली हैं। Signatures सबसे कम प्राथमिकता हैं।

Signature rollout भी encryption rollout से एक साल या अधिक बाद होगा, क्योंकि कोई backward compatibility संभव नहीं है। साथ ही, उद्योग में MLDSA adoption को CA/Browser Forum और Certificate Authorities द्वारा मानकीकृत किया जाएगा। CAs को पहले hardware security module (HSM) support की आवश्यकता है, जो वर्तमान में उपलब्ध नहीं है [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)। हम उम्मीद करते हैं कि CA/Browser Forum विशिष्ट parameter choices पर निर्णयों को आगे बढ़ाएगा, जिसमें composite signatures को समर्थन देना या आवश्यक बनाना शामिल है [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)।

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

यदि हम एक ही tunnels पर पुराने और नए ratchet protocols दोनों का समर्थन नहीं कर सकते, तो migration बहुत अधिक कठिन होगा।

हमें बस एक-के-बाद-दूसरे को आज़माने में सक्षम होना चाहिए, जैसा कि हमने X25519 के साथ किया था, सिद्ध होने के लिए।

## Issues

- Noise Hash चयन - SHA256 के साथ बने रहें या अपग्रेड करें?
  SHA256 अगले 20-30 वर्षों के लिए अच्छा होना चाहिए, PQ द्वारा खतरा नहीं,
  देखें [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) और [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)।
  यदि SHA256 टूट जाता है तो हमारी और भी बुरी समस्याएं हैं (netdb)।
- NTCP2 अलग पोर्ट, अलग router पता
- SSU2 relay / peer test
- SSU2 version फील्ड
- SSU2 router पता version
