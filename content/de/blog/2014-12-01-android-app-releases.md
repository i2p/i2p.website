---
title: "Veröffentlichungen der Android-App"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 und Bote 0.3 wurden auf der Website, bei Google Play und F-Droid veröffentlicht."
categories: ["press"]
---

Es ist schon einige Zeit her, dass ich zuletzt Updates zu unserer Android-Entwicklung veröffentlicht habe, und in der Zwischenzeit gab es mehrere I2P-Veröffentlichungen, ohne dass entsprechende Android-Veröffentlichungen erschienen. Endlich ist das Warten vorbei!

## Neue App-Versionen

Neue Versionen von I2P Android und Bote wurden veröffentlicht! Sie können von diesen URLs heruntergeladen werden:

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

Die wichtigste Änderung in diesen Releases ist die Umstellung auf Androids neues Material Design-System. Material hat es App-Entwicklern mit, sagen wir mal, "minimalistischen" Design-Fähigkeiten (so wie ich) wesentlich erleichtert, Apps zu erstellen, die sich angenehmer nutzen lassen. I2P Android aktualisiert außerdem seinen zugrunde liegenden I2P router auf die soeben veröffentlichte Version 0.9.17. Bote bringt mehrere neue Funktionen sowie viele kleinere Verbesserungen mit; zum Beispiel können Sie jetzt neue E-Mail-Zieladressen per QR-Codes hinzufügen.

Wie ich in meinem letzten Update erwähnt habe, hat sich der Signaturschlüssel, der zum Signieren der Apps verwendet wird, geändert. Der Grund dafür war, dass wir den Paketnamen von I2P Android ändern mussten. Der alte Paketname (`net.i2p.android.router`) war auf Google Play bereits vergeben (wir wissen bis heute nicht, wer ihn verwendet hat), und wir wollten für alle Distributionen von I2P Android denselben Paketnamen und denselben Signaturschlüssel verwenden. Auf diese Weise kann ein Nutzer die App zunächst von der I2P-Website installieren und sie später, falls die Website blockiert ist, über Google Play aktualisieren. Das Android-Betriebssystem betrachtet eine Anwendung als völlig unterschiedlich, wenn sich ihr Paketname ändert; daher haben wir die Gelegenheit genutzt, die Stärke des Signaturschlüssels zu erhöhen.

Der Fingerabdruck (SHA-256) des neuen Signaturschlüssels lautet:

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

Vor einigen Monaten haben wir sowohl I2P Android als auch Bote im Google Play Store in Norwegen veröffentlicht, um den Veröffentlichungsprozess dort zu testen. Wir freuen uns, bekanntzugeben, dass beide Apps nun weltweit von [Privacy Solutions](https://privacysolutions.no/) veröffentlicht werden. Die Apps sind unter diesen URLs zu finden:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

Die globale Veröffentlichung erfolgt in mehreren Phasen, beginnend mit den Ländern, für die wir Übersetzungen haben. Die bemerkenswerte Ausnahme hiervon ist Frankreich; aufgrund von Importvorschriften für kryptografischen Code können wir diese Apps auf Google Play Frankreich noch nicht anbieten. Dies ist dasselbe Problem, das auch andere Apps wie TextSecure und Orbot betroffen hat.

## F-Droid

Keine Sorge, F-Droid-Nutzer: Wir haben Sie nicht vergessen! Zusätzlich zu den beiden oben genannten Stellen haben wir ein eigenes F-Droid-Repository eingerichtet. Wenn Sie diesen Beitrag auf Ihrem Smartphone lesen, [klicken Sie hier](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6), um es zu F-Droid hinzuzufügen (das funktioniert nur in einigen Android-Browsern). Oder Sie können die untenstehende URL manuell zu Ihrer F-Droid-Repository-Liste hinzufügen:

https://f-droid.i2p.io/repo

Wenn Sie den Fingerabdruck (SHA-256) des Repository-Signaturschlüssels manuell überprüfen oder ihn beim Hinzufügen des Repositories eingeben möchten, hier ist er:

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
Leider wurde die I2P-App im Haupt-Repository von F-Droid nicht aktualisiert, weil unser F-Droid-Maintainer nicht mehr erreichbar ist. Wir hoffen, dass wir durch den Betrieb dieses Binär-Repositorys unsere F-Droid-Nutzer besser unterstützen und sie auf dem neuesten Stand halten können. Wenn Sie I2P bereits aus dem Haupt-Repository von F-Droid installiert haben, müssen Sie es deinstallieren, wenn Sie aktualisieren möchten, da der Signaturschlüssel ein anderer ist. Die Apps in unserem F-Droid-Repository sind dieselben APKs, die auf unserer Website und bei Google Play bereitgestellt werden, sodass Sie künftig über jede dieser Quellen aktualisieren können.
