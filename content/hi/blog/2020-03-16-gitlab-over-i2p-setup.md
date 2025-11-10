---
title: "I2P पर Gitlab सेटअप"
date: 2020-03-16
author: "idk"
description: "I2P Git repositories का मिरर उपलब्ध कराएँ और दूसरों के लिए Clearnet (सार्वजनिक इंटरनेट) repositories का ब्रिज प्रदान करें"
categories: ["development"]
---

यह वह सेटअप प्रक्रिया है जिसका उपयोग मैं Gitlab और I2P को कॉन्फ़िगर करने varten करता हूँ, जहाँ सेवा को स्वयं प्रबंधित करने के लिए Docker का उपयोग किया जाता है। इस तरीके से I2P पर Gitlab की होस्टिंग करना बहुत आसान है; इसे एक व्यक्ति बिना अधिक कठिनाई के प्रशासित कर सकता है। ये निर्देश किसी भी Debian-आधारित सिस्टम पर काम करने चाहिए और उन सभी सिस्टमों पर आसानी से अनुकूलित किए जा सकते हैं जहाँ Docker और एक I2P router उपलब्ध हों।

## निर्भरताएँ और Docker

क्योंकि Gitlab एक कंटेनर में चलता है, हमें अपने मुख्य सिस्टम पर केवल कंटेनर के लिए आवश्यक निर्भरताएँ ही स्थापित करनी होती हैं। सुविधाजनक रूप से, आप इसके साथ अपनी सभी आवश्यक चीज़ें स्थापित कर सकते हैं:

```
sudo apt install docker.io
```
## Docker कंटेनर प्राप्त करें

docker इंस्टॉल हो जाने के बाद, आप gitlab के लिए आवश्यक docker कंटेनर प्राप्त कर सकते हैं। *उन्हें अभी न चलाएँ।*

```
docker pull gitlab/gitlab-ce
```
## Gitlab के लिए I2P HTTP प्रॉक्सी सेट अप करें (महत्वपूर्ण जानकारी, वैकल्पिक चरण)

I2P के भीतर स्थित Gitlab सर्वरों को I2P के बाहर इंटरनेट पर मौजूद सर्वरों के साथ इंटरैक्ट करने की क्षमता के साथ या बिना चलाया जा सकता है। जिस स्थिति में Gitlab सर्वर को I2P के बाहर के सर्वरों के साथ इंटरैक्ट करने की *अनुमति नहीं है*, उस स्थिति में I2P के बाहर इंटरनेट पर किसी git सर्वर से git रिपोजिटरी क्लोन करके उनकी गुमनामी तोड़ी नहीं जा सकती।

जिस स्थिति में Gitlab सर्वर को I2P के बाहर के सर्वरों के साथ इंटरैक्ट करना *अनुमत* हो, यह उपयोगकर्ताओं के लिए एक "Bridge" के रूप में कार्य कर सकता है, जो इसका उपयोग करके I2P के बाहर की सामग्री को I2P-प्रवेशयोग्य स्रोत पर मिरर कर सकते हैं, हालांकि इस स्थिति में यह *गुमनाम नहीं है*।

**यदि आप वेब रिपोज़िटरीज़ तक पहुँच वाली ब्रिज्ड, गैर-अनाम Gitlab इंस्टेंस रखना चाहते हैं**, कोई अतिरिक्त संशोधन आवश्यक नहीं है।

**यदि आप एक I2P-Only Gitlab इंस्टेंस रखना चाहते हैं, जिसे Web-Only रिपॉज़िटरीज़ तक पहुंच न हो**, तो आपको Gitlab को I2P HTTP प्रॉक्सी का उपयोग करने के लिए कॉन्फ़िगर करना होगा। क्योंकि डिफ़ॉल्ट I2P HTTP प्रॉक्सी केवल `127.0.0.1` पर सुनती है, आपको Docker के लिए एक नई प्रॉक्सी सेटअप करनी होगी जो Docker नेटवर्क के Host/Gateway पते पर सुनती हो, जो आमतौर पर `172.17.0.1` होता है। मैं इसे पोर्ट `4446` पर कॉन्फ़िगर करता हूँ।

## स्थानीय रूप से कंटेनर प्रारंभ करें

जब आप वह सेटअप कर लें, तो आप कंटेनर शुरू कर सकते हैं और अपने Gitlab instance को स्थानीय रूप से प्रकाशित कर सकते हैं:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
अपने स्थानीय Gitlab इंस्टेंस पर जाएँ और अपना एडमिन खाता सेट अप करें। एक मजबूत पासवर्ड चुनें, और अपने संसाधनों के अनुरूप उपयोगकर्ता खातों की सीमाएँ कॉन्फ़िगर करें।

## अपनी सेवा के tunnels सेट अप करें और Hostname के लिए पंजीकरण करें

जब आप Gitlab को स्थानीय रूप से सेट अप कर लें, तो I2P Router console पर जाएँ। आपको दो सर्वर tunnels सेट अप करनी होंगी, एक TCP port 8080 पर Gitlab वेब (HTTP) इंटरफ़ेस की ओर, और एक TCP Port 8022 पर Gitlab SSH इंटरफ़ेस की ओर।

### Gitlab Web(HTTP) Interface

वेब इंटरफ़ेस के लिए, "HTTP" server tunnel का उपयोग करें। http://127.0.0.1:7657/i2ptunnelmgr से "New Tunnel Wizard" लॉन्च करें और निम्न मान दर्ज करें:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

SSH इंटरफ़ेस के लिए, "Standard" server tunnel का उपयोग करें। http://127.0.0.1:7657/i2ptunnelmgr से "New Tunnel Wizard" लॉन्च करें और निम्न मान दर्ज करें:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

अंत में, यदि आपने या तो `gitlab.rb` में परिवर्तन किया है या कोई hostname (होस्टनेम) रजिस्टर किया है, तो सेटिंग्स प्रभावी होने के लिए आपको gitlab सेवा को पुनः प्रारंभ करना होगा।
