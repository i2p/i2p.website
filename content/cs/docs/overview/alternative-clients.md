---
title: "Alternativní I2P klienti"
description: "Komunitou spravované implementace I2P klienta (aktualizováno pro rok 2025)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Hlavní implementace I2P klienta používá **Java**. Pokud na konkrétním systému nemůžete nebo nechcete používat Javu, existují alternativní implementace I2P klienta vyvíjené a udržované členy komunity. Tyto programy poskytují stejnou základní funkčnost s využitím různých programovacích jazyků nebo přístupů.

---

## Srovnávací tabulka

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**Webové stránky:** [https://i2pd.website](https://i2pd.website)

**Popis:** i2pd (*I2P Daemon*) je plně vybavený I2P klient implementovaný v C++. Je stabilní pro produkční použití již mnoho let (přibližně od roku 2016) a je aktivně udržován komunitou. i2pd plně implementuje síťové protokoly a API I2P, což ho činí zcela kompatibilním se sítí Java I2P. Tento C++ router je často používán jako odlehčená alternativa na systémech, kde Java runtime není k dispozici nebo není žádoucí. i2pd obsahuje vestavěnou webovou konzoli pro konfiguraci a monitorování. Je multiplatformní a dostupný v mnoha balíčkovacích formátech — existuje dokonce i Android verze i2pd (například prostřednictvím F-Droid).

---

## Go-I2P (Go)

**Repozitář:** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**Popis:** Go-I2P je I2P klient napsaný v programovacím jazyce Go. Jedná se o nezávislou implementaci I2P routeru, která se snaží využít efektivity a přenositelnosti jazyka Go. Projekt je aktivně vyvíjen, ale stále se nachází v rané fázi a zatím není plně funkční. K roku 2025 je Go-I2P považován za experimentální — je aktivně vyvíjen komunitními vývojáři, ale není doporučen pro produkční použití, dokud nedosáhne vyšší úrovně zralosti. Cílem Go-I2P je poskytnout moderní, odlehčený I2P router s plnou kompatibilitou se sítí I2P po dokončení vývoje.

---

## I2P+ (Java fork)

**Webová stránka:** [https://i2pplus.github.io](https://i2pplus.github.io)

**Popis:** I2P+ je komunitou udržovaná odnož standardního Java I2P klienta. Nejedná se o reimplementaci v novém jazyce, ale spíše o vylepšenou verzi Java routeru s dodatečnými funkcemi a optimalizacemi. I2P+ se zaměřuje na poskytování vylepšené uživatelské zkušenosti a lepšího výkonu při zachování plné kompatibility s oficiální I2P sítí. Přináší osvěženější rozhraní webové konzole, uživatelsky přívětivější možnosti konfigurace a různé optimalizace (například zlepšený výkon torrentů a lepší správu síťových peerů, zejména pro routery za firewally). I2P+ vyžaduje Java prostředí stejně jako oficiální I2P software, takže není řešením pro prostředí bez Javy. Pro uživatele, kteří však Java mají a chtějí alternativní sestavení s extra možnostmi, poskytuje I2P+ přesvědčivou volbu. Tato odnož je udržována aktuální s upstream I2P vydáními (s číslem verze doplněným o "+") a lze ji získat z webové stránky projektu.
