---
title: "فهرس الوثائق التقنية"
description: "فهرس الوثائق التقنية لـ I2P"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/ar/docs/develop/overview"
  - "/ar/docs/develop/overview/"
---


## نظرة عامة {#overview}

- [مقدمة تقنية](/docs/overview/intro)
- [مقدمة أقل تقنية](/docs/overview/intro/)
- [نموذج التهديدات والتحليل](/docs/overview/threat-model)
- [مقارنات مع شبكات مجهولة أخرى](/docs/overview/comparison)
- [مخطط حزمة البروتوكول](/docs/development/protocol-stack)
- [أوراق بحثية عن I2P](/papers/)
- [العروض التقديمية والمقالات والدروس ومقاطع الفيديو والمقابلات](/about/media/)
- [نظرة عامة على مشروع الإنترنت الخفي (I2P) - 28 أغسطس 2003 (PDF)](/docs/historical/i2p_philosophy.pdf)


## مواضيع طبقة التطبيقات {#applications}

- [نظرة عامة ودليل تطوير التطبيقات](/docs/development/applications)
- [التسمية ودفتر العناوين](/docs/overview/naming)
- [أوامر تغذية اشتراك دفتر العناوين](/docs/specs/subscription)
- [نظرة عامة على الإضافات](/docs/guides/plugins)
- [مواصفات الإضافات](/docs/specs/plugin)
- [العملاء المُدارون](/docs/applications/managed-clients)
- [تضمين الموجه في تطبيقك](/docs/applications/embedding)
- [بت تورنت عبر I2P](/docs/applications/bittorrent)
- [واجهة برمجة إضافة I2PControl](/docs/api/i2pcontrol)
- [تنسيق hostsdb.blockfile](/docs/specs/blockfile)
- [تنسيق ملف التكوين](/docs/specs/configuration)


## واجهات برمجة وبروتوكولات طبقة التطبيقات {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [تكوين I2PTunnel](/docs/specs/configuration)
- [وكيل SOCKS](/docs/api/socks)
- [بروتوكول SAMv3](/docs/api/samv3)
- [بروتوكول SAM](/docs/legacy/sam) (مهمل)
- [بروتوكول SAMv2](/docs/legacy/samv2) (مهمل)
- [بروتوكول BOB](/docs/legacy/bob) (مهمل)


## واجهات برمجة وبروتوكولات النقل من طرف إلى طرف {#transport-api}

- [نظرة عامة على بروتوكول التدفق](/docs/api/streaming)
- [مواصفات بروتوكول التدفق](/docs/specs/streaming)
- [حزم البيانات](/docs/api/datagrams)
- [مواصفات حزم البيانات](/docs/specs/datagrams)


## واجهة برمجة وبروتوكول العميل إلى الموجه {#i2cp}

- [نظرة عامة على I2CP](/docs/specs/i2cp)
- [مواصفات I2CP](/docs/specs/i2cp)
- [مواصفات هياكل البيانات المشتركة](/docs/specs/common-structures)


## التشفير من طرف إلى طرف {#encryption}

- [تشفير ECIES-X25519-AEAD-Ratchet للوجهات](/docs/specs/ecies)
- [تشفير ECIES-X25519 الهجين](/docs/specs/ecies-hybrid)
- [تشفير ECIES-X25519 للموجهات](/docs/specs/ecies-routers)
- [تشفير ElGamal/AES+SessionTag](/docs/specs/elgamal-aes)
- [تفاصيل تشفير ElGamal و AES](/docs/specs/cryptography)


## قاعدة بيانات الشبكة {#netdb}

- [نظرة عامة على قاعدة بيانات الشبكة والتفاصيل وتحليل التهديدات](/docs/overview/network-database)
- [التجزئات التشفيرية](/docs/specs/cryptography#hashes)
- [التوقيعات التشفيرية](/docs/specs/cryptography#signatures)
- [توقيعات Red25519](/docs/specs/red25519)
- [مواصفات إعادة بذر الموجه](/docs/misc/reseed)
- [عناوين Base32 لمجموعات الإيجار المشفرة](/docs/specs/b32encrypted)


## بروتوكول رسائل الموجه {#i2np}

- [نظرة عامة على I2NP](/docs/specs/i2np)
- [مواصفات I2NP](/docs/specs/i2np)
- [مواصفات هياكل البيانات المشتركة](/docs/specs/common-structures)
- [مواصفات مجموعة الإيجار المشفرة](/docs/specs/encryptedleaseset)


## الأنفاق {#tunnels}

- [تصنيف واختيار الأقران](/docs/overview/peer-selection)
- [نظرة عامة على توجيه الأنفاق](/docs/overview/tunnel-routing)
- [توجيه الثوم والمصطلحات](/docs/overview/garlic-routing)
- [بناء وتشفير الأنفاق](/docs/specs/tunnel-creation)
- [ElGamal/AES لتشفير طلب البناء](/docs/specs/elgamal-tunnel-creation)
- [تفاصيل تشفير ElGamal و AES](/docs/specs/cryptography)
- [مواصفات بناء الأنفاق (ElGamal)](/docs/specs/tunnel-creation)
- [مواصفات بناء الأنفاق (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [مواصفات رسائل الأنفاق منخفضة المستوى](/docs/specs/tunnel-message)
- [الأنفاق أحادية الاتجاه](/docs/legacy/unidirectional)
- [تصنيف واختيار الأقران في شبكة I2P المجهولة - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## طبقة النقل {#transports}

- [نظرة عامة على طبقة النقل](/docs/overview/transport)
- [مواصفات NTCP2](/docs/specs/ntcp2)
- [مواصفات SSU2](/docs/specs/ssu2)
- [NTCP (قديم)](/docs/legacy/ntcp)
- [نظرة عامة على SSU (قديم)](/docs/legacy/ssu-overview)


## مواضيع الموجه الأخرى {#router}

- [تحديثات برنامج الموجه](/docs/specs/updates)
- [مواصفات إعادة بذر الموجه](/docs/misc/reseed)
- [الأداء](/docs/overview/performance)
- [تنسيق ملف التكوين](/docs/specs/configuration)
- [تنسيق ملف GeoIP](/docs/legacy/geoip)
- [المنافذ المستخدمة بواسطة I2P](/docs/overview/ports)


## أدلة وموارد المطورين {#develop}

- [دليل المطور الجديد](/docs/development/new-developers)
- [دليل المترجم الجديد](/docs/development/new-translators)
- [إرشادات المطورين](/docs/development/dev-guidelines)
- [المقترحات](/proposals/)
- [تضمين الموجه في تطبيقك](/docs/applications/embedding)
- [كيفية إعداد خادم إعادة البذر](/docs/guides/reseed-server)
- [المنافذ المستخدمة بواسطة I2P](/docs/overview/ports)
- [خارطة طريق المشروع](/get-involved/roadmap/)
- [وثائق invisiblenet I2P القديمة - 2003](/docs/historical/)
