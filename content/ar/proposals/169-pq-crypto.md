---
title: "بروتوكولات التشفير لما بعد الكم"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "مفتوح"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## نظرة عامة

بينما كانت الأبحاث والمنافسة على تشفير ما بعد الكم (PQ) المناسب تسير لمدة عقد من الزمن، لم تصبح الخيارات واضحة حتى وقت قريب.

بدأنا في النظر إلى تداعيات التشفير المقاوم للكم في عام 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

أضافت معايير TLS دعم التشفير الهجين في العامين الماضيين وهي تُستخدم الآن لجزء كبير من حركة البيانات المشفرة على الإنترنت بسبب الدعم في Chrome و Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

أصدر معهد NIST مؤخراً ونشر الخوارزميات الموصى بها للتشفير ما بعد الكمي [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). تدعم عدة مكتبات تشفير شائعة الآن معايير NIST أو ستصدر الدعم في المستقبل القريب.

كل من [Cloudflare](https://blog.cloudflare.com/pq-2024/) و [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) يوصيان ببدء الهجرة فوراً. انظر أيضاً الأسئلة الشائعة لـ NSA PQ لعام 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). يجب أن يكون I2P رائداً في الأمان والتشفير. الآن هو الوقت المناسب لتنفيذ الخوارزميات الموصى بها. باستخدام نظام نوع التشفير المرن ونظام نوع التوقيع لدينا، سنضيف أنواعاً للتشفير الهجين، وللـ PQ والتوقيعات الهجينة.

## الأهداف

- اختيار الخوارزميات المقاومة لـ PQ
- إضافة خوارزميات PQ-only والهجينة إلى بروتوكولات I2P حيثما كان ذلك مناسباً
- تحديد متغيرات متعددة
- اختيار أفضل المتغيرات بعد التنفيذ والاختبار والتحليل والبحث
- إضافة الدعم تدريجياً ومع التوافق مع الإصدارات السابقة

## الأهداف غير المحددة

- لا تغير بروتوكولات التشفير أحادية الاتجاه (Noise N)
- لا تتخل عن SHA256، غير مهدد على المدى القريب بواسطة PQ
- لا تختر المتغيرات المفضلة النهائية في هذا الوقت

## نموذج التهديد

- أجهزة router في OBEP أو IBGW، التي قد تتواطأ،
  لتخزين رسائل garlic للفك اللاحق (forward secrecy)
- مراقبو الشبكة
  الذين يخزنون رسائل النقل للفك اللاحق (forward secrecy)
- مشاركو الشبكة الذين يزورون التوقيعات لـ RI أو LS أو streaming أو datagrams،
  أو هياكل أخرى

## البروتوكولات المتأثرة

سنقوم بتعديل البروتوكولات التالية، تقريباً بترتيب التطوير. الطرح الشامل سيكون على الأرجح من أواخر 2025 حتى منتصف 2027. راجع قسم الأولويات والطرح أدناه للتفاصيل.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## التصميم

سندعم معايير NIST FIPS 203 و 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) والتي تستند إلى، ولكنها غير متوافقة مع، CRYSTALS-Kyber و CRYSTALS-Dilithium (الإصدارات 3.1، 3، والإصدارات الأقدم).

### Key Exchange

سوف ندعم تبادل المفاتيح المختلط في البروتوكولات التالية:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
يوفر PQ KEM المفاتيح المؤقتة فقط، ولا يدعم بشكل مباشر مصافحات المفاتيح الثابتة مثل Noise XK و IK.

Noise N لا يستخدم تبادل مفاتيح ثنائي الاتجاه وبالتالي فهو غير مناسب للتشفير المختلط.

لذلك سنقوم بدعم التشفير المختلط فقط، لـ NTCP2 و SSU2 و Ratchet. سنقوم بتعريف متغيرات ML-KEM الثلاثة كما هو موضح في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)، لإجمالي 3 أنواع تشفير جديدة. الأنواع المختلطة ستُعرّف فقط بالاقتران مع X25519.

أنواع التشفير الجديدة هي:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
النفقات الإضافية ستكون كبيرة. أحجام الرسائل النموذجية 1 و 2 (لـ XK و IK) تبلغ حاليًا حوالي 100 بايت (قبل أي حمولة إضافية). هذا سيزيد بمقدار 8 إلى 15 مرة حسب الخوارزمية.

### Signatures

سوف ندعم توقيعات PQ والتوقيعات المختلطة في الهياكل التالية:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
لذلك سندعم التوقيعات PQ-only والهجينة على حد سواء. سنحدد المتغيرات الثلاثة لـ ML-DSA كما هو موضح في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)، وثلاثة متغيرات هجينة مع Ed25519، وثلاثة متغيرات PQ-only مع prehash لملفات SU3 فقط، بإجمالي 9 أنواع توقيع جديدة. ستُحدد الأنواع الهجينة فقط بالتركيب مع Ed25519. سنستخدم ML-DSA المعياري، وليس متغيرات pre-hash (HashML-DSA)، باستثناء ملفات SU3.

سنستخدم متغير التوقيع "المُحوَّط" أو العشوائي، وليس المتغير "الحتمي"، كما هو محدد في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) القسم 3.4. هذا يضمن أن كل توقيع مختلف، حتى عند التوقيع على نفس البيانات، ويوفر حماية إضافية ضد هجمات القنوات الجانبية. راجع قسم ملاحظات التنفيذ أدناه للحصول على تفاصيل إضافية حول اختيارات الخوارزمية بما في ذلك التشفير والسياق.

أنواع التوقيع الجديدة هي:

| Type | Code |
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
شهادات X.509 وترميزات DER الأخرى ستستخدم البُنى المركبة ومعرفات الكائنات المحددة في [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

الحمولة الإضافية ستكون كبيرة. أحجام الوجهة النموذجية Ed25519 وهوية router هي 391 بايت. ستزيد هذه بمقدار 3.5x إلى 6.8x حسب الخوارزمية. توقيعات Ed25519 هي 64 بايت. ستزيد هذه بمقدار 38x إلى 76x حسب الخوارزمية. RouterInfo الموقع، وLeaseSet، والرسائل القابلة للرد، ورسائل التدفق الموقعة النموذجية تبلغ حوالي 1KB. ستزيد هذه بمقدار 3x إلى 8x حسب الخوارزمية.

نظرًا لأن أنواع هوية الوجهة والـ router الجديدة لن تحتوي على حشو، فلن تكون قابلة للضغط. أحجام الوجهات وهويات الـ router المضغوطة بـ gzip أثناء النقل ستزداد بمقدار 12 إلى 38 مرة حسب الخوارزمية.

### Legal Combinations

بالنسبة للوجهات (Destinations)، أنواع التوقيع الجديدة مدعومة مع جميع أنواع التشفير في الـ leaseset. قم بتعيين نوع التشفير في شهادة المفتاح إلى NONE (255).

بالنسبة لـ RouterIdentities، نوع تشفير ElGamal مهجور. أنواع التوقيع الجديدة مدعومة مع تشفير X25519 (النوع 4) فقط. ستُشار إلى أنواع التشفير الجديدة في RouterAddresses. سيستمر نوع التشفير في شهادة المفتاح كونه النوع 4.

### New Crypto Required

- ML-KEM (المعروف سابقاً باسم CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (المعروف سابقاً باسم CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (المعروف سابقاً باسم Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) يُستخدم فقط مع SHAKE128
- SHA3-256 (المعروف سابقاً باسم Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 و SHAKE256 (امتدادات XOF لـ SHA3-128 و SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

متجهات الاختبار لـ SHA3-256 و SHAKE128 و SHAKE256 متوفرة في [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

لاحظ أن مكتبة Java bouncycastle تدعم جميع ما سبق. دعم مكتبة C++ متوفر في OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

لن ندعم [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)، فهو أبطأ بكثير وأكبر من ML-DSA. لن ندعم FIPS206 القادم (Falcon)، لأنه لم يتم توحيده معياريًا بعد. لن ندعم NTRU أو مرشحي PQ الآخرين الذين لم يتم توحيدهم معياريًا من قبل NIST.

### Rosenpass

هناك بعض الأبحاث [paper](https://eprint.iacr.org/2020/379.pdf) حول تكييف Wireguard (IK) للتشفير PQ الخالص، ولكن توجد عدة أسئلة مفتوحة في تلك الورقة. لاحقاً، تم تنفيذ هذا النهج باسم Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) لـ PQ Wireguard.

يستخدم Rosenpass مصافحة مشابهة لـ Noise KK مع مفاتيح Classic McEliece 460896 ثابتة مُشتركة مسبقاً (500 كيلوبايت لكل منها) ومفاتيح Kyber-512 (في الأساس MLKEM-512) مؤقتة. نظراً لأن النصوص المشفرة لـ Classic McEliece تبلغ 188 بايت فقط، ومفاتيح Kyber-512 العامة والنصوص المشفرة معقولة، فإن كلا رسائل المصافحة تتسع في MTU قياسي لـ UDP. يُستخدم المفتاح المشترك الناتج (osk) من مصافحة PQ KK كمفتاح مُشارك مسبقاً مدخل (psk) لمصافحة Wireguard IK القياسية. لذلك هناك مصافحتان كاملتان إجمالاً، واحدة PQ خالصة وأخرى X25519 خالصة.

لا يمكننا فعل أي من هذا لاستبدال مصافحات XK و IK الخاصة بنا لأن:

- لا يمكننا القيام بـ KK، Bob لا يملك المفتاح الثابت الخاص بـ Alice
- المفاتيح الثابتة بحجم 500KB كبيرة جداً
- لا نريد رحلة ذهاب وإياب إضافية

هناك الكثير من المعلومات المفيدة في الورقة البيضاء، وسنقوم بمراجعتها للحصول على أفكار وإلهام. TODO.

## Specification

### تبادل المفاتيح

قم بتحديث الأقسام والجداول في وثيقة الهياكل المشتركة [/docs/specs/common-structures/](/docs/specs/common-structures/) كما يلي:

### التوقيعات

أنواع المفاتيح العامة الجديدة هي:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
المفاتيح العامة الهجينة هي مفتاح X25519. مفاتيح KEM العامة هي مفتاح PQ المؤقت المرسل من Alice إلى Bob. التشفير وترتيب البايتات محددان في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

مفاتيح MLKEM*_CT ليست في الواقع مفاتيح عامة، بل هي "النص المشفر" المرسل من Bob إلى Alice في مصافحة Noise. تم إدراجها هنا للاكتمال.

### التركيبات القانونية

أنواع المفاتيح الخاصة الجديدة هي:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
المفاتيح الخاصة الهجينة هي مفاتيح X25519. مفاتيح KEM الخاصة مخصصة لـ Alice فقط. تشفير KEM وترتيب البايتات محددان في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### مطلوب تشفير جديد

أنواع مفاتيح التوقيع العامة الجديدة هي:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
المفاتيح العامة الهجينة للتوقيع هي مفتاح Ed25519 متبوعًا بمفتاح PQ، كما هو موضح في [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). يتم تعريف التشفير وترتيب البايتات في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### البدائل

أنواع مفاتيح التوقيع الخاصة الجديدة هي:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
المفاتيح الخاصة للتوقيع الهجين هي مفتاح Ed25519 متبوعاً بمفتاح PQ، كما هو موضح في [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). التشفير وترتيب البايت محددان في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

أنواع التوقيع الجديدة هي:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
التوقيعات الهجينة هي توقيع Ed25519 متبوعاً بتوقيع PQ، كما هو موضح في [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). يتم التحقق من التوقيعات الهجينة عن طريق التحقق من كلا التوقيعين، والفشل في حالة فشل أي منهما. التشفير وترتيب البايت محددان في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

أنواع مفاتيح التوقيع العامة الجديدة هي:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
أنواع المفاتيح العامة المشفرة الجديدة هي:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
أنواع المفاتيح الهجينة لا تُدرج أبداً في شهادات المفاتيح؛ فقط في leasesets.

بالنسبة للوجهات التي تحتوي على أنواع توقيع Hybrid أو PQ، استخدم NONE (النوع 255) لنوع التشفير، ولكن لا يوجد مفتاح تشفير، وكامل القسم الرئيسي البالغ 384 بايت مخصص لمفتاح التوقيع.

### الهياكل الشائعة

فيما يلي أطوال أنواع الوجهة الجديدة. نوع التشفير لجميعها هو NONE (النوع 255) وطول مفتاح التشفير يُعامل على أنه 0. يتم استخدام القسم الكامل البالغ 384 بايت للجزء الأول من مفتاح التوقيع العام. ملاحظة: هذا يختلف عن المواصفة لأنواع التوقيع ECDSA_SHA512_P521 و RSA، حيث حافظنا على مفتاح ElGamal بحجم 256 بايت في الوجهة رغم أنه غير مستخدم.

لا توجد حشوة. الطول الإجمالي هو 7 + إجمالي طول المفتاح. طول شهادة المفتاح هو 4 + طول المفتاح الزائد.

مثال على تدفق بايت الوجهة بحجم 1319 بايت لـ MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

إليك أطوال أنواع الوجهة (Destination) الجديدة. نوع التشفير لجميعها هو X25519 (النوع 4). يتم استخدام القسم المكون من 352 بايت بالكامل بعد المفتاح العام X28819 للجزء الأول من مفتاح التوقيع العام. لا توجد حشوة. الطول الإجمالي هو 39 + الطول الإجمالي للمفتاح. طول شهادة المفتاح هو 4 + طول المفتاح الزائد.

مثال على تدفق بايت هوية router بحجم 1351 بايت لـ MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### مفتاح خاص

تستخدم المصافحات أنماط المصافحة من [Noise Protocol](https://noiseprotocol.org/noise.html).

يتم استخدام تخطيط الأحرف التالي:

- e = مفتاح مؤقت لمرة واحدة (one-time ephemeral key)
- s = مفتاح ثابت (static key)
- p = حمولة الرسالة (message payload)
- e1 = مفتاح PQ مؤقت لمرة واحدة، يُرسل من Alice إلى Bob
- ekem1 = نص KEM المشفر، يُرسل من Bob إلى Alice

التعديلات التالية على XK و IK للسرية المستقبلية المختلطة (hfs) كما هو محدد في [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 5:

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
نمط e1 محدد كما يلي، كما هو موضح في [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
يتم تعريف نمط ekem1 كما يلي، كما هو محدد في [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) القسم 4:

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
### مفتاح التوقيع العام

#### Issues

- هل يجب أن نغير دالة hash للمصافحة؟ انظر [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 ليس عرضة لـ PQ، ولكن إذا كنا نريد ترقية
  دالة hash الخاصة بنا، فالآن هو الوقت المناسب، بينما نغير أشياء أخرى.
  اقتراح IETF SSH الحالي [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) هو استخدام MLKEM768
  مع SHA256، و MLKEM1024 مع SHA384. يتضمن هذا الاقتراح
  نقاش حول الاعتبارات الأمنية.
- هل يجب أن نتوقف عن إرسال بيانات ratchet من نوع 0-RTT (غير الـ LS)؟
- هل يجب أن نبدل ratchet من IK إلى XK إذا لم نرسل بيانات 0-RTT؟

#### Overview

يسري هذا القسم على كل من بروتوكولي IK و XK.

يتم تعريف المصافحة الهجين في [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). الرسالة الأولى، من Alice إلى Bob، تحتوي على e1، مفتاح التغليف، قبل حمولة الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدع `EncryptAndHash()` عليه (كـ Alice) أو `DecryptAndHash()` (كـ Bob). ثم قم بمعالجة حمولة الرسالة كالمعتاد.

الرسالة الثانية، من Bob إلى Alice، تحتوي على ekem1، النص المشفر، قبل حمولة الرسالة. يتم التعامل مع هذا كمفتاح ثابت إضافي؛ استدع EncryptAndHash() عليه (كـ Bob) أو DecryptAndHash() (كـ Alice). ثم، احسب kem_shared_key واستدع MixKey(kem_shared_key). ثم عالج حمولة الرسالة كالمعتاد.

#### Defined ML-KEM Operations

نحدد الوظائف التالية المقابلة للعناصر الأساسية للتشفير المستخدمة كما هو محدد في [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

```
(ciphertext, kem_shared_key) = ENCAPS(encap_key)
```

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

لاحظ أن كل من encap_key والنص المشفر محميان بالتشفير داخل كتل ChaCha/Poly في رسائل مصافحة Noise 1 و 2. سيتم فك تشفيرهما كجزء من عملية المصافحة.

يتم خلط ال kem_shared_key في chaining key باستخدام MixHash(). انظر أدناه للتفاصيل.

#### Alice KDF for Message 1

بالنسبة لـ XK: بعد نمط الرسالة 'es' وقبل الحمولة، أضف:

أو

بالنسبة لـ IK: بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

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
#### Bob KDF for Message 1

بالنسبة لـ XK: بعد نمط الرسالة 'es' وقبل الحمولة، أضف:

أو

بالنسبة لـ IK: بعد نمط الرسالة 'es' وقبل نمط الرسالة 's'، أضف:

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
#### Bob KDF for Message 2

بالنسبة لـ XK: بعد نمط الرسالة 'ee' وقبل الحمولة، أضف:

أو

بالنسبة لـ IK: بعد نمط الرسالة 'ee' وقبل نمط الرسالة 'se'، أضف:

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
```
#### Alice KDF for Message 2

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
```
#### KDF for Message 3 (XK only)

دون تغيير

#### KDF for split()

بدون تغيير

### مفتاح التوقيع الخاص

قم بتحديث مواصفات ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) كما يلي:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

التغييرات: احتوى ratchet الحالي على المفتاح الثابت في قسم ChaCha الأول، والحمولة في القسم الثاني. مع ML-KEM، يوجد الآن ثلاثة أقسام. القسم الأول يحتوي على المفتاح العام المُشفر PQ. القسم الثاني يحتوي على المفتاح الثابت. القسم الثالث يحتوي على الحمولة.

التنسيق المشفر:

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
التنسيق المفكوك التشفير:

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

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
لاحظ أن الحمولة يجب أن تحتوي على كتلة DateTime، لذا الحد الأدنى لحجم الحمولة هو 7. يمكن حساب الأحجام الدنيا للرسالة 1 وفقاً لذلك.

#### 1g) New Session Reply format

التغييرات: ratchet الحالي يحتوي على payload فارغ للقسم الأول من ChaCha، والـ payload في القسم الثاني. مع ML-KEM، يوجد الآن ثلاثة أقسام. القسم الأول يحتوي على النص المشفر PQ المشفر. القسم الثاني يحتوي على payload فارغ. القسم الثالث يحتوي على الـ payload.

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
التنسيق المفكوك التشفير:

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
لاحظ أنه بينما ستحتوي الرسالة 2 عادةً على حمولة غير صفرية، فإن مواصفات ratchet [/docs/specs/ecies/](/docs/specs/ecies/) لا تتطلب ذلك، لذا فإن الحد الأدنى لحجم الحمولة هو 0. يمكن حساب الأحجام الدنيا للرسالة 2 وفقاً لذلك.

### التوقيع

قم بتحديث مواصفات NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) كما يلي:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

التغييرات: يحتوي NTCP2 الحالي فقط على الخيارات الموجودة في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام PQ المشفر.

المحتويات الخام:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير مُظهرة):

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
الأحجام:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

#### 2) SessionCreated

التغييرات: يحتوي NTCP2 الحالي على الخيارات الموجودة في قسم ChaCha فقط. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام المشفر PQ.

المحتويات الخام:

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
البيانات غير المشفرة (علامة المصادقة Poly1305 غير معروضة):

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين router.

#### 3) SessionConfirmed

غير متغير

#### Key Derivation Function (KDF) (for data phase)

غير متغير

### شهادات المفاتيح

حدّث مواصفات SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) كما يلي:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

الترويسة الطويلة هي 32 بايت. تُستخدم قبل إنشاء الجلسة، لطلب الرمز المميز، وطلب الجلسة، وإنشاء الجلسة، وإعادة المحاولة. كما تُستخدم أيضًا لرسائل اختبار النظير وثقب الجدار خارج الجلسة.

TODO: يمكننا استخدام حقل الإصدار داخلياً واستخدام 3 لـ MLKEM512 و 4 لـ MLKEM768. هل نفعل ذلك فقط للنوعين 0 و 1 أم لجميع الأنواع الستة؟

قبل تشفير الرأس:

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

بدون تغيير

#### SessionRequest (Type 0)

التغييرات: SSU2 الحالي يحتوي فقط على بيانات الكتلة في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضاً على المفتاح العام المشفر PQ.

المحتويات الخام:

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
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
الأحجام، غير شاملة لأعباء IP الإضافية:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

الحد الأدنى لـ MTU لـ MLKEM768_X25519: حوالي 1316 لـ IPv4 و 1336 لـ IPv6.

#### SessionCreated (Type 1)

التغييرات: يحتوي SSU2 الحالي فقط على بيانات الكتلة في قسم ChaCha. مع ML-KEM، سيحتوي قسم ChaCha أيضًا على المفتاح العام PQ المشفر.

المحتويات الخام:

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
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
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
الأحجام، غير شاملة حمولة IP الإضافية:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين router.

الحد الأدنى لـ MTU لـ MLKEM768_X25519: حوالي 1316 لـ IPv4 و 1336 لـ IPv6.

#### SessionConfirmed (Type 2)

دون تغيير

#### KDF for data phase

بدون تغيير

#### المشاكل

كتل Relay وكتل Peer Test ورسائل Peer Test تحتوي جميعها على توقيعات. لسوء الحظ، توقيعات PQ أكبر من الـ MTU. لا توجد آلية حالية لتجزئة كتل Relay أو Peer Test أو الرسائل عبر حزم UDP متعددة. يجب توسيع البروتوكول لدعم التجزئة. سيتم ذلك في اقتراح منفصل سيتم تحديده لاحقاً. حتى يتم إنجاز ذلك، لن يتم دعم Relay و Peer Test.

#### نظرة عامة

يمكننا استخدام حقل الإصدار داخلياً واستخدام 3 لـ MLKEM512 و 4 لـ MLKEM768.

بالنسبة للرسائل 1 و 2، MLKEM768 سيزيد من أحجام الحزم إلى ما يتجاوز الحد الأدنى لـ MTU وهو 1280. على الأرجح لن ندعمه لذلك الاتصال إذا كان MTU منخفضاً جداً.

بالنسبة للرسائل 1 و 2، فإن MLKEM1024 سيزيد أحجام الحزم إلى ما يتجاوز الحد الأقصى لـ MTU البالغ 1500. هذا سيتطلب تجزئة الرسائل 1 و 2، وسيكون تعقيداً كبيراً. ربما لن نقوم بذلك.

التتابع واختبار النظير: انظر أعلاه

### أحجام الوجهات

TODO: هل توجد طريقة أكثر كفاءة لتعريف التوقيع/التحقق لتجنب نسخ التوقيع؟

### أحجام RouterIdent

قائمة المهام

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) القسم 8.1 يمنع HashML-DSA في شهادات X.509 ولا يخصص OIDs لـ HashML-DSA، بسبب تعقيدات التنفيذ والأمان المنخفض.

بالنسبة للتوقيعات PQ-only لملفات SU3، استخدم معرفات الكائنات (OIDs) المعرّفة في [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) للمتغيرات non-prehash للشهادات. نحن لا نعرّف التوقيعات الهجينة لملفات SU3، لأنه قد يتوجب علينا حساب hash للملفات مرتين (على الرغم من أن HashML-DSA و X2559 يستخدمان نفس دالة hash وهي SHA512). أيضاً، ربط مفتاحين وتوقيعين في شهادة X.509 سيكون غير معياري تماماً.

لاحظ أننا نمنع توقيع Ed25519 لملفات SU3، وبينما قمنا بتعريف توقيع Ed25519ph، لم نتفق أبداً على OID له، أو نستخدمه.

أنواع التوقيع العادية غير مسموحة لملفات SU3؛ استخدم متغيرات ph (prehash).

### أنماط المصافحة

الحد الأقصى الجديد لحجم الوجهة سيكون 2599 (3468 في base 64).

تحديث الوثائق الأخرى التي تقدم إرشادات حول أحجام Destination، بما في ذلك:

- SAMv3
- Bittorrent
- إرشادات المطورين
- التسمية / دفتر العناوين / خوادم القفز
- مستندات أخرى

## Overhead Analysis

### دالة اشتقاق المفاتيح لمصافحة Noise

زيادة الحجم (بايت):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
السرعة:

السرعات كما ورد في [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
نتائج الاختبار الأولية في Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

الحجم:

أحجام المفاتيح النموذجية، التوقيع، RIdent، Dest أو الزيادات في الحجم (Ed25519 مدرج للمرجع) بافتراض نوع تشفير X25519 للـ RIs. الحجم المضاف لـ Router Info، LeaseSet، البيانات القابلة للرد، وكل واحدة من حزمتي streaming (SYN و SYN ACK) المذكورتين. Destinations و Leasesets الحالية تحتوي على padding مكرر وقابلة للضغط أثناء النقل. الأنواع الجديدة لا تحتوي على padding ولن تكون قابلة للضغط، مما يؤدي إلى زيادة أعلى بكثير في الحجم أثناء النقل. انظر قسم التصميم أعلاه.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
السرعة:

السرعات كما أُبلغ عنها من قبل [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
نتائج الاختبارات الأولية في Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

فئات أمان NIST ملخصة في [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) الشريحة 10. المعايير الأولية: الحد الأدنى لفئة أمان NIST يجب أن يكون 2 للبروتوكولات المختلطة و 3 لـ PQ فقط.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

هذه كلها بروتوكولات هجينة. من المحتمل أن نحتاج إلى تفضيل MLKEM768؛ MLKEM512 ليس آمناً بما فيه الكفاية.

فئات أمان NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

يحدد هذا الاقتراح أنواع التوقيع المختلطة وأنواع التوقيع PQ-only. MLDSA44 المختلط أفضل من MLDSA65 PQ-only. أحجام المفاتيح والتوقيعات لـ MLDSA65 و MLDSA87 كبيرة جداً بالنسبة لنا، على الأقل في البداية.

فئات الأمان NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

بينما سنحدد وننفذ 3 أنواع تشفير و9 أنواع توقيع، نخطط لقياس الأداء أثناء التطوير، وتحليل تأثيرات زيادة أحجام البنية بشكل أكبر. سنواصل أيضًا البحث ومراقبة التطورات في المشاريع والبروتوكولات الأخرى.

بعد عام أو أكثر من التطوير، سنحاول الاستقرار على نوع مفضل أو افتراضي لكل حالة استخدام. سيتطلب الاختيار إجراء مقايضات في عرض النطاق الترددي ووحدة المعالجة المركزية ومستوى الأمان المقدر. قد لا تكون جميع الأنواع مناسبة أو مسموحة لجميع حالات الاستخدام.

التفضيلات الأولية كما يلي، وقد تخضع للتغيير:

التشفير: MLKEM768_X25519

التوقيعات: MLDSA44_EdDSA_SHA512_Ed25519

القيود الأولية هي كما يلي، وهي قابلة للتغيير:

التشفير: MLKEM1024_X25519 غير مسموح لـ SSU2

التوقيعات: MLDSA87 والمتغير المختلط كبيرة جداً على الأرجح؛ MLDSA65 والمتغير المختلط قد تكون كبيرة جداً

## Implementation Notes

### Library Support

مكتبات Bouncycastle و BoringSSL و WolfSSL تدعم الآن MLKEM و MLDSA. دعم OpenSSL سيكون في إصدارهم 3.5 في 8 أبريل 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

مكتبة Noise الخاصة بـ southernstorm.com والمُحدثة بواسطة Java I2P احتوت على دعم أولي للمصافحات الهجينة، لكننا أزلناها لعدم استخدامها؛ سيتعين علينا إعادة إضافتها وتحديثها لتتطابق مع [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

سنستخدم المتغير "المحوط" أو العشوائي للتوقيع، وليس المتغير "الحتمي"، كما هو محدد في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) القسم 3.4. هذا يضمن أن كل توقيع مختلف، حتى عندما يكون على نفس البيانات، ويوفر حماية إضافية ضد هجمات القنوات الجانبية. بينما يحدد [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) أن المتغير "المحوط" هو الافتراضي، قد يكون هذا صحيحاً أو غير صحيح في مختلف المكتبات. يجب على المطورين التأكد من استخدام المتغير "المحوط" للتوقيع.

نستخدم عملية التوقيع العادية (تُسمى Pure ML-DSA Signature Generation) والتي تُرمز الرسالة داخلياً كـ 0x00 || len(ctx) || ctx || message، حيث ctx هي قيمة اختيارية بحجم 0x00..0xFF. نحن لا نستخدم أي سياق اختياري. len(ctx) == 0. هذه العملية محددة في [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10 و Algorithm 3 step 5. لاحظ أن بعض متجهات الاختبار المنشورة قد تتطلب تعيين وضع حيث لا يتم ترميز الرسالة.

### Reliability

زيادة الحجم ستؤدي إلى تجزئة tunnel أكثر بكثير لمخازن NetDB، ومصافحات streaming، والرسائل الأخرى. تحقق من تغييرات الأداء والموثوقية.

### Structure Sizes

ابحث عن وتحقق من أي كود يحدد الحجم بالبايت لمعلومات الـ router والـ leasesets.

### NetDB

مراجعة وتقليل الحد الأقصى لـ LS/RI المخزنة في ذاكرة الوصول العشوائي أو على القرص إذا أمكن، للحد من زيادة التخزين. زيادة الحد الأدنى لمتطلبات النطاق الترددي لـ floodfills؟

### Ratchet

#### عمليات ML-KEM المحددة

يجب أن يكون التصنيف/الكشف التلقائي للبروتوكولات المتعددة على نفس tunnels ممكناً بناءً على فحص طول الرسالة 1 (New Session Message). باستخدام MLKEM512_X25519 كمثال، طول الرسالة 1 أكبر بـ 816 بايت من بروتوكول ratchet الحالي، والحد الأدنى لحجم الرسالة 1 (مع تضمين حمولة DateTime فقط) هو 919 بايت. معظم أحجام الرسالة 1 مع ratchet الحالي لديها حمولة أقل من 816 بايت، لذا يمكن تصنيفها كـ non-hybrid ratchet. الرسائل الكبيرة هي على الأرجح POSTs وهي نادرة.

لذا الاستراتيجية الموصى بها هي:

- إذا كانت الرسالة 1 أقل من 919 بايت، فهو بروتوكول ratchet الحالي.
- إذا كانت الرسالة 1 أكبر من أو تساوي 919 بايت، فمن المحتمل أنه MLKEM512_X25519.
  جرب MLKEM512_X25519 أولاً، وإذا فشل، جرب بروتوكول ratchet الحالي.

هذا يجب أن يسمح لنا بدعم standard ratchet و hybrid ratchet بكفاءة على نفس الوجهة، تماماً كما دعمنا سابقاً ElGamal و ratchet على نفس الوجهة. لذلك، يمكننا الانتقال إلى بروتوكول MLKEM hybrid بسرعة أكبر بكثير مما لو لم نتمكن من دعم بروتوكولات مزدوجة لنفس الوجهة، لأننا يمكننا إضافة دعم MLKEM للوجهات الموجودة.

التركيبات المطلوبة المدعومة هي:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

المجموعات التالية قد تكون معقدة، وهي غير مطلوبة للدعم، لكن قد تكون كذلك، حسب التنفيذ:

- أكثر من MLKEM واحد
- ElG + واحد أو أكثر من MLKEM
- X25519 + واحد أو أكثر من MLKEM
- ElG + X25519 + واحد أو أكثر من MLKEM

قد لا نحاول دعم خوارزميات MLKEM متعددة (على سبيل المثال، MLKEM512_X25519 و MLKEM_768_X25519) على نفس الوجهة. اختر واحداً فقط؛ ومع ذلك، يعتمد ذلك على اختيارنا لمتغير MLKEM المفضل، حتى تتمكن أنفاق عميل HTTP من استخدام واحد منها. يعتمد على التنفيذ.

قد نحاول دعم ثلاث خوارزميات (على سبيل المثال X25519 و MLKEM512_X25519 و MLKEM769_X25519) على نفس الوجهة. قد يكون التصنيف واستراتيجية إعادة المحاولة معقدين للغاية. قد يكون التكوين وواجهة المستخدم للتكوين معقدين للغاية. يعتمد على التنفيذ.

على الأرجح لن نحاول دعم خوارزميات ElGamal والخوارزميات الهجينة على نفس الوجهة. ElGamal عفا عليه الزمن، وElGamal + هجين فقط (بدون X25519) لا يبدو منطقياً كثيراً. أيضاً، رسائل الجلسة الجديدة لكل من ElGamal والهجين كبيرة الحجم، لذلك ستحتاج استراتيجيات التصنيف غالباً إلى تجربة فك التشفير لكلا النوعين، مما سيكون غير فعال. يعتمد على التنفيذ.

يمكن للعملاء استخدام نفس مفاتيح X25519 الثابتة أو مفاتيح مختلفة لبروتوكولي X25519 والهجين على نفس الأنفاق، حسب التنفيذ.

#### Alice KDF للرسالة 1

تسمح مواصفة ECIES برسائل Garlic في حمولة New Session Message، مما يتيح تسليم 0-RTT للحزمة الأولى من streaming، عادةً HTTP GET، مع leaseset الخاص بالعميل. ومع ذلك، فإن حمولة New Session Message لا تتمتع بالسرية الأمامية. نظرًا لأن هذا الاقتراح يركز على تعزيز السرية الأمامية لـ ratchet، قد تؤجل التطبيقات أو يجب عليها تأجيل تضمين حمولة streaming، أو رسالة streaming الكاملة، حتى أول Existing Session Message. سيكون هذا على حساب تسليم 0-RTT. قد تعتمد الاستراتيجيات أيضًا على نوع حركة البيانات أو نوع tunnel، أو على GET مقابل POST، على سبيل المثال. يعتمد على التطبيق.

#### Bob KDF للرسالة 1

MLKEM أو MLDSA أو كلاهما على نفس الوجهة، سيزيد بشكل كبير من حجم رسالة الجلسة الجديدة، كما هو موضح أعلاه. قد يقلل هذا بشكل كبير من موثوقية تسليم رسالة الجلسة الجديدة من خلال الأنفاق، حيث يجب تقسيمها إلى رسائل نفق متعددة بحجم 1024 بايت. نجاح التسليم يتناسب مع العدد الأسي للأجزاء. قد تستخدم التطبيقات استراتيجيات مختلفة لتحديد حجم الرسالة، على حساب تسليم 0-RTT. يعتمد على التطبيق.

### Ratchet

يمكننا تعيين MSB للمفتاح المؤقت (key[31] & 0x80) في طلب الجلسة للإشارة إلى أن هذا اتصال هجين. هذا سيسمح لنا بتشغيل كل من NTCP العادي و NTCP الهجين على نفس المنفذ. سيتم دعم متغير هجين واحد فقط، والإعلان عنه في عنوان router. على سبيل المثال، v=2,3 أو v=2,4 أو v=2,5.

إذا لم نفعل ذلك، فنحن بحاجة إلى عنوان/منفذ نقل مختلف، واسم بروتوكول جديد مثل "NTCP1PQ1".

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى أجهزة router من النوع 4، وسيتم الإشارة إلى الدعم في عناوين router.

قائمة المهام

### SSU2

ربما نحتاج إلى عنوان/منفذ نقل مختلف، ولكن نأمل ألا نحتاج لذلك، لدينا header مع flags للرسالة 1. يمكننا استخدام حقل الإصدار داخلياً واستخدام 3 لـ MLKEM512 و 4 لـ MLKEM768. ربما يكون v=2,3,4 في العنوان كافياً. ولكن نحتاج إلى معرفات لكلا الخوارزميتين الجديدتين: 3a، 3b؟

تحقق وتأكد من أن SSU2 يمكنه التعامل مع RI المقسم عبر حزم متعددة (6-8؟). i2pd حالياً يدعم فقط حد أقصى 2 من الأجزاء؟

ملاحظة: رموز الأنواع للاستخدام الداخلي فقط. ستبقى الـ routers من النوع 4، وسيتم الإشارة إلى الدعم في عناوين الـ router.

قائمة المهام

## Router Compatibility

### Transport Names

من المحتمل أننا لن نحتاج إلى أسماء transport جديدة، إذا كان بإمكاننا تشغيل كل من النسخة القياسية والهجينة على نفس المنفذ، مع استخدام إشارات الإصدار.

إذا كنا نحتاج إلى أسماء transport جديدة، فستكون:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
ملاحظة أن SSU2 لا يمكنه دعم MLKEM1024، فهو كبير جداً.

### Router Enc. Types

لدينا عدة بدائل للنظر فيها:

#### Bob KDF للرسالة 2

غير مُوصى به. استخدم فقط وسائل النقل الجديدة المذكورة أعلاه التي تتطابق مع نوع الـ router. الـ routers الأقدم لا يمكنها الاتصال أو بناء الـ tunnels من خلالها أو إرسال رسائل الـ netDb إليها. سيتطلب عدة دورات إصدار لتصحيح الأخطاء وضمان الدعم قبل التمكين افتراضياً. قد يمدد عملية الطرح بسنة أو أكثر مقارنة بالبدائل أدناه.

#### Alice KDF للرسالة 2

موصى به. نظرًا لأن PQ لا يؤثر على مفتاح X25519 الثابت أو بروتوكولات N handshake، يمكننا ترك الـ routers كنوع 4، والإعلان فقط عن transports جديدة. الـ routers الأقدم ستظل قادرة على الاتصال، أو بناء tunnels من خلالها، أو إرسال رسائل netDb إليها.

#### KDF للرسالة 3 (XK فقط)

أجهزة التوجيه من النوع 4 يمكنها الإعلان عن عناوين NTCP2 و NTCP2PQ* كليهما. هذه يمكن أن تستخدم نفس المفتاح الثابت والمعاملات الأخرى، أو لا. هذه ستحتاج على الأرجح إلى منافذ مختلفة؛ سيكون من الصعب جداً دعم بروتوكولي NTCP2 و NTCP2PQ* على نفس المنفذ، لأنه لا يوجد ترويسة أو تأطير من شأنه أن يسمح لـ Bob بتصنيف وتأطير رسالة Session Request الواردة.

المنافذ والعناوين المنفصلة ستكون صعبة بالنسبة لـ Java ولكنها مباشرة بالنسبة لـ i2pd.

#### KDF لـ split()

يمكن لـ router من النوع 4 الإعلان عن عناوين SSU2 و SSU2PQ* كليهما. مع إضافة أعلام الرأس، يمكن لـ Bob تحديد نوع النقل الوارد في الرسالة الأولى. لذلك، يمكننا دعم كل من SSU2 و SSUPQ* على نفس المنفذ.

يمكن نشر هذه العناوين كعناوين منفصلة (كما فعل i2pd في التحولات السابقة) أو في نفس العنوان مع معامل يشير إلى دعم PQ (كما فعل Java i2p في التحولات السابقة).

إذا كان في نفس العنوان، أو على نفس المنفذ في عناوين مختلفة، فستستخدم هذه نفس المفتاح الثابت والمعاملات الأخرى. إذا كان في عناوين مختلفة مع منافذ مختلفة، فقد تستخدم هذه نفس المفتاح الثابت والمعاملات الأخرى، أو قد لا تفعل ذلك.

المنافذ والعناوين المنفصلة ستكون صعبة لـ Java ولكن مباشرة لـ i2pd.

#### Recommendations

قائمة المهام

### NTCP2

#### معرفات Noise

أجهزة التوجيه الأقدم تتحقق من RIs ولذلك لا يمكنها الاتصال أو بناء الأنفاق من خلالها أو إرسال رسائل netDb إليها. سيتطلب عدة دورات إصدار للتصحيح وضمان الدعم قبل التمكين بشكل افتراضي. ستكون نفس المشاكل مثل طرح enc. type 5/6/7؛ قد يمد الطرح لسنة أو أكثر مقارنة ببديل طرح type 4 enc. type المذكور أعلاه.

لا توجد بدائل.

### LS Enc. Types

#### 1b) تنسيق الجلسة الجديد (مع الربط)

قد تكون هذه موجودة في الـ LS مع مفاتيح X25519 من النوع 4 الأقدم. أجهزة الـ router الأقدم ستتجاهل المفاتيح غير المعروفة.

يمكن للوجهات أن تدعم أنواع مفاتيح متعددة، ولكن فقط من خلال القيام بمحاولات فك تشفير تجريبية للرسالة 1 باستخدام كل مفتاح. يمكن تخفيف الأعباء الإضافية من خلال الاحتفاظ بعدد مرات فك التشفير الناجحة لكل مفتاح، وتجربة المفتاح الأكثر استخداماً أولاً. يستخدم Java I2P هذه الاستراتيجية لـ ElGamal+X25519 على نفس الوجهة.

### Dest. Sig. Types

#### 1g) تنسيق رد الجلسة الجديدة

أجهزة router تتحقق من توقيعات leaseSet ولذلك لا يمكنها الاتصال أو استقبال leaseSets للوجهات من النوع 12-17. سيتطلب عدة دورات إصدار لإصلاح الأخطاء وضمان الدعم قبل التفعيل افتراضياً.

لا توجد بدائل.

## المواصفات

البيانات الأكثر قيمة هي حركة المرور من النهاية إلى النهاية، المشفرة باستخدام ratchet. كمراقب خارجي بين قفزات النفق، تكون مشفرة مرتين إضافيتين، مع تشفير النفق وتشفير النقل. كمراقب خارجي بين OBEP و IBGW، تكون مشفرة مرة واحدة إضافية فقط، مع تشفير النقل. كمشارك OBEP أو IBGW، يكون ratchet هو التشفير الوحيد. ومع ذلك، نظراً لأن الأنفاق أحادية الاتجاه، فإن التقاط كلا الرسالتين في مصافحة ratchet سيتطلب تآمر routers، ما لم يتم بناء الأنفاق مع OBEP و IBGW على نفس الـ router.

النموذج الأكثر إثارة للقلق حاليًا لتهديد PQ هو تخزين حركة البيانات اليوم، لفك تشفيرها بعد سنوات عديدة من الآن (forward secrecy). النهج المختلط سيوفر الحماية ضد ذلك.

نموذج التهديد PQ الخاص بكسر مفاتيح المصادقة في فترة زمنية معقولة (مثل بضعة أشهر) ثم انتحال المصادقة أو فك التشفير في الوقت شبه الفعلي، أبعد بكثير؟ وهذا عندما نريد الانتقال إلى مفاتيح PQC الثابتة.

إذن، نموذج التهديد PQ الأقدم هو قيام OBEP/IBGW بتخزين البيانات لفك التشفير لاحقاً. يجب أن ننفذ hybrid ratchet أولاً.

Ratchet له الأولوية العليا. Transports تأتي بعد ذلك. Signatures لها أقل أولوية.

سيكون طرح التوقيعات أيضاً متأخراً بسنة أو أكثر عن طرح التشفير، لأنه لا يمكن تحقيق التوافق مع الإصدارات السابقة. كما أن اعتماد MLDSA في الصناعة سيتم توحيده من قبل منتدى CA/Browser وسلطات الشهادات. تحتاج سلطات الشهادات أولاً إلى دعم وحدة الأمان المجهزة (HSM)، والذي غير متوفر حالياً [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). نتوقع أن يقود منتدى CA/Browser القرارات حول اختيارات المعاملات المحددة، بما في ذلك ما إذا كان سيتم دعم أو طلب التوقيعات المركبة [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

إذا كنا لا نستطيع دعم بروتوكولات ratchet القديمة والجديدة على نفس الأنفاق، فإن عملية الترحيل ستكون أكثر صعوبة بكثير.

يجب أن نكون قادرين على مجرد تجربة واحد ثم الآخر، كما فعلنا مع X25519، ليتم إثباته.

## Issues

- اختيار Noise Hash - البقاء مع SHA256 أم الترقية؟
  SHA256 يجب أن يكون جيداً لـ 20-30 سنة أخرى، غير مهدد بواسطة PQ،
  انظر [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) و [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  إذا تم كسر SHA256 فلدينا مشاكل أسوأ (netdb).
- NTCP2 منفذ منفصل، عنوان router منفصل
- SSU2 ترحيل / اختبار الند
- حقل إصدار SSU2
- إصدار عنوان router في SSU2
