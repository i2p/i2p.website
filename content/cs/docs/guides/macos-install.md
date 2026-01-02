---
title: "Instalace I2P na macOS (Dlouhá cesta)"
description: "Podrobný průvodce ruční instalací I2P a jeho závislostí na macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Co budete potřebovat

- Mac se systémem macOS 10.14 (Mojave) nebo novějším
- Administrátorská práva pro instalaci aplikací
- Přibližně 15-20 minut času
- Připojení k internetu pro stažení instalátorů

## Přehled

Tento instalační proces má čtyři hlavní kroky:

1. **Nainstalujte Javu** - Stáhněte a nainstalujte Oracle Java Runtime Environment
2. **Nainstalujte I2P** - Stáhněte a spusťte instalátor I2P
3. **Nakonfigurujte aplikaci I2P** - Nastavte spouštěč a přidejte ho do doku
4. **Nakonfigurujte šířku pásma I2P** - Spusťte průvodce nastavením pro optimalizaci vašeho připojení

## Část první: Instalace Java

I2P vyžaduje ke spuštění Javu. Pokud již máte nainstalovanou Javu 8 nebo novější, můžete [přeskočit na druhou část](#part-two-download-and-install-i2p).

### Step 1: Download Java

Navštivte [stránku pro stažení Oracle Java](https://www.oracle.com/java/technologies/downloads/) a stáhněte si instalátor pro macOS pro Javu 8 nebo novější.

![Stáhnout Oracle Java pro macOS](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Najděte stažený soubor `.dmg` ve složce Stažené a dvojitým kliknutím ho otevřete.

![Otevřete instalátor Javy](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS může zobrazit bezpečnostní upozornění, protože instalátor pochází od identifikovaného vývojáře. Klikněte na **Otevřít** pro pokračování.

![Udělte instalačnímu programu oprávnění k pokračování](/images/guides/macos-install/2-jre.png)

### Krok 1: Stáhněte Javu

Klikněte na **Install** pro zahájení procesu instalace Javy.

![Spuštění instalace Javy](/images/guides/macos-install/3-jre.png)

### Krok 2: Spusťte instalátor

Instalátor zkopíruje soubory a nakonfiguruje Javu ve vašem systému. Obvykle to trvá 1-2 minuty.

![Počkejte na dokončení instalace](/images/guides/macos-install/4-jre.png)

### Krok 3: Povolit instalaci

Když se zobrazí zpráva o úspěchu, Java je nainstalována! Klikněte na **Zavřít** a dokončete instalaci.

![Instalace Javy dokončena](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Nyní, když je Java nainstalována, můžete nainstalovat I2P router.

### Krok 4: Instalace Javy

Navštivte [stránku ke stažení](/downloads/) a stáhněte si instalátor **I2P pro Unix/Linux/BSD/Solaris** (soubor `.jar`).

```markdown
![Stáhnout instalátor I2P](/images/guides/macos-install/0-i2p.png)
```

### Krok 5: Počkejte na dokončení instalace

Dvojklikem spusťte stažený soubor `i2pinstall_X.X.X.jar`. Instalátor se spustí a požádá vás o výběr preferovaného jazyka.

![Vyberte svůj jazyk](/images/guides/macos-install/1-i2p.png)

### Krok 6: Instalace dokončena

Přečtěte si uvítací zprávu a pokračujte kliknutím na **Next**.

![Úvod instalátoru](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

Instalátor zobrazí důležité upozornění týkající se aktualizací. Aktualizace I2P jsou **end-to-end podepsané** a ověřené, i když je samotný instalátor nepodepsaný. Klikněte na **Další**.

![Důležité upozornění o aktualizacích](/images/guides/macos-install/3-i2p.png)

### Krok 1: Stáhnout I2P

Přečtěte si licenční smlouvu I2P (licence typu BSD). Klikněte na **Next** pro přijetí.

![License agreement](/images/guides/macos-install/4-i2p.png)

### Krok 2: Spusťte instalátor

Zvolte, kam nainstalovat I2P. Doporučuje se výchozí umístění (`/Applications/i2p`). Klikněte na **Další**.

![Vyberte instalační adresář](/images/guides/macos-install/5-i2p.png)

### Krok 3: Úvodní obrazovka

Ponechte všechny komponenty vybrané pro úplnou instalaci. Klikněte na **Další**.

![Vyberte komponenty k instalaci](/images/guides/macos-install/6-i2p.png)

### Krok 4: Důležité upozornění

Zkontrolujte své volby a klikněte na **Next** (Další) pro zahájení instalace I2P.

![Spustit instalaci](/images/guides/macos-install/7-i2p.png)

### Krok 5: Licenční smlouva

Instalátor zkopíruje soubory I2P do vašeho systému. Trvá to přibližně 1-2 minuty.

![Probíhá instalace](/images/guides/macos-install/8-i2p.png)

### Krok 6: Vyberte adresář pro instalaci

Instalátor vytváří spouštěcí skripty pro spuštění I2P.

![Generování spouštěcích skriptů](/images/guides/macos-install/9-i2p.png)

### Krok 7: Výběr komponent

Instalátor nabízí vytvoření zástupců na ploše a položek v nabídce. Proveďte svůj výběr a klikněte na **Další**.

![Vytvořit zástupce](/images/guides/macos-install/10-i2p.png)

### Krok 8: Spuštění instalace

Úspěch! I2P je nyní nainstalováno. Klikněte na **Hotovo** pro dokončení.

![Instalace dokončena](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Nyní usnadníme spouštění I2P jeho přidáním do složky Aplikace a do Docku.

### Krok 9: Instalace souborů

Otevřete Finder a přejděte do složky **Aplikace**.

![Otevřete složku Aplikace](/images/guides/macos-install/0-conf.png)

### Krok 10: Vygenerování spouštěcích skriptů

Vyhledejte složku **I2P** nebo aplikaci **Start I2P Router** uvnitř `/Applications/i2p/`.

![Najděte spouštěč I2P](/images/guides/macos-install/1-conf.png)

### Krok 11: Instalační zkratky

Přetáhněte aplikaci **Start I2P Router** do Docku pro snadný přístup. Můžete také vytvořit alias na ploše.

![Přidat I2P do Docku](/images/guides/macos-install/2-conf.png)

**Tip**: Klikněte pravým tlačítkem na ikonu I2P v Docku a vyberte **Možnosti → Ponechat v Docku**, aby zůstala trvale.

## Part Four: Configure I2P Bandwidth

Když poprvé spustíte I2P, projdete průvodcem nastavením pro konfiguraci vašich nastavení šířky pásma. To pomáhá optimalizovat výkon I2P pro vaše připojení.

### Krok 12: Instalace dokončena

Klikněte na ikonu I2P v Docku (nebo dvakrát klikněte na spouštěč). Ve vašem výchozím webovém prohlížeči se otevře I2P Router Console.

![Uvítací obrazovka I2P Router Console](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

Průvodce nastavením vás přivítá. Klikněte na **Další** a zahajte konfiguraci I2P.

![Úvod průvodce nastavením](/images/guides/macos-install/1-wiz.png)

### Krok 1: Otevřete složku Aplikace

Vyberte preferovaný **jazyk rozhraní** a zvolte **světlý** nebo **tmavý** motiv. Klikněte na **Další**.

![Vybrat jazyk a motiv](/images/guides/macos-install/2-wiz.png)

### Krok 2: Najít I2P Launcher

Průvodce vysvětlí test šířky pásma. Tento test se připojí ke službě **M-Lab** pro měření rychlosti vašeho internetového připojení. Klikněte na **Další** pro pokračování.

![Vysvětlení testu rychlosti připojení](/images/guides/macos-install/3-wiz.png)

### Krok 3: Přidat do Docku

Klikněte na **Run Test** pro změření rychlosti uploadu a downloadu. Test trvá přibližně 30-60 sekund.

![Spuštění testu šířky pásma](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Zkontrolujte výsledky testu. I2P doporučí nastavení šířky pásma na základě rychlosti vašeho připojení.

![Výsledky testu šířky pásma](/images/guides/macos-install/5-wiz.png)

### Krok 1: Spusťte I2P

Vyberte, kolik šířky pásma chcete sdílet se sítí I2P:

- **Automatická** (Doporučeno): I2P spravuje šířku pásma podle vašeho využití
- **Omezená**: Nastavte konkrétní limity pro upload/download
- **Neomezená**: Sdílejte co nejvíce (pro rychlá připojení)

Klikněte na **Další** pro uložení vašeho nastavení.

![Nastavení sdílení šířky pásma](/images/guides/macos-install/6-wiz.png)

### Krok 2: Uvítací průvodce

Váš I2P router je nyní nakonfigurován a běží! Konzole routeru zobrazí stav vašeho připojení a umožní vám procházet I2P stránky.

## Getting Started with I2P

Nyní, když je I2P nainstalováno a nakonfigurováno, můžete:

1. **Procházejte I2P stránky**: Navštivte [domovskou stránku I2P](http://127.0.0.1:7657/home) a prohlédněte si odkazy na populární I2P služby
2. **Nakonfigurujte svůj prohlížeč**: Nastavte [profil prohlížeče](/docs/guides/browser-config) pro přístup ke stránkám `.i2p`
3. **Prozkoumejte služby**: Vyzkoušejte I2P e-mail, fóra, sdílení souborů a další
4. **Sledujte svůj router**: [Konzole](http://127.0.0.1:7657/console) zobrazuje stav vaší sítě a statistiky

### Krok 3: Jazyk a motiv

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Konfigurace**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Adresář**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Nastavení šířky pásma**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Pokud chcete později změnit nastavení šířky pásma nebo překonfigurovat I2P, můžete znovu spustit průvodce nastavením z Konzole routeru:

1. Přejděte na [I2P Setup Wizard](http://127.0.0.1:7657/welcome)
2. Znovu projděte kroky průvodce

## Troubleshooting

### Krok 4: Informace o testu šířky pásma

- **Zkontrolujte Javu**: Ujistěte se, že je Java nainstalována spuštěním příkazu `java -version` v Terminálu
- **Zkontrolujte oprávnění**: Ujistěte se, že složka I2P má správná oprávnění
- **Zkontrolujte logy**: Podívejte se do `~/.i2p/wrapper.log` na chybové hlášky

### Krok 5: Spuštění testu šířky pásma

- Ujistěte se, že I2P běží (zkontrolujte Router Console)
- Nakonfigurujte nastavení proxy ve vašem prohlížeči na HTTP proxy `127.0.0.1:4444`
- Počkejte 5-10 minut po spuštění, než se I2P integruje do sítě

### Krok 6: Výsledky testů

- Spusťte test šířky pásma znovu a upravte svá nastavení
- Ujistěte se, že sdílíte část šířky pásma se sítí
- Zkontrolujte stav vašeho připojení v Router Console

## Část druhá: Stažení a instalace I2P

Jak odebrat I2P z vašeho Macu:

1. Ukončete I2P router, pokud běží
2. Smažte složku `/Applications/i2p`
3. Smažte složku `~/.i2p` (vaše konfigurace a data I2P)
4. Odstraňte ikonu I2P z vašeho Docku

## Next Steps

- **Připojte se ke komunitě**: Navštivte [i2pforum.net](http://i2pforum.net) nebo se podívejte na I2P na Redditu
- **Dozvědět se více**: Přečtěte si [dokumentaci I2P](/en/docs), abyste pochopili, jak síť funguje
- **Zapojte se**: Zvažte [přispívání do vývoje I2P](/en/get-involved) nebo provozování infrastruktury

Gratulujeme! Nyní jste součástí sítě I2P. Vítejte na neviditelném internetu!

---

 NEPTEJTE se, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá neúplný, přeložte jej tak, jak je.
