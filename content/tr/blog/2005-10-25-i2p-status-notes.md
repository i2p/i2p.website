---
title: "2005-10-25 için I2P Durum Notları"
date: 2005-10-25
author: "jr"
description: "Ağın 400-500 eşe kadar büyümesi, Fortuna PRNG entegrasyonu, GCJ yerel derleme desteği, i2psnark hafif torrent istemcisi ve tunnel bootstrap (önyükleme) saldırısı analizini kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, cepheden yeni haberler

* Index

1) Ağ durumu 2) Fortuna entegrasyonu 3) GCJ durumu 4) i2psnark geri dönüyor 5) Bootstrapping (başlatma/önyükleme süreci) hakkında daha fazlası 6) Virüs incelemeleri 7) ???

* 1) Net status

Geçen hafta ağda oldukça iyi geçti - işler oldukça kararlı görünüyor, aktarım hızı normal ve ağ 4-500 eş düğüm (peer) aralığına doğru büyümeye devam ediyor. 0.6.1.3 sürümünden bu yana bazı önemli iyileştirmeler de yapıldı ve bunlar performans ve güvenilirliği etkiledikleri için, bu hafta ilerleyen günlerde 0.6.1.4 sürümünü yayınlayacağımızı bekliyorum.

* 2) Fortuna integration

Casey Marshall'ın hızlı düzeltmesi [1] sayesinde, GNU-Crypto'nun Fortuna [2] sözde rastgele sayı üretecini entegre edebildik. Bu, blackdown JVM ile yaşadığımız pek çok hayal kırıklığının kaynağını ortadan kaldırıyor ve GCJ ile sorunsuz çalışmamızı sağlıyor. Fortuna'yı I2P'ye entegre etmek, smeghead'in "pants"i (bir 'ant' tabanlı 'portage') geliştirmesinin başlıca nedenlerinden biriydi; dolayısıyla şimdi "pants"in bir başka başarılı kullanımını daha gerçekleştirmiş olduk :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Listede [3] belirtildiği gibi, artık router'ı ve çoğu istemciyi GCJ [4] ile sorunsuz çalıştırabiliyoruz. Web konsolunun kendisi hâlâ tam olarak çalışmıyor, bu yüzden router.config ile kendi router yapılandırmanızı yapmanız gerekiyor (yine de bir dakika kadar sonra kendiliğinden çalışmalı ve tunnel'larınızı başlatmalıdır). GCJ'nin sürüm planlarımıza nasıl uyacağı konusunda tam olarak emin değilim, ancak şu anda saf java dağıtıp hem java hem de yerel olarak derlenmiş sürümleri destekleme eğilimindeyim. Farklı işletim sistemleri ve kütüphane sürümleri için pek çok farklı derlemeyi oluşturup dağıtmak biraz zahmetli. Bu konuda güçlü görüşleri olan var mı?

GCJ desteğinin bir diğer olumlu özelliği, C/C++/Python vb. dillerden akış kütüphanesini kullanabilme olanağıdır. Böyle bir entegrasyon üzerinde birinin çalışıp çalışmadığını bilmiyorum, ancak muhtemelen buna değer; bu alanda geliştirme yapmaya ilgi duyuyorsanız, lütfen bana bildirin!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

i2p-bt, I2P’ye port edilen ve çok kullanılan ilk BitTorrent istemcisi olsa da, eco epey zaman önce snark [5] portuyla ilk hamleyi yapan kişiydi. Ne yazık ki güncel kalmadı ya da diğer anonim BitTorrent istemcileriyle uyumluluğunu korumadı, bu yüzden bir süreliğine ortadan kayboldu. Buna karşın geçen hafta i2p-bt<->sam<->streaming lib<->i2cp zincirinin bir yerindeki performans sorunlarıyla uğraşıyordum, bu yüzden mjw’nin özgün snark koduna geçip basit bir port [6] yaptım; java.net.*Socket çağrılarını I2PSocket* çağrılarıyla, InetAddresses yerine Destinations ve URLs yerine EepGet çağrılarıyla değiştirerek. Sonuç, artık I2P sürümüyle birlikte dağıtacağımız küçücük bir komut satırı BitTorrent istemcisi (derlenmiş olarak yaklaşık 60KB).

Ragnarok, blok seçim algoritmasını geliştirmek için üzerinde çalışmaya çoktan başladı ve umarız 0.6.2 sürümünden önce ona hem bir web arayüzü hem de çoklu torrent desteği kazandıracağız. Yardım etmekle ilgileniyorsanız, bizimle iletişime geçin! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

Son zamanlarda posta listesi, Michael’ın tunnel inşasına ilişkin yeni simülasyonları ve analizi sayesinde oldukça aktif. Tartışma hâlâ sürüyor; Toad, Tom ve polecat’ten gelen bazı iyi fikirlerle birlikte, 0.6.2 sürümü için elden geçireceğimiz anonimliğe ilişkin bazı tasarım konularındaki ödünleşimlere katkıda bulunmak isterseniz bir göz atın [7].

Biraz göze hoş gelen şeylerle ilgilenenler için, Michael’ın sizin için bir çözümü de var, saldırının kimliğinizi tespit etme olasılığını gösteren bir simülasyonla - kontrol ettikleri ağın yüzdesinin bir fonksiyonu olarak [8], ve tunnelinizin ne kadar aktif olduğunun bir fonksiyonu olarak [9]

(Güzel iş, Michael, teşekkürler!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     ("i2p tunnel bootstrap attack" ileti dizisini takip edin) [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Belirli bir I2P destekli uygulamayla birlikte dağıtıldığı iddia edilen olası kötü amaçlı yazılım sorunları hakkında bir süredir bazı tartışmalar var ve Complication bunu derinlemesine inceleme konusunda harika bir iş çıkardı. Veriler ortada, bu yüzden kendi görüşünüzü oluşturabilirsiniz. [10]

Bu konudaki tüm araştırmaların için teşekkürler, Complication!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Gördüğün gibi bir sürü şey oluyor, ama toplantıya zaten geç kaldığım için bunu herhalde kaydedip göndermeliyim, ha? #i2p'de görüşürüz :)

=jr
