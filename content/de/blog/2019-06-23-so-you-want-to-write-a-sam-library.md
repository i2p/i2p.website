---
title: "Sie möchten also eine SAM-Bibliothek schreiben"
date: 2019-06-23
author: "idk"
description: "Einsteigerleitfaden zum Schreiben einer SAM-Bibliothek!"
---

*Oder, wie man mit [i2p](https://geti2p.net) spricht, für Leute, die nicht wirklich daran gewöhnt sind, Spezifikationen zu lesen*

Meiner Meinung nach gehört die SAM API zu den besten Funktionen von I2P, da sie verwendet werden kann, um eine Brücke zwischen I2P und Ihrer Anwendung oder der Programmiersprache Ihrer Wahl zu bauen. Derzeit existieren Dutzende von SAM-Bibliotheken für eine Vielzahl von Programmiersprachen, darunter:

- [i2psam, for c++](https://github.com/i2p/i2psam)
- [libsam3, for C](https://github.com/i2p/libsam3)
- [txi2p for Python](https://github.com/str4d/txi2p)
- [i2plib for Python](https://github.com/l-n-s/i2plib)
- [i2p.socket for Python](https://github.com/majestrate/i2p.socket)
- [leaflet for Python](https://github.com/MuxZeroNet/leaflet)
- [gosam, for Go](https://github.com/eyedeekay/gosam)
- [sam3 for Go](https://github.com/eyedeekay/sam3)
- [node-i2p for nodejs](https://github.com/redhog/node-i2p)
- [haskell-network-anonymous-i2p](https://github.com/solatis/haskell-network-anonymous-i2p)
- [i2pdotnet for .Net languages](https://github.com/SamuelFisher/i2pdotnet)
- [rust-i2p](https://github.com/stallmanifold/rust-i2p)
- [and i2p.rb for ruby](https://github.com/dryruby/i2p.rb)

Wenn Sie eine dieser Sprachen verwenden, können Sie Ihre Anwendung möglicherweise bereits auf I2P portieren, indem Sie eine vorhandene Bibliothek nutzen. Darum geht es in diesem Tutorial jedoch nicht. Dieses Tutorial behandelt, was zu tun ist, wenn Sie eine SAM-Bibliothek in einer neuen Sprache erstellen möchten. In diesem Tutorial werde ich eine neue SAM-Bibliothek in Java implementieren. Ich habe Java gewählt, weil es noch keine Java-Bibliothek gibt, die Sie mit SAM verbindet, wegen der Verwendung von Java in Android und weil es eine Sprache ist, mit der fast jeder zumindest ein *bisschen* Erfahrung hat, sodass Sie es hoffentlich in eine Sprache Ihrer Wahl übertragen können.

## Erstellen Ihrer Bibliothek

Wie Sie Ihre eigene Bibliothek einrichten, hängt von der Sprache ab, die Sie verwenden möchten. Für diese Beispielbibliothek verwenden wir Java, sodass wir eine Bibliothek wie folgt erstellen können:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Oder, wenn Sie gradle 5 oder höher verwenden:

```sh
gradle init --type java-library --project-name jsam
```
## Einrichten der Bibliothek

Es gibt einige Datenelemente, die nahezu jede SAM‑Bibliothek vermutlich verwalten sollte. Sie muss mindestens die Adresse der SAM Bridge, die Sie zu verwenden beabsichtigen, sowie den Signaturtyp, den Sie verwenden möchten, speichern.

### Storing the SAM address

Ich bevorzuge, die SAM-Adresse als String und Integer zu speichern und sie zur Laufzeit in einer Funktion wieder zusammenzusetzen.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Die gültigen Signaturtypen für einen I2P Tunnel sind DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519; es wird jedoch dringend empfohlen, EdDSA_SHA512_Ed25519 als Standard zu verwenden, wenn Sie mindestens SAM 3.1 implementieren. In Java bietet sich die 'enum'-Datenstruktur für diese Aufgabe an, da sie dafür vorgesehen ist, eine Gruppe von Konstanten zu enthalten. Fügen Sie das enum sowie eine Instanz dieses enum in Ihre Java-Klassendefinition ein.

```java
enum SIGNATURE_TYPE {
    DSA_SHA1,
    ECDSA_SHA256_P256,
    ECDSA_SHA384_P384,
    ECDSA_SHA512_P521,
    EdDSA_SHA512_Ed25519;
}
public SIGNATURE_TYPE SigType = SIGNATURE_TYPE.EdDSA_SHA512_Ed25519;
```
### Speichern der SAM-Adresse

Damit ist das zuverlässige Speichern des von der SAM-Verbindung verwendeten Signaturtyps sichergestellt, aber Sie müssen ihn noch als Zeichenkette abrufen, um ihn an die Bridge zu übermitteln.

```java
public String SignatureType() {
    switch (SigType) {
        case DSA_SHA1:
            return "SIGNATURE_TYPE=DSA_SHA1";
        case ECDSA_SHA256_P256:
            return "SIGNATURE_TYPE=ECDSA_SHA256_P256";
        case ECDSA_SHA384_P384:
            return "SIGNATURE_TYPE=ECDSA_SHA384_P384";
        case ECDSA_SHA512_P521:
            return "SIGNATURE_TYPE=ECDSA_SHA512_P521";
        case EdDSA_SHA512_Ed25519:
            return "SIGNATURE_TYPE=EdDSA_SHA512_Ed25519";
    }
    return "";
}
```
Es ist wichtig, Dinge zu testen, also schreiben wir einige Tests:

```java
@Test public void testValidDefaultSAMAddress() {
    Jsam classUnderTest = new Jsam();
    assertEquals("127.0.0.1:7656", classUnderTest.SAMAddress());
}
@Test public void testValidDefaultSignatureType() {
    Jsam classUnderTest = new Jsam();
    assertEquals("EdDSA_SHA512_Ed25519", classUnderTest.SignatureType());
}
```
Sobald das erledigt ist, beginnen Sie mit der Erstellung Ihres Konstruktors. Beachten Sie, dass wir unserer Bibliothek Standardwerte gegeben haben, die in Standardsituationen auf allen bislang existierenden I2P router nützlich sind.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Kommen wir endlich zum interessanten Teil. Die Interaktion mit der SAM-Bridge erfolgt, indem ein "Befehl" an die Adresse der SAM-Bridge gesendet wird, und das Ergebnis des Befehls lässt sich als eine Menge von String-basierten Schlüssel-Wert-Paaren parsen. Vor diesem Hintergrund stellen wir nun eine Lese-/Schreibverbindung zur zuvor definierten SAM-Adresse her und schreiben anschließend eine "CommandSAM"-Funktion sowie einen Antwort-Parser.

### Speichern des Signaturtyps

Wir kommunizieren mit SAM über einen Socket, daher müssen Sie, um eine Verbindung zum Socket herzustellen, aus dem Socket zu lesen und in den Socket zu schreiben, die folgenden privaten Variablen in der Klasse Jsam erstellen:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Außerdem sollten Sie diese Variablen in Ihren Konstruktoren instanziieren, indem Sie dafür eine Funktion erstellen.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
    startConnection();
}
public void startConnection() {
    try {
        socket = new Socket(SAMHost, SAMPort);
        writer = new PrintWriter(socket.getOutputStream(), true);
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
### Sending a Command to SAM

Jetzt bist du bereit, endlich mit SAM zu sprechen. Um alles übersichtlich zu halten, lass uns eine Funktion erstellen, die einen einzelnen Befehl an SAM sendet, der mit einem Zeilenumbruch endet, und die ein Reply-Objekt zurückgibt, das wir im nächsten Schritt erstellen werden:

```java
public Reply CommandSAM(String args) {
    writer.println(args + "\n");
    try {
        String repl = reader.readLine();
        return new Reply(repl);
    } catch (Exception e) {
        //omitted for brevity
    }
}
```
Beachten Sie, dass wir den writer und reader, die wir im vorherigen Schritt aus dem socket erstellt haben, als unsere Ein- und Ausgabe für den socket verwenden. Wenn wir vom reader eine Antwort erhalten, übergeben wir die Zeichenkette an den Reply-Konstruktor, der sie parst und das Reply-Objekt zurückgibt.

### Parsing a reply and creating a Reply object.

Um Antworten einfacher zu verarbeiten, verwenden wir ein Reply-Objekt, um die Ergebnisse, die wir von der SAM-Bridge erhalten, automatisch zu parsen. Ein Reply-Objekt hat mindestens ein topic, ein type und ein result sowie eine beliebige Anzahl von Schlüssel-Wert-Paaren.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Wie Sie sehen, werden wir das "result" als ein Enum (Enumerationstyp), REPLY_TYPES, speichern. Dieses Enum enthält alle möglichen Antwortergebnisse, die die SAM-Bridge zurückgeben könnte.

```java
enum REPLY_TYPES {
    OK,
    CANT_REACH_PEER,
    DUPLICATED_ID,
    DUPLICATED_DEST,
    I2P_ERROR,
    INVALID_KEY,
    KEY_NOT_FOUND,
    PEER_NOT_FOUND,
    TIMEOUT;
    public static REPLY_TYPES set(String type) {
        String temp = type.trim();
        switch (temp) {
        case "RESULT=OK":
            return OK;
        case "RESULT=CANT_REACH_PEER":
            return CANT_REACH_PEER;
        case "RESULT=DUPLICATED_ID":
            return DUPLICATED_ID;
        case "RESULT=DUPLICATED_DEST":
            return DUPLICATED_DEST;
        case "RESULT=I2P_ERROR":
            return I2P_ERROR;
        case "RESULT=INVALID_KEY":
            return INVALID_KEY;
        case "RESULT=KEY_NOT_FOUND":
            return KEY_NOT_FOUND;
        case "RESULT=PEER_NOT_FOUND":
            return PEER_NOT_FOUND;
        case "RESULT=TIMEOUT":
            return TIMEOUT;
        }
        return I2P_ERROR;
    }
    public static String get(REPLY_TYPES type) {
        switch (type) {
        case OK:
            return "RESULT=OK";
        case CANT_REACH_PEER:
            return "RESULT=CANT_REACH_PEER";
        case DUPLICATED_ID:
            return "RESULT=DUPLICATED_ID";
        case DUPLICATED_DEST:
            return "RESULT=DUPLICATED_DEST";
        case I2P_ERROR:
            return "RESULT=I2P_ERROR";
        case INVALID_KEY:
            return "RESULT=INVALID_KEY";
        case KEY_NOT_FOUND:
            return "RESULT=KEY_NOT_FOUND";
        case PEER_NOT_FOUND:
            return "RESULT=PEER_NOT_FOUND";
        case TIMEOUT:
            return "RESULT=TIMEOUT";
        }
        return "RESULT=I2P_ERROR";
    }
};
```
Erstellen wir nun unseren Konstruktor, der den vom Socket empfangenen Antwort-String als Parameter entgegennimmt, ihn parst und die Informationen verwendet, um das Antwortobjekt zu initialisieren. Die Antwort ist durch Leerzeichen getrennt; Schlüssel-Wert-Paare sind durch ein Gleichheitszeichen verbunden und enden mit einem Zeilenumbruch.

```java
public Reply(String reply) {
    String trimmed = reply.trim();
    String[] replyvalues = reply.split(" ");
    if (replyvalues.length < 2) {
        //omitted for brevity
    }
    topic = replyvalues[0];
    type = replyvalues[1];
    result = REPLY_TYPES.set(replyvalues[2]);

    String[] replyLast = Arrays.copyOfRange(replyvalues, 2, replyvalues.length);
    for (int x = 0; x < replyLast.length; x++) {
        String[] kv = replyLast[x].split("=", 2);
        if (kv.length != 2) {

        }
        replyMap.put(kv[0], kv[1]);
    }
}
```
Zum Schluss fügen wir dem Reply-Objekt der Einfachheit halber eine toString()-Funktion hinzu, die eine String-Darstellung des Reply-Objekts zurückgibt.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Verbindung zum SAM-Port herstellen

Jetzt sind wir bereit, die Kommunikation mit SAM herzustellen, indem wir eine "Hello"-Nachricht senden. Wenn Sie eine neue SAM-Bibliothek schreiben, sollten Sie vermutlich mindestens SAM 3.1 anvisieren, da es sowohl in I2P als auch in i2pd verfügbar ist und Unterstützung für den SIGNATURE_TYPE-Parameter einführt.

```java
public boolean HelloSAM() {
    Reply repl = CommandSAM("HELLO VERSION MIN=3.0 MAX=3.1 \n");
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return true;
    }
    System.out.println(repl.String());
    return false;
}
```
Wie Sie sehen, verwenden wir die zuvor erstellte CommandSAM-Funktion, um den durch einen Zeilenumbruch abgeschlossenen Befehl `HELLO VERSION MIN=3.0 MAX=3.1 \n` zu senden. Damit teilen Sie SAM mit, dass Sie die Kommunikation mit der API starten möchten und dass Sie SAM in den Versionen 3.0 und 3.1 sprechen können. Der router wird wiederum mit etwas wie `HELLO REPLY RESULT=OK VERSION=3.1` antworten, was eine Zeichenkette ist, die Sie an den Reply-Konstruktor übergeben können, um ein gültiges Reply-Objekt zu erhalten. Von nun an können wir unsere CommandSAM-Funktion und das Reply-Objekt verwenden, um die gesamte Kommunikation über die SAM bridge abzuwickeln.

Zum Schluss fügen wir einen Test für unsere Funktion "HelloSAM" hinzu.

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Einen Befehl an SAM senden

Jetzt, da Sie Ihre Verbindung zu SAM ausgehandelt und sich auf eine von beiden Seiten unterstützte SAM-Version geeinigt haben, können Sie Peer-to-Peer-Verbindungen für Ihre Anwendung einrichten, damit sie sich mit anderen i2p-Anwendungen verbinden kann. Dazu senden Sie einen "SESSION CREATE"-Befehl an die SAM Bridge. Dafür verwenden wir eine CreateSession-Funktion, die eine Session-ID und einen Destination-Typ-Parameter akzeptiert.

```java
public String CreateSession(String id, String destination ) {
    if (destination == "") {
        destination = "TRANSIENT";
    }
    Reply repl = CommandSAM("SESSION CREATE STYLE=STREAM ID=" + ID + " DESTINATION=" + destination);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        return id;
    }
    return "";
}
```
Das war einfach, oder? Alles, was wir tun mussten, war, das Muster aus unserer HelloSAM-Funktion auf den `SESSION CREATE`-Befehl zu übertragen. Eine gute Antwort von der Bridge liefert weiterhin OK; in diesem Fall geben wir die ID der neu erstellten SAM-Verbindung zurück. Andernfalls geben wir einen leeren String zurück, da das ohnehin eine ungültige ID ist und der Vorgang fehlgeschlagen ist; so lässt sich das leicht prüfen. Sehen wir uns an, ob diese Funktion funktioniert, indem wir einen Test dafür schreiben:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Beachten Sie, dass wir in diesem Test *müssen* zuerst HelloSAM aufrufen, um die Kommunikation mit SAM herzustellen, bevor wir unsere Sitzung starten. Andernfalls wird die Bridge mit einem Fehler antworten und der Test wird fehlschlagen.

### Das Parsen einer Antwort und das Erstellen eines Reply-Objekts.

Nun ist Ihre Sitzung etabliert und Ihre lokale Destination (Zieladresse) vorhanden, und Sie müssen entscheiden, was Sie damit tun möchten. Ihre Sitzung kann nun angewiesen werden, sich über I2P mit einem entfernten Dienst zu verbinden oder auf eingehende Verbindungen zu warten, um darauf zu reagieren. Bevor Sie jedoch eine Verbindung zu einer entfernten Destination herstellen können, müssen Sie möglicherweise die Base64-Darstellung der Destination beschaffen, die die API erwartet. Um dies zu tun, erstellen wir eine Funktion LookupName, die die Base64-Darstellung in einer verwendbaren Form zurückgibt.

```java
public String LookupName(String name) {
    String cmd = "NAMING LOOKUP NAME=" + name + "\n";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.replyMap.get("VALUE"));
        return repl.replyMap.get("VALUE");
    }
    return "";
}
```
Erneut ist dies nahezu dasselbe wie unsere Funktionen HelloSAM und CreateSession, mit einem Unterschied. Da wir gezielt nach dem VALUE suchen und das Feld NAME dem Argument `name` entspricht, gibt es einfach den Base64-String der angeforderten Destination zurück.

Jetzt, da wir unsere Funktion LookupName haben, testen wir sie:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### "HELLO" an SAM senden

Endlich werden wir mit unserer neuen Bibliothek eine Verbindung zu einem anderen Dienst herstellen. Dieser Teil hat mich anfangs etwas verwirrt, aber die scharfsinnigsten Java-Entwickler haben sich wahrscheinlich gefragt, warum wir nicht die Socket-Klasse erweitert haben, statt innerhalb der Jsam-Klasse eine Socket-Variable zu erstellen. Das liegt daran, dass wir bis jetzt mit dem "Control Socket (Steuer-Socket)" kommuniziert haben und für die eigentliche Kommunikation einen neuen Socket erstellen müssen. Deshalb haben wir bis jetzt damit gewartet, die Jsam-Klasse von der Socket-Klasse abzuleiten:

```java
public class Jsam extends Socket {
```
Außerdem ändern wir unsere Funktion startConnection so, dass wir sie verwenden können, um vom Control-Socket zu dem Socket zu wechseln, den wir in unserer Anwendung verwenden werden. Sie wird nun ein Socket-Argument entgegennehmen.

```java
public void startConnection(Socket socket) {
    try {
        socket.connect(new InetSocketAddress(SAMHost, SAMPort), 600 );
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        writer = new PrintWriter(socket.getOutputStream(), true);
    } catch (Exception e) {
        System.out.println(e);
    }
    try {
        reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    } catch (Exception e) {
        System.out.println(e);
    }
}
```
Dies ermöglicht es uns, schnell und einfach einen neuen Socket zu öffnen, um darüber zu kommunizieren, den "Hello SAM"-Handshake erneut durchzuführen und den Stream zu verbinden.

```java
public String ConnectSession(String id, String destination) {
    startConnection(this);
    HelloSAM();
    if (destination.endsWith(".i2p")) {
        destination = LookupName(destination);
    }
    String cmd = "STREAM CONNECT ID=" + id + " DESTINATION=" + destination + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
Und jetzt haben Sie einen neuen Socket für die Kommunikation über SAM! Lassen Sie uns dasselbe für das Annehmen von Remote-Verbindungen tun:

```java
public String AcceptSession(String id) {
    startConnection(this);
    HelloSAM();
    String cmd = "STREAM ACCEPT ID=" + id  + " SILENT=false";
    Reply repl = CommandSAM(cmd);
    if (repl.result == Reply.REPLY_TYPES.OK) {
        System.out.println(repl.String());
        return id;
    }
    System.out.println(repl.String());
    return "";
}
```
So, das war’s. So baut man eine SAM-Bibliothek, Schritt für Schritt. In Zukunft werde ich Querverweise auf die funktionsfähige Version der Bibliothek Jsam und die SAM v3-Spezifikation einfügen, aber fürs Erste muss ich noch ein paar andere Dinge erledigen.
