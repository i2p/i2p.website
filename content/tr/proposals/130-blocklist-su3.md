---
title: "SU3 Formatında Engelleme Listesi"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Open"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Genel Bakış

Bu teklif, engelleme listesi güncellemelerinin ayrı bir su3 dosyasında dağıtılması içindir.


## Motivasyon

Bu olmadan, engelleme listesi yalnızca sürümde güncellenir.
Bu format, farklı yönlendirici uygulamalarında kullanılabilir.


## Tasarım

su3 dosyası içinde sarılacak formatı tanımlayın.
IP veya yönlendirici hash'ine göre engellemeye izin verin.
Yönlendiriciler bir URL'ye abone olabilir veya başka yollarla elde edilen bir dosyayı içe aktarabilir.
su3 dosyası, içe aktarma sırasında doğrulanması gereken bir imza içerir.


## Şartname

Yönlendirici güncelleme şartname sayfasına eklenecek.

Yeni içerik türü BLOCKLIST (5) tanımlayın.
Yeni dosya türü TXT_GZ (4) (.txt.gz formatı) tanımlayın.
Girdiler, ya bir IPv4 veya IPv6 adresi ya da 44 karakterlik base64 kodlu bir yönlendirici hash'i olacak şekilde, satır başına bir tanedir.
Örn. x.y.0.0/16 gibi bir ağ maskesi ile engellemeyi desteklemek isteğe bağlıdır.
Bir girişi engellemek için, önüne '!' koyun.
Yorumlar '#' ile başlar.


## Geçiş

n/a


