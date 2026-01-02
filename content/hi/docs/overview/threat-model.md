---
title: "I2P खतरा मॉडल"
description: "I2P के डिज़ाइन में विचार किए गए हमलों की सूची और लागू की गई सुरक्षा उपाय"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. "Anonymous" का अर्थ क्या है

I2P *व्यावहारिक गुमनामी* प्रदान करता है—अदृश्यता नहीं। गुमनामी को इस रूप में परिभाषित किया जाता है कि किसी विरोधी के लिए उस जानकारी को जानना कितना कठिन है जिसे आप निजी रखना चाहते हैं: आप कौन हैं, आप कहाँ हैं, या आप किससे बात करते हैं। पूर्ण गुमनामी असंभव है; इसके बजाय, I2P का लक्ष्य वैश्विक निष्क्रिय और सक्रिय विरोधियों के खिलाफ **पर्याप्त गुमनामी** प्राप्त करना है।

आपकी गुमनामी इस बात पर निर्भर करती है कि आप I2P को कैसे कॉन्फ़िगर करते हैं, आप peers और subscriptions को कैसे चुनते हैं, और आप कौन से applications को expose करते हैं।

---

## 2. क्रिप्टोग्राफिक और ट्रांसपोर्ट विकास (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**वर्तमान क्रिप्टोग्राफिक सुइट (Noise XK):** - **X25519** कुंजी विनिमय के लिए   - **ChaCha20/Poly1305 AEAD** एन्क्रिप्शन के लिए   - **Ed25519 (EdDSA-SHA512)** हस्ताक्षर के लिए   - **SHA-256** हैशिंग और HKDF के लिए   - वैकल्पिक **ML-KEM hybrids** पोस्ट-क्वांटम परीक्षण के लिए

सभी ElGamal और AES-CBC उपयोग समाप्त कर दिए गए हैं। Transport पूरी तरह से NTCP2 (TCP) और SSU2 (UDP) है; दोनों IPv4/IPv6, forward secrecy, और DPI obfuscation का समर्थन करते हैं।

---

## 3. नेटवर्क आर्किटेक्चर सारांश

- **Free-route mixnet:** प्रेषक और प्राप्तकर्ता प्रत्येक अपनी स्वयं की tunnels परिभाषित करते हैं।  
- **कोई केंद्रीय प्राधिकरण नहीं:** Routing और naming विकेंद्रीकृत हैं; प्रत्येक router स्थानीय विश्वास बनाए रखता है।  
- **एकदिशीय tunnels:** Inbound और outbound अलग-अलग हैं (10 मिनट की जीवनकाल)।  
- **Exploratory tunnels:** डिफ़ॉल्ट रूप से 2 hops; client tunnels 2–3 hops।  
- **Floodfill routers:** ~55 000 nodes में से ~1 700 (~6 %) वितरित NetDB को बनाए रखते हैं।  
- **NetDB rotation:** Keyspace UTC मध्यरात्रि पर दैनिक रूप से घूमता है।  
- **Sub-DB isolation:** संस्करण 2.4.0 से, प्रत्येक client और router अलग-अलग databases का उपयोग करते हैं ताकि linking को रोका जा सके।

---

## 4. हमले की श्रेणियां और वर्तमान सुरक्षा

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. आधुनिक नेटवर्क डेटाबेस (NetDB)

**मुख्य तथ्य (अभी भी सटीक):** - संशोधित Kademlia DHT, RouterInfo और LeaseSets को संग्रहीत करता है।   - SHA-256 key hashing; 10 s timeout के साथ 2 निकटतम floodfills को समानांतर queries।   - LeaseSet जीवनकाल ≈ 10 min (LeaseSet2) या 18 h (MetaLeaseSet)।

**नए प्रकार (0.9.38 के बाद से):** - **LeaseSet2 (Type 3)** – एकाधिक एन्क्रिप्शन प्रकार, टाइमस्टैम्प युक्त।   - **EncryptedLeaseSet2 (Type 5)** – निजी सेवाओं के लिए blinded destination (DH या PSK प्रमाणीकरण)।   - **MetaLeaseSet (Type 7)** – मल्टीहोमिंग और विस्तारित समाप्ति अवधि।

**प्रमुख सुरक्षा उन्नयन – Sub-DB Isolation (2.4.0):** - router↔client जुड़ाव को रोकता है।   - प्रत्येक client और router अलग netDb खंडों का उपयोग करते हैं।   - सत्यापित और ऑडिट किया गया (2.5.0)।

---

## 6. हिडन मोड और प्रतिबंधित रूट्स

- **Hidden Mode:** लागू किया गया (Freedom House स्कोर के अनुसार सख्त देशों में स्वचालित)।  
    Router RouterInfo प्रकाशित नहीं करते या ट्रैफ़िक को route नहीं करते।  
- **Restricted Routes:** आंशिक रूप से लागू किया गया (केवल बुनियादी trust-only tunnel)।  
    व्यापक trusted-peer routing की योजना बनी हुई है (3.0+)।

ट्रेड-ऑफ: बेहतर गोपनीयता ↔ नेटवर्क क्षमता में कम योगदान।

---

## 7. DoS और Floodfill हमले

**ऐतिहासिक:** 2013 UCSB शोध ने दिखाया कि Eclipse और Floodfill टेकओवर संभव थे। **आधुनिक सुरक्षा में शामिल हैं:** - दैनिक keyspace रोटेशन। - Floodfill सीमा ≈ 500, प्रति /16 एक। - यादृच्छिक स्टोरेज सत्यापन विलंब। - नए-router वरीयता (2.6.0)। - स्वचालित नामांकन सुधार (2.9.0)। - भीड़-जागरूक रूटिंग और lease थ्रॉटलिंग (2.4.0+)।

Floodfill हमले सैद्धांतिक रूप से संभव हैं लेकिन व्यावहारिक रूप से कठिन हैं।

---

## 8. ट्रैफिक विश्लेषण और सेंसरशिप

I2P ट्रैफ़िक की पहचान करना कठिन है: कोई निश्चित पोर्ट नहीं, कोई plaintext handshake नहीं, और यादृच्छिक padding।   NTCP2 और SSU2 पैकेट सामान्य प्रोटोकॉल की नकल करते हैं और ChaCha20 हेडर obfuscation का उपयोग करते हैं।   Padding रणनीतियाँ बुनियादी हैं (यादृच्छिक आकार), dummy traffic लागू नहीं है (महंगा)।   Tor exit nodes से कनेक्शन 2.6.0 से अवरुद्ध हैं (संसाधनों की सुरक्षा के लिए)।

---

## 9. स्थायी सीमाएं (स्वीकृत)

- कम-विलंबता वाले ऐप्स के लिए टाइमिंग सहसंबंध एक मौलिक जोखिम बना रहता है।
- ज्ञात सार्वजनिक गंतव्यों के खिलाफ इंटरसेक्शन हमले अभी भी शक्तिशाली हैं।
- Sybil हमलों के खिलाफ पूर्ण सुरक्षा का अभाव है (HashCash लागू नहीं किया गया)।
- स्थिर-दर ट्रैफ़िक और महत्वपूर्ण विलंब अभी तक लागू नहीं हुए हैं (3.0 में योजनाबद्ध)।

इन सीमाओं के बारे में पारदर्शिता जानबूझकर है — यह उपयोगकर्ताओं को गुमनामी को अधिक आंकने से रोकती है।

---

## 10. नेटवर्क सांख्यिकी (2025)

- विश्वभर में ~55,000 सक्रिय routers (2013 में 7,000 से ↑)  
- ~1,700 floodfill routers (~6%)  
- डिफ़ॉल्ट रूप से 95% tunnel routing में भाग लेते हैं  
- बैंडविड्थ स्तर: K (<12 KB/s) → X (>2 MB/s)  
- न्यूनतम floodfill दर: 128 KB/s  
- Router console Java 8+ (आवश्यक), अगले चक्र में Java 17+ की योजना

---

## 11. विकास और केंद्रीय संसाधन

- आधिकारिक साइट: [geti2p.net](/)
- दस्तावेज़: [Documentation](/docs/)  
- Debian रिपॉजिटरी: <https://deb.i2pgit.org> ( Oct 2023 में deb.i2p2.de को बदल दिया गया )  
- सोर्स कोड: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub मिरर  
- सभी रिलीज़ साइन किए गए SU3 कंटेनर हैं (RSA-4096, zzz/str4d keys)  
- कोई सक्रिय मेलिंग लिस्ट नहीं; कम्युनिटी <https://i2pforum.net> और IRC2P के माध्यम से।  
- अपडेट साइकिल: 6–8 सप्ताह की स्थिर रिलीज़।

---

## 12. 0.8.x के बाद से सुरक्षा सुधारों का सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. ज्ञात अनसुलझे या नियोजित कार्य

- व्यापक प्रतिबंधित मार्ग (विश्वसनीय-सहकर्मी रूटिंग) → 3.0 में योजनाबद्ध।
- समय प्रतिरोध के लिए गैर-तुच्छ विलंब/बैचिंग → 3.0 में योजनाबद्ध।
- उन्नत पैडिंग और डमी ट्रैफ़िक → अकार्यान्वित।
- HashCash पहचान सत्यापन → बुनियादी ढांचा मौजूद है लेकिन निष्क्रिय।
- R5N DHT प्रतिस्थापन → केवल प्रस्ताव।

---

## 14. मुख्य संदर्भ

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [I2P आधिकारिक दस्तावेज़ीकरण](/docs/)

---

## 15. निष्कर्ष

I2P का मूल गुमनामी मॉडल दो दशकों से कायम है: वैश्विक विशिष्टता का त्याग करके स्थानीय विश्वास और सुरक्षा को प्राथमिकता देना। ElGamal से X25519, NTCP से NTCP2, और मैनुअल reseeds से Sub-DB अलगाव तक, परियोजना ने गहन रक्षा और पारदर्शिता के अपने दर्शन को बनाए रखते हुए विकास किया है।

किसी भी कम-विलंबता वाले mixnet के खिलाफ कई हमले सैद्धांतिक रूप से संभव रहते हैं, लेकिन I2P की निरंतर सुदृढ़ीकरण प्रक्रिया उन्हें तेजी से अव्यावहारिक बना रही है। नेटवर्क पहले से कहीं अधिक बड़ा, तेज़ और सुरक्षित है — फिर भी अपनी सीमाओं के बारे में ईमानदार है।
