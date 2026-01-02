---
title: "I2P'ye Giriş"
description: "I2P anonim ağına daha az teknik bir giriş"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## I2P Nedir?

The Invisible Internet Project (I2P), sansüre dirençli, eşler arası iletişim sağlayan anonim bir ağ katmanıdır. Anonim bağlantılar, kullanıcının trafiğini şifreleyerek ve dünya çapındaki gönüllüler tarafından işletilen dağıtık bir ağ üzerinden göndererek sağlanır.

## Temel Özellikler

### Anonymity

I2P hem mesaj gönderenin hem de alanın kimliğini gizler. IP adresinizin web siteleri ve hizmetler tarafından görülebildiği geleneksel internet bağlantılarının aksine, I2P kimliğinizi gizli tutmak için birden fazla şifreleme ve yönlendirme katmanı kullanır.

### Decentralization

I2P'de merkezi bir otorite yoktur. Ağ, bant genişliği ve hesaplama kaynakları bağışlayan gönüllüler tarafından sürdürülür. Bu durum, ağı sansüre ve tek arıza noktalarına karşı dirençli kılar.

### Anonimlik

I2P içindeki tüm trafik uçtan uca şifrelenir. Mesajlar ağ üzerinden geçerken birden fazla kez şifrelenir, bu da Tor'un çalışma şekline benzer ancak uygulamada önemli farklılıklar vardır.

## How It Works

### Merkeziyetsizlik

I2P, trafiği yönlendirmek için "tunnel" (tünel) kullanır. Veri gönderdiğinizde veya aldığınızda:

1. Yönlendiriciniz bir outbound tunnel (gönderme için) oluşturur
2. Yönlendiriciniz bir inbound tunnel (alma için) oluşturur
3. Mesajlar şifrelenir ve birden fazla router üzerinden gönderilir
4. Her router yalnızca önceki ve sonraki adımı bilir, tam yolu bilmez

### Uçtan Uca Şifreleme

I2P, geleneksel soğan yönlendirmesini "garlic routing" ile geliştirir:

- Birden fazla mesaj birlikte paketlenebilir (sarımsak soğanındaki dişler gibi)
- Bu, daha iyi performans ve ek anonimlik sağlar
- Trafik analizini zorlaştırır

### Network Database

I2P, aşağıdakileri içeren dağıtılmış bir ağ veritabanı tutar:

- Yönlendirici bilgileri
- Hedef adresleri (.i2p web siteleri gibi)
- Şifrelenmiş yönlendirme verileri

## Common Use Cases

### Tüneller

`.i2p` ile biten web sitelerini barındırın veya ziyaret edin - bunlara yalnızca I2P ağı içinden erişilebilir ve hem barındırıcılar hem de ziyaretçiler için güçlü anonimlik garantileri sağlar.

### Garlic Routing

I2P üzerinden BitTorrent kullanarak anonim olarak dosya paylaşın. Birçok torrent uygulamasında I2P desteği yerleşik olarak bulunur.

### Ağ Veritabanı

I2P-Bote veya I2P için tasarlanmış diğer e-posta uygulamalarını kullanarak anonim e-posta gönderin ve alın.

### Messaging

I2P ağı üzerinden IRC, anlık mesajlaşma veya diğer iletişim araçlarını gizli bir şekilde kullanın.

## Getting Started

I2P'yi denemek için hazır mısınız? Sisteminize I2P kurmak için [indirmeler sayfamızı](/downloads) ziyaret edin.

Daha fazla teknik ayrıntı için [Teknik Giriş](/docs/overview/tech-intro) bölümüne bakın veya tam [belgeleri](/docs) inceleyin.

## Nasıl Çalışır

- [Teknik Giriş](/docs/overview/tech-intro) - Daha derin teknik kavramlar
- [Tehdit Modeli](/docs/overview/threat-model) - I2P'nin güvenlik modelini anlamak
- [Tor ile Karşılaştırma](/docs/overview/comparison) - I2P'nin Tor'dan farkları
- [Kriptografi](/docs/specs/cryptography) - I2P'nin kriptografik algoritmaları hakkında detaylar
