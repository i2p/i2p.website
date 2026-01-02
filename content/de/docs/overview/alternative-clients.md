---
title: "Alternative I2P-Clients"
description: "Von der Community gepflegte I2P-Client-Implementierungen (aktualisiert für 2025)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Die Haupt-I2P-Client-Implementierung verwendet **Java**. Wenn Sie Java auf einem bestimmten System nicht verwenden können oder möchten, gibt es alternative I2P-Client-Implementierungen, die von Community-Mitgliedern entwickelt und gepflegt werden. Diese Programme bieten dieselbe Kernfunktionalität unter Verwendung verschiedener Programmiersprachen oder Ansätze.

---

## Vergleichstabelle

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

**Website:** [https://i2pd.website](https://i2pd.website)

**Beschreibung:** i2pd (der *I2P Daemon*) ist ein voll funktionsfähiger I2P-Client, der in C++ implementiert ist. Er ist seit vielen Jahren stabil für den produktiven Einsatz (seit etwa 2016) und wird aktiv von der Community gepflegt. i2pd implementiert die I2P-Netzwerkprotokolle und -APIs vollständig, wodurch er vollständig kompatibel mit dem Java-I2P-Netzwerk ist. Dieser C++-Router wird oft als leichtgewichtige Alternative auf Systemen verwendet, auf denen die Java-Laufzeitumgebung nicht verfügbar oder nicht erwünscht ist. i2pd enthält eine integrierte webbasierte Konsole für Konfiguration und Überwachung. Es ist plattformübergreifend und in vielen Paketformaten verfügbar — es gibt sogar eine Android-Version von i2pd (zum Beispiel über F-Droid).

---

## Go-I2P (Go)

**Repository:** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**Beschreibung:** Go-I2P ist ein I2P-Client, der in der Programmiersprache Go geschrieben wurde. Es handelt sich um eine unabhängige Implementierung des I2P router, die darauf abzielt, die Effizienz und Portabilität von Go zu nutzen. Das Projekt befindet sich in aktiver Entwicklung, ist jedoch noch in einem frühen Stadium und noch nicht funktionsvollständig. Stand 2025 gilt Go-I2P als experimentell – es wird aktiv von Community-Entwicklern weiterentwickelt, ist jedoch noch nicht für den produktiven Einsatz empfohlen, bis es weiter ausgereift ist. Das Ziel von Go-I2P ist es, einen modernen, leichtgewichtigen I2P router mit voller Kompatibilität zum I2P-Netzwerk bereitzustellen, sobald die Entwicklung abgeschlossen ist.

---

## I2P+ (Java-Fork)

**Website:** [https://i2pplus.github.io](https://i2pplus.github.io)

**Beschreibung:** I2P+ ist ein von der Community gepflegter Fork des Standard-Java-I2P-Clients. Es handelt sich nicht um eine Neuimplementierung in einer anderen Programmiersprache, sondern um eine erweiterte Version des Java-routers mit zusätzlichen Funktionen und Optimierungen. I2P+ konzentriert sich darauf, eine verbesserte Benutzererfahrung und bessere Leistung zu bieten, während es vollständig kompatibel mit dem offiziellen I2P-Netzwerk bleibt. Es führt eine aufgefrischte Web-Konsolen-Oberfläche, benutzerfreundlichere Konfigurationsoptionen und verschiedene Optimierungen ein (zum Beispiel verbesserte Torrent-Leistung und bessere Handhabung von Netzwerk-Peers, insbesondere für router hinter Firewalls). I2P+ benötigt eine Java-Umgebung genau wie die offizielle I2P-Software, es ist also keine Lösung für Umgebungen ohne Java. Für Benutzer, die jedoch Java haben und einen alternativen Build mit zusätzlichen Funktionen wünschen, bietet I2P+ eine überzeugende Option. Dieser Fork wird mit den Upstream-I2P-Versionen auf dem neuesten Stand gehalten (wobei die Versionsnummerierung ein "+" anhängt) und kann von der Projekt-Website bezogen werden.
