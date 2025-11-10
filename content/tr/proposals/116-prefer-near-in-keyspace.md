---
title: "Anahtarlıkta Yakınlardaki Yönlendiricileri Tercih Et"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Araştırma Gerekli"
thread: "http://zzz.i2p/topics/1874"
---

## Genel Bakış

Bu, akranların organize edilerek, anahtarlıkta onlara yakın olan akranlarla bağlantı kurmayı tercih etmelerini sağlayacak bir öneridir.

## Motivasyon

Bu fikrin amacı, bir yönlendiricinin önceden başka bir yönlendiriciye bağlı olma olasılığını artırarak tünel oluşturma başarısını artırmaktır.

## Tasarım

### Gerekli Değişiklikler

Bu değişiklik:

1. Her yönlendiricinin anahtarlıkta kendilerine yakın bağlantıları tercih etmesini gerektirir.
2. Her yönlendiricinin, diğer tüm yönlendiricilerin anahtarlıkta kendilerine yakın bağlantıları tercih ettiğini bilmesi gerekir.

### Tünel Oluşturma İçin Avantajlar

Bir tünel oluşturduğunuzda::

    A -uzun-> B -kısa-> C -kısa-> D

(anahtarlıkta uzun/rastgele vs kısa adım), muhtemelen tünel oluşumunun nerede başarısız olduğunu tahmin edebilir ve o noktada farklı bir akran deneyebilirsiniz. Ek olarak, anahtar alandaki daha yoğun bölgeleri tespit etmenizi ve yönlendiricilerin bunları kullanmamasını sağlayabilirsiniz çünkü bu, birilerinin iş birliği yaptığı anlamına gelebilir.

Bir tünel oluşturduğunuzda::

    A -uzun-> B -uzun-> C -kısa-> D

ve başarısız olursa, muhtemelen C -> D arasında başarısız olduğunu çıkarım yapabilir ve başka bir D adımı seçebilirsiniz.

Ayrıca OBEP'nin IBGW'ye daha yakın olduğu tüneller oluşturabilir ve bu tünelleri, verilen IBGW'de daha yakın OBEP ile birlikte bir LeaseSet'te kullanabilirsiniz.

## Güvenlik İmplikasyonları

Anahtarlıkta kısa vs uzun adımların konumunu rastgeleleştirirseniz, bir saldırgan muhtemelen pek bir avantaj elde edemeyecektir.

Ancak en büyük dezavantaj, kullanıcı sayımını biraz daha kolay hale getirebilir.
