---
title: "अदृश्य मल्टीहोमिंग"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "खुला"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## अवलोकन

यह प्रस्ताव एक protocol के लिए एक design को रेखांकित करता है जो किसी I2P client, service या external balancer process को कई routers को transparently manage करने में सक्षम बनाता है जो एक single [Destination](http://localhost:63465/docs/specs/common-structures/#destination) को host कर रहे हैं।

यह प्रस्ताव वर्तमान में कोई ठोस implementation निर्दिष्ट नहीं करता। इसे [I2CP](/docs/specs/i2cp/) के extension के रूप में, या एक नए protocol के रूप में implement किया जा सकता है।

## प्रेरणा

Multihoming वह स्थिति है जहाँ समान Destination को host करने के लिए कई router का उपयोग किया जाता है। I2P के साथ multihome करने का वर्तमान तरीका यह है कि प्रत्येक router पर समान Destination को स्वतंत्र रूप से चलाया जाए; किसी भी विशेष समय पर clients द्वारा उपयोग किया जाने वाला router वह होता है जिसने सबसे अंत में LeaseSet publish किया हो।

यह एक hack है और संभावित रूप से बड़ी websites के लिए scale पर काम नहीं करेगा। मान लेते हैं कि हमारे पास 100 multihoming router हैं जिनमें से हर एक के पास 16 tunnels हैं। यह हर 10 मिनट में 1600 LeaseSet publishes होता है, या लगभग 3 प्रति सेकंड। floodfills overwhelmed हो जाएंगे और throttles शुरू हो जाएंगे। और यह तो lookup traffic का जिक्र करने से पहले की बात है।

प्रस्ताव 123 इस समस्या को एक मेटा-LeaseSet के साथ हल करता है, जो 100 वास्तविक LeaseSet हैश की सूची बनाता है। एक लुकअप दो-चरणीय प्रक्रिया बन जाता है: पहले मेटा-LeaseSet को देखना, और फिर नामित LeaseSet में से किसी एक को देखना। यह लुकअप ट्रैफिक समस्या का एक अच्छा समाधान है, लेकिन अपने आप में यह एक महत्वपूर्ण गोपनीयता लीक बनाता है: प्रकाशित मेटा-LeaseSet की निगरानी करके यह निर्धारित करना संभव है कि कौन से multihoming router ऑनलाइन हैं, क्योंकि प्रत्येक वास्तविक LeaseSet एक अकेले router से मेल खाता है।

हमें I2P client या service के लिए एक तरीके की आवश्यकता है जो एक single Destination को multiple routers में फैला सके, ऐसे तरीके से जो single router के उपयोग से अलग न दिखे (LeaseSet के दृष्टिकोण से)।

## डिज़ाइन

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

निम्नलिखित वांछित कॉन्फ़िगरेशन की कल्पना करें:

- एक Destination के साथ एक client application।
- चार routers, जिनमें से प्रत्येक तीन inbound tunnels का प्रबंधन करता है।
- सभी बारह tunnels को एक single LeaseSet में प्रकाशित किया जाना चाहिए।

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### परिभाषाएं

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### उच्च-स्तरीय अवलोकन

- एक Destination को लोड करें या जेनरेट करें।

- प्रत्येक router के साथ एक session खोलें, जो Destination से जुड़ा हो।

- समय-समय पर (लगभग हर दस मिनट में, लेकिन tunnel की जीवंतता के आधार पर कम या ज्यादा):

- प्रत्येक router से fast tier प्राप्त करें।

- प्रत्येक router के लिए tunnels बनाने हेतु peers के superset का उपयोग करें।

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- सभी सक्रिय routers से सक्रिय inbound tunnels का सेट एकत्र करें, और एक
    LeaseSet बनाएं।

- एक या अधिक routers के माध्यम से LeaseSet को प्रकाशित करें।

### सिंगल-क्लाइंट

इस configuration को बनाने और प्रबंधित करने के लिए, client को वर्तमान में [I2CP](/docs/specs/i2cp/) द्वारा प्रदान की जाने वाली सुविधाओं के अतिरिक्त निम्नलिखित नई functionality की आवश्यकता है:

- एक router को tunnels बनाने के लिए कहें, उनके लिए LeaseSet बनाए बिना।
- inbound pool में मौजूदा tunnels की सूची प्राप्त करें।

इसके अतिरिक्त, निम्नलिखित कार्यक्षमता client को अपनी tunnels का प्रबंधन करने में महत्वपूर्ण लचीलापन प्रदान करेगी:

- एक router के fast tier की contents प्राप्त करें।
- किसी router को दिए गए peers की list का उपयोग करके inbound या outbound tunnel बनाने के लिए कहें।

### मल्टी-क्लाइंट

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### सामान्य client प्रक्रिया

**सेशन बनाएं** - दिए गए Destination के लिए एक सेशन बनाएं।

**Session Status** - पुष्टि कि session स्थापित हो गया है, और client अब tunnel बनाना शुरू कर सकता है।

**Get Fast Tier** - उन peers की सूची का अनुरोध करें जिनके माध्यम से router वर्तमान में tunnels बनाने पर विचार करेगा।

**Peer List** - router को ज्ञात peers की एक सूची।

**Tunnel बनाएं** - Router से अनुरोध करें कि वह निर्दिष्ट peers के माध्यम से एक नया tunnel बनाए।

**Tunnel Status** - किसी विशिष्ट tunnel build का परिणाम, जब यह उपलब्ध हो जाता है।

**Tunnel Pool प्राप्त करें** - Destination के लिए inbound या outbound pool में मौजूदा tunnels की सूची का अनुरोध करें।

**Tunnel List** - अनुरोधित पूल के लिए tunnels की सूची।

**LeaseSet प्रकाशित करें** - राउटर से अनुरोध करें कि वह प्रदान किए गए LeaseSet को Destination के लिए आउटबाउंड टनल में से किसी एक के माध्यम से प्रकाशित करे। कोई उत्तर स्थिति की आवश्यकता नहीं है; राउटर को तब तक पुनः प्रयास जारी रखना चाहिए जब तक वह संतुष्ट न हो जाए कि LeaseSet प्रकाशित हो गया है।

**Send Packet** - क्लाइंट से एक आउटगोइंग packet। वैकल्पिक रूप से एक outbound tunnel निर्दिष्ट करता है जिसके माध्यम से packet भेजा जाना चाहिए (होना चाहिए?)।

**Send Status** - क्लाइंट को packet भेजने की सफलता या असफलता की जानकारी देता है।

**Packet Received** - क्लाइंट के लिए एक आने वाला पैकेट। वैकल्पिक रूप से उस inbound tunnel को निर्दिष्ट करता है जिसके माध्यम से पैकेट प्राप्त हुआ था(?)

## Security implications

router के दृष्टिकोण से, यह डिज़ाइन कार्यात्मक रूप से मौजूदा स्थिति के बराबर है। router अभी भी सभी tunnel बनाता है, अपने स्वयं के peer profile बनाए रखता है, और router तथा client operations के बीच अलगाव को लागू करता है। डिफ़ॉल्ट कॉन्फ़िगरेशन में यह बिल्कुल समान है, क्योंकि उस router के लिए tunnel उसके अपने fast tier से बनाए जाते हैं।

netDB के दृष्टिकोण से, इस protocol के माध्यम से बनाया गया एक single LeaseSet status quo के समान है, क्योंकि यह पहले से मौजूद functionality का उपयोग करता है। हालांकि, 16 Leases के करीब पहुंचने वाले बड़े LeaseSets के लिए, किसी observer के लिए यह निर्धारित करना संभव हो सकता है कि LeaseSet multihomed है:

- तेज़ टियर का वर्तमान अधिकतम आकार 75 peers है। Inbound Gateway
  (IBGW, वह नोड जो Lease में प्रकाशित होता है) को टियर के एक हिस्से से चुना जाता है
  (प्रत्येक tunnel pool के लिए hash द्वारा यादृच्छिक रूप से विभाजित, गिनती द्वारा नहीं):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

इसका मतलब है कि औसतन IBGWs 20-30 peers के एक सेट से होंगे।

- एक single-homed setup में, एक पूर्ण 16-tunnel LeaseSet में 16 IBGWs होंगे जो (मान लें) 20 peers के set से randomly चुने गए होंगे।

- एक डिफ़ॉल्ट कॉन्फ़िगरेशन का उपयोग करते हुए 4-router multihomed सेटअप में, एक पूर्ण 16-tunnel LeaseSet में अधिकतम 80 peers के सेट से यादृच्छिक रूप से चुने गए 16 IBGWs होंगे, हालांकि routers के बीच सामान्य peers का एक अंश होने की संभावना है।

इस प्रकार डिफ़ॉल्ट कॉन्फ़िगरेशन के साथ, सांख्यिकीय विश्लेषण के माध्यम से यह पता लगाना संभव हो सकता है कि इस प्रोटोकॉल द्वारा एक LeaseSet जेनरेट किया जा रहा है। यह पता लगाना भी संभव हो सकता है कि कितने router हैं, हालांकि तेज़ tiers पर churn का प्रभाव इस विश्लेषण की प्रभावशीलता को कम कर देगा।

चूंकि client का peers के चयन पर पूर्ण नियंत्रण होता है, peers के एक सीमित समूह से IBGWs का चयन करके इस जानकारी के रिसाव को कम या समाप्त किया जा सकता है।

## Compatibility

यह डिज़ाइन नेटवर्क के साथ पूर्णतः backwards-compatible है, क्योंकि LeaseSet format में कोई बदलाव नहीं हैं। सभी routers को नए protocol के बारे में जानना होगा, लेकिन यह कोई चिंता की बात नहीं है क्योंकि वे सभी एक ही entity द्वारा नियंत्रित होंगे।

## Performance and scalability notes

इस प्रस्ताव द्वारा प्रति LeaseSet 16 Leases की ऊपरी सीमा अपरिवर्तित है। उन Destinations के लिए जिन्हें इससे अधिक tunnels की आवश्यकता है, दो संभावित नेटवर्क संशोधन हैं:

- LeaseSets के आकार की ऊपरी सीमा बढ़ाना। यह लागू करने के लिए सबसे सरल होगा (हालांकि इसके व्यापक रूप से उपयोग होने से पहले व्यापक नेटवर्क समर्थन की आवश्यकता होगी), लेकिन बड़े पैकेट आकार के कारण धीमी lookups का परिणाम हो सकता है। अधिकतम संभव LeaseSet आकार अंतर्निहित transports के MTU द्वारा परिभाषित होता है, और इसलिए लगभग 16kB होता है।

- Proposal 123 को tiered LeaseSets के लिए implement करें। इस proposal के साथ मिलकर,
  sub-LeaseSets के लिए Destinations को कई routers में फैलाया जा सकता है, जो एक clearnet service के लिए कई IP addresses की तरह प्रभावी रूप से काम करता है।

## Acknowledgements

psi के साथ हुई चर्चा के लिए धन्यवाद जिसके कारण यह प्रस्ताव बना।
