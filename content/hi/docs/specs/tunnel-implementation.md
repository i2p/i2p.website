---
title: "Tunnel कार्यान्वयन"
description: "I2P tunnel संचालन, निर्माण, और संदेश प्रसंस्करण का विनिर्देश"
slug: "tunnel-implementation"
aliases:
  - "/hi/docs/specs/implementation"
  - "/hi/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

यह पृष्ठ वर्तमान tunnel कार्यान्वयन का दस्तावेजीकरण करता है।

## Tunnel अवलोकन {#tunnel.overview}

I2P के भीतर, संदेश peers की एक virtual tunnel के माध्यम से एक दिशा में पारित किए जाते हैं, संदेश को अगले hop तक पहुंचाने के लिए जो भी साधन उपलब्ध हैं उनका उपयोग करते हुए। संदेश tunnel के *gateway* पर आते हैं, bundled up और/या fragmented होकर निश्चित आकार के tunnel messages में बदल जाते हैं, और tunnel में अगले hop को forward कर दिए जाते हैं, जो संदेश को process और verify करता है और इसे अगले hop को भेजता है, और इसी तरह यह तब तक चलता है जब तक यह tunnel endpoint तक नहीं पहुंच जाता। वह *endpoint* gateway द्वारा bundled up किए गए संदेशों को लेता है और निर्देश के अनुसार उन्हें forward करता है - या तो किसी अन्य router को, किसी अन्य router पर किसी अन्य tunnel को, या locally।

सभी tunnel समान रूप से काम करते हैं, लेकिन इन्हें दो अलग समूहों में बांटा जा सकता है - inbound tunnels और outbound tunnels। Inbound tunnels में एक अविश्वसनीय gateway होता है जो संदेशों को tunnel creator की ओर भेजता है, जो tunnel endpoint का काम करता है। Outbound tunnels के लिए, tunnel creator gateway का काम करता है और संदेशों को remote endpoint तक भेजता है।

tunnel का निर्माता यह तय करता है कि कौन से peers tunnel में भाग लेंगे, और प्रत्येक को आवश्यक configuration data प्रदान करता है। इनमें कोई भी संख्या में hops हो सकते हैं। इसका उद्देश्य यह है कि प्रतिभागियों या तीसरे पक्ष के लिए tunnel की लंबाई निर्धारित करना कठिन हो, या यहां तक कि मिलीभगत करने वाले प्रतिभागियों के लिए भी यह जानना कठिन हो कि वे बिल्कुल एक ही tunnel का हिस्सा हैं या नहीं (उस स्थिति को छोड़कर जहां मिलीभगत करने वाले peers tunnel में एक-दूसरे के बगल में हैं)।

व्यावहारिक रूप में, विभिन्न उद्देश्यों के लिए tunnel pools की एक श्रृंखला का उपयोग किया जाता है - प्रत्येक स्थानीय client destination के पास अपने inbound tunnels और outbound tunnels का अपना सेट होता है, जो इसकी गुमनामी और प्रदर्शन आवश्यकताओं को पूरा करने के लिए कॉन्फ़िगर किया गया होता है। इसके अतिरिक्त, router स्वयं network database में भाग लेने और tunnels को प्रबंधित करने के लिए pools की एक श्रृंखला बनाए रखता है।

I2P एक स्वाभाविक रूप से पैकेट स्विच्ड नेटवर्क है, इन tunnels के साथ भी, जो इसे समानांतर में चलने वाली कई tunnels का फायदा उठाने की अनुमति देता है, लचीलापन बढ़ाता है और लोड को संतुलित करता है। मुख्य I2P layer के बाहर, client applications के लिए एक वैकल्पिक end to end streaming library उपलब्ध है, जो TCP-esque ऑपरेशन को expose करती है, जिसमें message reordering, retransmission, congestion control आदि शामिल है।

I2P tunnel शब्दावली का अवलोकन [tunnel overview page](/docs/overview/tunnel-routing) पर है।

## Tunnel संचालन (संदेश प्रसंस्करण) {#tunnel.operation}

### अवलोकन

tunnel बनने के बाद, [I2NP messages](/docs/specs/i2np) को प्रोसेस किया जाता है और इसके माध्यम से पास किया जाता है। tunnel संचालन में चार अलग-अलग प्रक्रियाएं होती हैं, जिन्हें tunnel के विभिन्न peers द्वारा संभाला जाता है।

1. सबसे पहले, tunnel gateway कई I2NP messages एकत्रित करता है और उन्हें delivery के लिए tunnel messages में preprocess करता है।
2. इसके बाद, वह gateway उस preprocessed data को encrypt करता है, फिर इसे पहले hop पर forward करता है।
3. वह peer, और बाद के tunnel participants, encryption की एक layer को unwrap करते हैं, यह verify करते हुए कि यह duplicate नहीं है, फिर इसे अगले peer पर forward करते हैं।
4. अंततः, tunnel messages endpoint पर पहुंच जाते हैं जहाँ gateway द्वारा originally bundle किए गए I2NP messages को reassemble किया जाता है और अनुरोध के अनुसार forward कर दिया जाता है।

मध्यवर्ती tunnel प्रतिभागियों को नहीं पता होता कि वे inbound या outbound tunnel में हैं; वे हमेशा अगले hop के लिए "encrypt" करते हैं। इसलिए, हम outbound tunnel gateway पर "decrypt" करने के लिए symmetric AES encryption का फायदा उठाते हैं, ताकि plaintext outbound endpoint पर प्रकट हो जाए।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Gateway Processing {#tunnel.gateway}

#### संदेश पूर्व-प्रसंस्करण {#tunnel.preprocessing}

एक tunnel gateway का कार्य [I2NP messages](/docs/specs/i2np) को खंडित करना और उन्हें निश्चित आकार के [tunnel messages](/docs/specs/tunnel-message) में पैक करना और tunnel messages को एन्क्रिप्ट करना है। Tunnel messages में निम्नलिखित होते हैं:

- एक 4 byte Tunnel ID
- एक 16 byte IV (initialization vector)
- एक checksum
- Padding, यदि आवश्यक हो
- एक या अधिक { delivery instruction, I2NP message fragment } जोड़े

Tunnel ID 4 बाइट संख्याएं हैं जो प्रत्येक hop पर उपयोग की जाती हैं - participants जानते हैं कि किस tunnel ID के साथ संदेशों को सुनना है और अगले hop के लिए किस tunnel ID पर उन्हें आगे भेजा जाना चाहिए, और प्रत्येक hop उस tunnel ID को चुनता है जिस पर वे संदेश प्राप्त करते हैं। Tunnel खुद अल्पकालिक होते हैं (10 मिनट)। भले ही बाद के tunnel समान peers के अनुक्रम का उपयोग करके बनाए जाएं, प्रत्येक hop का tunnel ID बदल जाएगा।

पथ के साथ संदेश के आकार को समायोजित करके विरोधियों को संदेशों को टैग करने से रोकने के लिए, सभी tunnel संदेश 1024 बाइट्स के निश्चित आकार में होते हैं। बड़े I2NP संदेशों को समायोजित करने के साथ-साथ छोटे संदेशों को अधिक कुशलता से समर्थित करने के लिए, gateway बड़े I2NP संदेशों को टुकड़ों में विभाजित करता है जो प्रत्येक tunnel संदेश के भीतर समाहित होते हैं। endpoint कम समय के लिए टुकड़ों से I2NP संदेश को फिर से बनाने का प्रयास करेगा, लेकिन आवश्यकता के अनुसार उन्हें छोड़ देगा।

विवरण [tunnel message specification](/docs/specs/tunnel-message) में हैं।

### गेटवे एन्क्रिप्शन

संदेशों को padded payload में preprocessing के बाद, gateway एक यादृच्छिक 16 byte IV value बनाता है, आवश्यकता के अनुसार इसे और tunnel संदेश को iteratively encrypt करता है, और tuple {tunnelID, IV, encrypted tunnel message} को अगले hop पर भेजता है।

gateway पर encryption कैसे की जाती है, यह इस बात पर निर्भर करता है कि tunnel inbound है या outbound। Inbound tunnels के लिए, वे केवल एक random IV चुनते हैं, इसे postprocess और update करके gateway के लिए IV generate करते हैं और उस IV को अपनी layer key के साथ मिलाकर preprocessed data को encrypt करते हैं। Outbound tunnels के लिए उन्हें tunnel के सभी hops के लिए IV और layer keys के साथ (unencrypted) IV और preprocessed data को iteratively decrypt करना होता है। Outbound tunnel encryption का परिणाम यह होता है कि जब हर peer इसे encrypt करता है, तो endpoint initial preprocessed data को recover कर लेता है।

### प्रतिभागी प्रसंस्करण {#tunnel.participant}

जब कोई peer एक tunnel संदेश प्राप्त करता है, तो यह जांचता है कि संदेश पहले जैसे ही पिछले hop से आया है (जो पहले संदेश के tunnel से गुजरने पर प्रारंभिक किया जाता है)। यदि पिछला peer एक अलग router है, या यदि संदेश पहले से देखा जा चुका है, तो संदेश को छोड़ दिया जाता है। फिर participant प्राप्त IV को अपनी IV key का उपयोग करके AES256/ECB से encrypt करता है ताकि वर्तमान IV निर्धारित कर सके, उस IV का उपयोग participant की layer key के साथ data को encrypt करने के लिए करता है, वर्तमान IV को फिर से अपनी IV key का उपयोग करके AES256/ECB से encrypt करता है, फिर tuple {nextTunnelId, nextIV, encryptedData} को अगले hop को forward करता है। IV की यह दोहरी encryption (उपयोग से पहले और बाद दोनों में) एक निश्चित प्रकार के confirmation attacks से निपटने में मदद करती है।

डुप्लिकेट संदेश की पहचान message IVs पर एक decaying Bloom filter द्वारा की जाती है। प्रत्येक router एक single Bloom filter बनाए रखता है जिसमें IV और उन सभी tunnels के लिए प्राप्त संदेश के पहले block का XOR होता है जिनमें वह भाग ले रहा है, जो 10-20 मिनट बाद (जब tunnels समाप्त हो जाएंगे) देखे गए entries को हटाने के लिए संशोधित होता है। bloom filter का आकार और उपयोग किए गए parameters router के network connection को संतृप्त करने के लिए पर्याप्त हैं और false positive की संभावना नगण्य है। Bloom filter में डाला गया unique value IV और पहले block का XOR है ताकि tunnel में nonsequential colluding peers संदेश को IV और पहले block को बदलकर दोबारा भेजने से tag न कर सकें।

### Endpoint Processing {#tunnel.endpoint}

tunnel के अंतिम hop पर tunnel message प्राप्त करने और validate करने के बाद, endpoint यह कैसे recover करता है कि gateway द्वारा encode किया गया data इस पर निर्भर करता है कि tunnel एक inbound है या outbound tunnel। outbound tunnels के लिए, endpoint अपनी layer key के साथ message को encrypt करता है बिल्कुल किसी अन्य participant की तरह, जिससे preprocessed data expose हो जाता है। inbound tunnels के लिए, endpoint भी tunnel creator होता है इसलिए वे केवल iteratively IV और message को decrypt कर सकते हैं, प्रत्येक step की layer और IV keys का उपयोग reverse order में करके।

इस बिंदु पर, tunnel endpoint के पास gateway द्वारा भेजा गया पूर्व-संसाधित डेटा होता है, जिसे वह फिर शामिल I2NP संदेशों में पार्स कर सकता है और उन्हें उनके डिलीवरी निर्देशों के अनुसार आगे भेज सकता है।

## Tunnel निर्माण {#tunnel.building}

tunnel बनाते समय, निर्माता को प्रत्येक hop को आवश्यक कॉन्फ़िगरेशन डेटा के साथ एक अनुरोध भेजना होगा और tunnel को सक्षम करने से पहले सभी के सहमत होने का इंतज़ार करना होगा। अनुरोध एन्क्रिप्ट किए जाते हैं ताकि केवल वे peers जिन्हें जानकारी के एक हिस्से (जैसे tunnel layer या IV key) की आवश्यकता है, उनके पास ही वह डेटा हो। इसके अलावा, केवल tunnel निर्माता के पास peer के उत्तर तक पहुंच होगी। tunnels का उत्पादन करते समय तीन महत्वपूर्ण आयाम ध्यान में रखने चाहिए: कौन से peers का उपयोग किया जाता है (और कहाँ), अनुरोध कैसे भेजे जाते हैं (और उत्तर कैसे प्राप्त होते हैं), और उन्हें कैसे बनाए रखा जाता है।

### पीयर चयन {#tunnel.peerselection}

दो प्रकार की tunnels - inbound और outbound - के अलावा, विभिन्न tunnels के लिए उपयोग किए जाने वाले peer selection की दो शैलियां हैं - exploratory और client। Exploratory tunnels का उपयोग network database रखरखाव और tunnel रखरखाव दोनों के लिए किया जाता है, जबकि client tunnels का उपयोग end to end client संदेशों के लिए किया जाता है।

#### खोजी Tunnel Peer चयन {#tunnel.selection.exploratory}

Exploratory tunnel नेटवर्क के एक उपसमूह से peers के यादृच्छिक चयन से बनाए जाते हैं। विशेष उपसमूह स्थानीय router पर और उनकी tunnel routing आवश्यकताओं पर निर्भर करता है। सामान्यतः, exploratory tunnel उन यादृच्छिक रूप से चुने गए peers से बनाए जाते हैं जो peer की "न तो असफल लेकिन सक्रिय" प्रोफाइल श्रेणी में होते हैं। केवल tunnel routing के अतिरिक्त tunnel का द्वितीयक उद्देश्य कम उपयोग वाले उच्च क्षमता के peers को खोजना है ताकि उन्हें client tunnel में उपयोग के लिए प्रोत्साहित किया जा सके।

खोजपरक peer selection के बारे में [Peer Profiling and Selection page](/docs/overview/peer-selection) पर विस्तार से चर्चा की गई है।

#### Client Tunnel Peer Selection {#tunnel.selection.client}

Client tunnels अधिक कड़े आवश्यकताओं के साथ बनाए जाते हैं - स्थानीय router अपनी "तेज़ और उच्च क्षमता" प्रोफ़ाइल श्रेणी से peers का चयन करेगा ताकि प्रदर्शन और विश्वसनीयता client एप्लिकेशन की आवश्यकताओं को पूरा कर सके। हालांकि, उस बुनियादी चयन के अलावा कई महत्वपूर्ण विवरण हैं जिनका पालन किया जाना चाहिए, यह client की गुमनामी आवश्यकताओं पर निर्भर करता है।

Client peer selection के बारे में [Peer Profiling and Selection page](/docs/overview/peer-selection) पर विस्तार से चर्चा की गई है।

#### Tunnels के भीतर Peer Ordering {#ordering}

Peers को tunnels के भीतर [predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 update](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)) से निपटने के लिए क्रमबद्ध किया जाता है।

predecessor attack को विफल करने के लिए, tunnel selection peers को एक कड़े क्रम में रखता है - यदि A, B, और C किसी विशेष tunnel pool के लिए एक tunnel में हैं, तो A के बाद का hop हमेशा B होता है, और B के बाद का hop हमेशा C होता है।

ऑर्डरिंग को startup पर प्रत्येक tunnel pool के लिए एक random 32-byte key generate करके लागू किया जाता है। Peers को ordering का अनुमान नहीं लगाना चाहिए, या एक attacker दो router hashes को काफी दूरी पर craft कर सकता है ताकि tunnel के दोनों छोरों पर होने की संभावना को अधिकतम कर सके। Peers को random key से (peer के hash को random key के साथ concatenated) के SHA256 Hash के XOR distance के अनुसार sort किया जाता है:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
क्योंकि प्रत्येक tunnel pool एक अलग random key का उपयोग करता है, ordering एक single pool के भीतर consistent है लेकिन अलग-अलग pools के बीच नहीं। प्रत्येक router restart पर नई keys generate की जाती हैं।

### अनुरोध डिलीवरी {#tunnel.request}

एक multi-hop tunnel का निर्माण एक single build message का उपयोग करके किया जाता है जो बार-बार decrypt और forward किया जाता है। [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) की शब्दावली में, यह "non-interactive" telescopic tunnel building है।

यह tunnel request तैयारी, वितरण, और प्रतिक्रिया विधि [डिज़ाइन की गई है](/docs/specs/tunnel-creation) ताकि exposed predecessors की संख्या कम हो सके, प्रेषित संदेशों की संख्या कम हो, उचित connectivity की जांच हो सके, और पारंपरिक telescopic tunnel निर्माण के message counting हमले से बचा जा सके। (यह विधि, जो पहले से स्थापित tunnel के हिस्से के माध्यम से tunnel को विस्तारित करने के लिए संदेश भेजती है, "Hashing it out" पेपर में "interactive" telescopic tunnel building कहलाती है।)

Tunnel अनुरोध और प्रतिक्रिया संदेशों का विवरण, और उनकी एन्क्रिप्शन, [यहां निर्दिष्ट है](/docs/specs/tunnel-creation)।

Peers विभिन्न कारणों से tunnel निर्माण अनुरोधों को अस्वीकार कर सकते हैं, हालांकि चार बढ़ती गंभीरता वाली अस्वीकृतियों की एक श्रृंखला ज्ञात है: संभाव्य अस्वीकृति (router की क्षमता के नजदीक पहुंचने के कारण, या अनुरोधों की बाढ़ के जवाब में), क्षणिक अधिभार, bandwidth अधिभार, और गंभीर विफलता। जब प्राप्त होती है, तो उन चारों को tunnel निर्माता द्वारा संबंधित router के अपने profile को समायोजित करने में मदद के लिए व्याख्यायित किया जाता है।

peer profiling पर अधिक जानकारी के लिए, [Peer Profiling and Selection page](/docs/overview/peer-selection) देखें।

### Tunnel Pools {#tunnel.pooling}

कुशल संचालन की अनुमति देने के लिए, router एक श्रृंखला के tunnel pools को बनाए रखता है, जिसमें प्रत्येक अपने कॉन्फ़िगरेशन के साथ एक विशिष्ट उद्देश्य के लिए उपयोग किए जाने वाले tunnels के समूह का प्रबंधन करता है। जब उस उद्देश्य के लिए एक tunnel की आवश्यकता होती है, तो router यादृच्छिक रूप से उपयुक्त pool में से एक का चयन करता है। कुल मिलाकर, दो exploratory tunnel pools हैं - एक inbound और एक outbound - प्रत्येक router के default configuration का उपयोग करते हैं। इसके अतिरिक्त, प्रत्येक local destination के लिए pools की एक जोड़ी है - एक inbound और एक outbound tunnel pool। ये pools उस configuration का उपयोग करते हैं जो local destination द्वारा [I2CP](/docs/specs/i2cp) के माध्यम से router से कनेक्ट करते समय निर्दिष्ट की जाती है, या यदि निर्दिष्ट नहीं है तो router के defaults का उपयोग करते हैं।

प्रत्येक पूल के कॉन्फ़िगरेशन में कुछ मुख्य सेटिंग्स होती हैं, जो परिभाषित करती हैं कि कितनी tunnel सक्रिय रखनी हैं, असफलता की स्थिति में कितनी बैकअप tunnel बनाए रखनी हैं, tunnel कितनी लंबी होनी चाहिए, क्या उन लंबाइयों को यादृच्छिक बनाना चाहिए, साथ ही व्यक्तिगत tunnel को कॉन्फ़िगर करते समय अनुमतित अन्य कोई भी सेटिंग्स। कॉन्फ़िगरेशन विकल्प [I2CP page](/docs/specs/i2cp) पर निर्दिष्ट हैं।

### Tunnel की लंबाई और डिफ़ॉल्ट {#length}

[टनल ओवरव्यू पेज पर](/docs/overview/tunnel-routing#length)।

### पूर्वानुमानित निर्माण रणनीति और प्राथमिकता {#strategy}

Tunnel निर्माण महंगा है, और tunnel बनने के बाद एक निश्चित समय में समाप्त हो जाते हैं। हालांकि, जब कोई pool में tunnel समाप्त हो जाते हैं, तो Destination अनिवार्य रूप से मृत हो जाता है। इसके अलावा, tunnel निर्माण की सफलता दर स्थानीय और वैश्विक नेटवर्क स्थितियों दोनों के साथ बहुत भिन्न हो सकती है। इसलिए, यह सुनिश्चित करने के लिए एक पूर्वानुमान लगाने वाली, अनुकूलनीय निर्माण रणनीति बनाए रखना महत्वपूर्ण है कि नए tunnel की आवश्यकता से पहले सफलतापूर्वक बनाए जाएं, बिना अतिरिक्त tunnel बनाए, उन्हें बहुत जल्दी बनाए, या एन्क्रिप्टेड build संदेश बनाने और भेजने में बहुत अधिक CPU या bandwidth की खपत किए।

प्रत्येक tuple {exploratory/client, in/out, length, length variance} के लिए router एक सफल tunnel build के लिए आवश्यक समय पर statistics बनाए रखता है। इन statistics का उपयोग करके, यह गणना करता है कि tunnel की समाप्ति से कितनी देर पहले उसे replacement बनाने का प्रयास शुरू करना चाहिए। जैसे-जैसे समाप्ति का समय बिना सफल replacement के नजदीक आता है, यह समानांतर में कई build attempts शुरू करता है, और फिर आवश्यकता होने पर समानांतर attempts की संख्या बढ़ा देगा।

बैंडविड्थ और CPU उपयोग को सीमित करने के लिए, router सभी pools में outstanding build attempts की अधिकतम संख्या को भी सीमित करता है। Critical builds (जो exploratory tunnels के लिए हैं, और उन pools के लिए जिनके tunnels समाप्त हो गए हैं) को प्राथमिकता दी जाती है।

## Tunnel Message Throttling {#tunnel.throttling}

यद्यपि I2P के भीतर के tunnel एक circuit switched network से समानता रखते हैं, I2P के भीतर सब कुछ सख्ती से message आधारित है - tunnel केवल accounting tricks हैं जो messages की delivery को व्यवस्थित करने में मदद करती हैं। Messages की विश्वसनीयता या क्रम के बारे में कोई मान्यता नहीं बनाई जाती है, और retransmissions को उच्चतर स्तरों पर छोड़ दिया जाता है (जैसे I2P की client layer streaming library)। यह I2P को packet switched और circuit switched दोनों networks के लिए उपलब्ध throttling techniques का लाभ उठाने की अनुमति देता है। उदाहरण के लिए, प्रत्येक router यह ट्रैक कर सकता है कि प्रत्येक tunnel कितना data उपयोग कर रहा है का moving average, इसे उन सभी averages के साथ मिला सकता है जो अन्य tunnels द्वारा उपयोग किए जा रहे हैं जिनमें router भाग ले रहा है, और अपनी क्षमता और उपयोग के आधार पर अतिरिक्त tunnel participation requests को स्वीकार या अस्वीकार करने में सक्षम हो सकता है। दूसरी ओर, प्रत्येक router उन messages को बस drop कर सकता है जो इसकी क्षमता से अधिक हैं, सामान्य Internet पर उपयोग की जाने वाली research का फायदा उठाते हुए।

वर्तमान कार्यान्वयन में, router एक भारित यादृच्छिक प्रारंभिक त्याग (WRED) रणनीति को लागू करते हैं। सभी भाग लेने वाले router (आंतरिक प्रतिभागी, इनबाउंड गेटवे, और आउटबाउंड endpoint) के लिए, router बैंडविड्थ सीमा के पास आने पर संदेशों के एक हिस्से को यादृच्छिक रूप से गिराना शुरू कर देगा। जैसे-जैसे ट्रैफिक सीमा के करीब आता है, या उससे अधिक हो जाता है, अधिक संदेश गिराए जाते हैं। आंतरिक प्रतिभागी के लिए, सभी संदेश खंडित और पैड किए जाते हैं और इसलिए समान आकार के होते हैं। हालांकि, इनबाउंड गेटवे और आउटबाउंड endpoint पर, गिराने का निर्णय पूरे (संयुक्त) संदेश पर किया जाता है, और संदेश का आकार ध्यान में रखा जाता है। बड़े संदेशों के गिराए जाने की संभावना अधिक होती है। इसके अलावा, इनबाउंड गेटवे की तुलना में आउटबाउंड endpoint पर संदेशों के गिराए जाने की संभावना अधिक होती है, क्योंकि वे संदेश अपनी यात्रा में उतने "आगे" नहीं होते हैं और इस प्रकार उन संदेशों को गिराने की नेटवर्क लागत कम होती है।

## भविष्य का कार्य {#future}

### मिक्सिंग/बैचिंग {#tunnel.mixing}

gateway और प्रत्येक hop पर messages को delay करने, reorder करने, reroute करने, या padding के लिए कौन सी रणनीतियों का उपयोग किया जा सकता है? यह कितनी हद तक automatically होना चाहिए, कितना per tunnel या per hop setting के रूप में configure किया जाना चाहिए, और tunnel के creator (और बदले में, user) को इस operation को कैसे control करना चाहिए? यह सब अज्ञात है, जिसे भविष्य की किसी दूर की release के लिए काम किया जाना है।

### पैडिंग

पैडिंग रणनीतियों का उपयोग विभिन्न स्तरों पर किया जा सकता है, जो अलग-अलग विरोधियों के लिए संदेश आकार की जानकारी के एक्सपोज़र को संबोधित करती हैं। वर्तमान निश्चित tunnel संदेश आकार 1024 बाइट्स है। हालांकि इसके भीतर, खंडित संदेशों को tunnel द्वारा बिल्कुल भी पैड नहीं किया जाता है, लेकिन एंड टू एंड संदेशों के लिए, वे garlic wrapping के हिस्से के रूप में पैड हो सकते हैं।

### WRED

WRED रणनीतियों का end-to-end प्रदर्शन और नेटवर्क congestion के पतन की रोकथाम पर महत्वपूर्ण प्रभाव होता है। वर्तमान WRED रणनीति का सावधानीपूर्वक मूल्यांकन और सुधार किया जाना चाहिए।
