---
title: "IRC přes I2P"
description: "Kompletní průvodce I2P IRC sítěmi, klienty, tunely a nastavením serveru (aktualizováno 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

**Klíčové body**

- I2P poskytuje **end-to-end šifrování** pro IRC provoz skrze své tunely. **Vypněte SSL/TLS** v IRC klientech, pokud nepoužíváte outproxy do clearnetu.
- Předkonfigurovaný **Irc2P** klientský tunel poslouchá na **127.0.0.1:6668** ve výchozím nastavení. Připojte svého IRC klienta na tuto adresu a port.
- Nepoužívejte termín "router‑provided TLS." Používejte "nativní šifrování I2P" nebo "end‑to‑end šifrování."

## Rychlý start (Java I2P)

1. Otevřete **Hidden Services Manager** na adrese `http://127.0.0.1:7657/i2ptunnel/` a ujistěte se, že tunel **Irc2P** je **spuštěný**.
2. Ve svém IRC klientovi nastavte **server** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **vypnuto**.
3. Připojte se a vstupte do kanálů jako `#i2p`, `#i2p-dev`, `#i2p-help`.

Pro uživatele **i2pd** (router v C++), vytvořte klientský tunnel v souboru `tunnels.conf` (viz příklady níže).

## Sítě a servery

### IRC2P (main community network)

- Federované servery: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- Tunel **Irc2P** na `127.0.0.1:6668` se připojuje k jednomu z těchto serverů automaticky.
- Typické kanály: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Servery: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Primární jazyky: ruština a angličtina. Na některých hostitelích existují webová rozhraní.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminál)** — silná podpora SOCKS; snadné skriptování.
- **Pidgin (desktop)** — stále udržovaný; dobře funguje pro Windows/Linux.
- **Thunderbird Chat (desktop)** — podporováno v ESR 128+.
- **The Lounge (self‑hosted web)** — moderní webový klient.

### IRC2P (hlavní komunitní síť)

- **LimeChat** (zdarma, open source).
- **Textual** (placená v App Store; zdrojový kód dostupný ke kompilaci).

### Síť Ilita

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protokol: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- Šifrování: **vypnuto**
- Uživatelské jméno/přezdívka: libovolné

#### Thunderbird Chat

- Typ účtu: **IRC**
- Server: **127.0.0.1**
- Port: **6668**
- SSL/TLS: **vypnuto**
- Volitelné: automatické připojení ke kanálům při navázání spojení

#### Dispatch (SAM v3)

Příklad výchozích hodnot `config.toml`:

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

- Irc2P klientský tunel: **127.0.0.1:6668** → upstream server na **portu 6667**.
- Hidden Services Manager: `http://127.0.0.1:7657/i2ptunnel/`.

### Doporučené, aktivně udržované

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
Samostatný tunel pro Ilitu (příklad):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### Možnosti pro macOS

- **Povolit SAM** v Java I2P (ve výchozím nastavení vypnuto) na `/configclients` nebo `clients.config`.
- Výchozí hodnoty: **127.0.0.1:7656/TCP** a **127.0.0.1:7655/UDP**.
- Doporučená kryptografie: `SIGNATURE_TYPE=7` (Ed25519) a `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 s ElGamal fallbackem) nebo pouze `4` pro výhradně moderní.

### Příklady konfigurací

- Java I2P výchozí: **2 příchozí / 2 odchozí**.
- i2pd výchozí: **5 příchozích / 5 odchozích**.
- Pro IRC: **2–3 každý** je dostačující; nastavte explicitně pro konzistentní chování napříč routery.

## Nastavení klienta

- **Nepovolujte SSL/TLS** pro interní I2P IRC připojení. I2P již poskytuje end‑to‑end šifrování. Dodatečné TLS přidává režii bez přínosu pro anonymitu.
- Používejte **trvalé klíče** pro stabilní identitu; vyhněte se opětovnému generování klíčů při každém restartu, pokud netestujete.
- Pokud více aplikací používá IRC, preferujte **samostatné tunnely** (nesdílené), abyste snížili korelaci mezi službami.
- Pokud musíte povolit vzdálené ovládání (SAM/I2CP), svažte na localhost a zabezpečte přístup pomocí SSH tunnelů nebo autentizovaných reverse proxy.

## Alternative connection method: SOCKS5

Někteří klienti se mohou připojit přes I2P SOCKS5 proxy: **127.0.0.1:4447**. Pro nejlepší výsledky preferujte dedikovaný IRC client tunnel na portu 6668; SOCKS nemůže sanitizovat identifikátory aplikační vrstvy a může uniklé informace, pokud klient není navržen pro anonymitu.

## Troubleshooting

- **Nelze se připojit** — ujistěte se, že tunel Irc2P běží a router je plně zabootstrapován.
- **Zamrzne při resolve/join** — znovu zkontrolujte, že SSL je **vypnuto** a klient směřuje na **127.0.0.1:6668**.
- **Vysoká latence** — I2P má záměrně vyšší latenci. Udržujte počet tunelů rozumný (2–3) a vyhněte se rychlým smyčkám opětovného připojení.
- **Používání SAM aplikací** — potvrďte, že SAM je povolen (Java) nebo není blokován firewallem (i2pd). Dlouhodobé relace jsou doporučeny.

## Appendix: Ports and naming

- Běžné porty IRC tunelů: **6668** (výchozí pro Irc2P), **6667** a **6669** jako alternativy.
- `.b32.i2p` hostnames: standardní forma 52 znaků; existují rozšířené formy s 56+ znaky pro LS2/pokročilé certifikáty. Používejte `.i2p` hostnames, pokud výslovně nepotřebujete b32 adresy.
