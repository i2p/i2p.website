---
title: "نظرة عامة على I2NP"
description: "نظرة عامة على بروتوكول شبكة I2P (I2NP) - تنسيق الرسائل، الأنواع، الأولويات، وقيود الحجم."
slug: "i2np-overview"
aliases:
  - "/ar/docs/protocol/i2np"
  - "/ar/docs/protocol/i2np/"
  - "/ar/i2np"
  - "/ar/i2np/"
category: "البروتوكولات"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## نظرة عامة

بروتوكول شبكة I2P (I2NP)، الذي يقع بين I2CP والبروتوكولات النقل المختلفة لـ I2P، يُعنى بإدارة توجيه وخلط الرسائل بين الراوترات، وكذلك اختيار وسائط النقل المستخدمة عند التواصل مع ندّ يدعم عدة وسائط نقل مشتركة.

## تعريف I2NP

يمكن استخدام رسائل I2NP (بروتوكول شبكة I2P) للرسائل من نوع "وجهة واحدة"، أو من نوع "راوتر إلى راوتر"، أو من نوع "نقطة إلى نقطة". وبتشفير الرسائل ولفّها داخل رسائل أخرى، يمكن إرسالها بطريقة آمنة عبر عدة محطات وسيطة حتى تصل إلى الوجهة النهائية. ويُستخدم الأولوية فقط محليًا في نقطة المنشأ، أي عند ترتيبها في قائمة الانتظار للإرسال الخارجي.

قد لا تكون الأولويات المذكورة أدناه حالية وتخضع للتغيير. وقد تختلف طريقة تنفيذ قائمة الانتظار حسب الأولوية.

## تنسيق الرسالة {#format}

تحدد الجدول التالي الرأس التقليدي بحجم 16 بايت المستخدم في NTCP. تستخدم وسائط النقل SSU وNTCP2 رؤوسًا معدلة.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Type</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unique ID</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Checksum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 - 61.2KB</td>
</tr>
</table>
بينما يكون الحد الأقصى لحجم الحمولة 64 كيلوبايت نظريًا، فإن الحجم يخضع لقيود إضافية تتعلق بطريقة تجزئة رسائل I2NP إلى رسائل نفق متعددة بحجم 1 كيلوبايت كما هو موضح في [صفحة تنفيذ النفق](/docs/specs/tunnel-implementation/).

الحد الأقصى لعدد القطع هو 64، وقد لا تكون الرسالة محاذاة بشكل مثالي، لذلك يجب أن تتسع الرسالة في 63 قطعة على الأكثر نظريًا.

أقصى حجم لجزء أولي هو 956 بايت (بافتراض وضعية التسليم TUNNEL)؛ وأقصى حجم لجزء لاحق هو 996 بايت. وبالتالي، فإن أقصى حجم ممكن هو تقريبًا 956 + (62 × 996) = 62708 بايت، أو 61.2 كيلوبايت.

بالإضافة إلى ذلك، قد تكون هناك قيود إضافية على وسائل النقل. فإن الحد الأقصى لـ NTCP هو 16 كيلوبايت - 6 = 16378 بايت. والحد الأقصى لـ SSU هو تقريبًا 32 كيلوبايت. والحد الأقصى لـ NTCP2 هو تقريبًا 64 كيلوبايت - 20 = 65516 بايت، وهو أعلى مما يمكن أن تدعمه النفق.

لاحظ أن هذه ليست الحدود الخاصة بحزم البيانات التي يراها العميل، لأن الموجه قد يجمع مجموعة تأجير (leaseset) و/أو علامات جلسة (session tags) مع رسالة العميل ضمن رسالة ثومية (garlic message). حيث يمكن أن تضيف مجموعة التأجير والعلامات معًا حوالي 5.5 كيلوبايت. وبالتالي فإن الحد الحالي لحزمة البيانات هو حوالي 10 كيلوبايت. وسيتم زيادة هذا الحد في إصدار قادم.

## أنواع الرسائل {#types}

كلما كان الرقم الأعلى أولوية أعلى. إن الجزء الأكبر من حركة المرور يتكون من TunnelDataMessages (الأولوية 400)، وبالتالي فإن أي شيء فوق 400 يُعتبر عمليًا أولوية عالية، وأي شيء تحته أولوية منخفضة. لاحظ أيضًا أن العديد من الرسائل يتم توجيهها عادةً عبر أنفاق استكشافية، وليس عبر أنفاق العميل، وبالتالي قد لا تكون في نفس الطابور ما لم تكن المحطات الأولى تقع على نفس الندّ.

أيضًا، ليست جميع أنواع الرسائل تُرسل بدون تشفير. على سبيل المثال، عند اختبار نفق، يقوم الموجه بتغليف رسالة حالة التسليم (DeliveryStatusMessage)، والتي بدورها تُغلف في رسالة ثومية (GarlicMessage)، ثم تُغلف داخل رسالة بيانات (DataMessage).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Priority</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Comments</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookupMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">May vary</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseSearchReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Typ. 161</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Size is 65 + 32*(number of hashes) where typically, the hashes for three floodfill routers are returned.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseStoreMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Varies</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">460</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet. RouterInfo structures are compressed, and size varies; however there is a continuing effort to reduce the amount of data published in a RouterInfo.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4 - 62080</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">425</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary on a per-destination basis</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DeliveryStatusMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Used for message replies, and for testing tunnels - generally wrapped in a GarlicMessage</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/overview/garlic-routing/">GarlicMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generally wrapped in a DataMessage - but when unwrapped, given a priority of 100 by the forwarding router</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelDataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1028</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The most common message. Priority for tunnel participants, outbound endpoints, and inbound gateways was reduced to 200 as of release 0.6.1.33. Outbound gateway messages (i.e. those originated locally) remains at 400.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelGatewayMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300/400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildReplyMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Others (Types 0, 4-9, 12)</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">0, 4-9, 12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Obsolete, Unused</td>
</tr>
</table>
## اختبار النفق

تتطلب اختبار النفق بدءًا من إصدار API 0.9.68 لعام 2026-02، حيث يُسمح للراوترات بإسقاط الأنظمة النفقية المشاركة التي لم تستقبل أي حركة مرور بعد الدقيقتين الأوليين.

## مواصفات البروتوكول الكاملة

انظر [صفحة مواصفات I2NP](/docs/specs/i2np/) للحصول على مواصفات البروتوكول الكاملة. انظر أيضًا [صفحة مواصفات هياكل البيانات الشائعة](/docs/specs/common-structures/).

## العمل المستقبلي

ليس من الواضح ما إذا كان نظام الأولوية الحالي فعالًا بشكل عام، أو ما إذا كانت أولويات الرسائل المختلفة بحاجة إلى تعديل إضافي. هذا موضوع يتطلب مزيدًا من البحث والتحليل والاختبار.
