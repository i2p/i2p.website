---
title: "2005-03-29 tarihli I2P Durum Notları"
date: 2005-03-29
author: "jr"
description: "Yığınlama, UDP (SSU) taşıma protokolü ve Q dağıtık depoyu içeren 0.5.0.5 sürümünü kapsayan haftalık I2P geliştirme durumu notları"
categories: ["status"]
---

Herkese selam, haftalık durum notlarının zamanı geldi

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Hepiniz 0.5.0.4 sürümüne bu kadar hızlı yükseltmede harika bir iş çıkardığınız için, yeni 0.5.0.5 sürümünü toplantıdan sonra yayımlayacağız. Geçen hafta tartıştığımız gibi, büyük değişiklik, her birine kendi başına tam 1KB boyutunda bir tunnel mesajı vermek yerine birden fazla küçük mesajı birlikte paketleyen batching code (toplu paketleme kodu) eklenmesidir. Bu tek başına devrim niteliğinde olmasa da, iletilen mesaj sayısını ve kullanılan bant genişliğini, özellikle IRC gibi hizmetlerde, önemli ölçüde azaltmalıdır.

Sürüm duyurusunda daha fazla bilgi olacak, ancak 0.5.0.5 revizyonuyla birlikte iki başka önemli konu daha gündeme geliyor.  İlk olarak, 0.5.0.4 öncesini kullanan kullanıcılar için desteği bırakıyoruz - 0.5.0.4 kullanan 100'ün hayli üzerinde kullanıcı var ve daha önceki sürümlerde ciddi sorunlar mevcut.  İkincisi, yeni derlemede önemli bir anonimlik düzeltmesi var; her ne kadar onu gerçekleştirmek biraz geliştirme çabası gerektirse de, imkânsız değil.  Değişikliğin büyük kısmı netDb (ağ veritabanı) yönetimimize ilişkin - işi sıkı tutmayıp gelişigüzel davranmak ve girdileri her yere önbelleğe atmak yerine, söz konusu veriye sahip olsak da olmasak da, yalnızca açıkça bize verilmiş öğeler için netDb isteklerine yanıt vereceğiz.

Her zamanki gibi, hata düzeltmeleri ve bazı yeni özellikler var, ancak daha fazla bilgi sürüm duyurusunda açıklanacaktır.

* 2) UDP (SSU)

Son 6-12 aydır ara ara tartıştığımız gibi, 0.6 sürümü yayımlandıktan sonra router'lar arası iletişimimiz için UDP'ye geçeceğiz. Bu yolda daha ileri gitmek için, taşıma protokolünün ilk taslağını CVS'de yayımladık @ http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Bu, belgede belirtilen hedeflerle uyumlu, oldukça basit bir protokoldür ve hem kimlik doğrulamak hem de veriyi güvence altına almak için I2P'nin yeteneklerinden yararlanırken, dışarıya mümkün olduğunca az bilgi ifşa eder. I2P çalıştırmayan biri için bağlantı el sıkışmasının ilk kısmı dahi ayırt edilemez. Protokolün davranışı, zamanlayıcıların nasıl tetikleneceği veya üç farklı yarı güvenilir durum göstergesinin nasıl kullanılacağı gibi ayrıntılar bakımından henüz spesifikasyonda tamamen tanımlanmış değildir; ancak şifreleme, paketleştirme ve NAT hole punching (NAT üzerinden iki uç arasında bağlantı kurmak için delik açma tekniği) temellerini kapsar. Bunların hiçbiri henüz uygulanmış değil, ancak yakında uygulanacak; bu nedenle geri bildirimlerinizi memnuniyetle karşılarız!

* 3) Q

Aum, dağıtık bir veri deposu olan Q(uartermaster) üzerinde harıl harıl çalışıyor ve belgelerin ilk taslağı yayında [1]. Oradaki ilginç fikirlerden biri, doğrudan bir DHT yaklaşımından memcached [2] tarzı bir sisteme doğru bir yönelim gibi görünüyor; her kullanıcının tüm aramaları tamamen *yerel olarak* yapması ve asıl veriyi Q sunucusundan "doğrudan" (gerçi I2P üzerinden) istemesiyle. Her neyse, hoş şeyler; belki Aum uyanıksa [3] ondan bir güncelleme koparabiliriz?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] şu saat dilimlerine lanet olsun!

* 4) ???

Pek çok şey daha oluyor ve toplantıya sadece birkaç dakikadan fazla zaman kalmış olsaydı anlatmaya devam edebilirdim, ama hayat bu.  Uğrayın

# i2p'de birazdan sohbet için.

=jr
