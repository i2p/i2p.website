---
title: "I2P, Maven Central'da"
date: 2016-06-13
author: "str4d"
description: "I2P istemci kütüphaneleri artık Maven Central'da mevcut!"
categories: ["summer-dev"]
---

Summer Dev'in API'ler ayının neredeyse yarısındayız ve birçok alanda büyük ilerleme kaydediyoruz. Bunlardan ilkinin tamamlandığını duyurmaktan mutluyum: I2P istemci kitaplıkları artık Maven Central'da mevcut!

Bu, Java geliştiricilerinin uygulamalarında I2P'yi kullanmasını çok daha kolay hale getirmelidir. Kütüphaneleri mevcut bir kurulumdan edinmeleri gerekmeden, I2P'yi doğrudan bağımlılıklarına ekleyebilirler. Yeni sürümlere yükseltmek de benzer şekilde çok daha kolay olacaktır.

## Bunlar nasıl kullanılır

Hakkında bilgi sahibi olmanız gereken iki kitaplık var:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Bunlardan birini ya da her ikisini projenizin bağımlılıklarına ekleyin ve hazırsınız!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Diğer derleme sistemleri için, çekirdek ve akış kitaplıklarına ait Maven Central sayfalarına bakın.

Android geliştiricileri, aynı kitaplıkların yanı sıra Android’e özgü yardımcıları içeren I2P Android istemci kitaplığını kullanmalıdır. Yakında yeni I2P kitaplıklarına bağımlı olacak şekilde güncelleyeceğim; böylece çapraz platform uygulamalar I2P Android ya da masaüstü I2P ile yerel (native) olarak çalışabilecek.

## Get hacking!

Bu kütüphanelerle başlamanıza yardımcı olması için uygulama geliştirme kılavuzumuza göz atın. Ayrıca bu kütüphaneler hakkında IRC'deki #i2p-dev kanalında bizimle sohbet edebilirsiniz. Ve eğer kullanmaya başlarsanız, Twitter'da #I2PSummer etiketiyle ne üzerinde çalıştığınızı bize bildirin!
