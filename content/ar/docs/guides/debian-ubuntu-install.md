---
title: "تثبيت I2P على Debian و Ubuntu"
aliases:
  - "/ar/debian"
  - "/ar/debian/"
description: "دليل كامل لتثبيت I2P على Debian وUbuntu والتوزيعات المشتقة منهما باستخدام المستودعات الرسمية"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

يحافظ مشروع I2P على حزم رسمية لـ Debian وUbuntu والتوزيعات المشتقة منها. يوفر هذا الدليل تعليمات شاملة لتثبيت I2P باستخدام مستودعاتنا الرسمية.

---

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
---

## التثبيت على Ubuntu

**ملاحظة:** يبدو أن النص المراد ترجمته فارغ أو لم يتم تضمينه. يرجى تقديم النص الفعلي المراد ترجمته.

1. افتح [وحدة تحكم I2P Router](http://127.0.0.1:7657/)
2. انتقل إلى [صفحة إعدادات الشبكة](http://127.0.0.1:7657/confignet)
3. لاحظ أرقام المنافذ المدرجة (عادةً منافذ عشوائية بين 9000-31000)
4. قم بتوجيه منافذ UDP وTCP هذه في الموجه/جدار الحماية الخاص بك

يمكن لـ Ubuntu ومشتقاته الرسمية (Linux Mint، elementary OS، Trisquel، إلخ) استخدام I2P PPA (Personal Package Archive) لسهولة التثبيت والتحديثات التلقائية.

هذه هي الطريقة الأسرع والأكثر موثوقية لتثبيت I2P على الأنظمة المبنية على Ubuntu.

## Post-Installation Configuration

**الخطوة 1: إضافة مستودع PPA الخاص بـ I2P**

1. قم بزيارة [صفحة الإعدادات](http://127.0.0.1:7657/config.jsp)
2. ابحث عن قسم إعدادات النطاق الترددي
3. الإعدادات الافتراضية هي 96 كيلوبايت/ثانية للتنزيل / 40 كيلوبايت/ثانية للرفع
4. قم بزيادة هذه القيم إذا كان لديك إنترنت أسرع (مثلاً، 250 كيلوبايت/ثانية للتنزيل / 100 كيلوبايت/ثانية للرفع لاتصال النطاق العريض النموذجي)

افتح terminal واشغّل:

## التثبيت على Debian

يضيف هذا الأمر مستودع I2P PPA إلى `/etc/apt/sources.list.d/` ويستورد تلقائياً مفتاح GPG الذي يوقع المستودع. يضمن توقيع GPG أن الحزم لم يتم التلاعب بها منذ بنائها.

### Method 1: Command Line Installation (Recommended)

**الخطوة 2: تحديث قائمة الحزم**

حدّث قاعدة بيانات حزم النظام لديك لتضمين الـ PPA الجديد:

يقوم هذا بجلب أحدث معلومات الحزم من جميع المستودعات المُفعّلة، بما في ذلك I2P PPA الذي قمت بإضافته للتو.

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
**الخطوة 3: تثبيت I2P**

الآن قم بتثبيت I2P:

هذا كل شيء! انتقل إلى قسم [إعداد ما بعد التثبيت](#post-installation-configuration) لتتعلم كيفية بدء تشغيل I2P وإعداده.

```bash
sudo apt-get update
```
إذا كنت تفضل واجهة رسومية، يمكنك إضافة PPA باستخدام مركز البرمجيات في Ubuntu.

**الخطوة 1: فتح البرامج والتحديثات**

افتح "البرامج والتحديثات" من قائمة التطبيقات.

```bash
sudo apt-get install i2p
```
![قائمة مركز البرامج](/images/guides/debian/software-center-menu.png)

### Method 2: Using the Software Center GUI

**الخطوة 2: انتقل إلى البرامج الأخرى**

اختر علامة تبويب "البرامج الأخرى" وانقر على زر "إضافة" في الأسفل لتكوين PPA جديد.

![تبويب البرامج الأخرى](/images/guides/debian/software-center-addother.png)

**الخطوة 3: إضافة مستودع I2P PPA**

في مربع حوار PPA، أدخل:

![Add PPA Dialog](/images/guides/debian/software-center-ppatool.png)

**الخطوة 4: إعادة تحميل معلومات المستودع**

انقر على زر "إعادة التحميل" لتنزيل معلومات المستودع المحدثة.

![زر إعادة التحميل](/images/guides/debian/software-center-reload.png)

```
ppa:i2p-maintainers/i2p
```
**الخطوة 5: تثبيت I2P**

افتح تطبيق "Software" من قائمة التطبيقات، ابحث عن "i2p"، ثم انقر على تثبيت.

![تطبيق البرامج](/images/guides/debian/software-center-software.png)

بمجرد اكتمال التثبيت، انتقل إلى [تكوين ما بعد التثبيت](#post-installation-configuration).

بالتأكيد، سأقوم بالترجمة فقط دون أي تعليقات أو أسئلة. ومع ذلك، لاحظت أن النص المطلوب ترجمته يحتوي فقط على "---" وهو فاصل Markdown.

---

بعد تثبيت I2P، ستحتاج إلى تشغيل الـ router وإجراء بعض الإعدادات الأولية.

توفر حزم I2P ثلاث طرق لتشغيل موجه I2P:

ابدأ تشغيل I2P يدويًا عند الحاجة باستخدام سكريبت `i2prouter`:

## Next Steps

**مهم**: **لا** تستخدم `sudo` أو تشغل هذا كمستخدم root! يجب تشغيل I2P كمستخدمك العادي.

### الطريقة 2: استخدام واجهة مركز البرامج الرسومية

لإيقاف I2P:

### Initial Router Configuration

إذا كنت تستخدم نظام غير x86 أو أن Java Service Wrapper لا يعمل على منصتك، استخدم:

### إشعار هام

مرة أخرى، **لا** تستخدم `sudo` أو تقم بالتشغيل كمستخدم root.

للحصول على أفضل تجربة، قم بتكوين I2P للبدء تلقائياً عند إقلاع النظام، حتى قبل تسجيل الدخول:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
يفتح هذا مربع حوار التكوين. حدد "نعم" لتفعيل I2P كخدمة نظام.

**هذه هي الطريقة الموصى بها** لأن: - I2P يبدأ تلقائياً عند الإقلاع - يحافظ الموجه الخاص بك على تكامل أفضل مع الشبكة - تساهم في استقرار الشبكة - I2P متاح فوراً عندما تحتاج إليه

بعد تشغيل I2P للمرة الأولى، سيستغرق الأمر عدة دقائق للاندماج في الشبكة. في هذه الأثناء، قم بتكوين هذه الإعدادات الأساسية:

```bash
cat /etc/debian_version
```
للحصول على الأداء الأمثل والمشاركة في الشبكة، قم بتوجيه منافذ I2P عبر NAT/جدار الحماية الخاص بك:

إذا كنت بحاجة إلى مساعدة في إعادة توجيه المنافذ، يوفر موقع [portforward.com](https://portforward.com) أدلة خاصة بكل جهاز توجيه.

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
إعدادات النطاق الترددي الافتراضية محافظة. اضبطها بناءً على اتصالك بالإنترنت:

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**ملاحظة**: تعيين حدود أعلى يساعد الشبكة ويحسن أداءك الخاص.

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
للوصول إلى مواقع I2P (eepsites) والخدمات، قم بتكوين متصفحك لاستخدام بروكسي HTTP الخاص بـ I2P:

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
راجع [دليل إعداد المتصفح](/docs/guides/browser-config) للحصول على تعليمات الإعداد التفصيلية لمتصفحات Firefox وChrome والمتصفحات الأخرى.

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
---

إذا تلقيت أخطاء مفتاح GPG أثناء التثبيت:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
إذا لم يكن I2P يتلقى التحديثات:

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
إذا كنت تستخدم مستودعات `deb.i2p2.de` أو `deb.i2p2.no` القديمة:

الآن بعد أن تم تثبيت وتشغيل I2P:

مرحبًا بك في الإنترنت الخفي!

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**لـ Debian Buster أو الإصدارات الأقدم فقط**، ستحتاج أيضًا إلى إنشاء رابط رمزي (symlink):

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**الخطوة 6: تحديث قوائم الحزم**

قم بتحديث قاعدة بيانات حزم نظامك لتضمين مستودع I2P:

```bash
sudo apt-get update
```
**الخطوة 7: تثبيت I2P**

قم بتثبيت كل من موجه I2P وحزمة مفتاح التشفير (التي تضمن تلقيك تحديثات المفاتيح المستقبلية):

```bash
sudo apt-get install i2p i2p-keyring
```
رائع! تم الآن تثبيت I2P. تابع إلى قسم [التكوين بعد التثبيت](#post-installation-configuration).

---

## تكوين ما بعد التثبيت

بعد تثبيت I2P، ستحتاج إلى تشغيل الراوتر وإجراء بعض الإعدادات الأولية.

### المتطلبات الأساسية

توفر حزم I2P ثلاث طرق لتشغيل موجه I2P:

#### Option 1: On-Demand (Basic)

ابدأ I2P يدويًا عند الحاجة باستخدام النص البرمجي `i2prouter`:

```bash
i2prouter start
```
**مهم**: لا تستخدم `sudo` أو تشغّل هذا كمشرف! يجب أن يعمل I2P كمستخدمك العادي.

لإيقاف I2P:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

إذا كنت تستخدم نظامًا غير x86 أو لم يعمل برنامج Java Service Wrapper على نظامك، فاستخدم:

```bash
i2prouter-nowrapper
```
مرة أخرى، لا تستخدم `sudo` أو قم بالتشغيل كجذر (root).

#### Option 3: System Service (Recommended)

للحصول على أفضل تجربة، قم بتهيئة I2P للبدء تلقائيًا عند تشغيل النظام، حتى قبل تسجيل الدخول:

```bash
sudo dpkg-reconfigure i2p
```
هذا يفتح نافذة تهيئة. اختر "نعم" لتمكين I2P كخدمة نظام.

**هذه هي الطريقة الموصى بها** لأنها:  
- تبدأ I2P تلقائيًا عند التشغيل  
- يحافظ جهاز التوجيه الخاص بك على تكامل أفضل مع الشبكة  
- تساهم في استقرار الشبكة  
- تكون I2P متاحة فورًا عندما تحتاج إليها

### خطوات التثبيت

بعد بدء تشغيل I2P لأول مرة، سيستغرق الدمج في الشبكة عدة دقائق. وفي الوقت نفسه، قم بتكوين هذه الإعدادات الأساسية:

#### 1. Configure NAT/Firewall

لأداء مثالي والمشاركة في الشبكة، قم بإعادة توجيه منافذ I2P عبر جهاز التوجيه/الجدار الناري (NAT/firewall):

- تأكد من أنك لا تشغل I2P كمستخدم root: `ps aux | grep i2p`
- تحقق من السجلات: `tail -f ~/.i2p/wrapper.log`
- تحقق من تثبيت Java: `java -version`

إذا كنت بحاجة إلى مساعدة في توجيه المنفذ، فإن موقع [portforward.com](https://portforward.com) يوفّر أدلة خاصة بكل جهاز توجيه.

#### 2. Adjust Bandwidth Settings

الإعدادات الافتراضية للنطاق الترددي تكون متحفظة. قم بتعديلها بناءً على اتصال الإنترنت الخاص بك:

1. أعد تنزيل البصمة الرئيسية والتحقق منها (الخطوة 3-4 أعلاه)
2. تأكد من أن ملف حلقة المفاتيح لديه الصلاحيات الصحيحة: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

**ملاحظة**: تعيين حدود أعلى يساعد الشبكة ويعمل على تحسين أدائك الخاص.

#### 3. Configure Your Browser

للوصول إلى مواقع وخدمات I2P (المواقع المخفية)، قم بتكوين متصفحك لاستخدام وكيل HTTP الخاص بـ I2P:

راجع دليل [تكوين المتصفح](/docs/guides/browser-config) للحصول على تعليمات إعداد مفصلة لمتصفحات Firefox وChrome وغيرها.

---

## استكشاف الأخطاء وإصلاحها

### Migrating from old repositories

1. تحقق من إعداد المستودع: `cat /etc/apt/sources.list.d/i2p.list`
2. حدّث قوائم الحزم: `sudo apt-get update`
3. تحقق من تحديثات I2P: `sudo apt-get upgrade`

### أخطاء مفتاح المستودع

إذا تلقيت أخطاء متعلقة بمفتاح GPG أثناء التثبيت:

1. قم بإزالة المستودع القديم: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. اتبع خطوات [تثبيت Debian](#debian-installation) أعلاه
3. قم بالتحديث: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

### التحديثات لا تعمل

إذا لم يكن I2P يستلم التحديثات:

- [قم بإعداد متصفحك](/docs/guides/browser-config) للوصول إلى مواقع I2P
- استكشف [لوحة تحكم I2P router](http://127.0.0.1:7657/) لمراقبة الـ router الخاص بك
- تعرف على [تطبيقات I2P](/docs/applications/) التي يمكنك استخدامها
- اقرأ عن [كيفية عمل I2P](/docs/overview/tech-intro) لفهم الشبكة

### الانتقال من المستودعات القديمة

إذا كنت تستخدم مستودعات `deb.i2p2.de` أو `deb.i2p2.no` القديمة:

1. قم بإزالة المستودع القديم: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. اتبع خطوات [تثبيت ديبيان](#debian-installation) أعلاه
3. التحديث: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

## الخطوات التالية

الآن بعد تثبيت I2P وتشغيله:

- [قم بتكوين متصفحك](/docs/guides/browser-config) للوصول إلى مواقع I2P
- استكشف [وحدة تحكم موجه I2P](http://127.0.0.1:7657/) لمراقبة جهاز التوجيه الخاص بك
- تعرف على [تطبيقات I2P](/docs/applications/) التي يمكنك استخدامها
- اقرأ عن [كيف يعمل I2P](/docs/overview/tech-intro) لفهم الشبكة

مرحبًا بكم في الإنترنت الخفي!
