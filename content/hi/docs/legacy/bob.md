---
title: "BOB - Basic Open Bridge"
description: "गंतव्य प्रबंधन के लिए अप्रचलित API"
slug: "bob"
aliases:
  - "/hi/docs/api/bob"
  - "/hi/docs/api/bob/"
  - "/hi/bob"
  - "/hi/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## चेतावनी - अप्रचलित

नए अनुप्रयोगों के उपयोग के लिए नहीं। BOB, जैसा कि यहाँ निर्दिष्ट है, केवल DSA-SHA1 signature प्रकार का समर्थन करता है। BOB को नए signature प्रकारों या अन्य उन्नत सुविधाओं का समर्थन करने के लिए विस्तारित नहीं किया जाएगा। नए अनुप्रयोगों को [SAM V3](/docs/api/samv3) का उपयोग करना चाहिए।

BOB समर्थन को Java I2P के नए इंस्टॉल से रिलीज़ 1.7.0 (2022-02) के अनुसार हटा दिया गया था। यह अभी भी Java I2P में काम करेगा जो मूल रूप से संस्करण 1.6.1 या पहले के रूप में इंस्टॉल किया गया था, अपडेट के बाद भी, लेकिन यह असमर्थित है और किसी भी समय टूट सकता है। BOB अभी भी i2pd द्वारा 2025-05 तक समर्थित है, लेकिन एप्लिकेशन को अभी भी उपरोक्त कारणों से SAMv3 में माइग्रेट करना चाहिए। यहाँ दस्तावेज़ित API के किसी भी एक्सटेंशन के लिए [i2pd दस्तावेज़](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) देखें जो i2pd द्वारा समर्थित हैं।

इस बिंदु पर, BOB के अधिकांश अच्छे विचारों को SAMv3 में शामिल कर लिया गया है, जिसमें अधिक सुविधाएं और अधिक वास्तविक-जगत का उपयोग है। BOB अभी भी कुछ installations पर काम कर सकता है (ऊपर देखें), लेकिन इसे SAMv3 में उपलब्ध उन्नत सुविधाएं नहीं मिल रही हैं और यह मूलतः असमर्थित है, i2pd को छोड़कर।

## BOB API के लिए भाषा लाइब्रेरीज़

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## अवलोकन

`KEYS` = keypair public+private, ये BASE64 हैं

`KEY` = सार्वजनिक कुंजी (public key), BASE64 भी

`ERROR` जैसा कि निहित है, संदेश `"ERROR "+DESCRIPTION+"\n"` वापस करता है, जहाँ `DESCRIPTION` वह है जो गलत हुआ।

`OK` वापस `"OK"` करता है, और यदि डेटा वापस करना है, तो यह उसी लाइन पर होता है। `OK` का मतलब है कि कमांड पूर्ण हो गई है।

`DATA` lines में वह जानकारी होती है जिसका आपने अनुरोध किया था। प्रत्येक request के लिए कई `DATA` lines हो सकती हैं।

**नोट:** help कमांड एकमात्र कमांड है जिसके लिए नियमों में अपवाद है... यह वास्तव में कुछ भी नहीं लौटा सकता! यह जानबूझकर है, क्योंकि help एक HUMAN कमांड है न कि APPLICATION कमांड।

## कनेक्शन और संस्करण

सभी BOB स्थिति आउटपुट लाइनों के रूप में होता है। लाइनें \\n या \\r\\n से समाप्त हो सकती हैं, जो सिस्टम पर निर्भर करता है। कनेक्शन पर, BOB दो लाइनें आउटपुट करता है:

```
BOB version
OK
```
वर्तमान संस्करण है: 00.00.10

ध्यान दें कि पिछले संस्करणों में अपरकेस hex अंक उपयोग किए गए थे और I2P versioning मानकों के अनुरूप नहीं थे। यह अनुशंसा की जाती है कि बाद के संस्करणों में केवल 0-9 अंक का उपयोग करें।

### संस्करण इतिहास

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## कमांड्स

**कृपया ध्यान दें:** कमांड की वर्तमान जानकारी के लिए कृपया बिल्ट-इन help कमांड का उपयोग करें। बस localhost 2827 पर telnet करें और help टाइप करें और आप प्रत्येक कमांड पर पूरा दस्तावेज़ीकरण प्राप्त कर सकते हैं।

Commands कभी भी अप्रचलित या बदले नहीं जाते, हालांकि समय-समय पर नए commands जोड़े जाते हैं।

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
एक बार सेट अप हो जाने पर, सभी TCP sockets आवश्यकतानुसार block कर सकते हैं और करेंगे, और command channel से/को किसी अतिरिक्त messages की आवश्यकता नहीं है। यह router को stream की गति को नियंत्रित करने की अनुमति देता है बिना OOM के साथ फट जाने के जैसा कि SAM करता है जब यह एक socket में या बाहर कई streams को धकेलने की कोशिश करते समय घुट जाता है -- यह scale नहीं कर सकता जब आपके पास बहुत सारे connections हों!

इस विशेष interface के बारे में जो बात अच्छी है वह यह है कि इससे interface करने के लिए कुछ भी लिखना SAM की तुलना में बहुत बहुत आसान है। सेट अप के बाद कोई अन्य प्रोसेसिंग करने की जरूरत नहीं है। इसका configuration इतना सरल है कि बहुत सरल tools जैसे nc (netcat) का उपयोग किसी application को point करने के लिए किया जा सकता है। इसका मूल्य यह है कि कोई व्यक्ति किसी application के लिए up और down times को schedule कर सकता है, और ऐसा करने के लिए application को बदलने या उस application को बंद करने की भी जरूरत नहीं है। इसके बजाय, आप सचमुच destination को "unplug" कर सकते हैं, और इसे फिर से "plug in" कर सकते हैं। जब तक bridge को up करते समय same IP/port addresses और destination keys का उपयोग किया जाता है, normal TCP application को कोई फर्क नहीं पड़ेगा, और वह notice नहीं करेगा। यह बस fooled हो जाएगा -- destinations reachable नहीं हैं, और कुछ भी अंदर नहीं आ रहा।

## उदाहरण

निम्नलिखित उदाहरण के लिए, हम दो destinations के साथ एक बहुत सरल local loopback connection सेटअप करेंगे। Destination "mouth" INET superserver daemon से CHARGEN service होगी। Destination "ear" एक local port होगा जिसमें आप telnet कर सकते हैं, और सुंदर ASCII test की धारा देख सकते हैं।

### उदाहरण सत्र संवाद

सरल telnet 127.0.0.1 2827 काम करता है।

- A = एप्लिकेशन
- C = BOB का कमांड रिस्पॉन्स।

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**उपरोक्त DESTINATION KEY को नोट कर लें, आपकी अलग होगी!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
इस बिंदु पर, कोई त्रुटि नहीं थी, "mouth" के nickname के साथ एक destination सेट अप हो गया है। जब आप प्रदान किए गए destination से संपर्क करते हैं, तो आप वास्तव में `19/TCP` पर `CHARGEN` service से जुड़ते हैं।

अब दूसरे हिस्से के लिए, ताकि हम वास्तव में इस destination से संपर्क कर सकें।

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
अब हमें बस 127.0.0.1, port 37337 पर telnet करना है, destination key या address book से host address भेजना है जिससे हम संपर्क करना चाहते हैं। इस मामले में, हम "mouth" से संपर्क करना चाहते हैं, हमें बस key paste करनी है और यह काम हो जाता है।

**नोट:** command channel में "quit" कमांड SAM की तरह tunnels को disconnect नहीं करता है।

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
इस spew के कुछ virtual miles के बाद, `Control-]` दबाएं

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
यहाँ जो हुआ वह यह है...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
आप I2P SITES से भी जुड़ सकते हैं!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
काफी बेहतरीन है, है ना? यदि आप चाहें तो कुछ अन्य प्रसिद्ध I2P SITES आज़माएं, या फिर कुछ गैर-मौजूद साइटें भी, ताकि आप समझ सकें कि विभिन्न स्थितियों में कैसा आउटपुट मिलने की उम्मीद करनी चाहिए। अधिकतर, यह सुझाव दिया जाता है कि आप किसी भी त्रुटि संदेश को नज़रअंदाज़ करें। ये एप्लिकेशन के लिए निरर्थक होंगे, और केवल मानव डिबगिंग के लिए प्रस्तुत किए गए हैं।

### सफाई करना

अब जब हमारा सभी destinations के साथ काम पूरा हो गया है, तो आइए उन्हें बंद कर देते हैं।

पहले, आइए देखते हैं कि हमारे पास कौन से destination nicknames हैं।

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
ठीक है, वे वहाँ हैं। पहले, आइए "mouth" को हटाते हैं।

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
अब "ear" को हटाने के लिए, ध्यान दें कि यह तब होता है जब आप बहुत तेज़ी से टाइप करते हैं, और यह आपको दिखाता है कि सामान्य ERROR संदेश कैसे दिखते हैं।

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## शांत मोड

मैं bridge के receiver end का उदाहरण दिखाने की परेशानी नहीं उठाऊंगा क्योंकि यह बहुत सरल है। इसके लिए दो संभावित सेटिंग्स हैं, और इसे "quiet" command से toggle किया जाता है।

डिफ़ॉल्ट शांत (quiet) नहीं है, और आपके listening socket में आने वाला पहला डेटा वह destination है जो संपर्क स्थापित कर रहा है। यह एक single line है जिसमें BASE64 address होता है जिसके बाद newline आता है। उसके बाद सब कुछ application के वास्तविक उपयोग के लिए होता है।

quiet mode में, इसे एक नियमित Internet कनेक्शन के रूप में समझें। कोई अतिरिक्त डेटा बिल्कुल नहीं आता। यह बिल्कुल वैसा ही है जैसे आप सादे रूप से नियमित Internet से जुड़े हों। यह mode एक प्रकार की पारदर्शिता की अनुमति देता है जो router console tunnel settings pages पर उपलब्ध है, ताकि आप BOB का उपयोग करके किसी destination को web server की ओर point कर सकें, उदाहरण के लिए, और आपको web server में कोई भी संशोधन करने की आवश्यकता नहीं होगी।

## BOB के फायदे

इसके लिए BOB का उपयोग करने का फायदा वही है जिस पर हमने पहले चर्चा की थी। आप एप्लिकेशन के लिए यादृच्छिक अपटाइम शेड्यूल कर सकते हैं, किसी अलग मशीन पर रीडायरेक्ट कर सकते हैं, आदि। इसका एक उपयोग router-to-destination अपनेस गेसिंग को गड़बड़ाने की कोशिश करना हो सकता है। आप सेवाओं पर यादृच्छिक अप और डाउन टाइम बनाने के लिए पूरी तरह से अलग प्रक्रिया के साथ destination को रोक और शुरू कर सकते हैं। इस तरह आप केवल ऐसी सेवा से संपर्क करने की क्षमता को रोक रहे होंगे, और इसे बंद करके दोबारा शुरू करने की परेशानी नहीं उठानी पड़ेगी। आप अपडेट करते समय अपने LAN पर किसी अलग मशीन पर रीडायरेक्ट और पॉइंट कर सकते हैं, या जो चल रहा है उसके आधार पर बैकअप मशीनों के सेट पर पॉइंट कर सकते हैं, आदि। केवल आपकी कल्पना ही सीमित करती है कि आप BOB के साथ क्या कर सकते हैं।
