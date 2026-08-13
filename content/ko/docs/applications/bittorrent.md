---
title: "I2P를 통한 Bittorrent"
description: "I2P에서 BitTorrent 클라이언트와 트래커를 위한 프로토콜 사양"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

I2P에는 여러 bittorrent 클라이언트와 트래커가 있습니다. I2P 주소 체계는 IP와 포트 대신 Destination을 사용하므로, I2P에서 작동하려면 트래커와 클라이언트 소프트웨어에 약간의 변경이 필요합니다. 이러한 변경 사항은 아래에 명시되어 있습니다. 기존 I2P 클라이언트 및 트래커와의 호환성을 위한 지침을 주의 깊게 확인하시기 바랍니다.

이 페이지는 모든 클라이언트와 트래커에 공통되는 프로토콜 세부사항을 명시합니다. 특정 클라이언트와 트래커는 다른 고유한 기능이나 프로토콜을 구현할 수 있습니다.

클라이언트 및 tracker 소프트웨어의 I2P 추가 포팅을 환영합니다.

---

## 개발자를 위한 일반 가이드

대부분의 비-Java bittorrent 클라이언트는 [SAMv3](/docs/api/samv3/)를 통해 I2P에 연결됩니다. SAM 세션(또는 I2P 내부에서는 tunnel 풀 또는 tunnel 집합)은 장기간 지속되도록 설계되었습니다. 대부분의 bittorrent 클라이언트는 시작 시 생성되고 종료 시 닫히는 하나의 세션만 필요합니다. I2P는 회로가 빠르게 생성되고 폐기될 수 있는 Tor와는 다릅니다. 애플리케이션을 설계하여 두 개 이상의 동시 세션을 사용하거나 빠르게 생성하고 폐기하도록 하기 전에 신중히 고려하고 I2P 개발자와 상의하세요. Bittorrent 클라이언트는 모든 연결에 대해 고유한 세션을 생성해서는 안 됩니다. 공지(announce)와 클라이언트 연결에 동일한 세션을 사용하도록 클라이언트를 설계하세요.

또한 클라이언트 설정(그리고 router 설정에 대한 사용자 가이드, 또는 router를 번들로 포함하는 경우 router 기본값)이 사용자들이 소비하는 것보다 더 많은 리소스를 네트워크에 기여하도록 보장해 주시기 바랍니다. I2P는 P2P 네트워크이며, 인기 있는 애플리케이션이 네트워크를 지속적인 혼잡 상태로 몰아넣는다면 네트워크가 생존할 수 없습니다.

I2P outproxy를 통해 clearnet으로 bittorrent 지원을 제공하지 마세요. 차단될 가능성이 높습니다. 가이드는 outproxy 운영자에게 문의하세요.

Java I2P와 i2pd router 구현은 독립적이며 동작, 기능 지원 및 기본값에 약간의 차이가 있습니다. 두 router의 최신 버전으로 애플리케이션을 테스트하시기 바랍니다.

i2pd SAM은 기본적으로 활성화되어 있지만, Java I2P SAM은 그렇지 않습니다. 사용자에게 Java I2P에서 SAM을 활성화하는 방법(router 콘솔의 /configclients를 통해)에 대한 지침을 제공하거나, 초기 연결이 실패할 경우 "I2P가 실행 중이고 SAM 인터페이스가 활성화되어 있는지 확인하세요"와 같은 적절한 오류 메시지를 사용자에게 제공하세요.

Java I2P와 i2pd router는 tunnel 수량에 대해 서로 다른 기본값을 가지고 있습니다. Java의 기본값은 2이고 i2pd의 기본값은 5입니다. 대부분의 낮은-중간 수준의 대역폭과 낮은-중간 수준의 연결 수에서는 3이 충분합니다. Java I2P와 i2pd router에서 일관된 성능을 얻기 위해 SESSION CREATE 메시지에서 tunnel 수량을 명시해 주세요.

I2P는 여러 서명 및 암호화 유형을 지원합니다. 호환성을 위해 I2P는 기본적으로 오래되고 비효율적인 유형을 사용하므로, 모든 클라이언트는 최신 유형을 지정해야 합니다.

SAM을 사용하는 경우, 서명 타입은 DEST GENERATE 및 SESSION CREATE (임시용) 명령에서 지정됩니다. 모든 클라이언트는 SIGNATURE_TYPE=7 (Ed25519)로 설정해야 합니다.

암호화 유형은 SAM SESSION CREATE 명령이나 i2cp 옵션에서 지정됩니다. 여러 암호화 유형이 허용됩니다. 일부 tracker는 ECIES-X25519를 지원하고, 일부는 ElGamal을 지원하며, 일부는 둘 다 지원합니다. 클라이언트는 두 가지 모두에 연결할 수 있도록 i2cp.leaseSetEncType=4,0 (ECIES-X25519와 ElGamal용)으로 설정해야 합니다.

DHT 지원은 동일한 세션에서 TCP와 UDP를 위한 SAM v3.3 PRIMARY와 SUBSESSIONS가 필요합니다. 이는 클라이언트가 Java로 작성되지 않는 한 클라이언트 측에서 상당한 개발 노력이 필요할 것입니다. i2pd는 현재 SAM v3.3을 지원하지 않습니다. libtorrent는 현재 SAM v3.3을 지원하지 않습니다.

DHT 지원 없이는 magnet 링크가 작동하도록 설정 가능한 알려진 공개 tracker 목록에 자동으로 알림을 보내고 싶을 수 있습니다. 현재 운영 중인 공개 tracker에 대한 정보는 I2P 사용자들에게 문의하고 기본값을 최신 상태로 유지하세요. i2p_pex 확장을 지원하는 것도 DHT 지원 부족을 완화하는 데 도움이 될 것입니다.

애플리케이션이 필요한 리소스만 사용하도록 보장하는 개발자 가이드는 [SAMv3 명세](/docs/api/samv3/)와 [애플리케이션에 I2P 번들링 가이드](/docs/applications/embedding/)를 참조하세요. 추가 지원이 필요하면 I2P 또는 i2pd 개발자에게 문의하세요.

---

## 공지사항

클라이언트는 일반적으로 구형 트래커와의 호환성을 위해 announce에 가짜 port=6881 매개변수를 포함합니다. 트래커는 port 매개변수를 무시할 수 있으며, 이를 필수로 요구해서는 안 됩니다.

ip 매개변수는 클라이언트의 [Destination](/docs/specs/common-structures/#struct_Destination)을 I2P Base 64 알파벳 [A-Z][a-z][0-9]-~를 사용하여 base 64로 인코딩한 것입니다. [Destination](/docs/specs/common-structures/#struct_Destination)은 387+ 바이트이므로 Base 64는 516+ 바이트입니다. 클라이언트는 일반적으로 구형 트래커와의 호환성을 위해 Base 64 Destination에 ".i2p"를 추가합니다. 트래커는 ".i2p" 추가를 요구하지 않아야 합니다.

다른 매개변수들은 표준 bittorrent와 동일합니다.

클라이언트의 현재 Destination은 387바이트 이상입니다(Base 64 인코딩에서는 516바이트 이상). 현재로서는 475바이트를 합리적인 최대값으로 가정할 수 있습니다. 트래커가 압축된 응답을 전달하기 위해 Base64를 디코딩해야 하므로(아래 참조), 트래커는 발표 시 Base64를 디코딩하고 잘못된 Base64를 거부해야 합니다.

기본 응답 유형은 비압축(non-compact)입니다. 클라이언트는 compact=1 매개변수를 사용하여 압축 응답을 요청할 수 있습니다. 트래커는 요청 시 압축 응답을 반환할 수 있지만 반드시 그럴 필요는 없습니다. 참고: 현재 모든 인기 있는 트래커들이 압축 응답을 지원하며, 적어도 하나의 트래커는 announce에서 compact=1을 요구합니다. 모든 클라이언트는 압축 응답을 요청하고 지원해야 합니다.

새로운 I2P 클라이언트 개발자들은 포트 4444의 HTTP 클라이언트 프록시보다는 자신의 tunnel을 통해 announce를 구현할 것을 강력히 권장합니다. 이렇게 하는 것이 더 효율적이며 tracker에서 destination 강제를 허용합니다 (아래 참조).

UDP 공지의 명세서는 2025년 6월에 확정되었습니다. 다양한 I2P 클라이언트와 트래커에서의 지원은 2025년 후반에 순차적으로 출시될 예정입니다. 추가 정보는 아래를 참조하세요.

---

## 비압축 트래커 응답

참고: 더 이상 사용되지 않습니다. 모든 인기 있는 tracker는 이제 compact 응답을 지원하며, 적어도 하나는 announce에서 compact=1을 요구합니다. 모든 클라이언트는 compact 응답을 요청하고 지원해야 합니다.

비압축 응답은 표준 비트토렌트와 동일하지만 I2P "ip"를 사용합니다. 이는 아마도 ".i2p" 접미사가 붙은 긴 base64로 인코딩된 "DNS 문자열"입니다.

Tracker들은 일반적으로 구형 클라이언트와의 호환성을 위해 가짜 포트 키를 포함하거나 announce의 포트를 사용합니다. 클라이언트들은 포트 매개변수를 무시해야 하며, 이를 필수로 요구해서는 안 됩니다.

ip 키의 값은 위에서 설명한 대로 클라이언트의 [Destination](/docs/specs/common-structures/#struct_Destination)을 base 64로 인코딩한 것입니다. 트래커는 일반적으로 기존 클라이언트와의 호환성을 위해 announce ip에 ".i2p"가 없었다면 Base 64 Destination에 ".i2p"를 추가합니다. 클라이언트는 응답에서 ".i2p"가 추가되는 것을 요구해서는 안 됩니다.

다른 응답 키와 값들은 표준 비트토렌트와 동일합니다.

---

## 컴팩트 트래커 응답

압축 응답에서 "peers" 딕셔너리 키의 값은 단일 바이트 문자열이며, 길이는 32바이트의 배수입니다. 이 문자열은 피어들의 바이너리 [Destination](/docs/specs/common-structures/#struct_Destination)에 대한 연결된 [32바이트 SHA-256 해시](/docs/specs/common-structures/#type_Hash)를 포함합니다. 이 해시는 tracker에 의해 계산되어야 하며, destination 강제 적용(아래 참조)이 사용되는 경우는 예외로, 이 경우 X-I2P-DestHash 또는 X-I2P-DestB32 HTTP 헤더로 전달된 해시가 바이너리로 변환되어 저장될 수 있습니다. peers 키는 없을 수도 있고, peers 값이 길이 0일 수도 있습니다.

클라이언트와 tracker 모두에서 압축 응답 지원은 선택사항이지만, 명목상 응답 크기를 90% 이상 줄여주므로 적극 권장됩니다.

---

## 목적지 강제 적용

일부 I2P bittorrent 클라이언트는 자체 tunnel을 통해 announce하지만 전부는 아닙니다. Tracker는 이를 요구하고 I2PTunnel HTTP Server tunnel에서 추가한 HTTP 헤더를 사용하여 클라이언트의 [Destination](/docs/specs/common-structures/#struct_Destination)을 검증함으로써 스푸핑을 방지할 수 있습니다. 헤더는 X-I2P-DestHash, X-I2P-DestB64, X-I2P-DestB32이며, 이들은 같은 정보를 다른 형식으로 나타낸 것입니다. 이러한 헤더는 클라이언트가 스푸핑할 수 없습니다. Destination을 강제하는 tracker는 ip announce 매개변수를 전혀 요구할 필요가 없습니다.

여러 클라이언트가 자체 tunnel 대신 HTTP 프록시를 사용하여 공지를 수행하므로, destination 강제 적용은 해당 클라이언트들이 자체 tunnel을 통한 공지 방식으로 전환되기 전까지는 해당 클라이언트들의 사용을 방지합니다.

안타깝게도 네트워크가 성장함에 따라 악의적인 행동의 양도 증가할 것이므로, 결국 모든 tracker가 destination을 강제할 것으로 예상됩니다. tracker와 클라이언트 개발자 모두 이를 예상해야 합니다.

---

## 호스트 이름 알림

토렌트 파일의 공지 URL 호스트 이름은 일반적으로 [I2P 명명 표준](/docs/overview/naming/)을 따릅니다. 주소록의 호스트 이름과 ".b32.i2p" Base 32 호스트 이름 외에도, 전체 Base 64 Destination(".i2p"가 추가되거나 추가되지 않은 형태)도 지원되어야 합니다. 비공개 tracker는 이러한 형식 중 어떤 것으로든 자신의 호스트 이름을 인식해야 합니다.

익명성을 보호하기 위해, 클라이언트는 일반적으로 토렌트 파일에서 I2P가 아닌 announce URL을 무시해야 합니다.

---

## 클라이언트 연결

클라이언트 간 연결은 TCP를 통한 표준 프로토콜을 사용합니다. 현재 uTP 통신을 지원하는 I2P 클라이언트는 알려져 있지 않습니다.

I2P는 위에서 설명한 바와 같이 주소로 387+ 바이트 [Destinations](/docs/specs/common-structures/#struct_Destination)를 사용합니다.

클라이언트가 destination의 해시만 가지고 있는 경우 (compact 응답이나 PEX에서 얻은 것과 같이), Base 32로 인코딩하고 ".b32.i2p"를 붙인 다음 Naming Service에 질의하여 조회를 수행해야 하며, 이는 사용 가능한 경우 전체 Destination을 반환합니다.

클라이언트가 비압축 응답에서 받은 피어의 전체 Destination을 가지고 있다면, 연결 설정에서 이를 직접 사용해야 합니다. Destination을 다시 Base 32 해시로 변환하여 조회하지 마세요. 이는 매우 비효율적입니다.

---

## 교차 네트워크 방지

익명성을 보호하기 위해 I2P bittorrent 클라이언트는 일반적으로 I2P가 아닌 announce나 피어 연결을 지원하지 않습니다. I2P HTTP outproxy는 종종 announce를 차단합니다. bittorrent 트래픽을 지원하는 알려진 SOCKS outproxy는 없습니다.

HTTP inproxy를 통한 비I2P 클라이언트의 사용을 방지하기 위해, I2P tracker들은 종종 X-Forwarded-For HTTP 헤더가 포함된 접근이나 announce를 차단합니다. Tracker는 IPv4 또는 IPv6 IP가 포함된 표준 네트워크 announce를 거부하고, 응답에서 이를 전달하지 않아야 합니다.

---

## PEX

I2P PEX는 ut_pex를 기반으로 합니다. ut_pex의 공식 사양이 없는 것으로 보이므로, 도움을 위해 libtorrent 소스를 검토해야 할 수도 있습니다. 이는 [확장 핸드셰이크](http://www.bittorrent.org/beps/bep_0010.html)에서 "i2p_pex"로 식별되는 확장 메시지입니다. 최대 3개의 키 "added", "added.f", "dropped"를 가진 bencoded 딕셔너리를 포함합니다. added와 dropped 값은 각각 단일 바이트 문자열로, 길이는 32바이트의 배수입니다. 이러한 바이트 문자열들은 peer들의 바이너리 [Destinations](/docs/specs/common-structures/#struct_Destination)의 SHA-256 해시를 연결한 것입니다. 이는 위에서 지정된 i2p compact 응답 형식의 peers 딕셔너리 값과 동일한 형식입니다. added.f 값은 있는 경우 ut_pex에서와 동일합니다.

---

## DHT

DHT 지원은 버전 0.9.2부터 i2psnark 클라이언트에 포함되어 있습니다. [BEP 5](http://www.bittorrent.org/beps/bep_0005.html)와의 주요 차이점들이 아래에 설명되어 있으며, 변경될 수 있습니다. DHT를 지원하는 클라이언트를 개발하고자 하는 경우 I2P 개발자에게 문의하시기 바랍니다.

표준 DHT와 달리, I2P DHT는 옵션 핸드셰이크의 비트나 PORT 메시지를 사용하지 않습니다. 이는 [확장 핸드셰이크](http://www.bittorrent.org/beps/bep_0010.html)에서 "i2p_dht"로 식별되는 확장 메시지로 광고됩니다. 이 메시지는 "port"와 "rport"라는 두 개의 키를 가진 bencoded 딕셔너리를 포함하며, 둘 다 정수 값입니다.

compact node info에 나열된 UDP (datagram) 포트는 응답 가능한 (서명된) 데이터그램을 수신하는 데 사용됩니다. 이는 announce를 제외한 쿼리에 사용됩니다. 이를 "query port"라고 합니다. 이는 확장 메시지의 "port" 값입니다. 쿼리는 [I2CP](/docs/specs/i2cp/) 프로토콜 번호 17을 사용합니다.

해당 UDP 포트에 추가하여, 쿼리 포트 + 1과 같은 두 번째 데이터그램 포트를 사용합니다. 이는 응답, 오류, 그리고 공지를 위한 서명되지 않은 (원시) 데이터그램을 수신하는 데 사용됩니다. 응답에는 쿼리에서 전송된 토큰이 포함되어 있어 서명할 필요가 없기 때문에 이 포트는 효율성을 증대시킵니다. 우리는 이를 "응답 포트"라고 부릅니다. 이는 확장 메시지의 "rport" 값입니다. 쿼리 포트 + 1이어야 합니다. 응답과 공지는 [I2CP](/docs/specs/i2cp/) 프로토콜 번호 18을 사용합니다.

컴팩트 피어 정보는 4바이트 IP + 2바이트 포트 대신 32바이트(32바이트 SHA256 해시)입니다. 피어 포트는 없습니다. 응답에서 "values" 키는 문자열 목록이며, 각각은 단일 컴팩트 피어 정보를 포함합니다.

Compact node info는 20바이트 Node ID + 4바이트 IP + 2바이트 포트 대신 54바이트(20바이트 Node ID + 32바이트 SHA256 Hash + 2바이트 포트)입니다. 응답에서 "nodes" 키는 연결된 compact node info가 포함된 단일 바이트 문자열입니다.

보안 노드 ID 요구사항: 다양한 DHT 공격을 더 어렵게 만들기 위해, 노드 ID의 첫 4바이트는 destination Hash의 첫 4바이트와 일치해야 하고, 노드 ID의 다음 2바이트는 destination hash의 다음 2바이트를 포트와 배타적 OR 연산한 값과 일치해야 합니다.

토렌트 파일에서 trackerless 토렌트 딕셔너리의 "nodes" 키는 미정입니다. 호스트 문자열과 포트 정수를 포함하는 리스트들의 리스트 대신, 32바이트 바이너리 문자열들(SHA256 해시)의 리스트가 될 수 있습니다. 대안: 연결된 해시들로 구성된 단일 바이트 문자열, 또는 문자열들만의 리스트.

---

## 데이터그램 (UDP) 트래커

I2P의 UDP announce 사양은 2025년 6월에 확정되었습니다. 다양한 I2P 클라이언트와 tracker에서의 지원은 2025년 후반에 순차적으로 출시될 예정입니다. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와의 차이점은 [UDP announce 사양](/docs/specs/udp-announces/)에 문서화되어 있습니다. 이 사양은 또한 [새로운 Datagram 2/3 형식](/docs/specs/datagrams/) 지원을 요구합니다.

---

## 추가 정보

빠른 집합(fast set)을 계산하기 위한 예비 사양은 [제안 172](/proposals/172-bep6-allowed-fast)에 있습니다.

---

## 추가 정보

- I2P bittorrent 표준은 일반적으로 [zzz.i2p](http://zzz.i2p/)에서 논의됩니다.
- 현재 tracker 소프트웨어 기능에 대한 차트도 [해당 사이트에서 확인할 수 있습니다](http://zzz.i2p/files/trackers.html).
- [I2P bittorrent FAQ](http://forum.i2p/viewtopic.php?t=2068)
- [I2P에서의 DHT 논의](http://zzz.i2p/topics/812)
