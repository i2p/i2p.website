---
title: "Yazılım Güncelleme Belirtimi"
description: "I2P yazılım güncelleme mekanizması, SU3 dosya formatı ve haber beslemesi için spesifikasyon"
slug: "updates"
aliases:
  - "/tr/updates"
  - "/tr/updates/"
category: "Tasarım"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Genel Bakış

I2P, otomatik yazılım güncellemesi için basit ama güvenli bir sistem kullanır. Router konsolu, yapılandırılabilir bir I2P URL'sinden periyodik olarak bir haber dosyası çeker. Varsayılan proje haber sunucusu çökerse diye, proje web sitesine işaret eden sabit kodlanmış bir yedek URL vardır.

Haber dosyasının içeriği router konsolunun ana sayfasında görüntülenir. Ayrıca, haber dosyası yazılımın en güncel sürüm numarasını içerir. Eğer sürüm numarası router'ın sürüm numarasından daha yüksekse, kullanıcıya bir güncellemenin mevcut olduğunu belirten bir gösterge görüntüler.

Router, yapılandırıldıysa yeni sürümü isteğe bağlı olarak indirebilir veya indirip kurabilir.

## Eski Haber Dosyası Belirtimi

Bu format, 0.9.17 sürümünden itibaren su3 haber formatı ile değiştirilmiştir.

news.xml dosyası aşağıdaki öğeleri içerebilir:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
i2p.release girdisindeki parametreler aşağıdaki gibidir. Tüm anahtarlar büyük/küçük harf duyarsızdır. Tüm değerler çift tırnak içinde olmalıdır.

**date** : Router sürümünün çıkış tarihi. Kullanılmıyor. Format belirtilmemiş.

**minJavaVersion** : Mevcut sürümü çalıştırmak için gereken minimum Java sürümü. 0.9.9 sürümü itibariyle.

**minVersion** : Mevcut sürüme güncellemek için gereken router'ın minimum sürümü. Eğer bir router bundan daha eski ise, kullanıcının önce ara bir sürüme (manuel olarak?) güncelleme yapması gerekir. 0.9.9 sürümü itibarıyla.

**su3Clearnet** : .su3 güncelleme dosyasının clearnet'te (I2P olmayan ağda) bulunabileceği bir veya daha fazla HTTP URL'si. Birden fazla URL boşluk veya virgülle ayrılmalıdır. 0.9.9 sürümünden itibaren.

**su3SSL** : .su3 güncelleme dosyasının clearnet'te (I2P olmayan ağda) bulunabileceği bir veya daha fazla HTTPS URL'si. Birden fazla URL boşluk veya virgülle ayrılmalıdır. 0.9.9 sürümünden itibaren.

**sudTorrent** : Güncellemenin .sud (pack200 olmayan) torrent'i için magnet bağlantısı. 0.9.4 sürümünden itibaren.

**su2Torrent** : Güncellemenin .su2 (pack200) torrent'i için magnet bağlantısı. 0.9.4 sürümünden itibaren.

**su3Torrent** : Güncellemenin .su3 (yeni format) torrent'i için magnet bağlantısı. 0.9.9 sürümü itibarıyla.

**version** : Gerekli. Mevcut en güncel router sürümü.

Elementler, tarayıcılar tarafından yorumlanmasını önlemek için XML yorumları içinde dahil edilebilir. i2p.release elementi ve sürümü gereklidir. Diğerleri isteğe bağlıdır. NOT: Ayrıştırıcı sınırlamaları nedeniyle bir elementin tamamı tek bir satırda olmalıdır.

## Güncelleme Dosyası Spesifikasyonu

0.9.9 sürümünden itibaren, i2pupdate.su3 olarak adlandırılan imzalı güncelleme dosyası, aşağıda belirtilen "su3" dosya formatını kullanacaktır. Onaylı sürüm imzacıları 4096-bit RSA anahtarları kullanacaktır. Bu imzacılar için X.509 genel anahtar sertifikaları router kurulum paketlerinde dağıtılmaktadır. Güncellemeler, yeni onaylı imzacılar için sertifikalar içerebilir ve/veya iptal için silinecek sertifikaların listesini içerebilir.

## Eski Güncelleme Dosyası Spesifikasyonu

Bu format 0.9.9 sürümü itibariyle kullanımdan kaldırılmıştır.

İmzalı güncelleme dosyası, geleneksel olarak i2pupdate.sud adıyla adlandırılan, başına 56 baytlık başlık eklenmiş basit bir zip dosyasıdır. Başlık şunları içerir:

- 40-byte'lık bir DSA [İmza](/docs/specs/common-structures#signature)
- UTF-8 formatında 16-byte'lık bir I2P sürümü, gerekirse sondaki sıfırlarla doldurulmuş

İmza sadece zip arşivini kapsar - başa eklenen sürümü değil. İmza, router'a yapılandırılmış DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) anahtarlarından biriyle eşleşmelidir ve bu anahtar, mevcut proje yayın yöneticilerinin anahtarlarının sabit kodlanmış varsayılan listesini içerir.

Sürüm karşılaştırma amaçları için, sürüm alanları [0-9]* içerir, alan ayırıcıları '-', '_' ve '.' karakterleridir ve diğer tüm karakterler göz ardı edilir.

Sürüm 0.8.8 itibarıyla, sürüm ayrıca zip dosyası yorumu olarak UTF-8 formatında, sonundaki sıfırlar olmadan belirtilmelidir. Güncellenen router, başlıktaki sürümün (imza kapsamında olmayan) zip dosyası yorumundaki sürümle (imza kapsamında olan) eşleştiğini doğrular. Bu, başlıktaki sürüm numarasının sahtecilik yapılmasını önler.

## İndirme ve Kurulum

Router önce yapılandırılabilir I2P URL'leri listesinden birinden güncelleme dosyasının başlığını yerleşik HTTP istemcisi ve proxy'si kullanarak indirir ve sürümün daha yeni olduğunu kontrol eder. Bu, en son dosyaya sahip olmayan güncelleme ana bilgisayarları sorununu önler. Router daha sonra tam güncelleme dosyasını indirir. Router kurulumdan önce güncelleme dosyası sürümünün daha yeni olduğunu doğrular. Ayrıca tabii ki imzayı doğrular ve yukarıda açıklandığı gibi zip dosyası yorumunun başlık sürümüyle eşleştiğini doğrular.

Zip dosyası çıkarılır ve I2P yapılandırma dizinindeki "i2pupdate.zip" dosyasına kopyalanır (Linux'ta ~/.i2p).

0.7.12 sürümü itibariyle, router Pack200 açma işlemini desteklemektedir. Zip arşivi içindeki .jar.pack veya .war.pack uzantılı dosyalar şeffaf bir şekilde .jar veya .war dosyasına açılır. .pack dosyaları içeren güncelleme dosyaları geleneksel olarak '.su2' uzantısıyla adlandırılır. Pack200, güncelleme dosyalarını yaklaşık %60 oranında küçültür.

0.8.7 sürümünden itibaren, zip arşivi bir lib/jbigi.jar dosyası içeriyorsa router libjbigi.so ve libjcpuid.so dosyalarını silecek, böylece yeni dosyalar jbigi.jar'dan çıkarılacaktır.

0.8.12 sürümünden itibaren, zip arşivi deletelist.txt dosyası içeriyorsa, router orada listelenen dosyaları silecektir. Format şu şekildedir:

- Her satırda bir dosya adı
- Tüm dosya adları kurulum dizinine göre göreli; mutlak dosya adlarına izin verilmez, ".." ile başlayan dosyalar olmaz
- Yorumlar '#' ile başlar

Router daha sonra deletelist.txt dosyasını silecektir.

## SU3 Dosya Spesifikasyonu

Bu spesifikasyon, sürüm 0.9.9 itibariyle router güncellemeleri, sürüm 0.9.14 itibariyle reseed verisi, sürüm 0.9.15 itibariyle eklentiler ve sürüm 0.9.17 itibariyle haber dosyası için kullanılmaktadır.

### Önceki .sud/.su2 formatındaki sorunlar

- Sihirli numara veya bayrak yok
- Sıkıştırma, pack200 olup olmadığı veya imzalama algoritması belirtmenin yolu yok
- Sürüm imza tarafından kapsanmıyor, bu nedenle zip dosyası yorumunda (router dosyaları için) veya plugin.config dosyasında (eklentiler için) bulunması zorunlu kılınarak uygulanıyor
- İmzalayan belirtilmediği için doğrulayıcı bilinen tüm anahtarları denemek zorunda
- Veri-öncesi-imza formatı dosya oluşturmak için iki geçiş gerektiriyor

### Hedefler

- Yukarıdaki sorunları düzelt
- Daha güvenli imza algoritmasına geçiş yap
- Mevcut sürüm denetleyicileriyle uyumluluk için sürüm bilgisini aynı format ve ofset içinde tut
- Tek geçişli imza doğrulama ve dosya çıkarma

### Spesifikasyon

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Gelecek sürümlerle uyumluluk için kullanılmayan tüm alanlar 0 olarak ayarlanmalıdır.

### İmza Detayları

İmza, byte 0'dan başlayarak tüm başlığı ve içeriğin sonuna kadar olan kısmı kapsar. Ham imzalar kullanıyoruz. Verinin hash'ini alın (byte 8-9'daki imza türünün ima ettiği hash türünü kullanarak) ve bunu "ham" imzalama veya doğrulama fonksiyonuna geçirin (örneğin Java'da "NONEwithRSA").

İmza doğrulama ve içerik çıkarma tek geçişte uygulanabilse de, bir uygulama doğrulamaya başlamadan önce hash türünü belirlemek için ilk 10 baytı okuyup tamponlamalıdır.

Çeşitli imza türleri için imza uzunlukları [Signature](/docs/specs/common-structures#signature) spesifikasyonunda verilmiştir. Gerekirse imzayı önde gelen sıfırlarla doldurun. Çeşitli imza türlerinin parametreleri için [kriptografi ayrıntıları sayfasına](/docs/specs/cryptography#sig) bakın.

### Notlar

İçerik türü, güven alanını belirtir. Her içerik türü için, istemciler bu içeriği imzalamaya yetkili taraflar için bir dizi X.509 genel anahtar sertifikası tutar. Yalnızca belirtilen içerik türü için olan sertifikalar kullanılabilir. Sertifika, imzalayanın ID'si ile aranır. İstemciler, içerik türünün uygulama için beklendiği gibi olduğunu doğrulamalıdır.

Tüm değerler ağ bayt sıralamasındadır (big endian).

Java "NONEwithRSA" ile uyumlu Raw RSA imzalarının python implementasyonu için [bu Stack Overflow makalesine](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530) bakın.

## SU3 Router Güncelleme Dosyası Spesifikasyonu

### SU3 Detayları

- SU3 İçerik Türü: 1 (ROUTER GÜNCELLEMESİ)
- SU3 Dosya Türü: 0 (ZIP)
- SU3 Sürümü: Router sürümü

Zip dosyalarındaki jar ve war dosyaları, yukarıda "su2" dosyaları için belgelendiği gibi artık pack200 ile sıkıştırılmıyor, çünkü son Java çalışma zamanları bunu artık desteklemiyor.

### Notlar

- Sürümler için, SU3 versiyonu "temel" router versiyonudur, örneğin "0.9.20".
- 0.9.20 sürümünden itibaren desteklenen geliştirme yapıları için, SU3 versiyonu "tam" router versiyonudur, örneğin "0.9.20-5" veya "0.9.20-5-rc". [I2P kaynak kodunda](https://github.com/i2p/i2p.i2p) RouterVersion.java dosyasına bakın.

## SU3 Reseed Dosya Spesifikasyonu

0.9.14 sürümünden itibaren, reseed verileri "su3" dosya formatında teslim edilmektedir.

### Hedefler

- Kurbanları ayrı, güvenilmeyen bir ağa yönlendirebilecek ortadaki adam saldırılarını önlemek için güçlü imzalar ve güvenilir sertifikalarla imzalanmış dosyalar.
- Güncellemeler ve eklentiler için halihazırda kullanılan su3 dosya formatını kullan
- 200 dosya almak yavaş olan reseeding işlemini hızlandırmak için tek sıkıştırılmış dosya

### Spesifikasyon

1. Dosya "i2pseeds.su3" olarak adlandırılmalıdır. 0.9.42 sürümünden itibaren, istemci mevcut ağ ID'sinin 2 olduğunu varsayarak istek URL'sine "?netid=2" sorgu dizesi eklemelidir. Bu, çapraz ağ bağlantılarını önlemek için kullanılabilir. Test ağları farklı bir ağ ID'si ayarlamalıdır. Detaylar için 147 numaralı öneriye bakın.
2. Dosya, web sunucusunda router bilgileri ile aynı dizinde bulunmalıdır.
3. Bir router önce (dizin URL'si)/i2pseeds.su3 dosyasını almaya çalışacaktır; bu başarısız olursa dizin URL'sini alacak ve ardından bağlantılarda bulunan bireysel router bilgi dosyalarını alacaktır.

### SU3 Detayları

- SU3 İçerik Türü: 3 (RESEED)
- SU3 Dosya Türü: 0 (ZIP)
- SU3 Sürümü: Epoch'tan (dönem başlangıcından) itibaren saniye, ASCII formatında (date +%s). 2038 veya 2106'da sıfırlanmaz.
- Zip dosyasındaki router bilgi dosyaları "üst seviyede" bulunmalıdır. Zip dosyasında dizin yoktur.
- Router bilgi dosyaları eski reseed mekanizmasında olduğu gibi "routerInfo-(44 karakterli base 64 router hash).dat" şeklinde adlandırılmalıdır. I2P base 64 alfabesi kullanılmalıdır.

### Notlar

- Uyarı: Birçok reseed'in IPv6 üzerinden yanıt vermediği bilinmektedir. IPv4'ü zorlama veya tercih etme önerilir.
- Uyarı: Bazı reseed'ler kendi imzalı CA sertifikaları kullanır. Uygulamalar, reseed işlemi yaparken bu CA'ları içe aktarıp güvenmeli veya kendi imzalı reseed'leri reseed listesinden çıkarmalıdır.
- Reseed imzalayıcı anahtarları, RSA-4096 anahtarları (imza türü 6) ile kendi imzalı X.509 sertifikaları olarak uygulamalara dağıtılır. Uygulamalar sertifikalardaki geçerli tarihleri zorunlu kılmalıdır.

## SU3 Eklenti Dosyası Spesifikasyonu

0.9.15 sürümünden itibaren, eklentiler "su3" dosya formatında paketlenebilir.

### SU3 Detayları

- SU3 İçerik Türü: 2 (PLUGIN)
- SU3 Dosya Türü: 0 (ZIP) - Ayrıntılar için [plugin spesifikasyonuna](/docs/specs/plugin) bakın.
- SU3 Sürümü: Plugin sürümü, plugin.config dosyasındakiyle eşleşmelidir.

Zip içindeki jar ve war dosyaları, yukarıda "su2" dosyaları için belgelendiği gibi pack200 ile sıkıştırılmamalıdır, çünkü güncel Java çalışma zamanları artık bunu desteklememektedir.

## SU3 Haber Dosyası Spesifikasyonu

0.9.17 sürümünden itibaren, haberler "su3" dosya formatında teslim edilmektedir.

### Hedefler

- Güçlü imzalar ve güvenilir sertifikalarla imzalanmış haberler
- Güncellemeler, reseeding ve eklentiler için halihazırda kullanılan su3 dosya formatını kullanma
- Standart ayrıştırıcılarla kullanım için standart XML formatı
- Standart besleme okuyucuları ve oluşturucularla kullanım için standart Atom formatı
- Konsolda görüntülemeden önce HTML'in temizlenmesi ve doğrulanması
- HTML konsolu olmayan Android ve diğer platformlarda kolay uygulama için uygun

### SU3 Detayları

- SU3 İçerik Türü: 4 (NEWS)
- SU3 Dosya Türü: 1 (XML) veya 3 (XML.GZ)
- SU3 Sürümü: Epoch'tan bu yana geçen saniye, ASCII formatında (date +%s). 2038 veya 2106'da sıfırlanmaz.
- Dosya Formatı: XML veya gziplenmiş XML, [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed içeren. Karakter kümesi UTF-8 olmalıdır.

### Atom Feed Detayları

Aşağıdaki `<feed>` öğeleri kullanılır:

**`<entry>`** : Bir haber öğesi. Aşağıya bakın.

**`<i2p:release>`** : I2P güncelleme metadata'sı. Aşağıya bakın.

**`<i2p:revocations>`** : Sertifika iptalleri. Aşağıya bakınız.

**`<i2p:blocklist>`** : Blocklist verileri. Aşağıya bakın.

**`<updated>`** : Zorunlu. Feed için zaman damgası ([RFC 4287](https://tools.ietf.org/html/rfc4287) bölüm 3.3 ve [RFC 3339](https://tools.ietf.org/html/rfc3339)'a uygun).

### Atom Girişi Detayları

Haber akışındaki her Atom `<entry>` router konsolunda ayrıştırılabilir ve görüntülenebilir. Aşağıdaki öğeler kullanılır:

**`<author>`** : İsteğe bağlı. `<name>` içerir - Girdi yazarının adı.

**`<content>`** : Gerekli. İçerik, type="xhtml" olmalıdır. XHTML, izin verilen öğelerin beyaz listesi ve izin verilmeyen özniteliklerin kara listesi ile sanitize edilecektir. İstemciler, beyaz listede olmayan bir öğeyle karşılaştıklarında bir öğeyi, kapsayan girdiyi veya tüm beslemyi görmezden gelebilir.

**`<link>`** : İsteğe bağlı. Daha fazla bilgi için bağlantı.

**`<summary>`** : İsteğe bağlı. Araç ipucu için uygun kısa özet.

**`<title>`** : Gerekli. Haber girişinin başlığı.

**`<updated>`** : Gerekli. Bu giriş için zaman damgası ([RFC 4287](https://tools.ietf.org/html/rfc4287) bölüm 3.3 ve [RFC 3339](https://tools.ietf.org/html/rfc3339) standartlarına uygun).

### Atom i2p:release Detayları

Feed'de en az bir `<i2p:release>` varlığı bulunmalıdır. Her biri aşağıdaki öznitelikleri ve varlıkları içerir:

**date (öznitelik)** : Zorunlu. Bu giriş için zaman damgası ([RFC 4287](https://tools.ietf.org/html/rfc4287) bölüm 3.3 ve [RFC 3339](https://tools.ietf.org/html/rfc3339)'a uygun). Tarih ayrıca kısaltılmış yyyy-mm-dd formatında da olabilir ('T' olmadan); bu RFC 3339'daki "full-date" formatıdır. Bu formatta herhangi bir işlem için zamanın 00:00:00 UTC olduğu varsayılır.

**minJavaVersion (özellik)** : Mevcut ise, mevcut sürümü çalıştırmak için gereken minimum Java sürümü.

**minVersion (öznitelik)** : Mevcut ise, mevcut sürüme güncellemek için gereken router'ın minimum sürümü. Bir router bundan daha eski ise, kullanıcı önce bir ara sürüme (manuel olarak?) güncelleme yapmalıdır.

**`<i2p:version>`** : Gerekli. Mevcut en son router sürümü.

**`<i2p:update>`** : Bir güncelleme dosyası (bir veya daha fazla). En az bir alt öğe içermelidir.   - type (öznitelik): "sud", "su2", veya "su3". Tüm `<i2p:update>` öğeleri arasında benzersiz olmalıdir.   - `<i2p:clearnet>`: Ağ dışı doğrudan indirme bağlantıları (sıfır veya daha fazla). href (öznitelik): Standart clearnet http bağlantısı.   - `<i2p:clearnetssl>`: Ağ dışı doğrudan indirme bağlantıları (sıfır veya daha fazla). href (öznitelik): Standart clearnet https bağlantısı.   - `<i2p:torrent>`: Ağ içi magnet bağlantısı. href (öznitelik): Bir magnet bağlantısı.   - `<i2p:url>`: Ağ içi doğrudan indirme bağlantıları (sıfır veya daha fazla). href (öznitelik): Ağ içi http .i2p bağlantısı.

### Atom i2p:revocations Detayları

Bu varlık isteğe bağlıdır ve feed'de en fazla bir `<i2p:revocations>` varlığı bulunur. Bu özellik 0.9.26 sürümünden itibaren desteklenmektedir.

`<i2p:revocations>` varlığı bir veya daha fazla `<i2p:crl>` varlığı içerir. `<i2p:crl>` varlığı aşağıdaki nitelikleri içerir:

**updated (öznitelik)** : Gerekli. Bu giriş için zaman damgası ([RFC 4287](https://tools.ietf.org/html/rfc4287) bölüm 3.3 ve [RFC 3339](https://tools.ietf.org/html/rfc3339)'a uygun). Tarih ayrıca kısaltılmış yyyy-mm-dd formatında da olabilir ('T' olmadan); bu RFC 3339'daki "tam-tarih" formatıdır. Bu formatta herhangi bir işlem için saatin 00:00:00 UTC olduğu varsayılır.

**id (nitelik)** : Gerekli. Bu CRL'nin yaratıcısı için benzersiz bir id.

**(varlık içeriği)** : Gerekli. Satır sonları ile birlikte standart base 64 kodlanmış Sertifika İptal Listesi (CRL), '-----BEGIN X509 CRL-----' satırı ile başlar ve '-----END X509 CRL-----' satırı ile biter. CRL'ler hakkında daha fazla bilgi için [RFC 5280](https://tools.ietf.org/html/rfc5280)'e bakınız.

### Atom i2p:blocklist Detayları

Bu varlık isteğe bağlıdır ve feed içinde en fazla bir `<i2p:blocklist>` varlığı bulunur. Bu özelliğin 0.9.28 sürümünde uygulanması planlanmaktadır.

`<i2p:blocklist>` varlığı bir veya daha fazla `<i2p:block>` veya `<i2p:unblock>` varlığı, bir "updated" varlığı ve "signer" ile "sig" özniteliklerini içerir:

**signer (nitelik)** : Gerekli. Bu engel listesini imzalamak için kullanılan genel anahtar için benzersiz bir kimlik (UTF-8).

**sig (öznitelik)** : Gerekli. code:b64sig formatında bir imza, burada code ASCII imza türü numarasıdır ve b64sig base 64 kodlanmış imzadır (I2P alfabesi). İmzalanacak verinin spesifikasyonu için aşağıya bakınız.

**`<updated>`** : Gerekli. Engelleme listesi için zaman damgası ([RFC 4287](https://tools.ietf.org/html/rfc4287) bölüm 3.3 ve [RFC 3339](https://tools.ietf.org/html/rfc3339)'a uygun). Tarih ayrıca kısaltılmış yyyy-mm-dd formatında da olabilir ('T' olmadan); bu RFC 3339'daki "full-date" formatıdır. Bu formatta, herhangi bir işlem için saatin UTC 00:00:00 olduğu varsayılır.

**`<i2p:block>`** : İsteğe bağlı, birden fazla öğeye izin verilir. Tek bir giriş, ya gerçek bir IPv4 veya IPv6 adresi, ya da 44 karakterlik base 64 router hash (I2P alfabesi). IPv6 adresleri kısaltılmış formatta olabilir ("::" içeren). Netmask içeren girişler için destek, örneğin x.y.0.0/16, isteğe bağlıdır. Sunucu adları için destek isteğe bağlıdır.

**`<i2p:unblock>`** : İsteğe bağlı, birden fazla varlığa izin verilir. `<i2p:block>` ile aynı format.

**İmza spesifikasyonu:** İmzalanacak veya doğrulanacak veriyi oluşturmak için, aşağıdaki verileri ASCII kodlamasında birleştirin: Güncellenen string ve ardından yeni satır (ASCII 0x0a), sonra alındığı sırayla her blok girişi ve her birinin ardından yeni satır, sonra alındığı sırayla her engelleme kaldırma girişi ve her birinin ardından yeni satır.

## Engelleme Listesi Dosya Spesifikasyonu

TBD, uygulanmadı, öneri 130'a bakın. Engelleme listesi güncellemeleri haber dosyasında teslim edilir, yukarıya bakın.

## Gelecek Çalışmalar

- Router güncelleme mekanizması web router konsolu'nun bir parçasıdır. Şu anda router konsolu olmayan gömülü bir router'ın güncellenmesi için herhangi bir hüküm bulunmamaktadır.

## Referanslar

- **[CRYPTO-SIG]** [Kriptografi - İmzalar](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P Kaynak Kodu](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Plugin Spesifikasyonu](/docs/specs/plugin)
- **[Python]** [Python RSA Ham İmzalar](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Tarih ve Zaman](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom Sendikasyon Formatı](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Sertifika İptal Listeleri](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [İmza Türü](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [İmzalama Genel Anahtarı Türü](/docs/specs/common-structures#signingpublickey)
