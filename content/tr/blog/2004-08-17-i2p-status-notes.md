---
title: "2004-08-17 tarihli I2P Durum Notları"
date: 2004-08-17
author: "jr"
description: "Ağ performansı sorunlarını, DoS saldırılarını ve Stasher DHT (Dağıtık Hash Tablosu) geliştirme çalışmalarını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese selam, güncelleme zamanı

## Dizin:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Ağ durumu ve 0.3.4.3

Son bir hafta içinde ağ çalışır durumdaydı, ancak zaman zaman çok fazla sorun yaşandı ve güvenilirlikte dramatik bir düşüşe yol açtı. 0.3.4.2 sürümü, bazı uyumsuzluk ve zaman eşzamanlama sorunlarının neden olduğu bir DoS (Hizmet Engelleme) durumunu ele almada önemli ölçüde yardımcı oldu - DoS’u gösteren netDb (ağ veritabanı) istekleri grafiğine bakın (grafiğin dışına taşan ani sıçramalar); 0.3.4.2’nin devreye alınmasıyla bu durduruldu. Ne yazık ki bu da kendi sorunlar kümesini beraberinde getirdi ve bant genişliği grafiğinde görülebileceği gibi önemli sayıda mesajın yeniden iletilmesine neden oldu. Oradaki artan yük, kullanıcı etkinliğinde gerçek bir artıştan da kaynaklanıyordu, bu yüzden o kadar da /o kadar/ çılgınca değil ;) Ama yine de bir sorundu.

Son birkaç gündür oldukça bencil davrandım. Bir dizi hata düzeltmesini birkaç router üzerinde test edip dağıttık, ama henüz yayımlamadım; çünkü simülasyonlarımı çalıştırırken yazılımdaki uyumsuzlukların birbiriyle etkileşimini test etme fırsatını nadiren buluyorum. Bu yüzden, çok sayıda router berbat durumdayken router'ların iyi performans göstermesini sağlayacak yolları bulmak için ince ayar yaparken siz son derece boktan bir ağ işleyişine maruz kaldınız. Bu cephede ilerleme kaydediyoruz - netDb (ağ veritabanı) sömürüsünde bulunan eşleri profillemek ve onlardan kaçınmak, netDb istek kuyruklarını daha verimli yönetmek ve tunnel çeşitlendirmesini zorunlu kılmak.

Henüz orada değiliz, ama umutluyum. Şu anda canlı ağ üzerinde testler yürütülüyor ve hazır olduğunda, sonuçları içeren 0.3.4.3 sürümü yayımlanacak.

## 2) Stasher

Aum bir süredir kendi DHT’si (Dağıtık Karma Tablosu) üzerinde gerçekten harika işler çıkarıyor; şu anda bazı önemli sınırlamaları olsa da, umut verici görünüyor. Genel kullanım için kesinlikle henüz hazır değil, ama test (veya kod yazma :) konusunda ona yardımcı olmaya hazırsanız, siteye göz atın ve bir düğüm başlatın.

## 3) ???

Şimdilik bu kadar. Toplantı bir dakika önce başlamış olması gerektiğine göre, sanırım artık toparlamalıyım. Hepinizle #i2p kanalında görüşürüz!

=jr
