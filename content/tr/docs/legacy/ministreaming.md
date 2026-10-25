---
title: "Ministreaming Kütüphanesi"
description: "I2P'nin ilk TCP benzeri taşıma katmanına dair tarihi notlar"
slug: "ministreaming"
aliases:
  - "/tr/ministreaming"
  - "/tr/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Not

Ministreaming kütüphanesi, "tam" [streaming library](/docs/api/streaming) tarafından geliştirilmiş ve genişletilmiştir. Ministreaming kullanımdan kaldırılmıştır ve günümüzün uygulamalarıyla uyumsuzdur. Aşağıdaki dokümantasyon eskidir. Ayrıca streaming'in ministreaming'i aynı Java paketi (net.i2p.client.streaming) içinde genişlettiğini unutmayın, bu nedenle mevcut API dokümantasyonu her ikisini de içerir. Kullanımdan kalkan ministreaming sınıfları ve metodları Javadoc'larda açıkça kullanımdan kaldırılmış olarak işaretlenmiştir.

## Ministreaming Kütüphanesi

Ministreaming kütüphanesi, güvenilmez, sırasız ve kimlik doğrulaması olmayan bir mesaj katmanı üzerinde güvenilir, sıralı ve kimlik doğrulamalı mesaj akışlarının çalışmasına olanak tanıyan temel [I2CP](/docs/protocol/i2cp) üzerinde bir katmandır. Tıpkı TCP ile IP ilişkisi gibi, bu streaming işlevselliği de bir dizi ödünleşim ve optimizasyon sunar, ancak bu işlevselliği temel I2P koduna gömmek yerine, TCP benzeri karmaşıklıkları ayrı tutmak ve alternatif optimize edilmiş uygulamalara izin vermek için kendi kütüphanesine ayrılmıştır.

Ministreaming kütüphanesi, mihi tarafından [I2PTunnel](/docs/api/i2ptunnel) uygulamasının bir parçası olarak yazılmış, daha sonra ayrıştırılarak BSD lisansı altında yayınlanmıştır. "Mini"streaming kütüphanesi olarak adlandırılmasının nedeni, uygulamada bazı basitleştirmeler yapması, oysa daha sağlam bir streaming kütüphanesinin I2P üzerindeki işlem için daha fazla optimize edilebilecek olmasıdır. Ministreaming kütüphanesindeki iki ana sorun, geleneksel TCP iki fazlı kurulum protokolünü kullanması ve mevcut sabit pencere boyutunun 1 olmasıdır. Kurulum sorunu uzun yaşamlı stream'ler için küçüktür, ancak hızlı HTTP istekleri gibi kısa olanlar için etki önemli olabilir. Pencere boyutuna gelince, ministreaming kütüphanesi gönderilen mesajlar içinde herhangi bir ID veya sıralama tutmaz (veya herhangi bir uygulama seviyesi ACK veya SACK içermez), bu nedenle başka bir mesaj göndermeden önce ortalama olarak bir mesaj gönderme süresinin iki katı kadar beklemek zorundadır.

Bu sorunlara rağmen, ministreaming kütüphanesi birçok durumda oldukça iyi performans sergiler ve API'si hem oldukça basittir hem de farklı streaming uygulamaları tanıtıldığında değişmeden kalabilme yeteneğine sahiptir. Kütüphane kendi ministreaming.jar dosyasında dağıtılır. Java'da geliştirme yapan geliştiriciler API'ye doğrudan erişebilirken, diğer dillerde geliştirme yapan geliştiriciler bunu [SAM](/docs/api/samv3)'ın streaming desteği aracılığıyla kullanabilir.
