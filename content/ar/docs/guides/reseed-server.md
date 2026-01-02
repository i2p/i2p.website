---
title: "إنشاء وتشغيل خادم إعادة البذر (Reseed Server) الخاص بـ I2P"
description: "دليل شامل لإعداد وتشغيل خادم reseed من I2P لمساعدة أجهزة router الجديدة على الانضمام إلى الشبكة"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

خوادم إعادة البذر (Reseed hosts) هي بنية تحتية حيوية لشبكة I2P، حيث توفر لأجهزة router الجديدة مجموعة أولية من العقد خلال عملية الإقلاع الأولي (bootstrap). سيرشدك هذا الدليل خلال إعداد وتشغيل خادم reseed خاص بك.

## ما هو خادم إعادة البذر (Reseed Server) في I2P؟

يساعد خادم إعادة البذر (reseed server) في I2P على دمج أجهزة التوجيه الجديدة في شبكة I2P من خلال:

- **توفير الاكتشاف الأولي للنظراء**: تتلقى أجهزة Router الجديدة مجموعة أولية من عقد الشبكة للاتصال بها
- **استعادة Bootstrap**: مساعدة أجهزة Router التي تواجه صعوبة في الحفاظ على الاتصالات
- **التوزيع الآمن**: عملية إعادة التوزيع (reseeding) مشفرة وموقعة رقمياً لضمان أمان الشبكة

عندما يبدأ router I2P جديد للمرة الأولى (أو فقد جميع اتصالات النظراء الخاصة به)، فإنه يتصل بخوادم reseed لتنزيل مجموعة أولية من معلومات الـ router. هذا يسمح للـ router الجديد بالبدء في بناء قاعدة بيانات الشبكة الخاصة به وإنشاء tunnels.

## المتطلبات الأساسية

قبل البدء، ستحتاج إلى:

- خادم Linux (يُفضّل Debian/Ubuntu) مع صلاحيات root
- اسم نطاق يشير إلى خادمك
- ذاكرة وصول عشوائي لا تقل عن 1GB ومساحة قرص 10GB
- router I2P يعمل على الخادم لملء قاعدة بيانات الشبكة (netDb)
- إلمام أساسي بإدارة أنظمة Linux

## إعداد الخادم

### Step 1: Update System and Install Dependencies

أولاً، قم بتحديث نظامك وتثبيت الحزم المطلوبة:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
هذا يثبت: - **golang-go**: بيئة تشغيل لغة البرمجة Go - **git**: نظام التحكم في الإصدارات - **make**: أداة أتمتة البناء - **docker.io & docker-compose**: منصة الحاويات لتشغيل Nginx Proxy Manager

![تثبيت الحزم المطلوبة](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

استنسخ مستودع reseed-tools وقم ببناء التطبيق:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
حزمة `reseed-tools` توفر الوظائف الأساسية لتشغيل خادم reseed. تتعامل مع: - جمع معلومات router من قاعدة بيانات الشبكة المحلية الخاصة بك - تعبئة معلومات router في ملفات SU3 موقعة - تقديم هذه الملفات عبر HTTPS

![استنساخ مستودع reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

قم بإنشاء شهادة SSL والمفتاح الخاص لخادم reseed الخاص بك:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**المعاملات المهمة**: - `--signer`: عنوان بريدك الإلكتروني (استبدل `admin@stormycloud.org` بعنوانك الخاص) - `--netdb`: المسار إلى قاعدة بيانات الشبكة الخاصة بموجه I2P - `--port`: المنفذ الداخلي (يُنصح باستخدام 8443) - `--ip`: الربط بـ localhost (سنستخدم reverse proxy للوصول العام) - `--trustProxy`: الوثوق برؤوس X-Forwarded-For من الـ reverse proxy

سيقوم الأمر بإنشاء: - مفتاح خاص لتوقيع ملفات SU3 - شهادة SSL لاتصالات HTTPS الآمنة

![توليد شهادة SSL](/images/guides/reseed/reseed_03.png)

### الخطوة 1: تحديث النظام وتثبيت التبعيات

**هام جداً**: احتفظ بنسخة احتياطية آمنة للمفاتيح المُولّدة الموجودة في `/home/i2p/.reseed/`:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
قم بتخزين هذه النسخة الاحتياطية في موقع آمن ومشفر مع وصول محدود. هذه المفاتيح ضرورية لتشغيل خادم إعادة البذر الخاص بك ويجب حمايتها بعناية.

## Configuring the Service

### الخطوة 2: استنساخ وبناء أدوات Reseed

أنشئ خدمة systemd لتشغيل خادم إعادة البذر تلقائيًا:

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
**تذكر استبدال** `admin@stormycloud.org` بعنوان بريدك الإلكتروني الخاص.

الآن قم بتفعيل وبدء الخدمة:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
تحقق من أن الخدمة قيد التشغيل:

```bash
sudo systemctl status reseed
```
![التحقق من حالة خدمة إعادة البذر](/images/guides/reseed/reseed_04.png)

### الخطوة 3: إنشاء شهادة SSL

للحصول على الأداء الأمثل، قد ترغب في إعادة تشغيل خدمة الـ reseed بشكل دوري لتحديث معلومات الـ router:

```bash
sudo crontab -e
```
أضف هذا السطر لإعادة تشغيل الخدمة كل 3 ساعات:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

يعمل خادم reseed على localhost:8443 ويحتاج إلى reverse proxy للتعامل مع حركة HTTPS العامة. نوصي باستخدام Nginx Proxy Manager لسهولة استخدامه.

### الخطوة 4: احفظ نسخة احتياطية من مفاتيحك

نشر Nginx Proxy Manager باستخدام Docker:

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
هذا يكشف: - **المنفذ 80**: حركة مرور HTTP - **المنفذ 81**: واجهة الإدارة - **المنفذ 443**: حركة مرور HTTPS

### Configure Proxy Manager

1. قم بالوصول إلى واجهة الإدارة على `http://your-server-ip:81`

2. تسجيل الدخول باستخدام بيانات الاعتماد الافتراضية:
   - **البريد الإلكتروني**: admin@example.com
   - **كلمة المرور**: changeme

**مهم**: قم بتغيير بيانات الاعتماد هذه فوراً بعد تسجيل الدخول الأول!

![تسجيل الدخول إلى Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. انتقل إلى **Proxy Hosts** وانقر على **Add Proxy Host**

![إضافة مضيف بروكسي](/images/guides/reseed/reseed_06.png)

4. قم بتكوين مضيف الوكيل (proxy host):
   - **اسم النطاق**: نطاق إعادة البذر الخاص بك (مثال: `reseed.example.com`)
   - **البروتوكول**: `https`
   - **اسم المضيف / عنوان IP للتوجيه**: `127.0.0.1`
   - **منفذ التوجيه**: `8443`
   - فعّل **تخزين الأصول مؤقتاً (Cache Assets)**
   - فعّل **حظر الثغرات الشائعة (Block Common Exploits)**
   - فعّل **دعم Websockets**

![تكوين تفاصيل مضيف البروكسي](/images/guides/reseed/reseed_07.png)

5. في تبويب **SSL**:
   - اختر **Request a new SSL Certificate** (Let's Encrypt)
   - فعّل **Force SSL**
   - فعّل **HTTP/2 Support**
   - وافق على شروط خدمة Let's Encrypt

![إعدادات شهادة SSL](/images/guides/reseed/reseed_08.png)

6. انقر على **حفظ**

يجب أن يكون خادم إعادة التهيئة (reseed) الخاص بك متاحًا الآن على `https://reseed.example.com`

![تكوين ناجح لخادم reseed](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

بمجرد أن يصبح خادم إعادة البذر (reseed server) الخاص بك جاهزاً للعمل، اتصل بمطوري I2P لإضافته إلى قائمة خوادم إعادة البذر الرسمية.

### الخطوة 5: إنشاء خدمة Systemd

راسل **zzz** (المطور الرئيسي لـ I2P) عبر البريد الإلكتروني بالمعلومات التالية:

- **البريد الإلكتروني على I2P**: zzz@mail.i2p
- **البريد الإلكتروني على Clearnet**: zzz@i2pmail.org

### الخطوة 6: اختياري - تكوين عمليات إعادة التشغيل الدورية

قم بتضمين ما يلي في بريدك الإلكتروني:

1. **عنوان URL لخادم Reseed**: عنوان URL الكامل لبروتوكول HTTPS (مثال: `https://reseed.example.com`)
2. **شهادة reseed العامة**: موجودة في `/home/i2p/.reseed/` (أرفق ملف `.crt`)
3. **البريد الإلكتروني للتواصل**: طريقة الاتصال المفضلة لديك لتلقي إشعارات صيانة الخادم
4. **موقع الخادم**: اختياري لكنه مفيد (البلد/المنطقة)
5. **وقت التشغيل المتوقع**: التزامك بصيانة الخادم

### Verification

سيتحقق مطورو I2P من أن خادم إعادة البذر (reseed server) الخاص بك: - مُكوّن بشكل صحيح ويقدم معلومات الموجه (router) - يستخدم شهادات SSL صالحة - يوفر ملفات SU3 موقعة بشكل صحيح - متاح ويستجيب

بمجرد الموافقة، سيتم إضافة خادم إعادة التوزيع الخاص بك إلى القائمة الموزعة مع أجهزة توجيه I2P، مما يساعد المستخدمين الجدد على الانضمام إلى الشبكة!

## Monitoring and Maintenance

### تثبيت Nginx Proxy Manager

راقب خدمة إعادة البذر الخاصة بك:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### تكوين مدير البروكسي

راقب موارد النظام:

```bash
htop
df -h
```
### Update Reseed Tools

قم بتحديث reseed-tools بشكل دوري للحصول على أحدث التحسينات:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### معلومات الاتصال

إذا كنت تستخدم Let's Encrypt من خلال Nginx Proxy Manager، فإن الشهادات ستتجدد تلقائياً. تحقق من أن التجديد يعمل:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## تكوين الخدمة

### المعلومات المطلوبة

تحقق من السجلات بحثًا عن الأخطاء:

```bash
sudo journalctl -u reseed -n 50
```
المشاكل الشائعة: - router الخاص بـ I2P غير قيد التشغيل أو قاعدة بيانات الشبكة فارغة - المنفذ 8443 قيد الاستخدام بالفعل - مشاكل في الأذونات مع مجلد `/home/i2p/.reseed/`

### التحقق

تأكد من أن موجه I2P الخاص بك قيد التشغيل وقد ملأ قاعدة بيانات الشبكة الخاصة به:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
يجب أن ترى العديد من ملفات `.dat`. إذا كانت فارغة، انتظر حتى يكتشف router الخاص بك I2P نظراء الشبكة.

### SSL Certificate Errors

تحقق من صحة الشهادات الخاصة بك:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### فحص حالة الخدمة

تحقق من: - سجلات DNS تشير بشكل صحيح إلى الخادم الخاص بك - جدار الحماية يسمح بالمنافذ 80 و 443 - Nginx Proxy Manager يعمل: `docker ps`

## Security Considerations

- **حافظ على أمان مفاتيحك الخاصة**: لا تشارك أو تكشف محتويات `/home/i2p/.reseed/` أبدًا
- **التحديثات المنتظمة**: حافظ على تحديث حزم النظام وDocker وreseed-tools
- **راقب السجلات**: راقب أنماط الوصول المشبوهة
- **تحديد المعدل**: فكر في تطبيق تحديد المعدل لمنع إساءة الاستخدام
- **قواعد الجدار الناري**: اكشف فقط المنافذ الضرورية (80، 443، 81 لواجهة الإدارة)
- **واجهة الإدارة**: قيّد الوصول إلى واجهة إدارة Nginx Proxy Manager (المنفذ 81) على عناوين IP الموثوقة فقط

## Contributing to the Network

من خلال تشغيل خادم reseed، فإنك توفر بنية تحتية حيوية لشبكة I2P. شكراً لمساهمتك في إنترنت أكثر خصوصية ولامركزية!

للأسئلة أو المساعدة، تواصل مع مجتمع I2P: - **المنتدى**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p على شبكات مختلفة - **التطوير**: [i2pgit.org](https://i2pgit.org)

---

*الدليل تم إنشاؤه في الأصل بواسطة [Stormy Cloud](https://www.stormycloud.org)، معدل لتوثيق I2P.*
