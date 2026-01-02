---
title: "I2P Yeniden Tohum (Reseed) Sunucusu Oluşturma ve Çalıştırma"
description: "I2P yeniden tohum sunucusu kurulumu ve işletimi için eksiksiz kılavuz - yeni router'ların ağa katılmasına yardımcı olmak için"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed sunucuları, bootstrap sürecinde yeni router'lara başlangıç düğüm grubu sağlayarak I2P ağı için kritik altyapı bileşenleridir. Bu kılavuz, kendi reseed sunucunuzu kurma ve çalıştırma adımlarında size yol gösterecektir.

## I2P Reseed Sunucusu Nedir?

Bir I2P reseed sunucusu, yeni yönlendiricilerin I2P ağına entegrasyonuna şu şekilde yardımcı olur:

- **İlk eş keşfi sağlama**: Yeni yönlendiriciler, bağlanmak için bir başlangıç ağ düğümleri seti alır
- **Bootstrap kurtarma**: Bağlantıları sürdürmekte zorlanan yönlendiricilere yardımcı olma
- **Güvenli dağıtım**: Reseeding işlemi, ağ güvenliğini sağlamak için şifrelenir ve dijital olarak imzalanır

Yeni bir I2P router ilk kez başlatıldığında (veya tüm eş bağlantılarını kaybettiğinde), başlangıç router bilgilerini indirmek için reseed sunucularına bağlanır. Bu, yeni router'ın kendi network database'ini oluşturmaya ve tunnel'lar kurmaya başlamasını sağlar.

## Ön Gereksinimler

Başlamadan önce ihtiyacınız olanlar:

- Root erişimi olan bir Linux sunucusu (Debian/Ubuntu önerilir)
- Sunucunuzu işaret eden bir alan adı
- En az 1GB RAM ve 10GB disk alanı
- Network database'i doldurmak için sunucuda çalışan bir I2P router
- Linux sistem yönetimine dair temel bilgi

## Sunucuyu Hazırlama

### Step 1: Update System and Install Dependencies

İlk olarak, sisteminizi güncelleyin ve gerekli paketleri kurun:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Bu şu bileşenleri kurar: - **golang-go**: Go programlama dili çalışma zamanı - **git**: Sürüm kontrol sistemi - **make**: Derleme otomasyon aracı - **docker.io & docker-compose**: Nginx Proxy Manager'ı çalıştırmak için konteyner platformu

![Gerekli paketlerin kurulumu](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

reseed-tools deposunu klonlayın ve uygulamayı derleyin:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
`reseed-tools` paketi bir reseed sunucusu çalıştırmak için temel işlevselliği sağlar. Şunları yönetir: - Yerel ağ veritabanınızdan router bilgilerini toplama - Router bilgilerini imzalı SU3 dosyalarına paketleme - Bu dosyaları HTTPS üzerinden sunma

![Cloning reseed-tools repository](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Reseed sunucunuzun SSL sertifikasını ve özel anahtarını oluşturun:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Önemli parametreler**: - `--signer`: E-posta adresiniz (`admin@stormycloud.org` yerine kendinizinkini yazın) - `--netdb`: I2P router'ınızın network database yolunu belirtin - `--port`: İç port (8443 önerilir) - `--ip`: Localhost'a bağlan (genel erişim için reverse proxy kullanacağız) - `--trustProxy`: Reverse proxy'den gelen X-Forwarded-For başlıklarına güven

Komut şunları oluşturacaktır: - SU3 dosyalarını imzalamak için bir özel anahtar - Güvenli HTTPS bağlantıları için bir SSL sertifikası

![SSL sertifikası oluşturma](/images/guides/reseed/reseed_03.png)

### Adım 1: Sistemi Güncelleyin ve Bağımlılıkları Kurun

**Kritik**: `/home/i2p/.reseed/` dizininde bulunan oluşturulan anahtarları güvenli bir şekilde yedekleyin:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Bu yedeği güvenli, şifrelenmiş ve erişimi kısıtlanmış bir konumda saklayın. Bu anahtarlar reseed sunucunuzun çalışması için gereklidir ve dikkatli bir şekilde korunmalıdır.

## Configuring the Service

### Adım 2: Reseed Araçlarını Klonlama ve Derleme

Reseed sunucusunu otomatik olarak çalıştırmak için bir systemd servisi oluşturun:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**Unutmayın** `admin@stormycloud.org` adresini kendi e-posta adresinizle değiştirin.

Şimdi servisi etkinleştirin ve başlatın:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Servisin çalıştığını kontrol edin:

```bash
sudo systemctl status reseed
```
![Reseed servis durumunu doğrulama](/images/guides/reseed/reseed_04.png)

### Adım 3: SSL Sertifikası Oluşturma

Optimum performans için, router bilgilerini yenilemek amacıyla reseed servisini periyodik olarak yeniden başlatmak isteyebilirsiniz:

```bash
sudo crontab -e
```
Servisi her 3 saatte bir yeniden başlatmak için bu satırı ekleyin:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

Reseed sunucusu localhost:8443 üzerinde çalışır ve genel HTTPS trafiğini işlemek için bir ters proxy'ye ihtiyaç duyar. Kullanım kolaylığı nedeniyle Nginx Proxy Manager öneriyoruz.

### Adım 4: Anahtarlarınızı Yedekleyin

Docker kullanarak Nginx Proxy Manager'ı dağıtın:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
Bu şunları açar: - **Port 80**: HTTP trafiği - **Port 81**: Yönetim arayüzü - **Port 443**: HTTPS trafiği

### Configure Proxy Manager

1. Yönetim arayüzüne `http://your-server-ip:81` adresinden erişin

2. Varsayılan kimlik bilgileriyle giriş yapın:
   - **E-posta**: admin@example.com
   - **Parola**: changeme

**Önemli**: İlk girişten hemen sonra bu kimlik bilgilerini değiştirin!

![Nginx Proxy Manager girişi](/images/guides/reseed/reseed_05.png)

3. **Proxy Hosts** (Proxy Ana Bilgisayarları) bölümüne gidin ve **Add Proxy Host** (Proxy Ana Bilgisayarı Ekle) seçeneğine tıklayın

![Proxy host ekleme](/images/guides/reseed/reseed_06.png)

4. Proxy host'unu yapılandırın:
   - **Domain Name**: Reseed alan adınız (örn., `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - **Cache Assets**'i etkinleştirin
   - **Block Common Exploits**'i etkinleştirin
   - **Websockets Support**'u etkinleştirin

![Proxy host detaylarını yapılandırma](/images/guides/reseed/reseed_07.png)

5. **SSL** sekmesinde:
   - **Request a new SSL Certificate** (Let's Encrypt) seçeneğini seçin
   - **Force SSL** seçeneğini etkinleştirin
   - **HTTP/2 Support** seçeneğini etkinleştirin
   - Let's Encrypt Hizmet Koşulları'nı kabul edin

![SSL sertifikası yapılandırması](/images/guides/reseed/reseed_08.png)

6. **Kaydet**'e tıklayın

Reseed sunucunuz artık `https://reseed.example.com` adresinden erişilebilir olmalıdır

![Başarılı reseed sunucusu yapılandırması](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Reseed sunucunuz çalışır duruma geldiğinde, resmi reseed sunucu listesine eklenmesi için I2P geliştiricileriyle iletişime geçin.

### Adım 5: Systemd Servisi Oluşturma

**zzz**'ye (I2P baş geliştiricisi) aşağıdaki bilgilerle e-posta gönderin:

- **I2P E-posta**: zzz@mail.i2p
- **Clearnet E-posta**: zzz@i2pmail.org

### Adım 6: İsteğe Bağlı - Periyodik Yeniden Başlatmaları Yapılandırın

E-postanıza şunları ekleyin:

1. **Reseed sunucu URL'si**: Tam HTTPS URL'si (örn., `https://reseed.example.com`)
2. **Genel reseed sertifikası**: `/home/i2p/.reseed/` konumunda bulunur (`.crt` dosyasını ekleyin)
3. **İletişim e-postası**: Sunucu bakım bildirimleri için tercih ettiğiniz iletişim yöntemi
4. **Sunucu konumu**: İsteğe bağlı ancak yararlıdır (ülke/bölge)
5. **Beklenen çalışma süresi**: Sunucuyu sürdürme taahhüdünüz

### Verification

I2P geliştiricileri reseed sunucunuzun şu özelliklere sahip olduğunu doğrulayacaktır: - Düzgün yapılandırılmış ve router bilgisi sunuyor olması - Geçerli SSL sertifikaları kullanıyor olması - Doğru şekilde imzalanmış SU3 dosyaları sağlıyor olması - Erişilebilir ve yanıt veriyor olması

Onaylandıktan sonra, reseed sunucunuz I2P router'larıyla dağıtılan listeye eklenecek ve yeni kullanıcıların ağa katılmasına yardımcı olacak!

## Monitoring and Maintenance

### Nginx Proxy Manager Kurulumu

Reseed servisinizi izleyin:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Proxy Manager'ı Yapılandırma

Sistem kaynaklarını takip edin:

```bash
htop
df -h
```
### Update Reseed Tools

En son iyileştirmeleri almak için reseed-tools'u düzenli olarak güncelleyin:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### İletişim Bilgileri

Nginx Proxy Manager üzerinden Let's Encrypt kullanıyorsanız, sertifikalar otomatik olarak yenilenecektir. Yenilemenin çalıştığını doğrulayın:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Servisi Yapılandırma

### Gerekli Bilgiler

Hataları kontrol etmek için günlükleri inceleyin:

```bash
sudo journalctl -u reseed -n 50
```
Yaygın sorunlar: - I2P router çalışmıyor veya network database boş - 8443 portu zaten kullanımda - `/home/i2p/.reseed/` dizini ile ilgili izin sorunları

### Doğrulama

I2P router'ınızın çalıştığından ve ağ veritabanını doldurduğundan emin olun:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Birçok `.dat` dosyası görmelisiniz. Eğer boşsa, I2P router'ınızın eşleri keşfetmesini bekleyin.

### SSL Certificate Errors

Sertifikalarınızın geçerli olduğunu doğrulayın:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Servis Durumunu Kontrol Edin

Kontrol edin: - DNS kayıtları sunucunuza doğru şekilde yönlendiriliyor - Güvenlik duvarı 80 ve 443 portlarına izin veriyor - Nginx Proxy Manager çalışıyor: `docker ps`

## Security Considerations

- **Özel anahtarlarınızı güvende tutun**: `/home/i2p/.reseed/` içeriğini asla paylaşmayın veya açığa çıkarmayın
- **Düzenli güncellemeler**: Sistem paketlerini, Docker'ı ve reseed-tools'u güncel tutun
- **Günlükleri izleyin**: Şüpheli erişim kalıplarına dikkat edin
- **Hız sınırlama**: Kötüye kullanımı önlemek için hız sınırlama uygulamayı düşünün
- **Güvenlik duvarı kuralları**: Yalnızca gerekli portları açın (80, 443, 81 yönetici için)
- **Yönetici arayüzü**: Nginx Proxy Manager yönetici arayüzünü (port 81) güvenilir IP'lerle sınırlandırın

## Contributing to the Network

Bir reseed sunucusu çalıştırarak, I2P ağı için kritik altyapı sağlıyorsunuz. Daha özel ve merkezi olmayan bir internete katkıda bulunduğunuz için teşekkür ederiz!

Sorularınız veya yardım talepleriniz için I2P topluluğuna ulaşın: - **Forum**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: Çeşitli ağlarda #i2p - **Geliştirme**: [i2pgit.org](https://i2pgit.org)

---


*Rehber aslen [Stormy Cloud](https://www.stormycloud.org) tarafından oluşturulmuştur, I2P dokümantasyonu için uyarlanmıştır.*
