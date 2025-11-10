---
title: "2005-01-18자 I2P 상태 노트"
date: 2005-01-18
author: "jr"
description: "네트워크 상태, 0.5 tunnel 라우팅 설계, i2pmail.v2, 그리고 azneti2p_0.2 보안 수정을 다루는 주간 I2P 개발 현황 노트"
categories: ["status"]
---

안녕하세요 여러분, 주간 업데이트 시간이에요

* Index

1) Net status 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

음, 여기 보고할 만한 건 많지 않네요 - 지난주와 마찬가지로 여전히 잘 작동하고 있고, 네트워크 규모도 여전히 비슷하며, 아마 조금 더 커졌을지도 몰라요.  멋진 신규 사이트들이 몇 개 생겨나고 있어요 - 자세한 내용은 포럼 [1]과 orion [2]를 참고하세요.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

postman, dox, frosk, 그리고 cervantes(그리고 자신의 routers를 통해 tunnel(터널)로 데이터를 전달해 준 모든 분들 ;) )의 도움 덕분에, 우리는 하루치 분량의 메시지 크기 통계를 수집했습니다 [3]. 거기에는 두 가지 통계 세트가 있습니다 - 줌의 높이와 너비. 이는 다양한 메시지 패딩 전략이 네트워크 부하에 미치는 영향을 탐구하려는 요구에서 비롯되었으며, 0.5 tunnel 라우팅을 위한 초안 중 하나에서 설명된 바와 같이 [4] (ooOOoo 예쁜 그림들).

The scary part about what I found digging through those was that by using some pretty simple hand-tuned padding breakpoints, padding to those fixed sizes would still ended up with over 25% of the bandwidth wasted.  Yeah, I know, we're not going to do that. Perhaps y'all can come up with something better by digging through that raw data.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

사실, 그 [4] 링크는 tunnel 라우팅에 대한 0.5 계획의 현황으로 연결됩니다. Connelly가 [5]에 게시했듯이, 최근 IRC에서 일부 초안들을 두고 많은 논의가 있었고, polecat, bla, duck, nickster, detonate 등과 다른 이들이 제안과 날카로운 질문들(음, 빈정거림도요 ;) )로 기여했습니다. 일주일 남짓 지난 뒤, 우리는 [4]와 관련해 잠재적인 취약점을 발견했는데, 이는 공격자가 어떻게든 inbound tunnel gateway(수신 방향 tunnel 게이트웨이)를 장악하고 그 tunnel의 후반부에 있는 다른 피어 중 하나도 함께 제어할 수 있는 상황을 다룹니다. 대부분의 경우 이것만으로 엔드포인트가 드러나지는 않을 것이고, 네트워크가 성장할수록 그런 일을 해내기는 확률적으로도 어려워지겠지만, 그래도 Sucks (tm).

그래서 [6]이 등장합니다.  이것으로 그 문제를 해결하고, 임의 길이의 tunnel을 사용할 수 있게 하며, 세계 기아 문제까지 해결합니다 [7].  다만 공격자가 tunnel 안에 루프를 만들 수 있는 또 다른 문제가 생기기는 하지만, ElGamal/AES에서 사용되는 세션 태그에 관해 Taral이 작년에 제안한 [8] 내용을 바탕으로, 일련의 동기화된 의사난수 생성기를 사용하여 그로 인한 피해를 최소화할 수 있습니다 [9].

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] 어떤 진술이 거짓인지 맞혀 보세요? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

위 내용이 혼란스럽게 들리더라도 걱정하지 마세요 - 지금 공개적으로 복잡하고 까다로운 설계 문제들의 속사정이 철저히 검토되고 있는 모습을 보고 계신 겁니다. 반대로 위 내용이 *혼란스럽지 않게* 느껴지신다면 연락 주세요, 저희는 이 내용을 함께 머리를 맞대고 파고들 더 많은 분들을 늘 찾고 있으니까요 :)

어쨌든, 리스트 [10]에서 언급했듯이, 다음으로 남은 세부 사항을 정리하기 위해 두 번째 전략 [6]을 구현하고자 합니다. 현재 0.5의 계획은 하위 호환되지 않는 변경 사항들 - 새로운 tunnel 암호화 등 - 을 한데 모아 0.5.0으로 릴리스한 뒤, 그것이 네트워크에서 안정화되면 제안서에 설명된 대로 풀링 전략을 조정하는 작업 등 0.5의 다른 부분들 [11]로 넘어가 이를 0.5.1로 릴리스하는 것입니다. 이달 말까지 0.5.0을 출시할 수 있기를 바라지만, 지켜보겠습니다.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

얼마 전 postman이 차세대 메일 인프라[12]에 대한 실행 초안을 공개했는데, 정말 멋져 보입니다. 물론 우리가 더 생각해낼 수 있는 부가 기능들은 항상 더 있겠지만, 여러 면에서 아키텍처가 상당히 훌륭합니다. 지금까지 문서화된 내용[13]을 확인해 보시고, 의견을 postman에게 알려 주세요!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

내가 메일링 리스트[14]에 올렸듯이, 원래의 azureus용 azneti2p 플러그인에는 심각한 익명성 버그가 있었다. 문제는 일부 사용자는 익명이고 다른 사용자는 그렇지 않은 혼합 토렌트에서, 익명 사용자들이 I2P를 통해서가 아니라 비익명 사용자들에게 /직접/ 연결한다는 점이었다. Paul Gardner와 다른 azureus 개발자들은 매우 신속히 대응하여 즉시 패치를 배포했다. 내가 확인했던 문제는 azureus v. 2203-b12 + azneti2p_0.2에서는 더 이상 존재하지 않는다.

다만 잠재적인 익명성 문제를 검토하기 위해 코드를 전반적으로 감사해 보지는 못했으므로, "자기 책임하에 사용하십시오"(한편, I2P도 1.0 릴리스 이전에는 같은 말을 했습니다). 가능하시다면 Azureus 개발자들은 해당 플러그인에 대한 더 많은 피드백과 버그 리포트를 반길 것입니다. 물론 다른 문제가 밝혀지면 계속 알려드리겠습니다.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

보시다시피 여러 가지 일이 많이 벌어지고 있습니다. 제가 꺼낼 얘기는 대략 이 정도고, 더 논의하고 싶은 게 있으시면 40분 뒤 회의에 잠깐 들러 주세요(아니면 위의 내용에 대해 그냥 한바탕 하소연하고 싶으셔도 좋아요).

=jr
