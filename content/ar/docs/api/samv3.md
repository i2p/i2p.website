---
title: "SAMv3"
description: "بروتوكول المراسلة المجهولة البسيط للتطبيقات غير جافا في I2P"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM هو بروتوكول عميل بسيط للتفاعل مع I2P. يُعد SAM البروتوكول الموصى به للتطبيقات غير المكتوبة بلغة Java للاتصال بشبكة I2P، ويدعمه تنفيذ العديد من الراوترات. أما التطبيقات المكتوبة بلغة Java فيجب أن تستخدم واجهات برمجة التطبيقات للتدفق أو I2CP مباشرةً.

تم تقديم إصدار SAM 3 في إصدار I2P 0.7.3 (مايو 2009) وهو واجهة مستقرة ومدعومة. الإصدار 3.1 مستقر أيضًا ويدعم خيار نوع التوقيع، وهو ما يُوصى به بشدة. تدعم الإصدارات الأحدث من سلسلة 3.x ميزات متقدمة. يُلاحظ أن i2pd لا يدعم حاليًا معظم ميزات الإصدارين 3.2 و3.3.

بدائل: [SOCKS](/docs/api/socks)، [التدفق](/docs/api/streaming)، [I2CP](/docs/protocol/i2cp)، [BOB (مُهمل)](/docs/api/bob). الإصدارات المُهملة: [SAM V1](/docs/api/sam)، [SAM V2](/docs/api/samv2).

## مكتبات SAM المعروفة

تحذير: قد تكون بعض هذه العناصر قديمة جدًا أو غير مدعومة. لا يتم اختبار أي منها أو مراجعتها أو صيانتها من قبل مشروع I2P ما لم يُذكر خلاف ذلك أدناه. قم ببحثك الخاص.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## البدء السريع

لتنفيذ تطبيق أساسي نظيرًا إلى نظير عبر TCP فقط، يجب أن يدعم العميل الأوامر التالية:

- `HELLO VERSION MIN=3.1 MAX=3.1` - مطلوب لجميع الأوامر المتبقية
- `DEST GENERATE SIGNATURE_TYPE=7` - لتوليد المفتاح الخاص والوجهة (destination)
- `NAMING LOOKUP NAME=...` - لتحويل عناوين .i2p إلى وجهات
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - مطلوب من أجل أوامر STREAM CONNECT و STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - لإنشاء اتصالات صادرة
- `STREAM ACCEPT ID=...` - لقبول الاتصالات الواردة

## إرشادات عامة للمطورين

### تصميم التطبيق

تم تصميم جلسات SAM (أو داخل I2P، مجموعات الأنفاق أو مجموعات من الأنفاق) لتكون طويلة الأمد. معظم التطبيقات ستحتاج فقط إلى جلسة واحدة، تُنشأ عند بدء التشغيل وتُغلق عند الخروج. يختلف I2P عن Tor، حيث يمكن إنشاء الدوائر بسرعة والتخلص منها بسرعة. فكّر بعناية واستشر مطوري I2P قبل تصميم تطبيقك لاستخدام أكثر من جلستين متزامنتين، أو لإنشاء الجلسات والتخلص منها بسرعة. لن تتطلب معظم نماذج التهديد جلسة فريدة لكل اتصال.

كما يرجى التأكد من أن إعدادات تطبيقك (وإرشاداتك للمستخدمين حول إعدادات الراوتر، أو الإعدادات الافتراضية للراوتر إذا قمت بتضمين راوتر مع التطبيق) ستؤدي إلى مساهمة مستخدميك بموارد أكثر في الشبكة مما يستهلكونه. إن I2P هي شبكة نظير إلى نظير، ولا يمكن للشبكة أن تبقى حية إذا أدت تطبيقات شهيرة إلى ازدحام دائم فيها.

### التوافق والاختبار

تنفيذات موجهات Java I2P وi2pd مستقلة ولها اختلافات طفيفة في السلوك ودعم الميزات والإعدادات الافتراضية. يرجى اختبار تطبيقك بالإصدار الأحدث من كلا الموجهين.

يتم تمكين SAM في i2pd بشكل افتراضي؛ أما في Java I2P فهو غير ممكّن. قدم تعليمات للمستخدمين حول كيفية تمكين SAM في Java I2P (عبر /configclients في واجهة سطر أوامر الموجه)، و/أو قدم رسالة خطأ واضحة للمستخدم في حال فشل الاتصال الأولي، مثلاً: "تأكد من أن خدمة I2P تعمل وتم تمكين واجهة SAM".

لدى موجهات Java I2P وi2pd إعدادات افتراضية مختلفة لكميات النفق. الافتراضي في Java هو 2، والافتراضي في i2pd هو 5. بالنسبة لمعظم الاستخدامات ذات عرض النطاق المنخفض إلى المتوسط وعدد الاتصالات المنخفض إلى المتوسط، يكون 2 أو 3 كافيًا. يُرجى تحديد كمية النفق في رسالة SESSION CREATE للحصول على أداء متسق مع موجهات Java I2P وi2pd. انظر أدناه.

للمزيد من التوجيهات للمطورين حول التأكد من أن تطبيقك يستخدم فقط الموارد التي يحتاجها، يُرجى الاطلاع على [دليلنا لتضمين I2P مع تطبيقك](/docs/applications/embedding).

### أنواع التوقيع والتشفير

يدعم I2P أنواعًا متعددة من التوقيع والتشفير. من أجل التوافق مع الإصدارات السابقة، يعتمد SAM افتراضيًا على أنواع قديمة وغير فعّالة، لذا يجب على جميع العملاء تحديد أنواع أحدث.

يتم تحديد نوع التوقيع في أوامر DEST GENERATE وSESSION CREATE (للعابرة). يجب أن تقوم جميع العميلات بتعيين `SIGNATURE_TYPE=7` (Ed25519).

يتم تحديد نوع التشفير في أمر SESSION CREATE. يُسمح بأنواع تشفير متعددة. يجب على العميل تعيين `i2cp.leaseSetEncType=4` (لتشفير ECIES-X25519 فقط) أو `i2cp.leaseSetEncType=6,4` (لـ MLKEM-768 و ECIES-X25519، للراوترات التي تدعم API 0.9.67 أو أعلى).

## تغييرات الإصدار 3

### تغييرات الإصدار 3.0

تم تقديم الإصدار 3.0 في إصدار I2P 0.7.3. وفر SAM v2 طريقة لإدارة عدة مآخذ (sockets) على نفس وجهة I2P *بشكل متوازٍ*، أي أن العميل لا يحتاج إلى الانتظار حتى يتم إرسال البيانات بنجاح عبر مأخذ واحد قبل إرسال البيانات عبر مأخذ آخر. ولكن جميع البيانات كانت تمر عبر نفس مأخذ العميل إلى SAM، مما كان معقدًا إلى حد ما من حيث الإدارة بالنسبة للعميل.

يُدير SAM v3 المآخذ (sockets) بطريقة مختلفة: يتطابق كل *مأخذ I2P* مع مأخذ عميل-إلى-SAM فريد، مما يجعل التعامل معه أسهل بكثير. وهذا يشبه [BOB](/docs/api/bob).

يوفر SAM v3 أيضًا منفذ UDP لإرسال الرسائل من خلال I2P، ويمكنه إعادة توجيه رسائل I2P إلى خادم الرسائل الخاص بالعميل.

### تغييرات الإصدار 3.1

تم تقديم الإصدار 3.1 في إصدار Java I2P 0.9.14 (يوليو 2014). يُوصى بتطبيق SAM 3.1 كحد أدنى لأنه يدعم أنواع توقيع أفضل من SAM 3.0. كما يدعم i2pd معظم ميزات الإصدار 3.1.

- أصبح دعم معامل SIGNATURE_TYPE متاحًا الآن في DEST GENERATE وSESSION CREATE.
- أصبحت المعاملات MIN وMAX في HELLO VERSION اختيارية الآن.
- أصبحت المعاملات MIN وMAX في HELLO VERSION تدعم الإصدارات المكونة من رقم واحد مثل "3".
- أصبح RAW SEND مدعومًا الآن على منفذ الجسر (bridge socket).

### تغييرات الإصدار 3.2

تم إدخال الإصدار 3.2 في إصدار Java I2P 0.9.24 (يناير 2016). لاحظ أن i2pd لا يدعم حاليًا معظم ميزات الإصدار 3.2.

#### دعم منفذ وبروتوكول I2CP

- خيارات إنشاء الجلسة FROM_PORT و TO_PORT
- خيار SESSION CREATE STYLE=RAW وهو PROTOCOL
- خيارات FROM_PORT و TO_PORT في أوامر STREAM CONNECT و DATAGRAM SEND و RAW SEND
- خيار PROTOCOL في أمر RAW SEND
- حدث DATAGRAM RECEIVED و RAW RECEIVED والاتصالات أو الرسائل القابلة للرد التي يتم تمريرها أو استلامها، وتشمل FROM_PORT و TO_PORT
- الخيار HEADER=true في جلسة RAW سيؤدي إلى إضافة سطر في بداية الرسائل الخام المُعاد توجيهها يحتوي على: PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- يمكن الآن أن تبدأ السطر الأول من الرسائل المرسلة عبر المنفذ 7655 بأي إصدار 3.x
- يمكن أن يحتوي السطر الأول من الرسائل المرسلة عبر المنفذ 7655 على أي من الخيارات التالية: FROM_PORT، TO_PORT، PROTOCOL
- حدث RAW RECEIVED يتضمن PROTOCOL=nnn

#### SSL والمصادقة

- USER/PASSWORD في معلمات HELLO للمصادقة. انظر [أدناه](#authorization).
- تهيئة اختيارية للمصادقة باستخدام أمر AUTH. انظر [أدناه](#authorization-configuration-sam-32-or-higher-optional-feature).
- دعم اختياري لبروتوكول SSL/TLS على منفذ التحكم. انظر [أدناه](#ssl).
- خيار STREAM FORWARD مع SSL=true

#### التشغيل المتعدد للخيوط

- يُسمح بقبول عمليات STREAM المعلقة بشكل متزامن على نفس معرف الجلسة.

#### تحليل سطر الأوامر والحفاظ على الاتصال (Keepalive)

- أوامر اختيارية QUIT وSTOP وEXIT لإغلاق الجلسة والوصلة. انظر [أدناه](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- سيعالج تحليل الأوامر UTF-8 بشكل صحيح
- يعالج تحليل الأوامر المسافات البيضاء داخل علامات الاقتباس بشكل موثوق
- يمكن أن يستخدم الشرطة المائلة العكسية '\\' للهروب من علامات الاقتباس في سطر الأوامر
- يُوصى بأن يقوم الخادم بتعيين الأوامر إلى الأحرف الكبيرة، لتسهيل الاختبار عبر telnet.
- قد يُسمح بقيم خيارات فارغة مثل PROTOCOL أو PROTOCOL=، حسب التنفيذ.
- PING/PONG للحفاظ على الاتصال. انظر أدناه.
- قد يقوم الخوادم بتنفيذ مهلات زمنية لأمر HELLO أو الأوامر اللاحقة، حسب التنفيذ.

### تغييرات الإصدار 3.3

تم تقديم الإصدار 3.3 في إصدار Java I2P 0.9.25 (مارس 2016). لاحظ أن i2pd لا يدعم حاليًا معظم ميزات الإصدار 3.3.

- يمكن استخدام نفس الجلسة لكل من الدفق والرسائل المُجزأة والبيانات الخام في وقت واحد. سيتم توجيه الحُزم والدفق الواردة بناءً على بروتوكول I2P ومنفذ الوجهة (to-port). راجع [قسم الجلسات الأساسية (PRIMARY) أدناه](#sam-primary-sessions-v33-and-higher).
- أصبح من الممكن الآن أن تدعم أوامير DATAGRAM SEND وRAW SEND الخيارات التالية: SEND_TAGS، TAG_THRESHOLD، EXPIRES، وSEND_LEASESET. راجع [قسم إرسال الرسائل المُجزأة القابلة للرد أو الأولية (الخام) أدناه](#sending-repliable-or-raw-datagrams).

### تغييرات 2025-04

تمت الموافقة على مقترحين ودمجهما في المواصفات هنا في أبريل 2025. لا يوجد تغيير في الإصدار للإشارة إلى الدعم. بعض التنفيذات لا تدعمها بعد، وفي تنفيذات أخرى، يكون الدعم أوليًا.

- دعم داتاغرام 2/3 (الاقتراح 163). يُحدد في SESSION CREATE وSESSION ADD (الجلسات الفرعية). انظر أدناه.
- استرجاع خيارات leaseset (الاقتراح 167). يُحدد باستخدام NAMING LOOKUP OPTIONS=true. انظر أدناه.

## بروتوكول الإصدار 3

### نظرة عامة على مواصفات بروتوكول الرسائل المبسطة المجهولة (SAM) الإصدار 3.3

يتحدث تطبيق العميل إلى جسر SAM، الذي يتولى جميع وظائف I2P (باستخدام [مكتبة الدفق](/docs/api/streaming) للتدفقات الافتراضية، أو [I2CP](/docs/protocol/i2cp) مباشرة للرسائل الصغيرة).

بشكل افتراضي، تكون الاتصالات بين العميل وواجهة SAM غير مشفرة وغير موثقة. قد تدعم واجهة SAM اتصالات SSL/TLS؛ وتُعد تفاصيل التهيئة والتنفيذ خارج نطاق هذا المواصفة. بدءًا من SAM 3.2، يتم دعم معلمات اختيارية للمصادقة (اسم المستخدم/كلمة المرور) أثناء الاتصال الأولي، وقد تتطلبها واجهة SAM.

يمكن أن تتخذ اتصالات I2P عدة أشكال مميزة:

- [التدفقات الافتراضية](/docs/api/streaming)
- [وحدات البالتات القابلة للرد والموثّقة](/docs/specs/datagrams#repliable) (رسائل تحتوي على حقل FROM)
- [وحدات البالتات المجهولة](/docs/specs/datagrams#raw) (رسائل مجهولة المصدر مباشرة)
- [Datagram2](/docs/specs/datagrams#datagram2) (تنسيق جديد قابل للرد وموثّق)
- [Datagram3](/docs/specs/datagrams#datagram3) (تنسيق جديد قابل للرد ولكن غير موثّق)

تُدعم اتصالات I2P من خلال جلسات I2P، وكل جلسة I2P مرتبطة بعنوان (يُسمى وجهة). ترتبط جلسة I2P بإحدى الأنواع الثلاثة المذكورة أعلاه، ولا يمكنها نقل اتصالات من نوع آخر، ما لم تستخدم [جلسات أولية](#sam-primary-sessions-v33-and-higher).

### التشفير والهروب

يتم إرسال جميع رسائل SAM هذه في سطر واحد، وينتهي كل سطر بحرف السطر الجديد (\\n). قبل SAM 3.2، كان يُدعم فقط ASCII ذو 7 بت. بدءًا من SAM 3.2، يجب أن تكون الترميزات بـ UTF-8. ويجب أن تعمل أي مفاتيح أو قيم مُشفّرة باستخدام UTF-8.

التنسيق المعروض في هذا المواصفة أدناه مخصص فقط لسهولة القراءة، ومع أن الكلمتين الأوليين في كل رسالة يجب أن تبقيا بالترتيب المحدد، إلا أن ترتيب أزواج المفتاح=القيمة يمكن أن يتغير (مثلاً "ONE TWO A=B C=D" أو "ONE TWO C=D A=B" كلاهما تركيبان صحيحان تمامًا). بالإضافة إلى ذلك، البروتوكول حساس لحالة الأحرف (Case-sensitive). وفيما يلي، تسبق الأمثلة الخاصة بالرسائل علامة "->" للدلالة على الرسائل المرسلة من العميل إلى جسر SAM، وعلامة "<-" للدلالة على الرسائل المرسلة من جسر SAM إلى العميل.

تتخذ أمر أو استجابة السطر الأساسي إحدى الصيغ التالية:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
يُدعم الأمر COMMAND بدون SUBCOMMAND لبعض الأوامر الجديدة في SAM 3.2 فقط.

يجب فصل أزواج المفتاح=القيمة بواسطة مسافة واحدة فقط. (ابتداءً من SAM 3.2، يُسمح بوجود أكثر من مسافة) ويجب وضع القيم بين علامتي اقتباس مزدوجتين إذا كانت تحتوي على مسافات، على سبيل المثال: key="long value text". (قبل SAM 3.2، لم يكن هذا يعمل بشكل موثوق في بعض التطبيقات)

قبل SAM 3.2، لم تكن هناك آلية للهروب (escaping). بدءًا من SAM 3.2، يمكن استخدام الشرطة المائلة العكسية '\\' لجعل علامات الاقتباس المزدوجة غير فعّالة (escape)، ويمكن تمثيل الشرطة المائلة العكسية نفسها باستخدام شرطتين مائلتين عكسيتين '\\\\'.

### القيم الفارغة

اعتبارًا من SAM 3.2، قد تُسمح القيم الفارغة للخيارات مثل KEY أو KEY= أو KEY=""، ويعتمد ذلك على التنفيذ.

### حساسية الحالة

البروتوكول كما هو مُحدد، حساس لحالة الأحرف (case-sensitive). يُوصى، رغم أنه ليس إلزاميًا، أن يقوم الخادم بتحويل الأوامر إلى أحرف كبيرة (upper case) لتسهيل الاختبار عبر برنامج telnet. هذا يسمح، على سبيل المثال، باستخدام "hello version". يعتمد هذا السلوك على التنفيذ. لا تقم بتحويل المفاتيح (keys) أو القيم (values) إلى أحرف كبيرة، لأن ذلك قد يتسبب في إتلاف خيارات [I2CP](/docs/protocol/i2cp).

### التصافح اليدوي لاتصال SAM

لا يمكن أن تحدث أي اتصالات SAM حتى يتفق العميل والجسر على إصدار البروتوكول، ويتم ذلك بإرسال العميل لرسالة HELLO وإرسال الجسر لرسالة HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
و

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
اعتبارًا من الإصدار 3.1 (I2P 0.9.14)، أصبحت المعلمتان MIN و MAX اختياريتين. سيقوم SAM دائمًا بإرجاع أعلى إصدار ممكن وفقًا لقيود MIN و MAX، أو إصدار الخادم الحالي إذا لم تُعطَ أي قيود.

إذا لم يستطع جسر SAM العثور على إصدار مناسب، فإنه يرد بـ:

```
<- HELLO REPLY RESULT=NOVERSION
```
إذا حدث خطأ ما، مثل تنسيق طلب غير صحيح، فإنه يرد بـ:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

قد تقدم مقبس التحكم في الخادم دعمًا اختياريًا لـ SSL/TLS، حسب التكوين الموجود على الخادم والعميل. قد تقدم التطبيقات طبقات نقل أخرى أيضًا؛ هذا الأمر يقع خارج نطاق تعريف البروتوكول.

#### المصادقة

لإتمام عملية المصادقة، يجب على العميل إضافة USER="xxx" PASSWORD="yyy" إلى معلمات HELLO. يُوصى باستخدام علامتي اقتباس حول اسم المستخدم وكلمة المرور، لكنهما غير مطلوبتين. يجب الهروب من علامة الاقتباس المزدوجة داخل اسم المستخدم أو كلمة المرور باستخدام خط مائل عكسي (\). في حال الفشل، سيقوم الخادم بالرد بـ I2P_ERROR مع رسالة توضيحية. ويُوصى بتمكين SSL على أي خوادم SAM تتطلب مصادقة.

#### مهلة انتهاء الوقت

قد تقوم الخوادم بتنفيذ مهلات زمنية للإمر HELLO أو للأوامر اللاحقة، ويعتمد ذلك على التنفيذ. يجب على العملاء إرسال الأمر HELLO والأمر التالي مباشرةً بعد الاتصال.

إذا حدثت مهلة قبل استلام HELLO، يرد الجسر بـ:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
ثم ينقطع الاتصال.

إذا حدثت مهلة بعد استلام HELLO ولكن قبل الأمر التالي، يرد الجسر بـ:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
ثم ينقطع الاتصال.

### منافذ وبروتوكول I2CP

اعتبارًا من SAM 3.2، يمكن للمُرسِل العميل لـ SAM تحديد منافذ وبروتوكول [I2CP](/docs/protocol/i2cp) لتمريرها إلى [I2CP](/docs/protocol/i2cp)، وسوف يقوم جسر SAM بتمرير معلومات منفذ وبروتوكول [I2CP](/docs/protocol/i2cp) المستلمة إلى العميل SAM.

بالنسبة لـ FROM_PORT و TO_PORT، يكون النطاق الصحيح بين 0 و65535، والقيمة الافتراضية هي 0.

بالنسبة إلى البروتوكول (PROTOCOL)، الذي يمكن تحديده فقط للوضع RAW، يكون النطاق الصحيح بين 0 و255، والقيمة الافتراضية هي 18.

بالنسبة لأوامر SESSION، فإن المنافذ والبروتوكول المحددين يعتبران الإعدادات الافتراضية لهذه الجلسة. أما بالنسبة للتيارات أو الحزم الفردية، فإن المنافذ والبروتوكول المحددين يُطغون على الإعدادات الافتراضية للجلسة. وبالنسبة للتيارات أو الحزم المستلمة، فإن المنافذ والبروتوكول المُشار إليها تكون كما تم استلامها عبر [I2CP](/docs/protocol/i2cp).

#### الاختلافات المهمة عن بروتوكول الإنترنت القياسي

منافذ I2CP مخصصة لمقابس I2P وحزم البيانات (datagrams). وهي غير مرتبطة بمقابسك المحلية التي تتصل بـ SAM.

- المنفذ 0 صالح ويحمل معنى خاصًا.
- المنافذ 1-1023 ليست خاصة أو مُمتَيزة.
- تستمع الخوادم افتراضيًا إلى المنفذ 0، مما يعني "جميع المنافذ".
- ترسل العميلات افتراضيًا إلى المنفذ 0، مما يعني "أي منفذ".
- ترسل العميلات افتراضيًا من المنفذ 0، مما يعني "غير محدد".
- قد تحتوي الخوادم على خدمة تستمع إلى المنفذ 0 وخدمات أخرى تستمع إلى منافذ أعلى. في هذه الحالة تكون خدمة المنفذ 0 هي الافتراضية، وسيتم الاتصال بها إذا لم يتطابق منفذ المقبس أو الداتاغرام الوارد مع خدمة أخرى.
- معظم وجهات I2P تحتوي فقط على خدمة واحدة قيد التشغيل، لذا يمكنك استخدام الإعدادات الافتراضية وتجاهل تهيئة منافذ I2CP.
- يتطلب تحديد منافذ I2CP استخدام SAM 3.2 أو 3.3.
- إذا كنت لا تحتاج إلى منافذ I2CP، فلن تحتاج إلى SAM 3.2 أو 3.3؛ حيث يكون SAM 3.1 كافيًا.
- البروتوكول 0 صالح ويعني "أي بروتوكول". لا يُنصح باستخدامه، ومن المرجح ألا يعمل.
- يتم تتبع مقابس I2P عبر معرّف اتصال داخلي. لذلك، ليس هناك حاجة إلى أن يكون الخماسي (dest:port:dest:port:protocol) فريدًا. على سبيل المثال، قد توجد مقابس متعددة بنفس المنافذ بين وجهتين. ولا يحتاج العميل إلى اختيار "منفذ حر" للاتصال الصادر.

إذا كنت تقوم بتصميم تطبيق SAM 3.3 يحتوي على جلسات فرعية متعددة، فكر جيدًا في كيفية استخدام المنافذ والبروتوكولات بشكل فعّال. راجع مواصفات [I2CP](/docs/protocol/i2cp) للحصول على مزيد من المعلومات.

### جلسات SAM

يتم إنشاء جلسة SAM من خلال عميل يقوم بفتح مقبس (socket) إلى جسر SAM، وتنفيذ عملية تبادل تحية (handshake)، وإرسال رسالة SESSION CREATE، وينتهي الجلسة عندما يتم فصل المقبس.

يتم ربط كل وجهة I2P مسجلة بشكل فريد بمعرف جلسة (أو لقب). يجب أن تكون معرفات الجلسات، بما في ذلك معرفات الجلسات الفرعية للجلسات الأساسية (PRIMARY)، فريدة عالميًا على خادم SAM. ولمنع التصادم المحتمل للمعرفات مع العملاء الآخرين، فإن الممارسة الأفضل هي أن يقوم العميل بتوليد المعرفات عشوائيًا.

يتم ربط كل جلسة بشكل فريد مع:

- المقبس الذي يُنشئ العميل من خلاله الجلسة
- المعرف الخاص به (أو الاسم المستعار)

#### طلب إنشاء جلسة

يمكن لرسالة إنشاء الجلسة استخدام إحدى هذه الأشكال فقط (تتم مجابهة الرسائل المستلمة من خلال أشكال أخرى برسالة خطأ):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
تحدد الـ DESTINATION الوجهة التي يجب استخدامها لإرسال واستقبال الرسائل/التيارات. إن $privkey هو الشكل المشفّر بقاعدة 64 لسلسلة متتالية تتكون من [الوجهة] (/docs/specs/common-structures#type_Destination)، متبوعةً بـ [المفتاح الخاص] (/docs/specs/common-structures#type_PrivateKey)، ثم بـ [مفتاح التوقيع الخاص] (/docs/specs/common-structures#type_SigningPrivateKey)، ويمكن اختيارياً إضافة [توقيع غير متصل] (/docs/specs/common-structures#struct_OfflineSignature)، والذي يبلغ طوله 663 بايت أو أكثر بصيغته الثنائية، أو 884 بايت أو أكثر عند تشفيره بقاعدة 64، وذلك حسب نوع التوقيع. ويُحدد التنسيق الثنائي في ملف المفتاح الخاص. انظر الملاحظات الإضافية حول [المفتاح الخاص] (/docs/specs/common-structures#type_PrivateKey) في قسم توليد مفتاح الوجهة أدناه.

إذا كانت المفتاح الخاص للتوقيع عبارة عن أصفار فقط، يتبع قسم [التوقيع غير المتصل](/docs/specs/common-structures#struct_OfflineSignature). تُدعم التواقيع غير المتصلة فقط للجلسات من نوع STREAM وRAW. لا يمكن إنشاء التواقيع غير المتصلة باستخدام DESTINATION=TRANSIENT. يكون تنسيق قسم التوقيع غير المتصل كما يلي:

1. طابع انتهاء الصلاحية (4 بايت، بترتيب بايت كبير، الثواني منذ العصر، يُعاد التدوير في عام 2106)
2. نوع التوقيع للمفتاح العمومي المؤقت للتوقيع (2 بايت، بترتيب بايت كبير)
3. المفتاح العمومي المؤقت للتوقيع (الطول حسب ما يحدده نوع التوقيع المؤقت)
4. توقيع الحقول الثلاثة أعلاه بواسطة المفتاح غير المتصل (الطول حسب ما يحدده نوع توقيع الوجهة)
5. المفتاح الخاص المؤقت للتوقيع (الطول حسب ما يحدده نوع التوقيع المؤقت)

إذا تم تحديد الوجهة على أنها TRANSIENT، فإن جسر SAM يقوم بإنشاء وجهة جديدة. بدءًا من الإصدار 3.1 (I2P 0.9.14)، إذا كانت الوجهة هي TRANSIENT، يُدعم المعلمة الاختيارية SIGNATURE_TYPE. يمكن أن تكون قيمة SIGNATURE_TYPE أي اسم (مثل ECDSA_SHA256_P256، دون مراعاة حالة الأحرف) أو رقم (مثل 1) مدعوم من قبل [شهادات المفاتيح](/docs/specs/common-structures#type_Certificate). القيمة الافتراضية هي DSA_SHA1، وهي ليست ما تريده. بالنسبة لمعظم التطبيقات، يُرجى تحديد SIGNATURE_TYPE=7.

$nickname هو اختيار العميل. لا يسمح باستخدام المسافات البيضاء.

تُمرر الخيارات الإضافية المُعطاة إلى تهيئة جلسة I2P إذا لم يتم تفسيرها بواسطة جسر SAM (مثل: outbound.length=0).

يختلف برنامج التوجيه Java I2P عن i2pd في القيم الافتراضية لكمية الأنفاق. فالقيمة الافتراضية في Java هي 2، بينما في i2pd هي 5. بالنسبة لمعظم الاستخدامات ذات النطاق الترددي المنخفض إلى المتوسط وعدد الاتصالات المنخفض إلى المتوسط، تكون كمية 2 أو 3 كافية. يُرجى تحديد كميات الأنفاق في رسالة SESSION CREATE للحصول على أداء متسق مع برنامجي التوجيه Java I2P وi2pd، وذلك باستخدام خيارات مثل: inbound.quantity=3 outbound.quantity=3. تُوثَّق هذه الخيارات وغيرها في الروابط أدناه](#tunnel-i2cp-and-streaming-options).

يجب أن يكون جسر SAM نفسه قد تم تهيئته مسبقًا بالراوتر الذي ينبغي أن يتواصل من خلاله عبر I2P (على الرغم من أنه إذا لزم الأمر قد توجد طريقة لتوفير قيمة بديلة، مثل i2cp.tcp.host=localhost و i2cp.tcp.port=7654).

#### استجابة إنشاء الجلسة

بعد استلام رسالة إنشاء الجلسة، سيقوم جسر SAM بالرد برسالة حالة الجلسة، كما يلي:

إذا نجحت العملية:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
الـ $privkey هو تمثيل base 64 للتسلسل الذي يتكون من [الوجهة] (/docs/specs/common-structures#type_Destination) متبوعة بـ [المفتاح الخاص] (/docs/specs/common-structures#type_PrivateKey) ثم بـ [مفتاح التوقيع الخاص] (/docs/specs/common-structures#type_SigningPrivateKey)، مع إمكانية إضافة اختيارية لـ [التوقيع غير المتصل] (/docs/specs/common-structures#struct_OfflineSignature)، والذي يبلغ طوله 663 بايت أو أكثر بصيغته الثنائية، و884 بايت أو أكثر عند تمثيله بـ base 64، وذلك حسب نوع التوقيع. ويُحدد التنسيق الثنائي في وثيقة ملف المفتاح الخاص.

إذا احتوى SESSION CREATE على مفتاح خاص للتوقيع يتكون من أصفار فقط وقسم [توقيع غير متصل](/docs/specs/common-structures#struct_OfflineSignature)، فستتضمن ردية SESSION STATUS نفس البيانات بنفس التنسيق. انظر قسم SESSION CREATE أعلاه للتفاصيل.

إذا كان الاسم المستعار مرتبطًا بالفعل بجلسة:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
إذا كان الوجهة قيد الاستخدام بالفعل:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
إذا لم تكن الوجهة مفتاح وجهة خاصًا صالحًا:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
إذا حدث خطأ آخر:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
إذا لم تكن الحالة "موافق"، فيجب أن يحتوي الرسالة (MESSAGE) على معلومات يمكن قراءتها من قبل الإنسان توضح السبب وراء عدم إمكانية إنشاء الجلسة.

لاحظ أن الموجه يقوم ببناء النفق قبل الرد بحالة الجلسة. قد يستغرق هذا عدة ثوانٍ، أو دقيقة أو أكثر عند بدء تشغيل الموجه أو أثناء ازدحام الشبكة الشديد. إذا لم ينجح الأمر، فلن يرد الموجه برسالة فشل لعدة دقائق. لا تضبط مهلة قصيرة تنتظر فيها الرد. ولا تتخلى عن الجلسة أثناء بناء النفق جارٍ، ولا تحاول المحاولة مرة أخرى.

تستمر جلسات SAM في العمل طالما أن المقبس (socket) المرتبط بها مفتوح، وتموت عندما يُغلق هذا المقبس. وعندما يُغلق المقبس، تنتهي الجلسة، وتتوقف جميع الاتصالات التي تستخدم هذه الجلسة في اللحظة نفسها. وبالعكس أيضًا، عندما تنتهي جلسة SAM لأي سبب كان، يقوم جسر SAM بإغلاق المقبس المرتبط بها.

### التدفقات الافتراضية SAM

يتم ضمان إرسال الدفق الافتراضي بشكل موثوق ومرتب، مع إشعار الفشل أو النجاح فور توفره.

الـ Streams هي مقابس اتصال ثنائية الاتجاه بين وجهتين في شبكة I2P، ولكن يجب أن تتم طلبية فتحها من إحدى الطرفين. ومن الآن فصاعدًا، تُستخدم أوامر CONNECT من قِبل عميل SAM لتقديم هذا الطلب. وتُستخدم أوامر FORWARD / ACCEPT من قِبل عميل SAM عندما يرغب في الاستماع للطلبات الواردة من جهات أخرى في شبكة I2P.

### تدفقات SAM الظاهرية: CONNECT

يطلب العميل الاتصال من خلال:

- فتح مقبس جديد مع جسر SAM
- إرسال نفس تبادل التحية HELLO كما في الأعلى
- إرسال أمر STREAM CONNECT

#### طلب اتصال

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
يُنشئ هذا اتصالًا افتراضيًا جديدًا من الجلسة المحلية التي يكون معرّفها هو $nickname إلى الند المحدد.

الوجهة هي $destination، وهي تمثيل بصيغة base 64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، وتحتوي على 516 حرفًا على الأقل في ترميز base 64 (أو ما يعادل 387 بايت أو أكثر بصيغتها الثنائية)، وذلك حسب نوع التوقيع.

**ملاحظة:** منذ حوالي عام 2014 (SAM v3.1)، بدأ Java I2P أيضًا بدعم أسماء المضيف والعناوين b32 لـ $destination، ولكن هذا لم يكن موثقًا سابقًا. أصبح دعم أسماء المضيف والعناوين b32 رسميًا في Java I2P بدءًا من الإصدار 0.9.48. يدعم موجه i2pd أسماء المضيف والعناوين b32 بدءًا من الإصدار 2.38.0 (0.9.50). بالنسبة لكلا الموجهين، يشمل الدعم "b32" دعم العناوين "b33" الموسعة للوجهات المموهة.

#### استجابة الاتصال

إذا تم تمرير SILENT=true، فلن يُصدر جسر SAM أي رسالة أخرى عبر المقبس. إذا فشل الاتصال، فسيتم إغلاق المقبس. وإذا نجح الاتصال، فسيتم توجيه جميع البيانات المتبقية التي تمر عبر المقبس الحالي من وإلى نظير الوجهة في I2P الذي تم الاتصال به.

إذا كانت SILENT=false، وهي القيمة الافتراضية، فإن جسر SAM يُرسل رسالة أخيرة إلى عميله قبل توجيه المقبس أو إيقافه:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
قد تكون قيمة RESULT إحدى القيم التالية:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
إذا كانت النتيجة OK، يتم توجيه جميع البيانات المتبقية التي تمر عبر المقبس الحالي من وإلى نظير I2P الوجهة المتصل. وإذا تعذر إنشاء الاتصال (انتهاء المهلة، إلخ)، فستحتوي النتيجة على القيمة الخطأ المناسبة (مقرونة برسالة اختيارية يمكن قراءتها بواسطة الإنسان)، ويقوم جسر SAM بإغلاق المقبس.

مدة انتظار اتصال الدفق في الموجه داخليًا تقارب دقيقة واحدة، وتعتمد على التنفيذ. لا تقم بتعيين مهلة أقصر أثناء الانتظار للرد.

### تدفقات SAM الافتراضية: قبول

يُنتظر العميل طلب اتصال وارد من خلال:

- فتح منفذ جديد مع جسر SAM
- إرسال نفس تبادل التحية HELLO كما هو موضح أعلاه
- إرسال أمر STREAM ACCEPT

#### قبول الطلب

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
هذا يجعل الجلسة ${nickname} تستمع لطلب اتصال وارد واحد من شبكة I2P. لا يُسمح باستخدام ACCEPT بينما يوجد اتصال من نوع FORWARD نشط على الجلسة.

اعتبارًا من SAM 3.2، يُسمح بتنفيذ عمليات قبول STREAM متعددة متزامنة (قيد الانتظار) على نفس معرف الجلسة (حتى مع نفس المنفذ). قبل الإصدار 3.2، كانت عمليات القبول المتزامنة تفشل مع خطأ ALREADY_ACCEPTING. ملاحظة: يدعم Java I2P أيضًا عمليات القبول المتزامنة على SAM 3.1، بدءًا من الإصدار 0.9.24 (2016-01). كما يدعم i2pd عمليات القبول المتزامنة على SAM 3.1، بدءًا من الإصدار 2.50.0 (2023-12).

#### قبول الاستجابة

إذا تم تمرير SILENT=true، فلن يقوم جسر SAM بإرسال أي رسالة أخرى عبر المقبس. إذا فشل القبول، سيتم إغلاق المقبس. وإذا نجح القبول، فإن جميع البيانات المتبقية التي تمر عبر المقبس الحالي سيتم توجيهها من وإلى نظير I2P الوجهة المتصل به. من أجل الموثوقية، وللحصول على الوجهة الخاصة بالاتصالات الواردة، يُوصى باستخدام SILENT=false.

إذا كانت SILENT=false، وهي القيمة الافتراضية، فإن جسر SAM يستجيب بـ:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
قد تكون قيمة RESULT إحدى القيم التالية:

```
OK
I2P_ERROR
INVALID_ID
```
إذا كانت النتيجة ليست "ناجحة"، يتم إغلاق المقبس فورًا بواسطة جسر SAM. وإذا كانت النتيجة "ناجحة"، يبدأ جسر SAM في الانتظار لطلب اتصال وارد من نظير I2P آخر. وعندما يصل الطلب، يقبله جسر SAM و:

إذا تم تمرير SILENT=true، فلن يقوم جسر SAM بإرسال أي رسالة أخرى عبر مقبس العميل. سيتم توجيه جميع البيانات المتبقية التي تمر عبر المقبس الحالي من وإلى نظير I2P الوجهة المتصل.

إذا تم تمرير SILENT=false، وهي القيمة الافتراضية، يُرسل جسر SAM للعميل سطرًا نصيًا بتنسيق ASCII يحتوي على مفتاح الوجهة العام base64 للنقطة المُطلِبة، بالإضافة إلى معلومات إضافية خاصة بـ SAM 3.2 فقط:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
بعد هذا السطر المنتهي بـ '\\n'، يتم توجيه جميع البيانات المتبقية التي تمر عبر المقبس الحالي من وإلى نظير I2P المتصل، حتى يقوم أحد الطرفين بإغلاق المقبس.

#### أخطاء بعد النجاح

في حالات نادرة، قد تواجه جسر SAM خطأً بعد إرسال RESULT=OK، ولكن قبل استقبال اتصال وإرسال سطر $destination إلى العميل. قد تشمل هذه الأخطاء إيقاف تشغيل الموجه، إعادة تشغيل الموجه، أو إغلاق الجلسة. في هذه الحالات، عندما تكون SILENT=false، قد يُرسل جسر SAM السطر التالي، ولكن ليس مطلوبًا (يعتمد على التنفيذ):

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
قبل إغلاق المقبس مباشرة. بالطبع، لا يمكن فك تشفير هذا السطر كوجهة صالحة بتنسيق Base 64.

### تدفقات SAM الافتراضية: توجيه (FORWARD)

يمكن للعميل استخدام خادم مقبس عادي والانتظار لطلبات الاتصال القادمة من I2P. ولذلك، يجب على العميل:

- افتح مقبس جديد مع جسر SAM
- أرسل تبادل التحية (HELLO handshake) نفسه كما في الأعلى
- أرسل أمر التوجيه (forward command)

#### طلب توجيه

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
هذا يجعل الجلسة ${nickname} تستمع لطلبات الاتصال الواردة من شبكة I2P. لا يُسمح بالتحويل (FORWARD) بينما توجد عملية قبول معلقة (PENDING ACCEPT) على الجلسة.

#### استجابة توجيهية

يتم تعيين SILENT افتراضيًا على false. بغض النظر عما إذا كانت SILENT صحيحة أم خاطئة، فإن جسر SAM يرد دائمًا برسالة STREAM STATUS. لاحظ أن هذا سلوك مختلف عن STREAM ACCEPT و STREAM CONNECT عندما تكون SILENT=true. رسالة STREAM STATUS هي:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
قد تكون قيمة RESULT إحدى القيم التالية:

```
OK
I2P_ERROR
INVALID_ID
```
$host هو اسم المضيف أو عنوان IP لخادم المقبس الذي سيرسل إليه SAM طلبات الاتصال. إذا لم يُذكر، فإن SAM يستخدم عنوان IP للمقبس الذي أصدر أمر التوجيه.

$port هو رقم المنفذ الخاص بخادم المقبس الذي سترسل SAM طلبات الاتصال إليه. وهو إلزامي.

عندما يصل طلب اتصال من I2P، يقوم جسر SAM بفتح اتصال مأخذ تواصل (socket) إلى $host:$port. إذا تم قبول الاتصال في أقل من 3 ثوانٍ، فسيقوم SAM بقبول الاتصال من I2P، ثم:

إذا تم تمرير SILENT=true، يتم توجيه جميع البيانات التي تمر عبر المقبس الحالي من وإلى نظير I2P الوجهة المتصل.

إذا تم تمرير SILENT=false، وهي القيمة الافتراضية، فإن جسر SAM يُرسل عبر المقبس الذي تم الحصول عليه سطرًا بصيغة ASCII يحتوي على مفتاح العنوان العام بترميز base64 للنقطة الطرفية الطالبة، بالإضافة إلى معلومات إضافية خاصة بـ SAM 3.2 فقط:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
بعد هذا السطر المنتهي بـ '\\n'، يتم توجيه جميع البيانات المتبقية التي تمر عبر المقبس من وإلى نظير I2P الوجهة المتصل به، حتى يغلق أحد الطرفين المقبس.

اعتبارًا من SAM 3.2، إذا تم تحديد SSL=true، فإن منفذ التوجيه يعمل عبر SSL/TLS.

سيتوقف جهاز توجيه I2P عن الاستماع لطلبات الاتصال الواردة بمجرد إغلاق منفذ "التوجيه".

### حزم SAM

يوفر SAMv3 آليات لإرسال واستقبال الداتاغرامات عبر مآخذ الداتاغرام المحلية. كما تدعم بعض تطبيقات SAMv3 أيضًا الطريقة الأقدم v1/v2 لإرسال واستقبال الداتاغرامات عبر مأخذ جسر SAM. وكلا الطريقتين موثقتان أدناه.

يدعم I2P أربعة أنواع من الداتاغرام:

- تبدأ حزم البيانات القابلة للإجابة والمُوثَّقة بوجهة المرسل، وتحتوي على توقيع المرسل، بحيث يمكن للمستلم التحقق من أن وجهة المرسل لم يتم التلاعب بها، ويمكنه الرد على حزمة البيانات. يُعد تنسيق حزمة البيانات الجديد Datagram2 أيضًا قابلاً للإجابة ومُوثَّقًا.
- تنسيق حزمة البيانات الجديد Datagram3 قابل للإجابة ولكن غير موثَّق. معلومات المرسل غير مُحقَّقة.
- لا تحتوي حزم البيانات الخام (Raw datagrams) على وجهة المرسل أو توقيع.

تُعرّف منافذ I2CP الافتراضية لكل من الرسائل المشفرة ذات الرد والرسائل المشفرة الخام. يمكن تغيير منفذ I2CP للرسائل المشفرة الخام.

نمط تصميم البروتوكول الشائع هو إرسال حُزم بيانات قابلة للرد إلى الخوادم، مع تضمين معرف معين، ثم يقوم الخادم بالرد باستخدام حزمة بيانات خام تتضمن هذا المعرف، بحيث يمكن ربط الرد بالطلب. يلغي هذا النمط التصميمي التكاليف الإضافية الكبيرة الناتجة عن استخدام حزم البيانات القابلة للرد في الردود. جميع خيارات بروتوكولات ومنافذ I2CP تعتمد على التطبيق، وينبغي على المصممين أخذ هذه المسائل في الاعتبار.

انظر أيضًا الملاحظات المهمة حول MTU الداتاغرام في القسم أدناه.

#### إرسال حُزم بيانات قابلة لإعادة الإرسال أو أولية

على الرغم من أن I2P لا يحتوي بشكل جوهري على عنوان FROM، فإنه يتم توفير طبقة إضافية لتسهيل الاستخدام على شكل داتاغرامات قابلة للرد (repliable datagrams) - وهي رسائل غير مرتبة وغير موثوقة بحجم يصل إلى 31744 بايت وتشمل عنوان FROM (مع ترك ما يصل إلى 1 كيلوبايت للمادة الرأسية). ويتم التحقق من صحة عنوان FROM داخليًا بواسطة SAM (باستخدام مفتاح التوقيع للوجهة للتحقق من المصدر)، ويشمل ذلك منع إعادة الإرسال (replay prevention).

الحجم الأدنى هو 1. ولأفضل موثوقية في التسليم، يُوصى بأن يكون الحجم الأقصى حوالي 11 كيلوبايت. تتناسب الموثوقية عكسياً مع حجم الرسالة، وربما بشكل أسيّ.

بعد إنشاء جلسة SAM مع STYLE=DATAGRAM أو STYLE=RAW، يمكن للعميل إرسال حزم بيانات قابلة للإجابة أو حزم بيانات خام من خلال منفذ UDP الخاص بـ SAM (7655 افتراضيًا).

يجب أن تكون أول سطر في الداتاغرام المرسل عبر هذا المنفذ بالتنسيق التالي. هذا كله في سطر واحد (مفصولة بمسافات)، ويظهر في أسطر متعددة للتوضيح:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 هو إصدار SAM. ابتداءً من SAM 3.2، يُسمح باستخدام أي إصدار من سلسلة 3.x.
- $nickname هو معرّف جلسة DATAGRAM التي سيتم استخدامها.
- الوجهة هي $destination، وهي التنسيق القاعدة-64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، ويتكون من 516 حرفًا قاعدة-64 على الأقل (أو 387 بايت على الأقل بصيغتها الثنائية)، ويختلف الطول حسب نوع التوقيع. **ملاحظة:** منذ حوالي عام 2014 (SAM v3.1)، بدأ Java I2P بدعم أسماء المضيف (hostnames) والعناوين b32 كمُدخل للقيمة $destination، ولكن لم تُوثَّق هذه الميزة سابقًا. أصبح دعم أسماء المضيف والعناوين b32 رسميًا في Java I2P بدءًا من الإصدار 0.9.48. لا يدعم موجه i2pd حاليًا أسماء المضيف والعناوين b32؛ وقد تُضاف هذه الميزة في إصدار مستقبلي.
- جميع الخيارات هي إعدادات على مستوى كل داتاغرام وتأخذ الأسبقية على الإعدادات الافتراضية المحددة في الجملة SESSION CREATE.
- يتم تمرير خيارات الإصدار 3.3 SEND_TAGS وTAG_THRESHOLD وEXPIRES وSEND_LEASESET إلى بروتوكول [I2CP](/docs/protocol/i2cp) إذا كان مدعومًا. انظر [مواصفات بروتوكول I2CP](/docs/protocol/i2cp#msg_SendMessageExpire) للحصول على التفاصيل. يكون دعم الخادم SAM لهذه الخيارات اختياريًا، ويتجاهل الخادم هذه الخيارات إذا لم تكن مدعومة.
- تنتهي هذه السطر بـ '\\n'.

سيتم تجاهل السطر الأول من قِبل SAM قبل إرسال البيانات المتبقية من الرسالة إلى الوجهة المحددة.

للاطلاع على طريقة بديلة لإرسال الرسائل المشفرة ذات الإمكانية الردّية والرسائل الأولية (datagrams)، راجع [DATAGRAM SEND و RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### حزم SAM القابلة للإعادة: استلام حزمة

يتم كتابة البيانات المستلمة بواسطة SAM على المقبس الذي تم فتح جلسة البيانات من خلاله، إذا لم يتم تحديد منفذ إعادة توجيه في أمر SESSION CREATE. هذه هي الطريقة المتوافقة مع الإصدار v1/v2 لاستقبال الحزم البيانات.

عندما يصل حزمة بيانات، يقوم الجسر بتسليمها إلى العميل عبر الرسالة:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
المصدر هو $destination، وهو تمثيل بصيغة base 64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، ويتكون من 516 حرفًا أو أكثر بصيغة base 64 (أو 387 بايت أو أكثر بصيغتها الثنائية)، ويعتمد العدد على نوع التوقيع.

لا يُعرِّض جسر SAM للعميل أبدًا رؤوس المصادقة أو الحقول الأخرى، بل فقط البيانات التي قدّمها المرسل. ويستمر هذا حتى يتم إغلاق الجلسة (بإسقاط العميل للاتصال).

#### توجيه حزم البيانات الأولية أو القابلة للإجابة

عند إنشاء جلسة داتاغرام، يمكن للعميل أن يطلب من SAM توجيه الرسائل الواردة إلى عنوان ip:port محدد. ويقوم بذلك بإصدار أمر CREATE مع خيارات PORT وHOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
الـ $privkey هو تمثيل base 64 للتسلسل الذي يحتوي على [الوجهة] (/docs/specs/common-structures#type_Destination) متبوعة بـ [المفتاح الخاص] (/docs/specs/common-structures#type_PrivateKey) ثم بـ [مفتاح التوقيع الخاص] (/docs/specs/common-structures#type_SigningPrivateKey)، مع إمكانية إضافة اختيارية لـ [التوقيع غير المتصل] (/docs/specs/common-structures#struct_OfflineSignature)، ويتكوّن هذا الناتج من 884 حرفًا على الأقل في ترميز base 64 (أو 663 بايت على الأقل بصيغته الثنائية)، ويعتمد الطول على نوع التوقيع. ويُحدد التنسيق الثنائي في وثيقة ملف المفتاح الخاص.

تُدعم التوقيعات غير المتصلة للرسائل RAW وDATAGRAM2 وDATAGRAM3، ولكن لا تُدعم لـ DATAGRAM. راجع قسم إنشاء الجلسة أعلاه وقسم DATAGRAM2/3 أدناه للتفاصيل.

$host هو اسم المضيف أو عنوان IP للخادم الذي يستقبل الداتاغرامات والذي سيحول SAM الداتاغرامات إليه. إذا لم يتم تحديده، فإن SAM يستخدم عنوان IP الخاص بالمساحة (socket) التي أصدرت أمر التوجيه.

$port هو رقم المنفذ الخاص بخادم الداتاغرام الذي سيحول SAM إليه الداتاغرامات. إذا لم يتم تعيين $port، فلن يتم توجيه الداتاغرامات، بل سيتم استقبالها على مقبس التحكم بطريقة متوافقة مع الإصدار v1/v2.

تُمرَّر الخيارات الإضافية المُعطاة إلى تهيئة جلسة I2P إذا لم يتم تفسيرها بواسطة جسر SAM (مثلاً: outbound.length=0). تُوثَّق هذه الخيارات [أدناه](#tunnel-i2cp-and-streaming-options).

تُسبَق حزم الباتاجرام القابلة للإعادة التي تُنقَل دائمًا بالوجهة المشفرة بـ base64، باستثناء Datagram3، انظر أدناه. وعند وصول باتاجرام قابل للإعادة، يُرسِل الجسر إلى المضيف:المنفذ المحدد حزمة UDP تحتوي على البيانات التالية:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
تُحوَّل حُزم البيانات الأولية (datagrams) المُعاد توجيهها كما هي إلى المضيف:المنفذ المحدد دون بادئة. تحتوي حزمة UDP على البيانات التالية:

```
$datagram_payload
```
اعتبارًا من SAM 3.2، عندما يتم تحديد HEADER=true في SESSION CREATE، سيتم إضافة سطر ترويسة قبل حزمة الداتاكرام الأولية المحولة على النحو التالي:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$الوجهة هي التنميط الأساس-64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، والذي يتكون من 516 حرفًا أساس-64 أو أكثر (أو ما يعادل 387 بايت أو أكثر بالشكل الثنائي)، ويعتمد العدد على نوع التوقيع.

#### حزم البيانات المجهولة من نوع SAM (خام)

من خلال استغلال أقصى قدر من عرض النطاق الترددي في I2P، يسمح SAM للعملاء بإرسال واستقبال الرسائل الرقمية المجهولة، مع ترك مسؤولية المصادقة ومعلومات الرد للعميل نفسه. هذه الرسائل الرقمية غير موثوقة وغير مرتبة، وقد تصل إلى 32768 بايت.

الحجم الأدنى هو 1. للحصول على أفضل موثوقية في التسليم، يُوصى بأن يكون الحجم الأقصى حوالي 11 كيلوبايت.

بعد إنشاء جلسة SAM مع STYLE=RAW، يمكن للعميل إرسال حزم بيانات مجهولة الهوية عبر جسر SAM بنفس الطريقة تمامًا كما في [إرسال حزم بيانات قابلة للرد أو نيئة](#sending-repliable-or-raw-datagrams).

كلا الطريقتين لاستقبال الداتاغرامات متاحتان أيضًا للداتاغرامات المجهولة.

يتم كتابة البيانات المستلمة بواسطة SAM على المقبس الذي تم فتح جلسة البيانات من خلاله، إذا لم يتم تحديد منفذ إعادة توجيه في أمر SESSION CREATE. هذه هي الطريقة المتوافقة مع الإصدار v1/v2 لاستقبال الحزم البيانات.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
عندما يتعين توجيه الرسائل البسيطة المجهولة إلى مضيف:منفذ معين، يُرسل الجسر إلى المضيف:المنفذ المحدد رسالة تحتوي على البيانات التالية:

```
$datagram_payload
```
اعتبارًا من SAM 3.2، عندما يتم تحديد HEADER=true في SESSION CREATE، سيتم إضافة سطر ترويسة قبل حزمة الداتاكرام الأولية المحولة على النحو التالي:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
للاطلاع على طريقة بديلة لإرسال الرسائل الرقمية المجهولة، انظر [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### داتا جرام 2/3

ال Datagram 2/3 هما تنسيقان جديدان تم تحديدهما في أوائل عام 2025. لا توجد حاليًا أي تنفيذات معروفة. تحقق من وثائق التنفيذ للحصول على الحالة الحالية. انظر [المواصفة](/docs/specs/datagrams) لمزيد من المعلومات.

لا توجد حاليًا خطط لزيادة إصدار SAM للإشارة إلى دعم Datagram 2/3. قد يكون هذا مشكلة لأن بعض التطبيقات قد ترغب في دعم Datagram 2/3 دون دعم ميزات SAM v3.3. أي تغيير في الإصدار لم يتم تحديده بعد (TBD).

كلا Datagram2 و Datagram3 قابلين للإجابة، ولكن فقط Datagram2 موثوق.

يُطابق Datagram2 الحزم القابلة للإجابة من منظور SAM تمامًا. كلا النوعين موثَّقَان. فقط تنسيق I2CP والتوقيع يختلفان، ولكن هذا لا يكون مرئيًا لعملاء SAM. كما يدعم Datagram2 التوقيعات دون اتصال، وبالتالي يمكن استخدامه من قبل العُقد الوجهة الموقعة دون اتصال.

الهدف هو أن يحل Datagram2 محل Datagram القابل للإعادة (Repliable datagrams) في التطبيقات الجديدة التي لا تتطلب التوافق العكسي. يوفر Datagram2 حماية من إعادة التشغيل (replay protection) غير المتوفرة في Datagram القابل للإعادة. إذا كانت هناك حاجة للتوافق العكسي، يمكن للتطبيق دعم كل من Datagram2 و Datagram القابل للإعادة في نفس الجلسة باستخدام جلسات SAM 3.3 PRIMARY.

Datagram3 قابل للرد لكنه غير موثق. الحقل 'from' في تنسيق I2CP هو هاش وليس وجهة. ستكون $destination المرسلة من خادم SAM إلى العميل عبارة عن هاش بطول 44 حرفًا في الترميز base64. لتحويله إلى وجهة كاملة للرد، قم بفك ترميزه من base64 إلى 32 بايت ثنائي، ثم قم بترميزه إلى base32 ليصبح 52 حرفًا، وأضف ".b32.i2p" لإجراء عملية بحث باسم (NAMING LOOKUP). كما هو معتاد، ينبغي للعملاء الحفاظ على ذاكرتهم المؤقتة الخاصة لتجنب تكرار عمليات البحث باسم (NAMING LOOKUP).

يجب على مصممي التطبيقات اتخاذ أقصى درجات الحذر والنظر في الآثار الأمنية للرسائل المشفرة غير الموثقة.

#### اعتبارات MTU داتاجرام V3

قد تكون حزم البيانات الخاصة بـ I2P أكبر من الحد الأقصى لحجم وحدة الإرسال (MTU) على الإنترنت التقليدي البالغ 1500 بايت. من المرجح أن الحزم المرسلة محليًا والحزم القابلة لإعادة التوجيه التي تبدأ بوجهة base64 بحجم 516 بايت أو أكثر ستفوق هذا الحد. ومع ذلك، فإن حدود MTU الخاصة بـ localhost في أنظمة لينكس تكون عادةً أكبر بكثير، على سبيل المثال 65536. وتختلف حدود MTU الخاصة بـ localhost حسب نظام التشغيل. لن تكون حزم بيانات I2P أبدًا أكبر من 65536. ويعتمد حجم الحزمة على بروتوكول التطبيق المستخدم.

إذا كان عميل SAM موجودًا محليًا على خادم SAM وكانت النظام يدعم MTU أكبر، فلن يتم تجزئة الباقات محليًا. ولكن، إذا كان عميل SAM بعيدًا، فستتم تجزئة باقات IPv4 وستفشل باقات IPv6 (لأن IPv6 لا يدعم تجزئة UDP).

يجب أن يكون مطورو المكتبات والتطبيقات العميلة على دراية بهذه القضايا وتوثيق التوصيات لتجنب التجزئة ومنع فقدان الحزم، خاصةً في اتصالات العميل-الخادم SAM عن بُعد.

#### إرسال الداتا جرام، الإرسال الخام (معالجة داتا جرام متوافقة مع الإصدار V1/V2)

في SAM V3، فإن الطريقة المفضلة لإرسال الداتاغرامات هي عبر منفذ المقبس (socket) للداتاغرام على المنفذ 7655 كما هو موضح أعلاه. ومع ذلك، يمكن إرسال الداتاغرامات القابلة للرد مباشرة عبر مقبس جسر SAM باستخدام الأمر DATAGRAM SEND، كما هو موثق في [SAM V1](/docs/api/sam) و[SAM V2](/docs/api/samv2).

اعتبارًا من الإصدار 0.9.14 (الإصدار 3.1)، يمكن إرسال الرسائل الرقمية المجهولة مباشرة عبر مقبس جسر SAM باستخدام الأمر RAW SEND، كما هو موثق في [SAM V1](/docs/api/sam) و[SAM V2](/docs/api/samv2).

ابتداءً من الإصدار 0.9.24 (الإصدار 3.2)، قد تتضمن أوامر DATAGRAM SEND وRAW SEND المعلمات FROM_PORT=nnnn و/أو TO_PORT=nnnn لتجاوز المنافذ الافتراضية. وابتداءً من الإصدار 0.9.24 (الإصدار 3.2)، قد تتضمن أوامر RAW SEND المعلمة PROTOCOL=nnn لتجاوز البروتوكول الافتراضي.

لا تدعم هذه الأوامر معلمة المُعرف (ID). تُرسل حُزم البيانات إلى الجلسة التي تم إنشاؤها مؤخرًا بنمط DATAGRAM أو RAW، حسب الاقتضاء. قد تُضاف دعمًا لمعلمة المُعرف (ID) في إصدار قادم.

تنسيقات DATAGRAM2 وDATAGRAM3 *غير* مدعومة بالطريقة المتوافقة مع V1/V2.

### جلسات SAM الأساسية (V3.3 وما فوق)

*تم تقديم الإصدار 3.3 في إصدار I2P 0.9.25.*

*في إصدار سابق من هذا المواصفة، كانت الجلسات الأساسية (PRIMARY) تُعرف بالجلسات الرئيسية (MASTER). وفي كل من `i2pd` و`I2P+`، لا تزال تُعرف فقط بالجلسات الرئيسية (MASTER).*

يُضيف SAM v3.3 دعمًا لتشغيل تدفقات البث (streaming) ووحدات الباط (datagrams) والجلسات الفرعية الخام (raw subsessions) على نفس الجلسة الأساسية، وكذلك دعم تشغيل جلسات فرعية متعددة من نفس النوع. يستخدم كل حركة المرور من الجلسات الفرعية وجهة واحدة، أو مجموعة من الأنفاق. ويعتمد توجيه حركة المرور من I2P على خيارات المنفذ والبروتوكول الخاصة بالجلسات الفرعية.

لإنشاء جلسات فرعية متعددة، يجب إنشاء جلسة رئيسية ثم إضافة جلسات فرعية إلى الجلسة الرئيسية. يجب أن تحتوي كل جلسة فرعية على معرف فريد وبروتوكول منفذ فريد ورقم منفذ فريد. كما يمكن أيضًا إزالة الجلسات الفرعية من الجلسة الرئيسية.

باستخدام جلسة رئيسية وتشكيلة من الجلسات الفرعية، يمكن لعميل SAM دعم تطبيقات متعددة، أو تطبيق واحد متطور يستخدم مجموعة متنوعة من البروتوكولات، على مجموعة واحدة من الأنفاق. على سبيل المثال، يمكن لعميل بروتوكول مشاركة الملفات (bittorrent) إعداد جلسة فرعية للتدفق لاتصالات الند للند، إلى جانب جلسات فرعية للرسائل البيانات (datagram) والجلسة الفرعية الخام (raw) للتواصل عبر شبكة DHT.

#### إنشاء جلسة رئيسية

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
ستستجيب جسر SAM بنجاح أو فشل كما في [استجابة إنشاء جلسة قياسية](#session-creation-response).

لا تقم بتعيين خيارات PORT أو HOST أو FROM_PORT أو TO_PORT أو PROTOCOL أو LISTEN_PORT أو LISTEN_PROTOCOL أو HEADER في الجلسة الأساسية. لا يُسمح بإرسال أي بيانات على معرف الجلسة الأساسي (PRIMARY) أو على منفذ التحكم (control socket). يجب أن تستخدم جميع الأوامر مثل STREAM CONNECT وDATAGRAM SEND وما شابه ذلك معرف الجلسة الفرعية (subsession ID) عبر منفذ منفصل.

تتّصل الجلسة الأساسية بالراوتر وتبني الأنفاق. عندما يستجيب جسر SAM، تكون الأنفاق قد بُنيت وتكون الجلسة جاهزة لإضافة الجلسات الفرعية. يجب تزويد جميع خيارات [I2CP](/docs/protocol/i2cp) المتعلقة بمعايير النفق مثل الطول والكمية والاسم المستعار في أمر إنشاء الجلسة الأساسية (SESSION CREATE).

يتم دعم جميع أوامر الأدوات في الجلسة الأساسية.

عند إغلاق الجلسة الأساسية، يتم أيضًا إغلاق جميع الجلسات الفرعية.

ملاحظة: قبل الإصدار 0.9.47، استخدم STYLE=MASTER. تم دعم STYLE=PRIMARY بدءًا من الإصدار 0.9.47. لا يزال يتم دعم MASTER من أجل التوافق مع الإصدارات السابقة.

#### إنشاء جلسة فرعية

باستخدام نفس مقبس التحكم الذي تم إنشاء الجلسة الأساسية عليه:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
سترد جسر SAM بنجاح أو فشل كما هو الحال في [استجابة إنشاء جلسة قياسية](#session-creation-response). وبما أن الأنفاق قد تم بناؤها مسبقًا في عملية إنشاء الجلسة الأساسية، فيجب أن يستجيب جسر SAM فورًا.

لا تقم بتعيين خيار DESTINATION في SESSION ADD. ستستخدم الجلسة الفرعية الوجهة المحددة في الجلسة الأساسية. يجب إضافة جميع الجلسات الفرعية عبر منفذ التحكم، أي الاتصال نفسه الذي أنشأت عليه الجلسة الأساسية.

يجب أن تحتوي الجلسات الفرعية المتعددة على خيارات مميزة بدرجة كافية تسمح بتوجيه البيانات الواردة بشكل صحيح. وعلى وجه التحديد، يجب أن تمتلك الجلسات المتعددة من نفس النمط خيارات LISTEN_PORT مختلفة (و/أو LISTEN_PROTOCOL، في حالة RAW فقط). وسيؤدي إجراء SESSION ADD بمنفذ الاستماع والبروتوكول الذي يطابق جلسة فرعية موجودة إلى حدوث خطأ.

LISTEN_PORT هو المنفذ المحلي في I2P، أي منفذ الاستقبال (TO) للبيانات الواردة. إذا لم يتم تحديد LISTEN_PORT، فسيتم استخدام قيمة FROM_PORT. وإذا لم يتم تحديد كل من LISTEN_PORT و FROM_PORT، فستعتمد التوجيهات الواردة على STYLE و PROTOCOL فقط. بالنسبة إلى LISTEN_PORT و LISTEN_PROTOCOL، تعني القيمة 0 "أي قيمة"، أي أنها تعمل كرمز بديل (wildcard). إذا كانت كلتا القيمتين LISTEN_PORT و LISTEN_PROTOCOL تساويان 0، فستصبح هذه الجلسة الفرعية الافتراضية للحركة الواردة التي لا يتم توجيهها إلى جلسة فرعية أخرى. لن يتم توجيه حركة البث الواردة (البروتوكول 6) أبدًا إلى جلسة فرعية من نوع RAW، حتى لو كانت قيمة LISTEN_PROTOCOL الخاصة بها 0. ولا يجوز لجلسة فرعية من نوع RAW تعيين قيمة LISTEN_PROTOCOL تساوي 6. إذا لم توجد جلسة افتراضية أو جلسة فرعية تطابق بروتوكول ومنفذ الحركة الواردة، فسيتم تجاهل تلك البيانات.

استخدم معرّف الجلسة الفرعية، وليس معرّف الجلسة الأساسي، لإرسال واستقبال البيانات. يجب أن تستخدم جميع الأوامر مثل STREAM CONNECT، DATAGRAM SEND، وما إلى ذلك معرّف الجلسة الفرعية.

يتم دعم جميع أوامر الأدوات على الجلسة الأساسية أو الجلسات الفرعية. لا يتم دعم إرسال/استقبال حزم البيانات v1/v2 (datagram/raw) على الجلسة الأساسية أو على الجلسات الفرعية.

#### إيقاف جلسة فرعية

باستخدام نفس مقبس التحكم الذي تم إنشاء الجلسة الأساسية عليه:

```
->  SESSION REMOVE
          ID=$nickname
```
هذا يزيل جلسة فرعية من الجلسة الأساسية. لا تقم بتعيين أي خيارات أخرى على SESSION REMOVE. يجب إزالة الجلسات الفرعية عبر مقبس التحكم، أي الاتصال نفسه الذي أنشأت عليه الجلسة الأساسية. بعد إزالة الجلسة الفرعية، يتم إغلاقها ولا يمكن استخدامها لإرسال أو استقبال البيانات.

ستستجيب جسر SAM بنجاح أو فشل كما في [استجابة إنشاء جلسة قياسية](#session-creation-response).

### أوامر أداة SAM

تتطلب بعض أوامر الأدوات وجود جلسة مسبقة، وبعضها لا يتطلب ذلك. انظر التفاصيل أدناه.

#### البحث عن اسم المضيف

يمكن للعميل استخدام الرسالة التالية لاستعلام جسر SAM للحصول على تفسير الأسماء:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
التي يتم الإجابة عنها بواسطة

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
قد تكون قيمة RESULT إحدى القيم التالية:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
إذا كان NAME=ME، فستحتوي الإجابة على الوجهة المستخدمة في الجلسة الحالية (مفيد إذا كنت تستخدم جلسة عابرة). إذا لم يكن $result بحالة OK، فقد تتضمن MESSAGE رسالة وصفية مثل "تنسيق غير صحيح"، إلخ. وتشير INVALID_KEY إلى وجود خطأ ما في $name في الطلب، ربما بسبب أحرف غير صالحة.

$الوجهة هي التنميط الأساس-64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، والذي يتكون من 516 حرفًا أساس-64 أو أكثر (أو ما يعادل 387 بايت أو أكثر بالشكل الثنائي)، ويعتمد العدد على نوع التوقيع.

لا يتطلب NAMING LOOKUP أن تكون الجلسة قد أُنشئت مسبقًا. ومع ذلك، قد تفشل عملية بحث عن اسم .b32.i2p في بعض التنفيدات إذا لم تكن مخزنة مؤقتًا وتتطلب استعلامًا على الشبكة، وذلك بسبب عدم توفر أنفاق عميل للبحث.

#### خيارات البحث عن الاسم

تم توسيع عملية البحث في الأسماء (NAMING LOOKUP) بدءًا من واجهة برمجة تطبيقات الموجه (router API) 0.9.66 لدعم عمليات البحث عن الخدمات. قد تختلف الدعم باختلاف التنفيذ. راجع الاقتراح 167 للحصول على مزيد من المعلومات.

NAMING LOOKUP NAME=example.i2p OPTIONS=true يطلب خريطة الخيارات في الرد. يمكن أن يكون NAME عنوان base64 كاملاً عندما تكون OPTIONS=true.

إذا نجحت عملية البحث عن الوجهة وكانت هناك خيارات موجودة في leaseset، فستظهر في الرد، بعد الوجهة، واحدة أو أكثر من الخيارات على شكل OPTION:mفتاح=قيمة. سيكون لكل خيار بادئة OPTION: منفصلة. سيتم تضمين جميع الخيارات من leaseset، وليس فقط خيارات سجل الخدمة. على سبيل المثال، قد تكون هناك خيارات لمعايير معرّفة في المستقبل. مثال:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

تُعتبر المفاتيح التي تحتوي على علامة '='، وكذلك المفاتيح أو القيم التي تحتوي على سطر جديد، غير صالحة وسيتم إزالة زوج المفتاح/القيمة من الرد. إذا لم يتم العثور على أي خيارات في leaseset، أو إذا كان leaseset من الإصدار 1، فلن يتضمن الرد أي خيارات. إذا كانت OPTIONS=true موجودة في عملية البحث، ولم يتم العثور على leaseset، فسيتم إرجاع قيمة نتيجة جديدة هي LEASESET_NOT_FOUND.

#### توليد مفتاح الوجهة

يمكن توليد المفاتيح العامة والخاصة بصيغة base64 باستخدام الرسالة التالية:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
التي يتم الإجابة عنها بواسطة

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
ابتداءً من الإصدار 3.1 (I2P 0.9.14)، يتم دعم معلمة اختيارية تُسمى SIGNATURE_TYPE. يمكن أن تكون قيمة SIGNATURE_TYPE أي اسم (مثلاً ECDSA_SHA256_P256، غير حساس لحالة الأحرف) أو رقم (مثلاً 1) تدعمه [شهادات المفاتيح](/docs/specs/common-structures#type_Certificate). القيمة الافتراضية هي DSA_SHA1، وهي ليست ما تريده. بالنسبة لمعظم التطبيقات، يُرجى تحديد SIGNATURE_TYPE=7.

$الوجهة هي التنميط الأساس-64 لهيكل [الوجهة](/docs/specs/common-structures#type_Destination)، والذي يتكون من 516 حرفًا أساس-64 أو أكثر (أو ما يعادل 387 بايت أو أكثر بالشكل الثنائي)، ويعتمد العدد على نوع التوقيع.

$privkey هو تمثيل base 64 للسلسلة الناتجة عن دمج [الوجهة] (/docs/specs/common-structures#type_Destination) متبوعة بـ [المفتاح الخاص] (/docs/specs/common-structures#type_PrivateKey) ثم بـ [مفتاح التوقيع الخاص] (/docs/specs/common-structures#type_SigningPrivateKey)، ويتكوّن من 884 حرفًا على الأقل في التمثيل base 64 (أو 663 بايت على الأقل بصيغته الثنائية)، ويعتمد الطول على نوع التوقيع. ويُحدد التنسيق الثنائي في وثيقة ملف المفتاح الخاص.

ملاحظات حول المفتاح الخاص الثنائي (Private Key) المكون من 256 بايت: <a href="/docs/specs/common-structures#type_PrivateKey">[Private Key]</a>: لم يتم استخدام هذا الحقل منذ الإصدار 0.6 (2005). قد تُرسل تطبيقات SAM بيانات عشوائية أو أصفارًا كاملة في هذا الحقل؛ لذا لا داعي للقلق إذا ظهرت سلسلة من الحروف AAAA في الترميز base64. معظم التطبيقات ستخزن ببساطة السلسلة المشفرة بـ base64 وتعيدها كما هي في SESSION CREATE، أو تقوم بفك ترميزها إلى صيغة ثنائية للتخزين، ثم إعادة تشفيرها عند SESSION CREATE. ومع ذلك، يمكن للتطبيقات أن تقوم بفك تشفير base64، وتحليل البيانات الثنائية وفقًا لمواصفات PrivateKeyFile، ثم حذف الجزء الخاص بالمفتاح الخاص المكون من 256 بايت، واستبداله بـ 256 بايت من بيانات عشوائية أو أصفار عند إعادة التشفير لـ SESSION CREATE. يجب الحفاظ على جميع الحقول الأخرى في مواصفات PrivateKeyFile كما هي. قد يوفر هذا 256 بايت من مساحة التخزين في نظام الملفات، ولكن من المرجح أن لا يستحق العناء بالنسبة لمعظم التطبيقات. راجع الاقتراح 161 للحصول على معلومات وخلفية إضافية.

لا يتطلب DEST GENERATE أن تكون الجلسة قد تم إنشاؤها أولاً.

لا يمكن استخدام DEST GENERATE لإنشاء وجهة باستخدام توقيعات غير متصلة.

#### PING/PONG (SAM 3.2 أو أحدث)

قد يُرسل العميل أو الخادم ما يلي:

```
PING[ arbitrary text]
```
على منفذ التحكم، مع الاستجابة:

```
PONG[ arbitrary text from the ping]
```
يُستخدم للحفاظ على اتصال منفذ التحكم نشطًا. يجوز لأي من الطرفين إغلاق الجلسة والمنفذ إذا لم يتم استلام استجابة خلال وقت معقول، ويعتمد ذلك على التنفيذ.

إذا حدثت مهلة أثناء الانتظار لاستلام PONG من العميل، فقد يرسل الجسر:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
ثم انقطع الاتصال.

إذا حدثت مهلة أثناء انتظار رسالة PONG من الجسر، فقد يقطع العميل الاتصال ببساطة.

PING/PONG لا يتطلبان إنشاء جلسة أولاً.

#### QUIT/STOP/EXIT (SAM 3.2 أو أعلى، ميزات اختيارية)

الأوامر QUIT وSTOP وEXIT ستُغلق الجلسة والموصل (socket). تنفيذ هذا الأمر اختياري، لتسهيل الاختبار عبر telnet. ما إذا كان سيكون هناك أي رد قبل إغلاق الموصل (مثلاً رسالة SESSION STATUS) يعتمد على التنفيذ المحدد، وخارج نطاق هذا المواصفة.

QUIT/STOP/EXIT لا تتطلب أن تكون الجلسة قد تم إنشاؤها مسبقًا.

#### المساعدة (ميزة اختيارية)

قد تقوم الخوادم بتنفيذ أمر HELP. هذا التنفيذ اختياري، لتسهيل الاختبار عبر telnet. شكل المخرجات وكشف نهاية المخرجات يعتمدان على التنفيذ، وهما خارجان عن نطاق هذا المواصفة.

لا يتطلب HELP إنشاء جلسة أولاً.

#### تكوين المصادقة (SAM 3.2 أو أحدث، ميزة اختيارية)

تهيئة المصادقة باستخدام أمر AUTH. قد يقوم خادم SAM بتنفيذ هذه الأوامر لتسهيل التخزين الدائم للمصادق (credentials). إن تهيئة المصادقة بطرق أخرى غير هذه الأوامر تعتمد على التنفيذ المحدد وخارج نطاق هذا المواصفة.

- AUTH ENABLE يُفعّل المصادقة على الاتصالات اللاحقة
- AUTH DISABLE يُعطّل المصادقة على الاتصالات اللاحقة
- AUTH ADD USER="foo" PASSWORD="bar" يضيف مستخدمًا/كلمة مرور
- AUTH REMOVE USER="foo" يزيل هذا المستخدم

يُوصى باستخدام علامات الاقتباس المزدوجة لكل من اسم المستخدم وكلمة المرور، ولكنها ليست إلزامية. يجب هروب علامة الاقتباس المزدوجة الموجودة داخل اسم المستخدم أو كلمة المرور باستخدام خط مائل عكسي (\). في حالة الفشل، سيقوم الخادم بالرد بـ I2P_ERROR ورسالة توضيحية.

لا يتطلب AUTH إنشاء جلسة أولاً.

### قيم RESULT

هذه هي القيم التي يمكن أن تحملها حقل النتيجة (RESULT)، مع معانيها:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
قد تختلف التنفيذات المختلفة في نتيجة RESULT التي يتم إرجاعها في السيناريوهات المختلفة.

معظم الاستجابات التي تحتوي على نتيجة (RESULT) بخلاف OK ستشمل أيضًا رسالة (MESSAGE) بمعلومات إضافية. وعادةً ما تكون الرسالة مفيدة في تصحيح الأخطاء. ومع ذلك، فإن سلاسل الرسائل تعتمد على التنفيذ، وقد لا يتم ترجمتها من قبل خادم SAM إلى اللغة المحلية الحالية، وقد تحتوي على معلومات داخلية خاصة بالتنفيذ مثل الاستثناءات، وهي عرضة للتغيير دون إشعار. وعلى الرغم من أن عميلات SAM قد تختار عرض سلاسل الرسائل للمستخدمين، إلا أنه لا ينبغي اتخاذ قرارات برمجية بناءً على هذه السلاسل، لأن ذلك سيكون هشًا.

### خيارات النفق وI2CP والتدفق

يمكن تمرير هذه الخيارات كأزواج اسم=قيمة في سطر SAM SESSION CREATE.

قد تتضمن جميع الجلسات [خيارات I2CP مثل أطوال الأنفاق وكمياتها](/docs/protocol/i2cp#options). وقد تتضمن جلسات STREAM [خيارات مكتبة البث](/docs/api/streaming#options).

راجع تلك المراجع للحصول على أسماء الخيارات والقيم الافتراضية. الوثائق المشار إليها خاصة بتنفيذ جافا للراوتر. قد تتغير القيم الافتراضية. أسماء الخيارات وقيمها حساسة لحالة الأحرف. قد لا تدعم تنفيذات الراوتر الأخرى جميع الخيارات وقد يكون لديها قيم افتراضية مختلفة؛ راجع وثائق الراوتر للحصول على التفاصيل.

### ملاحظات BASE 64

يجب أن يستخدم الترميز Base 64 أبجدية I2P القياسية لـ Base 64 وهي "A-Z، a-z، 0-9، -، ~".

### الإعداد الافتراضي لـ SAM

المنفذ الافتراضي لـ SAM هو 7656. لا يكون SAM ممكّنًا افتراضيًا في برنامج توجيه Java I2P؛ بل يجب تشغيله يدويًا، أو تهيئته للتشغيل التلقائي، من خلال صفحة تهيئة العملاء (configure clients) في واجهة التحكم الخاصة بالراوتر، أو من خلال ملف clients.config. أما منفذ SAM UDP الافتراضي فهو 7655، ويستمع على 127.0.0.1. يمكن تغيير هذه الإعدادات في برنامج التوجيه بلغة Java بإضافة المعاملات sam.udp.port=nnnnn و/أو sam.udp.host=w.x.y.z إلى أمر التشغيل، أو في سطر SESSION.

تختلف التهيئة في الراوترات الأخرى حسب التنفيذ. راجع [دليل تهيئة i2pd هنا](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
