---
title: "2005-11-01 için I2P Durum Notları"
date: 2005-11-01
author: "jr"
description: "0.6.1.4 sürümünün başarılı şekilde yayınlanması, bootstrap saldırısı analizi, I2Phex 0.1.1.34 güvenlik düzeltmeleri, voi2p ses uygulamasının geliştirilmesi ve Syndie RSS besleği entegrasyonunu kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, yine haftanın o vakti geldi

* Index

1) 0.6.1.4 ve ağ durumu 2) önyüklemeler, öncüller, küresel pasif saldırganlar ve CBR 3) i2phex 0.1.1.34 4) voi2p uygulaması 5) syndie ve sucker 6) ???

* 1) 0.6.1.4 and net status

Geçen cumartesi günkü 0.6.1.4 sürümü oldukça sorunsuz geçti gibi görünüyor - ağın %75'i zaten güncelledi (teşekkürler!) ve kalanların çoğu da zaten 0.6.1.3 kullanıyor. Her şey makul derecede iyi çalışıyor gibi ve bununla ilgili pek geri bildirim duymadım - ne olumlu ne de olumsuz, kötü olsaydı yüksek sesle şikayet edeceğinizi varsayıyorum :)

Özellikle, çevirmeli modem bağlantısı kullanan kişilerden her türlü geri bildirimi almak isterim, çünkü yaptığım testler bu tür bir bağlantıyı yalnızca temel düzeyde simüle ediyor.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Listede birkaç fikirle ilgili çok daha fazla tartışma oldu ve başlatma (bootstrap) saldırılarının bir özeti çevrimiçi [1] yayımlandı. 3. seçenek için kriptografi gereksinimlerini belirleme konusunda biraz ilerleme kaydettim ve henüz hiçbir şey yayımlanmamış olsa da, oldukça basit.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Sabit bit hızı (CBR) tunnel kullanımıyla güçlü saldırganlara karşı direnci nasıl artırabileceğimiz konusunda daha fazla tartışma yapıldı ve bu yaklaşımı araştırma seçeneğimiz olsa da, doğru kullanımının ciddi ölçüde kaynak gerektirmesi nedeniyle şu anda I2P 3.0 için planlanmış durumda; ayrıca böyle bir ek yükle I2P’yi kullanmaya kimin istekli olacağı ve hangi grupların bunu yapabilecekleri ya da hiç yapamayacakları üzerinde muhtemelen ölçülebilir bir etkisi olacaktır.

* 3) I2Phex 0.1.1.34

Geçen cumartesi günü ayrıca yeni bir I2Phex sürümü yayınlandı [2], I2Phex'in eninde sonunda çalışmaz hale gelmesine yol açan bir dosya tanımlayıcısı sızıntısını gideriyor (teşekkürler Complication!) ve insanların I2Phex örneğinize uzaktan belirli dosyaları indirtmelerine izin veren bazı kodları kaldırıyor (teşekkürler GregorK!). Güncellemeniz şiddetle önerilir.

Ayrıca, CVS sürümüne (henüz yayımlanmadı) bazı eşzamanlama sorunlarını gideren bir güncelleme de yapıldı - Phex bazı ağ işlemlerinin anında gerçekleştirileceğini varsayıyor, oysa I2P bazen bir şeyleri yapmak için biraz zamana ihtiyaç duyabiliyor :) Bu durum, grafik kullanıcı arayüzünün (GUI) bir süre takılı kalması, indirme veya yüklemelerin duraksaması ya da bağlantıların reddedilmesi (ve belki birkaç başka şekilde) olarak kendini gösterebiliyor. Henüz fazla test edilmedi, ancak muhtemelen bu hafta 0.1.1.35 sürümüyle yayımlanacak. Daha fazla haber olduğunda, eminim forumda daha fazlası paylaşılacaktır.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum, yeni I2P üzerinden çalışan ses (ve metin) uygulaması üzerinde harıl harıl çalışıyor ve her ne kadar ben henüz görmemiş olsam da kulağa hoş geliyor. Belki Aum toplantıda bize bir güncelleme verebilir ya da ilk alfa sürümünü sabırla bekleyebiliriz :)

* 5) syndie and sucker

dust bir süredir syndie ve sucker üzerinde çalışıyor ve I2P’nin en son CVS derlemesi artık RSS ve atom beslemelerinden içeriği otomatik olarak çekmenize ve bunları syndie blogunuza göndermenize olanak tanıyor. Şu anda, lib/rome-0.7.jar ve lib/jdom.jar dosyalarını wrapper.config dosyanıza (wrapper.java.classpath.20 and 21) açıkça eklemeniz gerekiyor, ancak bunu daha sonra gerekli olmayacak şekilde paketleyeceğiz. Bu hâlâ devam eden bir çalışma ve rome 0.8 (henüz yayımlanmadı) beslemeden enclosures (ek öğeleri) yakalama gibi gerçekten hoş özellikler sunuyor gibi görünüyor; sucker da bunları daha sonra bir syndie gönderisine ek olarak içe aktarabilecek (şu anda zaten görselleri ve bağlantıları da işliyor!).

Diğer tüm RSS beslemelerinde olduğu gibi, içeriğin nasıl dahil edildiği konusunda bazı tutarsızlıklar var; bu nedenle bazı beslemeler diğerlerinden daha sorunsuz işleniyor. Bence insanlar farklı beslemelerle test etmeye yardımcı olur ve takıldığı sorunları dust’a bildirirlerse faydalı olabilir. Her hâlükârda, bu işler oldukça heyecan verici görünüyor, güzel iş, dust!

* 6) ???

Şimdilik bu kadar, ama eğer birinin soruları varsa ya da bazı konuları daha ayrıntılı tartışmak isterse, GMT 20:00'deki toplantıya uğrayın (yaz saati uygulamasını unutmayın!).

=jr
