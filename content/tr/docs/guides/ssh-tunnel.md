---
title: "I2P'ye Uzaktan Erişmek için SSH Tüneli Oluşturma"
description: "Windows, Linux ve Mac üzerinde uzak I2P yönlendiricinize erişmek için güvenli SSH tünelleri oluşturmayı öğrenin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Bir SSH tüneli, uzak I2P router'ınızın konsoluna veya diğer hizmetlerine erişmek için güvenli, şifreli bir bağlantı sağlar. Bu kılavuz, Windows, Linux ve Mac sistemlerinde SSH tünelleri oluşturmayı gösterir.

## SSH Tüneli Nedir?

SSH tüneli, veri ve bilgilerin şifrelenmiş bir SSH bağlantısı üzerinden güvenli bir şekilde yönlendirilmesi yöntemidir. Bunu internet üzerinden korumalı bir "boru hattı" oluşturmak olarak düşünün - verileriniz bu şifrelenmiş tünel içinden geçerken, yol boyunca hiç kimse verileri engelleyemez veya okuyamaz.

SSH tünellemesi özellikle şu durumlarda kullanışlıdır:

- **Uzak I2P router'lara erişim**: Uzak bir sunucuda çalışan I2P konsolunuza bağlanın
- **Güvenli bağlantılar**: Tüm trafik uçtan uca şifrelenir
- **Kısıtlamaları aşma**: Uzak sistemlerdeki servislere yerel hizmetlermiş gibi erişin
- **Port yönlendirme**: Yerel bir portu uzak bir servise eşleyin

I2P bağlamında, uzak bir sunucudaki I2P router konsolunuza (genellikle 7657 portunda) erişmek için bir SSH tüneli kullanarak bunu bilgisayarınızdaki yerel bir porta yönlendirebilirsiniz.

## Ön Koşullar

SSH tüneli oluşturmadan önce ihtiyacınız olanlar:

- **SSH istemcisi**:
  - Windows: [PuTTY](https://www.putty.org/) (ücretsiz indirme)
  - Linux/Mac: Yerleşik SSH istemcisi (Terminal üzerinden)
- **Uzak sunucu erişimi**:
  - Uzak sunucu için kullanıcı adı
  - Uzak sunucunun IP adresi veya hostname'i
  - SSH parolası veya anahtar tabanlı kimlik doğrulama
- **Kullanılabilir yerel port**: 1-65535 arasında kullanılmayan bir port seçin (I2P için yaygın olarak 7657 kullanılır)

## Tunnel Komutunu Anlamak

SSH tünel komutu bu kalıbı takip eder:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Parametreler açıklaması**: - **local_port**: Yerel makinenizdeki port (örn. 7657) - **destination_ip**: Genellikle `127.0.0.1` (uzak sunucuda localhost) - **destination_port**: Uzak sunucudaki servisin portu (örn. I2P için 7657) - **username**: Uzak sunucudaki kullanıcı adınız - **remote_server**: Uzak sunucunun IP adresi veya host adı

**Örnek**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Bu, şu şekilde bir tünel oluşturur: - Makinenizdeki yerel port 7657, uzak sunucunun localhost'unda (I2P'nin çalıştığı yerde) port 7657'ye yönlendirilir - `i2p` kullanıcısı olarak `20.228.143.58` sunucusuna bağlanılır

## Windows'ta SSH Tünelleri Oluşturma

Windows kullanıcıları, ücretsiz bir SSH istemcisi olan PuTTY'yi kullanarak SSH tünelleri oluşturabilir.

### Step 1: Download and Install PuTTY

PuTTY'yi [putty.org](https://www.putty.org/) adresinden indirin ve Windows sisteminize kurun.

### Step 2: Configure the SSH Connection

PuTTY'yi açın ve bağlantınızı yapılandırın:

1. **Oturum** kategorisinde:
   - Uzak sunucunuzun IP adresini veya ana bilgisayar adını **Host Name** alanına girin
   - **Port**'un 22'ye (varsayılan SSH portu) ayarlı olduğundan emin olun
   - Bağlantı türü **SSH** olmalıdır

![PuTTY oturum yapılandırması](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Sol kenar çubuğunda **Connection → SSH → Tunnels** bölümüne gidin:

1. **Kaynak bağlantı noktası**: Kullanmak istediğiniz yerel bağlantı noktasını girin (örn., `7657`)
2. **Hedef**: `127.0.0.1:7657` girin (uzak sunucudaki localhost:port)
3. Tüneli eklemek için **Ekle**'ye tıklayın
4. Tünel "Yönlendirilen bağlantı noktaları" listesinde görünmelidir

![PuTTY tünel yapılandırması](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Bağlantıyı başlatmak için **Open** düğmesine tıklayın
2. İlk kez bağlanıyorsanız, bir güvenlik uyarısı göreceksiniz - sunucuya güvenmek için **Yes** düğmesine tıklayın
3. İstendiğinde kullanıcı adınızı girin
4. İstendiğinde parolanızı girin

![PuTTY bağlantısı kuruldu](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Bağlandıktan sonra, bir tarayıcı açıp `http://127.0.0.1:7657` adresine giderek uzak I2P konsolunuza erişebilirsiniz

### Adım 1: PuTTY'yi İndirin ve Kurun

Her seferinde yeniden yapılandırmaktan kaçınmak için:

1. **Session** kategorisine geri dönün
2. **Saved Sessions** alanına bir isim girin (örn. "I2P Tunnel")
3. **Save** düğmesine tıklayın
4. Bir sonraki seferde, bu oturumu yükleyin ve **Open** düğmesine tıklayın

## Creating SSH Tunnels on Linux

Linux sistemleri terminale yerleşik SSH'ye sahiptir, bu da tünel oluşturmayı hızlı ve kolay hale getirir.

### Adım 2: SSH Bağlantısını Yapılandırın

Bir terminal açın ve SSH tüneli komutunu çalıştırın:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Değiştir**: - `7657` (ilk geçtiği yer): İstediğiniz yerel port - `127.0.0.1:7657`: Uzak sunucudaki hedef adres ve port - `i2p`: Uzak sunucudaki kullanıcı adınız - `20.228.143.58`: Uzak sunucunuzun IP adresi

![Linux SSH tüneli oluşturma](/images/guides/ssh-tunnel/sshtunnel_4.webp)

İstendiğinde şifrenizi girin. Bağlantı kurulduktan sonra tünel aktif hale gelir.

Tarayıcınızda `http://127.0.0.1:7657` adresinden uzak I2P konsolunuza erişin.

### Adım 3: Tüneli Yapılandırın

Tünel, SSH oturumu çalıştığı sürece aktif kalır. Arka planda çalışır durumda tutmak için:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Ek bayraklar**: - `-f`: SSH'yi arka planda çalıştırır - `-N`: Uzak komutları çalıştırma (yalnızca tünel)

Arka planda çalışan bir tüneli kapatmak için SSH sürecini bulun ve sonlandırın:

```bash
ps aux | grep ssh
kill [process_id]
```
### Adım 4: Bağlan

Daha iyi güvenlik ve kolaylık için SSH anahtar kimlik doğrulaması kullanın:

1. Bir SSH anahtar çifti oluşturun (eğer yoksa):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Genel anahtarınızı uzak sunucuya kopyalayın:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Artık şifre olmadan bağlanabilirsiniz:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Mac sistemleri Linux ile aynı SSH istemcisini kullanır, bu nedenle işlem aynıdır.

### İsteğe Bağlı: Oturumunuzu Kaydedin

Terminal'i açın (Uygulamalar → Yardımcı Programlar → Terminal) ve şunu çalıştırın:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Değiştirin**: - `7657` (ilk geçiş): İstediğiniz yerel port - `127.0.0.1:7657`: Uzak sunucudaki hedef adres ve port - `i2p`: Uzak sunucudaki kullanıcı adınız - `20.228.143.58`: Uzak sunucunuzun IP adresi

![Mac SSH tunnel oluşturma](/images/guides/ssh-tunnel/sshtunnel_5.webp)

İstendiğinde parolanızı girin. Bağlandıktan sonra, uzak I2P konsolunuza `http://127.0.0.1:7657` adresinden erişin

### Background Tunnels on Mac

Linux'ta olduğu gibi, tüneli arka planda çalıştırabilirsiniz:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Terminali Kullanma

Mac SSH anahtar kurulumu Linux ile aynıdır:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Tüneli Aktif Tutma

En yaygın kullanım senaryosu - uzaktaki I2P router konsolunuza erişim:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Ardından tarayıcınızda `http://127.0.0.1:7657` adresini açın.

### SSH Anahtarlarını Kullanma (Önerilen)

Aynı anda birden fazla portu yönlendirin:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Bu, hem 7657 portunu (I2P konsolu) hem de 7658 portunu (başka bir servis) yönlendirir.

### Custom Local Port

7657 portu zaten kullanımdaysa farklı bir yerel port kullanın:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
I2P konsoluna `http://127.0.0.1:8080` adresinden erişin.

## Troubleshooting

### Terminali Kullanma

**Hata**: "bind: Address already in use"

**Çözüm**: Farklı bir yerel port seçin veya o portu kullanan işlemi sonlandırın:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Mac'te Arka Plan Tünelleri

**Hata**: "Bağlantı reddedildi" veya "channel 2: open failed"

**Olası nedenler**: - Uzak servis çalışmıyor (uzak sunucuda I2P router'ın çalıştığını kontrol edin) - Güvenlik duvarı bağlantıyı engelliyor - Yanlış hedef portu

**Çözüm**: Uzak sunucuda I2P router'ın çalıştığını doğrulayın:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Mac'te SSH Anahtar Kurulumu

**Hata**: "İzin reddedildi" veya "Kimlik doğrulama başarısız oldu"

**Olası nedenler**: - Yanlış kullanıcı adı veya şifre - SSH anahtarı düzgün yapılandırılmamış - Uzak sunucuda SSH erişimi devre dışı bırakılmış

**Çözüm**: Kimlik bilgilerini doğrulayın ve uzak sunucuda SSH erişiminin etkin olduğundan emin olun.

### Tunnel Drops Connection

**Hata**: Belli bir hareketsizlik süresinden sonra bağlantı kopuyor

**Çözüm**: SSH yapılandırmanıza (`~/.ssh/config`) keep-alive ayarlarını ekleyin:

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **SSH anahtarları kullanın**: Parolalardan daha güvenli, ele geçirilmesi daha zor
- **Parola kimlik doğrulamasını devre dışı bırakın**: SSH anahtarları kurulduktan sonra, sunucuda parola girişini devre dışı bırakın
- **Güçlü parolalar kullanın**: Parola kimlik doğrulaması kullanıyorsanız, güçlü ve benzersiz bir parola kullanın
- **SSH erişimini sınırlayın**: Güvenilir IP adreslerine SSH erişimini sınırlamak için güvenlik duvarı kurallarını yapılandırın
- **SSH'ı güncel tutun**: SSH istemci ve sunucu yazılımınızı düzenli olarak güncelleyin
- **Günlükleri izleyin**: Şüpheli etkinlik için sunucudaki SSH günlüklerini kontrol edin
- **Standart olmayan SSH portları kullanın**: Otomatik saldırıları azaltmak için varsayılan SSH portunu (22) değiştirin

## Linux'ta SSH Tünelleri Oluşturma

### I2P Konsoluna Erişim

Tünelleri otomatik olarak kurmak için bir betik oluşturun:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Çalıştırılabilir yapın:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Çoklu Tüneller

Otomatik tünel oluşturma için bir systemd servisi oluşturun:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Ekle:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
Etkinleştir ve başlat:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Özel Yerel Port

Dinamik yönlendirme için bir SOCKS proxy oluşturun:

```bash
ssh -D 8080 user@remote-server
```
Tarayıcınızı `127.0.0.1:8080` adresini SOCKS5 proxy olarak kullanacak şekilde yapılandırın.

### Reverse Tunneling

Uzak sunucunun yerel makinenizdeki servislere erişmesine izin verin:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Port Zaten Kullanımda

Ara sunucu üzerinden tünel:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH tünelleme, uzak I2P router'lara ve diğer servislere güvenli bir şekilde erişmek için güçlü bir araçtır. Windows, Linux veya Mac kullanıyor olun, süreç basittir ve bağlantılarınız için güçlü şifreleme sağlar.

Ek yardım veya sorularınız için I2P topluluğunu ziyaret edin: - **Forum**: [i2pforum.net](https://i2pforum.net) - **IRC**: çeşitli ağlarda #i2p - **Belgeler**: [I2P Docs](/docs/)

---


*Rehber orijinal olarak [Stormy Cloud](https://www.stormycloud.org) tarafından oluşturulmuş, I2P dokümantasyonu için uyarlanmıştır.*
