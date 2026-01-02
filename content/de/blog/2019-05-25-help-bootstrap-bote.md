---
title: "Wie man sich freiwillig engagieren kann, indem man I2P‑Bote beim Bootstrapping unterstützt"
date: 2019-05-20
author: "idk"
description: "Hilf beim Bootstrapping von I2P-Bote!"
categories: ["development"]
---

Ein einfacher Weg, Menschen dabei zu helfen, sich gegenseitig privat Nachrichten zu schicken, besteht darin, einen I2P-Bote-Peer zu betreiben, der von neuen I2P-Bote-Nutzern verwendet werden kann, um ihre eigenen I2P-Bote-Peers zu bootstrappen (zu initialisieren). Leider war der Prozess zum Einrichten eines I2P-Bote-Bootstrap-Peers bislang deutlich weniger klar, als er sein sollte. Tatsächlich ist es extrem einfach!

**Was ist I2P-bote?**

I2P-bote ist ein privates Messaging-System, das auf i2p aufbaut und zusätzliche Funktionen bietet, die es noch schwieriger machen, Informationen über die übertragenen Nachrichten zu erkennen. Dadurch können private Nachrichten sicher übermittelt werden, wobei hohe Latenz toleriert wird und ohne dass man sich auf ein zentrales Relay (Weiterleitungsinstanz) verlassen muss, um Nachrichten zu senden, wenn der Absender offline geht. Dies steht im Gegensatz zu fast allen anderen verbreiteten privaten Messagingsystemen, die entweder erfordern, dass beide Gesprächspartner online sind, oder sich auf einen teilweise vertrauenswürdigen Dienst stützen, der Nachrichten im Namen von Absendern übermittelt, die offline gehen.

oder, ganz einfach erklärt: Es wird ähnlich wie E-Mail verwendet, weist jedoch keine der Datenschutzmängel von E-Mail auf.

**Schritt Eins: I2P-Bote installieren**

I2P-Bote ist ein I2P-Plugin, und die Installation ist sehr einfach. Die ursprünglichen Anleitungen sind auf der [bote eepSite, bote.i2p](http://bote.i2p/install/) verfügbar, aber wenn Sie sie im Clearnet lesen möchten, stammen diese Anleitungen mit freundlicher Genehmigung von bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Schritt zwei: Ermitteln Sie die Base64-Adresse Ihres I2P-Bote-Knotens**

Das ist der Punkt, an dem man leicht hängen bleiben kann – aber keine Sorge. Auch wenn Anleitungen dazu nicht leicht zu finden sind, ist das in Wirklichkeit einfach, und je nach Ihren Umständen stehen Ihnen mehrere Werkzeuge und Optionen zur Verfügung. Für Personen, die als Freiwillige Bootstrap-Knoten betreiben möchten, besteht der beste Weg darin, die erforderlichen Informationen aus der privaten Schlüsseldatei auszulesen, die vom bote tunnel verwendet wird.

**Wo sind die Schlüssel?**

I2P-Bote speichert seine destination keys (Zielschlüssel) in einer Textdatei, die unter Debian unter `/var/lib/i2p/i2p-config/i2pbote/local_dest.key` liegt. Auf Nicht-Debian-Systemen, auf denen i2p vom Benutzer installiert wurde, befindet sich der Schlüssel in `$HOME/.i2p/i2pbote/local_dest.key`, und unter Windows liegt die Datei in `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Methode A: Konvertieren Sie den Klartext-Schlüssel in die base64-Destination (Zieladresse)**

Um einen Klartext-Schlüssel in eine base64-Destination (Zieladresse) umzuwandeln, muss man den Schlüssel nehmen und daraus nur den Destination-Teil abtrennen. Um dies korrekt zu tun, muss man die folgenden Schritte durchführen:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Es gibt eine Reihe von Anwendungen und Skripten, die diese Schritte für Sie ausführen. Hier sind einige davon, aber die Liste ist bei weitem nicht vollständig:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Diese Funktionen sind auch in einer Reihe von Bibliotheken zur Entwicklung von I2P-Anwendungen verfügbar.

**Abkürzung:**


Da die lokale destination (Zieladresse) Ihres Bote-Knotens eine DSA destination ist, ist es schneller, die Datei local_dest.key einfach auf die ersten 516 Bytes zu kürzen. Um das einfach zu erledigen, führen Sie diesen Befehl aus, wenn Sie I2P-Bote mit I2P unter Debian ausführen:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Oder, wenn I2P für Ihr Benutzerkonto installiert ist:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Methode B: Eine Abfrage durchführen**

Falls Ihnen das zu viel Aufwand erscheint, können Sie die Base64-Destination (Zieladresse) Ihrer Bote-Verbindung ermitteln, indem Sie deren Base32-Adresse mit einer der verfügbaren Methoden zum Nachschlagen einer Base32-Adresse abfragen. Die Base32-Adresse Ihres Bote-Knotens finden Sie auf der Seite "Connection" der Bote-Plugin-Anwendung unter [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Schritt drei: Kontaktieren Sie uns!**

**Aktualisieren Sie die Datei built-in-peers.txt mit Ihrem neuen Knoten**

Jetzt, da Sie die korrekte Destination (Zieladresse) für Ihren I2P-Bote-Knoten haben, besteht der letzte Schritt darin, sich selbst zur Standard-Peer-Liste für [I2P-Bote hier](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) hier hinzuzufügen. Das können Sie tun, indem Sie das Repository forken, sich mit auskommentiertem Namen in die Liste eintragen und Ihre 516‑Zeichen-Destination direkt darunter hinzufügen, etwa so:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
und einen Pull Request einzureichen. Das ist alles; hilf also mit, i2p lebendig, dezentral und zuverlässig zu halten.
