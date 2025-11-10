---
title: "Kimlik Doğrulamalı Adres Yardımcıları"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Açık"
thread: "http://zzz.i2p/topics/2241"
---

## Genel Bakış

Bu öneri, adres yardımcı URL'lerine bir kimlik doğrulama mekanizması eklemektedir.

## Güdü

Adres yardımcı URL'leri doğası gereği güvensizdir. Herhangi biri bir bağlantıya, hatta bir resim için bile, bir adres yardımcı parametresi ekleyebilir ve "i2paddresshelper" URL parametresine herhangi bir hedef koyabilir. Kullanıcının HTTP proxy uygulamasına bağlı olarak, bu ana bilgisayar adı/hedef eşlemesi, eğer şu anda adres kitabında yoksa, kullanıcıya onay için bir geçiş sayfası sunsa da sunmasa da kabul edilebilir.

## Tasarım

Güvenilir yönlendirme sunucuları ve adres kitabı kayıt hizmetleri, kimlik doğrulama parametreleri ekleyen yeni adres yardımcı bağlantıları sağlayacaktır. İki yeni parametre, bir base 64 imza ve bir imzalayan-dizesi olacaktır.

Bu hizmetler bir genel anahtar sertifikası oluşturup sağlayacaktır. Bu sertifika, http proxy yazılımına dahil edilmek üzere indirilebilir olacaktır. Kullanıcılar ve yazılım geliştiricileri bu sertifikayı dahil ederek bu hizmetlere güvenip güvenmeyeceklerine karar vereceklerdir.

Bir adres yardımcı bağlantısına rastlanıldığında, http proxy ek kimlik doğrulama parametrelerini kontrol edecek ve imzayı doğrulamaya çalışacaktır. Başarılı doğrulama durumunda, proxy yeni girişi kabul ederek veya kullanıcıya bir geçiş sayfası göstererek daha önce olduğu gibi devam edecektir. Doğrulama başarısız olursa, proxy adres yardımcısını reddedebilir veya kullanıcıya ek bilgi gösterebilir.

Eğer kimlik doğrulama parametreleri mevcut değilse, http proxy kabul edebilir, reddedebilir veya kullanıcıya bilgi sunabilir.

Yönlendirme hizmetleri her zamanki gibi güvenilir olacaktır ancak ek kimlik doğrulama adımı ile. Başka sitelerdeki adres yardımcı bağlantıları değiştirilmek zorunda kalacaktır.

## Güvenlik Açılımları

Bu öneri, güvenilir kayıt / yönlendirme hizmetlerinden gelen kimlik doğrulaması ekleyerek güvenliği artırmaktadır.

## Spesifikasyon

Belirlenecek.

İki yeni parametre i2paddresshelpersig ve i2paddresshelpersigner olabilir mi?

Kabul edilen imza türleri belirlenecek. Muhtemelen RSA olmayabilir çünkü base 64 imzaları çok uzun olacaktır.

İmza algoritması: Belirlenecek. Belki sadece hostname=b64dest (kayıt kimlik doğrulaması için teklif 112 ile aynı)

Olası üçüncü yeni parametre: Kayıt kimlik doğrulama dizesi (#!'den sonraki kısım) HTTP proxy tarafından ek doğrulama için kullanılabilir. Dizedeki tüm "#" işareti "&#35;" veya "&num;" olarak kaçış yapılmalı ya da başka bir belirli (belirlenecek) URL-güvenli karakter ile değiştirilmelidir.

## Geçiş

Yeni kimlik doğrulama parametrelerini desteklemeyen eski HTTP proxy'ler onları yok sayacak ve web sunucusuna iletecektir, bu da zararsız olmalıdır.

Kimlik doğrulama parametrelerini isteğe bağlı olarak destekleyen yeni HTTP proxy'ler, bunları içermeyen eski adres yardımcı bağlantıları ile sorunsuz çalışacaktır.

Kimlik doğrulama parametrelerini zorunlu kılan yeni HTTP proxy'ler, bunları içermeyen eski adres yardımcı bağlantılarına izin vermeyecektir.

Bir proxy uygulamasının politikaları bir geçiş süresi boyunca evrilebilir.

## Sorunlar

Bir site sahibi, güvenilir bir yönlendirme sunucusundan imza gerektiği için kendi sitesi için bir adres yardımcısı üretemez. Güvenilir sunucuya kayıt yaptırmalı ve kimlik doğrulanmış yardım URL'sini o sunucudan almalıdır. Bir sitenin kendi kendine kimlik doğrulamalı adres yardımcı URL'si üretebilmesinin bir yolu var mı?

Alternatif olarak, proxy bir adres yardımcısı isteği için Referer'ı kontrol edebilir. Eğer Referer mevcutsa, bir b32 içeriyorsa ve b32 yardımcının hedefiyle eşleşiyorsa, kendi kendine yönlendirme olarak kabul edilebilir. Aksi halde bir üçüncü taraf isteği olduğu varsayılabilir ve reddedilebilir.
