---
title: "SOCKS-Proxy"
description: "I2Ps SOCKS-Tunnel sicher verwenden (aktualisiert für 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Achtung:** Der SOCKS-Tunnel leitet Anwendungsdaten ohne Bereinigung weiter. Viele Protokolle geben IPs, Hostnamen oder andere Identifikatoren preis. Verwenden Sie SOCKS nur mit Software, die Sie auf Anonymität geprüft haben.

---

## 1. Überblick

I2P bietet **SOCKS 4, 4a und 5** Proxy-Unterstützung für ausgehende Verbindungen über einen **I2PTunnel-Client**. Dies ermöglicht es Standardanwendungen, I2P-Ziele zu erreichen, kann aber **nicht auf das Clearnet zugreifen**. Es gibt **keinen SOCKS-Outproxy**, und der gesamte Datenverkehr bleibt innerhalb des I2P-Netzwerks.

### Implementierungszusammenfassung

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Unterstützte Adresstypen:** - `.i2p` Hostnamen (Adressbuch-Einträge) - Base32-Hashes (`.b32.i2p`) - Keine Unterstützung für Base64 oder Clearnet

---

## 2. Sicherheitsrisiken und Einschränkungen

### Anwendungsschicht-Leck

SOCKS arbeitet unterhalb der Anwendungsschicht und kann Protokolle nicht bereinigen. Viele Clients (z. B. Browser, IRC, E-Mail) enthalten Metadaten, die Ihre IP-Adresse, Ihren Hostnamen oder Systemdetails preisgeben.

Häufige Lecks umfassen: - IP-Adressen in E-Mail-Headern oder IRC-CTCP-Antworten   - Echte Namen/Benutzernamen in Protokoll-Payloads   - User-Agent-Strings mit Betriebssystem-Fingerabdrücken   - Externe DNS-Abfragen   - WebRTC und Browser-Telemetrie

**I2P kann diese Lecks nicht verhindern** – sie treten oberhalb der Tunnel-Ebene auf. Verwenden Sie SOCKS nur für **geprüfte Clients**, die für Anonymität entwickelt wurden.

### Gemeinsame Tunnel-Identität

Wenn mehrere Anwendungen einen SOCKS-Tunnel gemeinsam nutzen, teilen sie dieselbe I2P-destination-Identität. Dies ermöglicht eine Korrelation oder Fingerabdruckerstellung über verschiedene Dienste hinweg.

**Gegenmaßnahme:** Verwenden Sie **nicht gemeinsam genutzte Tunnel** für jede Anwendung und aktivieren Sie **persistente Schlüssel**, um konsistente kryptografische Identitäten über Neustarts hinweg beizubehalten.

### UDP-Modus auskommentiert

UDP-Unterstützung in SOCKS5 ist nicht implementiert. Das Protokoll wirbt mit UDP-Fähigkeit, aber Aufrufe werden ignoriert. Verwenden Sie nur TCP-Clients.

### Kein Outproxy nach Design

Anders als Tor bietet I2P **keine** SOCKS-basierten Clearnet-Outproxies. Versuche, externe IP-Adressen zu erreichen, werden fehlschlagen oder die Identität preisgeben. Verwenden Sie HTTP- oder HTTPS-Proxies, wenn Outproxying erforderlich ist.

---

## 3. Historischer Kontext

Entwickler haben lange davon abgeraten, SOCKS für anonyme Nutzung zu verwenden. Aus internen Entwicklerdiskussionen und den Treffen von 2004 [Meeting 81](/de/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) und [Meeting 82](/de/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> "Das Weiterleiten von beliebigem Datenverkehr ist unsicher, und es obliegt uns als Entwicklern von Anonymitätssoftware, die Sicherheit unserer Endnutzer stets im Vordergrund zu haben."

SOCKS-Unterstützung wurde aus Kompatibilitätsgründen aufgenommen, wird aber nicht für Produktionsumgebungen empfohlen. Nahezu jede Internetanwendung gibt sensible Metadaten preis, die für anonymes Routing ungeeignet sind.

---

## 4. Konfiguration

### Java I2P

1. Öffnen Sie den [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Erstellen Sie einen neuen Client-Tunnel vom Typ **"SOCKS 4/4a/5"**  
3. Konfigurieren Sie die Optionen:  
   - Lokaler Port (beliebiger verfügbarer Port)  
   - Shared client: *deaktivieren* für separate Identität pro Anwendung  
   - Persistent key: *aktivieren*, um Schlüsselkorrelation zu reduzieren  
4. Starten Sie den Tunnel

### i2pd

i2pd enthält SOCKS5-Unterstützung, die standardmäßig unter `127.0.0.1:4447` aktiviert ist. Die Konfiguration in `i2pd.conf` unter `[SOCKSProxy]` ermöglicht es Ihnen, Port, Host und tunnel-Parameter anzupassen.

---

## 5. Entwicklungszeitplan

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
Das SOCKS-Modul selbst hat seit 2013 keine größeren Protokoll-Updates erhalten, aber der umgebende Tunnel-Stack hat Leistungs- und kryptografische Verbesserungen erfahren.

---

## 6. Empfohlene Alternativen

Für jede **Produktions-**, **öffentlich zugängliche** oder **sicherheitskritische** Anwendung verwenden Sie eine der offiziellen I2P-APIs anstelle von SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Diese APIs bieten ordnungsgemäße Zieltrennung, kryptografische Identitätskontrolle und bessere Routing-Leistung.

---

## 7. OnionCat / GarliCat

OnionCat unterstützt I2P durch seinen GarliCat-Modus (`fd60:db4d:ddb5::/48` IPv6-Bereich). Weiterhin funktionsfähig, aber mit eingeschränkter Entwicklung seit 2019.

**Nutzungseinschränkungen:** - Erfordert manuelle `.oc.b32.i2p`-Konfiguration in SusiDNS   - Benötigt statische IPv6-Zuweisung   - Wird nicht offiziell vom I2P-Projekt unterstützt

Nur für fortgeschrittene VPN-über-I2P-Setups empfohlen.

---

## 8. Bewährte Verfahren

Falls Sie SOCKS verwenden müssen: 1. Erstellen Sie separate Tunnel pro Anwendung. 2. Deaktivieren Sie den gemeinsamen Client-Modus. 3. Aktivieren Sie persistente Schlüssel. 4. Erzwingen Sie SOCKS5-DNS-Auflösung. 5. Überprüfen Sie das Protokollverhalten auf Lecks. 6. Vermeiden Sie Clearnet-Verbindungen. 7. Überwachen Sie den Netzwerkverkehr auf Lecks.

---

## 9. Technische Zusammenfassung

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Fazit

Der SOCKS-Proxy in I2P bietet grundlegende Kompatibilität mit bestehenden TCP-Anwendungen, ist jedoch **nicht für starke Anonymitätsgarantien ausgelegt**. Er sollte nur in kontrollierten, geprüften Testumgebungen verwendet werden.

> Für ernsthafte Bereitstellungen migrieren Sie zu **SAM v3** oder der **Streaming API**. Diese APIs isolieren Anwendungsidentitäten, verwenden moderne Kryptographie und werden kontinuierlich weiterentwickelt.

---

### Zusätzliche Ressourcen

- [Offizielle SOCKS-Dokumentation](/docs/api/socks/)  
- [SAM v3 Spezifikation](/docs/api/samv3/)  
- [Streaming Library Dokumentation](/docs/specs/streaming/)  
- [I2PTunnel Referenz](/docs/specs/implementation/)  
- [I2P Entwickler-Dokumentation](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Community-Forum](https://i2pforum.net)
