---
title: "Yayın Güncellemeleri"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Kapalı"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Genel Bakış

API 0.9.58'den (Mart 2023'te yayınlandı) daha eski Java I2P ve i2pd yönlendiriciler, bir yayın SYN paket yeniden oynatma saldırısına karşı savunmasızdır.
Bu bir protokol tasarım sorunu olup, bir uygulama hatası değildir.

SYN paketleri imzalanmış durumdadır, ancak Alice'ten Bob'a gönderilen ilk SYN paketinin imzası Bob'un kimliğine bağlı değildir, bu nedenle Bob bu paketi depolayıp tekrar oynatabilir ve bunu bir kurban Charlie'ye gönderebilir. Charlie paketinin Alice'ten geldiğini düşünecek ve ona yanıt verecektir. Çoğu durumda bu zararsızdır, ancak SYN paketi başlangıç verileri içerebilir (örneğin bir GET veya POST) ve Charlie bunu hemen işleyecektir.


## Tasarım

Çözüm, Alice'in Bob'un varış yeri hash'ini imzalı SYN verilerine eklemesidir.
Bob alımda bu hash'in kendi hash'iyle eşleşip eşleşmediğini doğrular.

Potansiyel saldırı kurbanı Charlie, bu veriyi kontrol eder ve hash'iyle eşleşmediği takdirde SYN'i reddeder.

SYN'deki hash'i saklamak için NACKs seçenek alanını kullanarak,
değişiklik geriye dönük uyumlu olur, çünkü NACKs'lerin SYN paketinde bulunması beklenmez ve şu anda göz ardı edilir.

Her zamanki gibi, tüm seçenekler imza ile kapsanır, bu nedenle Bob hash'i yeniden yazamaz.

Alice ve Charlie API 0.9.58 veya daha yeni sürümde ise, Bob tarafından yapılan herhangi bir tekrar oynatma girişimi reddedilir.


## Spesifikasyon

[Streaming spesifikasyonunu](/docs/specs/streaming/) güncelleyin ve aşağıdaki bölümü ekleyin:

### Yeniden Çalma Önleme

Bob'un, Alice'den aldığı ve daha sonra bir kurban Charlie'ye gönderdiği geçerli imzalı SYNCHRONIZE paketini depolayarak bir yeniden oynatma saldırısı yapmasını önlemek için, Alice aşağıdaki şekilde SYNCHRONIZE paketine Bob'un varış yeri hash'ini eklemelidir:

.. raw:: html

  {% highlight lang='dataspec' %}
NACK sayısı alanını 8 olarak ayarlayın
  NACKs alanını Bob'un 32-bayt varış yeri hash'i olarak ayarlayın

{% endhighlight %}

Bir SYNCHRONIZE alındığında, eğer NACK sayısı alanı 8 ise,
Bob NACKs alanını 32-bayt varış yeri hash'i olarak yorumlamalı
ve bu hash'in kendi varış yeri hash'iyle eşleştiğini doğrulamalıdır.
Ayrıca, genellikle olduğu gibi paket imzasını doğrulamalıdır,
çünkü bu işlem tüm paketi, NACK sayısı ve NACKs alanları dahil, kapsar.
Eğer NACK sayısı 8 ise ve NACKs alanı uyuşmazsa,
Bob paketi düşürmelidir.

Bu, 0.9.58 ve daha yüksek sürümler için zorunludur.
Bu, daha eski sürümlerle geriye dönük uyumludur,
çünkü SYNCHRONIZE paketinde NACKs beklenmez.
Varış noktaları, karşı tarafın hangi sürümü çalıştırdığını bilmez ve bilemez.

Bob'dan Alice'e gönderilen SYNCHRONIZE ACK paketi için bir değişiklik gerekmez;
bu pakete NACKs eklemeyin.


## Güvenlik Analizi

Bu sorun, 2004 yılında oluşturulduğunda yayın protokolünde mevcuttu.
I2P geliştiricileri tarafından dahili olarak keşfedildi.
Sorunun hiç kullanıldığına dair elimizde bir kanıt yok.
Sömürü başarısı şansı, uygulama katmanı protokolü ve hizmetine bağlı olarak büyük ölçüde değişiklik gösterebilir.
Eşler arası uygulamalar, muhtemelen istemci/sunucu uygulamalarından daha fazla etkilenebilir.


## Uyumluluk

Sorun yok. Bilinen tüm uygulamalar şu anda SYN paketindeki NACKs alanını yok sayar.
Ve eğer yok saymazlardı ve 8 farklı mesaj için NACKs olarak yorumlamaya çalışsalar bile, bu mesajlar SYNCHRONIZE el sıkışması sırasında beklemede olmayacak ve NACKs anlam ifade etmeyecekti.


## Geçiş

Uygulamalar herhangi bir zamanda destek ekleyebilir, herhangi bir koordinasyona ihtiyaç yoktur.
Java I2P ve i2pd yönlendiricileri, API 0.9.58'de (Mart 2023'te yayınlandı) bunu uygulamıştır.


