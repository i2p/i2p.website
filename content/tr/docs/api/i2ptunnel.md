---
title: "I2PTunnel"
description: "I2P ile arayüz oluşturmak ve hizmet sağlamak için araç"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

I2PTunnel, I2P ağında arayüz oluşturmak ve hizmet sağlamak için temel bir I2P bileşenidir. TCP tabanlı ve medya akış uygulamalarının tünel soyutlaması aracılığıyla anonim olarak çalışmasını sağlar. Bir tünelin hedefi bir [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32) veya tam bir hedef anahtarı ile tanımlanabilir.

Kurulmuş her tunnel yerel olarak dinler (örn. `localhost:port`) ve dahili olarak I2P hedeflerine bağlanır. Bir hizmet barındırmak için, istenen IP ve porta işaret eden bir tunnel oluşturun. Buna karşılık gelen bir I2P destination key oluşturulur ve hizmetin I2P ağı içinde global olarak erişilebilir hale gelmesini sağlar. I2PTunnel web arayüzü [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/) adresinde mevcuttur.

---

## Varsayılan Hizmetler

### Sunucu tüneli

- **I2P Webserver** – I2P üzerinde kolay barındırma için [localhost:7658](http://localhost:7658) adresindeki bir Jetty web sunucusuna tunnel.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### İstemci tünelleri

- **I2P HTTP Proxy** – `localhost:4444` – I2P'ye ve İnternet'e outproxy'ler üzerinden göz atmak için kullanılır.  
- **I2P HTTPS Proxy** – `localhost:4445` – HTTP proxy'nin güvenli varyantı.  
- **Irc2P** – `localhost:6668` – Varsayılan anonim IRC ağ tüneli.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Depo SSH erişimi için client tunnel.  
- **Postman SMTP** – `localhost:7659` – Giden posta için client tunnel.  
- **Postman POP3** – `localhost:7660` – Gelen posta için client tunnel.

> Not: Yalnızca I2P Web Sunucusu varsayılan bir **sunucu tüneli**dir; diğer tüm tüneller harici I2P hizmetlerine bağlanan istemci tünelleridir.

---

## Yapılandırma

I2PTunnel yapılandırma spesifikasyonu [/spec/configuration](/docs/specs/configuration/) adresinde belgelenmiştir.

---

## İstemci Modları

### Standart

Bir I2P hedefindeki bir hizmete bağlanan yerel bir TCP portu açar. Yedeklilik için virgülle ayrılmış birden fazla hedef girişini destekler.

### HTTP

HTTP/HTTPS istekleri için bir proxy tüneli. Yerel ve uzak outproxy'leri, başlık temizlemeyi, önbelleğe almayı, kimlik doğrulamayı ve şeffaf sıkıştırmayı destekler.

**Gizlilik korumaları:**   - Başlıkları kaldırır: `Accept-*`, `Referer`, `Via`, `From`   - Host başlıklarını Base32 hedefleriyle değiştirir   - RFC uyumlu hop-by-hop kaldırma işlemini zorunlu kılar   - Şeffaf açma desteği ekler   - Dahili hata sayfaları ve yerelleştirilmiş yanıtlar sağlar

**Sıkıştırma davranışı:**   - İstekler özel başlık `X-Accept-Encoding: x-i2p-gzip` kullanabilir   - `Content-Encoding: x-i2p-gzip` içeren yanıtlar şeffaf bir şekilde açılır   - Sıkıştırma, verimlilik için MIME türü ve yanıt uzunluğuna göre değerlendirilir

**Kalıcılık (2.5.0'dan beri yeni):**   HTTP Keepalive ve kalıcı bağlantılar artık Gizli Hizmetler Yöneticisi aracılığıyla I2P üzerinde barındırılan hizmetler için desteklenmektedir. Bu, gecikmeyi ve bağlantı yükünü azaltır ancak henüz tüm atlamalar boyunca tam RFC 2616 uyumlu kalıcı soketleri etkinleştirmez.

**Pipelining:**   Desteklenmemektedir ve gereksizdir; modern tarayıcılar bunu kullanımdan kaldırmıştır.

**User-Agent davranışı:**   - **Outproxy:** Güncel Firefox ESR User-Agent kullanır.   - **Internal:** Anonimlik tutarlılığı için `MYOB/6.66 (AN/ON)`.

### IRC İstemcisi

I2P tabanlı IRC sunucularına bağlanır. Gizlilik için tanımlayıcıları filtrelerken güvenli bir komut alt kümesine izin verir.

### SOCKS 4/4a/5

TCP bağlantıları için SOCKS proxy yeteneği sağlar. UDP, Java I2P'de henüz uygulanmamıştır (yalnızca i2pd'de mevcuttur).

### BAĞLAN

SSL/TLS bağlantıları için HTTP `CONNECT` tünellemesini uygular.

### Streamr

TCP tabanlı kapsülleme yoluyla UDP tarzı akış yapmayı etkinleştirir. Karşılık gelen bir Streamr sunucu tüneli ile eşleştirildiğinde medya akışını destekler.

![I2PTunnel Streamr diyagramı](/images/I2PTunnel-streamr.png)

---

## Sunucu Modları

### Standart Sunucu

Yerel bir IP:port ile eşleştirilmiş bir TCP hedefi oluşturur.

### HTTP Sunucusu

Yerel bir web sunucusuyla arayüz oluşturan bir destination (hedef) oluşturur. Sıkıştırmayı (`x-i2p-gzip`), başlık temizlemeyi ve DDoS korumalarını destekler. Artık **kalıcı bağlantı desteğinden** (v2.5.0+) ve **iş parçacığı havuzu optimizasyonundan** (v2.7.0–2.9.0) faydalanır.

### HTTP Çift Yönlü

**Kullanımdan Kaldırılmış** – Hala çalışır ancak önerilmez. Outproxy kullanmadan hem HTTP sunucusu hem de istemci olarak görev yapar. Öncelikle tanı amaçlı geri döngü testleri için kullanılır.

### IRC Sunucusu

IRC servisleri için filtrelenmiş bir hedef oluşturur, istemci hedef anahtarlarını ana bilgisayar adları olarak iletir.

### Streamr Sunucusu

I2P üzerinden UDP tarzı veri akışlarını işlemek için bir Streamr istemci tüneli ile eşleşir.

---

## Yeni Özellikler (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Güvenlik Özellikleri

- Anonimlik için **başlık ayıklama** (Accept, Referer, From, Via)
- Giriş/çıkış proxy'sine bağlı olarak **User-Agent rastgeleleştirme**
- **POST hız sınırlama** ve **Slowloris koruması**
- Akış alt sistemlerinde **bağlantı kısıtlama**
- Tünel katmanında **ağ tıkanıklığı yönetimi**
- Uygulamalar arası sızıntıları önleyen **NetDB izolasyonu**

---

## Teknik Detaylar

- Varsayılan hedef anahtar boyutu: 516 bayt (genişletilmiş LS2 sertifikaları için aşılabilir)  
- Base32 adresleri: `{52–56+ karakter}.b32.i2p`  
- Server tünelleri hem Java I2P hem de i2pd ile uyumlu kalmaya devam ediyor  
- Kullanımdan kaldırılan özellik: yalnızca `httpbidirserver`; 0.9.59 sürümünden beri kaldırılan özellik yok  
- Tüm platformlar için doğru varsayılan portlar ve belge kökleri doğrulandı

---

## Özet

I2PTunnel, I2P ile uygulama entegrasyonunun omurgası olmaya devam ediyor. 0.9.59 ve 2.10.0 sürümleri arasında, kalıcı bağlantı desteği, kuantum sonrası şifreleme ve önemli iş parçacığı iyileştirmeleri kazandı. Çoğu yapılandırma uyumlu kalmaya devam ediyor, ancak geliştiriciler modern aktarım ve güvenlik varsayılanlarına uygunluğu sağlamak için kurulumlarını doğrulamalıdır.
