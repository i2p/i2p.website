---
title: "Reseed-Hosts"
description: "Betrieb von Reseed-Diensten und alternativen Bootstrap-Methoden"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Über Reseed-Hosts

Neue router benötigen eine Handvoll Peers, um dem I2P-Netzwerk beizutreten. Reseed-Hosts (Server für die anfängliche Peer-Bereitstellung) stellen dieses anfängliche Bootstrap-Set über verschlüsselte HTTPS-Downloads bereit. Jedes Reseed-Paket ist vom Host signiert und verhindert so Manipulationen durch nicht authentifizierte Parteien. Etablierte router können gelegentlich einen Reseed durchführen, wenn ihr Peer-Set veraltet ist.

### Netzwerk-Bootstrap-Prozess (Initialisierungsprozess)

Wenn ein I2P router zum ersten Mal startet oder über einen längeren Zeitraum offline war, benötigt er RouterInfo-Daten, um sich mit dem Netzwerk zu verbinden. Da der router keine vorhandenen Peers hat, kann er diese Informationen nicht aus dem I2P-Netzwerk selbst beziehen. Der Reseed-Mechanismus (Erstverbindung zum Netzwerk) löst dieses Bootstrap-Problem, indem er RouterInfo-Dateien von vertrauenswürdigen externen HTTPS-Servern bereitstellt.

Der Reseed-Prozess liefert 75-100 RouterInfo-Dateien in einem einzigen kryptografisch signierten Bündel. Dies stellt sicher, dass neue router schnell Verbindungen herstellen können, ohne sie Man-in-the-Middle-Angriffen auszusetzen, die sie in separate, nicht vertrauenswürdige Netzwerkpartitionen isolieren könnten.

### Aktueller Netzwerkstatus

Stand Oktober 2025 läuft das I2P-Netzwerk mit Router-Version 2.10.0 (API-Version 0.9.67). Das in Version 0.9.14 eingeführte Reseed-Protokoll bleibt in seiner Kernfunktionalität stabil und unverändert. Das Netzwerk betreibt mehrere unabhängige Reseed-Server, die weltweit verteilt sind, um Verfügbarkeit und Widerstandsfähigkeit gegen Zensur sicherzustellen.

Der Dienst [checki2p](https://checki2p.com/reseed) überwacht alle I2P-Reseed-Server alle 4 Stunden und bietet Echtzeit-Statusprüfungen sowie Verfügbarkeitsmetriken für die Reseed-Infrastruktur.

## Spezifikation des SU3-Dateiformats

Das SU3-Dateiformat ist die Grundlage des Reseed-Protokolls von I2P und ermöglicht die Bereitstellung kryptografisch signierter Inhalte. Das Verständnis dieses Formats ist für die Implementierung von Reseed-Servern und -Clients unerlässlich.

### Dateistruktur

Das SU3-Format besteht aus drei Hauptkomponenten: Header (40+ Bytes), Inhalt (variable Länge) und Signatur (deren Länge im Header angegeben ist).

#### Header-Format (Bytes 0-39 mindestens)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Reseed-spezifische SU3-Parameter

Für Reseed-Bundles muss die SU3-Datei die folgenden Eigenschaften aufweisen:

- **Dateiname**: Muss genau `i2pseeds.su3` sein
- **Inhaltstyp** (Byte 27): 0x03 (RESEED)
- **Dateityp** (Byte 25): 0x00 (ZIP)
- **Signaturtyp** (Bytes 8-9): 0x0006 (RSA-4096-SHA512)
- **Versionsstring**: Unix-Zeitstempel in ASCII (Sekunden seit der Unix-Epoche, im Format date +%s)
- **Signer-ID**: E-Mail-ähnlicher Bezeichner, der dem CN des X.509-Zertifikats entspricht

#### Query-Parameter für die Netzwerk-ID

Seit Version 0.9.42 fügen routers den Parameter `?netid=2` zu Reseed-Anfragen hinzu. Dies verhindert netzwerkübergreifende Verbindungen, da Testnetzwerke andere Netzwerk-IDs verwenden. Das aktuelle I2P-Produktionsnetz verwendet die Netzwerk-ID 2.

Beispielanfrage: `https://reseed.example.com/i2pseeds.su3?netid=2`

### ZIP-Inhaltsstruktur

Der Inhaltsabschnitt (nach dem Header, vor der Signatur) enthält ein Standard-ZIP-Archiv mit den folgenden Anforderungen:

- **Komprimierung**: Standard-ZIP-Komprimierung (DEFLATE)
- **Dateianzahl**: Typischerweise 75-100 RouterInfo-Dateien
- **Verzeichnisstruktur**: Alle Dateien müssen auf oberster Ebene liegen (keine Unterverzeichnisse)
- **Dateibenennung**: `routerInfo-{44-character-base64-hash}.dat`
- **Base64-Alphabet**: Es muss das von I2P modifizierte Base64-Alphabet verwendet werden

Das I2P-Base64-Alphabet unterscheidet sich von Standard-Base64, indem es `-` und `~` statt `+` und `/` verwendet, um die Kompatibilität mit Dateisystemen und URLs sicherzustellen.

### Kryptografische Signatur

Die Signatur deckt die gesamte Datei von Byte 0 bis zum Ende des Inhaltsabschnitts ab. Die Signatur selbst wird nach dem Inhalt angehängt.

#### Signaturalgorithmus (RSA-4096-SHA512)

1. Berechne den SHA-512-Hash der Bytes 0 bis zum Ende des Inhalts
2. Signiere den Hash mit "raw" RSA (NONEwithRSA in der Java-Terminologie)
3. Fülle die Signatur, falls erforderlich, mit führenden Nullen auf, um 512 Bytes zu erreichen
4. Hänge die 512-Byte-Signatur an die Datei an

#### Prozess der Signaturüberprüfung

Clients müssen:

1. Bytes 0-11 lesen, um Signaturtyp und -länge zu bestimmen
2. Gesamten Header lesen, um die Inhaltsgrenzen zu bestimmen
3. Inhalt streamen und dabei den SHA-512-Hash berechnen
4. Signatur vom Dateiende extrahieren
5. Signatur mithilfe des RSA-4096-öffentlichen Schlüssels des Unterzeichners verifizieren
6. Datei ablehnen, wenn die Signaturprüfung fehlschlägt

### Vertrauensmodell für Zertifikate

Reseed-Signaturschlüssel werden als selbstsignierte X.509-Zertifikate mit RSA-4096-Schlüsseln verteilt. Diese Zertifikate sind in I2P router-Paketen im Verzeichnis `certificates/reseed/` enthalten.

Zertifikatsformat: - **Schlüsseltyp**: RSA-4096 - **Signatur**: Selbstsigniert - **Subject CN**: Muss mit der Signer-ID im SU3-Header übereinstimmen - **Gültigkeitsdaten**: Clients sollten die Gültigkeitszeiträume des Zertifikats durchsetzen

## Einen Reseed-Host betreiben

Der Betrieb eines Reseed-Dienstes erfordert sorgfältige Beachtung von Anforderungen an Sicherheit, Zuverlässigkeit und Netzwerkdiversität. Mehr unabhängige Reseed-Hosts erhöhen die Resilienz und erschweren es Angreifern oder Zensoren, den Beitritt neuer router zu blockieren.

### Technische Anforderungen

#### Server-Spezifikationen

- **Betriebssystem**: Unix/Linux (Ubuntu, Debian, FreeBSD getestet und empfohlen)
- **Konnektivität**: Statische IPv4-Adresse erforderlich, IPv6 empfohlen, aber optional
- **CPU**: Mindestens 2 Kerne
- **RAM**: Mindestens 2 GB
- **Bandbreite**: Ungefähr 15 GB pro Monat
- **Betriebszeit**: 24/7-Betrieb erforderlich
- **I2P Router**: Gut integrierter I2P router, der durchgehend läuft

#### Softwareanforderungen

- **Java**: JDK 8 oder neuer (Java 17+ wird ab I2P 2.11.0 erforderlich sein)
- **Webserver**: nginx oder Apache mit Reverse-Proxy-Unterstützung (Lighttpd wird aufgrund von Einschränkungen des X-Forwarded-For-Headers nicht mehr unterstützt)
- **TLS/SSL**: Gültiges TLS-Zertifikat (Let's Encrypt, selbstsigniert oder kommerzielle CA (Zertifizierungsstelle))
- **DDoS-Schutz**: fail2ban oder gleichwertig (verpflichtend, nicht optional)
- **Reseed-Tools**: Offizielle reseed-tools von https://i2pgit.org/idk/reseed-tools

### Sicherheitsanforderungen

#### HTTPS/TLS-Konfiguration

- **Protokoll**: Nur HTTPS, kein HTTP-Fallback
- **TLS-Version**: Mindestens TLS 1.2
- **Cipher Suites**: Muss starke Chiffren unterstützen, die mit Java 8+ kompatibel sind
- **Zertifikats-CN/SAN**: Muss dem Hostnamen der bereitgestellten URL entsprechen
- **Zertifikatstyp**: Darf selbstsigniert sein, wenn dies mit dem Entwicklungsteam abgestimmt ist, oder von einer anerkannten Zertifizierungsstelle (CA) ausgestellt

#### Zertifikatsverwaltung

SU3-Signaturzertifikate und TLS-Zertifikate erfüllen unterschiedliche Zwecke:

- **TLS-Zertifikat** (`certificates/ssl/`): Sichert den HTTPS-Transport
- **SU3-Signaturzertifikat** (`certificates/reseed/`): Signiert Reseed-Bundles (Pakete zur Erstversorgung des netDb)

Beide Zertifikate müssen dem Reseed-Koordinator (zzz@mail.i2p) zur Aufnahme in router-Pakete übermittelt werden.

#### DDoS- und Scraping-Schutz

Reseed-Server sind periodischen Angriffen ausgesetzt – durch fehlerhafte Implementierungen, Botnets und böswillige Akteure, die versuchen, die netDb zu "scrapen" (automatisiert auszulesen). Schutzmaßnahmen umfassen:

- **fail2ban**: Erforderlich zur Ratenbegrenzung und zur Abwehr von Angriffen
- **Bundle-Diversität**: Unterschiedliche Sätze von RouterInfo (Router-Informationen in I2P) an verschiedene Anfragende ausliefern
- **Bundle-Konsistenz**: Dasselbe Bundle für wiederholte Anfragen von derselben IP innerhalb eines konfigurierbaren Zeitfensters ausliefern
- **IP-Protokollierungsbeschränkungen**: Keine Protokolle oder IP-Adressen veröffentlichen (Vorgabe der Datenschutzerklärung)

### Implementierungsmethoden

#### Methode 1: Offizielle reseed-tools (Empfohlen)

Die Referenzimplementierung, die vom I2P-Projekt gepflegt wird. Repository: https://i2pgit.org/idk/reseed-tools

**Installation**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
Beim ersten Start erzeugt das Tool: - `your-email@mail.i2p.crt` (SU3-Signaturzertifikat) - `your-email@mail.i2p.pem` (privater SU3-Signaturschlüssel) - `your-email@mail.i2p.crl` (Zertifikatsperrliste) - TLS-Zertifikat und -Schlüsseldateien

**Funktionen**: - Automatische Generierung von SU3 bundle (I2P-Update-Paketformat) (350 Varianten, jeweils 77 RouterInfos) - Integrierter HTTPS-Server - Cache alle 9 Stunden über cron neu aufbauen - Unterstützung des X-Forwarded-For-Headers mit dem Flag `--trustProxy` - Kompatibel mit Reverse-Proxy-Konfigurationen

**Bereitstellung für die Produktion**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Methode 2: Python-Implementierung (pyseeder)

Alternative Implementierung durch das PurpleI2P-Projekt: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Methode 3: Bereitstellung mit Docker

Für containerisierte Umgebungen existieren mehrere Docker-fähige Implementierungen:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Fügt Unterstützung für Tor-Onion-Service (versteckter Dienst) und IPFS hinzu

### Reverse-Proxy-Konfiguration

#### nginx-Konfiguration

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Apache-Konfiguration

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Registrierung und Koordination

Um Ihren reseed server (Server zur Erstinitialisierung des I2P-Netzes) in das offizielle I2P-Paket aufzunehmen:

1. Einrichtung und Tests abschließen
2. Sende beide Zertifikate (SU3 signing (Signierung des SU3-Containerformats) und TLS) an den Reseed-Koordinator
3. Kontakt: zzz@mail.i2p oder zzz@i2pmail.org
4. Trete #i2p-dev auf IRC2P bei zur Koordination mit anderen Operatoren

### Betriebliche bewährte Verfahren

#### Überwachung und Protokollierung

- Aktivieren Sie das kombinierte Apache/nginx-Logformat für Statistiken
- Logrotation implementieren (Protokolle wachsen schnell)
- Erfolg der Bundle-Erstellung und Zeiten für erneute Builds überwachen
- Bandbreitennutzung und Anfragemuster nachverfolgen
- IP-Adressen oder detaillierte Zugriffsprotokolle niemals veröffentlichen

#### Wartungsplan

- **Alle 9 Stunden**: SU3-Bundle-Cache neu aufbauen (automatisiert per cron)
- **Wöchentlich**: Protokolle auf Angriffsmuster prüfen
- **Monatlich**: I2P router und reseed-tools aktualisieren
- **Bei Bedarf**: TLS-Zertifikate erneuern (mit Let's Encrypt automatisieren)

#### Portauswahl

- Standard: 8443 (empfohlen)
- Alternative: Beliebiger Port zwischen 1024-49151
- Port 443: Erfordert Root-Rechte oder Portweiterleitung (iptables redirect empfohlen)

Beispiel für Portweiterleitung:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Alternative Reseed-Methoden (Reseed = initiales Laden von netDb-Einträgen)

Weitere Bootstrap-Optionen helfen Nutzern hinter restriktiven Netzwerken:

### Dateibasierter Reseed (Erst-/Neusynchronisierung der netDb)

Mit Version 0.9.16 eingeführt, ermöglicht das file-based reseeding (Reseed per Datei) Nutzern, RouterInfo-Bundles manuell zu laden. Diese Methode ist besonders nützlich für Nutzer in zensierten Regionen, in denen HTTPS-Reseed-Server blockiert sind.

**Ablauf**: 1. Eine vertrauenswürdige Kontaktperson erstellt mit ihrem router ein SU3-Bundle 2. Das Bundle wird per E-Mail, USB-Laufwerk oder über einen anderen Out-of-Band-Kanal übertragen 3. Der Nutzer legt `i2pseeds.su3` in das I2P-Konfigurationsverzeichnis 4. Der router erkennt und verarbeitet das Bundle beim Neustart automatisch

**Dokumentation**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Anwendungsfälle**: - Nutzer hinter staatlichen Firewalls, die Reseed-Server blockieren - Isolierte Netzwerke, die ein manuelles Bootstrapping erfordern - Test- und Entwicklungsumgebungen

### Cloudflare-vermitteltes Reseeding (Netzwerk-Initialisierung)

Die Weiterleitung von Reseed-Datenverkehr (Erstverbindungsaufbau zu I2P über Reseed-Server) über das CDN von Cloudflare bietet Betreibern in Regionen mit starker Zensur mehrere Vorteile.

**Vorteile**: - IP-Adresse des Origin-Servers vor Clients verborgen - DDoS-Schutz über Cloudflares Infrastruktur - Geografische Lastverteilung durch Edge-Caching - Verbesserte Performance für globale Clients

**Implementierungsanforderungen**: - `--trustProxy`-Flag in reseed-tools aktiviert - Cloudflare-Proxy für DNS-Eintrag aktiviert - Korrekte Handhabung des X-Forwarded-For-Headers

**Wichtige Hinweise**: - Cloudflare-Portbeschränkungen gelten (es müssen unterstützte Ports verwendet werden) - Konsistenz für dasselbe Client-Bundle erfordert Unterstützung für X-Forwarded-For - SSL/TLS-Konfiguration wird von Cloudflare verwaltet

**Dokumentation**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Zensurresistente Strategien

Die Forschung von Nguyen Phong Hoang (USENIX FOCI 2019) identifiziert zusätzliche Bootstrapping-Methoden für zensierte Netzwerke:

#### Cloud-Speicheranbieter

- **Box, Dropbox, Google Drive, OneDrive**: SU3-Dateien über öffentliche Links bereitstellen
- **Vorteil**: Schwer zu blockieren, ohne legitime Dienste zu beeinträchtigen
- **Einschränkung**: Erfordert die manuelle Weitergabe der URLs an die Benutzer

#### IPFS-Verteilung

- Reseed-Bundles auf dem InterPlanetary File System (IPFS, inhaltsadressiertes, verteiltes Dateisystem) hosten
- Inhaltsadressierter Speicher verhindert Manipulation
- Widerstandsfähig gegen Takedown-Versuche

#### Tor-Onion-Dienste

- Reseed-Server (Server zum initialen Herunterladen von netDb-Einträgen), über .onion-Adressen erreichbar
- Resistent gegen IP-basierte Sperrungen
- Erfordert einen Tor-Client auf dem System des Nutzers

**Forschungsdokumentation**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Länder, die I2P bekanntermaßen blockieren

Stand 2025 ist bestätigt, dass die folgenden Länder I2P-Reseed-Server (Server zur anfänglichen Peer-Versorgung neuer I2P router) blockieren: - China - Iran - Oman - Katar - Kuwait

Benutzer in diesen Regionen sollten alternative Bootstrap-Methoden oder zensurresistente Reseeding-Strategien verwenden.

## Protokolldetails für Implementierer

### Spezifikation für Reseed-Anfragen (Initialbefüllung der netDb)

#### Client-Verhalten

1. **Serverauswahl**: Router verwaltet eine hartcodierte Liste von Reseed-URLs
2. **Zufallsauswahl**: Client wählt zufällig einen Server aus der verfügbaren Liste
3. **Anfrageformat**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Sollte gängigen Browsern ähneln (z. B. "Wget/1.11.4")
5. **Wiederholungslogik**: Wenn die SU3-Anfrage fehlschlägt, auf das Parsen der Indexseite zurückgreifen
6. **Zertifikatsprüfung**: TLS-Zertifikat gegen den System-Zertifikatsspeicher prüfen
7. **SU3-Signaturprüfung**: Signatur gegen bekannte Reseed-Zertifikate verifizieren

#### Serververhalten

1. **Bundle-Auswahl**: Wähle eine pseudozufällige Teilmenge von RouterInfos aus der netDb aus
2. **Client-Tracking**: Anfragen anhand der Quell-IP identifizieren (unter Berücksichtigung von X-Forwarded-For)
3. **Bundle-Konsistenz**: Bei wiederholten Anfragen innerhalb eines Zeitfensters (typischerweise 8–12 Stunden) dasselbe Bundle zurückgeben
4. **Bundle-Diversität**: Verschiedenen Clients unterschiedliche Bundles zurückgeben, um die Netzwerkdiversität zu erhöhen
5. **Content-Type**: `application/octet-stream` oder `application/x-i2p-reseed`

### RouterInfo-Dateiformat

Jede `.dat`-Datei im Reseed-Paket enthält eine RouterInfo-Struktur:

**Dateibenennung**: `routerInfo-{base64-hash}.dat` - Der Hash besteht aus 44 Zeichen und verwendet das I2P-Base64-Alphabet - Beispiel: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Dateiinhalt**: - RouterIdentity (router-Hash, Verschlüsselungsschlüssel, Signaturschlüssel) - Veröffentlichungszeitstempel - router-Adressen (IP, Port, Transporttyp) - router-Fähigkeiten und Optionen - Signatur, die alle oben genannten Daten abdeckt

### Anforderungen an die Netzwerkdiversität

Um Netzwerkzentralisierung zu verhindern und die Erkennung von Sybil-Angriffen zu ermöglichen:

- **Keine vollständigen NetDb-Dumps**: Niemals alle RouterInfos an einen einzelnen Client ausliefern
- **Zufällige Auswahl**: Jedes Bündel enthält eine andere Teilmenge der verfügbaren Peers
- **Minimale Bündelgröße**: 75 RouterInfos (erhöht von ursprünglich 50)
- **Maximale Bündelgröße**: 100 RouterInfos
- **Aktualität**: RouterInfos sollten aktuell sein (innerhalb von 24 Stunden nach der Erstellung)

### Überlegungen zu IPv6

**Aktueller Status** (2025): - Mehrere Reseed-Server reagieren über IPv6 nicht - Clients sollten aus Zuverlässigkeitsgründen IPv4 bevorzugen oder erzwingen - IPv6-Unterstützung wird für neue Bereitstellungen empfohlen, ist aber nicht kritisch

**Implementierungshinweis**: Beim Konfigurieren von Dual-Stack-Servern stellen Sie sicher, dass sowohl die IPv4- als auch die IPv6-Bind-Adressen korrekt funktionieren oder deaktivieren Sie IPv6, wenn es nicht ordnungsgemäß unterstützt werden kann.

## Sicherheitsüberlegungen

### Bedrohungsmodell

Das reseed protocol (Reseed‑Protokoll, Mechanismus zum Erstbezug von Peer‑Informationen für I2P) schützt vor:

1. **Man-in-the-Middle-Angriffe**: RSA-4096-Signaturen verhindern die Manipulation von Bundles
2. **Netzwerkpartitionierung**: Mehrere unabhängige Reseed-Server verhindern einen einzelnen Kontrollpunkt
3. **Sybil-Angriffe**: Die Vielfalt der Bundles begrenzt die Fähigkeit des Angreifers, Nutzer zu isolieren
4. **Zensur**: Mehrere Server und alternative Methoden sorgen für Redundanz

Das Reseed-Protokoll schützt NICHT vor:

1. **Kompromittierte reseed-Server** (Server für die Erstinitialisierung ins I2P-Netzwerk): Wenn ein Angreifer die privaten Schlüssel der reseed-Zertifikate kontrolliert
2. **Vollständige Netzblockade**: Wenn alle reseed-Methoden in einer Region blockiert sind
3. **Langfristige Überwachung**: reseed-Anfragen geben die IP-Adresse des Nutzers preis, der versucht, I2P beizutreten

### Zertifikatsverwaltung

**Sicherheit privater Schlüssel**: - SU3-Signaturschlüssel offline aufbewahren, wenn sie nicht verwendet werden - Starke Passwörter für die Schlüsselverschlüsselung verwenden - Sichere Backups von Schlüsseln und Zertifikaten vorhalten - Für hochwertige Bereitstellungen Hardware-Sicherheitsmodule (HSMs) in Betracht ziehen

**Zertifikatswiderruf**: - Zertifikatsperrlisten (CRLs) werden über einen News-Feed verteilt - Kompromittierte Zertifikate können vom Koordinator widerrufen werden - Routers aktualisieren CRLs bei Software-Updates automatisch

### Maßnahmen zur Angriffsabwehr

**DDoS-Schutz**: - fail2ban-Regeln für exzessive Anfragen - Rate-Limiting auf Webserver-Ebene - Verbindungsbegrenzungen pro IP-Adresse - Cloudflare oder ein ähnliches CDN als zusätzliche Schutzschicht

**Scraping-Schutz**: - Unterschiedliche Bundles pro anfragender IP-Adresse - Zeitbasierte Zwischenspeicherung von Bundles pro IP-Adresse - Protokollierung von Mustern, die auf Scraping-Versuche hindeuten - Koordination mit anderen Betreibern bei erkannten Angriffen

## Tests und Validierung

### Testen Ihres Reseed-Servers

#### Methode 1: Neuinstallation des Routers

1. I2P auf einem sauberen System installieren
2. Ihre reseed URL (Quelle für die initiale Peer-/Netzwerk-Information) zur Konfiguration hinzufügen
3. Andere reseed URLs entfernen oder deaktivieren
4. Den router starten und die Protokolle auf ein erfolgreiches reseed überwachen
5. Innerhalb von 5–10 Minuten die Verbindung zum Netzwerk überprüfen

Erwartete Logausgabe:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Methode 2: Manuelle SU3-Validierung

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Methode 3: checki2p-Monitoring

Der Dienst unter https://checki2p.com/reseed führt alle 4 Stunden automatisierte Prüfungen auf allen registrierten I2P-Reseed-Servern durch. Dies ermöglicht:

- Verfügbarkeitsüberwachung
- Metriken zur Antwortzeit
- TLS-Zertifikatsvalidierung
- Überprüfung der SU3-Signatur
- Historische Betriebszeitdaten

Sobald Ihr Reseed-Server (Server zum Initialisieren der netDb) beim I2P-Projekt registriert ist, erscheint er innerhalb von 24 Stunden automatisch auf checki2p.

### Fehlerbehebung bei häufigen Problemen

**Problem**: "Unable to read signing key" beim ersten Start - **Lösung**: Das ist erwartetes Verhalten. Antworten Sie mit 'y', um neue Schlüssel zu erzeugen.

**Problem**: Router kann Signatur nicht verifizieren - **Ursache**: Zertifikat nicht im Vertrauensspeicher des Routers - **Lösung**: Zertifikat im Verzeichnis `~/.i2p/certificates/reseed/` ablegen

**Problem**: Dasselbe Bundle wird an verschiedene Clients ausgeliefert - **Ursache**: X-Forwarded-For-Header wird nicht korrekt weitergegeben - **Lösung**: Aktiviere `--trustProxy` und konfiguriere die Reverse-Proxy-Header

**Problem**: "Connection refused"-Fehler - **Ursache**: Port vom Internet aus nicht erreichbar - **Lösung**: Firewall-Regeln prüfen, Portweiterleitung überprüfen

**Problem**: Hohe CPU-Auslastung während des Bundle-Neuaufbaus - **Ursache**: Normales Verhalten beim Generieren von 350+ SU3-Varianten - **Lösung**: Ausreichende CPU-Ressourcen sicherstellen, ggf. die Neuaufbaufrequenz reduzieren

## Referenzinformationen

### Offizielle Dokumentation

- **Leitfaden für Reseed-Mitwirkende**: /guides/creating-and-running-an-i2p-reseed-server/
- **Anforderungen der Reseed-Richtlinie**: /guides/reseed-policy/
- **SU3-Spezifikation**: /docs/specs/updates/
- **Repository für Reseed-Tools**: https://i2pgit.org/idk/reseed-tools
- **Dokumentation der Reseed-Tools**: https://eyedeekay.github.io/reseed-tools/

### Alternative Implementierungen

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Python-WSGI-Reseed-Server**: https://github.com/torbjo/i2p-reseeder

### Community-Ressourcen

- **I2P-Forum**: https://i2pforum.net/
- **Gitea-Repository**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev auf IRC2P
- **Statusüberwachung**: https://checki2p.com/reseed

### Versionsverlauf

- **0.9.14** (2014): SU3-Reseed-Format eingeführt
- **0.9.16** (2014): Dateibasiertes Reseeding hinzugefügt
- **0.9.42** (2019): Erfordernis des Abfrageparameters 'Network ID'
- **2.0.0** (2022): SSU2-Transportprotokoll eingeführt
- **2.4.0** (2024): NetDB-Isolation und Sicherheitsverbesserungen
- **2.6.0** (2024): I2P-over-Tor-Verbindungen blockiert
- **2.10.0** (2025): Aktuelle stabile Version (Stand: September 2025)

### Signaturtypen-Referenz

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Reseed-Standard**: Typ 6 (RSA-SHA512-4096) ist für Reseed-Bundles erforderlich.

## Danksagung

Vielen Dank an alle Reseed-Operatoren (Betreiber von Reseed-Servern) dafür, dass sie das Netzwerk zugänglich und widerstandsfähig halten. Besondere Anerkennung für die folgenden Mitwirkenden und Projekte:

- **zzz**: Langjähriger I2P-Entwickler und Reseed-Koordinator (Reseed: initiale Befüllung der netDb über Seed-Server)
- **idk**: Aktueller Maintainer von reseed-tools und Release-Manager
- **Nguyen Phong Hoang**: Forschung zu zensurresistenten Reseed-Strategien
- **PurpleI2P Team**: Alternative I2P-Implementierungen und -Werkzeuge
- **checki2p**: Automatisierter Überwachungsdienst für die Reseed-Infrastruktur

Die dezentrale Reseed-Infrastruktur (Reseed = initiale Beschaffung von netDb-Peers zum Start ins Netzwerk) des I2P-Netzwerks ist das Ergebnis der Zusammenarbeit Dutzender Betreiber weltweit und stellt sicher, dass neue Nutzer unabhängig von lokaler Zensur oder technischen Hürden stets einen Weg finden, dem Netzwerk beizutreten.
