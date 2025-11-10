---
title: "Bitcoin Core가 I2P 지원을 추가했습니다!"
date: 2021-09-18
author: "idk"
description: "새로운 사용 사례와 수용 확대의 신호"
categories: ["general"]
---

수개월에 걸친 준비 끝에, 비트코인 코어가 I2P에 대한 공식 지원을 추가했습니다! Bitcoin-over-I2P 노드는 I2P와 clearnet(일반 인터넷) 모두에서 동작하는 노드의 도움을 받아 다른 비트코인 노드들과 완전히 상호작용할 수 있어, 비트코인 네트워크에서 동등한 참여자가 됩니다. 비트코인과 같은 대규모 커뮤니티가 I2P가 전 세계 사람들에게 프라이버시와 도달성을 제공함으로써 가져다줄 수 있는 이점을 주목하는 모습을 보게 되어 정말 고무적입니다.

## 작동 방식

I2P 지원은 SAM API를 통해 자동으로 이루어집니다. 이는 애플리케이션 개발자가 I2P 연결을 프로그래밍 방식으로 그리고 편리하게 구축할 수 있도록 하는 등, I2P가 특히 뛰어난 점들을 부각시키는 반가운 소식이기도 합니다. Bitcoin-over-I2P 사용자는 SAM API를 활성화하고 I2P를 활성화한 상태로 Bitcoin을 실행하면 수동 구성 없이 I2P를 사용할 수 있습니다.

## I2P Router 설정

비트코인에 익명 연결을 제공하기 위해 I2P Router를 설정하려면 SAM API를 활성화해야 합니다. Java I2P에서는 http://127.0.0.1:7657/configclients로 이동하여 "Start" 버튼을 눌러 SAM Application Bridge를 시작하십시오. 또한 "Run at Startup" 확인란을 선택하고 "Save Client Configuration"을 클릭하여 SAM Application Bridge를 기본적으로 활성화하는 것이 좋습니다.

i2pd에서는 SAM API가 일반적으로 기본값으로 활성화되어 있지만, 그렇지 않다면 다음을 설정해야 합니다:

```
sam.enabled=true
```
귀하의 i2pd.conf 파일에서.

## 익명성과 연결성을 위한 귀하의 비트코인 노드 구성

Bitcoin 자체를 익명 모드로 실행하려면 여전히 Bitcoin 데이터 디렉터리의 일부 구성 파일을 편집해야 합니다. 해당 디렉터리는 Windows에서는 %APPDATA%\Bitcoin, Linux에서는 ~/.bitcoin, Mac OSX에서는 ~/Library/Application Support/Bitcoin/ 입니다. 또한 I2P 지원이 포함되려면 최소 버전 22.0.0이 필요합니다.

이 지침을 따른 후에는 I2P 연결에는 I2P를, .onion 및 clearnet(일반 인터넷) 연결에는 Tor를 사용하여 모든 연결이 익명화되는 개인 비트코인 노드를 갖게 됩니다. 편의를 위해 Windows 사용자는 시작 메뉴를 열고 "Run"을 검색하여 Bitcoin 데이터 디렉터리를 여십시오. "Run" 프롬프트에서 "%APPDATA%\Bitcoin"을 입력하고 Enter 키를 누르십시오.

해당 디렉터리에서 "i2p.conf."라는 파일을 만드십시오. Windows에서는 저장할 때 Windows가 파일에 기본 확장자를 자동으로 추가하지 않도록 파일 이름에 따옴표를 붙였는지 확인해야 합니다. 파일에는 다음 I2P 관련 Bitcoin 구성 옵션이 포함되어야 합니다:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
다음으로, "tor.conf"라는 다른 파일을 만들어야 합니다. 이 파일에는 다음과 같은 Tor 관련 구성 옵션이 포함되어야 합니다:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
마지막으로, 이러한 구성 옵션을 데이터 디렉터리에 있는 Bitcoin 구성 파일인 "bitcoin.conf"에 "include"해야 합니다. bitcoin.conf 파일에 다음 두 줄을 추가하세요:

```
includeconf=i2p.conf
includeconf=tor.conf
```
이제 비트코인 노드는 익명 연결만 사용하도록 구성되었습니다. 원격 노드에 대한 직접 연결을 활성화하려면, 다음으로 시작하는 줄들을 제거하십시오:

```
onlynet=
```
비트코인 노드를 익명으로 유지할 필요가 없다면 이렇게 할 수 있으며, 이는 익명 사용자들이 나머지 비트코인 네트워크에 연결하는 데 도움이 됩니다.
