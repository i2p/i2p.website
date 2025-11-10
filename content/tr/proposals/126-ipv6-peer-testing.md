---
title: "IPv6 Peer Testi"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Closed"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Genel Bakış

Bu öneri, IPv6 için SSU Peer Testlerinin uygulanması içindir. 0.9.27 sürümünde uygulanmıştır.

## Motivasyon

IPv6 adresimizin güvenlik duvarı arkasında olup olmadığını güvenilir şekilde belirleyemiyoruz ve izleyemiyoruz.

Yıllar önce IPv6 desteği eklediğimizde, IPv6'nın hiçbir zaman güvenlik duvarı arkasında olmadığını varsaydık.

Daha yakın bir zamanda, 0.9.20 sürümünde (Mayıs 2015), v4/v6 erişilebilirlik durumunu dahili olarak ayırdık (bilet #1458).
Kapsamlı bilgi ve bağlantılar için o bilete bakın.

Hem v4 hem de v6 güvenlik duvarı arkasında ise, /confignet üzerinden TCP yapılandırma bölümünde zorlayarak güvenlik duvarı arkasına alabilirsiniz.

v6 için peer testi yapmıyoruz. Bu, SSU tanımında yasaklanmıştır.
v6 erişilebilirliğini düzenli olarak test edemezsek, v6 erişilebilir durumdan geçiş yapamayız.
Elde ettiğimiz şey, bir giriş bağlantısı aldığımızda erişilebilir olduğumuzu tahmin etmek,
ve bir süredir giriş bağlantısı almadığımızda erişilebilir olmadığımızı tahmin etmektir.
Sorun, eğer erişilemez olarak ilan ederseniz, v6 IP'nizi yayınlamazsınız,
ve ardından artık kimsenin netdb'sinde RI sona erene kadar daha fazla bağlantı almazsınız.

## Tasarım

Peer Testini IPv6 için uygulayın,
Peer testinin yalnızca IPv4 için izinli olduğu önceki kısıtlamaları kaldırarak.
Peer test mesajında IP uzunluğu için zaten bir alan bulunmaktadır.

## Spesifikasyon

SSU genel bakışının Yetenekler bölümünde aşağıdaki eklemeyi yapın:

0.9.26 sürümüne kadar, peer testi IPv6 adresleri için desteklenmiyordu, ve bir IPv6 adresi için mevcutsa 'B' yeteneği göz ardı edilmelidir.
0.9.27 sürümünden itibaren, peer testi IPv6 adresleri için desteklenmektedir, ve
bir IPv6 adresinde 'B' yeteneğinin varlığı veya yokluğu, gerçek desteği (veya destek eksikliğini) gösterir.

SSU genel bakış ve SSU spesifikasyonunun Peer Testi bölümlerinde aşağıdaki değişiklikleri yapın:

IPv6 Notları:
0.9.26 sürümüne kadar, yalnızca IPv4 adreslerinin testi desteklenmektedir.
Bu nedenle, tüm Alice-Bob ve Alice-Charlie iletişimi IPv4 üzerinden olmalıdır.
Bununla birlikte, Bob-Charlie iletişimi IPv4 veya IPv6 üzerinden olabilir.
PeerTest mesajında belirtilen Alice'in adresi 4 bayt olmalıdır.
0.9.27 sürümünden itibaren, IPv6 adreslerinin testi desteklenir ve Alice-Bob ile Alice-Charlie iletişimi,
Bob ve Charlie yayınladıkları IPv6 adreslerinde 'B' yeteneği ile destek gösteriyorsa IPv6 üzerinden olabilir.

Alice, Bob'a testi yapmak istediği taşıma aracı (IPv4 veya IPv6) üzerinden mevcut bir oturum kullanarak isteği gönderir.
Bob, Alice'ten IPv4 üzerinden bir istek aldığında, bir IPv4 adresi ilan eden Charlie'yi seçmelidir.
Bob, Alice'ten IPv6 üzerinden bir istek aldığında, bir IPv6 adresi ilan eden Charlie'yi seçmelidir.
Gerçek Bob-Charlie iletişimi IPv4 veya IPv6 (yani, Alice'in adres türünden bağımsız olarak) üzerinden olabilir.

## Geçiş

Yönlendiriciler aşağıdaki işlemleri gerçekleştirebilir:

1) Sürümlerini 0.9.27 veya daha yükseğe çıkarmayın

2) Yayınlanan herhangi bir IPv6 SSU adresinden 'B' yeteneğini kaldırın

3) IPv6 peer testini uygulayın
