---
title: "2004-10-19 için I2P Durum Notları"
date: 2004-10-19
author: "jr"
description: "0.4.1.3 sürümünü, tunnel (tünel) performans iyileştirmelerini, akış kitaplığındaki ilerlemeyi ve files.i2p arama motorunu kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, yine salı oldu

## Dizin

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

0.4.1.3 sürümü bir iki gün önce yayımlandı ve görünüşe göre çoğu kişi güncelledi (teşekkürler!). Ağ oldukça iyi çalışıyor, ancak güvenilirlikte hâlâ devrim niteliğinde bir artış yok. Bununla birlikte, 0.4.1.2'den kalan watchdog (gözetleyici zamanlayıcı) hataları ortadan kalktı (ya da en azından kimse onlardan bahsetmedi). Amacım, 0.4.1.3 sürümünün 0.4.2'den önceki son yama olması; tabii ki düzeltilmesi gereken büyük bir şey ortaya çıkarsa, bir yenisi daha çıkaracağız.

## 2) Tunnel test süresi, ve gönderim işleme süresi

0.4.1.3 sürümündeki en önemli değişiklikler, tunnel testleriyle ilgiliydi - sabit bir test süresi (30 saniye!) yerine, ölçülen performanstan türetilen çok daha agresif zaman aşımı sürelerimiz var. Bu iyi, çünkü artık herhangi bir işe yaramayacak kadar yavaş olduklarında tunnel'ları başarısız olarak işaretliyoruz. Ancak bu aynı zamanda kötü, çünkü bazen tunnel geçici olarak tıkanabiliyor ve o dönemde onları test edersek, normalde çalışacak bir tunnel'ı başarısız sayıyoruz.

Tek bir router üzerinde bir tunnel testinin ne kadar sürdüğüne dair yakın tarihli bir grafik:

Those are generally ok tunnel test times - they pass through 4 remote peers (with 2 hop tunnels), giving the bulk of them ~1-200ms per hop. However, thats not always the case, as you can see - sometimes it takes on the order of seconds per hop.

İşte sıradaki grafik burada devreye giriyor - belirli bir router bir mesaj göndermek istediği andan o mesajın soket üzerinden dışarıya boşaltıldığı ana kadar geçen kuyruk süresi:

Değerlerin yaklaşık yüzde 95’i 50 ms’nin altında, ama ani sıçramalar çok fena.

Bu ani sıçramaları ortadan kaldırmamızın yanı sıra, daha fazla eşin başarısız olduğu durumları da aşmamız gerekiyor. Şu anki haliyle, bir eşin tunnel'larımızı başarısız kıldığını 'öğrendiğimizde', aslında onların router'ına özgü hiçbir şey öğrenmiş olmuyoruz - eğer tam o sırada denk gelirsek bu sıçramalar, yüksek kapasiteli eşlerin bile yavaş görünmesine neden olabilir.

## 3) Akış kütüphanesi

Başarısız olan tunnel'ları atlatmanın ikinci kısmı kısmen streaming lib (akış kütüphanesi) tarafından gerçekleştirilecek - bize çok daha sağlam uçtan uca akış iletişimi sağlayarak. Bu tartışma yeni değil - lib bir süredir konuştuğumuz tüm o süslü özellikleri yapacak (ve elbette kendine düşen hatalar da olacak). Bu cephede çok ilerleme kaydedildi ve uygulama muhtemelen %60 oranında tamamlandı.

Daha fazla haber oldukça.

## 4) files.i2p

Ok, we've had a lot of new eepsites(I2P Sites) lately, which is kickass. I just want to point out this one especially as its got a pretty neat feature for the rest of us. If you haven't been to files.i2p, its basically a google-like search engine, with a cache of the sites it spiders (so you can both search and browse when the eepsite(I2P Site) is offline). v.cool.

## 5) ???

Bu haftanın durum notları oldukça kısa, ama pek çok şey oluyor - - toplantıdan önce daha fazlasını yazmaya zamanım yok. O halde, birkaç dakika içinde #i2p kanalına uğrayın, aptalca gözden kaçırdığım her ne varsa tartışabiliriz.

=jr
