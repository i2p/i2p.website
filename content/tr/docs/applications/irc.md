---
title: "IRC I2P Üzerinden"
description: "I2P IRC ağları, istemcileri, tünelleri ve sunucu kurulumu için eksiksiz kılavuz (2025 güncellemesi)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

**Temel noktalar**

- I2P, IRC trafiği için tünelleri aracılığıyla **uçtan uca şifreleme** sağlar. Clearnet'e outproxy yapmıyorsanız IRC istemcilerinde **SSL/TLS'yi devre dışı bırakın**.
- Önceden yapılandırılmış **Irc2P** istemci tüneli varsayılan olarak **127.0.0.1:6668** adresini dinler. IRC istemcinizi bu adres ve porta bağlayın.
- "Router tarafından sağlanan TLS" terimini kullanmayın. "I2P'nin yerel şifrelemesi" veya "uçtan uca şifreleme" kullanın.

## Hızlı başlangıç (Java I2P)

1. **Hidden Services Manager**'ı `http://127.0.0.1:7657/i2ptunnel/` adresinden açın ve **Irc2P** tünelinin **çalıştığından** emin olun.
2. IRC istemcinizde **sunucu** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **kapalı** olarak ayarlayın.
3. Bağlanın ve `#i2p`, `#i2p-dev`, `#i2p-help` gibi kanallara katılın.

**i2pd** kullanıcıları için (C++ router), `tunnels.conf` dosyasında bir istemci tüneli oluşturun (aşağıdaki örneklere bakın).

## Ağlar ve sunucular

### IRC2P (main community network)

- Federe sunucular: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- `127.0.0.1:6668` adresindeki **Irc2P** tüneli bunlardan birine otomatik olarak bağlanır.
- Tipik kanallar: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Sunucular: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Birincil diller: Rusça ve İngilizce. Bazı sunucularda web arayüzleri mevcuttur.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — güçlü SOCKS desteği; betik yazmayı kolaylaştırır.
- **Pidgin (masaüstü)** — hala bakımı yapılıyor; Windows/Linux için iyi çalışır.
- **Thunderbird Chat (masaüstü)** — ESR 128+ sürümlerinde destekleniyor.
- **The Lounge (kendi barındırılan web)** — modern web istemcisi.

### IRC2P (ana topluluk ağı)

- **LimeChat** (ücretsiz, açık kaynak).
- **Textual** (App Store'da ücretli; kaynak kodu derlemek için mevcut).

### Ilita ağı

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protokol: **IRC**
- Sunucu: **127.0.0.1**
- Port: **6668**
- Şifreleme: **kapalı**
- Kullanıcı adı/takma ad: herhangi biri

#### Thunderbird Chat

- Hesap türü: **IRC**
- Sunucu: **127.0.0.1**
- Port: **6668**
- SSL/TLS: **kapalı**
- İsteğe bağlı: bağlantıda kanallara otomatik katılım

#### Dispatch (SAM v3)

`config.toml` varsayılan değerleri örneği:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Irc2P istemci tüneli: **127.0.0.1:6668** → yukarı akış sunucusu **port 6667** üzerinde.
- Gizli Servisler Yöneticisi: `http://127.0.0.1:7657/i2ptunnel/`.

### Önerilen, aktif olarak bakımı yapılan

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Ilita için ayrı tünel (örnek):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### macOS seçenekleri

- **SAM'i Etkinleştir** Java I2P'de (varsayılan olarak kapalı) `/configclients` veya `clients.config` üzerinden.
- Varsayılanlar: **127.0.0.1:7656/TCP** ve **127.0.0.1:7655/UDP**.
- Önerilen kriptografi: `SIGNATURE_TYPE=7` (Ed25519) ve `i2cp.leaseSetEncType=4,0` (ElGamal yedeklemeli ECIES‑X25519) veya sadece modern sistemler için `4`.

### Örnek yapılandırmalar

- Java I2P varsayılanı: **2 gelen / 2 giden**.
- i2pd varsayılanı: **5 gelen / 5 giden**.
- IRC için: **Her birinden 2–3** yeterlidir; router'lar arasında tutarlı davranış için açıkça ayarlayın.

## İstemci kurulumu

- **SSL/TLS'yi etkinleştirmeyin** dahili I2P IRC bağlantıları için. I2P zaten uçtan uca şifreleme sağlar. Ekstra TLS, anonimlik kazancı olmadan ek yük getirir.
- Kararlı kimlik için **kalıcı anahtarlar** kullanın; test etmiyorsanız her yeniden başlatmada anahtar yeniden oluşturmaktan kaçının.
- Birden fazla uygulama IRC kullanıyorsa, servisler arası korelasyonu azaltmak için **ayrı tüneller** (paylaşılmayan) tercih edin.
- Uzaktan kontrol (SAM/I2CP) izni vermeniz gerekiyorsa, localhost'a bağlayın ve erişimi SSH tünelleri veya kimlik doğrulamalı ters proxy'lerle güvence altına alın.

## Alternative connection method: SOCKS5

Bazı istemciler I2P'nin SOCKS5 proxy'si üzerinden bağlanabilir: **127.0.0.1:4447**. En iyi sonuçlar için 6668 portundaki özel bir IRC istemci tunnel'ını tercih edin; SOCKS, uygulama katmanı tanımlayıcılarını temizleyemez ve istemci anonimlik için tasarlanmamışsa bilgi sızıntısına neden olabilir.

## Troubleshooting

- **Bağlanamıyor** — Irc2P tunnel'ının çalıştığından ve router'ın tamamen bootstrapped olduğundan emin olun.
- **Resolve/join aşamasında takılıyor** — SSL'nin **devre dışı** olduğunu ve istemcinin **127.0.0.1:6668** adresine yönlendirildiğini iki kez kontrol edin.
- **Yüksek gecikme** — I2P tasarım gereği yüksek gecikmeli bir protokoldür. Tunnel sayılarını makul seviyelerde tutun (2–3) ve hızlı yeniden bağlanma döngülerinden kaçının.
- **SAM uygulamalarını kullanma** — SAM'in etkin olduğunu (Java) veya güvenlik duvarı tarafından engellenmediğini (i2pd) doğrulayın. Uzun süreli oturumlar önerilir.

## Appendix: Ports and naming

- Yaygın IRC tüneli portları: **6668** (Irc2P varsayılanı), alternatif olarak **6667** ve **6669**.
- `.b32.i2p` host adları: 52 karakterlik standart form; LS2/gelişmiş sertifikalar için 56+ karakterlik genişletilmiş formlar mevcuttur. Açıkça b32 adreslerine ihtiyacınız olmadıkça `.i2p` host adlarını kullanın.
