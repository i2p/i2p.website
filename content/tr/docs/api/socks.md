---
title: "SOCKS Proxy"
description: "I2P'nin SOCKS tunnel'ını güvenli bir şekilde kullanma"
slug: "socks"
aliases:
  - "/tr/socks"
  - "/tr/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS ve SOCKS Proxy'leri {#overview}

SOCKS proxy 0.7.1 sürümü itibariyle çalışmaktadır. SOCKS 4/4a/5 desteklenmektedir. i2ptunnel'da bir SOCKS istemci tüneli oluşturarak SOCKS'ı etkinleştirin. Hem paylaşımlı istemciler hem de paylaşımsız istemciler desteklenmektedir. SOCKS outproxy bulunmadığından kullanımı sınırlıdır.

[SSS](/docs/overview/faq#socks)'de belirtildiği gibi:

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
Ve 2005 tarihli bir e-postadan alıntı:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Herhangi bir istemciyi güvenlik ve anonimlik açısından davranışını ve maruz kalan protokollerini denetlemeden I2P'nin üzerine basitçe bağlayabileceğimizi umut etmek saflıktır. Hemen hemen *her* uygulama ve protokol, özellikle bunun için tasarlanmadıkça anonimliği ihlal eder, ve öyle tasarlansa bile çoğu yine de ihlal eder. Gerçek budur. Son kullanıcılar, anonimlik ve güvenlik için tasarlanmış sistemlerle daha iyi hizmet alırlar. Mevcut sistemleri anonim ortamlarda çalışacak şekilde değiştirmek küçük bir başarı değildir, mevcut I2P API'lerini basitçe kullanmaktan kat kat daha fazla iş gerektirir.

SOCKS proxy standart adres defteri isimlerini destekler, ancak Base64 hedeflerini desteklemez. Base32 hash'leri 0.7 sürümünden itibaren çalışması gerekir. Yalnızca giden bağlantıları destekler, yani bir I2PTunnel İstemcisi olarak. UDP desteği taslak halinde ancak henüz çalışmıyor. Port numarasına göre outproxy seçimi taslak halinde.

## Ayrıca Bakınız {#see-also}

- Toplantı 81 (16 Mart 2004) ve Toplantı 82 (23 Mart 2004) için notlar.
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Bir Şeyi Çalıştırmayı Başarırsanız {#working}

Lütfen bize bildirin. Ve lütfen SOCKS proxy'lerinin riskleri hakkında kapsamlı uyarılar sağlayın.
