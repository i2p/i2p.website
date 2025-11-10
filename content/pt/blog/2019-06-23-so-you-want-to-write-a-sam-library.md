---
title: "Então você quer desenvolver uma biblioteca SAM"
date: 2019-06-23
author: "idk"
description: "Guia para iniciantes para desenvolver uma biblioteca SAM!"
---

*Ou, falando com [i2p](https://geti2p.net) para pessoas que não estão muito acostumadas a ler especificações*

Uma das melhores funcionalidades do I2P, na minha opinião, é a sua SAM API, que pode ser usada para construir uma ponte entre o I2P e a sua aplicação ou linguagem de preferência. Atualmente, existem dezenas de bibliotecas SAM para uma variedade de linguagens, incluindo:

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

Se você estiver usando qualquer uma dessas linguagens, talvez já consiga portar sua aplicação para o I2P usando uma biblioteca existente. No entanto, não é disso que trata este tutorial. Este tutorial trata do que fazer se você quiser criar uma biblioteca SAM em uma nova linguagem. Neste tutorial, vou implementar uma nova biblioteca SAM em Java. Escolhi Java porque ainda não existe uma biblioteca Java que conecte você ao SAM, por causa do uso de Java no Android e porque é uma linguagem com a qual quase todo mundo tem pelo menos um *pouco* de experiência; assim, espero que você consiga traduzi-la para uma linguagem de sua preferência.

## Criando sua biblioteca

A forma como você configura sua própria biblioteca vai variar dependendo da linguagem que deseja usar. Para esta biblioteca de exemplo, usaremos Java, assim podemos criar uma biblioteca como esta:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Ou, se você estiver usando o Gradle 5 ou superior:

```sh
gradle init --type java-library --project-name jsam
```
## Configurando a biblioteca

Há alguns dados que praticamente qualquer biblioteca SAM deve gerenciar. Ela, no mínimo, precisará armazenar o endereço do SAM Bridge (ponte SAM) que você pretende usar e o tipo de assinatura que deseja usar.

### Storing the SAM address

Eu prefiro armazenar o endereço SAM como uma String e um Integer, e recombiná-los em uma função em tempo de execução.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Os tipos de assinatura válidos para um I2P Tunnel são DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, mas é fortemente recomendado que você use EdDSA_SHA512_Ed25519 como padrão se implementar pelo menos SAM 3.1. Em Java, a estrutura de dados 'enum' (enumeração) presta-se bem a essa tarefa, pois é destinada a conter um conjunto de constantes. Adicione o enum e uma instância do enum à definição da sua classe Java.

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
### Armazenando o endereço SAM

Isso cuida de armazenar de forma confiável o tipo de assinatura em uso pela conexão SAM, mas você ainda precisa recuperá-lo como uma cadeia de caracteres para comunicá-lo à ponte.

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
É importante testar, então vamos escrever alguns testes:

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
Depois disso, comece a criar seu construtor. Observe que definimos padrões para nossa biblioteca que serão úteis em situações padrão em todos os I2P routers existentes até agora.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Finalmente, a parte boa. A interação com a ponte SAM é feita enviando um "command" para o endereço da ponte SAM, e você pode analisar o resultado do command como um conjunto de pares chave-valor baseados em cadeias de caracteres. Tendo isso em mente, vamos estabelecer uma conexão de leitura e escrita com o SAM Address que definimos antes e, em seguida, escrever uma função "CommandSAM" e um analisador de resposta.

### Armazenando o Tipo de Assinatura

Estamos nos comunicando com o SAM via um Socket, portanto, para se conectar ao socket, ler dele e escrever nele, você precisará criar as seguintes variáveis privadas na classe Jsam:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Você também vai querer instanciar essas variáveis nos seus Construtores, criando uma função para isso.

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
### Obtendo o tipo de assinatura:

Agora está tudo pronto para finalmente começar a se comunicar com o SAM. Para manter tudo bem organizado, vamos criar uma função que envie um único comando para o SAM, terminado por uma quebra de linha, e que retorne um objeto Reply, que criaremos na próxima etapa:

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
Observe que estamos usando o writer e o reader que criamos a partir do socket na etapa anterior como nossas entradas e saídas do socket. Quando recebemos uma resposta do reader, passamos a string para o construtor de Reply, que a analisa e retorna o objeto Reply.

### Parsing a reply and creating a Reply object.

Para lidar mais facilmente com as respostas, usaremos um objeto Reply para analisar automaticamente os resultados que obtivermos da SAM bridge. Uma resposta tem pelo menos um topic, um type e um result, além de um número arbitrário de pares chave-valor.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Como pode ver, armazenaremos o "result" como um enum, REPLY_TYPES. Este enum contém todos os possíveis resultados de resposta que a SAM bridge (ponte SAM) pode retornar.

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
Agora vamos criar nosso construtor, que recebe a string de resposta recebida do socket como parâmetro, a analisa e usa as informações para configurar o objeto de resposta. A resposta é delimitada por espaços, com pares chave-valor ligados por um sinal de igual e terminada por um caractere de nova linha.

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
Por fim, para maior conveniência, vamos dar ao objeto reply uma função toString() que retorna uma representação em string do objeto Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Conectando à porta SAM

Agora estamos prontos para estabelecer comunicação com o SAM enviando uma mensagem "Hello". Se você estiver escrevendo uma nova biblioteca SAM, provavelmente deveria ter como alvo, no mínimo, o SAM 3.1, já que ele está disponível tanto no I2P quanto no i2pd e introduz suporte para o parâmetro SIGNATURE_TYPE.

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
Como você pode ver, usamos a função CommandSAM que criamos anteriormente para enviar o comando terminado por quebra de linha `HELLO VERSION MIN=3.0 MAX=3.1 \n`. Isso informa ao SAM que você deseja começar a se comunicar com a API e que você é compatível com o SAM nas versões 3.0 e 3.1. O router, por sua vez, responderá com algo como `HELLO REPLY RESULT=OK VERSION=3.1`, que é uma string que você pode passar para o construtor Reply para obter um objeto Reply válido. De agora em diante, podemos usar nossa função CommandSAM e o objeto Reply para lidar com toda a nossa comunicação por meio da ponte SAM.

Finalmente, vamos adicionar um teste para nossa função "HelloSAM".

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Enviando um comando para o SAM

Agora que você negociou sua conexão com o SAM e concordou sobre uma versão do SAM que ambos suportam, você pode configurar conexões ponto a ponto para que seu aplicativo se conecte a outros aplicativos i2p. Você faz isso enviando o comando "SESSION CREATE" para a SAM Bridge. Para isso, usaremos uma função CreateSession que aceita um ID de sessão e um parâmetro de tipo de destino.

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
Isso foi fácil, certo? Tudo o que tivemos de fazer foi adaptar o padrão que usamos na nossa função HelloSAM para o comando `SESSION CREATE`. Uma boa resposta da ponte ainda retornará OK e, nesse caso, retornamos o ID da conexão SAM recém-criada. Caso contrário, retornamos uma string vazia, porque seria um ID inválido de qualquer forma e falhou, então é fácil de verificar. Vamos ver se esta função funciona escrevendo um teste para ela:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Observe que, neste teste, *devemos* chamar HelloSAM primeiro para estabelecer comunicação com o SAM antes de iniciar nossa sessão. Caso contrário, a ponte responderá com um erro e o teste falhará.

### Analisando uma resposta e criando um objeto Reply.

Agora que você tem sua sessão estabelecida e seu destino local, precisa decidir o que deseja fazer com eles. Sua sessão agora pode ser comandada a se conectar a um serviço remoto via I2P ou a aguardar conexões de entrada para responder. No entanto, antes que você possa se conectar a um destino remoto, talvez seja necessário obter o base64 do destino, que é o que a API espera. Para fazer isso, criaremos uma função LookupName, que retornará o base64 em uma forma utilizável.

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
Novamente, isto é quase o mesmo que as nossas funções HelloSAM e CreateSession, com uma diferença. Como estamos procurando especificamente o VALUE e o campo NAME será igual ao argumento `name`, ele simplesmente retorna a string base64 do destino solicitado.

Agora que temos nossa função LookupName, vamos testá-la:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Enviando "HELLO" ao SAM

Por fim, vamos estabelecer uma conexão com outro serviço usando nossa nova biblioteca. Esta parte me deixou um pouco confuso no começo, mas os desenvolvedores Java mais astutos provavelmente estavam se perguntando por que não estendemos a classe Socket em vez de criar uma variável Socket dentro da classe Jsam. Isso porque, até agora, estávamos nos comunicando com o "Control Socket" e precisamos criar um novo socket para fazer a comunicação de fato. Portanto, esperamos até agora para estender a classe Socket com a classe Jsam:

```java
public class Jsam extends Socket {
```
Além disso, vamos alterar nossa função startConnection para que possamos usá-la para alternar do socket de controle para o socket que usaremos em nossa aplicação. Ela agora aceitará um argumento Socket.

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
Isso nos permite abrir de forma rápida e fácil um novo socket para comunicação, realizar novamente o handshake (negociação inicial) "Hello SAM" e conectar o fluxo.

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
And now you have a new Socket for communicating over SAM! Let's do the same thing for Accepting remote connections:

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
Aí está. É assim que se cria uma biblioteca SAM, passo a passo. No futuro, vou fazer referências cruzadas disto com a versão funcional da biblioteca, Jsam, e com a especificação SAM v3, mas, por ora, preciso tratar de outras tarefas.
