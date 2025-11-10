---
title: "Windows Kolay Kurulum Paketi 1.9.0 Sürümü"
date: 2022-08-28
author: "idk"
description: "Windows Kolay Kurulum Paketi 1.9.0 - Önemli Kararlılık/Uyumluluk İyileştirmeler"
categories: ["release"]
API_Translate: doğru
---

## Bu güncelleme, yeni 1.9.0 router ve paket kullanıcıları için büyük kullanım kolaylığı iyileştirmeleri içerir.

Bu sürüm, yeni I2P 1.9.0 router'ı içerir ve Java 18.02.1 tabanlıdır.

Eski batch komut dosyaları, bizzat jpackage'ın içindeki daha esnek ve daha kararlı bir çözüme geçilerek aşamalı olarak kullanımdan kaldırıldı. Bu, batch komut dosyalarında mevcut olan dosya yolu belirleme ve dosya yollarını tırnak içine alma ile ilgili tüm hataları düzeltmelidir. Güncelledikten sonra batch komut dosyaları güvenle silinebilir. Bir sonraki güncellemede yükleyici tarafından kaldırılacaktır.

Tarama araçlarını yönetmek için bir alt proje başlatıldı: i2p.plugins.firefox; bu proje, birçok platformda I2P tarayıcılarını otomatik ve kararlı biçimde yapılandırmak için kapsamlı özelliklere sahiptir. Bu, toplu komut dosyalarının yerini almak için kullanıldı, ancak aynı zamanda platformlar arası bir I2P Browser yönetim aracı olarak da işlev görür. Katkılar kaynak deposunda şu adreste memnuniyetle karşılanır: http://git.idk.i2p/idk/i2p.plugins.firefox

Bu sürüm, IzPack yükleyicisinin kurduğu ve i2pd gibi üçüncü taraf router gerçeklemeleri tarafından sağlananlar da dahil olmak üzere, harici olarak çalışan I2P router'larla uyumluluğu geliştirir. Harici router keşfini iyileştirerek daha az sistem kaynağı gerektirir, başlatma süresini kısaltır ve kaynak çakışmalarının oluşmasını önler.

Buna ek olarak, profil Arkenfox profilinin en son sürümüne güncellendi. I2P in Private Browsing ve NoScript güncellendi. Profil, farklı tehdit modelleri için farklı yapılandırmaları değerlendirmeyi mümkün kılmak amacıyla yeniden yapılandırıldı.
