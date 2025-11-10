---
title: "2004-11-16 tarihli I2P Durum Notları"
date: 2004-11-16
author: "jr"
description: "Ağ tıkanıklığı sorunlarını, akış kütüphanesindeki gelişmeleri, BitTorrent'teki ilerlemeleri ve yaklaşan sürüm planlarını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, yine salı.

## Dizin

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Tıkanıklık

Biliyorum, 1. maddeye "Net status" adını verme alışkanlığımı bozuyorum, ama bu hafta "tıkanıklık" daha uygun görünüyor. Ağın kendisi oldukça iyi gidiyordu, ancak BitTorrent kullanımının artmasıyla işler giderek daha fazla tıkanmaya başladı ve bu da esasen bir congestion collapse (ağ tıkanıklığına bağlı çöküş) ile sonuçlandı.

Bu bekleniyordu ve yalnızca planımızı pekiştiriyor - yeni akış kütüphanesini kullanıma sunmak ve tunnel yönetimimizi, hızlı eşlerimiz başarısız olduğunda kullanabilmek için eşler hakkında yeterli veriye sahip olacağımız şekilde yenilemek. Son ağ sorunlarında başka bazı etkenler de etkendi, ancak büyük bölümü ağ tıkanıklığındaki artışa ve bunun sonucunda ortaya çıkan tunnel başarısızlıklarına bağlanabilir (bu da dolayısıyla her türden dengesiz eş seçimine yol açtı).

## 2) Akış

streaming lib (akış kütüphanesi) ile ilgili epey ilerleme kaydedildi ve canlı ağ üzerinden ona bir squid proxy bağladım; bunu normal web gezintim için sık sık kullanıyorum. mule’un yardımıyla, ağ üzerinden frost ve FUQID geçirerek akışları epey de zorladık (aman tanrım, bunu yapmadan önce frost’un ne kadar saldırgan olduğunu hiç fark etmemiştim!). Bu yolla birkaç önemli ve uzun süredir devam eden hata tespit edildi ve devasa sayıda bağlantıyı kontrol etmeye yardımcı olacak bazı ayarlamalar eklendi.

Toplu akışlar da hem yavaş başlangıç hem de tıkanıklık önleme ile harika çalışıyor ve hızlı gönder/yanıt bağlantıları (HTTP get+response gibi) tam olarak yapmaları gerekeni yapıyor.

Önümüzdeki birkaç gün içinde bazı gönüllüleri bunu daha yaygın şekilde devreye almayı denemeleri için görevlendirmeyi bekliyorum ve umarım yakında bizi 0.4.2 seviyesine ulaştırır. Bulaşıklarınızı yıkayacak kadar iyi olacağını söylemek istemem ve aradan sızacak hatalar olacağından eminim, ama yine de umut verici görünüyor.

## 3) BT

Son dönemdeki ağ sorunları bir kenara bırakılırsa, i2p-bt portu büyük ilerlemeler kaydediyor. Birkaç kişinin onun üzerinden 1 GB’den fazla veri indirdiğini biliyorum ve performans beklendiği gibi oldu (eski streaming lib (akış kütüphanesi) nedeniyle, swarm (torrent paylaşım kümesi) içindeki her eş için ~4KBps). #i2p-bt kanalında tartışılan çalışmaları takip etmeye çalışıyorum — belki duck toplantıda bize bir özet verebilir?

## 4) ???

Şimdilik benden bu kadar. Birkaç dakika içinde toplantıda hepinizle görüşürüz.

=jr
