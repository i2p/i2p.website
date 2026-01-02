---
title: "I2P-Bote के bootstrap (आरंभीकरण) में मदद करके स्वयंसेवक कैसे बनें"
date: 2019-05-20
author: "idk"
description: "I2P-Bote को बूटस्ट्रैप करने में मदद करें!"
categories: ["development"]
---

लोगों को एक-दूसरे को निजी रूप से संदेश भेजने में मदद करने का एक आसान तरीका है I2P-Bote peer (समकक्ष) चलाना, जिसका उपयोग नए Bote उपयोगकर्ता अपने स्वयं के I2P-Bote peers को बूटस्ट्रैप करने के लिए कर सकते हैं।
दुर्भाग्य से, अब तक I2P-Bote bootstrap peer को सेटअप करने की प्रक्रिया जितनी स्पष्ट होनी चाहिए थी, उससे कहीं अधिक अस्पष्ट रही है।
वास्तव में, यह बेहद सरल है!

**I2P-bote क्या है?**

I2P-bote एक निजी संदेश प्रणाली है जो i2p पर बनी है, जिसमें अतिरिक्त विशेषताएँ हैं जो प्रेषित संदेशों के बारे में जानकारी का पता लगाना और भी कठिन बना देती हैं। इस वजह से, यह उच्च विलंब (latency) सहते हुए भी निजी संदेशों को सुरक्षित रूप से प्रेषित कर सकता है, और जब प्रेषक ऑफ़लाइन हो, तो संदेश भेजने के लिए किसी केंद्रीकृत रिले पर निर्भर नहीं करता। यह लगभग हर अन्य लोकप्रिय निजी संदेश प्रणाली के विपरीत है, जो या तो दोनों पक्षों का ऑनलाइन होना आवश्यक करती हैं, या फिर उन प्रेषकों की ओर से संदेश पहुँचाने के लिए किसी आंशिक-विश्वसनीय सेवा (semi-trusted service) पर निर्भर रहती हैं जो ऑफ़लाइन हो जाते हैं।

या, आसान शब्दों में: इसका उपयोग ई‑मेल की तरह किया जाता है, लेकिन इसमें ई‑मेल की गोपनीयता संबंधी कोई भी खामी नहीं होती।

**चरण एक: I2P-Bote स्थापित करें**

I2P-Bote एक i2p प्लगइन है, और इसे इंस्टॉल करना बहुत आसान है। मूल निर्देश [bote eepSite, bote.i2p](http://bote.i2p/install/) पर उपलब्ध हैं, लेकिन यदि आप उन्हें clearnet (सामान्य इंटरनेट) पर पढ़ना चाहते हैं, तो ये निर्देश bote.i2p के सौजन्य से प्रस्तुत हैं:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**चरण दो: अपने I2P-Bote नोड का base64 पता प्राप्त करें**

यह वह हिस्सा है जहाँ कोई व्यक्ति अटक सकता है, लेकिन घबराइए नहीं। निर्देश ढूँढना भले थोड़ा कठिन हो, पर वास्तव में यह आसान है और आपकी परिस्थितियों पर निर्भर करते हुए आपके पास कई उपकरण और विकल्प उपलब्ध हैं। जो लोग स्वयंसेवक के रूप में bootstrap nodes (आरंभिक कनेक्शन नोड्स) चलाने में मदद करना चाहते हैं, उनके लिए सबसे अच्छा तरीका bote tunnel द्वारा उपयोग की जाने वाली निजी कुंजी फ़ाइल से आवश्यक जानकारी प्राप्त करना है।

**कुंजियाँ कहाँ हैं?**

I2P-Bote अपनी गंतव्य कुंजियाँ एक टेक्स्ट फ़ाइल में संग्रहीत करता है, जो Debian पर `/var/lib/i2p/i2p-config/i2pbote/local_dest.key` में स्थित होती है। गैर-Debian प्रणालियों में, जहाँ i2p उपयोगकर्ता द्वारा स्थापित किया गया है, कुंजी `$HOME/.i2p/i2pbote/local_dest.key` में होगी, और Windows पर फ़ाइल `C:\ProgramData\i2p\i2pbote\local_dest.key` में होगी।

**विधि A: प्लेन-टेक्स्ट कुंजी को base64 destination में रूपांतरित करें**

एक प्लेन-टेक्स्ट कुंजी को base64 destination (गंतव्य पहचान) में बदलने के लिए, कुंजी को लेकर उसमें से केवल destination भाग को अलग करना होता है। इसे सही तरीके से करने के लिए, निम्नलिखित चरण अपनाने चाहिए:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

इन चरणों को आपके लिए करने के लिए कई एप्लिकेशन और स्क्रिप्ट उपलब्ध हैं। यहाँ उनमें से कुछ दिए गए हैं, लेकिन यह सूची पूर्ण नहीं है:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

ये क्षमताएँ कई I2P एप्लिकेशन विकास लाइब्रेरीज़ में भी उपलब्ध हैं।

**शॉर्टकट:**

चूँकि आपके bote नोड का स्थानीय destination (गंतव्य) एक DSA destination है, इसलिए सबसे तेज़ यही है कि local_dest.key फ़ाइल को पहले 516 बाइट्स तक ट्रंकेट कर दिया जाए। इसे आसानी से करने के लिए, Debian पर I2P के साथ I2P-Bote चलाते समय यह कमांड चलाएँ:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
या, यदि I2P आपके उपयोगकर्ता खाते के अंतर्गत स्थापित है:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**विधि B: एक लुकअप करें**

यदि यह आपको कुछ ज़्यादा काम जैसा लगे, तो आप base32 address (पता) को क्वेरी करके, और base32 address ढूंढने के लिए उपलब्ध किसी भी विधि का उपयोग करके, अपनी Bote कनेक्शन का base64 destination (गंतव्य) खोज सकते हैं। आपके Bote नोड का base32 address "Connection" पेज पर, bote प्लगिन एप्लिकेशन के अंतर्गत, [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network) पर उपलब्ध है।

**चरण तीन: हमसे संपर्क करें!**

**अपने नए नोड के साथ built-in-peers.txt फ़ाइल को अद्यतन करें**

अब जबकि आपके I2P-Bote नोड के लिए सही destination (I2P का सार्वजनिक पता) मिल गया है, अंतिम चरण यह है कि आप स्वयं को [I2P-Bote यहाँ](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) यहाँ की डिफ़ॉल्ट समकक्षों की सूची में जोड़ें। आप ऐसा रिपॉज़िटरी को fork करके, सूची में अपना नाम टिप्पणी के रूप में (commented out) जोड़कर, और उसके ठीक नीचे अपना 516-अक्षरों वाला destination लिखकर कर सकते हैं, जैसे:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
और एक pull request सबमिट करना। बस इतना ही, इसलिए i2p को सक्रिय, विकेंद्रीकृत, और विश्वसनीय बनाए रखने में मदद करें।
