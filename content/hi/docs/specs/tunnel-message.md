---
title: "Tunnel संदेश विनिर्देश"
description: "I2P में tunnel संदेशों के प्रारूप के लिए विनिर्देश"
slug: "tunnel-message"
aliases:
  - "/hi/docs/legacy/tunnel-message"
  - "/hi/docs/legacy/tunnel-message/"
  - "/hi/tunnel_message_spec"
  - "/hi/tunnel_message_spec/"
category: "डिज़ाइन"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## अवलोकन

यह दस्तावेज़ tunnel संदेशों के प्रारूप को निर्दिष्ट करता है। tunnel के बारे में सामान्य जानकारी के लिए [tunnel दस्तावेज़](/docs/specs/tunnel-implementation) देखें।

## संदेश पूर्व-प्रसंस्करण

एक *tunnel gateway* प्रवेश द्वार है, या tunnel का पहला hop है। outbound tunnel के लिए, gateway tunnel का निर्माता होता है। inbound tunnel के लिए, gateway tunnel के निर्माता के विपरीत छोर पर होता है।

एक gateway *पूर्व-प्रसंस्करण* करता है [I2NP](/docs/specs/i2np) संदेशों का उन्हें खंडित करके और tunnel संदेशों में संयोजित करके।

जबकि I2NP संदेश 0 से लगभग 64 KB तक के परिवर्तनीय आकार के होते हैं, tunnel संदेश निश्चित आकार के होते हैं, लगभग 1 KB के। निश्चित संदेश आकार कई प्रकार के हमलों को सीमित करता है जो संदेश आकार को देखकर संभव होते हैं।

tunnel संदेश बनाए जाने के बाद, उन्हें [tunnel documentation](/docs/specs/tunnel-implementation) में वर्णित तरीके से एन्क्रिप्ट किया जाता है।

### Tunnel संदेश (एन्क्रिप्टेड)

ये एन्क्रिप्शन के बाद tunnel डेटा संदेश की सामग्री हैं।

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 बाइट्स। अगले hop की ID, गैर-शून्य।

**IV** :: : 16 bytes। प्रारंभिक वेक्टर।

**एन्क्रिप्टेड डेटा** :: : 1008 bytes। एन्क्रिप्टेड tunnel संदेश।

**कुल आकार: 1028 बाइट्स**

### Tunnel Message (डिक्रिप्टेड)

ये tunnel data message की सामग्री है जब वह decrypt हो जाता है।

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 बाइट्स। अगले hop का ID, गैर-शून्य।

**IV** :: : 16 bytes. प्रारंभिक वेक्टर।

**Checksum** :: : 4 बाइट्स। (संदेश की सामग्री (शून्य बाइट के बाद) + IV) के SHA256 hash के पहले 4 बाइट्स।

**Nonzero padding** :: : 0 या अधिक बाइट्स। पैडिंग के लिए रैंडम nonzero डेटा।

**Zero** :: : 1 byte. मान 0x00।

**डिलीवरी निर्देश** :: TunnelMessageDeliveryInstructions : लंबाई अलग-अलग होती है लेकिन आमतौर पर 7, 39, 43, या 47 बाइट्स होती है। fragment और fragment के लिए routing को इंगित करता है।

**संदेश खंड** :: : 1 से 996 बाइट्स, वास्तविक अधिकतम वितरण निर्देश के आकार पर निर्भर करता है। एक आंशिक या पूर्ण I2NP संदेश।

**कुल आकार: 1028 bytes**

#### नोट्स

- पैडिंग, यदि कोई है, तो instruction/message pairs से पहले होनी चाहिए। अंत में पैडिंग के लिए कोई प्रावधान नहीं है।
- checksum पैडिंग या zero byte को कवर नहीं करता। पहले delivery instructions से शुरू होने वाले message को लें, IV को concatenate करें, और उसका Hash लें।

## Tunnel संदेश वितरण निर्देश

निर्देश एक single control byte के साथ encoded होते हैं, जिसके बाद कोई भी आवश्यक अतिरिक्त जानकारी होती है। उस control byte में पहला bit (MSB) निर्धारित करता है कि header के बाकी हिस्से की व्याख्या कैसे की जाए - यदि यह set नहीं है, तो message या तो fragmented नहीं है या यह message का पहला fragment है। यदि यह set है, तो यह एक follow on fragment है।

यह specification केवल Tunnel Messages के अंदर Delivery Instructions के लिए है। ध्यान दें कि "Delivery Instructions" का उपयोग Garlic Cloves के अंदर भी किया जाता है, जहाँ format काफी अलग है। विवरण के लिए [I2NP documentation](/docs/specs/i2np#garlicclovedeliveryinstructions) देखें। Garlic Clove Delivery Instructions के लिए निम्नलिखित specification का उपयोग न करें!

### पहले Fragment की डिलीवरी निर्देश

यदि पहले बाइट का MSB 0 है, तो यह एक प्रारंभिक I2NP संदेश खंड है, या एक पूर्ण (अविभाजित) I2NP संदेश है, और निर्देश हैं:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 byte. Bit order: 76543210   - bit 7: प्रारंभिक fragment या unfragmented संदेश को निर्दिष्ट करने के लिए 0   - bits 6-5: delivery type

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: देरी शामिल? अनिम्प्लिमेंटेड, हमेशा 0। यदि 1 है, तो एक देरी बाइट शामिल है।
  - bit 3: खंडित? यदि 0 है, तो संदेश खंडित नहीं है, जो आगे है वह संपूर्ण संदेश है। यदि 1 है, तो संदेश खंडित है, और निर्देशों में एक Message ID शामिल है।
  - bit 2: विस्तृत विकल्प? अनिम्प्लिमेंटेड, हमेशा 0। यदि 1 है, तो विस्तृत विकल्प शामिल हैं।
  - bits 1-0: आरक्षित, भविष्य के उपयोग के साथ संगतता के लिए 0 पर सेट

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 बाइट्स। वैकल्पिक, उपस्थित यदि delivery type TUNNEL है। गंतव्य tunnel ID, शून्य नहीं।

**To Hash** :: : 32 bytes। वैकल्पिक, उपस्थित यदि delivery type ROUTER या TUNNEL है। यदि ROUTER है, तो router का SHA256 Hash। यदि TUNNEL है, तो gateway router का SHA256 Hash।

**Delay** :: : 1 byte। वैकल्पिक, यदि delay included flag सेट है तो मौजूद। tunnel संदेशों में: अनुप्रयुक्त नहीं, कभी मौजूद नहीं; मूल विशिष्टता: bit 7: प्रकार (0 = strict, 1 = randomized), bits 6-0: delay exponent (2^value मिनट)।

**Message ID** :: : 4 bytes. वैकल्पिक, मौजूद है यदि यह संदेश 2 या अधिक fragments का पहला है (यानी यदि fragmented bit 1 है)। एक ID जो सभी fragments को एक ही संदेश से संबंधित होने की विशिष्ट पहचान करता है (वर्तमान implementation I2NPMessageHeader.msg_id का उपयोग करता है)।

**Extended Options** :: : 2 या अधिक bytes। वैकल्पिक, केवल तभी उपस्थित होता है जब extend options flag सेट हो। अभी तक लागू नहीं किया गया, कभी उपस्थित नहीं होता; मूल specification: एक byte length और फिर उतने bytes।

**size** :: : 2 बाइट्स। उसके बाद आने वाले fragment की लंबाई। मान्य मान: tunnel message में 1 से लगभग 960 तक।

**कुल लंबाई:** सामान्य लंबाई है: - LOCAL डिलीवरी के लिए 3 बाइट्स (tunnel संदेश) - ROUTER डिलीवरी के लिए 35 बाइट्स या TUNNEL डिलीवरी के लिए 39 बाइट्स (खंडित नहीं किया गया tunnel संदेश) - ROUTER डिलीवरी के लिए 39 बाइट्स या TUNNEL डिलीवरी के लिए 43 बाइट्स (पहला खंड)

### अनुवर्ती खंड वितरण निर्देश

यदि पहले बाइट का MSB 1 है, तो यह एक follow-on fragment है, और निर्देश हैं:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte। Bit order: 76543210। Binary 1nnnnnnd:   - bit 7: 1 यह दर्शाने के लिए कि यह एक follow-on fragment है   - bits 6-1: nnnnnn 6 bit fragment number है 1 से 63 तक   - bit 0: d अंतिम fragment को दर्शाने के लिए 1 है, अन्यथा 0

**Message ID** :: : 4 बाइट्स। उस fragment sequence की पहचान करता है जिससे यह fragment संबंधित है। यह एक initial fragment के message ID से मेल खाएगा (एक fragment जिसमें flag bit 7 को 0 पर सेट किया गया हो और flag bit 3 को 1 पर सेट किया गया हो)।

**size** :: : 2 बाइट्स। इसके बाद आने वाले fragment की लंबाई। वैध मान: 1 से 996।

**कुल लंबाई: 7 बाइट्स**

## नोट्स

### I2NP संदेश अधिकतम आकार

जबकि अधिकतम I2NP संदेश आकार नाममात्र से 64 KB है, आकार I2NP संदेशों को कई 1 KB tunnel संदेशों में विभाजित करने की विधि द्वारा और भी सीमित है। अधिकतम fragments की संख्या 64 है, और प्रारंभिक fragment tunnel संदेश की शुरुआत में पूरी तरह से संरेखित नहीं हो सकता। इसलिए संदेश को नाममात्र से 63 fragments में फिट होना चाहिए।

प्रारंभिक fragment का अधिकतम आकार 956 bytes है (TUNNEL delivery mode मानते हुए); follow-on fragment का अधिकतम आकार 996 bytes है। इसलिए अधिकतम आकार लगभग 956 + (62 * 996) = 62708 bytes, या 61.2 KB है।

### क्रमबद्धता, बैचिंग, पैकिंग

Tunnel संदेश गिराए या पुनर्क्रमित हो सकते हैं। Tunnel gateway, जो tunnel संदेश बनाता है, I2NP संदेशों को खंडित करने और खंडों को tunnel संदेशों में कुशलता से पैक करने के लिए किसी भी batching, mixing, या reordering रणनीति को लागू करने के लिए स्वतंत्र है। सामान्यतः, एक अनुकूलतम पैकिंग संभव नहीं है ("packing problem")। Gateway विभिन्न देरी और पुनर्क्रमण रणनीतियों को लागू कर सकते हैं।

### कवर ट्रैफिक

Tunnel संदेश केवल padding हो सकते हैं (यानी कोई delivery निर्देश या message fragments बिल्कुल नहीं) cover traffic के लिए। यह अभी तक implemented नहीं है।

## संदर्भ

- **[I2NP]** [I2NP Protocol](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Tunnel Implementation](/docs/specs/tunnel-implementation)
