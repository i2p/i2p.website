---
title: "Taşıma Ağı Kimlik Kontrolü"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Closed"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Genel Bakış

NTCP2 (öneri 111) Bağlantı İsteği aşamasında farklı ağ kimliklerinde gelen bağlantıları reddetmez.
Bağlantı şu anda Alice'in RI'sını Bob kontrol ettiğinde,
Bağlantı Onaylandığı aşamada reddedilmelidir.

Benzer şekilde, SSU da Bağlantı İsteği aşamasında farklı ağ kimliklerinde gelen bağlantıları reddetmez.
Bağlantı şu anda Bob, Alice'in RI'sını kontrol ettiğinde,
Bağlantı Onaylandığı aşamadan sonra reddedilmelidir.

Bu öneri, her iki taşımada da Bağlantı İsteği aşamasını, geri uyumlu bir şekilde ağ kimliğini içerecek şekilde değiştirmektedir.


## Güdü

Yanlış ağdan gelen bağlantılar en kısa sürede reddedilmeli ve
eş kara listeye alınmalıdır.


## Hedefler

- Test ağlarının ve çatallanan ağların çapraz bulaşmasını önlemek

- NTCP2 ve SSU el sıkışmasına ağ kimliği eklemek

- NTCP2 için,
  alıcı (gelen bağlantı) ağ kimliğinin farklı olduğunu tespit edebilmeli,
  böylece eşin IP'sini kara listeye alabilir.

- SSU için,
  alıcı (gelen bağlantı) bağlantı isteği aşamasında kara listeye alamaz,
  çünkü gelen IP sahte olabilir. El sıkışmanın kriptografisini değiştirmek yeterlidir.

- Yanlış ağdan yeniden tohumlamayı önlemek

- Geriye dönük uyumlu olmalıdır


## Hedef Dışı Konular

- NTCP 1 artık kullanılmıyor, bu yüzden değiştirilmeyecek.


## Tasarım

NTCP2 için,
bir değeri XORlamak sadece şifrelemenin başarısız olmasına yol açar ve
alıcı, başlatanı kara listeye almak için yeterli bilgiye sahip olmaz,
bu nedenle bu yaklaşım tercih edilmez.

SSU için,
Bağlantı İsteği sırasında bir yerde ağ kimliğini XORlayacağız.
Bu geri uyumlu olması gerektiğinden, (id - 2) olarak XORlayacağız
böylece bu, mevcut ağ kimliği değeri 2 için bir işleyici olmayacaktır.


## Özellikler

### Dokümantasyon

Geçerli ağ kimliği değerleri için aşağıdaki özellikleri ekleyin:


| Kullanım | NetID Numarası |
|-------|--------------|
| Rezerve Edilmiş | 0 |
| Rezerve Edilmiş | 1 |
| Mevcut Ağ (varsayılan) | 2 |
| Rezerve Gelecek Ağlar | 3 - 15 |
| Çatal ve Test Ağları | 16 - 254 |
| Rezerve | 255 |


Varsayılanı değiştirmek için Java I2P yapılandırması "router.networkID=nnn".
Bunu daha iyi belgeleyin ve çatallanan ve test ağlarını yapılandırmalarına bu ayarı eklemeye teşvik edin.
Diğer uygulamaların bu seçeneği uygulamasını ve belgelemesini teşvik edin.


### NTCP2

Ağ kimliğini içeren Seçenekler'deki (bayt 0) ilk rezerve edilmiş baytı kullanın, şu anda 2.
Ağ kimliğini içerir.
Sıfır değilse, alıcı bunu yerel ağ kimliğinin en az anlamlı baytı ile karşılaştırmalıdır.
Eşleşmezlerse, alıcı hemen bağlantıyı kesmeli ve başlatanın IP'sini kara listeye almalıdır.


### SSU

SSU için, HMAC-MD5 hesaplamasında ((netid - 2) << 8) şeklinde bir XOR ekleyin.

Mevcut:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' eklemeyi, '^' özel veya anlamına gelir.
  payloadLength 2 baytlık bir işaretsiz tam sayıdır
  protocolVersion bir bayt 0x00
```

Yeni:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' eklemeyi, '^' özel veya, '<<' sola kaydırmayı ifade eder.
  payloadLength iki baytlık işaretsiz tam sayı, big endian
  protocolVersion iki bayt 0x0000, big endian
  netid iki baytlık işaretsiz tam sayı, big endian, yasal değerler 2-254
```


### Yeniden Tohumlama

Reseed su3 dosyasının alımına ?netid=nnn parametresini ekleyin.
Reseed yazılımını netid'yi kontrol edecek şekilde güncelleyin. Mevcut ve "2"ye eşit değilse,
iki nedenle reddedilmelidir: bir hata koduyla (belki 403) sonuçlanmalıdır.
Test veya çatallanan ağlar için alternatif bir netid yapılandırılabilmesi için reseed yazılımına yapılandırma seçeneği ekleyin.


## Notlar

Test ağlarını ve çatalları ağ kimliğini değiştirmeye zorlayamayız.
Yapabileceğimiz en iyi şey dokümantasyon ve iletişimdir.
Diğer ağlarla çapraz bulaşma keşfedersek, ağ kimliğinin değiştirilmesinin önemini açıklamak için
geliştiriciler veya operatörlerle iletişime geçmeye çalışmalıyız.


## Sorunlar


## Geçiş

Bu, mevcut ağ kimliği değeri 2 için geriye dönük uyumludur.
Herkesin farklı bir ağ kimliği değeriyle (test veya başka bir şekilde) bir ağ çalıştırması durumu olursa,
bu değişiklik geriye dönük uyumlu değildir.
Ancak, böyle bir durumu bildirmiyoruz.
Eğer sadece bir test ağı ise, sorun yok, sadece tüm yönlendiricileri aynı anda güncelleyin.
