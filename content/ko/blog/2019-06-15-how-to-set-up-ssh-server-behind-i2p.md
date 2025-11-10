---
title: "개인 접근을 위한 I2P 뒤의 SSH 서버 설정 방법"
date: 2019-06-15
author: "idk"
description: "I2P를 통한 SSH"
---

# 개인 접속을 위해 I2P 뒤에서 SSH 서버를 설정하는 방법

이 문서는 I2P 또는 i2pd를 사용하여 원격으로 SSH 서버에 접속하기 위해 I2P tunnel을 설정하고 조정하는 방법을 설명하는 튜토리얼입니다. 현재로서는 SSH 서버를 패키지 관리자를 통해 설치하고 서비스로 실행한다고 가정합니다.

고려사항: 이 가이드에서는 몇 가지 가정을 전제로 합니다. 이는 각자의 설정에서 발생하는 복잡성에 따라 조정되어야 하며, 특히 격리를 위해 VM이나 컨테이너를 사용하는 경우 그렇습니다. 여기서는 I2P router와 SSH 서버가 동일한 localhost에서 실행되고 있다고 가정합니다. 또한 새로 생성된 SSH 호스트 키를 사용해야 하며, 이를 위해 새로 설치한 sshd를 사용하거나 기존 키를 삭제하고 재생성을 강제하는 방법을 권장합니다. 예를 들어:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Java I2P의 웹 인터페이스를 사용하여 [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr)(숨겨진 서비스 관리자)로 이동한 다음 tunnel 마법사를 시작하세요.

#### Tunnel Wizard

이 tunnel을 SSH 서버용으로 설정하고 있으므로, "Server" tunnel 유형을 선택해야 합니다.

**스크린샷 자리표시자:** 마법사를 사용하여 "Server" tunnel을 생성하세요

나중에 미세 조정하면 되지만, 시작하기에는 Standard tunnel type이 가장 쉽습니다.

**스크린샷 자리표시자:** "Standard" 종류

좋은 설명을 작성하세요:

**스크린샷 자리표시자:** 용도를 설명하세요

그리고 SSH 서버가 어디에서 접속 가능할지 지정하세요.

**스크린샷 자리표시자:** 향후 SSH 서버가 설치될 위치를 가리키도록 설정하세요

결과를 검토한 다음 설정을 저장하세요.

**스크린샷 자리 표시자:** 설정을 저장하세요.

#### Advanced Settings

이제 Hidden Services Manager(숨은 서비스 관리자)로 돌아가서 사용 가능한 고급 설정을 살펴보세요. 반드시 변경해야 할 한 가지는 bulk connections(대용량 전송용 연결) 대신 interactive connections(상호작용형 연결)으로 설정하는 것입니다.

**스크린샷 자리표시자:** 대화형 연결에 맞게 tunnel을 구성하세요

그 외에도 SSH 서버에 접속할 때 성능에 영향을 줄 수 있는 다른 옵션들이 있습니다. 익명성에 그다지 크게 신경 쓰지 않는다면, 경유하는 홉 수를 줄일 수 있습니다. 속도에 문제가 있다면, tunnel(터널) 수를 더 늘리는 것이 도움이 될 수 있습니다. 몇 개의 예비 tunnel은 아마도 좋은 생각입니다. 약간 미세 조정이 필요할 수도 있습니다.

**스크린샷 자리표시자:** 익명성에 신경 쓰지 않는다면 tunnel 길이를 줄이십시오.

마지막으로, 모든 설정이 적용되도록 tunnel을 다시 시작하십시오.

특히 많은 수의 tunnel(터널)을 실행하기로 선택한 경우 유용한 또 다른 흥미로운 설정은 "Reduce on Idle"이며, 이 설정은 서비스가 장기간 비활성 상태였을 때 실행되는 tunnel의 수를 줄여 줍니다.

**스크린샷 자리표시자:** tunnel 수를 높게 설정했다면 유휴 시 감소

### Using i2pd

i2pd에서는 모든 구성은 웹 인터페이스가 아니라 파일을 통해 이루어집니다. i2pd에 SSH 서비스 tunnel을 구성하려면, 익명성과 성능 요구에 맞게 다음 예시 설정을 조정한 뒤 이를 tunnels.conf에 복사하세요.

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## 1단계: SSH 서버용 I2P tunnel 설정

SSH 서버에 어떻게 접근할지에 따라 몇 가지 설정을 변경하는 것이 좋습니다. 모든 SSH 서버에서 당연히 해야 하는 SSH 보안 강화 작업(공개 키 인증, root로 로그인 금지 등) 외에도, SSH 서버가 서버 tunnel 외의 어떤 주소에서도 수신하지 않도록 하려면 AddressFamily를 inet으로, ListenAddress를 127.0.0.1로 변경해야 합니다.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
SSH 서버에 22가 아닌 다른 포트를 사용하기로 했다면 I2P tunnel 구성에서 포트를 변경해야 합니다.

## Step Three: Set up I2P tunnel for SSH Client

클라이언트 연결을 구성하려면 SSH 서버의 I2P router console을 볼 수 있어야 합니다. 이 구성의 장점 중 하나는 I2P tunnel로의 초기 연결이 인증되므로, SSH 서버로의 초기 연결이 MITM(중간자) 공격을 당할 위험을 어느 정도 줄여 준다는 점입니다. 이러한 위험은 Trust-On-First-Use(처음 사용 시 신뢰) 시나리오에서 흔합니다.

### Java I2P 사용하기

#### Tunnel 마법사

먼저 hidden services manager에서 tunnel 구성 마법사를 시작한 다음 client tunnel을 선택하세요.

**스크린샷 자리표시자:** 마법사를 사용하여 클라이언트 tunnel을 생성하세요

다음으로, 표준 tunnel 유형을 선택하세요. 이 구성은 나중에 세부적으로 조정할 예정입니다.

**Screenshot placeholder:** 표준 유형

그것에 대한 좋은 설명을 제공하세요.

**Screenshot placeholder:** Give it a good description

이게 그나마 약간 까다로운 부분입니다. I2P router 콘솔의 hidden services manager(숨겨진 서비스 관리자)로 이동하여 SSH 서버 tunnel의 base64 "local destination"을 찾으세요. 이 정보를 다음 단계로 복사할 방법을 찾아야 합니다. 저는 보통 [Tox](https://tox.chat)으로 제게 보내곤 하며, 대부분의 사람에게는 off-the-record(기록이 남지 않는) 어떤 방식이든 충분합니다.

**스크린샷 자리표시자:** 연결하려는 destination(목적지)를 찾으세요

클라이언트 장치로 전송된, 연결하려는 base64 목적지를 찾았다면, 그것을 클라이언트 목적지 필드에 붙여넣으세요.

**스크린샷 자리표시자:** destination(목적지) 붙이기

마지막으로, SSH 클라이언트가 연결할 로컬 포트를 설정하십시오. 이 로컬 포트는 base64 destination(목적지)에 연결되며, 따라서 SSH 서버에 연결됩니다.

**스크린샷 자리 표시자:** 로컬 포트를 선택하세요

자동으로 시작할지 여부를 결정하십시오.

**스크린샷 자리표시자:** 자동 시작할지 결정하세요

#### 고급 설정

이전과 마찬가지로, 대화형 연결에 최적화되도록 설정을 변경하는 것이 좋습니다. 또한 서버에서 클라이언트 화이트리스트(허용 목록)를 설정하려면 "Generate key to enable persistent client tunnel identity" 라디오 버튼을 선택해야 합니다.

**Screenshot placeholder:** Configure it to be interactive

### Using i2pd

tunnels.conf에 다음 행들을 추가하고, 성능/익명성 요구 사항에 맞게 조정하여 설정할 수 있습니다.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

I2P에서 서버에 연결하도록 SSH 클라이언트를 설정하는 방법은 많지만, 익명 사용을 위해 SSH 클라이언트의 보안을 강화하기 위해 해야 할 몇 가지가 있습니다. 먼저, 익명 및 비익명 SSH 연결이 서로 오염될 위험을 피하기 위해 SSH 서버에 자신을 식별할 때 단일한 특정 키만 사용하도록 구성해야 합니다.

$HOME/.ssh/config 파일에 다음 행들이 포함되어 있는지 확인하세요:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
또는 .bash_alias에 항목을 만들어 옵션을 강제 적용하고 I2P에 자동으로 연결되도록 할 수 있습니다. 요지는 IdentitiesOnly(지정한 키만 사용)를 강제하고 개인 키 파일을 제공해야 한다는 것입니다.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

이것은 대체로 선택 사항이지만, 꽤 멋지고 우연히 당신의 destination(목적지)을 발견한 누구든 당신이 SSH 서비스를 호스팅하고 있다는 사실을 알아낼 수 없도록 해줍니다.

먼저, 지속적인 클라이언트 tunnel의 목적지를 가져온 다음 서버로 전송하십시오.

**스크린샷 자리표시자:** 클라이언트 Destination 가져오기

클라이언트의 base64 목적지를 서버의 목적지 허용 목록에 추가하십시오. 이제 해당 특정 클라이언트 tunnel에서만 서버 tunnel에 연결할 수 있으며, 그 외 누구도 해당 목적지에 연결할 수 없습니다.

**스크린샷 자리표시자:** 그리고 그것을 서버 화이트리스트에 붙여넣으세요

상호 인증이 최고다.

**참고:** 원문 게시물에서 참조된 이미지는 `/static/images/` 디렉터리에 추가해야 합니다: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
