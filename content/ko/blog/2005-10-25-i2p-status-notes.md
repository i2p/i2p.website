---
title: "2005-10-25자 I2P 상태 노트"
date: 2005-10-25
author: "jr"
description: "네트워크가 400-500 피어 규모로 성장, Fortuna PRNG(의사난수 생성기) 통합, GCJ 네이티브 컴파일 지원, i2psnark 경량 토렌트 클라이언트, 그리고 tunnel 부트스트랩 공격 분석을 다루는 주간 업데이트"
categories: ["status"]
---

여러분 안녕하세요, 최전선에서 전하는 추가 소식입니다

* Index

1) 네트워크 상태 2) Fortuna 통합 3) GCJ 상태 4) i2psnark 복귀 5) bootstrapping(초기화 과정) 추가 내용 6) 바이러스 조사 7) ???

* 1) Net status

지난주 네트워크 상황은 꽤 좋았습니다 - 전반적으로 안정적이고, 처리량도 정상이며, 피어 수는 400~500 범위로 계속 늘고 있습니다. 0.6.1.3 릴리스 이후에도 상당한 개선이 있었고, 이는 성능과 신뢰성에 영향을 주므로 이번 주 후반에 0.6.1.4 릴리스를 내놓을 것으로 예상합니다.

* 2) Fortuna integration

Casey Marshall의 빠른 수정 [1] 덕분에 GNU-Crypto의 Fortuna [2] 의사난수 생성기를 통합할 수 있었습니다. 이로써 blackdown JVM에서 겪던 많은 좌절의 원인이 제거되었고, GCJ와도 원활하게 작업할 수 있게 되었습니다. Fortuna를 I2P에 통합하는 것은 smeghead가 "pants"('ant'(Apache Ant 빌드 도구) 기반 'portage'(Gentoo의 Portage 스타일))를 개발한 주요한 이유 중 하나였으므로, 이제 우리는 또 하나의 성공적인 pants 활용을 하게 되었습니다 :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

메일링 리스트 [3]에서 언급했듯이, 이제 GCJ [4]로 router와 대부분의 클라이언트를 원활하게 실행할 수 있습니다. 다만 웹 콘솔 자체는 아직 완전히 동작하지 않으므로, router.config로 router 설정을 직접 해야 합니다(그래도 약 1분 정도 지나면 Just Work 하면서 tunnel을 자동으로 가동할 것입니다). GCJ를 우리의 릴리스 계획에 어떻게 포함할지는 아직 완전히 확신하지 못하지만, 현재로서는 순수 Java를 배포하되 Java와 네이티브로 컴파일된 버전 둘 다를 지원하는 방향으로 생각하고 있습니다. 서로 다른 OS와 라이브러리 버전에 맞춰 수많은 다른 빌드를 빌드하고 배포해야 하는 것은 꽤 번거롭습니다. 이 부분에 대해 강한 의견이 있으신가요?

GCJ 지원의 또 다른 장점은 C/C++/Python 등에서 스트리밍 라이브러리를 사용할 수 있다는 것입니다. 그런 종류의 통합 작업을 누가 진행하고 있는지는 모르겠지만, 아마도 충분히 해볼 만한 일일 테니, 그쪽에서 작업해 보고 싶다면 알려 주세요!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

i2p-bt는 I2P로 포팅된 BitTorrent 클라이언트 가운데 처음으로 널리 사용된 것이었지만, 사실 꽤 오래전에 eco가 snark[5]를 포팅해 선수를 쳤습니다. 안타깝게도 최신 상태를 유지하지 못했고 다른 익명 BitTorrent 클라이언트와의 호환성도 유지하지 못해 한동안 사실상 사라졌습니다. 하지만 지난주에 i2p-bt<->sam<->streaming lib<->i2cp 체인 어딘가에서 성능 문제를 다루는 데 애를 먹으면서, mjw의 원래 snark 코드로 옮겨가 간단한 포팅[6]을 했습니다. java.net.*Socket 호출을 I2PSocket* 호출로, InetAddresses를 Destinations(I2P 목적지 주소)로, 그리고 URLs를 EepGet 호출로 바꾸었습니다. 그 결과, 이제 I2P 릴리스에 함께 제공할 아주 작은 명령줄 BitTorrent 클라이언트(컴파일 시 약 60KB)가 나왔습니다.

Ragnarok은 블록 선택 알고리즘을 개선하기 위해 이미 코드를 파고들기 시작했으며, 0.6.2 릴리스 전에 그 안에 웹 인터페이스와 멀티토렌트 기능을 모두 추가할 수 있기를 바랍니다. 도움이 되고 싶다면 연락 주세요! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

최근 메일링 리스트가 Michael의 tunnel 구축에 대한 새로운 시뮬레이션과 분석으로 꽤 활발합니다. Toad, Tom, polecat이 몇 가지 좋은 아이디어를 제시하며 논의는 계속 진행 중이니, 우리가 0.6.2 릴리스에서 개편할 일부 익명성 관련 설계 이슈들의 트레이드오프에 대해 의견을 보태고 싶다면 살펴보세요 [7].

시각적 볼거리에 관심 있는 분들을 위해 Michael이 준비한 것도 있습니다, 해당 공격이 당신을 식별할 가능성이 어느 정도인지 - 네트워크에서 그들이 통제하는 비율의 함수[8], 그리고 당신의 tunnel이 얼마나 활발한지의 함수[9]로 보여 주는 시뮬레이션입니다

(잘했어, Michael. 고마워!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     ("i2p tunnel bootstrap attack" 스레드 참조) [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

특정 I2P 지원 애플리케이션과 함께 배포되고 있는 잠재적인 악성코드 문제에 대해 일부 논의가 있었으며, Complication이 이를 심층적으로 조사해 훌륭한 일을 해냈습니다. 관련 데이터는 공개되어 있으므로, 각자 판단하실 수 있습니다. [10]

Complication 님, 이에 대해 해 주신 모든 조사에 감사드립니다!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

보시다시피 정말 많은 일이 진행 중이지만, 제가 회의에 이미 늦어서 아마 이걸 저장하고 보내야겠죠, 그쵸? #i2p에서 봐요 :)

=jr
