---
title: "IPv6 Taşıma İyileştirmeleri"
number: "158"
author: "zzz, orijinal"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Kapalı"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
toc: true
---

## Not
Ağ dağıtımı ve test süreci devam ediyor.
Küçük revizyonlara tabi olabilir.


## Genel Bakış

Bu öneri, IPv6 için SSU ve NTCP2 taşımalarında iyileştirmeler uygulamayı amaçlamaktadır.


## Motivasyon

IPv6 dünyada büyüdükçe ve IPv6 destekli yapılandırmalar (özellikle mobilde) daha yaygın hale geldikçe,
IPv6 desteğimizi geliştirmemiz ve tüm yönlendiricilerin IPv4 destekli olduğu varsayımını ortadan kaldırmamız gerekiyor.


### Bağlantı Kontrolü

Eşler seçilirken, tüneller veya mesajları yönlendirmek için OBEP/IBGW yolları seçilirken,
yönlendirici A'nın yönlendirici B'ye bağlanıp bağlanamayacağını hesaplamak yararlıdır.
Genel olarak, bu, A'nın B'nin ilan ettiği gelen adreslerden birine uyan bir taşıma ve adres türü (IPv4/v6)
için giden kapasitesine sahip olup olmadığını belirlemek anlamına gelir.

Ancak, çoğu durumda A'nın yeteneklerini bilmiyoruz ve varsayımlar yapmamız gerekiyor.
Eğer A gizli veya güvenlik duvarı arkasındaysa, adresler yayınlanmaz ve doğrudan bilgimiz yoktur -
bu yüzden IPv4 destekli ve IPv6 destekli olmadığını varsayıyoruz.
Çözüm, IPv4 ve IPv6 için giden kapasite belirtmek amacıyla Yönlendirici Bilgilerine iki yeni "cap" veya yetenek eklenmesidir.


### IPv6 Tanıtıcıları

Spesifikasyonlarımız [SSU](/docs/specs/ssu2/) ve [SSU-SPEC](/docs/legacy/ssu/),
IPv6 tanıtıcılarının IPv4 tanıtımları için desteklenip desteklenmediği konusunda hatalar ve tutarsızlıklar içermektedir.
Her durumda, bu ne Java I2P'de ne de i2pd'de uygulanmamıştır.
Bu düzeltilmelidir.


### IPv6 Tanıtımları

Spesifikasyonlarımız [SSU](/docs/specs/ssu2/) ve [SSU-SPEC](/docs/legacy/ssu/), 
IPv6 tanıtımlarının desteklenmediğini açıkça belirtmektedir.
Bu varsayım altında, IPv6'nın asla güvenlik duvarı arkasında olmayacağı düşünüldü.
Bu açıkça doğru değil ve güvenlik duvarı arkasındaki IPv6 yönlendiricileri için desteğimizi geliştirmemiz gerekiyor.


### Tanıtım Diyagramları

Efsane: ----- IPv4, ====== IPv6'dır

Mevcut ipv4 yalnızca:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


IPv4 tanıtımı, IPv6 tanıtıcı

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

IPv6 tanıtımı, IPv6 tanıtıcı


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

IPv6 tanıtımı, IPv4 tanıtıcı

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Tasarım

Uygulanacak üç değişiklik bulunmaktadır.

- Yönlendirici Adres yeteneklerine giden IPv4 ve IPv6 desteğini belirtmek için "4" ve "6" yeteneklerini ekle
- IPv6 tanıtıcıları üzerinden IPv4 tanıtımlarını destekle
- IPv4 ve IPv6 tanıtıcıları üzerinden IPv6 tanıtımlarını destekle


## Şartname

### 4/6 Yetenek

Bu başlangıçta resmi bir teklif olmadan uygulandı, ancak IPv6 tanıtımları için gerekli olduğu için burada ekliyoruz.
Ayrıca bkz. [CAPS](http://zzz.i2p/topics/3050).


İki yeni yetenek "4" ve "6" tanımlanmıştır.
Bu yeni yetenekler, Yönlendirici Bilgilerindeki değil, Yönlendirici Adresindeki "caps" özelliğine eklenecektir.
NTCP2 için tanımlanmış bir "caps" özelliğimiz şu anda yok.
Tanıtıcıları olan bir SSU adresi, tanım gereği şu anda ipv4'tür. ipv6 tanıtımı hiç desteklemiyoruz.
Ancak, bu teklif IPv6 tanıtımları ile uyumludur. Aşağıya bakın.

Ek olarak, bir yönlendirici I2P-over-Yggdrasil gibi bir kaplama ağı üzerinden bağlantı desteğine sahip olabilir,
ancak bir adres yayınlamak istemiyor veya bu adres standart bir IPv4 veya IPv6 formatına sahip değil.
Bu yeni yetenek sistemi, bu ağları destekleyecek kadar esnek olmalıdır.

Aşağıdaki değişiklikleri tanımlıyoruz:

NTCP2: "caps" özelliği eklenmesi

SSU: Yönlendirici Adresinde bir ana veya tanıtıcı olmadan, IPv4, IPv6, veya her ikisi için giden desteği belirtmek için destek ekleyin.

Her iki taşıma: Aşağıdaki caps değerlerini tanımlayın:

- "4": IPv4 desteği
- "6": IPv6 desteği

Tek bir adreste birden fazla değer desteklenebilir. Aşağıya bakın.
Yönlendirici Adresinde "ana" değeri yoksa en az bir bu yetenekler zorunludur.
Yönlendirici Adresinde bir "ana" değeri varsa en fazla bir bu yetenekler isteğe bağlıdır.
Kaplama ağları veya diğer bağlantılar için destek göstermek üzere gelecekte ek taşıma yetenekleri tanımlanabilir.


#### Kullanım durumları ve örnekler

SSU:

Ana bilgisayarlı SSU: 4/6 isteğe bağlı, birden fazla değil.
Örnek: SSU caps="4" host="1.2.3.4" anahtar=... port="1234"

Sadece bir için giden SSU, diğeri yayınlanır: Sadece yetenekler, 4/6.
Örnek: SSU caps="6"

Tanıtıcılarlı SSU: asla birleştirilmez. 4 veya 6 gereklidir.
Örnek: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... anahtar=...

Gizli SSU: Sadece yetenekler, 4, 6 veya 46. Birden fazla izin verilir.
İki adres, biri 4 ve biri 6 gereksizdir.
Örnek: SSU caps="46"

NTCP2:

Ana bilgisayarlı NTCP2: 4/6 isteğe bağlı, birden fazla değil.
Örnek: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

Sadece bir için giden NTCP2, diğeri yayınlanır: Yetenekler, s, v sadece, 4/6/y, birden fazla izin verilir.
Örnek: NTCP2 caps="6" i=... s=... v="2"

Gizli NTCP2: Yetenekler, s, v sadece 4/6, birden fazla izin verilir. İki adres, biri 4 ve biri 6 gerekli değil.
Örnek: NTCP2 caps="46" i=... s=... v="2"


### IPv4 için IPv6 Tanıtıcıları

Hataları ve tutarsızlıkları düzeltmek için aşağıdaki değişiklikler gereklidir.
Bunu ayrıca önerinin "birinci kısmı" olarak da tanımladık.

#### Spesifikasyon Değişiklikleri

[SSU](/docs/specs/ssu2/) şu anda (IPv6 notları) diyor ki:

IPv6, sürüm 0.9.8 itibariyle desteklenmektedir. Yayınlanan aktarıcı adresleri IPv4 veya IPv6 olabilir ve Alice-Bob iletişimi IPv4 veya IPv6 üzerinden olabilir.

Aşağıdaki ekleyin:

Her ne kadar spesifikasyon 0.9.8 sürümü itibariyle değiştirilmiş olsa da, Alice-Bob iletişimi IPv6 üzerinden gerçekte 0.9.50 sürümüne kadar desteklenmemiştir.
Erken sürüm Java yönlendiriciler hataen IPv6 adresleri için 'C' yeteneğini yayınladı,
ancak bunlar gerçekte IPv6 üzerinden tanıtıcı olarak hareket etmiyorlardı.
Bu nedenle, yönlendiriciler bir IPv6 adresinde 'C' yeteneğine yalnızca yönlendirici sürümü 0.9.50 veya üstü ise güvenmelidir.


[SSU-SPEC](/docs/legacy/ssu/) şu anda (Aktarım İsteği) diyor ki:

IP adresi yalnızca paket kaynağı adresi ve portundan farklı gelmesi durumunda dahil edilir.
Mevcut uygulamada, IP uzunluğu her zaman 0 ve port her zaman 0'dır,
ve alıcı, paket kaynağı adresi ve portunu kullanmalıdır.
Bu mesaj IPv4 veya IPv6 aracılığıyla gönderilebilir. Eğer IPv6 ise, Alice IPv4 adresini ve portunu dahil etmelidir.

Aşağıdaki ekleyin:

Bu mesajı IPv6 üzerinden gönderirken bir IPv4 adresini tanıtmak için IP ve port eklenmelidir.
Bu, 0.9.50 sürümünden itibaren desteklenmektedir.


### IPv6 Tanıtımları

SSU aktarıcı mesajlarının üçü de (RelayRequest, RelayResponse ve RelayIntro) 
(Alis, Bob veya Charlie) IP adresinin uzunluğunu belirtmek için IP uzunluğu alanları içerir.

Bu nedenle, mesajların formatında bir değişiklik gerekmez.
Yalnızca sözlük değişiklikleri yapılarak, 16 baytlık IP adreslerine izin verildiği belirtilmelidir.

Spesifikasyonlarda aşağıdaki değişiklikler gereklidir.
Bunu ayrıca önerinin "ikinci kısmı" olarak da tanımladık.


#### Spesifikasyon Değişiklikleri

[SSU](/docs/specs/ssu2/) şu anda (IPv6 notları) diyor ki:

Bob-Charlie ve Alice-Charlie iletişimi yalnızca IPv4 üzerinden yapılır.

[SSU-SPEC](/docs/legacy/ssu/) şu anda (Aktarım İsteği) diyor ki:

IPv6 için aktarıcı uygulama planları yoktur.

Şu şekilde değiştirin:

IPv6 için aktarıcı desteği 0.9.xx sürümünden itibaren desteklenmektedir

[SSU-SPEC](/docs/legacy/ssu/) şu anda (Relay Response) diyor ki:

Charlie's IP adresi IPv4 olmalıdır, çünkü bu, Alice'in Hole Punch'tan sonra SessionRequest'i göndereceği adrestir.
IPv6 için aktarıcı planları yoktur.

Şu şekilde değiştirin:

Charlie's IP adresi IPv4 olabilir ya da 0.9.xx sürümünden itibaren IPv6 olabilir.
Bu, Alice'in Hole Punch'tan sonra SessionRequest'i göndereceği adrestir.
IPv6 için aktarıcı desteği 0.9.xx sürümünden itibaren desteklenmektedir

[SSU-SPEC](/docs/legacy/ssu/) şu anda (Relay Intro) diyor ki:

Alice'in IP adresi her zaman 4 bayt uzunluğundadır çünkü Alice, Charlie'ye IPv4 üzerinden bağlanmaya çalışmaktadır.
Bu mesaj, Bob'un Alice'e RelayResponse içinde dönecek Charlie'nin IPv4 adresini bilmesinin tek yolu olan 
bir kurulu IPv4 bağlantısı üzerinden gönderilmelidir.

Şu şekilde değiştirin:

IPv4 için, Alice'in IP adresi her zaman 4 bayttır çünkü Alice, Charlie'ye IPv4 üzerinden bağlanmaya çalışmaktadır.
0.9.xx sürümünden itibaren, IPv6 desteklenmektedir ve Alice'in IP adresi 16 bayt olabilir.

IPv4 için, bu mesaj, Bob'un Alice'e RelayResponse içinde dönecek Charlie'nin IPv4 adresini bilmesinin tek yolu olan 
bir kurulu IPv4 bağlantısı üzerinden gönderilmelidir.
0.9.xx sürümünden itibaren, IPv6 desteklenmektedir ve bu mesaj, bir kurulu IPv6 bağlantısı üzerinden gönderilebilir.

Ayrıca ekleyin:

0.9.xx sürümünden itibaren, tanıtıcılarla yayınlanan herhangi bir SSU adresi "caps" seçeneğinde "4" veya "6" içermelidir.


## Taşımacılık

Tüm eski yönlendiriciler, NTCP2'de caps özelliğini ve SSU caps özelliğindeki bilinmeyen yetenek karakterlerini görmezden gelmelidir.

Tanıtıcılarla bir SSU adresi içeren ve "4" veya "6" capa sahip olmayan herhangi bir adresin, IPv4 tanıtımı için olduğu varsayılır.
