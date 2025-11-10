---
title: "I2P Geliştirme Yol Haritası"
description: "I2P ağı için mevcut geliştirme planları ve tarihsel dönüm noktaları"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P, kademeli bir geliştirme modeli izliyor** ve sürümler yaklaşık her 13 haftada bir yayımlanıyor. Bu yol haritası, masaüstü ve Android Java sürümlerini tek, kararlı bir sürüm yolunda kapsar.

**Son Güncelleme:** Ağustos 2025

</div>

## 🎯 Gelecek Sürümler

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Sürüm 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Hedef: Erken Aralık 2025
</div>

- Hibrit PQ MLKEM Ratchet son hali, varsayılan olarak etkinleştir (öneri 169)
- Jetty 12, Java 17+ gerektir
- PQ (taşıma) üzerinde çalışmaya devam et (öneri 169)
- LS hizmet kaydı parametreleri için I2CP arama desteği (öneri 167)
- Tünel başına sınırlama
- Prometheus dostu istatistik alt sistemi
- Datagram 2/3 için SAM desteği

</div>

---

## 📦 Son Sürümler

### 2025 Sürümleri

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Sürüm 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Yayın Tarihi: 8 Eylül 2025</span>

- i2psnark UDP izleyici desteği (öneri 160)
- I2CP LS hizmet kaydı parametreleri (kısmi) (öneri 167)
- I2CP asenkron arama API'si
- Hibrit PQ MLKEM Ratchet Beta (öneri 169)
- PQ (taşımalar) üzerinde çalışmaya devam et (öneri 169)
- Tünel oluşturma bant genişliği parametreleri (öneri 168) Bölüm 2 (işleme)
- Tünel başına sınırlama üzerinde çalışmaya devam et
- Kullanılmayan taşıma ElGamal kodunu kaldır
- Eski SSU2 "aktif sınırlama" kodunu kaldır
- Eski istatistik günlüğü desteğini kaldır
- İstatistik/grafik alt sistemi temizleme
- Gizli mod iyileştirmeleri ve düzeltmeler

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Sürüm 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Yayın Tarihi: 2 Haziran 2025</span>

- Netdb haritası
- Datagram2, Datagram3 uygulaması (öneri 163)
- LS hizmet kaydı parametresi üzerinde çalışmalara başla (öneri 167)
- PQ üzerinde çalışmalara başla (öneri 169)
- Tünel başına sınırlama üzerinde çalışmaya devam et
- Tünel oluşturma bant genişliği parametreleri (öneri 168) Bölüm 1 (gönderme)
- Linux'ta varsayılan olarak /dev/random kullan
- Gereksiz LS render kodunu kaldır
- Yenilikleri HTML olarak görüntüle
- HTTP sunucu iş parçacığı kullanımını azalt
- Otomatik yayılma dolumu kaydı düzelt
- Wrapper güncellemesi 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Sürüm 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Yayın Tarihi: 29 Mart 2025</span>

- SHA256 bozulma hatasını düzelt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Sürüm 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Yayın Tarihi: 17 Mart 2025</span>

- Java 21+ yükleyici hatasını düzelt
- "Loopback" hatasını düzelt
- Dışa yönelik istemci tünelleri için tünel testlerini düzelt
- Boşluk içeren yollara yükleme hatasını düzelt
- Eski Docker konteynerini ve kütüphanelerini güncelle
- Konsol bildirim baloncukları
- SusiDNS en son ekleme ile sırala
- Noise'ta SHA256 havuzunu kullan
- Konsol koyu tema düzeltmeleri ve iyileştirmeleri
- .i2p.alt desteği

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Sürüm 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Yayın Tarihi: 3 Şubat 2025</span>

- RouterInfo yayımlama iyileştirmeleri
- SSU2 ACK verimliliğini artırma
- Yinelenen röle mesajlarının SSU2 işleme iyileştirmeleri
- Daha hızlı/değişken arama zaman aşımı
- LS süresi dolma iyileştirmeleri
- Simetrik NAT sınırında değişiklikler
- Daha fazla formda POST zorunluluğu
- SusiDNS koyu tema düzeltmeleri
- Bant genişliği testi düzenlemeleri
- Yeni Gan Çin çevirisi
- Kürtçe UI seçeneği ekle
- Yeni Jammy yapı
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 2024 Sürümleri</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 Ekim 2024</span>

- i2ptunnel HTTP sunucu iş parçacığı kullanımını azaltma
- I2PTunnel'de Genel UDP Tünelleri
- I2PTunnel'de Tarayıcı Proxy'si
- Web Sitesi Taşınması
- Sarı renge dönen tüneller için düzeltme
- Konsol /netdb yeniden yapımı

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 Ağustos 2024</span>

- Konsolda iframe boyut sorunlarını düzelt
- Grafikleri SVG'ye dönüştür
- Çeviri durumu raporunu paketle

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19 Temmuz 2024</span>

- Netdb bellek kullanımını azalt
- SSU1 kodunu kaldır
- i2psnark geçici dosya sızıntıları ve duraklamalarını düzelt
- i2psnark'ta daha verimli PEX
- Konsol grafiklerinin JS yenilemesi
- Grafik çizim iyileştirmeleri
- Susimail JS arama
- OBEP'de daha verimli mesaj işleme
- Yerel hedef I2CP aramalarında daha verimli
- JS değişken kapsama alanı sorunlarını düzelt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15 Mayıs 2024</span>

- HTTP kesilmesini düzelt
- Simetrik NAT algılanırsa G yeteneğini yayınla
- rrd4j 3.9.1-preview sürümüne güncelle

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 Mayıs 2024</span>

- NetDB DDoS azaltımları
- Tor blok listesi
- Susimail düzeltmeleri ve arama
- SSU1 kodunu kaldırmaya devam et
- Tomcat 9.0.88 sürümüne güncelle

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 Nisan 2024</span>

- Konsol iframe iyileştirmeleri
- i2psnark bant genişliği sınırlayıcısını yeniden tasarlama
- i2psnark ve susimail için Javascript sürükle-bırak
- i2ptunnel SSL hata işleme iyileştirmeleri
- i2ptunnel kalıcı HTTP bağlantısı desteği
- SSU1 kodunu kaldırmaya başla
- SSU2 röle etiketi talep işleme iyileştirmeleri
- SSU2 eş testi düzeltmeleri
- Susimail iyileştirmeleri (yükleme, markdown, HTML e-posta desteği)
- Tünel eş seçimi ayarlamaları
- RRD4J 3.9 sürümüne güncelle
- gradlew 8.5 sürümüne güncelle

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Sürüm 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18 Aralık 2023</span>

- NetDB bağlam yönetimi/Sabah NetDB
- Aşırı yüklü yönlendiricileri düşük öncelikli yaparak tıkanıklık yeteneklerini yönet
- Android yardımcı kitaplığını yeniden canlandır
- i2psnark yerel torrent dosyası seçici
- NetDB arama işleyici düzeltmeleri
- SSU1'i devre dışı bırak
- Gelecekte yayımlama yapan yönlendiricilerin yasaklanması
- SAM düzeltmeleri
- Susimail düzeltmeleri
- UPnP düzeltmeleri

</div>

---

### 2023-2022 Sürümleri

<details>
<summary>2023-2022 sürümlerini genişletmek için tıklayın</summary>

**Sürüm 2.3.0** — Yayın Tarihi: 28 Haziran 2023

- Tünel eş seçimi iyileştirmeleri
- Kullanıcı yapılandırılabilir blok listesi süresi dolması
- Aynı kaynaktan gelen hızlı patlama aramalarını kısıtla
- Tekrar algılama bilgi kaçağını düzelt
- Çok katmanlı leaseSets için NetDB düzeltmeleri
- Yanıt olarak alınan leaseSets için NetDB düzeltmeleri

**Sürüm 2.2.1** — Yayın Tarihi: 12 Nisan 2023

- Paketleme düzeltmeleri

**Sürüm 2.2.0** — Yayın Tarihi: 13 Mart 2023

- Tünel eş seçimi iyileştirmeleri
- Akışı yeniden oynatma düzeltmesi

**Sürüm 2.1.0** — Yayın Tarihi: 10 Ocak 2023

- SSU2 düzeltmeleri
- Tünel oluşturma tıkanıklık düzeltmeleri
- SSU eş testi ve simetrik NAT algılama düzeltmeleri
- Bozuk LS2 şifreli leaseSets düzeltme
- SSU 1'i devre dışı bırakma seçeneği (ön hazırlık)
- Sıkıştırılabilir dolgu (öneri 161)
- Yeni konsol eşler durumu sekmesi
- SOCKS proxy'sine torsocks desteği ekleyin ve diğer SOCKS iyileştirme ve düzeltmeleri

**Sürüm 2.0.0** — Yayın Tarihi: 21 Kasım 2022

- SSU2 bağlantı taşınması
- SSU2 anında onaylar
- Varsayılan olarak SSU2'yi etkinleştir
- i2ptunnel'de SHA-256 görsel proxy kimlik doğrulaması
- Modern AGP kullanmak için Android derleme sürecini güncelle
- Platformlar Arası(Masaüstü) I2P tarayıcı otomatik yapılandırma desteği

**Sürüm 1.9.0** — Yayın Tarihi: 22 Ağustos 2022

- SSU2 eş testi ve röle uygulaması
- SSU2 düzeltmeleri
- SSU MTU/PMTU iyileştirmeleri
- Küçük bir router bölümüne SSU2'yi etkinleştir
- Çıkmaz algılayıcısı ekle
- Daha fazla sertifika ithalat hatası düzeltmeler
- Yönlendirici yeniden başlatıldıktan sonra i2psnark DHT yeniden başlatmayı düzelt

**Sürüm 1.8.0** — Yayın Tarihi: 23 Mayıs 2022

- Yönlendirici aile düzeltmeleri ve iyileştirmeleri
- Yumuşak yeniden başlatma düzeltmeleri
- SSU düzeltmeleri ve performans iyileştirmeleri
- I2PSnark bağımsız düzeltmeler ve iyileştirmeler
- Güvenilen aileler için Sybil cezasından kaçınılması
- Tünel oluşturma yanıt süresi aşımını azaltma
- UPnP düzeltmeleri
- BOB kaynak kodunu kaldır
- Sertifika özetlerini düzelt
- Tomcat 9.0.62
- SSU2 desteği için yeniden düzenleme (öneri 159)
- SSU2 temel protokolünün başlangıç uygulaması (öneri 159)
- Android uygulamaları için SAM yetkilendirme açılır penceresi
- i2p.firefox'ta özel dizin kurulumları için desteği artır

**Sürüm 1.7.0** — Yayın Tarihi: 21 Şubat 2022

- BOB'u kaldır
- Yeni i2psnark torrent editörü
- i2psnark bağımsız düzeltmeler ve iyileştirmeler
- NetDB güvenilirliği iyileştirmeleri
- Sistem tepside açılır mesajlar ekleyin
- NTCP2 performans iyileştirmeleri
- İlk adım başarısız olduğunda giden tüneli kaldır
- Üçüncü taraf istemci tünel oluşturma başarısızlıklarından sonra araştırmacıya geri dönüş
- Aynı IP kısıtlamaları için tünel geri yüklemesi
- i2ptunnel UDP desteğinde yeniden düzenleme için I2
