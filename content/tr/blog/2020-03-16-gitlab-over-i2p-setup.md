---
title: "I2P üzerinden Gitlab Kurulumu"
date: 2020-03-16
author: "idk"
description: "Başkaları için I2P Git depolarını yansıtın ve Clearnet (açık internet) depolarını köprüleyin"
categories: ["development"]
---

Bu, hizmetin kendisini yönetmek için Docker kullanarak Gitlab ve I2P'yi yapılandırırken kullandığım kurulum sürecidir. Bu şekilde Gitlab'ı I2P üzerinde barındırmak çok kolaydır; tek bir kişi tarafından fazla bir zorluk olmadan yönetilebilir. Bu talimatlar herhangi bir Debian tabanlı sistemde çalışmalıdır ve Docker ile bir I2P router bulunan herhangi bir sisteme de kolayca uyarlanabilir.

## Bağımlılıklar ve Docker

Gitlab bir kapsayıcıda çalıştığı için, ana sistemimize yalnızca kapsayıcının gerektirdiği bağımlılıkları kurmamız gerekir. Kolaylıkla, ihtiyaç duyduğumuz her şeyi şununla kurabiliriz:

```
sudo apt install docker.io
```
## Docker kapsayıcılarını getirin

docker yüklendikten sonra, gitlab için gerekli docker konteynerlerini çekebilirsiniz. *Henüz çalıştırmayın.*

```
docker pull gitlab/gitlab-ce
```
## Gitlab için bir I2P HTTP proxy'si kurun (Önemli bilgiler, isteğe bağlı adımlar)

I2P içindeki Gitlab sunucuları, I2P dışındaki internet üzerindeki sunucularla etkileşim kurma yeteneğiyle ya da bu yetenek olmadan çalıştırılabilir. Gitlab sunucusunun I2P dışındaki sunucularla etkileşim kurmasına *izin verilmediği* durumda, I2P dışındaki internet üzerindeki bir git sunucusundan bir git deposu klonlanarak anonimliği bozulamaz.

Gitlab sunucusunun I2P dışındaki sunucularla etkileşime *izin verildiği* durumda, kullanıcılar için bir "Köprü" olarak işlev görebilir; kullanıcılar bunu, I2P dışındaki içeriği I2P üzerinden erişilebilir bir kaynağa yansıtmak için kullanabilir, ancak bu durumda *anonim değildir*.

**Web depolarına erişimi olan, köprülenmiş ve anonim olmayan bir Gitlab örneğine sahip olmak istiyorsanız**, başka bir değişiklik gerekli değildir.

**Web-Only Depolara erişimi olmayan, yalnızca I2P için bir Gitlab örneği istiyorsanız**, Gitlab’ı bir I2P HTTP Proxy kullanacak şekilde yapılandırmanız gerekir. Varsayılan I2P HTTP proxy yalnızca `127.0.0.1` üzerinde dinlediğinden, Docker için Docker ağının genellikle `172.17.0.1` olan Host/Gateway (Ana Makine/Ağ Geçidi) adresinde dinleyen yeni bir tane kurmanız gerekir. Ben kendi proxy’mi `4446` numaralı bağlantı noktasında yapılandırıyorum.

## Konteyneri Yerel Olarak Başlatın

Bunu ayarladıktan sonra, konteyneri başlatabilir ve Gitlab örneğinizi yerel olarak yayınlayabilirsiniz:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Yerel Gitlab örneğinize erişin ve yönetici hesabınızı oluşturun. Güçlü bir parola seçin ve kullanıcı hesap sınırlarını kaynaklarınıza uygun olacak şekilde yapılandırın.

## Hizmet tunnel'larınızı yapılandırın ve bir ana makine adı için kaydolun

Gitlab'ı yerel olarak kurup yapılandırdıktan sonra I2P Router console'a gidin. İki adet sunucu tunnel ayarlamanız gerekecek; bunlardan biri TCP port 8080'deki Gitlab web(HTTP) arayüzüne, diğeri TCP Port 8022'deki Gitlab SSH arayüzüne yönlendirilecek.

### Gitlab Web(HTTP) Interface

Web arayüzü için bir "HTTP" server tunnel kullanın. http://127.0.0.1:7657/i2ptunnelmgr adresinden "New Tunnel Wizard" sihirbazını başlatın ve aşağıdaki değerleri girin:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

SSH arayüzü için, "Standard" server tunnel kullanın. http://127.0.0.1:7657/i2ptunnelmgr adresinden "New Tunnel Wizard" başlatın ve aşağıdaki değerleri girin:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Son olarak, `gitlab.rb` dosyasını değiştirdiyseniz ya da bir ana bilgisayar adı kaydettiyseniz, ayarların yürürlüğe girmesi için gitlab hizmetini yeniden başlatmanız gerekecek.
