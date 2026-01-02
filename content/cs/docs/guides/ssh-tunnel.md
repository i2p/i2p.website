---
title: "Vytvoření SSH tunelu pro vzdálený přístup k I2P"
description: "Naučte se, jak vytvořit zabezpečené SSH tunely na Windows, Linux a Mac pro přístup ke vzdálenému I2P routeru"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SSH tunel poskytuje bezpečné, šifrované spojení pro přístup ke konzoli vašeho vzdáleného I2P routeru nebo k dalším službám. Tato příručka vám ukáže, jak vytvořit SSH tunely na systémech Windows, Linux a Mac.

## Co je SSH tunel?

SSH tunel je metoda směrování dat a informací bezpečně přes šifrované SSH spojení. Představte si to jako vytvoření chráněného "potrubí" přes internet - vaše data cestují tímto šifrovaným tunelem, což zabraňuje komukoli je cestou zachytit nebo přečíst.

SSH tunelování je zvláště užitečné pro:

- **Přístup ke vzdáleným I2P routerům**: Připojte se ke konzoli I2P běžící na vzdáleném serveru
- **Zabezpečená spojení**: Veškerý provoz je šifrován end-to-end
- **Obcházení omezení**: Přistupujte ke službám na vzdálených systémech, jako by byly lokální
- **Přesměrování portů**: Namapujte lokální port na vzdálenou službu

V kontextu I2P můžete použít SSH tunel pro přístup ke konzoli vašeho I2P routeru (typicky na portu 7657) na vzdáleném serveru tak, že ji přesměrujete na lokální port na vašem počítači.

## Předpoklady

Před vytvořením SSH tunelu budete potřebovat:

- **SSH klient**:
  - Windows: [PuTTY](https://www.putty.org/) (ke stažení zdarma)
  - Linux/Mac: Vestavěný SSH klient (přes Terminál)
- **Přístup ke vzdálenému serveru**:
  - Uživatelské jméno pro vzdálený server
  - IP adresa nebo hostname vzdáleného serveru
  - SSH heslo nebo autentizace pomocí klíče
- **Dostupný lokální port**: Zvolte nepoužívaný port v rozsahu 1-65535 (pro I2P se běžně používá 7657)

## Pochopení příkazu Tunnel

Příkaz pro SSH tunel se řídí tímto vzorem:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Vysvětlení parametrů**: - **local_port**: Port na vašem lokálním počítači (např. 7657) - **destination_ip**: Obvykle `127.0.0.1` (localhost na vzdáleném serveru) - **destination_port**: Port služby na vzdáleném serveru (např. 7657 pro I2P) - **username**: Vaše uživatelské jméno na vzdáleném serveru - **remote_server**: IP adresa nebo hostname vzdáleného serveru

**Příklad**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Toto vytvoří tunel, kde: - Lokální port 7657 na vašem počítači přeposílá na... - Port 7657 na localhost vzdáleného serveru (kde běží I2P) - Připojení jako uživatel `i2p` na server `20.228.143.58`

## Vytvoření SSH tunelů ve Windows

Uživatelé Windows mohou vytvářet SSH tunely pomocí PuTTY, bezplatného SSH klienta.

### Step 1: Download and Install PuTTY

Stáhněte si PuTTY z [putty.org](https://www.putty.org/) a nainstalujte ho do vašeho systému Windows.

### Step 2: Configure the SSH Connection

Otevřete PuTTY a nakonfigurujte své připojení:

1. V kategorii **Session**:
   - Zadejte IP adresu nebo hostname vašeho vzdáleného serveru do pole **Host Name**
   - Ujistěte se, že **Port** je nastaven na 22 (výchozí SSH port)
   - Typ připojení by měl být **SSH**

![Konfigurace relace PuTTY](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Přejděte na **Connection → SSH → Tunnels** v levém postranním panelu:

1. **Zdrojový port**: Zadejte lokální port, který chcete použít (např. `7657`)
2. **Cíl**: Zadejte `127.0.0.1:7657` (localhost:port na vzdáleném serveru)
3. Klikněte na **Přidat** pro přidání tunelu
4. Tunel by se měl objevit v seznamu "Přesměrované porty"

![Konfigurace PuTTY tunnelu](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Klikněte na **Open** pro zahájení připojení
2. Pokud se připojujete poprvé, zobrazí se bezpečnostní upozornění - klikněte na **Yes** pro důvěru serveru
3. Zadejte své uživatelské jméno, když budete vyzváni
4. Zadejte své heslo, když budete vyzváni

![PuTTY připojení navázáno](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Po připojení můžete přistupovat ke své vzdálené konzoli I2P otevřením prohlížeče a navigací na adresu `http://127.0.0.1:7657`

### Krok 1: Stažení a instalace PuTTY

Abyste se vyhnuli opětovné konfiguraci pokaždé:

1. Vraťte se do kategorie **Session**
2. Zadejte název do pole **Saved Sessions** (např. "I2P Tunnel")
3. Klikněte na **Save**
4. Příště stačí načíst tuto relaci a kliknout na **Open**

## Creating SSH Tunnels on Linux

Linuxové systémy mají SSH zabudované v terminálu, což činí vytváření tunelů rychlým a přímočarým.

### Krok 2: Konfigurace SSH připojení

Otevřete terminál a spusťte příkaz SSH tunelu:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Nahraďte**: - `7657` (první výskyt): Požadovaný místní port - `127.0.0.1:7657`: Cílová adresa a port na vzdáleném serveru - `i2p`: Vaše uživatelské jméno na vzdáleném serveru - `20.228.143.58`: IP adresa vašeho vzdáleného serveru

![Vytvoření SSH tunelu v Linuxu](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Když budete vyzváni, zadejte své heslo. Po připojení je tunel aktivní.

Přístup ke vzdálené I2P konzoli získáte v prohlížeči na adrese `http://127.0.0.1:7657`.

### Krok 3: Konfigurace tunelu

Tunel zůstává aktivní po celou dobu běhu SSH relace. Pro udržení běhu na pozadí:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Dodatečné příznaky**: - `-f`: Spustí SSH na pozadí - `-N`: Nespouštět vzdálené příkazy (pouze tunel)

Pro uzavření tunelu na pozadí najděte a ukončete SSH proces:

```bash
ps aux | grep ssh
kill [process_id]
```
### Krok 4: Připojení

Pro lepší zabezpečení a pohodlí použijte autentizaci pomocí SSH klíčů:

1. Vygenerujte pár SSH klíčů (pokud ho ještě nemáte):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Zkopírujte svůj veřejný klíč na vzdálený server:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Nyní se můžete připojit bez hesla:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Systémy Mac používají stejného SSH klienta jako Linux, takže proces je identický.

### Volitelné: Uložte si svou relaci

Otevřete Terminál (Aplikace → Utility → Terminál) a spusťte:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Nahraďte**: - `7657` (první výskyt): Váš požadovaný lokální port - `127.0.0.1:7657`: Cílová adresa a port na vzdáleném serveru - `i2p`: Vaše uživatelské jméno na vzdáleném serveru - `20.228.143.58`: IP adresa vašeho vzdáleného serveru

![Mac SSH tunnel creation](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Zadejte heslo, když budete vyzváni. Po připojení přistupujte ke své vzdálené konzoli I2P na adrese `http://127.0.0.1:7657`

### Background Tunnels on Mac

Stejně jako na Linuxu můžete tunel spustit na pozadí:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Používání terminálu

Nastavení SSH klíče na Macu je identické s Linuxem:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Udržování tunelu aktivního

Nejčastější případ použití - přístup ke konzoli vašeho vzdáleného I2P routeru:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Poté otevřete `http://127.0.0.1:7657` ve vašem prohlížeči.

### Použití SSH klíčů (doporučeno)

Přeposílání více portů najednou:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Toto přeposílá jak port 7657 (I2P konzole), tak 7658 (další službu).

### Custom Local Port

Použijte jiný lokální port, pokud je 7657 již používán:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Místo toho přistupujte ke konzoli I2P na `http://127.0.0.1:8080`.

## Troubleshooting

### Používání terminálu

**Chyba**: "bind: Address already in use"

**Řešení**: Zvolte jiný lokální port nebo ukončete proces, který tento port používá:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Tunely na pozadí na Macu

**Chyba**: "Connection refused" nebo "channel 2: open failed"

**Možné příčiny**: - Vzdálená služba není spuštěna (zkontrolujte, zda běží I2P router na vzdáleném serveru) - Firewall blokuje připojení - Nesprávný cílový port

**Řešení**: Ověřte, že I2P router běží na vzdáleném serveru:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Nastavení SSH klíčů na Macu

**Chyba**: "Permission denied" nebo "Authentication failed"

**Možné příčiny**: - Nesprávné uživatelské jméno nebo heslo - SSH klíč není správně nakonfigurován - SSH přístup je na vzdáleném serveru zakázán

**Řešení**: Ověřte přihlašovací údaje a ujistěte se, že je na vzdáleném serveru povolen SSH přístup.

### Tunnel Drops Connection

**Chyba**: Připojení se odpojí po období nečinnosti

**Řešení**: Přidejte nastavení keep-alive do vaší SSH konfigurace (`~/.ssh/config`):

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **Používejte SSH klíče**: Bezpečnější než hesla, obtížněji kompromitovatelné
- **Zakažte autentizaci heslem**: Jakmile jsou SSH klíče nastaveny, zakažte přihlašování heslem na serveru
- **Používejte silná hesla**: Pokud používáte autentizaci heslem, použijte silné, jedinečné heslo
- **Omezte SSH přístup**: Nakonfigurujte pravidla firewallu pro omezení SSH přístupu na důvěryhodné IP adresy
- **Udržujte SSH aktualizované**: Pravidelně aktualizujte svůj SSH klient a serverový software
- **Monitorujte logy**: Kontrolujte SSH logy na serveru kvůli podezřelé aktivitě
- **Používejte nestandardní SSH porty**: Změňte výchozí SSH port (22) pro snížení automatizovaných útoků

## Vytváření SSH tunelů v Linuxu

### Přístup k I2P konzoli

Vytvořte skript pro automatické vytvoření tunelů:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Udělejte jej spustitelným:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Více Tunelů

Vytvořte systemd službu pro automatické vytváření tunelů:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Přidat:

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
Povolit a spustit:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Vlastní lokální port

Vytvořte SOCKS proxy pro dynamické přesměrování:

```bash
ssh -D 8080 user@remote-server
```
Nakonfigurujte svůj prohlížeč tak, aby používal `127.0.0.1:8080` jako SOCKS5 proxy.

### Reverse Tunneling

Povolit vzdálenému serveru přístup ke službám na vašem lokálním počítači:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Port je již používán

Tunelování přes mezilehlý server:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

SSH tunelování je mocný nástroj pro bezpečný přístup ke vzdáleným I2P routerům a dalším službám. Ať už používáte Windows, Linux nebo Mac, proces je přímočarý a poskytuje silné šifrování pro vaše připojení.

Pro další pomoc nebo dotazy navštivte komunitu I2P: - **Fórum**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p na různých sítích - **Dokumentace**: [I2P Docs](/docs/)

---

 NEKLASTE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá neúplný, přeložte jej tak, jak je.

*Průvodce původně vytvořený [Stormy Cloud](https://www.stormycloud.org), upravený pro dokumentaci I2P.*
