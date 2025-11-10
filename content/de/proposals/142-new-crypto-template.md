---
title: "Neuer Verschlüsselungsvorschlags-Template"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
---

## Übersicht

Dieses Dokument beschreibt wichtige Fragen, die bei der Vorlage eines Ersatzes oder einer Ergänzung zu unserer elGamal-asymmetrischen Verschlüsselung berücksichtigt werden müssen.

Dies ist ein Informationsdokument.

## Motivation

ElGamal ist alt und langsam, und es gibt bessere Alternativen. Es gibt jedoch mehrere Probleme, die gelöst werden müssen, bevor wir einen neuen Algorithmus hinzufügen oder wechseln können. Dieses Dokument hebt diese ungelösten Probleme hervor.

## Hintergrundforschung

Jeder, der neue Kryptographie vorschlägt, muss zuerst mit den folgenden Dokumenten vertraut sein:

- Vorschlag 111 NTCP2 /proposals/111-ntcp-2/
- Vorschlag 123 LS2 /proposals/123-new-netdb-entries/
- Vorschlag 136 experimentelle Sig-Typen /proposals/136-experimental-sigtypes/
- Vorschlag 137 optionale Sig-Typen /proposals/137-optional-sigtypes/
- Diskussionsfäden hier für jeden der obigen Vorschläge, innerhalb verlinkt
- http://zzz.i2p/topics/2494 Prioritäten für Vorschläge 2018
- http://zzz.i2p/topics/2418 ECIES-Vorschlag
- http://zzz.i2p/topics/1768 Übersicht über neue asymmetrische Kryptographie
- Niedrig-Level-Krypto-Übersicht /docs/specs/cryptography/

## Verwendung der asymmetrischen Kryptographie

Zur Überprüfung verwenden wir ElGamal für:

1) Tunnelaufbaunachrichten (Schlüssel befindet sich in RouterIdentity)

2) Router-zu-Router-Verschlüsselung von netdb und anderen I2NP-Nachrichten (Schlüssel befindet sich in RouterIdentity)

3) Client End-to-End ElGamal+AES/SessionTag (Schlüssel befindet sich im LeaseSet, der Zielschlüssel wird nicht verwendet)

4) Vergängliches DH für NTCP und SSU

## Design

Jeder Vorschlag zum Ersetzen von ElGamal durch etwas anderes muss die folgenden Details angeben.

## Spezifikation

Jeder Vorschlag für neue asymmetrische Kryptographie muss die folgenden Dinge vollständig spezifizieren.

### 1. Allgemein

Beantworten Sie die folgenden Fragen in Ihrem Vorschlag. Beachten Sie, dass dies ein separater Vorschlag zu den Details in 2) unten sein kann, da es mit bestehenden Vorschlägen 111, 123, 136, 137 oder anderen konfligieren könnte.

- Für welche der oben genannten Fälle 1-4 schlagen Sie vor, die neue Kryptographie zu verwenden?
- Wenn für 1) oder 2) (Router), Wo soll der öffentliche Schlüssel platziert werden, in den RouterIdentity oder den RouterInfo-Props? Beabsichtigen Sie, den Kryptotyp im Schlüsselzertifikat zu verwenden? Komplett spezifizieren. Begründen Sie Ihre Entscheidung in beiden Fällen.
- Wenn für 3) (Client), beabsichtigen Sie, den öffentlichen Schlüssel im Ziel zu speichern und den Kryptotyp im Schlüsselzertifikat zu verwenden (wie im ECIES-Vorschlag), oder ihn in LS2 zu speichern (wie im Vorschlag 123), oder etwas anderes? Komplett spezifizieren und Ihre Entscheidung begründen.
- Für alle Anwendungen, wie wird die Unterstützung angekündigt? Wenn für 3), geht es in die LS2, oder irgendwo anders? Wenn für 1) und 2), ist es ähnlich zu den Vorschlägen 136 und/oder 137? Komplett spezifizieren und Ihre Entscheidungen begründen. Wahrscheinlich wird ein separater Vorschlag dafür benötigt.
- Komplett spezifizieren, wie und warum dies rückwärtskompatibel ist, und komplett einen Migrationsplan spezifizieren.
- Welche nicht implementierten Vorschläge sind Voraussetzungen für Ihren Vorschlag?

### 2. Spezifischer Kryptotyp

Beantworten Sie die folgenden Fragen in Ihrem Vorschlag:

- Allgemeine Kryptoinformationen, spezifische Kurven/Parameter, komplett Ihre Wahl begründen. Links zu Spezifikationen und anderen Informationen bereitstellen.
- Geschwindigkeitstestergebnisse im Vergleich zu ElG und anderen Alternativen, falls zutreffend. Verschlüsselung, Entschlüsselung und Schlüsselerzeugung einbeziehen.
- Verfügbarkeit von Bibliotheken in C++ und Java (sowohl OpenJDK, BouncyCastle als auch Drittanbieter)
  Für Drittanbieter oder nicht-Java, Links und Lizenzen bereitstellen
- Vorgeschlagene Krypto-Typnummer(n) (experimenteller Bereich oder nicht)

## Anmerkungen

