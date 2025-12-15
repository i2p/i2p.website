---
title: "Datagram2 프로토콜"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Closed"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## 상태

2025-04-15 리뷰에서 승인됨.
사양에 변경 사항이 통합되었습니다.
API 0.9.66에서 Java I2P로 구현되었습니다.
상태에 대한 구현 문서를 확인하십시오.



## 개요

[Prop123](/proposals/123-new-netdb-entries/)에서 별도의 제안으로 분리되었습니다.

오프라인 서명은 응답 가능한 데이터그램 처리에서 확인할 수 없습니다.
오프라인 서명된 것을 나타내는 플래그가 필요하지만 플래그를 넣을 곳이 없습니다.

완전히 새로운 I2CP 프로토콜 번호와 형식이 필요하며,
이것은 [DATAGRAMS](/docs/api/datagrams/) 사양에 추가될 것입니다.
이를 "Datagram2"라고 부릅시다.


## 목표

- 오프라인 서명 지원 추가
- 재생 저항 추가
- 서명 없는 플러버 추가
- 확장성을 위한 플래그 및 옵션 필드 추가


## 비목표

혼잡 제어 등을 위한 전체 엔드 투 엔드 프로토콜 지원.
이는 Datagram2 위에 빌드되거나 대체해야 할 것입니다. 이는 저수준 프로토콜입니다.
Datagram2 위에만 고성능 프로토콜을 설계하는 것은 의미가 없습니다. 이는 보낸 사람 필드와 서명 오버헤드 때문입니다.
이러한 프로토콜은 Datagram2로 초기 핸드셰이크를 수행한 다음 RAW 데이터그램으로 전환해야 합니다.


## 동기

2019년에 완료된 LS2 작업에서 남음.

Datagram2를 사용하는 첫 번째 응용 프로그램은
i2psnark 및 zzzot에서 구현된 바와 같이 비트토런트 UDP 발표가 될 것으로 예상됩니다,
자세한 내용은 [Prop160](/proposals/160-udp-trackers/)를 참조하십시오.


## 응답 가능한 데이터그램 사양

참조로,
다음은 [Datagrams](/docs/api/datagrams/)에서 복사한 응답 가능한 데이터그램 사양에 대한 리뷰입니다.
응답 가능한 데이터그램의 표준 I2CP 프로토콜 번호는 PROTO_DATAGRAM (17)입니다.

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: a `Destination`
          length: 387+ bytes
          The originator and signer of the datagram

  signature :: a `Signature`
               Signature type must match the signing public key type of $from
               length: 40+ bytes, as implied by the Signature type.
               For the default DSA_SHA1 key type:
                  The DSA `Signature` of the SHA-256 hash of the payload.
               For other key types:
                  The `Signature` of the payload.
               The signature may be verified by the signing public key of $from

  payload ::  The data
              Length: 0 to about 31.5 KB (see notes)

  Total length: Payload length + 423+
```



## 설계

- 새로운 프로토콜 19 - 옵션이 있는 응답 가능한 데이터그램 정의.
- 새로운 프로토콜 20 - 서명 없는 응답 가능한 데이터그램 정의.
- 오프라인 서명 및 향후 확장을 위한 플래그 필드 추가
- 처리 용이성을 위해 페이로드 후 서명 이동
- 응답 가능한 데이터그램이나 스트리밍과 다른 새로운 서명 사양,
  서명 확인이 응답 가능한 데이터그램이나 스트리밍으로 해석되면 실패합니다.
  이는 서명을 페이로드 후로 이동시키고,
  서명 함수에 대상 해시를 포함시켜 달성됩니다.
- 데이터그램에 대한 재생 방지 추가, [Prop164](/proposals/164-streaming/)에서 스트리밍에 대한 작업 수행.
- 임의의 옵션에 대한 섹션 추가
- [Common](/docs/specs/common-structures/)과 [Streaming](/docs/specs/streaming/)에서 오프라인 서명 형식 재사용.
- 오프라인 서명 섹션은 가변 길이의
  페이로드 및 서명 섹션 앞에 있어야 하며, 서명의 길이를 지정합니다.


## 사양

### 프로토콜

Datagram2의 새로운 I2CP 프로토콜 번호는 19입니다.
이를 [I2CP](/docs/protocol/i2cp/)에 PROTO_DATAGRAM2로 추가하십시오.

Datagram3의 새로운 I2CP 프로토콜 번호는 20입니다.
이를 [I2CP](/docs/protocol/i2cp/)에 PROTO_DATAGRAM2로 추가하십시오.


### Datagram2 형식

다음과 같이 [DATAGRAMS](/docs/api/datagrams/)에 Datagram2를 추가하십시오:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: a `Destination`
          length: 387+ bytes
          The originator and (unless offline signed) signer of the datagram

  flags :: (2 bytes)
           Bit order: 15 14 ... 3 2 1 0
           Bits 3-0: Version: 0x02 (0 0 1 0)
           Bit 4: If 0, no options; if 1, options mapping is included
           Bit 5: If 0, no offline sig; if 1, offline signed
           Bits 15-6: unused, set to 0 for compatibility with future uses

  options :: (2+ bytes if present)
           If flag indicates options are present, a `Mapping`
           containing arbitrary text options

  offline_signature ::
               If flag indicates offline keys, the offline signature section,
               as specified in the Common Structures Specification,
               with the following 4 fields. Length: varies by online and offline
               sig types, typically 102 bytes for Ed25519
               This section can, and should, be generated offline.

    expires :: Expires timestamp
               (4 bytes, big endian, seconds since epoch, rolls over in 2106)

    sigtype :: Transient sig type (2 bytes, big endian)

    pubkey :: Transient signing public key (length as implied by sig type),
              typically 32 bytes for Ed25519 sig type.

    offsig :: a `Signature`
              Signature of expires timestamp, transient sig type,
              and public key, by the destination public key,
              length: 40+ bytes, as implied by the Signature type, typically
              64 bytes for Ed25519 sig type.

  payload ::  The data
              Length: 0 to about 61 KB (see notes)

  signature :: a `Signature`
               Signature type must match the signing public key type of $from
               (if no offline signature) or the transient sigtype
               (if offline signed)
               length: 40+ bytes, as implied by the Signature type, typically
               64 bytes for Ed25519 sig type.
               The `Signature` of the payload and other fields as specified below.
               The signature is verified by the signing public key of $from
               (if no offline signature) or the transient pubkey
               (if offline signed)

```

총 길이: 최소 433 + 페이로드 길이;
오프라인 서명 없이 X25519 발신자의 일반적인 길이:
457 + 페이로드 길이.
메시지는 일반적으로 I2CP 레이어에서 gzip으로 압축되므로,
압축 가능한 출발지로부터의 경우 상당한 절약을 할 수 있습니다.

참고: 오프라인 서명 형식은 공통 구조 사양 [Common](/docs/specs/common-structures/) 및 [Streaming](/docs/specs/streaming/)와 동일합니다.

### 서명

서명은 다음 필드를 포함합니다.

- 프렐루드: 대상 목적지의 32바이트 해시 (데이터그램에 포함되지 않음)
- 플래그
- 옵션 (있을 경우)
- 오프라인 서명 (있을 경우)
- 페이로드

응답 가능한 데이터그램에서, DSA_SHA1 키 유형의 경우, 서명은
페이로드의 SHA-256 해시에 기반했지만, 여기서는 서명이
항상 위의 필드 (해시가 아님)를 포함합니다, 이는 키 유형에 관계없이 적용됩니다.


### ToHash 확인

수신자는 서명 (자신의 목적지 해시 사용)을 확인해야 하며,
재생 방지를 위해 실패 시 데이터그램을 폐기해야 합니다.


### Datagram3 형식

다음과 같이 [DATAGRAMS](/docs/api/datagrams/)에 Datagram3을 추가하십시오:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: a `Hash`
              length: 32 bytes
              The originator of the datagram

  flags :: (2 bytes)
           Bit order: 15 14 ... 3 2 1 0
           Bits 3-0: Version: 0x03 (0 0 1 1)
           Bit 4: If 0, no options; if 1, options mapping is included
           Bits 15-5: unused, set to 0 for compatibility with future uses

  options :: (2+ bytes if present)
           If flag indicates options are present, a `Mapping`
           containing arbitrary text options

  payload ::  The data
              Length: 0 to about 61 KB (see notes)

```

총 길이: 최소 34 + 페이로드 길이.



### SAM

SAMv3 사양에 STYLE=DATAGRAM2 및 STYLE=DATAGRAM3을 추가하십시오.
오프라인 서명에 대한 정보를 업데이트하십시오.


### 오버헤드

이 설계는 응답 가능한 데이터그램에 대해 2바이트의 오버헤드를 추가합니다.
이는 수용 가능합니다.



## 보안 분석

서명에 대상 해시를 포함시키면 재생 공격을 방지하는 데 효과적일 것입니다.

Datagram3 형식에는 서명이 없으므로 발신자를 검증할 수 없으며,
재생 공격이 가능합니다. 필요한 모든 검증은 응용 프로그램 계층에서 수행되거나,
라우터의 래칫 계층에 의해 수행되어야 합니다.



## 참고

- 실질적인 길이는 프로토콜 하위 계층에 의해 제한됩니다 - 터널
  메시지 사양 [TUNMSG](/docs/specs/tunnel-message/#notes)은 메시지를 약 61.2 KB로 제한하며,
  전송 [TRANSPORT](/docs/transport/)은 현재 메시지를 약 64 KB로 제한하므로,
  여기서의 데이터 길이는 약 61 KB로 제한됩니다.
- 큰 데이터그램의 신뢰성에 대한 중요한 주석, [API](/docs/api/datagrams/). 최고의 결과를 위해,
  페이로드를 약 10 KB 이하로 제한하십시오.




## 호환성

없음. 응용 프로그램은 프로토콜 및/또는 포트에 기반하여 Datagram2 I2CP 메시지를 라우팅하도록 다시 작성되어야 합니다.
잘못 라우팅되어 응답 가능한 데이터그램이나 스트리밍 메시지로 해석된 Datagram2 메시지는 서명, 형식 또는 둘 다에 따라 실패할 것입니다.



## 마이그레이션

각 UDP 응용 프로그램은 개별적으로 지원을 감지하고 마이그레이션해야 합니다.
가장 주목할 만한 UDP 응용 프로그램은 비트토런트입니다.

### 비트토런트

비트토런트 DHT: 확장 플래그가 필요할 가능성이 있으며,
예: i2p_dg2, BiglyBT와 조율하십시오

비트토런트 UDP 발표 [Prop160](/proposals/160-udp-trackers/): 처음부터 설계하십시오.
BiglyBT, i2psnark, zzzot와 조율하십시오

### 기타

Bote: 마이그레이션되지 않을 가능성이 높으며, 적극적으로 유지 관리되지 않습니다

Streamr: 아무도 사용하지 않으며, 마이그레이션 계획이 없습니다

SAM UDP 앱: 알려진 바 없습니다


## 참고문헌

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/specs/datagrams/)
* [I2CP](/docs/protocol/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/transport/)
* [TUNMSG](/docs/specs/tunnel-message/#notes)
