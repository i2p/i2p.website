---
title: "Adres Defteri Abonelik Akışı Komutları"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Kapalı"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Not
Ağ dağıtımı tamamlandı.
Resmi spesifikasyonu görmek için [SPEC](/docs/specs/subscription/) bağlantısını takip edin.

## Genel Bakış

Bu öneri, adres aboneliği akışının komutlarla genişletilmesi hakkındadır. Bu sayede, isim sunucuları, ana makine adı sahiplerinden giriş güncellemelerini yayınlayabilir. 0.9.26 sürümünde uygulanmıştır.

## Motivasyon

Şu anda, hosts.txt abonelik sunucuları sadece hosts.txt formatında veri gönderiyor; bu format aşağıdaki gibidir:

    ```text
    example.i2p=b64destination
    ```

Bununla ilgili birkaç problem var:

- Ana makine adı sahipleri, ana makine adlarıyla ilişkilendirilen Hedef'i güncelleyemez (örneğin, imza anahtarını daha güçlü bir türle değiştirmek için).
- Ana makine adı sahipleri, ana makine adlarını keyfi olarak devredemez; ilgili Hedef özel anahtarlarını doğrudan yeni sahiplerine vermeleri gerekir.
- Bir alt alan adının, ilgili baz ana makine adı tarafından kontrol edildiğini doğrulamanın bir yolu yoktur; bu, şu anda yalnızca bazı isim sunucuları tarafından bireysel olarak uygulanmaktadır.

## Tasarım

Bu öneri, hosts.txt formatına bir dizi komut satırı ekler. Bu komutlarla, isim sunucuları hizmetlerini genişleterek çeşitli ek özellikler sunabilirler. Bu öneriyi uygulayan istemciler, bu özellikleri normal abonelik süreciyle dinleyebileceklerdir.

Tüm komutlar, ilgili Hedef tarafından imzalanmalıdır. Bu, değişikliklerin yalnızca ana makine adı sahibinin talebi üzerine yapılmasını sağlar.

## Güvenlik etkileri

Bu önerinin anonimliğe hiçbir etkisi yoktur.

Bir Hedef anahtarının kontrolünü kaybetme riski artmaktadır; çünkü birini ele geçiren, bu komutları kullanarak ilgili ana makine adında değişiklikler yapabilir. Ancak bu durum, bir Hedef'i ele geçiren kişinin bir ana makine adını taklit etmesi ve (kısmen) trafiğini ele geçirmesiyle de halihazırda bir sorun oluşturmamaktadır. Artan risk, aynı zamanda bir Hedef'in ihlal edildiğini düşünmeleri durumunda hostname sahiplerine Hedefi değiştirme yeteneği verilerek dengelenir; bu, mevcut sistemde mümkün değildir.

## Spesifikasyon

### Yeni satır tipleri

Bu öneri iki yeni satır tipi ekler:

1. Ekle ve Değiştir komutları:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. Kaldır komutları:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### Sıralama
Bir akış sıralı veya eksiksiz olmak zorunda değildir. Örneğin, bir değişiklik komutu, bir ekleme komutundan önce veya ekleme komutu olmadan bir satırda olabilir.

Anahtarlar herhangi bir sırada olabilir. Yinelenen anahtarlara izin verilmez. Tüm anahtarlar ve değerler büyük-küçük harfe duyarlıdır.

### Ortak anahtarlar

Tüm komutlarda zorunlu:

sig
  Hedeften imza anahtarı kullanılarak yapılan B64 imza

İkinci bir hostname ve/veya hedeften referanslar:

oldname
  İkinci hostname (yeni veya değiştirilen)
olddest
  İkinci b64 hedef (yeni veya değiştirilen)
oldsig
  nolddest'ten imza anahtarı kullanılarak yapılan ikinci b64 imza

Diğer ortak anahtarlar:

action
  Bir komut
name
  Hostname, yalnızca example.i2p=b64dest ile başlamıyorsa mevcut
dest
  B64 hedef, yalnızca example.i2p=b64dest ile başlamıyorsa mevcut
date
  Epoch'tan itibaren saniye
expires
  Epoch'tan itibaren saniye


### Komutlar

"Add" komutu hariç tüm komutlar "action=command" anahtar/değer içermelidir.

Eski istemcilerle uyumluluk için, çoğu komut example.i2p=b64dest ile başlar, aşağıda belirtildiği gibi. Değişiklikler için, bunlar her zaman yeni değerlerdir. Eski değerler anahtar/değer bölümünde bulunur.

Listelenen anahtarlar zorunludur. Tüm komutlar burada tanımlanmayan ek anahtar/değer öğeleri içerebilir.

#### Ana makine adı ekleme
example.i2p=b64dest ile başlar
  EVET, bu yeni ana makine adı ve hedeftir.
action
  DAHİL EDİLMEZ, ima edilir.
sig
  imza

Örnek:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Ana makine adını değiştirme
example.i2p=b64dest ile başlar
  EVET, bu yeni ana makine adı ve eski hedeftir.
action
  changename
oldname
  değiştirilecek eski ana makine adı
sig
  imza

Örnek:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Hedefi değiştirme
example.i2p=b64dest ile başlar
  EVET, bu eski host adı ve yeni hedeftir.
action
  changedest
olddest
  değiştirilecek eski hedef
oldsig
  olddest'i kullanan imza
sig
  imza

Örnek:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Ana makine adı takma ismi ekleme
example.i2p=b64dest ile başlar
  EVET, bu yeni (takma) ana makine adı ve eski hedeftir.
action
  addname
oldname
  eski ana makine adı
sig
  imza

Örnek:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Hedef takma ismi ekle
(Kripto yükseltme için kullanılır)

example.i2p=b64dest ile başlar
  EVET, bu eski ana makine adı ve yeni (alternatif) hedeftir.
action
  adddest
olddest
  eski hedef
oldsig
  olddest'i kullanan imza
sig
  hedef kullanılarak imza

Örnek:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Alt alan adı ekleme
subdomain.example.i2p=b64dest ile başlar
  EVET, bu yeni ana makine alt alan adı ve hedeftir.
action
  addsubdomain
oldname
  daha yüksek seviyeli ana makine adı (example.i2p)
olddest
  daha yüksek seviyeli hedef (örneğin i2p için)
oldsig
  olddest'i kullanan imza
sig
  hedef kullanılarak imza

Örnek:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Meta verileri güncelle
example.i2p=b64dest ile başlar
  EVET, bu eski ana bilgisayar adı ve hedeftir.
action
  update
sig
  imza

(güncellenen anahtarları buraya ekleyin)

Örnek:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Ana makine adını kaldır
example.i2p=b64dest ile başlar
  HAYIR, bunlar seçeneklerde belirtilmiştir
action
  remove
name
  ana makine adı
dest
  hedef
sig
  imza

Örnek:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Bu hedefle tümünü kaldır
example.i2p=b64dest ile başlar
  HAYIR, bunlar seçeneklerde belirtilmiştir
action
  removeall
name
  eski ana makine adı, sadece bilgilendirme amaçlı
dest
  eski hedef, bu hedef ile tümü kaldırılır
sig
  imza

Örnek:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```


### İmzalar

Tüm komutlar, "sig=b64signature" imza anahtar/değerini içermelidir; bu, diğer veriler için imza, hedefin imza anahtarı kullanılarak yapılır.

Eski ve yeni hedefi içeren komutlar için, ayrıca bir oldsig=b64signature ve ya oldname, olddest veya her ikisi de bulunmalıdır.

Ekle veya Değiştir komutunda, doğrulama için genel anahtar, eklenmesi veya değiştirilmesi gereken Hedef içindedir.

Bazı ekleme veya düzenleme komutlarında, bir alias eklemek veya bir hedefi veya host adını değiştirmek için ek bir hedefe referans verilebilir. Bu durumda, ikinci bir imza dahil edilmeli ve her iki imza da doğrulanmalıdır. İkinci imza "iç" imza olup, önce imzalanır ve doğrulanır (dış imzayı hariç tutarak). İstemci değişiklikleri doğrulamak ve kabul etmek için gerekli ek işlemleri yapmalıdır.

oldsig her zaman "iç" imzadır. 'oldsig' veya 'sig' anahtarları olmadan imzalayın ve doğrulayın. sig her zaman "dış" imzadır. 'sig' anahtarı olmadan 'oldsig' anahtarıyla imzalanır ve doğrulanır.

#### İmzalar için giriş
İmza oluşturmak veya doğrulamak için bir bayt akışı oluşturmak için şöyle sıralayın:

- "sig" anahtarını kaldırın
- oldsig ile doğrulama yapıyorsanız, ayrıca "oldsig" anahtarını kaldırın
- Yalnızca Ekle veya Değiştir komutları için,
  örnek.example.i2p=b64destination çıktısı
- Herhangi bir anahtar kalırsa, "#!" çıktısını alın
- Seçenekleri UTF-8 anahtarına göre sıralayın, yinelenen anahtarlar varsa başarısız olun
- Her anahtar/değer çifti için, anahtar=değer çıkışı alın, ardından (eğer son anahtar/değer değilse)
  bir '#' ile devam edin

Notlar

- Yeni satır çıkışı almayın
- Çıkış kodlaması UTF-8'dir
- Tüm hedef ve imza kodlamaları I2P alfabesi kullanılarak Base 64'dir
- Anahtarlar ve değerler büyük-küçük harf duyarlıdır
- Ana makine adları küçük harf olmalıdır

## Uyumluluk

hosts.txt formatındaki tüm yeni satırlar, önünde yorum karakterleri kullanılarak uygulanmaktadır, böylece eski I2P sürümlerinin tüm yeni komutları yorum olarak yorumlamasına olanak tanır.

I2P router'ları yeni spesifikasyona güncellendiğinde, eski yorumları yeniden yorumlamayacak ancak abonelik akışlarının sonraki indirmelerinde yeni komutları dinlemeye başlayacaktır. Bu nedenle, isim sunucularının komut girdilerini bir şekilde kalıcı hale getirmesi veya etag desteğini etkinleştirmesi önemlidir, böylece router'lar tüm geçmiş komutları çekebilir.
