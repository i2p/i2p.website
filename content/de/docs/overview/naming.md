---
title: "Namensgebung und Adressbuch"
description: "Wie I2P menschenlesbare Hostnamen auf Ziele abbildet"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P-Adressen sind lange kryptographische Schlüssel. Das Namenssystem bietet eine benutzerfreundlichere Ebene über diesen Schlüsseln **ohne eine zentrale Autorität einzuführen**. Alle Namen sind **lokal**—jeder Router entscheidet unabhängig, auf welches Ziel sich ein Hostname bezieht.

> **Benötigen Sie Hintergrundinformationen?** Die [Naming-Diskussion](/docs/legacy/naming/) dokumentiert die ursprünglichen Designdebatten, alternativen Vorschläge und philosophischen Grundlagen hinter der dezentralisierten Namensgebung von I2P.

---

## 1. Komponenten

Die Namensschicht von I2P besteht aus mehreren unabhängigen, aber zusammenarbeitenden Subsystemen:

1. **Naming Service** – löst Hostnamen in Destinations auf und verarbeitet [Base32-Hostnamen](#base32-hostnames).
2. **HTTP-Proxy** – leitet `.i2p`-Anfragen an den Router weiter und schlägt Jump Services vor, wenn ein Name unbekannt ist.
3. **Host-Add Services** – CGI-artige Formulare, die neue Einträge in das lokale Adressbuch einfügen.
4. **Jump Services** – externe Helfer, die die Destination für einen angegebenen Hostnamen zurückgeben.
5. **Adressbuch** – ruft regelmäßig entfernte Host-Listen ab und führt sie unter Verwendung eines lokal vertrauenswürdigen „Web of Trust" zusammen.
6. **SusiDNS** – eine webbasierte Benutzeroberfläche zur Verwaltung von Adressbüchern, Abonnements und lokalen Überschreibungen.

Dieses modulare Design ermöglicht es Benutzern, ihre eigenen Vertrauensgrenzen zu definieren und den Benennungsprozess so weit wie gewünscht zu automatisieren.

---

## 2. Namensdienste

Die Naming-API des Routers (`net.i2p.client.naming`) unterstützt mehrere Backends durch die konfigurierbare Eigenschaft `i2p.naming.impl=<class>`. Jede Implementierung kann unterschiedliche Lookup-Strategien bieten, aber alle teilen dasselbe Vertrauens- und Auflösungsmodell.

### 2.1 Hosts.txt (legacy format)

Das veraltete Modell verwendete drei Klartext-Dateien, die der Reihe nach überprüft wurden:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Jede Zeile speichert eine `hostname=base64-destination` Zuordnung. Dieses einfache Textformat wird weiterhin vollständig für Import/Export unterstützt, ist jedoch nicht mehr die Standardeinstellung, da die Leistung nachlässt, sobald die Hostliste einige tausend Einträge überschreitet.

---

### 2.2 Blockfile Naming Service (default backend)

Eingeführt in **Release 0.8.8**, ist der Blockfile Naming Service nun das Standard-Backend. Er ersetzt Flachdateien durch einen hochperformanten Skiplist-basierten On-Disk-Key/Value-Store (`hostsdb.blockfile`), der etwa **10× schnellere Lookups** ermöglicht.

**Wichtige Merkmale:** - Speichert mehrere logische Adressbücher (privat, Benutzer und Hosts) in einer binären Datenbank. - Behält die Kompatibilität mit dem Import/Export von Legacy-hosts.txt bei. - Unterstützt Reverse-Lookups, Metadaten (Hinzufügedatum, Quelle, Kommentare) und effizientes Caching. - Verwendet die gleiche dreistufige Suchreihenfolge: privat → Benutzer → Hosts.

Dieser Ansatz bewahrt die Abwärtskompatibilität und verbessert gleichzeitig die Auflösungsgeschwindigkeit und Skalierbarkeit erheblich.

---

### 2.1 Hosts.txt (veraltetes Format)

Entwickler können benutzerdefinierte Backends implementieren, wie zum Beispiel: - **Meta** – aggregiert mehrere Namenssysteme. - **PetName** – unterstützt petnames, die in einer `petnames.txt` gespeichert sind. - **AddressDB**, **Exec**, **Eepget** und **Dummy** – für externe oder Fallback-Auflösung.

Die Blockfile-Implementierung bleibt das **empfohlene** Backend für die allgemeine Nutzung aufgrund von Leistung und Zuverlässigkeit.

---

## 3. Base32 Hostnames

Base32-Hostnamen (`*.b32.i2p`) funktionieren ähnlich wie Tors `.onion`-Adressen. Wenn Sie eine `.b32.i2p`-Adresse aufrufen:

1. Der Router dekodiert die Base32-Nutzlast.
2. Er rekonstruiert das Ziel direkt aus dem Schlüssel – **keine Adressbuch-Suche erforderlich**.

Dies garantiert die Erreichbarkeit, selbst wenn kein menschenlesbarer Hostname existiert. Erweiterte Base32-Namen, die in **Release 0.9.40** eingeführt wurden, unterstützen **LeaseSet2** und verschlüsselte Ziele.

---

## 4. Address Book & Subscriptions

Die Adressbuch-Anwendung ruft entfernte Host-Listen über HTTP ab und führt sie lokal gemäß benutzerkonfigurierter Vertrauensregeln zusammen.

### 2.2 Blockfile Naming Service (Standard-Backend)

- Abonnements sind Standard-`.i2p`-URLs, die auf `hosts.txt` oder inkrementelle Update-Feeds verweisen.
- Updates werden regelmäßig abgerufen (standardmäßig stündlich) und vor dem Zusammenführen validiert.
- Konflikte werden nach dem Prinzip **wer zuerst kommt, mahlt zuerst** aufgelöst, gemäß der Prioritätsreihenfolge:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Seit **I2P 2.3.0 (Juni 2023)** sind zwei Standard-Abonnementanbieter enthalten: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Diese Redundanz verbessert die Zuverlässigkeit unter Beibehaltung des lokalen Vertrauensmodells. Benutzer können Abonnements über SusiDNS hinzufügen oder entfernen.

#### Incremental Updates

Inkrementelle Updates werden über `newhosts.txt` abgerufen (ersetzt das ältere `recenthosts.cgi`-Konzept). Dieser Endpunkt bietet effiziente, **ETag-basierte** Delta-Updates – es werden nur neue Einträge seit der letzten Anfrage zurückgegeben oder `304 Not Modified`, wenn keine Änderungen vorliegen.

---

### 2.3 Alternative Backends und Plug-ins

- **Host-add services** (`add*.cgi`) ermöglichen die manuelle Übermittlung von Name-zu-Destination-Zuordnungen. Überprüfen Sie immer die Destination, bevor Sie sie akzeptieren.
- **Jump services** antworten mit dem entsprechenden Schlüssel und können über den HTTP-Proxy mit einem `?i2paddresshelper=`-Parameter umleiten.
  Häufige Beispiele: `stats.i2p`, `identiguy.i2p` und `notbob.i2p`.
  Diese Dienste sind **keine vertrauenswürdigen Autoritäten**—Benutzer müssen selbst entscheiden, welche sie verwenden möchten.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS ist verfügbar unter: `http://127.0.0.1:7657/susidns/`

Sie können: - Lokale Adressbücher ansehen und bearbeiten. - Abonnements verwalten und priorisieren. - Host-Listen importieren/exportieren. - Abrufpläne konfigurieren.

**Neu in I2P 2.8.1 (März 2025):** - Funktion "Nach neuesten sortieren" hinzugefügt. - Verbesserte Abonnementverwaltung (Behebung von ETag-Inkonsistenzen).

Alle Änderungen bleiben **lokal**—das Adressbuch jedes Routers ist einzigartig.

---

## 3. Base32-Hostnamen

Gemäß RFC 9476 hat I2P **`.i2p.alt`** im **März 2025 (I2P 2.8.1)** bei der GNUnet Assigned Numbers Authority (GANA) registriert.

**Zweck:** Verhinderung versehentlicher DNS-Lecks durch fehlkonfigurierte Software.

- RFC 9476-konforme DNS-Resolver werden `.alt`-Domains **nicht weiterleiten** an das öffentliche DNS.
- I2P-Software behandelt `.i2p.alt` als gleichwertig zu `.i2p` und entfernt das `.alt`-Suffix während der Auflösung.
- `.i2p.alt` ist **nicht** dazu gedacht, `.i2p` zu ersetzen; es ist eine technische Schutzmaßnahme, keine Umbenennung.

---

## 4. Adressbuch & Abonnements

- **Destination keys:** 516–616 Bytes (Base64)  
- **Hostnamen:** Max. 67 Zeichen (inklusive `.i2p`)  
- **Erlaubte Zeichen:** a–z, 0–9, `-`, `.` (keine doppelten Punkte, keine Großbuchstaben)  
- **Reserviert:** `*.b32.i2p`  
- **ETag und Last-Modified:** werden aktiv genutzt, um Bandbreite zu minimieren  
- **Durchschnittliche hosts.txt-Größe:** ~400 KB für ~800 Hosts (Beispielwert)  
- **Bandbreitennutzung:** ~10 Bytes/Sek. bei Abruf alle 12 Stunden

---

## 8. Security Model and Philosophy

I2P opfert absichtlich globale Eindeutigkeit zugunsten von Dezentralisierung und Sicherheit – eine direkte Anwendung von **Zooko's Triangle**.

**Kernprinzipien:** - **Keine zentrale Autorität:** alle Abfragen sind lokal.   - **Widerstandsfähigkeit gegen DNS-Hijacking:** Abfragen sind auf öffentliche Schlüssel des Ziels verschlüsselt.   - **Sybil-Angriffs-Prävention:** keine abstimmungs- oder konsensbasierte Namensgebung.   - **Unveränderliche Zuordnungen:** sobald eine lokale Zuordnung existiert, kann sie nicht remote überschrieben werden.

Blockchain-basierte Namenssysteme (z. B. Namecoin, ENS) haben versucht, alle drei Seiten von Zookos Dreieck zu lösen, aber I2P vermeidet diese bewusst aufgrund von Latenz, Komplexität und philosophischer Unvereinbarkeit mit seinem lokalen Vertrauensmodell.

---

## 9. Compatibility and Stability

- Zwischen 2023–2025 wurden keine Naming-Funktionen als veraltet markiert.
- Das Hosts.txt-Format, Jump-Services, Abonnements und alle Naming-API-Implementierungen bleiben funktionsfähig.
- Das I2P-Projekt gewährleistet strikte **Rückwärtskompatibilität**, während Leistungs- und Sicherheitsverbesserungen eingeführt werden (NetDB-Isolation, Sub-DB-Trennung usw.).

---

## 10. Best Practices

- Behalten Sie nur vertrauenswürdige Abonnements; vermeiden Sie große, unbekannte Host-Listen.
- Sichern Sie `hostsdb.blockfile` und `privatehosts.txt` vor dem Aktualisieren oder Neuinstallieren.
- Überprüfen Sie regelmäßig Jump-Dienste und deaktivieren Sie diejenigen, denen Sie nicht mehr vertrauen.
- Denken Sie daran: Ihr Adressbuch definiert Ihre Version der I2P-Welt—**jeder Hostname ist lokal**.

---

### Further Reading

- [Naming-Diskussion](/docs/legacy/naming/)  
- [Blockfile-Spezifikation](/docs/specs/blockfile/)  
- [Konfigurationsdatei-Format](/docs/specs/configuration/)  
- [Naming Service Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
