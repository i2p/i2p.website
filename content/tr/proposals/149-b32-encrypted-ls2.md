---
title: "Şifreli LS2 için B32"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
toc: true
---

## Not
Ağ dağıtımı ve test sürecinde.
Küçük revizyonlara tabi olabilir.
Resmi spesifikasyon için bkz. [SPEC](/docs/specs/b32-for-encrypted-leasesets/).


## Genel Bakış

Standart Base 32 ("b32") adresleri hedefin karma değerini içerir.
Bu, şifreli ls2 (öneri 123) için işe yaramaz.

Şifreli bir LS2 (öneri 123) için geleneksel bir base 32 adresi kullanamazsınız,
çünkü sadece hedefin karışımını içerir. Körlenmemiş genel anahtarı sağlamaz.
İstemcilerin hedefin genel anahtarını, imzalama türünü,
körlenmiş imzalama türünü ve bir kira setini almak ve şifresini çözmek
için isteğe bağlı bir gizli veya özel anahtarı bilmesi gerekir.
Bu nedenle, yalnızca bir base 32 adresi yetersizdir.
İstemcinin ya tam hedefe (genel anahtarı içeren) ya da sadece genel anahtara ihtiyacı vardır.
İstemcinin tam hedefi bir adres defterinde varsa ve adres defteri
karışım yoluyla tersine aramayı destekliyorsa, genel anahtar alınabilir.

Bu nedenle, karışım yerine genel anahtarı bir base32 adresine
koyacak yeni bir formata ihtiyacımız var. Bu format ayrıca
genel anahtarın imzalama türünü ve körleme şemasının imzalama türünü içermelidir.

Bu öneri, bu adresler için yeni bir b32 formatını belgeliyor.
Bu yeni formata tartışmalarda
"b33" adresi olarak atıfta bulunsak da, gerçek yeni format
alışılmış ".b32.i2p" ekini korur.

## Hedefler

- Gelecekteki körleme şemalarını desteklemek için hem körlenmemiş hem de körlenmiş imza türlerini ekle 
- 32 bayttan büyük genel anahtarları destekle
- Özellikle başlangıçta b32 karakterlerinin tamamen veya çoğunlukla rastgele olmasını sağla
  (tüm adreslerin aynı karakterlerle başlamasını istemiyoruz)
- Ayrıştırılabilir
- Körleme sırrı ve/veya istemci başına anahtar gereksinimini belirt
- Yazım hatalarını tespit etmek için bir denetim toplamı ekle
- Uzunluğu minimize et, normal kullanım için DNS etiket uzunluğunu 63 karakterin altında tut
- Büyük-küçük harf duyarlılığı olmayan base 32 kullanmaya devam et
- Alışılmış ".b32.i2p" ekini koru.

## Hedef Dışı

- Körleme sırrı ve/veya istemci başına anahtar içeren "özel" bağlantıları destekleme;
  bu güvensiz olur.


## Tasarım

- Yeni format, körlenmemiş genel anahtarı, körlenmemiş imza türünü
  ve körlenmiş imza türünü içerecek.
- Seçmeli olarak sır ve/veya özel anahtarı içerebilir, yalnızca özel bağlantılar için
- Var olan ".b32.i2p" ekini kullanacak, ancak daha uzun bir uzunluğa sahip olacak.
- Bir denetim toplamı ekle.
- Şifreli kiralama setleri için adresler, 52 karakterlik (32 bayt) geleneksel base 32 adreslerine
  kıyasla 56 veya daha fazla kodlanmış karakter (35 veya daha fazla kodlanmış bayt) tarafından tanımlanır.


## Spesifikasyon

### Oluşturma ve kodlama

{56+ karakter}.b32.i2p (ikili 35+ karakter) şeklinde bir ana bilgisayar adı oluştur:

```text
bayrak (1 bayt)
    bit 0: 1 bayt imza tipi için 0, 2 bayt imza tipi için 1
    bit 1: gizli yok, gizli gerekiyorsa 1
    bit 2: istemci başına kimlik doğrulama yok, 
           istemci özel anahtarı gerekiyorsa 1
    bitler 7-3: Kullanılmıyor, 0 olarak ayarla

  genel anahtar imza türü (bayraklarda belirtildiği gibi 1 veya 2 bayt)
    1 bayt ise üst baytın sıfır olduğu varsayılır

  körlenmiş anahtar imza türü (bayraklarda belirtildiği gibi 1 veya 2 bayt)
    1 bayt ise üst baytın sıfır olduğu varsayılır

  genel anahtar
    İmza türü tarafından belirlenen bayt sayısı

```

Son işleme ve denetim toplamı:

```text
Yukarıdaki gibi ikili verileri oluştur.
  Denetim toplamını küçük-endian olarak işle.
  Denetim toplamını hesapla = CRC-32(data[3:end])
  data[0] ^= (byte) denetim toplamı
  data[1] ^= (byte) (denetim toplamı >> 8)
  data[2] ^= (byte) (denetim toplamı >> 16)

  hostname = Base32.encode(data) || ".b32.i2p"
```

b32'nin sonundaki kullanılmayan bitlerin hepsi 0 olmalıdır.
Standart bir 56 karakterlik (35 bayt) adres için kullanılmayan bit yoktur.


### Kod Çözme ve Doğrulama

```text
hostname'den ".b32.i2p" çıkar
  data = Base32.decode(hostname)
  Denetim toplamını hesapla = CRC-32(data[3:end])
  Denetim toplamını küçük-endian olarak işle.
  flags = data[0] ^ (byte) denetim toplamı
  1 bayt imza türleri varsa:
    pubkey imza türü = data[1] ^ (byte) (denetim toplamı >> 8)
    körlenmiş imza türü = data[2] ^ (byte) (denetim toplamı >> 16)
  aksi takdirde (2 bayt imza türleri):
    pubkey imza türü = data[1] ^ ((byte) (denetim toplamı >> 8)) || data[2] ^ ((byte) (denetim toplamı >> 16))
    körlenmiş imza türü = data[3] || data[4]
  bayraklara göre geri kalanını çözerek genel anahtarı elde et
```


### Gizli ve Özel Anahtar Bitleri

Gizli ve özel anahtar bitleri istemciler, proxy'ler veya diğer
istemci tarafı kod için, kira setinin şifresini çözmek için gizli
ve/veya özel anahtar gerekeceğini belirtir. Belirli uygulamalar,
kullanıcıdan gerekli verileri sağlaması için bir istemde bulunabilir
veya gerekli veriler eksikse bağlantı girişimlerini reddedebilir.


## Gerekçe

- İlk 3 baytı karma ile XOR yapmak, sınırlı bir denetim toplamı
  kapasitesi sağlar ve tüm base32 karakterlerinin başlangıçta
  rasgele olmasını sağlar.
  Sadece birkaç bayrak ve imza türü kombinasyonu geçerlidir, bu nedenle
  herhangi bir yazım hatası geçersiz bir kombinasyon oluşturabilir ve reddedilir.
- Alışılmış durumda (1 bayt imza türleri, gizli yok, istemci başına
  kimlik doğrulama yok),
  hostname {56 karakter}.b32.i2p olacak, 35 bayta dekodlanacak,
  Tor ile aynı.
- Tor'un 2 baytlık denetim toplamı 1/64K yanlış negatif oranına sahiptir.
  3 bayt ile, birkaç baytın yok sayılmasıyla
  bizimki bir milyona yaklaşıyor, çünkü çoğu bayrak/imza türü
  kombinasyonu geçersiz.
- Adler-32 küçük girdiler için kötü bir seçimdir ve küçük
  değişiklikleri tespit etmek için kötü bir seçimdir .
  Bunun yerine CRC-32 kullan. CRC-32 hızlıdır ve yaygın olarak bulunur.

## Önbellekleme

Bu önerinin kapsamı dışında olsa da, yönlendiriciler ve/veya
istemciler genel anahtar ile hedef arasındaki eşlemeyi (muhtemelen
kalıcı olarak) hatırlamalı ve önbelleğe almalıdırlar.


## Notlar

- Eski ve yeni tatları uzunluklarına göre ayırt et. Eski b32 adresleri
  her zaman {52 karakter}.b32.i2p'dir. Yenileri {56+ karakter}.b32.i2p'dir.
- Tor tartışma başlığı: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- 2 bayt imza türlerinin hiçbir zaman gerçekleşeceğini beklemeyin, henüz
  13'teyiz. Şu anda uygulamanıza gerek yok.
- İstenirse, yeni formatın jump bağlantılarında (ve jump sunucuları tarafından sunulması
  halinde) kullanılabileceği gibi b32 de kullanılabilir.


## Sorunlar

- 32 bayttan uzun herhangi bir gizli, özel anahtar
  veya genel anahtar DNS maksimum etiket uzunluğunu aşacaktır.
  Tarayıcılar muhtemelen umursamaz.


## Geçiş

Geriye dönük uyumluluk sorunları yok. Daha uzun b32 adresleri, eski
yazılımdaki 32 baytlık karmalara dönüştürülemeyecektir.
