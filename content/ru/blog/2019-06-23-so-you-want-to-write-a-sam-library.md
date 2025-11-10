---
title: "Итак, вы хотите написать SAM-библиотеку"
date: 2019-06-23
author: "idk"
description: "Руководство для начинающих по написанию библиотеки SAM!"
---

*Или, о взаимодействии с [i2p](https://geti2p.net) для тех, кто не особенно привык читать спецификации*

Одной из лучших возможностей I2P, на мой взгляд, является его SAM API (API для взаимодействия приложений с I2P), который можно использовать для создания моста между I2P и вашим приложением или выбранным вами языком программирования. В настоящее время существуют десятки библиотек SAM для самых разных языков, включая:

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

Если вы используете любой из этих языков, возможно, вы уже сможете портировать своё приложение под I2P, воспользовавшись существующей библиотекой. Однако это руководство не об этом. Это руководство о том, что делать, если вы хотите создать библиотеку SAM на новом языке. В этом руководстве я реализую новую библиотеку SAM на Java. Я выбрал Java, потому что пока нет Java‑библиотеки, которая подключает к SAM, потому что Java используется в Android, а также потому, что это язык, с которым почти у всех есть хотя бы *небольшой* опыт, так что, возможно, вы сможете перенести это на язык по вашему выбору.

## Создание собственной библиотеки

То, как вы настроите собственную библиотеку, будет различаться в зависимости от языка, который вы хотите использовать. В этом примере мы будем использовать Java, поэтому библиотеку можно создать следующим образом:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
Или, если вы используете gradle 5 или новее:

```sh
gradle init --type java-library --project-name jsam
```
## Настройка библиотеки

Есть несколько параметров, которые почти любая библиотека SAM, скорее всего, должна уметь обрабатывать. По крайней мере, ей потребуется хранить адрес SAM Bridge, который вы собираетесь использовать, и тип подписи, который вы хотите применить.

### Storing the SAM address

Я предпочитаю хранить адрес SAM как строку и целое число и затем снова объединять их в функции во время выполнения.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

Допустимые типы подписи для I2P tunnel: DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519, однако настоятельно рекомендуется использовать по умолчанию EdDSA_SHA512_Ed25519, если вы реализуете как минимум SAM 3.1. В Java структура данных 'enum' хорошо подходит для этой задачи, поскольку она предназначена для хранения набора констант. Добавьте enum и экземпляр enum в определение вашего класса Java.

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
### Сохранение адреса SAM

Это обеспечивает надёжное сохранение типа подписи, используемого соединением SAM, но вам всё ещё нужно извлечь его в виде строки, чтобы передать мосту.

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
Важно проводить тестирование, поэтому давайте напишем несколько тестов:

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
Когда это будет сделано, приступайте к созданию своего конструктора. Обратите внимание, что мы задали в нашей библиотеке значения по умолчанию, которые будут полезны в типичных сценариях на всех существующих I2P routers на данный момент.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

Наконец-то самое интересное. Взаимодействие с мостом SAM осуществляется отправкой "команды" на адрес моста SAM, а результат команды можно разобрать как набор строковых пар ключ-значение. Имея это в виду, давайте установим соединение для чтения и записи с SAM Address, который мы определили ранее, затем напишем функцию "CommandSAM" и парсер ответа.

### Хранение типа подписи

Мы обмениваемся данными с SAM через сокет, поэтому, чтобы подключаться к сокету, читать из него и записывать в него, вам необходимо создать следующие приватные переменные в классе Jsam:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
Вам также следует инициализировать эти переменные в ваших конструкторах, создав для этого функцию.

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
### Получение типа подписи:

Теперь всё готово, чтобы наконец начать общаться с SAM. Чтобы всё было аккуратно организовано, давайте создадим функцию, которая отправляет одну команду в SAM, завершаемую символом новой строки, и возвращает объект Reply, который мы создадим на следующем шаге:

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
Обратите внимание, что мы используем writer и reader, созданные из сокета на предыдущем шаге, в качестве ввода и вывода сокета. Когда мы получаем ответ от reader, мы передаём строку в конструктор Reply, который разбирает её и возвращает объект Reply.

### Parsing a reply and creating a Reply object.

Чтобы упростить обработку ответов, мы будем использовать объект Reply, который автоматически разбирает результаты, полученные от SAM bridge. У ответа как минимум есть тема, тип и результат, а также произвольное число пар ключ–значение.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
Как видите, мы будем хранить "result" как перечисление REPLY_TYPES. Это перечисление содержит все возможные варианты ответов, которые может вернуть SAM bridge (мост SAM).

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
Теперь создадим наш конструктор, который принимает в качестве параметра строку ответа, полученную из сокета, разбирает её и использует эту информацию для настройки объекта ответа. Ответ разделён пробелами, пары ключ–значение соединены знаком равенства и завершается переводом строки.

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
Наконец, для удобства добавим объекту Reply функцию toString(), которая возвращает строковое представление объекта Reply.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### Подключение к порту SAM

Теперь мы готовы установить связь с SAM, отправив сообщение «Hello». Если вы пишете новую библиотеку SAM, вам, вероятно, следует ориентироваться как минимум на SAM 3.1, так как он доступен и в I2P, и в i2pd и вводит поддержку параметра SIGNATURE_TYPE.

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
Как вы видите, мы используем созданную ранее функцию CommandSAM, чтобы отправить команду с завершающим переводом строки `HELLO VERSION MIN=3.0 MAX=3.1 \n`. Это сообщает SAM, что вы хотите начать взаимодействие с API и что вы умеете работать с SAM версий 3.0 и 3.1. router, в свою очередь, ответит примерно так `HELLO REPLY RESULT=OK VERSION=3.1`, это строка, которую можно передать конструктору Reply, чтобы получить валидный объект Reply. С этого момента мы можем использовать нашу функцию CommandSAM и объект Reply, чтобы осуществлять всё взаимодействие через SAM bridge (мост SAM).

Наконец, добавим тест для нашей функции "HelloSAM".

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### Отправка команды в SAM

Теперь, когда вы согласовали соединение с SAM и договорились о версии SAM, которая поддерживается обеими сторонами, вы можете настроить одноранговые соединения для вашего приложения, чтобы подключаться к другим приложениям i2p. Это делается путем отправки команды "SESSION CREATE" на SAM Bridge (мост SAM). Для этого мы воспользуемся функцией CreateSession, которая принимает идентификатор сеанса и параметр типа назначения.

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
Это было нетрудно, правда? Всё, что нам нужно было сделать, — адаптировать шаблон, использованный в нашей функции HelloSAM, к команде `SESSION CREATE`. Корректный ответ от SAM bridge (SAM‑моста) по-прежнему вернёт OK, и в этом случае мы возвращаем ID только что созданного SAM‑соединения. В противном случае мы возвращаем пустую строку, потому что это всё равно недопустимый идентификатор и операция провалилась, так что проверять легко. Давайте проверим, работает ли эта функция, написав для неё тест:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
Обратите внимание, что в этом тесте мы *обязательно* должны сначала вызвать HelloSAM, чтобы установить связь с SAM перед началом сеанса. В противном случае SAM‑мост ответит ошибкой, и тест завершится неудачей.

### Разбор ответа и создание объекта Reply.

Теперь у вас установлен сеанс и локальный Destination (адрес назначения); нужно решить, что вы хотите с ними сделать. Теперь можно дать вашему сеансу команду подключиться к удалённому сервису через I2P или ждать входящих соединений, чтобы на них отвечать. Однако, прежде чем вы сможете подключиться к удалённому Destination, возможно, вам понадобится получить base64 этого Destination, именно его ожидает API. Чтобы это сделать, мы создадим функцию LookupName, которая вернёт base64 в пригодном для использования виде.

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
Снова, это почти то же самое, что и наши функции HelloSAM и CreateSession, с одним отличием. Поскольку нас интересует именно поле VALUE, а поле NAME будет совпадать с аргументом `name`, она просто возвращает base64-строку запрошенного назначения.

Теперь, когда у нас есть функция LookupName, давайте её протестируем:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### Скажем "HELLO" SAM

Наконец мы собираемся установить соединение с другим сервисом с помощью нашей новой библиотеки. Эта часть поначалу немного сбивала меня с толку, но самые проницательные разработчики на Java, вероятно, уже задавались вопросом, почему мы не расширили класс Socket, вместо того чтобы создавать переменную Socket внутри класса Jsam. Дело в том, что до сих пор мы общались через "Control Socket", а для реального обмена данными нам нужно создать новый сокет. Поэтому мы откладывали расширение класса Socket классом Jsam до настоящего момента:

```java
public class Jsam extends Socket {
```
Также изменим функцию startConnection, чтобы мы могли использовать её для переключения с управляющего сокета на сокет, который мы будем использовать в нашем приложении. Теперь она будет принимать аргумент типа Socket.

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
Это позволяет нам быстро и легко открыть новый сокет для обмена данными, снова выполнить рукопожатие "Hello SAM" и подключить поток.

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
И теперь у вас есть новый сокет для обмена данными через SAM! Давайте сделаем то же самое для приёма удалённых подключений:

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
Вот и всё. Так, шаг за шагом, создаётся библиотека SAM. В будущем я сверю это с рабочей версией библиотеки Jsam и спецификацией SAM v3, но пока мне нужно заняться другими делами.
