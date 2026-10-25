---
title: "I2NP विनिर्देश"
description: "I2P Network Protocol (I2NP) संदेश प्रारूप, प्राथमिकताएं, और router-to-router संचार के लिए सामान्य संरचनाएं।"
slug: "i2np"
aliases:
  - "/hi/spec/i2np"
  - "/hi/spec/i2np/"
  - "/hi/i2np_spec"
  - "/hi/i2np_spec/"
category: "प्रोटोकॉल"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## अवलोकन

I2P Network Protocol (I2NP) I2P transport protocols के ऊपर की परत है। यह एक router-to-router protocol है। इसका उपयोग network database lookups और replies के लिए, tunnels बनाने के लिए, और encrypted router व client data messages के लिए किया जाता है। I2NP messages को किसी दूसरे router को point-to-point भेजा जा सकता है, या उस router तक tunnels के माध्यम से anonymously भेजा जा सकता है।

## प्रोटोकॉल संस्करण {#versions}

सभी router को अपने I2NP प्रोटोकॉल संस्करण को RouterInfo गुणों में "router.version" फील्ड में प्रकाशित करना चाहिए। यह संस्करण फील्ड API संस्करण है, जो विभिन्न I2NP प्रोटोकॉल सुविधाओं के लिए समर्थन के स्तर को दर्शाता है, और यह आवश्यक रूप से वास्तविक router संस्करण नहीं है।

यदि वैकल्पिक (गैर-Java) router वास्तविक router implementation के बारे में कोई version की जानकारी प्रकाशित करना चाहते हैं, तो उन्हें यह किसी अन्य property में करना होगा। नीचे सूचीबद्ध के अलावा अन्य versions की अनुमति है। Support का निर्धारण numeric comparison के माध्यम से किया जाएगा; उदाहरण के लिए, 0.9.13 का मतलब है 0.9.12 features के लिए support। ध्यान दें कि "coreVersion" property अब router info में प्रकाशित नहीं की जाती है, और I2NP protocol version के निर्धारण के लिए कभी उपयोग नहीं की गई थी।

I2NP प्रोटोकॉल संस्करणों का एक मूलभूत सारांश निम्नलिखित है। विवरण के लिए, नीचे देखें।

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
ध्यान दें कि transport-संबंधित सुविधाएं और संगतता के मुद्दे भी हैं; विवरण के लिए NTCP और SSU transport दस्तावेज़ देखें।

## सामान्य संरचनाएं {#structures}

निम्नलिखित संरचनाएं कई I2NP संदेशों के तत्व हैं। ये पूर्ण संदेश नहीं हैं।

### I2NP संदेश हेडर {#struct-I2NPMessageHeader}

#### विवरण

सभी I2NP संदेशों के लिए सामान्य हेडर, जिसमें चेकसम, समाप्ति तिथि आदि जैसी महत्वपूर्ण जानकारी होती है।

#### सामग्री

संदर्भ के आधार पर तीन अलग-अलग प्रारूप उपयोग किए जाते हैं; एक मानक प्रारूप, और दो छोटे प्रारूप।

मानक 16 बाइट फॉर्मेट में 1 बाइट [Integer](/docs/specs/common-structures/#integer) होता है जो इस संदेश के प्रकार को निर्दिष्ट करता है, जिसके बाद 4 बाइट [Integer](/docs/specs/common-structures/#integer) होता है जो message-id को निर्दिष्ट करता है। इसके बाद एक समाप्ति [Date](/docs/specs/common-structures/#date) होता है, जिसके बाद 2 बाइट [Integer](/docs/specs/common-structures/#integer) होता है जो संदेश payload की लंबाई को निर्दिष्ट करता है, जिसके बाद एक [Hash](/docs/specs/common-structures/#hash) होता है, जो पहले बाइट तक काटा जाता है। इसके बाद वास्तविक संदेश डेटा आता है।

छोटे formats 8 byte expiration (milliseconds में) के बजाय 4 byte expiration (seconds में) का उपयोग करते हैं। छोटे formats में checksum या size नहीं होता, ये encapsulations द्वारा प्रदान किए जाते हैं, context के आधार पर।

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### नोट्स

- जब [SSU](/docs/transports/ssu/) के माध्यम से प्रसारित किया जाता है, तो 16-byte मानक header का उपयोग नहीं किया जाता है। केवल 1-byte type और 4-byte expiration (सेकंड में) शामिल किया जाता है। Message id और size को SSU data packet format में शामिल किया जाता है। Checksum की आवश्यकता नहीं है क्योंकि त्रुटियां decryption में पकड़ी जाती हैं।

- जब [NTCP2](/docs/specs/ntcp2/) या [SSU2](/docs/specs/ssu2/) पर प्रसारित किया जाता है, तो 16-byte का मानक header उपयोग नहीं किया जाता। केवल 1-byte type, 4-byte message id, और 4-byte expiration (सेकंड में) शामिल किए जाते हैं। आकार NTCP2 और SSU2 data packet formats में शामिल होता है। Checksum की आवश्यकता नहीं होती क्योंकि त्रुटियां decryption में पकड़ी जाती हैं।

- मानक हेडर अन्य संदेशों और संरचनाओं (Data, TunnelData, TunnelGateway, और GarlicClove) में निहित I2NP संदेशों के लिए भी आवश्यक है। रिलीज़ 0.8.12 के बाद से, ओवरहेड को कम करने के लिए, प्रोटोकॉल स्टैक में कुछ स्थानों पर checksum सत्यापन को निष्क्रिय कर दिया गया है। हालांकि, पुराने संस्करणों के साथ संगतता के लिए, checksum जेनरेशन अभी भी आवश्यक है। यह भविष्य के शोध का विषय है कि प्रोटोकॉल स्टैक में उन बिंदुओं को निर्धारित किया जाए जहाँ दूर के छोर के router का संस्करण ज्ञात है और checksum जेनरेशन को निष्क्रिय किया जा सकता है।

- छोटी समाप्ति अवधि unsigned है और 7 फरवरी, 2106 को wrap around हो जाएगी। उस तारीख से, सही समय प्राप्त करने के लिए एक offset जोड़ना होगा।

- Implementation ऐसे messages को reject कर सकते हैं जिनकी expiration भविष्य में बहुत दूर है। अनुशंसित अधिकतम expiration भविष्य में 60s है।

### BuildRequestRecord {#struct-BuildRequestRecord}

DEPRECATED, केवल वर्तमान नेटवर्क में उपयोग किया जाता है जब tunnel में ElGamal router होता है। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

#### विवरण

एक tunnel में एक hop के निर्माण का अनुरोध करने के लिए कई records के सेट में से एक Record। अधिक विवरण के लिए [tunnel overview](/docs/specs/tunnel-implementation/) और [ElGamal tunnel creation specification](/docs/specs/tunnel-creation/) देखें।

ECIES-X25519 BuildRequestRecords के लिए, [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) देखें।

#### सामग्री (ElGamal)

संदेश प्राप्त करने के लिए [TunnelId](/docs/specs/common-structures/#tunnelid), इसके बाद हमारी [RouterIdentity](/docs/specs/common-structures/#routeridentity) का [Hash](/docs/specs/common-structures/#hash)। इसके बाद अगले router की [RouterIdentity](/docs/specs/common-structures/#routeridentity) का [TunnelId](/docs/specs/common-structures/#tunnelid) और [Hash](/docs/specs/common-structures/#hash) आता है।

ElGamal और AES एन्क्रिप्टेड:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal encrypted:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
स्पष्ट पाठ:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### नोट्स

- 512-byte encrypted record में, ElGamal data में 514-byte ElGamal encrypted block [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) के bytes 1-256 और 258-513 शामिल हैं। block से दो padding bytes (स्थान 0 और 257 पर zero bytes) को हटा दिया जाता है।

- फील्ड सामग्री के विवरण के लिए [tunnel creation specification](/docs/specs/tunnel-creation/) देखें।

### BuildResponseRecord {#struct-BuildResponseRecord}

DEPRECATED, केवल वर्तमान network में उपयोग होता है जब tunnel में एक ElGamal router होता है। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

#### विवरण

एक build request के responses के साथ कई records के set में से एक Record। अधिक विवरण के लिए [tunnel overview](/docs/specs/tunnel-implementation/) और [ElGamal tunnel creation specification](/docs/specs/tunnel-creation/) देखें।

ECIES-X25519 BuildResponseRecords के लिए, [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) देखें।

#### सामग्री (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### नोट्स

- रैंडम डेटा फील्ड का उपयोग भविष्य में अनुरोधकर्ता को congestion या peer connectivity की जानकारी वापस भेजने के लिए किया जा सकता है।

- उत्तर फ़ील्ड के विवरण के लिए [tunnel creation specification](/docs/specs/tunnel-creation/) देखें।

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

केवल ECIES-X25519 routers के लिए, API version 0.9.51 के अनुसार। encrypted होने पर 218 bytes। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

केवल ECIES-X25519 routers के लिए, API संस्करण 0.9.51 के अनुसार। एन्क्रिप्ट होने पर 218 बाइट्स। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

### GarlicClove {#struct-GarlicClove}

चेतावनी: यह ElGamal-encrypted garlic messages [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) के भीतर garlic cloves के लिए उपयोग किया जाने वाला प्रारूप है। ECIES-AEAD-X25519-Ratchet garlic messages और garlic cloves का प्रारूप काफी अलग है; विशिष्टता के लिए [ECIES](/docs/specs/ecies/) देखें।

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### नोट्स

- Cloves कभी भी fragmented नहीं होते। जब Garlic Clove में उपयोग किया जाता है, तो Delivery Instructions flag byte का पहला bit encryption को निर्दिष्ट करता है। यदि यह bit 0 है, तो clove encrypted नहीं है। यदि 1 है, तो clove encrypted है, और flag byte के तुरंत बाद एक 32 byte Session Key आती है। Clove encryption पूरी तरह से implemented नहीं है।

- [garlic routing specification](/docs/overview/garlic-routing/) भी देखें।

- अधिकतम लंबाई सभी cloves की कुल लंबाई और GarlicMessage की अधिकतम लंबाई का एक फ़ंक्शन है।

- भविष्य में, certificate का उपयोग संभावित रूप से HashCash के लिए routing के लिए "भुगतान" करने हेतु किया जा सकता है।

- संदेश कोई भी I2NP संदेश हो सकता है (GarlicMessage सहित, हालांकि व्यवहार में इसका उपयोग नहीं किया जाता)। व्यवहार में उपयोग किए जाने वाले संदेश DataMessage, DeliveryStatusMessage, और DatabaseStoreMessage हैं।

- Clove ID आमतौर पर ट्रांसमिट पर एक रैंडम नंबर पर सेट किया जाता है और रिसीव पर डुप्लिकेट के लिए चेक किया जाता है (टॉप-लेवल Message ID के समान message ID स्पेस)

### Garlic Clove Delivery Instructions {#struct-GarlicCloveDeliveryInstructions}

यह format ElGamal-encrypted [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) और ECIES-AEAD-X25519-Ratchet encrypted [ECIES](/docs/specs/ecies/) दोनों garlic cloves के लिए उपयोग किया जाता है।

यह specification केवल Garlic Cloves के अंदर Delivery Instructions के लिए है। ध्यान दें कि "Delivery Instructions" का उपयोग Tunnel Messages के अंदर भी किया जाता है, जहाँ format काफी अलग होता है। विवरण के लिए [Tunnel Message documentation](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) देखें। Tunnel Message Delivery Instructions के लिए निम्नलिखित specification का उपयोग न करें!

Session key और delay का उपयोग नहीं होता और ये कभी उपस्थित नहीं होते, इसलिए तीन संभावित लंबाई 1 (LOCAL), 33 (ROUTER और DESTINATION), और 37 (TUNNEL) bytes हैं।

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## संदेश

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### विवरण

एक अवांछित डेटाबेस स्टोर, या सफल [DatabaseLookup](#msg-DatabaseLookup) संदेश की प्रतिक्रिया

#### विषय सूची

एक असंपीड़ित LeaseSet, LeaseSet2, MetaLeaseSet, या EncryptedLeaseset, या एक संपीड़ित RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### टिप्पणियाँ

- सुरक्षा के लिए, यदि संदेश एक tunnel के नीचे प्राप्त होता है तो reply fields को नजरअंदाज कर दिया जाता है।

- key वास्तविक RouterIdentity या Destination का "real" hash है, routing key नहीं।

- Types 3, 5, और 7 release 0.9.38 के अनुसार हैं। अधिक जानकारी के लिए proposal 123 देखें। ये types केवल उन routers को भेजे जाने चाहिए जो release 0.9.38 या उससे उच्चतर हैं।

- कनेक्शन कम करने के अनुकूलन के रूप में, यदि प्रकार एक LeaseSet है, reply token शामिल है, reply tunnel ID गैर-शून्य है, और reply gateway/tunnelID जोड़ी LeaseSet में एक lease के रूप में मिलती है, तो प्राप्तकर्ता reply को LeaseSet में किसी अन्य lease पर पुनर्निर्देशित कर सकता है।

- router OS और implementation को छुपाने के लिए, modification time को 0 और OS byte को 0xFF सेट करके Java router implementation के gzip से मैच करें, और XFL को 0x02 (max compression, slowest algorithm) सेट करें। RFC 1952 देखें। compressed router info के पहले 10 bytes होंगे (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### विवरण

नेटवर्क डेटाबेस में किसी आइटम को खोजने का अनुरोध। प्रतिक्रिया या तो [DatabaseStore](#msg-DatabaseStore) या [DatabaseSearchReply](#msg-DatabaseSearchReply) होती है।

#### सामग्री

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Reply Encryption

नोट: API 0.9.58 के अनुसार ElGamal router अब deprecated हैं। चूंकि query करने के लिए अनुशंसित न्यूनतम floodfill संस्करण अब 0.9.58 है, implementations को ElGamal floodfill router के लिए encryption implement करने की आवश्यकता नहीं है। ElGamal destinations अभी भी supported हैं।

Flag bit 4 का उपयोग bit 1 के साथ मिलकर reply encryption mode निर्धारित करने के लिए किया जाता है। Flag bit 4 केवल तभी set किया जाना चाहिए जब version 0.9.46 या उससे अधिक वाले routers को भेजा जा रहा हो। विवरण के लिए proposals 154 और 156 देखें।

नीचे दी गई तालिका में, "DH n/a" का मतलब है कि उत्तर एन्क्रिप्टेड नहीं है। "DH no" का मतलब है कि उत्तर की चाबियां अनुरोध में शामिल हैं। "DH yes" का मतलब है कि उत्तर की चाबियां DH ऑपरेशन से प्राप्त की गई हैं।

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### कोई एन्क्रिप्शन नहीं

reply_key, tags, और reply_tags मौजूद नहीं हैं।

#### ElG to ElG

0.9.7 से समर्थित। 0.9.58 से deprecated। ElG destination एक ElG router को lookup भेजता है।

अनुरोधकर्ता कुंजी निर्माण:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
संदेश प्रारूप:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES से ElG

0.9.46 से समर्थित। 0.9.58 से deprecated। ECIES destination एक ElG router को lookup भेजता है। reply_key और reply_tags फील्ड्स को ECIES-encrypted reply के लिए पुनः परिभाषित किया गया है।

अनुरोधकर्ता कुंजी निर्माण:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
संदेश प्रारूप: reply_key और reply_tags फ़ील्ड को निम्नलिखित प्रकार से पुनः परिभाषित करें:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
उत्तर एक ECIES Existing Session संदेश है, जैसा कि [ECIES](/docs/specs/ecies/) में परिभाषित है।

#### उत्तर प्रारूप

यह मौजूदा session message है, जो [ECIES](/docs/specs/ecies/) में समान है, संदर्भ के लिए नीचे कॉपी किया गया है।

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
AEAD पैरामीटर:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES से ECIES (0.9.49)

ECIES destination या router एक ECIES router को lookup भेजता है। 0.9.49 से समर्थित।

ECIES router 0.9.48 में पेश किए गए थे, देखें [Proposal 156](/proposals/156/)। ECIES destinations और router ऊपर "ECIES to ElG" सेक्शन में दिए गए समान फॉर्मेट का उपयोग कर सकते हैं, जिसमें अनुरोध में reply keys शामिल हों। lookup message encryption [ECIES-ROUTERS](/docs/specs/ecies-routers/) में निर्दिष्ट है। अनुरोधकर्ता गुमनाम है।

#### ECIES से ECIES (भविष्य में)

यह विकल्प अभी तक पूरी तरह से परिभाषित नहीं है। [प्रस्ताव 156](/proposals/156/) देखें।

#### नोट्स

- 0.9.16 से पहले, key RouterInfo या LeaseSet के लिए हो सकती थी, क्योंकि वे एक ही key space में होते हैं, और केवल किसी विशेष प्रकार के डेटा का अनुरोध करने के लिए कोई flag नहीं था।

- रिलीज़ 0.9.7 के अनुसार Encryption flag, reply key, और reply tags।

- एन्क्रिप्टेड उत्तर केवल तभी उपयोगी होते हैं जब प्रतिक्रिया tunnel के माध्यम से आती है।

- यदि वैकल्पिक DHT lookup रणनीतियां (उदाहरण के लिए, recursive lookups) लागू की जाती हैं तो शामिल किए गए tags की संख्या एक से अधिक हो सकती है।

- lookup key और exclude keys "वास्तविक" hashes हैं, routing keys नहीं।

- रिलीज़ 0.9.38 के अनुसार Types 3, 5, और 7 वापस किए जा सकते हैं। अधिक जानकारी के लिए proposal 123 देखें।

- Exploratory lookup नोट्स: एक exploratory lookup को key के करीब के non-floodfill hashes की एक सूची वापस करने के लिए परिभाषित किया गया है। हालांकि, implementation variants के लिए DatabaseSearchReply के महत्वपूर्ण नोट्स देखें। इसके अतिरिक्त, इस specification ने कभी स्पष्ट नहीं किया है कि क्या receiver को एक RI के लिए search key को lookup करना चाहिए और यदि उपस्थित है तो DSRM के बजाय एक DatabaseStore वापस करना चाहिए। Java lookup करता है; i2pd नहीं करता। इसलिए, पहले से प्राप्त hashes के लिए exploratory lookup का उपयोग करने की सिफारिश नहीं की जाती।

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### विवरण

एक असफल [DatabaseLookup](#msg-DatabaseLookup) Message का response

#### सामग्री

अनुरोधित key के सबसे नजदीक के router hashes की एक सूची

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### नोट्स

- 'from' hash अप्रमाणित है और इस पर भरोसा नहीं किया जा सकता।

- वापस किए गए peer hashes जरूरी नहीं है कि key के करीब हों उस router की तुलना में जिससे query की जा रही है। नियमित lookups के replies के लिए, यह नए floodfills की खोज और मजबूती के लिए "backwards" searching (key-से-दूर) की सुविधा प्रदान करता है।

- एक exploration lookup के लिए key आमतौर पर यादृच्छिक रूप से उत्पन्न होती है। इसलिए, response के non-floodfill peer_hashes का चयन एक अनुकूलित एल्गोरिदम का उपयोग करके किया जा सकता है, जैसे कि ऐसे peers प्रदान करना जो key के करीब हों लेकिन पूरे स्थानीय network database में जरूरी नहीं कि सबसे करीब हों, ताकि पूरे स्थानीय database की अकुशल sort या search से बचा जा सके। अन्य रणनीतियां जैसे कि caching भी उपयुक्त हो सकती हैं। यह implementation-dependent है।

- वापस किए गए hashes की सामान्य संख्या: 3

- वापस करने के लिए अनुशंसित अधिकतम hashes की संख्या: 16

- lookup key, peer hashes, और from hash "वास्तविक" hashes हैं, routing keys नहीं।

### DeliveryStatus {#msg-DeliveryStatus}

#### विवरण

एक सरल संदेश पावती। आमतौर पर संदेश के मूल भेजने वाले द्वारा बनाया जाता है, और संदेश के साथ ही Garlic Message में लपेटा जाता है, जिसे गंतव्य द्वारा वापस किया जाना होता है।

इस संदेश का उपयोग टनल परीक्षण के लिए भी किया जाता है, जहां प्रेषक इसे आउटबाउंड टनल के माध्यम से, एक इनबाउंड टनल की ओर भेजता है, और फिर स्वयं पर वापस लौटता है। इस उपयोग में भी, यह आमतौर पर गैर्लिक रैप्ड (garlic wrapped) होता है। टनल परीक्षण एपीआई संस्करण 0.9.68 2026-02 से आवश्यक है, क्योंकि राउटर को पहले दो मिनट के बाद कोई भी ट्रैफ़िक प्राप्त न करने वाले भाग लेने वाले टनल को छोड़ने की अनुमति दी जाती है।

#### विषय-सूची

डिलीवर किए गए संदेश का आईडी, और निर्माण या आगमन का समय।

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### टिप्पणियाँ

- यह प्रतीत होता है कि time stamp हमेशा creator द्वारा वर्तमान समय पर सेट किया जाता है। हालांकि, code में इसके कई उपयोग हैं, और भविष्य में और भी जोड़े जा सकते हैं।

- यह संदेश SSU [SSU-ED](/docs/transports/ssu/#establishDirect) में session established confirmation के रूप में भी उपयोग किया जाता है। इस मामले में, संदेश ID को एक random संख्या पर सेट किया जाता है, और "arrival time" को वर्तमान network-wide ID पर सेट किया जाता है, जो 2 है (यानी 0x0000000000000002)।

### Garlic {#msg-Garlic}

चेतावनी: यह एल-गामल-एन्क्रिप्टेड गैरलिक संदेशों [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) के लिए उपयोग किए जाने वाले प्रारूप के बारे में है। ECIES-AEAD-X25519-Ratchet गैरलिक संदेशों और गैरलिक क्लोव्स के लिए प्रारूप काफी अलग है; विशिष्टता के लिए [ECIES](/docs/specs/ecies/) देखें।

#### विवरण

एकाधिक एन्क्रिप्टेड I2NP संदेशों को लपेटने के लिए उपयोग किया जाता है

#### विषय-सूची

डिक्रिप्ट होने पर, [गैरलिक क्लोव्स](#struct-GarlicClove) और अतिरिक्त डेटा की एक श्रृंखला, जिसे क्लोव सेट के रूप में भी जाना जाता है।

एन्क्रिप्टेड:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
डिक्रिप्टेड डेटा, जिसे क्लोव सेट भी कहा जाता है:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### नोट्स

- जब अनएन्क्रिप्टेड हो, तो डेटा में एक या अधिक [Garlic Cloves](#struct-GarlicClove) होते हैं।

- AES encrypted block को न्यूनतम 128 bytes तक padded किया जाता है; 32-byte Session Tag के साथ encrypted message का न्यूनतम आकार 160 bytes होता है; 4 length bytes के साथ Garlic Message का न्यूनतम आकार 164 bytes होता है।

- वास्तविक अधिकतम लंबाई 64 KB से कम है; [I2NP](/docs/protocol/i2np/) देखें।

- [ElGamal/AES specification](/docs/specs/elgamal-aes/) भी देखें।

- [garlic routing specification](/docs/overview/garlic-routing/) भी देखें।

- AES encrypted block का 128 byte न्यूनतम आकार वर्तमान में configurable नहीं है, हालांकि GarlicMessage में GarlicClove में DataMessage का न्यूनतम आकार, overhead के साथ, वैसे भी 128 bytes है। भविष्य में न्यूनतम आकार बढ़ाने के लिए एक configurable विकल्प जोड़ा जा सकता है।

- संदेश ID आम तौर पर ट्रांसमिट पर एक यादृच्छिक संख्या पर सेट होता है और प्राप्त करते समय इसे अनदेखा किया जाता है।

- भविष्य में, certificate का उपयोग संभवतः routing के लिए "भुगतान" करने हेतु HashCash के लिए किया जा सकता है।

### TunnelData {#msg-TunnelData}

#### विवरण

एक सुरंग के गेटवे या प्रतिभागी द्वारा अगले प्रतिभागी या अंत बिंदु को भेजा गया संदेश। डेटा निश्चित लंबाई का होता है, जिसमें I2NP संदेश होते हैं जो खंडित, समूहित, पैड किए गए और एन्क्रिप्टेड होते हैं।

#### विषय-सूची

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### टिप्पणियाँ

- इस संदेश के लिए I2NP message ID प्रत्येक hop पर एक नई यादृच्छिक संख्या पर सेट किया जाता है।

- [Tunnel Message Specification](/docs/legacy/tunnel-message/) भी देखें

### TunnelGateway {#msg-TunnelGateway}

#### विवरण

टनल के इनबाउंड गेटवे पर भेजे जाने के लिए एक अन्य I2NP संदेश को लपेटता है।

#### सामग्री

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### नोट्स

- payload एक I2NP message है जिसमें मानक 16-byte header होता है।

### डेटा {#msg-Data}

#### विवरण

गैरिक मैसेज और गैरिक क्लोव्स द्वारा मनमाना डेटा लपेटने के लिए उपयोग किया जाता है।

#### सामग्री

एक लंबाई पूर्णांक, उसके बाद अपारदर्शी डेटा।

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### नोट्स

- इस संदेश में कोई routing जानकारी नहीं है और यह कभी भी "unwrapped" नहीं भेजा जाएगा। यह केवल `Garlic` संदेशों के अंदर उपयोग किया जाता है।

### TunnelBuild {#msg-TunnelBuild}

DEPRECATED, [VariableTunnelBuild](#msg-VariableTunnelBuild) का उपयोग करें

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### नोट्स

- 0.9.48 के अनुसार, इसमें ECIES-X25519 BuildRequestRecords भी हो सकते हैं, देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- [tunnel creation specification](/docs/specs/tunnel-creation/) भी देखें।

- इस message के लिए I2NP message ID को tunnel creation specification के अनुसार सेट किया जाना चाहिए।

- जबकि आज के network में यह message शायद ही कभी देखा जाता है, क्योंकि इसे `VariableTunnelBuild` message द्वारा प्रतिस्थापित कर दिया गया है, फिर भी यह बहुत लंबी tunnels के लिए उपयोग किया जा सकता है, और यह deprecated नहीं हुआ है। Routers को इसे implement करना आवश्यक है।

### TunnelBuildReply {#msg-TunnelBuildReply}

DEPRECATED, [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply) का उपयोग करें

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### नोट्स

- 0.9.48 के अनुसार, इसमें ECIES-X25519 BuildResponseRecords भी हो सकते हैं, देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- [tunnel निर्माण विनिर्देश](/docs/specs/tunnel-creation/) भी देखें।

- इस संदेश के लिए I2NP message ID को tunnel creation specification के अनुसार सेट करना आवश्यक है।

- जबकि आज के network में यह message शायद ही देखा जाता है, क्योंकि इसे `VariableTunnelBuildReply` message से बदल दिया गया है, फिर भी यह बहुत लंबे tunnels के लिए उपयोग हो सकता है, और इसे deprecated नहीं किया गया है। Routers को इसे implement करना आवश्यक है।

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### नोट्स

- 0.9.48 के अनुसार, इसमें ECIES-X25519 BuildRequestRecords भी हो सकते हैं, देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- यह संदेश router संस्करण 0.7.12 में पेश किया गया था, और इससे पहले के संस्करण वाले tunnel प्रतिभागियों को नहीं भेजा जा सकता है।

- [tunnel creation specification](/docs/specs/tunnel-creation/) भी देखें।

- इस संदेश के लिए I2NP message ID को tunnel creation specification के अनुसार सेट करना होगा।

- आज के नेटवर्क में रिकॉर्ड की सामान्य संख्या 4 है, कुल आकार 2113 के लिए।

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### नोट्स

- 0.9.48 से, इसमें ECIES-X25519 BuildResponseRecords भी हो सकते हैं, देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- यह संदेश router संस्करण 0.7.12 में पेश किया गया था, और उस संस्करण से पहले के tunnel प्रतिभागियों को नहीं भेजा जा सकता है।

- [tunnel निर्माण विनिर्देश](/docs/specs/tunnel-creation/) भी देखें।

- इस message के लिए I2NP message ID को tunnel creation specification के अनुसार सेट करना होगा।

- आज के नेटवर्क में रिकॉर्ड्स की सामान्य संख्या 4 है, कुल आकार 2113 के लिए।

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### विवरण

API संस्करण 0.9.51 के रूप में, केवल ECIES-X25519 राउटर्स के लिए।

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### टिप्पणियाँ

- 0.9.51 से। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- यह संदेश router version 0.9.51 में पेश किया गया था, और इससे पहले के version के tunnel participants को नहीं भेजा जा सकता है।

- आज के नेटवर्क में रिकॉर्ड की सामान्य संख्या 4 है, कुल आकार 873 के लिए।

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### विवरण

नए टनल के आउटबाउंड एंडपॉइंट से उत्पत्ति स्थल पर भेजा गया। API संस्करण 0.9.51 से केवल ECIES-X25519 राउटर्स के लिए।

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### नोट्स

- 0.9.51 के अनुसार। देखें [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)।

- आज के नेटवर्क में रिकॉर्ड की सामान्य संख्या 4 है, कुल आकार 873 के लिए।

## संदर्भ

- **[CRYPTO-ELG]** [Cryptography - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [सामान्य संरचनाएं - Date](/docs/specs/common-structures/#date)
- **[ECIES]** [ECIES स्पेसिफिकेशन](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [ECIES Routers स्पेसिफिकेशन](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Routing](/docs/overview/garlic-routing/)
- **[Hash]** [सामान्य संरचनाएं - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP प्रोटोकॉल](/docs/protocol/i2np/)
- **[Integer]** [सामान्य संरचनाएं - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [NTCP2 स्पेसिफिकेशन](/docs/specs/ntcp2/)
- **[Prop156]** [प्रस्ताव 156](/proposals/156/)
- **[Prop157]** [प्रस्ताव 157](/proposals/157/)
- **[RouterIdentity]** [सामान्य संरचनाएं - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU ट्रांसपोर्ट](/docs/transports/ssu/)
- **[SSU-ED]** [SSU ट्रांसपोर्ट - Establish Direct](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [SSU2 स्पेसिफिकेशन](/docs/specs/ssu2/)
- **[TMDI]** [Tunnel Message Delivery Instructions](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Tunnel Creation स्पेसिफिकेशन](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Tunnel Implementation](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Tunnel Message स्पेसिफिकेशन](/docs/legacy/tunnel-message/)
- **[TunnelId]** [सामान्य संरचनाएं - TunnelId](/docs/specs/common-structures/#tunnelid)
