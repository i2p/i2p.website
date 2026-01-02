---
title: "I2P रीसीड सर्वर बनाना और चलाना"
description: "नए राउटर्स को नेटवर्क में शामिल होने में मदद करने के लिए I2P reseed सर्वर सेटअप और संचालन की संपूर्ण गाइड"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed होस्ट I2P नेटवर्क के लिए महत्वपूर्ण इंफ्रास्ट्रक्चर हैं, जो bootstrap प्रक्रिया के दौरान नए routers को नोड्स के प्रारंभिक समूह प्रदान करते हैं। यह गाइड आपको अपना स्वयं का reseed सर्वर सेटअप करने और चलाने की प्रक्रिया से परिचित कराएगी।

## I2P Reseed सर्वर क्या है?

एक I2P reseed सर्वर नए routers को I2P नेटवर्क में एकीकृत करने में मदद करता है:

- **प्रारंभिक पीयर डिस्कवरी प्रदान करना**: नए routers को कनेक्ट करने के लिए नेटवर्क नोड्स का एक प्रारंभिक सेट प्राप्त होता है
- **Bootstrap रिकवरी**: उन routers की मदद करना जो कनेक्शन बनाए रखने में कठिनाई का सामना कर रहे हैं
- **सुरक्षित वितरण**: Reseeding प्रक्रिया एन्क्रिप्टेड और डिजिटली साइन की गई है ताकि नेटवर्क सुरक्षा सुनिश्चित हो सके

जब एक नया I2P router पहली बार शुरू होता है (या अपने सभी peer connections खो देता है), तो यह reseed servers से संपर्क करता है ताकि router information का एक प्रारंभिक सेट डाउनलोड कर सके। इससे नए router को अपना network database बनाना और tunnels स्थापित करना शुरू करने में मदद मिलती है।

## पूर्वापेक्षाएँ

शुरू करने से पहले, आपको यह चाहिए होगा:

- रूट एक्सेस के साथ एक Linux सर्वर (Debian/Ubuntu अनुशंसित)
- आपके सर्वर की ओर इशारा करता एक डोमेन नाम
- कम से कम 1GB RAM और 10GB डिस्क स्पेस
- netDb को पॉप्युलेट करने के लिए सर्वर पर एक चालू I2P router
- Linux सिस्टम एडमिनिस्ट्रेशन से बुनियादी परिचय

## सर्वर तैयार करना

### Step 1: Update System and Install Dependencies

पहले, अपने सिस्टम को अपडेट करें और आवश्यक पैकेजों को इंस्टॉल करें:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
यह इंस्टॉल करता है: - **golang-go**: Go प्रोग्रामिंग भाषा रनटाइम - **git**: वर्जन कंट्रोल सिस्टम - **make**: बिल्ड ऑटोमेशन टूल - **docker.io & docker-compose**: Nginx Proxy Manager चलाने के लिए कंटेनर प्लेटफॉर्म

![आवश्यक पैकेजों की स्थापना](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

reseed-tools रिपॉजिटरी को क्लोन करें और एप्लिकेशन को बिल्ड करें:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
`reseed-tools` पैकेज reseed सर्वर चलाने के लिए मुख्य कार्यक्षमता प्रदान करता है। यह निम्नलिखित को संभालता है: - आपके स्थानीय network database से router जानकारी एकत्र करना - router info को signed SU3 फाइलों में पैकेज करना - इन फाइलों को HTTPS के माध्यम से serve करना

![Cloning reseed-tools repository](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

अपने reseed server का SSL certificate और private key जनरेट करें:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**महत्वपूर्ण पैरामीटर**: - `--signer`: आपका ईमेल पता (`admin@stormycloud.org` को अपने ईमेल से बदलें) - `--netdb`: आपके I2P router के network database का पथ - `--port`: आंतरिक पोर्ट (8443 अनुशंसित है) - `--ip`: localhost से बाइंड करें (हम सार्वजनिक पहुँच के लिए reverse proxy का उपयोग करेंगे) - `--trustProxy`: reverse proxy से X-Forwarded-For headers पर भरोसा करें

यह कमांड निम्नलिखित जेनरेट करेगा: - SU3 फाइलों पर हस्ताक्षर करने के लिए एक प्राइवेट की - सुरक्षित HTTPS कनेक्शन के लिए एक SSL सर्टिफिकेट

![SSL certificate generation](/images/guides/reseed/reseed_03.png)

### चरण 1: सिस्टम अपडेट करें और डिपेंडेंसी इंस्टॉल करें

**महत्वपूर्ण**: `/home/i2p/.reseed/` में स्थित उत्पन्न keys का सुरक्षित रूप से backup लें:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
इस बैकअप को सीमित पहुंच वाले सुरक्षित, एन्क्रिप्टेड स्थान पर संग्रहीत करें। ये keys आपके reseed server के संचालन के लिए आवश्यक हैं और इन्हें सावधानीपूर्वक सुरक्षित रखा जाना चाहिए।

## Configuring the Service

### चरण 2: Reseed Tools को Clone और Build करें

systemd सर्विस बनाएं ताकि reseed सर्वर स्वचालित रूप से चले:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**याद रखें कि** `admin@stormycloud.org` को अपने स्वयं के ईमेल पते से बदलें।

अब सेवा को सक्षम और प्रारंभ करें:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
जांचें कि सेवा चल रही है:

```bash
sudo systemctl status reseed
```
![reseed सेवा स्थिति सत्यापित करना](/images/guides/reseed/reseed_04.png)

### चरण 3: SSL प्रमाणपत्र जनरेट करें

इष्टतम प्रदर्शन के लिए, आप router जानकारी को ताज़ा करने के लिए reseed service को समय-समय पर पुनः आरंभ करना चाह सकते हैं:

```bash
sudo crontab -e
```
हर 3 घंटे में सेवा को पुनः आरंभ करने के लिए यह लाइन जोड़ें:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

reseed सर्वर localhost:8443 पर चलता है और सार्वजनिक HTTPS ट्रैफ़िक को संभालने के लिए एक reverse proxy की आवश्यकता होती है। हम इसकी उपयोग में आसानी के लिए Nginx Proxy Manager की अनुशंसा करते हैं।

### चरण 4: अपनी Keys का बैकअप लें

Docker का उपयोग करके Nginx Proxy Manager को Deploy करें:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
यह निम्नलिखित को एक्सपोज़ करता है: - **Port 80**: HTTP traffic - **Port 81**: Admin interface - **Port 443**: HTTPS traffic

### Configure Proxy Manager

1. एडमिन इंटरफेस को `http://your-server-ip:81` पर एक्सेस करें

2. डिफ़ॉल्ट क्रेडेंशियल्स से लॉगिन करें:
   - **ईमेल**: admin@example.com
   - **पासवर्ड**: changeme

**महत्वपूर्ण**: पहली लॉगिन के तुरंत बाद इन क्रेडेंशियल्स को बदलें!

![Nginx Proxy Manager लॉगिन](/images/guides/reseed/reseed_05.png)

3. **Proxy Hosts** पर जाएं और **Add Proxy Host** पर क्लिक करें

![प्रॉक्सी होस्ट जोड़ना](/images/guides/reseed/reseed_06.png)

4. प्रॉक्सी होस्ट को कॉन्फ़िगर करें:
   - **Domain Name**: आपका reseed डोमेन (उदाहरण के लिए, `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - **Cache Assets** को सक्षम करें
   - **Block Common Exploits** को सक्षम करें
   - **Websockets Support** को सक्षम करें

![proxy host विवरण कॉन्फ़िगर करना](/images/guides/reseed/reseed_07.png)

5. **SSL** टैब में:
   - **Request a new SSL Certificate** (Let's Encrypt) चुनें
   - **Force SSL** सक्षम करें
   - **HTTP/2 Support** सक्षम करें
   - Let's Encrypt Terms of Service से सहमत हों

![SSL certificate configuration](/images/guides/reseed/reseed_08.png)

6. **Save** पर क्लिक करें

आपका reseed server अब `https://reseed.example.com` पर accessible होना चाहिए

![सफल reseed सर्वर कॉन्फ़िगरेशन](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

एक बार जब आपका reseed सर्वर operational हो जाए, तो I2P डेवलपर्स से संपर्क करें ताकि इसे आधिकारिक reseed सर्वर सूची में जोड़ा जा सके।

### चरण 5: Systemd सेवा बनाएं

**zzz** (I2P lead developer) को निम्नलिखित जानकारी के साथ ईमेल करें:

- **I2P ईमेल**: zzz@mail.i2p
- **Clearnet ईमेल**: zzz@i2pmail.org

### चरण 6: वैकल्पिक - आवधिक पुनरारंभ कॉन्फ़िगर करें

अपने ईमेल में शामिल करें:

1. **Reseed सर्वर URL**: पूर्ण HTTPS URL (उदाहरण के लिए, `https://reseed.example.com`)
2. **सार्वजनिक reseed प्रमाणपत्र**: `/home/i2p/.reseed/` पर स्थित (`.crt` फ़ाइल संलग्न करें)
3. **संपर्क ईमेल**: सर्वर रखरखाव सूचनाओं के लिए आपकी पसंदीदा संपर्क विधि
4. **सर्वर स्थान**: वैकल्पिक लेकिन सहायक (देश/क्षेत्र)
5. **अपेक्षित अपटाइम**: सर्वर को बनाए रखने के लिए आपकी प्रतिबद्धता

### Verification

I2P डेवलपर्स यह सत्यापित करेंगे कि आपका reseed सर्वर: - उचित रूप से कॉन्फ़िगर किया गया है और router जानकारी प्रदान कर रहा है - वैध SSL सर्टिफिकेट्स का उपयोग कर रहा है - सही ढंग से साइन की गई SU3 फ़ाइलें प्रदान कर रहा है - सुलभ और उत्तरदायी है

एक बार स्वीकृत होने के बाद, आपका reseed server I2P routers के साथ वितरित की जाने वाली सूची में जोड़ दिया जाएगा, जिससे नए उपयोगकर्ताओं को नेटवर्क से जुड़ने में मदद मिलेगी!

## Monitoring and Maintenance

### Nginx Proxy Manager इंस्टॉल करें

अपनी reseed सेवा की निगरानी करें:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### प्रॉक्सी मैनेजर को कॉन्फ़िगर करें

सिस्टम संसाधनों पर नज़र रखें:

```bash
htop
df -h
```
### Update Reseed Tools

नवीनतम सुधार प्राप्त करने के लिए reseed-tools को समय-समय पर अपडेट करें:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### संपर्क जानकारी

यदि Nginx Proxy Manager के माध्यम से Let's Encrypt का उपयोग कर रहे हैं, तो प्रमाणपत्र स्वतः नवीनीकृत हो जाएंगे। नवीनीकरण कार्य कर रहा है इसकी पुष्टि करें:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## सेवा को कॉन्फ़िगर करना

### आवश्यक जानकारी

त्रुटियों के लिए लॉग जांचें:

```bash
sudo journalctl -u reseed -n 50
```
सामान्य समस्याएं: - I2P router चालू नहीं है या network database खाली है - Port 8443 पहले से उपयोग में है - `/home/i2p/.reseed/` directory के साथ अनुमति संबंधी समस्याएं

### सत्यापन

सुनिश्चित करें कि आपका I2P router चल रहा है और उसने अपना network database populate कर लिया है:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
आपको कई `.dat` फ़ाइलें दिखाई देनी चाहिए। यदि खाली है, तो अपने I2P router को peers खोजने के लिए प्रतीक्षा करें।

### SSL Certificate Errors

अपने प्रमाणपत्रों को मान्य होने की पुष्टि करें:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### सेवा की स्थिति जांचें

जांचें: - DNS रिकॉर्ड आपके सर्वर की ओर सही तरीके से पॉइंट कर रहे हैं - Firewall पोर्ट 80 और 443 की अनुमति देता है - Nginx Proxy Manager चल रहा है: `docker ps`

## Security Considerations

- **अपनी निजी कुंजियों को सुरक्षित रखें**: `/home/i2p/.reseed/` की सामग्री को कभी साझा या उजागर न करें
- **नियमित अपडेट**: सिस्टम पैकेज, Docker, और reseed-tools को अपडेट रखें
- **लॉग की निगरानी करें**: संदिग्ध एक्सेस पैटर्न पर नज़र रखें
- **Rate limiting**: दुरुपयोग को रोकने के लिए rate limiting लागू करने पर विचार करें
- **Firewall नियम**: केवल आवश्यक पोर्ट (80, 443, 81 admin के लिए) को expose करें
- **Admin interface**: Nginx Proxy Manager admin interface (पोर्ट 81) को विश्वसनीय IPs तक सीमित रखें

## Contributing to the Network

reseed सर्वर चलाकर, आप I2P नेटवर्क के लिए महत्वपूर्ण इंफ्रास्ट्रक्चर प्रदान कर रहे हैं। अधिक निजी और विकेन्द्रीकृत इंटरनेट में योगदान देने के लिए धन्यवाद!

प्रश्नों या सहायता के लिए, I2P समुदाय से संपर्क करें: - **Forum**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: विभिन्न नेटवर्क पर #i2p - **Development**: [i2pgit.org](https://i2pgit.org)

---

IMPORTANT: केवल अनुवाद प्रदान करें। प्रश्न न पूछें, स्पष्टीकरण न दें, या कोई टिप्पणी न जोड़ें। भले ही टेक्स्ट केवल एक शीर्षक हो या अधूरा लगे, इसे जैसा है वैसा ही अनुवाद करें।

*गाइड मूल रूप से [Stormy Cloud](https://www.stormycloud.org) द्वारा बनाई गई, I2P दस्तावेज़ीकरण के लिए अनुकूलित।*
