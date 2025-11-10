---
title: "Překladatelský Průvodce"
description: "Pomozte zpřístupnit I2P uživatelům po celém světě překladem router konsole a webu"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Přehled

Pomozte zpřístupnit I2P uživatelům po celém světě překladem konsole routeru I2P a webu do vašeho jazyka. Překlad je průběžný proces a příspěvky jakékoliv velikosti jsou cenné.

## Platforma pro překlad

Pro všechny překlady I2P používáme **Transifex**. Jedná se o nejjednodušší a doporučenou metodu pro nové i zkušené překladatele.

### Začínáme s Transifex

1. **Vytvořte si účet** na [Transifex](https://www.transifex.com/)
2. **Připojte se k projektu I2P**: [I2P na Transifex](https://explore.transifex.com/otf/I2P/)
3. **Požádejte o připojení** k týmu pro váš jazyk (nebo požádejte o nový jazyk, pokud není uveden)
4. **Začněte překládat** jakmile budete schváleni

### Proč Transifex?

- **Uživatelsky přívětivé rozhraní** - Žádné technické znalosti nejsou potřeba
- **Paměť překladu** - Navrhuje překlady na základě předchozí práce
- **Spolupráce** - Práce s ostatními překladateli ve vašem jazyce
- **Kontrola kvality** - Proces kontroly zajišťuje přesnost
- **Automatické aktualizace** - Změny se synchronizují s vývojovým týmem

## Co překládat

### Konzole routeru (Priorita)

Konzole routeru I2P je hlavní rozhraní, se kterým uživatelé komunikují při používání I2P. Její překlad má největší okamžitý dopad na uživatelský zážitek.

**Klíčové oblasti k překladu:**

- **Hlavní rozhraní** - Navigace, menu, tlačítka, stavové zprávy
- **Konfigurační stránky** - Popisy nastavení a možnosti
- **Nápověda** - Vestavěné soubory nápovědy a bubliny s tipy
- **Novinky a aktualizace** - Počáteční zpravodajský kanál, který uživatelé vidí
- **Chybové zprávy** - Chybové a varovné zprávy pro uživatele
- **Konfigurace proxy** - Stránky pro nastavení HTTP, SOCKS a tunelů

Všechny překlady konsole routeru jsou spravovány prostřednictvím Transifex ve formátu `.po` (gettext).

## Pokyny pro překlad

### Styl a tón

- **Jasný a stručný** - I2P pracuje s technickými koncepty; udržujte překlady jednoduché
- **Konzistentní terminologie** - Používejte stejné pojmy (kontrola paměti překladů)
- **Formální vs. neformální** - Dodržujte konvence pro váš jazyk
- **Zachování formátování** - Zachovejte zástupné znaky jako `{0}`, `%s`, `<b>tags</b>` neporušené

### Technické ohledy

- **Kódování** - Vždy používejte kódování UTF-8
- **Zástupné znaky** - Nepřekládejte zástupné proměnné (`{0}`, `{1}`, `%s`, atd.)
- **HTML/Markdown** - Zachovejte HTML značky a Markdown formátování
- **Odkazy** - Nechejte URL nezměněné, pokud neexistuje lokalizovaná verze
- **Zkratky** - Zvažte, zda překládat nebo ponechat originál (např. "KB/s", "HTTP")

### Testování vašich překladů

Pokud máte přístup k routeru I2P:

1. Stáhněte nejnovější překladové soubory z Transifex
2. Umístěte je do vaší instalace I2P
3. Restartujte konzoli routeru
4. Zkontrolujte překlady v kontextu
5. Nahlaste jakékoliv problémy nebo potřebná vylepšení

## Získání pomoci

### Podpora komunity

- **IRC kanál**: `#i2p-dev` na I2P IRC nebo OFTC
- **Fórum**: Fóra pro vývoj I2P
- **Komentáře na Transifex**: Pokládejte dotazy přímo u překladových řetězců

### Časté dotazy

**Q: Jak často bych měl překládat?**
Překládejte svým tempem. I překlad několika řetězců pomáhá. Projekt je průběžný.

**Q: Co když můj jazyk není uveden?**
Požádejte o nový jazyk na Transifex. Pokud je o něj zájem, tým ho přidá.

**Q: Můžu překládat sám nebo potřebuji tým?**
Můžete začít sami. Jakmile se připojí více překladatelů ve vašem jazyce, můžete spolupracovat.

**Q: Jak vím, co potřebuje překlad?**
Transifex ukazuje procenta dokončení a zvýrazňuje nepřeložené řetězce.

**Q: Co když nesouhlasím s existujícím překladem?**
Navrhněte vylepšení na Transifex. Recenzenti zhodnotí změny.

## Pokročilé: Ruční překlad (volitelné)

Pro zkušené překladatele, kteří chtějí přímý přístup ke zdrojovým souborům:

### Požadavky

- **Git** - Systém pro správu verzí
- **POEdit** nebo textový editor - Pro úpravy souborů `.po`
- **Základní znalosti příkazové řádky**

### Postup

1. **Klonujte repozitář**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Najděte překladové soubory**:
   - Konzole routeru: `apps/routerconsole/locale/`
   - Hledejte `messages_xx.po` (kde `xx` je váš jazykový kód)

3. **Upravte překlady**:
   - Použijte POEdit nebo textový editor
   - Uložte s kódováním UTF-8

4. **Testujte lokálně** (pokud máte I2P nainstalováno)

5. **Odešlete změny**:
   - Vytvořte požadavek na sloučení na [I2P Git](https://i2pgit.org/)
   - Nebo sdílejte váš `.po` soubor s vývojovým týmem

**Poznámka**: Většina překladatelů by měla používat Transifex. Ruční překlad je pouze pro ty, kteří jsou obeznámeni s Gitem a vývojovými pracovními postupy.

## Děkujeme

Každý překlad pomáhá zpřístupnit I2P uživatelům po celém světě. Ať už přeložíte několik řetězců nebo celé sekce, vaše příspěvky mají skutečný dopad na pomoc lidem při ochraně jejich soukromí online.

**Připraveni začít?** [Připojte se k I2P na Transifex →](https://explore.transifex.com/otf/I2P/)
