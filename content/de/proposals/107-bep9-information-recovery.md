---
title: "BEP9 Informationswiederherstellung"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Dead"
thread: "http://zzz.i2p/topics/860"
---

## Übersicht

Dieser Vorschlag bezieht sich auf das Hinzufügen einer vollständigen Informationswiederherstellung zur I2P-Implementierung von BEP9.


## Motivation

BEP9 sendet nicht die gesamte Torrent-Datei, sodass mehrere wichtige
Dictionary-Einträge verloren gehen, und ändert den gesamten SHA1-Wert der Torrent-Dateien. Dies ist schlecht für Maggot-Links und schlecht, da wichtige Informationen verloren gehen. Tracker-Listen, Kommentare und alle zusätzlichen Daten sind weg. Eine Möglichkeit, diese Informationen wiederherzustellen, ist wichtig, und es muss so wenig wie möglich zur Torrent-Datei hinzugefügt werden. Außerdem darf es nicht zirkulär abhängig sein. Wiederherstellungsinformationen sollten aktuelle Clients in keiner Weise beeinflussen. Torrents ohne Tracker (Tracker-URL ist buchstäblich 'trackerless') enthalten das zusätzliche Feld nicht, da sie spezifisch für die Verwendung des Maggot-Protokolls zur Entdeckung und zum Herunterladen sind, bei dem die Informationen von vornherein nicht verloren gehen.


## Lösung

Alles, was getan werden muss, ist, die Informationen, die verloren gehen würden, zu komprimieren und im Info-Dictionary zu speichern.


### Implementierung
1. Erstellen Sie das normale Info-Dictionary.
2. Erstellen Sie das Haupt-Dictionary und lassen Sie den Info-Eintrag weg.
3. Bencodieren und komprimieren Sie das Haupt-Dictionary mit gzip.
4. Fügen Sie das komprimierte Haupt-Dictionary dem Info-Dictionary hinzu.
5. Fügen Sie Info zum Haupt-Dictionary hinzu.
6. Schreiben Sie die Torrent-Datei

### Wiederherstellung
1. Dekomprimieren Sie den Wiederherstellungseintrag im Info-Dictionary.
2. Bendumcode den Wiederherstellungseintrag.
3. Fügen Sie Info dem wiederhergestellten Dictionary hinzu.
4. Für Maggot-bewusste Clients können Sie nun überprüfen, ob der SHA1 korrekt ist.
5. Schreiben Sie die wiederhergestellte Torrent-Datei.


## Diskussion

Mit der oben beschriebenen Methode ist die Größe der Torrent-Erhöhung sehr klein, 200 bis 500 Bytes sind typisch. Robert wird mit der neuen Info-Dictionary-Eintragserstellung ausgeliefert, und sie kann nicht deaktiviert werden. Hier ist die Struktur:

```
main dict {
    Tracker-Strings, Kommentare, etc...
    info : {
        gzipped Haupt bencodiertes Dict minus des Info-Dictionarys und aller anderen
        üblichen Infos
    }
}
```
