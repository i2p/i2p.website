---
title: "مضيفو Reseed (إعادة البذر)"
description: "تشغيل خدمات reseed (إمداد بيانات التمهيد الأولي) وطرق bootstrap البديلة (التمهيد الأولي)"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## حول خوادم Reseed (التزويد الأولي بمعلومات الشبكة)

تحتاج routers الجديدة إلى عددٍ قليلٍ من النظراء للانضمام إلى شبكة I2P. يوفّر reseed hosts (خوادم التمهيد الأولي) مجموعة التمهيد الابتدائية عبر تنزيلات HTTPS مُشفَّرة. تُوقَّع كل حزمة reseed من قِبل المضيف، مما يمنع العبث بها من قِبل أطراف غير موثَّقة. قد تقوم routers المستقرة بإجراء reseed أحيانًا إذا أصبحت مجموعة نظرائها قديمة.

### عملية تمهيد الشبكة

عندما يبدأ I2P router للمرة الأولى أو يكون غير متصل لفترة طويلة، فإنه يحتاج إلى بيانات RouterInfo (معلومات الـ router) للاتصال بالشبكة. وبما أن الـ router لا يملك أقراناً موجودين مسبقاً، فلا يمكنه الحصول على هذه المعلومات من داخل شبكة I2P نفسها. تقوم آلية reseed (إعادة البذر) بحل مشكلة التمهيد هذه عبر توفير ملفات RouterInfo من خوادم HTTPS خارجية موثوقة.

توفّر عملية إعادة البذر 75-100 ملف RouterInfo (معلومات router) ضمن حزمة واحدة موقعة تشفيرياً. وهذا يضمن أن تتمكن routers الجديدة من إنشاء اتصالات بسرعة من دون تعريضها لهجمات الرجل في الوسط، التي قد تعزلها ضمن أقسام شبكية منفصلة وغير موثوقة.

### حالة الشبكة الحالية

اعتبارًا من أكتوبر 2025، تعمل شبكة I2P باستخدام إصدار router 2.10.0 (إصدار API 0.9.67). يظل reseed protocol (آلية لجلب الأقران الأوّليين للشبكة) الذي قُدِّم في الإصدار 0.9.14 مستقرًا ولم يطرأ عليه تغيير في وظيفته الأساسية. تحافظ الشبكة على عدة خوادم reseed مستقلة موزعة عالميًا لضمان التوافر ومقاومة الرقابة.

تراقب خدمة [checki2p](https://checki2p.com/reseed) جميع خوادم reseed (إعادة البذر) الخاصة بـ I2P كل 4 ساعات، وتوفر فحوصات حالة في الوقت الفعلي ومقاييس التوافر للبنية التحتية لـ reseed.

## مواصفة تنسيق ملف SU3

تنسيق ملف SU3 يمثّل الأساس لبروتوكول reseed (إعادة التزويد بعُقد البداية) الخاص بـ I2P، مما يوفّر تقديم محتوى مُوقّعًا تشفيريًا. يُعدّ فهم هذا التنسيق ضروريًا لتنفيذ خوادم وعملاء reseed.

### بنية الملفات

يتكوّن تنسيق SU3 من ثلاثة مكوّنات رئيسية: الرأس (40+ بايت)، المحتوى (بطول متغيّر)، والتوقيع (بطول محدَّد في الرأس).

#### تنسيق الترويسة (بايتات 0-39 كحد أدنى)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### معلمات SU3 الخاصة بـ Reseed (إعادة البذر)

بالنسبة لحزم إعادة البذر، يجب أن يتسم ملف SU3 بالخصائص التالية:

- **اسم الملف**: يجب أن يكون بالضبط `i2pseeds.su3`
- **نوع المحتوى** (البايت 27): 0x03 (RESEED)
- **نوع الملف** (البايت 25): 0x00 (ZIP)
- **نوع التوقيع** (البايتان 8-9): 0x0006 (RSA-4096-SHA512)
- **سلسلة الإصدار**: الطابع الزمني لـ Unix بصيغة ASCII (عدد الثواني منذ Epoch، date +%s format)
- **معرّف الموقّع**: معرّف بأسلوب البريد الإلكتروني يطابق CN (الاسم الشائع) في شهادة X.509

#### معلمة استعلام معرّف الشبكة

بدءًا من الإصدار 0.9.42، تقوم routers بإلحاق `?netid=2` بطلبات reseed (جلب بيانات التمهيد للشبكة). هذا يمنع الاتصالات عبر الشبكات، نظرًا لأن شبكات الاختبار تستخدم معرّفات شبكة مختلفة. تستخدم الشبكة الإنتاجية الحالية لـ I2P معرّف الشبكة 2.

مثال على الطلب: `https://reseed.example.com/i2pseeds.su3?netid=2`

### بنية محتوى ZIP

يحتوي قسم المحتوى (بعد الترويسة، قبل التوقيع) على أرشيف ZIP قياسي يستوفي المتطلبات التالية:

- **الضغط**: ضغط ZIP القياسي (DEFLATE، خوارزمية ضغط)
- **عدد الملفات**: عادةً 75-100 ملفات RouterInfo (بيانات Router في I2P)
- **بنية الدليل**: يجب أن تكون جميع الملفات في المستوى الأعلى (دون أدلة فرعية)
- **تسمية الملفات**: `routerInfo-{44-character-base64-hash}.dat`
- **أبجدية base64 (ترميز بقاعدة 64)**: يجب استخدام أبجدية base64 المعدّلة الخاصة بـ I2P

تختلف أبجدية base64 الخاصة بـ I2P عن base64 القياسي باستخدام `-` و`~` بدلاً من `+` و`/` لضمان التوافق مع أنظمة الملفات وعناوين URL.

### التوقيع التشفيري

يغطي التوقيع الملف بأكمله ابتداءً من البايت 0 وحتى نهاية قسم المحتوى. يُلحَق التوقيع نفسه بعد المحتوى.

#### خوارزمية التوقيع (RSA-4096-SHA512)

1. احسب قيمة التجزئة SHA-512 للبايتات من 0 حتى نهاية المحتوى
2. وقّع قيمة التجزئة باستخدام "raw" RSA (NONEwithRSA بمصطلحات Java)
3. عبّئ التوقيع بأصفار بادئة عند الحاجة للوصول إلى 512 بايت
4. ألحِق توقيعًا بطول 512 بايت بالملف

#### عملية التحقق من صحة التوقيع

يجب على العملاء:

1. اقرأ البايتات 0-11 لتحديد نوع التوقيع وطوله
2. اقرأ كامل الترويسة لتحديد حدود المحتوى
3. قم ببث المحتوى أثناء حساب تجزئة SHA-512
4. استخرج التوقيع من نهاية الملف
5. تحقق من التوقيع باستخدام المفتاح العام RSA-4096 الخاص بالموقّع
6. ارفض الملف إذا فشل التحقق من التوقيع

### نموذج الثقة للشهادات

تُوزَّع مفاتيح توقيع إعادة البذر على شكل شهادات X.509 موقَّعة ذاتيًا بمفاتيح RSA-4096. تُدرَج هذه الشهادات ضمن حزم I2P router في الدليل `certificates/reseed/`.

تنسيق الشهادة: - **نوع المفتاح**: RSA-4096 - **التوقيع**: موقعة ذاتيًا - **CN الخاص بالموضوع**: يجب أن يتطابق مع معرّف الموقّع في ترويسة SU3 - **تواريخ الصلاحية**: يجب على العملاء تطبيق فترات صلاحية الشهادة

## تشغيل مضيف Reseed (إعادة البذر)

يتطلب تشغيل خدمة reseed (آلية التزويد الأولي بمعلومات الشبكة للانضمام) اهتمامًا دقيقًا بمتطلبات الأمان والموثوقية وتنوع الشبكة. إن زيادة عدد مضيفي reseed المستقلين تعزز القدرة على الصمود وتُصعّب على المهاجمين أو الرقباء منع routers الجديدة من الانضمام.

### المتطلبات التقنية

#### مواصفات الخادم

- **نظام التشغيل**: Unix/Linux (تم اختبار Ubuntu وDebian وFreeBSD والتوصية بها)
- **الاتصال**: يتطلب عنوان IPv4 ثابتًا، وIPv6 مُوصى به لكنه اختياري
- **المعالج**: نواتان على الأقل
- **الذاكرة (RAM)**: 2 غيغابايت كحد أدنى
- **عرض النطاق الترددي**: حوالي 15 غيغابايت شهريًا
- **مدة التشغيل**: التشغيل على مدار الساعة طوال أيام الأسبوع مطلوب
- **I2P Router**: I2P router متكامل جيدًا ويعمل باستمرار

#### متطلبات البرمجيات

- **Java**: JDK 8 أو أحدث (سيكون Java 17+ مطلوباً اعتباراً من I2P 2.11.0)
- **خادم ويب**: nginx أو Apache مع دعم الوكيل العكسي (Lighttpd لم يعد مدعوماً بسبب قيود ترويسة X-Forwarded-For)
- **TLS/SSL**: شهادة TLS صالحة (Let's Encrypt، موقعة ذاتياً، أو سلطة شهادات تجارية (CA))
- **حماية DDoS**: fail2ban أو ما يعادله (إلزامي، ليس اختيارياً)
- **أدوات إعادة البذر**: reseed-tools الرسمية من https://i2pgit.org/idk/reseed-tools

### متطلبات الأمان

#### تهيئة HTTPS/TLS

- **البروتوكول**: HTTPS فقط، بدون HTTP كبديل احتياطي
- **إصدار TLS**: الحد الأدنى هو TLS 1.2
- **مجموعات التشفير**: يجب أن تدعم خوارزميات قوية متوافقة مع Java 8+
- **CN/SAN الخاصة بالشهادة**: (الاسم الشائع/اسم بديل للموضوع) يجب أن تتطابق مع اسم المضيف لعنوان URL المُقدَّم
- **نوع الشهادة**: قد تكون موقّعة ذاتيًا إذا تم التنسيق مع فريق التطوير، أو صادرة عن CA معترف بها (جهة إصدار الشهادات)

#### إدارة الشهادات

شهادات توقيع SU3 وشهادات TLS تخدم أغراضًا مختلفة:

- **شهادة TLS** (`certificates/ssl/`): تؤمّن نقل HTTPS
- **شهادة توقيع SU3** (`certificates/reseed/`): توقّع حزم reseed (إعادة البذر)

يجب تقديم الشهادتين إلى منسق reseed (التهيئة الأولية للشبكة) (zzz@mail.i2p) لإدراجهما ضمن حزم router.

#### حماية من هجمات حجب الخدمة الموزعة (DDoS) والكشط

تتعرض Reseed servers (خوادم إعادة البذر) لهجمات دورية من تنفيذات معيبة، وشبكات بوتنت، وجهات خبيثة تحاول كشط قاعدة بيانات الشبكة. تشمل إجراءات الحماية ما يلي:

- **fail2ban**: مطلوب لتقييد المعدّل وتخفيف الهجمات
- **تنوع الحزم**: تسليم مجموعات مختلفة من RouterInfo (المعلومات التعريفية الخاصة بـ Router) إلى جهات طالبة مختلفة
- **اتساق الحزمة**: تسليم الحزمة نفسها للطلبات المتكررة من نفس عنوان IP ضمن نافذة زمنية قابلة للتهيئة
- **قيود تسجيل IP**: عدم نشر السجلات أو عناوين IP (متطلب لسياسة الخصوصية)

### أساليب التنفيذ

#### الطريقة 1: reseed-tools الرسمية (موصى بها)

التنفيذ المرجعي الذي يُصانه مشروع I2P. المستودع: https://i2pgit.org/idk/reseed-tools

**التثبيت**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
عند التشغيل لأول مرة، ستقوم الأداة بإنشاء:
- `your-email@mail.i2p.crt` (شهادة توقيع SU3)
- `your-email@mail.i2p.pem` (المفتاح الخاص لتوقيع SU3)
- `your-email@mail.i2p.crl` (قائمة إبطال الشهادات)
- ملفات شهادة ومفتاح TLS

**الميزات**: - توليد حزمة SU3 تلقائيًا (350 متغيرًا، 77 RouterInfos لكل منها) - خادم HTTPS مدمج - إعادة بناء ذاكرة التخزين المؤقت كل 9 ساعات عبر cron - دعم ترويسة X-Forwarded-For مع الخيار `--trustProxy` - متوافق مع تكوينات الوكيل العكسي

**النشر في بيئة الإنتاج**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### الطريقة الثانية: تنفيذ بلغة بايثون (pyseeder)

تنفيذ بديل من مشروع PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### الطريقة الثالثة: نشر Docker

بالنسبة إلى البيئات المعتمدة على الحاويات، توجد عدة تنفيذات جاهزة لـ Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: يضيف خدمة أونيون الخاصة بـ Tor ودعم IPFS (نظام الملفات بين الكواكب)

### تهيئة الوكيل العكسي

#### تهيئة nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### تهيئة Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### التسجيل والتنسيق

لإدراج reseed server (خادم التمهيد للشبكة) الخاص بك في الحزمة الرسمية لـ I2P:

1. أكمل الإعداد والاختبار
2. أرسل الشهادتين (توقيع SU3 وTLS) إلى منسق reseed (آلية تزويد بيانات الشبكة للمستخدمين الجدد)
3. للتواصل: zzz@mail.i2p أو zzz@i2pmail.org
4. انضم إلى #i2p-dev على IRC2P للتنسيق مع مشغّلين آخرين

### أفضل الممارسات التشغيلية

#### المراقبة والتسجيل

- تمكين combined log format (تنسيق سجل موحّد) في Apache/nginx لأغراض الإحصاءات
- تنفيذ تدوير السجلات (تنمو السجلات بسرعة)
- مراقبة نجاح إنشاء الحزمة وأزمنة إعادة البناء
- تتبّع استخدام عرض النطاق وأنماط الطلبات
- عدم نشر عناوين IP أو سجلات الوصول التفصيلية مطلقًا

#### جدول الصيانة

- **كل 9 ساعات**: إعادة بناء ذاكرة التخزين المؤقت لحزمة SU3 (مؤتمت عبر cron، مُجدول المهام في أنظمة Unix)
- **أسبوعيًا**: مراجعة السجلات لرصد أنماط الهجمات
- **شهريًا**: تحديث I2P router و reseed-tools
- **حسب الحاجة**: تجديد شهادات TLS (أتمتة باستخدام Let's Encrypt)

#### اختيار المنفذ

- الافتراضي: 8443 (مُوصى به)
- بديل: أي منفذ بين 1024-49151
- المنفذ 443: يتطلب صلاحيات الجذر أو إعادة توجيه المنفذ (يوصى باستخدام iptables redirect)

مثال على إعادة توجيه المنافذ:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## أساليب Reseed البديلة (التمهيد الأولي للشبكة بجلب عناوين النظراء)

تساعد خيارات التمهيد الأخرى المستخدمين الموجودين خلف شبكات مقيِّدة:

### Reseed (التمهيد الأوّلي للشبكة) القائم على الملفات

قُدِّمت في الإصدار 0.9.16، تتيح عملية reseeding القائمة على الملفات (إعادة تمهيد الاتصال بالشبكة) للمستخدمين تحميل حِزَم RouterInfo يدويًا. هذه الطريقة مفيدة بشكل خاص للمستخدمين في المناطق الخاضعة للرقابة حيث تكون خوادم reseed عبر HTTPS محجوبة.

**العملية**: 1. تُنشئ جهة اتصال موثوقة حزمة SU3 باستخدام الـ router الخاص بهم 2. تُنقَل الحزمة عبر البريد الإلكتروني، أو محرك USB، أو قناة أخرى out-of-band (قناة منفصلة عن القناة الاعتيادية) 3. يضع المستخدم `i2pseeds.su3` في دليل إعدادات I2P 4. يقوم الـ Router تلقائياً باكتشاف الحزمة ومعالجتها عند إعادة التشغيل

**التوثيق**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**حالات الاستخدام**: - مستخدمون خلف جدران نارية وطنية تحجب خوادم reseed (خوادم تزويد نقاط الاتصال الأولية) - شبكات معزولة تتطلب تمهيداً يدوياً (bootstrap) - بيئات الاختبار والتطوير

### إعادة البذر عبر وكيل Cloudflare

يوفّر توجيه حركة مرور إعادة البذر عبر شبكة توصيل المحتوى (CDN) الخاصة بـ Cloudflare عدة مزايا للمشغلين في المناطق ذات الرقابة المشددة.

**المزايا**: - إخفاء عنوان IP للخادم الأصلي عن العملاء - حماية من هجمات حجب الخدمة الموزعة (DDoS) عبر البنية التحتية لـ Cloudflare - توزيع الحمل جغرافيًا عبر التخزين المؤقت على الحافة - أداء أفضل للعملاء حول العالم

**متطلبات التنفيذ**: - تم تمكين الخيار `--trustProxy` في reseed-tools (مجموعة أدوات إعادة البذر) - تم تمكين وكيل Cloudflare لسجل DNS - معالجة ترويسة X-Forwarded-For بشكل صحيح

**اعتبارات مهمة**: - تنطبق قيود منافذ Cloudflare (يجب استخدام المنافذ المدعومة) - يتطلب اتساق حزمة العميل نفسه دعم X-Forwarded-For - تتم إدارة تهيئة SSL/TLS بواسطة Cloudflare

**التوثيق**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### استراتيجيات مقاومة للرقابة

يُحدِّد بحثٌ أعدّه Nguyen Phong Hoang (USENIX FOCI 2019) أساليب تمهيد إضافية للشبكات الخاضعة للرقابة:

#### مزودو التخزين السحابي

- **Box, Dropbox, Google Drive, OneDrive**: استضافة ملفات SU3 عبر روابط عامة
- **الميزة**: يصعب حظرها دون تعطيل الخدمات المشروعة
- **العيب**: يتطلب توزيع عناوين URL يدويًا إلى المستخدمين

#### التوزيع عبر IPFS (نظام الملفات بين الكواكب)

- استضافة حزم إعادة البذر على InterPlanetary File System (نظام الملفات بين الكواكب)
- التخزين المعنون بالمحتوى يمنع التلاعب
- مقاوم لمحاولات الإزالة

#### خدمات أونيون الخاصة بتور

- خوادم reseed (خوادم التهيئة الأولية للشبكة) متاحة عبر عناوين .onion
- مقاومة للحجب المعتمد على عناوين IP
- يتطلب وجود عميل Tor على نظام المستخدم

**وثائق البحث**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### الدول المعروفة بحجب I2P

اعتبارًا من عام 2025، تم التأكيد أن الدول التالية تحجب خوادم إعادة البذر لـ I2P: - الصين - إيران - عُمان - قطر - الكويت

ينبغي على المستخدمين في هذه المناطق استخدام أساليب تمهيد بديلة أو استراتيجيات إعادة بذر مقاومة للرقابة.

## تفاصيل البروتوكول للمنفذين

### مواصفة طلب Reseed (التمهيد الأولي للشبكة)

#### سلوك العميل

1. **اختيار الخادم**: Router يحافظ على قائمة ثابتة مُضمَّنة في الشيفرة لروابط reseed (إعادة البذر)
2. **الاختيار العشوائي**: يختار العميل خادماً عشوائياً من القائمة المتاحة
3. **تنسيق الطلب**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: يجب أن يحاكي المتصفحات الشائعة (مثلاً، "Wget/1.11.4")
5. **منطق إعادة المحاولة**: إذا فشل طلب SU3، فارجع إلى تحليل صفحة الفهرس
6. **التحقق من الشهادة**: تحقق من شهادة TLS بمقارنتها مع مخزن الثقة للنظام
7. **التحقق من توقيع SU3**: تحقق من التوقيع بمقارنته مع شهادات reseed المعروفة

#### سلوك الخادم

1. **اختيار الحزمة**: اختيار مجموعة فرعية شبه عشوائية من RouterInfos (سجلات معلومات الـ router) من netDb
2. **تتبّع العملاء**: تحديد الطلبات حسب عنوان IP المصدر (مع مراعاة X-Forwarded-For)
3. **اتساق الحزمة**: إرجاع نفس الحزمة للطلبات المتكررة ضمن نافذة زمنية (عادةً 8-12 ساعة)
4. **تنوع الحزم**: إرجاع حزم مختلفة لعملاء مختلفين لتحقيق تنوّع الشبكة
5. **نوع المحتوى**: `application/octet-stream` أو `application/x-i2p-reseed`

### تنسيق ملف RouterInfo

كل ملف `.dat` في حزمة reseed (إعادة البذر) يحتوي على بنية RouterInfo (معلومات Router):

**تسمية الملفات**: `routerInfo-{base64-hash}.dat` - تتألف التجزئة من 44 حرفًا باستخدام أبجدية base64 الخاصة بـ I2P - مثال: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**محتويات الملف**: - RouterIdentity (router hash، مفتاح التشفير، مفتاح التوقيع) - الطابع الزمني للنشر - عناوين الـrouter (IP، المنفذ، نوع النقل) - قدرات الـrouter وخياراته - توقيع يغطي جميع البيانات أعلاه

### متطلبات تنوع الشبكة

لمنع مركزة الشبكة وتمكين الكشف عن هجوم Sybil (هجوم يعتمد على إنشاء هويات مزيفة متعددة):

- **لا تفريغات NetDb كاملة**: لا تُقدِّم جميع RouterInfos (معلومات Router) إلى عميل واحد
- **أخذ عينات عشوائية**: تحتوي كل حزمة على مجموعة فرعية مختلفة من الأقران المتاحين
- **الحد الأدنى لحجم الحزمة**: 75 RouterInfos (تمت زيادته من 50 في الأصل)
- **الحد الأقصى لحجم الحزمة**: 100 RouterInfos
- **الحداثة**: ينبغي أن تكون RouterInfos حديثة (خلال 24 ساعة من إنشائها)

### اعتبارات IPv6

**الحالة الحالية** (2025): - عدة خوادم reseed (خوادم التمهيد الأوّلي للشبكة) تُظهر عدم استجابة عبر IPv6 - ينبغي للعملاء تفضيل IPv4 أو فرضه من أجل الموثوقية - يُوصى بدعم IPv6 في عمليات النشر الجديدة، لكنه ليس أمراً حرجاً

**ملاحظة تنفيذية**: عند إعداد الخوادم ثنائية المكدس (dual-stack)، تأكد من أن عناوين الاستماع لكلٍّ من IPv4 وIPv6 تعمل بشكل صحيح، أو عطّل IPv6 إذا تعذّر دعمه بشكل صحيح.

## اعتبارات أمنية

### نموذج التهديد

يحمي بروتوكول إعادة البذر من:

1. **هجمات الرجل في الوسط**: تواقيع RSA-4096 تمنع العبث بالحزمة
2. **تقسيم الشبكة**: تعدد خوادم إعادة البذر المستقلة يمنع وجود نقطة تحكم واحدة
3. **هجمات سيبيل**: تنوع الحزم يحد من قدرة المهاجم على عزل المستخدمين
4. **الرقابة**: تعدد الخوادم والطرق البديلة يوفر التكرار

لا يحمي بروتوكول reseed (آلية الحصول على نقاط الاتصال الأولية) من:

1. **خوادم reseed (عملية التمهيد الأولية لاكتشاف نظراء شبكة I2P) المخترقة**: إذا كان المهاجم يتحكم في المفاتيح الخاصة لشهادات reseed
2. **الحجب الكامل للشبكة**: إذا تم حجب جميع طرق reseed في منطقة ما
3. **المراقبة طويلة الأمد**: طلبات reseed تكشف عنوان IP الذي يحاول الانضمام إلى I2P

### إدارة الشهادات

**أمان المفتاح الخاص**: - احتفظ بمفاتيح توقيع SU3 دون اتصال بالإنترنت عند عدم استخدامها - استخدم كلمات مرور قوية لتشفير المفاتيح - حافظ على نُسخ احتياطية آمنة للمفاتيح والشهادات - ضع في الاعتبار hardware security modules (HSMs) (وحدات أمن الأجهزة) لعمليات النشر عالية القيمة

**إلغاء الشهادات**: - توزيع قوائم إلغاء الشهادات (CRLs) عبر موجز الأخبار - يمكن للمنسّق إلغاء الشهادات المخترَقة - Routers تحدّث CRLs تلقائيًا مع تحديثات البرمجيات

### التخفيف من الهجمات

**الحماية من هجمات الحرمان من الخدمة الموزعة (DDoS)**: - قواعد fail2ban للطلبات المفرطة - تحديد معدل الطلبات على مستوى خادم الويب - تحديد عدد الاتصالات لكل عنوان IP - Cloudflare أو شبكة توصيل المحتوى (CDN) مماثلة كطبقة إضافية

**منع الكشط**: - حزم مختلفة لكل عنوان IP مُطلِب - تخزين مؤقت للحزم قائم على الوقت لكل عنوان IP - تسجيل أنماط تشير إلى محاولات الكشط - التنسيق مع المشغّلين الآخرين بشأن الهجمات المُكتشَفة

## الاختبار والتحقق من الصحة

### اختبار خادم إعادة البذر الخاص بك

#### الطريقة 1: تثبيت Router جديد

1. ثبّت I2P على نظام نظيف
2. أضف رابط reseed (إعادة البذر: تمهيد الاتصال الأولي بالشبكة) إلى الإعدادات
3. أزِل أو عطّل روابط reseed الأخرى
4. شغّل الـ router وراقب السجلات للتأكد من نجاح reseed
5. تحقّق من الاتصال بالشبكة خلال 5–10 دقائق

مخرجات السجل المتوقعة:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### الطريقة 2: التحقق اليدوي من SU3

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### الطريقة 3: مراقبة checki2p

تقوم الخدمة على https://checki2p.com/reseed بإجراء فحوصات آلية كل 4 ساعات على جميع خوادم reseed الخاصة بـ I2P (خوادم التمهيد الأولي) المسجّلة. يوفّر ذلك:

- مراقبة التوفر
- مقاييس زمن الاستجابة
- التحقق من صحة شهادة TLS
- التحقق من صحة توقيع SU3
- بيانات مدة التشغيل التاريخية

بمجرد تسجيل reseed (خادم التمهيد الأولي لشبكة I2P) الخاص بك لدى مشروع I2P، سيظهر تلقائيًا على checki2p خلال 24 ساعة.

### استكشاف المشكلات الشائعة وإصلاحها

**المشكلة**: "Unable to read signing key" عند التشغيل لأول مرة - **الحل**: هذا متوقع. أجب بـ 'y' لإنشاء مفاتيح جديدة.

**المشكلة**: Router يفشل في التحقق من التوقيع - **السبب**: الشهادة غير موجودة في مخزن الثقة الخاص بالـ router - **الحل**: ضع الشهادة في الدليل `~/.i2p/certificates/reseed/`

**المشكلة**: تسليم نفس الحزمة لعملاء مختلفين - **السبب**: ترويسة X-Forwarded-For لا تُمرَّر بالشكل الصحيح - **الحل**: فعّل `--trustProxy` وقم بتهيئة ترويسات الوكيل العكسي

**المشكلة**: "تم رفض الاتصال" - **السبب**: المنفذ غير قابل للوصول من الإنترنت - **الحل**: تحقق من قواعد جدار الحماية، وتأكد من إعدادات إعادة توجيه المنفذ

**Issue**: استهلاك مرتفع لوحدة المعالجة المركزية أثناء إعادة بناء الحزمة - **Cause**: سلوك طبيعي عند توليد 350+ تنويعات SU3 (تنسيق ملف التحديث في I2P) - **Solution**: احرص على توفر موارد كافية لوحدة المعالجة المركزية، وفكّر في تقليل وتيرة إعادة البناء

## معلومات مرجعية

### التوثيق الرسمي

- **دليل المساهمين في Reseed (خدمة تمهيد الشبكة)**: /guides/creating-and-running-an-i2p-reseed-server/
- **متطلبات سياسة Reseed**: /guides/reseed-policy/
- **مواصفة SU3**: /docs/specs/updates/
- **مستودع أدوات Reseed**: https://i2pgit.org/idk/reseed-tools
- **وثائق أدوات Reseed**: https://eyedeekay.github.io/reseed-tools/

### تنفيذات بديلة

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder (خادم لإعادة البذر)**: https://github.com/torbjo/i2p-reseeder

### موارد المجتمع

- **منتدى I2P**: https://i2pforum.net/
- **مستودع Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev على IRC2P
- **مراقبة الحالة**: https://checki2p.com/reseed

### سجل الإصدارات

- **0.9.14** (2014): تم تقديم تنسيق SU3 لعملية reseed (جلب بيانات التمهيد للشبكة)
- **0.9.16** (2014): إضافة reseeding القائم على الملفات
- **0.9.42** (2019): اشتراط معلمة الاستعلام Network ID
- **2.0.0** (2022): تم تقديم بروتوكول النقل SSU2
- **2.4.0** (2024): عزل NetDB وتحسينات أمنية
- **2.6.0** (2024): حظر اتصالات I2P-over-Tor
- **2.10.0** (2025): الإصدار المستقر الحالي (اعتبارًا من سبتمبر 2025)

### مرجع نوع التوقيع

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**معيار reseed (عملية التهيئة الأولية للشبكة)**: النوع 6 (RSA-SHA512-4096) مطلوب لحزم reseed.

## التقدير

شكرًا لكل مشغّل reseed (خدمة التمهيد الأوّلي لشبكة I2P) على إبقاء الشبكة متاحة وقادرة على الصمود. تقدير خاص للمساهمين والمشاريع التالية:

- **zzz**: مطوّر مخضرم في I2P ومنسّق reseed (التمهيد الأوّلي للشبكة)
- **idk**: المشرف الحالي على reseed-tools ومدير الإصدارات
- **Nguyen Phong Hoang**: أبحاث حول استراتيجيات reseeding المقاومة للرقابة
- **PurpleI2P Team**: تنفيذات بديلة لـ I2P وأدوات
- **checki2p**: خدمة مراقبة آلية للبنية التحتية الخاصة بـ reseed

تمثل البنية التحتية اللامركزية لإعادة البذر (reseed) لشبكة I2P جهداً تعاونياً يبذله عشرات المشغلين حول العالم، مما يضمن أن يتمكن المستخدمون الجدد دائماً من العثور على مسار للانضمام إلى الشبكة بغض النظر عن الرقابة المحلية أو العوائق التقنية.
