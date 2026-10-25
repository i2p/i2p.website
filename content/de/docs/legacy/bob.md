---
title: "BOB - Basic Open Bridge"
description: "Veraltete API für Destination-Verwaltung"
slug: "bob"
aliases:
  - "/de/docs/api/bob"
  - "/de/docs/api/bob/"
  - "/de/bob"
  - "/de/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Warnung - Veraltet

Nicht für neue Anwendungen geeignet. BOB, wie hier spezifiziert, unterstützt nur den DSA-SHA1 Signaturtyp. BOB wird nicht erweitert, um neue Signaturtypen oder andere erweiterte Funktionen zu unterstützen. Neue Anwendungen sollten [SAMv3](/docs/api/samv3) verwenden.

BOB-Unterstützung wurde ab Release 1.7.0 (2022-02) aus neuen Java I2P-Installationen entfernt. Es funktioniert weiterhin in Java I2P, das ursprünglich als Version 1.6.1 oder früher installiert wurde, auch nach Updates, aber es wird nicht unterstützt und kann jederzeit nicht mehr funktionieren. BOB wird ab 2025-05 weiterhin von i2pd unterstützt, aber Anwendungen sollten dennoch aus den oben genannten Gründen zu SAMv3 migrieren. Siehe [die i2pd-Dokumentation](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) für alle Erweiterungen der hier dokumentierten API, die von i2pd unterstützt werden.

Zu diesem Zeitpunkt wurden die meisten guten Ideen von BOB in SAMv3 integriert, das mehr Funktionen und eine breitere praktische Anwendung bietet. BOB funktioniert möglicherweise noch bei einigen Installationen (siehe oben), erhält jedoch nicht die erweiterten Funktionen, die für SAMv3 verfügbar sind, und wird im Wesentlichen nicht mehr unterstützt, außer von i2pd.

## Sprachbibliotheken für die BOB-API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Überblick

`KEYS` = Schlüsselpaar öffentlich+privat, diese sind BASE64

`KEY` = öffentlicher Schlüssel, ebenfalls BASE64

`ERROR` gibt wie impliziert die Nachricht `"ERROR "+DESCRIPTION+"\n"` zurück, wobei die `DESCRIPTION` angibt, was schief gelaufen ist.

`OK` gibt `"OK"` zurück, und falls Daten zurückgegeben werden sollen, stehen sie in derselben Zeile. `OK` bedeutet, dass der Befehl abgeschlossen ist.

`DATA`-Zeilen enthalten Informationen, die Sie angefordert haben. Es kann mehrere `DATA`-Zeilen pro Anfrage geben.

**HINWEIS:** Der help-Befehl ist der EINZIGE Befehl, der eine Ausnahme von den Regeln hat... er kann tatsächlich nichts zurückgeben! Dies ist beabsichtigt, da help ein HUMAN- und kein APPLICATION-Befehl ist.

## Verbindung und Version

Alle BOB-Statusausgaben erfolgen zeilenweise. Zeilen können je nach System mit \\n oder \\r\\n beendet werden. Bei der Verbindung gibt BOB zwei Zeilen aus:

```
BOB version
OK
```
Die aktuelle Version ist: 00.00.10

Beachten Sie, dass frühere Versionen Großbuchstaben-Hexadezimalziffern verwendeten und nicht den I2P-Versionierungsstandards entsprachen. Es wird empfohlen, dass nachfolgende Versionen nur die Ziffern 0-9 verwenden.

### Versionshistorie

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Befehle

**BITTE BEACHTEN:** Für AKTUELLE Details zu den Befehlen verwenden Sie BITTE den eingebauten Hilfe-Befehl. Verbinden Sie sich einfach per Telnet mit localhost 2827 und geben Sie help ein, um eine vollständige Dokumentation zu jedem Befehl zu erhalten.

Befehle werden niemals obsolet oder geändert, jedoch werden von Zeit zu Zeit neue Befehle hinzugefügt.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Einmal eingerichtet, können und werden alle TCP-Sockets bei Bedarf blockieren, und es sind keine zusätzlichen Nachrichten zum/vom Kommandokanal erforderlich. Dies ermöglicht es dem Router, den Stream zu steuern, ohne mit OOM-Fehlern (Out of Memory) zu explodieren, wie es bei SAM passiert, wenn es daran scheitert, viele Streams über einen Socket hinein- oder herauszupressen -- das kann nicht skalieren, wenn man viele Verbindungen hat!

Was an dieser speziellen Schnittstelle auch schön ist, ist dass das Schreiben von allem zur Schnittstellenanbindung viel, viel einfacher ist als bei SAM. Nach der Einrichtung ist keine weitere Verarbeitung erforderlich. Die Konfiguration ist so einfach, dass sehr einfache Werkzeuge wie nc (netcat) verwendet werden können, um auf eine Anwendung zu verweisen. Der Wert liegt darin, dass man Betriebszeiten für eine Anwendung planen kann, ohne die Anwendung dafür ändern oder sie überhaupt stoppen zu müssen. Stattdessen kann man das Ziel buchstäblich "ausstecken" und wieder "einstecken". Solange dieselben IP/Port-Adressen und Zielschlüssel beim Hochfahren der Brücke verwendet werden, wird es die normale TCP-Anwendung nicht kümmern und sie wird es nicht bemerken. Sie wird einfach getäuscht -- die Ziele sind nicht erreichbar und nichts kommt herein.

## Beispiele

Für das folgende Beispiel richten wir eine sehr einfache lokale Loopback-Verbindung mit zwei destinations ein. Destination "mouth" wird der CHARGEN-Dienst vom INET-Superserver-Daemon sein. Destination "ear" wird ein lokaler Port sein, zu dem Sie sich per Telnet verbinden können, um das hübsche ASCII-Test-Gekritzel zu beobachten.

### Beispiel-Sitzungsdialog

Einfaches telnet 127.0.0.1 2827 funktioniert.

- A = Anwendung
- C = BOBs Befehlsantwort.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**NOTIEREN SIE SICH DEN OBIGEN DESTINATION KEY, IHRER WIRD ANDERS SEIN!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
An diesem Punkt gab es keinen Fehler, eine Destination mit dem Nickname "mouth" ist eingerichtet. Wenn Sie die bereitgestellte Destination kontaktieren, verbinden Sie sich tatsächlich mit dem `CHARGEN`-Dienst auf `19/TCP`.

Nun zur anderen Hälfte, damit wir dieses Ziel tatsächlich kontaktieren können.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Jetzt müssen wir nur noch eine Telnet-Verbindung zu 127.0.0.1, Port 37337, herstellen und den Zielschlüssel oder die Host-Adresse aus dem Adressbuch senden, mit dem wir uns verbinden möchten. In diesem Fall wollen wir uns mit "mouth" verbinden, wir fügen einfach den Schlüssel ein und es funktioniert.

**HINWEIS:** Der "quit"-Befehl im Befehlskanal trennt die tunnel NICHT wie bei SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Nach ein paar virtuellen Meilen dieser Ausgabe drücken Sie `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Folgendes ist passiert...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Du kannst auch zu I2P SITES eine Verbindung herstellen!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Ziemlich cool, nicht wahr? Probieren Sie gerne einige andere bekannte I2P SITES aus, nicht existierende, etc., um ein Gefühl dafür zu bekommen, welche Art von Ausgabe in verschiedenen Situationen zu erwarten ist. Größtenteils wird empfohlen, alle Fehlermeldungen zu ignorieren. Sie wären für die Anwendung bedeutungslos und werden nur für menschliches Debugging präsentiert.

### Aufräumen

Lassen Sie uns nun unsere Ziele herunterfahren, da wir mit ihnen fertig sind.

Zuerst schauen wir uns an, welche Ziel-Nicknamen wir haben.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Gut, da sind sie. Entfernen wir zuerst "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Um nun "ear" zu entfernen, beachte, dass dies passiert, wenn du zu schnell tippst, und zeigt dir, wie typische FEHLER-Meldungen aussehen.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Ruhemodus

Ich werde mich nicht damit aufhalten, ein Beispiel für das Empfänger-Ende einer Bridge zu zeigen, da es sehr einfach ist. Es gibt zwei mögliche Einstellungen dafür, und es wird mit dem "quiet"-Befehl umgeschaltet.

Die Standardeinstellung ist NICHT quiet, und die ersten Daten, die in Ihren lauschenden Socket eingehen, sind die destination, die den Kontakt aufnimmt. Es handelt sich um eine einzelne Zeile, die aus der BASE64-Adresse gefolgt von einem Zeilenwechsel besteht. Alles danach ist für die tatsächliche Verarbeitung durch die Anwendung bestimmt.

Im Ruhemodus können Sie sich das wie eine normale Internetverbindung vorstellen. Es kommen überhaupt keine zusätzlichen Daten herein. Es ist genau so, als wären Sie einfach mit dem normalen Internet verbunden. Dieser Modus ermöglicht eine Form der Transparenz, ähnlich der, die auf den tunnel-Einstellungsseiten der router-Konsole verfügbar ist, sodass Sie BOB verwenden können, um eine Destination auf einen Webserver zu richten, beispielsweise, ohne den Webserver überhaupt modifizieren zu müssen.

## Vorteile von BOB

Der Vorteil bei der Verwendung von BOB hierfür ist wie zuvor besprochen. Sie könnten zufällige Betriebszeiten für die Anwendung planen, auf eine andere Maschine umleiten, etc. Eine Verwendung hierfür könnte beispielsweise sein, dass Sie versuchen möchten, das Erraten der router-zu-destination Verfügbarkeit zu erschweren. Sie könnten die destination mit einem völlig anderen Prozess stoppen und starten, um zufällige Verfügbarkeits- und Ausfallzeiten bei Diensten zu erzeugen. Auf diese Weise würden Sie nur die Möglichkeit stoppen, einen solchen Dienst zu kontaktieren, und müssten sich nicht darum kümmern, ihn herunterzufahren und neu zu starten. Sie könnten umleiten und auf eine andere Maschine in Ihrem LAN zeigen, während Sie Updates durchführen, oder je nach dem, was läuft, auf eine Reihe von Backup-Maschinen zeigen, etc, etc. Nur Ihre Fantasie begrenzt, was Sie mit BOB machen könnten.
