---
title: "Servery pro reseed (počáteční naplnění sítě)"
description: "Provozování služeb reseed (počáteční získání seznamu uzlů) a alternativních metod bootstrap (počáteční připojení k síti)"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## O reseed serverech

Nové routery potřebují hrstku uzlů, aby se připojily k síti I2P. Reseed servery poskytují tuto počáteční sadu pro bootstrap (počáteční zavedení) prostřednictvím šifrovaných stahování přes HTTPS. Každý reseed balíček je podepsán serverem, což brání manipulaci neověřenými stranami. Zavedené routery mohou příležitostně provést reseed, pokud jejich sada uzlů zastará.

### Proces bootstrapu sítě

Když se I2P router poprvé spustí nebo byl po delší dobu offline, potřebuje data RouterInfo, aby se připojil k síti. Protože router nemá žádné existující peery, nemůže tyto informace získat ze samotné sítě I2P. Mechanismus reseed (mechanismus počátečního zavedení do sítě) řeší problém s počátečním zavedením tím, že poskytuje soubory RouterInfo z důvěryhodných externích serverů HTTPS.

Proces reseedu (počáteční stažení důvěryhodných RouterInfo pro počáteční připojení do sítě) doručuje 75-100 souborů RouterInfo v jednom kryptograficky podepsaném balíčku. Tím je zajištěno, že nové routery mohou rychle navázat spojení, aniž by byly vystaveny útokům typu man-in-the-middle, které by je mohly izolovat do oddělených, nedůvěryhodných částí sítě.

### Aktuální stav sítě

K říjnu 2025 běží síť I2P na verzi routeru 2.10.0 (verze API 0.9.67). reseed protocol (protokol pro počáteční naplnění informacemi o síti) zavedený ve verzi 0.9.14 zůstává stabilní a ve své základní funkčnosti nezměněný. Síť udržuje více nezávislých reseed serverů rozmístěných po celém světě, aby byla zajištěna dostupnost a odolnost vůči cenzuře.

Služba [checki2p](https://checki2p.com/reseed) monitoruje všechny I2P reseed servery každé 4 hodiny a poskytuje kontroly stavu v reálném čase a metriky dostupnosti pro infrastrukturu reseed.

## Specifikace formátu souboru SU3

Formát souboru SU3 je základem protokolu reseed I2P (proces doplnění počátečních dat sítě), který zajišťuje doručování kryptograficky podepsaného obsahu. Porozumění tomuto formátu je zásadní pro implementaci reseed serverů a klientů.

### Struktura souborů

Formát SU3 se skládá ze tří hlavních částí: hlavičky (40+ bajtů), obsahu (proměnná délka) a podpisu (délka určená v hlavičce).

#### Formát hlavičky (bajty 0-39 minimálně)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Parametry SU3 specifické pro Reseed (počáteční zavedení sítě I2P)

U balíčků reseed (doplnění počátečních uzlů) musí mít soubor SU3 následující vlastnosti:

- **File name**: Musí být přesně `i2pseeds.su3`
- **Content Type** (bajt 27): 0x03 (RESEED)
- **File Type** (bajt 25): 0x00 (ZIP)
- **Signature Type** (bajty 8-9): 0x0006 (RSA-4096-SHA512)
- **Version String**: Unixové časové razítko v ASCII (sekundy od epochy, formát date +%s)
- **Signer ID**: ID ve formátu e-mailové adresy odpovídající CN certifikátu X.509

#### Parametr dotazu ID sítě

Od verze 0.9.42 routers připojují k požadavkům na reseed (počáteční stažení seznamu uzlů) parametr `?netid=2`. To brání navazování spojení napříč sítěmi, protože testovací sítě používají odlišná ID sítě. Aktuální produkční síť I2P používá ID sítě 2.

Ukázkový požadavek: `https://reseed.example.com/i2pseeds.su3?netid=2`

### Struktura obsahu archivu ZIP

Sekce obsahu (za hlavičkou, před podpisem) obsahuje standardní archiv ZIP s následujícími požadavky:

- **Komprese**: Standardní komprese ZIP (DEFLATE)
- **Počet souborů**: Obvykle 75–100 souborů RouterInfo (informační soubory routeru)
- **Adresářová struktura**: Všechny soubory musí být na nejvyšší úrovni (bez podadresářů)
- **Pojmenování souborů**: `routerInfo-{44-character-base64-hash}.dat`
- **Abeceda Base64**: Musí používat upravenou abecedu base64 systému I2P

Abeceda I2P base64 se liší od standardní base64 tím, že používá `-` a `~` místo `+` a `/`, aby byla zajištěna kompatibilita se souborovým systémem a adresami URL.

### Kryptografický podpis

Podpis pokrývá celý soubor od bajtu 0 až po konec sekce obsahu. Samotný podpis je připojen za obsah.

#### Algoritmus podpisu (RSA-4096-SHA512)

1. Vypočítejte hash SHA-512 bajtů od bajtu 0 až po konec obsahu
2. Podepište hash pomocí "raw" RSA (v terminologii Javy NONEwithRSA)
3. Je-li to nutné, doplňte podpis počátečními nulami na 512 bajtů
4. K souboru připojte 512bajtový podpis

#### Proces ověřování podpisu

Klienti musí:

1. Přečtěte bajty 0-11 k určení typu a délky podpisu
2. Přečtěte celou hlavičku k určení hranic obsahu
3. Streamujte obsah při výpočtu hashe SHA-512
4. Extrahujte podpis z konce souboru
5. Ověřte podpis pomocí veřejného klíče RSA-4096 podepisujícího
6. Odmítněte soubor, pokud ověření podpisu selže

### Model důvěry certifikátů

Podpisové klíče pro Reseed (úvodní bootstrap sítě) jsou distribuovány jako samopodepsané certifikáty X.509 s klíči RSA-4096. Tyto certifikáty jsou součástí balíčků routeru I2P v adresáři `certificates/reseed/`.

Formát certifikátu: - **Typ klíče**: RSA-4096 - **Podpis**: Samopodepsaný - **Subject CN**: Musí odpovídat ID podepisovatele v hlavičce SU3 - **Data platnosti**: Klienti by měli vynucovat dobu platnosti certifikátu

## Provozování Reseed Host (serveru pro počáteční bootstrap I2P)

Provozování reseed služby (služby, která poskytuje novým routerům počáteční data pro připojení do sítě) vyžaduje pečlivou pozornost věnovanou bezpečnosti, spolehlivosti a požadavkům na různorodost sítě. Více nezávislých reseed serverů zvyšuje odolnost a ztěžuje útočníkům či cenzorům bránit novým routerům v připojení do sítě.

### Technické požadavky

#### Specifikace serveru

- **Operační systém**: Unix/Linux (Ubuntu, Debian, FreeBSD otestované a doporučené)
- **Konektivita**: Statická IPv4 adresa je vyžadována, IPv6 je doporučeno, ale volitelné
- **CPU**: Minimálně 2 jádra
- **RAM**: Minimálně 2 GB
- **Šířka pásma**: Přibližně 15 GB měsíčně
- **Dostupnost**: Vyžadován nepřetržitý provoz 24/7
- **I2P Router**: Dobře integrovaný I2P router běžící nepřetržitě

#### Požadavky na software

- **Java**: JDK 8 nebo novější (Java 17+ bude vyžadována počínaje I2P 2.11.0)
- **Webový server**: nginx nebo Apache s podporou reverzní proxy (Lighttpd již není podporován kvůli omezením hlavičky X-Forwarded-For)
- **TLS/SSL**: Platný certifikát TLS (Let's Encrypt, samopodepsaný nebo od komerční certifikační autority (CA))
- **Ochrana proti DDoS**: fail2ban nebo ekvivalent (povinné, nikoli volitelné)
- **Nástroje pro reseed**: Oficiální reseed-tools z https://i2pgit.org/idk/reseed-tools

### Bezpečnostní požadavky

#### Konfigurace HTTPS/TLS

- **Protokol**: pouze HTTPS, bez nouzového přechodu na HTTP
- **Verze TLS**: minimálně TLS 1.2
- **Sady šifer**: musí podporovat silné šifry kompatibilní s prostředím Java 8+
- **CN/SAN certifikátu**: musí odpovídat názvu hostitele (hostname) obsluhované adresy URL
- **Typ certifikátu**: může být self-signed (vlastnoručně podepsaný), pokud je to domluveno s vývojářským týmem, nebo vydaný uznávanou certifikační autoritou

#### Správa certifikátů

Podpisové certifikáty SU3 a certifikáty TLS slouží k různým účelům:

- **Certifikát TLS** (`certificates/ssl/`): Zabezpečuje HTTPS přenos
- **Certifikát pro podpis SU3** (`certificates/reseed/`): Podepisuje reseed balíčky (pro počáteční zprovoznění sítě)

Oba certifikáty musí být poskytnuty koordinátorovi reseedu (počáteční zavedení do sítě) (zzz@mail.i2p) pro zařazení do balíčků routeru.

#### Ochrana proti DDoS a scrapingu

Reseed servery čelí periodickým útokům ze strany chybných implementací, botnetů i škodlivých aktérů, přičemž cílem je sklízet síťovou databázi (netDb). Mezi ochranná opatření patří:

- **fail2ban**: Vyžadováno pro omezování rychlosti a zmírňování útoků
- **Různorodost balíčků**: Doručovat různé sady RouterInfo (informace o routeru) různým žadatelům
- **Konzistence balíčků**: Doručovat stejný balíček při opakovaných požadavcích ze stejné IP v rámci konfigurovatelného časového okna
- **Omezení logování IP**: Nezveřejňovat logy ani IP adresy (požadavek zásad ochrany soukromí)

### Metody implementace

#### Metoda 1: Oficiální reseed-tools (doporučeno)

Kanonická implementace udržovaná projektem I2P. Repozitář: https://i2pgit.org/idk/reseed-tools

**Instalace**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
Při prvním spuštění nástroj vygeneruje: - `your-email@mail.i2p.crt` (podpisový certifikát SU3) - `your-email@mail.i2p.pem` (soukromý klíč pro podepisování SU3) - `your-email@mail.i2p.crl` (seznam odvolaných certifikátů) - soubory s TLS certifikátem a klíčem

**Funkce**: - Automatické generování SU3 bundle (aktualizačního balíčku I2P) (350 variant, každá s 77 RouterInfo) - Vestavěný HTTPS server - Obnovovat mezipaměť každých 9 hodin pomocí plánovače cron - Podpora hlavičky X-Forwarded-For s přepínačem `--trustProxy` - Kompatibilní s konfiguracemi reverse proxy

**Produkční nasazení**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Metoda 2: Implementace v Pythonu (pyseeder)

Alternativní implementace od projektu PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Metoda 3: Nasazení pomocí Dockeru

Pro kontejnerová prostředí existuje několik implementací připravených pro Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Přidává Tor onion službu a podporu pro IPFS

### Konfigurace reverzní proxy

#### Konfigurace nginxu

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Konfigurace Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Registrace a koordinace

Chcete-li zahrnout svůj reseed server (server pro počáteční získání informací o síti) do oficiálního balíčku I2P:

1. Dokončete nastavení a testování
2. Zašlete oba certifikáty (SU3 signing a TLS) koordinátorovi reseedu
3. Kontakt: zzz@mail.i2p nebo zzz@i2pmail.org
4. Připojte se do #i2p-dev na IRC2P pro koordinaci s ostatními operátory

### Provozní osvědčené postupy

#### Monitoring a logování

- Povolit kombinovaný formát logů Apache/nginx pro statistiky
- Zavést rotaci logů (logy rychle rostou)
- Sledovat úspěšnost generování balíčků a časy znovusestavení
- Sledovat využití šířky pásma a vzorce požadavků
- Nikdy nezveřejňovat IP adresy ani podrobné přístupové logy

#### Harmonogram údržby

- **Každých 9 hodin**: Přestavět mezipaměť balíčku SU3 (automatizováno pomocí cron)
- **Týdně**: Kontrolovat logy kvůli vzorcům útoků
- **Měsíčně**: Aktualizovat I2P router a reseed-tools
- **Podle potřeby**: Obnovit TLS certifikáty (automatizovat pomocí Let's Encrypt)

#### Výběr portu

- Výchozí: 8443 (doporučeno)
- Alternativa: Libovolný port v rozsahu 1024-49151
- Port 443: Vyžaduje práva roota nebo přesměrování portu (doporučeno přesměrování pomocí iptables)

Příklad přesměrování portů:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Alternativní metody reseedu (počátečního naplnění netDb)

Další možnosti bootstrapu (počátečního zavádění) pomáhají uživatelům v restriktivních sítích:

### Reseed ze souboru (počáteční načtení uzlů)

Zavedeno ve verzi 0.9.16, reseed (počáteční naplnění netDb) založený na souborech umožňuje uživatelům ručně načítat balíčky RouterInfo (informace o routeru). Tato metoda je obzvlášť užitečná pro uživatele v cenzurovaných regionech, kde jsou blokovány HTTPS reseed servery.

**Postup**: 1. Důvěryhodný kontakt vygeneruje balíček SU3 pomocí svého routeru 2. Balíček je předán e-mailem, přes USB disk nebo jiným out-of-band kanálem (oddělený kanál mimo běžné spojení) 3. Uživatel umístí `i2pseeds.su3` do konfiguračního adresáře I2P 4. Router po restartu balíček automaticky rozpozná a zpracuje

**Dokumentace**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Případy použití**: - Uživatelé za národními firewally blokujícími reseed servers (servery pro počáteční inicializaci sítě) - Izolované sítě vyžadující ruční bootstrap (počáteční inicializaci sítě) - Testovací a vývojová prostředí

### Reseeding (úvodní získání seznamu uzlů) přes proxy Cloudflare

Směrování provozu reseed (stažení počátečních informací o uzlech) přes CDN společnosti Cloudflare přináší pro provozovatele v regionech s vysokou mírou cenzury několik výhod.

**Výhody**: - IP adresa původního serveru skryta před klienty - Ochrana proti DDoS prostřednictvím infrastruktury Cloudflare - Geografická distribuce zátěže pomocí edge cachingu (kešování na okraji sítě) - Lepší výkon pro klienty po celém světě

**Požadavky na implementaci**: - přepínač `--trustProxy` povolen v reseed-tools - Cloudflare proxy povoleno pro DNS záznam - Správné zpracování hlavičky X-Forwarded-For

**Důležité poznámky**: - Platí omezení portů Cloudflare (je nutné použít podporované porty) - Konzistence balíčku pro stejného klienta vyžaduje podporu X-Forwarded-For - Konfiguraci SSL/TLS spravuje Cloudflare

**Dokumentace**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Strategie odolné vůči cenzuře

Výzkum Nguyen Phong Hoanga (USENIX FOCI 2019) identifikuje další inicializační metody pro cenzurované sítě:

#### Poskytovatelé cloudového úložiště

- **Box, Dropbox, Google Drive, OneDrive**: Hostovat soubory SU3 na veřejných odkazech
- **Výhoda**: Obtížné blokovat bez narušení legitimních služeb
- **Omezení**: Vyžaduje ruční distribuci adres URL uživatelům

#### Distribuce IPFS (decentralizovaný souborový systém)

- Hostovat balíčky pro reseed (počáteční zavedení sítě) na InterPlanetary File System
- Obsahově adresované úložiště zabraňuje pozměňování
- Odolné vůči pokusům o stažení z provozu

#### Onion služby Toru

- Reseed servery (servery pro počáteční načtení informací o uzlech) přístupné přes adresy .onion
- Odolné vůči blokování na základě IP adresy
- Vyžaduje klienta Tor v systému uživatele

**Výzkumná dokumentace**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Země se známým blokováním I2P

K roku 2025 je potvrzeno, že následující země blokují I2P reseed servery (servery pro počáteční stažení informací o síti): - Čína - Írán - Omán - Katar - Kuvajt

Uživatelé v těchto regionech by měli využívat alternativní metody bootstrapu nebo cenzuře odolné strategie reseedingu (počáteční stažení kontaktů do sítě).

## Podrobnosti protokolu pro implementátory

### Specifikace požadavku na reseed (počáteční zavedení do sítě I2P)

#### Chování klienta

1. **Výběr serveru**: Router udržuje pevně zakódovaný seznam URL pro reseed
2. **Náhodný výběr**: Klient náhodně vybírá server z dostupného seznamu
3. **Formát požadavku**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Měl by napodobovat běžné prohlížeče (např. "Wget/1.11.4")
5. **Logika opakování**: Pokud požadavek na SU3 selže, přejde se k parsování indexové stránky
6. **Ověření certifikátu**: Ověřit certifikát TLS vůči systémovému úložišti důvěryhodných certifikátů
7. **Ověření podpisu SU3**: Ověřit podpis vůči známým certifikátům pro reseed

#### Chování serveru

1. **Výběr balíčku**: Vybrat pseudonáhodnou podmnožinu RouterInfos (záznamy o I2P routerech) z netDb
2. **Sledování klientů**: Identifikovat požadavky podle zdrojové IP adresy (s ohledem na X-Forwarded-For)
3. **Konzistence balíčku**: Vrátit stejný balíček pro opakované požadavky v časovém okně (typicky 8-12 hodin)
4. **Různorodost balíčků**: Vrátit různé balíčky různým klientům pro rozmanitost sítě
5. **Content-Type**: `application/octet-stream` nebo `application/x-i2p-reseed`

### Formát souboru RouterInfo

Každý soubor `.dat` v balíčku reseed (počáteční naplnění netDb) obsahuje strukturu RouterInfo:

**Pojmenování souborů**: `routerInfo-{base64-hash}.dat` - Hash má 44 znaků a používá abecedu I2P Base64 - Příklad: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Obsah souboru**: - RouterIdentity (hash routeru, šifrovací klíč, podpisový klíč) - Časové razítko publikace - Adresy routeru (IP, port, typ transportu) - Schopnosti a volby routeru - Podpis pokrývající všechna výše uvedená data

### Požadavky na diverzitu sítě

Za účelem prevence centralizace sítě a umožnění detekce útoků Sybil:

- **Žádné úplné výpisy NetDb**: Nikdy neposkytujte všechny RouterInfo (informace o routeru) jedinému klientovi
- **Náhodný výběr**: Každý balíček obsahuje odlišnou podmnožinu dostupných uzlů
- **Minimální velikost balíčku**: 75 záznamů RouterInfo (zvýšeno z původních 50)
- **Maximální velikost balíčku**: 100 záznamů RouterInfo
- **Aktuálnost**: RouterInfo by měly být aktuální (do 24 hodin od vytvoření)

### Úvahy o IPv6

**Aktuální stav** (2025): - Několik reseed serverů (servery pro počáteční připojení do sítě) je přes IPv6 nedostupných - Klienti by kvůli spolehlivosti měli upřednostnit nebo vynutit IPv4 - Podpora IPv6 je pro nová nasazení doporučená, ale není kritická

**Poznámka k implementaci**: Při konfiguraci dual-stackových serverů zajistěte, aby obě naslouchací adresy IPv4 i IPv6 fungovaly správně, nebo IPv6 zakažte, pokud jej nelze řádně podporovat.

## Bezpečnostní hlediska

### Model hrozeb

Protokol reseed (počáteční bootstrap sítě I2P) chrání proti:

1. **Útoky typu man-in-the-middle**: Podpisy RSA-4096 zabraňují manipulaci s balíčkem
2. **Rozdělení sítě**: Více nezávislých reseed serverů (servery pro počáteční získání seznamu uzlů) zabraňuje jedinému bodu kontroly
3. **Útoky typu Sybil**: Různorodost balíčků omezuje schopnost útočníka izolovat uživatele
4. **Cenzura**: Více serverů a alternativní metody poskytují redundanci

reseed protocol (mechanismus pro získání počátečních routerů) NEchrání proti:

1. **Kompromitované reseed servery (reseed = počáteční bootstrap do sítě)**: Pokud útočník ovládá soukromé klíče k reseed certifikátům
2. **Úplné blokování sítě**: Pokud jsou v regionu zablokovány všechny metody reseed
3. **Dlouhodobé sledování**: Žádosti o reseed odhalují IP adresu pokoušející se připojit k I2P

### Správa certifikátů

**Zabezpečení soukromých klíčů**: - Uchovávejte SU3 podpisové klíče offline, když se nepoužívají - Používejte silná hesla pro šifrování klíčů - Zajišťujte bezpečné zálohy klíčů a certifikátů - Zvažte hardwarové bezpečnostní moduly (HSM) pro nasazení s vysokou hodnotou

**Odvolání certifikátů**: - Seznamy odvolaných certifikátů (CRLs) distribuované přes informační kanál - Kompromitované certifikáty může odvolat koordinátor - Routers automaticky aktualizují CRLs v rámci aktualizací softwaru

### Zmírnění útoků

**Ochrana proti DDoS**: - pravidla fail2ban pro nadměrné požadavky - omezování počtu požadavků na úrovni webového serveru - omezení počtu připojení na IP adresu - Cloudflare nebo podobné CDN pro další vrstvu

**Prevence scrapingu**: - Různé balíčky pro každou zdrojovou IP adresu - Časově řízené ukládání balíčků do mezipaměti podle IP - Logování vzorců naznačujících pokusy o scraping - Koordinace s ostatními operátory ohledně detekovaných útoků

## Testování a ověřování

### Testování vašeho Reseed Serveru (serveru pro počáteční naplnění netDb při bootstrapu)

#### Metoda 1: Čistá instalace routeru

1. Nainstalujte I2P na čistý systém
2. Přidejte svůj reseed URL (odkaz pro počáteční stažení seznamu uzlů) do konfigurace
3. Odstraňte nebo zakažte ostatní reseed URL
4. Spusťte router a sledujte logy kvůli úspěšnému reseedu
5. Ověřte připojení k síti do 5-10 minut

Očekávaný výstup logu:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Metoda 2: Ruční ověření SU3 (souborový formát podepsaných aktualizací I2P)

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Metoda 3: checki2p Monitoring

Služba na adrese https://checki2p.com/reseed provádí automatizované kontroly každé 4 hodiny u všech registrovaných I2P reseed serverů (reseed: počáteční stažení seznamu peerů pro připojení k síti). To poskytuje:

- Monitorování dostupnosti
- Metriky doby odezvy
- Ověření certifikátu TLS
- Ověření podpisu SU3
- Historická data o době provozu

Jakmile bude váš reseed (server pro počáteční připojení k síti I2P) zaregistrován u projektu I2P, automaticky se do 24 hodin objeví na checki2p.

### Odstraňování běžných problémů

**Problém**: "Unable to read signing key" při prvním spuštění - **Řešení**: To je očekávané. Zadejte 'y' pro vygenerování nových klíčů.

**Problém**: Router nedokáže ověřit podpis - **Příčina**: Certifikát není v důvěryhodném úložišti routeru - **Řešení**: Umístěte certifikát do adresáře `~/.i2p/certificates/reseed/`

**Problém**: Stejný balíček je doručován různým klientům - **Příčina**: Hlavička X-Forwarded-For není správně předávána - **Řešení**: Povolte `--trustProxy` a nakonfigurujte hlavičky reverzní proxy

**Problém**: chyby "Connection refused" - **Příčina**: Port není přístupný z internetu - **Řešení**: Zkontrolujte pravidla firewallu, ověřte přesměrování portů

**Problém**: Vysoké využití CPU během znovusestavování balíčku - **Příčina**: Normální chování při generování 350+ variant SU3 (formát podepsaných aktualizačních balíčků v I2P) - **Řešení**: Zajistěte dostatečný výkon CPU, zvažte snížení frekvence znovusestavování

## Referenční informace

### Oficiální dokumentace

- **Příručka pro přispěvatele k Reseed (počáteční zavedení klienta I2P stažením výchozích uzlů)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Požadavky na zásady Reseed**: /guides/reseed-policy/
- **Specifikace SU3**: /docs/specs/updates/
- **Repozitář nástrojů pro Reseed**: https://i2pgit.org/idk/reseed-tools
- **Dokumentace k nástrojům pro Reseed**: https://eyedeekay.github.io/reseed-tools/

### Alternativní implementace

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python WSGI reseeder**: https://github.com/torbjo/i2p-reseeder

### Komunitní zdroje

- **I2P fórum**: https://i2pforum.net/
- **Repozitář Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev na IRC2P
- **Monitorování stavu**: https://checki2p.com/reseed

### Historie verzí

- **0.9.14** (2014): Zaveden formát SU3 pro reseedování
- **0.9.16** (2014): Přidáno reseedování ze souborů
- **0.9.42** (2019): Vyžadován parametr dotazu Network ID
- **2.0.0** (2022): Zaveden transportní protokol SSU2
- **2.4.0** (2024): Izolace NetDB a vylepšení zabezpečení
- **2.6.0** (2024): Zablokována připojení I2P-over-Tor
- **2.10.0** (2025): Aktuální stabilní vydání (k září 2025)

### Referenční přehled typů podpisů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Reseed Standard (standard pro reseed)**: Typ 6 (RSA-SHA512-4096) je vyžadován pro balíčky reseedu.

## Poděkování

Díky všem provozovatelům reseedu za to, že udržují síť přístupnou a odolnou. Zvláštní poděkování následujícím přispěvatelům a projektům:

- **zzz**: Dlouholetý vývojář I2P a koordinátor reseedu (počáteční získání netDb z veřejných serverů)
- **idk**: Současný správce reseed-tools a správce vydání
- **Nguyen Phong Hoang**: Výzkum strategií reseedu odolných vůči cenzuře
- **PurpleI2P Team**: Alternativní implementace I2P a nástroje
- **checki2p**: Automatizovaná monitorovací služba pro infrastrukturu reseedu

Decentralizovaná infrastruktura reseed (počátečního zavedení do sítě) sítě I2P představuje společné úsilí desítek provozovatelů po celém světě a zajišťuje, že noví uživatelé vždy najdou cestu, jak se k síti připojit, bez ohledu na místní cenzuru či technické překážky.
