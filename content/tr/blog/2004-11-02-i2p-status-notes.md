---
title: "2004-11-02 tarihli I2P Durum Notları"
date: 2004-11-02
author: "jr"
description: "Ağ durumu, çekirdek bellek iyileştirmeleri, tunnel yönlendirme güvenlik düzeltmeleri, akış kitaplığı ilerlemesi ve posta/BitTorrent gelişmelerini kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Herkese selam, haftalık güncelleme zamanı

## Dizin:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Ağ durumu

Hemen hemen eskisi gibi - sabit sayıda eş, eepsites(I2P Sites) oldukça erişilebilir ve saatlerce IRC. Çeşitli eepsites(I2P Sites) için erişilebilirliğe birkaç farklı sayfa üzerinden göz atabilirsiniz: - `http://gott.i2p/sites.html` - `http://www.baffled.i2p/links.html` - `http://thetower.i2p/pings.txt`

## 2) Çekirdek güncellemeleri

Kanalda takılanlar (ya da CVS günlüklerini okuyanlar), son sürümden bu yana epey zaman geçmiş olsa da birçok şeyin olup bittiğini gördünüz. 0.4.1.3 sürümünden bu yana yapılan değişikliklerin tam listesini çevrimiçi bulabilirsiniz, ancak iki büyük değişiklik var, biri iyi, biri kötü:

İyi olan şu ki, her türden delice geçici nesne oluşturulmasının yol açtığı bellek tahsis/serbest bırakma trafiğini büyük ölçüde azalttık. Yeni akış kütüphanesini hata ayıklarken GC (çöp toplayıcı) delirmesini izlemekten sonunda bıktım; bu yüzden birkaç gün süren profil çıkarma, ince ayar ve optimizasyondan sonra en çirkin kısımlar temizlendi.

Kötüsü, bazı tunnel üzerinden yönlendirilen mesajların nasıl ele alındığına ilişkin bir hata düzeltmesi - bazı durumlarda bir mesaj, teslimattan önce tunnel üzerinden yönlendirilmesi yerine doğrudan hedeflenen router'a gönderiliyordu; bu da biraz kod yazabilen bir saldırgan tarafından istismar edilebilirdi. Artık şüphe durumunda doğru şekilde tunnel üzerinden yönlendiriyoruz.

Bu kulağa iyi gelebilir, ama 'kötü' yanı, ek atlamalar (hop) nedeniyle gecikmede bir miktar artış olacağı anlamına gelmesidir, gerçi bunlar zaten kullanılması gereken atlamalardır.

Çekirdekte başka hata ayıklama çalışmaları da sürüyor, bu yüzden henüz resmî bir sürüm yayınlanmadı - CVS HEAD 0.4.1.3-8. Önümüzdeki birkaç gün içinde muhtemelen tüm o işleri halletmek için 0.4.1.4 sürümünü yayınlayacağız. Elbette yeni streaming lib (akış kütüphanesi) içermeyecek.

## 3) Akış kütüphanesi

Streaming lib (streaming kütüphanesi) konusuna gelmişken, burada epey ilerleme kaydedildi ve eski ve yeni kütüphanelerin yan yana karşılaştırması iyi görünüyor. Ancak yapılacak işler hâlâ var ve geçen sefer söylediğim gibi, bunu aceleye getirip yayınlamayacağız. Bu da yol haritasının sarktığı anlamına geliyor; muhtemelen 2-3 haftalık bir gecikme söz konusu. Daha fazla ayrıntı hazır olduğunda paylaşacağız.

## 4) mail.i2p ilerleme durumu

Bu hafta çok sayıda yenilik - giriş ve çıkış vekil sunucuları çalışıyor! Daha fazla bilgi için www.postman.i2p adresine bakın.

## 5) BT ilerleme durumu

Son zamanlarda bir BitTorrent istemcisinin port edilmesi ve bazı tracker ayarlarının güncellenmesi konusunda yoğun bir hareketlilik yaşandı. Belki toplantı sırasında bu işlere dahil olanlardan bazı güncellemeler alabiliriz.

## 6) ???

Benden bu kadar. Gecikme için kusura bakmayın, şu yaz saati zımbırtısını tamamen unutmuşum. Neyse, birazdan görüşürüz.

=jr
