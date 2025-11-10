---
title: "GarliCat için İsim Çevirisi"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Kapalı"
thread: "http://zzz.i2p/topics/453"
---

## Genel Bakış

Bu öneri, I2P için DNS ters arama desteği eklemekle ilgilidir.

## Mevcut Çeviri Mekanizması

GarliCat (GC), diğer GC düğümlerine bağlantı kurmak için isim çevirisi gerçekleştirir. Bu isim çevirisi, bir adresin ikili temsilinin Base32 kodlu biçimine yeniden kodlamasından ibarettir. Dolayısıyla, çeviri ileri geri çalışır.

Bu adresler 80 bit uzunluğunda seçilir. Bunun nedeni, Tor'un gizli hizmetlerini adreslemek için 80 bit uzunluğunda değerler kullanmasıdır. Bu nedenle, OnionCat (Tor için GC), Tor ile ilave bir müdahaleye gerek kalmadan çalışır.

Ne yazık ki, (bu adresleme planına göre), I2P hizmetlerini adreslemek için 256 bit uzunluğunda değerler kullanır. Zaten belirtildiği gibi, GC ikili ve Base32 kodlu biçimler arasında dönüştürme yapar. GC bir katman 3 VPN olduğundan, ikili temsilinde adresler, toplam uzunluğu 128 bit olan IPv6 adresleri olarak tanımlanmıştır. Görünen o ki, 256 bit uzunluğundaki I2P adresleri buna sığmamaktadır.

Bu nedenle, ikinci bir isim çevirme adımı gerekli hale gelir:
IPv6 adresi (ikili) -1a-> Base32 adresi (80 bit) -2a-> I2P adresi (256 bit)
-1a- ... GC çevirisi
-2a- ... I2P hosts.txt araması

Mevcut çözüm, I2P yönlendiricisinin işi yapmasını sağlamaktır. Bu, I2P yönlendiricisinin hosts.txt veya privatehosts.txt dosyasına 80 bit Base32 adresi ve hedefini (I2P adresi) bir isim/değer çifti olarak eklemekle gerçekleştirilir.

Bu temel olarak çalışır ancak kendi içinde bir gelişme aşamasında olan ve yeterince olgunlaşmamış bir isim hizmetine (bana göre) bağlıdır (özellikle isim dağıtımı açısından).

## Ölçeklenebilir Bir Çözüm

I2P (ve belki de Tor) ile ilgili adresleme aşamalarını değiştirmeyi öneriyorum, böylece GC, IPv6 adresleri üzerine düzenli DNS protokolünü kullanarak ters aramalar yapar. Ters bölge, 256 bit I2P adresini Base32 kodlu biçiminde doğrudan içermelidir. Bu, arama mekanizmasını tek adımlı bir hale getirir ve daha fazla avantaj ekler.
IPv6 adresi (ikili) -1b-> I2P adresi (256 bit)
-1b- ... DNS ters araması

İnternet üzerindeki DNS aramaları anonimliğe ilişkin bilgi sızıntıları olarak bilinir. Dolayısıyla, bu aramalar I2P içerisinde gerçekleştirilmelidir. Bu, I2P içerisinde birden çok DNS hizmetinin bulunması gerektiği anlamına gelir. DNS sorguları genellikle UDP protokolü kullanılarak yapıldığından, I2P bu paketleri doğal olarak taşıyamadığından, GC'nin veri taşımacılığı için gereken bir gerekliliktir.

DNS ile ilgili diğer avantajlar şunlardır:
1) İyi bilinen bir standart protokoldür; dolayısıyla sürekli olarak geliştirilir ve birçok araç (istemciler, sunucular, kütüphaneler,...) mevcuttur.
2) Dağıtık bir sistemdir. Varsayılan olarak isim alanının birden fazla sunucuda paralel olarak barındırılmasını destekler.
3) Kriptografiyi (DNSSEC) destekler, bu da kaynak kayıtlarının kimlik doğrulamasını sağlar. Bu doğrudan bir hedefin anahtarlarıyla bağlanabilir.

## Gelecek Fırsatlar

Bu isim hizmetinin ileri aramalar yapmak için de kullanılma olasılığı olabilir. Bu, host adlarının I2P adreslerine ve/veya IPv6 adreslerine çevrilmesidir. Ancak bu tür bir arama, normalde düzenli İnternet isim sunucularını kullanan yerel olarak kurulu çözümleyici kütüphanesi tarafından yapıldığından (örneğin, Unix-benzeri sistemlerde /etc/resolv.conf olarak belirtildiği gibi) ek araştırma gerektirir. Bu, yukarıda açıkladığım GC'nin ters aramalarından farklıdır. Daha fazla bir fırsat, bir GC giden tüneli oluşturulduğunda I2P adresinin (hedefin) otomatik olarak kaydedilmesi olabilir. Bu, kullanılabilirliği büyük ölçüde artıracaktır.
