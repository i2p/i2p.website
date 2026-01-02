---
title: "I2P Mime Türleri"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Genel Bakış

Yaygın I2P dosya formatları için mime türlerini tanımlayın.
Debian paketlerine tanımları ekleyin.
.su3 türü ve muhtemelen diğerleri için bir işleyici sağlayın.


## Motivasyon

Bir tarayıcı ile indirirken yeniden tohumlama ve eklenti yüklemeyi kolaylaştırmak için,
.su3 dosyalarına bir mime türü ve işleyiciye ihtiyacımız var.

Bunu yaparken, mime tanım dosyasını yazmayı öğrenmenin ardından,
freedesktop.org standardını izleyerek diğer yaygın
I2P dosya türleri için tanımları ekleyebiliriz.
Genellikle indirilmeyen dosyalar için daha az kullanışlı olsa da,
adres defteri blok dosyası veritabanı (hostsdb.blockfile) gibi,
bu tanımlar, bir grafiksel dizin görüntüleyici kullanırken dosyaların daha iyi tanımlanmasını ve simgelenmesini sağlayacaktır. Örneğin, Ubuntu'da "nautilus" gibi.

Mime türlerini standart hale getirerek, her yönlendirici implementasyonu
uygun olarak işleyiciler yazabilir ve mime tanım dosyası tüm implementasyonlar tarafından paylaşılabilir.


## Tasarım

freedesktop.org standardını izleyen bir XML kaynak dosyası yazın ve
bunu Debian paketlerine dahil edin. Dosya "debian/(paket).sharedmimeinfo" olacaktır.

Tüm I2P mime türleri "application/x-i2p-" ile başlayacak,
jrobin rrd hariç.

Bu mime türlerinin işleyicileri uygulamaya özeldir ve burada
belirtilmeyecektir.

Ayrıca Jetty ile tanımları dahil edeceğiz ve bunları
yeniden tohum yazılımı veya talimatları ile birlikte ekleyeceğiz.


## Teknik Özellikler

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(genel)	application/x-i2p-su3

.su3	(yönlendirici güncelleme)	application/x-i2p-su3-update

.su3	(eklenti)	application/x-i2p-su3-plugin

.su3	(yeniden tohum)	application/x-i2p-su3-reseed

.su3	(haberler)		application/x-i2p-su3-news

.su3	(engelleme listesi)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Notlar

Yukarıda listelenen tüm dosya formatları non-Java yönlendirici implementasyonları tarafından kullanılmaz;
bazıları bile iyi tanımlanmış olmayabilir. Ancak, burada belgelendirme
gelecekte çapraz uygulanabilirlik tutarlılığını sağlayabilir.

".config", ".dat" ve ".info" gibi bazı dosya ekleri diğer
mime türleriyle çakışabilir. Bunlar, tam dosya adı, bir dosya adı deseni veya sihirli numaralar gibi ek verilerle ayırt edilebilir.
Örnekler için zzz.i2p konusundaki taslak i2p.sharedmimeinfo dosyasına bakın.

Önemli olanlar .su3 türleridir ve bu türler hem
benzersiz bir eklentiye hem de sağlam sihirli numara tanımlarına sahiptir.


## Göç

Uygulanabilir değil.
