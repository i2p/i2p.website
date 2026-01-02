---
title: "حزم Git لـ I2P"
description: "جلب وتوزيع المستودعات الكبيرة باستخدام git bundle وBitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

عندما تجعل ظروف الشبكة أمر `git clone` غير موثوق، يمكنك توزيع المستودعات على شكل **git bundles** عبر BitTorrent أو أي وسيلة نقل ملفات أخرى. الحزمة (bundle) هي ملف واحد يحتوي على سجل المستودع بالكامل. بمجرد التنزيل، تقوم بالجلب منها محلياً ثم تعود للاتصال بالمستودع البعيد الأساسي.

## 1. قبل أن تبدأ

إنشاء حزمة يتطلب استنساخ **كامل** لمستودع Git. الاستنساخات السطحية التي يتم إنشاؤها باستخدام `--depth 1` ستنتج بصمت حزمًا معطوبة تبدو وكأنها تعمل لكنها تفشل عندما يحاول الآخرون استخدامها. احرص دائمًا على الجلب من مصدر موثوق (GitHub على [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)، أو خادم Gitea الخاص بـ I2P على [i2pgit.org](https://i2pgit.org)، أو `git.idk.i2p` عبر I2P) وقم بتشغيل `git fetch --unshallow` إذا لزم الأمر لتحويل أي استنساخ سطحي إلى استنساخ كامل قبل إنشاء الحزم.

إذا كنت تستخدم حزمة موجودة فقط، فقم بتنزيلها فحسب. لا يلزم أي إعداد خاص.

## 2. تحميل حزمة

### Obtaining the Bundle File

قم بتنزيل ملف الحزمة عبر BitTorrent باستخدام I2PSnark (عميل التورنت المدمج في I2P) أو عملاء آخرين متوافقين مع I2P مثل BiglyBT مع إضافة I2P.

**مهم**: I2PSnark يعمل فقط مع ملفات التورنت المُنشأة خصيصًا لشبكة I2P. ملفات التورنت العادية من الإنترنت المفتوح غير متوافقة لأن I2P يستخدم Destinations (عناوين بحجم 387+ بايت) بدلاً من عناوين IP والمنافذ.

موقع ملف الحزمة يعتمد على نوع تثبيت I2P الخاص بك:

- **تثبيتات المستخدم/اليدوية** (المثبتة باستخدام مثبت Java): `~/.i2p/i2psnark/`
- **تثبيتات النظام/الخدمة** (المثبتة عبر apt-get أو مدير الحزم): `/var/lib/i2p/i2p-config/i2psnark/`

سيجد مستخدمو BiglyBT الملفات التي تم تنزيلها في دليل التنزيلات المُعَدّ لديهم.

### Cloning from the Bundle

**الطريقة القياسية** (تعمل في معظم الحالات):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
إذا واجهت أخطاء `fatal: multiple updates for ref` (مشكلة معروفة في Git 2.21.0 والإصدارات الأحدث عندما يحتوي إعداد Git العام على refspecs متضاربة للجلب)، استخدم طريقة التهيئة اليدوية:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
بدلاً من ذلك، يمكنك استخدام العلم `--update-head-ok`:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### الحصول على ملف الحزمة

بعد الاستنساخ من الحزمة، قم بتوجيه النسخة المستنسخة إلى المستودع البعيد المباشر حتى تتم عمليات الجلب المستقبلية عبر I2P أو clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
أو للوصول إلى الشبكة العادية:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
للوصول إلى SSH عبر I2P، تحتاج إلى تكوين tunnel عميل SSH في لوحة تحكم موجه I2P الخاص بك (عادةً المنفذ 7670) يشير إلى `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. إذا كنت تستخدم منفذاً غير قياسي:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### الاستنساخ من الحزمة

تأكد من أن المستودع الخاص بك محدّث بالكامل مع **نسخة كاملة** (وليست سطحية):

```bash
git fetch --all
```
إذا كان لديك نسخة محلية سطحية (shallow clone)، قم بتحويلها أولاً:

```bash
git fetch --unshallow
```
### التبديل إلى الوضع المباشر البعيد

**استخدام هدف البناء Ant** (موصى به لشجرة مصدر I2P):

```bash
ant git-bundle
```
هذا ينشئ كلاً من `i2p.i2p.bundle` (ملف الحزمة) و `i2p.i2p.bundle.torrent` (بيانات BitTorrent الوصفية).

**استخدام git bundle مباشرة**:

```bash
git bundle create i2p.i2p.bundle --all
```
للحزم الأكثر انتقائية:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

تحقق دائماً من الحزمة قبل التوزيع:

```bash
git bundle verify i2p.i2p.bundle
```
هذا يؤكد أن الحزمة صالحة ويعرض أي commits مطلوبة كمتطلبات مسبقة.

### المتطلبات الأساسية

انسخ الحزمة وبيانات التورنت الوصفية الخاصة بها إلى دليل I2PSnark الخاص بك:

**للتثبيتات الخاصة بالمستخدمين**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**لعمليات تثبيت النظام**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
يكتشف I2PSnark ويحمل ملفات .torrent تلقائيًا خلال ثوانٍ. يمكنك الوصول إلى واجهة الويب على [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) لبدء المشاركة.

## 4. Creating Incremental Bundles

للحصول على تحديثات دورية، قم بإنشاء حزم تدريجية تحتوي فقط على الـ commits الجديدة منذ آخر حزمة:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
يمكن للمستخدمين التحميل من الحزمة التدريجية إذا كان لديهم بالفعل المستودع الأساسي:

```bash
git fetch /path/to/update.bundle
```
تحقق دائمًا من أن الحزم التراكمية (incremental bundles) تعرض الالتزامات (commits) الأساسية المتوقعة:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

بمجرد أن يكون لديك مستودع عمل من الحزمة، تعامل معه كأي نسخة Git أخرى:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
أو لسير العمل الأبسط:

```bash
git fetch origin
git pull origin master
```
## 3. إنشاء حزمة

- **التوزيع المرن**: يمكن مشاركة المستودعات الكبيرة عبر BitTorrent، الذي يتعامل مع إعادة المحاولات والتحقق من القطع والاستئناف تلقائياً.
- **الإقلاع من نظير إلى نظير**: يمكن للمساهمين الجدد إقلاع نسختهم المستنسخة من النظراء القريبين على شبكة I2P، ثم جلب التغييرات التدريجية مباشرة من مستضيفات Git.
- **تقليل الحمل على الخادم**: يمكن للمرايا نشر حزم دورية لتخفيف الضغط على مستضيفات Git المباشرة، وهذا مفيد بشكل خاص للمستودعات الكبيرة أو ظروف الشبكة البطيئة.
- **النقل دون اتصال**: تعمل الحزم على أي وسيلة نقل للملفات (محركات USB، النقل المباشر، sneakernet)، وليس فقط BitTorrent.

الحزم لا تحل محل remotes المباشرة. إنها ببساطة توفر طريقة bootstrapping أكثر مرونة للاستنساخات الأولية أو التحديثات الرئيسية.

## 7. Troubleshooting

### توليد الحزمة

**المشكلة**: إنشاء الحزمة ينجح لكن الآخرين لا يستطيعون الاستنساخ من الحزمة.

**السبب**: نسختك المستنسخة من المصدر ضحلة (تم إنشاؤها باستخدام `--depth`).

**الحل**: التحويل إلى استنساخ كامل قبل إنشاء الحزم:

```bash
git fetch --unshallow
```
### التحقق من الحزمة الخاصة بك

**المشكلة**: `fatal: multiple updates for ref` عند الاستنساخ من bundle.

**السبب**: Git 2.21.0+ يتعارض مع مواصفات fetch العامة في `~/.gitconfig`.

**الحلول**: 1. استخدم التهيئة اليدوية: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. استخدم علامة `--update-head-ok`: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. احذف الإعدادات المتعارضة: `git config --global --unset remote.origin.fetch`

### التوزيع عبر I2PSnark

**المشكلة**: يُبلغ الأمر `git bundle verify` عن متطلبات مسبقة مفقودة.

**السبب**: حزمة تدريجية أو نسخة غير كاملة من المصدر.

**الحل**: إما جلب الـ commits المطلوبة مسبقاً أو استخدام الحزمة الأساسية أولاً، ثم تطبيق التحديثات التدريجية.
