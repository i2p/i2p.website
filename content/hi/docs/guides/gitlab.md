---
title: "I2P पर GitLab चलाना"
description: "I2P के अंदर Docker और I2P router का उपयोग करके GitLab को deploy करना"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

I2P के अंदर GitLab होस्ट करना सीधा है: GitLab omnibus container चलाएं, इसे loopback पर expose करें, और I2P tunnel के माध्यम से ट्रैफ़िक forward करें। नीचे दिए गए चरण `git.idk.i2p` के लिए उपयोग किए गए configuration को दर्शाते हैं लेकिन किसी भी self-hosted instance के लिए काम करते हैं।

## 1. पूर्वापेक्षाएँ

- Debian या कोई अन्य Linux distribution जिसमें Docker Engine installed हो (`sudo apt install docker.io` या Docker के repo से `docker-ce`)।
- एक I2P router (Java I2P या i2pd) जिसमें आपके users को serve करने के लिए पर्याप्त bandwidth हो।
- Optional: एक dedicated VM ताकि GitLab और router आपके desktop environment से isolated रहें।

## 2. GitLab Image को Pull करें

```bash
docker pull gitlab/gitlab-ce:latest
```
आधिकारिक image Ubuntu बेस लेयर्स से बनाई गई है और नियमित रूप से अपडेट की जाती है। यदि आपको अतिरिक्त आश्वासन की आवश्यकता है तो [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) का ऑडिट करें।

## 3. ब्रिजिंग बनाम I2P-Only के बीच निर्णय लें

- **I2P-only** इंस्टेंस कभी भी clearnet होस्ट से संपर्क नहीं करते हैं। उपयोगकर्ता अन्य I2P सेवाओं से रिपॉजिटरी को mirror कर सकते हैं लेकिन GitHub/GitLab.com से नहीं। यह गुमनामी को अधिकतम करता है।
- **Bridged** इंस्टेंस एक HTTP proxy के माध्यम से clearnet Git होस्ट तक पहुंचते हैं। यह सार्वजनिक प्रोजेक्ट को I2P में mirror करने के लिए उपयोगी है लेकिन यह सर्वर के outbound अनुरोधों को deanonymise कर देता है।

यदि आप bridged mode चुनते हैं, तो GitLab को Docker host पर bound एक I2P HTTP proxy का उपयोग करने के लिए configure करें (उदाहरण के लिए `http://172.17.0.1:4446`)। default router proxy केवल `127.0.0.1` पर listen करता है; Docker gateway address पर bound एक नई proxy tunnel जोड़ें।

## 4. कंटेनर प्रारंभ करें

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- प्रकाशित पोर्ट को loopback से bind करें; I2P tunnels उन्हें आवश्यकतानुसार expose करेंगे।
- `/srv/gitlab/...` को अपने host के लिए उपयुक्त storage paths से बदलें।

कंटेनर चालू होने के बाद, `https://127.0.0.1:8443/` पर जाएं, एक admin पासवर्ड सेट करें, और अकाउंट लिमिट कॉन्फ़िगर करें।

## 5. I2P के माध्यम से GitLab को उजागर करें

तीन I2PTunnel **server** tunnels बनाएं:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
प्रत्येक tunnel को उपयुक्त tunnel लंबाई और bandwidth के साथ कॉन्फ़िगर करें। सार्वजनिक instances के लिए, 3 hops के साथ प्रति दिशा 4–6 tunnels एक अच्छा प्रारंभिक बिंदु है। परिणामी Base32/Base64 destinations को अपने landing page पर प्रकाशित करें ताकि उपयोगकर्ता client tunnels को कॉन्फ़िगर कर सकें।

### Destination Enforcement

यदि आप HTTP(S) tunnels का उपयोग करते हैं, तो destination enforcement सक्षम करें ताकि केवल निर्दिष्ट hostname ही सेवा तक पहुंच सके। यह tunnel को एक सामान्य proxy के रूप में दुरुपयोग होने से रोकता है।

## 6. Maintenance Tips

- जब भी आप GitLab सेटिंग्स बदलें तो `docker exec gitlab gitlab-ctl reconfigure` चलाएं।
- डिस्क उपयोग (`/srv/gitlab/data`) की निगरानी करें—Git रिपॉजिटरी तेज़ी से बढ़ती हैं।
- कॉन्फ़िगरेशन और डेटा डायरेक्टरी का नियमित रूप से बैकअप लें। GitLab के [backup rake tasks](https://docs.gitlab.com/ee/raketasks/backup_restore.html) कंटेनर के अंदर काम करते हैं।
- व्यापक नेटवर्क से सेवा की पहुंच सुनिश्चित करने के लिए client mode में एक बाहरी monitoring tunnel रखने पर विचार करें।

## 6. रखरखाव सुझाव

- [अपने एप्लिकेशन में I2P एम्बेड करना](/docs/applications/embedding/)
- [I2P पर Git (क्लाइंट गाइड)](/docs/applications/git/)
- [ऑफ़लाइन/धीमे नेटवर्क के लिए Git bundles](/docs/applications/git-bundle/)

एक अच्छी तरह से कॉन्फ़िगर किया गया GitLab instance I2P के भीतर पूरी तरह से एक सहयोगात्मक विकास केंद्र प्रदान करता है। router को स्वस्थ रखें, GitLab सुरक्षा अपडेट के साथ अद्यतित रहें, और जैसे-जैसे आपका उपयोगकर्ता आधार बढ़ता है, समुदाय के साथ समन्वय करें।
