---
title: "بروتوكولات التشفير ما بعد الكمي"
aliases:
  - "/proposals/169-pq-crypto"
  - "/proposals/169-pq-crypto/"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "فتح"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### الحالة

| البروتوكول / الميزة | الحالة |
|--------------------|--------|
| Ratchet | مكتمل في Java I2P و i2pd |
| NTCP2 | بيتا الربع الأول 2026 |
| SSU2 | بدء التنفيذ قريباً، بيتا الربع الثالث 2026 |
| MLDSA SigTypes | أولوية منخفضة، على الأرجح 2027+ |
## نظرة عامة

بينما استمر البحث والمنافسة للحصول على تشفير ما بعد الكم (PQ) المناسب لعقد من الزمن، لم تصبح الخيارات واضحة حتى وقت قريب.

بدأنا في النظر إلى تأثيرات التشفير المقاوم للكم (PQ crypto) في عام 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

أضافت معايير TLS دعم التشفير المختلط في العامين الماضيين وأصبحت الآن تُستخدم لجزء كبير من حركة البيانات المشفرة على الإنترنت بسبب الدعم في Chrome و Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

نشر NIST مؤخراً ووضع اللمسات الأخيرة على الخوارزميات الموصى بها لتشفير ما بعد الكم [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). تدعم العديد من مكتبات التشفير الشائعة الآن معايير NIST أو ستصدر دعماً لها في المستقبل القريب.

كل من [Cloudflare](https://blog.cloudflare.com/pq-2024/) و [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) يوصيان ببدء الهجرة فوراً. انظر أيضاً الأسئلة الشائعة حول PQ من NSA لعام 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). يجب أن يكون I2P رائداً في الأمان والتشفير. الآن هو الوقت المناسب لتطبيق الخوارزميات الموصى بها. باستخدام نظام نوع التشفير المرن ونظام نوع التوقيع لدينا، سنضيف أنواعاً للتشفير الهجين، وللتوقيعات PQ والهجينة.

## الأهداف

- اختيار خوارزميات مقاومة للحوسبة الكمية
- إضافة خوارزميات الحوسبة الكمية فقط والمختلطة إلى بروتوكولات I2P حيث يكون ذلك مناسباً
- تعريف متغيرات متعددة
- اختيار أفضل المتغيرات بعد التنفيذ والاختبار والتحليل والبحث
- إضافة الدعم تدريجياً ومع التوافق مع الإصدارات السابقة

## الأهداف غير المرغوبة

- لا تغيّر بروتوكولات التشفير أحادية الاتجاه (Noise N)
- لا تتخلّ عن SHA256، غير مهدد قريباً بواسطة PQ
- لا تختر المتغيرات المفضلة النهائية في هذا الوقت

## نموذج التهديد

- أجهزة router في OBEP أو IBGW، قد تتواطأ،
  تخزن رسائل garlic للفك اللاحق (السرية الأمامية)
- مراقبو الشبكة
  يخزنون رسائل النقل للفك اللاحق (السرية الأمامية)
- مشاركو الشبكة يزورون التوقيعات لـ RI، LS، streaming، datagrams،
  أو هياكل أخرى

## البروتوكولات المتأثرة

سنقوم بتعديل البروتوكولات التالية، تقريباً بحسب ترتيب التطوير. من المحتمل أن يكون الإطلاق الشامل من أواخر 2025 حتى منتصف 2027. راجع قسم الأولويات والإطلاق أدناه للحصول على التفاصيل.

| البروتوكول / الميزة | الحالة |
|--------------------|--------|
| Hybrid MLKEM Ratchet و LS | معتمد 2025-06؛ تجريبي 2025-08؛ إصدار 2025-11 |
| Hybrid MLKEM NTCP2 | تم اختباره على الشبكة المباشرة، معتمد 2026-02؛ هدف تجريبي 2026-05؛ هدف إصدار 2026-08 |
| Hybrid MLKEM SSU2 | معتمد 2026-02؛ هدف تجريبي 2026-08؛ هدف إصدار 2026-11 |
| MLDSA SigTypes 12-14 | الاقتراح مستقر ولكن قد لا يتم الانتهاء منه حتى 2027 |
| MLDSA Dests | تم اختباره على الشبكة المباشرة، يتطلب ترقية الشبكة لدعم floodfill |
| Hybrid SigTypes 15-17 | أولي |
| Hybrid Dests | |
## التصميم

سندعم معايير NIST FIPS 203 و 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) والتي تستند إلى، ولكنها غير متوافقة مع، CRYSTALS-Kyber و CRYSTALS-Dilithium (الإصدارات 3.1، 3، والإصدارات الأقدم).

### تبادل المفاتيح

سندعم تبادل المفاتيح المختلط في البروتوكولات التالية:

| البروتوكول | نوع Noise | دعم PQ فقط؟ | دعم الهجين؟ |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | لا               | نعم             |
| SSU2    | XK         | لا               | نعم             |
| Ratchet | IK         | لا               | نعم             |
| TBM     | N          | لا               | لا              |
| NetDB   | N          | لا               | لا              |
PQ KEM يوفر مفاتيح مؤقتة فقط، ولا يدعم بشكل مباشر عمليات المصافحة بالمفاتيح الثابتة مثل Noise XK و IK.

Noise N لا يستخدم تبادل مفاتيح ثنائي الاتجاه ولذلك فهو غير مناسب للتشفير المختلط.

لذلك سندعم التشفير الهجين فقط، لـ NTCP2 و SSU2 و Ratchet. سنحدد متغيرات ML-KEM الثلاثة كما هو موضح في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)، لإجمالي 3 أنواع تشفير جديدة. ستُحدد الأنواع الهجينة فقط بالتركيب مع X25519.

أنواع التشفير الجديدة هي:

| النوع | الكود |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
ستكون النفقات العامة كبيرة. أحجام الرسائل النموذجية 1 و 2 (لـ XK و IK) تبلغ حالياً حوالي 100 بايت (قبل أي حمولة إضافية). وهذا سيزداد بمقدار 8 إلى 15 مرة حسب الخوارزمية.

### التوقيعات

سندعم التوقيعات PQ والهجينة في الهياكل التالية:

لذلك سندعم التوقيعات PQ-only والهجينة معاً. سنحدد المتغيرات الثلاثة لـ ML-DSA كما هو موضح في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)، وثلاثة متغيرات هجينة مع Ed25519، وثلاثة متغيرات PQ-only مع prehash لملفات SU3 فقط، ليصبح إجمالي أنواع التوقيعات الجديدة 9 أنواع. الأنواع الهجينة ستُحدد فقط بالتحالف مع Ed25519. سنستخدم ML-DSA القياسي، وليس متغيرات pre-hash (HashML-DSA)، باستثناء ملفات SU3.

| النوع | يدعم PQ فقط؟ | يدعم Hybrid؟ |
|------|------------------|-----------------|
| RouterInfo | نعم | نعم |
| LeaseSet | نعم | نعم |
| Streaming SYN/SYNACK/Close | نعم | نعم |
| Repliable Datagrams | نعم | نعم |
| Datagram2 (prop. 163) | نعم | نعم |
| I2CP create session msg | نعم | نعم |
| SU3 files | نعم | نعم |
| X.509 certificates | نعم | نعم |
| Java keystores | نعم | نعم |
سنستخدم متغير التوقيع "المحوط" أو العشوائي، وليس المتغير "الحتمي"، كما هو محدد في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) القسم 3.4. هذا يضمن أن كل توقيع مختلف، حتى عند التوقيع على نفس البيانات، ويوفر حماية إضافية ضد هجمات القنوات الجانبية. راجع قسم ملاحظات التنفيذ أدناه لتفاصيل إضافية حول خيارات الخوارزمية بما في ذلك التشفير والسياق.

أنواع التوقيع الجديدة هي:

شهادات X.509 والتشفيرات الأخرى بصيغة DER ستستخدم الهياكل المركبة ومعرفات الكائنات المحددة في [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| النوع | الكود |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
ستكون النفقات العامة كبيرة. أحجام هوية الوجهة والموجه النموذجية لـ Ed25519 هي 391 بايت. ستزيد هذه بمقدار 3.5 إلى 6.8 مرة اعتماداً على الخوارزمية. توقيعات Ed25519 تبلغ 64 بايت. ستزيد هذه بمقدار 38 إلى 76 مرة اعتماداً على الخوارزمية. RouterInfo الموقعة النموذجية وleaseSet والرسائل المرسلة القابلة للرد ورسائل التدفق الموقعة تبلغ حوالي 1 كيلوبايت. ستزيد هذه بمقدار 3 إلى 8 مرات اعتماداً على الخوارزمية.

نظراً لأن أنواع الهوية الجديدة للوجهة و router لن تحتوي على حشو، فلن تكون قابلة للضغط. أحجام الوجهات وهويات router التي يتم ضغطها بـ gzip أثناء النقل ستزداد بـ 12 إلى 38 مرة حسب الخوارزمية المستخدمة.

بالنسبة للوجهات، أنواع التوقيع الجديدة مدعومة مع جميع أنواع التشفير في leaseset. اضبط نوع التشفير في شهادة المفتاح إلى NONE (255).

### التركيبات القانونية

بالنسبة لـ RouterIdentities، نوع التشفير ElGamal أصبح مهجوراً. أنواع التوقيع الجديدة مدعومة فقط مع تشفير X25519 (النوع 4). أنواع التشفير الجديدة سيتم الإشارة إليها في RouterAddresses. نوع التشفير في شهادة المفتاح سيستمر في كونه النوع 4.

متجهات الاختبار لـ SHA3-256 و SHAKE128 و SHAKE256 متوفرة في [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### مطلوب تشفير جديد

- ML-KEM (سابقاً CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (سابقاً CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (سابقاً Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) يُستخدم فقط لـ SHAKE128
- SHA3-256 (سابقاً Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 و SHAKE256 (امتدادات XOF لـ SHA3-128 و SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

لاحظ أن مكتبة Java bouncycastle تدعم جميع ما سبق. دعم مكتبة C++ متوفر في OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

لن ندعم [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)، فهو أبطأ بكثير وأكبر من ML-DSA. لن ندعم FIPS206 القادم (Falcon)، فهو لم يُوحد بعد. لن ندعم NTRU أو مرشحي التشفير الكمومي الآخرين الذين لم يتم توحيدهم من قبل NIST.

### البدائل

هناك بعض البحوث [الأكاديمية](https://eprint.iacr.org/2020/379.pdf) حول تكييف Wireguard (IK) للتشفير المقاوم للكم الخالص، ولكن توجد عدة أسئلة مفتوحة في تلك الورقة. لاحقاً، تم تنفيذ هذا النهج باسم Rosenpass [Rosenpass](https://rosenpass.eu/) [الورقة البيضاء](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) لـ PQ Wireguard.

### Rosenpass

يستخدم Rosenpass مصافحة تشبه Noise KK مع مفاتيح ثابتة مُشاركة مسبقًا من Classic McEliece 460896 (500 كيلوبايت لكل منها) ومفاتيح مؤقتة من Kyber-512 (في الأساس MLKEM-512). نظرًا لأن النصوص المشفرة لـ Classic McEliece تبلغ 188 بايت فقط، ومفاتيح Kyber-512 العامة والنصوص المشفرة معقولة الحجم، فإن كلا رسالتي المصافحة تناسبان MTU قياسي لـ UDP. يُستخدم المفتاح المُشارك المُخرج (osk) من مصافحة PQ KK كمفتاح مُشارك مسبقًا مُدخل (psk) لمصافحة Wireguard IK القياسية. لذا هناك مصافحتان كاملتان في المجموع، واحدة PQ خالصة وأخرى X25519 خالصة.

لا يمكننا فعل أي من هذا لاستبدال مصافحات XK و IK الخاصة بنا لأن:

هناك الكثير من المعلومات المفيدة في الورقة البحثية، وسوف نراجعها للحصول على الأفكار والإلهام. مُؤجل.

- لا يمكننا القيام بـ KK، بوب لا يملك المفتاح الثابت لأليس
- المفاتيح الثابتة بحجم 500KB كبيرة جداً
- لا نريد رحلة إضافية ذهاباً وإياباً

حدّث الأقسام والجداول في وثيقة الهياكل المشتركة [/docs/specs/common-structures/](/docs/specs/common-structures/) كما يلي:

## المواصفة

### الهياكل الشائعة

أنواع المفاتيح العامة الجديدة هي:

#### المشاكل

المفاتيح العامة الهجينة هي مفتاح X25519. مفاتيح KEM العامة هي المفتاح PQ المؤقت المرسل من Alice إلى Bob. يتم تعريف التشفير وترتيب البايتات في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| النوع | طول المفتاح العام | منذ | الاستخدام |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM512 | 800 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM768 | 1184 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM1024 | 1568 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM512_CT | 768 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | راجع المقترح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| NONE | 0 | 0.9.xx | راجع المقترح 169، للوجهات مع أنواع التوقيع PQ فقط، وليس لـ RIs أو Leasesets |
مفاتيح MLKEM*_CT ليست مفاتيح عامة حقيقية، بل هي "النص المشفر" المرسل من Bob إلى Alice في مصافحة Noise. تم إدراجها هنا من أجل الاكتمال.

أنواع المفاتيح الخاصة الجديدة هي:

#### المفتاح الخاص

المفاتيح الخاصة المختلطة هي مفاتيح X25519. مفاتيح KEM الخاصة مخصصة لـ Alice فقط. يتم تعريف ترميز KEM وترتيب البايت في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| النوع | طول المفتاح الخاص | منذ | الاستخدام |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | راجع الاقتراح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | راجع الاقتراح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | راجع الاقتراح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM512 | 1632 | 0.9.xx | راجع الاقتراح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM768 | 2400 | 0.9.xx | راجع الاقتراح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
| MLKEM1024 | 3168 | 0.9.xx | راجع الاقتراح 169، للمصافحات فقط، وليس لـ Leasesets أو RIs أو Destinations |
أنواع مفاتيح التوقيع العامة الجديدة هي:

#### SigningPublicKey

مفاتيح التوقيع العامة المختلطة هي مفتاح Ed25519 متبوعاً بمفتاح PQ، كما هو موضح في [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). يتم تعريف التشفير وترتيب البايت في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| النوع | الطول (بايت) | منذ | الاستخدام |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65 | 1952 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87 | 2592 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44ph | 1344 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb |
| MLDSA65ph | 1984 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb |
| MLDSA87ph | 2624 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb |
أنواع مفاتيح التوقيع الخاصة الجديدة هي:

#### SigningPrivateKey

مفاتيح التوقيع الخاصة الهجينة هي مفتاح Ed25519 متبوعاً بمفتاح PQ، كما هو محدد في [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). التشفير وترتيب البايت معرفان في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| النوع | الطول (بايت) | منذ | الاستخدام |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65 | 4032 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87 | 4896 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44ph | 2592 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb. انظر الاقتراح 169 |
| MLDSA65ph | 4064 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb. انظر الاقتراح 169 |
| MLDSA87ph | 4928 | 0.9.xx | فقط لملفات SU3، وليس لهياكل netDb. انظر الاقتراح 169 |
أنواع التوقيع الجديدة هي:

التوقيعات الهجينة هي توقيع Ed25519 متبوعًا بتوقيع PQ، كما هو موضح في [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). يتم التحقق من التوقيعات الهجينة عن طريق التحقق من كلا التوقيعين، والفشل إذا فشل أي منهما. التشفير وترتيب البايتات محددان في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### التوقيع

أنواع مفاتيح التوقيع العامة الجديدة هي:

| النوع | الطول (بايت) | منذ | الاستخدام |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65 | 3309 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87 | 4627 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | انظر الاقتراح 169 |
| MLDSA44ph | 2484 | 0.9.xx | لملفات SU3 فقط، وليس لهياكل netDb. انظر الاقتراح 169 |
| MLDSA65ph | 3373 | 0.9.xx | لملفات SU3 فقط، وليس لهياكل netDb. انظر الاقتراح 169 |
| MLDSA87ph | 4691 | 0.9.xx | لملفات SU3 فقط، وليس لهياكل netDb. انظر الاقتراح 169 |
أنواع مفاتيح التشفير العامة الجديدة هي:

#### شهادات المفاتيح

مفاتيح التوقيع العامة المختلطة هي مفتاح Ed25519 متبوعاً بمفتاح PQ، كما هو موضح في [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). يتم تعريف التشفير وترتيب البايت في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| النوع | كود النوع | إجمالي طول المفتاح العام | منذ | الاستخدام |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | انظر المقترح 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | انظر المقترح 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | انظر المقترح 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | انظر المقترح 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | انظر المقترح 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | انظر المقترح 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | فقط لملفات SU3 |
| MLDSA65ph | 19 | n/a | 0.9.xx | فقط لملفات SU3 |
| MLDSA87ph | 20 | n/a | 0.9.xx | فقط لملفات SU3 |
بالنسبة للوجهات التي تحتوي على أنواع توقيع Hybrid أو PQ، استخدم NONE (النوع 255) لنوع التشفير، ولكن لا يوجد مفتاح تشفير، والقسم الرئيسي بالكامل البالغ 384 بايت مخصص لمفتاح التوقيع.

| النوع | رمز النوع | إجمالي طول المفتاح العام | منذ | الاستخدام |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | راجع المقترح 169، لـ Leasesets فقط، وليس لـ RIs أو Destinations |
| NONE | 255 | 0 | 0.9.xx | راجع المقترح 169 |
أنواع المفاتيح المختلطة لا يتم تضمينها أبداً في شهادات المفاتيح؛ فقط في leasesets.

لا توجد حشوة. الطول الإجمالي هو 7 + إجمالي طول المفتاح. طول شهادة المفتاح هو 4 + طول المفتاح الإضافي.

#### أحجام الوجهات

إليكم الأطوال للأنواع الجديدة من Destination. نوع التشفير لجميعها هو NONE (النوع 255) وطول مفتاح التشفير يُعامل كـ 0. يُستخدم القسم بالكامل البالغ 384 بايت للجزء الأول من مفتاح التوقيع العام. ملاحظة: هذا يختلف عن المواصفات لأنواع التوقيع ECDSA_SHA512_P521 وRSA، حيث حافظنا على مفتاح ElGamal بحجم 256 بايت في الوجهة رغم أنه لم يكن مُستخدماً.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

مثال على تدفق البايتات للوجهة بحجم 1319 بايت لـ MLDSA44:

مثال على تدفق بايت هوية الـ router بحجم 1351 بايت لـ MLDSA44:

| النوع | رمز النوع | إجمالي طول المفتاح العام | الرئيسي | الزائد | إجمالي طول الوجهة |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### أحجام RouterIdent

إليكم الأطوال لأنواع الوجهات الجديدة. نوع التشفير للجميع هو X25519 (النوع 4). يتم استخدام القسم بأكمله البالغ 352 بايت بعد المفتاح العام X28819 للجزء الأول من مفتاح التوقيع العام. لا توجد حشوة. الطول الإجمالي هو 39 + الطول الإجمالي للمفتاح. طول شهادة المفتاح هو 4 + طول المفتاح الإضافي.

تستخدم المصافحات أنماط مصافحة [Noise Protocol](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| النوع | رمز النوع | طول المفتاح العام الإجمالي | الرئيسي | الزائد | طول RouterIdent الإجمالي |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### المفتاح العام

التعديلات التالية على XK و IK للسرية الأمامية الهجينة (hfs) محددة كما هو موضح في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 5:

يتم تعريف نمط e1 كما يلي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

#### KDF للـ split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### معرفات Noise

نمط ekem1 معرّف كما يلي، كما هو محدد في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1ب) تنسيق الجلسة الجديد (مع الربط)

يطبق هذا القسم على كل من بروتوكولي IK و XK.

### أنماط المصافحة

المصافحة المختلطة معرّفة في [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). الرسالة الأولى، من أليس إلى بوب، تحتوي على e1، مفتاح التغليف، قبل حمولة الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدعي EncryptAndHash() عليه (كأليس) أو DecryptAndHash() (كبوب). ثم قم بمعالجة حمولة الرسالة كالمعتاد.

يتم استخدام تخطيط الحروف التالي:

- e = مفتاح مؤقت لمرة واحدة
- s = مفتاح ثابت
- p = حمولة الرسالة
- e1 = مفتاح PQ مؤقت لمرة واحدة، يُرسل من Alice إلى Bob
- ekem1 = نص KEM المشفر، يُرسل من Bob إلى Alice

نحن نحدد الوظائف التالية المقابلة للكتل البنائية التشفيرية المستخدمة كما هو محدد في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
(encap_key, decap_key) = PQ_KEYGEN()

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise Handshake KDF

#### 1ب) تنسيق الجلسة الجديد (مع الربط)

- هل يجب أن نغير دالة hash الخاصة بالـ handshake؟ انظر [المقارنة](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 ليس عرضة للـ PQ، ولكن إذا كنا نريد ترقية
  دالة الـ hash الخاصة بنا، فهذا هو الوقت المناسب، بينما نقوم بتغيير أشياء أخرى.
  اقتراح IETF SSH الحالي [مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) هو استخدام MLKEM768
  مع SHA256، و MLKEM1024 مع SHA384. يتضمن ذلك الاقتراح
  مناقشة للاعتبارات الأمنية.
- هل يجب أن نتوقف عن إرسال بيانات ratchet للـ 0-RTT (بخلاف الـ LS)؟
- هل يجب أن ننتقل بالـ ratchet من IK إلى XK إذا لم نرسل بيانات 0-RTT؟

#### نظرة عامة

kem_shared_key = DECAPS(ciphertext, decap_key)

لاحظ أن كلاً من encap_key والنص المشفر مُشفران داخل كتل ChaCha/Poly في رسائل مصافحة Noise 1 و 2. سيتم فك تشفيرهما كجزء من عملية المصافحة.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1، النص المشفر، قبل حمولة الرسالة. يتم التعامل معها كمفتاح ثابت إضافي؛ استدعِ EncryptAndHash() عليها (كـ Bob) أو DecryptAndHash() (كـ Alice). ثم، احسب kem_shared_key واستدعِ MixKey(kem_shared_key). ثم قم بمعالجة حمولة الرسالة كالمعتاد.

#### عمليات ML-KEM المحددة

بالنسبة لـ XK: بعد نمط الرسالة 'es' وقبل الحمولة، أضف:

أو

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

بالنسبة لـ IK: بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

لـ XK: بعد نمط الرسالة 'es' وقبل الحمولة، أضف:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

أو

يتم خلط kem_shared_key في مفتاح التسلسل باستخدام MixHash(). انظر أدناه للتفاصيل.

#### Alice KDF للرسالة 1

بالنسبة لـ XK: بعد نمط الرسالة 'ee' وقبل الحمولة، أضف:

أو

لـ IK: بعد نمط الرسالة 'ee' وقبل نمط الرسالة 'se'، أضف:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF للرسالة 1

بالنسبة لـ XK: بعد نمط الرسالة 'ee' وقبل الحمولة، أضف:

أو

للـ IK: بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF للرسالة 2

تحديث مواصفات ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) كما يلي:

أو

التنسيق المشفر:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF للرسالة 2

بعد نمط الرسالة 'ee' (وقبل نمط الرسالة 'ss' لـ IK)، أضف:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF للرسالة 3 (XK فقط)

غير متغير

#### معرفات Noise

غير متغير

### آلية التدوير (Ratchet)

التغييرات: ratchet الحالي يحتوي على حمولة فارغة للقسم الأول من ChaCha، والحمولة في القسم الثاني. مع ML-KEM، هناك الآن ثلاثة أقسام. يحتوي القسم الأول على النص المشفر PQ المشفر. القسم الثاني يحتوي على حمولة فارغة. القسم الثالث يحتوي على الحمولة.

#### عنوان طويل

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### رأس قصير

التغييرات: احتوى الـ ratchet الحالي على المفتاح الثابت في قسم ChaCha الأول، والحمولة في القسم الثاني. مع ML-KEM، أصبح هناك ثلاثة أقسام الآن. يحتوي القسم الأول على المفتاح العام PQ المشفر. يحتوي القسم الثاني على المفتاح الثابت. يحتوي القسم الثالث على الحمولة.

التنسيق المفكوك التشفير:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
التنسيق المفكوك:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
الأحجام:

| النوع | كود النوع | طول X | طول الرسالة 1 | طول الرسالة 1 المشفرة | طول الرسالة 1 المفكوكة | طول مفتاح PQ | طول pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
لاحظ أن الحمولة يجب أن تحتوي على كتلة DateTime، لذا فإن الحد الأدنى لحجم الحمولة هو 7. يمكن حساب الأحجام الدنيا للرسالة 1 وفقاً لذلك.

#### 1g) تنسيق رد الجلسة الجديدة

التغييرات: NTCP2 الحالي يحتوي فقط على الخيارات في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام PQ المشفر.

التنسيق المشفر:

```
  +----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
التنسيق المفكوك:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
الأحجام:

| النوع | كود النوع | طول Y | طول الرسالة 2 | طول تشفير الرسالة 2 | طول فك تشفير الرسالة 2 | طول PQ CT | طول opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
لاحظ أنه بينما ستحتوي الرسالة 2 عادةً على حمولة غير صفرية، فإن مواصفات ratchet [/docs/specs/ecies/](/docs/specs/ecies/) لا تتطلب ذلك، لذا فإن الحد الأدنى لحجم الحمولة هو 0. يمكن حساب الحد الأدنى لأحجام الرسالة 2 وفقاً لذلك.

### NTCP2

حديث مواصفات NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) كما يلي:

#### معرفات الضوضاء

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

المحتويات الخام:

حتى يمكن دعم PQ وغير-PQ NTCP2 على نفس عنوان وميناء router، نستخدم البت الأكثر أهمية من قيمة X (مفتاح X25519 العام المؤقت) لتمييز أنه اتصال PQ. هذا البت غير مُعيّن دائماً للاتصالات غير-PQ.

ملاحظة: يجب تعيين حقل الإصدار في كتلة خيارات الرسالة 1 إلى 2، حتى لاتصالات PQ.

بالنسبة لبوب، بعد إلغاء التشويش AES للـ X، اختبر X[31] & 0x80. إذا كانت البت مضبوطة، امحها باستخدام X[31] &= 0x7f، وفك التشفير عبر Noise كاتصال PQ. إذا كانت البت غير مضبوطة، فك التشفير عبر Noise كاتصال غير PQ كالمعتاد.

بالنسبة لـ PQ NTCP2 المُعلن عنه على عنوان router ومنفذ مختلف، هذا غير مطلوب.

للحصول على معلومات إضافية، راجع قسم العناوين المنشورة أدناه.

البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين router.

الأحجام:

| النوع | رمز النوع | طول X | طول الرسالة 1 | طول الرسالة 1 المشفرة | طول الرسالة 1 المفكوكة | طول مفتاح PQ | طول الخيارات |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

#### 2) SessionCreated

المحتويات الخام:

البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
الأحجام:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
الأحجام:

| النوع | رمز النوع | طول Y | طول Msg 2 | طول Msg 2 المشفّر | طول Msg 2 المفكوك | طول PQ CT | طول opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

#### 3) SessionConfirmed

غير متغير

#### دالة اشتقاق المفتاح (KDF) (لمرحلة البيانات)

غير متغير

#### العناوين المنشورة

في جميع الحالات، استخدم اسم نقل NTCP2 كالمعتاد.

استخدم نفس العنوان/المنفذ المستخدم في non-PQ وغير المحجوب بجدار ناري. يُدعم متغير PQ واحد فقط. في عنوان router، انشر v=2 (كالمعتاد) والمعامل الجديد pq=[3|4|5] للإشارة إلى MLKEM 512/768/1024. تضبط Alice الـ MSB الخاص بالمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال هجين. انظر أعلاه. ستتجاهل routers الأقدم المعامل pq وتتصل بطريقة non-pq كالمعتاد.

العناوين المحمية بجدار حماية (لا يتم نشر IP): في عنوان الـ router، انشر v=2 (كالمعتاد). لا حاجة لنشر معامل pq.

قد تتصل Alice بـ PQ Bob باستخدام متغير PQ الذي ينشره Bob، سواء كانت Alice تعلن عن دعم pq في معلومات router الخاصة بها أم لا، أو ما إذا كانت تعلن عن نفس المتغير.

في المواصفات الحالية، تم تعريف الرسائل 1 و 2 لتحتوي على كمية "معقولة" من الحشو، مع نطاق موصى به من 0-31 بايت، وبدون تحديد حد أقصى.

#### أقصى حشو

حتى API 0.9.68 (الإصدار 2.11.0)، طبّق Java I2P حد أقصى قدره 256 بايت من الحشو للاتصالات غير PQ، لكن هذا لم يكن موثقاً سابقاً. اعتباراً من API 0.9.69 (الإصدار 2.12.0)، يطبق Java I2P نفس الحد الأقصى للحشو في الاتصالات غير PQ كما هو الحال في MLKEM-512. انظر الجدول أدناه.

استخدم حجم الرسالة المحدد كحد أقصى للحشو، أي أن الحد الأقصى للحشو سيضاعف حجم الرسالة لاتصالات PQ، كما يلي:

استخدم حجم الرسالة المحدد كحد أقصى للحشو، أي أن الحد الأقصى للحشو سيضاعف حجم الرسالة في اتصالات PQ، كما يلي:

| الحد الأقصى لحشو الرسالة | غير-PQ (حتى 0.9.68) | غير-PQ (اعتباراً من 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

لاحظ أن MLKEM-1024 غير مدعوم في SSU2، حيث أن المفاتيح كبيرة جداً ولا يمكن احتواؤها ضمن datagram قياسي بحجم 1500 بايت.

#### معرفات الضوضاء

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

الرأسية الطويلة هي 32 بايت. تُستخدم قبل إنشاء الجلسة، لطلب الرمز المميز، وطلب الجلسة، وإنشاء الجلسة، وإعادة المحاولة. كما تُستخدم أيضاً لرسائل اختبار النظير وثقب الجدار الناري خارج الجلسة.

#### السرية الأمامية

في الرسائل التالية، قم بتعيين حقل ver (الإصدار) في الرأس الطويل إلى 3 أو 4، للإشارة إلى MLKEM-512 أو MLKEM-768.

في الرسائل التالية، اضبط حقل ver (الإصدار) في الرأس الطويل على 2، كالمعتاد، حتى لو كان MLKEM-512 أو MLKEM-768 مدعوماً. يمكن للتطبيقات أيضاً ضبط القيمة على 3 أو 4، إذا كان الطرف الآخر يدعم ذلك، لكن هذا ليس ضرورياً. يجب على التطبيقات قبول أي قيمة من 2-4.

- (0) طلب الجلسة
- (1) تم إنشاء الجلسة
- (9) إعادة المحاولة
- (10) طلب الرمز المميز
- (11) ثقب الاتصال

البيانات غير المشفرة (علامة مصادقة Poly1305 غير معروضة):

- (7) اختبار النظير (رسائل خارج الجلسة 5-7)

الأحجام، لا تشمل النفقات العامة لـ IP:

- طلب التتابع
- استجابة التتابع
- تقديم التتابع
- اختبار النظير

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

بدون تغيير

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### حجم الجلسة الجديدة

غير متغير

#### SessionRequest (النوع 0)

تغيير KDF لحماية الانتحال: لمعالجة المشاكل المثارة في الاقتراح 165 [Prop165]_، ولكن بحل مختلف، نقوم بتعديل KDF لطلب الجلسة. هذا فقط لجلسات PQ. يبقى KDF للجلسات غير PQ بدون تغيير.

المحتويات الخام:

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
الحد الأدنى لـ MTU لـ MLKEM768_X25519: 1318 لـ IPv4 و 1338 لـ IPv6. انظر أدناه.

| النوع | كود النوع | طول X | طول الرسالة 1 | طول الرسالة 1 المشفر | طول الرسالة 1 المفكك | طول مفتاح PQ | طول pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | غير متاح | كبير جداً | | | | |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

التغييرات: SSU2 الحالي يحتوي فقط على بيانات الكتلة في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام PQ المشفر.

البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

#### SessionCreated (النوع 1)

المحتويات الخام:

البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
الأحجام:

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
الأحجام، لا تتضمن الحمولة الإضافية لـ IP:

| النوع | رمز النوع | طول Y | طول Msg 2 | طول Msg 2 المشفّر | طول Msg 2 المفكوك | طول PQ CT | طول pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | كبير جدًا | | | | |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

التغييرات: SSU2 الحالي يحتوي فقط على بيانات الكتلة في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام PQ المشفر.

توقيعات PQ: تحتوي كتل Relay وكتل Peer Test ورسائل Peer Test جميعها على توقيعات. للأسف، توقيعات PQ أكبر من MTU. لا توجد آلية حالية لتجزئة كتل Relay أو Peer Test أو الرسائل عبر حزم UDP متعددة. يجب توسيع البروتوكول لدعم التجزئة. سيتم ذلك في اقتراح منفصل سيحدد لاحقاً. حتى اكتمال ذلك، لن يتم دعم Relay و Peer Test.

#### SessionConfirmed (النوع 2)

غير متغير

#### KDF لمرحلة البيانات

غير متغير

#### اختبار الترحيل والنظير

الكتل التالية تحتوي على حقول الإصدار. ستبقى الإصدار 2 (للتوافق مع Bob غير-PQ)، ولن تتغير إلى الإصدار 3/4 للـ PQ.

- SAMv3
- Bittorrent
- إرشادات المطورين
- التسمية / دفتر العناوين / خوادم القفز
- مستندات أخرى

في جميع الحالات، استخدم اسم نقل SSU2 كالمعتاد. MLKEM-1024 غير مدعوم.

#### العناوين المنشورة

استخدم نفس العنوان/المنفذ كما في حالة عدم استخدام PQ وعدم وجود جدار ناري. يتم دعم واحد أو كلا من متغيرات PQ. في عنوان الـ router، انشر v=2 (كالمعتاد) والمعامل الجديد pq=[3|4|3,4|4,3] للإشارة إلى MLKEM 512/768/كلاهما. الـ routers التي لديها MTU أقل من الحد الأدنى المحدد أدناه يجب ألا تنشر معامل "pq" يحتوي على "4". انشر 4,3 للإشارة إلى تفضيل MLKEM-768 أو 3,4 للإشارة إلى تفضيل MLKEM-512. الإصدار الفعلي متروك للمبادِر، وقد لا يتم احترام التفضيل. الـ routers التي لديها MTU أقل من الحد الأدنى المحدد أدناه يجب ألا تتصل باستخدام MLKEM768. الـ routers الأقدم ستتجاهل معامل pq وتتصل بدون PQ كالمعتاد.

استخدم الحذر لعدم تجاوز MTU مع MLKEM768. الحد الأدنى لـ MTU لـ MLKEM768_X25519 هو 1318 لـ IPv4 و 1338 لـ IPv6 (بافتراض حد أدنى للحمولة يبلغ 10 بايت مع كتلة DateTime وكتلة Padding أو RelayTagRequest). الحد الأدنى لـ MTU لـ SSU2 بشكل عام هو 1280، لذلك قد لا تستخدم جميع العقد MLKEM768. لا تنشر أو تستخدم MLKEM768 إذا كان MTU الفعلي أقل من الحد الأدنى، سواء محلياً أو كما يعلن عنه النظير. احذر من تضمين حجم حشو بحيث تتجاوز الرسالة 1 أو 2 MTU المحلي أو البعيد.

العناوين المحمية بجدار الحماية (لا يتم نشر IP): في عنوان الـ router، انشر v=2 (كالمعتاد). يجب نشر معامل pq في العناوين المحمية بجدار الحماية، لدعم التتابع.

يمكن لأليس الاتصال بـ Bob باستخدام PQ من خلال متغير PQ الذي ينشره Bob، سواء كانت أليس تعلن عن دعم pq في معلومات router الخاص بها أم لا، أو ما إذا كانت تعلن عن نفس المتغير.

في المواصفات الحالية، تم تعريف الرسائل 1 و 2 لتحتوي على كمية "معقولة" من الحشو، مع نطاق موصى به من 0-31 بايت، وبدون تحديد حد أقصى.

#### MTU

يمكننا استخدام حقل الإصدار داخلياً واستخدام 3 لـ MLKEM512 و 4 لـ MLKEM768.

### البث المباشر

بالنسبة للرسائل 1 و 2، فإن MLKEM768 سيزيد من أحجام الحزم لتتجاوز الحد الأدنى لـ MTU وهو 1280. من المحتمل أن لا ندعمه لذلك الاتصال إذا كان MTU منخفضاً جداً.

### ملفات SU3

بالنسبة للرسائل 1 و2، فإن MLKEM1024 سيزيد أحجام الحزم إلى ما يتجاوز الحد الأقصى للـ MTU البالغ 1500. هذا سيتطلب تجزئة الرسائل 1 و2، وسيكون تعقيداً كبيراً. من المحتمل أن لا نفعل ذلك.

Relay وPeer Test: انظر أعلاه

TODO: هل توجد طريقة أكثر كفاءة لتعريف التوقيع/التحقق لتجنب نسخ التوقيع؟

مطلوب إنجازه

[مسودة IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) القسم 8.1 تمنع HashML-DSA في شهادات X.509 ولا تخصص OIDs لـ HashML-DSA، بسبب تعقيدات التنفيذ وانخفاض الأمان.

### مواصفات أخرى

سيكون الحد الأقصى الجديد لحجم Destination هو 2599 (3468 في base 64).

لاحظ أننا نمنع توقيع Ed25519 لملفات SU3، وبينما حددنا توقيع Ed25519ph، لم نتفق أبداً على OID له، أو نستخدمه.

- إذا كانت الرسالة 1 أقل من 919 بايت، فهي بروتوكول ratchet الحالي.
- إذا كانت الرسالة 1 أكبر من أو تساوي 919 بايت، فمن المحتمل أن تكون MLKEM512_X25519.
  جرب MLKEM512_X25519 أولاً، وإذا فشل، جرب بروتوكول ratchet الحالي.

## تحليل النفقات العامة

### تبادل المفاتيح

أنواع التوقيع العادية غير مسموحة لملفات SU3؛ استخدم متغيرات ph (prehash).

| النوع | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
سيكون الحد الأقصى الجديد لحجم الوجهة 2599 (3468 في base 64).

تحديث الوثائق الأخرى التي تقدم إرشادات حول أحجام الوجهات، بما في ذلك:

| النوع | السرعة النسبية |
|------|----------------|
| X25519 DH/keygen | خط الأساس |
| MLKEM512 | أسرع بـ 2.25 مرة |
| MLKEM768 | أسرع بـ 1.5 مرة |
| MLKEM1024 | 1x (نفس السرعة) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = أبطأ بنسبة 22% |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = أبطأ بنسبة 32% |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = أبطأ بنسبة 50% |
زيادة الحجم (بايت):

| النوع | DH/encaps النسبي | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | خط الأساس | خط الأساس | خط الأساس |
| MLKEM512 | أسرع بـ 29 مرة | أسرع بـ 22 مرة | أسرع بـ 17 مرة |
| MLKEM768 | أسرع بـ 17 مرة | أسرع بـ 14 مرة | أسرع بـ 9 مرات |
| MLKEM1024 | أسرع بـ 12 مرة | أسرع بـ 10 مرات | أسرع بـ 6 مرات |
### التوقيعات

#### الأحجام

السرعات كما تم الإبلاغ عنها من قبل [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| النوع | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (كل رسالة) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | خط الأساس | خط الأساس |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### السرعات

تحديث الوثائق الأخرى التي تقدم إرشادات حول أحجام الوجهات، بما في ذلك:

| النوع | علامة السرعة النسبية | التحقق |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | خط الأساس | خط الأساس |
| MLDSA44 | أبطأ بـ 5 مرات | أسرع بمرتين |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
زيادة الحجم (بايت):

| النوع | علامة السرعة النسبية | التحقق | إنتاج المفتاح |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | خط الأساس | خط الأساس | خط الأساس |
| MLDSA44 | أبطأ 4.6 مرة | أسرع 1.7 مرة | أسرع 2.6 مرة |
| MLDSA65 | أبطأ 8.1 مرة | نفس السرعة | أسرع 1.5 مرة |
| MLDSA87 | أبطأ 11.1 مرة | أبطأ 1.5 مرة | نفس السرعة |
## تحليل الأمان

أحجام المفاتيح النموذجية، التوقيع، RIdent، Dest أو زيادات الحجم (Ed25519 مُدرج للمرجع) بافتراض نوع التشفير X25519 لـ RIs. الحجم المُضاف لـ Router Info، LeaseSet، البيانات القابلة للرد، وكل من حزمتي التدفق (SYN و SYN ACK) المدرجتين. Destinations و Leasesets الحالية تحتوي على حشو متكرر وقابلة للضغط أثناء النقل. الأنواع الجديدة لا تحتوي على حشو ولن تكون قابلة للضغط، مما يؤدي إلى زيادة حجم أعلى بكثير أثناء النقل. انظر قسم التصميم أعلاه.

| الفئة | مستوى الأمان |
|-------|-------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### المصافحات

السرعات كما تم الإبلاغ عنها من قبل [Cloudflare](https://blog.cloudflare.com/pq-2024/):

نتائج الاختبار الأولية في Java:

| الخوارزمية | فئة الأمان |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### التوقيعات

تم تلخيص فئات الأمان في NIST في [عرض NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) الشريحة 10. المعايير الأولية: يجب أن تكون الحد الأدنى لفئة أمان NIST لدينا 2 للبروتوكولات المختلطة و 3 للبروتوكولات PQ فقط.

هذه جميعها بروتوكولات مختلطة. يجب على التطبيقات تفضيل MLKEM768؛ MLKEM512 ليس آمناً بما فيه الكفاية.

| الخوارزمية | فئة الأمان |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## تفضيلات النوع

فئات الأمان NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

يحدد هذا الاقتراح أنواع التوقيع الهجينة والتي تعتمد على التشفير المقاوم للحوسبة الكمية فقط. MLDSA44 الهجين أفضل من MLDSA65 المقاوم للحوسبة الكمية فقط. أحجام المفاتيح والتوقيعات لـ MLDSA65 و MLDSA87 كبيرة جداً بالنسبة لنا، على الأقل في البداية.

فئات الأمان NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

بينما سنقوم بتعريف وتنفيذ 3 أنواع تشفير و9 أنواع توقيع، نخطط لقياس الأداء أثناء التطوير، وتحليل تأثيرات زيادة أحجام الهياكل بشكل أعمق. سنستمر أيضاً في البحث ومراقبة التطورات في المشاريع والبروتوكولات الأخرى.

بعد عام أو أكثر من التطوير، سنحاول الاستقرار على نوع مفضل أو افتراضي لكل حالة استخدام. سيتطلب الاختيار عمل مقايضات بين عرض النطاق الترددي ووحدة المعالجة المركزية ومستوى الأمان المقدر. قد لا تكون جميع الأنواع مناسبة أو مسموحة لجميع حالات الاستخدام.

التفضيلات الأولية كما يلي، وهي عرضة للتغيير:

التشفير: MLKEM768_X25519

## ملاحظات التطبيق

### دعم المكتبة

التواقيع: MLDSA44_EdDSA_SHA512_Ed25519

القيود الأولية كما يلي، وقابلة للتغيير:

### متغيرات التوقيع

التشفير: MLKEM1024_X25519 غير مسموح لـ SSU2

التوقيعات: MLDSA87 والمتغير الهجين كبيران جداً على الأرجح؛ MLDSA65 والمتغير الهجين قد يكونان كبيرين جداً

### الموثوقية

مكتبات Bouncycastle و BoringSSL و WolfSSL تدعم MLKEM و MLDSA الآن. دعم OpenSSL سيكون في الإصدار 3.5 في 8 أبريل 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### أحجام الهياكل

مكتبة Noise الخاصة بـ southernstorm.com والمُعدلة بواسطة Java I2P احتوت على دعم أولي للمصافحات المختلطة، لكننا أزلناها لعدم استخدامها؛ سيتوجب علينا إضافتها مرة أخرى وتحديثها لتتطابق مع [مواصفات Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### NetDB

سوف نستخدم النوع "المحمي" أو العشوائي للتوقيع، وليس النوع "الحتمي"، كما هو معرّف في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) القسم 3.4. هذا يضمن أن كل توقيع مختلف، حتى لو كان على نفس البيانات، ويوفر حماية إضافية ضد هجمات القنوات الجانبية. بينما يحدد [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) أن النوع "المحمي" هو الافتراضي، قد يكون هذا صحيحاً أو لا في مختلف المكتبات. يجب على المطورين التأكد من استخدام النوع "المحمي" للتوقيع.

### آلية التدوير (Ratchet)

#### المشاكل

نحن نستخدم عملية التوقيع العادية (تسمى Pure ML-DSA Signature Generation) والتي تُشفر الرسالة داخلياً كـ 0x00 || len(ctx) || ctx || message، حيث ctx هو قيمة اختيارية بحجم 0x00..0xFF. نحن لا نستخدم أي سياق اختياري. len(ctx) == 0. هذه العملية معرّفة في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10 وAlgorithm 3 step 5. لاحظ أن بعض test vectors المنشورة قد تتطلب تعيين وضع حيث لا يتم تشفير الرسالة.

زيادة الحجم ستؤدي إلى تجزئة أكبر بكثير للـ tunnel بالنسبة لمخازن NetDB ومصافحات التدفق والرسائل الأخرى. تحقق من تغييرات الأداء والموثوقية.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

اعثر على وتحقق من أي كود يحد من حجم البايت لمعلومات router وleasesets.

مراجعة وإمكانية تقليل الحد الأقصى لـ LS/RI المخزنة في ذاكرة الوصول العشوائي أو على القرص، لحد زيادة التخزين. زيادة الحد الأدنى لمتطلبات النطاق الترددي لـ floodfills؟

- أكثر من MLKEM واحد
- ElG + واحد أو أكثر من MLKEM
- X25519 + واحد أو أكثر من MLKEM
- ElG + X25519 + واحد أو أكثر من MLKEM

يجب أن يكون التصنيف/الكشف التلقائي لبروتوكولات متعددة على نفس الـ tunnels ممكناً بناءً على فحص طول الرسالة 1 (New Session Message). باستخدام MLKEM512_X25519 كمثال، طول الرسالة 1 أكبر بـ 816 بايت من بروتوكول ratchet الحالي، والحد الأدنى لحجم الرسالة 1 (مع تضمين حمولة DateTime فقط) هو 919 بايت. معظم أحجام الرسالة 1 مع ratchet الحالي لها حمولة أقل من 816 بايت، لذا يمكن تصنيفها كـ non-hybrid ratchet. الرسائل الكبيرة هي على الأرجح POSTs والتي تعتبر نادرة.

- اختيار Noise Hash - البقاء مع SHA256 أم الترقية؟
  SHA256 يجب أن يكون جيداً لـ 20-30 سنة أخرى، غير مهدد بـ PQ،
  انظر [عرض NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) و [عرض NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  إذا تم كسر SHA256 فلدينا مشاكل أسوأ (netdb).
- NTCP2 منفذ منفصل، عنوان router منفصل
- SSU2 relay / اختبار النظير
- حقل إصدار SSU2
- إصدار عنوان router في SSU2

لذا فإن الاستراتيجية الموصى بها هي:

هذا يجب أن يسمح لنا بدعم standard ratchet و hybrid ratchet بكفاءة على نفس الوجهة، تماماً كما دعمنا سابقاً ElGamal و ratchet على نفس الوجهة. لذلك، يمكننا الانتقال إلى بروتوكول MLKEM hybrid بسرعة أكبر مما لو لم نتمكن من دعم البروتوكولات المزدوجة لنفس الوجهة، لأنه يمكننا إضافة دعم MLKEM للوجهات الموجودة.

التركيبات المطلوبة المدعومة هي:

التركيبات التالية قد تكون معقدة، وليس مطلوباً دعمها، ولكن قد يتم ذلك، حسب التنفيذ:

#### الأنفاق المشتركة

قد لا نحاول دعم خوارزميات MLKEM متعددة (على سبيل المثال، MLKEM512_X25519 و MLKEM_768_X25519) على نفس الوجهة. اختر واحداً فقط؛ ومع ذلك، يعتمد ذلك على اختيارنا لمتغير MLKEM مفضل، حتى تتمكن أنفاق عميل HTTP من استخدام واحد. يعتمد على التنفيذ.

#### حجم الجلسة الجديدة

قد نحاول دعم ثلاث خوارزميات (على سبيل المثال X25519، MLKEM512_X25519، و MLKEM769_X25519) على نفس الوجهة. قد تكون استراتيجية التصنيف وإعادة المحاولة معقدة جداً. قد يكون التكوين وواجهة المستخدم للتكوين معقدين جداً. يعتمد على التنفيذ.

### NTCP2

من المحتمل ألا نحاول دعم خوارزميات ElGamal والخوارزميات المختلطة على نفس الوجهة. ElGamal عفا عليه الزمن، و ElGamal + مختلط فقط (بدون X25519) لا يبدو منطقياً. أيضاً، رسائل الجلسة الجديدة لـ ElGamal والمختلطة كبيرة الحجم، لذا استراتيجيات التصنيف ستضطر غالباً لمحاولة كلا عمليتي فك التشفير، مما سيكون غير فعال. يعتمد على التنفيذ.

#### التعتيم

يمكن للعملاء استخدام نفس مفاتيح X25519 الثابتة أو مفاتيح مختلفة لبروتوكولات X25519 والهجينة على نفس الأنفاق، حسب التنفيذ.

مواصفات ECIES تسمح برسائل garlic في حمولة New Session Message، مما يسمح بتسليم 0-RTT للحزمة الأولى من التدفق، عادة HTTP GET، مع leaseSet الخاص بالعميل. ومع ذلك، حمولة New Session Message لا تتمتع بالسرية المستقبلية. نظرًا لأن هذا الاقتراح يؤكد على تعزيز السرية المستقبلية لـ ratchet، قد تؤجل التطبيقات أو يجب أن تؤجل تضمين حمولة التدفق، أو رسالة التدفق الكاملة، حتى أول رسالة Existing Session Message. هذا سيكون على حساب تسليم 0-RTT. قد تعتمد الاستراتيجيات أيضًا على نوع حركة البيانات أو نوع tunnel، أو على GET مقابل POST، على سبيل المثال. يعتمد على التطبيق.

استخدام MLKEM أو MLDSA أو كليهما على نفس الوجهة، سيزيد بشكل كبير من حجم رسالة الجلسة الجديدة، كما هو موضح أعلاه. قد يؤدي هذا إلى انخفاض كبير في موثوقية تسليم رسالة الجلسة الجديدة عبر الأنفاق، حيث يجب تقسيمها إلى رسائل نفق متعددة بحجم 1024 بايت. نجاح التسليم يتناسب مع العدد الأسي للشظايا. قد تستخدم التطبيقات استراتيجيات متنوعة للحد من حجم الرسالة، على حساب تسليم 0-RTT. يعتمد على التطبيق.

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

### SSU2

نقوم بتعيين البت الأكثر أهمية (MSB) للمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال هجين. هذا يسمح لنا بتشغيل كل من NTCP القياسي و NTCP الهجين على نفس المنفذ. سيتم دعم متغير هجين واحد فقط، والإعلان عنه في عنوان router. على سبيل المثال، v=2,3 أو v=2,4 أو v=2,5.

كـ Bob، اختبر إذا كان (X[31] & 0x80) != 0 بعد إزالة التشويش. إذا كان الأمر كذلك، فهو اتصال PQ.

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

## توافق Router

### أسماء النقل

إصدار router الأدنى المطلوب لـ NTCP2-PQ سيتم تحديده لاحقاً.

### أنواع تشفير Router

نستخدم حقل الإصدار في الرأس الطويل ونضعه على 3 لـ MLKEM512 و 4 لـ MLKEM768. v=2,3,4 في العنوان سيكون كافياً.

#### التشويش

تحقق وأكد أن SSU2 يمكنه التعامل مع RI موقع بـ MLDSA ومجزأ عبر حزم متعددة (6-8؟).

#### أجهزة التوجيه من النوع 5/6/7

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

#### أجهزة Router من النوع 4

في جميع الحالات، استخدم أسماء النقل NTCP2 و SSU2 كالمعتاد.

### أنواع توقيعات Router

#### التوصيات

لدينا عدة بدائل للنظر فيها:

غير موصى به. استخدم فقط أنواع النقل الجديدة المذكورة أعلاه التي تطابق نوع الـ router. الـ routers الأقدم لا يمكنها الاتصال أو بناء tunnels من خلالها أو إرسال رسائل netDb إليها. سيتطلب عدة دورات إصدار لتصحيح الأخطاء وضمان الدعم قبل التفعيل افتراضياً. قد يؤدي إلى تمديد فترة النشر بسنة أو أكثر مقارنة بالبدائل أدناه.

### أنواع تشفير LS

#### أجهزة Router من النوع 12-17

موصى به. حيث أن PQ لا تؤثر على المفتاح الثابت X25519 أو بروتوكولات المصافحة N، يمكننا ترك الـ routers كنوع 4، والإعلان عن transports جديدة فقط. الـ routers الأقدم يمكنها لا تزال الاتصال، وبناء tunnels من خلالها، أو إرسال رسائل netDb إليها.

يُوصى باستخدام MLKEM-768 للـ Ratchet وNTCP2 وSSU2، كونه أفضل توازن بين الأمان وطول المفتاح.

### أنواع توقيع الوجهة

#### مفاتيح LS من النوع 5-7

أجهزة router الأقدم تتحقق من RIs وبالتالي لا يمكنها الاتصال أو بناء tunnels من خلالها أو إرسال رسائل netDb إليها. سيتطلب الأمر عدة دورات إصدار لتصحيح الأخطاء وضمان الدعم قبل التمكين افتراضياً. ستكون نفس المشاكل التي واجهناها في طرح نوع التشفير 5/6/7؛ قد يمتد الطرح لسنة أو أكثر مقارنة ببديل طرح نوع التشفير 4 المذكور أعلاه.

غير موصى به. استخدم فقط أنواع النقل الجديدة المذكورة أعلاه التي تطابق نوع الـ router. الـ routers الأقدم لا يمكنها الاتصال أو بناء tunnels من خلالها أو إرسال رسائل netDb إليها. سيتطلب عدة دورات إصدار لتصحيح الأخطاء وضمان الدعم قبل التفعيل افتراضياً. قد يؤدي إلى تمديد فترة النشر بسنة أو أكثر مقارنة بالبدائل أدناه.

## الأولويات والطرح

لا توجد بدائل.

يمكن للوجهات دعم أنواع مفاتيح متعددة، ولكن فقط عن طريق إجراء تجارب فك تشفير للرسالة 1 مع كل مفتاح. يمكن تخفيف هذا العبء الإضافي من خلال الاحتفاظ بعدادات لعمليات فك التشفير الناجحة لكل مفتاح، وتجربة المفتاح الأكثر استخداماً أولاً. تستخدم Java I2P هذه الاستراتيجية لـ ElGamal+X25519 على نفس الوجهة.

تقوم routers بالتحقق من توقيعات leaseset ولذلك لا يمكنها الاتصال أو استقبال leasesets للوجهات من نوع 12-17. سيتطلب الأمر عدة دورات إصدار لتصحيح الأخطاء وضمان الدعم قبل التمكين افتراضياً.

لا توجد بدائل.

البيانات الأكثر قيمة هي حركة المرور من طرف إلى طرف، المشفرة باستخدام ratchet. كمراقب خارجي بين قفزات tunnel، تكون مشفرة مرتين إضافيتين، مع تشفير tunnel وتشفير النقل. كمراقب خارجي بين OBEP وIBGW، تكون مشفرة مرة واحدة إضافية فقط، مع تشفير النقل. كمشارك OBEP أو IBGW، يكون ratchet هو التشفير الوحيد. ومع ذلك، نظراً لأن tunnels أحادية الاتجاه، فإن التقاط كلا الرسالتين في مصافحة ratchet سيتطلب routers متواطئة، ما لم يتم بناء tunnels مع OBEP وIBGW على نفس router.

نموذج التهديد PQ لكسر مفاتيح المصادقة في فترة زمنية معقولة (لنقل بضعة أشهر) ثم انتحال هوية المصادقة أو فك التشفير في الوقت شبه الفوري، هو أبعد بكثير؟ وهذا هو الوقت الذي نرغب فيه في الانتقال إلى مفاتيح PQC الثابتة.

تم تعليق العمل على دعم توقيع MLDSA في I2P حتى أواخر عام 2027 أو 2028، انتظارًا لإكمال الهيئات القياسية لاختيار الخوارزميات، وربما تقليل أحجام المفاتيح و/أو التوقيعات، وتعزيز تبني الصناعة لها. انظر [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)، و[COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)، و[PLANTS](https://datatracker.ietf.org/wg/plants/about/). أيضًا، سيكون تبني MLDSA في الصناعة معياريًا من خلال IETF ومنتدى CA/Browser وسلطات الشهادات. تحتاج سلطات الشهادات أولًا إلى دعم وحدات الأمان المادية (HSM)، والذي لا يتوفر حاليًا [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). نتوقع أن تقود IETF ومنتدى CA/Browser القرارات المتعلقة باختيارات المعلمات المحددة، بما في ذلك ما إذا كانت ستدعم أو تشترط التوقيعات المركبة [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| المعلم الهام | الهدف |
|-----------|--------|
| Ratchet beta | أواخر 2025 |
| اختيار أفضل نوع تشفير | أوائل 2026 |
| NTCP2 beta | أوائل 2026 |
| SSU2 beta | منتصف 2026 |
| Ratchet production | منتصف 2026 |
| Ratchet افتراضي | أواخر 2026 |
| Signature beta | أواخر 2026 |
| NTCP2 production | أواخر 2026 |
| SSU2 production | أوائل 2027 |
| اختيار أفضل نوع توقيع | أوائل 2027 |
| NTCP2 افتراضي | أوائل 2027 |
| SSU2 افتراضي | منتصف 2027 |
| Signature production | منتصف 2027 |
## الترحيل

Ratchet له الأولوية العليا. وسائل النقل تأتي بعد ذلك. التوقيعات لها أقل أولوية.

سيكون طرح التوقيع أيضاً متأخراً بعام أو أكثر عن طرح التشفير، لأن التوافق العكسي غير ممكن. كما أن اعتماد MLDSA في الصناعة سيتم توحيده من قبل منتدى CA/Browser وسلطات الشهادات. تحتاج سلطات الشهادات أولاً إلى دعم وحدة الأمان الأجهزة (HSM)، والذي غير متوفر حالياً [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). نتوقع أن يقود منتدى CA/Browser القرارات حول اختيارات المعايير المحددة، بما في ذلك ما إذا كان سيتم دعم أو طلب التوقيعات المركبة [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## المشاكل

يُتوقع أن تظل خوارزمية SHA256 آمنة لفترة أخرى تتراوح بين 20 إلى 30 عامًا، ولا تهددها الحوسبة الكمية ما بعد الكيوبتات (PQ)، انظر [عرض NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) و[عرض NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). إذا تم كسر SHA256، فسنواجه مشكلات أخطر بكثير (مثل تلف قاعدة البيانات الشبكية netDb).

## المراجع

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
