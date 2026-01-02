---
title: "Git Bundles pro I2P"
description: "Získávání a distribuce velkých repozitářů pomocí git bundle a BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Když síťové podmínky znesnadňují spolehlivé použití `git clone`, můžete distribuovat repozitáře jako **git bundles** přes BitTorrent nebo jakýkoliv jiný způsob přenosu souborů. Bundle je jediný soubor obsahující celou historii repozitáře. Po stažení z něj fetchujete lokálně a poté se přepnete zpět na upstream remote.

## 1. Než začnete

Generování balíčku vyžaduje **úplný** Git clone. Shallow clony vytvořené pomocí `--depth 1` tiše vytvoří nefunkční balíčky, které se zdají fungovat, ale selžou, když je zkusí použít ostatní. Vždy stahujte z důvěryhodného zdroje (GitHub na [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), instance I2P Gitea na [i2pgit.org](https://i2pgit.org), nebo `git.idk.i2p` přes I2P) a v případě potřeby spusťte `git fetch --unshallow` pro převod jakéhokoli shallow clone na úplný clone před vytvořením balíčků.

Pokud pouze používáte existující balíček, stačí jej stáhnout. Není potřeba žádná zvláštní příprava.

## 2. Stahování balíčku

### Obtaining the Bundle File

Stáhněte soubor balíčku přes BitTorrent pomocí I2PSnark (vestavěný torrent klient v I2P) nebo jiných I2P-kompatibilních klientů jako BiglyBT s I2P pluginem.

**Důležité**: I2PSnark funguje pouze s torrenty specificky vytvořenými pro síť I2P. Standardní clearnetové torrenty nejsou kompatibilní, protože I2P používá Destinations (adresy o délce 387+ bytů) místo IP adres a portů.

Umístění souboru balíčku závisí na typu vaší instalace I2P:

- **Uživatelské/manuální instalace** (instalováno pomocí Java instalátoru): `~/.i2p/i2psnark/`
- **Systémové/démonové instalace** (instalováno přes apt-get nebo správce balíčků): `/var/lib/i2p/i2p-config/i2psnark/`

Uživatelé BiglyBT najdou stažené soubory ve svém nakonfigurovaném adresáři pro stahování.

### Cloning from the Bundle

**Standardní metoda** (funguje ve většině případů):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Pokud narazíte na chyby `fatal: multiple updates for ref` (známý problém v Gitu 2.21.0 a novějších verzích, kdy globální konfigurace Gitu obsahuje konfliktní fetch refspecs), použijte ruční způsob inicializace:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternativně můžete použít příznak `--update-head-ok`:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Získání souboru Bundle

Po naklonování z balíčku nasměrujte svůj klon na živý remote, aby budoucí stahování probíhala přes I2P nebo clearnet:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Nebo pro přístup k čistému internetu:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Pro přístup k SSH přes I2P potřebujete v konzoli vašeho I2P routeru nakonfigurovaný SSH klientský tunel (obvykle port 7670) směřující na `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. Pokud používáte nestandardní port:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Klonování z balíčku

Ujistěte se, že je váš repozitář plně aktuální s **úplným klonem** (ne mělkým):

```bash
git fetch --all
```
Pokud máte mělký klon, nejprve jej převeďte:

```bash
git fetch --unshallow
```
### Přepnutí na živý vzdálený systém

**Použití cíle sestavení Ant** (doporučeno pro zdrojový strom I2P):

```bash
ant git-bundle
```
Toto vytvoří jak `i2p.i2p.bundle` (soubor bundle), tak `i2p.i2p.bundle.torrent` (metadata BitTorrent).

**Přímé použití git bundle**:

```bash
git bundle create i2p.i2p.bundle --all
```
Pro selektivnější balíčky:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Vždy před distribucí ověřte bundle:

```bash
git bundle verify i2p.i2p.bundle
```
Toto potvrzuje, že bundle je platný a zobrazuje všechny potřebné předchozí commity.

### Předpoklady

Zkopírujte bundle a jeho torrentová metadata do vašeho adresáře I2PSnark:

**Pro uživatelské instalace**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Pro systémové instalace**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark automaticky detekuje a načítá .torrent soubory během několika sekund. Pro zahájení seedování přejděte na webové rozhraní na adrese [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark).

## 4. Creating Incremental Bundles

Pro pravidelné aktualizace vytvořte inkrementální balíčky obsahující pouze nové commity od posledního balíčku:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Uživatelé mohou stáhnout z inkrementálního balíčku, pokud již mají základní repozitář:

```bash
git fetch /path/to/update.bundle
```
Vždy ověřte, že inkrementální balíčky zobrazují očekávané nezbytné commity:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Jakmile máte funkční repozitář z balíčku, pracujte s ním jako s jakýmkoli jiným Git klonem:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Nebo pro jednodušší pracovní postupy:

```bash
git fetch origin
git pull origin master
```
## 3. Vytvoření balíčku

- **Odolná distribuce**: Velké repozitáře lze sdílet přes BitTorrent, který automaticky řeší opakované pokusy, ověřování částí a pokračování v přenosu.
- **Peer-to-peer bootstrap**: Noví přispěvatelé mohou bootstrapovat svůj klon z blízkých peerů v síti I2P a poté získávat inkrementální změny přímo z Git hostů.
- **Snížené zatížení serveru**: Zrcadla mohou publikovat periodické balíčky pro uvolnění tlaku na živé Git hosty, což je zvláště užitečné pro velké repozitáře nebo pomalé síťové podmínky.
- **Offline přenos**: Balíčky fungují na jakémkoliv souborovém přenosu (USB disky, přímé přenosy, sneakernet), nejen na BitTorrentu.

Bundly nenahrazují živá vzdálená úložiště. Poskytují pouze odolnější metodu bootstrappingu pro počáteční klonování nebo větší aktualizace.

## 7. Troubleshooting

### Generování balíčku

**Problém**: Vytvoření bundle je úspěšné, ale ostatní nemohou klonovat z bundle.

**Příčina**: Váš zdrojový klon je mělký (vytvořen s parametrem `--depth`).

**Řešení**: Před vytvořením balíčků převeďte na úplný klon:

```bash
git fetch --unshallow
```
### Ověření vašeho balíčku

**Problém**: `fatal: multiple updates for ref` při klonování z bundle.

**Příčina**: Git 2.21.0+ je v konfliktu s globálními fetch refspecs v `~/.gitconfig`.

**Řešení**: 1. Použijte ruční inicializaci: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Použijte příznak `--update-head-ok`: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Odstraňte konfliktní konfiguraci: `git config --global --unset remote.origin.fetch`

### Distribuce přes I2PSnark

**Problém**: `git bundle verify` hlásí chybějící prerekvizity.

**Příčina**: Inkrementální balíček nebo neúplný klon zdroje.

**Řešení**: Buď stáhněte nezbytné předchozí commity, nebo nejprve použijte základní bundle a poté aplikujte inkrementální aktualizace.
