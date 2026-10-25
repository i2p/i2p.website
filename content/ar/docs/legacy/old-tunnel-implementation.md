---
title: "تطبيق Tunnel القديم"
description: "التوثيق التاريخي لتطبيق tunnel الأصلي في I2P قبل الإصدار 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/ar/docs/historical/tunnel-alt"
  - "/ar/docs/historical/tunnel-alt/"
  - "/ar/tunnel"
  - "/ar/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**ملاحظة: مهجور - غير مستخدم! تم استبداله في 0.6.1.10 - انظر [التنفيذ الحالي](/docs/specs/tunnel-implementation) للمواصفة النشطة.**

## 1) نظرة عامة على tunnel {#tunnel.overview}

داخل I2P، يتم تمرير الرسائل في اتجاه واحد عبر tunnel افتراضي من الأقران، باستخدام أي وسائل متاحة لتمرير الرسالة إلى القفزة التالية. تصل الرسائل إلى بوابة tunnel، ويتم تجميعها للمسار، وتُحوَّل إلى القفزة التالية في tunnel، والتي تعالج وتتحقق من صحة الرسالة وترسلها إلى القفزة التالية، وهكذا، حتى تصل إلى نقطة نهاية tunnel. تأخذ نقطة النهاية هذه الرسائل المجمعة بواسطة البوابة وتحولها كما هو مطلوب - إما إلى router آخر، أو إلى tunnel آخر على router آخر، أو محلياً.

تعمل جميع الـ tunnels بنفس الطريقة، ولكن يمكن تقسيمها إلى مجموعتين مختلفتين - الـ inbound tunnels والـ outbound tunnels. الـ inbound tunnels لها gateway غير موثوق يمرر الرسائل نحو منشئ الـ tunnel، والذي يعمل كنقطة نهاية الـ tunnel. بالنسبة للـ outbound tunnels، فإن منشئ الـ tunnel يعمل كـ gateway، حيث يمرر الرسائل إلى نقطة النهاية البعيدة.

يختار منشئ النفق بالضبط أي من الأقران سيشاركون في النفق، ويزود كل منهم ببيانات التكوين اللازمة. قد تتفاوت في الطول من 0 قفزة (حيث يكون البوابة هو أيضاً نقطة النهاية) إلى 7 قفزات (حيث توجد 6 أقران بعد البوابة وقبل نقطة النهاية). الهدف هو جعل من الصعب على المشاركين أو الأطراف الثالثة تحديد طول النفق، أو حتى للمشاركين المتواطئين تحديد ما إذا كانوا جزءاً من نفس النفق على الإطلاق (باستثناء الحالة التي يكون فيها الأقران المتواطئون بجانب بعضهم البعض في النفق). الرسائل التي تم إفسادها يتم أيضاً إسقاطها في أسرع وقت ممكن، مما يقلل من حمولة الشبكة.

بالإضافة إلى طولها، هناك معاملات قابلة للتكوين إضافية لكل tunnel يمكن استخدامها، مثل التحكم في حجم أو تكرار الرسائل المسلمة، وكيفية استخدام الحشو، وكم من الوقت يجب أن يكون tunnel في التشغيل، وما إذا كان يجب حقن رسائل chaff، وما إذا كان يجب استخدام التجزئة، وما هي استراتيجيات التجميع التي يجب توظيفها، إن وجدت.

في الممارسة العملية، يتم استخدام سلسلة من مجمعات الـ tunnel لأغراض مختلفة - كل وجهة عميل محلية لديها مجموعتها الخاصة من الـ inbound tunnels والـ outbound tunnels، مُكوّنة لتلبية احتياجاتها من إخفاء الهوية والأداء. بالإضافة إلى ذلك، يحتفظ الـ router نفسه بسلسلة من المجمعات للمشاركة في قاعدة بيانات الشبكة وإدارة الـ tunnels نفسها.

I2P هي شبكة تبديل حزم بطبيعتها، حتى مع هذه الأنفاق، مما يتيح لها الاستفادة من عدة أنفاق تعمل بشكل متوازي، وبالتالي زيادة المرونة وتوزيع الحمولة. خارج طبقة I2P الأساسية، توجد مكتبة اختيارية للبث المباشر من نقطة إلى نقطة متاحة لتطبيقات العميل، تكشف عن عمليات شبيهة بـ TCP، بما في ذلك إعادة ترتيب الرسائل، وإعادة الإرسال، والتحكم في الازدحام، إلخ.

## 2) عملية tunnel {#tunnel.operation}

تتضمن عملية التشغيل في tunnel أربع عمليات متميزة، يقوم بها أطراف مختلفون في tunnel. أولاً، يجمع gateway الخاص بـ tunnel عدداً من رسائل tunnel ويعالجها مسبقاً لتصبح شيئاً قابلاً للتسليم عبر tunnel. بعد ذلك، يشفر هذا gateway البيانات المعالجة مسبقاً، ثم يرسلها إلى القفزة الأولى. يقوم ذلك الطرف، والمشاركون التاليون في tunnel، بإزالة طبقة من التشفير، والتحقق من سلامة الرسالة، ثم إرسالها إلى الطرف التالي. في النهاية، تصل الرسالة إلى نقطة النهاية حيث يتم فصل الرسائل المجمعة بواسطة gateway مرة أخرى وإرسالها كما هو مطلوب.

معرفات الـ tunnel هي أرقام من 4 بايتات تُستخدم في كل قفزة - يعرف المشاركون أي معرف tunnel يجب الاستماع إليه للرسائل وأي معرف tunnel يجب إعادة توجيهها عليه إلى القفزة التالية. الـ tunnels نفسها قصيرة المدى (10 دقائق في الوقت الحالي)، ولكن اعتماداً على غرض الـ tunnel، وعلى الرغم من أن الـ tunnels اللاحقة قد يتم بناؤها باستخدام نفس تسلسل النظراء، فإن معرف tunnel لكل قفزة سيتغير.

### 2.1) معالجة الرسائل المسبقة {#tunnel.preprocessing}

عندما يريد gateway تسليم البيانات عبر tunnel، فإنه يجمع أولاً رسائل I2NP واحدة أو أكثر (بحد أقصى 32KB)، ويختار مقدار الحشو الذي سيتم استخدامه، ويقرر كيف يجب على نقطة نهاية tunnel التعامل مع كل رسالة I2NP، ثم يقوم بتشفير تلك البيانات في الحمولة الخام للـ tunnel:

- عدد صحيح غير مُوقع من 2 بايت يحدد عدد بايتات الحشو
- عدد مطابق من البايتات العشوائية
- سلسلة من صفر أو أكثر من أزواج { التعليمات، الرسالة }

التعليمات مُرمزة كما يلي:

- قيمة 1 بايت:
  ```
  bits 0-1: delivery type
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: delay included?  (1 = true, 0 = false)
     bit 3: fragmented?  (1 = true, 0 = false)
     bit 4: extended options?  (1 = true, 0 = false)
  bits 5-7: reserved
  ```
- إذا كان نوع التسليم TUNNEL، فسيكون هناك معرف tunnel بحجم 4 بايت
- إذا كان نوع التسليم TUNNEL أو ROUTER، فسيكون هناك router hash بحجم 32 بايت
- إذا كانت علامة تضمين التأخير صحيحة، قيمة 1 بايت:
  ```
     bit 0: type (0 = strict, 1 = randomized)
  bits 1-7: delay exponent (2^value minutes)
  ```
- إذا كانت علامة التجزئة صحيحة، معرف رسالة بحجم 4 بايت، وقيمة 1 بايت:
  ```
  bits 0-6: fragment number
     bit 7: is last?  (1 = true, 0 = false)
  ```
- إذا كانت علامة الخيارات الموسعة صحيحة:
  ```
  = حجم خيار بحجم 1 بايت (بالبايت)
  = ذلك العدد من البايتات
  ```
- حجم رسالة I2NP بحجم 2 بايت

يتم ترميز رسالة I2NP في شكلها المعياري، ويجب حشو الحمولة المعالجة مسبقاً لتصبح مضاعفاً لـ 16 بايت.

### 2.2) معالجة البوابة {#tunnel.gateway}

بعد المعالجة المسبقة للرسائل إلى حمولة مبطنة، يقوم الـ gateway بتشفير الحمولة باستخدام المفاتيح الثمانية، وبناء كتلة checksum حتى يتمكن كل peer من التحقق من سلامة الحمولة في أي وقت، بالإضافة إلى كتلة التحقق من النهاية إلى النهاية لنقطة نهاية الـ tunnel للتحقق من سلامة كتلة الـ checksum. التفاصيل المحددة تتبع.

التشفير المستخدم هو بحيث أن فك التشفير يتطلب فقط تشغيل البيانات باستخدام AES في وضع CBC، وحساب SHA256 لجزء ثابت معين من الرسالة (البايتات من 16 إلى $size-144)، والبحث عن أول 16 بايت من هذا الهاش في كتلة المجموع الاختباري. يوجد عدد ثابت من القفزات محدد (8 عقد) بحيث يمكننا التحقق من الرسالة دون تسريب الموقع في tunnel أو جعل الرسالة "تتقلص" باستمرار عند إزالة الطبقات. بالنسبة للـ tunnels الأقصر من 8 قفزات، سيأخذ منشئ tunnel مكان القفزات الزائدة، ويقوم بفك التشفير باستخدام مفاتيحه (بالنسبة للـ tunnels الصادرة، يتم هذا في البداية، وبالنسبة للـ tunnels الواردة، في النهاية).

الجزء الصعب في التشفير هو بناء كتلة المجموع التحققي المتشابكة، والذي يتطلب في الأساس معرفة كيف سيبدو hash الحمولة في كل خطوة، ترتيب هذه الـ hashes عشوائياً، ثم بناء مصفوفة لكيف سيبدو كل من هذه الـ hashes المرتبة عشوائياً في كل خطوة. يجب على البوابة نفسها أن تتظاهر بأنها واحدة من الأقران داخل كتلة المجموع التحققي حتى لا تستطيع القفزة الأولى معرفة أن القفزة السابقة كانت البوابة. لتصور هذا قليلاً:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
في المثال أعلاه، P[7] هو نفس البيانات الأصلية التي يتم تمريرها عبر tunnel (الرسائل المعالجة مسبقاً)، و V[7] هو أول 16 بايت من SHA256 لـ eH[0-7] كما يُرى على peer7 بعد فك التشفير. بالنسبة للخلايا في المصفوفة "الأعلى" من الـ hash، يتم اشتقاق قيمتها عن طريق تشفير الخلية الموجودة أسفلها بمفتاح الـ peer الموجود أسفلها، باستخدام نهاية العمود الموجود على يسارها كـ IV. بالنسبة للخلايا في المصفوفة "الأسفل" من الـ hash، فهي تساوي الخلية الموجودة فوقها، مفكوكة التشفير بمفتاح الـ peer الحالي، باستخدام نهاية الكتلة المشفرة السابقة في ذلك الصف.

مع هذه المصفوفة العشوائية من كتل checksum، سيكون كل peer قادراً على العثور على hash الخاص بالحمولة، أو إذا لم تكن موجودة، معرفة أن الرسالة تالفة. التشابك باستخدام وضع CBC يزيد من صعوبة وضع علامات على كتل checksum نفسها، ولكن لا يزال من الممكن أن تمر هذه العلامات دون اكتشاف لفترة وجيزة إذا كانت الأعمدة التي تلي البيانات المعلمة قد استُخدمت بالفعل للتحقق من الحمولة عند peer. في جميع الأحوال، نقطة نهاية tunnel (peer 7) تعرف بيقين ما إذا كانت أي من كتل checksum قد تم وضع علامات عليها، حيث أن ذلك سيؤدي إلى إفساد كتلة التحقق (V[7]).

IV[0] هو قيمة عشوائية من 16 بايت، و IV[i] هو أول 16 بايت من H(D(IV[i-1], K[i-1]) xor IV_WHITENER). لا نستخدم نفس IV على طول المسار، حيث أن ذلك سيسمح بتواطؤ بسيط، ونستخدم hash القيمة المفكوكة التشفير لنشر IV بحيث نعرقل تسرب المفتاح. IV_WHITENER هو قيمة ثابتة من 16 بايت.

عندما يريد الـ gateway إرسال الرسالة، يقوم بتصدير الصف الصحيح للند الذي يمثل القفزة الأولى (عادة صف peer1.recv) ويقوم بإعادة توجيهه بالكامل.

### 2.3) معالجة المشارك {#tunnel.participant}

عندما يستقبل مشارك في tunnel رسالة، يقوم بفك تشفير طبقة باستخدام مفتاح tunnel الخاص به باستخدام AES256 في وضع CBC مع أول 16 بايت كـ IV. ثم يقوم بحساب hash لما يراه كحمولة (البايتات من 16 إلى $size-144) ويبحث عن أول 16 بايت من ذلك hash داخل كتلة checksum المفكوكة التشفير. إذا لم يتم العثور على تطابق، يتم تجاهل الرسالة. وإلا، يتم تحديث IV عبر فك تشفيره، وإجراء XOR لتلك القيمة مع IV_WHITENER، واستبداله بأول 16 بايت من hash الخاص به. الرسالة الناتجة يتم إرسالها بعد ذلك إلى النظير التالي للمعالجة.

لمنع هجمات إعادة التشغيل على مستوى tunnel، يتتبع كل مشارك قيم IV المستلمة خلال فترة حياة tunnel، ويرفض المكررات. يجب أن يكون استخدام الذاكرة المطلوب طفيفاً، حيث أن كل tunnel له فترة حياة قصيرة جداً (10 دقائق في الوقت الحالي). معدل ثابت قدره 100 كيلوبايت/ثانية عبر tunnel مع رسائل 32 كيلوبايت كاملة سيعطي 1875 رسالة، مما يتطلب أقل من 30 كيلوبايت من الذاكرة. تتعامل البوابات ونقاط النهاية مع إعادة التشغيل من خلال تتبع معرفات الرسائل وتواريخ انتهاء الصلاحية على رسائل I2NP الموجودة في tunnel.

### 2.4) معالجة نقطة النهاية {#tunnel.endpoint}

عندما تصل الرسالة إلى نقطة نهاية tunnel، فإنها تفك التشفير وتتحقق منها مثل المشارك العادي. إذا كانت كتلة المجموع الاختباري تحتوي على تطابق صحيح، فإن نقطة النهاية تقوم بحساب hash لكتلة المجموع الاختباري نفسها (كما تظهر بعد فك التشفير) وتقارنها بـ hash التحقق المفكوك التشفير (الـ 16 بايت الأخيرة). إذا لم يتطابق hash التحقق هذا، فإن نقطة النهاية تأخذ علماً بمحاولة الوسم من قِبل أحد مشاركي tunnel وربما تتجاهل الرسالة.

في هذه المرحلة، تحصل نقطة نهاية النفق على البيانات المعالجة مسبقاً التي أرسلتها البوابة، والتي قد تقوم بعدها بتحليلها واستخراج رسائل I2NP المضمنة وتوجيهها حسب المطلوب في تعليمات التسليم الخاصة بها.

### 2.5) الحشو {#tunnel.padding}

عدة استراتيجيات لحشو tunnel ممكنة، لكل منها مزاياها الخاصة:

- لا توجد حشوة
- حشوة إلى حجم عشوائي
- حشوة إلى حجم ثابت
- حشوة إلى أقرب كيلوبايت
- حشوة إلى أقرب حجم أسي (2^n بايت)

*أيهما نستخدم؟ عدم وجود padding هو الأكثر كفاءة، التعبئة العشوائية (random padding) هي ما لدينا حالياً، الحجم الثابت سيكون إما هدراً شديداً أو يجبرنا على تنفيذ التجزئة. التعبئة إلى أقرب حجم أسي (على غرار Freenet) يبدو واعداً. ربما يجب أن نجمع بعض الإحصائيات على الشبكة حول أحجام الرسائل، ثم نرى ما التكاليف والفوائد التي ستنشأ من استراتيجيات مختلفة؟*

### 2.6) تجزئة tunnel {#tunnel.fragmentation}

بالنسبة لمخططات الحشو والخلط المختلفة، قد يكون من المفيد من ناحية إخفاء الهوية تجزئة رسالة I2NP واحدة إلى أجزاء متعددة، يتم تسليم كل منها بشكل منفصل من خلال رسائل tunnel مختلفة. قد تدعم نقطة النهاية هذا التجزيء أو لا تدعمه (بتجاهل أو الاحتفاظ بالأجزاء حسب الحاجة)، ولن يتم تنفيذ التعامل مع التجزيء على الفور.

### 2.7) البدائل {#tunnel.alternatives}

#### 2.7.1) لا تستخدم كتلة المجموع الاختباري {#tunnel.nochecksum}

أحد البدائل للعملية المذكورة أعلاه هو إزالة كتلة checksum بالكامل واستبدال hash التحقق بـ hash عادي للحمولة. هذا من شأنه أن يبسط المعالجة في بوابة tunnel ويوفر 144 بايت من عرض النطاق الترددي في كل hop. من ناحية أخرى، يمكن للمهاجمين داخل tunnel تعديل حجم الرسالة بسهولة إلى حجم يمكن تتبعه بسهولة من قبل المراقبين الخارجيين المتواطئين بالإضافة إلى مشاركي tunnel اللاحقين. كما أن التلف سيؤدي إلى إهدار كامل عرض النطاق الترددي اللازم لتمرير الرسالة. بدون التحقق لكل hop، سيكون من الممكن أيضاً استهلاك موارد الشبكة الزائدة من خلال بناء tunnels طويلة للغاية، أو من خلال بناء حلقات في tunnel.

#### 2.7.2) تعديل معالجة tunnel وسط العملية {#tunnel.reroute}

بينما يجب أن تكون خوارزمية توجيه tunnel البسيطة كافية لمعظم الحالات، هناك ثلاثة بدائل يمكن استكشافها:

- تأخير رسالة داخل tunnel في hop عشوائي إما لفترة زمنية محددة أو لفترة عشوائية. يمكن تحقيق هذا عبر استبدال الـ hash في كتلة الـ checksum بـ مثلاً أول 8 bytes من الـ hash، متبوعة بتعليمات التأخير. بدلاً من ذلك، يمكن للتعليمات أن تخبر المشارك بتفسير الـ payload الخام كما هو فعلاً، وإما التخلص من الرسالة أو الاستمرار في توجيهها عبر المسار (حيث سيتم تفسيرها من قبل نقطة النهاية كرسالة chaff). الجزء الأخير من هذا سيتطلب من الـ gateway تعديل خوارزمية التشفير الخاصة به لإنتاج الـ payload الواضح في hop مختلف، لكن هذا لا يجب أن يكون مشكلة كبيرة.

- السماح للـ routers المشاركة في tunnel بإعادة خلط الرسالة قبل إعادة توجيهها - ارتدادها عبر واحد من tunnels الصادرة الخاصة بذلك النظير، حاملة تعليمات للتسليم إلى القفزة التالية. يمكن استخدام هذا إما بطريقة محكومة (مع تعليمات في الطريق مثل التأخيرات أعلاه) أو بطريقة احتمالية.

- تنفيذ كود لمنشئ tunnel ليعيد تعريف "القفزة التالية" للنظير في tunnel، مما يسمح بإعادة توجيه ديناميكية إضافية.

#### 2.7.3) استخدام tunnels ثنائية الاتجاه {#tunnel.bidirectional}

الاستراتيجية الحالية لاستخدام tunnel منفصلين للاتصالات الواردة والصادرة ليست التقنية الوحيدة المتاحة، ولها تأثيرات على إخفاء الهوية. من الناحية الإيجابية، باستخدام tunnel منفصلين يقلل من بيانات حركة المرور المكشوفة للتحليل للمشاركين في tunnel - على سبيل المثال، النظراء في tunnel صادر من متصفح الويب سيرون فقط حركة مرور HTTP GET، بينما النظراء في tunnel وارد سيرون البيانات المُسلمة عبر tunnel. مع tunnel ثنائية الاتجاه، جميع المشاركين سيكون لديهم إمكانية الوصول لحقيقة أنه مثلاً تم إرسال 1KB في اتجاه واحد، ثم 100KB في الاتجاه الآخر. من الناحية السلبية، استخدام tunnel أحادية الاتجاه يعني أن هناك مجموعتين من النظراء التي تحتاج إلى وضع ملف تعريف ومحاسبة، ويجب اتخاذ عناية إضافية لمعالجة السرعة المتزايدة لهجمات predecessor. عملية تجميع وبناء tunnel المذكورة أدناه يجب أن تقلل من مخاوف هجوم predecessor، رغم أنه لو كان مرغوباً فيه، لن يكون من المشاكل الكبيرة بناء tunnel الوارد والصادر على نفس النظراء.

#### 2.7.4) استخدام حجم كتلة أصغر {#tunnel.smallerhashes}

في الوقت الحالي، استخدامنا لـ AES يحد من حجم الكتلة إلى 16 بايت، مما يوفر بدوره الحد الأدنى لحجم كل عمود من أعمدة كتلة المجموع الاختباري. إذا تم استخدام خوارزمية أخرى بحجم كتلة أصغر، أو يمكنها بطريقة أخرى السماح ببناء آمن لكتلة المجموع الاختباري بأجزاء أصغر من الـ hash، فقد يكون من المجدي استكشاف ذلك. الـ 16 بايت المستخدمة الآن في كل hop يجب أن تكون كافية أكثر من اللازم.

## 3) بناء tunnel {#tunnel.building}

عند بناء tunnel، يجب على المنشئ إرسال طلب مع بيانات التكوين اللازمة إلى كل من القفزات، ثم انتظار المشارك المحتمل للرد بالموافقة أو عدم الموافقة. رسائل طلب tunnel هذه وردودها مُغلّفة بـ garlic encryption بحيث لا يمكن سوى للـ router الذي يعرف المفتاح فك تشفيرها، والمسار المتخذ في كلا الاتجاهين موجه عبر tunnel أيضاً. هناك ثلاثة أبعاد مهمة يجب وضعها في الاعتبار عند إنتاج tunnels: أي أقران يتم استخدامها (وأين)، كيف يتم إرسال الطلبات (واستقبال الردود)، وكيف يتم صيانتها.

### 3.1) اختيار النظراء {#tunnel.peerselection}

بالإضافة إلى نوعي الـ tunnels - الوارد والصادر - هناك نمطان لاختيار النظراء يُستخدمان للـ tunnels المختلفة - الاستكشافي والعميل. تُستخدم الـ tunnels الاستكشافية لكل من صيانة قاعدة بيانات الشبكة وصيانة الـ tunnels، بينما تُستخدم tunnels العميل لرسائل العميل من طرف إلى طرف.

#### 3.1.1) اختيار الأقران لـ tunnel الاستكشافي {#tunnel.selection.exploratory}

يتم بناء الأنفاق الاستكشافية من مجموعة عشوائية من النظراء من مجموعة فرعية من الشبكة. تختلف المجموعة الفرعية المحددة بناءً على router المحلي وعلى احتياجات tunnel routing الخاصة به. بشكل عام، يتم بناء الأنفاق الاستكشافية من النظراء المختارين عشوائياً والذين يندرجون في فئة "غير فاشل ولكن نشط" في ملف تعريف النظراء. الغرض الثانوي من الأنفاق، إلى جانب tunnel routing فحسب، هو العثور على النظراء عالية السعة وقليلة الاستخدام بحيث يمكن ترقيتها للاستخدام في أنفاق العميل.

#### 3.1.2) اختيار نظير tunnel العميل {#tunnel.selection.client}

يتم بناء أنفاق العميل بمجموعة أكثر صرامة من المتطلبات - حيث سيقوم router المحلي باختيار النظراء من فئة الملف الشخصي "السريع وعالي السعة" بحيث يلبي الأداء والموثوقية احتياجات تطبيق العميل. ومع ذلك، هناك عدة تفاصيل مهمة تتجاوز هذا الاختيار الأساسي يجب الالتزام بها، اعتماداً على احتياجات إخفاء الهوية الخاصة بالعميل.

بالنسبة لبعض العملاء الذين يشعرون بالقلق من قيام الخصوم بتنفيذ هجوم السلف، يمكن لاختيار tunnel أن يحافظ على ترتيب النظراء المحددين بشكل صارم - إذا كان A وB وC في tunnel، فإن القفزة بعد A هي دائماً B، والقفزة بعد B هي دائماً C. الترتيب الأقل صرامة ممكن أيضاً، مما يضمن أنه بينما قد تكون القفزة بعد A هي B، فإن B لا يمكن أبداً أن يكون قبل A. تشمل خيارات التكوين الأخرى القدرة على جعل بوابات tunnel الواردة ونقاط نهاية tunnel الصادرة ثابتة فقط، أو تدويرها بمعدل MTBF.

### 3.2) تسليم الطلب {#tunnel.request}

كما ذُكر أعلاه، بمجرد أن يعرف منشئ النفق ما هي العقد التي يجب أن تدخل في النفق وبأي ترتيب، ينشئ المنشئ سلسلة من رسائل طلب النفق، كل منها تحتوي على المعلومات الضرورية لتلك العقدة. على سبيل المثال، الأنفاق المشاركة ستُعطى معرف النفق المكون من 4 بايت والذي يجب أن تستقبل عليه الرسائل، ومعرف النفق المكون من 4 بايت والذي يجب أن ترسل عليه الرسائل، والـ hash المكون من 32 بايت لهوية القفزة التالية، ومفتاح الطبقة المكون من 32 بايت المستخدم لإزالة طبقة من النفق. بالطبع، نقاط نهاية الأنفاق الصادرة لا تُعطى أي معلومات حول "القفزة التالية" أو "معرف النفق التالي". بوابات الأنفاق الواردة تُعطى مع ذلك مفاتيح الطبقات الثمانية بالترتيب الذي يجب أن تُشفر به (كما هو موصوف أعلاه). للسماح بالردود، يحتوي الطلب على session tag عشوائي ومفتاح session عشوائي يمكن للعقدة أن تستخدمه لـ garlic encrypt قرارها، بالإضافة إلى النفق الذي يجب أن يُرسل إليه ذلك الـ garlic. بالإضافة إلى المعلومات المذكورة أعلاه، قد يتم تضمين خيارات خاصة بالعميل المتنوعة، مثل ما هي عمليات التحكم في التدفق التي يجب وضعها على النفق، وما هي استراتيجيات الحشو أو المجموعات التي يجب استخدامها، إلخ.

بعد بناء جميع رسائل الطلب، يتم تغليفها بـ garlic encryption للموجه المستهدف وإرسالها عبر نفق استكشافي. عند الاستلام، يحدد ذلك النظير ما إذا كان بإمكانه أو سيشارك، حيث ينشئ رسالة رد ويقوم بكل من تغليف garlic وتوجيه tunnel للاستجابة باستخدام المعلومات المقدمة. عند استلام الرد في منشئ tunnel، يُعتبر tunnel صالحًا في تلك القفزة (إذا تم قبوله). بمجرد أن يقبل جميع الأنظار، يصبح tunnel نشطًا.

### 3.3) التجميع {#tunnel.pooling}

للسماح بالتشغيل الفعال، يحتفظ الـ router بسلسلة من مجمعات الـ tunnel، حيث تدير كل مجمعة مجموعة من الـ tunnels المستخدمة لغرض محدد مع تكوينها الخاص. عندما يكون هناك حاجة لـ tunnel لذلك الغرض، يختار الـ router واحداً من المجمعة المناسبة عشوائياً. بشكل عام، هناك مجمعتان استكشافيتان للـ tunnel - واحدة واردة وواحدة صادرة - كل منهما تستخدم إعدادات الاستكشاف الافتراضية للـ router. بالإضافة إلى ذلك، هناك زوج من المجمعات لكل وجهة محلية - مجمعة tunnel وارد ومجمعة tunnel صادر. تستخدم هذه المجمعات التكوين المحدد عندما اتصلت الوجهة المحلية بالـ router، أو إعدادات الـ router الافتراضية إذا لم تكن محددة.

كل pool يحتوي ضمن إعداداته على بعض الإعدادات الأساسية، التي تحدد عدد الـ tunnels التي يجب الاحتفاظ بها نشطة، وعدد الـ tunnels الاحتياطية التي يجب الاحتفاظ بها في حالة الفشل، وعدد مرات اختبار الـ tunnels، وطول الـ tunnels، وما إذا كان يجب عشوائية هذه الأطوال، وعدد مرات بناء tunnels بديلة، بالإضافة إلى أي من الإعدادات الأخرى المسموحة عند تكوين tunnels فردية.

### 3.4) البدائل {#tunnel.building.alternatives}

#### 3.4.1) البناء التلسكوبي {#tunnel.building.telescoping}

أحد الأسئلة التي قد تثار بخصوص استخدام الأنفاق الاستكشافية لإرسال واستقبال رسائل إنشاء الأنفاق هو كيف يؤثر ذلك على قابلية النفق للتعرض لهجمات السلف. بينما ستكون نقاط النهاية والبوابات لتلك الأنفاق موزعة عشوائياً عبر الشبكة (ربما حتى تتضمن منشئ النفق في تلك المجموعة)، هناك بديل آخر وهو استخدام مسارات الأنفاق نفسها لتمرير الطلب والاستجابة، كما يحدث في [TOR](https://www.torproject.org/). هذا، مع ذلك، قد يؤدي إلى تسريبات أثناء إنشاء النفق، مما يسمح للأقران باكتشاف عدد القفزات الموجودة لاحقاً في النفق من خلال مراقبة التوقيت أو عدد الحزم أثناء بناء النفق. يمكن استخدام تقنيات لتقليل هذه المشكلة، مثل استخدام كل من القفزات كنقاط نهاية (حسب [2.7.2](#tunnel.reroute)) لعدد عشوائي من الرسائل قبل المتابعة لبناء القفزة التالية.

#### 3.4.2) أنفاق غير استكشافية للإدارة {#tunnel.building.nonexploratory}

البديل الثاني لعملية بناء tunnel هو إعطاء router مجموعة إضافية من تجمعات الداخلة والخارجة غير الاستكشافية، باستخدام تلك التجمعات لطلب واستجابة tunnel. بافتراض أن router لديه رؤية متكاملة جيدة للشبكة، فإن هذا لا ينبغي أن يكون ضرورياً، ولكن إذا كان router مقسماً بطريقة ما، فإن استخدام التجمعات غير الاستكشافية لإدارة tunnel سيقلل من تسريب المعلومات حول النظراء الموجودين في قسم router.

## 4) خنق tunnel {#tunnel.throttling}

على الرغم من أن tunnels داخل I2P تشبه الشبكات المبدلة بالدوائر، إلا أن كل شيء داخل I2P يعتمد بشكل صارم على الرسائل - tunnels ما هي إلا حيل محاسبية للمساعدة في تنظيم توصيل الرسائل. لا يتم افتراض أي شيء بخصوص موثوقية أو ترتيب الرسائل، وتُترك عمليات إعادة الإرسال للمستويات الأعلى (مثل مكتبة البث المتدفق في طبقة عميل I2P). هذا يسمح لـ I2P بالاستفادة من تقنيات التحكم في التدفق المتاحة لكل من الشبكات المبدلة بالحزم والشبكات المبدلة بالدوائر. على سبيل المثال، قد يحتفظ كل router بتتبع المتوسط المتحرك لكمية البيانات التي يستخدمها كل tunnel، ويجمع ذلك مع جميع المتوسطات المستخدمة بواسطة tunnels أخرى يشارك فيها router، ويكون قادراً على قبول أو رفض طلبات المشاركة الإضافية في tunnel بناءً على سعته واستخدامه. من ناحية أخرى، يمكن لكل router ببساطة إسقاط الرسائل التي تتجاوز قدرته، مستفيداً من البحوث المستخدمة على الإنترنت العادي.

## 5) الخلط/التجميع {#tunnel.mixing}

ما هي الاستراتيجيات التي يجب استخدامها عند gateway وعند كل hop لتأخير أو إعادة ترتيب أو إعادة توجيه أو حشو الرسائل؟ إلى أي مدى يجب أن يتم هذا تلقائياً، وكم يجب تكوينه كإعداد لكل tunnel أو لكل hop، وكيف يجب على منشئ tunnel (وبدوره، المستخدم) التحكم في هذه العملية؟ كل هذا يبقى مجهولاً، ليتم حله في إصدار مستقبلي.
