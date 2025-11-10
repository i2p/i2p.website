---
title: "2005-10-11자 I2P 상태 노트"
date: 2005-10-11
author: "jr"
description: "0.6.1.2 릴리스의 성공, 안전하지 않은 IRC 메시지를 필터링하기 위한 새로운 I2PTunnelIRCClient 프록시, Syndie CLI와 RSS에서 SML로의 변환, 그리고 I2Phex 통합 계획을 다루는 주간 업데이트"
categories: ["status"]
---

안녕하세요, 여러분. 또 화요일이네요.

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) 스테가노그래피와 다크넷 (플레임워 관련) 6) ???

* 1) 0.6.1.2

지난주 0.6.1.2 릴리스는 지금까지 꽤 순조롭게 진행되었습니다 - 네트워크의 75%가 업그레이드했고, HTTP POST도 잘 동작하며, 스트리밍 라이브러리가 데이터를 상당히 효율적으로 전송하고 있습니다 (HTTP 요청에 대한 전체 응답이 종단 간 단 한 번의 왕복으로 수신되는 경우가 흔합니다). 네트워크도 조금 성장했는데 - 안정 시에는 피어 수가 대략 400개 수준으로 보이지만, 주말 동안 digg/gotroot [1] 언급이 정점에 달했을 때 churn(노드의 잦은 이탈·유입)과 함께 6-700까지 더 치솟았습니다.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (그래, 정말 오래된 기사라는 건 알아, 하지만 누군가 다시 찾아냈어)

0.6.1.2가 나온 이후로 더 많은 좋은 것들이 추가되었습니다 - 최근 irc2p netsplits(IRC 네트워크 분할 현상)의 원인이 밝혀졌고(수정됨), SSU의 패킷 전송에도 상당한 개선이 이루어졌습니다(패킷의 5% 이상을 절약). 0.6.1.3이 정확히 언제 나올지는 잘 모르겠지만, 아마 이번 주 후반쯤일지도 모르겠습니다. 지켜보죠.

* 2) I2PTunnelIRCClient

얼마 전, 약간의 논의 끝에, dust가 I2PTunnel - "ircclient" 프록시라는 새로운 확장 기능을 신속히 만들어냈습니다. 이는 I2P를 통해 클라이언트와 서버 사이에서 주고받는 내용을 필터링하여, 안전하지 않은 IRC 메시지를 제거하고 조정이 필요한 메시지는 다시 작성하는 방식으로 동작합니다. 몇 차례 테스트해 본 결과 꽤 좋아 보이며, dust가 이를 I2PTunnel에 기여해 이제 웹 인터페이스를 통해 사용자에게 제공되고 있습니다. irc2p 커뮤니티가 안전하지 않은 메시지를 버리도록 IRC 서버를 패치해 온 것은 훌륭했지만, 이제는 그런 작업을 그들이 해 주기를 신뢰할 필요가 없습니다 - 로컬 사용자가 자신의 필터링을 직접 제어할 수 있습니다.

사용하는 것은 꽤 쉽습니다 - 이전처럼 IRC용 "Client proxy"를 만드는 대신, 그냥 "IRC proxy"를 만들면 됩니다. 기존의 "Client proxy"를 "IRC proxy"로 전환하고 싶다면, i2ptunnel.config 파일을 (민망하지만) 편집하여 "tunnel.1.type=client"를 "tunnel.1.ircclient"로 변경하세요(또는 프록시에 맞는 번호로 바꾸세요).

순조롭게 진행되면, 다음 릴리스에서 IRC 연결을 위한 기본 I2PTunnel 프록시 유형으로 지정될 것입니다.

잘했어 dust, 고마워!

* 3) Syndie

Ragnarok의 예약된 syndication(콘텐츠 배포) 기능도 잘 진행되고 있고, 0.6.1.2가 나온 이후로 새로운 기능이 두 가지 더 나왔다 - 나는 Syndie [2]에 게시할 수 있는 새롭고 단순화된 CLI(명령줄 인터페이스)를 추가했고, dust (만세, dust!)가 RSS/Atom 피드에서 콘텐츠를 끌어오고 그 안에서 참조된 enclosures(첨부 항목)나 이미지도 함께 받아와 RSS 콘텐츠를 SML(Syndie Markup Language)로 변환하는 코드를 재빨리 작성했다(!!!) [3][4].

이 두 가지를 함께 놓고 보면 함의는 분명합니다. 추가 소식이 있을 때 알려드리겠습니다.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (조만간 CVS에 통합할 예정입니다)

* 4) I2Phex

소문에 따르면 I2Phex는 꽤 잘 작동하지만, 시간 경과에 따라 발생하는 문제들이 여전히 지속된다. 어떻게 진행할지에 관해 포럼 [5]에서 몇 가지 논의가 있었고, Phex의 수석 개발자인 GregorK도 참여하여 I2Phex 기능을 다시 Phex에 통합하는 데 지지 의사를 밝혔다(혹은 최소한 메인라인 Phex가 전송 계층을 위한 간단한 플러그인 인터페이스를 제공하도록 하자는 것이다).

이건 정말 끝내줄 일입니다. 유지보수해야 할 코드가 훨씬 줄어들고, 게다가 코드베이스를 개선하려는 Phex 팀의 작업 성과도 그대로 누릴 수 있으니까요. 다만 이게 성사되려면, 몇몇 해커들이 자진해서 나와 마이그레이션(이전)을 주도해야 합니다. I2Phex 코드에는 sirup이 어느 부분을 변경했는지가 꽤 명확하게 드러나 있어서 그리 어렵진 않겠지만, 그렇다고 아주 사소한 일은 아닐 겁니다 ;)

지금 당장 이 일을 시작할 시간은 없지만, 도와주고 싶다면 포럼에 들러 주세요.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

메일링 리스트 [6]에서는 최근 들어 스테가노그래피(은닉기법)와 다크넷에 관한 논의가 꽤 활발했습니다. 이 주제는 주로 제목이 "I2P conspiracy theories flamewar"인 Freenet tech list [7]로 옮겨갔지만, 여전히 진행 중입니다.

게시물 자체에 없는 걸 제가 더 보탤 수 있을지 잘 모르겠지만, 몇몇 분들은 그 토론이 I2P와 Freenet을 이해하는 데 도움이 되었다고 하시니 한 번 둘러볼 가치는 있을지도 모르겠습니다. 아니면 아닐 수도요 ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

보시다시피 흥미로운 일들이 많이 벌어지고 있고, 제가 분명 놓친 것도 있을 거예요. 몇 분 뒤에 열리는 주간 회의에 맞춰 #i2p에 잠깐 들러 인사해 주세요!

=jr
