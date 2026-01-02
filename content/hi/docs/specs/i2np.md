---
title: "I2P नेटवर्क प्रोटोकॉल (I2NP)"
description: "I2P के भीतर router से router संदेश प्रारूप, प्राथमिकताएँ, और आकार सीमाएँ।"
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## अवलोकन

I2P नेटवर्क प्रोटोकॉल (I2NP) यह निर्धारित करता है कि routers संदेशों का आदान-प्रदान कैसे करते हैं, कौन-से ट्रांसपोर्ट चुनते हैं, और गुमनामी बनाए रखते हुए ट्रैफ़िक को कैसे मिश्रित करते हैं। यह **I2CP** (क्लाइंट API) और ट्रांसपोर्ट प्रोटोकॉल्स (**NTCP2** और **SSU2**) के बीच संचालित होता है।

I2NP, I2P ट्रांसपोर्ट प्रोटोकॉल्स के ऊपर की लेयर है. यह एक router-to-router प्रोटोकॉल है, जिसका उपयोग इन कार्यों के लिए होता है: - नेटवर्क डेटाबेस लुकअप और उत्तर - tunnels बनाना - एन्क्रिप्टेड router और क्लाइंट डेटा संदेश

I2NP संदेश या तो बिंदु-से-बिंदु किसी अन्य router को भेजे जा सकते हैं, या उस router तक tunnels के माध्यम से गुमनाम रूप से भेजे जा सकते हैं।

Routers स्थानीय प्राथमिकताओं का उपयोग करके बहिर्गामी कार्य को कतारबद्ध करते हैं। उच्च प्राथमिकता संख्याएँ पहले संसाधित की जाती हैं। मानक tunnel डेटा प्राथमिकता (400) से ऊपर की कोई भी चीज़ को तात्कालिक माना जाता है।

### वर्तमान ट्रांसपोर्ट्स

I2P अब IPv4 और IPv6 दोनों के लिए **NTCP2** (TCP) और **SSU2** (UDP) का उपयोग करता है। दोनों ट्रांसपोर्ट निम्न का उपयोग करते हैं: - **X25519** कुंजी विनिमय (Noise protocol framework — Noise प्रोटोकॉल फ्रेमवर्क) - **ChaCha20/Poly1305** प्रमाणित एन्क्रिप्शन (AEAD) - **SHA-256** हैशिंग

**पुराने ट्रांसपोर्ट हटाए गए:** - NTCP (मूल TCP) को Java router से रिलीज़ 0.9.50 (मई 2021) में हटाया गया - SSU v1 (मूल UDP) को Java router से रिलीज़ 2.4.0 (दिसंबर 2023) में हटाया गया - SSU v1 को i2pd से रिलीज़ 2.44.0 (नवंबर 2022) में हटाया गया

2025 तक, नेटवर्क पूरी तरह Noise (प्रोटोकॉल फ्रेमवर्क) आधारित ट्रांसपोर्ट्स पर स्थानांतरित हो चुका है, और लेगेसी ट्रांसपोर्ट का समर्थन बिल्कुल नहीं है।

---

## संस्करण क्रमांकन प्रणाली

**महत्वपूर्ण:** I2P एक दोहरी संस्करण प्रणाली का उपयोग करता है, जिसे स्पष्ट रूप से समझना आवश्यक है:

### रिलीज़ संस्करण (उपयोगकर्ता-उन्मुख)

ये वे संस्करण हैं जिन्हें उपयोगकर्ता देखते और डाउनलोड करते हैं: - 0.9.50 (मई 2021) - अंतिम 0.9.x रिलीज़ - **1.5.0** (अगस्त 2021) - पहला 1.x रिलीज़ - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (2021-2022 के दौरान) - **2.0.0** (नवंबर 2022) - पहला 2.x रिलीज़ - 2.1.0 से 2.9.0 तक (2023-2025 के दौरान) - **2.10.0** (8 सितंबर, 2025) - वर्तमान रिलीज़

### API संस्करण (प्रोटोकॉल संगतता)

ये आंतरिक संस्करण संख्याएँ हैं जो RouterInfo गुणधर्मों के "router.version" फ़ील्ड में प्रकाशित की जाती हैं: - 0.9.50 (मई 2021) - **0.9.51** (अगस्त 2021) - रिलीज़ 1.5.0 के लिए API संस्करण - 0.9.52 से 0.9.66 तक (2.x रिलीज़ के दौरान भी जारी) - **0.9.67** (सितंबर 2025) - रिलीज़ 2.10.0 के लिए API संस्करण

**मुख्य बिंदु:** 0.9.51 से 0.9.67 तक क्रमांकित कोई रिलीज़ नहीं हुई थी। ये संख्याएँ केवल API (एप्लिकेशन प्रोग्रामिंग इंटरफेस) संस्करण पहचानकर्ताओं के रूप में मौजूद हैं। I2P ने रिलीज़ 0.9.50 से सीधे 1.5.0 पर छलांग लगाई।

### संस्करण मैपिंग तालिका

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**आगामी:** रिलीज़ 2.11.0 (दिसंबर 2025 के लिए नियोजित) में Java 17+ की आवश्यकता होगी और डिफ़ॉल्ट रूप से post-quantum cryptography (पोस्ट-क्वांटम क्रिप्टोग्राफी) सक्रिय की जाएगी।

---

## प्रोटोकॉल संस्करण

सभी router को अपने I2NP प्रोटोकॉल संस्करण को RouterInfo (राउटर जानकारी की डेटा संरचना) की प्रॉपर्टीज़ में मौजूद "router.version" फ़ील्ड में प्रकाशित करना आवश्यक है। यह संस्करण फ़ील्ड API संस्करण है, जो विभिन्न I2NP प्रोटोकॉल विशेषताओं के समर्थन के स्तर को दर्शाता है, और यह आवश्यक नहीं कि यह वास्तविक router संस्करण हो।

यदि वैकल्पिक (गैर-Java) routers वास्तविक router के कार्यान्वयन के बारे में किसी भी संस्करण संबंधी जानकारी प्रकाशित करना चाहते हैं, तो उन्हें यह किसी अन्य प्रॉपर्टी में करना होगा। नीचे सूचीबद्ध संस्करणों के अलावा अन्य संस्करण भी अनुमत हैं। समर्थन का निर्धारण संख्यात्मक तुलना के माध्यम से किया जाएगा; उदाहरण के लिए, 0.9.13 का अर्थ 0.9.12 की सुविधाओं के लिए समर्थन है।

**नोट:** "coreVersion" प्रॉपर्टी अब router की जानकारी में प्रकाशित नहीं की जाती है और I2NP प्रोटोकॉल संस्करण का निर्धारण करने के लिए कभी उपयोग नहीं की गई थी।

### API संस्करण सुविधाओं का सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**नोट:** ट्रांसपोर्ट-संबंधित विशेषताएँ और संगतता समस्याएँ भी मौजूद हैं। विवरण के लिए NTCP2 और SSU2 ट्रांसपोर्ट प्रलेखन देखें।

---

## संदेश हेडर

I2NP एक तार्किक 16-बाइट हेडर संरचना का उपयोग करता है, जबकि आधुनिक ट्रांसपोर्ट प्रोटोकॉल (NTCP2 और SSU2) एक संक्षिप्त 9-बाइट हेडर उपयोग करते हैं, जो अनावश्यक आकार और चेकसम फ़ील्ड्स को छोड़ देता है। फ़ील्ड्स अवधारणात्मक रूप से समान ही रहते हैं।

### हेडर प्रारूप तुलना

**मानक फ़ॉर्मेट (16 बाइट्स):**

पुराने NTCP ट्रांसपोर्ट में और तब उपयोग किया जाता है जब I2NP संदेश अन्य संदेशों के भीतर समाहित होते हैं (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**SSU के लिए संक्षिप्त प्रारूप (अप्रचलित, 5 बाइट्स):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**NTCP2, SSU2, और ECIES-Ratchet Garlic Cloves (I2P में 'garlic' संदेश का हिस्सा) के लिए संक्षिप्त प्रारूप (9 बाइट्स):**

आधुनिक ट्रांसपोर्ट प्रोटोकॉल में और ECIES (Elliptic Curve Integrated Encryption Scheme—दीर्घवृत्तीय वक्र समेकित एन्क्रिप्शन योजना) द्वारा एन्क्रिप्ट किए गए garlic संदेशों में उपयोग किया जाता है।

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### हेडर फ़ील्ड विवरण

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### कार्यान्वयन संबंधी नोट्स

- SSU (अप्रचलित) के माध्यम से प्रसारित होने पर, केवल प्रकार और 4-बाइट समाप्ति समय शामिल थे
- NTCP2 या SSU2 के माध्यम से प्रसारित होने पर, 9-बाइट का संक्षिप्त फ़ॉर्मेट उपयोग किया जाता है
- अन्य संदेशों (Data, TunnelData, TunnelGateway, GarlicClove) में समाहित I2NP संदेशों के लिए मानक 16-बाइट हेडर आवश्यक है
- रिलीज़ 0.8.12 से, दक्षता के लिए प्रोटोकॉल स्टैक के कुछ स्थानों पर checksum (चेकसम) का सत्यापन अक्षम कर दिया गया है, लेकिन संगतता के लिए checksum का निर्माण अभी भी आवश्यक है
- संक्षिप्त समाप्ति समय चिह्न-रहित होता है और 7 फ़रवरी, 2106 को रैप-अराउंड कर जाएगा। उस तारीख के बाद सही समय प्राप्त करने के लिए एक ऑफसेट जोड़ना होगा
- पुराने संस्करणों के साथ संगतता हेतु, भले ही उनका सत्यापन न किया जाए, हमेशा checksum उत्पन्न करें

---

## आकार सीमाएँ

Tunnel संदेश I2NP पेलोड को नियत आकार के हिस्सों में विभाजित करते हैं:
- **पहला खंड:** लगभग 956 बाइट
- **बाद के खंड:** प्रत्येक लगभग 996 बाइट
- **अधिकतम खंड:** 64 (0-63 क्रमांकित)
- **अधिकतम पेलोड:** लगभग 61,200 बाइट (61.2 KB)

**गणना:** 956 + (63 × 996) = 63,704 बाइट्स का सैद्धांतिक अधिकतम, जबकि ओवरहेड के कारण व्यावहारिक सीमा लगभग 61,200 बाइट्स।

### ऐतिहासिक संदर्भ

पुराने ट्रांसपोर्ट्स में फ्रेम आकार की सीमाएँ अधिक कड़ी थीं: - NTCP: 16 KB फ्रेम - SSU: लगभग 32 KB फ्रेम

NTCP2 लगभग 65 KB आकार के फ्रेम का समर्थन करता है, लेकिन tunnel फ्रैगमेंटेशन सीमा अब भी लागू होती है।

### एप्लिकेशन डेटा संबंधी विचार

Garlic messages (I2P में संदेशों को समूहित करने की विधि) LeaseSets, Session Tags, या एन्क्रिप्टेड LeaseSet2 रूपांतरों को बंडल कर सकते हैं, जिससे पेलोड डेटा के लिए उपलब्ध स्थान कम हो जाता है।

**अनुशंसा:** विश्वसनीय वितरण सुनिश्चित करने के लिए Datagrams (डेटा पैकेट का एक प्रकार) को ≤ 10 KB तक ही रखना चाहिए। 61 KB की सीमा के निकट पहुँचने वाले संदेशों को निम्नलिखित समस्याओं का सामना हो सकता है: - खंडन और पुनर्संयोजन के कारण विलंबता में वृद्धि - वितरण विफलता की उच्च संभावना - ट्रैफ़िक विश्लेषण के प्रति अधिक उजागर होना

### Fragmentation (डेटा को छोटे हिस्सों में बाँटने की प्रक्रिया) के तकनीकी विवरण

प्रत्येक tunnel संदेश ठीक 1,024 बाइट (1 KB) का होता है और इसमें शामिल होते हैं: - 4-बाइट tunnel ID - 16-बाइट initialization vector (IV) (आरंभीकरण सदिश) - 1,004 बाइट कूटबद्ध डेटा

कूटबद्ध डेटा के भीतर, tunnel संदेश खंडित I2NP संदेशों को वहन करते हैं, जिनके फ़्रैगमेंट हेडर यह दर्शाते हैं: - फ़्रैगमेंट संख्या (0-63) - यह पहला या अनुवर्ती फ़्रैगमेंट है - पुनर्संयोजन के लिए सम्पूर्ण संदेश ID

पहला खंड पूर्ण I2NP संदेश हेडर (16 बाइट्स) शामिल करता है, जिससे payload (डेटा सामग्री) के लिए लगभग 956 बाइट्स बचते हैं। अनुवर्ती खंड संदेश हेडर शामिल नहीं करते, जिससे प्रति खंड लगभग 996 बाइट्स का payload संभव हो पाता है।

---

## सामान्य संदेश प्रकार

Routers संदेश प्रकार और प्राथमिकता का उपयोग आउटबाउंड कार्य को निर्धारित करने के लिए करते हैं। उच्च प्राथमिकता मान पहले संसाधित किए जाते हैं। नीचे दिए गए मान वर्तमान Java I2P डिफ़ॉल्ट मानों से मेल खाते हैं (API संस्करण 0.9.67 के अनुसार)।

**नोट:** प्राथमिकताएँ कार्यान्वयन पर निर्भर होती हैं। प्रामाणिक प्राथमिकता मानों के लिए, Java I2P स्रोत कोड में `OutNetMessage` क्लास के दस्तावेज़ीकरण को देखें।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**आरक्षित संदेश प्रकार:** - प्रकार 0: आरक्षित - प्रकार 4-9: भविष्य में उपयोग हेतु आरक्षित - प्रकार 12-17: भविष्य में उपयोग हेतु आरक्षित - प्रकार 224-254: प्रायोगिक संदेशों के लिए आरक्षित - प्रकार 255: भविष्य के विस्तार हेतु आरक्षित

### संदेश प्रकार टिप्पणियाँ

- Control-plane messages (नियंत्रण-समतल संदेश) (DatabaseLookup, TunnelBuild, आदि) आमतौर पर **अन्वेषी tunnels** से होकर गुजरते हैं, न कि क्लाइंट tunnels से, जिससे स्वतंत्र प्राथमिकता निर्धारण संभव हो पाता है
- प्राथमिकता मान अनुमानित होते हैं और कार्यान्वयन के अनुसार बदल सकते हैं
- TunnelBuild (21) और TunnelBuildReply (22) अप्रचलित हैं, लेकिन बहुत लंबे tunnels (>8 hops) के साथ अनुकूलता के लिए अब भी लागू किए जाते हैं (यहाँ 'hops' = मध्यवर्ती router चरण)
- मानक tunnel डेटा प्राथमिकता 400 है; इससे ऊपर कुछ भी तत्काल माना जाता है
- आज के नेटवर्क में सामान्य tunnel लंबाई 3-4 hops होती है, इसलिए अधिकांश tunnel निर्माण ShortTunnelBuild (218-byte records) या VariableTunnelBuild (528-byte records) का उपयोग करते हैं

---

## एन्क्रिप्शन और संदेश रैपिंग

router अक्सर प्रेषण से पहले I2NP संदेशों को लपेटते हैं, जिससे कई एन्क्रिप्शन परतें बनती हैं। एक DeliveryStatus संदेश इस प्रकार हो सकता है: 1. एक GarlicMessage में लिपटा हुआ (एन्क्रिप्टेड) 2. एक DataMessage के अंदर 3. एक TunnelData संदेश के भीतर (फिर से एन्क्रिप्टेड)

प्रत्येक hop (नेटवर्क में एक मध्यवर्ती नोड) केवल अपनी परत को डिक्रिप्ट करता है; अंतिम गंतव्य सबसे भीतरी पेलोड को प्रकट करता है।

### एन्क्रिप्शन एल्गोरिद्म

**लीगेसी (चरणबद्ध रूप से हटाया जा रहा है):** - ElGamal/AES + SessionTags (सत्र टैग) - असममित एन्क्रिप्शन के लिए ElGamal-2048 - सममित एन्क्रिप्शन के लिए AES-256 - 32-बाइट session tags

**वर्तमान (API 0.9.48 के अनुसार मानक):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD with ratcheting forward secrecy (आगे की गोपनीयता) - Noise प्रोटोकॉल फ़्रेमवर्क (गंतव्यों के लिए Noise_IK_25519_ChaChaPoly_SHA256) - 8-byte सेशन टैग्स (32 bytes से घटाकर) - forward secrecy के लिए Signal Double Ratchet एल्गोरिथ्म - API संस्करण 0.9.46 (2020) में प्रस्तुत किया गया - API संस्करण 0.9.58 (2023) से सभी routers के लिए अनिवार्य

**भविष्य (2.10.0 में बीटा):** - Post-quantum hybrid cryptography (क्वांटम-युग के बाद की मिश्रित क्रिप्टोग्राफी) जो MLKEM (ML-KEM-768) तथा X25519 के संयोजन का उपयोग करती है - Hybrid ratchet (क्रमिक-कुंजी तंत्र) जो परंपरागत और post-quantum key agreement (कुंजी-सहमति) को संयोजित करता है - ECIES-X25519 के साथ पिछली संगतता रखता है - रिलीज़ 2.11.0 (दिसंबर 2025) में डिफ़ॉल्ट बन जाएगा

### ElGamal Router का अप्रचलन

**गंभीर:** ElGamal routers को API संस्करण 0.9.58 (रिलीज़ 2.2.0, मार्च 2023) से अप्रचलित घोषित किया गया है। चूँकि क्वेरी करने के लिए अनुशंसित न्यूनतम floodfill संस्करण अब 0.9.58 है, इसलिए कार्यान्वयनों को ElGamal floodfill routers के लिए एन्क्रिप्शन लागू करने की आवश्यकता नहीं है।

**हालाँकि:** ElGamal (ElGamal एन्क्रिप्शन एल्गोरिद्म) डेस्टिनेशन अभी भी पिछली संगतता के लिए समर्थित हैं। ElGamal एन्क्रिप्शन का उपयोग करने वाले क्लाइंट अभी भी ECIES (अण्डाकार वक्र समेकित एन्क्रिप्शन योजना) routers के माध्यम से संचार कर सकते हैं।

### ECIES-X25519-AEAD-Ratchet का विवरण

यह I2P की क्रिप्टोग्राफी विशिष्टता में क्रिप्टो प्रकार 4 है। यह प्रदान करता है:

**मुख्य विशेषताएँ:** - ratcheting (हर संदेश के लिए नई कुंजियाँ) के माध्यम से Forward secrecy - सत्र टैग भंडारण में कमी (8 bytes बनाम 32 bytes) - कई सत्र प्रकार (नया सत्र, मौजूदा सत्र, एक-बार उपयोग) - Noise protocol (एक क्रिप्टोग्राफ़िक हैंडशेक फ़्रेमवर्क) Noise_IK_25519_ChaChaPoly_SHA256 पर आधारित - Signal के Double Ratchet algorithm (संदेश-कुंजी रैचेट एल्गोरिद्म) के साथ एकीकृत

**क्रिप्टोग्राफिक प्रिमिटिव्स:** - X25519 Diffie-Hellman कुंजी सहमति के लिए - ChaCha20 स्ट्रीम एन्क्रिप्शन के लिए - Poly1305 संदेश प्रामाणीकरण (AEAD) के लिए - SHA-256 हैशिंग के लिए - HKDF कुंजी व्युत्पत्ति के लिए

**सत्र प्रबंधन:** - नया सत्र: स्थिर destination key का उपयोग करके प्रारंभिक कनेक्शन - मौजूदा सत्र: आगामी संदेशों के लिए session tags का उपयोग - एक-बार का सत्र: कम ओवरहेड हेतु एक-संदेश सत्र

पूर्ण तकनीकी विवरण के लिए [ECIES Specification](/docs/specs/ecies/) और [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/) देखें।

---

## सामान्य संरचनाएँ

निम्नलिखित संरचनाएँ कई I2NP संदेशों के घटक हैं। ये पूर्ण संदेश नहीं हैं।

### BuildRequestRecord (ElGamal)

**अप्रचलित.** वर्तमान नेटवर्क में केवल तब उपयोग किया जाता है जब किसी tunnel में ElGamal router हो। आधुनिक प्रारूप के लिए [ECIES Tunnel Creation](/docs/specs/implementation/) देखें।

**उद्देश्य:** tunnel में एक हॉप के निर्माण का अनुरोध करने के लिए कई रिकॉर्डों के सेट में से एक रिकॉर्ड।

**प्रारूप:**

ElGamal और AES एन्क्रिप्टेड (कुल 528 बाइट्स):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamal (एक सार्वजनिक-कुंजी क्रिप्टोग्राफ़ी एल्गोरिथ्म) एन्क्रिप्टेड संरचना (528 बाइट्स):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Cleartext (स्पष्ट-पाठ) संरचना (एन्क्रिप्शन से पहले 222 बाइट्स):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**नोट्स:** - ElGamal-2048 एन्क्रिप्शन 514-बाइट का ब्लॉक बनाता है, लेकिन दो पैडिंग बाइट्स (स्थितियाँ 0 और 257 पर) हटा दी जाती हैं, परिणामस्वरूप 512 बाइट्स रह जाती हैं - फ़ील्ड विवरण के लिए [Tunnel निर्माण विनिर्देशन](/docs/specs/implementation/) देखें - स्रोत कोड: `net.i2p.data.i2np.BuildRequestRecord` - स्थिरांक: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 लंबा)

ECIES-X25519 routers के लिए, API संस्करण 0.9.48 में पेश किया गया। मिश्रित tunnels के साथ पिछली संगतता बनाए रखने के लिए 528 बाइट्स का उपयोग करता है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**कुल आकार:** 528 बाइट्स (संगतता के लिए ElGamal के समान)

स्पष्ट-पाठ संरचना और एन्क्रिप्शन विवरण के लिए [ECIES Tunnel Creation](/docs/specs/implementation/) देखें।

### BuildRequestRecord (ECIES-X25519 Short)

केवल ECIES-X25519 routers के लिए, API संस्करण 0.9.51 (रिलीज़ 1.5.0) से। यह वर्तमान मानक प्रारूप है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**कुल आकार:** 218 बाइट्स (528 बाइट्स से 59% की कमी)

**मुख्य अंतर:** संक्षिप्त रिकॉर्ड, उन्हें रिकॉर्ड में स्पष्ट रूप से शामिल करने के बजाय, सभी कुंजियाँ HKDF (key derivation function, कुंजी व्युत्पन्न फ़ंक्शन) के माध्यम से व्युत्पन्न करते हैं। इसमें शामिल हैं:
- लेयर कुंजियाँ (tunnel एन्क्रिप्शन के लिए)
- IV कुंजियाँ (tunnel एन्क्रिप्शन के लिए)
- Reply कुंजियाँ (build reply (निर्माण प्रत्युत्तर) के लिए)
- Reply IVs (build reply के लिए)

सभी कुंजियाँ X25519 key exchange (एलिप्टिक-कर्व Diffie–Hellman कुंजी-अदला-बदली) से प्राप्त साझा रहस्य के आधार पर, Noise protocol (क्रिप्टोग्राफ़िक हैंडशेक फ्रेमवर्क) के HKDF (HMAC-आधारित कुंजी व्युत्पत्ति फ़ंक्शन) तंत्र का उपयोग करके व्युत्पन्न की जाती हैं।

**लाभ:** - 4 छोटे रिकॉर्ड एक ही tunnel संदेश (873 बाइट्स) में समा जाते हैं - प्रत्येक रिकॉर्ड के लिए अलग-अलग संदेशों के बजाय तीन-संदेश वाला tunnel निर्माण - बैंडविड्थ और विलंबता में कमी - लंबे प्रारूप के समान सुरक्षा गुण

औचित्य के लिए [प्रस्ताव 157](/proposals/157-new-tbm/) और पूर्ण विनिर्देश के लिए [ECIES Tunnel Creation](/docs/specs/implementation/) देखें।

**स्रोत कोड:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - स्थिरांक: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal)

**अप्रचलित।** केवल तब उपयोग किया जाता है जब tunnel में ElGamal (क्रिप्टोग्राफ़िक एल्गोरिद्म) router शामिल हो।

**उद्देश्य:** बिल्ड अनुरोध के उत्तरों वाले बहु-रिकॉर्ड सेट में से एक रिकॉर्ड।

**प्रारूप:**

एन्क्रिप्टेड (528 बाइट्स, BuildRequestRecord के समान आकार):

```
bytes 0-527 :: AES-encrypted record
```
एन्क्रिप्शन-रहित संरचना:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**प्रत्युत्तर कोड:** - `0` - स्वीकार - `30` - अस्वीकार (बैंडविड्थ सीमा पार)

reply फ़ील्ड के विवरण के लिए [Tunnel निर्माण विनिर्देश](/docs/specs/implementation/) देखें।

### बिल्ड प्रतिक्रिया रिकॉर्ड (ECIES-X25519)

ECIES-X25519 (एलिप्टिक कर्व आधारित क्रिप्टोग्राफिक सूट) routers के लिए, API संस्करण 0.9.48+। संबंधित अनुरोध के समान आकार (लंबे के लिए 528, छोटे के लिए 218)।

**प्रारूप:**

लंबा प्रारूप (528 बाइट):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
संक्षिप्त प्रारूप (218 बाइट्स):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**स्पष्ट-पाठ संरचना (दोनों प्रारूप):**

इसमें एक मैपिंग संरचना (I2P का key-value फ़ॉर्मेट) शामिल है: - उत्तर स्थिति कोड (आवश्यक) - उपलब्ध बैंडविड्थ पैरामीटर ("b") (वैकल्पिक, API 0.9.65 में जोड़ा गया) - भविष्य के विस्तारों के लिए अन्य वैकल्पिक पैरामीटर

**उत्तर स्थिति कोड:** - `0` - सफलता - `30` - अस्वीकृत: बैंडविड्थ सीमा पार

पूर्ण विनिर्देश के लिए [ECIES Tunnel Creation](/docs/specs/implementation/) देखें।

### GarlicClove (लहसुन की कली) (ElGamal/AES)

**चेतावनी:** यह वह प्रारूप है जो ElGamal से एन्क्रिप्ट किए गए garlic messages (समूहित संदेश) के भीतर मौजूद garlic cloves (उप-संदेश) के लिए उपयोग होता है। ECIES-AEAD-X25519-Ratchet garlic messages और garlic cloves का प्रारूप इससे काफी भिन्न है। आधुनिक प्रारूप के लिए [ECIES विनिर्देश](/docs/specs/ecies/) देखें।

**routers के लिए अप्रचलित (API 0.9.58+), destinations के लिए अब भी समर्थित।**

**प्रारूप:**

एन्क्रिप्शन-रहित:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**नोट्स:** - Cloves (GarlicMessage के उप-संदेश) कभी खंडित नहीं किए जाते - जब Delivery Instructions फ्लैग बाइट का पहला बिट 0 हो, तो clove एन्क्रिप्टेड नहीं होता - जब पहला बिट 1 हो, तो clove एन्क्रिप्टेड होता है (अभी लागू नहीं किया गया फीचर) - अधिकतम लंबाई कुल clove लंबाइयों और अधिकतम GarlicMessage लंबाई का एक फ़ंक्शन है - प्रमाणपत्र का उपयोग HashCash के साथ राउटिंग के लिए "pay" करने में किया जा सकता है (भविष्य की संभावना) - व्यवहार में प्रयुक्त संदेश: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage के भीतर GarlicMessage हो सकता है (nested garlic), लेकिन व्यवहार में इसका उपयोग नहीं होता

अवधारणात्मक अवलोकन के लिए [Garlic Routing](/docs/overview/garlic-routing/) देखें।

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

ECIES-X25519 routers और गंतव्यों के लिए, API संस्करण 0.9.46+। यह वर्तमान मानक प्रारूप है।

**अत्यंत महत्वपूर्ण अंतर:** ECIES garlic (I2P में bundled संदेशों की तकनीक) स्पष्ट clove (I2P संदेश का उपघटक) संरचनाओं के बजाय Noise protocol (एक क्रिप्टोग्राफ़िक हैंडशेक फ़्रेमवर्क) ब्लॉक्स पर आधारित एक पूरी तरह भिन्न संरचना का उपयोग करता है।

**प्रारूप:**

ECIES 'garlic' संदेश (I2P में कई संदेशों को एक साथ पैक करने की तकनीक) कई ब्लॉकों की शृंखला से मिलकर बने होते हैं:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**ब्लॉक प्रकार:** - `0` - Garlic Clove ब्लॉक (एक I2NP संदेश समाहित करता है) - `1` - दिनांक-समय ब्लॉक (टाइमस्टैम्प) - `2` - विकल्प ब्लॉक (डिलीवरी विकल्प) - `3` - पैडिंग ब्लॉक - `254` - समापन ब्लॉक (अभी लागू नहीं)

**Garlic Clove Block (type 0) (Garlic संदेश का उप-घटक ब्लॉक):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**ElGamal प्रारूप से मुख्य अंतर:** - 8-बाइट Date के स्थान पर 4-बाइट समाप्ति समय (epoch से सेकंड) का उपयोग करता है - कोई प्रमाणपत्र फ़ील्ड नहीं - प्रकार और लंबाई सहित ब्लॉक संरचना में संलग्न है - पूरे संदेश को ChaCha20/Poly1305 AEAD से एन्क्रिप्ट किया गया है - सेशन प्रबंधन ratcheting (क्रमिक कुंजी-अपडेट तंत्र) के माध्यम से

Noise protocol framework (Noise प्रोटोकॉल का ढांचा) और ब्लॉक संरचनाओं पर पूर्ण विवरण के लिए [ECIES Specification](/docs/specs/ecies/) देखें।

### Garlic Clove (I2P संदेश का उप-घटक) के वितरण निर्देश

यह फ़ॉर्मेट ElGamal और ECIES दोनों प्रकार की garlic cloves (garlic संदेश के घटक) के लिए उपयोग किया जाता है। यह संलग्न संदेश को कैसे पहुँचाया जाए, यह निर्दिष्ट करता है।

**अति महत्वपूर्ण चेतावनी:** यह विनिर्देश केवल Garlic Cloves (लहसुन की कलियाँ) के भीतर वाले Delivery Instructions (वितरण निर्देश) के लिए है। "Delivery Instructions" Tunnel Messages के भीतर भी उपयोग होते हैं, जहाँ उनका प्रारूप काफ़ी भिन्न होता है। tunnel के Delivery Instructions के लिए [Tunnel Message Specification](/docs/specs/implementation/) देखें। इन दोनों प्रारूपों को कदापि न मिलाएँ।

**प्रारूप:**

सत्र कुंजी और विलंब उपयोग में नहीं हैं और कभी मौजूद नहीं होते, इसलिए तीन संभावित लंबाइयाँ हैं:
- 1 बाइट (स्थानीय)
- 33 बाइट (ROUTER और गंतव्य)
- 37 बाइट (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**सामान्य लंबाइयाँ:** - स्थानीय वितरण: 1 बाइट (केवल flag) - ROUTER / DESTINATION वितरण: 33 बाइट (flag + hash) - TUNNEL वितरण: 37 बाइट (flag + hash + tunnel ID)

**डिलीवरी प्रकारों के विवरण:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**कार्यान्वयन नोट्स:** - सेशन कुंजी एन्क्रिप्शन लागू नहीं है और फ्लैग बिट हमेशा 0 रहती है - विलंब पूरी तरह लागू नहीं है और फ्लैग बिट हमेशा 0 रहती है - TUNNEL डिलीवरी के लिए, हैश गेटवे router की पहचान करता है और tunnel ID यह निर्दिष्ट करता है कि कौन‑सा इनबाउंड tunnel है - DESTINATION डिलीवरी के लिए, हैश DESTINATION की सार्वजनिक कुंजी का SHA-256 होता है - ROUTER डिलीवरी के लिए, हैश router की पहचान का SHA-256 होता है

---

## I2NP (I2P नेटवर्क प्रोटोकॉल) संदेश

सभी I2NP संदेश प्रकारों के लिए पूर्ण संदेश विनिर्देश।

### संदेश प्रकारों का सारांश

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**आरक्षित:** - प्रकार 0: आरक्षित - प्रकार 4-9: भविष्य में उपयोग के लिए आरक्षित - प्रकार 12-17: भविष्य में उपयोग के लिए आरक्षित - प्रकार 224-254: प्रायोगिक संदेशों के लिए आरक्षित - प्रकार 255: भविष्य के विस्तार के लिए आरक्षित

---

### DatabaseStore (डेटाबेस स्टोर) (प्रकार 1)

**उद्देश्य:** एक अनुरोध-रहित डेटाबेस स्टोर, या सफल DatabaseLookup संदेश के उत्तर के रूप में।

**सामग्री:** एक असंकुचित LeaseSet, LeaseSet2, MetaLeaseSet, या EncryptedLeaseSet, या एक संकुचित RouterInfo.

**रिप्लाई टोकन सहित फ़ॉर्मेट:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**reply token (उत्तर टोकन) == 0 होने पर फ़ॉर्मेट:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**स्रोत कोड:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (RouterInfo संरचना के लिए) - `net.i2p.data.LeaseSet` (LeaseSet संरचना के लिए)

---

### DatabaseLookup (प्रकार 2)

**उद्देश्य:** नेटवर्क डेटाबेस में किसी प्रविष्टि को खोजने के लिए एक अनुरोध। प्रतिक्रिया या तो DatabaseStore (डेटाबेस में प्रविष्टि को संग्रहीत करने वाला संदेश) या DatabaseSearchReply (खोज का उत्तर देने वाला संदेश) होती है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**उत्तर एन्क्रिप्शन मोڈ्स:**

**NOTE:** ElGamal routers API 0.9.58 से अप्रचलित हैं। क्योंकि क्वेरी करने के लिए अनुशंसित न्यूनतम floodfill संस्करण अब 0.9.58 है, इसलिए कार्यान्वयनों को ElGamal floodfill routers के लिए एन्क्रिप्शन लागू करने की आवश्यकता नहीं है। ElGamal गंतव्य अभी भी समर्थित हैं।

फ़्लैग बिट 4 (ECIESFlag) का उपयोग बिट 1 (encryptionFlag) के साथ मिलकर उत्तर एन्क्रिप्शन मोड निर्धारित करने के लिए किया जाता है:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**कोई एन्क्रिप्शन नहीं (flags 0,0):**

reply_key, tags, और reply_tags मौजूद नहीं हैं।

**ElG से ElG (flags 0,1) - अप्रचलित:**

0.9.7 से समर्थित, 0.9.58 से अप्रचलित.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES (Elliptic Curve Integrated Encryption Scheme - दीर्घवृत्तीय वक्र समेकित एन्क्रिप्शन योजना) से ElG (ElGamal - एलगेमल) (flags 1,0) - अप्रचलित:**

0.9.46 से समर्थित, 0.9.58 से अप्रचलित।

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
प्रत्युत्तर ECIES (Elliptic Curve Integrated Encryption Scheme, दीर्घवृत्त वक्र समेकित एन्क्रिप्शन योजना) मौजूदा सत्र संदेश है, जैसा कि [ECIES विनिर्देश](/docs/specs/ecies/) में परिभाषित है:

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES से ECIES (flags 1,0) - वर्तमान मानक:**

ECIES destination (गंतव्य) या router एक ECIES router को लुकअप अनुरोध भेजता है। 0.9.49 से समर्थित।

उपरोक्त "ECIES to ElG" के समान ही प्रारूप है। लुकअप संदेश का एन्क्रिप्शन [ECIES Routers](/docs/specs/ecies/#routers) में निर्दिष्ट है। अनुरोधकर्ता अनाम है।

**ECIES (अण्डाकार वक्र समेकित एन्क्रिप्शन योजना) से ECIES, DH (डिफी–हेल्मन) (flags 1,1) के साथ - भविष्य:**

अभी तक पूरी तरह परिभाषित नहीं है। [Proposal 156](/proposals/156-ecies-routers/) देखें।

**टिप्पणियाँ:** - 0.9.16 से पहले, कुंजी RouterInfo या LeaseSet के लिए हो सकती थी (एक ही कुंजी स्पेस, अलग करने के लिए कोई फ़्लैग नहीं) - एन्क्रिप्टेड उत्तर केवल तब उपयोगी हैं जब प्रतिक्रिया tunnel के माध्यम से हो - शामिल टैगों की संख्या एक से अधिक हो सकती है यदि वैकल्पिक DHT लुकअप रणनीतियाँ लागू की जाती हैं - लुकअप कुंजी और बहिष्करण कुंजियाँ "वास्तविक" हैश हैं, रूटिंग कुंजियाँ नहीं - प्रकार 3, 5, और 7 (LeaseSet2 variants) 0.9.38 से लौटाए जा सकते हैं। देखें [प्रस्ताव 123](/proposals/123-new-netdb-entries/) - **Exploratory lookup notes (अन्वेषणात्मक लुकअप संबंधी नोट्स):** An exploratory lookup को इस प्रकार परिभाषित किया गया है कि वह कुंजी के निकट गैर-floodfill हैशों की सूची लौटाए। हालांकि, कार्यान्वयन भिन्न हैं: Java एक RI के लिए खोज कुंजी को लुकअप करता है और यदि मौजूद हो तो DatabaseStore लौटाता है; i2pd ऐसा नहीं करता। इसलिए, पहले से प्राप्त हैशों के लिए exploratory lookup का उपयोग करने की अनुशंसा नहीं की जाती।

**स्रोत कोड:** - `net.i2p.data.i2np.DatabaseLookupMessage` - एन्क्रिप्शन: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (डेटाबेस खोज उत्तर) (प्रकार 3)

**उद्देश्य:** विफल DatabaseLookup (डेटाबेस खोज) संदेश के लिए प्रतिक्रिया।

**सामग्री:** अनुरोधित कुंजी के सबसे निकट वाले router हैशों की सूची।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```

**स्रोत कोड:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (डिलिवरी स्थिति) (प्रकार 10)

**उद्देश्य:** एक सरल संदेश पावती। आम तौर पर संदेश प्रेषक द्वारा बनाया जाता है और स्वयं संदेश के साथ इसे Garlic Message में लपेटा जाता है, ताकि गंतव्य द्वारा इसे वापस भेजा जा सके।

**सामग्री:** पहुंचाए गए संदेश का ID और निर्माण या आगमन समय।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**टिप्पणियाँ:** - टाइम स्टैम्प हमेशा निर्माता द्वारा वर्तमान समय पर सेट किया जाता है। हालांकि, कोड में इसके कई उपयोग हैं, और भविष्य में और जोड़े जा सकते हैं - यह संदेश SSU में सत्र स्थापित होने की पुष्टि के रूप में भी उपयोग होता है। इस स्थिति में, संदेश आईडी एक यादृच्छिक संख्या पर सेट की जाती है, और "arrival time" वर्तमान नेटवर्क-व्यापी आईडी पर सेट किया जाता है, जो 2 है (अर्थात, `0x0000000000000002`) - DeliveryStatus (डिलीवरी की पुष्टि वाला संदेश प्रकार) आमतौर पर एक GarlicMessage (कई संदेशों का संकुल) में लपेटकर tunnel के माध्यम से भेजा जाता है ताकि प्रेषक का खुलासा किए बिना पुष्टि प्रदान की जा सके - tunnel परीक्षण में विलंबता और विश्वसनीयता मापने के लिए उपयोग किया जाता है

**स्रोत कोड:** - `net.i2p.data.i2np.DeliveryStatusMessage` - प्रयुक्त स्थान: `net.i2p.router.tunnel.InboundEndpointProcessor` tunnel परीक्षण के लिए

---

### GarlicMessage (लहसुन-आधारित संदेश; प्रकार 11)

**चेतावनी:** यह ElGamal-कूटबद्ध garlic संदेशों के लिए उपयोग किया जाने वाला प्रारूप है। ECIES-AEAD-X25519-Ratchet garlic संदेशों का प्रारूप काफी भिन्न है। आधुनिक प्रारूप के लिए [ECIES विनिर्देश](/docs/specs/ecies/) देखें।

**उद्देश्य:** कई एन्क्रिप्टेड I2NP संदेशों को लपेटने के लिए उपयोग किया जाता है।

**Contents:** डिक्रिप्ट करने पर, Garlic Cloves (Garlic संदेश की इकाइयाँ) और अतिरिक्त डेटा की एक श्रृंखला मिलती है, जिसे Clove Set (इकाइयों का समूह) भी कहा जाता है।

**कूटबद्ध प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**डिक्रिप्टेड डेटा (Clove Set — I2P में garlic encryption संरचना के भीतर कई संदेशों का समूह):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**ECIES-X25519-AEAD-Ratchet प्रारूप के लिए (routers के लिए वर्तमान मानक):**

देखें [ECIES विनिर्देश](/docs/specs/ecies/) और [प्रस्ताव 144](/proposals/144-ecies-x25519-aead-ratchet/).

**स्रोत कोड:** - `net.i2p.data.i2np.GarlicMessage` - एन्क्रिप्शन: `net.i2p.crypto.elgamal.ElGamalAESEngine` (अप्रचलित) - आधुनिक एन्क्रिप्शन: `net.i2p.crypto.ECIES` पैकेज

---

### TunnelData (प्रकार 18)

**उद्देश्य:** एक संदेश जो tunnel के gateway या किसी प्रतिभागी से अगले प्रतिभागी या एंडपॉइंट को भेजा जाता है। डेटा निश्चित लंबाई का होता है, जिसमें खंडित, बैच किए गए, पैड किए गए और एन्क्रिप्टेड I2NP संदेश शामिल होते हैं।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**पेलोड संरचना (1024 बाइट्स):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**टिप्पणियाँ:** - TunnelData के लिए I2NP संदेश आईडी प्रत्येक hop (मार्ग का चरण) पर एक नई यादृच्छिक संख्या पर सेट की जाती है - tunnel संदेश प्रारूप (एन्क्रिप्टेड डेटा के भीतर) [Tunnel Message Specification](/docs/specs/implementation/) में निर्दिष्ट है - प्रत्येक hop AES-256 in CBC mode का उपयोग करके एक परत डिक्रिप्ट करता है - डिक्रिप्ट किए गए डेटा का उपयोग करके IV को प्रत्येक hop पर अपडेट किया जाता है - कुल आकार बिल्कुल 1,028 बाइट (4 tunnelId + 1024 data) है - यह tunnel ट्रैफ़िक की मूलभूत इकाई है - TunnelData संदेश विखंडित I2NP संदेशों (GarlicMessage, DatabaseStore, आदि) को वहन करते हैं

**स्रोत कोड:** - `net.i2p.data.i2np.TunnelDataMessage` - स्थिरांक: `TunnelDataMessage.DATA_LENGTH = 1024` - प्रसंस्करण: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (प्रकार 19)

**उद्देश्य:** tunnel के inbound gateway (आवक प्रवेश-द्वार) पर, tunnel में भेजे जाने हेतु किसी अन्य I2NP संदेश को लपेटता है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**नोट्स:** - पेलोड एक I2NP message है जिसमें मानक 16-बाइट हेडर होता है - स्थानीय router से tunnels में संदेश इंजेक्ट करने के लिए उपयोग किया जाता है - गेटवे आवश्यक होने पर संलग्न संदेश को खंडों में विभाजित करता है - खंडन के बाद, उन खंडों को TunnelData संदेशों में लपेटा जाता है - TunnelGateway कभी नेटवर्क पर नहीं भेजा जाता; यह tunnel प्रसंस्करण से पहले उपयोग किया जाने वाला आंतरिक संदेश प्रकार है

**स्रोत कोड:** - `net.i2p.data.i2np.TunnelGatewayMessage` - प्रसंस्करण: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (डेटा संदेश) (प्रकार 20)

**Purpose:** Garlic Messages (I2P में प्रयुक्त garlic प्रकार के संदेश) और Garlic Cloves (उसी संदेश के उपघटक) द्वारा किसी भी डेटा को लपेटने के लिए उपयोग किया जाता है (आमतौर पर एंड-टू-एंड एन्क्रिप्टेड एप्लिकेशन डेटा)।

**प्रारूप:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**नोट्स:** - इस संदेश में कोई रूटिंग जानकारी नहीं होती और इसे कभी भी "अनरैप्ड" रूप में नहीं भेजा जाएगा - केवल Garlic messages (I2P में प्रयुक्त बहु-संदेश समेकन तकनीक) के भीतर उपयोग होता है - आमतौर पर एंड-टू-एंड एन्क्रिप्टेड एप्लिकेशन डेटा (HTTP, IRC, email, आदि) शामिल होता है - डेटा प्रायः ElGamal/AES या ECIES-एन्क्रिप्टेड पेलोड होता है - tunnel संदेश खंडन सीमाओं के कारण व्यवहारिक अधिकतम लंबाई लगभग 61.2 KB होती है

**स्रोत कोड:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (प्रकार 21)

**अप्रचलित।** VariableTunnelBuild (प्रकार 23) या ShortTunnelBuild (प्रकार 25) का उपयोग करें।

**उद्देश्य:** 8 हॉप्स के लिए निश्चित लंबाई का tunnel निर्माण अनुरोध.

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**टिप्पणियाँ:** - 0.9.48 से, इसमें ECIES-X25519 BuildRequestRecords (बिल्ड अनुरोध रिकॉर्ड्स) शामिल हो सकते हैं। देखें [ECIES Tunnel Creation](/docs/specs/implementation/) - विस्तृत जानकारी के लिए [Tunnel Creation Specification](/docs/specs/implementation/) देखें - इस संदेश के लिए I2NP message ID को tunnel creation specification के अनुसार सेट किया जाना चाहिए - आज के नेटवर्क में यह शायद ही दिखता है (VariableTunnelBuild द्वारा प्रतिस्थापित), फिर भी बहुत लंबे tunnels के लिए इसका उपयोग किया जा सकता है और इसे औपचारिक रूप से अप्रचलित घोषित नहीं किया गया है - Routers को संगतता के लिए इसे अब भी लागू करना आवश्यक है - स्थिर 8-record प्रारूप लचीला नहीं है और छोटे tunnels के लिए बैंडविड्थ बर्बाद करता है

**स्रोत कोड:** - `net.i2p.data.i2np.TunnelBuildMessage` - स्थिरांक: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (प्रकार 22)

**अप्रचलित।** VariableTunnelBuildReply (प्रकार 24) या OutboundTunnelBuildReply (प्रकार 26) का उपयोग करें।

**उद्देश्य:** 8 हॉप्स के लिए निश्चित लंबाई की tunnel build reply (tunnel निर्माण का उत्तर)।

**प्रारूप:**

TunnelBuildMessage के समान प्रारूप, जिसमें BuildRequestRecords के स्थान पर BuildResponseRecords हैं।

```
Total size: 8 × 528 = 4,224 bytes
```
**नोट्स:** - संस्करण 0.9.48 से, इसमें ECIES-X25519 BuildResponseRecords हो सकते हैं। देखें [ECIES Tunnel Creation](/docs/specs/implementation/) - विवरण के लिए देखें [Tunnel Creation Specification](/docs/specs/implementation/) - इस संदेश के लिए I2NP message ID को tunnel निर्माण विनिर्देशन के अनुसार सेट किया जाना चाहिए - आज के नेटवर्क में यह शायद ही दिखाई देता है (VariableTunnelBuildReply द्वारा प्रतिस्थापित), फिर भी बहुत लंबे tunnels के लिए इसका उपयोग किया जा सकता है और इसे औपचारिक रूप से अप्रचलित (deprecated) घोषित नहीं किया गया है - Routers को संगतता के लिए इसे अब भी लागू करना आवश्यक है

**स्रोत कोड:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (परिवर्तनीय tunnel निर्माण) (प्रकार 23)

**उद्देश्य:** 1-8 hops के लिए परिवर्तनीय-लंबाई tunnel निर्माण. ElGamal और ECIES-X25519 दोनों routers का समर्थन करता है.

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**नोट्स:** - संस्करण 0.9.48 से, इसमें ECIES-X25519 BuildRequestRecords (निर्माण अनुरोध रिकॉर्ड) शामिल हो सकते हैं। देखें [ECIES tunnel निर्माण](/docs/specs/implementation/) - router संस्करण 0.7.12 (2009) में प्रस्तुत किया गया - संस्करण 0.7.12 से पुराने संस्करण वाले tunnel प्रतिभागियों को यह भेजा नहीं जा सकता - विवरण हेतु देखें [tunnel निर्माण विशिष्टता](/docs/specs/implementation/) - I2NP संदेश ID को tunnel निर्माण विशिष्टता के अनुसार सेट किया जाना चाहिए - **सामान्य रिकॉर्ड की संख्या:** 4 (एक 4-हॉप tunnel के लिए) - **सामान्य कुल आकार:** 1 + (4 × 528) = 2,113 बाइट्स - यह ElGamal routers के लिए मानक tunnel build संदेश है - ECIES routers सामान्यतः इसके बजाय ShortTunnelBuild (type 25) का उपयोग करते हैं

**स्रोत कोड:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (प्रकार 24)

**उद्देश्य:** 1-8 hops (नेटवर्क में मध्यवर्ती नोड्स) के लिए परिवर्तनीय लंबाई वाला tunnel निर्माण प्रत्युत्तर। दोनों ElGamal और ECIES-X25519 routers का समर्थन करता है।

**प्रारूप:**

VariableTunnelBuildMessage के समान प्रारूप, जिसमें BuildRequestRecords के बजाय BuildResponseRecords होते हैं।

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**टिप्पणियाँ:** - संस्करण 0.9.48 से, इसमें ECIES-X25519 BuildResponseRecords हो सकते हैं। देखें [ECIES Tunnel Creation](/docs/specs/implementation/) - router संस्करण 0.7.12 (2009) में प्रस्तुत किया गया - संस्करण 0.7.12 से पहले के tunnel प्रतिभागियों को यह नहीं भेजा जाना चाहिए - विवरण के लिए [Tunnel Creation Specification](/docs/specs/implementation/) देखें - tunnel निर्माण विशिष्टता के अनुसार I2NP (I2P का नेटवर्क प्रोटोकॉल) संदेश ID सेट किया जाना चाहिए - **रिकॉर्डों की सामान्य संख्या:** 4 - **सामान्य कुल आकार:** 2,113 बाइट्स

**स्रोत कोड:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (प्रकार 25)

**उद्देश्य:** केवल ECIES-X25519 (एक एलिप्टिक-वक्र-आधारित एन्क्रिप्शन स्कीम) routers के लिए छोटे tunnel build संदेश। API संस्करण 0.9.51 (रिलीज़ 1.5.0, अगस्त 2021) में प्रस्तुत। यह ECIES tunnel builds के लिए वर्तमान मानक है।

**प्रारूप:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**टिप्पणियाँ:** - router संस्करण 0.9.51 में प्रस्तुत किया गया (रिलीज़ 1.5.0, अगस्त 2021) - API संस्करण 0.9.51 से पहले tunnel प्रतिभागियों को भेजा नहीं जा सकता - पूर्ण विनिर्देशन के लिए [ECIES Tunnel निर्माण](/docs/specs/implementation/) देखें - औचित्य के लिए [प्रस्ताव 157](/proposals/157-new-tbm/) देखें - **रिकॉर्डों की सामान्य संख्या:** 4 - **सामान्य कुल आकार:** 1 + (4 × 218) = 873 बाइट्स - **बैंडविड्थ बचत:** VariableTunnelBuild (I2P में tunnel निर्माण संदेश का एक प्रकार) की तुलना में 59% छोटा (873 बनाम 2,113 बाइट्स) - **प्रदर्शन लाभ:** 4 छोटे रिकॉर्ड एक tunnel संदेश में समा जाते हैं; VariableTunnelBuild को 3 tunnel संदेशों की आवश्यकता होती है - अब यह शुद्ध ECIES-X25519 tunnels के लिए मानक tunnel build प्रारूप है - रिकॉर्ड कुंजियाँ स्पष्ट रूप से शामिल करने के बजाय HKDF के माध्यम से व्युत्पन्न करते हैं

**स्रोत कोड:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - स्थिरांक: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (प्रकार 26)

**उद्देश्य:** नए tunnel के आउटबाउंड एंडपॉइंट से प्रारंभकर्ता को भेजा जाता है। केवल ECIES-X25519 routers के लिए। API संस्करण 0.9.51 (रिलीज़ 1.5.0, अगस्त 2021) में पेश किया गया।

**प्रारूप:**

ShortTunnelBuildMessage के समान प्रारूप, जिसमें ShortBuildRequestRecords के बजाय ShortBuildResponseRecords हैं।

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**टिप्पणियाँ:** - इसका परिचय router संस्करण 0.9.51 में हुआ (रिलीज़ 1.5.0, अगस्त 2021) - पूर्ण विनिर्देशन के लिए [ECIES Tunnel Creation](/docs/specs/implementation/) देखें - **रिकॉर्ड की सामान्य संख्या:** 4 - **कुल सामान्य आकार:** 873 बाइट्स - यह उत्तर नव-निर्मित आउटबाउंड tunnel के माध्यम से आउटबाउंड एंडपॉइंट (OBEP) से वापस tunnel निर्माता को भेजा जाता है - यह पुष्टि करता है कि सभी हॉप्स ने tunnel build स्वीकार कर लिया है

**स्रोत कोड:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## संदर्भ

### आधिकारिक विनिर्देश

- **[I2NP विनिर्देश](/docs/specs/i2np/)** - I2NP संदेश प्रारूप का पूर्ण विनिर्देश
- **[सामान्य संरचनाएँ](/docs/specs/common-structures/)** - I2P में प्रयुक्त डेटा प्रकार और संरचनाएँ
- **[Tunnel निर्माण](/docs/specs/implementation/)** - ElGamal (एक सार्वजनिक-कुंजी क्रिप्टोसिस्टम) tunnel निर्माण (अप्रचलित)
- **[ECIES Tunnel निर्माण](/docs/specs/implementation/)** - ECIES-X25519 tunnel निर्माण (वर्तमान)
- **[Tunnel संदेश](/docs/specs/implementation/)** - Tunnel संदेश प्रारूप और वितरण निर्देश
- **[NTCP2 विनिर्देश](/docs/specs/ntcp2/)** - TCP परिवहन प्रोटोकॉल
- **[SSU2 विनिर्देश](/docs/specs/ssu2/)** - UDP परिवहन प्रोटोकॉल
- **[ECIES विनिर्देश](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet एन्क्रिप्शन
- **[क्रिप्टोग्राफी विनिर्देश](/docs/specs/cryptography/)** - निम्न-स्तरीय क्रिप्टोग्राफिक प्रिमिटिव्स
- **[I2CP विनिर्देश](/docs/specs/i2cp/)** - क्लाइंट प्रोटोकॉल विनिर्देश
- **[डेटाग्राम विनिर्देश](/docs/api/datagrams/)** - Datagram2 और Datagram3 प्रारूप

### प्रस्ताव

- **[प्रस्ताव 123](/proposals/123-new-netdb-entries/)** - नई netDB प्रविष्टियाँ (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[प्रस्ताव 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet एन्क्रिप्शन
- **[प्रस्ताव 154](/proposals/154-ecies-lookups/)** - एन्क्रिप्टेड डेटाबेस लुकअप
- **[प्रस्ताव 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[प्रस्ताव 157](/proposals/157-new-tbm/)** - छोटे tunnel निर्माण संदेश (संक्षिप्त प्रारूप)
- **[प्रस्ताव 159](/proposals/159-ssu2/)** - SSU2 ट्रांसपोर्ट
- **[प्रस्ताव 161](/hi/proposals/161-ri-dest-padding/)** - कम्प्रेस करने योग्य पैडिंग
- **[प्रस्ताव 163](/proposals/163-datagram2/)** - डेटाग्राम2 और डेटाग्राम3
- **[प्रस्ताव 167](/proposals/167-service-records/)** - LeaseSet सर्विस रिकॉर्ड पैरामीटर
- **[प्रस्ताव 168](/proposals/168-tunnel-bandwidth/)** - Tunnel निर्माण बैंडविड्थ पैरामीटर
- **[प्रस्ताव 169](/proposals/169-pq-crypto/)** - पोस्ट-क्वांटम हाइब्रिड क्रिप्टोग्राफी

### प्रलेखन

- **[Garlic Routing](/docs/overview/garlic-routing/)** - परतदार संदेश बंडलिंग
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - अप्रचलित एन्क्रिप्शन योजना
- **[Tunnel Implementation](/docs/specs/implementation/)** - खंडन और प्रसंस्करण
- **[Network Database](/docs/specs/common-structures/)** - वितरित हैश तालिका
- **[NTCP2 Transport](/docs/specs/ntcp2/)** - TCP ट्रांसपोर्ट विनिर्देश
- **[SSU2 Transport](/docs/specs/ssu2/)** - UDP ट्रांसपोर्ट विनिर्देश
- **[Technical Introduction](/docs/overview/tech-intro/)** - I2P आर्किटेक्चर का अवलोकन

### स्रोत कोड

- **[Java I2P रिपॉज़िटरी](https://i2pgit.org/I2P_Developers/i2p.i2p)** - आधिकारिक Java कार्यान्वयन
- **[GitHub मिरर](https://github.com/i2p/i2p.i2p)** - Java I2P का GitHub मिरर
- **[i2pd रिपॉज़िटरी](https://github.com/PurpleI2P/i2pd)** - C++ कार्यान्वयन

### मुख्य स्रोत कोड स्थान

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - I2NP संदेश कार्यान्वयन - `core/java/src/net/i2p/crypto/` - क्रिप्टोग्राफिक कार्यान्वयन - `router/java/src/net/i2p/router/tunnel/` - Tunnel प्रसंस्करण - `router/java/src/net/i2p/router/transport/` - परिवहन कार्यान्वयन

**स्थिरांक और मान:** - `I2NPMessage.MAX_SIZE = 65536` - अधिकतम I2NP संदेश आकार - `I2NPMessageImpl.HEADER_LENGTH = 16` - मानक हेडर आकार - `TunnelDataMessage.DATA_LENGTH = 1024` - tunnel संदेश पेलोड - `EncryptedBuildRecord.RECORD_SIZE = 528` - लंबा बिल्ड रिकॉर्ड - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - छोटा बिल्ड रिकॉर्ड - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - प्रति बिल्ड अधिकतम रिकॉर्ड

---

## परिशिष्ट A: नेटवर्क सांख्यिकी और वर्तमान स्थिति

### नेटवर्क संरचना (अक्टूबर 2025 तक)

- **कुल routers:** लगभग 60,000-70,000 (बदलता रहता है)
- **Floodfill routers:** लगभग 500-700 सक्रिय
- **एन्क्रिप्शन प्रकार:**
  - ECIES-X25519: routers में से >95%
  - ElGamal: routers में से <5% (अप्रचलित, केवल पुरानी संगतता के लिए)
- **ट्रांसपोर्ट अपनाना:**
  - SSU2: >60% प्राथमिक ट्रांसपोर्ट
  - NTCP2: ~40% प्राथमिक ट्रांसपोर्ट
  - पुराने ट्रांसपोर्ट (SSU1, NTCP): 0% (हटाए गए)
- **हस्ताक्षर प्रकार:**
  - EdDSA (Ed25519): अधिकांश
  - ECDSA: कम प्रतिशत
  - RSA: निषिद्ध (हटाया गया)

### न्यूनतम Router आवश्यकताएँ

- **API संस्करण:** 0.9.16+ (नेटवर्क के साथ EdDSA (Elliptic Curve Digital Signature Algorithm — अण्डाकार वक्र डिजिटल हस्ताक्षर एल्गोरिद्म) संगतता हेतु)
- **अनुशंसित न्यूनतम:** API 0.9.51+ (ECIES (Elliptic Curve Integrated Encryption Scheme — अण्डाकार वक्र एकीकृत एन्क्रिप्शन योजना) short tunnel बिल्ड्स)
- **floodfills के लिए वर्तमान न्यूनतम:** API 0.9.58+ (ElGamal (एन्क्रिप्शन एल्गोरिद्म) router का अप्रचलन)
- **आगामी आवश्यकता:** Java 17+ (रिलीज़ 2.11.0, दिसंबर 2025 से)

### बैंडविड्थ आवश्यकताएँ

- **न्यूनतम:** 128 KBytes/sec (N flag या उससे अधिक) floodfill के लिए
- **अनुशंसित:** 256 KBytes/sec (O flag) या उससे अधिक
- **Floodfill आवश्यकताएँ:**
  - न्यूनतम 128 KB/sec बैंडविड्थ
  - स्थिर अपटाइम (>95% अनुशंसित)
  - कम लैटेंसी (<500ms पीयर्स तक)
  - हेल्थ परीक्षण पास करें (क्यू समय, जॉब लैग)

### Tunnel सांख्यिकी

- **सामान्य tunnel लंबाई:** 3-4 hops (बीच के नोड/कदम)
- **अधिकतम tunnel लंबाई:** 8 hops (सैद्धांतिक, बहुत कम उपयोग)
- **सामान्य tunnel जीवनकाल:** 10 मिनट
- **Tunnel निर्माण सफलता दर:** >85% अच्छी तरह से जुड़े हुए routers के लिए
- **Tunnel निर्माण संदेश प्रारूप:**
  - ECIES routers: ShortTunnelBuild (218-byte रिकॉर्ड्स)
  - मिश्रित tunnels: VariableTunnelBuild (528-byte रिकॉर्ड्स)

### प्रदर्शन मेट्रिक्स

- **Tunnel निर्माण समय:** 1-3 सेकंड (सामान्यतः)
- **एंड-टू-एंड विलंबता:** 0.5-2 सेकंड (सामान्यतः, कुल 6-8 हॉप्स)
- **थ्रूपुट:** Tunnel बैंडविड्थ द्वारा सीमित (सामान्यतः प्रति tunnel 10-50 KB/sec)
- **अधिकतम डेटाग्राम आकार:** 10 KB अनुशंसित (61.2 KB सैद्धांतिक अधिकतम)

---

## परिशिष्ट बी: अप्रचलित और हटाई गई विशेषताएँ

### पूरी तरह हटाया गया (अब समर्थित नहीं है)

- **NTCP transport** - रिलीज़ 0.9.50 (मई 2021) में हटाया गया
- **SSU v1 transport** - Java I2P से रिलीज़ 2.4.0 (दिसंबर 2023) में हटाया गया
- **SSU v1 transport** - i2pd से रिलीज़ 2.44.0 (नवंबर 2022) में हटाया गया
- **RSA signature types** - API 0.9.28 से निषिद्ध

### अप्रचलित (समर्थित लेकिन अनुशंसित नहीं)

- **ElGamal routers** - API 0.9.58 (मार्च 2023) से अप्रचलित
  - पश्च-संगतता के लिए ElGamal destinations अब भी समर्थित हैं
  - नए routers को केवल ECIES-X25519 का उपयोग करना चाहिए
- **TunnelBuild (प्रकार 21)** - VariableTunnelBuild और ShortTunnelBuild के पक्ष में अप्रचलित
  - बहुत लंबे tunnels (>8 हॉप्स) के लिए अब भी कार्यान्वित है
- **TunnelBuildReply (प्रकार 22)** - VariableTunnelBuildReply और OutboundTunnelBuildReply के पक्ष में अप्रचलित
- **ElGamal/AES एन्क्रिप्शन** - ECIES-X25519-AEAD-Ratchet के पक्ष में अप्रचलित
  - लेगेसी destinations के लिए अब भी उपयोग किया जाता है
- **लंबे ECIES BuildRequestRecords (528 bytes)** - छोटे प्रारूप (218 bytes) के पक्ष में अप्रचलित
  - ElGamal हॉप्स वाले मिश्रित tunnels में अब भी उपयोग किया जाता है

### लेगेसी समर्थन की समयरेखा

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## परिशिष्ट C: आगामी विकास

### Post-Quantum Cryptography (क्वांटम-पश्चात कूटलेखन)

**स्थिति:** रिलीज़ 2.10.0 (सितंबर 2025) से बीटा, 2.11.0 (दिसंबर 2025) में डिफ़ॉल्ट बन जाएगा

**कार्यान्वयन:** - पारंपरिक X25519 और पोस्ट-क्वांटम MLKEM (ML-KEM-768) को संयोजित करने वाला हाइब्रिड दृष्टिकोण - मौजूदा ECIES-X25519 इन्फ्रास्ट्रक्चर के साथ बैकवर्ड-कम्पैटिबल - Signal Double Ratchet (Signal प्रोटोकॉल का डबल रैचेट एल्गोरिदम) का उपयोग, जिसमें पारंपरिक और PQ (पोस्ट-क्वांटम) दोनों प्रकार की कुंजी सामग्री होती है - विवरण के लिए [Proposal 169](/proposals/169-pq-crypto/) देखें

**स्थानांतरण मार्ग:** 1. रिलीज़ 2.10.0 (सितंबर 2025): बीटा विकल्प के रूप में उपलब्ध 2. रिलीज़ 2.11.0 (दिसंबर 2025): डिफ़ॉल्ट रूप से सक्षम 3. भविष्य की रिलीज़: अंततः अनिवार्य

### योजना की गई विशेषताएँ

- **IPv6 सुधार** - बेहतर IPv6 समर्थन और संक्रमण तंत्र
- **प्रति tunnel throttling (गति सीमित करना)** - प्रति tunnel सूक्ष्म-स्तरीय बैंडविड्थ नियंत्रण
- **उन्नत मेट्रिक्स** - बेहतर प्रदर्शन निगरानी और निदान
- **प्रोटोकॉल अनुकूलन** - कम ओवरहेड और बेहतर दक्षता
- **बेहतर floodfill चयन** - बेहतर नेटवर्क डेटाबेस वितरण

### अनुसंधान क्षेत्र

- **Tunnel की लंबाई का अनुकूलन** - खतरे के मॉडल के आधार पर गतिशील tunnel की लंबाई
- **उन्नत पैडिंग** - ट्रैफिक विश्लेषण प्रतिरोध में सुधार
- **नई एन्क्रिप्शन योजनाएँ** - क्वांटम कंप्यूटिंग खतरों के लिए तैयारी
- **भीड़ नियंत्रण** - नेटवर्क लोड के बेहतर प्रबंधन
- **मोबाइल समर्थन** - मोबाइल डिवाइसों और नेटवर्क के लिए अनुकूलन

---

## परिशिष्ट D: कार्यान्वयन दिशानिर्देश

### नए कार्यान्वयन के लिए

**न्यूनतम आवश्यकताएँ:** 1. API संस्करण 0.9.51+ की विशेषताओं का समर्थन करें 2. ECIES-X25519-AEAD-Ratchet एन्क्रिप्शन को लागू करें 3. NTCP2 और SSU2 ट्रांसपोर्ट्स का समर्थन करें 4. ShortTunnelBuild संदेशों को लागू करें (218-बाइट रिकॉर्ड्स) 5. LeaseSet2 वैरिएंट्स का समर्थन करें (प्रकार 3, 5, 7) 6. EdDSA हस्ताक्षरों का उपयोग करें (Ed25519)

**अनुशंसित:** 1. post-quantum hybrid cryptography (पोस्ट-क्वांटम खतरों-रोधी मिश्रित क्रिप्टोग्राफी) का समर्थन करें (संस्करण 2.11.0 से) 2. प्रति-tunnel बैंडविड्थ पैरामीटर लागू करें 3. Datagram2 और Datagram3 प्रारूप का समर्थन करें 4. LeaseSets में सेवा रिकॉर्ड विकल्प लागू करें 5. /docs/specs/ पर आधिकारिक विनिर्देशों का पालन करें

**आवश्यक नहीं:** 1. ElGamal router का समर्थन (अप्रचलित) 2. पुराने ट्रांसपोर्ट का समर्थन (SSU1, NTCP) 3. लंबे ECIES BuildRequestRecords (शुद्ध ECIES tunnels के लिए 528 bytes) 4. TunnelBuild/TunnelBuildReply संदेश (Variable या Short वैरिएंट का उपयोग करें)

### परीक्षण और सत्यापन

**प्रोटोकॉल अनुपालन:** 1. आधिकारिक Java I2P router के साथ अंतरसंचालनीयता का परीक्षण करें 2. i2pd C++ router के साथ अंतरसंचालनीयता का परीक्षण करें 3. विनिर्देशों के अनुरूप संदेश प्रारूपों को सत्यापित करें 4. tunnel निर्माण/विघटन चक्रों का परीक्षण करें 5. परीक्षण वेक्टर के साथ एन्क्रिप्शन/डीक्रिप्शन सत्यापित करें

**प्रदर्शन परीक्षण:** 1. tunnel निर्माण की सफलता दर मापें (>85% होना चाहिए) 2. विभिन्न tunnel लंबाइयों के साथ परीक्षण करें (2-8 हॉप्स) 3. खंडीकरण और पुनर्संयोजन को सत्यापित करें 4. लोड के तहत परीक्षण करें (एक साथ कई tunnels) 5. एंड-टू-एंड विलंबता मापें

**सुरक्षा परीक्षण:** 1. एन्क्रिप्शन के कार्यान्वयन को सत्यापित करें (test vectors (मानक परीक्षण इनपुट-आउटपुट सेट) का उपयोग करें) 2. replay attack (पुराने संदेश को फिर से भेजकर किया गया हमला) की रोकथाम का परीक्षण करें 3. संदेश समाप्ति के प्रबंधन को सत्यापित करें 4. गलत स्वरूप वाले संदेशों के विरुद्ध परीक्षण करें 5. उचित यादृच्छिक संख्या जनन को सत्यापित करें

### कार्यान्वयन में आम गलतियाँ

1. **भ्रमित करने वाले डिलीवरी निर्देश फॉर्मेट** - Garlic clove ('garlic' संदेश का 'clove' घटक) बनाम tunnel message
2. **गलत कुंजी व्युत्पत्ति** - शॉर्ट बिल्ड रिकॉर्ड्स के लिए HKDF (HMAC-आधारित कुंजी व्युत्पन्न फ़ंक्शन) का उपयोग
3. **Message ID हैंडलिंग** - tunnel builds के लिए सही तरीके से सेट नहीं किया जा रहा है
4. **फ्रैग्मेंटेशन समस्याएँ** - 61.2 KB की व्यावहारिक सीमा का पालन नहीं किया जा रहा
5. **Endianness (बाइट क्रम) त्रुटियाँ** - Java सभी पूर्णांकों के लिए big-endian का उपयोग करता है
6. **समाप्ति हैंडलिंग** - शॉर्ट फॉर्मेट 7 फरवरी, 2106 को रैप हो जाता है
7. **Checksum जनरेशन** - सत्यापित न होने पर भी आवश्यक
