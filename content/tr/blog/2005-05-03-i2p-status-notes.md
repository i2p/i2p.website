---
title: "2005-05-03 için I2P Durum Notları"
date: 2005-05-03
author: "jr"
description: "Ağ kararlılığı, SSU UDP taşıma protokolünün canlı testlerindeki başarı, i2phex dosya paylaşımındaki ilerleme ve yaklaşan 3-4 haftalık yokluk hakkında haftalık güncelleme"
categories: ["status"]
---

Hi y'all, lots of stuff on the table this week

* Index

1) Ağ durumu 2) SSU durumu 3) i2phex 4) kayıp 5) ???

* 1) Net status

Genel ağ sağlığında büyük bir değişiklik yok; durum oldukça stabil görünüyor ve zaman zaman yaşanan dalgalanmalara rağmen hizmetler iyi durumda. Son sürümden bu yana CVS'e pek çok güncelleme yapıldı ancak işi tamamen durduracak nitelikte hata düzeltmeleri yok. Taşınmamdan önce, en güncel CVS'i daha fazla kullanıcıya ulaştırmak için bir sürüm daha çıkarabiliriz, ama henüz emin değilim.

* 2) SSU status

Benden sürekli UDP aktarımında büyük ilerleme olduğunu duymaktan bıktınız mı? Eh, ne yapalım — UDP aktarımında gerçekten çok ilerleme var. Hafta sonu boyunca özel ağ testlerinden çıkıp canlı ağa geçtik ve bir düzine kadar router yükseltme yaparak SSU adreslerini yayımladı — bu da onların çoğu kullanıcı için TCP aktarımı üzerinden erişilebilir olmasını sağlarken, SSU etkinleştirilmiş router'ların UDP üzerinden iletişim kurmasına olanak tanıdı.

Test süreci hâlâ çok erken aşamada, ancak beklediğimden çok daha iyi geçti. Tıkanıklık kontrolü gayet düzgün çalıştı ve hem aktarım hızı hem de gecikme oldukça yeterliydi - gerçek bant genişliği sınırlarını doğru şekilde belirleyebildi ve o bağlantıyı rekabet eden TCP akışlarıyla etkin biçimde paylaşabildi.

Yardımcı gönüllülerden toplanan istatistikler sayesinde, aşırı tıkanık ağlarda düzgün çalışabilmek için seçmeli onay (SACK) kodunun ne kadar önemli olduğu ortaya çıktı. Son birkaç günü bu kodu uygulayıp test etmekle geçirdim ve SSU belirtimini [1] yeni, verimli bir SACK tekniğini içerecek şekilde güncelledim. Bu, önceki SSU koduyla geriye dönük uyumlu olmayacak; bu yüzden test etmeye yardımcı olanların, yeni bir derleme test için hazır olana kadar (umarım bir iki gün içinde) SSU taşıma katmanını devre dışı bırakması gerekiyor.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup bir süredir phex'in i2p'ye portu üzerinde harıl harıl çalışıyor ve sıradan kullanıcı için hazır hâle gelmesine daha çok iş olsa da, bu akşam biraz önce onu çalıştırabildim, sirup'un paylaşıma açtığı dosyalara göz atabildim, biraz veri çekebildim ve *öksürür* "anlık" sohbet arayüzünü kullanabildim.

sirup'un eepsite(I2P Site) [2] üzerinde çok daha fazla bilgi var ve hâlihazırda i2p topluluğunda bulunan kişilerin test etmeye yardımcı olması harika olurdu (ancak lütfen, sirup bunu herkese açık bir sürüm olarak onaylayana ve i2p en az 0.6, hatta 1.0 olana kadar, bunu i2p topluluğu içinde tutalım). Sanırım sirup bu haftaki toplantıda olacak, belki o zaman daha fazla bilgi edinebiliriz!

[2] http://sirup.i2p/

* 4) awol

Hazır yeri gelmişken, muhtemelen gelecek haftaki toplantıda burada olmayacağım ve sonraki 3-4 hafta çevrimdışı olacağım. Bu muhtemelen yeni sürüm çıkmayacağı anlamına gelse de, insanların üzerinde çalışıp kurcalayabileceği gerçekten ilginç bir yığın şey hâlâ var:  = feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,     addressbook, susimail, q gibi uygulamalar ya da tamamen yeni bir şey.  = eepproxy - filtreleme,     kalıcı HTTP bağlantıları için     destek, 'listen on' ACL'leri ve belki de bir     exponential backoff (üstel geri bekleme stratejisi), outproxy (I2P dışa çıkış vekil sunucusu) zaman aşımıyla başa çıkmak için (     basit round robin yerine)  = PRNG (sözde rastgele sayı üreteci) (listede tartışıldığı gibi)  = PMTU (Yol MTU'su) kitaplığı (Java'da ya da JNI ile C'de)  = birim testi ödülü ve GCJ ödülü  = router bellek profilleme ve ince ayar  = ve çok daha fazlası.

Yani, canınız sıkılıyor ve yardımcı olmak istiyorsunuz ama ilhama da ihtiyaç duyuyorsanız, belki yukarıdakilerden biri sizi harekete geçirir. Muhtemelen ara sıra bir internet kafeye uğrarım, bu yüzden bana e-postayla ulaşabilirsiniz, ancak yanıt sürem gün mertebesinde olacaktır.

* 5) ???

Tamam, şimdilik değineceklerim aşağı yukarı bu kadar. Önümüzdeki hafta boyunca SSU testlerine yardımcı olmak isteyenler, blogumda [3] yer alacak bilgiler için gözünüzü açık tutun. Geri kalanınızla toplantıda görüşürüz!

=jr [3] http://jrandom.dev.i2p/
