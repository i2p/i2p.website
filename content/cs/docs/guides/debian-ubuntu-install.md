---
title: "Instalace I2P na Debianu a Ubuntu"
aliases:
  - "/cs/debian"
  - "/cs/debian/"
description: "Kompletní průvodce instalací I2P na Debian, Ubuntu a jejich derivátech pomocí oficiálních repozitářů"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Projekt I2P udržuje oficiální balíčky pro Debian, Ubuntu a jejich odvozené distribuce. Tento průvodce poskytuje komplexní pokyny pro instalaci I2P pomocí našich oficiálních repozitářů.

---

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
NEPOKLÁDEJTE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá být neúplný, přeložte ho tak, jak je.

## Podporované platformy

---

- **Ubuntu** 18.04 (Bionic) a novější
- **Linux Mint** 19 (Tara) a novější
- **Debian** Buster (10) a novější
- **Knoppix**
- Další distribuce založené na Debianu (LMDE, ParrotOS, Kali Linux atd.)

NEKLADEŤE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá neúplný, přeložte jej tak, jak je.

Balíčky pro Debian jsou kompatibilní s:

## Metody instalace

**Podporované architektury**: amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

- **Možnost 1**: [Ubuntu a odvozeniny](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, atd.)
- **Možnost 2**: [Debian a distribuce založené na Debianu](#debian-installation) (včetně LMDE, Kali, ParrotOS)

Balíčky I2P mohou fungovat i na jiných systémech založených na Debianu, které nejsou výslovně uvedeny výše. Pokud narazíte na problémy, prosím [nahlaste je na našem GitLabu](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Instalace na Ubuntu

Vyberte způsob instalace, který odpovídá vaší distribuci:

### Method 1: Command Line Installation (Recommended)

---

NEPOKLÁDEJTE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá být neúplný, přeložte jej tak, jak je.

Ubuntu a jeho oficiální deriváty (Linux Mint, elementary OS, Trisquel atd.) mohou využít I2P PPA (Personal Package Archive) pro snadnou instalaci a automatické aktualizace.

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Toto je nejrychlejší a nejspolehlivější metoda pro instalaci I2P na systémech založených na Ubuntu.

**Krok 1: Přidání I2P PPA**

Otevřete terminál a spusťte:

```bash
sudo apt-get update
```
Tento příkaz přidá I2P PPA do `/etc/apt/sources.list.d/` a automaticky importuje GPG klíč, který podepisuje repozitář. GPG podpis zajišťuje, že balíčky nebyly od jejich sestavení změněny.

**Krok 2: Aktualizace seznamu balíčků**

Aktualizujte databázi balíčků vašeho systému, aby zahrnovala nové PPA:

```bash
sudo apt-get install i2p
```
Toto stáhne nejnovější informace o balíčcích ze všech povolených repozitářů, včetně PPA I2P, které jste právě přidali.

### Method 2: Using the Software Center GUI

**Krok 3: Instalace I2P**

Nyní nainstalujte I2P:

To je vše! Přeskočte do sekce [Konfigurace po instalaci](#post-installation-configuration), kde se dozvíte, jak spustit a nastavit I2P.

Pokud upřednostňujete grafické rozhraní, můžete přidat PPA pomocí Ubuntu Software Center.

**Krok 1: Otevřete Software a aktualizace**

Spusťte "Software a aktualizace" z nabídky aplikací.

![Menu Software Center](/images/guides/debian/software-center-menu.png)

**Krok 2: Přejděte do sekce Další software**

Vyberte záložku "Other Software" a klikněte na tlačítko "Add" ve spodní části pro konfiguraci nového PPA.

```
ppa:i2p-maintainers/i2p
```
![Záložka Další software](/images/guides/debian/software-center-addother.png)

**Krok 3: Přidání I2P PPA**

V dialogovém okně PPA zadejte:

![Dialogové okno Přidat PPA](/images/guides/debian/software-center-ppatool.png)

**Krok 4: Obnovit informace o repozitáři**

Klikněte na tlačítko „Reload" pro stažení aktualizovaných informací z repozitáře.

![Tlačítko Obnovit](/images/guides/debian/software-center-reload.png)

**Krok 5: Instalace I2P**

Otevřete aplikaci „Software" z nabídky aplikací, vyhledejte „i2p" a klikněte na Instalovat.

## Klíčové vlastnosti

![Softwarová aplikace](/images/guides/debian/software-center-software.png)

### Important Notice

Po dokončení instalace pokračujte na [Konfiguraci po instalaci](#post-installation-configuration).

### Prerequisites

I2P je **decentralizovaná síť pro anonymní komunikaci**, která šifruje a směruje provoz přes dobrovolníky provozující routery po celém světě.

### Metoda 1: Instalace z příkazové řádky (doporučeno)

I2P používá **tunnely** pro odesílání a přijímání provozu. Každý tunnel prochází několika routery, přičemž každý router zná pouze předchozí a následující hop. To vytváří **vrstvenou anonymitu** podobnou Tor, ale s důležitými rozdíly:

Debian a jeho downstream distribuce (LMDE, Kali Linux, ParrotOS, Knoppix atd.) by měly používat oficiální I2P Debian repozitář na `deb.i2p.net`.

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
**Naše staré repozitáře na `deb.i2p2.de` a `deb.i2p2.no` již nejsou podporovány.** Pokud používáte tyto zastaralé repozitáře, postupujte prosím podle níže uvedených pokynů pro migraci na nový repozitář na `deb.i2p.net`.

Všechny níže uvedené kroky vyžadují root přístup. Buď přepněte na uživatele root pomocí `su`, nebo před každý příkaz přidejte `sudo`.

**Krok 1: Nainstalujte požadované balíčky**

```bash
cat /etc/debian_version
```
Ujistěte se, že máte nainstalované potřebné nástroje:

Tyto balíčky umožňují bezpečný HTTPS přístup k repozitáři, detekci distribuce a stahování souborů.

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Krok 2: Přidejte repozitář I2P**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Příkaz, který použijete, závisí na vaší verzi Debianu. Nejprve zjistěte, kterou verzi používáte:

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Zkontrolujte to proti [informacím o vydáních Debianu](https://wiki.debian.org/LTS/) pro identifikaci kódového názvu vaší distribuce (např. Bookworm, Bullseye, Buster).

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pro Debian Bullseye (11) nebo novější:**

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
**Pro deriváty Debianu (LMDE, Kali, ParrotOS atd.) na Bullseye nebo novějších:**

**Pro Debian Buster (10) nebo starší:**

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Pro deriváty Debianu na Buster-ekvivalentu nebo starším:**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
**Krok 3: Stáhněte podpisový klíč repozitáře**

**Krok 4: Ověřte otisk klíče**

Před důvěřováním klíči ověřte, že jeho otisk odpovídá oficiálnímu podpisovému klíči I2P:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Ověřte, že výstup zobrazuje tento otisk:**

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
⚠️ **Nepokračujte, pokud se otisk neshoduje.** To by mohlo indikovat kompromitované stažení.

**Krok 5: Instalace klíče repozitáře**

```bash
sudo apt-get update
```
Zkopírujte ověřenou klíčenku do systémového adresáře klíčenek:

**Pouze pro Debian Buster nebo starší** je také potřeba vytvořit symbolický odkaz:

```bash
sudo apt-get install i2p i2p-keyring
```
**Krok 6: Aktualizace seznamů balíčků**

Obnovte databázi balíčků vašeho systému, aby zahrnovala repozitář I2P:

## Jak to funguje

**Krok 7: Instalace I2P**

### Metoda 2: Pomocí grafického rozhraní Software Center

Nainstalujte jak I2P router, tak balíček s klíčenkou (který zajistí, že budete dostávat budoucí aktualizace klíčů):

#### Option 1: On-Demand (Basic)

Skvělé! I2P je nyní nainstalováno. Pokračujte do sekce [Konfigurace po instalaci](#post-installation-configuration).

```bash
i2prouter start
```
---

NEKLASTĚ otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpisem nebo se zdá neúplný, přeložte ho tak, jak je.

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Po instalaci I2P budete muset spustit router a provést počáteční konfiguraci.

```bash
i2prouter-nowrapper
```
Balíčky I2P poskytují tři způsoby spuštění I2P routeru:

#### Option 3: System Service (Recommended)

Spusťte I2P manuálně podle potřeby pomocí skriptu `i2prouter`:

```bash
sudo dpkg-reconfigure i2p
```
**Důležité**: **Nepoužívejte** `sudo` ani toto nespouštějte jako root! I2P by mělo běžet pod vaším běžným uživatelským účtem.

Zastavení I2P:

### Initial Router Configuration

Pokud používáte systém jiný než x86 nebo Java Service Wrapper na vaší platformě nefunguje, použijte:

#### 1. Configure NAT/Firewall

Znovu, **nepoužívejte** `sudo` ani nespouštějte jako root.

- **Skrytá umístění**: Služby (eepsites) jsou přístupné pouze v síti I2P
- **Garlic encryption**: Mnoho zpráv zabalených společně pro lepší soukromí
- **Distribuovaná síť**: Žádný centrální bod selhání
- **Šifrování end-to-end**: Provoz je šifrován od zdroje k cíli
- **Nízká latence**: Optimalizováno pro interaktivní provoz

Pro nejlepší zkušenost nakonfigurujte I2P tak, aby se spouštěl automaticky při startu systému, ještě před přihlášením:

#### 2. Adjust Bandwidth Settings

Toto otevře dialogové okno konfigurace. Vyberte „Ano" pro povolení I2P jako systémové služby.

- I2P je **síť uvnitř sítě** (overlay network) - běží nad internetem
- Routery jsou provozovány dobrovolníky, nikoli centrální autoritou
- Síť je určena primárně pro služby **uvnitř I2P**, nikoli pro přístup na běžný internet

**Toto je doporučená metoda**, protože: - I2P se spustí automaticky při startu systému - Váš router udržuje lepší integraci se sítí - Přispíváte ke stabilitě sítě - I2P je okamžitě dostupné, když ho potřebujete

#### 3. Configure Your Browser

Po prvním spuštění I2P bude trvat několik minut, než se integruje do sítě. Mezitím nakonfigurujte tato základní nastavení:

Pro optimální výkon a účast v síti přesměrujte porty I2P skrz svůj NAT/firewall:

Pokud potřebujete pomoc s přesměrováním portů, [portforward.com](https://portforward.com) nabízí příručky specifické pro jednotlivé routery.

## Debian Installation

### Důležité upozornění

1. Otevřete [I2P Router Console](http://127.0.0.1:7657/)
2. Přejděte na [stránku konfigurace sítě](http://127.0.0.1:7657/confignet)
3. Poznamenejte si čísla portů (obvykle náhodné porty mezi 9000-31000)
4. Přesměrujte tyto UDP a TCP porty ve vašem routeru/firewallu

### Předpoklady

Výchozí nastavení šířky pásma je konzervativní. Upravte je podle vašeho internetového připojení:

1. Navštivte [konfigurační stránku](http://127.0.0.1:7657/config.jsp)
2. Najděte sekci nastavení šířky pásma
3. Výchozí hodnoty jsou 96 KB/s pro stahování / 40 KB/s pro odesílání
4. Zvyšte tyto hodnoty, pokud máte rychlejší internetové připojení (např. 250 KB/s pro stahování / 100 KB/s pro odesílání u typického širokopásmového připojení)

### Kroky instalace

**Poznámka**: Nastavení vyšších limitů pomáhá síti a zlepšuje váš vlastní výkon.

- Ujistěte se, že I2P neběží jako root: `ps aux | grep i2p`
- Zkontrolujte logy: `tail -f ~/.i2p/wrapper.log`
- Ověřte, že je nainstalována Java: `java -version`

### Migrating from old repositories

Pro přístup k I2P stránkám (eepsite) a službám nakonfigurujte svůj prohlížeč tak, aby používal HTTP proxy I2P:

1. Znovu stáhněte a ověřte otisk klíče (Krok 3-4 výše)
2. Ujistěte se, že soubor s klíčenkou má správná oprávnění: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

Přečtěte si náš [Průvodce konfigurací prohlížeče](/docs/guides/browser-config) s podrobnými pokyny pro nastavení Firefoxu, Chrome a dalších prohlížečů.

## Post-Installation Configuration

Pokud během instalace obdržíte chyby GPG klíče:

1. Ověřte, že je repozitář nakonfigurován: `cat /etc/apt/sources.list.d/i2p.list`
2. Aktualizujte seznam balíčků: `sudo apt-get update`
3. Zkontrolujte aktualizace I2P: `sudo apt-get upgrade`

Pokud I2P nepřijímá aktualizace:
