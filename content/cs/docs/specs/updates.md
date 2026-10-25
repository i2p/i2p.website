---
title: "Specifikace aktualizace softwaru"
description: "Specifikace pro mechanismus aktualizace softwaru I2P, formát souborů SU3 a zpravodajský kanál"
slug: "updates"
aliases:
  - "/cs/updates"
  - "/cs/updates/"
category: "Návrh"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Přehled

I2P používá jednoduchý, ale bezpečný systém pro automatické aktualizace softwaru. Konzola routeru pravidelně stahuje soubor s novinkami z konfigurovatelné I2P URL adresy. Existuje pevně zakódovaná záložní URL adresa směřující na projektový web pro případ, že výchozí server s novinkami projektu nebude dostupný.

Obsah souboru s novinkami se zobrazuje na domovské stránce konzole routeru. Kromě toho soubor s novinkami obsahuje číslo nejnovější verze softwaru. Pokud je verze vyšší než číslo verze routeru, zobrazí se uživateli oznámení, že je k dispozici aktualizace.

Router může volitelně stáhnout, nebo stáhnout a nainstalovat, novou verzi, pokud je k tomu nakonfigurován.

## Specifikace starého souboru novinek

Tento formát je od vydání 0.9.17 nahrazen formátem su3 news.

Soubor news.xml může obsahovat následující prvky:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Parametry v záznamu i2p.release jsou následující. Všechny klíče jsou necitlivé na velká a malá písmena. Všechny hodnoty musí být uzavřeny v uvozovkách.

**date** : Datum vydání verze routeru. Nepoužívá se. Formát není specifikován.

**minJavaVersion** : Minimální verze Javy potřebná ke spuštění aktuální verze. Od vydání 0.9.9.

**minVersion** : Minimální verze routeru potřebná pro aktualizaci na současnou verzi. Pokud je router starší než tato verze, uživatel musí (ručně?) nejprve aktualizovat na přechodnou verzi. Od vydání 0.9.9.

**su3Clearnet** : Jedna nebo více HTTP URL adres, kde lze najít .su3 soubor s aktualizací na clearnetu (mimo I2P). Více URL adres musí být odděleno mezerou nebo čárkou. Od verze 0.9.9.

**su3SSL** : Jedna nebo více HTTPS URL, kde lze najít aktualizační soubor .su3 na clearnetu (mimo I2P). Více URL musí být odděleno mezerou nebo čárkou. Od verze 0.9.9.

**sudTorrent** : Magnetický odkaz pro .sud (non-pack200) torrent aktualizace. Od verze 0.9.4.

**su2Torrent** : Magnet odkaz pro .su2 (pack200) torrent aktualizace. Od verze 0.9.4.

**su3Torrent** : Magnetický odkaz pro .su3 (nový formát) torrent aktualizace. Od verze 0.9.9.

**version** : Povinné. Nejnovější aktuální verze router dostupná.

Elementy mohou být zahrnuty do XML komentářů, aby se zabránilo jejich interpretaci prohlížeči. Element i2p.release a verze jsou povinné. Všechny ostatní jsou volitelné. POZNÁMKA: Kvůli omezením parseru musí být celý element na jednom řádku.

## Specifikace aktualizačního souboru

Od verze 0.9.9 bude podepsaný soubor s aktualizací s názvem i2pupdate.su3 používat formát souboru "su3" specifikovaný níže. Schválení podepisovatelé vydání budou používat 4096-bitové RSA klíče. X.509 certifikáty veřejných klíčů pro tyto podepisovatele jsou distribuovány v instalačních balíčcích routeru. Aktualizace mohou obsahovat certifikáty pro nové, schválené podepisovatele a/nebo obsahovat seznam certifikátů ke smazání pro zrušení.

## Specifikace starého souboru aktualizace

Tento formát je zastaralý od vydání 0.9.9.

Podepsaný soubor aktualizace, tradičně nazvaný i2pupdate.sud, je jednoduše zip soubor s připojenou 56 bajtovou hlavičkou na začátku. Hlavička obsahuje:

- 40bytový DSA [Signature](/docs/specs/common-structures#signature)
- 16bytová I2P verze v UTF-8, doplněná koncovými nulami pokud je to nutné

Podpis pokrývá pouze zip archiv - ne připojenou verzi. Podpis musí odpovídat jednomu z DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) nakonfigurovaných v routeru, který má pevně zakódovaný výchozí seznam klíčů současných správců vydání projektu.

Pro účely porovnávání verzí obsahují pole verzí [0-9]*, oddělovače polí jsou '-', '_' a '.', a všechny ostatní znaky jsou ignorovány.

Od verze 0.8.8 musí být verze také specifikována jako komentář zip souboru v UTF-8, bez koncových nul. Aktualizující router ověřuje, že verze v hlavičce (nekrytá podpisem) odpovídá verzi v komentáři zip souboru, která je kryta podpisem. To zabraňuje falšování čísla verze v hlavičce.

## Stažení a instalace

Router nejprve stáhne hlavičku aktualizačního souboru z jedné z konfigurovatelného seznamu I2P URL, pomocí vestavěného HTTP klienta a proxy, a zkontroluje, zda je verze novější. Tím se předchází problému s aktualizačními hostiteli, kteří nemají nejnovější soubor. Router poté stáhne celý aktualizační soubor. Router před instalací ověří, že verze aktualizačního souboru je novější. Také samozřejmě ověří podpis a ověří, že komentář zip souboru odpovídá verzi v hlavičce, jak je vysvětleno výše.

Zip soubor je extrahován a zkopírován jako "i2pupdate.zip" do konfiguračního adresáře I2P (~/.i2p na Linuxu).

Od verze 0.7.12 router podporuje Pack200 dekompresní. Soubory uvnitř zip archivu s příponou .jar.pack nebo .war.pack jsou transparentně dekompresovány na soubory .jar nebo .war. Aktualizační soubory obsahující .pack soubory jsou tradičně pojmenovány s příponou '.su2'. Pack200 zmenšuje aktualizační soubory přibližně o 60%.

Od verze 0.8.7 router smaže soubory libjbigi.so a libjcpuid.so, pokud zip archiv obsahuje soubor lib/jbigi.jar, aby se nové soubory extrahovaly z jbigi.jar.

Od verze 0.8.12, pokud zip archiv obsahuje soubor deletelist.txt, router odstraní soubory v něm uvedené. Formát je:

- Jeden název souboru na řádek
- Všechny názvy souborů jsou relativní k instalačnímu adresáři; absolutní názvy souborů nejsou povoleny, žádné soubory nezačínají na ".."
- Komentáře začínají na '#'

Router poté smaže soubor deletelist.txt.

## Specifikace souboru SU3

Tato specifikace se používá pro aktualizace routerů od verze 0.9.9, reseed data od verze 0.9.14, pluginy od verze 0.9.15 a soubor zpráv od verze 0.9.17.

### Problémy s předchozím formátem .sud/.su2

- Žádné magické číslo ani příznaky
- Není způsob, jak specifikovat kompresi, pack200 nebo ne, nebo podepisovací algoritmus
- Verze není pokryta podpisem, takže je vynucena vyžadováním, aby byla v komentáři zip souboru (pro router soubory) nebo v souboru plugin.config (pro pluginy)
- Podepisovatel není specifikován, takže ověřovatel musí vyzkoušet všechny známé klíče
- Formát podpis-před-daty vyžaduje dva průchody pro generování souboru

### Cíle

- Opravit výše uvedené problémy
- Přejít na bezpečnější algoritmus podpisu
- Zachovat informace o verzi ve stejném formátu a offsetu pro kompatibilitu s existujícími kontrolami verzí
- Jednoprochodové ověření podpisu a extrakce souboru

### Specifikace

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Všechna nepoužitá pole musí být nastavena na 0 pro kompatibilitu s budoucími verzemi.

### Detaily podpisu

Podpis pokrývá celou hlavičku začínající na bytu 0 až po konec obsahu. Používáme raw podpisy. Vezměte hash dat (pomocí typu hashe implikovaného typem podpisu na bytech 8-9) a předejte ho "raw" funkci pro podpisování nebo ověřování (např. "NONEwithRSA" v Javě).

Zatímco ověření podpisu a extrakce obsahu mohou být implementovány v jednom průchodu, implementace musí přečíst a uložit do bufferu prvních 10 bajtů pro určení typu hash před zahájením ověřování.

Délky podpisů pro různé typy podpisů jsou uvedeny ve specifikaci [Signature](/docs/specs/common-structures#signature). V případě potřeby doplňte podpis počátečními nulami. Podívejte se na [stránku s detaily kryptografie](/docs/specs/cryptography#sig) pro parametry různých typů podpisů.

### Poznámky

Typ obsahu specifikuje doménu důvěry. Pro každý typ obsahu si klienti udržují sadu X.509 certifikátů veřejných klíčů pro strany, kterým důvěřují při podepisování daného obsahu. Mohou být použity pouze certifikáty pro specifikovaný typ obsahu. Certifikát se vyhledává podle ID podepisovatele. Klienti musí ověřit, že typ obsahu odpovídá tomu, co aplikace očekává.

Všechny hodnoty jsou v síťovém pořadí bajtů (big endian).

Pro pythonovou implementaci Raw RSA podpisů kompatibilní s Java "NONEwithRSA", viz [tento článek na Stack Overflow](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## Specifikace souboru SU3 Router Update

### Podrobnosti SU3

- SU3 Content Type: 1 (ROUTER UPDATE)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Verze routeru

Soubory jar a war v zip archivu již nejsou komprimovány pomocí pack200, jak je zdokumentováno výše pro soubory "su2", protože nedávné Java runtime prostředí již tuto funkcionalitu nepodporují.

### Poznámky

- Pro vydání je verze SU3 "základní" verze routeru, např. "0.9.20".
- Pro vývojářské sestavení, která jsou podporována od vydání 0.9.20, je verze SU3 "úplná" verze routeru, např. "0.9.20-5" nebo "0.9.20-5-rc". Viz RouterVersion.java ve [zdrojovém kódu I2P](https://github.com/i2p/i2p.i2p).

## Specifikace SU3 Reseed souboru

Od verze 0.9.14 jsou reseed data doručována ve formátu souboru "su3".

### Cíle

- Podepsané soubory se silnými podpisy a důvěryhodnými certifikáty k prevenci útoků man-in-the-middle, které by mohly nasměrovat oběti do samostatné, nedůvěryhodné sítě.
- Použití formátu souborů su3 již používaného pro aktualizace a pluginy
- Jeden komprimovaný soubor pro urychlení reseedingu, který byl pomalý při stahování 200 souborů

### Specifikace

1. Soubor musí být pojmenován "i2pseeds.su3". Od verze 0.9.42 by žadatel měl připojit řetězec dotazu "?netid=2" k URL požadavku, za předpokladu aktuálního síťového ID 2. Toto může být použito k zabránění připojení mezi sítěmi. Testovací sítě by měly nastavit jiné síťové ID. Viz návrh 147 pro podrobnosti.
2. Soubor musí být ve stejném adresáři jako router infos na webovém serveru.
3. Router se nejprve pokusí načíst (index URL)/i2pseeds.su3; pokud se to nezdaří, načte index URL a poté načte jednotlivé router info soubory nalezené v odkazech.

### Podrobnosti SU3

- SU3 Content Type: 3 (RESEED)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Sekundy od epochy, v ASCII (date +%s). NEPŘETOČÍ se v roce 2038 nebo 2106.
- Soubory router info v zip souboru musí být na "nejvyšší úrovni". V zip souboru nejsou žádné adresáře.
- Soubory router info musí být pojmenovány "routerInfo-(44 znakový base 64 router hash).dat", jako ve starém reseed mechanismu. Musí být použita I2P base 64 abeceda.

### Poznámky

- Varování: Několik reseed serverů je známo jako nereagující přes IPv6. Doporučuje se vynucení nebo upřednostnění IPv4.
- Varování: Některé reseed servery používají samopodepsané CA certifikáty. Implementace musí buď importovat a důvěřovat těmto CA při reseedování, nebo vynechat samopodepsané reseed servery ze seznamu reseed serverů.
- Klíče reseed podepisovatele jsou distribuovány do implementací jako samopodepsané X.509 certifikáty s RSA-4096 klíči (typ podpisu 6). Implementace by měly vynucovat platná data v certifikátech.

## Specifikace souboru SU3 pluginu

Od verze 0.9.15 mohou být pluginy zabaleny ve formátu souborů "su3".

### Detaily SU3

- SU3 Content Type: 2 (PLUGIN)
- SU3 File Type: 0 (ZIP) - Podrobnosti najdete ve [specifikaci pluginu](/docs/specs/plugin).
- SU3 Version: Verze pluginu, musí odpovídat té v plugin.config.

Soubory jar a war v zip archivu by neměly být komprimovány pomocí pack200, jak je dokumentováno výše pro soubory "su2", protože nejnovější verze Java runtime již tuto funkci nepodporují.

## Specifikace SU3 News souboru

Od verze 0.9.17 jsou novinky doručovány ve formátu souboru "su3".

### Cíle

- Podepsané zprávy se silnými podpisy a důvěryhodnými certifikáty
- Použití formátu souborů su3 již používaného pro aktualizace, reseeding a pluginy
- Standardní formát XML pro použití se standardními parsery
- Standardní formát Atom pro použití se standardními čtečkami a generátory feedů
- Sanitizace a ověření HTML před zobrazením v konzole
- Vhodné pro snadnou implementaci na Androidu a dalších platformách bez HTML konzole

### Detaily SU3

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) nebo 3 (XML.GZ)
- SU3 Version: Sekundy od epochy, v ASCII (date +%s). NEPŘEKLOPÍ se v roce 2038 nebo 2106.
- Formát souboru: XML nebo gzipovaný XML, obsahující [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed. Kódování musí být UTF-8.

### Podrobnosti Atom Feed

Používají se následující prvky `<feed>`:

**`<entry>`** : Zpravodajská položka. Viz níže.

**`<i2p:release>`** : Metadata aktualizace I2P. Viz níže.

**`<i2p:revocations>`** : Odvolání certifikátů. Viz níže.

**`<i2p:blocklist>`** : Data seznamu zakázaných. Viz níže.

**`<updated>`** : Povinné. Časová značka pro feed (v souladu s [RFC 4287](https://tools.ietf.org/html/rfc4287) sekce 3.3 a [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Podrobnosti Atom záznamu

Každý Atom `<entry>` v novinkách může být analyzován a zobrazen v konzoli routeru. Používají se následující elementy:

**`<author>`** : Volitelné. Obsahuje `<name>` - Jméno autora příspěvku.

**`<content>`** : Povinné. Obsah, musí být type="xhtml". XHTML bude sanitizováno pomocí whitelistu povolených elementů a blacklistu nepovolených atributů. Klienti mohou ignorovat element, nebo obsahující záznam, nebo celý feed, když narazí na element, který není na whitelistu.

**`<link>`** : Volitelné. Odkaz pro další informace.

**`<summary>`** : Volitelné. Krátké shrnutí, vhodné pro tooltip.

**`<title>`** : Povinné. Název příspěvku s novinkami.

**`<updated>`** : Povinné. Časová značka pro tuto položku (odpovídající [RFC 4287](https://tools.ietf.org/html/rfc4287) sekce 3.3 a [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Atom i2p:release Detaily

V kanálu musí být alespoň jedna entita `<i2p:release>`. Každá obsahuje následující atributy a entity:

**date (atribut)** : Povinný. Časové razítko pro tento záznam (v souladu s [RFC 4287](https://tools.ietf.org/html/rfc4287) sekce 3.3 a [RFC 3339](https://tools.ietf.org/html/rfc3339)). Datum může být také v zkráceném formátu yyyy-mm-dd (bez 'T'); jedná se o "full-date" formát v RFC 3339. V tomto formátu se pro jakékoliv zpracování předpokládá čas 00:00:00 UTC.

**minJavaVersion (atribut)** : Pokud je přítomen, minimální verze Javy vyžadovaná pro spuštění aktuální verze.

**minVersion (atribut)** : Pokud je přítomen, minimální verze routeru požadovaná pro aktualizaci na současnou verzi. Pokud je router starší než tato verze, uživatel musí (ručně?) nejprve aktualizovat na mezilehlou verzi.

**`<i2p:version>`** : Povinné. Nejnovější aktuální verze routeru k dispozici.

**`<i2p:update>`** : Soubor aktualizace (jeden nebo více). Musí obsahovat alespoň jeden podřízený prvek.   - type (atribut): "sud", "su2", nebo "su3". Musí být jedinečný napříč všemi prvky `<i2p:update>`.   - `<i2p:clearnet>`: Přímé odkazy ke stažení mimo síť (nula nebo více). href (atribut): Standardní clearnet http odkaz.   - `<i2p:clearnetssl>`: Přímé odkazy ke stažení mimo síť (nula nebo více). href (atribut): Standardní clearnet https odkaz.   - `<i2p:torrent>`: In-network magnet odkaz. href (atribut): Magnet odkaz.   - `<i2p:url>`: Přímé odkazy ke stažení v síti (nula nebo více). href (atribut): In-network http .i2p odkaz.

### Atom i2p:revocations Detaily

Tato entita je volitelná a v kanálu je maximálně jedna entita `<i2p:revocations>`. Tato funkce je podporována od verze 0.9.26.

Entita `<i2p:revocations>` obsahuje jednu nebo více entit `<i2p:crl>`. Entita `<i2p:crl>` obsahuje následující atributy:

**updated (atribut)** : Povinný. Časová značka pro tento záznam (odpovídající [RFC 4287](https://tools.ietf.org/html/rfc4287) sekci 3.3 a [RFC 3339](https://tools.ietf.org/html/rfc3339)). Datum může být také ve zkráceném formátu yyyy-mm-dd (bez 'T'); toto je formát "full-date" v RFC 3339. V tomto formátu se předpokládá, že čas je 00:00:00 UTC pro jakékoli zpracování.

**id (atribut)** : Povinný. Jedinečný identifikátor pro tvůrce tohoto CRL.

**(obsah entity)** : Povinné. Standardní base 64 kódovaný Certificate Revocation List (CRL) s novými řádky, začínající řádkem '-----BEGIN X509 CRL-----' a končící řádkem '-----END X509 CRL-----'. Více informací o CRL najdete v [RFC 5280](https://tools.ietf.org/html/rfc5280).

### Podrobnosti Atom i2p:blocklist

Tato entita je volitelná a ve feedu je nejvýše jedna entita `<i2p:blocklist>`. Tato funkce je naplánována k implementaci ve verzi 0.9.28.

Entita `<i2p:blocklist>` obsahuje jednu nebo více entit `<i2p:block>` nebo `<i2p:unblock>`, entitu "updated" a atributy "signer" a "sig":

**signer (atribut)** : Povinný. Jedinečný identifikátor (UTF-8) pro veřejný klíč použitý k podepsání tohoto blocklist.

**sig (atribut)** : Povinný. Podpis ve formátu code:b64sig, kde code je číslo typu podpisu v ASCII a b64sig je podpis kódovaný v base 64 (I2P abeceda). Viz níže pro specifikaci dat, která mají být podepsána.

**`<updated>`** : Povinné. Časová značka pro seznam blokovaných adres (v souladu s [RFC 4287](https://tools.ietf.org/html/rfc4287) sekce 3.3 a [RFC 3339](https://tools.ietf.org/html/rfc3339)). Datum může být také v zkráceném formátu yyyy-mm-dd (bez 'T'); toto je formát "full-date" v RFC 3339. V tomto formátu se čas považuje za 00:00:00 UTC pro jakékoliv zpracování.

**`<i2p:block>`** : Volitelný, povoleno více entit. Jedna položka, buď literální IPv4 nebo IPv6 adresa, nebo 44-znakový base 64 router hash (I2P abeceda). IPv6 adresy mohou být ve zkráceném formátu (obsahující "::"). Podpora pro položky s netmaskou, např. x.y.0.0/16, je volitelná. Podpora pro názvy hostitelů je volitelná.

**`<i2p:unblock>`** : Volitelné, více entit je povoleno. Stejný formát jako `<i2p:block>`.

**Specifikace podpisu:** Pro generování dat, která mají být podepsána nebo ověřena, spojte následující data v ASCII kódování: Aktualizovaný řetězec následovaný novým řádkem (ASCII 0x0a), poté každý blokový záznam v pořadí, jak byl přijat, s novým řádkem po každém, poté každý odblokový záznam v pořadí, jak byl přijat, s novým řádkem po každém.

## Specifikace souboru blokovaných položek

TBD, neimplementováno, viz návrh 130. Aktualizace seznamu blokovaných jsou doručovány v souboru news, viz výše.

## Budoucí práce

- Mechanismus aktualizace routeru je součástí webové router konzole. V současné době neexistuje žádné opatření pro aktualizace vestavěného routeru postrádajícího router konzoli.

## Reference

- **[CRYPTO-SIG]** [Kryptografie - Podpisy](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P Zdrojový kód](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Specifikace pluginu](/docs/specs/plugin)
- **[Python]** [Python RSA Raw Podpisy](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Datum a čas](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom Syndication Format](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Certificate Revocation Lists](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Typ Signature](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [Typ SigningPublicKey](/docs/specs/common-structures#signingpublickey)
