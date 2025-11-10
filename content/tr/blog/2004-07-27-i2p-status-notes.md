---
title: "2004-07-27 tarihli I2P Durum Notları"
date: 2004-07-27
author: "jr"
description: "0.3.3 sürümündeki performans sorunlarını ve yaklaşan optimizasyonları ele alan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet,
haftalık söylenme seansı vakti

## Dizin:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Geçtiğimiz Cuma 0.3.3 sürümünü yayımladık ve bir-iki günlük epey çalkantılı bir dönemin ardından fena gitmiyor gibi görünüyor. 0.3.2.3 kadar iyi değil, ama genellikle irc.duck.i2p'ye 2-7 saatlik oturumlar boyunca bağlı kalabildim. Ancak pek çok kişinin sorun yaşadığını gördüğüm için logger'ı çalıştırdım ve neler olup bittiğini ayrıntılı olarak izledim. Kısa cevap şu: Gerektiğinden fazla bant genişliği kullanıyorduk; bu da ağ sıkışıklığına ve tunnel başarısızlıklarına (test iletilerinin zaman aşımına uğraması vb. nedenlerle) yol açıyordu.

Son birkaç günü yeniden simülatörde geçirip, neleri iyileştirebileceğimizi görmek için bir ağ üzerinden bir dizi heartbeat (nabız sinyali) çalıştırdım ve buna dayanarak bir sürü güncelleme yolda:

### netDb update to operate more efficiently

Mevcut netDb sorgu iletileri 10+KB'ye kadar olabilir ve başarılı yanıtlar sık olsa da, başarısız yanıtlar 30+KB'ye kadar olabilir (çünkü her ikisi de tam RouterInfo yapıları içerir). Yeni netDb, bu tam RouterInfo yapılarını router'ın hash'i ile değiştirerek 10KB ve 30KB iletileri ~100 baytlık iletilere dönüştürüyor.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Bu yapılar eski bir fikrin kalıntılarıydı ancak sistemin anonimliğine veya güvenliğine herhangi bir değer katmıyor. Bunları daha basit bir yanıt veri noktaları kümesi lehine kaldırarak, tunnel (tünel) yönetimi mesaj boyutlarını önemli ölçüde azaltıyor ve garlic encryption süresini yarıya indiriyoruz.

### netDb'nin daha verimli çalışması için güncelleme

Kod, tunnel oluşturma sırasında biraz fazla 'konuşkandı'; bu nedenle gereksiz mesajlar kesildi.

### SourceRouteBlock'u ve SourceRouteReplyMessage'i atın

Garlic routing (garlic yönlendirme) için kripto kodunun bazı bölümleri, kullanmadığımız bazı garlic routing tekniklerine dayanarak sabit dolgu kullanıyordu (Eylül ve Ekim aylarında bunu yazdığımda, tunnels yerine çok atlamalı garlic routing yapacağımızı sanıyordum).

Ayrıca, her atlama için tunnel ID’lerini eklemek üzere tunnel yönlendirmesine tam kapsamlı bir güncelleme yapıp yapamayacağımı araştırıyorum.

Yol haritasından da görebileceğiniz gibi, bu 0.4.1 sürümünün büyük bir bölümünü kapsıyor, ancak netDb değişikliği geriye dönük uyumluluğun kaybedilmesi anlamına geldiğinden, geriye dönük uyumlu olmayan bir dizi işi de tek seferde tamamlayabiliriz.

Hâlâ simülasyonda testler çalıştırıyorum ve per-hop tunnel id (her atlama için 'tunnel' kimliği) işini tamamlayıp tamamlayamayacağımı görmem gerekiyor, ama bir iki gün içinde yeni bir yama sürümü yayımlamayı umuyorum. Geriye dönük uyumlu olmayacak, bu yüzden yükseltme biraz sarsıntılı olacak, ama buna değecek.

## 2) NativeBigInteger

Iakin, Freenet ekibi için NativeBigInteger kodunda bazı güncellemeler yapıyor; bizim kullanmadığımız bazı kısımları optimize ediyor, ayrıca doğru native library (yerel kütüphane)’yi otomatik olarak seçmemizi sağlayacak CPU tespit kodu da hazırlıyor. Bu, jbigi’yi varsayılan kurulumla tek bir lib içinde dağıtabileceğimiz ve kullanıcıdan herhangi bir şey istemeden doğru olanı seçeceği anlamına geliyor. Ayrıca, bunu kaynak kodumuza dahil edebilmemiz için yaptığı değişiklikleri ve yeni CPU tespit kodunu yayımlamayı da kabul etti (yaşasın Iakin!). Bunun ne zaman dağıtılacağını bilmiyorum, ancak dağıtıldığında insanlara haber vereceğim; çünkü mevcut jbigi kütüphanelerine sahip olanların muhtemelen yenisine ihtiyacı olacak.

## 3) ???

Eh, geçen hafta çoğunlukla koda gömülmüş durumdaydık, bu yüzden çok fazla güncelleme yok. Başka gündeme getirmek istediğiniz bir şey var mı? Varsa, bu akşam 21:00 GMT’de #i2p’deki toplantıya uğrayın.

=jr
