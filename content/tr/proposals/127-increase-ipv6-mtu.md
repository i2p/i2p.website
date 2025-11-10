---
title: "IPv6 MTU'yu Artır"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Genel Bakış

Bu öneri, azami SSU IPv6 MTU'yu 1472'den 1488'e artırmaktır.
0.9.28'de uygulanmıştır.


## Gerekçe

IPv4 MTU, 16'nın katı ve üzerine 12 eklenmelidir. IPv6 MTU, 16'nın katı olmalıdır.

Yıllar önce IPv6 desteği ilk kez eklendiğinde, max IPv6 MTU'yu 1472 olarak ayarladık, bu da 1484 olan IPv4 MTU'sundan daha azdı. Bu, işleri basit tutmak ve mevcut IPv4 MTU'sundan daha az olması için yapıldı. IPv6 desteği şimdi kararlı olduğuna göre, IPv6 MTU'yu IPv4 MTU'sundan daha yüksek ayarlayabilmeliyiz.

Tipik arayüz MTU'su 1500 olduğundan, IPv6 MTU'yu 16 artırarak 1488'e yükseltmek mantıklıdır.


## Tasarım

Maksimumu 1472'den 1488'e değiştirin.


## Teknik Spesifikasyon

SSU genel bakışındaki "Yönlendirici Adresi" ve "MTU" bölümlerinde,
maksimum IPv6 MTU'yu 1472'den 1488'e değiştirin.


## Geçiş

Yönlendiricilerin, bağlantı MTU'sunu her zamanki gibi yerel ve uzak MTU'nun minimumu olarak ayarlayacağını bekliyoruz. Bir sürüm kontrolü gerekmemelidir.

Bir sürüm kontrolünün gerekli olduğunu belirlersek, bu değişiklik için minimum sürüm seviyesi olarak 0.9.28'i ayarlayacağız.
