---
title: "명명 및 주소록"
description: "I2P가 사람이 읽을 수 있는 호스트명을 destination에 매핑하는 방법"
slug: "naming"
aliases:
  - "/ko/docs/specs/naming"
  - "/ko/docs/specs/naming/"
  - "/ko/docs/naming"
  - "/ko/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## 개요

I2P는 로컬 이름-목적지 매핑을 기반으로 작동하도록 설계된 범용 명명 라이브러리와 기본 구현체, 그리고 [주소록](#address-book)이라는 애드온 애플리케이션을 함께 제공합니다. I2P는 또한 Tor의 .onion 주소와 유사한 [Base32 호스트명](#base32-names)을 지원합니다.

주소록은 신뢰망 기반의 안전하고 분산된 인간이 읽을 수 있는 명명 시스템으로, 모든 인간이 읽을 수 있는 이름이 전역적으로 고유해야 한다는 요구사항 대신 지역적 고유성만을 보장함으로써 절충점을 제공합니다. I2P의 모든 메시지는 목적지로 암호학적 주소가 지정되지만, 서로 다른 사람들이 각자 다른 목적지를 가리키는 "Alice"라는 지역 주소록 항목을 가질 수 있습니다. 사람들은 여전히 신뢰망에서 지정한 피어의 공개 주소록을 가져오거나, 제3자가 제공하는 항목을 추가하거나, (일부 사람들이 선착순 등록 시스템을 사용하여 일련의 공개 주소록을 조직하는 경우) 이러한 주소록을 네임 서버로 취급하여 전통적인 DNS를 모방하는 방식으로 새로운 이름을 발견할 수 있습니다.

참고: I2P 네이밍 시스템의 배경 논리, 그에 대한 일반적인 반대 논거 및 가능한 대안에 대해서는 [네이밍 논의](/docs/legacy/naming/) 페이지를 참조하세요.

---

## 이름 시스템 구성 요소

I2P에는 중앙 명명 기관이 없습니다. 모든 호스트명은 로컬입니다.

네이밍 시스템은 매우 간단하며, 대부분이 router 외부의 애플리케이션에서 구현되지만 I2P 배포판에 번들로 제공됩니다. 구성 요소는 다음과 같습니다:

1. 조회를 수행하고 [Base32 호스트명](#base32-names)을 처리하는 로컬 [naming service](#naming-services).
2. router에 조회를 요청하고 실패한 조회를 지원하기 위해 사용자를 원격 jump service로 안내하는 [HTTP proxy](#http-proxy).
3. 사용자가 로컬 hosts.txt에 호스트를 추가할 수 있게 해주는 HTTP [host-add forms](#host-add-services).
4. 자체 조회 및 리다이렉션을 제공하는 HTTP [jump services](#jump-services).
5. HTTP를 통해 검색된 외부 호스트 목록을 로컬 목록과 병합하는 [address book](#address-book) 애플리케이션.
6. address book 설정 및 로컬 호스트 목록 보기를 위한 간단한 웹 프론트엔드인 [SusiDNS](#susidns) 애플리케이션.

---

## 명명 서비스

I2P의 모든 destination은 516바이트(또는 그 이상)의 키입니다. (정확히 말하면, 256바이트 공개 키 + 128바이트 서명 키 + 3바이트 이상의 인증서로 구성되며, Base64 표현에서는 516바이트 이상입니다. 현재 서명 타입 표시를 위해 null이 아닌 [Certificates](/docs/legacy/naming/#certificates)가 사용되고 있습니다. 따라서 최근에 생성된 destination의 인증서는 3바이트보다 큽니다.)

애플리케이션(i2ptunnel 또는 HTTP 프록시)이 이름으로 목적지에 접근하려고 할 때, router는 매우 간단한 로컬 조회를 통해 해당 이름을 해결합니다.

### Hosts.txt 네이밍 서비스

hosts.txt 명명 서비스는 텍스트 파일을 통해 간단한 선형 검색을 수행합니다. 이 명명 서비스는 0.8.8 릴리스까지 기본값이었으며, 이후 Blockfile 명명 서비스로 교체되었습니다. hosts.txt 형식은 파일이 수천 개의 항목으로 증가한 후 너무 느려졌습니다.

호스트 이름을 찾아서 516바이트 destination key로 변환하기 위해 세 개의 로컬 파일을 순서대로 선형 검색합니다. 각 파일은 간단한 [설정 파일 형식](/docs/specs/configuration/)으로 되어 있으며, hostname=base64 형태로 한 줄에 하나씩 기록되어 있습니다. 해당 파일들은 다음과 같습니다:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile 네이밍 서비스

Blockfile Naming Service는 hostsdb.blockfile이라는 단일 데이터베이스 파일에 여러 "주소록"을 저장합니다. 이 Naming Service는 릴리스 0.8.8부터 기본값입니다.

blockfile은 단순히 여러 정렬된 맵(키-값 쌍)을 디스크에 저장하는 방식으로, skiplist로 구현됩니다. blockfile 형식은 [Blockfile 페이지](/docs/specs/blockfile/)에 명시되어 있습니다. 이는 컴팩트한 형식으로 빠른 Destination 조회를 제공합니다. blockfile 오버헤드가 상당하지만, destination들은 hosts.txt 형식에서와 같이 Base 64가 아닌 바이너리로 저장됩니다. 또한 blockfile은 고급 주소록 기능을 구현하기 위해 각 항목에 대한 임의의 메타데이터 저장(추가 날짜, 소스, 주석 등) 기능을 제공합니다. blockfile 저장 요구사항은 hosts.txt 형식에 비해 적당한 증가이며, blockfile은 조회 시간을 약 10배 단축시킵니다.

생성 시 네이밍 서비스는 hosts.txt 네이밍 서비스에서 사용되는 세 개의 파일에서 항목을 가져옵니다. 블록파일은 privatehosts.txt, userhosts.txt, hosts.txt라는 이름의 순서대로 검색되는 세 개의 맵을 유지하여 이전 구현을 모방합니다. 또한 빠른 역방향 조회를 구현하기 위해 역방향 조회 맵을 유지합니다.

### 기타 네이밍 서비스 기능

조회는 대소문자를 구분하지 않습니다. 첫 번째 일치 항목이 사용되며, 충돌은 감지되지 않습니다. 조회에서 명명 규칙의 강제는 없습니다. 조회는 몇 분 동안 캐시됩니다. Base 32 해석은 [아래에 설명되어 있습니다](#base32-names). Naming Service API의 전체 설명은 [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)를 참조하세요. 이 API는 0.8.7 릴리스에서 추가 및 제거, 호스트명과 함께 임의 속성 저장, 기타 기능을 제공하기 위해 크게 확장되었습니다.

### 대안 및 실험적 네이밍 서비스

naming 서비스는 `i2p.naming.impl=class` 설정 속성으로 지정됩니다. 다른 구현도 가능합니다. 예를 들어, router 내에서 네트워크를 통한 실시간 조회(DNS와 유사한) 기능에 대한 실험적인 기능이 있습니다. 자세한 정보는 [토론 페이지의 대안들](/docs/legacy/naming/#alternatives)을 참조하세요.

HTTP 프록시는 '.i2p'로 끝나는 모든 호스트명에 대해 router를 통해 조회를 수행합니다. 그렇지 않으면 구성된 HTTP outproxy로 요청을 전달합니다. 따라서 실제로는 모든 HTTP (I2P 사이트) 호스트명이 의사 최상위 도메인 '.i2p'로 끝나야 합니다.

router가 호스트명을 해결하지 못하면, HTTP 프록시는 여러 "점프" 서비스에 대한 링크와 함께 오류 페이지를 사용자에게 반환합니다. 자세한 내용은 아래를 참조하세요.

---

## .i2p.alt 도메인

우리는 이전에 [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html)에 명시된 절차에 따라 [.i2p TLD 예약을 신청](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)했습니다. 그러나 이 신청과 다른 모든 신청들이 거부되었고, RFC 6761은 "실수"였다고 선언되었습니다.

GNUnet 팀과 다른 개발자들의 수년간의 작업 끝에, .alt 도메인은 2023년 말 [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html)에서 특수 용도 TLD로 예약되었습니다. IANA에서 승인한 공식 등록기관은 없지만, 주요 비공식 등록기관인 [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html)에 .i2p.alt 도메인을 등록했습니다. 이것이 다른 사람들이 해당 도메인을 사용하는 것을 막지는 않지만, 사용을 억제하는 데 도움이 될 것입니다.

.alt 도메인의 한 가지 장점은 이론적으로 DNS resolver들이 RFC 9476을 준수하도록 업데이트되면 .alt 요청을 전달하지 않게 되어 DNS 유출을 방지할 수 있다는 것입니다. .i2p.alt 호스트명과의 호환성을 위해 I2P 소프트웨어와 서비스들은 .alt TLD를 제거하여 이러한 호스트명을 처리할 수 있도록 업데이트되어야 합니다. 이러한 업데이트는 2024년 상반기에 예정되어 있습니다.

현재로서는 .i2p.alt를 I2P 호스트명의 표시 및 교환을 위한 선호 형식으로 만들 계획은 없습니다. 이는 추가적인 연구와 논의가 필요한 주제입니다.

---

## 주소록

### 들어오는 구독 및 병합

주소록 애플리케이션은 주기적으로 다른 사용자들의 hosts.txt 파일을 가져와서 여러 검사를 거친 후 로컬 hosts.txt와 병합합니다. 이름 충돌은 선착순 기준으로 해결됩니다.

다른 사용자의 hosts.txt 파일을 구독하는 것은 그들에게 어느 정도의 신뢰를 부여하는 것을 의미합니다. 예를 들어, 그들이 새로운 사이트에 대한 새로운 호스트/키 항목을 당신에게 전달하기 전에 자신의 키를 빠르게 입력하여 새로운 사이트를 '하이재킹'하는 것을 원하지 않을 것입니다.

이러한 이유로, 기본적으로 구성되는 유일한 구독은 `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`이며, 이는 I2P 릴리스에 포함된 hosts.txt의 사본을 포함합니다. 사용자는 로컬 주소록 애플리케이션에서 추가 구독을 구성해야 합니다 (subscriptions.txt 또는 [SusiDNS](#susidns)를 통해).

다른 공개 주소록 구독 링크들:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

이러한 서비스의 운영자들은 호스트를 목록에 등재하는 데 있어 다양한 정책을 가질 수 있습니다. 이 목록에 포함되는 것이 보증을 의미하지는 않습니다.

### 명명 규칙

I2P 내에서 호스트 이름에 대한 기술적 제약이 없기를 바라지만, 주소록은 구독으로부터 가져온 호스트 이름에 대해 여러 제한사항을 적용합니다. 이는 기본적인 인쇄상의 합리성과 브라우저와의 호환성, 그리고 보안을 위해 수행됩니다. 규칙은 본질적으로 RFC2396 섹션 3.2.2와 동일합니다. 이러한 규칙을 위반하는 호스트 이름은 다른 router로 전파되지 않을 수 있습니다.

명명 규칙:

- 이름은 가져올 때 소문자로 변환됩니다.
- 이름은 소문자로 변환한 후 기존 userhosts.txt 및 hosts.txt(privatehosts.txt 제외)의 기존 이름과 충돌하는지 확인됩니다.
- 소문자로 변환한 후 [a-z] [0-9] '.' 및 '-'만 포함해야 합니다.
- '.' 또는 '-'로 시작하면 안 됩니다.
- '.i2p'로 끝나야 합니다.
- '.i2p'를 포함하여 최대 67자입니다.
- '..'을 포함하면 안 됩니다.
- '.-' 또는 '-.'을 포함하면 안 됩니다(0.6.1.33부터).
- IDN용 'xn--'을 제외하고는 '--'을 포함하면 안 됩니다.
- Base32 호스트명(*.b32.i2p)은 base 32 사용을 위해 예약되어 있으므로 가져올 수 없습니다.
- 프로젝트 사용을 위해 예약된 특정 호스트명은 허용되지 않습니다(proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p 및 기타).
- 'www.'로 시작하는 호스트명은 권장되지 않으며 일부 등록 서비스에서 거부됩니다. 일부 주소록 구현체는 조회 시 'www.' 접두사를 자동으로 제거합니다. 따라서 'www.example.i2p'를 등록하는 것은 불필요하며, 'www.example.i2p'와 'example.i2p'에 다른 목적지를 등록하면 일부 사용자에게는 'www.example.i2p'에 접근할 수 없게 됩니다.
- 키는 base64 유효성을 검사합니다.
- 키는 hosts.txt(privatehosts.txt 제외)의 기존 키와 충돌하는지 확인됩니다.
- 최소 키 길이 516바이트.
- 최대 키 길이 616바이트(최대 100바이트의 인증서를 고려함).

구독을 통해 받은 이름 중 모든 검사를 통과한 이름은 로컬 네이밍 서비스를 통해 추가됩니다.

호스트명의 '.' 기호는 특별한 의미가 없으며, 실제 명명 체계나 신뢰 계층 구조를 나타내지 않습니다. 'host.i2p'라는 이름이 이미 존재하더라도, 누구든지 자신의 hosts.txt에 'a.host.i2p'라는 이름을 추가할 수 있으며, 이 이름은 다른 사람들의 주소록으로 가져올 수 있습니다. 도메인이 아닌 '소유자'에게 서브도메인을 거부하는 방법(인증서?)과 이러한 방법의 바람직함 및 실현 가능성은 향후 논의할 주제입니다.

국제 도메인 이름(IDN)도 i2p에서 작동합니다 (punycode 'xn--' 형식 사용). Firefox의 주소 표시줄에서 IDN .i2p 도메인 이름이 올바르게 렌더링되도록 하려면, about:config에서 'network.IDN.whitelist.i2p (boolean) = true'를 추가하세요.

주소록 애플리케이션은 privatehosts.txt를 전혀 사용하지 않으므로, 실제로 이 파일은 hosts.txt에 이미 있는 사이트에 대한 개인 별칭이나 "애칭"을 배치하기에 적절한 유일한 장소입니다.

### 고급 구독 피드 형식

릴리스 0.9.26부터 구독 사이트와 클라이언트는 서명을 포함한 메타데이터가 포함된 고급 hosts.txt 피드 프로토콜을 지원할 수 있습니다. 이 형식은 표준 hosts.txt hostname=base64destination 형식과 역호환됩니다. 자세한 내용은 [사양](/docs/specs/subscription/)을 참조하세요.

### 발신 구독

Address Book은 병합된 hosts.txt를 다른 사용자들이 구독을 위해 접근할 수 있는 위치(일반적으로 로컬 I2P 사이트의 홈 디렉토리에 있는 hosts.txt)에 게시합니다. 이 단계는 선택사항이며 기본적으로 비활성화되어 있습니다.

### 호스팅 및 HTTP 전송 문제

주소록 애플리케이션은 eepget과 함께 구독의 웹 서버에서 반환되는 Etag 및/또는 Last-Modified 정보를 저장합니다. 이는 변경사항이 없을 경우 다음 가져오기에서 웹 서버가 '304 Not Modified'를 반환하므로 필요한 대역폭을 크게 줄여줍니다.

그러나 hosts.txt가 변경된 경우 전체 파일이 다운로드됩니다. 이 문제에 대한 논의는 아래를 참조하세요.

정적 hosts.txt 또는 동등한 CGI 애플리케이션을 제공하는 호스트는 Content-Length 헤더와 Etag 또는 Last-Modified 헤더 중 하나를 반드시 제공하도록 강력히 권장됩니다. 또한 서버가 적절한 경우 '304 Not Modified'를 전송하도록 해야 합니다. 이는 네트워크 대역폭을 대폭 줄이고 손상 가능성을 감소시킵니다.

---

## 호스트 서비스 추가

호스트 추가 서비스는 호스트명과 Base64 키를 매개변수로 받아 로컬 hosts.txt에 추가하는 간단한 CGI 애플리케이션입니다. 다른 router들이 해당 hosts.txt를 구독하면, 새로운 호스트명/키가 네트워크를 통해 전파됩니다.

호스트 추가 서비스는 최소한 위에 나열된 주소록 애플리케이션에서 부과하는 제한 사항을 적용하는 것이 권장됩니다. 호스트 추가 서비스는 호스트명과 키에 대해 추가 제한 사항을 부과할 수 있습니다. 예를 들어:

- '서브도메인' 수의 제한.
- 다양한 방법을 통한 '서브도메인' 인증.
- Hashcash 또는 서명된 인증서.
- 호스트 이름 및/또는 콘텐츠의 편집 검토.
- 콘텐츠별 호스트 분류.
- 특정 호스트 이름의 예약 또는 거부.
- 주어진 기간 내 등록 가능한 이름 수 제한.
- 등록과 게시 간의 지연.
- 검증을 위해 호스트가 활성 상태여야 하는 요구사항.
- 만료 및/또는 폐지.
- IDN 스푸핑 거부.

---

## 점프 서비스

jump service는 호스트명을 매개변수로 받아서 `?i2paddresshelper=key` 문자열이 추가된 적절한 URL로 301 리디렉션을 반환하는 간단한 CGI 애플리케이션입니다. HTTP 프록시는 추가된 문자열을 해석하여 해당 키를 실제 목적지로 사용합니다. 또한 프록시는 해당 키를 캐시하므로 재시작할 때까지 address helper가 필요하지 않습니다.

구독과 마찬가지로 점프 서비스를 사용하는 것은 어느 정도의 신뢰를 전제로 한다는 점에 유의하세요. 점프 서비스가 악의적으로 사용자를 잘못된 목적지로 리디렉션할 수 있기 때문입니다.

최상의 서비스를 제공하기 위해, jump 서비스는 여러 hosts.txt 제공자에 구독하여 로컬 호스트 목록을 최신 상태로 유지해야 합니다.

---

## SusiDNS

SusiDNS는 주소록 구독을 설정하고 네 개의 주소록 파일에 접근하기 위한 단순한 웹 인터페이스 프론트엔드입니다. 모든 실제 작업은 '주소록' 애플리케이션에 의해 수행됩니다.

현재 SusiDNS 내에서 주소록 명명 규칙의 시행이 거의 없어서, 사용자가 주소록 구독 규칙에서는 거부될 호스트명을 로컬에서 입력할 수 있습니다.

---

## Base32 이름

I2P는 Tor의 .onion 주소와 유사한 Base32 호스트명을 지원합니다. Base32 주소는 516자로 이루어진 전체 Base64 Destination이나 addresshelper보다 훨씬 짧고 다루기 쉽습니다. 예시: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

Tor에서 주소는 16자(80비트) 또는 SHA-1 해시의 절반입니다. I2P는 52자(256비트)를 사용하여 전체 SHA-256 해시를 나타냅니다. 형식은 {52 chars}.b32.i2p입니다. Tor는 숨겨진 서비스에 대해 동일한 형식인 {52 chars}.onion으로 변환하는 [제안](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)을 가지고 있습니다. Base32는 naming service에서 구현되며, 이는 I2CP를 통해 router에 질의하여 leaseSet을 조회하고 전체 Destination을 가져옵니다. Base32 조회는 Destination이 활성화되어 있고 leaseSet을 게시하고 있을 때만 성공적으로 수행됩니다. 해결 과정에서 netDb 조회가 필요할 수 있기 때문에, 로컬 주소록 조회보다 상당히 오래 걸릴 수 있습니다.

Base32 주소는 호스트명이나 전체 목적지가 사용되는 대부분의 곳에서 사용할 수 있지만, 이름이 즉시 해석되지 않으면 실패할 수 있는 몇 가지 예외가 있습니다. 예를 들어, I2PTunnel은 이름이 목적지로 해석되지 않으면 실패합니다.

---

## 확장 Base32 이름

Extended base 32 이름은 암호화된 lease set을 지원하기 위해 릴리스 0.9.40에서 도입되었습니다. 암호화된 leaseSet의 주소는 ".b32.i2p"를 제외하고 56개 이상의 인코딩된 문자(35개 이상의 디코딩된 바이트)로 식별되며, 이는 기존 base 32 주소의 52개 문자(32바이트)와 비교됩니다. 추가 정보는 제안서 123과 149를 참조하세요.

표준 Base 32("b32") 주소는 목적지의 해시를 포함합니다. 이는 암호화된 ls2(제안 123)에서는 작동하지 않습니다.

암호화된 LS2(proposal 123)에는 전통적인 base 32 주소를 사용할 수 없습니다. 이는 목적지의 해시만을 포함하기 때문입니다. 블라인딩되지 않은 공개키를 제공하지 않습니다. 클라이언트는 leaseset을 가져와서 복호화하기 위해 목적지의 공개키, 서명 타입, 블라인딩된 서명 타입, 그리고 선택적인 비밀키 또는 개인키를 알아야 합니다. 따라서 base 32 주소만으로는 불충분합니다. 클라이언트는 전체 목적지(공개키를 포함하는) 또는 공개키 자체가 필요합니다. 클라이언트가 주소록에 전체 목적지를 가지고 있고, 주소록이 해시를 통한 역방향 조회를 지원한다면, 공개키를 검색할 수 있습니다.

따라서 해시 대신 공개 키를 base32 주소에 넣는 새로운 형식이 필요합니다. 이 형식은 공개 키의 서명 유형과 블라인딩 체계의 서명 유형도 포함해야 합니다.

이 섹션은 이러한 주소들을 위한 새로운 b32 형식을 문서화합니다. 논의 과정에서 이 새로운 형식을 "b33" 주소라고 언급했지만, 실제 새로운 형식은 기존의 ".b32.i2p" 접미사를 그대로 유지합니다.

### 생성 및 인코딩

다음과 같이 {56+ 문자}.b32.i2p (바이너리로 35+ 문자)의 hostname을 구성합니다. 먼저 base 32로 인코딩할 바이너리 데이터를 구성합니다:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
후처리 및 체크섬:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32의 끝에 있는 사용되지 않은 비트는 반드시 0이어야 합니다. 표준 56자(35바이트) 주소에는 사용되지 않은 비트가 없습니다.

### 디코딩 및 검증

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### 비밀키 및 개인키 비트

secret과 private key 비트는 클라이언트, 프록시 또는 기타 클라이언트 측 코드에 leaseset을 복호화하기 위해 secret 및/또는 private key가 필요함을 나타내는 데 사용됩니다. 특정 구현에서는 사용자에게 필요한 데이터를 제공하도록 요청하거나, 필요한 데이터가 누락된 경우 연결 시도를 거부할 수 있습니다.

### 참고사항

- 처음 3바이트를 해시와 XOR하면 제한적인 체크섬 기능을 제공하고, 시작 부분의 모든 base32 문자가 무작위화되도록 보장합니다. 유효한 플래그와 sigtype 조합은 몇 개뿐이므로, 오타가 있으면 유효하지 않은 조합을 생성할 가능성이 높아 거부됩니다.
- 일반적인 경우(1바이트 sigtype, 비밀 없음, 클라이언트별 인증 없음)에서 호스트명은 {56 chars}.b32.i2p가 되며, 35바이트로 디코딩되어 Tor와 동일합니다.
- Tor의 2바이트 체크섬은 1/64K의 거짓 음성률을 가집니다. 3바이트에서 몇 개의 무시되는 바이트를 제외하면, 대부분의 플래그/sigtype 조합이 유효하지 않기 때문에 우리 것은 백만 분의 1에 접근합니다.
- Adler-32는 작은 입력과 작은 변경 사항을 감지하는 데 좋지 않은 선택입니다. 대신 CRC-32를 사용합니다. CRC-32는 빠르고 널리 사용 가능합니다.
- 이 명세의 범위 밖이지만, router와/또는 클라이언트는 공개 키에서 destination으로의 매핑과 그 반대의 매핑을 기억하고 캐시해야 합니다(아마도 영구적으로).
- 길이로 이전 형식과 새 형식을 구분합니다. 기존 b32 주소는 항상 {52 chars}.b32.i2p입니다. 새로운 것은 {56+ chars}.b32.i2p입니다.
- Tor 토론 스레드는 [여기에 있습니다](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- 2바이트 sigtype이 일어날 것이라고 기대하지 마세요. 우리는 아직 13까지만 사용하고 있습니다. 지금 구현할 필요는 없습니다.
- 새로운 형식은 원하는 경우 b32처럼 점프 링크에서 사용하고 점프 서버에서 제공할 수 있습니다.
- 32바이트보다 긴 비밀, 개인 키 또는 공개 키는 DNS 최대 레이블 길이인 63문자를 초과합니다. 브라우저는 아마도 신경 쓰지 않을 것입니다.
- 역호환성 문제는 없습니다. 더 긴 b32 주소는 기존 소프트웨어에서 32바이트 해시로 변환되지 않습니다.
