---
title: "Diskussion zur Namensgebung"
description: "Historische Debatte über das Namensmodell von I2P und warum globale DNS-ähnliche Schemata verworfen wurden"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Kontext:** Diese Seite archiviert langjährige Debatten aus der frühen Phase des I2P-Designs. Sie erläutert, warum das Projekt lokal vertraute Adressbücher gegenüber DNS-ähnlichen Abfragen oder mehrheitsbasierten Registern bevorzugte. Hinweise zur aktuellen Nutzung finden Sie in der [Dokumentation zur Namensgebung](/docs/overview/naming/).

## Verworfene Alternativen

I2Ps Sicherheitsziele schließen gängige Namensschemata aus:

- **DNS-ähnliche Namensauflösung.** Jeder Resolver auf dem Abfragepfad könnte Antworten fälschen oder zensieren. Selbst mit DNSSEC bleiben kompromittierte Registrare oder Zertifizierungsstellen ein einzelner Ausfallpunkt. In I2P sind Destinationen *sind* öffentliche Schlüssel—die Übernahme einer Abfrage würde eine Identität vollständig kompromittieren.
- **Abstimmungsbasierte Namensgebung.** Ein Angreifer kann unbegrenzt Identitäten erzeugen (ein Sybil-Angriff) und Stimmen für populäre Namen „gewinnen“. Proof-of-Work (Arbeitsnachweis)-Gegenmaßnahmen erhöhen die Kosten, führen jedoch zu erheblichem Koordinationsaufwand.

Stattdessen belässt I2P die Namensauflösung bewusst oberhalb der Transportschicht. Die mitgelieferte Naming-Bibliothek bietet ein service-provider interface (Schnittstelle für Dienstanbieter) an, sodass alternative Schemata koexistieren können—Nutzer entscheiden, welchen Adressbüchern oder Jump Services (Sprungdienste) sie vertrauen.

## Lokale gegenüber globalen Namen (jrandom, 2005)

- Namen in I2P sind **lokal eindeutig, aber menschenlesbar**. Ihr `boss.i2p` muss nicht mit dem `boss.i2p` von jemand anderem übereinstimmen, und das ist so vorgesehen.
- Wenn ein böswilliger Akteur Sie dazu brächte, die Zieladresse hinter einem Namen zu ändern, würde er damit effektiv einen Dienst kapern. Der Verzicht auf globale Eindeutigkeit verhindert diese Art von Angriff.
- Behandeln Sie Namen wie Lesezeichen oder IM-Spitznamen — Sie wählen selbst, welchen Zieladressen Sie vertrauen, indem Sie bestimmte Adressbücher abonnieren oder Schlüssel manuell hinzufügen.

## Häufige Einwände & Antworten (zzz)

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
## Besprochene Ideen zur Effizienzsteigerung

- Inkrementelle Updates bereitstellen (nur Destinations (I2P-Zieladressen), die seit dem letzten Abruf hinzugefügt wurden).
- Ergänzende Feeds (`recenthosts.cgi`) neben vollständigen Hosts-Dateien anbieten.
- Skriptfähige Werkzeuge erkunden (zum Beispiel `i2host.i2p`), um Feeds zusammenzuführen oder nach Vertrauensebenen zu filtern.

## Wesentliche Erkenntnisse

- Sicherheit hat Vorrang vor globalem Konsens: lokal gepflegte Adressbücher minimieren das Risiko von Hijacking.
- Mehrere Namensansätze können über die Naming-API koexistieren—Nutzer entscheiden selbst, was sie als vertrauenswürdig erachten.
- Völlig dezentrale globale Namensgebung bleibt ein offenes Forschungsproblem; die Abwägungen zwischen Sicherheit, menschlicher Merkfähigkeit und globaler Eindeutigkeit spiegeln weiterhin [Zookos Dreieck](https://zooko.com/distnames.html) wider.

## Referenzen

- [Dokumentation zum Namenssystem](/docs/overview/naming/)
- [Zookos “Names: Decentralized, Secure, Human-Meaningful: Choose Two”](https://zooko.com/distnames.html)
- Beispiel für einen inkrementellen Feed: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
