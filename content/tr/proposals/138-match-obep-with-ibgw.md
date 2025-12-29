---
title: "OBEP'leri IBGW'lerle Eşleştirme"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Açık"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Genel Bakış

Bu öneri, bir mesaj gönderildiğinde tünellerin, hedef Destination'un LeaseSet'inin IBGW'lerinden biriyle eşleşecek şekilde seçilmesine veya kurulmasına neden olan outbound tünelleri için bir I2CP seçeneği ekler.


## Motivasyon

Çoğu I2P yönlendiricisi, tıkanıklık yönetimi için bir çeşit paket düşürme kullanır. Referans uygulama, hem mesaj boyutunu hem de seyahat mesafesini dikkate alan bir WRED stratejisi kullanır (bkz. [tunnel throttling belgeleri](/docs/specs/implementation/#tunnelthrottling)). Bu strateji nedeniyle, paket kaybının ana kaynağı OBEP'tir.


## Tasarım

Bir mesaj gönderirken, gönderen, OBEP'sinin alıcının IBGW'lerinden biriyle aynı yönlendirici olduğu bir tünel seçer veya kurar. Böylece, mesaj bir tünelden çıkıp diğerine doğrudan gider, arada kablo üzerinden gönderilmesine gerek kalmaz.


## Güvenlik etkileri

Bu mod, alıcının göndericinin OBEP'sini seçtiği anlamına gelir. Mevcut gizliliği korumak için, bu mod outbound tünellerin, outbound.length I2CP seçeneği tarafından belirtilenden bir adım daha uzun inşa edilmesine neden olur (son adım muhtemelen gönderenin hızlı katmanının dışında olabilir).


## Şartname

[I2CP spesifikasyonu](/docs/specs/i2cp/)'na yeni bir I2CP seçeneği eklendi:

    outbound.matchEndWithTarget
        Boolean

        Varsayılan değer: duruma özgü

        Eğer true ise, yönlendirici, bu oturum sırasında gönderilen
        mesajlar için, tünelin OBEP'si hedef Destination'un
        IBGW'lerinden biri olacak şekilde outbound tüneller seçer.
        Eğer böyle bir tünel yoksa, yönlendirici bir tane kurar.


## Uyumluluk

Geriye dönük uyumluluk sağlanır, zira yönlendiriciler her zaman mesajları kendilerine gönderebilir.


## Uygulama

### Java I2P

Tünel kurma ve mesaj gönderme şu anda ayrı alt sistemlerdir:

- BuildExecutor yalnızca outbound tünel havuzunun outbound.* seçeneklerini bilir
  ve kullanımına ilişkin bir görüşü yoktur.

- OutboundClientMessageOneShotJob yalnızca mevcut
  havuzdan bir tünel seçebilir; bir müşteri mesajı
  geldiğinde ve outbound tünel yoksa, yönlendirici mesajı
  düşürür.

Bu öneriyi uygulamak, bu iki alt sistemin etkileşimde bulunması için bir yol tasarlanmasını gerektirir.

### i2pd

Bir test uygulaması tamamlandı.


## Performans

Bu önerinin gecikme, RTT ve paket kaybı üzerinde çeşitli etkileri vardır:

- Çoğu durumda, bu modun mevcut bir tünel yerine ilk mesajda yeni bir tünel kurulmasını gerektirmesi muhtemeldir, bu da gecikme ekler.

- Standart tüneller için, OBEP muhtemelen IBGW'yi bulup bağlanması gerektiğinde, ilk RTT'yi artıran gecikme ekler (bu ilk paket gönderildikten sonra olur). Bu modu kullanarak, OBEP tünel kurulumu sırasında IBGW'yi bulup bağlanmalıdır, aynı gecikmeyi ekler ancak ilk RTT'yi azaltır (bu ilk paket gönderilmeden önce olur).

- Şu anda standart olan VariableTunnelBuild boyutu 2641 bayttır. Böylece, bu modun bu boyuttan büyük ortalama mesaj boyutlarına sahip mesajlar için daha düşük paket kaybı sonucunu doğuracağı öngörülmektedir.

Bu etkileri araştırmak için daha fazla araştırma gereklidir, böylece hangi standart tünellerin bu modun varsayılan olarak etkinleştirilmesinden fayda sağlayacağına karar verilebilir.
