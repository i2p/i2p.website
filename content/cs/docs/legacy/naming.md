---
title: "Diskuse o pojmenování"
description: "Historická debata o modelu pojmenování I2P a proč byla globální schémata ve stylu DNS odmítnuta"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Kontext:** Tato stránka archivuje dlouhodobé diskuse z rané éry návrhu I2P. Vysvětluje, proč projekt upřednostnil lokálně důvěryhodné adresáře před vyhledáváním ve stylu DNS nebo registry založenými na většinovém hlasování. Aktuální pokyny k používání najdete v [dokumentaci k pojmenovávání](/docs/overview/naming/).

## Zamítnuté alternativy

Bezpečnostní cíle I2P vylučují obvyklá schémata pojmenování:

- **Překlad názvů ve stylu DNS.** Jakýkoli resolver na trase dotazu může podvrhovat nebo cenzurovat odpovědi. I s DNSSEC zůstávají kompromitovaní registrátoři nebo certifikační autority jediným bodem selhání. V I2P *jsou* destinace veřejné klíče—únos dotazu by zcela kompromitoval identitu.
- **Pojmenování založené na hlasování.** Útočník může vytvářet neomezené množství identit (útok Sybil) a “vyhrát” hlasování pro populární názvy. Mitigace pomocí proof-of-work (důkaz o vykonané práci) zvyšují náklady, ale zavádějí výraznou koordinační režii.

Namísto toho I2P záměrně ponechává pojmenovávání nad transportní vrstvou. Přibalená knihovna pro pojmenovávání nabízí rozhraní pro poskytovatele služeb, díky čemuž mohou koexistovat alternativní schémata — uživatelé rozhodují, kterým seznamům adres nebo jump services (službám pro dohledání jmen) důvěřují.

## Lokální vs globální jména (jrandom, 2005)

- Názvy v I2P jsou **lokálně jedinečné, ale lidsky čitelné**. Vaše `boss.i2p` se nemusí shodovat s `boss.i2p` někoho jiného, a je to tak záměrně.
- Pokud by vás zlovolný útočník přiměl změnit destinaci skrytou za názvem, fakticky by tím unesl službu. Nevyžadování globální jedinečnosti tomuto typu útoku brání.
- Zacházejte s názvy jako se záložkami nebo přezdívkami v chatovacích aplikacích—vy si vybíráte, kterým destinacím budete důvěřovat, a to přihlášením k odběru konkrétních adresářů adres nebo ručním přidáním klíčů.

## Časté námitky & odpovědi (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Probrané nápady na zvýšení efektivity

- Poskytovat přírůstkové aktualizace (pouze destinace přidané od posledního načtení).
- Nabízet doplňkové kanály (`recenthosts.cgi`) vedle kompletních souborů hosts.
- Prozkoumat skriptovatelné nástroje (například `i2host.i2p`) pro slučování kanálů nebo filtrování podle úrovní důvěry.

## Hlavní poznatky

- Bezpečnost má přednost před globálním konsensem: lokálně spravované adresáře minimalizují riziko únosu.
- Více přístupů k pojmenování může koexistovat prostřednictvím naming API (rozhraní pro pojmenování)—uživatelé rozhodují, čemu budou důvěřovat.
- Zcela decentralizované globální pojmenování zůstává otevřeným výzkumným problémem; kompromisy mezi bezpečností, lidskou zapamatovatelností a globální jedinečností stále odrážejí [Zookův trojúhelník](https://zooko.com/distnames.html).

## Reference

- [Dokumentace k pojmenování](/docs/overview/naming/)
- [Zookův „Jména: decentralizovaná, bezpečná, srozumitelná pro člověka: vyberte dvě“](https://zooko.com/distnames.html)
- Ukázkový inkrementální kanál: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
