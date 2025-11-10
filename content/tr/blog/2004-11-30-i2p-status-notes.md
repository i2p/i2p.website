---
title: "I2P Durum Notları 2004-11-30 için"
date: 2004-11-30
author: "jr"
description: "0.4.2 ve 0.4.2.1 sürümlerini, mail.i2p gelişmelerini, i2p-bt ilerlemesini ve eepsite güvenlik tartışmalarını kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet

## Dizin

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 ve 0.4.2.1

Nihayet 0.4.2’yi yayımladığımızdan beri, ağın güvenilirliği ve aktarım hızı bir süreliğine ciddi biçimde arttı, ta ki bizim yarattığımız yepyeni hatalarla karşılaşana kadar. Çoğu kişi için IRC bağlantıları saatlerce kesintisiz sürüyor, ancak bazı sorunlarla karşılaşanlar için süreç epey sarsıntılı geçti. Yine de çok sayıda düzeltme yapıldı ve bu gece ilerleyen saatlerde veya yarın sabahın erken saatlerinde indirilmeye hazır yeni 0.4.2.1 sürümümüz olacak.

## 2) mail.i2p

Bugün erken saatlerde postman, konuşmak istediği bazı konular olduğunu belirten bir not iletti - daha fazla bilgi için toplantı kayıtlarına bakın (ya da bunu toplantıdan önce okuyorsanız, uğrayın).

## 3) i2p-bt

Yeni sürümün dezavantajlarından biri, i2p-bt uyarlamasıyla ilgili bazı sorunlarla karşılaşıyor olmamız. Sorunların bir kısmı streaming lib (akış kütüphanesi) içinde tespit edilip bulunup düzeltildi, ancak ihtiyaç duyduğumuz noktaya getirmek için daha fazla çalışma gerekli.

## 4) eepsites(I2P Siteleri)

Son aylarda listede, kanalda ve forumda, eepsites(I2P Sites) ve eepproxy'nin nasıl çalıştığıyla ilgili bazı sorunlar hakkında tartışmalar oldu - yakın zamanda bazıları hangi başlıkların nasıl filtrelendiğine ilişkin sorunlardan bahsetti, diğerleri kötü yapılandırılmış tarayıcıların tehlikelerini gündeme getirdi ve risklerin çoğunu özetleyen DrWoo'nun bir sayfası da var. Özellikle dikkat çekici bir durum da şu: bazı kişiler, kullanıcılar applet'leri devre dışı bırakmazsa kullanıcının bilgisayarını ele geçirecek applet'ler üzerinde aktif olarak çalışıyor. (BU YÜZDEN TARAYICINIZDA JAVA VE JAVASCRIPT'İ DEVRE DIŞI BIRAKIN)

Bu, elbette, işleri nasıl güvence altına alabileceğimiz üzerine bir tartışmaya yol açıyor. Kendi tarayıcımızı geliştirmemiz veya önceden yapılandırılmış güvenli ayarlarla bir tarayıcıyı paketlememiz yönünde öneriler duydum, ama gerçekçi olalım - bu, burada kimsenin girişeceği bir işten çok daha fazla emek gerektirir. Ancak, üç başka yaklaşım var:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

İlki, şu anda sahip olduğumuzla hemen hemen aynı; tek fark, içeriği muffin veya freenet'in anonimlik filtresi gibi bir şey üzerinden geçirip filtrelememiz.

Buradaki dezavantaj, bunun hâlâ HTTP başlıklarını açığa çıkarması; dolayısıyla HTTP tarafını da anonimleştirmemiz gerekecek.

İkincisi, CGIproxy ile `http://duck.i2p/` üzerinde gördüğünüze çok benzer; alternatif olarak freenet'in fproxy'sinde gördüğünüz gibidir. Bu, HTTP tarafını da kapsar.

Üçüncü seçeneğin avantajları ve dezavantajları var - çok daha etkileyici arayüzleri kullanmamıza olanak tanır (bazı bilinen güvenli javascript’i vb. güvenle kullanabildiğimiz için), ancak geriye dönük uyumsuzluk gibi bir dezavantajı var. Belki de bunun bir filtreyle birleştirilmesi, makroları filtrelenmiş html içine gömmenize olanak sağlar mı?

Her neyse, bu önemli bir geliştirme çalışması ve I2P'nin en güçlü kullanım alanlarından biri olan güvenli ve anonim etkileşimli web sitelerini ele alıyor. Belki gerekeni nasıl elde edebileceğimize dair başka fikirleri ya da bilgileri olan birileri vardır?

## 5) ???

Tamam, toplantıya geç kalıyorum, bu yüzden sanırım bunu imzalayıp göndermeliyim, ha?

=jr [bakalım gpg'yi düzgün çalıştırabilecek miyim...]
