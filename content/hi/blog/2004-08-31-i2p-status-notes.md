---
title: "I2P स्थिति नोट्स 2004-08-31 के लिए"
date: 2004-08-31
author: "jr"
description: "साप्ताहिक I2P स्थिति अद्यतन जिसमें नेटवर्क प्रदर्शन में गिरावट, 0.3.5 रिलीज़ योजना, प्रलेखन आवश्यकताएँ, और Stasher DHT प्रगति शामिल हैं"
categories: ["status"]
---

तो लड़के और लड़कियाँ, फिर से मंगलवार है!

## अनुक्रमणिका:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

खैर, जैसा कि आप सबने ध्यान दिया होगा, नेटवर्क पर उपयोगकर्ताओं की संख्या काफ़ी स्थिर रही है, लेकिन पिछले कुछ दिनों में प्रदर्शन में काफ़ी गिरावट आई है। इसका कारण peer selection (पीयर चयन) और संदेश वितरण कोड में बग्स की एक श्रृंखला रही है, जो पिछले हफ्ते एक मामूली DoS होने पर उजागर हुई। परिणामस्वरूप, मूलतः सबके tunnels लगातार विफल हो रहे हैं, जिसका बर्फ़ के गोले की तरह बढ़ता हुआ असर पड़ा है। तो नहीं, समस्या सिर्फ़ आपके साथ नहीं है — बाक़ी हम सबके लिए भी नेट बहुत ख़राब रही है ;)

लेकिन अच्छी खबर यह है कि हमने समस्याओं को काफ़ी जल्दी ठीक कर दिया, और वे पिछले हफ्ते से CVS में हैं, पर अगला रिलीज़ आने तक लोगों के लिए नेटवर्क अभी भी काफ़ी खराब रहेगा। इसी संदर्भ में...

## 2) 0.3.5 और 0.4

भले ही अगला रिलीज़ 0.4 रिलीज़ के लिए हमारी योजना में शामिल सभी सुविधाएँ लाएगा (नया इंस्टॉलर, नया वेब इंटरफ़ेस मानक, नया i2ptunnel इंटरफ़ेस, systray और windows service, थ्रेडिंग में सुधार, बग फिक्स, आदि), पिछला रिलीज़ समय के साथ जिस तरह बिगड़ता गया, वह बहुत कुछ बताता है। मैं चाहता हूँ कि हम इन रिलीज़ पर थोड़ा धीमे चलें, ताकि उन्हें और अधिक व्यापक रूप से तैनात होने का समय मिले और खामियाँ खुद सामने आ सकें। हालाँकि सिमुलेटर बुनियादी बातों की पड़ताल कर सकता है, लेकिन लाइव नेट पर दिखने वाली स्वाभाविक नेटवर्क समस्याओं का अनुकरण करने का कोई तरीका उसके पास नहीं है (कम से कम अभी नहीं)।

इसलिए, अगला रिलीज़ 0.3.5 होगा — उम्मीद है कि यह 0.3.* श्रृंखला का अंतिम रिलीज़ होगा, लेकिन अगर अन्य समस्याएँ सामने आती हैं तो शायद नहीं। जून में जब मैं ऑफ़लाइन था, तब नेटवर्क कैसे काम कर रहा था, इस पर पीछे मुड़कर देखें तो लगभग दो सप्ताह बाद चीज़ें बिगड़ने लगी थीं। इस वजह से, मेरा विचार है कि जब तक हम कम-से-कम दो सप्ताह तक उच्च स्तर की विश्वसनीयता बनाए रखने में सक्षम नहीं हो जाते, तब तक हमें खुद को अगले 0.4 रिलीज़ स्तर तक बढ़ाने को टाल देना चाहिए। इसका यह मतलब नहीं है कि इस बीच हम काम नहीं करेंगे, बेशक।

खैर, जैसा कि पिछले हफ्ते बताया था, hypercubus नए इंस्टॉल सिस्टम पर लगातार काम कर रहे हैं, मेरी तरफ़ से चीज़ों में इधर-उधर बदलाव करने और अजीबो-गरीब सिस्टम्स के लिए समर्थन की मांग से निपटते हुए। हम अगले कुछ दिनों में सब कुछ पक्का कर लेंगे ताकि अगले कुछ दिनों में 0.3.5 रिलीज़ निकाल सकें।

## 3) प्रलेखन

0.4 से पहले वाले दो सप्ताह के "testing window" के दौरान हमें जो एक महत्वपूर्ण काम करना है, वह है बहुत व्यापक दस्तावेज़ीकरण करना। मैं यह जानना चाहता हूँ कि आपको क्या लगता है, हमारे दस्तावेज़ों में क्या कमी है - ऐसे कौन से प्रश्न हैं जिनका उत्तर हमें देना चाहिए? भले ही मैं यह कहना चाहूँ कि "ok, now, go write those documents", मैं यथार्थवादी हूँ, इसलिए मैं सिर्फ इतना चाहता हूँ कि आप बता दें कि वे दस्तावेज़ किन बातों पर चर्चा करेंगे।

उदाहरण के लिए, जिन दस्तावेज़ों पर मैं अभी काम कर रहा हूँ, उनमें से एक धमकी मॉडल का संशोधित संस्करण है, जिसे मैं अब उपयोग के मामलों की एक शृंखला के रूप में वर्णित करूँगा, जो बताती है कि I2P विभिन्न व्यक्तियों की आवश्यकताओं को कैसे पूरा कर सकता है, जिसमें शामिल हैं: कार्यात्मकता, किन हमलावरों से चिंता होती है, और उनसे बचाव कैसे किया जाता है।

यदि आपको लगता है कि आपके प्रश्न का समाधान करने के लिए किसी पूरी तरह विस्तृत दस्तावेज़ की आवश्यकता नहीं है, तो उसे बस प्रश्न के रूप में लिख दें और हम उसे अक्सर पूछे जाने वाले प्रश्न (FAQ) में जोड़ सकते हैं।

## 4) stasher update

Aum आज थोड़ी देर पहले चैनल पर एक अपडेट के साथ आया था (जबकि मैं उससे सवालों की बौछार कर रहा था):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
तो, जैसा कि आप देख सकते हैं, बहुत ज़्यादा प्रगति हुई है। भले ही कुंजियाँ DHT layer (वितरित हैश तालिका परत) के ऊपर सत्यापित की जाएँ, यह बहुत जबरदस्त है (मेरी विनम्र राय में)। आगे बढ़ो, aum!

## 5) ???

ठीक है, मुझे बस इतना ही कहना था (जो अच्छा है, क्योंकि बैठक कुछ ही पलों में शुरू होने वाली है)... बस आ जाना और जो चाहो कह देना!

=jr
