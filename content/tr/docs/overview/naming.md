---
title: "İsimlendirme ve Adres Defteri"
description: "I2P'nin okunabilir alan adlarını hedeflere nasıl eşlediği"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P adresleri uzun kriptografik anahtarlardır. İsimlendirme sistemi, **merkezi bir otorite olmaksızın** bu anahtarların üzerine daha kullanıcı dostu bir katman sağlar. Tüm isimler **yereldir**—her router, bir ana bilgisayar adının hangi hedefe işaret ettiğine bağımsız olarak karar verir.

> **Arka plan bilgisine mi ihtiyacınız var?** [İsimlendirme tartışması](/docs/legacy/naming/) belgesinde I2P'nin merkezi olmayan isimlendirme sisteminin ardındaki özgün tasarım tartışmaları, alternatif öneriler ve felsefi temeller yer almaktadır.

---

## 1. Bileşenler

I2P'nin isimlendirme katmanı, birbirinden bağımsız ancak birlikte çalışan birkaç alt sistemden oluşur:

1. **İsim çözümleme hizmeti** – ana bilgisayar adlarını hedeflere çözümler ve [Base32 ana bilgisayar adlarını](#base32-hostnames) yönetir.
2. **HTTP proxy** – `.i2p` sorgularını router'a iletir ve bir isim bilinmediğinde jump servislerini önerir.
3. **Host-add hizmetleri** – yerel adres defterine yeni girdiler ekleyen CGI tarzı formlar.
4. **Jump servisleri** – verilen bir ana bilgisayar adı için hedefi döndüren uzak yardımcılar.
5. **Adres defteri** – yerel olarak güvenilen bir "güven ağı" kullanarak uzak ana bilgisayar listelerini periyodik olarak getirir ve birleştirir.
6. **SusiDNS** – adres defterlerini, abonelikleri ve yerel geçersiz kılmaları yönetmek için web tabanlı bir kullanıcı arayüzü.

Bu modüler tasarım, kullanıcıların kendi güven sınırlarını tanımlamalarına ve isimlendirme sürecini istedikleri kadar otomatikleştirmelerine olanak tanır.

---

## 2. İsimlendirme Hizmetleri

Router'ın adlandırma API'si (`net.i2p.client.naming`), yapılandırılabilir `i2p.naming.impl=<class>` özelliği aracılığıyla birden fazla arka ucu destekler. Her uygulama farklı arama stratejileri sunabilir, ancak hepsi aynı güven ve çözümleme modelini paylaşır.

### 2.1 Hosts.txt (legacy format)

Eski model, sırayla kontrol edilen üç düz metin dosyası kullanıyordu:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Her satır bir `hostname=base64-destination` eşleştirmesi depolar. Bu basit metin formatı içe/dışa aktarma için tam olarak desteklenmeye devam eder, ancak host listesi birkaç bin girişi aştığında düşük performans nedeniyle artık varsayılan değildir.

---

### 2.2 Blockfile Naming Service (default backend)

**0.8.8 sürümünde** tanıtılan Blockfile Naming Service artık varsayılan arka uçtur. Düz dosyaları, yaklaşık **10 kat daha hızlı sorgulama** sunan yüksek performanslı skiplist tabanlı disk üzerinde anahtar/değer deposu (`hostsdb.blockfile`) ile değiştirir.

**Temel özellikler:** - Birden fazla mantıksal adres defterini (özel, kullanıcı ve ana bilgisayarlar) tek bir ikili veritabanında saklar. - Eski hosts.txt içe/dışa aktarma ile uyumluluğu korur. - Ters arama, meta veriler (eklenme tarihi, kaynak, yorumlar) ve verimli önbelleklemeyi destekler. - Aynı üç katmanlı arama sırasını kullanır: özel → kullanıcı → ana bilgisayarlar.

Bu yaklaşım, geriye dönük uyumluluğu korurken çözümleme hızını ve ölçeklenebilirliği önemli ölçüde iyileştirir.

---

### 2.1 Hosts.txt (eski format)

Geliştiriciler şunlar gibi özel backend'ler uygulayabilir: - **Meta** – birden fazla isimlendirme sistemini bir araya getirir. - **PetName** – `petnames.txt` dosyasında saklanan petname'leri destekler. - **AddressDB**, **Exec**, **Eepget** ve **Dummy** – harici veya yedek çözümleme için.

Blockfile uygulaması, performans ve güvenilirlik nedeniyle genel kullanım için **önerilen** arka uç olmaya devam etmektedir.

---

## 3. Base32 Hostnames

Base32 host adları (`*.b32.i2p`) Tor'un `.onion` adreslerine benzer şekilde çalışır. Bir `.b32.i2p` adresine eriştiğinizde:

1. Router, Base32 yükünü çözer.
2. Hedefi doğrudan anahtardan yeniden oluşturur—**adres defteri araması gerekmez**.

Bu, insan tarafından okunabilir bir hostname olmasa bile erişilebilirliği garanti eder. **0.9.40 sürümünde** tanıtılan genişletilmiş Base32 isimleri **LeaseSet2** ve şifrelenmiş hedefleri destekler.

---

## 4. Address Book & Subscriptions

Adres defteri uygulaması, uzak sunucu listelerini HTTP üzerinden alır ve kullanıcı tarafından yapılandırılan güven kurallarına göre yerel olarak birleştirir.

### 2.2 Blockfile İsimlendirme Servisi (varsayılan arka uç)

- Abonelikler, `hosts.txt` veya artımlı güncelleme akışlarını işaret eden standart `.i2p` URL'leridir.
- Güncellemeler periyodik olarak (varsayılan olarak saatlik) alınır ve birleştirmeden önce doğrulanır.
- Çakışmalar **ilk gelen, ilk hizmet alır** kuralıyla öncelik sırasına göre çözülür:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

**I2P 2.3.0 (Haziran 2023)** sürümünden itibaren, iki varsayılan abonelik sağlayıcısı dahil edilmiştir: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Bu fazlalık, yerel güven modelini korurken güvenilirliği artırır. Kullanıcılar SusiDNS aracılığıyla abonelikleri ekleyebilir veya kaldırabilir.

#### Incremental Updates

Artımlı güncellemeler `newhosts.txt` aracılığıyla alınır (eski `recenthosts.cgi` kavramının yerini alır). Bu uç nokta, verimli, **ETag tabanlı** delta güncellemeleri sağlar—yalnızca son istekten bu yana yeni girişleri veya değişiklik olmadığında `304 Not Modified` döndürür.

---

### 2.3 Alternatif Arka Uçlar ve Eklentiler

- **Host-add servisleri** (`add*.cgi`) isim-hedef eşlemelerinin manuel olarak gönderilmesine izin verir. Kabul etmeden önce her zaman hedefi doğrulayın.  
- **Jump servisleri** uygun anahtar ile yanıt verir ve HTTP proxy üzerinden `?i2paddresshelper=` parametresi ile yönlendirme yapabilir.  
  Yaygın örnekler: `stats.i2p`, `identiguy.i2p` ve `notbob.i2p`.  
  Bu servisler **güvenilir otoriteler değildir**—kullanıcılar hangisini kullanacaklarına kendileri karar vermelidir.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS şu adreste mevcuttur: `http://127.0.0.1:7657/susidns/`

Şunları yapabilirsiniz: - Yerel adres defterlerini görüntüleme ve düzenleme. - Abonelikleri yönetme ve önceliklendirme. - Host listelerini içe/dışa aktarma. - Getirme zamanlamalarını yapılandırma.

**I2P 2.8.1'de Yeni (Mart 2025):** - "En yeniye göre sırala" özelliği eklendi. - Abonelik yönetimi iyileştirildi (ETag tutarsızlıkları için düzeltme).

Tüm değişiklikler **yerel** kalır—her router'ın adres defteri benzersizdir.

---

## 3. Base32 Alan Adları

RFC 9476'yı takip ederek, I2P **`.i2p.alt`** adresini GNUnet Assigned Numbers Authority (GANA) nezdinde **Mart 2025 (I2P 2.8.1)** itibarıyla tescil ettirmiştir.

**Amaç:** Yanlış yapılandırılmış yazılımlardan kaynaklanan kazara DNS sızıntılarını önlemek.

- RFC 9476 uyumlu DNS çözümleyicileri `.alt` alan adlarını genel DNS'e **iletmez**.
- I2P yazılımı `.i2p.alt` ile `.i2p`'yi eşdeğer kabul eder ve çözümleme sırasında `.alt` sonekini kaldırır.
- `.i2p.alt`, `.i2p`'nin yerini almak için **değildir**; bu bir teknik güvenlik önlemidir, yeniden markalama değildir.

---

## 4. Adres Defteri & Abonelikler

- **Destination anahtarları:** 516–616 bayt (Base64)  
- **Host adları:** Maksimum 67 karakter (`.i2p` dahil)  
- **İzin verilen karakterler:** a–z, 0–9, `-`, `.` (çift nokta yok, büyük harf yok)  
- **Ayrılmış:** `*.b32.i2p`  
- **ETag ve Last-Modified:** bant genişliğini en aza indirmek için aktif olarak kullanılır  
- **Ortalama hosts.txt boyutu:** ~800 host için ~400 KB (örnek değer)  
- **Bant genişliği kullanımı:** her 12 saatte bir alındığında ~10 bayt/saniye

---

## 8. Security Model and Philosophy

I2P, merkezi olmayan yapı ve güvenlik karşılığında kasıtlı olarak küresel benzersizliği feda eder—bu, **Zooko's Triangle** (Zooko Üçgeni) ilkesinin doğrudan bir uygulamasıdır.

**Temel ilkeler:** - **Merkezi otorite yok:** tüm aramalar yereldir.   - **DNS ele geçirmeye karşı direnç:** sorgular hedef genel anahtarlarına şifrelenir.   - **Sybil saldırısı önleme:** oylama veya konsensüs tabanlı adlandırma yok.   - **Değiştirilemez eşleşmeler:** yerel bir ilişki oluşturulduktan sonra, uzaktan geçersiz kılınamaz.

Blockchain tabanlı isimlendirme sistemleri (örn. Namecoin, ENS), Zooko üçgeninin her üç tarafını da çözmeyi araştırmıştır, ancak I2P gecikme, karmaşıklık ve yerel güven modeliyle felsefi uyumsuzluk nedeniyle bunlardan kasıtlı olarak kaçınmaktadır.

---

## 9. Compatibility and Stability

- 2023–2025 yılları arasında hiçbir isimlendirme özelliği kullanımdan kaldırılmadı.
- Hosts.txt formatı, atlama servisleri, abonelikler ve tüm isimlendirme API uygulamaları işlevsel durumda.
- I2P Projesi, performans ve güvenlik iyileştirmeleri (NetDB izolasyonu, Sub-DB ayrımı vb.) getirirken katı **geriye dönük uyumluluk** sağlıyor.

---

## 10. Best Practices

- Yalnızca güvenilir abonelikleri tutun; büyük, bilinmeyen host listelerinden kaçının.
- Yükseltme veya yeniden yüklemeden önce `hostsdb.blockfile` ve `privatehosts.txt` dosyalarını yedekleyin.
- Jump servislerini düzenli olarak gözden geçirin ve artık güvenmediğiniz servisleri devre dışı bırakın.
- Unutmayın: adres defteriniz I2P dünyanızın sürümünü tanımlar—**her hostname yereldir**.

---

### Further Reading

- [İsimlendirme Tartışması](/docs/legacy/naming/)  
- [Blockfile Spesifikasyonu](/docs/specs/blockfile/)  
- [Yapılandırma Dosyası Formatı](/docs/specs/configuration/)  
- [Naming Service Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
