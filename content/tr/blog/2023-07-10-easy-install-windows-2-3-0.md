---
title: "Windows için Easy-Install 2.3.0 yayınlandı"
date: 2023-07-10
author: "idk"
description: "Windows için Easy-Install 2.3.0 Yayınlandı"
categories: ["release"]
API_Translate: doğru
---

Windows için I2P Easy-Install bundle 2.3.0 sürümü artık yayımlandı. Her zamanki gibi, bu sürüm güncellenmiş bir I2P router içeriyor. Bu, ağ üzerinde hizmet barındıran kişileri etkileyen güvenlik sorunlarını da kapsar.

Bu, I2P Desktop GUI ile uyumsuz olacak Easy-Install paketinin son sürümü olacaktır. İçerdiği tüm webextensions (web uzantıları) için yeni sürümleri içerecek şekilde güncellendi. Özel temalarla uyumsuz olmasına neden olan I2P in Private Browsing içindeki uzun süredir devam eden bir hata düzeltildi. Kullanıcılara yine de özel temaları *yüklememeleri* tavsiye edilir. Snark sekmeleri Firefox’ta sekme sırasının en üstüne otomatik olarak sabitlenmez. Alternatif cookieStores (çerez depoları) kullanımı dışında, Snark sekmeleri artık normal tarayıcı sekmeleri gibi davranır.

**Ne yazık ki, bu sürüm hâlâ imzasız bir `.exe` yükleyici.** Lütfen kullanmadan önce yükleyicinin sağlama toplamını (checksum) doğrulayın. **Güncellemeler ise** I2P imzalama anahtarlarımla imzalanmıştır ve bu nedenle güvenlidir.

Bu sürüm OpenJDK 20 ile derlenmiştir. Tarayıcıyı başlatmak için bir kitaplık olarak i2p.plugins.firefox sürüm 1.1.0'ı kullanır. Bir I2P router olarak ve uygulamaları sağlamak için i2p.i2p sürüm 2.3.0'ı kullanır. Her zaman olduğu gibi, en uygun ilk fırsatta I2P router'ın en son sürümüne güncellemeniz önerilir.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
