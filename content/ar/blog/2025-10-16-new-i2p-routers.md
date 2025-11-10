---
title: "New I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "تظهر عدة تنفيذات جديدة لـ I2P router، بما في ذلك emissary بلغة Rust و go-i2p بلغة Go، مما يوفر إمكانات جديدة للتضمين وتنويع الشبكة."
---

إنه وقت مثير لتطوير I2P، فمجتمعنا ينمو، وهناك الآن عدة نماذج أولية جديدة لـ I2P router تعمل بكامل طاقتها تظهر على الساحة! نحن متحمسون للغاية لهذا التطور ولمشاركة الأخبار معكم.

## كيف يساعد هذا الشبكة؟

إن كتابة I2P routers (الموجّهات) يساعدنا على إثبات أن وثائق المواصفات لدينا يمكن استخدامها لإنتاج I2P routers جديدة، ويفتح الشفرة أمام أدوات تحليل جديدة، ويحسّن عموماً أمن الشبكة وقابليتها للتشغيل البيني. إن تعدّد I2P routers يعني أن الأخطاء المحتملة ليست متطابقة، وقد لا ينجح هجوم على router معيّن على router آخر، وبذلك نتجنب مشكلة الأحادية التقنية. وربما يكون الأفق الأكثر إثارة على المدى الطويل، مع ذلك، هو التضمين.

## ما هو التضمين؟

في سياق I2P، يُقصد بالتضمين طريقة لإدراج router خاص بـ I2P داخل تطبيق آخر مباشرةً، دون الحاجة إلى router مستقل يعمل في الخلفية. هذه طريقة تمكّننا من جعل I2P أسهل استخداماً، مما يجعل الشبكة أسهل في النمو من خلال جعل البرمجيات أكثر إتاحة. كلٌّ من Java وC++ يعاني من صعوبة الاستخدام خارج منظومته البيئية الخاصة؛ فـ C++ تتطلب ارتباطات C مكتوبة يدوياً وهشة، وفي حالة Java، العناء المتمثل في التواصل مع تطبيق يعمل على JVM من تطبيق لا يعمل على JVM.

على الرغم من أن هذه الحالة طبيعية تمامًا من نواحٍ كثيرة، أعتقد أنه يمكن تحسينها لجعل I2P أكثر سهولة للوصول. توفّر لغات أخرى حلولًا أكثر أناقة لهذه المشكلات. وبالطبع، ينبغي لنا دائمًا أخذ الإرشادات القائمة لـ Java و C++ routers بعين الاعتبار واستخدامها.

## يظهر مبعوث من الظلام

بشكل مستقل تمامًا عن فريقنا، قام مطوّر يُدعى altonen بتطوير تنفيذ لـ I2P بلغة Rust يُسمّى emissary. وعلى الرغم من أنه لا يزال جديدًا إلى حدٍّ كبير، وأن Rust ليست مألوفة لنا، فإن هذا المشروع المثير للاهتمام يبدو واعدًا للغاية. نهنئ altonen على إنشاء emissary، وقد أعجبنا به كثيرًا.

### Why Rust?

السبب الرئيسي لاستخدام Rust هو في الأساس نفس سبب استخدام Java أو Go. Rust لغة برمجة مُصرَّفة تتميز بإدارة للذاكرة ومجتمع ضخم شديد الحماس. كما توفّر Rust مزايا متقدمة لإنتاج واجهات ربط (bindings) مع لغة البرمجة C قد تكون أسهل في الصيانة مقارنةً باللغات الأخرى، مع الاستفادة في الوقت نفسه من ميزات Rust القوية في أمان الذاكرة.

### Do you want to get involved with emissary?

يجري تطوير emissary على GitHub بواسطة altonen. يمكنك العثور على المستودع في: [altonen/emissary](https://github.com/altonen/emissary). كما تعاني Rust من نقص في مكتبات عميل SAMv3 الشاملة والمتوافقة مع أدوات الشبكات الشائعة في Rust. إن كتابة مكتبة SAMv3 تُعد مكانًا رائعًا للبدء.

## go-i2p is getting closer to completion

على مدى نحو ثلاث سنوات كنت أعمل على go-i2p، محاولاً تحويل مكتبة ناشئة إلى I2P router مكتمل الوظائف مكتوباً بـ Go الخالصة، وهي لغة أخرى آمنة من ناحية الذاكرة. خلال الأشهر الستة الماضية تقريباً، تمت إعادة هيكلته بشكل جذري لتحسين الأداء والموثوقية وقابلية الصيانة.

### Why Go?

على الرغم من أن Rust وGo تتشاركان العديد من المزايا نفسها، فإن Go أبسط بكثير للتعلّم من نواحٍ عديدة. على مدى سنوات، وُجدت مكتبات وتطبيقات ممتازة لاستخدام I2P بلغة البرمجة Go، بما في ذلك أكثر تنفيذات مكتبات SAMv3.3 اكتمالاً. ولكن من دون I2P router يمكننا إدارته تلقائيًا(مثل router مضمّن)، ما يزال ذلك يمثّل عائقًا أمام المستخدمين. الهدف من go-i2p هو سدّ تلك الفجوة وإزالة التعقيدات المزعجة أمام مطوّري تطبيقات I2P الذين يعملون بلغة Go.

### لماذا Rust؟

يتم تطوير go-i2p على Github، بشكل أساسي بواسطة eyedeekay في الوقت الحالي وهو مفتوح لمساهمات المجتمع على [go-i2p](https://github.com/go-i2p/). ضمن مساحة الأسماء هذه توجد العديد من المشاريع، مثل:

#### Router Libraries

قمنا ببناء هذه المكتبات لإنتاج مكتبات I2P router لدينا. وهي موزّعة على عدة مستودعات متخصّصة لتسهيل المراجعة وجعلها مفيدة لأشخاص آخرين يرغبون في بناء I2P routers تجريبية ومخصّصة.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

حسنًا، هناك مشروع خامل لتطوير [I2P router in C#](https://github.com/PeterZander/i2p-cs) إذا كنت تريد تشغيل I2P على جهاز XBox. يبدو هذا رائعًا فعلاً. إذا لم يكن ذلك خيارك المفضّل أيضًا، يمكنك أن تفعل كما فعل altonen وتطوّر واحدًا جديدًا بالكامل.

### هل ترغب في المشاركة في emissary؟

يمكنك برمجة I2P router لأي سبب كان؛ فهي شبكة حرة، لكن سيساعدك أن تعرف لماذا. هل هناك مجتمع تريد تمكينه، أو أداة تعتقد أنها ملائمة لـ I2P، أو إستراتيجية تريد تجربتها؟ حدّد هدفك لتعرف من أين ينبغي أن تبدأ، وما الشكل الذي ستكون عليه حالة "مكتملة".

### Decide what language you want to do it in and why

إليك بعض الأسباب التي قد تجعلك تختار لغة:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

ولكن إليك بعض الأسباب التي قد تجعلك لا تختار تلك اللغات:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

هناك مئات من لغات البرمجة، ونرحب بمكتبات I2P وrouters التي تتم صيانتها في كل منها. اختر مفاضلاتك بحكمة وابدأ.

## go-i2p يقترب من الاكتمال

سواء أردت العمل بـ Rust، Go، Java، C++ أو أي لغة أخرى، فتواصل معنا على #i2p-dev على Irc2P. ابدأ من هناك، وسنرشدك إلى قنوات خاصة بـ router (المُوجّه في I2P). نحن موجودون أيضًا على ramble.i2p في f/i2p، وعلى reddit في r/i2p، وكذلك على GitHub و git.idk.i2p. نتطلع إلى التواصل معك قريبًا.
