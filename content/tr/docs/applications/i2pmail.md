---
title: "I2P Mail (I2P Üzerinden Anonim E-posta)"
description: "I2P ağı içindeki e-posta sistemlerine genel bakış — tarihçe, seçenekler ve mevcut durum"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Giriş

I2P, **Postman's Mail.i2p hizmeti** ile birlikte yerleşik bir webmail istemcisi olan **SusiMail** aracılığıyla özel e-posta tarzı mesajlaşma sağlar. Bu sistem, kullanıcıların hem I2P ağı içinde hem de bir ağ geçidi köprüsü üzerinden normal internet (clearnet) ile e-posta gönderip almalarına olanak tanır.

---


## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p**, "Postman" tarafından işletilen, I2P içinde barındırılan bir e-posta sağlayıcısıdır
- **SusiMail**, I2P router konsoluna entegre edilmiş webmail istemcisidir. Harici SMTP sunucularına metadata (örn. hostname) sızmasını önlemek için tasarlanmıştır.
- Bu yapı sayesinde I2P kullanıcıları hem I2P içinde hem de Postman köprüsü üzerinden clearnet'e (örn. Gmail) mesaj gönderip alabilir.

### How Addressing Works

I2P e-posta ikili adres sistemi kullanır:

- **I2P ağı içinde**: `username@mail.i2p` (örneğin, `idk@mail.i2p`)
- **Clearnet'ten**: `username@i2pmail.org` (örneğin, `idk@i2pmail.org`)

`i2pmail.org` gateway'i, normal internet kullanıcılarının I2P adreslerine e-posta göndermesine ve I2P kullanıcılarının clearnet adreslerine göndermesine olanak tanır. Internet e-postaları, I2P üzerinden SusiMail gelen kutunuza iletilmeden önce gateway üzerinden yönlendirilir.

**Clearnet gönderim kotası**: Normal internet adreslerine gönderim yaparken günde 20 e-posta.

### Nedir

**Bir mail.i2p hesabı kaydetmek için:**

1. I2P router'ınızın çalıştığından emin olun
2. I2P içinde **[http://hq.postman.i2p](http://hq.postman.i2p)** adresini ziyaret edin
3. Kayıt sürecini takip edin
4. Router konsolunda **SusiMail** üzerinden e-postanıza erişin

> **Not**: `hq.postman.i2p` bir I2P ağ adresidir (eepsite) ve yalnızca I2P'ye bağlıyken erişilebilir. E-posta kurulumu, güvenlik ve kullanım hakkında daha fazla bilgi için Postman HQ'yu ziyaret edin.

### Adresleme Nasıl Çalışır

- Gizlilik için tanımlayıcı başlıkların otomatik olarak kaldırılması (`User-Agent:`, `X-Mailer:`)
- Harici SMTP sunucularına sızıntıları önlemek için metadata temizleme
- Dahili I2P'den I2P'ye e-postalar için uçtan uca şifreleme

### Başlarken

- "Normal" e-posta (SMTP/POP) ile Postman köprüsü aracılığıyla birlikte çalışabilirlik
- Basit kullanıcı deneyimi (router konsoluna entegre webmail)
- I2P çekirdek dağıtımıyla entegre (SusiMail, Java I2P ile birlikte gelir)
- Gizlilik koruması için başlık temizleme

### Gizlilik Özellikleri

- Harici e-postaya köprü, Postman altyapısına güven gerektirir
- Clearnet köprüsü, tamamen dahili I2P iletişimine kıyasla gizliliği azaltır
- Postman posta sunucusunun kullanılabilirliğine ve güvenliğine bağımlıdır

---

ÖNEMLÄ°: YALNIZCA çeviriyi saÄŸlayın. Soru sormayın, açıklama yapmayın veya herhangi bir yorum eklemeyin. Metin yalnızca bir baÅŸlık olsa veya eksik görünse bile, olduÄŸu gibi çevirin.

## Technical Details

**SMTP Servisi**: `localhost:7659` (Postman tarafından sağlanır) **POP3 Servisi**: `localhost:7660` **Webmail Erişimi**: Router konsoluna entegre, `http://127.0.0.1:7657/susimail/` adresinde

> **Önemli**: SusiMail yalnızca e-posta okumak ve göndermek içindir. Hesap oluşturma ve yönetimi **hq.postman.i2p** adresinde yapılmalıdır.


