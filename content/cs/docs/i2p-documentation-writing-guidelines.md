---
title: "Pokyny pro psaní dokumentace I2P"
description: "Udržujte jednotnost, přesnost a přístupnost napříč technickou dokumentací I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Účel:** Zajistit konzistenci, přesnost a přístupnost napříč technickou dokumentací I2P

---

## Základní principy

### 1. Ověřte vše

**Nikdy nepředpokládejte ani nehádejte.** Všechna technická tvrzení musí být ověřena podle: - Aktuální zdrojový kód I2P (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Oficiální dokumentace API (https://i2p.github.io/i2p.i2p/  - Specifikace konfigurace [/docs/specs/](/docs/) - Poznámky k nejnovějším verzím [/releases/](/categories/release/)

**Příklad správného ověření:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Srozumitelnost před stručností

Pište pro vývojáře, kteří se mohou s I2P setkat poprvé. Koncepty vysvětlujte do hloubky a nepředpokládejte žádné předchozí znalosti.

**Příklad:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Přístupnost především

Dokumentace musí být pro vývojáře dostupná na clearnetu (běžný internet), ačkoli I2P je překryvná síť. Vždy poskytujte alternativy přístupné z clearnetu k interním zdrojům I2P.

---

## Technická správnost

### Dokumentace API a rozhraní

**Vždy uveďte:** 1. Plné názvy balíčků při prvním uvedení: `net.i2p.app.ClientApp` 2. Úplné signatury metod včetně návratových typů 3. Názvy a typy parametrů 4. Povinné vs volitelné parametry

**Příklad:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Konfigurační vlastnosti

Při dokumentaci konfiguračních souborů: 1. Uveďte přesné názvy vlastností 2. Uveďte kódování souboru (UTF-8 pro konfigurační soubory I2P) 3. Uveďte úplné příklady 4. Uveďte výchozí hodnoty 5. Uveďte verzi, ve které byly vlastnosti zavedeny nebo změněny

**Příklad:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Konstanty a výčty

Při dokumentování konstant používejte skutečné názvy z kódu:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Rozlišujte mezi podobnými pojmy

I2P má několik překrývajících se systémů. Vždy upřesněte, který systém dokumentujete:

**Příklad:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## Adresy URL a odkazy na dokumentaci

### Pravidla přístupnosti adres URL

1. **Primární odkazy** by měly používat adresy URL dostupné z clearnetu
2. **I2P-interní adresy URL** (domény .i2p) musí obsahovat poznámky k dostupnosti
3. **Vždy poskytujte alternativy** při odkazování na interní zdroje v I2P

**Šablona pro interní adresy URL v I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### Doporučené referenční URL pro I2P

**Oficiální specifikace:** - [Konfigurace](/docs/specs/configuration/) - [Zásuvný modul](/docs/specs/plugin/) - [Index dokumentace](/docs/)

**Dokumentace k API (vyberte nejaktuálnější):** - Nejaktuálnější: https://i2p.github.io/i2p.i2p/ (API 0.9.66 k verzi I2P 2.10.0) - Zrcadlo na clearnetu: https://eyedeekay.github.io/javadoc-i2p/

**Zdrojový kód:** - GitLab (oficiální): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - Zrcadlo na GitHubu: https://github.com/i2p/i2p.i2p

### Standardy formátu odkazů

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Sledování verzí

### Metadata dokumentu

Každý technický dokument by měl obsahovat metadata o verzi v oddílu frontmatter (úvodní hlavička souboru):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Definice polí:** - `lastUpdated`: Rok-měsíc, kdy byl dokument naposledy revidován/aktualizován - `accurateFor`: Verze I2P, vůči které byl dokument ověřen - `reviewStatus`: Jedna z hodnot "draft", "needs-review", "verified", "outdated"

### Odkazy na verze v obsahu

Při uvádění verzí: 1. Pro aktuální verzi použijte **tučné písmo**: "**verze 2.10.0** (září 2025)" 2. U historických odkazů uveďte jak číslo verze, tak datum 3. Pokud je to relevantní, uvádějte verzi API odděleně od verze I2P

**Příklad:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Dokumentování změn v průběhu času

U funkcí, které se vyvíjely:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Upozornění na zastarání

Pokud dokumentujete zastaralé funkce:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Standardy terminologie

### Oficiální pojmy I2P

Používejte tyto přesné termíny důsledně:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Terminologie spravovaného klienta

Při dokumentování spravovaných klientů:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Terminologie konfigurace

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Názvy balíčků a tříd

Při prvním výskytu vždy používejte plně kvalifikované názvy, poté krátké názvy:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Ukázky kódu a formátování

### Příklady kódu v jazyce Java

Používejte správné zvýrazňování syntaxe a úplné příklady:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Požadavky na ukázky kódu:** 1. Přidejte komentáře vysvětlující klíčové řádky 2. Ukažte zpracování chyb tam, kde je to vhodné 3. Používejte realistické názvy proměnných 4. Dodržujte I2P konvence kódování (odsazení čtyřmi mezerami) 5. Uveďte importy, pokud nejsou z kontextu zřejmé

### Příklady konfigurace

Zobrazte kompletní, platné příklady konfigurace:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Příklady příkazového řádku

Používejte `$` pro uživatelské příkazy, `#` pro root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Vložený kód

Používejte zpětné apostrofy pro: - Názvy metod: `startup()` - Názvy tříd: `ClientApp` - Názvy vlastností: `clientApp.0.main` - Názvy souborů: `clients.config` - Konstanty: `SVC_HTTP_PROXY` - Názvy balíčků: `net.i2p.app`

---

## Tón a hlas

### Profesionální, ale přístupný

Pište pro technické publikum bez blahosklonného tónu:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Činný rod

Používejte činný rod pro větší srozumitelnost:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Rozkazovací způsob v pokynech

Používejte přímé rozkazy v procedurálním obsahu:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Vyhněte se zbytečnému žargonu

Vysvětlete pojmy při prvním výskytu:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Pokyny k interpunkci

1. **Žádné em pomlčky** - místo nich používejte běžné pomlčky, čárky nebo středníky
2. Používejte **oxfordskou čárku** v seznamech: "console, i2ptunnel, and Jetty"
3. **Tečky uvnitř bloků kódu** pouze pokud jsou gramaticky nezbytné
4. **Složené výčty** používají středníky, pokud položky obsahují čárky

---

## Struktura dokumentu

### Standardní pořadí sekcí

Pro dokumentaci API:

1. **Přehled** - co funkce dělá, proč existuje
2. **Implementace** - jak ji implementovat/použít
3. **Konfigurace** - jak ji nakonfigurovat
4. **Reference API** - podrobné popisy metod a vlastností
5. **Příklady** - kompletní funkční příklady
6. **Osvědčené postupy** - tipy a doporučení
7. **Historie verzí** - kdy byla zavedena, změny v průběhu času
8. **Odkazy** - odkazy na související dokumentaci

### Hierarchie nadpisů

Používejte sémantické úrovně nadpisů:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Informační boxy

Používejte blokové citace pro zvláštní upozornění:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Seznamy a organizace

**Neuspořádané seznamy** pro položky bez pořadí:

```markdown
- First item
- Second item
- Third item
```
**Číslované seznamy** pro postupné kroky:

```markdown
1. First step
2. Second step
3. Third step
```
**Seznamy definic** pro vysvětlení pojmů:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Časté chyby, kterým je třeba se vyhnout

### 1. Snadno zaměnitelné podobné systémy

**Nezaměňujte:** - registr ClientAppManager vs. PortMapper - typy i2ptunnel tunnel vs. konstanty služby port mapperu - ClientApp vs. RouterApp (různé kontexty) - Spravovaní vs. nespravovaní klienti

**Vždy upřesněte, o jakém systému** mluvíte:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Zastaralé odkazy na verze

**Nedělejte:** - Označovat staré verze jako „aktuální“ - Odkazovat na zastaralou dokumentaci API - Používat zastaralé signatury metod v příkladech

**Dělejte:** - Před zveřejněním zkontrolujte poznámky k vydání - Ověřte, že dokumentace API odpovídá aktuální verzi - Aktualizujte příklady tak, aby používaly aktuální osvědčené postupy

### 3. Nedostupné adresy URL

**Nedělejte:** - Neodkazujte pouze na domény .i2p bez alternativ na clearnetu (veřejném internetu) - Nepoužívejte nefunkční nebo zastaralé adresy URL dokumentace - Neodkazujte na místní cesty file://

**Doporučeno:** - Poskytněte clearnetové alternativy pro všechny interní odkazy I2P - Ověřte, že jsou adresy URL dostupné před zveřejněním - Používejte trvalé adresy URL (geti2p.net, nikoli dočasný hosting)

### 4. Neúplné příklady kódu

**Nedělejte:** - Uvádět fragmenty bez kontextu - Vynechávat zpracování chyb - Používat nedefinované proměnné - Přeskakovat importní příkazy, když nejsou zřejmé

**Dělejte:** - Uveďte úplné, kompilovatelné příklady - Zahrňte potřebné ošetření chyb - Vysvětlete, co dělá každý důležitý řádek - Otestujte příklady před zveřejněním

### 5. Dvojznačná tvrzení

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Konvence Markdownu

### Pojmenování souborů

Použijte kebab-case (styl pojmenování slov oddělených pomlčkami) pro názvy souborů: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Formát Frontmatter (úvodní metadata)

Vždy zahrňte YAML frontmatter (YAMLové záhlaví s metadaty):

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Formátování odkazů

**Interní odkazy** (v rámci dokumentace):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Externí odkazy** (na další zdroje):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Odkazy na repozitáře kódu**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Formátování tabulek

Použijte tabulky ve formátu GitHub Flavored Markdown (GFM):

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Jazykové značky pro bloky kódu

Vždy uveďte jazyk pro zvýrazňování syntaxe:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Kontrolní seznam pro revizi

Před zveřejněním dokumentace ověřte:

- [ ] Všechna technická tvrzení ověřena proti zdrojovému kódu nebo oficiální dokumentaci
- [ ] Čísla verzí a data jsou aktuální
- [ ] Všechny URL jsou dostupné z clearnetu (veřejný internet) (nebo jsou uvedeny alternativy)
- [ ] Ukázky kódu jsou úplné a otestované
- [ ] Terminologie odpovídá konvencím I2P
- [ ] Žádné em‑pomlčky (použijte běžné pomlčky nebo jinou interpunkci)
- [ ] Frontmatter (úvodní metadata) je úplný a přesný
- [ ] Hierarchie nadpisů je sémantická (h1 → h2 → h3)
- [ ] Seznamy a tabulky jsou správně naformátované
- [ ] Sekce Reference obsahuje všechny citované zdroje
- [ ] Dokument se řídí pokyny ke struktuře
- [ ] Tón je profesionální, ale srozumitelný
- [ ] Podobné koncepty jsou jasně odlišeny
- [ ] Žádné nefunkční odkazy ani reference
- [ ] Konfigurační příklady jsou platné a aktuální

---

**Zpětná vazba:** Pokud narazíte na problémy nebo máte návrhy k těmto pokynům, odešlete je prosím prostřednictvím oficiálních vývojových kanálů I2P.
