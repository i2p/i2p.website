---
title: "Addressbook-Abonnement-Feed-Befehle"
description: "Spezifikation zur Erweiterung des Adressabonnement-Feeds mit Befehlen, um Name Servern zu ermöglichen, Eintragsänderungen von Hostname-Inhabern zu übertragen."
slug: "subscription"
aliases:
  - "/de/docs/specs/subscription-spec"
  - "/de/docs/specs/subscription-spec/"
category: "Formate"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Überblick

Diese Spezifikation erweitert den Adressabonnement-Feed mit Befehlen, um es Nameservern zu ermöglichen, Eintragsänderungen von Hostname-Inhabern zu übertragen. In Version 0.9.26 implementiert, ursprünglich in Vorschlag 112 vorgeschlagen.

## Motivation

Zuvor haben die hosts.txt-Abonnement-Server die Daten nur im hosts.txt-Format gesendet, welches wie folgt aussieht:

```
example.i2p=b64destination
```
Es gibt mehrere Probleme damit:

- Hostname-Inhaber können die mit ihren Hostnamen verknüpfte Destination nicht aktualisieren (um z.B. den Signaturschlüssel auf einen stärkeren Typ zu upgraden).
- Hostname-Inhaber können ihre Hostnamen nicht willkürlich aufgeben; sie müssen die entsprechenden privaten Destination-Schlüssel direkt an den neuen Inhaber weitergeben.
- Es gibt keine Möglichkeit zu authentifizieren, dass eine Subdomain von dem entsprechenden Basis-Hostnamen kontrolliert wird; dies wird derzeit nur individuell von einigen Nameservern durchgesetzt.

## Design

Diese Spezifikation fügt eine Anzahl von Befehlszeilen zum hosts.txt-Format hinzu. Mit diesen Befehlen können Name-Server ihre Dienste erweitern, um eine Reihe zusätzlicher Funktionen bereitzustellen. Clients, die diese Spezifikation implementieren, können über den regulären Abonnement-Prozess auf diese Funktionen zugreifen.

Alle Befehlszeilen müssen von der entsprechenden Destination signiert werden. Dies stellt sicher, dass Änderungen nur auf Anfrage des Hostname-Inhabers vorgenommen werden.

## Sicherheitsauswirkungen

Diese Spezifikation hat keinen Einfluss auf die Anonymität.

Es gibt ein erhöhtes Risiko, das mit dem Verlust der Kontrolle über einen Destination-Schlüssel verbunden ist, da jemand, der ihn erlangt, diese Befehle verwenden kann, um Änderungen an allen zugehörigen Hostnamen vorzunehmen. Dies ist jedoch nicht mehr ein Problem als der Status quo, bei dem jemand, der eine Destination erlangt, einen Hostnamen nachahmen und (teilweise) dessen Datenverkehr übernehmen kann. Das erhöhte Risiko wird auch dadurch ausgeglichen, dass Hostname-Inhabern die Möglichkeit gegeben wird, die mit einem Hostnamen verknüpfte Destination zu ändern, falls sie glauben, dass die Destination kompromittiert wurde; dies ist mit dem aktuellen System unmöglich.

## Spezifikation

### Neue Zeilentypen

Es gibt zwei neue Arten von Zeilen:

1. Add- und Change-Befehle:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Befehle entfernen:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Sortierung

Ein Feed ist nicht notwendigerweise in der richtigen Reihenfolge oder vollständig. Zum Beispiel kann ein Änderungsbefehl in einer Zeile vor einem Hinzufügungsbefehl stehen oder ohne einen Hinzufügungsbefehl.

Schlüssel können in beliebiger Reihenfolge stehen. Doppelte Schlüssel sind nicht erlaubt. Alle Schlüssel und Werte sind groß-/kleinschreibungsabhängig.

### Gemeinsame Schlüssel

Erforderlich in allen Befehlen:

**sig** : B64-Signatur, verwendet den Signaturschlüssel vom Ziel

Referenzen zu einem zweiten Hostnamen und/oder Ziel:

**oldname** : Ein zweiter Hostname (neu oder geändert)

**olddest** : Ein zweites b64-Ziel (neu oder geändert)

**oldsig** : Eine zweite b64-Signatur, die den Signierschlüssel von olddest verwendet

Andere häufige Schlüssel:

**action** : Ein Befehl

**name** : Der Hostname, nur vorhanden wenn nicht vorangestellt von `example.i2p=b64dest`

**dest** : Das b64-Ziel, nur vorhanden wenn nicht von `example.i2p=b64dest` vorangestellt

**date** : In Sekunden seit Epoch

**expires** : In Sekunden seit Epoch

### Befehle

Alle Befehle außer dem "Add"-Befehl müssen ein `action=command` Schlüssel/Wert-Paar enthalten.

Für die Kompatibilität mit älteren Clients werden die meisten Befehle von `example.i2p=b64dest` vorangestellt, wie unten vermerkt. Bei Änderungen sind dies immer die neuen Werte. Alle alten Werte sind im Schlüssel/Wert-Bereich enthalten.

Aufgelistete Schlüssel sind erforderlich. Alle Befehle können zusätzliche Schlüssel/Wert-Paare enthalten, die hier nicht definiert sind.

#### Hostname hinzufügen

**Vorangestellt von example.i2p=b64dest** : JA, dies ist der neue Hostname und das neue Ziel.

**action** : NICHT enthalten, ist impliziert.

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!sig=b64sig
```
#### Hostname ändern

**Vorangestellt von example.i2p=b64dest** : JA, dies ist der neue Hostname und das alte Ziel.

**action** : changename

**oldname** : der alte Hostname, der ersetzt werden soll

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Destination ändern

**Vorangestellt von example.i2p=b64dest** : JA, das ist der alte Hostname und das neue Ziel.

**action** : changedest

**olddest** : das alte Ziel, das ersetzt werden soll

**oldsig** : Signatur mit olddest

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Hostname-Alias hinzufügen

**Vorangestellt von example.i2p=b64dest** : JA, dies ist der neue (Alias) Hostname und das alte Ziel.

**action** : addname

**oldname** : der alte Hostname

**sig** : Signatur

Beispiel:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Ziel-Alias hinzufügen

(Wird für Krypto-Upgrade verwendet)

**Vorangestellt durch example.i2p=b64dest** : JA, dies ist der alte Hostname und das neue (alternative) Ziel.

**action** : adddest

**olddest** : das alte Ziel

**oldsig** : Signatur mit olddest

**sig** : Signatur mit dest

Beispiel:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Subdomain hinzufügen

**Vorangestellt durch subdomain.example.i2p=b64dest** : JA, dies ist der neue Host-Subdomain-Name und die Destination.

**action** : addsubdomain

**oldname** : der übergeordnete Hostname (example.i2p)

**olddest** : das höherstufige Ziel (zum Beispiel.i2p)

**oldsig** : Signatur mit olddest

**sig** : Signatur mit dest

Beispiel:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Metadaten aktualisieren

**Vorangestellt durch example.i2p=b64dest** : JA, das ist der alte Hostname und die alte Destination.

**action** : update

**sig** : Signatur

(fügen Sie hier alle aktualisierten Schlüssel hinzu)

Beispiel:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Hostname entfernen

**Vorangestellt durch example.i2p=b64dest** : NEIN, diese werden in den Optionen angegeben

**action** : remove

**name** : der Hostname

**dest** : das Ziel

**sig** : Signatur

Beispiel:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Alle mit diesem Ziel entfernen

**Vorangestellt durch example.i2p=b64dest** : NEIN, diese werden in den Optionen angegeben

**action** : removeall

**name** : der alte Hostname, nur informativ

**dest** : das alte dest, alle mit diesem dest werden entfernt

**sig** : Signatur

Beispiel:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Signaturen

Alle Befehle müssen ein Signatur-Schlüssel/Wert-Paar `sig=b64signature` enthalten, wobei die Signatur für die anderen Daten unter Verwendung des destination signing key erstellt wird.

Für Befehle, die ein altes und neues Ziel enthalten, muss es auch eine `oldsig=b64signature` geben und entweder oldname, olddest oder beides.

Bei einem Add- oder Change-Befehl befindet sich der öffentliche Schlüssel zur Verifikation in der Destination, die hinzugefügt oder geändert werden soll.

Bei einigen Hinzufügungs- oder Bearbeitungskommandos kann ein zusätzliches Ziel referenziert werden, beispielsweise beim Hinzufügen eines Alias oder beim Ändern eines Ziels oder Hostnamens. In diesem Fall muss eine zweite Signatur enthalten sein und beide sollten verifiziert werden. Die zweite Signatur ist die "innere" Signatur und wird zuerst signiert und verifiziert (unter Ausschluss der "äußeren" Signatur). Der Client sollte alle zusätzlichen Maßnahmen ergreifen, die notwendig sind, um Änderungen zu verifizieren und zu akzeptieren.

oldsig ist immer die "innere" Signatur. Signieren und verifizieren ohne die 'oldsig' oder 'sig' Schlüssel. sig ist immer die "äußere" Signatur. Signieren und verifizieren mit dem 'oldsig' Schlüssel vorhanden, aber nicht dem 'sig' Schlüssel.

#### Eingabe für Signaturen

Um einen Byte-Stream zur Erstellung oder Überprüfung der Signatur zu generieren, serialisieren Sie wie folgt:

- Entfernen Sie den "sig" Schlüssel
- Bei der Verifikation mit oldsig, entfernen Sie auch den "oldsig" Schlüssel
- Nur für Add- oder Change-Befehle, geben Sie `example.i2p=b64dest` aus
- Falls noch Schlüssel vorhanden sind, geben Sie `#!` aus
- Sortieren Sie die Optionen nach UTF-8 Schlüssel, fehlschlagen bei doppelten Schlüsseln
- Für jedes Schlüssel/Wert-Paar, geben Sie `key=value` aus, gefolgt von (falls nicht das letzte Schlüssel/Wert-Paar) einem `#`

Hinweise:

- Keine Zeilenumbruch ausgeben
- Ausgabekodierung ist UTF-8
- Alle Ziel- und Signaturkodierung erfolgt in Base 64 mit dem I2P-Alphabet
- Schlüssel und Werte sind groß-/kleinschreibungsempfindlich
- Hostnamen müssen in Kleinbuchstaben sein

## Kompatibilität

Alle neuen Zeilen im hosts.txt-Format werden mit führenden Kommentarzeichen implementiert, sodass alle älteren I2P-Versionen die neuen Befehle als Kommentare interpretieren.

Wenn I2P router auf die neue Spezifikation aktualisieren, werden sie alte Kommentare nicht neu interpretieren, sondern beginnen, auf neue Befehle in nachfolgenden Abrufen ihrer Abonnement-Feeds zu hören. Daher ist es wichtig, dass Namensserver Befehlseinträge in irgendeiner Form persistieren oder etag-Unterstützung aktivieren, damit router alle vergangenen Befehle abrufen können.
