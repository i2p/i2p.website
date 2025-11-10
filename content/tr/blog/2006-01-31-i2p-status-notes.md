---
title: "2006-01-31 tarihli I2P Durum Notları"
date: 2006-01-31
author: "jr"
description: "Ağ güvenilirliğiyle ilgili zorluklar, yeni tunnel oluşturma kriptografisiyle birlikte yaklaşan 0.6.1.10 sürümü ve geriye dönük uyumluluğu bozan değişiklikler"
categories: ["status"]
---

Selam millet, salı yine geldi çattı,

* Index

1) Ağ durumu 2) 0.6.1.10 durumu 3) ???

* 1) Net status

Son bir haftadır, canlı ağda tunnel oluşturmanın güvenilirliğini artırmak için birkaç farklı ince ayar deniyorum, ancak henüz bir çığır açan gelişme olmadı. Yine de CVS’de bazı kayda değer değişiklikler yapıldı, fakat bunları... kararlı olarak niteleyemem. Bu yüzden genel olarak, insanların ya en güncel sürümü (0.6.1.9, CVS’de i2p_0_6_1_9 olarak etiketlenmiş) kullanmalarını ya da en yeni derlemelerde en fazla 1 atlamalı tunnel kullanmalarını öneririm. Öte yandan...

* 2) 0.6.1.10 status

Küçük ince ayarlarla uzun süre uğraşmak yerine, yeni tunnel oluşturma kriptografisine ve sürecine [1] geçiş yapmak için yerel test ağım üzerinde çalışıyorum. Bu, tunnel oluşturma başarısızlık oranının büyük bir kısmını azaltmalı; ardından gerekirse daha da ince ayar yapabiliriz.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Ne yazık ki bunun bir yan etkisi, 0.6.1.10’un geriye dönük uyumlu olmayacak olması. Uzun zamandır geriye dönük uyumsuz bir sürüm çıkarmadık, ama ilk zamanlarda bunu epey yapıyorduk, bu yüzden çok büyük bir sorun olmamalı. Özetle, yerel test ağımda gayet iyi çalıştıktan sonra, erken test için birkaç cesur kişiye paralel olarak sunacağız; ardından yayıma hazır olduğunda, yalnızca seed referanslarını (başlangıç sunucusu referansları) yeni ağın seeds’leriyle değiştirip yayına alacağız.

0.6.1.10 sürümünün yayımlanması için bir ETA’m yok, ama şu anda oldukça iyi görünüyor (çoğu tunnel uzunluğu düzgün çalışıyor, ancak henüz stres testine tabi tutmadığım birkaç dal var). Elbette, yeni gelişmeler oldukça daha fazlasını paylaşacağım.

* 3) ???

Şimdilik bahsedeceklerim aşağı yukarı bu kadar, gerçi başkalarının üzerinde çalıştığı şeyler olduğunu biliyorum ve ilerisi için de kolumda birkaç koz var, ama zamanı gelince daha fazlasını öğreneceğiz. Neyse, birkaç dakika içinde görüşürüz!

=jr
