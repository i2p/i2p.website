---
title: "Průvodce pro nové vývojáře"
description: "Jak začít přispívat do I2P: studijní materiály, zdrojový kód, sestavování, nápady, publikování, komunita, překlady a nástroje"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: aktualizovat část překladu
---

Takže chcete začít pracovat na I2P? Skvělé! Zde je rychlý průvodce, jak začít přispívat na webové stránky nebo software, vyvíjet nebo vytvářet překlady.

Ještě nejste připraveni na programování? Zkuste se nejprve [zapojit](/get-involved/).

## Poznejte Javu

I2P router a jeho vestavěné aplikace používají jako hlavní programovací jazyk Javu. Pokud nemáte zkušenosti s Javou, můžete se vždy podívat na [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Prostudujte si úvodní dokument "jak na to", další dokumenty "jak na to", technický úvod a související dokumenty:

- Jak začít: [Úvod do I2P](/docs/overview/intro/)
- Centrum dokumentace: [Dokumentace](/docs/)
- Technický úvod: [Technický úvod](/docs/overview/tech-intro/)

Toto vám poskytne dobrý přehled o tom, jak je I2P strukturován a jaké různé funkce vykonává.

## Získání kódu I2P

Pro vývoj I2P routeru nebo vestavěných aplikací potřebujete získat zdrojový kód.

### Náš současný způsob: Git

I2P má oficiální Git služby a přijímá příspěvky přes Git na našem vlastním GitLabu:

- Uvnitř I2P: <http://git.idk.i2p>
- Mimo I2P: <https://i2pgit.org>

Naklonujte hlavní repozitář:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
Zrcadlo pouze pro čtení je také dostupné na GitHubu:

- GitHub mirror: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## Sestavení I2P

Pro kompilaci kódu potřebujete Sun/Oracle Java Development Kit 6 nebo vyšší, případně ekvivalentní JDK (Sun/Oracle JDK 6 silně doporučeno) a Apache Ant verze 1.7.0 nebo vyšší. Pokud pracujete na hlavním kódu I2P, přejděte do adresáře `i2p.i2p` a spusťte `ant`, abyste viděli možnosti sestavení.

Pro sestavení nebo práci na překladech konzole potřebujete nástroje `xgettext`, `msgfmt` a `msgmerge` z balíčku GNU gettext.

Pro vývoj nových aplikací se podívejte do [průvodce vývojem aplikací](/docs/develop/applications/).

## Nápady pro vývoj

Podívejte se na seznam TODO projektu nebo na seznam problémů na GitLabu pro nápady:

- GitLab issues: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Zpřístupnění výsledků

Požadavky na práva k provádění commitů najdete na konci stránky s licencemi. Tyto práva potřebujete k vkládání kódu do `i2p.i2p` (pro webové stránky není vyžadováno!).

- [Stránka licencí](/docs/develop/licenses#commit)

## Poznejte nás!

Vývojáři se zdržují na IRC. Lze je zastihnout na různých sítích a na interních sítích I2P. Obvyklým místem je kanál `#i2p-dev`. Připojte se na kanál a pozdravte! Máme také další [pokyny pro pravidelné vývojáře](/docs/develop/dev-guidelines/).

## Překlady

Překladatelé webových stránek a routerové konzole: Další kroky najdete v [Příručce pro nové překladatele](/docs/develop/new-translators/).

## Nástroje

I2P je open source software, který je většinou vyvíjen pomocí open-source nástrojů. Projekt I2P nedávno získal licenci pro YourKit Java Profiler. Open source projekty mají nárok na bezplatnou licenci za podmínky, že YourKit je zmíněn na webových stránkách projektu. Pokud máte zájem o profilování I2P codebase, kontaktujte nás.

YourKit laskavě podporuje open source projekty svými plně vybavенými profilery. YourKit, LLC je tvůrcem inovativních a inteligentních nástrojů pro profilování Java a .NET aplikací. Podívejte se na přední softwarové produkty YourKit:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
