---
title: "SAM V3"
description: "गैर-जावा I2P अनुप्रयोगों के लिए सरल गुमनाम संदेश प्रोटोकॉल"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM I2P के साथ बातचीत करने के लिए एक सरल क्लाइंट प्रोटोकॉल है। गैर-जावा एप्लिकेशन के लिए I2P नेटवर्क से जुड़ने हेतु SAM को अनुशंसित प्रोटोकॉल माना जाता है, और यह कई राउटर लागू करणों द्वारा समर्थित है। जावा एप्लिकेशन को सीधे स्ट्रीमिंग या I2CP एपीआई का उपयोग करना चाहिए।

SAM संस्करण 3 को I2P रिलीज़ 0.7.3 (मई 2009) में जारी किया गया था और यह एक स्थिर व समर्थित इंटरफ़ेस है। 3.1 भी स्थिर है तथा हस्ताक्षर प्रकार विकल्प का समर्थन करता है, जिसकी बहुत अधिक सिफारिश की जाती है। अधिक हाल के 3.x संस्करण उन्नत सुविधाओं का समर्थन करते हैं। ध्यान दें कि वर्तमान में i2pd अधिकांश 3.2 और 3.3 सुविधाओं का समर्थन नहीं करता है।

विकल्प: [SOCKS](/docs/api/socks), [स्ट्रीमिंग](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (अप्रचलित)](/docs/api/bob)। अप्रचलित संस्करण: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2)।

## ज्ञात SAM लाइब्रेरी

चेतावनी: इनमें से कुछ बहुत पुराने या समर्थित नहीं हो सकते हैं। नीचे उल्लेखित के अलावा कोई भी I2P परियोजना द्वारा परीक्षण, समीक्षा या रखरखाव नहीं किया जाता है। अपना स्वयं का शोध करें।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## त्वरित शुरुआत

एक बेसिक टीसीपी-केवल, पीयर-टू-पीयर एप्लिकेशन लागू करने के लिए, क्लाइंट निम्नलिखित कमांड्स का समर्थन करना चाहिए:

- `HELLO VERSION MIN=3.1 MAX=3.1` - शेष सभी के लिए आवश्यक
- `DEST GENERATE SIGNATURE_TYPE=7` - हमारी निजी कुंजी और गंतव्य उत्पन्न करने के लिए
- `NAMING LOOKUP NAME=...` - .i2p पतों को गंतव्य में परिवर्तित करने के लिए
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - STREAM CONNECT और STREAM ACCEPT के लिए आवश्यक
- `STREAM CONNECT ID=... DESTINATION=...` - बाहर जाने वाले कनेक्शन बनाने के लिए
- `STREAM ACCEPT ID=...` - आने वाले कनेक्शन स्वीकार करने के लिए

## डेवलपर्स के लिए सामान्य मार्गदर्शन

### एप्लिकेशन डिज़ाइन

SAM सत्र (या I2P के अंदर, टनल पूल या टनल के समुच्चय) लंबे समय तक चलने के लिए डिज़ाइन किए गए हैं। अधिकांश अनुप्रयोगों को केवल एक सत्र की आवश्यकता होगी, जिसे प्रारंभ होने पर बनाया जाएगा और बंद करते समय बंद कर दिया जाएगा। I2P Tor से अलग है, जहाँ परिपथ तेजी से बनाए जा सकते हैं और फेंके जा सकते हैं। अपने अनुप्रयोग को एक या दो से अधिक एक साथ चल रहे सत्रों का उपयोग करने के लिए डिज़ाइन करने से पहले या उन्हें तेजी से बनाने और छोड़ने के लिए, सावधानीपूर्वक सोचें और I2P डेवलपर्स से परामर्श करें। अधिकांश खतरे के मॉडल को प्रत्येक कनेक्शन के लिए एक अद्वितीय सत्र की आवश्यकता नहीं होगी।

साथ ही, कृपया सुनिश्चित करें कि आपके अनुप्रयोग की सेटिंग्स (और उपयोगकर्ताओं को राउटर सेटिंग्स के बारे में दी गई जानकारी, या यदि आप एक राउटर को पैकेज कर रहे हैं तो राउटर की डिफ़ॉल्ट सेटिंग्स) इस तरह की हों कि आपके उपयोगकर्ता नेटवर्क में उपभोग की तुलना में अधिक संसाधन योगदान करें। I2P एक पीयर-टू-पीयर नेटवर्क है, और यह नेटवर्क तब तक नहीं टिक सकता यदि कोई लोकप्रिय अनुप्रयोग नेटवर्क को स्थायी रूप से अतिभारित कर दे।

### अनुकूलता और परीक्षण

जावा I2P और i2pd राउटर लागूकरण स्वतंत्र होते हैं और व्यवहार, सुविधा समर्थन और डिफ़ॉल्ट में मामूली अंतर होते हैं। कृपया अपने अनुप्रयोग को दोनों राउटर्स के नवीनतम संस्करण के साथ परीक्षण करें।

i2pd SAM डिफ़ॉल्ट रूप से सक्षम होता है; जबकि जावा I2P SAM सक्षम नहीं होता। अपने उपयोगकर्ताओं को जावा I2P में SAM सक्षम करने के लिए निर्देश प्रदान करें (राउटर कंसोल में /configclients के माध्यम से), और/या यदि प्रारंभिक कनेक्ट विफल हो जाए तो उपयोगकर्ता को एक स्पष्ट त्रुटि संदेश दें, उदाहरण के लिए: "सुनिश्चित करें कि I2P चल रहा है और SAM इंटरफ़ेस सक्षम है"।

जावा I2P और i2pd राउटर टनल मात्रा के लिए अलग-अलग डिफ़ॉल्ट का उपयोग करते हैं। जावा का डिफ़ॉल्ट 2 है और i2pd का डिफ़ॉल्ट 5 है। अधिकांश कम से मध्यम बैंडविड्थ और कम से मध्यम कनेक्शन गणना के लिए, 2 या 3 पर्याप्त है। जावा I2P और i2pd राउटर के साथ सुसंगत प्रदर्शन प्राप्त करने के लिए SESSION CREATE संदेश में टनल मात्रा निर्दिष्ट करें। नीचे देखें।

आपके अनुप्रयोग द्वारा केवल उन्हीं संसाधनों का उपयोग सुनिश्चित करने के लिए डेवलपर्स के लिए अधिक मार्गदर्शन के लिए, कृपया [अपने अनुप्रयोग के साथ I2P को एकीकृत करने के हमारे मार्गदर्शिका](/docs/applications/embedding) देखें।

### हस्ताक्षर और एन्क्रिप्शन प्रकार

I2P बहु लिपि और एन्क्रिप्शन प्रकारों का समर्थन करता है। पिछड़ी संगतता के लिए, SAM पुराने और अकुशल प्रकारों पर डिफ़ॉल्ट रूप से सेट होता है, इसलिए सभी क्लाइंटों को नए प्रकार निर्दिष्ट करने चाहिए।

हस्ताक्षर प्रकार DEST GENERATE और SESSION CREATE (अस्थायी के लिए) कमांड में निर्दिष्ट किया जाता है। सभी क्लाइंट्स को `SIGNATURE_TYPE=7` (Ed25519) सेट करना चाहिए।

एन्क्रिप्शन प्रकार SESSION CREATE कमांड में निर्दिष्ट किया जाता है। एक से अधिक एन्क्रिप्शन प्रकारों की अनुमति है। क्लाइंट्स को या तो `i2cp.leaseSetEncType=4` (केवल ECIES-X25519 के लिए) या `i2cp.leaseSetEncType=6,4` (MLKEM-768 और ECIES-X25519 के लिए, API 0.9.67 या उच्च समर्थित राउटर्स के लिए) सेट करना चाहिए।

## संस्करण 3 में परिवर्तन

### संस्करण 3.0 में परिवर्तन

संस्करण 3.0 को I2P रिलीज़ 0.7.3 में पेश किया गया था। SAM v2 एक ही I2P गंतव्य पर कई सॉकेट्स को *समानांतर रूप से* प्रबंधित करने का एक तरीका प्रदान करता था, अर्थात् क्लाइंट को एक सॉकेट पर डेटा सफलतापूर्वक भेजे जाने की प्रतीक्षा किए बिना दूसरे सॉकेट पर डेटा भेजने की आवश्यकता नहीं थी। लेकिन सभी डेटा एक ही क्लाइंट-से-SAM सॉकेट के माध्यम से गुजरता था, जिसे क्लाइंट के लिए प्रबंधित करना काफी जटिल था।

SAM v3 सॉकेट को एक अलग तरीके से प्रबंधित करता है: प्रत्येक *I2P सॉकेट* एक अद्वितीय क्लाइंट-से-SAM सॉकेट से मेल खाता है, जिसे संभालना बहुत अधिक सरल होता है। यह [BOB](/docs/api/bob) के समान है।

SAM v3 I2P के माध्यम से डेटाग्राम भेजने के लिए एक UDP पोर्ट भी प्रदान करता है, और क्लाइंट के डेटाग्राम सर्वर पर वापस I2P डेटाग्राम अग्रेषित कर सकता है।

### संस्करण 3.1 में परिवर्तन

संस्करण 3.1 को जावा I2P रिलीज़ 0.9.14 (जुलाई 2014) में पेश किया गया था। SAM 3.1 को SAM 3.0 की तुलना में बेहतर हस्ताक्षर प्रकारों के समर्थन के कारण न्यूनतम SAM कार्यान्वयन के रूप में अनुशंसित किया जाता है। i2pd भी अधिकांश 3.1 सुविधाओं का समर्थन करता है।

- DEST GENERATE और SESSION CREATE अब SIGNATURE_TYPE पैरामीटर का समर्थन करते हैं।
- HELLO VERSION में MIN और MAX पैरामीटर अब वैकल्पिक हैं।
- HELLO VERSION में MIN और MAX पैरामीटर अब एकल-अंकीय संस्करणों जैसे "3" का समर्थन करते हैं।
- अब ब्रिज सॉकेट पर RAW SEND का समर्थन किया जाता है।

### संस्करण 3.2 में परिवर्तन

संस्करण 3.2 को जावा I2P रिलीज़ 0.9.24 (जनवरी 2016) में पेश किया गया था। ध्यान दें कि वर्तमान में i2pd अधिकांश 3.2 सुविधाओं का समर्थन नहीं करता है।

#### I2CP पोर्ट और प्रोटोकॉल समर्थन

- SESSION CREATE विकल्प FROM_PORT और TO_PORT
- SESSION CREATE STYLE=RAW विकल्प PROTOCOL
- STREAM CONNECT, DATAGRAM SEND, और RAW SEND विकल्प FROM_PORT और TO_PORT
- RAW SEND विकल्प PROTOCOL
- DATAGRAM RECEIVED, RAW RECEIVED, और अग्रेषित या प्राप्त स्ट्रीम और repliable डेटाग्राम में FROM_PORT और TO_PORT शामिल हैं
- RAW सत्र विकल्प HEADER=true अग्रेषित raw डेटाग्राम के आरंभ में PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn युक्त एक पंक्ति जोड़ देगा
- पोर्ट 7655 के माध्यम से भेजे गए डेटाग्राम की पहली पंक्ति अब किसी भी 3.x संस्करण से शुरू हो सकती है
- पोर्ट 7655 के माध्यम से भेजे गए डेटाग्राम की पहली पंक्ति में FROM_PORT, TO_PORT, PROTOCOL में से कोई भी विकल्प हो सकता है
- RAW RECEIVED में PROTOCOL=nnn शामिल है

#### एसएसएल और प्रमाणीकरण

- अधिकृतकरण के लिए HELLO पैरामीटर में उपयोगकर्ता/पासवर्ड। देखें [नीचे](#authorization)।
- AUTH कमांड के साथ वैकल्पिक अधिकृतकरण विन्यास। देखें [नीचे](#authorization-configuration-sam-32-or-higher-optional-feature)।
- नियंत्रण सॉकेट पर वैकल्पिक SSL/TLS समर्थन। देखें [नीचे](#ssl)।
- स्ट्रीम फॉरवर्ड विकल्प SSL=true

#### मल्टीथ्रेडिंग

- एक ही सत्र ID पर समवर्ती लंबित STREAM ACCEPT की अनुमति दी जाती है।

#### कमांड लाइन पार्सिंग और कीपएलाइव

- सत्र और सॉकेट को बंद करने के लिए वैकल्पिक कमांड QUIT, STOP और EXIT। विवरण के लिए [नीचे](#quitstopexitinvisible-sam-32-or-higher-optional-features) देखें।
- कमांड पार्सिंग UTF-8 को उचित तरीके से संभालेगी।
- कमांड पार्सिंग उद्धरण चिह्नों के भीतर रिक्त स्थान (whitespace) को विश्वसनीय तरीके से संभालती है।
- कमांड लाइन पर उद्धरण चिह्नों को एस्केप करने के लिए बैकस्लैश '\\' का उपयोग किया जा सकता है।
- परीक्षण को टेलनेट के माध्यम से सरल बनाने हेतु सर्वर द्वारा कमांड को अपरकेस में मैप करने की अनुशंसा की जाती है।
- खाली विकल्प मान जैसे PROTOCOL या PROTOCOL= की अनुमति हो सकती है, लागू करने पर निर्भर करता है।
- कीपएलाइव के लिए PING/PONG। नीचे देखें।
- सर्वर HELLO या बाद की कमांड के लिए टाइमआउट लागू कर सकते हैं, लागू करने पर निर्भर करता है।

### संस्करण 3.3 के परिवर्तन

संस्करण 3.3 मार्च 2016 में जावा I2P संस्करण 0.9.25 में पेश किया गया था। ध्यान दें कि वर्तमान में i2pd अधिकांश 3.3 सुविधाओं का समर्थन नहीं करता है।

- एक ही सत्र का उपयोग एक साथ स्ट्रीम, डेटाग्राम और रॉ के लिए किया जा सकता है। आने वाले पैकेट और स्ट्रीम को I2P प्रोटोकॉल और to-port के आधार पर मार्ग प्रदान किया जाएगा। नीचे [प्राथमिक अनुभाग देखें](#sam-primary-sessions-v33-and-higher)।
- अब DATAGRAM SEND और RAW SEND विकल्पों SEND_TAGS, TAG_THRESHOLD, EXPIRES और SEND_LEASESET का समर्थन करते हैं। [नीचे डेटाग्राम भेजने के अनुभाग देखें](#sending-repliable-or-raw-datagrams)।

### 2025-04 परिवर्तन

अप्रैल 2025 में यहाँ दो प्रस्तावों को मानदंड में शामिल करने के लिए मंजूरी दे दी गई थी। समर्थन को इंगित करने के लिए कोई संस्करण परिवर्तन नहीं है। कुछ कार्यान्वयन अभी तक समर्थन नहीं करते हैं, और अन्य कार्यान्वयन में, समर्थन प्रारंभिक है।

- डेटाग्राम 2/3 समर्थन (प्रस्ताव 163)। SESSION CREATE और SESSION ADD (उप-सत्रों) में निर्दिष्ट। नीचे देखें।
- लीजसेट विकल्पों का पुनरुद्धार (प्रस्ताव 167)। NAMING LOOKUP OPTIONS=true के साथ निर्दिष्ट। नीचे देखें।

## संस्करण 3 प्रोटोकॉल

### सरल अज्ञात संदेशन (SAM) संस्करण 3.3 विशिष्टता अवलोकन

क्लाइंट एप्लिकेशन SAM ब्रिज से संवाद करता है, जो सभी I2P कार्यक्षमता को संभालता है (आभासी स्ट्रीम के लिए [स्ट्रीमिंग लाइब्रेरी](/docs/api/streaming) का उपयोग करके, या डेटाग्राम के लिए सीधे [I2CP](/docs/protocol/i2cp) का उपयोग करके)।

डिफ़ॉल्ट रूप से, क्लाइंट-से-SAM ब्रिज संचार एन्क्रिप्टेड और प्रमाणित नहीं होता है। SAM ब्रिज SSL/TLS कनेक्शन का समर्थन कर सकता है; कॉन्फ़िगरेशन और लागूकरण के विवरण इस विनिर्देश के दायरे से बाहर हैं। SAM 3.2 से, प्रारंभिक हैंडशेक में वैकल्पिक प्रमाणीकरण उपयोगकर्ता/पासवर्ड पैरामीटर समर्थित हैं और ब्रिज द्वारा आवश्यक हो सकते हैं।

I2P संचार कई अलग-अलग रूप ले सकते हैं:

- [आभासी स्ट्रीम](/docs/api/streaming)
- [उत्तर योग्य और प्रमाणित डेटाग्राम](/docs/specs/datagrams#repliable) (एक FROM फ़ील्ड के साथ संदेश)
- [गुमनाम डेटाग्राम](/docs/specs/datagrams#raw) (कच्चे गुमनाम संदेश)
- [डेटाग्राम2](/docs/specs/datagrams#datagram2) (एक नया उत्तर योग्य और प्रमाणित प्रारूप)
- [डेटाग्राम3](/docs/specs/datagrams#datagram3) (एक नया उत्तर योग्य लेकिन अप्रमाणित प्रारूप)

I2P संचार I2P सत्रों द्वारा समर्थित होते हैं, और प्रत्येक I2P सत्र एक पते (गंतव्य कहा जाता है) से बँधा होता है। एक I2P सत्र उपरोक्त तीन प्रकारों में से एक से संबद्ध होता है, और अन्य प्रकार के संचार को ढो नहीं सकता, जब तक [प्राथमिक सत्रों](#sam-primary-sessions-v33-and-higher) का उपयोग न किया जा रहा हो।

### एनकोडिंग और एस्केपिंग

इन सभी SAM संदेशों को एकल पंक्ति में भेजा जाता है, जिसका अंत नई पंक्ति चरित्र (\\n) द्वारा होता है। SAM 3.2 से पहले, केवल 7-बिट ASCII का समर्थन किया जाता था। SAM 3.2 से, एन्कोडिंग UTF-8 होनी चाहिए। कोई भी UTF8-एन्कोडेड कुंजियाँ या मान काम करने चाहिए।

नीचे इस विशिष्टता में दिखाया गया स्वरूप केवल पठनीयता के लिए है, और जबकि प्रत्येक संदेश में पहले दो शब्द अपने विशिष्ट क्रम में रहने चाहिए, कुंजी=मान युग्मों का क्रम बदल सकता है (उदाहरण के लिए, "ONE TWO A=B C=D" या "ONE TWO C=D A=B" दोनों पूरी तरह से वैध निर्माण हैं)। इसके अतिरिक्त, प्रोटोकॉल केस-संवेदनशील है। आगे आने वाले उदाहरणों में, ग्राहक द्वारा SAM ब्रिज को भेजे गए संदेशों के लिए "->" और SAM ब्रिज द्वारा ग्राहक को भेजे गए संदेशों के लिए "<-" का उपयोग किया गया है।

मूल कमांड या प्रतिक्रिया लाइन निम्नलिखित रूपों में से एक लेती है:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
केवल SAM 3.2 में कुछ नए कमांड्स के लिए SUBCOMMAND के बिना COMMAND समर्थित है।

कुंजी=मान युग्मों को एकल स्थान द्वारा अलग करना आवश्यक है। (SAM 3.2 से, एकाधिक स्थानों की अनुमति है) यदि मान में स्थान शामिल हैं, तो उन्हें दोहरी उद्धरण चिह्नों में लपेटना चाहिए, उदाहरण के लिए key="लंबा मान पाठ"। (SAM 3.2 से पहले, कुछ कार्यान्वयनों में यह विश्वसनीय रूप से काम नहीं करता था)

SAM 3.2 से पहले, कोई एस्केपिंग तंत्र नहीं था। SAM 3.2 से, डबल कोट्स को बैकस्लैश '\\' से एस्केप किया जा सकता है और बैकस्लैश को दो बैकस्लैश '\\\\' के रूप में दर्शाया जा सकता है।

### खाली मान

SAM 3.2 के रूप में, खाली विकल्प मान जैसे KEY, KEY=, या KEY="" की अनुमति हो सकती है, लागू करने पर निर्भर।

### केस संवेदनशीलता

जैसा कि निर्दिष्ट किया गया है, प्रोटोकॉल केस-संवेदनशील (case-sensitive) है। परीक्षण को टेलनेट (telnet) के माध्यम से आसान बनाने के लिए सर्वर द्वारा कमांड्स को अपर केस में मैप करने की अनुशंसा की जाती है, लेकिन आवश्यक नहीं है। उदाहरण के लिए इससे "hello version" कार्य कर सकता है। यह कार्यान्वयन पर निर्भर है। [I2CP](/docs/protocol/i2cp) विकल्पों को नष्ट कर देने के कारण कुंजियों (keys) या मानों को अपर केस में मैप न करें।

### SAM कनेक्शन हैंडशेक

ग्राहक और ब्रिज द्वारा प्रोटोकॉल संस्करण पर सहमति होने के बाद ही SAM संचार हो सकता है, जो ग्राहक द्वारा HELLO भेजकर और ब्रिज द्वारा HELLO REPLY भेजकर किया जाता है:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
और

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
संस्करण 3.1 (I2P 0.9.14) से, MIN और MAX पैरामीटर वैकल्पिक हैं। SAM हमेशा MIN और MAX बाधाओं के आधार पर संभव उच्चतम संस्करण लौटाएगा, या यदि कोई बाधा नहीं दी गई है तो वर्तमान सर्वर संस्करण लौटाएगा।

यदि SAM ब्रिज उपयुक्त संस्करण नहीं ढूंढ पाता है, तो यह इस प्रकार प्रतिक्रिया देता है:

```
<- HELLO REPLY RESULT=NOVERSION
```
यदि कोई त्रुटि हुई है, जैसे कि बुरे अनुरोध प्रारूप के कारण, तो यह इस प्रकार प्रतिक्रिया देता है:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### एसएसएल

सर्वर का नियंत्रण सॉकेट वैकल्पिक रूप से SSL/TLS समर्थन प्रदान कर सकता है, जैसा कि सर्वर और क्लाइंट पर कॉन्फ़िगर किया गया हो। लागूकरण अन्य परिवहन परतों को भी प्रदान कर सकते हैं; यह प्रोटोकॉल परिभाषा के दायरे से बाहर है।

#### प्राधिकरण

प्राधिकरण के लिए, क्लाइंट HELLO पैरामीटर में USER="xxx" PASSWORD="yyy" जोड़ता है। उपयोगकर्ता और पासवर्ड के लिए डबल कोट्स की अनुशंसा की गई है, लेकिन आवश्यक नहीं है। उपयोगकर्ता या पासवर्ड के अंदर आने वाले डबल कोट को बैकस्लैश से एस्केप किया जाना चाहिए। विफलता के मामले में सर्वर I2P_ERROR और एक संदेश के साथ प्रतिक्रिया देगा। उन सभी SAM सर्वरों पर SSL सक्षम करने की अनुशंसा की जाती है जहाँ प्राधिकरण आवश्यक हो।

#### समय समाप्ति

सर्वर HELLO या बाद के कमांड्स के लिए टाइमआउट लागू कर सकते हैं, जो कार्यान्वयन पर निर्भर करता है। क्लाइंट्स को कनेक्ट होने के बाद तुरंत HELLO और अगला कमांड भेजना चाहिए।

यदि HELLO प्राप्त होने से पहले टाइमआउट होता है, तो ब्रिज निम्नलिखित के साथ प्रतिक्रिया देता है:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
और फिर डिस्कनेक्ट हो जाता है।

यदि HELLO प्राप्त होने के बाद लेकिन अगले कमांड से पहले टाइमआउट होता है, तो ब्रिज निम्न के साथ उत्तर देता है:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
और फिर डिस्कनेक्ट हो जाता है।

### I2CP पोर्ट और प्रोटोकॉल

SAM 3.2 के रूप में, [I2CP](/docs/protocol/i2cp) पोर्ट और प्रोटोकॉल SAM क्लाइंट भेजने वाले द्वारा निर्दिष्ट किए जा सकते हैं जिसे [I2CP](/docs/protocol/i2cp) में पारित किया जाना है, और SAM ब्रिज प्राप्त [I2CP](/docs/protocol/i2cp) पोर्ट और प्रोटोकॉल जानकारी को SAM क्लाइंट को पारित कर देगा।

FROM_PORT और TO_PORT के लिए, वैध सीमा 0-65535 है, और डिफ़ॉल्ट 0 है।

प्रोटोकॉल के लिए, जिसे केवल आरए (RAW) के लिए निर्दिष्ट किया जा सकता है, वैध सीमा 0-255 है, और डिफ़ॉल्ट 18 है।

SESSION कमांड के लिए, निर्दिष्ट पोर्ट और प्रोटोकॉल उस सत्र के लिए डिफ़ॉल्ट होते हैं। व्यक्तिगत स्ट्रीम या डेटाग्राम के लिए, निर्दिष्ट पोर्ट और प्रोटोकॉल सत्र के डिफ़ॉल्ट को ओवरराइड करते हैं। प्राप्त स्ट्रीम या डेटाग्राम के लिए, निर्दिष्ट पोर्ट और प्रोटोकॉल [I2CP](/docs/protocol/i2cp) से प्राप्त के अनुसार होते हैं।

#### मानक आईपी से महत्वपूर्ण अंतर

I2CP पोर्ट I2P सॉकेट और डेटाग्राम के लिए हैं। ये आपके स्थानीय सॉकेट से संबंधित नहीं हैं जो SAM से जुड़ते हैं।

- पोर्ट 0 मान्य है और इसका विशेष अर्थ होता है।
- पोर्ट 1-1023 विशेष या विशेषाधिकार प्राप्त नहीं हैं।
- सर्वर डिफ़ॉल्ट रूप से पोर्ट 0 पर सुनते हैं, जिसका अर्थ है "सभी पोर्ट्स"।
- क्लाइंट डिफ़ॉल्ट रूप से पोर्ट 0 पर भेजते हैं, जिसका अर्थ है "कोई भी पोर्ट"।
- क्लाइंट डिफ़ॉल्ट रूप से पोर्ट 0 से भेजते हैं, जिसका अर्थ है "अनिर्दिष्ट"।
- सर्वर में पोर्ट 0 पर सुनने वाली सेवा हो सकती है और उच्च पोर्ट्स पर अन्य सेवाएँ सुन रही हो सकती हैं। ऐसा होने पर, पोर्ट 0 सेवा डिफ़ॉल्ट होती है, और तब कनेक्ट किया जाएगा जब आने वाला सॉकेट या डेटाग्राम पोर्ट किसी अन्य सेवा से मेल नहीं खाता हो।
- अधिकांश I2P गंतव्यों पर केवल एक सेवा चलती है, इसलिए आप डिफ़ॉल्ट का उपयोग कर सकते हैं, और I2CP पोर्ट विन्यास को अनदेखा कर सकते हैं।
- I2CP पोर्ट्स निर्दिष्ट करने के लिए SAM 3.2 या 3.3 की आवश्यकता होती है।
- यदि आपको I2CP पोर्ट्स की आवश्यकता नहीं है, तो आपको SAM 3.2 या 3.3 की आवश्यकता नहीं है; 3.1 पर्याप्त है।
- प्रोटोकॉल 0 मान्य है और इसका अर्थ "कोई भी प्रोटोकॉल" होता है। यह अनुशंसित नहीं है, और शायद काम नहीं करेगा।
- I2P सॉकेट्स को एक आंतरिक कनेक्शन ID द्वारा ट्रैक किया जाता है। इसलिए, dest:port:dest:port:protocol के 5-टुपल के अद्वितीय होने की कोई आवश्यकता नहीं है। उदाहरण के लिए, दो गंतव्यों के बीच समान पोर्ट्स के साथ कई सॉकेट्स हो सकते हैं। आउटबाउंड कनेक्शन के लिए क्लाइंट को "मुक्त पोर्ट" चुनने की आवश्यकता नहीं होती है।

यदि आप कई सबसेशन के साथ एक SAM 3.3 एप्लिकेशन डिज़ाइन कर रहे हैं, तो पोर्ट और प्रोटोकॉल का प्रभावी ढंग से उपयोग करने के बारे में सावधानीपूर्वक सोचें। अधिक जानकारी के लिए [I2CP](/docs/protocol/i2cp) विनिर्देश देखें।

### SAM सत्र

एक SAM सत्र क्लाइंट द्वारा SAM ब्रिज से एक सॉकेट खोलकर, हैंडशेक करके, और SESSION CREATE संदेश भेजकर बनाया जाता है, और जब सॉकेट डिस्कनेक्ट हो जाता है तो सत्र समाप्त हो जाता है।

प्रत्येक पंजीकृत I2P गंतव्य को एक सत्र ID (या उपनाम) के साथ विशिष्ट रूप से जोड़ा जाता है। SAM सर्वर पर सत्र ID, साथ ही PRIMARY सत्रों के लिए सबसेशन ID, वैश्विक रूप से अद्वितीय होने चाहिए। अन्य क्लाइंट्स के साथ संभावित ID टक्कर को रोकने के लिए, क्लाइंट द्वारा ID को यादृच्छिक रूप से उत्पन्न करना सर्वोत्तम अभ्यास है।

प्रत्येक सत्र का संबंध निम्नलिखित से अद्वितीय रूप से होता है:

- सॉकेट जिससे क्लाइंट सत्र बनाता है
- इसकी आईडी (या उपनाम)

#### सत्र सृजन अनुरोध

सत्र निर्माण संदेश केवल इनमें से एक रूप का उपयोग कर सकता है (अन्य रूपों के माध्यम से प्राप्त संदेशों का उत्तर एक त्रुटि संदेश के साथ दिया जाता है):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION यह निर्दिष्ट करता है कि संदेशों/स्ट्रीम्स को भेजने और प्राप्त करने के लिए किस गंतव्य का उपयोग किया जाना चाहिए। $privkey उस संयोजन का बेस 64 है जिसमें [Destination](/docs/specs/common-structures#type_Destination) के बाद [Private Key](/docs/specs/common-structures#type_PrivateKey), फिर [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) शामिल होता है, वैकल्पिक रूप से [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature) भी शामिल हो सकता है, जो बाइनरी में 663 या अधिक बाइट्स और बेस 64 में 884 या अधिक बाइट्स का होता है, जो हस्ताक्षर प्रकार पर निर्भर करता है। बाइनरी प्रारूप को Private Key File में निर्दिष्ट किया गया है। नीचे दिए गए Destination Key Generation अनुभाग में [Private Key](/docs/specs/common-structures#type_PrivateKey) के बारे में अतिरिक्त टिप्पणियाँ देखें।

यदि हस्ताक्षर कुंजी (signing private key) सभी शून्य है, तो [ऑफ़लाइन हस्ताक्षर](/docs/specs/common-structures#struct_OfflineSignature) खंड अनुसरण करता है। ऑफ़लाइन हस्ताक्षर केवल STREAM और RAW सत्रों के लिए समर्थित हैं। DESTINATION=TRANSIENT के साथ ऑफ़लाइन हस्ताक्षर नहीं बनाए जा सकते। ऑफ़लाइन हस्ताक्षर खंड का प्रारूप इस प्रकार है:

1. समाप्ति टाइमस्टैम्प (4 बाइट, बड़े-एंडियन, एपॉक के बाद के सेकंड, 2106 में ओवरफ्लो होगा)
2. पारगमन हस्ताक्षर सार्वजनिक कुंजी का हस्ताक्षर प्रकार (2 बाइट, बड़े-एंडियन)
3. पारगमन हस्ताक्षर सार्वजनिक कुंजी (पारगमन हस्ताक्षर प्रकार द्वारा निर्दिष्ट लंबाई के अनुसार)
4. ऑफ़लाइन कुंजी द्वारा ऊपर के तीन क्षेत्रों का हस्ताक्षर (गंतव्य हस्ताक्षर प्रकार द्वारा निर्दिष्ट लंबाई के अनुसार)
5. पारगमन हस्ताक्षर निजी कुंजी (पारगमन हस्ताक्षर प्रकार द्वारा निर्दिष्ट लंबाई के अनुसार)

यदि गंतव्य को TRANSIENT के रूप में निर्दिष्ट किया गया है, तो SAM ब्रिज एक नया गंतव्य बनाता है। संस्करण 3.1 (I2P 0.9.14) से, यदि गंतव्य TRANSIENT है, तो एक वैकल्पिक पैरामीटर SIGNATURE_TYPE समर्थित है। SIGNATURE_TYPE मान [Key Certificates](/docs/specs/common-structures#type_Certificate) द्वारा समर्थित कोई भी नाम (उदाहरण के लिए ECDSA_SHA256_P256, केस असंवेदनशील) या संख्या (उदाहरण के लिए 1) हो सकता है। डिफ़ॉल्ट DSA_SHA1 है, जो आपकी आवश्यकता नहीं है। अधिकांश अनुप्रयोगों के लिए, कृपया SIGNATURE_TYPE=7 निर्दिष्ट करें।

$nickname क्लाइंट की पसंद है। कोई व्हाइटस्पेस की अनुमति नहीं है।

दिए गए अतिरिक्त विकल्पों को SAM ब्रिज द्वारा व्याख्या नहीं किए जाने पर I2P सत्र विन्यास में पारित किया जाता है (उदाहरण के लिए, outbound.length=0)।

जावा I2P और i2pd राउटर टनल मात्रा के लिए अलग-अलग डिफ़ॉल्ट रखते हैं। जावा का डिफ़ॉल्ट 2 है और i2pd का डिफ़ॉल्ट 5 है। अधिकांश कम से मध्यम बैंडविड्थ और कम से मध्यम कनेक्शन गणना के लिए, 2 या 3 पर्याप्त है। जावा I2P और i2pd राउटर के साथ सुसंगत प्रदर्शन प्राप्त करने के लिए SESSION CREATE संदेश में टनल मात्रा निर्दिष्ट करें, विकल्पों का उपयोग करें जैसे inbound.quantity=3 outbound.quantity=3। इन और अन्य विकल्पों को नीचे दिए गए लिंक में दस्तावेज़ीकृत किया गया है](#tunnel-i2cp-and-streaming-options)।

SAM ब्रिज को पहले से ही यह कॉन्फ़िगर किया जाना चाहिए कि वह I2P के माध्यम से किस राउटर के साथ संचार करे (हालाँकि आवश्यकता होने पर ओवरराइड प्रदान करने का तरीका हो सकता है, उदाहरण के लिए i2cp.tcp.host=localhost और i2cp.tcp.port=7654)।

#### सत्र सृजन प्रतिक्रिया

सत्र निर्माण संदेश प्राप्त करने के बाद, SAM ब्रिज निम्नलिखित के अनुसार एक सत्र स्थिति संदेश के साथ उत्तर देगा:

यदि निर्माण सफल रहा:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey उसके बाद [निजी कुंजी](/docs/specs/common-structures#type_PrivateKey) और उसके बाद [हस्ताक्षर निजी कुंजी](/docs/specs/common-structures#type_SigningPrivateKey) के संयोजन का आधार 64 है, वैकल्पिक रूप से [ऑफलाइन हस्ताक्षर](/docs/specs/common-structures#struct_OfflineSignature) के साथ, जो बाइनरी में 663 या अधिक बाइट्स और आधार 64 में 884 या अधिक बाइट्स है, हस्ताक्षर प्रकार के आधार पर। बाइनरी प्रारूप निजी कुंजी फ़ाइल में निर्दिष्ट है।

यदि SESSION CREATE में सभी शून्यों की एक साइनिंग निजी कुंजी और एक [ऑफ़लाइन साइनेचर](/docs/specs/common-structures#struct_OfflineSignature) अनुभाग शामिल था, तो SESSION STATUS प्रतिक्रिया में उसी स्वरूप में समान डेटा शामिल होगा। विवरण के लिए ऊपर SESSION CREATE अनुभाग देखें।

यदि उपनाम पहले से ही एक सत्र से जुड़ा हुआ है:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
यदि गंतव्य पहले से उपयोग में है:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
यदि गंतव्य एक मान्य निजी गंतव्य कुंजी नहीं है:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
यदि कोई अन्य त्रुटि हुई है:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
यदि यह ठीक नहीं है, तो सत्र बनाए न जा सकने के कारण के बारे में मानव-पठनीय जानकारी MESSAGE में शामिल होनी चाहिए।

ध्यान दें कि राउटर SESSION STATUS के साथ प्रतिक्रिया देने से पहले टनल बनाता है। इसमें कई सेकंड लग सकते हैं, या राउटर प्रारंभ होने या गंभीर नेटवर्क भीड़ के दौरान एक मिनट या अधिक समय लग सकता है। यदि असफल होता है, तो राउटर कई मिनटों तक विफलता संदेश के साथ प्रतिक्रिया नहीं देगा। प्रतिक्रिया की प्रतीक्षा करते समय छोटे समय सीमा (timeout) को सेट न करें। टनल निर्माण जारी होने के दौरान सत्र छोड़कर पुनः प्रयास न करें।

SAM सत्र उस सॉकेट के साथ जीते हैं और मरते हैं जिसके साथ वे जुड़े होते हैं। जब सॉकेट बंद हो जाता है, तो सत्र समाप्त हो जाता है, और सत्र का उपयोग करके सभी संचार एक साथ समाप्त हो जाते हैं। और इसके विपरीत, जब किसी भी कारण से सत्र समाप्त हो जाता है, तो SAM ब्रिज सॉकेट को बंद कर देता है।

### SAM वर्चुअल स्ट्रीम्स

वर्चुअल स्ट्रीम को विश्वसनीय तरीके से और क्रम में भेजे जाने की गारंटी दी जाती है, जैसे ही उपलब्ध हो, विफलता और सफलता की सूचना के साथ।

स्ट्रीम दो I2P गंतव्यों के बीच द्विदिश योग्य संचार सॉकेट होते हैं, लेकिन उनका खुलना उनमें से एक द्वारा अनुरोधित होना चाहिए। आगे, ऐसे अनुरोध के लिए SAM क्लाइंट द्वारा CONNECT कमांड का उपयोग किया जाता है। जब SAM क्लाइंट अन्य I2P गंतव्यों से आने वाले अनुरोधों को सुनना चाहता है, तो वह FORWARD / ACCEPT कमांड का उपयोग करता है।

### SAM आभासी स्ट्रीम: CONNECT

एक क्लाइंट निम्न द्वारा एक कनेक्शन के लिए पूछता है:

- SAM ब्रिज के साथ एक नया सॉकेट खोलना
- ऊपर दिए गए अनुसार ही HELLO हैंडशेक भेजना
- STREAM CONNECT कमांड भेजना

#### कनेक्ट अनुरोध

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
यह $nickname आईडी वाले स्थानीय सत्र से निर्दिष्ट पीयर तक एक नया आभासी संबंध स्थापित करता है।

लक्ष्य $destination है, जो [Destination](/docs/specs/common-structures#type_Destination) का आधार 64 है, जिसमें हस्ताक्षर प्रकार के आधार पर 516 या अधिक आधार 64 अक्षर (बाइनरी में 387 या अधिक बाइट्स) होते हैं।

**नोट:** लगभग 2014 से (SAM v3.1), जावा I2P ने $destination के लिए होस्टनाम और b32 पतों का भी समर्थन किया है, लेकिन यह पहले अदस्तावेज़ीकृत था। होस्टनाम और b32 पते अब जावा I2P द्वारा आधिकारिक तौर पर संस्करण 0.9.48 से समर्थित हैं। i2pd राउटर संस्करण 2.38.0 (0.9.50) से होस्टनाम और b32 पतों का समर्थन करता है। दोनों राउटर्स के लिए, "b32" समर्थन में अंधे गंतव्यों के लिए विस्तारित "b33" पतों का समर्थन शामिल है।

#### कनेक्ट प्रतिक्रिया

यदि SILENT=true पारित किया जाता है, तो SAM ब्रिज सॉकेट पर कोई अन्य संदेश जारी नहीं करेगा। यदि कनेक्शन विफल हो जाता है, तो सॉकेट बंद कर दिया जाएगा। यदि कनेक्शन सफल हो जाता है, तो वर्तमान सॉकेट से गुजरने वाला सभी शेष डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाएगा और उससे अग्रेषित किया जाएगा।

यदि SILENT=false, जो डिफ़ॉल्ट मान है, तो SAM ब्रिज सॉकेट को अग्रेषित करने या बंद करने से पहले अपने क्लाइंट को अंतिम संदेश भेजता है:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
परिणाम मान निम्नलिखित में से एक हो सकता है:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
यदि परिणाम OK है, तो वर्तमान सॉकेट से गुजरने वाला सभी शेष डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाता है और उससे अग्रेषित किया जाता है। यदि कनेक्शन संभव नहीं था (टाइमआउट, आदि), तो परिणाम उपयुक्त त्रुटि मान (एक वैकल्पिक मानव-पठनीय संदेश के साथ) युक्त होगा, और SAM ब्रिज सॉकेट को बंद कर देता है।

राउटर स्ट्रीम कनेक्ट टाइमआउट आंतरिक रूप से लगभग एक मिनट का होता है, जो लागूकरण पर निर्भर करता है। प्रतिक्रिया की प्रतीक्षा में कम समय के लिए टाइमआउट सेट न करें।

### SAM आभासी स्ट्रीम: स्वीकार करें

एक क्लाइंट आने वाले कनेक्शन अनुरोध की प्रतीक्षा इस प्रकार करता है:

- SAM ब्रिज के साथ एक नया सॉकेट खोलना
- ऊपर दिए गए अनुसार ही HELLO हैंडशेक भेजना
- STREAM ACCEPT कमांड भेजना

#### अनुरोध स्वीकार करें

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
यह सत्र को ${nickname} आई2पी नेटवर्क से एक आने वाले कनेक्शन अनुरोध के लिए सुनने के लिए बनाता है। सत्र पर सक्रिय FORWARD होने के दौरान ACCEPT की अनुमति नहीं है।

SAM 3.2 के रूप में, एक ही सत्र ID पर (यहां तक कि एक ही पोर्ट के साथ भी) कई एक साथ लंबित STREAM ACCEPT की अनुमति है। 3.2 से पहले, एक साथ स्वीकृति ALREADY_ACCEPTING के साथ विफल हो जाएगी। नोट: जावा I2P भी SAM 3.1 पर एक साथ स्वीकृति का समर्थन करता है, संस्करण 0.9.24 (2016-01) से। i2pd भी SAM 3.1 पर एक साथ स्वीकृति का समर्थन करता है, संस्करण 2.50.0 (2023-12) से।

#### प्रतिक्रिया स्वीकार करें

यदि SILENT=true पारित किया जाता है, तो SAM ब्रिज सॉकेट पर कोई अन्य संदेश जारी नहीं करेगा। यदि स्वीकृति विफल हो जाती है, तो सॉकेट बंद कर दिया जाएगा। यदि स्वीकृति सफल हो जाती है, तो वर्तमान सॉकेट से गुजरने वाला सभी शेष डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाएगा और उससे वापस आएगा। विश्वसनीयता के लिए, और आने वाले कनेक्शन के लिए गंतव्य प्राप्त करने के लिए, SILENT=false की अनुशंसा की जाती है।

यदि SILENT=false, जो डिफ़ॉल्ट मान है, तो SAM ब्रिज निम्न के साथ उत्तर देता है:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
परिणाम मान निम्नलिखित में से एक हो सकता है:

```
OK
I2P_ERROR
INVALID_ID
```
यदि परिणाम OK नहीं है, तो सॉकेट को SAM ब्रिज द्वारा तुरंत बंद कर दिया जाता है। यदि परिणाम OK है, तो SAM ब्रिज किसी अन्य I2P पीयर से आने वाले कनेक्शन अनुरोध की प्रतीक्षा शुरू कर देता है। जब कोई अनुरोध पहुँचता है, तो SAM ब्रिज इसे स्वीकार कर लेता है और:

यदि SILENT=true पारित किया गया है, तो SAM ब्रिज क्लाइंट सॉकेट पर कोई अन्य संदेश जारी नहीं करेगा। वर्तमान सॉकेट से गुजरने वाला शेष सभी डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाता है और उससे अग्रेषित किया जाता है।

यदि SILENT=false पारित किया गया था, जो डिफ़ॉल्ट मान है, तो SAM ब्रिज क्लाइंट को अनुरोध करने वाले पीयर की base64 सार्वजनिक गंतव्य कुंजी युक्त एक ASCII लाइन भेजता है, और केवल SAM 3.2 के लिए अतिरिक्त जानकारी:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
इस '\\n' से समाप्त होने वाली पंक्ति के बाद, वर्तमान सॉकेट के माध्यम से जाने वाला सभी शेष डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाता है और उससे अग्रेषित किया जाता है, जब तक कि कोई भी पीयर सॉकेट को बंद न कर दे।

#### ठीक के बाद त्रुटियाँ

कुछ दुर्लभ मामलों में, SAM ब्रिज को RESULT=OK भेजने के बाद लेकिन कनेक्शन आने और क्लाइंट को $destination लाइन भेजने से पहले एक त्रुटि का सामना करना पड़ सकता है। इन त्रुटियों में राउटर बंद होना, राउटर पुनः आरंभ होना और सत्र बंद होना शामिल हो सकते हैं। ऐसे मामलों में, जब SILENT=false हो, तो SAM ब्रिज लाइन भेज सकता है, लेकिन उसके लिए आवश्यक नहीं है (लागूकरण पर निर्भर), निम्न लाइन भेज सकता है:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
सॉकेट को तुरंत बंद करने से पहले। निश्चित रूप से, यह पंक्ति एक वैध बेस 64 गंतव्य के रूप में डिकोड करने योग्य नहीं है।

### SAM आभासी स्ट्रीम: आगे भेजें

एक क्लाइंट सामान्य सॉकेट सर्वर का उपयोग कर सकता है और I2P से आने वाले कनेक्शन अनुरोधों की प्रतीक्षा कर सकता है। इसके लिए, क्लाइंट को निम्नलिखित करना चाहिए:

- SAM ब्रिज के साथ एक नया सॉकेट खोलें
- ऊपर की तरह ही HELLO हैंडशेक भेजें
- फॉरवर्ड कमांड भेजें

#### अग्रेषित अनुरोध

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
यह सत्र को ${nickname} I2P नेटवर्क से आने वाले कनेक्शन अनुरोधों के लिए सुनने के लिए सक्षम करता है। सत्र पर ACCEPT के लंबित होने के दौरान FORWARD की अनुमति नहीं है।

#### अग्र प्रतिक्रिया

SILENT का डिफ़ॉल्ट मान false होता है। चाहे SILENT का मान true हो या false, SAM ब्रिज हमेशा एक STREAM STATUS संदेश के साथ उत्तर देता है। ध्यान दें कि यह व्यवहार STREAM ACCEPT और STREAM CONNECT के मामले में SILENT=true होने पर अलग होता है। STREAM STATUS संदेश यह है:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
परिणाम मान निम्नलिखित में से एक हो सकता है:

```
OK
I2P_ERROR
INVALID_ID
```
$host सॉकेट सर्वर का होस्टनाम या आईपी पता है जिसकी ओर SAM कनेक्शन अनुरोध अग्रेषित करेगा। यदि न दिया गया हो, तो SAM उस सॉकेट का आईपी लेता है जिसने फॉरवर्ड कमान जारी की थी।

$port सॉकेट सर्वर का पोर्ट नंबर है जिस पर SAM कनेक्शन अनुरोध अग्रेषित करेगा। यह अनिवार्य है।

जब I2P से एक कनेक्शन अनुरोध आता है, तो SAM ब्रिज $host:$port पर एक सॉकेट कनेक्शन खोलता है। यदि इसे 3 सेकंड से कम समय में स्वीकार कर लिया जाता है, तो SAM I2P से कनेक्शन स्वीकार कर लेगा, और फिर:

यदि SILENT=true पारित किया गया था, तो प्राप्त वर्तमान सॉकेट से गुजरने वाले सभी डेटा को जुड़े हुए I2P गंतव्य पीयर को भेजा जाता है और उससे वापस भेजा जाता है।

यदि SILENT=false पारित किया गया था, जो डिफ़ॉल्ट मान है, तो SAM ब्रिज प्राप्त सॉकेट पर एक ASCII लाइन भेजता है जिसमें अनुरोध करने वाले पीयर की बेस64 सार्वजनिक गंतव्य कुंजी शामिल होती है, और केवल SAM 3.2 के लिए अतिरिक्त जानकारी:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
इस '\\n' से समाप्त पंक्ति के बाद, सॉकेट के माध्यम से जाने वाला सभी शेष डेटा जुड़े हुए I2P गंतव्य पीयर को अग्रेषित किया जाता है, जब तक कि किसी एक पक्ष द्वारा सॉकेट बंद नहीं कर दिया जाता।

SAM 3.2 के अनुसार, यदि SSL=true निर्दिष्ट किया गया है, तो अग्रेषण सॉकेट SSL/TLS के माध्यम से होता है।

जैसे ही "फॉरवर्डिंग" सॉकेट बंद होता है, I2P राउटर आने वाले कनेक्शन अनुरोधों को सुनना बंद कर देगा।

### SAM डेटाग्राम

SAMv3 स्थानीय डेटाग्राम सॉकेट के माध्यम से डेटाग्राम भेजने और प्राप्त करने के तंत्र प्रदान करता है। कुछ SAMv3 कार्यान्वयन SAM ब्रिज सॉकेट के माध्यम से डेटाग्राम भेजने/प्राप्त करने के पुराने v1/v2 तरीके का भी समर्थन करते हैं। नीचे दोनों के बारे में दस्तावेजीकरण किया गया है।

I2P डेटाग्राम के चार प्रकार का समर्थन करता है:

- रिप्लाय योग्य और प्रमाणित डेटाग्राम में प्रेषक के गंतव्य से पूर्वप्रत्ययित होते हैं, और प्रेषक के हस्ताक्षर शामिल होते हैं, ताकि प्राप्तकर्ता यह सत्यापित कर सके कि प्रेषक का गंतव्य नकली नहीं है, और डेटाग्राम को उत्तर दे सके। नया Datagram2 प्रारूप भी रिप्लाय योग्य और प्रमाणित है।
- नया Datagram3 प्रारूप रिप्लाय योग्य है लेकिन प्रमाणित नहीं है। प्रेषक की जानकारी सत्यापित नहीं है।
- कच्चे डेटाग्राम में प्रेषक का गंतव्य या हस्ताक्षर शामिल नहीं होता है।

प्रतिक्रियाशील और रॉ डेटाग्राम दोनों के लिए डिफ़ॉल्ट I2CP पोर्ट निर्धारित हैं। रॉ डेटाग्राम के लिए I2CP पोर्ट बदला जा सकता है।

एक सामान्य प्रोटोकॉल डिज़ाइन पैटर्न सर्वर को उत्तर योग्य डेटाग्राम भेजने के लिए कुछ पहचानकर्ता (आइडेंटिफायर) सहित होता है, और सर्वर उस पहचानकर्ता को शामिल करके एक कच्चे डेटाग्राम के रूप में प्रतिक्रिया देता है, ताकि प्रतिक्रिया को अनुरोध के साथ संबंधित किया जा सके। यह डिज़ाइन पैटर्न उत्तरों में उत्तर योग्य डेटाग्राम के महत्वपूर्ण ओवरहेड को खत्म कर देता है। I2CP प्रोटोकॉल और पोर्ट्स के सभी विकल्प अनुप्रयोग-विशिष्ट होते हैं, और डिज़ाइनरों को इन मुद्दों पर विचार करना चाहिए।

नीचे दिए गए अनुभाग में डेटाग्राम MTU पर महत्वपूर्ण टिप्पणियों को भी देखें।

#### उत्तर योग्य या कच्चे डेटाग्राम भेजना

हालांकि I2P में अंतर्निहित रूप से कोई FROM पता नहीं होता है, लेकिन उपयोग की सुविधा के लिए रिप्लाई योग्य डेटाग्राम के रूप में एक अतिरिक्त परत प्रदान की जाती है — 31744 बाइट्स तक के अव्यवस्थित और अविश्वसनीय संदेश जिनमें एक FROM पता शामिल होता है (जिससे हेडर सामग्री के लिए लगभग 1KB तक का स्थान बचता है)। यह FROM पता SAM द्वारा आंतरिक रूप से प्रमाणित किया जाता है (स्रोत को सत्यापित करने के लिए गंतव्य की साइनिंग कुंजी का उपयोग करके) और पुनः प्रेषण रोकथाम (replay prevention) भी शामिल होती है।

न्यूनतम आकार 1 है। वितरण की विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है। विश्वसनीयता संदेश के आकार के व्युत्क्रमानुपाती होती है, शायद घातीय रूप से भी।

STYLE=DATAGRAM या STYLE=RAW के साथ SAM सत्र स्थापित करने के बाद, क्लाइंट SAM के UDP पोर्ट (डिफ़ॉल्ट रूप से 7655) के माध्यम से repliable या raw डेटाग्राम भेज सकता है।

इस पोर्ट के माध्यम से भेजे गए डेटाग्राम की पहली पंक्ति निम्नलिखित प्रारूप में होनी चाहिए। यह पूरा एक ही पंक्ति में होता है (स्पेस से अलग किया गया), स्पष्टता के लिए कई पंक्तियों में दिखाया गया है:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 SAM का संस्करण है। SAM 3.2 से, कोई भी 3.x संस्करण अनुमत है।
- $nickname उस DATAGRAM सत्र की पहचान है जिसका उपयोग किया जाएगा
- लक्ष्य $destination है, जो [Destination](/docs/specs/common-structures#type_Destination) का आधार 64 है, जिसमें 516 या अधिक आधार 64 वर्ण (बाइनरी में 387 या अधिक बाइट्स), हस्ताक्षर प्रकार के आधार पर भिन्न होता है। **नोट:** लगभग 2014 (SAM v3.1) से, जावा I2P लक्ष्य के लिए होस्टनाम और b32 पते का भी समर्थन करता है, लेकिन यह पहले दस्तावेजीकृत नहीं था। होस्टनाम और b32 पते अब जावा I2P द्वारा आधिकारिक तौर पर संस्करण 0.9.48 से समर्थित हैं। i2pd राउटर वर्तमान में होस्टनाम और b32 पतों का समर्थन नहीं करता है; भविष्य में इसका समर्थन जोड़ा जा सकता है।
- सभी विकल्प प्रति-डेटाग्राम सेटिंग्स हैं जो SESSION CREATE में निर्दिष्ट डिफ़ॉल्ट को ओवरराइड करती हैं।
- संस्करण 3.3 के विकल्प SEND_TAGS, TAG_THRESHOLD, EXPIRES, और SEND_LEASESET को [I2CP](/docs/protocol/i2cp) को भेज दिया जाएगा यदि समर्थित हो। विवरण के लिए [I2CP विशिष्टता](/docs/protocol/i2cp#msg_SendMessageExpire) देखें। SAM सर्वर द्वारा इन विकल्पों का समर्थन ऐच्छिक है, यदि असमर्थित हो तो यह इन विकल्पों को नजरअंदाज कर देगा।
- यह पंक्ति '\\n' से समाप्त होती है।

संदेश के शेष डेटा को निर्दिष्ट गंतव्य पर भेजने से पहले SAM द्वारा पहली पंक्ति को त्याग दिया जाएगा।

उत्तर योग्य और कच्चे डेटाग्राम भेजने की एक वैकल्पिक विधि के लिए, [डेटाग्राम भेजें और कच्चा भेजें](#datagram-send-raw-send-v1v2-compatible-datagram-handling) देखें।

#### SAM प्रतिक्रियाशील डेटाग्राम: एक डेटाग्राम की प्राप्ति

यदि SESSION CREATE कमांड में अग्रेषित पोर्ट (forwarding PORT) निर्दिष्ट नहीं किया गया है, तो प्राप्त डेटाग्राम को SAM द्वारा उस सॉकेट पर लिखा जाता है जिससे डेटाग्राम सत्र खोला गया था। डेटाग्राम प्राप्त करने का यह v1/v2-अनुकूल तरीका है।

जब एक डेटाग्राम पहुँचता है, तो ब्रिज इसे संदेश के माध्यम से क्लाइंट को वितरित करता है:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
स्रोत $destination है, जो [डेस्टिनेशन](/docs/specs/common-structures#type_Destination) का बेस 64 है, जिसमें हस्ताक्षर प्रकार के आधार पर 516 या अधिक बेस 64 अक्षर (बाइनरी में 387 या अधिक बाइट्स) होते हैं।

SAM ब्रिज कभी भी क्लाइंट के लिए प्रमाणीकरण हेडर या अन्य फ़ील्ड को प्रदर्शित नहीं करता है, केवल वह डेटा प्रदान करता है जो प्रेषक ने दिया था। यह तब तक जारी रहता है जब तक कि सत्र बंद नहीं हो जाता (क्लाइंट द्वारा कनेक्शन छोड़ने पर)।

#### कच्चे या पुनः उत्तर योग्य डेटाग्राम अग्रेषित करना

डेटाग्राम सत्र बनाते समय, क्लाइंट SAM से आगे आने वाले संदेशों को निर्दिष्ट ip:port पर अग्रेषित करने के लिए कह सकता है। ऐसा वह PORT और HOST विकल्पों के साथ CREATE कमांड जारी करके करता है:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey उसके बाद [निजी कुंजी](/docs/specs/common-structures#type_PrivateKey) के बाद [हस्ताक्षर निजी कुंजी](/docs/specs/common-structures#type_SigningPrivateKey) के संयोजन का आधार 64 है, वैकल्पिक रूप से [ऑफ़लाइन हस्ताक्षर](/docs/specs/common-structures#struct_OfflineSignature) के साथ, जो 884 या अधिक आधार 64 वर्ण (बाइनरी में 663 या अधिक बाइट्स) है, हस्ताक्षर प्रकार के आधार पर। बाइनरी प्रारूप निजी कुंजी फ़ाइल में निर्दिष्ट है।

RAW, DATAGRAM2 और DATAGRAM3 डेटाग्राम के लिए ऑफ़लाइन हस्ताक्षर समर्थित हैं, लेकिन DATAGRAM के लिए नहीं। विवरण के लिए ऊपर दिए गए SESSION CREATE अनुभाग और नीचे दिए गए DATAGRAM2/3 अनुभाग देखें।

$host वह होस्टनाम या आईपी पता है जिस पर डेटाग्राम सर्वर स्थित है, जिसकी ओर SAM डेटाग्राम अग्रेषित करेगा। यदि न दिया गया हो, तो SAM उस सॉकेट का आईपी लेता है जिसने फॉरवर्ड कमांड जारी किया था।

$port डेटाग्राम सर्वर का पोर्ट नंबर है जिसकी ओर SAM डेटाग्राम अग्रेषित करेगा। यदि $port सेट नहीं है, तो डेटाग्राम अग्रेषित नहीं किए जाएंगे, वे नियंत्रण सॉकेट पर v1/v2-अनुकूल तरीके से प्राप्त किए जाएंगे।

अतिरिक्त विकल्प जो दिए गए हैं, उन्हें SAM ब्रिज द्वारा व्याख्या नहीं किए जाने पर I2P सत्र विन्यास में पारित कर दिया जाता है (उदाहरण के लिए, outbound.length=0)। इन विकल्पों को [नीचे दस्तावेज़ीकृत किया गया है](#tunnel-i2cp-and-streaming-options)।

अग्रेषित उत्तर-योग्य डेटाग्राम हमेशा base64 गंतव्य से पूर्व-निर्धारित होते हैं, सिवाय Datagram3 के, नीचे देखें। जब कोई उत्तर-योग्य डेटाग्राम पहुँचता है, तो ब्रिज निर्दिष्ट होस्ट:पोर्ट पर निम्नलिखित डेटा युक्त UDP पैकेट भेजता है:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
अग्रेषित कच्चे डेटाग्राम निर्दिष्ट होस्ट:पोर्ट पर उसी रूप में अग्रेषित किए जाते हैं बिना किसी उपसर्ग के। यूडीपी पैकेट में निम्नलिखित डेटा शामिल है:

```
$datagram_payload
```
SAM 3.2 के अनुसार, जब SESSION CREATE में HEADER=true निर्दिष्ट किया जाता है, तो अग्रेषित रॉ डेटाग्राम में निम्नलिखित तरीके से एक हेडर लाइन को आगे जोड़ दिया जाएगा:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination [Destination](/docs/specs/common-structures#type_Destination) का बेस 64 है, जिसमें हस्ताक्षर प्रकार के आधार पर 516 या अधिक बेस 64 अक्षर (बाइनरी में 387 या अधिक बाइट्स) होते हैं।

#### SAM अनाम (कच्चे) डेटाग्राम

I2P की बैंडविड्थ का अधिकतम उपयोग करते हुए, SAM क्लाइंट को गुमनाम डेटाग्राम भेजने और प्राप्त करने की अनुमति देता है, जहां प्रमाणीकरण और उत्तर की जानकारी क्लाइंट के स्वयं पर छोड़ दी जाती है। ये डेटाग्राम अविश्वसनीय और बिना क्रम के होते हैं, और अधिकतम 32768 बाइट्स तक के हो सकते हैं।

न्यूनतम आकार 1 है। वितरण की विश्वसनीयता के लिए, अनुशंसित अधिकतम आकार लगभग 11 KB है।

STYLE=RAW के साथ SAM सत्र स्थापित करने के बाद, क्लाइंट SAM ब्रिज के माध्यम से बिल्कुल उसी तरह से अज्ञात डेटाग्राम भेज सकता है जैसे [उत्तर योग्य या कच्चे डेटाग्राम भेजने](#sending-repliable-or-raw-datagrams) के लिए किया जाता है।

डेटाग्राम प्राप्त करने के दोनों तरीके अज्ञात डेटाग्राम के लिए भी उपलब्ध हैं।

यदि SESSION CREATE कमांड में अग्रेषित पोर्ट (forwarding PORT) निर्दिष्ट नहीं किया गया है, तो प्राप्त डेटाग्राम को SAM द्वारा उस सॉकेट पर लिखा जाता है जिससे डेटाग्राम सत्र खोला गया था। डेटाग्राम प्राप्त करने का यह v1/v2-अनुकूल तरीका है।

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
जब किसी होस्ट:पोर्ट पर अज्ञात डेटाग्राम अग्रेषित किए जाने हों, तो ब्रिज निर्दिष्ट होस्ट:पोर्ट को निम्नलिखित डेटा युक्त संदेश भेजता है:

```
$datagram_payload
```
SAM 3.2 के अनुसार, जब SESSION CREATE में HEADER=true निर्दिष्ट किया जाता है, तो अग्रेषित रॉ डेटाग्राम में निम्नलिखित तरीके से एक हेडर लाइन को आगे जोड़ दिया जाएगा:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
एनाउनिमस डेटाग्राम भेजने की वैकल्पिक विधि के लिए, [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling) देखें।

#### डेटाग्राम 2/3

डेटाग्राम 2/3 अर्ली 2025 में निर्दिष्ट नए प्रारूप हैं। वर्तमान में कोई ज्ञात कार्यान्वयन मौजूद नहीं है। वर्तमान स्थिति के लिए कार्यान्वयन दस्तावेज़ीकरण देखें। अधिक जानकारी के लिए [विनिर्देश](/docs/specs/datagrams) देखें।

डेटाग्राम 2/3 समर्थन को दर्शाने के लिए SAM संस्करण को बढ़ाने की कोई वर्तमान योजना नहीं है। यह एक समस्या हो सकती है क्योंकि कार्यान्वयन डेटाग्राम 2/3 को समर्थन देना चाह सकते हैं लेकिन SAM v3.3 सुविधाओं को नहीं। कोई भी संस्करण परिवर्तन TBD (अभी निर्धारित नहीं) है।

डेटाग्राम2 और डेटाग्राम3 दोनों में उत्तर देने की क्षमता होती है। केवल डेटाग्राम2 प्रमाणित है।

डेटाग्राम2 सैम दृष्टिकोण से पुनः भेजे जा सकने वाले डेटाग्राम के समान है। दोनों की प्रमाणीकरण की गई होती है। केवल आई2सीपी प्रारूप और हस्ताक्षर भिन्न होते हैं, लेकिन यह सैम क्लाइंट्स के लिए दृश्यमान नहीं होता है। डेटाग्राम2 ऑफ़लाइन हस्ताक्षर का भी समर्थन करता है, इसलिए इसका उपयोग ऑफ़लाइन हस्ताक्षरित गंतव्य द्वारा किया जा सकता है।

इरादा यह है कि नई ऐप्लिकेशन्स के लिए Repliable डेटाग्राम को Datagram2 द्वारा प्रतिस्थापित किया जाए जिन्हें पिछड़ी संगतता की आवश्यकता नहीं होती। Datagram2 में पुनः भेजने की सुरक्षा उपलब्ध है जो Repliable डेटाग्राम में नहीं होती। यदि पिछड़ी संगतता की आवश्यकता हो, तो एक ऐप्लिकेशन SAM 3.3 PRIMARY सत्रों के साथ एक ही सत्र पर Datagram2 और Repliable दोनों का समर्थन कर सकता है।

डेटाग्राम3 उत्तर देने योग्य है लेकिन प्रमाणित नहीं है। I2CP प्रारूप में 'from' फ़ील्ड एक हैश है, गंतव्य नहीं। SAM सर्वर द्वारा क्लाइंट को भेजा गया $destination 44-बाइट बेस64 हैश होगा। उत्तर के लिए पूर्ण गंतव्य में इसे परिवर्तित करने के लिए, इसे 32-बाइट बाइनरी में बेस64-डिकोड करें, फिर इसे 52 अक्षरों में बेस32-एनकोड करें और NAMING LOOKUP के लिए ".b32.i2p" जोड़ें। जैसा कि सामान्य है, बार-बार NAMING LOOKUP से बचने के लिए क्लाइंट को अपना कैश बनाए रखना चाहिए।

एप्लिकेशन डिजाइनरों को असुरक्षित डेटाग्राम के सुरक्षा निहितार्थों पर विचार करते हुए अत्यधिक सावधानी बरतनी चाहिए।

#### V3 डेटाग्राम MTU पर विचार

I2P डेटाग्राम आम इंटरनेट MTU 1500 की तुलना में बड़े हो सकते हैं। 516+ बाइट के बेस64 गंतव्य के साथ उपसर्गित स्थानीय रूप से भेजे गए डेटाग्राम और अग्रेषित उत्तर योग्य डेटाग्राम उस MTU से अधिक होने की संभावना है। हालांकि, लिनक्स सिस्टम पर लोकलहोस्ट MTU आमतौर पर बहुत बड़ा होता है, उदाहरण के लिए 65536। लोकलहोस्ट MTU ओएस के अनुसार भिन्न होंगे। I2P डेटाग्राम कभी भी 65536 से बड़े नहीं होंगे। डेटाग्राम का आकार एप्लिकेशन प्रोटोकॉल पर निर्भर करता है।

यदि SAM क्लाइंट SAM सर्वर के स्थानीय है और सिस्टम बड़े MTU का समर्थन करता है, तो डेटाग्राम स्थानीय रूप से विखंडित नहीं होंगे। हालाँकि, यदि SAM क्लाइंट दूरस्थ है, तो IPv4 डेटाग्राम विखंडित हो जाएंगे और IPv6 डेटाग्राम विफल हो जाएंगे (IPv6 UDP विखंडन का समर्थन नहीं करता है)।

क्लाइंट लाइब्रेरी और एप्लिकेशन डेवलपर्स को इन मुद्दों के बारे में पता होना चाहिए और खंडन से बचने और पैकेट नुकसान को रोकने के लिए अनुशंसाओं को दस्तावेज़ीकृत करना चाहिए, विशेष रूप से दूरस्थ SAM क्लाइंट-सर्वर कनेक्शन पर।

#### डेटाग्राम भेजें, रॉ भेजें (V1/V2 संगत डेटाग्राम हैंडलिंग)

SAM V3 में, डेटाग्राम भेजने का पसंदीदा तरीका ऊपर दस्तावेज़ीकृत बंदरगाह 7655 पर डेटाग्राम सॉकेट के माध्यम से है। हालाँकि, [SAM V1](/docs/api/sam) और [SAM V2](/docs/api/samv2) में दस्तावेज़ीकृत अनुसार DATAGRAM SEND कमांड का उपयोग करके SAM ब्रिज सॉकेट के माध्यम से सीधे उत्तर योग्य डेटाग्राम भेजे जा सकते हैं।

संस्करण 0.9.14 (संस्करण 3.1) से, अज्ञात डेटाग्राम को SAM ब्रिज सॉकेट के माध्यम से सीधे RAW SEND कमांड का उपयोग करके भेजा जा सकता है, जैसा कि [SAM V1](/docs/api/sam) और [SAM V2](/docs/api/samv2) में दस्तावेज़ीकृत है।

रिलीज़ 0.9.24 (संस्करण 3.2) से, DATAGRAM SEND और RAW SEND में डिफ़ॉल्ट पोर्ट्स को ओवरराइड करने के लिए पैरामीटर FROM_PORT=nnnn और/या TO_PORT=nnnn शामिल हो सकते हैं। रिलीज़ 0.9.24 (संस्करण 3.2) से, RAW SEND में डिफ़ॉल्ट प्रोटोकॉल को ओवरराइड करने के लिए पैरामीटर PROTOCOL=nnn शामिल हो सकता है।

ये कमांड ID पैरामीटर को समर्थन नहीं देते हैं। डेटाग्राम उचित रूप से हाल ही में बनाए गए DATAGRAM- या RAW-शैली के सत्र में भेजे जाते हैं। भविष्य में जारी किए जाने पर ID पैरामीटर के लिए समर्थन जोड़ा जा सकता है।

DATAGRAM2 और DATAGRAM3 प्रारूप V1/V2 संगत तरीके से *समर्थित नहीं* हैं।

### SAM प्राथमिक सत्र (V3.3 और उच्चतर)

*संस्करण 3.3 को I2P रिलीज़ 0.9.25 में पेश किया गया था।*

*इस विनिर्देश के एक पूर्व संस्करण में, प्राथमिक (PRIMARY) सत्रों को मास्टर (MASTER) सत्र के रूप में जाना जाता था। दोनों `i2pd` और `I2P+` में, उन्हें अभी भी केवल मास्टर सत्र के रूप में जाना जाता है।*

SAM v3.3 में एक ही प्राथमिक सत्र पर स्ट्रीमिंग, डेटाग्राम और रॉ उप-सत्र चलाने तथा एक ही शैली के कई उप-सत्र चलाने के लिए समर्थन जोड़ा गया है। सभी उप-सत्र ट्रैफ़िक एकल गंतव्य या टनलों के समूह का उपयोग करता है। I2P से ट्रैफ़िक के मार्ग का निर्धारण उप-सत्रों के लिए पोर्ट और प्रोटोकॉल विकल्पों के आधार पर किया जाता है।

मल्टीप्लेक्स्ड सबसेशन बनाने के लिए, आपको एक प्राथमिक सत्र बनाना होगा और फिर प्राथमिक सत्र में सबसेशन जोड़ने होंगे। प्रत्येक सबसेशन का एक अद्वितीय आईडी और एक अद्वितीय लिसन प्रोटोकॉल और पोर्ट होना चाहिए। सबसेशन को प्राथमिक सत्र से हटाया भी जा सकता है।

एक प्राइमरी सत्र और सबसेशन के संयोजन के साथ, एक SAM क्लाइंट एक ही टनल सेट पर कई एप्लिकेशन्स का समर्थन कर सकता है, या विभिन्न प्रोटोकॉल का उपयोग करते हुए एक एकल उन्नत एप्लिकेशन। उदाहरण के लिए, एक बिटटॉरेंट क्लाइंट स्ट्रीमिंग सबसेशन को पीयर-टू-पीयर कनेक्शन के लिए सेट कर सकता है, जिसके साथ DHT संचार के लिए डेटाग्राम और रॉ सबसेशन भी हों।

#### एक प्राथमिक सत्र बनाना

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM ब्रिज सफलता या विफलता के साथ प्रतिक्रिया देगा, जैसा कि [मानक सत्र निर्माण की प्रतिक्रिया में](#session-creation-response)।

प्राथमिक सत्र पर PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL या HEADER विकल्प सेट न करें। आप प्राथमिक सत्र ID या नियंत्रण सॉकेट पर कोई भी डेटा नहीं भेज सकते। स्ट्रीम कनेक्ट, डेटाग्राम भेजें आदि जैसे सभी कमांड एक अलग सॉकेट पर सबसेशन ID का उपयोग करने चाहिए।

प्राथमिक सत्र राउटर से जुड़ता है और टनल बनाता है। जब SAM ब्रिज प्रतिक्रिया देता है, तो टनल बन चुके होते हैं और सत्र सब-सत्रों को जोड़ने के लिए तैयार होता है। लंबाई, मात्रा और उपनाम जैसे टनल पैरामीटर से संबंधित सभी [I2CP](/docs/protocol/i2cp) विकल्प प्राथमिक के SESSION CREATE में प्रदान किए जाने चाहिए।

प्राथमिक सत्र पर सभी उपयोगिता आदेश समर्थित हैं।

जब प्राथमिक सत्र बंद हो जाता है, तो सभी उप-सत्र भी बंद हो जाते हैं।

नोट: संस्करण 0.9.47 से पहले, STYLE=MASTER का उपयोग करें। संस्करण 0.9.47 से STYLE=PRIMARY को समर्थन प्राप्त है। पुरानी संगतता के लिए MASTER को अभी भी समर्थन प्राप्त है।

#### एक सबसेशन बनाना

जिस नियंत्रण सॉकेट का उपयोग प्राथमिक सत्र बनाने के लिए किया गया था, उसी का उपयोग करना:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM ब्रिज सफलता या विफलता के साथ प्रतिक्रिया देगा, जैसा कि [मानक सत्र निर्माण के प्रति प्रतिक्रिया](#session-creation-response) में है। चूंकि टनल पहले से ही प्राथमिक सत्र निर्माण में बना दिए गए थे, SAM ब्रिज तुरंत प्रतिक्रिया देना चाहिए।

SESSION ADD पर DESTINATION विकल्प सेट न करें। सबसेशन प्राथमिक सेशन में निर्दिष्ट गंतव्य का उपयोग करेगा। सभी सबसेशन को नियंत्रण सॉकेट पर जोड़ा जाना चाहिए, अर्थात उसी कनेक्शन पर जिस पर आपने प्राथमिक सेशन बनाया था।

एकाधिक सबसेशन में पर्याप्त रूप से अद्वितीय विकल्प होने चाहिए ताकि आने वाले डेटा को सही ढंग से रूट किया जा सके। विशेष रूप से, एक ही शैली के एकाधिक सत्रों में अलग-अलग LISTEN_PORT विकल्प होने चाहिए (और/या केवल RAW के लिए LISTEN_PROTOCOL)। ऐसे लिसन पोर्ट और प्रोटोकॉल के साथ SESSION ADD करने पर जो किसी मौजूदा सबसेशन को दोहराता है, त्रुटि होगी।

LISTEN_PORT स्थानीय I2P पोर्ट है, अर्थात आने वाले डेटा के लिए प्राप्त (TO) पोर्ट। यदि LISTEN_PORT निर्दिष्ट नहीं किया गया है, तो FROM_PORT मान का उपयोग किया जाएगा। यदि LISTEN_PORT और FROM_PORT दोनों निर्दिष्ट नहीं हैं, तो आने वाले मार्ग को केवल STYLE और PROTOCOL के आधार पर किया जाएगा। LISTEN_PORT और LISTEN_PROTOCOL के लिए, 0 का अर्थ है कोई भी मान, अर्थात एक वाइल्डकार्ड। यदि LISTEN_PORT और LISTEN_PROTOCOL दोनों 0 हैं, तो यह सबसेशन उस आने वाले ट्रैफ़िक के लिए डिफ़ॉल्ट होगा जिसे किसी अन्य सबसेशन पर मार्ग के रूप में नहीं भेजा जाता है। आने वाला स्ट्रीमिंग ट्रैफ़िक (प्रोटोकॉल 6) को कभी भी RAW सबसेशन पर मार्ग के रूप में नहीं भेजा जाएगा, भले ही उसका LISTEN_PROTOCOL 0 हो। एक RAW सबसेशन LISTEN_PROTOCOL के रूप में 6 नहीं सेट कर सकता है। यदि आने वाले ट्रैफ़िक के प्रोटोकॉल और पोर्ट के मेल खाने वाला कोई डिफ़ॉल्ट या सबसेशन नहीं है, तो उस डेटा को छोड़ दिया जाएगा।

डेटा भेजने और प्राप्त करने के लिए प्राथमिक सत्र ID के बजाय सबसेशन ID का उपयोग करें। स्ट्रीम कनेक्ट (STREAM CONNECT), डेटाग्राम भेजें (DATAGRAM SEND) आदि जैसे सभी कमांड सबसेशन ID का उपयोग करने चाहिए।

एक प्राथमिक सत्र या उप-सत्र पर सभी उपयोगिता आदेश समर्थित हैं। प्राथमिक सत्र या उप-सत्र पर v1/v2 डेटाग्राम/कच्चा भेजना/प्राप्त करना समर्थित नहीं है।

#### एक सबसेशन को रोकना

जिस नियंत्रण सॉकेट का उपयोग प्राथमिक सत्र बनाने के लिए किया गया था, उसी का उपयोग करना:

```
->  SESSION REMOVE
          ID=$nickname
```
यह प्राथमिक सत्र से एक सबसेशन को हटा देता है। SESSION REMOVE पर कोई अन्य विकल्प सेट न करें। सबसेशन को नियंत्रण सॉकेट पर हटाया जाना चाहिए, अर्थात उसी कनेक्शन पर जिस पर आपने प्राथमिक सत्र बनाया था। एक बार सबसेशन हटाए जाने के बाद, इसे बंद कर दिया जाता है और डेटा भेजने या प्राप्त करने के लिए इसका उपयोग नहीं किया जा सकता है।

SAM ब्रिज सफलता या विफलता के साथ प्रतिक्रिया देगा, जैसा कि [मानक सत्र निर्माण की प्रतिक्रिया में](#session-creation-response)।

### SAM उपयोगिता कमांड

कुछ उपयोगिता कमांड्स के लिए पहले से मौजूद सत्र की आवश्यकता होती है और कुछ के लिए नहीं। नीचे विवरण देखें।

#### होस्ट नाम लुकअप

ग्राहक द्वारा नाम संकल्प के लिए SAM ब्रिज के लिए निम्नलिखित संदेश का उपयोग किया जा सकता है:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
जिसका उत्तर दिया जाता है

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
परिणाम मान निम्नलिखित में से एक हो सकता है:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
यदि NAME=ME है, तो उत्तर में वर्तमान सत्र द्वारा उपयोग किया गया गंतव्य शामिल होगा (यदि आप एक TRANSIENT का उपयोग कर रहे हैं तो यह उपयोगी है)। यदि $result OK नहीं है, तो MESSAGE में "बुरा प्रारूप" आदि जैसा वर्णनात्मक संदेश हो सकता है। INVALID_KEY का अर्थ है कि अनुरोध में $name के साथ कुछ गलत है, संभवतः अमान्य अक्षर हैं।

$destination [Destination](/docs/specs/common-structures#type_Destination) का बेस 64 है, जिसमें हस्ताक्षर प्रकार के आधार पर 516 या अधिक बेस 64 अक्षर (बाइनरी में 387 या अधिक बाइट्स) होते हैं।

नामकरण लुकअप के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो। हालाँकि, कुछ लागू करणों में, .b32.i2p लुकअप जो कैशित नहीं है और जिसके लिए नेटवर्क क्वेरी की आवश्यकता होती है, विफल हो सकता है, क्योंकि लुकअप के लिए कोई क्लाइंट टनल उपलब्ध नहीं होते हैं।

#### नाम लुकअप विकल्प

राउटर एपीआई 0.9.66 से NAMING LOOKUP को सेवा लुकअप के लिए समर्थन के साथ बढ़ाया गया है। समर्थन कार्यान्वयन के अनुसार भिन्न हो सकता है। अतिरिक्त जानकारी के लिए प्रस्ताव 167 देखें।

NAMING LOOKUP NAME=example.i2p OPTIONS=true प्रतिक्रिया में विकल्प मैपिंग का अनुरोध करता है। OPTIONS=true होने पर NAME पूर्ण base64 गंतव्य हो सकता है।

यदि गंतव्य लुकअप सफल रहा और लीजसेट में विकल्प मौजूद थे, तो उत्तर में गंतव्य के बाद, OPTION:key=value के रूप में एक या अधिक विकल्प होंगे। प्रत्येक विकल्प में अलग OPTION: उपसर्ग होगा। सभी लीजसेट विकल्पों को शामिल किया जाएगा, केवल सेवा रिकॉर्ड विकल्पों को नहीं। उदाहरण के लिए, भविष्य में परिभाषित पैरामीटर के लिए विकल्प मौजूद हो सकते हैं। उदाहरण:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

जिन कुंजियों में '=', होता है और जिन कुंजियों या मानों में नई पंक्ति होती है, उन्हें अमान्य माना जाता है और कुंजी/मान युग्म को उत्तर से हटा दिया जाएगा। यदि लीजसेट में कोई विकल्प नहीं मिलते हैं, या यदि लीजसेट संस्करण 1 था, तो प्रतिक्रिया में कोई विकल्प शामिल नहीं किया जाएगा। यदि लुकअप में OPTIONS=true था, और लीजसेट नहीं मिला, तो एक नया परिणाम मान LEASESET_NOT_FOUND वापस किया जाएगा।

#### गंतव्य कुंजी उत्पादन

निम्नलिखित संदेश का उपयोग करके सार्वजनिक और निजी बेस64 कुंजियाँ उत्पन्न की जा सकती हैं:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
जिसका उत्तर दिया जाता है

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
संस्करण 3.1 (I2P 0.9.14) से, एक वैकल्पिक पैरामीटर SIGNATURE_TYPE समर्थित है। SIGNATURE_TYPE का मान कोई भी नाम (जैसे ECDSA_SHA256_P256, केस असंवेदनशील) या संख्या (जैसे 1) हो सकता है जो [की प्रमाणपत्रों](/docs/specs/common-structures#type_Certificate) द्वारा समर्थित हो। डिफ़ॉल्ट DSA_SHA1 है, जो आपकी आवश्यकता नहीं है। अधिकांश अनुप्रयोगों के लिए, कृपया SIGNATURE_TYPE=7 निर्दिष्ट करें।

$destination [Destination](/docs/specs/common-structures#type_Destination) का बेस 64 है, जिसमें हस्ताक्षर प्रकार के आधार पर 516 या अधिक बेस 64 अक्षर (बाइनरी में 387 या अधिक बाइट्स) होते हैं।

$privkey उस संयोजन का बेस 64 है जिसमें [डेस्टिनेशन](/docs/specs/common-structures#type_Destination) के बाद [प्राइवेट की](/docs/specs/common-structures#type_PrivateKey) और फिर [साइनिंग प्राइवेट की](/docs/specs/common-structures#type_SigningPrivateKey) शामिल है, जिसकी लंबाई 884 या अधिक बेस 64 अक्षर (बाइनरी में 663 या अधिक बाइट्स) होती है, जो साइनेचर प्रकार पर निर्भर करता है। बाइनरी प्रारूप को प्राइवेट की फाइल में निर्दिष्ट किया गया है।

256-बाइट बाइनरी [निजी कुंजी](/docs/specs/common-structures#type_PrivateKey) के बारे में टिप्पणियाँ: यह फ़ील्ड संस्करण 0.6 (2005) के बाद से अप्रयुक्त है। SAM कार्यान्वयन इस फ़ील्ड में यादृच्छिक डेटा या सभी शून्य भेज सकते हैं; बेस 64 में AAAA की श्रृंखला के बारे में चिंतित न हों। अधिकांश अनुप्रयोग बेस 64 स्ट्रिंग को सीधे संग्रहीत करेंगे और उसे SESSION CREATE में जैसा-का-ताई वापस कर देंगे, या संग्रहण के लिए बाइनरी में डिकोड करेंगे और फिर SESSION CREATE के लिए पुनः एन्कोड करेंगे। हालाँकि, अनुप्रयोग बेस 64 को डिकोड कर सकते हैं, PrivateKeyFile विनिर्देश के अनुसार बाइनरी को पार्स कर सकते हैं, 256-बाइट निजी कुंजी भाग को त्याग सकते हैं, और फिर SESSION CREATE के लिए पुनः एन्कोड करते समय इसे 256 बाइट यादृच्छिक डेटा या सभी शून्य के साथ प्रतिस्थापित कर सकते हैं। PrivateKeyFile विनिर्देश में सभी अन्य फ़ील्ड्स को संरक्षित रखना चाहिए। इससे फ़ाइल प्रणाली भंडारण में 256 बाइट की बचत होगी, लेकिन अधिकांश अनुप्रयोगों के लिए यह प्रयास के लायक नहीं हो सकता है। अतिरिक्त जानकारी और पृष्ठभूमि के लिए प्रस्ताव 161 देखें।

DEST GENERATE के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो।

ऑफ़लाइन हस्ताक्षरों के साथ गंतव्य बनाने के लिए DEST GENERATE का उपयोग नहीं किया जा सकता है।

#### PING/PONG (SAM 3.2 या उच्चतर)

ग्राहक या सर्वर में से कोई भी भेज सकता है:

```
PING[ arbitrary text]
```
नियंत्रण पोर्ट पर, निम्न प्रतिक्रिया के साथ:

```
PONG[ arbitrary text from the ping]
```
नियंत्रण सॉकेट कीपएलाइव के लिए उपयोग किया जाएगा। कोई भी पक्ष सत्र और सॉकेट को बंद कर सकता है यदि उचित समय में कोई प्रतिक्रिया प्राप्त नहीं होती है, जो लागूकरण पर निर्भर करता है।

यदि क्लाइंट से PONG की प्रतीक्षा करते समय टाइमआउट होता है, तो ब्रिज भेज सकता है:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
और फिर डिस्कनेक्ट करें।

यदि ब्रिज से PONG की प्रतीक्षा करते समय टाइमआउट होता है, तो क्लाइंट बस डिस्कनेक्ट हो सकता है।

पिंग/पॉन्ग के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो।

#### QUIT/STOP/EXIT (SAM 3.2 या उच्चतर, वैकल्पिक सुविधाएँ)

कमांड QUIT, STOP और EXIT सत्र और सॉकेट को बंद कर देंगे। इसका कार्यान्वयन वैकल्पिक है, ताकि telnet के माध्यम से परीक्षण करने में आसानी हो। सॉकेट बंद होने से पहले कोई प्रतिक्रिया है या नहीं (उदाहरण के लिए, एक SESSION STATUS संदेश) यह कार्यान्वयन-विशिष्ट है और इस विनिर्देश के दायरे से बाहर है।

QUIT/STOP/EXIT के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो।

#### सहायता (वैकल्पिक सुविधा)

सर्वर HELP कमांड लागू कर सकते हैं। टेलनेट के माध्यम से परीक्षण को सरल बनाने के लिए यह लागू करना वैकल्पिक है। आउटपुट प्रारूप और आउटपुट के अंत का पता लगाना लागूकरण-विशिष्ट होता है और इस विनिर्देश के दायरे से बाहर है।

HELP के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो।

#### प्राधिकरण विन्यास (SAM 3.2 या उच्चतर, वैकल्पिक सुविधा)

AUTH कमांड का उपयोग करके प्राधिकरण विन्यास। एक SAM सर्वर प्रमाणपत्रों के स्थायी भंडारण को सुविधाजनक बनाने के लिए इन कमांडों को लागू कर सकता है। इन कमांडों के अलावा प्रमाणीकरण का विन्यास लागूकरण-विशिष्ट है और इस विनिर्देश के दायरे से बाहर है।

- AUTH ENABLE अगले कनेक्शन पर प्राधिकरण सक्षम करता है
- AUTH DISABLE अगले कनेक्शन पर प्राधिकरण अक्षम करता है
- AUTH ADD USER="foo" PASSWORD="bar" एक उपयोक्ता/पासवर्ड जोड़ता है
- AUTH REMOVE USER="foo" इस उपयोक्ता को हटाता है

उपयोगकर्ता और पासवर्ड के लिए डबल कोट्स की अनुशंसा की जाती है, लेकिन आवश्यक नहीं है। उपयोगकर्ता या पासवर्ड के अंदर आने वाले डबल कोट्स को बैकस्लैश के साथ एस्केप किया जाना चाहिए। विफलता की स्थिति में सर्वर I2P_ERROR और एक संदेश के साथ प्रतिक्रिया देगा।

AUTH के लिए आवश्यक नहीं है कि पहले एक सत्र बनाया गया हो।

### परिणाम मान

ये वे मान हैं जिन्हें RESULT फ़ील्ड द्वारा उनके अर्थ के साथ ले जाया जा सकता है:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
विभिन्न लागूकरण विभिन्न परिदृश्यों में कौन सा परिणाम (RESULT) लौटाया जाता है, इसमें सुसंगत नहीं हो सकते हैं।

OK के अलावा, परिणाम (RESULT) के साथ अधिकांश प्रतिक्रियाओं में अतिरिक्त जानकारी के साथ एक संदेश (MESSAGE) भी शामिल होगा। समस्याओं को डिबग करने में संदेश आम तौर पर सहायक होगा। हालांकि, संदेश स्ट्रिंग्स लागू करने पर निर्भर करते हैं, वर्तमान स्थानीयकरण में SAM सर्वर द्वारा अनुवादित हो सकते हैं या नहीं भी हो सकते हैं, अपवाद जैसी आंतरिक कार्यान्वयन-विशिष्ट जानकारी शामिल हो सकती है, और बिना सूचना के बदले जा सकते हैं। जबकि SAM क्लाइंट उपयोगकर्ताओं को संदेश स्ट्रिंग्स उजागर करना चुन सकते हैं, उन्हें उन स्ट्रिंग्स पर आधारित कार्यक्रम निर्णय नहीं लेने चाहिए, क्योंकि यह नाजुक होगा।

### टनल, I2CP और स्ट्रीमिंग विकल्प

इन विकल्पों को SAM SESSION CREATE लाइन में name=value जोड़े के रूप में पारित किया जा सकता है।

सभी सत्रों में [I2CP विकल्प जैसे टनल की लंबाई और मात्रा](/docs/protocol/i2cp#options) शामिल हो सकते हैं। STREAM सत्रों में [स्ट्रीमिंग लाइब्रेरी विकल्प](/docs/api/streaming#options) शामिल हो सकते हैं।

विकल्प नामों और डिफ़ॉल्ट के लिए उन संदर्भों को देखें। संदर्भित प्रलेखन जावा राउटर लागू करने के लिए है। डिफ़ॉल्ट परिवर्तन के अधीन हैं। विकल्प नाम और मान केस-संवेदनशील होते हैं। अन्य राउटर लागू करने वाले सभी विकल्पों का समर्थन नहीं कर सकते हैं और भिन्न डिफ़ॉल्ट हो सकते हैं; विवरण के लिए राउटर प्रलेखन देखें।

### बेस 64 नोट्स

बेस 64 एन्कोडिंग के लिए I2P मानक बेस 64 वर्णमाला "A-Z, a-z, 0-9, -, ~" का उपयोग करना चाहिए।

### डिफ़ॉल्ट SAM सेटअप

डिफ़ॉल्ट SAM पोर्ट 7656 है। जावा I2P राउटर में डिफ़ॉल्ट रूप से SAM सक्षम नहीं होता है; इसे राउटर कंसोल के कॉन्फ़िगर क्लाइंट्स पृष्ठ पर या clients.config फ़ाइल में मैन्युअल रूप से शुरू करना होगा, या स्वचालित रूप से शुरू होने के लिए कॉन्फ़िगर करना होगा। डिफ़ॉल्ट SAM UDP पोर्ट 7655 है, जो 127.0.0.1 पर सुनता है। जावा राउटर में इन्हें पॉकेट में sam.udp.port=nnnnn और/या sam.udp.host=w.x.y.z तर्क जोड़कर बदला जा सकता है, या SESSION लाइन पर।

अन्य राउटरों में विन्यास लागूकरण-विशिष्ट होता है। [यहाँ i2pd विन्यास गाइड देखें](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/)।
