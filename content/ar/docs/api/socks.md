---
title: "بروكسي SOCKS"
description: "استخدام نفق SOCKS الخاص بـ I2P بشكل آمن (محدث للإصدار 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **تحذير:** نفق SOCKS يُعيد توجيه حمولات التطبيقات دون تنظيفها. العديد من البروتوكولات تُسرّب عناوين IP أو أسماء المضيفين أو معرّفات أخرى. استخدم SOCKS فقط مع البرامج التي قمت بمراجعتها للتأكد من إخفاء الهوية.

---

## 1. نظرة عامة

يوفر I2P دعم بروكسي **SOCKS 4 و 4a و 5** للاتصالات الصادرة من خلال **عميل I2PTunnel**. يُمكّن التطبيقات القياسية من الوصول إلى وجهات I2P لكن **لا يمكنه الوصول إلى الإنترنت العادي (clearnet)**. لا يوجد **SOCKS outproxy**، وتبقى جميع حركة المرور داخل شبكة I2P.

### ملخص التنفيذ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**أنواع العناوين المدعومة:** - أسماء النطاقات `.i2p` (إدخالات دفتر العناوين) - عناوين Base32 المشفرة (`.b32.i2p`) - لا يوجد دعم لـ Base64 أو الإنترنت العادي

---

## 2. المخاطر الأمنية والقيود

### تسرب طبقة التطبيق

يعمل SOCKS أسفل طبقة التطبيق ولا يمكنه تنقية البروتوكولات. تتضمن العديد من العملاء (مثل المتصفحات وIRC والبريد الإلكتروني) بيانات وصفية تكشف عنوان IP الخاص بك أو اسم المضيف أو تفاصيل النظام.

تشمل التسريبات الشائعة: - عناوين IP في رؤوس البريد الإلكتروني أو استجابات IRC CTCP - الأسماء الحقيقية/أسماء المستخدمين في حمولات البروتوكول - سلاسل user-agent التي تحتوي على بصمات نظام التشغيل - استعلامات DNS الخارجية - WebRTC وبيانات القياس عن بُعد للمتصفح

**لا يمكن لـ I2P منع هذه التسريبات**—فهي تحدث فوق طبقة الـ tunnel. استخدم SOCKS فقط مع **العملاء المدققين** المصممين لإخفاء الهوية.

### هوية النفق المشترك

إذا شاركت عدة تطبيقات نفس نفق SOCKS، فإنها تشترك في نفس هوية وجهة I2P. وهذا يتيح الربط أو التعرف على البصمات عبر خدمات مختلفة.

**التخفيف:** استخدم **الأنفاق غير المشتركة** لكل تطبيق وقم بتفعيل **المفاتيح الدائمة** للحفاظ على هويات تشفيرية متسقة عبر إعادة التشغيل.

### تم إيقاف وضع UDP

دعم UDP في SOCKS5 غير مطبق. يعلن البروتوكول عن قدرة UDP، لكن يتم تجاهل الاستدعاءات. استخدم عملاء TCP فقط.

### بدون Outproxy بالتصميم

على عكس Tor، لا يوفر I2P وكلاء خروج (outproxies) إلى الإنترنت العادي تعتمد على **SOCKS**. ستفشل محاولات الوصول إلى عناوين IP الخارجية أو قد تكشف الهوية. استخدم وكلاء HTTP أو HTTPS إذا كان الوصول إلى الإنترنت الخارجي مطلوباً.

---

## 3. السياق التاريخي

لطالما حذّر المطورون من استخدام SOCKS للأغراض المجهولة. من مناقشات المطورين الداخلية و[الاجتماع 81](/ar/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) و[الاجتماع 82](/ar/blog/2004/03/23/i2p-dev-meeting-march-23-2004/) لعام 2004:

> "إعادة توجيه حركة المرور العشوائية غير آمن، ويتوجب علينا كمطورين لبرامج إخفاء الهوية أن نضع سلامة مستخدمينا النهائيين في مقدمة اهتماماتنا."

تم تضمين دعم SOCKS للتوافق ولكن لا يُنصح به في بيئات الإنتاج. تقريباً كل تطبيق إنترنت يسرب بيانات وصفية حساسة غير مناسبة للتوجيه المجهول.

---

## 4. الإعدادات

### Java I2P

1. افتح [مدير I2PTunnel](http://127.0.0.1:7657/i2ptunnel)  
2. أنشئ tunnel عميل جديد من نوع **"SOCKS 4/4a/5"**  
3. قم بتكوين الخيارات:  
   - المنفذ المحلي (أي منفذ متاح)  
   - العميل المشترك: *تعطيل* للحصول على هوية منفصلة لكل تطبيق  
   - المفتاح المستمر: *تفعيل* لتقليل ارتباط المفاتيح  
4. ابدأ تشغيل الـ tunnel

### i2pd

يتضمن i2pd دعم SOCKS5 مفعّل افتراضياً على `127.0.0.1:4447`. يمكنك ضبط المنفذ والمضيف ومعاملات tunnel من خلال الإعدادات في `i2pd.conf` تحت قسم `[SOCKSProxy]`.

---

## 5. الجدول الزمني للتطوير

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
لم يشهد وحدة SOCKS نفسها أي تحديثات رئيسية للبروتوكول منذ عام 2013، لكن مجموعة tunnel المحيطة بها حصلت على تحسينات في الأداء والتشفير.

---

## 6. البدائل الموصى بها

لأي تطبيق **إنتاجي**، **متاح للعامة**، أو **حساس أمنياً**، استخدم واحدة من واجهات برمجة التطبيقات الرسمية لـ I2P بدلاً من SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
توفر هذه الواجهات البرمجية عزلًا مناسبًا للوجهات، والتحكم في الهوية التشفيرية، وأداء توجيه أفضل.

---

## 7. OnionCat / GarliCat

يدعم OnionCat شبكة I2P من خلال وضع GarliCat الخاص به (نطاق IPv6 `fd60:db4d:ddb5::/48`). لا يزال يعمل ولكن مع تطوير محدود منذ عام 2019.

**تحذيرات الاستخدام:** - يتطلب تكوين يدوي لـ `.oc.b32.i2p` في SusiDNS   - يحتاج إلى تعيين ثابت لـ IPv6   - غير مدعوم رسمياً من مشروع I2P

يُوصى به فقط لإعدادات VPN-over-I2P المتقدمة.

---

## 8. أفضل الممارسات

إذا كان يجب عليك استخدام SOCKS: 1. أنشئ tunnels منفصلة لكل تطبيق.   2. عطّل وضع العميل المشترك.   3. فعّل المفاتيح المستمرة.   4. فرض حل DNS عبر SOCKS5.   5. راجع سلوك البروتوكول للكشف عن التسريبات.   6. تجنب اتصالات clearnet.   7. راقب حركة الشبكة للكشف عن التسريبات.

---

## 9. الملخص التقني

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. الخاتمة

يوفر بروكسي SOCKS في I2P توافقًا أساسيًا مع تطبيقات TCP الموجودة ولكنه **غير مصمم لضمانات إخفاء هوية قوية**. يجب استخدامه فقط في بيئات اختبار خاضعة للرقابة والمراجعة.

> للنشر الجاد، انتقل إلى **SAM v3** أو **Streaming API**. تعمل هذه الواجهات البرمجية على عزل هويات التطبيقات، وتستخدم التشفير الحديث، وتتلقى التطوير المستمر.

---

### موارد إضافية

- [مستندات SOCKS الرسمية](/docs/api/socks/)  
- [مواصفات SAM v3](/docs/api/samv3/)  
- [مستندات مكتبة البث](/docs/specs/streaming/)  
- [مرجع I2PTunnel](/docs/specs/implementation/)  
- [مستندات مطوري I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [منتدى المجتمع](https://i2pforum.net)
