---
title: "Danke für das Herunterladen von I2P"
description: "Ihr Download hat begonnen. Unterstützen Sie die I2P-Entwicklung mit einer Spende."
layout: "download"
type: "spenden"
---

## Danke, dass Sie I2P heruntergeladen haben!

Ihr Download hat begonnen. Falls er nicht automatisch startet, überprüfen Sie bitte Ihren Download-Ordner oder kehren Sie zur [Download-Seite](/en/downloads/) zurück.

### Nächste Schritte

Jetzt, da Sie I2P haben, erfahren Sie hier, wie Sie loslegen können:

1. **Install I2P** - Follow our [installation guides](/en/docs/guides/) for your platform
2. **Configure Your Browser** - Set up your browser to use I2P with our [browser configuration guide](/en/docs/guides/browser-config/)
3. **Explore I2P Sites** - Start browsing .i2p sites and discover the I2P network
4. **Get Support** - Join our [community forums](/en/contact/#forums) or [IRC channels](/en/contact/#irc) if you need help

---

I2P ist ein anonymes Overlay-Netzwerk, das darauf abzielt, die Privatsphäre und Sicherheit der Kommunikation im Internet zu verbessern. Es verwendet Techniken wie garlic encryption, um die Metadaten der Benutzer zu schützen und die Rückverfolgbarkeit zu minimieren. 

## Installation

Um I2P zu installieren, laden Sie das Installationspaket von der [offiziellen I2P-Website](https://geti2p.net) herunter und folgen Sie den Anweisungen für Ihr Betriebssystem. 

### Konfiguration

Nach der Installation müssen Sie den I2P-Router konfigurieren. Öffnen Sie die `router.config`-Datei und passen Sie die Einstellungen nach Ihren Bedürfnissen an. 

Ein Beispiel für eine grundlegende Konfiguration:

```plaintext
router.externalPort=12345
router.externalHost=example.com
```

### Tunnels einrichten

I2P verwendet Tunnels, um den Datenverkehr zu anonymisieren. Jeder Tunnel besteht aus mehreren Hops, die den Datenverkehr durch das Netzwerk leiten. Um einen Tunnel einzurichten, verwenden Sie das I2PTunnel-Tool und konfigurieren Sie die Tunnelparameter in der `tunnels.conf`-Datei.

### Netzwerksicherheit

I2P bietet Schutz durch die Verwendung von NTCP2 und SSU-Protokollen, die für die Verschlüsselung und Authentifizierung der Verbindungen sorgen. Stellen Sie sicher, dass Ihr Router auf dem neuesten Stand ist, um die neuesten Sicherheitsupdates zu erhalten.

### Eepsites

Eepsites sind Websites, die innerhalb des I2P-Netzwerks gehostet werden. Sie bieten eine zusätzliche Ebene der Anonymität, da sie nur über das I2P-Netzwerk zugänglich sind. Um eine Eepsite zu erstellen, richten Sie einen Webserver ein und konfigurieren Sie ihn mit dem I2PTunnel-Tool.

Weitere Informationen finden Sie in der [I2P-Dokumentation](https://geti2p.net/de/docs).

### 💜 Unterstützung der I2P-Entwicklung

I2P ist ein **kostenloses, quelloffenes Projekt**, das von Freiwilligen auf der ganzen Welt aufgebaut und gepflegt wird. Wir haben **keine Unternehmensunterstützung, kein Risikokapital und keine Werbung**. Wir sind vollständig auf die Unterstützung der Gemeinschaft angewiesen, um das Netzwerk am Laufen zu halten und zu erweitern.

Ihre Spenden helfen uns: - Infrastruktur zu pflegen (Reseed-Server, Download-Spiegel, Build-Systeme) - Neue Funktionen zu entwickeln und die Leistung zu verbessern - Entwickler zu unterstützen, die ihre Zeit der Privattechnologie widmen - I2P für Nutzer überall kostenlos zu halten

#### Spenden mit Kryptowährung

<div class="crypto-box"> <h4>Monero (XMR) - Empfohlen</h4> <p>Monero bietet die stärksten Datenschutzgarantien. Alle Transaktionen sind vertraulich und nicht nachverfolgbar.</p> <div class="crypto-address">85igd4Dw6ychvi8iUYADHfgLCmdT348SA6sMnYgxE86YZxX98Au6rsF9B9DmcqEXWRZWDcPdarufHUUqwP73GVrq6BaC9dr</div> </div>

<div class="crypto-box"> <h4>Bitcoin (BTC)</h4> <div class="crypto-address">3JSSF45pAW5ujWbBuRFe25pBiwp1vjSRNb</div> </div>

<div class="crypto-box"> <h4>Zcash (ZEC)</h4> <div class="crypto-address">t1TwTuu4qU25aGvh59EMkCAZdmwJepkyQcD</div> </div>

<p style="margin-top: var(--spacing-lg); font-size: 0.9rem;">Möchten Sie mit einer anderen Kryptowährung spenden? <a href="/en/contact/">Kontaktieren Sie uns</a> und wir geben Ihnen eine Adresse.</p>

<p style="margin-top: var(--spacing-md);"><a href="/en/financial-support/" style="font-weight: 600;">Alle Spendenoptionen und finanzielle Transparenz anzeigen →</a></p>
