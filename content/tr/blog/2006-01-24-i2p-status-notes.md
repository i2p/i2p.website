---
title: "2006-01-24 tarihli I2P Durum Notları"
date: 2006-01-24
author: "jr"
description: "Ağ durumu güncellemesi, 0.6.2 için yeni tunnel oluşturma süreci ve güvenilirlik iyileştirmeleri"
categories: ["status"]
---

Selam millet, salı sürekli geri geliyor...

* Index

1) Ağ durumu 2) Yeni derleme süreci 3) ???

* 1) Net status

Geçtiğimiz hafta ağda pek fazla değişiklik olmadı; kullanıcıların çoğu (77%) en son sürüme geçmiş durumda. Yine de, yeni tunnel oluşturma süreciyle ilgili bazı ciddi değişiklikler yolda ve bu değişiklikler, yayınlanmamış derlemeleri test etmeye yardımcı olanlar için bazı aksaklıklara yol açacak. Bununla birlikte, genel olarak, yayınlanmış sürümleri kullananlar oldukça güvenilir bir hizmet düzeyi almaya devam etmelidir.

* 2) New build process

0.6.2 için yapılan tunnel yenilemesinin bir parçası olarak, değişen koşullara daha iyi uyum sağlamak ve yükü daha temiz bir şekilde ele almak için router içinde kullanılan prosedürü değiştiriyoruz.  Bu, yeni eş (peer) seçim stratejilerinin ve yeni tunnel oluşturma kriptografisinin entegrasyonuna bir ön adımdır ve tamamen geriye dönük uyumludur.  Ancak bu süreçte, tunnel oluşturma sürecindeki bazı tuhaflıkları temizliyoruz; bu tuhaflıkların bazıları bazı güvenilirlik sorunlarının üzerini örtmeye yardımcı olmuş olsa da, anonimlik ile güvenilirlik arasında optimal olmayan bir ödünleşime yol açmış olabilirler.  Özellikle, felaket düzeyindeki arızalarda yedek 1 atlamalı tunnels kullanırlardı - yeni süreç ise yedek tunnels kullanmak yerine ulaşılamazlığı tercih edecek; bu da insanların daha fazla güvenilirlik sorunu göreceği anlamına geliyor.  En azından, tunnel güvenilirliği sorunlarının kaynağı ele alınana kadar bunlar görünür olacak.

Her neyse, şu anda derleme süreci kabul edilebilir düzeyde güvenilirlik sağlamıyor, ancak sağladığında bunu bir sürümle sizlere yayınlayacağız.

* 3) ???

Birkaç başka kişinin de ilgili çeşitli faaliyetler üzerinde çalıştığını biliyorum, ama uygun gördüklerinde bizi bilgilendirmeyi onlara bırakıyorum. Her halükârda, birkaç dakika içinde toplantıda hepinizle görüşürüz!

=jr
