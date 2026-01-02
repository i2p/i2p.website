---
title: "Python और I2P के साथ गोपनीयता-सचेत अनुप्रयोग विकसित करना"
date: 2018-10-23
author: "villain"
description: "Python के साथ I2P एप्लिकेशन विकास की बुनियादी अवधारणाएँ"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) गोपनीयता-जागरूक अनुप्रयोग विकसित करने के लिए एक फ्रेमवर्क प्रदान करता है। यह सामान्य इंटरनेट के ऊपर काम करने वाला एक वर्चुअल नेटवर्क है, जिसमें होस्ट अपने "वास्तविक" IP पते उजागर किए बिना डेटा का आदान-प्रदान कर सकते हैं। I2P नेटवर्क के भीतर कनेक्शन उन वर्चुअल पतों के बीच स्थापित होते हैं जिन्हें *I2P destinations* कहा जाता है। जितनी आवश्यकता हो उतने destinations रखना संभव है; आप चाहें तो प्रत्येक कनेक्शन के लिए नया destination भी उपयोग कर सकते हैं; ये दूसरी तरफ वास्तविक IP पते के बारे में कोई जानकारी उजागर नहीं करते।

यह लेख I2P अनुप्रयोग विकसित करते समय जानने योग्य मूलभूत अवधारणाओं का वर्णन करता है। कोड उदाहरण Python में लिखे गए हैं और अंतर्निहित असमकालिक फ्रेमवर्क asyncio का उपयोग करते हैं।

## SAM API को सक्रिय करना और i2plib की स्थापना

I2P क्लाइंट एप्लिकेशन के लिए कई अलग-अलग API प्रदान करता है। सामान्य क्लाइंट‑सर्वर ऐप्स I2PTunnel, HTTP और Socks प्रॉक्सी का उपयोग कर सकते हैं, जबकि Java एप्लिकेशन आमतौर पर I2CP का उपयोग करते हैं। Python जैसी अन्य भाषाओं के साथ विकास करने के लिए, सबसे अच्छा विकल्प [SAM](/docs/api/samv3/) है। मूल Java क्लाइंट इम्प्लीमेंटेशन में SAM डिफ़ॉल्ट रूप से निष्क्रिय रहता है, इसलिए हमें इसे सक्षम करना होगा। Router Console पर जाएँ, पेज "I2P internals" -> "Clients"। "Run at Startup" को चेक करें और "Start" दबाएँ, फिर "Save Client Configuration"।

![SAM API सक्षम करें](https://geti2p.net/images/enable-sam.jpeg)

[C++ कार्यान्वयन i2pd](https://i2pd.website) में SAM डिफ़ॉल्ट रूप से सक्षम है।

मैंने SAM API के लिए एक उपयोगी Python लाइब्रेरी विकसित की है, जिसका नाम [i2plib](https://github.com/l-n-s/i2plib) है। आप इसे pip का उपयोग करके इंस्टॉल कर सकते हैं या GitHub से सोर्स कोड मैन्युअल रूप से डाउनलोड कर सकते हैं।

```bash
pip install i2plib
```
This library works with the Python's built-in [asynchronous framework asyncio](https://docs.python.org/3/library/asyncio.html), so please note that code samples are taken from async functions (coroutines) which are running inside the event loop. Additional examples of i2plib usage can be found in the [source code repository](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## I2P Destination और सेशन निर्माण

I2P destination असल में एन्क्रिप्शन और क्रिप्टोग्राफ़िक हस्ताक्षर कुंजियों का एक सेट है। इस सेट की सार्वजनिक कुंजियाँ I2P नेटवर्क पर प्रकाशित की जाती हैं और IP पतों के स्थान पर कनेक्शन स्थापित करने के लिए उपयोग की जाती हैं।

इस प्रकार आप [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination) बनाते हैं:

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
base32 पता एक हैश होता है जिसका उपयोग अन्य पीयर्स नेटवर्क में आपके पूर्ण Destination का पता लगाने के लिए करते हैं। यदि आप अपने प्रोग्राम में इस destination को स्थायी पता के रूप में उपयोग करने की योजना बना रहे हैं, तो *dest.private_key.data* से बाइनरी डेटा को एक स्थानीय फ़ाइल में सहेजें।

अब आप एक SAM session बना सकते हैं, जिसका शाब्दिक अर्थ I2P में Destination (I2P पहचान/पता) को ऑनलाइन करना है:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
महत्वपूर्ण नोट: जब तक *session_writer* सॉकेट खुला रखा जाता है, Destination ऑनलाइन रहेगा। यदि आप इसे बंद करना चाहें, तो आप *session_writer.close()* कॉल कर सकते हैं।

## Making outgoing connections

अब जब Destination (गंतव्य) ऑनलाइन है, आप इसका उपयोग करके अन्य पीयर्स से कनेक्ट कर सकते हैं। उदाहरण के लिए, इस तरह आप "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p" से कनेक्ट करते हैं, HTTP GET अनुरोध भेजते हैं और प्रतिक्रिया पढ़ते हैं (यह "i2p-projekt.i2p" वेब सर्वर है):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## आने वाले कनेक्शनों को स्वीकार करना

आउटगोइंग कनेक्शन बनाना आसान है, लेकिन जब आप कनेक्शन स्वीकार करते हैं, तो एक महत्वपूर्ण बात है। जब कोई नया क्लाइंट कनेक्ट हो जाता है, SAM API सॉकेट पर क्लाइंट के Destination (गंतव्य) का base64-एन्कोडेड रूप वाली एक ASCII स्ट्रिंग भेजता है। चूंकि Destination और डेटा एक ही चंक में आ सकते हैं, आपको इसका ध्यान रखना चाहिए।

एक साधारण PING-PONG सर्वर इस प्रकार दिखता है। यह आने वाले कनेक्शन को स्वीकार करता है, क्लाइंट के Destination (I2P में पहचान/गंतव्य) को *remote_destination* वेरिएबल में सहेजता है और "PONG" स्ट्रिंग वापस भेजता है:

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## अधिक जानकारी

यह लेख TCP-जैसे स्ट्रीमिंग प्रोटोकॉल के उपयोग का वर्णन करता है। SAM API डाटाग्राम भेजने और प्राप्त करने के लिए UDP-जैसा प्रोटोकॉल भी प्रदान करता है। यह सुविधा बाद में i2plib में जोड़ी जाएगी।

यह केवल बुनियादी जानकारी है, लेकिन I2P का उपयोग करके अपना खुद का प्रोजेक्ट शुरू करने के लिए यह पर्याप्त है। Invisible Internet (अदृश्य इंटरनेट) गोपनीयता-केंद्रित अनुप्रयोगों के हर तरह के विकास के लिए एक बेहतरीन उपकरण है। नेटवर्क की ओर से कोई डिज़ाइन संबंधी प्रतिबंध नहीं हैं; वे अनुप्रयोग क्लाइंट-सर्वर के साथ-साथ P2P भी हो सकते हैं।

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
