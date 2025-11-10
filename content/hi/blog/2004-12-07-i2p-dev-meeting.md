---
title: "I2P डेवलपर बैठक - दिसंबर 07, 2004"
date: 2004-12-07
author: "@duck"
description: "07 दिसंबर 2004 की I2P विकास बैठक का लॉग."
categories: ["meeting"]
---

## त्वरित पुनरावलोकन

<p class="attendees-inline"><strong>उपस्थित:</strong> ant, bushka, clayboy, dinoman, duck, Frooze, mule, postman, protokol, Ragnarok, slart, ugha2p</p>

## बैठक लॉग

<div class="irc-log">22:00:00 &lt;@duck&gt; Tue Dec  7
21:00:00 UTC 2004
22:00:04 &lt;@duck&gt; I2P बैठक का समय
22:00:05 &lt;Frooze&gt; मैंने अभी i2p के लिए Frooze बना दिया।  मुझे तो यह भी नहीं पता कि 'frooze' क्या होता है।
22:00:21 &lt;@duck&gt; जैसा कि http://dev.i2p.net/pipermail/i2p/2004-December/000509.html पर घोषित किया गया है
22:00:29 &lt;@duck&gt; कार्यसूची:
22:00:29 &lt;@duck&gt; 0) नमस्ते
22:00:29 &lt;@duck&gt; 1) 0.4.2.3
22:00:29 &lt;@duck&gt; 2) i2p-bt
22:00:29 &lt;@duck&gt; 3) #idlerpg
22:00:29 &lt;@duck&gt; 4) ???
22:00:32 &lt;@duck&gt; .
22:01:09 &lt;@duck&gt; 0) नमस्ते
22:01:15 &lt;clayboy&gt; नमस्ते
22:01:16 &lt;@duck&gt; jrandom ने बताया कि तबीयत खराब है
22:01:20 &lt;+ugha2p&gt; नमस्ते।
22:01:30 &lt;@duck&gt; और मुझे मैसेज किया कि शायद वह नहीं आ पाएगा
22:01:39 &lt;+protokol&gt; http://www.google.com/search?q=frooze
22:01:41 &lt;@duck&gt; तो देखते हैं और बस शुरू करते हैं
22:01:46 &lt;clayboy&gt; आशा है वह जल्दी ठीक हो जाए
22:02:06 &lt;@duck&gt; 1) 0.4.2.3
22:02:16 &lt;@duck&gt; नया रिलीज़ बेहद जल्द आ जाएगा
22:02:31 &lt;@duck&gt; यानी कल या गुरुवार।
22:02:41 &lt;@duck&gt; काफ़ी सारे बगफ़िक्स हुए हैं
22:03:24 &lt;+ugha2p&gt; क्या नए CVS revisions memory/CPU समस्याएँ भी ठीक करते हैं?
22:03:29 &lt;clayboy&gt; हममें से कुछ लोग CVS builds चला रहे हैं, यह काफ़ी बढ़िया काम कर रहा है
22:03:33 &lt;@duck&gt; ज़्यादातर streaming lib, sam bridge, आदि
22:04:17 &lt;+ugha2p&gt; मुझे I2P से कुछ असामान्य लोड दिख रहे हैं।
22:04:23 &lt;clayboy&gt; मुझे लगता है वे कई revisions पहले ठीक हो गए थे, ugha2p
22:04:41 &lt;+ugha2p&gt; (Running -7)
22:04:51 &lt;clayboy&gt; ओह, हम्म
22:04:52 &lt;@duck&gt; ugha2p: history में उसके बारे में कुछ नहीं दिख रहा
22:05:48 &lt;+protokol&gt; पता है क्या अच्छा होगा (भले ही संभव/लायक न हो) — changelog का एक RSS feed
22:05:48 &lt;@duck&gt; ठीक है
22:05:49 &lt;+ugha2p&gt; अजीब है।
22:06:01 &lt;+protokol&gt; ;-)
22:06:17 &lt;@duck&gt; शायद एक bugzilla item रिपोर्ट कर दो
22:06:25 &lt;@duck&gt; या पता नहीं
22:06:34 &lt;+ugha2p&gt; Java process लगभग आधे समय 100% CPU खा रहा है।
22:07:18 &lt;+ugha2p&gt; तो, आपको इस issue के बारे में कुछ पता नहीं? क्या आपके routers ठीक काम कर रहे हैं?
22:07:24 &lt;dinoman&gt; हाँ, मेरे यहाँ भी high है -6
22:08:24 &lt;@duck&gt; मेरे nptl upgrade के बाद से top/uptime info अजीब बर्ताव कर रही है, तो कह नहीं सकता
22:09:03 &lt;+ugha2p&gt; ठीक है, शायद हमें आगे बढ़ना चाहिए?
22:09:07 &lt;@duck&gt; ठीक है
22:09:14 &lt;@duck&gt; 2) i2p-bt
22:09:24 &lt;+ugha2p&gt; और jrandom से पूछना कि वह 0.4.2.3 कब रिलीज़ करने वाला है
22:09:40 &lt;+ugha2p&gt; यह मेरे लिए NPTL के साथ ठीक चला है।
22:09:45 &lt;@duck&gt; ugha2p: उसने कहा कल या गुरुवार
22:09:58 &lt;+ugha2p&gt; सही।
22:09:59 &lt;@duck&gt; कल मैंने नया i2p-bt रिलीज़ किया
22:10:23 &lt;@duck&gt; मुझे पूरे 'buffer' कॉन्सेप्ट की कुछ नई समझ मिली
22:10:42 &lt;@duck&gt; साथ ही Ragnarok के कुछ पुराने pending patches थे
22:11:13 &lt;mule&gt; duck: बधाई, अच्छा काम!
22:11:15 &lt;@duck&gt; slice size भी बढ़ाया गया है, यानी हर बार 32KB भेजने के बजाय अब 128KB भेजता है
22:11:29 &lt;@duck&gt; जिससे queue भरी रहनी चाहिए
22:11:47 &lt;+ugha2p&gt; हाँ, धन्यवाद, duck. :)
22:11:56 &lt;@duck&gt; DrWoo और दूसरों ने कुछ GUI फीचर अनुरोध दायर किए हैं
22:12:23 &lt;@duck&gt; पर मैं खुद GUI इस्तेमाल नहीं करता, wxpython नहीं जानता और शायद बहुत परवाह भी नहीं करता :)
22:12:31 &lt;+Ragnarok&gt; हर slice को एक single message में फिट करना उम्मीद के मुताबिक अच्छा काम नहीं किया?
22:12:57 &lt;clayboy&gt; http://brittanyworld.i2p/bittorrent/ पर कई seeded torrents हैं, अगर कोई आज़माना चाहे (i2p 0.4.2.2-7 और i2p-bt 0.1.3 के साथ)
22:13:10 &lt;@duck&gt; Ragnarok: यह थोड़ा अनुमान ही था
22:13:27 &lt;@duck&gt; यह local transfers पर काफ़ी अधिक throughput देता है
22:13:51 &lt;+ugha2p&gt; शायद हमें इंतज़ार करना चाहिए कि कोई एक full-featured client पोर्ट कर दे?
22:14:10 &lt;+Ragnarok&gt; हम्म, ठीक
22:14:13 &lt;@duck&gt; हम सब इंतज़ार कर सकते हैं :)
22:14:37 &lt;clayboy&gt; BitTorrent वास्तव में "full featured" है, bt के लिए मैं सिर्फ़ इसी client का उपयोग करता हूँ (I2P के बाहर भी) :)
22:15:15 &lt;+ugha2p&gt; ऐसा नहीं है। :)
22:16:02 &lt;@duck&gt; व्यक्तिगत तौर पर मुझे उचित defaults वाली चीज़ें पसंद हैं
22:16:17 &lt;@duck&gt; जैसे mldonkey में आप 10 लाख चीज़ें बदल सकते हैं और ज़्यादातर यूज़र को नहीं पता कि वे क्या करती हैं
22:16:50 &lt;@duck&gt; इससे user-myths बनते हैं, जैसे I2P यूज़र हर समय 'Reseed' दबाते रहना, या काम न करे तो फिर से इंस्टॉल कर देना
22:17:01 &lt;+ugha2p&gt; जो बिल्ली के बच्चों को मारता है
22:17:28 &lt;slart&gt; bittornado के बारे में क्या ख़याल है?
22:17:43 &lt;+Ragnarok&gt; मुझे लगता है मैं pygtk GUI लिखने के लिए उकसाया जा सकता हूँ, पर मेरे पास और बहुत काम है, और मुझे पक्का नहीं कि लोग क्या चाहते हैं
22:17:45 &lt;+protokol&gt; azureus?
22:17:57 &lt;@duck&gt; मेरे अंदर का एक हिस्सा तो बेशक काम न करने के बहाने बना रहा है
22:18:03 &lt;+protokol&gt; azureus plugins सपोर्ट करता है
22:18:10 &lt;@duck&gt; protokol: तो फिर एक plugin लिखो
22:18:32 &lt;+protokol&gt; हेह
22:18:40 &lt;slart&gt; bittornado आधिकारिक bt पर आधारित है, है ना?
22:18:50 &lt;+protokol&gt; कहना आसान, करना मुश्किल
22:18:52 &lt;@duck&gt; slart: मैंने उसे देखा और रो पड़ा
22:19:07 &lt;@duck&gt; उसमें कुछ सुधार हैं, जो उपयोगी हो सकते हैं
22:19:17 &lt;@duck&gt; लेकिन दूसरी ओर, उसने पूरी चीज़ को बहुत ज़्यादा जटिल बना दिया
22:19:22 &lt;@duck&gt; बिना original code को साफ़ किए
22:19:36 &lt;+Ragnarok&gt; उफ़
22:19:56 &lt;@duck&gt; वह GUI फीचर कि अगर arguments न दिए जाएँ तो आप एक torrent चुन सकें, वहीं से लिया गया है और i2p-bt में जोड़ा गया है
22:20:11 &lt;clayboy&gt; पहले basic BitTorrent को बेहतरीन तरह से चलाएं, फिर इन हल्की-फुल्की GUI चीज़ों की चिंता करें :)
22:20:46 &lt;@duck&gt; slart: शायद और भी चीज़ें इस्तेमाल की जा सकती हैं; बस किसी को इसे (ठीक ढंग से) करना होगा
22:21:23 &lt;+ugha2p&gt; खैर, मुझे लगता है यह पहले से ही बढ़िया काम करता है। :)
22:21:53 &lt;slart&gt; abc client tornado का उपयोग करता है (मेरा ख़याल है)
22:22:15 &lt;clayboy&gt; मुझे लगता है हमें अभी भी काफ़ी heavy-duty testing करनी है ताकि पता चले कि i2p-bt के ज़रिए वाकई कितना डेटा धकेला जा सकता है
22:22:21 &lt;bushka&gt; हाँ, करता है slart.
22:23:49 &lt;@duck&gt; वे कैसे काम करते हैं, उस पर निर्भर करते हुए आप i2p-bt के बदलावों को उन पर काफ़ी आसानी से पोर्ट कर सकते हैं
22:24:41 &lt;@duck&gt; कृपया इसे आज़माएँ और रिपोर्ट करें
22:25:47 &lt;@duck&gt; .
22:25:55 &lt;@duck&gt; i2p-bt / BitTorrent पर कोई और टिप्पणी?
22:26:08 &lt;slart&gt; python :S
22:26:41 &lt;+ugha2p&gt; .
22:26:51 &lt;@duck&gt; slart: अगर आपको python पसंद नहीं, तो आप azureus को पोर्ट करने की कोशिश कर सकते हैं
22:27:00 &lt;+ugha2p&gt; slart: उसके बारे में क्या?
22:27:06 &lt;slart&gt; speed testing के लिए linux जैसी किसी चीज़ को seed करने के लिए हम कितने लोगों को जुटा सकते हैं?
22:27:15 &lt;slart&gt; *iso
22:27:34 &lt;@duck&gt; चलो नया I2P रिलीज़ आने के बाद वह आज़माते हैं
22:27:57 &lt;@duck&gt; (क्योंकि ज़्यादातर लोगों के लिए CVS से I2P router build खींचना काफ़ी चुनौती है)
22:28:17 &lt;+protokol&gt; एह
22:28:54 &lt;@duck&gt; pl
22:28:57 &lt;@duck&gt; अरे, ठीक है
22:29:10 &lt;@duck&gt; 3) #idlerpg
22:29:22 &lt;@duck&gt; यह मज़ेदार IRC RPG game मिला
22:29:36 &lt;@duck&gt; इसके लिए कुछ करना नहीं होता, बस idle रहना है
22:29:56 &lt;+ugha2p&gt; खैर, LOGIN तो करना होता है। ;)
22:30:04 &lt;@duck&gt; आह ;)
22:30:18 &lt;mule&gt; cvs update -dP :)
22:30:18 &lt;mule&gt; ant dist updater :)
22:30:20 &lt;+postman&gt; यह सबसे मज़ेदार चीज़ है जो मैंने देखी है, और मुझे यह पसंद है :)
22:30:30 &lt;+protokol&gt; इसमें पुरस्कार होने चाहिए
22:30:45 &lt;@duck&gt; ircnet पर इसके 779 online खिलाड़ी हैं
22:30:46 &lt;+ugha2p&gt; duck: मैं सोच रहा था, यह अपग्रेड न करने की एक संभावित वजह हो सकती है।
22:30:52 &lt;+protokol&gt; जीतने या स्तर पाने पर yodels दिए जाएँ
22:31:03 &lt;+ugha2p&gt; हालाँकि मुझे नहीं लगता कि I2P पर लोग इतने बचकाने होंगे। :)
22:31:14 &lt;+protokol&gt; मुझे पता है duck के पास yodels में लगभग $10000 हैं
22:31:18 &lt;@duck&gt; protokol: हाँ, मुझे देखना होगा कि वे quests कैसे काम करते हैं
22:31:39 &lt;@duck&gt; शायद हम इसके साथ कुछ मज़ेदार चीज़ें कर सकें
22:31:42 &lt;@duck&gt; ugha2p: आपका मतलब?
22:31:49 &lt;ant&gt; * cervantes अपने router को रीस्टार्ट किए बिना और 40 दिन नहीं गुज़ारने वाला
22:32:08 &lt;@duck&gt; ugha2p: ओह, खेल की वजह से अपडेट न करना :)
22:32:18 &lt;+protokol&gt; Linux: अगर आप बिना रीस्टार्ट किए ठीक नहीं कर सकते, तो आप इसे ठीक नहीं कर सकते।
22:32:20 &lt;@duck&gt; ठीक है, मेरा router रीस्टार्ट होते समय मैं इसे pause पर रख दूँगा
22:32:24 &lt;+ugha2p&gt; :)
22:32:33 &lt;@duck&gt; तो अगर आप इसे ठीक से sync करें, तो आप हारेंगे नहीं
22:32:35 &lt;@duck&gt; हेहे
22:32:55 &lt;ant&gt; &lt;cervantes&gt; यह अच्छा है... क्योंकि आपका router हर समय रीस्टार्ट होता रहता है :P
22:33:16 &lt;@duck&gt; इसे कहते हैं dedicated testing :)
22:33:20 &lt;ant&gt; &lt;cervantes&gt; मेरा ख़याल है इससे समीकरण में roulette भी शामिल हो जाता है
22:33:23 &lt;@duck&gt; ठीक है
22:33:38 &lt;@duck&gt; .
22:33:49 &lt;+ugha2p&gt; .
22:34:05 &lt;@duck&gt; 5) ???
22:34:08 &lt;@duck&gt; s/5/4/
22:34:12 &lt;@duck&gt; ओपन माइक!
22:34:23 &lt;+postman&gt; .
22:34:53 &lt;mule&gt; थोड़ा tweaking करके आप दो routers रख सकते हैं। एक सिर्फ़ खेल के लिए, जिसे आप साल में सिर्फ़ एक बार अपग्रेड करें
22:34:53 &lt;@duck&gt; कोई प्रश्न? टिप्पणियाँ? सुझाव?
22:35:38 &lt;ant&gt; &lt;mahes&gt; नमस्ते, मेरे पास एक सामान्य non-dev प्रश्न है
22:36:08 &lt;@duck&gt; पूछिए
22:36:08 &lt;+ugha2p&gt; बैठक कराने के लिए धन्यवाद, duck.
22:36:50 &lt;ant&gt; &lt;mahes&gt; यदि मैं eepsite सेट करूँ, तो उसे mahes.i2p जैसे पते से कैसे पहुँचा जा सकता है
22:36:59 &lt;+protokol&gt; मेरी एक चिंता है
22:37:44 &lt;+protokol&gt; (लड़ाई शुरू) मुझे लगता है .i2p कई कारणों से घटिया TLD है
22:38:19 &lt;+ugha2p&gt; mahes: "कैसे" से आपका क्या मतलब? लोग अपने ब्राउज़र को eepproxy इस्तेमाल करने के लिए कॉन्फ़िगर करेंगे, और अपने address bar में बस http://mahes.i2p/ लिख देंगे।
22:38:19 &lt;+protokol&gt; मेरा मानना है हमें ऐसा लेना चाहिए जो a) एक syllable हो b) एक शब्द की तरह बोला जा सके c) जिसमें कोई number न हो'
22:38:46 &lt;+ugha2p&gt; जैसे .eep?
22:39:07 &lt;@duck&gt; mahes:: अपनी eepsite की ओर इशारा करने वाला कोई 'nice name' पाने के लिए, उसे आपके hosts.txt फ़ाइल में होना चाहिए
22:39:37 &lt;+protokol&gt; ज़रूर
22:40:01 &lt;+ugha2p&gt; आप mailing list पर एक प्रस्ताव दे सकते हैं।
22:40:03 &lt;@duck&gt; आप इसे eepsite announcement forum पर पोस्ट कर सकते हैं ताकि दूसरे भी इसे पा सकें
22:40:09 &lt;+ugha2p&gt; सम्भवत: जब हमारे पास MyI2P होगा तब इसे विचार किया जाएगा।
22:40:35 &lt;+protokol&gt; हेह, मैं कोशिश करूँगा पर jr इसे किसी वजह से पहले ही खारिज कर चुका है
22:41:06 &lt;ant&gt; &lt;mahes&gt; खैर. मैं तो बस एक user हूँ...  ठीक है, तो मैं बस mahes.i2p=hhfbwer8328... प्रकाशित कर दूँ और यह अपने आप फैल जाएगा
22:41:32 &lt;@duck&gt; यह अपने आप नहीं फैलता, लोगों को किसी तरह इसे अपनी hosts.txt में डालना पड़ता है
22:41:39 &lt;ant&gt; &lt;mahes&gt; ठीक है
22:41:52 &lt;@duck&gt; पर इसे फ़ोरम पर घोषित करें तो इसके फैलने की संभावना ज़्यादा है :)
22:42:34 &lt;@duck&gt; .
22:43:18 &lt;@duck&gt; चलो इसे एक *baf* दें
22:43:20 &lt;+ugha2p&gt; .
22:43:30  * ugha2p baffer का इंतज़ार कर रहा है।
22:43:38  * duck तैयारी कर रहा है
22:43:45  * duck ने बैठक को *baf* करके बंद किया </div>
