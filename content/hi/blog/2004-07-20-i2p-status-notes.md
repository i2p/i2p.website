---
title: "2004-07-20 के लिए I2P स्थिति टिप्पणियाँ"
date: 2004-07-20
author: "jr"
description: "0.3.2.3 रिलीज़, क्षमता में बदलाव, वेबसाइट अद्यतन और सुरक्षा संबंधी विचारों को शामिल करने वाला साप्ताहिक स्थिति अद्यतन"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, और रोडमैप**

पिछले हफ्ते 0.3.2.3 के रिलीज़ के बाद, आप सबने अपग्रेडिंग बहुत बढ़िया की है - अब हमारे पास सिर्फ दो लोग बचे हैं जो अपग्रेड नहीं हुए हैं (एक 0.3.2.2 पर और एक काफ़ी पीछे 0.3.1.4 पर :). पिछले कुछ दिनों में नेटवर्क सामान्य से अधिक भरोसेमंद रहा है - लोग irc.duck.i2p पर एक बार में घंटों तक ठहर रहे हैं, eepsites(I2P Sites) से बड़े फ़ाइल डाउनलोड सफल हो रहे हैं, और सामान्य eepsite(I2P Site) तक पहुँच भी काफ़ी अच्छी है। चूँकि सब कुछ अच्छा चल रहा है और मैं चाहता हूँ कि आप सतर्क बने रहें, मैंने कुछ बुनियादी अवधारणाएँ बदलने का फैसला किया है और हम उन्हें एक-दो दिनों में 0.3.3 रिलीज़ में तैनात कर देंगे.

चूंकि कुछ लोगों ने हमारी समय-सारणी पर टिप्पणी की, यह सोचते हुए कि क्या हम वे तारीखें पूरी कर पाएंगे जिन्हें हमने प्रकाशित किया था, मैंने तय किया कि मुझे वेबसाइट को मेरे palmpilot में मौजूद रोडमैप के अनुरूप अपडेट कर देना चाहिए, इसलिए मैंने कर दिया [1]। तारीखें आगे खिसक गई हैं और कुछ मदों को पुनर्व्यवस्थित किया गया है, लेकिन योजना अब भी वही है जिसके बारे में पिछले महीने चर्चा की गई थी [2]।

0.4 उल्लेखित चार रिलीज़ मानदंडों (कार्यात्मक, सुरक्षित, गुमनाम, और स्केलेबल) को पूरा करेगा, हालाँकि 0.4.2 से पहले, NAT (Network Address Translation) और फ़ायरवॉल के पीछे रहने वाले बहुत कम लोग भाग ले पाएँगे, और 0.4.3 से पहले अन्य routers के साथ बड़ी संख्या में TCP कनेक्शनों को बनाए रखने के ओवरहेड के कारण नेटवर्क के आकार पर एक व्यावहारिक ऊपरी सीमा रहेगी।

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

पिछले हफ्ते भर में, #i2p पर लोगों ने मुझे कभी-कभी यह शिकायत करते सुना है कि हमारी विश्वसनीयता रैंकिंग्स पूरी तरह मनमानी हैं (और पिछले कुछ रिलीज़ों में इससे हुई परेशानी)। इसलिए हमने विश्वसनीयता की अवधारणा को पूरी तरह हटा दिया है, और उसकी जगह क्षमता का एक माप रखा है - "एक पीयर हमारे लिए कितना कर सकता है?" इसका असर पीयर चयन और पीयर प्रोफाइलिंग कोड (और स्वाभाविक रूप से router console) में तो पड़ा है, लेकिन उसके अलावा ज़्यादा बदलाव नहीं हुआ।

इस परिवर्तन के बारे में अधिक जानकारी संशोधित पीयर चयन पृष्ठ [3] पर देखी जा सकती है, और जब 0.3.3 जारी किया जाएगा, तो आप सभी उसके प्रभाव को प्रत्यक्ष रूप से देख सकेंगे (मैं पिछले कुछ दिनों से इसे आज़मा रहा हूँ, कुछ सेटिंग्स को समायोजित कर रहा हूँ, आदि।)

[3] http://www.i2p.net/redesign/how_peerselection

**3) वेबसाइट अद्यतन**

पिछले सप्ताह के दौरान, हमने वेबसाइट रीडिज़ाइन [4] पर काफी प्रगति की है - नेविगेशन को सरल बनाना, कुछ प्रमुख पृष्ठों को साफ़ करना, पुरानी सामग्री को आयात करना, और कुछ नई प्रविष्टियाँ [5] लिखना। हम साइट को लाइव करने के लिए लगभग तैयार हैं, लेकिन अभी भी कुछ चीज़ें बाकी हैं जिन्हें करना है।

आज सुबह, duck ने साइट का अवलोकन किया और जिन पृष्ठों की कमी है उनकी सूची तैयार की, और आज दोपहर के अद्यतनों के बाद, कुछ प्रमुख लंबित मुद्दे हैं जिनके बारे में मुझे उम्मीद है कि हम या तो उन्हें स्वयं सुलझाएँगे या कुछ स्वयंसेवक उन पर काम शुरू करेंगे:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

इसके अलावा, मेरा मानना है कि साइट लगभग लाइव करने के लिए तैयार है। क्या किसी के पास इस संबंध में कोई सुझाव या चिंताएँ हैं?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) हमले और रक्षा-उपाय**

Connelly नेटवर्क की सुरक्षा और गुमनामी में कमज़ोरियाँ खोजने के लिए कुछ नए दृष्टिकोण लेकर आया है, और ऐसा करते हुए उसे कुछ ऐसे तरीक़े मिले हैं जिनसे हम सुधार कर सकते हैं। हालाँकि जिन तकनीकों का उसने वर्णन किया है उनके कुछ पहलू वास्तव में I2P से मेल नहीं खाते, शायद आप सब देख सकें कि उन्हें कैसे विस्तार देकर नेटवर्क पर और आगे हमला किया जा सकता है? अरे, एक बार कोशिश करके देखो :)

**5) ???**

आज रात की मीटिंग से पहले मुझे फिलहाल इतना ही याद है—अगर मैंने कुछ अनदेखा किया हो तो बेझिझक बता दें। खैर, कुछ ही मिनटों में #i2p पर मिलते हैं।

=jr
