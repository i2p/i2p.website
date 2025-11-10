---
title: "I2P 2005-10-04 için Durum Notları"
date: 2005-10-04
author: "jr"
description: "0.6.1.1 sürümünün 3-400 eşle başarıya ulaşması, i2phex fork (çatallanma) uzlaştırma çabaları ve pet names (kullanıcıya özel adlar) ile zamanlanmış çekme işlemlerini içeren Syndie otomasyonundaki ilerlemeyi kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, haftalık durum notlarımızın zamanı geldi (buraya tezahürat ekleyin)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

Her zamanki yerlerde duyurulduğu üzere, 0.6.1.1 geçen gün yayımlandı ve şu ana kadar geri bildirimler olumlu oldu. Ağ, istikrarlı biçimde 3-400 bilinen peer (eş düğüm) sayısına ulaştı ve performans oldukça iyi, ancak CPU kullanımı biraz arttı. Bu muhtemelen, geçersiz IP adreslerinin yanlışlıkla kabul edilmesine izin veren ve bunun sonucunda gereğinden yüksek churn (düğüm sirkülasyonu) oluşturan uzun süredir devam eden hatalardan kaynaklanıyor. 0.6.1.1'den beri CVS build'lerinde buna ve diğer şeylere yönelik düzeltmeler yapıldı, bu yüzden muhtemelen bu haftanın ilerleyen günlerinde 0.6.1.2'yi yayımlayacağız.

* 2) i2phex

Çeşitli forumlarda i2phex ve legion'un çatallamasıyla ilgili tartışmayı bazıları fark etmiş olabilir; bu arada legion ile benim aramda ek iletişim oldu ve bu ikisini yeniden birleştirmek için çalışıyoruz. Bu konuyla ilgili daha fazla bilgi mevcut olduğunda paylaşılacaktır.

Ayrıca, redzara i2phex’i mevcut phex sürümüyle birleştirme üzerinde yoğun şekilde çalışıyor ve striker da bazı ek iyileştirmeler geliştirdi; dolayısıyla yakında heyecan verici yenilikler yolda.

* 3) syndie

Ragnarok son birkaç gündür syndie üzerinde aralıksız çalışıyor; syndie'nin takma ad veritabanını, router (yönlendirici) üzerindeki takma ad veritabanıyla entegre ediyor ve ayrıca seçili uzak arşivlerden zamanlanmış çekme işlemleriyle sindikasyonu otomatikleştiriyor. Otomasyon kısmı tamam; biraz UI (kullanıcı arayüzü) işi kalsa da oldukça iyi durumda!

* 4) ???

Şu sıralar başka pek çok şey de oluyor; bunlara yeni teknik giriş dokümanları üzerinde bazı çalışmalar, IRC geçişi ve web sitesinin yenilenmesi de dahil. Konuşmak istediğiniz bir şey varsa, birkaç dakika içinde yapılacak toplantıya uğrayıp bir selam verin!

=jr
