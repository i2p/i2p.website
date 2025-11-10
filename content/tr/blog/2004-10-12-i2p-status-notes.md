---
title: "2004-10-12 için I2P Durum Notları"
date: 2004-10-12
author: "jr"
description: "0.4.1.2 sürümünü, dinamik kısıtlama deneylerini, 0.4.2 sürümü için akış kütüphanesi geliştirme çalışmalarını ve e-posta tartışmalarını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam ekip, haftalık güncellememizin zamanı geldi

## Dizin:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

Yeni 0.4.1.2 sürümü birkaç gündür yayında ve işler büyük ölçüde beklendiği gibi gidiyor - yine de yeni watchdog bileşeninde birkaç pürüz oldu, bu da işler 'Bad' olduğunda router'ınızı yeniden başlatmak yerine öldürmesine neden oluyor. Bugün daha önce belirttiğim gibi, bana bazı veriler göndermek için yeni istatistik günlükleme aracını kullanacak kişiler arıyorum, bu nedenle bu konudaki yardımınız çok takdir edilecektir.

## 2) 0.4.1.3

0.4.2 çıkmadan önce bir sürüm daha olacak, çünkü devam etmeden önce ağın mümkün olduğunca kararlı olmasını istiyorum. Şu anda denediğim şey, tunnel katılımı üzerinde dinamik bir kısıtlama - router'lara, aşırı yüklenmişlerse veya tunnel'ları her zamankinden yavaşsa istekleri olasılıksal olarak reddetmelerini söylemek. Bu olasılıklar ve eşikler, tutulan istatistiklerden dinamik olarak hesaplanıyor - 10 dakikalık tunnel test süreniz 60 dakikalık tunnel test sürenizden büyükse, tunnel isteğini 60minRate/10minRate olasılığıyla kabul edin (ve mevcut tunnel sayınız 60 dakikalık ortalama tunnel sayınızdan büyükse, onu p=60mRate/curTunnels olasılığıyla kabul edin).

Bir başka olası kısıtlama, bant genişliğini bu doğrultuda yumuşatmak - bant genişliği kullanımımız sıçradığında tunnels (tüneller) olasılıksal olarak reddetmek. Her neyse, tüm bunların amacı, ağ kullanımını yaymaya ve tunnels'ı daha fazla kişi arasında dengelemeye yardımcı olmaktır. Yük dengelemede yaşadığımız başlıca sorun, ezici bir kapasite *fazlası* olmasıydı ve bu nedenle "kahretsin, yavaşız, reddedelim" tetikleyicilerimizin hiçbiri tetiklenmedi. Bu yeni olasılıksal olanlar umarız hızlı değişimi kontrol altında tutar.

0.4.1.3 sürümünün ne zaman çıkacağına dair belirli bir planım yok - belki hafta sonu. İnsanların (yukarıdaki) gönderdiği veriler, buna değip değmeyeceğini ya da daha faydalı başka yollar olup olmadığını belirlemeye yardımcı olmalı.

## 3) 0.4.2

Geçen haftaki toplantıda konuştuğumuz gibi, 0.4.2 ve 0.4.3 sürümlerini yer değiştirdik - 0.4.2 yeni streaming kütüphanesi olacak ve 0.4.3 tunnel güncellemesi olacak.

TCP'nin akış işlevselliğine ilişkin literatürü yeniden gözden geçiriyorum ve I2P açısından dikkate değer bazı konular var. Özellikle, yüksek round trip time'ımız (gidiş-dönüş süresi) bizi XCP benzeri bir yaklaşıma yöneltiyor ve explicit congestion notification'ın (açık tıkanıklık bildirimi) çeşitli biçimlerinde muhtemelen oldukça agresif olmalıyız; ancak saatlerimiz bir dakikaya kadar kayabildiği için timestamp option (zaman damgası seçeneği) gibi bir şeyden yararlanamayız.

Ek olarak, kısa ömürlü bağlantıları işleyebilmesi için streaming lib'i (akış kitaplığı) eniyileyebildiğimizden emin olmak isteyeceğiz (ki standart TCP bu konuda pek iyi değildir) - örneğin, küçük (<32KB) HTTP GET isteklerini ve küçük (<32KB) yanıtları tam olarak üç mesajda gönderebilmek istiyorum:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
Her neyse, bunun için henüz pek fazla kod yazılmadı; protokol tarafı büyük ölçüde TCP'ye benzer görünüyor ve paketler de human'ın önerisi ile eski önerinin birleştirilmiş haline benziyor. Herhangi bir önerisi ya da fikri olan veya gerçeklemeye yardımcı olmak isteyen olursa, lütfen iletişime geçin.

## 4) e-posta tartışması

I2P içinde (ve dışında) e-posta ile ilgili bazı ilginç tartışmalar oldu - postman bir dizi fikri çevrimiçi olarak paylaştı ve öneriler arıyor. #mail.i2p kanalında da ilgili tartışmalar yapıldı. Belki postman’dan bir güncelleme alabiliriz?

## 5) ???

Şimdilik bu kadar. Birkaç dakika içinde toplantıya uğra ve yorumlarını getir :)

=jr
