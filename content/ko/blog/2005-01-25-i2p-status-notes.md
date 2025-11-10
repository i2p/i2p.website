---
title: "2005-01-25자 I2P 상태 노트"
date: 2005-01-25
author: "jr"
description: "0.5 tunnel 라우팅 진행 상황, SAM .NET 포팅, GCJ 컴파일, 및 UDP 트랜스포트 논의를 다루는 주간 I2P 개발 상태 노트"
categories: ["status"]
---

안녕하세요 여러분, 간단한 주간 현황 업데이트입니다

* Index

1) 0.5 상태 2) sam.net 3) gcj(자바용 GNU 컴파일러) 진행 상황 4) udp(사용자 데이터그램 프로토콜) 5) ???

* 1) 0.5 status

지난 한 주 동안 0.5 쪽에서 많은 진전이 있었습니다. 이전에 논의하던 문제들이 해결되어 암호화를 대폭 단순화하고 tunnel 루핑 문제를 제거했습니다. 새로운 기법[1]은 구현되었고 단위 테스트도 갖춰졌습니다. 다음으로 해당 tunnel들을 메인 router에 통합하기 위한 코드를 더 정리한 뒤, tunnel 관리 및 풀링 인프라스트럭처를 구축할 예정입니다. 그것들이 갖춰지면 sim(시뮬레이터)을 통해 돌려 보고, 궁극적으로 병렬 네트워크에서 충분히 안정화 테스트를 거친 다음 마무리하고 0.5라고 부르려 합니다.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead가 SAM 프로토콜을 .net용으로 새롭게 포팅했습니다 - c#, mono/gnu.NET과 호환됩니다 (smeghead 최고!).  이는 cvs의 i2p/apps/sam/csharp/ 아래에 있으며 nant 및 기타 도우미와 함께 제공됩니다 - 이제 .net 개발자 여러분 모두가 i2p로 개발을 시작할 수 있습니다 :)

* 3) gcj progress

smeghead는 요즘 맹활약 중입니다 - 최근 집계로는, 몇 가지 수정을 통해 최신 gcj [2] 빌드에서 router가 컴파일되고 있습니다 (w00t!).  아직 동작하진 않지만, gcj가 일부 내부 클래스 구문을 제대로 처리하지 못하는 문제를 우회하기 위한 수정은 분명한 진전입니다.    혹시 smeghead가 업데이트를 알려 줄 수 있을까요?

[2] http://gcc.gnu.org/java/

* 4) udp

여기서 특별히 덧붙일 말은 많지 않지만, Nightblade가 왜 우리가 UDP를 선택하는지에 대해 포럼에서 흥미로운 우려 사항들 [3]을 제기했습니다. 비슷한 우려가 있거나 제가 답글에서 언급한 문제들을 어떻게 대응할 수 있을지에 대한 다른 제안이 있다면, 부디 의견을 보태 주세요!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

그래, 알겠어, 또 회의록을 늦게 올렸네, 내 월급에서 깎아도 돼 ;)  아무튼, 할 일이 많으니까 회의를 위해 채널에 들르거나, 나중에 올라오는 로그를 확인하거나, 할 말이 있으면 메일링 리스트에 글을 올려 줘.  아, 참고로, 결국 못 이기고 i2p 안에서 블로그를 시작했어 [4].

=jr [4] http://jrandom.dev.i2p/ (키는 http://dev.i2p.net/i2p/hosts.txt에 있음)
