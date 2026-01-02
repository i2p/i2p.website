---
title: "I2P Mime प्रकार"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## अवलोकन

सामान्य I2P फाइल प्रारूपों के लिए mime प्रकार परिभाषित करें।
परिभाषाएँ Debian पैकेजों में शामिल करें।
.su3 प्रकार के लिए एक हैंडलर प्रदान करें, और शायद अन्य के लिए भी।


## प्रेरणा

ब्राउज़र के साथ डाउनलोड करते समय पुनःबीजिंग और प्लगइन स्थापना को आसान बनाने के लिए,
हमें .su3 फाइलों के लिए एक mime प्रकार और हैंडलर की आवश्यकता है।

जब हम इसमें हों, freedesktop.org मानक का पालन करते हुए mime परिभाषा फ़ाइल लिखने के बाद,
हम अन्य सामान्य I2P फाइल प्रकारों के लिए परिभाषाएँ जोड़ सकते हैं।
जबकि कम उपयोगी उन फाइलों के लिए जो आमतौर पर डाउनलोड नहीं की जाती हैं, जैसे कि
पता पुस्तिका ब्लॉकफाइल डेटाबेस (hostsdb.blockfile), ये परिभाषाएँ
फाइलों को बेहतर पहचानने और आइकोनीकरण करने को सक्षम करेंगीं जब ग्राफिकल
डायरेक्टरी व्यूअर जैसे "nautilus" पर Ubuntu का उपयोग करते हुए।

mime प्रकारों को मानक बनाकर, प्रत्येक राउटर कार्यान्वयन उपयुक्त रूप से हैंडलर लिख सकता है,
और mime परिभाषा फ़ाइल सभी कार्यान्वयनों द्वारा साझा की जा सकती है।


## डिज़ाइन

Freedesktop.org मानक का पालन करते हुए एक XML स्रोत फ़ाइल लिखें और इसे
Debian पैकेजों में शामिल करें। फ़ाइल का नाम है "debian/(पैकेज).sharedmimeinfo"।

सभी I2P mime प्रकार "application/x-i2p-" से शुरू होंगे, जरोबिन रर्ड को छोड़कर।

इन mime प्रकारों के लिए हैंडलर एप्लिकेशन-विशिष्ट हैं और यहाँ निर्दिष्ट नहीं होंगे।

हम Jetty के साथ परिभाषाएँ भी शामिल करेंगे, और उन्हें
पुनःबीज सॉफ़्टवेयर या निर्देशों के साथ शामिल करेंगे।


## विशिष्टता

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(generic)	application/x-i2p-su3

.su3	(router update)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(reseed)	application/x-i2p-su3-reseed

.su3	(news)		application/x-i2p-su3-news

.su3	(blocklist)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## नोट्स

ऊपर सूचीबद्ध सभी फाइल प्रारूपों का उपयोग गैर-जावा राउटर कार्यान्वयनों द्वारा नहीं किया जाता है;
कुछ अच्छी तरह से निर्दिष्ट भी नहीं हो सकते हैं। हालाँकि, उन्हें यहाँ दस्तावेजित करने से
भविष्य में क्रॉस-कार्यान्वयन संगति सक्षम हो सकती है।

कुछ फाइल प्रत्यय जैसे ".config", ".dat", और ".info" अन्य
mime प्रकारों के साथ ओवरलैप कर सकते हैं। इन्हें अतिरिक्त डेटा के साथ भिन्न किया जा सकता है जैसे
पूरा फाइल नाम, एक फाइल नाम पैटर्न, या जादुई संख्याएँ।
उदाहरणों के लिए zzz.i2p थ्रेड में ड्राफ्ट i2p.sharedmimeinfo फ़ाइल देखें।

महत्वपूर्ण हैं .su3 प्रकार, और उन प्रकारों के पास
एक अद्वितीय प्रत्यय और मजबूत जादू संख्या परिभाषाएँ हैं।


## प्रवास

लागू नहीं।
