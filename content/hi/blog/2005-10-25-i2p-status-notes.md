---
title: "2005-10-25 के लिए I2P स्थिति नोट्स"
date: 2005-10-25
author: "jr"
description: "Weekly update covering network growth to 400-500 peers, Fortuna PRNG integration, GCJ native compilation support, i2psnark lightweight torrent client, and tunnel bootstrap attack analysis"
categories: ["status"]
---

नमस्कार दोस्तों, मोर्चे से कुछ और खबरें

* Index

1) नेटवर्क स्थिति 2) Fortuna एकीकरण 3) GCJ स्थिति 4) i2psnark की वापसी 5) bootstrapping (प्रारंभिक सेटअप) पर अधिक 6) वायरस जांच 7) ???

* 1) Net status

पिछला सप्ताह नेटवर्क पर काफ़ी अच्छा रहा — चीज़ें काफ़ी स्थिर लग रही हैं, थ्रूपुट सामान्य है, और नेटवर्क 400–500 पीयर के दायरे में बढ़ता जा रहा है। 0.6.1.3 रिलीज़ के बाद से कुछ महत्वपूर्ण सुधार भी हुए हैं, और चूँकि वे प्रदर्शन और विश्वसनीयता को प्रभावित करते हैं, मुझे उम्मीद है कि इस सप्ताह के आगे चलकर हम 0.6.1.4 रिलीज़ करेंगे।

* 2) Fortuna integration

Thanks to Casey Marshall's quick fix [1], we've been able to integrate GNU-Crypto's Fortuna [2] pseduorandom number generator. This removes the cause of much frustration with the blackdown JVM, and lets us work smoothly with GCJ. Integrating Fortuna into I2P was one of the main reasons smeghead developed "pants" (an 'ant' based 'portage'), so we've now had another successful pants usage :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

जैसा कि सूची [3] में उल्लेख किया गया है, अब हम GCJ [4] के साथ router और अधिकांश क्लाइंट को बिना किसी रुकावट के चला सकते हैं। वेब कंसोल स्वयं अभी पूरी तरह काम नहीं कर रहा है, इसलिए आपको router.config के साथ अपना router कॉन्फ़िगरेशन स्वयं करना होगा (हालाँकि इसे लगभग एक मिनट में "Just Work" करना चाहिए और आपके tunnels शुरू कर देने चाहिए)। मुझे पूरी तरह यक़ीन नहीं है कि GCJ हमारी रिलीज़ योजनाओं में कैसे फिट होगा, हालांकि फिलहाल मैं pure java वितरित करने की ओर झुका हूँ लेकिन java और natively compiled दोनों संस्करणों का समर्थन करने के पक्ष में हूँ। अलग-अलग OSes और लाइब्रेरी वर्ज़न आदि के लिए ढेरों अलग बिल्ड बनाना और वितरित करना थोड़ा कष्टदायक है। क्या इस मोर्चे पर किसी की कोई मजबूत राय है?

GCJ समर्थन की एक और सकारात्मक विशेषता यह है कि C/C++/Python/आदि जैसी भाषाओं से streaming lib (स्ट्रीमिंग लाइब्रेरी) का उपयोग करने की सुविधा मिलती है। मुझे नहीं पता कि कोई उस तरह के एकीकरण पर काम कर रहा है या नहीं, लेकिन संभवतः यह सार्थक होगा, तो यदि आप उस मोर्चे पर विकास करने में रुचि रखते हैं, तो कृपया मुझे बताएं!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

हालाँकि i2p-bt I2P पर पोर्ट किया जाने वाला पहला BitTorrent क्लाइंट था जिसका काफ़ी उपयोग हुआ, eco ने काफ़ी समय पहले snark [5] का पोर्ट बनाकर सबसे पहले बाज़ी मार ली थी। दुर्भाग्यवश, वह ताज़ा नहीं रहा या अन्य अनाम BitTorrent क्लाइंट्स के साथ अनुकूलता बनाए नहीं रख सका, इसलिए वह कुछ समय के लिए लगभग गायब ही हो गया। पिछले सप्ताह, हालांकि, मुझे i2p-bt<->sam<->streaming lib<->i2cp शृंखला में कहीं प्रदर्शन संबंधी समस्याओं से निपटने में दिक्कत हो रही थी, तो मैं mjw के मूल snark कोड पर चला गया और एक साधारण पोर्ट [6] किया, जिसमें किसी भी java.net.*Socket calls को I2PSocket* calls से, InetAddresses को Destinations से, और URLs को EepGet calls से बदल दिया। परिणामस्वरूप एक छोटा-सा कमांड-लाइन BitTorrent क्लाइंट (कम्पाइल होने पर लगभग 60KB) मिला, जिसे अब हम I2P रिलीज़ के साथ शामिल करेंगे।

Ragnarok ने इसके ब्लॉक चयन एल्गोरिथ्म को बेहतर बनाने के लिए इसके कोड में पहले ही हैकिंग शुरू कर दी है, और उम्मीद है कि 0.6.2 रिलीज़ से पहले हम इसमें वेब इंटरफ़ेस और मल्टीटोरेंट क्षमताएँ दोनों जोड़ पाएँगे। यदि आप मदद करने में रुचि रखते हैं, तो संपर्क करें! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

हाल में मेलिंग सूची काफ़ी सक्रिय रही है, Michael के नए सिमुलेशन और tunnel निर्माण के विश्लेषण के साथ। चर्चा अभी भी जारी है, और Toad, Tom तथा polecat से कुछ अच्छे विचार आए हैं, तो यदि आप कुछ अनामता-संबंधी डिज़ाइन मुद्दों के लिए होने वाले समझौतों पर अपनी राय देना चाहते हैं, जिनका हम 0.6.2 रिलीज़ [7] के लिए पुनर्गठन करने वाले हैं, तो इसे देखें।

जो लोग कुछ दृश्य आकर्षण चाहते हैं, उनके लिए Michael ने एक सिमुलेशन भी दिया है, जो दिखाता है कि हमला आपकी पहचान कितनी संभावना से कर सकता है - वे नेटवर्क का कितना प्रतिशत नियंत्रित करते हैं, इसके फ़ंक्शन के रूप में [8], और आपका tunnel (I2P में ट्रैफ़िक रूट करने का मार्ग) कितना सक्रिय है, इसके फ़ंक्शन के रूप में [9]

(बहुत बढ़िया काम, माइकल, धन्यवाद!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     ("i2p tunnel bootstrap attack" थ्रेड का अनुसरण करें) [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

एक विशिष्ट I2P-सक्षम अनुप्रयोग के साथ वितरित किए जा रहे संभावित मैलवेयर संबंधी मुद्दों के बारे में कुछ चर्चा हुई है, और Complication ने इसकी गहराई से जांच करने में बहुत बढ़िया काम किया है। डेटा सार्वजनिक रूप से उपलब्ध है, इसलिए आप अपनी स्वयं की राय बना सकते हैं। [10]

Complication, इस पर आपके सभी शोध के लिए धन्यवाद!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

काफी कुछ चल रहा है, जैसा कि आप देख सकते हैं, लेकिन मीटिंग के लिए पहले ही देर हो चुकी है, तो शायद मुझे इसे सेव करके भेज देना चाहिए, है न? #i2p पर मिलते हैं :)

=jr
