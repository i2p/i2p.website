---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rejected"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## 개요

이 제안서는 I2PControl의 API2를 설명합니다.

이 제안서는 기존 버전과의 호환성을 깨뜨리기 때문에 거부되었으며 구현되지 않을 것입니다. 자세한 내용은 토론 스레드 링크를 참조하십시오.

### 개발자 주목!

모든 RPC 매개변수는 이제 소문자로 작성됩니다. 이는 기존 API1 구현과의 호환성을 깨뜨리게 됩니다. 이렇게 하는 이유는 사용자에게 API2 이상에서 가장 단순하고 일관된 API를 제공하기 위해서입니다.


## API 2 명세

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### 매개변수

**`"id"`**

요청의 ID 번호입니다. 어느 요청이 어느 응답을 생성했는지 식별하는 데 사용됩니다.

**`"method_name"`**

호출된 RPC의 이름입니다.

**`"auth_token"`**

세션 인증 토큰입니다. 'authenticate' 호출을 제외한 모든 RPC에 제공되어야 합니다.

**`"method_parameter_value"`**

메소드 매개변수입니다. 'get', 'set' 등과 같은 메소드의 다양한 변형을 제공하는 데 사용됩니다.

**`"result_value"`**

RPC가 반환하는 값입니다. 그 타입과 내용은 메소드와 메소드에 따라 다릅니다.


### 접두사

RPC 명명 규칙은 CSS에서 사용되는 것과 유사하며, 다른 API 구현 (i2p, kovri, i2pd)을 위한 벤더 접두사를 포함합니다.:

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

벤더 특유의 접두사를 사용하는 전체적인 아이디어는 약간의 여유를 제공하여 다른 구현이 따라잡기를 기다리지 않고 구현이 혁신할 수 있도록 하는 것입니다. 모든 구현이 RPC를 구현하면 그 여러 접두사를 제거하고 다음 API 버전에 핵심 RPC로 포함할 수 있습니다.


### 메소드 읽기 가이드

 * **rpc.method**

   * *parameter* [매개변수 유형]: [null], [number], [string], [boolean],
     [array] 또는 [object]. [object]는 {key:value} 맵입니다.

반환:
```text

  "return_value" [string] // RPC 호출에 의해 반환된 값입니다.
```


### 메소드

* **authenticate** - 올바른 비밀번호가 제공되면, 이 메소드는 추가 접근을 위한 토큰과 지원되는 API 레벨 목록을 제공합니다.

  * *password* [string]: 이 i2pcontrol 구현의 비밀번호

    반환:
```text
    [object]
    {
      "token" : [string], // 다른 모든 RPC 메소드에 제공될 토큰
      "api" : [[int],[int], ...]  // 지원되는 API 레벨 목록.
    }
```

* **control.** - i2p 제어

  * **control.reseed** - 리시드 시작

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

  * **control.restart** - i2p 인스턴스 재시작

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

  * **control.restart.graceful** - i2p 인스턴스를 우아하게 재시작

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

  * **control.shutdown** - i2p 인스턴스 종료

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

  * **control.shutdown.graceful** - i2p 인스턴스를 우아하게 종료

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

  * **control.update.find** - **차단됨** 서명된 업데이트 검색

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      true [boolean] // 서명된 업데이트가 있는 경우 true
```

  * **control.update.start** - 업데이트 프로세스 시작

    * [nil]: 매개변수가 필요하지 않습니다.

    반환:
```text
      [nil]
```

* **i2pcontrol.** - i2pcontrol 설정

  * **i2pcontrol.address** - i2pcontrol이 수신하는 IP 주소 얻기/설정

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: "0.0.0.0" 또는 "192.168.0.1"과 같은 IP 주소가 필요합니다.

    반환:
```text
      [nil]
```

  * **i2pcontrol.password** - i2pcontrol 비밀번호 변경

    * *set* [string]: 새 비밀번호를 이 문자열로 설정합니다.

    반환:
```text
      [nil]
```

  * **i2pcontrol.port** - i2pcontrol이 수신하는 포트 얻기/설정

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      7650 [number]
```

    * *set* [number]: i2pcontrol이 수신하는 포트를 이 포트로 변경합니다.

    반환:
```text
      [nil]
```

* **settings.** - i2p 인스턴스 설정 얻기/설정

  * **settings.advanced** - 고급 설정

    * *get*  [string]: 이 설정의 값을 가져옵니다.

    반환:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    반환:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: 이 설정의 값을 설정합니다.
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    반환:
```text
      [nil]
```

  * **settings.bandwidth.in** - 인바운드 대역폭 설정
  * **settings.bandwidth.out** - 아웃바운드 대역폭 설정

    * *get* [nil]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0 [number]
```

    * *set* [number]: 대역폭 제한을 설정합니다.

    반환:
```text
     [nil]
```

  * **settings.ntcp.autoip** - NTCP의 IP 자동 감지 설정 얻기

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - NTCP 호스트 이름 얻기

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: 새 호스트 이름을 설정합니다.

    반환:
```text
      [nil]
```

  * **settings.ntcp.port** - NTCP 포트

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0 [number]
```

    * *set* [number]: 새 NTCP 포트를 설정합니다.

    반환:
```text
      [nil]
```

    * *set* [boolean]: NTCP IP 자동 감지를 설정합니다.

    반환:
```text
      [nil]
```

  * **settings.ssu.autoip** - SSU의 IP 자동 감지 설정 구성

    * *get* [nil]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - SSU 호스트 이름 구성

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: 새 SSU 호스트 이름을 설정합니다.

    반환:
```text
      [nil]
```

  * **settings.ssu.port** - SSU 포트

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0 [number]
```

    * *set* [number]: 새 SSU 포트를 설정합니다.

    반환:
```text
      [nil]
```

    * *set* [boolean]: SSU IP 자동 감지를 설정합니다.

    반환:
```text
      [nil]
```

  * **settings.share** - 대역폭 공유 비율 얻기

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0 [number] // 대역폭 공유 비율 (0-100)
```

    * *set* [number]: 대역폭 공유 비율 설정 (0-100)

    반환:
```text
      [nil]
```

  * **settings.upnp** - UPNP 활성화 또는 비활성화

    * *get* [nil]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      true [boolean]
```

    * *set* [boolean]: SSU IP 자동 감지를 설정합니다.

    반환:
```text
      [nil]
```

* **stats.** - i2p 인스턴스에서 통계 가져오기

  * **stats.advanced** - 인스턴스 내에서 유지되는 모든 통계에 대한 액세스를 제공합니다.

    * *get* [string]: 제공할 고급 통계의 이름
    * *Optional:* *period* [number]: 요청된 통계의 기간

  * **stats.knownpeers** - 알려진 피어 수 반환
  * **stats.uptime** - 라우터 시작 이후 경과 시간(밀리초) 반환
  * **stats.bandwidth.in** - 인바운드 대역폭 반환 (이상적으로는 마지막 초)
  * **stats.bandwidth.in.total** - 마지막 재시작 이후 수신된 바이트 수 반환
  * **stats.bandwidth.out** - 아웃바운드 대역폭 반환 (이상적으로는 마지막 초)
  * **stats.bandwidth.out.total** - 마지막 재시작 이후 전송된 바이트 수 반환
  * **stats.tunnels.participating** - 현재 참여 중인 터널 수 반환
  * **stats.netdb.peers.active** - 최근에 통신한 피어 수 반환
  * **stats.netdb.peers.fast** - '빠른' 피어 수 반환
  * **stats.netdb.peers.highcapacity** - '고용량' 피어 수 반환
  * **stats.netdb.peers.known** - 알려진 피어 수 반환

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0.0 [number]
```

* **status.** - i2p 인스턴스 상태 가져오기

  * **status.router** - 라우터 상태 가져오기

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      "status" [string]
```

  * **status.net** - 라우터 네트워크 상태 가져오기

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - 현재 i2p 인스턴스가 플러드필인지 여부

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      true [boolean]
```

  * **status.isreseeding** - 현재 i2p 인스턴스가 리시드 중인지 여부

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      true [boolean]
```

  * **status.ip** - 이 i2p 인스턴스의 공인 IP 감지

    * *get* [null]: 이 매개변수는 설정할 필요가 없습니다.

    반환:
```text
      "0.0.0.0" [string]
```
