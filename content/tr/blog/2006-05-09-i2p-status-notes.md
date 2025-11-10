---
title: "2006-05-09 tarihli I2P Durum Notları"
date: 2006-05-09
author: "jr"
description: "Ağ kararlılığı iyileştirmeleri, yeni geliştirme sunucusu 'baz' ve GCJ Windows uyumluluk sorunları içeren 0.6.1.18 sürümü"
categories: ["status"]
---

Selam millet, salı yine geldi çattı

* Index

1) Ağ durumu ve 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Bir hafta daha süren test ve ince ayarların ardından, bugün öğleden sonra, üzerinde iyileştirmeler yapabileceğimiz daha kararlı bir ortama geçmemizi sağlaması gereken yeni bir sürüm yayınladık. Ancak bu sürüm yaygın olarak dağıtılana kadar pek bir etkisini görmeyebiliriz; dolayısıyla nasıl gideceğini görmek için birkaç gün beklememiz gerekebilir, ama ölçümler elbette devam edecek.

zzz'nin geçen gün dile getirdiği en son derlemeler ve sürümlere ilişkin bir husus, paralel tunnels sayısını azaltırken yedek tunnels sayısını artırmanın artık kayda değer bir etki yaratabildiğiydi. Yeterli sayıda canlı tunnels olmadan yeni leases (kiralama kayıtları) oluşturmayız; bu sayede bir canlı tunnel arızası durumunda yedek tunnels hızla devreye alınabilir ve bir istemcinin aktif lease olmadan kalma sıklığı azalır. Bununla birlikte bu yalnızca belirtiye yönelik bir ince ayardır ve en son sürüm kök nedeni ele almaya yardımcı olmalıdır.

* 2) baz

"baz", bar'ın bağışladığı yeni makine nihayet geldi; amd64 turion bir dizüstü bilgisayar (önyükleme diskinde winxp var ve harici sürücüler üzerinden kullanılmak üzere birkaç başka işletim sistemi daha mevcut). Son birkaç gündür ben de üzerinde çalışıyorum; üzerinde birkaç dağıtım fikrini denemeye çalışıyorum. Ancak karşılaştığım sorunlardan biri gcj'yi windows'ta çalışır hale getirmek. Daha doğrusu, modern bir gnu/classpath ile gcj. Ancak genel kanaat pek olumlu değil — mingw üzerinde yerel olarak derlenebiliyor ya da linux'tan çapraz derlenebiliyor, ama bir istisna bir dll sınırını geçtiğinde segfault (segmentation fault) gibi sorunlar yaşanıyor. Örneğin, java.io.File (libgcj.dll içinde bulunuyor) bir istisna fırlatırsa ve bu, net.i2p.* içindeki bir şey tarafından yakalanırsa (libi2p.dll veya i2p.exe içinde bulunuyor), *puf*, uygulama uçup gidiyor.

Evet, durum pek iç açıcı görünmüyor. Biri win32 geliştirmesine dahil olup yardımcı olabilirse gcj ekibi çok ilgilenir, ancak sağlam bir desteğin yakın zamanda gelmesi pek olası görünmüyor. Öyleyse, windows üzerinde sun jvm kullanmaya devam etmeyi planlamamız gerekecek gibi görünüyor; bu sırada *nix üzerinde gcj/kaffe/sun/ibm/etc destekleyerek. Yine de sanırım bu o kadar da kötü değil, çünkü JVM’leri paketleyip dağıtma konusunda sorun yaşayanlar *nix kullanıcıları.

* 3) ???

Tamam, toplantıya zaten geç kaldım, o yüzden bunu toparlayıp sanırım sekme değiştirip IRC penceresine geçsem iyi olacak... birazdan görüşürüz ;)

=jr
