---
title: "BOB – बेसिक ओपन ब्रिज"
description: "गंतव्य प्रबंधन के लिए अप्रचलित API (अप्रचलित)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **चेतावनी:** BOB (I2P का एक पुराना API ब्रिज) केवल पुराने DSA-SHA1 हस्ताक्षर प्रकार का समर्थन करता है। Java I2P ने **1.7.0 (2022-02)** में BOB को शामिल करना बंद कर दिया; यह केवल उन इंस्टॉलेशनों पर मौजूद है जो 1.6.1 या उससे पहले से शुरू किए गए थे और कुछ i2pd (C++ आधारित I2P router का इम्प्लीमेंटेशन) बिल्ड्स पर। नई अनुप्रयोगों को [SAM v3](/docs/api/samv3/) का उपयोग करना अनिवार्य है।

## प्रोग्रामिंग भाषा बाइंडिंग्स

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## प्रोटोकॉल नोट्स

- `KEYS` एक base64 गंतव्य (पब्लिक + प्राइवेट कुंजियाँ) को दर्शाता है.  
- `KEY` एक base64 पब्लिक कुंजी है.  
- `ERROR` प्रतिक्रियाएँ इस रूप में होती हैं: `ERROR <description>\n`.  
- `OK` कमांड के पूर्ण होने को दर्शाता है; वैकल्पिक डेटा उसी पंक्ति में आगे आता है.  
- `DATA` लाइनें अंतिम `OK` से पहले अतिरिक्त आउटपुट स्ट्रीम करती हैं.

`help` कमांड एकमात्र अपवाद है: “ऐसा कोई कमांड नहीं है” का संकेत देने के लिए यह कुछ भी नहीं लौटा सकता है।

## कनेक्शन बैनर

BOB (I2P का एक नियंत्रण इंटरफ़ेस) नई पंक्ति पर समाप्त होने वाली ASCII पंक्तियों का उपयोग करता है (LF या CRLF)। कनेक्शन स्थापित होने पर यह निम्नलिखित प्रेषित करता है:

```
BOB <version>
OK
```
वर्तमान संस्करण: `00.00.10`। पहले के बिल्ड बड़े अक्षरों वाले हेक्स अंकों और गैर-मानक क्रमांकन का उपयोग करते थे।

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## मुख्य कमांड

> पूर्ण कमांड विवरण के लिए, `telnet localhost 2827` से कनेक्ट करें और `help` चलाएँ।

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## अप्रचलन सारांश

- BOB (I2P का पुराना socket-आधारित control API) में आधुनिक हस्ताक्षर प्रकार, एन्क्रिप्टेड LeaseSets (I2P में गंतव्य तक पहुँचने हेतु tunnel endpoints युक्त डेटा-संरचना), या ट्रांसपोर्ट सुविधाओं का समर्थन नहीं है।
- API फ्रीज़ कर दी गई है; नए कमांड नहीं जोड़े जाएंगे।
- जो एप्लिकेशन अभी भी BOB पर निर्भर हैं, उन्हें यथाशीघ्र SAM v3 (I2P का अनुशंसित एप्लिकेशन API) पर माइग्रेट कर लेना चाहिए।
