---
title: "I2NP अवलोकन"
description: "I2P नेटवर्क प्रोटोकॉल (I2NP) का अवलोकन - संदेश प्रारूप, प्रकार, प्राथमिकताएँ, और आकार सीमाएँ।"
slug: "i2np-overview"
aliases:
  - "/hi/docs/protocol/i2np"
  - "/hi/docs/protocol/i2np/"
  - "/hi/i2np"
  - "/hi/i2np/"
category: "प्रोटोकॉल"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## अवलोकन

I2P नेटवर्क प्रोटोकॉल (I2NP), जो I2CP तथा विभिन्न I2P परिवहन प्रोटोकॉल के बीच स्थित है, राउटरों के बीच संदेशों के मार्गदर्शन और मिश्रण के साथ-साथ उस पीयर के साथ संचार के लिए किन परिवहन प्रोटोकॉल का उपयोग करना है, इसके चयन का प्रबंधन करता है, जिसके लिए कई सामान्य परिवहन प्रोटोकॉल समर्थित हैं।

## I2NP परिभाषा

I2NP (I2P नेटवर्क प्रोटोकॉल) संदेशों का उपयोग एक-हॉप, राउटर-से-राउटर, पॉइंट-टू-पॉइंट संदेशों के लिए किया जा सकता है। संदेशों को अन्य संदेशों में एन्क्रिप्ट और लपेटकर, उन्हें अंतिम गंतव्य तक कई हॉप्स के माध्यम से सुरक्षित तरीके से भेजा जा सकता है। प्राथमिकता का उपयोग केवल उत्पत्ति स्थल पर स्थानीय स्तर पर किया जाता है, अर्थात आउटबाउंड डिलीवरी के लिए कतार में लगाते समय।

नीचे सूचीबद्ध प्राथमिकताएँ वर्तमान नहीं हो सकती हैं और परिवर्तन के अधीन हैं। प्राथमिकता कतार लागूकरण में भिन्नता हो सकती है।

## संदेश प्रारूप {#format}

निम्नलिखित तालिका NTCP में उपयोग किए जाने वाले पारंपरिक 16-बाइट हेडर को निर्दिष्ट करती है। SSU और NTCP2 ट्रांसपोर्ट संशोधित हेडर का उपयोग करते हैं।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Type</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unique ID</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Checksum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 - 61.2KB</td>
</tr>
</table>
हालांकि अधिकतम पेलोड आकार औपचारिक रूप से 64KB है, आकार को [टनल लागूकरण पृष्ठ](/docs/specs/tunnel-implementation/) पर वर्णित आई2एनपी संदेशों को कई 1KB टनल संदेशों में खंडित करने की विधि द्वारा और अधिक सीमित किया जाता है।

अधिकतम फ्रैगमेंट्स की संख्या 64 है, और संदेश पूरी तरह संरेखित नहीं हो सकता है, इसलिए संदेश को आम तौर पर 63 फ्रैगमेंट्स में फिट होना चाहिए।

एक प्रारंभिक खंड का अधिकतम आकार 956 बाइट्स है (TUNNEL डिलीवरी मोड मानते हुए); एक अनुवर्ती खंड का अधिकतम आकार 996 बाइट्स है। इसलिए अधिकतम आकार लगभग 956 + (62 * 996) = 62708 बाइट्स, या 61.2 KB है।

इसके अतिरिक्त, ट्रांसपोर्ट में अतिरिक्त प्रतिबंध हो सकते हैं। NTCP सीमा 16KB - 6 = 16378 बाइट्स है। SSU सीमा लगभग 32 KB है। NTCP2 सीमा लगभग 64KB - 20 = 65516 बाइट्स है, जो किसी टनल द्वारा समर्थित सीमा से अधिक है।

ध्यान दें कि ये वे सीमाएं नहीं हैं जो क्लाइंट डेटाग्राम के लिए देखता है, क्योंकि राउटर एक गैरलिक संदेश में क्लाइंट संदेश के साथ एक रिप्लाई लीज़सेट और/या सत्र टैग्स को एक साथ पैक कर सकता है। लीज़सेट और टैग्स मिलकर लगभग 5.5KB जोड़ सकते हैं। इसलिए वर्तमान डेटाग्राम सीमा लगभग 10KB है। भविष्य के संस्करण में इस सीमा में वृद्धि की जाएगी।

## संदेश प्रकार {#types}

उच्च संख्या वाली प्राथमिकता का अर्थ है उच्च प्राथमिकता। अधिकांश ट्रैफ़िक TunnelDataMessages (प्राथमिकता 400) होता है, इसलिए 400 से ऊपर कुछ भी व्यावहारिक रूप से उच्च प्राथमिकता का होता है, और 400 से नीचे कुछ भी निम्न प्राथमिकता का होता है। ध्यान दें कि कई संदेशों को आमतौर पर क्लाइंट टनल के बजाय अन्वेषणात्मक टनल के माध्यम से रूट किया जाता है, और इसलिए जब तक पहले छलांग (हॉप्स) संयोगवश एक ही पीयर पर न हों, तब तक वे समान कतार में नहीं हो सकते।

इसके अलावा, सभी संदेश प्रकार एन्क्रिप्टेड किए बिना भेजे नहीं जाते हैं। उदाहरण के लिए, एक टनल का परीक्षण करते समय, राउटर एक DeliveryStatusMessage को लपेटता है, जिसे GarlicMessage में लपेटा जाता है, जिसे बदले में DataMessage में लपेटा जाता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Priority</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Comments</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookupMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">May vary</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseSearchReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Typ. 161</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Size is 65 + 32*(number of hashes) where typically, the hashes for three floodfill routers are returned.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseStoreMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Varies</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">460</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet. RouterInfo structures are compressed, and size varies; however there is a continuing effort to reduce the amount of data published in a RouterInfo.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4 - 62080</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">425</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary on a per-destination basis</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DeliveryStatusMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Used for message replies, and for testing tunnels - generally wrapped in a GarlicMessage</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/overview/garlic-routing/">GarlicMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generally wrapped in a DataMessage - but when unwrapped, given a priority of 100 by the forwarding router</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelDataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1028</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The most common message. Priority for tunnel participants, outbound endpoints, and inbound gateways was reduced to 200 as of release 0.6.1.33. Outbound gateway messages (i.e. those originated locally) remains at 400.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelGatewayMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300/400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildReplyMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Others (Types 0, 4-9, 12)</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">0, 4-9, 12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Obsolete, Unused</td>
</tr>
</table>
## टनल परीक्षण

API संस्करण 0.9.68 2026-02 से टनल परीक्षण आवश्यक है, क्योंकि ऐसे भाग लेने वाले टनल्स को राउटर द्वारा छोड़ दिया जा सकता है जिन्हें पहले दो मिनट के बाद कोई ट्रैफ़िक प्राप्त नहीं हुआ हो।

## पूर्ण प्रोटोकॉल विशिष्टता

पूर्ण प्रोटोकॉल विशिष्टता के लिए [I2NP विशिष्टता पृष्ठ](/docs/specs/i2np/) देखें। साथ ही [सामान्य डेटा संरचना विशिष्टता पृष्ठ](/docs/specs/common-structures/) भी देखें।

## भावी कार्य

यह स्पष्ट नहीं है कि वर्तमान प्राथमिकता योजना सामान्य रूप से प्रभावी है या नहीं, और विभिन्न संदेशों के लिए प्राथमिकताओं को आगे समायोजित करने की आवश्यकता है या नहीं। यह आगे के अनुसंधान, विश्लेषण और परीक्षण का विषय है।
