---
title: "Python과 I2P를 활용한 프라이버시를 고려한 애플리케이션 개발"
date: 2018-10-23
author: "villain"
description: "Python을 사용한 I2P 애플리케이션 개발의 기본 개념"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P)는 프라이버시를 중시하는 애플리케이션을 개발하기 위한 프레임워크를 제공합니다. 이는 일반 인터넷 위에서 작동하는 가상 네트워크로, 호스트는 자신의 "실제" IP 주소를 공개하지 않고 데이터를 교환할 수 있습니다. I2P 네트워크 내부의 연결은 *I2P destinations*(I2P에서 사용하는 가상 목적지 주소)라고 불리는 가상 주소들 사이에서 설정됩니다. 필요에 따라 destination을 원하는 만큼 보유할 수 있으며, 심지어 각 연결마다 새로운 destination을 사용할 수도 있습니다. 이러한 destination은 상대방에게 실제 IP 주소에 관한 어떠한 정보도 공개하지 않습니다.

이 문서는 I2P 애플리케이션을 개발할 때 알아야 하는 기본 개념을 설명합니다.
코드 예시는 내장 비동기 프레임워크인 asyncio를 사용하여 Python으로 작성되었습니다.

## SAM API 활성화 및 i2plib 설치

I2P는 클라이언트 애플리케이션을 위해 다양한 API를 제공합니다. 일반적인 클라이언트-서버 앱은 I2PTunnel, HTTP 및 Socks 프록시를 사용할 수 있으며, Java 애플리케이션은 보통 I2CP를 사용합니다. Python과 같은 다른 언어로 개발할 때는 [SAM](/docs/api/samv3/)이 가장 좋은 선택입니다. 원래의 Java 클라이언트 구현에서는 SAM이 기본적으로 비활성화되어 있으므로 이를 활성화해야 합니다. Router Console의 "I2P internals" -> "Clients" 페이지로 이동하세요. "Run at Startup"에 체크하고 "Start"를 누른 다음 "Save Client Configuration"을 클릭하세요.

![SAM API 활성화](https://geti2p.net/images/enable-sam.jpeg)

[C++ 구현체 i2pd](https://i2pd.website)는 기본적으로 SAM이 활성화되어 있습니다.

저는 SAM API(I2P 애플리케이션 연동용 API)를 위한 유용한 Python 라이브러리 [i2plib](https://github.com/l-n-s/i2plib)을 개발했습니다. pip로 설치하거나 GitHub에서 소스 코드를 수동으로 다운로드할 수 있습니다.

```bash
pip install i2plib
```
이 라이브러리는 Python에 내장된 [비동기 프레임워크 asyncio](https://docs.python.org/3/library/asyncio.html)와 함께 동작하므로, 코드 예제가 이벤트 루프 안에서 실행되는 비동기 함수(코루틴)에서 가져온 것임을 유의하세요. i2plib 사용에 대한 추가 예시는 [소스 코드 저장소](https://github.com/l-n-s/i2plib/tree/master/docs/examples)에서 확인할 수 있습니다.

## I2P Destination(목적지) 및 세션 생성

I2P 목적지(destination)는 말 그대로 암호화 키와 암호학적 서명 키로 이루어진 집합이다. 이 집합에 속한 공개 키는 I2P 네트워크에 공개되며 IP 주소 대신 연결을 설정하는 데 사용된다.

다음은 [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination)을 생성하는 방법입니다:

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
base32 주소는 네트워크에서 다른 피어들이 귀하의 전체 Destination(목적지)을 발견하는 데 사용되는 해시입니다. 이 Destination을 프로그램에서 영구 주소로 사용할 계획이라면, *dest.private_key.data*의 바이너리 데이터를 로컬 파일로 저장하십시오.

이제 SAM 세션을 생성할 수 있으며, 이는 문자 그대로 I2P에서 Destination(목적지 식별자)를 온라인 상태로 만드는 것을 의미합니다:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
여기서 중요한 참고 사항: *session_writer* 소켓이 열린 상태로 유지되는 동안 Destination(목적지)은 온라인 상태로 유지됩니다. 이를 끄고 싶다면 *session_writer.close()*를 호출할 수 있습니다.

## 아웃바운드 연결 생성

이제 Destination(목적지)가 온라인 상태일 때, 이를 사용하여 다른 피어에 연결할 수 있습니다. 예를 들어, 다음은 "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"에 연결한 다음 HTTP GET 요청을 보내고 응답을 읽는 방법입니다(이는 "i2p-projekt.i2p" 웹 서버입니다):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## 수신 연결 허용

아웃바운드 연결을 만드는 것은 간단하지만, 연결을 수락할 때는 한 가지 중요한 사항이 있습니다. 새 클라이언트가 연결되면 SAM API는 base64로 인코딩된 클라이언트의 Destination(I2P 목적지 식별자)을 담은 ASCII 문자열을 소켓으로 보냅니다. Destination과 데이터가 하나의 청크로 함께 도착할 수 있으므로, 이 점을 염두에 두어야 합니다.

간단한 PING-PONG 서버는 다음과 같습니다. 들어오는 연결을 수락하고, 클라이언트의 Destination을 *remote_destination* 변수에 저장한 뒤, "PONG" 문자열을 되돌려 보냅니다:

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## 자세한 정보

이 문서는 TCP와 유사한 스트리밍 프로토콜의 사용 방법을 설명합니다. SAM API는 데이터그램을 송수신하기 위한 UDP와 유사한 프로토콜도 제공합니다. 이 기능은 추후 i2plib에 추가될 예정입니다.

이것은 기본 정보에 불과하지만, I2P를 사용해 자신만의 프로젝트를 시작하기에는 충분합니다. Invisible Internet은 모든 종류의 프라이버시를 고려한 애플리케이션을 개발하는 데 훌륭한 도구입니다. 네트워크가 설계 제약을 강요하지 않으므로, 이러한 애플리케이션은 클라이언트-서버뿐만 아니라 P2P 방식으로도 구현할 수 있습니다.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
