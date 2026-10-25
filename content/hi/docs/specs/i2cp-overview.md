---
title: "I2CP अवलोकन"
description: "I2P क्लाइंट प्रोटोकॉल (I2CP) का अवलोकन - सत्र प्रबंधन, विकल्प, पेलोड प्रारूप और मल्टीप्लेक्सिंग।"
slug: "i2cp-overview"
aliases:
  - "/hi/docs/protocol/i2cp"
  - "/hi/docs/protocol/i2cp/"
  - "/hi/i2cp"
  - "/hi/i2cp/"
category: "प्रोटोकॉल"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## अवलोकन

I2P क्लाइंट प्रोटोकॉल (I2CP) राउटर तथा उस नेटवर्क पर संचार करने वाले किसी भी क्लाइंट के बीच जिम्मेदारियों को स्पष्ट रूप से अलग करता है। यह एकल टीसीपी सॉकेट के माध्यम से संदेश भेजकर और प्राप्त करके सुरक्षित एवं अतुल्यकालिक संदेशन को सक्षम करता है। I2CP के साथ, एक क्लाइंट अनुप्रयोग राउटर को यह बताता है कि वे कौन हैं (उनका "गंतव्य"), किस स्तर की गोपनीयता, विश्वसनीयता और विलंबता के बलिदान की अनुमति है, तथा संदेश कहाँ भेजे जाएँ। इसके बदले में, राउटर I2CP का उपयोग करके क्लाइंट को यह बताता है कि कोई संदेश प्राप्त हुआ है या नहीं, और कुछ टनल के उपयोग के लिए प्राधिकरण का अनुरोध करता है।

प्रोटोकॉल स्वयं जावा में लागू किया गया है, जिससे क्लाइंट SDK प्रदान किया जा सके। यह SDK i2p.jar पैकेज में उपलब्ध है, जो I2CP के क्लाइंट-साइड को लागू करता है। क्लाइंट्स को कभी भी राउटर.jar पैकेज तक पहुँचने की आवश्यकता नहीं होनी चाहिए, जिसमें स्वयं राउटर और I2CP का राउटर-साइड शामिल है। एक गैर-जावा क्लाइंट को TCP-शैली के कनेक्शन के लिए [स्ट्रीमिंग लाइब्रेरी](/docs/api/streaming/) को भी लागू करना होगा।

आवेदन आधार I2CP के साथ-साथ [स्ट्रीमिंग](/docs/api/streaming/) और [डेटाग्राम](/docs/specs/datagrams/) लाइब्रेरी का लाभ [सिंपल एनोनिमस मैसेजिंग (SAM)](/docs/api/samv3/) प्रोटोकॉल का उपयोग करके उठा सकते हैं, जिसके लिए क्लाइंट्स को किसी भी प्रकार की क्रिप्टोग्राफी से निपटने की आवश्यकता नहीं होती। इसके अलावा, क्लाइंट्स कई प्रॉक्सी में से किसी एक के माध्यम से नेटवर्क तक पहुँच सकते हैं - HTTP, CONNECT, और SOCKS 4/4a/5। वैकल्पिक रूप से, जावा क्लाइंट ministreaming.jar और streaming.jar में उन लाइब्रेरी तक पहुँच सकते हैं। इसलिए जावा और गैर-जावा दोनों प्रकार के आवेदनों के लिए कई विकल्प उपलब्ध हैं।

क्लाइंट-साइड एंड-टू-एंड एन्क्रिप्शन (I2CP कनेक्शन के माध्यम से डेटा को एन्क्रिप्ट करना) को I2P रिलीज 0.6 में अक्षम कर दिया गया था, जिससे राउटर में लागू ElGamal/AES एंड-टू-एंड एन्क्रिप्शन बरकरार रहा। क्लाइंट लाइब्रेरीज को अभी भी केवल [लीजसेट्स](/docs/specs/i2cp/#msg_CreateLeaseSet) और [सत्र विन्यास](/docs/specs/i2cp/#struct_SessionConfig) के लिए DSA सार्वजनिक/निजी कुंजी हस्ताक्षर, तथा उन कुंजियों के प्रबंधन को लागू करना होता है।

एक मानक I2P स्थापना में, बाहरी जावा क्लाइंट द्वारा I2CP के माध्यम से स्थानीय राउटर के साथ संचार के लिए पोर्ट 7654 का उपयोग किया जाता है। डिफ़ॉल्ट रूप से, राउटर पते 127.0.0.1 से बाध्य होता है। 0.0.0.0 से बाध्य होने के लिए, राउटर उन्नत विन्यास विकल्प `i2cp.tcp.bindAllInterfaces=true` सेट करें और राउटर को पुनः आरंभ करें। राउटर के समान JVM में स्थित क्लाइंट संदेशों को एक आंतरिक JVM इंटरफ़ेस के माध्यम से सीधे राउटर को पास करते हैं।

कुछ राउटर और क्लाइंट लागू करने में `i2cp.SSL=true` विकल्प द्वारा विनिर्दिष्ट SSL के माध्यम से बाह्य कनेक्शन का समर्थन भी हो सकता है। जबकि SSL डिफ़ॉल्ट नहीं है, खुले इंटरनेट के लिए उजागर हो सकने वाले किसी भी ट्रैफ़िक के लिए इसकी अत्यधिक अनुशंसा की जाती है। प्राधिकरण उपयोगकर्ता/पासवर्ड (यदि कोई हो), [निजी कुंजी](/docs/specs/common-structures/#type_PrivateKey) और [साइनिंग निजी कुंजी](/docs/specs/common-structures/#type_SigningPrivateKey) [गंतव्य](/docs/specs/common-structures/#struct_Destination) के लिए सभी स्पष्ट-रूप में संचारित किए जाते हैं जब तक कि SSL सक्षम नहीं है। कुछ राउटर और क्लाइंट लागू करने में डोमेन सॉकेट के माध्यम से बाह्य कनेक्शन का भी समर्थन हो सकता है।

## I2CP प्रोटोकॉल विनिर्देश

पूर्ण प्रोटोकॉल विशिष्टता के लिए [I2CP विशिष्टता पृष्ठ](/docs/specs/i2cp/) देखें।

## I2CP आरंभीकरण {#initialization}

जब कोई क्लाइंट राउटर से जुड़ता है, तो सबसे पहले वह एक एकल प्रोटोकॉल संस्करण बाइट (0x2A) भेजता है। फिर वह एक [GetDate संदेश](/docs/specs/i2cp/#msg_GetDate) भेजता है और [SetDate संदेश](/docs/specs/i2cp/#msg_SetDate) प्रतिक्रिया की प्रतीक्षा करता है। इसके बाद, वह सत्र विन्यास युक्त एक [CreateSession संदेश](/docs/specs/i2cp/#msg_CreateSession) भेजता है। इसके बाद वह राउटर से [RequestLeaseSet संदेश](/docs/specs/i2cp/#msg_RequestLeaseSet) की प्रतीक्षा करता है, जो इंगित करता है कि इनबाउंड टनल बना लिए गए हैं, और एक CreateLeaseSet संदेश के साथ प्रतिक्रिया देता है जिसमें हस्ताक्षरित LeaseSet होता है। अब क्लाइंट अन्य I2P गंतव्यों से कनेक्शन शुरू कर सकता है या कनेक्शन प्राप्त कर सकता है।

## I2CP विकल्प {#options}

### राउटर-साइड विकल्प

निम्नलिखित विकल्पों को पारंपरिक रूप से [CreateSession संदेश](/docs/specs/i2cp/#msg_CreateSession) या [ReconfigureSession संदेश](/docs/specs/i2cp/#msg_ReconfigureSession) में निहित [SessionConfig](/docs/specs/i2cp/#struct_SessionConfig) के माध्यम से राउटर को पारित किया जाता है।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Router-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">clientMessageTimeout</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8*1000 - 120*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">60*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The timeout (ms) for all sent messages. Unused. See the protocol specification for per-message settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.lowTagThreshold</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum number of ElGamal/AES Session Tags before we send more. Recommended: approximately tagsToSend * 2/3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.inboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset size. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.outboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to the far-end in the options block. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.tagsToSend</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of ElGamal/AES Session Tags to send at a time. For clients with relatively low bandwidth per-client-pair (IRC, some UDP apps), this may be set lower.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">explicitPeers</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">null</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Comma-separated list of Base 64 Hashes of peers to build tunnels through; for debugging only</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.dontPublishLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Should generally be set to true for clients and false for servers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4,0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineExpiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The expiration of the offline signature, 4 bytes, seconds since the epoch. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineSignature</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the offline signature. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A base 64 X25519 private key for the router to use to decrypt the encrypted LS2 locally, only if per-client authentication is enabled. Optionally preceded by the key type and ':'. Only "ECIES_X25519:" is supported, which is the default. See proposal 123. Do not confuse with i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetTransientPublicKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">[type:]b64 The base 64 of the transient private key, prefixed by an optional sig type number or name, default DSA_SHA1. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; the streaming lib default is None as of 0.8.1, the client side default is None as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.password</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">For authorization, if required by the router. If the client is running in the same JVM as a router, this option is not required. Warning - username and password are sent in the clear to the router, unless using SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.username</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If incoming zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If outgoing zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels in. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels out. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally used in routerconsole, which will use the first few characters of the Base64 hash of the destination by default.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally ignored unless inbound.nickname is unset.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.priority</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority adjustment for outbound messages. Higher is higher priority.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels in. Limit was increased from 6 to 16 in release 0.9; however, numbers higher than 6 are incompatible with older releases.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">Used for consistent peer ordering across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "inbound." are stored in the "unknown options" properties of the inbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "outbound." are stored in the "unknown options" properties of the outbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">shouldBundleReplyInfo</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Set to false to disable ever bundling a reply LeaseSet. For clients that do not publish their LeaseSet, this option must be true for any reply to be possible. "true" is also recommended for multihomed servers with long connection times.

Setting to "false" may save significant outbound bandwidth, especially if the client is configured with a large number of inbound tunnels (Leases). If replies are still required, this may shift the bandwidth burden to the far-end client and the floodfill. There are several cases where "false" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a "server", all connections are inbound so the connecting far-end destination obviously has the leaseset already. Connections are either short, or it is acceptable for latency on a long-lived connection to temporarily increase while the other end re-fetches the LeaseSet after expiration. HTTP servers may fit these requirements.</td>
</tr>
</table>
नोट: बड़ी मात्रा, लंबाई या भिन्नता की सेटिंग्स के कारण प्रदर्शन या विश्वसनीयता में गंभीर समस्याएं हो सकती हैं।

नोट: संस्करण 0.7.7 से, विकल्प नाम और मान UTF-8 एन्कोडिंग का उपयोग करने चाहिए। यह मुख्य रूप से उपनामों के लिए उपयोगी है। इस संस्करण से पहले, बहु-बाइट वर्णों वाले विकल्प दूषित हो जाते थे। चूंकि विकल्प [मैपिंग](/docs/specs/common-structures/#type_Mapping) में एन्कोडेड होते हैं, सभी विकल्प नाम और मान अधिकतम 255 बाइट्स (वर्ण नहीं) तक सीमित हैं।

### क्लाइंट-साइड विकल्प

निम्नलिखित विकल्प क्लाइंट पक्ष पर व्याख्या की जाते हैं, और यदि उन्हें I2PClient.createSession() कॉल के माध्यम से I2PSession को पारित किया जाता है तो उनकी व्याख्या की जाएगी। स्ट्रीमिंग लाइब्रेरी को इन विकल्पों को I2CP तक पहुँचाना भी चाहिए। अन्य लागू करने में अलग-अलग डिफ़ॉल्ट हो सकते हैं।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Client-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1800000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 30 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Close I2P session when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.encryptLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypt the lease</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.gzip</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip outbound data</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetBlindedType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See prop. 123</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The sig type of the blinded key for encrypted LS2. Default depends on the destination sig type. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.dh.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64pubkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the public key to use for DH per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.psk.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64privkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the private key to use for PSK per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">For encrypted leasesets. Base 64 SessionKey (44 characters)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOption.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">srvKey=srvValue</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A service record to be placed in the LeaseSet2 options. Example: "_smtp._tcp=1 86400 0 0 25 ...b32.i2p". nnn starts with 0. See proposal 167.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private keys for encryption. Optionally preceded by the encryption type name or number and ':'. For LS1, only one key is supported, and only "0:" or "ELGAMAL_2048:" is supported, which is the default. As of 0.9.39, for LS2, multiple keys may be comma-separated, and each key must be a different encryption type. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts. See proposals 123, 144, and 145. See also i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSigningPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private key for signatures. Optionally preceded by the key type and ':'. DSA_SHA1 is the default. Key type must match the signature type in the destination. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; None is the default as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 20 minutes, minimum 5 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reduce tunnel quantity when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel quantity when reduced (applies to both inbound and outbound)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.SSL</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Connect to the router using SSL. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.host</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">127.0.0.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router hostname. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.port</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7654</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router I2CP port. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
</table>
नोट: सभी तर्क, संख्याओं सहित, स्ट्रिंग हैं। सत्य/असत्य मान केस-असंवेदनशील स्ट्रिंग हैं। केस-असंवेदनशील "true" के अलावा कुछ भी असत्य के रूप में व्याख्या किया जाता है। सभी विकल्प नाम केस-संवेदनशील हैं।

## I2CP पेलोड डेटा प्रारूप और मल्टीप्लेक्सिंग {#format}

I2CP द्वारा संभाले गए एंड-टू-एंड संदेश (अर्थात, क्लाइंट द्वारा [SendMessageMessage](/docs/specs/i2cp/#msg_SendMessage) में भेजे गए डेटा और क्लाइंट द्वारा [MessagePayloadMessage](/docs/specs/i2cp/#msg_MessagePayload) में प्राप्त किए गए डेटा) को [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt) द्वारा निर्दिष्ट 0x1F 0x8B 0x08 के साथ शुरू होने वाले मानक 10-बाइट ग़ज़िप हेडर के साथ ग़ज़िप किया जाता है। रिलीज़ 0.7.1 से, I2P ग़ज़िप हेडर के अनदेखे हिस्सों का उपयोग प्रोटोकॉल, from-port और to-port जानकारी शामिल करने के लिए करता है, जिससे एक ही गंतव्य पर स्ट्रीमिंग और डेटाग्राम का समर्थन होता है, और बहुल चैनलों की उपस्थिति में डेटाग्राम का उपयोग करके प्रश्न/उत्तर को विश्वसनीय तरीके से काम करने की अनुमति मिलती है।

ग़ज़िप समारोह को पूरी तरह से बंद नहीं किया जा सकता है, हालांकि `i2cp.gzip=false` सेट करने से ग़ज़िप प्रयास सेटिंग 0 पर जाती है, जो थोड़ा सा सीपीयू बचा सकता है। लागूकर्ता सामग्री की संपीड़न क्षमता के आकलन के आधार पर प्रति-सॉकेट या प्रति-संदेश आधार पर विभिन्न ग़ज़िप प्रयास चुन सकते हैं। एपीआई 0.9.57 (प्रस्ताव 161) में लागू की गई गंतव्य पैडिंग की संपीड़न क्षमता के कारण, प्रत्येक दिशा में स्ट्रीमिंग सिन पैकेटों और उत्तर योग्य डेटाग्राम की संपीड़न की अनुशंसा की जाती है, भले ही पेलोड संपीड़ित न हो। इस मामले में ग़ज़िप प्रयास 0 के लिए ग़ज़िप/गनज़िप समारोह को सरल बनाने के लिए लागूकर्ता चाह सकते हैं, जो इस मामले में ग़ज़िप लाइब्रेरी की तुलना में बड़ी दक्षता प्राप्त करेगा।

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Content</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip header 0x1F 0x8B 0x08</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip flags</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4-5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Source port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6-7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Destination port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip xflags (set to 2 to be indistinguishable from the Java implementation)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip OS)</td>
</tr>
</table>
नोट: प्रयोगात्मक प्रोटोकॉल के लिए I2P प्रोटोकॉल संख्या 224-254 आरक्षित हैं। भविष्य के विस्तार के लिए I2P प्रोटोकॉल संख्या 255 आरक्षित है।

डेटा अखंडता को [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt) द्वारा निर्दिष्ट मानक gzip CRC-32 के साथ सत्यापित किया जाता है।

## मानक IP से महत्वपूर्ण अंतर {#ip-differences}

I2CP पोर्ट्स I2P सॉकेट्स और डेटाग्राम के लिए होते हैं। ये आपके स्थानीय सॉकेट्स या पोर्ट्स से संबंधित नहीं होते। चूंकि I2P रिलीज़ 0.7.1 से पहले पोर्ट्स और प्रोटोकॉल नंबर का समर्थन नहीं करता था, इसलिए पुराने संस्करणों के साथ संगतता बनाए रखने के लिए पोर्ट्स और प्रोटोकॉल नंबर मानक आईपी की तुलना में थोड़े अलग होते हैं:

- पोर्ट 0 मान्य है और इसका विशेष अर्थ है।
- पोर्ट 1-1023 विशेष या विशेषाधिकार प्राप्त नहीं हैं।
- सर्वर डिफ़ॉल्ट रूप से पोर्ट 0 पर सुनते हैं, जिसका अर्थ है "सभी पोर्ट"।
- क्लाइंट डिफ़ॉल्ट रूप से पोर्ट 0 पर भेजते हैं, जिसका अर्थ है "कोई भी पोर्ट"।
- क्लाइंट डिफ़ॉल्ट रूप से पोर्ट 0 से भेजते हैं, जिसका अर्थ है "अनिर्दिष्ट"।
- सर्वर में पोर्ट 0 पर सेवा सुनने के साथ-साथ उच्च पोर्ट पर अन्य सेवाएं भी सुन सकती हैं। यदि ऐसा है, तो पोर्ट 0 सेवा डिफ़ॉल्ट होगी, और इससे तब कनेक्ट किया जाएगा जब आने वाला सॉकेट या डेटाग्राम पोर्ट किसी अन्य सेवा से मेल नहीं खाता होगा।
- अधिकांश I2P गंतव्यों पर केवल एक सेवा चलती है, इसलिए आप डिफ़ॉल्ट का उपयोग कर सकते हैं और I2CP पोर्ट कॉन्फ़िगरेशन को अनदेखा कर सकते हैं।
- प्रोटोकॉल 0 मान्य है और इसका अर्थ है "कोई भी प्रोटोकॉल"। हालाँकि, इसकी अनुशंसा नहीं की जाती है, और शायद यह काम नहीं करेगा। स्ट्रीमिंग के लिए आवश्यक है कि प्रोटोकॉल नंबर 6 पर सेट हो।
- स्ट्रीमिंग सॉकेट को एक आंतरिक कनेक्शन ID द्वारा ट्रैक किया जाता है। इसलिए, dest:port:dest:port:protocol के 5-टुपल के अद्वितीय होने की आवश्यकता नहीं है। उदाहरण के लिए, दो गंतव्यों के बीच समान पोर्ट के साथ कई सॉकेट हो सकते हैं। बाहर जाने वाले कनेक्शन के लिए क्लाइंट को "मुक्त पोर्ट" चुनने की आवश्यकता नहीं है।

## भविष्य का कार्य {#future}

- वर्तमान प्राधिकरण तंत्र को हैश किए गए पासवर्ड के उपयोग के लिए संशोधित किया जा सकता है।
- Create Lease Set संदेश में साइनिंग निजी कुंजियाँ शामिल हैं, जिनकी आवश्यकता नहीं है। निरसन लागू नहीं किया गया है। इसे यादृच्छिक डेटा से प्रतिस्थापित किया जाना चाहिए या हटा दिया जाना चाहिए।
- कुछ सुधार पहले परिभाषित लेकिन लागू न किए गए संदेशों का उपयोग कर सकते हैं।
