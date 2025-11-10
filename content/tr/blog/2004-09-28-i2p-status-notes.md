---
title: "2004-09-28 için I2P Durum Notları"
date: 2004-09-28
author: "jr"
description: "Yeni taşıma protokolünün uygulanması, IP'nin otomatik algılanması ve 0.4.1 sürümünün ilerleme durumunu kapsayan haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, haftalık güncelleme zamanı

## Dizin:

1. New transport
2. 0.4.1 status
3. ???

## 1) Yeni taşıma protokolü

0.4.1 sürümünün çıkması beklenenden uzun sürdü, ancak planlanan her şeyle birlikte yeni taşıma protokolü ve uygulaması yerinde: IP tespiti, düşük maliyetli bağlantı kurulumu ve bağlantılar başarısız olduğunda hata ayıklamaya yardımcı olacak daha kolay bir arayüz. Bu, eski taşıma protokolünü tamamen kaldırıp yenisini uygulayarak yapıldı; yine de aynı jargon terimleri duruyor (2048bit DH + STS, AES256/CBC/PKCS#5). Protokolü incelemek isterseniz, belgelerde mevcut. Yeni uygulama ayrıca çok daha temiz, çünkü eski sürüm geçen yıl boyunca birikmiş güncellemelerden ibaretti.

Her neyse, yeni IP algılama kodunda bahsetmeye değer bazı noktalar var. En önemlisi, tamamen isteğe bağlıdır - yapılandırma sayfasında (veya doğrudan router.config içinde) bir IP adresi belirtirseniz, ne olursa olsun her zaman o adresi kullanır. Ancak bunu boş bırakırsanız, router, bağlantı kurduğu ilk eşin ona IP adresinin ne olduğunu söylemesine izin verir ve ardından (kendi RouterInfo’suna ekleyip ağ veritabanına (netDb) yerleştirdikten sonra) o adreste dinlemeye başlar. Aslında, bu tam olarak doğru değil - bir IP adresini açıkça belirlemediyseniz, eşin bağlantısı olmadığında hangi IP adresinden erişilebileceğini söyleyen herhangi birine güvenecektir. Dolayısıyla, internet bağlantınız yeniden başlarsa ve size yeni bir DHCP adresi verirse, router ulaşabildiği ilk eşe güvenecektir.

Evet, bu dyndns’e artık gerek kalmadığı anlamına geliyor. Elbette kullanmaya devam edebilirsiniz, ancak gerekli değil.

Ancak, bu, istediğiniz her şeyi sağlamaz - bir NAT veya güvenlik duvarınız varsa, harici IP adresinizi bilmek işin sadece yarısıdır - yine de gelen bağlantı için port yönlendirmesi yapmanız gerekir. Ama, bu bir başlangıç.

(yeri gelmişken, kendi özel I2P ağlarını veya simülatörlerini çalıştıran kişiler için, ayarlanması gereken yeni bir bayrak çifti vardır i2np.tcp.allowLocal ve i2np.tcp.tagFile)

## 2) 0.4.1 durumu

0.4.1 için yol haritasındaki maddelerin ötesinde, hem hata düzeltmeleri hem de ağ izleme güncellemeleri olmak üzere birkaç şey daha eklemek istiyorum. Şu anda bazı aşırı memory churn (sık tahsis/serbest bırakma) sorunlarının izini sürüyorum ve ağ üzerindeki zaman zaman ortaya çıkan güvenilirlik sorunlarıyla ilgili bazı hipotezleri incelemek istiyorum, ancak sürümü yakında, muhtemelen perşembe günü yayınlamaya hazır olacağız. Ne yazık ki geriye dönük uyumlu olmayacak, bu yüzden biraz sancılı olabilir, fakat yeni yükseltme süreci ve daha toleranslı taşıma katmanı gerçekleştirmesiyle önceki geriye dönük uyumsuz güncellemeler kadar kötü olmamalı.

## 3) ???

Evet, son iki haftadır kısa güncellemelerimiz oldu, ama bunun nedeni, çeşitli üst düzey tasarımlar yerine uygulamaya odaklanarak işin mutfağında olmamız. Size profiling verilerinden ya da yeni transport (taşıma protokolü) için 10,000 bağlantı etiketi önbelleğinden bahsedebilirim, ama bunlar o kadar ilgi çekici değil. Sizin de gündeme getirmek istediğiniz bazı ek konular olabilir; o yüzden bu akşamki toplantıya uğrayın ve aklınızdakileri dökün.

=jr
