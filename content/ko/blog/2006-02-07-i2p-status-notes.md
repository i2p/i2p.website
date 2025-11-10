---
title: "I2P Status Notes for 2006-02-07"
date: 2006-02-07
author: "jr"
description: "PRE(프록시 재암호화) 네트워크 테스트 진행 상황, ElGamal 암호화를 위한 짧은 지수 최적화, 그리고 gwebcache를 지원하는 I2Phex 0.1.1.37"
categories: ["status"]
---

안녕 여러분, 또 화요일이 돌아왔네

* Index

1) 네트워크 상태 2) _PRE 네트워크 진행률 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

There haven't been any substantial changes on the live net over the last week, so the live net status hasn't changed much.  On the other hand...

* 2) _PRE net progress

지난주에 0.6.1.10 릴리스를 위한 하위 호환되지 않는 코드를 CVS의 별도 브랜치(i2p_0_6_1_10_PRE)에 커밋하기 시작했고, 일군의 자원봉사자들이 이를 테스트하는 데 도움을 주었다. 이 새로운 _PRE 네트워크는 라이브 네트워크와 통신할 수 없으며, 의미 있는 익명성도 없다(피어가 10개 미만이기 때문). 해당 routers에서 수집한 pen register logs(연결 메타데이터 기록)를 통해 신규 코드와 기존 코드 모두에서 몇 가지 중대한 버그를 추적해 찾아내고 수정했지만, 추가적인 테스트와 개선은 계속되고 있다.

새로운 tunnel 생성 암호화의 한 측면은, 생성자가 각 홉마다 연산량이 큰 비대칭형 암호화를 사전에 수행해야 한다는 점이며, 반면 기존의 tunnel 생성에서는 이전 홉이 tunnel에 참여하기로 동의한 경우에만 암호화를 수행했다. 이러한 암호화에는 로컬 CPU 성능과 tunnel 길이에 따라 400~1000ms 이상 걸릴 수 있다(각 홉마다 완전한 ElGamal 암호화를 수행한다). 현재 _PRE net에서 사용 중인 최적화 중 하나는 짧은 지수(short exponent) [1]의 사용이다 - ElGamal 키의 'x'를 2048비트 대신 228비트 'x'로 사용하며, 이는 이산 로그 문제의 작업량에 맞추기 위해 권장되는 길이이다. 이로 인해 홉당 암호화 시간이 한 자릿수(10배) 규모로 줄었지만, 복호화 시간에는 영향을 주지 않는다.

짧은 지수의 사용에 대해서는 상반된 견해가 많고, 일반적인 경우에는 안전하지 않지만, 제가 파악한 바에 따르면 우리는 고정된 안전 소수(Oakley group 14 [2])를 사용하므로 q의 차수는 문제가 없을 것입니다. 다만 이와 같은 맥락에서 추가로 의견이 있으시다면, 더 듣고 싶습니다.

가장 큰 대안은 1024비트 암호화로 전환하는 것입니다(그 경우에는 아마 160비트의 짧은 지수를 사용할 수도 있습니다). 어쨌든 이는 적절할 수 있으며, _PRE net에서 2048비트 암호화가 너무 부담스럽다면 _PRE net 내에서 전환을 단행할 수도 있습니다. 그렇지 않다면, 새 암호화 방식이 더 널리 배포되는 0.6.1.10 릴리스까지 기다려 그것이 필요한지 판단할 수 있습니다. 그러한 전환이 가능해 보이면 더 많은 정보를 제공하겠습니다.

[1] "짧은 지수를 사용하는 디피-헬만 키 합의에 관하여" -     van Oorschot, Weiner가 EuroCrypt 96에서 발표.  다음에서 미러링됨     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

어쨌든, _PRE net에서는 많은 진전이 있었고, 이에 관한 대부분의 논의는 irc2p의 #i2p_pre 채널에서 이루어지고 있습니다.

* 3) I2Phex 0.1.1.37

Complication이 최신 I2Phex 코드를 병합하고 패치하여 gwebcaches(웹 기반 피어 캐시)를 지원하도록 했으며, 이는 Rawn의 pycache port와 호환됩니다. 이는 사용자가 I2Phex를 다운로드해 설치한 뒤, "Connect to the network"를 누르면 1~2분 후 기존 I2Phex 피어에 대한 참조 일부를 가져와 네트워크에 합류할 수 있다는 뜻입니다. 더 이상 i2phex.hosts 파일을 수동으로 관리하거나 키를 수동으로 공유하느라 고생할 필요가 없습니다(w00t)! 기본으로 gwebcaches가 두 개 제공되지만, i2phex.cfg의 i2pGWebCache0, i2pGWebCache1, i2pGWebCache2 속성을 수정해 변경하거나 세 번째를 추가할 수 있습니다.

잘하셨습니다, Complication과 Rawn!

* 4) ???

지금은 이 정도면 될 것 같네요, 회의에 이미 늦었으니 오히려 다행이기도 하고요 :)  곧 #i2p에서 다들 봐요

=jr
