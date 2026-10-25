---
title: "BOB - جسر أساسي مفتوح"
description: "واجهة برمجة تطبيقات مهجورة لإدارة الوجهات"
slug: "bob"
aliases:
  - "/ar/docs/api/bob"
  - "/ar/docs/api/bob/"
  - "/ar/bob"
  - "/ar/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## تحذير - مهجور

غير مخصص للاستخدام في التطبيقات الجديدة. BOB، كما هو محدد هنا، يدعم نوع التوقيع DSA-SHA1 فقط. لن يتم توسيع BOB لدعم أنواع التوقيع الجديدة أو الميزات المتقدمة الأخرى. يجب على التطبيقات الجديدة استخدام [SAMv3](/docs/api/samv3).

تم إزالة دعم BOB من التثبيتات الجديدة لـ Java I2P اعتباراً من الإصدار 1.7.0 (2022-02). سيستمر في العمل في Java I2P المثبت أصلاً كإصدار 1.6.1 أو أقدم، حتى بعد التحديثات، لكنه غير مدعوم وقد يتعطل في أي وقت. BOB ما زال مدعوماً من قبل i2pd اعتباراً من 2025-05، لكن التطبيقات يجب أن تنتقل إلى SAMv3 للأسباب المذكورة أعلاه. راجع [وثائق i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) لأي إضافات على الـ API الموثق هنا والمدعومة من قبل i2pd.

في هذه المرحلة، تم دمج معظم الأفكار الجيدة من BOB في SAMv3، الذي يحتوي على المزيد من الميزات والاستخدام الواقعي. قد يعمل BOB لا يزال على بعض التثبيتات (انظر أعلاه)، لكنه لا يحصل على الميزات المتقدمة المتاحة لـ SAMv3 وهو غير مدعوم بشكل أساسي، باستثناء i2pd.

## مكتبات اللغات لواجهة برمجة التطبيقات BOB

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## نظرة عامة

`KEYS` = زوج مفاتيح عام+خاص، هذه بتنسيق BASE64

`KEY` = المفتاح العام، أيضاً BASE64

`ERROR` كما هو مضمن يُرجع الرسالة `"ERROR "+DESCRIPTION+"\n"`، حيث أن `DESCRIPTION` هو ما حدث خطأ فيه.

`OK` ترجع `"OK"`، وإذا كان هناك بيانات لإرجاعها، فتكون في نفس السطر. `OK` تعني أن الأمر قد اكتمل.

تحتوي أسطر `DATA` على المعلومات التي طلبتها. قد يكون هناك عدة أسطر `DATA` لكل طلب.

**ملاحظة:** أمر المساعدة هو الأمر الوحيد الذي لديه استثناء من القواعد... يمكنه فعلياً عدم إرجاع أي شيء! هذا مقصود، حيث أن المساعدة هي أمر للإنسان وليس للتطبيق.

## الاتصال والإصدار

جميع مخرجات حالة BOB تكون على شكل أسطر. قد تنتهي الأسطر بـ \\n أو \\r\\n، حسب النظام. عند الاتصال، يخرج BOB سطرين:

```
BOB version
OK
```
الإصدار الحالي هو: 00.00.10

لاحظ أن الإصدارات السابقة استخدمت أرقام سادس عشر بأحرف كبيرة ولم تتوافق مع معايير الإصدارات في I2P. يُنصح بأن تستخدم الإصدارات اللاحقة الأرقام 0-9 فقط.

### تاريخ الإصدارات

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## الأوامر

**يرجى الملاحظة:** للحصول على التفاصيل الحالية حول الأوامر يرجى استخدام أمر المساعدة المدمج. فقط اتصل عبر telnet إلى localhost 2827 واكتب help وستحصل على توثيق كامل لكل أمر.

الأوامر لا تُلغى أو تُغيّر أبداً، ولكن تُضاف أوامر جديدة من وقت لآخر.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
بمجرد الإعداد، يمكن لجميع TCP sockets أن تتوقف حسب الحاجة وستفعل ذلك، ولا توجد حاجة لأي رسائل إضافية من/إلى قناة الأوامر. هذا يسمح للـ router بتنظيم سرعة التدفق دون الانفجار بـ OOM مثلما يفعل SAM حيث يختنق عند محاولة دفع العديد من التدفقات داخل أو خارج socket واحد -- هذا لا يمكن أن يتوسع عندما يكون لديك الكثير من الاتصالات!

ما هو رائع أيضًا في هذه الواجهة المحددة هو أن كتابة أي شيء للتفاعل معها أسهل بكثير من SAM. لا توجد معالجة أخرى للقيام بها بعد الإعداد. تكوينها بسيط جداً، لدرجة أن الأدوات البسيطة جداً، مثل nc (netcat) يمكن استخدامها للإشارة إلى تطبيق ما. القيمة هناك هي أنه يمكن للمرء جدولة أوقات التشغيل والإيقاف لتطبيق ما، دون الحاجة إلى تغيير التطبيق للقيام بذلك، أو حتى الحاجة إلى إيقاف ذلك التطبيق. بدلاً من ذلك، يمكنك حرفياً "فصل" الوجهة، و"توصيلها" مرة أخرى. طالما تم استخدام نفس عناوين IP/المنافذ ومفاتيح الوجهة عند رفع الجسر، فإن تطبيق TCP العادي لن يهتم، ولن يلاحظ. سيتم خداعه ببساطة -- الوجهات غير قابلة للوصول، وأنه لا شيء يأتي إلى الداخل.

## أمثلة

للمثال التالي، سنقوم بإعداد اتصال loopback محلي بسيط جداً، مع وجهتين. الوجهة "mouth" ستكون خدمة CHARGEN من INET superserver daemon. الوجهة "ear" ستكون منفذ محلي يمكنك الاتصال إليه عبر telnet، ومشاهدة نص ASCII الاختباري الجميل وهو يتدفق.

### مثال على حوار الجلسة

يعمل telnet بسيط 127.0.0.1 2827.

- A = التطبيق
- C = استجابة أمر BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**انتبه إلى مفتاح الوجهة أعلاه، مفتاحك سيكون مختلفاً!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
في هذه النقطة، لم يكن هناك خطأ، تم إعداد وجهة بالاسم المستعار "mouth". عندما تتصل بالوجهة المقدمة، فإنك تتصل فعلياً بخدمة `CHARGEN` على `19/TCP`.

الآن للنصف الآخر، حتى نتمكن فعلياً من الاتصال بهذه الوجهة.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
الآن كل ما نحتاج إليه هو استخدام telnet للاتصال بـ 127.0.0.1، المنفذ 37337، وإرسال مفتاح الوجهة أو عنوان المضيف من دفتر العناوين الذي نريد الاتصال به. في هذه الحالة، نريد الاتصال بـ "mouth"، كل ما نفعله هو لصق المفتاح وسيعمل.

**ملاحظة:** أمر "quit" في قناة الأوامر لا يقطع الاتصال بالـ tunnels مثل SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
بعد بضعة أميال افتراضية من هذا التدفق، اضغط `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
إليك ما حدث...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
يمكنك الاتصال بمواقع I2P أيضاً!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
رائع أليس كذلك؟ جرب بعض مواقع I2P المعروفة الأخرى إن أردت، أو مواقع غير موجودة، إلخ، للحصول على فكرة عن نوع المخرجات التي تتوقعها في مواقف مختلفة. في معظم الأحوال، يُنصح بتجاهل أي من رسائل الخطأ. فهي لن تكون ذات معنى للتطبيق، وهي معروضة فقط لأغراض التصحيح البشري.

### التنظيف

لنضع وجهاتنا الآن بعد أن انتهينا منها جميعًا.

أولاً، دعونا نرى ما هي أسماء الوجهات المستعارة المتوفرة لدينا.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
حسناً، ها هي هناك. أولاً، دعنا نزيل "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
الآن لإزالة "ear"، لاحظ أن هذا ما يحدث عندما تكتب بسرعة كبيرة، ويُظهر لك كيف تبدو رسائل الخطأ النموذجية.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## الوضع الصامت

لن أكلف نفسي عناء إظهار مثال على الطرف المستقبل للجسر لأنه بسيط جداً. هناك إعدادان محتملان له، ويتم التبديل بينهما باستخدام الأمر "quiet".

الإعداد الافتراضي ليس هادئًا، والبيانات الأولى التي تصل إلى socket الاستماع الخاص بك هي الوجهة التي تقوم بإجراء الاتصال. إنه سطر واحد يتكون من عنوان BASE64 متبوعًا بسطر جديد. كل شيء بعد ذلك مخصص للتطبيق لاستهلاكه فعليًا.

في الوضع الهادئ، فكر فيه كاتصال إنترنت عادي. لا تأتي أي بيانات إضافية على الإطلاق. الأمر تماماً كما لو كنت متصلاً بشكل عادي بالإنترنت العادي. هذا الوضع يتيح شكلاً من أشكال الشفافية مشابه لما هو متاح في صفحات إعدادات tunnel في وحدة تحكم router، بحيث يمكنك استخدام BOB لتوجيه وجهة إلى خادم ويب، على سبيل المثال، ولن تحتاج إلى تعديل خادم الويب على الإطلاق.

## مزايا BOB

الميزة من استخدام BOB لهذا الغرض كما ناقشنا سابقاً. يمكنك جدولة أوقات تشغيل عشوائية للتطبيق، إعادة التوجيه إلى جهاز مختلف، إلخ. قد يكون أحد استخدامات هذا شيئاً مثل الرغبة في محاولة إرباك تخمين حالة التشغيل بين router والوجهة. يمكنك إيقاف وتشغيل الوجهة بعملية مختلفة تماماً لجعل أوقات التشغيل والإيقاف عشوائية على الخدمات. بهذه الطريقة ستكون فقط توقف إمكانية الاتصال بمثل هذه الخدمة، ولن تحتاج إلى عناء إغلاقها وإعادة تشغيلها. يمكنك إعادة التوجيه والإشارة إلى جهاز مختلف على شبكتك المحلية أثناء قيامك بالتحديثات، أو الإشارة إلى مجموعة من أجهزة النسخ الاحتياطي حسب ما يعمل، إلخ، إلخ. فقط خيالك يحدد ما يمكنك فعله مع BOB.
