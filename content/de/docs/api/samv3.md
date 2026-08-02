---
title: "SAM V3"
description: "Einfaches anonymes Nachrichtenprotokoll für Nicht-Java-I2P-Anwendungen"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM ist ein einfaches Clientprotokoll zur Interaktion mit I2P. SAM ist das empfohlene Protokoll für Nicht-Java-Anwendungen, um eine Verbindung zum I2P-Netzwerk herzustellen, und wird von mehreren Router-Implementierungen unterstützt. Java-Anwendungen sollten die Streaming- oder I2CP-APIs direkt verwenden.

SAM-Version 3 wurde mit dem I2P-Release 0.7.3 (Mai 2009) eingeführt und ist eine stabile und unterstützte Schnittstelle. 3.1 ist ebenfalls stabil und unterstützt die Signaturtyp-Option, deren Nutzung dringend empfohlen wird. Neuere 3.x-Versionen unterstützen erweiterte Funktionen. Beachten Sie, dass i2pd derzeit die meisten Funktionen von 3.2 und 3.3 nicht unterstützt.

Alternativen: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (veraltet)](/docs/api/bob). Veraltete Versionen: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Bekannte SAM-Bibliotheken

Warnung: Einige davon können sehr alt oder nicht mehr unterstützt sein. Keines wird vom I2P-Projekt getestet, überprüft oder gewartet, es sei denn, dies wird unten angegeben. Führen Sie Ihre eigene Recherche durch.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Schnellstart

Um eine grundlegende TCP-only Peer-to-Peer-Anwendung zu implementieren, muss der Client die folgenden Befehle unterstützen:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Wird für alle folgenden Befehle benötigt
- `DEST GENERATE SIGNATURE_TYPE=7` - Zum Generieren unseres privaten Schlüssels und der Destination
- `NAMING LOOKUP NAME=...` - Zum Umwandeln von .i2p-Adressen in Destinations
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Wird für STREAM CONNECT und STREAM ACCEPT benötigt
- `STREAM CONNECT ID=... DESTINATION=...` - Zum Herstellen ausgehender Verbindungen
- `STREAM ACCEPT ID=...` - Zum Annehmen eingehender Verbindungen

## Allgemeine Anleitung für Entwickler

### Anwendungsentwurf

SAM-Sitzungen (oder innerhalb von I2P, Tunnel-Pools oder Gruppen von Tunneln) sind darauf ausgelegt, langfristig bestehen zu bleiben. Die meisten Anwendungen benötigen nur eine Sitzung, die beim Start erstellt und beim Beenden geschlossen wird. I2P unterscheidet sich von Tor, bei dem Circuits schnell erstellt und verworfen werden können. Überlegen Sie genau und konsultieren Sie die I2P-Entwickler, bevor Sie Ihre Anwendung so entwerfen, dass sie mehr als eine oder zwei gleichzeitige Sitzungen verwendet oder diese schnell erstellt und verwirft. Die meisten Bedrohungsmodelle erfordern keine eindeutige Sitzung für jede Verbindung.

Bitte stellen Sie außerdem sicher, dass die Einstellungen Ihrer Anwendung (sowie die Anleitung für Benutzer bezüglich Router-Einstellungen oder die Standardwerte des Routers, falls Sie einen Router bündeln) dazu führen, dass Ihre Benutzer mehr Ressourcen in das Netzwerk einbringen, als sie verbrauchen. I2P ist ein Peer-to-Peer-Netzwerk, und das Netzwerk kann nicht überleben, wenn eine beliebte Anwendung es in eine dauerhafte Überlastung treibt.

### Kompatibilität und Tests

Die Java-I2P- und i2pd-Router-Implementierungen sind unabhängig voneinander und weisen geringfügige Unterschiede im Verhalten, bei der Funktionsunterstützung und den Standardeinstellungen auf. Bitte testen Sie Ihre Anwendung mit der neuesten Version beider Router.

i2pd SAM ist standardmäßig aktiviert; Java I2P SAM ist es nicht. Geben Sie Ihren Benutzern Anweisungen, wie sie SAM in Java I2P aktivieren können (über /configclients in der Routerkonsole), und/oder zeigen Sie eine aussagekräftige Fehlermeldung an, falls die erste Verbindung fehlschlägt, z. B. „Stellen Sie sicher, dass I2P läuft und die SAM-Schnittstelle aktiviert ist“.

Die Java I2P- und i2pd-Router verwenden unterschiedliche Standardwerte für die Anzahl der Tunnel. Der Standardwert für Java ist 2, während i2pd den Wert 5 verwendet. Für die meisten Anwendungen mit geringer bis mittlerer Bandbreitennutzung und geringer bis mittlerer Anzahl an Verbindungen sind 2 oder 3 ausreichend. Bitte geben Sie die Tunnelanzahl in der SESSION CREATE-Nachricht an, um eine einheitliche Leistung mit den Java I2P- und i2pd-Routern zu erzielen. Siehe unten.

Für weitere Anleitungen an Entwickler, wie sichergestellt werden kann, dass Ihre Anwendung nur die Ressourcen verwendet, die sie benötigt, siehe [unser Leitfaden zum Einbetten von I2P in Ihre Anwendung](/docs/applications/embedding).

### Signatur- und Verschlüsselungstypen

I2P unterstützt mehrere Signatur- und Verschlüsselungstypen. Aus Gründen der Abwärtskompatibilität verwendet SAM standardmäßig alte und ineffiziente Typen, daher sollten alle Clients neuere Typen angeben.

Der Signaturtyp wird in den Befehlen DEST GENERATE und SESSION CREATE (für transient) angegeben. Alle Clients sollten `SIGNATURE_TYPE=7` (Ed25519) setzen.

Der Verschlüsselungstyp wird im SESSION CREATE-Befehl angegeben. Mehrere Verschlüsselungstypen sind erlaubt. Clients sollten entweder `i2cp.leaseSetEncType=4` (nur für ECIES-X25519) oder `i2cp.leaseSetEncType=6,4` (für MLKEM-768 und ECIES-X25519, für Router mit API 0.9.67 oder höher) setzen.

## Änderungen in Version 3

### Änderungen in Version 3.0

Version 3.0 wurde mit dem I2P-Release 0.7.3 eingeführt. SAM v2 ermöglichte es, mehrere Sockets auf demselben I2P-Ziel *parallel* zu verwalten, d. h., der Client musste nicht warten, bis Daten erfolgreich über einen Socket gesendet wurden, bevor er Daten über einen anderen Socket versendete. Allerdings liefen alle Daten über denselben Client-zu-SAM-Socket, was für den Client recht kompliziert zu verwalten war.

SAM v3 verwaltet Sockets auf eine andere Weise: Jeder *I2P-Socket* entspricht einem eindeutigen Client-zu-SAM-Socket, was wesentlich einfacher zu handhaben ist. Dies ist ähnlich wie bei [BOB](/docs/api/bob).

SAM v3 bietet auch einen UDP-Port zum Senden von Datagrammen über I2P und kann I2P-Datagramme an den Datagramm-Server des Clients zurückleiten.

### Änderungen in Version 3.1

Version 3.1 wurde mit der Java-I2P-Version 0.9.14 (Juli 2014) eingeführt. SAM 3.1 ist die empfohlene Mindestversion für eine SAM-Implementierung, da sie bessere Signaturtypen als SAM 3.0 unterstützt. i2pd unterstützt ebenfalls die meisten Funktionen von 3.1.

- DEST GENERATE und SESSION CREATE unterstützen jetzt einen SIGNATURE_TYPE-Parameter.
- Die MIN- und MAX-Parameter in HELLO VERSION sind jetzt optional.
- Die MIN- und MAX-Parameter in HELLO VERSION unterstützen jetzt einstellige Versionen wie „3“.
- RAW SEND wird jetzt auf dem Bridge-Socket unterstützt.

### Änderungen in Version 3.2

Version 3.2 wurde mit dem Java I2P-Release 0.9.24 (Januar 2016) eingeführt. Beachten Sie, dass i2pd derzeit die meisten Funktionen von Version 3.2 nicht unterstützt.

#### Unterstützung für I2CP-Port und -Protokoll

- SESSION CREATE-Optionen FROM_PORT und TO_PORT
- SESSION CREATE STYLE=RAW-Option PROTOCOL
- STREAM CONNECT-, DATAGRAM SEND- und RAW SEND-Optionen FROM_PORT und TO_PORT
- RAW SEND-Option PROTOCOL
- DATAGRAM RECEIVED, RAW RECEIVED sowie weitergeleitete oder empfangene Streams und repliable Datagrams enthalten FROM_PORT und TO_PORT
- Die RAW-Session-Option HEADER=true bewirkt, dass den weitergeleiteten Raw-Datagrammen eine Zeile mit PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn vorangestellt wird
- Die erste Zeile von Datagrammen, die über Port 7655 gesendet werden, darf nun mit einer beliebigen 3.x-Version beginnen
- Die erste Zeile von Datagrammen, die über Port 7655 gesendet werden, darf eine der Optionen FROM_PORT, TO_PORT, PROTOCOL enthalten
- RAW RECEIVED enthält PROTOCOL=nnn

#### SSL und Authentifizierung

- BENUTZER/KENNWORT in den HELLO-Parametern zur Autorisierung. Siehe [unten](#authorization).
- Optionale Autorisierungskonfiguration mit dem AUTH-Befehl. Siehe [unten](#authorization-configuration-sam-32-or-higher-optional-feature).
- Optionale SSL/TLS-Unterstützung am Steckplatz. Siehe [unten](#ssl).
- STREAM FORWARD-Option SSL=true

#### Multithreading

- Gleichzeitige ausstehende STREAM ACCEPTs sind für dieselbe Sitzungs-ID erlaubt.

#### Befehlszeilenverarbeitung und Keepalive

- Optionale Befehle QUIT, STOP und EXIT zum Schließen der Sitzung und des Sockets. Siehe [unten](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- Die Befehlsverarbeitung behandelt UTF-8 korrekt.
- Die Befehlsverarbeitung verarbeitet Leerzeichen innerhalb von Anführungszeichen zuverlässig.
- Ein Backslash '\\' kann Anführungszeichen in der Befehlszeile escapen.
- Es wird empfohlen, dass der Server Befehle in Großbuchstaben abbildet, um die Tests per Telnet zu vereinfachen.
- Leere Optionswerte wie PROTOCOL oder PROTOCOL= können erlaubt sein, abhängig von der Implementierung.
- PING/PONG für die Verbindungsaktivität (keepalive). Siehe unten.
- Server können Timeouts für den HELLO-Befehl oder nachfolgende Befehle implementieren, abhängig von der Implementierung.

### Änderungen in Version 3.3

Version 3.3 wurde mit der Java-I2P-Version 0.9.25 (März 2016) eingeführt. Beachten Sie, dass i2pd derzeit die meisten Funktionen von Version 3.3 nicht unterstützt.

- Derselbe Session kann gleichzeitig für Streams, Datagramme und Raw verwendet werden. Eingehende Pakete und Streams werden basierend auf dem I2P-Protokoll und dem Ziel-Port weitergeleitet. Siehe [den PRIMARY-Abschnitt weiter unten](#sam-primary-sessions-v33-and-higher).
- DATAGRAM SEND und RAW SEND unterstützen jetzt die Optionen SEND_TAGS, TAG_THRESHOLD, EXPIRES und SEND_LEASESET. Siehe [den Abschnitt zum Senden von Datagrammen weiter unten](#sending-repliable-or-raw-datagrams).

### Änderungen vom 2025-04

Zwei Vorschläge wurden im April 2025 genehmigt und in die Spezifikation aufgenommen. Es gibt keine Versionsänderung, um die Unterstützung anzuzeigen. Einige Implementierungen unterstützen dies noch nicht, und bei anderen ist die Unterstützung vorläufig.

- Unterstützung für Datagramm 2/3 (Vorschlag 163). Wird in SESSION CREATE und SESSION ADD (Untersitzungen) angegeben. Siehe unten.
- Abruf von Leaseset-Optionen (Vorschlag 167). Wird mit NAMING LOOKUP OPTIONS=true angegeben. Siehe unten.

## Version-3-Protokoll

### Übersicht über die Spezifikation der Simple Anonymous Messaging (SAM) Version 3.3

Die Client-Anwendung kommuniziert mit der SAM-Brücke, die sämtliche I2P-Funktionalitäten abwickelt (unter Verwendung der [Streaming-Bibliothek](/docs/api/streaming) für virtuelle Streams oder direkt [I2CP](/docs/protocol/i2cp) für Datagramme).

Standardmäßig ist die Kommunikation zwischen Client und SAM-Brücke unverschlüsselt und nicht authentifiziert. Die SAM-Brücke kann SSL/TLS-Verbindungen unterstützen; Konfigurations- und Implementierungsdetails dazu liegen außerhalb des Geltungsbereichs dieser Spezifikation. Ab SAM 3.2 werden optionale Authentifizierungsparameter Benutzer/Passwort im initialen Handshake unterstützt und können von der Brücke verlangt werden.

I2P-Kommunikation kann verschiedene deutliche Formen annehmen:

- [Virtuelle Streams](/docs/api/streaming)
- [Antwortfähige und authentifizierte Datagramme](/docs/specs/datagrams#repliable) (Nachrichten mit einem FROM-Feld)
- [Anonyme Datagramme](/docs/specs/datagrams#raw) (rohe anonyme Nachrichten)
- [Datagram2](/docs/specs/datagrams#datagram2) (ein neues Antwort-fähiges und authentifiziertes Format)
- [Datagram3](/docs/specs/datagrams#datagram3) (ein neues Antwort-fähiges, aber nicht authentifiziertes Format)

I2P-Kommunikationen werden durch I2P-Sitzungen unterstützt, und jede I2P-Sitzung ist an eine Adresse (genannt „destination“) gebunden. Eine I2P-Sitzung ist einem der drei oben genannten Typen zugeordnet und kann keine Kommunikation eines anderen Typs übertragen, es sei denn, [PRIMARY-Sitzungen](#sam-primary-sessions-v33-and-higher) werden verwendet.

### Codierung und Maskierung

Alle diese SAM-Nachrichten werden in einer einzelnen Zeile gesendet und durch das Zeilenumbruchzeichen (\\n) abgeschlossen. Vor SAM 3.2 wurde nur 7-Bit-ASCII unterstützt. Ab SAM 3.2 muss die Kodierung UTF-8 sein. Alle Schlüssel oder Werte, die in UTF-8 kodiert sind, sollten funktionieren.

Die in dieser Spezifikation gezeigte Formatierung dient lediglich der besseren Lesbarkeit. Während die ersten beiden Wörter jeder Nachricht ihre spezifische Reihenfolge beibehalten müssen, kann die Reihenfolge der Schlüssel=Wert-Paare geändert werden (z. B. sind „ONE TWO A=B C=D“ oder „ONE TWO C=D A=B“ beide gültige Formen). Außerdem ist das Protokoll groß- und kleinSchreibung-sensitiv. Im Folgenden wird jeder Nachrichtenbeispiel ein „->“ vorangestellt, wenn die Nachricht vom Client an die SAM-Brücke gesendet wird, bzw. ein „<-“, wenn die Nachricht von der SAM-Brücke an den Client gesendet wird.

Die grundlegende Befehls- oder Antwortzeile hat eine der folgenden Formen:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
COMMAND ohne SUBCOMMAND wird nur für einige neue Befehle in SAM 3.2 unterstützt.

Schlüssel=Wert-Paare müssen durch ein einzelnes Leerzeichen getrennt werden. (Ab SAM 3.2 sind mehrere Leerzeichen erlaubt) Werte müssen in doppelte Anführungszeichen eingeschlossen werden, wenn sie Leerzeichen enthalten, z. B. key="langer Wertetext". (Vor SAM 3.2 funktionierte dies in einigen Implementierungen nicht zuverlässig)

Vor SAM 3.2 gab es keinen Escape-Mechanismus. Ab SAM 3.2 können doppelte Anführungszeichen mit einem umgekehrten Schrägstrich „\“ maskiert werden, und ein einzelner umgekehrter Schrägstrich kann als zwei umgekehrte Schrägstriche „\\\\“ dargestellt werden.

### Leere Werte

Ab SAM 3.2 können leere Optionswerte wie KEY, KEY= oder KEY="" erlaubt sein, abhängig von der Implementierung.

### Groß- und Kleinschreibung

Das Protokoll ist, wie spezifiziert, groß- und kleinschreibungsempfindlich. Es wird empfohlen, aber nicht vorgeschrieben, dass der Server Befehle in Großbuchstaben umwandelt, um die Prüfung per Telnet zu vereinfachen. Dadurch wäre beispielsweise "hello version" möglich. Dies ist implementierungsabhängig. Wandeln Sie keine Schlüssel oder Werte in Großbuchstaben um, da dies [I2CP](/docs/protocol/i2cp)-Optionen beschädigen würde.

### SAM-Verbindungs-Handshake

Keine SAM-Kommunikation kann stattfinden, bevor Client und Bridge sich auf eine Protokollversion geeinigt haben. Dies geschieht dadurch, dass der Client ein HELLO sendet und die Bridge ein HELLO REPLY antwortet:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
und

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
Ab Version 3.1 (I2P 0.9.14) sind die Parameter MIN und MAX optional. SAM gibt immer die höchstmögliche Version unter Berücksichtigung der MIN- und MAX-Bedingungen zurück, oder die aktuelle Serverversion, falls keine Bedingungen angegeben sind.

Wenn die SAM-Brücke keine geeignete Version finden kann, antwortet sie mit:

```
<- HELLO REPLY RESULT=NOVERSION
```
Wenn ein Fehler auftritt, beispielsweise ein ungültiges Anfrageformat, antwortet es mit:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

Der Steuer-Socket des Servers kann optional SSL/TLS-Unterstützung bieten, wie auf Server- und Client-Seite konfiguriert. Implementierungen können auch andere Transportschichten anbieten; dies liegt außerhalb des Umfangs der Protokolldefinition.

#### Autorisierung

Für die Autorisierung fügt der Client USER="xxx" PASSWORD="yyy" zu den HELLO-Parametern hinzu. Anführungszeichen um Benutzername und Passwort sind empfohlen, aber nicht zwingend erforderlich. Ein Anführungszeichen innerhalb von Benutzernamen oder Passwort muss mit einem umgekehrten Schrägstrich (Backslash) maskiert werden. Im Fehlerfall antwortet der Server mit I2P_ERROR und einer Nachricht. Es wird empfohlen, SSL auf allen SAM-Servern zu aktivieren, für die eine Autorisierung erforderlich ist.

#### Zeitüberschreitungen

Server können zeitliche Beschränkungen (Timeouts) für den Befehl HELLO oder nachfolgende Befehle implementieren, abhängig von der jeweiligen Implementierung. Clients sollten nach dem Verbindungsaufbau umgehend den Befehl HELLO und den nächsten Befehl senden.

Wenn ein Timeout auftritt, bevor die HELLO-Nachricht empfangen wird, antwortet die Bridge mit:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
und trennt dann die Verbindung.

Wenn ein Timeout auftritt, nachdem das HELLO empfangen wurde, aber bevor der nächste Befehl eingeht, antwortet die Bridge mit:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
und trennt dann die Verbindung.

### I2CP-Ports und -Protokoll

Ab SAM 3.2 können die [I2CP](/docs/protocol/i2cp)-Ports und -Protokolle vom SAM-Client-Sender angegeben werden, um an [I2CP](/docs/protocol/i2cp) weitergeleitet zu werden, und die SAM-Brücke leitet die empfangenen [I2CP](/docs/protocol/i2cp)-Port- und Protokollinformationen an den SAM-Client weiter.

Für FROM_PORT und TO_PORT liegt der gültige Bereich zwischen 0 und 65535, der Standardwert ist 0.

Für PROTOCOL, das nur für RAW angegeben werden darf, liegt der gültige Bereich zwischen 0 und 255, der Standardwert ist 18.

Für SESSION-Befehle sind die angegebenen Ports und Protokolle die Standardwerte für diese Sitzung. Für einzelne Streams oder Datagramme überschreiben die angegebenen Ports und Protokolle die Standards der Sitzung. Für empfangene Streams oder Datagramme entsprechen die angezeigten Ports und Protokolle denjenigen, die über [I2CP](/docs/protocol/i2cp) empfangen wurden.

#### Wichtige Unterschiede zum Standard-IP

I2CP-Ports dienen I2P-Sockets und -Datagrammen. Sie haben keine Beziehung zu Ihren lokalen Sockets, die eine Verbindung zum SAM herstellen.

- Port 0 ist gültig und hat eine besondere Bedeutung.
- Die Ports 1–1023 sind nicht speziell oder privilegiert.
- Server lauschen standardmäßig auf Port 0, was „alle Ports“ bedeutet.
- Clients senden standardmäßig an Port 0, was „beliebiger Port“ bedeutet.
- Clients senden standardmäßig von Port 0, was „nicht angegeben“ bedeutet.
- Server können einen Dienst haben, der auf Port 0 lauscht, sowie weitere Dienste auf höheren Ports. In diesem Fall ist der Dienst auf Port 0 der Standard und wird verwendet, wenn der eingehende Socket- oder Datagramm-Port mit keinem anderen Dienst übereinstimmt.
- Die meisten I2P-Ziele besitzen nur einen laufenden Dienst, daher können Sie die Standardwerte verwenden und die I2CP-Port-Konfiguration ignorieren.
- Für die Angabe von I2CP-Ports ist SAM 3.2 oder 3.3 erforderlich.
- Wenn Sie keine I2CP-Ports benötigen, brauchen Sie auch kein SAM 3.2 oder 3.3; SAM 3.1 ist ausreichend.
- Protokoll 0 ist gültig und bedeutet „beliebiges Protokoll“. Dies wird nicht empfohlen und funktioniert wahrscheinlich nicht.
- I2P-Sockets werden anhand einer internen Verbindungs-ID verfolgt. Daher ist es nicht nötig, dass das 5-Tupel aus Ziel:Port:Ziel:Port:Protokoll eindeutig ist. Beispielsweise kann es mehrere Sockets mit denselben Ports zwischen zwei Zielen geben. Clients müssen also keinen „freien Port“ für eine ausgehende Verbindung wählen.

Wenn Sie eine SAM-3.3-Anwendung mit mehreren Subsitzungen entwerfen, sollten Sie sorgfältig überlegen, wie Ports und Protokolle effektiv verwendet werden. Weitere Informationen finden Sie in der [I2CP](/docs/protocol/i2cp)-Spezifikation.

### SAM-Sitzungen

Eine SAM-Sitzung wird erstellt, wenn ein Client einen Socket zur SAM-Brücke öffnet, einen Handshake durchführt und eine SESSION CREATE-Nachricht sendet. Die Sitzung wird beendet, wenn die Socket-Verbindung getrennt wird.

Jedes registrierte I2P-Ziel ist eindeutig einer Sitzungs-ID (oder einem Spitznamen) zugeordnet. Sitzungs-IDs, einschließlich Subsitzungs-IDs für PRIMARY-Sitzungen, müssen auf dem SAM-Server global eindeutig sein. Um mögliche ID-Kollisionen mit anderen Clients zu vermeiden, empfiehlt es sich, dass der Client IDs zufällig generiert.

Jede Sitzung ist eindeutig verbunden mit:

- der Socket, über den der Client die Sitzung erstellt
- seine ID (oder Spitzname)

#### Anfrage zur Sitzungserstellung

Die Sitzungserstellungs-Nachricht kann nur eine dieser Formen verwenden (Nachrichten, die in anderen Formen empfangen werden, werden mit einer Fehlermeldung beantwortet):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION gibt an, welches Ziel zum Senden und Empfangen von Nachrichten/Streams verwendet werden soll. $privkey ist die Base64-Kodierung der Konkatenation aus [Destination](/docs/specs/common-structures#type_Destination), gefolgt von dem [Private Key](/docs/specs/common-structures#type_PrivateKey), gefolgt von dem [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), optional gefolgt von der [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature). Diese hat binär 663 oder mehr Bytes und in Base64 884 oder mehr Bytes, abhängig vom Signaturtyp. Das binäre Format ist in Private Key File spezifiziert. Siehe zusätzliche Hinweise zum [Private Key](/docs/specs/common-structures#type_PrivateKey) im Abschnitt zur Generierung von Destination-Keys weiter unten.

Wenn der signierende private Schlüssel ausschließlich aus Nullen besteht, folgt der Abschnitt [Offline-Signatur](/docs/specs/common-structures#struct_OfflineSignature). Offline-Signaturen werden nur für STREAM- und RAW-Sitzungen unterstützt. Offline-Signaturen dürfen nicht mit DESTINATION=TRANSIENT erstellt werden. Das Format des Offline-Signaturabschnitts lautet:

1. Zeitstempel für Ablauf (4 Bytes, Big-Endian, Sekunden seit der Epoche, Überlauf im Jahr 2106)
2. Signaturtyp des flüchtigen Signierungs-Öffentlichen-Schlüssels (2 Bytes, Big-Endian)
3. Flüchtiger Signierungs-Öffentlicher-Schlüssel (Länge gemäß flüchtigem Signaturtyp)
4. Signatur der obigen drei Felder durch den Offline-Schlüssel (Länge gemäß Signaturtyp des Ziels)
5. Flüchtiger Signierungs-Privater-Schlüssel (Länge gemäß flüchtigem Signaturtyp)

Wenn das Ziel als TRANSIENT angegeben ist, erstellt die SAM-Brücke ein neues Ziel. Ab Version 3.1 (I2P 0.9.14) wird, falls das Ziel TRANSIENT ist, der optionale Parameter SIGNATURE_TYPE unterstützt. Der SIGNATURE_TYPE-Wert kann jeder unterstützte Name (z. B. ECDSA_SHA256_P256, Groß-/Kleinschreibung wird ignoriert) oder eine Zahl (z. B. 1) sein, wie in [Key Certificates](/docs/specs/common-structures#type_Certificate) beschrieben. Standardmäßig ist dies DSA_SHA1, was in der Regel NICHT gewünscht ist. Für die meisten Anwendungen sollte bitte SIGNATURE_TYPE=7 angegeben werden.

$nickname ist die Wahl des Clients. Leerzeichen sind nicht erlaubt.

Zusätzliche angegebene Optionen werden an die I2P-Sitzungskonfiguration weitergeleitet, sofern sie nicht vom SAM-Bridge interpretiert werden (z. B. outbound.length=0).

Die Java I2P- und i2pd-Router verwenden unterschiedliche Standardwerte für die Anzahl der Tunnel. Der Standardwert bei Java ist 2, bei i2pd ist er 5. Für die meisten Anwendungsfälle mit niedriger bis mittlerer Bandbreite und geringer bis mittlerer Anzahl an Verbindungen sind 2 oder 3 ausreichend. Bitte geben Sie die Tunnelanzahlen in der SESSION CREATE-Nachricht an, um eine konsistente Leistung mit den Java I2P- und i2pd-Routern zu erzielen, z. B. mit den Optionen inbound.quantity=3 outbound.quantity=3. Diese und andere Optionen [sind in den unten stehenden Links dokumentiert](#tunnel-i2cp-and-streaming-options).

Die SAM-Brücke selbst sollte bereits mit dem Router konfiguriert sein, über den sie über I2P kommunizieren soll (obwohl gegebenenfalls eine Überschreibung möglich sein könnte, z. B. i2cp.tcp.host=localhost und i2cp.tcp.port=7654).

#### Antwort auf die Sitzungserstellung

Nachdem die SAM-Brücke die Sitzungserstellungs-Nachricht erhalten hat, wird sie mit einer Sitzungsstatus-Nachricht antworten, wie folgt:

Wenn die Erstellung erfolgreich war:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
Die $privkey ist die Base64-Kodierung der Konkatenation des [Ziels](/docs/specs/common-structures#type_Destination), gefolgt vom [privaten Schlüssel](/docs/specs/common-structures#type_PrivateKey), gefolgt vom [Signatur-privaten Schlüssel](/docs/specs/common-structures#type_SigningPrivateKey), optional gefolgt von der [Offline-Signatur](/docs/specs/common-structures#struct_OfflineSignature), was binär 663 oder mehr Bytes und in Base64 884 oder mehr Bytes umfasst, abhängig vom Signaturtyp. Das Binärformat ist in der Spezifikation für Private Key Files festgelegt.

Wenn die SESSION CREATE eine signierende privaten Schlüssel aus lauter Nullen und einen [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature)-Abschnitt enthielt, wird die SESSION STATUS-Antwort dieselben Daten im selben Format enthalten. Weitere Einzelheiten finden Sie im Abschnitt SESSION CREATE oben.

Wenn der Spitzname bereits mit einer Sitzung verknüpft ist:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Wenn das Ziel bereits verwendet wird:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Wenn das Ziel kein gültiger privater Ziel-Schlüssel ist:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Wenn ein anderer Fehler aufgetreten ist:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Wenn es nicht in Ordnung ist, sollte die MESSAGE menschenlesbare Informationen enthalten, warum die Sitzung nicht erstellt werden konnte.

Beachten Sie, dass der Router Tunnel aufbaut, bevor er mit SESSION STATUS antwortet. Dies kann mehrere Sekunden oder, beim Routerstart oder bei starker Netzwerkbelastung, eine Minute oder länger dauern. Falls der Aufbau fehlschlägt, wird der Router erst nach mehreren Minuten mit einer Fehlermeldung antworten. Legen Sie keinen kurzen Timeout für die Wartezeit auf die Antwort fest. Brechen Sie die Sitzung nicht ab, während der Tunnelaufbau noch läuft, und versuchen Sie es nicht erneut.

SAM-Sitzungen leben und sterben mit dem Socket, mit dem sie verbunden sind. Wenn der Socket geschlossen wird, endet die Sitzung und alle Kommunikationen über diese Sitzung werden gleichzeitig beendet. Umgekehrt schließt die SAM-Brücke den Socket, wenn die Sitzung aus irgendeinem Grund endet.

### SAM Virtuelle Streams

Virtuelle Streams werden zuverlässig und in der richtigen Reihenfolge übertragen, wobei Fehler- und Erfolgsmeldungen sobald wie möglich weitergeleitet werden.

Streams sind bidirektionale Kommunikationssockets zwischen zwei I2P-Zielen, wobei deren Öffnung von einer der beiden Seiten angefordert werden muss. Danach verwendet der SAM-Client CONNECT-Befehle für eine solche Anfrage. FORWARD-/ACCEPT-Befehle werden vom SAM-Client verwendet, wenn er Anfragen von anderen I2P-Zielen empfangen möchte.

### SAM-Virtual-Streams: VERBINDEN

Ein Client fordert eine Verbindung an durch:

- Öffnen eines neuen Sockets über die SAM-Brücke
- Übergeben des gleichen HELLO-Handshakes wie oben
- Senden des STREAM CONNECT-Befehls

#### Verbindungsanfrage

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Dieser Befehl stellt eine neue virtuelle Verbindung von der lokalen Sitzung, deren ID $nickname ist, zu dem angegebenen Peer her.

Das Ziel ist $destination, also die Base64-Darstellung des [Ziels (Destination)](/docs/specs/common-structures#type_Destination), bestehend aus 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat), abhängig vom Signaturtyp.

**HINWEIS:** Seit etwa 2014 (SAM v3.1) unterstützt Java I2P auch Hostnamen und b32-Adressen für das $destination-Feld, was jedoch zuvor nicht dokumentiert war. Seit der Version 0.9.48 werden Hostnamen und b32-Adressen offiziell von Java I2P unterstützt. Der i2pd-Router unterstützt Hostnamen und b32-Adressen ab Version 2.38.0 (0.9.50). Bei beiden Routern umfasst die „b32“-Unterstützung auch die erweiterten „b33“-Adressen für verblindete Zieladressen.

#### Verbindungsantwort

Wenn SILENT=true übergeben wird, sendet die SAM-Brücke keine weiteren Nachrichten über den Socket. Wenn die Verbindung fehlschlägt, wird der Socket geschlossen. Wenn die Verbindung erfolgreich ist, wird alle verbleibende über den aktuellen Socket übertragene Daten an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen.

Wenn SILENT=false ist, was der Standardwert ist, sendet die SAM-Brücke eine letzte Nachricht an ihren Client, bevor sie den Socket weiterleitet oder herunterfährt:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Wenn das ERGEBNIS OK ist, wird alle verbleibende Datenübertragung über den aktuellen Socket an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen. Falls die Verbindung nicht hergestellt werden konnte (Timeout, etc.), enthält ERGEBNIS den entsprechenden Fehlerwert (gegebenenfalls mit einer optionalen menschenlesbaren NACHRICHT), und die SAM-Brücke schließt den Socket.

Das interne Timeout für die Router-Stream-Verbindung beträgt ungefähr eine Minute und ist implementierungsabhängig. Legen Sie kein kürzeres Timeout für das Warten auf die Antwort fest.

### SAM Virtuelle Streams: AKZEPTIEREN

Ein Client wartet auf eine eingehende Verbindungsanfrage durch:

- Öffnen eines neuen Sockets über die SAM-Brücke
- Übergeben desselben HELLO-Handshakes wie oben
- Senden des STREAM ACCEPT-Befehls

#### Anfrage annehmen

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Dies bewirkt, dass die Sitzung ${nickname} auf eine eingehende Verbindungsanfrage aus dem I2P-Netzwerk lauscht. ACCEPT ist nicht erlaubt, solange eine aktive FORWARD-Verbindung in der Sitzung besteht.

Ab SAM 3.2 sind mehrere gleichzeitige ausstehende STREAM ACCEPTs mit derselben Sitzungs-ID erlaubt (sogar mit demselben Port). Vor Version 3.2 scheiterten gleichzeitige Akzeptvorgänge mit ALREADY_ACCEPTING. Hinweis: Java I2P unterstützt gleichzeitige ACCEPTs ebenfalls ab Version 3.1, ab Release 0.9.24 (2016-01). i2pd unterstützt gleichzeitige ACCEPTs ebenfalls ab SAM 3.1, ab Release 2.50.0 (2023-12).

#### Akzeptiere Antwort

Wenn SILENT=true übergeben wird, sendet die SAM-Brücke keine weiteren Nachrichten über den Socket. Falls das Accept fehlschlägt, wird der Socket geschlossen. Wenn das Accept erfolgreich ist, wird alle verbleibende Datenübertragung durch den aktuellen Socket an den verbundenen I2P-Zielpeer weitergeleitet und umgekehrt. Aus Gründen der Zuverlässigkeit und um das Ziel eingehender Verbindungen zu erhalten, wird SILENT=false empfohlen.

Wenn SILENT=false ist, was der Standardwert ist, antwortet die SAM-Brücke mit:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

```
OK
I2P_ERROR
INVALID_ID
```
Wenn das Ergebnis nicht OK ist, wird der Socket sofort durch die SAM-Brücke geschlossen. Wenn das Ergebnis OK ist, beginnt die SAM-Brücke, auf eine eingehende Verbindungsanfrage von einem anderen I2P-Peer zu warten. Wenn eine Anfrage eintrifft, akzeptiert die SAM-Brücke diese und:

Wenn SILENT=true übergeben wurde, sendet die SAM-Brücke keine weiteren Nachrichten über den Client-Socket. Alle verbleibenden Daten, die durch den aktuellen Socket übertragen werden, werden an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen.

Wenn SILENT=false übergeben wurde, was der Standardwert ist, sendet die SAM-Brücke dem Client eine ASCII-Zeile, die den base64-kodierten öffentlichen Ziel-Schlüssel des anfragenden Peers sowie zusätzliche Informationen (nur für SAM 3.2) enthält:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Nach dieser durch „\n“ abgeschlossenen Zeile wird alle verbleibende über den aktuellen Socket übertragene Daten an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen, bis einer der Peers den Socket schließt.

#### Fehler nach OK

In seltenen Fällen kann die SAM-Brücke einen Fehler erleben, nachdem sie RESULT=OK gesendet hat, aber bevor eine Verbindung eingeht und die $destination-Zeile an den Client gesendet wird. Solche Fehler können das Herunterfahren des Routers, einen Neustart des Routers oder das Schließen der Sitzung umfassen. In diesen Fällen kann die SAM-Brücke, wenn SILENT=false ist, abhängig von der Implementierung (implementierungsabhängig), die folgende Zeile senden:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
bevor der Socket sofort geschlossen wird. Diese Zeile ist natürlich nicht als gültiges Base-64-Ziel decodierbar.

### SAM Virtuelle Streams: WEITERLEITEN

Ein Client kann einen regulären Socket-Server verwenden und auf Verbindungsanfragen aus I2P warten. Dazu muss der Client Folgendes tun:

- öffne einen neuen Socket mit der SAM-Brücke
- sende den gleichen HELLO-Handshake wie oben
- sende den Weiterleitungs-Befehl

#### Weiterleitungsanfrage

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Dies bewirkt, dass die Sitzung ${nickname} auf eingehende Verbindungsanfragen aus dem I2P-Netzwerk lauscht. FORWARD ist nicht erlaubt, solange ein ACCEPT auf der Sitzung aussteht.

#### Weiterleitungsantwort

SILENT hat standardmäßig den Wert false. Unabhängig davon, ob SILENT wahr oder falsch ist, antwortet die SAM-Brücke immer mit einer STREAM STATUS-Nachricht. Beachten Sie, dass dies ein anderes Verhalten im Vergleich zu STREAM ACCEPT und STREAM CONNECT ist, wenn SILENT=true. Die STREAM STATUS-Nachricht lautet:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

```
OK
I2P_ERROR
INVALID_ID
```
$host ist der Hostname oder die IP-Adresse des Socket-Servers, an den SAM Verbindungsanfragen weiterleitet. Falls nicht angegeben, verwendet SAM die IP-Adresse des Sockets, der den Forward-Befehl gesendet hat.

$port ist die Portnummer des Socket-Servers, an den SAM Verbindungsanfragen weiterleitet. Dies ist zwingend erforderlich.

Wenn eine Verbindungsanfrage von I2P eintrifft, öffnet die SAM-Brücke eine Socket-Verbindung zu $host:$port. Wenn diese innerhalb von weniger als 3 Sekunden akzeptiert wird, akzeptiert SAM die Verbindung von I2P und führt anschließend Folgendes aus:

Wenn SILENT=true übergeben wurde, wird alle über den erhaltenen aktuellen Socket übertragenen Daten an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen.

Wenn SILENT=false übergeben wurde, was der Standardwert ist, sendet die SAM-Brücke über den erhaltenen Socket eine ASCII-Zeile, die den base64-kodierten öffentlichen Ziel-Schlüssel des anfragenden Peers enthält, sowie zusätzliche Informationen, die nur für SAM 3.2 gelten:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Nach dieser durch '\n' abgeschlossenen Zeile werden alle weiteren über den Socket übertragenen Daten an den verbundenen I2P-Zielpeer weitergeleitet und von dort empfangen, bis eine der beiden Seiten den Socket schließt.

Ab SAM 3.2 erfolgt das Weiterleiten des Sockets über SSL/TLS, wenn SSL=true angegeben ist.

Der I2P-Router wird aufhören, eingehende Verbindungsanfragen zu empfangen, sobald der "forwarding"-Socket geschlossen wird.

### SAM-Datagramme

SAMv3 bietet Mechanismen zum Senden und Empfangen von Datagrammen über lokale Datagrammsockets. Einige SAMv3-Implementierungen unterstützen außerdem die ältere Methode der Version v1/v2 zum Senden/Empfangen von Datagrammen über den SAM-Bridge-Socket. Beide Methoden werden unten dokumentiert.

I2P unterstützt vier Arten von Datagrammen:

- Wiederverwendbare und authentifizierte Datagramme enthalten als Präfix das Ziel des Absenders und die Signatur des Absenders, sodass der Empfänger überprüfen kann, ob das Ziel des Absenders gefälscht wurde, und dass er auf das Datagramm antworten kann. Das neue Datagram2-Format ist ebenfalls wiederverwendbar und authentifiziert.
- Das neue Datagram3-Format ist wiederverwendbar, aber nicht authentifiziert. Die Absenderinformationen sind nicht verifiziert.
- Roh-Datagramme enthalten weder das Ziel des Absenders noch eine Signatur.

Standardmäßige I2CP-Ports sind sowohl für repliable als auch für raw Datagramme definiert. Der I2CP-Port kann für raw Datagramme geändert werden.

Ein gängiges Protokolldesign-Muster sieht vor, dass wiederholbare Datagramme an Server gesendet werden, wobei eine Kennung enthalten ist, und der Server antwortet mit einem einfachen Datagramm, das diese Kennung enthält, sodass die Antwort der Anfrage zugeordnet werden kann. Dieses Designmuster eliminiert den erheblichen Overhead wiederholbarer Datagramme in Antworten. Alle Entscheidungen bezüglich I2CP-Protokollen und -Ports sind anwendungsspezifisch, und Entwickler sollten diese Aspekte berücksichtigen.

Siehe auch die wichtigen Hinweise zur Datagramm-MTU im folgenden Abschnitt.

#### Senden von replikierbaren oder rohen Datagrammen

Obwohl I2P an sich keine FROM-Adresse enthält, wird der Benutzerfreundlichkeit halber eine zusätzliche Ebene in Form von antwortfähigen Datagrammen bereitgestellt – ungeordnete und unzuverlässige Nachrichten mit einer Größe von bis zu 31744 Bytes, die eine FROM-Adresse enthalten (wobei bis zu 1 KB für Header-Informationen verbleiben). Diese FROM-Adresse wird intern durch SAM authentifiziert (unter Verwendung des Signierschlüssels des Ziels zur Überprüfung der Quelle) und beinhaltet Schutz vor Wiedereinspielung (Replay Prevention).

Die Mindestgröße beträgt 1. Für eine optimale Zuverlässigkeit bei der Zustellung wird eine maximale Größe von etwa 11 KB empfohlen. Die Zuverlässigkeit nimmt mit zunehmender Nachrichtengröße ab, möglicherweise sogar exponentiell.

Nach dem Aufbau einer SAM-Sitzung mit STYLE=DATAGRAM oder STYLE=RAW kann der Client repliable oder raw Datagramme über den UDP-Port von SAM (standardmäßig 7655) senden.

Die erste Zeile eines Datagramms, das über diesen Port gesendet wird, muss das folgende Format aufweisen. Dies steht alles in einer Zeile (durch Leerzeichen getrennt), hier zur besseren Übersichtlichkeit in mehreren Zeilen dargestellt:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 ist die Version von SAM. Ab SAM 3.2 ist jede 3.x-Version erlaubt.
- $nickname ist die ID der DATAGRAM-Sitzung, die verwendet wird
- Das Ziel ist $destination, also die Base64-Codierung des [Zielorts](/docs/specs/common-structures#type_Destination), was 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat) entspricht, abhängig vom Signaturtyp. **HINWEIS:** Seit etwa 2014 (SAM v3.1) unterstützt Java I2P zusätzlich Hostnamen und b32-Adressen für $destination, was jedoch zuvor nicht dokumentiert war. Seit der Version 0.9.48 werden Hostnamen und b32-Adressen von Java I2P offiziell unterstützt. Der i2pd-Router unterstützt derzeit weder Hostnamen noch b32-Adressen; Unterstützung könnte in einer zukünftigen Version hinzugefügt werden.
- Alle Optionen sind pro-Datagramm-Einstellungen, die die in SESSION CREATE angegebenen Standardwerte überschreiben.
- Die Optionen der Version 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES und SEND_LEASESET werden an [I2CP](/docs/protocol/i2cp) weitergeleitet, sofern unterstützt. Details finden Sie in der [I2CP-Spezifikation](/docs/protocol/i2cp#msg_SendMessageExpire). Die Unterstützung durch den SAM-Server ist optional; diese Optionen werden bei Nichtunterstützung ignoriert.
- Diese Zeile ist mit '\\n' abgeschlossen.

Die erste Zeile wird von SAM verworfen, bevor die verbleibenden Daten der Nachricht an das angegebene Ziel gesendet werden.

Für eine alternative Methode zum Senden von antwortfähigen und rohen Datagrammen siehe [DATAGRAM SEND und RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### SAM-Replikierbare Datagramme: Empfang eines Datagramms

Eingehende Datagramme werden von SAM auf den Socket geschrieben, über den die Datagrammsitzung geöffnet wurde, sofern kein weiterleitender PORT im SESSION CREATE-Befehl angegeben ist. Dies ist die mit v1/v2 kompatible Methode, um Datagramme zu empfangen.

Wenn ein Datagramm ankommt, leitet die Bridge es über die Nachricht an den Client weiter:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
Die Quelle ist $destination, also die Base64-Darstellung des [Ziels](/docs/specs/common-structures#type_Destination), bestehend aus 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat), abhängig vom Signaturtyp.

Die SAM-Brücke gibt gegenüber dem Client niemals Authentifizierungsheader oder andere Felder preis, sondern lediglich die Daten, die der Absender bereitgestellt hat. Dies setzt sich fort, bis die Sitzung geschlossen wird (indem der Client die Verbindung trennt).

#### Weiterleitung von Roh- oder beantwortbaren Datagrammen

Beim Erstellen einer Datagramm-Sitzung kann der Client SAM auffordern, eingehende Nachrichten an eine angegebene IP:Port-Adresse weiterzuleiten. Dazu sendet er den CREATE-Befehl mit den Optionen PORT und HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
Die $privkey ist die Base64-Kodierung der Konkatenation des [Ziels](/docs/specs/common-structures#type_Destination), gefolgt vom [Privaten Schlüssel](/docs/specs/common-structures#type_PrivateKey), gefolgt vom [Signier-Privatschlüssel](/docs/specs/common-structures#type_SigningPrivateKey), optional gefolgt von der [Offline-Signatur](/docs/specs/common-structures#struct_OfflineSignature), was 884 oder mehr Base64-Zeichen (663 oder mehr Bytes im Binärformat) ergibt, abhängig vom Signaturtyp. Das Binärformat ist in der Spezifikation für Private Key Files festgelegt.

Offline-Signaturen werden für RAW-, DATAGRAM2- und DATAGRAM3-Datagramme unterstützt, jedoch nicht für DATAGRAM. Weitere Informationen finden Sie im Abschnitt SESSION CREATE oben und im Abschnitt DATAGRAM2/3 unten.

$host ist der Hostname oder die IP-Adresse des Datagramm-Servers, an den SAM Datagramme weiterleitet. Falls nicht angegeben, verwendet SAM die IP-Adresse des Sockets, der den Forward-Befehl gesendet hat.

$port ist die Portnummer des Datagrammservers, an den SAM Datagramme weiterleitet. Wenn $port nicht gesetzt ist, werden Datagramme NICHT weitergeleitet, sondern über den Steuer-Socket im v1/v2-kompatiblen Format empfangen.

Zusätzliche angegebene Optionen werden an die I2P-Sitzungskonfiguration weitergeleitet, sofern sie nicht vom SAM-Bridge interpretiert werden (z. B. outbound.length=0). Diese Optionen sind [unten dokumentiert](#tunnel-i2cp-and-streaming-options).

Weitergeleitete antwortfähige Datagramme werden immer mit dem base64-kodierten Ziel präfixiert, außer bei Datagram3, siehe unten. Wenn ein antwortfähiges Datagramm ankommt, sendet die Bridge an den angegebenen Host:Port ein UDP-Paket mit folgenden Daten:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Weitergeleitete rohe Datagramme werden ohne Präfix unverändert an den angegebenen Host:Port weitergeleitet. Das UDP-Paket enthält folgende Daten:

```
$datagram_payload
```
Ab SAM 3.2 wird, wenn HEADER=true in SESSION CREATE angegeben ist, dem weitergeleiteten rohen Datagramm eine Header-Zeile wie folgt vorangestellt:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Das $destination ist die Base64-Darstellung des [Ziels](/docs/specs/common-structures#type_Destination), das 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat) umfasst, abhängig vom Signaturtyp.

#### SAM Anonyme (Rohe) Datagramme

Indem die Bandbreite von I2P maximal ausgenutzt wird, ermöglicht SAM Clients das Senden und Empfangen anonymer Datagramme, wobei Authentifizierung und Antwortinformationen allein beim Client liegen. Diese Datagramme sind unzuverlässig und ungeordnet und können bis zu 32768 Bytes groß sein.

Die Mindestgröße beträgt 1. Für eine optimale Zuverlässigkeit bei der Zustellung wird eine maximale Größe von etwa 11 KB empfohlen.

Nachdem eine SAM-Sitzung mit STYLE=RAW eingerichtet wurde, kann der Client anonyme Datagramme über die SAM-Brücke senden, genau wie beim [Senden antwortfähiger Datagramme](#sending-repliable-or-raw-datagrams).

Beide Arten des Empfangs von Datagrammen sind auch für anonyme Datagramme verfügbar.

Eingehende Datagramme werden von SAM auf den Socket geschrieben, über den die Datagrammsitzung geöffnet wurde, sofern kein weiterleitender PORT im SESSION CREATE-Befehl angegeben ist. Dies ist die mit v1/v2 kompatible Methode, um Datagramme zu empfangen.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Wenn anonyme Datagramme an einen bestimmten Host:Port weitergeleitet werden sollen, sendet die Bridge an den angegebenen Host:Port eine Nachricht mit folgenden Daten:

```
$datagram_payload
```
Ab SAM 3.2 wird, wenn HEADER=true in SESSION CREATE angegeben ist, dem weitergeleiteten rohen Datagramm eine Header-Zeile wie folgt vorangestellt:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Für eine alternative Methode zum Senden anonymer Datagramme siehe [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Datagramm 2/3

Datagramm 2/3 sind neue Formate, die Anfang 2025 spezifiziert wurden. Derzeit existieren keine bekannten Implementierungen. Überprüfen Sie die Implementierungsdokumentation auf den aktuellen Status. Weitere Informationen finden Sie in der [Spezifikation](/docs/specs/datagrams).

Derzeit gibt es keine Pläne, die SAM-Version zu erhöhen, um die Unterstützung für Datagram 2/3 anzuzeigen. Dies könnte problematisch sein, da Implementierungen möglicherweise Datagram 2/3 unterstützen möchten, aber nicht die SAM v3.3-Features. Jede Versionsänderung steht noch aus (TBD).

Sowohl Datagram2 als auch Datagram3 sind replizierbar. Nur Datagram2 ist authentifiziert.

Datagram2 ist aus SAM-Sicht identisch mit replikierbaren Datagrammen. Beide sind authentifiziert. Lediglich das I2CP-Format und die Signatur unterscheiden sich, was für SAM-Clients jedoch nicht sichtbar ist. Datagram2 unterstützt außerdem Offline-Signaturen und kann daher von offline-signierten Zieladressen verwendet werden.

Der Zweck von Datagram2 besteht darin, replikierbare Datagramme für neue Anwendungen zu ersetzen, die keine Abwärtskompatibilität erfordern. Datagram2 bietet Schutz vor Wiedergabeangriffen, der bei replikierbaren Datagrammen nicht vorhanden ist. Falls Abwärtskompatibilität erforderlich ist, kann eine Anwendung sowohl Datagram2 als auch replikierbare Datagramme in derselben Sitzung unterstützen, sofern SAM 3.3 PRIMARY-Sitzungen verwendet werden.

Datagram3 ist replizierbar, aber nicht authentifiziert. Das Feld 'from' im I2CP-Format ist ein Hash, keine Zieladresse. Die $destination, die vom SAM-Server an den Client gesendet wird, ist ein 44 Zeichen langer base64-Hash. Um sie in eine vollständige Zieladresse für eine Antwort umzuwandeln, decodieren Sie sie zunächst von base64 in 32 Byte binär, dann codieren Sie sie als base32 in 52 Zeichen und hängen Sie ".b32.i2p" an, um eine NAMING LOOKUP durchzuführen. Wie üblich sollten Clients ihren eigenen Cache verwalten, um wiederholte NAMING LOOKUPs zu vermeiden.

Anwendungsentwickler sollten äußerste Vorsicht walten lassen und die Sicherheitsimplikationen von nicht authentifizierten Datagrammen berücksichtigen.

#### Überlegungen zur V3-Datagramm-MTU

I2P-Datagramme können größer sein als die typische Internet-MTU von 1500 Byte. Lokal gesendete Datagramme und weitergeleitete repliable Datagramme, die mit dem 516+ Byte langen base64-kodierten Ziel beginnen, überschreiten diese MTU wahrscheinlich. Allerdings sind die MTUs für localhost unter Linux-Systemen typischerweise viel größer, zum Beispiel 65536. Die localhost-MTU variiert je nach Betriebssystem. I2P-Datagramme werden niemals größer als 65536 sein. Die Größe der Datagramme hängt vom Anwendungsprotokoll ab.

Wenn der SAM-Client lokal zum SAM-Server ist und das System einen größeren MTU-Wert unterstützt, werden die Datagramme lokal nicht fragmentiert. Wenn jedoch der SAM-Client entfernt ist, würden IPv4-Datagramme fragmentiert und IPv6-Datagramme würden fehlschlagen (IPv6 unterstützt keine UDP-Fragmentierung).

Entwickler von Client-Bibliotheken und Anwendungen sollten diese Probleme kennen und Empfehlungen dokumentieren, um Fragmentierung und Paketverlust zu vermeiden, insbesondere bei entfernten SAM-Client-Server-Verbindungen.

#### DATAGRAMM SENDEN, ROH SENDEN (V1/V2-kompatible Datagrammverarbeitung)

In SAM V3 ist der bevorzugte Weg, Datagramme zu senden, der über den Datagramm-Socket an Port 7655, wie oben dokumentiert. Allerdings können repliable Datagramme direkt über den SAM-Brückensocket mithilfe des Befehls DATAGRAM SEND gesendet werden, wie in [SAM V1](/docs/api/sam) und [SAM V2](/docs/api/samv2) beschrieben.

Ab Version 0.9.14 (Version 3.1) können anonyme Datagramme direkt über den SAM-Brückensocket mit dem Befehl RAW SEND gesendet werden, wie in [SAM V1](/docs/api/sam) und [SAM V2](/docs/api/samv2) dokumentiert.

Ab Version 0.9.24 (Version 3.2) können DATAGRAM SEND und RAW SEND die Parameter FROM_PORT=nnnn und/oder TO_PORT=nnnn enthalten, um die Standardports zu überschreiben. Ab Version 0.9.24 (Version 3.2) kann RAW SEND den Parameter PROTOCOL=nnn enthalten, um das Standardprotokoll zu überschreiben.

Diese Befehle unterstützen *nicht* den ID-Parameter. Die Datagramme werden entsprechend an die zuletzt erstellte DATAGRAM- oder RAW-artige Sitzung gesendet. Die Unterstützung für den ID-Parameter könnte in einer zukünftigen Version hinzugefügt werden.

Die Formate DATAGRAM2 und DATAGRAM3 werden *nicht* auf eine V1/V2-kompatible Weise unterstützt.

### SAM PRIMARY-Sitzungen (V3.3 und höher)

*Version 3.3 wurde in I2P-Version 0.9.25 eingeführt.*

*In einer früheren Version dieser Spezifikation waren PRIMARY-Sitzungen als MASTER-Sitzungen bekannt. Sowohl in `i2pd` als auch in `I2P+` werden sie weiterhin ausschließlich als MASTER-Sitzungen bezeichnet.*

SAM v3.3 fügt Unterstützung für das gleichzeitige Ausführen von Streaming-, Datagramm- und Raw-Subsessions innerhalb derselben primären Session hinzu, sowie für die Nutzung mehrerer Subsessions desselben Typs. Der gesamte Datenverkehr der Subsessions nutzt ein einzelnes Ziel oder einen Satz von Tunnels. Die Weiterleitung des Datenverkehrs über I2P basiert auf den Port- und Protokolloptionen der Subsessions.

Um multiplexierte Subsitzungen zu erstellen, müssen Sie zunächst eine primäre Sitzung erstellen und anschließend Subsitzungen zur primären Sitzung hinzufügen. Jede Subsitzung muss eine eindeutige ID sowie ein eindeutiges Protokoll und eine eindeutige Portnummer für die Abhörung haben. Subsitzungen können auch wieder aus der primären Sitzung entfernt werden.

Mit einer PRIMARY-Sitzung und einer Kombination aus Subsitzungen kann ein SAM-Client mehrere Anwendungen oder eine einzelne anspruchsvolle Anwendung, die verschiedene Protokolle nutzt, über einen einzigen Satz von Tunneln unterstützen. Beispielsweise könnte ein BitTorrent-Client eine Streaming-Subsitzung für Peer-to-Peer-Verbindungen sowie Datagramm- und Raw-Subsitzungen für DHT-Kommunikation einrichten.

#### Erstellen einer PRIMÄREN Sitzung

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Die SAM-Brücke antwortet mit Erfolg oder Fehler, wie in [der Antwort auf eine Standard-SESSION CREATE](#session-creation-response).

Stellen Sie die Optionen PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL oder HEADER nicht für eine primäre Sitzung ein. Sie dürfen keine Daten über eine PRIMARY-Sitzungs-ID oder über den Steckplatz (control socket) senden. Alle Befehle wie STREAM CONNECT, DATAGRAM SEND usw. müssen die Subsitzungs-ID auf einem separaten Socket verwenden.

Die PRIMÄRE Sitzung stellt eine Verbindung zum Router her und baut Tunnel auf. Wenn die SAM-Brücke antwortet, wurden die Tunnel erstellt und die Sitzung ist bereit, um Untersitzungen hinzuzufügen. Alle [I2CP](/docs/protocol/i2cp)-Optionen, die Tunnelparameter wie Länge, Anzahl und Spitznamen betreffen, müssen bei der SESSION CREATE der primären Sitzung angegeben werden.

Alle Hilfsbefehle werden in einer primären Sitzung unterstützt.

Wenn die primäre Sitzung geschlossen wird, werden auch alle Subsitzungen geschlossen.

HINWEIS: Vor der Version 0.9.47 verwenden Sie STYLE=MASTER. STYLE=PRIMARY wird ab Version 0.9.47 unterstützt. MASTER wird aus Gründen der Abwärtskompatibilität weiterhin unterstützt.

#### Erstellen einer Subsession

Über den gleichen Steckplatz (Socket), auf dem die PRIMÄRE Sitzung erstellt wurde:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Die SAM-Brücke antwortet mit Erfolg oder Fehler, wie in [der Antwort auf eine Standard-SESSION CREATE](#session-creation-response). Da die Tunnel bereits bei der primären SESSION CREATE erstellt wurden, sollte die SAM-Brücke sofort antworten.

Stellen Sie die OPTION DESTINATION nicht bei einem SESSION ADD ein. Die Subsitzung wird das in der Hauptsitzung angegebene Ziel verwenden. Alle Subsitzungen müssen über den Steckplatz hinzugefügt werden, d. h. die gleiche Verbindung, auf der Sie die Hauptsitzung erstellt haben.

Mehrere Subsitzungen müssen ausreichend eindeutige Optionen aufweisen, damit eingehende Daten korrekt weitergeleitet werden können. Insbesondere müssen mehrere Sitzungen desselben Typs unterschiedliche LISTEN_PORT-Optionen (und/oder LISTEN_PROTOCOL, nur bei RAW) haben. Ein SESSION ADD mit einem Listen-Port und -Protokoll, das eine bestehende Subsitzung dupliziert, führt zu einem Fehler.

Der LISTEN_PORT ist der lokale I2P-Port, also der Empfangs- (TO-)Port für eingehende Daten. Wenn der LISTEN_PORT nicht angegeben ist, wird der FROM_PORT-Wert verwendet. Wenn weder LISTEN_PORT noch FROM_PORT angegeben sind, erfolgt die Weiterleitung eingehenden Datenverkehrs allein basierend auf STYLE und PROTOCOL. Für LISTEN_PORT und LISTEN_PROTOCOL bedeutet der Wert 0 „beliebig“, also ein Platzhalter (Wildcard). Wenn sowohl LISTEN_PORT als auch LISTEN_PROTOCOL den Wert 0 haben, wird diese Subsession die Standard-Subsession für eingehenden Datenverkehr sein, der nicht an eine andere Subsession weitergeleitet wird. Eingehender Streaming-Verkehr (Protokoll 6) wird niemals an eine RAW-Subsession weitergeleitet, selbst wenn deren LISTEN_PROTOCOL auf 0 steht. Eine RAW-Subsession darf kein LISTEN_PROTOCOL von 6 festlegen. Wenn keine Standard-Subsession oder passende Subsession für das Protokoll und den Port des eingehenden Datenverkehrs existiert, werden diese Daten verworfen.

Verwenden Sie die Subsession-ID, nicht die primäre Sitzungs-ID, zum Senden und Empfangen von Daten. Alle Befehle wie STREAM CONNECT, DATAGRAM SEND usw. müssen die Subsession-ID verwenden.

Alle Hilfsbefehle werden in einer primären Sitzung oder Subsitzung unterstützt. Das Senden/Empfangen von v1/v2-Datagrammen/rohen Daten wird in einer primären Sitzung oder in Subsitzungen nicht unterstützt.

#### Beenden einer Subsession

Über den gleichen Steckplatz (Socket), auf dem die PRIMÄRE Sitzung erstellt wurde:

```
->  SESSION REMOVE
          ID=$nickname
```
Dies entfernt eine Subsession aus der primären Sitzung. Legen Sie keine weiteren Optionen bei einem SESSION REMOVE fest. Subsessions müssen über den Steckverbinder (Control Socket) entfernt werden, also über dieselbe Verbindung, über die Sie die primäre Sitzung erstellt haben. Nachdem eine Subsession entfernt wurde, wird sie geschlossen und kann nicht mehr zum Senden oder Empfangen von Daten verwendet werden.

Die SAM-Brücke antwortet mit Erfolg oder Fehler, wie in [der Antwort auf eine Standard-SESSION CREATE](#session-creation-response).

### SAM-Dienstbefehle

Einige Hilfsbefehle erfordern eine vorhandene Sitzung, andere nicht. Siehe Details unten.

#### Nachschlagen des Hostnamens

Die folgende Nachricht kann vom Client verwendet werden, um die SAM-Brücke nach der Namensauflösung zu fragen:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
das beantwortet wird durch

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
Der RESULT-Wert kann einer der folgenden sein:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Wenn NAME=ME ist, enthält die Antwort das vom aktuellen Session verwendete Ziel (nützlich, wenn Sie ein TRANSIENTes verwenden). Wenn $result nicht OK ist, kann MESSAGE eine beschreibende Nachricht enthalten, wie etwa „bad format“ usw. INVALID_KEY bedeutet, dass mit $name in der Anfrage etwas nicht stimmt, möglicherweise ungültige Zeichen.

Das $destination ist die Base64-Darstellung des [Ziels](/docs/specs/common-structures#type_Destination), das 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat) umfasst, abhängig vom Signaturtyp.

NAMING LOOKUP erfordert nicht, dass zuerst eine Sitzung erstellt wurde. In einigen Implementierungen kann jedoch eine .b32.i2p-Suche, die nicht zwischengespeichert ist und eine Netzwerkanfrage erfordert, fehlschlagen, da keine Client-Tunnel für die Suche verfügbar sind.

#### Optionen für die Namensauflösung

NAMING LOOKUP wurde ab Router-API 0.9.66 erweitert, um Service-Suchen zu unterstützen. Die Unterstützung kann je nach Implementierung variieren. Weitere Informationen finden Sie in Vorschlag 167.

NAMING LOOKUP NAME=example.i2p OPTIONS=true fordert die Optionszuordnung in der Antwort an. NAME kann eine vollständige base64-Destination sein, wenn OPTIONS=true.

Wenn die Ziel-Suche erfolgreich war und Optionen in dem LeaseSet vorhanden waren, folgen in der Antwort nach dem Ziel eine oder mehrere Optionen in der Form OPTION:Schlüssel=Wert. Jede Option hat ein eigenes OPTION:-Präfix. Alle Optionen aus dem LeaseSet werden einbezogen, nicht nur die Dienst-Record-Optionen. Beispielsweise können Optionen für in Zukunft definierte Parameter vorhanden sein. Beispiel:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Schlüssel, die '=' enthalten, sowie Schlüssel oder Werte, die einen Zeilenumbruch enthalten, gelten als ungültig, und das Schlüssel-Wert-Paar wird aus der Antwort entfernt. Wenn keine Optionen im LeaseSet gefunden werden oder wenn das LeaseSet Version 1 war, enthält die Antwort keine Optionen. Falls OPTIONS=true in der Anfrage enthalten war und das LeaseSet nicht gefunden wurde, wird ein neuer Ergebniswert LEASESET_NOT_FOUND zurückgegeben.

#### Generierung des Ziel-Schlüssels

Öffentliche und private Base64-Schlüssel können mithilfe der folgenden Nachricht generiert werden:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
das beantwortet wird durch

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Ab Version 3.1 (I2P 0.9.14) wird ein optionaler Parameter SIGNATURE_TYPE unterstützt. Der Wert von SIGNATURE_TYPE kann beliebiger unterstützter Name (z. B. ECDSA_SHA256_P256, Groß-/Kleinschreibung wird ignoriert) oder eine Zahl (z. B. 1) sein, wie er in [Key Certificates](/docs/specs/common-structures#type_Certificate) definiert ist. Der Standardwert ist DSA_SHA1, was in der Regel NICHT gewünscht ist. Für die meisten Anwendungen sollte bitte SIGNATURE_TYPE=7 angegeben werden.

Das $destination ist die Base64-Darstellung des [Ziels](/docs/specs/common-structures#type_Destination), das 516 oder mehr Base64-Zeichen (387 oder mehr Bytes im Binärformat) umfasst, abhängig vom Signaturtyp.

Die $privkey ist die Base64-Darstellung der Konkatenation aus dem [Ziel (Destination)](/docs/specs/common-structures#type_Destination), gefolgt vom [privaten Schlüssel (PrivateKey)](/docs/specs/common-structures#type_PrivateKey) und dann vom [signierenden privaten Schlüssel (SigningPrivateKey)](/docs/specs/common-structures#type_SigningPrivateKey), was 884 oder mehr Base64-Zeichen (663 oder mehr Bytes im Binärformat) ergibt, abhängig vom Signaturtyp. Das Binärformat ist in der Spezifikation für Private Key Files festgelegt.

Hinweise zum 256-Byte-binären [Privaten Schlüssel](/docs/specs/common-structures#type_PrivateKey): Dieses Feld wird seit Version 0.6 (2005) nicht mehr verwendet. SAM-Implementierungen können zufällige Daten oder ausschließlich Nullen in diesem Feld senden; keine Sorge, wenn im Base64 eine Reihe von AAAA erscheint. Die meisten Anwendungen speichern einfach die Base64-Zeichenkette und geben sie unverändert bei der SESSION CREATE zurück, oder decodieren sie zur Speicherung in Binärform und encodieren sie erneut für die SESSION CREATE. Anwendungen können jedoch die Base64-Zeichenkette decodieren, die Binärdaten gemäß der PrivateKeyFile-Spezifikation auswerten, den 256-Byte-Abschnitt mit dem privaten Schlüssel verwerfen und diesen bei der erneuten Kodierung für die SESSION CREATE durch 256 Bytes zufälliger Daten oder ausschließlich Nullen ersetzen. ALLE anderen Felder in der PrivateKeyFile-Spezifikation müssen erhalten bleiben. Dies würde 256 Byte Speicherplatz auf dem Dateisystem sparen, ist aber für die meisten Anwendungen vermutlich nicht den Aufwand wert. Weitere Informationen und Hintergründe finden sich in Vorschlag 161.

DEST GENERATE erfordert nicht, dass zuerst eine Sitzung erstellt wurde.

DEST GENERATE kann nicht verwendet werden, um eine Zieladresse mit Offline-Signaturen zu erstellen.

#### PING/PONG (SAM 3.2 oder höher)

Entweder der Client oder der Server kann senden:

```
PING[ arbitrary text]
```
an dem Steuerungsport, mit der Antwort:

```
PONG[ arbitrary text from the ping]
```
zur Verwendung für die Steuerung der Socket-Keepalive-Funktion. Entweder Seite kann die Sitzung und den Socket schließen, wenn innerhalb eines angemessenen, implementierungsabhängigen Zeitraums keine Antwort empfangen wird.

Wenn ein Timeout beim Warten auf ein PONG vom Client auftritt, kann die Bridge Folgendes senden:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
und dann trennen.

Wenn ein Timeout beim Warten auf ein PONG von der Bridge auftritt, kann der Client einfach die Verbindung trennen.

PING/PONG erfordern nicht, dass zuerst eine Sitzung erstellt wurde.

#### QUIT/STOP/EXIT (SAM 3.2 oder höher, optionale Funktionen)

Die Befehle QUIT, STOP und EXIT schließen die Sitzung und den Socket. Die Implementierung ist optional und dient der Vereinfachung von Tests über Telnet. Ob eine Antwort vor dem Schließen des Sockets gesendet wird (z. B. eine SESSION STATUS-Nachricht) ist implementierungsabhängig und außerhalb des Geltungsbereichs dieser Spezifikation.

QUIT/STOP/EXIT erfordern nicht, dass zuerst eine Sitzung erstellt wurde.

#### HILFE (optionales Feature)

Server können einen HELP-Befehl implementieren. Die Implementierung ist optional, um die einfache Überprüfung über Telnet zu ermöglichen. Format der Ausgabe und Erkennung des Endes der Ausgabe sind implementierungsabhängig und außerhalb des Geltungsbereichs dieser Spezifikation.

HELP erfordert nicht, dass zuerst eine Sitzung erstellt wurde.

#### Autorisierungskonfiguration (SAM 3.2 oder höher, optionales Feature)

Autorisierungskonfiguration mithilfe des AUTH-Befehls. Ein SAM-Server kann diese Befehle implementieren, um die dauerhafte Speicherung von Anmeldeinformationen zu ermöglichen. Die Konfiguration der Authentifizierung außerhalb dieser Befehle ist implementierungsabhängig und liegt außerhalb des Geltungsbereichs dieser Spezifikation.

- AUTH ENABLE aktiviert die Autorisierung für nachfolgende Verbindungen
- AUTH DISABLE deaktiviert die Autorisierung für nachfolgende Verbindungen
- AUTH ADD USER="foo" PASSWORD="bar" fügt einen Benutzer/Passwort hinzu
- AUTH REMOVE USER="foo" entfernt diesen Benutzer

Doppelte Anführungszeichen für Benutzername und Passwort sind empfohlen, aber nicht erforderlich. Ein doppeltes Anführungszeichen innerhalb eines Benutzernamens oder Passworts muss mit einem umgekehrten Schrägstrich (Backslash) maskiert werden. Bei einem Fehler antwortet der Server mit I2P_ERROR und einer Nachricht.

AUTH erfordert nicht, dass zuerst eine Sitzung erstellt wurde.

### RESULT-Werte

Dies sind die Werte, die vom RESULT-Feld übertragen werden können, zusammen mit ihrer Bedeutung:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Unterschiedliche Implementierungen könnten nicht konsistent sein, welches RESULTAT in verschiedenen Szenarien zurückgegeben wird.

Die meisten Antworten mit einem ERGEBNIS, das nicht OK ist, enthalten zusätzlich eine NACHRICHT mit weiteren Informationen. Die NACHRICHT ist im Allgemeinen hilfreich bei der Fehlersuche. Allerdings hängen NACHRICHT-Texte von der jeweiligen Implementierung ab, können je nach SAM-Server in die aktuelle Lokalisierung übersetzt werden oder auch nicht, möglicherweise interne, implementierungsabhängige Informationen wie Ausnahmen enthalten und sind ohne Ankündigung änderbar. Obwohl SAM-Clients die NACHRICHT-Texte Benutzern anzeigen dürfen, sollten sie keine programmatischen Entscheidungen auf deren Basis treffen, da dies instabil wäre.

### Tunnel-, I2CP- und Streaming-Optionen

Diese Optionen können als Name=Wert-Paare in der SAM SESSION CREATE-Zeile übergeben werden.

Alle Sitzungen können [I2CP-Optionen wie Tunnel-Längen und -Mengen](/docs/protocol/i2cp#options) enthalten. STREAM-Sitzungen können [Optionen der Streaming-Bibliothek](/docs/api/streaming#options) enthalten.

Siehe diese Referenzen für Optionennamen und Standardwerte. Die referenzierte Dokumentation bezieht sich auf die Java-Router-Implementierung. Standardwerte können sich ändern. Optionennamen und -werte beachten die Groß-/Kleinschreibung. Andere Router-Implementierungen unterstützen möglicherweise nicht alle Optionen und können abweichende Standardwerte haben; für Details siehe die jeweilige Router-Dokumentation.

### BASE64-Anmerkungen

Die Base64-Kodierung muss das I2P-Standard-Base64-Alphabet "A-Z, a-z, 0-9, -, ~" verwenden.

### Standard-SAM-Einrichtung

Der Standard-SAM-Port ist 7656. SAM ist im Java-I2P-Router standardmäßig nicht aktiviert; es muss manuell gestartet oder auf der Seite „Clients konfigurieren“ in der Routerkonsole oder in der Datei clients.config zur automatischen Ausführung konfiguriert werden. Der Standard-SAM-UDP-Port ist 7655 und lauscht auf 127.0.0.1. Diese Einstellungen können im Java-Router geändert werden, indem die Argumente sam.udp.port=nnnnn und/oder sam.udp.host=w.x.y.z dem Aufruf oder der SESSION-Zeile hinzugefügt werden.

Die Konfiguration in anderen Routern ist implementierungsspezifisch. Siehe [den i2pd-Konfigurationsleitfaden hier](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
