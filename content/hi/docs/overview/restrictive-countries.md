---
title: "सख्त/प्रतिबंधित देश"
description: "जिन क्षेत्राधिकारों में routing या anonymity tools पर प्रतिबंध हैं वहां I2P कैसे व्यवहार करता है (Hidden Mode और strict list)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: दस्तावेज़
reviewStatus: "needs-review"
---

I2P का यह कार्यान्वयन (इस साइट पर वितरित Java कार्यान्वयन) में एक "Strict Countries List" शामिल है जिसका उपयोग उन क्षेत्रों में router व्यवहार को समायोजित करने के लिए किया जाता है जहां दूसरों के लिए routing में भाग लेना कानून द्वारा प्रतिबंधित हो सकता है। हालांकि हमें ऐसे किसी क्षेत्राधिकार की जानकारी नहीं है जो I2P का उपयोग करने पर रोक लगाता हो, कई देशों में ट्रैफिक relay करने पर व्यापक प्रतिबंध हैं। जो routers "strict" देशों में स्थित प्रतीत होते हैं, उन्हें स्वचालित रूप से Hidden mode में रखा जाता है।

यह प्रोजेक्ट इन निर्णयों को लेते समय नागरिक और डिजिटल अधिकार संगठनों के शोध का संदर्भ लेता है। विशेष रूप से, Freedom House द्वारा किया जा रहा शोध हमारे चुनावों को सूचित करता है। सामान्य मार्गदर्शन यह है कि उन देशों को शामिल किया जाए जिनका Civil Liberties (CL) स्कोर 16 या उससे कम है, या Internet Freedom स्कोर 39 या उससे कम है (मुक्त नहीं)।

## हिडन मोड सारांश

जब एक router को Hidden मोड में रखा जाता है, तो इसके व्यवहार में तीन मुख्य बातें बदलती हैं:

- यह netDb में RouterInfo प्रकाशित नहीं करता है।
- यह भाग लेने वाली tunnels को स्वीकार नहीं करता है।
- यह उसी देश के routers से सीधे कनेक्शन को अस्वीकार करता है।

ये सुरक्षा उपाय राउटर्स को विश्वसनीय तरीके से गिनना अधिक कठिन बना देते हैं, और दूसरों के लिए ट्रैफिक रिले करने पर स्थानीय प्रतिबंधों के उल्लंघन के जोखिम को कम करते हैं।

## सख्त देशों की सूची (2024 तक)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
यदि आपको लगता है कि किसी देश को strict list में जोड़ा जाना चाहिए या हटाया जाना चाहिए, तो कृपया एक issue खोलें: https://i2pgit.org/i2p/i2p.i2p/

संदर्भ: Freedom House – https://freedomhouse.org/
