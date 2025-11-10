---
title: "I2P Vorschlag #165: SSU2 Fix"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Offen"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Vorschlag von weko, orignal, the Anonymous und zzz.


### Überblick

Dieses Dokument schlägt Änderungen an SSU2 vor, nachdem ein Angriff auf I2P Schwachstellen in SSU2 ausnutzte. Das primäre Ziel ist die Erhöhung der Sicherheit und die Verhinderung von Distributed Denial of Service (DDoS) Angriffen und Versuchen der Deanonymisierung.

### Bedrohungsmodell

Ein Angreifer erstellt neue gefälschte RIs (Router existiert nicht): ist reguläres RI,
aber er verwendet Adresse, Port, s und i Schlüssel vom echten Bob's Router, dann
überflutet er das Netzwerk. Wenn wir versuchen, uns mit diesem (wie wir denken echten) Router zu verbinden, können wir als Alice diese Adresse verbinden, aber wir können nicht sicher sein, dass dies mit Bob's echtem RI geschah. Dies ist möglich und wurde für einen Distributed Denial of Service Angriff verwendet (große Menge solcher RIs erzeugen und das Netzwerk überfluten), auch kann dies Deanon-Angriffe erleichtern, indem gute Router manipuliert und Angreifer-Router nicht manipuliert werden, wenn wir IPs mit vielen RIs verbieten (anstatt besser den Tunnel-Aufbau auf diese RIs als zu einem Router zu verteilen).


### Mögliche Lösungen

#### 1. Fix mit Unterstützung für alte (vor der Änderung) Router

.. _overview-1:

Überblick
^^^^^^^^^

Ein Workaround, um SSU2-Verbindungen mit alten Routern zu unterstützen.

Verhalten
^^^^^^^^^

Bob's Routerprofil sollte ein 'verifiziert' Flag haben, das standardmäßig
für alle neuen Router (die noch kein Profil haben) auf false gesetzt ist. Wenn das 'verifiziert' Flag
false ist, führen wir niemals Verbindungen mit SSU2 von Alice zu Bob aus - wir können uns nicht sicher sein im RI. Wenn Bob sich mit uns (Alice) mit NTCP2 oder SSU2 verbunden hat oder wir (Alice) sich einmal mit NTCP2 mit Bob verbunden haben (wir können Bob's RouterIdent in diesen Fällen verifizieren) - wird das Flag auf true gesetzt.

Probleme
^^^^^^^^

Es gibt also ein Problem mit gefälschten SSU2-only RI-Fluten: wir können es nicht selbst verifizieren und müssen warten, bis der echte Router Verbindungen mit uns herstellt.

#### 2. RouterIdent während der Verbindungserstellung verifizieren

.. _overview-2:

Überblick
^^^^^^^^^

Fügen Sie einen “RouterIdent” Block für SessionRequest und SessionCreated hinzu.

Mögliches Format des RouterIdent Blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 Byte Flags, 32 Bytes RouterIdent. Flag_0: 0 wenn Empfänger's RouterIdent;
1 wenn Absender's RouterIdent

Verhalten
^^^^^^^^^

Alice (sollte(1), kann(2)) sendet im Payload RouterIdent Block Flag_0 = 0
und Bobs RouterIdent. Bob (sollte(3), kann(4)) überprüft, ob es sich um seinen
RouterIdent handelt, und wenn nicht: Terminiert die Sitzung mit dem Grund "Falscher RouterIdent", wenn es sein RouterIdent ist: sendet RI Block mit 1 in Flag_0 und Bobs RouterIdent.

Mit (1) unterstützt Bob keine alten Router. Mit (2) unterstützt Bob alte
Router, kann jedoch ein Opfer von DDoS von Routern werden, die versuchen, eine Verbindung mit gefälschten RIs herzustellen. Mit (3) unterstützt Alice keine alten Router. Mit (4) unterstützt Alice alte Router und verwendet ein hybrides
Schema: Fix 1 für alte Router und Fix 2 für neue Router. Wenn RI neue
Version sagt, aber während der Verbindung nicht der RouterIdent Block empfangen wurde - beenden und RI entfernen.

.. _problems-1:

Probleme
^^^^^^^^

Ein Angreifer kann seine gefälschten Router als alt tarnen, und mit (4) warten wir sowieso auf 'verifiziert' wie in Fix 1.

Notizen
^^^^^

Statt eines 32-Byte RouterIdent könnten wir wahrscheinlich einen 4-Byte
siphash-of-the-hash, ein HKDF oder etwas anderes verwenden, das ausreichend sein müsste.

#### 3. Bob setzt i = RouterIdent

.. _overview-3:

Überblick
^^^^^^^^^

Bob verwendet seinen RouterIdent als i-Schlüssel.

.. _behavior-1:

Verhalten
^^^^^^^^^

Bob (sollte(1), kann(2)) verwendet seinen eigenen RouterIdent als i-Schlüssel für SSU2.

Alice mit (1) verbindet sich nur, wenn i = Bobs RouterIdent. Alice mit (2)
verwendet das hybride Schema (Fix 3 und 1): wenn i = Bobs RouterIdent, können wir
eine Verbindung herstellen, ansonsten sollten wir es zuerst verifizieren (siehe Fix 1).

Mit (1) unterstützt Alice keine alten Router. Mit (2) unterstützt Alice alte Router.

.. _problems-2:

Probleme
^^^^^^^^

Ein Angreifer kann seine gefälschten Router als alt tarnen, und mit (2) warten wir sowieso auf 'verifiziert' wie in Fix 1.

.. _notes-1:

Notizen
^^^^^

Um die RI-Größe zu sparen, besser eine Handhabung hinzufügen, wenn i-Schlüssel nicht angegeben ist. Wenn es
ist, dann i = RouterIdent. In diesem Fall unterstützt Bob keine alten Router.

#### 4. Fügen Sie einen weiteren MixHash zu KDF von SessionRequest hinzu

.. _overview-4:

Überblick
^^^^^^^^^

Fügen Sie MixHash(Bob's ident hash) zum NOISE-State der "SessionRequest" Nachricht hinzu, z.B.
h = SHA256 (h || Bob's ident hash).
Es muss der letzte MixHash sein, der als ad für ENCRYPT oder DECRYPT verwendet wird.
Zusätzlicher SSU2-Header-Flag "Verifiziert Bob's ident" = 0x02 muss eingeführt werden.

.. _behavior-4:

Verhalten
^^^^^^^^^

- Alice fügt MixHash mit Bob's ident hash aus Bob's RouterInfo hinzu und verwendet es als ad für ENCRYPT und setzt den "Verifiziert Bob's ident" Flag
- Bob überprüft den "Verifiziert Bob's ident" Flag und fügt MixHash mit eigenem ident hash hinzu und verwendet es als ad für DECRYPT. Wenn AEAD/Chacha20/Poly1305 fehlschlägt, schließt Bob die Sitzung.

Kompatibilität mit älteren Routern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice muss die Routerversion von Bob überprüfen und wenn sie die minimale Version erfüllt, die diesen Vorschlag unterstützt, diesen MixHash hinzufügen und den "Verifiziert Bob's ident" Flag setzen. Wenn der Router älter ist, fügt Alice keinen MixHash hinzu und setzt nicht den "Verifiziert Bob's ident" Flag.
- Bob überprüft den "Verifiziert Bob's ident" Flag und fügt diesen MixHash hinzu, wenn er gesetzt ist. Ältere Router setzen diesen Flag nicht und dieser MixHash sollte nicht hinzugefügt werden.

.. _problems-4:

Probleme
^^^^^^^^

- Ein Angreifer kann gefälschte Router mit älterer Version beanspruchen. Irgendwann sollten ältere Router mit Vorsicht verwendet werden und nachdem sie auf andere Weise verifiziert wurden.


### Rückwärtskompatibilität

In den Fixes beschrieben.


### Aktueller Status

i2pd: Fix 1.
