---
title: "उपयोगकर्ताओं के लिए I2P के माध्यम से Git"
date: 2020-03-06
author: "idk"
description: "I2P पर Git"
categories: ["development"]
---

I2P Tunnel के माध्यम से git अभिगम स्थापित करने के लिए ट्यूटोरियल। यह tunnel I2P पर एकल git सेवा के लिए आपके प्रवेश बिंदु के रूप में कार्य करेगी। यह I2P को monotone से Git में स्थानांतरित करने के समग्र प्रयास का एक हिस्सा है।

## सबसे पहले: यह जानें कि सेवा जनता को कौन-सी क्षमताएँ प्रदान करती है

यह इस बात पर निर्भर करता है कि git सेवा कैसे कॉन्फ़िगर की गई है; वह सभी सेवाएँ एक ही पते पर उपलब्ध करा भी सकती है या नहीं भी।

git.idk.i2p के मामले में, एक सार्वजनिक HTTP URL उपलब्ध है, और आपके Git SSH क्लाइंट के लिए कॉन्फ़िगर करने हेतु एक SSH URL भी है। दोनों में से किसी का भी उपयोग push या pull के लिए किया जा सकता है, लेकिन SSH की अनुशंसा की जाती है।

## सबसे पहले: किसी Git सेवा पर एक खाता बनाएँ

दूरस्थ git सेवा पर अपनी रिपॉजिटरीज़ बनाने के लिए, उस सेवा पर एक उपयोगकर्ता खाता बनाएँ। बेशक, रिपॉजिटरीज़ को स्थानीय रूप से बनाना और उन्हें किसी दूरस्थ git सेवा पर पुश करना भी संभव है, लेकिन अधिकांश सेवाएँ एक खाता मांगेंगी और आपसे सर्वर पर रिपॉजिटरी के लिए space (स्थान) बनाने को कहेंगी।

## दूसरा: परीक्षण हेतु एक प्रोजेक्ट बनाएँ

To make sure the setup process works, it helps to make a repository to test with from the server. Browse to the i2p-hackers/i2p.i2p repository and fork it to your account.

## तीसरा: अपना git क्लाइंट tunnel सेट अप करें

किसी सर्वर पर पढ़ने-लिखने की पहुँच पाने के लिए, आपको अपने SSH क्लाइंट के लिए एक tunnel सेट अप करना होगा। अगर आपको केवल HTTP/S क्लोनिंग (केवल-पढ़ने की) चाहिए, तो आप यह सब छोड़ सकते हैं और बस http_proxy environment variable का उपयोग करके git को इस तरह कॉन्फ़िगर कर सकते हैं कि वह पहले से कॉन्फ़िगर किए गए I2P HTTP Proxy का उपयोग करे। उदाहरण के लिए:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
SSH एक्सेस के लिए, http://127.0.0.1:7657/i2ptunnelmgr से "New Tunnel Wizard" लॉन्च करें और Git सेवा के SSH base32 पते की ओर इंगित करने वाला एक client tunnel सेट करें।

## चौथा: क्लोन करने का प्रयास करें

अब आपका tunnel पूरी तरह कॉन्फ़िगर हो चुका है, आप SSH के जरिए क्लोन करने का प्रयास कर सकते हैं:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
आपको ऐसा त्रुटि संदेश मिल सकता है जिसमें दूरस्थ पक्ष (remote end) अप्रत्याशित रूप से कनेक्शन बंद कर दे। दुर्भाग्यवश git अभी भी पुनरारंभ योग्य क्लोनिंग का समर्थन नहीं करता। जब तक ऐसा नहीं होता, इसे संभालने के कुछ अपेक्षाकृत आसान तरीके हैं। पहला और सबसे आसान तरीका है कि कम गहराई (shallow depth) के साथ क्लोन करने की कोशिश करें:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
एक बार जब आप shallow clone (उथला क्लोन) कर लें, तो repo directory (रेपो निर्देशिका) में जाकर और चलाकर आप शेष को पुनरारंभ-सक्षम तरीके से प्राप्त कर सकते हैं:

```
git fetch --unshallow
```
इस समय, आपके पास अभी तक आपकी सभी branches नहीं हैं। आप उन्हें यह कमांड चलाकर प्राप्त कर सकते हैं:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## डेवलपर्स के लिए सुझाया गया कार्यप्रवाह

Revision control (संस्करण नियंत्रण) तब सबसे अच्छा काम करता है जब आप इसे अच्छी तरह इस्तेमाल करते हैं! हम जोर देकर सलाह देते हैं कि fork-first, feature-branch workflow (पहले fork करें और हर फ़ीचर के लिए अलग ब्रांच पर काम करें) अपनाएँ:

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```