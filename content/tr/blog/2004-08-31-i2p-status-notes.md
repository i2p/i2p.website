---
title: "2004-08-31 tarihli I2P Durum Notları"
date: 2004-08-31
author: "jr"
description: "Ağ performansındaki bozulmayı, 0.3.5 sürümü için planlamayı, dokümantasyon gereksinimlerini ve Stasher DHT (dağıtık karma tablosu) ilerlemesini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Evet kızlar ve erkekler, yine Salı!

## Dizin:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Şey, eminim hepiniz fark etmişsinizdir, ağdaki kullanıcı sayısı oldukça sabit kaldıysa da performans son birkaç gündür belirgin biçimde kötüleşti. Bunun kaynağı, geçen hafta küçük bir DoS yaşandığında açığa çıkan, eş seçimi ve mesaj iletimi kodundaki bir dizi hataydı. Sonuç olarak, esasen herkesin tunnel'ları sürekli olarak başarısız oluyor; bu da biraz kartopu etkisi yaratıyor. Yani hayır, sorun sadece sizde değil - ağ bizim geri kalanımız için de berbat ;)

Ama iyi haber şu ki sorunları oldukça hızlı düzelttik ve bunlar geçen haftadan beri CVS'te, fakat bir sonraki sürüm çıkana kadar ağ hâlâ kullanıcılar için berbat olacak. Bu vesileyle...

## 2) 0.3.5 ve 0.4

Bir sonraki sürüm, 0.4 sürümü için planladığımız tüm yenilikleri içerecek (yeni yükleyici, yeni web arayüzü standardı, yeni i2ptunnel arayüzü, sistem tepsisi ve Windows hizmeti, iş parçacığı iyileştirmeleri, hata düzeltmeleri vb.), ancak son sürümün zaman içinde bozulma biçimi çok şey anlatıyordu. Bu sürümlerde daha yavaş ilerlemek istiyorum; daha kapsamlı biçimde dağıtılmaları ve pürüzlerin kendini göstermesi için onlara zaman tanıyalım. Simülatör temelleri inceleyebilse de, canlı ağda gördüğümüz doğal ağ sorunlarını simüle etmenin bir yolu yok (en azından şimdilik).

Bu nedenle, bir sonraki sürüm 0.3.5 olacak - umarız 0.3.* serisindeki son sürüm olur, ancak başka sorunlar ortaya çıkarsa belki de olmayabilir. Haziran ayında çevrimdışıyken ağın nasıl çalıştığına baktığımda, yaklaşık iki hafta sonra işler bozulmaya başladı. Bu nedenle, en az iki hafta boyunca yüksek bir güvenilirlik düzeyini sürdürebilene kadar bizi bir sonraki 0.4 sürüm düzeyine yükseltmeyi erteleme düşüncesindeyim. Elbette bu, bu arada çalışmayacağımız anlamına gelmiyor.

Her neyse, geçen hafta belirtildiği gibi, hypercubus yeni kurulum sistemi üzerinde dur durak bilmeden çalışıyor; benim sürekli bir şeyleri değiştirip tuhaf sistemler için destek istememle de başa çıkıyor. Önümüzdeki birkaç gün içinde her şeyi netleştirip önümüzdeki birkaç gün içinde 0.3.5 sürümünü yayınlayabilmeliyiz.

## 3) dokümantasyon

0.4'ten önceki iki haftalık "test penceresi" sırasında yapmamız gereken önemli şeylerden biri, çılgınlar gibi belgelendirme yapmaktır. Merak ettiğim, belgelendirmemizde eksik olduğunu düşündüğünüz şeyler neler - yanıtlamamız gereken hangi sorularınız var? Her ne kadar "tamam, şimdi gidin o belgeleri yazın" demek istesem de, gerçekçiyim; bu yüzden tek istediğim, o belgelerin hangi konuları ele alacağını belirlemeniz.

Örneğin, şu anda üzerinde çalıştığım belgelerden biri tehdit modelinin gözden geçirilmiş sürümü; bunu artık, I2P'nin farklı bireylerin ihtiyaçlarına nasıl hizmet edebileceğini açıklayan bir dizi kullanım senaryosu olarak tanımlıyorum; bu senaryolar, işlevsellik, kişinin endişe duyduğu saldırganlar ve kendini nasıl savunduğu gibi unsurları içerir.

Sorunuzun yanıtlanması için ayrıntılı bir belge gerekmiyorsa, onu yalnızca bir soru olarak ifade edin; SSS'ye ekleyebiliriz.

## 4) stasher güncellemesi

Aum bugün erken saatlerde bir güncellemeyle kanala uğradı (ben de ona sorular yağdırırken):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Yani, gördüğünüz gibi, çok ama çok ilerleme var. Anahtarlar DHT katmanının üzerinde doğrulansa bile, bu acayip havalı (bence). Hadi aum!

## 5) ???

Tamam, söyleyeceklerim bu kadar (ki bu iyi, çünkü toplantı birazdan başlıyor)... uğrayın ve ne istiyorsanız söyleyin!

=jr
