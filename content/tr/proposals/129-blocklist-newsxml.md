---
title: "Haber Akışında Engelleme Listesi"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Genel Bakış

Bu öneri, imzalı su3 formatında dağıtılan haber dosyasında engelleme listesi güncellemelerini dağıtmak içindir.
0.9.28'de uygulanmıştır.

## Motivasyon

Bu olmadan, engelleme listesi yalnızca sürümde güncellenir.
Mevcut haber aboneliği kullanılır.
Bu format çeşitli yönlendirici uygulamalarında kullanılabilir, ancak şu anda yalnızca Java yönlendiricisi haber aboneliğini kullanıyor.

## Tasarım

Haberler.xml dosyasına yeni bir bölüm ekleyin.
IP veya yönlendirici hash'i ile engellemeye izin verin.
Bölümün kendi zaman damgası olacak.
Daha önce engellenmiş girişlerin engelini kaldırmaya izin verin.

Belirtilecek bölümün imzasını ekleyin.
İmza, zaman damgasını da kapsayacaktır.
İmza ithal edilirken doğrulanmalıdır.
İsmi belirtilmiş imzalayan, su3 imzalayanından farklı olabilir.
Yönlendiriciler engelleme listesi için farklı bir güven listesi kullanabilir.

## Spesifikasyon

Şu anda yönlendirici güncelleme spesifikasyon sayfasında.

Girdiler ya gerçek bir IPv4 veya IPv6 adresi,
ya da 44 karakterlik base64 kodlu bir yönlendirici hash'idir.
IPv6 adresleri kısaltılmış formatta (içeren "::") olabilir.
Örn. x.y.0.0/16 gibi ağ maskesiyle engelleme desteği isteğe bağlıdır.
Ana bilgisayar adları için destek isteğe bağlıdır.

## Geçiş

Bunu desteklemeyen yönlendiriciler yeni XML bölümünü görmezden gelecektir.

## Ayrıca Bakınız

Öneri 130
