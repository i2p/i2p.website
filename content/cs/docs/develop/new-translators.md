---
title: "Průvodce pro nové překladatele"
description: "Jak přispět překlady na web I2P a do konzole routeru pomocí Transifexu nebo manuálními metodami"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

Chcete pomoci zpřístupnit I2P více lidem po celém světě? Překlad je jeden z nejcennějších příspěvků, které můžete projektu poskytnout. Tento průvodce vás provede překladem konzole routeru.

## Metody překladu

Existují dva způsoby, jak přispět k překladům:

### Metoda 1: Transifex (Doporučeno)

**Toto je nejjednodušší způsob, jak přeložit I2P.** Transifex poskytuje webové rozhraní, které činí překlad jednoduchým a přístupným.

1. Zaregistrujte se na [Transifex](https://www.transifex.com/otf/I2P/)
2. Požádejte o připojení k překladatelskému týmu I2P
3. Začněte překládat přímo ve vašem prohlížeči

Nejsou potřeba žádné technické znalosti - stačí se zaregistrovat a můžete začít překládat!

### Metoda 2: Ruční překlad

Pro překladatele, kteří preferují práci s git a lokálními soubory, nebo pro jazyky, které ještě nejsou nastaveny na Transifexu.

**Požadavky:** - Znalost systému správy verzí git - Textový editor nebo nástroj pro překlady (doporučuje se POEdit) - Nástroje příkazového řádku: git, gettext

**Nastavení:** 1. Připojte se na [#i2p-dev na IRC](/contact/#irc) a představte se 2. Aktualizujte stav překladu na wiki (požádejte o přístup na IRC) 3. Naklonujte příslušný repozitář (viz sekce níže)

---

## Překlad konzole routeru

Konzole routeru je webové rozhraní, které vidíte při spuštění I2P. Překlad pomáhá uživatelům, kteří neovládají angličtinu.

### Použití Transifexu (doporučeno)

1. Přejděte na [I2P na Transifex](https://www.transifex.com/otf/I2P/)
2. Vyberte projekt router console
3. Zvolte svůj jazyk
4. Začněte překládat

### Manuální překlad konzole routeru

**Předpoklady:** - Stejné jako pro překlad webových stránek (git, gettext) - GPG klíč (pro přístup k commitování) - Podepsaná vývojářská smlouva

**Klonujte hlavní I2P repozitář:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Soubory k překladu:**

Konzole routeru má přibližně 15 souborů, které je třeba přeložit:

1. **Hlavní soubory rozhraní:**
   - `apps/routerconsole/locale/messages_*.po` - Hlavní zprávy konzole
   - `apps/routerconsole/locale-news/messages_*.po` - Zprávy novinek

2. **Soubory proxy:**
   - `apps/i2ptunnel/locale/messages_*.po` - Rozhraní pro konfiguraci tunelů

3. **Lokalizace aplikací:**
   - `apps/susidns/locale/messages_*.po` - Rozhraní adresáře kontaktů
   - `apps/susimail/locale/messages_*.po` - Rozhraní e-mailu
   - Další adresáře lokalizací specifické pro aplikace

4. **Soubory dokumentace:**
   - `installer/resources/readme/readme_*.html` - Instalační readme
   - Soubory nápovědy v různých aplikacích

**Pracovní postup překladu:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Odešlete svou práci:** - Vytvořte merge request na [GitLabu](https://i2pgit.org/I2P_Developers/i2p.i2p) - Nebo sdílejte soubory s vývojovým týmem na IRC

---

## Nástroje pro překlad

### POEdit (Vysoce doporučeno)

[POEdit](https://poedit.net/) je specializovaný editor pro překladové soubory .po.

**Funkce:** - Vizuální rozhraní pro překladatelskou práci - Zobrazuje kontext překladu - Automatická validace - Dostupné pro Windows, macOS a Linux

### Textové editory

Můžete také použít libovolný textový editor: - VS Code (s rozšířeními pro i18n) - Sublime Text - vim/emacs (pro uživatele terminálu)

### Kontroly kvality

Před odesláním: 1. **Zkontrolujte formátování:** Ujistěte se, že zástupné znaky jako `%s` a `{0}` zůstávají beze změny 2. **Otestujte své překlady:** Nainstalujte a spusťte I2P, abyste viděli, jak vypadají 3. **Konzistence:** Udržujte terminologii konzistentní napříč soubory 4. **Délka:** Některé řetězce mají omezení délky v uživatelském rozhraní

---

## Tipy pro překladatele

### Obecné pokyny

- **Buďte konzistentní:** Používejte stejné překlady pro běžné termíny v celém dokumentu
- **Zachovejte formátování:** Ponechte HTML tagy, zástupné symboly (`%s`, `{0}`) a zalomení řádků
- **Kontext je důležitý:** Pečlivě si přečtěte zdrojový anglický text, abyste porozuměli kontextu
- **Ptejte se:** Použijte IRC nebo fóra, pokud je něco nejasné

### Běžné pojmy I2P

Některé výrazy by měly zůstat v angličtině nebo být pečlivě transliterovány:

- **I2P** - Keep as is
- **eepsite** - I2P webová stránka (může vyžadovat vysvětlení ve vašem jazyce)
- **tunnel** - Cesta spojení (vyhněte se terminologii Tor jako "circuit")
- **netDb** - Síťová databáze
- **floodfill** - Typ routeru
- **destination** - Koncový bod I2P adresy

### Testování vašich překladů

1. Sestavte I2P s vašimi překlady
2. Změňte jazyk v nastavení router console
3. Procházejte všechny stránky a kontrolujte:
   - Text se vejde do prvků uživatelského rozhraní
   - Žádné nečitelné znaky (problémy s kódováním)
   - Překlady dávají smysl v kontextu

---

## Často kladené otázky

### Proč je proces překladu tak složitý?

Proces využívá správu verzí (git) a standardní překladatelské nástroje (.po soubory), protože:

1. **Odpovědnost:** Sledujte, kdo co a kdy změnil
2. **Kvalita:** Zkontrolujte změny před jejich zveřejněním
3. **Konzistence:** Udržujte správné formátování a strukturu souborů
4. **Škálovatelnost:** Efektivně spravujte překlady napříč více jazyky
5. **Spolupráce:** Více překladatelů může pracovat na stejném jazyce

### Potřebuji znalosti programování?

**Ne!** Pokud používáte Transifex, potřebujete pouze: - Plynulost v angličtině i ve vašem cílovém jazyce - Webový prohlížeč - Základní počítačové dovednosti

Pro ruční překlad budete potřebovat základní znalost práce s příkazovým řádkem, ale programování není vyžadováno.

### Jak dlouho to trvá?

- **Konzole routeru:** Přibližně 15-20 hodin pro všechny soubory
- **Údržba:** Několik hodin měsíčně pro aktualizaci nových řetězců

### Může na jednom jazyku pracovat více lidí?

Ano! Koordinace je klíčová: - Používejte Transifex pro automatickou koordinaci - Pro manuální práci komunikujte v IRC kanálu #i2p-dev - Rozdělte práci podle sekcí nebo souborů

### Co když můj jazyk není v seznamu?

Požádejte o to na Transifexu nebo kontaktujte tým na IRC. Vývojový tým může nový jazyk nastavit rychle.

### Jak mohu otestovat své překlady před odesláním?

- Sestavte I2P ze zdrojového kódu s vašimi překlady
- Nainstalujte a spusťte lokálně
- Změňte jazyk v nastavení konzole

---

## Získání pomoci

### IRC podpora

Připojte se k [#i2p-dev na IRC](/contact/#irc) pro: - Technickou pomoc s nástroji pro překlad - Dotazy ohledně terminologie I2P - Koordinaci s dalšími překladateli - Přímou podporu od vývojářů

### Fóra

- Diskuse o překladech na [I2P Forums](http://i2pforum.net/)
- Inside I2P: Překladatelské fórum na zzz.i2p (vyžaduje I2P router)

### Dokumentace

- [Dokumentace Transifex](https://docs.transifex.com/)
- [Dokumentace POEdit](https://poedit.net/support)
- [Příručka gettext](https://www.gnu.org/software/gettext/manual/)

---

## Uznání

Všichni překladatelé jsou uvedeni v: - Konzoli I2P routeru (stránka O programu) - Stránce s kredity na webu - Historii Git commitů - Oznámeních o vydání

Vaše práce přímo pomáhá lidem po celém světě používat I2P bezpečně a soukromě. Děkujeme za váš příspěvek!

---

## Další kroky

Připraveni začít překládat?

1. **Vyberte si svou metodu:**
   - Rychlý start: [Zaregistrujte se na Transifexu](https://www.transifex.com/otf/I2P/)
   - Manuální přístup: Připojte se na [#i2p-dev na IRC](/contact/#irc)

2. **Začněte pomalu:** Přeložte několik řetězců, abyste se seznámili s procesem

3. **Požádejte o pomoc:** Neváhejte se obrátit na IRC nebo fóra

**Děkujeme, že pomáháte zpřístupnit I2P všem!**
