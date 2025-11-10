---
title: "2005-02-08자 I2P 상태 노트"
date: 2005-02-08
author: "jr"
description: "0.4.2.6 업데이트, Bloom 필터를 포함한 0.5 tunnel 진행 상황, i2p-bt 0.1.6, 및 Fortuna PRNG를 다루는 주간 I2P 개발 현황 노트"
categories: ["status"]
---

안녕하세요 여러분, 다시 업데이트할 시간이에요

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

그렇게 느껴지지는 않겠지만, 0.4.2.6 릴리스가 나온 지 벌써 한 달이 넘었고 전반적으로 꽤 괜찮은 상태를 유지하고 있습니다. 그 이후로 꽤 유용한 업데이트 [1]가 이어졌지만, 새 릴리스를 서둘러 배포해야 할 만큼의 치명적인 문제는 없었습니다. 하지만 지난 하루이틀 사이에 정말 좋은 버그 수정들이 들어왔습니다(anon과 Sugadude에게 감사!), 그리고 지금이 0.5 릴리스가 코앞이 아니었다면 아마 바로 패키징해서 내보냈을 겁니다. anon의 업데이트는 스트리밍 라이브러리의 경계 조건을 수정했는데, 이 문제가 BT(비트토렌트)와 다른 대용량 전송에서 보이던 많은 타임아웃의 원인이었습니다. 모험할 기분이라면 CVS HEAD를 받아서 한번 써 보세요. 물론 다음 릴리스를 기다리셔도 됩니다.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

0.5 관련해서 매우 많은 진전이 있었습니다(이는 i2p-cvs 메일링 리스트 [2]에 있는 누구나가 증언할 수 있듯이).  모든 tunnel 업데이트와 다양한 성능 튜닝을 테스트했으며, 여러 [3] enforced ordering algorithms(강제 순서화 알고리즘)을 많이 포함하고 있지는 않지만 기본은 충실히 갖추었습니다.  또한 XLattice [5]의 (BSD 라이선스) Bloom 필터 [4] 세트를 통합하여, 메시지별 메모리 사용 없이 그리고 거의 0ms의 오버헤드로 재전송 공격을 탐지할 수 있게 했습니다.  우리의 요구에 맞추기 위해 필터를 간단히 확장해 시간이 지나면 소멸하도록 했으며, 그 결과 특정 tunnel이 만료된 이후에는 그 tunnel에서 보았던 IV(초기화 벡터)가 더 이상 해당 필터에 남아 있지 않게 됩니다.

0.5 릴리스에 가능한 한 많은 것을 포함하려고 노력하고 있지만, 동시에 우리는 예기치 못한 일을 예상해야 한다는 것도 알고 있습니다 — 즉, 이를 개선하는 가장 좋은 방법은 여러분이 직접 사용해 보고, 여러분에게 어떻게 작동하는지(그리고 작동하지 않는지)에서 배우는 것입니다. 이를 돕기 위해, 앞서 말씀드렸듯이, 우리는 하위 호환성을 깨뜨리는 0.5 릴리스를(가능하면 다음 주에) 내놓고, 그다음 거기서부터 개선 작업을 진행하여 준비가 되는 대로 0.5.1 릴리스를 빌드할 예정입니다.

로드맵 [6]을 돌아보면, 0.5.1로 연기되는 것은 엄격한 순서 보장뿐이다. 시간이 지나면서 throttling(전송률 제한)과 load balancing(부하 분산)도 개선될 것이라 확신하지만, 그 부분은 아마 앞으로도 계속 손질하게 될 것으로 예상한다. 또한 0.5에 포함하기를 바랐던 다운로드 도구와 원클릭 업데이트 코드 같은 다른 항목들도 논의되었지만, 그것들 역시 연기될 것으로 보인다.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck이 새로운 i2p-bt 릴리스를 패치해 공개했습니다(야호!). 평소와 같은 위치에서 받을 수 있으니, 뜨거울 때 얼른 받아가세요 [7]. 이번 업데이트와 anon의 streaming lib 패치 덕분에, 몇몇 파일을 시딩하는 동안 제 업링크 대역폭이 거의 포화되더군요, 그러니 한번 써보세요.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

지난주 회의에서 언급했듯이, smeghead는 최근 다양한 업데이트를 쉼 없이 진행해 왔고, gcj에서 I2P를 동작시키기 위해 분투하는 과정에서 일부 JVM에서 정말 끔찍한 PRNG(의사난수 생성기) 문제가 드러나 신뢰할 수 있는 PRNG의 도입이 사실상 불가피해졌습니다. GNU-Crypto 측으로부터 회신을 받았는데, 그들의 fortuna 구현은 아직 실제로 배포되지는 않았지만 우리의 요구에 가장 잘 맞는 것으로 보입니다. 0.5 릴리스에 포함시킬 수도 있겠지만, 필요한 양의 난수 데이터를 제공하도록 조정해야 하므로 0.5.1로 연기될 가능성이 큽니다.

* 5) ???

Lots of things going on, and there has been a burst of activity on the forum [8] lately as well, so I'm sure I've missed some things. In any case, swing on by the meeting in a few minutes and say whats on your mind (or just lurk and throw in the random snark)

=jr [8] http://forum.i2p.net/
