---
title: "Vytvoření a provoz I2P Reseed serveru"
description: "Kompletní průvodce nastavením a provozem I2P reseed serveru pro pomoc novým routerům připojit se do sítě"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Reseed hosty jsou klíčovou infrastrukturou pro síť I2P, poskytují novým routerům počáteční skupinu uzlů během procesu bootstrapu. Tento průvodce vás provede nastavením a provozem vlastního reseed serveru.

## Co je I2P Reseed Server?

Server pro reseed I2P pomáhá integrovat nové routery do sítě I2P tím, že:

- **Poskytování počátečního zjišťování protějšků**: Nové routery získají výchozí sadu síťových uzlů, ke kterým se připojí
- **Obnova bootstrapu**: Pomoc routerům, které mají potíže s udržením připojení
- **Bezpečná distribuce**: Proces reseedingu je šifrovaný a digitálně podepsaný pro zajištění síťové bezpečnosti

Když se nový I2P router spustí poprvé (nebo ztratil všechna svá peer připojení), kontaktuje reseed servery, aby stáhl počáteční sadu informací o routerech. To umožňuje novému routeru začít budovat vlastní síťovou databázi a navazovat tunnely.

## Předpoklady

Než začnete, budete potřebovat:

- Linuxový server (doporučuje se Debian/Ubuntu) s root přístupem
- Doménové jméno odkazující na váš server
- Minimálně 1GB RAM a 10GB diskového prostoru
- Běžící I2P router na serveru pro naplnění network database
- Základní znalost správy Linuxových systémů

## Příprava serveru

### Step 1: Update System and Install Dependencies

Nejprve aktualizujte systém a nainstalujte požadované balíčky:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Toto nainstaluje: - **golang-go**: Runtime programovacího jazyka Go - **git**: Systém pro správu verzí - **make**: Nástroj pro automatizaci buildů - **docker.io & docker-compose**: Kontejnerová platforma pro provoz Nginx Proxy Manager

![Instalace požadovaných balíčků](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Naklonujte repozitář reseed-tools a sestavte aplikaci:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
Balíček `reseed-tools` poskytuje základní funkcionalitu pro provoz reseed serveru. Zajišťuje: - Sběr informací o routerech z vaší lokální síťové databáze - Balení informací o routerech do podepsaných SU3 souborů - Poskytování těchto souborů přes HTTPS

![Klonování repozitáře reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Vygenerujte SSL certifikát a soukromý klíč vašeho reseed serveru:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Důležité parametry**: - `--signer`: Vaše e-mailová adresa (nahraďte `admin@stormycloud.org` svou vlastní) - `--netdb`: Cesta k síťové databázi vašeho I2P routeru - `--port`: Interní port (doporučuje se 8443) - `--ip`: Navázat na localhost (pro veřejný přístup použijeme reverzní proxy) - `--trustProxy`: Důvěřovat hlavičkám X-Forwarded-For z reverzní proxy

Příkaz vygeneruje: - Privátní klíč pro podepisování SU3 souborů - SSL certifikát pro zabezpečená HTTPS spojení

![Generování SSL certifikátu](/images/guides/reseed/reseed_03.png)

### Krok 1: Aktualizace systému a instalace závislostí

**Kritické**: Bezpečně zálohujte vygenerované klíče umístěné v `/home/i2p/.reseed/`:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Uložte tuto zálohu na bezpečné, šifrované místo s omezeným přístupem. Tyto klíče jsou nezbytné pro provoz vašeho reseed serveru a měly by být pečlivě chráněny.

## Configuring the Service

### Krok 2: Klonování a sestavení Reseed nástrojů

Vytvořte systemd službu pro automatické spuštění reseed serveru:

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
**Nezapomeňte nahradit** `admin@stormycloud.org` vlastní e-mailovou adresou.

Nyní službu povolte a spusťte:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Zkontrolujte, že služba běží:

```bash
sudo systemctl status reseed
```
![Ověření stavu reseed služby](/images/guides/reseed/reseed_04.png)

### Krok 3: Vygenerování SSL certifikátu

Pro optimální výkon můžete chtít pravidelně restartovat službu reseed pro obnovení informací o routerech:

```bash
sudo crontab -e
```
Přidejte tento řádek pro restartování služby každé 3 hodiny:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

Reseed server běží na localhost:8443 a potřebuje reverzní proxy pro zpracování veřejného HTTPS provozu. Doporučujeme Nginx Proxy Manager pro jeho snadné použití.

### Krok 4: Zálohujte své klíče

Nasazení Nginx Proxy Manager pomocí Dockeru:

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
Toto vystavuje: - **Port 80**: HTTP provoz - **Port 81**: Rozhraní pro správu - **Port 443**: HTTPS provoz

### Configure Proxy Manager

1. Přístup k administračnímu rozhraní na adrese `http://your-server-ip:81`

2. Přihlaste se pomocí výchozích přihlašovacích údajů:
   - **Email**: admin@example.com
   - **Heslo**: changeme

**Důležité**: Tyto přihlašovací údaje změňte okamžitě po prvním přihlášení!

![Přihlášení Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. Přejděte na **Proxy Hosts** a klikněte na **Add Proxy Host**

![Přidání proxy hostu](/images/guides/reseed/reseed_06.png)

4. Nakonfigurujte proxy hostitele:
   - **Doménové jméno**: Vaše reseed doména (např. `reseed.example.com`)
   - **Schéma**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - Povolte **Cache Assets**
   - Povolte **Block Common Exploits**
   - Povolte **Websockets Support**

![Konfigurace podrobností proxy hostitele](/images/guides/reseed/reseed_07.png)

5. V záložce **SSL**:
   - Vyberte **Request a new SSL Certificate** (Let's Encrypt)
   - Povolte **Force SSL**
   - Povolte **HTTP/2 Support**
   - Odsouhlaste podmínky služby Let's Encrypt

![Konfigurace SSL certifikátu](/images/guides/reseed/reseed_08.png)

6. Klikněte na **Uložit**

Váš reseed server by nyní měl být přístupný na `https://reseed.example.com`

![Úspěšná konfigurace reseed serveru](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Jakmile váš reseed server funguje, kontaktujte vývojáře I2P, aby byl přidán do oficiálního seznamu reseed serverů.

### Krok 5: Vytvoření Systemd služby

Napište e-mail **zzz** (vedoucímu vývojáři I2P) s následujícími informacemi:

- **I2P Email**: zzz@mail.i2p
- **Clearnet Email**: zzz@i2pmail.org

### Krok 6: Volitelné - Konfigurace periodických restartů

Uveďte ve svém e-mailu:

1. **URL reseed serveru**: Úplná HTTPS URL adresa (např. `https://reseed.example.com`)
2. **Veřejný reseed certifikát**: Umístěný v `/home/i2p/.reseed/` (přiložte soubor `.crt`)
3. **Kontaktní e-mail**: Váš preferovaný způsob kontaktu pro upozornění na údržbu serveru
4. **Umístění serveru**: Volitelné, ale užitečné (země/region)
5. **Předpokládaná dostupnost**: Váš závazek k udržování serveru

### Verification

Vývojáři I2P ověří, že váš reseed server: - Je správně nakonfigurován a poskytuje informace o routerech - Používá platné SSL certifikáty - Poskytuje správně podepsané SU3 soubory - Je dostupný a responzivní

Po schválení bude váš reseed server přidán do seznamu distribuovaného s I2P routery, což pomůže novým uživatelům připojit se k síti!

## Monitoring and Maintenance

### Instalace Nginx Proxy Manager

Monitorujte svou reseed službu:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Konfigurace správce proxy

Sledujte systémové prostředky:

```bash
htop
df -h
```
### Update Reseed Tools

Pravidelně aktualizujte reseed-tools, abyste získali nejnovější vylepšení:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Kontaktní informace

Pokud používáte Let's Encrypt prostřednictvím Nginx Proxy Manager, certifikáty se automaticky obnoví. Ověřte, že obnova funguje:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Konfigurace služby

### Požadované informace

Zkontrolujte logy na chyby:

```bash
sudo journalctl -u reseed -n 50
```
Časté problémy: - I2P router neběží nebo je netDb prázdná - Port 8443 je již používán - Problémy s oprávněními k adresáři `/home/i2p/.reseed/`

### Ověření

Ujistěte se, že váš I2P router běží a má naplněnou svou síťovou databázi:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Měli byste vidět mnoho souborů `.dat`. Pokud je prázdný, počkejte, až váš I2P router objeví protějšky.

### SSL Certificate Errors

Ověřte, že vaše certifikáty jsou platné:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Zkontrolovat stav služby

Zkontrolujte: - DNS záznamy správně ukazují na váš server - Firewall povoluje porty 80 a 443 - Nginx Proxy Manager běží: `docker ps`

## Security Considerations

- **Zabezpečte své soukromé klíče**: Nikdy nesdílejte ani nevystavujte obsah `/home/i2p/.reseed/`
- **Pravidelné aktualizace**: Udržujte aktuální systémové balíčky, Docker a reseed-tools
- **Sledujte logy**: Kontrolujte podezřelé vzory přístupu
- **Rate limiting**: Zvažte implementaci rate limitingu pro prevenci zneužití
- **Pravidla firewallu**: Vystavte pouze nezbytné porty (80, 443, 81 pro administraci)
- **Administrační rozhraní**: Omezte přístup k administračnímu rozhraní Nginx Proxy Manager (port 81) pouze na důvěryhodné IP adresy

## Contributing to the Network

Provozováním reseed serveru poskytujete kritickou infrastrukturu pro síť I2P. Děkujeme, že přispíváte k soukromějšímu a decentralizovanějšímu internetu!

Pro dotazy nebo pomoc se obraťte na komunitu I2P: - **Fórum**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p na různých sítích - **Vývoj**: [i2pgit.org](https://i2pgit.org)

---

 NEKLADETÉ otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text jen nadpis nebo se zdá neúplný, přeložte ho tak, jak je.

*Průvodce původně vytvořen [Stormy Cloud](https://www.stormycloud.org), upraveno pro dokumentaci I2P.*
