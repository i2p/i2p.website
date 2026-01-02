---
title: "GitLab'ı I2P Üzerinde Çalıştırma"
description: "I2P içinde Docker ve bir I2P yönlendiricisi kullanarak GitLab dağıtımı"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

GitLab'ı I2P içinde barındırmak basittir: GitLab omnibus konteynerini çalıştırın, loopback üzerinde açığa çıkarın ve trafiği bir I2P tüneli üzerinden yönlendirin. Aşağıdaki adımlar `git.idk.i2p` için kullanılan yapılandırmayı yansıtır ancak herhangi bir kendi barındırılan örnek için çalışır.

## 1. Ön Gereksinimler

- Docker Engine yüklü Debian veya başka bir Linux dağıtımı (`sudo apt install docker.io` veya Docker deposundan `docker-ce`).
- Kullanıcılarınıza hizmet verecek yeterli bant genişliğine sahip bir I2P router (Java I2P veya i2pd).
- İsteğe bağlı: GitLab ve router'ın masaüstü ortamınızdan izole kalması için ayrılmış bir VM.

## 2. GitLab İmajını Çekin

```bash
docker pull gitlab/gitlab-ce:latest
```
Resmi imaj Ubuntu temel katmanlarından oluşturulur ve düzenli olarak güncellenir. Ek güvence ihtiyacınız varsa [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) dosyasını inceleyin.

## 3. Köprüleme ile Yalnızca I2P Arasında Karar Verin

- **Yalnızca I2P** örnekleri asla clearnet sunucularıyla iletişim kurmaz. Kullanıcılar depoları diğer I2P hizmetlerinden yansıtabilir ancak GitHub/GitLab.com'dan yansıtamaz. Bu, anonimliği maksimize eder.
- **Köprülenmiş** örnekler, bir HTTP proxy üzerinden clearnet Git sunucularına erişir. Bu, genel projeleri I2P'ye yansıtmak için kullanışlıdır ancak sunucunun giden isteklerini anonimlikten çıkarır.

Bridged modu seçerseniz, GitLab'ı Docker host'unda bağlı bir I2P HTTP proxy kullanacak şekilde yapılandırın (örneğin `http://172.17.0.1:4446`). Varsayılan router proxy yalnızca `127.0.0.1` üzerinde dinler; Docker gateway adresine bağlı yeni bir proxy tunnel ekleyin.

## 4. Container'ı Başlatın

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- Yayınlanan portları loopback'e bağlayın; I2P tunnel'ları bunları gerektiğinde açığa çıkaracaktır.
- `/srv/gitlab/...` yolunu sunucunuza uygun depolama yollarıyla değiştirin.

Container çalıştıktan sonra `https://127.0.0.1:8443/` adresini ziyaret edin, bir yönetici parolası belirleyin ve hesap limitlerini yapılandırın.

## 5. GitLab'ı I2P Üzerinden Erişilebilir Hale Getirme

Üç adet I2PTunnel **sunucu** tüneli oluşturun:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Her tunnel'ı uygun tunnel uzunluğu ve bant genişliği ile yapılandırın. Genel erişime açık sunucular için, her yön başına 4–6 tunnel ile 3 hop iyi bir başlangıç noktasıdır. Ortaya çıkan Base32/Base64 adreslerini açılış sayfanızda yayınlayın, böylece kullanıcılar client tunnel'larını yapılandırabilir.

### Destination Enforcement

HTTP(S) tünelleri kullanıyorsanız, yalnızca hedeflenen hostname'in hizmete erişebilmesi için hedef zorunluluğunu etkinleştirin. Bu, tünelin genel bir proxy olarak kötüye kullanılmasını önler.

## 6. Maintenance Tips

- GitLab ayarlarını her değiştirdiğinizde `docker exec gitlab gitlab-ctl reconfigure` komutunu çalıştırın.
- Disk kullanımını izleyin (`/srv/gitlab/data`)—Git depoları hızla büyür.
- Yapılandırma ve veri dizinlerini düzenli olarak yedekleyin. GitLab'ın [yedekleme rake görevleri](https://docs.gitlab.com/ee/raketasks/backup_restore.html) container içinde çalışır.
- Hizmetin daha geniş ağdan erişilebilir olduğundan emin olmak için harici bir izleme tunnel'ını client modunda yerleştirmeyi düşünün.

## 6. Bakım İpuçları

- [I2P'yi uygulamanıza gömme](/docs/applications/embedding/)
- [I2P üzerinden Git (istemci rehberi)](/docs/applications/git/)
- [Çevrimdışı/yavaş ağlar için Git paketleri](/docs/applications/git-bundle/)

İyi yapılandırılmış bir GitLab örneği, tamamen I2P içinde işbirlikçi bir geliştirme merkezi sağlar. Router'ı sağlıklı tutun, GitLab güvenlik güncellemelerini takip edin ve kullanıcı tabanınız büyüdükçe toplulukla koordinasyon halinde olun.
