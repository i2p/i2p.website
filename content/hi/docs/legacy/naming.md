---
title: "नामकरण पर चर्चा"
description: "I2P के नामकरण मॉडल पर ऐतिहासिक बहस और यह कि वैश्विक DNS (डोमेन नेम सिस्टम)-शैली की प्रणालियों को क्यों अस्वीकार किया गया"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **संदर्भ:** यह पृष्ठ I2P के प्रारम्भिक डिज़ाइन युग की दीर्घकालिक बहसों का संग्रह है। यह बताता है कि परियोजना ने DNS-शैली लुकअप या बहुमत-मत रजिस्ट्रियों की तुलना में स्थानीय रूप से विश्वसनीय पता पुस्तिकाओं को क्यों प्राथमिकता दी। वर्तमान उपयोग संबंधी मार्गदर्शन के लिए, [नामकरण दस्तावेज़ीकरण](/docs/overview/naming/) देखें।

## त्यागे गए विकल्प

I2P के सुरक्षा उद्देश्यों के चलते पारंपरिक नामकरण योजनाएँ संभव नहीं हैं:

- **DNS-शैली का रिज़ॉल्यूशन.** लुकअप पथ पर कोई भी resolver (नाम-सुलझाने वाला सर्वर) जवाबों को स्पूफ कर सकता है या सेंसर कर सकता है। DNSSEC होने पर भी, समझौता किए गए registrars (डोमेन पंजीकरण प्रदाता) या certificate authorities (प्रमाणपत्र प्राधिकरण) अब भी एक single point of failure (एकल विफलता बिंदु) बने रहते हैं। I2P में, destinations *ही* public keys (सार्वजनिक कुंजियाँ) होते हैं—किसी लुकअप का हाइजैक पूरी तरह पहचान से समझौता कर देगा।
- **वोटिंग-आधारित नेमिंग.** कोई हमलावर असीमित पहचानें गढ़ सकता है (Sybil attack — सिबिल हमला) और लोकप्रिय नामों के लिए वोट “जीत” सकता है। Proof-of-work (कार्य का प्रमाण) आधारित उपाय लागत बढ़ाते हैं, लेकिन भारी समन्वय बोझ भी ले आते हैं।

इसके बजाय, I2P जानबूझकर नामकरण को ट्रांसपोर्ट लेयर के ऊपर रखता है। बंडल की गई नामकरण लाइब्रेरी एक service-provider interface (सेवा-प्रदाता इंटरफेस) प्रदान करती है ताकि वैकल्पिक योजनाएँ सह-अस्तित्व में रह सकें—उपयोगकर्ता तय करते हैं कि वे किन पता पुस्तिकाओं या जंप सेवाओं पर भरोसा करते हैं।

## स्थानीय बनाम वैश्विक नाम (jrandom, 2005)

- I2P में नाम **स्थानीय रूप से अद्वितीय, पर मानव-पठनीय** होते हैं। आपका `boss.i2p` किसी और के `boss.i2p` से मेल न भी खाए, और यह डिज़ाइन के अनुसार है।
- यदि कोई दुर्भावनापूर्ण हमलावर आपको किसी नाम के पीछे का destination (I2P का 'Destination', यानी सार्वजनिक-कुंजी-आधारित पता) बदलने के लिए बहला दे, तो वह प्रभावी रूप से किसी सेवा को हाइजैक कर देगा। वैश्विक अद्वितीयता से इंकार करना उस तरह के हमले को रोकता है।
- नामों को बुकमार्क या IM उपनामों की तरह समझें—आप किन destinations पर भरोसा करते हैं, यह विशिष्ट पता-पुस्तिकाओं की सदस्यता लेकर या कुंजियाँ मैन्युअल रूप से जोड़कर तय करते हैं।

## सामान्य आपत्तियाँ और उत्तर (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## दक्षता संबंधी विचारों पर चर्चा

- क्रमिक अद्यतन प्रदान करें (केवल वे destinations (I2P पते/पहचान) जो पिछली बार प्राप्ति के बाद जोड़े गए हों).
- पूर्ण hosts फ़ाइलों के साथ-साथ पूरक फ़ीड्स (`recenthosts.cgi`) उपलब्ध कराएं.
- स्क्रिप्टेबल टूलिंग (उदाहरण के लिए, `i2host.i2p`) का अन्वेषण करें ताकि फ़ीडों को एकीकृत किया जा सके या विश्वास स्तरों के आधार पर फ़िल्टर किया जा सके.

## मुख्य निष्कर्ष

- सुरक्षा को वैश्विक सहमति पर वरीयता दी जाती है: स्थानीय रूप से संजोई गई पता-पुस्तिकाएँ हाइजैकिंग के जोखिम को कम करती हैं।
- कई नामकरण पद्धतियाँ naming API (नामकरण हेतु एप्लिकेशन प्रोग्रामिंग इंटरफ़ेस) के माध्यम से सह-अस्तित्व में रह सकती हैं—किस पर भरोसा करना है, यह उपयोगकर्ता तय करते हैं।
- पूर्णतः विकेन्द्रीकृत वैश्विक नामकरण अभी भी एक खुली शोध समस्या बना हुआ है; सुरक्षा, मानवीय स्मरण-योग्यता और वैश्विक अद्वितीयता के बीच होने वाले समझौते अब भी [Zooko’s triangle](https://zooko.com/distnames.html) का प्रतिबिंब हैं।

## संदर्भ

- [नामकरण प्रलेखन](/docs/overview/naming/)
- [ज़ूको का “नाम: विकेन्द्रीकृत, सुरक्षित, मानव-अर्थपूर्ण: दो चुनें”](https://zooko.com/distnames.html)
- उदाहरण क्रमिक फ़ीड: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
