---
title: "Befehle für Adressabonnement-Feeds"
description: "Erweiterung für Adressbuch-Abonnement-Feeds, die es Inhabern von Hostnamen ermöglicht, ihre Einträge zu aktualisieren und zu verwalten"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Übersicht

Diese Spezifikation erweitert den Adressbuch-Abonnement-Feed um Befehle und ermöglicht es Nameservern, Eintragsaktualisierungen von Hostnamen-Inhabern zu verbreiten. Ursprünglich vorgeschlagen in [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (September 2014), implementiert in Version 0.9.26 (Juni 2016) und netzwerkweit ausgerollt mit Status ABGESCHLOSSEN.

Das System ist seit seiner ursprünglichen Implementierung stabil und unverändert geblieben und funktioniert weiterhin identisch unter I2P 2.10.0 (Router API 0.9.65, September 2025).

## Motivation

Früher lieferten die Abonnementserver für hosts.txt Daten nur im einfachen hosts.txt-Format:

```
example.i2p=b64destination
```
Dieses grundlegende Format führte zu mehreren Problemen:

- Hostname-Inhaber können die mit ihren Hostnamen verknüpfte Destination (Zieladresse) nicht aktualisieren (zum Beispiel, um den Signaturschlüssel auf einen stärkeren kryptografischen Typ umzustellen).
- Hostname-Inhaber können ihre Hostnamen nicht beliebig übertragen. Sie müssen die entsprechenden privaten Schlüssel der Destination direkt an den neuen Inhaber übergeben.
- Es gibt keine Möglichkeit, nachzuweisen, dass eine Subdomain vom zugehörigen Basis-Hostname kontrolliert wird. Dies wird derzeit nur individuell von einigen Nameservern durchgesetzt.

## Entwurf

Diese Spezifikation fügt dem hosts.txt-Format Befehlszeilen hinzu. Mit diesen Befehlen können Nameserver ihre Dienste erweitern und zusätzliche Funktionen bereitstellen. Clients, die diese Spezifikation implementieren, können über den regulären Abonnementprozess auf diese Funktionen lauschen.

Alle Befehlszeilen müssen von der entsprechenden Destination (I2P-Zieladresse) signiert sein. Dies stellt sicher, dass Änderungen nur auf Anforderung des Inhabers des Hostnamens vorgenommen werden.

## Sicherheitsauswirkungen

Diese Spezifikation beeinflusst die Anonymität nicht.

Es gibt ein erhöhtes Risiko, die Kontrolle über einen Destination-Schlüssel zu verlieren, da jemand, der ihn erlangt, diese Befehle verwenden kann, um Änderungen an beliebigen zugehörigen Hostnamen vorzunehmen. Dies stellt jedoch kein größeres Problem dar als der Status quo, in dem jemand, der eine Destination (I2P-Zieladresse) erlangt, sich als Hostname ausgeben und (teilweise) dessen Datenverkehr übernehmen kann. Das erhöhte Risiko wird dadurch ausgeglichen, dass Inhaber von Hostnamen die Möglichkeit erhalten, die einem Hostnamen zugeordnete Destination zu ändern, falls sie glauben, dass die Destination kompromittiert wurde. Dies ist mit dem aktuellen System nicht möglich.

## Spezifikation

### Neue Linientypen

Es gibt zwei neue Linientypen:

1. **Befehle zum Hinzufügen und Ändern:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Befehle entfernen:**

```
#!key1=val1#key2=val2...
```
#### Reihenfolge

Ein Feed ist nicht notwendigerweise in der richtigen Reihenfolge oder vollständig. Zum Beispiel kann ein change command in einer Zeile vor einem add command erscheinen oder ganz ohne add command.

Schlüssel können in beliebiger Reihenfolge angeordnet sein. Doppelte Schlüssel sind nicht zulässig. Bei allen Schlüsseln und Werten wird die Groß- und Kleinschreibung berücksichtigt.

### Allgemeine Schlüssel

**In allen Befehlen erforderlich:**

**sig** : Base64-Signatur, unter Verwendung des Signaturschlüssels der Destination (Zieladresse)

**Verweise auf einen zweiten Hostnamen und/oder eine Destination (Zieladresse):**

**oldname** : Ein zweiter Hostname (neu oder geändert)

**olddest** : Eine zweite Base64-Destination (neu oder geändert)

**oldsig** : Eine zweite Base64-Signatur, unter Verwendung des Signaturschlüssels aus olddest

**Weitere häufig verwendete Schlüssel:**

**Aktion** : Ein Befehl

**name** : Der Hostname, nur vorhanden, wenn `example.i2p=b64dest` nicht vorangestellt ist

**dest** : Die Base64-Zieladresse, nur vorhanden, sofern `example.i2p=b64dest` nicht vorangestellt ist

**date** : In Sekunden seit der Epoche

**expires** : In Sekunden seit der Unix-Epoche

### Befehle

Alle Befehle außer dem "Add"-Befehl müssen ein `action=command`-Schlüssel-Wert-Paar enthalten.

Zur Gewährleistung der Kompatibilität mit älteren Clients wird den meisten Befehlen, wie unten beschrieben, `example.i2p=b64dest` vorangestellt. Bei Änderungen sind dies stets die neuen Werte. Etwaige alte Werte sind im Schlüssel/Wert-Abschnitt enthalten.

Die aufgeführten Schlüssel sind erforderlich. Alle Befehle können zusätzliche Schlüssel-Wert-Paare enthalten, die hier nicht definiert sind.

#### Hostname hinzufügen

**Mit example.i2p=b64dest vorangestellt** : JA, das ist der neue Hostname und die neue Destination (I2P-Zieladresse).

**Aktion** : NICHT enthalten, es ist implizit.

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!sig=b64sig
```
#### Hostname ändern

**Mit vorangestelltem example.i2p=b64dest** : JA, dies ist der neue Hostname und das alte Ziel.

**Aktion** : changename

**oldname** : der alte Hostname, der ersetzt werden soll

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Ziel ändern

**Mit example.i2p=b64dest eingeleitet** : JA, dies ist der alte Hostname und die neue Destination (Zieladresse).

**action** : changedest

**olddest** : das alte Ziel, das ersetzt werden soll

**oldsig** : Signatur unter Verwendung von olddest

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Hostname-Alias hinzufügen

**Vorangestellt durch example.i2p=b64dest** : JA, das ist der neue (Alias-)Hostname und die alte Zieladresse.

**Aktion** : addname

**oldname** : der alte Hostname

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Destination-Alias hinzufügen

(Wird für ein Kryptografie-Upgrade verwendet)

**Mit vorangestelltem example.i2p=b64dest** : JA, dies ist der alte Hostname und die neue (alternative) Destination (Zieladresse in I2P).

**action** : adddest

**olddest** : das alte Ziel

**oldsig** : Signatur mit olddest

**sig** : Signatur unter Verwendung von dest

Beispiel:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Subdomain hinzufügen

**Mit vorangestelltem subdomain.example.i2p=b64dest** : JA, dies ist der neue Subdomain-Name und das Ziel.

**action** : addsubdomain

**oldname** : der übergeordnete Hostname (example.i2p)

**olddest** : das übergeordnete Ziel (z. B. example.i2p)

**oldsig** : Signatur mit olddest

**sig** : Signatur mithilfe von dest

Beispiel:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Metadaten aktualisieren

**Vorangestellt durch example.i2p=b64dest** : JA, dies ist der alte Hostname und die Zieladresse.

**Aktion** : Aktualisierung

**sig** : Signatur

(Fügen Sie hier alle aktualisierten Schlüssel hinzu)

Beispiel:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Hostname entfernen

**Mit example.i2p=b64dest vorangestellt** : NEIN, diese werden in den Optionen angegeben

**Aktion** : entfernen

**name** : der Hostname

**dest** : das Ziel

**sig** : Signatur

Beispiel:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Alle mit diesem Ziel entfernen

**Vorangestellt durch example.i2p=b64dest** : NEIN, diese werden in den Optionen festgelegt

**Aktion** : removeall

**dest** : die Destination (Zieladresse)

**sig** : Signatur

Beispiel:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Signaturen

Alle Befehle müssen von der zugehörigen Destination (Zieladresse) signiert werden. Befehle mit zwei Destinations benötigen möglicherweise zwei Signaturen.

`oldsig` ist immer die "innere" Signatur. Signieren und verifizieren, ohne dass die Schlüssel `oldsig` oder `sig` vorhanden sind. `sig` ist immer die "äußere" Signatur. Signieren und verifizieren mit vorhandenem `oldsig`-Schlüssel, aber ohne `sig`-Schlüssel.

#### Eingaben für Signaturen

Um einen Bytestrom zu erzeugen, mit dem die Signatur erstellt oder verifiziert werden kann, serialisieren Sie wie folgt:

1. Entferne den Schlüssel `sig`
2. Wenn mit `oldsig` verifiziert wird, entferne außerdem den Schlüssel `oldsig`
3. Nur für Add- oder Change-Kommandos (Hinzufügen bzw. Ändern): `example.i2p=b64dest` ausgeben
4. Wenn noch Schlüssel übrig sind, `#!` ausgeben
5. Sortiere die Optionen nach dem UTF-8-Schlüssel, bei doppelten Schlüsseln fehlschlagen
6. Für jedes Schlüssel/Wert-Paar `key=value` ausgeben, gefolgt von (falls nicht das letzte Schlüssel/Wert-Paar) einem `#`

**Hinweise**

- Keinen Zeilenumbruch ausgeben
- Die Ausgabekodierung ist UTF-8
- Die Kodierung aller Ziele und Signaturen erfolgt in Base 64 mit dem I2P-Alphabet
- Schlüssel und Werte unterscheiden Groß- und Kleinschreibung
- Hostnamen müssen in Kleinbuchstaben geschrieben sein

#### Aktuelle Signaturtypen

Seit I2P 2.10.0 werden für Ziele folgende Signaturtypen unterstützt:

- **EdDSA_SHA512_Ed25519** (Typ 7): Seit 0.9.15 am häufigsten für Destinations. Verwendet einen 32-Byte langen öffentlichen Schlüssel und eine 64-Byte-Signatur. Dies ist der empfohlene Signaturtyp für neue Destinations.
- **RedDSA_SHA512_Ed25519** (Typ 13): Nur für Destinations und verschlüsselte leaseSets verfügbar (seit 0.9.39).
- Veraltete Typen (DSA_SHA1, ECDSA-Varianten): weiterhin unterstützt, aber seit 0.9.58 für neue Router-Identitäten als veraltet markiert.

Hinweis: Post-Quanten-kryptografische Optionen sind seit I2P 2.10.0 verfügbar, jedoch noch nicht die Standard-Signaturtypen.

## Kompatibilität

Alle neuen Zeilen im hosts.txt-Format sind mithilfe vorangestellter Kommentarzeichen (`#!`) implementiert, sodass alle älteren I2P-Versionen die neuen Anweisungen als Kommentare interpretieren und sie problemlos ignorieren.

Wenn I2P routers auf die neue Spezifikation aktualisiert werden, werden sie alte Kommentare nicht neu interpretieren, sondern bei nachfolgenden Abrufen ihrer Abonnement-Feeds beginnen, neue Befehle zu verarbeiten. Daher ist es wichtig, dass Namensserver Befehlseinträge in irgendeiner Form dauerhaft vorhalten oder ETag-Unterstützung aktivieren, damit routers alle bisherigen Befehle abrufen können.

## Implementierungsstatus

**Erste Bereitstellung:** Version 0.9.26 (7. Juni 2016)

**Aktueller Status:** Stabil und unverändert bis einschließlich I2P 2.10.0 (Router API 0.9.65, September 2025)

**Status des Vorschlags:** GESCHLOSSEN (netzwerkweit erfolgreich ausgerollt)

**Implementierungsort:** `apps/addressbook/java/src/net/i2p/addressbook/` im I2P Java router

**Wichtige Klassen:** - `SubscriptionList.java`: Verwaltet die Abonnementverarbeitung - `Subscription.java`: Bearbeitet einzelne Abonnement-Feeds - `AddressBook.java`: Kernfunktionalität des Adressbuchs - `Daemon.java`: Hintergrunddienst für das Adressbuch

**Standard-Abonnement-URL:** `http://i2p-projekt.i2p/hosts.txt`

## Transportdetails

Abonnements verwenden HTTP mit Unterstützung für bedingte GET-Anfragen:

- **ETag-Header:** Unterstützt effiziente Änderungserkennung
- **Last-Modified-Header:** Erfasst die Aktualisierungszeiten von Abonnements
- **304 Not Modified:** Server sollten dies zurückgeben, wenn sich der Inhalt nicht geändert hat
- **Content-Length:** Wird für alle Antworten dringend empfohlen

Der I2P router verwendet standardmäßiges HTTP-Client-Verhalten mit korrekter Cache-Unterstützung.

## Versionskontext

**Hinweis zur I2P-Versionierung:** Ab etwa Version 1.5.0 (August 2021) wechselte I2P von der 0.9.x-Versionierung zur semantischen Versionierung (1.x, 2.x usw.). Die interne Version der Router API verwendet jedoch weiterhin die 0.9.x-Nummerierung aus Gründen der Abwärtskompatibilität. Stand Oktober 2025 ist die aktuelle Version I2P 2.10.0 mit der Router API in Version 0.9.65.

Dieses Spezifikationsdokument wurde ursprünglich für Version 0.9.49 (Februar 2021) verfasst und ist für die aktuelle Version 0.9.65 (I2P 2.10.0) weiterhin vollständig zutreffend, da am Abonnement-Feed-System seit seiner ursprünglichen Implementierung in 0.9.26 keine Änderungen vorgenommen wurden.

## Referenzen

- [Vorschlag 112 (Original)](/proposals/112-addressbook-subscription-feed-commands/)
- [Offizielle Spezifikation](/docs/specs/subscription/)
- [I2P-Dokumentation zum Namenssystem](/docs/overview/naming/)
- [Spezifikation allgemeiner Strukturen](/docs/specs/common-structures/)
- [I2P-Quellcode-Repository](https://github.com/i2p/i2p.i2p)
- [I2P-Gitea-Repository](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Verwandte Entwicklungen

Auch wenn sich das Abonnement-Feed-System selbst nicht geändert hat, könnten die folgenden damit zusammenhängenden Entwicklungen in I2Ps Namensinfrastruktur von Interesse sein:

- **Erweiterte Base32-Namen** (0.9.40+): Unterstützung für Base32-Adressen mit 56+ Zeichen für verschlüsselte leaseSets. Beeinflusst das Format des Abonnement-Feeds nicht.
- **.i2p.alt TLD-Registrierung** (RFC 9476, Ende 2023): Offizielle GANA-Registrierung von .i2p.alt als alternative TLD. Zukünftige router-Updates können das .alt-Suffix entfernen, aber Änderungen an Abonnementbefehlen sind nicht erforderlich.
- **Post-Quanten-Kryptografie** (2.10.0+): Verfügbar, aber nicht standardmäßig aktiviert. Künftige Berücksichtigung von Signaturalgorithmen in Abonnement-Feeds.
