---
title: "Así que quieres escribir una biblioteca SAM"
date: 2019-06-23
author: "idk"
description: "¡Guía para principiantes para desarrollar una biblioteca SAM!"
---

*O, comunicarse con [i2p](https://geti2p.net) para quienes no están realmente acostumbrados a leer especificaciones*

Una de las mejores características de I2P, en mi opinión, es su API SAM, que puede usarse para construir un puente entre I2P y tu aplicación o el lenguaje de tu elección. Actualmente, existen decenas de bibliotecas SAM para una variedad de lenguajes, incluidos:

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

Si estás usando alguno de estos lenguajes, puede que ya puedas portar tu aplicación a I2P utilizando una biblioteca existente. Sin embargo, de eso no trata este tutorial. Este tutorial trata sobre qué hacer si quieres crear una biblioteca SAM en un lenguaje nuevo. En este tutorial, implementaré una nueva biblioteca SAM en Java. Elegí Java porque aún no existe una biblioteca en Java que te conecte a SAM, por el uso de Java en Android y porque es un lenguaje con el que casi todo el mundo tiene al menos un *poco* de experiencia, así que, con suerte, podrás traducirlo al lenguaje de tu elección.

## Creación de tu biblioteca

La forma de configurar tu propia biblioteca variará según el lenguaje que desees usar. Para esta biblioteca de ejemplo, usaremos Java para poder crear una biblioteca como esta:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
O, si está usando gradle 5 o posterior:

```sh
gradle init --type java-library --project-name jsam
```
## Configuración de la biblioteca

Hay algunos datos que casi cualquier biblioteca SAM probablemente debería gestionar. Como mínimo, necesitará almacenar la dirección del SAM Bridge (puente SAM) que tiene intención de utilizar y el tipo de firma que desea utilizar.

### Storing the SAM address

Prefiero almacenar la dirección SAM como un String y un Integer, y recombinarlos en una función en tiempo de ejecución.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Los tipos de firma válidos para un I2P Tunnel son DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, pero se recomienda encarecidamente usar EdDSA_SHA512_Ed25519 como valor predeterminado si implementas al menos SAM 3.1. En Java, la estructura de datos 'enum' se presta bien para esta tarea, ya que está pensada para contener un grupo de constantes. Añade el enum, y una instancia del enum, a la definición de tu clase de Java.

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
### Almacenamiento de la dirección SAM

Eso se encarga de almacenar de forma fiable el tipo de firma en uso por la conexión SAM, pero aún debes recuperarlo como una cadena para comunicárselo al puente.

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
Es importante probar las cosas, así que escribamos algunas pruebas:

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
Una vez hecho esto, comienza a crear tu constructor. Ten en cuenta que hemos definido valores predeterminados en nuestra biblioteca que serán útiles en escenarios predeterminados en todos los routers I2P existentes hasta ahora.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Finalmente, la parte buena. La interacción con el puente SAM se realiza enviando un "command" a la dirección del puente SAM, y puedes analizar el resultado del comando como un conjunto de pares clave-valor basados en cadenas. Teniendo esto en cuenta, establezcamos una conexión de lectura y escritura con el SAM Address que definimos antes y luego escribamos una función "CommandSAM" y un analizador de respuestas.

### Almacenamiento del tipo de firma

Nos estamos comunicando con SAM a través de un Socket, así que, para conectarte al socket, leer desde él y escribir en él, necesitarás crear las siguientes variables privadas en la clase Jsam:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
También querrás instanciar esas variables en tus Constructores creando una función para hacerlo.

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
### Obtención del tipo de firma:

Ahora ya está todo listo para empezar, por fin, a comunicarte con SAM. Para mantener todo bien organizado, vamos a crear una función que envíe un único comando a SAM, terminado en un salto de línea, y que devuelva un objeto Reply, que crearemos en el siguiente paso:

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
Ten en cuenta que estamos usando el escritor (writer) y el lector (reader) que creamos a partir del socket en el paso anterior como nuestras entradas y salidas del socket. Cuando recibimos una respuesta del lector, pasamos la cadena al constructor de Reply, que la analiza y devuelve el objeto Reply.

### Parsing a reply and creating a Reply object.

Para manejar más fácilmente las respuestas, usaremos un objeto Reply para analizar automáticamente los resultados que obtenemos del SAM bridge. Una respuesta tiene al menos un tema, un tipo y un resultado, así como un número arbitrario de pares clave-valor.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Como puede ver, almacenaremos el "result" como un enum (enumeración), REPLY_TYPES. Este enum contiene todos los posibles resultados de respuesta que el SAM bridge podría devolver.

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
Ahora creemos nuestro constructor, que toma como parámetro la cadena de respuesta recibida del socket, la analiza y utiliza la información para configurar el objeto de respuesta. La respuesta está delimitada por espacios, con pares clave-valor unidos por un signo igual y terminada por un salto de línea.

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
Por último, para mayor comodidad, agreguemos al objeto Reply una función toString() que devuelva una representación en cadena del objeto Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Conectarse al puerto SAM

Ahora estamos listos para establecer comunicación con SAM enviando un mensaje "Hello". Si estás escribiendo una nueva biblioteca de SAM, probablemente deberías apuntar como mínimo a SAM 3.1, ya que está disponible tanto en I2P como en i2pd e introduce compatibilidad con el parámetro SIGNATURE_TYPE.

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
Como puedes ver, usamos la función CommandSAM que creamos antes para enviar el comando terminado en salto de línea `HELLO VERSION MIN=3.0 MAX=3.1 \n`. Esto le indica a SAM que quieres empezar a comunicarte con la API y que sabes hablar SAM versión 3.0 y 3.1. El router, a su vez, responderá con algo como `HELLO REPLY RESULT=OK VERSION=3.1`, que es una cadena que puedes pasar al constructor de Reply para obtener un objeto Reply válido. A partir de ahora, podemos usar nuestra función CommandSAM y el objeto Reply para gestionar toda nuestra comunicación a través del puente SAM.

Por último, agreguemos una prueba para nuestra función "HelloSAM".

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Enviar un comando a SAM

Ahora que has negociado tu conexión con SAM y acordado una versión de SAM que ambos admiten, puedes configurar conexiones peer-to-peer (entre pares) para que tu aplicación se conecte a otras aplicaciones i2p. Esto se hace enviando un comando "SESSION CREATE" al SAM Bridge. Para ello, usaremos una función CreateSession que acepta un ID de sesión y un parámetro de tipo de destino.

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
Eso fue fácil, ¿verdad? Todo lo que teníamos que hacer era adaptar el patrón que usamos en nuestra función HelloSAM al comando `SESSION CREATE`. Una buena respuesta del puente seguirá devolviendo OK, y en ese caso devolvemos el ID de la conexión SAM recién creada. De lo contrario, devolvemos una cadena vacía porque, de todos modos, es un ID no válido y ha fallado, así que es fácil de comprobar. Veamos si esta función funciona escribiendo una prueba para comprobarlo:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Tenga en cuenta que en esta prueba *debemos* llamar a HelloSAM primero para establecer comunicación con SAM antes de iniciar nuestra sesión. De lo contrario, el puente responderá con un error y la prueba fallará.

### Analizando una respuesta y creando un objeto Reply.

Ahora tienes tu sesión establecida y tu destino local, y necesitas decidir qué quieres hacer con ellos. Ahora puedes indicarle a tu sesión que se conecte a un servicio remoto a través de I2P, o que espere conexiones entrantes a las que responder. Sin embargo, antes de poder conectarte a un destino remoto, puede que necesites obtener el base64 del destino, que es lo que espera la API. Para ello, crearemos una función LookupName, que devolverá el base64 en un formato utilizable.

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
De nuevo, esto es casi lo mismo que nuestras funciones HelloSAM y CreateSession, con una diferencia. Como buscamos específicamente el VALUE y el campo NAME será el mismo que el argumento `name`, simplemente devuelve la cadena en base64 del destino solicitado.

Ahora que tenemos nuestra función LookupName, probémosla:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Diciendo "HELLO" a SAM

Por fin, vamos a establecer una conexión con otro servicio con nuestra nueva biblioteca. Esta parte me confundió un poco al principio, pero los desarrolladores de Java más astutos probablemente se preguntaban por qué no extendimos la clase Socket en lugar de crear una variable Socket dentro de la clase Jsam. Esto se debe a que, hasta ahora, nos hemos estado comunicando con el "Control Socket" y necesitamos crear un nuevo socket para realizar la comunicación propiamente dicha. Así que hemos esperado hasta ahora para que la clase Jsam extienda la clase Socket:

```java
public class Jsam extends Socket {
```
Además, vamos a modificar nuestra función startConnection para que podamos usarla para cambiar del socket de control al socket que usaremos en nuestra aplicación. Ahora recibirá un argumento de tipo Socket.

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
Esto nos permite abrir rápida y fácilmente un nuevo socket por el cual comunicarnos, realizar de nuevo el handshake "Hello SAM" y conectar el stream (flujo).

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
¡Y ahora ya cuentas con un nuevo Socket para comunicarte a través de SAM! Hagamos lo mismo para aceptar conexiones remotas:

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
Ahí lo tienes. Así es como se construye una biblioteca de SAM, paso a paso. En el futuro, haré referencias cruzadas de esto con la versión funcional de la biblioteca, Jsam, y la especificación de SAM v3, pero por ahora tengo que ocuparme de otras tareas.
