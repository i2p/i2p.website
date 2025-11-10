---
title: "I2P Yaz Geliştirme"
date: 2016-06-01
author: "str4d"
description: "Bu yaz, I2P’nin hem geliştiriciler hem de kullanıcılar için gizlilik yazılımı ekosistemini iyileştirmeyi hedefleyen bir geliştirme programına başlayacağını duyurmaktan memnuniyet duyuyoruz."
categories: ["summer-dev"]
---

Son birkaç yılda, kullanıcıların kendi verileri üzerinde kontrol sahibi olma gerekliliği giderek daha belirgin hale geldi. Signal gibi mesajlaşma uygulamalarının ve Tahoe-LAFS gibi dosya depolama sistemlerinin yükselişiyle bu konuda önemli ilerlemeler kaydedildi. HTTPS’i tüm dünyaya ulaştırmak için Let's Encrypt’in sürdürdüğü çalışma istikrarlı bir şekilde ivme kazanıyor.

Ama gizlilik ve anonimliği uygulamalara dahil etmek hiç de basit değildir. İnsanların her gün kullandığı yazılımların çoğu gizliliği koruyacak şekilde tasarlanmamıştır ve geliştiricilerin elindeki araçlarla çalışmak genelde kolay değildir. Yakın zamanda yayımlanan OnionScan araştırması, hizmetlerini yanlış yapılandırmanın teknik kullanıcılar için bile ne kadar kolay olduğuna ve bunun niyetlerini tamamen baltalayabildiğine dair bazı içgörüler sunuyor.

## Geliştiricilerin kullanıcılarına yardımcı olmalarına yardımcı olmak

Bu yaz, I2P'nin gizlilik yazılımları ekosistemini iyileştirmeye yönelik bir geliştirme programına başlayacağını memnuniyetle duyuruyoruz.
Amacımız, hem uygulamalarında I2P'den yararlanmak isteyen geliştiricilerin hem de uygulamalarını I2P üzerinden yapılandırıp çalıştırmaya çalışan kullanıcıların işini kolaylaştırmaktır.

Bu yaz zamanımızı üç tamamlayıcı alana odaklayacağız:

### June: APIs

Haziran ayında, I2P ile etkileşim kurmak için mevcut çeşitli kütüphaneleri güncelleyeceğiz. Bu yıl, SAM API'ye datagramlar ve bağlantı noktaları için destek gibi ek özellikler kazandırma konusunda önemli ilerleme kaydettik. Bu özellikleri C++ ve Python kütüphanelerimizde kolayca erişilebilir hâle getirmeyi planlıyoruz.

Ayrıca yakında, Java ve Android geliştiricilerinin uygulamalarına I2P desteği eklemesini çok daha kolay hale getireceğiz. Takipte kalın!

### Haziran: API'ler

Temmuz ayında, I2P desteği eklemekle ilgilendiklerini ifade eden uygulamalarla çalışacağız. Şu anda gizlilik alanında geliştirilen gerçekten yenilikçi fikirler var ve bu uygulamaların topluluklarının, eşler arası anonimlik üzerine on yılı aşkın araştırma ve geliştirmeden yararlanmalarına yardımcı olmak istiyoruz. Bu uygulamaların I2P üzerinden yerel olarak çalışacak şekilde genişletilmesi, kullanılabilirlik açısından ileriye doğru iyi bir adımdır ve bu süreçte bu uygulamaların kullanıcı bilgilerine yaklaşımını ve bu bilgileri nasıl işlediklerini de iyileştirecektir.

### Temmuz: Uygulamalar

Son olarak, Ağustos ayında I2P ile birlikte paketlediğimiz uygulamalara ve daha geniş bir eklenti yelpazesine odaklanacağız. Bunlardan bazıları, onları daha kullanıcı dostu hale getirmek - ve bekleyen hataları da düzeltmek - için biraz ilgiye ihtiyaç duyuyor! Uzun süredir I2P’yi destekleyenlerin bu çalışmanın sonucundan keyif alacağını umuyoruz.

## Take part in Summer Dev!

Bu alanlarda gerçekleştirmek istediğimiz daha pek çok fikrimiz var. Mahremiyet ve anonimlik yazılımları üzerinde çalışmak, kullanımı kolay web siteleri veya arayüzler tasarlamak ya da kullanıcılar için kılavuzlar yazmakla ilgileniyorsanız: IRC veya Twitter üzerinde bizimle sohbet edin! Topluluğumuza yeni katılanları karşılamaktan her zaman memnuniyet duyarız. Katılan tüm yeni katkıda bulunanlara I2P çıkartmaları göndereceğiz!

Benzer şekilde, I2P entegrasyonu konusunda yardım isteyen bir uygulama geliştiriciyseniz, ya da sadece kavramlar veya ayrıntılar hakkında sohbet etmek istiyorsanız: iletişime geçin! Temmuz Uygulamalar ayımıza dahil olmak istiyorsanız, Twitter'da @GetI2P, @i2p veya @str4d ile iletişime geçin. Bizi ayrıca OFTC veya FreeNode üzerindeki #i2p-dev kanalında bulabilirsiniz.

İlerledikçe burada paylaşımlar yapacağız, ancak ilerlememizi Twitter’da #I2PSummer etiketiyle takip edebilir ve kendi fikirlerinizi ve çalışmalarınızı paylaşabilirsiniz. Yaz gelsin!
