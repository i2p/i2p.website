---
title: "Git عبر I2P"
description: "توصيل عملاء Git بالخدمات المستضافة على I2P مثل i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

استنساخ ودفع المستودعات داخل I2P يستخدم نفس أوامر Git التي تعرفها بالفعل—عميلك يتصل ببساطة عبر tunnels الخاصة بـ I2P بدلاً من TCP/IP. يشرح هذا الدليل كيفية إعداد حساب وتكوين tunnels والتعامل مع الروابط البطيئة.

> **بداية سريعة:** الوصول للقراءة فقط يعمل من خلال وكيل HTTP: `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. اتبع الخطوات أدناه للوصول بصلاحيات القراءة/الكتابة عبر SSH.

## 1. إنشاء حساب

اختر خدمة Git على I2P وسجّل حسابًا:

- داخل I2P: `http://git.idk.i2p`
- المرآة على الإنترنت العادي: `https://i2pgit.org`

قد يتطلب التسجيل موافقة يدوية؛ تحقق من الصفحة الرئيسية للحصول على التعليمات. بمجرد الموافقة، قم بعمل fork أو إنشاء مستودع حتى يكون لديك شيء للاختبار به.

## 2. تكوين عميل I2PTunnel (SSH)

1. افتح وحدة تحكم router → **I2PTunnel** وأضف tunnel من نوع **Client** جديد.
2. أدخل وجهة الخدمة (Base32 أو Base64). بالنسبة لـ `git.idk.i2p` ستجد وجهتي HTTP وSSH على الصفحة الرئيسية للمشروع.
3. اختر منفذاً محلياً (على سبيل المثال `localhost:7442`).
4. فعّل التشغيل التلقائي إذا كنت تخطط لاستخدام tunnel بشكل متكرر.

ستؤكد واجهة المستخدم النفق الجديد وتعرض حالته. عندما يكون قيد التشغيل، يمكن لعملاء SSH الاتصال بـ `127.0.0.1` على المنفذ المختار.

## 3. الاستنساخ عبر SSH

استخدم منفذ النفق مع `GIT_SSH_COMMAND` أو مقطع تكوين SSH:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
إذا فشلت المحاولة الأولى (قد تكون الأنفاق بطيئة)، جرب استنساخًا سطحيًا:

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
قم بتكوين Git لجلب جميع الفروع:

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### نصائح الأداء

- أضف نفقًا أو اثنين احتياطيين في محرر الأنفاق لتحسين المرونة.
- للاختبار أو المستودعات منخفضة المخاطر يمكنك تقليل طول النفق إلى قفزة واحدة، ولكن كن على دراية بالمقايضة المتعلقة بعدم الكشف عن الهوية.
- احتفظ بـ `GIT_SSH_COMMAND` في بيئتك أو أضف إدخالاً إلى `~/.ssh/config`:

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
ثم قم بالاستنساخ باستخدام `git clone git@git.i2p:namespace/project.git`.

## 4. اقتراحات سير العمل

اعتمد سير عمل التفريع والتشعيب الشائع على GitLab/GitHub:

1. قم بتعيين مستودع upstream بعيد: `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. حافظ على تزامن `master` الخاص بك: `git pull upstream master`
3. أنشئ فروعاً للميزات من أجل التغييرات: `git checkout -b feature/new-thing`
4. ادفع الفروع إلى نسختك المنسوخة: `git push origin feature/new-thing`
5. قدم طلب دمج، ثم قم بعمل fast-forward لفرع master في نسختك المنسوخة من upstream.

## 5. تذكيرات الخصوصية

- يخزن Git طوابع الوقت للـ commit في المنطقة الزمنية المحلية الخاصة بك. لفرض طوابع الوقت بتوقيت UTC:

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
استخدم `git utccommit` بدلاً من `git commit` عندما تكون الخصوصية مهمة.

- تجنب تضمين عناوين URL أو عناوين IP من الإنترنت العادي (clearnet) في رسائل الالتزام أو البيانات الوصفية للمستودع إذا كانت عدم الكشف عن الهوية مصدر قلق.

## 6. استكشاف الأخطاء وإصلاحها

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
للسيناريوهات المتقدمة (نسخ المستودعات الخارجية، توزيع الحزم)، راجع الأدلة المصاحبة: [سير عمل حزم Git](/docs/applications/git-bundle/) و [استضافة GitLab عبر I2P](/docs/guides/gitlab/).
