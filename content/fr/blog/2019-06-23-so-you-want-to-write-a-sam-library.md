---
title: "Vous souhaitez écrire une bibliothèque SAM"
date: 2019-06-23
author: "idk"
description: "Guide du débutant pour écrire une bibliothèque SAM !"
---

*Ou, communiquer avec [i2p](https://geti2p.net) pour les personnes qui ne sont pas vraiment habituées à lire des spécifications*

L’une des meilleures fonctionnalités d’I2P, à mon avis, est son API SAM, qui peut être utilisée pour établir une passerelle entre I2P et votre application ou le langage de programmation de votre choix. Actuellement, des dizaines de bibliothèques SAM existent pour une variété de langages, notamment :

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

Si vous utilisez l’un de ces langages, il est peut-être déjà possible de porter votre application vers I2P en utilisant une bibliothèque existante. Cependant, ce n’est pas l’objet de ce tutoriel. Ce tutoriel explique quoi faire si vous souhaitez créer une bibliothèque SAM dans un nouveau langage. Dans ce tutoriel, je vais implémenter une nouvelle bibliothèque SAM en Java. J’ai choisi Java parce qu’il n’existe pas encore de bibliothèque Java qui vous connecte à SAM, en raison de l’utilisation de Java sur Android, et parce que c’est un langage avec lequel presque tout le monde a au moins un *peu* d’expérience, afin que, je l’espère, vous puissiez le porter dans le langage de votre choix.

## Création de votre bibliothèque

La façon de configurer votre propre bibliothèque dépendra du langage que vous souhaitez utiliser. Pour cette bibliothèque d'exemple, nous utiliserons java afin de pouvoir créer une bibliothèque comme ceci :

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Ou, si vous utilisez gradle 5 ou une version supérieure :

```sh
gradle init --type java-library --project-name jsam
```
## Configuration de la bibliothèque

Il y a quelques éléments de données que presque toute bibliothèque SAM devrait probablement gérer. Elle devra au minimum stocker l’adresse du SAM Bridge que vous avez l’intention d’utiliser et le type de signature que vous souhaitez utiliser.

### Storing the SAM address

Je préfère stocker l’adresse SAM sous la forme d’un String et d’un Integer, puis les recombiner dans une fonction à l’exécution.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Les types de signature valides pour un I2P Tunnel sont DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, mais il est fortement recommandé d'utiliser EdDSA_SHA512_Ed25519 par défaut si vous implémentez au moins SAM 3.1. En Java, la structure de données 'enum' (énumération) se prête bien à cette tâche, puisqu'elle est conçue pour contenir un ensemble de constantes. Ajoutez l'enum, ainsi qu'une instance de l'enum, à la définition de votre classe Java.

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
### Stockage de l’adresse SAM

Cela règle la question du stockage fiable du type de signature utilisé par la connexion SAM, mais il vous reste à le récupérer sous forme de chaîne de caractères afin de le communiquer au pont.

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
Il est important de tester, alors écrivons quelques tests :

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
Une fois cela fait, commencez à créer votre constructeur. Notez que nous avons défini des valeurs par défaut pour notre bibliothèque, qui seront utiles dans les configurations par défaut sur tous les I2P routers existants à ce jour.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Enfin, la partie intéressante. L’interaction avec le SAM bridge se fait en envoyant une "commande" à l’adresse du SAM bridge, et vous pouvez analyser le résultat de la commande comme un ensemble de paires clé-valeur basées sur des chaînes. Donc, en gardant cela à l’esprit, établissons une connexion en lecture-écriture à la SAM Address que nous avons définie auparavant, puis écrivons une fonction "CommandSAM" et un analyseur de réponse.

### Stockage du type de signature

Nous communiquons avec SAM via un socket ; pour vous connecter au socket, lire depuis celui-ci et y écrire, vous devrez créer les variables privées suivantes dans la classe Jsam :

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Vous voudrez également instancier ces variables dans vos constructeurs en créant une fonction pour ce faire.

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
### Récupération du type de signature :

Vous êtes maintenant prêt à enfin commencer à communiquer avec SAM. Pour garder les choses bien organisées, créons une fonction qui envoie une seule commande à SAM, terminée par un saut de ligne, et qui renvoie un objet Reply, que nous créerons à l’étape suivante :

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
Notez que nous utilisons les writer et reader que nous avons créés à partir du socket à l’étape précédente en tant qu’entrées et sorties pour le socket. Lorsque nous recevons une réponse du reader, nous passons la chaîne au constructeur de Reply, qui l’analyse et renvoie l’objet Reply.

### Parsing a reply and creating a Reply object.

Afin de gérer plus facilement les réponses, nous allons utiliser un objet Reply pour analyser automatiquement les résultats que nous obtenons du SAM bridge. Une réponse comporte au minimum un topic, un type et un result, ainsi qu’un nombre arbitraire de paires clé-valeur.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Comme vous pouvez le voir, nous allons stocker le "result" sous forme d'une énumération, REPLY_TYPES. Cette énumération contient tous les résultats de réponse possibles que le SAM bridge peut renvoyer.

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
Créons maintenant notre constructeur, qui prend en paramètre la chaîne de réponse reçue depuis le socket, l’analyse et utilise les informations pour configurer l’objet de réponse. La réponse est délimitée par des espaces, avec des paires clé-valeur reliées par un signe égal et terminée par un saut de ligne.

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
Enfin, pour plus de commodité, donnons à l'objet Reply une fonction toString() qui renvoie une représentation sous forme de chaîne de caractères de l'objet Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Connexion au port SAM

Nous sommes maintenant prêts à établir la communication avec SAM en envoyant un message "Hello". Si vous écrivez une nouvelle bibliothèque SAM, vous devriez probablement cibler au moins SAM 3.1, puisqu’il est disponible à la fois dans I2P et i2pd et introduit la prise en charge du paramètre SIGNATURE_TYPE.

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
Comme vous pouvez le voir, nous utilisons la fonction CommandSAM que nous avons créée auparavant pour envoyer la commande terminée par un retour à la ligne `HELLO VERSION MIN=3.0 MAX=3.1 \n`. Cela indique à SAM que vous souhaitez commencer à communiquer avec l'API, et que vous savez utiliser SAM en versions 3.0 et 3.1. Le router, de son côté, répondra par quelque chose comme `HELLO REPLY RESULT=OK VERSION=3.1`, qui est une chaîne que vous pouvez passer au constructeur Reply pour obtenir un objet Reply valide. Désormais, nous pouvons utiliser notre fonction CommandSAM et l'objet Reply pour gérer toutes nos communications via la passerelle SAM.

Enfin, ajoutons un test pour notre fonction "HelloSAM".

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Envoi d'une commande à SAM

Maintenant que vous avez négocié votre connexion à SAM et convenu d’une version de SAM que vous prenez tous les deux en charge, vous pouvez configurer des connexions pair-à-pair pour que votre application se connecte à d’autres applications i2p. Pour ce faire, vous envoyez une commande "SESSION CREATE" au SAM Bridge. Pour cela, nous utiliserons une fonction CreateSession qui accepte un identifiant de session et un paramètre de type de destination.

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
C’était facile, non ? Il suffisait d’adapter le modèle que nous avons utilisé dans notre fonction HelloSAM à la commande `SESSION CREATE`. Une bonne réponse du bridge renverra toujours OK, et dans ce cas nous renvoyons l’ID de la connexion SAM nouvellement créée. Sinon, nous renvoyons une chaîne vide, car de toute façon c’est un ID invalide et l’opération a échoué, donc c’est facile à vérifier. Voyons si cette fonction fonctionne en écrivant un test :

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Notez que dans ce test, nous *devons* appeler HelloSAM d'abord pour établir la communication avec SAM avant de démarrer notre session. Sinon, la passerelle répondra par une erreur et le test échouera.

### Analyse d’une réponse et création d’un objet Reply.

Vous avez maintenant établi votre session et votre destination locale, et vous devez décider ce que vous voulez en faire. Votre session peut désormais recevoir l’ordre de se connecter à un service distant via I2P, ou d’attendre des connexions entrantes auxquelles répondre. Cependant, avant de pouvoir vous connecter à une destination distante, il peut être nécessaire d’obtenir le base64 de la destination, car c’est ce que l’API attend. Pour ce faire, nous allons créer une fonction LookupName, qui renverra le base64 sous une forme exploitable.

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
Là encore, c’est presque identique à nos fonctions HelloSAM et CreateSession, à une différence près. Comme nous recherchons spécifiquement la VALUE et que le champ NAME sera identique à l’argument `name`, elle renvoie simplement la chaîne en base64 de la destination demandée.

Maintenant que nous avons notre fonction LookupName, testons-la :

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Dire "HELLO" à SAM

Enfin, nous allons établir une connexion à un autre service avec notre nouvelle bibliothèque. Cette partie m'a un peu dérouté au début, mais les développeurs Java les plus avisés se demandaient probablement pourquoi nous n'avons pas étendu la classe Socket au lieu de créer une variable Socket à l'intérieur de la classe Jsam. C'est parce que, jusqu'à présent, nous communiquions avec le "Control Socket" (socket de contrôle) et nous devons créer un nouveau socket pour effectuer la communication proprement dite. Nous avons donc attendu pour étendre la classe Socket avec la classe Jsam jusqu'à présent:

```java
public class Jsam extends Socket {
```
Par ailleurs, modifions notre fonction startConnection afin de pouvoir l'utiliser pour passer du socket de contrôle au socket que nous utiliserons dans notre application. Elle prendra désormais un argument Socket.

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
Cela nous permet d’ouvrir rapidement et facilement une nouvelle socket pour communiquer, d’effectuer à nouveau le handshake « Hello SAM » et de connecter le flux.

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
Et maintenant, vous avez un nouveau Socket pour communiquer via SAM ! Faisons la même chose pour l’acceptation de connexions distantes:

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
Voilà. Voici comment créer une bibliothèque SAM, pas à pas. À l'avenir, je le confronterai à la version fonctionnelle de la bibliothèque, Jsam, ainsi qu'à la spécification SAM v3, mais pour l'instant j'ai d'autres choses à faire.
