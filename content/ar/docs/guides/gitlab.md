---
title: "تشغيل GitLab عبر I2P"
description: "نشر GitLab داخل I2P باستخدام Docker وموجه I2P"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

استضافة GitLab داخل I2P أمر مباشر: قم بتشغيل حاوية GitLab omnibus، وعرضها على loopback، وإعادة توجيه حركة المرور عبر tunnel في I2P. الخطوات أدناه تعكس التكوين المستخدم لـ `git.idk.i2p` ولكنها تعمل مع أي مثيل مستضاف ذاتياً.

## 1. المتطلبات الأساسية

- Debian أو توزيعة Linux أخرى مع تثبيت Docker Engine (`sudo apt install docker.io` أو `docker-ce` من مستودع Docker).
- router I2P (Java I2P أو i2pd) بعرض نطاق كافٍ لخدمة المستخدمين.
- اختياري: جهاز افتراضي مخصص بحيث يظل GitLab وال router معزولين عن بيئة سطح المكتب الخاصة بك.

## 2. سحب صورة GitLab

```bash
docker pull gitlab/gitlab-ce:latest
```
الصورة الرسمية مبنية من طبقات Ubuntu الأساسية ويتم تحديثها بانتظام. راجع [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) إذا كنت بحاجة إلى مزيد من الطمأنينة.

## 3. قرر بين الوضع الجسري أو I2P فقط

- مثيلات **I2P فقط** لا تتصل أبدًا بمضيفات clearnet. يمكن للمستخدمين نسخ المستودعات من خدمات I2P الأخرى ولكن ليس من GitHub/GitLab.com. هذا يزيد من إخفاء الهوية إلى أقصى حد.
- المثيلات **المجسورة** تصل إلى مضيفات Git على clearnet عبر وكيل HTTP. هذا مفيد لنسخ المشاريع العامة إلى I2P ولكنه يكشف هوية الطلبات الصادرة من الخادم.

إذا اخترت وضع الجسر (bridged mode)، قم بتكوين GitLab لاستخدام بروكسي I2P HTTP مرتبط على مضيف Docker (على سبيل المثال `http://172.17.0.1:4446`). يستمع بروكسي الموجه الافتراضي على `127.0.0.1` فقط؛ أضف tunnel بروكسي جديد مرتبط بعنوان بوابة Docker.

## 4. تشغيل الحاوية

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
- اربط المنافذ المنشورة بـ loopback؛ أنفاق I2P ستعرضها حسب الحاجة.
- استبدل `/srv/gitlab/...` بمسارات التخزين المناسبة لمضيفك.

بمجرد تشغيل الحاوية، قم بزيارة `https://127.0.0.1:8443/`، وقم بتعيين كلمة مرور المسؤول، وقم بتكوين حدود الحساب.

## 5. عرض GitLab عبر I2P

أنشئ ثلاثة أنفاق I2PTunnel من نوع **خادم**:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
قم بتكوين كل tunnel بأطوال tunnel وعرض نطاق مناسبين. بالنسبة للحالات العامة، 3 hops مع 4-6 tunnels لكل اتجاه تعتبر نقطة انطلاق جيدة. انشر وجهات Base32/Base64 الناتجة على صفحتك الرئيسية حتى يتمكن المستخدمون من تكوين client tunnels.

### Destination Enforcement

إذا كنت تستخدم أنفاق HTTP(S)، قم بتفعيل فرض الوجهة (destination enforcement) بحيث لا يمكن سوى لاسم المضيف المقصود الوصول إلى الخدمة. هذا يمنع استغلال النفق كوكيل عام.

## 6. Maintenance Tips

- قم بتشغيل `docker exec gitlab gitlab-ctl reconfigure` كلما قمت بتغيير إعدادات GitLab.
- راقب استخدام القرص (`/srv/gitlab/data`)—مستودعات Git تنمو بسرعة.
- قم بعمل نسخ احتياطية لدلائل الإعدادات والبيانات بانتظام. [مهام backup rake الخاصة بـ GitLab](https://docs.gitlab.com/ee/raketasks/backup_restore.html) تعمل داخل الحاوية.
- فكّر في وضع نفق مراقبة خارجي في وضع العميل للتأكد من إمكانية الوصول إلى الخدمة من الشبكة الأوسع.

## 6. نصائح الصيانة

- [تضمين I2P في تطبيقك](/docs/applications/embedding/)
- [Git عبر I2P (دليل العميل)](/docs/applications/git/)
- [حزم Git للشبكات غير المتصلة/البطيئة](/docs/applications/git-bundle/)

توفر نسخة GitLab مهيأة جيدًا مركزًا للتطوير التعاوني بالكامل داخل I2P. حافظ على صحة الـ router، وابقَ محدثًا بتحديثات أمان GitLab، ونسّق مع المجتمع مع نمو قاعدة المستخدمين لديك.
