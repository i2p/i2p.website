---
title: "नए I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "कई नए I2P router के कार्यान्वयन उभर रहे हैं, जिनमें Rust में emissary और Go में go-i2p शामिल हैं, जो एम्बेडिंग (अंतर्निवेशन) और नेटवर्क विविधता के लिए नई संभावनाएँ ला रहे हैं।"
---

I2P विकास के लिए यह एक रोमांचक समय है, हमारा समुदाय बढ़ रहा है और अब कई नए, पूर्णतः कार्यात्मक I2P router प्रोटोटाइप उभर रहे हैं! हम इस विकास के बारे में और आपके साथ यह समाचार साझा करने के लिए बेहद उत्साहित हैं।

## यह नेटवर्क की मदद कैसे करता है?

I2P routers विकसित करना हमें यह साबित करने में मदद करता है कि हमारी विशिष्टताओं के दस्तावेज़ों का उपयोग नए I2P routers बनाने के लिए किया जा सकता है, कोड को नए विश्लेषण उपकरणों के लिए खोलता है, और समग्र रूप से नेटवर्क की सुरक्षा और अंतरसंचालनीयता में सुधार करता है। कई I2P routers होने का मतलब है कि संभावित बग एक जैसे नहीं होते; एक router पर किया गया हमला दूसरे router पर काम न करे, जिससे मोनोकल्चर समस्या से बचाव होता है। हालाँकि, दीर्घकाल में सबसे रोमांचक संभावना शायद embedding (किसी सिस्टम/डिवाइस में अंत:स्थापन) है।

## एम्बेडिंग क्या है?

I2P के संदर्भ में, embedding (एप्लिकेशन के भीतर समाहित करना) ऐसा तरीका है जिसमें एक I2P router को सीधे किसी दूसरी ऐप में शामिल किया जाता है, बिना पृष्ठभूमि में चल रहे किसी स्वतंत्र router की आवश्यकता के। यह I2P को उपयोग में सरल बनाने का एक तरीका है, जिससे सॉफ़्टवेयर को अधिक सुलभ बनाकर नेटवर्क का विस्तार करना आसान हो जाता है। Java और C++ दोनों अपनी-अपनी इकोसिस्टम के बाहर उपयोग में कठिन होने की समस्या से जूझते हैं; C++ के मामले में नाज़ुक, हाथ से लिखी हुई C bindings की आवश्यकता पड़ती है, और Java के मामले में non-JVM एप्लिकेशन से JVM एप्लिकेशन तक संचार करना कष्टदायक होता है।

हालाँकि कई मायनों में यह स्थिति काफी सामान्य है, मेरा मानना है कि I2P को अधिक सुलभ बनाने के लिए इसे सुधारा जा सकता है। अन्य भाषाओं में इन समस्याओं के लिए अधिक सुरुचिपूर्ण समाधान मौजूद हैं। बेशक, हमें Java और C++ routers के लिए मौजूद दिशानिर्देशों पर हमेशा विचार करना चाहिए और उनका उपयोग करना चाहिए।

## दूत अंधकार से प्रकट होता है

हमारी टीम से पूरी तरह स्वतंत्र रूप से, altonen नाम के एक डेवलपर ने Rust में I2P का एक कार्यान्वयन, emissary, विकसित किया है। हालाँकि यह अभी काफ़ी नया है, और Rust से हम परिचित नहीं हैं, यह रोचक प्रोजेक्ट बहुत संभावनाएँ रखता है। emissary बनाने के लिए altonen को बधाई, हम काफ़ी प्रभावित हैं।

### Why Rust?

Rust का उपयोग करने का मुख्य कारण मूलतः वही है जो Java या Go का उपयोग करने का कारण है। Rust एक कम्पाइल्ड प्रोग्रामिंग भाषा है, जिसमें मेमोरी प्रबंधन है और एक विशाल, अत्यंत उत्साही समुदाय है। Rust C प्रोग्रामिंग भाषा के लिए bindings (इंटरफ़ेस जोड़) बनाने हेतु उन्नत सुविधाएँ भी प्रदान करता है, जिन्हें अन्य भाषाओं की तुलना में बनाए रखना अधिक आसान हो सकता है, और साथ ही Rust की सशक्त मेमोरी-सुरक्षा विशेषताओं का लाभ बनाए रखता है।

### Do you want to get involved with emissary?

emissary का विकास Github पर altonen द्वारा किया जाता है। आप रिपॉजिटरी यहाँ पा सकते हैं: [altonen/emissary](https://github.com/altonen/emissary)। Rust में भी लोकप्रिय Rust नेटवर्किंग टूल्स के साथ संगत, व्यापक SAMv3 क्लाइंट लाइब्रेरियों की कमी है; SAMv3 लाइब्रेरी लिखना शुरुआत करने का एक बढ़िया तरीका है।

## go-i2p is getting closer to completion

लगभग 3 वर्षों से मैं go-i2p पर काम कर रहा हूँ, एक शुरुआती लाइब्रेरी को pure-Go में पूर्ण विकसित I2P router में बदलने की कोशिश कर रहा हूँ। पिछले लगभग 6 महीनों में, प्रदर्शन, विश्वसनीयता, और अनुरक्षणीयता में सुधार के लिए इसे बड़े पैमाने पर पुनर्संरचित किया गया है।

### Why Go?

हालाँकि Rust और Go में कई समान लाभ हैं, कई मायनों में Go सीखना कहीं अधिक सरल है। वर्षों से, Go प्रोग्रामिंग भाषा में I2P के उपयोग के लिए उत्कृष्ट लाइब्रेरियाँ और एप्लिकेशन उपलब्ध रहे हैं, जिनमें SAMv3.3 लाइब्रेरियों के सबसे पूर्ण कार्यान्वयन शामिल हैं। लेकिन ऐसा I2P router जिसे हम स्वतः प्रबंधित कर सकें(जैसे कि एक एंबेडेड router), उसके बिना यह उपयोगकर्ताओं के लिए अब भी एक बाधा बना रहता है। go-i2p का उद्देश्य उस अंतर को पाटना है, और Go में काम कर रहे I2P एप्लिकेशन डेवलपर्स के लिए सभी पेचीदगियों को दूर करना है।

### Rust क्यों?

go-i2p का विकास Github पर किया जाता है, इस समय मुख्य रूप से eyedeekay द्वारा, और [go-i2p](https://github.com/go-i2p/) पर समुदाय से योगदान के लिए खुला है। इस namespace (नेमस्पेस) के अंतर्गत कई परियोजनाएँ मौजूद हैं, जैसे:

#### Router Libraries

हमने ये लाइब्रेरीज़ अपनी I2P router लाइब्रेरीज़ बनाने के लिए विकसित की हैं। समीक्षा को आसान बनाने और उन्हें उन अन्य लोगों के लिए उपयोगी बनाने के लिए, जो प्रयोगात्मक, कस्टम I2P routers बनाना चाहते हैं, इन्हें कई केंद्रित रिपॉज़िटरीज़ में विभाजित किया गया है।

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

खैर, यदि आप XBox पर I2P चलाना चाहते हैं, तो [I2P router in C#](https://github.com/PeterZander/i2p-cs) लिखने का एक निष्क्रिय प्रोजेक्ट है। वास्तव में यह काफ़ी बढ़िया लगता है। यदि वह भी आपकी पसंद नहीं है, तो आप जैसा altonen ने किया, वैसा करके एक बिल्कुल नया विकसित कर सकते हैं।

### क्या आप emissary में शामिल होना चाहते हैं?

आप किसी भी कारण से I2P router लिख सकते हैं—यह एक मुक्त नेटवर्क है—लेकिन आप यह क्यों करना चाहते हैं, यह जानना आपके लिए मददगार होगा। क्या कोई समुदाय है जिसे आप सशक्त बनाना चाहते हैं, कोई टूल जो आपको I2P के लिए उपयुक्त लगता है, या कोई रणनीति जिसे आप आज़माना चाहते हैं? यह तय करें कि आपका लक्ष्य क्या है ताकि आपको पता चले कि शुरुआत कहाँ से करनी है, और "पूर्ण" अवस्था कैसी दिखेगी।

### Decide what language you want to do it in and why

यहाँ कुछ कारण हैं जिनकी वजह से आप किसी भाषा का चयन कर सकते हैं:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

लेकिन यहाँ कुछ कारण दिए गए हैं जिनके चलते आप उन भाषाओं को नहीं चुनना चाहेंगे:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

सैकड़ों प्रोग्रामिंग भाषाएँ हैं और हम उन सभी में नियमित रूप से अनुरक्षित I2P लाइब्रेरीज़ और routers का स्वागत करते हैं। अपने विकल्पों के बीच समझदारी से संतुलन तय करें और शुरू करें।

## go-i2p पूरा होने के और करीब पहुँच रहा है

चाहे आप Rust, Go, Java, C++ या किसी अन्य भाषा में काम करना चाहते हों, Irc2P पर #i2p-dev से संपर्क करें। वहीं से शुरुआत करें, और हम आपको router-विशिष्ट चैनलों पर शामिल करा देंगे। हम ramble.i2p के f/i2p पर, reddit के r/i2p पर, और GitHub तथा git.idk.i2p पर भी मौजूद हैं। हम आपसे जल्द सुनने की प्रतीक्षा कर रहे हैं।
