---
title: "Adressbuch-Abonnement-Feed-Befehle"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Closed"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Hinweis
Netzwerkbereitstellung abgeschlossen.
Siehe [SPEC](/docs/specs/subscription/) für die offizielle Spezifikation.


## Übersicht

Dieser Vorschlag befasst sich mit der Erweiterung des Adressabonnement-Feeds um Befehle, um
Namensservern zu ermöglichen, Eintragsaktualisierungen von Hostnamen-Inhabern zu senden.
Implementiert in 0.9.26.


## Motivation

Derzeit senden die hosts.txt-Abonnementserver Daten im hosts.txt
Format, das wie folgt aussieht:

  ```text
  example.i2p=b64destination
  ```

Es gibt mehrere Probleme damit:

- Inhaber von Hostnamen können das mit ihren Hostnamen verbundene Ziel nicht aktualisieren
  (zum Beispiel, um den Signaturschlüssel auf einen stärkeren Typ zu aktualisieren).
- Inhaber von Hostnamen können ihre Hostnamen nicht willkürlich aufgeben; sie müssen die
  entsprechenden privaten Zielschlüssel direkt an den neuen Inhaber übergeben.
- Es gibt keine Möglichkeit zu authentifizieren, dass eine Subdomain von der
  entsprechenden Basis-Hostname kontrolliert wird; dies wird derzeit nur individuell von
  einigen Namensservern durchgesetzt.

## Design

Dieser Vorschlag fügt dem hosts.txt-Format eine Anzahl von Befehlszeilen hinzu. Mit diesen
Befehlen können Namensserver ihre Dienste erweitern, um eine Reihe von zusätzlichen
Funktionen bereitzustellen. Clients, die diesen Vorschlag implementieren, können
diese Funktionen durch den regulären Abonnementprozess empfangen.

Alle Befehlszeilen müssen von der entsprechenden Destination signiert sein. Dies stellt sicher,
dass Änderungen nur auf Wunsch des Hostnamen-Inhabers vorgenommen werden.

## Sicherheitsimplikationen

Dieser Vorschlag hat keine Auswirkungen auf die Anonymität.

Es gibt ein erhöhtes Risiko, die Kontrolle über einen Destinationsschlüssel zu verlieren, da
jemand, der ihn erhält, diese Befehle nutzen kann, um Änderungen an allen damit verbundenen
Hostnamen vorzunehmen. Aber dies ist kein größeres Problem als der Status quo, bei dem jemand,
der eine Destination erlangt, einen Hostnamen imitieren und (teilweise) dessen Verkehr übernehmen kann.
Das erhöhte Risiko wird auch ausgeglichen dadurch, dass Hostnamen-Inhaber die Möglichkeit haben,
die Destination zu ändern, die mit einem Hostnamen verbunden ist, für den Fall, dass sie glauben,
dass die Destination kompromittiert wurde; dies ist mit dem aktuellen System unmöglich.

## Spezifikation

### Neue Zeilentypen

Dieser Vorschlag fügt zwei neue Zeilentypen hinzu:

1. Hinzufügen und Ändern von Befehlen:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. Entfernen von Befehlen:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### Reihenfolge
Ein Feed ist nicht unbedingt in Reihenfolge oder vollständig. Zum Beispiel kann ein Änderungsbefehl
vor einem Hinzufügebefehl stehen oder ohne einen Hinzufügebefehl.

Schlüssel können in beliebiger Reihenfolge sein. Doppelte Schlüssel sind nicht erlaubt.
Alle Schlüssel und Werte sind groß- und kleinschreibungsempfindlich.

### Gemeinsame Schlüssel

Erforderlich in allen Befehlen:

sig
  B64-Signatur, die den Signaturschlüssel von der Destination benutzt

Referenzen zu einem zweiten Hostnamen und/oder einer Destination:

oldname
  Ein zweiter Hostname (neu oder geändert)
olddest
  Eine zweite b64-Destination (neu oder geändert)
oldsig
  Eine zweite b64-Signatur, die den Signaturschlüssel von nolddest benutzt

Andere häufige Schlüssel:

action
  Ein Befehl
name
  Der Hostname, nur vorhanden, wenn er nicht von example.i2p=b64dest vorangegangen ist
dest
  Die b64-Destination, nur vorhanden, wenn sie nicht von example.i2p=b64dest vorangegangen ist
date
  In Sekunden seit der Epoche
expires
  In Sekunden seit der Epoche

### Befehle

Alle Befehle außer dem "Hinzufügen"-Befehl müssen ein "action=command"
Schlüssel/Wert-Paar enthalten.

Zur Kompatibilität mit älteren Clients werden den meisten Befehlen von example.i2p=b64dest vorangestellt,
wie unten angegeben. Bei Änderungen sind dies immer die neuen Werte. Alle alten Werte
werden im Schlüssel/Wert-Bereich aufgenommen.

Aufgelistete Schlüssel sind erforderlich. Alle Befehle können zusätzliche Schlüssel/Wert-Paare enthalten,
die hier nicht definiert sind.

#### Hostname hinzufügen
Vorangegangen von example.i2p=b64dest
  JA, dies ist der neue Hostname und die Destination.
action
  NICHT enthalten, es wird impliziert.
sig
  Signatur

Beispiel:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Hostname ändern
Vorangegangen von example.i2p=b64dest
  JA, dies ist der neue Hostname und die alte Destination.
action
  changename
oldname
  der alte Hostname, der ersetzt werden soll
sig
  Signatur

Beispiel:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Destination ändern
Vorangegangen von example.i2p=b64dest
  JA, dies ist der alte Hostname und die neue Destination.
action
  changedest
olddest
  die alte Destination, die ersetzt werden soll
oldsig
  Signatur, die olddest benutzt
sig
  Signatur

Beispiel:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Hostname-Alias hinzufügen
Vorangegangen von example.i2p=b64dest
  JA, dies ist der neue (Alias-)Hostname und die alte Destination.
action
  addname
oldname
  der alte Hostname
sig
  Signatur

Beispiel:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Destination-Alias hinzufügen
(Wird für Kryptografie-Upgrade verwendet)

Vorangegangen von example.i2p=b64dest
  JA, dies ist der alte Hostname und die neue (alternative) Destination.
action
  adddest
olddest
  die alte Destination
oldsig
  Signatur, die olddest benutzt
sig
  Signatur, die dest benutzt

Beispiel:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Subdomain hinzufügen
Vorangegangen von subdomain.example.i2p=b64dest
  JA, dies ist der neue Host-Subdomain-Name und die Destination.
action
  addsubdomain
oldname
  der höhere Hostname (example.i2p)
olddest
  die höhere Destination (für example.i2p)
oldsig
  Signatur, die olddest benutzt
sig
  Signatur, die dest benutzt

Beispiel:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Metadaten aktualisieren
Vorangegangen von example.i2p=b64dest
  JA, dies ist der alte Hostname und die Destination.
action
  update
sig
  Signatur

(alle aktualisierten Schlüssel hier hinzufügen)

Beispiel:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Hostname entfernen
Vorangegangen von example.i2p=b64dest
  NEIN, diese sind in den Optionen angegeben
action
  remove
name
  der Hostname
dest
  die Destination
sig
  Signatur

Beispiel:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Alle mit dieser Destination entfernen
Vorangegangen von example.i2p=b64dest
  NEIN, diese sind in den Optionen angegeben
action
  removeall
name
  der alte Hostname, nur beratend
dest
  die alte Destination, alle mit dieser Destination werden entfernt
sig
  Signatur

Beispiel:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```


### Signaturen

Alle Befehle müssen einen Signaturschlüssel/Wert "sig=b64signature" enthalten, bei dem die
Signatur für die anderen Daten den Signaturschlüssel der Destination benutzt.

Für Befehle, die eine alte und neue Destination umfassen, muss auch ein
oldsig=b64signature vorhanden sein, und entweder oldname, olddest, oder beides.

Bei einem Hinzufügungs- oder Änderungsbefehl ist der öffentliche Schlüssel zur Verifikation in der
Destination enthalten, die hinzugefügt oder geändert werden soll.

In einigen Hinzufügungs- oder Bearbeitungsbefehlen kann es eine zusätzliche referenzierte Destination geben,
beispielsweise wenn ein Alias hinzugefügt wird oder eine Destination oder ein Hostname geändert wird. In
diesem Fall muss eine zweite Signatur enthalten sein und beide sollten verifiziert werden. Die zweite
Signatur ist die "innere" Signatur und wird zuerst signiert und verifiziert (ohne die "äußere" Signatur).
Der Client sollte alle zusätzlichen notwendigen Schritte unternehmen, um Änderungen zu verifizieren und
zu akzeptieren.

oldsig ist immer die "innere" Signatur. Signieren und Verifizieren ohne die 'oldsig'- oder
'sig'-Schlüssel. sig ist immer die "äußere" Signatur. Signieren und Verifizieren mit
dem 'oldsig'-Schlüssel vorhanden, aber nicht dem 'sig'-Schlüssel.

#### Eingabe für Signaturen
Um einen Byte-Stream zur Erstellung oder Verifikation der Signatur zu generieren, serialisieren Sie wie folgt:

- Entfernen Sie den "sig"-Schlüssel
- Wenn mit oldsig verifiziert wird, entfernen Sie auch den "oldsig"-Schlüssel
- Nur für Hinzufügungs- oder Änderungsbefehle,
  Ausgabe example.i2p=b64dest
- Wenn verbleibende Schlüssel vorhanden sind, Ausgabe "#!"
- Sortieren Sie die Optionen nach UTF-8-Key, scheitern Sie, wenn doppelte Schlüssel vorhanden sind
- Für jedes Schlüssel/Wert-Paar, Ausgabe key=value, gefolgt von (wenn nicht das letzte Schlüssel/Wert-Paar)
  einem '#'

Hinweise

- Keine neue Zeile ausgeben
- Ausgabe-Codierung ist UTF-8
- Alle Ziel- und Signaturcodierungen erfolgen in Base 64 unter Verwendung des I2P-Alphabets
- Schlüssel und Werte sind groß- und kleinschreibungsempfindlich
- Hostnamen müssen in Kleinbuchstaben sein


## Kompatibilität

Alle neuen Zeilen im hosts.txt-Format werden mit führenden Kommentarzeichen umgesetzt, sodass alle älteren I2P-Versionen
die neuen Befehle als Kommentare interpretieren.

Wenn I2P-Router auf die neue Spezifikation aktualisieren, werden alte Kommentare nicht neu interpretiert,
sondern beginnen, auf neue Befehle in nachfolgenden Abrufen ihrer Abonnement-Feeds zu hören.
Daher ist es wichtig, dass Namensserver Befehls-Einträge in irgendeiner Weise aufbewahren oder
etag-Unterstützung aktivieren, damit Router alle vergangenen Befehle abrufen können.


