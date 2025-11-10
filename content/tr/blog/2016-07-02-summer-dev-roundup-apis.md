---
title: "Yaz geliştirme özeti: API'ler"
date: 2016-07-02
author: "str4d"
description: "Summer Dev'in ilk ayında, Java, Android ve Python geliştiricileri için API'lerimizin kullanılabilirliğini iyileştirdik."
categories: ["summer-dev"]
---

Summer Dev tüm hızıyla sürüyor: bir süredir işleri rayına oturtmak, pürüzleri gidermek ve ortalığı toparlamakla meşguldük. Şimdi ilk özetimize geçme zamanı; kaydettiğimiz ilerlemeler konusunda sizi son durumdan haberdar edeceğiz!

## API'lerin ayı

Bu ayki hedefimiz "bütünleşmek"ti - API'lerimizin ve kütüphanelerimizin çeşitli toplulukların mevcut altyapıları içinde çalışmasını sağlamak, böylece uygulama geliştiricileri I2P ile daha verimli çalışabilir ve kullanıcıların ayrıntılar hakkında endişelenmesine gerek kalmaz.

### Java / Android

I2P istemci kütüphaneleri artık Maven Central’da mevcut! Bu, Java geliştiricilerinin uygulamalarında I2P’yi kullanmasını çok daha kolay hale getirmelidir. Kitaplıkları mevcut bir kurulumdan edinmeleri gerekmek yerine, I2P’yi basitçe bağımlılıklarına ekleyebilirler. Yeni sürümlere yükseltmek de benzer şekilde çok daha kolay olacaktır.

I2P Android istemci kitaplığı da yeni I2P kitaplıklarını kullanacak şekilde güncellendi. Bu, platformlar arası uygulamaların I2P Android ya da masaüstü I2P ile doğrudan çalışabileceği anlamına gelir.

### Java / Android

#### txi2p

Twisted eklentisi `txi2p` artık I2P içi portları destekliyor ve yerel, uzak ve port yönlendirmesi yapılmış SAM API'leri üzerinden sorunsuz çalışır. Kullanım yönergeleri için dokümantasyonuna bakın ve herhangi bir sorunu GitHub'da bildirin.

#### i2psocket

`i2psocket`’in ilk (beta) sürümü yayınlandı! Bu, standart Python `socket` kütüphanesinin birebir yerine geçen bir çözüm olup, SAM API’si üzerinden I2P desteğiyle onu genişletir. Kullanım talimatları ve herhangi bir sorunu bildirmek için GitHub sayfasına bakın.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

Temmuz ayında Tahoe-LAFS ile çalışacak olmaktan heyecan duyuyoruz! I2P, uzun süredir yamalı bir Tahoe-LAFS sürümüyle çalışan en büyük genel gridlerden birine ev sahipliği yapıyor. Uygulamalar ayı boyunca, I2P ve Tor için yerel destek eklemeye yönelik süregelen çalışmalarında onlara yardımcı olacağız; böylece I2P kullanıcıları, upstream (ana proje) tarafındaki tüm iyileştirmelerden yararlanabilecek.

I2P entegrasyonu planları hakkında konuşacağımız ve tasarım konusunda yardımcı olacağımız birkaç başka proje daha var. Gelişmeleri takipte kalın!

## Take part in Summer Dev!

Bu alanlarda gerçekleştirmek istediğimiz daha pek çok fikrimiz var. Mahremiyet ve anonimlik yazılımları üzerinde çalışmak, kullanılabilir web siteleri veya arayüzler tasarlamak ya da kullanıcılar için kılavuzlar yazmakla ilgileniyorsanız: IRC’de ya da Twitter’da bizimle sohbet edin! Topluluğumuza yeni katılanları ağırlamaktan her zaman memnuniyet duyarız.

İlerledikçe burada paylaşacağız, ancak siz de Twitter'da #I2PSummer etiketiyle ilerlememizi takip edebilir ve kendi fikirlerinizi ve çalışmalarınızı paylaşabilirsiniz. Yaz gelsin!
