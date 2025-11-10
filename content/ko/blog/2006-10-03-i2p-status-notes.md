---
title: "2006-10-03자 I2P 상태 노트"
date: 2006-10-03
author: "jr"
description: "네트워크 성능 분석, CPU 병목 현상 조사, Syndie 1.0 릴리스 계획 수립 및 분산 버전 관리 평가"
categories: ["status"]
---

여러분 안녕하세요, 이번 주 상태 노트는 늦었습니다.

* Index

1) 네트워크 상태 2) router 개발 상태 3) Syndie의 취지 계속 4) Syndie 개발 상태 5) 분산 버전 관리 6) ???

* 1) Net status

지난 1~2주 동안 irc 및 기타 서비스는 비교적 안정적이었으나, dev.i2p/squid.i2p/www.i2p/cvs.i2p에서는 (일시적인 운영체제 관련 문제로 인해) 몇 가지 작은 장애가 있었습니다. 현재로서는 상황이 안정적인 상태로 보입니다.

* 2) Router dev status

Syndie 논의의 다른 한편은 '그렇다면 그게 router에는 어떤 의미인가요?'라는 것이고, 이에 답하기 위해 현재 router 개발의 현황이 어떤지 간단히 설명드리겠습니다.

전반적으로, router가 1.0에 도달하지 못하게 막는 것은 제 관점에서는 익명성 특성이 아니라 성능입니다. 물론 개선해야 할 익명성 관련 이슈들이 있지만, 익명 네트워크 치고는 꽤 괜찮은 성능을 내고 있음에도 현재 성능은 더 폭넓은 활용을 하기에 충분하지 않습니다. 게다가 네트워크의 익명성을 향상시키는 것만으로 성능이 좋아지지는 않습니다(제가 떠올릴 수 있는 대부분의 경우, 익명성 향상은 처리량을 낮추고 지연 시간을 늘립니다). 따라서 먼저 성능 문제를 해결해야 합니다. 성능이 부족하다면, 익명성 기법이 아무리 강력하더라도 전체 시스템은 충분하지 않기 때문입니다.

그렇다면 우리의 성능을 제한하는 요인은 무엇일까요? 의외로 CPU 사용량인 것으로 보입니다. 왜 그런지 정확히 살펴보기 전에, 먼저 약간 더 배경을 설명하겠습니다.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

따라서 router에는 여러 계층(티어)이 필요합니다 - 일부는 전 세계에서 접근 가능하며 대역폭 상한이 높은 것(티어 A), 일부는 그렇지 않은 것(티어 B). 이는 사실상 netDb의 capacity 정보로 이미 구현되어 있으며, 하루이틀 전 기준으로 티어 B 대 티어 A의 비율은 대략 3대 1이었습니다 (cap L, M, N 또는 O의 router가 93대, cap K가 278대).

Now, there are basically two scarce resources to be managed in tier A - bandwidth and CPU. Bandwidth can be managed by the usual means (split load across a wide pool, have some peers handle insane amounts [e.g. those on T3s], and reject or throttle individual tunnels and connections).

CPU 사용량을 관리하는 일은 더 어렵다. 티어 A router에서 관찰되는 주요 CPU 병목은 tunnel 구축 요청의 복호화다. 대형 router는 이 작업에 의해 완전히 점유될 수 있으며(실제로 그렇게 되고 있다) - 예를 들어, 내 router 중 하나의 전체 기간 평균 tunnel 복호화 시간은 225ms이고, 전체 기간 *평균* tunnel 요청 복호화 빈도는 60초당 254회, 즉 초당 4.2회다. 이 둘을 단순히 곱해 보기만 해도 CPU의 95%가 tunnel 요청 복호화에만 소비된다는 것을 보여 준다(게다가 이는 이벤트 수의 급증은 고려하지 않은 것이다). 그 router는 여전히 어떻게든 한 번에 4-6000개의 tunnel에 참여하면서, 복호화된 요청의 약 80%를 수락한다.

안타깝게도, 그 router의 CPU에 부하가 매우 심하기 때문에, 요청이 복호화되기도 전에 상당수의 tunnel 빌드 요청을 버릴 수밖에 없습니다(그렇지 않으면 요청들이 대기열에 너무 오래 머물러, 설령 수락되더라도 원래 요청자는 그것들이 손실되었거나 부하가 너무 커서 어차피 아무것도 할 수 없다고 여겼을 것입니다). 그런 관점에서 보면, 그 router의 80% 수락률은 훨씬 더 나빠 보입니다 - 운영 기간 동안 약 25만 건의 요청을 복호화했으며(즉, 약 20만 건이 수락되었다는 뜻), CPU 과부하로 인해 복호화 대기열에서 약 43만 건의 요청을 버려야 했습니다(그 결과 80% 수락률이 30%로 떨어진 셈입니다).

해결책은 tunnel 요청 복호화에 필요한 관련 CPU 비용을 줄이는 방향인 것으로 보입니다. CPU 시간을 10배 줄일 수 있다면, 티어 A router의 처리 용량이 크게 늘어나 거부(명시적 거부와 요청 드롭으로 인한 묵시적 거부 모두)가 줄어들 것입니다. 이는 다시 tunnel 구축 성공률을 높여 lease(리스) 만료 빈도를 낮추고, 결과적으로 tunnel 재구축으로 인한 네트워크의 대역폭 부하를 줄이게 됩니다.

이를 수행하는 한 가지 방법은 tunnel 빌드 요청에서 사용하는 2048bit Elgamal을, 이를테면 1024bit 또는 768bit로 바꾸는 것이다. 그러나 그 경우의 문제는 tunnel 빌드 요청 메시지의 암호를 깨면 tunnel의 전체 경로를 알게 된다는 점이다. 설령 이 방식을 택한다 해도 얼마나 이득일까? 복호화 시간이 한 자릿수(약 10배) 개선되더라도, tier B 대 tier A의 비율이 한 자릿수(약 10배) 늘어나는 것(일명 프리라이더 문제)으로 그 효과가 상쇄될 수 있고, 그러면 우리는 막히게 된다. 우리는 512 또는 256bit Elgamal로까지 낮출 수는 없기 때문이다(그리고 그런 채로 거울 속의 자신을 볼 수도 없으니까 ;)

하나의 대안은 더 약한 암호화를 사용하되, 새로운 tunnel 빌드 과정에서 우리가 추가했던 패킷 카운팅 공격에 대한 보호를 포기하는 것이다. 그렇게 하면 Tor와 유사한 망원경식 tunnel에서 전적으로 일시적인 협상 키를 사용할 수 있다 (다만, 다시 말하지만, 서비스를 식별하는 아주 단순한 수동적 패킷 카운팅 공격에 tunnel 생성자가 노출된다).

또 다른 아이디어는 netDb에 더욱 명시적인 부하 정보를 게시하고 활용하여, 클라이언트가 위에서와 같이 높은 대역폭의 router가 들여다보지도 않고 tunnel 요청 메시지의 60%를 드롭하는 상황을 보다 정확하게 감지할 수 있게 하는 것입니다. 이 방향으로 시도해 볼 만한 몇 가지 실험이 있으며, 이는 완전한 하위 호환성을 유지한 채 수행할 수 있으므로, 머지않아 이를 보게 될 것입니다.

그래서, 현시점에서 제가 보기에는 그것이 router/네트워크의 병목입니다. 이를 어떻게 해결할 수 있을지에 대한 모든 제안을 매우 감사히 받겠습니다.

* 3) Syndie rationale continued

포럼에 Syndie와 그것이 전반적인 구도에서 어떤 위치를 차지하는지에 관한 알찬 게시물이 올라왔습니다 - <http://forum.i2p.net/viewtopic.php?t=1910>에서 확인해 보세요

또한, 현재 작업 중인 Syndie 문서에서 두 가지 발췌를 강조해서 소개하고자 합니다. 먼저, irc(그리고 아직 공개되지 않은 FAQ)에서:

<bar> 내가 계속 생각해온 질문은, 나중에 누가 Syndie 프로덕션 서버/아카이브를 호스팅할 만큼        배짱이 클까?  <bar> 그게 오늘날 eepsites(I2P Sites)만큼        추적하기 쉬워지지 않을까?  <jrandom> 공개 Syndie 아카이브는 포럼에 게시된 콘텐츠를        *읽을* 수 있는 능력이 없습니다, 포럼이 그렇게 할 수 있도록 하는 키를        공개하지 않는 한  <jrandom> 그리고 usecases.html의 두 번째 단락을 보세요  <jrandom> 물론, 아카이브를 호스팅하는 이들이 포럼을 내리라는 법적        명령을 받으면 아마 그렇게 할 것입니다  <jrandom> (하지만 그렇게 되면 사람들은 포럼 운영을 방해하지 않고        다른 아카이브로 옮길 수 있습니다)  <void> 그래, 마이그레이션이        다른 매체로 이뤄질 때도 끊김 없을 거라는 사실을 언급해야 해  <bar> 내 아카이브가 종료되면, 내 전체 포럼을 새로운        곳에 업로드할 수 있지?  <jrandom> 맞아 bar  <void> 마이그레이션하는 동안 두 가지 방법을 동시에 사용할 수 있어  <void> 그리고 누구나 그 매체들을 동기화할 수 있어  <jrandom> 맞아 void

(아직 공개되지 않은) Syndie usecases.html의 관련 섹션은 다음과 같습니다:

많은 다양한 그룹들이 종종 토론을 온라인 포럼으로 조직하고자 하지만, 전통적인 포럼(웹사이트, BBS 등)의 중앙집중적 특성은 문제가 될 수 있다. 예를 들어, 포럼을 호스팅하는 사이트는 서비스 거부(DoS) 공격이나 행정적 조치로 오프라인으로 중단될 수 있다. 또한 단일 호스트는 그룹의 활동을 모니터링하기 쉬운 단일 지점을 제공하므로, 포럼이 가명성을 갖춘 경우에도 그 가명들이 개별 메시지를 게시하거나 읽은 IP와 연결될 수 있다.

게다가 포럼은 분산되어 있을 뿐만 아니라, 임시(ad-hoc) 방식으로 구성되면서도 다른 조직화 기법들과 완전히 호환됩니다. 즉, 일부 소규모 그룹은 한 가지 기법(위키 사이트에 메시지를 붙여넣어 배포하는 방식)을 사용해 포럼을 운영할 수 있고, 다른 그룹은 또 다른 기법(OpenDHT 같은 분산 해시 테이블에 메시지를 게시하는 방식)을 사용해 포럼을 운영할 수 있으며, 두 가지 기법을 모두 아는 사람이 있다면 두 포럼을 서로 동기화할 수 있습니다. 이렇게 하면 위키 사이트만 알던 사람과 OpenDHT 서비스만 알던 사람이 서로에 대해 아무것도 모른 채로도 대화할 수 있습니다. 더 나아가 Syndie는 개별 cell(소그룹)이 전체 조직과 소통하는 동안 자신의 노출 범위를 스스로 제어할 수 있게 합니다.

* 4) Syndie dev status

최근 Syndie에 많은 진전이 있었고, IRC 채널의 사용자들에게 알파 릴리스 7개를 배포했습니다. 스크립팅 가능한 인터페이스의 주요 문제 대부분이 해결되었으며, 이달 말에 Syndie 1.0을 릴리스할 수 있기를 기대하고 있습니다.

내가 방금 "1.0"이라고 말했나요? 그럼요! Syndie 1.0은 텍스트 기반 애플리케이션이 될 것이며, mutt나 tin 같은 다른 텍스트 기반 앱들의 사용성과는 비교조차 되지 않겠지만, 모든 기능을 제공하고, HTTP 및 파일 기반 신디케이션 전략을 지원하며, 바라건대 잠재적 개발자들에게 Syndie의 역량을 보여줄 것입니다.

현재로서는 사람들이 자신의 아카이브와 읽기 습관을 더 잘 정리할 수 있도록 하는 Syndie 1.1 릴리스를 임시로 계획하고 있으며, 일부 검색 기능(간단한 검색과 어쩌면 lucene의 전문 검색)을 통합하는 1.2 릴리스도 고려하고 있습니다. Syndie 2.0은 아마 첫 GUI(그래픽 사용자 인터페이스) 릴리스가 될 것이고, 브라우저 플러그인은 3.0과 함께 제공될 것입니다. 물론 추가 아카이브 및 메시지 배포 네트워크에 대한 지원도 구현되는 대로 제공될 것입니다(freenet, mixminion/mixmaster/smtp, opendht, gnutella 등).

하지만 텍스트 기반 앱은 사실상 기술 애호가를 위한 것이라, 일부가 원하는 것처럼 Syndie 1.0이 세상을 뒤흔드는 제품이 되지는 않으리라는 점은 알고 있습니다. 다만 '1.0'을 최종 릴리스로 보는 습관을 버리고, 대신 시작으로 여겼으면 합니다.

* 5) Distributed version control

So far, I've been mucking around with subversion as the vcs for Syndie, even though I'm only really fluent in CVS and clearcase. This is because I'm offline most of the time, and even when I am online, dialup is slow, so subversion's local diff/revert/etc has been quite handy. However, yesterday void poked me with the suggestion that we look into one of the distributed systems instead.

몇 년 전에 I2P용 VCS(버전 관리 시스템)를 평가할 때 그것들을 살펴보았지만, 오프라인 기능이 필요하지 않았기 때문에(그때는 네트워크 접근성이 좋았습니다) 배워둘 가치가 없다고 보고 채택하지 않았습니다. 이제는 상황이 그렇지 않아서 지금은 그것들을 좀 더 자세히 살펴보고 있습니다.

- From what I can see, darcs, monotone, and codeville are the top

여러 후보 중에서도 darcs의 패치 기반 VCS(버전 관리 시스템)가 특히 매력적으로 보인다. 예를 들어, 나는 모든 작업을 로컬에서 수행한 뒤 gzip'ed(압축한) 및 gpg'ed(암호화/서명한) diff들을 scp로 dev.i2p.net의 Apache 디렉터리에 올릴 수 있고, 다른 사람들은 자신이 선택한 위치에 gzip'ed와 gpg'ed diff를 게시하는 방식으로 자신의 변경 사항을 기여할 수 있다. 릴리스를 태그할 시점이 되면, 릴리스에 포함된 패치들의 집합을 지정하는 darcs diff를 만들고, 다른 것들과 마찬가지로 그 .gz'ed/.gpg'ed diff도 업로드할 것이다(물론 실제 tar.bz2, .exe, .zip 파일도 함께 배포할 것이다 ;).

그리고 특히 흥미로운 점은, 이러한 gzip/gpg 처리된 diff(차분)는 Syndie 메시지에 첨부 파일로 게시될 수 있으며, 그 결과 Syndie는 자체 호스팅이 가능해진다는 것이다.

이런 녀석들 써보신 분 계신가요? 조언 부탁드립니다.

* 6) ???

이번에는 텍스트가 화면 기준으로 24화면 분량뿐이에요(포럼 글 포함) ;)
안타깝게도 회의에는 참석하지 못했지만, 늘 그렇듯 여러분의 아이디어나 제안을 듣고 싶습니다—메일링 리스트나 포럼에 글을 올리시거나 IRC로 들러 주세요.

=jr
