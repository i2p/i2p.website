---
title: "Nastavení Gitlabu přes I2P"
date: 2020-03-16
author: "idk"
description: "Zrcadlete I2P Git repozitáře a zprostředkujte ostatním přístup k Clearnet repozitářům"
categories: ["development"]
---

Toto je postup nastavení, který používám k konfiguraci Gitlabu a I2P, přičemž Docker slouží ke správě samotné služby. Gitlab je tímto způsobem na I2P velmi snadné hostovat; spravovat jej bez větších obtíží zvládne i jediná osoba. Tyto pokyny by měly fungovat na jakémkoli systému založeném na Debianu a snadno se dají použít i na jakémkoli systému, kde jsou k dispozici Docker a I2P router.

## Závislosti a Docker

Protože Gitlab běží v kontejneru, na našem hlavním systému musíme nainstalovat pouze závislosti potřebné pro tento kontejner. Pohodlně můžete vše potřebné nainstalovat pomocí:

```
sudo apt install docker.io
```
## Stáhněte Docker kontejnery

Jakmile máte nainstalovaný Docker, můžete stáhnout kontejnery Dockeru potřebné pro GitLab. *Zatím je nespouštějte.*

```
docker pull gitlab/gitlab-ce
```
## Nastavení I2P HTTP proxy pro Gitlab (Důležité informace, volitelné kroky)

Servery Gitlab uvnitř I2P lze provozovat se schopností komunikovat se servery na internetu mimo I2P, nebo bez ní. V případě, že server Gitlab *nemá povoleno* komunikovat se servery mimo I2P, není možné jej deanonymizovat klonováním repozitáře Git ze serveru Git na internetu mimo I2P.

V případě, že je serveru Gitlab *povoleno* komunikovat se servery mimo I2P, může sloužit jako "Bridge" (most) pro uživatele, kteří jej mohou použít k zrcadlení obsahu mimo I2P na zdroj přístupný v I2P, nicméně v tomto případě *není anonymní*.

**Pokud chcete mít přemostěnou, neanonymní instanci Gitlabu s přístupem k webovým repozitářům**, nejsou nutné žádné další úpravy.

**Pokud chcete mít instanci Gitlabu pouze v I2P bez přístupu k repozitářům dostupným pouze na webu**, budete muset nakonfigurovat Gitlab tak, aby používal I2P HTTP Proxy. Protože výchozí I2P HTTP proxy naslouchá pouze na `127.0.0.1`, budete muset nastavit novou pro Docker, která naslouchá na adrese hostitele/brány sítě Docker, což je obvykle `172.17.0.1`. Konfiguruji ji na portu `4446`.

## Spusťte kontejner lokálně

Jakmile to máte nastavené, můžete spustit kontejner a zpřístupnit svou instanci Gitlabu lokálně:

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
Navštivte svou lokální instanci Gitlabu a nastavte svůj administrátorský účet. Zvolte silné heslo a nastavte limity uživatelských účtů tak, aby odpovídaly vašim prostředkům.

## Nastavte tunnels pro svou službu a zaregistrujte si název hostitele

Jakmile máte Gitlab nastavený lokálně, přejděte do I2P Router console. Budete muset nastavit dva serverové tunnels, jeden vedoucí k web(HTTP) rozhraní Gitlabu na TCP portu 8080 a jeden k SSH rozhraní Gitlabu na TCP Portu 8022.

### Gitlab Web(HTTP) Interface

Pro webové rozhraní použijte serverový "HTTP" tunnel. Z http://127.0.0.1:7657/i2ptunnelmgr spusťte "New Tunnel Wizard" a zadejte následující hodnoty:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Pro rozhraní SSH použijte "Standard" serverový tunnel. Z http://127.0.0.1:7657/i2ptunnelmgr spusťte "New Tunnel Wizard" a zadejte následující hodnoty:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Nakonec, pokud jste buď upravili `gitlab.rb`, nebo jste zaregistrovali název hostitele, budete muset restartovat službu GitLab, aby se nastavení projevila.
