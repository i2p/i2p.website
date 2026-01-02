---
title: "Adres Aboneliği Besleme Komutları"
description: "Adres abonelik beslemelerine yönelik, ana makine adı sahiplerinin kayıtlarını güncelleyip yönetmelerini sağlayan bir uzantı"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Genel Bakış

Bu belirtim, adres abonelik akışını komutlarla genişleterek ad sunucularının ana makine adı sahiplerinden gelen kayıt güncellemelerini yayınlamasına olanak tanır. İlk olarak [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (Eylül 2014) kapsamında önerildi, 0.9.26 sürümünde (Haziran 2016) uygulandı ve CLOSED durumuyla ağ genelinde devreye alındı.

Sistem, ilk uygulanmasından bu yana istikrarlı ve değişmeden kalmış olup, I2P 2.10.0’da (Router API 0.9.65, Eylül 2025) aynı şekilde çalışmayı sürdürmektedir.

## Motivasyon

Daha önce, hosts.txt abonelik sunucuları verileri yalnızca basit bir hosts.txt biçiminde gönderirdi:

```
example.i2p=b64destination
```
Bu temel biçim birkaç sorun yarattı:

- Ana makine adı sahipleri, ana makine adlarıyla ilişkili Hedefi güncelleyemezler (örneğin, imzalama anahtarını daha güçlü bir kriptografik türe yükseltmek için).
- Ana makine adı sahipleri ana makine adlarından keyfi olarak vazgeçemezler. İlgili Hedefin özel anahtarlarını doğrudan yeni sahibine vermeleri gerekir.
- Bir alt alan adının karşılık gelen temel ana makine adı tarafından kontrol edildiğini doğrulamanın bir yolu yoktur. Bu durum şu anda yalnızca bazı ad sunucuları tarafından tek tek uygulanmaktadır.

## Tasarım

Bu belirtim, hosts.txt biçimine komut satırları ekler. Bu komutlarla, ad sunucuları hizmetlerini genişleterek ek özellikler sağlayabilir. Bu belirtimi uygulayan istemciler, bu özellikleri standart abonelik süreci aracılığıyla dinleyebilir.

Tüm komut satırları, ilgili Destination (bir hizmetin kriptografik adresi) tarafından imzalanmış olmalıdır. Bu, değişikliklerin yalnızca ana makine adı sahibinin talebi üzerine yapılmasını sağlar.

## Güvenlik Etkileri

Bu belirtim anonimliği etkilemez.

Destination (I2P hedef tanımlayıcısı) anahtarının kontrolünü kaybetme riski artmıştır; çünkü onu ele geçiren biri, ilişkili herhangi bir ana bilgisayar adı üzerinde değişiklik yapmak için bu komutları kullanabilir. Ancak bu, mevcut duruma kıyasla daha büyük bir sorun değildir; zira bir Destination ele geçiren biri bir ana bilgisayar adını taklit edebilir ve trafiğini (kısmen) ele geçirebilir. Artan risk, ana bilgisayar adı sahiplerine, bir ana bilgisayar adıyla ilişkilendirilmiş Destination’ı, Destination’ın ele geçirildiğine inandıkları durumda değiştirme olanağı verilerek dengelenmektedir. Bu, mevcut sistemde mümkün değildir.

## Teknik Şartname

### Yeni Satır Türleri

İki yeni çizgi türü vardır:

1. **Add ve Change komutları:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Kaldırma komutları:**

```
#!key1=val1#key2=val2...
```
#### Sıralama

Bir besleme her zaman doğru sırada ya da eksiksiz olmayabilir. Örneğin, change komutu bir satırda add komutundan önce görünebilir ya da add komutu olmadan görünebilir.

Anahtarlar herhangi bir sırada olabilir. Yinelenen anahtarlara izin verilmez. Tüm anahtarlar ve değerler büyük-küçük harfe duyarlıdır.

### Ortak Anahtarlar

**Tüm komutlarda zorunludur:**

**sig** : Hedefin imzalama anahtarı kullanılarak oluşturulmuş Base64 imza

**İkinci bir ana bilgisayar adına ve/veya hedefe referanslar:**

**oldname** : İkinci bir ana makine adı (yeni veya değiştirilmiş)

**olddest** : İkinci bir Base64 hedefi (yeni veya değiştirilmiş)

**oldsig** : olddest'teki imzalama anahtarını kullanan ikinci bir Base64 imzası

**Diğer yaygın anahtarlar:**

**eylem** : Bir komut

**name** : Ana makine adı; yalnızca kendisinden önce `example.i2p=b64dest` yoksa mevcuttur.

**dest** : Base64 hedef, yalnızca öncesinde `example.i2p=b64dest` yoksa bulunur

**date** : epoch (Unix zaman başlangıcı) başlangıcından beri saniye cinsinden

**expires** : epoch (Unix zamanının başlangıcı) itibarıyla saniye cinsinden

### Komutlar

"Add" komutu dışındaki tüm komutlar `action=command` anahtar/değer çifti içermelidir.

Eski istemcilerle uyumluluk için, aşağıda belirtildiği gibi komutların çoğunun başına `example.i2p=b64dest` eklenir. Değişiklikler için bunlar her zaman yeni değerlerdir. Eski değerlerin tümü anahtar/değer bölümüne dahil edilir.

Listelenen anahtarlar zorunludur. Tüm komutlar burada tanımlanmayan ek anahtar/değer çiftleri içerebilir.

#### Ana bilgisayar adı ekle

**Başında example.i2p=b64dest varsa** : EVET, bu yeni ana makine adı ve hedeftir.

**eylem** : DAHİL EDİLMEZ, örtük olarak kabul edilir.

**sig** : imza

Örnek:

```
example.i2p=b64dest#!sig=b64sig
```
#### Ana Bilgisayar Adını Değiştir

**Başında example.i2p=b64dest varsa** : EVET, bu yeni ana makine adı ve eski hedeftir.

**eylem** : ad değişikliği

**oldname** : eski ana makine adı, değiştirilecek

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Hedefi Değiştir

**Ön eki example.i2p=b64dest olan** : EVET, bu eski ana makine adı ve yeni hedeftir.

**action** : changedest

**olddest** : eski hedef, değiştirilecek

**oldsig** : olddest kullanılarak oluşturulan imza

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Ana Bilgisayar Adına Takma Ad Ekle

**Önünde example.i2p=b64dest var** : EVET, bu yeni (takma ad) ana makine adı ve eski destination (hedef) anlamına gelir.

**eylem** : addname

**oldname** : eski ana bilgisayar adı

**sig** : imza

Örnek:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Hedef Takma Adı Ekle

(Şifreleme yükseltmesi için kullanılır)

**Öncesinde example.i2p=b64dest varsa** : EVET, bu, eski ana makine adı ve yeni (alternatif) destination (hedef) demektir.

**eylem** : adddest

**olddest** : eski hedef

**oldsig** : olddest kullanan imza

**sig** : dest kullanılarak oluşturulan imza

Örnek:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Alt Alan Adı Ekle

**Başına subdomain.example.i2p=b64dest eklenmiş** : EVET, bu yeni alt alan adı ve destination (hedef).

**action** : addsubdomain

**oldname** : bir üst düzeydeki ana makine adı (example.i2p)

**olddest** : daha üst düzey hedef (örneğin example.i2p)

**oldsig** : olddest kullanılarak oluşturulan imza

**sig** : dest kullanılarak oluşturulan imza

Örnek:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Üstveriyi Güncelle

**example.i2p=b64dest ile başlayan** : EVET, bu eski ana makine adı ve hedeftir.

**eylem** : güncelleme

**sig** : imza

(güncellenmiş anahtarları buraya ekleyin)

Örnek:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Ana bilgisayar adını kaldır

**Başına example.i2p=b64dest eklenmiş** : HAYIR, bunlar seçeneklerde belirtilir

**eylem** : kaldır

**name** : ana bilgisayar adı

**dest** : hedef

**sig** : imza

Örnek:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Bu hedefe sahip olanların tümünü kaldır

**Başına example.i2p=b64dest eklenmesi** : HAYIR, bunlar seçeneklerde belirtilir

**action** : removeall

**dest** : hedef

**sig** : imza

Örnek:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### İmzalar

Tüm komutlar, ilgili Destination (I2P hedef adresi) tarafından imzalanmalıdır. İki Destination içeren komutlar iki imza gerektirebilir.

`oldsig` her zaman "iç" imzadır. `oldsig` veya `sig` anahtarları mevcut değilken imzalayın ve doğrulayın. `sig` her zaman "dış" imzadır. `oldsig` anahtarı mevcutken ancak `sig` anahtarı mevcut değilken imzalayın ve doğrulayın.

#### İmzalar için girdi

İmzayı oluşturmak veya doğrulamak için bir bayt akışı üretmek üzere, aşağıdaki gibi serileştirin:

1. `sig` anahtarını kaldırın
2. Doğrulama `oldsig` ile yapılıyorsa, `oldsig` anahtarını da kaldırın
3. Yalnızca Add veya Change komutları için, `example.i2p=b64dest` çıktısını verin
4. Herhangi bir anahtar kalırsa, `#!` çıktısını verin
5. Seçenekleri UTF-8 anahtarına göre sıralayın, yinelenen anahtarlar varsa hata verin
6. Her anahtar/değer çifti için `key=value` çıktısını verin, ardından (son anahtar/değer çifti değilse) bir `#` ekleyin

**Notlar**

- Çıktıya yeni satır eklemeyin
- Çıktı kodlaması UTF-8'dir
- Tüm hedef ve imza kodlaması, I2P alfabesi kullanılarak Base 64 biçimindedir
- Anahtarlar ve değerler büyük/küçük harfe duyarlıdır
- Ana makine adları küçük harfli olmalıdır

#### Mevcut İmza Türleri

I2P 2.10.0 itibarıyla, Destination'lar (hedef adresler) için aşağıdaki imza türleri desteklenmektedir:

- **EdDSA_SHA512_Ed25519** (Tür 7): 0.9.15'ten beri hedefler için en yaygınıdır. 32 baytlık bir açık anahtar ve 64 baytlık bir imza kullanır. Bu, yeni hedefler için önerilen imza türüdür.
- **RedDSA_SHA512_Ed25519** (Tür 13): Yalnızca hedefler ve şifrelenmiş leaseSet'ler için kullanılabilir (0.9.39'dan beri).
- Eski türler (DSA_SHA1, ECDSA varyantları): Hâlâ desteklenir ancak 0.9.58 itibarıyla yeni Router Kimlikleri için kullanımdan kaldırılmıştır.

Not: Kuantum-sonrası kriptografik seçenekler I2P 2.10.0 itibarıyla kullanılabilir, ancak henüz varsayılan imza türleri değil.

## Uyumluluk

hosts.txt biçimindeki tüm yeni satırlar, baştaki yorum karakterleri (`#!`) kullanılarak uygulanır; bu nedenle daha eski tüm I2P sürümleri, yeni komutları yorum satırları olarak değerlendirip bunları sorunsuzca görmezden gelir.

I2P router’lar yeni spesifikasyona güncelendiğinde, eski yorumları yeniden yorumlamayacaklar, ancak abonelik beslemelerini daha sonra getirirken yeni komutları dinlemeye başlayacaklar. Bu nedenle ad sunucularının komut girdilerini bir şekilde kalıcı olarak saklamaları ya da router’ların geçmiş tüm komutları alabilmeleri için ETag (HTTP Entity Tag üstbilgisi) desteğini etkinleştirmeleri önemlidir.

## Uygulama Durumu

**İlk dağıtım:** Sürüm 0.9.26 (7 Haziran 2016)

**Mevcut durum:** I2P 2.10.0'a kadar kararlı ve değişmeden kaldı (Router API 0.9.65, Eylül 2025)

**Öneri durumu:** KAPALI (başarıyla ağ genelinde devreye alındı)

**Gerçekleme konumu:** `apps/addressbook/java/src/net/i2p/addressbook/` I2P Java router içinde

**Temel sınıflar:** - `SubscriptionList.java`: Abonelik işlemlerini yönetir - `Subscription.java`: Tek tek abonelik akışlarını işler - `AddressBook.java`: Adres Defteri'nin temel işlevleri - `Daemon.java`: Adres Defteri arka plan hizmeti

**Varsayılan abonelik URL'si:** `http://i2p-projekt.i2p/hosts.txt`

## Taşıma Ayrıntıları

Abonelikler, koşullu GET desteği olan HTTP’yi kullanır:

- **ETag başlığı:** Verimli değişiklik tespitine olanak tanır
- **Last-Modified başlığı:** Abonelik güncelleme zamanlarını izler
- **304 Not Modified:** İçerik değişmediğinde sunucuların bunu döndürmesi gerekir
- **Content-Length:** Tüm yanıtlar için şiddetle önerilir

I2P router, uygun önbellekleme desteğiyle standart HTTP istemcisi davranışını kullanır.

## Sürüm Bağlamı

**I2P sürümleme notu:** Yaklaşık 1.5.0 sürümü (Ağustos 2021) civarında, I2P 0.9.x sürümlemesinden anlamsal sürümlemeye (1.x, 2.x vb.) geçti. Ancak, geriye dönük uyumluluk için dahili Router API sürümü 0.9.x numaralandırmasını kullanmaya devam ediyor. Ekim 2025 itibarıyla, güncel sürüm I2P 2.10.0 ve Router API sürümü 0.9.65’tir.

Bu spesifikasyon belgesi, aslen 0.9.49 sürümü (Şubat 2021) için yazılmış olup, abonelik besleme sisteminde 0.9.26’daki ilk uygulamasından bu yana hiçbir değişiklik yapılmadığından, mevcut 0.9.65 sürümü (I2P 2.10.0) için de tamamen doğrudur.

## Referanslar

- [Öneri 112 (Orijinal)](/proposals/112-addressbook-subscription-feed-commands/)
- [Resmi Spesifikasyon](/docs/specs/subscription/)
- [I2P Adlandırma Dokümantasyonu](/docs/overview/naming/)
- [Ortak Yapılar Spesifikasyonu](/docs/specs/common-structures/)
- [I2P Kaynak Kodu Deposu](https://github.com/i2p/i2p.i2p)
- [I2P Gitea Deposu](https://i2pgit.org/I2P_Developers/i2p.i2p)

## İlgili Gelişmeler

Abonelik besleme sistemi değişmemiş olsa da, I2P'nin adlandırma altyapısına ilişkin aşağıdaki ilgili gelişmeler ilginizi çekebilir:

- **Genişletilmiş Base32 Adları** (0.9.40+): Şifrelenmiş leasesets için 56+ karakterli base32 adreslerine destek. Abonelik akışı biçimini etkilemez.
- **.i2p.alt TLD Kaydı** (RFC 9476, 2023 sonları): .i2p.alt'ın alternatif bir TLD olarak resmi GANA kaydı. Gelecekteki router güncellemeleri .alt sonekini kaldırabilir, ancak abonelik komutlarında herhangi bir değişiklik gerekmez.
- **Kuantum Sonrası Kriptografi** (2.10.0+): Mevcut, ancak varsayılan değil. Abonelik akışlarında imza algoritmaları için gelecekte değerlendirilecektir.
