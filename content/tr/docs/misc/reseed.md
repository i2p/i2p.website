---
title: "Reseed Sunucuları (başlangıç için ağ verisi sağlayıcıları)"
description: "Reseed (ilk eş temini) hizmetlerinin işletimi ve alternatif bootstrap (başlangıç) yöntemleri"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Reseed Sunucuları Hakkında

Yeni router'ların I2P ağına katılmak için birkaç eş düğüme ihtiyacı vardır. Reseed ana makineleri (reseed: yeniden tohumlama) bu başlangıç kümesini şifrelenmiş HTTPS indirmeleri üzerinden sağlar. Her reseed paketi ana makine tarafından imzalanır; bu, kimliği doğrulanmamış tarafların kurcalamasını önler. Kurulu router'lar, eş kümeleri güncelliğini yitirdiğinde ara sıra reseed edebilir.

### Ağ Önyükleme Süreci

Bir I2P router ilk kez başlatıldığında veya uzun süre çevrimdışı kaldığında, ağa bağlanabilmesi için RouterInfo (router bilgisi) verilerine ihtiyaç duyar. Router mevcut eşlere sahip olmadığından, bu bilgiyi I2P ağının içinden temin edemez. Reseed mekanizması (başlangıç/önyükleme için tohumlama mekanizması), güvenilir harici HTTPS sunucularından RouterInfo dosyaları sağlayarak bu önyükleme sorununu çözer.

Reseed (yeniden tohumlama) işlemi, tek bir kriptografik olarak imzalanmış paket içinde 75-100 RouterInfo dosyasını teslim eder. Bu, yeni router'ların onları ayrı ve güvenilmeyen ağ bölümlerine izole edebilecek ortadaki adam saldırılarına maruz bırakmadan hızla bağlantılar kurabilmesini sağlar.

### Güncel Ağ Durumu

Ekim 2025 itibarıyla, I2P ağı router sürümü 2.10.0 (API sürümü 0.9.67) ile çalışmaktadır. 0.9.14 sürümünde tanıtılan reseed protocol (ağa ilk kez katılım için gerekli başlangıç verilerinin indirildiği protokol) temel işlevselliği açısından kararlıdır ve değişmemiştir. Ağ, erişilebilirliği ve sansüre direnç sağlamak için küresel olarak dağıtılmış birden çok bağımsız reseed servers bulundurmaktadır.

Hizmet [checki2p](https://checki2p.com/reseed), tüm I2P reseed (yeni kurulumların ağa katılabilmesi için başlangıç ağ verilerini sağlayan mekanizma) sunucularını her 4 saatte bir izler ve reseed altyapısı için gerçek zamanlı durum kontrolleri ile kullanılabilirlik ölçümleri sağlar.

## SU3 Dosya Biçimi Belirtimi

SU3 dosya formatı, kriptografik olarak imzalanmış içerik dağıtımı sağlayarak I2P'nin reseed protokolünün (başlangıç [bootstrap] verilerinin sağlanması) temelini oluşturur. Bu formatı anlamak, reseed sunucuları ve istemcilerinin uygulanması için esastır.

### Dosya Yapısı

SU3 formatı üç ana bileşenden oluşur: başlık (40+ bayt), içerik (değişken uzunlukta) ve imza (uzunluğu başlıkta belirtilir).

#### Başlık Biçimi (Bayt 0-39, en az)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Reseed'e Özgü SU3 Parametreleri

Reseed bundles (I2P'ye ilk bağlantı için gerekli tohum verilerini içeren paketler) için SU3 dosyası aşağıdaki özelliklere sahip olmalıdır:

- **Dosya adı**: Tam olarak `i2pseeds.su3` olmalıdır
- **İçerik Türü** (bayt 27): 0x03 (RESEED)
- **Dosya Türü** (bayt 25): 0x00 (ZIP)
- **İmza Türü** (bayt 8-9): 0x0006 (RSA-4096-SHA512)
- **Sürüm Dizesi**: ASCII biçiminde Unix zaman damgası (epoch'tan beri geçen saniyeler, date +%s biçimi)
- **İmzalayan Kimliği**: X.509 sertifikasının CN'si ile eşleşen e-posta biçeminde tanımlayıcı

#### Ağ Kimliği Sorgu Parametresi

0.9.42 sürümünden beri, router'lar reseed (ilk ağ tohumlaması) isteklerine `?netid=2` ekler. Bu, çapraz ağ bağlantılarını engeller; çünkü test ağları farklı ağ kimlikleri kullanır. Mevcut I2P üretim ağı ağ kimliği 2'yi kullanır.

Örnek istek: `https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP İçerik Yapısı

İçerik bölümü (başlıktan sonra, imzadan önce) aşağıdaki gereksinimleri karşılayan standart bir ZIP arşivi içerir:

- **Sıkıştırma**: Standart ZIP sıkıştırması (DEFLATE)
- **Dosya sayısı**: Tipik olarak 75-100 RouterInfo (router bilgisi) dosyası
- **Dizin yapısı**: Tüm dosyalar en üst düzeyde olmalıdır (alt dizin yok)
- **Dosya adlandırma**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64 alfabesi**: I2P'nin değiştirilmiş base64 alfabesi kullanılmalıdır

I2P base64 alfabesi, dosya sistemi ve URL uyumluluğunu sağlamak için `+` ve `/` yerine `-` ve `~` kullanarak standart base64'ten farklıdır.

### Kriptografik İmza

İmza, 0. bayttan başlayarak içerik bölümünün sonuna kadar dosyanın tamamını kapsar. İmzanın kendisi ise içeriğin ardından eklenir.

#### İmza Algoritması (RSA-4096-SHA512)

1. 0. bayttan içeriğin sonuna kadar olan baytların SHA-512 özetini hesaplayın
2. Özeti "raw" RSA (Java terminolojisinde NONEwithRSA) kullanarak imzalayın
3. Gerekiyorsa 512 bayta ulaşması için imzayı baştaki sıfırlarla doldurun
4. 512 baytlık imzayı dosyanın sonuna ekleyin

#### İmza Doğrulama Süreci

İstemciler şunları yapmalıdır:

1. İmza türünü ve uzunluğunu belirlemek için 0-11 arası baytları okuyun
2. İçerik sınırlarını belirlemek için tüm başlığı okuyun
3. SHA-512 özeti hesaplanırken içeriği akış halinde işleyin
4. İmzayı dosyanın sonundan ayıklayın
5. İmzayı, imzalayanın RSA-4096 açık anahtarını kullanarak doğrulayın
6. İmza doğrulaması başarısız olursa dosyayı reddedin

### Sertifika Güven Modeli

Reseed imzalayıcı anahtarları, RSA-4096 anahtarlarıyla kendinden imzalı X.509 sertifikaları olarak dağıtılır. Bu sertifikalar, I2P router paketlerinde `certificates/reseed/` dizininde yer alır.

Sertifika formatı: - **Anahtar türü**: RSA-4096 - **İmza**: Öz-imzalı - **Subject CN**: SU3 başlığındaki Signer ID ile eşleşmelidir - **Geçerlilik tarihleri**: İstemciler sertifikaların geçerlilik sürelerini uygulamalıdır

## Reseed Sunucusu Çalıştırma

Bir reseed hizmeti (ağa katılım için başlangıç ağ verisini sağlayan hizmet) işletmek, güvenlik, güvenilirlik ve ağ çeşitliliği gereksinimlerine titizlikle dikkat etmeyi gerektirir. Daha fazla bağımsız reseed sunucusu, dayanıklılığı artırır ve saldırganların ya da sansürcülerin yeni router'ların ağa katılımını engellemesini zorlaştırır.

### Teknik Gereksinimler

#### Sunucu Özellikleri

- **İşletim Sistemi**: Unix/Linux (Ubuntu, Debian, FreeBSD test edilmiş ve önerilir)
- **Bağlantı**: Statik IPv4 adresi gereklidir, IPv6 önerilir ancak zorunlu değildir
- **CPU**: En az 2 çekirdek
- **RAM**: En az 2 GB
- **Bant genişliği**: Aylık yaklaşık 15 GB
- **Çalışma süresi**: 7/24 çalışma zorunludur
- **I2P Router**: Sürekli çalışan, iyi entegre edilmiş bir I2P router

#### Yazılım Gereksinimleri

- **Java**: JDK 8 veya daha yenisi (I2P 2.11.0 ile başlayarak Java 17+ gerekli olacaktır)
- **Web Sunucusu**: Ters proxy desteğine sahip nginx veya Apache (X-Forwarded-For başlığı kısıtlamaları nedeniyle Lighttpd artık desteklenmiyor)
- **TLS/SSL**: Geçerli TLS sertifikası (Let's Encrypt, kendinden imzalı veya ticari Sertifika Otoritesi (CA))
- **DDoS Koruması**: fail2ban veya eşdeğeri (zorunlu, isteğe bağlı değil)
- **Reseed Tools** (I2P ağına ilk katılım için başlangıç verilerini sağlayan araçlar): https://i2pgit.org/idk/reseed-tools adresindeki resmi reseed-tools

### Güvenlik Gereksinimleri

#### HTTPS/TLS Yapılandırması

- **Protokol**: Yalnızca HTTPS, HTTP'ye geri dönüş (fallback) yok
- **TLS Sürümü**: En az TLS 1.2
- **Şifre süitleri (cipher suites)**: Java 8+ ile uyumlu güçlü şifreleme algoritmalarını desteklemelidir
- **Sertifika CN/SAN**: Sunulan URL'nin ana makine adıyla eşleşmelidir
- **Sertifika Türü**: Geliştirme ekibiyle iletişime geçilirse self-signed (kendinden imzalı) olabilir veya tanınmış bir CA (Sertifika Otoritesi) tarafından verilebilir

#### Sertifika Yönetimi

SU3 imzalama sertifikaları ve TLS sertifikaları farklı amaçlara hizmet eder:

- **TLS Sertifikası** (`certificates/ssl/`): HTTPS taşımayı güvence altına alır
- **SU3 İmzalama Sertifikası** (`certificates/reseed/`): reseed paketlerini (ağa ilk katılım paketleri) imzalar

Her iki sertifika da router paketlerine dahil edilmek üzere reseed koordinatörüne (zzz@mail.i2p) sağlanmalıdır.

#### DDoS ve Scraping (veri kazıma) Koruması

Reseed sunucuları, hatalı uygulamalar, botnetler ve ağ veritabanını kazımaya çalışan kötü niyetli aktörlerden gelen periyodik saldırılarla karşı karşıya kalır. Koruma önlemleri şunları içerir:

- **fail2ban**: Hız sınırlama ve saldırı hafifletme için gereklidir
- **Paket Çeşitliliği**: Farklı istekte bulunanlara farklı RouterInfo (router bilgi kaydı) kümeleri teslim edin
- **Paket Tutarlılığı**: Aynı IP'den yapılandırılabilir bir zaman penceresi içinde yinelenen isteklere aynı paketi teslim edin
- **IP Günlükleme Kısıtlamaları**: Günlükleri veya IP adreslerini ifşa etmeyin (gizlilik politikası gereği)

### Uygulama Yöntemleri

#### Yöntem 1: Resmi reseed-tools (Önerilir)

I2P projesi tarafından sürdürülen kanonik uygulama. Depo: https://i2pgit.org/idk/reseed-tools

**Kurulum**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
İlk çalıştırmada, araç şunları oluşturur: - `your-email@mail.i2p.crt` (SU3 imzalama sertifikası) - `your-email@mail.i2p.pem` (SU3 imzalama özel anahtarı) - `your-email@mail.i2p.crl` (Sertifika iptal listesi) - TLS sertifikası ve anahtar dosyaları

**Özellikler**: - Otomatik SU3 paket üretimi (350 varyant, her birinde 77 RouterInfo (yöneltici bilgisi)) - Yerleşik HTTPS sunucusu - Önbelleğin cron aracılığıyla her 9 saatte bir yeniden oluşturulması - `--trustProxy` bayrağıyla X-Forwarded-For üstbilgisi desteği - Ters proxy yapılandırmalarıyla uyumlu

**Üretim Ortamına Dağıtım**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Yöntem 2: Python Uygulaması (pyseeder)

PurpleI2P projesi tarafından geliştirilen alternatif bir gerçekleme: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Yöntem 3: Docker ile Dağıtım

Konteynerleştirilmiş ortamlar için, Docker'a hazır birkaç gerçekleştirim mevcuttur:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Tor onion service (Tor onion servisi) ve IPFS desteği ekler

### Ters Proxy Yapılandırması

#### nginx Yapılandırması

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Apache Yapılandırması

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Kayıt ve Koordinasyon

reseed server'ınızın (ağa ilk katılım için router listesini sağlayan sunucu) resmi I2P paketine dahil edilmesi için:

1. Kurulumu ve testleri tamamlayın
2. Her iki sertifikayı (SU3 signing ve TLS) reseed (ağ başlangıç bilgisi dağıtımı) koordinatörüne gönderin
3. İletişim: zzz@mail.i2p veya zzz@i2pmail.org
4. Diğer operatörlerle koordinasyon için IRC2P'deki #i2p-dev kanalına katılın

### Operasyonel En İyi Uygulamalar

#### İzleme ve Günlükleme

- İstatistikler için Apache/nginx birleşik günlük biçimini etkinleştirin
- Günlük döndürmeyi uygulayın (günlükler hızla büyür)
- Paket oluşturma başarısını ve yeniden oluşturma sürelerini izleyin
- Bant genişliği kullanımını ve istek kalıplarını izleyin
- IP adreslerini veya ayrıntılı erişim günlüklerini asla kamuya açıklamayın

#### Bakım Takvimi

- **Her 9 saatte bir**: SU3 paket önbelleğini yeniden oluştur (cron ile otomatikleştirildi)
- **Haftalık**: Günlükleri saldırı kalıpları açısından gözden geçir
- **Aylık**: I2P router'ı ve reseed-tools'u güncelle
- **Gerektikçe**: TLS sertifikalarını yenile (Let's Encrypt ile otomatikleştir)

#### Port Seçimi

- Varsayılan: 8443 (önerilir)
- Alternatif: 1024-49151 arasındaki herhangi bir port
- Port 443: root ayrıcalıkları veya port yönlendirmesi gerektirir (iptables redirect önerilir)

Örnek port yönlendirme:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Alternatif Yeniden Tohumlama Yöntemleri

Diğer önyükleme seçenekleri, kısıtlayıcı ağların arkasındaki kullanıcılara yardımcı olur:

### Dosya Tabanlı Reseed (ağın başlangıç verilerinin dosyadan alınması)

0.9.16 sürümünde tanıtılan dosya tabanlı reseed (yeniden tohumlama), kullanıcıların RouterInfo (yönlendirici bilgisi) paketlerini elle yüklemesine olanak tanır. Bu yöntem, HTTPS reseed sunucularının engellendiği sansürlü bölgelerdeki kullanıcılar için özellikle yararlıdır.

**Süreç**: 1. Güvenilir bir kişi, router'ını kullanarak bir SU3 paketi oluşturur 2. Paket e-posta, USB sürücü veya başka bir bant dışı kanal üzerinden aktarılır 3. Kullanıcı `i2pseeds.su3` dosyasını I2P yapılandırma dizinine yerleştirir 4. Router yeniden başlatıldığında paketi otomatik olarak algılar ve işler

**Dokümantasyon**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Kullanım Senaryoları**: - reseed sunucularını engelleyen ulusal güvenlik duvarlarının arkasındaki kullanıcılar - manuel bootstrap (el ile ilk başlatma) gerektiren izole ağlar - test ve geliştirme ortamları

### Cloudflare vekil sunucusu üzerinden Reseeding (başlangıç verilerinin yeniden alınması)

Reseed (ağa ilk katılım için başlangıç verilerinin alınması) trafiğini Cloudflare'in CDN'i aracılığıyla yönlendirmek, yüksek düzeyde sansür uygulanan bölgelerdeki operatörler için çeşitli avantajlar sağlar.

**Faydalar**: - Kaynak sunucunun IP adresi istemcilerden gizlenir - Cloudflare'ın altyapısı aracılığıyla DDoS koruması - Edge caching (uç önbellekleme) aracılığıyla coğrafi yük dağıtımı - Küresel istemciler için iyileştirilmiş performans

**Uygulama Gereksinimleri**: - reseed-tools içinde `--trustProxy` bayrağı etkin - DNS kaydı için Cloudflare proxy etkin - X-Forwarded-For üstbilgisinin uygun şekilde işlenmesi

**Önemli Hususlar**: - Cloudflare bağlantı noktası (port) kısıtlamaları geçerlidir (desteklenen bağlantı noktaları kullanılmalıdır) - Aynı istemci bundle (demet) tutarlılığı X-Forwarded-For desteği gerektirir - SSL/TLS yapılandırması Cloudflare tarafından yönetilir

**Dokümantasyon**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Sansüre Dayanıklı Stratejiler

Nguyen Phong Hoang’ın (USENIX FOCI 2019) çalışması, sansürlü ağlar için ek önyükleme yöntemlerini tanımlamaktadır:

#### Bulut Depolama Sağlayıcıları

- **Box, Dropbox, Google Drive, OneDrive**: SU3 (I2P imzalı güncelleme dosyası formatı) dosyalarını herkese açık bağlantılarda barındırın
- **Avantaj**: Meşru hizmetleri aksatmadan engellemesi zordur
- **Sınırlama**: Kullanıcılara URL'lerin elle dağıtılmasını gerektirir

#### IPFS (InterPlanetary File System - Gezegenlerarası Dosya Sistemi) Dağıtımı

- Reseed paketlerini InterPlanetary File System (IPFS, merkeziyetsiz dosya sistemi) üzerinde barındırın
- İçerik-adresli depolama, kurcalamayı önler
- Kaldırma girişimlerine karşı dayanıklıdır

#### Tor Onion Hizmetleri

- .onion adresleri üzerinden erişilebilen Reseed servers (ağa ilk katılım için başlangıç sunucuları)
- IP tabanlı engellemeye dayanıklı
- Kullanıcının sisteminde Tor istemcisi gerektirir

**Araştırma Dokümantasyonu**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### I2P'nin Engellendiği Bilinen Ülkeler

2025 itibarıyla, aşağıdaki ülkelerde I2P reseed servers (ağa ilk bağlantıyı sağlayan sunucular) erişiminin engellendiği doğrulanmıştır: - Çin - İran - Umman - Katar - Kuveyt

Bu bölgelerdeki kullanıcılar, alternatif bootstrap yöntemleri (başlangıç yöntemleri) veya sansüre dirençli reseeding stratejileri (yeniden tohumlama stratejileri) kullanmalıdır.

## Uygulayıcılar için Protokol Ayrıntıları

### Reseed (netDb'nin ilk tohumlanması) İstek Şartnamesi

#### İstemci Davranışı

1. **Sunucu Seçimi**: Router sabit kodlanmış reseed URL'lerinin (başlangıç URL'leri) bir listesini tutar
2. **Rastgele Seçim**: İstemci mevcut listeden rastgele bir sunucu seçer
3. **İstek Biçimi**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Yaygın tarayıcıları taklit etmelidir (örn. "Wget/1.11.4")
5. **Yeniden Deneme Mantığı**: SU3 isteği başarısız olursa, indeks sayfasını ayrıştırmaya başvurun
6. **Sertifika Doğrulama**: TLS sertifikasını sistemin güvenilir sertifika deposuna karşı doğrulayın
7. **SU3 İmza Doğrulama**: İmzayı bilinen reseed sertifikalarına karşı doğrulayın

#### Sunucu Davranışı

1. **Demet Seçimi**: netDb içinden RouterInfos (yönlendirici bilgileri kayıtları) psödorastgele bir alt kümesini seçin
2. **İstemci İzleme**: İstekleri kaynak IP'ye göre belirleyin (X-Forwarded-For'u dikkate alarak)
3. **Demet Tutarlılığı**: Zaman penceresi içinde tekrarlanan isteklere aynı demeti döndürün (genellikle 8-12 saat)
4. **Demet Çeşitliliği**: Ağ çeşitliliği için farklı istemcilere farklı demetler döndürün
5. **Content-Type**: `application/octet-stream` veya `application/x-i2p-reseed`

### RouterInfo Dosya Biçimi

reseed paketindeki her `.dat` dosyası bir RouterInfo (router bilgisi) yapısı içerir:

**Dosya Adlandırma**: `routerInfo-{base64-hash}.dat` - Özet 44 karakterdir ve I2P base64 alfabesini kullanır - Örnek: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Dosya İçeriği**: - RouterIdentity (router hash, şifreleme anahtarı, imzalama anahtarı) - Yayın zaman damgası - Router adresleri (IP, port, taşıma türü) - Router yetenekleri ve seçenekleri - Yukarıdaki tüm verileri kapsayan imza

### Ağ Çeşitliliği Gereksinimleri

Ağın merkezileşmesini önlemek ve Sybil saldırılarının tespitini sağlamak için:

- **Tam NetDb dökümleri yok**: Tüm RouterInfos (RouterInfo nesneleri; router bilgi kayıtları) öğelerini tek bir istemciye asla sunmayın
- **Rastgele örnekleme**: Her paket, mevcut eşlerin farklı bir alt kümesini içerir
- **Minimum paket boyutu**: 75 RouterInfos (orijinal 50'den artırıldı)
- **Maksimum paket boyutu**: 100 RouterInfos
- **Güncellik**: RouterInfos güncel olmalıdır (oluşturulmasından itibaren 24 saat içinde)

### IPv6 ile ilgili hususlar

**Mevcut Durum** (2025): - Bazı reseed sunucuları IPv6 üzerinden yanıt vermiyor - İstemciler güvenilirlik için IPv4'ü tercih etmeli veya zorlamalı - Yeni kurulumlar için IPv6 desteği önerilir ancak kritik değildir

**Uygulama Notu**: Dual-stack sunucuları yapılandırırken, hem IPv4 hem de IPv6 dinleme adreslerinin düzgün çalıştığından emin olun, ya da IPv6 düzgün şekilde desteklenemiyorsa IPv6'yı devre dışı bırakın.

## Güvenlik Hususları

### Tehdit Modeli

Reseed protokolü aşağıdakilere karşı koruma sağlar:

1. **Aradaki adam saldırıları**: RSA-4096 imzaları bundle (paket) kurcalanmasını önler
2. **Ağ bölünmesi**: Birden fazla bağımsız reseed sunucusu (ağa ilk katılım için) tekil bir kontrol noktasının oluşmasını engeller
3. **Sybil saldırıları**: Bundle çeşitliliği, saldırganın kullanıcıları izole etme yeteneğini sınırlar
4. **Sansür**: Birden çok sunucu ve alternatif yöntemler yedeklilik sağlar

Reseed protokolü şunlara karşı koruma sağlamaz:

1. **Ele geçirilmiş reseed (I2P ağına ilk katılım için önyükleme işlemi) sunucuları**: Saldırgan reseed sertifikalarının özel anahtarlarını kontrol ediyorsa
2. **Ağın tamamen engellenmesi**: Bir bölgede tüm reseed yöntemleri engellenmişse
3. **Uzun vadeli izleme**: Reseed istekleri, I2P'ye katılmaya çalışan IP adresini ortaya çıkarır

### Sertifika Yönetimi

**Özel Anahtar Güvenliği**: - Kullanılmadıklarında SU3 imzalama anahtarlarını çevrimdışı olarak saklayın - Anahtar şifrelemesi için güçlü parolalar kullanın - Anahtarların ve sertifikaların güvenli yedeklerini muhafaza edin - Kritik öneme sahip dağıtımlar için donanım güvenlik modüllerini (HSM'ler) değerlendirin

**Sertifika İptali**: - Haber akışı aracılığıyla dağıtılan Sertifika İptal Listeleri (CRL'ler) - Kompromize olmuş sertifikalar koordinatör tarafından iptal edilebilir - Routers yazılım güncellemeleriyle CRL'leri otomatik olarak günceller

### Saldırıların Azaltılması

**DDoS Koruması**: - aşırı istekler için fail2ban kuralları - web sunucusu düzeyinde hız sınırlaması - IP adresi başına bağlantı sınırları - ek bir katman için Cloudflare veya benzeri bir CDN (İçerik Dağıtım Ağı)

**Veri kazıma önleme**: - İstek yapan IP başına farklı paketler - IP başına zaman bazlı paket önbellekleme - Veri kazıma girişimlerini gösteren kalıpların günlüklenmesi - Tespit edilen saldırılar konusunda diğer operatörlerle koordinasyon

## Test ve Geçerleme

### Reseed (önyükleme verileri) sunucunuzun test edilmesi

#### Yöntem 1: Sıfırdan Router Kurulumu

1. I2P'yi temiz bir sistem üzerine kurun
2. reseed (ağa ilk eş bilgilerini alma) URL'nizi yapılandırmaya ekleyin
3. Diğer reseed URL'lerini kaldırın veya devre dışı bırakın
4. router'ı başlatın ve başarılı reseed için günlükleri izleyin
5. 5-10 dakika içinde ağa bağlandığınızı doğrulayın

Beklenen günlük çıktısı:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Yöntem 2: Manuel SU3 (imzalı güncelleme dosyası formatı) Doğrulaması

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Yöntem 3: checki2p İzleme

https://checki2p.com/reseed adresindeki hizmet, kayıtlı tüm I2P reseed sunucularında her 4 saatte bir otomatik kontroller gerçekleştirir. Bu şunları sağlar:

- Kullanılabilirlik izleme
- Yanıt süresi metrikleri
- TLS sertifikası doğrulaması
- SU3 imza doğrulaması
- Geçmiş çalışma süresi verileri

reseed'iniz (başlangıç sunucusu) I2P projesine kaydedildiğinde, 24 saat içinde checki2p'de otomatik olarak görünecektir.

### Yaygın Sorunların Giderilmesi

**Sorun**: İlk çalıştırmada "imzalama anahtarı okunamıyor" - **Çözüm**: Bu beklenen bir durumdur. Yeni anahtarlar oluşturmak için 'y' yanıtını verin.

**Sorun**: Router imzayı doğrulayamıyor - **Neden**: Sertifika router'ın güven deposunda değil - **Çözüm**: Sertifikayı `~/.i2p/certificates/reseed/` dizinine yerleştirin

**Sorun**: Aynı paket farklı istemcilere sunuluyor - **Neden**: X-Forwarded-For başlığı doğru şekilde iletilmiyor - **Çözüm**: `--trustProxy` seçeneğini etkinleştirin ve ters proxy başlıklarını yapılandırın

**Sorun**: "Connection refused" hataları - **Neden**: Bağlantı noktası İnternet'ten erişilebilir değil - **Çözüm**: Güvenlik duvarı kurallarını kontrol edin, bağlantı noktası yönlendirmesini doğrulayın

**Sorun**: bundle yeniden oluşturma sırasında yüksek CPU kullanımı - **Neden**: 350'den fazla SU3 (I2P imzalı güncelleme dosyası biçimi) varyasyonu oluşturulurken normal davranıştır - **Çözüm**: Yeterli CPU kaynaklarını sağlayın, yeniden oluşturma sıklığını azaltmayı düşünün

## Referans Bilgileri

### Resmi Dokümantasyon

- **Reseed (yeniden tohumlama) Katkıda Bulunanlar Kılavuzu**: /guides/creating-and-running-an-i2p-reseed-server/
- **Reseed Politika Gereksinimleri**: /guides/reseed-policy/
- **SU3 Teknik Şartnamesi**: /docs/specs/updates/
- **Reseed Araçları Deposu**: https://i2pgit.org/idk/reseed-tools
- **Reseed Araçları Belgeleri**: https://eyedeekay.github.io/reseed-tools/

### Alternatif Gerçeklemeler

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder (ilk kurulum için netDb verilerini sağlayan hizmet)**: https://github.com/torbjo/i2p-reseeder

### Topluluk Kaynakları

- **I2P Forumu**: https://i2pforum.net/
- **Gitea Deposu**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev IRC2P üzerinde
- **Durum İzleme**: https://checki2p.com/reseed

### Sürüm Geçmişi

- **0.9.14** (2014): SU3 reseed formatı tanıtıldı
- **0.9.16** (2014): Dosya tabanlı reseeding eklendi
- **0.9.42** (2019): Network ID sorgu parametresi zorunluluğu
- **2.0.0** (2022): SSU2 taşıma protokolü tanıtıldı
- **2.4.0** (2024): NetDB izolasyonu ve güvenlik iyileştirmeleri
- **2.6.0** (2024): I2P-over-Tor bağlantıları engellendi
- **2.10.0** (2025): Güncel kararlı sürüm (Eylül 2025 itibarıyla)

### İmza Türü Referansı

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Reseed (yeniden tohumlama) Standardı**: Type 6 (RSA-SHA512-4096) reseed paketleri için gereklidir.

## Takdir

Ağın erişilebilir ve dayanıklı kalmasını sağladıkları için tüm reseed operator (reseed hizmeti işletmecisi)lere teşekkürler. Aşağıdaki katkıda bulunanlar ve projelere özel teşekkürler:

- **zzz**: Uzun süredir I2P geliştiricisi ve reseed (I2P ağının ilk önyüklemesini sağlayan sunucular/işlem) koordinatörü
- **idk**: reseed-tools'un mevcut bakımcısı ve sürüm yöneticisi
- **Nguyen Phong Hoang**: Sansüre dirençli reseeding stratejileri üzerine araştırma
- **PurpleI2P Team**: Alternatif I2P gerçeklemeleri ve araçları
- **checki2p**: reseed altyapısı için otomatik izleme hizmeti

I2P ağının merkeziyetsiz reseed altyapısı (ağa ilk katılım için gerekli başlangıç bilgilerini sağlayan mekanizma), dünya çapında onlarca operatörün ortak çabasını temsil eder ve yerel sansür ya da teknik engeller ne olursa olsun yeni kullanıcıların ağa katılmak için her zaman bir yol bulabilmesini sağlar.
