---
title: "مواصفات I2NP"
description: "تنسيقات رسائل بروتوكول شبكة I2P (I2NP)، والأولويات، والهياكل المشتركة للاتصال بين أجهزة router."
slug: "i2np"
aliases:
  - "/ar/spec/i2np"
  - "/ar/spec/i2np/"
  - "/ar/i2np_spec"
  - "/ar/i2np_spec/"
category: "البروتوكولات"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## نظرة عامة

بروتوكول شبكة I2P (I2NP) هو الطبقة التي تعلو بروتوكولات النقل في I2P. إنه بروتوكول من router إلى router. يُستخدم للبحث في قاعدة بيانات الشبكة والردود، ولإنشاء الـ tunnels، ولرسائل البيانات المشفرة للـ router والعميل. يمكن إرسال رسائل I2NP من نقطة إلى نقطة إلى router آخر، أو إرسالها بشكل مجهول عبر tunnels إلى ذلك الـ router.

## إصدارات البروتوكول {#versions}

يجب على جميع الـ routers نشر إصدار بروتوكول I2NP الخاص بهم في حقل "router.version" في خصائص RouterInfo. هذا الحقل للإصدار هو إصدار واجهة برمجة التطبيقات (API)، والذي يشير إلى مستوى الدعم لميزات بروتوكول I2NP المختلفة، وليس بالضرورة الإصدار الفعلي للـ router.

إذا أرادت الـ routers البديلة (غير Java) نشر أي معلومات إصدار حول تطبيق الـ router الفعلي، يجب عليها القيام بذلك في خاصية أخرى. الإصدارات غير تلك المدرجة أدناه مسموحة. سيتم تحديد الدعم من خلال مقارنة رقمية؛ على سبيل المثال، 0.9.13 يعني الدعم لميزات 0.9.12. لاحظ أن خاصية "coreVersion" لم تعد تُنشر في معلومات الـ router، ولم تُستخدم أبداً لتحديد إصدار بروتوكول I2NP.

ملخص أساسي لإصدارات بروتوكول I2NP كما يلي. للتفاصيل، انظر أدناه.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
لاحظ أن هناك أيضاً ميزات متعلقة بالنقل ومشاكل توافق؛ راجع وثائق نقل NTCP و SSU للحصول على التفاصيل.

## الهياكل الشائعة {#structures}

الهياكل التالية هي عناصر من رسائل I2NP متعددة. وهي ليست رسائل كاملة.

### رأس رسالة I2NP {#struct-I2NPMessageHeader}

#### الوصف

رأس مشترك لجميع رسائل I2NP، والذي يحتوي على معلومات مهمة مثل المجموع الاختباري وتاريخ انتهاء الصلاحية، إلخ.

#### المحتويات

هناك ثلاثة تنسيقات منفصلة مستخدمة، حسب السياق؛ تنسيق واحد قياسي، وتنسيقان مختصران.

يحتوي التنسيق القياسي المكون من 16 بايت على 1 بايت [Integer](/docs/specs/common-structures/#integer) يحدد نوع هذه الرسالة، متبوعًا بـ 4 بايت [Integer](/docs/specs/common-structures/#integer) يحدد معرف الرسالة. بعد ذلك يوجد تاريخ انتهاء الصلاحية [Date](/docs/specs/common-structures/#date)، متبوعًا بـ 2 بايت [Integer](/docs/specs/common-structures/#integer) يحدد طول حمولة الرسالة، متبوعًا بـ [Hash](/docs/specs/common-structures/#hash)، والذي يتم اقتطاعه إلى البايت الأول. بعد ذلك تأتي بيانات الرسالة الفعلية.

تستخدم التنسيقات القصيرة انتهاء صالحية من 4 بايت بالثواني بدلاً من انتهاء صالحية من 8 بايت بالميلي ثانية. التنسيقات القصيرة لا تحتوي على checksum أو حجم، حيث يتم توفير هذه من خلال التغليف، اعتماداً على السياق.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### ملاحظات

- عند الإرسال عبر [SSU](/docs/transports/ssu/)، لا يتم استخدام الرأس القياسي بحجم 16 بايت. يتم تضمين نوع بحجم 1 بايت فقط وانتهاء صلاحية بحجم 4 بايت بالثواني. يتم دمج معرف الرسالة والحجم في تنسيق حزمة بيانات SSU. المجموع الاختباري غير مطلوب حيث يتم اكتشاف الأخطاء في فك التشفير.

- عند الإرسال عبر [NTCP2](/docs/specs/ntcp2/) أو [SSU2](/docs/specs/ssu2/)، لا يتم استخدام الرأس المعياري بحجم 16 بايت. يتم تضمين نوع واحد بايت فقط، ومعرف رسالة 4 بايت، وانتهاء صلاحية 4 بايت بالثواني. يتم دمج الحجم في تنسيقات حزم البيانات NTCP2 و SSU2. المجموع الاختباري غير مطلوب لأن الأخطاء يتم التقاطها في فك التشفير.

- الرأس القياسي مطلوب أيضاً لرسائل I2NP الموجودة داخل رسائل وهياكل أخرى (Data، TunnelData، TunnelGateway، و GarlicClove). اعتباراً من الإصدار 0.8.12، لتقليل الأعباء الإضافية، تم تعطيل التحقق من checksum في بعض النقاط في مكدس البروتوكول. ومع ذلك، من أجل التوافق مع الإصدارات الأقدم، لا يزال إنشاء checksum مطلوباً. إنه موضوع للبحث المستقبلي لتحديد النقاط في مكدس البروتوكول حيث يكون إصدار router النهائي البعيد معروفاً ويمكن تعطيل إنشاء checksum.

- انتهاء الصلاحية القصير غير موقع وسيلتف حول 7 فبراير 2106. اعتباراً من ذلك التاريخ، يجب إضافة إزاحة للحصول على الوقت الصحيح.

- قد ترفض التطبيقات الرسائل التي لها تواريخ انتهاء بعيدة جداً في المستقبل. الحد الأقصى الموصى به لانتهاء الصلاحية هو 60 ثانية في المستقبل.

### BuildRequestRecord {#struct-BuildRequestRecord}

مُهمل، يُستخدم فقط في الشبكة الحالية عندما يحتوي tunnel على router ElGamal. انظر [إنشاء ECIES Tunnel](/docs/specs/tunnel-creation-ecies/).

#### الوصف

سجل واحد في مجموعة من السجلات المتعددة لطلب إنشاء قفزة واحدة في tunnel. لمزيد من التفاصيل راجع [نظرة عامة على tunnel](/docs/specs/tunnel-implementation/) و[مواصفات إنشاء tunnel باستخدام ElGamal](/docs/specs/tunnel-creation/).

بالنسبة لـ ECIES-X25519 BuildRequestRecords، انظر [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### المحتويات (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) لاستقبال الرسائل عليه، متبوعاً بـ [Hash](/docs/specs/common-structures/#hash) الخاص بـ [RouterIdentity](/docs/specs/common-structures/#routeridentity) الخاص بنا. بعد ذلك يأتي [TunnelId](/docs/specs/common-structures/#tunnelid) و [Hash](/docs/specs/common-structures/#hash) الخاص بـ [RouterIdentity](/docs/specs/common-structures/#routeridentity) للموجه التالي.

مشفر بـ ElGamal وَ AES:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
مشفر بـ ElGamal:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
النص الواضح:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### ملاحظات

- في السجل المشفر بحجم 512 بايت، تحتوي بيانات ElGamal على البايتات 1-256 و 258-513 من كتلة ElGamal المشفرة بحجم 514 بايت [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). يتم إزالة بايتي الحشو من الكتلة (البايتات الصفرية في المواضع 0 و 257).

- راجع [مواصفات إنشاء الأنفاق](/docs/specs/tunnel-creation/) للحصول على تفاصيل حول محتويات الحقول.

### BuildResponseRecord {#struct-BuildResponseRecord}

مهجور، يُستخدم فقط في الشبكة الحالية عندما يحتوي tunnel على router ElGamal. انظر [إنشاء ECIES Tunnel](/docs/specs/tunnel-creation-ecies/).

#### الوصف

سجل واحد في مجموعة من السجلات المتعددة مع الردود على طلب البناء. لمزيد من التفاصيل انظر [نظرة عامة على tunnel](/docs/specs/tunnel-implementation/) و [مواصفات إنشاء tunnel باستخدام ElGamal](/docs/specs/tunnel-creation/).

بالنسبة لـ ECIES-X25519 BuildResponseRecords، انظر [إنشاء الأنفاق ECIES](/docs/specs/tunnel-creation-ecies/).

#### المحتويات (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### ملاحظات

- يمكن استخدام حقل البيانات العشوائية في المستقبل لإرجاع معلومات الازدحام أو اتصال النظراء إلى الطالب.

- راجع [مواصفات إنشاء الـ tunnel](/docs/specs/tunnel-creation/) للتفاصيل حول حقل الرد.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

لـ routers ECIES-X25519 فقط، اعتباراً من إصدار API 0.9.51. 218 بايت عند التشفير. راجع [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### سجل استجابة البناء المختصر {#struct-ShortBuildResponseRecord}

لـ routers ECIES-X25519 فقط، اعتباراً من إصدار API 0.9.51. 218 بايت عند التشفير. انظر [إنشاء tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

تحذير: هذا هو التنسيق المستخدم لقطع garlic cloves داخل رسائل garlic encryption المشفرة بـ ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). التنسيق لرسائل ECIES-AEAD-X25519-Ratchet garlic وقطع garlic cloves مختلف بشكل كبير؛ راجع [ECIES](/docs/specs/ecies/) للحصول على المواصفات.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### ملاحظات

- لا يتم تجزئة Cloves أبداً. عند الاستخدام في Garlic Clove، يحدد البت الأول من بايت علامة تعليمات التسليم التشفير. إذا كان هذا البت 0، فإن clove غير مشفر. إذا كان 1، فإن clove مشفر، و32 بايت Session Key يتبع بايت العلامة مباشرة. تشفير Clove غير مُطبق بالكامل.

- انظر أيضاً [مواصفات garlic routing](/docs/overview/garlic-routing/).

- الطول الأقصى هو دالة من الطول الإجمالي لجميع القطع والطول الأقصى لـ GarlicMessage.

- في المستقبل، يمكن أن تُستخدم الشهادة لـ HashCash لـ"دفع" تكلفة التوجيه.

- يمكن أن تكون الرسالة أي رسالة I2NP (بما في ذلك GarlicMessage، رغم أن ذلك لا يُستخدم عملياً). الرسائل المستخدمة عملياً هي DataMessage و DeliveryStatusMessage و DatabaseStoreMessage.

- يتم عادة تعيين Clove ID إلى رقم عشوائي عند الإرسال ويتم فحصه للتأكد من عدم وجود تكرارات عند الاستقبال (نفس مساحة معرف الرسالة كمعرفات الرسائل في المستوى الأعلى)

### تعليمات تسليم فص الثوم المشفر {#struct-GarlicCloveDeliveryInstructions}

هذا هو التنسيق المستخدم لكل من garlic cloves المشفرة بـ ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) وتلك المشفرة بـ ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/).

هذه المواصفة مخصصة لتعليمات التسليم داخل Garlic Cloves فقط. لاحظ أن "تعليمات التسليم" تُستخدم أيضاً داخل Tunnel Messages، حيث يكون التنسيق مختلفاً بشكل كبير. راجع [وثائق Tunnel Message](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) للتفاصيل. لا تستخدم المواصفة التالية لتعليمات التسليم الخاصة بـ Tunnel Message!

مفتاح الجلسة والتأخير غير مستخدمين وغير موجودين أبداً، لذا الأطوال الثلاثة المحتملة هي 1 (LOCAL)، و33 (ROUTER و DESTINATION)، و37 (TUNNEL) بايت.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## الرسائل

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### الوصف

متجر قاعدة بيانات غير مطلوب، أو الاستجابة لرسالة [DatabaseLookup](#msg-DatabaseLookup) ناجحة

#### المحتويات

LeaseSet أو LeaseSet2 أو MetaLeaseSet أو EncryptedLeaseset غير مضغوط، أو RouterInfo مضغوط

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### ملاحظات

- لأغراض الأمان، يتم تجاهل حقول الرد إذا تم استقبال الرسالة عبر tunnel.

- المفتاح هو الـ hash "الحقيقي" لـ RouterIdentity أو Destination، وليس مفتاح التوجيه.

- الأنواع 3 و 5 و 7 هي اعتباراً من الإصدار 0.9.38. راجع المقترح 123 لمزيد من المعلومات. يجب إرسال هذه الأنواع فقط إلى routers بالإصدار 0.9.38 أو أعلى.

- كتحسين لتقليل الاتصالات، إذا كان النوع هو LeaseSet، وكان رمز الرد مضمناً، وكان معرف نفق الرد غير صفري، وتم العثور على زوج بوابة الرد/معرف النفق في LeaseSet كإيجار، فيمكن للمستقبل إعادة توجيه الرد إلى أي إيجار آخر في LeaseSet.

- لإخفاء نظام تشغيل الـ router والتنفيذ، طابق تنفيذ الـ Java router لـ gzip عن طريق تعيين وقت التعديل إلى 0 وبايت نظام التشغيل إلى 0xFF، وتعيين XFL إلى 0x02 (ضغط أقصى، خوارزمية أبطأ). راجع RFC 1952. أول 10 بايتات من معلومات الـ router المضغوطة ستكون (hex): 1F 8B 08 00 00 00 00 00 02 FF

### البحث في قاعدة البيانات {#msg-DatabaseLookup}

#### الوصف

طلب للبحث عن عنصر في قاعدة بيانات الشبكة. الاستجابة تكون إما [DatabaseStore](#msg-DatabaseStore) أو [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### المحتويات

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### تشفير الردود

ملاحظة: أصبحت routers ElGamal مهجورة اعتباراً من API 0.9.58. نظراً لأن الحد الأدنى الموصى به لإصدار floodfill للاستعلام هو الآن 0.9.58، فإن التطبيقات لا تحتاج إلى تنفيذ التشفير لـ routers floodfill من نوع ElGamal. الوجهات ElGamal لا تزال مدعومة.

يتم استخدام بت العلم 4 مع بت 1 لتحديد وضع تشفير الرد. يجب تعيين بت العلم 4 فقط عند الإرسال إلى routers بإصدار 0.9.46 أو أحدث. راجع المقترحات 154 و 156 للتفاصيل.

في الجدول أدناه، "DH n/a" تعني أن الرد غير مُشفر. "DH no" تعني أن مفاتيح الرد مُضمنة في الطلب. "DH yes" تعني أن مفاتيح الرد مُشتقة من عملية DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### بدون تشفير

reply_key و tags و reply_tags غير موجودة.

#### ElG إلى ElG

مدعوم اعتباراً من 0.9.7. مهجور اعتباراً من 0.9.58. وجهة ElG ترسل بحث إلى router من نوع ElG.

توليد مفتاح الطالب:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
تنسيق الرسالة:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES إلى ElG

مدعوم اعتباراً من الإصدار 0.9.46. مهجور اعتباراً من الإصدار 0.9.58. وجهة ECIES ترسل استعلام إلى router من نوع ElG. حقول reply_key و reply_tags يتم إعادة تعريفهما للرد المشفر بـ ECIES.

توليد مفتاح الطالب:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
تنسيق الرسالة: إعادة تعريف حقول reply_key و reply_tags كما يلي:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
الرد هو رسالة ECIES Existing Session، كما هو محدد في [ECIES](/docs/specs/ecies/).

#### تنسيق الرد

هذه هي رسالة الجلسة الحالية، نفس الرسالة الموجودة في [ECIES](/docs/specs/ecies/)، منسوخة أدناه للمرجع.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
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
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
معايير AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES إلى ECIES (0.9.49)

وجهة ECIES أو router يرسل استعلام إلى ECIES router. مدعوم منذ الإصدار 0.9.49.

تم إدخال routers الـ ECIES في الإصدار 0.9.48، انظر [الاقتراح 156](/proposals/156/). وجهات الـ ECIES والـ routers قد تستخدم نفس التنسيق كما في قسم "ECIES إلى ElG" أعلاه، مع تضمين مفاتيح الرد في الطلب. تشفير رسالة البحث محدد في [ECIES-ROUTERS](/docs/specs/ecies-routers/). الطالب مجهول الهوية.

#### ECIES إلى ECIES (مستقبلي)

هذا الخيار لم يتم تعريفه بالكامل بعد. راجع [اقتراح 156](/proposals/156/).

#### ملاحظات

- قبل الإصدار 0.9.16، قد يكون المفتاح خاصاً بـ RouterInfo أو LeaseSet، حيث أنهما في نفس مساحة المفاتيح، ولم يكن هناك علم لطلب نوع معين فقط من البيانات.

- علامة التشفير ومفتاح الرد وعلامات الرد اعتبارًا من الإصدار 0.9.7.

- الردود المشفرة مفيدة فقط عندما تكون الاستجابة من خلال tunnel.

- يمكن أن يكون عدد العلامات المضمنة أكبر من واحدة إذا تم تنفيذ استراتيجيات بحث DHT بديلة (على سبيل المثال، عمليات البحث التكرارية).

- مفتاح البحث ومفاتيح الاستبعاد هي الـ hashes "الحقيقية"، وليس مفاتيح التوجيه.

- الأنواع 3 و 5 و 7 قد يتم إرجاعها اعتباراً من الإصدار 0.9.38. راجع المقترح 123 لمزيد من المعلومات.

- ملاحظات البحث الاستكشافي: يُعرّف البحث الاستكشافي بأنه يعيد قائمة من الـ hashes غير الـ floodfill القريبة من المفتاح. ومع ذلك، راجع الملاحظات المهمة لـ DatabaseSearchReply للحصول على متغيرات التنفيذ. بالإضافة إلى ذلك، لم توضح هذه المواصفة أبداً ما إذا كان يجب على المستقبل البحث عن مفتاح البحث للحصول على RI وإرجاع DatabaseStore بدلاً من DSRM إذا كان موجوداً. Java يقوم بالبحث؛ i2pd لا يقوم بذلك. لذلك، لا يُنصح باستخدام البحث الاستكشافي للـ hashes المستلمة مسبقاً.

### رد البحث في قاعدة البيانات {#msg-DatabaseSearchReply}

#### الوصف

الاستجابة لرسالة [DatabaseLookup](#msg-DatabaseLookup) فاشلة

#### المحتويات

قائمة بـ hashes الـ router الأقرب للمفتاح المطلوب

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### ملاحظات

- قيمة التجميع (hash) الخاصة بـ 'from' غير مصادق عليها ولا يمكن الوثوق بها.

- هاشات الـ peer المُرجعة ليست بالضرورة أقرب إلى المفتاح من الـ router الذي يتم استعلامه. بالنسبة للردود على عمليات البحث العادية، هذا يسهل اكتشاف floodfills جديدة والبحث "العكسي" (الأبعد عن المفتاح) لتحسين القوة والموثوقية.

- المفتاح للبحث الاستكشافي يتم توليده عادة بشكل عشوائي. لذلك، قد يتم اختيار peer_hashes غير الـ floodfill في الاستجابة باستخدام خوارزمية محسنة، مثل توفير peers قريبة من المفتاح وليس بالضرورة الأقرب في قاعدة بيانات الشبكة المحلية بأكملها، لتجنب فرز أو بحث غير فعال في قاعدة البيانات المحلية بأكملها. استراتيجيات أخرى مثل التخزين المؤقت قد تكون مناسبة أيضاً. هذا يعتمد على التنفيذ.

- العدد النموذجي للهاشات المُرجعة: 3

- العدد الأقصى الموصى به من الـ hashes للإرجاع: 16

- مفتاح البحث وهاشات النظراء وهاش المرسل هي هاشات "حقيقية"، وليست مفاتيح توجيه.

### حالة التسليم {#msg-DeliveryStatus}

#### الوصف

إقرار رسالة بسيط. يتم إنشاؤه عادةً من قبل منشئ الرسالة، ويُلف في Garlic Message مع الرسالة نفسها، ليتم إرجاعه من قبل الوجهة.

يُستخدم هذا الرسالة أيضًا لاختبار النفق، حيث يُرسل المُرسل لها عبر نفق صادر إلى نفق وارد، ثم يعود إليها مرة أخرى. وفي هذا التطبيق أيضًا، تكون الرسالة عادةً مغلفة بتقنية Garlic. وقد أصبح اختبار النفق مطلوبًا بدءًا من إصدار واجهة برمجة التطبيقات (API) 0.9.68 لعام 2026-02، حيث يُسمح للراوترات بحذف النُفق المشاركة التي لم تستلم أي حركة مرور بعد أول دقيقتين.

#### المحتويات

معرّف الرسالة التي تم تسليمها، ووقت إنشائها أو وصولها.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### ملاحظات

- يبدو أن الطابع الزمني يتم تعيينه دائماً من قبل المنشئ إلى الوقت الحالي. ومع ذلك، هناك عدة استخدامات لهذا في الكود، وقد يتم إضافة المزيد في المستقبل.

- تُستخدم هذه الرسالة أيضًا كتأكيد لإنشاء جلسة في SSU [SSU-ED](/docs/transports/ssu/#establishDirect). في هذه الحالة، يتم تعيين معرف الرسالة إلى رقم عشوائي، ويتم تعيين "وقت الوصول" إلى المعرف الحالي على مستوى الشبكة، والذي هو 2 (أي 0x0000000000000002).

### Garlic {#msg-Garlic}

تحذير: هذا هو التنسيق المستخدم للرسائل المغطية المشفرة باستخدام خوارزمية إل-غامال [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). أما تنسيق رسائل الثوم المشفرة باستخدام ECIES-AEAD-X25519-Ratchet والقطع الثومية (garlic cloves) فهو مختلف بشكل كبير؛ انظر [ECIES](/docs/specs/ecies/) للمواصفات.

#### الوصف

تُستخدم لتغليف رسائل I2NP المشفرة المتعددة

#### المحتويات

عند فك التشفير، تكون سلسلة من [Garlic Cloves](#struct-GarlicClove) وبيانات إضافية، والمعروفة أيضًا باسم Clove Set.

مشفر:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
البيانات المُفكَّكة التشفير، والمعروفة أيضًا باسم مجموعة Clove:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### ملاحظات

- عندما تكون غير مشفرة، تحتوي البيانات على واحد أو أكثر من [Garlic Cloves](#struct-GarlicClove).

- الكتلة المشفرة بـ AES مُبطنة بحد أدنى 128 بايت؛ مع Session Tag بحجم 32 بايت يكون الحد الأدنى لحجم الرسالة المشفرة 160 بايت؛ مع 4 بايتات الطول يكون الحد الأدنى لحجم Garlic Message 164 بايت.

- الطول الأقصى الفعلي أقل من 64 كيلوبايت؛ انظر [I2NP](/docs/protocol/i2np/).

- انظر أيضًا [مواصفات ElGamal/AES](/docs/specs/elgamal-aes/).

- انظر أيضاً [مواصفات garlic routing](/docs/overview/garlic-routing/).

- الحد الأدنى لحجم الكتلة المشفرة بـ AES والبالغ 128 بايت غير قابل للتكوين حالياً، ومع ذلك فإن الحد الأدنى لحجم DataMessage في GarlicClove في GarlicMessage، مع النفقات الإضافية، هو 128 بايت على أي حال. قد يتم إضافة خيار قابل للتكوين لزيادة الحد الأدنى للحجم في المستقبل.

- معرف الرسالة يُعيّن عادة إلى رقم عشوائي عند الإرسال ويبدو أنه يُتجاهل عند الاستقبال.

- في المستقبل، يمكن أن تُستخدم الشهادة للدفع مقابل التوجيه باستخدام HashCash.

### TunnelData {#msg-TunnelData}

#### الوصف

رسالة تُرسل من بوابة النفق أو أحد مشاركيه إلى المشارك التالي أو النهاية. تكون البيانات ذات طول ثابت، وتحتوي على رسائل I2NP التي تم تجزئتها وتجميعها وإضافة الحشو إليها وتشفيرها.

#### المحتويات

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### ملاحظات

- يتم تعيين معرف رسالة I2NP لهذه الرسالة إلى رقم عشوائي جديد في كل قفزة.

- انظر أيضاً [مواصفات رسائل الأنفاق](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### الوصف

يلف رسالة I2NP أخرى لإرسالها عبر نفق عند بوابة الدخول الخاصة بالنفق.

#### المحتويات

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### ملاحظات

- الحمولة هي رسالة I2NP مع رأس قياسي بحجم 16 بايت.

### البيانات {#msg-Data}

#### الوصف

تُستخدم بواسطة رسائل Garlic وGarlic Cloves لتغليف بيانات عشوائية.

#### المحتويات

عدد صحيح للطول، يتبعه بيانات غير شفافة.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### ملاحظات

- هذه الرسالة لا تحتوي على معلومات توجيه ولن يتم إرسالها أبداً "غير مغلفة". تُستخدم فقط داخل رسائل `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

مُهمل، استخدم [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### ملاحظات

- اعتباراً من الإصدار 0.9.48، قد يحتوي أيضاً على ECIES-X25519 BuildRequestRecords، انظر [إنشاء نفق ECIES](/docs/specs/tunnel-creation-ecies/).

- انظر أيضاً [مواصفات إنشاء tunnel](/docs/specs/tunnel-creation/).

- يجب تعيين معرف رسالة I2NP لهذه الرسالة وفقاً لمواصفات إنشاء tunnel.

- بينما نادراً ما تُشاهد هذه الرسالة في الشبكة اليوم، حيث تم استبدالها برسالة `VariableTunnelBuild`، قد تُستخدم لا تزال للأنفاق الطويلة جداً، ولم يتم إهمالها. يجب على أجهزة router تنفيذها.

### TunnelBuildReply {#msg-TunnelBuildReply}

مُهمل، استخدم [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### ملاحظات

- اعتباراً من الإصدار 0.9.48، قد يحتوي أيضاً على ECIES-X25519 BuildResponseRecords، انظر [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- انظر أيضًا [مواصفات إنشاء tunnel](/docs/specs/tunnel-creation/).

- يجب تعيين معرف رسالة I2NP لهذه الرسالة وفقاً لمواصفات إنشاء tunnel.

- بينما نادراً ما تُرى هذه الرسالة في شبكة اليوم، حيث تم استبدالها برسالة `VariableTunnelBuildReply`، إلا أنه قد يتم استخدامها للأنفاق الطويلة جداً، ولم يتم إهمالها. يجب على أجهزة router تنفيذها.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### ملاحظات

- اعتباراً من الإصدار 0.9.48، قد يحتوي أيضاً على ECIES-X25519 BuildRequestRecords، راجع [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- تم تقديم هذه الرسالة في إصدار router 0.7.12، وقد لا يتم إرسالها إلى المشاركين في tunnel الذين يستخدمون إصدارات أقدم من ذلك.

- انظر أيضاً [مواصفات إنشاء الأنفاق](/docs/specs/tunnel-creation/).

- يجب تعيين معرف رسالة I2NP لهذه الرسالة وفقاً لمواصفات إنشاء tunnel.

- العدد النموذجي للسجلات في الشبكة اليوم هو 4، بحجم إجمالي قدره 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### ملاحظات

- اعتباراً من الإصدار 0.9.48، قد يحتوي أيضاً على ECIES-X25519 BuildResponseRecords، انظر [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- تم إدخال هذه الرسالة في إصدار router 0.7.12، وقد لا يتم إرسالها إلى المشاركين في tunnel الذين يستخدمون إصدارات أقدم من ذلك.

- انظر أيضًا [مواصفات إنشاء الأنفاق](/docs/specs/tunnel-creation/).

- يجب تعيين معرف رسالة I2NP لهذه الرسالة وفقاً لمواصفات إنشاء tunnel.

- العدد النمطي للسجلات في الشبكة اليوم هو 4، بحجم إجمالي قدره 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### الوصف

اعتبارًا من إصدار API 0.9.51، للراوترات التي تستخدم ECIES-X25519 فقط.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### ملاحظات

- اعتباراً من 0.9.51. انظر [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- تم تقديم هذه الرسالة في إصدار router 0.9.51، وقد لا يتم إرسالها إلى مشاركي tunnel الذين يستخدمون إصدارات أقدم من ذلك.

- العدد النموذجي للسجلات في الشبكة اليوم هو 4، بحجم إجمالي قدره 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### الوصف

تم الإرسال من نقطة النهاية الصادرة لتونيل جديد إلى المصدر. بدءًا من إصدار API 0.9.51، ولأجهزة التوجيه ECIES-X25519 فقط.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### ملاحظات

- اعتباراً من الإصدار 0.9.51. انظر [إنشاء الأنفاق باستخدام ECIES](/docs/specs/tunnel-creation-ecies/).

- العدد النموذجي للسجلات في الشبكة اليوم هو 4، بحجم إجمالي قدره 873.

## المراجع

- **[CRYPTO-ELG]** [التشفير - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [الهياكل المشتركة - التاريخ](/docs/specs/common-structures/#date)
- **[ECIES]** [مواصفات ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [مواصفات موجهات ECIES](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [توجيه Garlic](/docs/overview/garlic-routing/)
- **[Hash]** [الهياكل المشتركة - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [بروتوكول I2NP](/docs/protocol/i2np/)
- **[Integer]** [الهياكل المشتركة - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [مواصفات NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [الاقتراح 156](/proposals/156/)
- **[Prop157]** [الاقتراح 157](/proposals/157/)
- **[RouterIdentity]** [الهياكل المشتركة - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [نقل SSU](/docs/transports/ssu/)
- **[SSU-ED]** [نقل SSU - إنشاء مباشر](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [مواصفات SSU2](/docs/specs/ssu2/)
- **[TMDI]** [تعليمات توصيل رسائل tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [مواصفات إنشاء tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [إنشاء tunnel بـ ECIES](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [تطبيق tunnel](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [مواصفات رسائل tunnel](/docs/legacy/tunnel-message/)
- **[TunnelId]** [الهياكل المشتركة - TunnelId](/docs/specs/common-structures/#tunnelid)
