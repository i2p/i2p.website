---
title: "I2P के लिए Git Bundles"
description: "बड़े रिपॉजिटरी को git bundle और BitTorrent के साथ fetch करना और वितरित करना"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

जब नेटवर्क परिस्थितियाँ `git clone` को अविश्वसनीय बना देती हैं, तो आप **git bundles** के रूप में repositories को BitTorrent या किसी अन्य फ़ाइल ट्रांसपोर्ट के माध्यम से वितरित कर सकते हैं। एक bundle एक single file होती है जिसमें पूरी repository history होती है। एक बार डाउनलोड हो जाने के बाद, आप इससे locally fetch करते हैं और फिर upstream remote पर वापस switch करते हैं।

## 1. शुरू करने से पहले

बंडल जनरेट करने के लिए एक **पूर्ण** Git clone की आवश्यकता होती है। `--depth 1` के साथ बनाए गए Shallow clones चुपचाप टूटे हुए बंडल उत्पन्न करेंगे जो काम करते हुए प्रतीत होते हैं लेकिन जब अन्य लोग उनका उपयोग करने का प्रयास करते हैं तो विफल हो जाते हैं। हमेशा किसी विश्वसनीय स्रोत (GitHub पर [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), I2P Gitea instance पर [i2pgit.org](https://i2pgit.org), या I2P के माध्यम से `git.idk.i2p`) से fetch करें और बंडल बनाने से पहले किसी भी shallow clone को full clone में बदलने के लिए आवश्यकता होने पर `git fetch --unshallow` चलाएं।

यदि आप केवल एक मौजूदा bundle का उपयोग कर रहे हैं, तो बस इसे डाउनलोड करें। किसी विशेष तैयारी की आवश्यकता नहीं है।

## 2. एक बंडल डाउनलोड करना

### Obtaining the Bundle File

I2PSnark (I2P में अंतर्निहित torrent क्लाइंट) या I2P प्लगइन के साथ BiglyBT जैसे अन्य I2P-संगत क्लाइंट का उपयोग करके BitTorrent के माध्यम से बंडल फ़ाइल डाउनलोड करें।

**महत्वपूर्ण**: I2PSnark केवल उन्हीं torrents के साथ काम करता है जो विशेष रूप से I2P नेटवर्क के लिए बनाए गए हैं। मानक clearnet torrents संगत नहीं हैं क्योंकि I2P, IP addresses और ports के बजाय Destinations (387+ byte addresses) का उपयोग करता है।

बंडल फ़ाइल का स्थान आपके I2P इंस्टॉलेशन प्रकार पर निर्भर करता है:

- **उपयोगकर्ता/मैनुअल इंस्टॉलेशन** (Java installer के साथ इंस्टॉल किया गया): `~/.i2p/i2psnark/`
- **सिस्टम/डेमॉन इंस्टॉलेशन** (apt-get या package manager के माध्यम से इंस्टॉल किया गया): `/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT उपयोगकर्ता डाउनलोड की गई फ़ाइलें अपनी कॉन्फ़िगर की गई डाउनलोड निर्देशिका में पाएंगे।

### Cloning from the Bundle

**मानक विधि** (अधिकांश मामलों में काम करती है):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
यदि आपको `fatal: multiple updates for ref` errors का सामना करना पड़े (Git 2.21.0 और बाद के संस्करणों में एक ज्ञात समस्या जब global Git config में विरोधाभासी fetch refspecs हों), तो manual initialization approach का उपयोग करें:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
वैकल्पिक रूप से, आप `--update-head-ok` फ्लैग का उपयोग कर सकते हैं:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### बंडल फ़ाइल प्राप्त करना

बंडल से क्लोन करने के बाद, अपने क्लोन को लाइव रिमोट की ओर इंगित करें ताकि भविष्य की fetches I2P या clearnet के माध्यम से हों:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
या क्लियरनेट एक्सेस के लिए:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
I2P SSH एक्सेस के लिए, आपको अपने I2P router कंसोल में एक SSH क्लाइंट tunnel कॉन्फ़िगर करना होगा (आमतौर पर पोर्ट 7670) जो `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p` की ओर इशारा करता हो। यदि गैर-मानक पोर्ट का उपयोग कर रहे हैं:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### बंडल से क्लोनिंग

सुनिश्चित करें कि आपकी repository **complete clone** के साथ पूरी तरह से अप-टू-डेट है (shallow नहीं):

```bash
git fetch --all
```
यदि आपके पास shallow clone है, तो इसे पहले convert करें:

```bash
git fetch --unshallow
```
### लाइव रिमोट पर स्विच करना

**Ant build target का उपयोग** (I2P source tree के लिए अनुशंसित):

```bash
ant git-bundle
```
यह `i2p.i2p.bundle` (bundle फ़ाइल) और `i2p.i2p.bundle.torrent` (BitTorrent metadata) दोनों बनाता है।

**git bundle का सीधे उपयोग करना**:

```bash
git bundle create i2p.i2p.bundle --all
```
अधिक चयनात्मक बंडल के लिए:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

वितरित करने से पहले हमेशा bundle को सत्यापित करें:

```bash
git bundle verify i2p.i2p.bundle
```
यह पुष्टि करता है कि bundle वैध है और किसी भी आवश्यक prerequisite commits को दिखाता है।

### पूर्वापेक्षाएँ

बंडल और इसके टोरेंट मेटाडेटा को अपनी I2PSnark डायरेक्टरी में कॉपी करें:

**उपयोगकर्ता इंस्टॉलेशन के लिए**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**सिस्टम इंस्टॉलेशन के लिए**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark स्वचालित रूप से .torrent फाइलों का पता लगाता है और सेकंडों में लोड कर देता है। सीडिंग शुरू करने के लिए [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) पर वेब इंटरफेस एक्सेस करें।

## 4. Creating Incremental Bundles

समय-समय पर अपडेट के लिए, केवल अंतिम बंडल के बाद के नए commits वाले incremental bundles बनाएं:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
उपयोगकर्ता incremental bundle से fetch कर सकते हैं यदि उनके पास पहले से base repository है:

```bash
git fetch /path/to/update.bundle
```
हमेशा सत्यापित करें कि incremental bundles अपेक्षित prerequisite commits दिखाते हैं:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

एक बार जब आपके पास bundle से एक कार्यशील repository हो जाए, तो इसे किसी भी अन्य Git clone की तरह ट्रीट करें:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
या सरल वर्कफ़्लो के लिए:

```bash
git fetch origin
git pull origin master
```
## 3. बंडल बनाना

- **लचीला वितरण**: बड़े repositories को BitTorrent के माध्यम से साझा किया जा सकता है, जो स्वचालित रूप से retries, piece verification, और resume को संभालता है।
- **Peer-to-peer bootstrap**: नए योगदानकर्ता I2P network पर निकटवर्ती peers से अपना clone bootstrap कर सकते हैं, फिर Git hosts से सीधे incremental changes प्राप्त कर सकते हैं।
- **सर्वर लोड में कमी**: Mirrors समय-समय पर bundles प्रकाशित कर सकते हैं ताकि live Git hosts पर दबाव कम हो, विशेष रूप से बड़े repositories या धीमी network स्थितियों के लिए उपयोगी।
- **Offline transport**: Bundles किसी भी file transport (USB drives, direct transfers, sneakernet) पर काम करते हैं, न कि केवल BitTorrent पर।

बंडल लाइव रिमोट को प्रतिस्थापित नहीं करते हैं। वे केवल शुरुआती clone या बड़े अपडेट के लिए एक अधिक लचीली bootstrapping विधि प्रदान करते हैं।

## 7. Troubleshooting

### बंडल उत्पन्न करना

**समस्या**: Bundle निर्माण सफल होता है लेकिन अन्य bundle से clone नहीं कर सकते।

**कारण**: आपका स्रोत क्लोन shallow है (`--depth` के साथ बनाया गया)।

**समाधान**: बंडल बनाने से पहले फुल clone में परिवर्तित करें:

```bash
git fetch --unshallow
```
### आपके बंडल का सत्यापन

**समस्या**: बंडल से क्लोन करते समय `fatal: multiple updates for ref`।

**कारण**: Git 2.21.0+ में `~/.gitconfig` के global fetch refspecs के साथ विरोध है।

**समाधान**: 1. मैन्युअल इनिशियलाइज़ेशन का उपयोग करें: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. `--update-head-ok` फ्लैग का उपयोग करें: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. conflicting कॉन्फ़िग को हटाएं: `git config --global --unset remote.origin.fetch`

### I2PSnark के माध्यम से वितरण

**समस्या**: `git bundle verify` लापता पूर्वापेक्षाओं की रिपोर्ट करता है।

**कारण**: इंक्रीमेंटल bundle या अपूर्ण स्रोत क्लोन।

**समाधान**: या तो आवश्यक कमिट्स को फेच करें या पहले बेस बंडल का उपयोग करें, फिर इंक्रीमेंटल अपडेट लागू करें।
