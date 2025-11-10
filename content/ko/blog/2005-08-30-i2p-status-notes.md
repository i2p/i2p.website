---
title: "2005-08-30에 대한 I2P 상태 노트"
date: 2005-08-30
author: "jr"
description: "NAT 문제, floodfill netDb 배포, Syndie 국제화 진행 상황을 포함한 0.6.0.3 네트워크 상태에 대한 주간 업데이트"
categories: ["status"]
---

안녕하세요, 여러분. 이번 주도 그 시간이 돌아왔네요

* Index

1) 네트워크 상태 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

0.6.0.3가 출시된 지 일주일이 되었고, 보고 결과는 꽤 좋은 편이지만 일부에게는 로깅과 표시가 꽤 혼란스러웠다. 몇 분 전 기준으로 I2P는 상당수의 사용자가 NAT나 방화벽을 잘못 구성했다고 보고하고 있는데, 241개 피어 중 41개는 상태가 ERR-Reject로 바뀌었고, 200개는 (명시적인 상태를 받을 수 있을 때) 정상적으로 OK였다. 이는 좋은 상황은 아니지만, 무엇을 더 해야 하는지에 좀 더 초점을 맞추는 데에는 도움이 되었다.

릴리스 이후 오래 지속된 오류 상황에 대한 몇 가지 버그 수정이 있었고, 그 결과 현재 CVS HEAD는 0.6.0.3-4까지 올라갔습니다. 이는 이번 주 후반에 0.6.0.4로 배포될 가능성이 높습니다.

* 2) floodfill netDb

제 블로그[2]에서 논의한 바[1]와 같이, 우리는 현재 관측되는 경로 제한 현상(routers의 20%)을 해결하고 전반을 조금 단순화하기 위해 하위 호환 netDb를 새로 시험해 보고 있습니다. floodfill netDb는 추가 설정 없이 0.6.0.3-4의 일부로 배포되며, 기본적으로 기존 kademlia db로 되돌아가기 전에 floodfill db 내부에서 먼저 질의하는 방식으로 동작합니다. 몇 분이 시험에 도움을 주고 싶다면 0.6.0.3-4로 올려서 한 번 써 보세요!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Syndie 개발은 매우 순조롭게 진행되고 있으며, 완전한 원격 신디케이션이 동작 중이고 I2P의 요구에 맞게 최적화되어 있습니다(HTTP 요청 수를 최소화하고, 대신 결과와 업로드를 multipart HTTP POST로 묶습니다). 새로운 원격 신디케이션을 통해 사용자는 로컬 Syndie 인스턴스를 실행하여 오프라인으로 읽고 게시할 수 있고, 이후 다른 사람의 Syndie와 동기화하여 새 게시물을 내려받고 로컬에서 만든 게시물을 올릴 수 있습니다(대량으로든, 블로그 단위로든, 게시물 단위로든).

공개 Syndie 사이트 중 하나는 syndiemedia.i2p(웹에서도 http://syndiemedia.i2p.net/에서 접속할 수 있음)이며, 공개 아카이브는 http://syndiemedia.i2p/archive/archive.txt에서 이용할 수 있습니다(해당 주소를 Syndie 노드에 지정하여 동기화하십시오). 해당 syndiemedia의 'front page'는 기본적으로 제 블로그만 포함하도록 필터링되어 있지만, 드롭다운을 통해 다른 블로그에도 접근할 수 있고 그에 따라 기본값을 조정할 수 있습니다. (시간이 지나면서 syndiemedia.i2p의 기본값은 소개 글과 블로그 모음으로 변경되어 syndie에 들어가는 좋은 진입점이 될 것입니다).

여전히 진행 중인 작업 중 하나는 Syndie 코드베이스의 국제화입니다. 저는 어떤 머신(잠재적으로 서로 다른 문자 집합/로케일/등을 가질 수 있음)에서든 어떤 콘텐츠(어떤 문자 집합/로케일/등)와도 제대로 동작하고, 사용자의 브라우저가 올바르게 해석할 수 있도록 데이터를 깔끔하게 제공하도록 로컬 사본을 수정해 두었습니다. 다만 Syndie가 사용하는 Jetty 구성 요소 하나에서 문제에 부딪혔는데, 국제화된 멀티파트 요청(multipart requests)을 처리하는 그들의 클래스가 문자 집합을 고려하지 않습니다. 아직은 ;)

어쨌든, 국제화 부분이 정리되기만 하면 모든 언어에서 콘텐츠와 블로그를 표시하고 편집할 수 있게 됩니다(물론 아직 번역되지는 않습니다). 그때까지는 국제화가 완료되었을 때 지금 만든 콘텐츠가 깨질 수도 있습니다(서명된 콘텐츠 영역 안에 UTF-8 문자열이 있기 때문입니다). 하지만 그래도 마음껏 이것저것 해 보셔도 되고, 가능하면 오늘 밤이나 내일쯤에는 마무리할 수 있기를 바랍니다.

또한 SML [3]에 대해 아직 논의 단계에 있는 몇 가지 아이디어로는, 사용자가 즐겨 쓰는 BT 클라이언트(susibt, i2p-bt, azneti2p, 혹은 I2P가 아닌 BT 클라이언트)에서 첨부된 토렌트를 한 번의 클릭으로 곧바로 시작할 수 있게 해 주는 [torrent attachment="1"]my file[/torrent] 태그가 포함됩니다. 다른 종류의 훅(hook)에 대한 수요가 있나요(예: [ed2k] 태그)? 아니면 Syndie에서 콘텐츠를 푸시하는 전혀 다른 기발한 아이디어가 있나요?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

어쨌든, 지금 진행되는 일이 아주 많으니 10분 후에 irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p 또는 freenode.net에서 열리는 회의에 잠깐 들러 주세요!

=jr
