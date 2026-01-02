---
title: "Tek Yönlü Tunnels"
description: "I2P'nin tek yönlü tunnel tasarımının tarihsel özeti."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Tarihsel Not:** Bu sayfa, referans için eski “Unidirectional Tunnels” tartışmasını korur. Mevcut davranış için etkin [tunnel uygulama dokümantasyonu](/docs/specs/implementation/) sayfasına başvurun.

## Genel Bakış

I2P **tek yönlü tunnel'lar** oluşturur: bir tunnel dışa giden trafiği taşır ve ayrı bir tunnel içe gelen yanıtları taşır. Bu yapı en eski ağ tasarımlarına kadar uzanır ve Tor gibi çift yönlü devreli sistemlerden temel bir fark olarak kalır. Terimler ve uygulama ayrıntıları için [tunnel genel bakış](/docs/overview/tunnel-routing/) ve [tunnel spesifikasyonu](/docs/specs/implementation/) bölümlerine bakın.

## İnceleme

- Tek yönlü tunnel'lar istek ve yanıt trafiğini ayrı tutar; bu nedenle, tek bir işbirliği yapan eş grubu bir gidiş-dönüşün yalnızca yarısını gözlemler.
- Zamanlama saldırılarının, tek bir devreyi analiz etmek yerine iki tunnel havuzunu (giden ve gelen) kesiştirmesi gerekir; bu da korelasyon için çıtayı yükseltir.
- Bağımsız gelen ve giden havuzlar, router'ların gecikme, kapasite ve hata yönetimi özelliklerini yön başına ayarlamasına olanak tanır.
- Dezavantajlar arasında, eş yönetimi karmaşıklığının artması ve güvenilir hizmet sunumu için birden çok tunnel kümesini sürdürme gereksinimi yer alır.

## Anonimlik

Hermann ve Grothoff’un [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf) makalesi, tek yönlü tunnels’a karşı öncül saldırıları analiz eder; kararlı saldırganların nihayetinde uzun süreli eşleri doğrulayabileceğini öne sürer. Topluluktan gelen geri bildirimler, çalışmanın saldırganın sabrı ve yasal yetkileri hakkında belirli varsayımlara dayandığını ve yaklaşımı, çift yönlü tasarımları etkileyen zamanlama saldırılarıyla kıyaslamadığını belirtir. Süregelen araştırmalar ve pratik deneyim, tek yönlü tunnels’ın bir gözden kaçırma değil, bilinçli bir anonimlik tercihi olduğu yönündeki kanaati pekiştirmeye devam ediyor.
