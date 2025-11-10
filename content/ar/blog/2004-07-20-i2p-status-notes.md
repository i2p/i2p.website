---
title: "ملاحظات حالة I2P بتاريخ 2004-07-20"
date: 2004-07-20
author: "jr"
description: "تحديث الحالة الأسبوعي الذي يغطي إصدار 0.3.2.3، وتغييرات السعة، وتحديثات الموقع الإلكتروني، والاعتبارات الأمنية"
categories: ["status"]
---

**1) 0.3.2.3، 0.3.3، وخارطة الطريق**

بعد إصدار 0.3.2.3 الأسبوع الماضي، لقد قمتم جميعاً بعمل رائع في الترقية — لم يبقَ لدينا الآن سوى حالتين لم تُجرِيا الترقية (إحداهما على 0.3.2.2 وأخرى ما تزال على إصدار قديم جداً 0.3.1.4 :). خلال الأيام القليلة الماضية كانت الشبكة أكثر موثوقية من المعتاد — الناس يبقون على irc.duck.i2p لساعات متواصلة، وتنزيلات الملفات الأكبر تتم بنجاح من eepsites(I2P Sites)، وإمكانية الوصول إلى eepsite(I2P Site) بشكل عام جيدة إلى حدٍ ما. وبما أن الأمور تسير على ما يرام وأريد أن أبقيكم على أهبة الاستعداد، فقد قررت تغيير بعض المفاهيم الأساسية وسنقوم بنشرها في إصدار 0.3.3 خلال يوم أو يومين.

نظرًا لتعليقات عدد من الأشخاص بشأن جدولنا الزمني وتساؤلهم عمّا إذا كنا سنلتزم بالمواعيد التي نشرناها، قررتُ أن عليّ على الأرجح تحديث الموقع ليعكس خريطة الطريق التي لديّ على جهاز PalmPilot الخاص بي، ففعلت ذلك [1]. لقد تأخرت المواعيد وتمت إعادة ترتيب بعض البنود، لكن الخطة ما تزال هي نفسها التي نوقشت الشهر الماضي [2].

ستفي النسخة 0.4 بمعايير الإصدار الأربعة المذكورة (وظيفية، آمنة، مجهولة الهوية، وقابلة للتوسع)، إلا أنه قبل 0.4.2 لن يتمكن سوى عدد قليل من الأشخاص الموجودين خلف NATs (ترجمة عناوين الشبكة) وجدران الحماية من المشاركة، وقبل 0.4.3 سيكون هناك حد أعلى فعّال لحجم الشبكة بسبب العبء الإضافي المترتب على الحفاظ على عدد كبير من اتصالات TCP إلى routers أخرى.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

على مدار الأسبوع الماضي تقريبًا، سمعني الناس في #i2p أتذمّر أحيانًا من أن تصنيفات الموثوقية لدينا اعتباطية تمامًا (وما سببته من معاناة في الإصدارات القليلة الماضية). لذلك تخلّينا بالكامل عن مفهوم الموثوقية، واستبدلناه بقياس للسعة - "ما مقدار ما يمكن لنظير أن يفعله لنا؟" وقد كان لهذا تأثيرات متتالية عبر كود اختيار النظراء وكود توصيف النظراء (وبالطبع على الـrouter console)، لكن بخلاف ذلك، لم يتغير الكثير.

يمكن الاطلاع على مزيد من المعلومات حول هذا التغيير في صفحة اختيار النظراء المُنقَّحة [3]، وعند صدور الإصدار 0.3.3 ستتمكنون جميعًا من رؤية الأثر بأنفسكم مباشرةً (لقد كنتُ أجري بعض التجارب عليه خلال الأيام القليلة الماضية، وأعدّل بعض الإعدادات، إلخ).

[3] http://www.i2p.net/redesign/how_peerselection

**3) تحديثات الموقع الإلكتروني**

على مدار الأسبوع الماضي، أحرزنا تقدماً كبيراً في إعادة تصميم الموقع [4] - تبسيط التنقل، وتنظيف بعض الصفحات الرئيسية، واستيراد المحتوى القديم، وكتابة بعض الإدخالات الجديدة [5]. نحن على وشك نقل الموقع ليصبح مباشراً، لكن لا تزال هناك بعض الأمور التي يجب إنجازها.

في وقتٍ سابق من اليوم، قام duck بمراجعة الموقع وأعدّ جردًا بالصفحات التي تنقصنا، وبعد تحديثات بعد ظهر اليوم، ما تزال هناك بعض المشكلات المتبقية آمل أن نتمكن إما من معالجتها أو أن نجد متطوعين يبادرون للتعامل معها:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

إلى جانب ذلك، أعتقد أن الموقع بات قريبًا جدًا من الجاهزية للإطلاق المباشر. هل لدى أيٍّ منكم أي اقتراحات أو مخاوف في هذا الصدد؟

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) الهجمات ووسائل الدفاع**

كان كونلي يبتكر بعض المقاربات الجديدة لمحاولة إيجاد ثغرات في أمن الشبكة وإخفاء الهوية فيها، وخلال ذلك توصّل إلى بعض السبل التي يمكننا من خلالها تحسين الأمور. ومع أن بعض جوانب التقنيات التي وصفها لا تتوافق تماماً مع I2P، ربما يا جماعة ترون طرقاً يمكن من خلالها توسيعها لمهاجمة الشبكة بشكل أكبر؟ هيا، جرّبوها :)

**5) ???**

هذا تقريبًا كل ما أستطيع تذكّره قبل اجتماع الليلة - لا تترددوا في طرح أي شيء آخر قد فاتني. على أي حال، أراكم جميعًا في #i2p خلال بضع دقائق.

=jr
