---
title: "I2P 다운로드"
description: "Windows, macOS, Linux, Android 등에서 사용할 수 있는 최신 버전의 I2P를 다운로드하세요."
type: "다운로드"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: I2P는 익명성을 제공하는 네트워크 레이어로, 사용자가 인터넷을 보다 안전하게 탐색할 수 있도록 돕습니다. I2P는 다양한 애플리케이션과 함께 작동하며, 익명성을 유지하기 위해 트래픽을 암호화하고 여러 노드를 통해 라우팅합니다.

## I2P의 주요 구성 요소

- **Router**: I2P 네트워크에 연결하고 트래픽을 라우팅하는 소프트웨어입니다.
- **Tunnel**: 데이터가 네트워크를 통해 이동하는 경로입니다. 각 터널은 단방향이며, 송신과 수신을 위해 별도의 터널이 필요합니다.
- **LeaseSet**: I2P 네트워크에서 특정 목적지에 대한 정보를 포함하는 데이터 구조입니다.
- **netDb**: 네트워크 데이터베이스로, I2P 네트워크의 노드 정보를 저장합니다.

## 시작하기

I2P를 설치하려면, [공식 다운로드 페이지](https://geti2p.net/en/download)에서 최신 버전을 다운로드하십시오. 설치가 완료되면, I2P 콘솔에 접근하여 설정을 구성할 수 있습니다.

```bash
java -jar i2pinstall_1.9.0.jar
```

설치 후, 웹 브라우저에서 `http://127.0.0.1:7657`을 열어 I2P 콘솔에 접근하십시오. 여기서 네트워크 설정을 조정하고, 터널을 관리할 수 있습니다.

I2P는 다양한 프로토콜을 지원하며, SAMv3와 I2PTunnel을 통해 애플리케이션과 통합할 수 있습니다. 이를 통해 익명성을 유지하면서도 다양한 인터넷 서비스를 사용할 수 있습니다.
windows: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷을 탐색하거나, 파일을 공유하거나, 메시지를 익명으로 전송할 수 있습니다. I2P는 `garlic encryption`을 사용하여 데이터의 보안을 강화합니다. 

## I2P의 주요 구성 요소

1. **Router**: I2P 네트워크의 핵심으로, 데이터 패킷을 전송하고 수신합니다.
2. **Tunnel**: 데이터가 네트워크를 통해 이동하는 경로입니다.
3. **leaseSet**: I2P 네트워크에서 서비스의 위치를 나타내는 데이터 구조입니다.
4. **netDb**: 네트워크 데이터베이스로, I2P 네트워크의 라우터 정보를 저장합니다.
5. **floodfill**: netDb에 정보를 전파하는 라우터입니다.

I2P는 `NTCP2`와 `SSU` 프로토콜을 사용하여 라우터 간의 통신을 관리합니다. `SAMv3` 인터페이스는 외부 애플리케이션이 I2P 네트워크와 상호 작용할 수 있도록 지원합니다. `I2PTunnel`은 트래픽을 I2P 네트워크로 라우팅하는 데 사용됩니다. 

I2P는 강력한 익명성을 제공하며, `eepsite`를 통해 익명 웹사이트를 호스팅할 수 있습니다.
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "Java 필요"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: I2P는 사용자의 인터넷 활동을 익명화하는 데 중점을 둔 네트워크입니다. I2P 네트워크는 여러 레이어의 암호화를 사용하여 데이터를 보호하며, 각 메시지는 여러 개의 "터널"을 통해 전송됩니다. 이러한 터널은 I2P 라우터에 의해 동적으로 생성되고 관리됩니다.

I2P는 다음과 같은 주요 구성 요소로 구성됩니다:

- **라우터**: I2P 네트워크의 핵심 요소로, 데이터 패킷을 전송하고 수신합니다.
- **터널**: 데이터가 네트워크를 통해 이동하는 경로입니다. 각 터널은 송신 및 수신을 위한 별도의 경로를 가집니다.
- **leaseSet**: 네트워크에서 특정 목적지에 대한 정보를 포함하는 데이터 구조입니다.
- **netDb**: 네트워크 데이터베이스로, I2P 네트워크의 라우터 및 목적지 정보를 저장합니다.
- **floodfill**: netDb의 데이터를 다른 라우터에 전파하는 특수한 라우터입니다.

I2P는 NTCP2 및 SSU 프로토콜을 사용하여 라우터 간의 통신을 처리합니다. 이러한 프로토콜은 네트워크의 보안과 효율성을 보장합니다.

I2P를 통해 사용자는 익명으로 웹사이트를 호스팅할 수 있으며, 이를 "eepsite"라고 부릅니다. 또한, SAMv3 인터페이스를 통해 외부 애플리케이션이 I2P 네트워크와 상호작용할 수 있습니다.

I2PTunnel은 사용자가 I2P 네트워크를 통해 트래픽을 라우팅할 수 있도록 지원하는 도구입니다. I2CP 및 I2NP 프로토콜을 사용하여 라우터와 통신합니다.

I2P는 강력한 익명성을 제공하며, 사용자 프라이버시를 보호하는 데 중점을 둔 다양한 기능을 제공합니다.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: 다음은 I2P 네트워크에서의 기본적인 데이터 흐름입니다:

1. **I2P Router**: I2P 라우터는 네트워크의 핵심 구성 요소로, 데이터 패킷을 다른 라우터로 전달합니다. 라우터는 NTCP2 및 SSU 프로토콜을 사용하여 서로 통신합니다.

2. **Tunnels**: 터널은 데이터가 네트워크를 통해 이동하는 경로입니다. 각 I2P 라우터는 여러 개의 터널을 설정하여 데이터를 전송하고 수신합니다.

3. **LeaseSets**: leaseSet은 터널의 끝점을 설명하는 데이터 구조입니다. 이는 다른 라우터가 데이터를 올바른 목적지로 라우팅할 수 있도록 돕습니다.

4. **Network Database (netDb)**: 네트워크 데이터베이스는 I2P 네트워크의 분산된 데이터 저장소로, 라우터 정보와 leaseSet을 저장합니다. floodfill 라우터는 이 데이터베이스를 유지 관리합니다.

5. **Garlic Encryption**: I2P는 garlic encryption을 사용하여 데이터의 보안을 강화합니다. 이는 여러 메시지를 하나의 암호화된 패킷으로 결합하여 전송하는 방식입니다.
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "Java 불필요 - Java 런타임 포함"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: 참
links: I2P는 익명성을 제공하는 네트워크 레이어로, 사용자가 인터넷을 통해 안전하게 통신할 수 있도록 설계되었습니다. I2P는 다양한 프로토콜을 지원하며, 사용자는 `I2PTunnel`을 통해 웹사이트를 호스팅하거나, `SAMv3` 인터페이스를 사용하여 애플리케이션을 개발할 수 있습니다. 

I2P의 주요 구성 요소는 다음과 같습니다:

- **Router**: I2P 네트워크에 연결하고 데이터를 전송하는 소프트웨어
- **Tunnel**: 익명성을 유지하며 데이터를 전송하는 경로
- **LeaseSet**: 네트워크에서 목적지의 위치 정보를 포함하는 데이터 구조
- **NetDb**: 네트워크 데이터베이스로, I2P 네트워크의 라우터 및 목적지 정보를 저장

I2P는 `garlic encryption`(마늘 암호화)을 사용하여 데이터의 보안을 강화하며, `NTCP2` 및 `SSU` 프로토콜을 통해 라우터 간의 통신을 관리합니다. 

자세한 정보는 [I2P 공식 웹사이트](https://geti2p.net)를 참조하세요.
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: I2P는 익명성을 제공하는 네트워크 레이어로, 사용자가 인터넷 상에서 프라이버시를 보호할 수 있도록 설계되었습니다. I2P 네트워크는 다양한 애플리케이션을 지원하며, 사용자는 이를 통해 안전하게 통신할 수 있습니다.

## I2P의 주요 기능

- **익명성**: I2P는 사용자의 IP 주소를 숨기고, 트래픽을 암호화하여 프라이버시를 보호합니다.
- **분산형 네트워크**: I2P는 중앙 서버 없이 작동하며, 네트워크 참여자들이 서로 정보를 공유합니다.
- **다양한 프로토콜 지원**: I2P는 HTTP, SMTP, IRC 등 다양한 프로토콜을 지원하여 다양한 애플리케이션과의 호환성을 제공합니다.

## 시작하기

I2P를 사용하려면, 먼저 I2P 소프트웨어를 다운로드하고 설치해야 합니다. 설치가 완료되면, I2P 콘솔에 접속하여 네트워크 설정을 구성할 수 있습니다. I2P 콘솔은 웹 기반 인터페이스로, 사용자가 네트워크 상태를 모니터링하고 설정을 조정할 수 있도록 도와줍니다.

## I2P의 구성 요소

- **Router**: I2P 네트워크의 핵심 구성 요소로, 트래픽을 라우팅하고 네트워크 참여자 간의 연결을 관리합니다.
- **Tunnel**: 데이터를 전송하기 위한 경로로, 익명성을 유지하기 위해 여러 노드를 통해 트래픽을 전달합니다.
- **LeaseSet**: I2P 네트워크에서 목적지 정보를 포함하는 데이터 구조로, 트래픽을 올바른 목적지로 라우팅하는 데 사용됩니다.

I2P는 지속적으로 발전하고 있으며, 커뮤니티의 기여를 통해 더욱 안전하고 효율적인 네트워크로 성장하고 있습니다.
file: "i2pinstall_2.10.0.jar"
size: "~30M"
requirements: "Java 8 이상"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷 상에서 자신의 신원을 숨기고 안전하게 통신할 수 있습니다. I2P는 다양한 애플리케이션을 지원하며, 웹 브라우징, 파일 공유, 이메일 전송 등을 포함합니다.

## I2P의 주요 구성 요소

- **Router**: I2P 네트워크의 핵심 구성 요소로, 데이터 패킷을 다른 라우터로 전달합니다.
- **Tunnel**: 데이터가 익명으로 전송되는 경로입니다. 각 사용자는 송신 및 수신 터널을 설정합니다.
- **LeaseSet**: 터널의 엔드포인트 정보를 포함하는 데이터 구조입니다.
- **NetDb**: 네트워크 데이터베이스로, 라우터와 터널 정보를 저장합니다.
- **Floodfill**: 네트워크 데이터베이스를 유지하고 업데이트하는 특별한 라우터입니다.

## I2P의 작동 방식

I2P는 "garlic encryption"을 사용하여 데이터를 보호합니다. 이는 여러 메시지를 하나의 암호화된 패킷으로 결합하여 보안을 강화합니다. I2P는 또한 NTCP2 및 SSU 프로토콜을 사용하여 라우터 간의 안전한 연결을 설정합니다.

## 시작하기

I2P를 설치하려면 [공식 다운로드 페이지](https://geti2p.net/en/download)에서 최신 버전을 다운로드하십시오. 설치 후, I2P는 자동으로 시작되며, 로컬 웹 인터페이스를 통해 구성할 수 있습니다. I2P의 다양한 기능을 활용하려면, SAMv3 및 I2PTunnel과 같은 도구를 사용할 수 있습니다.

## 추가 리소스

- [I2P 공식 문서](https://geti2p.net/en/docs)
- [I2P 커뮤니티 포럼](https://geti2p.net/en/forums)
- [I2P 개발자 가이드](https://geti2p.net/en/developer)
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷 상에서 안전하게 통신할 수 있습니다. I2P는 여러 기술을 사용하여 사용자의 위치와 신원을 숨깁니다. 이러한 기술에는 garlic encryption과 같은 고급 암호화 방법이 포함됩니다.

I2P 네트워크는 여러 구성 요소로 이루어져 있습니다. 주요 구성 요소로는 router, tunnel, leaseSet, netDb, floodfill 등이 있습니다. 이들은 모두 사용자의 익명성을 보장하기 위해 협력합니다.

I2P는 NTCP2 및 SSU 프로토콜을 사용하여 데이터를 전송합니다. 이러한 프로토콜은 데이터의 무결성과 기밀성을 유지하는 데 중요한 역할을 합니다. 사용자는 I2PTunnel을 통해 웹사이트에 액세스하거나 SAMv3 인터페이스를 사용하여 애플리케이션을 I2P 네트워크에 연결할 수 있습니다.

I2P는 또한 I2CP 및 I2NP 프로토콜을 사용하여 내부 통신을 관리합니다. 이러한 프로토콜은 I2P 네트워크 내에서 메시지를 라우팅하고 전달하는 데 필수적입니다.

I2P를 사용하여 eepsite를 호스팅할 수 있으며, 이는 사용자가 익명으로 웹사이트를 운영할 수 있도록 합니다. I2P는 개인 정보 보호와 보안을 중시하는 사용자에게 강력한 도구를 제공합니다.
file: "i2psource_2.10.0.tar.bz2"
size: "~3천3백만"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷에서 개인 정보를 보호하면서 안전하게 통신할 수 있습니다. I2P는 여러 가지 프로토콜을 지원하며, 사용자는 `I2PTunnel`을 사용하여 웹사이트를 호스팅하거나, `SAMv3` 인터페이스를 통해 애플리케이션을 개발할 수 있습니다.

I2P의 주요 구성 요소는 다음과 같습니다:

- **Router**: 네트워크의 핵심 역할을 하며, 메시지를 다른 I2P 노드로 전달합니다.
- **Tunnel**: 메시지를 익명으로 전송하기 위해 사용되는 경로입니다.
- **LeaseSet**: 네트워크에서의 익명 주소를 설명하는 데이터 구조입니다.
- **netDb**: I2P 네트워크의 분산 데이터베이스로, 노드 정보를 저장합니다.
- **Floodfill**: netDb의 데이터를 다른 노드에 전파하는 특별한 라우터입니다.

I2P는 `NTCP2`와 `SSU` 프로토콜을 사용하여 네트워크 연결을 관리합니다. 이러한 프로토콜은 각각 TCP와 UDP 기반의 통신을 지원합니다. I2P의 보안은 `garlic encryption`을 통해 강화됩니다. 이는 메시지를 여러 계층으로 암호화하여 전송하는 방식입니다.

자세한 정보는 [I2P 공식 사이트](https://geti2p.net)를 참조하세요.
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: 다음은 I2P 네트워크에서 사용되는 주요 구성 요소들입니다:

- **Router**: I2P 네트워크의 핵심 구성 요소로, 데이터 패킷을 전송하고 수신합니다.
- **Tunnel**: 데이터가 네트워크를 통해 전송되는 경로입니다. 각 터널은 여러 라우터를 통해 구성됩니다.
- **LeaseSet**: I2P 네트워크에서 목적지 정보를 포함하는 데이터 구조입니다.
- **NetDb**: 네트워크 데이터베이스로, 라우터와 터널 정보를 저장합니다.
- **Floodfill**: 네트워크 데이터베이스의 정보를 전파하는 라우터입니다.
- **NTCP2** 및 **SSU**: I2P에서 사용하는 두 가지 전송 프로토콜입니다.
- **SAMv3**: I2P와 외부 애플리케이션 간의 통신을 위한 API입니다.
- **I2PTunnel**: I2P 네트워크를 통해 트래픽을 라우팅하는 데 사용되는 도구입니다.
- **I2CP**: I2P 클라이언트와 라우터 간의 통신 프로토콜입니다.
- **I2NP**: I2P 네트워크의 내부 패킷 포맷입니다.
- **Eepsite**: I2P 네트워크 내에서 호스팅되는 웹사이트입니다.
- **Garlic Encryption**: I2P에서 사용되는 데이터 암호화 방법입니다. 

이러한 구성 요소들은 I2P 네트워크의 보안성과 익명성을 유지하는 데 필수적입니다.
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "안드로이드 4.0+, 최소 512MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷을 탐색하거나, 익명으로 데이터를 전송할 수 있습니다. I2P는 여러 가지 프로토콜을 지원하며, 특히 `I2PTunnel`을 통해 HTTP 및 HTTPS 트래픽을 처리할 수 있습니다. 

I2P 네트워크는 `router`와 `tunnel`을 사용하여 데이터를 전송합니다. 각 `router`는 `leaseSet`을 통해 다른 `router`와 통신하며, `netDb`를 사용하여 네트워크의 다른 `router`를 찾습니다. `floodfill`은 네트워크의 메타데이터를 저장하고 배포하는 역할을 합니다.

I2P는 `NTCP2` 및 `SSU` 프로토콜을 사용하여 `router` 간의 연결을 관리합니다. `SAMv3` 인터페이스를 통해 개발자는 I2P 네트워크와 상호작용할 수 있습니다. `I2CP`는 `router`와 클라이언트 간의 통신을 위한 프로토콜입니다.

이러한 구성 요소들은 모두 `garlic encryption`을 사용하여 데이터를 보호합니다. `eepsite`는 I2P 네트워크 내에서 호스팅되는 웹사이트입니다. I2P는 사용자의 프라이버시를 보호하기 위해 설계된 강력한 도구입니다.
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: 다음은 I2P 네트워크에서의 기본적인 개념들입니다:

### I2P 네트워크의 구조

I2P는 익명성을 제공하기 위해 설계된 분산 네트워크입니다. 이 네트워크는 여러 개의 **router**로 구성되어 있으며, 각 router는 서로 연결되어 데이터를 전송합니다. I2P는 **garlic encryption**을 사용하여 데이터를 보호하며, 이는 여러 메시지를 하나의 패킷으로 결합하여 전송하는 방식입니다.

### 익명 통신

I2P에서의 통신은 **tunnel**을 통해 이루어집니다. 각 tunnel은 여러 hop으로 구성되어 있으며, 데이터는 각 hop을 통해 전송됩니다. 이를 통해 송신자와 수신자 간의 직접적인 연결을 피하고 익명성을 유지합니다.

### 리소스 공유

I2P 네트워크에서는 **eepsite**를 통해 웹사이트를 호스팅할 수 있습니다. eepsite는 I2P 내에서만 접근 가능한 웹사이트로, 익명성을 보장합니다. 이를 통해 사용자는 자신의 신원을 노출하지 않고 콘텐츠를 공유할 수 있습니다.

### 데이터베이스 관리

I2P는 **netDb**라는 분산 데이터베이스를 사용하여 네트워크 정보를 관리합니다. netDb는 각 router의 정보를 저장하며, **floodfill** router가 이를 유지 관리합니다. 이를 통해 네트워크의 상태를 효율적으로 관리할 수 있습니다.

### 프로토콜

I2P는 여러 프로토콜을 지원합니다. **NTCP2**와 **SSU**는 I2P의 기본 전송 프로토콜로, 각각 TCP와 UDP를 기반으로 합니다. **SAMv3**는 외부 애플리케이션이 I2P 네트워크와 상호작용할 수 있도록 하는 API입니다.

이러한 개념들은 I2P 네트워크의 작동 원리를 이해하는 데 필수적입니다.
primary: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷을 탐색하거나 콘텐츠를 호스팅할 수 있습니다. I2P는 메시지를 암호화하고 여러 노드를 통해 라우팅하여 사용자의 IP 주소를 숨깁니다. 

## I2P의 주요 구성 요소

- **Router**: I2P 네트워크에 연결하고 트래픽을 라우팅합니다.
- **Tunnel**: 데이터가 이동하는 경로로, 송신자와 수신자 간에 설정됩니다.
- **LeaseSet**: I2P 네트워크에서 서비스의 위치를 설명하는 데이터 구조입니다.
- **NetDb**: 네트워크 데이터베이스로, I2P 네트워크의 노드 정보를 저장합니다.
- **Floodfill**: 네트워크 데이터베이스의 정보를 전파하는 특별한 노드입니다.

I2P는 NTCP2 및 SSU 프로토콜을 사용하여 노드 간의 통신을 관리합니다. SAMv3 인터페이스를 통해 개발자는 I2P 네트워크와 상호 작용할 수 있습니다. I2PTunnel은 사용자가 I2P 네트워크를 통해 트래픽을 터널링할 수 있도록 합니다.

I2P는 강력한 익명성을 제공하며, 이는 주로 garlic encryption(마늘 암호화) 기술을 사용하여 달성됩니다. 이는 메시지를 여러 계층으로 암호화하여 각 계층이 다른 노드에 의해 해독되도록 합니다.
name: "StormyCloud"
location: "미국"
url: "https://stormycloud.org"
resources: I2P는 익명성을 제공하는 네트워크 레이어입니다. 사용자는 I2P를 통해 인터넷 상에서 자신의 신원을 보호하고, 검열을 우회할 수 있습니다. I2P는 분산형 네트워크로, 중앙 서버 없이 운영됩니다. 이는 사용자의 프라이버시를 강화하고, 네트워크의 내구성을 높입니다.

I2P는 여러 가지 프로토콜을 지원합니다. 예를 들어, `I2PTunnel`은 HTTP 및 HTTPS 트래픽을 익명화하는 데 사용됩니다. `SAMv3`는 I2P 네트워크와 상호작용하기 위한 API를 제공합니다. 이러한 도구들은 사용자가 I2P 네트워크를 통해 안전하게 통신할 수 있도록 도와줍니다.

I2P의 핵심 구성 요소 중 하나는 `router`입니다. 각 `router`는 네트워크의 다른 `router`와 통신하여 데이터를 전송합니다. 데이터는 `tunnel`을 통해 전송되며, 이는 여러 `router`를 거쳐 목적지에 도달합니다. 이 과정에서 `garlic encryption`이 사용되어 데이터의 보안을 강화합니다.

`leaseSet`과 `netDb`는 I2P 네트워크의 중요한 부분입니다. `leaseSet`은 `tunnel`의 정보를 포함하며, `netDb`는 네트워크의 분산 데이터베이스로서 `router` 정보를 저장합니다. `floodfill` `router`는 `netDb`의 데이터를 관리하고 전파하는 역할을 합니다.

I2P는 `NTCP2`와 `SSU`와 같은 전송 프로토콜을 사용하여 `router` 간의 통신을 지원합니다. 이러한 프로토콜은 네트워크의 효율성과 보안을 유지하는 데 필수적입니다.

I2P 네트워크에서 웹사이트는 `eepsite`라고 불립니다. `eepsite`는 I2P 네트워크 내에서만 접근 가능하며, 사용자의 익명성을 보장합니다. `eepsite`를 호스팅하려면 `I2PTunnel`을 설정해야 합니다.

I2P는 지속적으로 발전하고 있으며, 커뮤니티의 기여로 기능이 확장되고 있습니다. I2P를 사용하여 안전하고 익명성을 유지한 상태로 인터넷을 탐색하세요.
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
