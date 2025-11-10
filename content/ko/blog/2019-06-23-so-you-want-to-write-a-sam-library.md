---
title: "SAM 라이브러리를 개발하고 싶으신가요"
date: 2019-06-23
author: "idk"
description: "SAM 라이브러리를 작성하기 위한 초보자 가이드!"
---

*또는, 스펙을 읽는 것에 그다지 익숙하지 않은 사람들을 위한 [i2p](https://geti2p.net)와 대화하기*

제 생각에 I2P의 가장 훌륭한 기능 중 하나는 SAM API로, 이를 사용하면 I2P와 사용자가 선택한 애플리케이션이나 프로그래밍 언어 사이에 브리지를 구축할 수 있습니다. 현재 다양한 프로그래밍 언어를 위한 수십 개의 SAM 라이브러리가 존재하며, 다음을 포함합니다:

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

이들 언어 중 하나를 사용하고 있다면, 기존 라이브러리를 사용해 이미 애플리케이션을 I2P로 포팅할 수 있을지도 모릅니다. 하지만 이 튜토리얼의 주제는 그것이 아닙니다. 이 튜토리얼은 새로운 언어로 SAM 라이브러리를 만들고자 할 때 무엇을 해야 하는지에 관한 것입니다. 이 튜토리얼에서는 Java로 새로운 SAM 라이브러리를 구현하겠습니다. SAM에 연결하는 Java 라이브러리가 아직 없고, Android에서의 Java 사용, 그리고 거의 모든 사람이 적어도 *조금은* 경험해 본 언어이기 때문에 Java를 선택했습니다. 따라서 여러분이 원하는 언어로도 쉽게 옮겨 구현할 수 있기를 바랍니다.

## 라이브러리 만들기

직접 라이브러리를 구성하는 방법은 사용하려는 언어에 따라 달라집니다. 이 예시 라이브러리에서는 java를 사용할 것이므로 다음과 같이 라이브러리를 만들 수 있습니다:

```sh
mkdir jsam
cd jsam
gradle init --type java-library
```
또는 gradle 5 이상을 사용 중이라면:

```sh
gradle init --type java-library --project-name jsam
```
## 라이브러리 설정

거의 모든 SAM 라이브러리가 관리해야 하는 데이터 항목이 몇 가지 있다. 최소한 사용할 SAM Bridge의 주소와 사용할 서명 유형을 저장해야 한다.

### Storing the SAM address

저는 SAM 주소를 String과 Integer로 나누어 저장하고, 런타임에 함수에서 다시 결합하는 것을 선호합니다.

```java
public String SAMHost = "127.0.0.1";
public int SAMPort = 7656;
public String SAMAddress(){
    return SAMHost + ":" + SAMPort;
}
```
### Storing the Signature Type

I2P Tunnel에 대한 유효한 서명 유형은 DSA_SHA1, ECDSA_SHA256_P256, ECDSA_SHA384_P384, ECDSA_SHA512_P521, EdDSA_SHA512_Ed25519이며, 최소한 SAM 3.1을 구현한다면 기본으로 EdDSA_SHA512_Ed25519를 사용할 것을 강력히 권장합니다. Java에서 'enum'(열거형) 자료구조는 상수의 집합을 담도록 설계되었기 때문에 이 작업에 적합합니다. Java 클래스 정의에 enum과 해당 enum의 인스턴스를 추가하십시오.

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
### Retrieving the signature type:

그것으로 SAM 연결에서 사용 중인 서명 유형을 신뢰성 있게 저장하는 문제는 해결되지만, 브리지에 전달하기 위해서는 여전히 그것을 문자열로 가져와야 한다.

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
테스트하는 것은 중요하니, 몇 가지 테스트를 작성해 봅시다:

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
그 작업이 완료되면 생성자 구현을 시작하세요. 참고로, 지금까지 존재하는 모든 I2P routers의 기본 설정 상황에서 유용하도록 라이브러리에 기본값을 제공해 두었습니다.

```java
public Jsam(String host, int port, SIGNATURE_TYPE sig) {
    SAMHost = host;
    SAMPort = port;
    SigType = sig;
}
```
## Establishing a SAM Connection

마침내, 좋은 부분입니다. SAM bridge와의 상호작용은 SAM bridge의 주소로 "명령"을 보내는 방식으로 이루어지며, 명령의 결과는 문자열 기반의 키-값 쌍 집합으로 파싱할 수 있습니다. 그러니 이를 염두에 두고, 앞서 정의한 SAM Address에 대한 읽기-쓰기 연결을 설정한 다음, "CommandSAM" 함수와 응답 파서를 작성해 봅시다.

### 서명 유형 저장

우리는 소켓을 통해 SAM과 통신하므로, 소켓에 연결하고 소켓에서 읽고 소켓에 쓰기 위해서는 Jsam 클래스에 다음의 private 변수를 선언해야 합니다:

```java
private Socket socket;
private PrintWriter writer;
private BufferedReader reader;
```
또한 그런 변수들을 생성자에서 초기화하기 위해 이를 수행하는 함수를 만드는 것이 좋습니다.

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
### 서명 유형 가져오기:

이제 SAM과 드디어 통신을 시작할 모든 준비가 되었습니다. 정리를 깔끔하게 하기 위해, 개행 문자로 종료되는 단일 명령을 SAM에 보내고 다음 단계에서 만들 Reply 객체를 반환하는 함수를 만들어 봅시다:

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
이전 단계에서 소켓에서 생성한 writer와 reader를 소켓에 대한 입력과 출력으로 사용하고 있다는 점에 유의하세요. reader로부터 응답을 받으면, 해당 문자열을 Reply 생성자에 전달하고, 그 생성자가 이를 파싱하여 Reply 객체를 반환합니다.

### Parsing a reply and creating a Reply object.

응답을 보다 쉽게 처리하기 위해, SAM bridge(SAM 브리지)에서 받는 결과를 자동으로 파싱하는 Reply 객체를 사용하겠습니다. Reply 객체는 최소한 topic, type, result를 가지며, 추가로 임의 개수의 키-값 쌍을 포함할 수 있습니다.

```java
public class Reply {
    String topic;
    String type;
    REPLY_TYPES result;
    Map<String, String> replyMap = new HashMap<String, String>();
```
보시다시피 우리는 "result"를 enum인 REPLY_TYPES로 저장할 것입니다. 이 enum에는 SAM bridge가 응답할 수 있는 가능한 모든 응답 결과가 포함되어 있습니다.

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
이제 소켓에서 받은 응답 문자열을 매개변수로 받아 파싱하고, 그 정보를 사용해 응답 객체를 설정하는 생성자를 만들어 봅시다. 응답은 공백으로 구분되며, 키-값 쌍은 등호(=)로 연결되고 개행 문자로 종료됩니다.

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
마지막으로, 편의를 위해 reply 객체에 Reply 객체의 문자열 표현을 반환하는 toString() 메서드를 추가합시다.

```java
public String toString() {
    return topic + " " + type + " " + REPLY_TYPES.get(result) + " " + replyMap.toString();
}
}
```
### SAM 포트에 연결하기

이제 "Hello" 메시지를 보내 SAM과 통신을 설정할 준비가 되었습니다. 새 SAM 라이브러리를 작성 중이라면, I2P와 i2pd 모두에서 사용 가능하며 SIGNATURE_TYPE 매개변수 지원이 도입된 최소한 SAM 3.1을 대상으로 하는 것이 좋습니다.

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
보시다시피, 앞에서 만든 CommandSAM 함수로 개행 문자로 끝나는 명령 `HELLO VERSION MIN=3.0 MAX=3.1 \n`을 보냅니다. 이는 SAM에게 API와의 통신을 시작하려 하며 SAM 3.0과 3.1 버전을 지원한다는 것을 알립니다. 이에 대해 router는 `HELLO REPLY RESULT=OK VERSION=3.1` 같은 응답을 보내는데, 이는 Reply 생성자에 전달하여 유효한 Reply 객체를 얻을 수 있는 문자열입니다. 이제부터는 SAM bridge를 통한 모든 통신을 처리하기 위해 CommandSAM 함수와 Reply 객체를 사용할 수 있습니다.

마지막으로, "HelloSAM" 함수에 대한 테스트를 추가해 봅시다.

```java
@Test public void testHelloSAM() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
}
```
### SAM에 명령 보내기

이제 SAM과의 연결을 협상하고 양측이 사용하는 SAM 버전에 합의했으므로, 애플리케이션이 다른 i2p 애플리케이션에 연결할 수 있도록 피어 투 피어(P2P) 연결을 설정할 수 있습니다. 이는 SAM Bridge에 "SESSION CREATE" 명령을 보내 수행합니다. 이를 위해 세션 ID와 destination type 매개변수를 받는 CreateSession 함수를 사용하겠습니다.

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
생각보다 간단했죠? 우리가 해야 했던 건 HelloSAM 함수에서 사용했던 패턴을 `SESSION CREATE` 명령에 맞게 적용하는 것뿐입니다. 브리지로부터의 정상 응답은 여전히 OK를 반환하며, 그 경우 새로 생성된 SAM 연결의 ID를 반환합니다. 그렇지 않다면 실패한 것이므로 어차피 유효한 ID가 아니기에 빈 문자열을 반환합니다. 덕분에 검사하기가 쉽습니다. 이제 이 함수가 제대로 동작하는지 테스트를 작성해 확인해 봅시다:

```java
@Test public void testCreateSession() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("test", classUnderTest.CreateSession("test", ""));
}
```
이 테스트에서는 세션을 시작하기 전에 SAM과의 통신을 설정하기 위해 먼저 HelloSAM을 *반드시* 호출해야 합니다. 그렇지 않으면 브리지가 오류로 응답하고 테스트가 실패합니다.

### 응답을 파싱하고 Reply 객체를 생성하기.

이제 세션이 설정되었고 로컬 destination(목적지)도 준비되었으니, 이를 가지고 무엇을 할지 결정해야 합니다. 이제 세션에 I2P를 통해 원격 서비스에 연결하라고 지시할 수도 있고, 들어오는 연결을 기다렸다가 응답하도록 할 수도 있습니다. 그러나 원격 destination에 연결하기 전에, API가 기대하는 형식인 해당 destination의 base64를 확보해야 할 수도 있습니다. 이를 위해 사용 가능한 형태로 base64를 반환하는 LookupName 함수를 만들겠습니다.

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
다시 한번, 이것은 우리의 HelloSAM 및 CreateSession 함수와 거의 동일하지만 한 가지 차이가 있습니다. 우리는 VALUE를 특정해서 찾고 있고 NAME 필드는 `name` 인자와 동일하므로, 요청된 destination(목적지)의 base64 문자열만을 반환합니다.

이제 LookupName 함수를 만들었으니, 테스트해 봅시다:

```java
@Test public void testLookupName() {
    Jsam classUnderTest = new Jsam();
    assertTrue("HelloSAM should return 'true' in the presence of an alive SAM bridge", classUnderTest.HelloSAM());
    assertEquals("8ZAW~KzGFMUEj0pdchy6GQOOZbuzbqpWtiApEj8LHy2~O~58XKxRrA43cA23a9oDpNZDqWhRWEtehSnX5NoCwJcXWWdO1ksKEUim6cQLP-VpQyuZTIIqwSADwgoe6ikxZG0NGvy5FijgxF4EW9zg39nhUNKRejYNHhOBZKIX38qYyXoB8XCVJybKg89aMMPsCT884F0CLBKbHeYhpYGmhE4YW~aV21c5pebivvxeJPWuTBAOmYxAIgJE3fFU-fucQn9YyGUFa8F3t-0Vco-9qVNSEWfgrdXOdKT6orr3sfssiKo3ybRWdTpxycZ6wB4qHWgTSU5A-gOA3ACTCMZBsASN3W5cz6GRZCspQ0HNu~R~nJ8V06Mmw~iVYOu5lDvipmG6-dJky6XRxCedczxMM1GWFoieQ8Ysfuxq-j8keEtaYmyUQme6TcviCEvQsxyVirr~dTC-F8aZ~y2AlG5IJz5KD02nO6TRkI2fgjHhv9OZ9nskh-I2jxAzFP6Is1kyAAAA", classUnderTest.LookupName("i2p-projekt.i2p"));
}
```
### SAM에게 "HELLO" 보내기

마침내, 새 라이브러리를 사용해 다른 서비스에 연결을 설정해 보겠습니다. 처음에는 이 부분이 다소 혼란스러웠지만, 가장 예리한 Java 개발자라면 왜 Jsam 클래스 내부에 Socket 변수를 만드는 대신 Socket 클래스를 상속하지 않았는지 궁금했을 겁니다. 이는 지금까지 우리가 "Control Socket"과만 통신해 왔고, 실제 통신을 수행하려면 새 소켓을 만들어야 하기 때문입니다. 그래서 Jsam 클래스가 Socket 클래스를 상속하도록 하는 일은 지금까지 미뤄 두었습니다:

```java
public class Jsam extends Socket {
```
또한, 제어 소켓에서 애플리케이션에서 사용할 소켓으로 전환할 수 있도록 startConnection 함수를 수정합시다. 이제 이 함수는 Socket 인자를 받습니다.

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
이를 통해 통신에 사용할 새 소켓을 빠르고 쉽게 열고, "Hello SAM" 핸드셰이크를 다시 수행한 다음 스트림을 연결할 수 있습니다.

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
이제 SAM을 통해 통신하기 위한 새 소켓이 생겼습니다! 원격 연결 수락도 같은 방식으로 해봅시다:

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
이상입니다. SAM 라이브러리를 단계별로 구축하는 방법은 위와 같습니다. 앞으로는 이 내용을 라이브러리의 실제 작동 버전인 Jsam 및 SAM v3 사양과 교차 참조할 예정이지만, 지금은 다른 작업들을 먼저 처리해야 합니다.
