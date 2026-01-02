---
title: "Opsiyonel İmza Türleri için Floodfill Desteği"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Genel Bakış

Floodfill'lerin opsiyonel imza türleri için desteklerini ilan edebilmesi için bir yol ekleyin.
Bu, uzun vadede yeni imza türlerini desteklemek için bir yol sağlayacak,
tüm uygulamalar bunları desteklemese bile.


## Güdü

GOST önerisi 134, daha önce kullanılmamış deneysel imza türü aralığıyla ilgili birkaç sorunu ortaya çıkardı.

İlk olarak, deneysel aralıktaki imza türleri rezerve edilemediğinden,
birden fazla imza türü için aynı anda kullanılabilirler.

İkinci olarak, deneysel imza türüne sahip bir router bilgisi veya kiralama seti bir floodfill'de depolanamıyorsa,
yeni imza türü tam anlamıyla test edilmesi veya deneme bazında kullanılması zorlaşır.

Üçüncü olarak, öneri 136 uygulanırsa, bu güvenli değildir çünkü herhangi biri bir girişi üzerine yazabilir.

Dördüncü olarak, yeni bir imza türü uygulamak büyük bir geliştirme çabası olabilir.
Tüm yönlendirici uygulamalarının geliştiricilerini belirli bir
dağıtım zamanında yeni bir imza türü desteği eklemeleri konusunda ikna etmek zor olabilir.
Geliştiricilerin zamanları ve motivasyonları farklılık gösterebilir.

Beşinci olarak, GOST standart aralıkta bir imza türü kullanıyorsa,
belirli bir floodfill'in GOST'u destekleyip desteklemediğini bilmenin bir yolu yoktur.


## Tasarım

Tüm floodfill'ler imza türlerini DSA (0), ECDSA (1-3) ve EdDSA (7) desteklemek zorundadır.

Standart (deneysel olmayan) aralıktaki diğer herhangi bir imza türü için,
bir floodfill, yönlendirici bilgi özelliklerinde destek ilan edebilir.


## Özellikler


Opsiyonel bir imza türünü destekleyen bir yönlendirici,
yayınlanmış yönlendirici bilgisine virgülle ayrılmış imza türü numaraları ile "sigTypes" özelliği eklemelidir.
İmza türleri sayısal sıralamaya göre olacaktır.
Zorunlu imza türleri (0-4,7) dahil edilmemelidir.

Örneğin: sigTypes=9,10

Opsiyonel imza türlerini destekleyen yönlendiriciler,
sadece bu imza türü için destek ilan eden floodfill'lere depolama, arama veya flood işlemlerini gerçekleştirmelidir.


## Geçiş

Uygulanabilir değil.
Sadece opsiyonel bir imza türünü destekleyen yönlendiricilerin uygulaması gerekir.


## Sorunlar

İmza türünü destekleyen çok sayıda floodfill yoksa, bulmak zor olabilirler.

PSA için tüm floodfill'ler için ECDSA 384 ve 521 (imza türleri 2 ve 3) gerektirmek gerekli olmayabilir.
Bu türler yaygın olarak kullanılmamaktadır.

Sıfır olmayan şifreleme türleri ile benzer sorunlar ele alınması gerekecektir,
bu henüz resmi olarak önerilmemiştir.


## Notlar

Deneysel aralıkta olmayan bilinmeyen imza türleri için NetDB saklamaları
floodfill'ler tarafından reddedilmeye devam edecektir, çünkü imza doğrulanamaz.


