---
title: "Kişisel erişim için I2P üzerinden bir ssh sunucusu nasıl kurulur"
date: 2019-06-15
author: "idk"
description: "I2P üzerinden SSH"
---

# Kişisel erişim için I2P’nin arkasında bir SSH sunucusu nasıl kurulur

Bu, I2P veya i2pd kullanarak uzaktan bir SSH sunucusuna erişimde kullanmak üzere bir I2P tunnel kurup ince ayarlarını yapmaya yönelik bir kılavuzdur. Şimdilik, SSH sunucunuzu bir paket yöneticisi aracılığıyla kuracağınızı ve bir hizmet olarak çalıştığını varsayar.

Dikkat edilmesi gerekenler: Bu kılavuzda bazı varsayımlarda bulunuyorum. Bunlar, özellikle izolasyon için VM'ler (sanal makineler) veya containers (kapsayıcılar) kullanıyorsanız, sizin kurulumunuzda ortaya çıkabilecek güçlükler doğrultusunda ayarlanmalıdır. Bu, I2P router ile SSH sunucusunun aynı localhost'ta çalıştığını varsayar. Yeni oluşturulmuş SSH ana bilgisayar anahtarları kullanmalısınız; bunu ya yeni kurulmuş bir sshd kullanarak ya da eski anahtarları silip yeniden oluşturulmalarını zorlayarak yapabilirsiniz. Örneğin:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Java I2P'nin web arayüzünü kullanarak, [Gizli Hizmetler Yöneticisi](http://127.0.0.1:7657/i2ptunnelmgr) bölümüne gidin ve tunnel sihirbazını başlatın.

#### Tunnel Wizard

SSH sunucusu için bu tunnel'i yapılandırdığınız için, "Server" tunnel türünü seçmeniz gerekir.

**Ekran görüntüsü yer tutucusu:** Bir "Server" tunnel oluşturmak için sihirbazı kullanın

İnce ayarını daha sonra yapmalısınız, ancak başlamak için en kolay olan Standard tunnel türüdür.

**Ekran görüntüsü yer tutucusu:** "Standart" çeşidinden

Buna iyi bir açıklama yazın:


**Ekran görüntüsü yer tutucusu:** Ne için olduğunu açıklayın

Ve SSH sunucusunun nereden erişilebilir olacağını belirtin.

**Ekran görüntüsü yer tutucusu:** Hedef olarak SSH sunucunuzun gelecekteki konumunu belirtin

Sonuçları gözden geçirin ve ayarlarınızı kaydedin.

**Ekran görüntüsü yer tutucusu:** Ayarları kaydedin.

#### Advanced Settings

Şimdi Hidden Services Manager'a (Gizli Servisler Yöneticisi) geri dönün ve mevcut gelişmiş ayarları gözden geçirin. Kesinlikle değiştirmek isteyeceğiniz şeylerden biri, bunu toplu bağlantılar yerine etkileşimli bağlantılar için yapılandırmaktır.

**Ekran görüntüsü yer tutucusu:** Etkileşimli bağlantılar için tunnel'inizi yapılandırın

Bunun dışında, SSH sunucunuza erişirken performansı etkileyebilecek diğer seçenekler de vardır. Anonimliğiniz konusunda o kadar endişeli değilseniz, aldığınız atlama sayısını azaltabilirsiniz. Hızla ilgili sorun yaşıyorsanız, daha yüksek tunnel sayısı yardımcı olabilir. Birkaç yedek tunnel muhtemelen iyi bir fikirdir. Biraz ince ayar yapmanız gerekebilir.

**Ekran görüntüsü yer tutucusu:** Anonimlik sizin için önemli değilse, tunnel uzunluğunu azaltın.

Son olarak, tüm ayarlarınızın geçerli olması için tunnel'i yeniden başlatın.

Özellikle çok sayıda tunnels çalıştırmayı seçerseniz ilginç bir ayar olan "Reduce on Idle", uzun süreli hareketsizlik durumunda çalışan tunnels sayısını azaltır.

**Ekran görüntüsü yer tutucu:** Boştayken azaltın, yüksek sayıda tunnels seçtiyseniz

### Using i2pd

i2pd ile, tüm yapılandırma web arayüzü yerine dosyalar üzerinden yapılır. i2pd için bir SSH Service tunnel yapılandırmak için, aşağıdaki örnek ayarları anonimlik ve performans ihtiyaçlarınıza göre uyarlayın ve bunları tunnels.conf dosyasına kopyalayın.

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Birinci Adım: SSH Sunucusu için I2P tunnel kurulumu

SSH sunucunuza nasıl erişmek istediğinize bağlı olarak, ayarlarda birkaç değişiklik yapmak isteyebilirsiniz. Tüm SSH sunucularında yapmanız gereken bariz SSH güçlendirme işlemlerinin (Public-Key Authentication, root olarak oturum açmanın kapatılması vb.) yanı sıra, SSH sunucunuzun sunucu tunnel (I2P tüneli) dışında hiçbir adreste dinlemesini istemiyorsanız, AddressFamily değerini inet ve ListenAddress değerini 127.0.0.1 olarak değiştirmelisiniz.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
SSH sunucunuz için 22 dışında bir bağlantı noktası kullanmayı seçerseniz, I2P tunnel yapılandırmanızda bağlantı noktasını değiştirmeniz gerekecektir.

## Step Three: Set up I2P tunnel for SSH Client

İstemci bağlantınızı yapılandırabilmek için SSH sunucusunun I2P router konsolunu görebiliyor olmanız gerekir. Bu kurulumun güzel bir yanı da I2P tunnel’a yapılan ilk bağlantının kimliği doğrulanır olmasıdır; bu, SSH sunucusuna yaptığınız ilk bağlantının ortadaki adam (MITM) saldırısına uğrama riskini bir miktar azaltır ki bu, Trust-On-First-Use (TOFU) senaryolarında görülen bir risktir.

### Java I2P'yi Kullanma

#### Tunnel Sihirbazı

Öncelikle, gizli hizmetler yöneticisinden tunnel yapılandırma sihirbazını başlatın ve bir istemci tunnel seçin.

**Ekran görüntüsü yer tutucusu:** Client tunnel oluşturmak için sihirbazı kullanın

Ardından, standart tunnel türünü seçin. Bu yapılandırmaya daha sonra ince ayar yapacaksınız.

**Ekran görüntüsü yer tutucusu:** Standart türünde

İyi bir açıklama yazın.

**Ekran görüntüsü yer tutucusu:** İyi bir açıklama girin

Zor sayılabilecek tek kısım burası. I2P router konsolunun gizli servisler yöneticisine gidin ve SSH sunucu tunnel'ının base64 "local destination" bilgisini bulun. Bu bilgiyi bir sonraki adıma kopyalamanın bir yolunu bulmanız gerekecek. Genelde bunu kendime [Tox](https://tox.chat) üzerinden gönderiyorum; çoğu kişi için herhangi bir off-the-record (kayıt dışı/OTR) yöntem yeterli olacaktır.

**Ekran görüntüsü yer tutucu:** Bağlanmak istediğiniz hedefi bulun

Bağlanmak istediğiniz ve istemci cihazınıza iletilmiş olan base64 hedefi bulduğunuzda, onu istemci hedef alanına yapıştırın.

**Ekran görüntüsü yer tutucusu:** Hedefi ekleyin

Son olarak, SSH istemcinizin bağlanacağı yerel bir port belirleyin. Bu yerel port, base64 destination (base64 kodlu hedef) adresine ve dolayısıyla SSH sunucusuna bağlanacaktır.

**Ekran görüntüsü yer tutucusu:** Yerel bir bağlantı noktası seçin

Otomatik olarak başlamasını isteyip istemediğinize karar verin.

**Ekran görüntüsü yer tutucusu:** Otomatik olarak başlatılmasını isteyip istemediğinize karar verin

#### Gelişmiş Ayarlar

Daha önce olduğu gibi, ayarları etkileşimli bağlantılar için optimize edilmiş olacak şekilde değiştirmeniz gerekir. Ayrıca, sunucuda istemci beyaz listeleme (whitelisting) ayarlamak istiyorsanız, "Generate key to enable persistent client tunnel identity" radyo düğmesini seçmelisiniz.

**Ekran görüntüsü yer tutucusu:** Etkileşimli olacak şekilde yapılandırın

### Using i2pd

Bunu, tunnels.conf dosyanıza aşağıdaki satırları ekleyerek yapılandırabilir ve performans/anonimlik gereksinimlerinize göre ayarlayabilirsiniz.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

I2P üzerindeki sunucunuza bağlanmak için bir SSH istemcisini yapılandırmanın pek çok yolu vardır, ancak anonim kullanım için SSH istemcinizi güvenli hâle getirmek adına yapmanız gereken bazı şeyler vardır. İlk olarak, anonim ve anonim olmayan SSH bağlantılarınızın birbirine karışma riskini önlemek için, yalnızca tek ve belirli bir anahtarla SSH sunucusuna kimliğini bildirecek şekilde yapılandırmalısınız.

$HOME/.ssh/config dosyanızın aşağıdaki satırları içerdiğinden emin olun:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Alternatif olarak, seçeneklerinizi zorunlu kılmak ve I2P ile otomatik bağlantı kurmak için .bash_alias dosyasına bir giriş ekleyebilirsiniz. Özetle, IdentitiesOnly ayarını zorunlu kılmalı ve bir kimlik dosyası sağlamalısınız.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Bu az çok isteğe bağlıdır, ancak oldukça güzel bir özelliktir ve hedefinize rastlayan herhangi birinin SSH hizmeti barındırdığınızı fark etmesini engeller.

İlk olarak, kalıcı istemci tunnel hedefini alın ve bunu sunucuya iletin.

**Ekran görüntüsü yer tutucusu:** İstemci hedefini al

İstemcinin base64 hedefini sunucunun hedef beyaz listesine ekleyin. Artık yalnızca o belirli client tunnel'dan server tunnel'a bağlanabileceksiniz ve başka hiç kimse o hedefe bağlanamayacak.

**Ekran görüntüsü yer tutucusu:** Ve bunu sunucu beyaz listesine yapıştırın

Karşılıklı kimlik doğrulama en iyisidir.

**Not:** Orijinal gönderide atıfta bulunulan görsellerin `/static/images/` dizinine eklenmesi gerekir: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
