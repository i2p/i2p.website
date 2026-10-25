---
title: "पुराना Tunnel कार्यान्वयन"
description: "I2P के मूल tunnel implementation का ऐतिहासिक दस्तावेजीकरण 0.6.1.10 से पहले"
slug: "old-tunnel-implementation"
aliases:
  - "/hi/docs/historical/tunnel-alt"
  - "/hi/docs/historical/tunnel-alt/"
  - "/hi/tunnel"
  - "/hi/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**नोट: अप्रचलित - उपयोग नहीं किया जाता! 0.6.1.10 में बदला गया - सक्रिय विनिर्देश के लिए [वर्तमान कार्यान्वयन](/docs/specs/tunnel-implementation) देखें।**

## 1) Tunnel अवलोकन {#tunnel.overview}

I2P के भीतर, संदेश peers की एक आभासी tunnel के माध्यम से एक दिशा में पारित किए जाते हैं, संदेश को अगली hop तक पहुंचाने के लिए उपलब्ध किसी भी साधन का उपयोग करते हुए। संदेश tunnel के gateway पर पहुंचते हैं, path के लिए bundled हो जाते हैं, और tunnel में अगली hop को forward कर दिए जाते हैं, जो संदेश की वैधता को process और verify करती है और इसे अगली hop को भेजती है, और इसी तरह यह तब तक चलता रहता है जब तक यह tunnel endpoint तक नहीं पहुंच जाता। यह endpoint gateway द्वारा bundled किए गए संदेशों को लेता है और उन्हें निर्देशानुसार forward करता है - या तो किसी अन्य router को, किसी अन्य router पर किसी अन्य tunnel को, या स्थानीय रूप से।

सभी tunnel एक समान काम करते हैं, लेकिन इन्हें दो अलग समूहों में विभाजित किया जा सकता है - inbound tunnel और outbound tunnel। inbound tunnel में एक अविश्वसनीय gateway होता है जो संदेशों को tunnel creator की ओर भेजता है, जो tunnel endpoint का काम करता है। outbound tunnel के लिए, tunnel creator gateway का काम करता है, संदेशों को remote endpoint तक पहुंचाता है।

tunnel का निर्माता ठीक-ठीक यह चुनता है कि कौन से peers tunnel में भाग लेंगे, और हर एक को आवश्यक configuration data प्रदान करता है। ये लंबाई में 0 hops (जहाँ gateway भी endpoint है) से लेकर 7 hops (जहाँ gateway के बाद और endpoint से पहले 6 peers हैं) तक हो सकते हैं। इसका उद्देश्य यह है कि प्रतिभागियों या तीसरे पक्ष के लिए tunnel की लंबाई निर्धारित करना कठिन हो, या यहाँ तक कि मिलकर काम करने वाले प्रतिभागियों के लिए भी यह पता लगाना मुश्किल हो कि वे एक ही tunnel का हिस्सा हैं या नहीं (उस स्थिति को छोड़कर जहाँ मिलकर काम करने वाले peers tunnel में एक-दूसरे के बगल में हैं)। Messages जो भ्रष्ट हो गए हैं, उन्हें भी जल्द से जल्द drop कर दिया जाता है, जिससे network load कम हो जाता है।

उनकी लंबाई के अलावा, प्रत्येक tunnel के लिए अतिरिक्त कॉन्फ़िगरेबल पैरामीटर हैं जिनका उपयोग किया जा सकता है, जैसे कि वितरित संदेशों के आकार या आवृत्ति पर थ्रॉटल, पैडिंग का उपयोग कैसे किया जाना चाहिए, tunnel कितने समय तक संचालन में रहना चाहिए, चाफ़ संदेशों को इंजेक्ट करना है या नहीं, fragmentation का उपयोग करना है या नहीं, और यदि कोई हो तो कौन सी batching रणनीतियों को अपनाया जाना चाहिए।

व्यवहार में, विभिन्न उद्देश्यों के लिए tunnel pools की एक श्रृंखला का उपयोग किया जाता है - प्रत्येक स्थानीय client destination के पास अपने स्वयं के inbound tunnels और outbound tunnels का सेट होता है, जो इसकी गुमनामी और प्रदर्शन आवश्यकताओं को पूरा करने के लिए कॉन्फ़िगर किया जाता है। इसके अतिरिक्त, router स्वयं network database में भाग लेने और tunnels को प्रबंधित करने के लिए pools की एक श्रृंखला बनाए रखता है।

I2P एक स्वाभाविक रूप से packet switched network है, इन tunnels के साथ भी, जो इसे समानांतर में चलने वाले कई tunnels का लाभ उठाने की अनुमति देता है, resilience बढ़ाता है और load को संतुलित करता है। मुख्य I2P layer के बाहर, client applications के लिए एक वैकल्पिक end to end streaming library उपलब्ध है, जो TCP-जैसा operation प्रदान करती है, जिसमें message reordering, retransmission, congestion control आदि शामिल है।

## 2) Tunnel संचालन {#tunnel.operation}

Tunnel संचालन में चार अलग प्रक्रियाएं होती हैं, जो tunnel के विभिन्न peers द्वारा की जाती हैं। पहले, tunnel gateway कई tunnel संदेशों को एकत्र करता है और उन्हें tunnel delivery के लिए प्रीप्रोसेस करता है। इसके बाद, वह gateway उस प्रीप्रोसेस किए गए डेटा को encrypt करता है, फिर इसे पहले hop को forward करता है। वह peer, और बाद के tunnel प्रतिभागी, encryption की एक परत को unwrap करते हैं, संदेश की integrity को verify करते हैं, फिर इसे अगले peer को forward करते हैं। अंततः, संदेश endpoint पर पहुंचता है जहां gateway द्वारा bundled किए गए संदेश फिर से अलग किए जाते हैं और अनुरोध के अनुसार forward किए जाते हैं।

Tunnel ID 4 बाइट संख्याएं हैं जो प्रत्येक hop पर उपयोग की जाती हैं - प्रतिभागी जानते हैं कि किस tunnel ID के साथ संदेशों को सुनना है और अगले hop पर आगे भेजने के लिए किस tunnel ID का उपयोग करना चाहिए। Tunnel स्वयं अल्पकालिक होती हैं (वर्तमान में 10 मिनट), लेकिन tunnel के उद्देश्य के आधार पर, और हालांकि बाद की tunnel समान peers के अनुक्रम का उपयोग करके बनाई जा सकती हैं, प्रत्येक hop की tunnel ID बदल जाएगी।

### 2.1) संदेश प्रीप्रोसेसिंग {#tunnel.preprocessing}

जब gateway tunnel के माध्यम से data deliver करना चाहता है, तो यह पहले शून्य या अधिक I2NP messages एकत्र करता है (32KB से अधिक नहीं), चुनता है कि कितना padding उपयोग किया जाएगा, और तय करता है कि प्रत्येक I2NP message को tunnel endpoint द्वारा कैसे handle किया जाना चाहिए, उस data को raw tunnel payload में encode करते हुए:

- 2 byte unsigned integer जो padding bytes की संख्या निर्दिष्ट करता है
- उतने ही random bytes
- शून्य या अधिक { instructions, message } जोड़ों की श्रृंखला

निर्देश इस प्रकार एन्कोड किए गए हैं:

- 1 byte value:
  ```
  bits 0-1: delivery type
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: delay included?  (1 = true, 0 = false)
     bit 3: fragmented?  (1 = true, 0 = false)
     bit 4: extended options?  (1 = true, 0 = false)
  bits 5-7: reserved
  ```
- यदि delivery type TUNNEL था, तो एक 4 byte tunnel ID
- यदि delivery type TUNNEL या ROUTER था, तो एक 32 byte router hash
- यदि delay included flag true है, तो एक 1 byte value:
  ```
     bit 0: type (0 = strict, 1 = randomized)
  bits 1-7: delay exponent (2^value minutes)
  ```
- यदि fragmented flag true है, तो एक 4 byte message ID, और एक 1 byte value:
  ```
  bits 0-6: fragment number
     bit 7: is last?  (1 = true, 0 = false)
  ```
- यदि extended options flag true है:
  ```
  = एक 1 byte option size (bytes में)
  = उतने bytes
  ```
- I2NP message का 2 byte size

I2NP संदेश को उसके मानक रूप में एन्कोड किया जाता है, और पूर्व-प्रसंस्कृत पेलोड को 16 बाइट्स के गुणज तक पैड करना होगा।

### 2.2) Gateway प्रसंस्करण {#tunnel.gateway}

संदेशों के padded payload में preprocessing के बाद, gateway आठ keys के साथ payload को encrypt करता है, एक checksum block बनाता है ताकि हर peer किसी भी समय payload की integrity को verify कर सके, साथ ही tunnel endpoint के लिए एक end to end verification block भी बनाता है जो checksum block की integrity को verify कर सके। विशिष्ट विवरण नीचे दिए गए हैं।

उपयोग की जाने वाली encryption इस प्रकार की है कि decryption के लिए केवल AES को CBC mode में data पर चलाने, message के एक निश्चित fixed portion (bytes 16 से $size-144 तक) का SHA256 calculate करने, और checksum block में उस hash के पहले 16 bytes को खोजने की आवश्यकता होती है। एक fixed संख्या में hops defined हैं (8 peers) ताकि हम tunnel में position को leak किए बिना या layers के peel off होने पर message को लगातार "shrink" हुए बिना message को verify कर सकें। 8 hops से छोटी tunnels के लिए, tunnel creator अतिरिक्त hops की जगह लेगा और अपनी keys के साथ decrypt करेगा (outbound tunnels के लिए, यह शुरुआत में किया जाता है, और inbound tunnels के लिए, अंत में)।

एन्क्रिप्शन में कठिन हिस्सा उस उलझे हुए checksum block का निर्माण है, जिसके लिए मूल रूप से यह पता लगाना आवश्यक है कि प्रत्येक चरण में payload का hash कैसा दिखेगा, उन hashes को बेतरतीब ढंग से व्यवस्थित करना, फिर एक matrix बनाना कि उन बेतरतीब ढंग से व्यवस्थित hashes में से प्रत्येक प्रत्येक चरण में कैसा दिखेगा। Gateway को स्वयं यह दिखावा करना चाहिए कि वह checksum block के भीतर peers में से एक है ताकि पहला hop यह नहीं बता सके कि पिछला hop gateway था। इसे थोड़ा दृश्य रूप में समझने के लिए:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
उपरोक्त में, P[7] मूल डेटा के समान है जो tunnel के माध्यम से पारित किया जा रहा है (preprocessed messages), और V[7] peer7 पर decryption के बाद देखे गए eH[0-7] के SHA256 के पहले 16 bytes हैं। matrix में hash से "ऊपर" वाली cells के लिए, उनका मान उसके नीचे की cell को उसके नीचे वाले peer की key से encrypt करके प्राप्त किया जाता है, जिसमें उसके बाईं ओर के column के अंत का उपयोग IV के रूप में किया जाता है। matrix में hash से "नीचे" वाली cells के लिए, वे उनके ऊपर वाली cell के बराबर होती हैं, जो वर्तमान peer की key द्वारा decrypt की गई होती हैं, जिसमें उस row पर पिछले encrypted block के अंत का उपयोग किया जाता है।

checksum blocks के इस randomized matrix के साथ, प्रत्येक peer payload का hash खोजने में सक्षम होगा, या यदि यह वहाँ नहीं है, तो यह जान जाएगा कि message corrupt है। CBC mode का उपयोग करके entanglement checksum blocks को स्वयं tag करने में कठिनाई बढ़ाता है, लेकिन यह अभी भी संभव है कि यह tagging कुछ समय के लिए undetected रह जाए यदि tagged data के बाद के columns का उपयोग पहले से ही किसी peer पर payload को check करने के लिए किया गया हो। किसी भी स्थिति में, tunnel endpoint (peer 7) निश्चित रूप से जानता है कि क्या कोई भी checksum blocks tagged हुए हैं, क्योंकि यह verification block (V[7]) को corrupt कर देगा।

IV[0] एक यादृच्छिक 16 बाइट मान है, और IV[i] H(D(IV[i-1], K[i-1]) xor IV_WHITENER) के पहले 16 बाइट्स हैं। हम पथ के साथ समान IV का उपयोग नहीं करते हैं, क्योंकि यह तुच्छ मिलीभगत की अनुमति देगा, और हम key leakage को बाधित करने के लिए IV को प्रसारित करने हेतु डिक्रिप्टेड मान के hash का उपयोग करते हैं। IV_WHITENER एक निश्चित 16 बाइट मान है।

जब gateway संदेश भेजना चाहता है, तो वे उस peer के लिए सही row को export करते हैं जो पहला hop है (आमतौर पर peer1.recv row) और उसे पूरी तरह से forward करते हैं।

### 2.3) प्रतिभागी प्रसंस्करण {#tunnel.participant}

जब tunnel में कोई participant एक message प्राप्त करता है, तो वे अपनी tunnel key के साथ एक layer को decrypt करते हैं, AES256 का उपयोग करके CBC mode में पहले 16 bytes को IV के रूप में लेकर। फिर वे payload के रूप में जो देखते हैं उसका hash calculate करते हैं (bytes 16 से $size-144 तक) और उस hash के पहले 16 bytes को decrypted checksum block के भीतर खोजते हैं। यदि कोई match नहीं मिलता, तो message को discard कर दिया जाता है। अन्यथा, IV को update किया जाता है इसे decrypt करके, उस value को IV_WHITENER के साथ XOR करके, और इसे उसके hash के पहले 16 bytes से replace करके। परिणामी message को फिर processing के लिए अगले peer को forward कर दिया जाता है।

tunnel स्तर पर replay attacks को रोकने के लिए, प्रत्येक प्रतिभागी tunnel के जीवनकाल के दौरान प्राप्त IVs का ट्रैक रखता है और डुप्लिकेट्स को अस्वीकार करता है। आवश्यक मेमोरी उपयोग न्यूनतम होना चाहिए, क्योंकि प्रत्येक tunnel का जीवनकाल बहुत छोटा होता है (वर्तमान में 10m)। पूर्ण 32KB संदेशों के साथ tunnel के माध्यम से निरंतर 100KBps की गति से 1875 संदेश आएंगे, जिसके लिए 30KB से कम मेमोरी की आवश्यकता होगी। Gateways और endpoints tunnel में समाहित I2NP संदेशों पर message IDs और expirations को ट्रैक करके replay को handle करते हैं।

### 2.4) एंडपॉइंट प्रसंस्करण {#tunnel.endpoint}

जब एक संदेश tunnel endpoint पर पहुंचता है, तो वे इसे एक सामान्य प्रतिभागी की तरह decrypt और verify करते हैं। यदि checksum block में एक वैध मैच है, तो endpoint फिर checksum block का hash स्वयं compute करता है (जैसा कि decryption के बाद देखा गया) और उसकी तुलना decrypted verification hash (अंतिम 16 bytes) से करता है। यदि वह verification hash मैच नहीं करता, तो endpoint tunnel प्रतिभागियों में से एक द्वारा tagging के प्रयास को नोट करता है और संभवतः संदेश को discard कर देता है।

इस बिंदु पर, tunnel endpoint के पास gateway द्वारा भेजा गया preprocessed data होता है, जिसे वह फिर included I2NP messages में parse कर सकता है और उनके delivery instructions के अनुसार आगे forward कर सकता है।

### 2.5) पैडिंग {#tunnel.padding}

कई tunnel padding रणनीतियां संभव हैं, जिनमें से प्रत्येक के अपने फायदे हैं:

- कोई padding नहीं
- एक यादृच्छिक आकार में padding
- एक निश्चित आकार में padding
- निकटतम KB में padding
- निकटतम घातांक आकार में padding (2^n bytes)

*कौन सा उपयोग करें? no padding सबसे कुशल है, random padding वह है जो हमारे पास अभी है, fixed size या तो एक अत्यधिक बर्बादी होगी या हमें fragmentation को implement करने के लिए मजबूर करेगी। निकटतम exponential size तक padding करना (Freenet की तरह) आशाजनक लगता है। शायद हमें नेटवर्क पर कुछ आंकड़े इकट्ठे करने चाहिए कि messages का आकार क्या होता है, फिर देखना चाहिए कि अलग-अलग रणनीतियों से क्या लागत और फायदे होंगे?*

### 2.6) टनल विखंडन {#tunnel.fragmentation}

विभिन्न padding और mixing योजनाओं के लिए, गुमनामी के दृष्टिकोण से यह उपयोगी हो सकता है कि एक I2NP संदेश को कई भागों में विभाजित किया जाए, जिसमें प्रत्येक को अलग-अलग tunnel संदेशों के माध्यम से अलग-अलग वितरित किया जाए। endpoint इस fragmentation का समर्थन कर भी सकता है और नहीं भी (आवश्यकता के अनुसार fragments को छोड़ना या रखना), और fragmentation को संभालना तुरंत लागू नहीं किया जाएगा।

### 2.7) विकल्प {#tunnel.alternatives}

#### 2.7.1) checksum block का उपयोग न करें {#tunnel.nochecksum}

उपरोक्त प्रक्रिया का एक विकल्प यह है कि checksum block को पूरी तरह से हटा दिया जाए और verification hash को payload के plain hash से बदल दिया जाए। इससे tunnel gateway पर प्रसंस्करण सरल हो जाएगा और प्रत्येक hop पर 144 bytes की bandwidth की बचत होगी। दूसरी ओर, tunnel के भीतर के आक्रमणकारी message के आकार को आसानी से ऐसे size में समायोजित कर सकते हैं जो बाहरी साजिशी observers और बाद के tunnel participants द्वारा आसानी से traceable हो। भ्रष्टाचार के कारण message को आगे भेजने के लिए आवश्यक पूरी bandwidth भी बर्बाद हो जाएगी। Per-hop validation के बिना, अत्यधिक लंबे tunnels बनाकर या tunnel में loops बनाकर अतिरिक्त network resources की खपत करना भी संभव हो जाएगा।

#### 2.7.2) tunnel प्रसंस्करण को बीच में समायोजित करना {#tunnel.reroute}

जबकि सरल tunnel रूटिंग एल्गोरिदम अधिकांश मामलों के लिए पर्याप्त होना चाहिए, तीन विकल्प हैं जिनका अन्वेषण किया जा सकता है:

- tunnel के भीतर किसी भी arbitrary hop पर एक message को निर्दिष्ट समय अवधि या randomized period के लिए देरी करना। यह checksum block में hash को बदलकर प्राप्त किया जा सकता है, जैसे hash के पहले 8 bytes के साथ, उसके बाद कुछ delay instructions। वैकल्पिक रूप से, instructions participant को raw payload को वैसे ही interpret करने को कह सकते हैं, और या तो message को discard कर दें या इसे path के नीचे forward करना जारी रखें (जहाँ इसे endpoint द्वारा chaff message के रूप में interpret किया जाएगा)। इसके बाद के हिस्से में gateway को अपने encryption algorithm को adjust करने की आवश्यकता होगी ताकि एक अलग hop पर cleartext payload produce हो सके, लेकिन इसमें ज्यादा परेशानी नहीं होनी चाहिए।

- tunnel में भाग लेने वाले routers को संदेश को आगे भेजने से पहले उसे remix करने की अनुमति दें - इसे उस peer की अपनी outbound tunnels में से किसी एक के माध्यम से bounce करते हुए, अगले hop तक पहुंचाने के निर्देशों के साथ। इसका उपयोग या तो नियंत्रित तरीके से (ऊपर दी गई delays जैसे en-route निर्देशों के साथ) या संभावनाओं के आधार पर किया जा सकता है।

- tunnel creator के लिए कोड implement करें ताकि tunnel में किसी peer के "next hop" को redefine किया जा सके, जिससे आगे dynamic redirection की अनुमति मिले।

#### 2.7.3) द्विदिशीय tunnels का उपयोग करें {#tunnel.bidirectional}

inbound और outbound संचार के लिए दो अलग tunnel का उपयोग करने की वर्तमान रणनीति एकमात्र उपलब्ध तकनीक नहीं है, और इसके गुमनामी संबंधी प्रभाव हैं। सकारात्मक पक्ष पर, अलग tunnel का उपयोग करके यह tunnel में भागीदारों के विश्लेषण के लिए उजागर होने वाले ट्रैफिक डेटा को कम करता है - उदाहरण के लिए, वेब ब्राउज़र से outbound tunnel में peers केवल HTTP GET के ट्रैफिक को देखेंगे, जबकि inbound tunnel में peers tunnel के साथ पहुंचाए गए payload को देखेंगे। bidirectional tunnel के साथ, सभी भागीदारों के पास इस तथ्य तक पहुंच होगी कि जैसे 1KB एक दिशा में भेजा गया, फिर 100KB दूसरी दिशा में। नकारात्मक पक्ष पर, unidirectional tunnel का उपयोग करने का मतलब है कि peers के दो सेट हैं जिन्हें profile किया जाना चाहिए और जिनका हिसाब रखा जाना चाहिए, और predecessor attacks की बढ़ी हुई गति को संबोधित करने के लिए अतिरिक्त सावधानी बरतनी चाहिए। नीचे वर्णित tunnel pooling और building प्रक्रिया को predecessor attack की चिंताओं को कम करना चाहिए, हालांकि यदि वांछित हो, तो inbound और outbound दोनों tunnel को समान peers के साथ build करना बहुत कठिन नहीं होगा।

#### 2.7.4) छोटे blocksize का उपयोग करें {#tunnel.smallerhashes}

इस समय, AES का हमारा उपयोग हमारे ब्लॉक साइज़ को 16 बाइट्स तक सीमित करता है, जो बदले में checksum ब्लॉक कॉलम के लिए न्यूनतम साइज़ प्रदान करता है। यदि कोई अन्य एल्गोरिदम का उपयोग छोटे ब्लॉक साइज़ के साथ किया जाता, या अन्यथा hash के छोटे हिस्सों के साथ checksum ब्लॉक के सुरक्षित निर्माण की अनुमति दे सकता, तो इसे खोजना उपयुक्त हो सकता है। प्रत्येक hop पर अब उपयोग किए जाने वाले 16 बाइट्स पर्याप्त से अधिक होने चाहिए।

## 3) Tunnel निर्माण {#tunnel.building}

जब एक tunnel बनाते समय, creator को प्रत्येक hop को आवश्यक configuration डेटा के साथ एक अनुरोध भेजना होता है, फिर संभावित participant के जवाब का इंतजार करना पड़ता है जिसमें वे बताते हैं कि वे सहमत हैं या नहीं। ये tunnel request संदेश और उनके जवाब garlic wrapped होते हैं ताकि केवल वही router जो key जानता है उसे decrypt कर सके, और दोनों दिशाओं में लिया गया path भी tunnel routed होता है। tunnels बनाते समय तीन महत्वपूर्ण आयामों को ध्यान में रखना चाहिए: कौन से peers का उपयोग किया जाता है (और कहाँ), अनुरोध कैसे भेजे जाते हैं (और जवाब कैसे प्राप्त होते हैं), और उन्हें कैसे maintain किया जाता है।

### 3.1) Peer चयन {#tunnel.peerselection}

दो प्रकार की tunnels - inbound और outbound - के अतिरिक्त, विभिन्न tunnels के लिए उपयोग की जाने वाली peer selection की दो शैलियां हैं - exploratory और client। Exploratory tunnels का उपयोग network database रखरखाव और tunnel रखरखाव दोनों के लिए किया जाता है, जबकि client tunnels का उपयोग end to end client संदेशों के लिए किया जाता है।

#### 3.1.1) खोजी tunnel साथी चयन {#tunnel.selection.exploratory}

एक्सप्लोरेटरी tunnels नेटवर्क के एक सबसेट से साथियों (peers) के यादृच्छिक चयन से बनाए जाते हैं। विशिष्ट सबसेट स्थानीय router पर और उनकी tunnel routing आवश्यकताओं पर निर्भर करता है। सामान्यतः, एक्सप्लोरेटरी tunnels यादृच्छिक रूप से चयनित साथियों से बनाए जाते हैं जो peer की "विफल नहीं लेकिन सक्रिय" प्रोफ़ाइल श्रेणी में हैं। केवल tunnel routing के अलावा tunnels का द्वितीयक उद्देश्य कम उपयोग वाले उच्च क्षमता वाले साथियों को खोजना है ताकि उन्हें client tunnels में उपयोग के लिए बढ़ावा दिया जा सके।

#### 3.1.2) क्लाइंट tunnel पीयर चयन {#tunnel.selection.client}

Client tunnel अधिक कड़े आवश्यकताओं के साथ बनाए जाते हैं - local router अपनी "fast and high capacity" प्रोफाइल श्रेणी से peers का चयन करेगा ताकि प्रदर्शन और विश्वसनीयता client application की आवश्यकताओं को पूरा कर सके। हालांकि, उस बुनियादी चयन के अलावा कई महत्वपूर्ण विवरण हैं जिनका पालन किया जाना चाहिए, जो client की गुमनामी की आवश्यकताओं पर निर्भर करता है।

कुछ clients के लिए जो adversaries द्वारा predecessor attack किए जाने की चिंता करते हैं, tunnel selection peers को एक strict order में रख सकता है - यदि A, B, और C एक tunnel में हैं, तो A के बाद hop हमेशा B होगा, और B के बाद hop हमेशा C होगा। एक कम strict ordering भी संभव है, जो यह सुनिश्चित करती है कि जबकि A के बाद hop B हो सकता है, B कभी भी A से पहले नहीं हो सकता। अन्य configuration options में केवल inbound tunnel gateways और outbound tunnel endpoints को fixed रखने या MTBF rate पर rotate करने की क्षमता शामिल है।

### 3.2) अनुरोध डिलिवरी {#tunnel.request}

जैसा कि ऊपर उल्लेख किया गया है, एक बार tunnel creator को पता चल जाता है कि tunnel में कौन से peers होने चाहिए और किस क्रम में, तो creator एक series of tunnel request messages बनाता है, जिसमें से प्रत्येक में उस peer के लिए आवश्यक जानकारी होती है। उदाहरण के लिए, participating tunnels को 4 byte tunnel ID दिया जाएगा जिस पर उन्हें messages प्राप्त करने हैं, 4 byte tunnel ID जिस पर उन्हें messages भेजने हैं, next hop की identity का 32 byte hash, और tunnel से एक layer को हटाने के लिए उपयोग की जाने वाली 32 byte layer key। निश्चित रूप से, outbound tunnel endpoints को कोई "next hop" या "next tunnel ID" जानकारी नहीं दी जाती है। हालांकि inbound tunnel gateways को 8 layer keys उस क्रम में दी जाती हैं जिसमें उन्हें encrypt किया जाना चाहिए (जैसा कि ऊपर वर्णित है)। replies की अनुमति देने के लिए, request में एक random session tag और एक random session key होती है जिससे peer अपने निर्णय को garlic encrypt कर सकता है, साथ ही वह tunnel भी होता है जिसपर उस garlic को भेजा जाना चाहिए। उपरोक्त जानकारी के अलावा, विभिन्न client specific options भी शामिल हो सकते हैं, जैसे कि tunnel पर कौन सी throttling लगानी है, कौन सी padding या batch strategies का उपयोग करना है, आदि।

सभी request messages बनाने के बाद, वे target router के लिए garlic wrapped होते हैं और एक exploratory tunnel के माध्यम से भेजे जाते हैं। प्राप्ति पर, वह peer निर्धारित करता है कि क्या वे भाग ले सकते हैं या लेंगे, एक reply message बनाते हैं और दी गई जानकारी के साथ response को garlic wrapping और tunnel routing दोनों करते हैं। tunnel creator पर reply प्राप्त होने पर, tunnel को उस hop पर valid माना जाता है (यदि स्वीकार किया गया हो)। एक बार सभी peers द्वारा स्वीकार किए जाने पर, tunnel active हो जाता है।

### 3.3) पूलिंग {#tunnel.pooling}

कुशल संचालन की अनुमति देने के लिए, router tunnel pools की एक श्रृंखला बनाए रखता है, जिसमें प्रत्येक अपनी कॉन्फ़िगरेशन के साथ एक विशिष्ट उद्देश्य के लिए उपयोग किए जाने वाले tunnels के समूह का प्रबंधन करता है। जब उस उद्देश्य के लिए tunnel की आवश्यकता होती है, तो router उपयुक्त pool में से यादृच्छिक रूप से एक का चयन करता है। कुल मिलाकर, दो exploratory tunnel pools हैं - एक inbound और एक outbound - प्रत्येक router के exploration defaults का उपयोग करते हैं। इसके अतिरिक्त, प्रत्येक local destination के लिए pools की एक जोड़ी है - एक inbound और एक outbound tunnel। ये pools उस कॉन्फ़िगरेशन का उपयोग करते हैं जो local destination द्वारा router से कनेक्ट होने पर निर्दिष्ट की गई थी, या यदि निर्दिष्ट नहीं है तो router के defaults का उपयोग करते हैं।

प्रत्येक pool के configuration में कुछ मुख्य सेटिंग्स होती हैं, जो परिभाषित करती हैं कि कितने tunnel को सक्रिय रखना है, विफलता के मामले में कितने backup tunnel बनाए रखने हैं, tunnel का परीक्षण कितनी बार करना है, tunnel कितने लंबे होने चाहिए, क्या उन लंबाइयों को randomized करना चाहिए, replacement tunnel कितनी बार बनाए जाने चाहिए, साथ ही व्यक्तिगत tunnel को configure करते समय अनुमतित अन्य सभी सेटिंग्स।

### 3.4) विकल्प {#tunnel.building.alternatives}

#### 3.4.1) टेलिस्कोपिक निर्माण {#tunnel.building.telescoping}

एक सवाल जो exploratory tunnels के उपयोग के संबंध में उत्पन्न हो सकता है tunnel creation messages भेजने और प्राप्त करने के लिए यह है कि यह predecessor attacks के लिए tunnel की संवेदनशीलता को कैसे प्रभावित करता है। जबकि उन tunnels के endpoints और gateways network में यादृच्छिक रूप से वितरित होंगे (शायद उस सेट में tunnel creator भी शामिल हो), एक अन्य विकल्प tunnel pathways का उपयोग करना है request और response को पास करने के लिए, जैसा कि [TOR](https://www.torproject.org/) में किया जाता है। हालांकि, इससे tunnel creation के दौरान leaks हो सकते हैं, जिससे peers को पता चल सकता है कि tunnel में बाद में कितने hops हैं timing या packet count की निगरानी करके जब tunnel बनाया जा रहा हो। इस समस्या को कम करने के लिए तकनीकों का उपयोग किया जा सकता है, जैसे कि प्रत्येक hop को endpoints के रूप में उपयोग करना ([2.7.2](#tunnel.reroute) के अनुसार) random संख्या में messages के लिए अगले hop को build करना जारी रखने से पहले।

#### 3.4.2) प्रबंधन के लिए गैर-खोजी tunnel {#tunnel.building.nonexploratory}

tunnel निर्माण प्रक्रिया का दूसरा विकल्प यह है कि router को अतिरिक्त non-exploratory inbound और outbound pools का सेट दिया जाए, जिनका उपयोग tunnel request और response के लिए किया जाए। यह मानते हुए कि router का network का एक अच्छी तरह से एकीकृत दृश्य है, यह आवश्यक नहीं होना चाहिए, लेकिन यदि router किसी तरह से विभाजित था, तो tunnel प्रबंधन के लिए non-exploratory pools का उपयोग करने से इस बारे में जानकारी का रिसाव कम हो जाएगा कि router के partition में कौन से peers हैं।

## 4) Tunnel थ्रॉटलिंग {#tunnel.throttling}

भले ही I2P के भीतर के tunnel एक circuit switched network से मिलते-जुलते हैं, I2P के भीतर सब कुछ पूरी तरह से message based है - tunnel केवल संदेशों की डिलीवरी को व्यवस्थित करने में मदद करने के लिए accounting tricks हैं। संदेशों की विश्वसनीयता या क्रम के बारे में कोई अनुमान नहीं लगाया जाता है, और retransmissions को उच्च स्तरों पर छोड़ दिया जाता है (जैसे I2P की client layer streaming library)। यह I2P को packet switched और circuit switched networks दोनों के लिए उपलब्ध throttling तकनीकों का फायदा उठाने की अनुमति देता है। उदाहरण के लिए, प्रत्येक router इस बात का moving average रख सकता है कि हर tunnel कितना डेटा उपयोग कर रहा है, इसे उन सभी averages के साथ जोड़ सकता है जो अन्य tunnels द्वारा उपयोग किए जा रहे हैं जिसमें router भाग ले रहा है, और अपनी क्षमता और उपयोग के आधार पर अतिरिक्त tunnel participation requests को स्वीकार या अस्वीकार कर सकता है। दूसरी ओर, प्रत्येक router उन संदेशों को छोड़ सकता है जो इसकी क्षमता से अधिक हैं, सामान्य इंटरनेट पर उपयोग किए जाने वाले अनुसंधान का फायदा उठाते हुए।

## 5) मिक्सिंग/बैचिंग {#tunnel.mixing}

Gateway और प्रत्येक hop पर messages को delay करने, reorder करने, reroute करने, या padding के लिए कौन सी रणनीतियों का उपयोग किया जाना चाहिए? यह कितनी हद तक स्वचालित रूप से किया जाना चाहिए, कितना प्रति tunnel या प्रति hop setting के रूप में configure किया जाना चाहिए, और tunnel के creator (और बदले में, user) को इस operation को कैसे नियंत्रित करना चाहिए? यह सब अज्ञात छोड़ा गया है, भविष्य की release के लिए इस पर काम किया जाना है।
