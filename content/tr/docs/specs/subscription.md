---
title: "Adres Defteri Abonelik Beslemesi Komutları"
description: "Hostname sahiplerinden gelen giriş güncellemelerini name server'ların yayınlamasını sağlamak için adres abonelik feed'ini komutlarla genişletmeye yönelik spesifikasyon."
slug: "subscription"
aliases:
  - "/tr/docs/specs/subscription-spec"
  - "/tr/docs/specs/subscription-spec/"
category: "Formatlar"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Genel Bakış

Bu spesifikasyon, hostname sahiplerinden gelen giriş güncellemelerini name server'ların yayınlamasını sağlamak için adres abonelik beslemesini komutlarla genişletir. 0.9.26 sürümünde uygulandı, orijinal olarak 112 numaralı öneri ile önerildi.

## Motivasyon

Daha önce, hosts.txt abonelik sunucuları verileri yalnızca hosts.txt formatında gönderiyordu, bu format şu şekildedir:

```
example.i2p=b64destination
```
Bununla ilgili birkaç sorun var:

- Hostname sahipleri, hostname'leri ile ilişkilendirilmiş Destination'ı güncelleyemez (örneğin imzalama anahtarını daha güçlü bir türe yükseltmek için).
- Hostname sahipleri hostname'lerini keyfi olarak bırakamaz; karşılık gelen Destination özel anahtarlarını doğrudan yeni sahibine vermelidir.
- Bir alt alan adının karşılık gelen temel hostname tarafından kontrol edildiğini doğrulamanın bir yolu yoktur; bu şu anda yalnızca bazı ad sunucuları tarafından bireysel olarak uygulanmaktadır.

## Tasarım

Bu özellik hosts.txt formatına bir dizi komut satırı ekler. Bu komutlar ile name server'lar hizmetlerini genişleterek bir dizi ek özellik sağlayabilir. Bu özelliği uygulayan istemciler, normal abonelik süreci aracılığıyla bu özellikleri dinleyebileceklerdir.

Tüm komut satırları ilgili Destination tarafından imzalanmalıdır. Bu, değişikliklerin yalnızca hostname sahibinin talebi üzerine yapılmasını sağlar.

## Güvenlik Etkileri

Bu özellik anonimliği etkilemez.

Destination anahtarının kontrolünün kaybedilmesiyle ilişkili risk artışı vardır, çünkü bu anahtarı elde eden biri bu komutları kullanarak ilişkili herhangi bir hostname'de değişiklik yapabilir. Ancak bu, mevcut durumdan daha fazla bir sorun değildir; çünkü mevcut sistemde Destination'ı elde eden biri bir hostname'i taklit edebilir ve trafiğini (kısmen) ele geçirebilir. Artan risk, hostname sahiplerine Destination'ın tehlikeye girdiğini düşündükleri durumda hostname ile ilişkili Destination'ı değiştirme yeteneği vererek dengelenir; bu mevcut sistemde imkansızdır.

## Spesifikasyon

### Yeni Satır Türleri

İki yeni satır türü bulunmaktadır:

1. Ekleme ve Değiştirme komutları:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Komutları kaldır:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Sıralama

Bir beslem mutlaka sıralı veya tam olmak zorunda değildir. Örneğin, bir değiştirme komutu bir ekleme komutundan önce gelen bir satırda olabilir veya ekleme komutu olmadan bulunabilir.

Anahtarlar herhangi bir sırada olabilir. Yinelenen anahtarlara izin verilmez. Tüm anahtarlar ve değerler büyük/küçük harf duyarlıdır.

### Ortak Anahtarlar

Tüm komutlarda gerekli:

**sig** : B64 imza, hedeften gelen imzalama anahtarı kullanılarak

İkinci bir hostname ve/veya hedef referansları:

**oldname** : İkinci bir hostname (yeni veya değiştirilmiş)

**olddest** : İkinci bir b64 hedefi (yeni veya değiştirilmiş)

**oldsig** : olddest'ten gelen imzalama anahtarını kullanan ikinci bir b64 imzası

Diğer yaygın anahtarlar:

**action** : Bir komut

**name** : Hostname, yalnızca önünde `example.i2p=b64dest` bulunmuyorsa mevcut

**dest** : B64 hedef adresi, yalnızca `example.i2p=b64dest` ile başlamıyorsa mevcut

**date** : Epoch'tan bu yana saniye cinsinden

**expires** : Epoch'tan bu yana geçen saniye cinsinden

### Komutlar

"Add" komutu dışındaki tüm komutlar bir `action=command` anahtar/değer çifti içermelidir.

Eski istemcilerle uyumluluk için, çoğu komut aşağıda belirtildiği gibi `example.i2p=b64dest` ile başlar. Değişiklikler için, bunlar her zaman yeni değerlerdir. Eski değerler anahtar/değer bölümüne dahil edilir.

Listelenen anahtarlar gereklidir. Tüm komutlar burada tanımlanmayan ek anahtar/değer öğeleri içerebilir.

#### Hostname Ekle

**example.i2p=b64dest ile başlar** : EVET, bu yeni host adı ve hedefidir.

**action** : DAHİL DEĞİL, zımni olarak belirtilmiştir.

**sig** : imza

Örnek:

```
example.i2p=b64dest#!sig=b64sig
```
#### Hostname'i Değiştir

**example.i2p=b64dest tarafından öncellenir** : EVET, bu yeni host adı ve eski hedef.

**action** : changename

**oldname** : değiştirilecek eski hostname

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Hedefi Değiştir

**example.i2p=b64dest tarafından öncelenir** : EVET, bu eski host adı ve yeni hedef.

**action** : changedest

**olddest** : değiştirilecek eski dest

**oldsig** : olddest kullanarak imza

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Hostname Takma Adı Ekle

**example.i2p=b64dest ile önceden tanımlanmış** : EVET, bu yeni (takma ad) host adı ve eski hedef.

**action** : addname

**oldname** : eski hostname

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Hedef Takma Adı Ekle

(Kripto yükseltmesi için kullanılır)

**example.i2p=b64dest ile öncelenir** : EVET, bu eski host adı ve yeni (alternatif) hedef.

**action** : adddest

**olddest** : eski hedef

**oldsig** : olddest kullanılarak yapılan imza

**sig** : dest kullanarak imza

Örnek:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Alt Alan Adı Ekle

**subdomain.example.i2p=b64dest ile öncelenir** : EVET, bu yeni host alt alan adı ve hedefidir.

**action** : addsubdomain

**oldname** : üst düzey ana bilgisayar adı (example.i2p)

**olddest** : üst düzey hedef (örneğin example.i2p)

**oldsig** : olddest kullanarak imza

**sig** : dest kullanarak imza

Örnek:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Metadata Güncelleme

**example.i2p=b64dest ile öncellenir** : EVET, bu eski host adı ve destination'dır.

**action** : update

**sig** : imza

(güncellenmiş anahtarları buraya ekleyin)

Örnek:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Hostname'i Kaldır

**example.i2p=b64dest ile öncelenir** : HAYIR, bunlar seçeneklerde belirtilir

**action** : remove

**name** : ana bilgisayar adı

**dest** : hedef

**sig** : imza

Örnek:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Bu Hedefle Tümünü Kaldır

**example.i2p=b64dest ile önceden belirtilir** : HAYIR, bunlar seçeneklerde belirtilir

**action** : removeall

**name** : eski hostname, yalnızca bilgi amaçlı

**dest** : eski dest, bu dest ile olan tüm kayıtlar kaldırılır

**sig** : imza

Örnek:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### İmzalar

Tüm komutlar, diğer veriler için hedef imzalama anahtarını kullanan `sig=b64signature` imza anahtar/değer çiftini içermelidir.

Eski ve yeni hedef içeren komutlar için ayrıca bir `oldsig=b64signature` ve oldname, olddest veya her ikisi bulunmalıdır.

Bir Add veya Change komutunda, doğrulama için genel anahtar eklenecek veya değiştirilecek Destination içindedir.

Bazı ekleme veya düzenleme komutlarında, örneğin bir takma ad eklerken veya bir hedef ya da host adını değiştirirken, ek bir hedef referans alınabilir. Bu durumda, ikinci bir imza dahil edilmeli ve her ikisi de doğrulanmalıdır. İkinci imza "iç" imzadır ve önce imzalanır ve doğrulanır ("dış" imza hariç tutularak). İstemci, değişiklikleri doğrulamak ve kabul etmek için gerekli ek eylemleri gerçekleştirmelidir.

oldsig her zaman "iç" imzadır. 'oldsig' veya 'sig' anahtarları mevcut olmadan imzala ve doğrula. sig her zaman "dış" imzadır. 'oldsig' anahtarı mevcut olduğunda ancak 'sig' anahtarı olmadığında imzala ve doğrula.

#### İmzalar için Girdi

İmzayı oluşturmak veya doğrulamak için bir bayt akışı oluşturmak için aşağıdaki gibi serileştirin:

- "sig" anahtarını kaldır
- Oldsig ile doğruluyorsa, "oldsig" anahtarını da kaldır
- Yalnızca Add veya Change komutları için `example.i2p=b64dest` çıktısı ver
- Herhangi bir anahtar kalırsa, `#!` çıktısı ver
- Seçenekleri UTF-8 anahtarına göre sırala, yinelenen anahtarlar varsa başarısız ol
- Her anahtar/değer için `key=value` çıktısı ver, ardından (son anahtar/değer değilse) bir `#` ekle

Notlar:

- Yeni satır çıktısı verme
- Çıktı kodlaması UTF-8'dir
- Tüm hedef ve imza kodlaması I2P alfabesi kullanılarak Base 64 formatındadır
- Anahtarlar ve değerler büyük/küçük harfe duyarlıdır
- Host adları küçük harfle olmalıdır

## Uyumluluk

hosts.txt formatındaki tüm yeni satırlar başta yorum karakterleri kullanılarak uygulanır, bu nedenle tüm eski I2P sürümleri yeni komutları yorum olarak yorumlayacaktır.

I2P router'ları yeni spesifikasyona güncellendiğinde, eski yorumları yeniden yorumlamayacaklar, ancak abonelik beslemelerinin sonraki getirmelerinde yeni komutları dinlemeye başlayacaklar. Bu nedenle ad sunucularının komut girişlerini bir şekilde kalıcı hale getirmeleri veya router'ların tüm geçmiş komutları getirmesini sağlayacak etag desteğini etkinleştirmeleri önemlidir.
