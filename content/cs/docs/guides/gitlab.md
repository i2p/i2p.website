---
title: "Provoz GitLabu přes I2P"
description: "Nasazení GitLabu uvnitř I2P pomocí Dockeru a I2P routeru"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Hostování GitLabu uvnitř I2P je jednoduché: spusťte GitLab omnibus kontejner, zpřístupněte ho na loopback a přesměrujte provoz přes I2P tunnel. Níže uvedené kroky odpovídají konfiguraci použité pro `git.idk.i2p`, ale fungují pro jakoukoli self-hosted instanci.

## 1. Předpoklady

- Debian nebo jiná Linuxová distribuce s nainstalovaným Docker Engine (`sudo apt install docker.io` nebo `docker-ce` z repozitáře Docker).
- I2P router (Java I2P nebo i2pd) s dostatečnou šířkou pásma pro obsluhu vašich uživatelů.
- Volitelné: dedikovaný VM, aby GitLab a router zůstaly izolované od vašeho desktopového prostředí.

## 2. Stáhněte GitLab Image

```bash
docker pull gitlab/gitlab-ce:latest
```
Oficiální obraz je vytvořen z Ubuntu základních vrstev a pravidelně aktualizován. Pokud potřebujete další ujištění, prostudujte si [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile).

## 3. Rozhodněte se mezi Bridgingem a čistě I2P

- **Pouze I2P** instance nikdy nekontaktují hosty na clearnetu. Uživatelé mohou zrcadlit repozitáře z jiných I2P služeb, ale ne z GitHub/GitLab.com. To maximalizuje anonymitu.
- **Propojené** instance se připojují k Git hostům na clearnetu přes HTTP proxy. To je užitečné pro zrcadlení veřejných projektů do I2P, ale deanonymizuje odchozí požadavky serveru.

Pokud zvolíte bridged režim, nakonfigurujte GitLab tak, aby používal I2P HTTP proxy svázané na Docker hostiteli (například `http://172.17.0.1:4446`). Výchozí router proxy naslouchá pouze na `127.0.0.1`; přidejte nový proxy tunnel svázaný s Docker gateway adresou.

## 4. Spuštění kontejneru

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
- Svažte publikované porty na loopback; tunely I2P je zpřístupní podle potřeby.
- Nahraďte `/srv/gitlab/...` cestami k úložišti, které vyhovují vašemu hostiteli.

Jakmile je kontejner spuštěn, navštivte `https://127.0.0.1:8443/`, nastavte administrátorské heslo a nakonfigurujte omezení účtů.

## 5. Zpřístupnění GitLabu přes I2P

Vytvořte tři I2PTunnel **server** tunely:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Nakonfigurujte každý tunnel s odpovídající délkou a šířkou pásma. Pro veřejné instance je dobrým výchozím bodem 3 hopy se 4–6 tunnely na směr. Zveřejněte výsledné Base32/Base64 destinace na své úvodní stránce, aby si uživatelé mohli nakonfigurovat klientské tunnely.

### Destination Enforcement

Pokud používáte HTTP(S) tunely, aktivujte vynucení cílové destinace, aby k službě měl přístup pouze zamýšlený hostname. To zabrání zneužití tunelu jako generické proxy.

## 6. Maintenance Tips

- Spusťte `docker exec gitlab gitlab-ctl reconfigure` vždy, když změníte nastavení GitLabu.
- Sledujte využití disku (`/srv/gitlab/data`) – Git repozitáře rychle rostou.
- Pravidelně zálohujte konfigurační a datové adresáře. GitLabové [backup rake tasks](https://docs.gitlab.com/ee/raketasks/backup_restore.html) fungují uvnitř kontejneru.
- Zvažte umístění externího monitorovacího tunelu v klientském režimu, abyste zajistili dostupnost služby ze širší sítě.

## 6. Tipy pro údržbu

- [Embedding I2P ve vaší aplikaci](/docs/applications/embedding/)
- [Git přes I2P (průvodce pro klienty)](/docs/applications/git/)
- [Git bundle soubory pro offline/pomalé sítě](/docs/applications/git-bundle/)

Dobře nakonfigurovaná instance GitLabu poskytuje centrum pro společný vývoj zcela uvnitř I2P. Udržujte router v dobrém stavu, průběžně aktualizujte bezpečnostní záplaty GitLabu a koordinujte se s komunitou, jak vaše uživatelská základna roste.
