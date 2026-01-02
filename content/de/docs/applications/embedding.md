---
title: "I2P in Ihre Anwendung einbetten"
description: "Aktualisierte praktische Anleitung zum verantwortungsvollen Bündeln eines I2P-Routers mit Ihrer Anwendung"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Die Bündelung von I2P mit Ihrer Anwendung ist eine leistungsstarke Möglichkeit, Benutzer einzubinden – aber nur, wenn der Router verantwortungsvoll konfiguriert ist.

## 1. Koordination mit Router-Teams

- Kontaktieren Sie die **Java I2P** und **i2pd** Maintainer vor dem Bundling. Sie können Ihre Standardeinstellungen überprüfen und auf Kompatibilitätsprobleme hinweisen.
- Wählen Sie die Router-Implementierung, die zu Ihrem Stack passt:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Andere Sprachen** → bündeln Sie einen Router und integrieren Sie ihn mit [SAM v3](/docs/api/samv3/) oder [I2CP](/docs/specs/i2cp/)
- Überprüfen Sie die Weiterverteilungsbedingungen für Router-Binärdateien und Abhängigkeiten (Java Runtime, ICU, etc.).

## 2. Empfohlene Standard-Konfiguration

Streben Sie danach, "mehr beizutragen als Sie verbrauchen." Moderne Standardeinstellungen priorisieren die Netzwerkgesundheit und -stabilität.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Teilnehmende Tunnel bleiben unverzichtbar

Deaktivieren Sie **nicht** die Teilnahme an Tunneln.

1. Router, die nicht weiterleiten, haben selbst eine schlechtere Leistung.
2. Das Netzwerk ist auf freiwillige Kapazitätsteilung angewiesen.
3. Cover-Traffic (weitergeleiteter Verkehr) verbessert die Anonymität.

**Offizielle Mindestwerte:** - Gemeinsam genutzte Bandbreite: ≥ 12 KB/s   - Floodfill automatische Aktivierung: ≥ 128 KB/s   - Empfohlen: 2 eingehende / 2 ausgehende Tunnel (Java I2P Standard)

## 3. Persistenz und Reseeding

Persistente Statusverzeichnisse (`netDb/`, profiles, certificates) müssen zwischen den Ausführungen erhalten bleiben.

Ohne Persistenz lösen Ihre Benutzer bei jedem Start reseeds aus – was die Leistung beeinträchtigt und die Last auf reseed-Servern erhöht.

Wenn Persistenz nicht möglich ist (z.B. bei Containern oder temporären Installationen):

1. Bündeln Sie **1.000–2.000 Router-Infos** im Installationsprogramm.
2. Betreiben Sie einen oder mehrere eigene Reseed-Server, um öffentliche zu entlasten.

Konfigurationsvariablen: - Basisverzeichnis: `i2p.dir.base` - Konfigurationsverzeichnis: `i2p.dir.config` - Enthält `certificates/` für das Reseeding.

## 4. Sicherheit und Offenlegung

- Halten Sie die Router-Konsole (`127.0.0.1:7657`) nur lokal verfügbar.
- Verwenden Sie HTTPS, wenn Sie die Benutzeroberfläche extern bereitstellen.
- Deaktivieren Sie externe SAM/I2CP-Verbindungen, sofern nicht erforderlich.
- Überprüfen Sie die enthaltenen Plugins – liefern Sie nur das aus, was Ihre Anwendung unterstützt.
- Verwenden Sie immer Authentifizierung für den Fernzugriff auf die Konsole.

**Sicherheitsfunktionen seit Version 2.5.0:** - NetDB-Isolation zwischen Anwendungen (2.4.0+)   - DoS-Schutz und Tor-Blockierlisten (2.5.1)   - NTCP2-Widerstandsfähigkeit gegen Probing (2.9.0)   - Verbesserungen bei der Floodfill-Router-Auswahl (2.6.0+)

## 5. Unterstützte APIs (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Alle offiziellen Dokumentationen befinden sich unter `/docs/api/` — der alte Pfad `/spec/samv3/` existiert **nicht**.

## 6. Netzwerk und Ports

Typische Standardports: - 4444 – HTTP-Proxy   - 4445 – HTTPS-Proxy   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router-Konsole   - 7658 – Lokale I2P-Site   - 6668 – IRC-Proxy   - 9000–31000 – Zufälliger Router-Port (UDP/TCP eingehend)

Router wählen beim ersten Start einen zufälligen eingehenden Port. Portweiterleitung verbessert die Leistung, aber UPnP kann dies möglicherweise automatisch handhaben.

## 7. Moderne Änderungen (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Benutzererfahrung und Testing

- Kommunizieren, was I2P tut und warum Bandbreite geteilt wird.
- Router-Diagnosen bereitstellen (Bandbreite, tunnels, Reseed-Status).
- Bundles auf Windows, macOS und Linux testen (einschließlich Low-RAM).
- Interoperabilität mit **Java I2P** und **i2pd** Peers überprüfen.
- Wiederherstellung nach Netzwerkausfällen und ungraceful Exits testen.

## 9. Community-Ressourcen

- Forum: [i2pforum.net](https://i2pforum.net) oder `http://i2pforum.i2p` innerhalb von I2P.  
- Code: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (Irc2P-Netzwerk): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` unbestätigt; existiert möglicherweise nicht.  
  - Bitte klären Sie, welches Netzwerk (Irc2P vs ilita.i2p) Ihren Kanal hostet.

Verantwortungsvolles Einbetten bedeutet, Benutzererfahrung, Leistung und Netzwerkbeitrag in Einklang zu bringen. Verwenden Sie diese Standardeinstellungen, bleiben Sie mit den Router-Entwicklern synchron und testen Sie unter realen Lastbedingungen vor der Veröffentlichung.
