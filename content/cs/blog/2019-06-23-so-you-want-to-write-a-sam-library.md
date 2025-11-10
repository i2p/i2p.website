---
title: "Tak chcete napsat knihovnu pro SAM"
date: 2019-06-23
author: "idk"
description: "Příručka pro začátečníky: jak napsat knihovnu pro SAM!"
---

*Nebo, komunikace s [i2p](https://geti2p.net) pro lidi, kteří nejsou příliš zvyklí číst specifikace*

Jednou z nejlepších funkcí I2P je podle mého názoru jeho SAM API, které lze použít k vytvoření mostu mezi I2P a vaší aplikací nebo vámi zvoleným jazykem. V současnosti existují desítky knihoven SAM pro různé jazyky, včetně:

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

Pokud používáte některý z těchto jazyků, možná už budete moci portovat svou aplikaci na I2P s využitím existující knihovny. O tom ale tento návod není. Tento návod je o tom, co dělat, pokud chcete vytvořit SAM library (knihovna pro rozhraní SAM) v novém jazyce. V tomto návodu implementuji novou SAM library v jazyce Java. Zvolil jsem Javu, protože zatím neexistuje Java knihovna, která by vás připojila k SAM, kvůli využití Javy v Androidu, a také proto, že je to jazyk, se kterým má téměř každý alespoň *trochu* zkušeností, takže jej snad budete moci převést do jazyka podle svého výběru.

## Vytvoření vaší knihovny

Jak si nastavíte vlastní knihovnu, se bude lišit podle jazyka, který chcete použít. V tomto příkladu použijeme Javu, takže můžeme vytvořit knihovnu takto:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Nebo, pokud používáte gradle 5 nebo novější:

```sh
gradle init --type java-library --project-name jsam
```
## Nastavení knihovny

Existuje několik údajů, které by téměř každá knihovna SAM měla pravděpodobně spravovat. Bude přinejmenším muset uložit adresu SAM Bridge, který hodláte použít, a typ podpisu, který hodláte použít.

### Storing the SAM address

Dávám přednost ukládat adresu SAM jako String a Integer a za běhu je znovu zkombinovat ve funkci.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Platné typy podpisů pro I2P Tunnel jsou DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, ale důrazně se doporučuje použít EdDSA_SHA512_Ed25519 jako výchozí, pokud implementujete alespoň SAM 3.1. V Javě se k tomuto úkolu hodí datová struktura 'enum', protože je určena k obsahování skupiny konstant. Do definice své třídy v Javě přidejte enum a instanci tohoto enumu.

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
### Uložení adresy SAM

Tím je zajištěno spolehlivé uložení typu podpisu, který používá připojení SAM, ale pořád jej ještě musíte získat jako řetězec, abyste jej mohli předat bridge.

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
Je důležité věci testovat, tak pojďme napsat několik testů:

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
Jakmile je to hotovo, začněte vytvářet svůj konstruktor. Všimněte si, že jsme naší knihovně nastavili výchozí hodnoty, které budou užitečné ve výchozích situacích na všech dosavadních I2P routerech.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

A konečně to nejlepší. Interakce s mostem SAM se provádí odesláním "příkazu" na adresu mostu SAM a výsledek příkazu můžete parsovat jako sadu řetězcových dvojic klíč-hodnota. Mějme to na paměti a navážeme připojení pro čtení i zápis k SAM Address, kterou jsme si dříve definovali, poté napíšeme funkci "CommandSAM" a parser odpovědi.

### Ukládání typu podpisu

Komunikujeme se SAM přes Socket, takže abyste se mohli k socketu připojit, číst z něj a zapisovat do něj, budete muset ve třídě Jsam vytvořit následující soukromé proměnné:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Také budete chtít tyto proměnné inicializovat ve svých konstruktorech vytvořením funkce k tomuto účelu.

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
### Získání typu podpisu:

Nyní máte vše připraveno a můžete konečně začít komunikovat s protokolem SAM. Aby bylo vše pěkně uspořádané, vytvořme funkci, která odešle jeden příkaz protokolu SAM, ukončený znakem nového řádku, a vrátí objekt Reply, který vytvoříme v dalším kroku:

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
Všimněte si, že jako vstupy a výstupy pro socket používáme writer a reader, které jsme v předchozím kroku vytvořili z proměnné socket. Když obdržíme odpověď od reader, předáme řetězec konstruktoru Reply, který ji parsuje a vrátí objekt Reply.

### Parsing a reply and creating a Reply object.

Abychom mohli snáze zpracovávat odpovědi, použijeme objekt Reply k automatickému parsování výsledků, které získáme od SAM bridge. Odpověď obsahuje alespoň téma, typ a výsledek, a také libovolný počet párů klíč–hodnota.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Jak vidíte, budeme ukládat "result" jako výčtový typ (enum), REPLY_TYPES. Tento výčtový typ obsahuje všechny možné výsledky odpovědi, kterými může SAM bridge odpovědět.

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
Nyní vytvořme náš konstruktor, který jako parametr přijme řetězec odpovědi přijatý ze socketu, rozparsuje jej a použije získané informace k inicializaci objektu odpovědi. Odpověď je tvořena položkami oddělenými mezerami, přičemž dvojice klíč–hodnota jsou spojeny znakem rovná se a je ukončena znakem nového řádku.

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
Nakonec, pro větší pohodlí, přidejme objektu odpovědi funkci toString(), která vrací řetězcovou reprezentaci objektu Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Připojení k portu SAM

Nyní jsme připraveni navázat komunikaci se SAM odesláním zprávy "Hello". Pokud píšete novou knihovnu pro SAM, měli byste pravděpodobně cílit alespoň na SAM 3.1, protože je k dispozici jak v I2P, tak v i2pd a zavádí podporu pro parametr SIGNATURE_TYPE.

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
As you can see, we use the CommandSAM function we created before to send the newline-terminated command `HELLO VERSION MIN=3.0 MAX=3.1 \n`. This tells SAM that you want to start communicating with the API, and that you know how to speak SAM version 3.0 and 3.1. The router, in turn, will respond with like `HELLO REPLY RESULT=OK VERSION=3.1` which is a string you can pass to the Reply constructor to get a valid Reply object. From now on, we can use our CommandSAM function and Reply object to deal with all our communication across the SAM bridge.

Finally, let's add a test for our "HelloSAM" function.

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Odeslání příkazu SAMu

Nyní, když jste vyjednali své připojení k SAM a dohodli se na verzi SAM, které oba rozumíte, můžete nastavit peer-to-peer připojení pro svou aplikaci, aby se mohla připojit k dalším i2p aplikacím. Uděláte to odesláním příkazu "SESSION CREATE" na SAM Bridge. K tomu použijeme funkci CreateSession, která přijímá ID relace a parametr typu destinace.

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
To bylo snadné, že? Vše, co jsme museli udělat, bylo přizpůsobit vzor, který jsme použili v naší funkci HelloSAM, příkazu `SESSION CREATE`. Správná odpověď od bridge (mostu) opět vrátí OK, a v tom případě vrátíme ID nově vytvořeného SAM spojení. V opačném případě vrátíme prázdný řetězec, protože to stejně není platné ID a operace selhala, takže se to snadno zkontroluje. Ověřme, že tato funkce funguje, napsáním testu:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Vezměte na vědomí, že v tomto testu *musíme* nejprve zavolat HelloSAM, abychom navázali komunikaci se SAM před zahájením naší relace. Pokud ne, most odpoví chybou a test selže.

### Parsování odpovědi a vytvoření objektu Reply.

Now you have your session established and your local destination, and need to decide what you want to do with them. Your session can now be commanded to connect to a remote service over I2P, or to wait for incoming connections to respond to. However, before you can connect to a remote destination, you may need to obtain the base64 of the destination, which is what the API expects. In order to do this, we'll create a LookupName function, which will return the base64 in a usable form.

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
Opět je to téměř totéž jako naše funkce HelloSAM a CreateSession, s jediným rozdílem. Protože hledáme konkrétně VALUE a pole NAME bude stejné jako argument `name`, jednoduše vrátí base64 řetězec požadované destinace.

Nyní, když máme funkci LookupName, otestujme ji:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Říct "HELLO" SAMu

Konečně se chystáme navázat spojení s jinou službou pomocí naší nové knihovny. Tato část mě zpočátku trochu mátla, ale ti nejbystřejší Java vývojáři si nejspíš říkali, proč jsme místo vytvoření proměnné typu Socket uvnitř třídy Jsam nezdědili z třídy Socket. Je to proto, že až dosud jsme komunikovali přes "Control Socket" a pro vlastní komunikaci potřebujeme vytvořit nový socket. Proto jsme s rozšířením třídy Socket třídou Jsam počkali až doteď:

```java
public class Jsam extends Socket {
```
Také upravme naši funkci startConnection tak, abychom ji mohli použít k přepnutí z řídicího socketu na socket, který budeme používat v naší aplikaci. Nyní bude přijímat argument typu Socket.

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
To nám umožňuje rychle a snadno otevřít nový socket pro komunikaci, znovu provést handshake "Hello SAM" a připojit stream.

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
A nyní máte nový Socket pro komunikaci přes SAM! Pojďme udělat totéž pro Přijímání vzdálených připojení:

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
A je to. Takto se krok za krokem vytváří knihovna SAM. V budoucnu to propojím křížovými odkazy s funkční verzí knihovny, Jsam, a se specifikací SAM v3, ale teď se musím věnovat dalším věcem.
